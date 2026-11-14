"""Draft restricted semantic frontend and ordinary GNU target lowering.

Generated development draft; Python rules remain in business_display.
Only these explicit structural forms and declared literal rules are admitted.
Not a general Python compiler or a complete CPU equivalence proof.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import DISPLAY_BINDINGS

APPROVED = {'contexts_numeric': {'DecimalMemory'}, 'business_budget': {'_six_place_decimal_fields', 'append_six_place_decimal_value'},
 'business_reuse': {'collect_blocked_cargo', 'terrain_cell_query'},
 'contexts_display': {'MarkerResult',
                      'RouteCost',
                      'SpriteAppendResult',
                      'TileRun',
                      'WorldSelection'},
 'domain': {'CarryOutcome',
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
            'low8',
            'negative_byte',
            'negative_word',
            'read_packed_long',
            'replace_word',
            's16',
            'store_packed_long_reverse',
            'u16',
            'u32',
            'u8',
            'uint'}}

DECLARATIONS = {'append_live_command_string_words': {'signature': 'state: GameState, source: Table, x: Word, y: '
                                                   'Word, attributes: Word=0, reset_scroll: '
                                                   'bool=True',
                                      'returns': 'SpriteAppendResult',
                                      'flow': 'checked_state(state)\n'
                                              'checked_table(source, state)\n'
                                              'uint(x, 16)\n'
                                              'uint(y, 16)\n'
                                              'uint(attributes, 16)\n'
                                              'if type(reset_scroll) is not bool:\n'
                                              "    raise ValueError('explicit reset choice "
                                              "required')\n"
                                              'if reset_scroll:\n'
                                              "    state.set_scalar('scroll_x', 0)\n"
                                              "    state.set_scalar('scroll_y', 0)\n"
                                              "state.set_scalar('clip_min_x', 112)\n"
                                              "state.set_scalar('clip_max_x', 352)\n"
                                              "state.set_scalar('clip_min_y', 112)\n"
                                              "state.set_scalar('clip_max_y', 448)\n"
                                              'records = source.cursor()\n'
                                              "if state.scalar('sprite_count') >= 80:\n"
                                              '    return SpriteAppendResult(records, attributes)\n'
                                              'attributes &= 63488\n'
                                              "origin_x = u16(x - state.scalar('scroll_x') + 128)\n"
                                              "origin_y = u16(y - state.scalar('scroll_y') + 128)\n"
                                              'output = '
                                              "state.sprite_entries.cursor(u16(state.scalar('sprite_count') "
                                              '<< 3))\n'
                                              'while True:\n'
                                              '    coordinate_x = records.word()\n'
                                              '    if coordinate_x == 32768:\n'
                                              '        return SpriteAppendResult(records, '
                                              'attributes)\n'
                                              '    if attributes & 4096:\n'
                                              '        size = records.word(0, 4)\n'
                                              '        coordinate_x = u16(-u16(coordinate_x + 8))\n'
                                              '    coordinate_x = u16(coordinate_x + origin_x)\n'
                                              "    if coordinate_x >= state.scalar('clip_min_x') "
                                              "and coordinate_x < state.scalar('clip_max_x'):\n"
                                              '        output.set_word(0, coordinate_x)\n'
                                              '        packed = u32(records.word(0, 4) << 4)\n'
                                              '        coordinate_y = u16(s16(low16(packed)) >> '
                                              '4)\n'
                                              '        size = packed >> 16\n'
                                              '        if attributes & 2048:\n'
                                              '            coordinate_y = u16(-u16(coordinate_y + '
                                              '((size & 12) << 1) + 8))\n'
                                              '        coordinate_y = u16(coordinate_y + '
                                              'origin_y)\n'
                                              '        if coordinate_y >= '
                                              "state.scalar('clip_min_y') and coordinate_y < "
                                              "state.scalar('clip_max_y'):\n"
                                              '            output.set_word(0, coordinate_y, 6)\n'
                                              '            output.set_word(0, u16(size << 8), 2)\n'
                                              "            if state.scalar('sprite_count') != 0:\n"
                                              '                output.set_byte(0, '
                                              "state.scalar('sprite_count'), -5)\n"
                                              "            state.set_scalar('sprite_count', "
                                              "u8(state.scalar('sprite_count') + 1))\n"
                                              '            output.set_word(0, records.word(0, 2) ^ '
                                              'attributes, 4)\n'
                                              '            output = output.advance(8)\n'
                                              '    records = records.advance(6)\n'
                                              "    if state.scalar('sprite_count') >= 80:\n"
                                              '        return SpriteAppendResult(records, '
                                              'attributes)'},
 'append_route_selection_pair': {'signature': 'state: GameState',
                                 'returns': 'None',
                                 'flow': 'checked_state(state)\n'
                                         'destination = state.route_candidate_list.cursor()\n'
                                         'while not negative_word(destination.next_word()):\n'
                                         '    pass\n'
                                         'destination.set_word(0, '
                                         "state.scalar('route_first_member'), -2)\n"
                                         "destination.put_word(state.scalar('route_second_member'))\n"
                                         'destination.set_word(0, 65535, 2)'},
 'append_route_cursor_sprite': {'signature': 'state: GameState',
                                'returns': 'None',
                                'flow': 'checked_state(state)\n'
                                        "if state.scalar('ui_gate_flags') & 4:\n"
                                        '    return\n'
                                        "x = state.scalar('route_row_coordinate')\n"
                                        "y = state.scalar('route_column_coordinate')\n"
                                        "state.set_scalar('scroll_x', "
                                        "state.scalar('map_scroll_x'))\n"
                                        "state.set_scalar('scroll_y', "
                                        "state.scalar('map_scroll_y'))\n"
                                        'append_live_command_string_words(state, '
                                        'state.route_cursor_shape, x, y, 0, False)'},
 'step_world_route_cursor': {'signature': 'state: GameState',
                             'returns': 'None',
                             'flow': 'checked_state(state)\n'
                                     "controls = state.scalar('held_controls_WORD')\n"
                                     'direction = 0\n'
                                     'if controls & 1:\n'
                                     "    row = state.scalar('route_row_coordinate')\n"
                                     '    if row == 0:\n'
                                     '        return\n'
                                     '    row = u16(row - 16)\n'
                                     "    column = state.scalar('route_column_coordinate')\n"
                                     '    direction = 1\n'
                                     'elif controls & 8:\n'
                                     "    if state.scalar('route_column_coordinate') >= 1104:\n"
                                     '        return\n'
                                     "    row = state.scalar('route_row_coordinate')\n"
                                     "    column = u16(state.scalar('route_column_coordinate') + "
                                     '16)\n'
                                     '    direction = 2\n'
                                     'elif controls & 2:\n'
                                     "    if state.scalar('route_row_coordinate') >= 1136:\n"
                                     '        return\n'
                                     "    row = u16(state.scalar('route_row_coordinate') + 16)\n"
                                     "    column = state.scalar('route_column_coordinate')\n"
                                     '    direction = 3\n'
                                     'elif controls & 4:\n'
                                     "    column = state.scalar('route_column_coordinate')\n"
                                     '    if column == 0:\n'
                                     '        return\n'
                                     '    column = u16(column - 16)\n'
                                     "    row = state.scalar('route_row_coordinate')\n"
                                     '    direction = 4\n'
                                     'else:\n'
                                     '    return\n'
                                     'result = query_route_move_cost(state, row, column)\n'
                                     'if negative_word(result.cost):\n'
                                     '    return\n'
                                     "budget = state.scalar('remaining_move_budget')\n"
                                     'if budget < result.cost:\n'
                                     '    return\n'
                                     "state.set_scalar('remaining_move_budget', u16(budget - "
                                     'result.cost))\n'
                                     'if direction == 1 or direction == 3:\n'
                                     "    state.set_scalar('route_row_coordinate', result.row)\n"
                                     'else:\n'
                                     "    state.set_scalar('route_column_coordinate', "
                                     'result.column)\n'
                                     "state.route_direction_bytes.set_byte(state.scalar('route_step_count'), "
                                     'direction)\n'
                                     "state.set_scalar('route_step_count', "
                                     "u16(state.scalar('route_step_count') + 1))"},
 'query_scaled_route_terrain': {'signature': 'state: GameState, row: Word, column: Word',
                                'returns': 'RouteCost',
                                'flow': 'checked_state(state)\n'
                                        'uint(row, 16)\n'
                                        'uint(column, 16)\n'
                                        'terrain, cost = terrain_cell_query(state, row >> 4, '
                                        'column >> 4)\n'
                                        'return RouteCost(u16(row >> 4 << 4), u16(column >> 4 << '
                                        '4), cost)'},
 'query_route_move_cost': {'signature': 'state: GameState, row: Word, column: Word',
                           'returns': 'RouteCost',
                           'flow': 'checked_state(state)\n'
                                   'uint(row, 16)\n'
                                   'uint(column, 16)\n'
                                   'return query_scaled_route_terrain(state, row, column)'},
 'append_candidate_member_panel': {'signature': 'state: GameState',
                                   'returns': 'Cursor',
                                   'flow': 'checked_state(state)\n'
                                           'output = '
                                           "state.command_queue.cursor(state.scalar('command_queue_offset'))\n"
                                           'for tile in (6, 49954, 50048, 50049, 50049, 50049, '
                                           '50049, 52096):\n'
                                           '    output.append_word(tile)\n'
                                           'members = state.selection_members.cursor()\n'
                                           'row_tile = 50082\n'
                                           'while True:\n'
                                           '    output.set_word(0, 6, 16)\n'
                                           '    output.append_word(6)\n'
                                           '    output.put_word(row_tile)\n'
                                           '    row_tile = u16(row_tile + 128)\n'
                                           '    output.set_word(0, row_tile, 16)\n'
                                           '    row_tile = u16(row_tile + 128)\n'
                                           '    output = output.advance(2)\n'
                                           '    output.set_word(0, 50050, 16)\n'
                                           '    output.append_word(50050)\n'
                                           '    tile = u16((members.next_byte() << 3) + 49177)\n'
                                           '    output = append_short_paired_tiles(state, output, '
                                           'tile, 3).destination\n'
                                           '    output.set_word(0, 52098, 16)\n'
                                           '    output.append_word(52098)\n'
                                           '    output = output.advance(16)\n'
                                           "    state.set_scalar('command_queue_offset', "
                                           "u16(state.scalar('command_queue_offset') + 16))\n"
                                           '    if negative_byte(members.byte()):\n'
                                           '        break\n'
                                           '    output.append_word(6)\n'
                                           '    output.append_word(row_tile)\n'
                                           '    row_tile = u16(row_tile + 128)\n'
                                           '    output.append_word(50050)\n'
                                           '    for index in range(4):\n'
                                           '        output.append_word(49153)\n'
                                           '    output.append_word(52098)\n'
                                           "    state.set_scalar('command_queue_offset', "
                                           "u16(state.scalar('command_queue_offset') + 16))\n"
                                           'for tile in (6, row_tile, 54144, 54145, 54145, 54145, '
                                           '54145, 56192):\n'
                                           '    output.append_word(tile)\n'
                                           'output.put_word(0)\n'
                                           "state.set_scalar('command_queue_offset', "
                                           "u16(state.scalar('command_queue_offset') + 32))\n"
                                           'return output'},
 'append_short_paired_tiles': {'signature': 'state: GameState, destination: Cursor, tile: Long, '
                                            'counter: Long',
                               'returns': 'TileRun',
                               'flow': 'checked_state(state)\n'
                                       'checked_cursor(destination, state)\n'
                                       'uint(tile, 32)\n'
                                       'uint(counter, 32)\n'
                                       'for index in descending_inclusive(low16(counter)):\n'
                                       '    destination.put_word(low16(tile))\n'
                                       '    tile = replace_word(tile, u16(tile + 1))\n'
                                       '    destination.set_word(0, low16(tile), 16)\n'
                                       '    tile = replace_word(tile, u16(tile + 1))\n'
                                       '    destination = destination.advance(2)\n'
                                       'return TileRun(destination, tile, replace_word(counter, '
                                       '65535))'},
 'append_selected_group_panel': {'signature': 'state: GameState',
                                 'returns': 'Cursor',
                                 'flow': 'checked_state(state)\n'
                                         'selected = '
                                         "state.table(state.scalar('active_descriptor'))\n"
                                         'amount = read_packed_long(selected, 5)\n'
                                         'append_six_place_decimal_value(state, amount, 50054, '
                                         '49153, state.decimal_scratch.cursor())\n'
                                         'amount = read_packed_long(selected, 9)\n'
                                         'append_six_place_decimal_value(state, amount, 50054, '
                                         '49153, state.decimal_scratch.cursor(12))\n'
                                         'output = '
                                         "state.command_queue.cursor(state.scalar('command_queue_offset'))\n"
                                         'for tile in (15, 50050, 50048):\n'
                                         '    output.append_word(tile)\n'
                                         'for index in range(13):\n'
                                         '    output.append_word(50049)\n'
                                         'output.append_word(52096)\n'
                                         'output.set_word(0, 15, 34)\n'
                                         'output.append_word(15)\n'
                                         'output.set_word(0, 50306, 34)\n'
                                         'output.append_word(50178)\n'
                                         'output.set_word(0, 50050, 34)\n'
                                         'output.append_word(50050)\n'
                                         'output = append_wide_paired_tiles(state, output, 49225, '
                                         '5).destination\n'
                                         'output.set_word(0, 49153, 34)\n'
                                         'output.append_word(49153)\n'
                                         'digits = state.decimal_scratch.cursor()\n'
                                         'for index in range(6):\n'
                                         '    output.set_word(0, digits.next_word(), 34)\n'
                                         '    output.append_word(49153)\n'
                                         'output.set_word(0, 52098, 34)\n'
                                         'output.append_word(52098)\n'
                                         'output = output.advance(34)\n'
                                         'output.set_word(0, 15, 34)\n'
                                         'output.append_word(15)\n'
                                         'output.set_word(0, 50690, 34)\n'
                                         'output.append_word(50562)\n'
                                         'output.set_word(0, 50050, 34)\n'
                                         'output.append_word(50050)\n'
                                         'output = append_wide_paired_tiles(state, output, 49237, '
                                         '3).destination\n'
                                         'for index in range(3):\n'
                                         '    output.set_word(0, 49153, 34)\n'
                                         '    output.append_word(49153)\n'
                                         'for index in range(6):\n'
                                         '    output.set_word(0, digits.next_word(), 34)\n'
                                         '    output.append_word(49153)\n'
                                         'output.set_word(0, 52098, 34)\n'
                                         'output.append_word(52098)\n'
                                         'output = output.advance(34)\n'
                                         'output.set_word(0, 15, 34)\n'
                                         'output.append_word(15)\n'
                                         'output.set_word(0, 51074, 34)\n'
                                         'output.append_word(50946)\n'
                                         'output.set_word(0, 50050, 34)\n'
                                         'output.append_word(50050)\n'
                                         'output = append_wide_paired_tiles(state, output, 49245, '
                                         '5).destination\n'
                                         'for index in range(5):\n'
                                         '    output.set_word(0, 49153, 34)\n'
                                         '    output.append_word(49153)\n'
                                         'selected = '
                                         "state.table(state.scalar('active_descriptor'))\n"
                                         'count = selected.byte() & 15\n'
                                         'tens_tile = 49153\n'
                                         'if count >= 10:\n'
                                         '    tens_tile = 50055\n'
                                         '    count = u16(count - 10)\n'
                                         'output.set_word(0, tens_tile, 34)\n'
                                         'output.append_word(49153)\n'
                                         'output.set_word(0, u16(count + 50054), 34)\n'
                                         'output.append_word(49153)\n'
                                         'output.set_word(0, 52098, 34)\n'
                                         'output.append_word(52098)\n'
                                         'output = output.advance(34)\n'
                                         'output.set_word(0, 15, 68)\n'
                                         'output.set_word(0, 15, 34)\n'
                                         'output.append_word(15)\n'
                                         'output.set_word(0, 51202, 68)\n'
                                         'output.set_word(0, 50818, 34)\n'
                                         'output.append_word(50434)\n'
                                         'output.set_word(0, 54144, 68)\n'
                                         'output.set_word(0, 50050, 34)\n'
                                         'output.append_word(50050)\n'
                                         'for index in range(13):\n'
                                         '    output.set_word(0, 54145, 68)\n'
                                         '    output.set_word(0, 49153, 34)\n'
                                         '    output.append_word(49153)\n'
                                         'output.set_word(0, 56192, 68)\n'
                                         'output.set_word(0, 52098, 34)\n'
                                         'output.append_word(52098)\n'
                                         'output.set_word(0, 0, 68)\n'
                                         "state.set_scalar('command_queue_offset', "
                                         "u16(state.scalar('command_queue_offset') + 340))\n"
                                         'return output'},
 'append_wide_paired_tiles': {'signature': 'state: GameState, destination: Cursor, tile: Long, '
                                           'counter: Long',
                              'returns': 'TileRun',
                              'flow': 'checked_state(state)\n'
                                      'checked_cursor(destination, state)\n'
                                      'uint(tile, 32)\n'
                                      'uint(counter, 32)\n'
                                      'for index in descending_inclusive(low16(counter)):\n'
                                      '    destination.put_word(low16(tile))\n'
                                      '    tile = replace_word(tile, u16(tile + 1))\n'
                                      '    destination.set_word(0, low16(tile), 34)\n'
                                      '    tile = replace_word(tile, u16(tile + 1))\n'
                                      '    destination = destination.advance(2)\n'
                                      'return TileRun(destination, tile, replace_word(counter, '
                                      '65535))'},
 'step_candidate_selection_cursor': {'signature': 'state: GameState',
                                     'returns': 'None',
                                     'flow': 'checked_state(state)\n'
                                             "controls = state.scalar('held_controls_BYTE') & 3\n"
                                             'if controls == 0:\n'
                                             "    state.set_scalar('repeat_timer', 1)\n"
                                             '    return\n'
                                             "delay = u16(state.scalar('repeat_timer') - 1)\n"
                                             "state.set_scalar('repeat_timer', delay)\n"
                                             'if delay != 0:\n'
                                             '    return\n'
                                             "state.set_scalar('repeat_timer', 12)\n"
                                             'if controls & 2:\n'
                                             '    index = '
                                             "u16(state.scalar('selected_candidate_index') + 1)\n"
                                             '    if '
                                             'negative_byte(state.selection_members.byte(index)):\n'
                                             '        index = 0\n'
                                             "    state.set_scalar('selected_candidate_index', "
                                             'index)\n'
                                             "elif state.scalar('selected_candidate_index') != 0:\n"
                                             "    state.set_scalar('selected_candidate_index', "
                                             "u16(state.scalar('selected_candidate_index') - 1))\n"
                                             'else:\n'
                                             '    index = 0\n'
                                             '    while not '
                                             'negative_byte(state.selection_members.byte(index, '
                                             '1)):\n'
                                             '        index = u16(index + 1)\n'
                                             "    state.set_scalar('selected_candidate_index', "
                                             'index)'},
 'append_candidate_selection_sprite': {'signature': 'state: GameState',
                                       'returns': 'None',
                                       'flow': 'checked_state(state)\n'
                                               "if state.scalar('pressed_controls_BYTE') & 32:\n"
                                               '    return\n'
                                               "controls = state.scalar('held_controls_BYTE') & 3\n"
                                               "if controls == 0 and state.scalar('ui_gate_flags') "
                                               '& 8:\n'
                                               '    return\n'
                                               "x = u16(state.scalar('selected_candidate_index') * "
                                               '24 + 48)\n'
                                               'append_live_command_string_words(state, '
                                               'state.candidate_cursor_shape, x, 136)'},
 'collect_group_members_below_capacity': {'signature': 'state: GameState',
                                          'returns': 'Word',
                                          'flow': 'checked_state(state)\n'
                                                  'selected = '
                                                  "state.table(state.scalar('active_descriptor'))\n"
                                                  'count = u16((selected.byte() & 15) - 1)\n'
                                                  'members = selected.cursor(13)\n'
                                                  'output = state.candidate_roster.cursor()\n'
                                                  'found = 0\n'
                                                  'for index in descending_inclusive(count):\n'
                                                  '    member_offset = u16(members.next_byte() << '
                                                  '1)\n'
                                                  '    capacity = '
                                                  'state.officer_capacity.word(member_offset)\n'
                                                  '    if capacity != '
                                                  'state.officer_readiness.word(member_offset):\n'
                                                  '        output.append_word(member_offset >> 1)\n'
                                                  '        found = u16(found + 1)\n'
                                                  'output.put_word(65535)\n'
                                                  "state.set_scalar('candidate_member_count', "
                                                  'found)\n'
                                                  'return found'},
 'clear_world_group_selection_marks': {'signature': 'state: GameState',
                                       'returns': 'None',
                                       'flow': 'checked_state(state)\n'
                                               "state.set_scalar('saved_scroll_x', "
                                               "state.scalar('map_scroll_x'))\n"
                                               "state.set_scalar('saved_scroll_y', "
                                               "state.scalar('map_scroll_y'))\n"
                                               'group = state.group_records\n'
                                               'while True:\n'
                                               '    header = group.byte() & 239\n'
                                               '    group.set_byte(0, header)\n'
                                               '    count = header & 15\n'
                                               '    if count == 0:\n'
                                               '        return\n'
                                               '    group = group.at(count, 13)'},
 'select_world_group_or_city_at_marker': {'signature': 'state: GameState, marker: Word',
                                          'returns': 'WorldSelection',
                                          'flow': 'checked_state(state)\n'
                                                  'uint(marker, 16)\n'
                                                  'result = find_world_marker_record(state, '
                                                  'marker)\n'
                                                  'if result.outcome.carry:\n'
                                                  "    state.set_scalar('world_aux_flag', 0)\n"
                                                  '    scene = result.record.byte()\n'
                                                  "    state.set_scalar('selected_scene', scene)\n"
                                                  '    if scene != 50:\n'
                                                  '        offset = u16(scene * 4)\n'
                                                  '        y = '
                                                  'state.city_world_positions.word(offset)\n'
                                                  '        x = '
                                                  'state.city_world_positions.word(offset, 2)\n'
                                                  '        x = 0 if x < 104 else u16(x - 104)\n'
                                                  '        y = 0 if y < 152 else u16(y - 152)\n'
                                                  "        state.set_scalar('active_descriptor', "
                                                  '0)\n'
                                                  '        return WorldSelection(x, y, None)\n'
                                                  'group = state.group_records\n'
                                                  'while group.byte(0, 13) != low8(marker):\n'
                                                  '    group = group.at(group.byte() & 15, 13)\n'
                                                  "state.set_scalar('active_descriptor', "
                                                  'group.base)\n'
                                                  'x = u16(group.byte(0, 1) << 4)\n'
                                                  "state.set_scalar('selected_world_x', x)\n"
                                                  'x = 0 if x < 104 else u16(x - 104)\n'
                                                  'y = u16(group.byte(0, 2) << 4)\n'
                                                  "state.set_scalar('selected_world_y', y)\n"
                                                  'y = 0 if y < 152 else u16(y - 152)\n'
                                                  'return WorldSelection(x, y, group)'},
 'find_world_marker_record': {'signature': 'state: GameState, marker: Word', 'returns': 'MarkerResult', 'flow': "checked_state(state)\nuint(marker, 16)\nrecords = state.world_command_records.cursor(1)\nwhile records.next_byte() != low8(marker):\n    while records.next_byte() != 0:\n        pass\n    records = records.advance(1)\nrecords = records.advance(1)\nif negative_byte(records.next_byte()):\n    return MarkerResult(records, state.carry_result(1))\nstate.set_scalar('selected_scene', 65535)\nreturn MarkerResult(records, state.carry_result(0))"},
 'test_selected_group_enemy_contacts': {'signature': 'state: GameState, stride_carrier: Word',
                                        'returns': 'CarryOutcome',
                                        'flow': 'checked_state(state)\n'
                                                'uint(stride_carrier, 16)\n'
                                                "if state.scalar('selected_scene') != 50:\n"
                                                '    return state.carry_result(0)\n'
                                                'selected = '
                                                "state.table(state.scalar('active_descriptor'))\n"
                                                'count = '
                                                'encode_live_group_coordinate_packet(state, stride_carrier)\n'
                                                'if count != 0:\n'
                                                '    return state.carry_result(0)\n'
                                                "state.set_scalar('adjacent_count_tick', "
                                                "u16(state.scalar('adjacent_count_tick') + 2))\n"
                                                'return state.carry_result(1)'},
 'set_pending_group_move_position': {'signature': 'state: GameState, direction: Word',
                                     'returns': 'WorldSelection',
                                     'flow': 'checked_state(state)\n'
                                             'uint(direction, 16)\n'
                                             "x = state.scalar('selected_world_x')\n"
                                             "y = state.scalar('selected_world_y')\n"
                                             'if direction == 1:\n'
                                             '    x = u16(x - 16)\n'
                                             'elif direction == 2:\n'
                                             '    y = u16(y + 16)\n'
                                             '    group = '
                                             "state.table(state.scalar('active_descriptor'))\n"
                                             '    group.set_byte(0, group.byte() | 128)\n'
                                             'elif direction == 3:\n'
                                             '    x = u16(x + 16)\n'
                                             'else:\n'
                                             '    y = u16(y - 16)\n'
                                             '    group = '
                                             "state.table(state.scalar('active_descriptor'))\n"
                                             '    group.set_byte(0, group.byte() & 127)\n'
                                             "state.set_scalar('pending_world_x', x)\n"
                                             "state.set_scalar('pending_world_y', y)\n"
                                             'return WorldSelection(x, y, None)'},
 'merge_compatible_world_groups': {'signature': 'state: GameState',
                                   'returns': 'Table',
                                   'flow': 'checked_state(state)\n'
                                           'selected = '
                                           "state.table(state.scalar('active_descriptor'))\n"
                                           'x = selected.byte(0, 1)\n'
                                           'y = selected.byte(0, 2)\n'
                                           'owner = selected.byte(0, 4)\n'
                                           'group = state.group_records\n'
                                           'while True:\n'
                                           '    header = group.byte()\n'
                                           '    if not header & 64:\n'
                                           '        if header & 15 == 0:\n'
                                           '            break\n'
                                           '        if group.base != selected.base and '
                                           'group.byte(0, 1) == x and (group.byte(0, 2) == y) and '
                                           '(group.byte(0, 4) == owner):\n'
                                           '            if group.base < selected.base:\n'
                                           '                selected, group = (group, selected)\n'
                                           '            merge_world_group_records(state, selected, '
                                           'group)\n'
                                           '            break\n'
                                           '    group = group.at(header & 15, 13)\n'
                                           "state.set_scalar('active_descriptor', selected.base)\n"
                                           'return selected'},
 'merge_world_group_records': {'signature': 'state: GameState, destination: Table, source: Table',
                               'returns': 'Table',
                               'flow': 'checked_state(state)\n'
                                       'checked_table(destination, state)\n'
                                       'checked_table(source, state)\n'
                                       'source_count = source.byte() & 15\n'
                                       'destination_count = destination.byte() & 15\n'
                                       'destination.set_byte(0, u8(destination_count + '
                                       'source_count))\n'
                                       'append_at = destination.cursor(u16(destination_count + '
                                       '13))\n'
                                       'total = u32(read_packed_long(destination, 5) + '
                                       'read_packed_long(source, 5))\n'
                                       'if total > 999999:\n'
                                       '    total = 999999\n'
                                       'store_packed_long_reverse(destination, 5, total)\n'
                                       'total = u32(read_packed_long(destination, 9) + '
                                       'read_packed_long(source, 9))\n'
                                       'if total > 999999:\n'
                                       '    total = 999999\n'
                                       'store_packed_long_reverse(destination, 9, total)\n'
                                       'scratch = state.group_member_scratch.cursor()\n'
                                       'index = 0\n'
                                       'while True:\n'
                                       '    scratch.append_byte(source.byte(index, 13))\n'
                                       '    index = u16(index + 1)\n'
                                       '    if index >= source_count:\n'
                                       '        break\n'
                                       'following = source.cursor(u16(source_count + 13))\n'
                                       'shifted = source.cursor(source_count)\n'
                                       'moving = source.cursor()\n'
                                       'if append_at.base != moving.base:\n'
                                       '    while True:\n'
                                       '        value = moving.previous_byte()\n'
                                       '        shifted = shifted.advance(-1)\n'
                                       '        shifted.set_byte(0, value)\n'
                                       '        if append_at.base >= moving.base:\n'
                                       '            break\n'
                                       'scratch = state.group_member_scratch.cursor()\n'
                                       'for index in descending_inclusive(u16(source_count - 1)):\n'
                                       '    append_at.append_byte(scratch.next_byte())\n'
                                       'while True:\n'
                                       '    count = following.byte() & 15\n'
                                       '    if count == 0:\n'
                                       '        break\n'
                                       '    for index in descending_inclusive(u16(count + 12)):\n'
                                       '        shifted.append_byte(following.next_byte())\n'
                                       'shifted.set_byte(0, 0)\n'
                                       'members = destination.cursor(13)\n'
                                       'count = destination.byte() & 15\n'
                                       'speed_sum = 0\n'
                                       'for index in descending_inclusive(u16(count - 1)):\n'
                                       '    member = members.next_byte()\n'
                                       '    speed_sum = u16(speed_sum + '
                                       'state.officer_march_speed.byte(member))\n'
                                       'average = divu_retained(speed_sum, count)\n'
                                       'destination.set_byte(0, low8(average), 3)\n'
                                       'return destination',
                               'slots': {999999: ('merged_resource_cap', 0, 2147483647)}},
 'test_pending_group_destination': {'signature': 'state: GameState, owner_carrier: Word=0', 'returns': 'CarryOutcome', 'flow': "checked_state(state)\nuint(owner_carrier, 16)\nx = state.scalar('pending_world_x') >> 4\ny = state.scalar('pending_world_y') >> 4\nselected = state.table(state.scalar('active_descriptor'))\nselected_count = selected.byte() & 15\nowner = owner_carrier & 65280 | selected.byte(0, 4)\ngroup = state.group_records\nwhile True:\n    count = group.byte() & 15\n    if count == 0:\n        break\n    if group.byte(0, 1) == low8(x) and group.byte(0, 2) == low8(y):\n        if group.byte(0, 4) != low8(owner):\n            return state.carry_result(1)\n        command = state.world_command_records.at(state.scalar('world_command_offset'))\n        if command.byte(0, 1) != 0:\n            return state.carry_result(0)\n        if u16(count + selected_count) > 10:\n            return state.carry_result(1)\n        return state.carry_result(0)\n    group = group.at(u16(count + 13))\ncities = state.city_locations\nfor city in descending_inclusive(39):\n    if cities.byte() != 0 and cities.byte(0, 1) == low8(x) and (cities.byte(0, 2) == low8(y)):\n        relationship = state.force_relationship_bits.word(u16(owner * 2))\n        city_owner = state.city_owner_bytes.byte(city)\n        if low8(owner) == city_owner or relationship & 1 << (s16(city_owner if city_owner < 128 else city_owner | 65280) & 31):\n            return state.carry_result(1)\n        collect_blocked_cargo(state, cities)\n        return state.carry_result(1)\n    cities = cities.advance(-4)\nreturn state.carry_result(0)"},
 'encode_live_group_coordinate_packet': {'signature': 'state: GameState, stride_carrier: Word',
                                         'returns': 'Word',
                                         'flow': 'checked_state(state)\n'
                                                 'uint(stride_carrier, 16)\n'
                                                 'selected = '
                                                 "state.table(state.scalar('active_descriptor'))\n"
                                                 'coordinate = u16(selected.byte(0, 1) << 8 | '
                                                 'selected.byte(0, 2))\n'
                                                 'owner = selected.byte(0, 4)\n'
                                                 'neighbours = (u16(coordinate - 256), '
                                                 'u16(coordinate + 1), u16(coordinate + 256), '
                                                 'u16(coordinate - 1))\n'
                                                 'state.adjacent_group_offsets.set_long(0, '
                                                 '4294967295)\n'
                                                 'state.adjacent_group_offsets.set_long(0, '
                                                 '4294967295, 4)\n'
                                                 'offset = 0\n'
                                                 'while True:\n'
                                                 '    header = state.group_records.byte(offset)\n'
                                                 '    count = header & 15\n'
                                                 '    if count == 0:\n'
                                                 '        break\n'
                                                 '    if not state.group_records.byte(offset) & '
                                                 '32:\n'
                                                 '        if state.group_records.byte(offset, 4) '
                                                 '!= owner:\n'
                                                 '            other_coordinate = '
                                                 'u16(state.group_records.byte(offset, 1) << 8 | '
                                                 'state.group_records.byte(offset, 2))\n'
                                                 '            if other_coordinate == '
                                                 'neighbours[0]:\n'
                                                 '                '
                                                 'state.adjacent_group_offsets.set_word(0, '
                                                 'offset)\n'
                                                 '            elif other_coordinate == '
                                                 'neighbours[1]:\n'
                                                 '                '
                                                 'state.adjacent_group_offsets.set_word(0, offset, '
                                                 '2)\n'
                                                 '            elif other_coordinate == '
                                                 'neighbours[2]:\n'
                                                 '                '
                                                 'state.adjacent_group_offsets.set_word(0, offset, '
                                                 '4)\n'
                                                 '            elif other_coordinate == '
                                                 'neighbours[3]:\n'
                                                 '                '
                                                 'state.adjacent_group_offsets.set_word(0, offset, '
                                                 '6)\n'
                                                 '    offset = u16(offset + 13 + ((stride_carrier & 0xFF00) | count))\n'
                                                 'entries = state.adjacent_group_offsets.cursor()\n'
                                                 'found = 0\n'
                                                 'for index in range(4):\n'
                                                 '    if not negative_word(entries.next_word()):\n'
                                                 '        found = u16(found + 1)\n'
                                                 'return found'}}

def _lower_append_live_command_string_words(e, rules):
    e.label('player_pc_00ac08')
    e.ins('clr.w', '0xf60a:w', 4)
    e.label('player_pc_00ac0c')
    e.ins('clr.w', '0xf60e:w', 4)
    e.label('player_pc_00ac10')
    e.ins('move.w', '#0x70,0xf302:w', 6)
    e.label('player_pc_00ac16')
    e.ins('move.w', '#0x160,0xf304:w', 6)
    e.label('player_pc_00ac1c')
    e.ins('move.w', '#0x70,0xf306:w', 6)
    e.label('player_pc_00ac22')
    e.ins('move.w', '#0x1c0,0xf308:w', 6)
    e.label('player_pc_00ac28')
    e.ins('movem.l', '%d3-%d7/%a1,-(%a7)', 4)
    e.label('player_pc_00ac2c')
    e.ins('cmpi.b', '#0x50,0xf300:w', 6)
    e.label('player_pc_00ac32')
    e.ins('bcc.w', 'player_pc_00ad00', 4)
    e.label('player_pc_00ac36')
    e.ins('andi.w', '#0xf800,%d2', 4)
    e.label('player_pc_00ac3a')
    e.ins('move.w', '%d0,%d3', 2)
    e.label('player_pc_00ac3c')
    e.ins('sub.w', '0xf60a:w,%d3', 4)
    e.label('player_pc_00ac40')
    e.ins('addi.w', '#0x80,%d3', 4)
    e.label('player_pc_00ac44')
    e.ins('move.w', '%d1,%d4', 2)
    e.label('player_pc_00ac46')
    e.ins('sub.w', '0xf60e:w,%d4', 4)
    e.label('player_pc_00ac4a')
    e.ins('addi.w', '#0x80,%d4', 4)
    e.label('player_pc_00ac4e')
    e.ins('clr.w', '%d5', 2)
    e.label('player_pc_00ac50')
    e.ins('move.b', '0xf300:w,%d5', 4)
    e.label('player_pc_00ac54')
    e.ins('lsl.w', '#0x3,%d5', 2)
    e.label('player_pc_00ac56')
    e.ins('lea.l', '0xf800:w,%a1', 4)
    e.label('player_pc_00ac5a')
    e.ins('lea.l', '(%a1, %d5.w),%a1', 4)
    e.label('player_pc_00ac5e')
    e.ins('move.w', '(%a0),%d5', 2)
    e.label('player_pc_00ac60')
    e.ins('cmpi.w', '#0x8000,%d5', 4)
    e.label('player_pc_00ac64')
    e.ins('beq.w', 'player_pc_00ad00', 4)
    e.label('player_pc_00ac68')
    e.ins('btst.l', '#0xc,%d2', 4)
    e.label('player_pc_00ac6c')
    e.ins('beq.b', 'player_pc_00ac8a', 2)
    e.label('player_pc_00ac6e')
    e.ins('move.w', '0x4(%a0),%d7', 4)
    e.label('player_pc_00ac72')
    e.ins('andi.l', '#0xffff,%d7', 6)
    e.label('player_pc_00ac78')
    e.ins('lsl.w', '#0x4,%d7', 2)
    e.label('player_pc_00ac7a')
    e.ins('swap', '%d7', 2)
    e.label('player_pc_00ac7c')
    e.ins('andi.w', '#0x3,%d7', 4)
    e.label('player_pc_00ac80')
    e.ins('lsl.w', '#0x3,%d7', 2)
    e.label('player_pc_00ac82')
    e.ins('addi.w', '#0x8,%d7', 4)
    e.label('player_pc_00ac86')
    e.ins('add.w', '%d7,%d5', 2)
    e.label('player_pc_00ac88')
    e.ins('neg.w', '%d5', 2)
    e.label('player_pc_00ac8a')
    e.ins('add.w', '%d3,%d5', 2)
    e.label('player_pc_00ac8c')
    e.ins('cmp.w', '0xf302:w,%d5', 4)
    e.label('player_pc_00ac90')
    e.ins('bcs.b', 'player_pc_00acf4', 2)
    e.label('player_pc_00ac92')
    e.ins('cmp.w', '0xf304:w,%d5', 4)
    e.label('player_pc_00ac96')
    e.ins('bcc.b', 'player_pc_00acf4', 2)
    e.label('player_pc_00ac98')
    e.ins('move.w', '%d5,(%a1)', 2)
    e.label('player_pc_00ac9a')
    e.ins('moveq', '#0,%d5', 2)
    e.label('player_pc_00ac9c')
    e.ins('move.w', '0x4(%a0),%d5', 4)
    e.label('player_pc_00aca0')
    e.ins('lsl.l', '#0x4,%d5', 2)
    e.label('player_pc_00aca2')
    e.ins('asr.w', '#0x4,%d5', 2)
    e.label('player_pc_00aca4')
    e.ins('move.l', '%d5,%d6', 2)
    e.label('player_pc_00aca6')
    e.ins('btst.l', '#0xb,%d2', 4)
    e.label('player_pc_00acaa')
    e.ins('beq.b', 'player_pc_00acbe', 2)
    e.label('player_pc_00acac')
    e.ins('move.l', '%d6,%d7', 2)
    e.label('player_pc_00acae')
    e.ins('swap', '%d7', 2)
    e.label('player_pc_00acb0')
    e.ins('andi.w', '#0xc,%d7', 4)
    e.label('player_pc_00acb4')
    e.ins('lsl.w', '#0x1,%d7', 2)
    e.label('player_pc_00acb6')
    e.ins('addi.w', '#0x8,%d7', 4)
    e.label('player_pc_00acba')
    e.ins('add.w', '%d7,%d5', 2)
    e.label('player_pc_00acbc')
    e.ins('neg.w', '%d5', 2)
    e.label('player_pc_00acbe')
    e.ins('add.w', '%d4,%d5', 2)
    e.label('player_pc_00acc0')
    e.ins('cmp.w', '0xf306:w,%d5', 4)
    e.label('player_pc_00acc4')
    e.ins('bcs.b', 'player_pc_00acf4', 2)
    e.label('player_pc_00acc6')
    e.ins('cmp.w', '0xf308:w,%d5', 4)
    e.label('player_pc_00acca')
    e.ins('bcc.b', 'player_pc_00acf4', 2)
    e.label('player_pc_00accc')
    e.ins('move.w', '%d5,0x6(%a1)', 4)
    e.label('player_pc_00acd0')
    e.ins('swap', '%d6', 2)
    e.label('player_pc_00acd2')
    e.ins('lsl.w', '#0x8,%d6', 2)
    e.label('player_pc_00acd4')
    e.ins('move.w', '%d6,0x2(%a1)', 4)
    e.label('player_pc_00acd8')
    e.ins('tst.b', '0xf300:w', 4)
    e.label('player_pc_00acdc')
    e.ins('beq.b', 'player_pc_00ace4', 2)
    e.label('player_pc_00acde')
    e.ins('move.b', '0xf300:w,-0x5(%a1)', 6)
    e.label('player_pc_00ace4')
    e.ins('addq.b', '#0x1,0xf300:w', 4)
    e.label('player_pc_00ace8')
    e.ins('move.w', '0x2(%a0),%d5', 4)
    e.label('player_pc_00acec')
    e.ins('eor.w', '%d2,%d5', 2)
    e.label('player_pc_00acee')
    e.ins('move.w', '%d5,0x4(%a1)', 4)
    e.label('player_pc_00acf2')
    e.ins('addq.l', '#0x8,%a1', 2)
    e.label('player_pc_00acf4')
    e.ins('addq.l', '#0x6,%a0', 2)
    e.label('player_pc_00acf6')
    e.ins('cmpi.b', '#0x50,0xf300:w', 6)
    e.label('player_pc_00acfc')
    e.ins('bcs.w', 'player_pc_00ac5e', 4)
    e.label('player_pc_00ad00')
    e.ins('movem.l', '(%a7)+,%d3-%d7/%a1', 4)
    e.label('player_pc_00ad04')
    e.ins('rts', '', 2)

def _lower_append_route_selection_pair(e, rules):
    e.label('player_pc_014106')
    e.ins('lea.l', '0x9f00:w,%a0', 4)
    e.label('player_pc_01410a')
    e.ins('tst.w', '(%a0)+', 2)
    e.label('player_pc_01410c')
    e.ins('bpl.b', 'player_pc_01410a', 2)
    e.label('player_pc_01410e')
    e.ins('move.w', '0xf35e:w,-0x2(%a0)', 6)
    e.label('player_pc_014114')
    e.ins('move.w', '0xf360:w,(%a0)', 4)
    e.label('player_pc_014118')
    e.ins('move.w', '#0xffff,0x2(%a0)', 6)
    e.label('player_pc_01411e')
    e.ins('rts', '', 2)

def _lower_append_route_cursor_sprite(e, rules):
    e.label('player_pc_014120')
    e.ins('btst.b', '#0x2,0xf321:w', 6)
    e.label('player_pc_014126')
    e.ins('bne.b', 'player_pc_01414e', 2)
    e.label('player_pc_014128')
    e.ins('lea.l', '38(%pc),%a0', 4)
    e.label('player_pc_01412c')
    e.ins('nop', '', 2)
    e.label('player_pc_01412e')
    e.ins('move.w', '0xff3822:l,%d0', 6)
    e.label('player_pc_014134')
    e.ins('move.w', '0xff3824:l,%d1', 6)
    e.label('player_pc_01413a')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_01413c')
    e.ins('move.w', '0xf314:w,0xf60a:w', 6)
    e.label('player_pc_014142')
    e.ins('move.w', '0xf318:w,0xf60e:w', 6)
    e.label('player_pc_014148')
    e.ins('jsr', 'player_pc_00ac10:l', 6)
    e.label('player_pc_01414e')
    e.ins('rts', '', 2)

def _lower_step_world_route_cursor(e, rules):
    e.label('player_pc_01416a')
    e.ins('move.w', '0xf602:w,%d4', 4)
    e.label('player_pc_01416e')
    e.ins('btst.l', '#0x0,%d4', 4)
    e.label('player_pc_014172')
    e.ins('beq.b', 'player_pc_0141ae', 2)
    e.label('player_pc_014174')
    e.ins('move.w', '0xff3822:l,%d0', 6)
    e.label('player_pc_01417a')
    e.ins('beq.w', 'player_pc_014292', 4)
    e.label('player_pc_01417e')
    e.ins('subi.w', '#0x10,%d0', 4)
    e.label('player_pc_014182')
    e.ins('move.w', '0xff3824:l,%d1', 6)
    e.label('player_pc_014188')
    e.ins('bsr.w', 'player_pc_0142ca', 4)
    e.label('player_pc_01418c')
    e.ins('tst.w', '%d3', 2)
    e.label('player_pc_01418e')
    e.ins('bmi.w', 'player_pc_014292', 4)
    e.label('player_pc_014192')
    e.ins('move.w', '0xf674:w,%d4', 4)
    e.label('player_pc_014196')
    e.ins('sub.w', '%d3,%d4', 2)
    e.label('player_pc_014198')
    e.ins('bcs.w', 'player_pc_014292', 4)
    e.label('player_pc_01419c')
    e.ins('move.w', '%d4,0xf674:w', 4)
    e.label('player_pc_0141a0')
    e.ins('move.w', '%d0,0xff3822:l', 6)
    e.label('player_pc_0141a6')
    e.ins('move.w', '#0x1,%d1', 4)
    e.label('player_pc_0141aa')
    e.ins('bra.w', 'player_pc_01427c', 4)
    e.label('player_pc_0141ae')
    e.ins('btst.l', '#0x3,%d4', 4)
    e.label('player_pc_0141b2')
    e.ins('beq.b', 'player_pc_0141f6', 2)
    e.label('player_pc_0141b4')
    e.ins('cmpi.w', '#0x450,0xff3824:l', 8)
    e.label('player_pc_0141bc')
    e.ins('bcc.w', 'player_pc_014292', 4)
    e.label('player_pc_0141c0')
    e.ins('move.w', '0xff3822:l,%d0', 6)
    e.label('player_pc_0141c6')
    e.ins('move.w', '0xff3824:l,%d1', 6)
    e.label('player_pc_0141cc')
    e.ins('addi.w', '#0x10,%d1', 4)
    e.label('player_pc_0141d0')
    e.ins('bsr.w', 'player_pc_0142ca', 4)
    e.label('player_pc_0141d4')
    e.ins('tst.w', '%d3', 2)
    e.label('player_pc_0141d6')
    e.ins('bmi.w', 'player_pc_014292', 4)
    e.label('player_pc_0141da')
    e.ins('move.w', '0xf674:w,%d4', 4)
    e.label('player_pc_0141de')
    e.ins('sub.w', '%d3,%d4', 2)
    e.label('player_pc_0141e0')
    e.ins('bcs.w', 'player_pc_014292', 4)
    e.label('player_pc_0141e4')
    e.ins('move.w', '%d4,0xf674:w', 4)
    e.label('player_pc_0141e8')
    e.ins('move.w', '%d1,0xff3824:l', 6)
    e.label('player_pc_0141ee')
    e.ins('move.w', '#0x2,%d1', 4)
    e.label('player_pc_0141f2')
    e.ins('bra.w', 'player_pc_01427c', 4)
    e.label('player_pc_0141f6')
    e.ins('btst.l', '#0x1,%d4', 4)
    e.label('player_pc_0141fa')
    e.ins('beq.b', 'player_pc_01423e', 2)
    e.label('player_pc_0141fc')
    e.ins('cmpi.w', '#0x470,0xff3822:l', 8)
    e.label('player_pc_014204')
    e.ins('bcc.w', 'player_pc_014292', 4)
    e.label('player_pc_014208')
    e.ins('move.w', '0xff3822:l,%d0', 6)
    e.label('player_pc_01420e')
    e.ins('addi.w', '#0x10,%d0', 4)
    e.label('player_pc_014212')
    e.ins('move.w', '0xff3824:l,%d1', 6)
    e.label('player_pc_014218')
    e.ins('bsr.w', 'player_pc_0142ca', 4)
    e.label('player_pc_01421c')
    e.ins('tst.w', '%d3', 2)
    e.label('player_pc_01421e')
    e.ins('bmi.w', 'player_pc_014292', 4)
    e.label('player_pc_014222')
    e.ins('move.w', '0xf674:w,%d4', 4)
    e.label('player_pc_014226')
    e.ins('sub.w', '%d3,%d4', 2)
    e.label('player_pc_014228')
    e.ins('bcs.w', 'player_pc_014292', 4)
    e.label('player_pc_01422c')
    e.ins('move.w', '%d4,0xf674:w', 4)
    e.label('player_pc_014230')
    e.ins('move.w', '%d0,0xff3822:l', 6)
    e.label('player_pc_014236')
    e.ins('move.w', '#0x3,%d1', 4)
    e.label('player_pc_01423a')
    e.ins('bra.w', 'player_pc_01427c', 4)
    e.label('player_pc_01423e')
    e.ins('btst.l', '#0x2,%d4', 4)
    e.label('player_pc_014242')
    e.ins('beq.w', 'player_pc_014292', 4)
    e.label('player_pc_014246')
    e.ins('move.w', '0xff3824:l,%d1', 6)
    e.label('player_pc_01424c')
    e.ins('beq.w', 'player_pc_014292', 4)
    e.label('player_pc_014250')
    e.ins('subi.w', '#0x10,%d1', 4)
    e.label('player_pc_014254')
    e.ins('move.w', '0xff3822:l,%d0', 6)
    e.label('player_pc_01425a')
    e.ins('bsr.w', 'player_pc_0142ca', 4)
    e.label('player_pc_01425e')
    e.ins('tst.w', '%d3', 2)
    e.label('player_pc_014260')
    e.ins('bmi.w', 'player_pc_014292', 4)
    e.label('player_pc_014264')
    e.ins('move.w', '0xf674:w,%d4', 4)
    e.label('player_pc_014268')
    e.ins('sub.w', '%d3,%d4', 2)
    e.label('player_pc_01426a')
    e.ins('bcs.w', 'player_pc_014292', 4)
    e.label('player_pc_01426e')
    e.ins('move.w', '%d4,0xf674:w', 4)
    e.label('player_pc_014272')
    e.ins('move.w', '%d1,0xff3824:l', 6)
    e.label('player_pc_014278')
    e.ins('move.w', '#0x4,%d1', 4)
    e.label('player_pc_01427c')
    e.ins('lea.l', '0xff3800:l,%a0', 6)
    e.label('player_pc_014282')
    e.ins('move.w', '0xff3820:l,%d0', 6)
    e.label('player_pc_014288')
    e.ins('move.b', '%d1,(%a0, %d0.w)', 4)
    e.label('player_pc_01428c')
    e.ins('addq.w', '#0x1,0xff3820:l', 6)
    e.label('player_pc_014292')
    e.ins('rts', '', 2)

def _lower_query_scaled_route_terrain(e, rules):
    e.label('player_pc_014294')
    e.ins('lsr.w', '#0x4,%d0', 2)
    e.label('player_pc_014296')
    e.ins('lsr.w', '#0x4,%d1', 2)
    e.label('player_pc_014298')
    e.ins('bsr.w', 'player_pc_0142a2', 4)
    e.label('player_pc_01429c')
    e.ins('lsl.w', '#0x4,%d0', 2)
    e.label('player_pc_01429e')
    e.ins('lsl.w', '#0x4,%d1', 2)
    e.label('player_pc_0142a0')
    e.ins('rts', '', 2)

def _lower_query_route_move_cost(e, rules):
    e.label('player_pc_0142ca')
    e.ins('bsr.b', 'player_pc_014294', 2)
    e.label('player_pc_0142cc')
    e.ins('tst.w', '%d3', 2)
    e.label('player_pc_0142ce')
    e.ins('rts', '', 2)

def _lower_append_candidate_member_panel(e, rules):
    e.label('player_pc_014494')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_014498')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_01449c')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_0144a0')
    e.ins('move.w', '#0xc322,(%a0)+', 4)
    e.label('player_pc_0144a4')
    e.ins('move.w', '#0xc380,(%a0)+', 4)
    e.label('player_pc_0144a8')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_0144ac')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_0144b0')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_0144b4')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_0144b8')
    e.ins('move.w', '#0xcb80,(%a0)+', 4)
    e.label('player_pc_0144bc')
    e.ins('lea.l', '0xff3930:l,%a1', 6)
    e.label('player_pc_0144c2')
    e.ins('move.w', '#0xc3a2,%d2', 4)
    e.label('player_pc_0144c6')
    e.ins('move.w', '#0x6,0x10(%a0)', 6)
    e.label('player_pc_0144cc')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_0144d0')
    e.ins('move.w', '%d2,(%a0)', 2)
    e.label('player_pc_0144d2')
    e.ins('addi.w', '#0x80,%d2', 4)
    e.label('player_pc_0144d6')
    e.ins('move.w', '%d2,0x10(%a0)', 4)
    e.label('player_pc_0144da')
    e.ins('addi.w', '#0x80,%d2', 4)
    e.label('player_pc_0144de')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_0144e0')
    e.ins('move.w', '#0xc382,0x10(%a0)', 6)
    e.label('player_pc_0144e6')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_0144ea')
    e.ins('clr.w', '%d0', 2)
    e.label('player_pc_0144ec')
    e.ins('move.b', '(%a1)+,%d0', 2)
    e.label('player_pc_0144ee')
    e.ins('lsl.w', '#0x3,%d0', 2)
    e.label('player_pc_0144f0')
    e.ins('addi.w', '#0xc019,%d0', 4)
    e.label('player_pc_0144f4')
    e.ins('move.w', '#0x3,%d1', 4)
    e.label('player_pc_0144f8')
    e.ins('bsr.w', 'player_pc_014562', 4)
    e.label('player_pc_0144fc')
    e.ins('move.w', '#0xcb82,0x10(%a0)', 6)
    e.label('player_pc_014502')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_014506')
    e.ins('adda.w', '#0x10,%a0', 4)
    e.label('player_pc_01450a')
    e.ins('addi.w', '#0x10,0xf31a:w', 6)
    e.label('player_pc_014510')
    e.ins('tst.b', '(%a1)', 2)
    e.label('player_pc_014512')
    e.ins('bmi.b', 'player_pc_01453a', 2)
    e.label('player_pc_014514')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_014518')
    e.ins('move.w', '%d2,(%a0)+', 2)
    e.label('player_pc_01451a')
    e.ins('addi.w', '#0x80,%d2', 4)
    e.label('player_pc_01451e')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_014522')
    e.ins('move.w', '#0x3,%d0', 4)
    e.label('player_pc_014526')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_01452a')
    e.ins('dbra', '%d0,player_pc_014526', 4)
    e.label('player_pc_01452e')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_014532')
    e.ins('addi.w', '#0x10,0xf31a:w', 6)
    e.label('player_pc_014538')
    e.ins('bra.b', 'player_pc_0144c6', 2)
    e.label('player_pc_01453a')
    e.ins('move.w', '#0x6,(%a0)+', 4)
    e.label('player_pc_01453e')
    e.ins('move.w', '%d2,(%a0)+', 2)
    e.label('player_pc_014540')
    e.ins('move.w', '#0xd380,(%a0)+', 4)
    e.label('player_pc_014544')
    e.ins('move.w', '#0xd381,(%a0)+', 4)
    e.label('player_pc_014548')
    e.ins('move.w', '#0xd381,(%a0)+', 4)
    e.label('player_pc_01454c')
    e.ins('move.w', '#0xd381,(%a0)+', 4)
    e.label('player_pc_014550')
    e.ins('move.w', '#0xd381,(%a0)+', 4)
    e.label('player_pc_014554')
    e.ins('move.w', '#0xdb80,(%a0)+', 4)
    e.label('player_pc_014558')
    e.ins('clr.w', '(%a0)', 2)
    e.label('player_pc_01455a')
    e.ins('addi.w', '#0x20,0xf31a:w', 6)
    e.label('player_pc_014560')
    e.ins('rts', '', 2)

def _lower_append_short_paired_tiles(e, rules):
    e.label('player_pc_014562')
    e.ins('move.w', '%d0,(%a0)', 2)
    e.label('player_pc_014564')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_014566')
    e.ins('move.w', '%d0,0x10(%a0)', 4)
    e.label('player_pc_01456a')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_01456c')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_01456e')
    e.ins('dbra', '%d1,player_pc_014562', 4)
    e.label('player_pc_014572')
    e.ins('rts', '', 2)

def _lower_append_selected_group_panel(e, rules):
    e.label('player_pc_014574')
    e.ins('movea.l', '0xff382c:l,%a1', 6)
    e.label('player_pc_01457a')
    e.ins('move.b', '0x5(%a1),%d0', 4)
    e.label('player_pc_01457e')
    e.ins('lsl.w', '#0x8,%d0', 2)
    e.label('player_pc_014580')
    e.ins('move.b', '0x6(%a1),%d0', 4)
    e.label('player_pc_014584')
    e.ins('lsl.l', '#0x8,%d0', 2)
    e.label('player_pc_014586')
    e.ins('move.b', '0x7(%a1),%d0', 4)
    e.label('player_pc_01458a')
    e.ins('lsl.l', '#0x8,%d0', 2)
    e.label('player_pc_01458c')
    e.ins('move.b', '0x8(%a1),%d0', 4)
    e.label('player_pc_014590')
    e.ins('move.w', '#0xc386,%d1', 4)
    e.label('player_pc_014594')
    e.ins('move.w', '#0xc001,%d2', 4)
    e.label('player_pc_014598')
    e.ins('lea.l', '0xd300:w,%a6', 4)
    e.label('player_pc_01459c')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_0145a2')
    e.ins('move.b', '0x9(%a1),%d0', 4)
    e.label('player_pc_0145a6')
    e.ins('lsl.w', '#0x8,%d0', 2)
    e.label('player_pc_0145a8')
    e.ins('move.b', '0xa(%a1),%d0', 4)
    e.label('player_pc_0145ac')
    e.ins('lsl.l', '#0x8,%d0', 2)
    e.label('player_pc_0145ae')
    e.ins('move.b', '0xb(%a1),%d0', 4)
    e.label('player_pc_0145b2')
    e.ins('lsl.l', '#0x8,%d0', 2)
    e.label('player_pc_0145b4')
    e.ins('move.b', '0xc(%a1),%d0', 4)
    e.label('player_pc_0145b8')
    e.ins('lea.l', '0xd30c:w,%a6', 4)
    e.label('player_pc_0145bc')
    e.ins('jsr', 'player_pc_01270a:l', 6)
    e.label('player_pc_0145c2')
    e.ins('lea.l', '0xd100:w,%a0', 4)
    e.label('player_pc_0145c6')
    e.ins('adda.w', '0xf31a:w,%a0', 4)
    e.label('player_pc_0145ca')
    e.ins('move.w', '#0xf,(%a0)+', 4)
    e.label('player_pc_0145ce')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_0145d2')
    e.ins('move.w', '#0xc380,(%a0)+', 4)
    e.label('player_pc_0145d6')
    e.ins('move.w', '#0xc,%d0', 4)
    e.label('player_pc_0145da')
    e.ins('move.w', '#0xc381,(%a0)+', 4)
    e.label('player_pc_0145de')
    e.ins('dbra', '%d0,player_pc_0145da', 4)
    e.label('player_pc_0145e2')
    e.ins('move.w', '#0xcb80,(%a0)+', 4)
    e.label('player_pc_0145e6')
    e.ins('move.w', '#0xf,0x22(%a0)', 6)
    e.label('player_pc_0145ec')
    e.ins('move.w', '#0xf,(%a0)+', 4)
    e.label('player_pc_0145f0')
    e.ins('move.w', '#0xc482,0x22(%a0)', 6)
    e.label('player_pc_0145f6')
    e.ins('move.w', '#0xc402,(%a0)+', 4)
    e.label('player_pc_0145fa')
    e.ins('move.w', '#0xc382,0x22(%a0)', 6)
    e.label('player_pc_014600')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_014604')
    e.ins('move.w', '#0xc049,%d0', 4)
    e.label('player_pc_014608')
    e.ins('move.w', '#0x5,%d1', 4)
    e.label('player_pc_01460c')
    e.ins('bsr.w', 'player_pc_014778', 4)
    e.label('player_pc_014610')
    e.ins('move.w', '#0xc001,0x22(%a0)', 6)
    e.label('player_pc_014616')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_01461a')
    e.ins('lea.l', '0xd300:w,%a1', 4)
    e.label('player_pc_01461e')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_014622')
    e.ins('move.w', '(%a1)+,0x22(%a0)', 4)
    e.label('player_pc_014626')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_01462a')
    e.ins('dbra', '%d0,player_pc_014622', 4)
    e.label('player_pc_01462e')
    e.ins('move.w', '#0xcb82,0x22(%a0)', 6)
    e.label('player_pc_014634')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_014638')
    e.ins('adda.w', '#0x22,%a0', 4)
    e.label('player_pc_01463c')
    e.ins('move.w', '#0xf,0x22(%a0)', 6)
    e.label('player_pc_014642')
    e.ins('move.w', '#0xf,(%a0)+', 4)
    e.label('player_pc_014646')
    e.ins('move.w', '#0xc602,0x22(%a0)', 6)
    e.label('player_pc_01464c')
    e.ins('move.w', '#0xc582,(%a0)+', 4)
    e.label('player_pc_014650')
    e.ins('move.w', '#0xc382,0x22(%a0)', 6)
    e.label('player_pc_014656')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_01465a')
    e.ins('move.w', '#0xc055,%d0', 4)
    e.label('player_pc_01465e')
    e.ins('move.w', '#0x3,%d1', 4)
    e.label('player_pc_014662')
    e.ins('bsr.w', 'player_pc_014778', 4)
    e.label('player_pc_014666')
    e.ins('move.w', '#0x2,%d0', 4)
    e.label('player_pc_01466a')
    e.ins('move.w', '#0xc001,0x22(%a0)', 6)
    e.label('player_pc_014670')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_014674')
    e.ins('dbra', '%d0,player_pc_01466a', 4)
    e.label('player_pc_014678')
    e.ins('move.w', '#0x5,%d0', 4)
    e.label('player_pc_01467c')
    e.ins('move.w', '(%a1)+,0x22(%a0)', 4)
    e.label('player_pc_014680')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_014684')
    e.ins('dbra', '%d0,player_pc_01467c', 4)
    e.label('player_pc_014688')
    e.ins('move.w', '#0xcb82,0x22(%a0)', 6)
    e.label('player_pc_01468e')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_014692')
    e.ins('adda.w', '#0x22,%a0', 4)
    e.label('player_pc_014696')
    e.ins('move.w', '#0xf,0x22(%a0)', 6)
    e.label('player_pc_01469c')
    e.ins('move.w', '#0xf,(%a0)+', 4)
    e.label('player_pc_0146a0')
    e.ins('move.w', '#0xc782,0x22(%a0)', 6)
    e.label('player_pc_0146a6')
    e.ins('move.w', '#0xc702,(%a0)+', 4)
    e.label('player_pc_0146aa')
    e.ins('move.w', '#0xc382,0x22(%a0)', 6)
    e.label('player_pc_0146b0')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_0146b4')
    e.ins('move.w', '#0xc05d,%d0', 4)
    e.label('player_pc_0146b8')
    e.ins('move.w', '#0x5,%d1', 4)
    e.label('player_pc_0146bc')
    e.ins('bsr.w', 'player_pc_014778', 4)
    e.label('player_pc_0146c0')
    e.ins('move.w', '#0x4,%d0', 4)
    e.label('player_pc_0146c4')
    e.ins('move.w', '#0xc001,0x22(%a0)', 6)
    e.label('player_pc_0146ca')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_0146ce')
    e.ins('dbra', '%d0,player_pc_0146c4', 4)
    e.label('player_pc_0146d2')
    e.ins('move.w', '#0xc001,%d0', 4)
    e.label('player_pc_0146d6')
    e.ins('movea.l', '0xff382c:l,%a2', 6)
    e.label('player_pc_0146dc')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_0146de')
    e.ins('move.b', '(%a2),%d2', 2)
    e.label('player_pc_0146e0')
    e.ins('andi.w', '#0xf,%d2', 4)
    e.label('player_pc_0146e4')
    e.ins('cmpi.w', '#0xa,%d2', 4)
    e.label('player_pc_0146e8')
    e.ins('bcs.b', 'player_pc_0146f2', 2)
    e.label('player_pc_0146ea')
    e.ins('move.w', '#0xc387,%d0', 4)
    e.label('player_pc_0146ee')
    e.ins('subi.w', '#0xa,%d2', 4)
    e.label('player_pc_0146f2')
    e.ins('move.w', '%d0,0x22(%a0)', 4)
    e.label('player_pc_0146f6')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_0146fa')
    e.ins('addi.w', '#0xc386,%d2', 4)
    e.label('player_pc_0146fe')
    e.ins('move.w', '%d2,0x22(%a0)', 4)
    e.label('player_pc_014702')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_014706')
    e.ins('move.w', '#0xcb82,0x22(%a0)', 6)
    e.label('player_pc_01470c')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_014710')
    e.ins('adda.w', '#0x22,%a0', 4)
    e.label('player_pc_014714')
    e.ins('move.w', '#0xf,0x44(%a0)', 6)
    e.label('player_pc_01471a')
    e.ins('move.w', '#0xf,0x22(%a0)', 6)
    e.label('player_pc_014720')
    e.ins('move.w', '#0xf,(%a0)+', 4)
    e.label('player_pc_014724')
    e.ins('move.w', '#0xc802,0x44(%a0)', 6)
    e.label('player_pc_01472a')
    e.ins('move.w', '#0xc682,0x22(%a0)', 6)
    e.label('player_pc_014730')
    e.ins('move.w', '#0xc502,(%a0)+', 4)
    e.label('player_pc_014734')
    e.ins('move.w', '#0xd380,0x44(%a0)', 6)
    e.label('player_pc_01473a')
    e.ins('move.w', '#0xc382,0x22(%a0)', 6)
    e.label('player_pc_014740')
    e.ins('move.w', '#0xc382,(%a0)+', 4)
    e.label('player_pc_014744')
    e.ins('move.w', '#0xc,%d0', 4)
    e.label('player_pc_014748')
    e.ins('move.w', '#0xd381,0x44(%a0)', 6)
    e.label('player_pc_01474e')
    e.ins('move.w', '#0xc001,0x22(%a0)', 6)
    e.label('player_pc_014754')
    e.ins('move.w', '#0xc001,(%a0)+', 4)
    e.label('player_pc_014758')
    e.ins('dbra', '%d0,player_pc_014748', 4)
    e.label('player_pc_01475c')
    e.ins('move.w', '#0xdb80,0x44(%a0)', 6)
    e.label('player_pc_014762')
    e.ins('move.w', '#0xcb82,0x22(%a0)', 6)
    e.label('player_pc_014768')
    e.ins('move.w', '#0xcb82,(%a0)+', 4)
    e.label('player_pc_01476c')
    e.ins('clr.w', '0x44(%a0)', 4)
    e.label('player_pc_014770')
    e.ins('addi.w', '#0x154,0xf31a:w', 6)
    e.label('player_pc_014776')
    e.ins('rts', '', 2)

def _lower_append_wide_paired_tiles(e, rules):
    e.label('player_pc_014778')
    e.ins('move.w', '%d0,(%a0)', 2)
    e.label('player_pc_01477a')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_01477c')
    e.ins('move.w', '%d0,0x22(%a0)', 4)
    e.label('player_pc_014780')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_014782')
    e.ins('addq.w', '#0x2,%a0', 2)
    e.label('player_pc_014784')
    e.ins('dbra', '%d1,player_pc_014778', 4)
    e.label('player_pc_014788')
    e.ins('rts', '', 2)

def _lower_step_candidate_selection_cursor(e, rules):
    e.label('player_pc_0148a4')
    e.ins('move.b', '0xf602:w,%d0', 4)
    e.label('player_pc_0148a8')
    e.ins('andi.w', '#0x3,%d0', 4)
    e.label('player_pc_0148ac')
    e.ins('beq.b', 'player_pc_01490c', 2)
    e.label('player_pc_0148ae')
    e.ins('subi.w', '#0x1,0xf608:w', 6)
    e.label('player_pc_0148b4')
    e.ins('bne.b', 'player_pc_014912', 2)
    e.label('player_pc_0148b6')
    e.ins('move.w', '#0xc,0xf608:w', 6)
    e.label('player_pc_0148bc')
    e.ins('btst.l', '#0x1,%d0', 4)
    e.label('player_pc_0148c0')
    e.ins('bne.b', 'player_pc_0148ec', 2)
    e.label('player_pc_0148c2')
    e.ins('tst.w', '0xf676:w', 4)
    e.label('player_pc_0148c6')
    e.ins('bne.b', 'player_pc_0148e4', 2)
    e.label('player_pc_0148c8')
    e.ins('lea.l', '0xff3930:l,%a0', 6)
    e.label('player_pc_0148ce')
    e.ins('clr.w', '%d0', 2)
    e.label('player_pc_0148d0')
    e.ins('tst.b', '0x1(%a0, %d0.w)', 4)
    e.label('player_pc_0148d4')
    e.ins('bmi.w', 'player_pc_0148dc', 4)
    e.label('player_pc_0148d8')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_0148da')
    e.ins('bra.b', 'player_pc_0148d0', 2)
    e.label('player_pc_0148dc')
    e.ins('move.w', '%d0,0xf676:w', 4)
    e.label('player_pc_0148e0')
    e.ins('bra.w', 'player_pc_014912', 4)
    e.label('player_pc_0148e4')
    e.ins('subq.w', '#0x1,0xf676:w', 4)
    e.label('player_pc_0148e8')
    e.ins('bra.w', 'player_pc_014912', 4)
    e.label('player_pc_0148ec')
    e.ins('move.w', '0xf676:w,%d0', 4)
    e.label('player_pc_0148f0')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_0148f2')
    e.ins('lea.l', '0xff3930:l,%a0', 6)
    e.label('player_pc_0148f8')
    e.ins('tst.b', '(%a0, %d0.w)', 4)
    e.label('player_pc_0148fc')
    e.ins('bpl.b', 'player_pc_014906', 2)
    e.label('player_pc_0148fe')
    e.ins('clr.w', '0xf676:w', 4)
    e.label('player_pc_014902')
    e.ins('bra.w', 'player_pc_014912', 4)
    e.label('player_pc_014906')
    e.ins('move.w', '%d0,0xf676:w', 4)
    e.label('player_pc_01490a')
    e.ins('bra.b', 'player_pc_014912', 2)
    e.label('player_pc_01490c')
    e.ins('move.w', '#0x1,0xf608:w', 6)
    e.label('player_pc_014912')
    e.ins('rts', '', 2)

def _lower_append_candidate_selection_sprite(e, rules):
    e.label('player_pc_014914')
    e.ins('btst.b', '#0x5,0xf603:w', 6)
    e.label('player_pc_01491a')
    e.ins('bne.w', 'player_pc_014954', 4)
    e.label('player_pc_01491e')
    e.ins('move.b', '0xf602:w,%d0', 4)
    e.label('player_pc_014922')
    e.ins('andi.w', '#0x3,%d0', 4)
    e.label('player_pc_014926')
    e.ins('bne.w', 'player_pc_014932', 4)
    e.label('player_pc_01492a')
    e.ins('btst.b', '#0x3,0xf321:w', 6)
    e.label('player_pc_014930')
    e.ins('bne.b', 'player_pc_014954', 2)
    e.label('player_pc_014932')
    e.ins('lea.l', '34(%pc),%a0', 4)
    e.label('player_pc_014936')
    e.ins('nop', '', 2)
    e.label('player_pc_014938')
    e.ins('move.w', '0xf676:w,%d0', 4)
    e.label('player_pc_01493c')
    e.ins('move.w', '%d0,%d1', 2)
    e.label('player_pc_01493e')
    e.ins('lsl.w', '#0x1,%d0', 2)
    e.label('player_pc_014940')
    e.ins('add.w', '%d1,%d0', 2)
    e.label('player_pc_014942')
    e.ins('lsl.w', '#0x3,%d0', 2)
    e.label('player_pc_014944')
    e.ins('addi.w', '#0x30,%d0', 4)
    e.label('player_pc_014948')
    e.ins('move.w', '#0x88,%d1', 4)
    e.label('player_pc_01494c')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_01494e')
    e.ins('jsr', 'player_pc_00ac08:l', 6)
    e.label('player_pc_014954')
    e.ins('rts', '', 2)

def _lower_collect_group_members_below_capacity(e, rules):
    e.label('player_pc_0149a0')
    e.ins('lea.l', '0xb000:w,%a0', 4)
    e.label('player_pc_0149a4')
    e.ins('lea.l', '0xb200:w,%a1', 4)
    e.label('player_pc_0149a8')
    e.ins('movea.l', '0xff382c:l,%a2', 6)
    e.label('player_pc_0149ae')
    e.ins('move.b', '(%a2),%d2', 2)
    e.label('player_pc_0149b0')
    e.ins('andi.w', '#0xf,%d2', 4)
    e.label('player_pc_0149b4')
    e.ins('subq.w', '#0x1,%d2', 2)
    e.label('player_pc_0149b6')
    e.ins('adda.w', '#0xd,%a2', 4)
    e.label('player_pc_0149ba')
    e.ins('lea.l', '0xf500:w,%a3', 4)
    e.label('player_pc_0149be')
    e.ins('clr.w', '%d0', 2)
    e.label('player_pc_0149c0')
    e.ins('clr.w', '%d1', 2)
    e.label('player_pc_0149c2')
    e.ins('move.b', '(%a2)+,%d1', 2)
    e.label('player_pc_0149c4')
    e.ins('lsl.w', '#0x1,%d1', 2)
    e.label('player_pc_0149c6')
    e.ins('move.w', '(%a0, %d1.w),%d3', 4)
    e.label('player_pc_0149ca')
    e.ins('cmp.w', '(%a1, %d1.w),%d3', 4)
    e.label('player_pc_0149ce')
    e.ins('beq.b', 'player_pc_0149d6', 2)
    e.label('player_pc_0149d0')
    e.ins('lsr.w', '#0x1,%d1', 2)
    e.label('player_pc_0149d2')
    e.ins('move.w', '%d1,(%a3)+', 2)
    e.label('player_pc_0149d4')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_0149d6')
    e.ins('dbra', '%d2,player_pc_0149c0', 4)
    e.label('player_pc_0149da')
    e.ins('move.w', '#0xffff,(%a3)', 4)
    e.label('player_pc_0149de')
    e.ins('move.w', '%d0,0xf636:w', 4)
    e.label('player_pc_0149e2')
    e.ins('rts', '', 2)

def _lower_clear_world_group_selection_marks(e, rules):
    e.label('player_pc_014c7c')
    e.ins('move.w', '0xf314:w,0xf356:w', 6)
    e.label('player_pc_014c82')
    e.ins('move.w', '0xf318:w,0xf354:w', 6)
    e.label('player_pc_014c88')
    e.ins('lea.l', '0x9000:w,%a0', 4)
    e.label('player_pc_014c8c')
    e.ins('move.b', '(%a0),%d0', 2)
    e.label('player_pc_014c8e')
    e.ins('bclr.l', '#0x4,%d0', 4)
    e.label('player_pc_014c92')
    e.ins('move.b', '%d0,(%a0)', 2)
    e.label('player_pc_014c94')
    e.ins('andi.w', '#0xf,%d0', 4)
    e.label('player_pc_014c98')
    e.ins('beq.w', 'player_pc_014ca2', 4)
    e.label('player_pc_014c9c')
    e.ins('lea.l', '0xd(%a0, %d0.w),%a0', 4)
    e.label('player_pc_014ca0')
    e.ins('bra.b', 'player_pc_014c8c', 2)
    e.label('player_pc_014ca2')
    e.ins('rts', '', 2)

def _lower_select_world_group_or_city_at_marker(e, rules):
    e.label('player_pc_014ca4')
    e.ins('bsr.w', 'player_pc_014d34', 4)
    e.label('player_pc_014ca8')
    e.ins('bcs.w', 'player_pc_014cf8', 4)
    e.label('player_pc_014cac')
    e.ins('lea.l', '0x9000:w,%a1', 4)
    e.label('player_pc_014cb0')
    e.ins('cmp.b', '0xd(%a1),%d0', 4)
    e.label('player_pc_014cb4')
    e.ins('beq.b', 'player_pc_014cc2', 2)
    e.label('player_pc_014cb6')
    e.ins('move.b', '(%a1),%d1', 2)
    e.label('player_pc_014cb8')
    e.ins('andi.w', '#0xf,%d1', 4)
    e.label('player_pc_014cbc')
    e.ins('lea.l', '0xd(%a1, %d1.w),%a1', 4)
    e.label('player_pc_014cc0')
    e.ins('bra.b', 'player_pc_014cb0', 2)
    e.label('player_pc_014cc2')
    e.ins('move.l', '%a1,0xff382c:l', 6)
    e.label('player_pc_014cc8')
    e.ins('clr.w', '%d1', 2)
    e.label('player_pc_014cca')
    e.ins('move.b', '0x1(%a1),%d1', 4)
    e.label('player_pc_014cce')
    e.ins('lsl.w', '#0x4,%d1', 2)
    e.label('player_pc_014cd0')
    e.ins('move.w', '%d1,0xff3bb6:l', 6)
    e.label('player_pc_014cd6')
    e.ins('subi.w', '#0x68,%d1', 4)
    e.label('player_pc_014cda')
    e.ins('bcc.b', 'player_pc_014cde', 2)
    e.label('player_pc_014cdc')
    e.ins('clr.w', '%d1', 2)
    e.label('player_pc_014cde')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_014ce0')
    e.ins('move.b', '0x2(%a1),%d2', 4)
    e.label('player_pc_014ce4')
    e.ins('lsl.w', '#0x4,%d2', 2)
    e.label('player_pc_014ce6')
    e.ins('move.w', '%d2,0xff3bb8:l', 6)
    e.label('player_pc_014cec')
    e.ins('subi.w', '#0x98,%d2', 4)
    e.label('player_pc_014cf0')
    e.ins('bcc.b', 'player_pc_014cf4', 2)
    e.label('player_pc_014cf2')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_014cf4')
    e.ins('bra.w', 'player_pc_014d32', 4)
    e.label('player_pc_014cf8')
    e.ins('clr.w', '0xf772:w', 4)
    e.label('player_pc_014cfc')
    e.ins('clr.w', '%d1', 2)
    e.label('player_pc_014cfe')
    e.ins('move.b', '(%a1),%d1', 2)
    e.label('player_pc_014d00')
    e.ins('move.w', '%d1,0xf68a:w', 4)
    e.label('player_pc_014d04')
    e.ins('cmpi.w', '#0x32,%d1', 4)
    e.label('player_pc_014d08')
    e.ins('beq.b', 'player_pc_014cac', 2)
    e.label('player_pc_014d0a')
    e.ins('lea.l', '0xd4ac6:l,%a1', 6)
    e.label('player_pc_014d10')
    e.ins('lsl.w', '#0x2,%d1', 2)
    e.label('player_pc_014d12')
    e.ins('move.w', '(%a1, %d1.w),%d2', 4)
    e.label('player_pc_014d16')
    e.ins('move.w', '0x2(%a1, %d1.w),%d1', 4)
    e.label('player_pc_014d1a')
    e.ins('subi.w', '#0x68,%d1', 4)
    e.label('player_pc_014d1e')
    e.ins('bcc.w', 'player_pc_014d24', 4)
    e.label('player_pc_014d22')
    e.ins('clr.w', '%d1', 2)
    e.label('player_pc_014d24')
    e.ins('subi.w', '#0x98,%d2', 4)
    e.label('player_pc_014d28')
    e.ins('bcc.b', 'player_pc_014d2c', 2)
    e.label('player_pc_014d2a')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_014d2c')
    e.ins('clr.l', '0xff382c:l', 6)
    e.label('player_pc_014d32')
    e.ins('rts', '', 2)

def _lower_find_world_marker_record(e, rules):
    e.label('player_pc_014d34')
    e.ins('lea.l', '0xff3000:l,%a1', 6)
    e.label('player_pc_014d3a')
    e.ins('addq.w', '#0x1,%a1', 2)
    e.label('player_pc_014d3c')
    e.ins('cmp.b', '(%a1)+,%d0', 2)
    e.label('player_pc_014d3e')
    e.ins('beq.w', 'player_pc_014d48', 4)
    e.label('player_pc_014d42')
    e.ins('tst.b', '(%a1)+', 2)
    e.label('player_pc_014d44')
    e.ins('bne.b', 'player_pc_014d42', 2)
    e.label('player_pc_014d46')
    e.ins('bra.b', 'player_pc_014d3a', 2)
    e.label('player_pc_014d48')
    e.ins('addq.w', '#0x1,%a1', 2)
    e.label('player_pc_014d4a')
    e.ins('tst.b', '(%a1)+', 2)
    e.label('player_pc_014d4c')
    e.ins('bpl.w', 'player_pc_014d58', 4)
    e.label('player_pc_014d50')
    e.ins('ori.w', '#0x1,%sr', 4)
    e.label('player_pc_014d54')
    e.ins('bra.w', 'player_pc_014d62', 4)
    e.label('player_pc_014d58')
    e.ins('move.w', '#0xffff,0xf68a:w', 6)
    e.label('player_pc_014d5e')
    e.ins('andi.w', '#0xfffe,%sr', 4)
    e.label('player_pc_014d62')
    e.ins('rts', '', 2)

def _lower_test_selected_group_enemy_contacts(e, rules):
    e.label('player_pc_014e20')
    e.ins('cmpi.w', '#0x32,0xf68a:w', 6)
    e.label('player_pc_014e26')
    e.ins('bne.w', 'player_pc_014e52', 4)
    e.label('player_pc_014e2a')
    e.ins('movea.l', '0xff382c:l,%a0', 6)
    e.label('player_pc_014e30')
    e.ins('movem.l', '%d1-%d2,-(%a7)', 4)
    e.label('player_pc_014e34')
    e.ins('jsr', 'player_pc_01cea0:l', 6)
    e.label('player_pc_014e3a')
    e.ins('movem.l', '(%a7)+,%d1-%d2', 4)
    e.label('player_pc_014e3e')
    e.ins('tst.w', '%d0', 2)
    e.label('player_pc_014e40')
    e.ins('bne.w', 'player_pc_014e52', 4)
    e.label('player_pc_014e44')
    e.ins('addq.w', '#0x2,0xff3bb2:l', 6)
    e.label('player_pc_014e4a')
    e.ins('ori.w', '#0x1,%sr', 4)
    e.label('player_pc_014e4e')
    e.ins('bra.w', 'player_pc_014e56', 4)
    e.label('player_pc_014e52')
    e.ins('andi.w', '#0xfffe,%sr', 4)
    e.label('player_pc_014e56')
    e.ins('rts', '', 2)

def _lower_set_pending_group_move_position(e, rules):
    e.label('player_pc_0150de')
    e.ins('move.w', '0xff3bb6:l,%d1', 6)
    e.label('player_pc_0150e4')
    e.ins('move.w', '0xff3bb8:l,%d2', 6)
    e.label('player_pc_0150ea')
    e.ins('subq.w', '#0x1,%d0', 2)
    e.label('player_pc_0150ec')
    e.ins('bne.b', 'player_pc_0150f4', 2)
    e.label('player_pc_0150ee')
    e.ins('subi.w', '#0x10,%d1', 4)
    e.label('player_pc_0150f2')
    e.ins('bra.b', 'player_pc_015120', 2)
    e.label('player_pc_0150f4')
    e.ins('subq.w', '#0x1,%d0', 2)
    e.label('player_pc_0150f6')
    e.ins('bne.b', 'player_pc_015108', 2)
    e.label('player_pc_0150f8')
    e.ins('addi.w', '#0x10,%d2', 4)
    e.label('player_pc_0150fc')
    e.ins('movea.l', '0xff382c:l,%a1', 6)
    e.label('player_pc_015102')
    e.ins('bset.b', '#0x7,(%a1)', 4)
    e.label('player_pc_015106')
    e.ins('bra.b', 'player_pc_015120', 2)
    e.label('player_pc_015108')
    e.ins('subq.w', '#0x1,%d0', 2)
    e.label('player_pc_01510a')
    e.ins('bne.b', 'player_pc_015112', 2)
    e.label('player_pc_01510c')
    e.ins('addi.w', '#0x10,%d1', 4)
    e.label('player_pc_015110')
    e.ins('bra.b', 'player_pc_015120', 2)
    e.label('player_pc_015112')
    e.ins('subi.w', '#0x10,%d2', 4)
    e.label('player_pc_015116')
    e.ins('movea.l', '0xff382c:l,%a1', 6)
    e.label('player_pc_01511c')
    e.ins('bclr.b', '#0x7,(%a1)', 4)
    e.label('player_pc_015120')
    e.ins('move.w', '%d1,0xff3bba:l', 6)
    e.label('player_pc_015126')
    e.ins('move.w', '%d2,0xff3bbc:l', 6)
    e.label('player_pc_01512c')
    e.ins('rts', '', 2)

def _lower_merge_compatible_world_groups(e, rules):
    e.label('player_pc_01512e')
    e.ins('movea.l', '0xff382c:l,%a0', 6)
    e.label('player_pc_015134')
    e.ins('move.b', '0x1(%a0),%d1', 4)
    e.label('player_pc_015138')
    e.ins('move.b', '0x2(%a0),%d2', 4)
    e.label('player_pc_01513c')
    e.ins('move.b', '0x4(%a0),%d3', 4)
    e.label('player_pc_015140')
    e.ins('lea.l', '0x9000:w,%a1', 4)
    e.label('player_pc_015144')
    e.ins('move.b', '(%a1),%d0', 2)
    e.label('player_pc_015146')
    e.ins('btst.l', '#0x6,%d0', 4)
    e.label('player_pc_01514a')
    e.ins('bne.b', 'player_pc_015174', 2)
    e.label('player_pc_01514c')
    e.ins('andi.w', '#0xf,%d0', 4)
    e.label('player_pc_015150')
    e.ins('beq.b', 'player_pc_01517e', 2)
    e.label('player_pc_015152')
    e.ins('cmpa.l', '%a0,%a1', 2)
    e.label('player_pc_015154')
    e.ins('beq.b', 'player_pc_015174', 2)
    e.label('player_pc_015156')
    e.ins('cmp.b', '0x1(%a1),%d1', 4)
    e.label('player_pc_01515a')
    e.ins('bne.b', 'player_pc_015174', 2)
    e.label('player_pc_01515c')
    e.ins('cmp.b', '0x2(%a1),%d2', 4)
    e.label('player_pc_015160')
    e.ins('bne.b', 'player_pc_015174', 2)
    e.label('player_pc_015162')
    e.ins('cmp.b', '0x4(%a1),%d3', 4)
    e.label('player_pc_015166')
    e.ins('bne.b', 'player_pc_015174', 2)
    e.label('player_pc_015168')
    e.ins('cmpa.l', '%a0,%a1', 2)
    e.label('player_pc_01516a')
    e.ins('bhi.b', 'player_pc_01516e', 2)
    e.label('player_pc_01516c')
    e.ins('exg', '%a0,%a1', 2)
    e.label('player_pc_01516e')
    e.ins('bsr.w', 'player_pc_015186', 4)
    e.label('player_pc_015172')
    e.ins('bra.b', 'player_pc_01517e', 2)
    e.label('player_pc_015174')
    e.ins('andi.w', '#0xf,%d0', 4)
    e.label('player_pc_015178')
    e.ins('lea.l', '0xd(%a1, %d0.w),%a1', 4)
    e.label('player_pc_01517c')
    e.ins('bra.b', 'player_pc_015144', 2)
    e.label('player_pc_01517e')
    e.ins('move.l', '%a0,0xff382c:l', 6)
    e.label('player_pc_015184')
    e.ins('rts', '', 2)

def _lower_merge_world_group_records(e, rules):
    e.label('player_pc_015186')
    e.ins('move.b', '(%a1),%d0', 2)
    e.label('player_pc_015188')
    e.ins('andi.w', '#0xf,%d0', 4)
    e.label('player_pc_01518c')
    e.ins('move.b', '(%a0),%d1', 2)
    e.label('player_pc_01518e')
    e.ins('andi.w', '#0xf,%d1', 4)
    e.label('player_pc_015192')
    e.ins('move.w', '%d1,%d2', 2)
    e.label('player_pc_015194')
    e.ins('add.w', '%d0,%d1', 2)
    e.label('player_pc_015196')
    e.ins('move.b', '%d1,(%a0)', 2)
    e.label('player_pc_015198')
    e.ins('addi.w', '#0xd,%d2', 4)
    e.label('player_pc_01519c')
    e.ins('lea.l', '(%a0, %d2.w),%a4', 4)
    e.label('player_pc_0151a0')
    e.ins('move.b', '0x5(%a0),%d2', 4)
    e.label('player_pc_0151a4')
    e.ins('lsl.w', '#0x8,%d2', 2)
    e.label('player_pc_0151a6')
    e.ins('move.b', '0x6(%a0),%d2', 4)
    e.label('player_pc_0151aa')
    e.ins('lsl.l', '#0x8,%d2', 2)
    e.label('player_pc_0151ac')
    e.ins('move.b', '0x7(%a0),%d2', 4)
    e.label('player_pc_0151b0')
    e.ins('lsl.l', '#0x8,%d2', 2)
    e.label('player_pc_0151b2')
    e.ins('move.b', '0x8(%a0),%d2', 4)
    e.label('player_pc_0151b6')
    e.ins('move.b', '0x5(%a1),%d3', 4)
    e.label('player_pc_0151ba')
    e.ins('lsl.w', '#0x8,%d3', 2)
    e.label('player_pc_0151bc')
    e.ins('move.b', '0x6(%a1),%d3', 4)
    e.label('player_pc_0151c0')
    e.ins('lsl.l', '#0x8,%d3', 2)
    e.label('player_pc_0151c2')
    e.ins('move.b', '0x7(%a1),%d3', 4)
    e.label('player_pc_0151c6')
    e.ins('lsl.l', '#0x8,%d3', 2)
    e.label('player_pc_0151c8')
    e.ins('move.b', '0x8(%a1),%d3', 4)
    e.label('player_pc_0151cc')
    e.ins('add.l', '%d3,%d2', 2)
    e.label('player_pc_0151ce')
    e.ins('cmpi.l', '#'+hex(rules['merged_resource_cap'])+',%d2', 6)
    e.label('player_pc_0151d4')
    e.ins('bls.b', 'player_pc_0151dc', 2)
    e.label('player_pc_0151d6')
    e.ins('move.l', '#'+hex(rules['merged_resource_cap'])+',%d2', 6)
    e.label('player_pc_0151dc')
    e.ins('move.b', '%d2,0x8(%a0)', 4)
    e.label('player_pc_0151e0')
    e.ins('lsr.l', '#0x8,%d2', 2)
    e.label('player_pc_0151e2')
    e.ins('move.b', '%d2,0x7(%a0)', 4)
    e.label('player_pc_0151e6')
    e.ins('lsr.l', '#0x8,%d2', 2)
    e.label('player_pc_0151e8')
    e.ins('move.b', '%d2,0x6(%a0)', 4)
    e.label('player_pc_0151ec')
    e.ins('lsr.w', '#0x8,%d2', 2)
    e.label('player_pc_0151ee')
    e.ins('move.b', '%d2,0x5(%a0)', 4)
    e.label('player_pc_0151f2')
    e.ins('move.b', '0x9(%a0),%d2', 4)
    e.label('player_pc_0151f6')
    e.ins('lsl.w', '#0x8,%d2', 2)
    e.label('player_pc_0151f8')
    e.ins('move.b', '0xa(%a0),%d2', 4)
    e.label('player_pc_0151fc')
    e.ins('lsl.l', '#0x8,%d2', 2)
    e.label('player_pc_0151fe')
    e.ins('move.b', '0xb(%a0),%d2', 4)
    e.label('player_pc_015202')
    e.ins('lsl.l', '#0x8,%d2', 2)
    e.label('player_pc_015204')
    e.ins('move.b', '0xc(%a0),%d2', 4)
    e.label('player_pc_015208')
    e.ins('move.b', '0x9(%a1),%d3', 4)
    e.label('player_pc_01520c')
    e.ins('lsl.w', '#0x8,%d3', 2)
    e.label('player_pc_01520e')
    e.ins('move.b', '0xa(%a1),%d3', 4)
    e.label('player_pc_015212')
    e.ins('lsl.l', '#0x8,%d3', 2)
    e.label('player_pc_015214')
    e.ins('move.b', '0xb(%a1),%d3', 4)
    e.label('player_pc_015218')
    e.ins('lsl.l', '#0x8,%d3', 2)
    e.label('player_pc_01521a')
    e.ins('move.b', '0xc(%a1),%d3', 4)
    e.label('player_pc_01521e')
    e.ins('add.l', '%d2,%d3', 2)
    e.label('player_pc_015220')
    e.ins('cmpi.l', '#'+hex(rules['merged_resource_cap'])+',%d3', 6)
    e.label('player_pc_015226')
    e.ins('bls.b', 'player_pc_01522e', 2)
    e.label('player_pc_015228')
    e.ins('move.l', '#'+hex(rules['merged_resource_cap'])+',%d3', 6)
    e.label('player_pc_01522e')
    e.ins('move.b', '%d3,0xc(%a0)', 4)
    e.label('player_pc_015232')
    e.ins('lsr.l', '#0x8,%d3', 2)
    e.label('player_pc_015234')
    e.ins('move.b', '%d3,0xb(%a0)', 4)
    e.label('player_pc_015238')
    e.ins('lsr.l', '#0x8,%d3', 2)
    e.label('player_pc_01523a')
    e.ins('move.b', '%d3,0xa(%a0)', 4)
    e.label('player_pc_01523e')
    e.ins('lsr.w', '#0x8,%d3', 2)
    e.label('player_pc_015240')
    e.ins('move.b', '%d3,0x9(%a0)', 4)
    e.label('player_pc_015244')
    e.ins('clr.w', '%d1', 2)
    e.label('player_pc_015246')
    e.ins('lea.l', '0xf65c:w,%a2', 4)
    e.label('player_pc_01524a')
    e.ins('move.b', '0xd(%a1, %d1.w),(%a2)+', 4)
    e.label('player_pc_01524e')
    e.ins('addq.w', '#0x1,%d1', 2)
    e.label('player_pc_015250')
    e.ins('cmp.w', '%d0,%d1', 2)
    e.label('player_pc_015252')
    e.ins('bcs.b', 'player_pc_01524a', 2)
    e.label('player_pc_015254')
    e.ins('move.w', '%d0,%d1', 2)
    e.label('player_pc_015256')
    e.ins('addi.w', '#0xd,%d1', 4)
    e.label('player_pc_01525a')
    e.ins('lea.l', '(%a1, %d1.w),%a2', 4)
    e.label('player_pc_01525e')
    e.ins('lea.l', '(%a1, %d0.w),%a3', 4)
    e.label('player_pc_015262')
    e.ins('lea.l', '(%a1),%a5', 2)
    e.label('player_pc_015264')
    e.ins('movea.l', '%a3,%a1', 2)
    e.label('player_pc_015266')
    e.ins('cmpa.l', '%a5,%a4', 2)
    e.label('player_pc_015268')
    e.ins('beq.b', 'player_pc_015270', 2)
    e.label('player_pc_01526a')
    e.ins('move.b', '-(%a5),-(%a3)', 2)
    e.label('player_pc_01526c')
    e.ins('cmpa.l', '%a5,%a4', 2)
    e.label('player_pc_01526e')
    e.ins('bcs.b', 'player_pc_01526a', 2)
    e.label('player_pc_015270')
    e.ins('lea.l', '0xf65c:w,%a6', 4)
    e.label('player_pc_015274')
    e.ins('subq.w', '#0x1,%d0', 2)
    e.label('player_pc_015276')
    e.ins('move.b', '(%a6)+,(%a4)+', 2)
    e.label('player_pc_015278')
    e.ins('dbra', '%d0,player_pc_015276', 4)
    e.label('player_pc_01527c')
    e.ins('move.b', '(%a2),%d0', 2)
    e.label('player_pc_01527e')
    e.ins('andi.w', '#0xf,%d0', 4)
    e.label('player_pc_015282')
    e.ins('beq.b', 'player_pc_015290', 2)
    e.label('player_pc_015284')
    e.ins('addi.w', '#0xc,%d0', 4)
    e.label('player_pc_015288')
    e.ins('move.b', '(%a2)+,(%a1)+', 2)
    e.label('player_pc_01528a')
    e.ins('dbra', '%d0,player_pc_015288', 4)
    e.label('player_pc_01528e')
    e.ins('bra.b', 'player_pc_01527c', 2)
    e.label('player_pc_015290')
    e.ins('clr.b', '(%a1)', 2)
    e.label('player_pc_015292')
    e.ins('lea.l', '0xd(%a0),%a1', 4)
    e.label('player_pc_015296')
    e.ins('lea.l', '0xc400:w,%a2', 4)
    e.label('player_pc_01529a')
    e.ins('moveq', '#0,%d0', 2)
    e.label('player_pc_01529c')
    e.ins('clr.w', '%d1', 2)
    e.label('player_pc_01529e')
    e.ins('move.b', '(%a0),%d2', 2)
    e.label('player_pc_0152a0')
    e.ins('andi.w', '#0xf,%d2', 4)
    e.label('player_pc_0152a4')
    e.ins('move.w', '%d2,%d3', 2)
    e.label('player_pc_0152a6')
    e.ins('subq.w', '#0x1,%d3', 2)
    e.label('player_pc_0152a8')
    e.ins('move.b', '(%a1)+,%d1', 2)
    e.label('player_pc_0152aa')
    e.ins('clr.w', '%d4', 2)
    e.label('player_pc_0152ac')
    e.ins('move.b', '(%a2, %d1.w),%d4', 4)
    e.label('player_pc_0152b0')
    e.ins('add.w', '%d4,%d0', 2)
    e.label('player_pc_0152b2')
    e.ins('dbra', '%d3,player_pc_0152a8', 4)
    e.label('player_pc_0152b6')
    e.ins('divu.w', '%d2,%d0', 2)
    e.label('player_pc_0152b8')
    e.ins('move.b', '%d0,0x3(%a0)', 4)
    e.label('player_pc_0152bc')
    e.ins('rts', '', 2)

def _lower_test_pending_group_destination(e, rules):
    e.label('player_pc_0152be')
    e.ins('move.w', '0xff3bba:l,%d0', 6)
    e.label('player_pc_0152c4')
    e.ins('lsr.w', '#0x4,%d0', 2)
    e.label('player_pc_0152c6')
    e.ins('move.w', '0xff3bbc:l,%d1', 6)
    e.label('player_pc_0152cc')
    e.ins('lsr.w', '#0x4,%d1', 2)
    e.label('player_pc_0152ce')
    e.ins('movea.l', '0xff382c:l,%a0', 6)
    e.label('player_pc_0152d4')
    e.ins('move.b', '(%a0),%d2', 2)
    e.label('player_pc_0152d6')
    e.ins('andi.w', '#0xf,%d2', 4)
    e.label('player_pc_0152da')
    e.ins('move.b', '0x4(%a0),%d4', 4)
    e.label('player_pc_0152de')
    e.ins('lea.l', '0x9000:w,%a1', 4)
    e.label('player_pc_0152e2')
    e.ins('move.b', '(%a1),%d3', 2)
    e.label('player_pc_0152e4')
    e.ins('andi.w', '#0xf,%d3', 4)
    e.label('player_pc_0152e8')
    e.ins('beq.b', 'player_pc_01532a', 2)
    e.label('player_pc_0152ea')
    e.ins('cmp.b', '0x1(%a1),%d0', 4)
    e.label('player_pc_0152ee')
    e.ins('bne.b', 'player_pc_015322', 2)
    e.label('player_pc_0152f0')
    e.ins('cmp.b', '0x2(%a1),%d1', 4)
    e.label('player_pc_0152f4')
    e.ins('bne.b', 'player_pc_015322', 2)
    e.label('player_pc_0152f6')
    e.ins('cmp.b', '0x4(%a1),%d4', 4)
    e.label('player_pc_0152fa')
    e.ins('bne.w', 'player_pc_01537e', 4)
    e.label('player_pc_0152fe')
    e.ins('lea.l', '0xff3000:l,%a2', 6)
    e.label('player_pc_015304')
    e.ins('adda.w', '0xff3826:l,%a2', 6)
    e.label('player_pc_01530a')
    e.ins('tst.b', '0x1(%a2)', 4)
    e.label('player_pc_01530e')
    e.ins('bne.w', 'player_pc_015378', 4)
    e.label('player_pc_015312')
    e.ins('move.w', '%d3,%d4', 2)
    e.label('player_pc_015314')
    e.ins('add.w', '%d2,%d4', 2)
    e.label('player_pc_015316')
    e.ins('cmpi.w', '#0xa,%d4', 4)
    e.label('player_pc_01531a')
    e.ins('bhi.w', 'player_pc_01537e', 4)
    e.label('player_pc_01531e')
    e.ins('bra.w', 'player_pc_015378', 4)
    e.label('player_pc_015322')
    e.ins('addi.w', '#0xd,%d3', 4)
    e.label('player_pc_015326')
    e.ins('adda.w', '%d3,%a1', 2)
    e.label('player_pc_015328')
    e.ins('bra.b', 'player_pc_0152e2', 2)
    e.label('player_pc_01532a')
    e.ins('lea.l', '0xce9c:w,%a1', 4)
    e.label('player_pc_01532e')
    e.ins('move.w', '#0x27,%d2', 4)
    e.label('player_pc_015332')
    e.ins('tst.b', '(%a1)', 2)
    e.label('player_pc_015334')
    e.ins('beq.b', 'player_pc_015342', 2)
    e.label('player_pc_015336')
    e.ins('cmp.b', '0x1(%a1),%d0', 4)
    e.label('player_pc_01533a')
    e.ins('bne.b', 'player_pc_015342', 2)
    e.label('player_pc_01533c')
    e.ins('cmp.b', '0x2(%a1),%d1', 4)
    e.label('player_pc_015340')
    e.ins('beq.b', 'player_pc_01534c', 2)
    e.label('player_pc_015342')
    e.ins('subq.w', '#0x4,%a1', 2)
    e.label('player_pc_015344')
    e.ins('dbra', '%d2,player_pc_015332', 4)
    e.label('player_pc_015348')
    e.ins('bra.w', 'player_pc_015378', 4)
    e.label('player_pc_01534c')
    e.ins('lea.l', '0xe710:w,%a3', 4)
    e.label('player_pc_015350')
    e.ins('move.w', '%d4,%d7', 2)
    e.label('player_pc_015352')
    e.ins('lsl.w', '#0x1,%d7', 2)
    e.label('player_pc_015354')
    e.ins('move.w', '(%a3, %d7.w),%d7', 4)
    e.label('player_pc_015358')
    e.ins('lea.l', '0xf428:w,%a3', 4)
    e.label('player_pc_01535c')
    e.ins('move.b', '(%a3, %d2.w),%d3', 4)
    e.label('player_pc_015360')
    e.ins('cmp.b', '%d3,%d4', 2)
    e.label('player_pc_015362')
    e.ins('beq.w', 'player_pc_01537e', 4)
    e.label('player_pc_015366')
    e.ins('ext.w', '%d3', 2)
    e.label('player_pc_015368')
    e.ins('btst.l', '%d3,%d7', 2)
    e.label('player_pc_01536a')
    e.ins('bne.w', 'player_pc_01537e', 4)
    e.label('player_pc_01536e')
    e.ins('movea.l', '%a1,%a0', 2)
    e.label('player_pc_015370')
    e.ins('bsr.w', 'player_pc_0154c8', 4)
    e.label('player_pc_015374')
    e.ins('bra.w', 'player_pc_01537e', 4)
    e.label('player_pc_015378')
    e.ins('andi.w', '#0xfffe,%sr', 4)
    e.label('player_pc_01537c')
    e.ins('bra.b', 'player_pc_015382', 2)
    e.label('player_pc_01537e')
    e.ins('ori.w', '#0x1,%sr', 4)
    e.label('player_pc_015382')
    e.ins('rts', '', 2)

def _lower_encode_live_group_coordinate_packet(e, rules):
    e.label('player_pc_01cea0')
    e.ins('movea.l', '0xff382c:l,%a0', 6)
    e.label('player_pc_01cea6')
    e.ins('move.b', '0x1(%a0),%d0', 4)
    e.label('player_pc_01ceaa')
    e.ins('lsl.w', '#0x8,%d0', 2)
    e.label('player_pc_01ceac')
    e.ins('move.b', '0x2(%a0),%d0', 4)
    e.label('player_pc_01ceb0')
    e.ins('move.b', '0x4(%a0),%d7', 4)
    e.label('player_pc_01ceb4')
    e.ins('move.w', '%d0,%d1', 2)
    e.label('player_pc_01ceb6')
    e.ins('move.w', '%d0,%d2', 2)
    e.label('player_pc_01ceb8')
    e.ins('move.w', '%d0,%d3', 2)
    e.label('player_pc_01ceba')
    e.ins('subi.w', '#0x100,%d0', 4)
    e.label('player_pc_01cebe')
    e.ins('addq.w', '#0x1,%d1', 2)
    e.label('player_pc_01cec0')
    e.ins('addi.w', '#0x100,%d2', 4)
    e.label('player_pc_01cec4')
    e.ins('subq.w', '#0x1,%d3', 2)
    e.label('player_pc_01cec6')
    e.ins('move.l', '#0xffffffff,0xefbe:w', 8)
    e.label('player_pc_01cece')
    e.ins('move.l', '#0xffffffff,0xefc2:w', 8)
    e.label('player_pc_01ced6')
    e.ins('lea.l', '0x9000:w,%a1', 4)
    e.label('player_pc_01ceda')
    e.ins('clr.w', '%d4', 2)
    e.label('player_pc_01cedc')
    e.ins('move.b', '(%a1, %d4.w),%d5', 4)
    e.label('player_pc_01cee0')
    e.ins('andi.b', '#0xf,%d5', 4)
    e.label('player_pc_01cee4')
    e.ins('beq.w', 'player_pc_01cf40', 4)
    e.label('player_pc_01cee8')
    e.ins('btst.b', '#0x5,(%a1, %d4.w)', 6)
    e.label('player_pc_01ceee')
    e.ins('bne.w', 'player_pc_01cf38', 4)
    e.label('player_pc_01cef2')
    e.ins('cmp.b', '0x4(%a1, %d4.w),%d7', 4)
    e.label('player_pc_01cef6')
    e.ins('beq.w', 'player_pc_01cf38', 4)
    e.label('player_pc_01cefa')
    e.ins('move.b', '0x1(%a1, %d4.w),%d6', 4)
    e.label('player_pc_01cefe')
    e.ins('lsl.w', '#0x8,%d6', 2)
    e.label('player_pc_01cf00')
    e.ins('move.b', '0x2(%a1, %d4.w),%d6', 4)
    e.label('player_pc_01cf04')
    e.ins('cmp.w', '%d0,%d6', 2)
    e.label('player_pc_01cf06')
    e.ins('bne.w', 'player_pc_01cf12', 4)
    e.label('player_pc_01cf0a')
    e.ins('move.w', '%d4,0xefbe:w', 4)
    e.label('player_pc_01cf0e')
    e.ins('bra.w', 'player_pc_01cf38', 4)
    e.label('player_pc_01cf12')
    e.ins('cmp.w', '%d1,%d6', 2)
    e.label('player_pc_01cf14')
    e.ins('bne.w', 'player_pc_01cf20', 4)
    e.label('player_pc_01cf18')
    e.ins('move.w', '%d4,0xefc0:w', 4)
    e.label('player_pc_01cf1c')
    e.ins('bra.w', 'player_pc_01cf38', 4)
    e.label('player_pc_01cf20')
    e.ins('cmp.w', '%d2,%d6', 2)
    e.label('player_pc_01cf22')
    e.ins('bne.w', 'player_pc_01cf2e', 4)
    e.label('player_pc_01cf26')
    e.ins('move.w', '%d4,0xefc2:w', 4)
    e.label('player_pc_01cf2a')
    e.ins('bra.w', 'player_pc_01cf38', 4)
    e.label('player_pc_01cf2e')
    e.ins('cmp.w', '%d3,%d6', 2)
    e.label('player_pc_01cf30')
    e.ins('bne.w', 'player_pc_01cf38', 4)
    e.label('player_pc_01cf34')
    e.ins('move.w', '%d4,0xefc4:w', 4)
    e.label('player_pc_01cf38')
    e.ins('addi.w', '#0xd,%d4', 4)
    e.label('player_pc_01cf3c')
    e.ins('add.w', '%d5,%d4', 2)
    e.label('player_pc_01cf3e')
    e.ins('bra.b', 'player_pc_01cedc', 2)
    e.label('player_pc_01cf40')
    e.ins('clr.w', '%d0', 2)
    e.label('player_pc_01cf42')
    e.ins('move.w', '#0x3,%d1', 4)
    e.label('player_pc_01cf46')
    e.ins('lea.l', '0xefbe:w,%a1', 4)
    e.label('player_pc_01cf4a')
    e.ins('tst.w', '(%a1)+', 2)
    e.label('player_pc_01cf4c')
    e.ins('bmi.w', 'player_pc_01cf52', 4)
    e.label('player_pc_01cf50')
    e.ins('addq.w', '#0x1,%d0', 2)
    e.label('player_pc_01cf52')
    e.ins('dbra', '%d1,player_pc_01cf4a', 4)
    e.label('player_pc_01cf56')
    e.ins('rts', '', 2)

LOWERERS = {
    'append_live_command_string_words':_lower_append_live_command_string_words,
    'append_route_selection_pair':_lower_append_route_selection_pair,
    'append_route_cursor_sprite':_lower_append_route_cursor_sprite,
    'step_world_route_cursor':_lower_step_world_route_cursor,
    'query_scaled_route_terrain':_lower_query_scaled_route_terrain,
    'query_route_move_cost':_lower_query_route_move_cost,
    'append_candidate_member_panel':_lower_append_candidate_member_panel,
    'append_short_paired_tiles':_lower_append_short_paired_tiles,
    'append_selected_group_panel':_lower_append_selected_group_panel,
    'append_wide_paired_tiles':_lower_append_wide_paired_tiles,
    'step_candidate_selection_cursor':_lower_step_candidate_selection_cursor,
    'append_candidate_selection_sprite':_lower_append_candidate_selection_sprite,
    'collect_group_members_below_capacity':_lower_collect_group_members_below_capacity,
    'clear_world_group_selection_marks':_lower_clear_world_group_selection_marks,
    'select_world_group_or_city_at_marker':_lower_select_world_group_or_city_at_marker,
    'find_world_marker_record':_lower_find_world_marker_record,
    'test_selected_group_enemy_contacts':_lower_test_selected_group_enemy_contacts,
    'set_pending_group_move_position':_lower_set_pending_group_move_position,
    'merge_compatible_world_groups':_lower_merge_compatible_world_groups,
    'merge_world_group_records':_lower_merge_world_group_records,
    'test_pending_group_destination':_lower_test_pending_group_destination,
    'encode_live_group_coordinate_packet':_lower_encode_live_group_coordinate_packet,
}

def compile_display(source):
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    records['append_selected_group_panel']['effects'] = dict(legacy_projection=records['append_selected_group_panel']['effects'],
        sole_selected_panel_fields={name:records[name]['effects'] for name in ('_selected_group_panel_store_fields', '_selected_group_panel_cell_fields', '_selected_group_panel_amount_fields', '_selected_group_panel_decimal_fields', 'append_wide_paired_tiles_fields', '_selected_group_panel_call_fields', '_selected_group_panel_blank_cells_fields', '_selected_group_panel_digits_fields', 'append_selected_group_panel_fields')})
    records['append_wide_paired_tiles']['effects'] = dict(legacy_projection=records['append_wide_paired_tiles']['effects'],
        sole_fullFrame=records['append_wide_paired_tiles_fields']['effects'])
    records['append_live_command_string_words']['effects'] = dict(legacy_projection=records['append_live_command_string_words']['effects'],
        sole_sprite_packet_fields={name:records[name]['effects'] for name in ('_sprite_bit', '_sprite_compare', '_sprite_finish', '_sprite_increment_count', '_sprite_left_long_four', '_sprite_signed_vertical_word', '_sprite_swap', 'append_live_command_sprite_fields', 'append_live_command_sprite_packet_fields')})
    sole_route_command_fields = {name: records[name]['effects'] for name in ('_route_command_emit_fields', '_route_command_memory_delta_fields', '_route_command_call_fields', 'execute_city_group_display_fields', 'append_route_selection_pair_fields', 'append_route_cursor_sprite_fields', 'step_world_route_cursor_fields', 'query_scaled_route_terrain_fields', 'query_route_move_cost_fields', 'append_candidate_member_panel_fields', 'append_short_paired_tiles_fields', 'step_candidate_selection_cursor_fields', 'append_candidate_selection_sprite_fields', 'collect_group_members_below_capacity_fields', 'clear_world_group_selection_marks_fields')}
    for owner in ('append_route_selection_pair', 'append_route_cursor_sprite', 'step_world_route_cursor', 'query_scaled_route_terrain', 'query_route_move_cost', 'append_candidate_member_panel', 'append_short_paired_tiles', 'step_candidate_selection_cursor', 'append_candidate_selection_sprite', 'collect_group_members_below_capacity', 'clear_world_group_selection_marks'):
        records[owner]['effects'] = dict(legacy_projection=records[owner]['effects'], sole_route_command_fields=sole_route_command_fields)
    return lower_declared({b.name:records[b.name] for b in DISPLAY_BINDINGS}, DISPLAY_BINDINGS, LOWERERS)

# B18 complete AC08 descriptor fields; physical native lowerers unchanged.
APPROVED.setdefault('contexts_display',set()).update({'SpritePacketMemory', '_first_memory_word', '_first_long', '_first_word', '_first_byte', '_first_shift_word', '_first_add_word', 'FirstDeploymentFrame', '_first_sub_word', 'SpritePacketFields', 'first_replace'})
APPROVED.setdefault('domain',set()).add('swap_words')
DECLARATIONS.update({'_selected_group_panel_store_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame, value: Word, offset: Word=0, *, advance: bool=False, clear: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': "uint(value, 16)\nuint(offset, 16)\nif type(advance) is not bool or type(clear) is not bool:\n    raise ValueError('explicit selected-panel write shape required')\nif clear:\n    frame.roster.word(0, offset)\nframe.roster.set_word(0, value, offset)\nframe = memory.sync_status(_first_memory_word(frame, value))\nif advance:\n    frame = first_replace(frame, roster=frame.roster.advance(2))\nreturn frame"}, '_selected_group_panel_cell_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame, far_tile: Word, near_tile: Word', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _selected_group_panel_store_fields(memory, frame, far_tile, 34)\nreturn _selected_group_panel_store_fields(memory, frame, near_tile, advance=True)'}, '_selected_group_panel_amount_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame, offset: Word', 'returns': 'FirstDeploymentFrame', 'flow': "frame = memory.sync_status(_first_byte(frame, 'target_x', frame.candidates.byte(0, offset)))\nframe = memory.sync_status(_first_shift_word(frame, 'target_x', low16(frame.target_x), 8))\nframe = memory.sync_status(_first_byte(frame, 'target_x', frame.candidates.byte(0, offset + 1)))\nfor displacement in (2, 3):\n    previous = frame.target_x\n    value = u32(previous << 8)\n    carry = bool(previous & 1 << 24)\n    status = (17 if carry else 0) | (8 if value & 2147483648 else 0) | (4 if value == 0 else 0)\n    frame = memory.sync_status(first_replace(frame, target_x=value, status=status))\n    frame = memory.sync_status(_first_byte(frame, 'target_x', frame.candidates.byte(0, offset + displacement)))\nreturn frame"}, '_selected_group_panel_decimal_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'memory.frame(frame, True)\nnumeric = DecimalMemory(memory.state, frame.stack_cursor)\ndigit_tile = low16(frame.target_y)\nfields = _six_place_decimal_fields(numeric, frame.target_x, digit_tile, low16(frame.unit), memory.cursor_at(frame.auxiliary.base))\nframe = first_replace(frame, target_x=fields.remainder, count=replace_word(frame.count, fields.divisor), distance=replace_word(frame.distance, fields.started), offset_x=replace_word(frame.offset_x, fields.glyph), auxiliary=fields.destination, stack_cursor=numeric.stack_cursor, status=16 if fields.glyph < digit_tile else 0)\nreturn memory.sync_status(_first_memory_word(frame, fields.glyph))'}, 'append_wide_paired_tiles_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.frame(frame, True)\nfor index in descending_inclusive(low16(frame.target_y)):\n    frame = _selected_group_panel_store_fields(memory, frame, low16(frame.target_x))\n    frame = memory.sync_status(_first_add_word(frame, 'target_x', low16(frame.target_x), 1))\n    frame = _selected_group_panel_store_fields(memory, frame, low16(frame.target_x), 34)\n    frame = memory.sync_status(_first_add_word(frame, 'target_x', low16(frame.target_x), 1))\n    frame = first_replace(frame, roster=frame.roster.advance(2), target_y=replace_word(frame.target_y, u16(low16(frame.target_y) - 1)))\nreturn memory.frame(frame, True)"}, '_selected_group_panel_call_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "memory.frame(frame, True)\ncall = DecimalMemory(memory.state, frame.stack_cursor)\ncall.enter_call(continuation)\nentered = first_replace(frame, stack_cursor=call.stack_cursor)\nif target == 75530:\n    result = _selected_group_panel_decimal_fields(memory, entered)\nelif target == 83832:\n    result = append_wide_paired_tiles_fields(memory, entered)\nelse:\n    raise ValueError('selected panel has no other declared child target')\ncall.stack_cursor = result.stack_cursor\ncall.leave_call(continuation)\nreturn first_replace(result, stack_cursor=call.stack_cursor)"}, '_selected_group_panel_blank_cells_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame, counter: Word', 'returns': 'FirstDeploymentFrame', 'flow': "frame = memory.sync_status(_first_word(frame, 'target_x', counter))\nfor index in descending_inclusive(low16(frame.target_x)):\n    frame = _selected_group_panel_cell_fields(memory, frame, 49153, 49153)\n    frame = first_replace(frame, target_x=replace_word(frame.target_x, u16(low16(frame.target_x) - 1)))\nreturn frame"}, '_selected_group_panel_digits_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = memory.sync_status(_first_word(frame, 'target_x', 5))\nfor index in descending_inclusive(low16(frame.target_x)):\n    glyph = frame.candidates.word()\n    frame = first_replace(frame, candidates=frame.candidates.advance(2))\n    frame = _selected_group_panel_cell_fields(memory, frame, glyph, 49153)\n    frame = first_replace(frame, target_x=replace_word(frame.target_x, u16(low16(frame.target_x) - 1)))\nreturn frame"}, 'append_selected_group_panel_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.frame(frame, True)\nstate = memory.state\nframe = first_replace(frame, candidates=memory.cursor_at(state.read(16726060, 4)))\nframe = _selected_group_panel_amount_fields(memory, frame, 5)\nframe = memory.sync_status(_first_word(frame, 'target_y', 50054))\nframe = memory.sync_status(_first_word(frame, 'unit', 49153))\nframe = first_replace(frame, auxiliary=memory.cursor_at(4294955776))\nframe = _selected_group_panel_call_fields(memory, frame, 75530, 83362)\nframe = _selected_group_panel_amount_fields(memory, frame, 9)\nframe = first_replace(frame, auxiliary=memory.cursor_at(4294955788))\nframe = _selected_group_panel_call_fields(memory, frame, 75530, 83394)\nframe = first_replace(frame, roster=memory.cursor_at(4294955264))\nqueue_offset = state.read(4294963994, 2)\nframe = first_replace(frame, roster=frame.roster.advance(s16(queue_offset)))\nfor tile in (15, 50050, 50048):\n    frame = _selected_group_panel_store_fields(memory, frame, tile, advance=True)\nframe = memory.sync_status(_first_word(frame, 'target_x', 12))\nfor index in descending_inclusive(low16(frame.target_x)):\n    frame = _selected_group_panel_store_fields(memory, frame, 50049, advance=True)\n    frame = first_replace(frame, target_x=replace_word(frame.target_x, u16(low16(frame.target_x) - 1)))\nframe = _selected_group_panel_store_fields(memory, frame, 52096, advance=True)\nfor far_tile, near_tile in ((15, 15), (50306, 50178), (50050, 50050)):\n    frame = _selected_group_panel_cell_fields(memory, frame, far_tile, near_tile)\nframe = memory.sync_status(_first_word(frame, 'target_x', 49225))\nframe = memory.sync_status(_first_word(frame, 'target_y', 5))\nframe = _selected_group_panel_call_fields(memory, frame, 83832, 83472)\nframe = _selected_group_panel_cell_fields(memory, frame, 49153, 49153)\nframe = first_replace(frame, candidates=memory.cursor_at(4294955776))\nframe = _selected_group_panel_digits_fields(memory, frame)\nframe = _selected_group_panel_cell_fields(memory, frame, 52098, 52098)\nframe = first_replace(frame, roster=frame.roster.advance(34))\nfor far_tile, near_tile in ((15, 15), (50690, 50562), (50050, 50050)):\n    frame = _selected_group_panel_cell_fields(memory, frame, far_tile, near_tile)\nframe = memory.sync_status(_first_word(frame, 'target_x', 49237))\nframe = memory.sync_status(_first_word(frame, 'target_y', 3))\nframe = _selected_group_panel_call_fields(memory, frame, 83832, 83558)\nframe = _selected_group_panel_blank_cells_fields(memory, frame, 2)\nframe = _selected_group_panel_digits_fields(memory, frame)\nframe = _selected_group_panel_cell_fields(memory, frame, 52098, 52098)\nframe = first_replace(frame, roster=frame.roster.advance(34))\nfor far_tile, near_tile in ((15, 15), (51074, 50946), (50050, 50050)):\n    frame = _selected_group_panel_cell_fields(memory, frame, far_tile, near_tile)\nframe = memory.sync_status(_first_word(frame, 'target_x', 49245))\nframe = memory.sync_status(_first_word(frame, 'target_y', 5))\nframe = _selected_group_panel_call_fields(memory, frame, 83832, 83648)\nframe = _selected_group_panel_blank_cells_fields(memory, frame, 4)\nframe = memory.sync_status(_first_word(frame, 'target_x', 49153))\nframe = first_replace(frame, controller=memory.cursor_at(state.read(16726060, 4)))\nframe = memory.sync_status(_first_word(frame, 'unit', 0))\nframe = memory.sync_status(_first_byte(frame, 'unit', frame.controller.byte()))\nframe = memory.sync_status(_first_word(frame, 'unit', low16(frame.unit) & 15))\nframe = memory.sync_status(_sprite_compare(frame, low16(frame.unit), 10, 16))\nif not frame.status & 1:\n    frame = memory.sync_status(_first_word(frame, 'target_x', 50055))\n    frame = memory.sync_status(_first_sub_word(frame, 'unit', low16(frame.unit), 10))\nframe = _selected_group_panel_cell_fields(memory, frame, low16(frame.target_x), 49153)\nframe = memory.sync_status(_first_add_word(frame, 'unit', low16(frame.unit), 50054))\nframe = _selected_group_panel_cell_fields(memory, frame, low16(frame.unit), 49153)\nframe = _selected_group_panel_cell_fields(memory, frame, 52098, 52098)\nframe = first_replace(frame, roster=frame.roster.advance(34))\nfor bottom, middle, top in ((15, 15, 15), (51202, 50818, 50434), (54144, 50050, 50050)):\n    frame = _selected_group_panel_store_fields(memory, frame, bottom, 68)\n    frame = _selected_group_panel_store_fields(memory, frame, middle, 34)\n    frame = _selected_group_panel_store_fields(memory, frame, top, advance=True)\nframe = memory.sync_status(_first_word(frame, 'target_x', 12))\nfor index in descending_inclusive(low16(frame.target_x)):\n    frame = _selected_group_panel_store_fields(memory, frame, 54145, 68)\n    frame = _selected_group_panel_store_fields(memory, frame, 49153, 34)\n    frame = _selected_group_panel_store_fields(memory, frame, 49153, advance=True)\n    frame = first_replace(frame, target_x=replace_word(frame.target_x, u16(low16(frame.target_x) - 1)))\nframe = _selected_group_panel_store_fields(memory, frame, 56192, 68)\nframe = _selected_group_panel_store_fields(memory, frame, 52098, 34)\nframe = _selected_group_panel_store_fields(memory, frame, 52098, advance=True)\nframe = _selected_group_panel_store_fields(memory, frame, 0, 68, clear=True)\nprevious = state.read(4294963994, 2)\nstate.write(4294963994, 2, u16(previous + 340))\nchanged = _first_add_word(frame, 'target_x', previous, 340)\nframe = memory.sync_status(first_replace(changed, target_x=frame.target_x))\nreturn memory.frame(frame, True)"}, '_sprite_bit': {'signature': 'frame: FirstDeploymentFrame, attributes: Word, mask: Word',
                 'returns': 'FirstDeploymentFrame',
                 'flow': 'if mask not in (4096, 2048):\n'
                         "    raise ValueError('actual sprite flip bit required')\n"
                         'return first_replace(frame, status=None if frame.status is None else frame.status '
                         '& 27 | (0 if attributes & mask else 4))'},
 '_sprite_compare': {'signature': 'frame: FirstDeploymentFrame, observed, threshold, bits',
                     'returns': 'FirstDeploymentFrame',
                     'flow': 'uint(observed, bits)\n'
                             'uint(threshold, bits)\n'
                             'if bits not in (8, 16):\n'
                             "    raise ValueError('original sprite comparison width required')\n"
                             'mask, sign = ((1 << bits) - 1, 1 << bits - 1)\n'
                             'difference = observed - threshold & mask\n'
                             'status = None if frame.status is None else frame.status & 16 | (1 if observed '
                             '< threshold else 0) | (4 if difference == 0 else 0) | (8 if difference & sign '
                             'else 0) | (2 if (observed ^ threshold) & (observed ^ difference) & sign else '
                             '0)\n'
                             'return first_replace(frame, status=status)'},
 '_sprite_finish': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame, x: Word, y: Word, '
                                 'attributes: Word, observed, threshold, bits',
                    'returns': 'SpritePacketFields',
                    'flow': 'frame = memory.sync_status(_sprite_compare(frame, observed, threshold, bits))\n'
                            'difference = observed - threshold & (1 << bits) - 1\n'
                            'sign = 1 << bits - 1\n'
                            'frame = memory.restore_scratch(frame)\n'
                            'return SpritePacketFields(frame, x, y, attributes, observed < threshold, '
                            'difference == 0, bool(difference & sign), bool((observed ^ threshold) & '
                            '(observed ^ difference) & sign)).validate(memory)'},
 '_sprite_increment_count': {'signature': 'frame: FirstDeploymentFrame, value',
                             'returns': 'FirstDeploymentFrame',
                             'flow': 'uint(value, 8)\n'
                                     'result = u8(value + 1)\n'
                                     'return first_replace(frame, status=(17 if value == 255 else 0) | (8 if '
                                     'result & 128 else 0) | (4 if result == 0 else 0) | (2 if value == 127 '
                                     'else 0))'},
 '_sprite_left_long_four': {'signature': 'frame: FirstDeploymentFrame, value: Long',
                            'returns': 'FirstDeploymentFrame',
                            'flow': 'uint(value, 32)\n'
                                    'shifted = u32(value << 4)\n'
                                    'carry = bool(value & 268435456)\n'
                                    'return first_replace(frame, offset_x=shifted, status=(17 if carry else '
                                    '0) | (8 if shifted & 2147483648 else 0) | (4 if shifted == 0 else 0))'},
 '_sprite_signed_vertical_word': {'signature': 'frame: FirstDeploymentFrame, value: Word',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'uint(value, 16)\n'
                                          'shifted = u16(s16(value) >> 4)\n'
                                          'carry = bool(value & 8)\n'
                                          'return first_replace(frame, offset_x=replace_word(frame.offset_x, '
                                          'shifted), status=(17 if carry else 0) | (8 if shifted & 32768 '
                                          'else 0) | (4 if shifted == 0 else 0))'},
 '_sprite_swap': {'signature': 'frame: FirstDeploymentFrame, name: str',
                  'returns': 'FirstDeploymentFrame',
                  'flow': 'value = swap_words(frame.carrier(name))\nreturn _first_long(frame, name, value)'},
 'append_live_command_sprite_fields': {'signature': 'memory: SpritePacketMemory, frame: '
                                                    'FirstDeploymentFrame, *, reset_scroll: bool=True, '
                                                    'initialize_clip: bool=True',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'memory.frame(frame, True)\n'
                                               'result = append_live_command_sprite_packet_fields(memory, '
                                               'frame, low16(frame.target_x), low16(frame.target_y), '
                                               'low16(frame.unit), reset_scroll=reset_scroll, '
                                               'initialize_clip=initialize_clip)\n'
                                               'return memory.frame(result.frame, True)'},
 'append_live_command_sprite_packet_fields': {'signature': 'memory: SpritePacketMemory, frame: '
                                                           'FirstDeploymentFrame, x: Word, y: Word, '
                                                           'attributes: Word, *, reset_scroll: bool, '
                                                           'initialize_clip: bool',
                                              'returns': 'SpritePacketFields',
                                              'flow': 'if type(memory) is not SpritePacketMemory:\n'
                                                      "    raise ValueError('actual sprite memory "
                                                      "required')\n"
                                                      'memory.frame(frame, frame.stack_cursor is not None)\n'
                                                      'for value in (x, y, attributes):\n'
                                                      '    uint(value, 16)\n'
                                                      'if type(reset_scroll) is not bool or '
                                                      'type(initialize_clip) is not bool:\n'
                                                      "    raise ValueError('explicit original sprite prefix "
                                                      "choices required')\n"
                                                      'if reset_scroll and (not initialize_clip):\n'
                                                      "    raise ValueError('AC08 reset includes clipping "
                                                      "prefix')\n"
                                                      'state = memory.state\n'
                                                      'if reset_scroll:\n'
                                                      '    for address in (4294964746, 4294964750):\n'
                                                      '        state.read(address, 2)\n'
                                                      '        state.write(address, 2, 0)\n'
                                                      '        frame = '
                                                      'memory.sync_status(_first_memory_word(frame, 0))\n'
                                                      'if initialize_clip:\n'
                                                      '    for address, value in ((4294963970, 112), '
                                                      '(4294963972, 352), (4294963974, 112), (4294963976, '
                                                      '448)):\n'
                                                      '        state.write(address, 2, value)\n'
                                                      '        frame = '
                                                      'memory.sync_status(_first_memory_word(frame, value))\n'
                                                      'frame = memory.save_scratch(frame)\n'
                                                      'count = state.read(4294963968, 1)\n'
                                                      'frame = memory.sync_status(_sprite_compare(frame, '
                                                      'count, 80, 8))\n'
                                                      'if count >= 80:\n'
                                                      '    return _sprite_finish(memory, frame, x, y, '
                                                      'attributes, count, 80, 8)\n'
                                                      'attributes &= 63488\n'
                                                      "frame = memory.sync_status(_first_word(frame, 'unit', "
                                                      'attributes))\n'
                                                      "frame = _first_word(frame, 'count', x)\n"
                                                      'scroll_x = state.read(4294964746, 2)\n'
                                                      "frame = _first_sub_word(frame, 'count', x, scroll_x)\n"
                                                      'origin_x = u16(x - scroll_x)\n'
                                                      'frame = memory.sync_status(_first_add_word(frame, '
                                                      "'count', origin_x, 128))\n"
                                                      'origin_x = u16(origin_x + 128)\n'
                                                      "frame = _first_word(frame, 'distance', y)\n"
                                                      'scroll_y = state.read(4294964750, 2)\n'
                                                      "frame = _first_sub_word(frame, 'distance', y, "
                                                      'scroll_y)\n'
                                                      'origin_y = u16(y - scroll_y)\n'
                                                      'frame = memory.sync_status(_first_add_word(frame, '
                                                      "'distance', origin_y, 128))\n"
                                                      'origin_y = u16(origin_y + 128)\n'
                                                      "frame = _first_word(frame, 'offset_x', 0)\n"
                                                      'count = state.read(4294963968, 1)\n'
                                                      "frame = _first_byte(frame, 'offset_x', count)\n"
                                                      'frame = memory.sync_status(_first_shift_word(frame, '
                                                      "'offset_x', count, 3))\n"
                                                      'output = memory.cursor_at(4294965248, u16(count << '
                                                      '3))\n'
                                                      'frame = first_replace(frame, candidates=output)\n'
                                                      'while True:\n'
                                                      '    records = frame.roster\n'
                                                      '    coordinate_x = records.word()\n'
                                                      "    frame = _first_word(frame, 'offset_x', "
                                                      'coordinate_x)\n'
                                                      '    frame = memory.sync_status(_sprite_compare(frame, '
                                                      'coordinate_x, 32768, 16))\n'
                                                      '    if coordinate_x == 32768:\n'
                                                      '        return _sprite_finish(memory, frame, x, y, '
                                                      'attributes, coordinate_x, 32768, 16)\n'
                                                      '    frame = memory.sync_status(_sprite_bit(frame, '
                                                      'attributes, 4096))\n'
                                                      '    if attributes & 4096:\n'
                                                      '        packed_size = records.word(0, 4)\n'
                                                      "        frame = _first_word(frame, 'choice', "
                                                      'packed_size)\n'
                                                      "        frame = _first_long(frame, 'choice', "
                                                      'packed_size)\n'
                                                      "        frame = _first_shift_word(frame, 'choice', "
                                                      'packed_size, 4)\n'
                                                      "        frame = _sprite_swap(frame, 'choice')\n"
                                                      '        correction = low16(frame.choice) & 3\n'
                                                      "        frame = _first_word(frame, 'choice', "
                                                      'correction)\n'
                                                      "        frame = _first_shift_word(frame, 'choice', "
                                                      'correction, 3)\n'
                                                      '        correction = u16(correction << 3)\n'
                                                      "        frame = _first_add_word(frame, 'choice', "
                                                      'correction, 8)\n'
                                                      '        correction = u16(correction + 8)\n'
                                                      "        frame = _first_add_word(frame, 'offset_x', "
                                                      'coordinate_x, correction)\n'
                                                      '        coordinate_x = u16(coordinate_x + '
                                                      'correction)\n'
                                                      "        frame = _first_sub_word(frame, 'offset_x', 0, "
                                                      'coordinate_x)\n'
                                                      '        coordinate_x = u16(-coordinate_x)\n'
                                                      '    frame = memory.sync_status(_first_add_word(frame, '
                                                      "'offset_x', coordinate_x, origin_x))\n"
                                                      '    coordinate_x = u16(coordinate_x + origin_x)\n'
                                                      '    minimum = state.read(4294963970, 2)\n'
                                                      '    frame = memory.sync_status(_sprite_compare(frame, '
                                                      'coordinate_x, minimum, 16))\n'
                                                      '    visible_x = coordinate_x >= minimum\n'
                                                      '    if visible_x:\n'
                                                      '        maximum = state.read(4294963972, 2)\n'
                                                      '        frame = '
                                                      'memory.sync_status(_sprite_compare(frame, '
                                                      'coordinate_x, maximum, 16))\n'
                                                      '        visible_x = coordinate_x < maximum\n'
                                                      '    if visible_x:\n'
                                                      '        output.set_word(0, coordinate_x)\n'
                                                      '        frame = _first_memory_word(frame, '
                                                      'coordinate_x)\n'
                                                      "        frame = _first_long(frame, 'offset_x', 0)\n"
                                                      '        packed_size = records.word(0, 4)\n'
                                                      "        frame = _first_word(frame, 'offset_x', "
                                                      'packed_size)\n'
                                                      '        frame = _sprite_left_long_four(frame, '
                                                      'packed_size)\n'
                                                      '        frame = _sprite_signed_vertical_word(frame, '
                                                      'low16(frame.offset_x))\n'
                                                      '        packed = frame.offset_x\n'
                                                      '        coordinate_y = low16(packed)\n'
                                                      "        frame = _first_long(frame, 'offset_y', "
                                                      'packed)\n'
                                                      '        frame = memory.sync_status(_sprite_bit(frame, '
                                                      'attributes, 2048))\n'
                                                      '        if attributes & 2048:\n'
                                                      "            frame = _first_long(frame, 'choice', "
                                                      'packed)\n'
                                                      "            frame = _sprite_swap(frame, 'choice')\n"
                                                      '            correction = low16(frame.choice) & 12\n'
                                                      "            frame = _first_word(frame, 'choice', "
                                                      'correction)\n'
                                                      '            frame = _first_shift_word(frame, '
                                                      "'choice', correction, 1)\n"
                                                      '            correction = u16(correction << 1)\n'
                                                      "            frame = _first_add_word(frame, 'choice', "
                                                      'correction, 8)\n'
                                                      '            correction = u16(correction + 8)\n'
                                                      '            frame = _first_add_word(frame, '
                                                      "'offset_x', coordinate_y, correction)\n"
                                                      '            coordinate_y = u16(coordinate_y + '
                                                      'correction)\n'
                                                      '            frame = _first_sub_word(frame, '
                                                      "'offset_x', 0, coordinate_y)\n"
                                                      '            coordinate_y = u16(-coordinate_y)\n'
                                                      '        frame = '
                                                      "memory.sync_status(_first_add_word(frame, 'offset_x', "
                                                      'coordinate_y, origin_y))\n'
                                                      '        coordinate_y = u16(coordinate_y + origin_y)\n'
                                                      '        minimum = state.read(4294963974, 2)\n'
                                                      '        frame = '
                                                      'memory.sync_status(_sprite_compare(frame, '
                                                      'coordinate_y, minimum, 16))\n'
                                                      '        visible_y = coordinate_y >= minimum\n'
                                                      '        if visible_y:\n'
                                                      '            maximum = state.read(4294963976, 2)\n'
                                                      '            frame = '
                                                      'memory.sync_status(_sprite_compare(frame, '
                                                      'coordinate_y, maximum, 16))\n'
                                                      '            visible_y = coordinate_y < maximum\n'
                                                      '        if visible_y:\n'
                                                      '            output.set_word(0, coordinate_y, 6)\n'
                                                      '            frame = _first_memory_word(frame, '
                                                      'coordinate_y)\n'
                                                      "            frame = _sprite_swap(frame, 'offset_y')\n"
                                                      '            size = low16(frame.offset_y)\n'
                                                      '            frame = _first_shift_word(frame, '
                                                      "'offset_y', size, 8)\n"
                                                      '            size = u16(size << 8)\n'
                                                      '            output.set_word(0, size, 2)\n'
                                                      '            frame = _first_memory_word(frame, size)\n'
                                                      '            count = state.read(4294963968, 1)\n'
                                                      '            frame = '
                                                      'memory.sync_status(_sprite_compare(frame, count, 0, '
                                                      '8))\n'
                                                      '            if count != 0:\n'
                                                      '                count = state.read(4294963968, 1)\n'
                                                      '                output.set_byte(0, count, -5)\n'
                                                      '                frame = '
                                                      'memory.sync_status(_sprite_compare(frame, count, 0, '
                                                      '8))\n'
                                                      '            count = state.read(4294963968, 1)\n'
                                                      '            state.write(4294963968, 1, u8(count + '
                                                      '1))\n'
                                                      '            frame = '
                                                      'memory.sync_status(_sprite_increment_count(frame, '
                                                      'count))\n'
                                                      '            tile = records.word(0, 2)\n'
                                                      "            frame = _first_word(frame, 'offset_x', "
                                                      'tile)\n'
                                                      '            tile = u16(tile ^ attributes)\n'
                                                      "            frame = _first_word(frame, 'offset_x', "
                                                      'tile)\n'
                                                      '            output.set_word(0, tile, 4)\n'
                                                      '            frame = '
                                                      'memory.sync_status(_first_memory_word(frame, tile))\n'
                                                      '            output = output.advance(8)\n'
                                                      '            frame = first_replace(frame, '
                                                      'candidates=output)\n'
                                                      '    frame = first_replace(frame, '
                                                      'roster=records.advance(6))\n'
                                                      '    count = state.read(4294963968, 1)\n'
                                                      '    frame = memory.sync_status(_sprite_compare(frame, '
                                                      'count, 80, 8))\n'
                                                      '    if count >= 80:\n'
                                                      '        return _sprite_finish(memory, frame, x, y, '
                                                      'attributes, count, 80, 8)'},
 'append_live_command_string_words': {'signature': 'state: GameState, source: Table, x: Word, y: Word, '
                                                   'attributes: Word=0, reset_scroll: bool=True',
                                      'returns': 'SpriteAppendResult',
                                      'flow': 'checked_state(state)\n'
                                              'checked_table(source, state)\n'
                                              'result = '
                                              'append_live_command_sprite_packet_fields(SpritePacketMemory(state), '
                                              'first_replace(FirstDeploymentFrame.unobserved(), '
                                              'roster=source.cursor()), x, y, attributes, '
                                              'reset_scroll=reset_scroll, initialize_clip=True)\n'
                                              'return SpriteAppendResult(result.frame.roster, '
                                              'result.attributes)'}})

DECLARATIONS.update({'_route_command_emit_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame, address: Long, value: Long, width: int=2, clear: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': "if width not in (1, 2) or type(clear) is not bool:\n    raise ValueError('original route command BYTE/WORD store required')\nvalue &= (1 << width * 8) - 1\nif clear:\n    memory.state.read(u32(address), width)\nmemory.state.write(u32(address), width, value)\nreturn _movement_test(memory.state, frame, value, width * 8)"}, '_route_command_memory_delta_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame, address: Long, amount: Word, subtract: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': 'frame, value = _movement_binary_flags(memory.state, frame, memory.state.read(address, 2), amount, 16, subtract)\nmemory.state.write(address, 2, value)\nreturn frame'}, '_route_command_call_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "uint(target, 32)\nuint(continuation, 32)\nallowed = ((44048, 82254), (44040, 84308), (83298, 83196), (82634, 82316), (82634, 82388), (82634, 82460), (82634, 82526), (82580, 82636), (82594, 82588))\nif (target, continuation) not in allowed:\n    raise ValueError('original route/menu child and physical continuation required')\nmemory.frame(frame, True)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = first_replace(frame, stack_cursor=stack)\nif target in (44040, 44048):\n    returned = append_live_command_sprite_fields(memory, entered, reset_scroll=target == 44040, initialize_clip=True)\nelif target == 83298:\n    returned = append_short_paired_tiles_fields(memory, entered)\nelif target == 82634:\n    returned = query_route_move_cost_fields(memory, entered)\nelif target == 82580:\n    returned = query_scaled_route_terrain_fields(memory, entered)\nelse:\n    from ..high_level_remaining_flows.business_city import terrain_cell_query_fields\n    returned = terrain_cell_query_fields(memory.state, entered)\nmemory.frame(returned, True)\nactual = returned.stack_cursor.long()\nif actual != continuation:\n    raise FirstDeploymentReturnBoundary(actual, returned, continuation)\nreturn first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))"}, 'execute_city_group_display_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame, target: Long', 'returns': 'FirstDeploymentFrame', 'flow': "uint(target, 32)\nmemory.frame(frame, True)\nchildren = {82182: append_route_selection_pair_fields, 82208: append_route_cursor_sprite_fields, 82282: step_world_route_cursor_fields, 82580: query_scaled_route_terrain_fields, 82634: query_route_move_cost_fields, 83092: append_candidate_member_panel_fields, 83298: append_short_paired_tiles_fields, 84132: step_candidate_selection_cursor_fields, 84244: append_candidate_selection_sprite_fields, 84384: collect_group_members_below_capacity_fields, 85116: clear_world_group_selection_marks_fields}\nif target not in children:\n    raise ValueError('closed full-frame route/candidate software entry required')\nreturn children[target](memory, frame)"}, 'append_route_selection_pair_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'memory.frame(frame, True)\nframe = first_replace(frame, roster=memory.cursor_at(4294942464))\nwhile True:\n    value = frame.roster.word()\n    frame = first_replace(frame, roster=frame.roster.advance(2))\n    frame = _movement_test(memory.state, frame, value, 16)\n    if frame.status & 8:\n        break\nframe = _route_command_emit_fields(memory, frame, u32(frame.roster.base - 2), memory.state.read(4294964062, 2))\nframe = _route_command_emit_fields(memory, frame, frame.roster.base, memory.state.read(4294964064, 2))\nreturn _route_command_emit_fields(memory, frame, u32(frame.roster.base + 2), 65535)'}, 'append_route_cursor_sprite_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_gameplay import _map_presentation_bit_fields\nmemory.frame(frame, True)\nframe = _map_presentation_bit_fields(memory.state, frame, memory.state.read(4294964001, 1), 4)\nif not frame.status & 4:\n    return frame\nframe = first_replace(frame, roster=memory.cursor_at(82256))\nframe = _movement_move(memory.state, frame, 'target_x', memory.state.read(16726050, 2), 16)\nframe = _movement_move(memory.state, frame, 'target_y', memory.state.read(16726052, 2), 16)\nframe = _movement_move(memory.state, frame, 'unit', 0, 16)\nframe = _route_command_emit_fields(memory, frame, 4294964746, memory.state.read(4294963988, 2))\nframe = _route_command_emit_fields(memory, frame, 4294964750, memory.state.read(4294963992, 2))\nreturn _route_command_call_fields(memory, frame, 44048, 82254)"}, 'step_world_route_cursor_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_gameplay import _map_presentation_bit_fields\nmemory.frame(frame, True)\nstate = memory.state\nframe = _movement_move(state, frame, 'distance', state.read(4294964738, 2), 16)\nselected = 0\nfor mask, direction in ((1, 1), (8, 2), (2, 3), (4, 4)):\n    frame = _map_presentation_bit_fields(state, frame, frame.distance, mask)\n    if not frame.status & 4:\n        selected = direction\n        break\nif selected == 0:\n    return frame\nif selected == 1:\n    frame = _movement_move(state, frame, 'target_x', state.read(16726050, 2), 16)\n    if frame.status & 4:\n        return frame\n    frame, coordinate = _movement_binary_flags(state, frame, low16(frame.target_x), 16, 16, True)\n    frame = first_replace(frame, target_x=replace_word(frame.target_x, coordinate))\n    frame = _movement_move(state, frame, 'target_y', state.read(16726052, 2), 16)\n    continuation = 82316\nelif selected == 2:\n    frame = _movement_compare(state, frame, state.read(16726052, 2), 1104, 16)\n    if not frame.status & 1:\n        return frame\n    frame = _movement_move(state, frame, 'target_x', state.read(16726050, 2), 16)\n    frame = _movement_move(state, frame, 'target_y', state.read(16726052, 2), 16)\n    frame = _movement_add_word(state, frame, 'target_y', 16)\n    continuation = 82388\nelif selected == 3:\n    frame = _movement_compare(state, frame, state.read(16726050, 2), 1136, 16)\n    if not frame.status & 1:\n        return frame\n    frame = _movement_move(state, frame, 'target_x', state.read(16726050, 2), 16)\n    frame = _movement_add_word(state, frame, 'target_x', 16)\n    frame = _movement_move(state, frame, 'target_y', state.read(16726052, 2), 16)\n    continuation = 82460\nelse:\n    frame = _movement_move(state, frame, 'target_y', state.read(16726052, 2), 16)\n    if frame.status & 4:\n        return frame\n    frame, coordinate = _movement_binary_flags(state, frame, low16(frame.target_y), 16, 16, True)\n    frame = first_replace(frame, target_y=replace_word(frame.target_y, coordinate))\n    frame = _movement_move(state, frame, 'target_x', state.read(16726050, 2), 16)\n    continuation = 82526\nframe = _route_command_call_fields(memory, frame, 82634, continuation)\nframe = _movement_test(state, frame, low16(frame.count), 16)\nif frame.status & 8:\n    return frame\nframe = _movement_move(state, frame, 'distance', state.read(4294964852, 2), 16)\nframe, budget = _movement_binary_flags(state, frame, low16(frame.distance), low16(frame.count), 16, True)\nframe = first_replace(frame, distance=replace_word(frame.distance, budget))\nif frame.status & 1:\n    return frame\nframe = _route_command_emit_fields(memory, frame, 4294964852, low16(frame.distance))\ncoordinate_address = 16726050 if selected in (1, 3) else 16726052\ncoordinate_value = low16(frame.target_x) if selected in (1, 3) else low16(frame.target_y)\nframe = _route_command_emit_fields(memory, frame, coordinate_address, coordinate_value)\nframe = _movement_move(state, frame, 'target_y', selected, 16)\nframe = first_replace(frame, roster=memory.cursor_at(16726016))\nframe = _movement_move(state, frame, 'target_x', state.read(16726048, 2), 16)\nframe = _route_command_emit_fields(memory, frame, frame.roster.address(low16(frame.target_x)), low8(frame.target_y), 1)\nreturn _route_command_memory_delta_fields(memory, frame, 16726048, 1)"}, 'query_scaled_route_terrain_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.frame(frame, True)\nframe = _movement_fixed_shift_word(memory.state, frame, 'target_x', 4, True)\nframe = _movement_fixed_shift_word(memory.state, frame, 'target_y', 4, True)\nframe = _route_command_call_fields(memory, frame, 82594, 82588)\nframe = _movement_fixed_shift_word(memory.state, frame, 'target_x', 4)\nreturn _movement_fixed_shift_word(memory.state, frame, 'target_y', 4)"}, 'query_route_move_cost_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'memory.frame(frame, True)\nframe = _route_command_call_fields(memory, frame, 82580, 82636)\nreturn _movement_test(memory.state, frame, low16(frame.count), 16)'}, 'append_candidate_member_panel_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_gameplay import _map_presentation_db_fields\nmemory.frame(frame, True)\nstate = memory.state\nframe = first_replace(frame, roster=memory.cursor_at(4294955264))\nframe = first_replace(frame, roster=frame.roster.advance(s16(state.read(4294963994, 2))))\nfor tile in (6, 49954, 50048, 50049, 50049, 50049, 50049, 52096):\n    frame = _selected_group_panel_store_fields(memory, frame, tile, advance=True)\nframe = first_replace(frame, candidates=memory.cursor_at(16726320))\nframe = _movement_move(state, frame, 'unit', 50082, 16)\nwhile True:\n    frame = _selected_group_panel_store_fields(memory, frame, 6, 16)\n    frame = _selected_group_panel_store_fields(memory, frame, 6, advance=True)\n    frame = _selected_group_panel_store_fields(memory, frame, low16(frame.unit))\n    frame = _movement_add_word(state, frame, 'unit', 128)\n    frame = _selected_group_panel_store_fields(memory, frame, low16(frame.unit), 16)\n    frame = _movement_add_word(state, frame, 'unit', 128)\n    frame = first_replace(frame, roster=frame.roster.advance(2))\n    frame = _selected_group_panel_store_fields(memory, frame, 50050, 16)\n    frame = _selected_group_panel_store_fields(memory, frame, 50050, advance=True)\n    frame = _movement_move(state, frame, 'target_x', 0, 16)\n    frame = _movement_move(state, frame, 'target_x', frame.candidates.byte(), 8)\n    frame = first_replace(frame, candidates=frame.candidates.advance(1))\n    frame = _movement_fixed_shift_word(state, frame, 'target_x', 3)\n    frame = _movement_add_word(state, frame, 'target_x', 49177)\n    frame = _movement_move(state, frame, 'target_y', 3, 16)\n    frame = _route_command_call_fields(memory, frame, 83298, 83196)\n    frame = _selected_group_panel_store_fields(memory, frame, 52098, 16)\n    frame = _selected_group_panel_store_fields(memory, frame, 52098, advance=True)\n    frame = first_replace(frame, roster=frame.roster.advance(16))\n    frame = _route_command_memory_delta_fields(memory, frame, 4294963994, 16)\n    frame = _movement_test(state, frame, frame.candidates.byte(), 8)\n    if frame.status & 8:\n        break\n    frame = _selected_group_panel_store_fields(memory, frame, 6, advance=True)\n    frame = _selected_group_panel_store_fields(memory, frame, low16(frame.unit), advance=True)\n    frame = _movement_add_word(state, frame, 'unit', 128)\n    frame = _selected_group_panel_store_fields(memory, frame, 50050, advance=True)\n    frame = _movement_move(state, frame, 'target_x', 3, 16)\n    while True:\n        frame = _selected_group_panel_store_fields(memory, frame, 49153, advance=True)\n        frame, more = _map_presentation_db_fields(frame, 'target_x')\n        if not more:\n            break\n    frame = _selected_group_panel_store_fields(memory, frame, 52098, advance=True)\n    frame = _route_command_memory_delta_fields(memory, frame, 4294963994, 16)\nfor tile in (6, low16(frame.unit), 54144, 54145, 54145, 54145, 54145, 56192):\n    frame = _selected_group_panel_store_fields(memory, frame, tile, advance=True)\nframe = _selected_group_panel_store_fields(memory, frame, 0, clear=True)\nreturn _route_command_memory_delta_fields(memory, frame, 4294963994, 32)"}, 'append_short_paired_tiles_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_gameplay import _map_presentation_db_fields\nmemory.frame(frame, True)\nwhile True:\n    frame = _selected_group_panel_store_fields(memory, frame, low16(frame.target_x))\n    frame = _movement_adjust_word(memory.state, frame, 'target_x', 1)\n    frame = _selected_group_panel_store_fields(memory, frame, low16(frame.target_x), 16)\n    frame = _movement_adjust_word(memory.state, frame, 'target_x', 1)\n    frame = first_replace(frame, roster=frame.roster.advance(2))\n    frame, more = _map_presentation_db_fields(frame, 'target_y')\n    if not more:\n        return frame"}, 'step_candidate_selection_cursor_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_gameplay import _map_presentation_bit_fields\nmemory.frame(frame, True)\nstate = memory.state\nframe = _movement_move(state, frame, 'target_x', state.read(4294964738, 1), 8)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 3, 16)\nif frame.status & 4:\n    return _route_command_emit_fields(memory, frame, 4294964744, 1)\nframe = _route_command_memory_delta_fields(memory, frame, 4294964744, 1, True)\nif not frame.status & 4:\n    return frame\nframe = _route_command_emit_fields(memory, frame, 4294964744, 12)\nframe = _map_presentation_bit_fields(state, frame, frame.target_x, 2)\nif not frame.status & 4:\n    frame = _movement_move(state, frame, 'target_x', state.read(4294964854, 2), 16)\n    frame = _movement_adjust_word(state, frame, 'target_x', 1)\n    frame = first_replace(frame, roster=memory.cursor_at(16726320))\n    frame = _movement_test(state, frame, frame.roster.byte(low16(frame.target_x)), 8)\n    if frame.status & 8:\n        return _route_command_emit_fields(memory, frame, 4294964854, 0, clear=True)\n    return _route_command_emit_fields(memory, frame, 4294964854, low16(frame.target_x))\nframe = _movement_test(state, frame, state.read(4294964854, 2), 16)\nif not frame.status & 4:\n    return _route_command_memory_delta_fields(memory, frame, 4294964854, 1, True)\nframe = first_replace(frame, roster=memory.cursor_at(16726320))\nframe = _movement_move(state, frame, 'target_x', 0, 16)\nwhile True:\n    frame = _movement_test(state, frame, frame.roster.byte(low16(frame.target_x), 1), 8)\n    if frame.status & 8:\n        return _route_command_emit_fields(memory, frame, 4294964854, low16(frame.target_x))\n    frame = _movement_adjust_word(state, frame, 'target_x', 1)"}, 'append_candidate_selection_sprite_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_gameplay import _map_presentation_bit_fields\nmemory.frame(frame, True)\nstate = memory.state\nframe = _map_presentation_bit_fields(state, frame, state.read(4294964739, 1), 32)\nif not frame.status & 4:\n    return frame\nframe = _movement_move(state, frame, 'target_x', state.read(4294964738, 1), 8)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 3, 16)\nif frame.status & 4:\n    frame = _map_presentation_bit_fields(state, frame, state.read(4294964001, 1), 8)\n    if not frame.status & 4:\n        return frame\nframe = first_replace(frame, roster=memory.cursor_at(84310))\nframe = _movement_move(state, frame, 'target_x', state.read(4294964854, 2), 16)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_x', 1)\nframe = _movement_add_word(state, frame, 'target_x', low16(frame.target_y))\nframe = _movement_fixed_shift_word(state, frame, 'target_x', 3)\nframe = _movement_add_word(state, frame, 'target_x', 48)\nframe = _movement_move(state, frame, 'target_y', 136, 16)\nframe = _movement_move(state, frame, 'unit', 0, 16)\nreturn _route_command_call_fields(memory, frame, 44040, 84308)"}, 'collect_group_members_below_capacity_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_gameplay import _map_presentation_db_fields\nmemory.frame(frame, True)\nstate = memory.state\nframe = first_replace(frame, roster=memory.cursor_at(4294946816), candidates=memory.cursor_at(4294947328), controller=memory.cursor_at(state.read(16726060, 4)))\nframe = _movement_move(state, frame, 'unit', frame.controller.byte(), 8)\nframe = _movement_move(state, frame, 'unit', low16(frame.unit) & 15, 16)\nframe = _movement_adjust_word(state, frame, 'unit', -1)\nframe = first_replace(frame, controller=frame.controller.advance(13), scan=memory.cursor_at(4294964480))\nframe = _movement_move(state, frame, 'target_x', 0, 16)\nwhile True:\n    frame = _movement_move(state, frame, 'target_y', 0, 16)\n    frame = _movement_move(state, frame, 'target_y', frame.controller.byte(), 8)\n    frame = first_replace(frame, controller=frame.controller.advance(1))\n    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)\n    frame = _movement_move(state, frame, 'count', frame.roster.word(low16(frame.target_y)), 16)\n    frame = _movement_compare(state, frame, low16(frame.count), frame.candidates.word(low16(frame.target_y)), 16)\n    if not frame.status & 4:\n        frame = _movement_fixed_shift_word(state, frame, 'target_y', 1, True)\n        frame = _route_command_emit_fields(memory, frame, frame.scan.base, low16(frame.target_y))\n        frame = first_replace(frame, scan=frame.scan.advance(2))\n        frame = _movement_adjust_word(state, frame, 'target_x', 1)\n    frame, more = _map_presentation_db_fields(frame, 'unit')\n    if not more:\n        break\nframe = _route_command_emit_fields(memory, frame, frame.scan.base, 65535)\nreturn _route_command_emit_fields(memory, frame, 4294964790, low16(frame.target_x))"}, 'clear_world_group_selection_marks_fields': {'signature': 'memory: SpritePacketMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_gameplay import _map_presentation_bit_fields\nmemory.frame(frame, True)\nstate = memory.state\nframe = _route_command_emit_fields(memory, frame, 4294964054, state.read(4294963988, 2))\nframe = _route_command_emit_fields(memory, frame, 4294964052, state.read(4294963992, 2))\nframe = first_replace(frame, roster=memory.cursor_at(4294938624))\nwhile True:\n    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)\n    frame = _map_presentation_bit_fields(state, frame, frame.target_x, 16)\n    frame = first_replace(frame, target_x=frame.target_x & ~16)\n    frame = _route_command_emit_fields(memory, frame, frame.roster.base, low8(frame.target_x), 1)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)\n    if frame.status & 4:\n        return frame\n    frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.target_x)) + 13))"}})
APPROVED.setdefault((2, 'high_level_main_flows.business_movement_support'), set()).update(('_movement_move', '_movement_test', '_movement_compare', '_movement_fixed_shift_word', '_movement_add_word', '_movement_adjust_word', '_movement_binary_flags'))
APPROVED.setdefault((2, 'high_level_main_flows.business_gameplay'), set()).update(('_map_presentation_bit_fields', '_map_presentation_db_fields'))
APPROVED.setdefault((2, 'high_level_main_flows.contexts_gameplay'), set()).update(('FirstDeploymentReturnBoundary',))
APPROVED.setdefault((2, 'high_level_remaining_flows.business_city'), set()).update(('terrain_cell_query_fields',))
