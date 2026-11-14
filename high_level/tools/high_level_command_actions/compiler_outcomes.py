"""Draft restricted outcomes semantic AST admission and ordinary target emission.

Business rules remain separate. Generation reads explicit source text only.
Not an arbitrary Python compiler or an independent behavior acceptance.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import OUTCOMES_BINDINGS

APPROVED = {'business_reuse': {'build_battlefield_outcome_candidates',
                    'build_city_assigned_outcome_candidates',
                    'detach_defeated_duelist',
                    'grant_duel_fallback_progress',
                    'grant_duel_troop_difference_progress',
                    'remove_zero_readiness_duelist',
                    'settle_duel_result_roster',
                    'signed_divmod'},
 'contexts_outcomes': {'DuelDispositionContext',
                       'DuelSettlementContext',
                       'DuelSettlementResult',
                       'checked_context'},
 'domain': {'CarryOutcome',
            'Cursor',
            'GameState',
            'Long',
            'Table',
            'Word',
            'checked_state',
            'divu_retained',
            'high16',
            'low16',
            'negative_word',
            'replace_byte',
            'replace_word',
            'swap_words',
            'u16',
            'u32',
            'uint'}}

DECLARATIONS = {'_multiply_word_parts': {'signature': 'value: Long, factor: Word',
                          'returns': 'Long',
                          'flow': 'return u32(low16(value) * factor + swap_words(high16(value) * '
                                  'factor))'},
 '_random_fraction': {'signature': 'state: GameState, span: Word, base: Word=0',
                      'returns': 'Word',
                      'flow': 'sample = low16(state.sample_random())\n'
                              'return u16(high16(u32(sample * span)) + base)'},
 '_duel_training_loss': {'signature': 'state: GameState, carrier: Long',
                         'returns': 'Long',
                         'flow': 'sample = low16(state.sample_random())\n'
                                 'doubled = u32(sample << 1)\n'
                                 'scaled = replace_word(doubled, u16(low16(doubled) + sample))\n'
                                 'loss = u16(high16(scaled) + 1)\n'
                                 'previous = low16(carrier)\n'
                                 'return replace_word(carrier, 0 if previous < loss else '
                                 'u16(previous - loss))'},
 'settle_duel_training_and_troops': {'signature': 'state: GameState, context: '
                                                  'DuelSettlementContext',
                                     'returns': 'DuelSettlementResult',
                                     'flow': 'state = checked_state(state)\n'
                                             'context = checked_context(context, '
                                             'DuelSettlementContext)\n'
                                             'progress = state.officer_word_c000\n'
                                             "first = state.scalar('duel_primary_officer')\n"
                                             'carrier = replace_byte(context.training_carrier, '
                                             "state.scalar('duel_training_primary'))\n"
                                             "if state.scalar('duel_result') == 4:\n"
                                             '    carrier = _duel_training_loss(state, carrier)\n'
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
                                             '    carrier = _duel_training_loss(state, carrier)\n'
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
 'settle_duel_packets': {'signature': 'state: GameState, context: DuelSettlementContext',
                         'returns': 'CarryOutcome',
                         'flow': 'state = checked_state(state)\n'
                                 'context = checked_context(context, DuelSettlementContext)\n'
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
 '_seek_officer_unbounded': {'signature': 'source: Cursor, officer: Word',
                             'returns': 'None',
                             'flow': 'while source.next_word() & 255 != officer:\n    pass'},
 '_compact_live_roster': {'signature': 'source: Cursor',
                          'returns': 'None',
                          'flow': 'while True:\n'
                                  '    member = source.next_word()\n'
                                  '    source.set_word(0, member, -4)\n'
                                  '    if negative_word(member):\n'
                                  '        return'},
 '_append_at_roster_end': {'signature': 'destination: Cursor, officer: Word',
                           'returns': 'None',
                           'flow': 'while not negative_word(destination.next_word()):\n'
                                   '    pass\n'
                                   'destination.set_word(0, officer, -2)\n'
                                   'destination.put_word(65535)'},
 'apply_duel_disposition': {'signature': 'state: GameState, context: DuelDispositionContext',
                            'returns': 'None',
                            'flow': 'state = checked_state(state)\n'
                                    'context = checked_context(context, DuelDispositionContext)\n'
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
                                    '    _append_at_roster_end(retired, officer)\n'
                                    '    _seek_officer_unbounded(active, officer)\n'
                                    '    _compact_live_roster(active)\n'
                                    'elif disposition == 2:\n'
                                    "    if officer == state.scalar('roster_side_owner'):\n"
                                    '        active = state.battle_primary_roster.cursor()\n'
                                    '        retired = '
                                    'state.battle_primary_retired_roster.cursor()\n'
                                    '    else:\n'
                                    '        active = state.battle_secondary_roster.cursor()\n'
                                    '        retired = '
                                    'state.battle_secondary_retired_roster.cursor()\n'
                                    '    _seek_officer_unbounded(active, officer)\n'
                                    '    _compact_live_roster(active)\n'
                                    '    _append_at_roster_end(retired, officer)'},
 'detach_zero_readiness_duelists': {'signature': 'state: GameState',
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
 '_candidate_strength_totals': {'signature': 'state: GameState',
                                'returns': 'tuple[Long, Word, Word]',
                                'flow': 'source = state.action_candidates.cursor()\n'
                                        'troops, first_attribute, second_attribute = (0, 0, 0)\n'
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
 'compute_outcome_force_ratio': {'signature': 'state: GameState',
                                 'returns': 'Word',
                                 'flow': 'state = checked_state(state)\n'
                                         'random_factor = _random_fraction(state, 6, 10)\n'
                                         'build_city_assigned_outcome_candidates(state)\n'
                                         'troops, first_attribute, second_attribute = '
                                         '_candidate_strength_totals(state)\n'
                                         'troops = replace_word(troops, u16(low16(troops) + 1)) >> '
                                         '5\n'
                                         'first_factor = u16((first_attribute >> 3) + 1)\n'
                                         'second_factor = u16((second_attribute >> 3) + 1)\n'
                                         'numerator = _multiply_word_parts(troops, first_factor)\n'
                                         'numerator = _multiply_word_parts(numerator, '
                                         'second_factor)\n'
                                         'numerator = _multiply_word_parts(numerator, '
                                         'random_factor)\n'
                                         'build_battlefield_outcome_candidates(state)\n'
                                         'troops, first_attribute, second_attribute = '
                                         '_candidate_strength_totals(state)\n'
                                         'troops >>= 5\n'
                                         'troops = replace_word(troops, u16(low16(troops) + 1))\n'
                                         'first_factor = u16((first_attribute >> 3) + 1)\n'
                                         'second_factor = u16((second_attribute >> 3) + 1)\n'
                                         'denominator = _multiply_word_parts(troops, '
                                         'first_factor)\n'
                                         'denominator = _multiply_word_parts(denominator, '
                                         'first_factor)\n'
                                         'quotient, remainder = signed_divmod(state, numerator, '
                                         'denominator)\n'
                                         'ratio = low16(quotient)\n'
                                         "state.set_scalar('outcome_ratio', ratio)\n"
                                         'return ratio'},
 'apply_battlefield_ratio_losses': {'signature': 'state: GameState',
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
                                            '    factor = _random_fraction(state, 40, 30)\n'
                                            '    scaled_factor = u32(factor * '
                                            "state.scalar('outcome_ratio'))\n"
                                            '    loss = '
                                            'divu_retained(_multiply_word_parts(scaled_factor, '
                                            'low16(troops)), 1000)\n'
                                            '    remaining = u16(low16(troops) - low16(loss))\n'
                                            '    state.officer_troops.set_word(troop_offset, '
                                            'remaining, 2)\n'
                                            '    points = u16(points + '
                                            'low16(divu_retained(low16(loss), 400)))\n'
                                            '    readiness_offset = troop_offset >> 1\n'
                                            '    readiness = '
                                            'state.officer_readiness.word(readiness_offset)\n'
                                            '    percent = _random_fraction(state, 30)\n'
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
 '_low_readiness_progress': {'signature': 'state: GameState, readiness_offset: Word, '
                                          'check_city_head: bool, detach: bool',
                             'returns': 'Word',
                             'flow': 'progress = state.officer_word_c000.word(readiness_offset)\n'
                                     'value = divu_retained(progress, 5)\n'
                                     'officer = readiness_offset >> 1\n'
                                     'if check_city_head:\n'
                                     "    scene_offset = u16(state.scalar('battle_scene') << 1)\n"
                                     '    if officer == state.city_head_words.word(scene_offset):\n'
                                     '        value = replace_word(value, u16(low16(value) + 30))\n'
                                     'if detach:\n'
                                     '    state.officer_city_assignment.set_byte(officer, 255)\n'
                                     'if state.officer_status.byte(officer) & 16:\n'
                                     '    value = replace_word(value, u16(low16(value) + 20))\n'
                                     'return low16(value)'},
 'apply_city_assigned_heavy_losses': {'signature': 'state: GameState',
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
                                              '    factor = _random_fraction(state, 40, 50)\n'
                                              '    loss = divu_retained(u32(factor * '
                                              'low16(troops)), 100)\n'
                                              '    state.officer_troops.set_word(troop_offset, '
                                              'u16(low16(troops) - low16(loss)), 2)\n'
                                              '    points = u16(points + '
                                              'low16(divu_retained(low16(loss), 400)))\n'
                                              '    readiness_offset = troop_offset >> 1\n'
                                              '    readiness = '
                                              'state.officer_readiness.word(readiness_offset)\n'
                                              '    percent = _random_fraction(state, 60)\n'
                                              '    readiness_loss = '
                                              'low16(divu_retained(u32(percent * readiness), '
                                              '100))\n'
                                              '    remaining = u16(readiness - readiness_loss)\n'
                                              '    '
                                              'state.officer_readiness.set_word(readiness_offset, '
                                              'remaining)\n'
                                              '    if remaining <= 10:\n'
                                              '        points = u16(points + '
                                              '_low_readiness_progress(state, readiness_offset, '
                                              'True, False))\n'
                                              "state.set_scalar('outcome_second_points', points)\n"
                                              'return points'},
 '_assigned_troop_total': {'signature': 'state: GameState, assignments: Table, city: Word',
                           'returns': 'Long',
                           'flow': 'total = 0\n'
                                   'for officer in range(255, -1, -1):\n'
                                   '    if assignments.byte(officer) == city & 255:\n'
                                   '        total = u32(total + '
                                   'state.officer_troops.long(u16(officer << 2)))\n'
                                   '        total = u32(total + 100)\n'
                                   'return total'},
 'consume_city_battle_resources': {'signature': 'state: GameState',
                                   'returns': 'None',
                                   'flow': 'state = checked_state(state)\n'
                                           "city = state.scalar('battle_scene')\n"
                                           'total = _assigned_troop_total(state, '
                                           'state.battlefield_city_assignment, city)\n'
                                           'factor = _random_fraction(state, 11, 10)\n'
                                           'consumed = divu_retained(_multiply_word_parts(total, '
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
                                           'total = _assigned_troop_total(state, '
                                           'state.officer_city_assignment, city)\n'
                                           'factor = _random_fraction(state, 11, 10)\n'
                                           'consumed = '
                                           'low16(divu_retained(_multiply_word_parts(total, '
                                           'factor), 500))\n'
                                           "city_offset = u16(state.scalar('battle_scene') << 2)\n"
                                           'food = state.city_food.long(city_offset)\n'
                                           'remaining = 0 if food < consumed else u32(food - '
                                           'consumed)\n'
                                           'state.city_food.set_long(city_offset, remaining)'},
 'apply_battlefield_heavy_losses_and_detach': {'signature': 'state: GameState',
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
                                                       '    factor = _random_fraction(state, 40, '
                                                       '50)\n'
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
                                                       '    percent = _random_fraction(state, 61)\n'
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
                                                       '_low_readiness_progress(state, '
                                                       'readiness_offset, False, True))\n'
                                                       "state.set_scalar('outcome_first_points', "
                                                       'points)\n'
                                                       'return points'}}

def _lower_settle_duel_training_and_troops(e,rules):
    e.label('action_pc_0188a6')
    e.ins('lea.l','0xc500:w,%a0',4)
    e.label('action_pc_0188aa')
    e.ins('lea.l','0xb200:w,%a1',4)
    e.label('action_pc_0188ae')
    e.ins('lea.l','0xc800:w,%a2',4)
    e.label('action_pc_0188b2')
    e.ins('lea.l','0xc000:w,%a3',4)
    e.label('action_pc_0188b6')
    e.ins('lea.l','0xbe00:w,%a4',4)
    e.label('action_pc_0188ba')
    e.ins('move.w','0xffff80e0:l,%d0',6)
    e.label('action_pc_0188c0')
    e.ins('move.b','0xffff8101:l,%d2',6)
    e.label('action_pc_0188c6')
    e.ins('cmpi.w','#0x4,0xffff8114:l',8)
    e.label('action_pc_0188ce')
    e.ins('bne.w','action_pc_0188f4',4)
    e.label('action_pc_0188d2')
    e.ins('move.w','%d0,-(%a7)',2)
    e.label('action_pc_0188d4')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_0188da')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('action_pc_0188e0')
    e.ins('move.l','%d0,%d1',2)
    e.label('action_pc_0188e2')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('action_pc_0188e4')
    e.ins('add.w','%d1,%d0',2)
    e.label('action_pc_0188e6')
    e.ins('swap','%d0',2)
    e.label('action_pc_0188e8')
    e.ins('addq.w','#0x1,%d0',2)
    e.label('action_pc_0188ea')
    e.ins('sub.w','%d0,%d2',2)
    e.label('action_pc_0188ec')
    e.ins('bcc.w','action_pc_0188f2',4)
    e.label('action_pc_0188f0')
    e.ins('clr.w','%d2',2)
    e.label('action_pc_0188f2')
    e.ins('move.w','(%a7)+,%d0',2)
    e.label('action_pc_0188f4')
    e.ins('move.b','%d2,(%a0, %d0.w)',4)
    e.label('action_pc_0188f8')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_0188fa')
    e.ins('move.w','0xffff810c:l,(%a1, %d0.w)',8)
    e.label('action_pc_018902')
    e.ins('bne.w','action_pc_01891a',4)
    e.label('action_pc_018906')
    e.ins('move.w','0xffff80e2:l,%d1',6)
    e.label('action_pc_01890c')
    e.ins('bsr.w','action_pc_0189d4',4)
    e.label('action_pc_018910')
    e.ins('move.w','0xffff80e0:l,%d1',6)
    e.label('action_pc_018916')
    e.ins('bsr.w','action_pc_018a54',4)
    e.label('action_pc_01891a')
    e.ins('move.w','0xffff80e2:l,%d0',6)
    e.label('action_pc_018920')
    e.ins('move.b','0xffff8103:l,%d2',6)
    e.label('action_pc_018926')
    e.ins('cmpi.w','#0x5,0xffff8114:l',8)
    e.label('action_pc_01892e')
    e.ins('bne.w','action_pc_018954',4)
    e.label('action_pc_018932')
    e.ins('move.w','%d0,-(%a7)',2)
    e.label('action_pc_018934')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_01893a')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('action_pc_018940')
    e.ins('move.l','%d0,%d1',2)
    e.label('action_pc_018942')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('action_pc_018944')
    e.ins('add.w','%d1,%d0',2)
    e.label('action_pc_018946')
    e.ins('swap','%d0',2)
    e.label('action_pc_018948')
    e.ins('addq.w','#0x1,%d0',2)
    e.label('action_pc_01894a')
    e.ins('sub.w','%d0,%d2',2)
    e.label('action_pc_01894c')
    e.ins('bcc.w','action_pc_018952',4)
    e.label('action_pc_018950')
    e.ins('clr.w','%d2',2)
    e.label('action_pc_018952')
    e.ins('move.w','(%a7)+,%d0',2)
    e.label('action_pc_018954')
    e.ins('move.b','%d2,(%a0, %d0.w)',4)
    e.label('action_pc_018958')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_01895a')
    e.ins('move.w','0xffff810e:l,(%a1, %d0.w)',8)
    e.label('action_pc_018962')
    e.ins('bne.w','action_pc_01897a',4)
    e.label('action_pc_018966')
    e.ins('move.w','0xffff80e0:l,%d1',6)
    e.label('action_pc_01896c')
    e.ins('bsr.w','action_pc_0189d4',4)
    e.label('action_pc_018970')
    e.ins('move.w','0xffff80e2:l,%d1',6)
    e.label('action_pc_018976')
    e.ins('bsr.w','action_pc_018a54',4)
    e.label('action_pc_01897a')
    e.ins('move.w','0xffff80e0:l,%d6',6)
    e.label('action_pc_018980')
    e.ins('move.w','0xffff80e2:l,%d7',6)
    e.label('action_pc_018986')
    e.ins('move.w','%d6,%d0',2)
    e.label('action_pc_018988')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('action_pc_01898a')
    e.ins('move.w','0x2(%a2, %d0.w),%d2',4)
    e.label('action_pc_01898e')
    e.ins('sub.w','0xffff8118:l,%d2',6)
    e.label('action_pc_018994')
    e.ins('bcc.w','action_pc_01899a',4)
    e.label('action_pc_018998')
    e.ins('clr.w','%d2',2)
    e.label('action_pc_01899a')
    e.ins('move.w','%d7,%d0',2)
    e.label('action_pc_01899c')
    e.ins('bsr.w','action_pc_018a2e',4)
    e.label('action_pc_0189a0')
    e.ins('move.w','%d7,%d0',2)
    e.label('action_pc_0189a2')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('action_pc_0189a4')
    e.ins('move.w','0x2(%a2, %d0.w),%d2',4)
    e.label('action_pc_0189a8')
    e.ins('sub.w','0xffff811a:l,%d2',6)
    e.label('action_pc_0189ae')
    e.ins('bcc.w','action_pc_0189b4',4)
    e.label('action_pc_0189b2')
    e.ins('clr.w','%d2',2)
    e.label('action_pc_0189b4')
    e.ins('move.w','%d6,%d0',2)
    e.label('action_pc_0189b6')
    e.ins('bsr.w','action_pc_018a2e',4)
    e.label('action_pc_0189ba')
    e.ins('lsl.w','#0x2,%d6',2)
    e.label('action_pc_0189bc')
    e.ins('lsl.w','#0x2,%d7',2)
    e.label('action_pc_0189be')
    e.ins('move.w','0xffff8118:l,0x2(%a2, %d6.w)',8)
    e.label('action_pc_0189c6')
    e.ins('move.w','0xffff811a:l,0x2(%a2, %d7.w)',8)
    e.label('action_pc_0189ce')
    e.ins('bsr.w','action_pc_018a94',4)
    e.label('action_pc_0189d2')
    e.ins('rts','',2)

def _lower_settle_duel_packets(e,rules):
    e.label('action_pc_018b00')
    e.ins('lea.l','0xff7050:l,%a0',6)
    e.label('action_pc_018b06')
    e.ins('lea.l','0xff70a0:l,%a1',6)
    e.label('action_pc_018b0c')
    e.ins('lea.l','0xff70f0:l,%a2',6)
    e.label('action_pc_018b12')
    e.ins('lea.l','0xff70f1:l,%a3',6)
    e.label('action_pc_018b18')
    e.ins('move.w','0xff706a:l,%d0',6)
    e.label('action_pc_018b1e')
    e.ins('cmp.w','0xffff80e0:l,%d0',6)
    e.label('action_pc_018b24')
    e.ins('beq.w','action_pc_018b2c',4)
    e.label('action_pc_018b28')
    e.ins('exg','%a0,%a1',2)
    e.label('action_pc_018b2a')
    e.ins('exg','%a2,%a3',2)
    e.label('action_pc_018b2c')
    e.ins('move.w','0x1c(%a0),0xffff810c:l',8)
    e.label('action_pc_018b34')
    e.ins('move.w','0x1c(%a1),0xffff810e:l',8)
    e.label('action_pc_018b3c')
    e.ins('move.w','0xff706a:l,%d0',6)
    e.label('action_pc_018b42')
    e.ins('move.w','0xff70ba:l,%d1',6)
    e.label('action_pc_018b48')
    e.ins('move.b','0xff70f0:l,%d2',6)
    e.label('action_pc_018b4e')
    e.ins('beq.w','action_pc_018b56',4)
    e.label('action_pc_018b52')
    e.ins('bsr.w','action_pc_018b94',4)
    e.label('action_pc_018b56')
    e.ins('exg','%d0,%d1',2)
    e.label('action_pc_018b58')
    e.ins('move.b','0xff70f1:l,%d2',6)
    e.label('action_pc_018b5e')
    e.ins('beq.w','action_pc_018b66',4)
    e.label('action_pc_018b62')
    e.ins('bsr.w','action_pc_018b94',4)
    e.label('action_pc_018b66')
    e.ins('cmpi.b','#0x1,0xff70f0:l',8)
    e.label('action_pc_018b6e')
    e.ins('beq.w','action_pc_018b8e',4)
    e.label('action_pc_018b72')
    e.ins('cmpi.b','#0x1,0xff70f1:l',8)
    e.label('action_pc_018b7a')
    e.ins('beq.w','action_pc_018b8e',4)
    e.label('action_pc_018b7e')
    e.ins('bsr.w','action_pc_018c56',4)
    e.label('action_pc_018b82')
    e.ins('jsr','-734(%pc)',4)
    e.label('action_pc_018b86')
    e.ins('andi.w','#0xfffe,%sr',4)
    e.label('action_pc_018b8a')
    e.ins('bra.w','action_pc_018b92',4)
    e.label('action_pc_018b8e')
    e.ins('ori.w','#0x1,%sr',4)
    e.label('action_pc_018b92')
    e.ins('rts','',2)

def _lower_apply_duel_disposition(e,rules):
    e.label('action_pc_018b94')
    e.ins('movem.l','%d0-%d1/%a0-%a1,-(%a7)',4)
    e.label('action_pc_018b98')
    e.ins('tst.w','0xefe0:w',4)
    e.label('action_pc_018b9c')
    e.ins('beq.w','action_pc_018c30',4)
    e.label('action_pc_018ba0')
    e.ins('cmpi.b','#0x2,%d2',4)
    e.label('action_pc_018ba4')
    e.ins('beq.w','action_pc_018bf4',4)
    e.label('action_pc_018ba8')
    e.ins('cmpi.b','#0x3,%d2',4)
    e.label('action_pc_018bac')
    e.ins('bne.w','action_pc_018c50',4)
    e.label('action_pc_018bb0')
    e.ins('lea.l','0xa5ce:w,%a0',4)
    e.label('action_pc_018bb4')
    e.ins('lea.l','0xa550:w,%a1',4)
    e.label('action_pc_018bb8')
    e.ins('move.w','0xf68a:w,%d3',4)
    e.label('action_pc_018bbc')
    e.ins('ori.w','#0x80,%d3',4)
    e.label('action_pc_018bc0')
    e.ins('cmp.w','0xf702:w,%d0',4)
    e.label('action_pc_018bc4')
    e.ins('beq.w','action_pc_018bd4',4)
    e.label('action_pc_018bc8')
    e.ins('ori.w','#0x40,%d3',4)
    e.label('action_pc_018bcc')
    e.ins('lea.l','0xa57a:w,%a0',4)
    e.label('action_pc_018bd0')
    e.ins('lea.l','0xa5a4:w,%a1',4)
    e.label('action_pc_018bd4')
    e.ins('tst.w','(%a0)+',2)
    e.label('action_pc_018bd6')
    e.ins('bpl.b','action_pc_018bd4',2)
    e.label('action_pc_018bd8')
    e.ins('move.w','%d0,-0x2(%a0)',4)
    e.label('action_pc_018bdc')
    e.ins('move.w','#0xffff,(%a0)',4)
    e.label('action_pc_018be0')
    e.ins('move.w','(%a1)+,%d3',2)
    e.label('action_pc_018be2')
    e.ins('andi.w','#0xff,%d3',4)
    e.label('action_pc_018be6')
    e.ins('cmp.w','%d0,%d3',2)
    e.label('action_pc_018be8')
    e.ins('bne.b','action_pc_018be0',2)
    e.label('action_pc_018bea')
    e.ins('move.w','(%a1)+,-0x4(%a1)',4)
    e.label('action_pc_018bee')
    e.ins('bpl.b','action_pc_018bea',2)
    e.label('action_pc_018bf0')
    e.ins('bra.w','action_pc_018c50',4)
    e.label('action_pc_018bf4')
    e.ins('cmp.w','0xf702:w,%d0',4)
    e.label('action_pc_018bf8')
    e.ins('bne.w','action_pc_018c08',4)
    e.label('action_pc_018bfc')
    e.ins('lea.l','0xa550:w,%a0',4)
    e.label('action_pc_018c00')
    e.ins('lea.l','0xa5ce:w,%a1',4)
    e.label('action_pc_018c04')
    e.ins('bra.w','action_pc_018c10',4)
    e.label('action_pc_018c08')
    e.ins('lea.l','0xa5a4:w,%a0',4)
    e.label('action_pc_018c0c')
    e.ins('lea.l','0xa57a:w,%a1',4)
    e.label('action_pc_018c10')
    e.ins('move.w','(%a0)+,%d1',2)
    e.label('action_pc_018c12')
    e.ins('andi.w','#0xff,%d1',4)
    e.label('action_pc_018c16')
    e.ins('cmp.w','%d0,%d1',2)
    e.label('action_pc_018c18')
    e.ins('bne.b','action_pc_018c10',2)
    e.label('action_pc_018c1a')
    e.ins('move.w','(%a0)+,-0x4(%a0)',4)
    e.label('action_pc_018c1e')
    e.ins('bpl.b','action_pc_018c1a',2)
    e.label('action_pc_018c20')
    e.ins('tst.w','(%a1)+',2)
    e.label('action_pc_018c22')
    e.ins('bpl.b','action_pc_018c20',2)
    e.label('action_pc_018c24')
    e.ins('move.w','%d0,-0x2(%a1)',4)
    e.label('action_pc_018c28')
    e.ins('move.w','#0xffff,(%a1)',4)
    e.label('action_pc_018c2c')
    e.ins('bra.w','action_pc_018c50',4)
    e.label('action_pc_018c30')
    e.ins('cmpi.b','#0x3,%d2',4)
    e.label('action_pc_018c34')
    e.ins('beq.w','action_pc_018c50',4)
    e.label('action_pc_018c38')
    e.ins('move.w','#0x6,%d1',4)
    e.label('action_pc_018c3c')
    e.ins('cmp.w','0xffff80e0:l,%d0',6)
    e.label('action_pc_018c42')
    e.ins('beq.w','action_pc_018c4a',4)
    e.label('action_pc_018c46')
    e.ins('move.w','#0x7,%d1',4)
    e.label('action_pc_018c4a')
    e.ins('move.w','%d1,0xffff8114:l',6)
    e.label('action_pc_018c50')
    e.ins('movem.l','(%a7)+,%d0-%d1/%a0-%a1',4)
    e.label('action_pc_018c54')
    e.ins('rts','',2)

def _lower_detach_zero_readiness_duelists(e,rules):
    e.label('action_pc_018c56')
    e.ins('tst.w','0xefe0:w',4)
    e.label('action_pc_018c5a')
    e.ins('beq.w','action_pc_018c86',4)
    e.label('action_pc_018c5e')
    e.ins('tst.w','0xff706c:l',6)
    e.label('action_pc_018c64')
    e.ins('bne.w','action_pc_018c72',4)
    e.label('action_pc_018c68')
    e.ins('move.w','0xff706a:l,%d0',6)
    e.label('action_pc_018c6e')
    e.ins('bsr.w','action_pc_018c88',4)
    e.label('action_pc_018c72')
    e.ins('tst.w','0xff70bc:l',6)
    e.label('action_pc_018c78')
    e.ins('bne.w','action_pc_018c86',4)
    e.label('action_pc_018c7c')
    e.ins('move.w','0xff70ba:l,%d0',6)
    e.label('action_pc_018c82')
    e.ins('bsr.w','action_pc_018c88',4)
    e.label('action_pc_018c86')
    e.ins('rts','',2)

def _lower_compute_outcome_force_ratio(e,rules):
    e.label('action_pc_01c1c2')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_01c1c8')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('action_pc_01c1ce')
    e.ins('move.l','%d0,%d1',2)
    e.label('action_pc_01c1d0')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('action_pc_01c1d2')
    e.ins('add.l','%d1,%d0',2)
    e.label('action_pc_01c1d4')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('action_pc_01c1d6')
    e.ins('swap','%d0',2)
    e.label('action_pc_01c1d8')
    e.ins('addi.w','#0xa,%d0',4)
    e.label('action_pc_01c1dc')
    e.ins('bsr.w','action_pc_01c2a0',4)
    e.label('action_pc_01c1e0')
    e.ins('moveq','#0,%d1',2)
    e.label('action_pc_01c1e2')
    e.ins('clr.w','%d2',2)
    e.label('action_pc_01c1e4')
    e.ins('clr.w','%d3',2)
    e.label('action_pc_01c1e6')
    e.ins('lea.l','0xc800:w,%a0',4)
    e.label('action_pc_01c1ea')
    e.ins('lea.l','0xb400:w,%a1',4)
    e.label('action_pc_01c1ee')
    e.ins('lea.l','0xb600:w,%a2',4)
    e.label('action_pc_01c1f2')
    e.ins('lea.l','0xd300:w,%a3',4)
    e.label('action_pc_01c1f6')
    e.ins('move.w','(%a3)+,%d4',2)
    e.label('action_pc_01c1f8')
    e.ins('bmi.w','action_pc_01c20e',4)
    e.label('action_pc_01c1fc')
    e.ins('lsl.w','#0x1,%d4',2)
    e.label('action_pc_01c1fe')
    e.ins('add.w','(%a1, %d4.w),%d2',4)
    e.label('action_pc_01c202')
    e.ins('add.w','(%a2, %d4.w),%d3',4)
    e.label('action_pc_01c206')
    e.ins('lsl.w','#0x1,%d4',2)
    e.label('action_pc_01c208')
    e.ins('add.l','(%a0, %d4.w),%d1',4)
    e.label('action_pc_01c20c')
    e.ins('bra.b','action_pc_01c1f6',2)
    e.label('action_pc_01c20e')
    e.ins('addq.w','#0x1,%d1',2)
    e.label('action_pc_01c210')
    e.ins('lsr.l','#0x5,%d1',2)
    e.label('action_pc_01c212')
    e.ins('lsr.w','#0x3,%d2',2)
    e.label('action_pc_01c214')
    e.ins('lsr.w','#0x3,%d3',2)
    e.label('action_pc_01c216')
    e.ins('addq.w','#0x1,%d2',2)
    e.label('action_pc_01c218')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('action_pc_01c21a')
    e.ins('move.w','%d1,%d4',2)
    e.label('action_pc_01c21c')
    e.ins('mulu.w','%d2,%d4',2)
    e.label('action_pc_01c21e')
    e.ins('swap','%d1',2)
    e.label('action_pc_01c220')
    e.ins('mulu.w','%d2,%d1',2)
    e.label('action_pc_01c222')
    e.ins('swap','%d1',2)
    e.label('action_pc_01c224')
    e.ins('add.l','%d4,%d1',2)
    e.label('action_pc_01c226')
    e.ins('move.w','%d1,%d4',2)
    e.label('action_pc_01c228')
    e.ins('mulu.w','%d3,%d4',2)
    e.label('action_pc_01c22a')
    e.ins('swap','%d1',2)
    e.label('action_pc_01c22c')
    e.ins('mulu.w','%d3,%d1',2)
    e.label('action_pc_01c22e')
    e.ins('swap','%d1',2)
    e.label('action_pc_01c230')
    e.ins('add.l','%d4,%d1',2)
    e.label('action_pc_01c232')
    e.ins('move.w','%d1,%d4',2)
    e.label('action_pc_01c234')
    e.ins('mulu.w','%d0,%d4',2)
    e.label('action_pc_01c236')
    e.ins('swap','%d1',2)
    e.label('action_pc_01c238')
    e.ins('mulu.w','%d0,%d1',2)
    e.label('action_pc_01c23a')
    e.ins('swap','%d1',2)
    e.label('action_pc_01c23c')
    e.ins('add.l','%d4,%d1',2)
    e.label('action_pc_01c23e')
    e.ins('bsr.w','action_pc_01c2c8',4)
    e.label('action_pc_01c242')
    e.ins('lea.l','0xd300:w,%a0',4)
    e.label('action_pc_01c246')
    e.ins('lea.l','0xc800:w,%a1',4)
    e.label('action_pc_01c24a')
    e.ins('lea.l','0xb400:w,%a2',4)
    e.label('action_pc_01c24e')
    e.ins('lea.l','0xb600:w,%a3',4)
    e.label('action_pc_01c252')
    e.ins('moveq','#0,%d2',2)
    e.label('action_pc_01c254')
    e.ins('clr.w','%d3',2)
    e.label('action_pc_01c256')
    e.ins('clr.w','%d4',2)
    e.label('action_pc_01c258')
    e.ins('move.w','(%a0)+,%d5',2)
    e.label('action_pc_01c25a')
    e.ins('bmi.w','action_pc_01c270',4)
    e.label('action_pc_01c25e')
    e.ins('lsl.w','#0x1,%d5',2)
    e.label('action_pc_01c260')
    e.ins('add.w','(%a2, %d5.w),%d3',4)
    e.label('action_pc_01c264')
    e.ins('add.w','(%a3, %d5.w),%d4',4)
    e.label('action_pc_01c268')
    e.ins('lsl.w','#0x1,%d5',2)
    e.label('action_pc_01c26a')
    e.ins('add.l','(%a1, %d5.w),%d2',4)
    e.label('action_pc_01c26e')
    e.ins('bra.b','action_pc_01c258',2)
    e.label('action_pc_01c270')
    e.ins('lsr.l','#0x5,%d2',2)
    e.label('action_pc_01c272')
    e.ins('lsr.w','#0x3,%d3',2)
    e.label('action_pc_01c274')
    e.ins('lsr.w','#0x3,%d4',2)
    e.label('action_pc_01c276')
    e.ins('addq.w','#0x1,%d2',2)
    e.label('action_pc_01c278')
    e.ins('addq.w','#0x1,%d3',2)
    e.label('action_pc_01c27a')
    e.ins('addq.w','#0x1,%d4',2)
    e.label('action_pc_01c27c')
    e.ins('move.w','%d2,%d5',2)
    e.label('action_pc_01c27e')
    e.ins('mulu.w','%d3,%d5',2)
    e.label('action_pc_01c280')
    e.ins('swap','%d2',2)
    e.label('action_pc_01c282')
    e.ins('mulu.w','%d3,%d2',2)
    e.label('action_pc_01c284')
    e.ins('swap','%d2',2)
    e.label('action_pc_01c286')
    e.ins('add.l','%d5,%d2',2)
    e.label('action_pc_01c288')
    e.ins('move.w','%d2,%d5',2)
    e.label('action_pc_01c28a')
    e.ins('mulu.w','%d3,%d5',2)
    e.label('action_pc_01c28c')
    e.ins('swap','%d2',2)
    e.label('action_pc_01c28e')
    e.ins('mulu.w','%d3,%d2',2)
    e.label('action_pc_01c290')
    e.ins('swap','%d2',2)
    e.label('action_pc_01c292')
    e.ins('add.l','%d5,%d2',2)
    e.label('action_pc_01c294')
    e.ins('jsr','action_pc_035760:l',6)
    e.label('action_pc_01c29a')
    e.ins('move.w','%d1,0xefbc:w',4)
    e.label('action_pc_01c29e')
    e.ins('rts','',2)

def _lower_apply_battlefield_ratio_losses(e,rules):
    e.label('action_pc_01c2fc')
    e.ins('bsr.b','action_pc_01c2c8',2)
    e.label('action_pc_01c2fe')
    e.ins('lea.l','0xd300:w,%a0',4)
    e.label('action_pc_01c302')
    e.ins('lea.l','0xc800:w,%a1',4)
    e.label('action_pc_01c306')
    e.ins('lea.l','0xb200:w,%a2',4)
    e.label('action_pc_01c30a')
    e.ins('lea.l','0xcc00:w,%a3',4)
    e.label('action_pc_01c30e')
    e.ins('lea.l','0xc000:w,%a4',4)
    e.label('action_pc_01c312')
    e.ins('lea.l','0xc700:w,%a5',4)
    e.label('action_pc_01c316')
    e.ins('clr.w','%d7',2)
    e.label('action_pc_01c318')
    e.ins('move.w','(%a0)+,%d2',2)
    e.label('action_pc_01c31a')
    e.ins('bmi.w','action_pc_01c396',4)
    e.label('action_pc_01c31e')
    e.ins('lsl.w','#0x2,%d2',2)
    e.label('action_pc_01c320')
    e.ins('move.l','(%a1, %d2.w),%d3',4)
    e.label('action_pc_01c324')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_01c32a')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('action_pc_01c330')
    e.ins('move.l','%d0,%d1',2)
    e.label('action_pc_01c332')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('action_pc_01c334')
    e.ins('add.l','%d1,%d0',2)
    e.label('action_pc_01c336')
    e.ins('lsl.l','#0x3,%d0',2)
    e.label('action_pc_01c338')
    e.ins('swap','%d0',2)
    e.label('action_pc_01c33a')
    e.ins('addi.w','#0x1e,%d0',4)
    e.label('action_pc_01c33e')
    e.ins('mulu.w','0xefbc:w,%d0',4)
    e.label('action_pc_01c342')
    e.ins('move.w','%d0,%d1',2)
    e.label('action_pc_01c344')
    e.ins('mulu.w','%d3,%d1',2)
    e.label('action_pc_01c346')
    e.ins('swap','%d0',2)
    e.label('action_pc_01c348')
    e.ins('mulu.w','%d3,%d0',2)
    e.label('action_pc_01c34a')
    e.ins('swap','%d0',2)
    e.label('action_pc_01c34c')
    e.ins('add.l','%d1,%d0',2)
    e.label('action_pc_01c34e')
    e.ins('divu.w','#0x3e8,%d0',4)
    e.label('action_pc_01c352')
    e.ins('sub.w','%d0,%d3',2)
    e.label('action_pc_01c354')
    e.ins('move.w','%d3,0x2(%a1, %d2.w)',4)
    e.label('action_pc_01c358')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('action_pc_01c35e')
    e.ins('divu.w','#0x190,%d0',4)
    e.label('action_pc_01c362')
    e.ins('add.w','%d0,%d7',2)
    e.label('action_pc_01c364')
    e.ins('lsr.w','#0x1,%d2',2)
    e.label('action_pc_01c366')
    e.ins('move.w','(%a2, %d2.w),%d3',4)
    e.label('action_pc_01c36a')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_01c370')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('action_pc_01c376')
    e.ins('move.l','%d0,%d1',2)
    e.label('action_pc_01c378')
    e.ins('lsl.l','#0x4,%d0',2)
    e.label('action_pc_01c37a')
    e.ins('sub.l','%d1,%d0',2)
    e.label('action_pc_01c37c')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('action_pc_01c37e')
    e.ins('swap','%d0',2)
    e.label('action_pc_01c380')
    e.ins('mulu.w','%d3,%d0',2)
    e.label('action_pc_01c382')
    e.ins('divu.w','#0x64,%d0',4)
    e.label('action_pc_01c386')
    e.ins('sub.w','%d0,%d3',2)
    e.label('action_pc_01c388')
    e.ins('bne.w','action_pc_01c390',4)
    e.label('action_pc_01c38c')
    e.ins('move.w','#0x1,%d3',4)
    e.label('action_pc_01c390')
    e.ins('move.w','%d3,(%a2, %d2.w)',4)
    e.label('action_pc_01c394')
    e.ins('bra.b','action_pc_01c318',2)
    e.label('action_pc_01c396')
    e.ins('move.w','%d7,0xefb8:w',4)
    e.label('action_pc_01c39a')
    e.ins('rts','',2)

def _lower_apply_city_assigned_heavy_losses(e,rules):
    e.label('action_pc_01c39c')
    e.ins('bsr.w','action_pc_01c2a0',4)
    e.label('action_pc_01c3a0')
    e.ins('lea.l','0xd300:w,%a0',4)
    e.label('action_pc_01c3a4')
    e.ins('lea.l','0xc800:w,%a1',4)
    e.label('action_pc_01c3a8')
    e.ins('lea.l','0xb200:w,%a2',4)
    e.label('action_pc_01c3ac')
    e.ins('lea.l','0xc000:w,%a3',4)
    e.label('action_pc_01c3b0')
    e.ins('lea.l','0xcc00:w,%a4',4)
    e.label('action_pc_01c3b4')
    e.ins('lea.l','0xf45e:w,%a5',4)
    e.label('action_pc_01c3b8')
    e.ins('lea.l','0xc700:w,%a6',4)
    e.label('action_pc_01c3bc')
    e.ins('clr.w','%d7',2)
    e.label('action_pc_01c3be')
    e.ins('move.w','(%a0)+,%d2',2)
    e.label('action_pc_01c3c0')
    e.ins('bmi.w','action_pc_01c460',4)
    e.label('action_pc_01c3c4')
    e.ins('lsl.w','#0x2,%d2',2)
    e.label('action_pc_01c3c6')
    e.ins('move.l','(%a1, %d2.w),%d3',4)
    e.label('action_pc_01c3ca')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_01c3d0')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('action_pc_01c3d6')
    e.ins('move.l','%d0,%d1',2)
    e.label('action_pc_01c3d8')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('action_pc_01c3da')
    e.ins('add.l','%d1,%d0',2)
    e.label('action_pc_01c3dc')
    e.ins('lsl.l','#0x3,%d0',2)
    e.label('action_pc_01c3de')
    e.ins('swap','%d0',2)
    e.label('action_pc_01c3e0')
    e.ins('addi.w','#0x32,%d0',4)
    e.label('action_pc_01c3e4')
    e.ins('mulu.w','%d3,%d0',2)
    e.label('action_pc_01c3e6')
    e.ins('divu.w','#0x64,%d0',4)
    e.label('action_pc_01c3ea')
    e.ins('sub.w','%d0,%d3',2)
    e.label('action_pc_01c3ec')
    e.ins('move.w','%d3,0x2(%a1, %d2.w)',4)
    e.label('action_pc_01c3f0')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('action_pc_01c3f6')
    e.ins('divu.w','#0x190,%d0',4)
    e.label('action_pc_01c3fa')
    e.ins('add.w','%d0,%d7',2)
    e.label('action_pc_01c3fc')
    e.ins('lsr.w','#0x1,%d2',2)
    e.label('action_pc_01c3fe')
    e.ins('move.w','(%a2, %d2.w),%d3',4)
    e.label('action_pc_01c402')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_01c408')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('action_pc_01c40e')
    e.ins('move.l','%d0,%d1',2)
    e.label('action_pc_01c410')
    e.ins('lsl.l','#0x4,%d0',2)
    e.label('action_pc_01c412')
    e.ins('sub.l','%d1,%d0',2)
    e.label('action_pc_01c414')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('action_pc_01c416')
    e.ins('swap','%d0',2)
    e.label('action_pc_01c418')
    e.ins('mulu.w','%d3,%d0',2)
    e.label('action_pc_01c41a')
    e.ins('divu.w','#0x64,%d0',4)
    e.label('action_pc_01c41e')
    e.ins('sub.w','%d0,%d3',2)
    e.label('action_pc_01c420')
    e.ins('move.w','%d3,(%a2, %d2.w)',4)
    e.label('action_pc_01c424')
    e.ins('cmpi.w','#0xa,%d3',4)
    e.label('action_pc_01c428')
    e.ins('bhi.b','action_pc_01c3be',2)
    e.label('action_pc_01c42a')
    e.ins('move.w','(%a3, %d2.w),%d3',4)
    e.label('action_pc_01c42e')
    e.ins('andi.l','#0xffff,%d3',6)
    e.label('action_pc_01c434')
    e.ins('divu.w','#0x5,%d3',4)
    e.label('action_pc_01c438')
    e.ins('lsr.w','#0x1,%d2',2)
    e.label('action_pc_01c43a')
    e.ins('move.w','0xf68a:w,%d4',4)
    e.label('action_pc_01c43e')
    e.ins('lsl.w','#0x1,%d4',2)
    e.label('action_pc_01c440')
    e.ins('cmp.w','(%a5, %d4.w),%d2',4)
    e.label('action_pc_01c444')
    e.ins('bne.w','action_pc_01c44c',4)
    e.label('action_pc_01c448')
    e.ins('addi.w','#0x1e,%d3',4)
    e.label('action_pc_01c44c')
    e.ins('btst.b','#0x4,(%a6, %d2.w)',6)
    e.label('action_pc_01c452')
    e.ins('beq.w','action_pc_01c45a',4)
    e.label('action_pc_01c456')
    e.ins('addi.w','#0x14,%d3',4)
    e.label('action_pc_01c45a')
    e.ins('add.w','%d3,%d7',2)
    e.label('action_pc_01c45c')
    e.ins('bra.w','action_pc_01c3be',4)
    e.label('action_pc_01c460')
    e.ins('move.w','%d7,0xefba:w',4)
    e.label('action_pc_01c464')
    e.ins('rts','',2)

def _lower_consume_city_battle_resources(e,rules):
    e.label('action_pc_01c466')
    e.ins('lea.l','0xc800:w,%a0',4)
    e.label('action_pc_01c46a')
    e.ins('lea.l','0xa050:w,%a1',4)
    e.label('action_pc_01c46e')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('action_pc_01c472')
    e.ins('move.w','#0xff,%d1',4)
    e.label('action_pc_01c476')
    e.ins('moveq','#0,%d2',2)
    e.label('action_pc_01c478')
    e.ins('cmp.b','(%a1, %d1.w),%d0',4)
    e.label('action_pc_01c47c')
    e.ins('bne.w','action_pc_01c48e',4)
    e.label('action_pc_01c480')
    e.ins('move.w','%d1,%d3',2)
    e.label('action_pc_01c482')
    e.ins('lsl.w','#0x2,%d3',2)
    e.label('action_pc_01c484')
    e.ins('add.l','(%a0, %d3.w),%d2',4)
    e.label('action_pc_01c488')
    e.ins('addi.l','#0x64,%d2',6)
    e.label('action_pc_01c48e')
    e.ins('dbra','%d1,action_pc_01c478',4)
    e.label('action_pc_01c492')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_01c498')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('action_pc_01c49e')
    e.ins('move.l','%d0,%d1',2)
    e.label('action_pc_01c4a0')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('action_pc_01c4a2')
    e.ins('add.l','%d1,%d0',2)
    e.label('action_pc_01c4a4')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('action_pc_01c4a6')
    e.ins('add.l','%d1,%d0',2)
    e.label('action_pc_01c4a8')
    e.ins('swap','%d0',2)
    e.label('action_pc_01c4aa')
    e.ins('addi.w','#0xa,%d0',4)
    e.label('action_pc_01c4ae')
    e.ins('move.w','%d2,%d3',2)
    e.label('action_pc_01c4b0')
    e.ins('mulu.w','%d0,%d3',2)
    e.label('action_pc_01c4b2')
    e.ins('swap','%d2',2)
    e.label('action_pc_01c4b4')
    e.ins('mulu.w','%d0,%d2',2)
    e.label('action_pc_01c4b6')
    e.ins('swap','%d2',2)
    e.label('action_pc_01c4b8')
    e.ins('add.l','%d3,%d2',2)
    e.label('action_pc_01c4ba')
    e.ins('divu.w','#0x1f4,%d2',4)
    e.label('action_pc_01c4be')
    e.ins('lea.l','0xee24:w,%a2',4)
    e.label('action_pc_01c4c2')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('action_pc_01c4c6')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('action_pc_01c4c8')
    e.ins('move.l','(%a2, %d0.w),%d1',4)
    e.label('action_pc_01c4cc')
    e.ins('andi.l','#0xffff,%d2',6)
    e.label('action_pc_01c4d2')
    e.ins('sub.l','%d2,%d1',2)
    e.label('action_pc_01c4d4')
    e.ins('bcc.w','action_pc_01c4da',4)
    e.label('action_pc_01c4d8')
    e.ins('moveq','#0,%d1',2)
    e.label('action_pc_01c4da')
    e.ins('move.l','%d1,(%a2, %d0.w)',4)
    e.label('action_pc_01c4de')
    e.ins('lea.l','0xcc00:w,%a1',4)
    e.label('action_pc_01c4e2')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('action_pc_01c4e6')
    e.ins('move.w','#0xff,%d1',4)
    e.label('action_pc_01c4ea')
    e.ins('moveq','#0,%d2',2)
    e.label('action_pc_01c4ec')
    e.ins('cmp.b','(%a1, %d1.w),%d0',4)
    e.label('action_pc_01c4f0')
    e.ins('bne.w','action_pc_01c502',4)
    e.label('action_pc_01c4f4')
    e.ins('move.w','%d1,%d3',2)
    e.label('action_pc_01c4f6')
    e.ins('lsl.w','#0x2,%d3',2)
    e.label('action_pc_01c4f8')
    e.ins('add.l','(%a0, %d3.w),%d2',4)
    e.label('action_pc_01c4fc')
    e.ins('addi.l','#0x64,%d2',6)
    e.label('action_pc_01c502')
    e.ins('dbra','%d1,action_pc_01c4ec',4)
    e.label('action_pc_01c506')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_01c50c')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('action_pc_01c512')
    e.ins('move.l','%d0,%d1',2)
    e.label('action_pc_01c514')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('action_pc_01c516')
    e.ins('add.l','%d1,%d0',2)
    e.label('action_pc_01c518')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('action_pc_01c51a')
    e.ins('add.l','%d1,%d0',2)
    e.label('action_pc_01c51c')
    e.ins('swap','%d0',2)
    e.label('action_pc_01c51e')
    e.ins('addi.w','#0xa,%d0',4)
    e.label('action_pc_01c522')
    e.ins('move.w','%d2,%d3',2)
    e.label('action_pc_01c524')
    e.ins('mulu.w','%d0,%d3',2)
    e.label('action_pc_01c526')
    e.ins('swap','%d2',2)
    e.label('action_pc_01c528')
    e.ins('mulu.w','%d0,%d2',2)
    e.label('action_pc_01c52a')
    e.ins('swap','%d2',2)
    e.label('action_pc_01c52c')
    e.ins('add.l','%d3,%d2',2)
    e.label('action_pc_01c52e')
    e.ins('divu.w','#0x1f4,%d2',4)
    e.label('action_pc_01c532')
    e.ins('andi.l','#0xffff,%d2',6)
    e.label('action_pc_01c538')
    e.ins('lea.l','0xe09c:w,%a2',4)
    e.label('action_pc_01c53c')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('action_pc_01c540')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('action_pc_01c542')
    e.ins('move.l','(%a2, %d0.w),%d3',4)
    e.label('action_pc_01c546')
    e.ins('sub.l','%d2,%d3',2)
    e.label('action_pc_01c548')
    e.ins('bcc.w','action_pc_01c54e',4)
    e.label('action_pc_01c54c')
    e.ins('moveq','#0,%d3',2)
    e.label('action_pc_01c54e')
    e.ins('move.l','%d3,(%a2, %d0.w)',4)
    e.label('action_pc_01c552')
    e.ins('rts','',2)

def _lower_apply_battlefield_heavy_losses_and_detach(e,rules):
    e.label('action_pc_01c5ee')
    e.ins('bsr.w','action_pc_01c2c8',4)
    e.label('action_pc_01c5f2')
    e.ins('lea.l','0xd300:w,%a0',4)
    e.label('action_pc_01c5f6')
    e.ins('lea.l','0xc800:w,%a1',4)
    e.label('action_pc_01c5fa')
    e.ins('lea.l','0xb200:w,%a2',4)
    e.label('action_pc_01c5fe')
    e.ins('lea.l','0xc000:w,%a3',4)
    e.label('action_pc_01c602')
    e.ins('lea.l','0xc700:w,%a4',4)
    e.label('action_pc_01c606')
    e.ins('lea.l','0xcc00:w,%a5',4)
    e.label('action_pc_01c60a')
    e.ins('clr.w','%d7',2)
    e.label('action_pc_01c60c')
    e.ins('move.w','(%a0)+,%d2',2)
    e.label('action_pc_01c60e')
    e.ins('bmi.w','action_pc_01c698',4)
    e.label('action_pc_01c612')
    e.ins('lsl.w','#0x2,%d2',2)
    e.label('action_pc_01c614')
    e.ins('move.l','(%a1, %d2.w),%d3',4)
    e.label('action_pc_01c618')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_01c61e')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('action_pc_01c624')
    e.ins('move.l','%d0,%d1',2)
    e.label('action_pc_01c626')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('action_pc_01c628')
    e.ins('add.l','%d1,%d0',2)
    e.label('action_pc_01c62a')
    e.ins('lsl.l','#0x3,%d0',2)
    e.label('action_pc_01c62c')
    e.ins('swap','%d0',2)
    e.label('action_pc_01c62e')
    e.ins('addi.w','#0x32,%d0',4)
    e.label('action_pc_01c632')
    e.ins('mulu.w','%d3,%d0',2)
    e.label('action_pc_01c634')
    e.ins('divu.w','#0x64,%d0',4)
    e.label('action_pc_01c638')
    e.ins('sub.w','%d0,%d3',2)
    e.label('action_pc_01c63a')
    e.ins('move.w','%d3,0x2(%a1, %d2.w)',4)
    e.label('action_pc_01c63e')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('action_pc_01c644')
    e.ins('divu.w','#0x190,%d0',4)
    e.label('action_pc_01c648')
    e.ins('add.w','%d0,%d7',2)
    e.label('action_pc_01c64a')
    e.ins('lsr.w','#0x1,%d2',2)
    e.label('action_pc_01c64c')
    e.ins('move.w','(%a2, %d2.w),%d3',4)
    e.label('action_pc_01c650')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_01c656')
    e.ins('mulu.w','#0x3d,%d0',4)
    e.label('action_pc_01c65a')
    e.ins('swap','%d0',2)
    e.label('action_pc_01c65c')
    e.ins('mulu.w','%d3,%d0',2)
    e.label('action_pc_01c65e')
    e.ins('divu.w','#0x64,%d0',4)
    e.label('action_pc_01c662')
    e.ins('sub.w','%d0,%d3',2)
    e.label('action_pc_01c664')
    e.ins('move.w','%d3,(%a2, %d2.w)',4)
    e.label('action_pc_01c668')
    e.ins('cmpi.w','#0xa,%d3',4)
    e.label('action_pc_01c66c')
    e.ins('bhi.b','action_pc_01c60c',2)
    e.label('action_pc_01c66e')
    e.ins('move.w','(%a3, %d2.w),%d3',4)
    e.label('action_pc_01c672')
    e.ins('andi.l','#0xffff,%d3',6)
    e.label('action_pc_01c678')
    e.ins('divu.w','#0x5,%d3',4)
    e.label('action_pc_01c67c')
    e.ins('lsr.w','#0x1,%d2',2)
    e.label('action_pc_01c67e')
    e.ins('move.b','#0xff,(%a5, %d2.w)',6)
    e.label('action_pc_01c684')
    e.ins('btst.b','#0x4,(%a4, %d2.w)',6)
    e.label('action_pc_01c68a')
    e.ins('beq.w','action_pc_01c692',4)
    e.label('action_pc_01c68e')
    e.ins('addi.w','#0x14,%d3',4)
    e.label('action_pc_01c692')
    e.ins('add.w','%d3,%d7',2)
    e.label('action_pc_01c694')
    e.ins('bra.w','action_pc_01c60c',4)
    e.label('action_pc_01c698')
    e.ins('move.w','%d7,0xefb8:w',4)
    e.label('action_pc_01c69c')
    e.ins('rts','',2)

LOWERERS = {
    'settle_duel_training_and_troops':_lower_settle_duel_training_and_troops,
    'settle_duel_packets':_lower_settle_duel_packets,
    'apply_duel_disposition':_lower_apply_duel_disposition,
    'detach_zero_readiness_duelists':_lower_detach_zero_readiness_duelists,
    'compute_outcome_force_ratio':_lower_compute_outcome_force_ratio,
    'apply_battlefield_ratio_losses':_lower_apply_battlefield_ratio_losses,
    'apply_city_assigned_heavy_losses':_lower_apply_city_assigned_heavy_losses,
    'consume_city_battle_resources':_lower_consume_city_battle_resources,
    'apply_battlefield_heavy_losses_and_detach':_lower_apply_battlefield_heavy_losses_and_detach,
}

def compile_outcomes(source):
    records = semantic_functions(source,DECLARATIONS,APPROVED)
    for binding in OUTCOMES_BINDINGS:
        field = binding.name+'_frame_fields'
        records[binding.name]['effects'] = dict(
            actual_legacy_projection=records[binding.name]['effects'],
            sole_complete_field_core=records[field]['effects'],
            shared_actual_fields={name:records[name]['effects'] for name in ()})
    return lower_declared({binding.name:records[binding.name] for binding in OUTCOMES_BINDINGS},OUTCOMES_BINDINGS,LOWERERS)

# C58 sole complete fields and compatibility projections; fixed original defaults only.
DECLARATIONS.pop('_multiply_word_parts',None)
DECLARATIONS.pop('_random_fraction',None)
DECLARATIONS.pop('_duel_training_loss',None)
DECLARATIONS.pop('_seek_officer_unbounded',None)
DECLARATIONS.pop('_compact_live_roster',None)
DECLARATIONS.pop('_append_at_roster_end',None)
DECLARATIONS.pop('_candidate_strength_totals',None)
DECLARATIONS.pop('_low_readiness_progress',None)
DECLARATIONS.pop('_assigned_troop_total',None)
DECLARATIONS.update({'settle_duel_training_and_troops': {'signature': 'state: GameState, context: DuelSettlementContext, entry_frame: CommandFrame | None=None', 'returns': 'DuelSettlementResult', 'flow': "memory, entered = _personnel_legacy_entry(state, entry_frame, 100518)\ncontext = checked_context(context, DuelSettlementContext)\nif context.training_carrier != entered.data[2]:\n    raise ValueError('duel training must retain the actual incoming D2 LONG')\nactual = settle_duel_training_and_troops_frame_fields(memory, entered)\nreturn DuelSettlementResult(actual.data[2])"}, 'settle_duel_packets': {'signature': 'state: GameState, context: DuelSettlementContext, entry_frame: CommandFrame | None=None', 'returns': 'CarryOutcome', 'flow': "memory, entered = _personnel_legacy_entry(state, entry_frame, 101120)\ncontext = checked_context(context, DuelSettlementContext)\nif context.training_carrier != entered.data[2]:\n    raise ValueError('duel training must retain the actual incoming D2 LONG')\nactual = settle_duel_packets_frame_fields(memory, entered)\nreturn state.carry_result(actual.status_word & 1)"}, 'apply_duel_disposition': {'signature': 'state: GameState, context: DuelDispositionContext, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': "memory, entered = _personnel_legacy_entry(state, entry_frame, 101268)\ncontext = checked_context(context, DuelDispositionContext)\nif context.officer != entered.data[0] & 65535 or context.disposition != entered.data[2] & 255:\n    raise ValueError('duel disposition must match actual D0 WORD/D2 BYTE')\nactual = apply_duel_disposition_frame_fields(memory, entered)\nreturn None"}, 'detach_zero_readiness_duelists': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 101462)\nactual = detach_zero_readiness_duelists_frame_fields(memory, entered)\nreturn None'}, 'compute_outcome_force_ratio': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'Word', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 115138)\nactual = compute_outcome_force_ratio_frame_fields(memory, entered)\nreturn actual.data[1] & 65535'}, 'apply_battlefield_ratio_losses': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'Word', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 115452)\nactual = apply_battlefield_ratio_losses_frame_fields(memory, entered)\nreturn actual.data[7] & 65535'}, 'apply_city_assigned_heavy_losses': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'Word', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 115612)\nactual = apply_city_assigned_heavy_losses_frame_fields(memory, entered)\nreturn actual.data[7] & 65535'}, 'consume_city_battle_resources': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 115814)\nactual = consume_city_battle_resources_frame_fields(memory, entered)\nreturn None'}, 'apply_battlefield_heavy_losses_and_detach': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'Word', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 116206)\nactual = apply_battlefield_heavy_losses_and_detach_frame_fields(memory, entered)\nreturn actual.data[7] & 65535'}, 'settle_duel_training_and_troops_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'return _personnel_existing_fields(memory, frame, 100518)'}, 'settle_duel_packets_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'return _personnel_existing_fields(memory, frame, 101120)'}, 'apply_duel_disposition_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'return _personnel_existing_fields(memory, frame, 101268)'}, 'detach_zero_readiness_duelists_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'return _personnel_existing_fields(memory, frame, 101462)'}, 'compute_outcome_force_ratio_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'return _personnel_existing_fields(memory, frame, 115138)'}, 'apply_battlefield_ratio_losses_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'return _personnel_existing_fields(memory, frame, 115452)'}, 'apply_city_assigned_heavy_losses_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'return _personnel_existing_fields(memory, frame, 115612)'}, 'consume_city_battle_resources_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'return _personnel_existing_fields(memory, frame, 115814)'}, 'apply_battlefield_heavy_losses_and_detach_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'return _personnel_existing_fields(memory, frame, 116206)'}})
APPROVED.setdefault('contexts_personnel',set()).update(['CommandFrame', 'PersonnelMemory', '_personnel_existing_fields', '_personnel_legacy_entry'])
APPROVED.setdefault('domain',set()).update({'Boundary'})
