"""Draft restricted semantic frontend and ordinary GNU target lowering.

Generated development draft; Python rules remain in business_recruitment.
Only these explicit structural forms and declared literal rules are admitted.
Not a general Python compiler or a complete CPU equivalence proof.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import RECRUITMENT_BINDINGS

APPROVED = {'business_budget': {'append_six_place_decimal_value'},
 'business_display': {'append_live_command_string_words'},
 'contexts_recruitment': {'SeparatorRowContext',
                          'SeparatorRowResult',
                          'TilePairContext',
                          'TilePairResult',
                          'checked_context'},
 'domain': {'Boundary',
            'Cursor',
            'GameState',
            'Long',
            'Word',
            'checked_state',
            'descending_inclusive',
            'divu_retained',
            'high16',
            'low16',
            'negative_word',
            'replace_word',
            'swap_words',
            'u16',
            'u32',
            'uint'}}

DECLARATIONS = {'_queue_cursor': {'signature': 'state: GameState',
                   'returns': 'Cursor',
                   'flow': "return state.display_queue.cursor(state.scalar('queue_offset'))"},
 '_finish_queue': {'signature': 'state: GameState, destination: Cursor, length: Word',
 'returns': 'None',
 'flow': 'checked_state(state)\n'
         '_finish_queue_fields(EquipmentMenuMemory(state), destination, length)'},
 '_paired_tiles': {'signature': 'state: GameState, context: TilePairContext, row_stride: Word',
 'returns': 'TilePairResult',
 'flow': 'context = checked_context(context, TilePairContext, state)\n'
         'fields = _paired_tiles_fields(EquipmentMenuMemory(state), context.destination, '
         'low16(context.tile), low16(context.counter), row_stride)\n'
         'return TilePairResult(fields.destination, replace_word(context.tile, fields.value), '
         'replace_word(context.counter, fields.field_if_written))'},
 'append_recruitment_paired_tiles': {'signature': 'state: GameState, context: TilePairContext',
                                     'returns': 'TilePairResult',
                                     'flow': 'state = checked_state(state)\n'
                                             'return _paired_tiles(state, context, 34)'},
 'append_equipment_paired_tiles': {'signature': 'state: GameState, context: TilePairContext',
                                   'returns': 'TilePairResult',
                                   'flow': 'state = checked_state(state)\n'
                                           'return _paired_tiles(state, context, 34)'},
 'append_candidate_paired_tiles': {'signature': 'state: GameState, context: TilePairContext',
                                   'returns': 'TilePairResult',
                                   'flow': 'state = checked_state(state)\n'
                                           'return _paired_tiles(state, context, 20)'},
 'append_candidate_separator_row': {'signature': 'state: GameState, context: SeparatorRowContext',
                                    'returns': 'SeparatorRowResult',
                                    'flow': 'state = checked_state(state)\n'
                                            'context = checked_context(context, '
                                            'SeparatorRowContext, state)\n'
                                            'destination = context.destination\n'
                                            'destination.append_word(8)\n'
                                            'destination.append_word(low16(context.coordinate))\n'
                                            'coordinate = replace_word(context.coordinate, '
                                            'u16(low16(context.coordinate) + 256))\n'
                                            'destination.append_word(50050)\n'
                                            'for _ in range(6):\n'
                                            '    destination.append_word(49153)\n'
                                            'destination.append_word(52098)\n'
                                            'return SeparatorRowResult(destination, coordinate)'},
 '_append_large_dialog': {'signature': 'state: GameState, first_labels: tuple, second_labels: tuple',
 'returns': 'None',
 'flow': 'checked_state(state)\n'
         '_append_large_dialog_fields(EquipmentMenuMemory(state), first_labels, second_labels)'},
 'append_recruitment_dialog_frame': {'signature': 'state: GameState',
                                     'returns': 'None',
                                     'flow': 'state = checked_state(state)\n'
                                             '_append_large_dialog(state, ((49181, 3), (49157, '
                                             '1)), ((49161, 3),))\n'
                                             "state.set_scalar('queue_dirty_flags', "
                                             "state.scalar('queue_dirty_flags') | 1)"},
 'append_equipment_dialog_frame': {'signature': 'state: GameState',
                                   'returns': 'None',
                                   'flow': 'state = checked_state(state)\n'
                                           '_append_large_dialog(state, ((49169, 3), (49185, 1)), '
                                           '((49177, 1), (49189, 1), (49185, 1)))'},
 'prepare_player_recruitment_capacity': {'signature': 'state: GameState',
                                         'returns': 'Word',
                                         'flow': 'state = checked_state(state)\n'
                                                 "state.set_scalar('recruitment_input', 0)\n"
                                                 "state.set_scalar('action_amount', 0)\n"
                                                 "state.set_scalar('amount_digit_position', 3)\n"
                                                 "city_offset = u16(state.scalar('command_city') "
                                                 '<< 2)\n'
                                                 "state.set_scalar('recruitment_capacity', "
                                                 'state.city_gold.long(city_offset))\n'
                                                 'gold_units = '
                                                 "low16(divu_retained(state.scalar('recruitment_capacity'), "
                                                 '100))\n'
                                                 'source = '
                                                 'state.recruitment_source.long(city_offset)\n'
                                                 'source_units = u32(low16(source) * 10 + '
                                                 'swap_words(high16(source) * 10))\n'
                                                 'remaining_pool = u32(100000 - '
                                                 'state.recruitment_pool.long(city_offset))\n'
                                                 'pool_units = low16(divu_retained(remaining_pool, '
                                                 '100))\n'
                                                 'available_units = min(source_units, pool_units)\n'
                                                 'if gold_units > available_units:\n'
                                                 '    gold_units = low16(available_units)\n'
                                                 "    state.set_scalar('recruitment_capacity', "
                                                 'u32(low16(available_units) * 100))\n'
                                                 'digit_start = 3\n'
                                                 'if gold_units >= 10:\n'
                                                 '    digit_start -= 1\n'
                                                 '    if gold_units >= 100:\n'
                                                 '        digit_start -= 1\n'
                                                 '        if gold_units >= 1000:\n'
                                                 '            digit_start -= 1\n'
                                                 "state.set_scalar('recruitment_digit_start', "
                                                 'digit_start)\n'
                                                 'return digit_start'},
 '_update_blink_cursor': {'signature': 'state: GameState, x: Word',
                          'returns': 'None',
                          'flow': "count = state.scalar('cursor_blink_counter')\n"
                                  'if count >= 24:\n'
                                  "    state.set_scalar('cursor_blink_counter', 24)\n"
                                  "state.set_scalar('cursor_blink_counter', "
                                  "u16(state.scalar('cursor_blink_counter') - 1))\n"
                                  "if state.scalar('cursor_blink_counter') >= 12:\n"
                                  "    y = u16(u16(state.scalar('amount_digit_position') << 3) + "
                                  '248)\n'
                                  '    append_live_command_string_words(state, '
                                  'state.amount_cursor_shape, x, y)'},
 'update_recruitment_input_cursor': {'signature': 'state: GameState',
                                     'returns': 'None',
                                     'flow': 'state = checked_state(state)\n'
                                             '_update_blink_cursor(state, 80)'},
 'update_recruitment_total_cursor': {'signature': 'state: GameState',
                                     'returns': 'None',
                                     'flow': 'state = checked_state(state)\n'
                                             '_update_blink_cursor(state, 104)'},
 '_append_input_digits': {'signature': 'state: GameState, scalar_name: str',
 'returns': 'None',
 'flow': 'checked_state(state)\n'
         '_append_input_digits_fields(EquipmentMenuMemory(state), scalar_name)'},
 'append_recruitment_input_digits': {'signature': 'state: GameState',
                                     'returns': 'None',
                                     'flow': 'state = checked_state(state)\n'
                                             "_append_input_digits(state, 'recruitment_input')"},
 'append_equipment_input_digits': {'signature': 'state: GameState',
                                   'returns': 'None',
                                   'flow': 'state = checked_state(state)\n'
                                           "_append_input_digits(state, 'equipment_input')"},
 '_append_total_digits': {'signature': 'state: GameState, value: Long',
 'returns': 'None',
 'flow': 'checked_state(state)\n_append_total_digits_fields(EquipmentMenuMemory(state), value)'},
 'append_recruitment_total_digits': {'signature': 'state: GameState',
                                     'returns': 'None',
                                     'flow': 'state = checked_state(state)\n'
                                             '_append_total_digits(state, '
                                             "state.scalar('action_amount'))"},
 'append_equipment_total_digits': {'signature': 'state: GameState',
                                   'returns': 'None',
                                   'flow': 'state = checked_state(state)\n'
                                           "if state.scalar('command_id') == 27:\n"
                                           "    value = state.scalar('special_equipment_amount')\n"
                                           'else:\n'
                                           "    value = state.scalar('recruitment_input')\n"
                                           '_append_total_digits(state, value)'},
 '_append_amount_cursor': {'signature': 'state: GameState, y_base: Word',
                           'returns': 'None',
                           'flow': "y = u16(u16(state.scalar('amount_digit_position') << 3) + "
                                   'y_base)\n'
                                   'append_live_command_string_words(state, '
                                   'state.amount_cursor_shape, 88, y)'},
 'append_equipment_amount_cursor': {'signature': 'state: GameState',
                                    'returns': 'None',
                                    'flow': 'state = checked_state(state)\n'
                                            "if state.scalar('controller_edges') & 32:\n"
                                            '    return\n'
                                            "if state.scalar('ui_gate_flags') & 8:\n"
                                            '    return\n'
                                            '_append_amount_cursor(state, 144)'},
 'append_candidate_amount_cursor': {'signature': 'state: GameState',
                                    'returns': 'None',
                                    'flow': 'state = checked_state(state)\n'
                                            "if state.scalar('ui_gate_flags') & 8:\n"
                                            '    return\n'
                                            '_append_amount_cursor(state, 144)'},
 'clear_equipment_dialog_rows': {'signature': 'state: GameState',
                                 'returns': 'None',
                                 'flow': 'state = checked_state(state)\n'
                                         'destination = _queue_cursor(state)\n'
                                         'for displacement in (204, 170, 136, 102, 68, 34):\n'
                                         '    destination.set_word(0, 15, displacement)\n'
                                         'destination.append_word(15)\n'
                                         'for displacement, coordinate in ((204, 51092), (170, '
                                         '50964), (136, 50836), (102, 50708), (68, 50580), (34, '
                                         '50452)):\n'
                                         '    destination.set_word(0, coordinate, displacement)\n'
                                         'destination.append_word(50324)\n'
                                         'for _ in range(15):\n'
                                         '    for displacement in (204, 170, 136, 102, 68, 34):\n'
                                         '        destination.set_word(0, 0, displacement)\n'
                                         '    destination.append_word(0)\n'
                                         'destination.set_word(0, 0, 204)\n'
                                         "state.set_scalar('queue_offset', "
                                         "u16(state.scalar('queue_offset') + 238))"},
 '_append_candidate_row_pair': {'signature': 'state: GameState, destination: Cursor, coordinate: '
                                             'Word, labels: tuple',
                                'returns': 'tuple[Cursor, Word]',
                                'flow': 'destination.set_word(0, 8, 20)\n'
                                        'destination.append_word(8)\n'
                                        'destination.set_word(0, coordinate, 20)\n'
                                        'destination.append_word(u16(coordinate - 128))\n'
                                        'coordinate = u16(coordinate + 128)\n'
                                        'destination.set_word(0, 50050, 20)\n'
                                        'destination.append_word(50050)\n'
                                        'for tile, counter in labels:\n'
                                        '    destination = _paired_tiles(state, '
                                        'TilePairContext(destination, tile, counter), '
                                        '20).destination\n'
                                        'destination.set_word(0, 52098, 20)\n'
                                        'destination.append_word(52098)\n'
                                        'destination.base = u32(destination.base + 20)\n'
                                        'return (destination, coordinate)'},
 'append_candidate_dialog_frame': {'signature': 'state: GameState',
                                   'returns': 'None',
                                   'flow': 'state = checked_state(state)\n'
                                           'destination = _queue_cursor(state)\n'
                                           'destination.append_word(8)\n'
                                           'destination.append_word(50208)\n'
                                           'destination.append_word(50048)\n'
                                           'for _ in range(6):\n'
                                           '    destination.append_word(50049)\n'
                                           'destination.append_word(52096)\n'
                                           'destination, coordinate = '
                                           '_append_candidate_row_pair(state, destination, 50464, '
                                           '((49157, 5),))\n'
                                           'separator = append_candidate_separator_row(state, '
                                           'SeparatorRowContext(destination, coordinate))\n'
                                           'destination, coordinate = (separator.destination, '
                                           'low16(separator.next_coordinate))\n'
                                           'destination, coordinate = '
                                           '_append_candidate_row_pair(state, destination, '
                                           'coordinate, ((49169, 1), (49161, 3)))\n'
                                           'separator = append_candidate_separator_row(state, '
                                           'SeparatorRowContext(destination, coordinate))\n'
                                           'destination, coordinate = (separator.destination, '
                                           'low16(separator.next_coordinate))\n'
                                           'destination, coordinate = '
                                           '_append_candidate_row_pair(state, destination, '
                                           'coordinate, ((49157, 1), (49173, 1), (49169, 1)))\n'
                                           'destination.append_word(8)\n'
                                           'destination.append_word(coordinate)\n'
                                           'destination.append_word(54144)\n'
                                           'for _ in range(6):\n'
                                           '    destination.append_word(54145)\n'
                                           'destination.append_word(56192)\n'
                                           '_finish_queue(state, destination, 200)'},
 'clear_candidate_dialog_rows': {'signature': 'state: GameState',
                                 'returns': 'None',
                                 'flow': 'state = checked_state(state)\n'
                                         'destination = _queue_cursor(state)\n'
                                         'rows = (180, 160, 140, 120, 100, 80, 60, 40, 20)\n'
                                         'for displacement in rows:\n'
                                         '    destination.set_word(0, 8, displacement)\n'
                                         'destination.append_word(8)\n'
                                         'for index, displacement in enumerate(rows):\n'
                                         '    destination.set_word(0, 51360 - index * 128, '
                                         'displacement)\n'
                                         'destination.append_word(50208)\n'
                                         'for _ in range(8):\n'
                                         '    for displacement in rows:\n'
                                         '        destination.set_word(0, 32768, displacement)\n'
                                         '    destination.append_word(32768)\n'
                                         'destination.set_word(0, 0, 180)\n'
                                         "state.set_scalar('queue_offset', "
                                         "u16(state.scalar('queue_offset') + 200))"},
 'update_equipment_category': {'signature': 'state: GameState',
                               'returns': 'None',
                               'flow': 'state = checked_state(state)\n'
                                       "held = state.scalar('controller_held') & 3\n"
                                       'if held == 0:\n'
                                       "    state.set_scalar('controller_repeat', 1)\n"
                                       '    return\n'
                                       "repeat = u16(state.scalar('controller_repeat') - 1)\n"
                                       "state.set_scalar('controller_repeat', repeat)\n"
                                       'if repeat:\n'
                                       '    return\n'
                                       "state.set_scalar('controller_repeat', 12)\n"
                                       "category = state.scalar('equipment_category')\n"
                                       'if held & 2:\n'
                                       "    state.set_scalar('equipment_category', 0 if category "
                                       ">= 2 else u16(state.scalar('equipment_category') + 1))\n"
                                       'else:\n'
                                       "    state.set_scalar('equipment_category', 2 if category "
                                       "== 0 else u16(state.scalar('equipment_category') - 1))"},
 'append_equipment_category_cursor': {'signature': 'state: GameState',
                                      'returns': 'None',
                                      'flow': 'state = checked_state(state)\n'
                                              "if state.scalar('controller_edges') & 32:\n"
                                              '    return\n'
                                              "held = state.scalar('controller_held') & 3\n"
                                              "if held == 0 and state.scalar('ui_gate_flags') & "
                                              '16:\n'
                                              '    return\n'
                                              "category = state.scalar('equipment_category')\n"
                                              'x = u16(u16(u16(category << 1) + '
                                              "state.scalar('equipment_category')) << 3)\n"
                                              'x = u16(x + 64)\n'
                                              'append_live_command_string_words(state, '
                                              'state.equipment_category_cursor_shape, x, 128)'},
 'prepare_selected_training_cost_steps': {'signature': 'state: GameState',
                                          'returns': 'Long',
                                          'flow': 'state = checked_state(state)\n'
                                                  'source = state.command_candidates.cursor()\n'
                                                  'total = 0\n'
                                                  'while True:\n'
                                                  '    candidate = source.next_word()\n'
                                                  '    if negative_word(candidate):\n'
                                                  '        break\n'
                                                  '    if candidate & 16384:\n'
                                                  '        total = u32(total + '
                                                  'state.officer_troops.long(u16(candidate << '
                                                  '2)))\n'
                                                  '        total = u32(total + 100)\n'
                                                  'packed = divu_retained(total, 100)\n'
                                                  'if total // 100 > 65535:\n'
                                                  "    raise Boundary('original training-cost DIVU "
                                                  "overflow flags undefined')\n"
                                                  'if low16(packed) == 0:\n'
                                                  '    packed = replace_word(packed, 1)\n'
                                                  'base_cost = low16(packed)\n'
                                                  "state.set_scalar('training_cost_step_ones', "
                                                  'base_cost)\n'
                                                  'tens = u32(base_cost * 10)\n'
                                                  "state.set_scalar('training_cost_step_tens', "
                                                  'tens)\n'
                                                  "state.set_scalar('training_cost_step_hundreds', "
                                                  'u32(low16(tens) * 10))\n'
                                                  'return base_cost'},
 'update_selected_training_amount': {'signature': 'state: GameState',
                                     'returns': 'None',
                                     'flow': 'state = checked_state(state)\n'
                                             "vertical = state.scalar('controller_held') & 12\n"
                                             'if vertical:\n'
                                             "    repeat = u16(state.scalar('controller_repeat') - "
                                             '1)\n'
                                             "    state.set_scalar('controller_repeat', repeat)\n"
                                             '    if repeat:\n'
                                             '        return\n'
                                             "    state.set_scalar('controller_repeat', 12)\n"
                                             '    if not vertical & 8:\n'
                                             '        position = '
                                             "state.scalar('amount_digit_position')\n"
                                             '        if position == 0:\n'
                                             '            return\n'
                                             '        offset = u16(u16(1 - '
                                             "state.scalar('amount_digit_position')) << 2)\n"
                                             '        required = '
                                             'state.training_cost_steps.long(offset, 4)\n'
                                             '        if required <= '
                                             "state.scalar('training_cost_limit'):\n"
                                             '            '
                                             "state.set_scalar('amount_digit_position', "
                                             "u16(state.scalar('amount_digit_position') - 1))\n"
                                             '        return\n'
                                             "    if state.scalar('amount_digit_position') >= 2:\n"
                                             '        return\n'
                                             "    state.set_scalar('amount_digit_position', "
                                             "u16(state.scalar('amount_digit_position') + 1))\n"
                                             "horizontal = state.scalar('controller_held') & 3\n"
                                             'if horizontal == 0:\n'
                                             "    state.set_scalar('controller_repeat', 1)\n"
                                             '    return\n'
                                             "repeat = u16(state.scalar('controller_repeat') - 1)\n"
                                             "state.set_scalar('controller_repeat', repeat)\n"
                                             'if repeat:\n'
                                             '    return\n'
                                             "state.set_scalar('controller_repeat', 12)\n"
                                             'offset = u16(u16(2 - '
                                             "state.scalar('amount_digit_position')) << 2)\n"
                                             'increment = state.training_cost_steps.long(offset)\n'
                                             'points = state.training_point_steps.word(offset >> '
                                             '1)\n'
                                             "cost = state.scalar('training_cost')\n"
                                             'if horizontal & 2:\n'
                                             '    if cost < increment:\n'
                                             '        return\n'
                                             "    state.set_scalar('training_cost', u32(cost - "
                                             'increment))\n'
                                             "    state.set_scalar('training_points', "
                                             "u16(state.scalar('training_points') - points))\n"
                                             '    return\n'
                                             'new_cost = u32(cost + increment)\n'
                                             "if new_cost > state.scalar('training_cost_limit'):\n"
                                             '    return\n'
                                             "new_points = u16(state.scalar('training_points') + "
                                             'points)\n'
                                             'if new_points >= 1000:\n'
                                             '    return\n'
                                             "state.set_scalar('training_cost', new_cost)\n"
                                             "state.set_scalar('training_points', new_points)"},
 'append_training_cost_digits': {'signature': 'state: GameState',
                                 'returns': 'None',
                                 'flow': 'state = checked_state(state)\n'
                                         'destination = _queue_cursor(state)\n'
                                         'append_six_place_decimal_value(state, '
                                         "state.scalar('training_cost'), 50054, 49153, "
                                         'state.training_digit_scratch.cursor())\n'
                                         'destination.append_word(6)\n'
                                         'destination.append_word(50860)\n'
                                         'source = state.training_digit_scratch.cursor()\n'
                                         'for _ in range(6):\n'
                                         '    destination.append_word(source.next_word())\n'
                                         '_finish_queue(state, destination, 16)'},
 'append_training_amount_cursor': {'signature': 'state: GameState',
                                   'returns': 'None',
                                   'flow': 'state = checked_state(state)\n'
                                           "if state.scalar('controller_pair') & 48:\n"
                                           '    return\n'
                                           "if state.scalar('ui_gate_flags') & 8:\n"
                                           '    return\n'
                                           "y = u16(u16(state.scalar('amount_digit_position') << "
                                           '3) + 168)\n'
                                           'append_live_command_string_words(state, '
                                           'state.training_cursor_shape, 88, y)'},
 'prepare_selected_training_origin_and_speed': {'signature': 'state: GameState',
                                                'returns': 'Word',
                                                'flow': 'state = checked_state(state)\n'
                                                        'city_offset = '
                                                        "u16(state.scalar('command_city') << 2)\n"
                                                        'origin_y = '
                                                        'state.city_world_positions.word(city_offset, '
                                                        '2) & 65520\n'
                                                        "state.set_scalar('training_origin_y', "
                                                        'origin_y)\n'
                                                        'packed_y = u16(origin_y << 4) & 65280\n'
                                                        'origin_x = '
                                                        'state.city_world_positions.word(city_offset) '
                                                        '& 65520\n'
                                                        "state.set_scalar('training_origin_x', "
                                                        'origin_x)\n'
                                                        "state.set_scalar('training_origin_packed', "
                                                        'origin_x >> 4 | packed_y)\n'
                                                        'source = '
                                                        'state.command_candidates.cursor()\n'
                                                        'count, speed_sum = (0, 0)\n'
                                                        'while True:\n'
                                                        '    candidate = source.next_word()\n'
                                                        '    if negative_word(candidate):\n'
                                                        '        break\n'
                                                        '    if candidate < 16384:\n'
                                                        '        continue\n'
                                                        '    count = u16(count + 1)\n'
                                                        '    speed = '
                                                        'state.officer_march_speed.byte(candidate '
                                                        '& 255)\n'
                                                        '    speed_sum = u16(speed_sum + speed)\n'
                                                        "state.set_scalar('training_selected_count', "
                                                        'count)\n'
                                                        'mean_speed = '
                                                        'low16(divu_retained(speed_sum, count))\n'
                                                        "state.set_scalar('training_mean_speed', "
                                                        'mean_speed)\n'
                                                        'return mean_speed'}}

def _lower_update_recruitment_input_cursor(e, rules):
    e.label('player_pc_012f58')
    e.ins('cmpi.w', '#0x18,0xf39c:w', 6)
    e.label('player_pc_012f5e')
    e.ins('bcs.b', 'player_pc_012f66', 2)
    e.label('player_pc_012f60')
    e.ins('move.w', '#0x18,0xf39c:w', 6)
    e.label('player_pc_012f66')
    e.ins('subq.w', '#0x1,0xf39c:w', 4)
    e.label('player_pc_012f6a')
    e.ins('cmpi.w', '#0xc,0xf39c:w', 6)
    e.label('player_pc_012f70')
    e.ins('bcs.b', 'player_pc_012f8c', 2)
    e.label('player_pc_012f72')
    e.ins('lea.l', '-1252(%pc),%a0', 4)
    e.label('player_pc_012f76')
    e.ins('move.w', '#0x50,%d0', 4)
    e.label('player_pc_012f7a')
    e.ins('move.w', '0xf39a:w,%d1', 4)
    e.label('player_pc_012f7e')
    e.ins('lsl.w', '#0x3,%d1', 2)
    e.label('player_pc_012f80')
    e.ins('addi.w', '#0xf8,%d1', 4)
    e.label('player_pc_012f84')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_012f86')
    e.ins('jsr', 'player_pc_00ac08:l', 6)
    e.label('player_pc_012f8c')
    e.ins('rts', '', 2)

def _lower_update_recruitment_total_cursor(e, rules):
    e.label('player_pc_013034')
    e.ins('cmpi.w', '#0x18,0xf39c:w', 6)
    e.label('player_pc_01303a')
    e.ins('bcs.b', 'player_pc_013042', 2)
    e.label('player_pc_01303c')
    e.ins('move.w', '#0x18,0xf39c:w', 6)
    e.label('player_pc_013042')
    e.ins('subq.w', '#0x1,0xf39c:w', 4)
    e.label('player_pc_013046')
    e.ins('cmpi.w', '#0xc,0xf39c:w', 6)
    e.label('player_pc_01304c')
    e.ins('bcs.b', 'player_pc_013068', 2)
    e.label('player_pc_01304e')
    e.ins('lea.l', '-1472(%pc),%a0', 4)
    e.label('player_pc_013052')
    e.ins('move.w', '#0x68,%d0', 4)
    e.label('player_pc_013056')
    e.ins('move.w', '0xf39a:w,%d1', 4)
    e.label('player_pc_01305a')
    e.ins('lsl.w', '#0x3,%d1', 2)
    e.label('player_pc_01305c')
    e.ins('addi.w', '#0xf8,%d1', 4)
    e.label('player_pc_013060')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_013062')
    e.ins('jsr', 'player_pc_00ac08:l', 6)
    e.label('player_pc_013068')
    e.ins('rts', '', 2)

def _lower_append_recruitment_dialog_frame(e, rules):
    e.label('player_pc_01306a')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_01306e')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_013072')
    e.ins('move.w', '#0xf,(%a0)+', 4)
    e.label('player_pc_013076')
    e.ins('move.w', '#0xc494,(%a0)+', 4)
    e.label('player_pc_01307a')
    e.ins('move.w', '#0xc380,(%a0)+', 4)
    e.label('player_pc_01307e')
    e.ins('move.w', '#0xc,%d0', 4)
    e.label('player_pc_013082')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_013086')
    e.ins('dbra', '%d0,player_pc_013082', 4)
    e.label('player_pc_01308a')
    e.ins('move.w', '#0xcb80,(%a0)+', 4)
    e.label('player_pc_01308e')
    e.ins('move.w', '#0xf,0x22(%a0)', 6)
    e.label('player_pc_013094')
    e.ins('move.w', '#0xf,(%a0)+', 4)
    e.label('player_pc_013098')
    e.ins('move.w', '#0xc594,0x22(%a0)', 6)
    e.label('player_pc_01309e')
    e.ins('move.w', '#0xc514,(%a0)+', 4)
    e.label('player_pc_0130a2')
    e.ins('move.w', '#0xc382,0x22(%a0)', 6)
    e.label('player_pc_0130a8')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_0130ac')
    e.ins('move.w', '#0xc01d,%d0', 4)
    e.label('player_pc_0130b0')
    e.ins('move.w', '#0x3,%d1', 4)
    e.label('player_pc_0130b4')
    e.ins('bsr.w', 'player_pc_013176', 4)
    e.label('player_pc_0130b8')
    e.ins('move.w', '#0xc005,%d0', 4)
    e.label('player_pc_0130bc')
    e.ins('move.w', '#0x1,%d1', 4)
    e.label('player_pc_0130c0')
    e.ins('bsr.w', 'player_pc_013176', 4)
    e.label('player_pc_0130c4')
    e.ins('move.w', '#0x6,%d0', 4)
    e.label('player_pc_0130c8')
    e.ins('move.w', '#0xc001,0x22(%a0)', 6)
    e.label('player_pc_0130ce')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_0130d2')
    e.ins('dbra', '%d0,player_pc_0130c8', 4)
    e.label('player_pc_0130d6')
    e.ins('move.w', '#0xcb82,0x22(%a0)', 6)
    e.label('player_pc_0130dc')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_0130e0')
    e.ins('adda.w', '#0x22,%a0', 4)
    e.label('player_pc_0130e4')
    e.ins('move.w', '#0xf,(%a0)+', 4)
    e.label('player_pc_0130e8')
    e.ins('move.w', '#0xc614,(%a0)+', 4)
    e.label('player_pc_0130ec')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_0130f0')
    e.ins('move.w', '#0xc,%d0', 4)
    e.label('player_pc_0130f4')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_0130f8')
    e.ins('dbra', '%d0,player_pc_0130f4', 4)
    e.label('player_pc_0130fc')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_013100')
    e.ins('move.w', '#0xf,0x22(%a0)', 6)
    e.label('player_pc_013106')
    e.ins('move.w', '#0xf,(%a0)+', 4)
    e.label('player_pc_01310a')
    e.ins('move.w', '#0xc714,0x22(%a0)', 6)
    e.label('player_pc_013110')
    e.ins('move.w', '#0xc694,(%a0)+', 4)
    e.label('player_pc_013114')
    e.ins('move.w', '#0xc382,0x22(%a0)', 6)
    e.label('player_pc_01311a')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_01311e')
    e.ins('move.w', '#0xc009,%d0', 4)
    e.label('player_pc_013122')
    e.ins('move.w', '#0x3,%d1', 4)
    e.label('player_pc_013126')
    e.ins('bsr.w', 'player_pc_013176', 4)
    e.label('player_pc_01312a')
    e.ins('move.w', '#0x8,%d0', 4)
    e.label('player_pc_01312e')
    e.ins('move.w', '#0xc001,0x22(%a0)', 6)
    e.label('player_pc_013134')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_013138')
    e.ins('dbra', '%d0,player_pc_01312e', 4)
    e.label('player_pc_01313c')
    e.ins('move.w', '#0xcb82,0x22(%a0)', 6)
    e.label('player_pc_013142')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_013146')
    e.ins('adda.w', '#0x22,%a0', 4)
    e.label('player_pc_01314a')
    e.ins('move.w', '#0xf,(%a0)+', 4)
    e.label('player_pc_01314e')
    e.ins('move.w', '#0xc794,(%a0)+', 4)
    e.label('player_pc_013152')
    e.ins('move.w', '#0xd380,(%a0)+', 4)
    e.label('player_pc_013156')
    e.ins('move.w', '#0xc,%d0', 4)
    e.label('player_pc_01315a')
    e.ins('move.w', '#0xd381,(%a0)+', 4)
    e.label('player_pc_01315e')
    e.ins('dbra', '%d0,player_pc_01315a', 4)
    e.label('player_pc_013162')
    e.ins('move.w', '#0xdb80,(%a0)+', 4)
    e.label('player_pc_013166')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_013168')
    e.ins('addi.w', '#0xee,0xf31a:w', 6)
    e.label('player_pc_01316e')
    e.ins('bset.b', '#0x0,0xf3a4:w', 6)
    e.label('player_pc_013174')
    e.ins('rts', '', 2)

def _lower_append_recruitment_paired_tiles(e, rules):
    e.label('player_pc_013176')
    e.ins('move.w', '%d0,(%a0)', 2)
    e.label('player_pc_013178')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_01317a')
    e.ins('move.w', '%d0,0x22(%a0)', 4)
    e.label('player_pc_01317e')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_013180')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_013182')
    e.ins('dbra', '%d1,player_pc_013176', 4)
    e.label('player_pc_013186')
    e.ins('rts', '', 2)

def _lower_prepare_player_recruitment_capacity(e, rules):
    e.label('player_pc_013188')
    e.ins('clr.l', '0xf3e4:w', 4)
    e.label('player_pc_01318c')
    e.ins('clr.l', '0xf39e:w', 4)
    e.label('player_pc_013190')
    e.ins('move.w', '#0x3,0xf39a:w', 6)
    e.label('player_pc_013196')
    e.ins('move.w', '0xf364:w,%d0', 4)
    e.label('player_pc_01319a')
    e.ins('lsl.w', '#0x2,%d0', 2)
    e.label('player_pc_01319c')
    e.ins('lea.l', '0xdffc:w,%a0', 4)
    e.label('player_pc_0131a0')
    e.ins('move.l', '(%a0, %d0.w),0xf3e8:w', 6)
    e.label('player_pc_0131a6')
    e.ins('move.l', '0xf3e8:w,%d2', 4)
    e.label('player_pc_0131aa')
    e.ins('divu.w', '#0x64,%d2', 4)
    e.label('player_pc_0131ae')
    e.ins('lea.l', '0xe13c:w,%a1', 4)
    e.label('player_pc_0131b2')
    e.ins('move.l', '(%a1, %d0.w),%d3', 4)
    e.label('player_pc_0131b6')
    e.ins('move.l', '%d3,%d4', 2)
    e.label('player_pc_0131b8')
    e.ins('mulu.w', '#0xa,%d3', 4)
    e.label('player_pc_0131bc')
    e.ins('swap', '%d4', 2)
    e.label('player_pc_0131be')
    e.ins('mulu.w', '#0xa,%d4', 4)
    e.label('player_pc_0131c2')
    e.ins('swap', '%d4', 2)
    e.label('player_pc_0131c4')
    e.ins('add.l', '%d4,%d3', 2)
    e.label('player_pc_0131c6')
    e.ins('lea.l', '0xe774:w,%a1', 4)
    e.label('player_pc_0131ca')
    e.ins('move.l', '#0x186a0,%d4', 6)
    e.label('player_pc_0131d0')
    e.ins('sub.l', '(%a1, %d0.w),%d4', 4)
    e.label('player_pc_0131d4')
    e.ins('divu.w', '#0x64,%d4', 4)
    e.label('player_pc_0131d8')
    e.ins('andi.l', '#0xffff,%d4', 6)
    e.label('player_pc_0131de')
    e.ins('cmp.l', '%d3,%d4', 2)
    e.label('player_pc_0131e0')
    e.ins('bcc.w', 'player_pc_0131e6', 4)
    e.label('player_pc_0131e4')
    e.ins('move.l', '%d4,%d3', 2)
    e.label('player_pc_0131e6')
    e.ins('andi.l', '#0xffff,%d2', 6)
    e.label('player_pc_0131ec')
    e.ins('cmp.l', '%d3,%d2', 2)
    e.label('player_pc_0131ee')
    e.ins('bls.b', 'player_pc_0131fa', 2)
    e.label('player_pc_0131f0')
    e.ins('move.w', '%d3,%d2', 2)
    e.label('player_pc_0131f2')
    e.ins('mulu.w', '#0x64,%d3', 4)
    e.label('player_pc_0131f6')
    e.ins('move.l', '%d3,0xf3e8:w', 4)
    e.label('player_pc_0131fa')
    e.ins('move.w', '#0x3,%d1', 4)
    e.label('player_pc_0131fe')
    e.ins('cmpi.w', '#0xa,%d2', 4)
    e.label('player_pc_013202')
    e.ins('bcs.b', 'player_pc_013216', 2)
    e.label('player_pc_013204')
    e.ins('subq.w', '#0x1,%d1', 2)
    e.label('player_pc_013206')
    e.ins('cmpi.w', '#0x64,%d2', 4)
    e.label('player_pc_01320a')
    e.ins('bcs.b', 'player_pc_013216', 2)
    e.label('player_pc_01320c')
    e.ins('subq.w', '#0x1,%d1', 2)
    e.label('player_pc_01320e')
    e.ins('cmpi.w', '#0x3e8,%d2', 4)
    e.label('player_pc_013212')
    e.ins('bcs.b', 'player_pc_013216', 2)
    e.label('player_pc_013214')
    e.ins('subq.w', '#0x1,%d1', 2)
    e.label('player_pc_013216')
    e.ins('move.w', '%d1,0xf3ec:w', 4)
    e.label('player_pc_01321a')
    e.ins('rts', '', 2)

def _lower_append_recruitment_input_digits(e, rules):
    e.label('player_pc_01321c')
    e.ins('move.l', '0xf3e4:w,%d0', 4)
    e.label('player_pc_013220')
    e.ins('move.w', '#0xc386,%d1', 4)
    e.label('player_pc_013224')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_013226')
    e.ins('lea.l', '0xef00:w,%a6', 4)
    e.label('player_pc_01322a')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_013230')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_013234')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_013238')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_01323c')
    e.ins('move.w', '#0xc5a4,(%a0)+', 4)
    e.label('player_pc_013240')
    e.ins('lea.l', '0xef00:w,%a1', 4)
    e.label('player_pc_013244')
    e.ins('clr.w', '%d0', 2)
    e.label('player_pc_013246')
    e.ins('move.w', '#0x5,%d1', 4)
    e.label('player_pc_01324a')
    e.ins('move.w', '(%a1)+,%d2', 2)
    e.label('player_pc_01324c')
    e.ins('bne.b', 'player_pc_01325e', 2)
    e.label('player_pc_01324e')
    e.ins('cmp.w', '0xf39a:w,%d0', 4)
    e.label('player_pc_013252')
    e.ins('bcc.b', 'player_pc_01325a', 2)
    e.label('player_pc_013254')
    e.ins('move.w', '#0xc001,%d2', 4)
    e.label('player_pc_013258')
    e.ins('bra.b', 'player_pc_01325e', 2)
    e.label('player_pc_01325a')
    e.ins('move.w', '#0xc386,%d2', 4)
    e.label('player_pc_01325e')
    e.ins('move.w', '%d2,(%a0)+', 2)
    e.label('player_pc_013260')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_013262')
    e.ins('dbra', '%d1,player_pc_01324a', 4)
    e.label('player_pc_013266')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_013268')
    e.ins('addi.w', '#0x10,0xf31a:w', 6)
    e.label('player_pc_01326e')
    e.ins('rts', '', 2)

def _lower_append_recruitment_total_digits(e, rules):
    e.label('player_pc_013270')
    e.ins('move.l', '0xf39e:w,%d0', 4)
    e.label('player_pc_013274')
    e.ins('move.w', '#0xc386,%d1', 4)
    e.label('player_pc_013278')
    e.ins('move.w', '#0xc001,%d2', 4)
    e.label('player_pc_01327c')
    e.ins('lea.l', '0xef0c:w,%a6', 4)
    e.label('player_pc_013280')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_013286')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_01328a')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_01328e')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_013292')
    e.ins('move.w', '#0xc724,(%a0)+', 4)
    e.label('player_pc_013296')
    e.ins('lea.l', '0xef0c:w,%a1', 4)
    e.label('player_pc_01329a')
    e.ins('move.w', '#0x2,%d0', 4)
    e.label('player_pc_01329e')
    e.ins('move.l', '(%a1)+,(%a0)+', 2)
    e.label('player_pc_0132a0')
    e.ins('dbra', '%d0,player_pc_01329e', 4)
    e.label('player_pc_0132a4')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_0132a6')
    e.ins('addi.w', '#0x10,0xf31a:w', 6)
    e.label('player_pc_0132ac')
    e.ins('rts', '', 2)

def _lower_append_equipment_amount_cursor(e, rules):
    e.label('player_pc_013510')
    e.ins('btst.b', '#0x5,0xf603:w', 6)
    e.label('player_pc_013516')
    e.ins('bne.w', 'player_pc_01353c', 4)
    e.label('player_pc_01351a')
    e.ins('btst.b', '#0x3,0xf321:w', 6)
    e.label('player_pc_013520')
    e.ins('bne.b', 'player_pc_01353c', 2)
    e.label('player_pc_013522')
    e.ins('lea.l', '-2708(%pc),%a0', 4)
    e.label('player_pc_013526')
    e.ins('move.w', '#0x58,%d0', 4)
    e.label('player_pc_01352a')
    e.ins('move.w', '0xf39a:w,%d1', 4)
    e.label('player_pc_01352e')
    e.ins('lsl.w', '#0x3,%d1', 2)
    e.label('player_pc_013530')
    e.ins('addi.w', '#0x90,%d1', 4)
    e.label('player_pc_013534')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_013536')
    e.ins('jsr', 'player_pc_00ac08:l', 6)
    e.label('player_pc_01353c')
    e.ins('rts', '', 2)

def _lower_clear_equipment_dialog_rows(e, rules):
    e.label('player_pc_01353e')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_013542')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_013546')
    e.ins('move.w', '#0xf,0xcc(%a0)', 6)
    e.label('player_pc_01354c')
    e.ins('move.w', '#0xf,0xaa(%a0)', 6)
    e.label('player_pc_013552')
    e.ins('move.w', '#0xf,0x88(%a0)', 6)
    e.label('player_pc_013558')
    e.ins('move.w', '#0xf,0x66(%a0)', 6)
    e.label('player_pc_01355e')
    e.ins('move.w', '#0xf,0x44(%a0)', 6)
    e.label('player_pc_013564')
    e.ins('move.w', '#0xf,0x22(%a0)', 6)
    e.label('player_pc_01356a')
    e.ins('move.w', '#0xf,(%a0)+', 4)
    e.label('player_pc_01356e')
    e.ins('move.w', '#0xc794,0xcc(%a0)', 6)
    e.label('player_pc_013574')
    e.ins('move.w', '#0xc714,0xaa(%a0)', 6)
    e.label('player_pc_01357a')
    e.ins('move.w', '#0xc694,0x88(%a0)', 6)
    e.label('player_pc_013580')
    e.ins('move.w', '#0xc614,0x66(%a0)', 6)
    e.label('player_pc_013586')
    e.ins('move.w', '#0xc594,0x44(%a0)', 6)
    e.label('player_pc_01358c')
    e.ins('move.w', '#0xc514,0x22(%a0)', 6)
    e.label('player_pc_013592')
    e.ins('move.w', '#0xc494,(%a0)+', 4)
    e.label('player_pc_013596')
    e.ins('move.w', '#0xe,%d0', 4)
    e.label('player_pc_01359a')
    e.ins('clr.w', '0xcc(%a0)', 4)
    e.label('player_pc_01359e')
    e.ins('clr.w', '0xaa(%a0)', 4)
    e.label('player_pc_0135a2')
    e.ins('clr.w', '0x88(%a0)', 4)
    e.label('player_pc_0135a6')
    e.ins('clr.w', '0x66(%a0)', 4)
    e.label('player_pc_0135aa')
    e.ins('clr.w', '0x44(%a0)', 4)
    e.label('player_pc_0135ae')
    e.ins('clr.w', '0x22(%a0)', 4)
    e.label('player_pc_0135b2')
    e.ins('clr.w', '(%a0)+', 2)
    e.label('player_pc_0135b4')
    e.ins('dbra', '%d0,player_pc_01359a', 4)
    e.label('player_pc_0135b8')
    e.ins('clr.w', '0xcc(%a0)', 4)
    e.label('player_pc_0135bc')
    e.ins('addi.w', '#0xee,0xf31a:w', 6)
    e.label('player_pc_0135c2')
    e.ins('rts', '', 2)

def _lower_append_equipment_dialog_frame(e, rules):
    e.label('player_pc_0135c4')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_0135c8')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_0135cc')
    e.ins('move.w', '#0xf,(%a0)+', 4)
    e.label('player_pc_0135d0')
    e.ins('move.w', '#0xc494,(%a0)+', 4)
    e.label('player_pc_0135d4')
    e.ins('move.w', '#0xc380,(%a0)+', 4)
    e.label('player_pc_0135d8')
    e.ins('move.w', '#0xc,%d0', 4)
    e.label('player_pc_0135dc')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_0135e0')
    e.ins('dbra', '%d0,player_pc_0135dc', 4)
    e.label('player_pc_0135e4')
    e.ins('move.w', '#0xcb80,(%a0)+', 4)
    e.label('player_pc_0135e8')
    e.ins('move.w', '#0xf,0x22(%a0)', 6)
    e.label('player_pc_0135ee')
    e.ins('move.w', '#0xf,(%a0)+', 4)
    e.label('player_pc_0135f2')
    e.ins('move.w', '#0xc594,0x22(%a0)', 6)
    e.label('player_pc_0135f8')
    e.ins('move.w', '#0xc514,(%a0)+', 4)
    e.label('player_pc_0135fc')
    e.ins('move.w', '#0xc382,0x22(%a0)', 6)
    e.label('player_pc_013602')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_013606')
    e.ins('move.w', '#0xc011,%d0', 4)
    e.label('player_pc_01360a')
    e.ins('move.w', '#0x3,%d1', 4)
    e.label('player_pc_01360e')
    e.ins('bsr.w', 'player_pc_0136e2', 4)
    e.label('player_pc_013612')
    e.ins('move.w', '#0xc021,%d0', 4)
    e.label('player_pc_013616')
    e.ins('move.w', '#0x1,%d1', 4)
    e.label('player_pc_01361a')
    e.ins('bsr.w', 'player_pc_0136e2', 4)
    e.label('player_pc_01361e')
    e.ins('move.w', '#0x6,%d0', 4)
    e.label('player_pc_013622')
    e.ins('move.w', '#0xc001,0x22(%a0)', 6)
    e.label('player_pc_013628')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_01362c')
    e.ins('dbra', '%d0,player_pc_013622', 4)
    e.label('player_pc_013630')
    e.ins('move.w', '#0xcb82,0x22(%a0)', 6)
    e.label('player_pc_013636')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_01363a')
    e.ins('adda.w', '#0x22,%a0', 4)
    e.label('player_pc_01363e')
    e.ins('move.w', '#0xf,(%a0)+', 4)
    e.label('player_pc_013642')
    e.ins('move.w', '#0xc614,(%a0)+', 4)
    e.label('player_pc_013646')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_01364a')
    e.ins('move.w', '#0xc,%d0', 4)
    e.label('player_pc_01364e')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_013652')
    e.ins('dbra', '%d0,player_pc_01364e', 4)
    e.label('player_pc_013656')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_01365a')
    e.ins('move.w', '#0xf,0x22(%a0)', 6)
    e.label('player_pc_013660')
    e.ins('move.w', '#0xf,(%a0)+', 4)
    e.label('player_pc_013664')
    e.ins('move.w', '#0xc714,0x22(%a0)', 6)
    e.label('player_pc_01366a')
    e.ins('move.w', '#0xc694,(%a0)+', 4)
    e.label('player_pc_01366e')
    e.ins('move.w', '#0xc382,0x22(%a0)', 6)
    e.label('player_pc_013674')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_013678')
    e.ins('move.w', '#0xc019,%d0', 4)
    e.label('player_pc_01367c')
    e.ins('move.w', '#0x1,%d1', 4)
    e.label('player_pc_013680')
    e.ins('bsr.w', 'player_pc_0136e2', 4)
    e.label('player_pc_013684')
    e.ins('move.w', '#0xc025,%d0', 4)
    e.label('player_pc_013688')
    e.ins('move.w', '#0x1,%d1', 4)
    e.label('player_pc_01368c')
    e.ins('bsr.w', 'player_pc_0136e2', 4)
    e.label('player_pc_013690')
    e.ins('move.w', '#0xc021,%d0', 4)
    e.label('player_pc_013694')
    e.ins('move.w', '#0x1,%d1', 4)
    e.label('player_pc_013698')
    e.ins('bsr.w', 'player_pc_0136e2', 4)
    e.label('player_pc_01369c')
    e.ins('move.w', '#0x6,%d0', 4)
    e.label('player_pc_0136a0')
    e.ins('move.w', '#0xc001,0x22(%a0)', 6)
    e.label('player_pc_0136a6')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_0136aa')
    e.ins('dbra', '%d0,player_pc_0136a0', 4)
    e.label('player_pc_0136ae')
    e.ins('move.w', '#0xcb82,0x22(%a0)', 6)
    e.label('player_pc_0136b4')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_0136b8')
    e.ins('adda.w', '#0x22,%a0', 4)
    e.label('player_pc_0136bc')
    e.ins('move.w', '#0xf,(%a0)+', 4)
    e.label('player_pc_0136c0')
    e.ins('move.w', '#0xc794,(%a0)+', 4)
    e.label('player_pc_0136c4')
    e.ins('move.w', '#0xd380,(%a0)+', 4)
    e.label('player_pc_0136c8')
    e.ins('move.w', '#0xc,%d0', 4)
    e.label('player_pc_0136cc')
    e.ins('move.w', '#0xd381,(%a0)+', 4)
    e.label('player_pc_0136d0')
    e.ins('dbra', '%d0,player_pc_0136cc', 4)
    e.label('player_pc_0136d4')
    e.ins('move.w', '#0xdb80,(%a0)+', 4)
    e.label('player_pc_0136d8')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_0136da')
    e.ins('addi.w', '#0xee,0xf31a:w', 6)
    e.label('player_pc_0136e0')
    e.ins('rts', '', 2)

def _lower_append_equipment_paired_tiles(e, rules):
    e.label('player_pc_0136e2')
    e.ins('move.w', '%d0,(%a0)', 2)
    e.label('player_pc_0136e4')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_0136e6')
    e.ins('move.w', '%d0,0x22(%a0)', 4)
    e.label('player_pc_0136ea')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_0136ec')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_0136ee')
    e.ins('dbra', '%d1,player_pc_0136e2', 4)
    e.label('player_pc_0136f2')
    e.ins('rts', '', 2)

def _lower_append_equipment_input_digits(e, rules):
    e.label('player_pc_0136f4')
    e.ins('move.l', '0xf3ee:w,%d0', 4)
    e.label('player_pc_0136f8')
    e.ins('move.w', '#0xc386,%d1', 4)
    e.label('player_pc_0136fc')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_0136fe')
    e.ins('lea.l', '0xef00:w,%a6', 4)
    e.label('player_pc_013702')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_013708')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_01370c')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_013710')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_013714')
    e.ins('move.w', '#0xc5a4,(%a0)+', 4)
    e.label('player_pc_013718')
    e.ins('clr.w', '%d1', 2)
    e.label('player_pc_01371a')
    e.ins('lea.l', '0xef00:w,%a1', 4)
    e.label('player_pc_01371e')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_013722')
    e.ins('move.w', '(%a1)+,%d2', 2)
    e.label('player_pc_013724')
    e.ins('bne.b', 'player_pc_013738', 2)
    e.label('player_pc_013726')
    e.ins('cmp.w', '0xf39a:w,%d1', 4)
    e.label('player_pc_01372a')
    e.ins('bcs.w', 'player_pc_013734', 4)
    e.label('player_pc_01372e')
    e.ins('move.w', '#0xc386,%d2', 4)
    e.label('player_pc_013732')
    e.ins('bra.b', 'player_pc_013738', 2)
    e.label('player_pc_013734')
    e.ins('move.w', '#0xc001,%d2', 4)
    e.label('player_pc_013738')
    e.ins('move.w', '%d2,(%a0)+', 2)
    e.label('player_pc_01373a')
    e.ins('addq.w', '#0x1,%d1', 2)
    e.label('player_pc_01373c')
    e.ins('dbra', '%d0,player_pc_013722', 4)
    e.label('player_pc_013740')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_013742')
    e.ins('addi.w', '#0x10,0xf31a:w', 6)
    e.label('player_pc_013748')
    e.ins('rts', '', 2)

def _lower_append_equipment_total_digits(e, rules):
    e.label('player_pc_01374a')
    e.ins('cmpi.w', '#0x1b,0xf362:w', 6)
    e.label('player_pc_013750')
    e.ins('beq.w', 'player_pc_01375c', 4)
    e.label('player_pc_013754')
    e.ins('move.l', '0xf3e4:w,%d0', 4)
    e.label('player_pc_013758')
    e.ins('bra.w', 'player_pc_013760', 4)
    e.label('player_pc_01375c')
    e.ins('move.l', '0xcfae:w,%d0', 4)
    e.label('player_pc_013760')
    e.ins('move.w', '#0xc386,%d1', 4)
    e.label('player_pc_013764')
    e.ins('move.w', '#0xc001,%d2', 4)
    e.label('player_pc_013768')
    e.ins('lea.l', '0xef0c:w,%a6', 4)
    e.label('player_pc_01376c')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_013772')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_013776')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_01377a')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_01377e')
    e.ins('move.w', '#0xc724,(%a0)+', 4)
    e.label('player_pc_013782')
    e.ins('lea.l', '0xef0c:w,%a1', 4)
    e.label('player_pc_013786')
    e.ins('move.w', '#0x2,%d0', 4)
    e.label('player_pc_01378a')
    e.ins('move.l', '(%a1)+,(%a0)+', 2)
    e.label('player_pc_01378c')
    e.ins('dbra', '%d0,player_pc_01378a', 4)
    e.label('player_pc_013790')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_013792')
    e.ins('addi.w', '#0x10,0xf31a:w', 6)
    e.label('player_pc_013798')
    e.ins('rts', '', 2)

def _lower_append_candidate_amount_cursor(e, rules):
    e.label('player_pc_013934')
    e.ins('btst.b', '#0x3,0xf321:w', 6)
    e.label('player_pc_01393a')
    e.ins('bne.b', 'player_pc_013956', 2)
    e.label('player_pc_01393c')
    e.ins('lea.l', '-3758(%pc),%a0', 4)
    e.label('player_pc_013940')
    e.ins('move.w', '#0x58,%d0', 4)
    e.label('player_pc_013944')
    e.ins('move.w', '0xf39a:w,%d1', 4)
    e.label('player_pc_013948')
    e.ins('lsl.w', '#0x3,%d1', 2)
    e.label('player_pc_01394a')
    e.ins('addi.w', '#0x90,%d1', 4)
    e.label('player_pc_01394e')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_013950')
    e.ins('jsr', 'player_pc_00ac08:l', 6)
    e.label('player_pc_013956')
    e.ins('rts', '', 2)

def _lower_append_candidate_dialog_frame(e, rules):
    e.label('player_pc_013958')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_01395c')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_013960')
    e.ins('move.w', '#0x8,(%a0)+', 4)
    e.label('player_pc_013964')
    e.ins('move.w', '#0xc420,(%a0)+', 4)
    e.label('player_pc_013968')
    e.ins('move.w', '#0xc380,(%a0)+', 4)
    e.label('player_pc_01396c')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_013970')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_013974')
    e.ins('dbra', '%d0,player_pc_013970', 4)
    e.label('player_pc_013978')
    e.ins('move.w', '#0xcb80,(%a0)+', 4)
    e.label('player_pc_01397c')
    e.ins('move.w', '#0xc520,%d2', 4)
    e.label('player_pc_013980')
    e.ins('move.w', '#0x8,0x14(%a0)', 6)
    e.label('player_pc_013986')
    e.ins('move.w', '#0x8,(%a0)+', 4)
    e.label('player_pc_01398a')
    e.ins('move.w', '%d2,0x14(%a0)', 4)
    e.label('player_pc_01398e')
    e.ins('subi.w', '#0x80,%d2', 4)
    e.label('player_pc_013992')
    e.ins('move.w', '%d2,(%a0)+', 2)
    e.label('player_pc_013994')
    e.ins('addi.w', '#0x100,%d2', 4)
    e.label('player_pc_013998')
    e.ins('move.w', '#0xc382,0x14(%a0)', 6)
    e.label('player_pc_01399e')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_0139a2')
    e.ins('move.w', '#0xc005,%d0', 4)
    e.label('player_pc_0139a6')
    e.ins('move.w', '#0x5,%d1', 4)
    e.label('player_pc_0139aa')
    e.ins('bsr.w', 'player_pc_013a84', 4)
    e.label('player_pc_0139ae')
    e.ins('move.w', '#0xcb82,0x14(%a0)', 6)
    e.label('player_pc_0139b4')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_0139b8')
    e.ins('adda.w', '#0x14,%a0', 4)
    e.label('player_pc_0139bc')
    e.ins('bsr.w', 'player_pc_013a96', 4)
    e.label('player_pc_0139c0')
    e.ins('move.w', '#0x8,0x14(%a0)', 6)
    e.label('player_pc_0139c6')
    e.ins('move.w', '#0x8,(%a0)+', 4)
    e.label('player_pc_0139ca')
    e.ins('move.w', '%d2,0x14(%a0)', 4)
    e.label('player_pc_0139ce')
    e.ins('subi.w', '#0x80,%d2', 4)
    e.label('player_pc_0139d2')
    e.ins('move.w', '%d2,(%a0)+', 2)
    e.label('player_pc_0139d4')
    e.ins('addi.w', '#0x100,%d2', 4)
    e.label('player_pc_0139d8')
    e.ins('move.w', '#0xc382,0x14(%a0)', 6)
    e.label('player_pc_0139de')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_0139e2')
    e.ins('move.w', '#0xc011,%d0', 4)
    e.label('player_pc_0139e6')
    e.ins('move.w', '#0x1,%d1', 4)
    e.label('player_pc_0139ea')
    e.ins('bsr.w', 'player_pc_013a84', 4)
    e.label('player_pc_0139ee')
    e.ins('move.w', '#0xc009,%d0', 4)
    e.label('player_pc_0139f2')
    e.ins('move.w', '#0x3,%d1', 4)
    e.label('player_pc_0139f6')
    e.ins('bsr.w', 'player_pc_013a84', 4)
    e.label('player_pc_0139fa')
    e.ins('move.w', '#0xcb82,0x14(%a0)', 6)
    e.label('player_pc_013a00')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_013a04')
    e.ins('adda.w', '#0x14,%a0', 4)
    e.label('player_pc_013a08')
    e.ins('bsr.w', 'player_pc_013a96', 4)
    e.label('player_pc_013a0c')
    e.ins('move.w', '#0x8,0x14(%a0)', 6)
    e.label('player_pc_013a12')
    e.ins('move.w', '#0x8,(%a0)+', 4)
    e.label('player_pc_013a16')
    e.ins('move.w', '%d2,0x14(%a0)', 4)
    e.label('player_pc_013a1a')
    e.ins('subi.w', '#0x80,%d2', 4)
    e.label('player_pc_013a1e')
    e.ins('move.w', '%d2,(%a0)+', 2)
    e.label('player_pc_013a20')
    e.ins('addi.w', '#0x100,%d2', 4)
    e.label('player_pc_013a24')
    e.ins('move.w', '#0xc382,0x14(%a0)', 6)
    e.label('player_pc_013a2a')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_013a2e')
    e.ins('move.w', '#0xc005,%d0', 4)
    e.label('player_pc_013a32')
    e.ins('move.w', '#0x1,%d1', 4)
    e.label('player_pc_013a36')
    e.ins('bsr.w', 'player_pc_013a84', 4)
    e.label('player_pc_013a3a')
    e.ins('move.w', '#0xc015,%d0', 4)
    e.label('player_pc_013a3e')
    e.ins('move.w', '#0x1,%d1', 4)
    e.label('player_pc_013a42')
    e.ins('bsr.w', 'player_pc_013a84', 4)
    e.label('player_pc_013a46')
    e.ins('move.w', '#0xc011,%d0', 4)
    e.label('player_pc_013a4a')
    e.ins('move.w', '#0x1,%d1', 4)
    e.label('player_pc_013a4e')
    e.ins('bsr.w', 'player_pc_013a84', 4)
    e.label('player_pc_013a52')
    e.ins('move.w', '#0xcb82,0x14(%a0)', 6)
    e.label('player_pc_013a58')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_013a5c')
    e.ins('adda.w', '#0x14,%a0', 4)
    e.label('player_pc_013a60')
    e.ins('move.w', '#0x8,(%a0)+', 4)
    e.label('player_pc_013a64')
    e.ins('move.w', '%d2,(%a0)+', 2)
    e.label('player_pc_013a66')
    e.ins('move.w', '#0xd380,(%a0)+', 4)
    e.label('player_pc_013a6a')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_013a6e')
    e.ins('move.w', '#0xd381,(%a0)+', 4)
    e.label('player_pc_013a72')
    e.ins('dbra', '%d0,player_pc_013a6e', 4)
    e.label('player_pc_013a76')
    e.ins('move.w', '#0xdb80,(%a0)+', 4)
    e.label('player_pc_013a7a')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_013a7c')
    e.ins('addi.w', '#0xc8,0xf31a:w', 6)
    e.label('player_pc_013a82')
    e.ins('rts', '', 2)

def _lower_append_candidate_paired_tiles(e, rules):
    e.label('player_pc_013a84')
    e.ins('move.w', '%d0,(%a0)', 2)
    e.label('player_pc_013a86')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_013a88')
    e.ins('move.w', '%d0,0x14(%a0)', 4)
    e.label('player_pc_013a8c')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_013a8e')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_013a90')
    e.ins('dbra', '%d1,player_pc_013a84', 4)
    e.label('player_pc_013a94')
    e.ins('rts', '', 2)

def _lower_append_candidate_separator_row(e, rules):
    e.label('player_pc_013a96')
    e.ins('move.w', '#0x8,(%a0)+', 4)
    e.label('player_pc_013a9a')
    e.ins('move.w', '%d2,(%a0)+', 2)
    e.label('player_pc_013a9c')
    e.ins('addi.w', '#0x100,%d2', 4)
    e.label('player_pc_013aa0')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_013aa4')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_013aa8')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_013aac')
    e.ins('dbra', '%d0,player_pc_013aa8', 4)
    e.label('player_pc_013ab0')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_013ab4')
    e.ins('rts', '', 2)

def _lower_update_equipment_category(e, rules):
    e.label('player_pc_013b86')
    e.ins('move.b', '0xf602:w,%d0', 4)
    e.label('player_pc_013b8a')
    e.ins('andi.w', '#0x3,%d0', 4)
    e.label('player_pc_013b8e')
    e.ins('beq.b', 'player_pc_013bd2', 2)
    e.label('player_pc_013b90')
    e.ins('subq.w', '#0x1,0xf608:w', 4)
    e.label('player_pc_013b94')
    e.ins('bne.b', 'player_pc_013bd8', 2)
    e.label('player_pc_013b96')
    e.ins('move.w', '#0xc,0xf608:w', 6)
    e.label('player_pc_013b9c')
    e.ins('btst.l', '#0x1,%d0', 4)
    e.label('player_pc_013ba0')
    e.ins('bne.b', 'player_pc_013bb8', 2)
    e.label('player_pc_013ba2')
    e.ins('tst.w', '0xf688:w', 4)
    e.label('player_pc_013ba6')
    e.ins('bne.b', 'player_pc_013bb2', 2)
    e.label('player_pc_013ba8')
    e.ins('move.w', '#0x2,0xf688:w', 6)
    e.label('player_pc_013bae')
    e.ins('bra.w', 'player_pc_013bd8', 4)
    e.label('player_pc_013bb2')
    e.ins('subq.w', '#0x1,0xf688:w', 4)
    e.label('player_pc_013bb6')
    e.ins('bra.b', 'player_pc_013bd8', 2)
    e.label('player_pc_013bb8')
    e.ins('cmpi.w', '#0x2,0xf688:w', 6)
    e.label('player_pc_013bbe')
    e.ins('bcs.b', 'player_pc_013bc8', 2)
    e.label('player_pc_013bc0')
    e.ins('clr.w', '0xf688:w', 4)
    e.label('player_pc_013bc4')
    e.ins('bra.w', 'player_pc_013bd8', 4)
    e.label('player_pc_013bc8')
    e.ins('addi.w', '#0x1,0xf688:w', 6)
    e.label('player_pc_013bce')
    e.ins('bra.w', 'player_pc_013bd8', 4)
    e.label('player_pc_013bd2')
    e.ins('move.w', '#0x1,0xf608:w', 6)
    e.label('player_pc_013bd8')
    e.ins('rts', '', 2)

def _lower_append_equipment_category_cursor(e, rules):
    e.label('player_pc_013bda')
    e.ins('btst.b', '#0x5,0xf603:w', 6)
    e.label('player_pc_013be0')
    e.ins('bne.w', 'player_pc_013c1a', 4)
    e.label('player_pc_013be4')
    e.ins('move.b', '0xf602:w,%d0', 4)
    e.label('player_pc_013be8')
    e.ins('andi.w', '#0x3,%d0', 4)
    e.label('player_pc_013bec')
    e.ins('bne.w', 'player_pc_013bf8', 4)
    e.label('player_pc_013bf0')
    e.ins('btst.b', '#0x4,0xf321:w', 6)
    e.label('player_pc_013bf6')
    e.ins('bne.b', 'player_pc_013c1a', 2)
    e.label('player_pc_013bf8')
    e.ins('lea.l', '34(%pc),%a0', 4)
    e.label('player_pc_013bfc')
    e.ins('nop', '', 2)
    e.label('player_pc_013bfe')
    e.ins('move.w', '0xf688:w,%d0', 4)
    e.label('player_pc_013c02')
    e.ins('lsl.w', '#0x1,%d0', 2)
    e.label('player_pc_013c04')
    e.ins('add.w', '0xf688:w,%d0', 4)
    e.label('player_pc_013c08')
    e.ins('lsl.w', '#0x3,%d0', 2)
    e.label('player_pc_013c0a')
    e.ins('addi.w', '#0x40,%d0', 4)
    e.label('player_pc_013c0e')
    e.ins('move.w', '#0x80,%d1', 4)
    e.label('player_pc_013c12')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_013c14')
    e.ins('jsr', 'player_pc_00ac08:l', 6)
    e.label('player_pc_013c1a')
    e.ins('rts', '', 2)

def _lower_clear_candidate_dialog_rows(e, rules):
    e.label('player_pc_013c7e')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_013c82')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_013c86')
    e.ins('move.w', '#0x8,0xb4(%a0)', 6)
    e.label('player_pc_013c8c')
    e.ins('move.w', '#0x8,0xa0(%a0)', 6)
    e.label('player_pc_013c92')
    e.ins('move.w', '#0x8,0x8c(%a0)', 6)
    e.label('player_pc_013c98')
    e.ins('move.w', '#0x8,0x78(%a0)', 6)
    e.label('player_pc_013c9e')
    e.ins('move.w', '#0x8,0x64(%a0)', 6)
    e.label('player_pc_013ca4')
    e.ins('move.w', '#0x8,0x50(%a0)', 6)
    e.label('player_pc_013caa')
    e.ins('move.w', '#0x8,0x3c(%a0)', 6)
    e.label('player_pc_013cb0')
    e.ins('move.w', '#0x8,0x28(%a0)', 6)
    e.label('player_pc_013cb6')
    e.ins('move.w', '#0x8,0x14(%a0)', 6)
    e.label('player_pc_013cbc')
    e.ins('move.w', '#0x8,(%a0)+', 4)
    e.label('player_pc_013cc0')
    e.ins('move.w', '#0xc8a0,0xb4(%a0)', 6)
    e.label('player_pc_013cc6')
    e.ins('move.w', '#0xc820,0xa0(%a0)', 6)
    e.label('player_pc_013ccc')
    e.ins('move.w', '#0xc7a0,0x8c(%a0)', 6)
    e.label('player_pc_013cd2')
    e.ins('move.w', '#0xc720,0x78(%a0)', 6)
    e.label('player_pc_013cd8')
    e.ins('move.w', '#0xc6a0,0x64(%a0)', 6)
    e.label('player_pc_013cde')
    e.ins('move.w', '#0xc620,0x50(%a0)', 6)
    e.label('player_pc_013ce4')
    e.ins('move.w', '#0xc5a0,0x3c(%a0)', 6)
    e.label('player_pc_013cea')
    e.ins('move.w', '#0xc520,0x28(%a0)', 6)
    e.label('player_pc_013cf0')
    e.ins('move.w', '#0xc4a0,0x14(%a0)', 6)
    e.label('player_pc_013cf6')
    e.ins('move.w', '#0xc420,(%a0)+', 4)
    e.label('player_pc_013cfa')
    e.ins('move.w', '#0x7,%d0', 4)
    e.label('player_pc_013cfe')
    e.ins('move.w', '#0x8000,0xb4(%a0)', 6)
    e.label('player_pc_013d04')
    e.ins('move.w', '#0x8000,0xa0(%a0)', 6)
    e.label('player_pc_013d0a')
    e.ins('move.w', '#0x8000,0x8c(%a0)', 6)
    e.label('player_pc_013d10')
    e.ins('move.w', '#0x8000,0x78(%a0)', 6)
    e.label('player_pc_013d16')
    e.ins('move.w', '#0x8000,0x64(%a0)', 6)
    e.label('player_pc_013d1c')
    e.ins('move.w', '#0x8000,0x50(%a0)', 6)
    e.label('player_pc_013d22')
    e.ins('move.w', '#0x8000,0x3c(%a0)', 6)
    e.label('player_pc_013d28')
    e.ins('move.w', '#0x8000,0x28(%a0)', 6)
    e.label('player_pc_013d2e')
    e.ins('move.w', '#0x8000,0x14(%a0)', 6)
    e.label('player_pc_013d34')
    e.ins('move.w', '#0x8000,(%a0)+', 4)
    e.label('player_pc_013d38')
    e.ins('dbra', '%d0,player_pc_013cfe', 4)
    e.label('player_pc_013d3c')
    e.ins('clr.w', '0xb4(%a0)', 4)
    e.label('player_pc_013d40')
    e.ins('addi.w', '#0xc8,0xf31a:w', 6)
    e.label('player_pc_013d46')
    e.ins('rts', '', 2)

def _lower_prepare_selected_training_cost_steps(e, rules):
    e.label('player_pc_013df6')
    e.ins('lea.l', '0xf500:w,%a0', 4)
    e.label('player_pc_013dfa')
    e.ins('lea.l', '0xc800:w,%a1', 4)
    e.label('player_pc_013dfe')
    e.ins('moveq', '#0,%d0', 2)
    e.label('player_pc_013e00')
    e.ins('move.w', '(%a0)+,%d1', 2)
    e.label('player_pc_013e02')
    e.ins('bmi.w', 'player_pc_013e1a', 4)
    e.label('player_pc_013e06')
    e.ins('btst.l', '#0xe,%d1', 4)
    e.label('player_pc_013e0a')
    e.ins('beq.b', 'player_pc_013e00', 2)
    e.label('player_pc_013e0c')
    e.ins('lsl.w', '#0x2,%d1', 2)
    e.label('player_pc_013e0e')
    e.ins('add.l', '(%a1, %d1.w),%d0', 4)
    e.label('player_pc_013e12')
    e.ins('addi.l', '#0x64,%d0', 6)
    e.label('player_pc_013e18')
    e.ins('bra.b', 'player_pc_013e00', 2)
    e.label('player_pc_013e1a')
    e.ins('divu.w', '#0x64,%d0', 4)
    e.label('player_pc_013e1e')
    e.ins('bne.w', 'player_pc_013e26', 4)
    e.label('player_pc_013e22')
    e.ins('move.w', '#0x1,%d0', 4)
    e.label('player_pc_013e26')
    e.ins('andi.l', '#0xffff,%d0', 6)
    e.label('player_pc_013e2c')
    e.ins('move.l', '%d0,0xf74e:w', 4)
    e.label('player_pc_013e30')
    e.ins('mulu.w', '#0xa,%d0', 4)
    e.label('player_pc_013e34')
    e.ins('move.l', '%d0,0xf752:w', 4)
    e.label('player_pc_013e38')
    e.ins('mulu.w', '#0xa,%d0', 4)
    e.label('player_pc_013e3c')
    e.ins('move.l', '%d0,0xf756:w', 4)
    e.label('player_pc_013e40')
    e.ins('rts', '', 2)

def _lower_update_selected_training_amount(e, rules):
    e.label('player_pc_013e92')
    e.ins('move.b', '0xf602:w,%d0', 4)
    e.label('player_pc_013e96')
    e.ins('andi.w', '#0xc,%d0', 4)
    e.label('player_pc_013e9a')
    e.ins('beq.b', 'player_pc_013ee8', 2)
    e.label('player_pc_013e9c')
    e.ins('subq.w', '#0x1,0xf608:w', 4)
    e.label('player_pc_013ea0')
    e.ins('bne.w', 'player_pc_013f64', 4)
    e.label('player_pc_013ea4')
    e.ins('move.w', '#0xc,0xf608:w', 6)
    e.label('player_pc_013eaa')
    e.ins('btst.l', '#0x3,%d0', 4)
    e.label('player_pc_013eae')
    e.ins('bne.b', 'player_pc_013eda', 2)
    e.label('player_pc_013eb0')
    e.ins('tst.w', '0xf39a:w', 4)
    e.label('player_pc_013eb4')
    e.ins('beq.w', 'player_pc_013f64', 4)
    e.label('player_pc_013eb8')
    e.ins('move.w', '#0x1,%d0', 4)
    e.label('player_pc_013ebc')
    e.ins('sub.w', '0xf39a:w,%d0', 4)
    e.label('player_pc_013ec0')
    e.ins('lsl.w', '#0x2,%d0', 2)
    e.label('player_pc_013ec2')
    e.ins('lea.l', '0xf752:w,%a0', 4)
    e.label('player_pc_013ec6')
    e.ins('move.l', '(%a0, %d0.w),%d0', 4)
    e.label('player_pc_013eca')
    e.ins('cmp.l', '0xf3f8:w,%d0', 4)
    e.label('player_pc_013ece')
    e.ins('bhi.w', 'player_pc_013f64', 4)
    e.label('player_pc_013ed2')
    e.ins('subq.w', '#0x1,0xf39a:w', 4)
    e.label('player_pc_013ed6')
    e.ins('bra.w', 'player_pc_013f64', 4)
    e.label('player_pc_013eda')
    e.ins('cmpi.w', '#0x2,0xf39a:w', 6)
    e.label('player_pc_013ee0')
    e.ins('bcc.w', 'player_pc_013f64', 4)
    e.label('player_pc_013ee4')
    e.ins('addq.w', '#0x1,0xf39a:w', 4)
    e.label('player_pc_013ee8')
    e.ins('move.b', '0xf602:w,%d0', 4)
    e.label('player_pc_013eec')
    e.ins('andi.b', '#0x3,%d0', 4)
    e.label('player_pc_013ef0')
    e.ins('beq.b', 'player_pc_013f5e', 2)
    e.label('player_pc_013ef2')
    e.ins('subq.w', '#0x1,0xf608:w', 4)
    e.label('player_pc_013ef6')
    e.ins('bne.w', 'player_pc_013f64', 4)
    e.label('player_pc_013efa')
    e.ins('move.w', '#0xc,0xf608:w', 6)
    e.label('player_pc_013f00')
    e.ins('move.w', '#0x2,%d1', 4)
    e.label('player_pc_013f04')
    e.ins('sub.w', '0xf39a:w,%d1', 4)
    e.label('player_pc_013f08')
    e.ins('lsl.w', '#0x2,%d1', 2)
    e.label('player_pc_013f0a')
    e.ins('lea.l', '0xf74e:w,%a0', 4)
    e.label('player_pc_013f0e')
    e.ins('move.l', '(%a0, %d1.w),%d2', 4)
    e.label('player_pc_013f12')
    e.ins('lsr.w', '#0x1,%d1', 2)
    e.label('player_pc_013f14')
    e.ins('move.w', '80(%pc, %d1.w),%d4', 4)
    e.label('player_pc_013f18')
    e.ins('btst.l', '#0x1,%d0', 4)
    e.label('player_pc_013f1c')
    e.ins('bne.w', 'player_pc_013f48', 4)
    e.label('player_pc_013f20')
    e.ins('move.l', '0xf3ba:w,%d3', 4)
    e.label('player_pc_013f24')
    e.ins('add.l', '%d2,%d3', 2)
    e.label('player_pc_013f26')
    e.ins('cmp.l', '0xf3f8:w,%d3', 4)
    e.label('player_pc_013f2a')
    e.ins('bhi.w', 'player_pc_013f64', 4)
    e.label('player_pc_013f2e')
    e.ins('move.w', '0xf670:w,%d5', 4)
    e.label('player_pc_013f32')
    e.ins('add.w', '%d4,%d5', 2)
    e.label('player_pc_013f34')
    e.ins('cmpi.w', '#0x3e8,%d5', 4)
    e.label('player_pc_013f38')
    e.ins('bcc.w', 'player_pc_013f64', 4)
    e.label('player_pc_013f3c')
    e.ins('move.l', '%d3,0xf3ba:w', 4)
    e.label('player_pc_013f40')
    e.ins('move.w', '%d5,0xf670:w', 4)
    e.label('player_pc_013f44')
    e.ins('bra.w', 'player_pc_013f64', 4)
    e.label('player_pc_013f48')
    e.ins('move.l', '0xf3ba:w,%d3', 4)
    e.label('player_pc_013f4c')
    e.ins('sub.l', '%d2,%d3', 2)
    e.label('player_pc_013f4e')
    e.ins('bcs.w', 'player_pc_013f64', 4)
    e.label('player_pc_013f52')
    e.ins('move.l', '%d3,0xf3ba:w', 4)
    e.label('player_pc_013f56')
    e.ins('sub.w', '%d4,0xf670:w', 4)
    e.label('player_pc_013f5a')
    e.ins('bra.w', 'player_pc_013f64', 4)
    e.label('player_pc_013f5e')
    e.ins('move.w', '#0x1,0xf608:w', 6)
    e.label('player_pc_013f64')
    e.ins('rts', '', 2)

def _lower_append_training_cost_digits(e, rules):
    e.label('player_pc_013f6c')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_013f70')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_013f74')
    e.ins('move.l', '0xf3ba:w,%d0', 4)
    e.label('player_pc_013f78')
    e.ins('move.w', '#0xc386,%d1', 4)
    e.label('player_pc_013f7c')
    e.ins('move.w', '#0xc001,%d2', 4)
    e.label('player_pc_013f80')
    e.ins('lea.l', '0xd300:w,%a6', 4)
    e.label('player_pc_013f84')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_013f8a')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_013f8e')
    e.ins('move.w', '#0xc6ac,(%a0)+', 4)
    e.label('player_pc_013f92')
    e.ins('lea.l', '0xd300:w,%a1', 4)
    e.label('player_pc_013f96')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_013f9a')
    e.ins('move.w', '(%a1)+,(%a0)+', 2)
    e.label('player_pc_013f9c')
    e.ins('dbra', '%d0,player_pc_013f9a', 4)
    e.label('player_pc_013fa0')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_013fa2')
    e.ins('addi.w', '#0x10,0xf31a:w', 6)
    e.label('player_pc_013fa8')
    e.ins('rts', '', 2)

def _lower_append_training_amount_cursor(e, rules):
    e.label('player_pc_013faa')
    e.ins('move.w', '0xf602:w,%d0', 4)
    e.label('player_pc_013fae')
    e.ins('andi.w', '#0x30,%d0', 4)
    e.label('player_pc_013fb2')
    e.ins('bne.w', 'player_pc_013fda', 4)
    e.label('player_pc_013fb6')
    e.ins('btst.b', '#0x3,0xf321:w', 6)
    e.label('player_pc_013fbc')
    e.ins('bne.w', 'player_pc_013fda', 4)
    e.label('player_pc_013fc0')
    e.ins('lea.l', '26(%pc),%a0', 4)
    e.label('player_pc_013fc4')
    e.ins('move.w', '#0x58,%d0', 4)
    e.label('player_pc_013fc8')
    e.ins('move.w', '0xf39a:w,%d1', 4)
    e.label('player_pc_013fcc')
    e.ins('lsl.w', '#0x3,%d1', 2)
    e.label('player_pc_013fce')
    e.ins('addi.w', '#0xa8,%d1', 4)
    e.label('player_pc_013fd2')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_013fd4')
    e.ins('jsr', 'player_pc_00ac08:l', 6)
    e.label('player_pc_013fda')
    e.ins('rts', '', 2)

def _lower_prepare_selected_training_origin_and_speed(e, rules):
    e.label('player_pc_013fe4')
    e.ins('lea.l', '0xf500:w,%a0', 4)
    e.label('player_pc_013fe8')
    e.ins('lea.l', '0xc400:w,%a1', 4)
    e.label('player_pc_013fec')
    e.ins('clr.l', '%d0', 2)
    e.label('player_pc_013fee')
    e.ins('clr.w', '%d1', 2)
    e.label('player_pc_013ff0')
    e.ins('move.w', '0xf364:w,%d2', 4)
    e.label('player_pc_013ff4')
    e.ins('lsl.w', '#0x2,%d2', 2)
    e.label('player_pc_013ff6')
    e.ins('lea.l', '0xd4ac6:l,%a5', 6)
    e.label('player_pc_013ffc')
    e.ins('move.w', '0x2(%a5, %d2.w),%d3', 4)
    e.label('player_pc_014000')
    e.ins('andi.w', '#0xfff0,%d3', 4)
    e.label('player_pc_014004')
    e.ins('move.w', '%d3,0xff3822:l', 6)
    e.label('player_pc_01400a')
    e.ins('lsl.w', '#0x4,%d3', 2)
    e.label('player_pc_01400c')
    e.ins('andi.w', '#0xff00,%d3', 4)
    e.label('player_pc_014010')
    e.ins('move.w', '(%a5, %d2.w),%d4', 4)
    e.label('player_pc_014014')
    e.ins('andi.w', '#0xfff0,%d4', 4)
    e.label('player_pc_014018')
    e.ins('move.w', '%d4,0xff3824:l', 6)
    e.label('player_pc_01401e')
    e.ins('lsr.w', '#0x4,%d4', 2)
    e.label('player_pc_014020')
    e.ins('or.w', '%d3,%d4', 2)
    e.label('player_pc_014022')
    e.ins('move.w', '%d4,0xff3828:l', 6)
    e.label('player_pc_014028')
    e.ins('move.w', '(%a0)+,%d2', 2)
    e.label('player_pc_01402a')
    e.ins('bmi.b', 'player_pc_014042', 2)
    e.label('player_pc_01402c')
    e.ins('cmpi.w', '#0x4000,%d2', 4)
    e.label('player_pc_014030')
    e.ins('bcs.b', 'player_pc_014028', 2)
    e.label('player_pc_014032')
    e.ins('addq.w', '#0x1,%d1', 2)
    e.label('player_pc_014034')
    e.ins('andi.w', '#0xff,%d2', 4)
    e.label('player_pc_014038')
    e.ins('clr.w', '%d3', 2)
    e.label('player_pc_01403a')
    e.ins('move.b', '(%a1, %d2.w),%d3', 4)
    e.label('player_pc_01403e')
    e.ins('add.w', '%d3,%d0', 2)
    e.label('player_pc_014040')
    e.ins('bra.b', 'player_pc_014028', 2)
    e.label('player_pc_014042')
    e.ins('move.w', '%d1,0xff382a:l', 6)
    e.label('player_pc_014048')
    e.ins('divu.w', '%d1,%d0', 2)
    e.label('player_pc_01404a')
    e.ins('move.w', '%d0,0xf672:w', 4)
    e.label('player_pc_01404e')
    e.ins('rts', '', 2)

LOWERERS = {
    'update_recruitment_input_cursor':_lower_update_recruitment_input_cursor,
    'update_recruitment_total_cursor':_lower_update_recruitment_total_cursor,
    'append_recruitment_dialog_frame':_lower_append_recruitment_dialog_frame,
    'append_recruitment_paired_tiles':_lower_append_recruitment_paired_tiles,
    'prepare_player_recruitment_capacity':_lower_prepare_player_recruitment_capacity,
    'append_recruitment_input_digits':_lower_append_recruitment_input_digits,
    'append_recruitment_total_digits':_lower_append_recruitment_total_digits,
    'append_equipment_amount_cursor':_lower_append_equipment_amount_cursor,
    'clear_equipment_dialog_rows':_lower_clear_equipment_dialog_rows,
    'append_equipment_dialog_frame':_lower_append_equipment_dialog_frame,
    'append_equipment_paired_tiles':_lower_append_equipment_paired_tiles,
    'append_equipment_input_digits':_lower_append_equipment_input_digits,
    'append_equipment_total_digits':_lower_append_equipment_total_digits,
    'append_candidate_amount_cursor':_lower_append_candidate_amount_cursor,
    'append_candidate_dialog_frame':_lower_append_candidate_dialog_frame,
    'append_candidate_paired_tiles':_lower_append_candidate_paired_tiles,
    'append_candidate_separator_row':_lower_append_candidate_separator_row,
    'update_equipment_category':_lower_update_equipment_category,
    'append_equipment_category_cursor':_lower_append_equipment_category_cursor,
    'clear_candidate_dialog_rows':_lower_clear_candidate_dialog_rows,
    'prepare_selected_training_cost_steps':_lower_prepare_selected_training_cost_steps,
    'update_selected_training_amount':_lower_update_selected_training_amount,
    'append_training_cost_digits':_lower_append_training_cost_digits,
    'append_training_amount_cursor':_lower_append_training_amount_cursor,
    'prepare_selected_training_origin_and_speed':_lower_prepare_selected_training_origin_and_speed,
}

DECLARATIONS.update({'_append_input_digits_fields': {'signature': 'memory: EquipmentMenuMemory, scalar_name: str, numeric_continuation: Long | '
              'None=None',
 'returns': 'EquipmentMenuFields',
 'flow': 'if type(memory) is not EquipmentMenuMemory:\n'
         "    raise ValueError('sealed equipment-menu memory required')\n"
         'value = memory.scalar(scalar_name)\n'
         "numeric_destination = memory.view('recruitment_digit_scratch').cursor()\n"
         'if memory.stack_cursor is not None:\n'
         '    if numeric_continuation is None:\n'
         "        raise Boundary('unobserved original1270A continuation')\n"
         '    memory.enter_call(numeric_continuation)\n'
         'formatted = _six_place_decimal_fields(memory.numeric, value, 50054, 0, '
         'numeric_destination)\n'
         'if memory.stack_cursor is not None:\n'
         '    memory.leave_call(numeric_continuation)\n'
         "destination = memory.view('display_queue').cursor(memory.scalar('queue_offset'))\n"
         'destination.append_word(6)\n'
         'destination.append_word(50596)\n'
         "source = memory.view('recruitment_digit_scratch').cursor()\n"
         'counter = u16(5)\n'
         'for position in range(6):\n'
         '    tile = source.next_word()\n'
         '    if tile == 0:\n'
         "        tile = 49153 if position < memory.scalar('amount_digit_position') else 50054\n"
         '    destination.append_word(tile)\n'
         '    counter = u16(counter - 1)\n'
         'carry, zero, negative, overflow = _finish_queue_fields(memory, destination, 16)\n'
         'return EquipmentMenuFields(destination, source, counter, u16(position + 1), tile, '
         'formatted.divisor, replace_word(formatted.remainder, counter), carry, zero, negative, '
         'overflow).validate(memory)'},
 '_append_large_dialog_fields': {'signature': 'memory: EquipmentMenuMemory, first_labels: tuple, second_labels: tuple, '
              'first_continuations: tuple | None=None, second_continuations: tuple | None=None',
 'returns': 'EquipmentMenuFields',
 'flow': 'if type(memory) is not EquipmentMenuMemory:\n'
         "    raise ValueError('sealed equipment-menu memory required')\n"
         "destination = memory.view('display_queue').cursor(memory.scalar('queue_offset'))\n"
         'field = None\n'
         'destination.append_word(15)\n'
         'destination.append_word(50324)\n'
         'destination.append_word(50048)\n'
         'for _ in range(13):\n'
         '    destination.append_word(50049)\n'
         'destination.append_word(52096)\n'
         'destination.set_word(0, 15, 34)\n'
         'destination.append_word(15)\n'
         'destination.set_word(0, 50580, 34)\n'
         'destination.append_word(50452)\n'
         'destination.set_word(0, 50050, 34)\n'
         'destination.append_word(50050)\n'
         'for label_index, (tile, counter) in enumerate(first_labels):\n'
         '    if memory.stack_cursor is not None:\n'
         '        if first_continuations is None:\n'
         "            raise Boundary('unobserved original paired-tile continuation')\n"
         '        memory.enter_call(first_continuations[label_index])\n'
         '    pair = _paired_tiles_fields(memory, destination, tile, counter, 34)\n'
         '    if memory.stack_cursor is not None:\n'
         '        memory.leave_call(first_continuations[label_index])\n'
         '    destination = pair.destination\n'
         '    field = pair.field_if_written\n'
         'for _ in range(7):\n'
         '    destination.set_word(0, 49153, 34)\n'
         '    destination.append_word(49153)\n'
         'destination.set_word(0, 52098, 34)\n'
         'destination.append_word(52098)\n'
         'destination.base = u32(destination.base + 34)\n'
         'destination.append_word(15)\n'
         'destination.append_word(50708)\n'
         'destination.append_word(50050)\n'
         'for _ in range(13):\n'
         '    destination.append_word(49153)\n'
         'destination.append_word(52098)\n'
         'destination.set_word(0, 15, 34)\n'
         'destination.append_word(15)\n'
         'destination.set_word(0, 50964, 34)\n'
         'destination.append_word(50836)\n'
         'destination.set_word(0, 50050, 34)\n'
         'destination.append_word(50050)\n'
         'for label_index, (tile, counter) in enumerate(second_labels):\n'
         '    if memory.stack_cursor is not None:\n'
         '        if second_continuations is None:\n'
         "            raise Boundary('unobserved original paired-tile continuation')\n"
         '        memory.enter_call(second_continuations[label_index])\n'
         '    pair = _paired_tiles_fields(memory, destination, tile, counter, 34)\n'
         '    if memory.stack_cursor is not None:\n'
         '        memory.leave_call(second_continuations[label_index])\n'
         '    destination = pair.destination\n'
         '    field = pair.field_if_written\n'
         'label_cells = sum((counter + 1 for _, counter in second_labels))\n'
         'for _ in range(13 - label_cells):\n'
         '    destination.set_word(0, 49153, 34)\n'
         '    destination.append_word(49153)\n'
         'destination.set_word(0, 52098, 34)\n'
         'destination.append_word(52098)\n'
         'destination.base = u32(destination.base + 34)\n'
         'destination.append_word(15)\n'
         'destination.append_word(51092)\n'
         'destination.append_word(54144)\n'
         'for _ in range(13):\n'
         '    destination.append_word(54145)\n'
         'destination.append_word(56192)\n'
         'carry, zero, negative, overflow = _finish_queue_fields(memory, destination, 238)\n'
         'return EquipmentMenuFields(destination, None, 65535, field, None, None, None, carry, '
         'zero, negative, overflow).validate(memory)'},
 '_append_total_digits_fields': {'signature': 'memory: EquipmentMenuMemory, value: Long, numeric_continuation: Long | None=None',
 'returns': 'EquipmentMenuFields',
 'flow': 'if type(memory) is not EquipmentMenuMemory:\n'
         "    raise ValueError('sealed equipment-menu memory required')\n"
         "numeric_destination = memory.view('command_digit_scratch').cursor()\n"
         'if memory.stack_cursor is not None:\n'
         '    if numeric_continuation is None:\n'
         "        raise Boundary('unobserved original1270A continuation')\n"
         '    memory.enter_call(numeric_continuation)\n'
         'formatted = _six_place_decimal_fields(memory.numeric, value, 50054, 49153, '
         'numeric_destination)\n'
         'if memory.stack_cursor is not None:\n'
         '    memory.leave_call(numeric_continuation)\n'
         "destination = memory.view('display_queue').cursor(memory.scalar('queue_offset'))\n"
         'destination.append_word(6)\n'
         'destination.append_word(50980)\n'
         "source = memory.view('command_digit_scratch').cursor()\n"
         'counter = u16(2)\n'
         'for _ in range(3):\n'
         '    destination.append_long(source.next_long())\n'
         '    counter = u16(counter - 1)\n'
         'carry, zero, negative, overflow = _finish_queue_fields(memory, destination, 16)\n'
         'return EquipmentMenuFields(destination, source, counter, 50054, 49153, '
         'formatted.divisor, replace_word(formatted.remainder, counter), carry, zero, negative, '
         'overflow).validate(memory)'},
 '_finish_queue_fields': {'signature': 'memory: EquipmentMenuMemory, destination: Cursor, length: '
                                       'Word',
                          'returns': 'tuple',
                          'flow': 'if type(memory) is not EquipmentMenuMemory:\n'
                                  "    raise ValueError('sealed equipment-menu memory required')\n"
                                  'memory.check_cursor(destination)\n'
                                  'uint(length, 16)\n'
                                  'destination.word()\n'
                                  'destination.put_word(0)\n'
                                  "previous = memory.scalar('queue_offset')\n"
                                  'current = u16(previous + length)\n'
                                  "memory.set_scalar('queue_offset', current)\n"
                                  'return (previous + length > 65535, current == 0, bool(current & '
                                  '32768), bool(~(previous ^ length) & (previous ^ current) & '
                                  '32768))'},
 '_paired_tiles_fields': {'signature': 'memory: EquipmentMenuMemory, destination: Cursor, tile: '
                                       'Word, counter: Word, row_stride: Word',
                          'returns': 'EquipmentMenuFields',
                          'flow': 'if type(memory) is not EquipmentMenuMemory:\n'
                                  "    raise ValueError('sealed equipment-menu memory required')\n"
                                  'memory.check_cursor(destination)\n'
                                  'uint(tile, 16)\n'
                                  'uint(counter, 16)\n'
                                  'uint(row_stride, 16)\n'
                                  'for _ in descending_inclusive(counter):\n'
                                  '    destination.put_word(tile)\n'
                                  '    old_tile = tile\n'
                                  '    tile = u16(tile + 1)\n'
                                  '    destination.set_word(0, tile, row_stride)\n'
                                  '    old_tile = tile\n'
                                  '    tile = u16(tile + 1)\n'
                                  '    destination.base = u32(destination.base + 2)\n'
                                  '    counter = u16(counter - 1)\n'
                                  'return EquipmentMenuFields(destination, None, tile, counter, '
                                  'None, None, None, old_tile + 1 > 65535, tile == 0, bool(tile & '
                                  '32768), bool(~(old_tile ^ 1) & (old_tile ^ tile) & '
                                  '32768)).validate(memory)'},
 'append_equipment_dialog_frame_fields': {'signature': 'memory: EquipmentMenuMemory',
 'returns': 'EquipmentMenuFields',
 'flow': 'return _append_large_dialog_fields(memory, ((49169, 3), (49185, 1)), ((49177, 1), '
         '(49189, 1), (49185, 1)), (79378, 79390), (79492, 79504, 79516))'},
 'append_equipment_input_digits_fields': {'signature': 'memory: EquipmentMenuMemory',
 'returns': 'EquipmentMenuFields',
 'flow': "return _append_input_digits_fields(memory, 'equipment_input', 79624)"},
 'append_equipment_total_digits_fields': {'signature': 'memory: EquipmentMenuMemory',
 'returns': 'EquipmentMenuFields',
 'flow': 'if type(memory) is not EquipmentMenuMemory:\n'
         "    raise ValueError('sealed equipment-menu memory required')\n"
         "if memory.scalar('command_id') == 27:\n"
         "    value = memory.scalar('special_equipment_amount')\n"
         'else:\n'
         "    value = memory.scalar('recruitment_input')\n"
         'return _append_total_digits_fields(memory, value, 79730)'}})


APPROVED.setdefault('contexts_equipment', set()).update({'EquipmentMenuMemory', 'EquipmentMenuFields'})
APPROVED.setdefault('business_budget', set()).update({'_six_place_decimal_fields'})

def compile_recruitment(source):
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    records['append_equipment_dialog_frame']['effects'] = dict(legacy_projection=records['append_equipment_dialog_frame']['effects'], supplied_unique_fields={name: records[name]['effects'] for name in ('_finish_queue_fields', '_paired_tiles_fields', '_append_large_dialog_fields', '_append_input_digits_fields', '_append_total_digits_fields', 'append_equipment_dialog_frame_fields')})
    records['append_equipment_input_digits']['effects'] = dict(legacy_projection=records['append_equipment_input_digits']['effects'], supplied_unique_fields={name: records[name]['effects'] for name in ('_finish_queue_fields', '_paired_tiles_fields', '_append_large_dialog_fields', '_append_input_digits_fields', '_append_total_digits_fields', 'append_equipment_input_digits_fields')})
    records['append_equipment_total_digits']['effects'] = dict(legacy_projection=records['append_equipment_total_digits']['effects'], supplied_unique_fields={name: records[name]['effects'] for name in ('_finish_queue_fields', '_paired_tiles_fields', '_append_large_dialog_fields', '_append_input_digits_fields', '_append_total_digits_fields', 'append_equipment_total_digits_fields')})
    return lower_declared({b.name:records[b.name] for b in RECRUITMENT_BINDINGS}, RECRUITMENT_BINDINGS, LOWERERS)

# C56 complete menu ABI and honest same-core compatibility declarations.
DECLARATIONS.update({'_append_input_digits_fields': {'signature': 'memory: EquipmentMenuMemory, scalar_name: str, numeric_continuation: Long | None=None, *, entry_frame: CommandFrame | None=None', 'returns': 'EquipmentMenuFields', 'flow': "if scalar_name == 'recruitment_input':\n    target = 78364\nelif scalar_name == 'equipment_input':\n    target = 79604\nelse:\n    raise ValueError('only original input rows required')\nreturn _equipment_complete_projection(memory, entry_frame, target)"}, '_append_large_dialog_fields': {'signature': 'memory: EquipmentMenuMemory, first_labels: tuple, second_labels: tuple, first_continuations: tuple | None=None, second_continuations: tuple | None=None, *, entry_frame: CommandFrame | None=None', 'returns': 'EquipmentMenuFields', 'flow': "if (first_labels, second_labels) == (((49181, 3), (49157, 1)), ((49161, 3),)):\n    target = 77930\nelif (first_labels, second_labels) == (((49169, 3), (49185, 1)), ((49177, 1), (49189, 1), (49185, 1))):\n    target = 79300\nelse:\n    raise ValueError('only original closed dialog label plans required')\nreturn _equipment_complete_projection(memory, entry_frame, target)"}, '_append_total_digits_fields': {'signature': 'memory: EquipmentMenuMemory, value: Long, numeric_continuation: Long | None=None, *, entry_frame: CommandFrame | None=None', 'returns': 'EquipmentMenuFields', 'flow': "if numeric_continuation == 78470:\n    target = 78448\nelif numeric_continuation == 79730:\n    target = 79690\nelse:\n    raise Boundary('partial total row lacks its actual original role')\nreturn _equipment_complete_projection(memory, entry_frame, target)"}, '_equipment_complete_projection': {'signature': 'memory, entry_frame, target', 'returns': None, 'flow': "if type(memory) is not EquipmentMenuMemory:\n    raise ValueError('actual equipment memory required')\nif entry_frame is None:\n    raise Boundary('historical partial equipment fields did not observe full D/A/SR-X/SP')\ncomplete = CommandMenuMemory(memory.state)\nactual = _recruitment_known_fields(complete, complete.enter(entry_frame), target)\nif actual is None:\n    complete.stop(entry_frame, target, 'unknown legacy equipment role')\nmemory.numeric.stack_cursor = complete.cursor_at(actual.addresses[7])\nstatus = actual.status_word\nreturn EquipmentMenuFields(complete.cursor_at(actual.addresses[0]), complete.cursor_at(actual.addresses[1]), actual.data[0] & 65535, actual.data[1] & 65535, actual.data[2] & 65535, actual.data[3] & 65535, actual.data[0], bool(status & 1), bool(status & 4), bool(status & 8), bool(status & 2)).validate(memory)"}, '_recruitment_known_fields': {'signature': 'memory, frame, target', 'returns': None, 'flow': 'if target == 77656:\n    return update_recruitment_input_cursor_frame_fields(memory, frame)\nif target == 77876:\n    return update_recruitment_total_cursor_frame_fields(memory, frame)\nif target == 77930:\n    return append_recruitment_dialog_frame_frame_fields(memory, frame)\nif target == 78198:\n    return append_recruitment_paired_tiles_frame_fields(memory, frame)\nif target == 78216:\n    return prepare_player_recruitment_capacity_frame_fields(memory, frame)\nif target == 78364:\n    return append_recruitment_input_digits_frame_fields(memory, frame)\nif target == 78448:\n    return append_recruitment_total_digits_frame_fields(memory, frame)\nif target == 79120:\n    return append_equipment_amount_cursor_frame_fields(memory, frame)\nif target == 79166:\n    return clear_equipment_dialog_rows_frame_fields(memory, frame)\nif target == 79300:\n    return append_equipment_dialog_frame_frame_fields(memory, frame)\nif target == 79586:\n    return append_equipment_paired_tiles_frame_fields(memory, frame)\nif target == 79604:\n    return append_equipment_input_digits_frame_fields(memory, frame)\nif target == 79690:\n    return append_equipment_total_digits_frame_fields(memory, frame)\nif target == 80180:\n    return append_candidate_amount_cursor_frame_fields(memory, frame)\nif target == 80216:\n    return append_candidate_dialog_frame_frame_fields(memory, frame)\nif target == 80516:\n    return append_candidate_paired_tiles_frame_fields(memory, frame)\nif target == 80534:\n    return append_candidate_separator_row_frame_fields(memory, frame)\nif target == 80774:\n    return update_equipment_category_frame_fields(memory, frame)\nif target == 80858:\n    return append_equipment_category_cursor_frame_fields(memory, frame)\nif target == 81022:\n    return clear_candidate_dialog_rows_frame_fields(memory, frame)\nif target == 81398:\n    return prepare_selected_training_cost_steps_frame_fields(memory, frame)\nif target == 81554:\n    return update_selected_training_amount_frame_fields(memory, frame)\nif target == 81772:\n    return append_training_cost_digits_frame_fields(memory, frame)\nif target == 81834:\n    return append_training_amount_cursor_frame_fields(memory, frame)\nif target == 81892:\n    return prepare_selected_training_origin_and_speed_frame_fields(memory, frame)\nreturn None'}, 'append_candidate_amount_cursor': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 80180)\nactual = append_candidate_amount_cursor_frame_fields(memory, entered)\nreturn None'}, 'append_candidate_amount_cursor_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\ntested = memory.state.read(4294964001, 1)\nframe = _command_bit_fields(memory, frame, tested, 3 % 8)\nif not not frame.status_word & 4:\n    frame = frame.with_address(0, u32(80190 + -3758))\n    frame = _command_load_fields(memory, frame, 0, 88, 16)\n    value = memory.state.read(4294964122, 2)\n    frame = _command_load_fields(memory, frame, 1, value, 16)\n    frame = _command_shift_fields(memory, frame, 1, 3, 16, False)\n    frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 144, 16, False, False)\n    frame = frame.with_data(1, result, 16)\n    frame = _command_load_fields(memory, frame, 2, 0, 16)\n    frame = _command_call_fields(memory, frame, 44040, 80214)\nreturn frame'}, 'append_candidate_dialog_frame': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 80216)\nactual = append_candidate_dialog_frame_frame_fields(memory, entered)\nreturn None'}, 'append_candidate_dialog_frame_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50208, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 2, 50464, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 8, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), frame.data[2] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 128, 16, True, False)\nframe = frame.with_data(2, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[2] & 65535, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 256, 16, False, False)\nframe = frame.with_data(2, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 49157, 16)\nframe = _command_load_fields(memory, frame, 1, 5, 16)\nframe = _command_call_fields(memory, frame, 80516, 80302)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(20))\nframe = _command_call_fields(memory, frame, 80534, 80320)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 8, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), frame.data[2] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 128, 16, True, False)\nframe = frame.with_data(2, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[2] & 65535, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 256, 16, False, False)\nframe = frame.with_data(2, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 49169, 16)\nframe = _command_load_fields(memory, frame, 1, 1, 16)\nframe = _command_call_fields(memory, frame, 80516, 80366)\nframe = _command_load_fields(memory, frame, 0, 49161, 16)\nframe = _command_load_fields(memory, frame, 1, 3, 16)\nframe = _command_call_fields(memory, frame, 80516, 80378)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(20))\nframe = _command_call_fields(memory, frame, 80534, 80396)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 8, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), frame.data[2] & 65535, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 128, 16, True, False)\nframe = frame.with_data(2, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[2] & 65535, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 256, 16, False, False)\nframe = frame.with_data(2, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 49157, 16)\nframe = _command_load_fields(memory, frame, 1, 1, 16)\nframe = _command_call_fields(memory, frame, 80516, 80442)\nframe = _command_load_fields(memory, frame, 0, 49173, 16)\nframe = _command_load_fields(memory, frame, 1, 1, 16)\nframe = _command_call_fields(memory, frame, 80516, 80454)\nframe = _command_load_fields(memory, frame, 0, 49169, 16)\nframe = _command_load_fields(memory, frame, 1, 1, 16)\nframe = _command_call_fields(memory, frame, 80516, 80466)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(20))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[2] & 65535, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54145, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 56192, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 200, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'append_candidate_paired_tiles_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': "frame = memory.enter(frame)\nreturn _command_numbered_pair_fields(memory, frame, 'candidate')"}, 'append_candidate_separator_row': {'signature': 'state: GameState, context: SeparatorRowContext, *, entry_frame: CommandFrame | None=None', 'returns': 'SeparatorRowResult', 'flow': "memory, entered = _command_legacy_entry(state, entry_frame, 80534)\ncontext = checked_context(context, SeparatorRowContext, state)\nif context.destination.base != entered.addresses[0] or context.coordinate != entered.data[0]:\n    raise ValueError('separator context must match real A0/D0 entry')\nactual = append_candidate_separator_row_frame_fields(memory, entered)\nreturn SeparatorRowResult(memory.cursor_at(actual.addresses[0]), actual.data[0])"}, 'append_candidate_separator_row_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[2] & 65535, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 256, 16, False, False)\nframe = frame.with_data(2, result, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nreturn frame'}, 'append_equipment_amount_cursor': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 79120)\nactual = append_equipment_amount_cursor_frame_fields(memory, entered)\nreturn None'}, 'append_equipment_amount_cursor_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\ntested = memory.state.read(4294964739, 1)\nframe = _command_bit_fields(memory, frame, tested, 5 % 8)\nif not not frame.status_word & 4:\n    tested = memory.state.read(4294964001, 1)\n    frame = _command_bit_fields(memory, frame, tested, 3 % 8)\n    if not not frame.status_word & 4:\n        frame = frame.with_address(0, u32(79140 + -2708))\n        frame = _command_load_fields(memory, frame, 0, 88, 16)\n        value = memory.state.read(4294964122, 2)\n        frame = _command_load_fields(memory, frame, 1, value, 16)\n        frame = _command_shift_fields(memory, frame, 1, 3, 16, False)\n        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 144, 16, False, False)\n        frame = frame.with_data(1, result, 16)\n        frame = _command_load_fields(memory, frame, 2, 0, 16)\n        frame = _command_call_fields(memory, frame, 44040, 79164)\nreturn frame'}, 'append_equipment_category_cursor': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 80858)\nactual = append_equipment_category_cursor_frame_fields(memory, entered)\nreturn None'}, 'append_equipment_category_cursor_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\ntested = memory.state.read(4294964739, 1)\nframe = _command_bit_fields(memory, frame, tested, 5 % 8)\nif not not frame.status_word & 4:\n    value = memory.state.read(4294964738, 1)\n    frame = _command_load_fields(memory, frame, 0, value, 8)\n    result = frame.data[0] & 65535 & 3\n    frame = _command_load_fields(memory, frame, 0, result, 16)\n    if not frame.status_word & 4:\n        frame = frame.with_address(0, u32(80890 + 34))\n        value = memory.state.read(4294964872, 2)\n        frame = _command_load_fields(memory, frame, 0, value, 16)\n        frame = _command_shift_fields(memory, frame, 0, 1, 16, False)\n        source = memory.state.read(4294964872, 2)\n        frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, source, 16, False, False)\n        frame = frame.with_data(0, result, 16)\n        frame = _command_shift_fields(memory, frame, 0, 3, 16, False)\n        frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 64, 16, False, False)\n        frame = frame.with_data(0, result, 16)\n        frame = _command_load_fields(memory, frame, 1, 128, 16)\n        frame = _command_load_fields(memory, frame, 2, 0, 16)\n        frame = _command_call_fields(memory, frame, 44040, 80922)\n    else:\n        tested = memory.state.read(4294964001, 1)\n        frame = _command_bit_fields(memory, frame, tested, 4 % 8)\n        if not not frame.status_word & 4:\n            frame = frame.with_address(0, u32(80890 + 34))\n            value = memory.state.read(4294964872, 2)\n            frame = _command_load_fields(memory, frame, 0, value, 16)\n            frame = _command_shift_fields(memory, frame, 0, 1, 16, False)\n            source = memory.state.read(4294964872, 2)\n            frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, source, 16, False, False)\n            frame = frame.with_data(0, result, 16)\n            frame = _command_shift_fields(memory, frame, 0, 3, 16, False)\n            frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 64, 16, False, False)\n            frame = frame.with_data(0, result, 16)\n            frame = _command_load_fields(memory, frame, 1, 128, 16)\n            frame = _command_load_fields(memory, frame, 2, 0, 16)\n            frame = _command_call_fields(memory, frame, 44040, 80922)\nreturn frame'}, 'append_equipment_dialog_frame': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 79300)\nactual = append_equipment_dialog_frame_frame_fields(memory, entered)\nreturn None'}, 'append_equipment_dialog_frame_fields': {'signature': 'memory: EquipmentMenuMemory, *, entry_frame: CommandFrame | None=None', 'returns': 'EquipmentMenuFields', 'flow': 'return _equipment_complete_projection(memory, entry_frame, 79300)'}, 'append_equipment_dialog_frame_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50324, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 12, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 15, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50580, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50452, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 49169, 16)\nframe = _command_load_fields(memory, frame, 1, 3, 16)\nframe = _command_call_fields(memory, frame, 79586, 79378)\nframe = _command_load_fields(memory, frame, 0, 49185, 16)\nframe = _command_load_fields(memory, frame, 1, 1, 16)\nframe = _command_call_fields(memory, frame, 79586, 79390)\nframe = _command_load_fields(memory, frame, 0, 6, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 49153, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(34))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50708, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 12, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 15, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50964, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50836, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 49177, 16)\nframe = _command_load_fields(memory, frame, 1, 1, 16)\nframe = _command_call_fields(memory, frame, 79586, 79492)\nframe = _command_load_fields(memory, frame, 0, 49189, 16)\nframe = _command_load_fields(memory, frame, 1, 1, 16)\nframe = _command_call_fields(memory, frame, 79586, 79504)\nframe = _command_load_fields(memory, frame, 0, 49185, 16)\nframe = _command_load_fields(memory, frame, 1, 1, 16)\nframe = _command_call_fields(memory, frame, 79586, 79516)\nframe = _command_load_fields(memory, frame, 0, 6, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 49153, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(34))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 51092, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 12, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54145, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 56192, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 238, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'append_equipment_input_digits': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 79604)\nactual = append_equipment_input_digits_frame_fields(memory, entered)\nreturn None'}, 'append_equipment_input_digits_fields': {'signature': 'memory: EquipmentMenuMemory, *, entry_frame: CommandFrame | None=None', 'returns': 'EquipmentMenuFields', 'flow': 'return _equipment_complete_projection(memory, entry_frame, 79604)'}, 'append_equipment_input_digits_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nvalue = memory.state.read(4294964206, 4)\nframe = _command_load_fields(memory, frame, 0, value, 32)\nframe = _command_load_fields(memory, frame, 1, 50054, 16)\nframe = _command_load_fields(memory, frame, 2, 0, 16)\nframe = frame.with_address(6, 4294962944)\nframe = _command_call_fields(memory, frame, 75530, 79624)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50596, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 1, 0, 16)\nframe = frame.with_address(1, 4294962944)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nwhile True:\n    value = memory.state.read(u32(frame.addresses[1]), 2)\n    frame = frame.with_address(1, frame.addresses[1] + 2)\n    frame = _command_load_fields(memory, frame, 2, value, 16)\n    if not not frame.status_word & 4:\n        source = memory.state.read(4294964122, 2)\n        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, source, 16, True, True)\n        if bool(frame.status_word & 1):\n            frame = _command_load_fields(memory, frame, 2, 49153, 16)\n        else:\n            frame = _command_load_fields(memory, frame, 2, 50054, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[2] & 65535, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, False, False)\n    frame = frame.with_data(1, result, 16)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 16, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'append_equipment_paired_tiles_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': "frame = memory.enter(frame)\nreturn _command_numbered_pair_fields(memory, frame, 'recruitment_equipment')"}, 'append_equipment_total_digits': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 79690)\nactual = append_equipment_total_digits_frame_fields(memory, entered)\nreturn None'}, 'append_equipment_total_digits_fields': {'signature': 'memory: EquipmentMenuMemory, *, entry_frame: CommandFrame | None=None', 'returns': 'EquipmentMenuFields', 'flow': 'return _equipment_complete_projection(memory, entry_frame, 79690)'}, 'append_equipment_total_digits_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\ndestination = memory.state.read(4294964066, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 27, 16, True, True)\nif bool(frame.status_word & 4):\n    value = memory.state.read(4294954926, 4)\n    frame = _command_load_fields(memory, frame, 0, value, 32)\nelse:\n    value = memory.state.read(4294964196, 4)\n    frame = _command_load_fields(memory, frame, 0, value, 32)\nframe = _command_load_fields(memory, frame, 1, 50054, 16)\nframe = _command_load_fields(memory, frame, 2, 49153, 16)\nframe = frame.with_address(6, 4294962956)\nframe = _command_call_fields(memory, frame, 75530, 79730)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50980, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(1, 4294962956)\nframe = _command_load_fields(memory, frame, 0, 2, 16)\nwhile True:\n    value = memory.state.read(u32(frame.addresses[1]), 4)\n    frame = frame.with_address(1, frame.addresses[1] + 4)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), value, 32)\n    frame = frame.with_address(0, frame.addresses[0] + 4)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 16, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'append_recruitment_dialog_frame': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 77930)\nactual = append_recruitment_dialog_frame_frame_fields(memory, entered)\nreturn None'}, 'append_recruitment_dialog_frame_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50324, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 12, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 15, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50580, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50452, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 49181, 16)\nframe = _command_load_fields(memory, frame, 1, 3, 16)\nframe = _command_call_fields(memory, frame, 78198, 78008)\nframe = _command_load_fields(memory, frame, 0, 49157, 16)\nframe = _command_load_fields(memory, frame, 1, 1, 16)\nframe = _command_call_fields(memory, frame, 78198, 78020)\nframe = _command_load_fields(memory, frame, 0, 6, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 49153, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(34))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50708, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 12, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 15, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50964, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50836, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50050, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 49161, 16)\nframe = _command_load_fields(memory, frame, 1, 3, 16)\nframe = _command_call_fields(memory, frame, 78198, 78122)\nframe = _command_load_fields(memory, frame, 0, 8, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 49153, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 52098, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(34))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 51092, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 12, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54145, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 56192, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 238, 16, False, False)\nmemory.state.write(4294963994, 2, result)\ntested = memory.state.read(4294964132, 1)\nframe = _command_bit_fields(memory, frame, tested, 0 % 8)\nmemory.state.write(4294964132, 1, tested | 1 << 0 % 8)\nreturn frame'}, 'append_recruitment_input_digits': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 78364)\nactual = append_recruitment_input_digits_frame_fields(memory, entered)\nreturn None'}, 'append_recruitment_input_digits_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nvalue = memory.state.read(4294964196, 4)\nframe = _command_load_fields(memory, frame, 0, value, 32)\nframe = _command_load_fields(memory, frame, 1, 50054, 16)\nframe = _command_load_fields(memory, frame, 2, 0, 16)\nframe = frame.with_address(6, 4294962944)\nframe = _command_call_fields(memory, frame, 75530, 78384)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50596, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(1, 4294962944)\nframe = _command_load_fields(memory, frame, 0, 0, 16)\nframe = _command_load_fields(memory, frame, 1, 5, 16)\nwhile True:\n    value = memory.state.read(u32(frame.addresses[1]), 2)\n    frame = frame.with_address(1, frame.addresses[1] + 2)\n    frame = _command_load_fields(memory, frame, 2, value, 16)\n    if not not frame.status_word & 4:\n        source = memory.state.read(4294964122, 2)\n        frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, source, 16, True, True)\n        if not frame.status_word & 1:\n            frame = _command_load_fields(memory, frame, 2, 50054, 16)\n        else:\n            frame = _command_load_fields(memory, frame, 2, 49153, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[2] & 65535, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)\n    frame = frame.with_data(0, result, 16)\n    frame, repeat = _command_dbra_fields(frame, 1)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 16, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'append_recruitment_paired_tiles_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': "frame = memory.enter(frame)\nreturn _command_numbered_pair_fields(memory, frame, 'recruitment_equipment')"}, 'append_recruitment_total_digits': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 78448)\nactual = append_recruitment_total_digits_frame_fields(memory, entered)\nreturn None'}, 'append_recruitment_total_digits_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nvalue = memory.state.read(4294964126, 4)\nframe = _command_load_fields(memory, frame, 0, value, 32)\nframe = _command_load_fields(memory, frame, 1, 50054, 16)\nframe = _command_load_fields(memory, frame, 2, 49153, 16)\nframe = frame.with_address(6, 4294962956)\nframe = _command_call_fields(memory, frame, 75530, 78470)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50980, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(1, 4294962956)\nframe = _command_load_fields(memory, frame, 0, 2, 16)\nwhile True:\n    value = memory.state.read(u32(frame.addresses[1]), 4)\n    frame = frame.with_address(1, frame.addresses[1] + 4)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), value, 32)\n    frame = frame.with_address(0, frame.addresses[0] + 4)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 16, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'append_training_amount_cursor': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 81834)\nactual = append_training_amount_cursor_frame_fields(memory, entered)\nreturn None'}, 'append_training_amount_cursor_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nvalue = memory.state.read(4294964738, 2)\nframe = _command_load_fields(memory, frame, 0, value, 16)\nresult = frame.data[0] & 65535 & 48\nframe = _command_load_fields(memory, frame, 0, result, 16)\nif not not frame.status_word & 4:\n    tested = memory.state.read(4294964001, 1)\n    frame = _command_bit_fields(memory, frame, tested, 3 % 8)\n    if not not frame.status_word & 4:\n        frame = frame.with_address(0, u32(81858 + 26))\n        frame = _command_load_fields(memory, frame, 0, 88, 16)\n        value = memory.state.read(4294964122, 2)\n        frame = _command_load_fields(memory, frame, 1, value, 16)\n        frame = _command_shift_fields(memory, frame, 1, 3, 16, False)\n        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 168, 16, False, False)\n        frame = frame.with_data(1, result, 16)\n        frame = _command_load_fields(memory, frame, 2, 0, 16)\n        frame = _command_call_fields(memory, frame, 44040, 81882)\nreturn frame'}, 'append_training_cost_digits': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 81772)\nactual = append_training_cost_digits_frame_fields(memory, entered)\nreturn None'}, 'append_training_cost_digits_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nvalue = memory.state.read(4294964154, 4)\nframe = _command_load_fields(memory, frame, 0, value, 32)\nframe = _command_load_fields(memory, frame, 1, 50054, 16)\nframe = _command_load_fields(memory, frame, 2, 49153, 16)\nframe = frame.with_address(6, 4294955776)\nframe = _command_call_fields(memory, frame, 75530, 81802)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50860, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = frame.with_address(1, 4294955776)\nframe = _command_load_fields(memory, frame, 0, 5, 16)\nwhile True:\n    value = memory.state.read(u32(frame.addresses[1]), 2)\n    frame = frame.with_address(1, frame.addresses[1] + 2)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), value, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 16, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'clear_candidate_dialog_rows': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 81022)\nactual = clear_candidate_dialog_rows_frame_fields(memory, entered)\nreturn None'}, 'clear_candidate_dialog_rows_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 180), 8, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 160), 8, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 140), 8, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 120), 8, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 100), 8, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 80), 8, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 60), 8, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 40), 8, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 8, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 180), 51360, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 160), 51232, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 140), 51104, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 120), 50976, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 100), 50848, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 80), 50720, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 60), 50592, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 40), 50464, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50336, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50208, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 7, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 180), 32768, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 160), 32768, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 140), 32768, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 120), 32768, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 100), 32768, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 80), 32768, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 60), 32768, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 40), 32768, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 32768, 16)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 32768, 16)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 180), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 200, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'clear_equipment_dialog_rows': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 79166)\nactual = clear_equipment_dialog_rows_frame_fields(memory, entered)\nreturn None'}, 'clear_equipment_dialog_rows_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294955264)\nvalue = memory.state.read(4294963994, 2)\nframe = frame.with_address(0, frame.addresses[0] + s16(value))\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 204), 15, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 170), 15, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 136), 15, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 102), 15, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 68), 15, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 15, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 204), 51092, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 170), 50964, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 136), 50836, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 102), 50708, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 68), 50580, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50452, 16)\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50324, 16)\nframe = frame.with_address(0, frame.addresses[0] + 2)\nframe = _command_load_fields(memory, frame, 0, 14, 16)\nwhile True:\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 204), 0, 16, True)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 170), 0, 16, True)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 136), 0, 16, True)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 102), 0, 16, True)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 68), 0, 16, True)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 0, 16, True)\n    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame, repeat = _command_dbra_fields(frame, 0)\n    if repeat:\n        continue\n    break\nframe = _command_store_fields(memory, frame, u32(frame.addresses[0] + 204), 0, 16, True)\ndestination = memory.state.read(4294963994, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 238, 16, False, False)\nmemory.state.write(4294963994, 2, result)\nreturn frame'}, 'prepare_player_recruitment_capacity': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'Word', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 78216)\nactual = prepare_player_recruitment_capacity_frame_fields(memory, entered)\nreturn actual.data[1] & 65535'}, 'prepare_player_recruitment_capacity_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _command_store_fields(memory, frame, 4294964196, 0, 32, True)\nframe = _command_store_fields(memory, frame, 4294964126, 0, 32, True)\nframe = _command_store_fields(memory, frame, 4294964122, 3, 16)\nvalue = memory.state.read(4294964068, 2)\nframe = _command_load_fields(memory, frame, 0, value, 16)\nframe = _command_shift_fields(memory, frame, 0, 2, 16, False)\nframe = frame.with_address(0, 4294959100)\nvalue = memory.state.read(u32(frame.addresses[0] + s16(frame.data[0] & 65535)), 4)\nframe = _command_store_fields(memory, frame, 4294964200, value, 32)\nvalue = memory.state.read(4294964200, 4)\nframe = _command_load_fields(memory, frame, 2, value, 32)\nframe = _command_quotient_fields(memory, frame, 2, 100, 78250)\nframe = frame.with_address(1, 4294959420)\nvalue = memory.state.read(u32(frame.addresses[1] + s16(frame.data[0] & 65535)), 4)\nframe = _command_load_fields(memory, frame, 3, value, 32)\nframe = _command_load_fields(memory, frame, 4, frame.data[3], 32)\nframe = _command_product_fields(memory, frame, 3, 10)\nvalue = frame.data[4]\nframe = _command_load_fields(memory, frame, 4, (value & 65535) << 16 | value >> 16, 32)\nframe = _command_product_fields(memory, frame, 4, 10)\nvalue = frame.data[4]\nframe = _command_load_fields(memory, frame, 4, (value & 65535) << 16 | value >> 16, 32)\nframe, result = _command_binary_fields(memory, frame, frame.data[3], frame.data[4], 32, False, False)\nframe = frame.with_data(3, result, 32)\nframe = frame.with_address(1, 4294961012)\nframe = _command_load_fields(memory, frame, 4, 100000, 32)\nsource = memory.state.read(u32(frame.addresses[1] + s16(frame.data[0] & 65535)), 4)\nframe, result = _command_binary_fields(memory, frame, frame.data[4], source, 32, True, False)\nframe = frame.with_data(4, result, 32)\nframe = _command_quotient_fields(memory, frame, 4, 100, 78292)\nresult = frame.data[4] & 65535\nframe = _command_load_fields(memory, frame, 4, result, 32)\nframe, result = _command_binary_fields(memory, frame, frame.data[4], frame.data[3], 32, True, True)\nif not not frame.status_word & 1:\n    frame = _command_load_fields(memory, frame, 3, frame.data[4], 32)\nresult = frame.data[2] & 65535\nframe = _command_load_fields(memory, frame, 2, result, 32)\nframe, result = _command_binary_fields(memory, frame, frame.data[2], frame.data[3], 32, True, True)\nif not bool(frame.status_word & 5):\n    frame = _command_load_fields(memory, frame, 2, frame.data[3] & 65535, 16)\n    frame = _command_product_fields(memory, frame, 3, 100)\n    frame = _command_store_fields(memory, frame, 4294964200, frame.data[3], 32)\nframe = _command_load_fields(memory, frame, 1, 3, 16)\nframe, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 10, 16, True, True)\nif not bool(frame.status_word & 1):\n    frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, True, False)\n    frame = frame.with_data(1, result, 16)\n    frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 100, 16, True, True)\n    if not bool(frame.status_word & 1):\n        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, True, False)\n        frame = frame.with_data(1, result, 16)\n        frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 1000, 16, True, True)\n        if not bool(frame.status_word & 1):\n            frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, True, False)\n            frame = frame.with_data(1, result, 16)\nframe = _command_store_fields(memory, frame, 4294964204, frame.data[1] & 65535, 16)\nreturn frame'}, 'prepare_selected_training_cost_steps': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'Long', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 81398)\nactual = prepare_selected_training_cost_steps_frame_fields(memory, entered)\nreturn actual.data[0]'}, 'prepare_selected_training_cost_steps_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294964480)\nframe = frame.with_address(1, 4294952960)\nframe = _command_load_fields(memory, frame, 0, 0, 32)\nwhile True:\n    value = memory.state.read(u32(frame.addresses[0]), 2)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame = _command_load_fields(memory, frame, 1, value, 16)\n    if bool(frame.status_word & 8):\n        break\n    frame = _command_bit_fields(memory, frame, frame.data[1], 14 % 32)\n    if bool(frame.status_word & 4):\n        continue\n    frame = _command_shift_fields(memory, frame, 1, 2, 16, False)\n    source = memory.state.read(u32(frame.addresses[1] + s16(frame.data[1] & 65535)), 4)\n    frame, result = _command_binary_fields(memory, frame, frame.data[0], source, 32, False, False)\n    frame = frame.with_data(0, result, 32)\n    frame, result = _command_binary_fields(memory, frame, frame.data[0], 100, 32, False, False)\n    frame = frame.with_data(0, result, 32)\n    continue\nframe = _command_quotient_fields(memory, frame, 0, 100, 81434)\nif not not frame.status_word & 4:\n    frame = _command_load_fields(memory, frame, 0, 1, 16)\nresult = frame.data[0] & 65535\nframe = _command_load_fields(memory, frame, 0, result, 32)\nframe = _command_store_fields(memory, frame, 4294965070, frame.data[0], 32)\nframe = _command_product_fields(memory, frame, 0, 10)\nframe = _command_store_fields(memory, frame, 4294965074, frame.data[0], 32)\nframe = _command_product_fields(memory, frame, 0, 10)\nframe = _command_store_fields(memory, frame, 4294965078, frame.data[0], 32)\nreturn frame'}, 'prepare_selected_training_origin_and_speed': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'Word', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 81892)\nactual = prepare_selected_training_origin_and_speed_frame_fields(memory, entered)\nreturn actual.data[0] & 65535'}, 'prepare_selected_training_origin_and_speed_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = frame.with_address(0, 4294964480)\nframe = frame.with_address(1, 4294951936)\nframe = _command_load_fields(memory, frame, 0, 0, 32)\nframe = _command_load_fields(memory, frame, 1, 0, 16)\nvalue = memory.state.read(4294964068, 2)\nframe = _command_load_fields(memory, frame, 2, value, 16)\nframe = _command_shift_fields(memory, frame, 2, 2, 16, False)\nframe = frame.with_address(5, 871110)\nvalue = memory.state.read(u32(frame.addresses[5] + 2 + s16(frame.data[2] & 65535)), 2)\nframe = _command_load_fields(memory, frame, 3, value, 16)\nresult = frame.data[3] & 65535 & 65520\nframe = _command_load_fields(memory, frame, 3, result, 16)\nframe = _command_store_fields(memory, frame, 16726050, frame.data[3] & 65535, 16)\nframe = _command_shift_fields(memory, frame, 3, 4, 16, False)\nresult = frame.data[3] & 65535 & 65280\nframe = _command_load_fields(memory, frame, 3, result, 16)\nvalue = memory.state.read(u32(frame.addresses[5] + s16(frame.data[2] & 65535)), 2)\nframe = _command_load_fields(memory, frame, 4, value, 16)\nresult = frame.data[4] & 65535 & 65520\nframe = _command_load_fields(memory, frame, 4, result, 16)\nframe = _command_store_fields(memory, frame, 16726052, frame.data[4] & 65535, 16)\nframe = _command_shift_fields(memory, frame, 4, 4, 16, True)\nresult = frame.data[4] & 65535 | frame.data[3] & 65535\nframe = _command_load_fields(memory, frame, 4, result, 16)\nframe = _command_store_fields(memory, frame, 16726056, frame.data[4] & 65535, 16)\nwhile True:\n    value = memory.state.read(u32(frame.addresses[0]), 2)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame = _command_load_fields(memory, frame, 2, value, 16)\n    if bool(frame.status_word & 8):\n        break\n    frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 16384, 16, True, True)\n    if bool(frame.status_word & 1):\n        continue\n    frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, False, False)\n    frame = frame.with_data(1, result, 16)\n    result = frame.data[2] & 65535 & 255\n    frame = _command_load_fields(memory, frame, 2, result, 16)\n    frame = _command_load_fields(memory, frame, 3, 0, 16)\n    value = memory.state.read(u32(frame.addresses[1] + s16(frame.data[2] & 65535)), 1)\n    frame = _command_load_fields(memory, frame, 3, value, 8)\n    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, frame.data[3] & 65535, 16, False, False)\n    frame = frame.with_data(0, result, 16)\n    continue\nframe = _command_store_fields(memory, frame, 16726058, frame.data[1] & 65535, 16)\nframe = _command_quotient_fields(memory, frame, 0, frame.data[1] & 65535, 81992)\nframe = _command_store_fields(memory, frame, 4294964850, frame.data[0] & 65535, 16)\nreturn frame'}, 'update_equipment_category': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 80774)\nactual = update_equipment_category_frame_fields(memory, entered)\nreturn None'}, 'update_equipment_category_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nvalue = memory.state.read(4294964738, 1)\nframe = _command_load_fields(memory, frame, 0, value, 8)\nresult = frame.data[0] & 65535 & 3\nframe = _command_load_fields(memory, frame, 0, result, 16)\nif bool(frame.status_word & 4):\n    frame = _command_store_fields(memory, frame, 4294964744, 1, 16)\nelse:\n    destination = memory.state.read(4294964744, 2)\n    frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\n    memory.state.write(4294964744, 2, result)\n    if not not frame.status_word & 4:\n        frame = _command_store_fields(memory, frame, 4294964744, 12, 16)\n        frame = _command_bit_fields(memory, frame, frame.data[0], 1 % 32)\n        if not frame.status_word & 4:\n            destination = memory.state.read(4294964872, 2)\n            frame, result = _command_binary_fields(memory, frame, destination, 2, 16, True, True)\n            if bool(frame.status_word & 1):\n                destination = memory.state.read(4294964872, 2)\n                frame, result = _command_binary_fields(memory, frame, destination, 1, 16, False, False)\n                memory.state.write(4294964872, 2, result)\n            else:\n                frame = _command_store_fields(memory, frame, 4294964872, 0, 16, True)\n        else:\n            value = memory.state.read(4294964872, 2)\n            frame = _command_test_fields(memory, frame, value, 16)\n            if not frame.status_word & 4:\n                destination = memory.state.read(4294964872, 2)\n                frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\n                memory.state.write(4294964872, 2, result)\n            else:\n                frame = _command_store_fields(memory, frame, 4294964872, 2, 16)\nreturn frame'}, 'update_recruitment_input_cursor': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 77656)\nactual = update_recruitment_input_cursor_frame_fields(memory, entered)\nreturn None'}, 'update_recruitment_input_cursor_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\ndestination = memory.state.read(4294964124, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 24, 16, True, True)\nif not bool(frame.status_word & 1):\n    frame = _command_store_fields(memory, frame, 4294964124, 24, 16)\ndestination = memory.state.read(4294964124, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\nmemory.state.write(4294964124, 2, result)\ndestination = memory.state.read(4294964124, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 12, 16, True, True)\nif not bool(frame.status_word & 1):\n    frame = frame.with_address(0, u32(77684 + -1252))\n    frame = _command_load_fields(memory, frame, 0, 80, 16)\n    value = memory.state.read(4294964122, 2)\n    frame = _command_load_fields(memory, frame, 1, value, 16)\n    frame = _command_shift_fields(memory, frame, 1, 3, 16, False)\n    frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 248, 16, False, False)\n    frame = frame.with_data(1, result, 16)\n    frame = _command_load_fields(memory, frame, 2, 0, 16)\n    frame = _command_call_fields(memory, frame, 44040, 77708)\nreturn frame'}, 'update_recruitment_total_cursor': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 77876)\nactual = update_recruitment_total_cursor_frame_fields(memory, entered)\nreturn None'}, 'update_recruitment_total_cursor_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\ndestination = memory.state.read(4294964124, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 24, 16, True, True)\nif not bool(frame.status_word & 1):\n    frame = _command_store_fields(memory, frame, 4294964124, 24, 16)\ndestination = memory.state.read(4294964124, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\nmemory.state.write(4294964124, 2, result)\ndestination = memory.state.read(4294964124, 2)\nframe, result = _command_binary_fields(memory, frame, destination, 12, 16, True, True)\nif not bool(frame.status_word & 1):\n    frame = frame.with_address(0, u32(77904 + -1472))\n    frame = _command_load_fields(memory, frame, 0, 104, 16)\n    value = memory.state.read(4294964122, 2)\n    frame = _command_load_fields(memory, frame, 1, value, 16)\n    frame = _command_shift_fields(memory, frame, 1, 3, 16, False)\n    frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 248, 16, False, False)\n    frame = frame.with_data(1, result, 16)\n    frame = _command_load_fields(memory, frame, 2, 0, 16)\n    frame = _command_call_fields(memory, frame, 44040, 77928)\nreturn frame'}, 'update_selected_training_amount': {'signature': 'state: GameState, *, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _command_legacy_entry(state, entry_frame, 81554)\nactual = update_selected_training_amount_frame_fields(memory, entered)\nreturn None'}, 'update_selected_training_amount_frame_fields': {'signature': 'memory: CommandMenuMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nvalue = memory.state.read(4294964738, 1)\nframe = _command_load_fields(memory, frame, 0, value, 8)\nresult = frame.data[0] & 65535 & 12\nframe = _command_load_fields(memory, frame, 0, result, 16)\nif bool(frame.status_word & 4):\n    value = memory.state.read(4294964738, 1)\n    frame = _command_load_fields(memory, frame, 0, value, 8)\n    result = frame.data[0] & 255 & 3\n    frame = _command_load_fields(memory, frame, 0, result, 8)\n    if bool(frame.status_word & 4):\n        frame = _command_store_fields(memory, frame, 4294964744, 1, 16)\n    else:\n        destination = memory.state.read(4294964744, 2)\n        frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\n        memory.state.write(4294964744, 2, result)\n        if not not frame.status_word & 4:\n            frame = _command_store_fields(memory, frame, 4294964744, 12, 16)\n            frame = _command_load_fields(memory, frame, 1, 2, 16)\n            source = memory.state.read(4294964122, 2)\n            frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, source, 16, True, False)\n            frame = frame.with_data(1, result, 16)\n            frame = _command_shift_fields(memory, frame, 1, 2, 16, False)\n            frame = frame.with_address(0, 4294965070)\n            value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[1] & 65535)), 4)\n            frame = _command_load_fields(memory, frame, 2, value, 32)\n            frame = _command_shift_fields(memory, frame, 1, 1, 16, True)\n            value = memory.state.read(u32(81686 + 80 + s16(frame.data[1] & 65535)), 2)\n            frame = _command_load_fields(memory, frame, 4, value, 16)\n            frame = _command_bit_fields(memory, frame, frame.data[0], 1 % 32)\n            if not frame.status_word & 4:\n                value = memory.state.read(4294964154, 4)\n                frame = _command_load_fields(memory, frame, 3, value, 32)\n                frame, result = _command_binary_fields(memory, frame, frame.data[3], frame.data[2], 32, True, False)\n                frame = frame.with_data(3, result, 32)\n                if not bool(frame.status_word & 1):\n                    frame = _command_store_fields(memory, frame, 4294964154, frame.data[3], 32)\n                    destination = memory.state.read(4294964848, 2)\n                    frame, result = _command_binary_fields(memory, frame, destination, frame.data[4] & 65535, 16, True, False)\n                    memory.state.write(4294964848, 2, result)\n            else:\n                value = memory.state.read(4294964154, 4)\n                frame = _command_load_fields(memory, frame, 3, value, 32)\n                frame, result = _command_binary_fields(memory, frame, frame.data[3], frame.data[2], 32, False, False)\n                frame = frame.with_data(3, result, 32)\n                source = memory.state.read(4294964216, 4)\n                frame, result = _command_binary_fields(memory, frame, frame.data[3], source, 32, True, True)\n                if not not frame.status_word & 5:\n                    value = memory.state.read(4294964848, 2)\n                    frame = _command_load_fields(memory, frame, 5, value, 16)\n                    frame, result = _command_binary_fields(memory, frame, frame.data[5] & 65535, frame.data[4] & 65535, 16, False, False)\n                    frame = frame.with_data(5, result, 16)\n                    frame, result = _command_binary_fields(memory, frame, frame.data[5] & 65535, 1000, 16, True, True)\n                    if not not frame.status_word & 1:\n                        frame = _command_store_fields(memory, frame, 4294964154, frame.data[3], 32)\n                        frame = _command_store_fields(memory, frame, 4294964848, frame.data[5] & 65535, 16)\nelse:\n    destination = memory.state.read(4294964744, 2)\n    frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\n    memory.state.write(4294964744, 2, result)\n    if not not frame.status_word & 4:\n        frame = _command_store_fields(memory, frame, 4294964744, 12, 16)\n        frame = _command_bit_fields(memory, frame, frame.data[0], 3 % 32)\n        if not frame.status_word & 4:\n            destination = memory.state.read(4294964122, 2)\n            frame, result = _command_binary_fields(memory, frame, destination, 2, 16, True, True)\n            if not not frame.status_word & 1:\n                destination = memory.state.read(4294964122, 2)\n                frame, result = _command_binary_fields(memory, frame, destination, 1, 16, False, False)\n                memory.state.write(4294964122, 2, result)\n                value = memory.state.read(4294964738, 1)\n                frame = _command_load_fields(memory, frame, 0, value, 8)\n                result = frame.data[0] & 255 & 3\n                frame = _command_load_fields(memory, frame, 0, result, 8)\n                if bool(frame.status_word & 4):\n                    frame = _command_store_fields(memory, frame, 4294964744, 1, 16)\n                else:\n                    destination = memory.state.read(4294964744, 2)\n                    frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\n                    memory.state.write(4294964744, 2, result)\n                    if not not frame.status_word & 4:\n                        frame = _command_store_fields(memory, frame, 4294964744, 12, 16)\n                        frame = _command_load_fields(memory, frame, 1, 2, 16)\n                        source = memory.state.read(4294964122, 2)\n                        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, source, 16, True, False)\n                        frame = frame.with_data(1, result, 16)\n                        frame = _command_shift_fields(memory, frame, 1, 2, 16, False)\n                        frame = frame.with_address(0, 4294965070)\n                        value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[1] & 65535)), 4)\n                        frame = _command_load_fields(memory, frame, 2, value, 32)\n                        frame = _command_shift_fields(memory, frame, 1, 1, 16, True)\n                        value = memory.state.read(u32(81686 + 80 + s16(frame.data[1] & 65535)), 2)\n                        frame = _command_load_fields(memory, frame, 4, value, 16)\n                        frame = _command_bit_fields(memory, frame, frame.data[0], 1 % 32)\n                        if not frame.status_word & 4:\n                            value = memory.state.read(4294964154, 4)\n                            frame = _command_load_fields(memory, frame, 3, value, 32)\n                            frame, result = _command_binary_fields(memory, frame, frame.data[3], frame.data[2], 32, True, False)\n                            frame = frame.with_data(3, result, 32)\n                            if not bool(frame.status_word & 1):\n                                frame = _command_store_fields(memory, frame, 4294964154, frame.data[3], 32)\n                                destination = memory.state.read(4294964848, 2)\n                                frame, result = _command_binary_fields(memory, frame, destination, frame.data[4] & 65535, 16, True, False)\n                                memory.state.write(4294964848, 2, result)\n                        else:\n                            value = memory.state.read(4294964154, 4)\n                            frame = _command_load_fields(memory, frame, 3, value, 32)\n                            frame, result = _command_binary_fields(memory, frame, frame.data[3], frame.data[2], 32, False, False)\n                            frame = frame.with_data(3, result, 32)\n                            source = memory.state.read(4294964216, 4)\n                            frame, result = _command_binary_fields(memory, frame, frame.data[3], source, 32, True, True)\n                            if not not frame.status_word & 5:\n                                value = memory.state.read(4294964848, 2)\n                                frame = _command_load_fields(memory, frame, 5, value, 16)\n                                frame, result = _command_binary_fields(memory, frame, frame.data[5] & 65535, frame.data[4] & 65535, 16, False, False)\n                                frame = frame.with_data(5, result, 16)\n                                frame, result = _command_binary_fields(memory, frame, frame.data[5] & 65535, 1000, 16, True, True)\n                                if not not frame.status_word & 1:\n                                    frame = _command_store_fields(memory, frame, 4294964154, frame.data[3], 32)\n                                    frame = _command_store_fields(memory, frame, 4294964848, frame.data[5] & 65535, 16)\n        else:\n            value = memory.state.read(4294964122, 2)\n            frame = _command_test_fields(memory, frame, value, 16)\n            if not bool(frame.status_word & 4):\n                frame = _command_load_fields(memory, frame, 0, 1, 16)\n                source = memory.state.read(4294964122, 2)\n                frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, source, 16, True, False)\n                frame = frame.with_data(0, result, 16)\n                frame = _command_shift_fields(memory, frame, 0, 2, 16, False)\n                frame = frame.with_address(0, 4294965074)\n                value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[0] & 65535)), 4)\n                frame = _command_load_fields(memory, frame, 0, value, 32)\n                source = memory.state.read(4294964216, 4)\n                frame, result = _command_binary_fields(memory, frame, frame.data[0], source, 32, True, True)\n                if not not frame.status_word & 5:\n                    destination = memory.state.read(4294964122, 2)\n                    frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)\n                    memory.state.write(4294964122, 2, result)\nreturn frame'}})
APPROVED.setdefault('contexts_command_fields',set()).update(['CommandFrame', 'CommandMenuMemory', '_command_binary_fields', '_command_bit_fields', '_command_call_fields', '_command_dbra_fields', '_command_decimal_place_fields', '_command_decimal_transaction_fields', '_command_load_fields', '_command_numbered_pair_fields', '_command_product_fields', '_command_quotient_fields', '_command_shift_fields', '_command_store_fields', '_command_tail_fields', '_command_test_fields'])
APPROVED.setdefault('domain',set()).update({'s16'})
APPROVED.setdefault('business_budget',set()).update({'_command_legacy_entry'})
