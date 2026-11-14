"""Draft restricted reuse semantic AST admission and ordinary target emission.

Business rules remain separate. Generation reads explicit source text only.
Not an arbitrary Python compiler or an independent behavior acceptance.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import REUSED_BINDINGS

APPROVED = {'contexts_reuse': {'ForceHeadMatch', 'RosterMemory'},
 'domain': {'GameState',
            'Long',
            'RandomSample',
            'Table',
            'Word',
            'checked_state',
            'checked_table',
            'descending_inclusive',
            'divu_retained',
            'high16',
            'low16',
            'low8',
            'negative_byte',
            'negative_long',
            'negative_word',
            'replace_word',
            's16',
            's8',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'},
 'contexts_message': {'MessageMemory',
                      'MessagePointerFields',
                      'MessagePreparation',
                      'SceneMessageInput',
                      'SceneMessageResult',
                      'SceneState',
                      'checked_scene_state'}}

DECLARATIONS = {'build_roster': {'signature': 'state: GameState, city: Word',
 'returns': 'Word',
 'flow': 'checked_state(state)\nreturn _build_roster_fields(RosterMemory(state), city)'},
 '_advance_random_pair': {'signature': 'state: GameState',
                          'returns': 'RandomSample',
                          'flow': 'checked_state(state)\n'
                                  "original = state.scalar('random_seed')\n"
                                  'if original == 0:\n'
                                  '    original = 711800410\n'
                                  'mixed = u32(u32(u32(u32(original << 2) + original) << 3) + '
                                  'original)\n'
                                  'sample = replace_word(original, low16(mixed))\n'
                                  'mixed = swap_words(mixed)\n'
                                  'sample = replace_word(sample, u16(low16(sample) + '
                                  'low16(mixed)))\n'
                                  'mixed = swap_words(replace_word(mixed, low16(sample)))\n'
                                  "state.set_scalar('random_seed', mixed)\n"
                                  'return RandomSample(sample, mixed)'},
 'step_random': {'signature': 'state: GameState',
                 'returns': 'Long',
                 'flow': 'return _advance_random_pair(state).sample'},
 'choose_city_head': {'signature': 'state: GameState, city: Word',
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
 'roster_contains_force_head_carry': {'signature': 'state: GameState, city: Word, head: Word',
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
 'debit_city_gold': {'signature': 'state: GameState',
                     'returns': 'None',
                     'flow': 'checked_state(state)\n'
                             "city = u16(state.scalar('deployment_city') << 2)\n"
                             "amount = state.scalar('action_amount')\n"
                             'state.city_gold.set_long(city, u32(state.city_gold.long(city) - '
                             'amount))'},
 'education_factor': {'signature': 'state: GameState, teacher: Word, target: Word',
                      'returns': 'Word',
                      'flow': 'checked_state(state)\n'
                              'uint(teacher, 16)\n'
                              'uint(target, 16)\n'
                              'index = 0\n'
                              'for threshold in (20, 40, 60, 80):\n'
                              '    if target < threshold:\n'
                              '        break\n'
                              '    index += 5\n'
                              'for threshold in (20, 40, 60, 80):\n'
                              '    if teacher < threshold:\n'
                              '        break\n'
                              '    index += 1\n'
                              'return u16(s8(state.education_factors.byte(index)))'},
 'commit_mutual_relationship': {'signature': 'state: GameState',
                                'returns': 'None',
                                'flow': 'checked_state(state)\n'
                                        "target = u16(state.scalar('relationship_target') << 1)\n"
                                        'bit = state.relationship_targets.word(target)\n'
                                        "force = u16(state.scalar('current_force') << 1)\n"
                                        'flags = state.force_relationships.word(force)\n'
                                        'state.force_relationships.set_word(force, u16(flags | 1 '
                                        '<< (bit & 31)))\n'
                                        "target = u16(state.scalar('relationship_target') << 1)\n"
                                        'target = u16(state.relationship_targets.word(target) << '
                                        '1)\n'
                                        "bit = state.scalar('current_force')\n"
                                        'flags = state.force_relationships.word(target)\n'
                                        'state.force_relationships.set_word(target, u16(flags | 1 '
                                        '<< (bit & 31)))'},
 '_add_live_progress': {'signature': 'progress: Table, offset: Word, gain: Word',
                        'returns': 'None',
                        'flow': 'progress.set_word(offset, u16(progress.word(offset) + gain))\n'
                                'if progress.word(offset) > 999:\n'
                                '    progress.set_word(offset, 999)'},
 'add_progress_be': {'signature': 'state: GameState, gain: Word',
                     'returns': 'None',
                     'flow': 'checked_state(state)\n'
                             'uint(gain, 16)\n'
                             "offset = u16(state.scalar('selected_officer') << 1)\n"
                             '_add_live_progress(state.officer_word_be00, offset, gain)'},
 'split_progress': {'signature': 'state: GameState, gain: Long',
                    'returns': 'Word',
                    'flow': 'checked_state(state)\n'
                            'uint(gain, 32)\n'
                            "offset = u16(state.scalar('selected_officer') << 1)\n"
                            'packed = divu_retained(low16(gain), 10)\n'
                            '_add_live_progress(state.officer_word_be00, offset, low16(packed))\n'
                            'amount = low16(packed) >> 1\n'
                            '_add_live_progress(state.officer_word_c000, offset, amount)\n'
                            'return amount'},
 'grant_duel_fallback_progress': {'signature': 'state: GameState, receiver_offset: Word, donor: '
                                               'Word, progress: Table',
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
 'grant_duel_troop_difference_progress': {'signature': 'state: GameState, receiver: Word, '
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
 '_active_duel_roster': {'signature': 'state: GameState, officer: Word',
                         'returns': None,
                         'flow': "if officer == state.scalar('roster_side_owner'):\n"
                                 '    return state.battle_primary_roster.cursor()\n'
                                 'return state.battle_secondary_roster.cursor()'},
 '_compact_after_match': {'signature': 'source',
                          'returns': None,
                          'flow': 'while True:\n'
                                  '    member = source.next_word()\n'
                                  '    source.set_word(0, member, -4)\n'
                                  '    if negative_word(member):\n'
                                  '        return'},
 'remove_zero_readiness_duelist': {'signature': 'state: GameState, officer: Word',
                                   'returns': 'None',
                                   'flow': 'checked_state(state)\n'
                                           'uint(officer, 16)\n'
                                           "if state.scalar('battle_active') == 0:\n"
                                           '    return\n'
                                           'state.officer_city_assignment.set_byte(officer, 255)\n'
                                           'source = _active_duel_roster(state, officer)\n'
                                           'while True:\n'
                                           '    member = source.next_word()\n'
                                           '    if negative_word(member):\n'
                                           '        return\n'
                                           '    if low8(member) == officer:\n'
                                           '        break\n'
                                           '_compact_after_match(source)'},
 'settle_duel_result_roster': {'signature': 'state: GameState',
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
 'transfer_battle_roster': {'signature': 'state: GameState, officer: Word',
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
                                    '_compact_after_match(source)\n'
                                    'while not negative_word(destination.next_word()):\n'
                                    '    pass\n'
                                    'destination.set_word(0, officer, -2)\n'
                                    'destination.put_word(65535)'},
 'detach_defeated_duelist': {'signature': 'state: GameState, officer: Word',
                             'returns': 'None',
                             'flow': 'checked_state(state)\n'
                                     'uint(officer, 16)\n'
                                     'state.officer_city_assignment.set_byte(officer, 255)\n'
                                     'source = _active_duel_roster(state, officer)\n'
                                     'while low8(source.next_word()) != officer:\n'
                                     '    pass\n'
                                     '_compact_after_match(source)'},
 'count_selected_deployment': {'signature': 'state: GameState',
                               'returns': 'Word',
                               'flow': 'checked_state(state)\n'
                                       'source = state.candidate_roster.cursor()\n'
                                       'count = 0\n'
                                       'while True:\n'
                                       '    member = source.next_word()\n'
                                       '    if negative_word(member):\n'
                                       '        return count\n'
                                       '    if member & 16384:\n'
                                       '        count = u16(count + 1)'},
 'initialize_selected_assignment': {'signature': 'state: GameState, group: Table',
                                    'returns': 'None',
                                    'flow': 'checked_state(state)\n'
                                            'checked_table(group, state)\n'
                                            'force = group.byte(0, 4)\n'
                                            "city = state.scalar('deployment_city')\n"
                                            'if force == state.city_owner_bytes.byte(city):\n'
                                            '    city |= 64\n'
                                            'source = state.candidate_roster.cursor()\n'
                                            'while True:\n'
                                            '    member = source.next_word()\n'
                                            '    if negative_word(member):\n'
                                            '        return\n'
                                            '    if not member & 16384:\n'
                                            '        continue\n'
                                            '    member = low8(member)\n'
                                            '    '
                                            'state.battlefield_city_assignment.set_byte(member, '
                                            'low8(city))\n'
                                            '    state.battle_positions.set_long(u16(member << 2), '
                                            '0)'},
 'selected_troop_weights': {'signature': 'state: GameState',
                            'returns': 'tuple[Long, Long]',
                            'flow': 'checked_state(state)\n'
                                    'source = state.candidate_roster.cursor()\n'
                                    'selected, total = (0, 0)\n'
                                    'while True:\n'
                                    '    member = source.next_word()\n'
                                    '    if negative_word(member):\n'
                                    '        break\n'
                                    '    offset = u16(member << 2)\n'
                                    '    if member & 16384:\n'
                                    '        selected = u32(selected + '
                                    'state.officer_troops.long(offset))\n'
                                    '        selected = u32(selected + 100)\n'
                                    '    total = u32(total + state.officer_troops.long(offset))\n'
                                    '    total = u32(total + 100)\n'
                                    'selected = replace_word(selected, low16(selected) >> 5)\n'
                                    'total = replace_word(total, low16(total) >> 5)\n'
                                    'return (selected, total)'},
 'refresh_object_attribute_average': {'signature': 'state: GameState, group: Table, divisor: Word',
                                      'returns': 'None',
                                      'flow': 'checked_state(state)\n'
                                              'checked_table(group, state)\n'
                                              'uint(divisor, 16)\n'
                                              'divisor = group.byte() & 15\n'
                                              'start = u8(divisor - 1)\n'
                                              'total = 0\n'
                                              'for index in descending_inclusive(start):\n'
                                              '    member = group.byte(index, 13)\n'
                                              '    total = u8(total + '
                                              'state.selected_attributes.byte(member))\n'
                                              'total = divu_retained(total, divisor)\n'
                                              'group.set_byte(0, low8(total), 3)'},
 'submit_deployment_queue': {'signature': 'state: GameState, group: Table',
                             'returns': 'None',
                             'flow': 'checked_state(state)\n'
                                     'checked_table(group, state)\n'
                                     "if state.scalar('command_sound') == 521:\n"
                                     "    if state.scalar('ui_state') == 5:\n"
                                     '        return\n'
                                     "city = state.scalar('deployment_city')\n"
                                     'if state.city_command_flags.byte(city) & 2:\n'
                                     '    return\n'
                                     'state.city_command_flags.set_byte(city, 2)\n'
                                     'officer = group.byte(0, 13)\n'
                                     'destination = '
                                     "state.deployment_queue.cursor(state.scalar('deployment_queue_offset'))\n"
                                     'destination.append_byte(0)\n'
                                     'destination.append_byte(officer)\n'
                                     'destination.append_byte(group.byte(0, 3))\n'
                                     'destination.append_byte(128)\n'
                                     "destination.append_byte(state.scalar('deployment_city_tail'))\n"
                                     'destination.append_byte(0)\n'
                                     'destination.set_byte(0, 255)\n'
                                     "counter = state.scalar('deployment_queue_offset')\n"
                                     "state.set_scalar('deployment_queue_offset', u16(counter + "
                                     '6))\n'
                                     'clear_original_tail_coordinate(state)'},
 'clear_original_tail_coordinate': {'signature': 'state: GameState',
                                    'returns': 'None',
                                    'flow': 'checked_state(state)\n'
                                            "city = state.scalar('battle_scene')\n"
                                            'if state.officer_city_assignment.byte(255) == '
                                            'low8(city):\n'
                                            '    state.battle_positions.set_long(u16(255 << 2), '
                                            '0)'},
 'build_city_assigned_outcome_candidates': {'signature': 'state: GameState',
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
 'build_battlefield_outcome_candidates': {'signature': 'state: GameState',
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
 'signed_divmod': {'signature': 'state: GameState, numerator: Long, denominator: Long',
                   'returns': 'tuple[Long, Long]',
                   'flow': 'checked_state(state)\n'
                           'uint(numerator, 32)\n'
                           'uint(denominator, 32)\n'
                           'if negative_long(denominator):\n'
                           '    quotient, remainder = positive_denominator(state, numerator, '
                           'u32(-denominator))\n'
                           '    return (u32(-quotient), remainder)\n'
                           'return positive_denominator(state, numerator, denominator)'},
 'positive_denominator': {'signature': 'state: GameState, numerator: Long, denominator: Long',
                          'returns': 'tuple[Long, Long]',
                          'flow': 'checked_state(state)\n'
                                  'uint(numerator, 32)\n'
                                  'uint(denominator, 32)\n'
                                  'if negative_long(numerator):\n'
                                  '    quotient, remainder = unsigned_divmod(state, '
                                  'u32(-numerator), denominator)\n'
                                  '    return (u32(-quotient), u32(-remainder))\n'
                                  'return unsigned_divmod(state, numerator, denominator)'},
 'unsigned_divmod': {'signature': 'state: GameState, numerator: Long, denominator: Long',
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
 'word_pair_divmod': {'signature': 'state: GameState, numerator: Long, denominator: Long',
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
 'prepare_message': {'signature': 'state: GameState, message: Word',
                     'returns': 'None',
                     'flow': 'checked_state(state)\n'
                             '_prepare_message_fields(MessageMemory(state), message)'},
 'select_message_layout': {'signature': 'state: GameState',
                           'returns': 'None',
                           'flow': 'checked_state(state)\n'
                                   '_select_message_fields(MessageMemory(state))'},
 'resolve_message_pointer': {'signature': 'state: GameState, message: Word',
                             'returns': 'Table',
                             'flow': 'checked_state(state)\n'
                                     'resolved = _resolve_message_fields(MessageMemory(state), '
                                     'message)\n'
                                     'return state.table(resolved.pointer)'},
 '_resolve_message_fields': {'signature': 'memory: MessageMemory, message: Word',
                             'returns': 'MessagePointerFields',
                             'flow': 'uint(message, 16)\n'
                                     'bank = memory.read(601162, 4)\n'
                                     'bank_offset = u16(message >> 8 << 1)\n'
                                     'bank_delta = memory.read(u32(601166 + s16(bank_offset)), 2)\n'
                                     'descriptor = u32(bank + s16(bank_delta))\n'
                                     'pointer = memory.read(descriptor, 4)\n'
                                     'item = u16(low8(message) << 1)\n'
                                     'item_delta = memory.read(u32(descriptor + s16(item) + 4), '
                                     '2)\n'
                                     'pointer = u32(pointer + s16(item_delta))\n'
                                     'return MessagePointerFields(pointer, descriptor, '
                                     'item_delta)'},
 '_select_message_fields': {'signature': 'memory: MessageMemory',
                            'returns': 'Word',
                            'flow': 'offset = u16(memory.read(4294964932, 2) << 2)\n'
                                    'scene = memory.read(u32(423740 + s16(offset)), 2)\n'
                                    'memory.write(4294964754, 2, scene)\n'
                                    'stage = memory.read(u32(423740 + s16(offset) + 2), 2)\n'
                                    'memory.write(4294964066, 2, stage)\n'
                                    'return offset'},
 '_prepare_message_fields': {'signature': 'memory: MessageMemory, message: Word',
 'returns': 'MessagePreparation',
 'flow': 'uint(message, 16)\n'
         'if negative_word(message):\n'
         '    return MessagePreparation(None, None, False, False, True, False)\n'
         'memory.read(4294964818, 2)\n'
         'memory.write(4294964818, 2, 0)\n'
         'resolved = _resolve_message_fields(memory, message)\n'
         'memory.write(4294964158, 4, resolved.pointer)\n'
         'scene = memory.read(4294964754, 2)\n'
         'memory.write(4294964162, 2, scene)\n'
         'stage = memory.read(4294964066, 2)\n'
         'memory.write(4294964164, 2, stage)\n'
         'memory.read(4294964074, 2)\n'
         'memory.write(4294964074, 2, 0)\n'
         'memory.read(4294964166, 2)\n'
         'memory.write(4294964166, 2, 0)\n'
         'memory.write(4294964736, 2, 40)\n'
         'layout_offset = _select_message_fields(memory)\n'
         'memory.write(4294963162, 2, 1)\n'
         'return MessagePreparation(resolved, layout_offset, False, False, False, False)'},
 'prepare_scene_message': {'signature': 'state: SceneState, inputs: SceneMessageInput',
                           'returns': 'SceneMessageResult',
                           'flow': 'checked_scene_state(state)\n'
                                   'if type(inputs) is not SceneMessageInput:\n'
                                   "    raise ValueError('explicit scene message input required')\n"
                                   'inputs.validate(state)\n'
                                   'observed = _prepare_message_fields(MessageMemory(state), '
                                   'low16(inputs.value))\n'
                                   'if observed.resolved is None:\n'
                                   '    destination = inputs.destination\n'
                                   '    source = inputs.source\n'
                                   '    value = inputs.value\n'
                                   '    field = inputs.field\n'
                                   'else:\n'
                                   '    destination = state.table_at(observed.resolved.pointer)\n'
                                   '    source = state.table_at(observed.resolved.descriptor)\n'
                                   '    value = replace_word(inputs.value, '
                                   'observed.layout_offset)\n'
                                   '    field = replace_word(inputs.field, '
                                   'observed.resolved.item_offset)\n'
                                   'result = SceneMessageResult(destination, source, value, field, '
                                   'observed.carry, observed.zero, observed.negative, '
                                   'observed.overflow)\n'
                                   'return result.validate(state)'}}

def _lower_build_roster(e,rules):
    e.label('action_pc_005f48')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('action_pc_005f4c')
    e.ins('lea.l','0xf500:w,%a1',4)
    e.label('action_pc_005f50')
    e.ins('clr.w','%d1',2)
    e.label('action_pc_005f52')
    e.ins('clr.w','%d3',2)
    e.label('action_pc_005f54')
    e.ins('move.w','0xf630:w,%d4',4)
    e.label('action_pc_005f58')
    e.ins('bmi.b','action_pc_005f5e',2)
    e.label('action_pc_005f5a')
    e.ins('move.w','%d4,(%a1)+',2)
    e.label('action_pc_005f5c')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('action_pc_005f5e')
    e.ins('move.b','(%a0)+,%d2',2)
    e.label('action_pc_005f60')
    e.ins('cmp.b','%d0,%d2',2)
    e.label('action_pc_005f62')
    e.ins('bne.b','action_pc_005f6e',2)
    e.label('action_pc_005f64')
    e.ins('cmp.w','0xf630:w,%d1',4)
    e.label('action_pc_005f68')
    e.ins('beq.b','action_pc_005f6e',2)
    e.label('action_pc_005f6a')
    e.ins('move.w','%d1,(%a1)+',2)
    e.label('action_pc_005f6c')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('action_pc_005f6e')
    e.ins('addq.w','#0x1,%d1',2)
    e.label('action_pc_005f70')
    e.ins('cmpi.w','#0x100,%d1',4)
    e.label('action_pc_005f74')
    e.ins('bcs.b','action_pc_005f5e',2)
    e.label('action_pc_005f76')
    e.ins('move.w','#0xffff,(%a1)',4)
    e.label('action_pc_005f7a')
    e.ins('rts','',2)

def _lower_step_random(e,rules):
    e.label('action_pc_0083d4')
    e.ins('move.l','0xf61c:w,%d1',4)
    e.label('action_pc_0083d8')
    e.ins('bne.b','action_pc_0083e0',2)
    e.label('action_pc_0083da')
    e.ins('move.l','#0x2a6d365a,%d1',6)
    e.label('action_pc_0083e0')
    e.ins('move.l','%d1,%d0',2)
    e.label('action_pc_0083e2')
    e.ins('asl.l','#0x2,%d1',2)
    e.label('action_pc_0083e4')
    e.ins('add.l','%d0,%d1',2)
    e.label('action_pc_0083e6')
    e.ins('asl.l','#0x3,%d1',2)
    e.label('action_pc_0083e8')
    e.ins('add.l','%d0,%d1',2)
    e.label('action_pc_0083ea')
    e.ins('move.w','%d1,%d0',2)
    e.label('action_pc_0083ec')
    e.ins('swap','%d1',2)
    e.label('action_pc_0083ee')
    e.ins('add.w','%d1,%d0',2)
    e.label('action_pc_0083f0')
    e.ins('move.w','%d0,%d1',2)
    e.label('action_pc_0083f2')
    e.ins('swap','%d1',2)
    e.label('action_pc_0083f4')
    e.ins('move.l','%d1,0xf61c:w',4)
    e.label('action_pc_0083f8')
    e.ins('rts','',2)

def _lower_choose_city_head(e,rules):
    e.label('action_pc_00e1f6')
    e.ins('movem.l','%d1-%d5/%a0-%a2,-(%a7)',4)
    e.label('action_pc_00e1fa')
    e.ins('lea.l','0xf500:w,%a0',4)
    e.label('action_pc_00e1fe')
    e.ins('move.w','(%a0)+,%d4',2)
    e.label('action_pc_00e200')
    e.ins('bmi.w','action_pc_00e232',4)
    e.label('action_pc_00e204')
    e.ins('bsr.w','action_pc_00e26c',4)
    e.label('action_pc_00e208')
    e.ins('bcs.w','action_pc_00e25a',4)
    e.label('action_pc_00e20c')
    e.ins('andi.w','#0xff,%d4',4)
    e.label('action_pc_00e210')
    e.ins('lea.l','0xc300:w,%a1',4)
    e.label('action_pc_00e214')
    e.ins('move.w','%d4,%d3',2)
    e.label('action_pc_00e216')
    e.ins('move.b','(%a1, %d3.w),%d1',4)
    e.label('action_pc_00e21a')
    e.ins('move.b','%d1,%d2',2)
    e.label('action_pc_00e21c')
    e.ins('move.w','(%a0)+,%d3',2)
    e.label('action_pc_00e21e')
    e.ins('bmi.b','action_pc_00e25a',2)
    e.label('action_pc_00e220')
    e.ins('andi.w','#0xff,%d3',4)
    e.label('action_pc_00e224')
    e.ins('move.b','(%a1, %d3.w),%d1',4)
    e.label('action_pc_00e228')
    e.ins('cmp.b','%d2,%d1',2)
    e.label('action_pc_00e22a')
    e.ins('bls.b','action_pc_00e21c',2)
    e.label('action_pc_00e22c')
    e.ins('move.w','%d3,%d4',2)
    e.label('action_pc_00e22e')
    e.ins('move.b','%d1,%d2',2)
    e.label('action_pc_00e230')
    e.ins('bra.b','action_pc_00e21c',2)
    e.label('action_pc_00e232')
    e.ins('lea.l','0xf427:w,%a0',4)
    e.label('action_pc_00e236')
    e.ins('move.b','#0xff,(%a0, %d0.w)',6)
    e.label('action_pc_00e23c')
    e.ins('lea.l','0xe80c:w,%a0',4)
    e.label('action_pc_00e240')
    e.ins('move.w','%d0,%d1',2)
    e.label('action_pc_00e242')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('action_pc_00e244')
    e.ins('add.w','%d0,%d1',2)
    e.label('action_pc_00e246')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('action_pc_00e248')
    e.ins('move.w','#0xffff,(%a0, %d1.w)',6)
    e.label('action_pc_00e24e')
    e.ins('move.w','#0xffff,0x4(%a0, %d1.w)',6)
    e.label('action_pc_00e254')
    e.ins('move.w','#0xffff,0x8(%a0, %d1.w)',6)
    e.label('action_pc_00e25a')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00e25c')
    e.ins('lea.l','0xf45e:w,%a0',4)
    e.label('action_pc_00e260')
    e.ins('move.w','%d4,(%a0, %d0.w)',4)
    e.label('action_pc_00e264')
    e.ins('move.w','%d4,%d0',2)
    e.label('action_pc_00e266')
    e.ins('movem.l','(%a7)+,%d1-%d5/%a0-%a2',4)
    e.label('action_pc_00e26a')
    e.ins('rts','',2)

def _lower_roster_contains_force_head_carry(e,rules):
    e.label('action_pc_00e26c')
    e.ins('lea.l','0xf427:w,%a2',4)
    e.label('action_pc_00e270')
    e.ins('clr.w','%d5',2)
    e.label('action_pc_00e272')
    e.ins('move.b','(%a2, %d0.w),%d5',4)
    e.label('action_pc_00e276')
    e.ins('lsl.w','#0x1,%d5',2)
    e.label('action_pc_00e278')
    e.ins('lea.l','0xe640:w,%a2',4)
    e.label('action_pc_00e27c')
    e.ins('move.w','(%a2, %d5.w),%d5',4)
    e.label('action_pc_00e280')
    e.ins('lea.l','0xf500:w,%a2',4)
    e.label('action_pc_00e284')
    e.ins('tst.w','(%a2)',2)
    e.label('action_pc_00e286')
    e.ins('bmi.w','action_pc_00e298',4)
    e.label('action_pc_00e28a')
    e.ins('cmp.w','(%a2)+,%d5',2)
    e.label('action_pc_00e28c')
    e.ins('bne.b','action_pc_00e284',2)
    e.label('action_pc_00e28e')
    e.ins('move.w','%d5,%d4',2)
    e.label('action_pc_00e290')
    e.ins('ori.w','#0x1,%sr',4)
    e.label('action_pc_00e294')
    e.ins('bra.w','action_pc_00e29c',4)
    e.label('action_pc_00e298')
    e.ins('andi.w','#0xfffe,%sr',4)
    e.label('action_pc_00e29c')
    e.ins('rts','',2)

def _lower_debit_city_gold(e,rules):
    e.label('action_pc_00e70a')
    e.ins('move.w','0xf392:w,%d0',4)
    e.label('action_pc_00e70e')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('action_pc_00e710')
    e.ins('lea.l','0xdffc:w,%a0',4)
    e.label('action_pc_00e714')
    e.ins('move.l','0xf39e:w,%d1',4)
    e.label('action_pc_00e718')
    e.ins('sub.l','%d1,(%a0, %d0.w)',4)
    e.label('action_pc_00e71c')
    e.ins('rts','',2)

def _lower_education_factor(e,rules):
    e.label('action_pc_00e71e')
    e.ins('clr.w','%d3',2)
    e.label('action_pc_00e720')
    e.ins('cmpi.w','#0x14,%d1',4)
    e.label('action_pc_00e724')
    e.ins('bcs.b','action_pc_00e748',2)
    e.label('action_pc_00e726')
    e.ins('move.w','#0x5,%d3',4)
    e.label('action_pc_00e72a')
    e.ins('cmpi.w','#0x28,%d1',4)
    e.label('action_pc_00e72e')
    e.ins('bcs.b','action_pc_00e748',2)
    e.label('action_pc_00e730')
    e.ins('move.w','#0xa,%d3',4)
    e.label('action_pc_00e734')
    e.ins('cmpi.w','#0x3c,%d1',4)
    e.label('action_pc_00e738')
    e.ins('bcs.b','action_pc_00e748',2)
    e.label('action_pc_00e73a')
    e.ins('move.w','#0xf,%d3',4)
    e.label('action_pc_00e73e')
    e.ins('cmpi.w','#0x50,%d1',4)
    e.label('action_pc_00e742')
    e.ins('bcs.b','action_pc_00e748',2)
    e.label('action_pc_00e744')
    e.ins('move.w','#0x14,%d3',4)
    e.label('action_pc_00e748')
    e.ins('cmpi.w','#0x14,%d0',4)
    e.label('action_pc_00e74c')
    e.ins('bcs.b','action_pc_00e768',2)
    e.label('action_pc_00e74e')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('action_pc_00e750')
    e.ins('cmpi.w','#0x28,%d0',4)
    e.label('action_pc_00e754')
    e.ins('bcs.b','action_pc_00e768',2)
    e.label('action_pc_00e756')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('action_pc_00e758')
    e.ins('cmpi.w','#0x3c,%d0',4)
    e.label('action_pc_00e75c')
    e.ins('bcs.b','action_pc_00e768',2)
    e.label('action_pc_00e75e')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('action_pc_00e760')
    e.ins('cmpi.w','#0x50,%d0',4)
    e.label('action_pc_00e764')
    e.ins('bcs.b','action_pc_00e768',2)
    e.label('action_pc_00e766')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('action_pc_00e768')
    e.ins('lea.l','12(%pc),%a0',4)
    e.label('action_pc_00e76c')
    e.ins('nop','',2)
    e.label('action_pc_00e76e')
    e.ins('move.b','(%a0, %d3.w),%d2',4)
    e.label('action_pc_00e772')
    e.ins('ext.w','%d2',2)
    e.label('action_pc_00e774')
    e.ins('rts','',2)

def _lower_commit_mutual_relationship(e,rules):
    e.label('action_pc_00ec16')
    e.ins('move.w','0xf3e0:w,%d0',4)
    e.label('action_pc_00ec1a')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00ec1c')
    e.ins('lea.l','0xe730:w,%a0',4)
    e.label('action_pc_00ec20')
    e.ins('move.w','(%a0, %d0.w),%d1',4)
    e.label('action_pc_00ec24')
    e.ins('move.w','0xf376:w,%d0',4)
    e.label('action_pc_00ec28')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00ec2a')
    e.ins('lea.l','0xe710:w,%a0',4)
    e.label('action_pc_00ec2e')
    e.ins('move.w','(%a0, %d0.w),%d2',4)
    e.label('action_pc_00ec32')
    e.ins('bset.l','%d1,%d2',2)
    e.label('action_pc_00ec34')
    e.ins('move.w','%d2,(%a0, %d0.w)',4)
    e.label('action_pc_00ec38')
    e.ins('move.w','0xf3e0:w,%d0',4)
    e.label('action_pc_00ec3c')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00ec3e')
    e.ins('lea.l','0xe730:w,%a0',4)
    e.label('action_pc_00ec42')
    e.ins('move.w','(%a0, %d0.w),%d0',4)
    e.label('action_pc_00ec46')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00ec48')
    e.ins('move.w','0xf376:w,%d1',4)
    e.label('action_pc_00ec4c')
    e.ins('lea.l','0xe710:w,%a0',4)
    e.label('action_pc_00ec50')
    e.ins('move.w','(%a0, %d0.w),%d2',4)
    e.label('action_pc_00ec54')
    e.ins('bset.l','%d1,%d2',2)
    e.label('action_pc_00ec56')
    e.ins('move.w','%d2,(%a0, %d0.w)',4)
    e.label('action_pc_00ec5a')
    e.ins('rts','',2)

def _lower_add_progress_be(e,rules):
    e.label('action_pc_00ef60')
    e.ins('move.w','0xf3a6:w,%d0',4)
    e.label('action_pc_00ef64')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00ef66')
    e.ins('lea.l','0xbe00:w,%a0',4)
    e.label('action_pc_00ef6a')
    e.ins('add.w','%d2,(%a0, %d0.w)',4)
    e.label('action_pc_00ef6e')
    e.ins('cmpi.w','#0x3e7,(%a0, %d0.w)',6)
    e.label('action_pc_00ef74')
    e.ins('bls.w','action_pc_00ef7e',4)
    e.label('action_pc_00ef78')
    e.ins('move.w','#0x3e7,(%a0, %d0.w)',6)
    e.label('action_pc_00ef7e')
    e.ins('rts','',2)

def _lower_split_progress(e,rules):
    e.label('action_pc_00f990')
    e.ins('move.w','0xf3a6:w,%d0',4)
    e.label('action_pc_00f994')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00f996')
    e.ins('andi.l','#0xffff,%d2',6)
    e.label('action_pc_00f99c')
    e.ins('divu.w','#0xa,%d2',4)
    e.label('action_pc_00f9a0')
    e.ins('lea.l','0xbe00:w,%a0',4)
    e.label('action_pc_00f9a4')
    e.ins('add.w','%d2,(%a0, %d0.w)',4)
    e.label('action_pc_00f9a8')
    e.ins('cmpi.w','#0x3e7,(%a0, %d0.w)',6)
    e.label('action_pc_00f9ae')
    e.ins('bls.b','action_pc_00f9b6',2)
    e.label('action_pc_00f9b0')
    e.ins('move.w','#0x3e7,(%a0, %d0.w)',6)
    e.label('action_pc_00f9b6')
    e.ins('lsr.w','#0x1,%d2',2)
    e.label('action_pc_00f9b8')
    e.ins('lea.l','0xc000:w,%a0',4)
    e.label('action_pc_00f9bc')
    e.ins('add.w','%d2,(%a0, %d0.w)',4)
    e.label('action_pc_00f9c0')
    e.ins('cmpi.w','#0x3e7,(%a0, %d0.w)',6)
    e.label('action_pc_00f9c6')
    e.ins('bls.b','action_pc_00f9ce',2)
    e.label('action_pc_00f9c8')
    e.ins('move.w','#0x3e7,(%a0, %d0.w)',6)
    e.label('action_pc_00f9ce')
    e.ins('rts','',2)

def _lower_grant_duel_fallback_progress(e,rules):
    e.label('action_pc_0189d4')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('action_pc_0189d6')
    e.ins('move.w','(%a3, %d1.w),%d2',4)
    e.label('action_pc_0189da')
    e.ins('ext.l','%d2',2)
    e.label('action_pc_0189dc')
    e.ins('divu.w','#0x28,%d2',4)
    e.label('action_pc_0189e0')
    e.ins('lsr.w','#0x1,%d1',2)
    e.label('action_pc_0189e2')
    e.ins('move.w','0xf68a:w,%d3',4)
    e.label('action_pc_0189e6')
    e.ins('lsl.w','#0x1,%d3',2)
    e.label('action_pc_0189e8')
    e.ins('lea.l','0xf45e:w,%a5',4)
    e.label('action_pc_0189ec')
    e.ins('cmp.w','(%a5, %d3.w),%d1',4)
    e.label('action_pc_0189f0')
    e.ins('beq.w','action_pc_018a00',4)
    e.label('action_pc_0189f4')
    e.ins('lea.l','0xa026:w,%a5',4)
    e.label('action_pc_0189f8')
    e.ins('cmp.w','(%a5, %d3.w),%d1',4)
    e.label('action_pc_0189fc')
    e.ins('bne.w','action_pc_018a04',4)
    e.label('action_pc_018a00')
    e.ins('addi.w','#0x1e,%d2',4)
    e.label('action_pc_018a04')
    e.ins('lea.l','0xc700:w,%a5',4)
    e.label('action_pc_018a08')
    e.ins('btst.b','#0x4,(%a5, %d1.w)',6)
    e.label('action_pc_018a0e')
    e.ins('beq.w','action_pc_018a16',4)
    e.label('action_pc_018a12')
    e.ins('addi.w','#0x14,%d2',4)
    e.label('action_pc_018a16')
    e.ins('move.w','(%a3, %d0.w),%d3',4)
    e.label('action_pc_018a1a')
    e.ins('add.w','%d2,%d3',2)
    e.label('action_pc_018a1c')
    e.ins('cmpi.w','#0x3e7,%d3',4)
    e.label('action_pc_018a20')
    e.ins('bls.w','action_pc_018a28',4)
    e.label('action_pc_018a24')
    e.ins('move.w','#0x3e7,%d3',4)
    e.label('action_pc_018a28')
    e.ins('move.w','%d3,(%a3, %d0.w)',4)
    e.label('action_pc_018a2c')
    e.ins('rts','',2)

def _lower_grant_duel_troop_difference_progress(e,rules):
    e.label('action_pc_018a2e')
    e.ins('andi.l','#0xffff,%d2',6)
    e.label('action_pc_018a34')
    e.ins('divu.w','#0x64,%d2',4)
    e.label('action_pc_018a38')
    e.ins('move.w','%d0,%d1',2)
    e.label('action_pc_018a3a')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('action_pc_018a3c')
    e.ins('move.w','(%a3, %d1.w),%d3',4)
    e.label('action_pc_018a40')
    e.ins('add.w','%d2,%d3',2)
    e.label('action_pc_018a42')
    e.ins('cmpi.w','#0x3e7,%d3',4)
    e.label('action_pc_018a46')
    e.ins('bls.w','action_pc_018a4e',4)
    e.label('action_pc_018a4a')
    e.ins('move.w','#0x3e7,%d3',4)
    e.label('action_pc_018a4e')
    e.ins('move.w','%d3,(%a3, %d1.w)',4)
    e.label('action_pc_018a52')
    e.ins('rts','',2)

def _lower_remove_zero_readiness_duelist(e,rules):
    e.label('action_pc_018a54')
    e.ins('movem.l','%d2/%a0,-(%a7)',4)
    e.label('action_pc_018a58')
    e.ins('tst.w','0xefe0:w',4)
    e.label('action_pc_018a5c')
    e.ins('beq.w','action_pc_018a8e',4)
    e.label('action_pc_018a60')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('action_pc_018a64')
    e.ins('move.b','#0xff,(%a0, %d1.w)',6)
    e.label('action_pc_018a6a')
    e.ins('lea.l','0xa550:w,%a0',4)
    e.label('action_pc_018a6e')
    e.ins('cmp.w','0xf702:w,%d1',4)
    e.label('action_pc_018a72')
    e.ins('beq.w','action_pc_018a7a',4)
    e.label('action_pc_018a76')
    e.ins('lea.l','0xa5a4:w,%a0',4)
    e.label('action_pc_018a7a')
    e.ins('move.w','(%a0)+,%d2',2)
    e.label('action_pc_018a7c')
    e.ins('bmi.w','action_pc_018a8e',4)
    e.label('action_pc_018a80')
    e.ins('andi.w','#0xff,%d2',4)
    e.label('action_pc_018a84')
    e.ins('cmp.w','%d1,%d2',2)
    e.label('action_pc_018a86')
    e.ins('bne.b','action_pc_018a7a',2)
    e.label('action_pc_018a88')
    e.ins('move.w','(%a0)+,-0x4(%a0)',4)
    e.label('action_pc_018a8c')
    e.ins('bpl.b','action_pc_018a88',2)
    e.label('action_pc_018a8e')
    e.ins('movem.l','(%a7)+,%d2/%a0',4)
    e.label('action_pc_018a92')
    e.ins('rts','',2)

def _lower_settle_duel_result_roster(e,rules):
    e.label('action_pc_018a94')
    e.ins('tst.w','0xefe0:w',4)
    e.label('action_pc_018a98')
    e.ins('beq.w','action_pc_018ac4',4)
    e.label('action_pc_018a9c')
    e.ins('cmpi.w','#0x6,0xffff8114:l',8)
    e.label('action_pc_018aa4')
    e.ins('bcs.w','action_pc_018ac4',4)
    e.label('action_pc_018aa8')
    e.ins('bne.w','action_pc_018aba',4)
    e.label('action_pc_018aac')
    e.ins('move.w','0xffff80e0:l,%d0',6)
    e.label('action_pc_018ab2')
    e.ins('bsr.w','action_pc_018ac6',4)
    e.label('action_pc_018ab6')
    e.ins('bra.w','action_pc_018ac4',4)
    e.label('action_pc_018aba')
    e.ins('move.w','0xffff80e2:l,%d0',6)
    e.label('action_pc_018ac0')
    e.ins('bsr.w','action_pc_018ac6',4)
    e.label('action_pc_018ac4')
    e.ins('rts','',2)

def _lower_transfer_battle_roster(e,rules):
    e.label('action_pc_018ac6')
    e.ins('lea.l','0xa5a4:w,%a0',4)
    e.label('action_pc_018aca')
    e.ins('lea.l','0xa57a:w,%a1',4)
    e.label('action_pc_018ace')
    e.ins('cmp.w','0xf702:w,%d0',4)
    e.label('action_pc_018ad2')
    e.ins('bne.w','action_pc_018ade',4)
    e.label('action_pc_018ad6')
    e.ins('lea.l','0xa550:w,%a0',4)
    e.label('action_pc_018ada')
    e.ins('lea.l','0xa5ce:w,%a1',4)
    e.label('action_pc_018ade')
    e.ins('move.w','(%a0)+,%d1',2)
    e.label('action_pc_018ae0')
    e.ins('bmi.w','action_pc_018afe',4)
    e.label('action_pc_018ae4')
    e.ins('andi.w','#0xff,%d1',4)
    e.label('action_pc_018ae8')
    e.ins('cmp.w','%d0,%d1',2)
    e.label('action_pc_018aea')
    e.ins('bne.b','action_pc_018ade',2)
    e.label('action_pc_018aec')
    e.ins('move.w','(%a0)+,-0x4(%a0)',4)
    e.label('action_pc_018af0')
    e.ins('bpl.b','action_pc_018aec',2)
    e.label('action_pc_018af2')
    e.ins('tst.w','(%a1)+',2)
    e.label('action_pc_018af4')
    e.ins('bpl.b','action_pc_018af2',2)
    e.label('action_pc_018af6')
    e.ins('move.w','%d0,-0x2(%a1)',4)
    e.label('action_pc_018afa')
    e.ins('move.w','#0xffff,(%a1)',4)
    e.label('action_pc_018afe')
    e.ins('rts','',2)

def _lower_detach_defeated_duelist(e,rules):
    e.label('action_pc_018c88')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('action_pc_018c8c')
    e.ins('move.b','#0xff,(%a0, %d0.w)',6)
    e.label('action_pc_018c92')
    e.ins('lea.l','0xa550:w,%a1',4)
    e.label('action_pc_018c96')
    e.ins('cmp.w','0xf702:w,%d0',4)
    e.label('action_pc_018c9a')
    e.ins('beq.w','action_pc_018ca2',4)
    e.label('action_pc_018c9e')
    e.ins('lea.l','0xa5a4:w,%a1',4)
    e.label('action_pc_018ca2')
    e.ins('move.w','(%a1)+,%d1',2)
    e.label('action_pc_018ca4')
    e.ins('andi.w','#0xff,%d1',4)
    e.label('action_pc_018ca8')
    e.ins('cmp.w','%d0,%d1',2)
    e.label('action_pc_018caa')
    e.ins('bne.b','action_pc_018ca2',2)
    e.label('action_pc_018cac')
    e.ins('move.w','(%a1)+,-0x4(%a1)',4)
    e.label('action_pc_018cb0')
    e.ins('bpl.b','action_pc_018cac',2)
    e.label('action_pc_018cb2')
    e.ins('rts','',2)

def _lower_count_selected_deployment(e,rules):
    e.label('action_pc_01b262')
    e.ins('lea.l','0xf500:w,%a1',4)
    e.label('action_pc_01b266')
    e.ins('clr.w','%d7',2)
    e.label('action_pc_01b268')
    e.ins('move.w','(%a1)+,%d0',2)
    e.label('action_pc_01b26a')
    e.ins('bmi.w','action_pc_01b278',4)
    e.label('action_pc_01b26e')
    e.ins('btst.l','#0xe,%d0',4)
    e.label('action_pc_01b272')
    e.ins('beq.b','action_pc_01b268',2)
    e.label('action_pc_01b274')
    e.ins('addq.w','#0x1,%d7',2)
    e.label('action_pc_01b276')
    e.ins('bra.b','action_pc_01b268',2)
    e.label('action_pc_01b278')
    e.ins('rts','',2)

def _lower_initialize_selected_assignment(e,rules):
    e.label('action_pc_01b27a')
    e.ins('lea.l','0xa050:w,%a1',4)
    e.label('action_pc_01b27e')
    e.ins('lea.l','0xf500:w,%a2',4)
    e.label('action_pc_01b282')
    e.ins('lea.l','0xa150:w,%a4',4)
    e.label('action_pc_01b286')
    e.ins('move.b','0x4(%a0),%d0',4)
    e.label('action_pc_01b28a')
    e.ins('lea.l','0xf427:w,%a3',4)
    e.label('action_pc_01b28e')
    e.ins('move.w','0xf392:w,%d1',4)
    e.label('action_pc_01b292')
    e.ins('cmp.b','(%a3, %d1.w),%d0',4)
    e.label('action_pc_01b296')
    e.ins('bne.w','action_pc_01b29e',4)
    e.label('action_pc_01b29a')
    e.ins('bset.l','#0x6,%d1',4)
    e.label('action_pc_01b29e')
    e.ins('move.w','(%a2)+,%d0',2)
    e.label('action_pc_01b2a0')
    e.ins('bmi.w','action_pc_01b2ba',4)
    e.label('action_pc_01b2a4')
    e.ins('btst.l','#0xe,%d0',4)
    e.label('action_pc_01b2a8')
    e.ins('beq.b','action_pc_01b29e',2)
    e.label('action_pc_01b2aa')
    e.ins('andi.w','#0xff,%d0',4)
    e.label('action_pc_01b2ae')
    e.ins('move.b','%d1,(%a1, %d0.w)',4)
    e.label('action_pc_01b2b2')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('action_pc_01b2b4')
    e.ins('clr.l','(%a4, %d0.w)',4)
    e.label('action_pc_01b2b8')
    e.ins('bra.b','action_pc_01b29e',2)
    e.label('action_pc_01b2ba')
    e.ins('rts','',2)

def _lower_selected_troop_weights(e,rules):
    e.label('action_pc_01b40e')
    e.ins('lea.l','0xf500:w,%a1',4)
    e.label('action_pc_01b412')
    e.ins('lea.l','0xc800:w,%a2',4)
    e.label('action_pc_01b416')
    e.ins('moveq','#0,%d5',2)
    e.label('action_pc_01b418')
    e.ins('moveq','#0,%d6',2)
    e.label('action_pc_01b41a')
    e.ins('move.w','(%a1)+,%d2',2)
    e.label('action_pc_01b41c')
    e.ins('bmi.w','action_pc_01b442',4)
    e.label('action_pc_01b420')
    e.ins('move.w','%d2,%d3',2)
    e.label('action_pc_01b422')
    e.ins('lsl.w','#0x2,%d3',2)
    e.label('action_pc_01b424')
    e.ins('btst.l','#0xe,%d2',4)
    e.label('action_pc_01b428')
    e.ins('beq.w','action_pc_01b436',4)
    e.label('action_pc_01b42c')
    e.ins('add.l','(%a2, %d3.w),%d5',4)
    e.label('action_pc_01b430')
    e.ins('addi.l','#0x64,%d5',6)
    e.label('action_pc_01b436')
    e.ins('add.l','(%a2, %d3.w),%d6',4)
    e.label('action_pc_01b43a')
    e.ins('addi.l','#0x64,%d6',6)
    e.label('action_pc_01b440')
    e.ins('bra.b','action_pc_01b41a',2)
    e.label('action_pc_01b442')
    e.ins('lsr.w','#0x5,%d5',2)
    e.label('action_pc_01b444')
    e.ins('lsr.w','#0x5,%d6',2)
    e.label('action_pc_01b446')
    e.ins('rts','',2)

def _lower_refresh_object_attribute_average(e,rules):
    e.label('action_pc_01b4ea')
    e.ins('move.b','(%a0),%d0',2)
    e.label('action_pc_01b4ec')
    e.ins('andi.w','#0xf,%d0',4)
    e.label('action_pc_01b4f0')
    e.ins('move.w','%d0,%d1',2)
    e.label('action_pc_01b4f2')
    e.ins('subi.b','#0x1,%d1',4)
    e.label('action_pc_01b4f6')
    e.ins('lea.l','0xc400:w,%a1',4)
    e.label('action_pc_01b4fa')
    e.ins('moveq','#0,%d2',2)
    e.label('action_pc_01b4fc')
    e.ins('clr.w','%d3',2)
    e.label('action_pc_01b4fe')
    e.ins('move.b','0xd(%a0, %d1.w),%d3',4)
    e.label('action_pc_01b502')
    e.ins('add.b','(%a1, %d3.w),%d2',4)
    e.label('action_pc_01b506')
    e.ins('dbra','%d1,action_pc_01b4fe',4)
    e.label('action_pc_01b50a')
    e.ins('divu.w','%d0,%d2',2)
    e.label('action_pc_01b50c')
    e.ins('move.b','%d2,0x3(%a0)',4)
    e.label('action_pc_01b510')
    e.ins('rts','',2)

def _lower_submit_deployment_queue(e,rules):
    e.label('action_pc_01b512')
    e.ins('move.l','%a0,-(%a7)',2)
    e.label('action_pc_01b514')
    e.ins('cmpi.w','#0x209,0xf612:w',6)
    e.label('action_pc_01b51a')
    e.ins('bne.w','action_pc_01b528',4)
    e.label('action_pc_01b51e')
    e.ins('cmpi.w','#0x5,0xf362:w',6)
    e.label('action_pc_01b524')
    e.ins('beq.w','action_pc_01b574',4)
    e.label('action_pc_01b528')
    e.ins('move.w','0xf392:w,%d0',4)
    e.label('action_pc_01b52c')
    e.ins('lea.l','0xea37:w,%a1',4)
    e.label('action_pc_01b530')
    e.ins('btst.b','#0x1,(%a1, %d0.w)',6)
    e.label('action_pc_01b536')
    e.ins('bne.w','action_pc_01b574',4)
    e.label('action_pc_01b53a')
    e.ins('move.b','#0x2,(%a1, %d0.w)',6)
    e.label('action_pc_01b540')
    e.ins('move.b','0xd(%a0),%d0',4)
    e.label('action_pc_01b544')
    e.ins('lea.l','0xff3000:l,%a1',6)
    e.label('action_pc_01b54a')
    e.ins('adda.w','0xff3826:l,%a1',6)
    e.label('action_pc_01b550')
    e.ins('move.b','#0x0,(%a1)+',4)
    e.label('action_pc_01b554')
    e.ins('move.b','%d0,(%a1)+',2)
    e.label('action_pc_01b556')
    e.ins('move.b','0x3(%a0),(%a1)+',4)
    e.label('action_pc_01b55a')
    e.ins('move.b','#0x80,(%a1)+',4)
    e.label('action_pc_01b55e')
    e.ins('move.b','0xf393:w,(%a1)+',4)
    e.label('action_pc_01b562')
    e.ins('clr.b','(%a1)+',2)
    e.label('action_pc_01b564')
    e.ins('move.b','#0xff,(%a1)',4)
    e.label('action_pc_01b568')
    e.ins('addi.w','#0x6,0xff3826:l',8)
    e.label('action_pc_01b570')
    e.ins('bsr.w','action_pc_01b578',4)
    e.label('action_pc_01b574')
    e.ins('movea.l','(%a7)+,%a0',2)
    e.label('action_pc_01b576')
    e.ins('rts','',2)

def _lower_clear_original_tail_coordinate(e,rules):
    e.label('action_pc_01b578')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('action_pc_01b57c')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('action_pc_01b580')
    e.ins('move.w','#0xff,%d1',4)
    e.label('action_pc_01b584')
    e.ins('lea.l','0xa150:w,%a1',4)
    e.label('action_pc_01b588')
    e.ins('cmp.b','(%a0, %d1.w),%d0',4)
    e.label('action_pc_01b58c')
    e.ins('bne.w','action_pc_01b598',4)
    e.label('action_pc_01b590')
    e.ins('move.w','%d1,%d2',2)
    e.label('action_pc_01b592')
    e.ins('lsl.w','#0x2,%d2',2)
    e.label('action_pc_01b594')
    e.ins('clr.l','(%a1, %d2.w)',4)
    e.label('action_pc_01b598')
    e.ins('dbra','%d1,action_pc_01b598',4)
    e.label('action_pc_01b59c')
    e.ins('rts','',2)

def _lower_build_city_assigned_outcome_candidates(e,rules):
    e.label('action_pc_01c2a0')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('action_pc_01c2a4')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('action_pc_01c2a8')
    e.ins('move.w','#0xff,%d1',4)
    e.label('action_pc_01c2ac')
    e.ins('move.w','0xf68a:w,%d2',4)
    e.label('action_pc_01c2b0')
    e.ins('clr.w','%d3',2)
    e.label('action_pc_01c2b2')
    e.ins('cmp.b','(%a0, %d1.w),%d2',4)
    e.label('action_pc_01c2b6')
    e.ins('bne.w','action_pc_01c2be',4)
    e.label('action_pc_01c2ba')
    e.ins('move.w','%d1,(%a1)+',2)
    e.label('action_pc_01c2bc')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('action_pc_01c2be')
    e.ins('dbra','%d1,action_pc_01c2b2',4)
    e.label('action_pc_01c2c2')
    e.ins('move.w','#0xffff,(%a1)',4)
    e.label('action_pc_01c2c6')
    e.ins('rts','',2)

def _lower_build_battlefield_outcome_candidates(e,rules):
    e.label('action_pc_01c2c8')
    e.ins('lea.l','0xa050:w,%a0',4)
    e.label('action_pc_01c2cc')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('action_pc_01c2d0')
    e.ins('lea.l','0xcc00:w,%a2',4)
    e.label('action_pc_01c2d4')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('action_pc_01c2d8')
    e.ins('move.w','#0xff,%d2',4)
    e.label('action_pc_01c2dc')
    e.ins('clr.w','%d3',2)
    e.label('action_pc_01c2de')
    e.ins('cmp.b','(%a0, %d2.w),%d0',4)
    e.label('action_pc_01c2e2')
    e.ins('bne.w','action_pc_01c2f2',4)
    e.label('action_pc_01c2e6')
    e.ins('tst.b','(%a2, %d2.w)',4)
    e.label('action_pc_01c2ea')
    e.ins('bmi.w','action_pc_01c2f2',4)
    e.label('action_pc_01c2ee')
    e.ins('move.w','%d2,(%a1)+',2)
    e.label('action_pc_01c2f0')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('action_pc_01c2f2')
    e.ins('dbra','%d2,action_pc_01c2de',4)
    e.label('action_pc_01c2f6')
    e.ins('move.w','#0xffff,(%a1)',4)
    e.label('action_pc_01c2fa')
    e.ins('rts','',2)

def _lower_signed_divmod(e,rules):
    e.label('action_pc_035760')
    e.ins('tst.l','%d2',2)
    e.label('action_pc_035762')
    e.ins('bpl.b','action_pc_03576c',2)
    e.label('action_pc_035764')
    e.ins('neg.l','%d2',2)
    e.label('action_pc_035766')
    e.ins('bsr.b','action_pc_03576c',2)
    e.label('action_pc_035768')
    e.ins('neg.l','%d1',2)
    e.label('action_pc_03576a')
    e.ins('rts','',2)

def _lower_positive_denominator(e,rules):
    e.label('action_pc_03576c')
    e.ins('tst.l','%d1',2)
    e.label('action_pc_03576e')
    e.ins('bpl.b','action_pc_03577a',2)
    e.label('action_pc_035770')
    e.ins('neg.l','%d1',2)
    e.label('action_pc_035772')
    e.ins('bsr.b','action_pc_03577a',2)
    e.label('action_pc_035774')
    e.ins('neg.l','%d1',2)
    e.label('action_pc_035776')
    e.ins('neg.l','%d2',2)
    e.label('action_pc_035778')
    e.ins('rts','',2)

def _lower_unsigned_divmod(e,rules):
    e.label('action_pc_03577a')
    e.ins('cmpi.l','#0xffff,%d2',6)
    e.label('action_pc_035780')
    e.ins('bls.b','action_pc_0357da',2)
    e.label('action_pc_035782')
    e.ins('cmp.l','%d1,%d2',2)
    e.label('action_pc_035784')
    e.ins('beq.b','action_pc_03578e',2)
    e.label('action_pc_035786')
    e.ins('bls.b','action_pc_035794',2)
    e.label('action_pc_035788')
    e.ins('move.l','%d1,%d2',2)
    e.label('action_pc_03578a')
    e.ins('moveq','#0,%d1',2)
    e.label('action_pc_03578c')
    e.ins('rts','',2)
    e.label('action_pc_03578e')
    e.ins('moveq','#1,%d1',2)
    e.label('action_pc_035790')
    e.ins('moveq','#0,%d2',2)
    e.label('action_pc_035792')
    e.ins('rts','',2)
    e.label('action_pc_035794')
    e.ins('movem.l','%d3-%d5,-(%a7)',4)
    e.label('action_pc_035798')
    e.ins('move.l','%d2,%d3',2)
    e.label('action_pc_03579a')
    e.ins('clr.w','%d3',2)
    e.label('action_pc_03579c')
    e.ins('swap','%d3',2)
    e.label('action_pc_03579e')
    e.ins('addq.l','#0x1,%d3',2)
    e.label('action_pc_0357a0')
    e.ins('move.l','%d1,%d4',2)
    e.label('action_pc_0357a2')
    e.ins('move.l','%d2,%d5',2)
    e.label('action_pc_0357a4')
    e.ins('move.l','%d3,%d2',2)
    e.label('action_pc_0357a6')
    e.ins('bsr.b','action_pc_0357da',2)
    e.label('action_pc_0357a8')
    e.ins('move.l','%d5,%d2',2)
    e.label('action_pc_0357aa')
    e.ins('divu.w','%d3,%d2',2)
    e.label('action_pc_0357ac')
    e.ins('divu.w','%d2,%d1',2)
    e.label('action_pc_0357ae')
    e.ins('andi.l','#0xffff,%d1',6)
    e.label('action_pc_0357b4')
    e.ins('move.l','%d5,%d2',2)
    e.label('action_pc_0357b6')
    e.ins('move.l','%d5,%d3',2)
    e.label('action_pc_0357b8')
    e.ins('swap','%d3',2)
    e.label('action_pc_0357ba')
    e.ins('mulu.w','%d1,%d2',2)
    e.label('action_pc_0357bc')
    e.ins('mulu.w','%d1,%d3',2)
    e.label('action_pc_0357be')
    e.ins('swap','%d3',2)
    e.label('action_pc_0357c0')
    e.ins('add.l','%d3,%d2',2)
    e.label('action_pc_0357c2')
    e.ins('sub.l','%d4,%d2',2)
    e.label('action_pc_0357c4')
    e.ins('bhi.b','action_pc_0357d0',2)
    e.label('action_pc_0357c6')
    e.ins('neg.l','%d2',2)
    e.label('action_pc_0357c8')
    e.ins('cmp.l','%d2,%d5',2)
    e.label('action_pc_0357ca')
    e.ins('bhi.b','action_pc_0357d4',2)
    e.label('action_pc_0357cc')
    e.ins('addq.l','#0x1,%d1',2)
    e.label('action_pc_0357ce')
    e.ins('bra.b','action_pc_0357b4',2)
    e.label('action_pc_0357d0')
    e.ins('subq.l','#0x1,%d1',2)
    e.label('action_pc_0357d2')
    e.ins('bra.b','action_pc_0357b4',2)
    e.label('action_pc_0357d4')
    e.ins('movem.l','(%a7)+,%d3-%d5',4)
    e.label('action_pc_0357d8')
    e.ins('rts','',2)

def _lower_word_pair_divmod(e,rules):
    e.label('action_pc_0357da')
    e.ins('movem.w','%d1/%d3,-(%a7)',4)
    e.label('action_pc_0357de')
    e.ins('clr.w','%d1',2)
    e.label('action_pc_0357e0')
    e.ins('swap','%d1',2)
    e.label('action_pc_0357e2')
    e.ins('divu.w','%d2,%d1',2)
    e.label('action_pc_0357e4')
    e.ins('move.w','%d1,%d3',2)
    e.label('action_pc_0357e6')
    e.ins('move.w','(%a7)+,%d1',2)
    e.label('action_pc_0357e8')
    e.ins('divu.w','%d2,%d1',2)
    e.label('action_pc_0357ea')
    e.ins('swap','%d1',2)
    e.label('action_pc_0357ec')
    e.ins('moveq','#0,%d2',2)
    e.label('action_pc_0357ee')
    e.ins('move.w','%d1,%d2',2)
    e.label('action_pc_0357f0')
    e.ins('move.w','%d3,%d1',2)
    e.label('action_pc_0357f2')
    e.ins('swap','%d1',2)
    e.label('action_pc_0357f4')
    e.ins('move.w','(%a7)+,%d3',2)
    e.label('action_pc_0357f6')
    e.ins('rts','',2)

def _lower_prepare_message(e,rules):
    e.label('action_pc_0676f2')
    e.ins('tst.w','%d0',2)
    e.label('action_pc_0676f4')
    e.ins('bmi.b','action_pc_067726',2)
    e.label('action_pc_0676f6')
    e.ins('clr.w','0xf652:w',4)
    e.label('action_pc_0676fa')
    e.ins('bsr.w','action_pc_0679d2',4)
    e.label('action_pc_0676fe')
    e.ins('move.l','%a0,0xf3be:w',4)
    e.label('action_pc_067702')
    e.ins('move.w','0xf612:w,0xf3c2:w',6)
    e.label('action_pc_067708')
    e.ins('move.w','0xf362:w,0xf3c4:w',6)
    e.label('action_pc_06770e')
    e.ins('clr.w','0xf36a:w',4)
    e.label('action_pc_067712')
    e.ins('clr.w','0xf3c6:w',4)
    e.label('action_pc_067716')
    e.ins('move.w','#0x28,0xf600:w',6)
    e.label('action_pc_06771c')
    e.ins('bsr.w','action_pc_067728',4)
    e.label('action_pc_067720')
    e.ins('move.w','#0x1,0xefda:w',6)
    e.label('action_pc_067726')
    e.ins('rts','',2)

def _lower_select_message_layout(e,rules):
    e.label('action_pc_067728')
    e.ins('move.w','0xf6c4:w,%d0',4)
    e.label('action_pc_06772c')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('action_pc_06772e')
    e.ins('move.w','12(%pc, %d0.w),0xf612:w',6)
    e.label('action_pc_067734')
    e.ins('move.w','8(%pc, %d0.w),0xf362:w',6)
    e.label('action_pc_06773a')
    e.ins('rts','',2)

def _lower_resolve_message_pointer(e,rules):
    e.label('action_pc_0679d2')
    e.ins('movea.l','0x92c4a:l,%a1',6)
    e.label('action_pc_0679d8')
    e.ins('move.w','%d0,%d1',2)
    e.label('action_pc_0679da')
    e.ins('lsr.w','#0x8,%d1',2)
    e.label('action_pc_0679dc')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('action_pc_0679de')
    e.ins('lea.l','0x92c4e:l,%a0',6)
    e.label('action_pc_0679e4')
    e.ins('move.w','(%a0, %d1.w),%d1',4)
    e.label('action_pc_0679e8')
    e.ins('adda.w','%d1,%a1',2)
    e.label('action_pc_0679ea')
    e.ins('movea.l','(%a1),%a0',2)
    e.label('action_pc_0679ec')
    e.ins('move.w','%d0,%d1',2)
    e.label('action_pc_0679ee')
    e.ins('andi.w','#0xff,%d1',4)
    e.label('action_pc_0679f2')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('action_pc_0679f4')
    e.ins('move.w','0x4(%a1, %d1.w),%d1',4)
    e.label('action_pc_0679f8')
    e.ins('adda.w','%d1,%a0',2)
    e.label('action_pc_0679fa')
    e.ins('rts','',2)

LOWERERS = {
    'build_roster':_lower_build_roster,
    'step_random':_lower_step_random,
    'choose_city_head':_lower_choose_city_head,
    'roster_contains_force_head_carry':_lower_roster_contains_force_head_carry,
    'debit_city_gold':_lower_debit_city_gold,
    'education_factor':_lower_education_factor,
    'commit_mutual_relationship':_lower_commit_mutual_relationship,
    'add_progress_be':_lower_add_progress_be,
    'split_progress':_lower_split_progress,
    'grant_duel_fallback_progress':_lower_grant_duel_fallback_progress,
    'grant_duel_troop_difference_progress':_lower_grant_duel_troop_difference_progress,
    'remove_zero_readiness_duelist':_lower_remove_zero_readiness_duelist,
    'settle_duel_result_roster':_lower_settle_duel_result_roster,
    'transfer_battle_roster':_lower_transfer_battle_roster,
    'detach_defeated_duelist':_lower_detach_defeated_duelist,
    'count_selected_deployment':_lower_count_selected_deployment,
    'initialize_selected_assignment':_lower_initialize_selected_assignment,
    'selected_troop_weights':_lower_selected_troop_weights,
    'refresh_object_attribute_average':_lower_refresh_object_attribute_average,
    'submit_deployment_queue':_lower_submit_deployment_queue,
    'clear_original_tail_coordinate':_lower_clear_original_tail_coordinate,
    'build_city_assigned_outcome_candidates':_lower_build_city_assigned_outcome_candidates,
    'build_battlefield_outcome_candidates':_lower_build_battlefield_outcome_candidates,
    'signed_divmod':_lower_signed_divmod,
    'positive_denominator':_lower_positive_denominator,
    'unsigned_divmod':_lower_unsigned_divmod,
    'word_pair_divmod':_lower_word_pair_divmod,
    'prepare_message':_lower_prepare_message,
    'select_message_layout':_lower_select_message_layout,
    'resolve_message_pointer':_lower_resolve_message_pointer,
}

DECLARATIONS.update({'prepare_scene_message_fields': {'signature': 'state: SceneState, message: Word',
                                  'returns': 'MessagePreparation',
                                  'flow': 'checked_scene_state(state)\n'
                                          'uint(message, 16)\n'
                                          'return _prepare_message_fields(MessageMemory(state), '
                                          'message)'}})


DECLARATIONS.update({'_build_roster_fields': {'signature': 'memory: RosterMemory, city: Word',
                          'returns': 'Word',
                          'flow': 'if type(memory) is not RosterMemory:\n'
                                  "    raise ValueError('sealed live roster endpoint "
                                  "required')\n"
                                  'uint(city, 16)\n'
                                  'assignments = 4294953984\n'
                                  'destination = 4294964480\n'
                                  'count = 0\n'
                                  'head = memory.read(4294964784, 2)\n'
                                  'if not negative_word(head):\n'
                                  '    memory.write(destination, 2, head)\n'
                                  '    destination = u32(destination + 2)\n'
                                  '    count = u16(count + 1)\n'
                                  'for officer in range(256):\n'
                                  '    assigned = memory.read(assignments, 1)\n'
                                  '    assignments = u32(assignments + 1)\n'
                                  '    if assigned == low8(city) and officer != '
                                  'memory.read(4294964784, 2):\n'
                                  '        memory.write(destination, 2, officer)\n'
                                  '        destination = u32(destination + 2)\n'
                                  '        count = u16(count + 1)\n'
                                  'memory.write(destination, 2, 65535)\n'
                                  'return count'},
 'build_scene_roster': {'signature': 'state: SceneState, city: Word',
                        'returns': 'Word',
                        'flow': 'checked_scene_state(state)\n'
                                'return _build_roster_fields(RosterMemory(state), city)'}})


def compile_reuse(source):
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    dependencies = {'prepare_message': ('_prepare_message_fields', '_resolve_message_fields', '_select_message_fields'), 'select_message_layout': ('_select_message_fields',), 'resolve_message_pointer': ('_resolve_message_fields',)}
    for name, phases in dependencies.items():
        records[name]['effects'] = dict(actual_wrapper_ast=records[name]['effects'], actual_shared_phases={phase: records[phase]['effects'] for phase in phases}, actual_scene_return_projection=records['prepare_scene_message']['effects'])
    records['build_roster']['effects'] = dict(actual_wrapper_ast=records['build_roster']['effects'], actual_shared_phase=records['_build_roster_fields']['effects'], actual_scene_wrapper_ast=records['build_scene_roster']['effects'])
    for owner in ('prepare_message', 'select_message_layout', 'resolve_message_pointer'):
        records[owner]['effects'] = dict(previous_partial_projection=records[owner]['effects'], sole_message_frame_fields={name: records[name]['effects'] for name in ('_message_word_fields', '_message_shift_fields', '_message_memory_flags', '_message_address_fields', '_message_call_fields', '_resolve_message_fields', '_select_message_fields', '_prepare_message_fields', 'prepare_scene_message_frame_fields', 'resolve_scene_message_pointer_frame_fields', 'select_scene_message_layout_frame_fields')})
    records['debit_city_gold']['effects'] = dict(actual_legacy_projection=records['debit_city_gold']['effects'], sole_complete_field_core=records['debit_city_gold_frame_fields']['effects'], shared_actual_progress_cap=records['_personnel_progress_cap_fields']['effects'])
    records['education_factor']['effects'] = dict(actual_legacy_projection=records['education_factor']['effects'], sole_complete_field_core=records['education_factor_frame_fields']['effects'], shared_actual_progress_cap=records['_personnel_progress_cap_fields']['effects'])
    records['commit_mutual_relationship']['effects'] = dict(actual_legacy_projection=records['commit_mutual_relationship']['effects'], sole_complete_field_core=records['commit_mutual_relationship_frame_fields']['effects'], shared_actual_progress_cap=records['_personnel_progress_cap_fields']['effects'])
    records['add_progress_be']['effects'] = dict(actual_legacy_projection=records['add_progress_be']['effects'], sole_complete_field_core=records['add_progress_be_frame_fields']['effects'], shared_actual_progress_cap=records['_personnel_progress_cap_fields']['effects'])
    records['split_progress']['effects'] = dict(actual_legacy_projection=records['split_progress']['effects'], sole_complete_field_core=records['split_progress_frame_fields']['effects'], shared_actual_progress_cap=records['_personnel_progress_cap_fields']['effects'])
    return lower_declared({b.name: records[b.name] for b in REUSED_BINDINGS}, REUSED_BINDINGS, LOWERERS)

DECLARATIONS.update({'count_selected_deployment': {'signature': 'state: GameState', 'returns': 'Word', 'flow': 'frame = project_deployment_command_fields(state, 111202)\nreturn u16(frame.choice)'}})

DECLARATIONS.update({'initialize_selected_assignment': {'signature': 'state: GameState, group: Table', 'returns': 'None', 'flow': 'project_deployment_command_fields(state, 111226, group)'}})

DECLARATIONS.update({'selected_troop_weights': {'signature': 'state: GameState', 'returns': 'tuple[Long, Long]', 'flow': 'frame = project_deployment_command_fields(state, 111630)\nreturn (frame.offset_x, frame.offset_y)'}})

DECLARATIONS.update({'refresh_object_attribute_average': {'signature': 'state: GameState, group: Table, divisor: Word', 'returns': 'None', 'flow': 'uint(divisor, 16)\nproject_deployment_command_fields(state, 111850, group)'}})

DECLARATIONS.update({'submit_deployment_queue': {'signature': 'state: GameState, group: Table', 'returns': 'None', 'flow': 'project_deployment_command_fields(state, 111890, group)'}})

DECLARATIONS.update({'clear_original_tail_coordinate': {'signature': 'state: GameState', 'returns': 'None', 'flow': 'project_deployment_command_fields(state, 111992)'}})

APPROVED.setdefault('contexts_logistics', set()).add('project_deployment_command_fields')

DECLARATIONS.update({'_message_word_fields': {'signature': 'memory: MessageMemory, name: str, value: Word', 'returns': 'None', 'flow': 'if memory.frame is not None:\n    memory.observe(_first_word(memory.frame, name, value))'}})

DECLARATIONS.update({'_message_shift_fields': {'signature': 'memory: MessageMemory, name: str, value: Word, amount: int, right: bool=False', 'returns': 'None', 'flow': "if name not in ('target_x', 'target_y') or amount not in (1, 2, 8) or type(right) is not bool:\n    raise ValueError('closed message WORD shift role required')\nif memory.frame is not None:\n    frame = _first_right_word(memory.frame, name, value, amount) if right else _first_shift_word(memory.frame, name, value, amount)\n    memory.observe(frame)"}})

DECLARATIONS.update({'_message_memory_flags': {'signature': 'memory: MessageMemory, value, bits: int=16', 'returns': 'None', 'flow': "uint(value, bits)\nif bits not in (16, 32):\n    raise ValueError('original message WORD/LONG memory width required')\nif memory.frame is not None:\n    status = memory.frame.status & 16 | (8 if value & 1 << bits - 1 else 0) | (4 if value == 0 else 0)\n    memory.observe(first_replace(memory.frame, status=status))"}})

DECLARATIONS.update({'_message_address_fields': {'signature': 'memory: MessageMemory, name: str, address: Long', 'returns': 'None', 'flow': "uint(address, 32)\nif name not in ('roster', 'candidates'):\n    raise ValueError('closed message pointer role required')\nif memory.frame is not None:\n    memory.observe(first_replace(memory.frame, **{name: memory.state.table_at(address).cursor()}))"}})

DECLARATIONS.update({'_message_call_fields': {'signature': 'memory: MessageMemory, target: int, continuation: Long, message: Word=0', 'returns': None, 'flow': "uint(continuation, 32)\nif target not in (424402, 423720):\n    raise ValueError('closed message child required')\nif memory.frame is not None:\n    stack = memory.frame.stack_cursor.advance(-4)\n    stack.set_long(0, continuation)\n    memory.observe(first_replace(memory.frame, stack_cursor=stack))\nresult = _resolve_message_fields(memory, message) if target == 424402 else _select_message_fields(memory)\nif memory.frame is not None:\n    actual = memory.frame.stack_cursor.long()\n    if actual != continuation:\n        raise FirstDeploymentReturnBoundary(actual, memory.frame, continuation)\n    memory.observe(first_replace(memory.frame, stack_cursor=memory.frame.stack_cursor.advance(4)))\nreturn result"}})

DECLARATIONS.update({'_resolve_message_fields': {'signature': 'memory: MessageMemory, message: Word', 'returns': 'MessagePointerFields', 'flow': "uint(message, 16)\nbank = memory.read(601162, 4)\n_message_address_fields(memory, 'candidates', bank)\n_message_word_fields(memory, 'target_y', message)\nbank_high = message >> 8\n_message_shift_fields(memory, 'target_y', message, 8, True)\nbank_offset = u16(bank_high << 1)\n_message_shift_fields(memory, 'target_y', bank_high, 1)\n_message_address_fields(memory, 'roster', 601166)\nbank_delta = memory.read(u32(601166 + s16(bank_offset)), 2)\n_message_word_fields(memory, 'target_y', bank_delta)\ndescriptor = u32(bank + s16(bank_delta))\n_message_address_fields(memory, 'candidates', descriptor)\npointer = memory.read(descriptor, 4)\n_message_address_fields(memory, 'roster', pointer)\n_message_word_fields(memory, 'target_y', message)\nitem_byte = low8(message)\n_message_word_fields(memory, 'target_y', item_byte)\nitem = u16(item_byte << 1)\n_message_shift_fields(memory, 'target_y', item_byte, 1)\nitem_delta = memory.read(u32(descriptor + s16(item) + 4), 2)\n_message_word_fields(memory, 'target_y', item_delta)\npointer = u32(pointer + s16(item_delta))\n_message_address_fields(memory, 'roster', pointer)\nreturn MessagePointerFields(pointer, descriptor, item_delta)"}})

DECLARATIONS.update({'_select_message_fields': {'signature': 'memory: MessageMemory', 'returns': 'Word', 'flow': "layout = memory.read(4294964932, 2)\n_message_word_fields(memory, 'target_x', layout)\noffset = u16(layout << 2)\n_message_shift_fields(memory, 'target_x', layout, 2)\nscene = memory.read(u32(423740 + s16(offset)), 2)\nmemory.write(4294964754, 2, scene)\n_message_memory_flags(memory, scene)\nstage = memory.read(u32(423740 + s16(offset) + 2), 2)\nmemory.write(4294964066, 2, stage)\n_message_memory_flags(memory, stage)\nreturn offset"}})

DECLARATIONS.update({'_prepare_message_fields': {'signature': 'memory: MessageMemory, message: Word', 'returns': 'MessagePreparation', 'flow': 'uint(message, 16)\n_message_memory_flags(memory, message)\nif negative_word(message):\n    return MessagePreparation(None, None, False, False, True, False)\nmemory.read(4294964818, 2)\nmemory.write(4294964818, 2, 0)\n_message_memory_flags(memory, 0)\nresolved = _message_call_fields(memory, 424402, 423678, message)\nmemory.write(4294964158, 4, resolved.pointer)\n_message_memory_flags(memory, resolved.pointer, 32)\nscene = memory.read(4294964754, 2)\nmemory.write(4294964162, 2, scene)\n_message_memory_flags(memory, scene)\nstage = memory.read(4294964066, 2)\nmemory.write(4294964164, 2, stage)\n_message_memory_flags(memory, stage)\nmemory.read(4294964074, 2)\nmemory.write(4294964074, 2, 0)\n_message_memory_flags(memory, 0)\nmemory.read(4294964166, 2)\nmemory.write(4294964166, 2, 0)\n_message_memory_flags(memory, 0)\nmemory.write(4294964736, 2, 40)\n_message_memory_flags(memory, 40)\nlayout_offset = _message_call_fields(memory, 423720, 423712)\nmemory.write(4294963162, 2, 1)\n_message_memory_flags(memory, 1)\nreturn MessagePreparation(resolved, layout_offset, False, False, False, False)'}})

DECLARATIONS.update({'prepare_scene_message_frame_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "checked_scene_state(state)\nif type(frame) is not FirstDeploymentFrame:\n    raise ValueError('complete actual message frame required')\nframe.validate(state, True)\nmemory = MessageMemory(state, frame)\n_prepare_message_fields(memory, low16(frame.target_x))\nreturn memory.frame"}})

DECLARATIONS.update({'resolve_scene_message_pointer_frame_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "checked_scene_state(state)\nif type(frame) is not FirstDeploymentFrame:\n    raise ValueError('complete actual message frame required')\nframe.validate(state, True)\nmemory = MessageMemory(state, frame)\n_resolve_message_fields(memory, low16(frame.target_x))\nreturn memory.frame"}})

DECLARATIONS.update({'select_scene_message_layout_frame_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "checked_scene_state(state)\nif type(frame) is not FirstDeploymentFrame:\n    raise ValueError('complete actual message frame required')\nframe.validate(state, True)\nmemory = MessageMemory(state, frame)\n_select_message_fields(memory)\nreturn memory.frame"}})

APPROVED.setdefault('contexts_first_deployment', set()).update({'FirstDeploymentFrame','FirstDeploymentReturnBoundary','first_replace'})
APPROVED.setdefault('business_formation', set()).update({'_first_word','_first_shift_word','_first_right_word'})

# C58 sole complete fields and compatibility projections; fixed original defaults only.
DECLARATIONS.pop('_add_live_progress',None)
DECLARATIONS.update({'build_roster': {'signature': 'state: GameState, city: Word', 'returns': 'Word', 'flow': 'checked_state(state)\nreturn _build_roster_fields(RosterMemory(state), city)'}, '_build_roster_fields': {'signature': 'memory: RosterMemory, city: Word', 'returns': 'Word', 'flow': "if type(memory) is not RosterMemory:\n    raise ValueError('sealed live roster endpoint required')\nuint(city, 16)\nassignments = 4294953984\ndestination = 4294964480\ncount = 0\nhead = memory.read(4294964784, 2)\nif not negative_word(head):\n    memory.write(destination, 2, head)\n    destination = u32(destination + 2)\n    count = u16(count + 1)\nfor officer in range(256):\n    assigned = memory.read(assignments, 1)\n    assignments = u32(assignments + 1)\n    if assigned == low8(city) and officer != memory.read(4294964784, 2):\n        memory.write(destination, 2, officer)\n        destination = u32(destination + 2)\n        count = u16(count + 1)\nmemory.write(destination, 2, 65535)\nreturn count"}, 'build_scene_roster': {'signature': 'state: SceneState, city: Word', 'returns': 'Word', 'flow': 'checked_scene_state(state)\nreturn _build_roster_fields(RosterMemory(state), city)'}, '_advance_random_pair': {'signature': 'state: GameState', 'returns': 'RandomSample', 'flow': "checked_state(state)\noriginal = state.scalar('random_seed')\nif original == 0:\n    original = 711800410\nmixed = u32(u32(u32(u32(original << 2) + original) << 3) + original)\nsample = replace_word(original, low16(mixed))\nmixed = swap_words(mixed)\nsample = replace_word(sample, u16(low16(sample) + low16(mixed)))\nmixed = swap_words(replace_word(mixed, low16(sample)))\nstate.set_scalar('random_seed', mixed)\nreturn RandomSample(sample, mixed)"}, 'step_random': {'signature': 'state: GameState', 'returns': 'Long', 'flow': 'return _advance_random_pair(state).sample'}, 'choose_city_head': {'signature': 'state: GameState, city: Word', 'returns': 'Word', 'flow': 'checked_state(state)\nuint(city, 16)\nsource = state.candidate_roster.cursor()\nhead = source.next_word()\nif negative_word(head):\n    state.city_owner_bytes.set_byte(city, 255)\n    offset = u16(u16(u16(city << 1) + city) << 2)\n    state.city_orders.set_word(offset, 65535)\n    state.city_orders.set_word(offset, 65535, 4)\n    state.city_orders.set_word(offset, 65535, 8)\nelse:\n    match = roster_contains_force_head_carry(state, city, head)\n    head = match.head\n    if match.carry == 0:\n        head = low8(head)\n        highest = state.officer_status_rating.byte(head)\n        while True:\n            candidate = source.next_word()\n            if negative_word(candidate):\n                break\n            candidate = low8(candidate)\n            rating = state.officer_status_rating.byte(candidate)\n            if rating > highest:\n                head, highest = (candidate, rating)\nstate.city_head_words.set_word(u16(city << 1), head)\nreturn head'}, 'roster_contains_force_head_carry': {'signature': 'state: GameState, city: Word, head: Word', 'returns': 'ForceHeadMatch', 'flow': 'checked_state(state)\nuint(city, 16)\nuint(head, 16)\nowner = state.city_owner_bytes.byte(city)\nforce_head = state.force_heads.word(u16(owner << 1))\nsource = state.candidate_roster.cursor()\nwhile not negative_word(source.word()):\n    if source.next_word() == force_head:\n        return ForceHeadMatch(force_head, state.carry_result(1))\nreturn ForceHeadMatch(head, state.carry_result(0))'}, 'debit_city_gold': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 59146)\nactual = debit_city_gold_frame_fields(memory, entered)\nreturn None'}, 'education_factor': {'signature': 'state: GameState, teacher: Word, target: Word, entry_frame: CommandFrame | None=None', 'returns': 'Word', 'flow': "memory, entered = _personnel_legacy_entry(state, entry_frame, 59166)\nuint(teacher, 16)\nuint(target, 16)\nif teacher != entered.data[0] & 65535 or target != entered.data[1] & 65535:\n    raise ValueError('teacher/target must match actual incoming D0/D1 WORDs')\nactual = education_factor_frame_fields(memory, entered)\nreturn actual.data[2] & 65535"}, 'commit_mutual_relationship': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 60438)\nactual = commit_mutual_relationship_frame_fields(memory, entered)\nreturn None'}, 'add_progress_be': {'signature': 'state: GameState, gain: Word, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': "memory, entered = _personnel_legacy_entry(state, entry_frame, 61280)\nuint(gain, 16)\nif gain != entered.data[2] & 65535:\n    raise ValueError('compatibility score/gain must match real incoming D2')\nactual = add_progress_be_frame_fields(memory, entered)\nreturn None"}, 'split_progress': {'signature': 'state: GameState, gain: Long, entry_frame: CommandFrame | None=None', 'returns': 'Word', 'flow': "memory, entered = _personnel_legacy_entry(state, entry_frame, 63888)\nuint(gain, 32)\nif gain != entered.data[2]:\n    raise ValueError('compatibility score/gain must match real incoming D2')\nactual = split_progress_frame_fields(memory, entered)\nreturn actual.data[2] & 65535"}, 'grant_duel_fallback_progress': {'signature': 'state: GameState, receiver_offset: Word, donor: Word, progress: Table', 'returns': 'Long', 'flow': "checked_state(state)\nuint(receiver_offset, 16)\nuint(donor, 16)\nchecked_table(progress, state)\ndonor_offset = u16(donor << 1)\nraw = progress.word(donor_offset)\ngain = divu_retained(u32(s16(raw)), 40)\ndonor = donor_offset >> 1\nscene_offset = u16(state.scalar('battle_scene') << 1)\nif donor == state.city_head_words.word(scene_offset):\n    gain = replace_word(gain, u16(low16(gain) + 30))\nelif donor == state.alternate_heads.word(scene_offset):\n    gain = replace_word(gain, u16(low16(gain) + 30))\nif state.officer_status.byte(donor) & 16:\n    gain = replace_word(gain, u16(low16(gain) + 20))\nupdated = u16(progress.word(receiver_offset) + low16(gain))\nif updated > 999:\n    updated = 999\nprogress.set_word(receiver_offset, updated)\nreturn gain"}, 'grant_duel_troop_difference_progress': {'signature': 'state: GameState, receiver: Word, troop_difference: Long, progress: Table', 'returns': 'Long', 'flow': 'checked_state(state)\nuint(receiver, 16)\nuint(troop_difference, 32)\nchecked_table(progress, state)\ngain = divu_retained(low16(troop_difference), 100)\noffset = u16(receiver << 1)\nupdated = u16(progress.word(offset) + low16(gain))\nif updated > 999:\n    updated = 999\nprogress.set_word(offset, updated)\nreturn gain'}, '_active_duel_roster': {'signature': 'state: GameState, officer: Word', 'returns': None, 'flow': "if officer == state.scalar('roster_side_owner'):\n    return state.battle_primary_roster.cursor()\nreturn state.battle_secondary_roster.cursor()"}, '_compact_after_match': {'signature': 'source', 'returns': None, 'flow': 'while True:\n    member = source.next_word()\n    source.set_word(0, member, -4)\n    if negative_word(member):\n        return'}, 'remove_zero_readiness_duelist': {'signature': 'state: GameState, officer: Word', 'returns': 'None', 'flow': "checked_state(state)\nuint(officer, 16)\nif state.scalar('battle_active') == 0:\n    return\nstate.officer_city_assignment.set_byte(officer, 255)\nsource = _active_duel_roster(state, officer)\nwhile True:\n    member = source.next_word()\n    if negative_word(member):\n        return\n    if low8(member) == officer:\n        break\n_compact_after_match(source)"}, 'settle_duel_result_roster': {'signature': 'state: GameState', 'returns': 'None', 'flow': "checked_state(state)\nif state.scalar('battle_active') == 0:\n    return\nresult = state.scalar('duel_result')\nif result < 6:\n    return\nif result == 6:\n    transfer_battle_roster(state, state.scalar('duel_primary_officer'))\nelse:\n    transfer_battle_roster(state, state.scalar('duel_secondary_officer'))"}, 'transfer_battle_roster': {'signature': 'state: GameState, officer: Word', 'returns': 'None', 'flow': "checked_state(state)\nuint(officer, 16)\nsource = state.battle_secondary_roster.cursor()\ndestination = state.battle_secondary_retired_roster.cursor()\nif officer == state.scalar('roster_side_owner'):\n    source = state.battle_primary_roster.cursor()\n    destination = state.battle_primary_retired_roster.cursor()\nwhile True:\n    member = source.next_word()\n    if negative_word(member):\n        return\n    if low8(member) == officer:\n        break\n_compact_after_match(source)\nwhile not negative_word(destination.next_word()):\n    pass\ndestination.set_word(0, officer, -2)\ndestination.put_word(65535)"}, 'detach_defeated_duelist': {'signature': 'state: GameState, officer: Word', 'returns': 'None', 'flow': 'checked_state(state)\nuint(officer, 16)\nstate.officer_city_assignment.set_byte(officer, 255)\nsource = _active_duel_roster(state, officer)\nwhile low8(source.next_word()) != officer:\n    pass\n_compact_after_match(source)'}, 'count_selected_deployment': {'signature': 'state: GameState', 'returns': 'Word', 'flow': 'frame = project_deployment_command_fields(state, 111202)\nreturn u16(frame.choice)'}, 'initialize_selected_assignment': {'signature': 'state: GameState, group: Table', 'returns': 'None', 'flow': 'project_deployment_command_fields(state, 111226, group)'}, 'selected_troop_weights': {'signature': 'state: GameState', 'returns': 'tuple[Long, Long]', 'flow': 'frame = project_deployment_command_fields(state, 111630)\nreturn (frame.offset_x, frame.offset_y)'}, 'refresh_object_attribute_average': {'signature': 'state: GameState, group: Table, divisor: Word', 'returns': 'None', 'flow': 'uint(divisor, 16)\nproject_deployment_command_fields(state, 111850, group)'}, 'submit_deployment_queue': {'signature': 'state: GameState, group: Table', 'returns': 'None', 'flow': 'project_deployment_command_fields(state, 111890, group)'}, 'clear_original_tail_coordinate': {'signature': 'state: GameState', 'returns': 'None', 'flow': 'project_deployment_command_fields(state, 111992)'}, 'build_city_assigned_outcome_candidates': {'signature': 'state: GameState', 'returns': 'Word', 'flow': "checked_state(state)\ndestination = state.action_candidates.cursor()\ncity = state.scalar('battle_scene')\ncount = 0\nfor officer in descending_inclusive(255):\n    if state.officer_city_assignment.byte(officer) == low8(city):\n        destination.append_word(officer)\n        count = u16(count + 1)\ndestination.put_word(65535)\nreturn count"}, 'build_battlefield_outcome_candidates': {'signature': 'state: GameState', 'returns': 'Word', 'flow': "checked_state(state)\ndestination = state.action_candidates.cursor()\ncity = state.scalar('battle_scene')\ncount = 0\nfor officer in descending_inclusive(255):\n    if state.battlefield_city_assignment.byte(officer) == low8(city):\n        if not negative_byte(state.officer_city_assignment.byte(officer)):\n            destination.append_word(officer)\n            count = u16(count + 1)\ndestination.put_word(65535)\nreturn count"}, 'signed_divmod': {'signature': 'state: GameState, numerator: Long, denominator: Long', 'returns': 'tuple[Long, Long]', 'flow': 'checked_state(state)\nuint(numerator, 32)\nuint(denominator, 32)\nif negative_long(denominator):\n    quotient, remainder = positive_denominator(state, numerator, u32(-denominator))\n    return (u32(-quotient), remainder)\nreturn positive_denominator(state, numerator, denominator)'}, 'positive_denominator': {'signature': 'state: GameState, numerator: Long, denominator: Long', 'returns': 'tuple[Long, Long]', 'flow': 'checked_state(state)\nuint(numerator, 32)\nuint(denominator, 32)\nif negative_long(numerator):\n    quotient, remainder = unsigned_divmod(state, u32(-numerator), denominator)\n    return (u32(-quotient), u32(-remainder))\nreturn unsigned_divmod(state, numerator, denominator)'}, 'unsigned_divmod': {'signature': 'state: GameState, numerator: Long, denominator: Long', 'returns': 'tuple[Long, Long]', 'flow': 'checked_state(state)\nuint(numerator, 32)\nuint(denominator, 32)\nif denominator <= 65535:\n    return word_pair_divmod(state, numerator, denominator)\nif denominator == numerator:\n    return (1, 0)\nif denominator > numerator:\n    return (0, numerator)\ndivisor_high = u32(high16(denominator) + 1)\nquotient, remainder = word_pair_divmod(state, numerator, divisor_high)\ndenominator_part = divu_retained(denominator, low16(divisor_high))\nquotient = low16(divu_retained(quotient, low16(denominator_part)))\nwhile True:\n    product = u32(low16(denominator) * low16(quotient))\n    upper_product = u32(high16(denominator) * low16(quotient))\n    product = u32(product + swap_words(upper_product))\n    if product > numerator:\n        quotient = u32(quotient - 1)\n        continue\n    remainder = u32(numerator - product)\n    if denominator <= remainder:\n        quotient = u32(quotient + 1)\n        continue\n    return (quotient, remainder)'}, 'word_pair_divmod': {'signature': 'state: GameState, numerator: Long, denominator: Long', 'returns': 'tuple[Long, Long]', 'flow': 'checked_state(state)\nuint(numerator, 32)\nuint(denominator, 32)\ndivisor = low16(denominator)\nupper_division = divu_retained(high16(numerator), divisor)\nupper_quotient = low16(upper_division)\nlower_dividend = u32(high16(upper_division) << 16 | low16(numerator))\nlower_division = divu_retained(lower_dividend, divisor)\nreturn (u32(upper_quotient << 16 | low16(lower_division)), high16(lower_division))'}, '_resolve_message_fields': {'signature': 'memory: MessageMemory, message: Word', 'returns': 'MessagePointerFields', 'flow': "uint(message, 16)\nbank = memory.read(601162, 4)\n_message_address_fields(memory, 'candidates', bank)\n_message_word_fields(memory, 'target_y', message)\nbank_high = message >> 8\n_message_shift_fields(memory, 'target_y', message, 8, True)\nbank_offset = u16(bank_high << 1)\n_message_shift_fields(memory, 'target_y', bank_high, 1)\n_message_address_fields(memory, 'roster', 601166)\nbank_delta = memory.read(u32(601166 + s16(bank_offset)), 2)\n_message_word_fields(memory, 'target_y', bank_delta)\ndescriptor = u32(bank + s16(bank_delta))\n_message_address_fields(memory, 'candidates', descriptor)\npointer = memory.read(descriptor, 4)\n_message_address_fields(memory, 'roster', pointer)\n_message_word_fields(memory, 'target_y', message)\nitem_byte = low8(message)\n_message_word_fields(memory, 'target_y', item_byte)\nitem = u16(item_byte << 1)\n_message_shift_fields(memory, 'target_y', item_byte, 1)\nitem_delta = memory.read(u32(descriptor + s16(item) + 4), 2)\n_message_word_fields(memory, 'target_y', item_delta)\npointer = u32(pointer + s16(item_delta))\n_message_address_fields(memory, 'roster', pointer)\nreturn MessagePointerFields(pointer, descriptor, item_delta)"}, '_select_message_fields': {'signature': 'memory: MessageMemory', 'returns': 'Word', 'flow': "layout = memory.read(4294964932, 2)\n_message_word_fields(memory, 'target_x', layout)\noffset = u16(layout << 2)\n_message_shift_fields(memory, 'target_x', layout, 2)\nscene = memory.read(u32(423740 + s16(offset)), 2)\nmemory.write(4294964754, 2, scene)\n_message_memory_flags(memory, scene)\nstage = memory.read(u32(423740 + s16(offset) + 2), 2)\nmemory.write(4294964066, 2, stage)\n_message_memory_flags(memory, stage)\nreturn offset"}, '_prepare_message_fields': {'signature': 'memory: MessageMemory, message: Word', 'returns': 'MessagePreparation', 'flow': 'uint(message, 16)\n_message_memory_flags(memory, message)\nif negative_word(message):\n    return MessagePreparation(None, None, False, False, True, False)\nmemory.read(4294964818, 2)\nmemory.write(4294964818, 2, 0)\n_message_memory_flags(memory, 0)\nresolved = _message_call_fields(memory, 424402, 423678, message)\nmemory.write(4294964158, 4, resolved.pointer)\n_message_memory_flags(memory, resolved.pointer, 32)\nscene = memory.read(4294964754, 2)\nmemory.write(4294964162, 2, scene)\n_message_memory_flags(memory, scene)\nstage = memory.read(4294964066, 2)\nmemory.write(4294964164, 2, stage)\n_message_memory_flags(memory, stage)\nmemory.read(4294964074, 2)\nmemory.write(4294964074, 2, 0)\n_message_memory_flags(memory, 0)\nmemory.read(4294964166, 2)\nmemory.write(4294964166, 2, 0)\n_message_memory_flags(memory, 0)\nmemory.write(4294964736, 2, 40)\n_message_memory_flags(memory, 40)\nlayout_offset = _message_call_fields(memory, 423720, 423712)\nmemory.write(4294963162, 2, 1)\n_message_memory_flags(memory, 1)\nreturn MessagePreparation(resolved, layout_offset, False, False, False, False)'}, 'prepare_message': {'signature': 'state: GameState, message: Word', 'returns': 'None', 'flow': 'checked_state(state)\n_prepare_message_fields(MessageMemory(state), message)'}, 'select_message_layout': {'signature': 'state: GameState', 'returns': 'None', 'flow': 'checked_state(state)\n_select_message_fields(MessageMemory(state))'}, 'resolve_message_pointer': {'signature': 'state: GameState, message: Word', 'returns': 'Table', 'flow': 'checked_state(state)\nresolved = _resolve_message_fields(MessageMemory(state), message)\nreturn state.table(resolved.pointer)'}, 'prepare_scene_message': {'signature': 'state: SceneState, inputs: SceneMessageInput', 'returns': 'SceneMessageResult', 'flow': "checked_scene_state(state)\nif type(inputs) is not SceneMessageInput:\n    raise ValueError('explicit scene message input required')\ninputs.validate(state)\nobserved = _prepare_message_fields(MessageMemory(state), low16(inputs.value))\nif observed.resolved is None:\n    destination = inputs.destination\n    source = inputs.source\n    value = inputs.value\n    field = inputs.field\nelse:\n    destination = state.table_at(observed.resolved.pointer)\n    source = state.table_at(observed.resolved.descriptor)\n    value = replace_word(inputs.value, observed.layout_offset)\n    field = replace_word(inputs.field, observed.resolved.item_offset)\nresult = SceneMessageResult(destination, source, value, field, observed.carry, observed.zero, observed.negative, observed.overflow)\nreturn result.validate(state)"}, 'prepare_scene_message_fields': {'signature': 'state: SceneState, message: Word', 'returns': 'MessagePreparation', 'flow': 'checked_scene_state(state)\nuint(message, 16)\nreturn _prepare_message_fields(MessageMemory(state), message)'}, '_message_word_fields': {'signature': 'memory: MessageMemory, name: str, value: Word', 'returns': 'None', 'flow': 'if memory.frame is not None:\n    memory.observe(_first_word(memory.frame, name, value))'}, '_message_shift_fields': {'signature': 'memory: MessageMemory, name: str, value: Word, amount: int, right: bool=False', 'returns': 'None', 'flow': "if name not in ('target_x', 'target_y') or amount not in (1, 2, 8) or type(right) is not bool:\n    raise ValueError('closed message WORD shift role required')\nif memory.frame is not None:\n    frame = _first_right_word(memory.frame, name, value, amount) if right else _first_shift_word(memory.frame, name, value, amount)\n    memory.observe(frame)"}, '_message_memory_flags': {'signature': 'memory: MessageMemory, value, bits: int=16', 'returns': 'None', 'flow': "uint(value, bits)\nif bits not in (16, 32):\n    raise ValueError('original message WORD/LONG memory width required')\nif memory.frame is not None:\n    status = memory.frame.status & 16 | (8 if value & 1 << bits - 1 else 0) | (4 if value == 0 else 0)\n    memory.observe(first_replace(memory.frame, status=status))"}, '_message_address_fields': {'signature': 'memory: MessageMemory, name: str, address: Long', 'returns': 'None', 'flow': "uint(address, 32)\nif name not in ('roster', 'candidates'):\n    raise ValueError('closed message pointer role required')\nif memory.frame is not None:\n    memory.observe(first_replace(memory.frame, **{name: memory.state.table_at(address).cursor()}))"}, '_message_call_fields': {'signature': 'memory: MessageMemory, target: int, continuation: Long, message: Word=0', 'returns': None, 'flow': "uint(continuation, 32)\nif target not in (424402, 423720):\n    raise ValueError('closed message child required')\nif memory.frame is not None:\n    stack = memory.frame.stack_cursor.advance(-4)\n    stack.set_long(0, continuation)\n    memory.observe(first_replace(memory.frame, stack_cursor=stack))\nresult = _resolve_message_fields(memory, message) if target == 424402 else _select_message_fields(memory)\nif memory.frame is not None:\n    actual = memory.frame.stack_cursor.long()\n    if actual != continuation:\n        raise FirstDeploymentReturnBoundary(actual, memory.frame, continuation)\n    memory.observe(first_replace(memory.frame, stack_cursor=memory.frame.stack_cursor.advance(4)))\nreturn result"}, 'prepare_scene_message_frame_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "checked_scene_state(state)\nif type(frame) is not FirstDeploymentFrame:\n    raise ValueError('complete actual message frame required')\nframe.validate(state, True)\nmemory = MessageMemory(state, frame)\n_prepare_message_fields(memory, low16(frame.target_x))\nreturn memory.frame"}, 'resolve_scene_message_pointer_frame_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "checked_scene_state(state)\nif type(frame) is not FirstDeploymentFrame:\n    raise ValueError('complete actual message frame required')\nframe.validate(state, True)\nmemory = MessageMemory(state, frame)\n_resolve_message_fields(memory, low16(frame.target_x))\nreturn memory.frame"}, 'select_scene_message_layout_frame_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "checked_scene_state(state)\nif type(frame) is not FirstDeploymentFrame:\n    raise ValueError('complete actual message frame required')\nframe.validate(state, True)\nmemory = MessageMemory(state, frame)\n_select_message_fields(memory)\nreturn memory.frame"}, 'debit_city_gold_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_read_fields(memory, frame, 0, 4294964114)\nframe = _personnel_shift_fields(memory, frame, 0, 2)\nframe = frame.with_address(0, 4294959100)\nframe = _personnel_read_fields(memory, frame, 1, 4294964126, 32)\nframe = _personnel_memory_arithmetic_fields(memory, frame, _personnel_indexed_address(frame, 0, 0), frame.data[1], 32, True)\nreturn memory.finish(frame)'}, 'education_factor_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_load_fields(memory, frame, 3, 0)\nfor threshold, row in ((20, 5), (40, 10), (60, 15), (80, 20)):\n    frame = _personnel_compare_fields(memory, frame, frame.data[1] & 65535, threshold)\n    if frame.status_word & 1:\n        break\n    frame = _personnel_load_fields(memory, frame, 3, row)\nfor threshold in (20, 40, 60, 80):\n    frame = _personnel_compare_fields(memory, frame, frame.data[0] & 65535, threshold)\n    if frame.status_word & 1:\n        break\n    frame = _personnel_arithmetic_fields(memory, frame, 3, 1)\nframe = frame.with_address(0, 59254)\nframe = _personnel_read_fields(memory, frame, 2, _personnel_indexed_address(frame, 0, 3), 8)\nframe = _personnel_ext_word_fields(memory, frame, 2)\nreturn memory.finish(frame)'}, 'commit_mutual_relationship_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_read_fields(memory, frame, 0, 4294964192)\nframe = _personnel_shift_fields(memory, frame, 0, 1)\nframe = frame.with_address(0, 4294960944)\nframe = _personnel_read_fields(memory, frame, 1, _personnel_indexed_address(frame, 0, 0))\nframe = _personnel_read_fields(memory, frame, 0, 4294964086)\nframe = _personnel_shift_fields(memory, frame, 0, 1)\nframe = frame.with_address(0, 4294960912)\nframe = _personnel_read_fields(memory, frame, 2, _personnel_indexed_address(frame, 0, 0))\nframe = _personnel_bit_set_fields(memory, frame, 2, frame.data[1])\nframe = _personnel_store_fields(memory, frame, _personnel_indexed_address(frame, 0, 0), frame.data[2] & 65535)\nframe = _personnel_read_fields(memory, frame, 0, 4294964192)\nframe = _personnel_shift_fields(memory, frame, 0, 1)\nframe = frame.with_address(0, 4294960944)\nframe = _personnel_read_fields(memory, frame, 0, _personnel_indexed_address(frame, 0, 0))\nframe = _personnel_shift_fields(memory, frame, 0, 1)\nframe = _personnel_read_fields(memory, frame, 1, 4294964086)\nframe = frame.with_address(0, 4294960912)\nframe = _personnel_read_fields(memory, frame, 2, _personnel_indexed_address(frame, 0, 0))\nframe = _personnel_bit_set_fields(memory, frame, 2, frame.data[1])\nframe = _personnel_store_fields(memory, frame, _personnel_indexed_address(frame, 0, 0), frame.data[2] & 65535)\nreturn memory.finish(frame)'}, '_personnel_progress_cap_fields': {'signature': 'memory, frame, address, gain', 'returns': None, 'flow': 'frame = _personnel_memory_arithmetic_fields(memory, frame, address, gain)\nvalue = memory.state.read(address, 2)\nframe = _personnel_compare_fields(memory, frame, value, 999)\nif not frame.status_word & 5:\n    frame = _personnel_store_fields(memory, frame, address, 999)\nreturn frame'}, 'add_progress_be_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_read_fields(memory, frame, 0, 4294964134)\nframe = _personnel_shift_fields(memory, frame, 0, 1)\nframe = frame.with_address(0, 4294950400)\nframe = _personnel_progress_cap_fields(memory, frame, _personnel_indexed_address(frame, 0, 0), frame.data[2] & 65535)\nreturn memory.finish(frame)'}, 'split_progress_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_read_fields(memory, frame, 0, 4294964134)\nframe = _personnel_shift_fields(memory, frame, 0, 1)\nframe = _personnel_and_fields(memory, frame, 2, 65535, 32)\nframe = _personnel_quotient_fields(memory, frame, 2, 10, 63900)\nframe = frame.with_address(0, 4294950400)\nframe = _personnel_progress_cap_fields(memory, frame, _personnel_indexed_address(frame, 0, 0), frame.data[2] & 65535)\nframe = _personnel_shift_fields(memory, frame, 2, 1, 16, True)\nframe = frame.with_address(0, 4294950912)\nframe = _personnel_progress_cap_fields(memory, frame, _personnel_indexed_address(frame, 0, 0), frame.data[2] & 65535)\nreturn memory.finish(frame)'}})
APPROVED.setdefault('contexts_personnel',set()).update(['CommandFrame', 'FirstDeploymentFrame', 'FirstDeploymentReturnBoundary', 'PersonnelMemory', '_first_right_word', '_first_shift_word', '_first_word', '_personnel_and_fields', '_personnel_arithmetic_fields', '_personnel_bit_set_fields', '_personnel_compare_fields', '_personnel_ext_word_fields', '_personnel_indexed_address', '_personnel_legacy_entry', '_personnel_load_fields', '_personnel_memory_arithmetic_fields', '_personnel_quotient_fields', '_personnel_read_fields', '_personnel_shift_fields', '_personnel_store_fields', 'first_replace'])
APPROVED.setdefault('domain',set()).update({'Boundary'})
