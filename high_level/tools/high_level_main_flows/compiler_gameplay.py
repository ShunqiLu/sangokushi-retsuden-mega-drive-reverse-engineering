"""Restricted business-text admission and ordinary mnemonic lowering.
An intermediate fixed-structure compiler, not arbitrary Python or CPU proof.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import BUSINESS_GAMEPLAY_BINDINGS

APPROVED={'business_commands': {'present_current_command_prompt', 'present_current_command_prompt_frame_fields'},
 'business_lowbank': {'draw_current_resource_glyphs'},
 'business_scene_support': {'cycle_second_player_choice', 'cycle_third_player_choice'},
 'contexts_commands': {'PresentCurrentCommandPromptInput'},
 'contexts_gameplay': {'BattlePolicy',
                       'GameplayCall',
                       'MapPresentation',
                       'ProjectValues',
                       'SetupPlane',
                       'SetupValues',
                       'TargetSearch',
                       'checked_context'},
 'contexts_lowbank': {'DrawCurrentResourceGlyphsInput'},
 'dataclasses': {'replace'},
 'domain': {'Boundary',
            'Cursor',
            'Long',
            'SceneState',
            'Table',
            'VideoPlaneAddress',
            'Word',
            'checked_state',
            'data_view',
            'descending_inclusive',
            'divu_retained',
            'low16',
            'low8',
            'negative_byte',
            'negative_word',
            'ram_view',
            'replace_byte',
            'replace_word',
            's16',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'},
 'services': {'append_map_sprites',
              'append_six_place_decimal_value',
              'append_six_place_decimal_fields',
              'award_defense_progress',
              'call_target',
              'clear_completed_monthly_actions',
              'decode_glyph_rows_to_buffers',
              'query_scaled_terrain',
              'refresh_gameplay_scene',
              'sample_random_pair'}}

DECLARATIONS={'_ram': {'signature': 'state, name', 'returns': None, 'flow': "return ram_view(state, 'ram_' + name)"},
 '_word': {'signature': 'state, name', 'returns': None, 'flow': 'return _ram(state, name).word()'},
 '_put': {'signature': 'state, name, value',
          'returns': None,
          'flow': '_ram(state, name).set_word(0, low16(value))'},
 '_call': {'signature': 'state, target, operands, continuation',
           'returns': None,
           'flow': 'from .services import call_target\n'
                   'result = call_target(state, u32(target), GameplayCall(operands, continuation))\n'
                   'if type(result) is not type(operands):\n'
                   "    raise Boundary('real gameplay call must return its declared operands')\n"
                   'return result.validate(state)'},
 '_indexed_call': {'signature': 'state, operands, selector, parameters, branch_base, continuation',
                   'returns': None,
                   'flow': 'displacement = data_view(state, parameters).word(low16(selector))\n'
                           'target = u32(branch_base + s16(displacement))\n'
                           'return _call(state, target, operands, continuation)'},
 '_project_order': {'signature': 'state, values, name',
                    'returns': None,
                    'flow': 'orders = _ram(state, name)\n'
                            "city = replace_word(values.city_index, _word(state, 'f364'))\n"
                            'city = replace_word(city, u16(low16(city) << 1))\n'
                            "city = replace_word(city, u16(low16(city) + _word(state, 'f364')))\n"
                            'city = replace_word(city, u16(low16(city) << 2))\n'
                            'officer = u32(s16(orders.word(low16(city))))\n'
                            'budget = u32(s16(orders.word(low16(city), displacement=2)))\n'
                            'return replace(values, city_index=city, officer=officer, budget=budget, '
                            'orders=orders)'},
 '_cancel_project': {'signature': 'values',
                     'returns': None,
                     'flow': 'values.orders.set_word(low16(values.city_index), 65535)\n'
                             'values.task_flags.byte(low16(values.officer))\n'
                             'values.task_flags.set_byte(low16(values.officer), 0)\n'
                             'return values'},
 '_pay_project': {'signature': 'state, values',
                  'returns': None,
                  'flow': "record = replace_word(values.record_index, u16(_word(state, 'f364') << 2))\n"
                          "gold = _ram(state, 'dffc')\n"
                          'value = gold.long(low16(record))\n'
                          'borrow = value < values.budget\n'
                          'value = u32(value - values.budget)\n'
                          'values = replace(values, record_index=record, value=value)\n'
                          'if not borrow:\n'
                          '    gold.set_long(low16(record), value)\n'
                          'return (values, borrow)'},
 '_project_aptitude': {'signature': 'state, values',
                       'returns': None,
                       'flow': 'value = divu_retained(values.budget, 5)\n'
                               'record = replace_word(values.record_index, u16(low16(values.officer) << '
                               '1))\n'
                               'value = replace_word(value, u16(low16(value) + _ram(state, '
                               "'b600').word(low16(record))))\n"
                               "record = replace_word(record, _ram(state, 'be00').word(low16(record)) "
                               '>> 1)\n'
                               'value = replace_word(value, u16(low16(value) + low16(record)))\n'
                               'return replace(values, value=value, record_index=record, '
                               "orders=_ram(state, 'be00'))"},
 '_reward_project_intellect': {'signature': 'state, values',
                               'returns': None,
                               'flow': 'officer = u32(values.officer << 1)\n'
                                       "intellect = _ram(state, 'be00')\n"
                                       'city = replace_word(values.city_index, '
                                       'intellect.word(low16(officer)))\n'
                                       'city = replace_word(city, u16(low16(city) + '
                                       'low16(values.value)))\n'
                                       'if low16(city) > 999:\n'
                                       '    city = replace_word(city, 999)\n'
                                       'intellect.set_word(low16(officer), low16(city))\n'
                                       'return replace(values, officer=officer, city_index=city, '
                                       'orders=intellect)'},
 'settle_first_city_project': {'signature': 'state: SceneState, values: ProjectValues',
                               'returns': 'ProjectValues',
                               'flow': 'from .services import sample_random_pair\n'
                                       'checked_context(values, ProjectValues, state)\n'
                                       "values = _project_order(state, values, 'e80c')\n"
                                       'if negative_word(low16(values.officer)):\n'
                                       '    return values\n'
                                       'values = replace(values, value=replace_byte(values.value, '
                                       'values.assignments.byte(low16(values.officer))))\n'
                                       "if low8(values.value) != _ram(state, 'f365').byte():\n"
                                       '    return _cancel_project(values)\n'
                                       'values, borrow = _pay_project(state, values)\n'
                                       'if borrow:\n'
                                       '    return _cancel_project(values)\n'
                                       'values = _project_aptitude(state, values)\n'
                                       'random = sample_random_pair(state)\n'
                                       'city = random.sample & 65535\n'
                                       'record = city\n'
                                       'city = swap_words(u32(city * 6))\n'
                                       'city = replace_word(city, u16(low16(city) + 10))\n'
                                       'value = divu_retained(u32(low16(values.value) * low16(city)), '
                                       '1000)\n'
                                       'value = u32(s16(low16(value)))\n'
                                       "record = replace_word(record, u16(_word(state, 'f364') << 2))\n"
                                       "field = _ram(state, 'e1dc')\n"
                                       'budget = u32(field.long(low16(record)) + value)\n'
                                       'if budget > 999:\n'
                                       '    budget = replace_word(budget, 999)\n'
                                       'field.set_long(low16(record), budget)\n'
                                       'return _reward_project_intellect(state, replace(values, '
                                       'city_index=city, record_index=record, budget=budget, '
                                       'value=value))'},
 'settle_second_city_project': {'signature': 'state: SceneState, values: ProjectValues',
                                'returns': 'ProjectValues',
                                'flow': 'from .services import sample_random_pair\n'
                                        'checked_context(values, ProjectValues, state)\n'
                                        "values = _project_order(state, values, 'e810')\n"
                                        'if negative_word(low16(values.officer)):\n'
                                        '    return values\n'
                                        'values = replace(values, value=replace_byte(values.value, '
                                        'values.assignments.byte(low16(values.officer))))\n'
                                        "if low8(values.value) != _ram(state, 'f365').byte():\n"
                                        '    return _cancel_project(values)\n'
                                        'values, borrow = _pay_project(state, values)\n'
                                        'if borrow:\n'
                                        '    return _cancel_project(values)\n'
                                        'values = _project_aptitude(state, values)\n'
                                        'city = swap_words(u32((sample_random_pair(state).sample & '
                                        '65535) << 2))\n'
                                        'scale = replace_word(values.scale, 8)\n'
                                        'offset = replace_word(values.city_offset, u16(_word(state, '
                                        "'f364') << 2))\n"
                                        "field = _ram(state, 'e31c')\n"
                                        'if field.long(low16(offset)) >= 80:\n'
                                        '    scale = replace_word(scale, 2)\n'
                                        'city = replace_word(city, u16(low16(city) + low16(scale)))\n'
                                        'value = u32(low16(values.value) * low16(city))\n'
                                        'city = replace_byte(replace_word(city, 0), _ram(state, '
                                        "'c200').byte(low16(values.officer)))\n"
                                        'record = u32(low16(value) * low16(city))\n'
                                        'value = swap_words(u32(low16(swap_words(value)) * '
                                        'low16(city)))\n'
                                        'value = divu_retained(u32(value + record), 60000)\n'
                                        'value = u32(s16(low16(value)))\n'
                                        "record = replace_word(record, u16(_word(state, 'f364') << 2))\n"
                                        'city = u32(field.long(low16(record)) + value)\n'
                                        'if low16(city) > 100:\n'
                                        '    city = replace_word(city, 100)\n'
                                        'field.set_long(low16(record), city)\n'
                                        'result = _reward_project_intellect(state, replace(values, '
                                        'city_index=city, record_index=record, value=value, '
                                        'scale=scale, city_offset=offset))\n'
                                        'if low16(value) >= 5:\n'
                                        '    officer = replace_word(result.officer, '
                                        'low16(result.officer) >> 1)\n'
                                        '    city = replace_byte(result.city_index, _ram(state, '
                                        "'c200').byte(low16(officer)))\n"
                                        '    city = replace_word(city, u16(low16(city) + 1))\n'
                                        '    if low16(city) <= 100:\n'
                                        "        _ram(state, 'c200').set_byte(low16(officer), "
                                        'low8(city))\n'
                                        '    result = replace(result, officer=officer, '
                                        "city_index=city, orders=_ram(state, 'c200'))\n"
                                        'return result'},
 'settle_third_city_project': {'signature': 'state: SceneState, values: ProjectValues',
                               'returns': 'ProjectValues',
                               'flow': 'from .services import sample_random_pair\n'
                                       'checked_context(values, ProjectValues, state)\n'
                                       "values = _project_order(state, values, 'e814')\n"
                                       'if negative_word(low16(values.officer)):\n'
                                       '    return values\n'
                                       'values = replace(values, value=replace_byte(values.value, '
                                       'values.assignments.byte(low16(values.officer))))\n'
                                       "if low8(values.value) != _ram(state, 'f365').byte():\n"
                                       '    return _cancel_project(values)\n'
                                       'values = replace(values, budget=u32(low16(values.budget) * '
                                       '100))\n'
                                       'values, borrow = _pay_project(state, values)\n'
                                       'if borrow:\n'
                                       '    return _cancel_project(values)\n'
                                       'budget = divu_retained(values.budget, 50)\n'
                                       'record = replace_word(values.record_index, '
                                       'u16(low16(values.officer) << 1))\n'
                                       'budget = replace_word(budget, u16(low16(budget) + _ram(state, '
                                       "'b600').word(low16(record))))\n"
                                       'value = replace_word(values.value, _ram(state, '
                                       "'be00').word(low16(record)) >> 2)\n"
                                       'budget = replace_word(budget, u16(low16(budget) + '
                                       'low16(value)))\n'
                                       'value = replace_word(value, _ram(state, '
                                       "'c000').word(low16(record)) >> 2)\n"
                                       'budget = replace_word(budget, u16(low16(budget) + '
                                       'low16(value)))\n'
                                       'city = sample_random_pair(state).sample & 65535\n'
                                       'record = city\n'
                                       'city = replace_word(swap_words(u32(city * 3)), '
                                       'u16(low16(swap_words(u32(city * 3))) + 6))\n'
                                       'budget = divu_retained(u32(low16(budget) * low16(city)), 1000)\n'
                                       "city = replace_word(city, u16(_word(state, 'f364') << 2))\n"
                                       "field = _ram(state, 'e59c')\n"
                                       'effect = replace_word(values.effect, '
                                       'u16(field.word(low16(city), displacement=2) + low16(budget)))\n'
                                       'if low16(effect) > 100:\n'
                                       '    effect = replace_word(effect, 100)\n'
                                       'field.set_word(low16(city), low16(effect), displacement=2)\n'
                                       'from .services import award_defense_progress\n'
                                       'reward = award_defense_progress(state, values.officer, budget)\n'
                                       'return replace(values, city_index=city, record_index=record, '
                                       'officer=reward.officer_index, budget=reward.doubled_gain, '
                                       'value=value, effect=effect, orders=reward.progress)'},
 'settle_all_city_projects': {'signature': 'state: SceneState, values: ProjectValues',
                              'returns': 'ProjectValues',
                              'flow': 'checked_context(values, ProjectValues, state)\n'
                                      "_word(state, 'f364')\n"
                                      "_put(state, 'f364', 0)\n"
                                      "values = replace(values, assignments=_ram(state, 'cc00'), "
                                      "task_flags=_ram(state, 'cd00'))\n"
                                      'while True:\n'
                                      "    _put(state, 'f364', u16(_word(state, 'f364') + 1))\n"
                                      '    values = settle_first_city_project(state, values)\n'
                                      '    values = settle_second_city_project(state, values)\n'
                                      '    values = settle_third_city_project(state, values)\n'
                                      "    if _word(state, 'f364') >= 40:\n"
                                      '        return values'},
 'settle_city_projects_and_refresh_map': {'signature': 'state: SceneState, values: ProjectValues',
                                          'returns': 'ProjectValues',
                                          'flow': 'from .services import decode_glyph_rows_to_buffers\n'
                                                  'checked_context(values, ProjectValues, state)\n'
                                                  'values = settle_all_city_projects(state, values)\n'
                                                  'from .services import '
                                                  'clear_completed_monthly_actions\n'
                                                  'monthly = clear_completed_monthly_actions(state, '
                                                  'values.city_index)\n'
                                                  'values = replace(values, '
                                                  'city_index=monthly.loop_counter, '
                                                  'orders=state.table_at(monthly.city_gates_end.base))\n'
                                                  "destination = _ram(state, 'd300').cursor()\n"
                                                  'for _ in descending_inclusive(31):\n'
                                                  '    destination.append_long(286331153)\n'
                                                  'result = decode_glyph_rows_to_buffers(state, '
                                                  "data_view(state, 'data_0119a4').cursor(), "
                                                  'destination, replace_word(values.city_index, 1), '
                                                  'replace_word(values.record_index, 3), '
                                                  'replace_word(values.budget, 2))\n'
                                                  'state.write(12582916, 4, 1075838976)\n'
                                                  "source = _ram(state, 'd300').cursor()\n"
                                                  'for _ in descending_inclusive(127):\n'
                                                  '    state.write(12582912, 4, source.next_long())\n'
                                                  'values = replace(values, '
                                                  'city_index=result.background, '
                                                  'record_index=result.foreground, '
                                                  'budget=replace_word(result.remaining, 65535))\n'
                                                  'from .business_lowbank import '
                                                  'draw_current_resource_glyphs\n'
                                                  'from .contexts_lowbank import '
                                                  'DrawCurrentResourceGlyphsInput\n'
                                                  'drawn = draw_current_resource_glyphs(state, '
                                                  'DrawCurrentResourceGlyphsInput(values.city_index))\n'
                                                  'values = replace(values, city_index=drawn.value, '
                                                  'orders=drawn.destination)\n'
                                                  "_put(state, 'f362', 12)\n"
                                                  'values = _call(state, 199284, values, 72046)\n'
                                                  "if not _word(state, 'f386'):\n"
                                                  '    values = _call(state, 33786, values, 72060)\n'
                                                  "_put(state, 'f612', 520)\n"
                                                  "_put(state, 'f362', 19)\n"
                                                  "_word(state, 'f36a')\n"
                                                  "_put(state, 'f36a', 0)\n"
                                                  "_put(state, 'f3c2', 522)\n"
                                                  "_word(state, 'f3c4')\n"
                                                  "_put(state, 'f3c4', 0)\n"
                                                  "_word(state, 'cea0')\n"
                                                  "_put(state, 'cea0', 0)\n"
                                                  "_ram(state, '3000').set_word(0, 65535)\n"
                                                  'return values'},
 'dispatch_gameplay_command_state': {'signature': 'state: SceneState, frame: MapPresentation',
                                     'returns': 'MapPresentation',
                                     'flow': 'checked_context(frame, MapPresentation, state)\n'
                                             "selector = replace_word(frame.x, u16(_word(state, 'f362') "
                                             '<< 1))\n'
                                             'frame = replace(frame, x=selector)\n'
                                             'return _indexed_call(state, frame, selector, '
                                             "'data_013d58', 81274, 81238)"},
 '_require_packet': {'signature': 'frame',
                     'returns': None,
                     'flow': 'if frame.packet is None:\n'
                             "    raise Boundary('actual live map packet is required')\n"
                             'return frame.packet'},
 '_append_map': {'signature': 'state, frame, reset_scroll=False, initialize_clip=True',
                 'returns': None,
                 'flow': 'from .services import append_map_sprites\n'
                         'if frame.source is None:\n'
                         "    raise Boundary('externally supplied sprite source required')\n"
                         'result = append_map_sprites(state, frame.source, frame.x, frame.y, '
                         'frame.attributes, reset_scroll=reset_scroll, '
                         'initialize_clip=initialize_clip)\n'
                         'return replace(frame, source=result.source, x=result.x, y=result.y, '
                         'attributes=result.attributes)'},
 'render_visible_map_packets': {'signature': 'state: SceneState, frame: MapPresentation',
                                'returns': 'MapPresentation',
                                'flow': 'checked_context(frame, MapPresentation, state)\n'
                                        "packet = _ram(state, '9000').cursor()\n"
                                        'while True:\n'
                                        '    officer = replace_byte(frame.officer, packet.byte())\n'
                                        '    frame = replace(frame, packet=packet, officer=officer)\n'
                                        '    if not low8(officer):\n'
                                        '        return render_map_marker_positions(state, frame)\n'
                                        '    if not officer & 32:\n'
                                        '        x = u16((packet.byte(1) << 4) + 16)\n'
                                        "        scroll = _word(state, 'f314')\n"
                                        '        count = replace_word(frame.count, u16(x - scroll))\n'
                                        '        frame = replace(frame, count=count)\n'
                                        '        if x >= scroll and low16(count) < 240:\n'
                                        '            y = u16((packet.byte(2) << 4) + 16)\n'
                                        "            scroll = _word(state, 'f318')\n"
                                        '            count = replace_word(count, u16(y - scroll))\n'
                                        '            frame = replace(frame, count=count)\n'
                                        '            if y >= scroll and low16(count) < 336:\n'
                                        '                frame = render_selected_map_packet(state, '
                                        'frame)\n'
                                        '    count = replace_byte(replace_word(frame.count, 0), '
                                        'packet.byte())\n'
                                        '    count = replace_word(count, low16(count) & 15)\n'
                                        '    packet.base = u32(packet.base + 13 + s16(low16(count)))\n'
                                        '    frame = replace(frame, count=count)'},
 'render_selected_map_packet': {'signature': 'state: SceneState, frame: MapPresentation',
                                'returns': 'MapPresentation',
                                'flow': 'checked_context(frame, MapPresentation, state)\n'
                                        'packet = _require_packet(frame)\n'
                                        "if _word(state, 'f36c') == 2:\n"
                                        '    frame = replace(frame, x=replace_byte(frame.x, '
                                        'packet.byte(4)))\n'
                                        "    if low8(frame.x) == _ram(state, 'f377').byte():\n"
                                        '        frame = replace(frame, x=replace_byte(frame.x, '
                                        'packet.byte()))\n'
                                        "        if not frame.x & 16 and _ram(state, 'f321').byte() & "
                                        '4:\n'
                                        '            return frame\n'
                                        'frame = select_map_packet_sprite(state, '
                                        'locate_map_packet_sprite(state, frame))\n'
                                        'frame = replace(frame, '
                                        'attributes=replace_word(frame.attributes, 2048 if '
                                        'negative_byte(packet.byte()) else 0))\n'
                                        "_put(state, 'f60a', _word(state, 'f314'))\n"
                                        "_put(state, 'f60e', _word(state, 'f318'))\n"
                                        'return _append_map(state, frame)'},
 'select_map_packet_sprite': {'signature': 'state: SceneState, frame: MapPresentation',
                              'returns': 'MapPresentation',
                              'flow': 'checked_context(frame, MapPresentation, state)\n'
                                      "source = data_view(state, 'data_015eb8').cursor()\n"
                                      "if _ram(state, 'f321').byte() & 16:\n"
                                      '    source.base = u32(source.base + 8)\n'
                                      'saved = (frame.x, frame.y, source, frame.packet)\n'
                                      'from .services import query_scaled_terrain\n'
                                      'terrain = query_scaled_terrain(state, frame.x, frame.y, '
                                      'frame.attributes, frame.tile)\n'
                                      'result = replace(frame, x=terrain.row, y=terrain.column, '
                                      'attributes=terrain.terrain, tile=terrain.cost, '
                                      'packet=terrain.costs.cursor())\n'
                                      "source = data_view(state, 'data_015ec8').cursor() if "
                                      'low16(result.attributes) == 4 else saved[2]\n'
                                      'return replace(result, x=saved[0], y=saved[1], source=source, '
                                      'packet=saved[3])'},
 'locate_map_packet_sprite': {'signature': 'state: SceneState, frame: MapPresentation',
                              'returns': 'MapPresentation',
                              'flow': 'checked_context(frame, MapPresentation, state)\n'
                                      'packet = _require_packet(frame)\n'
                                      'x, y = (frame.x, frame.y)\n'
                                      "if _word(state, 'f612') == 521 and _word(state, 'f362') == 6:\n"
                                      "    x = replace_word(x, _word(state, '3bb4'))\n"
                                      '    if low8(x) == packet.byte(13):\n'
                                      "        x = replace_word(x, u16(_word(state, '3bb6') + 8))\n"
                                      "        y = replace_word(y, u16(_word(state, '3bb8') + 8))\n"
                                      '        return replace(frame, x=x, y=y)\n'
                                      'x = replace_word(replace_word(x, 0), u16((packet.byte(1) << 4) + '
                                      '8))\n'
                                      'y = replace_word(replace_word(y, 0), u16((packet.byte(2) << 4) + '
                                      '8))\n'
                                      'return replace(frame, x=x, y=y)'},
 'render_map_marker_positions': {'signature': 'state: SceneState, frame: MapPresentation',
                                 'returns': 'MapPresentation',
                                 'flow': 'checked_context(frame, MapPresentation, state)\n'
                                         "markers = _ram(state, '9f00').cursor()\n"
                                         'while True:\n'
                                         '    x = replace_word(frame.x, markers.next_word())\n'
                                         '    frame = replace(frame, x=x)\n'
                                         '    if negative_word(low16(x)):\n'
                                         '        return frame\n'
                                         '    y = replace_word(frame.y, markers.next_word())\n'
                                         '    attributes = replace_word(frame.attributes, u16(low16(x) '
                                         '+ 16))\n'
                                         "    scroll = _word(state, 'f314')\n"
                                         '    borrow = low16(attributes) < scroll\n'
                                         '    attributes = replace_word(attributes, '
                                         'u16(low16(attributes) - scroll))\n'
                                         '    frame = replace(frame, y=y, attributes=attributes)\n'
                                         '    if borrow or low16(attributes) > 240:\n'
                                         '        continue\n'
                                         '    attributes = replace_word(attributes, u16(low16(y) + '
                                         '16))\n'
                                         "    scroll = _word(state, 'f318')\n"
                                         '    borrow = low16(attributes) < scroll\n'
                                         '    attributes = replace_word(attributes, '
                                         'u16(low16(attributes) - scroll))\n'
                                         '    frame = replace(frame, attributes=attributes)\n'
                                         '    if borrow or low16(attributes) > 336:\n'
                                         '        continue\n'
                                         "    _put(state, 'f60a', _word(state, 'f314'))\n"
                                         "    _put(state, 'f60e', _word(state, 'f318'))\n"
                                         '    frame = _append_map(state, replace(frame, '
                                         "source=data_view(state, 'data_015f6a').cursor(), "
                                         'attributes=replace_word(attributes, 0)))'},
 '_panel_destination': {'signature': 'state',
                        'returns': None,
                        'flow': "return _ram(state, 'd100').cursor(_word(state, 'f31a'))"},
 '_panel_column': {'signature': 'destination, gap, tiles',
                   'returns': None,
                   'flow': 'for row in range(len(tiles) - 1, 0, -1):\n'
                           '    destination.set_word(u16(gap * row), tiles[row])\n'
                           'destination.append_word(tiles[0])'},
 'append_city_currency_panel': {'signature': 'state: SceneState, frame: MapPresentation',
                                'returns': 'MapPresentation',
                                'flow': "from .services import append_six_place_decimal_fields\nchecked_context(frame, MapPresentation, state)\ndestination = _panel_destination(state)\n_panel_column(destination, 28, (12, 12))\n_panel_column(destination, 28, (49332, 49716))\n_panel_column(destination, 28, (50048, 54144))\nfor _ in descending_inclusive(9):\n    _panel_column(destination, 28, (50049, 54145))\n_panel_column(destination, 28, (52096, 56192))\ndestination.base = u32(destination.base + 28)\n_panel_column(destination, 28, (12, 12))\n_panel_column(destination, 28, (49460, 49588))\n_panel_column(destination, 28, (50050, 50050))\n_panel_column(destination, 28, (49157, 49158))\n_panel_column(destination, 28, (49159, 49160))\n_panel_column(destination, 28, (49153, 49153))\n_panel_column(destination, 28, (49153, 49153))\nx = _ram(state, 'e09c').long(u16(_word(state, 'f364') << 2))\n_ram(state, 'f3f8').set_long(0, x)\ny, attributes = (replace_word(frame.y, 50054), replace_word(frame.attributes, 49153))\nnumeric = append_six_place_decimal_fields(state, x, low16(y), low16(attributes), _ram(state, 'd300').cursor())\nx = numeric.remainder\ntile = replace_word(frame.tile, numeric.divisor)\nofficer = replace_word(frame.officer, numeric.started)\ncount = replace_word(frame.count, numeric.glyph)\nsource = _ram(state, 'd300').cursor()\nfor _ in descending_inclusive(5):\n    destination.set_word(28, source.next_word())\n    destination.append_word(49153)\n_panel_column(destination, 28, (52098, 52098))\ndestination.word(28)\ndestination.set_word(28, 0)\n_put(state, 'f31a', u16(_word(state, 'f31a') + 112))\nreturn replace(frame, x=replace_word(x, 65535), y=y, attributes=attributes, tile=tile, officer=officer, count=count, source=destination, destination=source)"},
 'append_two_row_sequential_tiles': {'signature': 'state: SceneState, frame: MapPresentation',
                                     'returns': 'MapPresentation',
                                     'flow': "checked_context(frame, MapPresentation, state)\nif frame.source is None:\n    raise Boundary('live two-row A0 output cursor required')\ndestination = frame.source.advance(0)\ntile = frame.y\nfor _ in descending_inclusive(3):\n    destination.set_word(0, low16(tile))\n    tile = replace_word(tile, u16(low16(tile) + 1))\n    destination.set_word(32, low16(tile))\n    tile = replace_word(tile, u16(low16(tile) + 1))\n    destination.base = u32(destination.base + 2)\nreturn replace(frame, x=replace_word(frame.x, 65535), y=tile, source=destination)"},
 'append_city_project_panel': {'signature': 'state: SceneState, frame: MapPresentation',
                               'returns': 'MapPresentation',
                               'flow': "checked_context(frame, MapPresentation, state)\ndestination = _panel_destination(state)\n_panel_column(destination, 32, (14, 14, 14, 14))\n_panel_column(destination, 32, (50334, 50718, 50846, 50974))\n_panel_column(destination, 32, (50048, 50050, 50050, 54144))\nfor _ in descending_inclusive(11):\n    _panel_column(destination, 32, (50049, 49153, 49153, 54145))\n_panel_column(destination, 32, (52096, 52098, 52098, 56192))\ndestination.base = u32(destination.base + 96)\n_panel_column(destination, 32, (14, 14))\n_panel_column(destination, 32, (50462, 50590))\n_panel_column(destination, 32, (50050, 50050))\nframe = append_two_row_sequential_tiles(state, replace(frame, source=destination, y=replace_word(frame.y, 49161)))\ndestination = frame.source\nfor _ in descending_inclusive(3):\n    _panel_column(destination, 32, (49153, 49153))\nframe = append_two_row_sequential_tiles(state, replace(frame, y=replace_word(frame.y, 49169)))\ndestination = frame.source\n_panel_column(destination, 32, (52098, 52098))\ndestination.word(32)\ndestination.set_word(32, 0)\n_put(state, 'f31a', u16(_word(state, 'f31a') + 192))\n_ram(state, 'f3a5').set_byte(0, _ram(state, 'f3a5').byte() | 32)\nreturn frame"},
 'append_current_city_value': {'signature': 'state: SceneState, frame: MapPresentation',
                               'returns': 'MapPresentation',
                               'flow': "from .services import append_six_place_decimal_fields\nchecked_context(frame, MapPresentation, state)\ndestination = _panel_destination(state)\ndestination.append_word(3)\ndestination.append_word(50602)\nx, y, attributes = (replace_word(frame.x, _word(state, 'f670')), replace_word(frame.y, 50054), replace_word(frame.attributes, 0))\nnumeric = append_six_place_decimal_fields(state, x, low16(y), low16(attributes), _ram(state, 'd300').cursor())\nx = numeric.remainder\ntile = replace_word(frame.tile, numeric.divisor)\nofficer = replace_word(frame.officer, numeric.started)\ncount = replace_word(frame.count, numeric.glyph)\ndigits, x = (_ram(state, 'd306').cursor(), replace_word(x, 0))\nfor _ in descending_inclusive(2):\n    attributes = replace_word(attributes, digits.next_word())\n    if not low16(attributes):\n        attributes = replace_word(attributes, 49153 if low16(x) < _word(state, 'f39a') else 50054)\n    destination.append_word(low16(attributes))\n    x = replace_word(x, u16(low16(x) + 1))\ndestination.word()\ndestination.put_word(0)\n_put(state, 'f31a', u16(_word(state, 'f31a') + 10))\nreturn replace(frame, x=x, y=replace_word(y, 65535), attributes=attributes, tile=tile, officer=officer, count=count, source=destination)"},
 'append_selected_long_value': {'signature': 'state: SceneState, frame: MapPresentation',
                                'returns': 'MapPresentation',
                                'flow': "from .services import append_six_place_decimal_fields\nchecked_context(frame, MapPresentation, state)\ndestination = _panel_destination(state)\ndestination.append_word(6)\ndestination.append_word(50860)\nx = _ram(state, 'f3ba').long()\ny, attributes = (replace_word(frame.y, 50054), replace_word(frame.attributes, 49153))\nnumeric = append_six_place_decimal_fields(state, x, low16(y), low16(attributes), _ram(state, 'd300').cursor())\nx = numeric.remainder\ntile = replace_word(frame.tile, numeric.divisor)\nofficer = replace_word(frame.officer, numeric.started)\ncount = replace_word(frame.count, numeric.glyph)\nsource = _ram(state, 'd300').cursor()\nfor _ in descending_inclusive(2):\n    destination.append_long(source.next_long())\ndestination.word()\ndestination.put_word(0)\n_put(state, 'f31a', u16(_word(state, 'f31a') + 16))\nreturn replace(frame, x=replace_word(x, 65535), y=y, attributes=attributes, tile=tile, officer=officer, count=count, source=destination, destination=source)"},
 'append_four_row_tile_columns': {'signature': 'state: SceneState, frame: MapPresentation',
                                  'returns': 'MapPresentation',
                                  'flow': "checked_context(frame, MapPresentation, state)\nif frame.source is None:\n    raise Boundary('actual four-row A0 output cursor required')\ndestination = frame.source.advance(0)\ntile = frame.y\nfor _ in descending_inclusive(low16(frame.x)):\n    destination.set_word(0, 50049)\n    destination.set_word(24, low16(tile))\n    tile = replace_word(tile, u16(low16(tile) + 1))\n    destination.set_word(48, low16(tile))\n    tile = replace_word(tile, u16(low16(tile) + 1))\n    destination.set_word(72, 54145)\n    destination.base = u32(destination.base + 2)\nreturn replace(frame, x=replace_word(frame.x, 65535), y=tile, source=destination)"},
 'append_four_row_status_panel': {'signature': 'state: SceneState, frame: MapPresentation',
                                  'returns': 'MapPresentation',
                                  'flow': "checked_context(frame, MapPresentation, state)\nfrom .business_commands import present_current_command_prompt\nfrom .contexts_commands import PresentCurrentCommandPromptInput\nshown = present_current_command_prompt(state, PresentCurrentCommandPromptInput(frame.x, frame.y, frame.remaining))\nframe = replace(frame, x=shown.value, y=shown.field, remaining=shown.remaining)\ndestination = _panel_destination(state)\n_panel_column(destination, 24, (10, 10, 10, 10))\n_panel_column(destination, 24, (49308, 49436, 49564, 49692))\n_panel_column(destination, 24, (50048, 50050, 50050, 54144))\nframe = append_four_row_tile_columns(state, replace(frame, source=destination, x=replace_word(frame.x, 5), y=replace_word(frame.y, 49165)))\ndestination = frame.source\nframe = append_four_row_tile_columns(state, replace(frame, x=replace_word(frame.x, 1), y=replace_word(frame.y, 49225)))\ndestination = frame.source\n_panel_column(destination, 24, (52096, 52098, 52098, 56192))\ndestination.word(72)\ndestination.set_word(72, 0)\n_put(state, 'f3a4', _word(state, 'f3a4') | 38912)\n_put(state, 'f31a', u16(_word(state, 'f31a') + 96))\nreturn frame"},
 'append_missing_city_queue_packets': {'signature': 'state: SceneState, frame: MapPresentation',
                                       'returns': 'MapPresentation',
                                       'flow': "checked_context(frame, MapPresentation, state)\ndestination = _ram(state, '3000').cursor(_word(state, '3826'))\nactive, heads = (_ram(state, 'ea38'), _ram(state, 'e640'))\nx, y, attributes = (frame.x, frame.y, frame.attributes)\nsource = frame.packet\nfor city in descending_inclusive(39):\n    x = replace_word(x, city)\n    if not active.byte(city):\n        continue\n    source = _ram(state, '3000').cursor()\n    attributes = replace_word(attributes, u16(city + 1))\n    found = False\n    while True:\n        y = replace_byte(y, source.next_byte())\n        if negative_byte(low8(y)):\n            break\n        y = replace_byte(y, source.next_byte())\n        y = replace_byte(y, source.next_byte())\n        y = replace_byte(y, source.next_byte())\n        if low8(y) == 128:\n            if source.next_byte() == low8(attributes):\n                found = True\n                break\n        while source.next_byte():\n            pass\n    if found:\n        continue\n    destination.byte()\n    destination.append_byte(0)\n    y = replace_word(y, u16(city << 1))\n    destination.append_byte(heads.byte(low16(y), displacement=1))\n    destination.append_byte(1)\n    destination.append_byte(128)\n    destination.append_byte(low8(attributes))\n    destination.byte()\n    destination.append_byte(0)\n    destination.set_byte(0, 255)\n    _put(state, '3826', u16(_word(state, '3826') + 6))\nreturn replace(frame, x=replace_word(x, 65535), y=y, attributes=attributes, source=destination, destination=active.cursor(), packet=source)"},
 'sort_map_packet_queue': {'signature': 'state: SceneState, frame: MapPresentation',
                           'returns': 'MapPresentation',
                           'flow': 'checked_context(frame, MapPresentation, state)\n'
                                   'frame = append_missing_city_queue_packets(state, frame)\n'
                                   "source = _ram(state, '3000').cursor()\n"
                                   "_put(state, '39b2', 0)\n"
                                   'x, y = (frame.x, frame.y)\n'
                                   'while not negative_byte(source.next_byte()):\n'
                                   '    x, y = (replace_byte(x, source.next_byte()), replace_byte(y, '
                                   'source.next_byte()))\n'
                                   "    insertion = _ram(state, '39b2').cursor()\n"
                                   '    while low8(y) <= insertion.byte():\n'
                                   '        insertion.base = u32(insertion.base + 2)\n'
                                   '    end = state.table_at(insertion.base).cursor()\n'
                                   '    while True:\n'
                                   '        end.base = u32(end.base + 2)\n'
                                   '        if not end.byte():\n'
                                   '            break\n'
                                   '    end.set_byte(2, 0)\n'
                                   '    shifted = state.table_at(u32(end.base + 2)).cursor()\n'
                                   '    while True:\n'
                                   '        for _ in range(2):\n'
                                   '            item = end.previous_byte()\n'
                                   '            shifted.base = u32(shifted.base - 1)\n'
                                   '            shifted.set_byte(0, item)\n'
                                   '        if end.base <= insertion.base:\n'
                                   '            break\n'
                                   '    insertion.set_byte(0, low8(y))\n'
                                   '    insertion.set_byte(1, low8(x))\n'
                                   '    while source.next_byte():\n'
                                   '        pass\n'
                                   "_put(state, '3bb2', 0)\n"
                                   'return replace(frame, x=x, y=y, packet=source)'},
 '_upload_prompt': {'signature': 'state, frame, parameters, remaining, command, longs, refresh=False',
                    'returns': None,
                    'flow': 'from .services import decode_glyph_rows_to_buffers, '
                            'refresh_gameplay_scene\n'
                            'x, y, tile = (replace_word(frame.x, 1), replace_word(frame.y, 3), '
                            'replace_word(frame.tile, remaining))\n'
                            'result = decode_glyph_rows_to_buffers(state, data_view(state, '
                            "parameters).cursor(), _ram(state, 'd300').cursor(), x, y, tile)\n"
                            'state.write(12582916, 4, command)\n'
                            "source = _ram(state, 'd300').cursor()\n"
                            'tile = replace_word(result.remaining, u16(longs - 1))\n'
                            'for _ in descending_inclusive(low16(tile)):\n'
                            '    state.write(12582912, 4, source.next_long())\n'
                            'tile = replace_word(tile, 65535)\n'
                            'x = refresh_gameplay_scene(state, result.background) if refresh else '
                            'result.background\n'
                            'return replace(frame, x=x, y=result.foreground, tile=tile, '
                            'source=result.source, destination=source)'},
 'upload_selected_queue_officer_name': {'signature': 'state: SceneState, frame: MapPresentation',
                                        'returns': 'MapPresentation',
                                        'flow': 'checked_context(frame, MapPresentation, state)\n'
                                                'packet = state.table_at(_ram(state, '
                                                "'382c').long()).cursor()\n"
                                                'officer = replace_byte(replace_word(frame.officer, 0), '
                                                'packet.byte(4))\n'
                                                'officer = replace_word(officer, u16(low16(officer) << '
                                                '1))\n'
                                                'officer = replace_word(officer, _ram(state, '
                                                "'e640').word(low16(officer)))\n"
                                                'count = replace_word(frame.count, low16(officer))\n'
                                                'officer = replace_word(officer, u16((low16(officer) << '
                                                '1) + low16(count)))\n'
                                                'officer = replace_word(officer, u16(low16(officer) << '
                                                '1))\n'
                                                'from .services import decode_glyph_rows_to_buffers\n'
                                                'x, y = (replace_word(frame.x, 1), '
                                                'replace_word(frame.y, 3))\n'
                                                'result = decode_glyph_rows_to_buffers(state, '
                                                'data_view(state, '
                                                "'data_08a504').cursor(low16(officer)), _ram(state, "
                                                "'d300').cursor(), x, y, replace_word(frame.tile, 2))\n"
                                                'state.write(12582916, 4, 1101004800)\n'
                                                "source = _ram(state, 'd300').cursor()\n"
                                                'for _ in descending_inclusive(95):\n'
                                                '    state.write(12582912, 4, source.next_long())\n'
                                                'result = decode_glyph_rows_to_buffers(state, '
                                                "data_view(state, 'data_01665e').cursor(), _ram(state, "
                                                "'d300').cursor(), result.background, "
                                                'result.foreground, replace_word(result.remaining, 0))\n'
                                                'state.write(12582916, 4, 1226833920)\n'
                                                "destination = _ram(state, 'd300').cursor()\n"
                                                'for _ in descending_inclusive(31):\n'
                                                '    state.write(12582912, 4, destination.next_long())\n'
                                                'return replace(frame, x=result.background, '
                                                'y=result.foreground, '
                                                'tile=replace_word(result.remaining, 65535), '
                                                'officer=officer, count=count, source=result.source, '
                                                'destination=destination)'},
 'dispatch_queue_command_state': {'signature': 'state: SceneState, frame: MapPresentation',
                                  'returns': 'MapPresentation',
                                  'flow': 'checked_context(frame, MapPresentation, state)\n'
                                          "x = replace_word(frame.x, u16(_word(state, 'f362') << 1))\n"
                                          'return _indexed_call(state, replace(frame, x=x), x, '
                                          "'data_016670', 91768, 91758)"},
 'render_city_map_entries': {'signature': 'state: SceneState, frame: MapPresentation',
                             'returns': 'MapPresentation',
                             'flow': 'checked_context(frame, MapPresentation, state)\n'
                                     "packet = _ram(state, 'ce9c').cursor()\n"
                                     'for city in descending_inclusive(39):\n'
                                     '    tile = replace_word(frame.tile, city)\n'
                                     '    frame = replace(frame, tile=tile, packet=packet)\n'
                                     '    if packet.byte() and (not packet.byte() & 16):\n'
                                     '        x = replace_word(replace_word(frame.x, 0), '
                                     'u16(packet.byte(1) << 4))\n'
                                     '        attributes = replace_word(frame.attributes, u16(low16(x) '
                                     '+ 16))\n'
                                     "        scroll = _word(state, 'f314')\n"
                                     '        borrow = low16(attributes) < scroll\n'
                                     '        attributes = replace_word(attributes, '
                                     'u16(low16(attributes) - scroll))\n'
                                     '        frame = replace(frame, x=x, attributes=attributes)\n'
                                     '        if not borrow and low16(attributes) <= 240:\n'
                                     '            y = replace_word(replace_word(frame.y, 0), '
                                     'u16(packet.byte(2) << 4))\n'
                                     '            attributes = replace_word(attributes, u16(low16(y) + '
                                     '16))\n'
                                     "            scroll = _word(state, 'f318')\n"
                                     '            borrow = low16(attributes) < scroll\n'
                                     '            attributes = replace_word(attributes, '
                                     'u16(low16(attributes) - scroll))\n'
                                     '            frame = replace(frame, y=y, attributes=attributes)\n'
                                     '            if not borrow and low16(attributes) <= 336:\n'
                                     '                frame = render_city_map_entry(state, frame)\n'
                                     '    packet.base = u32(packet.base - 4)\n'
                                     'return replace(frame, tile=replace_word(frame.tile, 65535))'},
 'render_city_map_entry': {'signature': 'state: SceneState, frame: MapPresentation',
                           'returns': 'MapPresentation',
                           'flow': 'checked_context(frame, MapPresentation, state)\n'
                                   'packet = _require_packet(frame)\n'
                                   'saved_tile = frame.tile\n'
                                   "if _word(state, 'f612') == 522 and _word(state, 'f362') == 2 and "
                                   "(low16(saved_tile) == _word(state, 'cea0')):\n"
                                   '    frame = replace(frame, x=replace_word(frame.x, _word(state, '
                                   "'cea4')), y=replace_word(frame.y, _word(state, 'cea6')))\n"
                                   "source = data_view(state, 'data_016a78').cursor()\n"
                                   "if not _ram(state, 'f321').byte() & 16:\n"
                                   '    source.base = u32(source.base + 8)\n'
                                   'saved_x, saved_y = (frame.x, frame.y)\n'
                                   'from .services import query_scaled_terrain\n'
                                   'terrain = query_scaled_terrain(state, replace_word(frame.x, '
                                   'u16(low16(frame.x) + 8)), replace_word(frame.y, u16(low16(frame.y) '
                                   '+ 8)), frame.attributes, frame.tile)\n'
                                   'result = replace(frame, x=terrain.row, y=terrain.column, '
                                   'attributes=terrain.terrain, tile=terrain.cost, '
                                   'packet=terrain.costs.cursor())\n'
                                   'if low16(result.attributes) == 4:\n'
                                   '    source.base = u32(source.base + 16)\n'
                                   'y = replace_word(saved_y, u16(low16(saved_y) + 8))\n'
                                   'attributes = replace_word(result.attributes, 2048 if '
                                   'negative_byte(packet.byte()) else 0)\n'
                                   "_put(state, 'f60a', _word(state, 'f314'))\n"
                                   "_put(state, 'f60e', _word(state, 'f318'))\n"
                                   'result = _append_map(state, replace(result, x=saved_x, y=y, '
                                   'attributes=attributes, source=source, packet=packet))\n'
                                   'return replace(result, tile=saved_tile)'},
 'upload_first_battle_prompt': {'signature': 'state: SceneState, frame: MapPresentation',
                                'returns': 'MapPresentation',
                                'flow': 'checked_context(frame, MapPresentation, state)\n'
                                        'state.set_status_word(9984)\n'
                                        "return _upload_prompt(state, frame, 'data_06c0ae', 11, "
                                        '1084227586, 384, True)'},
 'upload_second_battle_prompt': {'signature': 'state: SceneState, frame: MapPresentation',
                                 'returns': 'MapPresentation',
                                 'flow': 'checked_context(frame, MapPresentation, state)\n'
                                         'state.set_status_word(9984)\n'
                                         "return _upload_prompt(state, frame, 'data_06c0c6', 11, "
                                         '1084227586, 384, True)'},
 'upload_battle_action_prompt': {'signature': 'state: SceneState, frame: MapPresentation',
                                 'returns': 'MapPresentation',
                                 'flow': 'checked_context(frame, MapPresentation, state)\n'
                                         "return _upload_prompt(state, frame, 'data_06c0de', 4, "
                                         '1084227586, 160)'},
 'upload_battle_result_prompt': {'signature': 'state: SceneState, frame: MapPresentation',
                                 'returns': 'MapPresentation',
                                 'flow': 'checked_context(frame, MapPresentation, state)\n'
                                         "destination = _ram(state, 'd300').cursor()\n"
                                         'for _ in descending_inclusive(31):\n'
                                         '    destination.append_long(286331153)\n'
                                         'from .services import decode_glyph_rows_to_buffers\n'
                                         'result = decode_glyph_rows_to_buffers(state, data_view(state, '
                                         "'data_06c168').cursor(), destination, replace_word(frame.x, "
                                         '1), replace_word(frame.y, 3), replace_word(frame.tile, 5))\n'
                                         'state.write(12582916, 4, 1075838978)\n'
                                         "destination = _ram(state, 'd300').cursor()\n"
                                         'for _ in descending_inclusive(223):\n'
                                         '    state.write(12582912, 4, destination.next_long())\n'
                                         'return replace(frame, x=result.background, '
                                         'y=result.foreground, tile=replace_word(result.remaining, '
                                         '65535), source=result.source, destination=destination)'},
 'upload_selected_officer_names': {'signature': 'state: SceneState, frame: MapPresentation',
                                   'returns': 'MapPresentation',
                                   'flow': 'from .services import decode_glyph_rows_to_buffers\n'
                                           'checked_context(frame, MapPresentation, state)\n'
                                           "roster = _ram(state, 'af56').cursor(u16(_word(state, "
                                           "'f658') << 1))\n"
                                           'x = replace_word(frame.x, 1)\n'
                                           'state.write(12582916, 4, 1084227586)\n'
                                           'source = frame.source\n'
                                           'tile, attributes, remaining, y = (frame.tile, '
                                           'frame.attributes, replace_word(frame.remaining, 4), '
                                           'frame.y)\n'
                                           'destination = frame.destination\n'
                                           'for count in descending_inclusive(4):\n'
                                           '    remaining = replace_word(remaining, count)\n'
                                           '    attributes = replace_word(attributes, '
                                           'roster.next_word())\n'
                                           '    if negative_word(low16(attributes)):\n'
                                           '        y = replace_word(y, 3)\n'
                                           "        destination = _ram(state, 'd300').cursor()\n"
                                           '        for _ in descending_inclusive(15):\n'
                                           '            destination.append_long(286331153)\n'
                                           '        result = decode_glyph_rows_to_buffers(state, '
                                           "data_view(state, 'data_018844').cursor(), destination, x, "
                                           'y, replace_word(tile, 1))\n'
                                           '        x, y, tile, source = (result.background, '
                                           'result.foreground, result.remaining, result.source)\n'
                                           '        for _ in descending_inclusive(15):\n'
                                           '            destination.append_long(286331153)\n'
                                           "        destination = _ram(state, 'd300').cursor()\n"
                                           '        for _ in descending_inclusive(95):\n'
                                           '            state.write(12582912, 4, '
                                           'destination.next_long())\n'
                                           '        return replace(frame, x=x, y=y, '
                                           'tile=replace_word(tile, 65535), remaining=remaining, '
                                           'attributes=attributes, packet=roster, source=source, '
                                           'destination=destination)\n'
                                           '    y = replace_word(y, 2 if attributes & 16384 else 3)\n'
                                           '    attributes = replace_word(attributes, low16(attributes) '
                                           '& 255)\n'
                                           '    tile = replace_word(tile, low16(attributes))\n'
                                           '    attributes = replace_word(attributes, '
                                           'u16((low16(attributes) << 1) + low16(tile) << 1))\n'
                                           '    source = data_view(state, '
                                           "'data_08a504').cursor(low16(attributes))\n"
                                           '    result = decode_glyph_rows_to_buffers(state, source, '
                                           "_ram(state, 'd300').cursor(), x, y, replace_word(tile, 2))\n"
                                           '    x, y, tile, source = (result.background, '
                                           'result.foreground, result.remaining, result.source)\n'
                                           "    destination = _ram(state, 'd300').cursor()\n"
                                           '    for _ in descending_inclusive(95):\n'
                                           '        state.write(12582912, 4, destination.next_long())\n'
                                           'return replace(frame, x=x, y=y, tile=replace_word(tile, '
                                           '65535), remaining=replace_word(remaining, 65535), '
                                           'attributes=attributes, packet=roster, source=source, '
                                           'destination=destination)'},
 'select_active_battle_controller': {'signature': 'state: SceneState, frame: MapPresentation',
                                     'returns': 'MapPresentation',
                                     'flow': 'checked_context(frame, MapPresentation, state)\n'
                                             "if _word(state, 'f612') == 1031 and _word(state, 'f362') "
                                             'in (0, 2, 4):\n'
                                             '    return frame\n'
                                             "x, y = (replace_word(frame.x, _word(state, 'f68c')), "
                                             "replace_word(frame.y, _word(state, 'f68e')))\n"
                                             "if _ram(state, 'f6d7').byte() & 2:\n"
                                             '    x, y = (y, x)\n'
                                             "if low16(x) == _word(state, 'f67a'):\n"
                                             '    return replace(frame, x=x, y=y)\n'
                                             "if low16(x) != _word(state, 'f67c'):\n"
                                             "    if low16(x) == _word(state, 'f67e'):\n"
                                             "        if low16(y) == _word(state, 'f67c'):\n"
                                             '            return replace(frame, x=x, y=y)\n'
                                             "    elif low16(y) == _word(state, 'f67a'):\n"
                                             '        return replace(frame, x=x, y=y)\n'
                                             "_put(state, 'f602', _word(state, 'f604'))\n"
                                             'return replace(frame, x=x, y=y)'},
 'cycle_available_direction': {'signature': 'state: SceneState, frame: MapPresentation',
                               'returns': 'MapPresentation',
                               'flow': 'checked_context(frame, MapPresentation, state)\n'
                                       "direction_options = _ram(state, 'efbe').cursor()\n"
                                       "y = replace_word(frame.y, _word(state, 'efc6'))\n"
                                       "x = replace_byte(frame.x, _ram(state, 'f603').byte())\n"
                                       'x = replace_word(x, low16(x) & 12)\n'
                                       'if low16(x):\n'
                                       '    step = 2 if x & 4 else -2\n'
                                       '    while True:\n'
                                       '        y = replace_word(y, u16(low16(y) + step) & 7)\n'
                                       '        if not negative_word(direction_options.word(low16(y))):\n'
                                       '            break\n'
                                       "    _put(state, 'efc6', y)\n"
                                       'return replace(frame, x=x, y=y, destination=direction_options)'},
 'render_direction_choice': {'signature': 'state: SceneState, frame: MapPresentation',
                             'returns': 'MapPresentation',
                             'flow': 'checked_context(frame, MapPresentation, state)\n'
                                     "if _ram(state, 'f321').byte() & 16:\n"
                                     '    return frame\n'
                                     "offsets = data_view(state, 'data_01d012')\n"
                                     'attributes = replace_word(frame.attributes, u16(_word(state, '
                                     "'efc6') << 1))\n"
                                     "packet = state.table_at(_ram(state, '382c').long()).cursor()\n"
                                     'x = replace_byte(replace_word(frame.x, 0), packet.byte(1))\n'
                                     'x = replace_word(x, u16(low16(x) + '
                                     'offsets.word(low16(attributes))))\n'
                                     'x = replace_word(x, u16(low16(x) << 4))\n'
                                     'y = replace_byte(replace_word(frame.y, 0), packet.byte(2))\n'
                                     'y = replace_word(y, u16(low16(y) + '
                                     'offsets.word(low16(attributes), displacement=2)))\n'
                                     'y = replace_word(y, u16(low16(y) << 4))\n'
                                     "_put(state, 'f60a', _word(state, 'f314'))\n"
                                     "_put(state, 'f60e', _word(state, 'f318'))\n"
                                     'return _append_map(state, replace(frame, x=x, y=y, '
                                     'attributes=replace_word(attributes, 0), packet=offsets.cursor(), destination=packet, '
                                     "source=data_view(state, 'data_01d022').cursor()), False, False)"},
 'update_direction_choice': {'signature': 'state: SceneState, frame: MapPresentation',
                             'returns': 'MapPresentation',
                             'flow': 'checked_context(frame, MapPresentation, state)\n'
                                     'frame = render_direction_choice(state, '
                                     'cycle_available_direction(state, frame))\n'
                                     "if _ram(state, 'f603').byte() & 32:\n"
                                     '    frame = _call(state, 49334, frame, 118640)\n'
                                     "    _put(state, 'f612', 520)\n"
                                     "    _put(state, 'f362', 3)\n"
                                     "    _put(state, 'f36a', 18)\n"
                                     'return frame'},
 'dispatch_target_eligibility': {'signature': 'state: SceneState, search: TargetSearch',
                                 'returns': 'TargetSearch',
                                 'flow': 'checked_context(search, TargetSearch, state)\n'
                                         'origin_x, origin_y = (search.origin_x, search.origin_y)\n'
                                         'selector = replace_word(search.limit, u16(_word(state, '
                                         "'f6d4') << 1))\n"
                                         'search = _indexed_call(state, replace(search, '
                                         "limit=selector), selector, 'data_017bb2', 97264, 97196)\n"
                                         'return replace(search, origin_x=origin_x, origin_y=origin_y)'},
 'append_nearby_target_candidates': {'signature': 'state: SceneState, search: TargetSearch',
                                     'returns': 'TargetSearch',
                                     'flow': 'checked_context(search, TargetSearch, state)\n'
                                             'if None in (search.source, search.destination, '
                                             'search.officers, search.blocked):\n'
                                             "    raise Boundary('live target roster, positions and "
                                             "exclusion flags required')\n"
                                             'source, destination = (search.source, '
                                             'search.destination)\n'
                                             'while True:\n'
                                             '    candidate = replace_word(search.candidate, '
                                             'source.next_word())\n'
                                             '    search = replace(search, candidate=candidate)\n'
                                             '    if negative_word(low16(candidate)):\n'
                                             '        return search\n'
                                             '    if search.blocked.byte(low16(candidate)):\n'
                                             '        continue\n'
                                             '    candidate = replace_word(candidate, '
                                             'u16((low16(candidate) & 255) << 2))\n'
                                             '    x = replace_word(search.metric_x, '
                                             'search.officers.word(low16(candidate)) >> 7)\n'
                                             '    y = replace_word(search.metric_y, '
                                             'search.officers.word(low16(candidate), displacement=2) >> '
                                             '7)\n'
                                             '    candidate = replace_word(candidate, low16(candidate) '
                                             '>> 2)\n'
                                             '    search = dispatch_target_eligibility(state, '
                                             'replace(search, candidate=candidate, metric_x=x, '
                                             'metric_y=y))\n'
                                             '    if state.read_status_word() & 1:\n'
                                             '        continue\n'
                                             '    dx = u16(low16(search.metric_x) - '
                                             'low16(search.origin_x))\n'
                                             '    if low16(search.metric_x) < low16(search.origin_x):\n'
                                             '        dx = u16(-dx)\n'
                                             '    x = replace_word(search.metric_x, dx)\n'
                                             '    if dx > low16(search.count):\n'
                                             '        search = replace(search, metric_x=x)\n'
                                             '        continue\n'
                                             '    x = u32(dx * dx)\n'
                                             '    dy = u16(low16(search.metric_y) - '
                                             'low16(search.origin_y))\n'
                                             '    if low16(search.metric_y) < low16(search.origin_y):\n'
                                             '        dy = u16(-dy)\n'
                                             '    y = replace_word(search.metric_y, dy)\n'
                                             '    if dy > low16(search.count):\n'
                                             '        search = replace(search, metric_x=x, metric_y=y)\n'
                                             '        continue\n'
                                             '    y = u32(dy * dy)\n'
                                             '    x = u32(x + y)\n'
                                             '    search = _call(state, 198670, replace(search, city=x, '
                                             'metric_x=x, metric_y=y), 97168)\n'
                                             '    if low16(search.city) <= low16(search.count):\n'
                                             '        destination.append_word(low16(search.candidate))'},
 'build_nearby_battle_targets': {'signature': 'state: SceneState, search: TargetSearch',
                                 'returns': 'TargetSearch',
                                 'flow': 'from .services import refresh_gameplay_scene\n'
                                         'checked_context(search, TargetSearch, state)\n'
                                         'state.set_status_word(9984)\n'
                                         "_put(state, 'af80', 0)\n"
                                         "city = replace_word(search.city, _word(state, 'f3a6'))\n"
                                         'count = replace_byte(replace_word(search.count, 0), '
                                         "_ram(state, 'c400').byte(low16(city)))\n"
                                         'origin_x = replace_word(search.origin_x, low16(count))\n'
                                         'count = replace_word(count, u16((low16(count) << 3) + '
                                         'low16(origin_x)))\n'
                                         'city = replace_word(city, u16(low16(city) << 2))\n'
                                         "officers = _ram(state, 'a150')\n"
                                         'origin_x = replace_word(origin_x, officers.word(low16(city)) '
                                         '>> 7)\n'
                                         'origin_y = replace_word(search.origin_y, '
                                         'officers.word(low16(city), displacement=2) >> 7)\n'
                                         "candidate = u32(_word(state, 'f68a') * 2240)\n"
                                         'search = replace(search, city=city, count=count, '
                                         'candidate=candidate, origin_x=origin_x, origin_y=origin_y, '
                                         'officers=officers, terrain=state.table_at(u32(607720 + '
                                         "candidate)), destination=_ram(state, 'a62c').cursor())\n"
                                         'skip = False\n'
                                         "if _word(state, 'f6d4') == 1:\n"
                                         '    search = _call(state, 107598, replace(search, '
                                         'metric_x=replace_word(search.metric_x, low16(origin_x)), '
                                         'metric_y=replace_word(search.metric_y, low16(origin_y))), '
                                         '97012)\n'
                                         '    if low8(search.city) not in (0, 4, 7):\n'
                                         "        _put(state, 'af80', 311)\n"
                                         '        skip = True\n'
                                         'if not skip:\n'
                                         "    search = replace(search, source=_ram(state, 'a550' if "
                                         "_ram(state, 'f6d7').byte() & 2 else 'a5a4').cursor(), "
                                         "blocked=_ram(state, '3bc2'))\n"
                                         '    search = append_nearby_target_candidates(state, search)\n'
                                         'search.destination.put_word(65535)\n'
                                         'return replace(search, city=refresh_gameplay_scene(state, '
                                         'search.city))'},
 '_carry': {'signature': 'state, value',
            'returns': None,
            'flow': 'status = state.read_status_word()\n'
                    'state.set_status_word(status | 1 if value else status & 65534)'},
 'deduct_force_supply': {'signature': 'state: SceneState, policy: BattlePolicy',
                         'returns': 'BattlePolicy',
                         'flow': 'checked_context(policy, BattlePolicy, state)\n'
                                 'if policy.roster is None or policy.candidates is None or '
                                 'policy.controller is None:\n'
                                 "    raise Boundary('roster, supply and troop views required')\n"
                                 'scan = state.table_at(policy.roster.base).cursor()\n'
                                 'cost, unit = (0, policy.target_y)\n'
                                 'while True:\n'
                                 '    unit = replace_word(unit, scan.next_word())\n'
                                 '    if negative_word(low16(unit)):\n'
                                 '        break\n'
                                 '    unit = replace_word(unit, u16((low16(unit) & 255) << 2))\n'
                                 '    cost = u32(cost + policy.controller.long(low16(unit)))\n'
                                 '    cost = u32(cost + 100)\n'
                                 'cost = divu_retained(cost, 100) & 65535\n'
                                 'old_supply = policy.candidates.long()\n'
                                 'policy.candidates.set_long(0, u32(old_supply - cost))\n'
                                 'policy = replace(policy, target_x=cost, target_y=unit, scan=scan)\n'
                                 'if old_supply < cost:\n'
                                 '    policy.candidates.set_long(0, 0)\n'
                                 '    return apply_force_supply_losses(state, policy)\n'
                                 'return policy'},
 'settle_both_force_supply': {'signature': 'state: SceneState, policy: BattlePolicy',
                              'returns': 'BattlePolicy',
                              'flow': "checked_context(policy, BattlePolicy, state)\npolicy = replace(policy, controller=_ram(state, 'c800'), opponent=_ram(state, 'b200'))\n_word(state, 'f6d6')\n_put(state, 'f6d6', 0)\npolicy = deduct_force_supply(state, replace(policy, roster=_ram(state, 'a550').cursor(), candidates=_ram(state, 'f69e').cursor()))\n_put(state, 'f6d6', 2)\nreturn deduct_force_supply(state, replace(policy, roster=_ram(state, 'a5a4').cursor(), candidates=_ram(state, 'f6a2').cursor()))"},
 '_present_supply_notice': {'signature': 'state, policy, force, message',
                            'returns': None,
                            'flow': "saved_force = _word(state, 'f376')\n"
                                    'saved = (policy.target_x, policy.target_y, policy.roster, '
                                    'policy.controller, policy.opponent)\n'
                                    "_put(state, 'f376', force)\n"
                                    "_put(state, 'f740', message)\n"
                                    'result = _call(state, 155876, policy, 140098)\n'
                                    "_put(state, 'f376', saved_force)\n"
                                    'return replace(result, target_x=saved[0], target_y=saved[1], '
                                    'roster=saved[2], controller=saved[3], opponent=saved[4])'},
 'apply_force_supply_losses': {'signature': 'state: SceneState, policy: BattlePolicy',
                               'returns': 'BattlePolicy',
                               'flow': 'from .services import sample_random_pair\n'
                                       'checked_context(policy, BattlePolicy, state)\n'
                                       'if policy.roster is None or policy.controller is None or '
                                       'policy.opponent is None:\n'
                                       "    raise Boundary('actual force roster, troops and readiness "
                                       "required')\n"
                                       'sample_random_pair(state)\n'
                                       "sample = _word(state, 'f61c')\n"
                                       'readiness_loss = replace_word(swap_words(u32(sample * 3)), '
                                       'u16(low16(swap_words(u32(sample * 3))) + 3))\n'
                                       'troop_rate = replace_word(swap_words(u32(sample * 11)), '
                                       'u16(low16(swap_words(u32(sample * 11))) + 20))\n'
                                       'policy = replace(policy, target_x=readiness_loss, '
                                       'target_y=troop_rate, unit=sample)\n'
                                       'while True:\n'
                                       '    unit = replace_word(policy.unit, '
                                       'policy.roster.next_word())\n'
                                       '    policy = replace(policy, unit=unit)\n'
                                       '    if negative_word(low16(unit)):\n'
                                       '        return policy\n'
                                       '    unit = replace_word(unit, u16((low16(unit) & 255) << 1))\n'
                                       '    old = policy.opponent.word(low16(unit))\n'
                                       '    result = u16(old - low16(policy.target_x))\n'
                                       '    policy.opponent.set_word(low16(unit), result)\n'
                                       '    if old >= low16(policy.target_x) and result != 0:\n'
                                       '        unit = replace_word(unit, u16(low16(unit) << 1))\n'
                                       '        value = policy.controller.long(low16(unit))\n'
                                       '        count = divu_retained(u32(low16(value) * '
                                       'low16(policy.target_y)), 100) & 65535\n'
                                       '        policy.controller.set_long(low16(unit), '
                                       'u32(policy.controller.long(low16(unit)) - count))\n'
                                       '        policy = replace(policy, unit=unit, count=count)\n'
                                       '        continue\n'
                                       '    unit = replace_word(unit, low16(unit) >> 1)\n'
                                       "    assignments = _ram(state, 'cc00')\n"
                                       '    count = replace_byte(policy.count, '
                                       'assignments.byte(low16(unit)))\n'
                                       '    assignments.set_byte(low16(unit), 255)\n'
                                       '    compact = state.table_at(policy.roster.base).cursor()\n'
                                       '    while True:\n'
                                       '        following = compact.next_word()\n'
                                       '        compact.set_word(65532, following)\n'
                                       '        if negative_word(following):\n'
                                       '            break\n'
                                       '    policy.roster.base = u32(policy.roster.base - 2)\n'
                                       '    count = replace_word(count, low16(count) & 63)\n'
                                       "    rulers = _ram(state, 'f427')\n"
                                       '    count = replace_byte(count, rulers.byte(low16(count)))\n'
                                       '    count = replace_word(count, low16(count) & 15)\n'
                                       '    policy = replace(policy, unit=unit, count=count, '
                                       'scratch=rulers)\n'
                                       "    if low16(count) in (_word(state, 'f67a'), _word(state, "
                                       "'f67c'), _word(state, 'f67e')):\n"
                                       "        _put(state, 'f3d0', unit)\n"
                                       '        policy = _present_supply_notice(state, policy, '
                                       'low16(count), 202)\n'
                                       '        continue\n'
                                       "    count = replace_word(policy.count, u16(_word(state, 'f68a') "
                                       '<< 1))\n'
                                       '    policy = replace(policy, count=count, '
                                       "candidates=_ram(state, 'f45e').cursor())\n"
                                       "    if low16(unit) == _ram(state, 'f45e').word(low16(count)):\n"
                                       '        policy = _present_supply_notice(state, policy, '
                                       "_word(state, 'f68c'), 323)\n"
                                       '        continue\n'
                                       "    count = replace_word(count, _word(state, 'f68a'))\n"
                                       '    policy = replace(policy, count=count, '
                                       "candidates=_ram(state, 'a027').cursor())\n"
                                       "    if low8(unit) == _ram(state, 'a027').byte(low16(count)):\n"
                                       '        policy = _present_supply_notice(state, policy, '
                                       "_word(state, 'f68e'), 322)"},
 'check_battle_commanders_present': {'signature': 'state: SceneState, policy: BattlePolicy',
                                     'returns': 'BattlePolicy',
                                     'flow': 'checked_context(policy, BattlePolicy, state)\n'
                                             "assignments = _ram(state, 'cc00')\n"
                                             "commanders = _ram(state, 'a027').cursor()\n"
                                             "x = replace_word(policy.target_x, _word(state, 'f68a'))\n"
                                             'y = replace_byte(replace_word(policy.target_y, 0), '
                                             "commanders.byte(low16(x)))\n"
                                             'if assignments.byte(low16(y)) == 255:\n'
                                             '    _carry(state, True)\n'
                                             '    return replace(policy, target_x=x, target_y=y, '
                                             "candidates=assignments.cursor(), roster=commanders)\n"
                                             "x = replace_word(x, u16(_word(state, 'f68a') << 1))\n"
                                             "commanders = _ram(state, 'f45e').cursor()\n"
                                             "x = replace_byte(x, commanders.byte(low16(x)))\n"
                                             '_carry(state, assignments.byte(low16(x)) == 255)\n'
                                             'return replace(policy, target_x=x, target_y=y, '
                                             'candidates=assignments.cursor(), roster=commanders)'},
 'calculate_force_supply_budgets': {'signature': 'state: SceneState, policy: BattlePolicy',
                                    'returns': 'BattlePolicy',
                                    'flow': 'checked_context(policy, BattlePolicy, state)\n'
                                            "first, second = (_ram(state, 'a550').cursor(), _ram(state, "
                                            "'a5a4').cursor())\n"
                                            "if _ram(state, 'f6d7').byte() & 2:\n"
                                            '    first, second = (second, first)\n'
                                            "troops, unit, total = (_ram(state, 'c800'), "
                                            'policy.target_y, 0)\n'
                                            "for roster, destination in ((first, 'f768'), (second, "
                                            "'f76c')):\n"
                                            '    total = 0\n'
                                            '    while True:\n'
                                            '        unit = replace_word(unit, roster.next_word())\n'
                                            '        if negative_word(low16(unit)):\n'
                                            '            break\n'
                                            '        unit = replace_word(unit, u16(low16(unit) << 2))\n'
                                            '        total = u32(total + troops.long(low16(unit)))\n'
                                            '        total = u32(total + 100)\n'
                                            '    total = divu_retained(total, 50)\n'
                                            '    unit = replace_word(unit, low16(total))\n'
                                            '    total = replace_word(total, u16((low16(total) << 1) + '
                                            'low16(unit))) & 65535\n'
                                            '    _ram(state, destination).set_long(0, total)\n'
                                            'return replace(policy, target_x=total, target_y=unit, '
                                            'roster=first, scan=second, opponent=troops)'},
 'execute_secondary_force_orders': {'signature': 'state: SceneState, policy: BattlePolicy',
                                    'returns': 'BattlePolicy',
                                    'flow': 'checked_context(policy, BattlePolicy, state)\n'
                                            'policy = _call(state, 150272, policy, 140316)\n'
                                            'policy = calculate_force_supply_budgets(state, policy)\n'
                                            "roster, orders = (_ram(state, 'a5a4').cursor(), "
                                            "_ram(state, 'af96').cursor())\n"
                                            'while True:\n'
                                            '    choice = replace_word(policy.choice, '
                                            'roster.next_word())\n'
                                            '    policy = replace(policy, choice=choice, roster=roster, '
                                            'candidates=orders)\n'
                                            '    if negative_word(low16(choice)):\n'
                                            "        _put(state, 'f362', 0)\n"
                                            '        return policy\n'
                                            '    x = replace_word(policy.target_x, orders.next_word())\n'
                                            '    policy = replace(policy, target_x=x)\n'
                                            '    if low16(x) == 255:\n'
                                            '        continue\n'
                                            '    x = replace_word(x, u16(low16(x) << 1))\n'
                                            '    policy = _indexed_call(state, replace(policy, '
                                            "target_x=x), x, 'data_022456', 140510, 140362)\n"
                                            '    policy = replace(policy, roster=roster, '
                                            'candidates=orders)'},
 'execute_primary_force_orders': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\npolicy = _enter_battle_policy_call(state, policy, 144742)\npolicy = _prepare_first_side_assignment_policy(state, policy)\npolicy = _leave_battle_policy_call(state, policy, 144742)\npolicy = calculate_force_supply_budgets(state, policy)\nroster, orders = (_ram(state, 'a550').cursor(), _ram(state, 'af82').cursor())\nwhile True:\n    policy = _call(state, 144844, replace(policy, roster=roster, candidates=orders), 144758)\n    if state.read_status_word() & 1 or _word(state, 'f612') == 1041:\n        break\n    choice = replace_word(policy.choice, roster.next_word())\n    policy = replace(policy, choice=choice)\n    if negative_word(low16(choice)):\n        break\n    x = replace_word(policy.target_x, orders.next_word())\n    policy = replace(policy, target_x=x)\n    if low16(x) == 255:\n        continue\n    _put(state, 'f770', x)\n    x = replace_word(x, u16(low16(x) << 1))\n    policy = _indexed_call(state, replace(policy, target_x=x), x, 'data_0235b6', 144912, 144810)\n    policy = replace(policy, roster=roster, candidates=orders)\n_put(state, 'f362', 0)\nreturn policy"},
 'process_both_battle_force_turns': {'signature': 'state: SceneState, policy: BattlePolicy',
                                     'returns': 'BattlePolicy',
                                     'flow': "checked_context(policy, BattlePolicy, state)\npolicy = check_battle_commanders_present(state, settle_both_force_supply(state, policy))\nif state.read_status_word() & 1:\n    return policy\nx = replace_word(policy.target_x, _word(state, 'f68c'))\npolicy = replace(policy, target_x=x)\nif low16(x) not in (_word(state, 'f67a'), _word(state, 'f67c'), _word(state, 'f67e')):\n    _word(state, 'f6d6')\n    _put(state, 'f6d6', 0)\n    policy = execute_primary_force_orders(state, policy)\nx = replace_word(policy.target_x, _word(state, 'f68e'))\npolicy = replace(policy, target_x=x)\nif low16(x) not in (_word(state, 'f67a'), _word(state, 'f67c'), _word(state, 'f67e')):\n    _put(state, 'f6d6', 2)\n    policy = execute_secondary_force_orders(state, policy)\nif _word(state, 'f612') != 1041:\n    _word(state, 'f6d6')\n    _put(state, 'f6d6', 0)\nreturn policy"},
 'select_primary_force_order_policy': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\nalternate = bool(_ram(state, 'f6d7').byte() & 2)\nstate.sr = state.sr & 65531 | (0 if alternate else 4)\nif alternate:\n    return _call_battle_policy_external(state, 150258, policy, 150238)\nentered = _enter_battle_policy_call(state, policy, 150246)\nreturned = _initialize_first_side_policy(state, entered)\nreturn _leave_battle_policy_call(state, returned, 150246)"},
 'initialize_battle_policy_targets': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\npolicy = _load_battle_policy_map(state, policy)\nreturn initialize_secondary_policy_targets(state, initialize_primary_policy_targets(state, policy))'},
 'initialize_primary_policy_targets': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\npolicy = _read_battle_policy_anchor(state, policy)\npolicy = _call(state, 154666, policy, 154608)\npolicy = replace(policy, scan=_ram(state, 'a550').cursor(), choice=replace_word(policy.choice, 2))\npolicy = collect_order_target_candidates(state, policy)\nreturn _call(state, 155128, policy, 154624)"},
 'initialize_secondary_policy_targets': {'signature': 'state: SceneState, policy: BattlePolicy',
                                         'returns': 'BattlePolicy',
                                         'flow': 'checked_context(policy, BattlePolicy, state)\n'
                                                 'policy = _call(state, 155402, policy, 155380)\n'
                                                 'policy = _call(state, 154666, policy, 155384)\n'
                                                 'policy = replace(policy, scan=_ram(state, '
                                                 "'a5a4').cursor(), choice=replace_word(policy.choice, "
                                                 '4))\n'
                                                 'policy = collect_order_target_candidates(state, '
                                                 'policy)\n'
                                                 'return _call(state, 155432, policy, 155400)'},
 'collect_order_target_candidates': {'signature': 'state: SceneState, policy: BattlePolicy',
                                     'returns': 'BattlePolicy',
                                     'flow': 'checked_context(policy, BattlePolicy, state)\n'
                                             'policy = replace(policy, candidates=_ram(state, '
                                             "'a150').cursor())\n"
                                             'policy = _call(state, 154780, policy, 154738)\n'
                                             'if state.read_status_word() & 1:\n'
                                             '    return policy\n'
                                             'while True:\n'
                                             '    policy = _call(state, 154808, policy, 154746)\n'
                                             '    if state.read_status_word() & 1:\n'
                                             '        return policy\n'
                                             '    policy = _call(state, 155030, policy, 154754)\n'
                                             '    if state.read_status_word() & 1:\n'
                                             '        return policy\n'
                                             '    policy = offset_first_order_target_axis(state, '
                                             'policy)\n'
                                             '    if state.read_status_word() & 1:\n'
                                             '        return policy\n'
                                             '    policy = offset_second_order_target_axis(state, '
                                             'policy)\n'
                                             '    if state.read_status_word() & 1:\n'
                                             '        return policy\n'
                                             '    policy = replace(policy, '
                                             'choice=replace_word(policy.choice, '
                                             'u16(low16(policy.choice) + 2)))'},
 'offset_first_order_target_axis': {'signature': 'state: SceneState, policy: BattlePolicy',
                                    'returns': 'BattlePolicy',
                                    'flow': 'checked_context(policy, BattlePolicy, state)\n'
                                            'unit = replace_word(policy.unit, u16(low16(policy.choice) '
                                            '+ low16(policy.target_x)))\n'
                                            'return _call(state, 154816, replace(policy, unit=unit), '
                                            '155118)'},
 'offset_second_order_target_axis': {'signature': 'state: SceneState, policy: BattlePolicy',
                                     'returns': 'BattlePolicy',
                                     'flow': 'checked_context(policy, BattlePolicy, state)\n'
                                             'count = replace_word(policy.count, '
                                             'u16(low16(policy.choice) + low16(policy.target_y)))\n'
                                             'return _call(state, 155034, replace(policy, count=count), '
                                             '155126)'},
 'cycle_setup_option': {'signature': 'state: SceneState, values: SetupValues',
 'returns': 'SetupValues',
 'flow': 'checked_context(values, SetupValues, state)\n'
         'option = values.tile\n'
         "if _ram(state, 'f603').byte() & 1:\n"
         '    if not low16(option):\n'
         '        return replace(values, tile=replace_word(option, low16(values.stride)))\n'
         '    option = replace_word(option, u16(low16(option) - 1))\n'
         '    if not low16(option):\n'
         '        return replace(values, tile=option)\n'
         "if _ram(state, 'f603').byte() & 2:\n"
         '    option = 0 if low16(option) == low16(values.stride) else replace_word(option, '
         'u16(low16(option) + 1))\n'
         'return replace(values, tile=option)'},
 '_update_setup_option': {'signature': 'state, values, expected, field, maximum, parameter',
 'returns': None,
 'flow': "if _word(state, '7022') != expected:\n"
         '    return values\n'
         'values = cycle_setup_option(state, replace(values, tile=replace_word(values.tile, '
         '_word(state, field)), stride=replace_word(values.stride, maximum)))\n'
         '_put(state, field, values.tile)\n'
         'return render_current_setup_option(state, replace(values, source=data_view(state, '
         'parameter).cursor()))'},
 'update_first_setup_option': {'signature': 'state: SceneState, values: SetupValues',
                               'returns': 'SetupValues',
                               'flow': 'checked_context(values, SetupValues, state)\n'
                                       "return _update_setup_option(state, values, 0, '7026', 2, "
                                       "'data_02b084')"},
 'update_second_setup_option': {'signature': 'state: SceneState, values: SetupValues',
                                'returns': 'SetupValues',
                                'flow': 'checked_context(values, SetupValues, state)\n'
                                        "return _update_setup_option(state, values, 1, '7024', 2, "
                                        "'data_02b0b6')"},
 'update_third_setup_option': {'signature': 'state: SceneState, values: SetupValues',
                               'returns': 'SetupValues',
                               'flow': 'checked_context(values, SetupValues, state)\n'
                                       "return _update_setup_option(state, values, 2, '7028', 1, "
                                       "'data_02b0e8')"},
 'update_fourth_setup_option': {'signature': 'state: SceneState, values: SetupValues',
                                'returns': 'SetupValues',
                                'flow': 'checked_context(values, SetupValues, state)\n'
                                        "return _update_setup_option(state, values, 3, '702a', 2, "
                                        "'data_02b084')"},
 '_setup_sprites': {'signature': 'state, values',
 'returns': None,
 'flow': 'from .services import append_map_sprites\n'
         'if values.source is None:\n'
         "    raise Boundary('actual readonly setup sprite source required')\n"
         'result = append_map_sprites(state, values.source, values.value, values.option, '
         'values.position, reset_scroll=True, initialize_clip=True)\n'
         'return replace(values, value=result.x, option=result.y, position=result.attributes, '
         'source=result.source)'},
 'update_setup_player_choices': {'signature': 'state: SceneState, values: SetupValues',
 'returns': 'SetupValues',
 'flow': 'checked_context(values, SetupValues, state)\n'
         "if _word(state, '7022') != 5 and _word(state, '7022') != 6:\n"
         "    if _word(state, '7022') != 4:\n"
         '        return values\n'
         "    if _ram(state, 'f603').byte() & 4:\n"
         "        if _word(state, '702c'):\n"
         "            _put(state, '702c', u16(_word(state, '702c') - 1))\n"
         '        else:\n'
         "            _put(state, '702c', 6)\n"
         "            if _word(state, '7026') == 2:\n"
         "                _put(state, '702c', 2)\n"
         "    elif _ram(state, 'f603').byte() & 8:\n"
         "        if _word(state, '7026') >= 2:\n"
         "            if _word(state, '702c') == 2:\n"
         "                _word(state, '702c')\n"
         "                _put(state, '702c', 0)\n"
         '            else:\n'
         "                _put(state, '702c', u16(_word(state, '702c') + 1))\n"
         "        elif _word(state, '702c') == 6:\n"
         "            _word(state, '702c')\n"
         "            _put(state, '702c', 0)\n"
         '        else:\n'
         "            _put(state, '702c', u16(_word(state, '702c') + 1))\n"
         'values = replace(values, position=0)\n'
         "if not _word(state, '7026'):\n"
         "    parameters = 'data_02b05a'\n"
         "elif _word(state, '7026') == 1:\n"
         "    parameters = 'data_02b06a'\n"
         'else:\n'
         "    parameters = 'data_02b07a'\n"
         'choices = data_view(state, parameters).cursor()\n'
         'while True:\n'
         '    value = replace_word(values.value, choices.next_word())\n'
         '    values = replace(values, value=value)\n'
         '    if low16(value) == 65535:\n'
         '        break\n'
         '    option = replace_word(values.option, low16(value) & 255)\n'
         '    value = replace_word(value, low16(value) >> 8 & 255)\n'
         '    values = _setup_sprites(state, replace(values, value=value, option=option, '
         "source=data_view(state, 'data_02b10e').cursor()))\n"
         "if _word(state, '7026') < 2:\n"
         '    values = _setup_sprites(state, replace(values, value=replace_word(values.value, '
         '176), option=replace_word(values.option, 256), source=data_view(state, '
         "'data_02b10e').cursor()))\n"
         "if _word(state, '7022') == 6:\n"
         '    from .business_scene_support import cycle_third_player_choice\n'
         '    values = cycle_third_player_choice(state, replace(values, '
         "tile=replace_word(values.tile, _word(state, '7030'))))\n"
         "    _put(state, '7030', values.tile)\n"
         "if _word(state, '7022') < 5:\n"
         "    _word(state, '702e')\n"
         "    _put(state, '702e', 0)\n"
         "if _word(state, '7022') == 5:\n"
         '    from .business_scene_support import cycle_second_player_choice\n'
         '    values = cycle_second_player_choice(state, replace(values, '
         "tile=replace_word(values.tile, _word(state, '702e'))))\n"
         "    _put(state, '702e', values.tile)\n"
         "    _word(state, '7030')\n"
         "    _put(state, '7030', 0)\n"
         'return values'},
 'render_current_setup_option': {'signature': 'state: SceneState, values: SetupValues',
 'returns': 'SetupValues',
 'flow': 'checked_context(values, SetupValues, state)\n'
         "tile = replace_word(values.tile, _word(state, '7022'))\n"
         'if low16(tile) == 5:\n'
         '    return replace(values, tile=tile)\n'
         'tile = replace_word(tile, u16(low16(tile) << 1))\n'
         "coordinates = data_view(state, 'data_02b050').cursor()\n"
         'option = replace_word(values.option, coordinates.word(low16(tile)))\n'
         'value = replace_word(values.value, low16(option) >> 8 & 255)\n'
         'option = replace_word(option, low16(option) & 255)\n'
         'return _setup_sprites(state, replace(values, tile=tile, option=option, value=value, '
         'position=0, destination=coordinates))'},
 'advance_setup_reveal': {'signature': 'state: SceneState, values: SetupValues',
                          'returns': 'SetupValues',
                          'flow': 'checked_context(values, SetupValues, state)\n'
                                  "if _word(state, '7040') >= 16:\n"
                                  '    return values\n'
                                  "value = replace_word(values.value, u16(15 - _word(state, '7040')))\n"
                                  'values = _call(state, 56998, replace(values, value=value, '
                                  'position=replace_word(values.position, 64), source=data_view(state, '
                                  "'data_02b46e').cursor()), 176094)\n"
                                  "_put(state, '7040', u16(_word(state, '7040') + 1))\n"
                                  'return values'},
 'advance_setup_dismissal': {'signature': 'state: SceneState, values: SetupValues',
                             'returns': 'SetupValues',
                             'flow': 'checked_context(values, SetupValues, state)\n'
                                     "if not _word(state, '703e') or _word(state, '7042') >= 16:\n"
                                     '    return values\n'
                                     'values = _call(state, 56998, replace(values, '
                                     "value=replace_word(values.value, _word(state, '7042')), "
                                     'position=replace_word(values.position, 64), '
                                     "source=data_view(state, 'data_02b46e').cursor()), 176146)\n"
                                     "_put(state, '7042', u16(_word(state, '7042') + 1))\n"
                                     'return values'},
 'write_setup_video_address': {'signature': 'state: SceneState, plane: SetupPlane',
                               'returns': 'SetupPlane',
                               'flow': 'checked_context(plane, SetupPlane, state)\n'
                                       'address = low16(plane.command)\n'
                                       'command = u32((address & 16383 | 16384) << 16) | address >> 14\n'
                                       'state.write(12582916, 4, command)\n'
                                       'return replace(plane, command=command)'},
 'advance_setup_plane_row': {'signature': 'state: SceneState, plane: SetupPlane',
                             'returns': 'SetupPlane',
                             'flow': 'checked_context(plane, SetupPlane, state)\n'
                                     'column = replace_word(plane.column, u16(low16(plane.column) + '
                                     '1))\n'
                                     'plane = replace(plane, column=column)\n'
                                     'if low8(column) >= 32:\n'
                                     '    address = plane.video_address.advance_full(plane.row_stride)\n'
                                     '    plane = write_setup_video_address(state, replace(plane, '
                                     'video_address=address, command=replace_word(plane.command, '
                                     'address.word)))\n'
                                     '    plane = replace(plane, column=0)\n'
                                     'return plane'},
 'decode_setup_plane_rows': {'signature': 'state: SceneState, plane: SetupPlane',
                             'returns': 'SetupPlane',
                             'flow': 'checked_context(plane, SetupPlane, state)\n'
                                     "_put(state, '7008', 32768)\n"
                                     "_put(state, '700c', 65535)\n"
                                     'return decode_setup_plane_rows_with_masks(state, plane)'},
 'decode_setup_plane_rows_with_masks': {'signature': 'state: SceneState, plane: SetupPlane',
                                        'returns': 'SetupPlane',
                                        'flow': 'checked_context(plane, SetupPlane, state)\n'
                                                'state.write(12582916, 2, 36610)\n'
                                                'plane = write_setup_video_address(state, '
                                                'replace(plane, command=replace_word(plane.command, '
                                                'plane.video_address.word), column=0))\n'
                                                'while True:\n'
                                                '    marker = replace_byte(plane.marker, '
                                                'plane.source.next_byte())\n'
                                                '    tile = replace_byte(plane.tile, '
                                                'plane.source.next_byte())\n'
                                                '    plane = replace(plane, marker=marker, tile=tile)\n'
                                                '    if low8(marker) != low8(tile):\n'
                                                '        tile = replace_word(tile, u16(low16(tile) << '
                                                '8))\n'
                                                '        tile = replace_byte(tile, '
                                                'plane.source.next_byte())\n'
                                                '        tile = replace_word(tile, low16(tile) | '
                                                "_word(state, '7008'))\n"
                                                '        tile = replace_word(tile, low16(tile) & '
                                                "_word(state, '700c'))\n"
                                                '        state.write(12582912, 2, low16(tile))\n'
                                                '        plane = advance_setup_plane_row(state, '
                                                'replace(plane, tile=tile))\n'
                                                '    else:\n'
                                                '        repeat = plane.source.next_byte()\n'
                                                '        plane = replace(plane, repeat_count=repeat)\n'
                                                '        if not repeat:\n'
                                                '            return plane\n'
                                                '        tile = replace_byte(tile, '
                                                'plane.source.next_byte())\n'
                                                '        tile = replace_word(tile, u16(low16(tile) << '
                                                '8))\n'
                                                '        tile = replace_byte(tile, '
                                                'plane.source.next_byte())\n'
                                                '        tile = replace_word(tile, low16(tile) | '
                                                "_word(state, '7008'))\n"
                                                '        tile = replace_word(tile, low16(tile) & '
                                                "_word(state, '700c'))\n"
                                                '        plane = replace(plane, tile=tile)\n'
                                                '        for count in descending_inclusive(repeat):\n'
                                                '            state.write(12582912, 2, '
                                                'low16(plane.tile))\n'
                                                '            plane = advance_setup_plane_row(state, '
                                                'replace(plane, repeat_count=count))\n'
                                                '        plane = replace(plane, repeat_count=65535)'},
 'initialize_setup_video': {'signature': 'state: SceneState, values: SetupValues',
                            'returns': 'SetupValues',
                            'flow': 'checked_context(values, SetupValues, state)\n'
                                    'for command in (33336, 33596, 33798, 34174, 36610, 35969, 36865, '
                                    '37120, 37376):\n'
                                    '    state.write(12582916, 2, command)\n'
                                    "for name in ('f312', 'f314', 'f316', 'f318'):\n"
                                    '    _put(state, name, 0)\n'
                                    'state.write(12582916, 4, 1075838976)\n'
                                    'for _ in descending_inclusive(63):\n'
                                    '    state.write(12582912, 4, 286331153)\n'
                                    'state.write(12582916, 4, 1342177280)\n'
                                    'for _ in descending_inclusive(63):\n'
                                    '    state.write(12582912, 4, 572662306)\n'
                                    "source = data_view(state, 'data_02b4ee').cursor()\n"
                                    'state.write(12582916, 4, 1610612737)\n'
                                    'for _ in descending_inclusive(2047):\n'
                                    '    state.write(12582912, 4, source.next_long())\n'
                                    "source = data_view(state, 'data_02d4ee').cursor()\n"
                                    'state.write(12582916, 4, 1073741826)\n'
                                    'for _ in descending_inclusive(2047):\n'
                                    '    state.write(12582912, 4, source.next_long())\n'
                                    "first, second = ('data_02f4ee', 'data_02fa03') if not _word(state, "
                                    "'7036') else ('data_02fb8e', 'data_02fdef')\n"
                                    'plane = SetupPlane(replace_word(values.value, 65535), '
                                    'values.position, 572662306, values.rows, values.tile, 128, source, '
                                    'VideoPlaneAddress(57344))\n'
                                    'plane = decode_setup_plane_rows(state, replace(plane, '
                                    'source=data_view(state, first).cursor()))\n'
                                    'plane = decode_setup_plane_rows(state, replace(plane, '
                                    'source=data_view(state, second).cursor(), '
                                    'video_address=VideoPlaneAddress(57408)))\n'
                                    "_put(state, '7008', 0)\n"
                                    "_put(state, '700c', 65535)\n"
                                    'plane = decode_setup_plane_rows_with_masks(state, replace(plane, '
                                    "source=data_view(state, 'data_02ff1a').cursor(), "
                                    'video_address=VideoPlaneAddress(49152)))\n'
                                    "_put(state, '7008', 0)\n"
                                    "_put(state, '700c', 65535)\n"
                                    'plane = decode_setup_plane_rows_with_masks(state, replace(plane, '
                                    "source=data_view(state, 'data_02ffb9').cursor(), "
                                    'video_address=VideoPlaneAddress(49216)))\n'
                                    "source, destination = (data_view(state, 'data_02b46e').cursor(), "
                                    "_ram(state, 'fb00').cursor())\n"
                                    'for _ in descending_inclusive(31):\n'
                                    '    destination.append_long(source.next_long())\n'
                                    'return replace(values, value=replace_word(plane.command, 65535), '
                                    'position=plane.marker, attributes=plane.tile, '
                                    'rows=plane.repeat_count, tile=plane.column, '
                                    'option=plane.row_stride, source=source, destination=destination)'}}

def _lower_settle_city_projects_and_refresh_map(emitter,rules):
    emitter.segment(0x1190e,0x119a4)
    emitter.ins('bsr.w','main_pc_0119aa',4)
    emitter.ins('bsr.w','main_pc_011cca',4)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x1f,%d3',4)
    emitter.ins('move.l','#0x11111111,(%a1)+',6)
    emitter.ins('dbra','%d3,main_pc_01191e',4)
    emitter.ins('lea.l','122(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','#0x1,%d0',4)
    emitter.ins('move.w','#0x3,%d1',4)
    emitter.ins('move.w','#0x2,%d3',4)
    emitter.ins('jsr','main_pc_00ae8a:l',6)
    emitter.ins('move.l','#0x40200000,0xc00004:l',10)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x7f,%d3',4)
    emitter.ins('move.l','(%a1)+,0xc00000:l',6)
    emitter.ins('dbra','%d3,main_pc_011952',4)
    emitter.ins('jsr','main_pc_0055b0:l',6)
    emitter.ins('move.w','#0xc,0xf362:w',6)
    emitter.ins('jsr','main_pc_030a74:l',6)
    emitter.ins('tst.w','0xf386:w',4)
    emitter.ins('bne.w','main_pc_01197c',4)
    emitter.ins('jsr','main_pc_0083fa:l',6)
    emitter.ins('move.w','#0x208,0xf612:w',6)
    emitter.ins('move.w','#0x13,0xf362:w',6)
    emitter.ins('clr.w','0xf36a:w',4)
    emitter.ins('move.w','#0x20a,0xf3c2:w',6)
    emitter.ins('clr.w','0xf3c4:w',4)
    emitter.ins('clr.w','0xcea0:w',4)
    emitter.ins('move.w','#0xffff,0xff3000:l',8)
    emitter.ins('rts','',2)

def _lower_settle_all_city_projects(emitter,rules):
    emitter.segment(0x119aa,0x119d0)
    emitter.ins('clr.w','0xf364:w',4)
    emitter.ins('lea.l','0xcc00:w,%a6',4)
    emitter.ins('lea.l','0xcd00:w,%a5',4)
    emitter.ins('addq.w','#0x1,0xf364:w',4)
    emitter.ins('bsr.w','main_pc_0119d0',4)
    emitter.ins('bsr.w','main_pc_011aa8',4)
    emitter.ins('bsr.w','main_pc_011bc6',4)
    emitter.ins('cmpi.w','#0x28,0xf364:w',6)
    emitter.ins('bcs.b','main_pc_0119b6',2)
    emitter.ins('rts','',2)

def _lower_settle_first_city_project(emitter,rules):
    emitter.segment(0x119d0,0x11aa8)
    emitter.ins('move.w','0xf364:w,%d0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('add.w','0xf364:w,%d0',4)
    emitter.ins('lsl.w','#0x2,%d0',2)
    emitter.ins('lea.l','0xe80c:w,%a0',4)
    emitter.ins('movem.w','(%a0, %d0.w),%d2-%d3',6)
    emitter.ins('tst.w','%d2',2)
    emitter.ins('bmi.w','main_pc_011a8e',4)
    emitter.ins('move.b','(%a6, %d2.w),%d4',4)
    emitter.ins('cmp.b','0xf365:w,%d4',4)
    emitter.ins('bne.w','main_pc_011a9c',4)
    emitter.ins('move.w','0xf364:w,%d1',4)
    emitter.ins('lsl.w','#0x2,%d1',2)
    emitter.ins('lea.l','0xdffc:w,%a1',4)
    emitter.ins('move.l','(%a1, %d1.w),%d4',4)
    emitter.ins('sub.l','%d3,%d4',2)
    emitter.ins('bcs.w','main_pc_011a90',4)
    emitter.ins('move.l','%d4,(%a1, %d1.w)',4)
    emitter.ins('move.l','%d3,%d4',2)
    emitter.ins('divu.w','#0x5,%d4',4)
    emitter.ins('move.w','%d2,%d1',2)
    emitter.ins('lsl.w','#0x1,%d1',2)
    emitter.ins('lea.l','0xb600:w,%a0',4)
    emitter.ins('add.w','(%a0, %d1.w),%d4',4)
    emitter.ins('lea.l','0xbe00:w,%a0',4)
    emitter.ins('move.w','(%a0, %d1.w),%d1',4)
    emitter.ins('lsr.w','#0x1,%d1',2)
    emitter.ins('add.w','%d1,%d4',2)
    emitter.ins('jsr','main_pc_0083d4:l',6)
    emitter.ins('andi.l','#0xffff,%d0',6)
    emitter.ins('move.l','%d0,%d1',2)
    emitter.ins('lsl.l','#0x1,%d0',2)
    emitter.ins('add.l','%d1,%d0',2)
    emitter.ins('lsl.l','#0x1,%d0',2)
    emitter.ins('swap','%d0',2)
    emitter.ins('addi.w','#0xa,%d0',4)
    emitter.ins('mulu.w','%d0,%d4',2)
    emitter.ins('divu.w','#0x3e8,%d4',4)
    emitter.ins('ext.l','%d4',2)
    emitter.ins('move.w','0xf364:w,%d1',4)
    emitter.ins('lsl.w','#0x2,%d1',2)
    emitter.ins('lea.l','0xe1dc:w,%a0',4)
    emitter.ins('move.l','(%a0, %d1.w),%d3',4)
    emitter.ins('add.l','%d4,%d3',2)
    emitter.ins('cmpi.l','#0x3e7,%d3',6)
    emitter.ins('bls.w','main_pc_011a6e',4)
    emitter.ins('move.w','#0x3e7,%d3',4)
    emitter.ins('move.l','%d3,(%a0, %d1.w)',4)
    emitter.ins('lsl.l','#0x1,%d2',2)
    emitter.ins('lea.l','0xbe00:w,%a0',4)
    emitter.ins('move.w','(%a0, %d2.w),%d0',4)
    emitter.ins('add.w','%d4,%d0',2)
    emitter.ins('cmpi.w','#0x3e7,%d0',4)
    emitter.ins('bls.w','main_pc_011a8a',4)
    emitter.ins('move.w','#0x3e7,%d0',4)
    emitter.ins('move.w','%d0,(%a0, %d2.w)',4)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0xffff,(%a0, %d0.w)',6)
    emitter.ins('clr.b','(%a5, %d2.w)',4)
    emitter.ins('bra.b','main_pc_011a8e',2)
    emitter.ins('move.w','#0xffff,(%a0, %d0.w)',6)
    emitter.ins('clr.b','(%a5, %d2.w)',4)
    emitter.ins('bra.b','main_pc_011a8e',2)

def _lower_settle_second_city_project(emitter,rules):
    emitter.segment(0x11aa8,0x11bc6)
    emitter.ins('move.w','0xf364:w,%d0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('add.w','0xf364:w,%d0',4)
    emitter.ins('lsl.w','#0x2,%d0',2)
    emitter.ins('lea.l','0xe810:w,%a0',4)
    emitter.ins('movem.w','(%a0, %d0.w),%d2-%d3',6)
    emitter.ins('tst.w','%d2',2)
    emitter.ins('bmi.w','main_pc_011bac',4)
    emitter.ins('move.b','(%a6, %d2.w),%d4',4)
    emitter.ins('cmp.b','0xf365:w,%d4',4)
    emitter.ins('bne.w','main_pc_011bba',4)
    emitter.ins('move.w','0xf364:w,%d1',4)
    emitter.ins('lsl.w','#0x2,%d1',2)
    emitter.ins('lea.l','0xdffc:w,%a1',4)
    emitter.ins('move.l','(%a1, %d1.w),%d4',4)
    emitter.ins('sub.l','%d3,%d4',2)
    emitter.ins('bcs.w','main_pc_011bae',4)
    emitter.ins('move.l','%d4,(%a1, %d1.w)',4)
    emitter.ins('move.l','%d3,%d4',2)
    emitter.ins('divu.w','#0x5,%d4',4)
    emitter.ins('move.w','%d2,%d1',2)
    emitter.ins('lsl.w','#0x1,%d1',2)
    emitter.ins('lea.l','0xb600:w,%a0',4)
    emitter.ins('add.w','(%a0, %d1.w),%d4',4)
    emitter.ins('lea.l','0xbe00:w,%a0',4)
    emitter.ins('move.w','(%a0, %d1.w),%d1',4)
    emitter.ins('lsr.w','#0x1,%d1',2)
    emitter.ins('add.w','%d1,%d4',2)
    emitter.ins('jsr','main_pc_0083d4:l',6)
    emitter.ins('andi.l','#0xffff,%d0',6)
    emitter.ins('lsl.l','#0x2,%d0',2)
    emitter.ins('swap','%d0',2)
    emitter.ins('move.w','#0x8,%d5',4)
    emitter.ins('move.w','0xf364:w,%d6',4)
    emitter.ins('lsl.w','#0x2,%d6',2)
    emitter.ins('lea.l','0xe31c:w,%a1',4)
    emitter.ins('cmpi.l','#0x50,(%a1, %d6.w)',8)
    emitter.ins('bcs.b','main_pc_011b32',2)
    emitter.ins('move.w','#0x2,%d5',4)
    emitter.ins('add.w','%d5,%d0',2)
    emitter.ins('mulu.w','%d0,%d4',2)
    emitter.ins('lea.l','0xc200:w,%a0',4)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.b','(%a0, %d2.w),%d0',4)
    emitter.ins('move.w','%d4,%d1',2)
    emitter.ins('mulu.w','%d0,%d1',2)
    emitter.ins('swap','%d4',2)
    emitter.ins('mulu.w','%d0,%d4',2)
    emitter.ins('swap','%d4',2)
    emitter.ins('add.l','%d1,%d4',2)
    emitter.ins('divu.w','#0xea60,%d4',4)
    emitter.ins('ext.l','%d4',2)
    emitter.ins('move.w','0xf364:w,%d1',4)
    emitter.ins('lsl.w','#0x2,%d1',2)
    emitter.ins('lea.l','0xe31c:w,%a0',4)
    emitter.ins('move.l','(%a0, %d1.w),%d0',4)
    emitter.ins('add.l','%d4,%d0',2)
    emitter.ins('cmpi.w','#0x64,%d0',4)
    emitter.ins('bls.b','main_pc_011b6c',2)
    emitter.ins('move.w','#0x64,%d0',4)
    emitter.ins('move.l','%d0,(%a0, %d1.w)',4)
    emitter.ins('lsl.l','#0x1,%d2',2)
    emitter.ins('lea.l','0xbe00:w,%a0',4)
    emitter.ins('move.w','(%a0, %d2.w),%d0',4)
    emitter.ins('add.w','%d4,%d0',2)
    emitter.ins('cmpi.w','#0x3e7,%d0',4)
    emitter.ins('bls.w','main_pc_011b88',4)
    emitter.ins('move.w','#0x3e7,%d0',4)
    emitter.ins('move.w','%d0,(%a0, %d2.w)',4)
    emitter.ins('cmpi.w','#0x5,%d4',4)
    emitter.ins('bcs.w','main_pc_011bac',4)
    emitter.ins('lea.l','0xc200:w,%a0',4)
    emitter.ins('lsr.w','#0x1,%d2',2)
    emitter.ins('move.b','(%a0, %d2.w),%d0',4)
    emitter.ins('addq.w','#0x1,%d0',2)
    emitter.ins('cmpi.w','#0x64,%d0',4)
    emitter.ins('bhi.w','main_pc_011bac',4)
    emitter.ins('move.b','%d0,(%a0, %d2.w)',4)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0xffff,(%a0, %d0.w)',6)
    emitter.ins('clr.b','(%a5, %d2.w)',4)
    emitter.ins('bra.b','main_pc_011bac',2)
    emitter.ins('move.w','#0xffff,(%a0, %d0.w)',6)
    emitter.ins('clr.b','(%a5, %d2.w)',4)
    emitter.ins('bra.b','main_pc_011bac',2)

def _lower_settle_third_city_project(emitter,rules):
    emitter.segment(0x11bc6,0x11c8c)
    emitter.ins('move.w','0xf364:w,%d0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('add.w','0xf364:w,%d0',4)
    emitter.ins('lsl.w','#0x2,%d0',2)
    emitter.ins('lea.l','0xe814:w,%a0',4)
    emitter.ins('movem.w','(%a0, %d0.w),%d2-%d3',6)
    emitter.ins('tst.w','%d2',2)
    emitter.ins('bmi.w','main_pc_011c72',4)
    emitter.ins('move.b','(%a6, %d2.w),%d4',4)
    emitter.ins('cmp.b','0xf365:w,%d4',4)
    emitter.ins('bne.w','main_pc_011c80',4)
    emitter.ins('mulu.w','#0x64,%d3',4)
    emitter.ins('move.w','0xf364:w,%d1',4)
    emitter.ins('lsl.w','#0x2,%d1',2)
    emitter.ins('lea.l','0xdffc:w,%a1',4)
    emitter.ins('move.l','(%a1, %d1.w),%d4',4)
    emitter.ins('sub.l','%d3,%d4',2)
    emitter.ins('bcs.w','main_pc_011c74',4)
    emitter.ins('move.l','%d4,(%a1, %d1.w)',4)
    emitter.ins('divu.w','#0x32,%d3',4)
    emitter.ins('move.w','%d2,%d1',2)
    emitter.ins('lsl.w','#0x1,%d1',2)
    emitter.ins('lea.l','0xb600:w,%a0',4)
    emitter.ins('add.w','(%a0, %d1.w),%d3',4)
    emitter.ins('lea.l','0xbe00:w,%a0',4)
    emitter.ins('move.w','(%a0, %d1.w),%d4',4)
    emitter.ins('lsr.w','#0x2,%d4',2)
    emitter.ins('add.w','%d4,%d3',2)
    emitter.ins('lea.l','0xc000:w,%a0',4)
    emitter.ins('move.w','(%a0, %d1.w),%d4',4)
    emitter.ins('lsr.w','#0x2,%d4',2)
    emitter.ins('add.w','%d4,%d3',2)
    emitter.ins('jsr','main_pc_0083d4:l',6)
    emitter.ins('andi.l','#0xffff,%d0',6)
    emitter.ins('move.l','%d0,%d1',2)
    emitter.ins('lsl.l','#0x1,%d0',2)
    emitter.ins('add.l','%d1,%d0',2)
    emitter.ins('swap','%d0',2)
    emitter.ins('addq.w','#0x6,%d0',2)
    emitter.ins('mulu.w','%d0,%d3',2)
    emitter.ins('divu.w','#0x3e8,%d3',4)
    emitter.ins('move.w','0xf364:w,%d0',4)
    emitter.ins('lsl.w','#0x2,%d0',2)
    emitter.ins('lea.l','0xe59c:w,%a0',4)
    emitter.ins('move.w','0x2(%a0, %d0.w),%d7',4)
    emitter.ins('add.w','%d3,%d7',2)
    emitter.ins('cmpi.w','#0x64,%d7',4)
    emitter.ins('bls.w','main_pc_011c6a',4)
    emitter.ins('move.w','#0x64,%d7',4)
    emitter.ins('move.w','%d7,0x2(%a0, %d0.w)',4)
    emitter.ins('bsr.w','main_pc_011c8c',4)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0xffff,(%a0, %d0.w)',6)
    emitter.ins('clr.b','(%a5, %d2.w)',4)
    emitter.ins('bra.b','main_pc_011c72',2)
    emitter.ins('move.w','#0xffff,(%a0, %d0.w)',6)
    emitter.ins('clr.b','(%a5, %d2.w)',4)
    emitter.ins('bra.b','main_pc_011c72',2)

def _lower_dispatch_gameplay_command_state(emitter,rules):
    emitter.segment(0x13d48,0x13d58)
    emitter.ins('move.w','0xf362:w,%d0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','8(%pc, %d0.w),%d0',4)
    emitter.ins('jsr','38(%pc, %d0.w)',4)
    emitter.ins('rts','',2)

def _lower_render_visible_map_packets(emitter,rules):
    emitter.segment(0x15de6,0x15e3e)
    emitter.ins('lea.l','0x9000:w,%a2',4)
    emitter.ins('move.b','(%a2),%d4',2)
    emitter.ins('beq.w','main_pc_015e38',4)
    emitter.ins('btst.l','#0x5,%d4',4)
    emitter.ins('bne.b','main_pc_015e2a',2)
    emitter.ins('clr.w','%d5',2)
    emitter.ins('move.b','0x1(%a2),%d5',4)
    emitter.ins('lsl.w','#0x4,%d5',2)
    emitter.ins('addi.w','#0x10,%d5',4)
    emitter.ins('sub.w','0xf314:w,%d5',4)
    emitter.ins('bcs.b','main_pc_015e2a',2)
    emitter.ins('cmpi.w','#0xf0,%d5',4)
    emitter.ins('bcc.b','main_pc_015e2a',2)
    emitter.ins('clr.w','%d5',2)
    emitter.ins('move.b','0x2(%a2),%d5',4)
    emitter.ins('lsl.w','#0x4,%d5',2)
    emitter.ins('addi.w','#0x10,%d5',4)
    emitter.ins('sub.w','0xf318:w,%d5',4)
    emitter.ins('bcs.b','main_pc_015e2a',2)
    emitter.ins('cmpi.w','#0x150,%d5',4)
    emitter.ins('bcc.b','main_pc_015e2a',2)
    emitter.ins('bsr.w','main_pc_015e3e',4)
    emitter.ins('clr.w','%d5',2)
    emitter.ins('move.b','(%a2),%d5',2)
    emitter.ins('andi.w','#0xf,%d5',4)
    emitter.ins('lea.l','0xd(%a2, %d5.w),%a2',4)
    emitter.ins('bra.b','main_pc_015dea',2)
    emitter.ins('bsr.w','main_pc_015f1c',4)
    emitter.ins('rts','',2)

def _lower_render_selected_map_packet(emitter,rules):
    emitter.segment(0x15e3e,0x15e88)
    emitter.ins('cmpi.w','#0x2,0xf36c:w',6)
    emitter.ins('bne.b','main_pc_015e60',2)
    emitter.ins('move.b','0x4(%a2),%d0',4)
    emitter.ins('cmp.b','0xf377:w,%d0',4)
    emitter.ins('bne.b','main_pc_015e60',2)
    emitter.ins('move.b','(%a2),%d0',2)
    emitter.ins('btst.l','#0x4,%d0',4)
    emitter.ins('bne.b','main_pc_015e60',2)
    emitter.ins('btst.b','#0x2,0xf321:w',6)
    emitter.ins('bne.b','main_pc_015e86',2)
    emitter.ins('bsr.w','main_pc_015ed0',4)
    emitter.ins('bsr.w','main_pc_015e88',4)
    emitter.ins('clr.w','%d2',2)
    emitter.ins('tst.b','(%a2)',2)
    emitter.ins('bpl.w','main_pc_015e74',4)
    emitter.ins('move.w','#0x800,%d2',4)
    emitter.ins('move.w','0xf314:w,0xf60a:w',6)
    emitter.ins('move.w','0xf318:w,0xf60e:w',6)
    emitter.ins('jsr','main_pc_00ac10:l',6)
    emitter.ins('rts','',2)

def _lower_select_map_packet_sprite(emitter,rules):
    emitter.segment(0x15e88,0x15eb8)
    emitter.ins('lea.l','46(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('btst.b','#0x4,0xf321:w',6)
    emitter.ins('beq.w','main_pc_015e9c',4)
    emitter.ins('adda.w','#0x8,%a0',4)
    emitter.ins('movem.l','%d0-%d1/%a0/%a2,-(%a7)',4)
    emitter.ins('bsr.w','main_pc_014294',4)
    emitter.ins('movem.l','(%a7)+,%d0-%d1/%a0/%a2',4)
    emitter.ins('cmpi.w','#0x4,%d2',4)
    emitter.ins('bne.w','main_pc_015eb6',4)
    emitter.ins('lea.l','22(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('rts','',2)

def _lower_locate_map_packet_sprite(emitter,rules):
    emitter.segment(0x15ed0,0x15f1c)
    emitter.ins('cmpi.w','#0x209,0xf612:w',6)
    emitter.ins('bne.b','main_pc_015eec',2)
    emitter.ins('cmpi.w','#0x6,0xf362:w',6)
    emitter.ins('bne.b','main_pc_015eec',2)
    emitter.ins('move.w','0xff3bb4:l,%d0',6)
    emitter.ins('cmp.b','0xd(%a2),%d0',4)
    emitter.ins('beq.b','main_pc_015f06',2)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.b','0x1(%a2),%d0',4)
    emitter.ins('lsl.w','#0x4,%d0',2)
    emitter.ins('addi.w','#0x8,%d0',4)
    emitter.ins('clr.w','%d1',2)
    emitter.ins('move.b','0x2(%a2),%d1',4)
    emitter.ins('lsl.w','#0x4,%d1',2)
    emitter.ins('addi.w','#0x8,%d1',4)
    emitter.ins('bra.b','main_pc_015f1a',2)
    emitter.ins('move.w','0xff3bb6:l,%d0',6)
    emitter.ins('addi.w','#0x8,%d0',4)
    emitter.ins('move.w','0xff3bb8:l,%d1',6)
    emitter.ins('addi.w','#0x8,%d1',4)
    emitter.ins('rts','',2)

def _lower_render_map_marker_positions(emitter,rules):
    emitter.segment(0x15f1c,0x15f6a)
    emitter.ins('lea.l','0x9f00:w,%a1',4)
    emitter.ins('move.w','(%a1)+,%d0',2)
    emitter.ins('bmi.b','main_pc_015f68',2)
    emitter.ins('move.w','(%a1)+,%d1',2)
    emitter.ins('move.w','%d0,%d2',2)
    emitter.ins('addi.w','#0x10,%d2',4)
    emitter.ins('sub.w','0xf314:w,%d2',4)
    emitter.ins('bcs.w','main_pc_015f20',4)
    emitter.ins('cmpi.w','#0xf0,%d2',4)
    emitter.ins('bhi.b','main_pc_015f20',2)
    emitter.ins('move.w','%d1,%d2',2)
    emitter.ins('addi.w','#0x10,%d2',4)
    emitter.ins('sub.w','0xf318:w,%d2',4)
    emitter.ins('bcs.b','main_pc_015f20',2)
    emitter.ins('cmpi.w','#0x150,%d2',4)
    emitter.ins('bhi.b','main_pc_015f20',2)
    emitter.ins('lea.l','28(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('clr.w','%d2',2)
    emitter.ins('move.w','0xf314:w,0xf60a:w',6)
    emitter.ins('move.w','0xf318:w,0xf60e:w',6)
    emitter.ins('jsr','main_pc_00ac10:l',6)
    emitter.ins('bra.b','main_pc_015f20',2)
    emitter.ins('rts','',2)

def _lower_append_city_currency_panel(emitter,rules):
    emitter.segment(0x15f84,0x1605e)
    emitter.ins('lea.l','0xd100:w,%a0',4)
    emitter.ins('adda.w','0xf31a:w,%a0',4)
    emitter.ins('move.w','#0xc,0x1c(%a0)',6)
    emitter.ins('move.w','#0xc,(%a0)+',4)
    emitter.ins('move.w','#0xc234,0x1c(%a0)',6)
    emitter.ins('move.w','#0xc0b4,(%a0)+',4)
    emitter.ins('move.w','#0xd380,0x1c(%a0)',6)
    emitter.ins('move.w','#0xc380,(%a0)+',4)
    emitter.ins('move.w','#0x9,%d0',4)
    emitter.ins('move.w','#0xd381,0x1c(%a0)',6)
    emitter.ins('move.w','#0xc381,(%a0)+',4)
    emitter.ins('dbra','%d0,main_pc_015fae',4)
    emitter.ins('move.w','#0xdb80,0x1c(%a0)',6)
    emitter.ins('move.w','#0xcb80,(%a0)+',4)
    emitter.ins('adda.w','#0x1c,%a0',4)
    emitter.ins('move.w','#0xc,0x1c(%a0)',6)
    emitter.ins('move.w','#0xc,(%a0)+',4)
    emitter.ins('move.w','#0xc1b4,0x1c(%a0)',6)
    emitter.ins('move.w','#0xc134,(%a0)+',4)
    emitter.ins('move.w','#0xc382,0x1c(%a0)',6)
    emitter.ins('move.w','#0xc382,(%a0)+',4)
    emitter.ins('move.w','#0xc006,0x1c(%a0)',6)
    emitter.ins('move.w','#0xc005,(%a0)+',4)
    emitter.ins('move.w','#0xc008,0x1c(%a0)',6)
    emitter.ins('move.w','#0xc007,(%a0)+',4)
    emitter.ins('move.w','#0xc001,0x1c(%a0)',6)
    emitter.ins('move.w','#0xc001,(%a0)+',4)
    emitter.ins('move.w','#0xc001,0x1c(%a0)',6)
    emitter.ins('move.w','#0xc001,(%a0)+',4)
    emitter.ins('move.w','0xf364:w,%d0',4)
    emitter.ins('lsl.w','#0x2,%d0',2)
    emitter.ins('lea.l','0xe09c:w,%a1',4)
    emitter.ins('move.l','(%a1, %d0.w),%d0',4)
    emitter.ins('move.l','%d0,0xf3f8:w',4)
    emitter.ins('move.w','#0xc386,%d1',4)
    emitter.ins('move.w','#0xc001,%d2',4)
    emitter.ins('lea.l','0xd300:w,%a6',4)
    emitter.ins('jsr','main_pc_01270a:l',6)
    emitter.ins('move.w','#0x5,%d0',4)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','(%a1)+,0x1c(%a0)',4)
    emitter.ins('move.w','#0xc001,(%a0)+',4)
    emitter.ins('dbra','%d0,main_pc_01603c',4)
    emitter.ins('move.w','#0xcb82,0x1c(%a0)',6)
    emitter.ins('move.w','#0xcb82,(%a0)+',4)
    emitter.ins('clr.w','0x1c(%a0)',4)
    emitter.ins('addi.w','#0x70,0xf31a:w',6)
    emitter.ins('rts','',2)

def _lower_append_city_project_panel(emitter,rules):
    emitter.segment(0x1605e,0x1613c)
    emitter.ins('lea.l','0xd100:w,%a0',4)
    emitter.ins('adda.w','0xf31a:w,%a0',4)
    emitter.ins('move.w','#0xe,0x60(%a0)',6)
    emitter.ins('move.w','#0xe,0x40(%a0)',6)
    emitter.ins('move.w','#0xe,0x20(%a0)',6)
    emitter.ins('move.w','#0xe,(%a0)+',4)
    emitter.ins('move.w','#0xc71e,0x60(%a0)',6)
    emitter.ins('move.w','#0xc69e,0x40(%a0)',6)
    emitter.ins('move.w','#0xc61e,0x20(%a0)',6)
    emitter.ins('move.w','#0xc49e,(%a0)+',4)
    emitter.ins('move.w','#0xd380,0x60(%a0)',6)
    emitter.ins('move.w','#0xc382,0x40(%a0)',6)
    emitter.ins('move.w','#0xc382,0x20(%a0)',6)
    emitter.ins('move.w','#0xc380,(%a0)+',4)
    emitter.ins('move.w','#0xb,%d0',4)
    emitter.ins('move.w','#0xd381,0x60(%a0)',6)
    emitter.ins('move.w','#0xc001,0x40(%a0)',6)
    emitter.ins('move.w','#0xc001,0x20(%a0)',6)
    emitter.ins('move.w','#0xc381,(%a0)+',4)
    emitter.ins('dbra','%d0,main_pc_0160ac',4)
    emitter.ins('move.w','#0xdb80,0x60(%a0)',6)
    emitter.ins('move.w','#0xcb82,0x40(%a0)',6)
    emitter.ins('move.w','#0xcb82,0x20(%a0)',6)
    emitter.ins('move.w','#0xcb80,(%a0)+',4)
    emitter.ins('adda.w','#0x60,%a0',4)
    emitter.ins('move.w','#0xe,0x20(%a0)',6)
    emitter.ins('move.w','#0xe,(%a0)+',4)
    emitter.ins('move.w','#0xc59e,0x20(%a0)',6)
    emitter.ins('move.w','#0xc51e,(%a0)+',4)
    emitter.ins('move.w','#0xc382,0x20(%a0)',6)
    emitter.ins('move.w','#0xc382,(%a0)+',4)
    emitter.ins('move.w','#0xc009,%d1',4)
    emitter.ins('bsr.w','main_pc_01613c',4)
    emitter.ins('move.w','#0x3,%d0',4)
    emitter.ins('move.w','#0xc001,0x20(%a0)',6)
    emitter.ins('move.w','#0xc001,(%a0)+',4)
    emitter.ins('dbra','%d0,main_pc_01610a',4)
    emitter.ins('move.w','#0xc011,%d1',4)
    emitter.ins('bsr.w','main_pc_01613c',4)
    emitter.ins('move.w','#0xcb82,0x20(%a0)',6)
    emitter.ins('move.w','#0xcb82,(%a0)+',4)
    emitter.ins('clr.w','0x20(%a0)',4)
    emitter.ins('addi.w','#0xc0,0xf31a:w',6)
    emitter.ins('bset.b','#0x5,0xf3a5:w',6)
    emitter.ins('rts','',2)

def _lower_append_two_row_sequential_tiles(emitter,rules):
    emitter.segment(0x1613c,0x16152)
    emitter.ins('move.w','#0x3,%d0',4)
    emitter.ins('move.w','%d1,(%a0)',2)
    emitter.ins('addq.w','#0x1,%d1',2)
    emitter.ins('move.w','%d1,0x20(%a0)',4)
    emitter.ins('addq.w','#0x1,%d1',2)
    emitter.ins('addq.w','#0x2,%a0',2)
    emitter.ins('dbra','%d0,main_pc_016140',4)
    emitter.ins('rts','',2)

def _lower_append_current_city_value(emitter,rules):
    emitter.segment(0x161d4,0x1622e)
    emitter.ins('lea.l','0xd100:w,%a0',4)
    emitter.ins('adda.w','0xf31a:w,%a0',4)
    emitter.ins('move.w','#0x3,(%a0)+',4)
    emitter.ins('move.w','#0xc5aa,(%a0)+',4)
    emitter.ins('move.w','0xf670:w,%d0',4)
    emitter.ins('move.w','#0xc386,%d1',4)
    emitter.ins('clr.w','%d2',2)
    emitter.ins('lea.l','0xd300:w,%a6',4)
    emitter.ins('jsr','main_pc_01270a:l',6)
    emitter.ins('lea.l','0xd306:w,%a6',4)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.w','#0x2,%d1',4)
    emitter.ins('move.w','(%a6)+,%d2',2)
    emitter.ins('bne.w','main_pc_01621c',4)
    emitter.ins('cmp.w','0xf39a:w,%d0',4)
    emitter.ins('bcc.w','main_pc_016218',4)
    emitter.ins('move.w','#0xc001,%d2',4)
    emitter.ins('bra.w','main_pc_01621c',4)
    emitter.ins('move.w','#0xc386,%d2',4)
    emitter.ins('move.w','%d2,(%a0)+',2)
    emitter.ins('addq.w','#0x1,%d0',2)
    emitter.ins('dbra','%d1,main_pc_016202',4)
    emitter.ins('clr.w','(%a0)',2)
    emitter.ins('addi.w','#0xa,0xf31a:w',6)
    emitter.ins('rts','',2)

def _lower_append_selected_long_value(emitter,rules):
    emitter.segment(0x1622e,0x1626c)
    emitter.ins('lea.l','0xd100:w,%a0',4)
    emitter.ins('adda.w','0xf31a:w,%a0',4)
    emitter.ins('move.w','#0x6,(%a0)+',4)
    emitter.ins('move.w','#0xc6ac,(%a0)+',4)
    emitter.ins('move.l','0xf3ba:w,%d0',4)
    emitter.ins('move.w','#0xc386,%d1',4)
    emitter.ins('move.w','#0xc001,%d2',4)
    emitter.ins('lea.l','0xd300:w,%a6',4)
    emitter.ins('jsr','main_pc_01270a:l',6)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x2,%d0',4)
    emitter.ins('move.l','(%a1)+,(%a0)+',2)
    emitter.ins('dbra','%d0,main_pc_01625c',4)
    emitter.ins('clr.w','(%a0)',2)
    emitter.ins('addi.w','#0x10,0xf31a:w',6)
    emitter.ins('rts','',2)

def _lower_append_four_row_status_panel(emitter,rules):
    emitter.segment(0x1626c,0x162fc)
    emitter.ins('jsr','main_pc_005abc:l',6)
    emitter.ins('lea.l','0xd100:w,%a0',4)
    emitter.ins('adda.w','0xf31a:w,%a0',4)
    emitter.ins('move.w','#0xa,0x48(%a0)',6)
    emitter.ins('move.w','#0xa,0x30(%a0)',6)
    emitter.ins('move.w','#0xa,0x18(%a0)',6)
    emitter.ins('move.w','#0xa,(%a0)+',4)
    emitter.ins('move.w','#0xc21c,0x48(%a0)',6)
    emitter.ins('move.w','#0xc19c,0x30(%a0)',6)
    emitter.ins('move.w','#0xc11c,0x18(%a0)',6)
    emitter.ins('move.w','#0xc09c,(%a0)+',4)
    emitter.ins('move.w','#0xd380,0x48(%a0)',6)
    emitter.ins('move.w','#0xc382,0x30(%a0)',6)
    emitter.ins('move.w','#0xc382,0x18(%a0)',6)
    emitter.ins('move.w','#0xc380,(%a0)+',4)
    emitter.ins('move.w','#0x5,%d0',4)
    emitter.ins('move.w','#0xc00d,%d1',4)
    emitter.ins('bsr.w','main_pc_0162fc',4)
    emitter.ins('move.w','#0x1,%d0',4)
    emitter.ins('move.w','#0xc049,%d1',4)
    emitter.ins('bsr.w','main_pc_0162fc',4)
    emitter.ins('move.w','#0xdb80,0x48(%a0)',6)
    emitter.ins('move.w','#0xcb82,0x30(%a0)',6)
    emitter.ins('move.w','#0xcb82,0x18(%a0)',6)
    emitter.ins('move.w','#0xcb80,(%a0)+',4)
    emitter.ins('clr.w','0x48(%a0)',4)
    emitter.ins('ori.w','#0x9800,0xf3a4:w',6)
    emitter.ins('addi.w','#0x60,0xf31a:w',6)
    emitter.ins('rts','',2)

def _lower_append_four_row_tile_columns(emitter,rules):
    emitter.segment(0x162fc,0x1631a)
    emitter.ins('move.w','#0xc381,(%a0)',4)
    emitter.ins('move.w','%d1,0x18(%a0)',4)
    emitter.ins('addq.w','#0x1,%d1',2)
    emitter.ins('move.w','%d1,0x30(%a0)',4)
    emitter.ins('addq.w','#0x1,%d1',2)
    emitter.ins('move.w','#0xd381,0x48(%a0)',6)
    emitter.ins('addq.w','#0x2,%a0',2)
    emitter.ins('dbra','%d0,main_pc_0162fc',4)
    emitter.ins('rts','',2)

def _lower_sort_map_packet_queue(emitter,rules):
    emitter.segment(0x1631a,0x1636c)
    emitter.ins('bsr.w','main_pc_01636c',4)
    emitter.ins('lea.l','0xff3000:l,%a0',6)
    emitter.ins('clr.w','0xff39b2:l',6)
    emitter.ins('tst.b','(%a0)+',2)
    emitter.ins('bmi.b','main_pc_016364',2)
    emitter.ins('move.b','(%a0)+,%d0',2)
    emitter.ins('move.b','(%a0)+,%d1',2)
    emitter.ins('lea.l','0xff39b2:l,%a1',6)
    emitter.ins('cmp.b','(%a1),%d1',2)
    emitter.ins('bhi.b','main_pc_016340',2)
    emitter.ins('addq.w','#0x2,%a1',2)
    emitter.ins('bra.b','main_pc_016338',2)
    emitter.ins('lea.l','(%a1),%a2',2)
    emitter.ins('addq.w','#0x2,%a2',2)
    emitter.ins('tst.b','(%a2)',2)
    emitter.ins('bne.b','main_pc_016342',2)
    emitter.ins('clr.b','0x2(%a2)',4)
    emitter.ins('lea.l','0x2(%a2),%a3',4)
    emitter.ins('move.b','-(%a2),-(%a3)',2)
    emitter.ins('move.b','-(%a2),-(%a3)',2)
    emitter.ins('cmpa.l','%a2,%a1',2)
    emitter.ins('bcs.b','main_pc_016350',2)
    emitter.ins('move.b','%d1,(%a1)',2)
    emitter.ins('move.b','%d0,0x1(%a1)',4)
    emitter.ins('tst.b','(%a0)+',2)
    emitter.ins('bne.b','main_pc_01635e',2)
    emitter.ins('bra.b','main_pc_01632a',2)
    emitter.ins('clr.w','0xff3bb2:l',6)
    emitter.ins('rts','',2)

def _lower_append_missing_city_queue_packets(emitter,rules):
    emitter.segment(0x1636c,0x163e0)
    emitter.ins('lea.l','0xff3000:l,%a0',6)
    emitter.ins('adda.w','0xff3826:l,%a0',6)
    emitter.ins('lea.l','0xea38:w,%a1',4)
    emitter.ins('lea.l','0xe640:w,%a3',4)
    emitter.ins('move.w','#0x27,%d0',4)
    emitter.ins('tst.b','(%a1, %d0.w)',4)
    emitter.ins('beq.w','main_pc_0163da',4)
    emitter.ins('lea.l','0xff3000:l,%a2',6)
    emitter.ins('move.w','%d0,%d2',2)
    emitter.ins('addq.w','#0x1,%d2',2)
    emitter.ins('move.b','(%a2)+,%d1',2)
    emitter.ins('bmi.w','main_pc_0163ba',4)
    emitter.ins('move.b','(%a2)+,%d1',2)
    emitter.ins('move.b','(%a2)+,%d1',2)
    emitter.ins('move.b','(%a2)+,%d1',2)
    emitter.ins('cmpi.b','#0x80,%d1',4)
    emitter.ins('bne.w','main_pc_0163b4',4)
    emitter.ins('cmp.b','(%a2)+,%d2',2)
    emitter.ins('bne.w','main_pc_0163b4',4)
    emitter.ins('bra.w','main_pc_0163da',4)
    emitter.ins('tst.b','(%a2)+',2)
    emitter.ins('bne.b','main_pc_0163b4',2)
    emitter.ins('bra.b','main_pc_016396',2)
    emitter.ins('clr.b','(%a0)+',2)
    emitter.ins('move.w','%d0,%d1',2)
    emitter.ins('lsl.w','#0x1,%d1',2)
    emitter.ins('move.b','0x1(%a3, %d1.w),(%a0)+',4)
    emitter.ins('move.b','#0x1,(%a0)+',4)
    emitter.ins('move.b','#0x80,(%a0)+',4)
    emitter.ins('move.b','%d2,(%a0)+',2)
    emitter.ins('clr.b','(%a0)+',2)
    emitter.ins('move.b','#0xff,(%a0)',4)
    emitter.ins('addq.w','#0x6,0xff3826:l',6)
    emitter.ins('dbra','%d0,main_pc_016384',4)
    emitter.ins('rts','',2)

def _lower_upload_selected_queue_officer_name(emitter,rules):
    emitter.segment(0x165d8,0x1665e)
    emitter.ins('move.w','#0x1,%d0',4)
    emitter.ins('move.w','#0x3,%d1',4)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('movea.l','0xff382c:l,%a0',6)
    emitter.ins('clr.w','%d4',2)
    emitter.ins('move.b','0x4(%a0),%d4',4)
    emitter.ins('lsl.w','#0x1,%d4',2)
    emitter.ins('lea.l','0xe640:w,%a0',4)
    emitter.ins('move.w','(%a0, %d4.w),%d4',4)
    emitter.ins('move.w','%d4,%d5',2)
    emitter.ins('lsl.w','#0x1,%d4',2)
    emitter.ins('add.w','%d5,%d4',2)
    emitter.ins('lsl.w','#0x1,%d4',2)
    emitter.ins('lea.l','0x8a504:l,%a0',6)
    emitter.ins('adda.w','%d4,%a0',2)
    emitter.ins('move.w','#0x2,%d3',4)
    emitter.ins('jsr','main_pc_00ae8a:l',6)
    emitter.ins('move.l','#0x41a00000,0xc00004:l',10)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x5f,%d3',4)
    emitter.ins('move.l','(%a1)+,0xc00000:l',6)
    emitter.ins('dbra','%d3,main_pc_016626',4)
    emitter.ins('lea.l','44(%pc),%a0',4)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('clr.w','%d3',2)
    emitter.ins('jsr','main_pc_00ae8a:l',6)
    emitter.ins('move.l','#0x49200000,0xc00004:l',10)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x1f,%d3',4)
    emitter.ins('move.l','(%a1)+,0xc00000:l',6)
    emitter.ins('dbra','%d3,main_pc_016652',4)
    emitter.ins('rts','',2)

def _lower_dispatch_queue_command_state(emitter,rules):
    emitter.segment(0x16660,0x16670)
    emitter.ins('move.w','0xf362:w,%d0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','8(%pc, %d0.w),%d0',4)
    emitter.ins('jsr','12(%pc, %d0.w)',4)
    emitter.ins('rts','',2)

def _lower_render_city_map_entries(emitter,rules):
    emitter.segment(0x169aa,0x16a04)
    emitter.ins('lea.l','0xce9c:w,%a2',4)
    emitter.ins('move.w','#0x27,%d3',4)
    emitter.ins('tst.b','(%a2)',2)
    emitter.ins('beq.b','main_pc_0169fc',2)
    emitter.ins('btst.b','#0x4,(%a2)',4)
    emitter.ins('bne.b','main_pc_0169fc',2)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.b','0x1(%a2),%d0',4)
    emitter.ins('lsl.w','#0x4,%d0',2)
    emitter.ins('move.w','%d0,%d2',2)
    emitter.ins('addi.w','#0x10,%d2',4)
    emitter.ins('sub.w','0xf314:w,%d2',4)
    emitter.ins('bcs.w','main_pc_0169fc',4)
    emitter.ins('cmpi.w','#0xf0,%d2',4)
    emitter.ins('bhi.w','main_pc_0169fc',4)
    emitter.ins('clr.w','%d1',2)
    emitter.ins('move.b','0x2(%a2),%d1',4)
    emitter.ins('lsl.w','#0x4,%d1',2)
    emitter.ins('move.w','%d1,%d2',2)
    emitter.ins('addi.w','#0x10,%d2',4)
    emitter.ins('sub.w','0xf318:w,%d2',4)
    emitter.ins('bcs.w','main_pc_0169fc',4)
    emitter.ins('cmpi.w','#0x150,%d2',4)
    emitter.ins('bhi.w','main_pc_0169fc',4)
    emitter.ins('bsr.w','main_pc_016a04',4)
    emitter.ins('subq.w','#0x4,%a2',2)
    emitter.ins('dbra','%d3,main_pc_0169b2',4)
    emitter.ins('rts','',2)

def _lower_render_city_map_entry(emitter,rules):
    emitter.segment(0x16a04,0x16a78)
    emitter.ins('move.l','%d3,-(%a7)',2)
    emitter.ins('cmpi.w','#0x20a,0xf612:w',6)
    emitter.ins('bne.b','main_pc_016a24',2)
    emitter.ins('cmpi.w','#0x2,0xf362:w',6)
    emitter.ins('bne.b','main_pc_016a24',2)
    emitter.ins('cmp.w','0xcea0:w,%d3',4)
    emitter.ins('bne.b','main_pc_016a24',2)
    emitter.ins('move.w','0xcea4:w,%d0',4)
    emitter.ins('move.w','0xcea6:w,%d1',4)
    emitter.ins('lea.l','82(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('btst.b','#0x4,0xf321:w',6)
    emitter.ins('bne.w','main_pc_016a38',4)
    emitter.ins('adda.w','#0x8,%a0',4)
    emitter.ins('movem.l','%d0-%d1/%a0/%a2,-(%a7)',4)
    emitter.ins('addq.w','#0x8,%d0',2)
    emitter.ins('addq.w','#0x8,%d1',2)
    emitter.ins('bsr.w','main_pc_014294',4)
    emitter.ins('movem.l','(%a7)+,%d0-%d1/%a0/%a2',4)
    emitter.ins('cmpi.w','#0x4,%d2',4)
    emitter.ins('bne.w','main_pc_016a54',4)
    emitter.ins('adda.w','#0x10,%a0',4)
    emitter.ins('addq.w','#0x8,%d1',2)
    emitter.ins('clr.w','%d2',2)
    emitter.ins('tst.b','(%a2)',2)
    emitter.ins('bpl.w','main_pc_016a62',4)
    emitter.ins('move.w','#0x800,%d2',4)
    emitter.ins('move.w','0xf314:w,0xf60a:w',6)
    emitter.ins('move.w','0xf318:w,0xf60e:w',6)
    emitter.ins('jsr','main_pc_00ac10:l',6)
    emitter.ins('move.l','(%a7)+,%d3',2)
    emitter.ins('rts','',2)

def _lower_upload_first_battle_prompt(emitter,rules):
    emitter.segment(0x17a16,0x17a5a)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('lea.l','0x6c0ae:l,%a0',6)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x1,%d0',4)
    emitter.ins('move.w','#0x3,%d1',4)
    emitter.ins('move.w','#0xb,%d3',4)
    emitter.ins('jsr','main_pc_00ae8a:l',6)
    emitter.ins('move.l','#0x40a00002,0xc00004:l',10)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x17f,%d3',4)
    emitter.ins('move.l','(%a1)+,0xc00000:l',6)
    emitter.ins('dbra','%d3,main_pc_017a48',4)
    emitter.ins('jsr','main_pc_00af48:l',6)
    emitter.ins('rts','',2)

def _lower_upload_second_battle_prompt(emitter,rules):
    emitter.segment(0x17a5a,0x17a9e)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('lea.l','0x6c0c6:l,%a0',6)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x1,%d0',4)
    emitter.ins('move.w','#0x3,%d1',4)
    emitter.ins('move.w','#0xb,%d3',4)
    emitter.ins('jsr','main_pc_00ae8a:l',6)
    emitter.ins('move.l','#0x40a00002,0xc00004:l',10)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x17f,%d3',4)
    emitter.ins('move.l','(%a1)+,0xc00000:l',6)
    emitter.ins('dbra','%d3,main_pc_017a8c',4)
    emitter.ins('jsr','main_pc_00af48:l',6)
    emitter.ins('rts','',2)

def _lower_build_nearby_battle_targets(emitter,rules):
    emitter.segment(0x17a9e,0x17b44)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('clr.w','0xaf80:w',4)
    emitter.ins('move.w','0xf3a6:w,%d0',4)
    emitter.ins('lea.l','0xc400:w,%a0',4)
    emitter.ins('clr.w','%d3',2)
    emitter.ins('move.b','(%a0, %d0.w),%d3',4)
    emitter.ins('move.w','%d3,%d5',2)
    emitter.ins('lsl.w','#0x3,%d3',2)
    emitter.ins('add.w','%d5,%d3',2)
    emitter.ins('lsl.w','#0x2,%d0',2)
    emitter.ins('lea.l','0xa150:w,%a3',4)
    emitter.ins('move.w','(%a3, %d0.w),%d5',4)
    emitter.ins('lsr.w','#0x7,%d5',2)
    emitter.ins('move.w','0x2(%a3, %d0.w),%d6',4)
    emitter.ins('lsr.w','#0x7,%d6',2)
    emitter.ins('lea.l','0x945e8:l,%a0',6)
    emitter.ins('move.w','0xf68a:w,%d4',4)
    emitter.ins('mulu.w','#0x8c0,%d4',4)
    emitter.ins('adda.l','%d4,%a0',2)
    emitter.ins('lea.l','0xa62c:w,%a4',4)
    emitter.ins('cmpi.w','#0x1,0xf6d4:w',6)
    emitter.ins('bne.w','main_pc_017b16',4)
    emitter.ins('move.w','%d5,%d1',2)
    emitter.ins('move.w','%d6,%d2',2)
    emitter.ins('jsr','main_pc_01a44e:l',6)
    emitter.ins('cmpi.b','#0x0,%d0',4)
    emitter.ins('beq.w','main_pc_017b16',4)
    emitter.ins('cmpi.b','#0x4,%d0',4)
    emitter.ins('beq.w','main_pc_017b16',4)
    emitter.ins('cmpi.b','#0x7,%d0',4)
    emitter.ins('beq.w','main_pc_017b16',4)
    emitter.ins('move.w','#0x137,0xaf80:w',6)
    emitter.ins('bra.w','main_pc_017b38',4)
    emitter.ins('btst.b','#0x1,0xf6d7:w',6)
    emitter.ins('bne.w','main_pc_017b28',4)
    emitter.ins('lea.l','0xa5a4:w,%a1',4)
    emitter.ins('bra.w','main_pc_017b2c',4)
    emitter.ins('lea.l','0xa550:w,%a1',4)
    emitter.ins('lea.l','0xff3bc2:l,%a5',6)
    emitter.ins('jsr','16(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','#0xffff,(%a4)',4)
    emitter.ins('jsr','main_pc_00af48:l',6)
    emitter.ins('rts','',2)

def _lower_append_nearby_target_candidates(emitter,rules):
    emitter.segment(0x17b44,0x17b9a)
    emitter.ins('move.w','(%a1)+,%d4',2)
    emitter.ins('bmi.w','main_pc_017b98',4)
    emitter.ins('tst.b','(%a5, %d4.w)',4)
    emitter.ins('bne.b','main_pc_017b44',2)
    emitter.ins('andi.w','#0xff,%d4',4)
    emitter.ins('lsl.w','#0x2,%d4',2)
    emitter.ins('move.w','(%a3, %d4.w),%d1',4)
    emitter.ins('lsr.w','#0x7,%d1',2)
    emitter.ins('move.w','0x2(%a3, %d4.w),%d2',4)
    emitter.ins('lsr.w','#0x7,%d2',2)
    emitter.ins('lsr.w','#0x2,%d4',2)
    emitter.ins('bsr.w','main_pc_017b9a',4)
    emitter.ins('bcs.b','main_pc_017b44',2)
    emitter.ins('sub.w','%d5,%d1',2)
    emitter.ins('bcc.w','main_pc_017b72',4)
    emitter.ins('neg.w','%d1',2)
    emitter.ins('cmp.w','%d3,%d1',2)
    emitter.ins('bhi.b','main_pc_017b44',2)
    emitter.ins('mulu.w','%d1,%d1',2)
    emitter.ins('sub.w','%d6,%d2',2)
    emitter.ins('bcc.w','main_pc_017b80',4)
    emitter.ins('neg.w','%d2',2)
    emitter.ins('cmp.w','%d3,%d2',2)
    emitter.ins('bhi.b','main_pc_017b44',2)
    emitter.ins('mulu.w','%d2,%d2',2)
    emitter.ins('add.l','%d2,%d1',2)
    emitter.ins('move.l','%d1,%d0',2)
    emitter.ins('jsr','main_pc_03080e:l',6)
    emitter.ins('cmp.w','%d3,%d0',2)
    emitter.ins('bhi.b','main_pc_017b44',2)
    emitter.ins('move.w','%d4,(%a4)+',2)
    emitter.ins('bra.b','main_pc_017b44',2)
    emitter.ins('rts','',2)

def _lower_dispatch_target_eligibility(emitter,rules):
    emitter.segment(0x17b9a,0x17bb2)
    emitter.ins('movem.l','%d5-%d6,-(%a7)',4)
    emitter.ins('move.w','0xf6d4:w,%d7',4)
    emitter.ins('lsl.w','#0x1,%d7',2)
    emitter.ins('move.w','12(%pc, %d7.w),%d7',4)
    emitter.ins('jsr','70(%pc, %d7.w)',4)
    emitter.ins('movem.l','(%a7)+,%d5-%d6',4)
    emitter.ins('rts','',2)

def _lower_upload_battle_action_prompt(emitter,rules):
    emitter.segment(0x17ede,0x17f18)
    emitter.ins('lea.l','0x6c0de:l,%a0',6)
    emitter.ins('move.w','#0x1,%d0',4)
    emitter.ins('move.w','#0x3,%d1',4)
    emitter.ins('move.w','#0x4,%d3',4)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('jsr','main_pc_00ae8a:l',6)
    emitter.ins('move.l','#0x40a00002,0xc00004:l',10)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x9f,%d3',4)
    emitter.ins('move.l','(%a1)+,0xc00000:l',6)
    emitter.ins('dbra','%d3,main_pc_017f0c',4)
    emitter.ins('rts','',2)

def _lower_upload_battle_result_prompt(emitter,rules):
    emitter.segment(0x1874a,0x18792)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x1f,%d0',4)
    emitter.ins('move.l','#0x11111111,(%a1)+',6)
    emitter.ins('dbra','%d0,main_pc_018752',4)
    emitter.ins('move.w','#0x1,%d0',4)
    emitter.ins('move.w','#0x3,%d1',4)
    emitter.ins('move.w','#0x5,%d3',4)
    emitter.ins('lea.l','0x6c168:l,%a0',6)
    emitter.ins('jsr','main_pc_00ae8a:l',6)
    emitter.ins('move.l','#0x40200002,0xc00004:l',10)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0xdf,%d3',4)
    emitter.ins('move.l','(%a1)+,0xc00000:l',6)
    emitter.ins('dbra','%d3,main_pc_018786',4)
    emitter.ins('rts','',2)

def _lower_upload_selected_officer_names(emitter,rules):
    emitter.segment(0x18792,0x18844)
    emitter.ins('lea.l','0xaf56:w,%a6',4)
    emitter.ins('move.w','0xf658:w,%d0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('adda.w','%d0,%a6',2)
    emitter.ins('move.w','#0x1,%d0',4)
    emitter.ins('move.l','#0x40a00002,0xc00004:l',10)
    emitter.ins('move.w','#0x4,%d7',4)
    emitter.ins('move.w','(%a6)+,%d2',2)
    emitter.ins('bmi.b','main_pc_0187fe',2)
    emitter.ins('move.w','#0x3,%d1',4)
    emitter.ins('btst.l','#0xe,%d2',4)
    emitter.ins('beq.b','main_pc_0187c2',2)
    emitter.ins('move.w','#0x2,%d1',4)
    emitter.ins('andi.w','#0xff,%d2',4)
    emitter.ins('move.w','%d2,%d3',2)
    emitter.ins('lsl.w','#0x1,%d2',2)
    emitter.ins('add.w','%d3,%d2',2)
    emitter.ins('lsl.w','#0x1,%d2',2)
    emitter.ins('lea.l','0x8a504:l,%a0',6)
    emitter.ins('adda.w','%d2,%a0',2)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x2,%d3',4)
    emitter.ins('jsr','main_pc_00ae8a:l',6)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x5f,%d3',4)
    emitter.ins('move.l','(%a1)+,0xc00000:l',6)
    emitter.ins('dbra','%d3,main_pc_0187ec',4)
    emitter.ins('dbra','%d7,main_pc_0187b0',4)
    emitter.ins('bra.w','main_pc_018842',4)
    emitter.ins('move.w','#0x3,%d1',4)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0xf,%d3',4)
    emitter.ins('move.l','#0x11111111,(%a1)+',6)
    emitter.ins('dbra','%d3,main_pc_01880a',4)
    emitter.ins('lea.l','46(%pc),%a0',4)
    emitter.ins('move.w','#0x1,%d3',4)
    emitter.ins('jsr','main_pc_00ae8a:l',6)
    emitter.ins('move.w','#0xf,%d3',4)
    emitter.ins('move.l','#0x11111111,(%a1)+',6)
    emitter.ins('dbra','%d3,main_pc_018826',4)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('move.w','#0x5f,%d3',4)
    emitter.ins('move.l','(%a1)+,0xc00000:l',6)
    emitter.ins('dbra','%d3,main_pc_018838',4)
    emitter.ins('rts','',2)

def _lower_select_active_battle_controller(emitter,rules):
    emitter.segment(0x1a16e,0x1a1dc)
    emitter.ins('cmpi.w','#0x407,0xf612:w',6)
    emitter.ins('bne.w','main_pc_01a194',4)
    emitter.ins('tst.w','0xf362:w',4)
    emitter.ins('beq.w','main_pc_01a1da',4)
    emitter.ins('cmpi.w','#0x2,0xf362:w',6)
    emitter.ins('beq.w','main_pc_01a1da',4)
    emitter.ins('cmpi.w','#0x4,0xf362:w',6)
    emitter.ins('beq.w','main_pc_01a1da',4)
    emitter.ins('move.w','0xf68c:w,%d0',4)
    emitter.ins('move.w','0xf68e:w,%d1',4)
    emitter.ins('btst.b','#0x1,0xf6d7:w',6)
    emitter.ins('beq.w','main_pc_01a1a8',4)
    emitter.ins('exg','%d0,%d1',2)
    emitter.ins('cmp.w','0xf67a:w,%d0',4)
    emitter.ins('beq.w','main_pc_01a1da',4)
    emitter.ins('cmp.w','0xf67c:w,%d0',4)
    emitter.ins('beq.w','main_pc_01a1d4',4)
    emitter.ins('cmp.w','0xf67e:w,%d0',4)
    emitter.ins('beq.w','main_pc_01a1cc',4)
    emitter.ins('cmp.w','0xf67a:w,%d1',4)
    emitter.ins('beq.w','main_pc_01a1da',4)
    emitter.ins('bra.w','main_pc_01a1d4',4)
    emitter.ins('cmp.w','0xf67c:w,%d1',4)
    emitter.ins('beq.w','main_pc_01a1da',4)
    emitter.ins('move.w','0xf604:w,0xf602:w',6)
    emitter.ins('rts','',2)

def _lower_update_direction_choice(emitter,rules):
    emitter.segment(0x1cf58,0x1cf84)
    emitter.ins('bsr.w','main_pc_01cf84',4)
    emitter.ins('bsr.w','main_pc_01cfc6',4)
    emitter.ins('btst.b','#0x5,0xf603:w',6)
    emitter.ins('beq.w','main_pc_01cf82',4)
    emitter.ins('jsr','main_pc_00c0b6:l',6)
    emitter.ins('move.w','#0x208,0xf612:w',6)
    emitter.ins('move.w','#0x3,0xf362:w',6)
    emitter.ins('move.w','#0x12,0xf36a:w',6)
    emitter.ins('rts','',2)

def _lower_cycle_available_direction(emitter,rules):
    emitter.segment(0x1cf84,0x1cfc6)
    emitter.ins('lea.l','0xefbe:w,%a1',4)
    emitter.ins('move.w','0xefc6:w,%d1',4)
    emitter.ins('move.b','0xf603:w,%d0',4)
    emitter.ins('andi.w','#0xc,%d0',4)
    emitter.ins('beq.w','main_pc_01cfc4',4)
    emitter.ins('btst.l','#0x2,%d0',4)
    emitter.ins('bne.w','main_pc_01cfb4',4)
    emitter.ins('subq.w','#0x2,%d1',2)
    emitter.ins('andi.w','#0x7,%d1',4)
    emitter.ins('tst.w','(%a1, %d1.w)',4)
    emitter.ins('bmi.b','main_pc_01cfa0',2)
    emitter.ins('move.w','%d1,0xefc6:w',4)
    emitter.ins('bra.w','main_pc_01cfc4',4)
    emitter.ins('addq.w','#0x2,%d1',2)
    emitter.ins('andi.w','#0x7,%d1',4)
    emitter.ins('tst.w','(%a1, %d1.w)',4)
    emitter.ins('bmi.b','main_pc_01cfb4',2)
    emitter.ins('move.w','%d1,0xefc6:w',4)
    emitter.ins('rts','',2)

def _lower_render_direction_choice(emitter,rules):
    emitter.segment(0x1cfc6,0x1d012)
    emitter.ins('btst.b','#0x4,0xf321:w',6)
    emitter.ins('bne.w','main_pc_01d010',4)
    emitter.ins('lea.l','80(%pc),%a0',4)
    emitter.ins('lea.l','60(%pc),%a2',4)
    emitter.ins('move.w','0xefc6:w,%d2',4)
    emitter.ins('lsl.w','#0x1,%d2',2)
    emitter.ins('movea.l','0xff382c:l,%a1',6)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.b','0x1(%a1),%d0',4)
    emitter.ins('add.w','(%a2, %d2.w),%d0',4)
    emitter.ins('lsl.w','#0x4,%d0',2)
    emitter.ins('clr.w','%d1',2)
    emitter.ins('move.b','0x2(%a1),%d1',4)
    emitter.ins('add.w','0x2(%a2, %d2.w),%d1',4)
    emitter.ins('lsl.w','#0x4,%d1',2)
    emitter.ins('clr.w','%d2',2)
    emitter.ins('move.w','0xf314:w,0xf60a:w',6)
    emitter.ins('move.w','0xf318:w,0xf60e:w',6)
    emitter.ins('jsr','main_pc_00ac28:l',6)
    emitter.ins('rts','',2)

def _lower_process_both_battle_force_turns(emitter,rules):
    emitter.segment(0x221e4,0x2224c)
    emitter.ins('bsr.w','main_pc_02224c',4)
    emitter.ins('bsr.w','main_pc_0223d6',4)
    emitter.ins('bcs.w','main_pc_02224a',4)
    emitter.ins('move.w','0xf68c:w,%d0',4)
    emitter.ins('cmp.w','0xf67a:w,%d0',4)
    emitter.ins('beq.w','main_pc_022216',4)
    emitter.ins('cmp.w','0xf67c:w,%d0',4)
    emitter.ins('beq.w','main_pc_022216',4)
    emitter.ins('cmp.w','0xf67e:w,%d0',4)
    emitter.ins('beq.w','main_pc_022216',4)
    emitter.ins('clr.w','0xf6d6:w',4)
    emitter.ins('jsr','main_pc_023562:l',6)
    emitter.ins('move.w','0xf68e:w,%d0',4)
    emitter.ins('cmp.w','0xf67a:w,%d0',4)
    emitter.ins('beq.w','main_pc_02223c',4)
    emitter.ins('cmp.w','0xf67c:w,%d0',4)
    emitter.ins('beq.w','main_pc_02223c',4)
    emitter.ins('cmp.w','0xf67e:w,%d0',4)
    emitter.ins('beq.w','main_pc_02223c',4)
    emitter.ins('move.w','#0x2,0xf6d6:w',6)
    emitter.ins('bsr.w','main_pc_022418',4)
    emitter.ins('cmpi.w','#0x411,0xf612:w',6)
    emitter.ins('beq.w','main_pc_02224a',4)
    emitter.ins('clr.w','0xf6d6:w',4)
    emitter.ins('rts','',2)

def _lower_settle_both_force_supply(emitter,rules):
    emitter.segment(0x2224c,0x22278)
    emitter.ins('lea.l','0xc800:w,%a2',4)
    emitter.ins('lea.l','0xb200:w,%a4',4)
    emitter.ins('clr.w','0xf6d6:w',4)
    emitter.ins('lea.l','0xa550:w,%a0',4)
    emitter.ins('lea.l','0xf69e:w,%a1',4)
    emitter.ins('bsr.w','main_pc_022278',4)
    emitter.ins('move.w','#0x2,0xf6d6:w',6)
    emitter.ins('lea.l','0xa5a4:w,%a0',4)
    emitter.ins('lea.l','0xf6a2:w,%a1',4)
    emitter.ins('bsr.w','main_pc_022278',4)
    emitter.ins('rts','',2)

def _lower_deduct_force_supply(emitter,rules):
    emitter.segment(0x22278,0x222a8)
    emitter.ins('movea.l','%a0,%a3',2)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','(%a3)+,%d1',2)
    emitter.ins('bmi.b','main_pc_022292',2)
    emitter.ins('andi.w','#0xff,%d1',4)
    emitter.ins('lsl.w','#0x2,%d1',2)
    emitter.ins('add.l','(%a2, %d1.w),%d0',4)
    emitter.ins('addi.l','#0x64,%d0',6)
    emitter.ins('bra.b','main_pc_02227c',2)
    emitter.ins('divu.w','#0x64,%d0',4)
    emitter.ins('andi.l','#0xffff,%d0',6)
    emitter.ins('sub.l','%d0,(%a1)',2)
    emitter.ins('bcc.b','main_pc_0222a6',2)
    emitter.ins('clr.l','(%a1)',2)
    emitter.ins('bsr.w','main_pc_0222a8',4)
    emitter.ins('rts','',2)

def _lower_apply_force_supply_losses(emitter,rules):
    emitter.segment(0x222a8,0x223d6)
    emitter.ins('jsr','main_pc_0083d4:l',6)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','0xf61c:w,%d0',4)
    emitter.ins('move.l','%d0,%d1',2)
    emitter.ins('move.l','%d0,%d2',2)
    emitter.ins('lsl.l','#0x1,%d0',2)
    emitter.ins('add.l','%d1,%d0',2)
    emitter.ins('swap','%d0',2)
    emitter.ins('addi.w','#0x3,%d0',4)
    emitter.ins('move.l','%d2,%d1',2)
    emitter.ins('lsl.l','#0x2,%d1',2)
    emitter.ins('add.l','%d2,%d1',2)
    emitter.ins('lsl.l','#0x1,%d1',2)
    emitter.ins('add.l','%d2,%d1',2)
    emitter.ins('swap','%d1',2)
    emitter.ins('addi.w','#0x14,%d1',4)
    emitter.ins('move.w','(%a0)+,%d2',2)
    emitter.ins('bmi.w','main_pc_0223d4',4)
    emitter.ins('andi.w','#0xff,%d2',4)
    emitter.ins('lsl.w','#0x1,%d2',2)
    emitter.ins('sub.w','%d0,(%a4, %d2.w)',4)
    emitter.ins('bhi.b','main_pc_02234c',2)
    emitter.ins('lsr.w','#0x1,%d2',2)
    emitter.ins('lea.l','0xcc00:w,%a5',4)
    emitter.ins('move.b','(%a5, %d2.w),%d3',4)
    emitter.ins('move.b','#0xff,(%a5, %d2.w)',6)
    emitter.ins('movea.l','%a0,%a5',2)
    emitter.ins('move.w','(%a5)+,-0x4(%a5)',4)
    emitter.ins('bpl.b','main_pc_0222f6',2)
    emitter.ins('subq.w','#0x2,%a0',2)
    emitter.ins('andi.w','#0x3f,%d3',4)
    emitter.ins('lea.l','0xf427:w,%a5',4)
    emitter.ins('move.b','(%a5, %d3.w),%d3',4)
    emitter.ins('andi.w','#0xf,%d3',4)
    emitter.ins('cmp.w','0xf67a:w,%d3',4)
    emitter.ins('beq.w','main_pc_022326',4)
    emitter.ins('cmp.w','0xf67c:w,%d3',4)
    emitter.ins('beq.w','main_pc_022326',4)
    emitter.ins('cmp.w','0xf67e:w,%d3',4)
    emitter.ins('bne.w','main_pc_022366',4)
    emitter.ins('move.w','0xf376:w,-(%a7)',4)
    emitter.ins('movem.l','%d0-%d1/%a0/%a2/%a4,-(%a7)',4)
    emitter.ins('move.w','%d3,0xf376:w',4)
    emitter.ins('move.w','%d2,0xf3d0:w',4)
    emitter.ins('move.w','#0xca,0xf740:w',6)
    emitter.ins('jsr','main_pc_0260e4:l',6)
    emitter.ins('movem.l','(%a7)+,%d0-%d1/%a0/%a2/%a4',4)
    emitter.ins('move.w','(%a7)+,0xf376:w',4)
    emitter.ins('bra.b','main_pc_0222d2',2)
    emitter.ins('lsl.w','#0x1,%d2',2)
    emitter.ins('move.l','(%a2, %d2.w),%d3',4)
    emitter.ins('mulu.w','%d1,%d3',2)
    emitter.ins('divu.w','#0x64,%d3',4)
    emitter.ins('andi.l','#0xffff,%d3',6)
    emitter.ins('sub.l','%d3,(%a2, %d2.w)',4)
    emitter.ins('bra.w','main_pc_0222d2',4)
    emitter.ins('lea.l','0xf45e:w,%a1',4)
    emitter.ins('move.w','0xf68a:w,%d3',4)
    emitter.ins('lsl.w','#0x1,%d3',2)
    emitter.ins('cmp.w','(%a1, %d3.w),%d2',4)
    emitter.ins('beq.w','main_pc_0223ae',4)
    emitter.ins('lea.l','0xa027:w,%a1',4)
    emitter.ins('move.w','0xf68a:w,%d3',4)
    emitter.ins('cmp.b','(%a1, %d3.w),%d2',4)
    emitter.ins('bne.w','main_pc_0222d2',4)
    emitter.ins('move.w','0xf376:w,-(%a7)',4)
    emitter.ins('movem.l','%d0-%d1/%a0/%a2/%a4,-(%a7)',4)
    emitter.ins('move.w','0xf68e:w,0xf376:w',6)
    emitter.ins('move.w','#0x142,0xf740:w',6)
    emitter.ins('jsr','main_pc_0260e4:l',6)
    emitter.ins('movem.l','(%a7)+,%d0-%d1/%a0/%a2/%a4',4)
    emitter.ins('move.w','(%a7)+,0xf376:w',4)
    emitter.ins('bra.w','main_pc_0222d2',4)
    emitter.ins('move.w','0xf376:w,-(%a7)',4)
    emitter.ins('movem.l','%d0-%d1/%a0/%a2/%a4,-(%a7)',4)
    emitter.ins('move.w','0xf68c:w,0xf376:w',6)
    emitter.ins('move.w','#0x143,0xf740:w',6)
    emitter.ins('jsr','main_pc_0260e4:l',6)
    emitter.ins('movem.l','(%a7)+,%d0-%d1/%a0/%a2/%a4',4)
    emitter.ins('move.w','(%a7)+,0xf376:w',4)
    emitter.ins('bra.w','main_pc_0222d2',4)
    emitter.ins('rts','',2)

def _lower_check_battle_commanders_present(emitter,rules):
    emitter.segment(0x223d6,0x22418)
    emitter.ins('lea.l','0xcc00:w,%a1',4)
    emitter.ins('lea.l','0xa027:w,%a0',4)
    emitter.ins('move.w','0xf68a:w,%d0',4)
    emitter.ins('clr.w','%d1',2)
    emitter.ins('move.b','(%a0, %d0.w),%d1',4)
    emitter.ins('cmpi.b','#0xff,(%a1, %d1.w)',6)
    emitter.ins('beq.w','main_pc_022412',4)
    emitter.ins('move.w','0xf68a:w,%d0',4)
    emitter.ins('lea.l','0xf45e:w,%a0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.b','(%a0, %d0.w),%d0',4)
    emitter.ins('cmpi.b','#0xff,(%a1, %d0.w)',6)
    emitter.ins('beq.w','main_pc_022412',4)
    emitter.ins('andi.w','#0xfffe,%sr',4)
    emitter.ins('bra.w','main_pc_022416',4)
    emitter.ins('ori.w','#0x1,%sr',4)
    emitter.ins('rts','',2)

def _lower_execute_secondary_force_orders(emitter,rules):
    emitter.segment(0x22418,0x22456)
    emitter.ins('bsr.w','main_pc_024b00',4)
    emitter.ins('bsr.w','main_pc_022470',4)
    emitter.ins('lea.l','0xa5a4:w,%a0',4)
    emitter.ins('lea.l','0xaf96:w,%a1',4)
    emitter.ins('move.w','(%a0)+,%d7',2)
    emitter.ins('bmi.w','main_pc_022450',4)
    emitter.ins('move.w','(%a1)+,%d0',2)
    emitter.ins('cmpi.w','#0xff,%d0',4)
    emitter.ins('beq.b','main_pc_022428',2)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','28(%pc, %d0.w),%d0',4)
    emitter.ins('movem.l','%a0-%a1,-(%a7)',4)
    emitter.ins('lea.l','156(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','(%a0, %d0.w)',4)
    emitter.ins('movem.l','(%a7)+,%a0-%a1',4)
    emitter.ins('bra.b','main_pc_022428',2)
    emitter.ins('clr.w','0xf362:w',4)
    emitter.ins('rts','',2)

def _lower_calculate_force_supply_budgets(emitter,rules):
    emitter.segment(0x22470,0x224de)
    emitter.ins('lea.l','0xa550:w,%a0',4)
    emitter.ins('lea.l','0xa5a4:w,%a2',4)
    emitter.ins('btst.b','#0x1,0xf6d7:w',6)
    emitter.ins('beq.w','main_pc_022484',4)
    emitter.ins('exg','%a0,%a2',2)
    emitter.ins('lea.l','0xc800:w,%a4',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','(%a0)+,%d1',2)
    emitter.ins('bmi.w','main_pc_02249e',4)
    emitter.ins('lsl.w','#0x2,%d1',2)
    emitter.ins('add.l','(%a4, %d1.w),%d0',4)
    emitter.ins('addi.l','#0x64,%d0',6)
    emitter.ins('bra.b','main_pc_02248a',2)
    emitter.ins('divu.w','#0x32,%d0',4)
    emitter.ins('move.w','%d0,%d1',2)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('add.w','%d1,%d0',2)
    emitter.ins('andi.l','#0xffff,%d0',6)
    emitter.ins('move.l','%d0,0xf768:w',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','(%a2)+,%d1',2)
    emitter.ins('bmi.w','main_pc_0224c8',4)
    emitter.ins('lsl.w','#0x2,%d1',2)
    emitter.ins('add.l','(%a4, %d1.w),%d0',4)
    emitter.ins('addi.l','#0x64,%d0',6)
    emitter.ins('bra.b','main_pc_0224b4',2)
    emitter.ins('divu.w','#0x32,%d0',4)
    emitter.ins('move.w','%d0,%d1',2)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('add.w','%d1,%d0',2)
    emitter.ins('andi.l','#0xffff,%d0',6)
    emitter.ins('move.l','%d0,0xf76c:w',4)
    emitter.ins('rts','',2)

def _lower_execute_primary_force_orders(emitter,rules):
    emitter.segment(0x23562,0x235b6)
    emitter.ins('bsr.w','main_pc_02540e',4)
    emitter.ins('bsr.w','main_pc_022470',4)
    emitter.ins('lea.l','0xa550:w,%a0',4)
    emitter.ins('lea.l','0xaf82:w,%a1',4)
    emitter.ins('bsr.w','main_pc_0235cc',4)
    emitter.ins('bcs.w','main_pc_0235b0',4)
    emitter.ins('cmpi.w','#0x411,0xf612:w',6)
    emitter.ins('beq.w','main_pc_0235b0',4)
    emitter.ins('move.w','(%a0)+,%d7',2)
    emitter.ins('bmi.w','main_pc_0235b0',4)
    emitter.ins('move.w','(%a1)+,%d0',2)
    emitter.ins('cmpi.w','#0xff,%d0',4)
    emitter.ins('beq.b','main_pc_023572',2)
    emitter.ins('move.w','%d0,0xf770:w',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','28(%pc, %d0.w),%d0',4)
    emitter.ins('movem.l','%a0-%a1,-(%a7)',4)
    emitter.ins('lea.l','110(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','(%a0, %d0.w)',4)
    emitter.ins('movem.l','(%a7)+,%a0-%a1',4)
    emitter.ins('bra.b','main_pc_023572',2)
    emitter.ins('clr.w','0xf362:w',4)
    emitter.ins('rts','',2)

def _lower_select_primary_force_order_policy(emitter,rules):
    emitter.segment(0x24ad0,0x24aea)
    emitter.ins('btst.b','#0x1,0xf6d7:w',6)
    emitter.ins('beq.w','main_pc_024ae2',4)
    emitter.ins('bsr.w','main_pc_024af2',4)
    emitter.ins('bra.w','main_pc_024af0',4)
    emitter.ins('bsr.w','main_pc_02536a',4)
    emitter.ins('bra.w','main_pc_024af0',4)
    emitter.segment(0x24af0,0x24af2)
    emitter.ins('rts','',2)

def _lower_initialize_battle_policy_targets(emitter,rules):
    emitter.segment(0x25bd8,0x25be8)
    emitter.ins('jsr','main_pc_01a438:l',6)
    emitter.ins('bsr.w','main_pc_025be8',4)
    emitter.ins('bsr.w','main_pc_025ef0',4)
    emitter.ins('rts','',2)

def _lower_initialize_primary_policy_targets(emitter,rules):
    emitter.segment(0x25be8,0x25c02)
    emitter.ins('bsr.w','main_pc_025c02',4)
    emitter.ins('bsr.w','main_pc_025c2a',4)
    emitter.ins('lea.l','0xa550:w,%a3',4)
    emitter.ins('move.w','#0x2,%d7',4)
    emitter.ins('bsr.w','main_pc_025c6a',4)
    emitter.ins('bsr.w','main_pc_025df8',4)
    emitter.ins('rts','',2)

def _lower_collect_order_target_candidates(emitter,rules):
    emitter.segment(0x25c6a,0x25c9c)
    emitter.ins('lea.l','0xa150:w,%a1',4)
    emitter.ins('bsr.w','main_pc_025c9c',4)
    emitter.ins('bcs.w','main_pc_025c9a',4)
    emitter.ins('bsr.w','main_pc_025cb8',4)
    emitter.ins('bcs.w','main_pc_025c9a',4)
    emitter.ins('bsr.w','main_pc_025d96',4)
    emitter.ins('bcs.w','main_pc_025c9a',4)
    emitter.ins('bsr.w','main_pc_025dea',4)
    emitter.ins('bcs.w','main_pc_025c9a',4)
    emitter.ins('bsr.w','main_pc_025df2',4)
    emitter.ins('bcs.w','main_pc_025c9a',4)
    emitter.ins('addq.w','#0x2,%d7',2)
    emitter.ins('bra.b','main_pc_025c76',2)
    emitter.ins('rts','',2)

def _lower_offset_first_order_target_axis(emitter,rules):
    emitter.segment(0x25dea,0x25df2)
    emitter.ins('move.w','%d7,%d2',2)
    emitter.ins('add.w','%d0,%d2',2)
    emitter.ins('bra.w','main_pc_025cbe',4)

def _lower_offset_second_order_target_axis(emitter,rules):
    emitter.segment(0x25df2,0x25df8)
    emitter.ins('move.w','%d7,%d3',2)
    emitter.ins('add.w','%d1,%d3',2)
    emitter.ins('bra.b','main_pc_025d9c',2)

def _lower_initialize_secondary_policy_targets(emitter,rules):
    emitter.segment(0x25ef0,0x25f0a)
    emitter.ins('bsr.w','main_pc_025f0a',4)
    emitter.ins('bsr.w','main_pc_025c2a',4)
    emitter.ins('lea.l','0xa5a4:w,%a3',4)
    emitter.ins('move.w','#0x4,%d7',4)
    emitter.ins('bsr.w','main_pc_025c6a',4)
    emitter.ins('bsr.w','main_pc_025f28',4)
    emitter.ins('rts','',2)

def _lower_update_first_setup_option(emitter,rules):
    emitter.segment(0x2ad5a,0x2ad88)
    emitter.ins('tst.w','0xff7022:l',6)
    emitter.ins('bne.w','main_pc_02ad86',4)
    emitter.ins('move.w','0xff7026:l,%d5',6)
    emitter.ins('move.w','#0x2,%d6',4)
    emitter.ins('jsr','682(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','%d5,0xff7026:l',6)
    emitter.ins('lea.l','776(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','520(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('rts','',2)

def _lower_update_second_setup_option(emitter,rules):
    emitter.segment(0x2ad88,0x2adb8)
    emitter.ins('cmpi.w','#0x1,0xff7022:l',8)
    emitter.ins('bne.w','main_pc_02adb6',4)
    emitter.ins('move.w','0xff7024:l,%d5',6)
    emitter.ins('move.w','#0x2,%d6',4)
    emitter.ins('jsr','634(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','%d5,0xff7024:l',6)
    emitter.ins('lea.l','778(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','472(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('rts','',2)

def _lower_update_third_setup_option(emitter,rules):
    emitter.segment(0x2adb8,0x2ade8)
    emitter.ins('cmpi.w','#0x2,0xff7022:l',8)
    emitter.ins('bne.w','main_pc_02ade6',4)
    emitter.ins('move.w','0xff7028:l,%d5',6)
    emitter.ins('move.w','#0x1,%d6',4)
    emitter.ins('jsr','586(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','%d5,0xff7028:l',6)
    emitter.ins('lea.l','780(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','424(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('rts','',2)

def _lower_update_fourth_setup_option(emitter,rules):
    emitter.segment(0x2ade8,0x2ae18)
    emitter.ins('cmpi.w','#0x3,0xff7022:l',8)
    emitter.ins('bne.w','main_pc_02ae16',4)
    emitter.ins('move.w','0xff702a:l,%d5',6)
    emitter.ins('move.w','#0x2,%d6',4)
    emitter.ins('jsr','538(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','%d5,0xff702a:l',6)
    emitter.ins('lea.l','632(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','376(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('rts','',2)

def _lower_update_setup_player_choices(emitter,rules):
    emitter.segment(0x2ae18,0x2af8a)
    emitter.ins('cmpi.w','#0x5,0xff7022:l',8)
    emitter.ins('beq.w','main_pc_02aebc',4)
    emitter.ins('cmpi.w','#0x6,0xff7022:l',8)
    emitter.ins('beq.w','main_pc_02aebc',4)
    emitter.ins('cmpi.w','#0x4,0xff7022:l',8)
    emitter.ins('bne.w','main_pc_02af72',4)
    emitter.ins('btst.b','#0x2,0xf603:w',6)
    emitter.ins('beq.w','main_pc_02ae7c',4)
    emitter.ins('tst.w','0xff702c:l',6)
    emitter.ins('beq.w','main_pc_02ae5c',4)
    emitter.ins('subi.w','#0x1,0xff702c:l',8)
    emitter.ins('bra.w','main_pc_02aebc',4)
    emitter.ins('move.w','#0x6,0xff702c:l',8)
    emitter.ins('cmpi.w','#0x2,0xff7026:l',8)
    emitter.ins('bne.w','main_pc_02aebc',4)
    emitter.ins('move.w','#0x2,0xff702c:l',8)
    emitter.ins('bra.w','main_pc_02aebc',4)
    emitter.ins('btst.b','#0x3,0xf603:w',6)
    emitter.ins('beq.w','main_pc_02aebc',4)
    emitter.ins('cmpi.w','#0x2,0xff7026:l',8)
    emitter.ins('bcs.w','main_pc_02aeaa',4)
    emitter.ins('cmpi.w','#0x2,0xff702c:l',8)
    emitter.ins('beq.w','main_pc_02aea2',4)
    emitter.ins('bra.w','main_pc_02aeb4',4)
    emitter.ins('clr.w','0xff702c:l',6)
    emitter.ins('bra.b','main_pc_02aebc',2)
    emitter.ins('cmpi.w','#0x6,0xff702c:l',8)
    emitter.ins('beq.b','main_pc_02aea2',2)
    emitter.ins('addi.w','#0x1,0xff702c:l',8)
    emitter.ins('clr.l','%d2',2)
    emitter.ins('tst.w','0xff7026:l',6)
    emitter.ins('bne.w','main_pc_02aed2',4)
    emitter.ins('lea.l','400(%pc),%a5',4)
    emitter.ins('nop','',2)
    emitter.ins('bra.w','main_pc_02aeee',4)
    emitter.ins('cmpi.w','#0x1,0xff7026:l',8)
    emitter.ins('bne.w','main_pc_02aee8',4)
    emitter.ins('lea.l','394(%pc),%a5',4)
    emitter.ins('nop','',2)
    emitter.ins('bra.w','main_pc_02aeee',4)
    emitter.ins('lea.l','400(%pc),%a5',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','(%a5)+,%d0',2)
    emitter.ins('cmpi.w','#0xffff,%d0',4)
    emitter.ins('beq.w','main_pc_02af12',4)
    emitter.ins('move.w','%d0,%d1',2)
    emitter.ins('asr.w','#0x8,%d0',2)
    emitter.ins('andi.w','#0xff,%d0',4)
    emitter.ins('andi.w','#0xff,%d1',4)
    emitter.ins('lea.l','520(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','main_pc_00ac08:l',6)
    emitter.ins('bra.b','main_pc_02aeee',2)
    emitter.ins('cmpi.w','#0x2,0xff7026:l',8)
    emitter.ins('bcs.w','main_pc_02af74',4)
    emitter.ins('cmpi.w','#0x6,0xff7022:l',8)
    emitter.ins('bne.w','main_pc_02af3c',4)
    emitter.ins('move.w','0xff7030:l,%d5',6)
    emitter.ins('jsr','21996(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','%d5,0xff7030:l',6)
    emitter.ins('cmpi.w','#0x5,0xff7022:l',8)
    emitter.ins('bcc.w','main_pc_02af4e',4)
    emitter.ins('clr.w','0xff702e:l',6)
    emitter.ins('cmpi.w','#0x5,0xff7022:l',8)
    emitter.ins('bne.w','main_pc_02af72',4)
    emitter.ins('move.w','0xff702e:l,%d5',6)
    emitter.ins('jsr','21818(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','%d5,0xff702e:l',6)
    emitter.ins('clr.w','0xff7030:l',6)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0xb0,%d0',4)
    emitter.ins('move.w','#0x100,%d1',4)
    emitter.ins('lea.l','400(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','main_pc_00ac08:l',6)
    emitter.ins('bra.b','main_pc_02af1e',2)

def _lower_render_current_setup_option(emitter,rules):
    emitter.segment(0x2af8a,0x2afb8)
    emitter.ins('move.w','0xff7022:l,%d5',6)
    emitter.ins('cmpi.w','#0x5,%d5',4)
    emitter.ins('beq.b','main_pc_02afb6',2)
    emitter.ins('asl.w','#0x1,%d5',2)
    emitter.ins('lea.l','182(%pc),%a1',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','(%a1, %d5.w),%d1',4)
    emitter.ins('move.w','%d1,%d0',2)
    emitter.ins('asr.w','#0x8,%d0',2)
    emitter.ins('andi.w','#0xff,%d0',4)
    emitter.ins('andi.w','#0xff,%d1',4)
    emitter.ins('clr.l','%d2',2)
    emitter.ins('jsr','main_pc_00ac08:l',6)
    emitter.ins('rts','',2)

def _lower_advance_setup_reveal(emitter,rules):
    emitter.segment(0x2afb8,0x2afe6)
    emitter.ins('cmpi.w','#0x10,0xff7040:l',8)
    emitter.ins('bcc.w','main_pc_02afe4',4)
    emitter.ins('move.w','#0xf,%d0',4)
    emitter.ins('sub.w','0xff7040:l,%d0',6)
    emitter.ins('move.w','#0x40,%d1',4)
    emitter.ins('lea.l','1178(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','main_pc_00dea6:l',6)
    emitter.ins('addq.w','#0x1,0xff7040:l',6)
    emitter.ins('rts','',2)

def _lower_advance_setup_dismissal(emitter,rules):
    emitter.segment(0x2afe6,0x2b01a)
    emitter.ins('tst.w','0xff703e:l',6)
    emitter.ins('beq.w','main_pc_02b018',4)
    emitter.ins('cmpi.w','#0x10,0xff7042:l',8)
    emitter.ins('bcc.w','main_pc_02b018',4)
    emitter.ins('move.w','0xff7042:l,%d0',6)
    emitter.ins('move.w','#0x40,%d1',4)
    emitter.ins('lea.l','1126(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','main_pc_00dea6:l',6)
    emitter.ins('addq.w','#0x1,0xff7042:l',6)
    emitter.ins('rts','',2)

def _lower_cycle_setup_option(emitter,rules):
    emitter.segment(0x2b01a,0x2b050)
    emitter.ins('btst.b','#0x0,0xf603:w',6)
    emitter.ins('beq.w','main_pc_02b032',4)
    emitter.ins('tst.w','%d5',2)
    emitter.ins('beq.w','main_pc_02b048',4)
    emitter.ins('subi.w','#0x1,%d5',4)
    emitter.ins('beq.w','main_pc_02b046',4)
    emitter.ins('btst.b','#0x1,0xf603:w',6)
    emitter.ins('beq.w','main_pc_02b046',4)
    emitter.ins('cmp.w','%d6,%d5',2)
    emitter.ins('beq.w','main_pc_02b04c',4)
    emitter.ins('addi.w','#0x1,%d5',4)
    emitter.ins('rts','',2)
    emitter.ins('move.w','%d6,%d5',2)
    emitter.ins('rts','',2)
    emitter.ins('moveq','#0,%d5',2)
    emitter.ins('rts','',2)

def _lower_initialize_setup_video(emitter,rules):
    emitter.segment(0x2b15e,0x2b2fe)
    emitter.ins('move.w','#0x8238,0xc00004:l',8)
    emitter.ins('move.w','#0x833c,0xc00004:l',8)
    emitter.ins('move.w','#0x8406,0xc00004:l',8)
    emitter.ins('move.w','#0x857e,0xc00004:l',8)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.w','#0x8c81,0xc00004:l',8)
    emitter.ins('move.w','#0x9001,0xc00004:l',8)
    emitter.ins('move.w','#0x9100,0xc00004:l',8)
    emitter.ins('move.w','#0x9200,0xc00004:l',8)
    emitter.ins('move.w','#0x0,0xf312:w',6)
    emitter.ins('move.w','#0x0,0xf314:w',6)
    emitter.ins('move.w','#0x0,0xf316:w',6)
    emitter.ins('move.w','#0x0,0xf318:w',6)
    emitter.ins('move.l','#0x40200000,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a6',6)
    emitter.ins('move.l','#0x11111111,%d2',6)
    emitter.ins('move.w','#0x3f,%d0',4)
    emitter.ins('move.l','%d2,(%a6)',2)
    emitter.ins('dbra','%d0,main_pc_02b1d8',4)
    emitter.ins('move.l','#0x50000000,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a6',6)
    emitter.ins('move.l','#0x22222222,%d2',6)
    emitter.ins('move.w','#0x3f,%d0',4)
    emitter.ins('move.l','%d2,(%a6)',2)
    emitter.ins('dbra','%d0,main_pc_02b1f8',4)
    emitter.ins('move.l','#0x60000001,0xc00004:l',10)
    emitter.ins('lea.l','740(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('move.l','#0x7ff,%d0',6)
    emitter.ins('move.l','(%a0)+,(%a6)',2)
    emitter.ins('dbra','%d0,main_pc_02b214',4)
    emitter.ins('move.l','#0x40000002,0xc00004:l',10)
    emitter.ins('lea.l','8904(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('move.l','#0x7ff,%d0',6)
    emitter.ins('move.l','(%a0)+,(%a6)',2)
    emitter.ins('dbra','%d0,main_pc_02b230',4)
    emitter.ins('tst.w','0xff7036:l',6)
    emitter.ins('bne.w','main_pc_02b270',4)
    emitter.ins('lea.l','17068(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('lea.l','0xe000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('bsr.w','main_pc_02b3c4',4)
    emitter.ins('lea.l','18347(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('lea.l','0xe040:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('bsr.w','main_pc_02b3c4',4)
    emitter.ins('bra.w','main_pc_02b29c',4)
    emitter.ins('lea.l','18716(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('lea.l','0xe000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('bsr.w','main_pc_02b3c4',4)
    emitter.ins('lea.l','19303(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('lea.l','0xe040:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('bsr.w','main_pc_02b3c4',4)
    emitter.ins('lea.l','19580(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('lea.l','0xc000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('move.w','#0x0,0xff7008:l',8)
    emitter.ins('move.w','#0xffff,0xff700c:l',8)
    emitter.ins('bsr.w','main_pc_02b3d4',4)
    emitter.ins('lea.l','19701(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('lea.l','0xc040:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('move.w','#0x0,0xff7008:l',8)
    emitter.ins('move.w','#0xffff,0xff700c:l',8)
    emitter.ins('bsr.w','main_pc_02b3d4',4)
    emitter.ins('lea.l','388(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('lea.l','0xfb00:w,%a1',4)
    emitter.ins('move.w','#0x1f,%d0',4)
    emitter.ins('move.l','(%a0)+,(%a1)+',2)
    emitter.ins('dbra','%d0,main_pc_02b2f6',4)
    emitter.ins('rts','',2)

def _lower_decode_setup_plane_rows(emitter,rules):
    emitter.segment(0x2b3c4,0x2b446)
    emitter.ins('move.w','#0x8000,0xff7008:l',8)
    emitter.ins('move.w','#0xffff,0xff700c:l',8)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.w','%a1,%d0',2)
    emitter.ins('bsr.w','main_pc_02b446',4)
    emitter.ins('moveq','#0,%d4',2)
    emitter.ins('move.b','(%a0)+,%d1',2)
    emitter.ins('move.b','(%a0)+,%d2',2)
    emitter.ins('cmp.b','%d2,%d1',2)
    emitter.ins('beq.w','main_pc_02b408',4)
    emitter.ins('asl.w','#0x8,%d2',2)
    emitter.ins('move.b','(%a0)+,%d2',2)
    emitter.ins('or.w','0xff7008:l,%d2',6)
    emitter.ins('and.w','0xff700c:l,%d2',6)
    emitter.ins('move.w','%d2,0xc00000:l',6)
    emitter.ins('bsr.b','main_pc_02b430',2)
    emitter.ins('bra.b','main_pc_02b3e6',2)
    emitter.ins('moveq','#0,%d3',2)
    emitter.ins('move.b','(%a0)+,%d3',2)
    emitter.ins('beq.w','main_pc_02b444',4)
    emitter.ins('move.b','(%a0)+,%d2',2)
    emitter.ins('asl.w','#0x8,%d2',2)
    emitter.ins('move.b','(%a0)+,%d2',2)
    emitter.ins('or.w','0xff7008:l,%d2',6)
    emitter.ins('and.w','0xff700c:l,%d2',6)
    emitter.ins('move.w','%d2,0xc00000:l',6)
    emitter.ins('bsr.b','main_pc_02b430',2)
    emitter.ins('dbra','%d3,main_pc_02b416',4)
    emitter.ins('bra.b','main_pc_02b3e6',2)
    emitter.ins('addq.w','#0x1,%d4',2)
    emitter.ins('cmpi.b','#0x20,%d4',4)
    emitter.ins('bcs.w','main_pc_02b444',4)
    emitter.ins('adda.l','%d5,%a1',2)
    emitter.ins('move.w','%a1,%d0',2)
    emitter.ins('bsr.w','main_pc_02b446',4)
    emitter.ins('moveq','#0,%d4',2)
    emitter.ins('rts','',2)

def _lower_write_setup_video_address(emitter,rules):
    emitter.segment(0x2b446,0x2b46e)
    emitter.ins('movem.l','%d1,-(%a7)',4)
    emitter.ins('andi.l','#0xffff,%d0',6)
    emitter.ins('move.l','%d0,%d1',2)
    emitter.ins('andi.w','#0x3fff,%d0',4)
    emitter.ins('ori.w','#0x4000,%d0',4)
    emitter.ins('swap','%d0',2)
    emitter.ins('lsr.w','#0x8,%d1',2)
    emitter.ins('lsr.w','#0x6,%d1',2)
    emitter.ins('or.l','%d1,%d0',2)
    emitter.ins('move.l','%d0,0xc00004:l',6)
    emitter.ins('movem.l','(%a7)+,%d1',4)
    emitter.ins('rts','',2)

LOWERERS={
    'settle_city_projects_and_refresh_map':_lower_settle_city_projects_and_refresh_map,
    'settle_all_city_projects':_lower_settle_all_city_projects,
    'settle_first_city_project':_lower_settle_first_city_project,
    'settle_second_city_project':_lower_settle_second_city_project,
    'settle_third_city_project':_lower_settle_third_city_project,
    'dispatch_gameplay_command_state':_lower_dispatch_gameplay_command_state,
    'render_visible_map_packets':_lower_render_visible_map_packets,
    'render_selected_map_packet':_lower_render_selected_map_packet,
    'select_map_packet_sprite':_lower_select_map_packet_sprite,
    'locate_map_packet_sprite':_lower_locate_map_packet_sprite,
    'render_map_marker_positions':_lower_render_map_marker_positions,
    'append_city_currency_panel':_lower_append_city_currency_panel,
    'append_city_project_panel':_lower_append_city_project_panel,
    'append_two_row_sequential_tiles':_lower_append_two_row_sequential_tiles,
    'append_current_city_value':_lower_append_current_city_value,
    'append_selected_long_value':_lower_append_selected_long_value,
    'append_four_row_status_panel':_lower_append_four_row_status_panel,
    'append_four_row_tile_columns':_lower_append_four_row_tile_columns,
    'sort_map_packet_queue':_lower_sort_map_packet_queue,
    'append_missing_city_queue_packets':_lower_append_missing_city_queue_packets,
    'upload_selected_queue_officer_name':_lower_upload_selected_queue_officer_name,
    'dispatch_queue_command_state':_lower_dispatch_queue_command_state,
    'render_city_map_entries':_lower_render_city_map_entries,
    'render_city_map_entry':_lower_render_city_map_entry,
    'upload_first_battle_prompt':_lower_upload_first_battle_prompt,
    'upload_second_battle_prompt':_lower_upload_second_battle_prompt,
    'build_nearby_battle_targets':_lower_build_nearby_battle_targets,
    'append_nearby_target_candidates':_lower_append_nearby_target_candidates,
    'dispatch_target_eligibility':_lower_dispatch_target_eligibility,
    'upload_battle_action_prompt':_lower_upload_battle_action_prompt,
    'upload_battle_result_prompt':_lower_upload_battle_result_prompt,
    'upload_selected_officer_names':_lower_upload_selected_officer_names,
    'select_active_battle_controller':_lower_select_active_battle_controller,
    'update_direction_choice':_lower_update_direction_choice,
    'cycle_available_direction':_lower_cycle_available_direction,
    'render_direction_choice':_lower_render_direction_choice,
    'process_both_battle_force_turns':_lower_process_both_battle_force_turns,
    'settle_both_force_supply':_lower_settle_both_force_supply,
    'deduct_force_supply':_lower_deduct_force_supply,
    'apply_force_supply_losses':_lower_apply_force_supply_losses,
    'check_battle_commanders_present':_lower_check_battle_commanders_present,
    'execute_secondary_force_orders':_lower_execute_secondary_force_orders,
    'calculate_force_supply_budgets':_lower_calculate_force_supply_budgets,
    'execute_primary_force_orders':_lower_execute_primary_force_orders,
    'select_primary_force_order_policy':_lower_select_primary_force_order_policy,
    'initialize_battle_policy_targets':_lower_initialize_battle_policy_targets,
    'initialize_primary_policy_targets':_lower_initialize_primary_policy_targets,
    'collect_order_target_candidates':_lower_collect_order_target_candidates,
    'offset_first_order_target_axis':_lower_offset_first_order_target_axis,
    'offset_second_order_target_axis':_lower_offset_second_order_target_axis,
    'initialize_secondary_policy_targets':_lower_initialize_secondary_policy_targets,
    'update_first_setup_option':_lower_update_first_setup_option,
    'update_second_setup_option':_lower_update_second_setup_option,
    'update_third_setup_option':_lower_update_third_setup_option,
    'update_fourth_setup_option':_lower_update_fourth_setup_option,
    'update_setup_player_choices':_lower_update_setup_player_choices,
    'render_current_setup_option':_lower_render_current_setup_option,
    'advance_setup_reveal':_lower_advance_setup_reveal,
    'advance_setup_dismissal':_lower_advance_setup_dismissal,
    'cycle_setup_option':_lower_cycle_setup_option,
    'initialize_setup_video':_lower_initialize_setup_video,
    'decode_setup_plane_rows':_lower_decode_setup_plane_rows,
    'write_setup_video_address':_lower_write_setup_video_address,
}


# Finite actual new algorithm contracts, not old-body normalization.
APPROVED['contexts_render'] = {'RenderFields', 'checked_render_fields'}
APPROVED['contexts_tick'] = {'MapTickFrame', 'checked_tick_frame'}
APPROVED['reuse_display'] = {'append_map_sprite_transaction'}
RENDER_ACTUAL_DECLARATIONS = {'render_visible_map_packets': {'signature': 'state: SceneState, frame: MapPresentation',
                                'returns': 'MapPresentation',
                                'flow': 'checked_context(frame, MapPresentation, state)\n'
                                        'fields = _visible_map_packet_fields(state, '
                                        '_render_from_map(frame))\n'
                                        'return _render_to_map(frame, fields)'},
 'render_selected_map_packet': {'signature': 'state: SceneState, frame: MapPresentation',
                                'returns': 'MapPresentation',
                                'flow': 'checked_context(frame, MapPresentation, state)\n'
                                        'fields = _selected_map_packet_fields(state, '
                                        '_render_from_map(frame))\n'
                                        'return _render_to_map(frame, fields)'},
 'select_map_packet_sprite': {'signature': 'state: SceneState, frame: MapPresentation',
                              'returns': 'MapPresentation',
                              'flow': 'checked_context(frame, MapPresentation, state)\n'
                                      'fields = _select_map_sprite_fields(state, '
                                      '_render_from_map(frame))\n'
                                      'return _render_to_map(frame, fields)'},
 'locate_map_packet_sprite': {'signature': 'state: SceneState, frame: MapPresentation',
                              'returns': 'MapPresentation',
                              'flow': 'checked_context(frame, MapPresentation, state)\n'
                                      'fields = _locate_map_sprite_fields(state, '
                                      '_render_from_map(frame))\n'
                                      'return _render_to_map(frame, fields)'},
 'render_map_marker_positions': {'signature': 'state: SceneState, frame: MapPresentation',
                                 'returns': 'MapPresentation',
                                 'flow': 'checked_context(frame, MapPresentation, state)\n'
                                         'fields = _map_marker_fields(state, '
                                         '_render_from_map(frame))\n'
                                         'return _render_to_map(frame, fields)'},
 'render_city_map_entries': {'signature': 'state: SceneState, frame: MapPresentation',
                             'returns': 'MapPresentation',
                             'flow': 'checked_context(frame, MapPresentation, state)\n'
                                     'fields = _city_map_fields(state, _render_from_map(frame))\n'
                                     'return _render_to_map(frame, fields)'},
 'render_city_map_entry': {'signature': 'state: SceneState, frame: MapPresentation',
                           'returns': 'MapPresentation',
                           'flow': 'checked_context(frame, MapPresentation, state)\n'
                                   'fields = _city_map_entry_fields(state, '
                                   '_render_from_map(frame))\n'
                                   'return _render_to_map(frame, fields)'},
 'select_active_battle_controller': {'signature': 'state: SceneState, frame: MapPresentation',
                                     'returns': 'MapPresentation',
                                     'flow': 'checked_context(frame, MapPresentation, state)\n'
                                             'fields = _active_controller_fields(state, '
                                             '_render_from_map(frame))\n'
                                             'return _render_to_map(frame, fields)'},
 '_render_from_map': {'signature': 'frame',
                      'returns': None,
                      'flow': 'return RenderFields(frame.x, frame.y, frame.attributes, frame.tile, '
                              'frame.officer, frame.count, frame.index, frame.remaining, '
                              'frame.source, frame.destination, frame.packet, None, None, None, '
                              'None, None)'},
 '_render_from_tick': {'signature': 'state, frame',
                       'returns': None,
                       'flow': 'checked_tick_frame(frame, state)\n'
                               'return RenderFields(frame.motion_x, frame.motion_y, '
                               'frame.attributes, frame.tile_count, frame.officer, frame.count, '
                               'frame.index, frame.control_latch, frame.source, frame.destination, '
                               'frame.packet, frame.carry, frame.zero, frame.negative, '
                               'frame.overflow, frame.stack_cursor)'},
 '_render_to_map': {'signature': 'frame, fields',
                    'returns': None,
                    'flow': 'return replace(frame, x=fields.x, y=fields.y, '
                            'attributes=fields.attributes, tile=fields.tile, '
                            'officer=fields.officer, count=fields.count, index=fields.index, '
                            'remaining=fields.remaining, source=fields.source, '
                            'destination=fields.destination, packet=fields.packet)'},
 '_render_to_tick': {'signature': 'state, frame, fields',
                     'returns': None,
                     'flow': 'checked_render_fields(fields, state)\n'
                             'result = replace(frame, motion_x=fields.x, motion_y=fields.y, '
                             'attributes=fields.attributes, tile_count=fields.tile, '
                             'officer=fields.officer, count=fields.count, index=fields.index, '
                             'control_latch=fields.remaining, source=fields.source, '
                             'destination=fields.destination, packet=fields.packet, '
                             'carry=fields.carry, zero=fields.zero, negative=fields.negative, '
                             'overflow=fields.overflow, stack_cursor=fields.stack_cursor)\n'
                             'return checked_tick_frame(result, state)'},
 '_render_move': {'signature': 'fields, value, bits',
                  'returns': None,
                  'flow': 'masked = value & (1 << bits) - 1\n'
                          'return replace(fields, carry=False, zero=masked == 0, '
                          'negative=bool(masked & 1 << bits - 1), overflow=False)'},
 '_render_compare': {'signature': 'fields, left, right, bits',
                     'returns': None,
                     'flow': 'mask = (1 << bits) - 1\n'
                             'sign = 1 << bits - 1\n'
                             'left, right = (left & mask, right & mask)\n'
                             'difference = left - right & mask\n'
                             'return replace(fields, carry=left < right, zero=difference == 0, '
                             'negative=bool(difference & sign), overflow=bool((left ^ right) & '
                             '(left ^ difference) & sign))'},
 '_render_add': {'signature': 'fields, left, amount',
                 'returns': None,
                 'flow': 'left, amount = (low16(left), low16(amount))\n'
                         'total = left + amount\n'
                         'result = u16(total)\n'
                         'return replace(fields, carry=total > 65535, zero=result == 0, '
                         'negative=bool(result & 32768), overflow=bool(~(left ^ amount) & (left ^ '
                         'result) & 32768))'},
 '_render_bit': {'signature': 'fields, value, bit',
                 'returns': None,
                 'flow': 'return replace(fields, zero=not bool(value & 1 << bit))'},
 '_render_packet': {'signature': 'fields',
                    'returns': None,
                    'flow': 'if fields.packet is None:\n'
                            "    raise Boundary('real current map packet required')\n"
                            'return fields.packet'},
 '_render_sprite_fields': {'signature': 'state, fields',
                           'returns': None,
                           'flow': 'from .reuse_display import append_map_sprite_transaction\n'
                                   'if fields.source is None:\n'
                                   "    raise Boundary('actual external sprite source required')\n"
                                   'source = fields.source if type(fields.source) is Cursor else '
                                   'fields.source.cursor()\n'
                                   'fields = _render_enter_call(fields)\n'
                                   'result = append_map_sprite_transaction(state, source, '
                                   'fields.x, fields.y, fields.attributes, reset_scroll=False, '
                                   'initialize_clip=True)\n'
                                   'fields = _render_leave_call(fields)\n'
                                   'return replace(fields, source=result.source, x=result.x, '
                                   'y=result.y, attributes=result.attributes, carry=result.carry, '
                                   'zero=result.zero, negative=result.negative, '
                                   'overflow=result.overflow)'},
 '_visible_map_packet_fields': {'signature': 'state, fields',
                                'returns': None,
                                'flow': 'checked_render_fields(fields, state)\n'
                                        "packet = _ram(state, '9000').cursor()\n"
                                        'fields = replace(fields, packet=packet)\n'
                                        'while True:\n'
                                        '    officer = replace_byte(fields.officer, '
                                        'packet.byte())\n'
                                        '    fields = _render_move(replace(fields, '
                                        'officer=officer), officer, 8)\n'
                                        '    if not low8(officer):\n'
                                        '        return '
                                        '_render_leave_call(_map_marker_fields(state, '
                                        '_render_enter_call(fields)))\n'
                                        '    fields = _render_bit(fields, officer, 5)\n'
                                        '    if not officer & 32:\n'
                                        '        count = replace_word(fields.count, '
                                        'u16((packet.byte(1) << 4) + 16))\n'
                                        "        scroll = _word(state, 'f314')\n"
                                        '        fields = _render_compare(fields, low16(count), '
                                        'scroll, 16)\n'
                                        '        count = replace_word(count, u16(low16(count) - '
                                        'scroll))\n'
                                        '        fields = replace(fields, count=count)\n'
                                        '        if not fields.carry:\n'
                                        '            fields = _render_compare(fields, count, 240, '
                                        '16)\n'
                                        '            if fields.carry:\n'
                                        '                count = replace_word(fields.count, '
                                        'u16((packet.byte(2) << 4) + 16))\n'
                                        "                scroll = _word(state, 'f318')\n"
                                        '                fields = _render_compare(fields, count, '
                                        'scroll, 16)\n'
                                        '                count = replace_word(count, '
                                        'u16(low16(count) - scroll))\n'
                                        '                fields = replace(fields, count=count)\n'
                                        '                if not fields.carry:\n'
                                        '                    fields = _render_compare(fields, '
                                        'count, 336, 16)\n'
                                        '                    if fields.carry:\n'
                                        '                        fields = '
                                        '_render_leave_call(_selected_map_packet_fields(state, '
                                        '_render_enter_call(fields)))\n'
                                        '                        packet = _render_packet(fields)\n'
                                        '    count = replace_byte(replace_word(fields.count, 0), '
                                        'packet.byte())\n'
                                        '    count = replace_word(count, low16(count) & 15)\n'
                                        '    fields = _render_move(replace(fields, count=count), '
                                        'count, 16)\n'
                                        '    packet.base = u32(packet.base + 13 + '
                                        's16(low16(count)))'},
 '_selected_map_packet_fields': {'signature': 'state, fields',
                                 'returns': None,
                                 'flow': 'checked_render_fields(fields, state)\n'
                                         'packet = _render_packet(fields)\n'
                                         "mode = _word(state, 'f36c')\n"
                                         'fields = _render_compare(fields, mode, 2, 16)\n'
                                         'if mode == 2:\n'
                                         '    x = replace_byte(fields.x, packet.byte(4))\n'
                                         "    selected = _ram(state, 'f377').byte()\n"
                                         '    fields = _render_compare(replace(fields, x=x), x, '
                                         'selected, 8)\n'
                                         '    if low8(x) == selected:\n'
                                         '        x = replace_byte(fields.x, packet.byte())\n'
                                         '        fields = '
                                         '_render_bit(_render_move(replace(fields, x=x), x, 8), x, '
                                         '4)\n'
                                         '        if not x & 16:\n'
                                         "            option = _ram(state, 'f321').byte()\n"
                                         '            fields = _render_bit(fields, option, 2)\n'
                                         '            if option & 4:\n'
                                         '                return fields\n'
                                         'fields = '
                                         '_render_leave_call(_locate_map_sprite_fields(state, '
                                         '_render_enter_call(fields)))\n'
                                         'fields = '
                                         '_render_leave_call(_select_map_sprite_fields(state, '
                                         '_render_enter_call(fields)))\n'
                                         'flag = packet.byte()\n'
                                         'fields = _render_move(fields, flag, 8)\n'
                                         'attributes = replace_word(fields.attributes, 2048 if '
                                         'negative_byte(flag) else 0)\n'
                                         'fields = replace(fields, attributes=attributes)\n'
                                         'if negative_byte(flag):\n'
                                         '    fields = _render_move(fields, attributes, 16)\n'
                                         "_put(state, 'f60a', _word(state, 'f314'))\n"
                                         "_put(state, 'f60e', _word(state, 'f318'))\n"
                                         'return _render_sprite_fields(state, fields)'},
 '_select_map_sprite_fields': {'signature': 'state, fields',
                               'returns': None,
                               'flow': 'checked_render_fields(fields, state)\n'
                                       "source = data_view(state, 'data_015eb8').cursor()\n"
                                       "option = _ram(state, 'f321').byte()\n"
                                       'fields = _render_bit(fields, option, 4)\n'
                                       'if option & 16:\n'
                                       '    source.base = u32(source.base + 8)\n'
                                       'fields = replace(fields, source=source)\n'
                                       'saved_observations = fields\n'
                                       'fields = _render_save_terrain(state, fields)\n'
                                       'from .services import query_scaled_terrain\n'
                                       'fields = _render_enter_call(fields)\n'
                                       'terrain = query_scaled_terrain(state, fields.x, fields.y, '
                                       'fields.attributes, fields.tile)\n'
                                       'fields = _render_leave_call(fields)\n'
                                       'fields = replace(fields, attributes=terrain.terrain, '
                                       'tile=terrain.cost)\n'
                                       'fields = _render_restore_terrain(state, fields, '
                                       'saved_observations)\n'
                                       'fields = _render_compare(fields, terrain.terrain, 4, 16)\n'
                                       'source = fields.source\n'
                                       'if low16(terrain.terrain) == 4:\n'
                                       "    source = data_view(state, 'data_015ec8').cursor()\n"
                                       'return replace(fields, source=source)'},
 '_locate_map_sprite_fields': {'signature': 'state, fields',
                               'returns': None,
                               'flow': 'checked_render_fields(fields, state)\n'
                                       'packet = _render_packet(fields)\n'
                                       "mode = _word(state, 'f612')\n"
                                       'fields = _render_compare(fields, mode, 521, 16)\n'
                                       'special = False\n'
                                       'if mode == 521:\n'
                                       "    phase = _word(state, 'f362')\n"
                                       '    fields = _render_compare(fields, phase, 6, 16)\n'
                                       '    if phase == 6:\n'
                                       "        x = replace_word(fields.x, _word(state, '3bb4'))\n"
                                       '        selected = packet.byte(13)\n'
                                       '        fields = _render_compare(replace(fields, x=x), x, '
                                       'selected, 8)\n'
                                       '        special = low8(x) == selected\n'
                                       'if special:\n'
                                       "    x = replace_word(fields.x, _word(state, '3bb6'))\n"
                                       '    fields = _render_add(fields, x, 8)\n'
                                       '    x = replace_word(x, u16(low16(x) + 8))\n'
                                       "    y = replace_word(fields.y, _word(state, '3bb8'))\n"
                                       'else:\n'
                                       '    x = replace_word(fields.x, u16(packet.byte(1) << 4))\n'
                                       '    x = replace_word(x, u16(low16(x) + 8))\n'
                                       '    y = replace_word(fields.y, u16(packet.byte(2) << 4))\n'
                                       'fields = _render_add(fields, y, 8)\n'
                                       'y = replace_word(y, u16(low16(y) + 8))\n'
                                       'return replace(fields, x=x, y=y)'},
 '_map_marker_fields': {'signature': 'state, fields',
                        'returns': None,
                        'flow': 'checked_render_fields(fields, state)\n'
                                "markers = _ram(state, '9f00').cursor()\n"
                                'fields = replace(fields, destination=markers)\n'
                                'while True:\n'
                                '    x = replace_word(fields.x, markers.next_word())\n'
                                '    fields = _render_move(replace(fields, x=x), x, 16)\n'
                                '    if negative_word(low16(x)):\n'
                                '        return fields\n'
                                '    y = replace_word(fields.y, markers.next_word())\n'
                                '    attributes = replace_word(fields.attributes, u16(low16(x) + '
                                '16))\n'
                                "    scroll = _word(state, 'f314')\n"
                                '    fields = _render_compare(fields, attributes, scroll, 16)\n'
                                '    attributes = replace_word(attributes, u16(low16(attributes) - '
                                'scroll))\n'
                                '    fields = replace(fields, y=y, attributes=attributes)\n'
                                '    if fields.carry:\n'
                                '        continue\n'
                                '    fields = _render_compare(fields, attributes, 240, 16)\n'
                                '    if not fields.carry and (not fields.zero):\n'
                                '        continue\n'
                                '    attributes = replace_word(fields.attributes, u16(low16(y) + '
                                '16))\n'
                                "    scroll = _word(state, 'f318')\n"
                                '    fields = _render_compare(fields, attributes, scroll, 16)\n'
                                '    attributes = replace_word(attributes, u16(low16(attributes) - '
                                'scroll))\n'
                                '    fields = replace(fields, attributes=attributes)\n'
                                '    if fields.carry:\n'
                                '        continue\n'
                                '    fields = _render_compare(fields, attributes, 336, 16)\n'
                                '    if not fields.carry and (not fields.zero):\n'
                                '        continue\n'
                                "    _put(state, 'f60a', _word(state, 'f314'))\n"
                                "    _put(state, 'f60e', _word(state, 'f318'))\n"
                                '    fields = _render_sprite_fields(state, replace(fields, '
                                "source=data_view(state, 'data_015f6a').cursor(), "
                                'attributes=replace_word(attributes, 0)))'},
 '_city_map_fields': {'signature': 'state, fields',
                      'returns': None,
                      'flow': 'checked_render_fields(fields, state)\n'
                              "packet = _ram(state, 'ce9c').cursor()\n"
                              'fields = _render_move(replace(fields, packet=packet, '
                              'tile=replace_word(fields.tile, 39)), 39, 16)\n'
                              'while True:\n'
                              '    tile = fields.tile\n'
                              '    flag = packet.byte()\n'
                              '    fields = _render_move(replace(fields, tile=tile), flag, 8)\n'
                              '    if flag:\n'
                              '        flag = packet.byte()\n'
                              '        fields = _render_bit(fields, flag, 4)\n'
                              '        if not flag & 16:\n'
                              '            x = replace_word(fields.x, u16(packet.byte(1) << 4))\n'
                              '            attributes = replace_word(fields.attributes, '
                              'u16(low16(x) + 16))\n'
                              "            scroll = _word(state, 'f314')\n"
                              '            fields = _render_compare(fields, attributes, scroll, '
                              '16)\n'
                              '            attributes = replace_word(attributes, '
                              'u16(low16(attributes) - scroll))\n'
                              '            fields = replace(fields, x=x, attributes=attributes)\n'
                              '            if not fields.carry:\n'
                              '                fields = _render_compare(fields, attributes, 240, '
                              '16)\n'
                              '                if fields.carry or fields.zero:\n'
                              '                    y = replace_word(fields.y, u16(packet.byte(2) '
                              '<< 4))\n'
                              '                    attributes = replace_word(fields.attributes, '
                              'u16(low16(y) + 16))\n'
                              "                    scroll = _word(state, 'f318')\n"
                              '                    fields = _render_compare(fields, attributes, '
                              'scroll, 16)\n'
                              '                    attributes = replace_word(attributes, '
                              'u16(low16(attributes) - scroll))\n'
                              '                    fields = replace(fields, y=y, '
                              'attributes=attributes)\n'
                              '                    if not fields.carry:\n'
                              '                        fields = _render_compare(fields, '
                              'attributes, 336, 16)\n'
                              '                        if fields.carry or fields.zero:\n'
                              '                            fields = '
                              '_render_leave_call(_city_map_entry_fields(state, '
                              '_render_enter_call(fields)))\n'
                              '                            packet = _render_packet(fields)\n'
                              '    packet.base = u32(packet.base - 4)\n'
                              '    fields = replace(fields, tile=replace_word(fields.tile, '
                              'u16(low16(fields.tile) - 1)))\n'
                              '    if low16(fields.tile) == 65535:\n'
                              '        return fields'},
 '_city_map_entry_fields': {'signature': 'state, fields',
                            'returns': None,
                            'flow': 'checked_render_fields(fields, state)\n'
                                    'packet = _render_packet(fields)\n'
                                    'saved_tile = fields.tile\n'
                                    'fields = _render_push_value(state, fields, fields.tile)\n'
                                    "mode = _word(state, 'f612')\n"
                                    'fields = _render_compare(fields, mode, 522, 16)\n'
                                    'if mode == 522:\n'
                                    "    phase = _word(state, 'f362')\n"
                                    '    fields = _render_compare(fields, phase, 2, 16)\n'
                                    '    if phase == 2:\n'
                                    "        selected = _word(state, 'cea0')\n"
                                    '        fields = _render_compare(fields, saved_tile, '
                                    'selected, 16)\n'
                                    '        if low16(saved_tile) == selected:\n'
                                    '            fields = replace(fields, x=replace_word(fields.x, '
                                    "_word(state, 'cea4')), y=replace_word(fields.y, _word(state, "
                                    "'cea6')))\n"
                                    "source = data_view(state, 'data_016a78').cursor()\n"
                                    "option = _ram(state, 'f321').byte()\n"
                                    'fields = _render_bit(fields, option, 4)\n'
                                    'if not option & 16:\n'
                                    '    source.base = u32(source.base + 8)\n'
                                    'fields = replace(fields, source=source)\n'
                                    'saved_observations = fields\n'
                                    'fields = _render_save_terrain(state, fields)\n'
                                    'from .services import query_scaled_terrain\n'
                                    'fields = _render_enter_call(fields)\n'
                                    'terrain = query_scaled_terrain(state, replace_word(fields.x, '
                                    'u16(low16(fields.x) + 8)), replace_word(fields.y, '
                                    'u16(low16(fields.y) + 8)), fields.attributes, fields.tile)\n'
                                    'fields = _render_leave_call(fields)\n'
                                    'fields = _render_compare(replace(fields, '
                                    'attributes=terrain.terrain, tile=terrain.cost), '
                                    'terrain.terrain, 4, 16)\n'
                                    'fields = _render_restore_terrain(state, fields, '
                                    'saved_observations)\n'
                                    'source, packet = (fields.source, fields.packet)\n'
                                    'if low16(terrain.terrain) == 4:\n'
                                    '    source.base = u32(source.base + 16)\n'
                                    'y = replace_word(fields.y, u16(low16(fields.y) + 8))\n'
                                    'flag = packet.byte()\n'
                                    'fields = _render_move(fields, flag, 8)\n'
                                    'attributes = replace_word(fields.attributes, 2048 if '
                                    'negative_byte(flag) else 0)\n'
                                    'fields = replace(fields, y=y, attributes=attributes, '
                                    'source=source)\n'
                                    "_put(state, 'f60a', _word(state, 'f314'))\n"
                                    "_put(state, 'f60e', _word(state, 'f318'))\n"
                                    'fields = _render_sprite_fields(state, fields)\n'
                                    'fields, restored_tile = _render_pop_value(state, fields, '
                                    'saved_tile)\n'
                                    'return _render_move(replace(fields, tile=restored_tile), '
                                    'restored_tile, 32)'},
 '_active_controller_fields': {'signature': 'state, fields',
                               'returns': None,
                               'flow': 'checked_render_fields(fields, state)\n'
                                       "mode = _word(state, 'f612')\n"
                                       'fields = _render_compare(fields, mode, 1031, 16)\n'
                                       'if mode == 1031:\n'
                                       "    phase = _word(state, 'f362')\n"
                                       '    fields = _render_move(fields, phase, 16)\n'
                                       '    if not phase:\n'
                                       '        return fields\n'
                                       "    phase = _word(state, 'f362')\n"
                                       '    fields = _render_compare(fields, phase, 2, 16)\n'
                                       '    if phase == 2:\n'
                                       '        return fields\n'
                                       "    phase = _word(state, 'f362')\n"
                                       '    fields = _render_compare(fields, phase, 4, 16)\n'
                                       '    if phase == 4:\n'
                                       '        return fields\n'
                                       "x = replace_word(fields.x, _word(state, 'f68c'))\n"
                                       "y = replace_word(fields.y, _word(state, 'f68e'))\n"
                                       "option = _ram(state, 'f6d7').byte()\n"
                                       'fields = _render_bit(replace(fields, x=x, y=y), option, '
                                       '1)\n'
                                       'if option & 2:\n'
                                       '    x, y = (y, x)\n'
                                       '    fields = replace(fields, x=x, y=y)\n'
                                       "compared = _word(state, 'f67a')\n"
                                       'fields = _render_compare(fields, x, compared, 16)\n'
                                       'if low16(x) == compared:\n'
                                       '    return fields\n'
                                       "compared = _word(state, 'f67c')\n"
                                       'fields = _render_compare(fields, x, compared, 16)\n'
                                       'if low16(x) != compared:\n'
                                       "    compared = _word(state, 'f67e')\n"
                                       '    fields = _render_compare(fields, x, compared, 16)\n'
                                       '    if low16(x) == compared:\n'
                                       "        compared = _word(state, 'f67c')\n"
                                       '        fields = _render_compare(fields, y, compared, 16)\n'
                                       '        if low16(y) == compared:\n'
                                       '            return fields\n'
                                       '    else:\n'
                                       "        compared = _word(state, 'f67a')\n"
                                       '        fields = _render_compare(fields, y, compared, 16)\n'
                                       '        if low16(y) == compared:\n'
                                       '            return fields\n'
                                       "value = _word(state, 'f604')\n"
                                       "_put(state, 'f602', value)\n"
                                       'return _render_move(fields, value, 16)'},
 'render_visible_map_packets_complete': {'signature': 'state: SceneState, frame: MapTickFrame',
                                         'returns': 'MapTickFrame',
                                         'flow': 'fields = _visible_map_packet_fields(state, '
                                                 '_render_from_tick(state, frame))\n'
                                                 'return _render_to_tick(state, frame, fields)'},
 'render_city_map_entries_complete': {'signature': 'state: SceneState, frame: MapTickFrame',
                                      'returns': 'MapTickFrame',
                                      'flow': 'fields = _city_map_fields(state, '
                                              '_render_from_tick(state, frame))\n'
                                              'return _render_to_tick(state, frame, fields)'},
 'select_active_battle_controller_complete': {'signature': 'state: SceneState, frame: MapTickFrame',
                                              'returns': 'MapTickFrame',
                                              'flow': 'fields = _active_controller_fields(state, '
                                                      '_render_from_tick(state, frame))\n'
                                                      'return _render_to_tick(state, frame, '
                                                      'fields)'},
 '_render_push_value': {'signature': 'state, fields, value',
                        'returns': None,
                        'flow': 'if fields.stack_cursor is None:\n'
                                '    return fields\n'
                                'stack = fields.stack_cursor.advance(-4)\n'
                                'stack.set_long(0, value)\n'
                                'return replace(fields, stack_cursor=stack)'},
 '_render_pop_value': {'signature': 'state, fields, legacy_observation',
                       'returns': None,
                       'flow': 'if fields.stack_cursor is None:\n'
                               '    return (fields, legacy_observation)\n'
                               'value = fields.stack_cursor.long()\n'
                               'return (replace(fields, '
                               'stack_cursor=fields.stack_cursor.advance(4)), value)'},
 '_render_enter_call': {'signature': 'fields',
                        'returns': None,
                        'flow': 'if fields.stack_cursor is None:\n'
                                '    return fields\n'
                                'return replace(fields, '
                                'stack_cursor=fields.stack_cursor.advance(-4))'},
 '_render_leave_call': {'signature': 'fields',
                        'returns': None,
                        'flow': 'if fields.stack_cursor is None:\n'
                                '    return fields\n'
                                'return replace(fields, '
                                'stack_cursor=fields.stack_cursor.advance(4))'},
 '_render_save_terrain': {'signature': 'state, fields',
                          'returns': None,
                          'flow': 'if fields.source is None or fields.packet is None:\n'
                                  "    raise Boundary('real terrain-call source and packet aliases "
                                  "required')\n"
                                  'fields = _render_push_value(state, fields, fields.packet.base)\n'
                                  'fields = _render_push_value(state, fields, fields.source.base)\n'
                                  'fields = _render_push_value(state, fields, fields.y)\n'
                                  'return _render_push_value(state, fields, fields.x)'},
 '_render_restore_terrain': {'signature': 'state, fields, legacy_observations',
                             'returns': None,
                             'flow': 'if fields.stack_cursor is None:\n'
                                     '    return replace(fields, x=legacy_observations.x, '
                                     'y=legacy_observations.y, source=legacy_observations.source, '
                                     'packet=legacy_observations.packet)\n'
                                     'fields, x = _render_pop_value(state, fields, '
                                     'legacy_observations.x)\n'
                                     'fields, y = _render_pop_value(state, fields, '
                                     'legacy_observations.y)\n'
                                     'fields, source = _render_pop_value(state, fields, '
                                     'legacy_observations.source.base)\n'
                                     'fields, packet = _render_pop_value(state, fields, '
                                     'legacy_observations.packet.base)\n'
                                     'return replace(fields, x=x, y=y, '
                                     'source=state.table_at(source).cursor(), '
                                     'packet=state.table_at(packet).cursor())'}}
DECLARATIONS.update(RENDER_ACTUAL_DECLARATIONS)
RENDER_OWNER_ALGORITHMS = {'render_visible_map_packets': ['_visible_map_packet_fields',
                                '_selected_map_packet_fields',
                                '_select_map_sprite_fields',
                                '_locate_map_sprite_fields',
                                '_map_marker_fields'],
 'render_selected_map_packet': ['_selected_map_packet_fields',
                                '_select_map_sprite_fields',
                                '_locate_map_sprite_fields'],
 'select_map_packet_sprite': ['_select_map_sprite_fields'],
 'locate_map_packet_sprite': ['_locate_map_sprite_fields'],
 'render_map_marker_positions': ['_map_marker_fields'],
 'render_city_map_entries': ['_city_map_fields', '_city_map_entry_fields'],
 'render_city_map_entry': ['_city_map_entry_fields'],
 'select_active_battle_controller': ['_active_controller_fields']}

def compile_source(source):
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    for owner, helper in (('initialize_battle_policy_targets', '_load_battle_policy_map'), ('initialize_primary_policy_targets', '_read_battle_policy_anchor')):
        records[owner]['effects'] += '\nactual supplied same-state policy bridge: ' + records[helper]['effects']
    for owner in DEPLOYMENT_FIELD_OWNERS:
        records[owner]['effects'] += '\nactual supplied deployment call/return helpers: ' + '\n'.join((records[name]['effects'] for name in DEPLOYMENT_BRIDGE_HELPERS))
    for owner, algorithms in RENDER_OWNER_ALGORITHMS.items():
        records[owner]['effects'] = dict(legacy_projection=records[owner]['effects'], actual_algorithms={name: records[name]['effects'] for name in algorithms}, actual_complete_interfaces={name: records[name]['effects'] for name in ('render_visible_map_packets_complete', 'render_city_map_entries_complete', 'select_active_battle_controller_complete')}, supplied_live_fields={name: records[name]['effects'] for name in ('_render_from_map', '_render_from_tick', '_render_to_map', '_render_to_tick', '_render_move', '_render_compare', '_render_add', '_render_bit', '_render_packet', '_render_sprite_fields', '_render_push_value', '_render_pop_value', '_render_enter_call', '_render_leave_call', '_render_save_terrain', '_render_restore_terrain')})
    records['execute_primary_force_orders']['effects'] += '\nactual primary order chain: ' + '\n'.join((records[name]['effects'] for name in PRIMARY_ORDER_HELPERS))
    for owner in ('apply_force_supply_losses', 'calculate_force_supply_budgets', 'check_battle_commanders_present', 'deduct_force_supply', 'execute_secondary_force_orders', 'process_both_battle_force_turns', 'settle_both_force_supply'):
        records[owner]['effects'] += '\nsole complete force-turn fields: ' + '\n'.join((records[name]['effects'] for name in ('_force_budget_roster_fields', '_force_loss_compact_member_fields', '_force_loss_message_fields', '_force_turn_call_fields', '_force_turn_divu_mask_fields', '_force_turn_policy_fields', 'apply_force_supply_losses_fields', 'calculate_force_supply_budgets_fields', 'check_battle_commanders_present_fields', 'deduct_force_supply_fields', 'execute_secondary_force_orders_fields', 'process_both_battle_force_turns_fields', 'settle_both_force_supply_fields')))
    for owner in ('settle_all_city_projects', 'settle_city_projects_and_refresh_map', 'settle_first_city_project', 'settle_second_city_project', 'settle_third_city_project'):
        records[owner]['effects'] += '\nsole complete city project fields: ' + '\n'.join((records[name]['effects'] for name in ('_city_project_aptitude_fields', '_city_project_begin_fields', '_city_project_call_fields', '_city_project_cancel_fields', '_city_project_divu_fields', '_city_project_intellect_reward_fields', '_city_project_legacy_entry_fields', '_city_project_legacy_result_fields', '_city_project_pay_fields', 'settle_all_city_projects_fields', 'settle_city_projects_and_refresh_map_fields', 'settle_first_city_project_fields', 'settle_second_city_project_fields', 'settle_third_city_project_fields')))
    sole_map_presentation_fields = {name: records[name]['effects'] for name in ('_map_presentation_append_fields', '_map_presentation_arithmetic_fields', '_map_presentation_bit_fields', '_map_presentation_call_fields', '_map_presentation_db_fields', '_map_presentation_emit_fields', '_map_presentation_legacy_map_fields', '_map_presentation_legacy_map_result', '_map_presentation_legacy_render_fields', '_map_presentation_legacy_render_result', '_map_presentation_legacy_search_fields', '_map_presentation_legacy_search_result', '_map_presentation_memory_arithmetic_fields', '_map_presentation_scaled_terrain_fields', '_map_presentation_tile_column_fields', 'append_city_currency_panel_fields', 'append_city_project_panel_fields', 'append_current_city_value_fields', 'append_four_row_status_panel_fields', 'append_four_row_tile_columns_fields', 'append_missing_city_queue_packets_fields', 'append_nearby_target_candidates_fields', 'append_selected_long_value_fields', 'append_two_row_sequential_tiles_fields', 'build_nearby_battle_targets_fields', 'locate_map_packet_sprite_fields', 'render_city_map_entries_fields', 'render_city_map_entry_fields', 'render_map_marker_positions_fields', 'render_selected_map_packet_fields', 'render_visible_map_packets_fields', 'select_active_battle_controller_fields', 'select_map_packet_sprite_fields', 'sort_map_packet_queue_fields')}
    for owner in ('render_visible_map_packets', 'render_selected_map_packet', 'select_map_packet_sprite', 'locate_map_packet_sprite', 'render_map_marker_positions', 'append_city_currency_panel', 'append_city_project_panel', 'append_two_row_sequential_tiles', 'append_current_city_value', 'append_selected_long_value', 'append_four_row_status_panel', 'append_four_row_tile_columns', 'sort_map_packet_queue', 'append_missing_city_queue_packets', 'render_city_map_entries', 'render_city_map_entry', 'build_nearby_battle_targets', 'append_nearby_target_candidates', 'select_active_battle_controller'):
        records[owner]['effects'] = dict(legacy_projection=records[owner]['effects'], sole_current_map_fields=sole_map_presentation_fields)
    sole_setup_assignment_fields = {name: records[name]['effects'] for name in ('_setup_advance_plane_row_call_fields', '_setup_advance_plane_row_fields', '_setup_asl_word_fields', '_setup_call_fields', '_setup_change_word_fields', '_setup_compare_memory_fields', '_setup_coordinate_high_byte_fields', '_setup_legacy_entry_fields', '_setup_legacy_result_fields', '_setup_palette_transition_fields', '_setup_plane_legacy_entry_fields', '_setup_plane_legacy_result_fields', '_setup_plane_rows_fields', '_setup_transfer_longs_fields', '_setup_update_option_fields', '_setup_write_fields', 'advance_setup_dismissal_fields', 'advance_setup_plane_row_fields', 'advance_setup_reveal_fields', 'cycle_setup_option_fields', 'decode_setup_plane_rows_fields', 'decode_setup_plane_rows_with_masks_fields', 'initialize_setup_video_fields', 'render_current_setup_option_fields', 'update_first_setup_option_fields', 'update_fourth_setup_option_fields', 'update_second_setup_option_fields', 'update_setup_player_choices_fields', 'update_third_setup_option_fields', 'write_setup_video_address_fields')}
    for owner in ('update_first_setup_option', 'update_second_setup_option', 'update_third_setup_option', 'update_fourth_setup_option', 'update_setup_player_choices', 'render_current_setup_option', 'advance_setup_reveal', 'advance_setup_dismissal', 'cycle_setup_option', 'initialize_setup_video', 'decode_setup_plane_rows', 'write_setup_video_address', 'decode_setup_plane_rows_with_masks', 'advance_setup_plane_row'):
        records[owner]['effects'] = dict(legacy_projection=records[owner]['effects'], sole_current_setup_assignment_fields=sole_setup_assignment_fields)
    sole_game_text_fields = {name: records[name]['effects'] for name in ('_game_text_battle_prompt_fields', '_game_text_call_fields', '_game_text_fill_longs_fields', '_game_text_indexed_dispatch_fields', '_game_text_upload_longs_fields', 'cycle_available_direction_fields', 'dispatch_gameplay_command_state_fields', 'dispatch_queue_command_state_fields', 'dispatch_target_eligibility_fields', 'render_direction_choice_fields', 'update_direction_choice_fields', 'upload_battle_action_prompt_fields', 'upload_battle_result_prompt_fields', 'upload_first_battle_prompt_fields', 'upload_second_battle_prompt_fields', 'upload_selected_officer_names_fields', 'upload_selected_queue_officer_name_fields')}
    for owner in ('dispatch_gameplay_command_state', 'upload_selected_queue_officer_name', 'dispatch_queue_command_state', 'upload_first_battle_prompt', 'upload_second_battle_prompt', 'dispatch_target_eligibility', 'upload_battle_action_prompt', 'upload_battle_result_prompt', 'upload_selected_officer_names', 'update_direction_choice', 'cycle_available_direction', 'render_direction_choice'):
        records[owner]['effects'] = dict(legacy_projection=records[owner]['effects'], sole_current_game_text_fields=sole_game_text_fields)
    for owner, field in (('execute_primary_force_orders', 'execute_primary_force_orders_frame_fields'), ('select_primary_force_order_policy', 'select_primary_force_order_policy_frame_fields'), ('initialize_battle_policy_targets', 'initialize_battle_policy_targets_frame_fields'), ('initialize_primary_policy_targets', 'initialize_primary_policy_targets_frame_fields'), ('collect_order_target_candidates', 'collect_order_target_candidates_frame_fields'), ('offset_first_order_target_axis', 'offset_first_order_target_axis_frame_fields'), ('offset_second_order_target_axis', 'offset_second_order_target_axis_frame_fields'), ('initialize_secondary_policy_targets', 'initialize_secondary_policy_targets_frame_fields')):
        records[owner]['effects'] = dict(historical_projection=records[owner]['effects'], sole_complete_fields=records[field]['effects'], parameter_edit_status='NOT_AVAILABLE')
    for owner in ('execute_primary_force_orders', 'select_primary_force_order_policy'):
        records[owner]['effects']['sole_current_battle_order_dispatch'] = {name: records[name]['effects'] for name in ('_battle_order_child_fields', '_battle_order_call_fields')}
    return lower_declared(records, BUSINESS_GAMEPLAY_BINDINGS, LOWERERS)


# The real same-state typed bridge bodies are part of complete admission.
DECLARATIONS.update({'_load_battle_policy_map': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'from .services import BattlePolicyMemory, load_battlefield_map_fields\nchecked_context(policy, BattlePolicy, state)\nsource = load_battlefield_map_fields(BattlePolicyMemory(state))\nstate.sr = state.sr & 65520 | (8 if policy.distance & 2147483648 else 0) | (4 if policy.distance == 0 else 0)\nreturn replace(policy, roster=source.cursor())'}, '_read_battle_policy_anchor': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'from .services import BattlePolicyMemory, AnchorContext, read_city_deployment_anchor_fields\nchecked_context(policy, BattlePolicy, state)\nfields = read_city_deployment_anchor_fields(BattlePolicyMemory(state), AnchorContext(policy.target_x, policy.target_y), policy.unit)\nfields.validate_complete(state)\nstate.sr = state.sr & 65504 | (16 if fields.extend else 0) | (8 if fields.negative else 0) | (4 if fields.zero else 0)\nreturn replace(policy, target_x=fields.x, target_y=fields.y, unit=fields.index, scan=fields.cells.cursor())'}})
APPROVED['services'].update({'BattlePolicyMemory', 'AnchorContext', 'load_battlefield_map_fields', 'read_city_deployment_anchor_fields'})


# Complete current-policy bridges; ordinary native lowerers are unchanged.
DECLARATIONS.update({'_enter_battle_policy_call': {'signature': 'state: SceneState, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\nuint(continuation, 32)\nif policy.stack_cursor is None:\n    raise Boundary('complete battle-policy call requires actual current A7')\nstack = policy.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nreturn replace(policy, stack_cursor=stack)"}, '_leave_battle_policy_call': {'signature': 'state: SceneState, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\nuint(continuation, 32)\nif policy.stack_cursor is None:\n    raise Boundary('complete battle-policy return requires current A7')\nactual = policy.stack_cursor.long()\nif actual != continuation:\n    raise Boundary('battle-policy return slot changed to actual target ' + str(actual))\nreturn replace(policy, stack_cursor=policy.stack_cursor.advance(4))"}, '_battle_policy_second_anchor': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'from .services import BattlePolicyMemory, AnchorContext, read_city_second_deployment_anchor_fields\nchecked_context(policy, BattlePolicy, state)\nfields = read_city_second_deployment_anchor_fields(BattlePolicyMemory(state), AnchorContext(policy.target_x, policy.target_y), policy.unit).validate_complete(state)\nstate.sr = state.sr & 65504 | (16 if fields.extend else 0) | (4 if fields.zero else 0) | (1 if fields.extend else 0)\nreturn replace(policy, target_x=fields.x, target_y=fields.y, unit=fields.index, scan=fields.cells.cursor())'}, '_battle_policy_occupied': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "from .services import BattlePolicyMemory, build_deployment_occupied_cell_fields\nchecked_context(policy, BattlePolicy, state)\nif policy.stack_cursor is None:\n    raise Boundary('complete occupied builder requires actual entry A7')\nfields = build_deployment_occupied_cell_fields(BattlePolicyMemory(state), policy.unit, policy.count, state.sr & 16 != 0, policy.stack_cursor).validate_complete(state)\nstate.sr = state.sr & 65504 | (16 if fields.extend else 0) | 8\nreturn replace(policy, unit=fields.member, count=fields.coordinate, candidates=fields.destination, controller=fields.source, scan=fields.positions.cursor(), stack_cursor=fields.stack_cursor)"}, '_battle_policy_empty_slot': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "from .services import BattlePolicyMemory, find_next_empty_position_slot_fields\nchecked_context(policy, BattlePolicy, state)\nif policy.scan is None or policy.candidates is None:\n    raise Boundary('actual A3 roster and A1 position views required')\nfields = find_next_empty_position_slot_fields(BattlePolicyMemory(state), policy.scan, policy.candidates, policy.offset_y, state.sr & 16 != 0).validate_complete(state)\nstate.set_status_word(state.sr & 65504 | (16 if fields.extend else 0) | (8 if fields.negative else 0) | (4 if fields.zero else 0) | (1 if fields.carry else 0))\nreturn replace(policy, offset_y=fields.index, scan=fields.source)"}, '_call_battle_policy_occupied': {'signature': 'state: SceneState, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'entered = _enter_battle_policy_call(state, policy, continuation)\nresult = _battle_policy_occupied(state, entered)\nreturn _leave_battle_policy_call(state, result, continuation)'}, '_call_battle_policy_empty_slot': {'signature': 'state: SceneState, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'entered = _enter_battle_policy_call(state, policy, continuation)\nresult = _battle_policy_empty_slot(state, entered)\nreturn _leave_battle_policy_call(state, result, continuation)'}, '_call_battle_policy_second_anchor': {'signature': 'state: SceneState, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'entered = _enter_battle_policy_call(state, policy, continuation)\nresult = _battle_policy_second_anchor(state, entered)\nreturn _leave_battle_policy_call(state, result, continuation)'}, '_call_battle_policy_external': {'signature': 'state: SceneState, target: Long, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'entered = _enter_battle_policy_call(state, policy, continuation)\nresult = _call(state, target, entered, continuation)\nreturn _leave_battle_policy_call(state, result, continuation)'}, '_battle_policy_edge_tail': {'signature': 'state: SceneState, target: Long, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "from .services import call_target\nchecked_context(policy, BattlePolicy, state)\nresult = call_target(state, target, policy)\nif type(result) is not BattlePolicy:\n    raise Boundary('complete edge tail requires actual full BattlePolicy return')\nreturn result.validate(state)"}, '_battle_policy_add_word': {'signature': 'state: SceneState, left: Word, right: Word', 'returns': 'Word', 'flow': 'uint(left, 16)\nuint(right, 16)\nwide = left + right\nresult = u16(wide)\noverflow = ~(left ^ right) & (left ^ result) & 32768 != 0\nstate.sr = state.sr & 65504 | (17 if wide > 65535 else 0) | (8 if result & 32768 else 0) | (4 if result == 0 else 0) | (2 if overflow else 0)\nreturn result'}, '_battle_policy_edge_conditions': {'signature': 'state: SceneState, value: Word, maximum: Word', 'returns': 'bool', 'flow': 'from .services import deployment_edge_coordinate_allowed\nuint(value, 16)\nuint(maximum, 16)\nif deployment_edge_coordinate_allowed(value, maximum):\n    return False\nbound = 3 if value < 3 else maximum\nresult = u16(value - bound)\noverflow = (value ^ bound) & (value ^ result) & 32768 != 0\nstate.set_status_word(state.sr & 65520 | (8 if result & 32768 else 0) | (4 if result == 0 else 0) | (2 if overflow else 0))\nreturn True'}, 'initialize_battle_policy_targets': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\npolicy = _enter_battle_policy_call(state, policy, 154590)\npolicy = _load_battle_policy_map(state, policy)\npolicy = _leave_battle_policy_call(state, policy, 154590)\npolicy = _enter_battle_policy_call(state, policy, 154594)\npolicy = initialize_primary_policy_targets(state, policy)\npolicy = _leave_battle_policy_call(state, policy, 154594)\npolicy = _enter_battle_policy_call(state, policy, 154598)\npolicy = initialize_secondary_policy_targets(state, policy)\nreturn _leave_battle_policy_call(state, policy, 154598)'}, 'initialize_primary_policy_targets': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\npolicy = _enter_battle_policy_call(state, policy, 154604)\npolicy = _read_battle_policy_anchor(state, policy)\npolicy = _leave_battle_policy_call(state, policy, 154604)\npolicy = _call_battle_policy_occupied(state, policy, 154608)\npolicy = replace(policy, scan=_ram(state, 'a550').cursor(), choice=replace_word(policy.choice, 2))\npolicy = _enter_battle_policy_call(state, policy, 154620)\npolicy = collect_order_target_candidates(state, policy)\npolicy = _leave_battle_policy_call(state, policy, 154620)\nreturn _call_battle_policy_external(state, 155128, policy, 154624)"}, 'initialize_secondary_policy_targets': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\npolicy = _call_battle_policy_second_anchor(state, policy, 155380)\npolicy = _call_battle_policy_occupied(state, policy, 155384)\npolicy = replace(policy, scan=_ram(state, 'a5a4').cursor(), choice=replace_word(policy.choice, 4))\npolicy = _enter_battle_policy_call(state, policy, 155396)\npolicy = collect_order_target_candidates(state, policy)\npolicy = _leave_battle_policy_call(state, policy, 155396)\nreturn _call_battle_policy_external(state, 155432, policy, 155400)"}, 'collect_order_target_candidates': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\npolicy = replace(policy, candidates=_ram(state, 'a150').cursor())\npolicy = _call_battle_policy_empty_slot(state, policy, 154738)\nif state.read_status_word() & 1:\n    return policy\nwhile True:\n    policy = _call_battle_policy_external(state, 154808, policy, 154746)\n    if state.read_status_word() & 1:\n        return policy\n    policy = _call_battle_policy_external(state, 155030, policy, 154754)\n    if state.read_status_word() & 1:\n        return policy\n    policy = _enter_battle_policy_call(state, policy, 154762)\n    policy = offset_first_order_target_axis(state, policy)\n    policy = _leave_battle_policy_call(state, policy, 154762)\n    if state.read_status_word() & 1:\n        return policy\n    policy = _enter_battle_policy_call(state, policy, 154770)\n    policy = offset_second_order_target_axis(state, policy)\n    policy = _leave_battle_policy_call(state, policy, 154770)\n    if state.read_status_word() & 1:\n        return policy\n    policy = replace(policy, choice=replace_word(policy.choice, _battle_policy_add_word(state, low16(policy.choice), 2)))"}, 'offset_first_order_target_axis': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\nunit = replace_word(policy.unit, _battle_policy_add_word(state, low16(policy.choice), low16(policy.target_x)))\npolicy = replace(policy, unit=unit)\nif _battle_policy_edge_conditions(state, low16(unit), 25):\n    return policy\nreturn _battle_policy_edge_tail(state, 154814, policy)'}, 'offset_second_order_target_axis': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\ncount = replace_word(policy.count, _battle_policy_add_word(state, low16(policy.choice), low16(policy.target_y)))\npolicy = replace(policy, count=count)\nif _battle_policy_edge_conditions(state, low16(count), 37):\n    return policy\nreturn _battle_policy_edge_tail(state, 155036, policy)'}})
APPROVED['services'].update({'read_city_second_deployment_anchor_fields', 'build_deployment_occupied_cell_fields', 'find_next_empty_position_slot_fields', 'deployment_edge_coordinate_allowed'})
DEPLOYMENT_FIELD_OWNERS = ('initialize_battle_policy_targets', 'initialize_primary_policy_targets', 'initialize_secondary_policy_targets', 'collect_order_target_candidates', 'offset_first_order_target_axis', 'offset_second_order_target_axis')
DEPLOYMENT_BRIDGE_HELPERS = ('_enter_battle_policy_call', '_leave_battle_policy_call', '_battle_policy_second_anchor', '_battle_policy_occupied', '_battle_policy_empty_slot', '_call_battle_policy_occupied', '_call_battle_policy_empty_slot', '_call_battle_policy_second_anchor', '_call_battle_policy_external', '_battle_policy_edge_tail', '_battle_policy_add_word', '_battle_policy_edge_conditions')


# Complete edges, original BRA aliases and both distinct promotion kernels.
DECLARATIONS.update({'_battle_policy_retained_frame': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': None, 'flow': 'from .services import FirstDeploymentFrame\nchecked_context(policy, BattlePolicy, state)\nframe = FirstDeploymentFrame(target_x=policy.target_x, target_y=policy.target_y, unit=policy.unit, count=policy.count, distance=policy.distance, offset_x=policy.offset_x, offset_y=policy.offset_y, choice=policy.choice, roster=policy.roster, candidates=policy.candidates, controller=policy.controller, scan=policy.scan, opponent=policy.opponent, scratch=policy.scratch, auxiliary=policy.auxiliary, stack_cursor=policy.stack_cursor, status=state.sr & 31)\nreturn frame.validate(state, complete=True)'}, '_battle_policy_retained_result': {'signature': 'state: SceneState, policy: BattlePolicy, frame', 'returns': 'BattlePolicy', 'flow': "from .services import FirstDeploymentFrame\nchecked_context(policy, BattlePolicy, state)\nif type(frame) is not FirstDeploymentFrame:\n    raise Boundary('complete deployment requires the sole actual retained frame')\nframe.validate(state, complete=True)\nstate.sr = state.sr & 65504 | frame.status\nreturn replace(policy, target_x=frame.target_x, target_y=frame.target_y, unit=frame.unit, count=frame.count, distance=frame.distance, offset_x=frame.offset_x, offset_y=frame.offset_y, choice=frame.choice, roster=frame.roster, candidates=frame.candidates, controller=frame.controller, scan=frame.scan, opponent=frame.opponent, scratch=frame.scratch, auxiliary=frame.auxiliary, stack_cursor=frame.stack_cursor).validate(state)"}, '_battle_policy_first_edge': {'signature': 'state: SceneState, policy: BattlePolicy, prefix: bool', 'returns': 'BattlePolicy', 'flow': 'from .services import BattlePolicyMemory, scan_deployment_first_edge_fields\nframe = _battle_policy_retained_frame(state, policy)\nresult = scan_deployment_first_edge_fields(BattlePolicyMemory(state), frame, low16(frame.target_x), low16(frame.target_y), low16(frame.choice), low16(frame.offset_y), prefix).validate(state)\nreturn _battle_policy_retained_result(state, policy, result.frame)'}, '_battle_policy_second_edge': {'signature': 'state: SceneState, policy: BattlePolicy, prefix: bool', 'returns': 'BattlePolicy', 'flow': 'from .services import BattlePolicyMemory, scan_deployment_second_edge_fields\nframe = _battle_policy_retained_frame(state, policy)\nresult = scan_deployment_second_edge_fields(BattlePolicyMemory(state), frame, low16(frame.target_x), low16(frame.target_y), low16(frame.choice), low16(frame.offset_y), prefix).validate(state)\nreturn _battle_policy_retained_result(state, policy, result.frame)'}, '_call_battle_policy_first_edge': {'signature': 'state: SceneState, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'entered = _enter_battle_policy_call(state, policy, continuation)\nreturned = _battle_policy_first_edge(state, entered, True)\nreturn _leave_battle_policy_call(state, returned, continuation)'}, '_call_battle_policy_second_edge': {'signature': 'state: SceneState, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'entered = _enter_battle_policy_call(state, policy, continuation)\nreturned = _battle_policy_second_edge(state, entered, True)\nreturn _leave_battle_policy_call(state, returned, continuation)'}, '_call_battle_policy_first_promotion': {'signature': 'state: SceneState, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'from .services import BattlePolicyMemory, promote_first_roster_deployment_candidate_fields\nentered = _enter_battle_policy_call(state, policy, continuation)\nframe = _battle_policy_retained_frame(state, entered)\nreturned = promote_first_roster_deployment_candidate_fields(BattlePolicyMemory(state), frame)\npolicy = _battle_policy_retained_result(state, entered, returned)\nreturn _leave_battle_policy_call(state, policy, continuation)'}, '_call_battle_policy_second_promotion': {'signature': 'state: SceneState, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'from .services import BattlePolicyMemory, promote_second_roster_deployment_candidate_fields\nentered = _enter_battle_policy_call(state, policy, continuation)\nframe = _battle_policy_retained_frame(state, entered)\nreturned = promote_second_roster_deployment_candidate_fields(BattlePolicyMemory(state), frame)\npolicy = _battle_policy_retained_result(state, entered, returned)\nreturn _leave_battle_policy_call(state, policy, continuation)'}, '_battle_policy_edge_tail': {'signature': 'state: SceneState, target: Long, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\nif target == 154814:\n    return _battle_policy_first_edge(state, policy, False)\nif target == 155036:\n    return _battle_policy_second_edge(state, policy, False)\nraise Boundary('unknown original deployment tail target ' + str(target))"}, 'collect_order_target_candidates': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\npolicy = replace(policy, candidates=_ram(state, 'a150').cursor())\npolicy = _call_battle_policy_empty_slot(state, policy, 154738)\nif state.read_status_word() & 1:\n    return policy\nwhile True:\n    policy = _call_battle_policy_first_edge(state, policy, 154746)\n    if state.read_status_word() & 1:\n        return policy\n    policy = _call_battle_policy_second_edge(state, policy, 154754)\n    if state.read_status_word() & 1:\n        return policy\n    policy = _enter_battle_policy_call(state, policy, 154762)\n    policy = offset_first_order_target_axis(state, policy)\n    policy = _leave_battle_policy_call(state, policy, 154762)\n    if state.read_status_word() & 1:\n        return policy\n    policy = _enter_battle_policy_call(state, policy, 154770)\n    policy = offset_second_order_target_axis(state, policy)\n    policy = _leave_battle_policy_call(state, policy, 154770)\n    if state.read_status_word() & 1:\n        return policy\n    policy = replace(policy, choice=replace_word(policy.choice, _battle_policy_add_word(state, low16(policy.choice), 2)))"}, 'initialize_primary_policy_targets': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\npolicy = _enter_battle_policy_call(state, policy, 154604)\npolicy = _read_battle_policy_anchor(state, policy)\npolicy = _leave_battle_policy_call(state, policy, 154604)\npolicy = _call_battle_policy_occupied(state, policy, 154608)\npolicy = replace(policy, scan=_ram(state, 'a550').cursor(), choice=replace_word(policy.choice, 2))\npolicy = _enter_battle_policy_call(state, policy, 154620)\npolicy = collect_order_target_candidates(state, policy)\npolicy = _leave_battle_policy_call(state, policy, 154620)\nreturn _call_battle_policy_first_promotion(state, policy, 154624)"}, 'initialize_secondary_policy_targets': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\npolicy = _call_battle_policy_second_anchor(state, policy, 155380)\npolicy = _call_battle_policy_occupied(state, policy, 155384)\npolicy = replace(policy, scan=_ram(state, 'a5a4').cursor(), choice=replace_word(policy.choice, 4))\npolicy = _enter_battle_policy_call(state, policy, 155396)\npolicy = collect_order_target_candidates(state, policy)\npolicy = _leave_battle_policy_call(state, policy, 155396)\nreturn _call_battle_policy_second_promotion(state, policy, 155400)"}})
APPROVED['services'].update({'promote_first_roster_deployment_candidate_fields', 'scan_deployment_first_edge_fields', 'scan_deployment_second_edge_fields', 'promote_second_roster_deployment_candidate_fields', 'FirstDeploymentFrame'})
DEPLOYMENT_BRIDGE_HELPERS += ('_battle_policy_retained_frame', '_battle_policy_retained_result', '_battle_policy_first_edge', '_battle_policy_second_edge', '_call_battle_policy_first_edge', '_call_battle_policy_second_edge', '_call_battle_policy_first_promotion', '_call_battle_policy_second_promotion')

DECLARATIONS.update({'_initialize_first_side_policy': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "from .services import BattlePolicyMemory, FirstDeploymentFrame, initialize_first_side_deployment_fields\nchecked_context(policy, BattlePolicy, state)\nif policy.stack_cursor is None:\n    raise Boundary('first-side deployment requires actual callee-entry A7')\nframe = FirstDeploymentFrame(target_x=policy.target_x, target_y=policy.target_y, unit=policy.unit, count=policy.count, distance=policy.distance, offset_x=policy.offset_x, offset_y=policy.offset_y, choice=policy.choice, roster=policy.roster, candidates=policy.candidates, controller=policy.controller, scan=policy.scan, opponent=policy.opponent, scratch=policy.scratch, auxiliary=policy.auxiliary, stack_cursor=policy.stack_cursor, status=state.sr & 31)\nframe.validate(state, True)\nreturned = initialize_first_side_deployment_fields(BattlePolicyMemory(state), frame)\nreturned.validate(state, True)\nstate.sr = state.sr & 65504 | returned.status\nreturn replace(policy, target_x=returned.target_x, target_y=returned.target_y, unit=returned.unit, count=returned.count, distance=returned.distance, offset_x=returned.offset_x, offset_y=returned.offset_y, choice=returned.choice, roster=returned.roster, candidates=returned.candidates, controller=returned.controller, scan=returned.scan, opponent=returned.opponent, scratch=returned.scratch, auxiliary=returned.auxiliary, stack_cursor=returned.stack_cursor)"}})
APPROVED['services'].update({'FirstDeploymentFrame', 'initialize_first_side_deployment_fields'})
DEPLOYMENT_FIELD_OWNERS += ('execute_primary_force_orders', 'select_primary_force_order_policy')
DEPLOYMENT_BRIDGE_HELPERS += ('_initialize_first_side_policy',)


# Actual 23562 direct assignment call, distinct from the 24AD0 dispatcher.
DECLARATIONS.update({'_prepare_first_side_assignment_policy': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'from .services import BattlePolicyMemory, prepare_first_side_assignment_fields\nframe = _battle_policy_retained_frame(state, policy)\nreturned = prepare_first_side_assignment_fields(BattlePolicyMemory(state), frame)\nreturn _battle_policy_retained_result(state, policy, returned)'}})
APPROVED['services'].add('prepare_first_side_assignment_fields')
DEPLOYMENT_BRIDGE_HELPERS += ('_prepare_first_side_assignment_policy',)

# Actual23572/23576 full leader-roster call and return.
DECLARATIONS.update({'_call_battle_policy_leader_presence': {'signature': 'state: SceneState, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'from .services import BattlePolicyMemory, test_battlefield_leader_roster_presence_fields\nentered = _enter_battle_policy_call(state, policy, continuation)\nframe = _battle_policy_retained_frame(state, entered)\nfields = test_battlefield_leader_roster_presence_fields(BattlePolicyMemory(state), frame).validate(state)\nreturned = _battle_policy_retained_result(state, entered, fields.frame)\nreturn _leave_battle_policy_call(state, returned, continuation)'}, 'execute_primary_force_orders': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\npolicy = _enter_battle_policy_call(state, policy, 144742)\npolicy = _prepare_first_side_assignment_policy(state, policy)\npolicy = _leave_battle_policy_call(state, policy, 144742)\nbudget = calculate_force_supply_budgets(state, policy)\npolicy = replace(budget, controller=state.table_at(budget.scan.base), scan=policy.scan)\nroster, orders = (_ram(state, 'a550').cursor(), _ram(state, 'af82').cursor())\nwhile True:\n    policy = _call_battle_policy_leader_presence(state, replace(policy, roster=roster, candidates=orders), 144758)\n    roster, orders = (policy.roster, policy.candidates)\n    if state.read_status_word() & 1 or _word(state, 'f612') == 1041:\n        break\n    choice = replace_word(policy.choice, roster.next_word())\n    policy = replace(policy, choice=choice)\n    if negative_word(low16(choice)):\n        break\n    x = replace_word(policy.target_x, orders.next_word())\n    policy = replace(policy, target_x=x)\n    if low16(x) == 255:\n        continue\n    _put(state, 'f770', x)\n    x = replace_word(x, _order_shift_left(state, low16(x), 1, 16))\n    policy = _execute_primary_indexed_order(state, replace(policy, target_x=x))\n    roster, orders = (policy.roster, policy.candidates)\n_word(state, 'f362')\n_put(state, 'f362', 0)\nstate.sr = state.sr & 65520 | 4\nreturn policy"}})
APPROVED['services'].add('test_battlefield_leader_roster_presence_fields')
DEPLOYMENT_BRIDGE_HELPERS += ('_call_battle_policy_leader_presence',)


# Actual complete primary indexed policy body admission.
DECLARATIONS.update({'_order_move_flags': {'signature': 'state: SceneState, value: Long, bits: Word', 'returns': 'Long', 'flow': 'uint(value, bits)\nstate.sr = state.sr & 65520 | (8 if value & 1 << bits - 1 else 0) | (4 if value == 0 else 0)\nreturn value'}, '_order_compare_flags': {'signature': 'state: SceneState, left: Long, right: Long, bits: Word', 'returns': 'None', 'flow': 'uint(left, bits)\nuint(right, bits)\nmask = (1 << bits) - 1\nsign = 1 << bits - 1\ndifference = left - right & mask\noverflow = bool((left ^ right) & (left ^ difference) & sign)\nstate.sr = state.sr & 65520 | (1 if left < right else 0) | (2 if overflow else 0) | (8 if difference & sign else 0) | (4 if difference == 0 else 0)'}, '_order_shift_left': {'signature': 'state: SceneState, value: Long, count: Word, bits: Word', 'returns': 'Long', 'flow': "uint(value, bits)\nuint(count, 16)\nif not 1 <= count <= 8:\n    raise ValueError('actual bounded immediate shift required')\nshifted = value << count & (1 << bits) - 1\ncarried = bool(value & 1 << bits - count)\nstate.sr = state.sr & 65504 | (17 if carried else 0) | (8 if shifted & 1 << bits - 1 else 0) | (4 if shifted == 0 else 0)\nreturn shifted"}, '_order_shift_right': {'signature': 'state: SceneState, value: Word, count: Word', 'returns': 'Word', 'flow': "uint(value, 16)\nuint(count, 16)\nif not 1 <= count <= 8:\n    raise ValueError('actual bounded immediate shift required')\nshifted = value >> count\ncarried = bool(value & 1 << count - 1)\nstate.sr = state.sr & 65504 | (17 if carried else 0) | (4 if shifted == 0 else 0)\nreturn shifted"}, '_order_full_sr_carry': {'signature': 'state: SceneState, value: bool', 'returns': 'None', 'flow': "if type(value) is not bool:\n    raise ValueError('actual full-SR carry decision required')\nif not state.sr & 8192:\n    raise Boundary('original order full-SR operation requires supervisor')\nif state.sr & 32768:\n    raise Boundary('original order full-SR trace continuation unmodeled')\nstate.set_status_word(state.sr & 65534 | int(value))"}, '_order_force_has_city_assignment': {'signature': 'state: SceneState, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'from .services import BattlePolicyMemory, test_force_has_city_assignment_fields\nentered = _enter_battle_policy_call(state, policy, continuation)\nframe, _ = test_force_has_city_assignment_fields(BattlePolicyMemory(state), _battle_policy_retained_frame(state, entered))\nreturned = _battle_policy_retained_result(state, entered, frame)\nreturn _leave_battle_policy_call(state, returned, continuation)'}, '_order_sum_first_side_troops': {'signature': 'state: SceneState, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'from .services import BattlePolicyMemory, sum_first_side_roster_troops_fields\nentered = _enter_battle_policy_call(state, policy, continuation)\nframe, _, _ = sum_first_side_roster_troops_fields(BattlePolicyMemory(state), _battle_policy_retained_frame(state, entered))\nreturned = _battle_policy_retained_result(state, entered, frame)\nreturn _leave_battle_policy_call(state, returned, continuation)'}, '_order_scaled_random': {'signature': 'state: SceneState, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'from .services import sample_random_pair\nentered = _enter_battle_policy_call(state, policy, continuation)\nrandom = sample_random_pair(state)\nstate.sr = state.sr & 65519 | (16 if low16(random.sample) < low16(random.updated_state) else 0)\n_order_move_flags(state, random.updated_state, 32)\nreturned = replace(entered, target_x=random.sample, target_y=random.updated_state)\nreturned = _leave_battle_policy_call(state, returned, continuation)\nsample = _order_move_flags(state, random.sample & 65535, 32)\nsample = _order_shift_left(state, sample, 3, 32)\nsample = _order_move_flags(state, swap_words(sample), 32)\nreturn replace(returned, target_x=sample)'}, 'evaluate_primary_force_retreat_order': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\npolicy = replace(policy, roster=_ram(state, 'c800').cursor())\noffset = _order_move_flags(state, low16(policy.choice), 16)\noffset = _order_shift_left(state, offset, 2, 16)\ntroops = _order_move_flags(state, policy.roster.long(offset), 32)\npolicy = replace(policy, target_x=replace_word(policy.target_x, offset), target_y=troops)\n_order_compare_flags(state, troops, 200, 32)\nuse_small_force_gate = troops <= 200\nif not use_small_force_gate:\n    _order_compare_flags(state, troops, 500, 32)\n    if troops <= 500:\n        policy = replace(policy, roster=_ram(state, 'b000').cursor())\n        offset = _order_shift_right(state, low16(policy.target_x), 1)\n        skill = _order_move_flags(state, policy.roster.word(offset), 16)\n        skill = _order_shift_right(state, skill, 2)\n        policy = replace(policy, target_x=replace_word(policy.target_x, offset), target_y=replace_word(policy.target_y, skill), roster=_ram(state, 'b200').cursor())\n        aptitude = policy.roster.word(offset)\n        _order_compare_flags(state, skill, aptitude, 16)\n        use_small_force_gate = skill >= aptitude\nif use_small_force_gate:\n    gate = _order_move_flags(state, 2, 16)\n    force = _order_move_flags(state, _word(state, 'f68c'), 16)\n    offset = _order_shift_left(state, force, 1, 16)\n    policy = replace(policy, unit=replace_word(policy.unit, gate), target_x=replace_word(policy.target_x, offset), roster=_ram(state, 'e640').cursor())\n    ruler = policy.roster.word(offset)\n    _order_compare_flags(state, low16(policy.choice), ruler, 16)\n    if low16(policy.choice) == ruler:\n        policy = replace(policy, unit=replace_word(policy.unit, _order_move_flags(state, 4, 16)))\n        policy = _order_force_has_city_assignment(state, policy, 145668)\n        if not state.sr & 1:\n            _order_full_sr_carry(state, False)\n            return policy\n    policy = _order_scaled_random(state, policy, 145682)\n    _order_compare_flags(state, low16(policy.target_x), low16(policy.unit), 16)\n    if low16(policy.target_x) < low16(policy.unit):\n        return _execute_primary_retreat_modal(state, policy)\npolicy = _order_count_opposing_roster(state, policy, 145702)\n_order_compare_flags(state, low16(policy.target_x), 3, 16)\nuse_default_comparison = low16(policy.target_x) < 3\nif not use_default_comparison:\n    reserve = _order_move_flags(state, _ram(state, 'f69e').long(), 32)\n    use_default_comparison = reserve != 0\nif not use_default_comparison:\n    limit = _order_move_flags(state, _ram(state, 'f76c').long(), 32)\n    limit = divu_retained(limit, 6)\n    limit = _order_move_flags(state, limit & 65535, 32)\n    policy = replace(policy, unit=limit)\n    other = _ram(state, 'f6a2').long()\n    _order_compare_flags(state, limit, other, 32)\n    use_default_comparison = limit > other\nif use_default_comparison:\n    policy = _order_sum_first_side_troops(state, policy, 145744)\n    _order_compare_flags(state, low16(policy.unit), low16(policy.target_x), 16)\n    if low16(policy.unit) > low16(policy.target_x):\n        _order_full_sr_carry(state, False)\n        return policy\n    doubled = _order_shift_left(state, policy.count, 1, 32)\n    policy = replace(policy, count=doubled)\n    _order_compare_flags(state, doubled, policy.target_y, 32)\n    if doubled > policy.target_y:\n        _order_full_sr_carry(state, False)\n        return policy\n    strength = _order_move_flags(state, _ram(state, 'f76c').long(), 32)\n    policy = replace(policy, target_x=strength)\n    other = _ram(state, 'f6a2').long()\n    _order_compare_flags(state, strength, other, 32)\n    if strength < other:\n        _order_full_sr_carry(state, False)\n        return policy\npolicy = replace(policy, unit=replace_word(policy.unit, _order_move_flags(state, 2, 16)))\npolicy = _order_force_has_city_assignment(state, policy, 145778)\nif not state.sr & 1:\n    _order_full_sr_carry(state, False)\n    return policy\npolicy = _order_scaled_random(state, policy, 145792)\n_order_compare_flags(state, low16(policy.target_x), low16(policy.unit), 16)\nif low16(policy.target_x) < low16(policy.unit):\n    return _execute_primary_retreat_modal(state, policy)\n_order_full_sr_carry(state, False)\nreturn policy"}, '_execute_primary_retreat_modal': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "_put(state, 'f3a6', _order_move_flags(state, low16(policy.choice), 16))\nif policy.stack_cursor is None:\n    raise Boundary('primary retreat modal requires actual current A7')\nstack = policy.stack_cursor.advance(-2)\nstack.set_word(0, low16(policy.choice))\n_order_move_flags(state, low16(policy.choice), 16)\npolicy = _call_battle_policy_external(state, 97418, replace(policy, stack_cursor=stack), 145828)\nrestored = policy.stack_cursor.word()\npolicy = replace(policy, choice=replace_word(policy.choice, _order_move_flags(state, restored, 16)), stack_cursor=policy.stack_cursor.advance(2))\ntested = _order_move_flags(state, _word(state, 'f6e8'), 16)\nif negative_word(tested):\n    _order_full_sr_carry(state, False)\n    return policy\npolicy = _call_battle_policy_external(state, 98096, policy, 145842)\n_put(state, 'f3d2', _order_move_flags(state, _word(state, 'f3a6'), 16))\n_put(state, 'f740', _order_move_flags(state, 302, 16))\nvalue = _ram(state, 'f6d7').byte()\nstate.sr = state.sr & 65531 | (0 if value & 2 else 4)\n_ram(state, 'f6d7').set_byte(0, value ^ 2)\npolicy = _call_battle_policy_external(state, 155876, policy, 145866)\nvalue = _ram(state, 'f6d7').byte()\nstate.sr = state.sr & 65531 | (0 if value & 2 else 4)\n_ram(state, 'f6d7').set_byte(0, value ^ 2)\n_order_full_sr_carry(state, True)\nreturn policy"}, '_primary_order_tail': {'signature': 'state: SceneState, target: Long, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "if target == 146038:\n    return _primary_short_roster_tail(state, policy)\nif target == 148214:\n    return _primary_small_force_tail(state, policy)\nfrom .services import call_target\nreturned = call_target(state, target, policy)\nif type(returned) is not BattlePolicy:\n    raise Boundary('primary order tail requires actual BattlePolicy return')\nreturn returned.validate(state)"}, 'execute_primary_standard_order': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\npolicy = _enter_battle_policy_call(state, policy, 144916)\npolicy = evaluate_primary_force_retreat_order(state, policy)\npolicy = _leave_battle_policy_call(state, policy, 144916)\nif state.sr & 1:\n    return policy\npolicy = _primary_single_roster_gate(state, policy)\nif state.sr & 1:\n    return _primary_order_tail(state, 146038, policy)\npolicy = _primary_small_roster_gate(state, policy)\nif state.sr & 1:\n    return _primary_order_tail(state, 148214, policy)\npolicy = _call_battle_policy_external(state, 145206, policy, 144940)\nif state.sr & 1:\n    return policy\npolicy = _call_battle_policy_external(state, 144958, policy, 144948)\nif state.sr & 1:\n    return policy\nreturn _call_battle_policy_external(state, 145124, policy, 144956)'}, '_execute_primary_indexed_order': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\ndisplacement = data_view(state, 'data_0235b6').word(low16(policy.target_x))\n_order_move_flags(state, displacement, 16)\npolicy = replace(policy, target_x=replace_word(policy.target_x, displacement))\nif policy.stack_cursor is None or policy.roster is None or policy.candidates is None:\n    raise Boundary('primary indexed order requires actual A0/A1/A7')\nstack = policy.stack_cursor.advance(-4)\nstack.set_long(0, policy.candidates.base)\nstack = stack.advance(-4)\nstack.set_long(0, policy.roster.base)\npolicy = replace(policy, stack_cursor=stack, roster=state.table_at(144912).cursor())\ntarget = u32(144912 + s16(displacement))\nentered = _enter_battle_policy_call(state, policy, 144810)\nif target == 144912:\n    returned = execute_primary_standard_order(state, entered)\nelse:\n    returned = _call(state, target, entered, 144810)\nreturned = _leave_battle_policy_call(state, returned, 144810)\nstack = returned.stack_cursor\nroster = state.table_at(stack.long()).cursor()\nstack = stack.advance(4)\norders = state.table_at(stack.long()).cursor()\nreturn replace(returned, roster=roster, candidates=orders, stack_cursor=stack.advance(4))"}})
APPROVED['services'].update({'sum_first_side_roster_troops_fields', 'test_force_has_city_assignment_fields'})
PRIMARY_ORDER_HELPERS = ('_order_move_flags', '_order_compare_flags', '_order_shift_left', '_order_shift_right', '_order_full_sr_carry', '_order_force_has_city_assignment', '_order_sum_first_side_troops', '_order_scaled_random', 'evaluate_primary_force_retreat_order', '_execute_primary_retreat_modal', '_primary_order_tail', 'execute_primary_standard_order', '_execute_primary_indexed_order')


# Genuine strength-gate adapters, complete DECL and child effects.
DECLARATIONS.update({'_primary_single_roster_gate': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'from .services import BattlePolicyMemory, test_second_side_total_with_single_first_roster_fields\nentered = _enter_battle_policy_call(state, policy, 144924)\nframe, _ = test_second_side_total_with_single_first_roster_fields(BattlePolicyMemory(state), _battle_policy_retained_frame(state, entered))\nreturned = _battle_policy_retained_result(state, entered, frame)\nreturn _leave_battle_policy_call(state, returned, 144924)'}, '_primary_small_roster_gate': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'from .services import BattlePolicyMemory, test_second_side_total_with_small_second_roster_fields\nentered = _enter_battle_policy_call(state, policy, 144932)\nframe, _ = test_second_side_total_with_small_second_roster_fields(BattlePolicyMemory(state), _battle_policy_retained_frame(state, entered))\nreturned = _battle_policy_retained_result(state, entered, frame)\nreturn _leave_battle_policy_call(state, returned, 144932)'}})
APPROVED['services'].update({'test_second_side_total_with_single_first_roster_fields', 'test_second_side_total_with_small_second_roster_fields'})
PRIMARY_ORDER_HELPERS += ('_primary_single_roster_gate', '_primary_small_roster_gate')

DECLARATIONS.update({'_order_count_opposing_roster': {'signature': 'state: SceneState, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'from .services import count_opposing_battle_roster_fields\nentered = _enter_battle_policy_call(state, policy, continuation)\nframe = _battle_policy_retained_frame(state, entered)\nreturned = count_opposing_battle_roster_fields(state, frame)\nresult = _battle_policy_retained_result(state, entered, returned)\nreturn _leave_battle_policy_call(state, result, continuation)'}})
APPROVED['services'].add('count_opposing_battle_roster_fields')
DEPLOYMENT_BRIDGE_HELPERS += ('_order_count_opposing_roster',)

DECLARATIONS.update({'execute_primary_standard_order': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\npolicy = _enter_battle_policy_call(state, policy, 144916)\npolicy = evaluate_primary_force_retreat_order(state, policy)\npolicy = _leave_battle_policy_call(state, policy, 144916)\nif state.sr & 1:\n    return policy\npolicy = _primary_single_roster_gate(state, policy)\nif state.sr & 1:\n    return _primary_order_tail(state, 146038, policy)\npolicy = _primary_small_roster_gate(state, policy)\nif state.sr & 1:\n    return _primary_order_tail(state, 148214, policy)\npolicy = _call_battle_policy_external(state, 145206, policy, 144940)\nif state.sr & 1:\n    return policy\npolicy = _call_battle_policy_external(state, 144958, policy, 144948)\nif state.sr & 1:\n    return policy\nreturn _primary_secondary_standard_action(state, policy)'}})
DECLARATIONS.update({'_primary_secondary_standard_action': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'from .services import evaluate_secondary_standard_action_fields\nentered = _enter_battle_policy_call(state, policy, 144956)\nframe = _battle_policy_retained_frame(state, entered)\nresult = evaluate_secondary_standard_action_fields(state, frame, True)\nreturned = _battle_policy_retained_result(state, entered, result)\nreturn _leave_battle_policy_call(state, returned, 144956)'}})
APPROVED['services'].add('evaluate_secondary_standard_action_fields')
DEPLOYMENT_BRIDGE_HELPERS += ('_primary_secondary_standard_action',)

DECLARATIONS.update({'execute_primary_standard_order': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\npolicy = _enter_battle_policy_call(state, policy, 144916)\npolicy = evaluate_primary_force_retreat_order(state, policy)\npolicy = _leave_battle_policy_call(state, policy, 144916)\nif state.sr & 1:\n    return policy\npolicy = _primary_single_roster_gate(state, policy)\nif state.sr & 1:\n    return _primary_order_tail(state, 146038, policy)\npolicy = _primary_small_roster_gate(state, policy)\nif state.sr & 1:\n    return _primary_order_tail(state, 148214, policy)\npolicy = _primary_city_rectangle_call(state, policy, 144940)\nif state.sr & 1:\n    return policy\npolicy = _primary_standard_position_action(state, policy)\nif state.sr & 1:\n    return policy\nreturn _primary_secondary_standard_action(state, policy)'}})

DECLARATIONS.update({'_primary_standard_position_action': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'from .services import evaluate_standard_position_order_fields\nentered = _enter_battle_policy_call(state, policy, 144948)\nframe = _battle_policy_retained_frame(state, entered)\nfields = evaluate_standard_position_order_fields(state, frame, True).validate(state, True)\nreturned = _battle_policy_retained_result(state, entered, fields.frame)\nreturn _leave_battle_policy_call(state, returned, 144948)'}})
APPROVED['services'].add('evaluate_standard_position_order_fields')
DEPLOYMENT_BRIDGE_HELPERS += ('_primary_standard_position_action',)


# Full trigger/short-tail field and call effects, ordinary emission unchanged.
DECLARATIONS.update({'_primary_city_rectangle_call': {'signature': 'state: SceneState, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'from .services import BattleTriggerMemory, BattleTriggerFrame, trigger_battle_for_city_rectangle_fields\nentered = _enter_battle_policy_call(state, policy, continuation)\nframe = BattleTriggerFrame(target_x=entered.target_x, target_y=entered.target_y, unit=entered.unit, count=entered.count, distance=entered.distance, offset_x=entered.offset_x, offset_y=entered.offset_y, choice=entered.choice, roster=entered.roster, candidates=entered.candidates, controller=entered.controller, scan=entered.scan, opponent=entered.opponent, scratch=entered.scratch, auxiliary=entered.auxiliary, stack_cursor=entered.stack_cursor, status=state.sr, legacy_context=None)\nreturned = trigger_battle_for_city_rectangle_fields(BattleTriggerMemory(state), frame, low16(frame.choice)).validate_complete(state)\nstate.sr = returned.status\npolicy = replace(entered, target_x=returned.target_x, target_y=returned.target_y, unit=returned.unit, count=returned.count, distance=returned.distance, offset_x=returned.offset_x, offset_y=returned.offset_y, choice=returned.choice, roster=returned.roster, candidates=returned.candidates, controller=returned.controller, scan=returned.scan, opponent=returned.opponent, scratch=returned.scratch, auxiliary=returned.auxiliary, stack_cursor=returned.stack_cursor)\nreturn _leave_battle_policy_call(state, policy, continuation)'}, '_primary_short_roster_tail': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\npolicy = _primary_city_rectangle_call(state, policy, 146042)\nif state.sr & 1:\n    return policy\npolicy = _call_battle_policy_external(state, 141142, policy, 146050)\nif state.sr & 1:\n    return policy\npolicy = _call_battle_policy_external(state, 146494, policy, 146058)\nif state.sr & 1:\n    return policy\nreturn _call_battle_policy_external(state, 146068, policy, 146066)'}, '_primary_small_force_tail': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\npolicy = _primary_city_rectangle_call(state, policy, 148218)\nif state.sr & 1:\n    return policy\npolicy = _call_battle_policy_external(state, 141142, policy, 148226)\nif state.sr & 1:\n    return policy\npolicy = _call_battle_policy_external(state, 142640, policy, 148234)\nif state.sr & 1:\n    return policy\nreturn _call_battle_policy_external(state, 148244, policy, 148242)'}})
APPROVED['services'].update({'BattleTriggerMemory', 'BattleTriggerFrame', 'trigger_battle_for_city_rectangle_fields'})
PRIMARY_ORDER_HELPERS += ('_primary_city_rectangle_call', '_primary_short_roster_tail', '_primary_small_force_tail')


# Current post-C10 complete execute_primary_standard_order body; no old dictionary replacement.
DECLARATIONS.update({'execute_primary_standard_order': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\npolicy = _enter_battle_policy_call(state, policy, 144916)\npolicy = evaluate_primary_force_retreat_order(state, policy)\npolicy = _leave_battle_policy_call(state, policy, 144916)\nif state.sr & 1:\n    return policy\npolicy = _primary_single_roster_gate(state, policy)\nif state.sr & 1:\n    return _primary_order_tail(state, 146038, policy)\npolicy = _primary_small_roster_gate(state, policy)\nif state.sr & 1:\n    return _primary_order_tail(state, 148214, policy)\npolicy = _primary_city_rectangle_call(state, policy, 144940)\nif state.sr & 1:\n    return policy\npolicy = _primary_standard_position_action(state, policy)\nif state.sr & 1:\n    return policy\nreturn _primary_secondary_standard_action(state, policy)'}})


# Current post-C10 complete _primary_order_tail body; no old dictionary replacement.
DECLARATIONS.update({'_primary_order_tail': {'signature': 'state: SceneState, target: Long, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "if target == 146038:\n    return _primary_short_roster_tail(state, policy)\nif target == 148214:\n    return _primary_small_force_tail(state, policy)\nfrom .services import call_target\nreturned = call_target(state, target, policy)\nif type(returned) is not BattlePolicy:\n    raise Boundary('primary order tail requires actual BattlePolicy return')\nreturn returned.validate(state)"}})


# Current complete _primary_short_roster_tail actual retreat bridge.
DECLARATIONS.update({'_primary_short_roster_tail': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\npolicy = _primary_city_rectangle_call(state, policy, 146042)\nif state.sr & 1:\n    return policy\npolicy = _primary_other_city_retreat_call(state, policy, 146050)\nif state.sr & 1:\n    return policy\npolicy = _call_battle_policy_external(state, 146494, policy, 146058)\nif state.sr & 1:\n    return policy\nreturn _call_battle_policy_external(state, 146068, policy, 146066)'}})


# Current complete _primary_small_force_tail actual retreat bridge.
DECLARATIONS.update({'_primary_small_force_tail': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\npolicy = _primary_city_rectangle_call(state, policy, 148218)\nif state.sr & 1:\n    return policy\npolicy = _primary_other_city_retreat_call(state, policy, 148226)\nif state.sr & 1:\n    return policy\npolicy = _call_battle_policy_external(state, 142640, policy, 148234)\nif state.sr & 1:\n    return policy\nreturn _call_battle_policy_external(state, 148244, policy, 148242)'}})


# Complete actual _primary_other_city_retreat_call admission.
DECLARATIONS.update({'_primary_other_city_retreat_call': {'signature': 'state: SceneState, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'from .services import evaluate_other_city_retreat_order_fields\nentered = _enter_battle_policy_call(state, policy, continuation)\nframe = _battle_policy_retained_frame(state, entered)\nreturned = evaluate_other_city_retreat_order_fields(state, frame, True)\npolicy = _battle_policy_retained_result(state, entered, returned)\nreturn _leave_battle_policy_call(state, policy, continuation)'}})
APPROVED['services'].add('evaluate_other_city_retreat_order_fields')
PRIMARY_ORDER_HELPERS += ('_primary_other_city_retreat_call',)

# Root: actual23A6E guarded alternate with the original indexed caller slot.
DECLARATIONS.update({"_execute_primary_indexed_order":{"signature":"state: SceneState, policy: BattlePolicy","returns":"BattlePolicy","flow":"checked_context(policy, BattlePolicy, state)\ndisplacement = data_view(state, 'data_0235b6').word(low16(policy.target_x))\n_order_move_flags(state, displacement, 16)\npolicy = replace(policy, target_x=replace_word(policy.target_x, displacement))\nif policy.stack_cursor is None or policy.roster is None or policy.candidates is None:\n    raise Boundary('primary indexed order requires actual A0/A1/A7')\nstack = policy.stack_cursor.advance(-4)\nstack.set_long(0, policy.candidates.base)\nstack = stack.advance(-4)\nstack.set_long(0, policy.roster.base)\npolicy = replace(policy, stack_cursor=stack, roster=state.table_at(144912).cursor())\ntarget = u32(144912 + s16(displacement))\nentered = _enter_battle_policy_call(state, policy, 144810)\nif target == 144912:\n    returned = execute_primary_standard_order(state, entered)\nelif target == 146030:\n    returned = _primary_guarded_short_roster_tail(state, entered)\nelse:\n    returned = _call(state, target, entered, 144810)\nreturned = _leave_battle_policy_call(state, returned, 144810)\nstack = returned.stack_cursor\nroster = state.table_at(stack.long()).cursor()\nstack = stack.advance(4)\norders = state.table_at(stack.long()).cursor()\nreturn replace(returned, roster=roster, candidates=orders, stack_cursor=stack.advance(4))"},"_primary_guarded_short_roster_tail":{"signature":"state: SceneState, policy: BattlePolicy","returns":"BattlePolicy","flow":"checked_context(policy, BattlePolicy, state)\nfrom .services import BattlePolicyMemory, test_second_side_relative_total_shortfall_fields\nentered = _enter_battle_policy_call(state, policy, 146034)\nframe, _ = test_second_side_relative_total_shortfall_fields(BattlePolicyMemory(state), _battle_policy_retained_frame(state, entered))\nreturned = _battle_policy_retained_result(state, entered, frame)\npolicy = _leave_battle_policy_call(state, returned, 146034)\nif state.sr & 1:\n    return _primary_order_tail(state, 149526, policy)\nreturn _primary_short_roster_tail(state, policy)"}})
PRIMARY_ORDER_HELPERS += ('_primary_guarded_short_roster_tail',)

# Root: real2430A retreat mark call, complete current frame and shared core.
DECLARATIONS.update({"_primary_small_force_tail":{"signature":"state: SceneState, policy: BattlePolicy","returns":"BattlePolicy","flow":"checked_context(policy, BattlePolicy, state)\npolicy = _primary_city_rectangle_call(state, policy, 148218)\nif state.sr & 1:\n    return policy\npolicy = _primary_other_city_retreat_call(state, policy, 148226)\nif state.sr & 1:\n    return policy\npolicy = _primary_retreat_mark_call(state, policy, 148234)\nif state.sr & 1:\n    return policy\nreturn _call_battle_policy_external(state, 148244, policy, 148242)"},"_primary_retreat_mark_call":{"signature":"state: SceneState, policy: BattlePolicy, continuation: Long","returns":"BattlePolicy","flow":"from .services import BattlePolicyMemory, mark_eligible_actor_for_retreat_fields\nentered = _enter_battle_policy_call(state, policy, continuation)\nframe, _ = mark_eligible_actor_for_retreat_fields(BattlePolicyMemory(state), _battle_policy_retained_frame(state, entered))\nreturned = _battle_policy_retained_result(state, entered, frame)\nreturn _leave_battle_policy_call(state, returned, continuation)"}})
PRIMARY_ORDER_HELPERS += ('_primary_retreat_mark_call',)

# Actual24816 tail: source-level shared policies, distinct real return slots.
DECLARATIONS.update({"_primary_order_tail":{"signature":"state: SceneState, target: Long, policy: BattlePolicy","returns":"BattlePolicy","flow":"if target == 146038:\n    return _primary_short_roster_tail(state, policy)\nif target == 148214:\n    return _primary_small_force_tail(state, policy)\nif target == 149526:\n    return _primary_low_strength_fallback_tail(state, policy)\nfrom .services import call_target\nreturned = call_target(state, target, policy)\nif type(returned) is not BattlePolicy:\n    raise Boundary('primary order tail requires actual BattlePolicy return')\nreturn returned.validate(state)"},"_primary_low_strength_fallback_tail":{"signature":"state: SceneState, policy: BattlePolicy","returns":"BattlePolicy","flow":"checked_context(policy, BattlePolicy, state)\npolicy = _primary_city_rectangle_call(state, policy, 149530)\nif state.sr & 1:\n    return policy\npolicy = _primary_other_city_retreat_call(state, policy, 149538)\nif state.sr & 1:\n    return policy\npolicy = _primary_retreat_mark_call(state, policy, 149546)\nif state.sr & 1:\n    return policy\nreturn _call_battle_policy_external(state, 149556, policy, 149554)"}})
PRIMARY_ORDER_HELPERS += ('_primary_low_strength_fallback_tail',)

# Current movement successor also serves the actual primary retreat caller.
DECLARATIONS.update({"_call_battle_policy_external":{"signature":"state: SceneState, target: Long, policy: BattlePolicy, continuation: Long","returns":"BattlePolicy","flow":"entered = _enter_battle_policy_call(state, policy, continuation)\nif target == 97418:\n    from .business_movement_support import ensure_neighbor_capacity_fields\n    frame = ensure_neighbor_capacity_fields(state, _battle_policy_retained_frame(state, entered))\n    result = _battle_policy_retained_result(state, entered, frame)\nelse:\n    result = _call(state, target, entered, continuation)\nreturn _leave_battle_policy_call(state, result, continuation)"}})
APPROVED['business_movement_support'] = {'ensure_neighbor_capacity_fields'}


# Current entire primary actual outer-slot movement successor bridge.
DECLARATIONS.update({'_call_battle_policy_external': {'signature': 'state: SceneState, target: Long, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'entered = _enter_battle_policy_call(state, policy, continuation)\nif target == 97418:\n    from .business_movement_support import ensure_neighbor_capacity_fields\n    frame = ensure_neighbor_capacity_fields(state, _battle_policy_retained_frame(state, entered))\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 98096:\n    from .business_movement_support import integrate_selected_officer_into_packed_group_fields\n    frame = integrate_selected_officer_into_packed_group_fields(state, _battle_policy_retained_frame(state, entered))\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 155876:\n    from .business_movement_support import present_battle_message_fields\n    frame = present_battle_message_fields(state, _battle_policy_retained_frame(state, entered))\n    result = _battle_policy_retained_result(state, entered, frame)\nelse:\n    result = _call(state, target, entered, continuation)\nreturn _leave_battle_policy_call(state, result, continuation)'}})
APPROVED.setdefault('business_movement_support', set()).update({'integrate_selected_officer_into_packed_group_fields', 'present_battle_message_fields'})

DECLARATIONS.update({'_call_battle_policy_external': {'signature': 'state: SceneState, target: Long, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'entered = _enter_battle_policy_call(state, policy, continuation)\nif target == 97418:\n    from .business_movement_support import ensure_neighbor_capacity_fields\n    frame = ensure_neighbor_capacity_fields(state, _battle_policy_retained_frame(state, entered))\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 98096:\n    from .business_movement_support import integrate_selected_officer_into_packed_group_fields\n    frame = integrate_selected_officer_into_packed_group_fields(state, _battle_policy_retained_frame(state, entered))\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 155876:\n    from .business_movement_support import present_battle_message_fields\n    frame = present_battle_message_fields(state, _battle_policy_retained_frame(state, entered))\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 148244:\n    from ..high_level_remaining_flows.business_highbank import evaluate_contact_position_order_fields\n    frame = evaluate_contact_position_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 149556:\n    from ..high_level_remaining_flows.business_highbank import evaluate_anchor_position_order_fields\n    frame = evaluate_anchor_position_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    result = _battle_policy_retained_result(state, entered, frame)\nelse:\n    result = _call(state, target, entered, continuation)\nreturn _leave_battle_policy_call(state, result, continuation)'}})

APPROVED.setdefault('business_highbank', set()).update({'evaluate_contact_position_order_fields', 'evaluate_anchor_position_order_fields'})

DECLARATIONS.update({'_call_battle_policy_external': {'signature': 'state: SceneState, target: Long, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'entered = _enter_battle_policy_call(state, policy, continuation)\nif target == 97418:\n    from .business_movement_support import ensure_neighbor_capacity_fields\n    frame = ensure_neighbor_capacity_fields(state, _battle_policy_retained_frame(state, entered))\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 98096:\n    from .business_movement_support import integrate_selected_officer_into_packed_group_fields\n    frame = integrate_selected_officer_into_packed_group_fields(state, _battle_policy_retained_frame(state, entered))\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 155876:\n    from .business_movement_support import present_battle_message_fields\n    frame = present_battle_message_fields(state, _battle_policy_retained_frame(state, entered))\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 148244:\n    from ..high_level_remaining_flows.business_highbank import evaluate_contact_position_order_fields\n    frame = evaluate_contact_position_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 149556:\n    from ..high_level_remaining_flows.business_highbank import evaluate_anchor_position_order_fields\n    frame = evaluate_anchor_position_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 146494:\n    from ..high_level_remaining_flows.business_highbank import evaluate_readiness_contact_action_fields\n    frame = evaluate_readiness_contact_action_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 146620:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_second_staging_order_fields\n    frame = evaluate_guarded_second_staging_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    result = _battle_policy_retained_result(state, entered, frame)\nelse:\n    result = _call(state, target, entered, continuation)\nreturn _leave_battle_policy_call(state, result, continuation)'}})

DECLARATIONS.update({'_execute_primary_indexed_order': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\ndisplacement = data_view(state, 'data_0235b6').word(low16(policy.target_x))\n_order_move_flags(state, displacement, 16)\npolicy = replace(policy, target_x=replace_word(policy.target_x, displacement))\nif policy.stack_cursor is None or policy.roster is None or policy.candidates is None:\n    raise Boundary('primary indexed order requires actual A0/A1/A7')\nstack = policy.stack_cursor.advance(-4)\nstack.set_long(0, policy.candidates.base)\nstack = stack.advance(-4)\nstack.set_long(0, policy.roster.base)\npolicy = replace(policy, stack_cursor=stack, roster=state.table_at(144912).cursor())\ntarget = u32(144912 + s16(displacement))\nentered = _enter_battle_policy_call(state, policy, 144810)\nif target == 144912:\n    returned = execute_primary_standard_order(state, entered)\nelif target == 146030:\n    returned = _primary_guarded_short_roster_tail(state, entered)\nelif target == 146620:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_second_staging_order_fields\n    frame = evaluate_guarded_second_staging_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    returned = _battle_policy_retained_result(state, entered, frame)\nelse:\n    returned = _call(state, target, entered, 144810)\nreturned = _leave_battle_policy_call(state, returned, 144810)\nstack = returned.stack_cursor\nroster = state.table_at(stack.long()).cursor()\nstack = stack.advance(4)\norders = state.table_at(stack.long()).cursor()\nreturn replace(returned, roster=roster, candidates=orders, stack_cursor=stack.advance(4))"}})

APPROVED.setdefault('business_highbank', set()).update({'evaluate_readiness_contact_action_fields', 'evaluate_guarded_second_staging_order_fields'})

DECLARATIONS.update({'_call_battle_policy_external': {'signature': 'state: SceneState, target: Long, policy: BattlePolicy, continuation: Long', 'returns': 'BattlePolicy', 'flow': 'entered = _enter_battle_policy_call(state, policy, continuation)\nif target == 97418:\n    from .business_movement_support import ensure_neighbor_capacity_fields\n    frame = ensure_neighbor_capacity_fields(state, _battle_policy_retained_frame(state, entered))\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 98096:\n    from .business_movement_support import integrate_selected_officer_into_packed_group_fields\n    frame = integrate_selected_officer_into_packed_group_fields(state, _battle_policy_retained_frame(state, entered))\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 155876:\n    from .business_movement_support import present_battle_message_fields\n    frame = present_battle_message_fields(state, _battle_policy_retained_frame(state, entered))\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 148244:\n    from ..high_level_remaining_flows.business_highbank import evaluate_contact_position_order_fields\n    frame = evaluate_contact_position_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 149556:\n    from ..high_level_remaining_flows.business_highbank import evaluate_anchor_position_order_fields\n    frame = evaluate_anchor_position_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 146494:\n    from ..high_level_remaining_flows.business_highbank import evaluate_readiness_contact_action_fields\n    frame = evaluate_readiness_contact_action_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 146620:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_second_staging_order_fields\n    frame = evaluate_guarded_second_staging_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    result = _battle_policy_retained_result(state, entered, frame)\nelif target == 146068:\n    from ..high_level_remaining_flows.business_highbank import evaluate_first_staging_position_fields\n    frame = evaluate_first_staging_position_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    result = _battle_policy_retained_result(state, entered, frame)\nelse:\n    result = _call(state, target, entered, continuation)\nreturn _leave_battle_policy_call(state, result, continuation)'}})

APPROVED.setdefault('business_highbank', set()).add('evaluate_first_staging_position_fields')


# Whole indexed caller: current8 external branches and235AA retained elsewhere.
DECLARATIONS.update({'_execute_primary_indexed_order': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\ndisplacement = data_view(state, 'data_0235b6').word(low16(policy.target_x))\n_order_move_flags(state, displacement, 16)\npolicy = replace(policy, target_x=replace_word(policy.target_x, displacement))\nif policy.stack_cursor is None or policy.roster is None or policy.candidates is None:\n    raise Boundary('primary indexed order requires actual A0/A1/A7')\nstack = policy.stack_cursor.advance(-4)\nstack.set_long(0, policy.candidates.base)\nstack = stack.advance(-4)\nstack.set_long(0, policy.roster.base)\npolicy = replace(policy, stack_cursor=stack, roster=state.table_at(144912).cursor())\ntarget = u32(144912 + s16(displacement))\nentered = _enter_battle_policy_call(state, policy, 144810)\nif target == 144912:\n    returned = execute_primary_standard_order(state, entered)\nelif target == 146030:\n    returned = _primary_guarded_short_roster_tail(state, entered)\nelif target == 146620:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_second_staging_order_fields\n    frame = evaluate_guarded_second_staging_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    returned = _battle_policy_retained_result(state, entered, frame)\nelif target == 146846:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_first_region_order_fields\n    frame = evaluate_guarded_first_region_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    returned = _battle_policy_retained_result(state, entered, frame)\nelse:\n    returned = _call(state, target, entered, 144810)\nreturned = _leave_battle_policy_call(state, returned, 144810)\nstack = returned.stack_cursor\nroster = state.table_at(stack.long()).cursor()\nstack = stack.advance(4)\norders = state.table_at(stack.long()).cursor()\nreturn replace(returned, roster=roster, candidates=orders, stack_cursor=stack.advance(4))"}})
APPROVED.setdefault('business_highbank', set()).add('evaluate_guarded_first_region_order_fields')


# Whole current indexed caller, existing eight external branches/235AA unchanged.
DECLARATIONS.update({'_execute_primary_indexed_order': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\ndisplacement = data_view(state, 'data_0235b6').word(low16(policy.target_x))\n_order_move_flags(state, displacement, 16)\npolicy = replace(policy, target_x=replace_word(policy.target_x, displacement))\nif policy.stack_cursor is None or policy.roster is None or policy.candidates is None:\n    raise Boundary('primary indexed order requires actual A0/A1/A7')\nstack = policy.stack_cursor.advance(-4)\nstack.set_long(0, policy.candidates.base)\nstack = stack.advance(-4)\nstack.set_long(0, policy.roster.base)\npolicy = replace(policy, stack_cursor=stack, roster=state.table_at(144912).cursor())\ntarget = u32(144912 + s16(displacement))\nentered = _enter_battle_policy_call(state, policy, 144810)\nif target == 144912:\n    returned = execute_primary_standard_order(state, entered)\nelif target == 146030:\n    returned = _primary_guarded_short_roster_tail(state, entered)\nelif target == 146620:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_second_staging_order_fields\n    frame = evaluate_guarded_second_staging_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    returned = _battle_policy_retained_result(state, entered, frame)\nelif target == 146846:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_first_region_order_fields\n    frame = evaluate_guarded_first_region_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    returned = _battle_policy_retained_result(state, entered, frame)\nelif target == 147646:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_second_region_order_fields\n    frame = evaluate_guarded_second_region_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    returned = _battle_policy_retained_result(state, entered, frame)\nelif target == 148206:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_small_force_region_tail_fields\n    frame = evaluate_guarded_small_force_region_tail_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    returned = _battle_policy_retained_result(state, entered, frame)\nelse:\n    returned = _call(state, target, entered, 144810)\nreturned = _leave_battle_policy_call(state, returned, 144810)\nstack = returned.stack_cursor\nroster = state.table_at(stack.long()).cursor()\nstack = stack.advance(4)\norders = state.table_at(stack.long()).cursor()\nreturn replace(returned, roster=roster, candidates=orders, stack_cursor=stack.advance(4))"}})
APPROVED.setdefault('business_highbank', set()).update({'evaluate_guarded_second_region_order_fields', 'evaluate_guarded_small_force_region_tail_fields'})


# Whole indexed caller, all existing dispatch/235AA slots preserved.
DECLARATIONS.update({'_execute_primary_indexed_order': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': "checked_context(policy, BattlePolicy, state)\ndisplacement = data_view(state, 'data_0235b6').word(low16(policy.target_x))\n_order_move_flags(state, displacement, 16)\npolicy = replace(policy, target_x=replace_word(policy.target_x, displacement))\nif policy.stack_cursor is None or policy.roster is None or policy.candidates is None:\n    raise Boundary('primary indexed order requires actual A0/A1/A7')\nstack = policy.stack_cursor.advance(-4)\nstack.set_long(0, policy.candidates.base)\nstack = stack.advance(-4)\nstack.set_long(0, policy.roster.base)\npolicy = replace(policy, stack_cursor=stack, roster=state.table_at(144912).cursor())\ntarget = u32(144912 + s16(displacement))\nentered = _enter_battle_policy_call(state, policy, 144810)\nif target == 144912:\n    returned = execute_primary_standard_order(state, entered)\nelif target == 146030:\n    returned = _primary_guarded_short_roster_tail(state, entered)\nelif target == 146620:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_second_staging_order_fields\n    frame = evaluate_guarded_second_staging_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    returned = _battle_policy_retained_result(state, entered, frame)\nelif target == 146846:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_first_region_order_fields\n    frame = evaluate_guarded_first_region_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    returned = _battle_policy_retained_result(state, entered, frame)\nelif target == 147646:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_second_region_order_fields\n    frame = evaluate_guarded_second_region_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    returned = _battle_policy_retained_result(state, entered, frame)\nelif target == 148206:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_small_force_region_tail_fields\n    frame = evaluate_guarded_small_force_region_tail_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    returned = _battle_policy_retained_result(state, entered, frame)\nelif target == 148616:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_third_region_order_fields\n    frame = evaluate_guarded_third_region_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    returned = _battle_policy_retained_result(state, entered, frame)\nelif target == 148940:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_west_contact_order_fields\n    frame = evaluate_guarded_west_contact_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    returned = _battle_policy_retained_result(state, entered, frame)\nelif target == 149192:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_first_staging_order_fields\n    frame = evaluate_guarded_first_staging_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    returned = _battle_policy_retained_result(state, entered, frame)\nelif target == 149510:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_terrain_region_order_fields\n    frame = evaluate_guarded_terrain_region_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    returned = _battle_policy_retained_result(state, entered, frame)\nelif target == 150138:\n    from ..high_level_remaining_flows.business_highbank import evaluate_guarded_alternate_anchor_order_fields\n    frame = evaluate_guarded_alternate_anchor_order_fields(state, _battle_policy_retained_frame(state, entered), True).frame\n    returned = _battle_policy_retained_result(state, entered, frame)\nelse:\n    returned = _call(state, target, entered, 144810)\nreturned = _leave_battle_policy_call(state, returned, 144810)\nstack = returned.stack_cursor\nroster = state.table_at(stack.long()).cursor()\nstack = stack.advance(4)\norders = state.table_at(stack.long()).cursor()\nreturn replace(returned, roster=roster, candidates=orders, stack_cursor=stack.advance(4))"}})
APPROVED.setdefault('business_highbank', set()).update({'evaluate_guarded_west_contact_order_fields', 'evaluate_guarded_first_staging_order_fields', 'evaluate_guarded_terrain_region_order_fields', 'evaluate_guarded_third_region_order_fields', 'evaluate_guarded_alternate_anchor_order_fields'})

DECLARATIONS.update({'_force_budget_roster_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, address: str, destination: int, instruction: int', 'returns': 'FirstDeploymentFrame', 'flow': "if (address, destination, instruction) not in (('roster', 4294965096, 140446), ('controller', 4294965100, 140488)):\n    raise ValueError('original budget roster phase required')\nframe = _movement_move_long(state, frame, 'target_x', 0)\nwhile True:\n    roster = getattr(frame, address)\n    member = roster.word()\n    advanced = state.table_at(u32(roster.base + 2))\n    frame = first_replace(frame, **{address: advanced.cursor() if address == 'roster' else advanced})\n    frame = _movement_move(state, frame, 'target_y', member, 16)\n    if frame.status & 8:\n        break\n    frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)\n    frame = _movement_arithmetic_long(state, frame, 'target_x', frame.opponent.long(low16(frame.target_y)))\n    frame = _movement_arithmetic_long(state, frame, 'target_x', 100)\nif frame.target_x // 50 <= 65535:\n    frame = _movement_divu_word(state, frame, 'target_x', 50, instruction)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_x', 1)\nframe = _movement_add_word(state, frame, 'target_x', low16(frame.target_y))\nframe = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)\nstate.write(destination, 4, frame.target_x)\nreturn _movement_test_long(state, frame, frame.target_x)"}})

DECLARATIONS.update({'_force_loss_compact_member_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = first_replace(frame, scratch=state.table_at(frame.roster.base))\nwhile True:\n    value = frame.scratch.word()\n    frame = first_replace(frame, scratch=state.table_at(u32(frame.scratch.base + 2)))\n    frame = _settlement_store_word_fields(state, frame, frame.scratch, 0, value, displacement=-4)\n    if frame.status & 8:\n        break\nreturn first_replace(frame, roster=frame.roster.advance(-2))'}})

DECLARATIONS.update({'_force_loss_message_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, player: int, message: int, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "if (message, continuation) not in ((202, 140098), (322, 140194), (323, 140232)):\n    raise ValueError('original supply-loss message phase required')\nvalue = state.read(4294964086, 2)\nstack = frame.stack_cursor.advance(-2)\nstack.set_word(0, value)\nframe = first_replace(frame, stack_cursor=stack)\nframe = _movement_test(state, frame, value, 16)\nsaved = ('target_x', 'target_y', 'roster', 'controller', 'opponent')\nframe = _movement_save_longs(state, frame, saved)\nif message != 202:\n    player = state.read(player, 2)\nframe = _duel_menu_write_word_fields(state, frame, 4294964086, player)\nif message == 202:\n    frame = _duel_menu_write_word_fields(state, frame, 4294964176, low16(frame.unit))\nframe = _duel_menu_write_word_fields(state, frame, 4294965056, message)\nframe = _force_turn_call_fields(state, frame, 155876, continuation)\nframe = _movement_restore_longs(state, frame, saved)\nrestored = frame.stack_cursor.word()\nframe = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\nreturn _duel_menu_write_word_fields(state, frame, 4294964086, restored)"}})

DECLARATIONS.update({'_force_turn_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, target)\nuint(target, 32)\nuint(continuation, 32)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = first_replace(frame, stack_cursor=stack)\nif target == 139852:\n    returned = settle_both_force_supply_fields(state, entered)\nelif target == 139896:\n    returned = deduct_force_supply_fields(state, entered)\nelif target == 139944:\n    returned = apply_force_supply_losses_fields(state, entered)\nelif target == 140246:\n    returned = check_battle_commanders_present_fields(state, entered)\nelif target == 140312:\n    returned = execute_secondary_force_orders_fields(state, entered)\nelif target == 140400:\n    returned = calculate_force_supply_budgets_fields(state, entered)\nelif target == 144738:\n    policy = _force_turn_policy_fields(entered)\n    returned = _battle_policy_retained_frame(state, execute_primary_force_orders(state, policy))\nelif target == 155876:\n    returned = present_battle_message_fields(state, entered)\nelse:\n    returned = execute_deployment_menu_fields(state, target, entered)\nreturned = _resource_cost_frame(state, returned, target)\nactual = returned.stack_cursor.long()\nif actual != continuation:\n    from .business_movement_support import MovementContinuationBoundary\n    raise MovementContinuationBoundary(actual, returned, 'actual force-turn child return token changed')\nreturn first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))"}})

DECLARATIONS.update({'_force_turn_divu_mask_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, carrier: str, divisor: int, instruction: int', 'returns': 'FirstDeploymentFrame', 'flow': "if (carrier, divisor, instruction) not in (('target_x', 100, 139922), ('count', 100, 140116)):\n    raise ValueError('original masked force-loss division required')\nif frame.carrier(carrier) // divisor <= 65535:\n    frame = _movement_divu_word(state, frame, carrier, divisor, instruction)\nreturn _movement_move_long(state, frame, carrier, frame.carrier(carrier) & 65535)"}})

DECLARATIONS.update({'_force_turn_policy_fields': {'signature': 'frame: FirstDeploymentFrame', 'returns': 'BattlePolicy', 'flow': 'return BattlePolicy(target_x=frame.target_x, target_y=frame.target_y, unit=frame.unit, count=frame.count, distance=frame.distance, offset_x=frame.offset_x, offset_y=frame.offset_y, choice=frame.choice, roster=frame.roster, candidates=frame.candidates, controller=frame.controller, scan=frame.scan, opponent=frame.opponent, scratch=frame.scratch, auxiliary=frame.auxiliary, stack_cursor=frame.stack_cursor)'}})

DECLARATIONS.update({'apply_force_supply_losses': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\nframe = apply_force_supply_losses_fields(state, _battle_policy_retained_frame(state, policy))\nreturn _battle_policy_retained_result(state, policy, frame)'}})

DECLARATIONS.update({'apply_force_supply_losses_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 139944)\nframe = _force_turn_call_fields(state, frame, 33748, 139950)\nframe = _movement_move_long(state, frame, 'target_x', 0)\nframe = _movement_move(state, frame, 'target_x', state.read(4294964764, 2), 16)\nframe = _movement_move_long(state, frame, 'target_y', frame.target_x)\nframe = _movement_move_long(state, frame, 'unit', frame.target_x)\nframe = _special_action_shift_long(state, frame, 'target_x', 1)\nframe = _movement_arithmetic_long(state, frame, 'target_x', frame.target_y)\nframe = _special_action_swap(state, frame, 'target_x')\nframe = _movement_add_word(state, frame, 'target_x', 3)\nframe = _movement_move_long(state, frame, 'target_y', frame.unit)\nframe = _special_action_shift_long(state, frame, 'target_y', 2)\nframe = _movement_arithmetic_long(state, frame, 'target_y', frame.unit)\nframe = _special_action_shift_long(state, frame, 'target_y', 1)\nframe = _movement_arithmetic_long(state, frame, 'target_y', frame.unit)\nframe = _special_action_swap(state, frame, 'target_y')\nframe = _movement_add_word(state, frame, 'target_y', 20)\nwhile True:\n    member = frame.roster.word()\n    frame = first_replace(frame, roster=frame.roster.advance(2))\n    frame = _movement_move(state, frame, 'unit', member, 16)\n    if frame.status & 8:\n        return frame\n    frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 255, 16)\n    frame = _movement_fixed_shift_word(state, frame, 'unit', 1)\n    readiness = frame.opponent.word(low16(frame.unit))\n    frame, value = _movement_binary_flags(state, frame, readiness, low16(frame.target_x), 16, True)\n    frame.opponent.set_word(low16(frame.unit), value)\n    if not frame.status & 5:\n        frame = _movement_fixed_shift_word(state, frame, 'unit', 1)\n        frame = _movement_move_long(state, frame, 'count', frame.controller.long(low16(frame.unit)))\n        frame = _movement_multiply_word(state, frame, 'count', low16(frame.target_y))\n        frame = _force_turn_divu_mask_fields(state, frame, 'count', 100, 140116)\n        troops = frame.controller.long(low16(frame.unit))\n        frame, value = _movement_binary_flags(state, frame, troops, frame.count, 32, True)\n        frame.controller.set_long(low16(frame.unit), value)\n        continue\n    frame = _movement_fixed_shift_word(state, frame, 'unit', 1, True)\n    frame = first_replace(frame, scratch=state.table_at(4294953984))\n    frame = _movement_move(state, frame, 'count', frame.scratch.byte(low16(frame.unit)), 8)\n    frame = _settlement_write_byte_fields(state, frame, frame.scratch, 255, low16(frame.unit))\n    frame = _force_loss_compact_member_fields(state, frame)\n    frame = _movement_move(state, frame, 'count', low16(frame.count) & 63, 16)\n    frame = first_replace(frame, scratch=state.table_at(4294964263))\n    frame = _movement_move(state, frame, 'count', frame.scratch.byte(low16(frame.count)), 8)\n    frame = _movement_move(state, frame, 'count', low16(frame.count) & 15, 16)\n    for player in (4294964858, 4294964860, 4294964862):\n        frame = _movement_compare(state, frame, low16(frame.count), state.read(player, 2), 16)\n        if frame.status & 4:\n            break\n    else:\n        frame = first_replace(frame, candidates=state.table_at(4294964318).cursor())\n        frame = _movement_move(state, frame, 'count', state.read(4294964874, 2), 16)\n        frame = _movement_fixed_shift_word(state, frame, 'count', 1)\n        frame = _movement_compare(state, frame, low16(frame.unit), frame.candidates.word(low16(frame.count)), 16)\n        if frame.status & 4:\n            frame = _force_loss_message_fields(state, frame, 4294964876, 323, 140232)\n            continue\n        frame = first_replace(frame, candidates=state.table_at(4294942759).cursor())\n        frame = _movement_move(state, frame, 'count', state.read(4294964874, 2), 16)\n        frame = _movement_compare(state, frame, low8(frame.unit), frame.candidates.byte(low16(frame.count)), 8)\n        if frame.status & 4:\n            frame = _force_loss_message_fields(state, frame, 4294964878, 322, 140194)\n        continue\n    frame = _force_loss_message_fields(state, frame, low16(frame.count), 202, 140098)"}})

DECLARATIONS.update({'calculate_force_supply_budgets': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\nframe = calculate_force_supply_budgets_fields(state, _battle_policy_retained_frame(state, policy))\nresult = _battle_policy_retained_result(state, policy, frame)\nreturn replace(result, scan=state.table_at(frame.controller.base).cursor(), controller=policy.controller)'}})

DECLARATIONS.update({'calculate_force_supply_budgets_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 140400)\nframe = first_replace(frame, roster=state.table_at(4294944080).cursor(), controller=state.table_at(4294944164))\nfrom ..high_level_remaining_flows.business_city import _duel_menu_byte_bit_fields\nframe = _duel_menu_byte_bit_fields(state, frame, 4294964951, 1)\nif not frame.status & 4:\n    first, second = (frame.roster, frame.controller)\n    frame = first_replace(frame, roster=state.table_at(second.base).cursor(), controller=state.table_at(first.base))\nframe = first_replace(frame, opponent=state.table_at(4294952960))\nframe = _force_budget_roster_fields(state, frame, 'roster', 4294965096, 140446)\nreturn _force_budget_roster_fields(state, frame, 'controller', 4294965100, 140488)"}})

DECLARATIONS.update({'check_battle_commanders_present': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\nframe = check_battle_commanders_present_fields(state, _battle_policy_retained_frame(state, policy))\nreturn _battle_policy_retained_result(state, policy, frame)'}})

DECLARATIONS.update({'check_battle_commanders_present_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 140246)\nframe = first_replace(frame, candidates=state.table_at(4294953984).cursor(), roster=state.table_at(4294942759).cursor())\nframe = _movement_move(state, frame, 'target_x', state.read(4294964874, 2), 16)\nframe = _movement_move(state, frame, 'target_y', 0, 16)\nframe = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.target_x)), 8)\nframe = _movement_compare(state, frame, frame.candidates.byte(low16(frame.target_y)), 255, 8)\nif frame.status & 4:\n    state.sr |= 1\n    return first_replace(frame, status=frame.status | 1)\nframe = _movement_move(state, frame, 'target_x', state.read(4294964874, 2), 16)\nframe = first_replace(frame, roster=state.table_at(4294964318).cursor())\nframe = _movement_fixed_shift_word(state, frame, 'target_x', 1)\nframe = _movement_move(state, frame, 'target_x', frame.roster.byte(low16(frame.target_x)), 8)\nframe = _movement_compare(state, frame, frame.candidates.byte(low16(frame.target_x)), 255, 8)\ncarry = bool(frame.status & 4)\nstate.sr = state.sr & 65534 | int(carry)\nreturn first_replace(frame, status=frame.status & 30 | int(carry))"}})

DECLARATIONS.update({'deduct_force_supply': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\nframe = deduct_force_supply_fields(state, _battle_policy_retained_frame(state, policy))\nreturn _battle_policy_retained_result(state, policy, frame)'}})

DECLARATIONS.update({'deduct_force_supply_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 139896)\nframe = first_replace(frame, scan=state.table_at(frame.roster.base).cursor())\nframe = _movement_move_long(state, frame, 'target_x', 0)\nwhile True:\n    member = frame.scan.word()\n    frame = first_replace(frame, scan=frame.scan.advance(2))\n    frame = _movement_move(state, frame, 'target_y', member, 16)\n    if frame.status & 8:\n        break\n    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 255, 16)\n    frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)\n    frame = _movement_arithmetic_long(state, frame, 'target_x', frame.controller.long(low16(frame.target_y)))\n    frame = _movement_arithmetic_long(state, frame, 'target_x', 100)\nframe = _force_turn_divu_mask_fields(state, frame, 'target_x', 100, 139922)\nsupply = frame.candidates.long()\nframe, remaining = _movement_binary_flags(state, frame, supply, frame.target_x, 32, True)\nframe.candidates.set_long(0, remaining)\nif not frame.status & 1:\n    return frame\nframe.candidates.long()\nframe.candidates.set_long(0, 0)\nframe = _movement_test_long(state, frame, 0)\nreturn _force_turn_call_fields(state, frame, 139944, 139942)"}})

DECLARATIONS.update({'execute_secondary_force_orders': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\nframe = execute_secondary_force_orders_fields(state, _battle_policy_retained_frame(state, policy))\nreturn _battle_policy_retained_result(state, policy, frame)'}})

DECLARATIONS.update({'execute_secondary_force_orders_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 140312)\nframe = _force_turn_call_fields(state, frame, 150272, 140316)\nframe = _force_turn_call_fields(state, frame, 140400, 140320)\nframe = first_replace(frame, roster=state.table_at(4294944164).cursor(), candidates=state.table_at(4294946710).cursor())\nwhile True:\n    member = frame.roster.word()\n    frame = first_replace(frame, roster=frame.roster.advance(2))\n    frame = _movement_move(state, frame, 'choice', member, 16)\n    if frame.status & 8:\n        return _duel_menu_write_word_fields(state, frame, 4294964066, 0, clear=True)\n    order = frame.candidates.word()\n    frame = first_replace(frame, candidates=frame.candidates.advance(2))\n    frame = _movement_move(state, frame, 'target_x', order, 16)\n    frame = _movement_compare(state, frame, low16(frame.target_x), 255, 16)\n    if frame.status & 4:\n        continue\n    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)\n    relative = state.read(u32(140374 + s16(low16(frame.target_x))), 2)\n    frame = _movement_move(state, frame, 'target_x', relative, 16)\n    saved = ('roster', 'candidates')\n    frame = _movement_save_longs(state, frame, saved)\n    frame = first_replace(frame, roster=state.table_at(140510).cursor())\n    target = u32(frame.roster.base + s16(low16(frame.target_x)))\n    frame = _force_turn_call_fields(state, frame, target, 140362)\n    frame = _movement_restore_longs(state, frame, saved)"}})

DECLARATIONS.update({'process_both_battle_force_turns': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\nframe = process_both_battle_force_turns_fields(state, _battle_policy_retained_frame(state, policy))\nreturn _battle_policy_retained_result(state, policy, frame)'}})

DECLARATIONS.update({'process_both_battle_force_turns_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 139748)\nframe = _force_turn_call_fields(state, frame, 139852, 139752)\nframe = _force_turn_call_fields(state, frame, 140246, 139756)\nif frame.status & 1:\n    return frame\nfor affiliation, side, target, continuation in ((4294964876, 0, 144738, 139798), (4294964878, 2, 140312, 139836)):\n    frame = _movement_move(state, frame, 'target_x', state.read(affiliation, 2), 16)\n    for player in (4294964858, 4294964860, 4294964862):\n        frame = _movement_compare(state, frame, low16(frame.target_x), state.read(player, 2), 16)\n        if frame.status & 4:\n            break\n    else:\n        frame = _duel_menu_write_word_fields(state, frame, 4294964950, side, clear=side == 0)\n        frame = _force_turn_call_fields(state, frame, target, continuation)\nframe = _movement_compare(state, frame, state.read(4294964754, 2), 1041, 16)\nif frame.status & 4:\n    return frame\nreturn _duel_menu_write_word_fields(state, frame, 4294964950, 0, clear=True)"}})

DECLARATIONS.update({'settle_both_force_supply': {'signature': 'state: SceneState, policy: BattlePolicy', 'returns': 'BattlePolicy', 'flow': 'checked_context(policy, BattlePolicy, state)\nframe = settle_both_force_supply_fields(state, _battle_policy_retained_frame(state, policy))\nreturn _battle_policy_retained_result(state, policy, frame)'}})

DECLARATIONS.update({'settle_both_force_supply_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _resource_cost_frame(state, frame, 139852)\nframe = first_replace(frame, controller=state.table_at(4294952960), opponent=state.table_at(4294947328))\nframe = _duel_menu_write_word_fields(state, frame, 4294964950, 0, clear=True)\nframe = first_replace(frame, roster=state.table_at(4294944080).cursor(), candidates=state.table_at(4294964894).cursor())\nframe = _force_turn_call_fields(state, frame, 139896, 139876)\nframe = _duel_menu_write_word_fields(state, frame, 4294964950, 2)\nframe = first_replace(frame, roster=state.table_at(4294944164).cursor(), candidates=state.table_at(4294964898).cursor())\nreturn _force_turn_call_fields(state, frame, 139896, 139894)'}})

APPROVED.setdefault('services',set()).update(('FirstDeploymentFrame',))

APPROVED.setdefault('business_movement_support',set()).update(('first_replace', '_movement_move', '_movement_test', '_movement_compare', '_movement_move_long', '_movement_test_long', '_movement_arithmetic_long', '_movement_binary_flags', '_movement_fixed_shift_word', '_movement_add_word', '_movement_multiply_word', '_movement_save_longs', '_movement_restore_longs', '_movement_divu_word', 'present_battle_message_fields'))

APPROVED.setdefault('business_city',set()).update(('_resource_cost_frame', '_duel_menu_write_word_fields', '_settlement_store_word_fields', '_settlement_write_byte_fields', '_special_action_shift_long', '_special_action_swap', 'execute_deployment_menu_fields'))

APPROVED.setdefault('business_city',set()).update(('_duel_menu_byte_bit_fields',))

APPROVED.setdefault('business_movement_support',set()).update(('MovementContinuationBoundary',))

DECLARATIONS.pop('_project_order',None)

DECLARATIONS.pop('_cancel_project',None)

DECLARATIONS.pop('_pay_project',None)

DECLARATIONS.pop('_project_aptitude',None)

DECLARATIONS.pop('_reward_project_intellect',None)

DECLARATIONS.update({'_city_project_aptitude_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, division: int', 'returns': 'FirstDeploymentFrame', 'flow': "if division not in (72210, 72426):\n    raise ValueError('original first/second project aptitude phase required')\nframe = _movement_move_long(state, frame, 'distance', frame.count)\nframe = _city_project_divu_fields(state, frame, 'distance', 5, division)\nframe = _movement_move(state, frame, 'target_y', low16(frame.unit), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 1)\nframe = first_replace(frame, roster=state.table_at(4294948352).cursor())\nframe = _movement_add_word(state, frame, 'distance', frame.roster.word(low16(frame.target_y)))\nframe = first_replace(frame, roster=state.table_at(4294950400).cursor())\nframe = _movement_move(state, frame, 'target_y', frame.roster.word(low16(frame.target_y)), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 1, True)\nreturn _movement_add_word(state, frame, 'distance', low16(frame.target_y))"}})

DECLARATIONS.update({'_city_project_begin_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, table: int', 'returns': 'tuple[FirstDeploymentFrame, str]', 'flow': "if table not in (4294961164, 4294961168, 4294961172):\n    raise ValueError('original project order table required')\nframe = _movement_move(state, frame, 'target_x', state.read(4294964068, 2), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_x', 1)\nframe = _movement_add_word(state, frame, 'target_x', state.read(4294964068, 2))\nframe = _movement_fixed_shift_word(state, frame, 'target_x', 2)\nframe = first_replace(frame, roster=state.table_at(table).cursor())\nofficer = frame.roster.word(low16(frame.target_x))\nframe = first_replace(frame, unit=u32(s16(officer)))\nbudget = frame.roster.word(low16(frame.target_x), 2)\nframe = first_replace(frame, count=u32(s16(budget)))\nframe = _movement_test(state, frame, low16(frame.unit), 16)\nif frame.status & 8:\n    return (frame, 'absent')\nframe = _movement_move(state, frame, 'distance', frame.auxiliary.byte(low16(frame.unit)), 8)\nframe = _movement_compare(state, frame, low8(frame.distance), state.read(4294964069, 1), 8)\nreturn (frame, 'ready' if frame.status & 4 else 'cancel')"}})

DECLARATIONS.update({'_city_project_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, target)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, uint(continuation, 32))\nentered = first_replace(frame, stack_cursor=stack)\nif target == 72106:\n    result = settle_all_city_projects_fields(state, entered)\nelif target == 72144:\n    result = settle_first_city_project_fields(state, entered)\nelif target == 72360:\n    result = settle_second_city_project_fields(state, entered)\nelif target == 72646:\n    result = settle_third_city_project_fields(state, entered)\nelif target == 72844:\n    from .reuse_rules import award_defense_progress_fields\n    result = award_defense_progress_fields(state, entered)\nelif target == 72906:\n    from .reuse_rules import clear_completed_monthly_actions_fields\n    result = clear_completed_monthly_actions_fields(state, entered)\nelse:\n    result = execute_deployment_menu_fields(state, target, entered)\nresult = _resource_cost_frame(state, result, target)\nactual = result.stack_cursor.long()\nif actual != continuation:\n    from .business_movement_support import MovementContinuationBoundary\n    raise MovementContinuationBoundary(actual, result, 'actual project child return LONG changed')\nreturn first_replace(result, stack_cursor=result.stack_cursor.advance(4))"}})

DECLARATIONS.update({'_city_project_cancel_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _settlement_store_word_fields(state, frame, frame.roster, low16(frame.target_x), 65535)\nreturn _settlement_write_byte_fields(state, frame, frame.scratch, value=0, offset=low16(frame.unit), clear=True)'}})

DECLARATIONS.update({'_city_project_divu_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, carrier: str, divisor: int, instruction: int', 'returns': 'FirstDeploymentFrame', 'flow': "if (carrier, divisor, instruction) not in (('distance', 5, 72210), ('distance', 1000, 72266), ('distance', 5, 72426), ('distance', 60000, 72524), ('count', 50, 72714), ('count', 1000, 72778)):\n    raise ValueError('original project division phase required')\nif frame.carrier(carrier) // divisor <= 65535:\n    return _movement_divu_word(state, frame, carrier, divisor, instruction)\nreturn frame"}})

DECLARATIONS.update({'_city_project_intellect_reward_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _special_action_shift_long(state, frame, 'unit', 1)\nframe = first_replace(frame, roster=state.table_at(4294950400).cursor())\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(low16(frame.unit)), 16)\nframe = _movement_add_word(state, frame, 'target_x', low16(frame.distance))\nframe = _movement_compare(state, frame, low16(frame.target_x), 999, 16)\nif not frame.status & 5:\n    frame = _movement_move(state, frame, 'target_x', 999, 16)\nreturn _settlement_store_word_fields(state, frame, frame.roster, low16(frame.unit), low16(frame.target_x))"}})

DECLARATIONS.update({'_city_project_legacy_entry_fields': {'signature': 'state: SceneState, values: ProjectValues', 'returns': 'FirstDeploymentFrame', 'flow': 'checked_context(values, ProjectValues, state)\nreturn first_replace(FirstDeploymentFrame.unobserved(), target_x=values.city_index, target_y=values.record_index, unit=values.officer, count=values.budget, distance=values.value, offset_x=values.scale, offset_y=values.city_offset, choice=values.effect, roster=None if values.orders is None else values.orders.cursor(), scratch=values.task_flags, auxiliary=values.assignments, status=state.sr & 31)'}})

DECLARATIONS.update({'_city_project_legacy_result_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'ProjectValues', 'flow': 'return ProjectValues(officer=frame.unit, budget=frame.count, value=frame.distance, scale=frame.offset_x, effect=frame.choice, city_index=frame.target_x, record_index=frame.target_y, city_offset=frame.offset_y, assignments=state.table_at(frame.auxiliary.base), task_flags=state.table_at(frame.scratch.base), orders=state.table_at(frame.roster.base)).validate(state)'}})

DECLARATIONS.update({'_city_project_pay_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _movement_move(state, frame, 'target_y', state.read(4294964068, 2), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 2)\nframe = first_replace(frame, candidates=state.table_at(4294959100).cursor())\nframe = _movement_move_long(state, frame, 'distance', frame.candidates.long(low16(frame.target_y)))\nframe = _movement_arithmetic_long(state, frame, 'distance', frame.count, True)\nif not frame.status & 1:\n    frame.candidates.set_long(low16(frame.target_y), frame.distance)\n    frame = _movement_test_long(state, frame, frame.distance)\nreturn frame"}})

DECLARATIONS.update({'settle_all_city_projects': {'signature': 'state: SceneState, values: ProjectValues', 'returns': 'ProjectValues', 'flow': 'frame = settle_all_city_projects_fields(state, _city_project_legacy_entry_fields(state, values))\nreturn _city_project_legacy_result_fields(state, frame)'}})

DECLARATIONS.update({'settle_all_city_projects_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _resource_cost_frame(state, frame, 72106)\nframe = _duel_menu_write_word_fields(state, frame, 4294964068, 0, clear=True)\nframe = first_replace(frame, auxiliary=state.table_at(4294953984), scratch=state.table_at(4294954240))\nwhile True:\n    counter = state.read(4294964068, 2)\n    frame, counter = _movement_binary_flags(state, frame, counter, 1, 16)\n    state.write(4294964068, 2, counter)\n    for target, continuation in ((72144, 72126), (72360, 72130), (72646, 72134)):\n        frame = _city_project_call_fields(state, frame, target, continuation)\n    frame = _movement_compare(state, frame, state.read(4294964068, 2), 40, 16)\n    if not frame.status & 1:\n        return frame'}})

DECLARATIONS.update({'settle_city_projects_and_refresh_map': {'signature': 'state: SceneState, values: ProjectValues', 'returns': 'ProjectValues', 'flow': 'frame = settle_city_projects_and_refresh_map_fields(state, _city_project_legacy_entry_fields(state, values))\nreturn _city_project_legacy_result_fields(state, frame)'}})

DECLARATIONS.update({'settle_city_projects_and_refresh_map_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 71950)\nframe = _city_project_call_fields(state, frame, 72106, 71954)\nframe = _city_project_call_fields(state, frame, 72906, 71958)\nframe = first_replace(frame, candidates=state.table_at(4294955776).cursor())\nframe = _movement_move(state, frame, 'count', 31, 16)\nwhile True:\n    frame.candidates.set_long(0, 286331153)\n    frame = first_replace(frame, candidates=frame.candidates.advance(4))\n    frame = _movement_test_long(state, frame, 286331153)\n    remaining = u16(low16(frame.count) - 1)\n    frame = first_replace(frame, count=replace_word(frame.count, remaining))\n    if remaining == 65535:\n        break\nframe = first_replace(frame, roster=state.table_at(72100).cursor())\nframe = _movement_move(state, frame, 'target_x', 1, 16)\nframe = _movement_move(state, frame, 'target_y', 3, 16)\nframe = _movement_move(state, frame, 'count', 2, 16)\nframe = _city_project_call_fields(state, frame, 44682, 72000)\nstate.write(12582916, 4, 1075838976)\nframe = _movement_test_long(state, frame, 1075838976)\nframe = first_replace(frame, candidates=state.table_at(4294955776).cursor())\nframe = _movement_move(state, frame, 'count', 127, 16)\nwhile True:\n    value = frame.candidates.long()\n    frame = first_replace(frame, candidates=frame.candidates.advance(4))\n    state.write(12582912, 4, value)\n    frame = _movement_test_long(state, frame, value)\n    remaining = u16(low16(frame.count) - 1)\n    frame = first_replace(frame, count=replace_word(frame.count, remaining))\n    if remaining == 65535:\n        break\nframe = _city_project_call_fields(state, frame, 21936, 72034)\nframe = _duel_menu_write_word_fields(state, frame, 4294964066, 12)\nframe = _city_project_call_fields(state, frame, 199284, 72046)\nframe = _movement_test(state, frame, state.read(4294964102, 2), 16)\nif frame.status & 4:\n    frame = _city_project_call_fields(state, frame, 33786, 72060)\nfor address, value, clear in ((4294964754, 520, False), (4294964066, 19, False), (4294964074, 0, True), (4294964162, 522, False), (4294964164, 0, True), (4294954656, 0, True)):\n    frame = _duel_menu_write_word_fields(state, frame, address, value, clear=clear)\nreturn _duel_menu_write_word_fields(state, frame, 16723968, 65535)"}})

DECLARATIONS.update({'settle_first_city_project': {'signature': 'state: SceneState, values: ProjectValues', 'returns': 'ProjectValues', 'flow': 'frame = settle_first_city_project_fields(state, _city_project_legacy_entry_fields(state, values))\nreturn _city_project_legacy_result_fields(state, frame)'}})

DECLARATIONS.update({'settle_first_city_project_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 72144)\nframe, phase = _city_project_begin_fields(state, frame, 4294961164)\nif phase == 'absent':\n    return frame\nif phase == 'cancel':\n    return _city_project_cancel_fields(state, frame)\nframe = _city_project_pay_fields(state, frame)\nif frame.status & 1:\n    return _city_project_cancel_fields(state, frame)\nframe = _city_project_aptitude_fields(state, frame, 72210)\nframe = _city_project_call_fields(state, frame, 33748, 72244)\nframe = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)\nframe = _movement_move_long(state, frame, 'target_y', frame.target_x)\nframe = _special_action_shift_long(state, frame, 'target_x', 1)\nframe = _movement_arithmetic_long(state, frame, 'target_x', frame.target_y)\nframe = _special_action_shift_long(state, frame, 'target_x', 1)\nframe = _special_action_swap(state, frame, 'target_x')\nframe = _movement_add_word(state, frame, 'target_x', 10)\nframe = _movement_multiply_word(state, frame, 'distance', low16(frame.target_x))\nframe = _city_project_divu_fields(state, frame, 'distance', 1000, 72266)\nframe = _movement_move_long(state, frame, 'distance', u32(s16(low16(frame.distance))))\nframe = _movement_move(state, frame, 'target_y', state.read(4294964068, 2), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 2)\nframe = first_replace(frame, roster=state.table_at(4294959580).cursor())\nframe = _movement_move_long(state, frame, 'count', frame.roster.long(low16(frame.target_y)))\nframe = _movement_arithmetic_long(state, frame, 'count', frame.distance)\nframe = _movement_compare_address(state, frame, frame.count, 999)\nif not frame.status & 5:\n    frame = _movement_move(state, frame, 'count', 999, 16)\nframe.roster.set_long(low16(frame.target_y), frame.count)\nframe = _movement_test_long(state, frame, frame.count)\nreturn _city_project_intellect_reward_fields(state, frame)"}})

DECLARATIONS.update({'settle_second_city_project': {'signature': 'state: SceneState, values: ProjectValues', 'returns': 'ProjectValues', 'flow': 'frame = settle_second_city_project_fields(state, _city_project_legacy_entry_fields(state, values))\nreturn _city_project_legacy_result_fields(state, frame)'}})

DECLARATIONS.update({'settle_second_city_project_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 72360)\nframe, phase = _city_project_begin_fields(state, frame, 4294961168)\nif phase == 'absent':\n    return frame\nif phase == 'cancel':\n    return _city_project_cancel_fields(state, frame)\nframe = _city_project_pay_fields(state, frame)\nif frame.status & 1:\n    return _city_project_cancel_fields(state, frame)\nframe = _city_project_aptitude_fields(state, frame, 72426)\nframe = _city_project_call_fields(state, frame, 33748, 72460)\nframe = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)\nframe = _special_action_shift_long(state, frame, 'target_x', 2)\nframe = _special_action_swap(state, frame, 'target_x')\nframe = _movement_move(state, frame, 'offset_x', 8, 16)\nframe = _movement_move(state, frame, 'offset_y', state.read(4294964068, 2), 16)\nframe = _movement_fixed_shift_word(state, frame, 'offset_y', 2)\nframe = first_replace(frame, candidates=state.table_at(4294959900).cursor())\nframe = _movement_compare_address(state, frame, frame.candidates.long(low16(frame.offset_y)), 80)\nif not frame.status & 1:\n    frame = _movement_move(state, frame, 'offset_x', 2, 16)\nframe = _movement_add_word(state, frame, 'target_x', low16(frame.offset_x))\nframe = _movement_multiply_word(state, frame, 'distance', low16(frame.target_x))\nframe = first_replace(frame, roster=state.table_at(4294951424).cursor())\nframe = _movement_move(state, frame, 'target_x', 0, 16)\nframe = _movement_move(state, frame, 'target_x', frame.roster.byte(low16(frame.unit)), 8)\nframe = _movement_move(state, frame, 'target_y', low16(frame.distance), 16)\nframe = _movement_multiply_word(state, frame, 'target_y', low16(frame.target_x))\nframe = _special_action_swap(state, frame, 'distance')\nframe = _movement_multiply_word(state, frame, 'distance', low16(frame.target_x))\nframe = _special_action_swap(state, frame, 'distance')\nframe = _movement_arithmetic_long(state, frame, 'distance', frame.target_y)\nframe = _city_project_divu_fields(state, frame, 'distance', 60000, 72524)\nframe = _movement_move_long(state, frame, 'distance', u32(s16(low16(frame.distance))))\nframe = _movement_move(state, frame, 'target_y', state.read(4294964068, 2), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 2)\nframe = first_replace(frame, roster=state.table_at(4294959900).cursor())\nframe = _movement_move_long(state, frame, 'target_x', frame.roster.long(low16(frame.target_y)))\nframe = _movement_arithmetic_long(state, frame, 'target_x', frame.distance)\nframe = _movement_compare(state, frame, low16(frame.target_x), 100, 16)\nif not frame.status & 5:\n    frame = _movement_move(state, frame, 'target_x', 100, 16)\nframe.roster.set_long(low16(frame.target_y), frame.target_x)\nframe = _movement_test_long(state, frame, frame.target_x)\nframe = _city_project_intellect_reward_fields(state, frame)\nframe = _movement_compare(state, frame, low16(frame.distance), 5, 16)\nif frame.status & 1:\n    return frame\nframe = first_replace(frame, roster=state.table_at(4294951424).cursor())\nframe = _movement_fixed_shift_word(state, frame, 'unit', 1, True)\nframe = _movement_move(state, frame, 'target_x', frame.roster.byte(low16(frame.unit)), 8)\nframe = _movement_add_word(state, frame, 'target_x', 1)\nframe = _movement_compare(state, frame, low16(frame.target_x), 100, 16)\nif not frame.status & 5:\n    return frame\nreturn _settlement_write_byte_fields(state, frame, frame.roster, value=low8(frame.target_x), offset=low16(frame.unit))"}})

DECLARATIONS.update({'settle_third_city_project': {'signature': 'state: SceneState, values: ProjectValues', 'returns': 'ProjectValues', 'flow': 'frame = settle_third_city_project_fields(state, _city_project_legacy_entry_fields(state, values))\nreturn _city_project_legacy_result_fields(state, frame)'}})

DECLARATIONS.update({'settle_third_city_project_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 72646)\nframe, phase = _city_project_begin_fields(state, frame, 4294961172)\nif phase == 'absent':\n    return frame\nif phase == 'cancel':\n    return _city_project_cancel_fields(state, frame)\nframe = _movement_multiply_word(state, frame, 'count', 100)\nframe = _city_project_pay_fields(state, frame)\nif frame.status & 1:\n    return _city_project_cancel_fields(state, frame)\nframe = _city_project_divu_fields(state, frame, 'count', 50, 72714)\nframe = _movement_move(state, frame, 'target_y', low16(frame.unit), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 1)\nframe = first_replace(frame, roster=state.table_at(4294948352).cursor())\nframe = _movement_add_word(state, frame, 'count', frame.roster.word(low16(frame.target_y)))\nfor address in (4294950400, 4294950912):\n    frame = first_replace(frame, roster=state.table_at(address).cursor())\n    frame = _movement_move(state, frame, 'distance', frame.roster.word(low16(frame.target_y)), 16)\n    frame = _movement_fixed_shift_word(state, frame, 'distance', 2, True)\n    frame = _movement_add_word(state, frame, 'count', low16(frame.distance))\nframe = _city_project_call_fields(state, frame, 33748, 72760)\nframe = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)\nframe = _movement_move_long(state, frame, 'target_y', frame.target_x)\nframe = _special_action_shift_long(state, frame, 'target_x', 1)\nframe = _movement_arithmetic_long(state, frame, 'target_x', frame.target_y)\nframe = _special_action_swap(state, frame, 'target_x')\nframe = _movement_add_word(state, frame, 'target_x', 6)\nframe = _movement_multiply_word(state, frame, 'count', low16(frame.target_x))\nframe = _city_project_divu_fields(state, frame, 'count', 1000, 72778)\nframe = _movement_move(state, frame, 'target_x', state.read(4294964068, 2), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_x', 2)\nframe = first_replace(frame, roster=state.table_at(4294960540).cursor())\nframe = _movement_move(state, frame, 'choice', frame.roster.word(low16(frame.target_x), 2), 16)\nframe = _movement_add_word(state, frame, 'choice', low16(frame.count))\nframe = _movement_compare(state, frame, low16(frame.choice), 100, 16)\nif not frame.status & 5:\n    frame = _movement_move(state, frame, 'choice', 100, 16)\nframe = _settlement_store_word_fields(state, frame, frame.roster, low16(frame.target_x), low16(frame.choice), displacement=2)\nreturn _city_project_call_fields(state, frame, 72844, 72818)"}})

APPROVED.setdefault('business_movement_support',set()).update(('_movement_compare_address',))

APPROVED.setdefault('business_movement_support',set()).update(('MovementContinuationBoundary',))

APPROVED.setdefault('reuse_rules',set()).update(('award_defense_progress_fields',))

APPROVED.setdefault('reuse_rules',set()).update(('clear_completed_monthly_actions_fields',))

# D49 exact imports and whole-function declarations; ordinary lowerers unchanged.
APPROVED.setdefault((2, 'high_level_gameplay_flow.contexts_services'),set()).update(('SceneRefreshMemory',))
APPROVED.setdefault((2, 'high_level_gameplay_flow.business_services'),set()).update(('refresh_gameplay_scene_fields',))
APPROVED.setdefault((2, 'high_level_player_commands.contexts_display'),set()).update(('SpritePacketMemory',))
APPROVED.setdefault((2, 'high_level_player_commands.business_display'),set()).update(('append_live_command_sprite_fields',))
APPROVED.setdefault((2, 'high_level_battle_ai.contexts_policy_memory'),set()).update(('BattlePolicyMemory',))
APPROVED.setdefault((2, 'high_level_battle_ai.business_actions'),set()).update(('_deployment_terrain_lookup',))
APPROVED.setdefault((2, 'high_level_battle_ai.business_geometry'),set()).update(('rounded_deployment_radial_distance_fields',))
APPROVED.setdefault((2, 'high_level_gameplay_flow.business_battle'),set()).update(('_postbattle_bit_fields',))
APPROVED.setdefault('business_movement_support',set()).update(('MovementContinuationBoundary', '_movement_compare_address'))
APPROVED.setdefault((2, 'high_level_remaining_flows.business_city'),set()).update(('_city_encounter_shift_word_fields', '_duel_menu_byte_bit_fields', '_duel_menu_write_word_fields', '_resource_cost_frame', '_settlement_store_word_fields', '_settlement_write_byte_fields', '_special_action_shift_long', '_special_action_swap', 'execute_deployment_menu_fields'))
APPROVED.setdefault('services',set()).update(('mark_eligible_actor_for_retreat_fields', 'test_second_side_relative_total_shortfall_fields'))
APPROVED.setdefault((2, 'high_level_remaining_flows.business_highbank'),set()).update(('evaluate_anchor_position_order_fields', 'evaluate_contact_position_order_fields', 'evaluate_first_staging_position_fields', 'evaluate_guarded_alternate_anchor_order_fields', 'evaluate_guarded_first_region_order_fields', 'evaluate_guarded_first_staging_order_fields', 'evaluate_guarded_second_region_order_fields', 'evaluate_guarded_second_staging_order_fields', 'evaluate_guarded_small_force_region_tail_fields', 'evaluate_guarded_terrain_region_order_fields', 'evaluate_guarded_third_region_order_fields', 'evaluate_guarded_west_contact_order_fields', 'evaluate_readiness_contact_action_fields'))
DECLARATIONS.update({'_active_controller_fields': {'flow': 'entered = _map_presentation_legacy_render_fields(state, fields)\n'
                                       'returned = select_active_battle_controller_fields(state, entered)\n'
                                       'return _map_presentation_legacy_render_result(state, fields, returned)',
                               'returns': None,
                               'signature': 'state, fields'},
 '_city_map_entry_fields': {'flow': 'entered = _map_presentation_legacy_render_fields(state, fields)\n'
                                    'returned = render_city_map_entry_fields(state, entered)\n'
                                    'return _map_presentation_legacy_render_result(state, fields, returned)',
                            'returns': None,
                            'signature': 'state, fields'},
 '_city_map_fields': {'flow': 'entered = _map_presentation_legacy_render_fields(state, fields)\n'
                              'returned = render_city_map_entries_fields(state, entered)\n'
                              'return _map_presentation_legacy_render_result(state, fields, returned)',
                      'returns': None,
                      'signature': 'state, fields'},
 '_locate_map_sprite_fields': {'flow': 'entered = _map_presentation_legacy_render_fields(state, fields)\n'
                                       'returned = locate_map_packet_sprite_fields(state, entered)\n'
                                       'return _map_presentation_legacy_render_result(state, fields, returned)',
                               'returns': None,
                               'signature': 'state, fields'},
 '_map_marker_fields': {'flow': 'entered = _map_presentation_legacy_render_fields(state, fields)\n'
                                'returned = render_map_marker_positions_fields(state, entered)\n'
                                'return _map_presentation_legacy_render_result(state, fields, returned)',
                        'returns': None,
                        'signature': 'state, fields'},
 '_map_presentation_append_fields': {'flow': "view = frame.roster if carrier == 'roster' else frame.opponent\n"
                                             'frame = _map_presentation_emit_fields(state, frame, view.base, value, width, clear)\n'
                                             'return first_replace(frame, **{carrier: view.advance(width)})',
                                     'returns': 'FirstDeploymentFrame',
                                     'signature': 'state: SceneState, frame: FirstDeploymentFrame, carrier: str, value: int, width: int, '
                                                  'clear: bool=False'},
 '_map_presentation_arithmetic_fields': {'flow': 'frame, result = _movement_binary_flags(state, frame, low16(frame.carrier(carrier)), '
                                                 'value, 16, subtract)\n'
                                                 'return first_replace(frame, **{carrier: replace_word(frame.carrier(carrier), result)})',
                                         'returns': 'FirstDeploymentFrame',
                                         'signature': 'state: SceneState, frame: FirstDeploymentFrame, carrier: str, value: int, subtract: '
                                                      'bool=False'},
 '_map_presentation_bit_fields': {'flow': 'frame = _postbattle_bit_fields(frame, bool(value & mask))\n'
                                          'state.sr = state.sr & 65504 | frame.status\n'
                                          'return frame',
                                  'returns': 'FirstDeploymentFrame',
                                  'signature': 'state: SceneState, frame: FirstDeploymentFrame, value: int, mask: int'},
 '_map_presentation_call_fields': {'flow': "frame = _resource_cost_frame(state, frame, target)\nif target == 107598:\n    returned, category = _deployment_terrain_lookup(BattlePolicyMemory(state), frame, low16(frame.target_y), low16(frame.unit), continuation=continuation)\n    return returned\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = first_replace(frame, stack_cursor=stack)\nif target == 89662:\n    returned = render_selected_map_packet_fields(state, entered)\nelif target == 89736:\n    returned = select_map_packet_sprite_fields(state, entered)\nelif target == 89808:\n    returned = locate_map_packet_sprite_fields(state, entered)\nelif target == 89884:\n    returned = render_map_marker_positions_fields(state, entered)\nelif target == 90428:\n    returned = append_two_row_sequential_tiles_fields(state, entered)\nelif target == 90876:\n    returned = append_four_row_tile_columns_fields(state, entered)\nelif target == 90988:\n    returned = append_missing_city_queue_packets_fields(state, entered)\nelif target == 92676:\n    returned = render_city_map_entry_fields(state, entered)\nelif target == 97092:\n    returned = append_nearby_target_candidates_fields(state, entered)\nelif target == 97178:\n    returned = dispatch_target_eligibility_fields(state, entered)\nelif target == 82580:\n    returned = _map_presentation_scaled_terrain_fields(state, entered)\nelif target == 44048:\n    returned = append_live_command_sprite_fields(SpritePacketMemory(state), entered, reset_scroll=False, initialize_clip=True)\nelif target == 44872:\n    returned = refresh_gameplay_scene_fields(SceneRefreshMemory(state), entered)\nelif target == 198670:\n    returned = rounded_deployment_radial_distance_fields(BattlePolicyMemory(state), entered)\nelif target in (75530, 82594):\n    returned = execute_deployment_menu_fields(state, target, entered)\nelif target == 23228:\n    from .business_commands import present_current_command_prompt_frame_fields\n    returned = present_current_command_prompt_frame_fields(state, entered)\nelse:\n    raise MovementContinuationBoundary(target, entered, 'map presentation child lacks complete actual ABI')\nreturned = _resource_cost_frame(state, returned, target)\ntoken = returned.stack_cursor.long()\nif token != continuation:\n    raise MovementContinuationBoundary(token, returned, 'map presentation actual child return LONG changed')\nreturn first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))", 'returns': 'FirstDeploymentFrame', 'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int'},
 '_map_presentation_db_fields': {'flow': 'value = u16(low16(frame.carrier(carrier)) - 1)\n'
                                         'return (first_replace(frame, **{carrier: replace_word(frame.carrier(carrier), value)}), value != '
                                         '65535)',
                                 'returns': 'tuple',
                                 'signature': 'frame: FirstDeploymentFrame, carrier: str'},
 '_map_presentation_emit_fields': {'flow': 'if width == 1:\n'
                                           '    return _settlement_write_byte_fields(state, frame, state.table_at(address), value=value, '
                                           'clear=clear)\n'
                                           'if width == 2:\n'
                                           '    return _duel_menu_write_word_fields(state, frame, address, value, clear=clear)\n'
                                           'if width != 4 or clear:\n'
                                           "    raise ValueError('original map packet BYTE/WORD/LONG emission required')\n"
                                           'state.write(address, 4, value)\n'
                                           'return _movement_test_long(state, frame, value)',
                                   'returns': 'FirstDeploymentFrame',
                                   'signature': 'state: SceneState, frame: FirstDeploymentFrame, address: int, value: int, width: int, '
                                                'clear: bool=False'},
 '_map_presentation_legacy_map_fields': {'flow': 'checked_context(frame, MapPresentation, state)\n'
                                                 'return first_replace(FirstDeploymentFrame.unobserved(), target_x=frame.x, '
                                                 'target_y=frame.y, unit=frame.attributes, count=frame.tile, distance=frame.officer, '
                                                 'offset_x=frame.count, offset_y=frame.index, choice=frame.remaining, roster=frame.source, '
                                                 'candidates=frame.destination, controller=frame.packet)',
                                         'returns': 'FirstDeploymentFrame',
                                         'signature': 'state: SceneState, frame: MapPresentation'},
 '_map_presentation_legacy_map_result': {'flow': 'return replace(frame, x=returned.target_x, y=returned.target_y, '
                                                 'attributes=returned.unit, tile=returned.count, officer=returned.distance, '
                                                 'count=returned.offset_x, index=returned.offset_y, remaining=returned.choice, source=None '
                                                 'if returned.roster is None else returned.roster.cursor(), destination=None if '
                                                 'returned.candidates is None else returned.candidates.cursor(), packet=None if '
                                                 'returned.controller is None else returned.controller.cursor())',
                                         'returns': 'MapPresentation',
                                         'signature': 'state: SceneState, frame: MapPresentation, returned: FirstDeploymentFrame'},
 '_map_presentation_legacy_render_fields': {'flow': 'checked_render_fields(fields, state)\n'
                                                    'status = None\n'
                                                    'if all((type(value) is bool for value in (fields.carry, fields.zero, fields.negative, '
                                                    'fields.overflow))):\n'
                                                    '    status = state.sr & 16 | int(fields.carry) | (2 if fields.overflow else 0) | (4 '
                                                    'if fields.zero else 0) | (8 if fields.negative else 0)\n'
                                                    'return first_replace(FirstDeploymentFrame.unobserved(), target_x=fields.x, '
                                                    'target_y=fields.y, unit=fields.attributes, count=fields.tile, '
                                                    'distance=fields.officer, offset_x=fields.count, offset_y=fields.index, '
                                                    'choice=fields.remaining, roster=fields.source, candidates=fields.destination, '
                                                    'controller=fields.packet, stack_cursor=fields.stack_cursor, status=status)',
                                            'returns': 'FirstDeploymentFrame',
                                            'signature': 'state: SceneState, fields: RenderFields'},
 '_map_presentation_legacy_render_result': {'flow': 'return replace(fields, x=returned.target_x, y=returned.target_y, '
                                                    'attributes=returned.unit, tile=returned.count, officer=returned.distance, '
                                                    'count=returned.offset_x, index=returned.offset_y, remaining=returned.choice, '
                                                    'source=returned.roster, destination=returned.candidates, packet=returned.controller, '
                                                    'stack_cursor=returned.stack_cursor, carry=bool(returned.status & 1), '
                                                    'overflow=bool(returned.status & 2), zero=bool(returned.status & 4), '
                                                    'negative=bool(returned.status & 8))',
                                            'returns': 'RenderFields',
                                            'signature': 'state: SceneState, fields: RenderFields, returned: FirstDeploymentFrame'},
 '_map_presentation_legacy_search_fields': {'flow': 'checked_context(search, TargetSearch, state)\n'
                                                    'return first_replace(FirstDeploymentFrame.unobserved(), target_x=search.city, '
                                                    'target_y=search.metric_x, unit=search.metric_y, count=search.count, '
                                                    'distance=search.candidate, offset_x=search.origin_x, offset_y=search.origin_y, '
                                                    'choice=search.limit, roster=search.terrain, candidates=search.source, '
                                                    'controller=search.cities, scan=search.officers, opponent=search.destination, '
                                                    'scratch=search.blocked, status=state.sr & 31)',
                                            'returns': 'FirstDeploymentFrame',
                                            'signature': 'state: SceneState, search: TargetSearch'},
 '_map_presentation_legacy_search_result': {'flow': 'return replace(search, city=returned.target_x, metric_x=returned.target_y, '
                                                    'metric_y=returned.unit, count=returned.count, candidate=returned.distance, '
                                                    'origin_x=returned.offset_x, origin_y=returned.offset_y, limit=returned.choice, '
                                                    'terrain=returned.roster, source=None if returned.candidates is None else '
                                                    'returned.candidates.cursor(), cities=returned.controller, officers=returned.scan, '
                                                    'destination=None if returned.opponent is None else returned.opponent.cursor(), '
                                                    'blocked=returned.scratch)',
                                            'returns': 'TargetSearch',
                                            'signature': 'state: SceneState, search: TargetSearch, returned: FirstDeploymentFrame'},
 '_map_presentation_memory_arithmetic_fields': {'flow': 'frame, value = _movement_binary_flags(state, frame, state.read(address, 2), '
                                                        'amount, 16)\n'
                                                        'state.write(address, 2, value)\n'
                                                        'return frame',
                                                'returns': 'FirstDeploymentFrame',
                                                'signature': 'state: SceneState, frame: FirstDeploymentFrame, address: int, amount: int'},
 '_map_presentation_scaled_terrain_fields': {'flow': "frame = _movement_fixed_shift_word(state, frame, 'target_x', 4, True)\n"
                                                     "frame = _movement_fixed_shift_word(state, frame, 'target_y', 4, True)\n"
                                                     'frame = _map_presentation_call_fields(state, frame, 82594, 82588)\n'
                                                     "frame = _movement_fixed_shift_word(state, frame, 'target_x', 4)\n"
                                                     "return _movement_fixed_shift_word(state, frame, 'target_y', 4)",
                                             'returns': 'FirstDeploymentFrame',
                                             'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 '_map_presentation_tile_column_fields': {'flow': 'for index in range(len(tiles) - 1, 0, -1):\n'
                                                  '    frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + gap * '
                                                  'index), tiles[index], 2)\n'
                                                  "return _map_presentation_append_fields(state, frame, 'roster', tiles[0], 2)",
                                          'returns': 'FirstDeploymentFrame',
                                          'signature': 'state: SceneState, frame: FirstDeploymentFrame, gap: int, tiles: tuple'},
 '_select_map_sprite_fields': {'flow': 'entered = _map_presentation_legacy_render_fields(state, fields)\n'
                                       'returned = select_map_packet_sprite_fields(state, entered)\n'
                                       'return _map_presentation_legacy_render_result(state, fields, returned)',
                               'returns': None,
                               'signature': 'state, fields'},
 '_selected_map_packet_fields': {'flow': 'entered = _map_presentation_legacy_render_fields(state, fields)\n'
                                         'returned = render_selected_map_packet_fields(state, entered)\n'
                                         'return _map_presentation_legacy_render_result(state, fields, returned)',
                                 'returns': None,
                                 'signature': 'state, fields'},
 '_visible_map_packet_fields': {'flow': 'entered = _map_presentation_legacy_render_fields(state, fields)\n'
                                        'returned = render_visible_map_packets_fields(state, entered)\n'
                                        'return _map_presentation_legacy_render_result(state, fields, returned)',
                                'returns': None,
                                'signature': 'state, fields'},
 'append_city_currency_panel': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                        'returned = append_city_currency_panel_fields(state, entered)\n'
                                        'return _map_presentation_legacy_map_result(state, frame, returned)',
                                'returns': 'MapPresentation',
                                'signature': 'state: SceneState, frame: MapPresentation'},
 'append_city_currency_panel_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 89988)\n'
                                               'frame = first_replace(frame, '
                                               'roster=state.table_at(4294955264).cursor(state.read(4294963994, 2)))\n'
                                               'for tiles in ((12, 12), (49332, 49716), (50048, 54144)):\n'
                                               '    frame = _map_presentation_tile_column_fields(state, frame, 28, tiles)\n'
                                               "frame = _movement_move(state, frame, 'target_x', 9, 16)\n"
                                               'while True:\n'
                                               '    frame = _map_presentation_tile_column_fields(state, frame, 28, (50049, 54145))\n'
                                               "    frame, again = _map_presentation_db_fields(frame, 'target_x')\n"
                                               '    if not again:\n'
                                               '        break\n'
                                               'frame = _map_presentation_tile_column_fields(state, frame, 28, (52096, 56192))\n'
                                               'frame = first_replace(frame, roster=frame.roster.advance(28))\n'
                                               'for tiles in ((12, 12), (49460, 49588), (50050, 50050), (49157, 49158), (49159, 49160), '
                                               '(49153, 49153), (49153, 49153)):\n'
                                               '    frame = _map_presentation_tile_column_fields(state, frame, 28, tiles)\n'
                                               "frame = _movement_move(state, frame, 'target_x', state.read(4294964068, 2), 16)\n"
                                               "frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)\n"
                                               'frame = first_replace(frame, candidates=state.table_at(4294959260).cursor())\n'
                                               "frame = _movement_move_long(state, frame, 'target_x', "
                                               'frame.candidates.long(low16(frame.target_x)))\n'
                                               'frame = _map_presentation_emit_fields(state, frame, 4294964216, frame.target_x, 4)\n'
                                               "frame = _movement_move(state, frame, 'target_y', 50054, 16)\n"
                                               "frame = _movement_move(state, frame, 'unit', 49153, 16)\n"
                                               'frame = first_replace(frame, auxiliary=state.table_at(4294955776).cursor())\n'
                                               'frame = _map_presentation_call_fields(state, frame, 75530, 90164)\n'
                                               "frame = _movement_move(state, frame, 'target_x', 5, 16)\n"
                                               'frame = first_replace(frame, candidates=state.table_at(4294955776).cursor())\n'
                                               'while True:\n'
                                               '    value = frame.candidates.word()\n'
                                               '    frame = first_replace(frame, candidates=frame.candidates.advance(2))\n'
                                               '    frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + 28), '
                                               'value, 2)\n'
                                               "    frame = _map_presentation_append_fields(state, frame, 'roster', 49153, 2)\n"
                                               "    frame, again = _map_presentation_db_fields(frame, 'target_x')\n"
                                               '    if not again:\n'
                                               '        break\n'
                                               'frame = _map_presentation_tile_column_fields(state, frame, 28, (52098, 52098))\n'
                                               'frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + 28), 0, 2, '
                                               'True)\n'
                                               'return _map_presentation_memory_arithmetic_fields(state, frame, 4294963994, 112)',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'append_city_project_panel': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                       'returned = append_city_project_panel_fields(state, entered)\n'
                                       'return _map_presentation_legacy_map_result(state, frame, returned)',
                               'returns': 'MapPresentation',
                               'signature': 'state: SceneState, frame: MapPresentation'},
 'append_city_project_panel_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 90206)\n'
                                              'frame = first_replace(frame, '
                                              'roster=state.table_at(4294955264).cursor(state.read(4294963994, 2)))\n'
                                              'for tiles in ((14, 14, 14, 14), (50334, 50718, 50846, 50974), (50048, 50050, 50050, '
                                              '54144)):\n'
                                              '    frame = _map_presentation_tile_column_fields(state, frame, 32, tiles)\n'
                                              "frame = _movement_move(state, frame, 'target_x', 11, 16)\n"
                                              'while True:\n'
                                              '    frame = _map_presentation_tile_column_fields(state, frame, 32, (50049, 49153, 49153, '
                                              '54145))\n'
                                              "    frame, again = _map_presentation_db_fields(frame, 'target_x')\n"
                                              '    if not again:\n'
                                              '        break\n'
                                              'frame = _map_presentation_tile_column_fields(state, frame, 32, (52096, 52098, 52098, '
                                              '56192))\n'
                                              'frame = first_replace(frame, roster=frame.roster.advance(96))\n'
                                              'for tiles in ((14, 14), (50462, 50590), (50050, 50050)):\n'
                                              '    frame = _map_presentation_tile_column_fields(state, frame, 32, tiles)\n'
                                              "frame = _movement_move(state, frame, 'target_y', 49161, 16)\n"
                                              'frame = _map_presentation_call_fields(state, frame, 90428, 90374)\n'
                                              "frame = _movement_move(state, frame, 'target_x', 3, 16)\n"
                                              'while True:\n'
                                              '    frame = _map_presentation_tile_column_fields(state, frame, 32, (49153, 49153))\n'
                                              "    frame, again = _map_presentation_db_fields(frame, 'target_x')\n"
                                              '    if not again:\n'
                                              '        break\n'
                                              "frame = _movement_move(state, frame, 'target_y', 49169, 16)\n"
                                              'frame = _map_presentation_call_fields(state, frame, 90428, 90400)\n'
                                              'frame = _map_presentation_tile_column_fields(state, frame, 32, (52098, 52098))\n'
                                              'frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + 32), 0, 2, '
                                              'True)\n'
                                              'frame = _map_presentation_memory_arithmetic_fields(state, frame, 4294963994, 192)\n'
                                              'old = state.read(4294964133, 1)\n'
                                              'state.write(4294964133, 1, old | 32)\n'
                                              'return _map_presentation_bit_fields(state, frame, old, 32)',
                                      'returns': 'FirstDeploymentFrame',
                                      'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'append_current_city_value': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                       'returned = append_current_city_value_fields(state, entered)\n'
                                       'return _map_presentation_legacy_map_result(state, frame, returned)',
                               'returns': 'MapPresentation',
                               'signature': 'state: SceneState, frame: MapPresentation'},
 'append_current_city_value_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 90580)\n'
                                              'frame = first_replace(frame, '
                                              'roster=state.table_at(4294955264).cursor(state.read(4294963994, 2)))\n'
                                              'for value in (3, 50602):\n'
                                              "    frame = _map_presentation_append_fields(state, frame, 'roster', value, 2)\n"
                                              "frame = _movement_move(state, frame, 'target_x', state.read(4294964848, 2), 16)\n"
                                              "frame = _movement_move(state, frame, 'target_y', 50054, 16)\n"
                                              "frame = _movement_move(state, frame, 'unit', 0, 16)\n"
                                              'frame = first_replace(frame, auxiliary=state.table_at(4294955776).cursor())\n'
                                              'frame = _map_presentation_call_fields(state, frame, 75530, 90616)\n'
                                              'frame = first_replace(frame, auxiliary=state.table_at(4294955782).cursor())\n'
                                              "frame = _movement_move(state, frame, 'target_x', 0, 16)\n"
                                              "frame = _movement_move(state, frame, 'target_y', 2, 16)\n"
                                              'while True:\n'
                                              "    frame = _movement_move(state, frame, 'unit', frame.auxiliary.word(), 16)\n"
                                              '    frame = first_replace(frame, auxiliary=frame.auxiliary.advance(2))\n'
                                              '    if frame.status & 4:\n'
                                              '        frame = _movement_compare(state, frame, low16(frame.target_x), '
                                              'state.read(4294964122, 2), 16)\n'
                                              "        frame = _movement_move(state, frame, 'unit', 49153 if frame.status & 1 else 50054, "
                                              '16)\n'
                                              "    frame = _map_presentation_append_fields(state, frame, 'roster', low16(frame.unit), 2)\n"
                                              "    frame = _movement_add_word(state, frame, 'target_x', 1)\n"
                                              "    frame, again = _map_presentation_db_fields(frame, 'target_y')\n"
                                              '    if not again:\n'
                                              '        break\n'
                                              'frame = _map_presentation_emit_fields(state, frame, frame.roster.base, 0, 2, True)\n'
                                              'return _map_presentation_memory_arithmetic_fields(state, frame, 4294963994, 10)',
                                      'returns': 'FirstDeploymentFrame',
                                      'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'append_four_row_status_panel': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                          'returned = append_four_row_status_panel_fields(state, entered)\n'
                                          'return _map_presentation_legacy_map_result(state, frame, returned)',
                                  'returns': 'MapPresentation',
                                  'signature': 'state: SceneState, frame: MapPresentation'},
 'append_four_row_status_panel_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 90732)\n'
                                                 'frame = _map_presentation_call_fields(state, frame, 23228, 90738)\n'
                                                 'frame = first_replace(frame, '
                                                 'roster=state.table_at(4294955264).cursor(state.read(4294963994, 2)))\n'
                                                 'for tiles in ((10, 10, 10, 10), (49308, 49436, 49564, 49692), (50048, 50050, 50050, '
                                                 '54144)):\n'
                                                 '    frame = _map_presentation_tile_column_fields(state, frame, 24, tiles)\n'
                                                 'for count, tile, token in ((5, 49165, 90824), (1, 49225, 90836)):\n'
                                                 "    frame = _movement_move(state, frame, 'target_x', count, 16)\n"
                                                 "    frame = _movement_move(state, frame, 'target_y', tile, 16)\n"
                                                 '    frame = _map_presentation_call_fields(state, frame, 90876, token)\n'
                                                 'frame = _map_presentation_tile_column_fields(state, frame, 24, (52096, 52098, 52098, '
                                                 '56192))\n'
                                                 'frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + 72), 0, 2, '
                                                 'True)\n'
                                                 'frame = _duel_menu_write_word_fields(state, frame, 4294964132, state.read(4294964132, 2) '
                                                 '| 38912)\n'
                                                 'return _map_presentation_memory_arithmetic_fields(state, frame, 4294963994, 96)',
                                         'returns': 'FirstDeploymentFrame',
                                         'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'append_four_row_tile_columns': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                          'returned = append_four_row_tile_columns_fields(state, entered)\n'
                                          'return _map_presentation_legacy_map_result(state, frame, returned)',
                                  'returns': 'MapPresentation',
                                  'signature': 'state: SceneState, frame: MapPresentation'},
 'append_four_row_tile_columns_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 90876)\n'
                                                 'while True:\n'
                                                 '    frame = _map_presentation_emit_fields(state, frame, frame.roster.base, 50049, 2)\n'
                                                 '    frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + 24), '
                                                 'low16(frame.target_y), 2)\n'
                                                 "    frame = _movement_add_word(state, frame, 'target_y', 1)\n"
                                                 '    frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + 48), '
                                                 'low16(frame.target_y), 2)\n'
                                                 "    frame = _movement_add_word(state, frame, 'target_y', 1)\n"
                                                 '    frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + 72), '
                                                 '54145, 2)\n'
                                                 '    frame = first_replace(frame, roster=frame.roster.advance(2))\n'
                                                 "    frame, again = _map_presentation_db_fields(frame, 'target_x')\n"
                                                 '    if not again:\n'
                                                 '        return frame',
                                         'returns': 'FirstDeploymentFrame',
                                         'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'append_missing_city_queue_packets': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                               'returned = append_missing_city_queue_packets_fields(state, entered)\n'
                                               'return _map_presentation_legacy_map_result(state, frame, returned)',
                                       'returns': 'MapPresentation',
                                       'signature': 'state: SceneState, frame: MapPresentation'},
 'append_missing_city_queue_packets_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 90988)\n'
                                                      'frame = first_replace(frame, '
                                                      'roster=state.table_at(16723968).cursor(state.read(16726054, 2)), '
                                                      'candidates=state.table_at(4294961720).cursor(), '
                                                      'scan=state.table_at(4294960704).cursor())\n'
                                                      "frame = _movement_move(state, frame, 'target_x', 39, 16)\n"
                                                      'while True:\n'
                                                      '    frame = _movement_test(state, frame, '
                                                      'frame.candidates.byte(low16(frame.target_x)), 8)\n'
                                                      '    if not frame.status & 4:\n'
                                                      '        frame = first_replace(frame, controller=state.table_at(16723968).cursor())\n'
                                                      "        frame = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)\n"
                                                      "        frame = _movement_add_word(state, frame, 'unit', 1)\n"
                                                      '        found = False\n'
                                                      '        while True:\n'
                                                      "            frame = _movement_move(state, frame, 'target_y', "
                                                      'frame.controller.byte(), 8)\n'
                                                      '            frame = first_replace(frame, controller=frame.controller.advance(1))\n'
                                                      '            if frame.status & 8:\n'
                                                      '                break\n'
                                                      '            for index in range(3):\n'
                                                      "                frame = _movement_move(state, frame, 'target_y', "
                                                      'frame.controller.byte(), 8)\n'
                                                      '                frame = first_replace(frame, '
                                                      'controller=frame.controller.advance(1))\n'
                                                      '            frame = _movement_compare(state, frame, low8(frame.target_y), 128, 8)\n'
                                                      '            if frame.status & 4:\n'
                                                      '                value = frame.controller.byte()\n'
                                                      '                frame = first_replace(frame, '
                                                      'controller=frame.controller.advance(1))\n'
                                                      '                frame = _movement_compare(state, frame, low8(frame.unit), value, '
                                                      '8)\n'
                                                      '                if frame.status & 4:\n'
                                                      '                    found = True\n'
                                                      '                    break\n'
                                                      '            while True:\n'
                                                      '                value = frame.controller.byte()\n'
                                                      '                frame = first_replace(frame, '
                                                      'controller=frame.controller.advance(1))\n'
                                                      '                frame = _movement_test(state, frame, value, 8)\n'
                                                      '                if frame.status & 4:\n'
                                                      '                    break\n'
                                                      '        if not found:\n'
                                                      "            frame = _map_presentation_append_fields(state, frame, 'roster', 0, 1, "
                                                      'True)\n'
                                                      "            frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), "
                                                      '16)\n'
                                                      "            frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)\n"
                                                      "            frame = _map_presentation_append_fields(state, frame, 'roster', "
                                                      'frame.scan.byte(low16(frame.target_y), 1), 1)\n'
                                                      '            for value in (1, 128, low8(frame.unit)):\n'
                                                      "                frame = _map_presentation_append_fields(state, frame, 'roster', "
                                                      'value, 1)\n'
                                                      "            frame = _map_presentation_append_fields(state, frame, 'roster', 0, 1, "
                                                      'True)\n'
                                                      '            frame = _map_presentation_emit_fields(state, frame, frame.roster.base, '
                                                      '255, 1)\n'
                                                      '            frame = _map_presentation_memory_arithmetic_fields(state, frame, '
                                                      '16726054, 6)\n'
                                                      "    frame, again = _map_presentation_db_fields(frame, 'target_x')\n"
                                                      '    if not again:\n'
                                                      '        return frame',
                                              'returns': 'FirstDeploymentFrame',
                                              'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'append_nearby_target_candidates': {'flow': 'entered = _map_presentation_legacy_search_fields(state, search)\n'
                                             'returned = append_nearby_target_candidates_fields(state, entered)\n'
                                             'return _map_presentation_legacy_search_result(state, search, returned)',
                                     'returns': 'TargetSearch',
                                     'signature': 'state: SceneState, search: TargetSearch'},
 'append_nearby_target_candidates_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 97092)\n'
                                                    'while True:\n'
                                                    "    frame = _movement_move(state, frame, 'distance', frame.candidates.word(), 16)\n"
                                                    '    frame = first_replace(frame, candidates=frame.candidates.advance(2))\n'
                                                    '    if frame.status & 8:\n'
                                                    '        return frame\n'
                                                    '    frame = _movement_test(state, frame, frame.scratch.byte(low16(frame.distance)), '
                                                    '8)\n'
                                                    '    if not frame.status & 4:\n'
                                                    '        continue\n'
                                                    "    frame = _movement_move(state, frame, 'distance', low16(frame.distance) & 255, "
                                                    '16)\n'
                                                    "    frame = _movement_fixed_shift_word(state, frame, 'distance', 2)\n"
                                                    "    for carrier, displacement in (('target_y', 0), ('unit', 2)):\n"
                                                    '        frame = _movement_move(state, frame, carrier, '
                                                    'frame.scan.word(low16(frame.distance), displacement), 16)\n'
                                                    '        frame = _city_encounter_shift_word_fields(state, frame, carrier, 7, True)\n'
                                                    "    frame = _movement_fixed_shift_word(state, frame, 'distance', 2, True)\n"
                                                    '    frame = _map_presentation_call_fields(state, frame, 97178, 97128)\n'
                                                    '    if frame.status & 1:\n'
                                                    '        continue\n'
                                                    '    in_box = True\n'
                                                    "    for carrier, origin in (('target_y', frame.offset_x), ('unit', frame.offset_y)):\n"
                                                    '        frame = _map_presentation_arithmetic_fields(state, frame, carrier, '
                                                    'low16(origin), True)\n'
                                                    '        if frame.status & 1:\n'
                                                    '            frame, value = _movement_binary_flags(state, frame, 0, '
                                                    'low16(frame.carrier(carrier)), 16, True)\n'
                                                    '            frame = first_replace(frame, **{carrier: '
                                                    'replace_word(frame.carrier(carrier), value)})\n'
                                                    '        frame = _movement_compare(state, frame, low16(frame.carrier(carrier)), '
                                                    'low16(frame.count), 16)\n'
                                                    '        if not frame.status & 5:\n'
                                                    '            in_box = False\n'
                                                    '            break\n'
                                                    '        frame = _movement_multiply_word(state, frame, carrier, '
                                                    'low16(frame.carrier(carrier)))\n'
                                                    '    if not in_box:\n'
                                                    '        continue\n'
                                                    "    frame = _movement_arithmetic_long(state, frame, 'target_y', frame.unit)\n"
                                                    "    frame = _movement_move_long(state, frame, 'target_x', frame.target_y)\n"
                                                    '    frame = _map_presentation_call_fields(state, frame, 198670, 97168)\n'
                                                    '    frame = _movement_compare(state, frame, low16(frame.target_x), '
                                                    'low16(frame.count), 16)\n'
                                                    '    if frame.status & 5:\n'
                                                    "        frame = _map_presentation_append_fields(state, frame, 'opponent', "
                                                    'low16(frame.distance), 2)',
                                            'returns': 'FirstDeploymentFrame',
                                            'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'append_selected_long_value': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                        'returned = append_selected_long_value_fields(state, entered)\n'
                                        'return _map_presentation_legacy_map_result(state, frame, returned)',
                                'returns': 'MapPresentation',
                                'signature': 'state: SceneState, frame: MapPresentation'},
 'append_selected_long_value_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 90670)\n'
                                               'frame = first_replace(frame, '
                                               'roster=state.table_at(4294955264).cursor(state.read(4294963994, 2)))\n'
                                               'for value in (6, 50860):\n'
                                               "    frame = _map_presentation_append_fields(state, frame, 'roster', value, 2)\n"
                                               "frame = _movement_move_long(state, frame, 'target_x', state.read(4294964154, 4))\n"
                                               "frame = _movement_move(state, frame, 'target_y', 50054, 16)\n"
                                               "frame = _movement_move(state, frame, 'unit', 49153, 16)\n"
                                               'frame = first_replace(frame, auxiliary=state.table_at(4294955776).cursor())\n'
                                               'frame = _map_presentation_call_fields(state, frame, 75530, 90708)\n'
                                               'frame = first_replace(frame, candidates=state.table_at(4294955776).cursor())\n'
                                               "frame = _movement_move(state, frame, 'target_x', 2, 16)\n"
                                               'while True:\n'
                                               '    value = frame.candidates.long()\n'
                                               '    frame = first_replace(frame, candidates=frame.candidates.advance(4))\n'
                                               "    frame = _map_presentation_append_fields(state, frame, 'roster', value, 4)\n"
                                               "    frame, again = _map_presentation_db_fields(frame, 'target_x')\n"
                                               '    if not again:\n'
                                               '        break\n'
                                               'frame = _map_presentation_emit_fields(state, frame, frame.roster.base, 0, 2, True)\n'
                                               'return _map_presentation_memory_arithmetic_fields(state, frame, 4294963994, 16)',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'append_two_row_sequential_tiles': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                             'returned = append_two_row_sequential_tiles_fields(state, entered)\n'
                                             'return _map_presentation_legacy_map_result(state, frame, returned)',
                                     'returns': 'MapPresentation',
                                     'signature': 'state: SceneState, frame: MapPresentation'},
 'append_two_row_sequential_tiles_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 90428)\n'
                                                    "frame = _movement_move(state, frame, 'target_x', 3, 16)\n"
                                                    'while True:\n'
                                                    '    frame = _map_presentation_emit_fields(state, frame, frame.roster.base, '
                                                    'low16(frame.target_y), 2)\n'
                                                    "    frame = _movement_add_word(state, frame, 'target_y', 1)\n"
                                                    '    frame = _map_presentation_emit_fields(state, frame, u32(frame.roster.base + 32), '
                                                    'low16(frame.target_y), 2)\n'
                                                    "    frame = _movement_add_word(state, frame, 'target_y', 1)\n"
                                                    '    frame = first_replace(frame, roster=frame.roster.advance(2))\n'
                                                    "    frame, again = _map_presentation_db_fields(frame, 'target_x')\n"
                                                    '    if not again:\n'
                                                    '        return frame',
                                            'returns': 'FirstDeploymentFrame',
                                            'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'build_nearby_battle_targets': {'flow': 'entered = _map_presentation_legacy_search_fields(state, search)\n'
                                         'returned = build_nearby_battle_targets_fields(state, entered)\n'
                                         'return _map_presentation_legacy_search_result(state, search, returned)',
                                 'returns': 'TargetSearch',
                                 'signature': 'state: SceneState, search: TargetSearch'},
 'build_nearby_battle_targets_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 96926)\n'
                                                'state.set_status_word(9984)\n'
                                                'frame = first_replace(frame, status=0)\n'
                                                'frame = _duel_menu_write_word_fields(state, frame, 4294946688, 0, True)\n'
                                                "frame = _movement_move(state, frame, 'target_x', state.read(4294964134, 2), 16)\n"
                                                'frame = first_replace(frame, roster=state.table_at(4294951936).cursor())\n'
                                                "frame = _movement_move(state, frame, 'count', 0, 16)\n"
                                                "frame = _movement_move(state, frame, 'count', frame.roster.byte(low16(frame.target_x)), "
                                                '8)\n'
                                                "frame = _movement_move(state, frame, 'offset_x', low16(frame.count), 16)\n"
                                                "frame = _movement_fixed_shift_word(state, frame, 'count', 3)\n"
                                                "frame = _movement_add_word(state, frame, 'count', low16(frame.offset_x))\n"
                                                "frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)\n"
                                                'frame = first_replace(frame, scan=state.table_at(4294943056).cursor())\n'
                                                "for carrier, displacement in (('offset_x', 0), ('offset_y', 2)):\n"
                                                '    frame = _movement_move(state, frame, carrier, frame.scan.word(low16(frame.target_x), '
                                                'displacement), 16)\n'
                                                '    frame = _city_encounter_shift_word_fields(state, frame, carrier, 7, True)\n'
                                                'frame = first_replace(frame, roster=state.table_at(607720).cursor())\n'
                                                "frame = _movement_move(state, frame, 'distance', state.read(4294964874, 2), 16)\n"
                                                "frame = _movement_multiply_word(state, frame, 'distance', 2240)\n"
                                                'frame = first_replace(frame, roster=frame.roster.advance(frame.distance), '
                                                'opponent=state.table_at(4294944300).cursor())\n'
                                                'frame = _movement_compare(state, frame, state.read(4294964948, 2), 1, 16)\n'
                                                'skipped = False\n'
                                                'if frame.status & 4:\n'
                                                "    frame = _movement_move(state, frame, 'target_y', low16(frame.offset_x), 16)\n"
                                                "    frame = _movement_move(state, frame, 'unit', low16(frame.offset_y), 16)\n"
                                                '    frame = _map_presentation_call_fields(state, frame, 107598, 97012)\n'
                                                '    for terrain in (0, 4, 7):\n'
                                                '        frame = _movement_compare(state, frame, low8(frame.target_x), terrain, 8)\n'
                                                '        if frame.status & 4:\n'
                                                '            break\n'
                                                '    else:\n'
                                                '        frame = _duel_menu_write_word_fields(state, frame, 4294946688, 311)\n'
                                                '        skipped = True\n'
                                                'if not skipped:\n'
                                                '    frame = _map_presentation_bit_fields(state, frame, state.read(4294964951, 1), 2)\n'
                                                '    frame = first_replace(frame, candidates=state.table_at(4294944164 if frame.status & 4 '
                                                'else 4294944080).cursor(), scratch=state.table_at(16726978))\n'
                                                '    frame = _map_presentation_call_fields(state, frame, 97092, 97078)\n'
                                                'frame = _map_presentation_emit_fields(state, frame, frame.opponent.base, 65535, 2)\n'
                                                'return _map_presentation_call_fields(state, frame, 44872, 97090)',
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'locate_map_packet_sprite': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                      'returned = locate_map_packet_sprite_fields(state, entered)\n'
                                      'return _map_presentation_legacy_map_result(state, frame, returned)',
                              'returns': 'MapPresentation',
                              'signature': 'state: SceneState, frame: MapPresentation'},
 'locate_map_packet_sprite_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 89808)\n'
                                             'frame = _movement_compare(state, frame, state.read(4294964754, 2), 521, 16)\n'
                                             'selected = False\n'
                                             'if frame.status & 4:\n'
                                             '    frame = _movement_compare(state, frame, state.read(4294964066, 2), 6, 16)\n'
                                             '    if frame.status & 4:\n'
                                             "        frame = _movement_move(state, frame, 'target_x', state.read(16726964, 2), 16)\n"
                                             '        frame = _movement_compare(state, frame, low8(frame.target_x), '
                                             'frame.controller.byte(0, 13), 8)\n'
                                             '        selected = bool(frame.status & 4)\n'
                                             'if selected:\n'
                                             "    frame = _movement_move(state, frame, 'target_x', state.read(16726966, 2), 16)\n"
                                             "    frame = _movement_add_word(state, frame, 'target_x', 8)\n"
                                             "    frame = _movement_move(state, frame, 'target_y', state.read(16726968, 2), 16)\n"
                                             'else:\n'
                                             "    frame = _movement_move(state, frame, 'target_x', 0, 16)\n"
                                             "    frame = _movement_move(state, frame, 'target_x', frame.controller.byte(0, 1), 8)\n"
                                             "    frame = _movement_fixed_shift_word(state, frame, 'target_x', 4)\n"
                                             "    frame = _movement_add_word(state, frame, 'target_x', 8)\n"
                                             "    frame = _movement_move(state, frame, 'target_y', 0, 16)\n"
                                             "    frame = _movement_move(state, frame, 'target_y', frame.controller.byte(0, 2), 8)\n"
                                             "    frame = _movement_fixed_shift_word(state, frame, 'target_y', 4)\n"
                                             "return _movement_add_word(state, frame, 'target_y', 8)",
                                     'returns': 'FirstDeploymentFrame',
                                     'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'render_city_map_entries': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                     'returned = render_city_map_entries_fields(state, entered)\n'
                                     'return _map_presentation_legacy_map_result(state, frame, returned)',
                             'returns': 'MapPresentation',
                             'signature': 'state: SceneState, frame: MapPresentation'},
 'render_city_map_entries_complete': {'flow': 'observed = _render_from_tick(state, frame)\n'
                                              'entered = _map_presentation_legacy_render_fields(state, observed)\n'
                                              'returned = render_city_map_entries_fields(state, entered)\n'
                                              'return _render_to_tick(state, frame, _map_presentation_legacy_render_result(state, '
                                              'observed, returned))',
                                      'returns': 'MapTickFrame',
                                      'signature': 'state: SceneState, frame: MapTickFrame'},
 'render_city_map_entries_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 92586)\n'
                                            'frame = first_replace(frame, controller=state.table_at(4294954652).cursor())\n'
                                            "frame = _movement_move(state, frame, 'count', 39, 16)\n"
                                            'while True:\n'
                                            '    frame = _movement_test(state, frame, frame.controller.byte(), 8)\n'
                                            '    if not frame.status & 4:\n'
                                            '        frame = _map_presentation_bit_fields(state, frame, frame.controller.byte(), 16)\n'
                                            '        if frame.status & 4:\n'
                                            '            visible = True\n'
                                            "            for carrier, displacement, scroll, edge in (('target_x', 1, 4294963988, 240), "
                                            "('target_y', 2, 4294963992, 336)):\n"
                                            '                frame = _movement_move(state, frame, carrier, 0, 16)\n'
                                            '                frame = _movement_move(state, frame, carrier, frame.controller.byte(0, '
                                            'displacement), 8)\n'
                                            '                frame = _movement_fixed_shift_word(state, frame, carrier, 4)\n'
                                            "                frame = _movement_move(state, frame, 'unit', low16(frame.carrier(carrier)), "
                                            '16)\n'
                                            "                frame = _movement_add_word(state, frame, 'unit', 16)\n"
                                            "                frame = _map_presentation_arithmetic_fields(state, frame, 'unit', "
                                            'state.read(scroll, 2), True)\n'
                                            '                if frame.status & 1:\n'
                                            '                    visible = False\n'
                                            '                    break\n'
                                            '                frame = _movement_compare(state, frame, low16(frame.unit), edge, 16)\n'
                                            '                if not frame.status & 5:\n'
                                            '                    visible = False\n'
                                            '                    break\n'
                                            '            if visible:\n'
                                            '                frame = _map_presentation_call_fields(state, frame, 92676, 92668)\n'
                                            '    frame = first_replace(frame, controller=frame.controller.advance(-4))\n'
                                            "    frame, again = _map_presentation_db_fields(frame, 'count')\n"
                                            '    if not again:\n'
                                            '        return frame',
                                    'returns': 'FirstDeploymentFrame',
                                    'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'render_city_map_entry': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                   'returned = render_city_map_entry_fields(state, entered)\n'
                                   'return _map_presentation_legacy_map_result(state, frame, returned)',
                           'returns': 'MapPresentation',
                           'signature': 'state: SceneState, frame: MapPresentation'},
 'render_city_map_entry_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 92676)\n'
                                          'stack = frame.stack_cursor.advance(-4)\n'
                                          'stack.set_long(0, frame.count)\n'
                                          'frame = _movement_test_long(state, first_replace(frame, stack_cursor=stack), frame.count)\n'
                                          'frame = _movement_compare(state, frame, state.read(4294964754, 2), 522, 16)\n'
                                          'if frame.status & 4:\n'
                                          '    frame = _movement_compare(state, frame, state.read(4294964066, 2), 2, 16)\n'
                                          '    if frame.status & 4:\n'
                                          '        frame = _movement_compare(state, frame, low16(frame.count), state.read(4294954656, 2), '
                                          '16)\n'
                                          '        if frame.status & 4:\n'
                                          "            frame = _movement_move(state, frame, 'target_x', state.read(4294954660, 2), 16)\n"
                                          "            frame = _movement_move(state, frame, 'target_y', state.read(4294954662, 2), 16)\n"
                                          'frame = first_replace(frame, roster=state.table_at(92792).cursor())\n'
                                          'frame = _map_presentation_bit_fields(state, frame, state.read(4294964001, 1), 16)\n'
                                          'if frame.status & 4:\n'
                                          '    frame = first_replace(frame, roster=frame.roster.advance(8))\n'
                                          "saved = ('target_x', 'target_y', 'roster', 'controller')\n"
                                          'frame = _movement_save_longs(state, frame, saved)\n'
                                          "frame = _movement_add_word(state, frame, 'target_x', 8)\n"
                                          "frame = _movement_add_word(state, frame, 'target_y', 8)\n"
                                          'frame = _map_presentation_call_fields(state, frame, 82580, 92740)\n'
                                          'frame = _movement_restore_longs(state, frame, saved)\n'
                                          'frame = _movement_compare(state, frame, low16(frame.unit), 4, 16)\n'
                                          'if frame.status & 4:\n'
                                          '    frame = first_replace(frame, roster=frame.roster.advance(16))\n'
                                          "frame = _movement_add_word(state, frame, 'target_y', 8)\n"
                                          "frame = _movement_move(state, frame, 'unit', 0, 16)\n"
                                          'frame = _movement_test(state, frame, frame.controller.byte(), 8)\n'
                                          'if frame.status & 8:\n'
                                          "    frame = _movement_move(state, frame, 'unit', 2048, 16)\n"
                                          'frame = _duel_menu_write_word_fields(state, frame, 4294964746, state.read(4294963988, 2))\n'
                                          'frame = _duel_menu_write_word_fields(state, frame, 4294964750, state.read(4294963992, 2))\n'
                                          'frame = _map_presentation_call_fields(state, frame, 44048, 92788)\n'
                                          'restored = frame.stack_cursor.long()\n'
                                          'frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(4))\n'
                                          "return _movement_move_long(state, frame, 'count', restored)",
                                  'returns': 'FirstDeploymentFrame',
                                  'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'render_map_marker_positions': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                         'returned = render_map_marker_positions_fields(state, entered)\n'
                                         'return _map_presentation_legacy_map_result(state, frame, returned)',
                                 'returns': 'MapPresentation',
                                 'signature': 'state: SceneState, frame: MapPresentation'},
 'render_map_marker_positions_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 89884)\n'
                                                'frame = first_replace(frame, candidates=state.table_at(4294942464).cursor())\n'
                                                'while True:\n'
                                                "    frame = _movement_move(state, frame, 'target_x', frame.candidates.word(), 16)\n"
                                                '    frame = first_replace(frame, candidates=frame.candidates.advance(2))\n'
                                                '    if frame.status & 8:\n'
                                                '        return frame\n'
                                                "    frame = _movement_move(state, frame, 'target_y', frame.candidates.word(), 16)\n"
                                                '    frame = first_replace(frame, candidates=frame.candidates.advance(2))\n'
                                                '    visible = True\n'
                                                "    for carrier, scroll, edge in (('target_x', 4294963988, 240), ('target_y', 4294963992, "
                                                '336)):\n'
                                                "        frame = _movement_move(state, frame, 'unit', low16(frame.carrier(carrier)), 16)\n"
                                                "        frame = _movement_add_word(state, frame, 'unit', 16)\n"
                                                "        frame = _map_presentation_arithmetic_fields(state, frame, 'unit', "
                                                'state.read(scroll, 2), True)\n'
                                                '        if frame.status & 1:\n'
                                                '            visible = False\n'
                                                '            break\n'
                                                '        frame = _movement_compare(state, frame, low16(frame.unit), edge, 16)\n'
                                                '        if not frame.status & 5:\n'
                                                '            visible = False\n'
                                                '            break\n'
                                                '    if visible:\n'
                                                '        frame = first_replace(frame, roster=state.table_at(89962).cursor())\n'
                                                "        frame = _movement_move(state, frame, 'unit', 0, 16)\n"
                                                '        frame = _duel_menu_write_word_fields(state, frame, 4294964746, '
                                                'state.read(4294963988, 2))\n'
                                                '        frame = _duel_menu_write_word_fields(state, frame, 4294964750, '
                                                'state.read(4294963992, 2))\n'
                                                '        frame = _map_presentation_call_fields(state, frame, 44048, 89958)',
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'render_selected_map_packet': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                        'returned = render_selected_map_packet_fields(state, entered)\n'
                                        'return _map_presentation_legacy_map_result(state, frame, returned)',
                                'returns': 'MapPresentation',
                                'signature': 'state: SceneState, frame: MapPresentation'},
 'render_selected_map_packet_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 89662)\n'
                                               'frame = _movement_compare(state, frame, state.read(4294964076, 2), 2, 16)\n'
                                               'if frame.status & 4:\n'
                                               "    frame = _movement_move(state, frame, 'target_x', frame.controller.byte(0, 4), 8)\n"
                                               '    frame = _movement_compare(state, frame, low8(frame.target_x), state.read(4294964087, '
                                               '1), 8)\n'
                                               '    if frame.status & 4:\n'
                                               "        frame = _movement_move(state, frame, 'target_x', frame.controller.byte(), 8)\n"
                                               '        frame = _map_presentation_bit_fields(state, frame, frame.target_x, 16)\n'
                                               '        if frame.status & 4:\n'
                                               '            frame = _map_presentation_bit_fields(state, frame, state.read(4294964001, 1), '
                                               '4)\n'
                                               '            if not frame.status & 4:\n'
                                               '                return frame\n'
                                               'frame = _map_presentation_call_fields(state, frame, 89808, 89700)\n'
                                               'frame = _map_presentation_call_fields(state, frame, 89736, 89704)\n'
                                               "frame = _movement_move(state, frame, 'unit', 0, 16)\n"
                                               'frame = _movement_test(state, frame, frame.controller.byte(), 8)\n'
                                               'if frame.status & 8:\n'
                                               "    frame = _movement_move(state, frame, 'unit', 2048, 16)\n"
                                               'frame = _duel_menu_write_word_fields(state, frame, 4294964746, state.read(4294963988, 2))\n'
                                               'frame = _duel_menu_write_word_fields(state, frame, 4294964750, state.read(4294963992, 2))\n'
                                               'return _map_presentation_call_fields(state, frame, 44048, 89734)',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'render_visible_map_packets': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                        'returned = render_visible_map_packets_fields(state, entered)\n'
                                        'return _map_presentation_legacy_map_result(state, frame, returned)',
                                'returns': 'MapPresentation',
                                'signature': 'state: SceneState, frame: MapPresentation'},
 'render_visible_map_packets_complete': {'flow': 'observed = _render_from_tick(state, frame)\n'
                                                 'entered = _map_presentation_legacy_render_fields(state, observed)\n'
                                                 'returned = render_visible_map_packets_fields(state, entered)\n'
                                                 'return _render_to_tick(state, frame, _map_presentation_legacy_render_result(state, '
                                                 'observed, returned))',
                                         'returns': 'MapTickFrame',
                                         'signature': 'state: SceneState, frame: MapTickFrame'},
 'render_visible_map_packets_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 89574)\n'
                                               'frame = first_replace(frame, controller=state.table_at(4294938624).cursor())\n'
                                               'while True:\n'
                                               "    frame = _movement_move(state, frame, 'distance', frame.controller.byte(), 8)\n"
                                               '    if frame.status & 4:\n'
                                               '        return _map_presentation_call_fields(state, frame, 89884, 89660)\n'
                                               '    frame = _map_presentation_bit_fields(state, frame, frame.distance, 32)\n'
                                               '    if frame.status & 4:\n'
                                               '        visible = True\n'
                                               '        for displacement, scroll, edge in ((1, 4294963988, 240), (2, 4294963992, 336)):\n'
                                               "            frame = _movement_move(state, frame, 'offset_x', 0, 16)\n"
                                               "            frame = _movement_move(state, frame, 'offset_x', frame.controller.byte(0, "
                                               'displacement), 8)\n'
                                               "            frame = _movement_fixed_shift_word(state, frame, 'offset_x', 4)\n"
                                               "            frame = _movement_add_word(state, frame, 'offset_x', 16)\n"
                                               "            frame = _map_presentation_arithmetic_fields(state, frame, 'offset_x', "
                                               'state.read(scroll, 2), True)\n'
                                               '            if frame.status & 1:\n'
                                               '                visible = False\n'
                                               '                break\n'
                                               '            frame = _movement_compare(state, frame, low16(frame.offset_x), edge, 16)\n'
                                               '            if not frame.status & 1:\n'
                                               '                visible = False\n'
                                               '                break\n'
                                               '        if visible:\n'
                                               '            frame = _map_presentation_call_fields(state, frame, 89662, 89642)\n'
                                               "    frame = _movement_move(state, frame, 'offset_x', 0, 16)\n"
                                               "    frame = _movement_move(state, frame, 'offset_x', frame.controller.byte(), 8)\n"
                                               "    frame = _movement_move(state, frame, 'offset_x', low16(frame.offset_x) & 15, 16)\n"
                                               '    frame = first_replace(frame, controller=frame.controller.advance(13 + '
                                               's16(low16(frame.offset_x))))',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'select_active_battle_controller': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                             'returned = select_active_battle_controller_fields(state, entered)\n'
                                             'return _map_presentation_legacy_map_result(state, frame, returned)',
                                     'returns': 'MapPresentation',
                                     'signature': 'state: SceneState, frame: MapPresentation'},
 'select_active_battle_controller_complete': {'flow': 'observed = _render_from_tick(state, frame)\n'
                                                      'entered = _map_presentation_legacy_render_fields(state, observed)\n'
                                                      'returned = select_active_battle_controller_fields(state, entered)\n'
                                                      'return _render_to_tick(state, frame, _map_presentation_legacy_render_result(state, '
                                                      'observed, returned))',
                                              'returns': 'MapTickFrame',
                                              'signature': 'state: SceneState, frame: MapTickFrame'},
 'select_active_battle_controller_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 106862)\n'
                                                    'frame = _movement_compare(state, frame, state.read(4294964754, 2), 1031, 16)\n'
                                                    'if frame.status & 4:\n'
                                                    '    frame = _movement_test(state, frame, state.read(4294964066, 2), 16)\n'
                                                    '    if frame.status & 4:\n'
                                                    '        return frame\n'
                                                    '    for phase in (2, 4):\n'
                                                    '        frame = _movement_compare(state, frame, state.read(4294964066, 2), phase, '
                                                    '16)\n'
                                                    '        if frame.status & 4:\n'
                                                    '            return frame\n'
                                                    "frame = _movement_move(state, frame, 'target_x', state.read(4294964876, 2), 16)\n"
                                                    "frame = _movement_move(state, frame, 'target_y', state.read(4294964878, 2), 16)\n"
                                                    'frame = _map_presentation_bit_fields(state, frame, state.read(4294964951, 1), 2)\n'
                                                    'if not frame.status & 4:\n'
                                                    '    frame = first_replace(frame, target_x=frame.target_y, target_y=frame.target_x)\n'
                                                    'frame = _movement_compare(state, frame, low16(frame.target_x), state.read(4294964858, '
                                                    '2), 16)\n'
                                                    'if frame.status & 4:\n'
                                                    '    return frame\n'
                                                    'frame = _movement_compare(state, frame, low16(frame.target_x), state.read(4294964860, '
                                                    '2), 16)\n'
                                                    'if frame.status & 4:\n'
                                                    '    return _duel_menu_write_word_fields(state, frame, 4294964738, '
                                                    'state.read(4294964740, 2))\n'
                                                    'frame = _movement_compare(state, frame, low16(frame.target_x), state.read(4294964862, '
                                                    '2), 16)\n'
                                                    'if frame.status & 4:\n'
                                                    '    frame = _movement_compare(state, frame, low16(frame.target_y), '
                                                    'state.read(4294964860, 2), 16)\n'
                                                    'else:\n'
                                                    '    frame = _movement_compare(state, frame, low16(frame.target_y), '
                                                    'state.read(4294964858, 2), 16)\n'
                                                    'if frame.status & 4:\n'
                                                    '    return frame\n'
                                                    'return _duel_menu_write_word_fields(state, frame, 4294964738, state.read(4294964740, '
                                                    '2))',
                                            'returns': 'FirstDeploymentFrame',
                                            'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'select_map_packet_sprite': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                      'returned = select_map_packet_sprite_fields(state, entered)\n'
                                      'return _map_presentation_legacy_map_result(state, frame, returned)',
                              'returns': 'MapPresentation',
                              'signature': 'state: SceneState, frame: MapPresentation'},
 'select_map_packet_sprite_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 89736)\n'
                                             'frame = first_replace(frame, roster=state.table_at(89784).cursor())\n'
                                             'frame = _map_presentation_bit_fields(state, frame, state.read(4294964001, 1), 16)\n'
                                             'if not frame.status & 4:\n'
                                             '    frame = first_replace(frame, roster=frame.roster.advance(8))\n'
                                             "saved = ('target_x', 'target_y', 'roster', 'controller')\n"
                                             'frame = _movement_save_longs(state, frame, saved)\n'
                                             'frame = _map_presentation_call_fields(state, frame, 82580, 89764)\n'
                                             'frame = _movement_restore_longs(state, frame, saved)\n'
                                             'frame = _movement_compare(state, frame, low16(frame.unit), 4, 16)\n'
                                             'if frame.status & 4:\n'
                                             '    frame = first_replace(frame, roster=state.table_at(89800).cursor())\n'
                                             'return frame',
                                     'returns': 'FirstDeploymentFrame',
                                     'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'sort_map_packet_queue': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                   'returned = sort_map_packet_queue_fields(state, entered)\n'
                                   'return _map_presentation_legacy_map_result(state, frame, returned)',
                           'returns': 'MapPresentation',
                           'signature': 'state: SceneState, frame: MapPresentation'},
 'sort_map_packet_queue_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 90906)\n'
                                          'frame = _map_presentation_call_fields(state, frame, 90988, 90910)\n'
                                          'frame = first_replace(frame, roster=state.table_at(16723968).cursor())\n'
                                          'frame = _duel_menu_write_word_fields(state, frame, 16726450, 0, True)\n'
                                          'while True:\n'
                                          '    value = frame.roster.byte()\n'
                                          '    frame = first_replace(frame, roster=frame.roster.advance(1))\n'
                                          '    frame = _movement_test(state, frame, value, 8)\n'
                                          '    if frame.status & 8:\n'
                                          '        return _duel_menu_write_word_fields(state, frame, 16726962, 0, True)\n'
                                          "    for carrier in ('target_x', 'target_y'):\n"
                                          '        frame = _movement_move(state, frame, carrier, frame.roster.byte(), 8)\n'
                                          '        frame = first_replace(frame, roster=frame.roster.advance(1))\n'
                                          '    frame = first_replace(frame, candidates=state.table_at(16726450).cursor())\n'
                                          '    while True:\n'
                                          '        frame = _movement_compare(state, frame, low8(frame.target_y), frame.candidates.byte(), '
                                          '8)\n'
                                          '        if not frame.status & 5:\n'
                                          '            break\n'
                                          '        frame = first_replace(frame, candidates=frame.candidates.advance(2))\n'
                                          '    frame = first_replace(frame, controller=state.table_at(frame.candidates.base).cursor())\n'
                                          '    while True:\n'
                                          '        frame = first_replace(frame, controller=frame.controller.advance(2))\n'
                                          '        frame = _movement_test(state, frame, frame.controller.byte(), 8)\n'
                                          '        if frame.status & 4:\n'
                                          '            break\n'
                                          '    frame = _map_presentation_emit_fields(state, frame, u32(frame.controller.base + 2), 0, 1, '
                                          'True)\n'
                                          '    frame = first_replace(frame, scan=state.table_at(u32(frame.controller.base + 2)).cursor())\n'
                                          '    while True:\n'
                                          '        for index in range(2):\n'
                                          '            frame = first_replace(frame, controller=frame.controller.advance(-1), '
                                          'scan=frame.scan.advance(-1))\n'
                                          '            frame = _map_presentation_emit_fields(state, frame, frame.scan.base, '
                                          'frame.controller.byte(), 1)\n'
                                          '        frame = _movement_compare_address(state, frame, frame.candidates.base, '
                                          'frame.controller.base)\n'
                                          '        if not frame.status & 1:\n'
                                          '            break\n'
                                          '    frame = _map_presentation_emit_fields(state, frame, frame.candidates.base, '
                                          'low8(frame.target_y), 1)\n'
                                          '    frame = _map_presentation_emit_fields(state, frame, u32(frame.candidates.base + 1), '
                                          'low8(frame.target_x), 1)\n'
                                          '    while True:\n'
                                          '        value = frame.roster.byte()\n'
                                          '        frame = first_replace(frame, roster=frame.roster.advance(1))\n'
                                          '        frame = _movement_test(state, frame, value, 8)\n'
                                          '        if frame.status & 4:\n'
                                          '            break',
                                  'returns': 'FirstDeploymentFrame',
                                  'signature': 'state: SceneState, frame: FirstDeploymentFrame'}})

# D50 precise current source admission/DECL; ordinary lowerers unchanged.
APPROVED.setdefault((2, 'high_level_gameplay_flow.business_services'),set()).update(('clear_video_sprite_plane_fields', 'enqueue_sound_command_fields', 'initialize_video_registers_and_planes_fields'))
APPROVED.setdefault((2, 'high_level_scene_flows.business_scene'),set()).update(('_glyph_shift_long_fields', 'darken_palette_fields'))
APPROVED.setdefault('business_scene_support',set()).update(('_controller_setup_child_fields',))
DECLARATIONS.pop('_update_setup_option',None)
DECLARATIONS.pop('_setup_sprites',None)
DECLARATIONS.update({'_setup_advance_plane_row_call_fields': {'flow': 'if continuation not in (177158, 177194):\n'
                                                  "    raise ValueError('actual plane row tokens required')\n"
                                                  'return _setup_call_fields(state, frame, 177200, continuation)',
                                          'returns': 'FirstDeploymentFrame',
                                          'signature': 'state: SceneState, frame: FirstDeploymentFrame, continuation: Long'},
 '_setup_advance_plane_row_fields': {'flow': "frame = _map_presentation_arithmetic_fields(state, frame, 'distance', 1)\n"
                                             'frame = _movement_compare(state, frame, low8(frame.distance), 32, 8)\n'
                                             'if frame.status & 1:\n'
                                             '    return frame\n'
                                             'stride = frame.offset_x - 4294967296 if frame.offset_x & 2147483648 else frame.offset_x\n'
                                             'frame = first_replace(frame, candidates=frame.candidates.advance(stride))\n'
                                             "frame = _movement_move(state, frame, 'target_x', low16(frame.candidates.base), 16)\n"
                                             'frame = _setup_call_fields(state, frame, 177222, 177218)\n'
                                             "return _movement_move_long(state, frame, 'distance', 0)",
                                     'returns': 'FirstDeploymentFrame',
                                     'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 '_setup_asl_word_fields': {'flow': "if carrier not in ('target_x', 'target_y', 'unit', 'offset_x') or amount not in (1, 2, 8):\n"
                                    "    raise ValueError('actual setup ASL.W role/count required')\n"
                                    'original = frame.carrier(carrier)\n'
                                    'value = low16(original)\n'
                                    'overflow = 0\n'
                                    'for bit in range(amount):\n'
                                    '    frame, value = _movement_binary_flags(state, frame, value, value, 16)\n'
                                    '    overflow |= frame.status & 2\n'
                                    'status = frame.status | overflow\n'
                                    'state.sr = state.sr & 65504 | status\n'
                                    'return first_replace(frame, status=status, **{carrier: replace_word(original, value)})',
                            'returns': 'FirstDeploymentFrame',
                            'signature': 'state: SceneState, frame: FirstDeploymentFrame, carrier: str, amount: int'},
 '_setup_call_fields': {'flow': 'frame = _resource_cost_frame(state, frame, target)\n'
                                'stack = frame.stack_cursor.advance(-4)\n'
                                'stack.set_long(0, continuation)\n'
                                'entered = first_replace(frame, stack_cursor=stack)\n'
                                'if target == 44040:\n'
                                '    result = append_live_command_sprite_fields(SpritePacketMemory(state), entered, reset_scroll=False, '
                                'initialize_clip=False)\n'
                                'elif target == 56998:\n'
                                '    result = darken_palette_fields(SceneRefreshMemory(state), entered)\n'
                                'elif target == 26830:\n'
                                '    result = clear_video_sprite_plane_fields(SceneRefreshMemory(state), entered)\n'
                                'elif target == 26662:\n'
                                '    result = initialize_video_registers_and_planes_fields(SceneRefreshMemory(state), entered)\n'
                                'elif target == 32906:\n'
                                '    result = enqueue_sound_command_fields(SceneRefreshMemory(state), entered)\n'
                                'elif target == 176154:\n'
                                '    result = cycle_setup_option_fields(state, entered)\n'
                                'elif target == 176010:\n'
                                '    result = render_current_setup_option_fields(state, entered)\n'
                                'elif target in (177092, 177108, 177200):\n'
                                '    result = _setup_plane_rows_fields(state, entered, target)\n'
                                'elif target == 177222:\n'
                                '    result = write_setup_video_address_fields(state, entered)\n'
                                'elif target in (175450, 175496, 175544, 175592, 175640, 176056, 176102, 176478):\n'
                                '    children = {175450: update_first_setup_option_fields, 175496: update_second_setup_option_fields, '
                                '175544: update_third_setup_option_fields, 175592: update_fourth_setup_option_fields, 175640: '
                                'update_setup_player_choices_fields, 176056: advance_setup_reveal_fields, 176102: '
                                'advance_setup_dismissal_fields, 176478: initialize_setup_video_fields}\n'
                                '    result = children[target](state, entered)\n'
                                'else:\n'
                                '    from .business_scene_support import _controller_setup_child_fields\n'
                                '    result = _controller_setup_child_fields(state, entered, target)\n'
                                'result = _resource_cost_frame(state, result, target)\n'
                                'token = result.stack_cursor.long()\n'
                                'if token != continuation:\n'
                                "    raise MovementContinuationBoundary(token, result, 'actual setup child return LONG changed')\n"
                                'state.sr = state.sr & 65504 | result.status\n'
                                'return first_replace(result, stack_cursor=result.stack_cursor.advance(4))',
                        'returns': 'FirstDeploymentFrame',
                        'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long, continuation: Long'},
 '_setup_change_word_fields': {'flow': 'frame, value = _movement_binary_flags(state, frame, state.read(address, 2), amount, 16, subtract)\n'
                                       'state.write(address, 2, value)\n'
                                       'return frame',
                               'returns': 'FirstDeploymentFrame',
                               'signature': 'state: SceneState, frame: FirstDeploymentFrame, address: Long, amount: Word, subtract: '
                                            'bool=False'},
 '_setup_compare_memory_fields': {'flow': 'return _movement_compare(state, frame, state.read(address, width // 8), source, width)',
                                  'returns': 'FirstDeploymentFrame',
                                  'signature': 'state: SceneState, frame: FirstDeploymentFrame, address: Long, source: Word, width: '
                                               'int=16'},
 '_setup_coordinate_high_byte_fields': {'flow': 'original = frame.target_x\n'
                                                "frame = _movement_fixed_shift_word(state, frame, 'target_x', 8, True)\n"
                                                'value = u16(s16(low16(original)) >> 8)\n'
                                                'status = frame.status & 17 | (8 if value & 32768 else 0) | (4 if value == 0 else 0)\n'
                                                'state.sr = state.sr & 65504 | status\n'
                                                'return first_replace(frame, target_x=replace_word(original, value), status=status)',
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 '_setup_legacy_entry_fields': {'flow': 'checked_context(values, SetupValues, state)\n'
                                        'return first_replace(FirstDeploymentFrame.unobserved(), target_x=values.value, '
                                        'target_y=values.option, unit=values.position, count=values.attributes, distance=values.rows, '
                                        'offset_x=values.tile, offset_y=values.stride, choice=values.selector, roster=values.source, '
                                        'candidates=values.destination, status=state.sr & 31)',
                                'returns': 'FirstDeploymentFrame',
                                'signature': 'state: SceneState, values: SetupValues'},
 '_setup_legacy_result_fields': {'flow': 'return replace(values, value=frame.target_x, option=frame.target_y, position=frame.unit, '
                                         'attributes=frame.count, rows=frame.distance, tile=frame.offset_x, stride=frame.offset_y, '
                                         'selector=frame.choice, source=frame.roster, destination=frame.candidates)',
                                 'returns': 'SetupValues',
                                 'signature': 'state: SceneState, values: SetupValues, frame: FirstDeploymentFrame'},
 '_setup_palette_transition_fields': {'flow': 'if (counter, packet, token, dismiss) not in ((16740416, 177262, 176094, False), (16740418, '
                                              '177262, 176146, True)):\n'
                                              "    raise ValueError('closed actual setup fade phases required')\n"
                                              'if dismiss:\n'
                                              '    frame = _movement_test(state, frame, state.read(16740414, 2), 16)\n'
                                              '    if frame.status & 4:\n'
                                              '        return frame\n'
                                              'frame = _setup_compare_memory_fields(state, frame, counter, 16)\n'
                                              'if not frame.status & 1:\n'
                                              '    return frame\n'
                                              'if dismiss:\n'
                                              "    frame = _movement_move(state, frame, 'target_x', state.read(counter, 2), 16)\n"
                                              'else:\n'
                                              "    frame = _movement_move(state, frame, 'target_x', 15, 16)\n"
                                              "    frame = _map_presentation_arithmetic_fields(state, frame, 'target_x', "
                                              'state.read(counter, 2), True)\n'
                                              "frame = _movement_move(state, frame, 'target_y', 64, 16)\n"
                                              'frame = first_replace(frame, roster=state.table_at(packet).cursor())\n'
                                              'frame = _setup_call_fields(state, frame, 56998, token)\n'
                                              'return _setup_change_word_fields(state, frame, counter, 1)',
                                      'returns': 'FirstDeploymentFrame',
                                      'signature': 'state: SceneState, frame: FirstDeploymentFrame, counter: Long, packet: Long, token: '
                                                   'Long, dismiss: bool'},
 '_setup_plane_legacy_entry_fields': {'flow': 'checked_context(plane, SetupPlane, state)\n'
                                              'return first_replace(FirstDeploymentFrame.unobserved(), target_x=plane.command, '
                                              'target_y=plane.marker, unit=plane.tile, count=plane.repeat_count, distance=plane.column, '
                                              'offset_x=plane.row_stride, roster=plane.source, '
                                              'candidates=state.table_at(plane.video_address.carrier).cursor(), status=state.sr & 31)',
                                      'returns': 'FirstDeploymentFrame',
                                      'signature': 'state: SceneState, plane: SetupPlane'},
 '_setup_plane_legacy_result_fields': {'flow': 'return replace(plane, command=frame.target_x, marker=frame.target_y, tile=frame.unit, '
                                               'repeat_count=frame.count, column=frame.distance, row_stride=frame.offset_x, '
                                               'source=frame.roster, video_address=VideoPlaneAddress(frame.candidates.base))',
                                       'returns': 'SetupPlane',
                                       'signature': 'state: SceneState, plane: SetupPlane, frame: FirstDeploymentFrame'},
 '_setup_plane_rows_fields': {'flow': "if entry not in (177092, 177108, 177200):\n    raise ValueError('actual plane entry required')\nframe = _resource_cost_frame(state, frame, entry)\nif entry == 177200:\n    return _setup_advance_plane_row_fields(state, frame)\nif entry == 177092:\n    frame = _setup_write_fields(state, frame, 16740360, 32768)\n    frame = _setup_write_fields(state, frame, 16740364, 65535)\nframe = _setup_write_fields(state, frame, 12582916, 36610)\nframe = _movement_move(state, frame, 'target_x', low16(frame.candidates.base), 16)\nframe = _setup_call_fields(state, frame, 177222, 177122)\nframe = _movement_move_long(state, frame, 'distance', 0)\nframe = _movement_move(state, frame, 'target_y', frame.roster.byte(), 8)\nframe = first_replace(frame, roster=frame.roster.advance(1))\nwhile True:\n    frame = _movement_move(state, frame, 'unit', frame.roster.byte(), 8)\n    frame = first_replace(frame, roster=frame.roster.advance(1))\n    frame = _movement_compare(state, frame, low8(frame.target_y), low8(frame.unit), 8)\n    if frame.status & 4:\n        frame = _movement_move_long(state, frame, 'count', 0)\n        frame = _movement_move(state, frame, 'count', frame.roster.byte(), 8)\n        frame = first_replace(frame, roster=frame.roster.advance(1))\n        if frame.status & 4:\n            return frame\n        frame = _movement_move(state, frame, 'unit', frame.roster.byte(), 8)\n        frame = first_replace(frame, roster=frame.roster.advance(1))\n        frame = _setup_asl_word_fields(state, frame, 'unit', 8)\n        frame = _movement_move(state, frame, 'unit', frame.roster.byte(), 8)\n        frame = first_replace(frame, roster=frame.roster.advance(1))\n        while True:\n            frame = _movement_move(state, frame, 'unit', low16(frame.unit) | state.read(16740360, 2), 16)\n            frame = _movement_move(state, frame, 'unit', low16(frame.unit) & state.read(16740364, 2), 16)\n            frame = _setup_write_fields(state, frame, 12582912, low16(frame.unit))\n            frame = _setup_advance_plane_row_call_fields(state, frame, 177194)\n            frame, again = _map_presentation_db_fields(frame, 'count')\n            if not again:\n                break\n    else:\n        frame = _setup_asl_word_fields(state, frame, 'unit', 8)\n        frame = _movement_move(state, frame, 'unit', frame.roster.byte(), 8)\n        frame = first_replace(frame, roster=frame.roster.advance(1))\n        frame = _movement_move(state, frame, 'unit', low16(frame.unit) | state.read(16740360, 2), 16)\n        frame = _movement_move(state, frame, 'unit', low16(frame.unit) & state.read(16740364, 2), 16)\n        frame = _setup_write_fields(state, frame, 12582912, low16(frame.unit))\n        frame = _setup_advance_plane_row_call_fields(state, frame, 177158)", 'returns': 'FirstDeploymentFrame', 'signature': 'state: SceneState, frame: FirstDeploymentFrame, entry: Long'},
 '_setup_transfer_longs_fields': {'flow': "if destination_carrier not in ('auxiliary', 'candidates') or type(increment_destination) is not "
                                          'bool:\n'
                                          "    raise ValueError('actual setup LONG transfer destination required')\n"
                                          'while True:\n'
                                          '    value = frame.roster.long()\n'
                                          '    frame = first_replace(frame, roster=frame.roster.advance(4))\n'
                                          "    destination = frame.auxiliary if destination_carrier == 'auxiliary' else frame.candidates\n"
                                          '    frame = _setup_write_fields(state, frame, destination.base, value, 4)\n'
                                          '    if increment_destination:\n'
                                          '        frame = first_replace(frame, **{destination_carrier: destination.advance(4)})\n'
                                          "    frame, again = _map_presentation_db_fields(frame, 'target_x')\n"
                                          '    if not again:\n'
                                          '        return frame',
                                  'returns': 'FirstDeploymentFrame',
                                  'signature': 'state: SceneState, frame: FirstDeploymentFrame, destination_carrier: str, '
                                               'increment_destination: bool'},
 '_setup_update_option_fields': {'flow': 'valid = ((0, 16740390, 2, 176260, 175474, 175492), (1, 16740388, 2, 176310, 175522, 175540), (2, '
                                         '16740392, 1, 176360, 175570, 175588), (3, 16740394, 2, 176260, 175618, 175636))\n'
                                         'if (option, address, maximum, packet, cycle_token, render_token) not in valid:\n'
                                         "    raise ValueError('closed actual four option tails required')\n"
                                         'frame = _movement_test(state, frame, state.read(16740386, 2), 16) if option == 0 else '
                                         '_setup_compare_memory_fields(state, frame, 16740386, option)\n'
                                         'if not frame.status & 4:\n'
                                         '    return frame\n'
                                         "frame = _movement_move(state, frame, 'offset_x', state.read(address, 2), 16)\n"
                                         "frame = _movement_move(state, frame, 'offset_y', maximum, 16)\n"
                                         'frame = _setup_call_fields(state, frame, 176154, cycle_token)\n'
                                         'frame = _setup_write_fields(state, frame, address, low16(frame.offset_x))\n'
                                         'frame = first_replace(frame, roster=state.table_at(packet).cursor())\n'
                                         'return _setup_call_fields(state, frame, 176010, render_token)',
                                 'returns': 'FirstDeploymentFrame',
                                 'signature': 'state: SceneState, frame: FirstDeploymentFrame, option: int, address: Long, maximum: Word, '
                                              'packet: Long, cycle_token: Long, render_token: Long'},
 '_setup_write_fields': {'flow': 'if width not in (1, 2, 4) or type(clear) is not bool:\n'
                                 "    raise ValueError('closed setup memory width required')\n"
                                 'value &= (1 << width * 8) - 1\n'
                                 'if clear:\n'
                                 '    state.read(address, width)\n'
                                 'state.write(address, width, value)\n'
                                 'return _movement_test_long(state, frame, value) if width == 4 else _movement_test(state, frame, value, '
                                 'width * 8)',
                         'returns': 'FirstDeploymentFrame',
                         'signature': 'state: SceneState, frame: FirstDeploymentFrame, address: Long, value: Long, width: int=2, clear: '
                                      'bool=False'},
 'advance_setup_dismissal': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                     'returned = advance_setup_dismissal_fields(state, entered)\n'
                                     'return _setup_legacy_result_fields(state, values, returned)',
                             'returns': 'SetupValues',
                             'signature': 'state: SceneState, values: SetupValues'},
 'advance_setup_dismissal_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 176102)\n'
                                            'return _setup_palette_transition_fields(state, frame, 16740418, 177262, 176146, True)',
                                    'returns': 'FirstDeploymentFrame',
                                    'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'advance_setup_plane_row': {'flow': 'entered = _setup_plane_legacy_entry_fields(state, plane)\n'
                                     'returned = advance_setup_plane_row_fields(state, entered)\n'
                                     'return _setup_plane_legacy_result_fields(state, plane, returned)',
                             'returns': 'SetupPlane',
                             'signature': 'state: SceneState, plane: SetupPlane'},
 'advance_setup_plane_row_fields': {'flow': 'return _setup_plane_rows_fields(state, frame, 177200)',
                                    'returns': 'FirstDeploymentFrame',
                                    'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'advance_setup_reveal': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                  'returned = advance_setup_reveal_fields(state, entered)\n'
                                  'return _setup_legacy_result_fields(state, values, returned)',
                          'returns': 'SetupValues',
                          'signature': 'state: SceneState, values: SetupValues'},
 'advance_setup_reveal_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 176056)\n'
                                         'return _setup_palette_transition_fields(state, frame, 16740416, 177262, 176094, False)',
                                 'returns': 'FirstDeploymentFrame',
                                 'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'cycle_setup_option': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                'returned = cycle_setup_option_fields(state, entered)\n'
                                'return _setup_legacy_result_fields(state, values, returned)',
                        'returns': 'SetupValues',
                        'signature': 'state: SceneState, values: SetupValues'},
 'cycle_setup_option_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 176154)\n'
                                       'frame = _map_presentation_bit_fields(state, frame, state.read(4294964739, 1), 1)\n'
                                       'if not frame.status & 4:\n'
                                       '    frame = _movement_test(state, frame, low16(frame.offset_x), 16)\n'
                                       '    if frame.status & 4:\n'
                                       "        return _movement_move(state, frame, 'offset_x', low16(frame.offset_y), 16)\n"
                                       "    frame = _map_presentation_arithmetic_fields(state, frame, 'offset_x', 1, True)\n"
                                       '    if frame.status & 4:\n'
                                       '        return frame\n'
                                       'frame = _map_presentation_bit_fields(state, frame, state.read(4294964739, 1), 2)\n'
                                       'if frame.status & 4:\n'
                                       '    return frame\n'
                                       'frame = _movement_compare(state, frame, low16(frame.offset_x), low16(frame.offset_y), 16)\n'
                                       'if frame.status & 4:\n'
                                       "    return _movement_move_long(state, frame, 'offset_x', 0)\n"
                                       "return _map_presentation_arithmetic_fields(state, frame, 'offset_x', 1)",
                               'returns': 'FirstDeploymentFrame',
                               'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'decode_setup_plane_rows': {'flow': 'entered = _setup_plane_legacy_entry_fields(state, plane)\n'
                                     'returned = decode_setup_plane_rows_fields(state, entered)\n'
                                     'return _setup_plane_legacy_result_fields(state, plane, returned)',
                             'returns': 'SetupPlane',
                             'signature': 'state: SceneState, plane: SetupPlane'},
 'decode_setup_plane_rows_fields': {'flow': 'return _setup_plane_rows_fields(state, frame, 177092)',
                                    'returns': 'FirstDeploymentFrame',
                                    'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'decode_setup_plane_rows_with_masks': {'flow': 'entered = _setup_plane_legacy_entry_fields(state, plane)\n'
                                                'returned = decode_setup_plane_rows_with_masks_fields(state, entered)\n'
                                                'return _setup_plane_legacy_result_fields(state, plane, returned)',
                                        'returns': 'SetupPlane',
                                        'signature': 'state: SceneState, plane: SetupPlane'},
 'decode_setup_plane_rows_with_masks_fields': {'flow': 'return _setup_plane_rows_fields(state, frame, 177108)',
                                               'returns': 'FirstDeploymentFrame',
                                               'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'initialize_setup_video': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                    'returned = initialize_setup_video_fields(state, entered)\n'
                                    'return _setup_legacy_result_fields(state, values, returned)',
                            'returns': 'SetupValues',
                            'signature': 'state: SceneState, values: SetupValues'},
 'initialize_setup_video_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 176478)\n'
                                           'for register in (33336, 33596, 33798, 34174, 36610, 35969, 36865, 37120, 37376):\n'
                                           '    frame = _setup_write_fields(state, frame, 12582916, register)\n'
                                           'for address in (4294963986, 4294963988, 4294963990, 4294963992):\n'
                                           '    frame = _setup_write_fields(state, frame, address, 0)\n'
                                           'for command, pattern in ((1075838976, 286331153), (1342177280, 572662306)):\n'
                                           '    frame = _setup_write_fields(state, frame, 12582916, command, 4)\n'
                                           '    frame = first_replace(frame, auxiliary=state.table_at(12582912))\n'
                                           "    frame = _movement_move_long(state, frame, 'unit', pattern)\n"
                                           "    frame = _movement_move(state, frame, 'target_x', 63, 16)\n"
                                           '    while True:\n'
                                           '        frame = _setup_write_fields(state, frame, frame.auxiliary.base, frame.unit, 4)\n'
                                           "        frame, again = _map_presentation_db_fields(frame, 'target_x')\n"
                                           '        if not again:\n'
                                           '            break\n'
                                           'frame = _setup_write_fields(state, frame, 12582916, 1610612737, 4)\n'
                                           'frame = first_replace(frame, roster=state.table_at(177390).cursor())\n'
                                           "frame = _movement_move_long(state, frame, 'target_x', 2047)\n"
                                           "frame = _setup_transfer_longs_fields(state, frame, 'auxiliary', False)\n"
                                           'frame = _setup_write_fields(state, frame, 12582916, 1073741826, 4)\n'
                                           'frame = first_replace(frame, roster=state.table_at(185582).cursor())\n'
                                           "frame = _movement_move_long(state, frame, 'target_x', 2047)\n"
                                           "frame = _setup_transfer_longs_fields(state, frame, 'auxiliary', False)\n"
                                           'frame = _movement_test(state, frame, state.read(16740406, 2), 16)\n'
                                           'if frame.status & 4:\n'
                                           '    source_a, source_b, token_a, token_b = (193774, 195075, 176726, 176748)\n'
                                           'else:\n'
                                           '    source_a, source_b, token_a, token_b = (195470, 196079, 176774, 176796)\n'
                                           'frame = first_replace(frame, roster=state.table_at(source_a).cursor(), '
                                           'candidates=state.table_at(57344).cursor())\n'
                                           "frame = _movement_move_long(state, frame, 'offset_x', 128)\n"
                                           'frame = _setup_call_fields(state, frame, 177092, token_a)\n'
                                           'frame = first_replace(frame, roster=state.table_at(source_b).cursor(), '
                                           'candidates=state.table_at(57408).cursor())\n'
                                           "frame = _movement_move_long(state, frame, 'offset_x', 128)\n"
                                           'frame = _setup_call_fields(state, frame, 177092, token_b)\n'
                                           'for source, destination, token in ((196378, 49152, 176834), (196537, 49216, 176872)):\n'
                                           '    frame = first_replace(frame, roster=state.table_at(source).cursor(), '
                                           'candidates=state.table_at(destination).cursor())\n'
                                           "    frame = _movement_move_long(state, frame, 'offset_x', 128)\n"
                                           '    frame = _setup_write_fields(state, frame, 16740360, 0)\n'
                                           '    frame = _setup_write_fields(state, frame, 16740364, 65535)\n'
                                           '    frame = _setup_call_fields(state, frame, 177108, token)\n'
                                           'frame = first_replace(frame, roster=state.table_at(177262).cursor(), '
                                           'candidates=state.table_at(4294966016).cursor())\n'
                                           "frame = _movement_move(state, frame, 'target_x', 31, 16)\n"
                                           "return _setup_transfer_longs_fields(state, frame, 'candidates', True)",
                                   'returns': 'FirstDeploymentFrame',
                                   'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'render_current_setup_option': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                         'returned = render_current_setup_option_fields(state, entered)\n'
                                         'return _setup_legacy_result_fields(state, values, returned)',
                                 'returns': 'SetupValues',
                                 'signature': 'state: SceneState, values: SetupValues'},
 'render_current_setup_option_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 176010)\n'
                                                "frame = _movement_move(state, frame, 'offset_x', state.read(16740386, 2), 16)\n"
                                                'frame = _movement_compare(state, frame, low16(frame.offset_x), 5, 16)\n'
                                                'if frame.status & 4:\n'
                                                '    return advance_setup_reveal_fields(state, frame)\n'
                                                "frame = _setup_asl_word_fields(state, frame, 'offset_x', 1)\n"
                                                'frame = first_replace(frame, candidates=state.table_at(176208).cursor())\n'
                                                "frame = _movement_move(state, frame, 'target_y', "
                                                'frame.candidates.word(low16(frame.offset_x)), 16)\n'
                                                "frame = _movement_move(state, frame, 'target_x', low16(frame.target_y), 16)\n"
                                                'frame = _setup_coordinate_high_byte_fields(state, frame)\n'
                                                "frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 255, 16)\n"
                                                "frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 255, 16)\n"
                                                "frame = _movement_move_long(state, frame, 'unit', 0)\n"
                                                'return _setup_call_fields(state, frame, 44040, 176054)',
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'update_first_setup_option': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                       'returned = update_first_setup_option_fields(state, entered)\n'
                                       'return _setup_legacy_result_fields(state, values, returned)',
                               'returns': 'SetupValues',
                               'signature': 'state: SceneState, values: SetupValues'},
 'update_first_setup_option_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 175450)\n'
                                              'return _setup_update_option_fields(state, frame, 0, 16740390, 2, 176260, 175474, 175492)',
                                      'returns': 'FirstDeploymentFrame',
                                      'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'update_fourth_setup_option': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                        'returned = update_fourth_setup_option_fields(state, entered)\n'
                                        'return _setup_legacy_result_fields(state, values, returned)',
                                'returns': 'SetupValues',
                                'signature': 'state: SceneState, values: SetupValues'},
 'update_fourth_setup_option_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 175592)\n'
                                               'return _setup_update_option_fields(state, frame, 3, 16740394, 2, 176260, 175618, 175636)',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'update_second_setup_option': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                        'returned = update_second_setup_option_fields(state, entered)\n'
                                        'return _setup_legacy_result_fields(state, values, returned)',
                                'returns': 'SetupValues',
                                'signature': 'state: SceneState, values: SetupValues'},
 'update_second_setup_option_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 175496)\n'
                                               'return _setup_update_option_fields(state, frame, 1, 16740388, 2, 176310, 175522, 175540)',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'update_setup_player_choices': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                         'returned = update_setup_player_choices_fields(state, entered)\n'
                                         'return _setup_legacy_result_fields(state, values, returned)',
                                 'returns': 'SetupValues',
                                 'signature': 'state: SceneState, values: SetupValues'},
 'update_setup_player_choices_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 175640)\n'
                                                'frame = _setup_compare_memory_fields(state, frame, 16740386, 5)\n'
                                                'fifth = bool(frame.status & 4)\n'
                                                'if not fifth:\n'
                                                '    frame = _setup_compare_memory_fields(state, frame, 16740386, 6)\n'
                                                'if fifth or frame.status & 4:\n'
                                                '    render = True\n'
                                                'else:\n'
                                                '    frame = _setup_compare_memory_fields(state, frame, 16740386, 4)\n'
                                                '    if not frame.status & 4:\n'
                                                '        return frame\n'
                                                '    frame = _map_presentation_bit_fields(state, frame, state.read(4294964739, 1), 4)\n'
                                                '    if not frame.status & 4:\n'
                                                '        frame = _movement_test(state, frame, state.read(16740396, 2), 16)\n'
                                                '        if frame.status & 4:\n'
                                                '            frame = _setup_write_fields(state, frame, 16740396, 6)\n'
                                                '            frame = _setup_compare_memory_fields(state, frame, 16740390, 2)\n'
                                                '            if frame.status & 4:\n'
                                                '                frame = _setup_write_fields(state, frame, 16740396, 2)\n'
                                                '        else:\n'
                                                '            frame = _setup_change_word_fields(state, frame, 16740396, 1, True)\n'
                                                '    else:\n'
                                                '        frame = _map_presentation_bit_fields(state, frame, state.read(4294964739, 1), 8)\n'
                                                '        if not frame.status & 4:\n'
                                                '            frame = _setup_compare_memory_fields(state, frame, 16740390, 2)\n'
                                                '            if frame.status & 1:\n'
                                                '                frame = _setup_compare_memory_fields(state, frame, 16740396, 6)\n'
                                                '                if frame.status & 4:\n'
                                                '                    frame = _setup_write_fields(state, frame, 16740396, 0, clear=True)\n'
                                                '                else:\n'
                                                '                    frame = _setup_change_word_fields(state, frame, 16740396, 1)\n'
                                                '            else:\n'
                                                '                frame = _setup_compare_memory_fields(state, frame, 16740396, 2)\n'
                                                '                if frame.status & 4:\n'
                                                '                    frame = _setup_write_fields(state, frame, 16740396, 0, clear=True)\n'
                                                '                else:\n'
                                                '                    frame = _setup_change_word_fields(state, frame, 16740396, 1)\n'
                                                '    render = True\n'
                                                'if render:\n'
                                                "    frame = _movement_move_long(state, frame, 'unit', 0)\n"
                                                '    frame = _movement_test(state, frame, state.read(16740390, 2), 16)\n'
                                                '    if frame.status & 4:\n'
                                                '        address = 176218\n'
                                                '    else:\n'
                                                '        frame = _setup_compare_memory_fields(state, frame, 16740390, 1)\n'
                                                '        address = 176234 if frame.status & 4 else 176250\n'
                                                '    frame = first_replace(frame, scratch=state.table_at(address).cursor())\n'
                                                '    while True:\n'
                                                "        frame = _movement_move(state, frame, 'target_x', frame.scratch.word(), 16)\n"
                                                '        frame = first_replace(frame, scratch=frame.scratch.advance(2))\n'
                                                '        frame = _movement_compare(state, frame, low16(frame.target_x), 65535, 16)\n'
                                                '        if frame.status & 4:\n'
                                                '            break\n'
                                                "        frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\n"
                                                '        frame = _setup_coordinate_high_byte_fields(state, frame)\n'
                                                "        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 255, "
                                                '16)\n'
                                                "        frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 255, "
                                                '16)\n'
                                                '        frame = first_replace(frame, roster=state.table_at(176398).cursor())\n'
                                                '        frame = _setup_call_fields(state, frame, 44040, 175888)\n'
                                                'frame = _setup_compare_memory_fields(state, frame, 16740390, 2)\n'
                                                'if frame.status & 1:\n'
                                                "    frame = _movement_move(state, frame, 'target_x', 176, 16)\n"
                                                "    frame = _movement_move(state, frame, 'target_y', 256, 16)\n"
                                                '    frame = first_replace(frame, roster=state.table_at(176398).cursor())\n'
                                                '    frame = _setup_call_fields(state, frame, 44040, 176008)\n'
                                                'frame = _setup_compare_memory_fields(state, frame, 16740386, 6)\n'
                                                'if frame.status & 4:\n'
                                                "    frame = _movement_move(state, frame, 'offset_x', state.read(16740400, 2), 16)\n"
                                                '    frame = _setup_call_fields(state, frame, 197918, 175924)\n'
                                                '    frame = _setup_write_fields(state, frame, 16740400, low16(frame.offset_x))\n'
                                                'frame = _setup_compare_memory_fields(state, frame, 16740386, 5)\n'
                                                'if frame.status & 1:\n'
                                                '    frame = _setup_write_fields(state, frame, 16740398, 0, clear=True)\n'
                                                'frame = _setup_compare_memory_fields(state, frame, 16740386, 5)\n'
                                                'if not frame.status & 4:\n'
                                                '    return frame\n'
                                                "frame = _movement_move(state, frame, 'offset_x', state.read(16740398, 2), 16)\n"
                                                'frame = _setup_call_fields(state, frame, 197788, 175972)\n'
                                                'frame = _setup_write_fields(state, frame, 16740398, low16(frame.offset_x))\n'
                                                'return _setup_write_fields(state, frame, 16740400, 0, clear=True)',
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'update_third_setup_option': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                       'returned = update_third_setup_option_fields(state, entered)\n'
                                       'return _setup_legacy_result_fields(state, values, returned)',
                               'returns': 'SetupValues',
                               'signature': 'state: SceneState, values: SetupValues'},
 'update_third_setup_option_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 175544)\n'
                                              'return _setup_update_option_fields(state, frame, 2, 16740392, 1, 176360, 175570, 175588)',
                                      'returns': 'FirstDeploymentFrame',
                                      'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'write_setup_video_address': {'flow': 'entered = _setup_plane_legacy_entry_fields(state, plane)\n'
                                       'returned = write_setup_video_address_fields(state, entered)\n'
                                       'return _setup_plane_legacy_result_fields(state, plane, returned)',
                               'returns': 'SetupPlane',
                               'signature': 'state: SceneState, plane: SetupPlane'},
 'write_setup_video_address_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 177222)\n'
                                              "frame = _movement_save_longs(state, frame, ('target_y',))\n"
                                              "frame = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)\n"
                                              "frame = _movement_move_long(state, frame, 'target_y', frame.target_x)\n"
                                              "frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 16383, 16)\n"
                                              "frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) | 16384, 16)\n"
                                              "frame = _special_action_swap(state, frame, 'target_x')\n"
                                              "frame = _movement_fixed_shift_word(state, frame, 'target_y', 8, True)\n"
                                              "frame = _city_encounter_shift_word_fields(state, frame, 'target_y', 6, True)\n"
                                              "frame = _movement_move_long(state, frame, 'target_x', frame.target_x | frame.target_y)\n"
                                              'frame = _setup_write_fields(state, frame, 12582916, frame.target_x, 4)\n'
                                              "return _movement_restore_longs(state, frame, ('target_y',))",
                                      'returns': 'FirstDeploymentFrame',
                                      'signature': 'state: SceneState, frame: FirstDeploymentFrame'}})

# D50 option-five BEQ reaches its actual RTS; single complete DECL.
DECLARATIONS.update({'render_current_setup_option_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 176010)\n'
                                                "frame = _movement_move(state, frame, 'offset_x', state.read(16740386, 2), 16)\n"
                                                'frame = _movement_compare(state, frame, low16(frame.offset_x), 5, 16)\n'
                                                'if frame.status & 4:\n'
                                                '    return frame\n'
                                                "frame = _setup_asl_word_fields(state, frame, 'offset_x', 1)\n"
                                                'frame = first_replace(frame, candidates=state.table_at(176208).cursor())\n'
                                                "frame = _movement_move(state, frame, 'target_y', "
                                                'frame.candidates.word(low16(frame.offset_x)), 16)\n'
                                                "frame = _movement_move(state, frame, 'target_x', low16(frame.target_y), 16)\n"
                                                'frame = _setup_coordinate_high_byte_fields(state, frame)\n'
                                                "frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 255, 16)\n"
                                                "frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 255, 16)\n"
                                                "frame = _movement_move_long(state, frame, 'unit', 0)\n"
                                                'return _setup_call_fields(state, frame, 44040, 176054)',
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame'}})

# D50 first-window exact caller contract repair, sole core unchanged.
DECLARATIONS.update({'_setup_call_fields': {'flow': 'frame = _resource_cost_frame(state, frame, target)\n'
                                'stack = frame.stack_cursor.advance(-4)\n'
                                'stack.set_long(0, continuation)\n'
                                'entered = first_replace(frame, stack_cursor=stack)\n'
                                'if target == 44040:\n'
                                '    result = append_live_command_sprite_fields(SpritePacketMemory(state), entered, reset_scroll=True, '
                                'initialize_clip=True)\n'
                                'elif target == 56998:\n'
                                '    result = darken_palette_fields(SceneRefreshMemory(state), entered)\n'
                                'elif target == 26830:\n'
                                '    result = clear_video_sprite_plane_fields(SceneRefreshMemory(state), entered)\n'
                                'elif target == 26662:\n'
                                '    result = initialize_video_registers_and_planes_fields(SceneRefreshMemory(state), entered)\n'
                                'elif target == 32906:\n'
                                '    result = enqueue_sound_command_fields(SceneRefreshMemory(state), entered)\n'
                                'elif target == 176154:\n'
                                '    result = cycle_setup_option_fields(state, entered)\n'
                                'elif target == 176010:\n'
                                '    result = render_current_setup_option_fields(state, entered)\n'
                                'elif target in (177092, 177108, 177200):\n'
                                '    result = _setup_plane_rows_fields(state, entered, target)\n'
                                'elif target == 177222:\n'
                                '    result = write_setup_video_address_fields(state, entered)\n'
                                'elif target in (175450, 175496, 175544, 175592, 175640, 176056, 176102, 176478):\n'
                                '    children = {175450: update_first_setup_option_fields, 175496: update_second_setup_option_fields, '
                                '175544: update_third_setup_option_fields, 175592: update_fourth_setup_option_fields, 175640: '
                                'update_setup_player_choices_fields, 176056: advance_setup_reveal_fields, 176102: '
                                'advance_setup_dismissal_fields, 176478: initialize_setup_video_fields}\n'
                                '    result = children[target](state, entered)\n'
                                'else:\n'
                                '    from .business_scene_support import _controller_setup_child_fields\n'
                                '    result = _controller_setup_child_fields(state, entered, target)\n'
                                'result = _resource_cost_frame(state, result, target)\n'
                                'token = result.stack_cursor.long()\n'
                                'if token != continuation:\n'
                                "    raise MovementContinuationBoundary(token, result, 'actual setup child return LONG changed')\n"
                                'state.sr = state.sr & 65504 | result.status\n'
                                'return first_replace(result, stack_cursor=result.stack_cursor.advance(4))',
                        'returns': 'FirstDeploymentFrame',
                        'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long, continuation: Long'}})

# D51 exact source imports/DECL; ordinary mnemonic lowerers unchanged.
APPROVED.setdefault((2, 'high_level_scene_flows.business_scene'),set()).update(('decode_glyph_rows_to_buffers_fields',))
DECLARATIONS.update({'_game_text_battle_prompt_fields': {'flow': 'if type(second) is not bool:\n'
                                             "    raise ValueError('actual first/second prompt role required')\n"
                                             'state.sr = 9984\n'
                                             'frame = first_replace(frame, status=0)\n'
                                             'frame = first_replace(frame, roster=state.table_at(442566 if second else 442542).cursor(), '
                                             'candidates=state.table_at(4294955776).cursor())\n'
                                             "frame = _movement_move(state, frame, 'target_x', 1, 16)\n"
                                             "frame = _movement_move(state, frame, 'target_y', 3, 16)\n"
                                             "frame = _movement_move(state, frame, 'count', 11, 16)\n"
                                             'frame = _game_text_call_fields(state, frame, 44682, 96890 if second else 96822)\n'
                                             'frame = _setup_write_fields(state, frame, 12582916, 1084227586, 4)\n'
                                             'frame = first_replace(frame, candidates=state.table_at(4294955776).cursor())\n'
                                             "frame = _movement_move(state, frame, 'count', 383, 16)\n"
                                             "frame = _game_text_upload_longs_fields(state, frame, 'count')\n"
                                             'return _game_text_call_fields(state, frame, 44872, 96924 if second else 96856)',
                                     'returns': 'FirstDeploymentFrame',
                                     'signature': 'state: SceneState, frame: FirstDeploymentFrame, second: bool'},
 '_game_text_call_fields': {'flow': "frame = _resource_cost_frame(state, frame, target)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = first_replace(frame, stack_cursor=stack)\nif target == 81474:\n    from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_130_fields\n    result = lowbank_coordinate_live_state_130_fields(state, entered)\nelif target == 97306:\n    from ..high_level_remaining_flows.business_city import test_city_route_terrain_two_fields\n    result = test_city_route_terrain_two_fields(state, entered)\nelif target == 44682:\n    result = decode_glyph_rows_to_buffers_fields(SceneRefreshMemory(state), entered)\nelif target == 44872:\n    result = refresh_gameplay_scene_fields(SceneRefreshMemory(state), entered)\nelif target == 44072:\n    result = append_live_command_sprite_fields(SpritePacketMemory(state), entered, reset_scroll=False, initialize_clip=False)\nelif target == 118660:\n    result = cycle_available_direction_fields(state, entered)\nelif target == 118726:\n    result = render_direction_choice_fields(state, entered)\nelif target in (91768, 91976, 92056, 92824):\n    result = execute_deployment_menu_fields(state, target, entered)\nelse:\n    raise MovementContinuationBoundary(target, entered, 'gameplay text child lacks a complete admitted frame')\nresult = _resource_cost_frame(state, result, target)\ntoken = result.stack_cursor.long()\nif token != continuation:\n    raise MovementContinuationBoundary(token, result, 'gameplay text RTS slot changed')\nstate.sr = state.sr & 65504 | result.status\nreturn first_replace(result, stack_cursor=result.stack_cursor.advance(4))", 'returns': 'FirstDeploymentFrame', 'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long, continuation: Long'},
 '_game_text_fill_longs_fields': {'flow': 'while True:\n'
                                          '    frame = _setup_write_fields(state, frame, frame.candidates.base, 286331153, 4)\n'
                                          '    frame = first_replace(frame, candidates=frame.candidates.advance(4))\n'
                                          '    frame, again = _map_presentation_db_fields(frame, carrier)\n'
                                          '    if not again:\n'
                                          '        return frame',
                                  'returns': 'FirstDeploymentFrame',
                                  'signature': 'state: SceneState, frame: FirstDeploymentFrame, carrier: str'},
 '_game_text_indexed_dispatch_fields': {'flow': "frame = _movement_move(state, frame, 'target_x', state.read(4294964066, 2), 16)\n"
                                                "frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)\n"
                                                "frame = _movement_move(state, frame, 'target_x', "
                                                'state.table_at(table).word(low16(frame.target_x)), 16)\n'
                                                'return _game_text_call_fields(state, frame, u32(target_base + '
                                                's16(low16(frame.target_x))), token)',
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame, table: Long, target_base: Long, '
                                                     'token: Long'},
 '_game_text_upload_longs_fields': {'flow': 'while True:\n'
                                            '    value = frame.candidates.long()\n'
                                            '    frame = first_replace(frame, candidates=frame.candidates.advance(4))\n'
                                            '    frame = _setup_write_fields(state, frame, 12582912, value, 4)\n'
                                            '    frame, again = _map_presentation_db_fields(frame, carrier)\n'
                                            '    if not again:\n'
                                            '        return frame',
                                    'returns': 'FirstDeploymentFrame',
                                    'signature': 'state: SceneState, frame: FirstDeploymentFrame, carrier: str'},
 'cycle_available_direction': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                       'returned = cycle_available_direction_fields(state, entered)\n'
                                       'return _map_presentation_legacy_map_result(state, frame, returned)',
                               'returns': 'MapPresentation',
                               'signature': 'state: SceneState, frame: MapPresentation'},
 'cycle_available_direction_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 118660)\n'
                                              'frame = first_replace(frame, candidates=state.table_at(4294963134).cursor())\n'
                                              "frame = _movement_move(state, frame, 'target_y', state.read(4294963142, 2), 16)\n"
                                              "frame = _movement_move(state, frame, 'target_x', state.read(4294964739, 1), 8)\n"
                                              "frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 12, 16)\n"
                                              'if frame.status & 4:\n'
                                              '    return frame\n'
                                              'frame = _map_presentation_bit_fields(state, frame, frame.target_x, 4)\n'
                                              'backwards = bool(frame.status & 4)\n'
                                              'while True:\n'
                                              "    frame = _map_presentation_arithmetic_fields(state, frame, 'target_y', 2, backwards)\n"
                                              "    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 7, 16)\n"
                                              '    frame = _movement_test(state, frame, frame.candidates.word(low16(frame.target_y)), 16)\n'
                                              '    if not frame.status & 8:\n'
                                              '        break\n'
                                              'return _setup_write_fields(state, frame, 4294963142, low16(frame.target_y))',
                                      'returns': 'FirstDeploymentFrame',
                                      'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'dispatch_gameplay_command_state': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                             'returned = dispatch_gameplay_command_state_fields(state, entered)\n'
                                             'return _map_presentation_legacy_map_result(state, frame, returned)',
                                     'returns': 'MapPresentation',
                                     'signature': 'state: SceneState, frame: MapPresentation'},
 'dispatch_gameplay_command_state_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 81224)\n'
                                                    'return _game_text_indexed_dispatch_fields(state, frame, 81240, 81274, 81238)',
                                            'returns': 'FirstDeploymentFrame',
                                            'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'dispatch_queue_command_state': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                          'returned = dispatch_queue_command_state_fields(state, entered)\n'
                                          'return _map_presentation_legacy_map_result(state, frame, returned)',
                                  'returns': 'MapPresentation',
                                  'signature': 'state: SceneState, frame: MapPresentation'},
 'dispatch_queue_command_state_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 91744)\n'
                                                 'return _game_text_indexed_dispatch_fields(state, frame, 91760, 91768, 91758)',
                                         'returns': 'FirstDeploymentFrame',
                                         'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'dispatch_target_eligibility': {'flow': 'entered = _map_presentation_legacy_search_fields(state, search)\n'
                                         'returned = dispatch_target_eligibility_fields(state, entered)\n'
                                         'return _map_presentation_legacy_search_result(state, search, returned)',
                                 'returns': 'TargetSearch',
                                 'signature': 'state: SceneState, search: TargetSearch'},
 'dispatch_target_eligibility_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 97178)\n'
                                                "frame = _movement_save_longs(state, frame, ('offset_x', 'offset_y'))\n"
                                                "frame = _movement_move(state, frame, 'choice', state.read(4294964948, 2), 16)\n"
                                                "frame = _movement_fixed_shift_word(state, frame, 'choice', 1)\n"
                                                "frame = _movement_move(state, frame, 'choice', "
                                                'state.table_at(97202).word(low16(frame.choice)), 16)\n'
                                                'frame = _game_text_call_fields(state, frame, u32(97264 + s16(low16(frame.choice))), '
                                                '97196)\n'
                                                "return _movement_restore_longs(state, frame, ('offset_x', 'offset_y'))",
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'render_direction_choice': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                     'returned = render_direction_choice_fields(state, entered)\n'
                                     'return _map_presentation_legacy_map_result(state, frame, returned)',
                             'returns': 'MapPresentation',
                             'signature': 'state: SceneState, frame: MapPresentation'},
 'render_direction_choice_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 118726)\n'
                                            'frame = _map_presentation_bit_fields(state, frame, state.read(4294964001, 1), 16)\n'
                                            'if not frame.status & 4:\n'
                                            '    return frame\n'
                                            'frame = first_replace(frame, roster=state.table_at(118818).cursor(), '
                                            'controller=state.table_at(118802).cursor())\n'
                                            "frame = _movement_move(state, frame, 'unit', state.read(4294963142, 2), 16)\n"
                                            "frame = _movement_fixed_shift_word(state, frame, 'unit', 1)\n"
                                            'frame = first_replace(frame, candidates=state.table_at(state.read(16726060, 4)).cursor())\n'
                                            "frame = _movement_move(state, frame, 'target_x', 0, 16)\n"
                                            "frame = _movement_move(state, frame, 'target_x', frame.candidates.byte(1), 8)\n"
                                            "frame = _map_presentation_arithmetic_fields(state, frame, 'target_x', "
                                            'frame.controller.word(low16(frame.unit)))\n'
                                            "frame = _movement_fixed_shift_word(state, frame, 'target_x', 4)\n"
                                            "frame = _movement_move(state, frame, 'target_y', 0, 16)\n"
                                            "frame = _movement_move(state, frame, 'target_y', frame.candidates.byte(2), 8)\n"
                                            "frame = _map_presentation_arithmetic_fields(state, frame, 'target_y', "
                                            'frame.controller.word(low16(frame.unit), 2))\n'
                                            "frame = _movement_fixed_shift_word(state, frame, 'target_y', 4)\n"
                                            "frame = _movement_move(state, frame, 'unit', 0, 16)\n"
                                            'frame = _setup_write_fields(state, frame, 4294964746, state.read(4294963988, 2))\n'
                                            'frame = _setup_write_fields(state, frame, 4294964750, state.read(4294963992, 2))\n'
                                            'return _game_text_call_fields(state, frame, 44072, 118800)',
                                    'returns': 'FirstDeploymentFrame',
                                    'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'update_direction_choice': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                     'returned = update_direction_choice_fields(state, entered)\n'
                                     'return _map_presentation_legacy_map_result(state, frame, returned)',
                             'returns': 'MapPresentation',
                             'signature': 'state: SceneState, frame: MapPresentation'},
 'update_direction_choice_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 118616)\n'
                                            'frame = _game_text_call_fields(state, frame, 118660, 118620)\n'
                                            'frame = _game_text_call_fields(state, frame, 118726, 118624)\n'
                                            'frame = _map_presentation_bit_fields(state, frame, state.read(4294964739, 1), 32)\n'
                                            'if frame.status & 4:\n'
                                            '    return frame\n'
                                            'frame = _game_text_call_fields(state, frame, 49334, 118640)\n'
                                            'for address, value in ((4294964754, 208), (4294964066, 3), (4294964074, 18)):\n'
                                            '    frame = _setup_write_fields(state, frame, address, value)\n'
                                            'return frame',
                                    'returns': 'FirstDeploymentFrame',
                                    'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'upload_battle_action_prompt': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                         'returned = upload_battle_action_prompt_fields(state, entered)\n'
                                         'return _map_presentation_legacy_map_result(state, frame, returned)',
                                 'returns': 'MapPresentation',
                                 'signature': 'state: SceneState, frame: MapPresentation'},
 'upload_battle_action_prompt_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 98014)\n'
                                                'frame = first_replace(frame, roster=state.table_at(442590).cursor(), '
                                                'candidates=state.table_at(4294955776).cursor())\n'
                                                "frame = _movement_move(state, frame, 'target_x', 1, 16)\n"
                                                "frame = _movement_move(state, frame, 'target_y', 3, 16)\n"
                                                "frame = _movement_move(state, frame, 'count', 4, 16)\n"
                                                'frame = _game_text_call_fields(state, frame, 44682, 98042)\n'
                                                'frame = _setup_write_fields(state, frame, 12582916, 1084227586, 4)\n'
                                                'frame = first_replace(frame, candidates=state.table_at(4294955776).cursor())\n'
                                                "frame = _movement_move(state, frame, 'count', 159, 16)\n"
                                                "return _game_text_upload_longs_fields(state, frame, 'count')",
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'upload_battle_result_prompt': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                         'returned = upload_battle_result_prompt_fields(state, entered)\n'
                                         'return _map_presentation_legacy_map_result(state, frame, returned)',
                                 'returns': 'MapPresentation',
                                 'signature': 'state: SceneState, frame: MapPresentation'},
 'upload_battle_result_prompt_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 100170)\n'
                                                'frame = first_replace(frame, candidates=state.table_at(4294955776).cursor())\n'
                                                "frame = _movement_move(state, frame, 'target_x', 31, 16)\n"
                                                "frame = _game_text_fill_longs_fields(state, frame, 'target_x')\n"
                                                "frame = _movement_move(state, frame, 'target_x', 1, 16)\n"
                                                "frame = _movement_move(state, frame, 'target_y', 3, 16)\n"
                                                "frame = _movement_move(state, frame, 'count', 5, 16)\n"
                                                'frame = first_replace(frame, roster=state.table_at(442728).cursor())\n'
                                                'frame = _game_text_call_fields(state, frame, 44682, 100212)\n'
                                                'frame = _setup_write_fields(state, frame, 12582916, 1075838978, 4)\n'
                                                'frame = first_replace(frame, candidates=state.table_at(4294955776).cursor())\n'
                                                "frame = _movement_move(state, frame, 'count', 223, 16)\n"
                                                "return _game_text_upload_longs_fields(state, frame, 'count')",
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'upload_first_battle_prompt': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                        'returned = upload_first_battle_prompt_fields(state, entered)\n'
                                        'return _map_presentation_legacy_map_result(state, frame, returned)',
                                'returns': 'MapPresentation',
                                'signature': 'state: SceneState, frame: MapPresentation'},
 'upload_first_battle_prompt_fields': {'flow': 'return _game_text_battle_prompt_fields(state, _resource_cost_frame(state, frame, 96790), '
                                               'False)',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'upload_second_battle_prompt': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                         'returned = upload_second_battle_prompt_fields(state, entered)\n'
                                         'return _map_presentation_legacy_map_result(state, frame, returned)',
                                 'returns': 'MapPresentation',
                                 'signature': 'state: SceneState, frame: MapPresentation'},
 'upload_second_battle_prompt_fields': {'flow': 'return _game_text_battle_prompt_fields(state, _resource_cost_frame(state, frame, 96858), '
                                                'True)',
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'upload_selected_officer_names': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                           'returned = upload_selected_officer_names_fields(state, entered)\n'
                                           'return _map_presentation_legacy_map_result(state, frame, returned)',
                                   'returns': 'MapPresentation',
                                   'signature': 'state: SceneState, frame: MapPresentation'},
 'upload_selected_officer_names_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 100242)\n'
                                                  'frame = first_replace(frame, auxiliary=state.table_at(4294946646).cursor())\n'
                                                  "frame = _movement_move(state, frame, 'target_x', state.read(4294964824, 2), 16)\n"
                                                  "frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)\n"
                                                  'frame = first_replace(frame, '
                                                  'auxiliary=frame.auxiliary.advance(s16(low16(frame.target_x))))\n'
                                                  "frame = _movement_move(state, frame, 'target_x', 1, 16)\n"
                                                  'frame = _setup_write_fields(state, frame, 12582916, 1084227586, 4)\n'
                                                  "frame = _movement_move(state, frame, 'choice', 4, 16)\n"
                                                  'while True:\n'
                                                  "    frame = _movement_move(state, frame, 'unit', frame.auxiliary.word(), 16)\n"
                                                  '    frame = first_replace(frame, auxiliary=frame.auxiliary.advance(2))\n'
                                                  '    negative = bool(frame.status & 8)\n'
                                                  "    frame = _movement_move(state, frame, 'target_y', 3, 16)\n"
                                                  '    if negative:\n'
                                                  '        frame = first_replace(frame, candidates=state.table_at(4294955776).cursor())\n'
                                                  "        frame = _movement_move(state, frame, 'count', 15, 16)\n"
                                                  "        frame = _game_text_fill_longs_fields(state, frame, 'count')\n"
                                                  '        frame = first_replace(frame, roster=state.table_at(100420).cursor())\n'
                                                  "        frame = _movement_move(state, frame, 'count', 1, 16)\n"
                                                  '        frame = _game_text_call_fields(state, frame, 44682, 100386)\n'
                                                  "        frame = _movement_move(state, frame, 'count', 15, 16)\n"
                                                  "        frame = _game_text_fill_longs_fields(state, frame, 'count')\n"
                                                  '    else:\n'
                                                  '        frame = _map_presentation_bit_fields(state, frame, frame.unit, 1 << 14)\n'
                                                  '        if not frame.status & 4:\n'
                                                  "            frame = _movement_move(state, frame, 'target_y', 2, 16)\n"
                                                  "        frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 255, 16)\n"
                                                  "        frame = _movement_move(state, frame, 'count', low16(frame.unit), 16)\n"
                                                  "        frame = _movement_fixed_shift_word(state, frame, 'unit', 1)\n"
                                                  "        frame = _map_presentation_arithmetic_fields(state, frame, 'unit', "
                                                  'low16(frame.count))\n'
                                                  "        frame = _movement_fixed_shift_word(state, frame, 'unit', 1)\n"
                                                  '        frame = first_replace(frame, roster=state.table_at(u32(566532 + '
                                                  's16(low16(frame.unit)))).cursor(), candidates=state.table_at(4294955776).cursor())\n'
                                                  "        frame = _movement_move(state, frame, 'count', 2, 16)\n"
                                                  '        frame = _game_text_call_fields(state, frame, 44682, 100324)\n'
                                                  '    frame = first_replace(frame, candidates=state.table_at(4294955776).cursor())\n'
                                                  "    frame = _movement_move(state, frame, 'count', 95, 16)\n"
                                                  "    frame = _game_text_upload_longs_fields(state, frame, 'count')\n"
                                                  '    if negative:\n'
                                                  '        return frame\n'
                                                  "    frame, again = _map_presentation_db_fields(frame, 'choice')\n"
                                                  '    if not again:\n'
                                                  '        return frame',
                                          'returns': 'FirstDeploymentFrame',
                                          'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'upload_selected_queue_officer_name': {'flow': 'entered = _map_presentation_legacy_map_fields(state, frame)\n'
                                                'returned = upload_selected_queue_officer_name_fields(state, entered)\n'
                                                'return _map_presentation_legacy_map_result(state, frame, returned)',
                                        'returns': 'MapPresentation',
                                        'signature': 'state: SceneState, frame: MapPresentation'},
 'upload_selected_queue_officer_name_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 91608)\n'
                                                       "frame = _movement_move(state, frame, 'target_x', 1, 16)\n"
                                                       "frame = _movement_move(state, frame, 'target_y', 3, 16)\n"
                                                       'frame = first_replace(frame, candidates=state.table_at(4294955776).cursor(), '
                                                       'roster=state.table_at(state.read(16726060, 4)).cursor())\n'
                                                       "frame = _movement_move(state, frame, 'distance', 0, 16)\n"
                                                       "frame = _movement_move(state, frame, 'distance', frame.roster.byte(4), 8)\n"
                                                       "frame = _movement_fixed_shift_word(state, frame, 'distance', 1)\n"
                                                       'frame = first_replace(frame, roster=state.table_at(4294960704).cursor())\n'
                                                       "frame = _movement_move(state, frame, 'distance', "
                                                       'frame.roster.word(low16(frame.distance)), 16)\n'
                                                       "frame = _movement_move(state, frame, 'offset_x', low16(frame.distance), 16)\n"
                                                       "frame = _movement_fixed_shift_word(state, frame, 'distance', 1)\n"
                                                       "frame = _map_presentation_arithmetic_fields(state, frame, 'distance', "
                                                       'low16(frame.offset_x))\n'
                                                       "frame = _movement_fixed_shift_word(state, frame, 'distance', 1)\n"
                                                       'frame = first_replace(frame, roster=state.table_at(u32(566532 + '
                                                       's16(low16(frame.distance)))).cursor())\n'
                                                       "frame = _movement_move(state, frame, 'count', 2, 16)\n"
                                                       'frame = _game_text_call_fields(state, frame, 44682, 91668)\n'
                                                       'frame = _setup_write_fields(state, frame, 12582916, 1101004800, 4)\n'
                                                       'frame = first_replace(frame, candidates=state.table_at(4294955776).cursor())\n'
                                                       "frame = _movement_move(state, frame, 'count', 95, 16)\n"
                                                       "frame = _game_text_upload_longs_fields(state, frame, 'count')\n"
                                                       'frame = first_replace(frame, roster=state.table_at(91742).cursor(), '
                                                       'candidates=state.table_at(4294955776).cursor())\n'
                                                       "frame = _movement_move(state, frame, 'count', 0, 16)\n"
                                                       'frame = _game_text_call_fields(state, frame, 44682, 91712)\n'
                                                       'frame = _setup_write_fields(state, frame, 12582916, 1226833920, 4)\n'
                                                       'frame = first_replace(frame, candidates=state.table_at(4294955776).cursor())\n'
                                                       "frame = _movement_move(state, frame, 'count', 31, 16)\n"
                                                       "return _game_text_upload_longs_fields(state, frame, 'count')",
                                               'returns': 'FirstDeploymentFrame',
                                               'signature': 'state: SceneState, frame: FirstDeploymentFrame'}})


# C59 exact complete fields, compatibility projections and current closed dispatch.
DECLARATIONS.update({'_force_turn_call_fields': {'flow': 'frame = _resource_cost_frame(state, frame, target)\n'
                                     'uint(target, 32)\n'
                                     'uint(continuation, 32)\n'
                                     'stack = frame.stack_cursor.advance(-4)\n'
                                     'stack.set_long(0, continuation)\n'
                                     'entered = first_replace(frame, stack_cursor=stack)\n'
                                     'if target == 139852:\n'
                                     '    returned = settle_both_force_supply_fields(state, entered)\n'
                                     'elif target == 139896:\n'
                                     '    returned = deduct_force_supply_fields(state, entered)\n'
                                     'elif target == 139944:\n'
                                     '    returned = apply_force_supply_losses_fields(state, entered)\n'
                                     'elif target == 140246:\n'
                                     '    returned = check_battle_commanders_present_fields(state, '
                                     'entered)\n'
                                     'elif target == 140312:\n'
                                     '    returned = execute_secondary_force_orders_fields(state, '
                                     'entered)\n'
                                     'elif target == 140400:\n'
                                     '    returned = calculate_force_supply_budgets_fields(state, '
                                     'entered)\n'
                                     'elif target == 144738:\n'
                                     '    returned = execute_primary_force_orders_frame_fields(state, '
                                     'entered)\n'
                                     'elif target == 155876:\n'
                                     '    returned = present_battle_message_fields(state, entered)\n'
                                     'else:\n'
                                     '    returned = execute_deployment_menu_fields(state, target, '
                                     'entered)\n'
                                     'returned = _resource_cost_frame(state, returned, target)\n'
                                     'actual = returned.stack_cursor.long()\n'
                                     'if actual != continuation:\n'
                                     '    from .business_movement_support import '
                                     'MovementContinuationBoundary\n'
                                     "    raise MovementContinuationBoundary(actual, returned, 'actual "
                                     "force-turn child return token changed')\n"
                                     'return first_replace(returned, '
                                     'stack_cursor=returned.stack_cursor.advance(4))',
                             'returns': 'FirstDeploymentFrame',
                             'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int, '
                                          'continuation: int'},
 '_primary_target_child_frame_fields': {'flow': 'from .services import BattlePolicyMemory\n'
                                                'frame = display_frame_fields(state, frame)\n'
                                                'if target == 107576:\n'
                                                '    from ..high_level_battle_ai.business_actions '
                                                'import _battle_action_map_fields\n'
                                                '    return '
                                                '_battle_action_map_fields(BattlePolicyMemory(state), '
                                                'frame)\n'
                                                'if target == 144844:\n'
                                                '    from .services import '
                                                'test_battlefield_leader_roster_presence_fields\n'
                                                '    return '
                                                'test_battlefield_leader_roster_presence_fields(BattlePolicyMemory(state), '
                                                'frame).validate(state).frame\n'
                                                'if target in (152590, 152426):\n'
                                                '    from .services import '
                                                'prepare_first_side_assignment_fields, '
                                                'initialize_first_side_deployment_fields\n'
                                                '    if target == 152590:\n'
                                                '        return '
                                                'prepare_first_side_assignment_fields(BattlePolicyMemory(state), '
                                                'frame)\n'
                                                '    return '
                                                'initialize_first_side_deployment_fields(BattlePolicyMemory(state), '
                                                'frame)\n'
                                                'if target in (154626, 154666, 154780, 155402, 154808, '
                                                '154814, 155030, 155036):\n'
                                                '    policy = _force_turn_policy_fields(frame)\n'
                                                '    if target == 154626:\n'
                                                '        returned = _read_battle_policy_anchor(state, '
                                                'policy)\n'
                                                '    elif target == 154666:\n'
                                                '        returned = _battle_policy_occupied(state, '
                                                'policy)\n'
                                                '    elif target == 154780:\n'
                                                '        returned = _battle_policy_empty_slot(state, '
                                                'policy)\n'
                                                '    elif target == 155402:\n'
                                                '        returned = _battle_policy_second_anchor(state, '
                                                'policy)\n'
                                                '    elif target in (154808, 154814):\n'
                                                '        returned = _battle_policy_first_edge(state, '
                                                'policy, target == 154808)\n'
                                                '    else:\n'
                                                '        returned = _battle_policy_second_edge(state, '
                                                'policy, target == 155030)\n'
                                                '    return _battle_policy_retained_frame(state, '
                                                'returned)\n'
                                                'if target in (155128, 155432):\n'
                                                '    from .services import '
                                                'promote_first_roster_deployment_candidate_fields, '
                                                'promote_second_roster_deployment_candidate_fields\n'
                                                '    if target == 155128:\n'
                                                '        return '
                                                'promote_first_roster_deployment_candidate_fields(BattlePolicyMemory(state), '
                                                'frame)\n'
                                                '    return '
                                                'promote_second_roster_deployment_candidate_fields(BattlePolicyMemory(state), '
                                                'frame)\n'
                                                'from .business_main import '
                                                '_campaign_known_child_fields\n'
                                                'return _campaign_known_child_fields(state, frame, '
                                                'target)',
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame, '
                                                     'target: int'},
 'collect_order_target_candidates': {'flow': 'checked_context(policy, BattlePolicy, state)\n'
                                             'entered = _battle_policy_retained_frame(state, policy)\n'
                                             'returned = '
                                             'collect_order_target_candidates_frame_fields(state, '
                                             'entered)\n'
                                             'return _battle_policy_retained_result(state, policy, '
                                             'returned)',
                                     'returns': 'BattlePolicy',
                                     'signature': 'state: SceneState, policy: BattlePolicy'},
 'collect_order_target_candidates_frame_fields': {'flow': 'from .business_movement_support import '
                                                          '_movement_add_word\n'
                                                          'frame = display_frame_fields(state, frame)\n'
                                                          'frame = display_address_fields(state, frame, '
                                                          "'candidates', 4294943056)\n"
                                                          'frame = display_call_fields(state, frame, '
                                                          '154780, 154738)\n'
                                                          'if frame.status & 1:\n'
                                                          '    return frame\n'
                                                          'while True:\n'
                                                          '    for target, continuation in ((154808, '
                                                          '154746), (155030, 154754), (155114, 154762), '
                                                          '(155122, 154770)):\n'
                                                          '        frame = display_call_fields(state, '
                                                          'frame, target, continuation)\n'
                                                          '        if frame.status & 1:\n'
                                                          '            return frame\n'
                                                          '    frame = _movement_add_word(state, frame, '
                                                          "'choice', 2)",
                                                  'returns': 'FirstDeploymentFrame',
                                                  'signature': 'state: SceneState, frame: '
                                                               'FirstDeploymentFrame'},
 'execute_primary_force_orders': {'flow': 'checked_context(policy, BattlePolicy, state)\n'
                                          'entered = _battle_policy_retained_frame(state, policy)\n'
                                          'returned = execute_primary_force_orders_frame_fields(state, '
                                          'entered)\n'
                                          'return _battle_policy_retained_result(state, policy, '
                                          'returned)',
                                  'returns': 'BattlePolicy',
                                  'signature': 'state: SceneState, policy: BattlePolicy'},
 'execute_primary_force_orders_frame_fields': {'flow': 'from .business_movement_support import '
                                                       '_movement_compare, _movement_save_longs, '
                                                       '_movement_restore_longs\n'
                                                       'frame = display_frame_fields(state, frame)\n'
                                                       'frame = display_call_fields(state, frame, '
                                                       '152590, 144742)\n'
                                                       'frame = display_call_fields(state, frame, '
                                                       '140400, 144746)\n'
                                                       'frame = display_address_fields(state, frame, '
                                                       "'roster', 4294944080)\n"
                                                       'frame = display_address_fields(state, frame, '
                                                       "'candidates', 4294946690)\n"
                                                       'while True:\n'
                                                       '    frame = display_call_fields(state, frame, '
                                                       '144844, 144758)\n'
                                                       '    if frame.status & 1:\n'
                                                       '        break\n'
                                                       '    frame = _movement_compare(state, frame, '
                                                       'state.read(4294964754, 2), 1041, 16)\n'
                                                       '    if frame.status & 4:\n'
                                                       '        break\n'
                                                       '    leader = frame.roster.word()\n'
                                                       '    frame = first_replace(frame, '
                                                       'roster=frame.roster.advance(2))\n'
                                                       '    frame = display_move_fields(state, frame, '
                                                       "'choice', leader)\n"
                                                       '    if frame.status & 8:\n'
                                                       '        break\n'
                                                       '    order = frame.candidates.word()\n'
                                                       '    frame = first_replace(frame, '
                                                       'candidates=frame.candidates.advance(2))\n'
                                                       '    frame = display_move_fields(state, frame, '
                                                       "'target_x', order)\n"
                                                       '    frame = _movement_compare(state, frame, '
                                                       'low16(frame.target_x), 255, 16)\n'
                                                       '    if frame.status & 4:\n'
                                                       '        continue\n'
                                                       '    frame = display_store_fields(state, frame, '
                                                       '144786, 4294965104, low16(frame.target_x))\n'
                                                       '    frame = display_shift_word_fields(state, '
                                                       "frame, 'target_x', 1)\n"
                                                       '    table_word = state.read(u32(144822 + '
                                                       's16(low16(frame.target_x))), 2)\n'
                                                       '    frame = display_move_fields(state, frame, '
                                                       "'target_x', table_word)\n"
                                                       '    frame = _movement_save_longs(state, frame, '
                                                       "('roster', 'candidates'))\n"
                                                       '    frame = display_address_fields(state, '
                                                       "frame, 'roster', 144912)\n"
                                                       '    target = u32(frame.roster.base + '
                                                       's16(low16(frame.target_x)))\n'
                                                       '    frame = display_call_fields(state, frame, '
                                                       'target, 144810)\n'
                                                       '    frame = _movement_restore_longs(state, '
                                                       "frame, ('roster', 'candidates'))\n"
                                                       'return display_store_fields(state, frame, '
                                                       '144816, 4294964066, 0, clear=True)',
                                               'returns': 'FirstDeploymentFrame',
                                               'signature': 'state: SceneState, frame: '
                                                            'FirstDeploymentFrame'},
 'initialize_battle_policy_targets': {'flow': 'checked_context(policy, BattlePolicy, state)\n'
                                              'entered = _battle_policy_retained_frame(state, policy)\n'
                                              'returned = '
                                              'initialize_battle_policy_targets_frame_fields(state, '
                                              'entered)\n'
                                              'return _battle_policy_retained_result(state, policy, '
                                              'returned)',
                                      'returns': 'BattlePolicy',
                                      'signature': 'state: SceneState, policy: BattlePolicy'},
 'initialize_battle_policy_targets_frame_fields': {'flow': 'frame = display_frame_fields(state, frame)\n'
                                                           'frame = display_call_fields(state, frame, '
                                                           '107576, 154590)\n'
                                                           'frame = display_call_fields(state, frame, '
                                                           '154600, 154594)\n'
                                                           'return display_call_fields(state, frame, '
                                                           '155376, 154598)',
                                                   'returns': 'FirstDeploymentFrame',
                                                   'signature': 'state: SceneState, frame: '
                                                                'FirstDeploymentFrame'},
 'initialize_primary_policy_targets': {'flow': 'checked_context(policy, BattlePolicy, state)\n'
                                               'entered = _battle_policy_retained_frame(state, policy)\n'
                                               'returned = '
                                               'initialize_primary_policy_targets_frame_fields(state, '
                                               'entered)\n'
                                               'return _battle_policy_retained_result(state, policy, '
                                               'returned)',
                                       'returns': 'BattlePolicy',
                                       'signature': 'state: SceneState, policy: BattlePolicy'},
 'initialize_primary_policy_targets_frame_fields': {'flow': 'frame = display_frame_fields(state, '
                                                            'frame)\n'
                                                            'frame = display_call_fields(state, frame, '
                                                            '154626, 154604)\n'
                                                            'frame = display_call_fields(state, frame, '
                                                            '154666, 154608)\n'
                                                            'frame = display_address_fields(state, '
                                                            "frame, 'scan', 4294944080)\n"
                                                            'frame = display_move_fields(state, frame, '
                                                            "'choice', 2)\n"
                                                            'frame = display_call_fields(state, frame, '
                                                            '154730, 154620)\n'
                                                            'return display_call_fields(state, frame, '
                                                            '155128, 154624)',
                                                    'returns': 'FirstDeploymentFrame',
                                                    'signature': 'state: SceneState, frame: '
                                                                 'FirstDeploymentFrame'},
 'initialize_secondary_policy_targets': {'flow': 'checked_context(policy, BattlePolicy, state)\n'
                                                 'entered = _battle_policy_retained_frame(state, '
                                                 'policy)\n'
                                                 'returned = '
                                                 'initialize_secondary_policy_targets_frame_fields(state, '
                                                 'entered)\n'
                                                 'return _battle_policy_retained_result(state, policy, '
                                                 'returned)',
                                         'returns': 'BattlePolicy',
                                         'signature': 'state: SceneState, policy: BattlePolicy'},
 'initialize_secondary_policy_targets_frame_fields': {'flow': 'frame = display_frame_fields(state, '
                                                              'frame)\n'
                                                              'frame = display_call_fields(state, '
                                                              'frame, 155402, 155380)\n'
                                                              'frame = display_call_fields(state, '
                                                              'frame, 154666, 155384)\n'
                                                              'frame = display_address_fields(state, '
                                                              "frame, 'scan', 4294944164)\n"
                                                              'frame = display_move_fields(state, '
                                                              "frame, 'choice', 4)\n"
                                                              'frame = display_call_fields(state, '
                                                              'frame, 154730, 155396)\n'
                                                              'return display_call_fields(state, frame, '
                                                              '155432, 155400)',
                                                      'returns': 'FirstDeploymentFrame',
                                                      'signature': 'state: SceneState, frame: '
                                                                   'FirstDeploymentFrame'},
 'offset_first_order_target_axis': {'flow': 'checked_context(policy, BattlePolicy, state)\n'
                                            'entered = _battle_policy_retained_frame(state, policy)\n'
                                            'returned = '
                                            'offset_first_order_target_axis_frame_fields(state, '
                                            'entered)\n'
                                            'return _battle_policy_retained_result(state, policy, '
                                            'returned)',
                                    'returns': 'BattlePolicy',
                                    'signature': 'state: SceneState, policy: BattlePolicy'},
 'offset_first_order_target_axis_frame_fields': {'flow': 'from .business_movement_support import '
                                                         '_movement_add_word\n'
                                                         'frame = display_frame_fields(state, frame)\n'
                                                         'frame = display_move_fields(state, frame, '
                                                         "'unit', low16(frame.choice))\n"
                                                         'frame = _movement_add_word(state, frame, '
                                                         "'unit', low16(frame.target_x))\n"
                                                         'return '
                                                         '_primary_target_child_frame_fields(state, '
                                                         'frame, 154814)',
                                                 'returns': 'FirstDeploymentFrame',
                                                 'signature': 'state: SceneState, frame: '
                                                              'FirstDeploymentFrame'},
 'offset_second_order_target_axis': {'flow': 'checked_context(policy, BattlePolicy, state)\n'
                                             'entered = _battle_policy_retained_frame(state, policy)\n'
                                             'returned = '
                                             'offset_second_order_target_axis_frame_fields(state, '
                                             'entered)\n'
                                             'return _battle_policy_retained_result(state, policy, '
                                             'returned)',
                                     'returns': 'BattlePolicy',
                                     'signature': 'state: SceneState, policy: BattlePolicy'},
 'offset_second_order_target_axis_frame_fields': {'flow': 'from .business_movement_support import '
                                                          '_movement_add_word\n'
                                                          'frame = display_frame_fields(state, frame)\n'
                                                          'frame = display_move_fields(state, frame, '
                                                          "'count', low16(frame.choice))\n"
                                                          'frame = _movement_add_word(state, frame, '
                                                          "'count', low16(frame.target_y))\n"
                                                          'return '
                                                          '_primary_target_child_frame_fields(state, '
                                                          'frame, 155036)',
                                                  'returns': 'FirstDeploymentFrame',
                                                  'signature': 'state: SceneState, frame: '
                                                               'FirstDeploymentFrame'},
 'select_primary_force_order_policy': {'flow': 'checked_context(policy, BattlePolicy, state)\n'
                                               'entered = _battle_policy_retained_frame(state, policy)\n'
                                               'returned = '
                                               'select_primary_force_order_policy_frame_fields(state, '
                                               'entered)\n'
                                               'return _battle_policy_retained_result(state, policy, '
                                               'returned)',
                                       'returns': 'BattlePolicy',
                                       'signature': 'state: SceneState, policy: BattlePolicy'},
 'select_primary_force_order_policy_frame_fields': {'flow': 'from .business_map import '
                                                            '_world_map_bit_fields\n'
                                                            'frame = display_frame_fields(state, '
                                                            'frame)\n'
                                                            'frame = _world_map_bit_fields(state, '
                                                            'frame, state.read(4294964951, 1), 1)\n'
                                                            'return display_call_fields(state, frame, '
                                                            '152426, 150246) if frame.status & 4 else '
                                                            'display_call_fields(state, frame, 150258, '
                                                            '150238)',
                                                    'returns': 'FirstDeploymentFrame',
                                                    'signature': 'state: SceneState, frame: '
                                                                 'FirstDeploymentFrame'}})
APPROVED.setdefault('business_main', set()).update(('_campaign_known_child_fields',))
APPROVED.setdefault('business_map', set()).update(('_world_map_bit_fields',))
APPROVED.setdefault('business_movement_support', set()).update(('MovementContinuationBoundary', '_movement_add_word', '_movement_compare', '_movement_restore_longs', '_movement_save_longs'))
APPROVED.setdefault('contexts_display_fields', set()).update(('display_address_fields', 'display_call_fields', 'display_child_fields', 'display_frame_fields', 'display_move_fields', 'display_shift_word_fields', 'display_store_fields'))
APPROVED.setdefault('services', set()).update(('BattlePolicyMemory', 'initialize_first_side_deployment_fields', 'prepare_first_side_assignment_fields', 'promote_first_roster_deployment_candidate_fields', 'promote_second_roster_deployment_candidate_fields', 'test_battlefield_leader_roster_presence_fields'))
APPROVED.setdefault((2, 'high_level_battle_ai.business_actions'), set()).update(('_battle_action_map_fields',))

APPROVED.setdefault((2, 'high_level_remaining_flows.business_city'), set()).update(('test_city_route_terrain_two_fields',))

APPROVED.setdefault((2, 'high_level_remaining_flows.business_lowbank'), set()).update(('lowbank_coordinate_live_state_130_fields',))


# Complete six-function Main rule-reuse Frame40 normal frontend109; old scalar interfaces and all opcode lowerers unchanged.
MONTHLY_ACTION_FIELD_DECLARATIONS = {'award_defense_progress': {'signature': 'state: SceneState, officer: Long, gain: Long', 'returns': 'DefenseProgressResult', 'flow': 'checked_state(state)\nuint(officer, 32)\nuint(gain, 32)\nframe = first_replace(FirstDeploymentFrame.unobserved(), unit=officer, count=gain, status=state.sr & 31)\nframe = award_defense_progress_fields(state, frame)\nreturn DefenseProgressResult(frame.unit, frame.count, state.table_at(frame.roster.base))'}, 'clear_completed_monthly_actions': {'signature': 'state: SceneState, retained_counter: Long', 'returns': 'MonthlyActionsResult', 'flow': 'checked_state(state)\nuint(retained_counter, 32)\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=retained_counter, status=state.sr & 31)\nframe = clear_completed_monthly_actions_fields(state, frame)\nreturn MonthlyActionsResult(frame.target_x, frame.roster)'}, 'query_scaled_terrain': {'signature': 'state: SceneState, row: Long, column: Long, retained_terrain: Long, retained_cost: Long', 'returns': 'TerrainQueryResult', 'flow': "checked_state(state)\nfor value in (row, column, retained_terrain, retained_cost):\n    uint(value, 32)\ncell_row = low16(row) >> 4\ncell_column = low16(column) >> 4\nindex = u16(u16(u16(cell_row + u16(cell_row << 3)) << 3) + cell_column)\nterrain = data_view(state, 'data_0ee5f0').byte(index)\ncosts = data_view(state, 'data_00670a')\ncost = costs.byte(terrain)\nreturn TerrainQueryResult(replace_word(row, u16(cell_row << 4)), replace_word(column, u16(cell_column << 4)), replace_word(retained_terrain, terrain), replace_word(retained_cost, cost), costs)"}, '_project_rule_frame_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, entry: int, defense: bool', 'returns': 'FirstDeploymentFrame', 'flow': "checked_state(state)\nif type(frame) is not FirstDeploymentFrame or (entry, defense) not in ((72844, True), (72906, False)):\n    raise ValueError('current sole project rule fields required')\nframe.validate(state, complete=False)\nneeded = (frame.target_x, frame.unit, frame.count, frame.stack_cursor, frame.status) if defense else (frame.target_x, frame.status)\nif any((value is None for value in needed)):\n    raise MovementContinuationBoundary(entry, frame, 'historical rule projection lacks actual saved D0 WORD/SP or observed fields')\nstate.sr = state.sr & 65504 | frame.status\nreturn frame"}, 'award_defense_progress_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _project_rule_frame_fields(state, frame, 72844, True)\nvalue = low16(frame.target_x)\nstack = frame.stack_cursor.advance(-2)\nstack.set_word(0, value)\nframe = first_replace(frame, stack_cursor=stack)\nframe = _movement_test(state, frame, value, 16)\nframe = _movement_fixed_shift_word(state, frame, 'unit', 1)\nframe = _movement_fixed_shift_word(state, frame, 'count', 1)\nfor address in (4294950400, 4294950912):\n    frame = first_replace(frame, roster=state.table_at(address).cursor())\n    frame = _movement_move(state, frame, 'target_x', frame.roster.word(low16(frame.unit)), 16)\n    frame = _movement_add_word(state, frame, 'target_x', low16(frame.count))\n    frame = _movement_compare(state, frame, low16(frame.target_x), 999, 16)\n    if not frame.status & 5:\n        frame = _movement_move(state, frame, 'target_x', 999, 16)\n    frame = _settlement_store_word_fields(state, frame, frame.roster, low16(frame.unit), low16(frame.target_x))\nrestored = frame.stack_cursor.word()\nframe = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\nreturn _movement_move(state, frame, 'target_x', restored, 16)"}, 'clear_completed_monthly_actions_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _project_rule_frame_fields(state, frame, 72906, False)\nframe = first_replace(frame, roster=state.table_at(4294954240).cursor())\nframe = _movement_move(state, frame, 'target_x', 255, 16)\nwhile True:\n    frame = _movement_compare(state, frame, frame.roster.byte(), 1, 8)\n    if frame.status & 4:\n        frame = _settlement_write_byte_fields(state, frame, frame.roster, value=0, clear=True)\n    frame = first_replace(frame, roster=frame.roster.advance(1))\n    remaining = low16(frame.target_x) - 1 & 65535\n    frame = first_replace(frame, target_x=replace_word(frame.target_x, remaining))\n    if remaining == 65535:\n        break\nframe = first_replace(frame, roster=state.table_at(4294961720).cursor())\nframe = _movement_move(state, frame, 'target_x', 39, 16)\nwhile True:\n    value = frame.roster.byte()\n    frame.roster.set_byte(0, value & 253)\n    frame = first_replace(frame, roster=frame.roster.advance(1))\n    frame = _postbattle_bit_fields(frame, bool(value & 2))\n    state.sr = state.sr & 65504 | frame.status\n    remaining = low16(frame.target_x) - 1 & 65535\n    frame = first_replace(frame, target_x=replace_word(frame.target_x, remaining))\n    if remaining == 65535:\n        return frame", 'slots': {255: ('officer_latch', 0, 65535), 39: ('city_latch', 0, 65535)}}}
MONTHLY_ACTION_FIELD_APPROVED = {'domain': {'Long', 'descending_inclusive', 'data_view', 'u8', 'checked_state', 'replace_word', 'ram_view', 'u16', 'low16', 'SceneState', 'uint'}, 'contexts_rule_reuse': {'DefenseProgressResult', 'TerrainQueryResult', 'MonthlyActionsResult'}, 'services': {'FirstDeploymentFrame'}, 'business_movement_support': {'MovementContinuationBoundary', '_movement_test', '_movement_compare', '_movement_move', 'first_replace', '_movement_fixed_shift_word', '_movement_add_word'}, (2, 'high_level_remaining_flows.business_city'): {'_settlement_write_byte_fields', '_settlement_store_word_fields'}, (2, 'high_level_gameplay_flow.business_battle'): {'_postbattle_bit_fields'}}

def compile_monthly_action_fields(source):
    """Whole current Scene/Frame catalog to the existing Officer40 lowerer.

    Only the original two bounded DBRA latches are editable semantic slots.
    Fixed clear/BCLR order, complete Frame carriers and all six bodies must
    match the explicit grammar. Old scalar None is not a Frame authority.
    """
    records = semantic_functions(source, MONTHLY_ACTION_FIELD_DECLARATIONS,
        MONTHLY_ACTION_FIELD_APPROVED)
    if set(records) != set(MONTHLY_ACTION_FIELD_DECLARATIONS):
        raise CompileError('all six complete reuse-rule bodies required')
    root = 'clear_completed_monthly_actions_fields'
    declaration = MONTHLY_ACTION_FIELD_DECLARATIONS[root]
    if (declaration['signature'] != 'state: SceneState, frame: FirstDeploymentFrame'
            or declaration['returns'] != 'FirstDeploymentFrame'
            or set(records[root]['rules']) != {'officer_latch','city_latch'}):
        raise CompileError('the real complete Scene/Frame ABI and two bounded latches required')
    from ..high_level_city_officer.compiler_officer import Lowerer
    lowerer = Lowerer('clear_monthly_actions', dict(slots=records[root]['rules'],
        args=declaration['signature'], returns=declaration['returns']))
    lowerer.clear_monthly_actions()
    unit = lowerer.finish()
    if (unit['binding'] != dict(name='clear_monthly_actions',entry=72906,end=72946,completion='return')
            or len(unit['instructions']) != 12
            or sum(row['encoding_bytes'] for row in unit['instructions']) != 40):
        raise CompileError('entire original Officer Binding40 and all twelve ordinary rows required')
    unit['effects'].update(current_Frame_root=root,
        effective_current_root_DECLARE=dict(declaration),
        complete_reuse_catalog_effects={name:record['effects'] for name,record in records.items()},
        ordinary_compiler='tools.high_level_city_officer.compiler_officer',
        ordinary_lowerer='Lowerer.clear_monthly_actions',
        scalar_None_not_relabelled_as_Frame=True)
    return dict(units=[unit],allocated_bytes=40,instructions=12,
        current_semantic_records=records,complete_current_catalog_admitted=True,
        complete_current_catalog_count=len(records),original_generation_input=False,
        complete_CPU=False,opaque_opcode_payload=False,
        old_scalar_frontend_unchanged=True,entire_current_Frame_catalog_not_projection=True)


# Source140: genuine complete roster/save routes; caller-owned real return LONGs.
DECLARATIONS.update({'_city_project_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, target)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, uint(continuation, 32))\nentered = first_replace(frame, stack_cursor=stack)\nif target == 72106:\n    result = settle_all_city_projects_fields(state, entered)\nelif target == 72144:\n    result = settle_first_city_project_fields(state, entered)\nelif target == 72360:\n    result = settle_second_city_project_fields(state, entered)\nelif target == 72646:\n    result = settle_third_city_project_fields(state, entered)\nelif target == 72844:\n    from .reuse_rules import award_defense_progress_fields\n    result = award_defense_progress_fields(state, entered)\nelif target == 72906:\n    from .reuse_rules import clear_completed_monthly_actions_fields\n    result = clear_completed_monthly_actions_fields(state, entered)\nelif target == 33786:\n    result = _city_project_save_fields(state, entered)\nelse:\n    result = execute_deployment_menu_fields(state, target, entered)\nresult = _resource_cost_frame(state, result, target)\nactual = result.stack_cursor.long()\nif actual != continuation:\n    from .business_movement_support import MovementContinuationBoundary\n    raise MovementContinuationBoundary(actual, result, 'actual project child return LONG changed')\nreturn first_replace(result, stack_cursor=result.stack_cursor.advance(4))"}, '_city_project_save_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 33786)\nfrom ..high_level_storage.contexts_scene_storage import SceneStorageState\nfrom ..high_level_storage.contexts_storage_fields import StorageFrame\nfrom ..high_level_storage.business_save import write_saved_game_state_frame_fields\nstorage = SceneStorageState(state)\nentered = StorageFrame(d0=frame.target_x, d1=frame.target_y, d2=frame.unit, d3=frame.count, d4=frame.distance, d5=frame.offset_x, d6=frame.offset_y, d7=frame.choice, a0=frame.roster.base, a1=frame.candidates.base, a2=frame.controller.base, a3=frame.scan.base, a4=frame.opponent.base, a5=frame.scratch.base, a6=frame.auxiliary.base, stack_cursor=frame.stack_cursor.base, status_word=state.sr & 65504 | frame.status)\nreturned = write_saved_game_state_frame_fields(storage, entered)\nif type(returned) is not StorageFrame:\n    from .business_movement_support import MovementContinuationBoundary\n    raise MovementContinuationBoundary(33786, frame, 'complete storage return frame required')\nreturned.validate(storage)\nstate.sr = returned.status_word\nreturn first_replace(frame, target_x=returned.d0, target_y=returned.d1, unit=returned.d2, count=returned.d3, distance=returned.d4, offset_x=returned.d5, offset_y=returned.d6, choice=returned.d7, roster=state.table_at(returned.a0).cursor(), candidates=state.table_at(returned.a1).cursor(), controller=state.table_at(returned.a2).cursor(), scan=state.table_at(returned.a3).cursor(), opponent=state.table_at(returned.a4).cursor(), scratch=state.table_at(returned.a5).cursor(), auxiliary=state.table_at(returned.a6).cursor(), stack_cursor=state.table_at(returned.stack_cursor).cursor(), status=returned.status_word & 31)"}})
APPROVED.setdefault((2, 'high_level_storage.contexts_scene_storage'), set()).update(('SceneStorageState',))
APPROVED.setdefault((2, 'high_level_storage.contexts_storage_fields'), set()).update(('StorageFrame',))
APPROVED.setdefault((2, 'high_level_storage.business_save'), set()).update(('write_saved_game_state_frame_fields',))


# Source142: complete battle-order dispatch; real outer CALL LONG retained.
DECLARATIONS.update({'execute_primary_force_orders_frame_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from .business_movement_support import _movement_compare, _movement_save_longs, _movement_restore_longs\nframe = display_frame_fields(state, frame)\nframe = display_call_fields(state, frame, 152590, 144742)\nframe = display_call_fields(state, frame, 140400, 144746)\nframe = display_address_fields(state, frame, 'roster', 4294944080)\nframe = display_address_fields(state, frame, 'candidates', 4294946690)\nwhile True:\n    frame = display_call_fields(state, frame, 144844, 144758)\n    if frame.status & 1:\n        break\n    frame = _movement_compare(state, frame, state.read(4294964754, 2), 1041, 16)\n    if frame.status & 4:\n        break\n    leader = frame.roster.word()\n    frame = first_replace(frame, roster=frame.roster.advance(2))\n    frame = display_move_fields(state, frame, 'choice', leader)\n    if frame.status & 8:\n        break\n    order = frame.candidates.word()\n    frame = first_replace(frame, candidates=frame.candidates.advance(2))\n    frame = display_move_fields(state, frame, 'target_x', order)\n    frame = _movement_compare(state, frame, low16(frame.target_x), 255, 16)\n    if frame.status & 4:\n        continue\n    frame = display_store_fields(state, frame, 144786, 4294965104, low16(frame.target_x))\n    frame = display_shift_word_fields(state, frame, 'target_x', 1)\n    table_word = state.read(u32(144822 + s16(low16(frame.target_x))), 2)\n    frame = display_move_fields(state, frame, 'target_x', table_word)\n    frame = _movement_save_longs(state, frame, ('roster', 'candidates'))\n    frame = display_address_fields(state, frame, 'roster', 144912)\n    target = u32(frame.roster.base + s16(low16(frame.target_x)))\n    frame = _battle_order_call_fields(state, frame, target, 144810)\n    frame = _movement_restore_longs(state, frame, ('roster', 'candidates'))\nreturn display_store_fields(state, frame, 144816, 4294964066, 0, clear=True)"}, 'select_primary_force_order_policy_frame_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'from .business_map import _world_map_bit_fields\nframe = display_frame_fields(state, frame)\nframe = _world_map_bit_fields(state, frame, state.read(4294964951, 1), 1)\nreturn display_call_fields(state, frame, 152426, 150246) if frame.status & 4 else _battle_order_call_fields(state, frame, 150258, 150238)'}, '_game_text_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, target)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = first_replace(frame, stack_cursor=stack)\nif target == 81474:\n    from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_130_fields\n    result = lowbank_coordinate_live_state_130_fields(state, entered)\nelif target == 97306:\n    from ..high_level_remaining_flows.business_city import test_city_route_terrain_two_fields\n    result = test_city_route_terrain_two_fields(state, entered)\nelif target == 44682:\n    result = decode_glyph_rows_to_buffers_fields(SceneRefreshMemory(state), entered)\nelif target == 44872:\n    result = refresh_gameplay_scene_fields(SceneRefreshMemory(state), entered)\nelif target == 44072:\n    result = append_live_command_sprite_fields(SpritePacketMemory(state), entered, reset_scroll=False, initialize_clip=False)\nelif target == 118660:\n    result = cycle_available_direction_fields(state, entered)\nelif target == 118726:\n    result = render_direction_choice_fields(state, entered)\nelif target in (91768, 91976, 92056, 92824):\n    result = execute_deployment_menu_fields(state, target, entered)\nelif target == 49334:\n    from .business_commands import open_roster_selection_message_frame_fields\n    result = open_roster_selection_message_frame_fields(state, entered)\nelse:\n    raise MovementContinuationBoundary(target, entered, 'gameplay text child lacks a complete admitted frame')\nresult = _resource_cost_frame(state, result, target)\ntoken = result.stack_cursor.long()\nif token != continuation:\n    raise MovementContinuationBoundary(token, result, 'gameplay text RTS slot changed')\nstate.sr = state.sr & 65504 | result.status\nreturn first_replace(result, stack_cursor=result.stack_cursor.advance(4))"}, '_battle_order_child_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = display_frame_fields(state, frame)\nuint(target, 32)\nif target in (146620, 146846, 147646, 148206, 148616, 148940, 149192, 149510, 150138):\n    from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_65_fields\n    return highbank_coordinate_live_state_65_fields(state, frame, entry=target)\nif target == 150258:\n    from ..high_level_battle_ai.business_formation import initialize_second_side_deployment_fields\n    return initialize_second_side_deployment_fields(BattlePolicyMemory(state), frame)\nreturn display_child_fields(state, frame, target)'}, '_battle_order_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "frame = display_frame_fields(state, frame)\nuint(target, 32)\nuint(continuation, 32)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = first_replace(frame, stack_cursor=stack)\nreturned = _battle_order_child_fields(state, entered, target)\nreturned = display_frame_fields(state, returned)\nactual = returned.stack_cursor.long()\nif actual != continuation:\n    raise MovementContinuationBoundary(actual, returned, 'original display child continuation changed')\nreturn first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))"}})
APPROVED.setdefault((2, 'high_level_remaining_flows.business_highbank'), set()).update(('highbank_coordinate_live_state_65_fields',))
APPROVED.setdefault((2, 'high_level_battle_ai.business_formation'), set()).update(('initialize_second_side_deployment_fields',))
APPROVED.setdefault('business_commands', set()).update(('open_roster_selection_message_frame_fields',))


# Source145: full world-force stages, no selector clamp or synthetic result.
DECLARATIONS.update({'_game_text_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, target)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = first_replace(frame, stack_cursor=stack)\nif target == 81474:\n    from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_130_fields\n    result = lowbank_coordinate_live_state_130_fields(state, entered)\nelif target in (97214, 97264, 97306, 97334, 97340, 97366):\n    result = execute_deployment_menu_fields(state, target, entered)\nelif target == 44682:\n    result = decode_glyph_rows_to_buffers_fields(SceneRefreshMemory(state), entered)\nelif target == 44872:\n    result = refresh_gameplay_scene_fields(SceneRefreshMemory(state), entered)\nelif target == 44072:\n    result = append_live_command_sprite_fields(SpritePacketMemory(state), entered, reset_scroll=False, initialize_clip=False)\nelif target == 118660:\n    result = cycle_available_direction_fields(state, entered)\nelif target == 118726:\n    result = render_direction_choice_fields(state, entered)\nelif target in (91768, 91976, 92056, 92824):\n    result = execute_deployment_menu_fields(state, target, entered)\nelif target == 49334:\n    from .business_commands import open_roster_selection_message_frame_fields\n    result = open_roster_selection_message_frame_fields(state, entered)\nelif target == 81274:\n    from ..high_level_remaining_flows.business_lowbank import lowbank_process_counted_records_39_fields\n    result = lowbank_process_counted_records_39_fields(state, entered)\nelif target in (82000, 82958, 83850, 84844, 85592, 88602, 88672, 88950, 88958, 89114, 89214, 89284, 89488, 89510, 89552):\n    result = execute_deployment_menu_fields(state, target, entered)\nelse:\n    raise MovementContinuationBoundary(target, entered, 'gameplay text child lacks a complete admitted frame')\nresult = _resource_cost_frame(state, result, target)\ntoken = result.stack_cursor.long()\nif token != continuation:\n    raise MovementContinuationBoundary(token, result, 'gameplay text RTS slot changed')\nstate.sr = state.sr & 65504 | result.status\nreturn first_replace(result, stack_cursor=result.stack_cursor.advance(4))"}})
APPROVED.setdefault((2, 'high_level_remaining_flows.business_lowbank'), set()).update(('lowbank_process_counted_records_39_fields',))
