"""Restricted business-text admission and ordinary mnemonic lowering.
An intermediate fixed-structure compiler, not arbitrary Python or CPU proof.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import BUSINESS_HIGHBANK_BINDINGS

APPROVED={'contexts_highbank': {'GrowthResult',
                       'GrowthValues',
                       'GrowthFrame',
                       'FullGrowthResult',
                       'GrowthScanObservation',
                       'MessageDispatch',
                       'MessageLayout',
                       'OfficerSelection',
                       'checked_context'},
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
              'call_target',
              'expand_glyph_row',
              'sample_random_pair',
              'step_random',
              'write_vdp_swapped_byte_rle_stream'}}

DECLARATIONS={'_ram': {'signature': 'state, name',
          'returns': None,
          'flow': "return ram_view(state, 'ram_' + name)"},
 '_word': {'signature': 'state, name', 'returns': None, 'flow': 'return _ram(state, name).word()'},
 '_put': {'signature': 'state, name, value',
          'returns': None,
          'flow': '_ram(state, name).set_word(0, u16(value))'},
 '_carry': {'signature': 'state, value',
            'returns': None,
            'flow': 'status = state.read_status_word()\n'
                    'state.set_status_word(status | 1 if value else status & 65534)'},
 '_random': {'signature': 'state',
             'returns': None,
             'flow': 'from .services import step_random\nreturn step_random(state)'},
 '_ratio_attribute_growth': {'signature': 'state, values, first',
                             'returns': None,
                             'flow': "strength, intellect = (_ram(state, 'c000'), _ram(state, "
                                     "'be00'))\n"
                                     'selected = low16(values.selected)\n'
                                     'numerator = strength.word(selected) if first else '
                                     'intellect.word(selected)\n'
                                     'value = replace_word(values.value, numerator)\n'
                                     'category = replace_word(values.category, low16(value))\n'
                                     'value = replace_word(value, u16(low16(value) << 1))\n'
                                     'value = replace_word(value, u16(low16(value) + '
                                     'low16(category)))\n'
                                     'other = intellect.word(selected) if first else '
                                     'strength.word(selected)\n'
                                     'category = replace_word(category, u16(low16(category) + '
                                     'other))\n'
                                     'value &= 65535\n'
                                     'value = divu_retained(value, low16(category))\n'
                                     "field = _ram(state, 'b400' if first else 'b600')\n"
                                     'category = replace_word(category, field.word(selected))\n'
                                     'category = replace_word(category, u16(low16(category) + '
                                     'low16(value)))\n'
                                     'if low16(category) > 255:\n'
                                     '    category = replace_word(category, 255)\n'
                                     'field.set_word(selected, low16(category))\n'
                                     'return replace(values, value=value, category=category)'},
 'increase_growth_first_attribute': {'signature': 'state: SceneState, values: GrowthValues',
                                     'returns': 'GrowthValues',
                                     'flow': 'checked_context(values, GrowthValues, state)\n'
                                             'return _ratio_attribute_growth(state, values, True)'},
 'increase_growth_second_attribute': {'signature': 'state: SceneState, values: GrowthValues',
                                      'returns': 'GrowthValues',
                                      'flow': 'checked_context(values, GrowthValues, state)\n'
                                              'return _ratio_attribute_growth(state, values, '
                                              'False)'},
 'increase_growth_random_attribute': {'signature': 'state: SceneState, values: GrowthValues',
                                      'returns': 'GrowthValues',
                                      'flow': 'checked_context(values, GrowthValues, state)\n'
                                              'saved_index = low16(values.selected)\n'
                                              'sample = _random(state) & 65535\n'
                                              'value = swap_words(u32((sample << 1) + sample))\n'
                                              'selected = replace_word(sample, saved_index)\n'
                                              'category = replace_word(values.category, '
                                              'low16(value))\n'
                                              'value = replace_word(value, u16(low16(value) << '
                                              '2))\n'
                                              'value = replace_word(value, u16(low16(value) + '
                                              'low16(category)))\n'
                                              "field = _ram(state, 'b800')\n"
                                              'category = replace_word(category, '
                                              'field.word(low16(selected)))\n'
                                              'category = replace_word(category, '
                                              'u16(low16(category) + low16(value)))\n'
                                              'if low16(category) > 150:\n'
                                              '    category = replace_word(category, 150)\n'
                                              'field.set_word(low16(selected), low16(category))\n'
                                              'return GrowthValues(selected, value, category)',
                                      'slots': {150: ('growth_random_attribute_cap', 0, 65535)}},
 'increase_growth_command_radius': {'signature': 'state: SceneState, values: GrowthValues',
                                    'returns': 'GrowthValues',
                                    'flow': 'checked_context(values, GrowthValues, state)\n'
                                            'selected = replace_word(values.selected, '
                                            'low16(values.selected) >> 1)\n'
                                            "field = _ram(state, 'c400')\n"
                                            'value = values.value\n'
                                            'if field.byte(low16(selected)) < 20:\n'
                                            '    from .services import sample_random_pair\n'
                                            '    saved_index = low16(selected)\n'
                                            '    sampled = sample_random_pair(state)\n'
                                            '    selected = replace_word(sampled.sample, '
                                            'saved_index)\n'
                                            '    value = replace_word(sampled.updated_state, '
                                            "_word(state, 'f61c'))\n"
                                            '    if value & 16:\n'
                                            '        field.set_byte(low16(selected), '
                                            'u8(field.byte(low16(selected)) + 1))\n'
                                            'return replace(values, selected=selected, '
                                            'value=value)'},
 'check_growth_notification_owner': {'signature': 'state: SceneState, values: GrowthValues',
                                     'returns': 'GrowthResult',
                                     'flow': 'checked_context(values, GrowthValues, state)\n'
                                             "assignments, rulers = (_ram(state, 'cc00'), "
                                             "_ram(state, 'f427'))\n"
                                             'value = replace_byte(values.value, '
                                             'assignments.byte(low16(values.selected)))\n'
                                             'notify = False\n'
                                             'if not negative_byte(low8(value)):\n'
                                             '    value = replace_word(value, low16(value) & 63)\n'
                                             '    value = replace_byte(value, '
                                             'rulers.byte(low16(value)))\n'
                                             '    notify = low8(value) == _ram(state, '
                                             "'f67b').byte() or low8(value) == _ram(state, "
                                             "'f67d').byte() or low8(value) == _ram(state, "
                                             "'f67f').byte()\n"
                                             '_carry(state, notify)\n'
                                             'return GrowthResult(replace(values, value=value), '
                                             'notify, assignments)'},
 'advance_officer_growth_levels': {'signature': 'state: SceneState, values: GrowthValues',
                                   'returns': 'GrowthResult',
                                   'flow': 'checked_context(values, GrowthValues, state)\n'
                                           'observed = _scan_officer_growth(state, values, None, '
                                           'None)\n'
                                           'return GrowthResult(observed.values, observed.carry, '
                                           'observed.assignments)'},
 'sort_high_loyalty_officers': {'signature': 'state: SceneState, choice: OfficerSelection',
                                'returns': 'OfficerSelection',
                                'flow': 'checked_context(choice, OfficerSelection, state)\n'
                                        "assignments, loyalty, rulers = (_ram(state, 'cc00'), "
                                        "_ram(state, 'c300'), _ram(state, 'f427'))\n"
                                        "force = replace_word(choice.force, _word(state, 'efb0'))\n"
                                        'scan = replace_word(choice.scan, 255)\n'
                                        "_put(state, 'f100', 65535)\n"
                                        'count, score, trait = (choice.count, choice.score, '
                                        'choice.trait)\n'
                                        'displaced, displaced_score = (choice.displaced, '
                                        'choice.displaced_score)\n'
                                        'for officer in descending_inclusive(255):\n'
                                        '    score = replace_byte(score, '
                                        'assignments.byte(officer))\n'
                                        '    if not low8(score) or negative_byte(low8(score)):\n'
                                        '        continue\n'
                                        '    score = replace_word(score, low16(score) & 63)\n'
                                        '    if low8(force) != rulers.byte(low16(score)):\n'
                                        '        continue\n'
                                        '    if loyalty.byte(officer) < 90:\n'
                                        '        continue\n'
                                        '    score = replace_word(score, 0)\n'
                                        '    score = replace_byte(score, loyalty.byte(officer))\n'
                                        "    names, scores = (_ram(state, 'f100').cursor(), "
                                        "_ram(state, 'f200').cursor())\n"
                                        '    trait = replace_word(trait, officer)\n'
                                        '    while not negative_word(names.word()):\n'
                                        '        if low16(score) > scores.word():\n'
                                        '            break\n'
                                        '        names.base = u32(names.base + 2)\n'
                                        '        scores.base = u32(scores.base + 2)\n'
                                        '    while True:\n'
                                        '        displaced_score = replace_word(displaced_score, '
                                        'scores.word())\n'
                                        '        scores.append_word(low16(score))\n'
                                        '        score = replace_word(score, '
                                        'low16(displaced_score))\n'
                                        '        displaced = replace_word(displaced, '
                                        'names.word())\n'
                                        '        names.append_word(low16(trait))\n'
                                        '        trait = replace_word(trait, low16(displaced))\n'
                                        '        if negative_word(low16(trait)):\n'
                                        '            break\n'
                                        '    names.put_word(65535)\n'
                                        '    count = replace_word(count, u16(low16(count) + 1))\n'
                                        'scan = replace_word(scan, 65535)\n'
                                        'return OfficerSelection(count, force, scan, score, trait, '
                                        'displaced, displaced_score, choice.selected)'},
 'append_mid_loyalty_officers_by_trait': {'signature': 'state: SceneState, choice: '
                                                       'OfficerSelection',
                                          'returns': 'OfficerSelection',
                                          'flow': 'checked_context(choice, OfficerSelection, '
                                                  'state)\n'
                                                  "destination = _ram(state, 'f100').cursor()\n"
                                                  'while not '
                                                  'negative_word(destination.next_word()):\n'
                                                  '    pass\n'
                                                  'destination.base = u32(destination.base - 2)\n'
                                                  "assignments, rulers = (_ram(state, 'cc00'), "
                                                  "_ram(state, 'f427'))\n"
                                                  "loyalty, traits = (_ram(state, 'c300'), "
                                                  "_ram(state, 'c700'))\n"
                                                  'scan = replace_word(choice.force, 255)\n'
                                                  'force = replace_word(choice.scan, _word(state, '
                                                  "'efb0'))\n"
                                                  'score, count = (choice.score, choice.count)\n'
                                                  'for officer in descending_inclusive(255):\n'
                                                  '    score = replace_byte(score, '
                                                  'assignments.byte(officer))\n'
                                                  '    if not low8(score) or '
                                                  'negative_byte(low8(score)):\n'
                                                  '        continue\n'
                                                  '    score = replace_word(score, low16(score) & '
                                                  '63)\n'
                                                  '    if low8(force) != '
                                                  'rulers.byte(low16(score)):\n'
                                                  '        continue\n'
                                                  '    if loyalty.byte(officer) < 80 or '
                                                  'loyalty.byte(officer) >= 90:\n'
                                                  '        continue\n'
                                                  '    score = replace_byte(score, '
                                                  'traits.byte(officer))\n'
                                                  '    score = replace_word(score, low16(score) & '
                                                  '7)\n'
                                                  '    if low8(score) != low8(choice.trait):\n'
                                                  '        continue\n'
                                                  '    destination.append_word(officer)\n'
                                                  '    count = replace_word(count, '
                                                  'u16(low16(count) + 1))\n'
                                                  'destination.put_word(65535)\n'
                                                  'return replace(choice, count=count, '
                                                  'force=replace_word(scan, 65535), scan=force, '
                                                  'score=score)'},
 'build_ten_officer_selection': {'signature': 'state: SceneState, choice: OfficerSelection',
                                 'returns': 'OfficerSelection',
                                 'flow': 'checked_context(choice, OfficerSelection, state)\n'
                                         'choice = sort_high_loyalty_officers(state, '
                                         'replace(choice, count=replace_word(choice.count, 0)))\n'
                                         'for trait in (4, 3, 2):\n'
                                         '    if low16(choice.count) >= 10:\n'
                                         '        break\n'
                                         '    choice = append_mid_loyalty_officers_by_trait(state, '
                                         'replace(choice, trait=replace_word(choice.trait, '
                                         'trait)))\n'
                                         "source, destination = (_ram(state, 'f100').cursor(), "
                                         "_ram(state, 'f500').cursor())\n"
                                         'count = replace_word(choice.count, 0)\n'
                                         'while True:\n'
                                         '    officer = source.next_word()\n'
                                         '    destination.append_word(officer)\n'
                                         '    if negative_word(officer):\n'
                                         '        break\n'
                                         '    count = replace_word(count, u16(low16(count) + 1))\n'
                                         '    if low16(count) >= 10:\n'
                                         '        break\n'
                                         'destination.put_word(65535)\n'
                                         "_put(state, 'f636', count)\n"
                                         'return replace(choice, count=count)'},
 'select_highest_trait_officer': {'signature': 'state: SceneState, choice: OfficerSelection',
                                  'returns': 'OfficerSelection',
                                  'flow': 'checked_context(choice, OfficerSelection, state)\n'
                                          "assignments, traits, loyalty = (_ram(state, 'cc00'), "
                                          "_ram(state, 'c700'), _ram(state, 'c300'))\n"
                                          "first, second = (_ram(state, 'b400'), _ram(state, "
                                          "'b600'))\n"
                                          'trait, best = (replace_word(choice.count, 0), '
                                          'replace_word(choice.force, 0))\n'
                                          'selected, score, scan = (choice.selected, choice.score, '
                                          'choice.scan)\n'
                                          'offset = choice.trait\n'
                                          'for officer in descending_inclusive(255):\n'
                                          '    scan = replace_word(scan, officer)\n'
                                          '    score = replace_byte(score, '
                                          'assignments.byte(officer))\n'
                                          '    if not low8(score):\n'
                                          '        continue\n'
                                          '    score = replace_word(score, low16(score) & 192)\n'
                                          '    if low16(score):\n'
                                          '        continue\n'
                                          '    score = replace_byte(score, traits.byte(officer))\n'
                                          '    score = replace_word(score, low16(score) & 7)\n'
                                          '    if low16(score) < low16(trait):\n'
                                          '        continue\n'
                                          '    if low16(score) != low16(trait):\n'
                                          '        best = replace_word(best, 0)\n'
                                          '    trait = replace_word(trait, low16(score))\n'
                                          '    score = replace_byte(replace_word(score, 0), '
                                          'loyalty.byte(officer))\n'
                                          '    offset = replace_word(offset, u16(officer << 1))\n'
                                          '    score = replace_word(score, u16(low16(score) + '
                                          'first.word(low16(offset))))\n'
                                          '    score = replace_word(score, u16(low16(score) + '
                                          'second.word(low16(offset))))\n'
                                          '    if low16(score) > low16(best):\n'
                                          '        best = replace_word(best, low16(score))\n'
                                          '        selected = replace_word(selected, officer)\n'
                                          "_put(state, 'f3a6', selected)\n"
                                          "_put(state, 'f376', _word(state, 'f376') & 255)\n"
                                          'return replace(choice, count=trait, force=best, '
                                          'scan=replace_word(scan, 65535), score=score, '
                                          'trait=offset, selected=selected)'},
 'calculate_force_command_budget': {'signature': 'state: SceneState, choice: OfficerSelection',
                                    'returns': 'OfficerSelection',
                                    'flow': 'checked_context(choice, OfficerSelection, state)\n'
                                            "cities = _ram(state, 'e320').cursor()\n"
                                            'mean = 0\n'
                                            'for _ in descending_inclusive(39):\n'
                                            '    mean = u32(mean + cities.next_long())\n'
                                            'mean = divu_retained(mean, 40)\n'
                                            "loyalty, assignments = (_ram(state, 'c300'), "
                                            "_ram(state, 'cc00'))\n"
                                            'total, count = (0, replace_word(choice.score, 0))\n'
                                            'item, member = (replace_word(choice.trait, 0), '
                                            'choice.displaced)\n'
                                            'for officer in descending_inclusive(255):\n'
                                            '    item = replace_byte(item, '
                                            'assignments.byte(officer))\n'
                                            '    if not low8(item):\n'
                                            '        continue\n'
                                            '    item = replace_word(item, low16(item) & 192)\n'
                                            '    if low16(item):\n'
                                            '        continue\n'
                                            '    item = replace_byte(item, loyalty.byte(officer))\n'
                                            '    total = replace_word(total, u16(low16(total) + '
                                            'low16(item)))\n'
                                            '    count = replace_word(count, u16(low16(count) + '
                                            '1))\n'
                                            "packet = _ram(state, '9000').cursor()\n"
                                            'while True:\n'
                                            '    item = replace_byte(item, packet.byte())\n'
                                            '    item = replace_word(item, low16(item) & 15)\n'
                                            '    if not low16(item):\n'
                                            '        break\n'
                                            '    member = replace_byte(member, packet.byte(4))\n'
                                            "    if low8(member) == _ram(state, 'f377').byte():\n"
                                            '        for offset in '
                                            'descending_inclusive(u16(low16(item) - 1)):\n'
                                            '            item = replace_word(item, offset)\n'
                                            '            member = replace_byte(member, '
                                            'loyalty.byte(u16(13 + offset)))\n'
                                            '            member = replace_byte(member, '
                                            'packet.byte(low16(member)))\n'
                                            '            total = replace_word(total, '
                                            'u16(low16(total) + low16(member)))\n'
                                            '            count = replace_word(count, '
                                            'u16(low16(count) + 1))\n'
                                            '    item = replace_byte(item, packet.byte())\n'
                                            '    item = replace_word(item, low16(item) & 15)\n'
                                            '    packet.base = u32(packet.base + 13 + '
                                            's16(low16(item)))\n'
                                            'total = divu_retained(total, low16(count))\n'
                                            'mean = replace_word(mean, u16(low16(mean) + '
                                            'low16(total)))\n'
                                            'mean = divu_retained(u32(low16(mean) * low16(count)), '
                                            '280)\n'
                                            "_put(state, 'efdc', mean)\n"
                                            'return replace(choice, '
                                            'count=replace_word(choice.count, 65535), force=mean, '
                                            'scan=total, score=count, trait=item, '
                                            'displaced=member)'},
 '_dispatch_message': {'signature': 'state, target, selector, layout, continuation',
                       'returns': None,
                       'flow': 'from .services import call_target\n'
                               'result = call_target(state, u32(target), MessageDispatch(selector, '
                               'layout, continuation))\n'
                               'if type(result) is not MessageLayout:\n'
                               "    raise Boundary('message handler must return its real layout "
                               "carriers')\n"
                               'return result.validate(state)'},
 'dispatch_highbank_command_state': {'signature': 'state: SceneState, layout: MessageLayout',
                                     'returns': 'MessageLayout',
                                     'flow': 'checked_context(layout, MessageLayout, state)\n'
                                             'selector = replace_word(layout.symbol, '
                                             "u16(_word(state, 'f362') << 1))\n"
                                             'selector = replace_word(selector, data_view(state, '
                                             "'data_066c10').word(low16(selector)))\n"
                                             'layout = _dispatch_message(state, 420904 + '
                                             's16(low16(selector)), selector, layout, 420866)\n'
                                             'layout = _dispatch_message(state, 55532, '
                                             'layout.symbol, layout, 420872)\n'
                                             'return _dispatch_message(state, 41304, '
                                             'layout.symbol, layout, 420878)'},
 'lookup_message_layout_words': {'signature': 'state: SceneState, layout: MessageLayout',
                                 'returns': 'MessageLayout',
                                 'flow': 'checked_context(layout, MessageLayout, state)\n'
                                         "offset = u16(_word(state, 'f6c4') << 2)\n"
                                         "colors = data_view(state, 'data_06747e')\n"
                                         'return replace(layout, '
                                         'symbol=u32(s16(colors.word(offset))), '
                                         'position=u32(s16(colors.word(offset, displacement=2))))'},
 'lookup_message_fill_pattern': {'signature': 'state: SceneState, layout: MessageLayout',
                                 'returns': 'MessageLayout',
                                 'flow': 'checked_context(layout, MessageLayout, state)\n'
                                         'return replace(layout, fill=data_view(state, '
                                         "'data_06749a').long(u16(_word(state, 'f6c4') << 2)))"},
 'append_scrolling_message_header': {'signature': 'state: SceneState, layout: MessageLayout',
                                     'returns': 'MessageLayout',
                                     'flow': 'checked_context(layout, MessageLayout, state)\n'
                                             'if layout.destination is None:\n'
                                             "    raise Boundary('live message destination "
                                             "required')\n"
                                             'position = replace_word(layout.position, 16528 if '
                                             "_word(state, 'f37a') else 16480)\n"
                                             'layout.destination.append_word(low16(position))\n'
                                             'position = replace_word(position, _word(state, '
                                             "'f37c') & 65528)\n"
                                             'stride = replace_word(layout.stride, '
                                             'low16(position))\n'
                                             'position = replace_word(position, '
                                             'u16(low16(position) + low16(stride)))\n'
                                             "if _word(state, 'f37a'):\n"
                                             '    position = replace_word(position, '
                                             'u16(low16(position) + low16(stride)))\n'
                                             'position = replace_word(position, '
                                             'u16((low16(position) << 2) + 41120))\n'
                                             "if _word(state, 'f37a'):\n"
                                             '    position = replace_word(position, '
                                             'u16(low16(position) + 2304))\n'
                                             'layout.destination.append_word(low16(position))\n'
                                             'return replace(layout, position=position, '
                                             'stride=stride)'},
 'append_scrolling_message_glyph': {'signature': 'state: SceneState, layout: MessageLayout',
                                    'returns': 'MessageLayout',
                                    'flow': 'checked_context(layout, MessageLayout, state)\n'
                                            'position = replace_word(layout.position, '
                                            'u16((low16(layout.symbol) & 65280) << 3))\n'
                                            'symbol = replace_word(layout.symbol, '
                                            'u16((low16(layout.symbol) & 255) << 5))\n'
                                            'symbol = replace_word(symbol, low16(symbol) | '
                                            'low16(position))\n'
                                            'return append_scrolling_message_bitmap(state, '
                                            'replace(layout, symbol=symbol, position=position, '
                                            'bitmap=data_view(state, '
                                            "'data_08159c').cursor(low16(symbol))))"},
 'append_scrolling_message_bitmap': {'signature': 'state: SceneState, layout: MessageLayout',
                                     'returns': 'MessageLayout',
                                     'flow': 'from .services import expand_glyph_row\n'
                                             'checked_context(layout, MessageLayout, state)\n'
                                             'if layout.destination is None or layout.bitmap is '
                                             'None:\n'
                                             "    raise Boundary('bitmap and live plane "
                                             "destination required')\n"
                                             'destination, bitmap = (layout.destination, '
                                             'layout.bitmap)\n'
                                             "previous = _ram(state, 'f516').cursor()\n"
                                             'stride, position = (replace_word(layout.stride, 64), '
                                             'layout.position)\n'
                                             "if _word(state, 'f37a'):\n"
                                             '    stride, position = (replace_word(stride, 96), '
                                             'replace_word(position, 3))\n'
                                             '    for _ in descending_inclusive(3):\n'
                                             '        layout = lookup_message_fill_pattern(state, '
                                             'layout)\n'
                                             '        destination.set_long(192, layout.fill)\n'
                                             '        destination.set_long(96, layout.fill)\n'
                                             '        destination.append_long(layout.fill)\n'
                                             '    position = replace_word(position, 65535)\n'
                                             'row_offset = replace_word(layout.row_offset, '
                                             'u16(low16(stride) << 1))\n'
                                             "_put(state, 'f31a', u16(_word(state, 'f31a') + "
                                             'low16(row_offset)))\n'
                                             "_put(state, 'f31a', u16(_word(state, 'f31a') + "
                                             'low16(stride)))\n'
                                             "_put(state, 'f31a', u16(_word(state, 'f31a') + 4))\n"
                                             'stride = replace_word(swap_words(stride), 15)\n'
                                             'row_offset = replace_word(swap_words(row_offset), '
                                             "_word(state, 'f37c') & 7)\n"
                                             'symbol, first, second = (layout.symbol, '
                                             'layout.first_plane, layout.second_plane)\n'
                                             'shift_count, fill = (layout.shift_count, '
                                             'layout.fill)\n'
                                             'for row in descending_inclusive(15):\n'
                                             '    colors = lookup_message_layout_words(state, '
                                             'replace(layout, symbol=symbol, position=position))\n'
                                             '    symbol, position = (colors.symbol, '
                                             'colors.position)\n'
                                             '    first = expand_glyph_row(state, bitmap, '
                                             'low8(symbol), low8(position))\n'
                                             '    second = expand_glyph_row(state, bitmap, '
                                             'low8(symbol), low8(position))\n'
                                             '    fill = lookup_message_fill_pattern(state, '
                                             'replace(layout, fill=fill)).fill\n'
                                             '    shift_count = replace_word(shift_count, '
                                             'low16(row_offset))\n'
                                             '    if low16(shift_count):\n'
                                             '        shift_count = replace_word(shift_count, '
                                             'u16((low16(shift_count) << 2) - 1))\n'
                                             '        symbol = replace_word(symbol, 0)\n'
                                             '        for _ in '
                                             'descending_inclusive(low16(shift_count)):\n'
                                             '            '
                                             'state.set_status_word(state.read_status_word() & '
                                             '65519)\n'
                                             '            carry, next_carry = (first & 1, second & '
                                             '1)\n'
                                             '            first >>= 1\n'
                                             '            second = u32(second >> 1 | carry << 31)\n'
                                             '            fill = u32(fill >> 1 | next_carry << '
                                             '31)\n'
                                             '            '
                                             'state.set_status_word(state.read_status_word() | '
                                             '16)\n'
                                             '            symbol = u32(symbol >> 1 | 2147483648)\n'
                                             '        shift_count = replace_word(shift_count, '
                                             '65535)\n'
                                             '    position = previous.long() & symbol\n'
                                             '    first |= position\n'
                                             '    '
                                             'destination.set_long(low16(swap_words(row_offset)), '
                                             'fill)\n'
                                             '    destination.set_long(low16(swap_words(stride)), '
                                             'second)\n'
                                             '    destination.append_long(first)\n'
                                             '    previous.append_long(fill)\n'
                                             '    stride = replace_word(stride, u16(row - 1))\n'
                                             'stride, row_offset = (swap_words(stride), '
                                             'swap_words(row_offset))\n'
                                             "if _word(state, 'f37a'):\n"
                                             '    for _ in descending_inclusive(3):\n'
                                             '        fill = lookup_message_fill_pattern(state, '
                                             'replace(layout, fill=fill)).fill\n'
                                             '        destination.set_long(low16(row_offset), '
                                             'fill)\n'
                                             '        destination.set_long(low16(stride), fill)\n'
                                             '        destination.append_long(fill)\n'
                                             '    position = replace_word(position, 65535)\n'
                                             'destination.set_word(low16(row_offset), 0)\n'
                                             'return replace(layout, symbol=symbol, '
                                             'position=position, stride=stride, '
                                             'row_offset=row_offset, first_plane=first, '
                                             'second_plane=second, fill=fill, '
                                             'shift_count=shift_count, previous_rows=previous)'},
 'advance_scrolling_message': {'signature': 'state: SceneState, layout: MessageLayout',
 'returns': 'MessageLayout',
 'flow': 'checked_context(layout, MessageLayout, state)\n'
         'fields = _advance_scrolling_message_core(state, layout)\n'
         'if fields.layout is None:\n'
         "    raise Boundary('complete MessageLayout result is required')\n"
         'return fields.layout'},
 'lookup_message_decoration_style': {'signature': 'state: SceneState, layout: MessageLayout',
                                     'returns': 'MessageLayout',
                                     'flow': 'checked_context(layout, MessageLayout, state)\n'
                                             'symbol = replace_word(layout.symbol, '
                                             "u16(_word(state, 'f6c4') << 1))\n"
                                             'return replace(layout, symbol=symbol, '
                                             'stride=replace_word(layout.stride, data_view(state, '
                                             "'data_067516').word(low16(symbol))))"},
 'advance_message_decoration_stage': {'signature': 'state: SceneState, layout: MessageLayout',
                                      'returns': 'MessageLayout',
                                      'flow': 'checked_context(layout, MessageLayout, state)\n'
                                              'layout = lookup_message_decoration_style(state, '
                                              'replace(layout, destination=_ram(state, '
                                              "'d100').cursor(_word(state, 'f31a'))))\n"
                                              'selector = replace_word(layout.symbol, '
                                              "u16(_word(state, 'f36a') << 1))\n"
                                              'selector = replace_word(selector, data_view(state, '
                                              "'data_067502').word(low16(selector)))\n"
                                              'layout = _dispatch_message(state, 423198 + '
                                              's16(low16(selector)), selector, layout, 423140)\n'
                                              "_put(state, 'f36a', u16(_word(state, 'f36a') + 1))\n"
                                              'selector = replace_word(layout.symbol, _word(state, '
                                              "'f36a'))\n"
                                              'if low16(selector) >= 4:\n'
                                              "    _put(state, 'f362', u16(_word(state, 'f362') + "
                                              '1))\n'
                                              "    _put(state, 'f36a', 0)\n"
                                              "_ram(state, 'f3a4').set_byte(0, _ram(state, "
                                              "'f3a4').byte() | 64)\n"
                                              'return replace(layout, symbol=selector)'},
 'dispatch_message_control': {'signature': 'state: SceneState, layout: MessageLayout',
 'returns': 'MessageLayout',
 'flow': 'checked_context(layout, MessageLayout, state)\n'
         'fields = dispatch_message_control_fields(state, layout)\n'
         'current = layout if fields.layout_after_handler is None else '
         'fields.layout_after_handler\n'
         'return replace(current, symbol=replace_word(current.symbol, fields.value), '
         'position=current.position if fields.field_if_written is None else '
         'replace_word(current.position, fields.field_if_written), stride=current.stride if '
         'fields.tile_if_written is None else replace_word(current.stride, '
         'fields.tile_if_written), destination=current.destination if '
         'fields.destination_if_written is None else fields.destination_if_written, '
         'previous_rows=current.previous_rows if fields.source_if_written is None else '
         'fields.source_if_written)'},
 'render_force_city_markers': {'signature': 'state: SceneState, layout: MessageLayout',
                               'returns': 'MessageLayout',
                               'flow': 'from .services import write_vdp_swapped_byte_rle_stream, '
                                       'append_map_sprites\n'
                                       'from .domain import VideoPlaneAddress\n'
                                       'checked_context(layout, MessageLayout, state)\n'
                                       "if _word(state, 'f612') == 512 and _word(state, 'f352') <= "
                                       '16:\n'
                                       '    return layout\n'
                                       "if not _word(state, 'efc8'):\n"
                                       '    state.set_status_word(9984)\n'
                                       '    write_vdp_swapped_byte_rle_stream(state, '
                                       "data_view(state, 'data_067c90').cursor(), "
                                       'VideoPlaneAddress(replace_word(layout.symbol, 8192)))\n'
                                       '    state.set_status_word(9472)\n'
                                       "    _put(state, 'efc8', 1)\n"
                                       "palette = _ram(state, 'fb50')\n"
                                       'palette.set_word(0, 0)\n'
                                       'palette.set_word(2, 3648)\n'
                                       'palette.set_word(4, 2798)\n'
                                       'palette.set_word(6, 2574)\n'
                                       'palette.set_word(8, 736)\n'
                                       'palette.set_word(10, 206)\n'
                                       'palette.set_word(12, 3744)\n'
                                       'palette.set_word(14, 0)\n'
                                       'position, stride = (layout.position, layout.stride)\n'
                                       'for city in range(40):\n'
                                       "    owner = _ram(state, 'f428').byte(city)\n"
                                       '    if owner == 255:\n'
                                       '        continue\n'
                                       "    selector = u16((owner << 1) + (_word(state, 'f320') >> "
                                       '3 & 1) << 2)\n'
                                       '    pointer = data_view(state, '
                                       "'data_067b10').long(selector)\n"
                                       '    offset = u16(city << 2)\n'
                                       '    symbol = replace_word(city, u16(data_view(state, '
                                       "'data_0d4aca').word(offset, displacement=2) - 16))\n"
                                       '    position = replace_word(0, data_view(state, '
                                       "'data_0d4aca').word(offset))\n"
                                       '    stride = replace_word(stride, 0)\n'
                                       "    _put(state, 'f60a', _word(state, 'f314'))\n"
                                       "    _put(state, 'f60e', _word(state, 'f318'))\n"
                                       '    result = append_map_sprites(state, '
                                       'state.table_at(pointer).cursor(), symbol, position, '
                                       'stride, reset_scroll=False, initialize_clip=True)\n'
                                       '    position, stride = (result.y, result.attributes)\n'
                                       'return replace(layout, symbol=40, position=position, '
                                       'stride=stride)'},
 '_scan_officer_growth': {'signature': 'state, values, attribute_pointer, owner_pointer',
                          'returns': None,
                          'flow': 'checked_context(values, GrowthValues, state)\n'
                                  "strength, intellect, levels = (_ram(state, 'c000'), _ram(state, "
                                  "'be00'), _ram(state, 'c600'))\n"
                                  "thresholds, assignments = (data_view(state, 'data_066478'), "
                                  "_ram(state, 'cc00'))\n"
                                  "_put(state, 'ef78', 0)\n"
                                  'while True:\n'
                                  '    selected = replace_word(values.selected, _word(state, '
                                  "'ef78'))\n"
                                  '    values = replace(values, selected=selected)\n'
                                  '    if low16(selected) >= 256:\n'
                                  "        _put(state, 'cfcc', 1)\n"
                                  '        _carry(state, False)\n'
                                  '        return GrowthScanObservation(values, strength, '
                                  'intellect, levels, thresholds, attribute_pointer, '
                                  'owner_pointer, assignments, False, False, False, False)\n'
                                  '    if assignments.byte(low16(selected)) == 255:\n'
                                  "        _put(state, 'ef78', _word(state, 'ef78') + 1)\n"
                                  '        continue\n'
                                  '    category = replace_word(values.category, 0)\n'
                                  '    category = replace_byte(category, '
                                  'levels.byte(low16(selected)))\n'
                                  '    category = replace_word(category, u16(low16(category) << '
                                  '1))\n'
                                  '    selected = replace_word(selected, u16(low16(selected) << '
                                  '1))\n'
                                  '    value = replace_word(values.value, '
                                  'strength.word(low16(selected)))\n'
                                  '    value = replace_word(value, u16(low16(value) + '
                                  'intellect.word(low16(selected))))\n'
                                  '    values = GrowthValues(selected, value, category)\n'
                                  '    if low16(value) < thresholds.word(low16(category)):\n'
                                  "        _put(state, 'ef78', _word(state, 'ef78') + 1)\n"
                                  '        continue\n'
                                  '    values = increase_growth_first_attribute(state, values)\n'
                                  '    values = increase_growth_second_attribute(state, values)\n'
                                  '    values = increase_growth_random_attribute(state, values)\n'
                                  '    values = increase_growth_command_radius(state, values)\n'
                                  '    levels.set_byte(low16(values.selected), '
                                  'u8(levels.byte(low16(values.selected)) + 1))\n'
                                  '    outcome = check_growth_notification_owner(state, values)\n'
                                  '    values = outcome.values\n'
                                  '    attribute_pointer, owner_pointer = (assignments, '
                                  "_ram(state, 'f427'))\n"
                                  '    if not outcome.notification_requested:\n'
                                  '        continue\n'
                                  "    _put(state, 'f3d0', values.selected)\n"
                                  '    value = levels.byte(low16(values.selected))\n'
                                  "    _ram(state, 'f3c8').set_long(0, value)\n"
                                  '    _carry(state, True)\n'
                                  '    return GrowthScanObservation(replace(values, value=value), '
                                  'strength, intellect, levels, thresholds, attribute_pointer, '
                                  'owner_pointer, assignments, True, value == 0, False, False)'},
 'scan_officer_growth_levels': {'signature': 'state: SceneState, frame: GrowthFrame',
                                'returns': 'FullGrowthResult',
                                'flow': 'checked_context(frame, GrowthFrame, state)\n'
                                        'observed = _scan_officer_growth(state, frame.values, '
                                        'frame.attribute_pointer, frame.owner_pointer)\n'
                                        'return observed.complete(state)'}}

def _lower_advance_officer_growth_levels(emitter,rules):
    emitter.segment(0x662e4,0x66370)
    emitter.ins('lea.l','0xc000:w,%a0',4)
    emitter.ins('lea.l','0xbe00:w,%a1',4)
    emitter.ins('lea.l','0xc600:w,%a2',4)
    emitter.ins('lea.l','390(%pc),%a3',4)
    emitter.ins('nop','',2)
    emitter.ins('lea.l','0xcc00:w,%a6',4)
    emitter.ins('clr.w','0xef78:w',4)
    emitter.ins('move.w','0xef78:w,%d0',4)
    emitter.ins('cmpi.w','#0x100,%d0',4)
    emitter.ins('bcc.w','main_pc_066364',4)
    emitter.ins('cmpi.b','#0xff,(%a6, %d0.w)',6)
    emitter.ins('beq.w','main_pc_06632e',4)
    emitter.ins('clr.w','%d2',2)
    emitter.ins('move.b','(%a2, %d0.w),%d2',4)
    emitter.ins('lsl.w','#0x1,%d2',2)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','(%a0, %d0.w),%d1',4)
    emitter.ins('add.w','(%a1, %d0.w),%d1',4)
    emitter.ins('cmp.w','(%a3, %d2.w),%d1',4)
    emitter.ins('bcc.w','main_pc_066334',4)
    emitter.ins('addq.w','#0x1,0xef78:w',4)
    emitter.ins('bra.b','main_pc_0662fe',2)
    emitter.ins('bsr.w','main_pc_066370',4)
    emitter.ins('bsr.w','main_pc_0663a2',4)
    emitter.ins('bsr.w','main_pc_0663d4',4)
    emitter.ins('bsr.w','main_pc_06640e',4)
    emitter.ins('addq.b','#0x1,(%a2, %d0.w)',4)
    emitter.ins('bsr.w','main_pc_06643a',4)
    emitter.ins('bcc.b','main_pc_0662fe',2)
    emitter.ins('move.w','%d0,0xf3d0:w',4)
    emitter.ins('moveq','#0,%d1',2)
    emitter.ins('move.b','(%a2, %d0.w),%d1',4)
    emitter.ins('move.l','%d1,0xf3c8:w',4)
    emitter.ins('ori.w','#0x1,%sr',4)
    emitter.ins('bra.w','main_pc_06636e',4)
    emitter.ins('move.w','#0x1,0xcfcc:w',6)
    emitter.ins('andi.w','#0xfffe,%sr',4)
    emitter.ins('rts','',2)

def _lower_increase_growth_first_attribute(emitter,rules):
    emitter.segment(0x66370,0x663a2)
    emitter.ins('lea.l','0xb400:w,%a4',4)
    emitter.ins('move.w','(%a0, %d0.w),%d1',4)
    emitter.ins('move.w','%d1,%d2',2)
    emitter.ins('lsl.w','#0x1,%d1',2)
    emitter.ins('add.w','%d2,%d1',2)
    emitter.ins('add.w','(%a1, %d0.w),%d2',4)
    emitter.ins('andi.l','#0xffff,%d1',6)
    emitter.ins('divu.w','%d2,%d1',2)
    emitter.ins('move.w','(%a4, %d0.w),%d2',4)
    emitter.ins('add.w','%d1,%d2',2)
    emitter.ins('cmpi.w','#0xff,%d2',4)
    emitter.ins('bls.w','main_pc_06639c',4)
    emitter.ins('move.w','#0xff,%d2',4)
    emitter.ins('move.w','%d2,(%a4, %d0.w)',4)
    emitter.ins('rts','',2)

def _lower_increase_growth_second_attribute(emitter,rules):
    emitter.segment(0x663a2,0x663d4)
    emitter.ins('lea.l','0xb600:w,%a4',4)
    emitter.ins('move.w','(%a1, %d0.w),%d1',4)
    emitter.ins('move.w','%d1,%d2',2)
    emitter.ins('lsl.w','#0x1,%d1',2)
    emitter.ins('add.w','%d2,%d1',2)
    emitter.ins('add.w','(%a0, %d0.w),%d2',4)
    emitter.ins('andi.l','#0xffff,%d1',6)
    emitter.ins('divu.w','%d2,%d1',2)
    emitter.ins('move.w','(%a4, %d0.w),%d2',4)
    emitter.ins('add.w','%d1,%d2',2)
    emitter.ins('cmpi.w','#0xff,%d2',4)
    emitter.ins('bls.w','main_pc_0663ce',4)
    emitter.ins('move.w','#0xff,%d2',4)
    emitter.ins('move.w','%d2,(%a4, %d0.w)',4)
    emitter.ins('rts','',2)

def _lower_increase_growth_random_attribute(emitter,rules):
    emitter.segment(0x663d4,0x6640e)
    emitter.ins('move.w','%d0,-(%a7)',2)
    emitter.ins('jsr','main_pc_0083d4:l',6)
    emitter.ins('andi.l','#0xffff,%d0',6)
    emitter.ins('move.l','%d0,%d1',2)
    emitter.ins('lsl.l','#0x1,%d1',2)
    emitter.ins('add.l','%d0,%d1',2)
    emitter.ins('swap','%d1',2)
    emitter.ins('move.w','(%a7)+,%d0',2)
    emitter.ins('move.w','%d1,%d2',2)
    emitter.ins('lsl.w','#0x2,%d1',2)
    emitter.ins('add.w','%d2,%d1',2)
    emitter.ins('lea.l','0xb800:w,%a4',4)
    emitter.ins('move.w','(%a4, %d0.w),%d2',4)
    emitter.ins('add.w','%d1,%d2',2)
    emitter.ins('cmpi.w',"#"+hex(rules["growth_random_attribute_cap"])+",%d2",4)
    emitter.ins('bls.w','main_pc_066408',4)
    emitter.ins('move.w',"#"+hex(rules["growth_random_attribute_cap"])+",%d2",4)
    emitter.ins('move.w','%d2,(%a4, %d0.w)',4)
    emitter.ins('rts','',2)

def _lower_increase_growth_command_radius(emitter,rules):
    emitter.segment(0x6640e,0x6643a)
    emitter.ins('lsr.w','#0x1,%d0',2)
    emitter.ins('lea.l','0xc400:w,%a4',4)
    emitter.ins('cmpi.b','#0x14,(%a4, %d0.w)',6)
    emitter.ins('bcc.w','main_pc_066438',4)
    emitter.ins('move.w','%d0,-(%a7)',2)
    emitter.ins('jsr','main_pc_0083d4:l',6)
    emitter.ins('move.w','(%a7)+,%d0',2)
    emitter.ins('move.w','0xf61c:w,%d1',4)
    emitter.ins('btst.l','#0x4,%d1',4)
    emitter.ins('beq.w','main_pc_066438',4)
    emitter.ins('addq.b','#0x1,(%a4, %d0.w)',4)
    emitter.ins('rts','',2)

def _lower_check_growth_notification_owner(emitter,rules):
    emitter.segment(0x6643a,0x66478)
    emitter.ins('lea.l','0xcc00:w,%a4',4)
    emitter.ins('lea.l','0xf427:w,%a5',4)
    emitter.ins('move.b','(%a4, %d0.w),%d1',4)
    emitter.ins('bmi.w','main_pc_06646a',4)
    emitter.ins('andi.w','#0x3f,%d1',4)
    emitter.ins('move.b','(%a5, %d1.w),%d1',4)
    emitter.ins('cmp.b','0xf67b:w,%d1',4)
    emitter.ins('beq.w','main_pc_066472',4)
    emitter.ins('cmp.b','0xf67d:w,%d1',4)
    emitter.ins('beq.w','main_pc_066472',4)
    emitter.ins('cmp.b','0xf67f:w,%d1',4)
    emitter.ins('beq.w','main_pc_066472',4)
    emitter.ins('andi.w','#0xfffe,%sr',4)
    emitter.ins('bra.w','main_pc_066476',4)
    emitter.ins('ori.w','#0x1,%sr',4)
    emitter.ins('rts','',2)

def _lower_build_ten_officer_selection(emitter,rules):
    emitter.segment(0x664ac,0x66504)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('bsr.w','main_pc_066504',4)
    emitter.ins('cmpi.w','#0xa,%d0',4)
    emitter.ins('bcc.w','main_pc_0664e2',4)
    emitter.ins('move.w','#0x4,%d4',4)
    emitter.ins('bsr.w','main_pc_06657c',4)
    emitter.ins('cmpi.w','#0xa,%d0',4)
    emitter.ins('bcc.w','main_pc_0664e2',4)
    emitter.ins('move.w','#0x3,%d4',4)
    emitter.ins('bsr.w','main_pc_06657c',4)
    emitter.ins('cmpi.w','#0xa,%d0',4)
    emitter.ins('bcc.w','main_pc_0664e2',4)
    emitter.ins('move.w','#0x2,%d4',4)
    emitter.ins('bsr.w','main_pc_06657c',4)
    emitter.ins('lea.l','0xf100:w,%a0',4)
    emitter.ins('lea.l','0xf500:w,%a1',4)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.w','(%a0)+,(%a1)+',2)
    emitter.ins('bmi.w','main_pc_0664fa',4)
    emitter.ins('addq.w','#0x1,%d0',2)
    emitter.ins('cmpi.w','#0xa,%d0',4)
    emitter.ins('bcs.b','main_pc_0664ec',2)
    emitter.ins('move.w','#0xffff,(%a1)',4)
    emitter.ins('move.w','%d0,0xf636:w',4)
    emitter.ins('rts','',2)

def _lower_sort_high_loyalty_officers(emitter,rules):
    emitter.segment(0x66504,0x6657c)
    emitter.ins('lea.l','0xcc00:w,%a2',4)
    emitter.ins('lea.l','0xc300:w,%a3',4)
    emitter.ins('lea.l','0xf427:w,%a4',4)
    emitter.ins('move.w','0xefb0:w,%d1',4)
    emitter.ins('move.w','#0xff,%d2',4)
    emitter.ins('move.w','#0xffff,0xf100:w',6)
    emitter.ins('move.b','(%a2, %d2.w),%d3',4)
    emitter.ins('beq.w','main_pc_066576',4)
    emitter.ins('bmi.w','main_pc_066576',4)
    emitter.ins('andi.w','#0x3f,%d3',4)
    emitter.ins('cmp.b','(%a4, %d3.w),%d1',4)
    emitter.ins('bne.w','main_pc_066576',4)
    emitter.ins('cmpi.b','#0x5a,(%a3, %d2.w)',6)
    emitter.ins('bcs.w','main_pc_066576',4)
    emitter.ins('clr.w','%d3',2)
    emitter.ins('move.b','(%a3, %d2.w),%d3',4)
    emitter.ins('lea.l','0xf100:w,%a0',4)
    emitter.ins('lea.l','0xf200:w,%a1',4)
    emitter.ins('move.w','%d2,%d4',2)
    emitter.ins('tst.w','(%a0)',2)
    emitter.ins('bmi.w','main_pc_066562',4)
    emitter.ins('cmp.w','(%a1),%d3',2)
    emitter.ins('bhi.w','main_pc_066562',4)
    emitter.ins('addq.w','#0x2,%a0',2)
    emitter.ins('addq.w','#0x2,%a1',2)
    emitter.ins('bra.b','main_pc_066550',2)
    emitter.ins('move.w','(%a1),%d6',2)
    emitter.ins('move.w','%d3,(%a1)+',2)
    emitter.ins('move.w','%d6,%d3',2)
    emitter.ins('move.w','(%a0),%d5',2)
    emitter.ins('move.w','%d4,(%a0)+',2)
    emitter.ins('move.w','%d5,%d4',2)
    emitter.ins('bpl.b','main_pc_066562',2)
    emitter.ins('move.w','#0xffff,(%a0)',4)
    emitter.ins('addq.w','#0x1,%d0',2)
    emitter.ins('dbra','%d2,main_pc_06651e',4)
    emitter.ins('rts','',2)

def _lower_append_mid_loyalty_officers_by_trait(emitter,rules):
    emitter.segment(0x6657c,0x665e6)
    emitter.ins('lea.l','0xf100:w,%a0',4)
    emitter.ins('tst.w','(%a0)+',2)
    emitter.ins('bpl.b','main_pc_066580',2)
    emitter.ins('subq.w','#0x2,%a0',2)
    emitter.ins('lea.l','0xcc00:w,%a1',4)
    emitter.ins('lea.l','0xf427:w,%a2',4)
    emitter.ins('lea.l','0xc300:w,%a3',4)
    emitter.ins('lea.l','0xc700:w,%a4',4)
    emitter.ins('move.w','#0xff,%d1',4)
    emitter.ins('move.w','0xefb0:w,%d2',4)
    emitter.ins('move.b','(%a1, %d1.w),%d3',4)
    emitter.ins('beq.w','main_pc_0665dc',4)
    emitter.ins('bmi.w','main_pc_0665dc',4)
    emitter.ins('andi.w','#0x3f,%d3',4)
    emitter.ins('cmp.b','(%a2, %d3.w),%d2',4)
    emitter.ins('bne.w','main_pc_0665dc',4)
    emitter.ins('cmpi.b','#0x50,(%a3, %d1.w)',6)
    emitter.ins('bcs.w','main_pc_0665dc',4)
    emitter.ins('cmpi.b','#0x5a,(%a3, %d1.w)',6)
    emitter.ins('bcc.w','main_pc_0665dc',4)
    emitter.ins('move.b','(%a4, %d1.w),%d3',4)
    emitter.ins('andi.w','#0x7,%d3',4)
    emitter.ins('cmp.b','%d4,%d3',2)
    emitter.ins('bne.w','main_pc_0665dc',4)
    emitter.ins('move.w','%d1,(%a0)+',2)
    emitter.ins('addq.w','#0x1,%d0',2)
    emitter.ins('dbra','%d1,main_pc_06659e',4)
    emitter.ins('move.w','#0xffff,(%a0)',4)
    emitter.ins('rts','',2)

def _lower_dispatch_highbank_command_state(emitter,rules):
    emitter.segment(0x66bf4,0x66c10)
    emitter.ins('move.w','0xf362:w,%d0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','20(%pc, %d0.w),%d0',4)
    emitter.ins('jsr','40(%pc, %d0.w)',4)
    emitter.ins('jsr','main_pc_00d8ec:l',6)
    emitter.ins('jsr','main_pc_00a158:l',6)
    emitter.ins('rts','',2)

def _lower_select_highest_trait_officer(emitter,rules):
    emitter.segment(0x670b8,0x67126)
    emitter.ins('lea.l','0xcc00:w,%a0',4)
    emitter.ins('lea.l','0xc700:w,%a1',4)
    emitter.ins('lea.l','0xc300:w,%a2',4)
    emitter.ins('lea.l','0xb400:w,%a3',4)
    emitter.ins('lea.l','0xb600:w,%a4',4)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('clr.w','%d1',2)
    emitter.ins('move.w','#0xff,%d2',4)
    emitter.ins('move.b','(%a0, %d2.w),%d3',4)
    emitter.ins('beq.w','main_pc_067116',4)
    emitter.ins('andi.w','#0xc0,%d3',4)
    emitter.ins('bne.w','main_pc_067116',4)
    emitter.ins('move.b','(%a1, %d2.w),%d3',4)
    emitter.ins('andi.w','#0x7,%d3',4)
    emitter.ins('cmp.w','%d0,%d3',2)
    emitter.ins('bcs.w','main_pc_067116',4)
    emitter.ins('beq.w','main_pc_0670f8',4)
    emitter.ins('clr.w','%d1',2)
    emitter.ins('move.w','%d3,%d0',2)
    emitter.ins('clr.w','%d3',2)
    emitter.ins('move.b','(%a2, %d2.w),%d3',4)
    emitter.ins('move.w','%d2,%d4',2)
    emitter.ins('lsl.w','#0x1,%d4',2)
    emitter.ins('add.w','(%a3, %d4.w),%d3',4)
    emitter.ins('add.w','(%a4, %d4.w),%d3',4)
    emitter.ins('cmp.w','%d1,%d3',2)
    emitter.ins('bls.w','main_pc_067116',4)
    emitter.ins('move.w','%d3,%d1',2)
    emitter.ins('move.w','%d2,%d7',2)
    emitter.ins('dbra','%d2,main_pc_0670d4',4)
    emitter.ins('move.w','%d7,0xf3a6:w',4)
    emitter.ins('andi.w','#0xff,0xf376:w',6)
    emitter.ins('rts','',2)

def _lower_calculate_force_command_budget(emitter,rules):
    emitter.segment(0x67126,0x671b0)
    emitter.ins('lea.l','0xe320:w,%a0',4)
    emitter.ins('move.w','#0x27,%d0',4)
    emitter.ins('moveq','#0,%d1',2)
    emitter.ins('add.l','(%a0)+,%d1',2)
    emitter.ins('dbra','%d0,main_pc_067130',4)
    emitter.ins('divu.w','#0x28,%d1',4)
    emitter.ins('lea.l','0xc300:w,%a0',4)
    emitter.ins('lea.l','0xcc00:w,%a1',4)
    emitter.ins('move.w','#0xff,%d0',4)
    emitter.ins('moveq','#0,%d2',2)
    emitter.ins('clr.w','%d3',2)
    emitter.ins('clr.w','%d4',2)
    emitter.ins('move.b','(%a1, %d0.w),%d4',4)
    emitter.ins('beq.w','main_pc_067164',4)
    emitter.ins('andi.w','#0xc0,%d4',4)
    emitter.ins('bne.w','main_pc_067164',4)
    emitter.ins('move.b','(%a0, %d0.w),%d4',4)
    emitter.ins('add.w','%d4,%d2',2)
    emitter.ins('addq.w','#0x1,%d3',2)
    emitter.ins('dbra','%d0,main_pc_06714c',4)
    emitter.ins('lea.l','0x9000:w,%a1',4)
    emitter.ins('move.b','(%a1),%d4',2)
    emitter.ins('andi.w','#0xf,%d4',4)
    emitter.ins('beq.w','main_pc_0671a0',4)
    emitter.ins('move.b','0x4(%a1),%d5',4)
    emitter.ins('cmp.b','0xf377:w,%d5',4)
    emitter.ins('bne.w','main_pc_067194',4)
    emitter.ins('subq.w','#0x1,%d4',2)
    emitter.ins('move.b','0xd(%a0, %d4.w),%d5',4)
    emitter.ins('move.b','(%a1, %d5.w),%d5',4)
    emitter.ins('add.w','%d5,%d2',2)
    emitter.ins('addq.w','#0x1,%d3',2)
    emitter.ins('dbra','%d4,main_pc_067184',4)
    emitter.ins('move.b','(%a1),%d4',2)
    emitter.ins('andi.w','#0xf,%d4',4)
    emitter.ins('lea.l','0xd(%a1, %d4.w),%a1',4)
    emitter.ins('bra.b','main_pc_06716c',2)
    emitter.ins('divu.w','%d3,%d2',2)
    emitter.ins('add.w','%d2,%d1',2)
    emitter.ins('mulu.w','%d3,%d1',2)
    emitter.ins('divu.w','#0x118,%d1',4)
    emitter.ins('move.w','%d1,0xefdc:w',4)
    emitter.ins('rts','',2)

def _lower_advance_scrolling_message(emitter,rules):
    emitter.segment(0x671b6,0x67238)
    emitter.ins('subq.w','#0x1,0xefda:w',4)
    emitter.ins('bne.w','main_pc_067236',4)
    emitter.ins('move.w','0xefd8:w,%d0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','-22(%pc, %d0.w),0xefda:w',6)
    emitter.ins('movea.l','0xf3be:w,%a0',4)
    emitter.ins('addq.l','#0x2,0xf3be:w',4)
    emitter.ins('move.w','(%a0),%d0',2)
    emitter.ins('move.w','%d0,0xf77c:w',4)
    emitter.ins('beq.b','main_pc_06720a',2)
    emitter.ins('bmi.b','main_pc_06722a',2)
    emitter.ins('lea.l','0xd100:w,%a0',4)
    emitter.ins('adda.w','0xf31a:w,%a0',4)
    emitter.ins('bsr.w','main_pc_067354',4)
    emitter.ins('bsr.w','main_pc_06738c',4)
    emitter.ins('addi.w','#0x12,0xf37c:w',6)
    emitter.ins('cmpi.w','#0x120,0xf37c:w',6)
    emitter.ins('bcs.w','main_pc_067236',4)
    emitter.ins('eori.w','#0x1,0xf37a:w',6)
    emitter.ins('clr.w','0xf37c:w',4)
    emitter.ins('bra.w','main_pc_067236',4)
    emitter.ins('lea.l','0xd100:w,%a0',4)
    emitter.ins('adda.w','0xf31a:w,%a0',4)
    emitter.ins('bsr.w','main_pc_067354',4)
    emitter.ins('lea.l','658(%pc),%a2',4)
    emitter.ins('nop','',2)
    emitter.ins('bsr.w','main_pc_0673a6',4)
    emitter.ins('addi.w','#0x12,0xf37c:w',6)
    emitter.ins('bra.w','main_pc_067236',4)
    emitter.ins('andi.w','#0xff,%d0',4)
    emitter.ins('move.w','8(%pc, %d0.w),%d0',4)
    emitter.ins('jmp','26(%pc, %d0.w)',4)
    emitter.ins('rts','',2)

def _lower_append_scrolling_message_header(emitter,rules):
    emitter.segment(0x67354,0x6738c)
    emitter.ins('move.w','#0x4060,%d1',4)
    emitter.ins('tst.w','0xf37a:w',4)
    emitter.ins('beq.b','main_pc_067362',2)
    emitter.ins('move.w','#0x4090,%d1',4)
    emitter.ins('move.w','%d1,(%a0)+',2)
    emitter.ins('move.w','0xf37c:w,%d1',4)
    emitter.ins('andi.w','#0xfff8,%d1',4)
    emitter.ins('move.w','%d1,%d2',2)
    emitter.ins('add.w','%d2,%d1',2)
    emitter.ins('tst.w','0xf37a:w',4)
    emitter.ins('beq.b','main_pc_067378',2)
    emitter.ins('add.w','%d2,%d1',2)
    emitter.ins('lsl.w','#0x2,%d1',2)
    emitter.ins('addi.w','#0xa0a0,%d1',4)
    emitter.ins('tst.w','0xf37a:w',4)
    emitter.ins('beq.b','main_pc_067388',2)
    emitter.ins('addi.w','#0x900,%d1',4)
    emitter.ins('move.w','%d1,(%a0)+',2)
    emitter.ins('rts','',2)

def _lower_append_scrolling_message_glyph(emitter,rules):
    emitter.segment(0x6738c,0x6746a)
    emitter.ins('move.w','%d0,%d1',2)
    emitter.ins('andi.w','#0xff00,%d1',4)
    emitter.ins('lsl.w','#0x3,%d1',2)
    emitter.ins('andi.w','#0xff,%d0',4)
    emitter.ins('lsl.w','#0x5,%d0',2)
    emitter.ins('or.w','%d1,%d0',2)
    emitter.ins('lea.l','0x8159c:l,%a2',6)
    emitter.ins('lea.l','(%a2, %d0.w),%a2',4)
    emitter.ins('move.w','#0x40,%d2',4)
    emitter.ins('lea.l','0xf516:w,%a1',4)
    emitter.ins('tst.w','0xf37a:w',4)
    emitter.ins('beq.b','main_pc_0673ce',2)
    emitter.ins('move.w','#0x60,%d2',4)
    emitter.ins('move.w','#0x3,%d1',4)
    emitter.ins('bsr.w','main_pc_06748e',4)
    emitter.ins('move.l','%d5,0xc0(%a0)',4)
    emitter.ins('move.l','%d5,0x60(%a0)',4)
    emitter.ins('move.l','%d5,(%a0)+',2)
    emitter.ins('dbra','%d1,main_pc_0673bc',4)
    emitter.ins('move.w','%d2,%d3',2)
    emitter.ins('lsl.w','#0x1,%d3',2)
    emitter.ins('add.w','%d3,0xf31a:w',4)
    emitter.ins('add.w','%d2,0xf31a:w',4)
    emitter.ins('addi.w','#0x4,0xf31a:w',6)
    emitter.ins('swap','%d2',2)
    emitter.ins('swap','%d3',2)
    emitter.ins('move.w','#0xf,%d2',4)
    emitter.ins('move.w','0xf37c:w,%d3',4)
    emitter.ins('andi.w','#0x7,%d3',4)
    emitter.ins('bsr.w','main_pc_06746a',4)
    emitter.ins('jsr','main_pc_00af04:l',6)
    emitter.ins('move.l','%d7,-(%a7)',2)
    emitter.ins('jsr','main_pc_00af04:l',6)
    emitter.ins('move.l','(%a7)+,%d4',2)
    emitter.ins('bsr.w','main_pc_06748e',4)
    emitter.ins('move.w','%d3,%d6',2)
    emitter.ins('beq.b','main_pc_06742c',2)
    emitter.ins('lsl.w','#0x2,%d6',2)
    emitter.ins('subq.w','#0x1,%d6',2)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('andi.w','#0xffef,%sr',4)
    emitter.ins('roxr.l','#0x1,%d4',2)
    emitter.ins('roxr.l','#0x1,%d7',2)
    emitter.ins('roxr.l','#0x1,%d5',2)
    emitter.ins('ori.w','#0x10,%sr',4)
    emitter.ins('roxr.l','#0x1,%d0',2)
    emitter.ins('dbra','%d6,main_pc_067412',4)
    emitter.ins('move.l','(%a1),%d1',2)
    emitter.ins('and.l','%d0,%d1',2)
    emitter.ins('or.l','%d1,%d4',2)
    emitter.ins('swap','%d2',2)
    emitter.ins('swap','%d3',2)
    emitter.ins('move.l','%d5,(%a0, %d3.w)',4)
    emitter.ins('move.l','%d7,(%a0, %d2.w)',4)
    emitter.ins('move.l','%d4,(%a0)+',2)
    emitter.ins('move.l','%d5,(%a1)+',2)
    emitter.ins('swap','%d2',2)
    emitter.ins('swap','%d3',2)
    emitter.ins('dbra','%d2,main_pc_0673f0',4)
    emitter.ins('swap','%d2',2)
    emitter.ins('swap','%d3',2)
    emitter.ins('tst.w','0xf37a:w',4)
    emitter.ins('beq.b','main_pc_067464',2)
    emitter.ins('move.w','#0x3,%d1',4)
    emitter.ins('bsr.w','main_pc_06748e',4)
    emitter.ins('move.l','%d5,(%a0, %d3.w)',4)
    emitter.ins('move.l','%d5,(%a0, %d2.w)',4)
    emitter.ins('move.l','%d5,(%a0)+',2)
    emitter.ins('dbra','%d1,main_pc_067452',4)
    emitter.ins('clr.w','(%a0, %d3.w)',4)
    emitter.ins('rts','',2)

def _lower_lookup_message_layout_words(emitter,rules):
    emitter.segment(0x6746a,0x6747e)
    emitter.ins('move.w','0xf6c4:w,%d0',4)
    emitter.ins('lsl.w','#0x2,%d0',2)
    emitter.ins('lea.l','12(%pc),%a3',4)
    emitter.ins('nop','',2)
    emitter.ins('movem.w','(%a3, %d0.w),%d0-%d1',6)
    emitter.ins('rts','',2)

def _lower_lookup_message_fill_pattern(emitter,rules):
    emitter.segment(0x6748e,0x6749a)
    emitter.ins('move.w','0xf6c4:w,%d5',4)
    emitter.ins('lsl.w','#0x2,%d5',2)
    emitter.ins('move.l','4(%pc, %d5.w),%d5',4)
    emitter.ins('rts','',2)

def _lower_advance_message_decoration_stage(emitter,rules):
    emitter.segment(0x674ca,0x67502)
    emitter.ins('lea.l','0xd100:w,%a0',4)
    emitter.ins('adda.w','0xf31a:w,%a0',4)
    emitter.ins('bsr.w','main_pc_06750a',4)
    emitter.ins('move.w','0xf36a:w,%d0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','36(%pc, %d0.w),%d0',4)
    emitter.ins('jsr','60(%pc, %d0.w)',4)
    emitter.ins('addq.w','#0x1,0xf36a:w',4)
    emitter.ins('move.w','0xf36a:w,%d0',4)
    emitter.ins('cmpi.w','#0x4,%d0',4)
    emitter.ins('bcs.b','main_pc_067500',2)
    emitter.ins('addq.w','#0x1,0xf362:w',4)
    emitter.ins('clr.w','0xf36a:w',4)
    emitter.ins('bset.b','#0x6,0xf3a4:w',6)
    emitter.ins('rts','',2)

def _lower_lookup_message_decoration_style(emitter,rules):
    emitter.segment(0x6750a,0x67516)
    emitter.ins('move.w','0xf6c4:w,%d0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','4(%pc, %d0.w),%d2',4)
    emitter.ins('rts','',2)

def _lower_dispatch_message_control(emitter,rules):
    emitter.segment(0x676c4,0x676d6)
    emitter.ins('move.w','0xf380:w,%d0',4)
    emitter.ins('cmpi.w','#0x60,%d0',4)
    emitter.ins('bcc.b','main_pc_0676de',2)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','4(%pc, %d0.w),%d0',4)
    emitter.ins('bra.b','main_pc_0676f2',2)
    emitter.segment(0x676de,0x676f2)
    emitter.ins('subi.w','#0x60,%d0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','102(%pc, %d0.w),%d0',4)
    emitter.ins('lea.l','200(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','(%a0, %d0.w)',4)

def _lower_render_force_city_markers(emitter,rules):
    emitter.segment(0x679fc,0x67b10)
    emitter.ins('cmpi.w','#0x200,0xf612:w',6)
    emitter.ins('bne.w','main_pc_067a10',4)
    emitter.ins('cmpi.w','#0x10,0xf352:w',6)
    emitter.ins('bls.w','main_pc_067b0e',4)
    emitter.ins('tst.w','0xefc8:w',4)
    emitter.ins('bne.w','main_pc_067a36',4)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('lea.l','626(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','#0x2000,%d0',4)
    emitter.ins('jsr','main_pc_03ab52:l',6)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('move.w','#0x1,0xefc8:w',6)
    emitter.ins('cmpi.w','#0x20,0xf352:w',6)
    emitter.ins('bne.b','main_pc_067a70',2)
    emitter.ins('move.w','#0x0,0xfb50:w',6)
    emitter.ins('move.w','#0xe40,0xfb52:w',6)
    emitter.ins('move.w','#0xaee,0xfb54:w',6)
    emitter.ins('move.w','#0xa0e,0xfb56:w',6)
    emitter.ins('move.w','#0x2e0,0xfb58:w',6)
    emitter.ins('move.w','#0xce,0xfb5a:w',6)
    emitter.ins('move.w','#0xea0,0xfb5c:w',6)
    emitter.ins('move.w','#0x0,0xfb5e:w',6)
    emitter.ins('bra.b','main_pc_067aa0',2)
    emitter.ins('move.w','#0x0,0xfb50:w',6)
    emitter.ins('move.w','#0xe40,0xfb52:w',6)
    emitter.ins('move.w','#0xaee,0xfb54:w',6)
    emitter.ins('move.w','#0xa0e,0xfb56:w',6)
    emitter.ins('move.w','#0x2e0,0xfb58:w',6)
    emitter.ins('move.w','#0xce,0xfb5a:w',6)
    emitter.ins('move.w','#0xea0,0xfb5c:w',6)
    emitter.ins('move.w','#0x0,0xfb5e:w',6)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('movem.l','%d0,-(%a7)',4)
    emitter.ins('moveq','#0,%d1',2)
    emitter.ins('lea.l','0xf428:w,%a0',4)
    emitter.ins('move.b','(%a0, %d0.w),%d1',4)
    emitter.ins('cmpi.b','#0xff,%d1',4)
    emitter.ins('beq.b','main_pc_067b02',2)
    emitter.ins('asl.w','#0x1,%d1',2)
    emitter.ins('movem.l','%d0,-(%a7)',4)
    emitter.ins('move.w','0xf320:w,%d0',4)
    emitter.ins('lsr.w','#0x3,%d0',2)
    emitter.ins('andi.w','#0x1,%d0',4)
    emitter.ins('add.w','%d0,%d1',2)
    emitter.ins('asl.w','#0x2,%d1',2)
    emitter.ins('lea.l','68(%pc),%a1',4)
    emitter.ins('nop','',2)
    emitter.ins('movea.l','(%a1, %d1.w),%a0',4)
    emitter.ins('movem.l','(%a7)+,%d0',4)
    emitter.ins('move.w','%d0,%d2',2)
    emitter.ins('asl.w','#0x2,%d2',2)
    emitter.ins('lea.l','0xd4aca:l,%a1',6)
    emitter.ins('move.w','0x2(%a1, %d2.w),%d0',4)
    emitter.ins('subi.w','#0x10,%d0',4)
    emitter.ins('move.w','(%a1, %d2.w),%d1',4)
    emitter.ins('clr.w','%d2',2)
    emitter.ins('move.w','0xf314:w,0xf60a:w',6)
    emitter.ins('move.w','0xf318:w,0xf60e:w',6)
    emitter.ins('jsr','main_pc_00ac10:l',6)
    emitter.ins('movem.l','(%a7)+,%d0',4)
    emitter.ins('addq.w','#0x1,%d0',2)
    emitter.ins('cmpi.w','#0x28,%d0',4)
    emitter.ins('bcs.b','main_pc_067aa2',2)
    emitter.ins('rts','',2)

LOWERERS={
    'advance_officer_growth_levels':_lower_advance_officer_growth_levels,
    'increase_growth_first_attribute':_lower_increase_growth_first_attribute,
    'increase_growth_second_attribute':_lower_increase_growth_second_attribute,
    'increase_growth_random_attribute':_lower_increase_growth_random_attribute,
    'increase_growth_command_radius':_lower_increase_growth_command_radius,
    'check_growth_notification_owner':_lower_check_growth_notification_owner,
    'build_ten_officer_selection':_lower_build_ten_officer_selection,
    'sort_high_loyalty_officers':_lower_sort_high_loyalty_officers,
    'append_mid_loyalty_officers_by_trait':_lower_append_mid_loyalty_officers_by_trait,
    'dispatch_highbank_command_state':_lower_dispatch_highbank_command_state,
    'select_highest_trait_officer':_lower_select_highest_trait_officer,
    'calculate_force_command_budget':_lower_calculate_force_command_budget,
    'advance_scrolling_message':_lower_advance_scrolling_message,
    'append_scrolling_message_header':_lower_append_scrolling_message_header,
    'append_scrolling_message_glyph':_lower_append_scrolling_message_glyph,
    'lookup_message_layout_words':_lower_lookup_message_layout_words,
    'lookup_message_fill_pattern':_lower_lookup_message_fill_pattern,
    'advance_message_decoration_stage':_lower_advance_message_decoration_stage,
    'lookup_message_decoration_style':_lower_lookup_message_decoration_style,
    'dispatch_message_control':_lower_dispatch_message_control,
    'render_force_city_markers':_lower_render_force_city_markers,
}


# Finite actual new algorithm contracts, not old-body normalization.
APPROVED['contexts_render'] = {'RenderFields', 'checked_render_fields'}
APPROVED['contexts_tick'] = {'MapTickFrame', 'checked_tick_frame'}
APPROVED['business_gameplay'] = {'_render_move', '_render_compare', '_render_sprite_fields',
    '_render_from_tick', '_render_to_tick', '_render_push_value', '_render_pop_value',
    '_render_enter_call', '_render_leave_call'}
APPROVED['services'].update({'write_vdp_swapped_byte_rle_stream_complete', 'SwappedByteRleRetained'})
RENDER_ACTUAL_DECLARATIONS = {'render_force_city_markers': {'signature': 'state: SceneState, layout: MessageLayout',
                               'returns': 'MessageLayout',
                               'flow': 'checked_context(layout, MessageLayout, state)\n'
                                       'fields = RenderFields(layout.symbol, layout.position, '
                                       'layout.stride, layout.row_offset, layout.first_plane, '
                                       'layout.fill, layout.shift_count, layout.second_plane, '
                                       'layout.bitmap, layout.destination, layout.previous_rows, '
                                       'None, None, None, None, None)\n'
                                       'result = _force_render_fields(state, fields)\n'
                                       'return replace(layout, symbol=result.x, position=result.y, '
                                       'stride=result.attributes)'},
 '_force_render_fields': {'signature': 'state, fields',
                          'returns': None,
                          'flow': 'from .services import '
                                  'write_vdp_swapped_byte_rle_stream_complete, '
                                  'SwappedByteRleRetained\n'
                                  'from .domain import VideoPlaneAddress\n'
                                  'from .business_gameplay import _render_move, _render_compare, '
                                  '_render_sprite_fields, _render_push_value, _render_pop_value, '
                                  '_render_enter_call, _render_leave_call\n'
                                  'checked_render_fields(fields, state)\n'
                                  "mode = _word(state, 'f612')\n"
                                  'fields = _render_compare(fields, mode, 512, 16)\n'
                                  'if mode == 512:\n'
                                  "    phase = _word(state, 'f352')\n"
                                  '    fields = _render_compare(fields, phase, 16, 16)\n'
                                  '    if phase <= 16:\n'
                                  '        return fields\n'
                                  "cached = _word(state, 'efc8')\n"
                                  'fields = _render_move(fields, cached, 16)\n'
                                  'if not cached:\n'
                                  '    state.set_status_word(9984)\n'
                                  '    fields = _render_enter_call(fields)\n'
                                  '    decoded = write_vdp_swapped_byte_rle_stream_complete(state, '
                                  "data_view(state, 'data_067c90').cursor(), "
                                  'VideoPlaneAddress(replace_word(fields.x, 8192)), '
                                  'SwappedByteRleRetained(fields.y, fields.attributes, '
                                  'fields.officer))\n'
                                  '    fields = replace(fields, source=decoded.source, '
                                  'x=decoded.command_carrier, y=decoded.marker_carrier, '
                                  'attributes=decoded.token_carrier, tile=decoded.count_carrier, '
                                  'officer=decoded.packed_word_carrier, carry=decoded.carry, '
                                  'zero=decoded.zero, negative=decoded.negative, '
                                  'overflow=decoded.overflow)\n'
                                  '    fields = _render_leave_call(fields)\n'
                                  '    state.set_status_word(9472)\n'
                                  "    _put(state, 'efc8', 1)\n"
                                  "phase = _word(state, 'f352')\n"
                                  'fields = _render_compare(fields, phase, 32, 16)\n'
                                  "palette = _ram(state, 'fb50')\n"
                                  'for offset, color in ((0, 0), (2, 3648), (4, 2798), (6, 2574), '
                                  '(8, 736), (10, 206), (12, 3744), (14, 0)):\n'
                                  '    palette.set_word(offset, color)\n'
                                  'fields = _render_move(replace(fields, x=0), 0, 32)\n'
                                  'while True:\n'
                                  '    city = fields.x\n'
                                  '    saved_city = city\n'
                                  '    fields = _render_push_value(state, fields, city)\n'
                                  "    source = _ram(state, 'f428')\n"
                                  '    owner = source.byte(low16(city))\n'
                                  '    fields = _render_compare(replace(fields, x=city, y=owner, '
                                  'source=source), owner, 255, 8)\n'
                                  '    if owner != 255:\n'
                                  '        fields = _render_push_value(state, fields, fields.x)\n'
                                  "        animation = _word(state, 'f320')\n"
                                  '        selector = u16((owner << 1) + (animation >> 3 & 1) << '
                                  '2)\n'
                                  "        directory = data_view(state, 'data_067b10')\n"
                                  '        pointer = directory.long(selector)\n'
                                  '        fields, restored_city = _render_pop_value(state, '
                                  'fields, city)\n'
                                  '        city = restored_city\n'
                                  "        coordinates = data_view(state, 'data_0d4aca')\n"
                                  '        offset = u16(low16(city) << 2)\n'
                                  '        x = replace_word(city, u16(coordinates.word(offset, '
                                  'displacement=2) - 16))\n'
                                  '        y = replace_word(selector, coordinates.word(offset))\n'
                                  '        attributes = replace_word(fields.attributes, 0)\n'
                                  '        fields = replace(fields, x=x, y=y, '
                                  'attributes=attributes, source=state.table_at(pointer).cursor(), '
                                  'destination=coordinates)\n'
                                  "        _put(state, 'f60a', _word(state, 'f314'))\n"
                                  "        _put(state, 'f60e', _word(state, 'f318'))\n"
                                  '        fields = _render_sprite_fields(state, fields)\n'
                                  '    fields, restored_city = _render_pop_value(state, fields, '
                                  'saved_city)\n'
                                  '    next_city = replace_word(restored_city, '
                                  'u16(low16(restored_city) + 1))\n'
                                  '    fields = _render_compare(replace(fields, x=next_city), '
                                  'next_city, 40, 16)\n'
                                  '    if not fields.carry:\n'
                                  '        return fields'},
 'render_force_city_markers_complete': {'signature': 'state: SceneState, frame: MapTickFrame',
                                        'returns': 'MapTickFrame',
                                        'flow': 'from .business_gameplay import _render_from_tick, '
                                                '_render_to_tick\n'
                                                'fields = _force_render_fields(state, '
                                                '_render_from_tick(state, frame))\n'
                                                'return _render_to_tick(state, frame, fields)'}}
DECLARATIONS.update(RENDER_ACTUAL_DECLARATIONS)
RENDER_OWNER_ALGORITHMS = {'render_force_city_markers': ['render_force_city_markers_fields']}

# Complete actual field-core contracts; ordinary lowerers unchanged.
APPROVED['contexts_highbank'].add('ScrollingMessageAdvance')
DECLARATIONS.update({'_advance_scrolling_message_core': {'signature': 'state: SceneState, layout: MessageLayout | None',
                                     'returns': 'ScrollingMessageAdvance',
                                     'flow': 'checked_state(state)\n'
                                             'if layout is not None:\n'
                                             '    checked_context(layout, MessageLayout, state)\n'
                                             "timer = u16(_word(state, 'efda') - 1)\n"
                                             "_put(state, 'efda', timer)\n"
                                             'if timer:\n'
                                             '    return ScrollingMessageAdvance(layout, timer)\n'
                                             'if layout is None:\n'
                                             "    raise Boundary('due 671B6 message needs current "
                                             'D0..D7/A0/A1/A2 MessageLayout; SceneTick has no such '
                                             "live input')\n"
                                             'symbol = replace_word(layout.symbol, '
                                             "u16(_word(state, 'efd8') << 1))\n"
                                             "_put(state, 'efda', data_view(state, "
                                             "'data_0671b0').word(low16(symbol)))\n"
                                             'source = state.table_at(_ram(state, '
                                             "'f3be').long()).cursor()\n"
                                             "_ram(state, 'f3be').set_long(0, u32(_ram(state, "
                                             "'f3be').long() + 2))\n"
                                             'symbol = replace_word(symbol, source.word())\n'
                                             "_put(state, 'f77c', symbol)\n"
                                             'layout = replace(layout, symbol=symbol)\n'
                                             'if not negative_word(low16(symbol)):\n'
                                             '    layout = append_scrolling_message_header(state, '
                                             'replace(layout, destination=_ram(state, '
                                             "'d100').cursor(_word(state, 'f31a'))))\n"
                                             '    if low16(symbol):\n'
                                             '        layout = '
                                             'append_scrolling_message_glyph(state, layout)\n'
                                             "        _put(state, 'f37c', u16(_word(state, 'f37c') "
                                             '+ 18))\n'
                                             "        if _word(state, 'f37c') >= 288:\n"
                                             "            _put(state, 'f37a', _word(state, 'f37a') "
                                             '^ 1)\n'
                                             "            _word(state, 'f37c')\n"
                                             "            _put(state, 'f37c', 0)\n"
                                             '    else:\n'
                                             '        layout = '
                                             'append_scrolling_message_bitmap(state, '
                                             'replace(layout, bitmap=data_view(state, '
                                             "'data_0674aa').cursor()))\n"
                                             "        _put(state, 'f37c', u16(_word(state, 'f37c') "
                                             '+ 18))\n'
                                             '    return ScrollingMessageAdvance(layout, timer)\n'
                                             'selector = replace_word(symbol, low16(symbol) & '
                                             '255)\n'
                                             'selector = replace_word(selector, data_view(state, '
                                             "'data_067238').word(low16(selector)))\n"
                                             'return '
                                             'ScrollingMessageAdvance(_dispatch_message(state, '
                                             '422478 + s16(low16(selector)), selector, layout, '
                                             '422450), timer)'}})

DECLARATIONS.update({'dispatch_message_control_fields': {'signature': 'state: SceneState, layout: MessageLayout | None=None',
 'returns': 'MessageControlFields',
 'flow': 'checked_state(state)\n'
         'if layout is not None:\n'
         '    checked_context(layout, MessageLayout, state)\n'
         "selector = _word(state, 'f380')\n"
         'current = None\n'
         'handler_field = None\n'
         'handler_tile = None\n'
         'handler_destination = None\n'
         'if selector < 96:\n'
         '    selector = u16(selector << 1)\n'
         "    selector = data_view(state, 'data_0676d6').word(s16(selector))\n"
         'else:\n'
         '    selector = u16(selector - 96 << 1)\n'
         "    selector = data_view(state, 'data_06774c').word(s16(selector))\n"
         '    handler_destination = state.table_at(423858).cursor()\n'
         '    target = 423858 + s16(selector)\n'
         '    from .services import enter_special_message_mode_fields, '
         'fixed_special_message_fields, choose_special_message_for_action_fields\n'
         '    if target == 423858:\n'
         '        selected = enter_special_message_mode_fields(state)\n'
         '    elif target == 424098:\n'
         '        selected = fixed_special_message_fields(state)\n'
         '    elif target == 424104:\n'
         '        selected = choose_special_message_for_action_fields(state)\n'
         '    else:\n'
         '        selected = None\n'
         '    if selected is None:\n'
         '        if layout is None:\n'
         "            raise Boundary('676EE target requires actual complete MessageLayout or "
         "recovered WORD handler')\n"
         '        actual = replace(layout, symbol=replace_word(layout.symbol, selector), '
         'destination=handler_destination)\n'
         '        current = _dispatch_message(state, target, actual.symbol, actual, 423666)\n'
         '        selector = low16(current.symbol)\n'
         '    else:\n'
         '        selected.validate(state)\n'
         '        selector = selected.value\n'
         '        handler_field = selected.field_if_written\n'
         '        handler_tile = selected.tile_if_written\n'
         '        if selected.destination_if_written is not None:\n'
         '            handler_destination = selected.destination_if_written.cursor()\n'
         '        if layout is not None:\n'
         '            current = replace(layout, symbol=replace_word(layout.symbol, selector), '
         'position=layout.position if handler_field is None else replace_word(layout.position, '
         'handler_field), stride=layout.stride if handler_tile is None else '
         'replace_word(layout.stride, handler_tile), destination=handler_destination)\n'
         'from .services import prepare_scene_message_fields\n'
         'message = prepare_scene_message_fields(state, selector)\n'
         'if message.resolved is None:\n'
         '    return MessageControlFields(selector, handler_field, handler_destination, None, '
         'current, message.carry, message.zero, message.negative, message.overflow, '
         'handler_tile).validate(state)\n'
         'return MessageControlFields(message.layout_offset, message.resolved.item_offset, '
         'state.table_at(message.resolved.pointer).cursor(), '
         'state.table_at(message.resolved.descriptor).cursor(), current, message.carry, '
         'message.zero, message.negative, message.overflow, handler_tile).validate(state)'}})


APPROVED.setdefault('contexts_highbank', set()).update({'MessageControlFields'})
APPROVED.setdefault('services', set()).update({'prepare_scene_message_fields'})


APPROVED.setdefault('services', set()).update({'enter_special_message_mode_fields', 'fixed_special_message_fields', 'choose_special_message_for_action_fields'})

def compile_source(source):
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    records['advance_officer_growth_levels']['effects'] = dict(actual_shared_algorithm=records['_scan_officer_growth']['effects'], strict_complete_return=records['scan_officer_growth_levels']['effects'], legacy_observation_projection=records['advance_officer_growth_levels']['effects'])
    records['render_force_city_markers']['effects'] = dict(legacy_projection=records['render_force_city_markers']['effects'], actual_complete_algorithm=records['render_force_city_markers_fields']['effects'], strict_live_projection=records['render_force_city_markers_complete']['effects'], legacy_render_projection=records['_force_render_fields']['effects'], supplied_call_fields={name: records[name]['effects'] for name in ('_force_render_entry_fields', '_highbank_frame_fields', '_highbank_write_fields', '_highbank_child_fields', '_highbank_target_fields')})
    records['dispatch_message_control']['effects'] = dict(legacy_projection=records['dispatch_message_control']['effects'], supplied_unique_fields={name: records[name]['effects'] for name in ('dispatch_message_control_fields',)})
    records['advance_officer_growth_levels']['effects']['actual_full_fields'] = {name: records[name]['effects'] for name in ('_growth_carry_fields', '_growth_project_values_fields', '_growth_ratio_attribute_fields', '_growth_saved_index_random_fields', 'advance_officer_growth_levels_fields', 'check_growth_notification_owner_fields', 'increase_growth_command_radius_fields', 'increase_growth_first_attribute_fields', 'increase_growth_random_attribute_fields', 'increase_growth_second_attribute_fields')}
    for owner in ('increase_growth_first_attribute', 'increase_growth_second_attribute', 'increase_growth_random_attribute', 'increase_growth_command_radius', 'check_growth_notification_owner'):
        records[owner]['effects'] += '\nsole complete growth fields: ' + '\n'.join((records[name]['effects'] for name in ('_growth_carry_fields', '_growth_project_values_fields', '_growth_ratio_attribute_fields', '_growth_saved_index_random_fields', 'advance_officer_growth_levels_fields', 'check_growth_notification_owner_fields', 'increase_growth_command_radius_fields', 'increase_growth_first_attribute_fields', 'increase_growth_random_attribute_fields', 'increase_growth_second_attribute_fields')))
    sole_highbank_fields = {name: records[name]['effects'] for name in ('_highbank_frame_fields', '_highbank_write_fields', '_highbank_memory_add_fields', '_highbank_shift_fields', '_highbank_dbra_fields', '_highbank_child_fields', '_highbank_target_fields', 'sort_high_loyalty_officers_fields', 'append_mid_loyalty_officers_by_trait_fields', 'build_ten_officer_selection_fields', 'select_highest_trait_officer_fields', 'calculate_force_command_budget_fields', 'dispatch_highbank_command_state_fields', 'lookup_message_layout_words_fields', 'lookup_message_fill_pattern_fields', 'lookup_message_decoration_style_fields', 'append_scrolling_message_header_fields', '_highbank_roxr_plane_fields', 'append_scrolling_message_glyph_fields', 'append_scrolling_message_bitmap_fields', '_highbank_scroll_timer_fields', '_highbank_due_message_fields', 'advance_scrolling_message_fields', 'advance_message_decoration_stage_fields', '_highbank_selection_observation_fields', '_highbank_selection_projection', '_highbank_message_observation_fields', '_highbank_message_projection')}
    for owner in ('build_ten_officer_selection', 'sort_high_loyalty_officers', 'append_mid_loyalty_officers_by_trait', 'dispatch_highbank_command_state', 'select_highest_trait_officer', 'calculate_force_command_budget', 'advance_scrolling_message', 'append_scrolling_message_header', 'append_scrolling_message_glyph', 'lookup_message_layout_words', 'lookup_message_fill_pattern', 'advance_message_decoration_stage', 'lookup_message_decoration_style'):
        records[owner]['effects'] = dict(historical_projection=records[owner]['effects'], actual_complete_fields=sole_highbank_fields)
    records['increase_growth_random_attribute']['rules']['growth_random_attribute_cap'] = records['increase_growth_random_attribute_fields']['rules']['growth_random_attribute_cap']
    return lower_declared(records, BUSINESS_HIGHBANK_BINDINGS, LOWERERS)

DECLARATIONS.update({'_growth_carry_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, requested: bool', 'returns': 'FirstDeploymentFrame', 'flow': 'status = frame.status & 30 | (1 if requested else 0)\nstate.sr = state.sr & 65504 | status\nreturn first_replace(frame, status=status)'}})

DECLARATIONS.update({'_growth_project_values_fields': {'signature': 'values: GrowthValues, attribute_pointer=None, owner_pointer=None', 'returns': 'FirstDeploymentFrame', 'flow': 'return first_replace(FirstDeploymentFrame.unobserved(), target_x=values.selected, target_y=values.value, unit=values.category, opponent=attribute_pointer, scratch=owner_pointer)'}})

DECLARATIONS.update({'_growth_ratio_attribute_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, first: bool', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_remaining_flows.business_city import _resource_cost_frame, _settlement_store_word_fields\nif type(first) is not bool:\n    raise ValueError('closed growth attribute role required')\nframe = _resource_cost_frame(state, frame, 418672 if first else 418722)\nframe = first_replace(frame, opponent=state.table_at(4294947840 if first else 4294948352))\nnumerator = frame.roster if first else frame.candidates\nother = frame.candidates if first else frame.roster\nframe = _movement_move(state, frame, 'target_y', numerator.word(low16(frame.target_x)), 16)\nframe = _movement_move(state, frame, 'unit', low16(frame.target_y), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 1)\nframe = _movement_add_word(state, frame, 'target_y', low16(frame.unit))\nframe = _movement_add_word(state, frame, 'unit', other.word(low16(frame.target_x)))\nframe = _movement_move_long(state, frame, 'target_y', frame.target_y & 65535)\nif low16(frame.unit) == 0:\n    raise MovementContinuationBoundary(418696 if first else 418746, frame, 'original DIVU requires its actual divide-by-zero exception frame')\nframe = first_replace(frame, target_y=divu_retained(frame.target_y, low16(frame.unit)))\nframe = _movement_move(state, frame, 'unit', frame.opponent.word(low16(frame.target_x)), 16)\nframe = _movement_add_word(state, frame, 'unit', low16(frame.target_y))\nframe = _movement_compare(state, frame, low16(frame.unit), 255, 16)\nif not frame.status & 5:\n    frame = _movement_move(state, frame, 'unit', 255, 16)\nreturn _settlement_store_word_fields(state, frame, frame.opponent, low16(frame.target_x), low16(frame.unit))"}})

DECLARATIONS.update({'_growth_saved_index_random_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "if continuation not in (418780, 418854):\n    raise ValueError('closed growth random continuation required')\nfrom ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory\nfrom ..high_level_battle_ai.business_actions import sample_battle_action_random_fields\nstack = frame.stack_cursor.advance(-2)\nstack.set_word(0, low16(frame.target_x))\nframe = _movement_test(state, first_replace(frame, stack_cursor=stack), low16(frame.target_x), 16)\nreturn sample_battle_action_random_fields(BattlePolicyMemory(state), frame, continuation)"}})

DECLARATIONS.update({'_ratio_attribute_growth': {'signature': 'state, values, first', 'returns': None, 'flow': 'checked_context(values, GrowthValues, state)\nframe = _growth_ratio_attribute_fields(state, _growth_project_values_fields(values), first)\nreturn GrowthValues(frame.target_x, frame.target_y, frame.unit)'}})

DECLARATIONS.update({'_scan_officer_growth': {'signature': 'state, values, attribute_pointer, owner_pointer', 'returns': None, 'flow': 'checked_context(values, GrowthValues, state)\nframe = advance_officer_growth_levels_fields(state, _growth_project_values_fields(values, attribute_pointer, owner_pointer))\nreturn GrowthScanObservation(GrowthValues(frame.target_x, frame.target_y, frame.unit), state.table_at(frame.roster.base), state.table_at(frame.candidates.base), frame.controller, state.table_at(frame.scan.base), frame.opponent, frame.scratch, frame.auxiliary, bool(frame.status & 1), bool(frame.status & 4), bool(frame.status & 8), bool(frame.status & 2))'}})

DECLARATIONS.update({'advance_officer_growth_levels': {'signature': 'state: SceneState, values: GrowthValues', 'returns': 'GrowthResult', 'flow': 'checked_context(values, GrowthValues, state)\nobserved = _scan_officer_growth(state, values, None, None)\nreturn GrowthResult(observed.values, observed.carry, observed.assignments)'}})

DECLARATIONS.update({'advance_officer_growth_levels_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_remaining_flows.business_city import _resource_cost_frame, _duel_menu_write_word_fields, _settlement_change_header_byte_fields, _deployment_menu_call_fields\nframe = _resource_cost_frame(state, frame, 418532)\nframe = first_replace(frame, roster=state.table_at(4294950912).cursor(), candidates=state.table_at(4294950400).cursor(), controller=state.table_at(4294952448), scan=state.table_at(418936).cursor(), auxiliary=state.table_at(4294953984))\nframe = _duel_menu_write_word_fields(state, frame, 4294963064, 0, True)\nwhile True:\n    frame = _movement_move(state, frame, 'target_x', state.read(4294963064, 2), 16)\n    frame = _movement_compare(state, frame, low16(frame.target_x), 256, 16)\n    if not frame.status & 1:\n        frame = _duel_menu_write_word_fields(state, frame, 4294954956, 1)\n        return _growth_carry_fields(state, frame, False)\n    frame = _movement_compare(state, frame, frame.auxiliary.byte(low16(frame.target_x)), 255, 8)\n    assigned = not bool(frame.status & 4)\n    if assigned:\n        frame = _movement_move(state, frame, 'unit', 0, 16)\n        frame = _movement_move(state, frame, 'unit', frame.controller.byte(low16(frame.target_x)), 8)\n        frame = _movement_fixed_shift_word(state, frame, 'unit', 1)\n        frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)\n        frame = _movement_move(state, frame, 'target_y', frame.roster.word(low16(frame.target_x)), 16)\n        frame = _movement_add_word(state, frame, 'target_y', frame.candidates.word(low16(frame.target_x)))\n        frame = _movement_compare(state, frame, low16(frame.target_y), frame.scan.word(low16(frame.unit)), 16)\n        if not frame.status & 1:\n            frame = _deployment_menu_call_fields(state, frame, 418672, 418616)\n            frame = _deployment_menu_call_fields(state, frame, 418722, 418620)\n            frame = _deployment_menu_call_fields(state, frame, 418772, 418624)\n            frame = _deployment_menu_call_fields(state, frame, 418830, 418628)\n            frame = _settlement_change_header_byte_fields(state, frame, frame.controller.at(low16(frame.target_x)), False)\n            frame = _deployment_menu_call_fields(state, frame, 418874, 418636)\n            if not frame.status & 1:\n                continue\n            frame = _duel_menu_write_word_fields(state, frame, 4294964176, low16(frame.target_x))\n            frame = _movement_move_long(state, frame, 'target_y', 0)\n            frame = _movement_move(state, frame, 'target_y', frame.controller.byte(low16(frame.target_x)), 8)\n            state.write(4294964168, 4, frame.target_y)\n            from .business_movement_support import _movement_test_long\n            frame = _movement_test_long(state, frame, frame.target_y)\n            return _growth_carry_fields(state, frame, True)\n    old = state.read(4294963064, 2)\n    frame, advanced = _movement_binary_flags(state, frame, old, 1, 16)\n    state.write(4294963064, 2, advanced)"}})

DECLARATIONS.update({'check_growth_notification_owner': {'signature': 'state: SceneState, values: GrowthValues', 'returns': 'GrowthResult', 'flow': 'checked_context(values, GrowthValues, state)\nframe = check_growth_notification_owner_fields(state, _growth_project_values_fields(values))\nreturn GrowthResult(GrowthValues(frame.target_x, frame.target_y, frame.unit), bool(frame.status & 1), frame.opponent)'}})

DECLARATIONS.update({'check_growth_notification_owner_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_remaining_flows.business_city import _resource_cost_frame\nframe = _resource_cost_frame(state, frame, 418874)\nframe = first_replace(frame, opponent=state.table_at(4294953984), scratch=state.table_at(4294964263))\nframe = _movement_move(state, frame, 'target_y', frame.opponent.byte(low16(frame.target_x)), 8)\nif frame.status & 8:\n    return _growth_carry_fields(state, frame, False)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 63, 16)\nframe = _movement_move(state, frame, 'target_y', frame.scratch.byte(low16(frame.target_y)), 8)\nfor address in (4294964859, 4294964861, 4294964863):\n    frame = _movement_compare(state, frame, low8(frame.target_y), state.read(address, 1), 8)\n    if frame.status & 4:\n        return _growth_carry_fields(state, frame, True)\nreturn _growth_carry_fields(state, frame, False)"}})

DECLARATIONS.update({'increase_growth_command_radius': {'signature': 'state: SceneState, values: GrowthValues', 'returns': 'GrowthValues', 'flow': 'checked_context(values, GrowthValues, state)\nframe = increase_growth_command_radius_fields(state, _growth_project_values_fields(values))\nreturn GrowthValues(frame.target_x, frame.target_y, frame.unit)'}})

DECLARATIONS.update({'increase_growth_command_radius_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_remaining_flows.business_city import _resource_cost_frame, _settlement_change_header_byte_fields\nframe = _resource_cost_frame(state, frame, 418830)\nframe = _movement_fixed_shift_word(state, frame, 'target_x', 1, True)\nframe = first_replace(frame, opponent=state.table_at(4294951936))\nframe = _movement_compare(state, frame, frame.opponent.byte(low16(frame.target_x)), 20, 8)\nif not frame.status & 1:\n    return frame\nframe = _growth_saved_index_random_fields(state, frame, 418854)\nrestored = frame.stack_cursor.word()\nframe = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\nframe = _movement_move(state, frame, 'target_x', restored, 16)\nframe = _movement_move(state, frame, 'target_y', state.read(4294964764, 2), 16)\nfrom ..high_level_gameplay_flow.business_battle import _postbattle_bit_fields\nframe = _postbattle_bit_fields(frame, bool(frame.target_y & 16))\nstate.sr = state.sr & 65504 | frame.status\nif not frame.status & 4:\n    frame = _settlement_change_header_byte_fields(state, frame, frame.opponent.at(low16(frame.target_x)), False)\nreturn frame"}})

DECLARATIONS.update({'increase_growth_first_attribute': {'signature': 'state: SceneState, values: GrowthValues', 'returns': 'GrowthValues', 'flow': 'checked_context(values, GrowthValues, state)\nframe = increase_growth_first_attribute_fields(state, _growth_project_values_fields(values))\nreturn GrowthValues(frame.target_x, frame.target_y, frame.unit)'}})

DECLARATIONS.update({'increase_growth_first_attribute_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _growth_ratio_attribute_fields(state, frame, True)'}})

DECLARATIONS.update({'increase_growth_random_attribute': {'signature': 'state: SceneState, values: GrowthValues', 'returns': 'GrowthValues', 'flow': 'checked_context(values, GrowthValues, state)\nframe = increase_growth_random_attribute_fields(state, _growth_project_values_fields(values))\nreturn GrowthValues(frame.target_x, frame.target_y, frame.unit)'}})

DECLARATIONS.update({'increase_growth_random_attribute_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_remaining_flows.business_city import _resource_cost_frame, _settlement_store_word_fields, _special_action_shift_long\nframe = _resource_cost_frame(state, frame, 418772)\nframe = _growth_saved_index_random_fields(state, frame, 418780)\nframe = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)\nframe = _movement_move_long(state, frame, 'target_y', frame.target_x)\nframe = _special_action_shift_long(state, frame, 'target_y', 1)\nframe = _movement_arithmetic_long(state, frame, 'target_y', frame.target_x)\nframe = _movement_move_long(state, frame, 'target_y', swap_words(frame.target_y))\nrestored = frame.stack_cursor.word()\nframe = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\nframe = _movement_move(state, frame, 'target_x', restored, 16)\nframe = _movement_move(state, frame, 'unit', low16(frame.target_y), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 2)\nframe = _movement_add_word(state, frame, 'target_y', low16(frame.unit))\nframe = first_replace(frame, opponent=state.table_at(4294948864))\nframe = _movement_move(state, frame, 'unit', frame.opponent.word(low16(frame.target_x)), 16)\nframe = _movement_add_word(state, frame, 'unit', low16(frame.target_y))\nframe = _movement_compare(state, frame, low16(frame.unit), 150, 16)\nif not frame.status & 5:\n    frame = _movement_move(state, frame, 'unit', 150, 16)\nreturn _settlement_store_word_fields(state, frame, frame.opponent, low16(frame.target_x), low16(frame.unit))"}})

DECLARATIONS.update({'increase_growth_second_attribute': {'signature': 'state: SceneState, values: GrowthValues', 'returns': 'GrowthValues', 'flow': 'checked_context(values, GrowthValues, state)\nframe = increase_growth_second_attribute_fields(state, _growth_project_values_fields(values))\nreturn GrowthValues(frame.target_x, frame.target_y, frame.unit)'}})

DECLARATIONS.update({'increase_growth_second_attribute_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _growth_ratio_attribute_fields(state, frame, False)'}})

DECLARATIONS.update({'scan_officer_growth_levels': {'signature': 'state: SceneState, frame: GrowthFrame', 'returns': 'FullGrowthResult', 'flow': 'checked_context(frame, GrowthFrame, state)\nobserved = _scan_officer_growth(state, frame.values, frame.attribute_pointer, frame.owner_pointer)\nreturn observed.complete(state)'}})

APPROVED.setdefault('contexts_gameplay',set()).update(('FirstDeploymentFrame', 'first_replace', 'MovementContinuationBoundary'))

APPROVED.setdefault('business_movement_support',set()).update(('_movement_move', '_movement_move_long', '_movement_test', '_movement_fixed_shift_word', '_movement_add_word', '_movement_binary_flags', '_movement_compare', '_movement_arithmetic_long', '_movement_test_long'))

APPROVED.setdefault('business_city',set()).update(('_resource_cost_frame', '_settlement_store_word_fields', '_settlement_change_header_byte_fields', '_deployment_menu_call_fields', '_duel_menu_write_word_fields', '_special_action_shift_long'))

APPROVED.setdefault('contexts_policy_memory',set()).update(('BattlePolicyMemory',))

APPROVED.setdefault('business_actions',set()).update(('sample_battle_action_random_fields',))

APPROVED.setdefault('business_battle',set()).update(('_postbattle_bit_fields',))

# B51: full actual bodies, not old scalar shape fallback.
DECLARATIONS.update({'_advance_scrolling_message_core': {'signature': 'state: SceneState, layout: MessageLayout | None', 'returns': 'ScrollingMessageAdvance', 'flow': 'checked_state(state)\nentered = FirstDeploymentFrame.unobserved() if layout is None else _highbank_message_observation_fields(state, layout)\nreturned, timer = _highbank_scroll_timer_fields(state, entered)\nif timer:\n    return ScrollingMessageAdvance(layout, timer)\nreturned = _highbank_due_message_fields(state, returned)\nreturn ScrollingMessageAdvance(_highbank_message_projection(state, returned), timer)'}, '_highbank_child_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': 'stack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = first_replace(frame, stack_cursor=stack)\nresult = _highbank_target_fields(state, entered, target)\nactual = result.stack_cursor.long()\nif actual != continuation:\n    raise FirstDeploymentReturnBoundary(actual, result, continuation)\nreturn first_replace(result, stack_cursor=result.stack_cursor.advance(4))'}, '_highbank_dbra_fields': {'signature': 'frame: FirstDeploymentFrame, name: str', 'returns': 'FirstDeploymentFrame', 'flow': 'return first_replace(frame, **{name: replace_word(frame.carrier(name), u16(low16(frame.carrier(name)) - 1))})'}, '_highbank_due_message_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _highbank_frame_fields(state, frame, 422334)\nframe = _movement_move(state, frame, 'target_x', state.read(4294963160, 2), 16)\nframe = _highbank_shift_fields(state, frame, 'target_x', 1)\nframe = _highbank_write_fields(state, frame, 4294963162, state.table_at(422320).word(low16(frame.target_x)))\nframe = first_replace(frame, roster=state.table_at(state.read(4294964158, 4)).cursor())\nframe, value = _highbank_memory_add_fields(state, frame, 4294964158, 2, 4)\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(), 16)\nframe = _highbank_write_fields(state, frame, 4294965116, low16(frame.target_x))\nif frame.status & 4:\n    frame = first_replace(frame, roster=state.table_at(u32(4294955264 + s16(state.read(4294963994, 2)))).cursor())\n    frame = _highbank_child_fields(state, frame, 422740, 422422)\n    frame = first_replace(frame, controller=state.table_at(423082))\n    frame = _highbank_child_fields(state, frame, 422822, 422432)\n    frame, value = _highbank_memory_add_fields(state, frame, 4294964092, 18)\n    return frame\nif frame.status & 8:\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 255, 16)\n    frame = _movement_move(state, frame, 'target_x', state.table_at(422456).word(low16(frame.target_x)), 16)\n    return _highbank_target_fields(state, frame, u32(422478 + s16(low16(frame.target_x))))\nframe = first_replace(frame, roster=state.table_at(u32(4294955264 + s16(state.read(4294963994, 2)))).cursor())\nframe = _highbank_child_fields(state, frame, 422740, 422376)\nframe = _highbank_child_fields(state, frame, 422796, 422380)\nframe, value = _highbank_memory_add_fields(state, frame, 4294964092, 18)\nframe = _movement_compare(state, frame, state.read(4294964092, 2), 288, 16)\nif not frame.status & 1:\n    frame = _highbank_write_fields(state, frame, 4294964090, state.read(4294964090, 2) ^ 1)\n    frame = _highbank_write_fields(state, frame, 4294964092, 0, clear=True)\nreturn frame"}, '_highbank_frame_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, entry: int', 'returns': 'FirstDeploymentFrame', 'flow': 'from ..high_level_remaining_flows.business_city import _resource_cost_frame\nreturn _resource_cost_frame(state, frame, entry)'}, '_highbank_memory_add_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, address: int, amount: int, size: int=2', 'returns': 'tuple', 'flow': 'old = state.read(address, size)\nobserved = frame.status\nworking = frame if observed is not None else first_replace(frame, status=state.sr & 31)\nworking, value = _movement_binary_flags(state, working, old, abs(amount), size * 8, amount < 0)\nstate.write(address, size, value)\nreturn (working if observed is not None else first_replace(working, status=None), value)'}, '_highbank_message_observation_fields': {'signature': 'state: SceneState, layout: MessageLayout', 'returns': 'FirstDeploymentFrame', 'flow': 'checked_context(layout, MessageLayout, state)\nreturn first_replace(FirstDeploymentFrame.unobserved(), target_x=layout.symbol, target_y=layout.position, unit=layout.stride, count=layout.row_offset, distance=layout.first_plane, offset_x=layout.fill, offset_y=layout.shift_count, choice=layout.second_plane, roster=layout.destination, controller=layout.bitmap, candidates=layout.previous_rows)'}, '_highbank_message_projection': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'MessageLayout', 'flow': 'return MessageLayout(frame.target_x, frame.target_y, frame.unit, frame.count, frame.distance, frame.offset_x, frame.offset_y, frame.choice, frame.roster, None if frame.controller is None else state.table_at(frame.controller.base).cursor(), frame.candidates).validate(state)'}, '_highbank_roxr_plane_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, name: str', 'returns': 'FirstDeploymentFrame', 'flow': "if name not in ('target_x', 'distance', 'choice', 'offset_x'):\n    raise ValueError('actual scrolling plane rotation carrier required')\noriginal = frame.carrier(name)\ncarried = bool(original & 1)\nrotated = original >> 1 | (2147483648 if frame.status & 16 else 0)\nstatus = (17 if carried else 0) | (8 if rotated & 2147483648 else 0) | (4 if rotated == 0 else 0)\nstate.sr = state.sr & 65504 | status\nreturn first_replace(frame, **{name: rotated}, status=status)"}, '_highbank_scroll_timer_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': "checked_state(state)\nif type(frame) is not FirstDeploymentFrame:\n    raise ValueError('actual Highbank fields required')\nframe.validate(state, False)\nreturn _highbank_memory_add_fields(state, frame, 4294963162, -1)"}, '_highbank_selection_observation_fields': {'signature': 'state: SceneState, choice: OfficerSelection', 'returns': 'FirstDeploymentFrame', 'flow': 'checked_context(choice, OfficerSelection, state)\nreturn first_replace(FirstDeploymentFrame.unobserved(), target_x=choice.count, target_y=choice.force, unit=choice.scan, count=choice.score, distance=choice.trait, offset_x=choice.displaced, offset_y=choice.displaced_score, choice=choice.selected)'}, '_highbank_selection_projection': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'OfficerSelection', 'flow': 'return OfficerSelection(frame.target_x, frame.target_y, frame.unit, frame.count, frame.distance, frame.offset_x, frame.offset_y, frame.choice).validate(state)'}, '_highbank_shift_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, name: str, count: int', 'returns': 'FirstDeploymentFrame', 'flow': 'from ..high_level_remaining_flows.business_highbank import _position_order_shift\nframe = _position_order_shift(frame, name, count)\nstate.sr = state.sr & 65504 | frame.status\nreturn frame'}, '_highbank_target_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int', 'returns': 'FirstDeploymentFrame', 'flow': "if target == 420948:\n    from ..high_level_remaining_flows.business_highbank import confirm_scenario_force_choice_fields\n    return confirm_scenario_force_choice_fields(state, frame)\nif target == 423344:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_paired_columns_fields\n    return build_scenario_paired_columns_fields(state, frame)\nif target == 419076:\n    return sort_high_loyalty_officers_fields(state, frame)\nif target == 419196:\n    return append_mid_loyalty_officers_by_trait_fields(state, frame)\nif target == 422740:\n    return append_scrolling_message_header_fields(state, frame)\nif target == 422796:\n    return append_scrolling_message_glyph_fields(state, frame)\nif target == 422822:\n    return append_scrolling_message_bitmap_fields(state, frame)\nif target == 423018:\n    return lookup_message_layout_words_fields(state, frame)\nif target == 423054:\n    return lookup_message_fill_pattern_fields(state, frame)\nif target == 423178:\n    return lookup_message_decoration_style_fields(state, frame)\nif target == 44804:\n    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\n    from ..high_level_scene_flows.business_scene import expand_glyph_row_fields\n    return expand_glyph_row_fields(SceneRefreshMemory(state), frame)\nif target == 41304:\n    from .business_map import refresh_world_cursor_attributes_alternate_1_frame_fields\n    return refresh_world_cursor_attributes_alternate_1_frame_fields(state, frame)\nif target == 55532:\n    from .business_commands import append_current_command_description_frame_fields\n    return append_current_command_description_frame_fields(state, frame)\nraise MovementContinuationBoundary(target, frame, 'actual Highbank child has no admitted full-field return')"}, '_highbank_write_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, address: int, value, size: int=2, clear: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': "if size not in (1, 2, 4) or type(clear) is not bool:\n    raise ValueError('actual Highbank memory width required')\nif clear:\n    state.read(address, size)\nstate.write(address, size, value)\nif size == 4:\n    return _movement_test_long(state, frame, value)\nreturn _movement_test(state, frame, value, size * 8)"}, 'advance_message_decoration_stage': {'signature': 'state: SceneState, layout: MessageLayout', 'returns': 'MessageLayout', 'flow': 'entered = _highbank_message_observation_fields(state, layout)\nreturned = advance_message_decoration_stage_fields(state, entered)\nreturn _highbank_message_projection(state, returned)'}, 'advance_message_decoration_stage_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _highbank_frame_fields(state, frame, 423114)\nframe = first_replace(frame, roster=state.table_at(u32(4294955264 + s16(state.read(4294963994, 2)))).cursor())\nframe = _highbank_child_fields(state, frame, 423178, 423126)\nframe = _movement_move(state, frame, 'target_x', state.read(4294964074, 2), 16)\nframe = _highbank_shift_fields(state, frame, 'target_x', 1)\nframe = _movement_move(state, frame, 'target_x', state.table_at(423170).word(low16(frame.target_x)), 16)\nframe = _highbank_child_fields(state, frame, u32(423198 + s16(low16(frame.target_x))), 423140)\nframe, value = _highbank_memory_add_fields(state, frame, 4294964074, 1)\nframe = _movement_move(state, frame, 'target_x', state.read(4294964074, 2), 16)\nframe = _movement_compare(state, frame, low16(frame.target_x), 4, 16)\nif not frame.status & 1:\n    frame, value = _highbank_memory_add_fields(state, frame, 4294964066, 1)\n    frame = _highbank_write_fields(state, frame, 4294964074, 0, clear=True)\n    previous = state.read(4294964132, 1)\n    state.write(4294964132, 1, previous | 64)\n    status = frame.status & 27 | (0 if previous & 64 else 4)\n    state.sr = state.sr & 65504 | status\n    return first_replace(frame, status=status)\nreturn frame"}, 'advance_scrolling_message': {'signature': 'state: SceneState, layout: MessageLayout', 'returns': 'MessageLayout', 'flow': 'entered = _highbank_message_observation_fields(state, layout)\nreturned = advance_scrolling_message_fields(state, entered)\nreturn _highbank_message_projection(state, returned)'}, 'advance_scrolling_message_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame, timer = _highbank_scroll_timer_fields(state, frame)\nreturn frame if timer else _highbank_due_message_fields(state, frame)'}, 'append_mid_loyalty_officers_by_trait': {'signature': 'state: SceneState, choice: OfficerSelection', 'returns': 'OfficerSelection', 'flow': 'entered = _highbank_selection_observation_fields(state, choice)\nreturned = append_mid_loyalty_officers_by_trait_fields(state, entered)\nreturn _highbank_selection_projection(state, returned)'}, 'append_mid_loyalty_officers_by_trait_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _highbank_frame_fields(state, frame, 419196)\nframe = first_replace(frame, roster=state.table_at(4294963456).cursor())\nwhile True:\n    value = frame.roster.word()\n    frame = first_replace(frame, roster=frame.roster.advance(2))\n    frame = _movement_test(state, frame, value, 16)\n    if frame.status & 8:\n        break\nframe = first_replace(frame, roster=frame.roster.advance(-2), candidates=state.table_at(4294953984).cursor(), controller=state.table_at(4294964263), scan=state.table_at(4294951680).cursor(), opponent=state.table_at(4294952704))\nframe = _movement_move(state, frame, 'target_y', 255, 16)\nframe = _movement_move(state, frame, 'unit', state.read(4294963120, 2), 16)\nwhile True:\n    frame = _movement_move(state, frame, 'count', frame.candidates.byte(low16(frame.target_y)), 8)\n    eligible = not bool(frame.status & 12)\n    if eligible:\n        frame = _movement_move(state, frame, 'count', low16(frame.count) & 63, 16)\n        frame = _movement_compare(state, frame, low8(frame.unit), frame.controller.byte(low16(frame.count)), 8)\n        eligible = bool(frame.status & 4)\n    if eligible:\n        frame = _movement_compare(state, frame, frame.scan.byte(low16(frame.target_y)), 80, 8)\n        eligible = not bool(frame.status & 1)\n    if eligible:\n        frame = _movement_compare(state, frame, frame.scan.byte(low16(frame.target_y)), 90, 8)\n        eligible = bool(frame.status & 1)\n    if eligible:\n        frame = _movement_move(state, frame, 'count', frame.opponent.byte(low16(frame.target_y)), 8)\n        frame = _movement_move(state, frame, 'count', low16(frame.count) & 7, 16)\n        frame = _movement_compare(state, frame, low8(frame.count), low8(frame.distance), 8)\n        eligible = bool(frame.status & 4)\n    if eligible:\n        frame = _highbank_write_fields(state, frame, frame.roster.base, low16(frame.target_y))\n        frame = first_replace(frame, roster=frame.roster.advance(2))\n        frame = _movement_add_word(state, frame, 'target_x', 1)\n    frame = _highbank_dbra_fields(frame, 'target_y')\n    if low16(frame.target_y) == 65535:\n        return _highbank_write_fields(state, frame, frame.roster.base, 65535)"}, 'append_scrolling_message_bitmap': {'signature': 'state: SceneState, layout: MessageLayout', 'returns': 'MessageLayout', 'flow': 'entered = _highbank_message_observation_fields(state, layout)\nreturned = append_scrolling_message_bitmap_fields(state, entered)\nreturn _highbank_message_projection(state, returned)'}, 'append_scrolling_message_bitmap_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _highbank_frame_fields(state, frame, 422822)\nframe = _movement_move(state, frame, 'unit', 64, 16)\nframe = first_replace(frame, candidates=state.table_at(4294964502).cursor())\nframe = _movement_test(state, frame, state.read(4294964090, 2), 16)\nif not frame.status & 4:\n    frame = _movement_move(state, frame, 'unit', 96, 16)\n    frame = _movement_move(state, frame, 'target_y', 3, 16)\n    while True:\n        frame = _highbank_child_fields(state, frame, 423054, 422848)\n        for displacement in (192, 96, 0):\n            frame = _highbank_write_fields(state, frame, u32(frame.roster.base + displacement), frame.offset_x, 4)\n        frame = first_replace(frame, roster=frame.roster.advance(4))\n        frame = _highbank_dbra_fields(frame, 'target_y')\n        if low16(frame.target_y) == 65535:\n            break\nframe = _movement_move(state, frame, 'count', low16(frame.unit), 16)\nframe = _highbank_shift_fields(state, frame, 'count', 1)\nframe, value = _highbank_memory_add_fields(state, frame, 4294963994, low16(frame.count))\nframe, value = _highbank_memory_add_fields(state, frame, 4294963994, low16(frame.unit))\nframe, value = _highbank_memory_add_fields(state, frame, 4294963994, 4)\nframe = _movement_move_long(state, frame, 'unit', swap_words(frame.unit))\nframe = _movement_move_long(state, frame, 'count', swap_words(frame.count))\nframe = _movement_move(state, frame, 'unit', 15, 16)\nframe = _movement_move(state, frame, 'count', state.read(4294964092, 2), 16)\nframe = _movement_move(state, frame, 'count', low16(frame.count) & 7, 16)\nwhile True:\n    frame = _highbank_child_fields(state, frame, 423018, 422900)\n    frame = _highbank_child_fields(state, frame, 44804, 422906)\n    stack = frame.stack_cursor.advance(-4)\n    frame = _highbank_write_fields(state, frame, stack.base, frame.choice, 4)\n    frame = first_replace(frame, stack_cursor=stack)\n    frame = _highbank_child_fields(state, frame, 44804, 422914)\n    saved = frame.stack_cursor.long()\n    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(4))\n    frame = _movement_move_long(state, frame, 'distance', saved)\n    frame = _highbank_child_fields(state, frame, 423054, 422920)\n    frame = _movement_move(state, frame, 'offset_y', low16(frame.count), 16)\n    if not frame.status & 4:\n        frame = _highbank_shift_fields(state, frame, 'offset_y', 2)\n        frame, value = _movement_binary_flags(state, frame, low16(frame.offset_y), 1, 16, True)\n        frame = first_replace(frame, offset_y=replace_word(frame.offset_y, value))\n        frame = _movement_move(state, frame, 'target_x', 0, 16)\n        while True:\n            state.set_status_word(state.sr & 65519)\n            frame = first_replace(frame, status=state.sr & 31)\n            for name in ('distance', 'choice', 'offset_x'):\n                frame = _highbank_roxr_plane_fields(state, frame, name)\n            state.set_status_word(state.sr | 16)\n            frame = first_replace(frame, status=state.sr & 31)\n            frame = _highbank_roxr_plane_fields(state, frame, 'target_x')\n            frame = _highbank_dbra_fields(frame, 'offset_y')\n            if low16(frame.offset_y) == 65535:\n                break\n    frame = _movement_move_long(state, frame, 'target_y', frame.candidates.long())\n    frame = _movement_move_long(state, frame, 'target_y', frame.target_y & frame.target_x)\n    frame = _movement_move_long(state, frame, 'distance', frame.distance | frame.target_y)\n    frame = _movement_move_long(state, frame, 'unit', swap_words(frame.unit))\n    frame = _movement_move_long(state, frame, 'count', swap_words(frame.count))\n    frame = _highbank_write_fields(state, frame, u32(frame.roster.base + s16(low16(frame.count))), frame.offset_x, 4)\n    frame = _highbank_write_fields(state, frame, u32(frame.roster.base + s16(low16(frame.unit))), frame.choice, 4)\n    frame = _highbank_write_fields(state, frame, frame.roster.base, frame.distance, 4)\n    frame = first_replace(frame, roster=frame.roster.advance(4))\n    frame = _highbank_write_fields(state, frame, frame.candidates.base, frame.offset_x, 4)\n    frame = first_replace(frame, candidates=frame.candidates.advance(4))\n    frame = _movement_move_long(state, frame, 'unit', swap_words(frame.unit))\n    frame = _movement_move_long(state, frame, 'count', swap_words(frame.count))\n    frame = _highbank_dbra_fields(frame, 'unit')\n    if low16(frame.unit) == 65535:\n        break\nframe = _movement_move_long(state, frame, 'unit', swap_words(frame.unit))\nframe = _movement_move_long(state, frame, 'count', swap_words(frame.count))\nframe = _movement_test(state, frame, state.read(4294964090, 2), 16)\nif not frame.status & 4:\n    frame = _movement_move(state, frame, 'target_y', 3, 16)\n    while True:\n        frame = _highbank_child_fields(state, frame, 423054, 422998)\n        frame = _highbank_write_fields(state, frame, u32(frame.roster.base + s16(low16(frame.count))), frame.offset_x, 4)\n        frame = _highbank_write_fields(state, frame, u32(frame.roster.base + s16(low16(frame.unit))), frame.offset_x, 4)\n        frame = _highbank_write_fields(state, frame, frame.roster.base, frame.offset_x, 4)\n        frame = first_replace(frame, roster=frame.roster.advance(4))\n        frame = _highbank_dbra_fields(frame, 'target_y')\n        if low16(frame.target_y) == 65535:\n            break\nreturn _highbank_write_fields(state, frame, u32(frame.roster.base + s16(low16(frame.count))), 0, clear=True)"}, 'append_scrolling_message_glyph': {'signature': 'state: SceneState, layout: MessageLayout', 'returns': 'MessageLayout', 'flow': 'entered = _highbank_message_observation_fields(state, layout)\nreturned = append_scrolling_message_glyph_fields(state, entered)\nreturn _highbank_message_projection(state, returned)'}, 'append_scrolling_message_glyph_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _highbank_frame_fields(state, frame, 422796)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 65280, 16)\nframe = _highbank_shift_fields(state, frame, 'target_y', 3)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 255, 16)\nframe = _highbank_shift_fields(state, frame, 'target_x', 5)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) | low16(frame.target_y), 16)\nframe = first_replace(frame, controller=state.table_at(u32(529820 + s16(low16(frame.target_x)))))\nreturn append_scrolling_message_bitmap_fields(state, frame)"}, 'append_scrolling_message_header': {'signature': 'state: SceneState, layout: MessageLayout', 'returns': 'MessageLayout', 'flow': 'entered = _highbank_message_observation_fields(state, layout)\nreturned = append_scrolling_message_header_fields(state, entered)\nreturn _highbank_message_projection(state, returned)'}, 'append_scrolling_message_header_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _highbank_frame_fields(state, frame, 422740)\nframe = _movement_move(state, frame, 'target_y', 16480, 16)\nframe = _movement_test(state, frame, state.read(4294964090, 2), 16)\nif not frame.status & 4:\n    frame = _movement_move(state, frame, 'target_y', 16528, 16)\nframe = _highbank_write_fields(state, frame, frame.roster.base, low16(frame.target_y))\nframe = first_replace(frame, roster=frame.roster.advance(2))\nframe = _movement_move(state, frame, 'target_y', state.read(4294964092, 2), 16)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 65528, 16)\nframe = _movement_move(state, frame, 'unit', low16(frame.target_y), 16)\nframe = _movement_add_word(state, frame, 'target_y', low16(frame.unit))\nframe = _movement_test(state, frame, state.read(4294964090, 2), 16)\nif not frame.status & 4:\n    frame = _movement_add_word(state, frame, 'target_y', low16(frame.unit))\nframe = _highbank_shift_fields(state, frame, 'target_y', 2)\nframe = _movement_add_word(state, frame, 'target_y', 41120)\nframe = _movement_test(state, frame, state.read(4294964090, 2), 16)\nif not frame.status & 4:\n    frame = _movement_add_word(state, frame, 'target_y', 2304)\nframe = _highbank_write_fields(state, frame, frame.roster.base, low16(frame.target_y))\nreturn first_replace(frame, roster=frame.roster.advance(2))"}, 'build_ten_officer_selection': {'signature': 'state: SceneState, choice: OfficerSelection', 'returns': 'OfficerSelection', 'flow': 'entered = _highbank_selection_observation_fields(state, choice)\nreturned = build_ten_officer_selection_fields(state, entered)\nreturn _highbank_selection_projection(state, returned)'}, 'build_ten_officer_selection_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _highbank_frame_fields(state, frame, 418988)\nframe = _movement_move(state, frame, 'target_x', 0, 16)\nframe = _highbank_child_fields(state, frame, 419076, 418994)\nfor trait, continuation in ((4, 419010), (3, 419026), (2, 419042)):\n    frame = _movement_compare(state, frame, low16(frame.target_x), 10, 16)\n    if not frame.status & 1:\n        break\n    frame = _movement_move(state, frame, 'distance', trait, 16)\n    frame = _highbank_child_fields(state, frame, 419196, continuation)\nframe = first_replace(frame, roster=state.table_at(4294963456).cursor(), candidates=state.table_at(4294964480).cursor())\nframe = _movement_move(state, frame, 'target_x', 0, 16)\nwhile True:\n    value = frame.roster.word()\n    frame = first_replace(frame, roster=frame.roster.advance(2))\n    frame = _highbank_write_fields(state, frame, frame.candidates.base, value)\n    frame = first_replace(frame, candidates=frame.candidates.advance(2))\n    if frame.status & 8:\n        break\n    frame = _movement_add_word(state, frame, 'target_x', 1)\n    frame = _movement_compare(state, frame, low16(frame.target_x), 10, 16)\n    if not frame.status & 1:\n        break\nframe = _highbank_write_fields(state, frame, frame.candidates.base, 65535)\nreturn _highbank_write_fields(state, frame, 4294964790, low16(frame.target_x))"}, 'calculate_force_command_budget': {'signature': 'state: SceneState, choice: OfficerSelection', 'returns': 'OfficerSelection', 'flow': 'entered = _highbank_selection_observation_fields(state, choice)\nreturned = calculate_force_command_budget_fields(state, entered)\nreturn _highbank_selection_projection(state, returned)'}, 'calculate_force_command_budget_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _highbank_frame_fields(state, frame, 422182)\nframe = first_replace(frame, roster=state.table_at(4294959904).cursor())\nframe = _movement_move(state, frame, 'target_x', 39, 16)\nframe = _movement_move_long(state, frame, 'target_y', 0)\nwhile True:\n    value = frame.roster.long()\n    frame = first_replace(frame, roster=frame.roster.advance(4))\n    frame = _movement_arithmetic_long(state, frame, 'target_y', value)\n    frame = _highbank_dbra_fields(frame, 'target_x')\n    if low16(frame.target_x) == 65535:\n        break\nframe = _movement_divu_word(state, frame, 'target_y', 40, 422198)\nframe = first_replace(frame, roster=state.table_at(4294951680).cursor(), candidates=state.table_at(4294953984).cursor())\nframe = _movement_move(state, frame, 'target_x', 255, 16)\nframe = _movement_move_long(state, frame, 'unit', 0)\nframe = _movement_move(state, frame, 'count', 0, 16)\nframe = _movement_move(state, frame, 'distance', 0, 16)\nwhile True:\n    frame = _movement_move(state, frame, 'distance', frame.candidates.byte(low16(frame.target_x)), 8)\n    eligible = not bool(frame.status & 4)\n    if eligible:\n        frame = _movement_move(state, frame, 'distance', low16(frame.distance) & 192, 16)\n        eligible = bool(frame.status & 4)\n    if eligible:\n        frame = _movement_move(state, frame, 'distance', frame.roster.byte(low16(frame.target_x)), 8)\n        frame = _movement_add_word(state, frame, 'unit', low16(frame.distance))\n        frame = _movement_add_word(state, frame, 'count', 1)\n    frame = _highbank_dbra_fields(frame, 'target_x')\n    if low16(frame.target_x) == 65535:\n        break\nframe = first_replace(frame, candidates=state.table_at(4294938624).cursor())\nwhile True:\n    frame = _movement_move(state, frame, 'distance', frame.candidates.byte(), 8)\n    frame = _movement_move(state, frame, 'distance', low16(frame.distance) & 15, 16)\n    if frame.status & 4:\n        break\n    frame = _movement_move(state, frame, 'offset_x', frame.candidates.byte(0, 4), 8)\n    frame = _movement_compare(state, frame, low8(frame.offset_x), state.read(4294964087, 1), 8)\n    if frame.status & 4:\n        frame, value = _movement_binary_flags(state, frame, low16(frame.distance), 1, 16, True)\n        frame = first_replace(frame, distance=replace_word(frame.distance, value))\n        while True:\n            frame = _movement_move(state, frame, 'offset_x', frame.roster.byte(low16(frame.distance), 13), 8)\n            frame = _movement_move(state, frame, 'offset_x', frame.candidates.byte(low16(frame.offset_x)), 8)\n            frame = _movement_add_word(state, frame, 'unit', low16(frame.offset_x))\n            frame = _movement_add_word(state, frame, 'count', 1)\n            frame = _highbank_dbra_fields(frame, 'distance')\n            if low16(frame.distance) == 65535:\n                break\n    frame = _movement_move(state, frame, 'distance', frame.candidates.byte(), 8)\n    frame = _movement_move(state, frame, 'distance', low16(frame.distance) & 15, 16)\n    frame = first_replace(frame, candidates=frame.candidates.advance(13 + s16(low16(frame.distance))))\nframe = _movement_divu_word(state, frame, 'unit', low16(frame.count), 422304)\nframe = _movement_add_word(state, frame, 'target_y', low16(frame.unit))\nframe = _movement_multiply_word(state, frame, 'target_y', low16(frame.count))\nframe = _movement_divu_word(state, frame, 'target_y', 280, 422310)\nreturn _highbank_write_fields(state, frame, 4294963164, low16(frame.target_y))"}, 'dispatch_highbank_command_state': {'signature': 'state: SceneState, layout: MessageLayout', 'returns': 'MessageLayout', 'flow': 'entered = _highbank_message_observation_fields(state, layout)\nreturned = dispatch_highbank_command_state_fields(state, entered)\nreturn _highbank_message_projection(state, returned)'}, 'dispatch_highbank_command_state_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _highbank_frame_fields(state, frame, 420852)\nframe = _movement_move(state, frame, 'target_x', state.read(4294964066, 2), 16)\nframe = _highbank_shift_fields(state, frame, 'target_x', 1)\nframe = _movement_move(state, frame, 'target_x', state.table_at(420880).word(low16(frame.target_x)), 16)\nframe = _highbank_child_fields(state, frame, u32(420904 + s16(low16(frame.target_x))), 420866)\nframe = _highbank_child_fields(state, frame, 55532, 420872)\nreturn _highbank_child_fields(state, frame, 41304, 420878)"}, 'lookup_message_decoration_style': {'signature': 'state: SceneState, layout: MessageLayout', 'returns': 'MessageLayout', 'flow': 'entered = _highbank_message_observation_fields(state, layout)\nreturned = lookup_message_decoration_style_fields(state, entered)\nreturn _highbank_message_projection(state, returned)'}, 'lookup_message_decoration_style_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _highbank_frame_fields(state, frame, 423178)\nframe = _movement_move(state, frame, 'target_x', state.read(4294964932, 2), 16)\nframe = _highbank_shift_fields(state, frame, 'target_x', 1)\nreturn _movement_move(state, frame, 'unit', state.table_at(423190).word(low16(frame.target_x)), 16)"}, 'lookup_message_fill_pattern': {'signature': 'state: SceneState, layout: MessageLayout', 'returns': 'MessageLayout', 'flow': 'entered = _highbank_message_observation_fields(state, layout)\nreturned = lookup_message_fill_pattern_fields(state, entered)\nreturn _highbank_message_projection(state, returned)'}, 'lookup_message_fill_pattern_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _highbank_frame_fields(state, frame, 423054)\nframe = _movement_move(state, frame, 'offset_x', state.read(4294964932, 2), 16)\nframe = _highbank_shift_fields(state, frame, 'offset_x', 2)\nreturn _movement_move_long(state, frame, 'offset_x', state.table_at(423066).long(low16(frame.offset_x)))"}, 'lookup_message_layout_words': {'signature': 'state: SceneState, layout: MessageLayout', 'returns': 'MessageLayout', 'flow': 'entered = _highbank_message_observation_fields(state, layout)\nreturned = lookup_message_layout_words_fields(state, entered)\nreturn _highbank_message_projection(state, returned)'}, 'lookup_message_layout_words_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _highbank_frame_fields(state, frame, 423018)\nframe = _movement_move(state, frame, 'target_x', state.read(4294964932, 2), 16)\nframe = _highbank_shift_fields(state, frame, 'target_x', 2)\nframe = first_replace(frame, scan=state.table_at(423038).cursor())\noffset = low16(frame.target_x)\nfirst = u32(s16(frame.scan.word(offset)))\nsecond = u32(s16(frame.scan.word(offset, 2)))\nreturn first_replace(frame, target_x=first, target_y=second)"}, 'select_highest_trait_officer': {'signature': 'state: SceneState, choice: OfficerSelection', 'returns': 'OfficerSelection', 'flow': 'entered = _highbank_selection_observation_fields(state, choice)\nreturned = select_highest_trait_officer_fields(state, entered)\nreturn _highbank_selection_projection(state, returned)'}, 'select_highest_trait_officer_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _highbank_frame_fields(state, frame, 422072)\nframe = first_replace(frame, roster=state.table_at(4294953984).cursor(), candidates=state.table_at(4294952704).cursor(), controller=state.table_at(4294951680), scan=state.table_at(4294947840).cursor(), opponent=state.table_at(4294948352))\nframe = _movement_move(state, frame, 'target_x', 0, 16)\nframe = _movement_move(state, frame, 'target_y', 0, 16)\nframe = _movement_move(state, frame, 'unit', 255, 16)\nwhile True:\n    frame = _movement_move(state, frame, 'count', frame.roster.byte(low16(frame.unit)), 8)\n    eligible = not bool(frame.status & 4)\n    if eligible:\n        frame = _movement_move(state, frame, 'count', low16(frame.count) & 192, 16)\n        eligible = bool(frame.status & 4)\n    if eligible:\n        frame = _movement_move(state, frame, 'count', frame.candidates.byte(low16(frame.unit)), 8)\n        frame = _movement_move(state, frame, 'count', low16(frame.count) & 7, 16)\n        frame = _movement_compare(state, frame, low16(frame.count), low16(frame.target_x), 16)\n        eligible = not bool(frame.status & 1)\n    if eligible:\n        if not frame.status & 4:\n            frame = _movement_move(state, frame, 'target_y', 0, 16)\n        frame = _movement_move(state, frame, 'target_x', low16(frame.count), 16)\n        frame = _movement_move(state, frame, 'count', 0, 16)\n        frame = _movement_move(state, frame, 'count', frame.controller.byte(low16(frame.unit)), 8)\n        frame = _movement_move(state, frame, 'distance', low16(frame.unit), 16)\n        frame = _highbank_shift_fields(state, frame, 'distance', 1)\n        frame = _movement_add_word(state, frame, 'count', frame.scan.word(low16(frame.distance)))\n        frame = _movement_add_word(state, frame, 'count', frame.opponent.word(low16(frame.distance)))\n        frame = _movement_compare(state, frame, low16(frame.count), low16(frame.target_y), 16)\n        if not frame.status & 5:\n            frame = _movement_move(state, frame, 'target_y', low16(frame.count), 16)\n            frame = _movement_move(state, frame, 'choice', low16(frame.unit), 16)\n    frame = _highbank_dbra_fields(frame, 'unit')\n    if low16(frame.unit) == 65535:\n        break\nframe = _highbank_write_fields(state, frame, 4294964134, low16(frame.choice))\nreturn _highbank_write_fields(state, frame, 4294964086, state.read(4294964086, 2) & 255)"}, 'sort_high_loyalty_officers': {'signature': 'state: SceneState, choice: OfficerSelection', 'returns': 'OfficerSelection', 'flow': 'entered = _highbank_selection_observation_fields(state, choice)\nreturned = sort_high_loyalty_officers_fields(state, entered)\nreturn _highbank_selection_projection(state, returned)'}, 'sort_high_loyalty_officers_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _highbank_frame_fields(state, frame, 419076)\nframe = first_replace(frame, controller=state.table_at(4294953984), scan=state.table_at(4294951680).cursor(), opponent=state.table_at(4294964263))\nframe = _movement_move(state, frame, 'target_y', state.read(4294963120, 2), 16)\nframe = _movement_move(state, frame, 'unit', 255, 16)\nframe = _highbank_write_fields(state, frame, 4294963456, 65535)\nwhile True:\n    frame = _movement_move(state, frame, 'count', frame.controller.byte(low16(frame.unit)), 8)\n    eligible = not bool(frame.status & 12)\n    if eligible:\n        frame = _movement_move(state, frame, 'count', low16(frame.count) & 63, 16)\n        frame = _movement_compare(state, frame, low8(frame.target_y), frame.opponent.byte(low16(frame.count)), 8)\n        eligible = bool(frame.status & 4)\n    if eligible:\n        frame = _movement_compare(state, frame, frame.scan.byte(low16(frame.unit)), 90, 8)\n        eligible = not bool(frame.status & 1)\n    if eligible:\n        frame = _movement_move(state, frame, 'count', 0, 16)\n        frame = _movement_move(state, frame, 'count', frame.scan.byte(low16(frame.unit)), 8)\n        frame = first_replace(frame, roster=state.table_at(4294963456).cursor(), candidates=state.table_at(4294963712).cursor())\n        frame = _movement_move(state, frame, 'distance', low16(frame.unit), 16)\n        while True:\n            frame = _movement_test(state, frame, frame.roster.word(), 16)\n            if frame.status & 8:\n                break\n            frame = _movement_compare(state, frame, low16(frame.count), frame.candidates.word(), 16)\n            if not frame.status & 5:\n                break\n            frame = first_replace(frame, roster=frame.roster.advance(2), candidates=frame.candidates.advance(2))\n        while True:\n            frame = _movement_move(state, frame, 'offset_y', frame.candidates.word(), 16)\n            frame = _highbank_write_fields(state, frame, frame.candidates.base, low16(frame.count))\n            frame = first_replace(frame, candidates=frame.candidates.advance(2))\n            frame = _movement_move(state, frame, 'count', low16(frame.offset_y), 16)\n            frame = _movement_move(state, frame, 'offset_x', frame.roster.word(), 16)\n            frame = _highbank_write_fields(state, frame, frame.roster.base, low16(frame.distance))\n            frame = first_replace(frame, roster=frame.roster.advance(2))\n            frame = _movement_move(state, frame, 'distance', low16(frame.offset_x), 16)\n            if frame.status & 8:\n                break\n        frame = _highbank_write_fields(state, frame, frame.roster.base, 65535)\n        frame = _movement_add_word(state, frame, 'target_x', 1)\n    frame = _highbank_dbra_fields(frame, 'unit')\n    if low16(frame.unit) == 65535:\n        return frame"}})

APPROVED.setdefault('business_commands',set()).update(('append_current_command_description_frame_fields',))

APPROVED.setdefault('business_map',set()).update(('refresh_world_cursor_attributes_alternate_1_frame_fields',))

APPROVED.setdefault('business_movement_support',set()).update(('_movement_divu_word', '_movement_multiply_word', '_movement_restore_longs', '_movement_save_longs', '_movement_shift_long'))

APPROVED.setdefault('contexts_gameplay',set()).update(('FirstDeploymentReturnBoundary',))

APPROVED.setdefault((2, 'high_level_battle_ai.business_actions'),set()).update(('sample_battle_action_random_fields',))

APPROVED.setdefault((2, 'high_level_battle_ai.contexts_policy_memory'),set()).update(('BattlePolicyMemory',))

APPROVED.setdefault((2, 'high_level_gameplay_flow.business_battle'),set()).update(('_postbattle_bit_fields',))

APPROVED.setdefault((2, 'high_level_gameplay_flow.contexts_services'),set()).update(('SceneRefreshMemory',))

APPROVED.setdefault((2, 'high_level_remaining_flows.business_city'),set()).update(('_deployment_menu_call_fields', '_duel_menu_write_word_fields', '_resource_cost_frame', '_settlement_change_header_byte_fields', '_settlement_store_word_fields', '_special_action_shift_long'))

APPROVED.setdefault((2, 'high_level_remaining_flows.business_highbank'),set()).update(('_position_order_shift',))

APPROVED.setdefault((2, 'high_level_scene_flows.business_scene'),set()).update(('expand_glyph_row_fields',))


# Reconstruction repair: 6740A BEQ skips 6740C..6742A, including the A1 read.
DECLARATIONS.update({'append_scrolling_message_bitmap_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _highbank_frame_fields(state, frame, 422822)\nframe = _movement_move(state, frame, 'unit', 64, 16)\nframe = first_replace(frame, candidates=state.table_at(4294964502).cursor())\nframe = _movement_test(state, frame, state.read(4294964090, 2), 16)\nif not frame.status & 4:\n    frame = _movement_move(state, frame, 'unit', 96, 16)\n    frame = _movement_move(state, frame, 'target_y', 3, 16)\n    while True:\n        frame = _highbank_child_fields(state, frame, 423054, 422848)\n        for displacement in (192, 96, 0):\n            frame = _highbank_write_fields(state, frame, u32(frame.roster.base + displacement), frame.offset_x, 4)\n        frame = first_replace(frame, roster=frame.roster.advance(4))\n        frame = _highbank_dbra_fields(frame, 'target_y')\n        if low16(frame.target_y) == 65535:\n            break\nframe = _movement_move(state, frame, 'count', low16(frame.unit), 16)\nframe = _highbank_shift_fields(state, frame, 'count', 1)\nframe, value = _highbank_memory_add_fields(state, frame, 4294963994, low16(frame.count))\nframe, value = _highbank_memory_add_fields(state, frame, 4294963994, low16(frame.unit))\nframe, value = _highbank_memory_add_fields(state, frame, 4294963994, 4)\nframe = _movement_move_long(state, frame, 'unit', swap_words(frame.unit))\nframe = _movement_move_long(state, frame, 'count', swap_words(frame.count))\nframe = _movement_move(state, frame, 'unit', 15, 16)\nframe = _movement_move(state, frame, 'count', state.read(4294964092, 2), 16)\nframe = _movement_move(state, frame, 'count', low16(frame.count) & 7, 16)\nwhile True:\n    frame = _highbank_child_fields(state, frame, 423018, 422900)\n    frame = _highbank_child_fields(state, frame, 44804, 422906)\n    stack = frame.stack_cursor.advance(-4)\n    frame = _highbank_write_fields(state, frame, stack.base, frame.choice, 4)\n    frame = first_replace(frame, stack_cursor=stack)\n    frame = _highbank_child_fields(state, frame, 44804, 422914)\n    saved = frame.stack_cursor.long()\n    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(4))\n    frame = _movement_move_long(state, frame, 'distance', saved)\n    frame = _highbank_child_fields(state, frame, 423054, 422920)\n    frame = _movement_move(state, frame, 'offset_y', low16(frame.count), 16)\n    if not frame.status & 4:\n        frame = _highbank_shift_fields(state, frame, 'offset_y', 2)\n        frame, value = _movement_binary_flags(state, frame, low16(frame.offset_y), 1, 16, True)\n        frame = first_replace(frame, offset_y=replace_word(frame.offset_y, value))\n        frame = _movement_move(state, frame, 'target_x', 0, 16)\n        while True:\n            state.set_status_word(state.sr & 65519)\n            frame = first_replace(frame, status=state.sr & 31)\n            for name in ('distance', 'choice', 'offset_x'):\n                frame = _highbank_roxr_plane_fields(state, frame, name)\n            state.set_status_word(state.sr | 16)\n            frame = first_replace(frame, status=state.sr & 31)\n            frame = _highbank_roxr_plane_fields(state, frame, 'target_x')\n            frame = _highbank_dbra_fields(frame, 'offset_y')\n            if low16(frame.offset_y) == 65535:\n                break\n        frame = _movement_move_long(state, frame, 'target_y', frame.candidates.long())\n        frame = _movement_move_long(state, frame, 'target_y', frame.target_y & frame.target_x)\n        frame = _movement_move_long(state, frame, 'distance', frame.distance | frame.target_y)\n    frame = _movement_move_long(state, frame, 'unit', swap_words(frame.unit))\n    frame = _movement_move_long(state, frame, 'count', swap_words(frame.count))\n    frame = _highbank_write_fields(state, frame, u32(frame.roster.base + s16(low16(frame.count))), frame.offset_x, 4)\n    frame = _highbank_write_fields(state, frame, u32(frame.roster.base + s16(low16(frame.unit))), frame.choice, 4)\n    frame = _highbank_write_fields(state, frame, frame.roster.base, frame.distance, 4)\n    frame = first_replace(frame, roster=frame.roster.advance(4))\n    frame = _highbank_write_fields(state, frame, frame.candidates.base, frame.offset_x, 4)\n    frame = first_replace(frame, candidates=frame.candidates.advance(4))\n    frame = _movement_move_long(state, frame, 'unit', swap_words(frame.unit))\n    frame = _movement_move_long(state, frame, 'count', swap_words(frame.count))\n    frame = _highbank_dbra_fields(frame, 'unit')\n    if low16(frame.unit) == 65535:\n        break\nframe = _movement_move_long(state, frame, 'unit', swap_words(frame.unit))\nframe = _movement_move_long(state, frame, 'count', swap_words(frame.count))\nframe = _movement_test(state, frame, state.read(4294964090, 2), 16)\nif not frame.status & 4:\n    frame = _movement_move(state, frame, 'target_y', 3, 16)\n    while True:\n        frame = _highbank_child_fields(state, frame, 423054, 422998)\n        frame = _highbank_write_fields(state, frame, u32(frame.roster.base + s16(low16(frame.count))), frame.offset_x, 4)\n        frame = _highbank_write_fields(state, frame, u32(frame.roster.base + s16(low16(frame.unit))), frame.offset_x, 4)\n        frame = _highbank_write_fields(state, frame, frame.roster.base, frame.offset_x, 4)\n        frame = first_replace(frame, roster=frame.roster.advance(4))\n        frame = _highbank_dbra_fields(frame, 'target_y')\n        if low16(frame.target_y) == 65535:\n            break\nreturn _highbank_write_fields(state, frame, u32(frame.roster.base + s16(low16(frame.count))), 0, clear=True)"}})

# C57 sole complete 676C4 control and truthful legacy projections.
DECLARATIONS.update({'_message_control_transaction_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': "from ..high_level_command_actions.contexts_message import MessageMemory\nfrom ..high_level_command_actions.business_reuse import _prepare_message_fields\nframe = _highbank_frame_fields(state, frame, 423620)\nframe = _movement_move(state, frame, 'target_x', state.read(4294964096, 2), 16)\nframe = _movement_compare(state, frame, low16(frame.target_x), 96, 16)\nif frame.status & 1:\n    frame = _highbank_shift_fields(state, frame, 'target_x', 1)\n    frame = _movement_move(state, frame, 'target_x', state.table_at(423638).word(low16(frame.target_x)), 16)\nelse:\n    frame, selected = _movement_binary_flags(state, frame, low16(frame.target_x), 96, 16, True)\n    frame = first_replace(frame, target_x=replace_word(frame.target_x, selected))\n    frame = _highbank_shift_fields(state, frame, 'target_x', 1)\n    frame = _movement_move(state, frame, 'target_x', state.table_at(423756).word(low16(frame.target_x)), 16)\n    frame = first_replace(frame, roster=state.table_at(423858).cursor())\n    frame = _highbank_child_fields(state, frame, u32(423858 + s16(low16(frame.target_x))), 423666)\nmemory = MessageMemory(state, frame)\npreparation = _prepare_message_fields(memory, low16(frame.target_x))\nreturn (memory.frame, preparation)"}, 'dispatch_message_control_frame_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'returned, preparation = _message_control_transaction_fields(state, frame)\nreturn returned'}, 'dispatch_message_control_fields': {'signature': 'state: SceneState, layout: MessageLayout | None=None, *, entry_frame: FirstDeploymentFrame | None=None', 'returns': 'MessageControlFields', 'flow': "checked_state(state)\nif layout is not None:\n    checked_context(layout, MessageLayout, state)\nif entry_frame is None:\n    raise Boundary('676C4 control requires its actual complete D/A/SR-X/SP entry frame')\nreturned, preparation = _message_control_transaction_fields(state, entry_frame)\ncurrent = None if layout is None else _highbank_message_projection(state, returned)\nif preparation.resolved is None:\n    field = destination = source = tile = None\nelse:\n    field = preparation.resolved.item_offset\n    destination = state.table_at(preparation.resolved.pointer).cursor()\n    source = state.table_at(preparation.resolved.descriptor).cursor()\n    tile = low16(returned.unit)\nstatus = returned.status\nreturn MessageControlFields(low16(returned.target_x), field, destination, source, current, bool(status & 1), bool(status & 4), bool(status & 8), bool(status & 2), tile).validate(state)"}, 'dispatch_message_control': {'signature': 'state: SceneState, layout: MessageLayout, *, entry_frame: FirstDeploymentFrame | None=None', 'returns': 'MessageLayout', 'flow': "checked_context(layout, MessageLayout, state)\nif entry_frame is None:\n    raise Boundary('676C4 legacy layout is missing actual full address registers and A7/CCR-X')\nreturned = dispatch_message_control_frame_fields(state, entry_frame)\nreturn _highbank_message_projection(state, returned)"}})
APPROVED.setdefault((2,'high_level_command_actions.contexts_message'),set()).update({'MessageMemory'})
APPROVED.setdefault((2,'high_level_command_actions.business_reuse'),set()).update({'_prepare_message_fields'})

APPROVED.setdefault((2, 'high_level_remaining_flows.business_highbank'), set()).update(('build_scenario_paired_columns_fields', 'confirm_scenario_force_choice_fields'))


# Source136: saturation cap is extracted from the sole complete growth algorithm.
DECLARATIONS.update({'increase_growth_random_attribute_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_remaining_flows.business_city import _resource_cost_frame, _settlement_store_word_fields, _special_action_shift_long\nframe = _resource_cost_frame(state, frame, 418772)\nframe = _growth_saved_index_random_fields(state, frame, 418780)\nframe = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)\nframe = _movement_move_long(state, frame, 'target_y', frame.target_x)\nframe = _special_action_shift_long(state, frame, 'target_y', 1)\nframe = _movement_arithmetic_long(state, frame, 'target_y', frame.target_x)\nframe = _movement_move_long(state, frame, 'target_y', swap_words(frame.target_y))\nrestored = frame.stack_cursor.word()\nframe = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\nframe = _movement_move(state, frame, 'target_x', restored, 16)\nframe = _movement_move(state, frame, 'unit', low16(frame.target_y), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 2)\nframe = _movement_add_word(state, frame, 'target_y', low16(frame.unit))\nframe = first_replace(frame, opponent=state.table_at(4294948864))\nframe = _movement_move(state, frame, 'unit', frame.opponent.word(low16(frame.target_x)), 16)\nframe = _movement_add_word(state, frame, 'unit', low16(frame.target_y))\nframe = _movement_compare(state, frame, low16(frame.unit), 150, 16)\nif not frame.status & 5:\n    frame = _movement_move(state, frame, 'unit', 150, 16)\nreturn _settlement_store_word_fields(state, frame, frame.opponent, low16(frame.target_x), low16(frame.unit))", 'slots': {150: ('growth_random_attribute_cap', 0, 65535)}}})


# Source141: sole full force-marker algorithm and real CALL routes; physical owners unchanged.
DECLARATIONS.update({'_force_render_fields': {'signature': 'state: SceneState, fields: RenderFields, *, entry_frame: FirstDeploymentFrame | None=None', 'returns': 'RenderFields', 'flow': 'actual = _force_render_entry_fields(state, fields, entry_frame)\nreturned = render_force_city_markers_fields(state, actual)\nreturn RenderFields(returned.target_x, returned.target_y, returned.unit, returned.count, returned.distance, returned.offset_x, returned.offset_y, returned.choice, returned.roster, returned.candidates, returned.controller, bool(returned.status & 1), bool(returned.status & 4), bool(returned.status & 8), bool(returned.status & 2), returned.stack_cursor)'}, 'render_force_city_markers': {'signature': 'state: SceneState, layout: MessageLayout, *, entry_frame: FirstDeploymentFrame | None=None', 'returns': 'MessageLayout', 'flow': 'checked_context(layout, MessageLayout, state)\nfields = RenderFields(layout.symbol, layout.position, layout.stride, layout.row_offset, layout.first_plane, layout.fill, layout.shift_count, layout.second_plane, layout.bitmap, layout.destination, layout.previous_rows, None, None, None, None, None)\nresult = _force_render_fields(state, fields, entry_frame=entry_frame)\nreturn replace(layout, symbol=result.x, position=result.y, stride=result.attributes)'}, 'render_force_city_markers_complete': {'signature': 'state: SceneState, frame: MapTickFrame, *, entry_frame: FirstDeploymentFrame | None=None', 'returns': 'MapTickFrame', 'flow': "from .business_gameplay import _render_from_tick\nchecked_tick_frame(frame, state)\nif entry_frame is None:\n    raise Boundary('679FC MapTick projection requires independently supplied complete entry_frame')\nactual = _force_render_entry_fields(state, _render_from_tick(state, frame), entry_frame)\nif frame.vdp_port.base != actual.auxiliary.base:\n    raise ValueError('679FC MapTick A6 observation contradicts actual entry')\nreturned = render_force_city_markers_fields(state, actual)\nreturn replace(frame, motion_x=returned.target_x, motion_y=returned.target_y, attributes=returned.unit, tile_count=returned.count, officer=returned.distance, count=returned.offset_x, index=returned.offset_y, control_latch=returned.choice, source=returned.roster, destination=returned.candidates, packet=returned.controller, vdp_port=returned.auxiliary, stack_cursor=returned.stack_cursor, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))"}, '_highbank_target_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int', 'returns': 'FirstDeploymentFrame', 'flow': "if target == 420948:\n    from ..high_level_remaining_flows.business_highbank import confirm_scenario_force_choice_fields\n    return confirm_scenario_force_choice_fields(state, frame)\nif target == 423344:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_paired_columns_fields\n    return build_scenario_paired_columns_fields(state, frame)\nif target == 419076:\n    return sort_high_loyalty_officers_fields(state, frame)\nif target == 419196:\n    return append_mid_loyalty_officers_by_trait_fields(state, frame)\nif target == 422740:\n    return append_scrolling_message_header_fields(state, frame)\nif target == 422796:\n    return append_scrolling_message_glyph_fields(state, frame)\nif target == 422822:\n    return append_scrolling_message_bitmap_fields(state, frame)\nif target == 423018:\n    return lookup_message_layout_words_fields(state, frame)\nif target == 423054:\n    return lookup_message_fill_pattern_fields(state, frame)\nif target == 423178:\n    return lookup_message_decoration_style_fields(state, frame)\nif target == 44804:\n    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\n    from ..high_level_scene_flows.business_scene import expand_glyph_row_fields\n    return expand_glyph_row_fields(SceneRefreshMemory(state), frame)\nif target == 41304:\n    from .business_map import refresh_world_cursor_attributes_alternate_1_frame_fields\n    return refresh_world_cursor_attributes_alternate_1_frame_fields(state, frame)\nif target == 55532:\n    from .business_commands import append_current_command_description_frame_fields\n    return append_current_command_description_frame_fields(state, frame)\nif target == 240466:\n    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\n    from ..high_level_scene_flows.business_scene import write_vdp_swapped_byte_rle_stream_fields\n    return write_vdp_swapped_byte_rle_stream_fields(SceneRefreshMemory(state), frame)\nif target == 44048:\n    from ..high_level_player_commands.contexts_display import SpritePacketMemory\n    from ..high_level_player_commands.business_display import append_live_command_sprite_fields\n    return append_live_command_sprite_fields(SpritePacketMemory(state), frame, reset_scroll=False, initialize_clip=True)\nraise MovementContinuationBoundary(target, frame, 'actual Highbank child has no admitted full-field return')"}, '_force_render_entry_fields': {'signature': 'state: SceneState, fields: RenderFields, entry_frame: FirstDeploymentFrame | None', 'returns': 'FirstDeploymentFrame', 'flow': "checked_render_fields(fields, state)\nif entry_frame is None:\n    raise Boundary('679FC render observations require actual complete16 carriers/CCR-X/SP')\nframe = _highbank_frame_fields(state, entry_frame, 424444)\nif (fields.x, fields.y, fields.attributes, fields.tile, fields.officer, fields.count, fields.index, fields.remaining) != (frame.target_x, frame.target_y, frame.unit, frame.count, frame.distance, frame.offset_x, frame.offset_y, frame.choice):\n    raise ValueError('679FC legacy numeric observations contradict actual entry')\nfor observed, actual in ((fields.source, frame.roster), (fields.destination, frame.candidates), (fields.packet, frame.controller), (fields.stack_cursor, frame.stack_cursor)):\n    if observed is not None and observed.base != actual.base:\n        raise ValueError('679FC legacy address observation contradicts actual entry')\nfor observed, mask in ((fields.carry, 1), (fields.zero, 4), (fields.negative, 8), (fields.overflow, 2)):\n    if observed is not None and observed != bool(frame.status & mask):\n        raise ValueError('679FC legacy condition observation contradicts actual entry')\nreturn frame"}, 'render_force_city_markers_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _highbank_frame_fields(state, frame, 424444)\nframe = _movement_compare(state, frame, state.read(4294964754, 2), 512, 16)\nif frame.status & 4:\n    frame = _movement_compare(state, frame, state.read(4294964050, 2), 16, 16)\n    if frame.status & 5:\n        return frame\nframe = _movement_test(state, frame, state.read(4294963144, 2), 16)\nif frame.status & 4:\n    state.set_status_word(9984)\n    frame = first_replace(frame, status=0, roster=state.table_at(425104).cursor())\n    frame = _movement_move(state, frame, 'target_x', 8192, 16)\n    frame = _highbank_child_fields(state, frame, 240466, 424492)\n    state.set_status_word(9472)\n    frame = first_replace(frame, status=0)\n    frame = _highbank_write_fields(state, frame, 4294963144, 1)\nframe = _movement_compare(state, frame, state.read(4294964050, 2), 32, 16)\nfor offset, color in ((0, 0), (2, 3648), (4, 2798), (6, 2574), (8, 736), (10, 206), (12, 3744), (14, 0)):\n    frame = _highbank_write_fields(state, frame, 4294966096 + offset, color)\nframe = _movement_move_long(state, frame, 'target_x', 0)\nwhile True:\n    frame = _movement_save_longs(state, frame, ('target_x',))\n    frame = _movement_move_long(state, frame, 'target_y', 0)\n    frame = first_replace(frame, roster=state.table_at(4294964264).cursor())\n    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(s16(low16(frame.target_x))), 8)\n    frame = _movement_compare(state, frame, low8(frame.target_y), 255, 8)\n    if not frame.status & 4:\n        frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)\n        frame = _movement_save_longs(state, frame, ('target_x',))\n        frame = _movement_move(state, frame, 'target_x', state.read(4294964000, 2), 16)\n        frame = _movement_fixed_shift_word(state, frame, 'target_x', 3, True)\n        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 1, 16)\n        frame = _movement_add_word(state, frame, 'target_y', low16(frame.target_x))\n        frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)\n        frame = first_replace(frame, candidates=state.table_at(424720).cursor())\n        pointer = frame.candidates.long(s16(low16(frame.target_y)))\n        frame = first_replace(frame, roster=state.table_at(pointer).cursor())\n        frame = _movement_restore_longs(state, frame, ('target_x',))\n        frame = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)\n        frame = _movement_fixed_shift_word(state, frame, 'unit', 2)\n        frame = first_replace(frame, candidates=state.table_at(871114).cursor())\n        frame = _movement_move(state, frame, 'target_x', frame.candidates.word(s16(low16(frame.unit)), 2), 16)\n        frame, value = _movement_binary_flags(state, frame, low16(frame.target_x), 16, 16, True)\n        frame = first_replace(frame, target_x=replace_word(frame.target_x, value))\n        frame = _movement_move(state, frame, 'target_y', frame.candidates.word(s16(low16(frame.unit))), 16)\n        frame = _movement_move(state, frame, 'unit', 0, 16)\n        frame = _highbank_write_fields(state, frame, 4294964746, state.read(4294963988, 2))\n        frame = _highbank_write_fields(state, frame, 4294964750, state.read(4294963992, 2))\n        frame = _highbank_child_fields(state, frame, 44048, 424706)\n    frame = _movement_restore_longs(state, frame, ('target_x',))\n    frame = _movement_add_word(state, frame, 'target_x', 1)\n    frame = _movement_compare(state, frame, low16(frame.target_x), 40, 16)\n    if not frame.status & 1:\n        return frame"}})
APPROVED.setdefault((2, 'high_level_gameplay_flow.contexts_services'), set()).update(('SceneRefreshMemory',))
APPROVED.setdefault((2, 'high_level_scene_flows.business_scene'), set()).update(('write_vdp_swapped_byte_rle_stream_fields',))
APPROVED.setdefault((2, 'high_level_player_commands.contexts_display'), set()).update(('SpritePacketMemory',))
APPROVED.setdefault((2, 'high_level_player_commands.business_display'), set()).update(('append_live_command_sprite_fields',))

# B108 actual674CA four-entry layout table; existing paired entry remains unchanged.
APPROVED.setdefault((2, 'high_level_remaining_flows.business_highbank'), set()).update(['build_scenario_single_row_fields', 'build_scenario_triple_columns_fields', 'build_scenario_alternate_row_fields'])
DECLARATIONS.update({'_highbank_target_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int', 'returns': 'FirstDeploymentFrame', 'flow': "if target == 423198:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_single_row_fields\n    return build_scenario_single_row_fields(state, frame)\nif target == 423438:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_triple_columns_fields\n    return build_scenario_triple_columns_fields(state, frame)\nif target == 423570:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_alternate_row_fields\n    return build_scenario_alternate_row_fields(state, frame)\nif target == 420948:\n    from ..high_level_remaining_flows.business_highbank import confirm_scenario_force_choice_fields\n    return confirm_scenario_force_choice_fields(state, frame)\nif target == 423344:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_paired_columns_fields\n    return build_scenario_paired_columns_fields(state, frame)\nif target == 419076:\n    return sort_high_loyalty_officers_fields(state, frame)\nif target == 419196:\n    return append_mid_loyalty_officers_by_trait_fields(state, frame)\nif target == 422740:\n    return append_scrolling_message_header_fields(state, frame)\nif target == 422796:\n    return append_scrolling_message_glyph_fields(state, frame)\nif target == 422822:\n    return append_scrolling_message_bitmap_fields(state, frame)\nif target == 423018:\n    return lookup_message_layout_words_fields(state, frame)\nif target == 423054:\n    return lookup_message_fill_pattern_fields(state, frame)\nif target == 423178:\n    return lookup_message_decoration_style_fields(state, frame)\nif target == 44804:\n    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\n    from ..high_level_scene_flows.business_scene import expand_glyph_row_fields\n    return expand_glyph_row_fields(SceneRefreshMemory(state), frame)\nif target == 41304:\n    from .business_map import refresh_world_cursor_attributes_alternate_1_frame_fields\n    return refresh_world_cursor_attributes_alternate_1_frame_fields(state, frame)\nif target == 55532:\n    from .business_commands import append_current_command_description_frame_fields\n    return append_current_command_description_frame_fields(state, frame)\nif target == 240466:\n    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\n    from ..high_level_scene_flows.business_scene import write_vdp_swapped_byte_rle_stream_fields\n    return write_vdp_swapped_byte_rle_stream_fields(SceneRefreshMemory(state), frame)\nif target == 44048:\n    from ..high_level_player_commands.contexts_display import SpritePacketMemory\n    from ..high_level_player_commands.business_display import append_live_command_sprite_fields\n    return append_live_command_sprite_fields(SpritePacketMemory(state), frame, reset_scroll=False, initialize_clip=True)\nraise MovementContinuationBoundary(target, frame, 'actual Highbank child has no admitted full-field return')"}})

# B109 actual6724E text terminator tail; preserve original live stack.
APPROVED.setdefault((2, 'high_level_remaining_flows.business_highbank'), set()).add('restore_scenario_saved_command_fields')
DECLARATIONS.update({'_highbank_target_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int', 'returns': 'FirstDeploymentFrame', 'flow': "if target == 422478:\n    from ..high_level_remaining_flows.business_highbank import restore_scenario_saved_command_fields\n    return restore_scenario_saved_command_fields(state, frame)\nif target == 423198:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_single_row_fields\n    return build_scenario_single_row_fields(state, frame)\nif target == 423438:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_triple_columns_fields\n    return build_scenario_triple_columns_fields(state, frame)\nif target == 423570:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_alternate_row_fields\n    return build_scenario_alternate_row_fields(state, frame)\nif target == 420948:\n    from ..high_level_remaining_flows.business_highbank import confirm_scenario_force_choice_fields\n    return confirm_scenario_force_choice_fields(state, frame)\nif target == 423344:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_paired_columns_fields\n    return build_scenario_paired_columns_fields(state, frame)\nif target == 419076:\n    return sort_high_loyalty_officers_fields(state, frame)\nif target == 419196:\n    return append_mid_loyalty_officers_by_trait_fields(state, frame)\nif target == 422740:\n    return append_scrolling_message_header_fields(state, frame)\nif target == 422796:\n    return append_scrolling_message_glyph_fields(state, frame)\nif target == 422822:\n    return append_scrolling_message_bitmap_fields(state, frame)\nif target == 423018:\n    return lookup_message_layout_words_fields(state, frame)\nif target == 423054:\n    return lookup_message_fill_pattern_fields(state, frame)\nif target == 423178:\n    return lookup_message_decoration_style_fields(state, frame)\nif target == 44804:\n    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\n    from ..high_level_scene_flows.business_scene import expand_glyph_row_fields\n    return expand_glyph_row_fields(SceneRefreshMemory(state), frame)\nif target == 41304:\n    from .business_map import refresh_world_cursor_attributes_alternate_1_frame_fields\n    return refresh_world_cursor_attributes_alternate_1_frame_fields(state, frame)\nif target == 55532:\n    from .business_commands import append_current_command_description_frame_fields\n    return append_current_command_description_frame_fields(state, frame)\nif target == 240466:\n    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\n    from ..high_level_scene_flows.business_scene import write_vdp_swapped_byte_rle_stream_fields\n    return write_vdp_swapped_byte_rle_stream_fields(SceneRefreshMemory(state), frame)\nif target == 44048:\n    from ..high_level_player_commands.contexts_display import SpritePacketMemory\n    from ..high_level_player_commands.business_display import append_live_command_sprite_fields\n    return append_live_command_sprite_fields(SpritePacketMemory(state), frame, reset_scroll=False, initialize_clip=True)\nraise MovementContinuationBoundary(target, frame, 'actual Highbank child has no admitted full-field return')"}})

# B109 finite67238 controls: actual direct tail preserves original scrolling caller slot.
APPROVED.setdefault((2, 'high_level_remaining_flows.business_highbank'), set()).update(['toggle_scenario_choice_fields', 'compose_scenario_numeric_text_fields', 'compose_scenario_numeric_text_fields_entry_6729c', 'compose_scenario_member_name_fields', 'compose_scenario_member_name_fields_entry_672e6', 'restore_scenario_previous_text_fields', 'compose_scenario_member_name_fields_entry_672f6', 'compose_scenario_status_pair_fields', 'compose_scenario_numeric_text_fields_entry_67338', 'compose_scenario_numeric_text_fields_entry_67346'])
DECLARATIONS.update({'_highbank_target_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int', 'returns': 'FirstDeploymentFrame', 'flow': "if target == 422492:\n    from ..high_level_remaining_flows.business_highbank import toggle_scenario_choice_fields\n    return toggle_scenario_choice_fields(state, frame)\nif target == 422504:\n    from ..high_level_remaining_flows.business_highbank import compose_scenario_numeric_text_fields\n    return compose_scenario_numeric_text_fields(state, frame)\nif target == 422556:\n    from ..high_level_remaining_flows.business_highbank import compose_scenario_numeric_text_fields_entry_6729c\n    return compose_scenario_numeric_text_fields_entry_6729c(state, frame)\nif target == 422562:\n    from ..high_level_remaining_flows.business_highbank import compose_scenario_member_name_fields\n    return compose_scenario_member_name_fields(state, frame)\nif target == 422630:\n    from ..high_level_remaining_flows.business_highbank import compose_scenario_member_name_fields_entry_672e6\n    return compose_scenario_member_name_fields_entry_672e6(state, frame)\nif target == 422636:\n    from ..high_level_remaining_flows.business_highbank import restore_scenario_previous_text_fields\n    return restore_scenario_previous_text_fields(state, frame)\nif target == 422646:\n    from ..high_level_remaining_flows.business_highbank import compose_scenario_member_name_fields_entry_672f6\n    return compose_scenario_member_name_fields_entry_672f6(state, frame)\nif target == 422662:\n    from ..high_level_remaining_flows.business_highbank import compose_scenario_status_pair_fields\n    return compose_scenario_status_pair_fields(state, frame)\nif target == 422712:\n    from ..high_level_remaining_flows.business_highbank import compose_scenario_numeric_text_fields_entry_67338\n    return compose_scenario_numeric_text_fields_entry_67338(state, frame)\nif target == 422726:\n    from ..high_level_remaining_flows.business_highbank import compose_scenario_numeric_text_fields_entry_67346\n    return compose_scenario_numeric_text_fields_entry_67346(state, frame)\nif target == 422478:\n    from ..high_level_remaining_flows.business_highbank import restore_scenario_saved_command_fields\n    return restore_scenario_saved_command_fields(state, frame)\nif target == 423198:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_single_row_fields\n    return build_scenario_single_row_fields(state, frame)\nif target == 423438:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_triple_columns_fields\n    return build_scenario_triple_columns_fields(state, frame)\nif target == 423570:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_alternate_row_fields\n    return build_scenario_alternate_row_fields(state, frame)\nif target == 420948:\n    from ..high_level_remaining_flows.business_highbank import confirm_scenario_force_choice_fields\n    return confirm_scenario_force_choice_fields(state, frame)\nif target == 423344:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_paired_columns_fields\n    return build_scenario_paired_columns_fields(state, frame)\nif target == 419076:\n    return sort_high_loyalty_officers_fields(state, frame)\nif target == 419196:\n    return append_mid_loyalty_officers_by_trait_fields(state, frame)\nif target == 422740:\n    return append_scrolling_message_header_fields(state, frame)\nif target == 422796:\n    return append_scrolling_message_glyph_fields(state, frame)\nif target == 422822:\n    return append_scrolling_message_bitmap_fields(state, frame)\nif target == 423018:\n    return lookup_message_layout_words_fields(state, frame)\nif target == 423054:\n    return lookup_message_fill_pattern_fields(state, frame)\nif target == 423178:\n    return lookup_message_decoration_style_fields(state, frame)\nif target == 44804:\n    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\n    from ..high_level_scene_flows.business_scene import expand_glyph_row_fields\n    return expand_glyph_row_fields(SceneRefreshMemory(state), frame)\nif target == 41304:\n    from .business_map import refresh_world_cursor_attributes_alternate_1_frame_fields\n    return refresh_world_cursor_attributes_alternate_1_frame_fields(state, frame)\nif target == 55532:\n    from .business_commands import append_current_command_description_frame_fields\n    return append_current_command_description_frame_fields(state, frame)\nif target == 240466:\n    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\n    from ..high_level_scene_flows.business_scene import write_vdp_swapped_byte_rle_stream_fields\n    return write_vdp_swapped_byte_rle_stream_fields(SceneRefreshMemory(state), frame)\nif target == 44048:\n    from ..high_level_player_commands.contexts_display import SpritePacketMemory\n    from ..high_level_player_commands.business_display import append_live_command_sprite_fields\n    return append_live_command_sprite_fields(SpritePacketMemory(state), frame, reset_scroll=False, initialize_clip=True)\nraise MovementContinuationBoundary(target, frame, 'actual Highbank child has no admitted full-field return')"}})

# B113 finite6774C special-message exact children:676EE already owns the real676F2 LONG.
APPROVED.setdefault((2, 'high_level_remaining_flows.business_highbank'), set()).update(['highbank_coordinate_live_state_178_fields', 'highbank_coordinate_live_state_179_fields', 'highbank_coordinate_live_state_180_fields', 'highbank_coordinate_live_state_178_alternate_1_fields', 'highbank_coordinate_live_state_178_alternate_2_fields', 'highbank_update_live_fields_18_fields', 'highbank_select_live_state_44_fields', 'highbank_update_live_fields_19_fields', 'highbank_update_live_fields_20_fields', 'highbank_update_live_fields_21_fields', 'highbank_coordinate_live_state_181_fields', 'highbank_coordinate_live_state_182_fields', 'highbank_update_live_fields_22_fields', 'highbank_update_live_fields_23_fields', 'highbank_coordinate_live_state_183_fields', 'highbank_coordinate_live_state_178_alternate_3_fields', 'highbank_coordinate_live_state_178_alternate_4_fields', 'highbank_update_live_fields_24_fields', 'highbank_update_live_fields_25_fields', 'highbank_coordinate_live_state_178_alternate_5_fields', 'highbank_update_live_fields_26_fields', 'highbank_coordinate_live_state_178_alternate_6_fields', 'highbank_update_live_fields_27_fields', 'highbank_update_live_fields_28_fields', 'highbank_update_live_fields_29_fields', 'highbank_update_live_fields_30_fields', 'highbank_update_live_fields_31_fields', 'highbank_update_live_fields_32_fields', 'highbank_coordinate_live_state_184_fields', 'highbank_coordinate_live_state_178_alternate_7_fields', 'highbank_update_live_fields_33_fields', 'highbank_update_live_fields_34_fields', 'highbank_update_live_fields_35_fields'])
DECLARATIONS.update({'_highbank_target_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int', 'returns': 'FirstDeploymentFrame', 'flow': "if target == 423858:\n    from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_178_fields\n    return highbank_coordinate_live_state_178_fields(state, frame)\nif target == 423940:\n    from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_179_fields\n    return highbank_coordinate_live_state_179_fields(state, frame)\nif target == 423960:\n    from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_180_fields\n    return highbank_coordinate_live_state_180_fields(state, frame)\nif target == 424024:\n    from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_178_alternate_1_fields\n    return highbank_coordinate_live_state_178_alternate_1_fields(state, frame)\nif target == 424062:\n    from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_178_alternate_2_fields\n    return highbank_coordinate_live_state_178_alternate_2_fields(state, frame)\nif target == 424098:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_18_fields\n    return highbank_update_live_fields_18_fields(state, frame)\nif target == 424104:\n    from ..high_level_remaining_flows.business_highbank import highbank_select_live_state_44_fields\n    return highbank_select_live_state_44_fields(state, frame)\nif target == 424120:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_19_fields\n    return highbank_update_live_fields_19_fields(state, frame)\nif target == 424126:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_20_fields\n    return highbank_update_live_fields_20_fields(state, frame)\nif target == 424132:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_21_fields\n    return highbank_update_live_fields_21_fields(state, frame)\nif target == 424138:\n    from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_181_fields\n    return highbank_coordinate_live_state_181_fields(state, frame)\nif target == 424156:\n    from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_182_fields\n    return highbank_coordinate_live_state_182_fields(state, frame)\nif target == 424192:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_22_fields\n    return highbank_update_live_fields_22_fields(state, frame)\nif target == 424198:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_23_fields\n    return highbank_update_live_fields_23_fields(state, frame)\nif target == 424204:\n    from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_183_fields\n    return highbank_coordinate_live_state_183_fields(state, frame)\nif target == 424222:\n    from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_178_alternate_3_fields\n    return highbank_coordinate_live_state_178_alternate_3_fields(state, frame)\nif target == 424230:\n    from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_178_alternate_4_fields\n    return highbank_coordinate_live_state_178_alternate_4_fields(state, frame)\nif target == 424238:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_24_fields\n    return highbank_update_live_fields_24_fields(state, frame)\nif target == 424244:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_25_fields\n    return highbank_update_live_fields_25_fields(state, frame)\nif target == 424250:\n    from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_178_alternate_5_fields\n    return highbank_coordinate_live_state_178_alternate_5_fields(state, frame)\nif target == 424270:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_26_fields\n    return highbank_update_live_fields_26_fields(state, frame)\nif target == 424276:\n    from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_178_alternate_6_fields\n    return highbank_coordinate_live_state_178_alternate_6_fields(state, frame)\nif target == 424284:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_27_fields\n    return highbank_update_live_fields_27_fields(state, frame)\nif target == 424290:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_28_fields\n    return highbank_update_live_fields_28_fields(state, frame)\nif target == 424296:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_29_fields\n    return highbank_update_live_fields_29_fields(state, frame)\nif target == 424302:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_30_fields\n    return highbank_update_live_fields_30_fields(state, frame)\nif target == 424308:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_31_fields\n    return highbank_update_live_fields_31_fields(state, frame)\nif target == 424314:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_32_fields\n    return highbank_update_live_fields_32_fields(state, frame)\nif target == 424320:\n    from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_184_fields\n    return highbank_coordinate_live_state_184_fields(state, frame)\nif target == 424376:\n    from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_178_alternate_7_fields\n    return highbank_coordinate_live_state_178_alternate_7_fields(state, frame)\nif target == 424384:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_33_fields\n    return highbank_update_live_fields_33_fields(state, frame)\nif target == 424390:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_34_fields\n    return highbank_update_live_fields_34_fields(state, frame)\nif target == 424396:\n    from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_35_fields\n    return highbank_update_live_fields_35_fields(state, frame)\nif target == 422492:\n    from ..high_level_remaining_flows.business_highbank import toggle_scenario_choice_fields\n    return toggle_scenario_choice_fields(state, frame)\nif target == 422504:\n    from ..high_level_remaining_flows.business_highbank import compose_scenario_numeric_text_fields\n    return compose_scenario_numeric_text_fields(state, frame)\nif target == 422556:\n    from ..high_level_remaining_flows.business_highbank import compose_scenario_numeric_text_fields_entry_6729c\n    return compose_scenario_numeric_text_fields_entry_6729c(state, frame)\nif target == 422562:\n    from ..high_level_remaining_flows.business_highbank import compose_scenario_member_name_fields\n    return compose_scenario_member_name_fields(state, frame)\nif target == 422630:\n    from ..high_level_remaining_flows.business_highbank import compose_scenario_member_name_fields_entry_672e6\n    return compose_scenario_member_name_fields_entry_672e6(state, frame)\nif target == 422636:\n    from ..high_level_remaining_flows.business_highbank import restore_scenario_previous_text_fields\n    return restore_scenario_previous_text_fields(state, frame)\nif target == 422646:\n    from ..high_level_remaining_flows.business_highbank import compose_scenario_member_name_fields_entry_672f6\n    return compose_scenario_member_name_fields_entry_672f6(state, frame)\nif target == 422662:\n    from ..high_level_remaining_flows.business_highbank import compose_scenario_status_pair_fields\n    return compose_scenario_status_pair_fields(state, frame)\nif target == 422712:\n    from ..high_level_remaining_flows.business_highbank import compose_scenario_numeric_text_fields_entry_67338\n    return compose_scenario_numeric_text_fields_entry_67338(state, frame)\nif target == 422726:\n    from ..high_level_remaining_flows.business_highbank import compose_scenario_numeric_text_fields_entry_67346\n    return compose_scenario_numeric_text_fields_entry_67346(state, frame)\nif target == 422478:\n    from ..high_level_remaining_flows.business_highbank import restore_scenario_saved_command_fields\n    return restore_scenario_saved_command_fields(state, frame)\nif target == 423198:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_single_row_fields\n    return build_scenario_single_row_fields(state, frame)\nif target == 423438:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_triple_columns_fields\n    return build_scenario_triple_columns_fields(state, frame)\nif target == 423570:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_alternate_row_fields\n    return build_scenario_alternate_row_fields(state, frame)\nif target == 420948:\n    from ..high_level_remaining_flows.business_highbank import confirm_scenario_force_choice_fields\n    return confirm_scenario_force_choice_fields(state, frame)\nif target == 423344:\n    from ..high_level_remaining_flows.business_highbank import build_scenario_paired_columns_fields\n    return build_scenario_paired_columns_fields(state, frame)\nif target == 419076:\n    return sort_high_loyalty_officers_fields(state, frame)\nif target == 419196:\n    return append_mid_loyalty_officers_by_trait_fields(state, frame)\nif target == 422740:\n    return append_scrolling_message_header_fields(state, frame)\nif target == 422796:\n    return append_scrolling_message_glyph_fields(state, frame)\nif target == 422822:\n    return append_scrolling_message_bitmap_fields(state, frame)\nif target == 423018:\n    return lookup_message_layout_words_fields(state, frame)\nif target == 423054:\n    return lookup_message_fill_pattern_fields(state, frame)\nif target == 423178:\n    return lookup_message_decoration_style_fields(state, frame)\nif target == 44804:\n    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\n    from ..high_level_scene_flows.business_scene import expand_glyph_row_fields\n    return expand_glyph_row_fields(SceneRefreshMemory(state), frame)\nif target == 41304:\n    from .business_map import refresh_world_cursor_attributes_alternate_1_frame_fields\n    return refresh_world_cursor_attributes_alternate_1_frame_fields(state, frame)\nif target == 55532:\n    from .business_commands import append_current_command_description_frame_fields\n    return append_current_command_description_frame_fields(state, frame)\nif target == 240466:\n    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory\n    from ..high_level_scene_flows.business_scene import write_vdp_swapped_byte_rle_stream_fields\n    return write_vdp_swapped_byte_rle_stream_fields(SceneRefreshMemory(state), frame)\nif target == 44048:\n    from ..high_level_player_commands.contexts_display import SpritePacketMemory\n    from ..high_level_player_commands.business_display import append_live_command_sprite_fields\n    return append_live_command_sprite_fields(SpritePacketMemory(state), frame, reset_scroll=False, initialize_clip=True)\nraise MovementContinuationBoundary(target, frame, 'actual Highbank child has no admitted full-field return')"}})
