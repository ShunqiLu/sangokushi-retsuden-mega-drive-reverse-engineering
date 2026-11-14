"""Restricted reuse structural source admission and ordinary mnemonic lowering.

Explicit semantic input only; no original ROM/ASM/IR/object input or opaque
opcode payload. Fixed original layout; unsupported source changes are rejected.
Actual service/IRQ and CPU behavior are not supplied by this finite compiler.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import REUSE_BINDINGS

APPROVED = {'contexts_reuse': {'DuelDispositionContext',
                    'DuelSettlementContext',
                    'DuelSettlementResult',
                    'EventSubmission',
                    'ForceHeadMatch',
                    'RadialSeed'},
 'domain': {'Byte',
            'CarryOutcome',
            'Cursor',
            'GameplayState',
            'GroupContext',
            'Long',
            'RandomSample',
            'Table',
            'Word',
            'add16',
            'add32',
            'byte',
            'checked_context',
            'checked_long',
            'checked_state',
            'checked_table',
            'checked_word',
            'clear_low_word',
            'descending_inclusive',
            'divu16',
            'divu_retained',
            'high16',
            'integer',
            'long',
            'low16',
            'low8',
            'low_byte',
            'low_word',
            'mask16',
            'mask32',
            'minimum32',
            'mulu16',
            'negate32',
            'negative_byte',
            'negative_long',
            'negative_word',
            'replace_byte',
            'replace_low_word',
            'replace_word',
            's16',
            'saturating_add32',
            'shl16',
            'shl32',
            'signed_word',
            'stitched_product',
            'sub16',
            'sub32',
            'sub8',
            'subtract_borrow32',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint',
            'unsigned',
            'word'}}

DECLARATIONS = {'scale_e000': {'signature': 'state: GameplayState, offset: Word, factor: Word',
                'returns': 'Long',
                'flow': "return _reuse_scale_field(state, offset, factor, 'e000')"},
 'scale_e0a0': {'signature': 'state: GameplayState, offset: Word, factor: Word',
                'returns': 'Long',
                'flow': "return _reuse_scale_field(state, offset, factor, 'e0a0')"},
 'scale_e140': {'signature': 'state: GameplayState, offset: Word, factor: Word',
                'returns': 'Long',
                'flow': "return _reuse_scale_field(state, offset, factor, 'e140')"},
 'scale_e1e0': {'signature': 'state: GameplayState, offset: Word, factor: Word',
                'returns': 'Long',
                'flow': "return _reuse_scale_field(state, offset, factor, 'e1e0')"},
 'scale_e320': {'signature': 'state: GameplayState, offset: Word, factor: Word',
                'returns': 'Long',
                'flow': "return _reuse_scale_field(state, offset, factor, 'e320')"},
 'scale_e5a0': {'signature': 'state: GameplayState, offset: Word, factor: Word',
                'returns': 'Long',
                'flow': "return _reuse_scale_field(state, offset, factor, 'e5a0')"},
 'adjust_battle_losing_loyalty': {'signature': 'state: GameplayState',
                                  'returns': 'None',
                                  'flow': 'sample = u32(state.sample_random() & 65535)\n'
                                          'decrement = u16(high16(u32(sample * 3)) + 1)\n'
                                          'loyalty = state.loyalty\n'
                                          'if state.outcome() == 5:\n'
                                          '    officer = state.losing_officer()\n'
                                          '    value = u16(loyalty.byte(officer))\n'
                                          '    if value < decrement:\n'
                                          '        value = u16(0)\n'
                                          '    else:\n'
                                          '        value = u16(value - decrement)\n'
                                          '    loyalty.set_byte(officer, low8(value))\n'
                                          'elif state.outcome() == 4:\n'
                                          '    officer = state.winning_officer()\n'
                                          '    value = u16(loyalty.byte(officer))\n'
                                          '    if value < decrement:\n'
                                          '        value = u16(0)\n'
                                          '    else:\n'
                                          '        value = u16(value - decrement)\n'
                                          '    loyalty.set_byte(officer, low8(value))'},
 'allocate_packed_group_resources': {'signature': 'state: GameplayState, packet: Table',
                                     'returns': 'None',
                                     'flow': 'packet = state.checked_table(packet)\n'
                                             'members = u16(packet.byte() - 1)\n'
                                             'total = 0\n'
                                             'for member in descending_inclusive(members):\n'
                                             '    officer = packet.byte(member, 13)\n'
                                             '    index = u16(officer << 2)\n'
                                             '    total = u32(total + '
                                             'state.troop_strengths.long(index))\n'
                                             '    total = u32(total + 100)\n'
                                             'multiplied = u32(u32(total << 1) + total)\n'
                                             'gold_cost = u32(divu_retained(multiplied, 5) & '
                                             '65535)\n'
                                             'rice_cost = gold_cost\n'
                                             'gold = state.city_ed84\n'
                                             'rice = state.city_ee24\n'
                                             'if state.side_flags() & 2 != 0:\n'
                                             '    gold = state.city_gold\n'
                                             '    rice = state.city_rice\n'
                                             'city = u16(state.city() << 2)\n'
                                             'available = gold.long(city)\n'
                                             'if available < gold_cost:\n'
                                             '    gold_cost = available\n'
                                             'gold.set_long(city, u32(available - gold_cost))\n'
                                             'available = rice.long(city)\n'
                                             'if available < rice_cost:\n'
                                             '    rice_cost = available\n'
                                             'rice.set_long(city, u32(available - rice_cost))\n'
                                             'packet.set_byte(8, low8(gold_cost))\n'
                                             'gold_cost = u32(gold_cost >> 8)\n'
                                             'packet.set_byte(7, low8(gold_cost))\n'
                                             'gold_cost = u32(gold_cost >> 8)\n'
                                             'packet.set_byte(6, low8(gold_cost))\n'
                                             'gold_cost = u32(gold_cost & 4294901760 | '
                                             'u16(gold_cost << 8))\n'
                                             'packet.set_byte(5, low8(gold_cost))\n'
                                             'packet.set_byte(12, low8(rice_cost))\n'
                                             'rice_cost = u32(rice_cost >> 8)\n'
                                             'packet.set_byte(11, low8(rice_cost))\n'
                                             'rice_cost = u32(rice_cost >> 8)\n'
                                             'packet.set_byte(10, low8(rice_cost))\n'
                                             'rice_cost = u32(rice_cost & 4294901760 | '
                                             'u16(low16(rice_cost) >> 8))\n'
                                             'packet.set_byte(9, low8(rice_cost))'},
 'append_group_from_survivor_roster': {'signature': 'state: GameplayState',
                                       'returns': 'Table',
                                       'flow': 'packet = state.packed_groups\n'
                                               'assignments = state.city_assignments\n'
                                               'while True:\n'
                                               '    count = u16(packet.byte() & 15)\n'
                                               '    if count == 0:\n'
                                               '        break\n'
                                               '    packet = packet.at(count, 13)\n'
                                               'count = u16(0)\n'
                                               'roster = state.survivor_roster.cursor()\n'
                                               'while True:\n'
                                               '    selected = roster.next_word()\n'
                                               '    if negative_word(selected):\n'
                                               '        break\n'
                                               '    if not selected & 16384:\n'
                                               '        continue\n'
                                               '    packet.set_byte(count, low8(selected), 13)\n'
                                               '    count = u16(count + 1)\n'
                                               '    selected = u16(selected & 255)\n'
                                               '    assignments.set_byte(selected, '
                                               'assignments.byte(selected) | 64)\n'
                                               'packet.set_byte(count, 0, 13)\n'
                                               'packet.set_byte(0, low8(count))\n'
                                               'if state.side_flags() & 2:\n'
                                               '    force = state.secondary_force()\n'
                                               'else:\n'
                                               '    force = state.primary_force()\n'
                                               'packet.set_byte(0, low8(force), 4)\n'
                                               'attributes = state.attributes\n'
                                               'remaining = u16(count - 1)\n'
                                               'total = u32(0)\n'
                                               'attribute = u16(0)\n'
                                               'for member_index in '
                                               'descending_inclusive(remaining):\n'
                                               '    attribute = u16(replace_byte(attribute, '
                                               'packet.byte(member_index, 13)))\n'
                                               '    attribute = u16(replace_byte(attribute, '
                                               'attributes.byte(attribute)))\n'
                                               '    total = u32(total & 4294901760 | '
                                               'u16(low16(total) + attribute))\n'
                                               'total = divu_retained(total, count)\n'
                                               'packet.set_byte(0, low8(total), 3)\n'
                                               'row, column = '
                                               'choose_empty_neighbor_position(state)\n'
                                               'packet.set_byte(0, low8(row), 1)\n'
                                               'packet.set_byte(0, low8(column), 2)\n'
                                               'return packet'},
 'append_queue': {'signature': 'state: GameplayState, city: Word, incoming_owner: Word',
                  'returns': 'Word',
                  'flow': 'city = checked_word(city)\n'
                          'incoming_owner = checked_word(incoming_owner)\n'
                          'owner = replace_byte(incoming_owner, state.owner(city))\n'
                          'if not negative_byte(owner):\n'
                          '    if owner == state.player_owner(0) or owner == state.player_owner(1) '
                          'or owner == state.player_owner(2):\n'
                          '        state.clear_queue_flag()\n'
                          'queue = state.queue()\n'
                          'while queue.read_next() != 255:\n'
                          '    pass\n'
                          'queue.rewind_probe()\n'
                          'queue.write(city)\n'
                          'return owner'},
 'apply_battlefield_heavy_losses_and_detach': {'signature': 'state: GameplayState',
                                               'returns': 'Word',
                                               'flow': 'state = checked_state(state)\n'
                                                       'build_battlefield_outcome_candidates(state)\n'
                                                       'source = state.action_candidates.cursor()\n'
                                                       'points = 0\n'
                                                       'while True:\n'
                                                       '    officer = source.next_word()\n'
                                                       '    if negative_word(officer):\n'
                                                       '        break\n'
                                                       '    troop_offset = u16(officer << 2)\n'
                                                       '    troops = '
                                                       'state.officer_troops.long(troop_offset)\n'
                                                       '    factor = _reuse_random_fraction(state, '
                                                       '40, 50)\n'
                                                       '    loss = divu_retained(u32(factor * '
                                                       'low16(troops)), 100)\n'
                                                       '    '
                                                       'state.officer_troops.set_word(troop_offset, '
                                                       'u16(low16(troops) - low16(loss)), 2)\n'
                                                       '    points = u16(points + '
                                                       'low16(divu_retained(low16(loss), 400)))\n'
                                                       '    readiness_offset = troop_offset >> 1\n'
                                                       '    readiness = '
                                                       'state.officer_readiness.word(readiness_offset)\n'
                                                       '    percent = '
                                                       '_reuse_random_fraction(state, 61)\n'
                                                       '    readiness_loss = '
                                                       'low16(divu_retained(u32(percent * '
                                                       'readiness), 100))\n'
                                                       '    remaining = u16(readiness - '
                                                       'readiness_loss)\n'
                                                       '    '
                                                       'state.officer_readiness.set_word(readiness_offset, '
                                                       'remaining)\n'
                                                       '    if remaining <= 10:\n'
                                                       '        points = u16(points + '
                                                       '_reuse_low_readiness_progress(state, '
                                                       'readiness_offset, False, True))\n'
                                                       "state.set_scalar('outcome_first_points', "
                                                       'points)\n'
                                                       'return points'},
 'apply_battlefield_ratio_losses': {'signature': 'state: GameplayState',
                                    'returns': 'Word',
                                    'flow': 'state = checked_state(state)\n'
                                            'build_battlefield_outcome_candidates(state)\n'
                                            'source = state.action_candidates.cursor()\n'
                                            'points = 0\n'
                                            'while True:\n'
                                            '    officer = source.next_word()\n'
                                            '    if negative_word(officer):\n'
                                            '        break\n'
                                            '    troop_offset = u16(officer << 2)\n'
                                            '    troops = state.officer_troops.long(troop_offset)\n'
                                            '    factor = _reuse_random_fraction(state, 40, 30)\n'
                                            '    scaled_factor = u32(factor * '
                                            "state.scalar('outcome_ratio'))\n"
                                            '    loss = '
                                            'divu_retained(_reuse_multiply_word_parts(scaled_factor, '
                                            'low16(troops)), 1000)\n'
                                            '    remaining = u16(low16(troops) - low16(loss))\n'
                                            '    state.officer_troops.set_word(troop_offset, '
                                            'remaining, 2)\n'
                                            '    points = u16(points + '
                                            'low16(divu_retained(low16(loss), 400)))\n'
                                            '    readiness_offset = troop_offset >> 1\n'
                                            '    readiness = '
                                            'state.officer_readiness.word(readiness_offset)\n'
                                            '    percent = _reuse_random_fraction(state, 30)\n'
                                            '    readiness_loss = low16(divu_retained(u32(percent '
                                            '* readiness), 100))\n'
                                            '    remaining = u16(readiness - readiness_loss)\n'
                                            '    if remaining == 0:\n'
                                            '        remaining = 1\n'
                                            '    '
                                            'state.officer_readiness.set_word(readiness_offset, '
                                            'remaining)\n'
                                            "state.set_scalar('outcome_first_points', points)\n"
                                            'return points'},
 'apply_city_assigned_heavy_losses': {'signature': 'state: GameplayState',
                                      'returns': 'Word',
                                      'flow': 'state = checked_state(state)\n'
                                              'build_city_assigned_outcome_candidates(state)\n'
                                              'source = state.action_candidates.cursor()\n'
                                              'points = 0\n'
                                              'while True:\n'
                                              '    officer = source.next_word()\n'
                                              '    if negative_word(officer):\n'
                                              '        break\n'
                                              '    troop_offset = u16(officer << 2)\n'
                                              '    troops = '
                                              'state.officer_troops.long(troop_offset)\n'
                                              '    factor = _reuse_random_fraction(state, 40, 50)\n'
                                              '    loss = divu_retained(u32(factor * '
                                              'low16(troops)), 100)\n'
                                              '    state.officer_troops.set_word(troop_offset, '
                                              'u16(low16(troops) - low16(loss)), 2)\n'
                                              '    points = u16(points + '
                                              'low16(divu_retained(low16(loss), 400)))\n'
                                              '    readiness_offset = troop_offset >> 1\n'
                                              '    readiness = '
                                              'state.officer_readiness.word(readiness_offset)\n'
                                              '    percent = _reuse_random_fraction(state, 60)\n'
                                              '    readiness_loss = '
                                              'low16(divu_retained(u32(percent * readiness), '
                                              '100))\n'
                                              '    remaining = u16(readiness - readiness_loss)\n'
                                              '    '
                                              'state.officer_readiness.set_word(readiness_offset, '
                                              'remaining)\n'
                                              '    if remaining <= 10:\n'
                                              '        points = u16(points + '
                                              '_reuse_low_readiness_progress(state, '
                                              'readiness_offset, True, False))\n'
                                              "state.set_scalar('outcome_second_points', points)\n"
                                              'return points'},
 'apply_duel_disposition': {'signature': 'state: GameplayState, context: DuelDispositionContext',
                            'returns': 'None',
                            'flow': 'state = checked_state(state)\n'
                                    'context = _reuse_checked_context(context, '
                                    'DuelDispositionContext)\n'
                                    'officer, disposition = (context.officer, '
                                    'context.disposition)\n'
                                    "if state.scalar('battle_active') == 0:\n"
                                    '    if disposition != 3:\n'
                                    '        result = 6 if officer == '
                                    "state.scalar('duel_primary_officer') else 7\n"
                                    "        state.set_scalar('duel_result', result)\n"
                                    '    return\n'
                                    'if disposition == 3:\n'
                                    "    scene_flags = state.scalar('battle_scene') | 128\n"
                                    "    if officer == state.scalar('roster_side_owner'):\n"
                                    '        retired = '
                                    'state.battle_primary_retired_roster.cursor()\n'
                                    '        active = state.battle_primary_roster.cursor()\n'
                                    '    else:\n'
                                    '        scene_flags |= 64\n'
                                    '        retired = '
                                    'state.battle_secondary_retired_roster.cursor()\n'
                                    '        active = state.battle_secondary_roster.cursor()\n'
                                    '    _reuse_append_at_roster_end(retired, officer)\n'
                                    '    _reuse_seek_officer_unbounded(active, officer)\n'
                                    '    _reuse_compact_live_roster(active)\n'
                                    'elif disposition == 2:\n'
                                    "    if officer == state.scalar('roster_side_owner'):\n"
                                    '        active = state.battle_primary_roster.cursor()\n'
                                    '        retired = '
                                    'state.battle_primary_retired_roster.cursor()\n'
                                    '    else:\n'
                                    '        active = state.battle_secondary_roster.cursor()\n'
                                    '        retired = '
                                    'state.battle_secondary_retired_roster.cursor()\n'
                                    '    _reuse_seek_officer_unbounded(active, officer)\n'
                                    '    _reuse_compact_live_roster(active)\n'
                                    '    _reuse_append_at_roster_end(retired, officer)'},
 'apply_returning_officer_loyalty': {'signature': 'state: GameplayState',
                                     'returns': 'None',
                                     'flow': 'sample = u32(state.sample_random() & 65535)\n'
                                             'factor = u16(high16(u32(sample * 5)) + 6)\n'
                                             'status = state.status\n'
                                             'value = u16(104)\n'
                                             'officer = u16(state.selected_officer() & 255)\n'
                                             'value = u16(replace_byte(value, low8(value - '
                                             'status.byte(officer))))\n'
                                             'value = u16(value >> 1)\n'
                                             'affinity = state.affinity\n'
                                             'source = u16(state.loyalty_source() & 255)\n'
                                             'influence = u16(affinity.byte(source))\n'
                                             'value = u32(low16(value) * low16(influence))\n'
                                             'value = u32(low16(value) * low16(factor))\n'
                                             'value = divu_retained(value, 500)\n'
                                             'if low16(value) > 100:\n'
                                             '    value = u32(value & 4294901760 | 100)\n'
                                             'status.set_byte(officer, low8(value))'},
 'attach_member_shift_packet': {'signature': 'state: GameplayState, officer: Word, context: '
                                             'GroupContext',
                                'returns': 'GroupContext',
                                'flow': 'officer = u16(officer)\n'
                                        'context = checked_context(context, state)\n'
                                        'target = context.target\n'
                                        'count = target.byte() & 15\n'
                                        'if count == 10:\n'
                                        '    added_bytes = 0\n'
                                        '    assignment = state.officer_assignments.byte(officer) '
                                        '& 63\n'
                                        '    if assignment <= 40:\n'
                                        '        assignment = u16(assignment | 128)\n'
                                        '        state.officer_assignments.set_byte(assignment, '
                                        'low8(assignment))\n'
                                        '    else:\n'
                                        '        assignment = u16(assignment - 40)\n'
                                        '        assignment = u16(assignment | 128)\n'
                                        '        state.officer_assignments.set_byte(officer, '
                                        'low8(assignment))\n'
                                        'else:\n'
                                        '    tail = target.at(count, 13)\n'
                                        '    destination = target.at(count, 14).cursor()\n'
                                        '    carried = tail.byte()\n'
                                        '    while True:\n'
                                        '        following_count = carried & 15\n'
                                        '        if following_count == 0:\n'
                                        '            destination.set_byte(0, 0)\n'
                                        '            break\n'
                                        '        for copied in '
                                        'descending_inclusive(u16(following_count + 12)):\n'
                                        '            displaced = destination.byte()\n'
                                        '            destination.append_byte(carried)\n'
                                        '            carried = displaced\n'
                                        '    count = target.byte() & 15\n'
                                        '    target.set_byte(0, u8(target.byte() + 1))\n'
                                        '    target.set_byte(count, low8(officer), 13)\n'
                                        '    assignment = u16(target.byte(4) + 41)\n'
                                        '    state.officer_assignments.set_byte(officer, '
                                        'low8(assignment))\n'
                                        '    added_bytes = 1\n'
                                        'source = context.source\n'
                                        'if source.address() >= target.address():\n'
                                        '    source = source.advance(added_bytes)\n'
                                        'return GroupContext(source, target)'},
 'build_battlefield_outcome_candidates': {'signature': 'state: GameplayState',
                                          'returns': 'Word',
                                          'flow': 'checked_state(state)\n'
                                                  'destination = state.action_candidates.cursor()\n'
                                                  "city = state.scalar('battle_scene')\n"
                                                  'count = 0\n'
                                                  'for officer in descending_inclusive(255):\n'
                                                  '    if '
                                                  'state.battlefield_city_assignment.byte(officer) '
                                                  '== low8(city):\n'
                                                  '        if not '
                                                  'negative_byte(state.officer_city_assignment.byte(officer)):\n'
                                                  '            destination.append_word(officer)\n'
                                                  '            count = u16(count + 1)\n'
                                                  'destination.put_word(65535)\n'
                                                  'return count'},
 'build_city_assigned_outcome_candidates': {'signature': 'state: GameplayState',
                                            'returns': 'Word',
                                            'flow': 'checked_state(state)\n'
                                                    'destination = '
                                                    'state.action_candidates.cursor()\n'
                                                    "city = state.scalar('battle_scene')\n"
                                                    'count = 0\n'
                                                    'for officer in descending_inclusive(255):\n'
                                                    '    if '
                                                    'state.officer_city_assignment.byte(officer) '
                                                    '== low8(city):\n'
                                                    '        destination.append_word(officer)\n'
                                                    '        count = u16(count + 1)\n'
                                                    'destination.put_word(65535)\n'
                                                    'return count'},
 'build_roster': {'signature': 'state: GameplayState, city: Word',
                  'returns': 'Word',
                  'flow': 'checked_state(state)\n'
                          'uint(city, 16)\n'
                          'assignments = state.officer_city_assignment.cursor()\n'
                          'destination = state.candidate_roster.cursor()\n'
                          'count = 0\n'
                          "head = state.scalar('preferred_head')\n"
                          'if not negative_word(head):\n'
                          '    destination.append_word(head)\n'
                          '    count = u16(count + 1)\n'
                          'for officer in range(256):\n'
                          '    assigned = assignments.next_byte()\n'
                          '    if assigned == low8(city) and officer != '
                          "state.scalar('preferred_head'):\n"
                          '        destination.append_word(officer)\n'
                          '        count = u16(count + 1)\n'
                          'destination.put_word(65535)\n'
                          'return count'},
 'choose_city_head': {'signature': 'state: GameplayState, city: Word',
                      'returns': 'Word',
                      'flow': 'checked_state(state)\n'
                              'uint(city, 16)\n'
                              'source = state.candidate_roster.cursor()\n'
                              'head = source.next_word()\n'
                              'if negative_word(head):\n'
                              '    state.city_owner_bytes.set_byte(city, 255)\n'
                              '    offset = u16(u16(u16(city << 1) + city) << 2)\n'
                              '    state.city_orders.set_word(offset, 65535)\n'
                              '    state.city_orders.set_word(offset, 65535, 4)\n'
                              '    state.city_orders.set_word(offset, 65535, 8)\n'
                              'else:\n'
                              '    match = roster_contains_force_head_carry(state, city, head)\n'
                              '    head = match.head\n'
                              '    if match.carry == 0:\n'
                              '        head = low8(head)\n'
                              '        highest = state.officer_status_rating.byte(head)\n'
                              '        while True:\n'
                              '            candidate = source.next_word()\n'
                              '            if negative_word(candidate):\n'
                              '                break\n'
                              '            candidate = low8(candidate)\n'
                              '            rating = state.officer_status_rating.byte(candidate)\n'
                              '            if rating > highest:\n'
                              '                head, highest = (candidate, rating)\n'
                              'state.city_head_words.set_word(u16(city << 1), head)\n'
                              'return head'},
 'choose_empty_neighbor_position': {'signature': 'state: GameplayState',
                                    'returns': 'tuple[Word, Word]',
                                    'flow': 'neighbors = state.neighbor_offsets\n'
                                            'costs = state.terrain_cost\n'
                                            'terrain = state.terrain_cells\n'
                                            'selected = u16(state.city() << 2)\n'
                                            'coordinates = state.city_coordinates\n'
                                            'center_row = u16(coordinates.word(selected, 2) >> 4)\n'
                                            'center_column = u16(coordinates.word(selected) >> 4)\n'
                                            'while True:\n'
                                            '    row = u16(center_row + neighbors.word())\n'
                                            '    if row >= 72:\n'
                                            '        neighbors = neighbors.advance(4)\n'
                                            '        continue\n'
                                            '    column = u16(center_column + neighbors.word(0, '
                                            '2))\n'
                                            '    if column >= 72:\n'
                                            '        neighbors = neighbors.advance(4)\n'
                                            '        continue\n'
                                            '    cell = u16(row << 3)\n'
                                            '    cell = u16(cell + row)\n'
                                            '    cell = u16(cell << 3)\n'
                                            '    cell = u16(cell + column)\n'
                                            '    kind = u16(terrain.byte(cell))\n'
                                            '    if negative_byte(costs.byte(kind)):\n'
                                            '        neighbors = neighbors.advance(4)\n'
                                            '        continue\n'
                                            '    groups = state.packed_groups\n'
                                            '    while True:\n'
                                            '        count = u16(groups.byte() & 15)\n'
                                            '        if count == 0:\n'
                                            '            return (row, column)\n'
                                            '        if low8(row) == groups.byte(0, 1):\n'
                                            '            if low8(column) == groups.byte(0, 2):\n'
                                            '                break\n'
                                            '        groups = groups.at(count, 13)\n'
                                            '    neighbors = neighbors.advance(4)'},
 'commit_income': {'signature': 'state: GameplayState, city: Word, offset: Word, factor: Word, '
                                'ledger: Table',
                   'returns': None,
                   'flow': 'gain: Long = scaled_income(state, offset, factor)\n'
                           'gain = saturating_add32(gain, ledger.long(offset))\n'
                           'ledger.set_long(offset, gain)\n'
                           'deplete_income(state, city, state.depletion_modifiers)'},
 'compute_outcome_force_ratio': {'signature': 'state: GameplayState',
                                 'returns': 'Word',
                                 'flow': 'state = checked_state(state)\n'
                                         'random_factor = _reuse_random_fraction(state, 6, 10)\n'
                                         'build_city_assigned_outcome_candidates(state)\n'
                                         'troops, first_attribute, second_attribute = '
                                         '_reuse_candidate_strength_totals(state)\n'
                                         'troops = replace_word(troops, u16(low16(troops) + 1)) >> '
                                         '5\n'
                                         'first_factor = u16((first_attribute >> 3) + 1)\n'
                                         'second_factor = u16((second_attribute >> 3) + 1)\n'
                                         'numerator = _reuse_multiply_word_parts(troops, '
                                         'first_factor)\n'
                                         'numerator = _reuse_multiply_word_parts(numerator, '
                                         'second_factor)\n'
                                         'numerator = _reuse_multiply_word_parts(numerator, '
                                         'random_factor)\n'
                                         'build_battlefield_outcome_candidates(state)\n'
                                         'troops, first_attribute, second_attribute = '
                                         '_reuse_candidate_strength_totals(state)\n'
                                         'troops >>= 5\n'
                                         'troops = replace_word(troops, u16(low16(troops) + 1))\n'
                                         'first_factor = u16((first_attribute >> 3) + 1)\n'
                                         'second_factor = u16((second_attribute >> 3) + 1)\n'
                                         'denominator = _reuse_multiply_word_parts(troops, '
                                         'first_factor)\n'
                                         'denominator = _reuse_multiply_word_parts(denominator, '
                                         'first_factor)\n'
                                         'quotient, remainder = signed_divmod(state, numerator, '
                                         'denominator)\n'
                                         'ratio = low16(quotient)\n'
                                         "state.set_scalar('outcome_ratio', ratio)\n"
                                         'return ratio'},
 'consume_city_battle_resources': {'signature': 'state: GameplayState',
                                   'returns': 'None',
                                   'flow': 'state = checked_state(state)\n'
                                           "city = state.scalar('battle_scene')\n"
                                           'total = _reuse_assigned_troop_total(state, '
                                           'state.battlefield_city_assignment, city)\n'
                                           'factor = _reuse_random_fraction(state, 11, 10)\n'
                                           'consumed = '
                                           'divu_retained(_reuse_multiply_word_parts(total, '
                                           'factor), 500)\n'
                                           "city_offset = u16(state.scalar('battle_scene') << 2)\n"
                                           'resource = '
                                           'state.city_battle_resource.long(city_offset)\n'
                                           'consumed = low16(consumed)\n'
                                           'remaining = 0 if resource < consumed else u32(resource '
                                           '- consumed)\n'
                                           'state.city_battle_resource.set_long(city_offset, '
                                           'remaining)\n'
                                           "city = state.scalar('battle_scene')\n"
                                           'total = _reuse_assigned_troop_total(state, '
                                           'state.officer_city_assignment, city)\n'
                                           'factor = _reuse_random_fraction(state, 11, 10)\n'
                                           'consumed = '
                                           'low16(divu_retained(_reuse_multiply_word_parts(total, '
                                           'factor), 500))\n'
                                           "city_offset = u16(state.scalar('battle_scene') << 2)\n"
                                           'food = state.city_food.long(city_offset)\n'
                                           'remaining = 0 if food < consumed else u32(food - '
                                           'consumed)\n'
                                           'state.city_food.set_long(city_offset, remaining)'},
 'credit_packed_group_resources': {'signature': 'state: GameplayState, packet: Table, city: Word',
                                   'returns': 'None',
                                   'flow': 'city = u16(city)\n'
                                           'packet = state.checked_table(packet)\n'
                                           'city = u16(city << 2)\n'
                                           'amount = u32(packet.byte(0, 5) << 24)\n'
                                           'amount = u32(amount | packet.byte(0, 6) << 16)\n'
                                           'amount = u32(amount | packet.byte(0, 7) << 8)\n'
                                           'amount = u32(amount | packet.byte(0, 8))\n'
                                           'gold = state.city_gold\n'
                                           'balance = u32(gold.long(city) + amount)\n'
                                           'if balance > 999999:\n'
                                           '    balance = u32(999999)\n'
                                           'gold.set_long(city, balance)\n'
                                           'amount = u32(packet.byte(0, 9) << 24)\n'
                                           'amount = u32(amount | packet.byte(0, 10) << 16)\n'
                                           'amount = u32(amount | packet.byte(0, 11) << 8)\n'
                                           'amount = u32(amount | packet.byte(0, 12))\n'
                                           'rice = state.city_rice\n'
                                           'balance = u32(rice.long(city) + amount)\n'
                                           'if balance > 999999:\n'
                                           '    balance = u32(999999)\n'
                                           'rice.set_long(city, balance)'},
 'credit_primary': {'signature': 'state: GameplayState, city: Word',
                    'returns': None,
                    'flow': 'modifiers: Table = state.city_modifiers\n'
                            'offset: Word = shl16(city, 2)\n'
                            'factor: Word = sub16(word(100), modifiers.word(offset, 2))\n'
                            'ledger: Table = state.primary_ledger\n'
                            'commit_income(state, city, offset, factor, ledger)'},
 'credit_secondary': {'signature': 'state: GameplayState, city: Word',
                      'returns': None,
                      'flow': 'modifiers: Table = state.city_modifiers\n'
                              'offset: Word = shl16(city, 2)\n'
                              'factor: Long = modifiers.long(offset)\n'
                              'ledger: Table = state.secondary_ledger\n'
                              'commit_income(state, city, offset, low_word(factor), ledger)'},
 'debit_primary': {'signature': 'state: GameplayState, city: Word',
                   'returns': None,
                   'flow': 'modifiers: Table = state.city_modifiers\n'
                           'factor: Word = word(100)\n'
                           'offset: Word = shl16(city, 2)\n'
                           'factor = sub16(factor, modifiers.word(offset, 2))\n'
                           'ledger: Table = state.primary_ledger\n'
                           'settle_expense(state, city, factor, ledger)'},
 'debit_secondary': {'signature': 'state: GameplayState, city: Word',
                     'returns': None,
                     'flow': 'modifiers: Table = state.city_modifiers\n'
                             'offset: Word = shl16(city, 2)\n'
                             'factor: Word = modifiers.word(offset, 2)\n'
                             'ledger: Table = state.secondary_ledger\n'
                             'settle_expense(state, city, factor, ledger)'},
 'deplete_income': {'signature': 'state: GameplayState, city: Word, thresholds: Table',
                    'returns': None,
                    'flow': 'offset: Word = shl16(city, 2)\n'
                            'threshold: Long = thresholds.long(offset)\n'
                            'tier: Word = word(0)\n'
                            'if low_word(threshold) <= 45:\n'
                            '    return\n'
                            'if low_word(threshold) > 55:\n'
                            '    tier = add16(tier, 4)\n'
                            '    if low_word(threshold) > 65:\n'
                            '        tier = add16(tier, 4)\n'
                            '        if low_word(threshold) > 75:\n'
                            '            tier = add16(tier, 4)\n'
                            '            if low_word(threshold) > 85:\n'
                            '                tier = add16(tier, 4)\n'
                            'saved_city: Word = city\n'
                            'step_random(state)\n'
                            'city = saved_city\n'
                            'parameters: Table = state.depletion_parameters\n'
                            'reduction_factor: Word = parameters.word(tier)\n'
                            'reduction_factor = mulu16(reduction_factor, state.seed_high())\n'
                            'reduction_factor = swap_words(reduction_factor)\n'
                            'reduction_factor = add16(reduction_factor, parameters.word(tier, 2))\n'
                            'reserve: Table = state.depletion_reserve\n'
                            'offset = shl16(city, 2)\n'
                            'loss: Word = reserve.word(offset, 2)\n'
                            'loss = mulu16(loss, reduction_factor)\n'
                            'loss = divu16(loss, 100)\n'
                            'reserve.subtract_word(offset, loss, 2)'},
 'detach_defeated_duelist': {'signature': 'state: GameplayState, officer: Word',
                             'returns': 'None',
                             'flow': 'checked_state(state)\n'
                                     'uint(officer, 16)\n'
                                     'state.officer_city_assignment.set_byte(officer, 255)\n'
                                     'source = _reuse_active_duel_roster(state, officer)\n'
                                     'while low8(source.next_word()) != officer:\n'
                                     '    pass\n'
                                     '_reuse_compact_after_match(source)'},
 'detach_member_keep_group_cursor': {'signature': 'state: GameplayState, officer: Word, context: '
                                                  'GroupContext',
                                     'returns': 'GroupContext',
                                     'flow': 'officer = u16(officer)\n'
                                             'context = checked_context(context, state)\n'
                                             'group = context.source\n'
                                             'count = group.byte() & 15\n'
                                             'if count == 1:\n'
                                             '    removed_bytes = 14\n'
                                             '    remove_group_reference(state, officer)\n'
                                             '    tail = group.at(count, 13).cursor()\n'
                                             '    destination = group.cursor()\n'
                                             'else:\n'
                                             '    removed_bytes = 1\n'
                                             '    index = 0\n'
                                             '    while group.byte(index, 13) != low8(officer):\n'
                                             '        index = u16(index + 1)\n'
                                             '    index = u16(index + 1)\n'
                                             '    while index != count:\n'
                                             '        group.set_byte(index, group.byte(index, 13), '
                                             '12)\n'
                                             '        index = u16(index + 1)\n'
                                             '    replace_group_head_reference(state, officer, '
                                             'group)\n'
                                             '    group.set_byte(0, u8(group.byte() - 1))\n'
                                             '    tail = group.at(count, 13).cursor()\n'
                                             '    destination = group.at(count, 12).cursor()\n'
                                             'while True:\n'
                                             '    following_count = tail.byte() & 15\n'
                                             '    if following_count == 0:\n'
                                             '        destination.set_byte(0, 0)\n'
                                             '        break\n'
                                             '    for copied in '
                                             'descending_inclusive(u16(following_count + 12)):\n'
                                             '        destination.append_byte(tail.next_byte())\n'
                                             'other = context.target\n'
                                             'if other.address() >= group.address():\n'
                                             '    other = other.advance(-removed_bytes)\n'
                                             'return GroupContext(group, other)'},
 'detach_zero_readiness_duelists': {'signature': 'state: GameplayState',
                                    'returns': 'None',
                                    'flow': 'state = checked_state(state)\n'
                                            "if state.scalar('battle_active') == 0:\n"
                                            '    return\n'
                                            'if state.duel_packet_first.word(28) == 0:\n'
                                            '    detach_defeated_duelist(state, '
                                            'state.duel_packet_first.word(26))\n'
                                            'if state.duel_packet_second.word(28) == 0:\n'
                                            '    detach_defeated_duelist(state, '
                                            'state.duel_packet_second.word(26))'},
 'divide_percent': {'signature': 'state: GameplayState, product: Long',
                    'returns': 'Long',
                    'flow': 'product = checked_long(product)\n'
                            'quotient, remainder = signed_divmod(state, product, 100)\n'
                            'return quotient'},
 'erase_group_packet': {'signature': 'state: GameplayState, packet: Table',
                        'returns': 'Table',
                        'flow': 'packet = state.checked_table(packet)\n'
                                'count = u16(packet.byte() & 15)\n'
                                'following = packet.at(count, 13)\n'
                                'count = u16(following.byte() & 15)\n'
                                'if count != 0:\n'
                                '    count = u16(count + 12)\n'
                                '    source = following.cursor()\n'
                                '    destination = packet.cursor()\n'
                                '    for remaining in descending_inclusive(count):\n'
                                '        destination.append_byte(source.next_byte())\n'
                                '    packet = state.table(destination.address())\n'
                                'packet.set_byte(0, 0)\n'
                                'return packet'},
 'find_group_at_coordinate': {'signature': 'state: GameplayState, coordinate: Word',
                              'returns': 'Table',
                              'flow': 'state = checked_state(state)\n'
                                      'coordinate = uint(coordinate, 16)\n'
                                      'x = coordinate >> 8\n'
                                      'y = low8(coordinate)\n'
                                      'group = state.group_packets\n'
                                      'while True:\n'
                                      '    members = group.byte() & 15\n'
                                      '    if members == 0:\n'
                                      '        return group\n'
                                      '    if group.byte(0, 1) == x:\n'
                                      '        if group.byte(0, 2) == y:\n'
                                      '            return group\n'
                                      '    group = group.advance(13 + members)'},
 'grant_duel_fallback_progress': {'signature': 'state: GameplayState, receiver_offset: Word, '
                                               'donor: Word, progress: Table',
                                  'returns': 'Long',
                                  'flow': 'checked_state(state)\n'
                                          'uint(receiver_offset, 16)\n'
                                          'uint(donor, 16)\n'
                                          'checked_table(progress, state)\n'
                                          'donor_offset = u16(donor << 1)\n'
                                          'raw = progress.word(donor_offset)\n'
                                          'gain = divu_retained(u32(s16(raw)), 40)\n'
                                          'donor = donor_offset >> 1\n'
                                          "scene_offset = u16(state.scalar('battle_scene') << 1)\n"
                                          'if donor == state.city_head_words.word(scene_offset):\n'
                                          '    gain = replace_word(gain, u16(low16(gain) + 30))\n'
                                          'elif donor == '
                                          'state.alternate_heads.word(scene_offset):\n'
                                          '    gain = replace_word(gain, u16(low16(gain) + 30))\n'
                                          'if state.officer_status.byte(donor) & 16:\n'
                                          '    gain = replace_word(gain, u16(low16(gain) + 20))\n'
                                          'updated = u16(progress.word(receiver_offset) + '
                                          'low16(gain))\n'
                                          'if updated > 999:\n'
                                          '    updated = 999\n'
                                          'progress.set_word(receiver_offset, updated)\n'
                                          'return gain'},
 'grant_duel_troop_difference_progress': {'signature': 'state: GameplayState, receiver: Word, '
                                                       'troop_difference: Long, progress: Table',
                                          'returns': 'Long',
                                          'flow': 'checked_state(state)\n'
                                                  'uint(receiver, 16)\n'
                                                  'uint(troop_difference, 32)\n'
                                                  'checked_table(progress, state)\n'
                                                  'gain = divu_retained(low16(troop_difference), '
                                                  '100)\n'
                                                  'offset = u16(receiver << 1)\n'
                                                  'updated = u16(progress.word(offset) + '
                                                  'low16(gain))\n'
                                                  'if updated > 999:\n'
                                                  '    updated = 999\n'
                                                  'progress.set_word(offset, updated)\n'
                                                  'return gain'},
 'grow_original_long_field': {'signature': 'state: GameplayState, target: Table',
                              'returns': 'Long',
                              'flow': 'previous = target.long()\n'
                                      'divided = divu_retained(previous, 100)\n'
                                      'updated = u32(previous + low16(divided))\n'
                                      'if updated > 1000:\n'
                                      '    updated = 1000\n'
                                      'target.set_long(0, updated)\n'
                                      'return updated'},
 'initialize_prebattle_head_bytes': {'signature': 'state: GameplayState',
                                     'returns': 'None',
                                     'flow': 'heads = state.force_heads.cursor()\n'
                                             'statuses = state.officer_status\n'
                                             'for slot in descending_inclusive(u16(15)):\n'
                                             '    head = heads.next_word()\n'
                                             '    if negative_word(head):\n'
                                             '        continue\n'
                                             '    statuses.set_byte(head, 100)'},
 'load_battlefield_map_context': {'signature': 'state: GameplayState',
                                  'returns': 'Table',
                                  'flow': 'checked_state(state)\n'
                                          "scene = state.scalar('battle_scene')\n"
                                          'return state.battlefield_maps.advance(scene * 2240)'},
 'locate_group_city': {'signature': 'state: GameplayState, packet: Table',
                       'returns': 'Word',
                       'flow': 'packet = state.checked_table(packet)\n'
                               'row_pixel = u16(packet.byte(0, 1) << 4)\n'
                               'row_pixel = u16(row_pixel + 8)\n'
                               'column_pixel = u16(packet.byte(0, 2) << 4)\n'
                               'previous_column_pixel = u16(column_pixel - 16)\n'
                               'coordinates = state.arrival_coordinates\n'
                               'city = u16(1)\n'
                               'while True:\n'
                               '    if row_pixel == coordinates.word(0, 2):\n'
                               '        if column_pixel == coordinates.word():\n'
                               '            return city\n'
                               '        if previous_column_pixel == coordinates.word(0, 2):\n'
                               '            return city\n'
                               '    coordinates = coordinates.advance(4)\n'
                               '    city = u16(city + 1)'},
 'owner_has_other_city_carry': {'signature': 'state: GameplayState',
                                'returns': 'CarryOutcome',
                                'flow': 'city = u16(state.city() - 1)\n'
                                        'owner = state.working_owner()\n'
                                        'for candidate in descending_inclusive(39):\n'
                                        '    if state.other_city_owners.byte(candidate) == owner:\n'
                                        '        if candidate != city:\n'
                                        '            return state.carry_result(0)\n'
                                        'return state.carry_result(1)'},
 'partition_city_survivors': {'signature': 'state: GameplayState',
                              'returns': 'None',
                              'flow': 'first = state.battle_candidate_roster.word()\n'
                                      'city = u16(state.officer_assignments.byte(first) & 63)\n'
                                      'owner = state.city_owners.byte(city)\n'
                                      'state.set_working_owner(owner)\n'
                                      'ruler = state.force_heads.word(u16(owner << 1))\n'
                                      'roster = state.battle_candidate_roster.cursor()\n'
                                      'remaining = state.remaining_roster.cursor()\n'
                                      'returning = state.survivor_roster.cursor()\n'
                                      'return_count = 0\n'
                                      'keep_count = 0\n'
                                      'while True:\n'
                                      '    officer = roster.next_word()\n'
                                      '    if negative_word(officer):\n'
                                      '        break\n'
                                      '    if officer == ruler:\n'
                                      '        outcome = owner_has_other_city_carry(state)\n'
                                      '        if outcome.carry == 0:\n'
                                      '            returning.append_word(officer)\n'
                                      '            return_count = u16(return_count + 1)\n'
                                      '        else:\n'
                                      '            state.officer_assignments.set_byte(officer, '
                                      '255)\n'
                                      '        continue\n'
                                      '    strength_index = u16(officer << 2)\n'
                                      '    if state.troop_strengths.long(strength_index) > 500:\n'
                                      '        if state.troop_strengths.long(strength_index) > '
                                      '1000:\n'
                                      '            remaining.append_word(officer)\n'
                                      '            keep_count = u16(keep_count + 1)\n'
                                      '            continue\n'
                                      '        resource_index = u16(strength_index >> 1)\n'
                                      '        if state.officer_resources.word(resource_index) > '
                                      '30:\n'
                                      '            remaining.append_word(officer)\n'
                                      '            keep_count = u16(keep_count + 1)\n'
                                      '            continue\n'
                                      '    sample = u16(state.sample_random() & 3)\n'
                                      '    if sample == 0:\n'
                                      '        returning.append_word(officer)\n'
                                      '        return_count = u16(return_count + 1)\n'
                                      '    else:\n'
                                      '        remaining.append_word(officer)\n'
                                      '        keep_count = u16(keep_count + 1)\n'
                                      'remaining.set_word(0, 65535)\n'
                                      'returning.set_word(0, 65535)\n'
                                      'state.set_returning_count(return_count)\n'
                                      'state.set_remaining_count(keep_count)'},
 'positive_denominator': {'signature': 'state: GameplayState, numerator: Long, denominator: Long',
                          'returns': 'tuple[Long, Long]',
                          'flow': 'checked_state(state)\n'
                                  'uint(numerator, 32)\n'
                                  'uint(denominator, 32)\n'
                                  'if negative_long(numerator):\n'
                                  '    quotient, remainder = unsigned_divmod(state, '
                                  'u32(-numerator), denominator)\n'
                                  '    return (u32(-quotient), u32(-remainder))\n'
                                  'return unsigned_divmod(state, numerator, denominator)'},
 'read_battlefield_terrain_type': {'signature': 'state: GameplayState, map_context: Table, x: '
                                                'Word, y: Word, retained: Long=0',
                                   'returns': 'Long',
                                   'flow': 'checked_state(state)\n'
                                           'checked_table(map_context, state)\n'
                                           'uint(x, 16)\n'
                                           'uint(y, 16)\n'
                                           'uint(retained, 32)\n'
                                           'offset = u16(((x >> 3) * 40 + (y >> 3)) * 2)\n'
                                           'tile = map_context.word(offset) & 1023\n'
                                           'carrier = replace_word(retained, tile)\n'
                                           'return replace_byte(carrier, '
                                           'state.terrain_category_lookup.byte(tile))'},
 'rebuild_primary_after_battle': {'signature': 'state: GameplayState',
                                  'returns': 'None',
                                  'flow': '_reuse_collect_city_attached_officers(state)\n'
                                          'partition_city_survivors(state)\n'
                                          'incoming = '
                                          '_reuse_collect_unassigned_city_officers(state)\n'
                                          'total = u16(incoming + state.remaining_count())\n'
                                          'if total > 10:\n'
                                          '    sort_returning_officer_status(state, u16(total - '
                                          '10))\n'
                                          'roster = state.survivor_roster.cursor()\n'
                                          'while True:\n'
                                          '    officer = roster.word()\n'
                                          '    if negative_word(officer):\n'
                                          '        break\n'
                                          '    roster.append_word(u16(officer | 16384))\n'
                                          'if not negative_word(state.survivor_roster.word()):\n'
                                          '    '
                                          'state.set_working_owner(state.secondary_owner_byte())\n'
                                          '    outcome = owner_has_other_city_carry(state)\n'
                                          '    if outcome.carry == 0:\n'
                                          '        state.set_resource_side(2)\n'
                                          '        packet = '
                                          'append_group_from_survivor_roster(state)\n'
                                          '        allocate_packed_group_resources(state, packet)\n'
                                          '    else:\n'
                                          '        city = u16(state.city() | 128)\n'
                                          '        roster = state.survivor_roster.cursor()\n'
                                          '        while True:\n'
                                          '            officer = roster.next_word()\n'
                                          '            if negative_word(officer):\n'
                                          '                break\n'
                                          '            officer = u16(officer & 255)\n'
                                          '            state.officer_assignments.set_byte(officer, '
                                          'low8(city))\n'
                                          'force = u16(state.primary_force() << 1)\n'
                                          'state.set_loyalty_source(state.force_heads.word(force))\n'
                                          'restore_returning_officer_assignments(state)'},
 'rebuild_secondary_after_battle': {'signature': 'state: GameplayState',
                                    'returns': 'None',
                                    'flow': '_reuse_collect_unassigned_city_officers(state)\n'
                                            'partition_city_survivors(state)\n'
                                            'incoming = '
                                            '_reuse_collect_city_attached_officers(state)\n'
                                            'total = u16(incoming + state.remaining_count())\n'
                                            'if total > 10:\n'
                                            '    sort_returning_officer_status(state, u16(total - '
                                            '10))\n'
                                            'roster = state.survivor_roster.cursor()\n'
                                            'while True:\n'
                                            '    officer = roster.word()\n'
                                            '    if negative_word(officer):\n'
                                            '        break\n'
                                            '    roster.append_word(u16(officer | 16384))\n'
                                            'if not negative_word(state.survivor_roster.word()):\n'
                                            '    '
                                            'state.set_working_owner(state.primary_owner_byte())\n'
                                            '    outcome = owner_has_other_city_carry(state)\n'
                                            '    if outcome.carry == 0:\n'
                                            '        state.set_resource_side(0)\n'
                                            '        packet = '
                                            'append_group_from_survivor_roster(state)\n'
                                            '        allocate_packed_group_resources(state, '
                                            'packet)\n'
                                            '    else:\n'
                                            '        city = u16(state.city() | 128)\n'
                                            '        roster = state.survivor_roster.cursor()\n'
                                            '        while True:\n'
                                            '            officer = roster.next_word()\n'
                                            '            if negative_word(officer):\n'
                                            '                break\n'
                                            '            officer = u16(officer & 255)\n'
                                            '            '
                                            'state.officer_assignments.set_byte(officer, '
                                            'low8(city))\n'
                                            'force = u16(state.secondary_force() << 1)\n'
                                            'state.set_loyalty_source(state.force_heads.word(force))\n'
                                            'restore_returning_officer_assignments(state)'},
 'remove_defeated_packed_member': {'signature': 'state: GameplayState, officer: Word, context: '
                                                'GroupContext',
                                   'returns': 'GroupContext',
                                   'flow': 'officer = u16(officer)\n'
                                           'context = checked_context(context, state)\n'
                                           'group = context.source\n'
                                           'state.officer_assignments.set_byte(officer, 255)\n'
                                           'old_head = group.byte(13)\n'
                                           'count = group.byte() & 15\n'
                                           'if count == 1:\n'
                                           '    new_head = 65535\n'
                                           '    removed_bytes = 14\n'
                                           '    tail = group.at(count, 13).cursor()\n'
                                           '    destination = group.cursor()\n'
                                           'else:\n'
                                           '    group.set_byte(0, u8(group.byte() - 1))\n'
                                           '    index = 0\n'
                                           '    removed_bytes = 1\n'
                                           '    while group.byte(index, 13) != low8(officer):\n'
                                           '        index = u16(index + 1)\n'
                                           '    while True:\n'
                                           '        index = u16(index + 1)\n'
                                           '        if index == count:\n'
                                           '            break\n'
                                           '        group.set_byte(index, group.byte(index, 13), '
                                           '12)\n'
                                           '    tail = group.at(count, 13).cursor()\n'
                                           '    destination = group.at(count, 12).cursor()\n'
                                           '    new_head = group.byte(13)\n'
                                           'while True:\n'
                                           '    following_count = tail.byte() & 15\n'
                                           '    if following_count == 0:\n'
                                           '        destination.set_byte(0, 0)\n'
                                           '        break\n'
                                           '    for copied in '
                                           'descending_inclusive(u16(following_count + 12)):\n'
                                           '        destination.append_byte(tail.next_byte())\n'
                                           'replace_or_remove_group_references(state, old_head, '
                                           'new_head)\n'
                                           'other = context.target\n'
                                           'if other.address() >= group.address():\n'
                                           '    other = other.advance(-removed_bytes)\n'
                                           'return GroupContext(group, other)'},
 'remove_group_reference': {'signature': 'state: GameplayState, officer: Word',
                            'returns': 'None',
                            'flow': 'officer = u16(officer)\n'
                                    'pairs = '
                                    'state.pair_references.at(state.pair_reference_offset())\n'
                                    'while pairs.byte() != 0:\n'
                                    '    if pairs.byte(0, 1) == low8(officer):\n'
                                    '        break\n'
                                    '    pairs = pairs.advance(2)\n'
                                    'else:\n'
                                    '    return None\n'
                                    'source = pairs.advance(2).cursor()\n'
                                    'destination = pairs.cursor()\n'
                                    'while True:\n'
                                    '    value = source.next_byte()\n'
                                    '    destination.append_byte(value)\n'
                                    '    if value == 0:\n'
                                    '        return None\n'
                                    '    destination.append_byte(source.next_byte())'},
 'remove_zero_readiness_duelist': {'signature': 'state: GameplayState, officer: Word',
                                   'returns': 'None',
                                   'flow': 'checked_state(state)\n'
                                           'uint(officer, 16)\n'
                                           "if state.scalar('battle_active') == 0:\n"
                                           '    return\n'
                                           'state.officer_city_assignment.set_byte(officer, 255)\n'
                                           'source = _reuse_active_duel_roster(state, officer)\n'
                                           'while True:\n'
                                           '    member = source.next_word()\n'
                                           '    if negative_word(member):\n'
                                           '        return\n'
                                           '    if low8(member) == officer:\n'
                                           '        break\n'
                                           '_reuse_compact_after_match(source)'},
 'replace_group_head_reference': {'signature': 'state: GameplayState, officer: Word, group: Table',
                                  'returns': 'None',
                                  'flow': 'officer = u16(officer)\n'
                                          'group = checked_table(group, state)\n'
                                          'replacement = group.byte(13)\n'
                                          'pairs = '
                                          'state.pair_references.at(state.pair_reference_offset())\n'
                                          'while pairs.byte() != 0:\n'
                                          '    if pairs.byte(0, 1) == low8(officer):\n'
                                          '        break\n'
                                          '    pairs = pairs.advance(2)\n'
                                          'else:\n'
                                          '    return None\n'
                                          'pairs.set_byte(0, replacement, 1)\n'
                                          'records = state.head_records.cursor()\n'
                                          'while records.byte(0, 1) != low8(officer):\n'
                                          '    records = records.advance(1).cursor()\n'
                                          '    while records.next_byte() != 0:\n'
                                          '        pass\n'
                                          'records.set_byte(0, replacement, 1)'},
 'replace_or_remove_group_references': {'signature': 'state: GameplayState, old_head: Word, '
                                                     'new_head: Word',
                                        'returns': 'None',
                                        'flow': 'old_head = u16(old_head)\n'
                                                'new_head = u16(new_head)\n'
                                                'if new_head == old_head:\n'
                                                '    return None\n'
                                                'pairs = '
                                                'state.pair_references.at(state.pair_reference_offset()).cursor()\n'
                                                'while True:\n'
                                                '    if pairs.next_byte() == 0:\n'
                                                '        return None\n'
                                                '    if pairs.next_byte() == low8(old_head):\n'
                                                '        break\n'
                                                'if negative_word(new_head):\n'
                                                '    destination = pairs.advance(-2).cursor()\n'
                                                '    while True:\n'
                                                '        value = pairs.next_byte()\n'
                                                '        destination.append_byte(value)\n'
                                                '        if value == 0:\n'
                                                '            return None\n'
                                                '        '
                                                'destination.append_byte(pairs.next_byte())\n'
                                                'pairs.set_byte(65535, low8(new_head))\n'
                                                'records = state.head_records.cursor()\n'
                                                'while True:\n'
                                                '    if negative_byte(records.next_byte()):\n'
                                                '        return None\n'
                                                '    if records.next_byte() == low8(old_head):\n'
                                                '        records.set_byte(65535, low8(new_head))\n'
                                                '        return None\n'
                                                '    while records.next_byte() != 0:\n'
                                                '        pass'},
 'replenish_b200_troops': {'signature': 'state: GameplayState, retained_city: Word',
                           'returns': 'Word',
                           'flow': 'retained_city = u16(retained_city)\n'
                                   'for officer in descending_inclusive(255):\n'
                                   '    retained_city = u16(replace_byte(retained_city, '
                                   'state.officer_assignments.byte(officer)))\n'
                                   '    if retained_city > 40:\n'
                                   '        continue\n'
                                   '    if state.city_processed.byte(retained_city) != 0:\n'
                                   '        continue\n'
                                   '    retained_city = u16(officer << 1)\n'
                                   '    capacity = state.capacities_b000.word(retained_city)\n'
                                   '    divided = divu_retained(u32(capacity * 15), 100)\n'
                                   '    updated = u16(state.troops_b200.word(retained_city) + '
                                   'low16(divided))\n'
                                   '    if updated > capacity:\n'
                                   '        updated = capacity\n'
                                   '    state.troops_b200.set_word(retained_city, updated)\n'
                                   'return retained_city'},
 'reset_queue': {'signature': 'state: GameplayState',
                 'returns': 'None',
                 'flow': 'queue = state.queue()\n'
                         'for slot in range(42):\n'
                         '    queue.write_next(255)'},
 'restore_returning_officer_assignments': {'signature': 'state: GameplayState',
                                           'returns': 'None',
                                           'flow': 'roster = state.remaining_roster.cursor()\n'
                                                   'city = state.city()\n'
                                                   'while True:\n'
                                                   '    officer = roster.next_word()\n'
                                                   '    if negative_word(officer):\n'
                                                   '        return None\n'
                                                   '    '
                                                   'state.officer_assignments.set_byte(officer, '
                                                   'low8(city))\n'
                                                   '    state.set_selected_officer(officer)\n'
                                                   '    apply_returning_officer_loyalty(state)'},
 'roster_contains_force_head_carry': {'signature': 'state: GameplayState, city: Word, head: Word',
                                      'returns': 'ForceHeadMatch',
                                      'flow': 'checked_state(state)\n'
                                              'uint(city, 16)\n'
                                              'uint(head, 16)\n'
                                              'owner = state.city_owner_bytes.byte(city)\n'
                                              'force_head = state.force_heads.word(u16(owner << '
                                              '1))\n'
                                              'source = state.candidate_roster.cursor()\n'
                                              'while not negative_word(source.word()):\n'
                                              '    if source.next_word() == force_head:\n'
                                              '        return ForceHeadMatch(force_head, '
                                              'state.carry_result(1))\n'
                                              'return ForceHeadMatch(head, state.carry_result(0))'},
 'rounded_radial_distance': {'signature': 'state: GameplayState, squared_distance: Long',
                             'returns': 'Long',
                             'flow': 'checked_state(state)\n'
                                     'uint(squared_distance, 32)\n'
                                     'if squared_distance == 0:\n'
                                     '    return 0\n'
                                     'seed = seed_radial_distance_from_thresholds(state, '
                                     'squared_distance)\n'
                                     'remaining, count, increment = (seed.remaining, seed.count, '
                                     'seed.increment)\n'
                                     'while True:\n'
                                     '    previous = remaining\n'
                                     '    remaining = u32(remaining - increment)\n'
                                     '    if previous < increment:\n'
                                     '        return replace_word(remaining, low16(count))\n'
                                     '    count = replace_word(count, u16(count + 1))\n'
                                     '    increment = replace_word(increment, u16(increment + 2))'},
 'sample_once': {'signature': 'state: GameplayState',
                 'returns': 'Word',
                 'flow': 'return _reuse_random_sample(state)'},
 'sample_small': {'signature': 'state: GameplayState',
                  'returns': 'Word',
                  'flow': 'while True:\n'
                          '    sample = u16(_reuse_random_sample(state) & 7)\n'
                          '    if sample < 5:\n'
                          '        return sample'},
 'sample_wide': {'signature': 'state: GameplayState',
                 'returns': 'Word',
                 'flow': 'while True:\n'
                         '    sample = u16(_reuse_random_sample(state) & 15)\n'
                         '    if sample < 10:\n'
                         '        return sample'},
 'scaled_income': {'signature': 'state: GameplayState, offset: Word, factor: Word',
                   'returns': None,
                   'flow': 'rates: Table = state.secondary_rates\n'
                           'thresholds: Table = state.depletion_modifiers\n'
                           'bases: Table = state.income_bases\n'
                           'factor = mulu16(factor, thresholds.word(offset, 2))\n'
                           'factor = mulu16(factor, rates.word(offset, 2))\n'
                           'factor = divu16(factor, 15000)\n'
                           'gain: Long = bases.long(offset)\n'
                           'gain = mask32(gain, 65535)\n'
                           'gain = mulu16(gain, factor)\n'
                           'return gain'},
 'seed_radial_distance_from_thresholds': {'signature': 'state: GameplayState, squared_distance: '
                                                       'Long, retained_count: Long=0, '
                                                       'retained_threshold: Long=0',
                                          'returns': 'RadialSeed',
                                          'flow': 'checked_state(state)\n'
                                                  'uint(squared_distance, 32)\n'
                                                  'uint(retained_count, 32)\n'
                                                  'uint(retained_threshold, 32)\n'
                                                  'if squared_distance >= 144781:\n'
                                                  '    return RadialSeed(u32(squared_distance - '
                                                  '144781), replace_word(retained_count, 381), '
                                                  '762, retained_threshold, None)\n'
                                                  'thresholds = state.radial_threshold_rows\n'
                                                  'while squared_distance >= thresholds.long():\n'
                                                  '    thresholds = thresholds.advance(6)\n'
                                                  'preceding_threshold = thresholds.long(0, -6)\n'
                                                  'increment = thresholds.word(0, -2)\n'
                                                  'remaining = u32(squared_distance - '
                                                  'preceding_threshold)\n'
                                                  'count = replace_word(retained_count, increment '
                                                  '>> 1)\n'
                                                  'return RadialSeed(remaining, count, increment, '
                                                  'preceding_threshold, thresholds)'},
 'settle_battle_packed_armies': {'signature': 'state: GameplayState',
                                 'returns': 'None',
                                 'flow': 'transfer_outcome_officer(state)\n'
                                         'selected = state.table(state.selected_group_pointer())\n'
                                         'other = '
                                         'state.group_packets.at(state.group_offsets.word(state.selected_group_offset()))\n'
                                         'context = GroupContext(selected, other)\n'
                                         'officer = state.primary_officer()\n'
                                         'if state.troops.word(u16(officer << 1)) == 0:\n'
                                         '    officer = state.primary_officer()\n'
                                         '    context = remove_defeated_packed_member(state, '
                                         'officer, context)\n'
                                         '    state.set_selected_group_pointer(0)\n'
                                         'context = GroupContext(context.target, context.source)\n'
                                         'officer = state.secondary_officer()\n'
                                         'if state.troops.word(u16(officer << 1)) == 0:\n'
                                         '    officer = state.secondary_officer()\n'
                                         '    context = remove_defeated_packed_member(state, '
                                         'officer, context)\n'
                                         '    '
                                         'state.set_selected_group_pointer(context.target.address())\n'
                                         'settle_group_at_city(state)\n'
                                         'adjust_battle_losing_loyalty(state)'},
 'settle_duel_packets': {'signature': 'state: GameplayState, context: DuelSettlementContext',
                         'returns': 'CarryOutcome',
                         'flow': 'state = checked_state(state)\n'
                                 'context = _reuse_checked_context(context, '
                                 'DuelSettlementContext)\n'
                                 'first_packet, second_packet = (state.duel_packet_first, '
                                 'state.duel_packet_second)\n'
                                 'if first_packet.word(26) != '
                                 "state.scalar('duel_primary_officer'):\n"
                                 '    primary_packet, secondary_packet = (second_packet, '
                                 'first_packet)\n'
                                 'else:\n'
                                 '    primary_packet, secondary_packet = (first_packet, '
                                 'second_packet)\n'
                                 "state.set_scalar('duel_readiness_primary', "
                                 'primary_packet.word(28))\n'
                                 "state.set_scalar('duel_readiness_secondary', "
                                 'secondary_packet.word(28))\n'
                                 'first = first_packet.word(26)\n'
                                 'second = second_packet.word(26)\n'
                                 "disposition = state.scalar('result_first')\n"
                                 'if disposition:\n'
                                 '    apply_duel_disposition(state, DuelDispositionContext(first, '
                                 'disposition))\n'
                                 "second_disposition = state.scalar('result_second')\n"
                                 'if second_disposition:\n'
                                 '    apply_duel_disposition(state, DuelDispositionContext(second, '
                                 'second_disposition))\n'
                                 "if state.scalar('result_first') == 1:\n"
                                 '    return state.carry_result(1)\n'
                                 "if state.scalar('result_second') == 1:\n"
                                 '    return state.carry_result(1)\n'
                                 'detach_zero_readiness_duelists(state)\n'
                                 'incoming = replace_byte(context.training_carrier, '
                                 'second_disposition)\n'
                                 'settle_duel_training_and_troops(state, '
                                 'DuelSettlementContext(incoming))\n'
                                 'return state.carry_result(0)'},
 'settle_duel_result_roster': {'signature': 'state: GameplayState',
                               'returns': 'None',
                               'flow': 'checked_state(state)\n'
                                       "if state.scalar('battle_active') == 0:\n"
                                       '    return\n'
                                       "result = state.scalar('duel_result')\n"
                                       'if result < 6:\n'
                                       '    return\n'
                                       'if result == 6:\n'
                                       '    transfer_battle_roster(state, '
                                       "state.scalar('duel_primary_officer'))\n"
                                       'else:\n'
                                       '    transfer_battle_roster(state, '
                                       "state.scalar('duel_secondary_officer'))"},
 'settle_duel_training_and_troops': {'signature': 'state: GameplayState, context: '
                                                  'DuelSettlementContext',
                                     'returns': 'DuelSettlementResult',
                                     'flow': 'state = checked_state(state)\n'
                                             'context = _reuse_checked_context(context, '
                                             'DuelSettlementContext)\n'
                                             'progress = state.officer_word_c000\n'
                                             "first = state.scalar('duel_primary_officer')\n"
                                             'carrier = replace_byte(context.training_carrier, '
                                             "state.scalar('duel_training_primary'))\n"
                                             "if state.scalar('duel_result') == 4:\n"
                                             '    carrier = _reuse_duel_training_loss(state, '
                                             'carrier)\n'
                                             'state.officer_training.set_byte(first, carrier & '
                                             '255)\n'
                                             'first_offset = u16(first << 1)\n'
                                             "readiness = state.scalar('duel_readiness_primary')\n"
                                             'state.officer_readiness.set_word(first_offset, '
                                             'readiness)\n'
                                             'if readiness == 0:\n'
                                             "    donor = state.scalar('duel_secondary_officer')\n"
                                             '    carrier = grant_duel_fallback_progress(state, '
                                             'first_offset, donor, progress)\n'
                                             '    remove_zero_readiness_duelist(state, '
                                             "state.scalar('duel_primary_officer'))\n"
                                             "second = state.scalar('duel_secondary_officer')\n"
                                             'carrier = replace_byte(carrier, '
                                             "state.scalar('duel_training_secondary'))\n"
                                             "if state.scalar('duel_result') == 5:\n"
                                             '    carrier = _reuse_duel_training_loss(state, '
                                             'carrier)\n'
                                             'state.officer_training.set_byte(second, carrier & '
                                             '255)\n'
                                             'second_offset = u16(second << 1)\n'
                                             'readiness = '
                                             "state.scalar('duel_readiness_secondary')\n"
                                             'state.officer_readiness.set_word(second_offset, '
                                             'readiness)\n'
                                             'if readiness == 0:\n'
                                             "    donor = state.scalar('duel_primary_officer')\n"
                                             '    carrier = grant_duel_fallback_progress(state, '
                                             'second_offset, donor, progress)\n'
                                             '    remove_zero_readiness_duelist(state, '
                                             "state.scalar('duel_secondary_officer'))\n"
                                             "first = state.scalar('duel_primary_officer')\n"
                                             "second = state.scalar('duel_secondary_officer')\n"
                                             'old_troops = state.officer_troops.word(u16(first << '
                                             '2), 2)\n'
                                             "new_troops = state.scalar('duel_troops_primary')\n"
                                             'difference = 0 if old_troops < new_troops else '
                                             'u16(old_troops - new_troops)\n'
                                             'carrier = '
                                             'grant_duel_troop_difference_progress(state, second, '
                                             'difference, progress)\n'
                                             'old_troops = state.officer_troops.word(u16(second << '
                                             '2), 2)\n'
                                             "new_troops = state.scalar('duel_troops_secondary')\n"
                                             'difference = 0 if old_troops < new_troops else '
                                             'u16(old_troops - new_troops)\n'
                                             'carrier = '
                                             'grant_duel_troop_difference_progress(state, first, '
                                             'difference, progress)\n'
                                             'state.officer_troops.set_word(u16(first << 2), '
                                             "state.scalar('duel_troops_primary'), 2)\n"
                                             'state.officer_troops.set_word(u16(second << 2), '
                                             "state.scalar('duel_troops_secondary'), 2)\n"
                                             'settle_duel_result_roster(state)\n'
                                             'return DuelSettlementResult(carrier)'},
 'settle_expense': {'signature': 'state: GameplayState, city: Word, factor: Word, ledger: Table',
                    'returns': None,
                    'flow': 'categories: Table = state.officer_categories\n'
                            'city = add16(city, 1)\n'
                            'state.set_head(word(-1))\n'
                            'count: Word = build_roster(state, city)\n'
                            'state.set_roster_count(count)\n'
                            'city = sub16(city, 1)\n'
                            'amounts: Table = state.officer_amounts\n'
                            'roster: Table = state.roster\n'
                            'total: Long = long(0)\n'
                            'while True:\n'
                            '    member: Word = roster.next_word()\n'
                            '    if signed_word(member) < 0:\n'
                            '        break\n'
                            '    member = shl16(member, 2)\n'
                            '    total = add32(total, amounts.long(member))\n'
                            'total = stitched_product(total, factor)\n'
                            'total = divu16(total, 5000)\n'
                            'roster = state.roster\n'
                            'fees_table: Table = state.expense_parameters\n'
                            'fees: Word = word(0)\n'
                            'while True:\n'
                            '    member = roster.next_word()\n'
                            '    if signed_word(member) < 0:\n'
                            '        break\n'
                            '    category: Byte = categories.byte(member)\n'
                            '    category = mask16(category, 5)\n'
                            '    category = shl16(category, 1)\n'
                            '    fees = add16(fees, fees_table.word(category))\n'
                            'fees = mulu16(fees, factor)\n'
                            'fees = divu16(fees, 100)\n'
                            'total = mask32(total, 65535)\n'
                            'fees = mask32(fees, 65535)\n'
                            'fees = add32(fees, total)\n'
                            'offset: Word = shl16(city, 2)\n'
                            'remaining: Long = ledger.long(offset)\n'
                            'remaining, borrowed = subtract_borrow32(remaining, fees)\n'
                            'if borrowed:\n'
                            '    settle_shortage(state, remaining, factor)\n'
                            '    remaining = long(0)\n'
                            'else:\n'
                            '    remaining = minimum32(remaining, 999999)\n'
                            'offset = shl16(city, 2)\n'
                            'ledger.set_long(offset, remaining)'},
 'settle_group_at_city': {'signature': 'state: GameplayState',
                          'returns': 'None',
                          'flow': 'if state.opposing_group() == 0:\n'
                                  '    return\n'
                                  'packet = state.table(state.opposing_group())\n'
                                  'row = u16(packet.byte(0, 1))\n'
                                  'column = u16(packet.byte(0, 2))\n'
                                  'kind, terrain = state.terrain_query(row, column)\n'
                                  'if not negative_byte(terrain):\n'
                                  '    return\n'
                                  'city = locate_group_city(state, packet)\n'
                                  'remaining = u16((packet.byte() & 15) - 1)\n'
                                  'assignments = state.city_assignments\n'
                                  'for member_index in descending_inclusive(remaining):\n'
                                  '    officer = u16(packet.byte(member_index, 13))\n'
                                  '    assignments.set_byte(officer, low8(city))\n'
                                  'credit_packed_group_resources(state, packet, city)\n'
                                  'erase_group_packet(state, packet)'},
 'settle_shortage': {'signature': 'state: GameplayState, outstanding: Long, factor: Word',
                     'returns': None,
                     'flow': 'outstanding = negate32(outstanding)\n'
                             'outstanding = stitched_product(outstanding, factor)\n'
                             'roster: Table = state.roster\n'
                             'scores: Table = state.scores\n'
                             'first: Table = state.first_score_components\n'
                             'second: Table = state.second_score_components\n'
                             'while True:\n'
                             '    member: Word = roster.next_word()\n'
                             '    if signed_word(member) < 0:\n'
                             '        break\n'
                             '    first_score: Long = long(0)\n'
                             '    member = shl16(member, 1)\n'
                             '    first_score = first.word(member)\n'
                             '    score: Long = long(0)\n'
                             '    score = second.word(member)\n'
                             '    score = add32(score, first_score)\n'
                             '    scores.append_long(score)\n'
                             'scores = state.scores\n'
                             'roster = state.roster\n'
                             'passes: Word = state.roster_count()\n'
                             'if passes > 1:\n'
                             '    passes = sub16(passes, 1)\n'
                             '    while True:\n'
                             '        compared: Word = word(0)\n'
                             '        member_offset: Word = word(0)\n'
                             '        score_offset: Word = word(0)\n'
                             '        while True:\n'
                             '            left: Long = scores.long(score_offset)\n'
                             '            if left > scores.long(score_offset, 4):\n'
                             '                scores.set_long(score_offset, '
                             'scores.long(score_offset, 4))\n'
                             '                scores.set_long(score_offset, left, 4)\n'
                             '                left = roster.word(member_offset)\n'
                             '                roster.set_word(member_offset, '
                             'roster.word(member_offset, 2))\n'
                             '                roster.set_word(member_offset, left, 2)\n'
                             '            compared = add16(compared, 1)\n'
                             '            member_offset = add16(member_offset, 2)\n'
                             '            score_offset = add16(score_offset, 4)\n'
                             '            if compared >= passes:\n'
                             '                break\n'
                             '        passes = sub16(passes, 1)\n'
                             '        if passes == 0:\n'
                             '            break\n'
                             'roster = state.roster\n'
                             'amounts: Table = state.officer_amounts\n'
                             'modifiers: Table = state.officer_modifiers\n'
                             'while True:\n'
                             '    member = roster.next_word()\n'
                             '    if signed_word(member) < 0:\n'
                             '        break\n'
                             '    offset: Word = shl16(member, 2)\n'
                             '    amount: Long = amounts.long(offset)\n'
                             '    if amount > outstanding:\n'
                             '        quantity: Long = outstanding\n'
                             '        outstanding = clear_low_word(outstanding)\n'
                             '    else:\n'
                             '        outstanding = sub32(outstanding, amount)\n'
                             '        quantity = amount\n'
                             '    modifier: Word = word(100)\n'
                             '    modifier = sub8(modifier, modifiers.byte(member))\n'
                             '    quantity = mulu16(quantity, modifier)\n'
                             '    quantity = divu16(quantity, 100)\n'
                             '    quantity = mask32(quantity, 65535)\n'
                             '    amount = sub32(amount, quantity)\n'
                             '    amounts.set_long(offset, amount)\n'
                             '    if outstanding == 0:\n'
                             '        break\n'
                             'if outstanding != 0:\n'
                             '    roster = state.roster\n'
                             '    modifiers = state.officer_modifiers\n'
                             '    penalties: Table = state.officer_penalties\n'
                             '    while True:\n'
                             '        member = roster.next_word()\n'
                             '        if signed_word(member) < 0:\n'
                             '            break\n'
                             '        deduction: Long = long(100)\n'
                             '        deduction = sub8(deduction, modifiers.byte(member))\n'
                             '        deduction = divu16(deduction, 10)\n'
                             '        borrowed = penalties.subtract_byte(member, deduction)\n'
                             '        if borrowed:\n'
                             '            penalties.set_byte(member, byte(0))'},
 'signed_divmod': {'signature': 'state: GameplayState, numerator: Long, denominator: Long',
                   'returns': 'tuple[Long, Long]',
                   'flow': 'checked_state(state)\n'
                           'uint(numerator, 32)\n'
                           'uint(denominator, 32)\n'
                           'if negative_long(denominator):\n'
                           '    quotient, remainder = positive_denominator(state, numerator, '
                           'u32(-denominator))\n'
                           '    return (u32(-quotient), remainder)\n'
                           'return positive_denominator(state, numerator, denominator)'},
 'sort_returning_officer_status': {'signature': 'state: GameplayState, surplus: Word',
                                   'returns': 'Word',
                                   'flow': 'surplus = u16(surplus)\n'
                                           'state.set_returning_count(u16(state.returning_count() '
                                           '+ surplus))\n'
                                           'roster = state.remaining_roster.cursor()\n'
                                           'candidates = state.battle_candidate_roster\n'
                                           'statuses = state.status_roster\n'
                                           'candidates.set_word(0, 65535)\n'
                                           'retained_status = 0\n'
                                           'while True:\n'
                                           '    offset = 0\n'
                                           '    officer = roster.next_word()\n'
                                           '    if negative_word(officer):\n'
                                           '        break\n'
                                           '    retained_status = '
                                           'u16(replace_byte(retained_status, '
                                           'state.status.byte(officer)))\n'
                                           '    while not negative_word(candidates.word(offset)):\n'
                                           '        if low8(retained_status) > '
                                           'statuses.byte(offset, 1):\n'
                                           '            break\n'
                                           '        offset = u16(offset + 2)\n'
                                           '    while True:\n'
                                           '        displaced = candidates.word(offset)\n'
                                           '        candidates.set_word(offset, officer)\n'
                                           '        if negative_word(officer):\n'
                                           '            break\n'
                                           '        displaced_status = statuses.word(offset)\n'
                                           '        statuses.set_word(offset, retained_status)\n'
                                           '        offset = u16(offset + 2)\n'
                                           '        officer = displaced\n'
                                           '        retained_status = displaced_status\n'
                                           'returning = state.survivor_roster.cursor()\n'
                                           'while not negative_word(returning.next_word()):\n'
                                           '    pass\n'
                                           'returning = returning.advance(-2)\n'
                                           'source = candidates.cursor()\n'
                                           'for member in descending_inclusive(u16(surplus - 1)):\n'
                                           '    returning.append_word(source.next_word())\n'
                                           'returning.set_word(0, 65535)\n'
                                           'remaining = state.remaining_roster.cursor()\n'
                                           'count = 0\n'
                                           'while True:\n'
                                           '    officer = source.next_word()\n'
                                           '    remaining.append_word(officer)\n'
                                           '    if negative_word(officer):\n'
                                           '        break\n'
                                           '    count = u16(count + 1)\n'
                                           'state.set_remaining_count(count)\n'
                                           'return count'},
 'step_random': {'signature': 'state: GameplayState',
                 'returns': 'Long',
                 'flow': 'return _reuse_advance_random_pair(state).sample'},
 'submit_classified_fields': {'signature': 'state: GameplayState, city: Word',
                              'returns': 'Word',
                              'flow': 'city = checked_word(city)\n'
                                      'saved_city = city\n'
                                      'offset = u16(city << 2)\n'
                                      "field = state.field('e320')\n"
                                      'mask = 0\n'
                                      'classified = divu_retained(field.read(offset), 10)\n'
                                      "mask = replace_byte(mask, state.parameter('mask', "
                                      'low16(classified)))\n'
                                      'if low16(classified) >= 7:\n'
                                      '    return saved_city\n'
                                      'sample = u16(sample_once(state) & mask)\n'
                                      'if sample != 0:\n'
                                      '    return saved_city\n'
                                      'append_queue(state, saved_city, sample)\n'
                                      'offset = u16(saved_city << 2)\n'
                                      'base_factor = 0\n'
                                      'base_factor = replace_byte(base_factor, '
                                      "state.parameter('factor', low16(classified)))\n"
                                      'factor = 0\n'
                                      'if low16(classified) < 7:\n'
                                      '    factor = sample_wide(state)\n'
                                      '    if low16(classified) >= 6:\n'
                                      '        factor = sample_small(state)\n'
                                      'factor = u16(factor + base_factor)\n'
                                      "_reuse_scale_field(state, offset, factor, 'e1e0')\n"
                                      "_reuse_scale_field(state, offset, factor, 'e000')\n"
                                      "_reuse_scale_field(state, offset, factor, 'e0a0')\n"
                                      "_reuse_scale_field(state, offset, factor, 'e5a0')\n"
                                      'factor = u16(sample_small(state) + 95)\n'
                                      "_reuse_scale_field(state, offset, factor, 'e140')\n"
                                      'return saved_city'},
 'submit_four_fields': {'signature': 'state: GameplayState, city: Word, incoming_owner: Word',
                        'returns': 'EventSubmission',
                        'flow': 'city = checked_word(city)\n'
                                'incoming_owner = checked_word(incoming_owner)\n'
                                'owner = replace_byte(incoming_owner, state.owner(city))\n'
                                'if negative_byte(owner):\n'
                                '    return EventSubmission(owner, owner)\n'
                                'saved_city = city\n'
                                'sample = u16(sample_once(state) & 15)\n'
                                'if sample != 0:\n'
                                '    return EventSubmission(saved_city, saved_city)\n'
                                'append_queue(state, saved_city, sample)\n'
                                'offset = u16(saved_city << 2)\n'
                                'factor = u16(sample_wide(state) + 80)\n'
                                "_reuse_scale_field(state, offset, factor, 'e1e0')\n"
                                'factor = u16(sample_small(state) + 95)\n'
                                "_reuse_scale_field(state, offset, factor, 'e140')\n"
                                'factor = u16(sample_wide(state) + 85)\n'
                                "_reuse_scale_field(state, offset, factor, 'e320')\n"
                                'factor = u16(sample_wide(state) + 80)\n'
                                "_reuse_scale_field(state, offset, factor, 'e0a0')\n"
                                'return EventSubmission(saved_city, saved_city)'},
 'submit_three_fields': {'signature': 'state: GameplayState, city: Word, incoming_owner: Word',
                         'returns': 'EventSubmission',
                         'flow': 'city = checked_word(city)\n'
                                 'incoming_owner = checked_word(incoming_owner)\n'
                                 'owner = replace_byte(incoming_owner, state.owner(city))\n'
                                 'if negative_byte(owner):\n'
                                 '    return EventSubmission(city, owner)\n'
                                 'saved_city = city\n'
                                 'sample = u16(sample_once(state) & 15)\n'
                                 'if sample != 0:\n'
                                 '    return EventSubmission(saved_city, saved_city)\n'
                                 'append_queue(state, saved_city, sample)\n'
                                 'offset = u16(saved_city << 2)\n'
                                 'factor = u16(sample_wide(state) + 80)\n'
                                 "_reuse_scale_field(state, offset, factor, 'e1e0')\n"
                                 'factor = u16(sample_small(state) + 95)\n'
                                 "_reuse_scale_field(state, offset, factor, 'e140')\n"
                                 'factor = u16(sample_wide(state) + 85)\n'
                                 "_reuse_scale_field(state, offset, factor, 'e320')\n"
                                 'return EventSubmission(saved_city, saved_city)'},
 'sum_group_troops': {'signature': 'state: GameplayState, roster: Cursor, troops: Table',
                      'returns': 'tuple[Long, Word]',
                      'flow': 'checked_state(state)\n'
                              'checked_table(roster, state)\n'
                              'checked_table(troops, state)\n'
                              'total, count = (0, 0)\n'
                              'while True:\n'
                              '    member = roster.next_word()\n'
                              '    if negative_word(member):\n'
                              '        return (total, count)\n'
                              '    count = u16(count + 1)\n'
                              '    total = u32(total + troops.long(u16(low8(member) << 2)))'},
 'terrain_cell_query': {'signature': 'state: GameplayState, row: Word, column: Word',
                        'returns': 'tuple[Byte, Byte]',
                        'flow': 'row = u16(row)\n'
                                'column = u16(column)\n'
                                'stride = u16(row << 3)\n'
                                'index = u16(u16(row + stride) << 3)\n'
                                'index = u16(index + column)\n'
                                'terrain = state.terrain_cells.byte(index)\n'
                                'cost = state.terrain_costs.byte(terrain)\n'
                                'return (terrain, cost)'},
 'transfer_battle_roster': {'signature': 'state: GameplayState, officer: Word',
                            'returns': 'None',
                            'flow': 'checked_state(state)\n'
                                    'uint(officer, 16)\n'
                                    'source = state.battle_secondary_roster.cursor()\n'
                                    'destination = state.battle_secondary_retired_roster.cursor()\n'
                                    "if officer == state.scalar('roster_side_owner'):\n"
                                    '    source = state.battle_primary_roster.cursor()\n'
                                    '    destination = '
                                    'state.battle_primary_retired_roster.cursor()\n'
                                    'while True:\n'
                                    '    member = source.next_word()\n'
                                    '    if negative_word(member):\n'
                                    '        return\n'
                                    '    if low8(member) == officer:\n'
                                    '        break\n'
                                    '_reuse_compact_after_match(source)\n'
                                    'while not negative_word(destination.next_word()):\n'
                                    '    pass\n'
                                    'destination.set_word(0, officer, -2)\n'
                                    'destination.put_word(65535)'},
 'transfer_outcome_officer': {'signature': 'state: GameplayState',
                              'returns': 'None',
                              'flow': 'outcome = state.outcome()\n'
                                      'if outcome < 6:\n'
                                      '    return None\n'
                                      'if outcome == 6:\n'
                                      '    officer = state.winning_officer()\n'
                                      'else:\n'
                                      '    officer = state.losing_officer()\n'
                                      'source = state.table(state.selected_group_pointer())\n'
                                      'target = '
                                      'state.group_packets.at(state.group_offsets.word(state.selected_group_offset()))\n'
                                      'if officer != state.primary_officer():\n'
                                      '    source, target = (target, source)\n'
                                      'context = detach_member_keep_group_cursor(state, officer, '
                                      'GroupContext(source, target))\n'
                                      'context = attach_member_shift_packet(state, officer, '
                                      'context)\n'
                                      'if officer != state.primary_officer():\n'
                                      '    context = GroupContext(context.target, context.source)\n'
                                      'state.set_selected_group_pointer(context.source.address())\n'
                                      'relative = u32(context.target.address() - '
                                      'state.group_packets.address())\n'
                                      'state.group_offsets.set_word(state.selected_group_offset(), '
                                      'u16(relative))'},
 'unsigned_divmod': {'signature': 'state: GameplayState, numerator: Long, denominator: Long',
                     'returns': 'tuple[Long, Long]',
                     'flow': 'checked_state(state)\n'
                             'uint(numerator, 32)\n'
                             'uint(denominator, 32)\n'
                             'if denominator <= 65535:\n'
                             '    return word_pair_divmod(state, numerator, denominator)\n'
                             'if denominator == numerator:\n'
                             '    return (1, 0)\n'
                             'if denominator > numerator:\n'
                             '    return (0, numerator)\n'
                             'divisor_high = u32(high16(denominator) + 1)\n'
                             'quotient, remainder = word_pair_divmod(state, numerator, '
                             'divisor_high)\n'
                             'denominator_part = divu_retained(denominator, low16(divisor_high))\n'
                             'quotient = low16(divu_retained(quotient, low16(denominator_part)))\n'
                             'while True:\n'
                             '    product = u32(low16(denominator) * low16(quotient))\n'
                             '    upper_product = u32(high16(denominator) * low16(quotient))\n'
                             '    product = u32(product + swap_words(upper_product))\n'
                             '    if product > numerator:\n'
                             '        quotient = u32(quotient - 1)\n'
                             '        continue\n'
                             '    remainder = u32(numerator - product)\n'
                             '    if denominator <= remainder:\n'
                             '        quotient = u32(quotient + 1)\n'
                             '        continue\n'
                             '    return (quotient, remainder)'},
 'word_pair_divmod': {'signature': 'state: GameplayState, numerator: Long, denominator: Long',
                      'returns': 'tuple[Long, Long]',
                      'flow': 'checked_state(state)\n'
                              'uint(numerator, 32)\n'
                              'uint(denominator, 32)\n'
                              'divisor = low16(denominator)\n'
                              'upper_division = divu_retained(high16(numerator), divisor)\n'
                              'upper_quotient = low16(upper_division)\n'
                              'lower_dividend = u32(high16(upper_division) << 16 | '
                              'low16(numerator))\n'
                              'lower_division = divu_retained(lower_dividend, divisor)\n'
                              'return (u32(upper_quotient << 16 | low16(lower_division)), '
                              'high16(lower_division))'},
 'wrapped_product': {'signature': 'value: Long, factor: Word',
                     'returns': 'Long',
                     'flow': 'value = checked_long(value)\n'
                             'factor = checked_word(factor)\n'
                             'return u32(value * factor)'},
 '_reuse_active_duel_roster': {'signature': 'state: GameplayState, officer: Word',
                               'returns': None,
                               'flow': "if officer == state.scalar('roster_side_owner'):\n"
                                       '    return state.battle_primary_roster.cursor()\n'
                                       'return state.battle_secondary_roster.cursor()'},
 '_reuse_advance_random_pair': {'signature': 'state: GameplayState',
                                'returns': 'RandomSample',
                                'flow': 'checked_state(state)\n'
                                        "original = state.scalar('random_seed')\n"
                                        'if original == 0:\n'
                                        '    original = 711800410\n'
                                        'mixed = u32(u32(u32(u32(original << 2) + original) << 3) '
                                        '+ original)\n'
                                        'sample = replace_word(original, low16(mixed))\n'
                                        'mixed = swap_words(mixed)\n'
                                        'sample = replace_word(sample, u16(low16(sample) + '
                                        'low16(mixed)))\n'
                                        'mixed = swap_words(replace_word(mixed, low16(sample)))\n'
                                        "state.set_scalar('random_seed', mixed)\n"
                                        'return RandomSample(sample, mixed)'},
 '_reuse_append_at_roster_end': {'signature': 'destination: Cursor, officer: Word',
                                 'returns': 'None',
                                 'flow': 'while not negative_word(destination.next_word()):\n'
                                         '    pass\n'
                                         'destination.set_word(0, officer, -2)\n'
                                         'destination.put_word(65535)'},
 '_reuse_assigned_troop_total': {'signature': 'state: GameplayState, assignments: Table, city: '
                                              'Word',
                                 'returns': 'Long',
                                 'flow': 'total = 0\n'
                                         'for officer in range(255, -1, -1):\n'
                                         '    if assignments.byte(officer) == city & 255:\n'
                                         '        total = u32(total + '
                                         'state.officer_troops.long(u16(officer << 2)))\n'
                                         '        total = u32(total + 100)\n'
                                         'return total'},
 '_reuse_candidate_strength_totals': {'signature': 'state: GameplayState',
                                      'returns': 'tuple[Long, Word, Word]',
                                      'flow': 'source = state.action_candidates.cursor()\n'
                                              'troops, first_attribute, second_attribute = (0, 0, '
                                              '0)\n'
                                              'while True:\n'
                                              '    officer = source.next_word()\n'
                                              '    if negative_word(officer):\n'
                                              '        return (troops, first_attribute, '
                                              'second_attribute)\n'
                                              '    offset = u16(officer << 1)\n'
                                              '    first_attribute = u16(first_attribute + '
                                              'state.officer_word_b400.word(offset))\n'
                                              '    second_attribute = u16(second_attribute + '
                                              'state.officer_word_b600.word(offset))\n'
                                              '    troops = u32(troops + '
                                              'state.officer_troops.long(u16(offset << 1)))'},
 '_reuse_compact_after_match': {'signature': 'source',
                                'returns': None,
                                'flow': 'while True:\n'
                                        '    member = source.next_word()\n'
                                        '    source.set_word(0, member, -4)\n'
                                        '    if negative_word(member):\n'
                                        '        return'},
 '_reuse_compact_live_roster': {'signature': 'source: Cursor',
                                'returns': 'None',
                                'flow': 'while True:\n'
                                        '    member = source.next_word()\n'
                                        '    source.set_word(0, member, -4)\n'
                                        '    if negative_word(member):\n'
                                        '        return'},
 '_reuse_duel_training_loss': {'signature': 'state: GameplayState, carrier: Long',
                               'returns': 'Long',
                               'flow': 'sample = low16(state.sample_random())\n'
                                       'doubled = u32(sample << 1)\n'
                                       'scaled = replace_word(doubled, u16(low16(doubled) + '
                                       'sample))\n'
                                       'loss = u16(high16(scaled) + 1)\n'
                                       'previous = low16(carrier)\n'
                                       'return replace_word(carrier, 0 if previous < loss else '
                                       'u16(previous - loss))'},
 '_reuse_low_readiness_progress': {'signature': 'state: GameplayState, readiness_offset: Word, '
                                                'check_city_head: bool, detach: bool',
                                   'returns': 'Word',
                                   'flow': 'progress = '
                                           'state.officer_word_c000.word(readiness_offset)\n'
                                           'value = divu_retained(progress, 5)\n'
                                           'officer = readiness_offset >> 1\n'
                                           'if check_city_head:\n'
                                           "    scene_offset = u16(state.scalar('battle_scene') << "
                                           '1)\n'
                                           '    if officer == '
                                           'state.city_head_words.word(scene_offset):\n'
                                           '        value = replace_word(value, u16(low16(value) + '
                                           '30))\n'
                                           'if detach:\n'
                                           '    state.officer_city_assignment.set_byte(officer, '
                                           '255)\n'
                                           'if state.officer_status.byte(officer) & 16:\n'
                                           '    value = replace_word(value, u16(low16(value) + '
                                           '20))\n'
                                           'return low16(value)'},
 '_reuse_multiply_word_parts': {'signature': 'value: Long, factor: Word',
                                'returns': 'Long',
                                'flow': 'return u32(low16(value) * factor + '
                                        'swap_words(high16(value) * factor))'},
 '_reuse_random_fraction': {'signature': 'state: GameplayState, span: Word, base: Word=0',
                            'returns': 'Word',
                            'flow': 'sample = low16(state.sample_random())\n'
                                    'return u16(high16(u32(sample * span)) + base)'},
 '_reuse_seek_officer_unbounded': {'signature': 'source: Cursor, officer: Word',
                                   'returns': 'None',
                                   'flow': 'while source.next_word() & 255 != officer:\n    pass'},
 '_reuse_checked_context': {'signature': 'value, expected',
                            'returns': None,
                            'flow': 'if type(value) is not expected:\n'
                                    "    raise ValueError('exact outcome-family context "
                                    "required')\n"
                                    'value.__post_init__()\n'
                                    'return value'},
 '_reuse_collect_city_attached_officers': {'signature': 'state: GameplayState',
                                           'returns': 'Word',
                                           'flow': 'output = '
                                                   'state.battle_candidate_roster.cursor()\n'
                                                   'city = state.city()\n'
                                                   'count = 0\n'
                                                   'for officer in descending_inclusive(255):\n'
                                                   '    if state.officer_assignments.byte(officer) '
                                                   '== low8(city):\n'
                                                   '        output.append_word(officer)\n'
                                                   '        count = u16(count + 1)\n'
                                                   'output.set_word(0, 65535)\n'
                                                   'return count'},
 '_reuse_collect_unassigned_city_officers': {'signature': 'state: GameplayState',
                                             'returns': 'Word',
                                             'flow': 'output = '
                                                     'state.battle_candidate_roster.cursor()\n'
                                                     'city = state.city()\n'
                                                     'count = 0\n'
                                                     'for officer in descending_inclusive(255):\n'
                                                     '    if '
                                                     'state.alternate_assignments.byte(officer) == '
                                                     'low8(city):\n'
                                                     '        if not '
                                                     'negative_byte(state.officer_assignments.byte(officer)):\n'
                                                     '            output.append_word(officer)\n'
                                                     '            count = u16(count + 1)\n'
                                                     'output.set_word(0, 65535)\n'
                                                     'return count'},
 '_reuse_random_sample': {'signature': 'state: GameplayState',
                          'returns': 'Word',
                          'flow': 'seed = state.seed()\n'
                                  'if seed == 0:\n'
                                  '    seed = 711800410\n'
                                  'original = seed\n'
                                  'mixed = u32(seed << 2)\n'
                                  'mixed = u32(mixed + original)\n'
                                  'mixed = u32(mixed << 3)\n'
                                  'mixed = u32(mixed + original)\n'
                                  'sample = replace_word(original, low16(mixed))\n'
                                  'mixed = swap_words(mixed)\n'
                                  'sample = replace_word(sample, u16(sample + mixed))\n'
                                  'mixed = replace_word(mixed, low16(sample))\n'
                                  'mixed = swap_words(mixed)\n'
                                  'state.store_seed(mixed)\n'
                                  'return low16(sample)'},
 '_reuse_scale_field': {'signature': 'state: GameplayState, offset: Word, factor: Word, '
                                     'field_name: str',
                        'returns': 'Long',
                        'flow': 'offset = checked_word(offset)\n'
                                'factor = checked_word(factor)\n'
                                'field = state.field(field_name)\n'
                                'previous = field.read(offset)\n'
                                'product = wrapped_product(previous, factor)\n'
                                'result = divide_percent(state, product)\n'
                                'field.write(offset, result)\n'
                                'return result'}}

def _lower_build_roster(e,rules):
    e.label('gameplay_pc_005f48')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('gameplay_pc_005f4c')
    e.ins('lea.l','0xf500:w,%a1',4)
    e.label('gameplay_pc_005f50')
    e.ins('clr.w','%d1',2)
    e.label('gameplay_pc_005f52')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_005f54')
    e.ins('move.w','0xf630:w,%d4',4)
    e.label('gameplay_pc_005f58')
    e.ins('bmi.b','gameplay_pc_005f5e',2)
    e.label('gameplay_pc_005f5a')
    e.ins('move.w','%d4,(%a1)+',2)
    e.label('gameplay_pc_005f5c')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('gameplay_pc_005f5e')
    e.ins('move.b','(%a0)+,%d2',2)
    e.label('gameplay_pc_005f60')
    e.ins('cmp.b','%d0,%d2',2)
    e.label('gameplay_pc_005f62')
    e.ins('bne.b','gameplay_pc_005f6e',2)
    e.label('gameplay_pc_005f64')
    e.ins('cmp.w','0xf630:w,%d1',4)
    e.label('gameplay_pc_005f68')
    e.ins('beq.b','gameplay_pc_005f6e',2)
    e.label('gameplay_pc_005f6a')
    e.ins('move.w','%d1,(%a1)+',2)
    e.label('gameplay_pc_005f6c')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('gameplay_pc_005f6e')
    e.ins('addq.w','#0x1,%d1',2)
    e.label('gameplay_pc_005f70')
    e.ins('cmpi.w','#0x100,%d1',4)
    e.label('gameplay_pc_005f74')
    e.ins('bcs.b','gameplay_pc_005f5e',2)
    e.label('gameplay_pc_005f76')
    e.ins('move.w','#0xffff,(%a1)',4)
    e.label('gameplay_pc_005f7a')
    e.ins('rts','',2)

def _lower_step_random(e,rules):
    e.label('gameplay_pc_0083d4')
    e.ins('move.l','0xf61c:w,%d1',4)
    e.label('gameplay_pc_0083d8')
    e.ins('bne.b','gameplay_pc_0083e0',2)
    e.label('gameplay_pc_0083da')
    e.ins('move.l','#0x2a6d365a,%d1',6)
    e.label('gameplay_pc_0083e0')
    e.ins('move.l','%d1,%d0',2)
    e.label('gameplay_pc_0083e2')
    e.ins('asl.l','#0x2,%d1',2)
    e.label('gameplay_pc_0083e4')
    e.ins('add.l','%d0,%d1',2)
    e.label('gameplay_pc_0083e6')
    e.ins('asl.l','#0x3,%d1',2)
    e.label('gameplay_pc_0083e8')
    e.ins('add.l','%d0,%d1',2)
    e.label('gameplay_pc_0083ea')
    e.ins('move.w','%d1,%d0',2)
    e.label('gameplay_pc_0083ec')
    e.ins('swap','%d1',2)
    e.label('gameplay_pc_0083ee')
    e.ins('add.w','%d1,%d0',2)
    e.label('gameplay_pc_0083f0')
    e.ins('move.w','%d0,%d1',2)
    e.label('gameplay_pc_0083f2')
    e.ins('swap','%d1',2)
    e.label('gameplay_pc_0083f4')
    e.ins('move.l','%d1,0xf61c:w',4)
    e.label('gameplay_pc_0083f8')
    e.ins('rts','',2)

def _lower_choose_city_head(e,rules):
    e.label('gameplay_pc_00e1f6')
    e.ins('movem.l','%d1-%d5/%a0-%a2,-(%a7)',4)
    e.label('gameplay_pc_00e1fa')
    e.ins('lea.l','0xf500:w,%a0',4)
    e.label('gameplay_pc_00e1fe')
    e.ins('move.w','(%a0)+,%d4',2)
    e.label('gameplay_pc_00e200')
    e.ins('bmi.w','gameplay_pc_00e232',4)
    e.label('gameplay_pc_00e204')
    e.ins('bsr.w','gameplay_pc_00e26c',4)
    e.label('gameplay_pc_00e208')
    e.ins('bcs.w','gameplay_pc_00e25a',4)
    e.label('gameplay_pc_00e20c')
    e.ins('andi.w','#0xff,%d4',4)
    e.label('gameplay_pc_00e210')
    e.ins('lea.l','0xc300:w,%a1',4)
    e.label('gameplay_pc_00e214')
    e.ins('move.w','%d4,%d3',2)
    e.label('gameplay_pc_00e216')
    e.ins('move.b','(%a1, %d3.w),%d1',4)
    e.label('gameplay_pc_00e21a')
    e.ins('move.b','%d1,%d2',2)
    e.label('gameplay_pc_00e21c')
    e.ins('move.w','(%a0)+,%d3',2)
    e.label('gameplay_pc_00e21e')
    e.ins('bmi.b','gameplay_pc_00e25a',2)
    e.label('gameplay_pc_00e220')
    e.ins('andi.w','#0xff,%d3',4)
    e.label('gameplay_pc_00e224')
    e.ins('move.b','(%a1, %d3.w),%d1',4)
    e.label('gameplay_pc_00e228')
    e.ins('cmp.b','%d2,%d1',2)
    e.label('gameplay_pc_00e22a')
    e.ins('bls.b','gameplay_pc_00e21c',2)
    e.label('gameplay_pc_00e22c')
    e.ins('move.w','%d3,%d4',2)
    e.label('gameplay_pc_00e22e')
    e.ins('move.b','%d1,%d2',2)
    e.label('gameplay_pc_00e230')
    e.ins('bra.b','gameplay_pc_00e21c',2)
    e.label('gameplay_pc_00e232')
    e.ins('lea.l','0xf427:w,%a0',4)
    e.label('gameplay_pc_00e236')
    e.ins('move.b','#0xff,(%a0, %d0.w)',6)
    e.label('gameplay_pc_00e23c')
    e.ins('lea.l','0xe80c:w,%a0',4)
    e.label('gameplay_pc_00e240')
    e.ins('move.w','%d0,%d1',2)
    e.label('gameplay_pc_00e242')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('gameplay_pc_00e244')
    e.ins('add.w','%d0,%d1',2)
    e.label('gameplay_pc_00e246')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('gameplay_pc_00e248')
    e.ins('move.w','#0xffff,(%a0, %d1.w)',6)
    e.label('gameplay_pc_00e24e')
    e.ins('move.w','#0xffff,0x4(%a0, %d1.w)',6)
    e.label('gameplay_pc_00e254')
    e.ins('move.w','#0xffff,0x8(%a0, %d1.w)',6)
    e.label('gameplay_pc_00e25a')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_00e25c')
    e.ins('lea.l','0xf45e:w,%a0',4)
    e.label('gameplay_pc_00e260')
    e.ins('move.w','%d4,(%a0, %d0.w)',4)
    e.label('gameplay_pc_00e264')
    e.ins('move.w','%d4,%d0',2)
    e.label('gameplay_pc_00e266')
    e.ins('movem.l','(%a7)+,%d1-%d5/%a0-%a2',4)
    e.label('gameplay_pc_00e26a')
    e.ins('rts','',2)

def _lower_roster_contains_force_head_carry(e,rules):
    e.label('gameplay_pc_00e26c')
    e.ins('lea.l','0xf427:w,%a2',4)
    e.label('gameplay_pc_00e270')
    e.ins('clr.w','%d5',2)
    e.label('gameplay_pc_00e272')
    e.ins('move.b','(%a2, %d0.w),%d5',4)
    e.label('gameplay_pc_00e276')
    e.ins('lsl.w','#0x1,%d5',2)
    e.label('gameplay_pc_00e278')
    e.ins('lea.l','0xe640:w,%a2',4)
    e.label('gameplay_pc_00e27c')
    e.ins('move.w','(%a2, %d5.w),%d5',4)
    e.label('gameplay_pc_00e280')
    e.ins('lea.l','0xf500:w,%a2',4)
    e.label('gameplay_pc_00e284')
    e.ins('tst.w','(%a2)',2)
    e.label('gameplay_pc_00e286')
    e.ins('bmi.w','gameplay_pc_00e298',4)
    e.label('gameplay_pc_00e28a')
    e.ins('cmp.w','(%a2)+,%d5',2)
    e.label('gameplay_pc_00e28c')
    e.ins('bne.b','gameplay_pc_00e284',2)
    e.label('gameplay_pc_00e28e')
    e.ins('move.w','%d5,%d4',2)
    e.label('gameplay_pc_00e290')
    e.ins('ori.w','#0x1,%sr',4)
    e.label('gameplay_pc_00e294')
    e.ins('bra.w','gameplay_pc_00e29c',4)
    e.label('gameplay_pc_00e298')
    e.ins('andi.w','#0xfffe,%sr',4)
    e.label('gameplay_pc_00e29c')
    e.ins('rts','',2)

def _lower_terrain_cell_query(e,rules):
    e.label('gameplay_pc_0142a2')
    e.ins('move.l','%d0,-(%a7)',2)
    e.label('gameplay_pc_0142a4')
    e.ins('move.w','%d0,%d2',2)
    e.label('gameplay_pc_0142a6')
    e.ins('lsl.w','#0x3,%d2',2)
    e.label('gameplay_pc_0142a8')
    e.ins('add.w','%d2,%d0',2)
    e.label('gameplay_pc_0142aa')
    e.ins('lsl.w','#0x3,%d0',2)
    e.label('gameplay_pc_0142ac')
    e.ins('add.w','%d1,%d0',2)
    e.label('gameplay_pc_0142ae')
    e.ins('lea.l','0xee5f0:l,%a2',6)
    e.label('gameplay_pc_0142b4')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_0142b6')
    e.ins('move.b','(%a2, %d0.w),%d2',4)
    e.label('gameplay_pc_0142ba')
    e.ins('lea.l','0x670a:l,%a2',6)
    e.label('gameplay_pc_0142c0')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_0142c2')
    e.ins('move.b','(%a2, %d2.w),%d3',4)
    e.label('gameplay_pc_0142c6')
    e.ins('move.l','(%a7)+,%d0',2)
    e.label('gameplay_pc_0142c8')
    e.ins('rts','',2)

def _lower_replenish_b200_troops(e,rules):
    e.label('gameplay_pc_016bb8')
    e.ins('lea.l','0xea37:w,%a0',4)
    e.label('gameplay_pc_016bbc')
    e.ins('lea.l','0xcc00:w,%a1',4)
    e.label('gameplay_pc_016bc0')
    e.ins('lea.l','0xb000:w,%a2',4)
    e.label('gameplay_pc_016bc4')
    e.ins('lea.l','0xb200:w,%a3',4)
    e.label('gameplay_pc_016bc8')
    e.ins('move.w','#0xff,%d0',4)
    e.label('gameplay_pc_016bcc')
    e.ins('move.b','(%a1, %d0.w),%d1',4)
    e.label('gameplay_pc_016bd0')
    e.ins('cmpi.w','#0x28,%d1',4)
    e.label('gameplay_pc_016bd4')
    e.ins('bhi.w','gameplay_pc_016c04',4)
    e.label('gameplay_pc_016bd8')
    e.ins('tst.b','(%a0, %d1.w)',4)
    e.label('gameplay_pc_016bdc')
    e.ins('bne.w','gameplay_pc_016c04',4)
    e.label('gameplay_pc_016be0')
    e.ins('move.w','%d0,%d1',2)
    e.label('gameplay_pc_016be2')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('gameplay_pc_016be4')
    e.ins('move.w','(%a2, %d1.w),%d2',4)
    e.label('gameplay_pc_016be8')
    e.ins('move.w','%d2,%d3',2)
    e.label('gameplay_pc_016bea')
    e.ins('mulu.w','#0xf,%d2',4)
    e.label('gameplay_pc_016bee')
    e.ins('divu.w','#0x64,%d2',4)
    e.label('gameplay_pc_016bf2')
    e.ins('move.w','(%a3, %d1.w),%d4',4)
    e.label('gameplay_pc_016bf6')
    e.ins('add.w','%d2,%d4',2)
    e.label('gameplay_pc_016bf8')
    e.ins('cmp.w','%d3,%d4',2)
    e.label('gameplay_pc_016bfa')
    e.ins('bls.w','gameplay_pc_016c00',4)
    e.label('gameplay_pc_016bfe')
    e.ins('move.w','%d3,%d4',2)
    e.label('gameplay_pc_016c00')
    e.ins('move.w','%d4,(%a3, %d1.w)',4)
    e.label('gameplay_pc_016c04')
    e.ins('dbra','%d0,gameplay_pc_016bcc',4)
    e.label('gameplay_pc_016c08')
    e.ins('rts','',2)

def _lower_grow_original_long_field(e,rules):
    e.label('gameplay_pc_016c0a')
    e.ins('move.l','(%a0),%d1',2)
    e.label('gameplay_pc_016c0c')
    e.ins('move.l','%d1,%d2',2)
    e.label('gameplay_pc_016c0e')
    e.ins('divu.w','#0x64,%d2',4)
    e.label('gameplay_pc_016c12')
    e.ins('andi.l','#0xffff,%d2',6)
    e.label('gameplay_pc_016c18')
    e.ins('add.l','%d2,%d1',2)
    e.label('gameplay_pc_016c1a')
    e.ins('cmpi.l','#0x3e8,%d1',6)
    e.label('gameplay_pc_016c20')
    e.ins('bls.b','gameplay_pc_016c28',2)
    e.label('gameplay_pc_016c22')
    e.ins('move.l','#0x3e8,%d1',6)
    e.label('gameplay_pc_016c28')
    e.ins('move.l','%d1,(%a0)',2)
    e.label('gameplay_pc_016c2a')
    e.ins('rts','',2)

def _lower_credit_primary(e,rules):
    e.label('gameplay_pc_016c2c')
    e.ins('lea.l','0xe280:w,%a0',4)
    e.label('gameplay_pc_016c30')
    e.ins('move.w','%d0,%d1',2)
    e.label('gameplay_pc_016c32')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('gameplay_pc_016c34')
    e.ins('move.w','#0x64,%d7',4)
    e.label('gameplay_pc_016c38')
    e.ins('sub.w','0x2(%a0, %d1.w),%d7',4)
    e.label('gameplay_pc_016c3c')
    e.ins('lea.l','0xe000:w,%a3',4)
    e.label('gameplay_pc_016c40')
    e.ins('bsr.w','gameplay_pc_016c5c',4)
    e.label('gameplay_pc_016c44')
    e.ins('rts','',2)

def _lower_credit_secondary(e,rules):
    e.label('gameplay_pc_016c46')
    e.ins('lea.l','0xe280:w,%a0',4)
    e.label('gameplay_pc_016c4a')
    e.ins('move.w','%d0,%d1',2)
    e.label('gameplay_pc_016c4c')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('gameplay_pc_016c4e')
    e.ins('move.l','(%a0, %d1.w),%d7',4)
    e.label('gameplay_pc_016c52')
    e.ins('lea.l','0xe0a0:w,%a3',4)
    e.label('gameplay_pc_016c56')
    e.ins('bsr.w','gameplay_pc_016c5c',4)
    e.label('gameplay_pc_016c5a')
    e.ins('rts','',2)

def _lower_commit_income(e,rules):
    e.label('gameplay_pc_016c5c')
    e.ins('bsr.w','gameplay_pc_016c72',4)
    e.label('gameplay_pc_016c60')
    e.ins('add.l','(%a3, %d1.w),%d3',4)
    e.label('gameplay_pc_016c64')
    e.ins('bcc.b','gameplay_pc_016c68',2)
    e.label('gameplay_pc_016c66')
    e.ins('moveq','#-1,%d3',2)
    e.label('gameplay_pc_016c68')
    e.ins('move.l','%d3,(%a3, %d1.w)',4)
    e.label('gameplay_pc_016c6c')
    e.ins('bsr.w','gameplay_pc_016c98',4)
    e.label('gameplay_pc_016c70')
    e.ins('rts','',2)

def _lower_scaled_income(e,rules):
    e.label('gameplay_pc_016c72')
    e.ins('lea.l','0xe1e0:w,%a1',4)
    e.label('gameplay_pc_016c76')
    e.ins('lea.l','0xe3c0:w,%a2',4)
    e.label('gameplay_pc_016c7a')
    e.ins('lea.l','0xe140:w,%a5',4)
    e.label('gameplay_pc_016c7e')
    e.ins('mulu.w','0x2(%a2, %d1.w),%d7',4)
    e.label('gameplay_pc_016c82')
    e.ins('mulu.w','0x2(%a1, %d1.w),%d7',4)
    e.label('gameplay_pc_016c86')
    e.ins('divu.w','#0x3a98,%d7',4)
    e.label('gameplay_pc_016c8a')
    e.ins('move.l','(%a5, %d1.w),%d3',4)
    e.label('gameplay_pc_016c8e')
    e.ins('andi.l','#0xffff,%d3',6)
    e.label('gameplay_pc_016c94')
    e.ins('mulu.w','%d7,%d3',2)
    e.label('gameplay_pc_016c96')
    e.ins('rts','',2)

def _lower_deplete_income(e,rules):
    e.label('gameplay_pc_016c98')
    e.ins('move.w','%d0,%d1',2)
    e.label('gameplay_pc_016c9a')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('gameplay_pc_016c9c')
    e.ins('move.l','(%a2, %d1.w),%d2',4)
    e.label('gameplay_pc_016ca0')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_016ca2')
    e.ins('cmpi.w','#0x2d,%d2',4)
    e.label('gameplay_pc_016ca6')
    e.ins('bls.b','gameplay_pc_016cfa',2)
    e.label('gameplay_pc_016ca8')
    e.ins('cmpi.w','#0x37,%d2',4)
    e.label('gameplay_pc_016cac')
    e.ins('bls.b','gameplay_pc_016cc8',2)
    e.label('gameplay_pc_016cae')
    e.ins('addq.w','#0x4,%d3',2)
    e.label('gameplay_pc_016cb0')
    e.ins('cmpi.w','#0x41,%d2',4)
    e.label('gameplay_pc_016cb4')
    e.ins('bls.b','gameplay_pc_016cc8',2)
    e.label('gameplay_pc_016cb6')
    e.ins('addq.w','#0x4,%d3',2)
    e.label('gameplay_pc_016cb8')
    e.ins('cmpi.w','#0x4b,%d2',4)
    e.label('gameplay_pc_016cbc')
    e.ins('bls.b','gameplay_pc_016cc8',2)
    e.label('gameplay_pc_016cbe')
    e.ins('addq.w','#0x4,%d3',2)
    e.label('gameplay_pc_016cc0')
    e.ins('cmpi.w','#0x55,%d2',4)
    e.label('gameplay_pc_016cc4')
    e.ins('bls.b','gameplay_pc_016cc8',2)
    e.label('gameplay_pc_016cc6')
    e.ins('addq.w','#0x4,%d3',2)
    e.label('gameplay_pc_016cc8')
    e.ins('move.w','%d0,%d2',2)
    e.label('gameplay_pc_016cca')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_016cd0')
    e.ins('move.w','%d2,%d0',2)
    e.label('gameplay_pc_016cd2')
    e.ins('lea.l','40(%pc),%a1',4)
    e.label('gameplay_pc_016cd6')
    e.ins('move.w','(%a1, %d3.w),%d2',4)
    e.label('gameplay_pc_016cda')
    e.ins('mulu.w','0xf61c:w,%d2',4)
    e.label('gameplay_pc_016cde')
    e.ins('swap','%d2',2)
    e.label('gameplay_pc_016ce0')
    e.ins('add.w','0x2(%a1, %d3.w),%d2',4)
    e.label('gameplay_pc_016ce4')
    e.ins('lea.l','0xe320:w,%a2',4)
    e.label('gameplay_pc_016ce8')
    e.ins('move.w','%d0,%d1',2)
    e.label('gameplay_pc_016cea')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('gameplay_pc_016cec')
    e.ins('move.w','0x2(%a2, %d1.w),%d3',4)
    e.label('gameplay_pc_016cf0')
    e.ins('mulu.w','%d2,%d3',2)
    e.label('gameplay_pc_016cf2')
    e.ins('divu.w','#0x64,%d3',4)
    e.label('gameplay_pc_016cf6')
    e.ins('sub.w','%d3,0x2(%a2, %d1.w)',4)
    e.label('gameplay_pc_016cfa')
    e.ins('rts','',2)

def _lower_debit_primary(e,rules):
    e.label('gameplay_pc_016d10')
    e.ins('lea.l','0xe280:w,%a3',4)
    e.label('gameplay_pc_016d14')
    e.ins('move.w','#0x64,%d7',4)
    e.label('gameplay_pc_016d18')
    e.ins('move.w','%d0,%d3',2)
    e.label('gameplay_pc_016d1a')
    e.ins('lsl.w','#0x2,%d3',2)
    e.label('gameplay_pc_016d1c')
    e.ins('sub.w','0x2(%a3, %d3.w),%d7',4)
    e.label('gameplay_pc_016d20')
    e.ins('lea.l','0xe000:w,%a5',4)
    e.label('gameplay_pc_016d24')
    e.ins('bsr.w','gameplay_pc_016d40',4)
    e.label('gameplay_pc_016d28')
    e.ins('rts','',2)

def _lower_debit_secondary(e,rules):
    e.label('gameplay_pc_016d2a')
    e.ins('lea.l','0xe280:w,%a3',4)
    e.label('gameplay_pc_016d2e')
    e.ins('move.w','%d0,%d1',2)
    e.label('gameplay_pc_016d30')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('gameplay_pc_016d32')
    e.ins('move.w','0x2(%a3, %d1.w),%d7',4)
    e.label('gameplay_pc_016d36')
    e.ins('lea.l','0xe0a0:w,%a5',4)
    e.label('gameplay_pc_016d3a')
    e.ins('bsr.w','gameplay_pc_016d40',4)
    e.label('gameplay_pc_016d3e')
    e.ins('rts','',2)

def _lower_settle_expense(e,rules):
    e.label('gameplay_pc_016d40')
    e.ins('lea.l','0xc700:w,%a4',4)
    e.label('gameplay_pc_016d44')
    e.ins('addq.w','#0x1,%d0',2)
    e.label('gameplay_pc_016d46')
    e.ins('move.w','#0xffff,0xf630:w',6)
    e.label('gameplay_pc_016d4c')
    e.ins('jsr','gameplay_pc_005f48:l',6)
    e.label('gameplay_pc_016d52')
    e.ins('move.w','%d3,0xf636:w',4)
    e.label('gameplay_pc_016d56')
    e.ins('subq.w','#0x1,%d0',2)
    e.label('gameplay_pc_016d58')
    e.ins('lea.l','0xc800:w,%a0',4)
    e.label('gameplay_pc_016d5c')
    e.ins('lea.l','0xf500:w,%a1',4)
    e.label('gameplay_pc_016d60')
    e.ins('moveq','#0,%d1',2)
    e.label('gameplay_pc_016d62')
    e.ins('move.w','(%a1)+,%d2',2)
    e.label('gameplay_pc_016d64')
    e.ins('bmi.b','gameplay_pc_016d6e',2)
    e.label('gameplay_pc_016d66')
    e.ins('lsl.w','#0x2,%d2',2)
    e.label('gameplay_pc_016d68')
    e.ins('add.l','(%a0, %d2.w),%d1',4)
    e.label('gameplay_pc_016d6c')
    e.ins('bra.b','gameplay_pc_016d62',2)
    e.label('gameplay_pc_016d6e')
    e.ins('move.l','%d1,%d3',2)
    e.label('gameplay_pc_016d70')
    e.ins('mulu.w','%d7,%d1',2)
    e.label('gameplay_pc_016d72')
    e.ins('swap','%d3',2)
    e.label('gameplay_pc_016d74')
    e.ins('mulu.w','%d7,%d3',2)
    e.label('gameplay_pc_016d76')
    e.ins('swap','%d3',2)
    e.label('gameplay_pc_016d78')
    e.ins('add.l','%d3,%d1',2)
    e.label('gameplay_pc_016d7a')
    e.ins('divu.w','#0x1388,%d1',4)
    e.label('gameplay_pc_016d7e')
    e.ins('lea.l','0xf500:w,%a0',4)
    e.label('gameplay_pc_016d82')
    e.ins('lea.l','92(%pc),%a1',4)
    e.label('gameplay_pc_016d86')
    e.ins('nop','',2)
    e.label('gameplay_pc_016d88')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_016d8a')
    e.ins('move.w','(%a0)+,%d3',2)
    e.label('gameplay_pc_016d8c')
    e.ins('bmi.b','gameplay_pc_016d9e',2)
    e.label('gameplay_pc_016d8e')
    e.ins('move.b','(%a4, %d3.w),%d4',4)
    e.label('gameplay_pc_016d92')
    e.ins('andi.w','#0x5,%d4',4)
    e.label('gameplay_pc_016d96')
    e.ins('lsl.w','#0x1,%d4',2)
    e.label('gameplay_pc_016d98')
    e.ins('add.w','(%a1, %d4.w),%d2',4)
    e.label('gameplay_pc_016d9c')
    e.ins('bra.b','gameplay_pc_016d8a',2)
    e.label('gameplay_pc_016d9e')
    e.ins('mulu.w','%d7,%d2',2)
    e.label('gameplay_pc_016da0')
    e.ins('divu.w','#0x64,%d2',4)
    e.label('gameplay_pc_016da4')
    e.ins('andi.l','#0xffff,%d1',6)
    e.label('gameplay_pc_016daa')
    e.ins('andi.l','#0xffff,%d2',6)
    e.label('gameplay_pc_016db0')
    e.ins('add.l','%d1,%d2',2)
    e.label('gameplay_pc_016db2')
    e.ins('move.w','%d0,%d3',2)
    e.label('gameplay_pc_016db4')
    e.ins('lsl.w','#0x2,%d3',2)
    e.label('gameplay_pc_016db6')
    e.ins('move.l','(%a5, %d3.w),%d4',4)
    e.label('gameplay_pc_016dba')
    e.ins('sub.l','%d2,%d4',2)
    e.label('gameplay_pc_016dbc')
    e.ins('bcc.w','gameplay_pc_016dc8',4)
    e.label('gameplay_pc_016dc0')
    e.ins('bsr.w','gameplay_pc_016dea',4)
    e.label('gameplay_pc_016dc4')
    e.ins('moveq','#0,%d4',2)
    e.label('gameplay_pc_016dc6')
    e.ins('bra.b','gameplay_pc_016dd6',2)
    e.label('gameplay_pc_016dc8')
    e.ins('cmpi.l','#0xf423f,%d4',6)
    e.label('gameplay_pc_016dce')
    e.ins('bls.b','gameplay_pc_016dd6',2)
    e.label('gameplay_pc_016dd0')
    e.ins('move.l','#0xf423f,%d4',6)
    e.label('gameplay_pc_016dd6')
    e.ins('move.w','%d0,%d3',2)
    e.label('gameplay_pc_016dd8')
    e.ins('lsl.w','#0x2,%d3',2)
    e.label('gameplay_pc_016dda')
    e.ins('move.l','%d4,(%a5, %d3.w)',4)
    e.label('gameplay_pc_016dde')
    e.ins('rts','',2)

def _lower_settle_shortage(e,rules):
    e.label('gameplay_pc_016dea')
    e.ins('neg.l','%d4',2)
    e.label('gameplay_pc_016dec')
    e.ins('move.l','%d4,%d5',2)
    e.label('gameplay_pc_016dee')
    e.ins('mulu.w','%d7,%d4',2)
    e.label('gameplay_pc_016df0')
    e.ins('swap','%d5',2)
    e.label('gameplay_pc_016df2')
    e.ins('mulu.w','%d7,%d5',2)
    e.label('gameplay_pc_016df4')
    e.ins('swap','%d5',2)
    e.label('gameplay_pc_016df6')
    e.ins('add.l','%d5,%d4',2)
    e.label('gameplay_pc_016df8')
    e.ins('lea.l','0xf500:w,%a0',4)
    e.label('gameplay_pc_016dfc')
    e.ins('lea.l','0xea60:w,%a1',4)
    e.label('gameplay_pc_016e00')
    e.ins('lea.l','0xbe00:w,%a2',4)
    e.label('gameplay_pc_016e04')
    e.ins('lea.l','0xc000:w,%a3',4)
    e.label('gameplay_pc_016e08')
    e.ins('move.w','(%a0)+,%d1',2)
    e.label('gameplay_pc_016e0a')
    e.ins('bmi.b','gameplay_pc_016e20',2)
    e.label('gameplay_pc_016e0c')
    e.ins('moveq','#0,%d2',2)
    e.label('gameplay_pc_016e0e')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('gameplay_pc_016e10')
    e.ins('move.w','(%a2, %d1.w),%d2',4)
    e.label('gameplay_pc_016e14')
    e.ins('moveq','#0,%d3',2)
    e.label('gameplay_pc_016e16')
    e.ins('move.w','(%a3, %d1.w),%d3',4)
    e.label('gameplay_pc_016e1a')
    e.ins('add.l','%d2,%d3',2)
    e.label('gameplay_pc_016e1c')
    e.ins('move.l','%d3,(%a1)+',2)
    e.label('gameplay_pc_016e1e')
    e.ins('bra.b','gameplay_pc_016e08',2)
    e.label('gameplay_pc_016e20')
    e.ins('lea.l','0xea60:w,%a0',4)
    e.label('gameplay_pc_016e24')
    e.ins('lea.l','0xf500:w,%a1',4)
    e.label('gameplay_pc_016e28')
    e.ins('move.w','0xf636:w,%d1',4)
    e.label('gameplay_pc_016e2c')
    e.ins('cmpi.w','#0x1,%d1',4)
    e.label('gameplay_pc_016e30')
    e.ins('bls.b','gameplay_pc_016e6a',2)
    e.label('gameplay_pc_016e32')
    e.ins('subq.w','#0x1,%d1',2)
    e.label('gameplay_pc_016e34')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_016e36')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_016e38')
    e.ins('clr.w','%d5',2)
    e.label('gameplay_pc_016e3a')
    e.ins('move.l','(%a0, %d5.w),%d6',4)
    e.label('gameplay_pc_016e3e')
    e.ins('cmp.l','0x4(%a0, %d5.w),%d6',4)
    e.label('gameplay_pc_016e42')
    e.ins('bls.b','gameplay_pc_016e5c',2)
    e.label('gameplay_pc_016e44')
    e.ins('move.l','0x4(%a0, %d5.w),(%a0, %d5.w)',6)
    e.label('gameplay_pc_016e4a')
    e.ins('move.l','%d6,0x4(%a0, %d5.w)',4)
    e.label('gameplay_pc_016e4e')
    e.ins('move.w','(%a1, %d3.w),%d6',4)
    e.label('gameplay_pc_016e52')
    e.ins('move.w','0x2(%a1, %d3.w),(%a1, %d3.w)',6)
    e.label('gameplay_pc_016e58')
    e.ins('move.w','%d6,0x2(%a1, %d3.w)',4)
    e.label('gameplay_pc_016e5c')
    e.ins('addq.w','#0x1,%d2',2)
    e.label('gameplay_pc_016e5e')
    e.ins('addq.w','#0x2,%d3',2)
    e.label('gameplay_pc_016e60')
    e.ins('addq.w','#0x4,%d5',2)
    e.label('gameplay_pc_016e62')
    e.ins('cmp.w','%d1,%d2',2)
    e.label('gameplay_pc_016e64')
    e.ins('bcs.b','gameplay_pc_016e3a',2)
    e.label('gameplay_pc_016e66')
    e.ins('subq.w','#0x1,%d1',2)
    e.label('gameplay_pc_016e68')
    e.ins('bne.b','gameplay_pc_016e34',2)
    e.label('gameplay_pc_016e6a')
    e.ins('lea.l','0xf500:w,%a0',4)
    e.label('gameplay_pc_016e6e')
    e.ins('lea.l','0xc800:w,%a1',4)
    e.label('gameplay_pc_016e72')
    e.ins('lea.l','0xc200:w,%a2',4)
    e.label('gameplay_pc_016e76')
    e.ins('move.w','(%a0)+,%d1',2)
    e.label('gameplay_pc_016e78')
    e.ins('bmi.b','gameplay_pc_016eae',2)
    e.label('gameplay_pc_016e7a')
    e.ins('move.w','%d1,%d3',2)
    e.label('gameplay_pc_016e7c')
    e.ins('lsl.w','#0x2,%d3',2)
    e.label('gameplay_pc_016e7e')
    e.ins('move.l','(%a1, %d3.w),%d2',4)
    e.label('gameplay_pc_016e82')
    e.ins('cmp.l','%d4,%d2',2)
    e.label('gameplay_pc_016e84')
    e.ins('bls.b','gameplay_pc_016e8c',2)
    e.label('gameplay_pc_016e86')
    e.ins('move.l','%d4,%d6',2)
    e.label('gameplay_pc_016e88')
    e.ins('clr.w','%d4',2)
    e.label('gameplay_pc_016e8a')
    e.ins('bra.b','gameplay_pc_016e90',2)
    e.label('gameplay_pc_016e8c')
    e.ins('sub.l','%d2,%d4',2)
    e.label('gameplay_pc_016e8e')
    e.ins('move.l','%d2,%d6',2)
    e.label('gameplay_pc_016e90')
    e.ins('move.w','#0x64,%d5',4)
    e.label('gameplay_pc_016e94')
    e.ins('sub.b','(%a2, %d1.w),%d5',4)
    e.label('gameplay_pc_016e98')
    e.ins('mulu.w','%d5,%d6',2)
    e.label('gameplay_pc_016e9a')
    e.ins('divu.w','#0x64,%d6',4)
    e.label('gameplay_pc_016e9e')
    e.ins('andi.l','#0xffff,%d6',6)
    e.label('gameplay_pc_016ea4')
    e.ins('sub.l','%d6,%d2',2)
    e.label('gameplay_pc_016ea6')
    e.ins('move.l','%d2,(%a1, %d3.w)',4)
    e.label('gameplay_pc_016eaa')
    e.ins('tst.l','%d4',2)
    e.label('gameplay_pc_016eac')
    e.ins('bne.b','gameplay_pc_016e76',2)
    e.label('gameplay_pc_016eae')
    e.ins('tst.l','%d4',2)
    e.label('gameplay_pc_016eb0')
    e.ins('beq.b','gameplay_pc_016ed8',2)
    e.label('gameplay_pc_016eb2')
    e.ins('lea.l','0xf500:w,%a0',4)
    e.label('gameplay_pc_016eb6')
    e.ins('lea.l','0xc200:w,%a1',4)
    e.label('gameplay_pc_016eba')
    e.ins('lea.l','0xc300:w,%a2',4)
    e.label('gameplay_pc_016ebe')
    e.ins('move.w','(%a0)+,%d1',2)
    e.label('gameplay_pc_016ec0')
    e.ins('bmi.b','gameplay_pc_016ed8',2)
    e.label('gameplay_pc_016ec2')
    e.ins('moveq','#100,%d2',2)
    e.label('gameplay_pc_016ec4')
    e.ins('sub.b','(%a1, %d1.w),%d2',4)
    e.label('gameplay_pc_016ec8')
    e.ins('divu.w','#0xa,%d2',4)
    e.label('gameplay_pc_016ecc')
    e.ins('sub.b','%d2,(%a2, %d1.w)',4)
    e.label('gameplay_pc_016ed0')
    e.ins('bcc.b','gameplay_pc_016ebe',2)
    e.label('gameplay_pc_016ed2')
    e.ins('clr.b','(%a2, %d1.w)',4)
    e.label('gameplay_pc_016ed6')
    e.ins('bra.b','gameplay_pc_016ebe',2)
    e.label('gameplay_pc_016ed8')
    e.ins('rts','',2)

def _lower_reset_queue(e,rules):
    e.label('gameplay_pc_017016')
    e.ins('moveq','#41,%d0',2)
    e.label('gameplay_pc_017018')
    e.ins('lea.l','0xd420:w,%a0',4)
    e.label('gameplay_pc_01701c')
    e.ins('move.b','#0xff,(%a0)+',4)
    e.label('gameplay_pc_017020')
    e.ins('dbra','%d0,gameplay_pc_01701c',4)
    e.label('gameplay_pc_017024')
    e.ins('rts','',2)

def _lower_append_queue(e,rules):
    e.label('gameplay_pc_017026')
    e.ins('lea.l','0xf428:w,%a0',4)
    e.label('gameplay_pc_01702a')
    e.ins('move.b','(%a0, %d7.w),%d0',4)
    e.label('gameplay_pc_01702e')
    e.ins('bmi.b','gameplay_pc_017048',2)
    e.label('gameplay_pc_017030')
    e.ins('cmp.w','0xf67a:w,%d0',4)
    e.label('gameplay_pc_017034')
    e.ins('beq.b','gameplay_pc_017042',2)
    e.label('gameplay_pc_017036')
    e.ins('cmp.w','0xf67c:w,%d0',4)
    e.label('gameplay_pc_01703a')
    e.ins('beq.b','gameplay_pc_017042',2)
    e.label('gameplay_pc_01703c')
    e.ins('cmp.w','0xf67e:w,%d0',4)
    e.label('gameplay_pc_017040')
    e.ins('bne.b','gameplay_pc_017048',2)
    e.label('gameplay_pc_017042')
    e.ins('move.w','#0x0,0xd448:w',6)
    e.label('gameplay_pc_017048')
    e.ins('lea.l','0xd420:w,%a0',4)
    e.label('gameplay_pc_01704c')
    e.ins('cmpi.b','#0xff,(%a0)+',4)
    e.label('gameplay_pc_017050')
    e.ins('bne.b','gameplay_pc_01704c',2)
    e.label('gameplay_pc_017052')
    e.ins('tst.b','-(%a0)',2)
    e.label('gameplay_pc_017054')
    e.ins('move.b','%d7,(%a0)',2)
    e.label('gameplay_pc_017056')
    e.ins('rts','',2)

def _lower_submit_three_fields(e,rules):
    e.label('gameplay_pc_0171a6')
    e.ins('lea.l','0xf428:w,%a0',4)
    e.label('gameplay_pc_0171aa')
    e.ins('move.b','(%a0, %d0.w),%d7',4)
    e.label('gameplay_pc_0171ae')
    e.ins('bmi.b','gameplay_pc_0171fa',2)
    e.label('gameplay_pc_0171b0')
    e.ins('move.w','%d0,%d7',2)
    e.label('gameplay_pc_0171b2')
    e.ins('jsr','996(%pc)',4)
    e.label('gameplay_pc_0171b6')
    e.ins('nop','',2)
    e.label('gameplay_pc_0171b8')
    e.ins('andi.w','#0xf,%d0',4)
    e.label('gameplay_pc_0171bc')
    e.ins('bne.w','gameplay_pc_0171f8',4)
    e.label('gameplay_pc_0171c0')
    e.ins('bsr.w','gameplay_pc_017026',4)
    e.label('gameplay_pc_0171c4')
    e.ins('movem.l','%d7,-(%a7)',4)
    e.label('gameplay_pc_0171c8')
    e.ins('asl.w','#0x2,%d7',2)
    e.label('gameplay_pc_0171ca')
    e.ins('jsr','1014(%pc)',4)
    e.label('gameplay_pc_0171ce')
    e.ins('nop','',2)
    e.label('gameplay_pc_0171d0')
    e.ins('addi.w','#0x50,%d0',4)
    e.label('gameplay_pc_0171d4')
    e.ins('bsr.w','gameplay_pc_017514',4)
    e.label('gameplay_pc_0171d8')
    e.ins('jsr','974(%pc)',4)
    e.label('gameplay_pc_0171dc')
    e.ins('nop','',2)
    e.label('gameplay_pc_0171de')
    e.ins('addi.w','#0x5f,%d0',4)
    e.label('gameplay_pc_0171e2')
    e.ins('bsr.w','gameplay_pc_01752a',4)
    e.label('gameplay_pc_0171e6')
    e.ins('jsr','986(%pc)',4)
    e.label('gameplay_pc_0171ea')
    e.ins('nop','',2)
    e.label('gameplay_pc_0171ec')
    e.ins('addi.w','#0x55,%d0',4)
    e.label('gameplay_pc_0171f0')
    e.ins('bsr.w','gameplay_pc_017540',4)
    e.label('gameplay_pc_0171f4')
    e.ins('movem.l','(%a7)+,%d7',4)
    e.label('gameplay_pc_0171f8')
    e.ins('move.w','%d7,%d0',2)
    e.label('gameplay_pc_0171fa')
    e.ins('rts','',2)

def _lower_submit_four_fields(e,rules):
    e.label('gameplay_pc_017342')
    e.ins('lea.l','0xf428:w,%a0',4)
    e.label('gameplay_pc_017346')
    e.ins('move.b','(%a0, %d0.w),%d7',4)
    e.label('gameplay_pc_01734a')
    e.ins('bmi.b','gameplay_pc_0173a2',2)
    e.label('gameplay_pc_01734c')
    e.ins('move.w','%d0,%d7',2)
    e.label('gameplay_pc_01734e')
    e.ins('jsr','584(%pc)',4)
    e.label('gameplay_pc_017352')
    e.ins('nop','',2)
    e.label('gameplay_pc_017354')
    e.ins('andi.w','#0xf,%d0',4)
    e.label('gameplay_pc_017358')
    e.ins('bne.w','gameplay_pc_0173a2',4)
    e.label('gameplay_pc_01735c')
    e.ins('bsr.w','gameplay_pc_017026',4)
    e.label('gameplay_pc_017360')
    e.ins('movem.l','%d7,-(%a7)',4)
    e.label('gameplay_pc_017364')
    e.ins('asl.w','#0x2,%d7',2)
    e.label('gameplay_pc_017366')
    e.ins('jsr','602(%pc)',4)
    e.label('gameplay_pc_01736a')
    e.ins('nop','',2)
    e.label('gameplay_pc_01736c')
    e.ins('addi.w','#0x50,%d0',4)
    e.label('gameplay_pc_017370')
    e.ins('bsr.w','gameplay_pc_017514',4)
    e.label('gameplay_pc_017374')
    e.ins('jsr','562(%pc)',4)
    e.label('gameplay_pc_017378')
    e.ins('nop','',2)
    e.label('gameplay_pc_01737a')
    e.ins('addi.w','#0x5f,%d0',4)
    e.label('gameplay_pc_01737e')
    e.ins('bsr.w','gameplay_pc_01752a',4)
    e.label('gameplay_pc_017382')
    e.ins('jsr','574(%pc)',4)
    e.label('gameplay_pc_017386')
    e.ins('nop','',2)
    e.label('gameplay_pc_017388')
    e.ins('addi.w','#0x55,%d0',4)
    e.label('gameplay_pc_01738c')
    e.ins('bsr.w','gameplay_pc_017540',4)
    e.label('gameplay_pc_017390')
    e.ins('jsr','560(%pc)',4)
    e.label('gameplay_pc_017394')
    e.ins('nop','',2)
    e.label('gameplay_pc_017396')
    e.ins('addi.w','#0x50,%d0',4)
    e.label('gameplay_pc_01739a')
    e.ins('bsr.w','gameplay_pc_01756c',4)
    e.label('gameplay_pc_01739e')
    e.ins('movem.l','(%a7)+,%d7',4)
    e.label('gameplay_pc_0173a2')
    e.ins('move.w','%d7,%d0',2)
    e.label('gameplay_pc_0173a4')
    e.ins('rts','',2)

def _lower_submit_classified_fields(e,rules):
    e.label('gameplay_pc_017474')
    e.ins('move.w','%d0,%d7',2)
    e.label('gameplay_pc_017476')
    e.ins('asl.w','#0x2,%d0',2)
    e.label('gameplay_pc_017478')
    e.ins('lea.l','0xe320:w,%a0',4)
    e.label('gameplay_pc_01747c')
    e.ins('moveq','#0,%d3',2)
    e.label('gameplay_pc_01747e')
    e.ins('move.l','(%a0, %d0.w),%d2',4)
    e.label('gameplay_pc_017482')
    e.ins('divu.w','#0xa,%d2',4)
    e.label('gameplay_pc_017486')
    e.ins('move.b','104(%pc, %d2.w),%d3',4)
    e.label('gameplay_pc_01748a')
    e.ins('cmpi.w','#0x7,%d2',4)
    e.label('gameplay_pc_01748e')
    e.ins('bcc.w','gameplay_pc_0174ec',4)
    e.label('gameplay_pc_017492')
    e.ins('jsr','260(%pc)',4)
    e.label('gameplay_pc_017496')
    e.ins('nop','',2)
    e.label('gameplay_pc_017498')
    e.ins('and.w','%d3,%d0',2)
    e.label('gameplay_pc_01749a')
    e.ins('bne.w','gameplay_pc_0174ec',4)
    e.label('gameplay_pc_01749e')
    e.ins('bsr.w','gameplay_pc_017026',4)
    e.label('gameplay_pc_0174a2')
    e.ins('movem.l','%d7,-(%a7)',4)
    e.label('gameplay_pc_0174a6')
    e.ins('asl.w','#0x2,%d7',2)
    e.label('gameplay_pc_0174a8')
    e.ins('moveq','#0,%d3',2)
    e.label('gameplay_pc_0174aa')
    e.ins('move.b','80(%pc, %d2.w),%d3',4)
    e.label('gameplay_pc_0174ae')
    e.ins('moveq','#0,%d0',2)
    e.label('gameplay_pc_0174b0')
    e.ins('cmpi.w','#0x7,%d2',4)
    e.label('gameplay_pc_0174b4')
    e.ins('bcc.b','gameplay_pc_0174c8',2)
    e.label('gameplay_pc_0174b6')
    e.ins('jsr','266(%pc)',4)
    e.label('gameplay_pc_0174ba')
    e.ins('nop','',2)
    e.label('gameplay_pc_0174bc')
    e.ins('cmpi.w','#0x6,%d2',4)
    e.label('gameplay_pc_0174c0')
    e.ins('bcs.b','gameplay_pc_0174c8',2)
    e.label('gameplay_pc_0174c2')
    e.ins('jsr','228(%pc)',4)
    e.label('gameplay_pc_0174c6')
    e.ins('nop','',2)
    e.label('gameplay_pc_0174c8')
    e.ins('add.w','%d3,%d0',2)
    e.label('gameplay_pc_0174ca')
    e.ins('bsr.w','gameplay_pc_017514',4)
    e.label('gameplay_pc_0174ce')
    e.ins('bsr.w','gameplay_pc_017556',4)
    e.label('gameplay_pc_0174d2')
    e.ins('bsr.w','gameplay_pc_01756c',4)
    e.label('gameplay_pc_0174d6')
    e.ins('bsr.w','gameplay_pc_017582',4)
    e.label('gameplay_pc_0174da')
    e.ins('jsr','204(%pc)',4)
    e.label('gameplay_pc_0174de')
    e.ins('nop','',2)
    e.label('gameplay_pc_0174e0')
    e.ins('addi.w','#0x5f,%d0',4)
    e.label('gameplay_pc_0174e4')
    e.ins('bsr.w','gameplay_pc_01752a',4)
    e.label('gameplay_pc_0174e8')
    e.ins('movem.l','(%a7)+,%d7',4)
    e.label('gameplay_pc_0174ec')
    e.ins('move.w','%d7,%d0',2)
    e.label('gameplay_pc_0174ee')
    e.ins('rts','',2)

def _lower_scale_e1e0(e,rules):
    e.label('gameplay_pc_017514')
    e.ins('lea.l','0xe1e0:w,%a0',4)
    e.label('gameplay_pc_017518')
    e.ins('move.l','(%a0, %d7.w),%d2',4)
    e.label('gameplay_pc_01751c')
    e.ins('bsr.w','gameplay_pc_0175dc',4)
    e.label('gameplay_pc_017520')
    e.ins('bsr.w','gameplay_pc_0175ec',4)
    e.label('gameplay_pc_017524')
    e.ins('move.l','%d2,(%a0, %d7.w)',4)
    e.label('gameplay_pc_017528')
    e.ins('rts','',2)

def _lower_scale_e140(e,rules):
    e.label('gameplay_pc_01752a')
    e.ins('lea.l','0xe140:w,%a0',4)
    e.label('gameplay_pc_01752e')
    e.ins('move.l','(%a0, %d7.w),%d2',4)
    e.label('gameplay_pc_017532')
    e.ins('bsr.w','gameplay_pc_0175dc',4)
    e.label('gameplay_pc_017536')
    e.ins('bsr.w','gameplay_pc_0175ec',4)
    e.label('gameplay_pc_01753a')
    e.ins('move.l','%d2,(%a0, %d7.w)',4)
    e.label('gameplay_pc_01753e')
    e.ins('rts','',2)

def _lower_scale_e320(e,rules):
    e.label('gameplay_pc_017540')
    e.ins('lea.l','0xe320:w,%a0',4)
    e.label('gameplay_pc_017544')
    e.ins('move.l','(%a0, %d7.w),%d2',4)
    e.label('gameplay_pc_017548')
    e.ins('bsr.w','gameplay_pc_0175dc',4)
    e.label('gameplay_pc_01754c')
    e.ins('bsr.w','gameplay_pc_0175ec',4)
    e.label('gameplay_pc_017550')
    e.ins('move.l','%d2,(%a0, %d7.w)',4)
    e.label('gameplay_pc_017554')
    e.ins('rts','',2)

def _lower_scale_e000(e,rules):
    e.label('gameplay_pc_017556')
    e.ins('lea.l','0xe000:w,%a0',4)
    e.label('gameplay_pc_01755a')
    e.ins('move.l','(%a0, %d7.w),%d2',4)
    e.label('gameplay_pc_01755e')
    e.ins('bsr.w','gameplay_pc_0175dc',4)
    e.label('gameplay_pc_017562')
    e.ins('bsr.w','gameplay_pc_0175ec',4)
    e.label('gameplay_pc_017566')
    e.ins('move.l','%d2,(%a0, %d7.w)',4)
    e.label('gameplay_pc_01756a')
    e.ins('rts','',2)

def _lower_scale_e0a0(e,rules):
    e.label('gameplay_pc_01756c')
    e.ins('lea.l','0xe0a0:w,%a0',4)
    e.label('gameplay_pc_017570')
    e.ins('move.l','(%a0, %d7.w),%d2',4)
    e.label('gameplay_pc_017574')
    e.ins('bsr.w','gameplay_pc_0175dc',4)
    e.label('gameplay_pc_017578')
    e.ins('bsr.w','gameplay_pc_0175ec',4)
    e.label('gameplay_pc_01757c')
    e.ins('move.l','%d2,(%a0, %d7.w)',4)
    e.label('gameplay_pc_017580')
    e.ins('rts','',2)

def _lower_scale_e5a0(e,rules):
    e.label('gameplay_pc_017582')
    e.ins('lea.l','0xe5a0:w,%a0',4)
    e.label('gameplay_pc_017586')
    e.ins('move.l','(%a0, %d7.w),%d2',4)
    e.label('gameplay_pc_01758a')
    e.ins('bsr.w','gameplay_pc_0175dc',4)
    e.label('gameplay_pc_01758e')
    e.ins('bsr.w','gameplay_pc_0175ec',4)
    e.label('gameplay_pc_017592')
    e.ins('move.l','%d2,(%a0, %d7.w)',4)
    e.label('gameplay_pc_017596')
    e.ins('rts','',2)

def _lower_sample_once(e,rules):
    e.label('gameplay_pc_017598')
    e.ins('movem.l','%d1,-(%a7)',4)
    e.label('gameplay_pc_01759c')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_0175a2')
    e.ins('movem.l','(%a7)+,%d1',4)
    e.label('gameplay_pc_0175a6')
    e.ins('rts','',2)

def _lower_sample_small(e,rules):
    e.label('gameplay_pc_0175a8')
    e.ins('movem.l','%d1,-(%a7)',4)
    e.label('gameplay_pc_0175ac')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_0175b2')
    e.ins('andi.w','#0x7,%d0',4)
    e.label('gameplay_pc_0175b6')
    e.ins('cmpi.w','#0x5,%d0',4)
    e.label('gameplay_pc_0175ba')
    e.ins('bcc.b','gameplay_pc_0175ac',2)
    e.label('gameplay_pc_0175bc')
    e.ins('movem.l','(%a7)+,%d1',4)
    e.label('gameplay_pc_0175c0')
    e.ins('rts','',2)

def _lower_sample_wide(e,rules):
    e.label('gameplay_pc_0175c2')
    e.ins('movem.l','%d1,-(%a7)',4)
    e.label('gameplay_pc_0175c6')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_0175cc')
    e.ins('andi.w','#0xf,%d0',4)
    e.label('gameplay_pc_0175d0')
    e.ins('cmpi.w','#0xa,%d0',4)
    e.label('gameplay_pc_0175d4')
    e.ins('bcc.b','gameplay_pc_0175c6',2)
    e.label('gameplay_pc_0175d6')
    e.ins('movem.l','(%a7)+,%d1',4)
    e.label('gameplay_pc_0175da')
    e.ins('rts','',2)

def _lower_wrapped_product(e,rules):
    e.label('gameplay_pc_0175dc')
    e.ins('move.l','%d2,%d4',2)
    e.label('gameplay_pc_0175de')
    e.ins('swap','%d4',2)
    e.label('gameplay_pc_0175e0')
    e.ins('mulu.w','%d0,%d4',2)
    e.label('gameplay_pc_0175e2')
    e.ins('swap','%d4',2)
    e.label('gameplay_pc_0175e4')
    e.ins('clr.w','%d4',2)
    e.label('gameplay_pc_0175e6')
    e.ins('mulu.w','%d0,%d2',2)
    e.label('gameplay_pc_0175e8')
    e.ins('add.l','%d4,%d2',2)
    e.label('gameplay_pc_0175ea')
    e.ins('rts','',2)

def _lower_divide_percent(e,rules):
    e.label('gameplay_pc_0175ec')
    e.ins('movem.l','%d1,-(%a7)',4)
    e.label('gameplay_pc_0175f0')
    e.ins('move.l','%d2,%d1',2)
    e.label('gameplay_pc_0175f2')
    e.ins('moveq','#100,%d2',2)
    e.label('gameplay_pc_0175f4')
    e.ins('jsr','gameplay_pc_035760:l',6)
    e.label('gameplay_pc_0175fa')
    e.ins('move.l','%d1,%d2',2)
    e.label('gameplay_pc_0175fc')
    e.ins('movem.l','(%a7)+,%d1',4)
    e.label('gameplay_pc_017600')
    e.ins('rts','',2)

def _lower_sum_group_troops(e,rules):
    e.label('gameplay_pc_0179be')
    e.ins('moveq','#0,%d0',2)
    e.label('gameplay_pc_0179c0')
    e.ins('clr.w','%d1',2)
    e.label('gameplay_pc_0179c2')
    e.ins('move.w','(%a1)+,%d2',2)
    e.label('gameplay_pc_0179c4')
    e.ins('bmi.b','gameplay_pc_0179d4',2)
    e.label('gameplay_pc_0179c6')
    e.ins('andi.w','#0xff,%d2',4)
    e.label('gameplay_pc_0179ca')
    e.ins('addq.w','#0x1,%d1',2)
    e.label('gameplay_pc_0179cc')
    e.ins('lsl.w','#0x2,%d2',2)
    e.label('gameplay_pc_0179ce')
    e.ins('add.l','(%a0, %d2.w),%d0',4)
    e.label('gameplay_pc_0179d2')
    e.ins('bra.b','gameplay_pc_0179c2',2)
    e.label('gameplay_pc_0179d4')
    e.ins('rts','',2)

def _lower_find_group_at_coordinate(e,rules):
    e.label('gameplay_pc_017d10')
    e.ins('clr.w','%d1',2)
    e.label('gameplay_pc_017d12')
    e.ins('move.b','%d0,%d1',2)
    e.label('gameplay_pc_017d14')
    e.ins('lsr.w','#0x8,%d0',2)
    e.label('gameplay_pc_017d16')
    e.ins('lea.l','0x9000:w,%a0',4)
    e.label('gameplay_pc_017d1a')
    e.ins('move.b','(%a0),%d2',2)
    e.label('gameplay_pc_017d1c')
    e.ins('andi.w','#0xf,%d2',4)
    e.label('gameplay_pc_017d20')
    e.ins('beq.w','gameplay_pc_017d3a',4)
    e.label('gameplay_pc_017d24')
    e.ins('cmp.b','0x1(%a0),%d0',4)
    e.label('gameplay_pc_017d28')
    e.ins('bne.w','gameplay_pc_017d34',4)
    e.label('gameplay_pc_017d2c')
    e.ins('cmp.b','0x2(%a0),%d1',4)
    e.label('gameplay_pc_017d30')
    e.ins('beq.w','gameplay_pc_017d3a',4)
    e.label('gameplay_pc_017d34')
    e.ins('lea.l','0xd(%a0, %d2.w),%a0',4)
    e.label('gameplay_pc_017d38')
    e.ins('bra.b','gameplay_pc_017d1a',2)
    e.label('gameplay_pc_017d3a')
    e.ins('rts','',2)

def _lower_settle_duel_training_and_troops(e,rules):
    e.label('gameplay_pc_0188a6')
    e.ins('lea.l','0xc500:w,%a0',4)
    e.label('gameplay_pc_0188aa')
    e.ins('lea.l','0xb200:w,%a1',4)
    e.label('gameplay_pc_0188ae')
    e.ins('lea.l','0xc800:w,%a2',4)
    e.label('gameplay_pc_0188b2')
    e.ins('lea.l','0xc000:w,%a3',4)
    e.label('gameplay_pc_0188b6')
    e.ins('lea.l','0xbe00:w,%a4',4)
    e.label('gameplay_pc_0188ba')
    e.ins('move.w','0xffff80e0:l,%d0',6)
    e.label('gameplay_pc_0188c0')
    e.ins('move.b','0xffff8101:l,%d2',6)
    e.label('gameplay_pc_0188c6')
    e.ins('cmpi.w','#0x4,0xffff8114:l',8)
    e.label('gameplay_pc_0188ce')
    e.ins('bne.w','gameplay_pc_0188f4',4)
    e.label('gameplay_pc_0188d2')
    e.ins('move.w','%d0,-(%a7)',2)
    e.label('gameplay_pc_0188d4')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_0188da')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_0188e0')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_0188e2')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_0188e4')
    e.ins('add.w','%d1,%d0',2)
    e.label('gameplay_pc_0188e6')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_0188e8')
    e.ins('addq.w','#0x1,%d0',2)
    e.label('gameplay_pc_0188ea')
    e.ins('sub.w','%d0,%d2',2)
    e.label('gameplay_pc_0188ec')
    e.ins('bcc.w','gameplay_pc_0188f2',4)
    e.label('gameplay_pc_0188f0')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_0188f2')
    e.ins('move.w','(%a7)+,%d0',2)
    e.label('gameplay_pc_0188f4')
    e.ins('move.b','%d2,(%a0, %d0.w)',4)
    e.label('gameplay_pc_0188f8')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_0188fa')
    e.ins('move.w','0xffff810c:l,(%a1, %d0.w)',8)
    e.label('gameplay_pc_018902')
    e.ins('bne.w','gameplay_pc_01891a',4)
    e.label('gameplay_pc_018906')
    e.ins('move.w','0xffff80e2:l,%d1',6)
    e.label('gameplay_pc_01890c')
    e.ins('bsr.w','gameplay_pc_0189d4',4)
    e.label('gameplay_pc_018910')
    e.ins('move.w','0xffff80e0:l,%d1',6)
    e.label('gameplay_pc_018916')
    e.ins('bsr.w','gameplay_pc_018a54',4)
    e.label('gameplay_pc_01891a')
    e.ins('move.w','0xffff80e2:l,%d0',6)
    e.label('gameplay_pc_018920')
    e.ins('move.b','0xffff8103:l,%d2',6)
    e.label('gameplay_pc_018926')
    e.ins('cmpi.w','#0x5,0xffff8114:l',8)
    e.label('gameplay_pc_01892e')
    e.ins('bne.w','gameplay_pc_018954',4)
    e.label('gameplay_pc_018932')
    e.ins('move.w','%d0,-(%a7)',2)
    e.label('gameplay_pc_018934')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01893a')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_018940')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_018942')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_018944')
    e.ins('add.w','%d1,%d0',2)
    e.label('gameplay_pc_018946')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_018948')
    e.ins('addq.w','#0x1,%d0',2)
    e.label('gameplay_pc_01894a')
    e.ins('sub.w','%d0,%d2',2)
    e.label('gameplay_pc_01894c')
    e.ins('bcc.w','gameplay_pc_018952',4)
    e.label('gameplay_pc_018950')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_018952')
    e.ins('move.w','(%a7)+,%d0',2)
    e.label('gameplay_pc_018954')
    e.ins('move.b','%d2,(%a0, %d0.w)',4)
    e.label('gameplay_pc_018958')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01895a')
    e.ins('move.w','0xffff810e:l,(%a1, %d0.w)',8)
    e.label('gameplay_pc_018962')
    e.ins('bne.w','gameplay_pc_01897a',4)
    e.label('gameplay_pc_018966')
    e.ins('move.w','0xffff80e0:l,%d1',6)
    e.label('gameplay_pc_01896c')
    e.ins('bsr.w','gameplay_pc_0189d4',4)
    e.label('gameplay_pc_018970')
    e.ins('move.w','0xffff80e2:l,%d1',6)
    e.label('gameplay_pc_018976')
    e.ins('bsr.w','gameplay_pc_018a54',4)
    e.label('gameplay_pc_01897a')
    e.ins('move.w','0xffff80e0:l,%d6',6)
    e.label('gameplay_pc_018980')
    e.ins('move.w','0xffff80e2:l,%d7',6)
    e.label('gameplay_pc_018986')
    e.ins('move.w','%d6,%d0',2)
    e.label('gameplay_pc_018988')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_01898a')
    e.ins('move.w','0x2(%a2, %d0.w),%d2',4)
    e.label('gameplay_pc_01898e')
    e.ins('sub.w','0xffff8118:l,%d2',6)
    e.label('gameplay_pc_018994')
    e.ins('bcc.w','gameplay_pc_01899a',4)
    e.label('gameplay_pc_018998')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_01899a')
    e.ins('move.w','%d7,%d0',2)
    e.label('gameplay_pc_01899c')
    e.ins('bsr.w','gameplay_pc_018a2e',4)
    e.label('gameplay_pc_0189a0')
    e.ins('move.w','%d7,%d0',2)
    e.label('gameplay_pc_0189a2')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_0189a4')
    e.ins('move.w','0x2(%a2, %d0.w),%d2',4)
    e.label('gameplay_pc_0189a8')
    e.ins('sub.w','0xffff811a:l,%d2',6)
    e.label('gameplay_pc_0189ae')
    e.ins('bcc.w','gameplay_pc_0189b4',4)
    e.label('gameplay_pc_0189b2')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_0189b4')
    e.ins('move.w','%d6,%d0',2)
    e.label('gameplay_pc_0189b6')
    e.ins('bsr.w','gameplay_pc_018a2e',4)
    e.label('gameplay_pc_0189ba')
    e.ins('lsl.w','#0x2,%d6',2)
    e.label('gameplay_pc_0189bc')
    e.ins('lsl.w','#0x2,%d7',2)
    e.label('gameplay_pc_0189be')
    e.ins('move.w','0xffff8118:l,0x2(%a2, %d6.w)',8)
    e.label('gameplay_pc_0189c6')
    e.ins('move.w','0xffff811a:l,0x2(%a2, %d7.w)',8)
    e.label('gameplay_pc_0189ce')
    e.ins('bsr.w','gameplay_pc_018a94',4)
    e.label('gameplay_pc_0189d2')
    e.ins('rts','',2)

def _lower_grant_duel_fallback_progress(e,rules):
    e.label('gameplay_pc_0189d4')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('gameplay_pc_0189d6')
    e.ins('move.w','(%a3, %d1.w),%d2',4)
    e.label('gameplay_pc_0189da')
    e.ins('ext.l','%d2',2)
    e.label('gameplay_pc_0189dc')
    e.ins('divu.w','#0x28,%d2',4)
    e.label('gameplay_pc_0189e0')
    e.ins('lsr.w','#0x1,%d1',2)
    e.label('gameplay_pc_0189e2')
    e.ins('move.w','0xf68a:w,%d3',4)
    e.label('gameplay_pc_0189e6')
    e.ins('lsl.w','#0x1,%d3',2)
    e.label('gameplay_pc_0189e8')
    e.ins('lea.l','0xf45e:w,%a5',4)
    e.label('gameplay_pc_0189ec')
    e.ins('cmp.w','(%a5, %d3.w),%d1',4)
    e.label('gameplay_pc_0189f0')
    e.ins('beq.w','gameplay_pc_018a00',4)
    e.label('gameplay_pc_0189f4')
    e.ins('lea.l','0xa026:w,%a5',4)
    e.label('gameplay_pc_0189f8')
    e.ins('cmp.w','(%a5, %d3.w),%d1',4)
    e.label('gameplay_pc_0189fc')
    e.ins('bne.w','gameplay_pc_018a04',4)
    e.label('gameplay_pc_018a00')
    e.ins('addi.w','#0x1e,%d2',4)
    e.label('gameplay_pc_018a04')
    e.ins('lea.l','0xc700:w,%a5',4)
    e.label('gameplay_pc_018a08')
    e.ins('btst.b','#0x4,(%a5, %d1.w)',6)
    e.label('gameplay_pc_018a0e')
    e.ins('beq.w','gameplay_pc_018a16',4)
    e.label('gameplay_pc_018a12')
    e.ins('addi.w','#0x14,%d2',4)
    e.label('gameplay_pc_018a16')
    e.ins('move.w','(%a3, %d0.w),%d3',4)
    e.label('gameplay_pc_018a1a')
    e.ins('add.w','%d2,%d3',2)
    e.label('gameplay_pc_018a1c')
    e.ins('cmpi.w','#0x3e7,%d3',4)
    e.label('gameplay_pc_018a20')
    e.ins('bls.w','gameplay_pc_018a28',4)
    e.label('gameplay_pc_018a24')
    e.ins('move.w','#0x3e7,%d3',4)
    e.label('gameplay_pc_018a28')
    e.ins('move.w','%d3,(%a3, %d0.w)',4)
    e.label('gameplay_pc_018a2c')
    e.ins('rts','',2)

def _lower_grant_duel_troop_difference_progress(e,rules):
    e.label('gameplay_pc_018a2e')
    e.ins('andi.l','#0xffff,%d2',6)
    e.label('gameplay_pc_018a34')
    e.ins('divu.w','#0x64,%d2',4)
    e.label('gameplay_pc_018a38')
    e.ins('move.w','%d0,%d1',2)
    e.label('gameplay_pc_018a3a')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('gameplay_pc_018a3c')
    e.ins('move.w','(%a3, %d1.w),%d3',4)
    e.label('gameplay_pc_018a40')
    e.ins('add.w','%d2,%d3',2)
    e.label('gameplay_pc_018a42')
    e.ins('cmpi.w','#0x3e7,%d3',4)
    e.label('gameplay_pc_018a46')
    e.ins('bls.w','gameplay_pc_018a4e',4)
    e.label('gameplay_pc_018a4a')
    e.ins('move.w','#0x3e7,%d3',4)
    e.label('gameplay_pc_018a4e')
    e.ins('move.w','%d3,(%a3, %d1.w)',4)
    e.label('gameplay_pc_018a52')
    e.ins('rts','',2)

def _lower_remove_zero_readiness_duelist(e,rules):
    e.label('gameplay_pc_018a54')
    e.ins('movem.l','%d2/%a0,-(%a7)',4)
    e.label('gameplay_pc_018a58')
    e.ins('tst.w','0xefe0:w',4)
    e.label('gameplay_pc_018a5c')
    e.ins('beq.w','gameplay_pc_018a8e',4)
    e.label('gameplay_pc_018a60')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('gameplay_pc_018a64')
    e.ins('move.b','#0xff,(%a0, %d1.w)',6)
    e.label('gameplay_pc_018a6a')
    e.ins('lea.l','0xa550:w,%a0',4)
    e.label('gameplay_pc_018a6e')
    e.ins('cmp.w','0xf702:w,%d1',4)
    e.label('gameplay_pc_018a72')
    e.ins('beq.w','gameplay_pc_018a7a',4)
    e.label('gameplay_pc_018a76')
    e.ins('lea.l','0xa5a4:w,%a0',4)
    e.label('gameplay_pc_018a7a')
    e.ins('move.w','(%a0)+,%d2',2)
    e.label('gameplay_pc_018a7c')
    e.ins('bmi.w','gameplay_pc_018a8e',4)
    e.label('gameplay_pc_018a80')
    e.ins('andi.w','#0xff,%d2',4)
    e.label('gameplay_pc_018a84')
    e.ins('cmp.w','%d1,%d2',2)
    e.label('gameplay_pc_018a86')
    e.ins('bne.b','gameplay_pc_018a7a',2)
    e.label('gameplay_pc_018a88')
    e.ins('move.w','(%a0)+,-0x4(%a0)',4)
    e.label('gameplay_pc_018a8c')
    e.ins('bpl.b','gameplay_pc_018a88',2)
    e.label('gameplay_pc_018a8e')
    e.ins('movem.l','(%a7)+,%d2/%a0',4)
    e.label('gameplay_pc_018a92')
    e.ins('rts','',2)

def _lower_settle_duel_result_roster(e,rules):
    e.label('gameplay_pc_018a94')
    e.ins('tst.w','0xefe0:w',4)
    e.label('gameplay_pc_018a98')
    e.ins('beq.w','gameplay_pc_018ac4',4)
    e.label('gameplay_pc_018a9c')
    e.ins('cmpi.w','#0x6,0xffff8114:l',8)
    e.label('gameplay_pc_018aa4')
    e.ins('bcs.w','gameplay_pc_018ac4',4)
    e.label('gameplay_pc_018aa8')
    e.ins('bne.w','gameplay_pc_018aba',4)
    e.label('gameplay_pc_018aac')
    e.ins('move.w','0xffff80e0:l,%d0',6)
    e.label('gameplay_pc_018ab2')
    e.ins('bsr.w','gameplay_pc_018ac6',4)
    e.label('gameplay_pc_018ab6')
    e.ins('bra.w','gameplay_pc_018ac4',4)
    e.label('gameplay_pc_018aba')
    e.ins('move.w','0xffff80e2:l,%d0',6)
    e.label('gameplay_pc_018ac0')
    e.ins('bsr.w','gameplay_pc_018ac6',4)
    e.label('gameplay_pc_018ac4')
    e.ins('rts','',2)

def _lower_transfer_battle_roster(e,rules):
    e.label('gameplay_pc_018ac6')
    e.ins('lea.l','0xa5a4:w,%a0',4)
    e.label('gameplay_pc_018aca')
    e.ins('lea.l','0xa57a:w,%a1',4)
    e.label('gameplay_pc_018ace')
    e.ins('cmp.w','0xf702:w,%d0',4)
    e.label('gameplay_pc_018ad2')
    e.ins('bne.w','gameplay_pc_018ade',4)
    e.label('gameplay_pc_018ad6')
    e.ins('lea.l','0xa550:w,%a0',4)
    e.label('gameplay_pc_018ada')
    e.ins('lea.l','0xa5ce:w,%a1',4)
    e.label('gameplay_pc_018ade')
    e.ins('move.w','(%a0)+,%d1',2)
    e.label('gameplay_pc_018ae0')
    e.ins('bmi.w','gameplay_pc_018afe',4)
    e.label('gameplay_pc_018ae4')
    e.ins('andi.w','#0xff,%d1',4)
    e.label('gameplay_pc_018ae8')
    e.ins('cmp.w','%d0,%d1',2)
    e.label('gameplay_pc_018aea')
    e.ins('bne.b','gameplay_pc_018ade',2)
    e.label('gameplay_pc_018aec')
    e.ins('move.w','(%a0)+,-0x4(%a0)',4)
    e.label('gameplay_pc_018af0')
    e.ins('bpl.b','gameplay_pc_018aec',2)
    e.label('gameplay_pc_018af2')
    e.ins('tst.w','(%a1)+',2)
    e.label('gameplay_pc_018af4')
    e.ins('bpl.b','gameplay_pc_018af2',2)
    e.label('gameplay_pc_018af6')
    e.ins('move.w','%d0,-0x2(%a1)',4)
    e.label('gameplay_pc_018afa')
    e.ins('move.w','#0xffff,(%a1)',4)
    e.label('gameplay_pc_018afe')
    e.ins('rts','',2)

def _lower_settle_duel_packets(e,rules):
    e.label('gameplay_pc_018b00')
    e.ins('lea.l','0xff7050:l,%a0',6)
    e.label('gameplay_pc_018b06')
    e.ins('lea.l','0xff70a0:l,%a1',6)
    e.label('gameplay_pc_018b0c')
    e.ins('lea.l','0xff70f0:l,%a2',6)
    e.label('gameplay_pc_018b12')
    e.ins('lea.l','0xff70f1:l,%a3',6)
    e.label('gameplay_pc_018b18')
    e.ins('move.w','0xff706a:l,%d0',6)
    e.label('gameplay_pc_018b1e')
    e.ins('cmp.w','0xffff80e0:l,%d0',6)
    e.label('gameplay_pc_018b24')
    e.ins('beq.w','gameplay_pc_018b2c',4)
    e.label('gameplay_pc_018b28')
    e.ins('exg','%a0,%a1',2)
    e.label('gameplay_pc_018b2a')
    e.ins('exg','%a2,%a3',2)
    e.label('gameplay_pc_018b2c')
    e.ins('move.w','0x1c(%a0),0xffff810c:l',8)
    e.label('gameplay_pc_018b34')
    e.ins('move.w','0x1c(%a1),0xffff810e:l',8)
    e.label('gameplay_pc_018b3c')
    e.ins('move.w','0xff706a:l,%d0',6)
    e.label('gameplay_pc_018b42')
    e.ins('move.w','0xff70ba:l,%d1',6)
    e.label('gameplay_pc_018b48')
    e.ins('move.b','0xff70f0:l,%d2',6)
    e.label('gameplay_pc_018b4e')
    e.ins('beq.w','gameplay_pc_018b56',4)
    e.label('gameplay_pc_018b52')
    e.ins('bsr.w','gameplay_pc_018b94',4)
    e.label('gameplay_pc_018b56')
    e.ins('exg','%d0,%d1',2)
    e.label('gameplay_pc_018b58')
    e.ins('move.b','0xff70f1:l,%d2',6)
    e.label('gameplay_pc_018b5e')
    e.ins('beq.w','gameplay_pc_018b66',4)
    e.label('gameplay_pc_018b62')
    e.ins('bsr.w','gameplay_pc_018b94',4)
    e.label('gameplay_pc_018b66')
    e.ins('cmpi.b','#0x1,0xff70f0:l',8)
    e.label('gameplay_pc_018b6e')
    e.ins('beq.w','gameplay_pc_018b8e',4)
    e.label('gameplay_pc_018b72')
    e.ins('cmpi.b','#0x1,0xff70f1:l',8)
    e.label('gameplay_pc_018b7a')
    e.ins('beq.w','gameplay_pc_018b8e',4)
    e.label('gameplay_pc_018b7e')
    e.ins('bsr.w','gameplay_pc_018c56',4)
    e.label('gameplay_pc_018b82')
    e.ins('jsr','-734(%pc)',4)
    e.label('gameplay_pc_018b86')
    e.ins('andi.w','#0xfffe,%sr',4)
    e.label('gameplay_pc_018b8a')
    e.ins('bra.w','gameplay_pc_018b92',4)
    e.label('gameplay_pc_018b8e')
    e.ins('ori.w','#0x1,%sr',4)
    e.label('gameplay_pc_018b92')
    e.ins('rts','',2)

def _lower_apply_duel_disposition(e,rules):
    e.label('gameplay_pc_018b94')
    e.ins('movem.l','%d0-%d1/%a0-%a1,-(%a7)',4)
    e.label('gameplay_pc_018b98')
    e.ins('tst.w','0xefe0:w',4)
    e.label('gameplay_pc_018b9c')
    e.ins('beq.w','gameplay_pc_018c30',4)
    e.label('gameplay_pc_018ba0')
    e.ins('cmpi.b','#0x2,%d2',4)
    e.label('gameplay_pc_018ba4')
    e.ins('beq.w','gameplay_pc_018bf4',4)
    e.label('gameplay_pc_018ba8')
    e.ins('cmpi.b','#0x3,%d2',4)
    e.label('gameplay_pc_018bac')
    e.ins('bne.w','gameplay_pc_018c50',4)
    e.label('gameplay_pc_018bb0')
    e.ins('lea.l','0xa5ce:w,%a0',4)
    e.label('gameplay_pc_018bb4')
    e.ins('lea.l','0xa550:w,%a1',4)
    e.label('gameplay_pc_018bb8')
    e.ins('move.w','0xf68a:w,%d3',4)
    e.label('gameplay_pc_018bbc')
    e.ins('ori.w','#0x80,%d3',4)
    e.label('gameplay_pc_018bc0')
    e.ins('cmp.w','0xf702:w,%d0',4)
    e.label('gameplay_pc_018bc4')
    e.ins('beq.w','gameplay_pc_018bd4',4)
    e.label('gameplay_pc_018bc8')
    e.ins('ori.w','#0x40,%d3',4)
    e.label('gameplay_pc_018bcc')
    e.ins('lea.l','0xa57a:w,%a0',4)
    e.label('gameplay_pc_018bd0')
    e.ins('lea.l','0xa5a4:w,%a1',4)
    e.label('gameplay_pc_018bd4')
    e.ins('tst.w','(%a0)+',2)
    e.label('gameplay_pc_018bd6')
    e.ins('bpl.b','gameplay_pc_018bd4',2)
    e.label('gameplay_pc_018bd8')
    e.ins('move.w','%d0,-0x2(%a0)',4)
    e.label('gameplay_pc_018bdc')
    e.ins('move.w','#0xffff,(%a0)',4)
    e.label('gameplay_pc_018be0')
    e.ins('move.w','(%a1)+,%d3',2)
    e.label('gameplay_pc_018be2')
    e.ins('andi.w','#0xff,%d3',4)
    e.label('gameplay_pc_018be6')
    e.ins('cmp.w','%d0,%d3',2)
    e.label('gameplay_pc_018be8')
    e.ins('bne.b','gameplay_pc_018be0',2)
    e.label('gameplay_pc_018bea')
    e.ins('move.w','(%a1)+,-0x4(%a1)',4)
    e.label('gameplay_pc_018bee')
    e.ins('bpl.b','gameplay_pc_018bea',2)
    e.label('gameplay_pc_018bf0')
    e.ins('bra.w','gameplay_pc_018c50',4)
    e.label('gameplay_pc_018bf4')
    e.ins('cmp.w','0xf702:w,%d0',4)
    e.label('gameplay_pc_018bf8')
    e.ins('bne.w','gameplay_pc_018c08',4)
    e.label('gameplay_pc_018bfc')
    e.ins('lea.l','0xa550:w,%a0',4)
    e.label('gameplay_pc_018c00')
    e.ins('lea.l','0xa5ce:w,%a1',4)
    e.label('gameplay_pc_018c04')
    e.ins('bra.w','gameplay_pc_018c10',4)
    e.label('gameplay_pc_018c08')
    e.ins('lea.l','0xa5a4:w,%a0',4)
    e.label('gameplay_pc_018c0c')
    e.ins('lea.l','0xa57a:w,%a1',4)
    e.label('gameplay_pc_018c10')
    e.ins('move.w','(%a0)+,%d1',2)
    e.label('gameplay_pc_018c12')
    e.ins('andi.w','#0xff,%d1',4)
    e.label('gameplay_pc_018c16')
    e.ins('cmp.w','%d0,%d1',2)
    e.label('gameplay_pc_018c18')
    e.ins('bne.b','gameplay_pc_018c10',2)
    e.label('gameplay_pc_018c1a')
    e.ins('move.w','(%a0)+,-0x4(%a0)',4)
    e.label('gameplay_pc_018c1e')
    e.ins('bpl.b','gameplay_pc_018c1a',2)
    e.label('gameplay_pc_018c20')
    e.ins('tst.w','(%a1)+',2)
    e.label('gameplay_pc_018c22')
    e.ins('bpl.b','gameplay_pc_018c20',2)
    e.label('gameplay_pc_018c24')
    e.ins('move.w','%d0,-0x2(%a1)',4)
    e.label('gameplay_pc_018c28')
    e.ins('move.w','#0xffff,(%a1)',4)
    e.label('gameplay_pc_018c2c')
    e.ins('bra.w','gameplay_pc_018c50',4)
    e.label('gameplay_pc_018c30')
    e.ins('cmpi.b','#0x3,%d2',4)
    e.label('gameplay_pc_018c34')
    e.ins('beq.w','gameplay_pc_018c50',4)
    e.label('gameplay_pc_018c38')
    e.ins('move.w','#0x6,%d1',4)
    e.label('gameplay_pc_018c3c')
    e.ins('cmp.w','0xffff80e0:l,%d0',6)
    e.label('gameplay_pc_018c42')
    e.ins('beq.w','gameplay_pc_018c4a',4)
    e.label('gameplay_pc_018c46')
    e.ins('move.w','#0x7,%d1',4)
    e.label('gameplay_pc_018c4a')
    e.ins('move.w','%d1,0xffff8114:l',6)
    e.label('gameplay_pc_018c50')
    e.ins('movem.l','(%a7)+,%d0-%d1/%a0-%a1',4)
    e.label('gameplay_pc_018c54')
    e.ins('rts','',2)

def _lower_detach_zero_readiness_duelists(e,rules):
    e.label('gameplay_pc_018c56')
    e.ins('tst.w','0xefe0:w',4)
    e.label('gameplay_pc_018c5a')
    e.ins('beq.w','gameplay_pc_018c86',4)
    e.label('gameplay_pc_018c5e')
    e.ins('tst.w','0xff706c:l',6)
    e.label('gameplay_pc_018c64')
    e.ins('bne.w','gameplay_pc_018c72',4)
    e.label('gameplay_pc_018c68')
    e.ins('move.w','0xff706a:l,%d0',6)
    e.label('gameplay_pc_018c6e')
    e.ins('bsr.w','gameplay_pc_018c88',4)
    e.label('gameplay_pc_018c72')
    e.ins('tst.w','0xff70bc:l',6)
    e.label('gameplay_pc_018c78')
    e.ins('bne.w','gameplay_pc_018c86',4)
    e.label('gameplay_pc_018c7c')
    e.ins('move.w','0xff70ba:l,%d0',6)
    e.label('gameplay_pc_018c82')
    e.ins('bsr.w','gameplay_pc_018c88',4)
    e.label('gameplay_pc_018c86')
    e.ins('rts','',2)

def _lower_detach_defeated_duelist(e,rules):
    e.label('gameplay_pc_018c88')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('gameplay_pc_018c8c')
    e.ins('move.b','#0xff,(%a0, %d0.w)',6)
    e.label('gameplay_pc_018c92')
    e.ins('lea.l','0xa550:w,%a1',4)
    e.label('gameplay_pc_018c96')
    e.ins('cmp.w','0xf702:w,%d0',4)
    e.label('gameplay_pc_018c9a')
    e.ins('beq.w','gameplay_pc_018ca2',4)
    e.label('gameplay_pc_018c9e')
    e.ins('lea.l','0xa5a4:w,%a1',4)
    e.label('gameplay_pc_018ca2')
    e.ins('move.w','(%a1)+,%d1',2)
    e.label('gameplay_pc_018ca4')
    e.ins('andi.w','#0xff,%d1',4)
    e.label('gameplay_pc_018ca8')
    e.ins('cmp.w','%d0,%d1',2)
    e.label('gameplay_pc_018caa')
    e.ins('bne.b','gameplay_pc_018ca2',2)
    e.label('gameplay_pc_018cac')
    e.ins('move.w','(%a1)+,-0x4(%a1)',4)
    e.label('gameplay_pc_018cb0')
    e.ins('bpl.b','gameplay_pc_018cac',2)
    e.label('gameplay_pc_018cb2')
    e.ins('rts','',2)

def _lower_load_battlefield_map_context(e,rules):
    e.label('gameplay_pc_01a438')
    e.ins('move.l','%d4,-(%a7)',2)
    e.label('gameplay_pc_01a43a')
    e.ins('lea.l','0x945e8:l,%a0',6)
    e.label('gameplay_pc_01a440')
    e.ins('move.w','0xf68a:w,%d4',4)
    e.label('gameplay_pc_01a444')
    e.ins('mulu.w','#0x8c0,%d4',4)
    e.label('gameplay_pc_01a448')
    e.ins('adda.l','%d4,%a0',2)
    e.label('gameplay_pc_01a44a')
    e.ins('move.l','(%a7)+,%d4',2)
    e.label('gameplay_pc_01a44c')
    e.ins('rts','',2)

def _lower_read_battlefield_terrain_type(e,rules):
    e.label('gameplay_pc_01a44e')
    e.ins('movem.l','%d1-%d3/%a0,-(%a7)',4)
    e.label('gameplay_pc_01a452')
    e.ins('lsr.w','#0x3,%d1',2)
    e.label('gameplay_pc_01a454')
    e.ins('move.w','%d1,%d3',2)
    e.label('gameplay_pc_01a456')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('gameplay_pc_01a458')
    e.ins('add.w','%d3,%d1',2)
    e.label('gameplay_pc_01a45a')
    e.ins('lsl.w','#0x3,%d1',2)
    e.label('gameplay_pc_01a45c')
    e.ins('lsr.w','#0x3,%d2',2)
    e.label('gameplay_pc_01a45e')
    e.ins('add.w','%d2,%d1',2)
    e.label('gameplay_pc_01a460')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('gameplay_pc_01a462')
    e.ins('move.w','(%a0, %d1.w),%d0',4)
    e.label('gameplay_pc_01a466')
    e.ins('andi.w','#0x3ff,%d0',4)
    e.label('gameplay_pc_01a46a')
    e.ins('lea.l','0x6c0b4:l,%a0',6)
    e.label('gameplay_pc_01a470')
    e.ins('move.b','(%a0, %d0.w),%d0',4)
    e.label('gameplay_pc_01a474')
    e.ins('movem.l','(%a7)+,%d1-%d3/%a0',4)
    e.label('gameplay_pc_01a478')
    e.ins('rts','',2)

def _lower_compute_outcome_force_ratio(e,rules):
    e.label('gameplay_pc_01c1c2')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c1c8')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c1ce')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_01c1d0')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_01c1d2')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01c1d4')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_01c1d6')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c1d8')
    e.ins('addi.w','#0xa,%d0',4)
    e.label('gameplay_pc_01c1dc')
    e.ins('bsr.w','gameplay_pc_01c2a0',4)
    e.label('gameplay_pc_01c1e0')
    e.ins('moveq','#0,%d1',2)
    e.label('gameplay_pc_01c1e2')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_01c1e4')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_01c1e6')
    e.ins('lea.l','0xc800:w,%a0',4)
    e.label('gameplay_pc_01c1ea')
    e.ins('lea.l','0xb400:w,%a1',4)
    e.label('gameplay_pc_01c1ee')
    e.ins('lea.l','0xb600:w,%a2',4)
    e.label('gameplay_pc_01c1f2')
    e.ins('lea.l','0xd300:w,%a3',4)
    e.label('gameplay_pc_01c1f6')
    e.ins('move.w','(%a3)+,%d4',2)
    e.label('gameplay_pc_01c1f8')
    e.ins('bmi.w','gameplay_pc_01c20e',4)
    e.label('gameplay_pc_01c1fc')
    e.ins('lsl.w','#0x1,%d4',2)
    e.label('gameplay_pc_01c1fe')
    e.ins('add.w','(%a1, %d4.w),%d2',4)
    e.label('gameplay_pc_01c202')
    e.ins('add.w','(%a2, %d4.w),%d3',4)
    e.label('gameplay_pc_01c206')
    e.ins('lsl.w','#0x1,%d4',2)
    e.label('gameplay_pc_01c208')
    e.ins('add.l','(%a0, %d4.w),%d1',4)
    e.label('gameplay_pc_01c20c')
    e.ins('bra.b','gameplay_pc_01c1f6',2)
    e.label('gameplay_pc_01c20e')
    e.ins('addq.w','#0x1,%d1',2)
    e.label('gameplay_pc_01c210')
    e.ins('lsr.l','#0x5,%d1',2)
    e.label('gameplay_pc_01c212')
    e.ins('lsr.w','#0x3,%d2',2)
    e.label('gameplay_pc_01c214')
    e.ins('lsr.w','#0x3,%d3',2)
    e.label('gameplay_pc_01c216')
    e.ins('addq.w','#0x1,%d2',2)
    e.label('gameplay_pc_01c218')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('gameplay_pc_01c21a')
    e.ins('move.w','%d1,%d4',2)
    e.label('gameplay_pc_01c21c')
    e.ins('mulu.w','%d2,%d4',2)
    e.label('gameplay_pc_01c21e')
    e.ins('swap','%d1',2)
    e.label('gameplay_pc_01c220')
    e.ins('mulu.w','%d2,%d1',2)
    e.label('gameplay_pc_01c222')
    e.ins('swap','%d1',2)
    e.label('gameplay_pc_01c224')
    e.ins('add.l','%d4,%d1',2)
    e.label('gameplay_pc_01c226')
    e.ins('move.w','%d1,%d4',2)
    e.label('gameplay_pc_01c228')
    e.ins('mulu.w','%d3,%d4',2)
    e.label('gameplay_pc_01c22a')
    e.ins('swap','%d1',2)
    e.label('gameplay_pc_01c22c')
    e.ins('mulu.w','%d3,%d1',2)
    e.label('gameplay_pc_01c22e')
    e.ins('swap','%d1',2)
    e.label('gameplay_pc_01c230')
    e.ins('add.l','%d4,%d1',2)
    e.label('gameplay_pc_01c232')
    e.ins('move.w','%d1,%d4',2)
    e.label('gameplay_pc_01c234')
    e.ins('mulu.w','%d0,%d4',2)
    e.label('gameplay_pc_01c236')
    e.ins('swap','%d1',2)
    e.label('gameplay_pc_01c238')
    e.ins('mulu.w','%d0,%d1',2)
    e.label('gameplay_pc_01c23a')
    e.ins('swap','%d1',2)
    e.label('gameplay_pc_01c23c')
    e.ins('add.l','%d4,%d1',2)
    e.label('gameplay_pc_01c23e')
    e.ins('bsr.w','gameplay_pc_01c2c8',4)
    e.label('gameplay_pc_01c242')
    e.ins('lea.l','0xd300:w,%a0',4)
    e.label('gameplay_pc_01c246')
    e.ins('lea.l','0xc800:w,%a1',4)
    e.label('gameplay_pc_01c24a')
    e.ins('lea.l','0xb400:w,%a2',4)
    e.label('gameplay_pc_01c24e')
    e.ins('lea.l','0xb600:w,%a3',4)
    e.label('gameplay_pc_01c252')
    e.ins('moveq','#0,%d2',2)
    e.label('gameplay_pc_01c254')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_01c256')
    e.ins('clr.w','%d4',2)
    e.label('gameplay_pc_01c258')
    e.ins('move.w','(%a0)+,%d5',2)
    e.label('gameplay_pc_01c25a')
    e.ins('bmi.w','gameplay_pc_01c270',4)
    e.label('gameplay_pc_01c25e')
    e.ins('lsl.w','#0x1,%d5',2)
    e.label('gameplay_pc_01c260')
    e.ins('add.w','(%a2, %d5.w),%d3',4)
    e.label('gameplay_pc_01c264')
    e.ins('add.w','(%a3, %d5.w),%d4',4)
    e.label('gameplay_pc_01c268')
    e.ins('lsl.w','#0x1,%d5',2)
    e.label('gameplay_pc_01c26a')
    e.ins('add.l','(%a1, %d5.w),%d2',4)
    e.label('gameplay_pc_01c26e')
    e.ins('bra.b','gameplay_pc_01c258',2)
    e.label('gameplay_pc_01c270')
    e.ins('lsr.l','#0x5,%d2',2)
    e.label('gameplay_pc_01c272')
    e.ins('lsr.w','#0x3,%d3',2)
    e.label('gameplay_pc_01c274')
    e.ins('lsr.w','#0x3,%d4',2)
    e.label('gameplay_pc_01c276')
    e.ins('addq.w','#0x1,%d2',2)
    e.label('gameplay_pc_01c278')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('gameplay_pc_01c27a')
    e.ins('addq.w','#0x1,%d4',2)
    e.label('gameplay_pc_01c27c')
    e.ins('move.w','%d2,%d5',2)
    e.label('gameplay_pc_01c27e')
    e.ins('mulu.w','%d3,%d5',2)
    e.label('gameplay_pc_01c280')
    e.ins('swap','%d2',2)
    e.label('gameplay_pc_01c282')
    e.ins('mulu.w','%d3,%d2',2)
    e.label('gameplay_pc_01c284')
    e.ins('swap','%d2',2)
    e.label('gameplay_pc_01c286')
    e.ins('add.l','%d5,%d2',2)
    e.label('gameplay_pc_01c288')
    e.ins('move.w','%d2,%d5',2)
    e.label('gameplay_pc_01c28a')
    e.ins('mulu.w','%d3,%d5',2)
    e.label('gameplay_pc_01c28c')
    e.ins('swap','%d2',2)
    e.label('gameplay_pc_01c28e')
    e.ins('mulu.w','%d3,%d2',2)
    e.label('gameplay_pc_01c290')
    e.ins('swap','%d2',2)
    e.label('gameplay_pc_01c292')
    e.ins('add.l','%d5,%d2',2)
    e.label('gameplay_pc_01c294')
    e.ins('jsr','gameplay_pc_035760:l',6)
    e.label('gameplay_pc_01c29a')
    e.ins('move.w','%d1,0xefbc:w',4)
    e.label('gameplay_pc_01c29e')
    e.ins('rts','',2)

def _lower_build_city_assigned_outcome_candidates(e,rules):
    e.label('gameplay_pc_01c2a0')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('gameplay_pc_01c2a4')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('gameplay_pc_01c2a8')
    e.ins('move.w','#0xff,%d1',4)
    e.label('gameplay_pc_01c2ac')
    e.ins('move.w','0xf68a:w,%d2',4)
    e.label('gameplay_pc_01c2b0')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_01c2b2')
    e.ins('cmp.b','(%a0, %d1.w),%d2',4)
    e.label('gameplay_pc_01c2b6')
    e.ins('bne.w','gameplay_pc_01c2be',4)
    e.label('gameplay_pc_01c2ba')
    e.ins('move.w','%d1,(%a1)+',2)
    e.label('gameplay_pc_01c2bc')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('gameplay_pc_01c2be')
    e.ins('dbra','%d1,gameplay_pc_01c2b2',4)
    e.label('gameplay_pc_01c2c2')
    e.ins('move.w','#0xffff,(%a1)',4)
    e.label('gameplay_pc_01c2c6')
    e.ins('rts','',2)

def _lower_build_battlefield_outcome_candidates(e,rules):
    e.label('gameplay_pc_01c2c8')
    e.ins('lea.l','0xa050:w,%a0',4)
    e.label('gameplay_pc_01c2cc')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('gameplay_pc_01c2d0')
    e.ins('lea.l','0xcc00:w,%a2',4)
    e.label('gameplay_pc_01c2d4')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01c2d8')
    e.ins('move.w','#0xff,%d2',4)
    e.label('gameplay_pc_01c2dc')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_01c2de')
    e.ins('cmp.b','(%a0, %d2.w),%d0',4)
    e.label('gameplay_pc_01c2e2')
    e.ins('bne.w','gameplay_pc_01c2f2',4)
    e.label('gameplay_pc_01c2e6')
    e.ins('tst.b','(%a2, %d2.w)',4)
    e.label('gameplay_pc_01c2ea')
    e.ins('bmi.w','gameplay_pc_01c2f2',4)
    e.label('gameplay_pc_01c2ee')
    e.ins('move.w','%d2,(%a1)+',2)
    e.label('gameplay_pc_01c2f0')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('gameplay_pc_01c2f2')
    e.ins('dbra','%d2,gameplay_pc_01c2de',4)
    e.label('gameplay_pc_01c2f6')
    e.ins('move.w','#0xffff,(%a1)',4)
    e.label('gameplay_pc_01c2fa')
    e.ins('rts','',2)

def _lower_apply_battlefield_ratio_losses(e,rules):
    e.label('gameplay_pc_01c2fc')
    e.ins('bsr.b','gameplay_pc_01c2c8',2)
    e.label('gameplay_pc_01c2fe')
    e.ins('lea.l','0xd300:w,%a0',4)
    e.label('gameplay_pc_01c302')
    e.ins('lea.l','0xc800:w,%a1',4)
    e.label('gameplay_pc_01c306')
    e.ins('lea.l','0xb200:w,%a2',4)
    e.label('gameplay_pc_01c30a')
    e.ins('lea.l','0xcc00:w,%a3',4)
    e.label('gameplay_pc_01c30e')
    e.ins('lea.l','0xc000:w,%a4',4)
    e.label('gameplay_pc_01c312')
    e.ins('lea.l','0xc700:w,%a5',4)
    e.label('gameplay_pc_01c316')
    e.ins('clr.w','%d7',2)
    e.label('gameplay_pc_01c318')
    e.ins('move.w','(%a0)+,%d2',2)
    e.label('gameplay_pc_01c31a')
    e.ins('bmi.w','gameplay_pc_01c396',4)
    e.label('gameplay_pc_01c31e')
    e.ins('lsl.w','#0x2,%d2',2)
    e.label('gameplay_pc_01c320')
    e.ins('move.l','(%a1, %d2.w),%d3',4)
    e.label('gameplay_pc_01c324')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c32a')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c330')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_01c332')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('gameplay_pc_01c334')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01c336')
    e.ins('lsl.l','#0x3,%d0',2)
    e.label('gameplay_pc_01c338')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c33a')
    e.ins('addi.w','#0x1e,%d0',4)
    e.label('gameplay_pc_01c33e')
    e.ins('mulu.w','0xefbc:w,%d0',4)
    e.label('gameplay_pc_01c342')
    e.ins('move.w','%d0,%d1',2)
    e.label('gameplay_pc_01c344')
    e.ins('mulu.w','%d3,%d1',2)
    e.label('gameplay_pc_01c346')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c348')
    e.ins('mulu.w','%d3,%d0',2)
    e.label('gameplay_pc_01c34a')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c34c')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01c34e')
    e.ins('divu.w','#0x3e8,%d0',4)
    e.label('gameplay_pc_01c352')
    e.ins('sub.w','%d0,%d3',2)
    e.label('gameplay_pc_01c354')
    e.ins('move.w','%d3,0x2(%a1, %d2.w)',4)
    e.label('gameplay_pc_01c358')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c35e')
    e.ins('divu.w','#0x190,%d0',4)
    e.label('gameplay_pc_01c362')
    e.ins('add.w','%d0,%d7',2)
    e.label('gameplay_pc_01c364')
    e.ins('lsr.w','#0x1,%d2',2)
    e.label('gameplay_pc_01c366')
    e.ins('move.w','(%a2, %d2.w),%d3',4)
    e.label('gameplay_pc_01c36a')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c370')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c376')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_01c378')
    e.ins('lsl.l','#0x4,%d0',2)
    e.label('gameplay_pc_01c37a')
    e.ins('sub.l','%d1,%d0',2)
    e.label('gameplay_pc_01c37c')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_01c37e')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c380')
    e.ins('mulu.w','%d3,%d0',2)
    e.label('gameplay_pc_01c382')
    e.ins('divu.w','#0x64,%d0',4)
    e.label('gameplay_pc_01c386')
    e.ins('sub.w','%d0,%d3',2)
    e.label('gameplay_pc_01c388')
    e.ins('bne.w','gameplay_pc_01c390',4)
    e.label('gameplay_pc_01c38c')
    e.ins('move.w','#0x1,%d3',4)
    e.label('gameplay_pc_01c390')
    e.ins('move.w','%d3,(%a2, %d2.w)',4)
    e.label('gameplay_pc_01c394')
    e.ins('bra.b','gameplay_pc_01c318',2)
    e.label('gameplay_pc_01c396')
    e.ins('move.w','%d7,0xefb8:w',4)
    e.label('gameplay_pc_01c39a')
    e.ins('rts','',2)

def _lower_apply_city_assigned_heavy_losses(e,rules):
    e.label('gameplay_pc_01c39c')
    e.ins('bsr.w','gameplay_pc_01c2a0',4)
    e.label('gameplay_pc_01c3a0')
    e.ins('lea.l','0xd300:w,%a0',4)
    e.label('gameplay_pc_01c3a4')
    e.ins('lea.l','0xc800:w,%a1',4)
    e.label('gameplay_pc_01c3a8')
    e.ins('lea.l','0xb200:w,%a2',4)
    e.label('gameplay_pc_01c3ac')
    e.ins('lea.l','0xc000:w,%a3',4)
    e.label('gameplay_pc_01c3b0')
    e.ins('lea.l','0xcc00:w,%a4',4)
    e.label('gameplay_pc_01c3b4')
    e.ins('lea.l','0xf45e:w,%a5',4)
    e.label('gameplay_pc_01c3b8')
    e.ins('lea.l','0xc700:w,%a6',4)
    e.label('gameplay_pc_01c3bc')
    e.ins('clr.w','%d7',2)
    e.label('gameplay_pc_01c3be')
    e.ins('move.w','(%a0)+,%d2',2)
    e.label('gameplay_pc_01c3c0')
    e.ins('bmi.w','gameplay_pc_01c460',4)
    e.label('gameplay_pc_01c3c4')
    e.ins('lsl.w','#0x2,%d2',2)
    e.label('gameplay_pc_01c3c6')
    e.ins('move.l','(%a1, %d2.w),%d3',4)
    e.label('gameplay_pc_01c3ca')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c3d0')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c3d6')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_01c3d8')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('gameplay_pc_01c3da')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01c3dc')
    e.ins('lsl.l','#0x3,%d0',2)
    e.label('gameplay_pc_01c3de')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c3e0')
    e.ins('addi.w','#0x32,%d0',4)
    e.label('gameplay_pc_01c3e4')
    e.ins('mulu.w','%d3,%d0',2)
    e.label('gameplay_pc_01c3e6')
    e.ins('divu.w','#0x64,%d0',4)
    e.label('gameplay_pc_01c3ea')
    e.ins('sub.w','%d0,%d3',2)
    e.label('gameplay_pc_01c3ec')
    e.ins('move.w','%d3,0x2(%a1, %d2.w)',4)
    e.label('gameplay_pc_01c3f0')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c3f6')
    e.ins('divu.w','#0x190,%d0',4)
    e.label('gameplay_pc_01c3fa')
    e.ins('add.w','%d0,%d7',2)
    e.label('gameplay_pc_01c3fc')
    e.ins('lsr.w','#0x1,%d2',2)
    e.label('gameplay_pc_01c3fe')
    e.ins('move.w','(%a2, %d2.w),%d3',4)
    e.label('gameplay_pc_01c402')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c408')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c40e')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_01c410')
    e.ins('lsl.l','#0x4,%d0',2)
    e.label('gameplay_pc_01c412')
    e.ins('sub.l','%d1,%d0',2)
    e.label('gameplay_pc_01c414')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('gameplay_pc_01c416')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c418')
    e.ins('mulu.w','%d3,%d0',2)
    e.label('gameplay_pc_01c41a')
    e.ins('divu.w','#0x64,%d0',4)
    e.label('gameplay_pc_01c41e')
    e.ins('sub.w','%d0,%d3',2)
    e.label('gameplay_pc_01c420')
    e.ins('move.w','%d3,(%a2, %d2.w)',4)
    e.label('gameplay_pc_01c424')
    e.ins('cmpi.w','#0xa,%d3',4)
    e.label('gameplay_pc_01c428')
    e.ins('bhi.b','gameplay_pc_01c3be',2)
    e.label('gameplay_pc_01c42a')
    e.ins('move.w','(%a3, %d2.w),%d3',4)
    e.label('gameplay_pc_01c42e')
    e.ins('andi.l','#0xffff,%d3',6)
    e.label('gameplay_pc_01c434')
    e.ins('divu.w','#0x5,%d3',4)
    e.label('gameplay_pc_01c438')
    e.ins('lsr.w','#0x1,%d2',2)
    e.label('gameplay_pc_01c43a')
    e.ins('move.w','0xf68a:w,%d4',4)
    e.label('gameplay_pc_01c43e')
    e.ins('lsl.w','#0x1,%d4',2)
    e.label('gameplay_pc_01c440')
    e.ins('cmp.w','(%a5, %d4.w),%d2',4)
    e.label('gameplay_pc_01c444')
    e.ins('bne.w','gameplay_pc_01c44c',4)
    e.label('gameplay_pc_01c448')
    e.ins('addi.w','#0x1e,%d3',4)
    e.label('gameplay_pc_01c44c')
    e.ins('btst.b','#0x4,(%a6, %d2.w)',6)
    e.label('gameplay_pc_01c452')
    e.ins('beq.w','gameplay_pc_01c45a',4)
    e.label('gameplay_pc_01c456')
    e.ins('addi.w','#0x14,%d3',4)
    e.label('gameplay_pc_01c45a')
    e.ins('add.w','%d3,%d7',2)
    e.label('gameplay_pc_01c45c')
    e.ins('bra.w','gameplay_pc_01c3be',4)
    e.label('gameplay_pc_01c460')
    e.ins('move.w','%d7,0xefba:w',4)
    e.label('gameplay_pc_01c464')
    e.ins('rts','',2)

def _lower_consume_city_battle_resources(e,rules):
    e.label('gameplay_pc_01c466')
    e.ins('lea.l','0xc800:w,%a0',4)
    e.label('gameplay_pc_01c46a')
    e.ins('lea.l','0xa050:w,%a1',4)
    e.label('gameplay_pc_01c46e')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01c472')
    e.ins('move.w','#0xff,%d1',4)
    e.label('gameplay_pc_01c476')
    e.ins('moveq','#0,%d2',2)
    e.label('gameplay_pc_01c478')
    e.ins('cmp.b','(%a1, %d1.w),%d0',4)
    e.label('gameplay_pc_01c47c')
    e.ins('bne.w','gameplay_pc_01c48e',4)
    e.label('gameplay_pc_01c480')
    e.ins('move.w','%d1,%d3',2)
    e.label('gameplay_pc_01c482')
    e.ins('lsl.w','#0x2,%d3',2)
    e.label('gameplay_pc_01c484')
    e.ins('add.l','(%a0, %d3.w),%d2',4)
    e.label('gameplay_pc_01c488')
    e.ins('addi.l','#0x64,%d2',6)
    e.label('gameplay_pc_01c48e')
    e.ins('dbra','%d1,gameplay_pc_01c478',4)
    e.label('gameplay_pc_01c492')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c498')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c49e')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_01c4a0')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('gameplay_pc_01c4a2')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01c4a4')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_01c4a6')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01c4a8')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c4aa')
    e.ins('addi.w','#0xa,%d0',4)
    e.label('gameplay_pc_01c4ae')
    e.ins('move.w','%d2,%d3',2)
    e.label('gameplay_pc_01c4b0')
    e.ins('mulu.w','%d0,%d3',2)
    e.label('gameplay_pc_01c4b2')
    e.ins('swap','%d2',2)
    e.label('gameplay_pc_01c4b4')
    e.ins('mulu.w','%d0,%d2',2)
    e.label('gameplay_pc_01c4b6')
    e.ins('swap','%d2',2)
    e.label('gameplay_pc_01c4b8')
    e.ins('add.l','%d3,%d2',2)
    e.label('gameplay_pc_01c4ba')
    e.ins('divu.w','#0x1f4,%d2',4)
    e.label('gameplay_pc_01c4be')
    e.ins('lea.l','0xee24:w,%a2',4)
    e.label('gameplay_pc_01c4c2')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01c4c6')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_01c4c8')
    e.ins('move.l','(%a2, %d0.w),%d1',4)
    e.label('gameplay_pc_01c4cc')
    e.ins('andi.l','#0xffff,%d2',6)
    e.label('gameplay_pc_01c4d2')
    e.ins('sub.l','%d2,%d1',2)
    e.label('gameplay_pc_01c4d4')
    e.ins('bcc.w','gameplay_pc_01c4da',4)
    e.label('gameplay_pc_01c4d8')
    e.ins('moveq','#0,%d1',2)
    e.label('gameplay_pc_01c4da')
    e.ins('move.l','%d1,(%a2, %d0.w)',4)
    e.label('gameplay_pc_01c4de')
    e.ins('lea.l','0xcc00:w,%a1',4)
    e.label('gameplay_pc_01c4e2')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01c4e6')
    e.ins('move.w','#0xff,%d1',4)
    e.label('gameplay_pc_01c4ea')
    e.ins('moveq','#0,%d2',2)
    e.label('gameplay_pc_01c4ec')
    e.ins('cmp.b','(%a1, %d1.w),%d0',4)
    e.label('gameplay_pc_01c4f0')
    e.ins('bne.w','gameplay_pc_01c502',4)
    e.label('gameplay_pc_01c4f4')
    e.ins('move.w','%d1,%d3',2)
    e.label('gameplay_pc_01c4f6')
    e.ins('lsl.w','#0x2,%d3',2)
    e.label('gameplay_pc_01c4f8')
    e.ins('add.l','(%a0, %d3.w),%d2',4)
    e.label('gameplay_pc_01c4fc')
    e.ins('addi.l','#0x64,%d2',6)
    e.label('gameplay_pc_01c502')
    e.ins('dbra','%d1,gameplay_pc_01c4ec',4)
    e.label('gameplay_pc_01c506')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c50c')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c512')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_01c514')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('gameplay_pc_01c516')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01c518')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_01c51a')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01c51c')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c51e')
    e.ins('addi.w','#0xa,%d0',4)
    e.label('gameplay_pc_01c522')
    e.ins('move.w','%d2,%d3',2)
    e.label('gameplay_pc_01c524')
    e.ins('mulu.w','%d0,%d3',2)
    e.label('gameplay_pc_01c526')
    e.ins('swap','%d2',2)
    e.label('gameplay_pc_01c528')
    e.ins('mulu.w','%d0,%d2',2)
    e.label('gameplay_pc_01c52a')
    e.ins('swap','%d2',2)
    e.label('gameplay_pc_01c52c')
    e.ins('add.l','%d3,%d2',2)
    e.label('gameplay_pc_01c52e')
    e.ins('divu.w','#0x1f4,%d2',4)
    e.label('gameplay_pc_01c532')
    e.ins('andi.l','#0xffff,%d2',6)
    e.label('gameplay_pc_01c538')
    e.ins('lea.l','0xe09c:w,%a2',4)
    e.label('gameplay_pc_01c53c')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01c540')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_01c542')
    e.ins('move.l','(%a2, %d0.w),%d3',4)
    e.label('gameplay_pc_01c546')
    e.ins('sub.l','%d2,%d3',2)
    e.label('gameplay_pc_01c548')
    e.ins('bcc.w','gameplay_pc_01c54e',4)
    e.label('gameplay_pc_01c54c')
    e.ins('moveq','#0,%d3',2)
    e.label('gameplay_pc_01c54e')
    e.ins('move.l','%d3,(%a2, %d0.w)',4)
    e.label('gameplay_pc_01c552')
    e.ins('rts','',2)

def _lower_apply_battlefield_heavy_losses_and_detach(e,rules):
    e.label('gameplay_pc_01c5ee')
    e.ins('bsr.w','gameplay_pc_01c2c8',4)
    e.label('gameplay_pc_01c5f2')
    e.ins('lea.l','0xd300:w,%a0',4)
    e.label('gameplay_pc_01c5f6')
    e.ins('lea.l','0xc800:w,%a1',4)
    e.label('gameplay_pc_01c5fa')
    e.ins('lea.l','0xb200:w,%a2',4)
    e.label('gameplay_pc_01c5fe')
    e.ins('lea.l','0xc000:w,%a3',4)
    e.label('gameplay_pc_01c602')
    e.ins('lea.l','0xc700:w,%a4',4)
    e.label('gameplay_pc_01c606')
    e.ins('lea.l','0xcc00:w,%a5',4)
    e.label('gameplay_pc_01c60a')
    e.ins('clr.w','%d7',2)
    e.label('gameplay_pc_01c60c')
    e.ins('move.w','(%a0)+,%d2',2)
    e.label('gameplay_pc_01c60e')
    e.ins('bmi.w','gameplay_pc_01c698',4)
    e.label('gameplay_pc_01c612')
    e.ins('lsl.w','#0x2,%d2',2)
    e.label('gameplay_pc_01c614')
    e.ins('move.l','(%a1, %d2.w),%d3',4)
    e.label('gameplay_pc_01c618')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c61e')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c624')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_01c626')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('gameplay_pc_01c628')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01c62a')
    e.ins('lsl.l','#0x3,%d0',2)
    e.label('gameplay_pc_01c62c')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c62e')
    e.ins('addi.w','#0x32,%d0',4)
    e.label('gameplay_pc_01c632')
    e.ins('mulu.w','%d3,%d0',2)
    e.label('gameplay_pc_01c634')
    e.ins('divu.w','#0x64,%d0',4)
    e.label('gameplay_pc_01c638')
    e.ins('sub.w','%d0,%d3',2)
    e.label('gameplay_pc_01c63a')
    e.ins('move.w','%d3,0x2(%a1, %d2.w)',4)
    e.label('gameplay_pc_01c63e')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c644')
    e.ins('divu.w','#0x190,%d0',4)
    e.label('gameplay_pc_01c648')
    e.ins('add.w','%d0,%d7',2)
    e.label('gameplay_pc_01c64a')
    e.ins('lsr.w','#0x1,%d2',2)
    e.label('gameplay_pc_01c64c')
    e.ins('move.w','(%a2, %d2.w),%d3',4)
    e.label('gameplay_pc_01c650')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c656')
    e.ins('mulu.w','#0x3d,%d0',4)
    e.label('gameplay_pc_01c65a')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c65c')
    e.ins('mulu.w','%d3,%d0',2)
    e.label('gameplay_pc_01c65e')
    e.ins('divu.w','#0x64,%d0',4)
    e.label('gameplay_pc_01c662')
    e.ins('sub.w','%d0,%d3',2)
    e.label('gameplay_pc_01c664')
    e.ins('move.w','%d3,(%a2, %d2.w)',4)
    e.label('gameplay_pc_01c668')
    e.ins('cmpi.w','#0xa,%d3',4)
    e.label('gameplay_pc_01c66c')
    e.ins('bhi.b','gameplay_pc_01c60c',2)
    e.label('gameplay_pc_01c66e')
    e.ins('move.w','(%a3, %d2.w),%d3',4)
    e.label('gameplay_pc_01c672')
    e.ins('andi.l','#0xffff,%d3',6)
    e.label('gameplay_pc_01c678')
    e.ins('divu.w','#0x5,%d3',4)
    e.label('gameplay_pc_01c67c')
    e.ins('lsr.w','#0x1,%d2',2)
    e.label('gameplay_pc_01c67e')
    e.ins('move.b','#0xff,(%a5, %d2.w)',6)
    e.label('gameplay_pc_01c684')
    e.ins('btst.b','#0x4,(%a4, %d2.w)',6)
    e.label('gameplay_pc_01c68a')
    e.ins('beq.w','gameplay_pc_01c692',4)
    e.label('gameplay_pc_01c68e')
    e.ins('addi.w','#0x14,%d3',4)
    e.label('gameplay_pc_01c692')
    e.ins('add.w','%d3,%d7',2)
    e.label('gameplay_pc_01c694')
    e.ins('bra.w','gameplay_pc_01c60c',4)
    e.label('gameplay_pc_01c698')
    e.ins('move.w','%d7,0xefb8:w',4)
    e.label('gameplay_pc_01c69c')
    e.ins('rts','',2)

def _lower_rebuild_primary_after_battle(e,rules):
    e.label('gameplay_pc_01c82c')
    e.ins('bsr.w','gameplay_pc_01c2a0',4)
    e.label('gameplay_pc_01c830')
    e.ins('bsr.w','gameplay_pc_01c942',4)
    e.label('gameplay_pc_01c834')
    e.ins('bsr.w','gameplay_pc_01c2c8',4)
    e.label('gameplay_pc_01c838')
    e.ins('move.w','%d3,%d0',2)
    e.label('gameplay_pc_01c83a')
    e.ins('add.w','0xefba:w,%d0',4)
    e.label('gameplay_pc_01c83e')
    e.ins('subi.w','#0xa,%d0',4)
    e.label('gameplay_pc_01c842')
    e.ins('bls.w','gameplay_pc_01c84a',4)
    e.label('gameplay_pc_01c846')
    e.ins('bsr.w','gameplay_pc_01c8bc',4)
    e.label('gameplay_pc_01c84a')
    e.ins('lea.l','0xaf56:w,%a0',4)
    e.label('gameplay_pc_01c84e')
    e.ins('move.w','(%a0),%d0',2)
    e.label('gameplay_pc_01c850')
    e.ins('bmi.w','gameplay_pc_01c85c',4)
    e.label('gameplay_pc_01c854')
    e.ins('bset.l','#0xe,%d0',4)
    e.label('gameplay_pc_01c858')
    e.ins('move.w','%d0,(%a0)+',2)
    e.label('gameplay_pc_01c85a')
    e.ins('bra.b','gameplay_pc_01c84e',2)
    e.label('gameplay_pc_01c85c')
    e.ins('tst.w','0xaf56:w',4)
    e.label('gameplay_pc_01c860')
    e.ins('bmi.w','gameplay_pc_01c8a6',4)
    e.label('gameplay_pc_01c864')
    e.ins('move.b','0xf68f:w,0xefe2:w',6)
    e.label('gameplay_pc_01c86a')
    e.ins('bsr.w','gameplay_pc_01c9fe',4)
    e.label('gameplay_pc_01c86e')
    e.ins('bcs.w','gameplay_pc_01c886',4)
    e.label('gameplay_pc_01c872')
    e.ins('move.w','#0x2,0xf6d6:w',6)
    e.label('gameplay_pc_01c878')
    e.ins('jsr','gameplay_pc_021514:l',6)
    e.label('gameplay_pc_01c87e')
    e.ins('bsr.w','gameplay_pc_01ca60',4)
    e.label('gameplay_pc_01c882')
    e.ins('bra.w','gameplay_pc_01c8a6',4)
    e.label('gameplay_pc_01c886')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01c88a')
    e.ins('bset.l','#0x7,%d0',4)
    e.label('gameplay_pc_01c88e')
    e.ins('lea.l','0xaf56:w,%a0',4)
    e.label('gameplay_pc_01c892')
    e.ins('lea.l','0xcc00:w,%a1',4)
    e.label('gameplay_pc_01c896')
    e.ins('move.w','(%a0)+,%d1',2)
    e.label('gameplay_pc_01c898')
    e.ins('bmi.w','gameplay_pc_01c8a6',4)
    e.label('gameplay_pc_01c89c')
    e.ins('andi.w','#0xff,%d1',4)
    e.label('gameplay_pc_01c8a0')
    e.ins('move.b','%d0,(%a1, %d1.w)',4)
    e.label('gameplay_pc_01c8a4')
    e.ins('bra.b','gameplay_pc_01c896',2)
    e.label('gameplay_pc_01c8a6')
    e.ins('lea.l','0xe640:w,%a0',4)
    e.label('gameplay_pc_01c8aa')
    e.ins('move.w','0xf68c:w,%d0',4)
    e.label('gameplay_pc_01c8ae')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01c8b0')
    e.ins('move.w','(%a0, %d0.w),0xf3f2:w',6)
    e.label('gameplay_pc_01c8b6')
    e.ins('bsr.w','gameplay_pc_01ca3c',4)
    e.label('gameplay_pc_01c8ba')
    e.ins('rts','',2)

def _lower_sort_returning_officer_status(e,rules):
    e.label('gameplay_pc_01c8bc')
    e.ins('add.w','%d0,0xefb8:w',4)
    e.label('gameplay_pc_01c8c0')
    e.ins('lea.l','0xaf28:w,%a0',4)
    e.label('gameplay_pc_01c8c4')
    e.ins('lea.l','0xc300:w,%a3',4)
    e.label('gameplay_pc_01c8c8')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('gameplay_pc_01c8cc')
    e.ins('lea.l','0xd320:w,%a2',4)
    e.label('gameplay_pc_01c8d0')
    e.ins('move.w','#0xffff,0xd300:w',6)
    e.label('gameplay_pc_01c8d6')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_01c8d8')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_01c8da')
    e.ins('move.w','(%a0)+,%d1',2)
    e.label('gameplay_pc_01c8dc')
    e.ins('bmi.w','gameplay_pc_01c912',4)
    e.label('gameplay_pc_01c8e0')
    e.ins('move.b','(%a3, %d1.w),%d2',4)
    e.label('gameplay_pc_01c8e4')
    e.ins('tst.w','(%a1, %d3.w)',4)
    e.label('gameplay_pc_01c8e8')
    e.ins('bmi.w','gameplay_pc_01c8f8',4)
    e.label('gameplay_pc_01c8ec')
    e.ins('cmp.b','0x1(%a2, %d3.w),%d2',4)
    e.label('gameplay_pc_01c8f0')
    e.ins('bhi.w','gameplay_pc_01c8f8',4)
    e.label('gameplay_pc_01c8f4')
    e.ins('addq.w','#0x2,%d3',2)
    e.label('gameplay_pc_01c8f6')
    e.ins('bra.b','gameplay_pc_01c8e4',2)
    e.label('gameplay_pc_01c8f8')
    e.ins('move.w','(%a1, %d3.w),%d4',4)
    e.label('gameplay_pc_01c8fc')
    e.ins('move.w','%d1,(%a1, %d3.w)',4)
    e.label('gameplay_pc_01c900')
    e.ins('bmi.b','gameplay_pc_01c8d8',2)
    e.label('gameplay_pc_01c902')
    e.ins('move.w','(%a2, %d3.w),%d5',4)
    e.label('gameplay_pc_01c906')
    e.ins('move.w','%d2,(%a2, %d3.w)',4)
    e.label('gameplay_pc_01c90a')
    e.ins('addq.w','#0x2,%d3',2)
    e.label('gameplay_pc_01c90c')
    e.ins('move.w','%d4,%d1',2)
    e.label('gameplay_pc_01c90e')
    e.ins('move.w','%d5,%d2',2)
    e.label('gameplay_pc_01c910')
    e.ins('bra.b','gameplay_pc_01c8f8',2)
    e.label('gameplay_pc_01c912')
    e.ins('lea.l','0xaf56:w,%a0',4)
    e.label('gameplay_pc_01c916')
    e.ins('tst.w','(%a0)+',2)
    e.label('gameplay_pc_01c918')
    e.ins('bpl.b','gameplay_pc_01c916',2)
    e.label('gameplay_pc_01c91a')
    e.ins('subq.w','#0x2,%a0',2)
    e.label('gameplay_pc_01c91c')
    e.ins('subq.w','#0x1,%d0',2)
    e.label('gameplay_pc_01c91e')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('gameplay_pc_01c922')
    e.ins('move.w','(%a1)+,(%a0)+',2)
    e.label('gameplay_pc_01c924')
    e.ins('dbra','%d0,gameplay_pc_01c922',4)
    e.label('gameplay_pc_01c928')
    e.ins('move.w','#0xffff,(%a0)',4)
    e.label('gameplay_pc_01c92c')
    e.ins('lea.l','0xaf28:w,%a0',4)
    e.label('gameplay_pc_01c930')
    e.ins('clr.w','%d1',2)
    e.label('gameplay_pc_01c932')
    e.ins('move.w','(%a1)+,(%a0)+',2)
    e.label('gameplay_pc_01c934')
    e.ins('bmi.w','gameplay_pc_01c93c',4)
    e.label('gameplay_pc_01c938')
    e.ins('addq.w','#0x1,%d1',2)
    e.label('gameplay_pc_01c93a')
    e.ins('bra.b','gameplay_pc_01c932',2)
    e.label('gameplay_pc_01c93c')
    e.ins('move.w','%d1,0xefba:w',4)
    e.label('gameplay_pc_01c940')
    e.ins('rts','',2)

def _lower_partition_city_survivors(e,rules):
    e.label('gameplay_pc_01c942')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('gameplay_pc_01c946')
    e.ins('lea.l','0xf427:w,%a1',4)
    e.label('gameplay_pc_01c94a')
    e.ins('lea.l','0xe640:w,%a2',4)
    e.label('gameplay_pc_01c94e')
    e.ins('move.w','0xd300:w,%d0',4)
    e.label('gameplay_pc_01c952')
    e.ins('clr.w','%d1',2)
    e.label('gameplay_pc_01c954')
    e.ins('move.b','(%a0, %d0.w),%d1',4)
    e.label('gameplay_pc_01c958')
    e.ins('andi.w','#0x3f,%d1',4)
    e.label('gameplay_pc_01c95c')
    e.ins('clr.w','%d0',2)
    e.label('gameplay_pc_01c95e')
    e.ins('move.b','(%a1, %d1.w),%d0',4)
    e.label('gameplay_pc_01c962')
    e.ins('move.b','%d0,0xefe2:w',4)
    e.label('gameplay_pc_01c966')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01c968')
    e.ins('move.w','(%a2, %d0.w),%d7',4)
    e.label('gameplay_pc_01c96c')
    e.ins('lea.l','0xd300:w,%a0',4)
    e.label('gameplay_pc_01c970')
    e.ins('lea.l','0xc800:w,%a1',4)
    e.label('gameplay_pc_01c974')
    e.ins('lea.l','0xb200:w,%a2',4)
    e.label('gameplay_pc_01c978')
    e.ins('lea.l','0xaf28:w,%a3',4)
    e.label('gameplay_pc_01c97c')
    e.ins('lea.l','0xaf56:w,%a4',4)
    e.label('gameplay_pc_01c980')
    e.ins('lea.l','0xcc00:w,%a5',4)
    e.label('gameplay_pc_01c984')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_01c986')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_01c988')
    e.ins('move.w','(%a0)+,%d6',2)
    e.label('gameplay_pc_01c98a')
    e.ins('bmi.w','gameplay_pc_01c9ec',4)
    e.label('gameplay_pc_01c98e')
    e.ins('cmp.w','%d7,%d6',2)
    e.label('gameplay_pc_01c990')
    e.ins('beq.w','gameplay_pc_01c9d0',4)
    e.label('gameplay_pc_01c994')
    e.ins('move.w','%d6,%d4',2)
    e.label('gameplay_pc_01c996')
    e.ins('lsl.w','#0x2,%d4',2)
    e.label('gameplay_pc_01c998')
    e.ins('cmpi.l','#0x1f4,(%a1, %d4.w)',8)
    e.label('gameplay_pc_01c9a0')
    e.ins('bls.w','gameplay_pc_01c9bc',4)
    e.label('gameplay_pc_01c9a4')
    e.ins('cmpi.l','#0x3e8,(%a1, %d4.w)',8)
    e.label('gameplay_pc_01c9ac')
    e.ins('bhi.w','gameplay_pc_01c9e6',4)
    e.label('gameplay_pc_01c9b0')
    e.ins('lsr.w','#0x1,%d4',2)
    e.label('gameplay_pc_01c9b2')
    e.ins('cmpi.w','#0x1e,(%a2, %d4.w)',6)
    e.label('gameplay_pc_01c9b8')
    e.ins('bhi.w','gameplay_pc_01c9e6',4)
    e.label('gameplay_pc_01c9bc')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c9c2')
    e.ins('andi.w','#0x3,%d0',4)
    e.label('gameplay_pc_01c9c6')
    e.ins('bne.w','gameplay_pc_01c9e6',4)
    e.label('gameplay_pc_01c9ca')
    e.ins('move.w','%d6,(%a4)+',2)
    e.label('gameplay_pc_01c9cc')
    e.ins('addq.w','#0x1,%d2',2)
    e.label('gameplay_pc_01c9ce')
    e.ins('bra.b','gameplay_pc_01c988',2)
    e.label('gameplay_pc_01c9d0')
    e.ins('bsr.w','gameplay_pc_01c9fe',4)
    e.label('gameplay_pc_01c9d4')
    e.ins('bcs.w','gameplay_pc_01c9de',4)
    e.label('gameplay_pc_01c9d8')
    e.ins('move.w','%d6,(%a4)+',2)
    e.label('gameplay_pc_01c9da')
    e.ins('addq.w','#0x1,%d2',2)
    e.label('gameplay_pc_01c9dc')
    e.ins('bra.b','gameplay_pc_01c988',2)
    e.label('gameplay_pc_01c9de')
    e.ins('move.b','#0xff,(%a5, %d6.w)',6)
    e.label('gameplay_pc_01c9e4')
    e.ins('bra.b','gameplay_pc_01c988',2)
    e.label('gameplay_pc_01c9e6')
    e.ins('move.w','%d6,(%a3)+',2)
    e.label('gameplay_pc_01c9e8')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('gameplay_pc_01c9ea')
    e.ins('bra.b','gameplay_pc_01c988',2)
    e.label('gameplay_pc_01c9ec')
    e.ins('move.w','#0xffff,(%a3)',4)
    e.label('gameplay_pc_01c9f0')
    e.ins('move.w','#0xffff,(%a4)',4)
    e.label('gameplay_pc_01c9f4')
    e.ins('move.w','%d2,0xefb8:w',4)
    e.label('gameplay_pc_01c9f8')
    e.ins('move.w','%d3,0xefba:w',4)
    e.label('gameplay_pc_01c9fc')
    e.ins('rts','',2)

def _lower_owner_has_other_city_carry(e,rules):
    e.label('gameplay_pc_01c9fe')
    e.ins('movem.l','%d0-%d2/%a0,-(%a7)',4)
    e.label('gameplay_pc_01ca02')
    e.ins('lea.l','0xf428:w,%a0',4)
    e.label('gameplay_pc_01ca06')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01ca0a')
    e.ins('subq.w','#0x1,%d0',2)
    e.label('gameplay_pc_01ca0c')
    e.ins('move.w','#0x27,%d1',4)
    e.label('gameplay_pc_01ca10')
    e.ins('move.b','0xefe2:w,%d2',4)
    e.label('gameplay_pc_01ca14')
    e.ins('cmp.b','(%a0, %d1.w),%d2',4)
    e.label('gameplay_pc_01ca18')
    e.ins('bne.w','gameplay_pc_01ca22',4)
    e.label('gameplay_pc_01ca1c')
    e.ins('cmp.w','%d0,%d1',2)
    e.label('gameplay_pc_01ca1e')
    e.ins('bne.w','gameplay_pc_01ca32',4)
    e.label('gameplay_pc_01ca22')
    e.ins('dbra','%d1,gameplay_pc_01ca14',4)
    e.label('gameplay_pc_01ca26')
    e.ins('movem.l','(%a7)+,%d0-%d2/%a0',4)
    e.label('gameplay_pc_01ca2a')
    e.ins('ori.w','#0x1,%sr',4)
    e.label('gameplay_pc_01ca2e')
    e.ins('bra.w','gameplay_pc_01ca3a',4)
    e.label('gameplay_pc_01ca32')
    e.ins('movem.l','(%a7)+,%d0-%d2/%a0',4)
    e.label('gameplay_pc_01ca36')
    e.ins('andi.w','#0xfffe,%sr',4)
    e.label('gameplay_pc_01ca3a')
    e.ins('rts','',2)

def _lower_restore_returning_officer_assignments(e,rules):
    e.label('gameplay_pc_01ca3c')
    e.ins('lea.l','0xaf28:w,%a0',4)
    e.label('gameplay_pc_01ca40')
    e.ins('lea.l','0xcc00:w,%a1',4)
    e.label('gameplay_pc_01ca44')
    e.ins('move.w','0xf68a:w,%d1',4)
    e.label('gameplay_pc_01ca48')
    e.ins('move.w','(%a0)+,%d0',2)
    e.label('gameplay_pc_01ca4a')
    e.ins('bmi.w','gameplay_pc_01ca5e',4)
    e.label('gameplay_pc_01ca4e')
    e.ins('move.b','%d1,(%a1, %d0.w)',4)
    e.label('gameplay_pc_01ca52')
    e.ins('move.w','%d0,0xf3a6:w',4)
    e.label('gameplay_pc_01ca56')
    e.ins('jsr','gameplay_pc_0208ce:l',6)
    e.label('gameplay_pc_01ca5c')
    e.ins('bra.b','gameplay_pc_01ca48',2)
    e.label('gameplay_pc_01ca5e')
    e.ins('rts','',2)

def _lower_allocate_packed_group_resources(e,rules):
    e.label('gameplay_pc_01ca60')
    e.ins('lea.l','0xc800:w,%a1',4)
    e.label('gameplay_pc_01ca64')
    e.ins('move.b','(%a0),%d0',2)
    e.label('gameplay_pc_01ca66')
    e.ins('andi.w','#0xff,%d0',4)
    e.label('gameplay_pc_01ca6a')
    e.ins('subq.w','#0x1,%d0',2)
    e.label('gameplay_pc_01ca6c')
    e.ins('moveq','#0,%d1',2)
    e.label('gameplay_pc_01ca6e')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_01ca70')
    e.ins('move.b','0xd(%a0, %d0.w),%d2',4)
    e.label('gameplay_pc_01ca74')
    e.ins('lsl.w','#0x2,%d2',2)
    e.label('gameplay_pc_01ca76')
    e.ins('add.l','(%a1, %d2.w),%d1',4)
    e.label('gameplay_pc_01ca7a')
    e.ins('addi.l','#0x64,%d1',6)
    e.label('gameplay_pc_01ca80')
    e.ins('dbra','%d0,gameplay_pc_01ca6e',4)
    e.label('gameplay_pc_01ca84')
    e.ins('move.l','%d1,%d2',2)
    e.label('gameplay_pc_01ca86')
    e.ins('lsl.l','#0x1,%d2',2)
    e.label('gameplay_pc_01ca88')
    e.ins('add.l','%d1,%d2',2)
    e.label('gameplay_pc_01ca8a')
    e.ins('divu.w','#0x5,%d2',4)
    e.label('gameplay_pc_01ca8e')
    e.ins('andi.l','#0xffff,%d2',6)
    e.label('gameplay_pc_01ca94')
    e.ins('move.l','%d2,%d3',2)
    e.label('gameplay_pc_01ca96')
    e.ins('lea.l','0xed84:w,%a1',4)
    e.label('gameplay_pc_01ca9a')
    e.ins('lea.l','0xee24:w,%a2',4)
    e.label('gameplay_pc_01ca9e')
    e.ins('btst.b','#0x1,0xf6d7:w',6)
    e.label('gameplay_pc_01caa4')
    e.ins('beq.w','gameplay_pc_01cab0',4)
    e.label('gameplay_pc_01caa8')
    e.ins('lea.l','0xdffc:w,%a1',4)
    e.label('gameplay_pc_01caac')
    e.ins('lea.l','0xe09c:w,%a2',4)
    e.label('gameplay_pc_01cab0')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01cab4')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_01cab6')
    e.ins('move.l','(%a1, %d0.w),%d1',4)
    e.label('gameplay_pc_01caba')
    e.ins('cmp.l','%d2,%d1',2)
    e.label('gameplay_pc_01cabc')
    e.ins('bcc.w','gameplay_pc_01cac2',4)
    e.label('gameplay_pc_01cac0')
    e.ins('move.l','%d1,%d2',2)
    e.label('gameplay_pc_01cac2')
    e.ins('sub.l','%d2,%d1',2)
    e.label('gameplay_pc_01cac4')
    e.ins('move.l','%d1,(%a1, %d0.w)',4)
    e.label('gameplay_pc_01cac8')
    e.ins('move.l','(%a2, %d0.w),%d1',4)
    e.label('gameplay_pc_01cacc')
    e.ins('cmp.l','%d3,%d1',2)
    e.label('gameplay_pc_01cace')
    e.ins('bcc.w','gameplay_pc_01cad4',4)
    e.label('gameplay_pc_01cad2')
    e.ins('move.l','%d1,%d3',2)
    e.label('gameplay_pc_01cad4')
    e.ins('sub.l','%d3,%d1',2)
    e.label('gameplay_pc_01cad6')
    e.ins('move.l','%d1,(%a2, %d0.w)',4)
    e.label('gameplay_pc_01cada')
    e.ins('move.b','%d2,0x8(%a0)',4)
    e.label('gameplay_pc_01cade')
    e.ins('lsr.l','#0x8,%d2',2)
    e.label('gameplay_pc_01cae0')
    e.ins('move.b','%d2,0x7(%a0)',4)
    e.label('gameplay_pc_01cae4')
    e.ins('lsr.l','#0x8,%d2',2)
    e.label('gameplay_pc_01cae6')
    e.ins('move.b','%d2,0x6(%a0)',4)
    e.label('gameplay_pc_01caea')
    e.ins('lsl.w','#0x8,%d2',2)
    e.label('gameplay_pc_01caec')
    e.ins('move.b','%d2,0x5(%a0)',4)
    e.label('gameplay_pc_01caf0')
    e.ins('move.b','%d3,0xc(%a0)',4)
    e.label('gameplay_pc_01caf4')
    e.ins('lsr.l','#0x8,%d3',2)
    e.label('gameplay_pc_01caf6')
    e.ins('move.b','%d3,0xb(%a0)',4)
    e.label('gameplay_pc_01cafa')
    e.ins('lsr.l','#0x8,%d3',2)
    e.label('gameplay_pc_01cafc')
    e.ins('move.b','%d3,0xa(%a0)',4)
    e.label('gameplay_pc_01cb00')
    e.ins('lsr.w','#0x8,%d3',2)
    e.label('gameplay_pc_01cb02')
    e.ins('move.b','%d3,0x9(%a0)',4)
    e.label('gameplay_pc_01cb06')
    e.ins('rts','',2)

def _lower_rebuild_secondary_after_battle(e,rules):
    e.label('gameplay_pc_01cb08')
    e.ins('bsr.w','gameplay_pc_01c2c8',4)
    e.label('gameplay_pc_01cb0c')
    e.ins('bsr.w','gameplay_pc_01c942',4)
    e.label('gameplay_pc_01cb10')
    e.ins('bsr.w','gameplay_pc_01c2a0',4)
    e.label('gameplay_pc_01cb14')
    e.ins('move.w','%d3,%d0',2)
    e.label('gameplay_pc_01cb16')
    e.ins('add.w','0xefba:w,%d0',4)
    e.label('gameplay_pc_01cb1a')
    e.ins('subi.w','#0xa,%d0',4)
    e.label('gameplay_pc_01cb1e')
    e.ins('bls.w','gameplay_pc_01cb26',4)
    e.label('gameplay_pc_01cb22')
    e.ins('bsr.w','gameplay_pc_01c8bc',4)
    e.label('gameplay_pc_01cb26')
    e.ins('lea.l','0xaf56:w,%a0',4)
    e.label('gameplay_pc_01cb2a')
    e.ins('move.w','(%a0),%d0',2)
    e.label('gameplay_pc_01cb2c')
    e.ins('bmi.w','gameplay_pc_01cb38',4)
    e.label('gameplay_pc_01cb30')
    e.ins('bset.l','#0xe,%d0',4)
    e.label('gameplay_pc_01cb34')
    e.ins('move.w','%d0,(%a0)+',2)
    e.label('gameplay_pc_01cb36')
    e.ins('bra.b','gameplay_pc_01cb2a',2)
    e.label('gameplay_pc_01cb38')
    e.ins('tst.w','0xaf56:w',4)
    e.label('gameplay_pc_01cb3c')
    e.ins('bmi.w','gameplay_pc_01cb80',4)
    e.label('gameplay_pc_01cb40')
    e.ins('move.b','0xf68d:w,0xefe2:w',6)
    e.label('gameplay_pc_01cb46')
    e.ins('bsr.w','gameplay_pc_01c9fe',4)
    e.label('gameplay_pc_01cb4a')
    e.ins('bcs.w','gameplay_pc_01cb60',4)
    e.label('gameplay_pc_01cb4e')
    e.ins('clr.w','0xf6d6:w',4)
    e.label('gameplay_pc_01cb52')
    e.ins('jsr','gameplay_pc_021514:l',6)
    e.label('gameplay_pc_01cb58')
    e.ins('bsr.w','gameplay_pc_01ca60',4)
    e.label('gameplay_pc_01cb5c')
    e.ins('bra.w','gameplay_pc_01cb80',4)
    e.label('gameplay_pc_01cb60')
    e.ins('lea.l','0xaf56:w,%a0',4)
    e.label('gameplay_pc_01cb64')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01cb68')
    e.ins('bset.l','#0x7,%d0',4)
    e.label('gameplay_pc_01cb6c')
    e.ins('lea.l','0xcc00:w,%a1',4)
    e.label('gameplay_pc_01cb70')
    e.ins('move.w','(%a0)+,%d1',2)
    e.label('gameplay_pc_01cb72')
    e.ins('bmi.w','gameplay_pc_01cb80',4)
    e.label('gameplay_pc_01cb76')
    e.ins('andi.w','#0xff,%d1',4)
    e.label('gameplay_pc_01cb7a')
    e.ins('move.b','%d0,(%a1, %d1.w)',4)
    e.label('gameplay_pc_01cb7e')
    e.ins('bra.b','gameplay_pc_01cb70',2)
    e.label('gameplay_pc_01cb80')
    e.ins('lea.l','0xe640:w,%a0',4)
    e.label('gameplay_pc_01cb84')
    e.ins('move.w','0xf68e:w,%d0',4)
    e.label('gameplay_pc_01cb88')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01cb8a')
    e.ins('move.w','(%a0, %d0.w),0xf3f2:w',6)
    e.label('gameplay_pc_01cb90')
    e.ins('bsr.w','gameplay_pc_01ca3c',4)
    e.label('gameplay_pc_01cb94')
    e.ins('rts','',2)

def _lower_settle_battle_packed_armies(e,rules):
    e.label('gameplay_pc_01d03c')
    e.ins('bsr.w','gameplay_pc_01d198',4)
    e.label('gameplay_pc_01d040')
    e.ins('movea.l','0xff382c:l,%a1',6)
    e.label('gameplay_pc_01d046')
    e.ins('lea.l','0x9000:w,%a2',4)
    e.label('gameplay_pc_01d04a')
    e.ins('lea.l','0xefbe:w,%a3',4)
    e.label('gameplay_pc_01d04e')
    e.ins('move.w','0xefc6:w,%d0',4)
    e.label('gameplay_pc_01d052')
    e.ins('adda.w','(%a3, %d0.w),%a2',4)
    e.label('gameplay_pc_01d056')
    e.ins('lea.l','0xb200:w,%a0',4)
    e.label('gameplay_pc_01d05a')
    e.ins('move.w','0xf702:w,%d0',4)
    e.label('gameplay_pc_01d05e')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01d060')
    e.ins('tst.w','(%a0, %d0.w)',4)
    e.label('gameplay_pc_01d064')
    e.ins('bne.w','gameplay_pc_01d076',4)
    e.label('gameplay_pc_01d068')
    e.ins('move.w','0xf702:w,%d0',4)
    e.label('gameplay_pc_01d06c')
    e.ins('bsr.w','gameplay_pc_01d0a2',4)
    e.label('gameplay_pc_01d070')
    e.ins('clr.l','0xff382c:l',6)
    e.label('gameplay_pc_01d076')
    e.ins('exg','%a1,%a2',2)
    e.label('gameplay_pc_01d078')
    e.ins('lea.l','0xb200:w,%a0',4)
    e.label('gameplay_pc_01d07c')
    e.ins('move.w','0xf706:w,%d0',4)
    e.label('gameplay_pc_01d080')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01d082')
    e.ins('tst.w','(%a0, %d0.w)',4)
    e.label('gameplay_pc_01d086')
    e.ins('bne.w','gameplay_pc_01d098',4)
    e.label('gameplay_pc_01d08a')
    e.ins('move.w','0xf706:w,%d0',4)
    e.label('gameplay_pc_01d08e')
    e.ins('bsr.w','gameplay_pc_01d0a2',4)
    e.label('gameplay_pc_01d092')
    e.ins('move.l','%a2,0xff382c:l',6)
    e.label('gameplay_pc_01d098')
    e.ins('bsr.w','gameplay_pc_01d3bc',4)
    e.label('gameplay_pc_01d09c')
    e.ins('bsr.w','gameplay_pc_01d4da',4)
    e.label('gameplay_pc_01d0a0')
    e.ins('rts','',2)

def _lower_remove_defeated_packed_member(e,rules):
    e.label('gameplay_pc_01d0a2')
    e.ins('movem.l','%d1-%d4/%a0-%a2,-(%a7)',4)
    e.label('gameplay_pc_01d0a6')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('gameplay_pc_01d0aa')
    e.ins('move.b','#0xff,(%a0, %d0.w)',6)
    e.label('gameplay_pc_01d0b0')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_01d0b2')
    e.ins('move.b','0xd(%a1),%d3',4)
    e.label('gameplay_pc_01d0b6')
    e.ins('lea.l','(%a1),%a0',2)
    e.label('gameplay_pc_01d0b8')
    e.ins('move.b','(%a1),%d1',2)
    e.label('gameplay_pc_01d0ba')
    e.ins('andi.w','#0xf,%d1',4)
    e.label('gameplay_pc_01d0be')
    e.ins('cmpi.w','#0x1,%d1',4)
    e.label('gameplay_pc_01d0c2')
    e.ins('beq.w','gameplay_pc_01d114',4)
    e.label('gameplay_pc_01d0c6')
    e.ins('subq.b','#0x1,(%a1)',2)
    e.label('gameplay_pc_01d0c8')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_01d0ca')
    e.ins('move.w','#0x1,%d5',4)
    e.label('gameplay_pc_01d0ce')
    e.ins('cmp.b','0xd(%a1, %d2.w),%d0',4)
    e.label('gameplay_pc_01d0d2')
    e.ins('beq.w','gameplay_pc_01d0da',4)
    e.label('gameplay_pc_01d0d6')
    e.ins('addq.w','#0x1,%d2',2)
    e.label('gameplay_pc_01d0d8')
    e.ins('bra.b','gameplay_pc_01d0ce',2)
    e.label('gameplay_pc_01d0da')
    e.ins('addq.w','#0x1,%d2',2)
    e.label('gameplay_pc_01d0dc')
    e.ins('cmp.w','%d2,%d1',2)
    e.label('gameplay_pc_01d0de')
    e.ins('beq.w','gameplay_pc_01d0ea',4)
    e.label('gameplay_pc_01d0e2')
    e.ins('move.b','0xd(%a1, %d2.w),0xc(%a1, %d2.w)',6)
    e.label('gameplay_pc_01d0e8')
    e.ins('bra.b','gameplay_pc_01d0da',2)
    e.label('gameplay_pc_01d0ea')
    e.ins('lea.l','0xd(%a1, %d1.w),%a2',4)
    e.label('gameplay_pc_01d0ee')
    e.ins('lea.l','0xc(%a1, %d1.w),%a1',4)
    e.label('gameplay_pc_01d0f2')
    e.ins('clr.w','%d4',2)
    e.label('gameplay_pc_01d0f4')
    e.ins('move.b','0xd(%a0),%d4',4)
    e.label('gameplay_pc_01d0f8')
    e.ins('move.b','(%a2),%d1',2)
    e.label('gameplay_pc_01d0fa')
    e.ins('andi.w','#0xf,%d1',4)
    e.label('gameplay_pc_01d0fe')
    e.ins('beq.w','gameplay_pc_01d10e',4)
    e.label('gameplay_pc_01d102')
    e.ins('addi.w','#0xc,%d1',4)
    e.label('gameplay_pc_01d106')
    e.ins('move.b','(%a2)+,(%a1)+',2)
    e.label('gameplay_pc_01d108')
    e.ins('dbra','%d1,gameplay_pc_01d106',4)
    e.label('gameplay_pc_01d10c')
    e.ins('bra.b','gameplay_pc_01d0f8',2)
    e.label('gameplay_pc_01d10e')
    e.ins('clr.b','(%a1)',2)
    e.label('gameplay_pc_01d110')
    e.ins('bra.w','gameplay_pc_01d122',4)
    e.label('gameplay_pc_01d114')
    e.ins('move.w','#0xffff,%d4',4)
    e.label('gameplay_pc_01d118')
    e.ins('move.w','#0xe,%d5',4)
    e.label('gameplay_pc_01d11c')
    e.ins('lea.l','0xd(%a1, %d1.w),%a2',4)
    e.label('gameplay_pc_01d120')
    e.ins('bra.b','gameplay_pc_01d0f8',2)
    e.label('gameplay_pc_01d122')
    e.ins('bsr.w','gameplay_pc_01d142',4)
    e.label('gameplay_pc_01d126')
    e.ins('movem.l','(%a7)+,%d1-%d4/%a0-%a2',4)
    e.label('gameplay_pc_01d12a')
    e.ins('exg','%d1,%a1',2)
    e.label('gameplay_pc_01d12c')
    e.ins('exg','%d2,%a2',2)
    e.label('gameplay_pc_01d12e')
    e.ins('cmp.l','%d1,%d2',2)
    e.label('gameplay_pc_01d130')
    e.ins('bcs.w','gameplay_pc_01d13c',4)
    e.label('gameplay_pc_01d134')
    e.ins('andi.l','#0xffff,%d5',6)
    e.label('gameplay_pc_01d13a')
    e.ins('sub.l','%d5,%d2',2)
    e.label('gameplay_pc_01d13c')
    e.ins('exg','%d1,%a1',2)
    e.label('gameplay_pc_01d13e')
    e.ins('exg','%d2,%a2',2)
    e.label('gameplay_pc_01d140')
    e.ins('rts','',2)

def _lower_replace_or_remove_group_references(e,rules):
    e.label('gameplay_pc_01d142')
    e.ins('cmp.w','%d3,%d4',2)
    e.label('gameplay_pc_01d144')
    e.ins('beq.w','gameplay_pc_01d196',4)
    e.label('gameplay_pc_01d148')
    e.ins('lea.l','0xff39b2:l,%a0',6)
    e.label('gameplay_pc_01d14e')
    e.ins('adda.w','0xff3bb2:l,%a0',6)
    e.label('gameplay_pc_01d154')
    e.ins('tst.b','(%a0)+',2)
    e.label('gameplay_pc_01d156')
    e.ins('beq.w','gameplay_pc_01d196',4)
    e.label('gameplay_pc_01d15a')
    e.ins('cmp.b','(%a0)+,%d3',2)
    e.label('gameplay_pc_01d15c')
    e.ins('bne.b','gameplay_pc_01d154',2)
    e.label('gameplay_pc_01d15e')
    e.ins('tst.w','%d4',2)
    e.label('gameplay_pc_01d160')
    e.ins('bmi.w','gameplay_pc_01d188',4)
    e.label('gameplay_pc_01d164')
    e.ins('move.b','%d4,-0x1(%a0)',4)
    e.label('gameplay_pc_01d168')
    e.ins('lea.l','0xff3000:l,%a0',6)
    e.label('gameplay_pc_01d16e')
    e.ins('tst.b','(%a0)+',2)
    e.label('gameplay_pc_01d170')
    e.ins('bmi.w','gameplay_pc_01d196',4)
    e.label('gameplay_pc_01d174')
    e.ins('cmp.b','(%a0)+,%d3',2)
    e.label('gameplay_pc_01d176')
    e.ins('beq.w','gameplay_pc_01d180',4)
    e.label('gameplay_pc_01d17a')
    e.ins('tst.b','(%a0)+',2)
    e.label('gameplay_pc_01d17c')
    e.ins('bne.b','gameplay_pc_01d17a',2)
    e.label('gameplay_pc_01d17e')
    e.ins('bra.b','gameplay_pc_01d16e',2)
    e.label('gameplay_pc_01d180')
    e.ins('move.b','%d4,-0x1(%a0)',4)
    e.label('gameplay_pc_01d184')
    e.ins('bra.w','gameplay_pc_01d196',4)
    e.label('gameplay_pc_01d188')
    e.ins('lea.l','-0x2(%a0),%a1',4)
    e.label('gameplay_pc_01d18c')
    e.ins('move.b','(%a0)+,(%a1)+',2)
    e.label('gameplay_pc_01d18e')
    e.ins('beq.w','gameplay_pc_01d196',4)
    e.label('gameplay_pc_01d192')
    e.ins('move.b','(%a0)+,(%a1)+',2)
    e.label('gameplay_pc_01d194')
    e.ins('bra.b','gameplay_pc_01d18c',2)
    e.label('gameplay_pc_01d196')
    e.ins('rts','',2)

def _lower_transfer_outcome_officer(e,rules):
    e.label('gameplay_pc_01d198')
    e.ins('cmpi.w','#0x6,0xffff8114:l',8)
    e.label('gameplay_pc_01d1a0')
    e.ins('bcs.w','gameplay_pc_01d208',4)
    e.label('gameplay_pc_01d1a4')
    e.ins('beq.w','gameplay_pc_01d1b2',4)
    e.label('gameplay_pc_01d1a8')
    e.ins('move.w','0xffff80e2:l,%d0',6)
    e.label('gameplay_pc_01d1ae')
    e.ins('bra.w','gameplay_pc_01d1b8',4)
    e.label('gameplay_pc_01d1b2')
    e.ins('move.w','0xffff80e0:l,%d0',6)
    e.label('gameplay_pc_01d1b8')
    e.ins('movea.l','0xff382c:l,%a0',6)
    e.label('gameplay_pc_01d1be')
    e.ins('lea.l','0x9000:w,%a1',4)
    e.label('gameplay_pc_01d1c2')
    e.ins('lea.l','0xefbe:w,%a2',4)
    e.label('gameplay_pc_01d1c6')
    e.ins('move.w','0xefc6:w,%d1',4)
    e.label('gameplay_pc_01d1ca')
    e.ins('adda.w','(%a2, %d1.w),%a1',4)
    e.label('gameplay_pc_01d1ce')
    e.ins('cmp.w','0xf702:w,%d0',4)
    e.label('gameplay_pc_01d1d2')
    e.ins('beq.w','gameplay_pc_01d1d8',4)
    e.label('gameplay_pc_01d1d6')
    e.ins('exg','%a0,%a1',2)
    e.label('gameplay_pc_01d1d8')
    e.ins('move.w','%d0,-(%a7)',2)
    e.label('gameplay_pc_01d1da')
    e.ins('bsr.w','gameplay_pc_01d20a',4)
    e.label('gameplay_pc_01d1de')
    e.ins('bsr.w','gameplay_pc_01d318',4)
    e.label('gameplay_pc_01d1e2')
    e.ins('move.w','(%a7)+,%d0',2)
    e.label('gameplay_pc_01d1e4')
    e.ins('cmp.w','0xf702:w,%d0',4)
    e.label('gameplay_pc_01d1e8')
    e.ins('beq.w','gameplay_pc_01d1ee',4)
    e.label('gameplay_pc_01d1ec')
    e.ins('exg','%a0,%a1',2)
    e.label('gameplay_pc_01d1ee')
    e.ins('move.l','%a0,0xff382c:l',6)
    e.label('gameplay_pc_01d1f4')
    e.ins('exg','%d1,%a1',2)
    e.label('gameplay_pc_01d1f6')
    e.ins('subi.l','#0xffff9000,%d1',6)
    e.label('gameplay_pc_01d1fc')
    e.ins('lea.l','0xefbe:w,%a2',4)
    e.label('gameplay_pc_01d200')
    e.ins('move.w','0xefc6:w,%d0',4)
    e.label('gameplay_pc_01d204')
    e.ins('move.w','%d1,(%a2, %d0.w)',4)
    e.label('gameplay_pc_01d208')
    e.ins('rts','',2)

def _lower_detach_member_keep_group_cursor(e,rules):
    e.label('gameplay_pc_01d20a')
    e.ins('move.w','%d3,-(%a7)',2)
    e.label('gameplay_pc_01d20c')
    e.ins('movem.l','%d1-%d2/%a0-%a2,-(%a7)',4)
    e.label('gameplay_pc_01d210')
    e.ins('move.b','(%a0),%d1',2)
    e.label('gameplay_pc_01d212')
    e.ins('andi.w','#0xf,%d1',4)
    e.label('gameplay_pc_01d216')
    e.ins('cmpi.w','#0x1,%d1',4)
    e.label('gameplay_pc_01d21a')
    e.ins('beq.w','gameplay_pc_01d254',4)
    e.label('gameplay_pc_01d21e')
    e.ins('move.w','#0x1,%d3',4)
    e.label('gameplay_pc_01d222')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_01d224')
    e.ins('cmp.b','0xd(%a0, %d2.w),%d0',4)
    e.label('gameplay_pc_01d228')
    e.ins('beq.w','gameplay_pc_01d230',4)
    e.label('gameplay_pc_01d22c')
    e.ins('addq.w','#0x1,%d2',2)
    e.label('gameplay_pc_01d22e')
    e.ins('bra.b','gameplay_pc_01d224',2)
    e.label('gameplay_pc_01d230')
    e.ins('addq.w','#0x1,%d2',2)
    e.label('gameplay_pc_01d232')
    e.ins('cmp.w','%d1,%d2',2)
    e.label('gameplay_pc_01d234')
    e.ins('beq.w','gameplay_pc_01d242',4)
    e.label('gameplay_pc_01d238')
    e.ins('move.b','0xd(%a0, %d2.w),0xc(%a0, %d2.w)',6)
    e.label('gameplay_pc_01d23e')
    e.ins('addq.w','#0x1,%d2',2)
    e.label('gameplay_pc_01d240')
    e.ins('bra.b','gameplay_pc_01d232',2)
    e.label('gameplay_pc_01d242')
    e.ins('bsr.w','gameplay_pc_01d29e',4)
    e.label('gameplay_pc_01d246')
    e.ins('subq.b','#0x1,(%a0)',2)
    e.label('gameplay_pc_01d248')
    e.ins('lea.l','0xd(%a0, %d1.w),%a1',4)
    e.label('gameplay_pc_01d24c')
    e.ins('lea.l','0xc(%a0, %d1.w),%a2',4)
    e.label('gameplay_pc_01d250')
    e.ins('bra.w','gameplay_pc_01d268',4)
    e.label('gameplay_pc_01d254')
    e.ins('move.w','#0xe,%d3',4)
    e.label('gameplay_pc_01d258')
    e.ins('bsr.w','gameplay_pc_01d2e8',4)
    e.label('gameplay_pc_01d25c')
    e.ins('lea.l','0xd(%a0, %d1.w),%a1',4)
    e.label('gameplay_pc_01d260')
    e.ins('movea.l','%a0,%a2',2)
    e.label('gameplay_pc_01d262')
    e.ins('movea.l','#0x0,%a0',6)
    e.label('gameplay_pc_01d268')
    e.ins('move.b','(%a1),%d1',2)
    e.label('gameplay_pc_01d26a')
    e.ins('andi.w','#0xf,%d1',4)
    e.label('gameplay_pc_01d26e')
    e.ins('beq.w','gameplay_pc_01d27e',4)
    e.label('gameplay_pc_01d272')
    e.ins('addi.w','#0xc,%d1',4)
    e.label('gameplay_pc_01d276')
    e.ins('move.b','(%a1)+,(%a2)+',2)
    e.label('gameplay_pc_01d278')
    e.ins('dbra','%d1,gameplay_pc_01d276',4)
    e.label('gameplay_pc_01d27c')
    e.ins('bra.b','gameplay_pc_01d268',2)
    e.label('gameplay_pc_01d27e')
    e.ins('clr.b','(%a2)',2)
    e.label('gameplay_pc_01d280')
    e.ins('movem.l','(%a7)+,%d1-%d2/%a0-%a2',4)
    e.label('gameplay_pc_01d284')
    e.ins('exg','%d0,%a0',2)
    e.label('gameplay_pc_01d286')
    e.ins('exg','%d1,%a1',2)
    e.label('gameplay_pc_01d288')
    e.ins('cmp.l','%d0,%d1',2)
    e.label('gameplay_pc_01d28a')
    e.ins('bcs.w','gameplay_pc_01d296',4)
    e.label('gameplay_pc_01d28e')
    e.ins('andi.l','#0xffff,%d3',6)
    e.label('gameplay_pc_01d294')
    e.ins('sub.l','%d3,%d1',2)
    e.label('gameplay_pc_01d296')
    e.ins('exg','%d0,%a0',2)
    e.label('gameplay_pc_01d298')
    e.ins('exg','%d1,%a1',2)
    e.label('gameplay_pc_01d29a')
    e.ins('move.w','(%a7)+,%d3',2)
    e.label('gameplay_pc_01d29c')
    e.ins('rts','',2)

def _lower_replace_group_head_reference(e,rules):
    e.label('gameplay_pc_01d29e')
    e.ins('move.w','%d1,-(%a7)',2)
    e.label('gameplay_pc_01d2a0')
    e.ins('move.b','0xd(%a0),%d1',4)
    e.label('gameplay_pc_01d2a4')
    e.ins('andi.w','#0xff,%d1',4)
    e.label('gameplay_pc_01d2a8')
    e.ins('lea.l','0xff39b2:l,%a1',6)
    e.label('gameplay_pc_01d2ae')
    e.ins('adda.w','0xff3bb2:l,%a1',6)
    e.label('gameplay_pc_01d2b4')
    e.ins('tst.b','(%a1)',2)
    e.label('gameplay_pc_01d2b6')
    e.ins('beq.w','gameplay_pc_01d2e4',4)
    e.label('gameplay_pc_01d2ba')
    e.ins('cmp.b','0x1(%a1),%d0',4)
    e.label('gameplay_pc_01d2be')
    e.ins('beq.w','gameplay_pc_01d2c6',4)
    e.label('gameplay_pc_01d2c2')
    e.ins('addq.w','#0x2,%a1',2)
    e.label('gameplay_pc_01d2c4')
    e.ins('bra.b','gameplay_pc_01d2b4',2)
    e.label('gameplay_pc_01d2c6')
    e.ins('move.b','%d1,0x1(%a1)',4)
    e.label('gameplay_pc_01d2ca')
    e.ins('lea.l','0xff3000:l,%a1',6)
    e.label('gameplay_pc_01d2d0')
    e.ins('cmp.b','0x1(%a1),%d0',4)
    e.label('gameplay_pc_01d2d4')
    e.ins('beq.w','gameplay_pc_01d2e0',4)
    e.label('gameplay_pc_01d2d8')
    e.ins('addq.w','#0x1,%a1',2)
    e.label('gameplay_pc_01d2da')
    e.ins('tst.b','(%a1)+',2)
    e.label('gameplay_pc_01d2dc')
    e.ins('bne.b','gameplay_pc_01d2da',2)
    e.label('gameplay_pc_01d2de')
    e.ins('bra.b','gameplay_pc_01d2d0',2)
    e.label('gameplay_pc_01d2e0')
    e.ins('move.b','%d1,0x1(%a1)',4)
    e.label('gameplay_pc_01d2e4')
    e.ins('move.w','(%a7)+,%d1',2)
    e.label('gameplay_pc_01d2e6')
    e.ins('rts','',2)

def _lower_remove_group_reference(e,rules):
    e.label('gameplay_pc_01d2e8')
    e.ins('lea.l','0xff39b2:l,%a1',6)
    e.label('gameplay_pc_01d2ee')
    e.ins('adda.w','0xff3bb2:l,%a1',6)
    e.label('gameplay_pc_01d2f4')
    e.ins('tst.b','(%a1)',2)
    e.label('gameplay_pc_01d2f6')
    e.ins('beq.w','gameplay_pc_01d316',4)
    e.label('gameplay_pc_01d2fa')
    e.ins('cmp.b','0x1(%a1),%d0',4)
    e.label('gameplay_pc_01d2fe')
    e.ins('beq.w','gameplay_pc_01d308',4)
    e.label('gameplay_pc_01d302')
    e.ins('adda.w','#0x2,%a1',4)
    e.label('gameplay_pc_01d306')
    e.ins('bra.b','gameplay_pc_01d2f4',2)
    e.label('gameplay_pc_01d308')
    e.ins('lea.l','0x2(%a1),%a2',4)
    e.label('gameplay_pc_01d30c')
    e.ins('move.b','(%a2)+,(%a1)+',2)
    e.label('gameplay_pc_01d30e')
    e.ins('beq.w','gameplay_pc_01d316',4)
    e.label('gameplay_pc_01d312')
    e.ins('move.b','(%a2)+,(%a1)+',2)
    e.label('gameplay_pc_01d314')
    e.ins('bra.b','gameplay_pc_01d30c',2)
    e.label('gameplay_pc_01d316')
    e.ins('rts','',2)

def _lower_attach_member_shift_packet(e,rules):
    e.label('gameplay_pc_01d318')
    e.ins('move.l','%a2,-(%a7)',2)
    e.label('gameplay_pc_01d31a')
    e.ins('move.b','(%a1),%d1',2)
    e.label('gameplay_pc_01d31c')
    e.ins('andi.w','#0xf,%d1',4)
    e.label('gameplay_pc_01d320')
    e.ins('cmpi.w','#0xa,%d1',4)
    e.label('gameplay_pc_01d324')
    e.ins('beq.w','gameplay_pc_01d374',4)
    e.label('gameplay_pc_01d328')
    e.ins('lea.l','0xd(%a1, %d1.w),%a2',4)
    e.label('gameplay_pc_01d32c')
    e.ins('lea.l','0xe(%a1, %d1.w),%a3',4)
    e.label('gameplay_pc_01d330')
    e.ins('move.b','(%a2),%d1',2)
    e.label('gameplay_pc_01d332')
    e.ins('move.b','%d1,%d2',2)
    e.label('gameplay_pc_01d334')
    e.ins('andi.w','#0xf,%d2',4)
    e.label('gameplay_pc_01d338')
    e.ins('beq.w','gameplay_pc_01d34c',4)
    e.label('gameplay_pc_01d33c')
    e.ins('addi.w','#0xc,%d2',4)
    e.label('gameplay_pc_01d340')
    e.ins('move.b','(%a3),%d3',2)
    e.label('gameplay_pc_01d342')
    e.ins('move.b','%d1,(%a3)+',2)
    e.label('gameplay_pc_01d344')
    e.ins('move.b','%d3,%d1',2)
    e.label('gameplay_pc_01d346')
    e.ins('dbra','%d2,gameplay_pc_01d340',4)
    e.label('gameplay_pc_01d34a')
    e.ins('bra.b','gameplay_pc_01d332',2)
    e.label('gameplay_pc_01d34c')
    e.ins('clr.b','(%a3)',2)
    e.label('gameplay_pc_01d34e')
    e.ins('move.b','(%a1),%d1',2)
    e.label('gameplay_pc_01d350')
    e.ins('andi.w','#0xf,%d1',4)
    e.label('gameplay_pc_01d354')
    e.ins('addq.b','#0x1,(%a1)',2)
    e.label('gameplay_pc_01d356')
    e.ins('move.b','%d0,0xd(%a1, %d1.w)',4)
    e.label('gameplay_pc_01d35a')
    e.ins('lea.l','0xcc00:w,%a2',4)
    e.label('gameplay_pc_01d35e')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_01d360')
    e.ins('move.b','0x4(%a1),%d3',4)
    e.label('gameplay_pc_01d364')
    e.ins('addi.w','#0x29,%d3',4)
    e.label('gameplay_pc_01d368')
    e.ins('move.b','%d3,(%a2, %d0.w)',4)
    e.label('gameplay_pc_01d36c')
    e.ins('move.w','#0x1,%d3',4)
    e.label('gameplay_pc_01d370')
    e.ins('bra.w','gameplay_pc_01d3a2',4)
    e.label('gameplay_pc_01d374')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_01d376')
    e.ins('lea.l','0xcc00:w,%a2',4)
    e.label('gameplay_pc_01d37a')
    e.ins('move.b','(%a2, %d0.w),%d1',4)
    e.label('gameplay_pc_01d37e')
    e.ins('andi.w','#0x3f,%d1',4)
    e.label('gameplay_pc_01d382')
    e.ins('cmpi.w','#0x28,%d1',4)
    e.label('gameplay_pc_01d386')
    e.ins('bhi.w','gameplay_pc_01d396',4)
    e.label('gameplay_pc_01d38a')
    e.ins('bset.l','#0x7,%d1',4)
    e.label('gameplay_pc_01d38e')
    e.ins('move.b','%d1,(%a2, %d1.w)',4)
    e.label('gameplay_pc_01d392')
    e.ins('bra.w','gameplay_pc_01d3a2',4)
    e.label('gameplay_pc_01d396')
    e.ins('subi.w','#0x28,%d1',4)
    e.label('gameplay_pc_01d39a')
    e.ins('bset.l','#0x7,%d1',4)
    e.label('gameplay_pc_01d39e')
    e.ins('move.b','%d1,(%a2, %d0.w)',4)
    e.label('gameplay_pc_01d3a2')
    e.ins('exg','%d0,%a0',2)
    e.label('gameplay_pc_01d3a4')
    e.ins('exg','%d1,%a1',2)
    e.label('gameplay_pc_01d3a6')
    e.ins('cmp.l','%d1,%d0',2)
    e.label('gameplay_pc_01d3a8')
    e.ins('bcs.w','gameplay_pc_01d3b4',4)
    e.label('gameplay_pc_01d3ac')
    e.ins('andi.l','#0xffff,%d3',6)
    e.label('gameplay_pc_01d3b2')
    e.ins('add.l','%d3,%d0',2)
    e.label('gameplay_pc_01d3b4')
    e.ins('exg','%d0,%a0',2)
    e.label('gameplay_pc_01d3b6')
    e.ins('exg','%d1,%a1',2)
    e.label('gameplay_pc_01d3b8')
    e.ins('movea.l','(%a7)+,%a2',2)
    e.label('gameplay_pc_01d3ba')
    e.ins('rts','',2)

def _lower_settle_group_at_city(e,rules):
    e.label('gameplay_pc_01d3bc')
    e.ins('tst.l','0xff382c:l',6)
    e.label('gameplay_pc_01d3c2')
    e.ins('beq.w','gameplay_pc_01d40a',4)
    e.label('gameplay_pc_01d3c6')
    e.ins('movea.l','0xff382c:l,%a0',6)
    e.label('gameplay_pc_01d3cc')
    e.ins('clr.w','%d0',2)
    e.label('gameplay_pc_01d3ce')
    e.ins('move.b','0x1(%a0),%d0',4)
    e.label('gameplay_pc_01d3d2')
    e.ins('clr.w','%d1',2)
    e.label('gameplay_pc_01d3d4')
    e.ins('move.b','0x2(%a0),%d1',4)
    e.label('gameplay_pc_01d3d8')
    e.ins('jsr','gameplay_pc_0142a2:l',6)
    e.label('gameplay_pc_01d3de')
    e.ins('tst.b','%d3',2)
    e.label('gameplay_pc_01d3e0')
    e.ins('bpl.w','gameplay_pc_01d40a',4)
    e.label('gameplay_pc_01d3e4')
    e.ins('bsr.w','gameplay_pc_01d40c',4)
    e.label('gameplay_pc_01d3e8')
    e.ins('move.b','(%a0),%d0',2)
    e.label('gameplay_pc_01d3ea')
    e.ins('andi.w','#0xf,%d0',4)
    e.label('gameplay_pc_01d3ee')
    e.ins('subq.w','#0x1,%d0',2)
    e.label('gameplay_pc_01d3f0')
    e.ins('lea.l','0xcc00:w,%a1',4)
    e.label('gameplay_pc_01d3f4')
    e.ins('clr.w','%d1',2)
    e.label('gameplay_pc_01d3f6')
    e.ins('move.b','0xd(%a0, %d0.w),%d1',4)
    e.label('gameplay_pc_01d3fa')
    e.ins('move.b','%d3,(%a1, %d1.w)',4)
    e.label('gameplay_pc_01d3fe')
    e.ins('dbra','%d0,gameplay_pc_01d3f4',4)
    e.label('gameplay_pc_01d402')
    e.ins('bsr.w','gameplay_pc_01d44c',4)
    e.label('gameplay_pc_01d406')
    e.ins('bsr.w','gameplay_pc_01d4b8',4)
    e.label('gameplay_pc_01d40a')
    e.ins('rts','',2)

def _lower_locate_group_city(e,rules):
    e.label('gameplay_pc_01d40c')
    e.ins('clr.w','%d0',2)
    e.label('gameplay_pc_01d40e')
    e.ins('move.b','0x1(%a0),%d0',4)
    e.label('gameplay_pc_01d412')
    e.ins('lsl.w','#0x4,%d0',2)
    e.label('gameplay_pc_01d414')
    e.ins('addq.w','#0x8,%d0',2)
    e.label('gameplay_pc_01d416')
    e.ins('clr.w','%d1',2)
    e.label('gameplay_pc_01d418')
    e.ins('move.b','0x2(%a0),%d1',4)
    e.label('gameplay_pc_01d41c')
    e.ins('lsl.w','#0x4,%d1',2)
    e.label('gameplay_pc_01d41e')
    e.ins('move.w','%d1,%d2',2)
    e.label('gameplay_pc_01d420')
    e.ins('subi.w','#0x10,%d2',4)
    e.label('gameplay_pc_01d424')
    e.ins('lea.l','0xd4aca:l,%a1',6)
    e.label('gameplay_pc_01d42a')
    e.ins('move.w','#0x1,%d3',4)
    e.label('gameplay_pc_01d42e')
    e.ins('cmp.w','0x2(%a1),%d0',4)
    e.label('gameplay_pc_01d432')
    e.ins('bne.w','gameplay_pc_01d444',4)
    e.label('gameplay_pc_01d436')
    e.ins('cmp.w','(%a1),%d1',2)
    e.label('gameplay_pc_01d438')
    e.ins('beq.w','gameplay_pc_01d44a',4)
    e.label('gameplay_pc_01d43c')
    e.ins('cmp.w','0x2(%a1),%d2',4)
    e.label('gameplay_pc_01d440')
    e.ins('beq.w','gameplay_pc_01d44a',4)
    e.label('gameplay_pc_01d444')
    e.ins('addq.w','#0x4,%a1',2)
    e.label('gameplay_pc_01d446')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('gameplay_pc_01d448')
    e.ins('bra.b','gameplay_pc_01d42e',2)
    e.label('gameplay_pc_01d44a')
    e.ins('rts','',2)

def _lower_credit_packed_group_resources(e,rules):
    e.label('gameplay_pc_01d44c')
    e.ins('lsl.w','#0x2,%d3',2)
    e.label('gameplay_pc_01d44e')
    e.ins('move.b','0x5(%a0),%d0',4)
    e.label('gameplay_pc_01d452')
    e.ins('lsl.w','#0x8,%d0',2)
    e.label('gameplay_pc_01d454')
    e.ins('move.b','0x6(%a0),%d0',4)
    e.label('gameplay_pc_01d458')
    e.ins('lsl.l','#0x8,%d0',2)
    e.label('gameplay_pc_01d45a')
    e.ins('move.b','0x7(%a0),%d0',4)
    e.label('gameplay_pc_01d45e')
    e.ins('lsl.l','#0x8,%d0',2)
    e.label('gameplay_pc_01d460')
    e.ins('move.b','0x8(%a0),%d0',4)
    e.label('gameplay_pc_01d464')
    e.ins('lea.l','0xdffc:w,%a1',4)
    e.label('gameplay_pc_01d468')
    e.ins('move.l','(%a1, %d3.w),%d1',4)
    e.label('gameplay_pc_01d46c')
    e.ins('add.l','%d0,%d1',2)
    e.label('gameplay_pc_01d46e')
    e.ins('cmpi.l','#0xf423f,%d1',6)
    e.label('gameplay_pc_01d474')
    e.ins('bls.w','gameplay_pc_01d47e',4)
    e.label('gameplay_pc_01d478')
    e.ins('move.l','#0xf423f,%d1',6)
    e.label('gameplay_pc_01d47e')
    e.ins('move.l','%d1,(%a1, %d3.w)',4)
    e.label('gameplay_pc_01d482')
    e.ins('move.b','0x9(%a0),%d0',4)
    e.label('gameplay_pc_01d486')
    e.ins('lsl.w','#0x8,%d0',2)
    e.label('gameplay_pc_01d488')
    e.ins('move.b','0xa(%a0),%d0',4)
    e.label('gameplay_pc_01d48c')
    e.ins('lsl.l','#0x8,%d0',2)
    e.label('gameplay_pc_01d48e')
    e.ins('move.b','0xb(%a0),%d0',4)
    e.label('gameplay_pc_01d492')
    e.ins('lsl.l','#0x8,%d0',2)
    e.label('gameplay_pc_01d494')
    e.ins('move.b','0xc(%a0),%d0',4)
    e.label('gameplay_pc_01d498')
    e.ins('lea.l','0xe09c:w,%a1',4)
    e.label('gameplay_pc_01d49c')
    e.ins('move.l','(%a1, %d3.w),%d1',4)
    e.label('gameplay_pc_01d4a0')
    e.ins('add.l','%d0,%d1',2)
    e.label('gameplay_pc_01d4a2')
    e.ins('cmpi.l','#0xf423f,%d1',6)
    e.label('gameplay_pc_01d4a8')
    e.ins('bls.w','gameplay_pc_01d4b2',4)
    e.label('gameplay_pc_01d4ac')
    e.ins('move.l','#0xf423f,%d1',6)
    e.label('gameplay_pc_01d4b2')
    e.ins('move.l','%d1,(%a1, %d3.w)',4)
    e.label('gameplay_pc_01d4b6')
    e.ins('rts','',2)

def _lower_erase_group_packet(e,rules):
    e.label('gameplay_pc_01d4b8')
    e.ins('move.b','(%a0),%d0',2)
    e.label('gameplay_pc_01d4ba')
    e.ins('andi.w','#0xf,%d0',4)
    e.label('gameplay_pc_01d4be')
    e.ins('lea.l','0xd(%a0, %d0.w),%a1',4)
    e.label('gameplay_pc_01d4c2')
    e.ins('move.b','(%a1),%d0',2)
    e.label('gameplay_pc_01d4c4')
    e.ins('andi.w','#0xf,%d0',4)
    e.label('gameplay_pc_01d4c8')
    e.ins('beq.w','gameplay_pc_01d4d6',4)
    e.label('gameplay_pc_01d4cc')
    e.ins('addi.w','#0xc,%d0',4)
    e.label('gameplay_pc_01d4d0')
    e.ins('move.b','(%a1)+,(%a0)+',2)
    e.label('gameplay_pc_01d4d2')
    e.ins('dbra','%d0,gameplay_pc_01d4d0',4)
    e.label('gameplay_pc_01d4d6')
    e.ins('clr.b','(%a0)',2)
    e.label('gameplay_pc_01d4d8')
    e.ins('rts','',2)

def _lower_adjust_battle_losing_loyalty(e,rules):
    e.label('gameplay_pc_01d4da')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01d4e0')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01d4e6')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_01d4e8')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_01d4ea')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01d4ec')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01d4ee')
    e.ins('addq.w','#0x1,%d0',2)
    e.label('gameplay_pc_01d4f0')
    e.ins('lea.l','0xc500:w,%a0',4)
    e.label('gameplay_pc_01d4f4')
    e.ins('cmpi.w','#0x5,0xffff8114:l',8)
    e.label('gameplay_pc_01d4fc')
    e.ins('beq.w','gameplay_pc_01d528',4)
    e.label('gameplay_pc_01d500')
    e.ins('cmpi.w','#0x4,0xffff8114:l',8)
    e.label('gameplay_pc_01d508')
    e.ins('bne.w','gameplay_pc_01d540',4)
    e.label('gameplay_pc_01d50c')
    e.ins('move.w','0xffff80e0:l,%d1',6)
    e.label('gameplay_pc_01d512')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_01d514')
    e.ins('move.b','(%a0, %d1.w),%d2',4)
    e.label('gameplay_pc_01d518')
    e.ins('sub.w','%d0,%d2',2)
    e.label('gameplay_pc_01d51a')
    e.ins('bcc.w','gameplay_pc_01d520',4)
    e.label('gameplay_pc_01d51e')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_01d520')
    e.ins('move.b','%d2,(%a0, %d1.w)',4)
    e.label('gameplay_pc_01d524')
    e.ins('bra.w','gameplay_pc_01d540',4)
    e.label('gameplay_pc_01d528')
    e.ins('move.w','0xffff80e2:l,%d1',6)
    e.label('gameplay_pc_01d52e')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_01d530')
    e.ins('move.b','(%a0, %d1.w),%d2',4)
    e.label('gameplay_pc_01d534')
    e.ins('sub.w','%d0,%d2',2)
    e.label('gameplay_pc_01d536')
    e.ins('bcc.w','gameplay_pc_01d53c',4)
    e.label('gameplay_pc_01d53a')
    e.ins('clr.w','%d2',2)
    e.label('gameplay_pc_01d53c')
    e.ins('move.b','%d2,(%a0, %d1.w)',4)
    e.label('gameplay_pc_01d540')
    e.ins('rts','',2)

def _lower_initialize_prebattle_head_bytes(e,rules):
    e.label('gameplay_pc_01d57a')
    e.ins('lea.l','0xe640:w,%a0',4)
    e.label('gameplay_pc_01d57e')
    e.ins('lea.l','0xc300:w,%a1',4)
    e.label('gameplay_pc_01d582')
    e.ins('move.w','#0xf,%d0',4)
    e.label('gameplay_pc_01d586')
    e.ins('move.w','(%a0)+,%d1',2)
    e.label('gameplay_pc_01d588')
    e.ins('bmi.w','gameplay_pc_01d592',4)
    e.label('gameplay_pc_01d58c')
    e.ins('move.b','#0x64,(%a1, %d1.w)',6)
    e.label('gameplay_pc_01d592')
    e.ins('dbra','%d0,gameplay_pc_01d586',4)
    e.label('gameplay_pc_01d596')
    e.ins('rts','',2)

def _lower_apply_returning_officer_loyalty(e,rules):
    e.label('gameplay_pc_0208ce')
    e.ins('movem.l','%d0-%d4/%a0-%a1,-(%a7)',4)
    e.label('gameplay_pc_0208d2')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_0208d8')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_0208de')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_0208e0')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('gameplay_pc_0208e2')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_0208e4')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_0208e6')
    e.ins('addi.w','#0x6,%d0',4)
    e.label('gameplay_pc_0208ea')
    e.ins('lea.l','0xc300:w,%a0',4)
    e.label('gameplay_pc_0208ee')
    e.ins('move.w','#0x68,%d1',4)
    e.label('gameplay_pc_0208f2')
    e.ins('move.w','0xf3a6:w,%d2',4)
    e.label('gameplay_pc_0208f6')
    e.ins('andi.w','#0xff,%d2',4)
    e.label('gameplay_pc_0208fa')
    e.ins('sub.b','(%a0, %d2.w),%d1',4)
    e.label('gameplay_pc_0208fe')
    e.ins('lsr.w','#0x1,%d1',2)
    e.label('gameplay_pc_020900')
    e.ins('lea.l','0xc200:w,%a1',4)
    e.label('gameplay_pc_020904')
    e.ins('move.w','0xf3f2:w,%d4',4)
    e.label('gameplay_pc_020908')
    e.ins('andi.w','#0xff,%d4',4)
    e.label('gameplay_pc_02090c')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_02090e')
    e.ins('move.b','(%a1, %d4.w),%d3',4)
    e.label('gameplay_pc_020912')
    e.ins('mulu.w','%d3,%d1',2)
    e.label('gameplay_pc_020914')
    e.ins('mulu.w','%d0,%d1',2)
    e.label('gameplay_pc_020916')
    e.ins('divu.w','#0x1f4,%d1',4)
    e.label('gameplay_pc_02091a')
    e.ins('cmpi.w','#0x64,%d1',4)
    e.label('gameplay_pc_02091e')
    e.ins('bls.w','gameplay_pc_020926',4)
    e.label('gameplay_pc_020922')
    e.ins('move.w','#0x64,%d1',4)
    e.label('gameplay_pc_020926')
    e.ins('move.b','%d1,(%a0, %d2.w)',4)
    e.label('gameplay_pc_02092a')
    e.ins('movem.l','(%a7)+,%d0-%d4/%a0-%a1',4)
    e.label('gameplay_pc_02092e')
    e.ins('rts','',2)

def _lower_append_group_from_survivor_roster(e,rules):
    e.label('gameplay_pc_021514')
    e.ins('lea.l','0x9000:w,%a0',4)
    e.label('gameplay_pc_021518')
    e.ins('lea.l','0xcc00:w,%a2',4)
    e.label('gameplay_pc_02151c')
    e.ins('move.b','(%a0),%d0',2)
    e.label('gameplay_pc_02151e')
    e.ins('andi.w','#0xf,%d0',4)
    e.label('gameplay_pc_021522')
    e.ins('beq.w','gameplay_pc_02152c',4)
    e.label('gameplay_pc_021526')
    e.ins('lea.l','0xd(%a0, %d0.w),%a0',4)
    e.label('gameplay_pc_02152a')
    e.ins('bra.b','gameplay_pc_02151c',2)
    e.label('gameplay_pc_02152c')
    e.ins('clr.w','%d0',2)
    e.label('gameplay_pc_02152e')
    e.ins('lea.l','0xaf56:w,%a1',4)
    e.label('gameplay_pc_021532')
    e.ins('move.w','(%a1)+,%d1',2)
    e.label('gameplay_pc_021534')
    e.ins('bmi.w','gameplay_pc_021550',4)
    e.label('gameplay_pc_021538')
    e.ins('btst.l','#0xe,%d1',4)
    e.label('gameplay_pc_02153c')
    e.ins('beq.b','gameplay_pc_021532',2)
    e.label('gameplay_pc_02153e')
    e.ins('move.b','%d1,0xd(%a0, %d0.w)',4)
    e.label('gameplay_pc_021542')
    e.ins('addq.w','#0x1,%d0',2)
    e.label('gameplay_pc_021544')
    e.ins('andi.w','#0xff,%d1',4)
    e.label('gameplay_pc_021548')
    e.ins('bset.b','#0x6,(%a2, %d1.w)',6)
    e.label('gameplay_pc_02154e')
    e.ins('bra.b','gameplay_pc_021532',2)
    e.label('gameplay_pc_021550')
    e.ins('clr.b','0xd(%a0, %d0.w)',4)
    e.label('gameplay_pc_021554')
    e.ins('move.b','%d0,(%a0)',2)
    e.label('gameplay_pc_021556')
    e.ins('btst.b','#0x1,0xf6d7:w',6)
    e.label('gameplay_pc_02155c')
    e.ins('bne.w','gameplay_pc_021568',4)
    e.label('gameplay_pc_021560')
    e.ins('move.w','0xf68c:w,%d1',4)
    e.label('gameplay_pc_021564')
    e.ins('bra.w','gameplay_pc_02156c',4)
    e.label('gameplay_pc_021568')
    e.ins('move.w','0xf68e:w,%d1',4)
    e.label('gameplay_pc_02156c')
    e.ins('move.b','%d1,0x4(%a0)',4)
    e.label('gameplay_pc_021570')
    e.ins('lea.l','0xc400:w,%a1',4)
    e.label('gameplay_pc_021574')
    e.ins('move.w','%d0,%d1',2)
    e.label('gameplay_pc_021576')
    e.ins('subq.w','#0x1,%d1',2)
    e.label('gameplay_pc_021578')
    e.ins('moveq','#0,%d2',2)
    e.label('gameplay_pc_02157a')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_02157c')
    e.ins('move.b','0xd(%a0, %d1.w),%d3',4)
    e.label('gameplay_pc_021580')
    e.ins('move.b','(%a1, %d3.w),%d3',4)
    e.label('gameplay_pc_021584')
    e.ins('add.w','%d3,%d2',2)
    e.label('gameplay_pc_021586')
    e.ins('dbra','%d1,gameplay_pc_02157c',4)
    e.label('gameplay_pc_02158a')
    e.ins('divu.w','%d0,%d2',2)
    e.label('gameplay_pc_02158c')
    e.ins('move.b','%d2,0x3(%a0)',4)
    e.label('gameplay_pc_021590')
    e.ins('bsr.w','gameplay_pc_021efe',4)
    e.label('gameplay_pc_021594')
    e.ins('move.b','%d0,0x1(%a0)',4)
    e.label('gameplay_pc_021598')
    e.ins('move.b','%d1,0x2(%a0)',4)
    e.label('gameplay_pc_02159c')
    e.ins('rts','',2)

def _lower_choose_empty_neighbor_position(e,rules):
    e.label('gameplay_pc_021efe')
    e.ins('lea.l','130(%pc),%a6',4)
    e.label('gameplay_pc_021f02')
    e.ins('lea.l','0x670a:l,%a5',6)
    e.label('gameplay_pc_021f08')
    e.ins('lea.l','0xee5f0:l,%a4',6)
    e.label('gameplay_pc_021f0e')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_021f12')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_021f14')
    e.ins('lea.l','0xd4ac6:l,%a1',6)
    e.label('gameplay_pc_021f1a')
    e.ins('move.w','0x2(%a1, %d0.w),%d7',4)
    e.label('gameplay_pc_021f1e')
    e.ins('lsr.w','#0x4,%d7',2)
    e.label('gameplay_pc_021f20')
    e.ins('move.w','(%a1, %d0.w),%d6',4)
    e.label('gameplay_pc_021f24')
    e.ins('lsr.w','#0x4,%d6',2)
    e.label('gameplay_pc_021f26')
    e.ins('move.w','%d7,%d0',2)
    e.label('gameplay_pc_021f28')
    e.ins('add.w','(%a6),%d0',2)
    e.label('gameplay_pc_021f2a')
    e.ins('cmpi.w','#0x48,%d0',4)
    e.label('gameplay_pc_021f2e')
    e.ins('bcc.w','gameplay_pc_021f7a',4)
    e.label('gameplay_pc_021f32')
    e.ins('move.w','%d6,%d1',2)
    e.label('gameplay_pc_021f34')
    e.ins('add.w','0x2(%a6),%d1',4)
    e.label('gameplay_pc_021f38')
    e.ins('cmpi.w','#0x48,%d1',4)
    e.label('gameplay_pc_021f3c')
    e.ins('bcc.w','gameplay_pc_021f7a',4)
    e.label('gameplay_pc_021f40')
    e.ins('move.w','%d0,%d2',2)
    e.label('gameplay_pc_021f42')
    e.ins('lsl.w','#0x3,%d2',2)
    e.label('gameplay_pc_021f44')
    e.ins('add.w','%d0,%d2',2)
    e.label('gameplay_pc_021f46')
    e.ins('lsl.w','#0x3,%d2',2)
    e.label('gameplay_pc_021f48')
    e.ins('add.w','%d1,%d2',2)
    e.label('gameplay_pc_021f4a')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_021f4c')
    e.ins('move.b','(%a4, %d2.w),%d3',4)
    e.label('gameplay_pc_021f50')
    e.ins('tst.b','(%a5, %d3.w)',4)
    e.label('gameplay_pc_021f54')
    e.ins('bmi.b','gameplay_pc_021f7a',2)
    e.label('gameplay_pc_021f56')
    e.ins('lea.l','0x9000:w,%a1',4)
    e.label('gameplay_pc_021f5a')
    e.ins('move.b','(%a1),%d2',2)
    e.label('gameplay_pc_021f5c')
    e.ins('andi.w','#0xf,%d2',4)
    e.label('gameplay_pc_021f60')
    e.ins('beq.w','gameplay_pc_021f80',4)
    e.label('gameplay_pc_021f64')
    e.ins('cmp.b','0x1(%a1),%d0',4)
    e.label('gameplay_pc_021f68')
    e.ins('bne.w','gameplay_pc_021f74',4)
    e.label('gameplay_pc_021f6c')
    e.ins('cmp.b','0x2(%a1),%d1',4)
    e.label('gameplay_pc_021f70')
    e.ins('beq.w','gameplay_pc_021f7a',4)
    e.label('gameplay_pc_021f74')
    e.ins('lea.l','0xd(%a1, %d2.w),%a1',4)
    e.label('gameplay_pc_021f78')
    e.ins('bra.b','gameplay_pc_021f5a',2)
    e.label('gameplay_pc_021f7a')
    e.ins('adda.w','#0x4,%a6',4)
    e.label('gameplay_pc_021f7e')
    e.ins('bra.b','gameplay_pc_021f26',2)
    e.label('gameplay_pc_021f80')
    e.ins('rts','',2)

def _lower_rounded_radial_distance(e,rules):
    e.label('gameplay_pc_03080e')
    e.ins('movem.l','%d1-%d3/%a0,-(%a7)',4)
    e.label('gameplay_pc_030812')
    e.ins('tst.l','%d0',2)
    e.label('gameplay_pc_030814')
    e.ins('beq.w','gameplay_pc_03082a',4)
    e.label('gameplay_pc_030818')
    e.ins('bsr.w','gameplay_pc_030830',4)
    e.label('gameplay_pc_03081c')
    e.ins('sub.l','%d2,%d0',2)
    e.label('gameplay_pc_03081e')
    e.ins('bcs.w','gameplay_pc_030828',4)
    e.label('gameplay_pc_030822')
    e.ins('addq.w','#0x1,%d1',2)
    e.label('gameplay_pc_030824')
    e.ins('addq.w','#0x2,%d2',2)
    e.label('gameplay_pc_030826')
    e.ins('bra.b','gameplay_pc_03081c',2)
    e.label('gameplay_pc_030828')
    e.ins('move.w','%d1,%d0',2)
    e.label('gameplay_pc_03082a')
    e.ins('movem.l','(%a7)+,%d1-%d3/%a0',4)
    e.label('gameplay_pc_03082e')
    e.ins('rts','',2)

def _lower_seed_radial_distance_from_thresholds(e,rules):
    e.label('gameplay_pc_030830')
    e.ins('cmpi.l','#0x2358d,%d0',6)
    e.label('gameplay_pc_030836')
    e.ins('bcs.b','gameplay_pc_03084c',2)
    e.label('gameplay_pc_030838')
    e.ins('subi.l','#0x2358d,%d0',6)
    e.label('gameplay_pc_03083e')
    e.ins('move.l','#0x2fa,%d2',6)
    e.label('gameplay_pc_030844')
    e.ins('move.w','#0x17d,%d1',4)
    e.label('gameplay_pc_030848')
    e.ins('bra.w','gameplay_pc_030874',4)
    e.label('gameplay_pc_03084c')
    e.ins('clr.w','%d1',2)
    e.label('gameplay_pc_03084e')
    e.ins('moveq','#1,%d2',2)
    e.label('gameplay_pc_030850')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_030852')
    e.ins('lea.l','34(%pc),%a0',4)
    e.label('gameplay_pc_030856')
    e.ins('cmp.l','(%a0),%d0',2)
    e.label('gameplay_pc_030858')
    e.ins('bcs.w','gameplay_pc_030860',4)
    e.label('gameplay_pc_03085c')
    e.ins('addq.l','#0x6,%a0',2)
    e.label('gameplay_pc_03085e')
    e.ins('bra.b','gameplay_pc_030856',2)
    e.label('gameplay_pc_030860')
    e.ins('move.l','-0x6(%a0),%d3',4)
    e.label('gameplay_pc_030864')
    e.ins('move.w','-0x2(%a0),%d2',4)
    e.label('gameplay_pc_030868')
    e.ins('sub.l','%d3,%d0',2)
    e.label('gameplay_pc_03086a')
    e.ins('move.w','%d2,%d1',2)
    e.label('gameplay_pc_03086c')
    e.ins('lsr.w','#0x1,%d1',2)
    e.label('gameplay_pc_03086e')
    e.ins('andi.l','#0xffff,%d2',6)
    e.label('gameplay_pc_030874')
    e.ins('rts','',2)

def _lower_signed_divmod(e,rules):
    e.label('gameplay_pc_035760')
    e.ins('tst.l','%d2',2)
    e.label('gameplay_pc_035762')
    e.ins('bpl.b','gameplay_pc_03576c',2)
    e.label('gameplay_pc_035764')
    e.ins('neg.l','%d2',2)
    e.label('gameplay_pc_035766')
    e.ins('bsr.b','gameplay_pc_03576c',2)
    e.label('gameplay_pc_035768')
    e.ins('neg.l','%d1',2)
    e.label('gameplay_pc_03576a')
    e.ins('rts','',2)

def _lower_positive_denominator(e,rules):
    e.label('gameplay_pc_03576c')
    e.ins('tst.l','%d1',2)
    e.label('gameplay_pc_03576e')
    e.ins('bpl.b','gameplay_pc_03577a',2)
    e.label('gameplay_pc_035770')
    e.ins('neg.l','%d1',2)
    e.label('gameplay_pc_035772')
    e.ins('bsr.b','gameplay_pc_03577a',2)
    e.label('gameplay_pc_035774')
    e.ins('neg.l','%d1',2)
    e.label('gameplay_pc_035776')
    e.ins('neg.l','%d2',2)
    e.label('gameplay_pc_035778')
    e.ins('rts','',2)

def _lower_unsigned_divmod(e,rules):
    e.label('gameplay_pc_03577a')
    e.ins('cmpi.l','#0xffff,%d2',6)
    e.label('gameplay_pc_035780')
    e.ins('bls.b','gameplay_pc_0357da',2)
    e.label('gameplay_pc_035782')
    e.ins('cmp.l','%d1,%d2',2)
    e.label('gameplay_pc_035784')
    e.ins('beq.b','gameplay_pc_03578e',2)
    e.label('gameplay_pc_035786')
    e.ins('bls.b','gameplay_pc_035794',2)
    e.label('gameplay_pc_035788')
    e.ins('move.l','%d1,%d2',2)
    e.label('gameplay_pc_03578a')
    e.ins('moveq','#0,%d1',2)
    e.label('gameplay_pc_03578c')
    e.ins('rts','',2)
    e.label('gameplay_pc_03578e')
    e.ins('moveq','#1,%d1',2)
    e.label('gameplay_pc_035790')
    e.ins('moveq','#0,%d2',2)
    e.label('gameplay_pc_035792')
    e.ins('rts','',2)
    e.label('gameplay_pc_035794')
    e.ins('movem.l','%d3-%d5,-(%a7)',4)
    e.label('gameplay_pc_035798')
    e.ins('move.l','%d2,%d3',2)
    e.label('gameplay_pc_03579a')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_03579c')
    e.ins('swap','%d3',2)
    e.label('gameplay_pc_03579e')
    e.ins('addq.l','#0x1,%d3',2)
    e.label('gameplay_pc_0357a0')
    e.ins('move.l','%d1,%d4',2)
    e.label('gameplay_pc_0357a2')
    e.ins('move.l','%d2,%d5',2)
    e.label('gameplay_pc_0357a4')
    e.ins('move.l','%d3,%d2',2)
    e.label('gameplay_pc_0357a6')
    e.ins('bsr.b','gameplay_pc_0357da',2)
    e.label('gameplay_pc_0357a8')
    e.ins('move.l','%d5,%d2',2)
    e.label('gameplay_pc_0357aa')
    e.ins('divu.w','%d3,%d2',2)
    e.label('gameplay_pc_0357ac')
    e.ins('divu.w','%d2,%d1',2)
    e.label('gameplay_pc_0357ae')
    e.ins('andi.l','#0xffff,%d1',6)
    e.label('gameplay_pc_0357b4')
    e.ins('move.l','%d5,%d2',2)
    e.label('gameplay_pc_0357b6')
    e.ins('move.l','%d5,%d3',2)
    e.label('gameplay_pc_0357b8')
    e.ins('swap','%d3',2)
    e.label('gameplay_pc_0357ba')
    e.ins('mulu.w','%d1,%d2',2)
    e.label('gameplay_pc_0357bc')
    e.ins('mulu.w','%d1,%d3',2)
    e.label('gameplay_pc_0357be')
    e.ins('swap','%d3',2)
    e.label('gameplay_pc_0357c0')
    e.ins('add.l','%d3,%d2',2)
    e.label('gameplay_pc_0357c2')
    e.ins('sub.l','%d4,%d2',2)
    e.label('gameplay_pc_0357c4')
    e.ins('bhi.b','gameplay_pc_0357d0',2)
    e.label('gameplay_pc_0357c6')
    e.ins('neg.l','%d2',2)
    e.label('gameplay_pc_0357c8')
    e.ins('cmp.l','%d2,%d5',2)
    e.label('gameplay_pc_0357ca')
    e.ins('bhi.b','gameplay_pc_0357d4',2)
    e.label('gameplay_pc_0357cc')
    e.ins('addq.l','#0x1,%d1',2)
    e.label('gameplay_pc_0357ce')
    e.ins('bra.b','gameplay_pc_0357b4',2)
    e.label('gameplay_pc_0357d0')
    e.ins('subq.l','#0x1,%d1',2)
    e.label('gameplay_pc_0357d2')
    e.ins('bra.b','gameplay_pc_0357b4',2)
    e.label('gameplay_pc_0357d4')
    e.ins('movem.l','(%a7)+,%d3-%d5',4)
    e.label('gameplay_pc_0357d8')
    e.ins('rts','',2)

def _lower_word_pair_divmod(e,rules):
    e.label('gameplay_pc_0357da')
    e.ins('movem.w','%d1/%d3,-(%a7)',4)
    e.label('gameplay_pc_0357de')
    e.ins('clr.w','%d1',2)
    e.label('gameplay_pc_0357e0')
    e.ins('swap','%d1',2)
    e.label('gameplay_pc_0357e2')
    e.ins('divu.w','%d2,%d1',2)
    e.label('gameplay_pc_0357e4')
    e.ins('move.w','%d1,%d3',2)
    e.label('gameplay_pc_0357e6')
    e.ins('move.w','(%a7)+,%d1',2)
    e.label('gameplay_pc_0357e8')
    e.ins('divu.w','%d2,%d1',2)
    e.label('gameplay_pc_0357ea')
    e.ins('swap','%d1',2)
    e.label('gameplay_pc_0357ec')
    e.ins('moveq','#0,%d2',2)
    e.label('gameplay_pc_0357ee')
    e.ins('move.w','%d1,%d2',2)
    e.label('gameplay_pc_0357f0')
    e.ins('move.w','%d3,%d1',2)
    e.label('gameplay_pc_0357f2')
    e.ins('swap','%d1',2)
    e.label('gameplay_pc_0357f4')
    e.ins('move.w','(%a7)+,%d3',2)
    e.label('gameplay_pc_0357f6')
    e.ins('rts','',2)

LOWERERS = {
    'build_roster':_lower_build_roster,
    'step_random':_lower_step_random,
    'choose_city_head':_lower_choose_city_head,
    'roster_contains_force_head_carry':_lower_roster_contains_force_head_carry,
    'terrain_cell_query':_lower_terrain_cell_query,
    'replenish_b200_troops':_lower_replenish_b200_troops,
    'grow_original_long_field':_lower_grow_original_long_field,
    'credit_primary':_lower_credit_primary,
    'credit_secondary':_lower_credit_secondary,
    'commit_income':_lower_commit_income,
    'scaled_income':_lower_scaled_income,
    'deplete_income':_lower_deplete_income,
    'debit_primary':_lower_debit_primary,
    'debit_secondary':_lower_debit_secondary,
    'settle_expense':_lower_settle_expense,
    'settle_shortage':_lower_settle_shortage,
    'reset_queue':_lower_reset_queue,
    'append_queue':_lower_append_queue,
    'submit_three_fields':_lower_submit_three_fields,
    'submit_four_fields':_lower_submit_four_fields,
    'submit_classified_fields':_lower_submit_classified_fields,
    'scale_e1e0':_lower_scale_e1e0,
    'scale_e140':_lower_scale_e140,
    'scale_e320':_lower_scale_e320,
    'scale_e000':_lower_scale_e000,
    'scale_e0a0':_lower_scale_e0a0,
    'scale_e5a0':_lower_scale_e5a0,
    'sample_once':_lower_sample_once,
    'sample_small':_lower_sample_small,
    'sample_wide':_lower_sample_wide,
    'wrapped_product':_lower_wrapped_product,
    'divide_percent':_lower_divide_percent,
    'sum_group_troops':_lower_sum_group_troops,
    'find_group_at_coordinate':_lower_find_group_at_coordinate,
    'settle_duel_training_and_troops':_lower_settle_duel_training_and_troops,
    'grant_duel_fallback_progress':_lower_grant_duel_fallback_progress,
    'grant_duel_troop_difference_progress':_lower_grant_duel_troop_difference_progress,
    'remove_zero_readiness_duelist':_lower_remove_zero_readiness_duelist,
    'settle_duel_result_roster':_lower_settle_duel_result_roster,
    'transfer_battle_roster':_lower_transfer_battle_roster,
    'settle_duel_packets':_lower_settle_duel_packets,
    'apply_duel_disposition':_lower_apply_duel_disposition,
    'detach_zero_readiness_duelists':_lower_detach_zero_readiness_duelists,
    'detach_defeated_duelist':_lower_detach_defeated_duelist,
    'load_battlefield_map_context':_lower_load_battlefield_map_context,
    'read_battlefield_terrain_type':_lower_read_battlefield_terrain_type,
    'compute_outcome_force_ratio':_lower_compute_outcome_force_ratio,
    'build_city_assigned_outcome_candidates':_lower_build_city_assigned_outcome_candidates,
    'build_battlefield_outcome_candidates':_lower_build_battlefield_outcome_candidates,
    'apply_battlefield_ratio_losses':_lower_apply_battlefield_ratio_losses,
    'apply_city_assigned_heavy_losses':_lower_apply_city_assigned_heavy_losses,
    'consume_city_battle_resources':_lower_consume_city_battle_resources,
    'apply_battlefield_heavy_losses_and_detach':_lower_apply_battlefield_heavy_losses_and_detach,
    'rebuild_primary_after_battle':_lower_rebuild_primary_after_battle,
    'sort_returning_officer_status':_lower_sort_returning_officer_status,
    'partition_city_survivors':_lower_partition_city_survivors,
    'owner_has_other_city_carry':_lower_owner_has_other_city_carry,
    'restore_returning_officer_assignments':_lower_restore_returning_officer_assignments,
    'allocate_packed_group_resources':_lower_allocate_packed_group_resources,
    'rebuild_secondary_after_battle':_lower_rebuild_secondary_after_battle,
    'settle_battle_packed_armies':_lower_settle_battle_packed_armies,
    'remove_defeated_packed_member':_lower_remove_defeated_packed_member,
    'replace_or_remove_group_references':_lower_replace_or_remove_group_references,
    'transfer_outcome_officer':_lower_transfer_outcome_officer,
    'detach_member_keep_group_cursor':_lower_detach_member_keep_group_cursor,
    'replace_group_head_reference':_lower_replace_group_head_reference,
    'remove_group_reference':_lower_remove_group_reference,
    'attach_member_shift_packet':_lower_attach_member_shift_packet,
    'settle_group_at_city':_lower_settle_group_at_city,
    'locate_group_city':_lower_locate_group_city,
    'credit_packed_group_resources':_lower_credit_packed_group_resources,
    'erase_group_packet':_lower_erase_group_packet,
    'adjust_battle_losing_loyalty':_lower_adjust_battle_losing_loyalty,
    'initialize_prebattle_head_bytes':_lower_initialize_prebattle_head_bytes,
    'apply_returning_officer_loyalty':_lower_apply_returning_officer_loyalty,
    'append_group_from_survivor_roster':_lower_append_group_from_survivor_roster,
    'choose_empty_neighbor_position':_lower_choose_empty_neighbor_position,
    'rounded_radial_distance':_lower_rounded_radial_distance,
    'seed_radial_distance_from_thresholds':_lower_seed_radial_distance_from_thresholds,
    'signed_divmod':_lower_signed_divmod,
    'positive_denominator':_lower_positive_denominator,
    'unsigned_divmod':_lower_unsigned_divmod,
    'word_pair_divmod':_lower_word_pair_divmod,
}

def compile_reuse(source):
    records=semantic_functions(source,DECLARATIONS,APPROVED)
    records['apply_returning_officer_loyalty']['effects'] += '\nsole returning-loyalty fields: ' + records['apply_returning_officer_loyalty_fields']['effects']
    records['read_battlefield_terrain_type']['effects'] += '\nsole terrain observations: ' + records['read_battlefield_terrain_type_observations']['effects']
    for owner in ('apply_battlefield_ratio_losses', 'apply_city_assigned_heavy_losses', 'apply_battlefield_heavy_losses_and_detach', 'rebuild_primary_after_battle', 'sort_returning_officer_status', 'partition_city_survivors', 'owner_has_other_city_carry', 'restore_returning_officer_assignments', 'allocate_packed_group_resources', 'rebuild_secondary_after_battle'):
        records[owner]['effects'] += '\nsole current city return/loss field cores: ' + '\n'.join(('apply_battlefield_ratio_losses_fields', 'apply_city_assigned_heavy_losses_fields', 'apply_battlefield_heavy_losses_and_detach_fields', 'rebuild_primary_after_battle_fields', 'sort_returning_officer_status_fields', 'partition_city_survivors_fields', 'owner_has_other_city_carry_fields', 'restore_returning_officer_assignments_fields', 'allocate_packed_group_resources_fields', 'rebuild_secondary_after_battle_fields'))
    for owner in ('build_roster', 'choose_city_head', 'roster_contains_force_head_carry', 'append_group_from_survivor_roster', 'choose_empty_neighbor_position'):
        records[owner]['effects'] += '\nsole consolidation/arrival/packet fields: ' + '\n'.join(('build_roster_fields', 'choose_city_head_fields', 'roster_contains_force_head_carry_fields', 'append_group_from_survivor_roster_fields', 'choose_empty_neighbor_position_fields'))
    sole_group_troop_fields = {name:records[name]['effects'] for name in ('sum_group_troops_fields',)}
    for owner in ('sum_group_troops',):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_group_troop_fields=sole_group_troop_fields)
    for owner in ('settle_battle_packed_armies', 'remove_defeated_packed_member', 'replace_or_remove_group_references', 'transfer_outcome_officer', 'detach_member_keep_group_cursor', 'replace_group_head_reference', 'remove_group_reference', 'attach_member_shift_packet'):
        records[owner]['effects'] += '\nsole packed-member field core: ' + '\n'.join(('settle_battle_packed_armies_fields', 'remove_defeated_packed_member_fields', 'replace_or_remove_group_references_fields', 'transfer_outcome_officer_fields', 'detach_member_keep_group_cursor_fields', 'replace_group_head_reference_fields', 'remove_group_reference_fields', 'attach_member_shift_packet_fields'))
    sole_duel_result_fields = {name:records[name]['effects'] for name in ('_duel_result_write_fields', '_duel_result_call_fields', '_duel_training_side_fields', 'settle_duel_training_and_troops_fields', '_duel_progress_store_fields', 'grant_duel_fallback_progress_fields', 'grant_duel_troop_difference_progress_fields', '_duel_result_compact_roster_fields', 'remove_zero_readiness_duelist_fields', 'settle_duel_result_roster_fields', 'transfer_battle_roster_fields')}
    for owner in ('settle_duel_training_and_troops', 'grant_duel_fallback_progress', 'grant_duel_troop_difference_progress', 'remove_zero_readiness_duelist', 'settle_duel_result_roster', 'transfer_battle_roster'):
        records[owner]['effects'] = dict(legacy_projection=records[owner]['effects'], sole_duel_result_fields=sole_duel_result_fields)
    sole_duel_packet_fields = {name:records[name]['effects'] for name in ('_duel_result_seek_unbounded_fields', '_duel_result_append_retired_fields', 'settle_duel_packets_fields', 'apply_duel_disposition_fields', 'detach_zero_readiness_duelists_fields', 'detach_defeated_duelist_fields', '_duel_result_compact_roster_fields', '_duel_result_call_fields')}
    for owner in ('settle_duel_packets', 'apply_duel_disposition', 'detach_zero_readiness_duelists', 'detach_defeated_duelist'):
        records[owner]['effects'] = dict(legacy_projection=records[owner]['effects'],sole_duel_packet_fields=sole_duel_packet_fields)
    sole_calendar_fields={name:records[name]['effects'] for name in ('_calendar_arithmetic_fields', '_calendar_bit_fields', '_calendar_call_fields', '_calendar_child_fields', '_calendar_compare_fields', '_calendar_db_fields', '_calendar_divu_fields', '_calendar_frame_fields', '_calendar_legacy_entry_fields', '_calendar_memory_arithmetic_fields', '_calendar_move_fields', '_calendar_pop_word_fields', '_calendar_product_terms', '_calendar_push_word_fields', '_calendar_restore_fields', '_calendar_sample_fields', '_calendar_save_fields', '_calendar_scale_fields', '_calendar_shift_fields', '_calendar_submit_fields', '_calendar_swap_fields', '_calendar_test_fields', '_calendar_value_fields', '_calendar_write_fields', 'append_queue_fields', 'commit_income_fields', 'credit_primary_fields', 'credit_secondary_fields', 'debit_primary_fields', 'debit_secondary_fields', 'deplete_income_fields', 'divide_percent_fields', 'grow_original_long_field_fields', 'replenish_b200_troops_fields', 'reset_queue_fields', 'sample_once_fields', 'sample_small_fields', 'sample_wide_fields', 'scale_e000_fields', 'scale_e0a0_fields', 'scale_e140_fields', 'scale_e1e0_fields', 'scale_e320_fields', 'scale_e5a0_fields', 'scaled_income_fields', 'settle_expense_fields', 'settle_shortage_fields', 'submit_calendar_classified_fields', 'submit_calendar_four_fields', 'submit_calendar_three_fields', 'wrapped_product_fields')}
    for owner in ('replenish_b200_troops', 'grow_original_long_field', 'credit_primary', 'credit_secondary', 'commit_income', 'scaled_income', 'deplete_income', 'debit_primary', 'debit_secondary', 'settle_expense', 'settle_shortage', 'reset_queue', 'append_queue', 'submit_three_fields', 'submit_four_fields', 'submit_classified_fields', 'scale_e1e0', 'scale_e140', 'scale_e320', 'scale_e000', 'scale_e0a0', 'scale_e5a0', 'sample_once', 'sample_small', 'sample_wide', 'wrapped_product', 'divide_percent'):
        records[owner]['effects']=dict(legacy_projection=records[owner]['effects'],sole_current_calendar_fields=sole_calendar_fields)
    return lower_declared({b.name:records[b.name] for b in REUSE_BINDINGS},REUSE_BINDINGS,LOWERERS)

DECLARATIONS.update({'apply_returning_officer_loyalty': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\napply_returning_officer_loyalty_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())'}})

DECLARATIONS.update({'apply_returning_officer_loyalty_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary\nfrom ..high_level_main_flows.business_movement_support import _movement_save_longs, _movement_restore_longs\nif type(memory) is not BattlePresentationMemory:\n    raise ValueError('closed same-state returning-loyalty memory required')\nentered = memory.validate_frame(frame)\nphysical = frame.stack_cursor is not None\nif type(memory.state) is not GameplayState and (not physical or frame.roster is None or frame.candidates is None):\n    raise MovementContinuationBoundary(133326, frame, 'original loyalty MOVEM requires the actual Scene A7/A0/A1 fields')\nsaved = ('target_x', 'target_y', 'unit', 'count', 'distance', 'roster', 'candidates')\nif physical:\n    frame = _movement_save_longs(memory.state, frame, saved)\nframe = _presentation_call_fields(memory, frame, 133336, _presentation_random_fields)\nsample = u32(frame.target_x & 65535)\nframe = _first_long(frame, 'target_x', sample)\nframe = _first_long(frame, 'target_y', sample)\nscaled = u32(sample * 5)\nframe = _first_long(frame, 'target_x', swap_words(scaled))\nfactor = u16(high16(scaled) + 6)\nframe = _first_add_word(frame, 'target_x', high16(scaled), 6)\nloyalty = memory.table(4294951680).cursor()\nframe = first_replace(frame, roster=loyalty)\nframe = _first_word(frame, 'target_y', 104)\nselected = memory.table(4294964134).word()\nframe = _first_word(frame, 'unit', selected)\nofficer = u16(selected & 255)\nframe = _first_word(frame, 'unit', officer)\nprior = loyalty.byte(officer)\ngap = u8(104 - prior)\noverflow = bool((104 ^ prior) & (104 ^ gap) & 128)\nconditions = (17 if 104 < prior else 0) | (2 if overflow else 0) | (8 if gap & 128 else 0) | (4 if gap == 0 else 0)\nframe = first_replace(frame, target_y=replace_byte(frame.target_y, gap), status=conditions)\nreduced = u16(gap >> 1)\nframe = _first_right_word(frame, 'target_y', gap, 1)\naffinity = memory.table(4294951424).cursor()\nframe = first_replace(frame, candidates=affinity)\nsource_word = memory.table(4294964210).word()\nframe = _first_word(frame, 'distance', source_word)\nsource = u16(source_word & 255)\nframe = _first_word(frame, 'distance', source)\nframe = _first_word(frame, 'count', 0)\ninfluence = u16(affinity.byte(source))\nframe = _first_byte(frame, 'count', influence)\nvalue = u32(low16(reduced) * low16(influence))\nframe = _first_long(frame, 'target_y', value)\nvalue = u32(low16(value) * low16(factor))\nframe = _first_long(frame, 'target_y', value)\nvalue = divu_retained(value, 500)\nframe = first_replace(frame, target_y=value)\nframe = _first_word(frame, 'target_y', low16(value))\nframe = _first_compare_word(frame, low16(value), 100)\nif low16(value) > 100:\n    value = u32(value & 4294901760 | 100)\n    frame = _first_word(frame, 'target_y', 100)\nloyalty.set_byte(officer, low8(value))\nframe = _first_byte(frame, 'target_y', low8(value))\nmemory.finish(frame)\nif physical:\n    frame = _movement_restore_longs(memory.state, frame, saved)\nelse:\n    frame = first_replace(frame, target_x=entered.target_x, target_y=entered.target_y, unit=entered.unit, count=entered.count, distance=entered.distance, roster=entered.roster, candidates=entered.candidates)\nreturn memory.finish(frame)"}})

APPROVED.setdefault('contexts_battle', set()).update({'_first_compare_word', '_first_word', '_first_right_word', 'BattlePresentationMemory', '_first_long', 'FirstDeploymentFrame', '_first_add_word', 'first_replace'})
APPROVED.setdefault('business_battle', set()).update({'_presentation_call_fields', '_presentation_random_fields'})
APPROVED.setdefault('business_formation', set()).add('_first_byte')
APPROVED.setdefault('contexts_gameplay', set()).add('MovementContinuationBoundary')
APPROVED.setdefault('business_movement_support', set()).update({'_movement_save_longs', '_movement_restore_longs'})


# Entire sole read_battlefield_terrain_type current body.
DECLARATIONS.update({'read_battlefield_terrain_type': {'signature': 'state: GameplayState, map_context: Table, x: Word, y: Word, retained: Long=0', 'returns': 'Long', 'flow': 'uint(retained, 32)\nreturn read_battlefield_terrain_type_observations(state, map_context, x, y, retained)[0]'}})


# Entire sole read_battlefield_terrain_type_observations current body.
DECLARATIONS.update({'read_battlefield_terrain_type_observations': {'signature': 'state: GameplayState, map_context: Table, x: Word, y: Word, retained: Long | None', 'returns': 'tuple', 'flow': 'checked_state(state)\nchecked_table(map_context, state)\nuint(x, 16)\nuint(y, 16)\nif retained is not None:\n    uint(retained, 32)\nbefore_shift = u16((x >> 3) * 40 + (y >> 3))\noffset = u16(before_shift * 2)\ntile = map_context.word(offset) & 1023\ncategory = state.terrain_category_lookup.byte(tile)\nterrain_word = tile & 65280 | category\ncarrier = None if retained is None else replace_word(retained, terrain_word)\nreturn (carrier, terrain_word, category, bool(before_shift & 32768))'}})

DECLARATIONS.update({'build_city_assigned_outcome_candidates': {'signature': 'state: GameplayState', 'returns': 'Word', 'flow': 'checked_state(state)\nfrom .business_battle import build_city_assigned_outcome_candidates_fields\nfrom .contexts_battle import BattlePresentationMemory, FirstDeploymentFrame\nreturn build_city_assigned_outcome_candidates_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())[1]'}})

DECLARATIONS.update({'build_battlefield_outcome_candidates': {'signature': 'state: GameplayState', 'returns': 'Word', 'flow': 'checked_state(state)\nfrom .business_battle import build_battlefield_outcome_candidates_fields\nfrom .contexts_battle import BattlePresentationMemory, FirstDeploymentFrame\nreturn build_battlefield_outcome_candidates_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())[1]'}})

APPROVED.setdefault('business_battle',set()).update({'build_city_assigned_outcome_candidates_fields', 'build_battlefield_outcome_candidates_fields'})
APPROVED.setdefault('contexts_battle',set()).update({'BattlePresentationMemory','FirstDeploymentFrame'})

DECLARATIONS.update({'settle_group_at_city': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'project_gameplay_arrival_fields(state, 119740)'}})

DECLARATIONS.update({'locate_group_city': {'signature': 'state: GameplayState, packet: Table', 'returns': 'Word', 'flow': 'frame = project_gameplay_arrival_fields(state, 119820, packet)\nreturn low16(frame.count)'}})

DECLARATIONS.update({'credit_packed_group_resources': {'signature': 'state: GameplayState, packet: Table, city: Word', 'returns': 'None', 'flow': 'project_gameplay_arrival_fields(state, 119884, packet, city)'}})

DECLARATIONS.update({'erase_group_packet': {'signature': 'state: GameplayState, packet: Table', 'returns': 'Table', 'flow': 'frame = project_gameplay_arrival_fields(state, 119992, packet)\nreturn state.table(frame.roster.base)'}})

DECLARATIONS.update({'adjust_battle_losing_loyalty': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'project_gameplay_arrival_fields(state, 120026)'}})

DECLARATIONS.update({'initialize_prebattle_head_bytes': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'project_gameplay_arrival_fields(state, 120186)'}})

DECLARATIONS.update({'terrain_cell_query': {'signature': 'state: GameplayState, row: Word, column: Word', 'returns': 'tuple[Byte, Byte]', 'flow': 'frame = project_gameplay_arrival_fields(state, 82594, row=row, column=column)\nreturn (low8(frame.unit), low8(frame.count))'}})

APPROVED.setdefault('contexts_reuse', set()).add('project_gameplay_arrival_fields')

DECLARATIONS.update({'compute_outcome_force_ratio': {'signature': 'state: GameplayState', 'returns': 'Word', 'flow': 'checked_state(state)\nframe = compute_outcome_force_ratio_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())\nreturn low16(frame.target_y)'}})

DECLARATIONS.update({'consume_city_battle_resources': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\nconsume_city_battle_resources_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())'}})

APPROVED.setdefault('business_battle', set()).update({'compute_outcome_force_ratio_fields','consume_city_battle_resources_fields'})


# Entire current sole allocate_packed_group_resources body.
DECLARATIONS.update({'allocate_packed_group_resources': {'signature': 'state: GameplayState, packet: Table', 'returns': 'None', 'flow': 'checked_state(state)\npacket = state.checked_table(packet)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=packet.cursor())\nfrom .business_battle import allocate_packed_group_resources_fields\nframe = allocate_packed_group_resources_fields(BattlePresentationMemory(state), frame)'}})


# Entire current sole apply_battlefield_heavy_losses_and_detach body.
DECLARATIONS.update({'apply_battlefield_heavy_losses_and_detach': {'signature': 'state: GameplayState', 'returns': 'Word', 'flow': 'checked_state(state)\nframe = FirstDeploymentFrame.unobserved()\nfrom .business_battle import apply_battlefield_heavy_losses_and_detach_fields\nframe = apply_battlefield_heavy_losses_and_detach_fields(BattlePresentationMemory(state), frame)\nreturn low16(frame.choice)'}})


# Entire current sole apply_battlefield_ratio_losses body.
DECLARATIONS.update({'apply_battlefield_ratio_losses': {'signature': 'state: GameplayState', 'returns': 'Word', 'flow': 'checked_state(state)\nframe = FirstDeploymentFrame.unobserved()\nfrom .business_battle import apply_battlefield_ratio_losses_fields\nframe = apply_battlefield_ratio_losses_fields(BattlePresentationMemory(state), frame)\nreturn low16(frame.choice)'}})


# Entire current sole apply_city_assigned_heavy_losses body.
DECLARATIONS.update({'apply_city_assigned_heavy_losses': {'signature': 'state: GameplayState', 'returns': 'Word', 'flow': 'checked_state(state)\nframe = FirstDeploymentFrame.unobserved()\nfrom .business_battle import apply_city_assigned_heavy_losses_fields\nframe = apply_city_assigned_heavy_losses_fields(BattlePresentationMemory(state), frame)\nreturn low16(frame.choice)'}})


# Entire current sole owner_has_other_city_carry body.
DECLARATIONS.update({'owner_has_other_city_carry': {'signature': 'state: GameplayState', 'returns': 'CarryOutcome', 'flow': 'checked_state(state)\nframe = FirstDeploymentFrame.unobserved()\nfrom .business_battle import owner_has_other_city_carry_fields\nframe = owner_has_other_city_carry_fields(BattlePresentationMemory(state), frame)\nreturn state.carry_result(frame.status & 1)'}})


# Entire current sole partition_city_survivors body.
DECLARATIONS.update({'partition_city_survivors': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\nframe = FirstDeploymentFrame.unobserved()\nfrom .business_battle import partition_city_survivors_fields\nframe = partition_city_survivors_fields(BattlePresentationMemory(state), frame)'}})


# Entire current sole rebuild_primary_after_battle body.
DECLARATIONS.update({'rebuild_primary_after_battle': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\nframe = FirstDeploymentFrame.unobserved()\nfrom .business_battle import rebuild_primary_after_battle_fields\nframe = rebuild_primary_after_battle_fields(BattlePresentationMemory(state), frame)'}})


# Entire current sole rebuild_secondary_after_battle body.
DECLARATIONS.update({'rebuild_secondary_after_battle': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\nframe = FirstDeploymentFrame.unobserved()\nfrom .business_battle import rebuild_secondary_after_battle_fields\nframe = rebuild_secondary_after_battle_fields(BattlePresentationMemory(state), frame)'}})


# Entire current sole restore_returning_officer_assignments body.
DECLARATIONS.update({'restore_returning_officer_assignments': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\nframe = FirstDeploymentFrame.unobserved()\nfrom .business_battle import restore_returning_officer_assignments_fields\nframe = restore_returning_officer_assignments_fields(BattlePresentationMemory(state), frame)'}})


# Entire current sole sort_returning_officer_status body.
DECLARATIONS.update({'sort_returning_officer_status': {'signature': 'state: GameplayState, surplus: Word', 'returns': 'Word', 'flow': 'checked_state(state)\nuint(surplus, 16)\nframe = FirstDeploymentFrame.unobserved()\nfrom .business_battle import sort_returning_officer_status_fields\nframe = sort_returning_officer_status_fields(BattlePresentationMemory(state), frame)\nreturn low16(frame.target_y)'}})

APPROVED.setdefault('business_battle', set()).update({'apply_battlefield_ratio_losses_fields', 'apply_battlefield_heavy_losses_and_detach_fields', 'allocate_packed_group_resources_fields', 'restore_returning_officer_assignments_fields', 'rebuild_primary_after_battle_fields', 'apply_city_assigned_heavy_losses_fields', 'owner_has_other_city_carry_fields', 'partition_city_survivors_fields', 'rebuild_secondary_after_battle_fields', 'sort_returning_officer_status_fields'})

APPROVED.setdefault('contexts_battle', set()).add('first_replace')


# Entire current sole append_group_from_survivor_roster body.
DECLARATIONS.update({'append_group_from_survivor_roster': {'signature': 'state: GameplayState', 'returns': 'Table', 'flow': 'checked_state(state)\nfrom .business_battle import append_group_from_survivor_roster_fields\nframe = append_group_from_survivor_roster_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())\nreturn state.table(frame.roster.base)'}})


# Entire current sole build_roster body.
DECLARATIONS.update({'build_roster': {'signature': 'state: GameplayState, city: Word', 'returns': 'Word', 'flow': 'checked_state(state)\nuint(city, 16)\nfrom .business_battle import build_roster_fields\nframe = build_roster_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())\nreturn low16(frame.count)'}})


# Entire current sole choose_city_head body.
DECLARATIONS.update({'choose_city_head': {'signature': 'state: GameplayState, city: Word', 'returns': 'Word', 'flow': 'checked_state(state)\nuint(city, 16)\nfrom .business_battle import choose_city_head_fields\nframe = choose_city_head_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())\nreturn low16(frame.target_x)'}})


# Entire current sole choose_empty_neighbor_position body.
DECLARATIONS.update({'choose_empty_neighbor_position': {'signature': 'state: GameplayState', 'returns': 'tuple[Word, Word]', 'flow': 'checked_state(state)\nfrom .business_battle import choose_empty_neighbor_position_fields\nframe = choose_empty_neighbor_position_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())\nreturn (low16(frame.target_x), low16(frame.target_y))'}})


# Entire current sole roster_contains_force_head_carry body.
DECLARATIONS.update({'roster_contains_force_head_carry': {'signature': 'state: GameplayState, city: Word, head: Word', 'returns': 'ForceHeadMatch', 'flow': 'checked_state(state)\nuint(city, 16)\nuint(head, 16)\nfrom .business_battle import roster_contains_force_head_carry_fields\nframe = roster_contains_force_head_carry_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())\nreturn ForceHeadMatch(low16(frame.distance), state.carry_result(frame.status & 1))'}})

APPROVED.setdefault('business_battle',set()).update({'choose_empty_neighbor_position_fields', 'choose_city_head_fields', 'append_group_from_survivor_roster_fields', 'roster_contains_force_head_carry_fields', 'build_roster_fields'})

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('contexts_services',set()).update({'SceneRefreshBoundary', 'SceneRefreshMemory'})
APPROVED.setdefault('business_formation',set()).update({'_first_shift_word'})
APPROVED.setdefault('business_movement_support',set()).update({'_movement_binary_flags'})
DECLARATIONS.update({'sum_group_troops': {'signature': 'state: GameplayState, roster: Cursor, troops: Table',
                      'returns': 'tuple[Long, Word]',
                      'flow': 'from .contexts_services import SceneRefreshMemory\n'
                              'checked_state(state)\n'
                              'checked_table(roster, state)\n'
                              'checked_table(troops, state)\n'
                              'entered = first_replace(FirstDeploymentFrame.unobserved(), '
                              'roster=troops.cursor(), candidates=roster.advance(0))\n'
                              'actual, count = sum_group_troops_fields(SceneRefreshMemory(state), entered)\n'
                              'roster.base = actual.candidates.base\n'
                              'return (actual.target_x, count)'},
 'sum_group_troops_fields': {'signature': 'memory, frame: FirstDeploymentFrame',
                             'returns': 'tuple[FirstDeploymentFrame, Word]',
                             'flow': 'from .contexts_services import SceneRefreshMemory, '
                                     'SceneRefreshBoundary\n'
                                     'from ..high_level_battle_ai.business_formation import '
                                     '_first_shift_word\n'
                                     'from ..high_level_main_flows.business_movement_support import '
                                     '_movement_binary_flags\n'
                                     'if type(memory) is not SceneRefreshMemory:\n'
                                     "    raise ValueError('same-state troop-sum memory required')\n"
                                     'memory.frame(frame)\n'
                                     'if frame.roster is None or frame.candidates is None:\n'
                                     '    raise SceneRefreshBoundary(96702, frame, None)\n'
                                     "frame = _first_long(frame, 'target_x', 0)\n"
                                     "frame = _first_word(frame, 'target_y', 0)\n"
                                     'count = 0\n'
                                     'while True:\n'
                                     '    member = frame.candidates.word()\n'
                                     '    frame = first_replace(frame, '
                                     'candidates=frame.candidates.advance(2))\n'
                                     "    frame = _first_word(frame, 'unit', member)\n"
                                     '    if negative_word(member):\n'
                                     '        return (memory.sync_status(frame), count)\n'
                                     '    officer = member & 255\n'
                                     "    frame = _first_word(frame, 'unit', officer)\n"
                                     '    frame, count = _movement_binary_flags(memory.state, frame, count, '
                                     '1, 16)\n'
                                     '    frame = first_replace(frame, target_y=None if frame.target_y is '
                                     'None else replace_word(frame.target_y, count))\n'
                                     "    frame = _first_shift_word(frame, 'unit', officer, 2)\n"
                                     '    quantity = frame.roster.long(officer << 2)\n'
                                     '    before = frame.target_x\n'
                                     '    frame, total = _movement_binary_flags(memory.state, frame, before, '
                                     'quantity, 32)\n'
                                     '    frame = first_replace(frame, target_x=total)'}})

DECLARATIONS.update({'attach_member_shift_packet': {'signature': 'state: GameplayState, officer: Word, context: GroupContext', 'returns': 'GroupContext', 'flow': 'checked_state(state)\nuint(officer, 16)\ncontext = checked_context(context, state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=context.source.cursor(), candidates=context.target.cursor())\nfrom .business_battle import attach_member_shift_packet_fields\nframe = attach_member_shift_packet_fields(BattlePresentationMemory(state), frame)\nreturn GroupContext(state.table(frame.roster.base), state.table(frame.candidates.base))'}})

DECLARATIONS.update({'detach_member_keep_group_cursor': {'signature': 'state: GameplayState, officer: Word, context: GroupContext', 'returns': 'GroupContext', 'flow': 'checked_state(state)\nuint(officer, 16)\ncontext = checked_context(context, state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=context.source.cursor(), candidates=context.target.cursor())\nfrom .business_battle import detach_member_keep_group_cursor_fields\nframe = detach_member_keep_group_cursor_fields(BattlePresentationMemory(state), frame)\nreturn GroupContext(state.table(frame.roster.base), state.table(frame.candidates.base))'}})

DECLARATIONS.update({'remove_defeated_packed_member': {'signature': 'state: GameplayState, officer: Word, context: GroupContext', 'returns': 'GroupContext', 'flow': 'checked_state(state)\nuint(officer, 16)\ncontext = checked_context(context, state)\nframe = first_replace(FirstDeploymentFrame.unobserved(), candidates=context.source.cursor(), controller=context.target)\nfrom .business_battle import remove_defeated_packed_member_fields\nframe = remove_defeated_packed_member_fields(BattlePresentationMemory(state), frame)\nreturn GroupContext(state.table(frame.candidates.base), state.table(frame.controller.base))'}})

DECLARATIONS.update({'remove_group_reference': {'signature': 'state: GameplayState, officer: Word', 'returns': 'None', 'flow': 'checked_state(state)\nuint(officer, 16)\nframe = FirstDeploymentFrame.unobserved()\nfrom .business_battle import remove_group_reference_fields\nframe = remove_group_reference_fields(BattlePresentationMemory(state), frame)'}})

DECLARATIONS.update({'replace_group_head_reference': {'signature': 'state: GameplayState, officer: Word, group: Table', 'returns': 'None', 'flow': 'checked_state(state)\nuint(officer, 16)\ngroup = state.checked_table(group)\nframe = first_replace(FirstDeploymentFrame.unobserved(), roster=group.cursor())\nfrom .business_battle import replace_group_head_reference_fields\nframe = replace_group_head_reference_fields(BattlePresentationMemory(state), frame)'}})

DECLARATIONS.update({'replace_or_remove_group_references': {'signature': 'state: GameplayState, old_head: Word, new_head: Word', 'returns': 'None', 'flow': 'checked_state(state)\nuint(old_head, 16)\nuint(new_head, 16)\nframe = FirstDeploymentFrame.unobserved()\nfrom .business_battle import replace_or_remove_group_references_fields\nframe = replace_or_remove_group_references_fields(BattlePresentationMemory(state), frame)'}})

DECLARATIONS.update({'settle_battle_packed_armies': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\nframe = FirstDeploymentFrame.unobserved()\nfrom .business_battle import settle_battle_packed_armies_fields\nframe = settle_battle_packed_armies_fields(BattlePresentationMemory(state), frame)'}})

DECLARATIONS.update({'transfer_outcome_officer': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\nframe = FirstDeploymentFrame.unobserved()\nfrom .business_battle import transfer_outcome_officer_fields\nframe = transfer_outcome_officer_fields(BattlePresentationMemory(state), frame)'}})

APPROVED.setdefault('business_battle',set()).update(('settle_battle_packed_armies_fields', 'remove_defeated_packed_member_fields', 'replace_or_remove_group_references_fields', 'transfer_outcome_officer_fields', 'detach_member_keep_group_cursor_fields', 'replace_group_head_reference_fields', 'remove_group_reference_fields', 'attach_member_shift_packet_fields'))

DECLARATIONS.update({'settle_duel_training_and_troops': {'signature': 'state: GameplayState, context: DuelSettlementContext', 'returns': 'DuelSettlementResult', 'flow': 'checked_state(state)\ncontext = _reuse_checked_context(context, DuelSettlementContext)\nframe = first_replace(FirstDeploymentFrame.unobserved(), unit=context.training_carrier)\nactual = settle_duel_training_and_troops_fields(BattlePresentationMemory(state), frame)\nreturn DuelSettlementResult(actual.count)'}})

DECLARATIONS.update({'grant_duel_fallback_progress': {'signature': 'state: GameplayState, receiver_offset: Word, donor: Word, progress: Table', 'returns': 'Long', 'flow': 'checked_state(state)\nuint(receiver_offset, 16)\nuint(donor, 16)\nprogress = state.checked_table(progress)\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=receiver_offset, target_y=donor, scan=progress.cursor())\nreturn grant_duel_fallback_progress_fields(BattlePresentationMemory(state), frame).count'}})

DECLARATIONS.update({'grant_duel_troop_difference_progress': {'signature': 'state: GameplayState, receiver: Word, troop_difference: Long, progress: Table', 'returns': 'Long', 'flow': 'checked_state(state)\nuint(receiver, 16)\nuint(troop_difference, 32)\nprogress = state.checked_table(progress)\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=receiver, unit=troop_difference, scan=progress.cursor())\nreturn grant_duel_troop_difference_progress_fields(BattlePresentationMemory(state), frame).count'}})

DECLARATIONS.update({'remove_zero_readiness_duelist': {'signature': 'state: GameplayState, officer: Word', 'returns': 'None', 'flow': 'checked_state(state)\nuint(officer, 16)\nentered = first_replace(FirstDeploymentFrame.unobserved(), target_y=officer)\nremove_zero_readiness_duelist_fields(BattlePresentationMemory(state), entered)'}})

DECLARATIONS.update({'settle_duel_result_roster': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\nsettle_duel_result_roster_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())'}})

DECLARATIONS.update({'transfer_battle_roster': {'signature': 'state: GameplayState, officer: Word', 'returns': 'None', 'flow': 'checked_state(state)\nuint(officer, 16)\nentered = first_replace(FirstDeploymentFrame.unobserved(), target_x=officer)\ntransfer_battle_roster_fields(BattlePresentationMemory(state), entered)'}})

DECLARATIONS.update({'_duel_result_write_fields': {'signature': 'memory, frame: FirstDeploymentFrame, address: Long, size: Word, value: Long', 'returns': 'FirstDeploymentFrame', 'flow': "if size not in (1, 2):\n    raise ValueError('closed duel result BYTE/WORD store required')\nmemory.state.write(address, size, value)\nreturn _movement_test(memory.state, frame, value, size * 8)"}})

DECLARATIONS.update({'_duel_result_call_fields': {'signature': 'memory, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "from .business_battle import _presentation_call_fields, _presentation_random_fields\nallowed = ((33748, 100570), (33748, 100666), (100820, 100624), (100820, 100720), (100948, 100634), (100948, 100730), (100910, 100768), (100910, 100794), (101012, 100818), (101062, 101046), (101062, 101060))\nif (target, continuation) not in allowed:\n    raise ValueError('original duel settlement child and continuation required')\ndef child(actual_memory, entered):\n    if target == 33748:\n        return _presentation_random_fields(actual_memory, entered)\n    if target == 100820:\n        return grant_duel_fallback_progress_fields(actual_memory, entered)\n    if target == 100948:\n        return remove_zero_readiness_duelist_fields(actual_memory, entered)\n    if target == 100910:\n        return grant_duel_troop_difference_progress_fields(actual_memory, entered)\n    if target == 101012:\n        return settle_duel_result_roster_fields(actual_memory, entered)\n    return transfer_battle_roster_fields(actual_memory, entered)\nreturn _presentation_call_fields(memory, frame, continuation, child)"}})

DECLARATIONS.update({'_duel_training_side_fields': {'signature': 'memory, frame: FirstDeploymentFrame, side: Word', 'returns': 'FirstDeploymentFrame', 'flow': "if side not in (0, 1):\n    raise ValueError('closed original duelist side required')\nstate = memory.state\nofficer_address, donor_address = (4294934752, 4294934754) if side == 0 else (4294934754, 4294934752)\nframe = _movement_move(state, frame, 'target_x', state.read(officer_address, 2), 16)\nframe = _movement_move(state, frame, 'unit', state.read(4294934785 + side * 2, 1), 8)\nframe = _movement_compare(state, frame, state.read(4294934804, 2), 4 + side, 16)\nif frame.status & 4:\n    stack = frame.stack_cursor.advance(-2)\n    stack.set_word(0, low16(frame.target_x))\n    frame = first_replace(frame, stack_cursor=stack)\n    frame = _movement_test(state, frame, low16(frame.target_x), 16)\n    frame = _duel_result_call_fields(memory, frame, 33748, 100570 if side == 0 else 100666)\n    frame = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)\n    frame = _movement_move_long(state, frame, 'target_y', frame.target_x)\n    value = frame.target_x\n    shifted = u32(value << 1)\n    flags = (17 if value & 2147483648 else 0) | (8 if shifted & 2147483648 else 0) | (4 if shifted == 0 else 0)\n    state.sr = state.sr & 65504 | flags\n    frame = first_replace(frame, target_x=shifted, status=flags)\n    frame = _movement_add_word(state, frame, 'target_x', low16(frame.target_y))\n    frame = _movement_move_long(state, frame, 'target_x', swap_words(frame.target_x))\n    frame = _movement_adjust_word(state, frame, 'target_x', 1)\n    frame, training = _movement_binary_flags(state, frame, low16(frame.unit), low16(frame.target_x), 16, True)\n    frame = first_replace(frame, unit=replace_word(frame.unit, training))\n    if frame.status & 1:\n        frame = _movement_move(state, frame, 'unit', 0, 16)\n    saved = frame.stack_cursor.word()\n    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\n    frame = _movement_move(state, frame, 'target_x', saved, 16)\nframe = _duel_result_write_fields(memory, frame, u32(frame.roster.base + s16(low16(frame.target_x))), 1, low8(frame.unit))\nframe = _movement_fixed_shift_word(state, frame, 'target_x', 1)\nreadiness = state.read(4294934796 + side * 2, 2)\nframe = _duel_result_write_fields(memory, frame, u32(frame.candidates.base + s16(low16(frame.target_x))), 2, readiness)\nif frame.status & 4:\n    frame = _movement_move(state, frame, 'target_y', state.read(donor_address, 2), 16)\n    frame = _duel_result_call_fields(memory, frame, 100820, 100624 if side == 0 else 100720)\n    frame = _movement_move(state, frame, 'target_y', state.read(officer_address, 2), 16)\n    frame = _duel_result_call_fields(memory, frame, 100948, 100634 if side == 0 else 100730)\nreturn frame"}})

DECLARATIONS.update({'settle_duel_training_and_troops_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.validate_frame(frame)\nfrom ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary\nif frame.stack_cursor is None:\n    raise MovementContinuationBoundary(100518, frame, 'actual duel settlement stack required')\nstate = memory.state\nframe = first_replace(frame, roster=state.table_at(4294952192).cursor(), candidates=state.table_at(4294947328).cursor(), controller=state.table_at(4294952960), scan=state.table_at(4294950912).cursor(), opponent=state.table_at(4294950400))\nframe = _duel_training_side_fields(memory, frame, 0)\nframe = _duel_training_side_fields(memory, frame, 1)\nframe = _movement_move(state, frame, 'offset_y', state.read(4294934752, 2), 16)\nframe = _movement_move(state, frame, 'choice', state.read(4294934754, 2), 16)\nfor old_officer, receiver, troops_address, continuation in (('offset_y', 'choice', 4294934808, 100768), ('choice', 'offset_y', 4294934810, 100794)):\n    frame = _movement_move(state, frame, 'target_x', low16(frame.carrier(old_officer)), 16)\n    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)\n    frame = _movement_move(state, frame, 'unit', frame.controller.word(s16(low16(frame.target_x)), 2), 16)\n    frame, difference = _movement_binary_flags(state, frame, low16(frame.unit), state.read(troops_address, 2), 16, True)\n    frame = first_replace(frame, unit=replace_word(frame.unit, difference))\n    if frame.status & 1:\n        frame = _movement_move(state, frame, 'unit', 0, 16)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.carrier(receiver)), 16)\n    frame = _duel_result_call_fields(memory, frame, 100910, continuation)\nframe = _movement_fixed_shift_word(state, frame, 'offset_y', 2)\nframe = _movement_fixed_shift_word(state, frame, 'choice', 2)\nfor carrier, address in (('offset_y', 4294934808), ('choice', 4294934810)):\n    frame = _duel_result_write_fields(memory, frame, u32(frame.controller.base + s16(low16(frame.carrier(carrier))) + 2), 2, state.read(address, 2))\nreturn _duel_result_call_fields(memory, frame, 101012, 100818)"}})

DECLARATIONS.update({'_duel_progress_store_fields': {'signature': 'memory, frame: FirstDeploymentFrame, offset: Word', 'returns': 'FirstDeploymentFrame', 'flow': "state = memory.state\nframe = _movement_move(state, frame, 'count', frame.scan.word(s16(offset)), 16)\nframe = _movement_add_word(state, frame, 'count', low16(frame.unit))\nframe = _movement_compare(state, frame, low16(frame.count), 999, 16)\nif not frame.status & 5:\n    frame = _movement_move(state, frame, 'count', 999, 16)\nreturn _duel_result_write_fields(memory, frame, u32(frame.scan.base + s16(offset)), 2, low16(frame.count))"}})

DECLARATIONS.update({'grant_duel_fallback_progress_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.validate_frame(frame)\nstate = memory.state\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 1)\nframe = _movement_move(state, frame, 'unit', frame.scan.word(s16(low16(frame.target_y))), 16)\nframe = _movement_move_long(state, frame, 'unit', u32(s16(low16(frame.unit))))\nframe = _movement_divu_word(state, frame, 'unit', 40, 100828)\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 1, True)\nframe = _movement_move(state, frame, 'count', state.read(4294964874, 2), 16)\nframe = _movement_fixed_shift_word(state, frame, 'count', 1)\nframe = first_replace(frame, scratch=state.table_at(4294964318))\nframe = _movement_compare(state, frame, low16(frame.target_y), frame.scratch.word(s16(low16(frame.count))), 16)\nhead = bool(frame.status & 4)\nif not head:\n    frame = first_replace(frame, scratch=state.table_at(4294942758))\n    frame = _movement_compare(state, frame, low16(frame.target_y), frame.scratch.word(s16(low16(frame.count))), 16)\n    head = bool(frame.status & 4)\nif head:\n    frame = _movement_add_word(state, frame, 'unit', 30)\nframe = first_replace(frame, scratch=state.table_at(4294952704))\nframe = _movement_bit(state, frame, frame.scratch.byte(s16(low16(frame.target_y))), 4)\nif not frame.status & 4:\n    frame = _movement_add_word(state, frame, 'unit', 20)\nreturn _duel_progress_store_fields(memory, frame, low16(frame.target_x))"}})

DECLARATIONS.update({'grant_duel_troop_difference_progress_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.validate_frame(frame)\nstate = memory.state\nframe = _movement_move_long(state, frame, 'unit', frame.unit & 65535)\nframe = _movement_divu_word(state, frame, 'unit', 100, 100916)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 1)\nreturn _duel_progress_store_fields(memory, frame, low16(frame.target_y))"}})

DECLARATIONS.update({'_duel_result_compact_roster_fields': {'signature': 'memory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'while True:\n    word_value = frame.roster.word()\n    frame = first_replace(frame, roster=frame.roster.advance(2))\n    frame = _duel_result_write_fields(memory, frame, u32(frame.roster.base - 4), 2, word_value)\n    if frame.status & 8:\n        return frame'}})

DECLARATIONS.update({'remove_zero_readiness_duelist_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.validate_frame(frame)\nstate = memory.state\nframe = _movement_save_longs(state, frame, ('unit', 'roster'))\nframe = _movement_test(state, frame, state.read(4294963168, 2), 16)\nif not frame.status & 4:\n    frame = first_replace(frame, roster=state.table_at(4294953984).cursor())\n    frame = _duel_result_write_fields(memory, frame, u32(frame.roster.base + s16(low16(frame.target_y))), 1, 255)\n    frame = first_replace(frame, roster=state.table_at(4294944080).cursor())\n    frame = _movement_compare(state, frame, low16(frame.target_y), state.read(4294964994, 2), 16)\n    if not frame.status & 4:\n        frame = first_replace(frame, roster=state.table_at(4294944164).cursor())\n    while True:\n        value = frame.roster.word()\n        frame = first_replace(frame, roster=frame.roster.advance(2))\n        frame = _movement_move(state, frame, 'unit', value, 16)\n        if frame.status & 8:\n            break\n        frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 255, 16)\n        frame = _movement_compare(state, frame, low16(frame.unit), low16(frame.target_y), 16)\n        if frame.status & 4:\n            frame = _duel_result_compact_roster_fields(memory, frame)\n            break\nreturn _movement_restore_longs(state, frame, ('unit', 'roster'))"}})

DECLARATIONS.update({'settle_duel_result_roster_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.validate_frame(frame)\nstate = memory.state\nframe = _movement_test(state, frame, state.read(4294963168, 2), 16)\nif frame.status & 4:\n    return frame\nframe = _movement_compare(state, frame, state.read(4294934804, 2), 6, 16)\nif frame.status & 1:\n    return frame\nprimary = bool(frame.status & 4)\nframe = _movement_move(state, frame, 'target_x', state.read(4294934752 if primary else 4294934754, 2), 16)\nreturn _duel_result_call_fields(memory, frame, 101062, 101046 if primary else 101060)"}})

DECLARATIONS.update({'transfer_battle_roster_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.validate_frame(frame)\nstate = memory.state\nframe = first_replace(frame, roster=state.table_at(4294944164).cursor(), candidates=state.table_at(4294944122).cursor())\nframe = _movement_compare(state, frame, low16(frame.target_x), state.read(4294964994, 2), 16)\nif frame.status & 4:\n    frame = first_replace(frame, roster=state.table_at(4294944080).cursor(), candidates=state.table_at(4294944206).cursor())\nwhile True:\n    value = frame.roster.word()\n    frame = first_replace(frame, roster=frame.roster.advance(2))\n    frame = _movement_move(state, frame, 'target_y', value, 16)\n    if frame.status & 8:\n        return frame\n    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 255, 16)\n    frame = _movement_compare(state, frame, low16(frame.target_y), low16(frame.target_x), 16)\n    if frame.status & 4:\n        break\nframe = _duel_result_compact_roster_fields(memory, frame)\nwhile True:\n    value = frame.candidates.word()\n    frame = first_replace(frame, candidates=frame.candidates.advance(2))\n    frame = _movement_test(state, frame, value, 16)\n    if frame.status & 8:\n        break\nframe = _duel_result_write_fields(memory, frame, u32(frame.candidates.base - 2), 2, low16(frame.target_x))\nreturn _duel_result_write_fields(memory, frame, frame.candidates.base, 2, 65535)"}})

APPROVED.setdefault('business_movement_support',set()).update({'_movement_move_long', '_movement_save_longs', '_movement_compare', '_movement_add_word', '_movement_move', '_movement_restore_longs', '_movement_fixed_shift_word', '_movement_binary_flags', '_movement_bit', '_movement_test', '_movement_divu_word', '_movement_adjust_word'})

APPROVED.setdefault('business_battle',set()).update({'_presentation_call_fields', '_presentation_random_fields'})

APPROVED.setdefault('contexts_gameplay',set()).update({'MovementContinuationBoundary'})

DECLARATIONS.update({'grant_duel_fallback_progress_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.validate_frame(frame)\nstate = memory.state\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 1)\nframe = _movement_move(state, frame, 'unit', frame.scan.word(s16(low16(frame.target_y))), 16)\nframe = _movement_move_long(state, frame, 'unit', u32(s16(low16(frame.unit))))\nframe = _movement_divu_word(state, frame, 'unit', 40, 100828)\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 1, True)\nframe = _movement_move(state, frame, 'count', state.read(4294964874, 2), 16)\nframe = _movement_fixed_shift_word(state, frame, 'count', 1)\nframe = first_replace(frame, scratch=state.table_at(4294964318))\nframe = _movement_compare(state, frame, low16(frame.target_y), frame.scratch.word(s16(low16(frame.count))), 16)\nhead = bool(frame.status & 4)\nif not head:\n    frame = first_replace(frame, scratch=state.table_at(4294942758))\n    frame = _movement_compare(state, frame, low16(frame.target_y), frame.scratch.word(s16(low16(frame.count))), 16)\n    head = bool(frame.status & 4)\nif head:\n    frame = _movement_add_word(state, frame, 'unit', 30)\nframe = first_replace(frame, scratch=state.table_at(4294952704))\nfrom .business_battle import _postbattle_bit_fields\nframe = _postbattle_bit_fields(frame, bool(frame.scratch.byte(s16(low16(frame.target_y))) & 16))\nstate.sr = state.sr & 65504 | frame.status\nif not frame.status & 4:\n    frame = _movement_add_word(state, frame, 'unit', 20)\nreturn _duel_progress_store_fields(memory, frame, low16(frame.target_x))"}})

APPROVED.setdefault('business_battle',set()).add('_postbattle_bit_fields')

DECLARATIONS.update({'settle_duel_packets': {'signature': 'state: GameplayState, context: DuelSettlementContext', 'returns': 'CarryOutcome', 'flow': 'checked_state(state)\ncontext = _reuse_checked_context(context, DuelSettlementContext)\nframe = first_replace(FirstDeploymentFrame.unobserved(), unit=context.training_carrier)\nframe = settle_duel_packets_fields(BattlePresentationMemory(state), frame)\nreturn state.carry_result(int(bool(frame.status & 1)))'}})

DECLARATIONS.update({'apply_duel_disposition': {'signature': 'state: GameplayState, context: DuelDispositionContext', 'returns': 'None', 'flow': 'checked_state(state)\ncontext = _reuse_checked_context(context, DuelDispositionContext)\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=context.officer, unit=context.disposition)\napply_duel_disposition_fields(BattlePresentationMemory(state), frame)'}})

DECLARATIONS.update({'detach_zero_readiness_duelists': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\ndetach_zero_readiness_duelists_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())'}})

DECLARATIONS.update({'detach_defeated_duelist': {'signature': 'state: GameplayState, officer: Word', 'returns': 'None', 'flow': 'checked_state(state)\nuint(officer, 16)\nframe = first_replace(FirstDeploymentFrame.unobserved(), target_x=officer)\ndetach_defeated_duelist_fields(BattlePresentationMemory(state), frame)'}})

DECLARATIONS.update({'_duel_result_compact_roster_fields': {'signature': "memory, frame: FirstDeploymentFrame, view_role: str='roster'", 'returns': 'FirstDeploymentFrame', 'flow': "if view_role not in ('roster', 'candidates'):\n    raise ValueError('closed original compacted roster role required')\nwhile True:\n    view = frame.roster if view_role == 'roster' else frame.candidates\n    word_value = view.word()\n    view = view.advance(2)\n    frame = first_replace(frame, **{view_role: view})\n    frame = _duel_result_write_fields(memory, frame, u32(view.base - 4), 2, word_value)\n    if frame.status & 8:\n        return frame"}})

DECLARATIONS.update({'_duel_result_call_fields': {'signature': 'memory, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "from .business_battle import _presentation_call_fields, _presentation_random_fields\nallowed = ((33748, 100570), (33748, 100666), (100820, 100624), (100820, 100720), (100948, 100634), (100948, 100730), (100910, 100768), (100910, 100794), (101012, 100818), (101062, 101046), (101062, 101060), (101268, 101206), (101268, 101222), (101462, 101250), (100518, 101254), (101512, 101490), (101512, 101510))\nif (target, continuation) not in allowed:\n    raise ValueError('original duel settlement child and continuation required')\ndef child(actual_memory, entered):\n    if target == 33748:\n        return _presentation_random_fields(actual_memory, entered)\n    if target == 100820:\n        return grant_duel_fallback_progress_fields(actual_memory, entered)\n    if target == 100948:\n        return remove_zero_readiness_duelist_fields(actual_memory, entered)\n    if target == 100910:\n        return grant_duel_troop_difference_progress_fields(actual_memory, entered)\n    if target == 101012:\n        return settle_duel_result_roster_fields(actual_memory, entered)\n    if target == 101268:\n        return apply_duel_disposition_fields(actual_memory, entered)\n    if target == 101462:\n        return detach_zero_readiness_duelists_fields(actual_memory, entered)\n    if target == 101512:\n        return detach_defeated_duelist_fields(actual_memory, entered)\n    if target == 100518:\n        return settle_duel_training_and_troops_fields(actual_memory, entered)\n    return transfer_battle_roster_fields(actual_memory, entered)\nreturn _presentation_call_fields(memory, frame, continuation, child)"}})

DECLARATIONS.update({'_duel_result_seek_unbounded_fields': {'signature': 'memory, frame: FirstDeploymentFrame, view_role: str, carrier: str', 'returns': 'FirstDeploymentFrame', 'flow': "if (view_role, carrier) not in (('roster', 'target_y'), ('candidates', 'target_y'), ('candidates', 'count')):\n    raise ValueError('closed original disposition search role required')\nstate = memory.state\nwhile True:\n    view = frame.roster if view_role == 'roster' else frame.candidates\n    value = view.word()\n    frame = first_replace(frame, **{view_role: view.advance(2)})\n    frame = _movement_move(state, frame, carrier, value, 16)\n    frame = _movement_move(state, frame, carrier, low16(frame.carrier(carrier)) & 255, 16)\n    frame = _movement_compare(state, frame, low16(frame.carrier(carrier)), low16(frame.target_x), 16)\n    if frame.status & 4:\n        return frame"}})

DECLARATIONS.update({'_duel_result_append_retired_fields': {'signature': 'memory, frame: FirstDeploymentFrame, view_role: str', 'returns': 'FirstDeploymentFrame', 'flow': "if view_role not in ('roster', 'candidates'):\n    raise ValueError('closed original retired roster required')\nwhile True:\n    view = frame.roster if view_role == 'roster' else frame.candidates\n    value = view.word()\n    view = view.advance(2)\n    frame = first_replace(frame, **{view_role: view})\n    frame = _movement_test(memory.state, frame, value, 16)\n    if frame.status & 8:\n        break\nframe = _duel_result_write_fields(memory, frame, u32(view.base - 2), 2, low16(frame.target_x))\nreturn _duel_result_write_fields(memory, frame, view.base, 2, 65535)"}})

DECLARATIONS.update({'settle_duel_packets_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.validate_frame(frame)\nstate = memory.state\nframe = first_replace(frame, roster=state.table_at(16740432).cursor(), candidates=state.table_at(16740512).cursor(), controller=state.table_at(16740592), scan=state.table_at(16740593).cursor())\nframe = _movement_move(state, frame, 'target_x', state.read(16740458, 2), 16)\nframe = _movement_compare(state, frame, low16(frame.target_x), state.read(4294934752, 2), 16)\nif not frame.status & 4:\n    frame = first_replace(frame, roster=frame.candidates, candidates=frame.roster, controller=state.table_at(frame.scan.base), scan=state.table_at(frame.controller.base).cursor())\nframe = _duel_result_write_fields(memory, frame, 4294934796, 2, frame.roster.word(0, 28))\nframe = _duel_result_write_fields(memory, frame, 4294934798, 2, frame.candidates.word(0, 28))\nframe = _movement_move(state, frame, 'target_x', state.read(16740458, 2), 16)\nframe = _movement_move(state, frame, 'target_y', state.read(16740538, 2), 16)\nframe = _movement_move(state, frame, 'unit', state.read(16740592, 1), 8)\nif not frame.status & 4:\n    frame = _duel_result_call_fields(memory, frame, 101268, 101206)\nframe = first_replace(frame, target_x=frame.target_y, target_y=frame.target_x)\nframe = _movement_move(state, frame, 'unit', state.read(16740593, 1), 8)\nif not frame.status & 4:\n    frame = _duel_result_call_fields(memory, frame, 101268, 101222)\nframe = _movement_compare(state, frame, state.read(16740592, 1), 1, 8)\nblocked = bool(frame.status & 4)\nif not blocked:\n    frame = _movement_compare(state, frame, state.read(16740593, 1), 1, 8)\n    blocked = bool(frame.status & 4)\nif not blocked:\n    frame = _duel_result_call_fields(memory, frame, 101462, 101250)\n    frame = _duel_result_call_fields(memory, frame, 100518, 101254)\n    state.sr &= 65534\nelse:\n    state.sr |= 1\nreturn first_replace(frame, status=state.sr & 31)"}})

DECLARATIONS.update({'apply_duel_disposition_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.validate_frame(frame)\nstate = memory.state\nsaved = ('target_x', 'target_y', 'roster', 'candidates')\nframe = _movement_save_longs(state, frame, saved)\nframe = _movement_test(state, frame, state.read(4294963168, 2), 16)\nif frame.status & 4:\n    frame = _movement_compare(state, frame, low8(frame.unit), 3, 8)\n    if not frame.status & 4:\n        frame = _movement_move(state, frame, 'target_y', 6, 16)\n        frame = _movement_compare(state, frame, low16(frame.target_x), state.read(4294934752, 2), 16)\n        if not frame.status & 4:\n            frame = _movement_move(state, frame, 'target_y', 7, 16)\n        frame = _duel_result_write_fields(memory, frame, 4294934804, 2, low16(frame.target_y))\n    return _movement_restore_longs(state, frame, saved)\nframe = _movement_compare(state, frame, low8(frame.unit), 2, 8)\ntransfer = bool(frame.status & 4)\nif transfer:\n    frame = _movement_compare(state, frame, low16(frame.target_x), state.read(4294964994, 2), 16)\n    primary = bool(frame.status & 4)\n    frame = first_replace(frame, roster=state.table_at(4294944080 if primary else 4294944164).cursor(), candidates=state.table_at(4294944206 if primary else 4294944122).cursor())\n    frame = _duel_result_seek_unbounded_fields(memory, frame, 'roster', 'target_y')\n    frame = _duel_result_compact_roster_fields(memory, frame)\n    frame = _duel_result_append_retired_fields(memory, frame, 'candidates')\nelse:\n    frame = _movement_compare(state, frame, low8(frame.unit), 3, 8)\n    if frame.status & 4:\n        frame = first_replace(frame, roster=state.table_at(4294944206).cursor(), candidates=state.table_at(4294944080).cursor())\n        frame = _movement_move(state, frame, 'count', state.read(4294964874, 2), 16)\n        frame = _movement_move(state, frame, 'count', low16(frame.count) | 128, 16)\n        frame = _movement_compare(state, frame, low16(frame.target_x), state.read(4294964994, 2), 16)\n        if not frame.status & 4:\n            frame = _movement_move(state, frame, 'count', low16(frame.count) | 64, 16)\n            frame = first_replace(frame, roster=state.table_at(4294944122).cursor(), candidates=state.table_at(4294944164).cursor())\n        frame = _duel_result_append_retired_fields(memory, frame, 'roster')\n        frame = _duel_result_seek_unbounded_fields(memory, frame, 'candidates', 'count')\n        frame = _duel_result_compact_roster_fields(memory, frame, 'candidates')\nreturn _movement_restore_longs(state, frame, saved)"}})

DECLARATIONS.update({'detach_zero_readiness_duelists_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.validate_frame(frame)\nstate = memory.state\nframe = _movement_test(state, frame, state.read(4294963168, 2), 16)\nif frame.status & 4:\n    return frame\nfor readiness, officer, continuation in ((16740460, 16740458, 101490), (16740540, 16740538, 101510)):\n    frame = _movement_test(state, frame, state.read(readiness, 2), 16)\n    if frame.status & 4:\n        frame = _movement_move(state, frame, 'target_x', state.read(officer, 2), 16)\n        frame = _duel_result_call_fields(memory, frame, 101512, continuation)\nreturn frame"}})

DECLARATIONS.update({'detach_defeated_duelist_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "memory.validate_frame(frame)\nstate = memory.state\nframe = first_replace(frame, roster=state.table_at(4294953984).cursor())\nframe = _duel_result_write_fields(memory, frame, u32(frame.roster.base + s16(low16(frame.target_x))), 1, 255)\nframe = first_replace(frame, candidates=state.table_at(4294944080).cursor())\nframe = _movement_compare(state, frame, low16(frame.target_x), state.read(4294964994, 2), 16)\nif not frame.status & 4:\n    frame = first_replace(frame, candidates=state.table_at(4294944164).cursor())\nframe = _duel_result_seek_unbounded_fields(memory, frame, 'candidates', 'target_y')\nreturn _duel_result_compact_roster_fields(memory, frame, 'candidates')"}})

# D52 exact imports/full DECL; ordinary mnemonic lowerers unchanged.
APPROVED.setdefault((2, 'high_level_battle_ai.business_formation'),set()).update(('_first_add_word', '_first_byte', '_first_compare_long', '_first_compare_word', '_first_long', '_first_right_word', '_first_shift_word', '_first_sub_word', '_first_word'))
APPROVED.setdefault((2, 'high_level_main_flows.business_movement_support'),set()).update(('_movement_add_word', '_movement_adjust_word', '_movement_arithmetic_long', '_movement_binary_flags', '_movement_bit', '_movement_compare', '_movement_divu_word', '_movement_fixed_shift_word', '_movement_move', '_movement_move_long', '_movement_multiply_word', '_movement_restore_longs', '_movement_save_longs', '_movement_test', 'signed_divmod_fields'))
APPROVED.setdefault((2, 'high_level_battle_ai.contexts_first_deployment'),set()).update(('FirstDeploymentFrame', 'first_replace'))
APPROVED.setdefault((2, 'high_level_scene_flows.domain'),set()).update(('SceneState', 'divu_retained', 'low16', 'low8', 'replace_byte', 'replace_word', 's16', 'swap_words', 'u16', 'u32', 'u8'))
APPROVED.setdefault((2, 'high_level_main_flows.contexts_gameplay'),set()).update(('MovementContinuationBoundary',))
APPROVED.setdefault('business_services',set()).update(('_scene_refresh_emit', '_scene_refresh_flags', 'load_gameplay_scene_fields', 'present_gameplay_message_fields', 'refresh_gameplay_scene_fields'))
APPROVED.setdefault('business_calendar',set()).update(('choose_city_head_after_mortality_fields', 'process_calendar_city_cycle_fields', 'process_calendar_event_schedulers_fields', 'process_first_calendar_event_fields', 'process_second_calendar_event_fields', 'process_third_calendar_event_fields', 'remove_mortal_officer_with_message_fields', 'scan_calendar_officer_mortality_fields', 'show_calendar_event_message_fields', 'show_first_calendar_event_values_fields', 'show_second_calendar_event_values_fields', 'show_third_calendar_event_values_fields'))
APPROVED.setdefault('business_battle',set()).update(('_postbattle_compare_byte_fields',))
APPROVED.setdefault((2, 'high_level_main_flows.business_gameplay'),set()).update(('_setup_asl_word_fields',))
DECLARATIONS.update({'_calendar_arithmetic_fields': {'flow': 'previous = _calendar_value_fields(frame, carrier)\n'
                                         'frame, value = _movement_binary_flags(memory.state, frame, previous & (1 << width * 8) - 1, '
                                         'operand, width * 8, subtract)\n'
                                         'retained = replace_byte(previous, value) if width == 1 else replace_word(previous, value) if '
                                         'width == 2 else value\n'
                                         'return first_replace(frame, **{carrier: retained})',
                                 'returns': None,
                                 'signature': 'memory, frame, carrier, operand, width=2, subtract=False'},
 '_calendar_bit_fields': {'flow': 'from .business_battle import _postbattle_bit_fields\n'
                                  'return memory.sync_status(_postbattle_bit_fields(frame, bool(value & mask)))',
                          'returns': None,
                          'signature': 'memory, frame, value, mask'},
 '_calendar_call_fields': {'flow': 'if frame.stack_cursor is None:\n'
                                   '    raise SceneRefreshBoundary(target, frame, token)\n'
                                   'stack = frame.stack_cursor.advance(-4)\n'
                                   'stack.set_long(0, token)\n'
                                   'entered = first_replace(frame, stack_cursor=stack)\n'
                                   'result = _calendar_child_fields(memory, entered, target)\n'
                                   'memory.frame(result)\n'
                                   'actual = result.stack_cursor.long()\n'
                                   'if actual != token:\n'
                                   '    raise SceneRefreshBoundary(actual, result, token)\n'
                                   'return memory.sync_status(first_replace(result, stack_cursor=result.stack_cursor.advance(4)))',
                           'returns': None,
                           'signature': 'memory, frame, target, token'},
 '_calendar_child_fields': {'flow': 'from .business_calendar import process_calendar_city_cycle_fields, '
                                    'scan_calendar_officer_mortality_fields, remove_mortal_officer_with_message_fields, '
                                    'choose_city_head_after_mortality_fields, process_calendar_event_schedulers_fields, '
                                    'show_calendar_event_message_fields, process_first_calendar_event_fields, '
                                    'show_first_calendar_event_values_fields, process_second_calendar_event_fields, '
                                    'show_second_calendar_event_values_fields, process_third_calendar_event_fields, '
                                    'show_third_calendar_event_values_fields\n'
                                    'own = {93112: replenish_b200_troops_fields, 93194: grow_original_long_field_fields, 93228: '
                                    'credit_primary_fields, 93254: credit_secondary_fields, 93276: commit_income_fields, 93298: '
                                    'scaled_income_fields, 93336: deplete_income_fields, 93456: debit_primary_fields, 93482: '
                                    'debit_secondary_fields, 93504: settle_expense_fields, 93674: settle_shortage_fields, 94230: '
                                    'reset_queue_fields, 94246: append_queue_fields, 94630: submit_calendar_three_fields, 95042: '
                                    'submit_calendar_four_fields, 95348: submit_calendar_classified_fields, 95508: scale_e1e0_fields, '
                                    '95530: scale_e140_fields, 95552: scale_e320_fields, 95574: scale_e000_fields, 95596: '
                                    'scale_e0a0_fields, 95618: scale_e5a0_fields, 95640: sample_once_fields, 95656: sample_small_fields, '
                                    '95682: sample_wide_fields, 95708: wrapped_product_fields, 95724: divide_percent_fields}\n'
                                    'calendar = {92986: process_calendar_city_cycle_fields, 93914: scan_calendar_officer_mortality_fields, '
                                    '94018: remove_mortal_officer_with_message_fields, 94170: choose_city_head_after_mortality_fields, '
                                    '94204: process_calendar_event_schedulers_fields, 94296: show_calendar_event_message_fields, 94334: '
                                    'process_first_calendar_event_fields, 94552: show_first_calendar_event_values_fields, 94716: '
                                    'process_second_calendar_event_fields, 94964: show_second_calendar_event_values_fields, 95142: '
                                    'process_third_calendar_event_fields, 95270: show_third_calendar_event_values_fields}\n'
                                    'if target in own:\n'
                                    '    return own[target](memory, frame)\n'
                                    'if target in calendar:\n'
                                    '    return calendar[target](memory, frame)\n'
                                    'if target == 33748:\n'
                                    '    from .business_battle import _presentation_random_fields\n'
                                    '    from .contexts_battle import BattlePresentationMemory\n'
                                    '    return _presentation_random_fields(BattlePresentationMemory(memory.state), frame)\n'
                                    'if target in (24392, 57846):\n'
                                    '    from .business_battle import build_roster_fields, choose_city_head_fields\n'
                                    '    from .contexts_battle import BattlePresentationMemory\n'
                                    '    algorithm = build_roster_fields if target == 24392 else choose_city_head_fields\n'
                                    '    return algorithm(BattlePresentationMemory(memory.state), frame)\n'
                                    'if target == 218976:\n'
                                    '    from ..high_level_main_flows.business_movement_support import signed_divmod_fields\n'
                                    '    return signed_divmod_fields(memory.state, frame)\n'
                                    'if target in (44872, 67372, 199284):\n'
                                    '    from .business_services import refresh_gameplay_scene_fields, load_gameplay_scene_fields, '
                                    'present_gameplay_message_fields\n'
                                    '    algorithm = refresh_gameplay_scene_fields if target == 44872 else load_gameplay_scene_fields if '
                                    'target == 67372 else present_gameplay_message_fields\n'
                                    '    return algorithm(memory, frame)\n'
                                    'raise SceneRefreshBoundary(target, frame, None)',
                            'returns': None,
                            'signature': 'memory, frame, target'},
 '_calendar_compare_fields': {'flow': 'if width == 1:\n'
                                      '    from .business_battle import _postbattle_compare_byte_fields\n'
                                      '    frame = _postbattle_compare_byte_fields(frame, left, right)\n'
                                      'elif width == 2:\n'
                                      '    frame = _first_compare_word(frame, left, right)\n'
                                      'elif width == 4:\n'
                                      '    frame = _first_compare_long(frame, left, right)\n'
                                      'else:\n'
                                      "    raise ValueError('actual calendar comparison width required')\n"
                                      'return memory.sync_status(frame)',
                              'returns': None,
                              'signature': 'memory, frame, left, right, width=2'},
 '_calendar_db_fields': {'flow': 'remaining_word = u16(low16(_calendar_value_fields(frame, carrier)) - 1)\n'
                                 'return (first_replace(frame, **{carrier: replace_word(frame.carrier(carrier), remaining_word)}), '
                                 'remaining_word != 65535)',
                         'returns': None,
                         'signature': 'frame, carrier'},
 '_calendar_divu_fields': {'flow': 'previous = _calendar_value_fields(frame, carrier)\n'
                                   'if divisor == 0:\n'
                                   '    raise SceneRefreshBoundary(pc, frame, None)\n'
                                   'quotient = previous // divisor\n'
                                   'result = divu_retained(previous, divisor)\n'
                                   'if quotient > 65535:\n'
                                   '    if not discarded or pc not in (93198, 93318, 93562, 93600, 95362, 93850):\n'
                                   '        raise SceneRefreshBoundary(pc, frame, None)\n'
                                   '    return first_replace(frame, **{carrier: result})\n'
                                   'frame = first_replace(frame, **{carrier: result})\n'
                                   'return _calendar_test_fields(memory, frame, quotient)',
                           'returns': None,
                           'signature': 'memory, frame, carrier, divisor, pc, discarded=False'},
 '_calendar_frame_fields': {'flow': 'if type(memory) is not SceneRefreshMemory:\n'
                                    "    raise ValueError('one existing Scene/gameplay calendar memory required')\n"
                                    'memory.frame(frame)\n'
                                    'from ..high_level_scene_flows.domain import SceneState\n'
                                    'if type(memory.state) is SceneState:\n'
                                    '    if frame.stack_cursor is None:\n'
                                    '        raise SceneRefreshBoundary(entry, frame, None)\n'
                                    '    frame.validate(memory.state, True)\n'
                                    'elif frame.stack_cursor is None or frame.status is None:\n'
                                    '    raise SceneRefreshBoundary(entry, frame, None)\n'
                                    'return frame',
                            'returns': 'FirstDeploymentFrame',
                            'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, entry: int'},
 '_calendar_legacy_entry_fields': {'flow': 'checked_state(state)\n'
                                           'for value in words:\n'
                                           '    uint(value, 16)\n'
                                           'frame = FirstDeploymentFrame.unobserved()\n'
                                           'for carrier, value in longs:\n'
                                           '    uint(value, 32)\n'
                                           '    frame = first_replace(frame, **{carrier: value})\n'
                                           'for carrier, table in views:\n'
                                           '    table = state.checked_table(table)\n'
                                           '    frame = first_replace(frame, **{carrier: table.cursor()})\n'
                                           'return (SceneRefreshMemory(state), frame)',
                                   'returns': None,
                                   'signature': 'state, words=(), longs=(), views=()'},
 '_calendar_memory_arithmetic_fields': {'flow': 'previous = memory.state.read(address, width)\n'
                                                'frame, value = _movement_binary_flags(memory.state, frame, previous, operand, width * 8, '
                                                'subtract)\n'
                                                'memory.state.write(address, width, value)\n'
                                                'return frame',
                                        'returns': None,
                                        'signature': 'memory, frame, address, operand, width=2, subtract=False'},
 '_calendar_move_fields': {'flow': 'if width == 1:\n'
                                   '    frame = _first_byte(frame, carrier, value)\n'
                                   'elif width == 2:\n'
                                   '    frame = _first_word(frame, carrier, value)\n'
                                   'elif width == 4:\n'
                                   '    frame = _first_long(frame, carrier, value)\n'
                                   'else:\n'
                                   "    raise ValueError('actual calendar operand width required')\n"
                                   'return memory.sync_status(frame)',
                           'returns': None,
                           'signature': 'memory, frame, carrier, value, width=2'},
 '_calendar_pop_word_fields': {'flow': 'value = frame.stack_cursor.word()\n'
                                       'frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\n'
                                       'return _calendar_write_fields(memory, frame, address, value)',
                               'returns': None,
                               'signature': 'memory, frame, address'},
 '_calendar_product_terms': {'flow': 'value = checked_long(value)\n'
                                     'factor = checked_word(factor)\n'
                                     'lower = mulu16(value, factor)\n'
                                     'upper = mulu16(swap_words(value), factor)\n'
                                     'shifted = u32(upper << 16)\n'
                                     'return (lower, upper, shifted, add32(lower, shifted))',
                             'returns': None,
                             'signature': 'value, factor'},
 '_calendar_push_word_fields': {'flow': 'if frame.stack_cursor is None:\n'
                                        '    raise SceneRefreshBoundary(92990, frame, None)\n'
                                        'stack = frame.stack_cursor.advance(-2)\n'
                                        'stack.set_word(0, value)\n'
                                        'frame = first_replace(frame, stack_cursor=stack)\n'
                                        'return _calendar_test_fields(memory, frame, value)',
                                'returns': None,
                                'signature': 'memory, frame, value'},
 '_calendar_restore_fields': {'flow': 'return _movement_restore_longs(memory.state, frame, names)',
                              'returns': None,
                              'signature': 'memory, frame, names'},
 '_calendar_sample_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, entry)\n'
                                     "frame = _calendar_save_fields(memory, frame, ('target_y',))\n"
                                     'while True:\n'
                                     '    frame = _calendar_call_fields(memory, frame, 33748, token)\n'
                                     '    if mask is None:\n'
                                     '        break\n'
                                     "    frame = _calendar_move_fields(memory, frame, 'target_x', low16(frame.target_x) & mask)\n"
                                     '    frame = _calendar_compare_fields(memory, frame, low16(frame.target_x), limit)\n'
                                     '    if frame.status & 1:\n'
                                     '        break\n'
                                     "return _calendar_restore_fields(memory, frame, ('target_y',))",
                             'returns': None,
                             'signature': 'memory, frame, entry, token, mask=None, limit=None'},
 '_calendar_save_fields': {'flow': 'if frame.stack_cursor is None:\n'
                                   '    raise SceneRefreshBoundary(94018, frame, None)\n'
                                   'return _movement_save_longs(memory.state, frame, names)',
                           'returns': None,
                           'signature': 'memory, frame, names'},
 '_calendar_scale_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, entry)\n'
                                    'frame = first_replace(frame, roster=memory.cursor_at(address))\n'
                                    "frame = _calendar_move_fields(memory, frame, 'unit', frame.roster.long(low16(frame.choice)), 4)\n"
                                    'frame = _calendar_call_fields(memory, frame, 95708, product_token)\n'
                                    'frame = _calendar_call_fields(memory, frame, 95724, division_token)\n'
                                    'return _calendar_write_fields(memory, frame, frame.roster.address(low16(frame.choice)), frame.unit, '
                                    '4)',
                            'returns': None,
                            'signature': 'memory, frame, entry, address, product_token, division_token'},
 '_calendar_shift_fields': {'flow': 'original = low16(_calendar_value_fields(frame, carrier))\n'
                                    'if arithmetic:\n'
                                    '    from ..high_level_main_flows.business_gameplay import _setup_asl_word_fields\n'
                                    "    if carrier == 'choice' and amount == 2:\n"
                                    '        projected = first_replace(frame, target_x=frame.choice)\n'
                                    "        shifted = _setup_asl_word_fields(memory.state, projected, 'target_x', 2)\n"
                                    '        frame = first_replace(frame, choice=shifted.target_x, status=shifted.status)\n'
                                    '    else:\n'
                                    '        frame = _setup_asl_word_fields(memory.state, frame, carrier, amount)\n'
                                    'elif amount == 0:\n'
                                    '    return _calendar_test_fields(memory, frame, original)\n'
                                    'elif right:\n'
                                    '    frame = _first_right_word(frame, carrier, original, amount)\n'
                                    'else:\n'
                                    '    frame = _first_shift_word(frame, carrier, original, amount)\n'
                                    'return memory.sync_status(frame)',
                            'returns': None,
                            'signature': 'memory, frame, carrier, amount, right=False, arithmetic=False'},
 '_calendar_submit_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, entry)\n'
                                     'frame = first_replace(frame, roster=memory.cursor_at(4294964264))\n'
                                     "frame = _calendar_move_fields(memory, frame, 'choice', frame.roster.byte(low16(frame.target_x)), 1)\n"
                                     'if frame.status & 8:\n'
                                     '    return frame\n'
                                     "frame = _calendar_move_fields(memory, frame, 'choice', low16(frame.target_x))\n"
                                     'frame = _calendar_call_fields(memory, frame, 95640, once_token)\n'
                                     "frame = _calendar_move_fields(memory, frame, 'target_x', low16(frame.target_x) & 15)\n"
                                     'if not frame.status & 4:\n'
                                     "    return _calendar_move_fields(memory, frame, 'target_x', low16(frame.choice))\n"
                                     'frame = _calendar_call_fields(memory, frame, 94246, append_token)\n'
                                     "frame = _calendar_save_fields(memory, frame, ('choice',))\n"
                                     "frame = _calendar_shift_fields(memory, frame, 'choice', 2, arithmetic=True)\n"
                                     'for sampler, sample_token, base, target, scale_token in scales:\n'
                                     '    frame = _calendar_call_fields(memory, frame, sampler, sample_token)\n'
                                     "    frame = _calendar_arithmetic_fields(memory, frame, 'target_x', base)\n"
                                     '    frame = _calendar_call_fields(memory, frame, target, scale_token)\n'
                                     "frame = _calendar_restore_fields(memory, frame, ('choice',))\n"
                                     "return _calendar_move_fields(memory, frame, 'target_x', low16(frame.choice))",
                             'returns': None,
                             'signature': 'memory, frame, entry, once_token, append_token, scales'},
 '_calendar_swap_fields': {'flow': 'return _calendar_move_fields(memory, frame, carrier, swap_words(_calendar_value_fields(frame, '
                                   'carrier)), 4)',
                           'returns': None,
                           'signature': 'memory, frame, carrier'},
 '_calendar_test_fields': {'flow': 'from .business_services import _scene_refresh_flags\n'
                                   'return _scene_refresh_flags(memory, frame, value, width)',
                           'returns': None,
                           'signature': 'memory, frame, value, width=2'},
 '_calendar_value_fields': {'flow': 'value = frame.carrier(carrier)\n'
                                    'if value is None:\n'
                                    '    raise SceneRefreshBoundary(92986, frame, None)\n'
                                    'return value',
                            'returns': 'int',
                            'signature': 'frame: FirstDeploymentFrame, carrier: str'},
 '_calendar_write_fields': {'flow': 'from .business_services import _scene_refresh_emit\n'
                                    'if clear:\n'
                                    '    memory.state.read(address, width)\n'
                                    'return _scene_refresh_emit(memory, frame, address, width, value)',
                            'returns': None,
                            'signature': 'memory, frame, address, value, width=2, clear=False'},
 'append_queue': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (city, incoming_owner), (), ())\n'
                          'actual = append_queue_fields(memory, entered)\n'
                          'return low16(actual.target_x)',
                  'returns': 'Word',
                  'signature': 'state: GameplayState, city: Word, incoming_owner: Word'},
 'append_queue_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 94246)\n'
                                 'frame = first_replace(frame, roster=memory.cursor_at(4294964264))\n'
                                 "frame = _calendar_move_fields(memory, frame, 'target_x', frame.roster.byte(low16(frame.choice)), 1)\n"
                                 'if not frame.status & 8:\n'
                                 '    for address in (4294964858, 4294964860, 4294964862):\n'
                                 '        frame = _calendar_compare_fields(memory, frame, low16(frame.target_x), '
                                 'memory.state.read(address, 2))\n'
                                 '        if frame.status & 4:\n'
                                 '            frame = _calendar_write_fields(memory, frame, 4294956104, 0)\n'
                                 '            break\n'
                                 'frame = first_replace(frame, roster=memory.cursor_at(4294956064))\n'
                                 'while True:\n'
                                 '    frame = _calendar_compare_fields(memory, frame, frame.roster.byte(), 255, 1)\n'
                                 '    frame = first_replace(frame, roster=frame.roster.advance(1))\n'
                                 '    if frame.status & 4:\n'
                                 '        break\n'
                                 'frame = first_replace(frame, roster=frame.roster.advance(-1))\n'
                                 'frame = _calendar_test_fields(memory, frame, frame.roster.byte(), 1)\n'
                                 'return _calendar_write_fields(memory, frame, frame.roster.base, low8(frame.choice), 1)',
                         'returns': 'FirstDeploymentFrame',
                         'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'commit_income': {'flow': "memory, entered = _calendar_legacy_entry_fields(state, (city, offset, factor), (), (('scan', ledger),))\n"
                           'actual = commit_income_fields(memory, entered)',
                   'returns': None,
                   'signature': 'state: GameplayState, city: Word, offset: Word, factor: Word, ledger: Table'},
 'commit_income_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 93276)\n'
                                  'frame = _calendar_call_fields(memory, frame, 93298, 93280)\n'
                                  "frame = _calendar_arithmetic_fields(memory, frame, 'count', frame.scan.long(low16(frame.target_y)), 4)\n"
                                  'if frame.status & 1:\n'
                                  "    frame = _calendar_move_fields(memory, frame, 'count', 4294967295, 4)\n"
                                  'frame = _calendar_write_fields(memory, frame, frame.scan.address(low16(frame.target_y)), frame.count, '
                                  '4)\n'
                                  'return _calendar_call_fields(memory, frame, 93336, 93296)',
                          'returns': 'FirstDeploymentFrame',
                          'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'credit_primary': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (city,), (), ())\n'
                            'actual = credit_primary_fields(memory, entered)',
                    'returns': None,
                    'signature': 'state: GameplayState, city: Word'},
 'credit_primary_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 93228)\n'
                                   'frame = first_replace(frame, roster=memory.cursor_at(4294959744), scan=memory.cursor_at(4294959104))\n'
                                   "frame = _calendar_move_fields(memory, frame, 'target_y', low16(frame.target_x))\n"
                                   "frame = _calendar_shift_fields(memory, frame, 'target_y', 2)\n"
                                   "frame = _calendar_move_fields(memory, frame, 'choice', 100)\n"
                                   "frame = _calendar_arithmetic_fields(memory, frame, 'choice', frame.roster.word(low16(frame.target_y), "
                                   '2), subtract=True)\n'
                                   'return _calendar_call_fields(memory, frame, 93276, 93252)',
                           'returns': 'FirstDeploymentFrame',
                           'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'credit_secondary': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (city,), (), ())\n'
                              'actual = credit_secondary_fields(memory, entered)',
                      'returns': None,
                      'signature': 'state: GameplayState, city: Word'},
 'credit_secondary_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 93254)\n'
                                     'frame = first_replace(frame, roster=memory.cursor_at(4294959744))\n'
                                     "frame = _calendar_move_fields(memory, frame, 'target_y', low16(frame.target_x))\n"
                                     "frame = _calendar_shift_fields(memory, frame, 'target_y', 2)\n"
                                     "frame = _calendar_move_fields(memory, frame, 'choice', frame.roster.long(low16(frame.target_y)), 4)\n"
                                     'frame = first_replace(frame, scan=memory.cursor_at(4294959264))\n'
                                     'return _calendar_call_fields(memory, frame, 93276, 93274)',
                             'returns': 'FirstDeploymentFrame',
                             'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'debit_primary': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (city,), (), ())\n'
                           'actual = debit_primary_fields(memory, entered)',
                   'returns': None,
                   'signature': 'state: GameplayState, city: Word'},
 'debit_primary_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 93456)\n'
                                  'frame = first_replace(frame, scan=memory.cursor_at(4294959744))\n'
                                  "frame = _calendar_move_fields(memory, frame, 'choice', 100)\n"
                                  "frame = _calendar_move_fields(memory, frame, 'count', low16(frame.target_x))\n"
                                  "frame = _calendar_shift_fields(memory, frame, 'count', 2)\n"
                                  "frame = _calendar_arithmetic_fields(memory, frame, 'choice', frame.scan.word(low16(frame.count), 2), "
                                  'subtract=True)\n'
                                  'frame = first_replace(frame, scratch=memory.cursor_at(4294959104))\n'
                                  'return _calendar_call_fields(memory, frame, 93504, 93480)',
                          'returns': 'FirstDeploymentFrame',
                          'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'debit_secondary': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (city,), (), ())\n'
                             'actual = debit_secondary_fields(memory, entered)',
                     'returns': None,
                     'signature': 'state: GameplayState, city: Word'},
 'debit_secondary_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 93482)\n'
                                    'frame = first_replace(frame, scan=memory.cursor_at(4294959744))\n'
                                    "frame = _calendar_move_fields(memory, frame, 'target_y', low16(frame.target_x))\n"
                                    "frame = _calendar_shift_fields(memory, frame, 'target_y', 2)\n"
                                    "frame = _calendar_move_fields(memory, frame, 'choice', frame.scan.word(low16(frame.target_y), 2))\n"
                                    'frame = first_replace(frame, scratch=memory.cursor_at(4294959264))\n'
                                    'return _calendar_call_fields(memory, frame, 93504, 93502)',
                            'returns': 'FirstDeploymentFrame',
                            'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'deplete_income': {'flow': "memory, entered = _calendar_legacy_entry_fields(state, (city,), (), (('candidates', thresholds),))\n"
                            'actual = deplete_income_fields(memory, entered)',
                    'returns': None,
                    'signature': 'state: GameplayState, city: Word, thresholds: Table'},
 'deplete_income_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 93336)\n'
                                   "frame = _calendar_move_fields(memory, frame, 'target_y', low16(frame.target_x))\n"
                                   "frame = _calendar_shift_fields(memory, frame, 'target_y', 2)\n"
                                   "frame = _calendar_move_fields(memory, frame, 'unit', frame.controller.long(low16(frame.target_y)), 4)\n"
                                   "frame = _calendar_move_fields(memory, frame, 'count', 0)\n"
                                   'frame = _calendar_compare_fields(memory, frame, low16(frame.unit), 45)\n'
                                   'if frame.status & (1 | 4):\n'
                                   '    return frame\n'
                                   'for threshold in (55, 65, 75, 85):\n'
                                   '    frame = _calendar_compare_fields(memory, frame, low16(frame.unit), threshold)\n'
                                   '    if frame.status & (1 | 4):\n'
                                   '        break\n'
                                   "    frame = _calendar_arithmetic_fields(memory, frame, 'count', 4)\n"
                                   "frame = _calendar_move_fields(memory, frame, 'unit', low16(frame.target_x))\n"
                                   'frame = _calendar_call_fields(memory, frame, 33748, 93392)\n'
                                   "frame = _calendar_move_fields(memory, frame, 'target_x', low16(frame.unit))\n"
                                   'frame = first_replace(frame, candidates=memory.cursor_at(93436))\n'
                                   "frame = _calendar_move_fields(memory, frame, 'unit', frame.candidates.word(low16(frame.count)))\n"
                                   "frame = _movement_multiply_word(memory.state, frame, 'unit', memory.state.read(4294964764, 2))\n"
                                   "frame = _calendar_swap_fields(memory, frame, 'unit')\n"
                                   "frame = _calendar_arithmetic_fields(memory, frame, 'unit', frame.candidates.word(low16(frame.count), "
                                   '2))\n'
                                   'frame = first_replace(frame, controller=memory.cursor_at(4294959904))\n'
                                   "frame = _calendar_move_fields(memory, frame, 'target_y', low16(frame.target_x))\n"
                                   "frame = _calendar_shift_fields(memory, frame, 'target_y', 2)\n"
                                   "frame = _calendar_move_fields(memory, frame, 'count', frame.controller.word(low16(frame.target_y), "
                                   '2))\n'
                                   "frame = _movement_multiply_word(memory.state, frame, 'count', low16(frame.unit))\n"
                                   "frame = _calendar_divu_fields(memory, frame, 'count', 100, 93426)\n"
                                   'return _calendar_memory_arithmetic_fields(memory, frame, '
                                   'frame.controller.address(low16(frame.target_y), 2), low16(frame.count), subtract=True)',
                           'returns': 'FirstDeploymentFrame',
                           'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'divide_percent': {'flow': "memory, entered = _calendar_legacy_entry_fields(state, (), (('unit', product),), ())\n"
                            'actual = divide_percent_fields(memory, entered)\n'
                            'return actual.unit',
                    'returns': 'Long',
                    'signature': 'state: GameplayState, product: Long'},
 'divide_percent_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 95724)\n'
                                   "frame = _calendar_save_fields(memory, frame, ('target_y',))\n"
                                   "frame = _calendar_move_fields(memory, frame, 'target_y', frame.unit, 4)\n"
                                   "frame = _calendar_move_fields(memory, frame, 'unit', 100, 4)\n"
                                   'frame = _calendar_call_fields(memory, frame, 218976, 95738)\n'
                                   "frame = _calendar_move_fields(memory, frame, 'unit', frame.target_y, 4)\n"
                                   "return _calendar_restore_fields(memory, frame, ('target_y',))",
                           'returns': 'FirstDeploymentFrame',
                           'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'grow_original_long_field': {'flow': "memory, entered = _calendar_legacy_entry_fields(state, (), (), (('roster', target),))\n"
                                      'actual = grow_original_long_field_fields(memory, entered)\n'
                                      'return actual.target_y',
                              'returns': 'Long',
                              'signature': 'state: GameplayState, target: Table'},
 'grow_original_long_field_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 93194)\n'
                                             "frame = _calendar_move_fields(memory, frame, 'target_y', frame.roster.long(), 4)\n"
                                             "frame = _calendar_move_fields(memory, frame, 'unit', frame.target_y, 4)\n"
                                             "frame = _calendar_divu_fields(memory, frame, 'unit', 100, 93198, True)\n"
                                             "frame = _calendar_move_fields(memory, frame, 'unit', frame.unit & 65535, 4)\n"
                                             "frame = _calendar_arithmetic_fields(memory, frame, 'target_y', frame.unit, 4)\n"
                                             'frame = _calendar_compare_fields(memory, frame, frame.target_y, 1000, 4)\n'
                                             'if not frame.status & 1 and (not frame.status & 4):\n'
                                             "    frame = _calendar_move_fields(memory, frame, 'target_y', 1000, 4)\n"
                                             'return _calendar_write_fields(memory, frame, frame.roster.base, frame.target_y, 4)',
                                     'returns': 'FirstDeploymentFrame',
                                     'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'replenish_b200_troops': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (retained_city,), (), ())\n'
                                   'actual = replenish_b200_troops_fields(memory, entered)\n'
                                   'return low16(actual.target_x)',
                           'returns': 'Word',
                           'signature': 'state: GameplayState, retained_city: Word'},
 'replenish_b200_troops_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 93112)\n'
                                          'frame = first_replace(frame, roster=memory.cursor_at(4294961719), '
                                          'candidates=memory.cursor_at(4294953984), controller=memory.cursor_at(4294946816), '
                                          'scan=memory.cursor_at(4294947328))\n'
                                          "frame = _calendar_move_fields(memory, frame, 'target_x', 255)\n"
                                          'while True:\n'
                                          "    frame = _calendar_move_fields(memory, frame, 'target_y', "
                                          'frame.candidates.byte(low16(frame.target_x)), 1)\n'
                                          '    frame = _calendar_compare_fields(memory, frame, low16(frame.target_y), 40)\n'
                                          '    if not frame.status & 1 and (not frame.status & 4):\n'
                                          '        pass\n'
                                          '    else:\n'
                                          '        frame = _calendar_test_fields(memory, frame, frame.roster.byte(low16(frame.target_y)), '
                                          '1)\n'
                                          '        if frame.status & 4:\n'
                                          "            frame = _calendar_move_fields(memory, frame, 'target_y', low16(frame.target_x))\n"
                                          "            frame = _calendar_shift_fields(memory, frame, 'target_y', 1)\n"
                                          "            frame = _calendar_move_fields(memory, frame, 'unit', "
                                          'frame.controller.word(low16(frame.target_y)))\n'
                                          "            frame = _calendar_move_fields(memory, frame, 'count', low16(frame.unit))\n"
                                          "            frame = _movement_multiply_word(memory.state, frame, 'unit', 15)\n"
                                          "            frame = _calendar_divu_fields(memory, frame, 'unit', 100, 93166)\n"
                                          "            frame = _calendar_move_fields(memory, frame, 'distance', "
                                          'frame.scan.word(low16(frame.target_y)))\n'
                                          "            frame = _calendar_arithmetic_fields(memory, frame, 'distance', low16(frame.unit))\n"
                                          '            frame = _calendar_compare_fields(memory, frame, low16(frame.distance), '
                                          'low16(frame.count))\n'
                                          '            if not frame.status & 1 and (not frame.status & 4):\n'
                                          "                frame = _calendar_move_fields(memory, frame, 'distance', low16(frame.count))\n"
                                          '            frame = _calendar_write_fields(memory, frame, '
                                          'frame.scan.address(low16(frame.target_y)), low16(frame.distance))\n'
                                          "    frame, again = _calendar_db_fields(frame, 'target_x')\n"
                                          '    if not again:\n'
                                          '        return frame',
                                  'returns': 'FirstDeploymentFrame',
                                  'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'reset_queue': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (), (), ())\nactual = reset_queue_fields(memory, entered)',
                 'returns': 'None',
                 'signature': 'state: GameplayState'},
 'reset_queue_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 94230)\n'
                                "frame = _calendar_move_fields(memory, frame, 'target_x', 41, 4)\n"
                                'frame = first_replace(frame, roster=memory.cursor_at(4294956064))\n'
                                'while True:\n'
                                '    frame = _calendar_write_fields(memory, frame, frame.roster.base, 255, 1)\n'
                                '    frame = first_replace(frame, roster=frame.roster.advance(1))\n'
                                "    frame, again = _calendar_db_fields(frame, 'target_x')\n"
                                '    if not again:\n'
                                '        return frame',
                        'returns': 'FirstDeploymentFrame',
                        'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'sample_once': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (), (), ())\n'
                         'actual = sample_once_fields(memory, entered)\n'
                         'return low16(actual.target_x)',
                 'returns': 'Word',
                 'signature': 'state: GameplayState'},
 'sample_once_fields': {'flow': 'return _calendar_sample_fields(memory, frame, 95640, 95650)',
                        'returns': 'FirstDeploymentFrame',
                        'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'sample_small': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (), (), ())\n'
                          'actual = sample_small_fields(memory, entered)\n'
                          'return low16(actual.target_x)',
                  'returns': 'Word',
                  'signature': 'state: GameplayState'},
 'sample_small_fields': {'flow': 'return _calendar_sample_fields(memory, frame, 95656, 95666, 7, 5)',
                         'returns': 'FirstDeploymentFrame',
                         'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'sample_wide': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (), (), ())\n'
                         'actual = sample_wide_fields(memory, entered)\n'
                         'return low16(actual.target_x)',
                 'returns': 'Word',
                 'signature': 'state: GameplayState'},
 'sample_wide_fields': {'flow': 'return _calendar_sample_fields(memory, frame, 95682, 95692, 15, 10)',
                        'returns': 'FirstDeploymentFrame',
                        'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'scale_e000': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (offset, factor), (), ())\n'
                        'actual = scale_e000_fields(memory, entered)\n'
                        'return actual.unit',
                'returns': 'Long',
                'signature': 'state: GameplayState, offset: Word, factor: Word'},
 'scale_e000_fields': {'flow': 'return _calendar_scale_fields(memory, frame, 95574, 4294959104, 95586, 95590)',
                       'returns': 'FirstDeploymentFrame',
                       'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'scale_e0a0': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (offset, factor), (), ())\n'
                        'actual = scale_e0a0_fields(memory, entered)\n'
                        'return actual.unit',
                'returns': 'Long',
                'signature': 'state: GameplayState, offset: Word, factor: Word'},
 'scale_e0a0_fields': {'flow': 'return _calendar_scale_fields(memory, frame, 95596, 4294959264, 95608, 95612)',
                       'returns': 'FirstDeploymentFrame',
                       'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'scale_e140': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (offset, factor), (), ())\n'
                        'actual = scale_e140_fields(memory, entered)\n'
                        'return actual.unit',
                'returns': 'Long',
                'signature': 'state: GameplayState, offset: Word, factor: Word'},
 'scale_e140_fields': {'flow': 'return _calendar_scale_fields(memory, frame, 95530, 4294959424, 95542, 95546)',
                       'returns': 'FirstDeploymentFrame',
                       'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'scale_e1e0': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (offset, factor), (), ())\n'
                        'actual = scale_e1e0_fields(memory, entered)\n'
                        'return actual.unit',
                'returns': 'Long',
                'signature': 'state: GameplayState, offset: Word, factor: Word'},
 'scale_e1e0_fields': {'flow': 'return _calendar_scale_fields(memory, frame, 95508, 4294959584, 95520, 95524)',
                       'returns': 'FirstDeploymentFrame',
                       'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'scale_e320': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (offset, factor), (), ())\n'
                        'actual = scale_e320_fields(memory, entered)\n'
                        'return actual.unit',
                'returns': 'Long',
                'signature': 'state: GameplayState, offset: Word, factor: Word'},
 'scale_e320_fields': {'flow': 'return _calendar_scale_fields(memory, frame, 95552, 4294959904, 95564, 95568)',
                       'returns': 'FirstDeploymentFrame',
                       'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'scale_e5a0': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (offset, factor), (), ())\n'
                        'actual = scale_e5a0_fields(memory, entered)\n'
                        'return actual.unit',
                'returns': 'Long',
                'signature': 'state: GameplayState, offset: Word, factor: Word'},
 'scale_e5a0_fields': {'flow': 'return _calendar_scale_fields(memory, frame, 95618, 4294960544, 95630, 95634)',
                       'returns': 'FirstDeploymentFrame',
                       'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'scaled_income': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (offset, factor), (), ())\n'
                           'actual = scaled_income_fields(memory, entered)',
                   'returns': None,
                   'signature': 'state: GameplayState, offset: Word, factor: Word'},
 'scaled_income_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 93298)\n'
                                  'frame = first_replace(frame, candidates=memory.cursor_at(4294959584), '
                                  'controller=memory.cursor_at(4294960064), scratch=memory.cursor_at(4294959424))\n'
                                  "frame = _movement_multiply_word(memory.state, frame, 'choice', "
                                  'frame.controller.word(low16(frame.target_y), 2))\n'
                                  "frame = _movement_multiply_word(memory.state, frame, 'choice', "
                                  'frame.candidates.word(low16(frame.target_y), 2))\n'
                                  "frame = _calendar_divu_fields(memory, frame, 'choice', 15000, 93318, True)\n"
                                  "frame = _calendar_move_fields(memory, frame, 'count', frame.scratch.long(low16(frame.target_y)), 4)\n"
                                  "frame = _calendar_move_fields(memory, frame, 'count', frame.count & 65535, 4)\n"
                                  "return _movement_multiply_word(memory.state, frame, 'count', low16(frame.choice))",
                          'returns': 'FirstDeploymentFrame',
                          'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'settle_expense': {'flow': "memory, entered = _calendar_legacy_entry_fields(state, (city, factor), (), (('scratch', ledger),))\n"
                            'actual = settle_expense_fields(memory, entered)',
                    'returns': None,
                    'signature': 'state: GameplayState, city: Word, factor: Word, ledger: Table'},
 'settle_expense_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 93504)\n'
                                   'frame = first_replace(frame, opponent=memory.cursor_at(4294952704))\n'
                                   "frame = _calendar_arithmetic_fields(memory, frame, 'target_x', 1)\n"
                                   'frame = _calendar_write_fields(memory, frame, 4294964784, 65535)\n'
                                   'frame = _calendar_call_fields(memory, frame, 24392, 93522)\n'
                                   'frame = _calendar_write_fields(memory, frame, 4294964790, low16(frame.count))\n'
                                   "frame = _calendar_arithmetic_fields(memory, frame, 'target_x', 1, subtract=True)\n"
                                   'frame = first_replace(frame, roster=memory.cursor_at(4294952960), '
                                   'candidates=memory.cursor_at(4294964480))\n'
                                   "frame = _calendar_move_fields(memory, frame, 'target_y', 0, 4)\n"
                                   'while True:\n'
                                   "    frame = _calendar_move_fields(memory, frame, 'unit', frame.candidates.word())\n"
                                   '    frame = first_replace(frame, candidates=frame.candidates.advance(2))\n'
                                   '    if frame.status & 8:\n'
                                   '        break\n'
                                   "    frame = _calendar_shift_fields(memory, frame, 'unit', 2)\n"
                                   "    frame = _calendar_arithmetic_fields(memory, frame, 'target_y', "
                                   'frame.roster.long(low16(frame.unit)), 4)\n'
                                   "frame = _calendar_move_fields(memory, frame, 'count', frame.target_y, 4)\n"
                                   "frame = _movement_multiply_word(memory.state, frame, 'target_y', low16(frame.choice))\n"
                                   "frame = _calendar_swap_fields(memory, frame, 'count')\n"
                                   "frame = _movement_multiply_word(memory.state, frame, 'count', low16(frame.choice))\n"
                                   "frame = _calendar_swap_fields(memory, frame, 'count')\n"
                                   "frame = _calendar_arithmetic_fields(memory, frame, 'target_y', frame.count, 4)\n"
                                   "frame = _calendar_divu_fields(memory, frame, 'target_y', 5000, 93562, True)\n"
                                   'frame = first_replace(frame, roster=memory.cursor_at(4294964480), candidates=memory.cursor_at(93664))\n'
                                   "frame = _calendar_move_fields(memory, frame, 'unit', 0)\n"
                                   'while True:\n'
                                   "    frame = _calendar_move_fields(memory, frame, 'count', frame.roster.word())\n"
                                   '    frame = first_replace(frame, roster=frame.roster.advance(2))\n'
                                   '    if frame.status & 8:\n'
                                   '        break\n'
                                   "    frame = _calendar_move_fields(memory, frame, 'distance', frame.opponent.byte(low16(frame.count)), "
                                   '1)\n'
                                   "    frame = _calendar_move_fields(memory, frame, 'distance', low16(frame.distance) & 5)\n"
                                   "    frame = _calendar_shift_fields(memory, frame, 'distance', 1)\n"
                                   "    frame = _calendar_arithmetic_fields(memory, frame, 'unit', "
                                   'frame.candidates.word(low16(frame.distance)))\n'
                                   "frame = _movement_multiply_word(memory.state, frame, 'unit', low16(frame.choice))\n"
                                   "frame = _calendar_divu_fields(memory, frame, 'unit', 100, 93600, True)\n"
                                   "frame = _calendar_move_fields(memory, frame, 'target_y', frame.target_y & 65535, 4)\n"
                                   "frame = _calendar_move_fields(memory, frame, 'unit', frame.unit & 65535, 4)\n"
                                   "frame = _calendar_arithmetic_fields(memory, frame, 'unit', frame.target_y, 4)\n"
                                   "frame = _calendar_move_fields(memory, frame, 'count', low16(frame.target_x))\n"
                                   "frame = _calendar_shift_fields(memory, frame, 'count', 2)\n"
                                   "frame = _calendar_move_fields(memory, frame, 'distance', frame.scratch.long(low16(frame.count)), 4)\n"
                                   "frame = _calendar_arithmetic_fields(memory, frame, 'distance', frame.unit, 4, True)\n"
                                   'if frame.status & 1:\n'
                                   '    frame = _calendar_call_fields(memory, frame, 93674, 93636)\n'
                                   "    frame = _calendar_move_fields(memory, frame, 'distance', 0, 4)\n"
                                   'else:\n'
                                   '    frame = _calendar_compare_fields(memory, frame, frame.distance, 999999, 4)\n'
                                   '    if not frame.status & (1 | 4):\n'
                                   "        frame = _calendar_move_fields(memory, frame, 'distance', 999999, 4)\n"
                                   "frame = _calendar_move_fields(memory, frame, 'count', low16(frame.target_x))\n"
                                   "frame = _calendar_shift_fields(memory, frame, 'count', 2)\n"
                                   'return _calendar_write_fields(memory, frame, frame.scratch.address(low16(frame.count)), '
                                   'frame.distance, 4)',
                           'returns': 'FirstDeploymentFrame',
                           'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'settle_shortage': {'flow': "memory, entered = _calendar_legacy_entry_fields(state, (factor,), (('distance', outstanding),), ())\n"
                             'actual = settle_shortage_fields(memory, entered)',
                     'returns': None,
                     'signature': 'state: GameplayState, outstanding: Long, factor: Word'},
 'settle_shortage_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 93674)\n'
                                    'previous = frame.distance\n'
                                    'frame, value = _movement_binary_flags(memory.state, frame, 0, previous, 32, True)\n'
                                    'frame = first_replace(frame, distance=value)\n'
                                    "frame = _calendar_move_fields(memory, frame, 'offset_x', frame.distance, 4)\n"
                                    "frame = _movement_multiply_word(memory.state, frame, 'distance', low16(frame.choice))\n"
                                    "frame = _calendar_swap_fields(memory, frame, 'offset_x')\n"
                                    "frame = _movement_multiply_word(memory.state, frame, 'offset_x', low16(frame.choice))\n"
                                    "frame = _calendar_swap_fields(memory, frame, 'offset_x')\n"
                                    "frame = _calendar_arithmetic_fields(memory, frame, 'distance', frame.offset_x, 4)\n"
                                    'frame = first_replace(frame, roster=memory.cursor_at(4294964480), '
                                    'candidates=memory.cursor_at(4294961760), controller=memory.cursor_at(4294950400), '
                                    'scan=memory.cursor_at(4294950912))\n'
                                    'while True:\n'
                                    "    frame = _calendar_move_fields(memory, frame, 'target_y', frame.roster.word())\n"
                                    '    frame = first_replace(frame, roster=frame.roster.advance(2))\n'
                                    '    if frame.status & 8:\n'
                                    '        break\n'
                                    "    frame = _calendar_move_fields(memory, frame, 'unit', 0, 4)\n"
                                    "    frame = _calendar_shift_fields(memory, frame, 'target_y', 1)\n"
                                    "    frame = _calendar_move_fields(memory, frame, 'unit', "
                                    'frame.controller.word(low16(frame.target_y)))\n'
                                    "    frame = _calendar_move_fields(memory, frame, 'count', 0, 4)\n"
                                    "    frame = _calendar_move_fields(memory, frame, 'count', frame.scan.word(low16(frame.target_y)))\n"
                                    "    frame = _calendar_arithmetic_fields(memory, frame, 'count', frame.unit, 4)\n"
                                    '    frame = _calendar_write_fields(memory, frame, frame.candidates.base, frame.count, 4)\n'
                                    '    frame = first_replace(frame, candidates=frame.candidates.advance(4))\n'
                                    'frame = first_replace(frame, roster=memory.cursor_at(4294961760), '
                                    'candidates=memory.cursor_at(4294964480))\n'
                                    "frame = _calendar_move_fields(memory, frame, 'target_y', memory.state.read(4294964790, 2))\n"
                                    'frame = _calendar_compare_fields(memory, frame, low16(frame.target_y), 1)\n'
                                    'if not frame.status & (1 | 4):\n'
                                    "    frame = _calendar_arithmetic_fields(memory, frame, 'target_y', 1, subtract=True)\n"
                                    '    while True:\n'
                                    "        for carrier in ('unit', 'count', 'offset_x'):\n"
                                    '            frame = _calendar_move_fields(memory, frame, carrier, 0)\n'
                                    '        while True:\n'
                                    "            frame = _calendar_move_fields(memory, frame, 'offset_y', "
                                    'frame.roster.long(low16(frame.offset_x)), 4)\n'
                                    '            frame = _calendar_compare_fields(memory, frame, frame.offset_y, '
                                    'frame.roster.long(low16(frame.offset_x), 4), 4)\n'
                                    '            if not frame.status & (1 | 4):\n'
                                    '                frame = _calendar_write_fields(memory, frame, '
                                    'frame.roster.address(low16(frame.offset_x)), frame.roster.long(low16(frame.offset_x), 4), 4)\n'
                                    '                frame = _calendar_write_fields(memory, frame, '
                                    'frame.roster.address(low16(frame.offset_x), 4), frame.offset_y, 4)\n'
                                    "                frame = _calendar_move_fields(memory, frame, 'offset_y', "
                                    'frame.candidates.word(low16(frame.count)))\n'
                                    '                frame = _calendar_write_fields(memory, frame, '
                                    'frame.candidates.address(low16(frame.count)), frame.candidates.word(low16(frame.count), 2))\n'
                                    '                frame = _calendar_write_fields(memory, frame, '
                                    'frame.candidates.address(low16(frame.count), 2), low16(frame.offset_y))\n'
                                    "            frame = _calendar_arithmetic_fields(memory, frame, 'unit', 1)\n"
                                    "            frame = _calendar_arithmetic_fields(memory, frame, 'count', 2)\n"
                                    "            frame = _calendar_arithmetic_fields(memory, frame, 'offset_x', 4)\n"
                                    '            frame = _calendar_compare_fields(memory, frame, low16(frame.unit), '
                                    'low16(frame.target_y))\n'
                                    '            if not frame.status & 1:\n'
                                    '                break\n'
                                    "        frame = _calendar_arithmetic_fields(memory, frame, 'target_y', 1, subtract=True)\n"
                                    '        if frame.status & 4:\n'
                                    '            break\n'
                                    'frame = first_replace(frame, roster=memory.cursor_at(4294964480), '
                                    'candidates=memory.cursor_at(4294952960), controller=memory.cursor_at(4294951424))\n'
                                    'while True:\n'
                                    "    frame = _calendar_move_fields(memory, frame, 'target_y', frame.roster.word())\n"
                                    '    frame = first_replace(frame, roster=frame.roster.advance(2))\n'
                                    '    if frame.status & 8:\n'
                                    '        break\n'
                                    "    frame = _calendar_move_fields(memory, frame, 'count', low16(frame.target_y))\n"
                                    "    frame = _calendar_shift_fields(memory, frame, 'count', 2)\n"
                                    "    frame = _calendar_move_fields(memory, frame, 'unit', frame.candidates.long(low16(frame.count)), "
                                    '4)\n'
                                    '    frame = _calendar_compare_fields(memory, frame, frame.unit, frame.distance, 4)\n'
                                    '    if not frame.status & (1 | 4):\n'
                                    "        frame = _calendar_move_fields(memory, frame, 'offset_y', frame.distance, 4)\n"
                                    "        frame = _calendar_move_fields(memory, frame, 'distance', 0)\n"
                                    '    else:\n'
                                    "        frame = _calendar_arithmetic_fields(memory, frame, 'distance', frame.unit, 4, True)\n"
                                    "        frame = _calendar_move_fields(memory, frame, 'offset_y', frame.unit, 4)\n"
                                    "    frame = _calendar_move_fields(memory, frame, 'offset_x', 100)\n"
                                    "    frame = _calendar_arithmetic_fields(memory, frame, 'offset_x', "
                                    'frame.controller.byte(low16(frame.target_y)), 1, True)\n'
                                    "    frame = _movement_multiply_word(memory.state, frame, 'offset_y', low16(frame.offset_x))\n"
                                    "    frame = _calendar_divu_fields(memory, frame, 'offset_y', 100, 93850, True)\n"
                                    "    frame = _calendar_move_fields(memory, frame, 'offset_y', frame.offset_y & 65535, 4)\n"
                                    "    frame = _calendar_arithmetic_fields(memory, frame, 'unit', frame.offset_y, 4, True)\n"
                                    '    frame = _calendar_write_fields(memory, frame, frame.candidates.address(low16(frame.count)), '
                                    'frame.unit, 4)\n'
                                    '    frame = _calendar_test_fields(memory, frame, frame.distance, 4)\n'
                                    '    if frame.status & 4:\n'
                                    '        break\n'
                                    'frame = _calendar_test_fields(memory, frame, frame.distance, 4)\n'
                                    'if frame.status & 4:\n'
                                    '    return frame\n'
                                    'frame = first_replace(frame, roster=memory.cursor_at(4294964480), '
                                    'candidates=memory.cursor_at(4294951424), controller=memory.cursor_at(4294951680))\n'
                                    'while True:\n'
                                    "    frame = _calendar_move_fields(memory, frame, 'target_y', frame.roster.word())\n"
                                    '    frame = first_replace(frame, roster=frame.roster.advance(2))\n'
                                    '    if frame.status & 8:\n'
                                    '        return frame\n'
                                    "    frame = _calendar_move_fields(memory, frame, 'unit', 100, 4)\n"
                                    "    frame = _calendar_arithmetic_fields(memory, frame, 'unit', "
                                    'frame.candidates.byte(low16(frame.target_y)), 1, True)\n'
                                    "    frame = _calendar_divu_fields(memory, frame, 'unit', 10, 93896)\n"
                                    '    frame = _calendar_memory_arithmetic_fields(memory, frame, '
                                    'frame.controller.address(low16(frame.target_y)), low8(frame.unit), 1, True)\n'
                                    '    if frame.status & 1:\n'
                                    '        frame = _calendar_write_fields(memory, frame, '
                                    'frame.controller.address(low16(frame.target_y)), 0, 1, True)',
                            'returns': 'FirstDeploymentFrame',
                            'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'submit_calendar_classified_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 95348)\n'
                                               "frame = _calendar_move_fields(memory, frame, 'choice', low16(frame.target_x))\n"
                                               "frame = _calendar_shift_fields(memory, frame, 'target_x', 2, arithmetic=True)\n"
                                               'frame = first_replace(frame, roster=memory.cursor_at(4294959904))\n'
                                               "frame = _calendar_move_fields(memory, frame, 'count', 0, 4)\n"
                                               "frame = _calendar_move_fields(memory, frame, 'unit', "
                                               'frame.roster.long(low16(frame.target_x)), 4)\n'
                                               "frame = _calendar_divu_fields(memory, frame, 'unit', 10, 95362, True)\n"
                                               "frame = _calendar_move_fields(memory, frame, 'count', memory.state.read(95472 + "
                                               's16(low16(frame.unit)), 1), 1)\n'
                                               'frame = _calendar_compare_fields(memory, frame, low16(frame.unit), 7)\n'
                                               'if not frame.status & 1:\n'
                                               "    return _calendar_move_fields(memory, frame, 'target_x', low16(frame.choice))\n"
                                               'frame = _calendar_call_fields(memory, frame, 95640, 95382)\n'
                                               "frame = _calendar_move_fields(memory, frame, 'target_x', low16(frame.target_x) & "
                                               'low16(frame.count))\n'
                                               'if not frame.status & 4:\n'
                                               "    return _calendar_move_fields(memory, frame, 'target_x', low16(frame.choice))\n"
                                               'frame = _calendar_call_fields(memory, frame, 94246, 95394)\n'
                                               "frame = _calendar_save_fields(memory, frame, ('choice',))\n"
                                               "frame = _calendar_shift_fields(memory, frame, 'choice', 2, arithmetic=True)\n"
                                               "frame = _calendar_move_fields(memory, frame, 'count', 0, 4)\n"
                                               "frame = _calendar_move_fields(memory, frame, 'count', memory.state.read(95484 + "
                                               's16(low16(frame.unit)), 1), 1)\n'
                                               "frame = _calendar_move_fields(memory, frame, 'target_x', 0, 4)\n"
                                               'frame = _calendar_compare_fields(memory, frame, low16(frame.unit), 7)\n'
                                               'if frame.status & 1:\n'
                                               '    frame = _calendar_call_fields(memory, frame, 95682, 95418)\n'
                                               '    frame = _calendar_compare_fields(memory, frame, low16(frame.unit), 6)\n'
                                               '    if not frame.status & 1:\n'
                                               '        frame = _calendar_call_fields(memory, frame, 95656, 95430)\n'
                                               "frame = _calendar_arithmetic_fields(memory, frame, 'target_x', low16(frame.count))\n"
                                               'for target, token in ((95508, 95438), (95574, 95442), (95596, 95446), (95618, 95450)):\n'
                                               '    frame = _calendar_call_fields(memory, frame, target, token)\n'
                                               'frame = _calendar_call_fields(memory, frame, 95656, 95454)\n'
                                               "frame = _calendar_arithmetic_fields(memory, frame, 'target_x', 95)\n"
                                               'frame = _calendar_call_fields(memory, frame, 95530, 95464)\n'
                                               "frame = _calendar_restore_fields(memory, frame, ('choice',))\n"
                                               "return _calendar_move_fields(memory, frame, 'target_x', low16(frame.choice))",
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'submit_calendar_four_fields': {'flow': 'return _calendar_submit_fields(memory, frame, 95042, 95058, 95072, ((95682, 95082, 80, 95508, '
                                         '95092), (95656, 95096, 95, 95530, 95106), (95682, 95110, 85, 95552, 95120), (95682, 95124, 80, '
                                         '95574, 95134)))',
                                 'returns': 'FirstDeploymentFrame',
                                 'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'submit_calendar_three_fields': {'flow': 'return _calendar_submit_fields(memory, frame, 94630, 94646, 94660, ((95682, 94670, 80, 95508, '
                                          '94680), (95656, 94684, 95, 95530, 94694), (95682, 94698, 85, 95552, 94708)))',
                                  'returns': 'FirstDeploymentFrame',
                                  'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'submit_classified_fields': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (city,), (), ())\n'
                                      'actual = submit_calendar_classified_fields(memory, entered)\n'
                                      'return low16(actual.target_x)',
                              'returns': 'Word',
                              'signature': 'state: GameplayState, city: Word'},
 'submit_four_fields': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (city, incoming_owner), (), ())\n'
                                'actual = submit_calendar_four_fields(memory, entered)\n'
                                'return EventSubmission(low16(actual.target_x), low16(actual.choice))',
                        'returns': 'EventSubmission',
                        'signature': 'state: GameplayState, city: Word, incoming_owner: Word'},
 'submit_three_fields': {'flow': 'memory, entered = _calendar_legacy_entry_fields(state, (city, incoming_owner), (), ())\n'
                                 'actual = submit_calendar_three_fields(memory, entered)\n'
                                 'return EventSubmission(low16(actual.target_x), low16(actual.choice))',
                         'returns': 'EventSubmission',
                         'signature': 'state: GameplayState, city: Word, incoming_owner: Word'},
 'wrapped_product': {'flow': 'return _calendar_product_terms(value, factor)[3]',
                     'returns': 'Long',
                     'signature': 'value: Long, factor: Word'},
 'wrapped_product_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 95708)\n'
                                    'lower, upper, shifted, result = _calendar_product_terms(frame.unit, low16(frame.target_x))\n'
                                    "frame = _calendar_move_fields(memory, frame, 'distance', frame.unit, 4)\n"
                                    "frame = _calendar_swap_fields(memory, frame, 'distance')\n"
                                    "frame = _calendar_move_fields(memory, frame, 'distance', upper, 4)\n"
                                    "frame = _calendar_swap_fields(memory, frame, 'distance')\n"
                                    "frame = _calendar_move_fields(memory, frame, 'distance', 0)\n"
                                    "frame = _calendar_move_fields(memory, frame, 'unit', lower, 4)\n"
                                    "frame = _calendar_arithmetic_fields(memory, frame, 'unit', shifted, 4)\n"
                                    'return first_replace(frame, unit=result)',
                            'returns': 'FirstDeploymentFrame',
                            'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'}})
