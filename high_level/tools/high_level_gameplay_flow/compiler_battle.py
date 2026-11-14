"""Restricted battle structural source admission and ordinary mnemonic lowering.

Explicit semantic input only; no original ROM/ASM/IR/object input or opaque
opcode payload. Fixed original layout; unsupported source changes are rejected.
Actual service/IRQ and CPU behavior are not supplied by this finite compiler.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import BATTLE_BINDINGS

APPROVED = {
    'business_reuse': {'apply_battlefield_heavy_losses_and_detach', 'apply_battlefield_ratio_losses', 'apply_city_assigned_heavy_losses', 'build_battlefield_outcome_candidates', 'build_city_assigned_outcome_candidates', 'build_roster', 'choose_city_head', 'compute_outcome_force_ratio', 'consume_city_battle_resources', 'find_group_at_coordinate', 'initialize_prebattle_head_bytes', 'load_battlefield_map_context', 'read_battlefield_terrain_type', 'rebuild_primary_after_battle', 'rebuild_secondary_after_battle', 'rounded_radial_distance', 'settle_battle_packed_armies', 'settle_duel_packets', 'settle_duel_training_and_troops', 'signed_divmod', 'step_random', 'sum_group_troops'},
    'business_services': {'clear_scene_video_and_state', 'clear_video_sprite_plane', 'copy_video_transfer_descriptor', 'enqueue_sound_command', 'expand_glyph_stream', 'initialize_video_registers_and_planes', 'load_gameplay_scene', 'present_gameplay_message', 'stage_sprite_word_packet'},
    'contexts_battle': {'BattleActionContext', 'BattleFlowResult', 'BattleSceneContext', 'DamagePotentialResult', 'GlyphBatchContext', 'MapTransferContext', 'NearestTerrainTarget', 'PacketInsertionResult', 'PacketMutationContext', 'PacketResourceContext', 'ProgressAllocationContext', 'SceneServiceContext', 'checked_context'},
    'contexts_reuse': {'DuelSettlementContext'},
    'contexts_services': {'GlyphColors'},
    'domain': {'Boundary', 'Cursor', 'GameplayState', 'Long', 'Table', 'Word', 'checked_cursor', 'checked_state', 'checked_table', 'descending_inclusive', 'divu_retained', 'high16', 'low16', 'low8', 'negative_byte', 'negative_word', 'replace_byte', 'replace_word', 's16', 'swap_words', 'u16', 'u32', 'u8', 'uint'},
    (2, 'high_level_battle_ai.business_actions'): {'_battle_action_map_fields', '_deployment_compare_byte', '_deployment_terrain_lookup'},
    (2, 'high_level_battle_ai.business_formation'): {'_first_byte', '_first_compare_long', '_first_sub_word'},
    (2, 'high_level_battle_ai.business_geometry'): {'rounded_deployment_radial_distance_fields'},
    (2, 'high_level_battle_ai.contexts_policy_memory'): {'BattlePolicyMemory'},
    (2, 'high_level_main_flows.business_movement_support'): {'_movement_add_word', '_movement_address_carrier', '_movement_adjust_word', '_movement_arithmetic_long', '_movement_binary_flags', '_movement_compare', '_movement_compare_address', '_movement_frame', '_movement_move', '_movement_move_long', '_movement_multiply_word', '_movement_restore_longs', '_movement_save_longs', '_movement_shift_long', '_movement_shift_word', '_movement_test', '_movement_test_long', 'present_battle_message_fields', 'signed_divmod_fields'},
    (2, 'high_level_main_flows.contexts_gameplay'): {'MovementContinuationBoundary'},
    (2, 'high_level_remaining_flows.business_city'): {'_city_movement_divide', '_recruitment_stitched_score_product', '_settlement_carry_packet_tail_fields', '_settlement_change_header_byte_fields', '_settlement_compact_pair_member_fields', '_settlement_relabel_active_member_fields', '_settlement_seek_pair_member_fields', '_settlement_shift_sample_long_fields', '_settlement_slide_member_tail_fields', '_settlement_store_word_fields', '_settlement_write_byte_fields', '_special_action_shift_long', 'adjust_battle_losing_loyalty_fields', 'classify_duel_object_result_fields', 'initialize_prebattle_head_bytes_fields', 'rebuild_city_links_from_primary_roster_fields', 'settle_group_at_city_fields'},
    (2, 'high_level_scene_flows.business_objects'): {'run_scene_object_controller_fields'},
    (2, 'high_level_scene_flows.business_scene'): {'decode_glyph_rows_to_buffers_fields', 'expand_glyph_stream_fields', 'write_vdp_dictionary_repeat_stream_fields'},
    (2, 'high_level_scene_flows.domain'): {'SceneState'},
}

DECLARATIONS = {'_port': {'signature': 'state, name',
           'returns': None,
           'flow': "return state.table('ram_' + name)"},
 '_shift_word': {'signature': 'carrier, amount',
                 'returns': None,
                 'flow': 'return replace_word(carrier, u16(low16(carrier) << amount))'},
 '_right_word': {'signature': 'carrier, amount',
                 'returns': None,
                 'flow': 'return replace_word(carrier, low16(carrier) >> amount)'},
 '_packed_resource': {'signature': 'packet, offset, retained=0',
                      'returns': None,
                      'flow': 'value = replace_byte(retained, packet.byte(0, offset))\n'
                              'value = _shift_word(value, 8)\n'
                              'value = replace_byte(value, packet.byte(0, offset + 1))\n'
                              'value = u32(value << 8)\n'
                              'value = replace_byte(value, packet.byte(0, offset + 2))\n'
                              'value = u32(value << 8)\n'
                              'return replace_byte(value, packet.byte(0, offset + 3))'},
 '_store_packed_resource': {'signature': 'packet, offset, value',
                            'returns': None,
                            'flow': 'packet.set_byte(0, low8(value), offset + 3)\n'
                                    'value >>= 8\n'
                                    'packet.set_byte(0, low8(value), offset + 2)\n'
                                    'value >>= 8\n'
                                    'packet.set_byte(0, low8(value), offset + 1)\n'
                                    'value = _right_word(value, 8)\n'
                                    'packet.set_byte(0, low8(value), offset)\n'
                                    'return value'},
 '_random_fraction': {'signature': 'state, multiplier, base=0',
                      'returns': None,
                      'flow': 'from .business_reuse import step_random\n'
                              'return u16(high16(u32(low16(step_random(state)) * multiplier)) + '
                              'base)'},
 '_visible_force': {'signature': 'state, force',
                    'returns': None,
                    'flow': "return force == _port(state, 'f67a').word() or force == _port(state, "
                            "'f67c').word() or force == _port(state, 'f67e').word()"},
 '_poll_word': {'signature': 'state, name, predicate',
                'returns': None,
                'flow': 'while not predicate(_port(state, name).word()):\n'
                        "    state.progress('battle-input-wait')"},
 'sample_city_postbattle_reserve': {'signature': 'state: GameplayState',
                                    'returns': 'Long',
                                    'flow': 'checked_state(state)\n'
                                            'from .business_reuse import step_random\n'
                                            'sample = low16(step_random(state))\n'
                                            'scaled = u32(sample * 13)\n'
                                            'carrier = swap_words(scaled)\n'
                                            "offset = u16(_port(state, 'f68a').word() << 2)\n"
                                            "_port(state, 'e59c').set_word(offset, low16(carrier), "
                                            '2)\n'
                                            'return carrier'},
 'distribute_city_battle_progress': {'signature': 'state: GameplayState',
                                     'returns': 'None',
                                     'flow': 'checked_state(state)\n'
                                             'from .business_reuse import '
                                             'build_city_assigned_outcome_candidates\n'
                                             'count = '
                                             'build_city_assigned_outcome_candidates(state)\n'
                                             "budget = u16(_port(state, 'efb8').word() << 1)\n"
                                             'if count == 0:\n'
                                             '    return\n'
                                             'award = divu_retained(budget, count)\n'
                                             "roster = _port(state, 'd300').cursor()\n"
                                             "ability, progress = (_port(state, 'c000'), "
                                             "_port(state, 'be00'))\n"
                                             'while True:\n'
                                             '    member = roster.next_word()\n'
                                             '    if negative_word(member):\n'
                                             '        return\n'
                                             '    offset = u16(member << 1)\n'
                                             '    current = ability.word(offset)\n'
                                             '    if current > progress.word(offset):\n'
                                             '        ability.set_word(offset, min(u16(current + '
                                             'low16(award)), 999))\n'
                                             '    else:\n'
                                             '        current = progress.word(offset)\n'
                                             '        progress.set_word(offset, min(u16(current + '
                                             'low16(award)), 999))'},
 'apply_assigned_city_light_attrition': {'signature': 'state: GameplayState',
                                         'returns': 'None',
                                         'flow': 'checked_state(state)\n'
                                                 'from .business_reuse import '
                                                 'build_city_assigned_outcome_candidates\n'
                                                 'build_city_assigned_outcome_candidates(state)\n'
                                                 "roster = _port(state, 'd300').cursor()\n"
                                                 "troops, readiness = (_port(state, 'c800'), "
                                                 "_port(state, 'b200'))\n"
                                                 'total = 0\n'
                                                 'while True:\n'
                                                 '    member = roster.next_word()\n'
                                                 '    if negative_word(member):\n'
                                                 "        _port(state, 'efba').set_word(0, total)\n"
                                                 '        return\n'
                                                 '    offset = u16(member << 2)\n'
                                                 '    original = troops.long(offset)\n'
                                                 '    loss = divu_retained(u32(low16(original) * '
                                                 '_random_fraction(state, 31, 30)), 100)\n'
                                                 '    troops.set_word(offset, u16(low16(original) '
                                                 '- low16(loss)), 2)\n'
                                                 '    total = u16(total + '
                                                 'low16(divu_retained(low16(loss), 400)))\n'
                                                 '    offset >>= 1\n'
                                                 '    original = readiness.word(offset)\n'
                                                 '    loss = divu_retained(u32(original * '
                                                 '_random_fraction(state, 31)), 100)\n'
                                                 '    remaining = u16(original - low16(loss))\n'
                                                 '    readiness.set_word(offset, 1 if remaining == '
                                                 '0 else remaining)'},
 'consume_city_battle_supply_long': {'signature': 'state: GameplayState',
                                     'returns': 'None',
                                     'flow': 'checked_state(state)\n'
                                             "amount = u32(_port(state, 'efbc').word() * 90)\n"
                                             "offset = u16(_port(state, 'f68a').word() << 2)\n"
                                             "supply = _port(state, 'ed84')\n"
                                             'original = supply.long(offset)\n'
                                             'loss = divu_retained(u32(low16(amount) * '
                                             'low16(original)), 1000)\n'
                                             'supply.set_long(offset, 0 if original < loss else '
                                             'u32(original - loss))\n'
                                             'cost = _random_fraction(state, 501, 500)\n'
                                             "gold = _port(state, 'dffc')\n"
                                             "offset = u16(_port(state, 'f68a').word() << 2)\n"
                                             'original = gold.long(offset)\n'
                                             'gold.set_long(offset, 0 if original < cost else '
                                             'u32(original - cost))'},
 'reduce_city_reserve_after_defeat': {'signature': 'state: GameplayState',
                                      'returns': 'None',
                                      'flow': 'checked_state(state)\n'
                                              'fraction = _random_fraction(state, 51)\n'
                                              "offset = u16(_port(state, 'f68a').word() << 2)\n"
                                              "reserve = _port(state, 'e59c')\n"
                                              'original = reserve.long(offset)\n'
                                              'loss = divu_retained(u32(low16(original) * '
                                              'fraction), 100)\n'
                                              'reserve.set_word(offset, u16(low16(original) - '
                                              'low16(loss)), 2)'},
 'consume_city_battle_supply_word': {'signature': 'state: GameplayState',
                                     'returns': 'None',
                                     'flow': 'checked_state(state)\n'
                                             'fraction = _random_fraction(state, 25, 50)\n'
                                             "offset = u16(_port(state, 'f68a').word() << 2)\n"
                                             "supply = _port(state, 'ed84')\n"
                                             'original = supply.long(offset)\n'
                                             'loss = divu_retained(u32(low16(original) * '
                                             'fraction), 100)\n'
                                             'supply.set_word(offset, u16(low16(original) - '
                                             'low16(loss)), 2)\n'
                                             'cost = _random_fraction(state, 501, 500)\n'
                                             "gold = _port(state, 'dffc')\n"
                                             "offset = u16(_port(state, 'f68a').word() << 2)\n"
                                             'original = gold.long(offset)\n'
                                             'remaining = 0 if low16(original) < cost else '
                                             'replace_word(original, u16(low16(original) - cost))\n'
                                             'gold.set_long(offset, remaining)'},
 'consolidate_city_after_battle': {'signature': 'state: GameplayState',
                                   'returns': 'None',
                                   'flow': 'checked_state(state)\n'
                                           'from .business_reuse import '
                                           'build_battlefield_outcome_candidates, build_roster, '
                                           'choose_city_head\n'
                                           'build_battlefield_outcome_candidates(state)\n'
                                           "assignments, roster = (_port(state, 'cc00'), "
                                           "_port(state, 'd300').cursor())\n"
                                           "city = _port(state, 'f68a').word()\n"
                                           'while True:\n'
                                           '    officer = roster.next_word()\n'
                                           '    if negative_word(officer):\n'
                                           '        break\n'
                                           '    assignments.set_byte(officer, low8(city))\n'
                                           "_port(state, 'f427').set_byte(city, _port(state, "
                                           "'f68d').byte())\n"
                                           "offset = u16(_port(state, 'f68a').word() << 2)\n"
                                           "gold = _port(state, 'dffc')\n"
                                           'gold.set_long(offset, min(u32(gold.long(offset) + '
                                           "_port(state, 'ed88').long(offset)), 999999))\n"
                                           "food, staging = (_port(state, 'e09c'), _port(state, "
                                           "'ee24'))\n"
                                           'staging.set_long(offset, min(u32(food.long(offset) + '
                                           'staging.long(offset)), 999999))\n'
                                           "_port(state, 'f630').set_word(0, 65535)\n"
                                           "build_roster(state, _port(state, 'f68a').word())\n"
                                           "choose_city_head(state, _port(state, 'f68a').word())"},
 'clear_city_officer_links': {'signature': 'state: GameplayState',
                              'returns': 'None',
                              'flow': 'checked_state(state)\n'
                                      "city, links = (_port(state, 'f68a').word(), _port(state, "
                                      "'a050'))\n"
                                      'for officer in descending_inclusive(255):\n'
                                      '    if links.byte(officer) == low8(city):\n'
                                      '        links.set_byte(officer, 0)'},
 'reassign_city_flagged_officers': {'signature': 'state: GameplayState',
                                    'returns': 'None',
                                    'flow': 'checked_state(state)\n'
                                            "owner = u16(_port(state, 'f68e').word() + 41)\n"
                                            "token = _port(state, 'f68a').word() | 64\n"
                                            "assignments = _port(state, 'cc00')\n"
                                            'for officer in descending_inclusive(255):\n'
                                            '    if assignments.byte(officer) == low8(token):\n'
                                            '        assignments.set_byte(officer, low8(owner))'},
 'rebuild_city_links_from_primary_roster': {'signature': 'state: GameplayState',
                                            'returns': 'None',
                                            'flow': 'checked_state(state)\n'
                                                    "links, city = (_port(state, 'a050'), "
                                                    "_port(state, 'f68a').word())\n"
                                                    'for officer in descending_inclusive(255):\n'
                                                    '    if links.byte(officer) & 63 == city:\n'
                                                    '        links.set_byte(officer, 0)\n'
                                                    "roster = _port(state, 'a550').cursor()\n"
                                                    'while True:\n'
                                                    '    officer = roster.next_word()\n'
                                                    '    if negative_word(officer):\n'
                                                    '        return\n'
                                                    '    links.set_byte(officer & 255, '
                                                    'low8(city))'},
 'classify_duel_object_result': {'signature': 'state: GameplayState',
                                 'returns': 'None',
                                 'flow': 'checked_state(state)\n'
                                         "first, second = (_port(state, '7050'), _port(state, "
                                         "'70a0'))\n"
                                         "first_flag, second_flag = (_port(state, '70f0').byte(), "
                                         "_port(state, '70f1').byte())\n"
                                         "selected = _port(state, '80e0').word()\n"
                                         'if selected != first.word(0, 26):\n'
                                         '    first, second = (second, first)\n'
                                         '    first_flag, second_flag = (second_flag, first_flag)\n'
                                         'if first.word(0, 28) == 0:\n'
                                         '    result = 3\n'
                                         'elif second.word(0, 28) == 0:\n'
                                         '    result = 2\n'
                                         'elif first_flag == 1:\n'
                                         '    result = 4\n'
                                         'elif second_flag == 1:\n'
                                         '    result = 5\n'
                                         'elif first_flag != 0:\n'
                                         '    result = 6\n'
                                         'elif second_flag != 0:\n'
                                         '    result = 7\n'
                                         'else:\n'
                                         '    return\n'
                                         "_port(state, '8114').set_word(0, result)"},
 'apply_postbattle_city_economic_attrition': {'signature': 'state: GameplayState',
                                              'returns': 'None',
                                              'flow': 'checked_state(state)\n'
                                                      'fraction = _random_fraction(state, 16, 5)\n'
                                                      "offset = u16(_port(state, 'f68a').word() << "
                                                      '2)\n'
                                                      "target = _port(state, 'e1dc')\n"
                                                      'original = target.long(offset)\n'
                                                      'loss = divu_retained(u32(low16(original) * '
                                                      'fraction), 100)\n'
                                                      'target.set_long(offset, '
                                                      'replace_word(original, u16(low16(original) '
                                                      '- low16(loss))))\n'
                                                      'fraction = _random_fraction(state, 11)\n'
                                                      "target = _port(state, 'e13c')\n"
                                                      'original = target.long(offset)\n'
                                                      'loss = divu_retained(u32(low16(original) * '
                                                      'fraction), 100)\n'
                                                      'target.set_long(offset, '
                                                      'replace_word(original, u16(low16(original) '
                                                      '- low16(loss))))\n'
                                                      'loss = _random_fraction(state, 6, 5)\n'
                                                      "target = _port(state, 'e31c')\n"
                                                      'original = target.word(offset, 2)\n'
                                                      'target.set_word(offset, 0 if original < '
                                                      'loss else u16(original - loss), 2)'},
 'city_reserve_forces_duel_carry': {'signature': 'state: GameplayState',
                                    'returns': None,
                                    'flow': 'checked_state(state)\n'
                                            'from .business_reuse import step_random\n'
                                            'step_random(state)\n'
                                            "offset = u16(_port(state, 'f68a').word() << 2)\n"
                                            "reserve = _port(state, 'e59c').word(offset, 2)\n"
                                            'if reserve >= 30:\n'
                                            '    return state.set_carry(False)\n'
                                            "sample = _port(state, 'f61c').word()\n"
                                            'threshold = high16(u32(sample * 100))\n'
                                            'return state.set_carry(threshold >= reserve)'},
 'group_matches_city_head_carry': {'signature': 'state: GameplayState, candidate: Word',
                                   'returns': None,
                                   'flow': 'checked_state(state)\n'
                                           'uint(candidate, 16)\n'
                                           "if _port(state, 'f6d7').byte() & 2:\n"
                                           "    city = u16(_port(state, 'f68a').word() << 1)\n"
                                           '    matched = candidate == _port(state, '
                                           "'f45e').word(city)\n"
                                           'else:\n'
                                           "    city = _port(state, 'f68a').word()\n"
                                           '    matched = low8(candidate) == _port(state, '
                                           "'a027').byte(city)\n"
                                           'return state.set_carry(matched)'},
 'refresh_packed_group_average': {'signature': 'state: GameplayState, packet: Table',
                                  'returns': 'Long',
                                  'flow': 'checked_state(state)\n'
                                          'checked_table(packet, state)\n'
                                          'count = packet.byte() & 15\n'
                                          'source, attributes = (packet.cursor(13), _port(state, '
                                          "'c400'))\n"
                                          'total = 0\n'
                                          'for _ in descending_inclusive(u16(count - 1)):\n'
                                          '    officer = source.next_byte()\n'
                                          '    total = replace_word(total, u16(low16(total) + '
                                          'attributes.byte(officer)))\n'
                                          'result = divu_retained(total, count)\n'
                                          'packet.set_byte(0, low8(result), 3)\n'
                                          'return result'},
 'copy_selected_city_group_parameter': {'signature': 'state: GameplayState, packet: Table',
                                        'returns': 'None',
                                        'flow': 'checked_state(state)\n'
                                                'checked_table(packet, state)\n'
                                                "selector = u16(_port(state, 'f6d6').word() << 2)\n"
                                                'source = '
                                                'state.table(state.table(98710).long(selector))\n'
                                                'packet.set_byte(0, source.byte(0, 1), 4)'},
 'reserve_packed_group_member_byte': {'signature': 'state: GameplayState, packet: Table, '
                                                   'previous_count: Word',
                                      'returns': 'PacketInsertionResult',
                                      'flow': 'checked_state(state)\n'
                                              'checked_table(packet, state)\n'
                                              'uint(previous_count, 16)\n'
                                              'source = packet.cursor(previous_count)\n'
                                              'source.base = u32(source.base + 13)\n'
                                              'start = source.base\n'
                                              'if previous_count == 0:\n'
                                              '    source.set_byte(0, 0)\n'
                                              'while True:\n'
                                              '    count = source.byte() & 15\n'
                                              '    if count == 0:\n'
                                              '        break\n'
                                              '    source.base = u32(source.base + 13 + count)\n'
                                              'destination = source.cursor()\n'
                                              'destination.base = u32(destination.base + 1)\n'
                                              'destination.set_byte(0, 0)\n'
                                              'while source.base > start:\n'
                                              '    value = source.previous_byte()\n'
                                              '    destination.base = u32(destination.base - 1)\n'
                                              '    destination.set_byte(0, value)\n'
                                              'return PacketInsertionResult(packet, destination, '
                                              'previous_count)'},
 'append_survivors_to_packed_group': {'signature': 'state: GameplayState, context: '
                                                   'PacketMutationContext',
                                      'returns': 'PacketInsertionResult',
                                      'flow': 'context = checked_context(context, '
                                              'PacketMutationContext, state)\n'
                                              'packet = context.packet\n'
                                              'count = packet.byte() & 15\n'
                                              'source = packet.cursor(u16(13 + count))\n'
                                              'append = source.cursor()\n'
                                              'packet.set_byte(0, u8(packet.byte() + '
                                              'context.member_count))\n'
                                              'destination = packet.cursor(u16(13 + u16(count + '
                                              'context.member_count)))\n'
                                              'while True:\n'
                                              '    following = source.byte() & 15\n'
                                              '    if following == 0:\n'
                                              '        break\n'
                                              '    for _ in descending_inclusive(u16(following + '
                                              '12)):\n'
                                              '        '
                                              'destination.append_byte(source.next_byte())\n'
                                              'destination.set_byte(0, 0)\n'
                                              'roster = context.insertion_roster\n'
                                              'while True:\n'
                                              '    officer = roster.word()\n'
                                              '    if negative_word(officer):\n'
                                              '        return PacketInsertionResult(packet, '
                                              'roster, context.member_count)\n'
                                              '    roster.append_word(65535)\n'
                                              '    append.append_byte(low8(officer))'},
 'add_staged_resources_to_packed_group': {'signature': 'state: GameplayState, packet: Table',
                                          'returns': 'None',
                                          'flow': 'checked_state(state)\n'
                                                  'checked_table(packet, state)\n'
                                                  "if _port(state, 'f6d7').byte() & 2:\n"
                                                  "    first, second = (_port(state, 'f69a'), "
                                                  "_port(state, 'f6a2'))\n"
                                                  'else:\n'
                                                  "    first, second = (_port(state, 'f696'), "
                                                  "_port(state, 'f69e'))\n"
                                                  'carrier = _packed_resource(packet, 5)\n'
                                                  'carrier = min(u32(carrier + first.long()), '
                                                  '999999)\n'
                                                  'carrier = _store_packed_resource(packet, 5, '
                                                  'carrier)\n'
                                                  'carrier = replace_byte(carrier, packet.byte(0, '
                                                  '9))\n'
                                                  'carrier = _shift_word(carrier, 8)\n'
                                                  'carrier = replace_byte(carrier, packet.byte(0, '
                                                  '10))\n'
                                                  'carrier = _shift_word(carrier, 8)\n'
                                                  'carrier = replace_byte(carrier, packet.byte(0, '
                                                  '11))\n'
                                                  'carrier = u32(carrier << 8)\n'
                                                  'carrier = replace_byte(carrier, packet.byte(0, '
                                                  '12))\n'
                                                  'carrier = min(u32(carrier + second.long()), '
                                                  '999999)\n'
                                                  '_store_packed_resource(packet, 9, carrier)\n'
                                                  'first.set_long(0, 0)\n'
                                                  'second.set_long(0, 0)'},
 'split_city_resources_into_group': {'signature': 'state: GameplayState, context: '
                                                  'PacketResourceContext',
                                     'returns': 'None',
                                     'flow': 'context = checked_context(context, '
                                             'PacketResourceContext, state)\n'
                                             'from .business_reuse import signed_divmod\n'
                                             "selector = u16(_port(state, 'f6d6').word() << 2)\n"
                                             'first = '
                                             'state.table(state.table(98394).long(selector))\n'
                                             'second = '
                                             'state.table(state.table(98410).long(selector))\n'
                                             'amount = _right_word(first.long(), 8)\n'
                                             "offset = u16(_port(state, 'f3a6').word() << 2)\n"
                                             "troops = _port(state, 'c800')\n"
                                             'selected = u32(troops.long(offset) + 100)\n'
                                             'numerator = u32(low16(amount) * low16(selected))\n'
                                             'denominator = low16(selected)\n'
                                             'while True:\n'
                                             '    member = context.roster.next_word()\n'
                                             '    if negative_word(member):\n'
                                             '        break\n'
                                             '    offset = u16((member & 255) << 2)\n'
                                             '    denominator = u32(denominator + '
                                             'troops.long(offset))\n'
                                             '    denominator = u32(denominator + 100)\n'
                                             'quotient, remainder = signed_divmod(state, '
                                             'numerator, denominator)\n'
                                             'share = u32(quotient << 8)\n'
                                             'first.set_long(0, u32(first.long() - share))\n'
                                             'quantity = _packed_resource(context.packet, 5, '
                                             'remainder)\n'
                                             '_store_packed_resource(context.packet, 5, '
                                             'min(u32(share + quantity), 999999))\n'
                                             'amount = _right_word(second.long(), 8)\n'
                                             'quotient, remainder = signed_divmod(state, '
                                             'u32(low16(amount) * low16(selected)), denominator)\n'
                                             'share = u32(quotient << 8)\n'
                                             'second.set_long(0, u32(second.long() - share))\n'
                                             'quantity = _packed_resource(context.packet, 9, '
                                             'remainder)\n'
                                             '_store_packed_resource(context.packet, 9, '
                                             'min(u32(share + quantity), 999999))'},
 'collect_battle_special_status_members': {'signature': 'state: GameplayState, source: Cursor, '
                                                        'destination: Cursor, side_bits: Word',
                                           'returns': 'Cursor',
                                           'flow': 'checked_state(state)\n'
                                                   'checked_cursor(source, state)\n'
                                                   'checked_cursor(destination, state)\n'
                                                   'uint(side_bits, 16)\n'
                                                   "statuses = _port(state, 'c700')\n"
                                                   'while True:\n'
                                                   '    member = source.next_word()\n'
                                                   '    if negative_word(member):\n'
                                                   '        return destination\n'
                                                   '    member &= 255\n'
                                                   '    if statuses.byte(member) & 16:\n'
                                                   '        destination.append_word(member | '
                                                   'side_bits)'},
 'sample_battle_special_status_factor': {'signature': 'state: GameplayState',
                                         'returns': 'Long',
                                         'flow': 'checked_state(state)\n'
                                                 "selector = _port(state, 'efd2').word()\n"
                                                 'offset = u16(u16(u16(selector << 1) + '
                                                 "_port(state, 'efd2').word()) << 3)\n"
                                                 "destination = _port(state, 'd300').cursor()\n"
                                                 'collect_battle_special_status_members(state, '
                                                 "_port(state, 'a550').cursor(), destination, 0)\n"
                                                 'collect_battle_special_status_members(state, '
                                                 "_port(state, 'a5a4').cursor(), destination, 2)\n"
                                                 'destination.put_word(65535)\n'
                                                 'if not negative_word(_port(state, '
                                                 "'d300').word()):\n"
                                                 '    offset = u16(offset + 4)\n'
                                                 '    source, strengths = (_port(state, '
                                                 "'d300').cursor(), _port(state, 'b600'))\n"
                                                 '    best_value, best_member = (0, 2)\n'
                                                 '    while True:\n'
                                                 '        member = source.next_word()\n'
                                                 '        if negative_word(member):\n'
                                                 '            break\n'
                                                 '        strength = strengths.word(u16(member << '
                                                 '1))\n'
                                                 '        if strength >= best_value:\n'
                                                 '            best_member, best_value = (member, '
                                                 'strength)\n'
                                                 '    if (best_member >> 4 ^ _port(state, '
                                                 "'f6d6').word()) & 2:\n"
                                                 '        offset = u16(offset + 4)\n'
                                                 'from .business_reuse import step_random\n'
                                                 'sample = low16(step_random(state))\n'
                                                 'parameters = state.table(106972)\n'
                                                 'result = swap_words(u32(sample * '
                                                 'parameters.word(offset)))\n'
                                                 'return replace_word(result, u16(low16(result) + '
                                                 'parameters.word(offset, 2)))'},
 'compute_battle_damage_potential': {'signature': 'state: GameplayState, factor: Long, '
                                                  'retained_damage: Long',
                                     'returns': 'DamagePotentialResult',
                                     'flow': 'checked_state(state)\n'
                                             'uint(factor, 32)\n'
                                             'uint(retained_damage, 32)\n'
                                             'factor = u32(low16(factor) * 100)\n'
                                             "strengths = _port(state, 'b600')\n"
                                             "opposing = u16(_port(state, 'f3a6').word() << 1)\n"
                                             'subtraction = u32(strengths.word(opposing) * '
                                             'low16(factor))\n'
                                             "acting = u16(_port(state, 'f3f2').word() << 1)\n"
                                             'numerator = u32(strengths.word(acting) * 1000)\n'
                                             'if numerator < subtraction:\n'
                                             '    return DamagePotentialResult(u32(numerator - '
                                             'subtraction), replace_word(retained_damage, 0))\n'
                                             'numerator = u32(numerator - subtraction)\n'
                                             'divisor = u16(_port(state, '
                                             "'c000').word(u16(_port(state, 'f3a6').word() << 1)) "
                                             '+ 100)\n'
                                             'result = divu_retained(numerator, divisor)\n'
                                             'damage = replace_word(retained_damage, '
                                             'low16(result))\n'
                                             'if low16(result) > 700:\n'
                                             '    result = replace_word(result, 700)\n'
                                             'return DamagePotentialResult(result, damage)'},
 'find_nearest_secondary_terrain_target': {'signature': 'state: GameplayState', 'returns': 'NearestTerrainTarget', 'flow': 'return find_nearest_secondary_terrain_target_observations(state)[0]'},
 'secondary_roster_has_terrain_six_carry': {'signature': 'state: GameplayState',
                                            'returns': None,
                                            'flow': 'checked_state(state)\n'
                                                    'from .business_reuse import '
                                                    'load_battlefield_map_context, '
                                                    'read_battlefield_terrain_type\n'
                                                    'map_context = '
                                                    'load_battlefield_map_context(state)\n'
                                                    'roster, positions = (_port(state, '
                                                    "'a5a4').cursor(), _port(state, 'a150'))\n"
                                                    'while True:\n'
                                                    '    member = roster.next_word()\n'
                                                    '    if negative_word(member):\n'
                                                    '        return state.set_carry(False)\n'
                                                    '    offset = u16(member << 2)\n'
                                                    '    x = positions.word(offset) >> 7\n'
                                                    '    y = positions.word(offset, 2) >> 7\n'
                                                    '    if '
                                                    'low8(read_battlefield_terrain_type(state, '
                                                    'map_context, x, y)) == 6:\n'
                                                    '        return state.set_carry(True)'},
 'merge_city_survivor_rosters': {'signature': 'state: GameplayState, destination: Cursor',
                                 'returns': 'Cursor',
                                 'flow': 'checked_state(state)\n'
                                         'checked_cursor(destination, state)\n'
                                         "source = _port(state, 'a5ce' if _port(state, "
                                         "'f6d7').byte() & 2 else 'a57a').cursor()\n"
                                         'source_head = source.cursor()\n'
                                         'count = 0\n'
                                         'while not negative_word(destination.next_word()):\n'
                                         '    count = u16(count + 1)\n'
                                         'destination.base = u32(destination.base - 2)\n'
                                         'while True:\n'
                                         '    member = source.next_word()\n'
                                         '    destination.append_word(member)\n'
                                         '    if negative_word(member):\n'
                                         '        break\n'
                                         '    count = u16(count + 1)\n'
                                         'source_head.put_word(65535)\n'
                                         'if count <= 10:\n'
                                         '    return destination\n'
                                         'inclusive_extra = u16(count - 11)\n'
                                         'destination.base = u32(destination.base - 2)\n'
                                         "token = _port(state, 'f68a').word() | 128\n"
                                         "assignments = _port(state, 'cc00')\n"
                                         "owner = _port(state, 'f68c').word()\n"
                                         "if _port(state, 'f6d7').byte() & 2:\n"
                                         "    owner = _port(state, 'f68e').word()\n"
                                         'notify = _visible_force(state, owner)\n'
                                         'for _ in descending_inclusive(inclusive_extra):\n'
                                         '    member = destination.previous_word()\n'
                                         '    if notify:\n'
                                         "        _port(state, 'f3d0').set_word(0, member)\n"
                                         '    assignments.set_byte(member, low8(token))\n'
                                         '    if notify:\n'
                                         "        _port(state, 'f740').set_word(0, 320)\n"
                                         '        present_battle_message(state)\n'
                                         'destination.put_word(65535)\n'
                                         'return destination'},
 'assign_city_survivor_roster_tokens': {'signature': 'state: GameplayState, roster: Cursor',
                                        'returns': 'None',
                                        'flow': 'checked_state(state)\n'
                                                'checked_cursor(roster, state)\n'
                                                'saved_base = roster.base\n'
                                                'merge_city_survivor_rosters(state, roster)\n'
                                                'roster.base = saved_base\n'
                                                "assignments, positions = (_port(state, 'cc00'), "
                                                "_port(state, 'a150'))\n"
                                                "_port(state, 'f68a').word()\n"
                                                "owner = _port(state, 'f68c').word()\n"
                                                "if _port(state, 'f6d7').byte() & 2:\n"
                                                "    owner = _port(state, 'f68e').word()\n"
                                                'token = u16(owner + 105)\n'
                                                'while True:\n'
                                                '    member = roster.next_word()\n'
                                                '    if negative_word(member):\n'
                                                '        roster.base = saved_base\n'
                                                '        return\n'
                                                '    member &= 255\n'
                                                '    assignments.set_byte(member, low8(token))\n'
                                                '    positions.set_long(u16(member << 2), 0)'},
 'remove_queued_packed_group_member': {'signature': 'state: GameplayState, queue: Cursor, '
                                                    'member_carrier: Long',
                                       'returns': 'Cursor',
                                       'flow': 'checked_state(state)\n'
                                               'checked_cursor(queue, state)\n'
                                               'uint(member_carrier, 32)\n'
                                               "records = _port(state, '3000').cursor()\n"
                                               'while True:\n'
                                               '    if negative_byte(records.next_byte()):\n'
                                               '        return queue\n'
                                               '    if records.next_byte() != '
                                               'low8(member_carrier):\n'
                                               '        while records.next_byte() != 0:\n'
                                               '            pass\n'
                                               '        continue\n'
                                               '    if records.byte(0, 1) != 128:\n'
                                               '        return queue\n'
                                               '    owner = records.byte(0, 2)\n'
                                               "    if owner != _port(state, 'f68b').byte():\n"
                                               '        return queue\n'
                                               '    while True:\n'
                                               '        value = queue.next_byte()\n'
                                               '        queue.set_byte(0, value, -3)\n'
                                               '        if value == 0:\n'
                                               '            return queue\n'
                                               '        value = queue.next_byte()\n'
                                               '        queue.set_byte(0, value, -3)'},
 'compact_active_packed_group_queue': {'signature': 'state: GameplayState, retained_member: Long=0',
                                       'returns': 'Cursor',
                                       'flow': 'checked_state(state)\n'
                                               'uint(retained_member, 32)\n'
                                               "queue = _port(state, '39b2').cursor(_port(state, "
                                               "'3bb2').word())\n"
                                               'while True:\n'
                                               '    if queue.next_byte() == 0:\n'
                                               '        return queue\n'
                                               '    retained_member = '
                                               'replace_byte(retained_member, queue.next_byte())\n'
                                               '    remove_queued_packed_group_member(state, '
                                               'queue, retained_member)'},
 'cache_battle_roster_totals': {'signature': 'state: GameplayState',
                                'returns': 'None',
                                'flow': 'checked_state(state)\n'
                                        'from .business_reuse import sum_group_troops\n'
                                        "troops = _port(state, 'c800')\n"
                                        'total, count = sum_group_troops(state, _port(state, '
                                        "'a550').cursor(), troops)\n"
                                        "_port(state, 'f6ae').set_long(0, total)\n"
                                        "_port(state, 'f6a6').set_word(0, count)\n"
                                        'total, count = sum_group_troops(state, _port(state, '
                                        "'a5a4').cursor(), troops)\n"
                                        "_port(state, 'f6b2').set_long(0, total)\n"
                                        "_port(state, 'f6a8').set_word(0, count)\n"
                                        "offset = u16(_port(state, 'f68a').word() << 2)\n"
                                        "_port(state, 'f6be').set_word(0, _port(state, "
                                        "'e59c').word(offset, 2))"},
 'upload_battlefield_tilemap': {'signature': 'state: GameplayState, retained_tile: Long=0',
                                'returns': 'Long',
                                'flow': 'checked_state(state)\n'
                                        'uint(retained_tile, 32)\n'
                                        'source = state.table(u32(607720 + _port(state, '
                                        "'f68a').word() * 2240)).cursor()\n"
                                        'command = 1342177283\n'
                                        'tile = retained_tile\n'
                                        'for _ in descending_inclusive(27):\n'
                                        '    state.write(12582916, 4, command)\n'
                                        '    for _ in descending_inclusive(39):\n'
                                        '        tile = replace_word(tile, source.next_word())\n'
                                        '        if tile & 256:\n'
                                        '            tile = replace_word(tile, low16(tile) | '
                                        '1792)\n'
                                        '        state.write(12582912, 2, low16(tile))\n'
                                        '    command = u32(command + 8388608)\n'
                                        'return tile'},
 'upload_battle_background_planes': {'signature': 'state: GameplayState, count_carrier: Long=0',
                                     'returns': 'Long',
                                     'flow': 'checked_state(state)\n'
                                             'uint(count_carrier, 32)\n'
                                             'from .business_services import '
                                             'copy_video_transfer_descriptor\n'
                                             'for index, command in ((0, 1610612739), (4, '
                                             '1073741825)):\n'
                                             '    state.write(12582916, 4, command)\n'
                                             '    source = '
                                             'state.table(state.table(429076).long(index)).cursor()\n'
                                             '    auxiliary = '
                                             'state.table(state.table(429084).long(index)).cursor()\n'
                                             '    count_carrier = _right_word(count_carrier, 1)\n'
                                             '    parameters = state.table(442118).cursor()\n'
                                             '    count_carrier = replace_word(count_carrier, '
                                             'parameters.word(index // 2))\n'
                                             '    result = state.service_at(44540, '
                                             'MapTransferContext(source, auxiliary, parameters, '
                                             'count_carrier))\n'
                                             '    if type(result) is not MapTransferContext:\n'
                                             "        raise Boundary('ADFC requires a real typed "
                                             "map-transfer outcome')\n"
                                             '    result.validate(state)\n'
                                             '    count_carrier = result.inclusive_count\n'
                                             'copy_video_transfer_descriptor(state, 6)\n'
                                             'return replace_word(count_carrier, 6)'},
 'append_force_head_glyphs': {'signature': 'state: GameplayState, context: GlyphBatchContext',
                              'returns': 'GlyphBatchContext',
                              'flow': 'context = checked_context(context, GlyphBatchContext, '
                                      'state)\n'
                                      'if context.source.word(0, 4) != 63:\n'
                                      '    request = GlyphBatchContext(context.source, '
                                      'context.destination, context.background, '
                                      'context.foreground, replace_word(context.inclusive_count, '
                                      '2))\n'
                                      '    result = state.service_at(44682, request)\n'
                                      '    if type(result) is not GlyphBatchContext:\n'
                                      "        raise Boundary('AE8A requires actual typed glyph "
                                      "conversion outcome')\n"
                                      '    return result.validate(state)\n'
                                      'for _ in descending_inclusive(15):\n'
                                      '    context.destination.append_long(286331153)\n'
                                      'request = GlyphBatchContext(context.source, '
                                      'context.destination, context.background, '
                                      'context.foreground, replace_word(context.inclusive_count, '
                                      '1))\n'
                                      'result = state.service_at(44682, request)\n'
                                      'if type(result) is not GlyphBatchContext:\n'
                                      "    raise Boundary('AE8A requires actual typed glyph "
                                      "conversion outcome')\n"
                                      'result.validate(state)\n'
                                      'for _ in descending_inclusive(15):\n'
                                      '    result.destination.append_long(286331153)\n'
                                      'return GlyphBatchContext(result.source, result.destination, '
                                      'result.background, result.foreground, '
                                      'replace_word(result.inclusive_count, 65535))'},
 'present_battle_message': {'signature': 'state: GameplayState',
                            'returns': 'None',
                            'flow': 'checked_state(state)\n'
                                    'from .business_services import clear_scene_video_and_state\n'
                                    "saved_scene = _port(state, 'f612').word()\n"
                                    "saved_menu = _port(state, 'f362').word()\n"
                                    "_port(state, 'f612').set_word(0, 1044)\n"
                                    "_port(state, 'f362').set_word(0, 0)\n"
                                    "_port(state, 'f600').set_word(0, 0)\n"
                                    'state.set_status_word(9472)\n'
                                    'while True:\n'
                                    "    _poll_word(state, 'f600', lambda value: value != 0)\n"
                                    "    if _port(state, 'f600').word() != 40:\n"
                                    '        break\n'
                                    '    clear_scene_video_and_state(state)\n'
                                    "    _port(state, 'f600').set_word(0, 0)\n"
                                    '    state.set_status_word(9472)\n'
                                    'state.set_status_word(9984)\n'
                                    "_port(state, 'f362').set_word(0, saved_menu)\n"
                                    "_port(state, 'f612').set_word(0, saved_scene)"},
 'integrate_selected_officer_into_packed_group': {'signature': 'state: GameplayState',
                                                  'returns': 'Table',
                                                  'flow': 'checked_state(state)\n'
                                                          'from .business_reuse import '
                                                          'find_group_at_coordinate\n'
                                                          'selector = u16((_port(state, '
                                                          "'f6d6').word() & 2) << 1)\n"
                                                          'selected = '
                                                          'state.table(state.table(98072).long(selector)).cursor()\n'
                                                          'selected_head = selected.cursor()\n'
                                                          'count_view = '
                                                          'state.table(state.table(98080).long(selector))\n'
                                                          'coordinate_view = '
                                                          'state.table(state.table(98088).long(selector))\n'
                                                          'count_view.set_word(0, '
                                                          'u16(count_view.word() - 1))\n'
                                                          "officer = _port(state, 'f3a6').word()\n"
                                                          'if not '
                                                          'group_matches_city_head_carry(state, '
                                                          'officer).carry:\n'
                                                          '    while selected.next_word() != '
                                                          'officer:\n'
                                                          '        pass\n'
                                                          '    while True:\n'
                                                          '        value = selected.next_word()\n'
                                                          '        selected.set_word(0, value, '
                                                          '-4)\n'
                                                          '        if negative_word(value):\n'
                                                          '            break\n'
                                                          '    coordinate = '
                                                          'coordinate_view.word()\n'
                                                          '    packet = '
                                                          'find_group_at_coordinate(state, '
                                                          'coordinate)\n'
                                                          '    packet.set_byte(0, coordinate >> 8, '
                                                          '1)\n'
                                                          '    packet.set_byte(0, '
                                                          'low8(coordinate), 2)\n'
                                                          '    previous = packet.byte() & 15\n'
                                                          '    if previous == 0:\n'
                                                          '        for displacement in range(5, '
                                                          '14):\n'
                                                          '            packet.set_byte(0, 0, '
                                                          'displacement)\n'
                                                          '    packet.set_byte(0, u8(packet.byte() '
                                                          '+ 1))\n'
                                                          '    '
                                                          'reserve_packed_group_member_byte(state, '
                                                          'packet, previous)\n'
                                                          '    packet.set_byte(u16(13 + previous), '
                                                          "_port(state, 'f3a7').byte())\n"
                                                          '    '
                                                          'split_city_resources_into_group(state, '
                                                          'PacketResourceContext(packet, '
                                                          'selected_head))\n'
                                                          '    '
                                                          'add_staged_resources_to_packed_group(state, '
                                                          'packet)\n'
                                                          "    assignments = _port(state, 'cc00')\n"
                                                          '    officer = _port(state, '
                                                          "'f3a6').word()\n"
                                                          '    assignments.set_byte(officer, '
                                                          'assignments.byte(officer) | 64)\n'
                                                          '    _port(state, '
                                                          "'a150').set_long(u16(officer << 2), 0)\n"
                                                          'else:\n'
                                                          '    survivors = selected.cursor()\n'
                                                          '    saved_base = survivors.base\n'
                                                          '    merge_city_survivor_rosters(state, '
                                                          'survivors)\n'
                                                          '    survivors.base = saved_base\n'
                                                          '    counter_source = selected.cursor()\n'
                                                          '    member_count = 0\n'
                                                          '    while not '
                                                          'negative_word(counter_source.next_word()):\n'
                                                          '        member_count = u16(member_count '
                                                          '+ 1)\n'
                                                          '    coordinate = '
                                                          'coordinate_view.word()\n'
                                                          '    packet = '
                                                          'find_group_at_coordinate(state, '
                                                          'coordinate)\n'
                                                          '    packet.set_byte(0, coordinate >> 8, '
                                                          '1)\n'
                                                          '    packet.set_byte(0, '
                                                          'low8(coordinate), 2)\n'
                                                          '    if packet.byte() & 15 == 0:\n'
                                                          '        for displacement in range(5, '
                                                          '14):\n'
                                                          '            packet.set_byte(0, 0, '
                                                          'displacement)\n'
                                                          '    '
                                                          'append_survivors_to_packed_group(state, '
                                                          'PacketMutationContext(packet, selected, '
                                                          'survivors, member_count))\n'
                                                          '    '
                                                          'assign_city_survivor_roster_tokens(state, '
                                                          'survivors)\n'
                                                          'refresh_packed_group_average(state, '
                                                          'packet)\n'
                                                          'copy_selected_city_group_parameter(state, '
                                                          'packet)\n'
                                                          'return packet'},
 'award_city_reserve_attrition': {'signature': 'state: GameplayState',
                                  'returns': 'Long',
                                  'flow': 'checked_state(state)\n'
                                          'from .business_reuse import step_random\n'
                                          'random = low16(step_random(state))\n'
                                          'loss = replace_word(swap_words(u32(random * 6)), '
                                          'u16(high16(u32(random * 6)) + 10))\n'
                                          "factor = _port(state, '3ed6').word()\n"
                                          'factor = divu_retained(u16(factor + 100), 10)\n'
                                          'loss = u32(low16(loss) * low16(factor))\n'
                                          "previous_troops = u32(_port(state, '3ed2').long() + "
                                          '500)\n'
                                          'factor = divu_retained(previous_troops, 100)\n'
                                          'loss = u32(low16(loss) * low16(factor))\n'
                                          "officer_offset = u16(_port(state, 'f3f2').word() << 1)\n"
                                          "factor = u16(_port(state, 'b400').word(officer_offset) "
                                          "+ _port(state, 'b600').word(officer_offset))\n"
                                          'factor = divu_retained(factor, 10)\n'
                                          'loss = divu_retained(u32(low16(loss) * low16(factor)), '
                                          '20000)\n'
                                          "if _port(state, '3eda').word() != 0:\n"
                                          '    loss = replace_word(loss, u16(low16(loss) * 6))\n'
                                          '    loss = divu_retained(low16(loss), 10)\n'
                                          "offset = u16(_port(state, 'f68a').word() << 2)\n"
                                          "reserves = _port(state, 'e59c')\n"
                                          'previous = reserves.long(offset)\n'
                                          'remaining = u16(low16(previous) - low16(loss))\n'
                                          'if low16(previous) < low16(loss):\n'
                                          '    if not '
                                          'secondary_roster_has_terrain_six_carry(state).carry:\n'
                                          "        owner = _port(state, 'f68c').word()\n"
                                          '        if _visible_force(state, owner):\n'
                                          "            _port(state, '7026').set_word(0, 24)\n"
                                          '            from .business_services import '
                                          'load_gameplay_scene\n'
                                          '            load_gameplay_scene(state)\n'
                                          "        saved_owner = _port(state, 'f376').word()\n"
                                          "        _port(state, 'f376').set_word(0, _port(state, "
                                          "'f68c').word())\n"
                                          "        force_offset = u16(_port(state, 'f68e').word() "
                                          '<< 1)\n'
                                          "        _port(state, 'f3d0').set_word(0, _port(state, "
                                          "'e640').word(force_offset))\n"
                                          "        _port(state, 'f740').set_word(0, 319)\n"
                                          "        _port(state, 'f6d7').set_byte(0, _port(state, "
                                          "'f6d7').byte() ^ 2)\n"
                                          '        present_battle_message(state)\n'
                                          "        _port(state, 'f6d7').set_byte(0, _port(state, "
                                          "'f6d7').byte() ^ 2)\n"
                                          "        _port(state, 'f376').set_word(0, saved_owner)\n"
                                          "        _port(state, 'f612').set_word(0, 1041)\n"
                                          "        _port(state, 'f362').set_word(0, 0)\n"
                                          "        _port(state, 'f6d6').set_word(0, 0)\n"
                                          '        remaining = 0\n'
                                          'reserves.set_word(offset, remaining, 2)\n'
                                          'return loss'},
 'resolve_city_battle_damage': {'signature': 'state: GameplayState, retained_damage: Long=0',
                                'returns': 'Long',
                                'flow': 'checked_state(state)\n'
                                        'uint(retained_damage, 32)\n'
                                        'from .business_reuse import step_random\n'
                                        'from .business_services import load_gameplay_scene\n'
                                        'step_random(state)\n'
                                        "offset = u16(_port(state, 'f68a').word() << 2)\n"
                                        "city_amount = _port(state, 'e59c').long(offset)\n"
                                        "sample = _port(state, 'f61c').word()\n"
                                        'fraction = u16(high16(u32(sample * 6)) + 5)\n'
                                        'debit = u32(low16(city_amount) * fraction)\n'
                                        "selector = u16(_port(state, 'f6d6').word() << 2)\n"
                                        'resources = '
                                        'state.table(state.table(99312).long(selector))\n'
                                        'available = resources.long()\n'
                                        'shortage = int(available < debit)\n'
                                        'remaining = 0 if shortage else u32(available - debit)\n'
                                        "_port(state, '3eda').set_word(0, shortage)\n"
                                        'resources.set_long(0, remaining)\n'
                                        "troops = _port(state, 'c800')\n"
                                        "acting_offset = u16(_port(state, 'f3f2').word() << 2)\n"
                                        "_port(state, '3ed2').set_long(0, "
                                        'troops.long(acting_offset))\n'
                                        "_port(state, '3ed6').set_word(0, 1792)\n"
                                        "if not negative_word(_port(state, 'f3a6').word()):\n"
                                        '    sampled = sample_battle_special_status_factor(state)\n'
                                        '    potential = compute_battle_damage_potential(state, '
                                        'sampled, retained_damage)\n'
                                        '    damage = potential.effective_damage\n'
                                        "    _port(state, '3ed6').set_word(0, low16(damage))\n"
                                        '    damage = replace_word(damage, u16(low16(damage) + '
                                        '200))\n'
                                        "    offset = u16(_port(state, 'f68a').word() << 2)\n"
                                        "    city_amount = _port(state, 'e59c').long(offset)\n"
                                        '    damage = u32(low16(damage) * u16(100 - '
                                        'low16(city_amount)))\n'
                                        '    damage = divu_retained(damage, 100)\n'
                                        "    acting_offset = u16(_port(state, 'f3f2').word() << "
                                        '1)\n'
                                        '    acting_ability = _port(state, '
                                        "'c000').word(acting_offset)\n"
                                        '    damage = divu_retained(u32(low16(damage) * '
                                        'acting_ability), 100)\n'
                                        "    if _port(state, '3eda').word() != 0:\n"
                                        '        damage = divu_retained(u32(low16(damage) << 2), '
                                        '10)\n'
                                        "    opposing_offset = u16(_port(state, 'f3a6').word() << "
                                        '2)\n'
                                        '    original = troops.long(opposing_offset)\n'
                                        '    reduced = 0 if low16(original) < low16(damage) else '
                                        'u16(low16(original) - low16(damage))\n'
                                        '    troops.set_long(opposing_offset, '
                                        'replace_word(original, reduced))\n'
                                        '    progress = divu_retained(u32(low16(damage) << 1), '
                                        '400)\n'
                                        "    acting_offset = u16(_port(state, 'f3f2').word() << "
                                        '1)\n'
                                        "    ability = _port(state, 'c000')\n"
                                        '    original_ability = ability.word(acting_offset)\n'
                                        '    ability.set_word(acting_offset, '
                                        'min(u16(original_ability + low16(progress)), 999))\n'
                                        '    damage = divu_retained(u32(low16(damage) * 2000), '
                                        'original_ability)\n'
                                        "    if _port(state, '3eda').word() != 0:\n"
                                        '        damage = _shift_word(damage, 1)\n'
                                        '    acting_troop_offset = u16(acting_offset << 1)\n'
                                        '    original = troops.long(acting_troop_offset)\n'
                                        '    reduced = 0 if low16(original) < low16(damage) else '
                                        'u16(low16(original) - low16(damage))\n'
                                        '    troops.set_long(acting_troop_offset, '
                                        'replace_word(original, reduced))\n'
                                        '    damage = divu_retained(low16(damage), 400)\n'
                                        "    opposing_offset = u16(_port(state, 'f3a6').word() << "
                                        '1)\n'
                                        '    original = ability.word(opposing_offset)\n'
                                        '    ability.set_word(opposing_offset, min(u16(original + '
                                        'low16(damage)), 999))\n'
                                        'award = award_city_reserve_attrition(state)\n'
                                        "offset = u16(_port(state, 'f3f2').word() << 1)\n"
                                        "progress = _port(state, 'be00')\n"
                                        'progress.set_word(offset, min(u16(progress.word(offset) + '
                                        'low16(award)), 999))\n'
                                        "owner = _port(state, 'f68c').word()\n"
                                        'if _visible_force(state, owner) and _port(state, '
                                        "'f612').word() != 1041:\n"
                                        "    _port(state, '7026').set_word(0, 24)\n"
                                        '    load_gameplay_scene(state)\n'
                                        'return award'},
 'settle_city_battle_outcome': {'signature': 'state: GameplayState',
                                'returns': 'None',
                                'flow': 'checked_state(state)\n'
                                        'from .business_reuse import compute_outcome_force_ratio, '
                                        'apply_battlefield_ratio_losses, '
                                        'apply_city_assigned_heavy_losses, '
                                        'consume_city_battle_resources, '
                                        'apply_battlefield_heavy_losses_and_detach, '
                                        'rebuild_primary_after_battle, '
                                        'rebuild_secondary_after_battle\n'
                                        'from .business_services import present_gameplay_message, '
                                        'stage_sprite_word_packet\n'
                                        "_port(state, 'f352').set_word(0, 32)\n"
                                        "owners, city = (_port(state, 'f427'), _port(state, "
                                        "'f68a').word())\n"
                                        "_port(state, 'f68e').set_word(0, 0)\n"
                                        "_port(state, 'f68f').set_byte(0, owners.byte(city))\n"
                                        "links = _port(state, 'a050')\n"
                                        'officer = 65535\n'
                                        'for candidate in descending_inclusive(255):\n'
                                        '    officer = candidate\n'
                                        '    if links.byte(candidate) == low8(city):\n'
                                        '        break\n'
                                        'else:\n'
                                        '    officer = 65535\n'
                                        "resident_city = _port(state, 'cc00').byte(officer) & 63\n"
                                        "_port(state, 'f68c').set_word(0, 0)\n"
                                        "_port(state, 'f68d').set_byte(0, "
                                        'owners.byte(resident_city))\n'
                                        'def notify(message):\n'
                                        "    rulers = _port(state, 'e640')\n"
                                        "    _port(state, 'f3d0').set_word(0, "
                                        "rulers.word(u16(_port(state, 'f68c').word() << 1)))\n"
                                        "    _port(state, 'f3d2').set_word(0, "
                                        "rulers.word(u16(_port(state, 'f68e').word() << 1)))\n"
                                        "    saved = _port(state, 'f362').word()\n"
                                        "    _port(state, 'f740').set_word(0, message)\n"
                                        "    _port(state, 'f608').set_word(0, 300)\n"
                                        "    _port(state, 'f362').set_word(0, 0)\n"
                                        '    present_gameplay_message(state)\n'
                                        "    _port(state, 'f362').set_word(0, saved)\n"
                                        "rulers = _port(state, 'e640')\n"
                                        "_port(state, 'f3d0').set_word(0, "
                                        "rulers.word(u16(_port(state, 'f68c').word() << 1)))\n"
                                        "_port(state, 'f3d2').set_word(0, "
                                        "rulers.word(u16(_port(state, 'f68e').word() << 1)))\n"
                                        "saved = _port(state, 'f362').word()\n"
                                        "_port(state, 'f740').set_word(0, 159)\n"
                                        "_port(state, 'f362').set_word(0, 0)\n"
                                        "_port(state, 'f608').set_word(0, 300)\n"
                                        "_port(state, 'f362').set_word(0, 0)\n"
                                        'present_gameplay_message(state)\n'
                                        "_port(state, 'f362').set_word(0, saved)\n"
                                        'consume_city_battle_resources(state)\n'
                                        'ratio = compute_outcome_force_ratio(state)\n'
                                        'if ratio < 10:\n'
                                        '    apply_battlefield_ratio_losses(state)\n'
                                        '    apply_city_assigned_heavy_losses(state)\n'
                                        '    distribute_city_battle_progress(state)\n'
                                        '    state.service_at(116194, '
                                        'ProgressAllocationContext())\n'
                                        '    sample_city_postbattle_reserve(state)\n'
                                        '    consume_city_battle_supply_long(state)\n'
                                        '    rebuild_primary_after_battle(state)\n'
                                        '    consolidate_city_after_battle(state)\n'
                                        '    reassign_city_flagged_officers(state)\n'
                                        "    _port(state, 'f6d6').set_word(0, 0)\n"
                                        "    _port(state, 'f646').set_word(0, _port(state, "
                                        "'f68a').word())\n"
                                        '    notify(161)\n'
                                        'else:\n'
                                        '    apply_battlefield_heavy_losses_and_detach(state)\n'
                                        '    apply_assigned_city_light_attrition(state)\n'
                                        '    distribute_city_battle_progress(state)\n'
                                        '    state.service_at(116194, '
                                        'ProgressAllocationContext())\n'
                                        '    reduce_city_reserve_after_defeat(state)\n'
                                        '    consume_city_battle_supply_word(state)\n'
                                        '    rebuild_secondary_after_battle(state)\n'
                                        "    _port(state, 'f6d6').set_word(0, 2)\n"
                                        "    _port(state, 'f646').set_word(0, _port(state, "
                                        "'f68a').word())\n"
                                        '    notify(162)\n'
                                        'apply_postbattle_city_economic_attrition(state)\n'
                                        'clear_city_officer_links(state)\n'
                                        "city = _port(state, 'f68a').word()\n"
                                        "_port(state, 'ea37').set_byte(city, 0)\n"
                                        "_port(state, 'f612').set_word(0, 513)\n"
                                        'stage_sprite_word_packet(state, '
                                        'state.table(115110).cursor(), 3221225510, 7, 51714)\n'
                                        "offset = u16(_port(state, 'f68a').word() << 2)\n"
                                        "_port(state, 'ee24').set_long(offset, 0)\n"
                                        "_port(state, 'ed84').set_long(offset, 0)\n"
                                        "_port(state, 'a622').set_byte(0, _port(state, "
                                        "'f68d').byte())\n"
                                        "_port(state, 'a623').set_byte(0, _port(state, "
                                        "'f68f').byte())"},
 'upload_battle_scene_labels': {'signature': 'state: GameplayState, context: BattleSceneContext',
                                'returns': 'BattleSceneContext',
                                'flow': 'context = checked_context(context, BattleSceneContext, '
                                        'state)\n'
                                        'from .business_services import expand_glyph_stream\n'
                                        'from .contexts_services import GlyphColors\n'
                                        'state.write(12582916, 4, 1075838978)\n'
                                        'for _ in descending_inclusive(31):\n'
                                        '    state.write(12582912, 4, 286331153)\n'
                                        'background = replace_word(context.background, 1)\n'
                                        'foreground = replace_word(context.foreground, 3)\n'
                                        'count = replace_word(context.glyph_count, 10)\n'
                                        'def glyphs(source, destination, inclusive_count):\n'
                                        '    request = GlyphBatchContext(source, destination, '
                                        'background, foreground, inclusive_count)\n'
                                        '    result = state.service_at(44682, request)\n'
                                        '    if type(result) is not GlyphBatchContext:\n'
                                        "        raise Boundary('AE8A glyph service requires its "
                                        "actual typed result')\n"
                                        '    return result.validate(state)\n'
                                        'def upload(source, inclusive_count):\n'
                                        '    for _ in descending_inclusive(inclusive_count):\n'
                                        '        state.write(12582912, 4, source.next_long())\n'
                                        'result = glyphs(state.table(442200).cursor(), '
                                        "_port(state, 'd300').cursor(), count)\n"
                                        'background, foreground, count = (result.background, '
                                        'result.foreground, result.inclusive_count)\n'
                                        "upload(_port(state, 'd300').cursor(), 351)\n"
                                        'state.write(12582916, 4, 1207959554)\n'
                                        "offset = u16(_port(state, 'f68a').word() << 2)\n"
                                        'result = glyphs(state.table(565778).cursor(offset), '
                                        "_port(state, 'd300').cursor(), replace_word(count, 1))\n"
                                        'background, foreground, count = (result.background, '
                                        'result.foreground, result.inclusive_count)\n'
                                        "upload(_port(state, 'd300').cursor(), 63)\n"
                                        "destination = _port(state, 'd300').cursor()\n"
                                        "for owner_port in ('f68e', 'f68c'):\n"
                                        '    owner_offset = u16(_port(state, owner_port).word() << '
                                        '1)\n'
                                        "    ruler = _port(state, 'e640').word(owner_offset)\n"
                                        '    label_offset = u16(u16(u16(ruler << 1) + ruler) << '
                                        '1)\n'
                                        '    result = append_force_head_glyphs(state, '
                                        'GlyphBatchContext(state.table(566532).cursor(label_offset), '
                                        'destination, background, foreground, count))\n'
                                        '    background, foreground, count = (result.background, '
                                        'result.foreground, result.inclusive_count)\n'
                                        '    destination = result.destination\n'
                                        "upload(_port(state, 'd300').cursor(), 191)\n"
                                        'background, foreground = (replace_word(background, 3), '
                                        'replace_word(foreground, 1))\n'
                                        'stream = expand_glyph_stream(state, '
                                        'state.table(566310).cursor(), _port(state, '
                                        "'d300').cursor(), GlyphColors(background, foreground), "
                                        'replace_word(count, 9))\n'
                                        'count = stream.remaining_carrier\n'
                                        "upload(_port(state, 'd300').cursor(), 79)\n"
                                        'upload(state.table(442740).cursor(), 15)\n'
                                        'state.write(12582916, 4, 1879048193)\n'
                                        'upload(state.table(442222).cursor(), 47)\n'
                                        'background, foreground = (replace_word(background, 1), '
                                        'replace_word(foreground, 3))\n'
                                        'stream = expand_glyph_stream(state, '
                                        'state.table(566310).cursor(), _port(state, '
                                        "'d300').cursor(), GlyphColors(background, foreground), "
                                        'replace_word(count, 9))\n'
                                        'state.write(12582916, 4, 1891631105)\n'
                                        "upload(_port(state, 'd300').cursor(), 79)\n"
                                        'state.write(12582916, 4, 1610612738)\n'
                                        'upload(state.table(703006).cursor(), 23)\n'
                                        'state.write(12582916, 4, 1509949442)\n'
                                        'upload(state.table(442414).cursor(), 31)\n'
                                        'upload(state.table(442600).cursor(), 31)\n'
                                        'cache_battle_roster_totals(state)\n'
                                        'return BattleSceneContext(replace_word(background, '
                                        '65535), foreground, stream.remaining_carrier, '
                                        'context.training_carrier)'},
 'initialize_battle_scene': {'signature': 'state: GameplayState, context: BattleSceneContext',
                             'returns': 'BattleSceneContext',
                             'flow': 'context = checked_context(context, BattleSceneContext, '
                                     'state)\n'
                                     'from .business_services import '
                                     'initialize_video_registers_and_planes, '
                                     'clear_video_sprite_plane, enqueue_sound_command\n'
                                     'state.set_status_word(9984)\n'
                                     "if _port(state, 'f6c4').word() == 0:\n"
                                     "    _port(state, 'f356').set_word(0, _port(state, "
                                     "'f314').word())\n"
                                     "    _port(state, 'f354').set_word(0, _port(state, "
                                     "'f318').word())\n"
                                     'initialize_video_registers_and_planes(state)\n'
                                     'clear_video_sprite_plane(state)\n'
                                     "if _port(state, 'f6c4').word() == 0:\n"
                                     "    _port(state, 'f6c8').set_word(0, 0)\n"
                                     "    work = [_port(state, name).cursor() for name in ('ae28', "
                                     "'3bc2', '3dc2', '3cc2')]\n"
                                     '    for _ in descending_inclusive(63):\n'
                                     '        for destination in work:\n'
                                     '            destination.append_long(0)\n'
                                     'state.write(12582916, 2, 33798)\n'
                                     'background = upload_battle_background_planes(state, '
                                     'context.background)\n'
                                     'glyph_count = upload_battlefield_tilemap(state, '
                                     'context.glyph_count)\n'
                                     'context = upload_battle_scene_labels(state, '
                                     'BattleSceneContext(background, context.foreground, '
                                     'glyph_count, context.training_carrier))\n'
                                     "_port(state, 'f312').set_word(0, 0)\n"
                                     "_port(state, 'f314').set_word(0, 256)\n"
                                     "_port(state, 'f316').set_word(0, 0)\n"
                                     "_port(state, 'f318').set_word(0, 0)\n"
                                     "if not _port(state, 'f3a5').byte() & 1:\n"
                                     "    _port(state, 'f764').set_byte(0, 141)\n"
                                     '    enqueue_sound_command(state, 141)\n'
                                     "_port(state, 'f6c4').set_word(0, 1)\n"
                                     "city = _port(state, 'f68a').word()\n"
                                     "_port(state, 'ea37').set_byte(city, 3)\n"
                                     "_port(state, 'f3a4').set_word(0, _port(state, 'f3a4').word() "
                                     '& 1)\n'
                                     'compact_active_packed_group_queue(state, '
                                     'replace_word(context.background, city))\n'
                                     'return context'},
 'run_battle_scene_round': {'signature': 'state: GameplayState, context: BattleSceneContext',
                            'returns': 'BattleFlowResult',
                            'flow': 'context = checked_context(context, BattleSceneContext, '
                                    'state)\n'
                                    'from .business_reuse import initialize_prebattle_head_bytes, '
                                    'settle_duel_training_and_troops, settle_duel_packets, '
                                    'settle_battle_packed_armies\n'
                                    'from .contexts_reuse import DuelSettlementContext\n'
                                    'from .business_services import '
                                    'initialize_video_registers_and_planes\n'
                                    "_port(state, 'efe0').set_word(0, _port(state, "
                                    "'f6c4').word())\n"
                                    'initialize_prebattle_head_bytes(state)\n'
                                    'training = context.training_carrier\n'
                                    'while True:\n'
                                    "    _port(state, 'f6c4').set_word(0, 2)\n"
                                    "    _port(state, 'f31e').set_word(0, 0)\n"
                                    '    result = state.service_at(251476, '
                                    'SceneServiceContext(training))\n'
                                    '    if type(result) is not BattleFlowResult:\n'
                                    "        raise Boundary('3D654 requires the real "
                                    "training-carrier outcome')\n"
                                    '    training = uint(result.training_carrier, 32)\n'
                                    '    initialize_video_registers_and_planes(state)\n'
                                    "    if _port(state, '8114').word() != 1:\n"
                                    '        result = settle_duel_training_and_troops(state, '
                                    'DuelSettlementContext(training))\n'
                                    '        training = result.progress_carrier\n'
                                    "        if _port(state, 'efe0').word() != 0:\n"
                                    "            _port(state, 'f612').set_word(0, 1024)\n"
                                    "            _port(state, 'f362').set_word(0, 0)\n"
                                    "            _port(state, 'f352').set_word(0, 0)\n"
                                    "            _port(state, 'f6c4').set_word(0, 1)\n"
                                    '            return BattleFlowResult(training)\n'
                                    '    else:\n'
                                    "        _port(state, 'f6c4').set_word(0, 3)\n"
                                    "        _port(state, '70f4').set_word(0, 1)\n"
                                    '        result = state.service_at(159156, '
                                    'SceneServiceContext(training))\n'
                                    '        if type(result) is not BattleFlowResult:\n'
                                    "            raise Boundary('26DB4 requires the real "
                                    "training-carrier outcome')\n"
                                    '        training = uint(result.training_carrier, 32)\n'
                                    '        state.set_status_word(9984)\n'
                                    '        initialize_video_registers_and_planes(state)\n'
                                    '        if settle_duel_packets(state, '
                                    'DuelSettlementContext(training)).carry:\n'
                                    '            continue\n'
                                    '        classify_duel_object_result(state)\n'
                                    "        if _port(state, 'efe0').word() != 0:\n"
                                    "            _port(state, 'f612').set_word(0, 1024)\n"
                                    "            _port(state, 'f362').set_word(0, 0)\n"
                                    "            _port(state, 'f352').set_word(0, 0)\n"
                                    '            return BattleFlowResult(training)\n'
                                    '    settle_battle_packed_armies(state)\n'
                                    "    _port(state, 'f6c4').set_word(0, 0)\n"
                                    "    _port(state, 'f612').set_word(0, 512)\n"
                                    "    _port(state, 'f352').set_word(0, 0)\n"
                                    "    _port(state, 'f764').set_word(0, 0)\n"
                                    '    rebuild_city_links_from_primary_roster(state)\n'
                                    '    return BattleFlowResult(training)'},
 'trigger_battle_for_city_rectangle': {'signature': 'state: GameplayState, context: BattleActionContext', 'returns': None, 'flow': 'context = checked_context(context, BattleActionContext, state)\nframe = BattleTriggerFrame(target_x=None, target_y=None, unit=None, count=None, distance=None, offset_x=None, offset_y=None, choice=None, roster=None, candidates=None, controller=None, scan=None, opponent=None, scratch=None, auxiliary=None, stack_cursor=None, status=state.sr, legacy_context=context)\nframe = trigger_battle_for_city_rectangle_fields(BattleTriggerMemory(state), frame, context.acting_officer)\nreturn state.carry_observed(int(bool(frame.status & 1)))'}}

def _lower_run_battle_scene_round(e,rules):
    e.label('gameplay_pc_000dc0')
    e.ins('move.w','0xf6c4:w,0xefe0:w',6)
    e.label('gameplay_pc_000dc6')
    e.ins('jsr','gameplay_pc_01d57a:l',6)
    e.label('gameplay_pc_000dcc')
    e.ins('move.w','#0x2,0xf6c4:w',6)
    e.label('gameplay_pc_000dd2')
    e.ins('clr.w','0xf31e:w',4)
    e.label('gameplay_pc_000dd6')
    e.ins('jsr','gameplay_pc_03d654:l',6)
    e.label('gameplay_pc_000ddc')
    e.ins('jsr','gameplay_pc_006826:l',6)
    e.label('gameplay_pc_000de2')
    e.ins('cmpi.w','#0x1,0xffff8114:l',8)
    e.label('gameplay_pc_000dea')
    e.ins('beq.w','gameplay_pc_000e14',4)
    e.label('gameplay_pc_000dee')
    e.ins('jsr','gameplay_pc_0188a6:l',6)
    e.label('gameplay_pc_000df4')
    e.ins('tst.w','0xefe0:w',4)
    e.label('gameplay_pc_000df8')
    e.ins('beq.w','gameplay_pc_000e5a',4)
    e.label('gameplay_pc_000dfc')
    e.ins('move.w','#0x400,0xf612:w',6)
    e.label('gameplay_pc_000e02')
    e.ins('clr.w','0xf362:w',4)
    e.label('gameplay_pc_000e06')
    e.ins('clr.w','0xf352:w',4)
    e.label('gameplay_pc_000e0a')
    e.ins('move.w','#0x1,0xf6c4:w',6)
    e.label('gameplay_pc_000e10')
    e.ins('bra.w','gameplay_pc_000e74',4)
    e.label('gameplay_pc_000e14')
    e.ins('move.w','#0x3,0xf6c4:w',6)
    e.label('gameplay_pc_000e1a')
    e.ins('move.w','#0x1,0xff70f4:l',8)
    e.label('gameplay_pc_000e22')
    e.ins('jsr','gameplay_pc_026db4:l',6)
    e.label('gameplay_pc_000e28')
    e.ins('move.w','#0x2700,%sr',4)
    e.label('gameplay_pc_000e2c')
    e.ins('jsr','gameplay_pc_006826:l',6)
    e.label('gameplay_pc_000e32')
    e.ins('jsr','gameplay_pc_018b00:l',6)
    e.label('gameplay_pc_000e38')
    e.ins('bcs.b','gameplay_pc_000dcc',2)
    e.label('gameplay_pc_000e3a')
    e.ins('jsr','gameplay_pc_01d598:l',6)
    e.label('gameplay_pc_000e40')
    e.ins('tst.w','0xefe0:w',4)
    e.label('gameplay_pc_000e44')
    e.ins('beq.w','gameplay_pc_000e5a',4)
    e.label('gameplay_pc_000e48')
    e.ins('move.w','#0x400,0xf612:w',6)
    e.label('gameplay_pc_000e4e')
    e.ins('clr.w','0xf362:w',4)
    e.label('gameplay_pc_000e52')
    e.ins('clr.w','0xf352:w',4)
    e.label('gameplay_pc_000e56')
    e.ins('bra.w','gameplay_pc_000e74',4)
    e.label('gameplay_pc_000e5a')
    e.ins('jsr','gameplay_pc_01d03c:l',6)
    e.label('gameplay_pc_000e60')
    e.ins('move.w','#0x0,0xf6c4:w',6)
    e.label('gameplay_pc_000e66')
    e.ins('move.w','#0x200,0xf612:w',6)
    e.label('gameplay_pc_000e6c')
    e.ins('clr.w','0xf352:w',4)
    e.label('gameplay_pc_000e70')
    e.ins('clr.w','0xf764:w',4)
    e.label('gameplay_pc_000e74')
    e.ins('jsr','gameplay_pc_01d542:l',6)
    e.label('gameplay_pc_000e7a')
    e.ins('rts','',2)

def _lower_initialize_battle_scene(e,rules):
    e.label('gameplay_pc_017602')
    e.ins('move.w','#0x2700,%sr',4)
    e.label('gameplay_pc_017606')
    e.ins('tst.w','0xf6c4:w',4)
    e.label('gameplay_pc_01760a')
    e.ins('bne.w','gameplay_pc_01761a',4)
    e.label('gameplay_pc_01760e')
    e.ins('move.w','0xf314:w,0xf356:w',6)
    e.label('gameplay_pc_017614')
    e.ins('move.w','0xf318:w,0xf354:w',6)
    e.label('gameplay_pc_01761a')
    e.ins('jsr','gameplay_pc_006826:l',6)
    e.label('gameplay_pc_017620')
    e.ins('jsr','gameplay_pc_0068ce:l',6)
    e.label('gameplay_pc_017626')
    e.ins('tst.w','0xf6c4:w',4)
    e.label('gameplay_pc_01762a')
    e.ins('bne.w','gameplay_pc_017658',4)
    e.label('gameplay_pc_01762e')
    e.ins('clr.w','0xf6c8:w',4)
    e.label('gameplay_pc_017632')
    e.ins('lea.l','0xae28:w,%a0',4)
    e.label('gameplay_pc_017636')
    e.ins('lea.l','0xff3bc2:l,%a1',6)
    e.label('gameplay_pc_01763c')
    e.ins('lea.l','0xff3dc2:l,%a2',6)
    e.label('gameplay_pc_017642')
    e.ins('lea.l','0xff3cc2:l,%a3',6)
    e.label('gameplay_pc_017648')
    e.ins('move.w','#0x3f,%d0',4)
    e.label('gameplay_pc_01764c')
    e.ins('clr.l','(%a0)+',2)
    e.label('gameplay_pc_01764e')
    e.ins('clr.l','(%a1)+',2)
    e.label('gameplay_pc_017650')
    e.ins('clr.l','(%a2)+',2)
    e.label('gameplay_pc_017652')
    e.ins('clr.l','(%a3)+',2)
    e.label('gameplay_pc_017654')
    e.ins('dbra','%d0,gameplay_pc_01764c',4)
    e.label('gameplay_pc_017658')
    e.ins('move.w','#0x8406,0xc00004:l',8)
    e.label('gameplay_pc_017660')
    e.ins('bsr.w','gameplay_pc_017710',4)
    e.label('gameplay_pc_017664')
    e.ins('bsr.w','gameplay_pc_017776',4)
    e.label('gameplay_pc_017668')
    e.ins('bsr.w','gameplay_pc_0177be',4)
    e.label('gameplay_pc_01766c')
    e.ins('clr.w','0xf312:w',4)
    e.label('gameplay_pc_017670')
    e.ins('move.w','#0x100,0xf314:w',6)
    e.label('gameplay_pc_017676')
    e.ins('clr.w','0xf316:w',4)
    e.label('gameplay_pc_01767a')
    e.ins('clr.w','0xf318:w',4)
    e.label('gameplay_pc_01767e')
    e.ins('btst.b','#0x0,0xf3a5:w',6)
    e.label('gameplay_pc_017684')
    e.ins('bne.w','gameplay_pc_017696',4)
    e.label('gameplay_pc_017688')
    e.ins('move.b','#0x8d,%d0',4)
    e.label('gameplay_pc_01768c')
    e.ins('move.b','%d0,0xf764:w',4)
    e.label('gameplay_pc_017690')
    e.ins('jsr','gameplay_pc_00808a:l',6)
    e.label('gameplay_pc_017696')
    e.ins('move.w','#0x1,0xf6c4:w',6)
    e.label('gameplay_pc_01769c')
    e.ins('lea.l','0xea37:w,%a0',4)
    e.label('gameplay_pc_0176a0')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_0176a4')
    e.ins('move.b','#0x3,(%a0, %d0.w)',6)
    e.label('gameplay_pc_0176aa')
    e.ins('andi.w','#0x1,0xf3a4:w',6)
    e.label('gameplay_pc_0176b0')
    e.ins('bsr.w','gameplay_pc_0176b6',4)
    e.label('gameplay_pc_0176b4')
    e.ins('rts','',2)

def _lower_compact_active_packed_group_queue(e,rules):
    e.label('gameplay_pc_0176b6')
    e.ins('lea.l','0xff39b2:l,%a0',6)
    e.label('gameplay_pc_0176bc')
    e.ins('adda.w','0xff3bb2:l,%a0',6)
    e.label('gameplay_pc_0176c2')
    e.ins('tst.b','(%a0)+',2)
    e.label('gameplay_pc_0176c4')
    e.ins('beq.w','gameplay_pc_0176d0',4)
    e.label('gameplay_pc_0176c8')
    e.ins('move.b','(%a0)+,%d0',2)
    e.label('gameplay_pc_0176ca')
    e.ins('bsr.w','gameplay_pc_0176d2',4)
    e.label('gameplay_pc_0176ce')
    e.ins('bra.b','gameplay_pc_0176c2',2)
    e.label('gameplay_pc_0176d0')
    e.ins('rts','',2)

def _lower_remove_queued_packed_group_member(e,rules):
    e.label('gameplay_pc_0176d2')
    e.ins('lea.l','0xff3000:l,%a1',6)
    e.label('gameplay_pc_0176d8')
    e.ins('tst.b','(%a1)+',2)
    e.label('gameplay_pc_0176da')
    e.ins('bmi.w','gameplay_pc_01770e',4)
    e.label('gameplay_pc_0176de')
    e.ins('cmp.b','(%a1)+,%d0',2)
    e.label('gameplay_pc_0176e0')
    e.ins('beq.w','gameplay_pc_0176ea',4)
    e.label('gameplay_pc_0176e4')
    e.ins('tst.b','(%a1)+',2)
    e.label('gameplay_pc_0176e6')
    e.ins('bne.b','gameplay_pc_0176e4',2)
    e.label('gameplay_pc_0176e8')
    e.ins('bra.b','gameplay_pc_0176d8',2)
    e.label('gameplay_pc_0176ea')
    e.ins('cmpi.b','#0x80,0x1(%a1)',6)
    e.label('gameplay_pc_0176f0')
    e.ins('bne.w','gameplay_pc_01770e',4)
    e.label('gameplay_pc_0176f4')
    e.ins('move.b','0x2(%a1),%d1',4)
    e.label('gameplay_pc_0176f8')
    e.ins('cmp.b','0xf68b:w,%d1',4)
    e.label('gameplay_pc_0176fc')
    e.ins('bne.w','gameplay_pc_01770e',4)
    e.label('gameplay_pc_017700')
    e.ins('move.b','(%a0)+,-0x3(%a0)',4)
    e.label('gameplay_pc_017704')
    e.ins('beq.w','gameplay_pc_01770e',4)
    e.label('gameplay_pc_017708')
    e.ins('move.b','(%a0)+,-0x3(%a0)',4)
    e.label('gameplay_pc_01770c')
    e.ins('bra.b','gameplay_pc_017700',2)
    e.label('gameplay_pc_01770e')
    e.ins('rts','',2)

def _lower_upload_battle_background_planes(e,rules):
    e.label('gameplay_pc_017710')
    e.ins('move.l','#0x60000003,0xc00004:l',10)
    e.label('gameplay_pc_01771a')
    e.ins('lea.l','0x68c14:l,%a2',6)
    e.label('gameplay_pc_017720')
    e.ins('movea.l','(%a2),%a0',2)
    e.label('gameplay_pc_017722')
    e.ins('lea.l','0x68c1c:l,%a2',6)
    e.label('gameplay_pc_017728')
    e.ins('movea.l','(%a2),%a1',2)
    e.label('gameplay_pc_01772a')
    e.ins('lsr.w','#0x1,%d0',2)
    e.label('gameplay_pc_01772c')
    e.ins('lea.l','0x6bf06:l,%a2',6)
    e.label('gameplay_pc_017732')
    e.ins('move.w','(%a2),%d0',2)
    e.label('gameplay_pc_017734')
    e.ins('jsr','gameplay_pc_00adfc:l',6)
    e.label('gameplay_pc_01773a')
    e.ins('move.l','#0x40000001,0xc00004:l',10)
    e.label('gameplay_pc_017744')
    e.ins('lea.l','0x68c14:l,%a2',6)
    e.label('gameplay_pc_01774a')
    e.ins('movea.l','0x4(%a2),%a0',4)
    e.label('gameplay_pc_01774e')
    e.ins('lea.l','0x68c1c:l,%a2',6)
    e.label('gameplay_pc_017754')
    e.ins('movea.l','0x4(%a2),%a1',4)
    e.label('gameplay_pc_017758')
    e.ins('lsr.w','#0x1,%d0',2)
    e.label('gameplay_pc_01775a')
    e.ins('lea.l','0x6bf06:l,%a2',6)
    e.label('gameplay_pc_017760')
    e.ins('move.w','0x2(%a2),%d0',4)
    e.label('gameplay_pc_017764')
    e.ins('jsr','gameplay_pc_00adfc:l',6)
    e.label('gameplay_pc_01776a')
    e.ins('move.w','#0x6,%d0',4)
    e.label('gameplay_pc_01776e')
    e.ins('jsr','gameplay_pc_008112:l',6)
    e.label('gameplay_pc_017774')
    e.ins('rts','',2)

def _lower_upload_battlefield_tilemap(e,rules):
    e.label('gameplay_pc_017776')
    e.ins('move.l','#0x50000003,%d2',6)
    e.label('gameplay_pc_01777c')
    e.ins('lea.l','0x945e8:l,%a0',6)
    e.label('gameplay_pc_017782')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_017786')
    e.ins('mulu.w','#0x8c0,%d0',4)
    e.label('gameplay_pc_01778a')
    e.ins('adda.l','%d0,%a0',2)
    e.label('gameplay_pc_01778c')
    e.ins('move.w','#0x1b,%d1',4)
    e.label('gameplay_pc_017790')
    e.ins('move.l','%d2,0xc00004:l',6)
    e.label('gameplay_pc_017796')
    e.ins('move.w','#0x27,%d0',4)
    e.label('gameplay_pc_01779a')
    e.ins('move.w','(%a0)+,%d3',2)
    e.label('gameplay_pc_01779c')
    e.ins('btst.l','#0x8,%d3',4)
    e.label('gameplay_pc_0177a0')
    e.ins('beq.w','gameplay_pc_0177a8',4)
    e.label('gameplay_pc_0177a4')
    e.ins('ori.w','#0x700,%d3',4)
    e.label('gameplay_pc_0177a8')
    e.ins('move.w','%d3,0xc00000:l',6)
    e.label('gameplay_pc_0177ae')
    e.ins('dbra','%d0,gameplay_pc_01779a',4)
    e.label('gameplay_pc_0177b2')
    e.ins('addi.l','#0x800000,%d2',6)
    e.label('gameplay_pc_0177b8')
    e.ins('dbra','%d1,gameplay_pc_017790',4)
    e.label('gameplay_pc_0177bc')
    e.ins('rts','',2)

def _lower_upload_battle_scene_labels(e,rules):
    e.label('gameplay_pc_0177be')
    e.ins('move.l','#0x40200002,0xc00004:l',10)
    e.label('gameplay_pc_0177c8')
    e.ins('move.w','#0x1f,%d0',4)
    e.label('gameplay_pc_0177cc')
    e.ins('move.l','#0x11111111,0xc00000:l',10)
    e.label('gameplay_pc_0177d6')
    e.ins('dbra','%d0,gameplay_pc_0177cc',4)
    e.label('gameplay_pc_0177da')
    e.ins('lea.l','0x6bf58:l,%a0',6)
    e.label('gameplay_pc_0177e0')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('gameplay_pc_0177e4')
    e.ins('move.w','#0x1,%d0',4)
    e.label('gameplay_pc_0177e8')
    e.ins('move.w','#0x3,%d1',4)
    e.label('gameplay_pc_0177ec')
    e.ins('move.w','#0xa,%d3',4)
    e.label('gameplay_pc_0177f0')
    e.ins('jsr','gameplay_pc_00ae8a:l',6)
    e.label('gameplay_pc_0177f6')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('gameplay_pc_0177fa')
    e.ins('move.w','#0x15f,%d3',4)
    e.label('gameplay_pc_0177fe')
    e.ins('move.l','(%a1)+,0xc00000:l',6)
    e.label('gameplay_pc_017804')
    e.ins('dbra','%d3,gameplay_pc_0177fe',4)
    e.label('gameplay_pc_017808')
    e.ins('move.l','#0x48000002,0xc00004:l',10)
    e.label('gameplay_pc_017812')
    e.ins('move.w','0xf68a:w,%d3',4)
    e.label('gameplay_pc_017816')
    e.ins('lsl.w','#0x2,%d3',2)
    e.label('gameplay_pc_017818')
    e.ins('lea.l','0x8a212:l,%a0',6)
    e.label('gameplay_pc_01781e')
    e.ins('adda.w','%d3,%a0',2)
    e.label('gameplay_pc_017820')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('gameplay_pc_017824')
    e.ins('move.w','#0x1,%d3',4)
    e.label('gameplay_pc_017828')
    e.ins('jsr','gameplay_pc_00ae8a:l',6)
    e.label('gameplay_pc_01782e')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('gameplay_pc_017832')
    e.ins('move.w','#0x3f,%d3',4)
    e.label('gameplay_pc_017836')
    e.ins('move.l','(%a1)+,0xc00000:l',6)
    e.label('gameplay_pc_01783c')
    e.ins('dbra','%d3,gameplay_pc_017836',4)
    e.label('gameplay_pc_017840')
    e.ins('move.w','0xf68e:w,%d4',4)
    e.label('gameplay_pc_017844')
    e.ins('lsl.w','#0x1,%d4',2)
    e.label('gameplay_pc_017846')
    e.ins('lea.l','0xe640:w,%a2',4)
    e.label('gameplay_pc_01784a')
    e.ins('move.w','(%a2, %d4.w),%d4',4)
    e.label('gameplay_pc_01784e')
    e.ins('move.w','%d4,%d5',2)
    e.label('gameplay_pc_017850')
    e.ins('lsl.w','#0x1,%d4',2)
    e.label('gameplay_pc_017852')
    e.ins('add.w','%d5,%d4',2)
    e.label('gameplay_pc_017854')
    e.ins('lsl.w','#0x1,%d4',2)
    e.label('gameplay_pc_017856')
    e.ins('lea.l','0x8a504:l,%a0',6)
    e.label('gameplay_pc_01785c')
    e.ins('adda.w','%d4,%a0',2)
    e.label('gameplay_pc_01785e')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('gameplay_pc_017862')
    e.ins('bsr.w','gameplay_pc_0179d6',4)
    e.label('gameplay_pc_017866')
    e.ins('move.w','0xf68c:w,%d4',4)
    e.label('gameplay_pc_01786a')
    e.ins('lsl.w','#0x1,%d4',2)
    e.label('gameplay_pc_01786c')
    e.ins('lea.l','0xe640:w,%a2',4)
    e.label('gameplay_pc_017870')
    e.ins('move.w','(%a2, %d4.w),%d4',4)
    e.label('gameplay_pc_017874')
    e.ins('move.w','%d4,%d5',2)
    e.label('gameplay_pc_017876')
    e.ins('lsl.w','#0x1,%d4',2)
    e.label('gameplay_pc_017878')
    e.ins('add.w','%d5,%d4',2)
    e.label('gameplay_pc_01787a')
    e.ins('lsl.w','#0x1,%d4',2)
    e.label('gameplay_pc_01787c')
    e.ins('lea.l','0x8a504:l,%a0',6)
    e.label('gameplay_pc_017882')
    e.ins('adda.w','%d4,%a0',2)
    e.label('gameplay_pc_017884')
    e.ins('bsr.w','gameplay_pc_0179d6',4)
    e.label('gameplay_pc_017888')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('gameplay_pc_01788c')
    e.ins('move.w','#0xbf,%d3',4)
    e.label('gameplay_pc_017890')
    e.ins('move.l','(%a1)+,0xc00000:l',6)
    e.label('gameplay_pc_017896')
    e.ins('dbra','%d3,gameplay_pc_017890',4)
    e.label('gameplay_pc_01789a')
    e.ins('lea.l','0x8a426:l,%a0',6)
    e.label('gameplay_pc_0178a0')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('gameplay_pc_0178a4')
    e.ins('move.w','#0x3,%d0',4)
    e.label('gameplay_pc_0178a8')
    e.ins('move.w','#0x1,%d1',4)
    e.label('gameplay_pc_0178ac')
    e.ins('move.w','#0x9,%d3',4)
    e.label('gameplay_pc_0178b0')
    e.ins('jsr','gameplay_pc_00af1e:l',6)
    e.label('gameplay_pc_0178b6')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('gameplay_pc_0178ba')
    e.ins('move.w','#0x4f,%d3',4)
    e.label('gameplay_pc_0178be')
    e.ins('move.l','(%a1)+,0xc00000:l',6)
    e.label('gameplay_pc_0178c4')
    e.ins('dbra','%d3,gameplay_pc_0178be',4)
    e.label('gameplay_pc_0178c8')
    e.ins('lea.l','0x6c174:l,%a1',6)
    e.label('gameplay_pc_0178ce')
    e.ins('move.w','#0xf,%d3',4)
    e.label('gameplay_pc_0178d2')
    e.ins('move.l','(%a1)+,0xc00000:l',6)
    e.label('gameplay_pc_0178d8')
    e.ins('dbra','%d3,gameplay_pc_0178d2',4)
    e.label('gameplay_pc_0178dc')
    e.ins('move.l','#0x70000001,0xc00004:l',10)
    e.label('gameplay_pc_0178e6')
    e.ins('lea.l','0x6bf6e:l,%a1',6)
    e.label('gameplay_pc_0178ec')
    e.ins('move.w','#0x2f,%d3',4)
    e.label('gameplay_pc_0178f0')
    e.ins('move.l','(%a1)+,0xc00000:l',6)
    e.label('gameplay_pc_0178f6')
    e.ins('dbra','%d3,gameplay_pc_0178f0',4)
    e.label('gameplay_pc_0178fa')
    e.ins('lea.l','0x8a426:l,%a0',6)
    e.label('gameplay_pc_017900')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('gameplay_pc_017904')
    e.ins('move.w','#0x1,%d0',4)
    e.label('gameplay_pc_017908')
    e.ins('move.w','#0x3,%d1',4)
    e.label('gameplay_pc_01790c')
    e.ins('move.w','#0x9,%d3',4)
    e.label('gameplay_pc_017910')
    e.ins('jsr','gameplay_pc_00af1e:l',6)
    e.label('gameplay_pc_017916')
    e.ins('move.l','#0x70c00001,0xc00004:l',10)
    e.label('gameplay_pc_017920')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('gameplay_pc_017924')
    e.ins('move.w','#0x4f,%d2',4)
    e.label('gameplay_pc_017928')
    e.ins('move.l','(%a1)+,0xc00000:l',6)
    e.label('gameplay_pc_01792e')
    e.ins('dbra','%d2,gameplay_pc_017928',4)
    e.label('gameplay_pc_017932')
    e.ins('move.l','#0x60000002,0xc00004:l',10)
    e.label('gameplay_pc_01793c')
    e.ins('lea.l','0xaba1e:l,%a1',6)
    e.label('gameplay_pc_017942')
    e.ins('move.w','#0x17,%d0',4)
    e.label('gameplay_pc_017946')
    e.ins('move.l','(%a1)+,0xc00000:l',6)
    e.label('gameplay_pc_01794c')
    e.ins('dbra','%d0,gameplay_pc_017946',4)
    e.label('gameplay_pc_017950')
    e.ins('move.l','#0x5a000002,0xc00004:l',10)
    e.label('gameplay_pc_01795a')
    e.ins('lea.l','0x6c02e:l,%a1',6)
    e.label('gameplay_pc_017960')
    e.ins('move.w','#0x1f,%d1',4)
    e.label('gameplay_pc_017964')
    e.ins('move.l','(%a1)+,0xc00000:l',6)
    e.label('gameplay_pc_01796a')
    e.ins('dbra','%d1,gameplay_pc_017964',4)
    e.label('gameplay_pc_01796e')
    e.ins('lea.l','0x6c0e8:l,%a1',6)
    e.label('gameplay_pc_017974')
    e.ins('move.w','#0x1f,%d1',4)
    e.label('gameplay_pc_017978')
    e.ins('move.l','(%a1)+,0xc00000:l',6)
    e.label('gameplay_pc_01797e')
    e.ins('dbra','%d1,gameplay_pc_017978',4)
    e.label('gameplay_pc_017982')
    e.ins('bsr.w','gameplay_pc_017988',4)
    e.label('gameplay_pc_017986')
    e.ins('rts','',2)

def _lower_cache_battle_roster_totals(e,rules):
    e.label('gameplay_pc_017988')
    e.ins('lea.l','0xc800:w,%a0',4)
    e.label('gameplay_pc_01798c')
    e.ins('lea.l','0xa550:w,%a1',4)
    e.label('gameplay_pc_017990')
    e.ins('bsr.w','gameplay_pc_0179be',4)
    e.label('gameplay_pc_017994')
    e.ins('move.l','%d0,0xf6ae:w',4)
    e.label('gameplay_pc_017998')
    e.ins('move.w','%d1,0xf6a6:w',4)
    e.label('gameplay_pc_01799c')
    e.ins('lea.l','0xa5a4:w,%a1',4)
    e.label('gameplay_pc_0179a0')
    e.ins('bsr.w','gameplay_pc_0179be',4)
    e.label('gameplay_pc_0179a4')
    e.ins('move.l','%d0,0xf6b2:w',4)
    e.label('gameplay_pc_0179a8')
    e.ins('move.w','%d1,0xf6a8:w',4)
    e.label('gameplay_pc_0179ac')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_0179b0')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_0179b2')
    e.ins('lea.l','0xe59c:w,%a0',4)
    e.label('gameplay_pc_0179b6')
    e.ins('move.w','0x2(%a0, %d0.w),0xf6be:w',6)
    e.label('gameplay_pc_0179bc')
    e.ins('rts','',2)

def _lower_append_force_head_glyphs(e,rules):
    e.label('gameplay_pc_0179d6')
    e.ins('cmpi.w','#0x3f,0x4(%a0)',6)
    e.label('gameplay_pc_0179dc')
    e.ins('beq.w','gameplay_pc_0179ee',4)
    e.label('gameplay_pc_0179e0')
    e.ins('move.w','#0x2,%d3',4)
    e.label('gameplay_pc_0179e4')
    e.ins('jsr','gameplay_pc_00ae8a:l',6)
    e.label('gameplay_pc_0179ea')
    e.ins('bra.w','gameplay_pc_017a14',4)
    e.label('gameplay_pc_0179ee')
    e.ins('move.w','#0xf,%d3',4)
    e.label('gameplay_pc_0179f2')
    e.ins('move.l','#0x11111111,(%a1)+',6)
    e.label('gameplay_pc_0179f8')
    e.ins('dbra','%d3,gameplay_pc_0179f2',4)
    e.label('gameplay_pc_0179fc')
    e.ins('move.w','#0x1,%d3',4)
    e.label('gameplay_pc_017a00')
    e.ins('jsr','gameplay_pc_00ae8a:l',6)
    e.label('gameplay_pc_017a06')
    e.ins('move.w','#0xf,%d3',4)
    e.label('gameplay_pc_017a0a')
    e.ins('move.l','#0x11111111,(%a1)+',6)
    e.label('gameplay_pc_017a10')
    e.ins('dbra','%d3,gameplay_pc_017a0a',4)
    e.label('gameplay_pc_017a14')
    e.ins('rts','',2)

def _lower_integrate_selected_officer_into_packed_group(e,rules):
    e.label('gameplay_pc_017f30')
    e.ins('move.w','0xf6d6:w,%d0',4)
    e.label('gameplay_pc_017f34')
    e.ins('andi.w','#0x2,%d0',4)
    e.label('gameplay_pc_017f38')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_017f3a')
    e.ins('movea.l','-36(%pc, %d0.w),%a0',4)
    e.label('gameplay_pc_017f3e')
    e.ins('movea.l','%a0,%a3',2)
    e.label('gameplay_pc_017f40')
    e.ins('movea.l','-34(%pc, %d0.w),%a1',4)
    e.label('gameplay_pc_017f44')
    e.ins('movea.l','-30(%pc, %d0.w),%a2',4)
    e.label('gameplay_pc_017f48')
    e.ins('subq.w','#0x1,(%a1)',2)
    e.label('gameplay_pc_017f4a')
    e.ins('move.w','0xf3a6:w,%d0',4)
    e.label('gameplay_pc_017f4e')
    e.ins('bsr.w','gameplay_pc_0181a6',4)
    e.label('gameplay_pc_017f52')
    e.ins('bcs.w','gameplay_pc_017fcc',4)
    e.label('gameplay_pc_017f56')
    e.ins('move.w','(%a0)+,%d1',2)
    e.label('gameplay_pc_017f58')
    e.ins('cmp.w','%d0,%d1',2)
    e.label('gameplay_pc_017f5a')
    e.ins('bne.b','gameplay_pc_017f56',2)
    e.label('gameplay_pc_017f5c')
    e.ins('move.w','(%a0)+,-0x4(%a0)',4)
    e.label('gameplay_pc_017f60')
    e.ins('bpl.b','gameplay_pc_017f5c',2)
    e.label('gameplay_pc_017f62')
    e.ins('move.w','(%a2),%d0',2)
    e.label('gameplay_pc_017f64')
    e.ins('bsr.w','gameplay_pc_017d10',4)
    e.label('gameplay_pc_017f68')
    e.ins('move.b','%d0,0x1(%a0)',4)
    e.label('gameplay_pc_017f6c')
    e.ins('move.b','%d1,0x2(%a0)',4)
    e.label('gameplay_pc_017f70')
    e.ins('move.b','(%a0),%d1',2)
    e.label('gameplay_pc_017f72')
    e.ins('andi.w','#0xf,%d1',4)
    e.label('gameplay_pc_017f76')
    e.ins('bne.b','gameplay_pc_017f9c',2)
    e.label('gameplay_pc_017f78')
    e.ins('clr.b','0x5(%a0)',4)
    e.label('gameplay_pc_017f7c')
    e.ins('clr.b','0x6(%a0)',4)
    e.label('gameplay_pc_017f80')
    e.ins('clr.b','0x7(%a0)',4)
    e.label('gameplay_pc_017f84')
    e.ins('clr.b','0x8(%a0)',4)
    e.label('gameplay_pc_017f88')
    e.ins('clr.b','0x9(%a0)',4)
    e.label('gameplay_pc_017f8c')
    e.ins('clr.b','0xa(%a0)',4)
    e.label('gameplay_pc_017f90')
    e.ins('clr.b','0xb(%a0)',4)
    e.label('gameplay_pc_017f94')
    e.ins('clr.b','0xc(%a0)',4)
    e.label('gameplay_pc_017f98')
    e.ins('clr.b','0xd(%a0)',4)
    e.label('gameplay_pc_017f9c')
    e.ins('addi.b','#0x1,(%a0)',4)
    e.label('gameplay_pc_017fa0')
    e.ins('bsr.w','gameplay_pc_01802a',4)
    e.label('gameplay_pc_017fa4')
    e.ins('move.b','0xf3a7:w,(%a2)',4)
    e.label('gameplay_pc_017fa8')
    e.ins('bsr.w','gameplay_pc_01807a',4)
    e.label('gameplay_pc_017fac')
    e.ins('bsr.w','gameplay_pc_018158',4)
    e.label('gameplay_pc_017fb0')
    e.ins('lea.l','0xcc00:w,%a1',4)
    e.label('gameplay_pc_017fb4')
    e.ins('move.w','0xf3a6:w,%d0',4)
    e.label('gameplay_pc_017fb8')
    e.ins('bset.b','#0x6,(%a1, %d0.w)',6)
    e.label('gameplay_pc_017fbe')
    e.ins('lea.l','0xa150:w,%a1',4)
    e.label('gameplay_pc_017fc2')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_017fc4')
    e.ins('clr.l','(%a1, %d0.w)',4)
    e.label('gameplay_pc_017fc8')
    e.ins('bra.w','gameplay_pc_018024',4)
    e.label('gameplay_pc_017fcc')
    e.ins('movea.l','%a0,%a4',2)
    e.label('gameplay_pc_017fce')
    e.ins('bsr.w','gameplay_pc_0182c4',4)
    e.label('gameplay_pc_017fd2')
    e.ins('clr.w','%d6',2)
    e.label('gameplay_pc_017fd4')
    e.ins('tst.w','(%a0)+',2)
    e.label('gameplay_pc_017fd6')
    e.ins('bmi.w','gameplay_pc_017fde',4)
    e.label('gameplay_pc_017fda')
    e.ins('addq.w','#0x1,%d6',2)
    e.label('gameplay_pc_017fdc')
    e.ins('bra.b','gameplay_pc_017fd4',2)
    e.label('gameplay_pc_017fde')
    e.ins('move.w','(%a2),%d0',2)
    e.label('gameplay_pc_017fe0')
    e.ins('bsr.w','gameplay_pc_017d10',4)
    e.label('gameplay_pc_017fe4')
    e.ins('move.b','%d0,0x1(%a0)',4)
    e.label('gameplay_pc_017fe8')
    e.ins('move.b','%d1,0x2(%a0)',4)
    e.label('gameplay_pc_017fec')
    e.ins('move.b','(%a0),%d1',2)
    e.label('gameplay_pc_017fee')
    e.ins('andi.w','#0xf,%d1',4)
    e.label('gameplay_pc_017ff2')
    e.ins('bne.b','gameplay_pc_018018',2)
    e.label('gameplay_pc_017ff4')
    e.ins('clr.b','0x5(%a0)',4)
    e.label('gameplay_pc_017ff8')
    e.ins('clr.b','0x6(%a0)',4)
    e.label('gameplay_pc_017ffc')
    e.ins('clr.b','0x7(%a0)',4)
    e.label('gameplay_pc_018000')
    e.ins('clr.b','0x8(%a0)',4)
    e.label('gameplay_pc_018004')
    e.ins('clr.b','0x9(%a0)',4)
    e.label('gameplay_pc_018008')
    e.ins('clr.b','0xa(%a0)',4)
    e.label('gameplay_pc_01800c')
    e.ins('clr.b','0xb(%a0)',4)
    e.label('gameplay_pc_018010')
    e.ins('clr.b','0xc(%a0)',4)
    e.label('gameplay_pc_018014')
    e.ins('clr.b','0xd(%a0)',4)
    e.label('gameplay_pc_018018')
    e.ins('bsr.w','gameplay_pc_0181e8',4)
    e.label('gameplay_pc_01801c')
    e.ins('bsr.w','gameplay_pc_018224',4)
    e.label('gameplay_pc_018020')
    e.ins('bsr.w','gameplay_pc_018158',4)
    e.label('gameplay_pc_018024')
    e.ins('bsr.w','gameplay_pc_018184',4)
    e.label('gameplay_pc_018028')
    e.ins('rts','',2)

def _lower_reserve_packed_group_member_byte(e,rules):
    e.label('gameplay_pc_01802a')
    e.ins('lea.l','0xd(%a0, %d1.w),%a1',4)
    e.label('gameplay_pc_01802e')
    e.ins('lea.l','(%a1),%a2',2)
    e.label('gameplay_pc_018030')
    e.ins('tst.w','%d1',2)
    e.label('gameplay_pc_018032')
    e.ins('bne.w','gameplay_pc_018038',4)
    e.label('gameplay_pc_018036')
    e.ins('clr.b','(%a1)',2)
    e.label('gameplay_pc_018038')
    e.ins('move.b','(%a1),%d2',2)
    e.label('gameplay_pc_01803a')
    e.ins('andi.w','#0xf,%d2',4)
    e.label('gameplay_pc_01803e')
    e.ins('beq.w','gameplay_pc_018048',4)
    e.label('gameplay_pc_018042')
    e.ins('lea.l','0xd(%a1, %d2.w),%a1',4)
    e.label('gameplay_pc_018046')
    e.ins('bra.b','gameplay_pc_018038',2)
    e.label('gameplay_pc_018048')
    e.ins('lea.l','0x1(%a1),%a4',4)
    e.label('gameplay_pc_01804c')
    e.ins('clr.b','(%a4)',2)
    e.label('gameplay_pc_01804e')
    e.ins('cmpa.l','%a2,%a1',2)
    e.label('gameplay_pc_018050')
    e.ins('bls.w','gameplay_pc_018058',4)
    e.label('gameplay_pc_018054')
    e.ins('move.b','-(%a1),-(%a4)',2)
    e.label('gameplay_pc_018056')
    e.ins('bra.b','gameplay_pc_01804e',2)
    e.label('gameplay_pc_018058')
    e.ins('rts','',2)

def _lower_split_city_resources_into_group(e,rules):
    e.label('gameplay_pc_01807a')
    e.ins('move.w','0xf6d6:w,%d0',4)
    e.label('gameplay_pc_01807e')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_018080')
    e.ins('movea.l','-40(%pc, %d0.w),%a1',4)
    e.label('gameplay_pc_018084')
    e.ins('movea.l','-28(%pc, %d0.w),%a2',4)
    e.label('gameplay_pc_018088')
    e.ins('move.l','(%a1),%d1',2)
    e.label('gameplay_pc_01808a')
    e.ins('lsr.w','#0x8,%d1',2)
    e.label('gameplay_pc_01808c')
    e.ins('lea.l','0xc800:w,%a4',4)
    e.label('gameplay_pc_018090')
    e.ins('move.w','0xf3a6:w,%d3',4)
    e.label('gameplay_pc_018094')
    e.ins('lsl.w','#0x2,%d3',2)
    e.label('gameplay_pc_018096')
    e.ins('move.l','(%a4, %d3.w),%d3',4)
    e.label('gameplay_pc_01809a')
    e.ins('addi.l','#0x64,%d3',6)
    e.label('gameplay_pc_0180a0')
    e.ins('mulu.w','%d3,%d1',2)
    e.label('gameplay_pc_0180a2')
    e.ins('moveq','#0,%d4',2)
    e.label('gameplay_pc_0180a4')
    e.ins('move.w','%d3,%d4',2)
    e.label('gameplay_pc_0180a6')
    e.ins('move.w','(%a3)+,%d2',2)
    e.label('gameplay_pc_0180a8')
    e.ins('bmi.b','gameplay_pc_0180bc',2)
    e.label('gameplay_pc_0180aa')
    e.ins('andi.w','#0xff,%d2',4)
    e.label('gameplay_pc_0180ae')
    e.ins('lsl.w','#0x2,%d2',2)
    e.label('gameplay_pc_0180b0')
    e.ins('add.l','(%a4, %d2.w),%d4',4)
    e.label('gameplay_pc_0180b4')
    e.ins('addi.l','#0x64,%d4',6)
    e.label('gameplay_pc_0180ba')
    e.ins('bra.b','gameplay_pc_0180a6',2)
    e.label('gameplay_pc_0180bc')
    e.ins('move.l','%d4,%d2',2)
    e.label('gameplay_pc_0180be')
    e.ins('jsr','gameplay_pc_035760:l',6)
    e.label('gameplay_pc_0180c4')
    e.ins('lsl.l','#0x8,%d1',2)
    e.label('gameplay_pc_0180c6')
    e.ins('sub.l','%d1,(%a1)',2)
    e.label('gameplay_pc_0180c8')
    e.ins('move.b','0x5(%a0),%d2',4)
    e.label('gameplay_pc_0180cc')
    e.ins('lsl.w','#0x8,%d2',2)
    e.label('gameplay_pc_0180ce')
    e.ins('move.b','0x6(%a0),%d2',4)
    e.label('gameplay_pc_0180d2')
    e.ins('lsl.l','#0x8,%d2',2)
    e.label('gameplay_pc_0180d4')
    e.ins('move.b','0x7(%a0),%d2',4)
    e.label('gameplay_pc_0180d8')
    e.ins('lsl.l','#0x8,%d2',2)
    e.label('gameplay_pc_0180da')
    e.ins('move.b','0x8(%a0),%d2',4)
    e.label('gameplay_pc_0180de')
    e.ins('add.l','%d2,%d1',2)
    e.label('gameplay_pc_0180e0')
    e.ins('cmpi.l','#0xf423f,%d1',6)
    e.label('gameplay_pc_0180e6')
    e.ins('bls.w','gameplay_pc_0180f0',4)
    e.label('gameplay_pc_0180ea')
    e.ins('move.l','#0xf423f,%d1',6)
    e.label('gameplay_pc_0180f0')
    e.ins('move.b','%d1,0x8(%a0)',4)
    e.label('gameplay_pc_0180f4')
    e.ins('lsr.l','#0x8,%d1',2)
    e.label('gameplay_pc_0180f6')
    e.ins('move.b','%d1,0x7(%a0)',4)
    e.label('gameplay_pc_0180fa')
    e.ins('lsr.l','#0x8,%d1',2)
    e.label('gameplay_pc_0180fc')
    e.ins('move.b','%d1,0x6(%a0)',4)
    e.label('gameplay_pc_018100')
    e.ins('lsr.w','#0x8,%d1',2)
    e.label('gameplay_pc_018102')
    e.ins('move.b','%d1,0x5(%a0)',4)
    e.label('gameplay_pc_018106')
    e.ins('move.l','(%a2),%d1',2)
    e.label('gameplay_pc_018108')
    e.ins('lsr.w','#0x8,%d1',2)
    e.label('gameplay_pc_01810a')
    e.ins('mulu.w','%d3,%d1',2)
    e.label('gameplay_pc_01810c')
    e.ins('move.l','%d4,%d2',2)
    e.label('gameplay_pc_01810e')
    e.ins('jsr','gameplay_pc_035760:l',6)
    e.label('gameplay_pc_018114')
    e.ins('lsl.l','#0x8,%d1',2)
    e.label('gameplay_pc_018116')
    e.ins('sub.l','%d1,(%a2)',2)
    e.label('gameplay_pc_018118')
    e.ins('move.b','0x9(%a0),%d2',4)
    e.label('gameplay_pc_01811c')
    e.ins('lsl.w','#0x8,%d2',2)
    e.label('gameplay_pc_01811e')
    e.ins('move.b','0xa(%a0),%d2',4)
    e.label('gameplay_pc_018122')
    e.ins('lsl.l','#0x8,%d2',2)
    e.label('gameplay_pc_018124')
    e.ins('move.b','0xb(%a0),%d2',4)
    e.label('gameplay_pc_018128')
    e.ins('lsl.l','#0x8,%d2',2)
    e.label('gameplay_pc_01812a')
    e.ins('move.b','0xc(%a0),%d2',4)
    e.label('gameplay_pc_01812e')
    e.ins('add.l','%d2,%d1',2)
    e.label('gameplay_pc_018130')
    e.ins('cmpi.l','#0xf423f,%d1',6)
    e.label('gameplay_pc_018136')
    e.ins('bls.w','gameplay_pc_018140',4)
    e.label('gameplay_pc_01813a')
    e.ins('move.l','#0xf423f,%d1',6)
    e.label('gameplay_pc_018140')
    e.ins('move.b','%d1,0xc(%a0)',4)
    e.label('gameplay_pc_018144')
    e.ins('lsr.l','#0x8,%d1',2)
    e.label('gameplay_pc_018146')
    e.ins('move.b','%d1,0xb(%a0)',4)
    e.label('gameplay_pc_01814a')
    e.ins('lsr.l','#0x8,%d1',2)
    e.label('gameplay_pc_01814c')
    e.ins('move.b','%d1,0xa(%a0)',4)
    e.label('gameplay_pc_018150')
    e.ins('lsr.w','#0x8,%d1',2)
    e.label('gameplay_pc_018152')
    e.ins('move.b','%d1,0x9(%a0)',4)
    e.label('gameplay_pc_018156')
    e.ins('rts','',2)

def _lower_refresh_packed_group_average(e,rules):
    e.label('gameplay_pc_018158')
    e.ins('move.b','(%a0),%d0',2)
    e.label('gameplay_pc_01815a')
    e.ins('andi.w','#0xf,%d0',4)
    e.label('gameplay_pc_01815e')
    e.ins('lea.l','0xd(%a0),%a1',4)
    e.label('gameplay_pc_018162')
    e.ins('moveq','#0,%d1',2)
    e.label('gameplay_pc_018164')
    e.ins('move.w','%d0,%d2',2)
    e.label('gameplay_pc_018166')
    e.ins('subq.w','#0x1,%d2',2)
    e.label('gameplay_pc_018168')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_01816a')
    e.ins('clr.w','%d4',2)
    e.label('gameplay_pc_01816c')
    e.ins('lea.l','0xc400:w,%a2',4)
    e.label('gameplay_pc_018170')
    e.ins('move.b','(%a1)+,%d3',2)
    e.label('gameplay_pc_018172')
    e.ins('move.b','(%a2, %d3.w),%d4',4)
    e.label('gameplay_pc_018176')
    e.ins('add.w','%d4,%d1',2)
    e.label('gameplay_pc_018178')
    e.ins('dbra','%d2,gameplay_pc_018170',4)
    e.label('gameplay_pc_01817c')
    e.ins('divu.w','%d0,%d1',2)
    e.label('gameplay_pc_01817e')
    e.ins('move.b','%d1,0x3(%a0)',4)
    e.label('gameplay_pc_018182')
    e.ins('rts','',2)

def _lower_copy_selected_city_group_parameter(e,rules):
    e.label('gameplay_pc_018184')
    e.ins('move.w','0xf6d6:w,%d0',4)
    e.label('gameplay_pc_018188')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_01818a')
    e.ins('movea.l','10(%pc, %d0.w),%a1',4)
    e.label('gameplay_pc_01818e')
    e.ins('move.b','0x1(%a1),0x4(%a0)',6)
    e.label('gameplay_pc_018194')
    e.ins('rts','',2)

def _lower_group_matches_city_head_carry(e,rules):
    e.label('gameplay_pc_0181a6')
    e.ins('btst.b','#0x1,0xf6d7:w',6)
    e.label('gameplay_pc_0181ac')
    e.ins('bne.w','gameplay_pc_0181c8',4)
    e.label('gameplay_pc_0181b0')
    e.ins('lea.l','0xa027:w,%a4',4)
    e.label('gameplay_pc_0181b4')
    e.ins('move.w','0xf68a:w,%d1',4)
    e.label('gameplay_pc_0181b8')
    e.ins('cmp.b','(%a4, %d1.w),%d0',4)
    e.label('gameplay_pc_0181bc')
    e.ins('bne.w','gameplay_pc_0181e2',4)
    e.label('gameplay_pc_0181c0')
    e.ins('ori.w','#0x1,%sr',4)
    e.label('gameplay_pc_0181c4')
    e.ins('bra.w','gameplay_pc_0181e6',4)
    e.label('gameplay_pc_0181c8')
    e.ins('lea.l','0xf45e:w,%a4',4)
    e.label('gameplay_pc_0181cc')
    e.ins('move.w','0xf68a:w,%d1',4)
    e.label('gameplay_pc_0181d0')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('gameplay_pc_0181d2')
    e.ins('cmp.w','(%a4, %d1.w),%d0',4)
    e.label('gameplay_pc_0181d6')
    e.ins('bne.w','gameplay_pc_0181e2',4)
    e.label('gameplay_pc_0181da')
    e.ins('ori.w','#0x1,%sr',4)
    e.label('gameplay_pc_0181de')
    e.ins('bra.w','gameplay_pc_0181e6',4)
    e.label('gameplay_pc_0181e2')
    e.ins('andi.w','#0xfffe,%sr',4)
    e.label('gameplay_pc_0181e6')
    e.ins('rts','',2)

def _lower_append_survivors_to_packed_group(e,rules):
    e.label('gameplay_pc_0181e8')
    e.ins('move.b','(%a0),%d0',2)
    e.label('gameplay_pc_0181ea')
    e.ins('andi.w','#0xf,%d0',4)
    e.label('gameplay_pc_0181ee')
    e.ins('lea.l','0xd(%a0, %d0.w),%a1',4)
    e.label('gameplay_pc_0181f2')
    e.ins('movea.l','%a1,%a3',2)
    e.label('gameplay_pc_0181f4')
    e.ins('add.b','%d6,(%a0)',2)
    e.label('gameplay_pc_0181f6')
    e.ins('add.w','%d6,%d0',2)
    e.label('gameplay_pc_0181f8')
    e.ins('lea.l','0xd(%a0, %d0.w),%a2',4)
    e.label('gameplay_pc_0181fc')
    e.ins('move.b','(%a1),%d0',2)
    e.label('gameplay_pc_0181fe')
    e.ins('andi.w','#0xf,%d0',4)
    e.label('gameplay_pc_018202')
    e.ins('beq.w','gameplay_pc_018212',4)
    e.label('gameplay_pc_018206')
    e.ins('addi.w','#0xc,%d0',4)
    e.label('gameplay_pc_01820a')
    e.ins('move.b','(%a1)+,(%a2)+',2)
    e.label('gameplay_pc_01820c')
    e.ins('dbra','%d0,gameplay_pc_01820a',4)
    e.label('gameplay_pc_018210')
    e.ins('bra.b','gameplay_pc_0181fc',2)
    e.label('gameplay_pc_018212')
    e.ins('clr.b','(%a2)',2)
    e.label('gameplay_pc_018214')
    e.ins('move.w','(%a4),%d0',2)
    e.label('gameplay_pc_018216')
    e.ins('bmi.w','gameplay_pc_018222',4)
    e.label('gameplay_pc_01821a')
    e.ins('move.w','#0xffff,(%a4)+',4)
    e.label('gameplay_pc_01821e')
    e.ins('move.b','%d0,(%a3)+',2)
    e.label('gameplay_pc_018220')
    e.ins('bra.b','gameplay_pc_018212',2)
    e.label('gameplay_pc_018222')
    e.ins('rts','',2)

def _lower_add_staged_resources_to_packed_group(e,rules):
    e.label('gameplay_pc_018224')
    e.ins('btst.b','#0x1,0xf6d7:w',6)
    e.label('gameplay_pc_01822a')
    e.ins('bne.w','gameplay_pc_01823a',4)
    e.label('gameplay_pc_01822e')
    e.ins('lea.l','0xf696:w,%a3',4)
    e.label('gameplay_pc_018232')
    e.ins('lea.l','0xf69e:w,%a4',4)
    e.label('gameplay_pc_018236')
    e.ins('bra.w','gameplay_pc_018242',4)
    e.label('gameplay_pc_01823a')
    e.ins('lea.l','0xf69a:w,%a3',4)
    e.label('gameplay_pc_01823e')
    e.ins('lea.l','0xf6a2:w,%a4',4)
    e.label('gameplay_pc_018242')
    e.ins('move.b','0x5(%a0),%d0',4)
    e.label('gameplay_pc_018246')
    e.ins('lsl.w','#0x8,%d0',2)
    e.label('gameplay_pc_018248')
    e.ins('move.b','0x6(%a0),%d0',4)
    e.label('gameplay_pc_01824c')
    e.ins('lsl.l','#0x8,%d0',2)
    e.label('gameplay_pc_01824e')
    e.ins('move.b','0x7(%a0),%d0',4)
    e.label('gameplay_pc_018252')
    e.ins('lsl.l','#0x8,%d0',2)
    e.label('gameplay_pc_018254')
    e.ins('move.b','0x8(%a0),%d0',4)
    e.label('gameplay_pc_018258')
    e.ins('add.l','(%a3),%d0',2)
    e.label('gameplay_pc_01825a')
    e.ins('cmpi.l','#0xf423f,%d0',6)
    e.label('gameplay_pc_018260')
    e.ins('bls.w','gameplay_pc_01826a',4)
    e.label('gameplay_pc_018264')
    e.ins('move.l','#0xf423f,%d0',6)
    e.label('gameplay_pc_01826a')
    e.ins('move.b','%d0,0x8(%a0)',4)
    e.label('gameplay_pc_01826e')
    e.ins('lsr.l','#0x8,%d0',2)
    e.label('gameplay_pc_018270')
    e.ins('move.b','%d0,0x7(%a0)',4)
    e.label('gameplay_pc_018274')
    e.ins('lsr.l','#0x8,%d0',2)
    e.label('gameplay_pc_018276')
    e.ins('move.b','%d0,0x6(%a0)',4)
    e.label('gameplay_pc_01827a')
    e.ins('lsr.w','#0x8,%d0',2)
    e.label('gameplay_pc_01827c')
    e.ins('move.b','%d0,0x5(%a0)',4)
    e.label('gameplay_pc_018280')
    e.ins('move.b','0x9(%a0),%d0',4)
    e.label('gameplay_pc_018284')
    e.ins('lsl.w','#0x8,%d0',2)
    e.label('gameplay_pc_018286')
    e.ins('move.b','0xa(%a0),%d0',4)
    e.label('gameplay_pc_01828a')
    e.ins('lsl.w','#0x8,%d0',2)
    e.label('gameplay_pc_01828c')
    e.ins('move.b','0xb(%a0),%d0',4)
    e.label('gameplay_pc_018290')
    e.ins('lsl.l','#0x8,%d0',2)
    e.label('gameplay_pc_018292')
    e.ins('move.b','0xc(%a0),%d0',4)
    e.label('gameplay_pc_018296')
    e.ins('add.l','(%a4),%d0',2)
    e.label('gameplay_pc_018298')
    e.ins('cmpi.l','#0xf423f,%d0',6)
    e.label('gameplay_pc_01829e')
    e.ins('bls.w','gameplay_pc_0182a8',4)
    e.label('gameplay_pc_0182a2')
    e.ins('move.l','#0xf423f,%d0',6)
    e.label('gameplay_pc_0182a8')
    e.ins('move.b','%d0,0xc(%a0)',4)
    e.label('gameplay_pc_0182ac')
    e.ins('lsr.l','#0x8,%d0',2)
    e.label('gameplay_pc_0182ae')
    e.ins('move.b','%d0,0xb(%a0)',4)
    e.label('gameplay_pc_0182b2')
    e.ins('lsr.l','#0x8,%d0',2)
    e.label('gameplay_pc_0182b4')
    e.ins('move.b','%d0,0xa(%a0)',4)
    e.label('gameplay_pc_0182b8')
    e.ins('lsr.w','#0x8,%d0',2)
    e.label('gameplay_pc_0182ba')
    e.ins('move.b','%d0,0x9(%a0)',4)
    e.label('gameplay_pc_0182be')
    e.ins('clr.l','(%a3)',2)
    e.label('gameplay_pc_0182c0')
    e.ins('clr.l','(%a4)',2)
    e.label('gameplay_pc_0182c2')
    e.ins('rts','',2)

def _lower_assign_city_survivor_roster_tokens(e,rules):
    e.label('gameplay_pc_0182c4')
    e.ins('movem.l','%d0-%d3/%a0/%a4-%a5,-(%a7)',4)
    e.label('gameplay_pc_0182c8')
    e.ins('bsr.w','gameplay_pc_01830a',4)
    e.label('gameplay_pc_0182cc')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('gameplay_pc_0182d0')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_0182d4')
    e.ins('move.w','0xf68c:w,%d3',4)
    e.label('gameplay_pc_0182d8')
    e.ins('btst.b','#0x1,0xf6d7:w',6)
    e.label('gameplay_pc_0182de')
    e.ins('beq.w','gameplay_pc_0182e6',4)
    e.label('gameplay_pc_0182e2')
    e.ins('move.w','0xf68e:w,%d3',4)
    e.label('gameplay_pc_0182e6')
    e.ins('addi.w','#0x69,%d3',4)
    e.label('gameplay_pc_0182ea')
    e.ins('lea.l','0xa150:w,%a5',4)
    e.label('gameplay_pc_0182ee')
    e.ins('move.w','(%a4)+,%d1',2)
    e.label('gameplay_pc_0182f0')
    e.ins('bmi.w','gameplay_pc_018304',4)
    e.label('gameplay_pc_0182f4')
    e.ins('andi.w','#0xff,%d1',4)
    e.label('gameplay_pc_0182f8')
    e.ins('move.b','%d3,(%a0, %d1.w)',4)
    e.label('gameplay_pc_0182fc')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('gameplay_pc_0182fe')
    e.ins('clr.l','(%a5, %d1.w)',4)
    e.label('gameplay_pc_018302')
    e.ins('bra.b','gameplay_pc_0182ee',2)
    e.label('gameplay_pc_018304')
    e.ins('movem.l','(%a7)+,%d0-%d3/%a0/%a4-%a5',4)
    e.label('gameplay_pc_018308')
    e.ins('rts','',2)

def _lower_merge_city_survivor_rosters(e,rules):
    e.label('gameplay_pc_01830a')
    e.ins('movem.l','%d0-%d2/%a3-%a6,-(%a7)',4)
    e.label('gameplay_pc_01830e')
    e.ins('lea.l','0xa57a:w,%a5',4)
    e.label('gameplay_pc_018312')
    e.ins('btst.b','#0x1,0xf6d7:w',6)
    e.label('gameplay_pc_018318')
    e.ins('beq.w','gameplay_pc_018320',4)
    e.label('gameplay_pc_01831c')
    e.ins('lea.l','0xa5ce:w,%a5',4)
    e.label('gameplay_pc_018320')
    e.ins('movea.l','%a5,%a3',2)
    e.label('gameplay_pc_018322')
    e.ins('clr.w','%d0',2)
    e.label('gameplay_pc_018324')
    e.ins('clr.w','%d1',2)
    e.label('gameplay_pc_018326')
    e.ins('tst.w','(%a4)+',2)
    e.label('gameplay_pc_018328')
    e.ins('bmi.w','gameplay_pc_018330',4)
    e.label('gameplay_pc_01832c')
    e.ins('addq.w','#0x1,%d0',2)
    e.label('gameplay_pc_01832e')
    e.ins('bra.b','gameplay_pc_018326',2)
    e.label('gameplay_pc_018330')
    e.ins('subq.w','#0x2,%a4',2)
    e.label('gameplay_pc_018332')
    e.ins('move.w','(%a5)+,(%a4)+',2)
    e.label('gameplay_pc_018334')
    e.ins('bmi.w','gameplay_pc_01833c',4)
    e.label('gameplay_pc_018338')
    e.ins('addq.w','#0x1,%d0',2)
    e.label('gameplay_pc_01833a')
    e.ins('bra.b','gameplay_pc_018332',2)
    e.label('gameplay_pc_01833c')
    e.ins('move.w','#0xffff,(%a3)',4)
    e.label('gameplay_pc_018340')
    e.ins('cmpi.w','#0xa,%d0',4)
    e.label('gameplay_pc_018344')
    e.ins('bls.w','gameplay_pc_0183b8',4)
    e.label('gameplay_pc_018348')
    e.ins('subi.w','#0xb,%d0',4)
    e.label('gameplay_pc_01834c')
    e.ins('subq.w','#0x2,%a4',2)
    e.label('gameplay_pc_01834e')
    e.ins('move.w','0xf68a:w,%d2',4)
    e.label('gameplay_pc_018352')
    e.ins('bset.l','#0x7,%d2',4)
    e.label('gameplay_pc_018356')
    e.ins('lea.l','0xcc00:w,%a6',4)
    e.label('gameplay_pc_01835a')
    e.ins('move.w','0xf68c:w,%d1',4)
    e.label('gameplay_pc_01835e')
    e.ins('btst.b','#0x1,0xf6d7:w',6)
    e.label('gameplay_pc_018364')
    e.ins('beq.w','gameplay_pc_01836c',4)
    e.label('gameplay_pc_018368')
    e.ins('move.w','0xf68e:w,%d1',4)
    e.label('gameplay_pc_01836c')
    e.ins('cmp.w','0xf67a:w,%d1',4)
    e.label('gameplay_pc_018370')
    e.ins('beq.w','gameplay_pc_018392',4)
    e.label('gameplay_pc_018374')
    e.ins('cmp.w','0xf67c:w,%d1',4)
    e.label('gameplay_pc_018378')
    e.ins('beq.w','gameplay_pc_018392',4)
    e.label('gameplay_pc_01837c')
    e.ins('cmp.w','0xf67e:w,%d1',4)
    e.label('gameplay_pc_018380')
    e.ins('beq.w','gameplay_pc_018392',4)
    e.label('gameplay_pc_018384')
    e.ins('move.w','-(%a4),%d1',2)
    e.label('gameplay_pc_018386')
    e.ins('move.b','%d2,(%a6, %d1.w)',4)
    e.label('gameplay_pc_01838a')
    e.ins('dbra','%d0,gameplay_pc_018384',4)
    e.label('gameplay_pc_01838e')
    e.ins('bra.w','gameplay_pc_0183b4',4)
    e.label('gameplay_pc_018392')
    e.ins('move.w','-(%a4),%d1',2)
    e.label('gameplay_pc_018394')
    e.ins('move.w','%d1,0xf3d0:w',4)
    e.label('gameplay_pc_018398')
    e.ins('move.b','%d2,(%a6, %d1.w)',4)
    e.label('gameplay_pc_01839c')
    e.ins('movem.l','%d0-%d7/%a0-%a7,-(%a7)',4)
    e.label('gameplay_pc_0183a0')
    e.ins('move.w','#0x140,0xf740:w',6)
    e.label('gameplay_pc_0183a6')
    e.ins('jsr','gameplay_pc_0260e4:l',6)
    e.label('gameplay_pc_0183ac')
    e.ins('movem.l','(%a7)+,%d0-%d7/%a0-%a7',4)
    e.label('gameplay_pc_0183b0')
    e.ins('dbra','%d0,gameplay_pc_018392',4)
    e.label('gameplay_pc_0183b4')
    e.ins('move.w','#0xffff,(%a4)',4)
    e.label('gameplay_pc_0183b8')
    e.ins('movem.l','(%a7)+,%d0-%d2/%a3-%a6',4)
    e.label('gameplay_pc_0183bc')
    e.ins('rts','',2)

def _lower_resolve_city_battle_damage(e,rules):
    e.label('gameplay_pc_0183f8')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_0183fe')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_018402')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_018404')
    e.ins('lea.l','0xe59c:w,%a0',4)
    e.label('gameplay_pc_018408')
    e.ins('move.l','(%a0, %d0.w),%d0',4)
    e.label('gameplay_pc_01840c')
    e.ins('moveq','#0,%d1',2)
    e.label('gameplay_pc_01840e')
    e.ins('move.w','0xf61c:w,%d1',4)
    e.label('gameplay_pc_018412')
    e.ins('move.l','%d1,%d2',2)
    e.label('gameplay_pc_018414')
    e.ins('lsl.l','#0x1,%d1',2)
    e.label('gameplay_pc_018416')
    e.ins('add.l','%d2,%d1',2)
    e.label('gameplay_pc_018418')
    e.ins('lsl.l','#0x1,%d1',2)
    e.label('gameplay_pc_01841a')
    e.ins('swap','%d1',2)
    e.label('gameplay_pc_01841c')
    e.ins('addi.w','#0x5,%d1',4)
    e.label('gameplay_pc_018420')
    e.ins('mulu.w','%d1,%d0',2)
    e.label('gameplay_pc_018422')
    e.ins('move.w','0xf6d6:w,%d1',4)
    e.label('gameplay_pc_018426')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('gameplay_pc_018428')
    e.ins('movea.l','-58(%pc, %d1.w),%a0',4)
    e.label('gameplay_pc_01842c')
    e.ins('clr.w','%d6',2)
    e.label('gameplay_pc_01842e')
    e.ins('move.l','(%a0),%d1',2)
    e.label('gameplay_pc_018430')
    e.ins('sub.l','%d0,%d1',2)
    e.label('gameplay_pc_018432')
    e.ins('bcc.b','gameplay_pc_01843a',2)
    e.label('gameplay_pc_018434')
    e.ins('moveq','#0,%d1',2)
    e.label('gameplay_pc_018436')
    e.ins('move.w','#0x1,%d6',4)
    e.label('gameplay_pc_01843a')
    e.ins('move.w','%d6,0xff3eda:l',6)
    e.label('gameplay_pc_018440')
    e.ins('move.l','%d1,(%a0)',2)
    e.label('gameplay_pc_018442')
    e.ins('lea.l','0xc800:w,%a0',4)
    e.label('gameplay_pc_018446')
    e.ins('move.w','0xf3f2:w,%d0',4)
    e.label('gameplay_pc_01844a')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_01844c')
    e.ins('move.l','(%a0, %d0.w),0xff3ed2:l',8)
    e.label('gameplay_pc_018454')
    e.ins('move.w','#0x700,0xff3ed6:l',8)
    e.label('gameplay_pc_01845c')
    e.ins('tst.w','0xf3a6:w',4)
    e.label('gameplay_pc_018460')
    e.ins('bmi.w','gameplay_pc_018556',4)
    e.label('gameplay_pc_018464')
    e.ins('jsr','gameplay_pc_01a706:l',6)
    e.label('gameplay_pc_01846a')
    e.ins('jsr','gameplay_pc_01a7a2:l',6)
    e.label('gameplay_pc_018470')
    e.ins('move.w','%d7,0xff3ed6:l',6)
    e.label('gameplay_pc_018476')
    e.ins('addi.w','#0xc8,%d7',4)
    e.label('gameplay_pc_01847a')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01847e')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_018480')
    e.ins('lea.l','0xe59c:w,%a0',4)
    e.label('gameplay_pc_018484')
    e.ins('move.l','(%a0, %d0.w),%d0',4)
    e.label('gameplay_pc_018488')
    e.ins('move.w','#0x64,%d1',4)
    e.label('gameplay_pc_01848c')
    e.ins('sub.w','%d0,%d1',2)
    e.label('gameplay_pc_01848e')
    e.ins('mulu.w','%d1,%d7',2)
    e.label('gameplay_pc_018490')
    e.ins('divu.w','#0x64,%d7',4)
    e.label('gameplay_pc_018494')
    e.ins('move.w','0xf3f2:w,%d0',4)
    e.label('gameplay_pc_018498')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01849a')
    e.ins('lea.l','0xc000:w,%a0',4)
    e.label('gameplay_pc_01849e')
    e.ins('move.w','(%a0, %d0.w),%d0',4)
    e.label('gameplay_pc_0184a2')
    e.ins('mulu.w','%d0,%d7',2)
    e.label('gameplay_pc_0184a4')
    e.ins('divu.w','#0x64,%d7',4)
    e.label('gameplay_pc_0184a8')
    e.ins('tst.w','0xff3eda:l',6)
    e.label('gameplay_pc_0184ae')
    e.ins('beq.w','gameplay_pc_0184be',4)
    e.label('gameplay_pc_0184b2')
    e.ins('andi.l','#0xffff,%d7',6)
    e.label('gameplay_pc_0184b8')
    e.ins('lsl.l','#0x2,%d7',2)
    e.label('gameplay_pc_0184ba')
    e.ins('divu.w','#0xa,%d7',4)
    e.label('gameplay_pc_0184be')
    e.ins('move.w','0xf3a6:w,%d0',4)
    e.label('gameplay_pc_0184c2')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_0184c4')
    e.ins('lea.l','0xc800:w,%a0',4)
    e.label('gameplay_pc_0184c8')
    e.ins('move.l','(%a0, %d0.w),%d1',4)
    e.label('gameplay_pc_0184cc')
    e.ins('sub.w','%d7,%d1',2)
    e.label('gameplay_pc_0184ce')
    e.ins('bcc.w','gameplay_pc_0184d4',4)
    e.label('gameplay_pc_0184d2')
    e.ins('clr.w','%d1',2)
    e.label('gameplay_pc_0184d4')
    e.ins('move.l','%d1,(%a0, %d0.w)',4)
    e.label('gameplay_pc_0184d8')
    e.ins('moveq','#0,%d5',2)
    e.label('gameplay_pc_0184da')
    e.ins('move.w','%d7,%d5',2)
    e.label('gameplay_pc_0184dc')
    e.ins('lsl.l','#0x1,%d5',2)
    e.label('gameplay_pc_0184de')
    e.ins('divu.w','#0x190,%d5',4)
    e.label('gameplay_pc_0184e2')
    e.ins('move.w','0xf3f2:w,%d0',4)
    e.label('gameplay_pc_0184e6')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_0184e8')
    e.ins('lea.l','0xc000:w,%a0',4)
    e.label('gameplay_pc_0184ec')
    e.ins('move.w','(%a0, %d0.w),%d1',4)
    e.label('gameplay_pc_0184f0')
    e.ins('move.w','%d1,%d2',2)
    e.label('gameplay_pc_0184f2')
    e.ins('add.w','%d5,%d1',2)
    e.label('gameplay_pc_0184f4')
    e.ins('cmpi.w','#0x3e7,%d1',4)
    e.label('gameplay_pc_0184f8')
    e.ins('bls.w','gameplay_pc_018500',4)
    e.label('gameplay_pc_0184fc')
    e.ins('move.w','#0x3e7,%d1',4)
    e.label('gameplay_pc_018500')
    e.ins('move.w','%d1,(%a0, %d0.w)',4)
    e.label('gameplay_pc_018504')
    e.ins('mulu.w','#0x7d0,%d7',4)
    e.label('gameplay_pc_018508')
    e.ins('divu.w','%d2,%d7',2)
    e.label('gameplay_pc_01850a')
    e.ins('tst.w','0xff3eda:l',6)
    e.label('gameplay_pc_018510')
    e.ins('beq.w','gameplay_pc_018516',4)
    e.label('gameplay_pc_018514')
    e.ins('lsl.w','#0x1,%d7',2)
    e.label('gameplay_pc_018516')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_018518')
    e.ins('lea.l','0xc800:w,%a0',4)
    e.label('gameplay_pc_01851c')
    e.ins('move.l','(%a0, %d0.w),%d1',4)
    e.label('gameplay_pc_018520')
    e.ins('sub.w','%d7,%d1',2)
    e.label('gameplay_pc_018522')
    e.ins('bcc.w','gameplay_pc_018528',4)
    e.label('gameplay_pc_018526')
    e.ins('clr.w','%d1',2)
    e.label('gameplay_pc_018528')
    e.ins('move.l','%d1,(%a0, %d0.w)',4)
    e.label('gameplay_pc_01852c')
    e.ins('andi.l','#0xffff,%d7',6)
    e.label('gameplay_pc_018532')
    e.ins('divu.w','#0x190,%d7',4)
    e.label('gameplay_pc_018536')
    e.ins('move.w','0xf3a6:w,%d0',4)
    e.label('gameplay_pc_01853a')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01853c')
    e.ins('lea.l','0xc000:w,%a0',4)
    e.label('gameplay_pc_018540')
    e.ins('move.w','(%a0, %d0.w),%d1',4)
    e.label('gameplay_pc_018544')
    e.ins('add.w','%d7,%d1',2)
    e.label('gameplay_pc_018546')
    e.ins('cmpi.w','#0x3e7,%d1',4)
    e.label('gameplay_pc_01854a')
    e.ins('bls.w','gameplay_pc_018552',4)
    e.label('gameplay_pc_01854e')
    e.ins('move.w','#0x3e7,%d1',4)
    e.label('gameplay_pc_018552')
    e.ins('move.w','%d1,(%a0, %d0.w)',4)
    e.label('gameplay_pc_018556')
    e.ins('bsr.w','gameplay_pc_0185e4',4)
    e.label('gameplay_pc_01855a')
    e.ins('move.w','0xf3f2:w,%d2',4)
    e.label('gameplay_pc_01855e')
    e.ins('lsl.w','#0x1,%d2',2)
    e.label('gameplay_pc_018560')
    e.ins('lea.l','0xbe00:w,%a0',4)
    e.label('gameplay_pc_018564')
    e.ins('move.w','(%a0, %d2.w),%d1',4)
    e.label('gameplay_pc_018568')
    e.ins('add.w','%d0,%d1',2)
    e.label('gameplay_pc_01856a')
    e.ins('cmpi.w','#0x3e7,%d1',4)
    e.label('gameplay_pc_01856e')
    e.ins('bls.b','gameplay_pc_018574',2)
    e.label('gameplay_pc_018570')
    e.ins('move.w','#0x3e7,%d1',4)
    e.label('gameplay_pc_018574')
    e.ins('move.w','%d1,(%a0, %d2.w)',4)
    e.label('gameplay_pc_018578')
    e.ins('move.w','0xf68c:w,%d0',4)
    e.label('gameplay_pc_01857c')
    e.ins('cmp.w','0xf67a:w,%d0',4)
    e.label('gameplay_pc_018580')
    e.ins('beq.w','gameplay_pc_018594',4)
    e.label('gameplay_pc_018584')
    e.ins('cmp.w','0xf67c:w,%d0',4)
    e.label('gameplay_pc_018588')
    e.ins('beq.w','gameplay_pc_018594',4)
    e.label('gameplay_pc_01858c')
    e.ins('cmp.w','0xf67e:w,%d0',4)
    e.label('gameplay_pc_018590')
    e.ins('bne.w','gameplay_pc_0185ac',4)
    e.label('gameplay_pc_018594')
    e.ins('cmpi.w','#0x411,0xf612:w',6)
    e.label('gameplay_pc_01859a')
    e.ins('beq.w','gameplay_pc_0185ac',4)
    e.label('gameplay_pc_01859e')
    e.ins('move.w','#0x18,0xff7026:l',8)
    e.label('gameplay_pc_0185a6')
    e.ins('jsr','gameplay_pc_01072c:l',6)
    e.label('gameplay_pc_0185ac')
    e.ins('rts','',2)

def _lower_award_city_reserve_attrition(e,rules):
    e.label('gameplay_pc_0185e4')
    e.ins('movem.l','%d1/%a0,-(%a7)',4)
    e.label('gameplay_pc_0185e8')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_0185ee')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_0185f4')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_0185f6')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_0185f8')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_0185fa')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_0185fc')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_0185fe')
    e.ins('addi.w','#0xa,%d0',4)
    e.label('gameplay_pc_018602')
    e.ins('moveq','#0,%d1',2)
    e.label('gameplay_pc_018604')
    e.ins('move.w','0xff3ed6:l,%d1',6)
    e.label('gameplay_pc_01860a')
    e.ins('addi.w','#0x64,%d1',4)
    e.label('gameplay_pc_01860e')
    e.ins('divu.w','#0xa,%d1',4)
    e.label('gameplay_pc_018612')
    e.ins('mulu.w','%d1,%d0',2)
    e.label('gameplay_pc_018614')
    e.ins('move.l','0xff3ed2:l,%d1',6)
    e.label('gameplay_pc_01861a')
    e.ins('addi.l','#0x1f4,%d1',6)
    e.label('gameplay_pc_018620')
    e.ins('divu.w','#0x64,%d1',4)
    e.label('gameplay_pc_018624')
    e.ins('mulu.w','%d1,%d0',2)
    e.label('gameplay_pc_018626')
    e.ins('move.w','0xf3f2:w,%d2',4)
    e.label('gameplay_pc_01862a')
    e.ins('lsl.w','#0x1,%d2',2)
    e.label('gameplay_pc_01862c')
    e.ins('lea.l','0xb400:w,%a0',4)
    e.label('gameplay_pc_018630')
    e.ins('move.w','(%a0, %d2.w),%d1',4)
    e.label('gameplay_pc_018634')
    e.ins('lea.l','0xb600:w,%a0',4)
    e.label('gameplay_pc_018638')
    e.ins('add.w','(%a0, %d2.w),%d1',4)
    e.label('gameplay_pc_01863c')
    e.ins('andi.l','#0xffff,%d1',6)
    e.label('gameplay_pc_018642')
    e.ins('divu.w','#0xa,%d1',4)
    e.label('gameplay_pc_018646')
    e.ins('mulu.w','%d1,%d0',2)
    e.label('gameplay_pc_018648')
    e.ins('divu.w','#0x4e20,%d0',4)
    e.label('gameplay_pc_01864c')
    e.ins('tst.w','0xff3eda:l',6)
    e.label('gameplay_pc_018652')
    e.ins('beq.w','gameplay_pc_018668',4)
    e.label('gameplay_pc_018656')
    e.ins('move.w','%d0,%d1',2)
    e.label('gameplay_pc_018658')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01865a')
    e.ins('add.w','%d1,%d0',2)
    e.label('gameplay_pc_01865c')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01865e')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_018664')
    e.ins('divu.w','#0xa,%d0',4)
    e.label('gameplay_pc_018668')
    e.ins('move.w','0xf68a:w,%d2',4)
    e.label('gameplay_pc_01866c')
    e.ins('lsl.w','#0x2,%d2',2)
    e.label('gameplay_pc_01866e')
    e.ins('lea.l','0xe59c:w,%a0',4)
    e.label('gameplay_pc_018672')
    e.ins('move.l','(%a0, %d2.w),%d1',4)
    e.label('gameplay_pc_018676')
    e.ins('sub.w','%d0,%d1',2)
    e.label('gameplay_pc_018678')
    e.ins('bcc.w','gameplay_pc_0186fc',4)
    e.label('gameplay_pc_01867c')
    e.ins('movem.l','%d0/%d2/%a0,-(%a7)',4)
    e.label('gameplay_pc_018680')
    e.ins('bsr.w','gameplay_pc_018706',4)
    e.label('gameplay_pc_018684')
    e.ins('bcs.w','gameplay_pc_0186f6',4)
    e.label('gameplay_pc_018688')
    e.ins('move.w','0xf68c:w,%d0',4)
    e.label('gameplay_pc_01868c')
    e.ins('cmp.w','0xf67a:w,%d0',4)
    e.label('gameplay_pc_018690')
    e.ins('beq.w','gameplay_pc_0186a4',4)
    e.label('gameplay_pc_018694')
    e.ins('cmp.w','0xf67c:w,%d0',4)
    e.label('gameplay_pc_018698')
    e.ins('beq.w','gameplay_pc_0186a4',4)
    e.label('gameplay_pc_01869c')
    e.ins('cmp.w','0xf67e:w,%d0',4)
    e.label('gameplay_pc_0186a0')
    e.ins('bne.w','gameplay_pc_0186b2',4)
    e.label('gameplay_pc_0186a4')
    e.ins('move.w','#0x18,0xff7026:l',8)
    e.label('gameplay_pc_0186ac')
    e.ins('jsr','gameplay_pc_01072c:l',6)
    e.label('gameplay_pc_0186b2')
    e.ins('move.w','0xf376:w,-(%a7)',4)
    e.label('gameplay_pc_0186b6')
    e.ins('move.w','0xf68c:w,0xf376:w',6)
    e.label('gameplay_pc_0186bc')
    e.ins('move.w','0xf68e:w,%d0',4)
    e.label('gameplay_pc_0186c0')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_0186c2')
    e.ins('lea.l','0xe640:w,%a0',4)
    e.label('gameplay_pc_0186c6')
    e.ins('move.w','(%a0, %d0.w),0xf3d0:w',6)
    e.label('gameplay_pc_0186cc')
    e.ins('move.w','#0x13f,0xf740:w',6)
    e.label('gameplay_pc_0186d2')
    e.ins('bchg.b','#0x1,0xf6d7:w',6)
    e.label('gameplay_pc_0186d8')
    e.ins('jsr','gameplay_pc_0260e4:l',6)
    e.label('gameplay_pc_0186de')
    e.ins('bchg.b','#0x1,0xf6d7:w',6)
    e.label('gameplay_pc_0186e4')
    e.ins('move.w','(%a7)+,0xf376:w',4)
    e.label('gameplay_pc_0186e8')
    e.ins('move.w','#0x411,0xf612:w',6)
    e.label('gameplay_pc_0186ee')
    e.ins('clr.w','0xf362:w',4)
    e.label('gameplay_pc_0186f2')
    e.ins('clr.w','0xf6d6:w',4)
    e.label('gameplay_pc_0186f6')
    e.ins('clr.w','%d1',2)
    e.label('gameplay_pc_0186f8')
    e.ins('movem.l','(%a7)+,%d0/%d2/%a0',4)
    e.label('gameplay_pc_0186fc')
    e.ins('move.w','%d1,0x2(%a0, %d2.w)',4)
    e.label('gameplay_pc_018700')
    e.ins('movem.l','(%a7)+,%d1/%a0',4)
    e.label('gameplay_pc_018704')
    e.ins('rts','',2)

def _lower_secondary_roster_has_terrain_six_carry(e,rules):
    e.label('gameplay_pc_018706')
    e.ins('movem.l','%d0-%d3/%a0-%a2,-(%a7)',4)
    e.label('gameplay_pc_01870a')
    e.ins('bsr.w','gameplay_pc_01a438',4)
    e.label('gameplay_pc_01870e')
    e.ins('lea.l','0xa5a4:w,%a1',4)
    e.label('gameplay_pc_018712')
    e.ins('lea.l','0xa150:w,%a2',4)
    e.label('gameplay_pc_018716')
    e.ins('move.w','(%a1)+,%d3',2)
    e.label('gameplay_pc_018718')
    e.ins('bmi.w','gameplay_pc_018740',4)
    e.label('gameplay_pc_01871c')
    e.ins('lsl.w','#0x2,%d3',2)
    e.label('gameplay_pc_01871e')
    e.ins('move.w','(%a2, %d3.w),%d1',4)
    e.label('gameplay_pc_018722')
    e.ins('lsr.w','#0x7,%d1',2)
    e.label('gameplay_pc_018724')
    e.ins('move.w','0x2(%a2, %d3.w),%d2',4)
    e.label('gameplay_pc_018728')
    e.ins('lsr.w','#0x7,%d2',2)
    e.label('gameplay_pc_01872a')
    e.ins('bsr.w','gameplay_pc_01a44e',4)
    e.label('gameplay_pc_01872e')
    e.ins('cmpi.b','#0x6,%d0',4)
    e.label('gameplay_pc_018732')
    e.ins('bne.b','gameplay_pc_018716',2)
    e.label('gameplay_pc_018734')
    e.ins('movem.l','(%a7)+,%d0-%d3/%a0-%a2',4)
    e.label('gameplay_pc_018738')
    e.ins('ori.w','#0x1,%sr',4)
    e.label('gameplay_pc_01873c')
    e.ins('bra.w','gameplay_pc_018748',4)
    e.label('gameplay_pc_018740')
    e.ins('movem.l','(%a7)+,%d0-%d3/%a0-%a2',4)
    e.label('gameplay_pc_018744')
    e.ins('andi.w','#0xfffe,%sr',4)
    e.label('gameplay_pc_018748')
    e.ins('rts','',2)

def _lower_sample_battle_special_status_factor(e,rules):
    e.label('gameplay_pc_01a706')
    e.ins('move.w','0xefd2:w,%d5',4)
    e.label('gameplay_pc_01a70a')
    e.ins('lsl.w','#0x1,%d5',2)
    e.label('gameplay_pc_01a70c')
    e.ins('add.w','0xefd2:w,%d5',4)
    e.label('gameplay_pc_01a710')
    e.ins('lsl.w','#0x3,%d5',2)
    e.label('gameplay_pc_01a712')
    e.ins('lea.l','0xd300:w,%a0',4)
    e.label('gameplay_pc_01a716')
    e.ins('lea.l','0xc700:w,%a2',4)
    e.label('gameplay_pc_01a71a')
    e.ins('clr.w','%d1',2)
    e.label('gameplay_pc_01a71c')
    e.ins('lea.l','0xa550:w,%a1',4)
    e.label('gameplay_pc_01a720')
    e.ins('bsr.w','gameplay_pc_01a78a',4)
    e.label('gameplay_pc_01a724')
    e.ins('move.w','#0x2,%d1',4)
    e.label('gameplay_pc_01a728')
    e.ins('lea.l','0xa5a4:w,%a1',4)
    e.label('gameplay_pc_01a72c')
    e.ins('bsr.w','gameplay_pc_01a78a',4)
    e.label('gameplay_pc_01a730')
    e.ins('move.w','#0xffff,(%a0)',4)
    e.label('gameplay_pc_01a734')
    e.ins('tst.w','0xd300:w',4)
    e.label('gameplay_pc_01a738')
    e.ins('bmi.w','gameplay_pc_01a76e',4)
    e.label('gameplay_pc_01a73c')
    e.ins('addq.w','#0x4,%d5',2)
    e.label('gameplay_pc_01a73e')
    e.ins('lea.l','0xd300:w,%a0',4)
    e.label('gameplay_pc_01a742')
    e.ins('lea.l','0xb600:w,%a1',4)
    e.label('gameplay_pc_01a746')
    e.ins('clr.w','%d0',2)
    e.label('gameplay_pc_01a748')
    e.ins('move.w','(%a0)+,%d2',2)
    e.label('gameplay_pc_01a74a')
    e.ins('bmi.b','gameplay_pc_01a75e',2)
    e.label('gameplay_pc_01a74c')
    e.ins('move.w','%d2,%d3',2)
    e.label('gameplay_pc_01a74e')
    e.ins('lsl.w','#0x1,%d3',2)
    e.label('gameplay_pc_01a750')
    e.ins('move.w','(%a1, %d3.w),%d4',4)
    e.label('gameplay_pc_01a754')
    e.ins('cmp.w','%d0,%d4',2)
    e.label('gameplay_pc_01a756')
    e.ins('bcs.b','gameplay_pc_01a748',2)
    e.label('gameplay_pc_01a758')
    e.ins('move.w','%d2,%d1',2)
    e.label('gameplay_pc_01a75a')
    e.ins('move.w','%d4,%d0',2)
    e.label('gameplay_pc_01a75c')
    e.ins('bra.b','gameplay_pc_01a748',2)
    e.label('gameplay_pc_01a75e')
    e.ins('lsr.w','#0x4,%d1',2)
    e.label('gameplay_pc_01a760')
    e.ins('move.w','0xf6d6:w,%d0',4)
    e.label('gameplay_pc_01a764')
    e.ins('eor.w','%d0,%d1',2)
    e.label('gameplay_pc_01a766')
    e.ins('btst.l','#0x1,%d1',4)
    e.label('gameplay_pc_01a76a')
    e.ins('beq.b','gameplay_pc_01a76e',2)
    e.label('gameplay_pc_01a76c')
    e.ins('addq.w','#0x4,%d5',2)
    e.label('gameplay_pc_01a76e')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01a774')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01a77a')
    e.ins('lea.l','-1440(%pc),%a0',4)
    e.label('gameplay_pc_01a77e')
    e.ins('mulu.w','(%a0, %d5.w),%d0',4)
    e.label('gameplay_pc_01a782')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01a784')
    e.ins('add.w','0x2(%a0, %d5.w),%d0',4)
    e.label('gameplay_pc_01a788')
    e.ins('rts','',2)

def _lower_collect_battle_special_status_members(e,rules):
    e.label('gameplay_pc_01a78a')
    e.ins('move.w','(%a1)+,%d0',2)
    e.label('gameplay_pc_01a78c')
    e.ins('bmi.b','gameplay_pc_01a7a0',2)
    e.label('gameplay_pc_01a78e')
    e.ins('andi.w','#0xff,%d0',4)
    e.label('gameplay_pc_01a792')
    e.ins('btst.b','#0x4,(%a2, %d0.w)',6)
    e.label('gameplay_pc_01a798')
    e.ins('beq.b','gameplay_pc_01a78a',2)
    e.label('gameplay_pc_01a79a')
    e.ins('or.w','%d1,%d0',2)
    e.label('gameplay_pc_01a79c')
    e.ins('move.w','%d0,(%a0)+',2)
    e.label('gameplay_pc_01a79e')
    e.ins('bra.b','gameplay_pc_01a78a',2)
    e.label('gameplay_pc_01a7a0')
    e.ins('rts','',2)

def _lower_compute_battle_damage_potential(e,rules):
    e.label('gameplay_pc_01a7a2')
    e.ins('mulu.w','#0x64,%d0',4)
    e.label('gameplay_pc_01a7a6')
    e.ins('lea.l','0xb600:w,%a0',4)
    e.label('gameplay_pc_01a7aa')
    e.ins('move.w','0xf3a6:w,%d1',4)
    e.label('gameplay_pc_01a7ae')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('gameplay_pc_01a7b0')
    e.ins('move.w','(%a0, %d1.w),%d1',4)
    e.label('gameplay_pc_01a7b4')
    e.ins('mulu.w','%d0,%d1',2)
    e.label('gameplay_pc_01a7b6')
    e.ins('move.w','0xf3f2:w,%d0',4)
    e.label('gameplay_pc_01a7ba')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01a7bc')
    e.ins('move.w','(%a0, %d0.w),%d0',4)
    e.label('gameplay_pc_01a7c0')
    e.ins('mulu.w','#0x3e8,%d0',4)
    e.label('gameplay_pc_01a7c4')
    e.ins('sub.l','%d1,%d0',2)
    e.label('gameplay_pc_01a7c6')
    e.ins('bcs.w','gameplay_pc_01a7f0',4)
    e.label('gameplay_pc_01a7ca')
    e.ins('lea.l','0xc000:w,%a0',4)
    e.label('gameplay_pc_01a7ce')
    e.ins('move.w','0xf3a6:w,%d1',4)
    e.label('gameplay_pc_01a7d2')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('gameplay_pc_01a7d4')
    e.ins('move.w','(%a0, %d1.w),%d1',4)
    e.label('gameplay_pc_01a7d8')
    e.ins('addi.w','#0x64,%d1',4)
    e.label('gameplay_pc_01a7dc')
    e.ins('divu.w','%d1,%d0',2)
    e.label('gameplay_pc_01a7de')
    e.ins('move.w','%d0,%d7',2)
    e.label('gameplay_pc_01a7e0')
    e.ins('cmpi.w','#0x2bc,%d0',4)
    e.label('gameplay_pc_01a7e4')
    e.ins('bls.w','gameplay_pc_01a7ec',4)
    e.label('gameplay_pc_01a7e8')
    e.ins('move.w','#0x2bc,%d0',4)
    e.label('gameplay_pc_01a7ec')
    e.ins('bra.w','gameplay_pc_01a7f2',4)
    e.label('gameplay_pc_01a7f0')
    e.ins('clr.w','%d7',2)
    e.label('gameplay_pc_01a7f2')
    e.ins('rts','',2)

def _lower_settle_city_battle_outcome(e,rules):
    e.label('gameplay_pc_01bfec')
    e.ins('move.w','#0x20,0xf352:w',6)
    e.label('gameplay_pc_01bff2')
    e.ins('lea.l','0xf427:w,%a0',4)
    e.label('gameplay_pc_01bff6')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01bffa')
    e.ins('clr.w','0xf68e:w',4)
    e.label('gameplay_pc_01bffe')
    e.ins('move.b','(%a0, %d0.w),0xf68f:w',6)
    e.label('gameplay_pc_01c004')
    e.ins('lea.l','0xa050:w,%a0',4)
    e.label('gameplay_pc_01c008')
    e.ins('move.w','#0xff,%d1',4)
    e.label('gameplay_pc_01c00c')
    e.ins('cmp.b','(%a0, %d1.w),%d0',4)
    e.label('gameplay_pc_01c010')
    e.ins('beq.b','gameplay_pc_01c016',2)
    e.label('gameplay_pc_01c012')
    e.ins('dbra','%d1,gameplay_pc_01c00c',4)
    e.label('gameplay_pc_01c016')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('gameplay_pc_01c01a')
    e.ins('clr.w','%d0',2)
    e.label('gameplay_pc_01c01c')
    e.ins('move.b','(%a0, %d1.w),%d0',4)
    e.label('gameplay_pc_01c020')
    e.ins('andi.w','#0x3f,%d0',4)
    e.label('gameplay_pc_01c024')
    e.ins('lea.l','0xf427:w,%a0',4)
    e.label('gameplay_pc_01c028')
    e.ins('clr.w','0xf68c:w',4)
    e.label('gameplay_pc_01c02c')
    e.ins('move.b','(%a0, %d0.w),0xf68d:w',6)
    e.label('gameplay_pc_01c032')
    e.ins('lea.l','0xe640:w,%a0',4)
    e.label('gameplay_pc_01c036')
    e.ins('move.w','0xf68c:w,%d0',4)
    e.label('gameplay_pc_01c03a')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01c03c')
    e.ins('move.w','(%a0, %d0.w),0xf3d0:w',6)
    e.label('gameplay_pc_01c042')
    e.ins('move.w','0xf68e:w,%d0',4)
    e.label('gameplay_pc_01c046')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01c048')
    e.ins('move.w','(%a0, %d0.w),0xf3d2:w',6)
    e.label('gameplay_pc_01c04e')
    e.ins('move.w','0xf362:w,-(%a7)',4)
    e.label('gameplay_pc_01c052')
    e.ins('move.w','#0x9f,0xf740:w',6)
    e.label('gameplay_pc_01c058')
    e.ins('clr.w','0xf362:w',4)
    e.label('gameplay_pc_01c05c')
    e.ins('move.w','#0x12c,0xf608:w',6)
    e.label('gameplay_pc_01c062')
    e.ins('clr.w','0xf362:w',4)
    e.label('gameplay_pc_01c066')
    e.ins('jsr','gameplay_pc_030a74:l',6)
    e.label('gameplay_pc_01c06c')
    e.ins('move.w','(%a7)+,0xf362:w',4)
    e.label('gameplay_pc_01c070')
    e.ins('bsr.w','gameplay_pc_01c466',4)
    e.label('gameplay_pc_01c074')
    e.ins('bsr.w','gameplay_pc_01c1c2',4)
    e.label('gameplay_pc_01c078')
    e.ins('cmpi.w','#0xa,%d1',4)
    e.label('gameplay_pc_01c07c')
    e.ins('bcc.w','gameplay_pc_01c0ec',4)
    e.label('gameplay_pc_01c080')
    e.ins('bsr.w','gameplay_pc_01c2fc',4)
    e.label('gameplay_pc_01c084')
    e.ins('bsr.w','gameplay_pc_01c39c',4)
    e.label('gameplay_pc_01c088')
    e.ins('bsr.w','gameplay_pc_01c57c',4)
    e.label('gameplay_pc_01c08c')
    e.ins('bsr.w','gameplay_pc_01c5e2',4)
    e.label('gameplay_pc_01c090')
    e.ins('bsr.w','gameplay_pc_01c554',4)
    e.label('gameplay_pc_01c094')
    e.ins('bsr.w','gameplay_pc_01c732',4)
    e.label('gameplay_pc_01c098')
    e.ins('bsr.w','gameplay_pc_01c82c',4)
    e.label('gameplay_pc_01c09c')
    e.ins('bsr.w','gameplay_pc_01cb96',4)
    e.label('gameplay_pc_01c0a0')
    e.ins('bsr.w','gameplay_pc_01cc94',4)
    e.label('gameplay_pc_01c0a4')
    e.ins('clr.w','0xf6d6:w',4)
    e.label('gameplay_pc_01c0a8')
    e.ins('lea.l','0xe640:w,%a0',4)
    e.label('gameplay_pc_01c0ac')
    e.ins('move.w','0xf68c:w,%d0',4)
    e.label('gameplay_pc_01c0b0')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01c0b2')
    e.ins('move.w','(%a0, %d0.w),0xf3d0:w',6)
    e.label('gameplay_pc_01c0b8')
    e.ins('move.w','0xf68e:w,%d0',4)
    e.label('gameplay_pc_01c0bc')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01c0be')
    e.ins('move.w','(%a0, %d0.w),0xf3d2:w',6)
    e.label('gameplay_pc_01c0c4')
    e.ins('move.w','0xf68a:w,0xf646:w',6)
    e.label('gameplay_pc_01c0ca')
    e.ins('move.w','0xf362:w,-(%a7)',4)
    e.label('gameplay_pc_01c0ce')
    e.ins('move.w','#0xa1,0xf740:w',6)
    e.label('gameplay_pc_01c0d4')
    e.ins('move.w','#0x12c,0xf608:w',6)
    e.label('gameplay_pc_01c0da')
    e.ins('clr.w','0xf362:w',4)
    e.label('gameplay_pc_01c0de')
    e.ins('jsr','gameplay_pc_030a74:l',6)
    e.label('gameplay_pc_01c0e4')
    e.ins('move.w','(%a7)+,0xf362:w',4)
    e.label('gameplay_pc_01c0e8')
    e.ins('bra.w','gameplay_pc_01c14e',4)
    e.label('gameplay_pc_01c0ec')
    e.ins('bsr.w','gameplay_pc_01c5ee',4)
    e.label('gameplay_pc_01c0f0')
    e.ins('bsr.w','gameplay_pc_01c69e',4)
    e.label('gameplay_pc_01c0f4')
    e.ins('bsr.w','gameplay_pc_01c57c',4)
    e.label('gameplay_pc_01c0f8')
    e.ins('bsr.w','gameplay_pc_01c5e2',4)
    e.label('gameplay_pc_01c0fc')
    e.ins('bsr.w','gameplay_pc_01c78c',4)
    e.label('gameplay_pc_01c100')
    e.ins('bsr.w','gameplay_pc_01c7c4',4)
    e.label('gameplay_pc_01c104')
    e.ins('bsr.w','gameplay_pc_01cb08',4)
    e.label('gameplay_pc_01c108')
    e.ins('move.w','#0x2,0xf6d6:w',6)
    e.label('gameplay_pc_01c10e')
    e.ins('lea.l','0xe640:w,%a0',4)
    e.label('gameplay_pc_01c112')
    e.ins('move.w','0xf68c:w,%d0',4)
    e.label('gameplay_pc_01c116')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01c118')
    e.ins('move.w','(%a0, %d0.w),0xf3d0:w',6)
    e.label('gameplay_pc_01c11e')
    e.ins('move.w','0xf68e:w,%d0',4)
    e.label('gameplay_pc_01c122')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01c124')
    e.ins('move.w','(%a0, %d0.w),0xf3d2:w',6)
    e.label('gameplay_pc_01c12a')
    e.ins('move.w','0xf68a:w,0xf646:w',6)
    e.label('gameplay_pc_01c130')
    e.ins('move.w','0xf362:w,-(%a7)',4)
    e.label('gameplay_pc_01c134')
    e.ins('move.w','#0xa2,0xf740:w',6)
    e.label('gameplay_pc_01c13a')
    e.ins('move.w','#0x12c,0xf608:w',6)
    e.label('gameplay_pc_01c140')
    e.ins('clr.w','0xf362:w',4)
    e.label('gameplay_pc_01c144')
    e.ins('jsr','gameplay_pc_030a74:l',6)
    e.label('gameplay_pc_01c14a')
    e.ins('move.w','(%a7)+,0xf362:w',4)
    e.label('gameplay_pc_01c14e')
    e.ins('bsr.w','gameplay_pc_0217c8',4)
    e.label('gameplay_pc_01c152')
    e.ins('bsr.w','gameplay_pc_01cc76',4)
    e.label('gameplay_pc_01c156')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01c15a')
    e.ins('lea.l','0xea37:w,%a0',4)
    e.label('gameplay_pc_01c15e')
    e.ins('clr.b','(%a0, %d0.w)',4)
    e.label('gameplay_pc_01c162')
    e.ins('move.w','#0x201,0xf612:w',6)
    e.label('gameplay_pc_01c168')
    e.ins('move.l','#0xc0000026,%d0',6)
    e.label('gameplay_pc_01c16e')
    e.ins('move.w','#0x7,%d1',4)
    e.label('gameplay_pc_01c172')
    e.ins('move.w','#0xca02,%d2',4)
    e.label('gameplay_pc_01c176')
    e.ins('lea.l','46(%pc),%a0',4)
    e.label('gameplay_pc_01c17a')
    e.ins('nop','',2)
    e.label('gameplay_pc_01c17c')
    e.ins('jsr','gameplay_pc_026bfa:l',6)
    e.label('gameplay_pc_01c182')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01c186')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_01c188')
    e.ins('lea.l','0xee24:w,%a0',4)
    e.label('gameplay_pc_01c18c')
    e.ins('clr.l','(%a0, %d0.w)',4)
    e.label('gameplay_pc_01c190')
    e.ins('lea.l','0xed84:w,%a0',4)
    e.label('gameplay_pc_01c194')
    e.ins('clr.l','(%a0, %d0.w)',4)
    e.label('gameplay_pc_01c198')
    e.ins('move.b','0xf68d:w,0xa622:w',6)
    e.label('gameplay_pc_01c19e')
    e.ins('move.b','0xf68f:w,0xa623:w',6)
    e.label('gameplay_pc_01c1a4')
    e.ins('rts','',2)

def _lower_sample_city_postbattle_reserve(e,rules):
    e.label('gameplay_pc_01c554')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c55a')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c560')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_01c562')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_01c564')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01c566')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('gameplay_pc_01c568')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01c56a')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c56c')
    e.ins('lea.l','0xe59c:w,%a0',4)
    e.label('gameplay_pc_01c570')
    e.ins('move.w','0xf68a:w,%d1',4)
    e.label('gameplay_pc_01c574')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('gameplay_pc_01c576')
    e.ins('move.w','%d0,0x2(%a0, %d1.w)',4)
    e.label('gameplay_pc_01c57a')
    e.ins('rts','',2)

def _lower_distribute_city_battle_progress(e,rules):
    e.label('gameplay_pc_01c57c')
    e.ins('bsr.w','gameplay_pc_01c2a0',4)
    e.label('gameplay_pc_01c580')
    e.ins('move.w','0xefb8:w,%d0',4)
    e.label('gameplay_pc_01c584')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('gameplay_pc_01c586')
    e.ins('tst.w','%d3',2)
    e.label('gameplay_pc_01c588')
    e.ins('beq.w','gameplay_pc_01c5e0',4)
    e.label('gameplay_pc_01c58c')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c592')
    e.ins('divu.w','%d3,%d0',2)
    e.label('gameplay_pc_01c594')
    e.ins('lea.l','0xd300:w,%a0',4)
    e.label('gameplay_pc_01c598')
    e.ins('lea.l','0xc000:w,%a1',4)
    e.label('gameplay_pc_01c59c')
    e.ins('lea.l','0xbe00:w,%a2',4)
    e.label('gameplay_pc_01c5a0')
    e.ins('move.w','(%a0)+,%d1',2)
    e.label('gameplay_pc_01c5a2')
    e.ins('bmi.w','gameplay_pc_01c5e0',4)
    e.label('gameplay_pc_01c5a6')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('gameplay_pc_01c5a8')
    e.ins('move.w','(%a1, %d1.w),%d2',4)
    e.label('gameplay_pc_01c5ac')
    e.ins('cmp.w','(%a2, %d1.w),%d2',4)
    e.label('gameplay_pc_01c5b0')
    e.ins('bls.w','gameplay_pc_01c5c8',4)
    e.label('gameplay_pc_01c5b4')
    e.ins('add.w','%d0,%d2',2)
    e.label('gameplay_pc_01c5b6')
    e.ins('cmpi.w','#0x3e7,%d2',4)
    e.label('gameplay_pc_01c5ba')
    e.ins('bls.w','gameplay_pc_01c5c2',4)
    e.label('gameplay_pc_01c5be')
    e.ins('move.w','#0x3e7,%d2',4)
    e.label('gameplay_pc_01c5c2')
    e.ins('move.w','%d2,(%a1, %d1.w)',4)
    e.label('gameplay_pc_01c5c6')
    e.ins('bra.b','gameplay_pc_01c5a0',2)
    e.label('gameplay_pc_01c5c8')
    e.ins('move.w','(%a2, %d1.w),%d2',4)
    e.label('gameplay_pc_01c5cc')
    e.ins('add.w','%d0,%d2',2)
    e.label('gameplay_pc_01c5ce')
    e.ins('cmpi.w','#0x3e7,%d2',4)
    e.label('gameplay_pc_01c5d2')
    e.ins('bls.w','gameplay_pc_01c5da',4)
    e.label('gameplay_pc_01c5d6')
    e.ins('move.w','#0x3e7,%d2',4)
    e.label('gameplay_pc_01c5da')
    e.ins('move.w','%d2,(%a2, %d1.w)',4)
    e.label('gameplay_pc_01c5de')
    e.ins('bra.b','gameplay_pc_01c5a0',2)
    e.label('gameplay_pc_01c5e0')
    e.ins('rts','',2)

def _lower_apply_assigned_city_light_attrition(e,rules):
    e.label('gameplay_pc_01c69e')
    e.ins('bsr.w','gameplay_pc_01c2a0',4)
    e.label('gameplay_pc_01c6a2')
    e.ins('lea.l','0xd300:w,%a0',4)
    e.label('gameplay_pc_01c6a6')
    e.ins('lea.l','0xc800:w,%a1',4)
    e.label('gameplay_pc_01c6aa')
    e.ins('lea.l','0xb200:w,%a2',4)
    e.label('gameplay_pc_01c6ae')
    e.ins('lea.l','0xc000:w,%a3',4)
    e.label('gameplay_pc_01c6b2')
    e.ins('lea.l','0xc700:w,%a4',4)
    e.label('gameplay_pc_01c6b6')
    e.ins('lea.l','0xcc00:w,%a5',4)
    e.label('gameplay_pc_01c6ba')
    e.ins('lea.l','0xf45e:w,%a6',4)
    e.label('gameplay_pc_01c6be')
    e.ins('clr.w','%d7',2)
    e.label('gameplay_pc_01c6c0')
    e.ins('move.w','(%a0)+,%d2',2)
    e.label('gameplay_pc_01c6c2')
    e.ins('bmi.w','gameplay_pc_01c72c',4)
    e.label('gameplay_pc_01c6c6')
    e.ins('lsl.w','#0x2,%d2',2)
    e.label('gameplay_pc_01c6c8')
    e.ins('move.l','(%a1, %d2.w),%d3',4)
    e.label('gameplay_pc_01c6cc')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c6d2')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c6d8')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_01c6da')
    e.ins('lsl.l','#0x5,%d0',2)
    e.label('gameplay_pc_01c6dc')
    e.ins('sub.l','%d1,%d0',2)
    e.label('gameplay_pc_01c6de')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c6e0')
    e.ins('addi.w','#0x1e,%d0',4)
    e.label('gameplay_pc_01c6e4')
    e.ins('mulu.w','%d3,%d0',2)
    e.label('gameplay_pc_01c6e6')
    e.ins('divu.w','#0x64,%d0',4)
    e.label('gameplay_pc_01c6ea')
    e.ins('sub.w','%d0,%d3',2)
    e.label('gameplay_pc_01c6ec')
    e.ins('move.w','%d3,0x2(%a1, %d2.w)',4)
    e.label('gameplay_pc_01c6f0')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c6f6')
    e.ins('divu.w','#0x190,%d0',4)
    e.label('gameplay_pc_01c6fa')
    e.ins('add.w','%d0,%d7',2)
    e.label('gameplay_pc_01c6fc')
    e.ins('lsr.w','#0x1,%d2',2)
    e.label('gameplay_pc_01c6fe')
    e.ins('move.w','(%a2, %d2.w),%d3',4)
    e.label('gameplay_pc_01c702')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c708')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c70e')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_01c710')
    e.ins('lsl.l','#0x5,%d0',2)
    e.label('gameplay_pc_01c712')
    e.ins('sub.l','%d1,%d0',2)
    e.label('gameplay_pc_01c714')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c716')
    e.ins('mulu.w','%d3,%d0',2)
    e.label('gameplay_pc_01c718')
    e.ins('divu.w','#0x64,%d0',4)
    e.label('gameplay_pc_01c71c')
    e.ins('sub.w','%d0,%d3',2)
    e.label('gameplay_pc_01c71e')
    e.ins('bne.w','gameplay_pc_01c726',4)
    e.label('gameplay_pc_01c722')
    e.ins('move.w','#0x1,%d3',4)
    e.label('gameplay_pc_01c726')
    e.ins('move.w','%d3,(%a2, %d2.w)',4)
    e.label('gameplay_pc_01c72a')
    e.ins('bra.b','gameplay_pc_01c6c0',2)
    e.label('gameplay_pc_01c72c')
    e.ins('move.w','%d7,0xefba:w',4)
    e.label('gameplay_pc_01c730')
    e.ins('rts','',2)

def _lower_consume_city_battle_supply_long(e,rules):
    e.label('gameplay_pc_01c732')
    e.ins('move.w','0xefbc:w,%d0',4)
    e.label('gameplay_pc_01c736')
    e.ins('mulu.w','#0x5a,%d0',4)
    e.label('gameplay_pc_01c73a')
    e.ins('lea.l','0xed84:w,%a0',4)
    e.label('gameplay_pc_01c73e')
    e.ins('move.w','0xf68a:w,%d1',4)
    e.label('gameplay_pc_01c742')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('gameplay_pc_01c744')
    e.ins('move.l','(%a0, %d1.w),%d2',4)
    e.label('gameplay_pc_01c748')
    e.ins('mulu.w','%d2,%d0',2)
    e.label('gameplay_pc_01c74a')
    e.ins('divu.w','#0x3e8,%d0',4)
    e.label('gameplay_pc_01c74e')
    e.ins('sub.l','%d0,%d2',2)
    e.label('gameplay_pc_01c750')
    e.ins('bcc.w','gameplay_pc_01c756',4)
    e.label('gameplay_pc_01c754')
    e.ins('moveq','#0,%d2',2)
    e.label('gameplay_pc_01c756')
    e.ins('move.l','%d2,(%a0, %d1.w)',4)
    e.label('gameplay_pc_01c75a')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c760')
    e.ins('mulu.w','#0x1f5,%d0',4)
    e.label('gameplay_pc_01c764')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c766')
    e.ins('addi.w','#0x1f4,%d0',4)
    e.label('gameplay_pc_01c76a')
    e.ins('lea.l','0xdffc:w,%a0',4)
    e.label('gameplay_pc_01c76e')
    e.ins('move.w','0xf68a:w,%d1',4)
    e.label('gameplay_pc_01c772')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('gameplay_pc_01c774')
    e.ins('move.l','(%a0, %d1.w),%d2',4)
    e.label('gameplay_pc_01c778')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c77e')
    e.ins('sub.l','%d0,%d2',2)
    e.label('gameplay_pc_01c780')
    e.ins('bcc.w','gameplay_pc_01c786',4)
    e.label('gameplay_pc_01c784')
    e.ins('moveq','#0,%d2',2)
    e.label('gameplay_pc_01c786')
    e.ins('move.l','%d2,(%a0, %d1.w)',4)
    e.label('gameplay_pc_01c78a')
    e.ins('rts','',2)

def _lower_reduce_city_reserve_after_defeat(e,rules):
    e.label('gameplay_pc_01c78c')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c792')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c798')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_01c79a')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_01c79c')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01c79e')
    e.ins('lsl.l','#0x3,%d0',2)
    e.label('gameplay_pc_01c7a0')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01c7a2')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_01c7a4')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01c7a6')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c7a8')
    e.ins('lea.l','0xe59c:w,%a0',4)
    e.label('gameplay_pc_01c7ac')
    e.ins('move.w','0xf68a:w,%d1',4)
    e.label('gameplay_pc_01c7b0')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('gameplay_pc_01c7b2')
    e.ins('move.l','(%a0, %d1.w),%d2',4)
    e.label('gameplay_pc_01c7b6')
    e.ins('mulu.w','%d2,%d0',2)
    e.label('gameplay_pc_01c7b8')
    e.ins('divu.w','#0x64,%d0',4)
    e.label('gameplay_pc_01c7bc')
    e.ins('sub.w','%d0,%d2',2)
    e.label('gameplay_pc_01c7be')
    e.ins('move.w','%d2,0x2(%a0, %d1.w)',4)
    e.label('gameplay_pc_01c7c2')
    e.ins('rts','',2)

def _lower_consume_city_battle_supply_word(e,rules):
    e.label('gameplay_pc_01c7c4')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c7ca')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c7d0')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_01c7d2')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_01c7d4')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01c7d6')
    e.ins('lsl.l','#0x3,%d0',2)
    e.label('gameplay_pc_01c7d8')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_01c7da')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c7dc')
    e.ins('addi.w','#0x32,%d0',4)
    e.label('gameplay_pc_01c7e0')
    e.ins('lea.l','0xed84:w,%a0',4)
    e.label('gameplay_pc_01c7e4')
    e.ins('move.w','0xf68a:w,%d1',4)
    e.label('gameplay_pc_01c7e8')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('gameplay_pc_01c7ea')
    e.ins('move.l','(%a0, %d1.w),%d2',4)
    e.label('gameplay_pc_01c7ee')
    e.ins('mulu.w','%d2,%d0',2)
    e.label('gameplay_pc_01c7f0')
    e.ins('divu.w','#0x64,%d0',4)
    e.label('gameplay_pc_01c7f4')
    e.ins('sub.w','%d0,%d2',2)
    e.label('gameplay_pc_01c7f6')
    e.ins('move.w','%d2,0x2(%a0, %d1.w)',4)
    e.label('gameplay_pc_01c7fa')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01c800')
    e.ins('mulu.w','#0x1f5,%d0',4)
    e.label('gameplay_pc_01c804')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_01c806')
    e.ins('addi.w','#0x1f4,%d0',4)
    e.label('gameplay_pc_01c80a')
    e.ins('lea.l','0xdffc:w,%a0',4)
    e.label('gameplay_pc_01c80e')
    e.ins('move.w','0xf68a:w,%d1',4)
    e.label('gameplay_pc_01c812')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('gameplay_pc_01c814')
    e.ins('move.l','(%a0, %d1.w),%d2',4)
    e.label('gameplay_pc_01c818')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_01c81e')
    e.ins('sub.w','%d0,%d2',2)
    e.label('gameplay_pc_01c820')
    e.ins('bcc.w','gameplay_pc_01c826',4)
    e.label('gameplay_pc_01c824')
    e.ins('moveq','#0,%d2',2)
    e.label('gameplay_pc_01c826')
    e.ins('move.l','%d2,(%a0, %d1.w)',4)
    e.label('gameplay_pc_01c82a')
    e.ins('rts','',2)

def _lower_consolidate_city_after_battle(e,rules):
    e.label('gameplay_pc_01cb96')
    e.ins('bsr.w','gameplay_pc_01c2c8',4)
    e.label('gameplay_pc_01cb9a')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('gameplay_pc_01cb9e')
    e.ins('lea.l','0xd300:w,%a1',4)
    e.label('gameplay_pc_01cba2')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01cba6')
    e.ins('move.w','(%a1)+,%d1',2)
    e.label('gameplay_pc_01cba8')
    e.ins('bmi.w','gameplay_pc_01cbb2',4)
    e.label('gameplay_pc_01cbac')
    e.ins('move.b','%d0,(%a0, %d1.w)',4)
    e.label('gameplay_pc_01cbb0')
    e.ins('bra.b','gameplay_pc_01cba6',2)
    e.label('gameplay_pc_01cbb2')
    e.ins('lea.l','0xf427:w,%a0',4)
    e.label('gameplay_pc_01cbb6')
    e.ins('move.b','0xf68d:w,(%a0, %d0.w)',6)
    e.label('gameplay_pc_01cbbc')
    e.ins('lea.l','0xdffc:w,%a0',4)
    e.label('gameplay_pc_01cbc0')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01cbc4')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_01cbc6')
    e.ins('move.l','(%a0, %d0.w),%d1',4)
    e.label('gameplay_pc_01cbca')
    e.ins('lea.l','0xed88:w,%a1',4)
    e.label('gameplay_pc_01cbce')
    e.ins('add.l','(%a1, %d0.w),%d1',4)
    e.label('gameplay_pc_01cbd2')
    e.ins('cmpi.l','#0xf423f,%d1',6)
    e.label('gameplay_pc_01cbd8')
    e.ins('bls.w','gameplay_pc_01cbe2',4)
    e.label('gameplay_pc_01cbdc')
    e.ins('move.l','#0xf423f,%d1',6)
    e.label('gameplay_pc_01cbe2')
    e.ins('move.l','%d1,(%a0, %d0.w)',4)
    e.label('gameplay_pc_01cbe6')
    e.ins('lea.l','0xe09c:w,%a0',4)
    e.label('gameplay_pc_01cbea')
    e.ins('move.l','(%a0, %d0.w),%d1',4)
    e.label('gameplay_pc_01cbee')
    e.ins('lea.l','0xee24:w,%a1',4)
    e.label('gameplay_pc_01cbf2')
    e.ins('add.l','(%a1, %d0.w),%d1',4)
    e.label('gameplay_pc_01cbf6')
    e.ins('cmpi.l','#0xf423f,%d1',6)
    e.label('gameplay_pc_01cbfc')
    e.ins('bls.w','gameplay_pc_01cc06',4)
    e.label('gameplay_pc_01cc00')
    e.ins('move.l','#0xf423f,%d1',6)
    e.label('gameplay_pc_01cc06')
    e.ins('move.l','%d1,(%a1, %d0.w)',4)
    e.label('gameplay_pc_01cc0a')
    e.ins('move.w','#0xffff,0xf630:w',6)
    e.label('gameplay_pc_01cc10')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01cc14')
    e.ins('jsr','gameplay_pc_005f48:l',6)
    e.label('gameplay_pc_01cc1a')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01cc1e')
    e.ins('jsr','gameplay_pc_00e1f6:l',6)
    e.label('gameplay_pc_01cc24')
    e.ins('rts','',2)

def _lower_clear_city_officer_links(e,rules):
    e.label('gameplay_pc_01cc76')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01cc7a')
    e.ins('lea.l','0xa050:w,%a0',4)
    e.label('gameplay_pc_01cc7e')
    e.ins('move.w','#0xff,%d1',4)
    e.label('gameplay_pc_01cc82')
    e.ins('cmp.b','(%a0, %d1.w),%d0',4)
    e.label('gameplay_pc_01cc86')
    e.ins('bne.w','gameplay_pc_01cc8e',4)
    e.label('gameplay_pc_01cc8a')
    e.ins('clr.b','(%a0, %d1.w)',4)
    e.label('gameplay_pc_01cc8e')
    e.ins('dbra','%d1,gameplay_pc_01cc82',4)
    e.label('gameplay_pc_01cc92')
    e.ins('rts','',2)

def _lower_reassign_city_flagged_officers(e,rules):
    e.label('gameplay_pc_01cc94')
    e.ins('move.w','0xf68e:w,%d0',4)
    e.label('gameplay_pc_01cc98')
    e.ins('addi.w','#0x29,%d0',4)
    e.label('gameplay_pc_01cc9c')
    e.ins('move.w','0xf68a:w,%d1',4)
    e.label('gameplay_pc_01cca0')
    e.ins('bset.l','#0x6,%d1',4)
    e.label('gameplay_pc_01cca4')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('gameplay_pc_01cca8')
    e.ins('move.w','#0xff,%d2',4)
    e.label('gameplay_pc_01ccac')
    e.ins('cmp.b','(%a0, %d2.w),%d1',4)
    e.label('gameplay_pc_01ccb0')
    e.ins('bne.w','gameplay_pc_01ccb8',4)
    e.label('gameplay_pc_01ccb4')
    e.ins('move.b','%d0,(%a0, %d2.w)',4)
    e.label('gameplay_pc_01ccb8')
    e.ins('dbra','%d2,gameplay_pc_01ccac',4)
    e.label('gameplay_pc_01ccbc')
    e.ins('rts','',2)

def _lower_rebuild_city_links_from_primary_roster(e,rules):
    e.label('gameplay_pc_01d542')
    e.ins('lea.l','0xa050:w,%a0',4)
    e.label('gameplay_pc_01d546')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01d54a')
    e.ins('move.w','#0xff,%d1',4)
    e.label('gameplay_pc_01d54e')
    e.ins('move.b','(%a0, %d1.w),%d2',4)
    e.label('gameplay_pc_01d552')
    e.ins('andi.w','#0x3f,%d2',4)
    e.label('gameplay_pc_01d556')
    e.ins('cmp.w','%d0,%d2',2)
    e.label('gameplay_pc_01d558')
    e.ins('bne.w','gameplay_pc_01d560',4)
    e.label('gameplay_pc_01d55c')
    e.ins('clr.b','(%a0, %d1.w)',4)
    e.label('gameplay_pc_01d560')
    e.ins('dbra','%d1,gameplay_pc_01d54e',4)
    e.label('gameplay_pc_01d564')
    e.ins('lea.l','0xa550:w,%a1',4)
    e.label('gameplay_pc_01d568')
    e.ins('move.w','(%a1)+,%d2',2)
    e.label('gameplay_pc_01d56a')
    e.ins('bmi.w','gameplay_pc_01d578',4)
    e.label('gameplay_pc_01d56e')
    e.ins('andi.w','#0xff,%d2',4)
    e.label('gameplay_pc_01d572')
    e.ins('move.b','%d0,(%a0, %d2.w)',4)
    e.label('gameplay_pc_01d576')
    e.ins('bra.b','gameplay_pc_01d568',2)
    e.label('gameplay_pc_01d578')
    e.ins('rts','',2)

def _lower_classify_duel_object_result(e,rules):
    e.label('gameplay_pc_01d598')
    e.ins('lea.l','0xff7050:l,%a0',6)
    e.label('gameplay_pc_01d59e')
    e.ins('lea.l','0xff70a0:l,%a1',6)
    e.label('gameplay_pc_01d5a4')
    e.ins('move.b','0xff70f0:l,%d0',6)
    e.label('gameplay_pc_01d5aa')
    e.ins('move.b','0xff70f1:l,%d1',6)
    e.label('gameplay_pc_01d5b0')
    e.ins('move.w','0xffff80e0:l,%d2',6)
    e.label('gameplay_pc_01d5b6')
    e.ins('cmp.w','0x1a(%a0),%d2',4)
    e.label('gameplay_pc_01d5ba')
    e.ins('beq.w','gameplay_pc_01d5c2',4)
    e.label('gameplay_pc_01d5be')
    e.ins('exg','%a0,%a1',2)
    e.label('gameplay_pc_01d5c0')
    e.ins('exg','%d0,%d1',2)
    e.label('gameplay_pc_01d5c2')
    e.ins('tst.w','0x1c(%a0)',4)
    e.label('gameplay_pc_01d5c6')
    e.ins('beq.w','gameplay_pc_01d5fa',4)
    e.label('gameplay_pc_01d5ca')
    e.ins('tst.w','0x1c(%a1)',4)
    e.label('gameplay_pc_01d5ce')
    e.ins('beq.w','gameplay_pc_01d606',4)
    e.label('gameplay_pc_01d5d2')
    e.ins('cmpi.b','#0x1,%d0',4)
    e.label('gameplay_pc_01d5d6')
    e.ins('beq.w','gameplay_pc_01d612',4)
    e.label('gameplay_pc_01d5da')
    e.ins('cmpi.b','#0x1,%d1',4)
    e.label('gameplay_pc_01d5de')
    e.ins('beq.w','gameplay_pc_01d61e',4)
    e.label('gameplay_pc_01d5e2')
    e.ins('tst.b','%d0',2)
    e.label('gameplay_pc_01d5e4')
    e.ins('bne.w','gameplay_pc_01d62a',4)
    e.label('gameplay_pc_01d5e8')
    e.ins('tst.b','%d1',2)
    e.label('gameplay_pc_01d5ea')
    e.ins('beq.w','gameplay_pc_01d632',4)
    e.label('gameplay_pc_01d5ee')
    e.ins('move.w','#0x7,0xffff8114:l',8)
    e.label('gameplay_pc_01d5f6')
    e.ins('bra.w','gameplay_pc_01d632',4)
    e.label('gameplay_pc_01d5fa')
    e.ins('move.w','#0x3,0xffff8114:l',8)
    e.label('gameplay_pc_01d602')
    e.ins('bra.w','gameplay_pc_01d632',4)
    e.label('gameplay_pc_01d606')
    e.ins('move.w','#0x2,0xffff8114:l',8)
    e.label('gameplay_pc_01d60e')
    e.ins('bra.w','gameplay_pc_01d632',4)
    e.label('gameplay_pc_01d612')
    e.ins('move.w','#0x4,0xffff8114:l',8)
    e.label('gameplay_pc_01d61a')
    e.ins('bra.w','gameplay_pc_01d632',4)
    e.label('gameplay_pc_01d61e')
    e.ins('move.w','#0x5,0xffff8114:l',8)
    e.label('gameplay_pc_01d626')
    e.ins('bra.w','gameplay_pc_01d632',4)
    e.label('gameplay_pc_01d62a')
    e.ins('move.w','#0x6,0xffff8114:l',8)
    e.label('gameplay_pc_01d632')
    e.ins('rts','',2)

def _lower_city_reserve_forces_duel_carry(e,rules):
    e.label('gameplay_pc_01e422')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_01e428')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_01e42c')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_01e42e')
    e.ins('lea.l','0xe59c:w,%a0',4)
    e.label('gameplay_pc_01e432')
    e.ins('move.w','0x2(%a0, %d0.w),%d0',4)
    e.label('gameplay_pc_01e436')
    e.ins('cmpi.w','#0x1e,%d0',4)
    e.label('gameplay_pc_01e43a')
    e.ins('bcc.b','gameplay_pc_01e45e',2)
    e.label('gameplay_pc_01e43c')
    e.ins('moveq','#0,%d1',2)
    e.label('gameplay_pc_01e43e')
    e.ins('move.w','0xf61c:w,%d1',4)
    e.label('gameplay_pc_01e442')
    e.ins('move.l','%d1,%d2',2)
    e.label('gameplay_pc_01e444')
    e.ins('lsl.l','#0x1,%d1',2)
    e.label('gameplay_pc_01e446')
    e.ins('add.l','%d2,%d1',2)
    e.label('gameplay_pc_01e448')
    e.ins('lsl.l','#0x3,%d1',2)
    e.label('gameplay_pc_01e44a')
    e.ins('add.l','%d2,%d1',2)
    e.label('gameplay_pc_01e44c')
    e.ins('lsl.l','#0x2,%d1',2)
    e.label('gameplay_pc_01e44e')
    e.ins('swap','%d1',2)
    e.label('gameplay_pc_01e450')
    e.ins('cmp.w','%d0,%d1',2)
    e.label('gameplay_pc_01e452')
    e.ins('bcs.w','gameplay_pc_01e45e',4)
    e.label('gameplay_pc_01e456')
    e.ins('ori.w','#0x1,%sr',4)
    e.label('gameplay_pc_01e45a')
    e.ins('bra.w','gameplay_pc_01e462',4)
    e.label('gameplay_pc_01e45e')
    e.ins('andi.w','#0xfffe,%sr',4)
    e.label('gameplay_pc_01e462')
    e.ins('rts','',2)

def _lower_find_nearest_secondary_terrain_target(e,rules):
    e.label('gameplay_pc_01e464')
    e.ins('jsr','gameplay_pc_01a438:l',6)
    e.label('gameplay_pc_01e46a')
    e.ins('lea.l','0xa5a4:w,%a1',4)
    e.label('gameplay_pc_01e46e')
    e.ins('lea.l','0xa150:w,%a2',4)
    e.label('gameplay_pc_01e472')
    e.ins('move.w','0xf3f2:w,%d0',4)
    e.label('gameplay_pc_01e476')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_01e478')
    e.ins('move.w','(%a2, %d0.w),%d3',4)
    e.label('gameplay_pc_01e47c')
    e.ins('lsr.w','#0x7,%d3',2)
    e.label('gameplay_pc_01e47e')
    e.ins('move.w','0x2(%a2, %d0.w),%d4',4)
    e.label('gameplay_pc_01e482')
    e.ins('lsr.w','#0x7,%d4',2)
    e.label('gameplay_pc_01e484')
    e.ins('move.w','#0xffff,%d5',4)
    e.label('gameplay_pc_01e488')
    e.ins('move.w','#0x8000,%d6',4)
    e.label('gameplay_pc_01e48c')
    e.ins('move.w','(%a1)+,%d7',2)
    e.label('gameplay_pc_01e48e')
    e.ins('bmi.w','gameplay_pc_01e4e0',4)
    e.label('gameplay_pc_01e492')
    e.ins('andi.w','#0xff,%d7',4)
    e.label('gameplay_pc_01e496')
    e.ins('lsl.w','#0x2,%d7',2)
    e.label('gameplay_pc_01e498')
    e.ins('move.w','(%a2, %d7.w),%d1',4)
    e.label('gameplay_pc_01e49c')
    e.ins('lsr.w','#0x7,%d1',2)
    e.label('gameplay_pc_01e49e')
    e.ins('move.w','0x2(%a2, %d7.w),%d2',4)
    e.label('gameplay_pc_01e4a2')
    e.ins('lsr.w','#0x7,%d2',2)
    e.label('gameplay_pc_01e4a4')
    e.ins('jsr','gameplay_pc_01a44e:l',6)
    e.label('gameplay_pc_01e4aa')
    e.ins('cmpi.b','#0x6,%d0',4)
    e.label('gameplay_pc_01e4ae')
    e.ins('bne.b','gameplay_pc_01e48c',2)
    e.label('gameplay_pc_01e4b0')
    e.ins('sub.w','%d3,%d1',2)
    e.label('gameplay_pc_01e4b2')
    e.ins('bcc.b','gameplay_pc_01e4b6',2)
    e.label('gameplay_pc_01e4b4')
    e.ins('neg.w','%d1',2)
    e.label('gameplay_pc_01e4b6')
    e.ins('mulu.w','%d1,%d1',2)
    e.label('gameplay_pc_01e4b8')
    e.ins('sub.w','%d4,%d2',2)
    e.label('gameplay_pc_01e4ba')
    e.ins('bcc.b','gameplay_pc_01e4be',2)
    e.label('gameplay_pc_01e4bc')
    e.ins('neg.w','%d2',2)
    e.label('gameplay_pc_01e4be')
    e.ins('mulu.w','%d2,%d2',2)
    e.label('gameplay_pc_01e4c0')
    e.ins('move.l','%d1,%d0',2)
    e.label('gameplay_pc_01e4c2')
    e.ins('add.l','%d2,%d0',2)
    e.label('gameplay_pc_01e4c4')
    e.ins('jsr','gameplay_pc_03080e:l',6)
    e.label('gameplay_pc_01e4ca')
    e.ins('cmp.w','%d5,%d0',2)
    e.label('gameplay_pc_01e4cc')
    e.ins('bcs.b','gameplay_pc_01e4d8',2)
    e.label('gameplay_pc_01e4ce')
    e.ins('bne.b','gameplay_pc_01e48c',2)
    e.label('gameplay_pc_01e4d0')
    e.ins('btst.b','#0x0,0xf321:w',6)
    e.label('gameplay_pc_01e4d6')
    e.ins('bne.b','gameplay_pc_01e48c',2)
    e.label('gameplay_pc_01e4d8')
    e.ins('move.w','%d0,%d5',2)
    e.label('gameplay_pc_01e4da')
    e.ins('lsr.w','#0x2,%d7',2)
    e.label('gameplay_pc_01e4dc')
    e.ins('move.w','%d7,%d6',2)
    e.label('gameplay_pc_01e4de')
    e.ins('bra.b','gameplay_pc_01e48c',2)
    e.label('gameplay_pc_01e4e0')
    e.ins('rts','',2)

def _lower_apply_postbattle_city_economic_attrition(e,rules):
    e.label('gameplay_pc_0217c8')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_0217ce')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_0217d4')
    e.ins('lsl.l','#0x4,%d0',2)
    e.label('gameplay_pc_0217d6')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_0217d8')
    e.ins('addi.w','#0x5,%d0',4)
    e.label('gameplay_pc_0217dc')
    e.ins('move.w','0xf68a:w,%d2',4)
    e.label('gameplay_pc_0217e0')
    e.ins('lsl.w','#0x2,%d2',2)
    e.label('gameplay_pc_0217e2')
    e.ins('lea.l','0xe1dc:w,%a0',4)
    e.label('gameplay_pc_0217e6')
    e.ins('move.l','(%a0, %d2.w),%d3',4)
    e.label('gameplay_pc_0217ea')
    e.ins('move.l','%d3,%d4',2)
    e.label('gameplay_pc_0217ec')
    e.ins('mulu.w','%d0,%d4',2)
    e.label('gameplay_pc_0217ee')
    e.ins('divu.w','#0x64,%d4',4)
    e.label('gameplay_pc_0217f2')
    e.ins('sub.w','%d4,%d3',2)
    e.label('gameplay_pc_0217f4')
    e.ins('move.l','%d3,(%a0, %d2.w)',4)
    e.label('gameplay_pc_0217f8')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_0217fe')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_021804')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_021806')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('gameplay_pc_021808')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_02180a')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_02180c')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_02180e')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_021810')
    e.ins('lea.l','0xe13c:w,%a0',4)
    e.label('gameplay_pc_021814')
    e.ins('move.l','(%a0, %d2.w),%d3',4)
    e.label('gameplay_pc_021818')
    e.ins('move.l','%d3,%d4',2)
    e.label('gameplay_pc_02181a')
    e.ins('mulu.w','%d0,%d4',2)
    e.label('gameplay_pc_02181c')
    e.ins('divu.w','#0x64,%d4',4)
    e.label('gameplay_pc_021820')
    e.ins('sub.w','%d4,%d3',2)
    e.label('gameplay_pc_021822')
    e.ins('move.l','%d3,(%a0, %d2.w)',4)
    e.label('gameplay_pc_021826')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_02182c')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('gameplay_pc_021832')
    e.ins('move.l','%d0,%d1',2)
    e.label('gameplay_pc_021834')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_021836')
    e.ins('add.l','%d1,%d0',2)
    e.label('gameplay_pc_021838')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('gameplay_pc_02183a')
    e.ins('swap','%d0',2)
    e.label('gameplay_pc_02183c')
    e.ins('addq.w','#0x5,%d0',2)
    e.label('gameplay_pc_02183e')
    e.ins('lea.l','0xe31c:w,%a0',4)
    e.label('gameplay_pc_021842')
    e.ins('move.w','0x2(%a0, %d2.w),%d3',4)
    e.label('gameplay_pc_021846')
    e.ins('sub.w','%d0,%d3',2)
    e.label('gameplay_pc_021848')
    e.ins('bcc.w','gameplay_pc_02184e',4)
    e.label('gameplay_pc_02184c')
    e.ins('clr.w','%d3',2)
    e.label('gameplay_pc_02184e')
    e.ins('move.w','%d3,0x2(%a0, %d2.w)',4)
    e.label('gameplay_pc_021852')
    e.ins('rts','',2)

def _lower_trigger_battle_for_city_rectangle(e,rules):
    e.label('gameplay_pc_023736')
    e.ins('lea.l','0xff3cc2:l,%a0',6)
    e.label('gameplay_pc_02373c')
    e.ins('tst.b','(%a0, %d7.w)',4)
    e.label('gameplay_pc_023740')
    e.ins('bne.w','gameplay_pc_0238a8',4)
    e.label('gameplay_pc_023744')
    e.ins('lea.l','0xff3dc2:l,%a1',6)
    e.label('gameplay_pc_02374a')
    e.ins('tst.b','(%a1, %d7.w)',4)
    e.label('gameplay_pc_02374e')
    e.ins('bne.w','gameplay_pc_0238a8',4)
    e.label('gameplay_pc_023752')
    e.ins('lea.l','0xae1b2:l,%a0',6)
    e.label('gameplay_pc_023758')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_02375c')
    e.ins('lsl.w','#0x3,%d0',2)
    e.label('gameplay_pc_02375e')
    e.ins('move.w','(%a0, %d0.w),%d1',4)
    e.label('gameplay_pc_023762')
    e.ins('move.w','0x2(%a0, %d0.w),%d2',4)
    e.label('gameplay_pc_023766')
    e.ins('move.w','0x4(%a0, %d0.w),%d3',4)
    e.label('gameplay_pc_02376a')
    e.ins('move.w','0x6(%a0, %d0.w),%d4',4)
    e.label('gameplay_pc_02376e')
    e.ins('lea.l','0xa150:w,%a0',4)
    e.label('gameplay_pc_023772')
    e.ins('move.w','%d7,%d0',2)
    e.label('gameplay_pc_023774')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_023776')
    e.ins('cmp.w','(%a0, %d0.w),%d1',4)
    e.label('gameplay_pc_02377a')
    e.ins('bhi.w','gameplay_pc_0238a8',4)
    e.label('gameplay_pc_02377e')
    e.ins('cmp.w','(%a0, %d0.w),%d2',4)
    e.label('gameplay_pc_023782')
    e.ins('bcs.w','gameplay_pc_0238a8',4)
    e.label('gameplay_pc_023786')
    e.ins('cmp.w','0x2(%a0, %d0.w),%d3',4)
    e.label('gameplay_pc_02378a')
    e.ins('bhi.w','gameplay_pc_0238a8',4)
    e.label('gameplay_pc_02378e')
    e.ins('cmp.w','0x2(%a0, %d0.w),%d4',4)
    e.label('gameplay_pc_023792')
    e.ins('bcs.w','gameplay_pc_0238a8',4)
    e.label('gameplay_pc_023796')
    e.ins('move.w','%d7,0xf3f2:w',4)
    e.label('gameplay_pc_02379a')
    e.ins('bsr.w','gameplay_pc_01e464',4)
    e.label('gameplay_pc_02379e')
    e.ins('move.w','%d7,-(%a7)',2)
    e.label('gameplay_pc_0237a0')
    e.ins('move.w','%d6,0xf3a6:w',4)
    e.label('gameplay_pc_0237a4')
    e.ins('bmi.w','gameplay_pc_0237b2',4)
    e.label('gameplay_pc_0237a8')
    e.ins('jsr','gameplay_pc_01e422:l',6)
    e.label('gameplay_pc_0237ae')
    e.ins('bcs.w','gameplay_pc_023806',4)
    e.label('gameplay_pc_0237b2')
    e.ins('move.w','#0x12f,0xf740:w',6)
    e.label('gameplay_pc_0237b8')
    e.ins('bchg.b','#0x1,0xf6d7:w',6)
    e.label('gameplay_pc_0237be')
    e.ins('jsr','gameplay_pc_0260e4:l',6)
    e.label('gameplay_pc_0237c4')
    e.ins('bchg.b','#0x1,0xf6d7:w',6)
    e.label('gameplay_pc_0237ca')
    e.ins('jsr','gameplay_pc_0183f8:l',6)
    e.label('gameplay_pc_0237d0')
    e.ins('cmpi.w','#0x411,0xf612:w',6)
    e.label('gameplay_pc_0237d6')
    e.ins('beq.w','gameplay_pc_02389e',4)
    e.label('gameplay_pc_0237da')
    e.ins('move.w','0xf68a:w,%d0',4)
    e.label('gameplay_pc_0237de')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('gameplay_pc_0237e0')
    e.ins('lea.l','0xe59c:w,%a0',4)
    e.label('gameplay_pc_0237e4')
    e.ins('move.l','(%a0, %d0.w),0xf3c8:w',6)
    e.label('gameplay_pc_0237ea')
    e.ins('move.w','#0x113,0xf740:w',6)
    e.label('gameplay_pc_0237f0')
    e.ins('bchg.b','#0x1,0xf6d7:w',6)
    e.label('gameplay_pc_0237f6')
    e.ins('jsr','gameplay_pc_0260e4:l',6)
    e.label('gameplay_pc_0237fc')
    e.ins('bchg.b','#0x1,0xf6d7:w',6)
    e.label('gameplay_pc_023802')
    e.ins('bra.w','gameplay_pc_02389e',4)
    e.label('gameplay_pc_023806')
    e.ins('move.w','0xf3f2:w,0xf3d0:w',6)
    e.label('gameplay_pc_02380c')
    e.ins('move.w','0xf3a6:w,0xf3d2:w',6)
    e.label('gameplay_pc_023812')
    e.ins('move.w','#0x114,0xf740:w',6)
    e.label('gameplay_pc_023818')
    e.ins('bchg.b','#0x1,0xf6d7:w',6)
    e.label('gameplay_pc_02381e')
    e.ins('jsr','gameplay_pc_0260e4:l',6)
    e.label('gameplay_pc_023824')
    e.ins('bchg.b','#0x1,0xf6d7:w',6)
    e.label('gameplay_pc_02382a')
    e.ins('move.w','0xf3f2:w,0xf702:w',6)
    e.label('gameplay_pc_023830')
    e.ins('move.w','0xf3a6:w,0xf706:w',6)
    e.label('gameplay_pc_023836')
    e.ins('move.w','0xf612:w,-(%a7)',4)
    e.label('gameplay_pc_02383a')
    e.ins('move.w','0xf362:w,-(%a7)',4)
    e.label('gameplay_pc_02383e')
    e.ins('move.w','#0x2,0xf772:w',6)
    e.label('gameplay_pc_023844')
    e.ins('move.w','#0x407,0xf612:w',6)
    e.label('gameplay_pc_02384a')
    e.ins('move.w','#0x3,0xf362:w',6)
    e.label('gameplay_pc_023850')
    e.ins('clr.w','0xf352:w',4)
    e.label('gameplay_pc_023854')
    e.ins('move.w','#0x2500,%sr',4)
    e.label('gameplay_pc_023858')
    e.ins('cmpi.w','#0xc4,0xf600:w',6)
    e.label('gameplay_pc_02385e')
    e.ins('bne.b','gameplay_pc_023858',2)
    e.label('gameplay_pc_023860')
    e.ins('move.w','#0x2700,%sr',4)
    e.label('gameplay_pc_023864')
    e.ins('jsr','gameplay_pc_000dc0:l',6)
    e.label('gameplay_pc_02386a')
    e.ins('move.w','#0x2500,%sr',4)
    e.label('gameplay_pc_02386e')
    e.ins('cmpi.w','#0x84,0xf600:w',6)
    e.label('gameplay_pc_023874')
    e.ins('bne.b','gameplay_pc_02386e',2)
    e.label('gameplay_pc_023876')
    e.ins('jsr','gameplay_pc_017602:l',6)
    e.label('gameplay_pc_02387c')
    e.ins('move.w','#0x2500,%sr',4)
    e.label('gameplay_pc_023880')
    e.ins('cmpi.w','#0x408,0xf612:w',6)
    e.label('gameplay_pc_023886')
    e.ins('beq.w','gameplay_pc_023892',4)
    e.label('gameplay_pc_02388a')
    e.ins('cmpi.w','#0x411,0xf612:w',6)
    e.label('gameplay_pc_023890')
    e.ins('bne.b','gameplay_pc_023880',2)
    e.label('gameplay_pc_023892')
    e.ins('move.w','#0x2700,%sr',4)
    e.label('gameplay_pc_023896')
    e.ins('move.w','(%a7)+,0xf362:w',4)
    e.label('gameplay_pc_02389a')
    e.ins('move.w','(%a7)+,0xf612:w',4)
    e.label('gameplay_pc_02389e')
    e.ins('move.w','(%a7)+,%d7',2)
    e.label('gameplay_pc_0238a0')
    e.ins('ori.w','#0x1,%sr',4)
    e.label('gameplay_pc_0238a4')
    e.ins('bra.w','gameplay_pc_0238ac',4)
    e.label('gameplay_pc_0238a8')
    e.ins('andi.w','#0xfffe,%sr',4)
    e.label('gameplay_pc_0238ac')
    e.ins('rts','',2)

def _lower_present_battle_message(e,rules):
    e.label('gameplay_pc_0260e4')
    e.ins('move.w','0xf612:w,-(%a7)',4)
    e.label('gameplay_pc_0260e8')
    e.ins('move.w','0xf362:w,-(%a7)',4)
    e.label('gameplay_pc_0260ec')
    e.ins('move.w','#0x414,0xf612:w',6)
    e.label('gameplay_pc_0260f2')
    e.ins('clr.w','0xf362:w',4)
    e.label('gameplay_pc_0260f6')
    e.ins('clr.w','0xf600:w',4)
    e.label('gameplay_pc_0260fa')
    e.ins('move.w','#0x2500,%sr',4)
    e.label('gameplay_pc_0260fe')
    e.ins('tst.w','0xf600:w',4)
    e.label('gameplay_pc_026102')
    e.ins('beq.b','gameplay_pc_0260fe',2)
    e.label('gameplay_pc_026104')
    e.ins('cmpi.w','#0x28,0xf600:w',6)
    e.label('gameplay_pc_02610a')
    e.ins('bne.w','gameplay_pc_02611e',4)
    e.label('gameplay_pc_02610e')
    e.ins('jsr','gameplay_pc_00060c:l',6)
    e.label('gameplay_pc_026114')
    e.ins('clr.w','0xf600:w',4)
    e.label('gameplay_pc_026118')
    e.ins('move.w','#0x2500,%sr',4)
    e.label('gameplay_pc_02611c')
    e.ins('bra.b','gameplay_pc_0260fe',2)
    e.label('gameplay_pc_02611e')
    e.ins('move.w','#0x2700,%sr',4)
    e.label('gameplay_pc_026122')
    e.ins('move.w','(%a7)+,0xf362:w',4)
    e.label('gameplay_pc_026126')
    e.ins('move.w','(%a7)+,0xf612:w',4)
    e.label('gameplay_pc_02612a')
    e.ins('rts','',2)

LOWERERS = {
    'run_battle_scene_round':_lower_run_battle_scene_round,
    'initialize_battle_scene':_lower_initialize_battle_scene,
    'compact_active_packed_group_queue':_lower_compact_active_packed_group_queue,
    'remove_queued_packed_group_member':_lower_remove_queued_packed_group_member,
    'upload_battle_background_planes':_lower_upload_battle_background_planes,
    'upload_battlefield_tilemap':_lower_upload_battlefield_tilemap,
    'upload_battle_scene_labels':_lower_upload_battle_scene_labels,
    'cache_battle_roster_totals':_lower_cache_battle_roster_totals,
    'append_force_head_glyphs':_lower_append_force_head_glyphs,
    'integrate_selected_officer_into_packed_group':_lower_integrate_selected_officer_into_packed_group,
    'reserve_packed_group_member_byte':_lower_reserve_packed_group_member_byte,
    'split_city_resources_into_group':_lower_split_city_resources_into_group,
    'refresh_packed_group_average':_lower_refresh_packed_group_average,
    'copy_selected_city_group_parameter':_lower_copy_selected_city_group_parameter,
    'group_matches_city_head_carry':_lower_group_matches_city_head_carry,
    'append_survivors_to_packed_group':_lower_append_survivors_to_packed_group,
    'add_staged_resources_to_packed_group':_lower_add_staged_resources_to_packed_group,
    'assign_city_survivor_roster_tokens':_lower_assign_city_survivor_roster_tokens,
    'merge_city_survivor_rosters':_lower_merge_city_survivor_rosters,
    'resolve_city_battle_damage':_lower_resolve_city_battle_damage,
    'award_city_reserve_attrition':_lower_award_city_reserve_attrition,
    'secondary_roster_has_terrain_six_carry':_lower_secondary_roster_has_terrain_six_carry,
    'sample_battle_special_status_factor':_lower_sample_battle_special_status_factor,
    'collect_battle_special_status_members':_lower_collect_battle_special_status_members,
    'compute_battle_damage_potential':_lower_compute_battle_damage_potential,
    'settle_city_battle_outcome':_lower_settle_city_battle_outcome,
    'sample_city_postbattle_reserve':_lower_sample_city_postbattle_reserve,
    'distribute_city_battle_progress':_lower_distribute_city_battle_progress,
    'apply_assigned_city_light_attrition':_lower_apply_assigned_city_light_attrition,
    'consume_city_battle_supply_long':_lower_consume_city_battle_supply_long,
    'reduce_city_reserve_after_defeat':_lower_reduce_city_reserve_after_defeat,
    'consume_city_battle_supply_word':_lower_consume_city_battle_supply_word,
    'consolidate_city_after_battle':_lower_consolidate_city_after_battle,
    'clear_city_officer_links':_lower_clear_city_officer_links,
    'reassign_city_flagged_officers':_lower_reassign_city_flagged_officers,
    'rebuild_city_links_from_primary_roster':_lower_rebuild_city_links_from_primary_roster,
    'classify_duel_object_result':_lower_classify_duel_object_result,
    'city_reserve_forces_duel_carry':_lower_city_reserve_forces_duel_carry,
    'find_nearest_secondary_terrain_target':_lower_find_nearest_secondary_terrain_target,
    'apply_postbattle_city_economic_attrition':_lower_apply_postbattle_city_economic_attrition,
    'trigger_battle_for_city_rectangle':_lower_trigger_battle_for_city_rectangle,
    'present_battle_message':_lower_present_battle_message,
}

def compile_battle(source):
    records=semantic_functions(source,DECLARATIONS,APPROVED)
    for owner in ('sample_battle_special_status_factor', 'collect_battle_special_status_members', 'compute_battle_damage_potential'):
        records[owner]['effects'] += '\nsole presentation subcores: ' + '\n'.join(records[name]['effects'] for name in ('_presentation_call_fields', '_presentation_collect_first_fields', '_presentation_collect_second_fields', '_presentation_frame', '_presentation_random_fields', '_presentation_sub_long_fields', 'collect_battle_special_status_members_fields', 'compute_battle_damage_potential_fields', 'sample_battle_special_status_factor_fields'))
    records['find_nearest_secondary_terrain_target']['effects'] += '\nsole target algorithm: ' + records['find_nearest_secondary_terrain_target_observations']['effects']
    records['find_nearest_secondary_terrain_target']['effects'] += '\nsole full nearest terrain fields: ' + '\n'.join(records[name]['effects'] for name in ('find_nearest_secondary_terrain_target_fields', '_nearest_terrain_radial_fields', '_city_outcome_frame_fields', '_presentation_call_fields', '_damage_map_fields', '_damage_terrain_fields', '_damage_add_long'))
    records['trigger_battle_for_city_rectangle']['effects'] += '\nsole trigger steps: ' + '\n'.join(records[name]['effects'] for name in ('_trigger_frame', '_trigger_conditions', '_trigger_compare', '_trigger_shift', '_trigger_retained_word', '_trigger_store', '_trigger_carry', '_trigger_push_word', '_trigger_pop_word', '_trigger_legacy_call', '_trigger_call', '_trigger_notification', '_trigger_wait', '_trigger_regular_damage', '_trigger_duel', 'trigger_battle_for_city_rectangle_fields'))
    for owner in ('resolve_city_battle_damage', 'award_city_reserve_attrition', 'secondary_roster_has_terrain_six_carry', 'trigger_battle_for_city_rectangle'):
        records[owner]['effects'] += '\nsole city damage fields: ' + '\n'.join(records[name]['effects'] for name in ('_damage_add_long', '_damage_apply_mutual_losses_fields', '_damage_bchg_side', '_damage_divide', '_damage_external_call', '_damage_map_fields', '_damage_potential_fields', '_damage_raise_ability_fields', '_damage_restore_longs', '_damage_save_longs', '_damage_shift_long', '_damage_store', '_damage_terrain_fields', '_damage_terrain_query_fields', '_damage_visible_owner', '_trigger_call', 'award_city_reserve_attrition_fields', 'resolve_city_battle_damage_fields', 'secondary_roster_has_terrain_six_fields'))
    records['_postbattle_fraction_fields']['effects'] += '\nshared closed shifts: ' + records['_postbattle_shift_long_fields']['effects']
    for owner in ('sample_city_postbattle_reserve', 'distribute_city_battle_progress', 'apply_assigned_city_light_attrition', 'consume_city_battle_supply_long', 'reduce_city_reserve_after_defeat', 'consume_city_battle_supply_word', 'clear_city_officer_links', 'reassign_city_flagged_officers', 'apply_postbattle_city_economic_attrition'):
        records[owner]['effects'] += '\nsole postbattle fields: ' + '\n'.join(records[name]['effects'] for name in ('_postbattle_candidates_fields', '_postbattle_city_resource_fields', '_postbattle_compare_byte_fields', '_postbattle_decrement_fields', '_postbattle_fraction_fields', '_postbattle_gold_debit_fields', '_postbattle_loss_fields', '_postbattle_memory_byte_fields', 'apply_assigned_city_light_attrition_fields', 'apply_postbattle_city_economic_attrition_fields', 'build_battlefield_outcome_candidates_fields', 'build_city_assigned_outcome_candidates_fields', 'clear_city_officer_links_fields', 'consume_city_battle_supply_long_fields', 'consume_city_battle_supply_word_fields', 'distribute_city_battle_progress_fields', 'reassign_city_flagged_officers_fields', 'reduce_city_reserve_after_defeat_fields', 'sample_city_postbattle_reserve_fields'))
    for owner in ('settle_city_battle_outcome_fields', 'distribute_city_battle_progress'):
        records[owner]['effects'] += '\nsole current city return/loss field cores: ' + '\n'.join(records[name]['effects'] for name in ('_city_outcome_child_fields', '_city_outcome_word_product_fields', '_postbattle_bit_fields', '_postbattle_byte_carrier_fields', '_postbattle_fraction_fields', '_postbattle_loss_roster_fields', '_postbattle_progress_tail_fields', '_postbattle_rebuild_rosters_fields', 'allocate_packed_group_resources_fields', 'apply_battlefield_heavy_losses_and_detach_fields', 'apply_battlefield_ratio_losses_fields', 'apply_city_assigned_heavy_losses_fields', 'distribute_battlefield_battle_progress_fields', 'distribute_city_battle_progress_fields', 'owner_has_other_city_carry_fields', 'partition_city_survivors_fields', 'rebuild_primary_after_battle_fields', 'rebuild_secondary_after_battle_fields', 'restore_returning_officer_assignments_fields', 'sort_returning_officer_status_fields'))
    for owner in ('consolidate_city_after_battle', 'settle_city_battle_outcome_fields'):
        records[owner]['effects'] += '\nsole consolidation/arrival/packet fields: ' + '\n'.join(records[name]['effects'] for name in ('_city_outcome_child_fields', 'append_group_from_survivor_roster_fields', 'build_roster_fields', 'choose_city_head_fields', 'choose_empty_neighbor_position_fields', 'consolidate_city_after_battle_fields', 'roster_contains_force_head_carry_fields'))
    records['city_reserve_forces_duel_carry']['effects'] += '\nsole actual duel gate fields: ' + records['city_reserve_forces_duel_carry_fields']['effects']
    sole_labels_fields = {name:records[name]['effects'] for name in ('_battle_labels_call_fields', '_battle_labels_upload_longs_fields', 'append_force_head_glyphs_fields', 'cache_battle_roster_totals_fields', 'upload_battle_scene_labels_fields')}
    for owner in ('upload_battle_scene_labels', 'append_force_head_glyphs', 'cache_battle_roster_totals'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_labels_fields=sole_labels_fields)
    for owner in ('settle_city_battle_outcome_fields', '_city_outcome_child_fields'):
        records[owner]['effects'] += '\nsole packed-member field core: ' + '\n'.join(records[name]['effects'] for name in ('_packed_compact_reference_fields', '_packed_relabel_active_fields', '_packed_restore_word_fields', '_packed_save_word_fields', '_packed_seek_reference_fields', '_packed_slide_tail_fields', 'attach_member_shift_packet_fields', 'detach_member_keep_group_cursor_fields', 'remove_defeated_packed_member_fields', 'remove_group_reference_fields', 'replace_group_head_reference_fields', 'replace_or_remove_group_references_fields', 'settle_battle_packed_armies_fields', 'transfer_outcome_officer_fields'))
    records['upload_battlefield_tilemap']['effects'] += '\nsole complete tilemap fields: ' + records['upload_battlefield_tilemap_fields']['effects']
    sole_battle_initialization_fields = {name:records[name]['effects'] for name in ('_battle_initialize_call_fields', 'compact_active_packed_group_queue_fields', 'initialize_battle_scene_fields', 'remove_queued_packed_group_member_fields', 'upload_battle_background_planes_fields')}
    for owner in ('initialize_battle_scene', 'compact_active_packed_group_queue', 'remove_queued_packed_group_member', 'upload_battle_background_planes'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_battle_initialization_fields=sole_battle_initialization_fields)
    sole_battle_round_fields = {name:records[name]['effects'] for name in ('_battle_scene_round_call_fields', 'run_battle_scene_round_fields')}
    for owner in ('run_battle_scene_round',):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_battle_round_fields=sole_battle_round_fields)
    return lower_declared({b.name:records[b.name] for b in BATTLE_BINDINGS},BATTLE_BINDINGS,LOWERERS)


# Complete sole 23736 core and original 1E464 terminating-word observation.
DECLARATIONS.update({'_trigger_frame': {'signature': 'memory, frame', 'returns': None, 'flow': "if type(memory) is not BattleTriggerMemory or type(frame) is not BattleTriggerFrame:\n    raise ValueError('sealed same-state trigger frame required')\nreturn frame.validate(memory.state)"}, '_trigger_conditions': {'signature': 'memory, frame, value, bits', 'returns': None, 'flow': 'uint(value, bits)\nstatus = frame.status & 65520 | (8 if value & 1 << bits - 1 else 0) | (4 if value == 0 else 0)\nmemory.state.sr = status\nreturn battle_replace(frame, status=status)'}, '_trigger_compare': {'signature': 'memory, frame, left, right', 'returns': None, 'flow': 'uint(left, 16)\nuint(right, 16)\nvalue = u16(left - right)\noverflow = (left ^ right) & (left ^ value) & 32768 != 0\nstatus = frame.status & 65520 | (8 if value & 32768 else 0) | (4 if value == 0 else 0) | (2 if overflow else 0) | (1 if left < right else 0)\nmemory.state.sr = status\nreturn battle_replace(frame, status=status)'}, '_trigger_shift': {'signature': 'memory, frame, value, amount', 'returns': None, 'flow': 'uint(value, 16)\nresult = u16(value << amount)\ncarry = bool(value & 1 << 16 - amount)\nstatus = frame.status & 65504 | (17 if carry else 0) | (8 if result & 32768 else 0) | (4 if result == 0 else 0)\nmemory.state.sr = status\nreturn (battle_replace(frame, status=status), result)'}, '_trigger_retained_word': {'signature': 'carrier, value', 'returns': None, 'flow': 'uint(value, 16)\nreturn None if carrier is None else replace_word(carrier, value)'}, '_trigger_store': {'signature': 'memory, frame, suffix, value, bits=16', 'returns': None, 'flow': "frame = _trigger_conditions(memory, frame, value, bits)\nif bits == 16:\n    memory.port(suffix).set_word(0, value)\nelif bits == 32:\n    memory.port(suffix).set_long(0, value)\nelse:\n    raise ValueError('actual trigger store width required')\nreturn frame"}, '_trigger_carry': {'signature': 'memory, frame, carry', 'returns': None, 'flow': "if type(carry) is not bool:\n    raise ValueError('actual carry branch required')\nstatus = frame.status & 65534 | int(carry)\nmemory.state.set_status_word(status)\nreturn battle_replace(frame, status=status)"}, '_trigger_push_word': {'signature': 'memory, frame, value', 'returns': None, 'flow': 'frame = _trigger_conditions(memory, frame, uint(value, 16), 16)\nif frame.stack_cursor is None:\n    return frame\nstack = frame.stack_cursor.advance(-2)\nstack.set_word(0, value)\nreturn battle_replace(frame, stack_cursor=stack)'}, '_trigger_pop_word': {'signature': 'memory, frame, legacy_value', 'returns': None, 'flow': 'if frame.stack_cursor is None:\n    value = uint(legacy_value, 16)\nelse:\n    value = frame.stack_cursor.word()\n    frame = battle_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\nreturn (_trigger_conditions(memory, frame, value, 16), value)'}, '_trigger_legacy_call': {'signature': 'memory, frame, target', 'returns': None, 'flow': "state, context = (memory.state, frame.legacy_context)\nselected, terminator = (None, None)\nif target == 124004:\n    result, terminator = find_nearest_secondary_terrain_target_observations(state)\n    selected = result.officer\n    frame = battle_replace(frame, offset_y=_trigger_retained_word(frame.offset_y, selected), choice=_trigger_retained_word(frame.choice, terminator))\nelif target == 123938:\n    city_reserve_forces_duel_carry(state)\nelif target == 155876:\n    present_battle_message(state)\nelif target == 99320:\n    resolve_city_battle_damage(state, context.damage_carrier)\nelif target == 3520:\n    run_battle_scene_round(state, context.scene)\nelif target == 95746:\n    initialize_battle_scene(state, context.scene)\nelse:\n    raise Boundary('unrecovered original legacy battle trigger call ' + str(target))\nreturn (battle_replace(frame, status=state.sr), selected, terminator)"}, '_trigger_call': {'signature': 'memory, frame, target, continuation', 'returns': None, 'flow': "frame = _trigger_frame(memory, frame)\nif not memory.complete:\n    return _trigger_legacy_call(memory, frame, target)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = battle_replace(frame, stack_cursor=stack)\nreturned = memory.state.service_at(target, entered)\nif type(returned) is not BattleTriggerFrame:\n    raise Boundary('real trigger child must return all observed full fields')\nreturned.validate_complete(memory.state)\nmemory.state.sr = returned.status\nactual = returned.stack_cursor.long()\nif actual != continuation:\n    raise Boundary('original trigger return slot changed to ' + str(actual))\nreturned = battle_replace(returned, stack_cursor=returned.stack_cursor.advance(4))\nreturn (returned, low16(returned.offset_y), low16(returned.choice))"}, '_trigger_notification': {'signature': 'memory, frame, message, continuation', 'returns': None, 'flow': "frame = _trigger_store(memory, frame, 'f740', message)\nvalue = memory.port('f6d7').byte()\nstatus = frame.status & 65531 | (0 if value & 2 else 4)\nmemory.state.sr = status\nmemory.port('f6d7').set_byte(0, value ^ 2)\nframe, _, _ = _trigger_call(memory, battle_replace(frame, status=status), 155876, continuation)\nvalue = memory.port('f6d7').byte()\nstatus = frame.status & 65531 | (0 if value & 2 else 4)\nmemory.state.sr = status\nmemory.port('f6d7').set_byte(0, value ^ 2)\nreturn battle_replace(frame, status=status)"}, '_trigger_wait': {'signature': 'memory, frame, suffix, expected, reason', 'returns': None, 'flow': "while True:\n    value = memory.port(suffix).word()\n    frame = _trigger_compare(memory, frame, value, expected)\n    if value == expected:\n        return frame\n    if memory.complete:\n        raise Boundary('original interrupt wait requires full resumed trigger fields: ' + reason)\n    memory.state.progress(reason)\n    frame = battle_replace(frame, status=memory.state.sr)"}, '_trigger_regular_damage': {'signature': 'memory, frame', 'returns': None, 'flow': "frame = _trigger_notification(memory, frame, 303, 145348)\nframe, _, _ = _trigger_call(memory, frame, 99320, 145360)\nmode = memory.port('f612').word()\nframe = _trigger_compare(memory, frame, mode, 1041)\nif mode == 1041:\n    return frame\noffset = memory.port('f68a').word()\nframe = _trigger_conditions(memory, battle_replace(frame, target_x=_trigger_retained_word(frame.target_x, offset)), offset, 16)\nframe, offset = _trigger_shift(memory, frame, offset, 2)\nsource = memory.port('e59c').cursor()\nframe = battle_replace(frame, target_x=_trigger_retained_word(frame.target_x, offset), roster=source)\nframe = _trigger_store(memory, frame, 'f3c8', source.long(offset), 32)\nreturn _trigger_notification(memory, frame, 275, 145404)"}, '_trigger_duel': {'signature': 'memory, frame', 'returns': None, 'flow': "frame = _trigger_store(memory, frame, 'f3d0', memory.port('f3f2').word())\nframe = _trigger_store(memory, frame, 'f3d2', memory.port('f3a6').word())\nframe = _trigger_notification(memory, frame, 276, 145444)\nframe = _trigger_store(memory, frame, 'f702', memory.port('f3f2').word())\nframe = _trigger_store(memory, frame, 'f706', memory.port('f3a6').word())\nsaved_scene = memory.port('f612').word()\nframe = _trigger_push_word(memory, frame, saved_scene)\nsaved_menu = memory.port('f362').word()\nframe = _trigger_push_word(memory, frame, saved_menu)\nframe = _trigger_store(memory, frame, 'f772', 2)\nframe = _trigger_store(memory, frame, 'f612', 1031)\nframe = _trigger_store(memory, frame, 'f362', 3)\nmemory.port('f352').word()\nframe = _trigger_store(memory, frame, 'f352', 0)\nmemory.state.set_status_word(9472)\nframe = _trigger_wait(memory, battle_replace(frame, status=9472), 'f600', 196, 'battle-input-wait')\nmemory.state.set_status_word(9984)\nframe, _, _ = _trigger_call(memory, battle_replace(frame, status=9984), 3520, 145514)\nmemory.state.set_status_word(9472)\nframe = _trigger_wait(memory, battle_replace(frame, status=9472), 'f600', 132, 'battle-input-wait')\nframe, _, _ = _trigger_call(memory, frame, 95746, 145532)\nmemory.state.set_status_word(9472)\nframe = battle_replace(frame, status=9472)\nwhile True:\n    mode = memory.port('f612').word()\n    frame = _trigger_compare(memory, frame, mode, 1032)\n    if mode == 1032:\n        break\n    mode = memory.port('f612').word()\n    frame = _trigger_compare(memory, frame, mode, 1041)\n    if mode == 1041:\n        break\n    if memory.complete:\n        raise Boundary('original duel completion requires full resumed trigger fields')\n    memory.state.progress('battle-scene-completion')\n    frame = battle_replace(frame, status=memory.state.sr)\nmemory.state.set_status_word(9984)\nframe, menu = _trigger_pop_word(memory, battle_replace(frame, status=9984), saved_menu)\nmemory.port('f362').set_word(0, menu)\nframe, scene = _trigger_pop_word(memory, frame, saved_scene)\nmemory.port('f612').set_word(0, scene)\nreturn frame"}, 'trigger_battle_for_city_rectangle_fields': {'signature': 'memory, frame, actor', 'returns': None, 'flow': "frame = _trigger_frame(memory, frame)\nactor = uint(actor, 16)\nif memory.complete and actor != low16(frame.choice):\n    raise ValueError('actual incoming D7 low WORD required')\nfirst_flags = memory.port('3cc2').cursor()\nframe = battle_replace(frame, roster=first_flags)\nflag = first_flags.byte(actor)\nframe = _trigger_conditions(memory, frame, flag, 8)\nif flag:\n    return _trigger_carry(memory, frame, False)\nsecond_flags = memory.port('3dc2').cursor()\nframe = battle_replace(frame, candidates=second_flags)\nflag = second_flags.byte(actor)\nframe = _trigger_conditions(memory, frame, flag, 8)\nif flag:\n    return _trigger_carry(memory, frame, False)\nbounds = memory.table(713138).cursor()\nframe = battle_replace(frame, roster=bounds)\noffset = memory.port('f68a').word()\nframe = _trigger_conditions(memory, battle_replace(frame, target_x=_trigger_retained_word(frame.target_x, offset)), offset, 16)\nframe, offset = _trigger_shift(memory, frame, offset, 3)\nframe = battle_replace(frame, target_x=_trigger_retained_word(frame.target_x, offset))\nx_min = bounds.word(offset)\nframe = _trigger_conditions(memory, battle_replace(frame, target_y=_trigger_retained_word(frame.target_y, x_min)), x_min, 16)\nx_max = bounds.word(offset, 2)\nframe = _trigger_conditions(memory, battle_replace(frame, unit=_trigger_retained_word(frame.unit, x_max)), x_max, 16)\ny_min = bounds.word(offset, 4)\nframe = _trigger_conditions(memory, battle_replace(frame, count=_trigger_retained_word(frame.count, y_min)), y_min, 16)\ny_max = bounds.word(offset, 6)\nframe = _trigger_conditions(memory, battle_replace(frame, distance=_trigger_retained_word(frame.distance, y_max)), y_max, 16)\npositions = memory.port('a150').cursor()\nframe = _trigger_conditions(memory, battle_replace(frame, roster=positions, target_x=_trigger_retained_word(frame.target_x, actor)), actor, 16)\nframe, actor_offset = _trigger_shift(memory, frame, actor, 2)\nframe = battle_replace(frame, target_x=_trigger_retained_word(frame.target_x, actor_offset))\nvalue = positions.word(actor_offset)\nframe = _trigger_compare(memory, frame, x_min, value)\nif x_min > value:\n    return _trigger_carry(memory, frame, False)\nvalue = positions.word(actor_offset)\nframe = _trigger_compare(memory, frame, x_max, value)\nif x_max < value:\n    return _trigger_carry(memory, frame, False)\nvalue = positions.word(actor_offset, 2)\nframe = _trigger_compare(memory, frame, y_min, value)\nif y_min > value:\n    return _trigger_carry(memory, frame, False)\nvalue = positions.word(actor_offset, 2)\nframe = _trigger_compare(memory, frame, y_max, value)\nif y_max < value:\n    return _trigger_carry(memory, frame, False)\nframe = _trigger_store(memory, frame, 'f3f2', actor)\nframe, selected, terminator = _trigger_call(memory, frame, 124004, 145310)\nframe = _trigger_push_word(memory, frame, terminator)\nframe = _trigger_store(memory, frame, 'f3a6', selected)\nduel = False\nif not negative_word(selected):\n    frame, _, _ = _trigger_call(memory, frame, 123938, 145326)\n    duel = bool(frame.status & 1)\nframe = _trigger_duel(memory, frame) if duel else _trigger_regular_damage(memory, frame)\nframe, saved_choice = _trigger_pop_word(memory, frame, terminator)\nframe = battle_replace(frame, choice=_trigger_retained_word(frame.choice, saved_choice))\nreturn _trigger_carry(memory, frame, True)"}, 'find_nearest_secondary_terrain_target_observations': {'signature': 'state: GameplayState', 'returns': 'tuple[NearestTerrainTarget, Word]', 'flow': "checked_state(state)\nfrom .business_reuse import load_battlefield_map_context, read_battlefield_terrain_type, rounded_radial_distance\nmap_context = load_battlefield_map_context(state)\npositions = _port(state, 'a150')\noffset = u16(_port(state, 'f3f2').word() << 2)\norigin_x = positions.word(offset) >> 7\norigin_y = positions.word(offset, 2) >> 7\ndistance, chosen = (65535, 32768)\nroster = _port(state, 'a5a4').cursor()\nwhile True:\n    member = roster.next_word()\n    if negative_word(member):\n        return (NearestTerrainTarget(distance, chosen), member)\n    offset = u16((member & 255) << 2)\n    x, y = (positions.word(offset) >> 7, positions.word(offset, 2) >> 7)\n    terrain = read_battlefield_terrain_type(state, map_context, x, y)\n    if low8(terrain) != 6:\n        continue\n    dx, dy = (u16(x - origin_x), u16(y - origin_y))\n    if x < origin_x:\n        dx = u16(-dx)\n    if y < origin_y:\n        dy = u16(-dy)\n    measured = low16(rounded_radial_distance(state, u32(dx * dx + dy * dy)))\n    if measured < distance or (measured == distance and (not _port(state, 'f321').byte() & 1)):\n        distance, chosen = (measured, offset >> 2)"}})
APPROVED['contexts_battle'].update({'BattleTriggerMemory', 'BattleTriggerFrame', 'battle_replace'})


# Complete actual23736 absolute-LONG task flags; single owner declaration.
DECLARATIONS.update({'trigger_battle_for_city_rectangle_fields': {'signature': 'memory, frame, actor', 'returns': None, 'flow': "frame = _trigger_frame(memory, frame)\nactor = uint(actor, 16)\nif memory.complete and actor != low16(frame.choice):\n    raise ValueError('actual incoming D7 low WORD required')\nfirst_flags = memory.table(16727234).cursor()\nframe = battle_replace(frame, roster=first_flags)\nflag = first_flags.byte(actor)\nframe = _trigger_conditions(memory, frame, flag, 8)\nif flag:\n    return _trigger_carry(memory, frame, False)\nsecond_flags = memory.table(16727490).cursor()\nframe = battle_replace(frame, candidates=second_flags)\nflag = second_flags.byte(actor)\nframe = _trigger_conditions(memory, frame, flag, 8)\nif flag:\n    return _trigger_carry(memory, frame, False)\nbounds = memory.table(713138).cursor()\nframe = battle_replace(frame, roster=bounds)\noffset = memory.port('f68a').word()\nframe = _trigger_conditions(memory, battle_replace(frame, target_x=_trigger_retained_word(frame.target_x, offset)), offset, 16)\nframe, offset = _trigger_shift(memory, frame, offset, 3)\nframe = battle_replace(frame, target_x=_trigger_retained_word(frame.target_x, offset))\nx_min = bounds.word(offset)\nframe = _trigger_conditions(memory, battle_replace(frame, target_y=_trigger_retained_word(frame.target_y, x_min)), x_min, 16)\nx_max = bounds.word(offset, 2)\nframe = _trigger_conditions(memory, battle_replace(frame, unit=_trigger_retained_word(frame.unit, x_max)), x_max, 16)\ny_min = bounds.word(offset, 4)\nframe = _trigger_conditions(memory, battle_replace(frame, count=_trigger_retained_word(frame.count, y_min)), y_min, 16)\ny_max = bounds.word(offset, 6)\nframe = _trigger_conditions(memory, battle_replace(frame, distance=_trigger_retained_word(frame.distance, y_max)), y_max, 16)\npositions = memory.port('a150').cursor()\nframe = _trigger_conditions(memory, battle_replace(frame, roster=positions, target_x=_trigger_retained_word(frame.target_x, actor)), actor, 16)\nframe, actor_offset = _trigger_shift(memory, frame, actor, 2)\nframe = battle_replace(frame, target_x=_trigger_retained_word(frame.target_x, actor_offset))\nvalue = positions.word(actor_offset)\nframe = _trigger_compare(memory, frame, x_min, value)\nif x_min > value:\n    return _trigger_carry(memory, frame, False)\nvalue = positions.word(actor_offset)\nframe = _trigger_compare(memory, frame, x_max, value)\nif x_max < value:\n    return _trigger_carry(memory, frame, False)\nvalue = positions.word(actor_offset, 2)\nframe = _trigger_compare(memory, frame, y_min, value)\nif y_min > value:\n    return _trigger_carry(memory, frame, False)\nvalue = positions.word(actor_offset, 2)\nframe = _trigger_compare(memory, frame, y_max, value)\nif y_max < value:\n    return _trigger_carry(memory, frame, False)\nframe = _trigger_store(memory, frame, 'f3f2', actor)\nframe, selected, terminator = _trigger_call(memory, frame, 124004, 145310)\nframe = _trigger_push_word(memory, frame, terminator)\nframe = _trigger_store(memory, frame, 'f3a6', selected)\nduel = False\nif not negative_word(selected):\n    frame, _, _ = _trigger_call(memory, frame, 123938, 145326)\n    duel = bool(frame.status & 1)\nframe = _trigger_duel(memory, frame) if duel else _trigger_regular_damage(memory, frame)\nframe, saved_choice = _trigger_pop_word(memory, frame, terminator)\nframe = battle_replace(frame, choice=_trigger_retained_word(frame.choice, saved_choice))\nreturn _trigger_carry(memory, frame, True)"}})

# B15 complete unique status/strength field bodies; old APIs only project.
DECLARATIONS.update({'_presentation_call_fields': {'signature': 'memory, frame, continuation, algorithm',
                               'returns': None,
                               'flow': 'frame = _presentation_frame(memory, frame)\n'
                                       'uint(continuation, 32)\n'
                                       'if frame.stack_cursor is None:\n'
                                       '    return memory.finish(algorithm(memory, frame))\n'
                                       'stack = frame.stack_cursor.advance(-4)\n'
                                       'stack.set_long(0, continuation)\n'
                                       'entered = first_replace(frame, stack_cursor=stack)\n'
                                       'memory.finish(entered)\n'
                                       'returned = memory.finish(algorithm(memory, entered))\n'
                                       'actual = returned.stack_cursor.long()\n'
                                       'if actual != continuation:\n'
                                       "    raise Boundary('original presentation child return slot changed "
                                       "to ' + str(actual))\n"
                                       'return first_replace(returned, '
                                       'stack_cursor=returned.stack_cursor.advance(4))'},
 '_presentation_collect_first_fields': {'signature': 'memory, frame',
                                        'returns': None,
                                        'flow': 'return collect_battle_special_status_members_fields(memory, '
                                                'frame, 0)'},
 '_presentation_collect_second_fields': {'signature': 'memory, frame',
                                         'returns': None,
                                         'flow': 'return '
                                                 'collect_battle_special_status_members_fields(memory, '
                                                 'frame, 2)'},
 '_presentation_frame': {'signature': 'memory, frame',
                         'returns': None,
                         'flow': 'if type(memory) is not BattlePresentationMemory:\n'
                                 "    raise ValueError('closed same-state presentation memory required')\n"
                                 'return memory.validate_frame(frame)'},
 '_presentation_random_fields': {'signature': 'memory, frame',
                                 'returns': None,
                                 'flow': 'return memory.random_fields(frame)'},
 '_presentation_sub_long_fields': {'signature': 'frame, name, left, right',
                                   'returns': None,
                                   'flow': 'uint(left, 32)\n'
                                           'uint(right, 32)\n'
                                           'value = u32(left - right)\n'
                                           'overflow = bool((left ^ right) & (left ^ value) & 2147483648)\n'
                                           'status = (17 if left < right else 0) | (2 if overflow else 0) | '
                                           '(8 if value & 2147483648 else 0) | (4 if value == 0 else 0)\n'
                                           'return first_replace(frame, **{name: value}, status=status)'},
 'collect_battle_special_status_members': {'signature': 'state: GameplayState, source: Cursor, destination: '
                                                        'Cursor, side_bits: Word',
                                           'returns': 'Cursor',
                                           'flow': 'checked_state(state)\n'
                                                   'checked_cursor(source, state)\n'
                                                   'checked_cursor(destination, state)\n'
                                                   'uint(side_bits, 16)\n'
                                                   'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                                   'roster=destination, candidates=source, '
                                                   "controller=_port(state, 'c700'))\n"
                                                   'return '
                                                   'collect_battle_special_status_members_fields(BattlePresentationMemory(state), '
                                                   'frame, side_bits).roster'},
 'collect_battle_special_status_members_fields': {'signature': 'memory, frame, side_bits: Word',
                                                  'returns': 'FirstDeploymentFrame',
                                                  'flow': 'frame = _presentation_frame(memory, frame)\n'
                                                          'uint(side_bits, 16)\n'
                                                          'source, destination, statuses = '
                                                          '(frame.candidates, frame.roster, '
                                                          'frame.controller)\n'
                                                          'for view in (source, destination, statuses):\n'
                                                          '    memory.checked_view(view)\n'
                                                          'if frame.target_y is not None and '
                                                          'low16(frame.target_y) != side_bits:\n'
                                                          "    raise ValueError('actual incoming D1 low WORD "
                                                          "required')\n"
                                                          'while True:\n'
                                                          '    member = source.next_word()\n'
                                                          "    frame = _first_word(frame, 'target_x', "
                                                          'member)\n'
                                                          '    if negative_word(member):\n'
                                                          '        return memory.finish(frame)\n'
                                                          '    member &= 255\n'
                                                          "    frame = _first_word(frame, 'target_x', "
                                                          'member)\n'
                                                          '    active = bool(statuses.byte(member) & 16)\n'
                                                          '    if frame.status is not None:\n'
                                                          '        frame = first_replace(frame, '
                                                          'status=frame.status & 27 | (0 if active else 4))\n'
                                                          '    if active:\n'
                                                          '        member |= side_bits\n'
                                                          "        frame = _first_word(frame, 'target_x', "
                                                          'member)\n'
                                                          '        destination.append_word(member)\n'
                                                          '        frame = _first_memory_word(frame, '
                                                          'member)'},
 'compute_battle_damage_potential': {'signature': 'state: GameplayState, factor: Long, retained_damage: Long',
                                     'returns': 'DamagePotentialResult',
                                     'flow': 'checked_state(state)\n'
                                             'uint(factor, 32)\n'
                                             'uint(retained_damage, 32)\n'
                                             'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                             'target_x=factor, choice=retained_damage)\n'
                                             'returned = '
                                             'compute_battle_damage_potential_fields(BattlePresentationMemory(state), '
                                             'frame, factor)\n'
                                             'return DamagePotentialResult(returned.target_x, '
                                             'returned.choice)'},
 'compute_battle_damage_potential_fields': {'signature': 'memory, frame, factor: Long',
                                            'returns': 'FirstDeploymentFrame',
                                            'flow': 'frame = _presentation_frame(memory, frame)\n'
                                                    'uint(factor, 32)\n'
                                                    'if frame.target_x is not None and frame.target_x != '
                                                    'factor:\n'
                                                    "    raise ValueError('actual incoming full D0 factor "
                                                    "required')\n"
                                                    'factor = u32(low16(factor) * 100)\n'
                                                    "frame = _first_long(frame, 'target_x', factor)\n"
                                                    'strengths = memory.table(4294948352).cursor()\n'
                                                    'frame = first_replace(frame, roster=strengths)\n'
                                                    'opposing = memory.table(4294964134).word()\n'
                                                    "frame = _first_word(frame, 'target_y', opposing)\n"
                                                    "frame = _first_shift_word(frame, 'target_y', opposing, "
                                                    '1)\n'
                                                    'strength = strengths.word(u16(opposing << 1))\n'
                                                    "frame = _first_word(frame, 'target_y', strength)\n"
                                                    'subtraction = u32(strength * low16(factor))\n'
                                                    "frame = _first_long(frame, 'target_y', subtraction)\n"
                                                    'acting = memory.table(4294964210).word()\n'
                                                    "frame = _first_word(frame, 'target_x', acting)\n"
                                                    "frame = _first_shift_word(frame, 'target_x', acting, "
                                                    '1)\n'
                                                    'strength = strengths.word(u16(acting << 1))\n'
                                                    "frame = _first_word(frame, 'target_x', strength)\n"
                                                    'numerator = u32(strength * 1000)\n'
                                                    "frame = _first_long(frame, 'target_x', numerator)\n"
                                                    'frame = _presentation_sub_long_fields(frame, '
                                                    "'target_x', numerator, subtraction)\n"
                                                    'if numerator < subtraction:\n'
                                                    "    return memory.finish(_first_word(frame, 'choice', "
                                                    '0))\n'
                                                    'divisors = memory.table(4294950912).cursor()\n'
                                                    'frame = first_replace(frame, roster=divisors)\n'
                                                    'opposing = memory.table(4294964134).word()\n'
                                                    "frame = _first_word(frame, 'target_y', opposing)\n"
                                                    "frame = _first_shift_word(frame, 'target_y', opposing, "
                                                    '1)\n'
                                                    'divisor = divisors.word(u16(opposing << 1))\n'
                                                    "frame = _first_word(frame, 'target_y', divisor)\n"
                                                    "frame = _first_add_word(frame, 'target_y', divisor, "
                                                    '100)\n'
                                                    'divisor = u16(divisor + 100)\n'
                                                    'result = divu_retained(u32(numerator - subtraction), '
                                                    'divisor)\n'
                                                    'frame = first_replace(frame, target_x=result)\n'
                                                    "frame = _first_word(frame, 'choice', low16(result))\n"
                                                    'frame = _first_compare_word(frame, low16(result), 700)\n'
                                                    'if low16(result) > 700:\n'
                                                    "    frame = _first_word(frame, 'target_x', 700)\n"
                                                    'return memory.finish(frame)'},
 'sample_battle_special_status_factor': {'signature': 'state: GameplayState',
                                         'returns': 'Long',
                                         'flow': 'checked_state(state)\n'
                                                 'return '
                                                 'sample_battle_special_status_factor_fields(BattlePresentationMemory(state), '
                                                 'FirstDeploymentFrame.unobserved()).target_x'},
 'sample_battle_special_status_factor_fields': {'signature': 'memory, frame',
                                                'returns': 'FirstDeploymentFrame',
                                                'flow': 'frame = _presentation_frame(memory, frame)\n'
                                                        'selector = memory.table(4294963154).word()\n'
                                                        "frame = _first_word(frame, 'offset_x', selector)\n"
                                                        "frame = _first_shift_word(frame, 'offset_x', "
                                                        'selector, 1)\n'
                                                        'offset = u16(selector << 1)\n'
                                                        'second_selector = memory.table(4294963154).word()\n'
                                                        "frame = _first_add_word(frame, 'offset_x', offset, "
                                                        'second_selector)\n'
                                                        'offset = u16(offset + second_selector)\n'
                                                        "frame = _first_shift_word(frame, 'offset_x', "
                                                        'offset, 3)\n'
                                                        'offset = u16(offset << 3)\n'
                                                        'destination = memory.table(4294955776).cursor()\n'
                                                        'frame = first_replace(frame, roster=destination, '
                                                        'controller=memory.table(4294952704), '
                                                        'candidates=memory.table(4294944080).cursor())\n'
                                                        "frame = _first_word(frame, 'target_y', 0)\n"
                                                        'frame = _presentation_call_fields(memory, frame, '
                                                        '108324, _presentation_collect_first_fields)\n'
                                                        "frame = _first_word(frame, 'target_y', 2)\n"
                                                        'frame = first_replace(frame, '
                                                        'candidates=memory.table(4294944164).cursor())\n'
                                                        'frame = _presentation_call_fields(memory, frame, '
                                                        '108336, _presentation_collect_second_fields)\n'
                                                        'frame.roster.put_word(65535)\n'
                                                        'frame = _first_memory_word(frame, 65535)\n'
                                                        'first_member = memory.table(4294955776).word()\n'
                                                        'frame = _first_memory_word(frame, first_member)\n'
                                                        'if not negative_word(first_member):\n'
                                                        "    frame = _first_add_word(frame, 'offset_x', "
                                                        'offset, 4)\n'
                                                        '    offset = u16(offset + 4)\n'
                                                        '    source = memory.table(4294955776).cursor()\n'
                                                        '    strengths = memory.table(4294948352).cursor()\n'
                                                        '    frame = first_replace(frame, roster=source, '
                                                        'candidates=strengths)\n'
                                                        "    frame = _first_word(frame, 'target_x', 0)\n"
                                                        '    best_value, best_member = (0, 2)\n'
                                                        '    while True:\n'
                                                        '        member = source.next_word()\n'
                                                        "        frame = _first_word(frame, 'unit', member)\n"
                                                        '        if negative_word(member):\n'
                                                        '            break\n'
                                                        "        frame = _first_word(frame, 'count', "
                                                        'member)\n'
                                                        "        frame = _first_shift_word(frame, 'count', "
                                                        'member, 1)\n'
                                                        '        strength = strengths.word(u16(member << '
                                                        '1))\n'
                                                        "        frame = _first_word(frame, 'distance', "
                                                        'strength)\n'
                                                        '        frame = _first_compare_word(frame, '
                                                        'strength, best_value)\n'
                                                        '        if strength >= best_value:\n'
                                                        '            best_value, best_member = (strength, '
                                                        'member)\n'
                                                        "            frame = _first_word(frame, 'target_y', "
                                                        'member)\n'
                                                        "            frame = _first_word(frame, 'target_x', "
                                                        'strength)\n'
                                                        "    frame = _first_right_word(frame, 'target_y', "
                                                        'best_member, 4)\n'
                                                        '    side = memory.table(4294964950).word()\n'
                                                        "    frame = _first_word(frame, 'target_x', side)\n"
                                                        '    selected_side = u16(best_member >> 4 ^ side)\n'
                                                        "    frame = _first_word(frame, 'target_y', "
                                                        'selected_side)\n'
                                                        '    side_differs = bool(selected_side & 2)\n'
                                                        '    if frame.status is not None:\n'
                                                        '        frame = first_replace(frame, '
                                                        'status=frame.status & 27 | (0 if side_differs else '
                                                        '4))\n'
                                                        '    if side_differs:\n'
                                                        "        frame = _first_add_word(frame, 'offset_x', "
                                                        'offset, 4)\n'
                                                        '        offset = u16(offset + 4)\n'
                                                        'frame = _presentation_call_fields(memory, frame, '
                                                        '108404, _presentation_random_fields)\n'
                                                        'sample = low16(frame.target_x)\n'
                                                        "frame = _first_long(frame, 'target_x', sample)\n"
                                                        'parameters = memory.table(106972).cursor()\n'
                                                        'frame = first_replace(frame, roster=parameters)\n'
                                                        'product = u32(sample * parameters.word(offset))\n'
                                                        "frame = _first_long(frame, 'target_x', product)\n"
                                                        'swapped = swap_words(product)\n'
                                                        "frame = _first_long(frame, 'target_x', swapped)\n"
                                                        'base = parameters.word(offset, 2)\n'
                                                        "frame = _first_add_word(frame, 'target_x', "
                                                        'low16(swapped), base)\n'
                                                        'return memory.finish(frame)'}})
APPROVED.setdefault('contexts_battle', set()).update({'_first_word', '_first_long', '_first_compare_word', '_first_right_word', 'FirstDeploymentFrame', 'BattlePresentationMemory', '_first_memory_word', '_first_shift_word', '_first_add_word', 'first_replace'})


# Entire sole _damage_add_long current field body.
DECLARATIONS.update({'_damage_add_long': {'signature': 'memory, frame, name, value', 'returns': None, 'flow': 'from ..high_level_main_flows.business_movement_support import _movement_arithmetic_long\nreturn _movement_arithmetic_long(memory.state, frame, name, value)'}})


# Entire sole _damage_apply_mutual_losses_fields current field body.
DECLARATIONS.update({'_damage_apply_mutual_losses_fields': {'signature': 'memory, frame', 'returns': None, 'flow': "frame = _damage_store(memory, frame, 16727766, low16(frame.choice))\nframe = _first_add_word(frame, 'choice', low16(frame.choice), 200)\nscene = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_x', scene)\nframe = _first_shift_word(frame, 'target_x', scene, 2)\nreserves = memory.table(4294960540).cursor()\nframe = first_replace(frame, roster=reserves)\namount = reserves.long(u16(scene << 2))\nframe = _first_long(frame, 'target_x', amount)\nframe = _first_word(frame, 'target_y', 100)\nfrom ..high_level_battle_ai.business_formation import _first_sub_word\nframe = _first_sub_word(frame, 'target_y', 100, low16(amount))\nframe = _first_long(frame, 'choice', low16(frame.choice) * low16(frame.target_y))\nretained_choice = divu_retained(frame.choice, 100)\nactor = memory.table(4294964210).word()\nframe = first_replace(_first_word(frame, 'target_x', actor), choice=retained_choice)\nframe = _first_shift_word(frame, 'target_x', actor, 1)\nability = memory.table(4294950912).cursor()\nframe = first_replace(frame, roster=ability)\nactor_ability = ability.word(u16(actor << 1))\nframe = _first_word(frame, 'target_x', actor_ability)\nframe = _first_long(frame, 'choice', low16(frame.choice) * actor_ability)\nretained_choice = divu_retained(frame.choice, 100)\nshortage = memory.table(16727770).word()\nframe = first_replace(_first_memory_word(frame, shortage), choice=retained_choice)\nif shortage:\n    frame = _first_long(frame, 'choice', frame.choice & 65535)\n    frame = _damage_shift_long(memory, frame, 'choice', 2)\n    retained_choice = divu_retained(frame.choice, 10)\nelse:\n    retained_choice = frame.choice\nopposing = memory.table(4294964134).word()\nframe = first_replace(_first_word(frame, 'target_x', opposing), choice=retained_choice)\nframe = _first_shift_word(frame, 'target_x', opposing, 2)\ntroops = memory.table(4294952960).cursor()\nframe = first_replace(frame, roster=troops)\noriginal = troops.long(u16(opposing << 2))\nframe = _first_long(frame, 'target_y', original)\ndamage = low16(frame.choice)\nframe = _first_sub_word(frame, 'target_y', low16(original), damage)\nif low16(original) < damage:\n    frame = _first_word(frame, 'target_y', 0)\ntroops.set_long(u16(opposing << 2), frame.target_y)\nframe = _first_long(frame, 'target_y', frame.target_y)\nframe = _first_long(frame, 'offset_x', 0)\nframe = _first_word(frame, 'offset_x', damage)\nframe = _damage_shift_long(memory, frame, 'offset_x', 1)\nretained_offset = divu_retained(frame.offset_x, 400)\nactor = memory.table(4294964210).word()\nframe = first_replace(_first_word(frame, 'target_x', actor), offset_x=retained_offset)\nframe = _first_shift_word(frame, 'target_x', actor, 1)\noffset = u16(actor << 1)\nability = memory.table(4294950912).cursor()\nframe = first_replace(frame, roster=ability)\noriginal_ability = ability.word(offset)\nframe = _first_word(frame, 'target_y', original_ability)\nframe = _first_word(frame, 'unit', original_ability)\nframe = _first_add_word(frame, 'target_y', original_ability, low16(frame.offset_x))\nnew_ability = u16(original_ability + low16(frame.offset_x))\nframe = _first_compare_word(frame, new_ability, 999)\nif new_ability > 999:\n    new_ability = 999\n    frame = _first_word(frame, 'target_y', new_ability)\nability.set_word(offset, new_ability)\nframe = _first_memory_word(frame, new_ability)\nframe = _first_long(frame, 'choice', low16(frame.choice) * 2000)\nretained_choice = divu_retained(frame.choice, original_ability)\nshortage = memory.table(16727770).word()\nframe = first_replace(_first_memory_word(frame, shortage), choice=retained_choice)\nif shortage:\n    frame = _first_shift_word(frame, 'choice', low16(frame.choice), 1)\nframe = _first_shift_word(frame, 'target_x', offset, 1)\noffset = u16(offset << 1)\ntroops = memory.table(4294952960).cursor()\nframe = first_replace(frame, roster=troops)\noriginal = troops.long(offset)\nframe = _first_long(frame, 'target_y', original)\ndamage = low16(frame.choice)\nframe = _first_sub_word(frame, 'target_y', low16(original), damage)\nif low16(original) < damage:\n    frame = _first_word(frame, 'target_y', 0)\ntroops.set_long(offset, frame.target_y)\nframe = _first_long(frame, 'target_y', frame.target_y)\nframe = _first_long(frame, 'choice', frame.choice & 65535)\nretained_choice = divu_retained(frame.choice, 400)\nopposing = memory.table(4294964134).word()\nframe = first_replace(_first_word(frame, 'target_x', opposing), choice=retained_choice)\nframe = _first_shift_word(frame, 'target_x', opposing, 1)\nability = memory.table(4294950912).cursor()\nframe = first_replace(frame, roster=ability)\nreturn _damage_raise_ability_fields(memory, frame, ability, u16(opposing << 1), low16(frame.choice))"}})


# Entire sole _damage_bchg_side current field body.
DECLARATIONS.update({'_damage_bchg_side': {'signature': 'memory, frame', 'returns': None, 'flow': 'value = memory.table(4294964951).byte()\nmemory.table(4294964951).set_byte(0, value ^ 2)\nstatus = None if frame.status is None else frame.status & 27 | (0 if value & 2 else 4)\nreturn memory.finish(first_replace(frame, status=status))'}})


# Entire sole _damage_divide current field body.
DECLARATIONS.update({'_damage_divide': {'signature': 'frame, name, divisor, instruction', 'returns': None, 'flow': 'from ..high_level_remaining_flows.business_city import _city_movement_divide\nreturn _city_movement_divide(frame, name, divisor, instruction)'}})


# Entire sole _damage_external_call current field body.
DECLARATIONS.update({'_damage_external_call': {'signature': 'memory, frame, target, continuation', 'returns': None, 'flow': "frame = _presentation_frame(memory, frame)\nif frame.stack_cursor is None:\n    if target == 155876:\n        present_battle_message(memory.state)\n    elif target == 67372:\n        from .business_services import load_gameplay_scene\n        load_gameplay_scene(memory.state)\n    else:\n        raise Boundary('unknown original city damage child ' + str(target))\n    return first_replace(frame, status=None)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = memory.finish(first_replace(frame, stack_cursor=stack))\nif target == 155876:\n    from ..high_level_main_flows.business_movement_support import present_battle_message_fields\n    returned = present_battle_message_fields(memory.state, entered)\nelif target == 67372:\n    from .contexts_services import SceneRefreshMemory\n    from .business_services import load_gameplay_scene_fields\n    returned = load_gameplay_scene_fields(SceneRefreshMemory(memory.state), entered)\nelse:\n    returned = memory.state.service_at(target, entered)\nreturned = memory.finish(returned)\nactual = returned.stack_cursor.long()\nif actual != continuation:\n    raise Boundary('original city damage child return slot changed to ' + str(actual))\nreturn first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))"}})


# Entire sole _damage_map_fields current field body.
DECLARATIONS.update({'_damage_map_fields': {'signature': 'memory, frame', 'returns': None, 'flow': 'if frame.stack_cursor is not None:\n    from ..high_level_battle_ai.business_actions import _battle_action_map_fields\n    from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory\n    return _battle_action_map_fields(BattlePolicyMemory(memory.state), frame)\nfrom .business_reuse import load_battlefield_map_context\nterrain = load_battlefield_map_context(memory.state)\nreturn first_replace(frame, roster=terrain.cursor(), status=None)'}})


# Entire sole _damage_potential_fields current field body.
DECLARATIONS.update({'_damage_potential_fields': {'signature': 'memory, frame', 'returns': None, 'flow': 'return compute_battle_damage_potential_fields(memory, frame, frame.target_x)'}})


# Entire sole _damage_raise_ability_fields current field body.
DECLARATIONS.update({'_damage_raise_ability_fields': {'signature': 'memory, frame, view, offset, increment', 'returns': None, 'flow': "value = view.word(offset)\nframe = _first_word(frame, 'target_y', value)\nframe = _first_add_word(frame, 'target_y', value, increment)\nvalue = u16(value + increment)\nframe = _first_compare_word(frame, value, 999)\nif value > 999:\n    value = 999\n    frame = _first_word(frame, 'target_y', value)\nview.set_word(offset, value)\nreturn _first_memory_word(frame, value)"}})


# Entire sole _damage_restore_longs current field body.
DECLARATIONS.update({'_damage_restore_longs': {'signature': 'memory, frame, names, observed', 'returns': None, 'flow': 'from ..high_level_main_flows.business_movement_support import _movement_restore_longs\nif frame.stack_cursor is not None:\n    frame = _movement_restore_longs(memory.state, frame, names)\nelse:\n    frame = first_replace(frame, **observed)\nreturn memory.finish(frame)'}})


# Entire sole _damage_save_longs current field body.
DECLARATIONS.update({'_damage_save_longs': {'signature': 'memory, frame, names', 'returns': None, 'flow': "from ..high_level_main_flows.business_movement_support import _movement_save_longs, _movement_address_carrier\nnumeric = ('target_x', 'target_y', 'unit', 'count', 'distance', 'offset_x', 'offset_y', 'choice')\nobserved = {name: frame.carrier(name) if name in numeric else _movement_address_carrier(frame, name) for name in names}\nif frame.stack_cursor is not None:\n    frame = _movement_save_longs(memory.state, frame, names)\nreturn (frame, observed)"}})


# Entire sole _damage_shift_long current field body.
DECLARATIONS.update({'_damage_shift_long': {'signature': 'memory, frame, name, amount', 'returns': None, 'flow': 'from ..high_level_remaining_flows.business_city import _special_action_shift_long\nreturn _special_action_shift_long(memory.state, frame, name, amount)'}})


# Entire sole _damage_store current field body.
DECLARATIONS.update({'_damage_store': {'signature': 'memory, frame, address, value, width=16', 'returns': None, 'flow': "uint(value, width)\nif width == 16:\n    memory.table(address).set_word(0, value)\n    frame = _first_memory_word(frame, value)\nelif width == 32:\n    memory.table(address).set_long(0, value)\n    status = None if frame.status is None else frame.status & 16 | (8 if value & 2147483648 else 0) | (4 if value == 0 else 0)\n    frame = first_replace(frame, status=status)\nelse:\n    raise ValueError('actual city damage store width required')\nreturn memory.finish(frame)"}})


# Entire sole _damage_terrain_fields current field body.
DECLARATIONS.update({'_damage_terrain_fields': {'signature': 'memory, frame, x, y, continuation', 'returns': None, 'flow': 'if frame.stack_cursor is not None:\n    from ..high_level_battle_ai.business_actions import _deployment_terrain_lookup\n    from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory\n    return _deployment_terrain_lookup(BattlePolicyMemory(memory.state), frame, x, y, continuation)\nfrom .business_reuse import read_battlefield_terrain_type_observations\ncarrier, word, category, extend = read_battlefield_terrain_type_observations(memory.state, frame.roster, x, y, frame.target_x)\nstatus = (16 if extend else 0) | (8 if category & 128 else 0) | (4 if category == 0 else 0)\nreturn (memory.finish(first_replace(frame, target_x=carrier, status=status)), category)'}})


# Entire sole _damage_terrain_query_fields current field body.
DECLARATIONS.update({'_damage_terrain_query_fields': {'signature': 'memory, frame', 'returns': None, 'flow': 'return secondary_roster_has_terrain_six_fields(memory, frame)[0]'}})


# Entire sole _damage_visible_owner current field body.
DECLARATIONS.update({'_damage_visible_owner': {'signature': 'memory, frame', 'returns': None, 'flow': "owner = memory.table(4294964876).word()\nframe = _first_word(frame, 'target_x', owner)\nfor address in (4294964858, 4294964860, 4294964862):\n    candidate = memory.table(address).word()\n    frame = _first_compare_word(frame, owner, candidate)\n    if owner == candidate:\n        return (memory.finish(frame), True)\nreturn (memory.finish(frame), False)"}})


# Entire sole _trigger_call current field body.
DECLARATIONS.update({'_trigger_call': {'signature': 'memory, frame, target, continuation', 'returns': None, 'flow': "frame = _trigger_frame(memory, frame)\nif not memory.complete:\n    return _trigger_legacy_call(memory, frame, target)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = battle_replace(frame, stack_cursor=stack)\nif target == 99320:\n    fields = FirstDeploymentFrame(target_x=entered.target_x, target_y=entered.target_y, unit=entered.unit, count=entered.count, distance=entered.distance, offset_x=entered.offset_x, offset_y=entered.offset_y, choice=entered.choice, roster=entered.roster, candidates=entered.candidates, controller=entered.controller, scan=entered.scan, opponent=entered.opponent, scratch=entered.scratch, auxiliary=entered.auxiliary, stack_cursor=entered.stack_cursor, status=entered.status & 31)\n    fields = resolve_city_battle_damage_fields(BattlePresentationMemory(memory.state), fields)[0]\n    returned = battle_replace(entered, target_x=fields.target_x, target_y=fields.target_y, unit=fields.unit, count=fields.count, distance=fields.distance, offset_x=fields.offset_x, offset_y=fields.offset_y, choice=fields.choice, roster=fields.roster, candidates=fields.candidates, controller=fields.controller, scan=fields.scan, opponent=fields.opponent, scratch=fields.scratch, auxiliary=fields.auxiliary, stack_cursor=fields.stack_cursor, status=memory.state.sr)\nelse:\n    returned = memory.state.service_at(target, entered)\nif type(returned) is not BattleTriggerFrame:\n    raise Boundary('real trigger child must return all observed full fields')\nreturned.validate_complete(memory.state)\nmemory.state.sr = returned.status\nactual = returned.stack_cursor.long()\nif actual != continuation:\n    raise Boundary('original trigger return slot changed to ' + str(actual))\nreturned = battle_replace(returned, stack_cursor=returned.stack_cursor.advance(4))\nreturn (returned, low16(returned.offset_y), low16(returned.choice))"}})


# Entire sole award_city_reserve_attrition current field body.
DECLARATIONS.update({'award_city_reserve_attrition': {'signature': 'state: GameplayState', 'returns': 'Long', 'flow': 'checked_state(state)\nreturn award_city_reserve_attrition_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved()).target_x'}})


# Entire sole award_city_reserve_attrition_fields current field body.
DECLARATIONS.update({'award_city_reserve_attrition_fields': {'signature': 'memory, frame', 'returns': None, 'flow': "frame = _presentation_frame(memory, frame)\nouter_names = ('target_y', 'roster')\nframe, outer = _damage_save_longs(memory, frame, outer_names)\nframe = _presentation_call_fields(memory, frame, 99822, _presentation_random_fields)\nframe = _first_long(frame, 'target_x', frame.target_x & 65535)\nframe = _first_long(frame, 'target_y', frame.target_x)\nframe = _damage_shift_long(memory, frame, 'target_x', 1)\nframe = _damage_add_long(memory, frame, 'target_x', frame.target_y)\nframe = _damage_shift_long(memory, frame, 'target_x', 1)\nframe = _first_long(frame, 'target_x', swap_words(frame.target_x))\nframe = _first_add_word(frame, 'target_x', low16(frame.target_x), 10)\nframe = _first_long(frame, 'target_y', 0)\nfactor = memory.table(16727766).word()\nframe = _first_word(frame, 'target_y', factor)\nframe = _first_add_word(frame, 'target_y', factor, 100)\nframe = _damage_divide(frame, 'target_y', 10, 99854)\nframe = _first_long(frame, 'target_x', low16(frame.target_x) * low16(frame.target_y))\nprevious = memory.table(16727762).long()\nframe = _first_long(frame, 'target_y', previous)\nframe = _damage_add_long(memory, frame, 'target_y', 500)\nframe = _damage_divide(frame, 'target_y', 100, 99872)\nframe = _first_long(frame, 'target_x', low16(frame.target_x) * low16(frame.target_y))\nactor = memory.table(4294964210).word()\nframe = _first_word(frame, 'unit', actor)\nframe = _first_shift_word(frame, 'unit', actor, 1)\noffset = u16(actor << 1)\nabilities = memory.table(4294947840).cursor()\nframe = first_replace(frame, roster=abilities)\nability = abilities.word(offset)\nframe = _first_word(frame, 'target_y', ability)\nreadiness = memory.table(4294948352).cursor()\nframe = first_replace(frame, roster=readiness)\nframe = _first_add_word(frame, 'target_y', ability, readiness.word(offset))\nframe = _first_long(frame, 'target_y', frame.target_y & 65535)\nframe = _damage_divide(frame, 'target_y', 10, 99906)\nframe = _first_long(frame, 'target_x', low16(frame.target_x) * low16(frame.target_y))\nframe = _damage_divide(frame, 'target_x', 20000, 99912)\nshortage = memory.table(16727770).word()\nframe = _first_memory_word(frame, shortage)\nif shortage:\n    loss = low16(frame.target_x)\n    frame = _first_word(frame, 'target_y', loss)\n    frame = _first_shift_word(frame, 'target_x', loss, 1)\n    frame = _first_add_word(frame, 'target_x', u16(loss << 1), loss)\n    frame = _first_shift_word(frame, 'target_x', u16(loss * 3), 1)\n    frame = _first_long(frame, 'target_x', frame.target_x & 65535)\n    frame = _damage_divide(frame, 'target_x', 10, 99940)\nscene = memory.table(4294964874).word()\nframe = _first_word(frame, 'unit', scene)\nframe = _first_shift_word(frame, 'unit', scene, 2)\noffset = u16(scene << 2)\nreserves = memory.table(4294960540).cursor()\nframe = first_replace(frame, roster=reserves)\nprevious = reserves.long(offset)\nframe = _first_long(frame, 'target_y', previous)\nfrom ..high_level_battle_ai.business_formation import _first_sub_word\nloss = low16(frame.target_x)\nframe = _first_sub_word(frame, 'target_y', low16(previous), loss)\nif low16(previous) < loss:\n    inner_names = ('target_x', 'unit', 'roster')\n    frame, inner = _damage_save_longs(memory, frame, inner_names)\n    frame = _presentation_call_fields(memory, frame, 99972, _damage_terrain_query_fields)\n    if not frame.status & 1:\n        frame, visible = _damage_visible_owner(memory, frame)\n        if visible:\n            frame = _damage_store(memory, frame, 16740390, 24)\n            frame = _damage_external_call(memory, frame, 67372, 100018)\n        saved_owner = memory.table(4294964086).word()\n        frame = _first_memory_word(frame, saved_owner)\n        if frame.stack_cursor is not None:\n            stack = frame.stack_cursor.advance(-2)\n            stack.set_word(0, saved_owner)\n            frame = first_replace(frame, stack_cursor=stack)\n        frame = _damage_store(memory, frame, 4294964086, memory.table(4294964876).word())\n        owner = memory.table(4294964878).word()\n        frame = _first_word(frame, 'target_x', owner)\n        frame = _first_shift_word(frame, 'target_x', owner, 1)\n        heads = memory.table(4294960704).cursor()\n        frame = first_replace(frame, roster=heads)\n        frame = _damage_store(memory, frame, 4294964176, heads.word(u16(owner << 1)))\n        frame = _damage_store(memory, frame, 4294965056, 319)\n        frame = _damage_bchg_side(memory, frame)\n        frame = _damage_external_call(memory, frame, 155876, 100062)\n        frame = _damage_bchg_side(memory, frame)\n        if frame.stack_cursor is not None:\n            saved_owner = frame.stack_cursor.word()\n            frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\n        frame = _damage_store(memory, frame, 4294964086, saved_owner)\n        frame = _damage_store(memory, frame, 4294964754, 1041)\n        memory.table(4294964066).word()\n        frame = _damage_store(memory, frame, 4294964066, 0)\n        memory.table(4294964950).word()\n        frame = _damage_store(memory, frame, 4294964950, 0)\n        frame = _first_word(frame, 'target_y', 0)\n    frame = _damage_restore_longs(memory, frame, inner_names, inner)\nremaining = low16(frame.target_y)\nrestored_offset = offset if frame.unit is None else low16(frame.unit)\nframe.roster.set_word(restored_offset, remaining, 2)\nframe = _first_memory_word(frame, remaining)\nframe = _damage_restore_longs(memory, frame, outer_names, outer)\nreturn memory.finish(frame)"}})


# Entire sole resolve_city_battle_damage current field body.
DECLARATIONS.update({'resolve_city_battle_damage': {'signature': 'state: GameplayState, retained_damage: Long=0', 'returns': 'Long', 'flow': 'checked_state(state)\nuint(retained_damage, 32)\nframe = first_replace(FirstDeploymentFrame.unobserved(), choice=retained_damage)\nreturn resolve_city_battle_damage_fields(BattlePresentationMemory(state), frame)[1]'}})


# Entire sole resolve_city_battle_damage_fields current field body.
DECLARATIONS.update({'resolve_city_battle_damage_fields': {'signature': 'memory, frame', 'returns': None, 'flow': "frame = _presentation_frame(memory, frame)\nframe = _presentation_call_fields(memory, frame, 99326, _presentation_random_fields)\nscene = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_x', scene)\nframe = _first_shift_word(frame, 'target_x', scene, 2)\nreserves = memory.table(4294960540).cursor()\nframe = first_replace(frame, roster=reserves)\namount = reserves.long(u16(scene << 2))\nframe = _first_long(frame, 'target_x', amount)\nframe = _first_long(frame, 'target_y', 0)\nseed = memory.table(4294964764).word()\nframe = _first_word(frame, 'target_y', seed)\nframe = _first_long(frame, 'unit', frame.target_y)\nframe = _damage_shift_long(memory, frame, 'target_y', 1)\nframe = _damage_add_long(memory, frame, 'target_y', frame.unit)\nframe = _damage_shift_long(memory, frame, 'target_y', 1)\nframe = _first_long(frame, 'target_y', swap_words(frame.target_y))\nframe = _first_add_word(frame, 'target_y', low16(frame.target_y), 5)\nframe = _first_long(frame, 'target_x', low16(amount) * low16(frame.target_y))\ndebit = frame.target_x\nside = memory.table(4294964950).word()\nframe = _first_word(frame, 'target_y', side)\nframe = _first_shift_word(frame, 'target_y', side, 2)\naddress = memory.table(99312).long(u16(side << 2))\nresources = memory.table(address).cursor()\nframe = first_replace(frame, roster=resources)\nframe = _first_word(frame, 'offset_y', 0)\navailable = resources.long()\nframe = _first_long(frame, 'target_y', available)\nframe = _presentation_sub_long_fields(frame, 'target_y', available, debit)\nshortage = available < debit\nif shortage:\n    frame = _first_long(frame, 'target_y', 0)\n    frame = _first_word(frame, 'offset_y', 1)\nframe = _damage_store(memory, frame, 16727770, int(shortage))\nresources.set_long(0, frame.target_y)\nstatus = None if frame.status is None else frame.status & 16 | (8 if frame.target_y & 2147483648 else 0) | (4 if frame.target_y == 0 else 0)\nframe = first_replace(frame, status=status)\ntroops = memory.table(4294952960).cursor()\nframe = first_replace(frame, roster=troops)\nactor = memory.table(4294964210).word()\nframe = _first_word(frame, 'target_x', actor)\nframe = _first_shift_word(frame, 'target_x', actor, 2)\nframe = _damage_store(memory, frame, 16727762, troops.long(u16(actor << 2)), 32)\nframe = _damage_store(memory, frame, 16727766, 1792)\nopposing = memory.table(4294964134).word()\nframe = _first_memory_word(frame, opposing)\nif not negative_word(opposing):\n    frame = _presentation_call_fields(memory, frame, 99434, sample_battle_special_status_factor_fields)\n    frame = _presentation_call_fields(memory, frame, 99440, _damage_potential_fields)\n    frame = _damage_apply_mutual_losses_fields(memory, frame)\nframe = _presentation_call_fields(memory, frame, 99674, award_city_reserve_attrition_fields)\naward = frame.target_x\nactor = memory.table(4294964210).word()\nframe = _first_word(frame, 'unit', actor)\nframe = _first_shift_word(frame, 'unit', actor, 1)\nprogress = memory.table(4294950400).cursor()\nframe = first_replace(frame, roster=progress)\nframe = _damage_raise_ability_fields(memory, frame, progress, u16(actor << 1), low16(award))\nframe, visible = _damage_visible_owner(memory, frame)\nif visible:\n    mode = memory.table(4294964754).word()\n    frame = _first_compare_word(frame, mode, 1041)\n    if mode != 1041:\n        frame = _damage_store(memory, frame, 16740390, 24)\n        frame = _damage_external_call(memory, frame, 67372, 99756)\nreturn (memory.finish(frame), award)"}})


# Entire sole secondary_roster_has_terrain_six_carry current field body.
DECLARATIONS.update({'secondary_roster_has_terrain_six_carry': {'signature': 'state: GameplayState', 'returns': None, 'flow': 'checked_state(state)\n_, selected = secondary_roster_has_terrain_six_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())\nreturn state.carry_observed(int(selected))'}})


# Entire sole secondary_roster_has_terrain_six_fields current field body.
DECLARATIONS.update({'secondary_roster_has_terrain_six_fields': {'signature': 'memory, frame', 'returns': None, 'flow': "frame = _presentation_frame(memory, frame)\nnames = ('target_x', 'target_y', 'unit', 'count', 'roster', 'candidates', 'controller')\nframe, saved = _damage_save_longs(memory, frame, names)\nframe = _presentation_call_fields(memory, frame, 100110, _damage_map_fields)\nroster = memory.table(4294944164).cursor()\npositions = memory.table(4294943056).cursor()\nframe = first_replace(frame, candidates=roster, controller=positions)\nselected = False\nwhile True:\n    member = roster.next_word()\n    frame = _first_word(frame, 'count', member)\n    if negative_word(member):\n        break\n    offset = u16(member << 2)\n    frame = _first_shift_word(frame, 'count', member, 2)\n    x = positions.word(offset)\n    frame = _first_word(frame, 'target_y', x)\n    frame = _first_right_word(frame, 'target_y', x, 7)\n    y = positions.word(offset, 2)\n    frame = _first_word(frame, 'unit', y)\n    frame = _first_right_word(frame, 'unit', y, 7)\n    frame, category = _damage_terrain_fields(memory, frame, x >> 7, y >> 7, 100142)\n    from ..high_level_battle_ai.business_actions import _deployment_compare_byte\n    frame = _deployment_compare_byte(memory, frame, category, 6)\n    if category == 6:\n        selected = True\n        break\nframe = _damage_restore_longs(memory, frame, names, saved)\nmemory.finish(frame)\nmemory.state.set_status_word(memory.state.read_status_word() & 65534 | int(selected))\nreturn (first_replace(frame, status=memory.state.sr & 31), selected)"}})

APPROVED.setdefault('business_movement_support', set()).update({'_movement_address_carrier', '_movement_restore_longs', '_movement_save_longs', 'present_battle_message_fields', '_movement_arithmetic_long'})

APPROVED.setdefault('business_city', set()).update({'_special_action_shift_long', '_city_movement_divide'})

APPROVED.setdefault('business_actions', set()).update({'_battle_action_map_fields', '_deployment_compare_byte', '_deployment_terrain_lookup'})

APPROVED.setdefault('business_formation', set()).update({'_first_sub_word'})

APPROVED.setdefault('contexts_policy_memory', set()).update({'BattlePolicyMemory'})

APPROVED.setdefault('business_reuse', set()).update({'read_battlefield_terrain_type_observations'})

APPROVED.setdefault('business_services', set()).update({'load_gameplay_scene_fields'})

APPROVED.setdefault('contexts_services', set()).update({'SceneRefreshMemory'})


# Entire sole _postbattle_candidates_fields current body.
DECLARATIONS.update({'_postbattle_candidates_fields': {'signature': 'memory, frame, battlefield, continuation=None', 'returns': None, 'flow': "frame = _presentation_frame(memory, frame)\nif continuation is not None and frame.stack_cursor is not None:\n    stack = frame.stack_cursor.advance(-4)\n    stack.set_long(0, continuation)\n    frame = first_replace(frame, stack_cursor=stack)\nsource = memory.table(4294942800 if battlefield else 4294953984).cursor()\ndestination = memory.table(4294955776).cursor()\nframe = first_replace(frame, roster=source, candidates=destination)\ncity = memory.table(4294964874).word()\nif battlefield:\n    assignments = memory.table(4294953984).cursor()\n    frame = first_replace(frame, controller=assignments)\n    frame = _first_word(frame, 'target_x', city)\n    index_name, city_name = ('unit', 'target_x')\nelse:\n    index_name, city_name = ('target_y', 'unit')\nframe = _first_word(frame, index_name, 255)\nif not battlefield:\n    frame = _first_word(frame, city_name, city)\nframe = _first_word(frame, 'count', 0)\ncount = 0\nfor officer in descending_inclusive(255):\n    assigned = source.byte(officer)\n    frame = _postbattle_compare_byte_fields(frame, low8(city), assigned)\n    selected = assigned == low8(city)\n    if selected and battlefield:\n        assignment = assignments.byte(officer)\n        frame = _postbattle_memory_byte_fields(frame, assignment)\n        selected = not negative_byte(assignment)\n    if selected:\n        destination.set_word(0, officer)\n        destination = destination.advance(2)\n        frame = first_replace(frame, candidates=destination)\n        frame = _first_memory_word(frame, officer)\n        frame = _first_add_word(frame, 'count', count, 1)\n        count = u16(count + 1)\n    frame = _postbattle_decrement_fields(frame, index_name, officer)\ndestination.set_word(0, 65535)\nframe = _first_memory_word(frame, 65535)\nif continuation is not None and frame.stack_cursor is not None:\n    actual = frame.stack_cursor.long()\n    if actual != continuation:\n        raise Boundary('actual postbattle candidate return changed to ' + str(actual))\n    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(4))\nreturn (memory.finish(frame), count)"}})


# Entire sole _postbattle_city_resource_fields current body.
DECLARATIONS.update({'_postbattle_city_resource_fields': {'signature': "memory, frame, address, index_name='target_y'", 'returns': None, 'flow': 'view = memory.table(address).cursor()\nframe = first_replace(frame, roster=view)\ncity = memory.table(4294964874).word()\nframe = _first_word(frame, index_name, city)\nframe = _first_shift_word(frame, index_name, city, 2)\nreturn (frame, view, u16(city << 2))'}})


# Entire sole _postbattle_compare_byte_fields current body.
DECLARATIONS.update({'_postbattle_compare_byte_fields': {'signature': 'frame, left, right', 'returns': None, 'flow': 'left, right = (u8(left), u8(right))\nvalue = u8(left - right)\noverflow = bool((left ^ right) & (left ^ value) & 128)\nstatus = None if frame.status is None else frame.status & 16 | (1 if left < right else 0) | (8 if value & 128 else 0) | (4 if value == 0 else 0) | (2 if overflow else 0)\nreturn first_replace(frame, status=status)'}})


# Entire sole _postbattle_decrement_fields current body.
DECLARATIONS.update({'_postbattle_decrement_fields': {'signature': 'frame, name, value', 'returns': None, 'flow': 'retained = frame.carrier(name)\nresult = None if retained is None else replace_word(retained, u16(value - 1))\nreturn first_replace(frame, **{name: result})'}})


# Entire sole _postbattle_fraction_fields current body.
DECLARATIONS.update({'_postbattle_fraction_fields': {'signature': 'memory, frame, multiplier, base, continuation', 'returns': None, 'flow': "frame = _presentation_call_fields(memory, frame, continuation, _presentation_random_fields)\nif multiplier == 501:\n    frame = _first_long(frame, 'target_x', low16(frame.target_x) * 501)\nelse:\n    frame = _first_long(frame, 'target_x', frame.target_x & 65535)\n    if multiplier != 16:\n        frame = _first_long(frame, 'target_y', frame.target_x)\n    if multiplier in (13, 25, 51, 6):\n        frame = _damage_shift_long(memory, frame, 'target_x', 1)\n        frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)\n        frame = _damage_shift_long(memory, frame, 'target_x', 2 if multiplier == 13 else 1 if multiplier == 6 else 3)\n        if multiplier != 6:\n            frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)\n        if multiplier == 51:\n            frame = _damage_shift_long(memory, frame, 'target_x', 1)\n            frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)\n    elif multiplier == 31:\n        frame = _damage_shift_long(memory, frame, 'target_x', 5)\n        frame = _presentation_sub_long_fields(frame, 'target_x', frame.target_x, frame.target_y)\n    elif multiplier == 11:\n        frame = _damage_shift_long(memory, frame, 'target_x', 2)\n        frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)\n        frame = _damage_shift_long(memory, frame, 'target_x', 1)\n        frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)\n    elif multiplier == 16:\n        frame = _damage_shift_long(memory, frame, 'target_x', 4)\n    else:\n        raise ValueError('closed original postbattle scale required')\nframe = _first_long(frame, 'target_x', swap_words(frame.target_x))\nif base:\n    frame = _first_add_word(frame, 'target_x', low16(frame.target_x), base)\nreturn frame"}})


# Entire sole _postbattle_gold_debit_fields current body.
DECLARATIONS.update({'_postbattle_gold_debit_fields': {'signature': 'memory, frame, continuation, word_borrow', 'returns': None, 'flow': "frame = _postbattle_fraction_fields(memory, frame, 501, 500, continuation)\nframe, gold, offset = _postbattle_city_resource_fields(memory, frame, 4294959100)\noriginal = gold.long(offset)\nframe = _first_long(frame, 'unit', original)\nframe = _first_long(frame, 'target_x', frame.target_x & 65535)\ncost = frame.target_x\nif word_borrow:\n    from ..high_level_battle_ai.business_formation import _first_sub_word\n    frame = _first_sub_word(frame, 'unit', low16(original), low16(cost))\n    insufficient = low16(original) < low16(cost)\nelse:\n    frame = _presentation_sub_long_fields(frame, 'unit', original, cost)\n    insufficient = original < cost\nif insufficient:\n    frame = _first_long(frame, 'unit', 0)\ngold.set_long(offset, frame.unit)\nreturn _first_long(frame, 'unit', frame.unit)"}})


# Entire sole _postbattle_loss_fields current body.
DECLARATIONS.update({'_postbattle_loss_fields': {'signature': 'frame, amount, divisor, instruction', 'returns': None, 'flow': "frame = _first_long(frame, 'target_x', low16(frame.target_x) * low16(amount))\nreturn _damage_divide(frame, 'target_x', divisor, instruction)"}})


# Entire sole _postbattle_memory_byte_fields current body.
DECLARATIONS.update({'_postbattle_memory_byte_fields': {'signature': 'frame, value', 'returns': None, 'flow': 'value = u8(value)\nstatus = None if frame.status is None else frame.status & 16 | (8 if value & 128 else 0) | (4 if value == 0 else 0)\nreturn first_replace(frame, status=status)'}})


# Entire sole apply_assigned_city_light_attrition current body.
DECLARATIONS.update({'apply_assigned_city_light_attrition': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\napply_assigned_city_light_attrition_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())'}})


# Entire sole apply_assigned_city_light_attrition_fields current body.
DECLARATIONS.update({'apply_assigned_city_light_attrition_fields': {'signature': 'memory, frame', 'returns': None, 'flow': "frame, _ = _postbattle_candidates_fields(memory, frame, False, 116386)\nroster = memory.table(4294955776).cursor()\ntroops, readiness = (memory.table(4294952960).cursor(), memory.table(4294947328).cursor())\nframe = first_replace(frame, roster=roster, candidates=troops, controller=readiness, scan=memory.table(4294950912).cursor(), opponent=memory.table(4294952704).cursor(), scratch=memory.table(4294953984).cursor(), auxiliary=memory.table(4294964318).cursor())\nframe = _first_word(frame, 'choice', 0)\ntotal = 0\nfrom ..high_level_battle_ai.business_formation import _first_sub_word\nwhile True:\n    member = roster.word()\n    roster = roster.advance(2)\n    frame = first_replace(frame, roster=roster)\n    frame = _first_word(frame, 'unit', member)\n    if negative_word(member):\n        memory.table(4294963130).set_word(0, total)\n        return memory.finish(_first_memory_word(frame, total))\n    frame = _first_shift_word(frame, 'unit', member, 2)\n    offset = u16(member << 2)\n    original = troops.long(offset)\n    frame = _first_long(frame, 'count', original)\n    frame = _postbattle_fraction_fields(memory, frame, 31, 30, 116434)\n    frame = _postbattle_loss_fields(frame, original, 100, 116454)\n    frame = _first_sub_word(frame, 'count', low16(original), low16(frame.target_x))\n    troops.set_word(offset, low16(frame.count), 2)\n    frame = _first_memory_word(frame, low16(frame.count))\n    frame = _first_long(frame, 'target_x', frame.target_x & 65535)\n    frame = _damage_divide(frame, 'target_x', 400, 116470)\n    frame = _first_add_word(frame, 'choice', total, low16(frame.target_x))\n    total = u16(total + low16(frame.target_x))\n    frame = _first_right_word(frame, 'unit', offset, 1)\n    offset >>= 1\n    original = readiness.word(offset)\n    frame = _first_word(frame, 'count', original)\n    frame = _postbattle_fraction_fields(memory, frame, 31, 0, 116488)\n    frame = _postbattle_loss_fields(frame, original, 100, 116504)\n    frame = _first_sub_word(frame, 'count', original, low16(frame.target_x))\n    remaining = u16(original - low16(frame.target_x))\n    if remaining == 0:\n        remaining = 1\n        frame = _first_word(frame, 'count', remaining)\n    readiness.set_word(offset, remaining)\n    frame = _first_memory_word(frame, remaining)"}})


# Entire sole apply_postbattle_city_economic_attrition current body.
DECLARATIONS.update({'apply_postbattle_city_economic_attrition': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\napply_postbattle_city_economic_attrition_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())'}})


# Entire sole apply_postbattle_city_economic_attrition_fields current body.
DECLARATIONS.update({'apply_postbattle_city_economic_attrition_fields': {'signature': 'memory, frame', 'returns': None, 'flow': "frame = _presentation_frame(memory, frame)\nframe = _postbattle_fraction_fields(memory, frame, 16, 5, 137166)\ncity = memory.table(4294964874).word()\nframe = _first_word(frame, 'unit', city)\nframe = _first_shift_word(frame, 'unit', city, 2)\noffset = u16(city << 2)\nfrom ..high_level_battle_ai.business_formation import _first_sub_word\nfor address, second in ((4294959580, False), (4294959420, True)):\n    if second:\n        frame = _postbattle_fraction_fields(memory, frame, 11, 0, 137214)\n    target = memory.table(address).cursor()\n    frame = first_replace(frame, roster=target)\n    original = target.long(offset)\n    frame = _first_long(frame, 'count', original)\n    frame = _first_long(frame, 'distance', original)\n    frame = _first_long(frame, 'distance', low16(original) * low16(frame.target_x))\n    frame = _damage_divide(frame, 'distance', 100, 137244 if second else 137198)\n    frame = _first_sub_word(frame, 'count', low16(original), low16(frame.distance))\n    target.set_long(offset, frame.count)\n    frame = _first_long(frame, 'count', frame.count)\nframe = _postbattle_fraction_fields(memory, frame, 6, 5, 137260)\ntarget = memory.table(4294959900).cursor()\nframe = first_replace(frame, roster=target)\noriginal = target.word(offset, 2)\nframe = _first_word(frame, 'count', original)\nloss = low16(frame.target_x)\nframe = _first_sub_word(frame, 'count', original, loss)\nif original < loss:\n    frame = _first_word(frame, 'count', 0)\ntarget.set_word(offset, low16(frame.count), 2)\nreturn memory.finish(_first_memory_word(frame, low16(frame.count)))"}})


# Entire sole build_battlefield_outcome_candidates_fields current body.
DECLARATIONS.update({'build_battlefield_outcome_candidates_fields': {'signature': 'memory, frame', 'returns': None, 'flow': 'return _postbattle_candidates_fields(memory, frame, True)'}})


# Entire sole build_city_assigned_outcome_candidates_fields current body.
DECLARATIONS.update({'build_city_assigned_outcome_candidates_fields': {'signature': 'memory, frame', 'returns': None, 'flow': 'return _postbattle_candidates_fields(memory, frame, False)'}})


# Entire sole clear_city_officer_links current body.
DECLARATIONS.update({'clear_city_officer_links': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\nclear_city_officer_links_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())'}})


# Entire sole clear_city_officer_links_fields current body.
DECLARATIONS.update({'clear_city_officer_links_fields': {'signature': 'memory, frame', 'returns': None, 'flow': "frame = _presentation_frame(memory, frame)\ncity = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_x', city)\nlinks = memory.table(4294942800).cursor()\nframe = first_replace(frame, roster=links)\nframe = _first_word(frame, 'target_y', 255)\nfor officer in descending_inclusive(255):\n    value = links.byte(officer)\n    frame = _postbattle_compare_byte_fields(frame, low8(city), value)\n    if value == low8(city):\n        links.byte(officer)\n        links.set_byte(officer, 0)\n        frame = _postbattle_memory_byte_fields(frame, 0)\n    frame = _postbattle_decrement_fields(frame, 'target_y', officer)\nreturn memory.finish(frame)"}})


# Entire sole consume_city_battle_supply_long current body.
DECLARATIONS.update({'consume_city_battle_supply_long': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\nconsume_city_battle_supply_long_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())'}})


# Entire sole consume_city_battle_supply_long_fields current body.
DECLARATIONS.update({'consume_city_battle_supply_long_fields': {'signature': 'memory, frame', 'returns': None, 'flow': "frame = _presentation_frame(memory, frame)\namount = memory.table(4294963132).word()\nframe = _first_word(frame, 'target_x', amount)\nframe = _first_long(frame, 'target_x', amount * 90)\nframe, supply, offset = _postbattle_city_resource_fields(memory, frame, 4294962564)\noriginal = supply.long(offset)\nframe = _first_long(frame, 'unit', original)\nframe = _postbattle_loss_fields(frame, original, 1000, 116554)\nloss = frame.target_x\nframe = _presentation_sub_long_fields(frame, 'unit', original, loss)\nif original < loss:\n    frame = _first_long(frame, 'unit', 0)\nsupply.set_long(offset, frame.unit)\nframe = _first_long(frame, 'unit', frame.unit)\nreturn memory.finish(_postbattle_gold_debit_fields(memory, frame, 116576, False))"}})


# Entire sole consume_city_battle_supply_word current body.
DECLARATIONS.update({'consume_city_battle_supply_word': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\nconsume_city_battle_supply_word_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())'}})


# Entire sole consume_city_battle_supply_word_fields current body.
DECLARATIONS.update({'consume_city_battle_supply_word_fields': {'signature': 'memory, frame', 'returns': None, 'flow': "frame = _presentation_frame(memory, frame)\nframe = _postbattle_fraction_fields(memory, frame, 25, 50, 116682)\nframe, supply, offset = _postbattle_city_resource_fields(memory, frame, 4294962564)\noriginal = supply.long(offset)\nframe = _first_long(frame, 'unit', original)\nframe = _postbattle_loss_fields(frame, original, 100, 116720)\nfrom ..high_level_battle_ai.business_formation import _first_sub_word\nframe = _first_sub_word(frame, 'unit', low16(original), low16(frame.target_x))\nsupply.set_word(offset, low16(frame.unit), 2)\nframe = _first_memory_word(frame, low16(frame.unit))\nreturn memory.finish(_postbattle_gold_debit_fields(memory, frame, 116736, True))"}})


# Entire sole distribute_city_battle_progress current body.
DECLARATIONS.update({'distribute_city_battle_progress': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\ndistribute_city_battle_progress_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())'}})


# Entire sole distribute_city_battle_progress_fields current body.
DECLARATIONS.update({'distribute_city_battle_progress_fields': {'signature': 'memory, frame', 'returns': None, 'flow': "frame, count = _postbattle_candidates_fields(memory, frame, False, 116096)\nbudget = memory.table(4294963128).word()\nframe = _first_word(frame, 'target_x', budget)\nframe = _first_shift_word(frame, 'target_x', budget, 1)\nframe = _first_memory_word(frame, count)\nif count == 0:\n    return memory.finish(frame)\nframe = _first_long(frame, 'target_x', u16(budget << 1))\nframe = _damage_divide(frame, 'target_x', count, 116114)\nroster = memory.table(4294955776).cursor()\nability, progress = (memory.table(4294950912).cursor(), memory.table(4294950400).cursor())\nframe = first_replace(frame, roster=roster, candidates=ability, controller=progress)\nwhile True:\n    member = roster.word()\n    roster = roster.advance(2)\n    frame = first_replace(frame, roster=roster)\n    frame = _first_word(frame, 'target_y', member)\n    if negative_word(member):\n        return memory.finish(frame)\n    frame = _first_shift_word(frame, 'target_y', member, 1)\n    offset = u16(member << 1)\n    current = ability.word(offset)\n    frame = _first_word(frame, 'unit', current)\n    comparison = progress.word(offset)\n    frame = _first_compare_word(frame, current, comparison)\n    destination = ability if current > comparison else progress\n    if current <= comparison:\n        current = progress.word(offset)\n        frame = _first_word(frame, 'unit', current)\n    frame = _first_add_word(frame, 'unit', current, low16(frame.target_x))\n    result = u16(current + low16(frame.target_x))\n    frame = _first_compare_word(frame, result, 999)\n    if result > 999:\n        result = 999\n        frame = _first_word(frame, 'unit', result)\n    destination.set_word(offset, result)\n    frame = _first_memory_word(frame, result)"}})


# Entire sole reassign_city_flagged_officers current body.
DECLARATIONS.update({'reassign_city_flagged_officers': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\nreassign_city_flagged_officers_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())'}})


# Entire sole reassign_city_flagged_officers_fields current body.
DECLARATIONS.update({'reassign_city_flagged_officers_fields': {'signature': 'memory, frame', 'returns': None, 'flow': "frame = _presentation_frame(memory, frame)\nowner = memory.table(4294964878).word()\nframe = _first_word(frame, 'target_x', owner)\nframe = _first_add_word(frame, 'target_x', owner, 41)\ncity = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_y', city)\nretained = frame.target_y\nstatus = None if frame.status is None else frame.status & 27 | (0 if city & 64 else 4)\nframe = first_replace(frame, target_y=None if retained is None else retained | 64, status=status)\nassignments = memory.table(4294953984).cursor()\nframe = first_replace(frame, roster=assignments)\nframe = _first_word(frame, 'unit', 255)\nfor officer in descending_inclusive(255):\n    value = assignments.byte(officer)\n    frame = _postbattle_compare_byte_fields(frame, low8(city | 64), value)\n    if value == low8(city | 64):\n        assignments.set_byte(officer, low8(owner + 41))\n        frame = _postbattle_memory_byte_fields(frame, low8(owner + 41))\n    frame = _postbattle_decrement_fields(frame, 'unit', officer)\nreturn memory.finish(frame)"}})


# Entire sole reduce_city_reserve_after_defeat current body.
DECLARATIONS.update({'reduce_city_reserve_after_defeat': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\nreduce_city_reserve_after_defeat_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())'}})


# Entire sole reduce_city_reserve_after_defeat_fields current body.
DECLARATIONS.update({'reduce_city_reserve_after_defeat_fields': {'signature': 'memory, frame', 'returns': None, 'flow': "frame = _presentation_frame(memory, frame)\nframe = _postbattle_fraction_fields(memory, frame, 51, 0, 116626)\nframe, reserves, offset = _postbattle_city_resource_fields(memory, frame, 4294960540)\noriginal = reserves.long(offset)\nframe = _first_long(frame, 'unit', original)\nframe = _postbattle_loss_fields(frame, original, 100, 116664)\nfrom ..high_level_battle_ai.business_formation import _first_sub_word\nframe = _first_sub_word(frame, 'unit', low16(original), low16(frame.target_x))\nreserves.set_word(offset, low16(frame.unit), 2)\nreturn memory.finish(_first_memory_word(frame, low16(frame.unit)))"}})


# Entire sole sample_city_postbattle_reserve current body.
DECLARATIONS.update({'sample_city_postbattle_reserve': {'signature': 'state: GameplayState', 'returns': 'Long', 'flow': 'checked_state(state)\nframe = sample_city_postbattle_reserve_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())\nreturn frame.target_x'}})


# Entire sole sample_city_postbattle_reserve_fields current body.
DECLARATIONS.update({'sample_city_postbattle_reserve_fields': {'signature': 'memory, frame', 'returns': None, 'flow': 'frame = _presentation_frame(memory, frame)\nframe = _postbattle_fraction_fields(memory, frame, 13, 0, 116058)\nframe, reserves, offset = _postbattle_city_resource_fields(memory, frame, 4294960540)\nreserves.set_word(offset, low16(frame.target_x), 2)\nreturn memory.finish(_first_memory_word(frame, low16(frame.target_x)))'}})

DECLARATIONS.update({'_postbattle_fraction_fields': {'signature': 'memory, frame, multiplier, base, continuation', 'returns': None, 'flow': "frame = _presentation_call_fields(memory, frame, continuation, _presentation_random_fields)\nif multiplier == 501:\n    frame = _first_long(frame, 'target_x', low16(frame.target_x) * 501)\nelse:\n    frame = _first_long(frame, 'target_x', frame.target_x & 65535)\n    if multiplier != 16:\n        frame = _first_long(frame, 'target_y', frame.target_x)\n    if multiplier in (13, 25, 51, 6):\n        frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 1)\n        frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)\n        frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 2 if multiplier == 13 else 1 if multiplier == 6 else 3)\n        if multiplier != 6:\n            frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)\n        if multiplier == 51:\n            frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 1)\n            frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)\n    elif multiplier == 31:\n        frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 5)\n        frame = _presentation_sub_long_fields(frame, 'target_x', frame.target_x, frame.target_y)\n    elif multiplier == 11:\n        frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 2)\n        frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)\n        frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 1)\n        frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)\n    elif multiplier == 16:\n        frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 4)\n    else:\n        raise ValueError('closed original postbattle scale required')\nframe = _first_long(frame, 'target_x', swap_words(frame.target_x))\nif base:\n    frame = _first_add_word(frame, 'target_x', low16(frame.target_x), base)\nreturn frame"}})

DECLARATIONS.update({'_postbattle_shift_long_fields': {'signature': 'memory, frame, name, amount', 'returns': None, 'flow': 'if amount in (3, 5):\n    from ..high_level_remaining_flows.business_city import _settlement_shift_sample_long_fields\n    return _settlement_shift_sample_long_fields(memory.state, frame, name, amount)\nreturn _damage_shift_long(memory, frame, name, amount)'}})

APPROVED.setdefault('business_city',set()).update({'_settlement_shift_sample_long_fields'})

DECLARATIONS.update({'rebuild_city_links_from_primary_roster': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'project_gameplay_arrival_fields(state, 120130)'}})

DECLARATIONS.update({'classify_duel_object_result': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'project_gameplay_arrival_fields(state, 120216)'}})

APPROVED.setdefault('contexts_reuse', set()).add('project_gameplay_arrival_fields')

DECLARATIONS.update({'settle_city_battle_outcome': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\nsettle_city_battle_outcome_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())'}})

DECLARATIONS.update({'_city_outcome_frame_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, entry: int', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_scene_flows.domain import SceneState\nfrom ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary\nfrom ..high_level_main_flows.business_movement_support import _movement_frame\nframe = _presentation_frame(memory, frame)\nif type(memory.state) is not SceneState or any((value is None for value in (frame.target_x, frame.target_y, frame.unit, frame.count, frame.distance, frame.offset_x, frame.offset_y, frame.choice, frame.roster, frame.candidates, frame.controller, frame.scan, frame.opponent, frame.scratch, frame.auxiliary, frame.stack_cursor, frame.status))):\n    raise MovementContinuationBoundary(entry, frame, 'city outcome requires actual retained fields and entry A7, not a zero scalar frame')\nreturn _movement_frame(memory.state, frame)"}})

DECLARATIONS.update({'_city_outcome_child_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, target: int', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary\nif target == 199284:\n    from .contexts_services import SceneRefreshMemory\n    from .business_services import present_gameplay_message_fields\n    return present_gameplay_message_fields(SceneRefreshMemory(memory.state), frame)\nif target == 115814:\n    return consume_city_battle_resources_fields(memory, frame)\nif target == 115138:\n    return compute_outcome_force_ratio_fields(memory, frame)\nif target == 115360:\n    return build_city_assigned_outcome_candidates_fields(memory, frame)[0]\nif target == 115400:\n    return build_battlefield_outcome_candidates_fields(memory, frame)[0]\nif target == 218976:\n    from ..high_level_main_flows.business_movement_support import signed_divmod_fields\n    return signed_divmod_fields(memory.state, frame)\nif target == 116092:\n    return distribute_city_battle_progress_fields(memory, frame)\nif target == 116052:\n    return sample_city_postbattle_reserve_fields(memory, frame)\nif target == 116382:\n    return apply_assigned_city_light_attrition_fields(memory, frame)\nif target == 116530:\n    return consume_city_battle_supply_long_fields(memory, frame)\nif target == 116620:\n    return reduce_city_reserve_after_defeat_fields(memory, frame)\nif target == 116676:\n    return consume_city_battle_supply_word_fields(memory, frame)\nif target == 117908:\n    return reassign_city_flagged_officers_fields(memory, frame)\nif target == 137160:\n    return apply_postbattle_city_economic_attrition_fields(memory, frame)\nif target == 117878:\n    return clear_city_officer_links_fields(memory, frame)\nraise MovementContinuationBoundary(target, frame, 'city outcome child needs its actual field/nonlocal-return ABI')"}})

DECLARATIONS.update({'_city_outcome_call_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, target: int, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _city_outcome_frame_fields(memory, frame, target)\ndef child(actual_memory, entered):\n    return _city_outcome_child_fields(actual_memory, entered, target)\nreturn _presentation_call_fields(memory, frame, continuation, child)'}})

DECLARATIONS.update({'_city_outcome_word_product_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, product: str, scratch: str, factor: int', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_remaining_flows.business_city import _recruitment_stitched_score_product\nif (product, scratch) not in (('target_y', 'distance'), ('unit', 'offset_x'), ('unit', 'count')):\n    raise ValueError('original city outcome product roles required')\nprojected = first_replace(frame, unit=frame.carrier(product), target_x=frame.carrier(scratch))\nprojected = _recruitment_stitched_score_product(memory.state, projected, uint(factor, 16))\nreturn first_replace(frame, **{product: projected.unit, scratch: projected.target_x}, status=projected.status)"}})

DECLARATIONS.update({'_city_outcome_strength_totals_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, defender: bool', 'returns': 'FirstDeploymentFrame', 'flow': "if type(defender) is not bool:\n    raise ValueError('original city/battlefield strength role required')\nif not defender:\n    frame = _first_long(frame, 'target_y', 0)\n    frame = _first_word(frame, 'unit', 0)\n    frame = _first_word(frame, 'count', 0)\n    frame = first_replace(frame, roster=memory.table(4294952960).cursor(), candidates=memory.table(4294947840).cursor(), controller=memory.table(4294948352), scan=memory.table(4294955776).cursor())\n    index_name, troop_name, first_name, second_name = ('distance', 'target_y', 'unit', 'count')\n    source, troops, first, second = (frame.scan, frame.roster, frame.candidates, frame.controller)\nelse:\n    frame = first_replace(frame, roster=memory.table(4294955776).cursor(), candidates=memory.table(4294952960).cursor(), controller=memory.table(4294947840), scan=memory.table(4294948352).cursor())\n    frame = _first_long(frame, 'unit', 0)\n    frame = _first_word(frame, 'count', 0)\n    frame = _first_word(frame, 'distance', 0)\n    index_name, troop_name, first_name, second_name = ('offset_x', 'unit', 'count', 'distance')\n    source, troops, first, second = (frame.roster, frame.candidates, frame.controller, frame.scan)\nwhile True:\n    member = source.word()\n    source = source.advance(2)\n    frame = first_replace(frame, **{'roster' if defender else 'scan': source})\n    frame = _first_word(frame, index_name, member)\n    if negative_word(member):\n        return frame\n    frame = _first_shift_word(frame, index_name, member, 1)\n    offset = u16(member << 1)\n    frame = _first_add_word(frame, first_name, low16(frame.carrier(first_name)), first.word(offset))\n    frame = _first_add_word(frame, second_name, low16(frame.carrier(second_name)), second.word(offset))\n    frame = _first_shift_word(frame, index_name, offset, 1)\n    frame = _damage_add_long(memory, frame, troop_name, troops.long(u16(offset << 1)))"}})

DECLARATIONS.update({'_city_outcome_scale_troops_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, carrier: str', 'returns': 'FirstDeploymentFrame', 'flow': "if carrier not in ('target_y', 'unit'):\n    raise ValueError('actual city outcome troop carrier required')\noriginal = uint(frame.carrier(carrier), 32)\nvalue = original >> 5\nstatus = (17 if original & 16 else 0) | (4 if value == 0 else 0)\nreturn memory.finish(first_replace(frame, **{carrier: value}, status=status))"}})

DECLARATIONS.update({'compute_outcome_force_ratio_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 115138)\nframe = _postbattle_fraction_fields(memory, frame, 6, 10, 115144)\nframe = _city_outcome_call_fields(memory, frame, 115360, 115168)\nframe = _city_outcome_strength_totals_fields(memory, frame, False)\nframe = _first_add_word(frame, 'target_y', low16(frame.target_y), 1)\nframe = _city_outcome_scale_troops_fields(memory, frame, 'target_y')\nframe = _first_right_word(frame, 'unit', low16(frame.unit), 3)\nframe = _first_right_word(frame, 'count', low16(frame.count), 3)\nframe = _first_add_word(frame, 'unit', low16(frame.unit), 1)\nframe = _first_add_word(frame, 'count', low16(frame.count), 1)\nframe = _city_outcome_word_product_fields(memory, frame, 'target_y', 'distance', low16(frame.unit))\nframe = _city_outcome_word_product_fields(memory, frame, 'target_y', 'distance', low16(frame.count))\nframe = _city_outcome_word_product_fields(memory, frame, 'target_y', 'distance', low16(frame.target_x))\nframe = _city_outcome_call_fields(memory, frame, 115400, 115266)\nframe = _city_outcome_strength_totals_fields(memory, frame, True)\nframe = _city_outcome_scale_troops_fields(memory, frame, 'unit')\nframe = _first_right_word(frame, 'count', low16(frame.count), 3)\nframe = _first_right_word(frame, 'distance', low16(frame.distance), 3)\nframe = _first_add_word(frame, 'unit', low16(frame.unit), 1)\nframe = _first_add_word(frame, 'count', low16(frame.count), 1)\nframe = _first_add_word(frame, 'distance', low16(frame.distance), 1)\nframe = _city_outcome_word_product_fields(memory, frame, 'unit', 'offset_x', low16(frame.count))\nframe = _city_outcome_word_product_fields(memory, frame, 'unit', 'offset_x', low16(frame.count))\nframe = _city_outcome_call_fields(memory, frame, 218976, 115354)\nmemory.table(4294963132).set_word(0, low16(frame.target_y))\nreturn memory.finish(_first_memory_word(frame, low16(frame.target_y)))"}})

DECLARATIONS.update({'_city_outcome_assigned_troops_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "city = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_x', city)\nframe = _first_word(frame, 'target_y', 255)\nframe = _first_long(frame, 'unit', 0)\nfor officer in descending_inclusive(255):\n    assigned = frame.candidates.byte(officer)\n    frame = _postbattle_compare_byte_fields(frame, low8(city), assigned)\n    if assigned == low8(city):\n        frame = _first_word(frame, 'count', officer)\n        frame = _first_shift_word(frame, 'count', officer, 2)\n        frame = _damage_add_long(memory, frame, 'unit', frame.roster.long(u16(officer << 2)))\n        frame = _damage_add_long(memory, frame, 'unit', 100)\n    frame = _postbattle_decrement_fields(frame, 'target_y', officer)\nreturn frame"}})

DECLARATIONS.update({'consume_city_battle_resources_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 115814)\nframe = first_replace(frame, roster=memory.table(4294952960).cursor(), candidates=memory.table(4294942800).cursor())\nframe = _city_outcome_assigned_troops_fields(memory, frame)\nframe = _postbattle_fraction_fields(memory, frame, 11, 10, 115864)\nframe = _city_outcome_word_product_fields(memory, frame, 'unit', 'count', low16(frame.target_x))\nframe = _damage_divide(frame, 'unit', 500, 115898)\nframe = first_replace(frame, controller=memory.table(4294962724))\ncity = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_x', city)\nframe = _first_shift_word(frame, 'target_x', city, 2)\nresource = frame.controller.long(u16(city << 2))\nframe = _first_long(frame, 'target_y', resource)\nframe = _first_long(frame, 'unit', frame.unit & 65535)\nframe = _presentation_sub_long_fields(frame, 'target_y', resource, frame.unit)\nif frame.status & 1:\n    frame = _first_long(frame, 'target_y', 0)\nframe.controller.set_long(u16(city << 2), frame.target_y)\nframe = _first_long(frame, 'target_y', frame.target_y)\nframe = first_replace(frame, candidates=memory.table(4294953984).cursor())\nframe = _city_outcome_assigned_troops_fields(memory, frame)\nframe = _postbattle_fraction_fields(memory, frame, 11, 10, 115980)\nframe = _city_outcome_word_product_fields(memory, frame, 'unit', 'count', low16(frame.target_x))\nframe = _damage_divide(frame, 'unit', 500, 116014)\nframe = _first_long(frame, 'unit', frame.unit & 65535)\nframe = first_replace(frame, controller=memory.table(4294959260))\ncity = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_x', city)\nframe = _first_shift_word(frame, 'target_x', city, 2)\nresource = frame.controller.long(u16(city << 2))\nframe = _first_long(frame, 'count', resource)\nframe = _presentation_sub_long_fields(frame, 'count', resource, frame.unit)\nif frame.status & 1:\n    frame = _first_long(frame, 'count', 0)\nframe.controller.set_long(u16(city << 2), frame.count)\nreturn memory.finish(_first_long(frame, 'count', frame.count))"}})

DECLARATIONS.update({'_city_outcome_store_word_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, address: int, value: int, clear: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': 'view = memory.table(address)\nif clear:\n    view.word()\nview.set_word(0, uint(value, 16))\nreturn memory.finish(_first_memory_word(frame, value))'}})

DECLARATIONS.update({'_city_outcome_head_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = first_replace(frame, roster=memory.table(4294960704).cursor())\nowner = memory.table(4294964876).word()\nframe = _first_word(frame, 'target_x', owner)\nframe = _first_shift_word(frame, 'target_x', owner, 1)\nframe = _city_outcome_store_word_fields(memory, frame, 4294964176, frame.roster.word(u16(owner << 1)))\nowner = memory.table(4294964878).word()\nframe = _first_word(frame, 'target_x', owner)\nframe = _first_shift_word(frame, 'target_x', owner, 1)\nreturn _city_outcome_store_word_fields(memory, frame, 4294964178, frame.roster.word(u16(owner << 1)))"}})

DECLARATIONS.update({'_city_outcome_notify_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, initial: bool, conquered: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': "if type(initial) is not bool or type(conquered) is not bool:\n    raise ValueError('original outcome notification arm required')\nframe = _city_outcome_head_fields(memory, frame)\nif not initial:\n    frame = _city_outcome_store_word_fields(memory, frame, 4294964806, memory.table(4294964874).word())\nsaved = memory.table(4294964066).word()\nstack = frame.stack_cursor.advance(-2)\nstack.set_word(0, saved)\nframe = first_replace(frame, stack_cursor=stack)\nframe = _first_memory_word(frame, saved)\nmessage = 159 if initial else 161 if conquered else 162\nframe = _city_outcome_store_word_fields(memory, frame, 4294965056, message)\nif initial:\n    frame = _city_outcome_store_word_fields(memory, frame, 4294964066, 0, True)\nframe = _city_outcome_store_word_fields(memory, frame, 4294964744, 300)\nframe = _city_outcome_store_word_fields(memory, frame, 4294964066, 0, True)\ncontinuation = 114796 if initial else 114916 if conquered else 115018\nframe = _city_outcome_call_fields(memory, frame, 199284, continuation)\nsaved = frame.stack_cursor.word()\nframe = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\nreturn _city_outcome_store_word_fields(memory, frame, 4294964066, saved)"}})

DECLARATIONS.update({'settle_city_battle_outcome_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 114668)\nframe = _city_outcome_store_word_fields(memory, frame, 4294964050, 32)\nframe = first_replace(frame, roster=memory.table(4294964263).cursor())\ncity = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_x', city)\nframe = _city_outcome_store_word_fields(memory, frame, 4294964878, 0, True)\nvalue = frame.roster.byte(city)\nmemory.table(4294964879).set_byte(0, value)\nframe = _postbattle_memory_byte_fields(frame, value)\nframe = first_replace(frame, roster=memory.table(4294942800).cursor())\nframe = _first_word(frame, 'target_y', 255)\nwhile True:\n    assigned = frame.roster.byte(low16(frame.target_y))\n    frame = _postbattle_compare_byte_fields(frame, low8(frame.target_x), assigned)\n    if frame.status & 4:\n        break\n    remaining = u16(low16(frame.target_y) - 1)\n    frame = first_replace(frame, target_y=replace_word(frame.target_y, remaining))\n    if remaining == 65535:\n        break\nframe = first_replace(frame, roster=memory.table(4294953984).cursor())\nframe = _first_word(frame, 'target_x', 0)\nvalue = frame.roster.byte(low16(frame.target_y))\nfrom ..high_level_battle_ai.business_formation import _first_byte\nframe = _first_byte(frame, 'target_x', value)\nframe = _first_word(frame, 'target_x', low16(frame.target_x) & 63)\nframe = first_replace(frame, roster=memory.table(4294964263).cursor())\nframe = _city_outcome_store_word_fields(memory, frame, 4294964876, 0, True)\nvalue = frame.roster.byte(low16(frame.target_x))\nmemory.table(4294964877).set_byte(0, value)\nframe = _postbattle_memory_byte_fields(frame, value)\nframe = _city_outcome_notify_fields(memory, frame, True)\nframe = _city_outcome_call_fields(memory, frame, 115814, 114804)\nframe = _city_outcome_call_fields(memory, frame, 115138, 114808)\nframe = _first_compare_word(frame, low16(frame.target_y), 10)\nconquered = bool(frame.status & 1)\nif conquered:\n    for target, continuation in ((115452, 114820), (115612, 114824), (116092, 114828), (116194, 114832), (116052, 114836), (116530, 114840), (116780, 114844), (117654, 114848), (117908, 114852)):\n        frame = _city_outcome_call_fields(memory, frame, target, continuation)\n    frame = _city_outcome_store_word_fields(memory, frame, 4294964950, 0, True)\nelse:\n    for target, continuation in ((116206, 114928), (116382, 114932), (116092, 114936), (116194, 114940), (116620, 114944), (116676, 114948), (117512, 114952)):\n        frame = _city_outcome_call_fields(memory, frame, target, continuation)\n    frame = _city_outcome_store_word_fields(memory, frame, 4294964950, 2)\nframe = _city_outcome_notify_fields(memory, frame, False, conquered)\nframe = _city_outcome_call_fields(memory, frame, 137160, 115026)\nframe = _city_outcome_call_fields(memory, frame, 117878, 115030)\ncity = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_x', city)\nframe = first_replace(frame, roster=memory.table(4294961719).cursor())\nframe.roster.byte(city)\nframe.roster.set_byte(city, 0)\nframe = _postbattle_memory_byte_fields(frame, 0)\nframe = _city_outcome_store_word_fields(memory, frame, 4294964754, 513)\nframe = _first_long(frame, 'target_x', 3221225510)\nframe = _first_word(frame, 'target_y', 7)\nframe = _first_word(frame, 'unit', 51714)\nframe = first_replace(frame, roster=memory.table(115110).cursor())\nframe = _city_outcome_call_fields(memory, frame, 158714, 115074)\ncity = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_x', city)\nframe = _first_shift_word(frame, 'target_x', city, 2)\noffset = u16(city << 2)\nfor address in (4294962724, 4294962564):\n    frame = first_replace(frame, roster=memory.table(address).cursor())\n    frame.roster.long(offset)\n    frame.roster.set_long(offset, 0)\n    frame = first_replace(frame, status=frame.status & 16 | 4)\nfor source, destination in ((4294964877, 4294944290), (4294964879, 4294944291)):\n    value = memory.table(source).byte()\n    memory.table(destination).set_byte(0, value)\n    frame = _postbattle_memory_byte_fields(frame, value)\nreturn memory.finish(frame)"}})

APPROVED.setdefault('domain', set()).update({'SceneState'})

APPROVED.setdefault('contexts_gameplay', set()).update({'MovementContinuationBoundary'})

APPROVED.setdefault('business_movement_support', set()).update({'_movement_frame', 'signed_divmod_fields'})

APPROVED.setdefault('business_city', set()).update({'_recruitment_stitched_score_product'})

APPROVED.setdefault('contexts_services', set()).update({'SceneRefreshMemory'})

APPROVED.setdefault('business_services', set()).update({'present_gameplay_message_fields'})

APPROVED.setdefault('business_formation', set()).update({'_first_byte'})


# Entire current sole _city_outcome_child_fields body.
DECLARATIONS.update({'_city_outcome_child_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, target: int', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary\nif target == 115452:\n    return apply_battlefield_ratio_losses_fields(memory, frame)\nif target == 115612:\n    return apply_city_assigned_heavy_losses_fields(memory, frame)\nif target == 116206:\n    return apply_battlefield_heavy_losses_and_detach_fields(memory, frame)\nif target == 116780:\n    return rebuild_primary_after_battle_fields(memory, frame)\nif target == 116924:\n    return sort_returning_officer_status_fields(memory, frame)\nif target == 117058:\n    return partition_city_survivors_fields(memory, frame)\nif target == 117246:\n    return owner_has_other_city_carry_fields(memory, frame)\nif target == 117308:\n    return restore_returning_officer_assignments_fields(memory, frame)\nif target == 117344:\n    return allocate_packed_group_resources_fields(memory, frame)\nif target == 117512:\n    return rebuild_secondary_after_battle_fields(memory, frame)\nif target == 116194:\n    return distribute_battlefield_battle_progress_fields(memory, frame)\nif target == 133326:\n    from .business_reuse import apply_returning_officer_loyalty_fields\n    return apply_returning_officer_loyalty_fields(memory, frame)\nif target == 199284:\n    from .contexts_services import SceneRefreshMemory\n    from .business_services import present_gameplay_message_fields\n    return present_gameplay_message_fields(SceneRefreshMemory(memory.state), frame)\nif target == 115814:\n    return consume_city_battle_resources_fields(memory, frame)\nif target == 115138:\n    return compute_outcome_force_ratio_fields(memory, frame)\nif target == 115360:\n    return build_city_assigned_outcome_candidates_fields(memory, frame)[0]\nif target == 115400:\n    return build_battlefield_outcome_candidates_fields(memory, frame)[0]\nif target == 218976:\n    from ..high_level_main_flows.business_movement_support import signed_divmod_fields\n    return signed_divmod_fields(memory.state, frame)\nif target == 116092:\n    return distribute_city_battle_progress_fields(memory, frame)\nif target == 116052:\n    return sample_city_postbattle_reserve_fields(memory, frame)\nif target == 116382:\n    return apply_assigned_city_light_attrition_fields(memory, frame)\nif target == 116530:\n    return consume_city_battle_supply_long_fields(memory, frame)\nif target == 116620:\n    return reduce_city_reserve_after_defeat_fields(memory, frame)\nif target == 116676:\n    return consume_city_battle_supply_word_fields(memory, frame)\nif target == 117908:\n    return reassign_city_flagged_officers_fields(memory, frame)\nif target == 137160:\n    return apply_postbattle_city_economic_attrition_fields(memory, frame)\nif target == 117878:\n    return clear_city_officer_links_fields(memory, frame)\nraise MovementContinuationBoundary(target, frame, 'city outcome child needs its actual field/nonlocal-return ABI')"}})


# Entire current sole _city_outcome_word_product_fields body.
DECLARATIONS.update({'_city_outcome_word_product_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, product: str, scratch: str, factor: int', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_remaining_flows.business_city import _recruitment_stitched_score_product\nif (product, scratch) not in (('target_y', 'distance'), ('unit', 'offset_x'), ('unit', 'count'), ('target_x', 'target_y')):\n    raise ValueError('original city outcome product roles required')\nprojected = first_replace(frame, unit=frame.carrier(product), target_x=frame.carrier(scratch))\nprojected = _recruitment_stitched_score_product(memory.state, projected, uint(factor, 16))\nreturn first_replace(frame, **{product: projected.unit, scratch: projected.target_x}, status=projected.status)"}})


# Entire current sole _postbattle_bit_fields body.
DECLARATIONS.update({'_postbattle_bit_fields': {'signature': 'frame, present', 'returns': None, 'flow': "if type(present) is not bool:\n    raise ValueError('observed original bit required')\nreturn first_replace(frame, status=None if frame.status is None else frame.status & 27 | (0 if present else 4))"}})


# Entire current sole _postbattle_byte_carrier_fields body.
DECLARATIONS.update({'_postbattle_byte_carrier_fields': {'signature': 'frame, name, value', 'returns': None, 'flow': 'from ..high_level_battle_ai.business_formation import _first_byte\nreturn _first_byte(frame, name, value)'}})


# Entire current sole _postbattle_fraction_fields body.
DECLARATIONS.update({'_postbattle_fraction_fields': {'signature': 'memory, frame, multiplier, base, continuation', 'returns': None, 'flow': "frame = _presentation_call_fields(memory, frame, continuation, _presentation_random_fields)\nif multiplier in (501, 61):\n    frame = _first_long(frame, 'target_x', low16(frame.target_x) * multiplier)\nelse:\n    frame = _first_long(frame, 'target_x', frame.target_x & 65535)\n    if multiplier != 16:\n        frame = _first_long(frame, 'target_y', frame.target_x)\n    if multiplier in (13, 25, 51, 6):\n        frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 1)\n        frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)\n        frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 2 if multiplier == 13 else 1 if multiplier == 6 else 3)\n        if multiplier != 6:\n            frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)\n        if multiplier == 51:\n            frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 1)\n            frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)\n    elif multiplier == 40:\n        frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 2)\n        frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)\n        frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 3)\n    elif multiplier in (30, 60):\n        frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 4)\n        frame = _presentation_sub_long_fields(frame, 'target_x', frame.target_x, frame.target_y)\n        frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 1 if multiplier == 30 else 2)\n    elif multiplier == 31:\n        frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 5)\n        frame = _presentation_sub_long_fields(frame, 'target_x', frame.target_x, frame.target_y)\n    elif multiplier == 11:\n        frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 2)\n        frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)\n        frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 1)\n        frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)\n    elif multiplier == 16:\n        frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 4)\n    else:\n        raise ValueError('closed original postbattle scale required')\nframe = _first_long(frame, 'target_x', swap_words(frame.target_x))\nif base:\n    frame = _first_add_word(frame, 'target_x', low16(frame.target_x), base)\nreturn frame"}})


# Entire current sole _postbattle_loss_roster_fields body.
DECLARATIONS.update({'_postbattle_loss_roster_fields': {'signature': 'memory, frame, profile', 'returns': None, 'flow': "if profile not in ('ratio', 'assigned-heavy', 'battlefield-heavy'):\n    raise ValueError('original postbattle loss profile required')\nassigned = profile == 'assigned-heavy'\nentry = 115612 if assigned else 115452 if profile == 'ratio' else 116206\nframe = _city_outcome_frame_fields(memory, frame, entry)\nframe, _ = _postbattle_candidates_fields(memory, frame, not assigned, entry + (4 if entry != 115452 else 2))\nroster = memory.table(4294955776).cursor()\ntroops = memory.table(4294952960).cursor()\nreadiness = memory.table(4294947328).cursor()\nability = memory.table(4294950912).cursor()\nflags = memory.table(4294952704).cursor()\nassignments = memory.table(4294953984).cursor()\nif profile == 'ratio':\n    frame = first_replace(frame, roster=roster, candidates=troops, controller=readiness, scan=assignments, opponent=ability, scratch=flags)\nelif assigned:\n    frame = first_replace(frame, roster=roster, candidates=troops, controller=readiness, scan=ability, opponent=assignments, scratch=memory.table(4294964318).cursor(), auxiliary=flags)\nelse:\n    frame = first_replace(frame, roster=roster, candidates=troops, controller=readiness, scan=ability, opponent=flags, scratch=assignments)\nframe = _first_word(frame, 'choice', 0)\npoints = 0\nfrom ..high_level_battle_ai.business_formation import _first_sub_word\nwhile True:\n    officer = roster.word()\n    roster = roster.advance(2)\n    frame = first_replace(frame, roster=roster)\n    frame = _first_word(frame, 'unit', officer)\n    if negative_word(officer):\n        destination = 4294963130 if assigned else 4294963128\n        memory.table(destination).set_word(0, points)\n        return memory.finish(_first_memory_word(frame, points))\n    frame = _first_shift_word(frame, 'unit', officer, 2)\n    troop_index = u16(officer << 2)\n    original = troops.long(troop_index)\n    frame = _first_long(frame, 'count', original)\n    troop_token = 115498 if profile == 'ratio' else 115664 if assigned else 116254\n    frame = _postbattle_fraction_fields(memory, frame, 40, 30 if profile == 'ratio' else 50, troop_token)\n    if profile == 'ratio':\n        frame = _first_long(frame, 'target_x', low16(frame.target_x) * memory.table(4294963132).word())\n        frame = _city_outcome_word_product_fields(memory, frame, 'target_x', 'target_y', low16(original))\n        frame = _damage_divide(frame, 'target_x', 1000, 115534)\n    else:\n        frame = _postbattle_loss_fields(frame, original, 100, 115686 if assigned else 116276)\n    frame = _first_sub_word(frame, 'count', low16(original), low16(frame.target_x))\n    troops.set_word(troop_index, low16(frame.count), 2)\n    frame = _first_memory_word(frame, low16(frame.count))\n    frame = _first_long(frame, 'target_x', frame.target_x & 65535)\n    frame = _damage_divide(frame, 'target_x', 400, 115550 if profile == 'ratio' else 115702 if assigned else 116292)\n    frame = _first_add_word(frame, 'choice', points, low16(frame.target_x))\n    points = u16(points + low16(frame.target_x))\n    frame = _first_right_word(frame, 'unit', troop_index, 1)\n    readiness_index = troop_index >> 1\n    original = readiness.word(readiness_index)\n    frame = _first_word(frame, 'count', original)\n    readiness_token = 115568 if profile == 'ratio' else 115720 if assigned else 116310\n    scale = 30 if profile == 'ratio' else 60 if assigned else 61\n    frame = _postbattle_fraction_fields(memory, frame, scale, 0, readiness_token)\n    frame = _postbattle_loss_fields(frame, original, 100, 115586 if profile == 'ratio' else 115738 if assigned else 116318)\n    frame = _first_sub_word(frame, 'count', original, low16(frame.target_x))\n    remaining = low16(frame.count)\n    if profile == 'ratio' and remaining == 0:\n        remaining = 1\n        frame = _first_word(frame, 'count', remaining)\n    readiness.set_word(readiness_index, remaining)\n    frame = _first_memory_word(frame, remaining)\n    if profile == 'ratio':\n        continue\n    frame = _first_compare_word(frame, remaining, 10)\n    if remaining > 10:\n        continue\n    original = ability.word(readiness_index)\n    frame = _first_word(frame, 'count', original)\n    frame = _first_long(frame, 'count', original)\n    frame = _damage_divide(frame, 'count', 5, 115764 if assigned else 116344)\n    frame = _first_right_word(frame, 'unit', readiness_index, 1)\n    officer = readiness_index >> 1\n    if assigned:\n        city = memory.table(4294964874).word()\n        frame = _first_word(frame, 'distance', city)\n        frame = _first_shift_word(frame, 'distance', city, 1)\n        head = frame.scratch.word(u16(city << 1))\n        frame = _first_compare_word(frame, officer, head)\n        if officer == head:\n            frame = _first_add_word(frame, 'count', low16(frame.count), 30)\n    else:\n        assignments.set_byte(officer, 255)\n        frame = _postbattle_memory_byte_fields(frame, 255)\n    marked = flags.byte(officer)\n    frame = _postbattle_bit_fields(frame, bool(marked & 16))\n    if marked & 16:\n        frame = _first_add_word(frame, 'count', low16(frame.count), 20)\n    frame = _first_add_word(frame, 'choice', points, low16(frame.count))\n    points = u16(points + low16(frame.count))"}})


# Entire current sole _postbattle_progress_tail_fields body.
DECLARATIONS.update({'_postbattle_progress_tail_fields': {'signature': 'memory, frame, count', 'returns': None, 'flow': "frame = _first_memory_word(frame, count)\nif count == 0:\n    return memory.finish(frame)\nframe = _first_long(frame, 'target_x', low16(frame.target_x))\nframe = _damage_divide(frame, 'target_x', count, 116114)\nroster = memory.table(4294955776).cursor()\nability, progress = (memory.table(4294950912).cursor(), memory.table(4294950400).cursor())\nframe = first_replace(frame, roster=roster, candidates=ability, controller=progress)\nwhile True:\n    member = roster.word()\n    roster = roster.advance(2)\n    frame = first_replace(frame, roster=roster)\n    frame = _first_word(frame, 'target_y', member)\n    if negative_word(member):\n        return memory.finish(frame)\n    frame = _first_shift_word(frame, 'target_y', member, 1)\n    offset = u16(member << 1)\n    current = ability.word(offset)\n    frame = _first_word(frame, 'unit', current)\n    comparison = progress.word(offset)\n    frame = _first_compare_word(frame, current, comparison)\n    destination = ability if current > comparison else progress\n    if current <= comparison:\n        current = progress.word(offset)\n        frame = _first_word(frame, 'unit', current)\n    frame = _first_add_word(frame, 'unit', current, low16(frame.target_x))\n    result = u16(current + low16(frame.target_x))\n    frame = _first_compare_word(frame, result, 999)\n    if result > 999:\n        result = 999\n        frame = _first_word(frame, 'unit', result)\n    destination.set_word(offset, result)\n    frame = _first_memory_word(frame, result)"}})


# Entire current sole _postbattle_rebuild_rosters_fields body.
DECLARATIONS.update({'_postbattle_rebuild_rosters_fields': {'signature': 'memory, frame, secondary', 'returns': None, 'flow': "if type(secondary) is not bool:\n    raise ValueError('original primary/secondary return flow required')\nentry = 117512 if secondary else 116780\nframe = _city_outcome_frame_fields(memory, frame, entry)\nfirst_target, last_target = (115400, 115360) if secondary else (115360, 115400)\nframe = _city_outcome_call_fields(memory, frame, first_target, entry + 4)\nframe = _city_outcome_call_fields(memory, frame, 117058, entry + 8)\nframe = _city_outcome_call_fields(memory, frame, last_target, entry + 12)\nincoming = low16(frame.count)\nframe = _first_word(frame, 'target_x', incoming)\nexisting = memory.table(4294963130).word()\nframe = _first_add_word(frame, 'target_x', incoming, existing)\ntotal = u16(incoming + existing)\nfrom ..high_level_battle_ai.business_formation import _first_sub_word\nframe = _first_sub_word(frame, 'target_x', total, 10)\nif total > 10:\n    frame = _city_outcome_call_fields(memory, frame, 116924, 117542 if secondary else 116810)\nroster = memory.table(4294946646).cursor()\nframe = first_replace(frame, roster=roster)\nwhile True:\n    officer = roster.word()\n    frame = _first_word(frame, 'target_x', officer)\n    if negative_word(officer):\n        break\n    frame = _postbattle_bit_fields(frame, bool(frame.target_x & 16384))\n    frame = first_replace(frame, target_x=frame.target_x | 16384)\n    roster.set_word(0, low16(frame.target_x))\n    roster = roster.advance(2)\n    frame = first_replace(frame, roster=roster)\n    frame = _first_memory_word(frame, low16(frame.target_x))\nfirst = memory.table(4294946646).word()\nframe = _first_memory_word(frame, first)\nif not negative_word(first):\n    owner = memory.table(4294964877 if secondary else 4294964879).byte()\n    memory.table(4294963170).set_byte(0, owner)\n    frame = _postbattle_memory_byte_fields(frame, owner)\n    frame = _city_outcome_call_fields(memory, frame, 117246, 117578 if secondary else 116846)\n    if not frame.status & 1:\n        if secondary:\n            memory.table(4294964950).word()\n        memory.table(4294964950).set_word(0, 0 if secondary else 2)\n        frame = _first_memory_word(frame, 0 if secondary else 2)\n        frame = _city_outcome_call_fields(memory, frame, 136468, 117592 if secondary else 116862)\n        frame = _city_outcome_call_fields(memory, frame, 117344, 117596 if secondary else 116866)\n    else:\n        if secondary:\n            frame = first_replace(frame, roster=memory.table(4294946646).cursor())\n        city = memory.table(4294964874).word()\n        frame = _first_word(frame, 'target_x', city)\n        frame = _postbattle_bit_fields(frame, bool(frame.target_x & 128))\n        frame = first_replace(frame, target_x=frame.target_x | 128)\n        if not secondary:\n            frame = first_replace(frame, roster=memory.table(4294946646).cursor())\n        frame = first_replace(frame, candidates=memory.table(4294953984).cursor())\n        while True:\n            officer = frame.roster.word()\n            frame = first_replace(frame, roster=frame.roster.advance(2))\n            frame = _first_word(frame, 'target_y', officer)\n            if negative_word(officer):\n                break\n            officer &= 255\n            frame = _first_word(frame, 'target_y', officer)\n            frame.candidates.set_byte(officer, low8(frame.target_x))\n            frame = _postbattle_memory_byte_fields(frame, low8(frame.target_x))\nheads = memory.table(4294960704).cursor()\nframe = first_replace(frame, roster=heads)\nforce = memory.table(4294964878 if secondary else 4294964876).word()\nframe = _first_word(frame, 'target_x', force)\nframe = _first_shift_word(frame, 'target_x', force, 1)\nruler = heads.word(u16(force << 1))\nmemory.table(4294964210).set_word(0, ruler)\nframe = _first_memory_word(frame, ruler)\nframe = _city_outcome_call_fields(memory, frame, 117308, 117652 if secondary else 116922)\nreturn memory.finish(frame)"}})


# Entire current sole allocate_packed_group_resources_fields body.
DECLARATIONS.update({'allocate_packed_group_resources_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 117344)\nfrom ..high_level_main_flows.business_movement_support import _movement_shift_long\nfrom ..high_level_battle_ai.business_formation import _first_sub_word, _first_compare_long\ntroops = memory.table(4294952960).cursor()\nframe = first_replace(frame, candidates=troops)\ncount = frame.roster.byte()\nframe = _postbattle_byte_carrier_fields(frame, 'target_x', count)\nframe = _first_word(frame, 'target_x', count)\nframe = _first_sub_word(frame, 'target_x', count, 1)\nframe = _first_long(frame, 'target_y', 0)\nframe = _first_word(frame, 'unit', 0)\nfor counter in descending_inclusive(u16(count - 1)):\n    officer = frame.roster.byte(counter, 13)\n    frame = _postbattle_byte_carrier_fields(frame, 'unit', officer)\n    frame = _first_shift_word(frame, 'unit', low16(frame.unit), 2)\n    frame = _damage_add_long(memory, frame, 'target_y', troops.long(low16(frame.unit)))\n    frame = _damage_add_long(memory, frame, 'target_y', 100)\n    frame = _postbattle_decrement_fields(frame, 'target_x', counter)\nframe = _first_long(frame, 'unit', frame.target_y)\nframe = _postbattle_shift_long_fields(memory, frame, 'unit', 1)\nframe = _damage_add_long(memory, frame, 'unit', frame.target_y)\nframe = _damage_divide(frame, 'unit', 5, 117386)\nframe = _first_long(frame, 'unit', frame.unit & 65535)\nframe = _first_long(frame, 'count', frame.unit)\ngold, rice = (memory.table(4294962564).cursor(), memory.table(4294962724).cursor())\nframe = first_replace(frame, candidates=gold, controller=rice)\nside = memory.table(4294964951).byte()\nframe = _postbattle_bit_fields(frame, bool(side & 2))\nif side & 2:\n    gold, rice = (memory.table(4294959100).cursor(), memory.table(4294959260).cursor())\n    frame = first_replace(frame, candidates=gold, controller=rice)\ncity = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_x', city)\nframe = _first_shift_word(frame, 'target_x', city, 2)\noffset = u16(city << 2)\nfor view, name in ((gold, 'unit'), (rice, 'count')):\n    available = view.long(offset)\n    frame = _first_long(frame, 'target_y', available)\n    frame = _first_compare_long(frame, available, frame.carrier(name))\n    if available < frame.carrier(name):\n        frame = _first_long(frame, name, available)\n    frame = _presentation_sub_long_fields(frame, 'target_y', frame.target_y, frame.carrier(name))\n    view.set_long(offset, frame.target_y)\n    frame = _first_long(frame, 'target_y', frame.target_y)\nfor name, first in (('unit', 5), ('count', 9)):\n    for displacement in (first + 3, first + 2, first + 1):\n        value = low8(frame.carrier(name))\n        frame.roster.set_byte(0, value, displacement)\n        frame = _postbattle_memory_byte_fields(frame, value)\n        if displacement != first + 1:\n            frame = _movement_shift_long(memory.state, frame, name, True)\n    if name == 'unit':\n        frame = _first_shift_word(frame, name, low16(frame.unit), 8)\n    else:\n        frame = _first_right_word(frame, name, low16(frame.count), 8)\n    value = low8(frame.carrier(name))\n    frame.roster.set_byte(0, value, first)\n    frame = _postbattle_memory_byte_fields(frame, value)\nreturn memory.finish(frame)"}})


# Entire current sole apply_battlefield_heavy_losses_and_detach_fields body.
DECLARATIONS.update({'apply_battlefield_heavy_losses_and_detach_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "return _postbattle_loss_roster_fields(memory, frame, 'battlefield-heavy')"}})


# Entire current sole apply_battlefield_ratio_losses_fields body.
DECLARATIONS.update({'apply_battlefield_ratio_losses_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "return _postbattle_loss_roster_fields(memory, frame, 'ratio')"}})


# Entire current sole apply_city_assigned_heavy_losses_fields body.
DECLARATIONS.update({'apply_city_assigned_heavy_losses_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "return _postbattle_loss_roster_fields(memory, frame, 'assigned-heavy')"}})


# Entire current sole distribute_battlefield_battle_progress_fields body.
DECLARATIONS.update({'distribute_battlefield_battle_progress_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 116194)\nframe, count = _postbattle_candidates_fields(memory, frame, True, 116198)\nbudget = memory.table(4294963130).word()\nframe = _first_word(frame, 'target_x', budget)\nframe = _first_shift_word(frame, 'target_x', budget, 1)\nreturn _postbattle_progress_tail_fields(memory, frame, count)"}})


# Entire current sole distribute_city_battle_progress_fields body.
DECLARATIONS.update({'distribute_city_battle_progress_fields': {'signature': 'memory, frame', 'returns': None, 'flow': "frame, count = _postbattle_candidates_fields(memory, frame, False, 116096)\nbudget = memory.table(4294963128).word()\nframe = _first_word(frame, 'target_x', budget)\nframe = _first_shift_word(frame, 'target_x', budget, 1)\nreturn _postbattle_progress_tail_fields(memory, frame, count)"}})


# Entire current sole owner_has_other_city_carry_fields body.
DECLARATIONS.update({'owner_has_other_city_carry_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 117246)\nsaved = ('target_x', 'target_y', 'unit', 'roster')\nframe, observed = _damage_save_longs(memory, frame, saved)\nowners = memory.table(4294964264).cursor()\nframe = first_replace(frame, roster=owners)\ncity = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_x', city)\nfrom ..high_level_battle_ai.business_formation import _first_sub_word\nframe = _first_sub_word(frame, 'target_x', city, 1)\nexcluded = u16(city - 1)\nframe = _first_word(frame, 'target_y', 39)\nowner = memory.table(4294963170).byte()\nframe = _postbattle_byte_carrier_fields(frame, 'unit', owner)\ncarry = True\nfor candidate in descending_inclusive(39):\n    assigned = owners.byte(candidate)\n    frame = _postbattle_compare_byte_fields(frame, owner, assigned)\n    if owner == assigned:\n        frame = _first_compare_word(frame, candidate, excluded)\n        if candidate != excluded:\n            carry = False\n            break\n    frame = _postbattle_decrement_fields(frame, 'target_y', candidate)\nframe = _damage_restore_longs(memory, frame, saved, observed)\nreturn memory.finish(first_replace(frame, status=frame.status & 30 | int(carry)))"}})


# Entire current sole partition_city_survivors_fields body.
DECLARATIONS.update({'partition_city_survivors_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 117058)\nassignments = memory.table(4294953984).cursor()\nowners = memory.table(4294964263).cursor()\nheads = memory.table(4294960704).cursor()\nframe = first_replace(frame, roster=assignments, candidates=owners, controller=heads)\nfirst = memory.table(4294955776).word()\nframe = _first_word(frame, 'target_x', first)\nframe = _first_word(frame, 'target_y', 0)\ncity = assignments.byte(first)\nframe = _postbattle_byte_carrier_fields(frame, 'target_y', city)\ncity &= 63\nframe = _first_word(frame, 'target_y', city)\nframe = _first_word(frame, 'target_x', 0)\nowner = owners.byte(city)\nframe = _postbattle_byte_carrier_fields(frame, 'target_x', owner)\nmemory.table(4294963170).set_byte(0, owner)\nframe = _postbattle_memory_byte_fields(frame, owner)\nframe = _first_shift_word(frame, 'target_x', owner, 1)\nruler = heads.word(u16(owner << 1))\nframe = _first_word(frame, 'choice', ruler)\nroster = memory.table(4294955776).cursor()\ntroops = memory.table(4294952960).cursor()\nreadiness = memory.table(4294947328).cursor()\nremaining, returning = (memory.table(4294946600).cursor(), memory.table(4294946646).cursor())\nframe = first_replace(frame, roster=roster, candidates=troops, controller=readiness, scan=remaining, opponent=returning, scratch=assignments)\nframe = _first_word(frame, 'unit', 0)\nframe = _first_word(frame, 'count', 0)\nreturn_count, keep_count = (0, 0)\nfrom ..high_level_battle_ai.business_formation import _first_compare_long\nwhile True:\n    officer = roster.word()\n    roster = roster.advance(2)\n    frame = first_replace(frame, roster=roster)\n    frame = _first_word(frame, 'offset_y', officer)\n    if negative_word(officer):\n        remaining.set_word(0, 65535)\n        frame = _first_memory_word(frame, 65535)\n        returning.set_word(0, 65535)\n        frame = _first_memory_word(frame, 65535)\n        memory.table(4294963128).set_word(0, return_count)\n        frame = _first_memory_word(frame, return_count)\n        memory.table(4294963130).set_word(0, keep_count)\n        return memory.finish(_first_memory_word(frame, keep_count))\n    frame = _first_compare_word(frame, officer, ruler)\n    goes_back = False\n    if officer == ruler:\n        frame = _city_outcome_call_fields(memory, frame, 117246, 117204)\n        if frame.status & 1:\n            assignments.set_byte(officer, 255)\n            frame = _postbattle_memory_byte_fields(frame, 255)\n            continue\n        goes_back = True\n    else:\n        frame = _first_word(frame, 'distance', officer)\n        frame = _first_shift_word(frame, 'distance', officer, 2)\n        offset = u16(officer << 2)\n        original = troops.long(offset)\n        frame = _first_compare_long(frame, original, 500)\n        weak = original <= 500\n        if not weak:\n            original = troops.long(offset)\n            frame = _first_compare_long(frame, original, 1000)\n            weak = original <= 1000\n            if weak:\n                frame = _first_right_word(frame, 'distance', offset, 1)\n                resource = readiness.word(offset >> 1)\n                frame = _first_compare_word(frame, resource, 30)\n                weak = resource <= 30\n        if weak:\n            frame = _presentation_call_fields(memory, frame, 117186, _presentation_random_fields)\n            sample = low16(frame.target_x) & 3\n            frame = _first_word(frame, 'target_x', sample)\n            goes_back = sample == 0\n    if goes_back:\n        returning.set_word(0, officer)\n        returning = returning.advance(2)\n        frame = first_replace(frame, opponent=returning)\n        frame = _first_memory_word(frame, officer)\n        frame = _first_add_word(frame, 'unit', return_count, 1)\n        return_count = u16(return_count + 1)\n    else:\n        remaining.set_word(0, officer)\n        remaining = remaining.advance(2)\n        frame = first_replace(frame, scan=remaining)\n        frame = _first_memory_word(frame, officer)\n        frame = _first_add_word(frame, 'count', keep_count, 1)\n        keep_count = u16(keep_count + 1)"}})


# Entire current sole rebuild_primary_after_battle_fields body.
DECLARATIONS.update({'rebuild_primary_after_battle_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _postbattle_rebuild_rosters_fields(memory, frame, False)'}})


# Entire current sole rebuild_secondary_after_battle_fields body.
DECLARATIONS.update({'rebuild_secondary_after_battle_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _postbattle_rebuild_rosters_fields(memory, frame, True)'}})


# Entire current sole restore_returning_officer_assignments_fields body.
DECLARATIONS.update({'restore_returning_officer_assignments_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 117308)\nroster = memory.table(4294946600).cursor()\nassignments = memory.table(4294953984).cursor()\nframe = first_replace(frame, roster=roster, candidates=assignments)\ncity = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_y', city)\nwhile True:\n    officer = frame.roster.word()\n    frame = first_replace(frame, roster=frame.roster.advance(2))\n    frame = _first_word(frame, 'target_x', officer)\n    if negative_word(officer):\n        return memory.finish(frame)\n    frame.candidates.set_byte(officer, low8(frame.target_y))\n    frame = _postbattle_memory_byte_fields(frame, low8(frame.target_y))\n    memory.table(4294964134).set_word(0, low16(frame.target_x))\n    frame = _first_memory_word(frame, low16(frame.target_x))\n    frame = _city_outcome_call_fields(memory, frame, 133326, 117340)"}})


# Entire current sole sort_returning_officer_status_fields body.
DECLARATIONS.update({'sort_returning_officer_status_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 116924)\nfrom ..high_level_main_flows.business_movement_support import _movement_binary_flags\nprevious = memory.table(4294963128).word()\nsurplus = low16(frame.target_x)\nframe, added = _movement_binary_flags(memory.state, frame, previous, surplus, 16)\nmemory.table(4294963128).set_word(0, added)\nsource = memory.table(4294946600).cursor()\nloyalty = memory.table(4294951680).cursor()\nsorted_members = memory.table(4294955776).cursor()\nsorted_status = memory.table(4294955808).cursor()\nframe = first_replace(frame, roster=source, scan=loyalty, candidates=sorted_members, controller=sorted_status)\nmemory.table(4294955776).set_word(0, 65535)\nframe = _first_memory_word(frame, 65535)\nframe = _first_word(frame, 'unit', 0)\nwhile True:\n    frame = _first_word(frame, 'count', 0)\n    member = source.word()\n    source = source.advance(2)\n    frame = first_replace(frame, roster=source)\n    frame = _first_word(frame, 'target_y', member)\n    if negative_word(member):\n        break\n    frame = _postbattle_byte_carrier_fields(frame, 'unit', loyalty.byte(member))\n    index = 0\n    while True:\n        occupied = sorted_members.word(index)\n        frame = _first_memory_word(frame, occupied)\n        if negative_word(occupied):\n            break\n        status = sorted_status.byte(index, 1)\n        frame = _postbattle_compare_byte_fields(frame, low8(frame.unit), status)\n        if low8(frame.unit) > status:\n            break\n        frame = _first_add_word(frame, 'count', index, 2)\n        index = u16(index + 2)\n    while True:\n        displaced = sorted_members.word(index)\n        frame = _first_word(frame, 'distance', displaced)\n        incoming = low16(frame.target_y)\n        sorted_members.set_word(index, incoming)\n        frame = _first_memory_word(frame, incoming)\n        if negative_word(incoming):\n            break\n        old_status = sorted_status.word(index)\n        frame = _first_word(frame, 'offset_x', old_status)\n        sorted_status.set_word(index, low16(frame.unit))\n        frame = _first_memory_word(frame, low16(frame.unit))\n        frame = _first_add_word(frame, 'count', index, 2)\n        index = u16(index + 2)\n        frame = _first_word(frame, 'target_y', low16(frame.distance))\n        frame = _first_word(frame, 'unit', low16(frame.offset_x))\nreturning = memory.table(4294946646).cursor()\nframe = first_replace(frame, roster=returning)\nwhile True:\n    value = returning.word()\n    returning = returning.advance(2)\n    frame = first_replace(frame, roster=returning)\n    frame = _first_memory_word(frame, value)\n    if negative_word(value):\n        break\nreturning = returning.advance(-2)\nframe = first_replace(frame, roster=returning)\nfrom ..high_level_battle_ai.business_formation import _first_sub_word\nframe = _first_sub_word(frame, 'target_x', surplus, 1)\nsource = memory.table(4294955776).cursor()\nframe = first_replace(frame, candidates=source)\nfor counter in descending_inclusive(u16(surplus - 1)):\n    value = source.word()\n    source, returning = (source.advance(2), returning.advance(2))\n    returning.advance(-2).set_word(0, value)\n    frame = first_replace(frame, candidates=source, roster=returning)\n    frame = _first_memory_word(frame, value)\n    frame = _postbattle_decrement_fields(frame, 'target_x', counter)\nreturning.set_word(0, 65535)\nframe = _first_memory_word(frame, 65535)\nremaining = memory.table(4294946600).cursor()\nframe = first_replace(frame, roster=remaining)\nframe = _first_word(frame, 'target_y', 0)\ncount = 0\nwhile True:\n    value = source.word()\n    remaining.set_word(0, value)\n    source, remaining = (source.advance(2), remaining.advance(2))\n    frame = first_replace(frame, candidates=source, roster=remaining)\n    frame = _first_memory_word(frame, value)\n    if negative_word(value):\n        memory.table(4294963130).set_word(0, count)\n        return memory.finish(_first_memory_word(frame, count))\n    frame = _first_add_word(frame, 'target_y', count, 1)\n    count = u16(count + 1)"}})

APPROVED.setdefault('business_movement_support', set()).update({'_movement_shift_long', '_movement_binary_flags'})

APPROVED.setdefault('business_reuse', set()).update({'apply_returning_officer_loyalty_fields'})

APPROVED.setdefault('business_formation', set()).update({'_first_sub_word', '_first_compare_long', '_first_byte'})


# Entire current sole _city_outcome_child_fields body.
DECLARATIONS.update({'_city_outcome_child_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, target: int', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary\nif target == 115452:\n    return apply_battlefield_ratio_losses_fields(memory, frame)\nif target == 115612:\n    return apply_city_assigned_heavy_losses_fields(memory, frame)\nif target == 116206:\n    return apply_battlefield_heavy_losses_and_detach_fields(memory, frame)\nif target == 116780:\n    return rebuild_primary_after_battle_fields(memory, frame)\nif target == 116924:\n    return sort_returning_officer_status_fields(memory, frame)\nif target == 117058:\n    return partition_city_survivors_fields(memory, frame)\nif target == 117246:\n    return owner_has_other_city_carry_fields(memory, frame)\nif target == 117308:\n    return restore_returning_officer_assignments_fields(memory, frame)\nif target == 117344:\n    return allocate_packed_group_resources_fields(memory, frame)\nif target == 117512:\n    return rebuild_secondary_after_battle_fields(memory, frame)\nif target == 116194:\n    return distribute_battlefield_battle_progress_fields(memory, frame)\nif target == 133326:\n    from .business_reuse import apply_returning_officer_loyalty_fields\n    return apply_returning_officer_loyalty_fields(memory, frame)\nif target == 24392:\n    return build_roster_fields(memory, frame)\nif target == 57846:\n    return choose_city_head_fields(memory, frame)\nif target == 57964:\n    return roster_contains_force_head_carry_fields(memory, frame)\nif target == 136468:\n    return append_group_from_survivor_roster_fields(memory, frame)\nif target == 139006:\n    return choose_empty_neighbor_position_fields(memory, frame)\nif target == 117654:\n    return consolidate_city_after_battle_fields(memory, frame)\nif target == 158714:\n    from .contexts_services import SceneRefreshMemory\n    from .business_services import stage_sprite_word_packet_fields\n    return stage_sprite_word_packet_fields(SceneRefreshMemory(memory.state), frame)\nif target == 199284:\n    from .contexts_services import SceneRefreshMemory\n    from .business_services import present_gameplay_message_fields\n    return present_gameplay_message_fields(SceneRefreshMemory(memory.state), frame)\nif target == 115814:\n    return consume_city_battle_resources_fields(memory, frame)\nif target == 115138:\n    return compute_outcome_force_ratio_fields(memory, frame)\nif target == 115360:\n    return build_city_assigned_outcome_candidates_fields(memory, frame)[0]\nif target == 115400:\n    return build_battlefield_outcome_candidates_fields(memory, frame)[0]\nif target == 218976:\n    from ..high_level_main_flows.business_movement_support import signed_divmod_fields\n    return signed_divmod_fields(memory.state, frame)\nif target == 116092:\n    return distribute_city_battle_progress_fields(memory, frame)\nif target == 116052:\n    return sample_city_postbattle_reserve_fields(memory, frame)\nif target == 116382:\n    return apply_assigned_city_light_attrition_fields(memory, frame)\nif target == 116530:\n    return consume_city_battle_supply_long_fields(memory, frame)\nif target == 116620:\n    return reduce_city_reserve_after_defeat_fields(memory, frame)\nif target == 116676:\n    return consume_city_battle_supply_word_fields(memory, frame)\nif target == 117908:\n    return reassign_city_flagged_officers_fields(memory, frame)\nif target == 137160:\n    return apply_postbattle_city_economic_attrition_fields(memory, frame)\nif target == 117878:\n    return clear_city_officer_links_fields(memory, frame)\nraise MovementContinuationBoundary(target, frame, 'city outcome child needs its actual field/nonlocal-return ABI')"}})


# Entire current sole append_group_from_survivor_roster_fields body.
DECLARATIONS.update({'append_group_from_survivor_roster_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 136468)\npacket, assignments = (memory.table(4294938624).cursor(), memory.table(4294953984).cursor())\nframe = first_replace(frame, roster=packet, controller=assignments)\nwhile True:\n    header = packet.byte()\n    frame = _postbattle_byte_carrier_fields(frame, 'target_x', header)\n    members = header & 15\n    frame = _first_word(frame, 'target_x', members)\n    if members == 0:\n        break\n    packet = packet.advance(13 + s16(members))\n    frame = first_replace(frame, roster=packet)\nframe = _first_word(frame, 'target_x', 0)\nsource = memory.table(4294946646).cursor()\nframe = first_replace(frame, candidates=source)\ncount = 0\nwhile True:\n    officer = source.word()\n    source = source.advance(2)\n    frame = first_replace(frame, candidates=source)\n    frame = _first_word(frame, 'target_y', officer)\n    if negative_word(officer):\n        break\n    frame = _postbattle_bit_fields(frame, bool(frame.target_y & 16384))\n    if not frame.target_y & 16384:\n        continue\n    packet.set_byte(count, low8(frame.target_y), 13)\n    frame = _postbattle_memory_byte_fields(frame, low8(frame.target_y))\n    frame = _first_add_word(frame, 'target_x', count, 1)\n    count = u16(count + 1)\n    officer &= 255\n    frame = _first_word(frame, 'target_y', officer)\n    previous = assignments.byte(officer)\n    assignments.set_byte(officer, previous | 64)\n    frame = _postbattle_bit_fields(frame, bool(previous & 64))\npacket.byte(count, 13)\npacket.set_byte(count, 0, 13)\nframe = _postbattle_memory_byte_fields(frame, 0)\npacket.set_byte(0, low8(frame.target_x))\nframe = _postbattle_memory_byte_fields(frame, low8(frame.target_x))\nside = memory.table(4294964951).byte()\nframe = _postbattle_bit_fields(frame, bool(side & 2))\nforce = memory.table(4294964878 if side & 2 else 4294964876).word()\nframe = _first_word(frame, 'target_y', force)\npacket.set_byte(0, low8(frame.target_y), 4)\nframe = _postbattle_memory_byte_fields(frame, low8(frame.target_y))\nattributes = memory.table(4294951936).cursor()\nframe = first_replace(frame, candidates=attributes)\nframe = _first_word(frame, 'target_y', low16(frame.target_x))\nfrom ..high_level_battle_ai.business_formation import _first_sub_word\nframe = _first_sub_word(frame, 'target_y', low16(frame.target_y), 1)\nframe = _first_long(frame, 'unit', 0)\nframe = _first_word(frame, 'count', 0)\nfor counter in descending_inclusive(u16(count - 1)):\n    officer = packet.byte(counter, 13)\n    frame = _postbattle_byte_carrier_fields(frame, 'count', officer)\n    value = attributes.byte(low16(frame.count))\n    frame = _postbattle_byte_carrier_fields(frame, 'count', value)\n    frame = _first_add_word(frame, 'unit', low16(frame.unit), low16(frame.count))\n    frame = _postbattle_decrement_fields(frame, 'target_y', counter)\nframe = _damage_divide(frame, 'unit', low16(frame.target_x), 136586)\npacket.set_byte(0, low8(frame.unit), 3)\nframe = _postbattle_memory_byte_fields(frame, low8(frame.unit))\nframe = _city_outcome_call_fields(memory, frame, 139006, 136596)\nframe.roster.set_byte(0, low8(frame.target_x), 1)\nframe = _postbattle_memory_byte_fields(frame, low8(frame.target_x))\nframe.roster.set_byte(0, low8(frame.target_y), 2)\nreturn memory.finish(_postbattle_memory_byte_fields(frame, low8(frame.target_y)))"}})


# Entire current sole build_roster_fields body.
DECLARATIONS.update({'build_roster_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 24392)\nassignments, destination = (memory.table(4294953984).cursor(), memory.table(4294964480).cursor())\nframe = first_replace(frame, roster=assignments, candidates=destination)\nframe = _first_word(frame, 'target_y', 0)\nframe = _first_word(frame, 'count', 0)\nhead = memory.table(4294964784).word()\nframe = _first_word(frame, 'distance', head)\ncount = 0\nif not negative_word(head):\n    destination.set_word(0, head)\n    destination = destination.advance(2)\n    frame = first_replace(frame, candidates=destination)\n    frame = _first_memory_word(frame, head)\n    frame = _first_add_word(frame, 'count', count, 1)\n    count = 1\nofficer = 0\nwhile True:\n    assigned = assignments.byte()\n    assignments = assignments.advance(1)\n    frame = first_replace(frame, roster=assignments)\n    frame = _postbattle_byte_carrier_fields(frame, 'unit', assigned)\n    frame = _postbattle_compare_byte_fields(frame, assigned, low8(frame.target_x))\n    if assigned == low8(frame.target_x):\n        nominated = memory.table(4294964784).word()\n        frame = _first_compare_word(frame, officer, nominated)\n        if officer != nominated:\n            destination.set_word(0, officer)\n            destination = destination.advance(2)\n            frame = first_replace(frame, candidates=destination)\n            frame = _first_memory_word(frame, officer)\n            frame = _first_add_word(frame, 'count', count, 1)\n            count = u16(count + 1)\n    frame = _first_add_word(frame, 'target_y', officer, 1)\n    officer = u16(officer + 1)\n    frame = _first_compare_word(frame, officer, 256)\n    if officer >= 256:\n        destination.set_word(0, 65535)\n        return memory.finish(_first_memory_word(frame, 65535))"}})


# Entire current sole choose_city_head_fields body.
DECLARATIONS.update({'choose_city_head_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 57846)\nsaved = ('target_y', 'unit', 'count', 'distance', 'offset_x', 'roster', 'candidates', 'controller')\nframe, observed = _damage_save_longs(memory, frame, saved)\nsource = memory.table(4294964480).cursor()\nframe = first_replace(frame, roster=source)\nhead = source.word()\nsource = source.advance(2)\nframe = first_replace(frame, roster=source)\nframe = _first_word(frame, 'distance', head)\nif not negative_word(head):\n    frame = _city_outcome_call_fields(memory, frame, 57964, 57864)\n    if not frame.status & 1:\n        head = low16(frame.distance) & 255\n        frame = _first_word(frame, 'distance', head)\n        ratings = memory.table(4294951680).cursor()\n        frame = first_replace(frame, candidates=ratings)\n        frame = _first_word(frame, 'count', head)\n        rating = ratings.byte(head)\n        frame = _postbattle_byte_carrier_fields(frame, 'target_y', rating)\n        frame = _postbattle_byte_carrier_fields(frame, 'unit', low8(frame.target_y))\n        while True:\n            officer = frame.roster.word()\n            frame = first_replace(frame, roster=frame.roster.advance(2))\n            frame = _first_word(frame, 'count', officer)\n            if negative_word(officer):\n                break\n            officer &= 255\n            frame = _first_word(frame, 'count', officer)\n            rating = frame.candidates.byte(officer)\n            frame = _postbattle_byte_carrier_fields(frame, 'target_y', rating)\n            frame = _postbattle_compare_byte_fields(frame, rating, low8(frame.unit))\n            if rating > low8(frame.unit):\n                frame = _first_word(frame, 'distance', officer)\n                frame = _postbattle_byte_carrier_fields(frame, 'unit', low8(frame.target_y))\nelse:\n    owners = memory.table(4294964263).cursor()\n    frame = first_replace(frame, roster=owners)\n    owners.set_byte(low16(frame.target_x), 255)\n    frame = _postbattle_memory_byte_fields(frame, 255)\n    orders = memory.table(4294961164).cursor()\n    frame = first_replace(frame, roster=orders)\n    city = low16(frame.target_x)\n    frame = _first_word(frame, 'target_y', city)\n    frame = _first_shift_word(frame, 'target_y', city, 1)\n    frame = _first_add_word(frame, 'target_y', low16(frame.target_y), city)\n    frame = _first_shift_word(frame, 'target_y', low16(frame.target_y), 2)\n    for displacement in (0, 4, 8):\n        orders.set_word(low16(frame.target_y), 65535, displacement)\n        frame = _first_memory_word(frame, 65535)\ncity = low16(frame.target_x)\nframe = _first_shift_word(frame, 'target_x', city, 1)\nheads = memory.table(4294964318).cursor()\nframe = first_replace(frame, roster=heads)\nhead = low16(frame.distance)\nheads.set_word(low16(frame.target_x), head)\nframe = _first_memory_word(frame, head)\nframe = _first_word(frame, 'target_x', head)\nreturn _damage_restore_longs(memory, frame, saved, observed)"}})


# Entire current sole choose_empty_neighbor_position_fields body.
DECLARATIONS.update({'choose_empty_neighbor_position_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 139006)\nneighbors = memory.table(139138).cursor()\ncosts, terrain = (memory.table(26378).cursor(), memory.table(976368).cursor())\nframe = first_replace(frame, auxiliary=neighbors, scratch=costs, opponent=terrain)\ncity = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_x', city)\nframe = _first_shift_word(frame, 'target_x', city, 2)\ncoordinates = memory.table(871110).cursor()\nframe = first_replace(frame, candidates=coordinates)\nrow = coordinates.word(u16(city << 2), 2)\nframe = _first_word(frame, 'choice', row)\nframe = _first_right_word(frame, 'choice', row, 4)\ncolumn = coordinates.word(u16(city << 2))\nframe = _first_word(frame, 'offset_y', column)\nframe = _first_right_word(frame, 'offset_y', column, 4)\nwhile True:\n    frame = _first_word(frame, 'target_x', low16(frame.choice))\n    frame = _first_add_word(frame, 'target_x', low16(frame.target_x), neighbors.word())\n    frame = _first_compare_word(frame, low16(frame.target_x), 72)\n    if low16(frame.target_x) < 72:\n        frame = _first_word(frame, 'target_y', low16(frame.offset_y))\n        frame = _first_add_word(frame, 'target_y', low16(frame.target_y), neighbors.word(0, 2))\n        frame = _first_compare_word(frame, low16(frame.target_y), 72)\n        if low16(frame.target_y) < 72:\n            frame = _first_word(frame, 'unit', low16(frame.target_x))\n            frame = _first_shift_word(frame, 'unit', low16(frame.unit), 3)\n            frame = _first_add_word(frame, 'unit', low16(frame.unit), low16(frame.target_x))\n            frame = _first_shift_word(frame, 'unit', low16(frame.unit), 3)\n            frame = _first_add_word(frame, 'unit', low16(frame.unit), low16(frame.target_y))\n            frame = _first_word(frame, 'count', 0)\n            kind = terrain.byte(low16(frame.unit))\n            frame = _postbattle_byte_carrier_fields(frame, 'count', kind)\n            cost = costs.byte(low16(frame.count))\n            frame = _postbattle_memory_byte_fields(frame, cost)\n            if not negative_byte(cost):\n                groups = memory.table(4294938624).cursor()\n                frame = first_replace(frame, candidates=groups)\n                while True:\n                    header = groups.byte()\n                    frame = _postbattle_byte_carrier_fields(frame, 'unit', header)\n                    members = header & 15\n                    frame = _first_word(frame, 'unit', members)\n                    if members == 0:\n                        return memory.finish(frame)\n                    present_row = groups.byte(0, 1)\n                    frame = _postbattle_compare_byte_fields(frame, low8(frame.target_x), present_row)\n                    occupied = low8(frame.target_x) == present_row\n                    if occupied:\n                        present_column = groups.byte(0, 2)\n                        frame = _postbattle_compare_byte_fields(frame, low8(frame.target_y), present_column)\n                        occupied = low8(frame.target_y) == present_column\n                    if occupied:\n                        break\n                    groups = groups.advance(13 + s16(members))\n                    frame = first_replace(frame, candidates=groups)\n    neighbors = neighbors.advance(4)\n    frame = first_replace(frame, auxiliary=neighbors)"}})


# Entire current sole consolidate_city_after_battle body.
DECLARATIONS.update({'consolidate_city_after_battle': {'signature': 'state: GameplayState', 'returns': 'None', 'flow': 'checked_state(state)\nconsolidate_city_after_battle_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())'}})


# Entire current sole consolidate_city_after_battle_fields body.
DECLARATIONS.update({'consolidate_city_after_battle_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 117654)\nframe = _city_outcome_call_fields(memory, frame, 115400, 117658)\nassignments, roster = (memory.table(4294953984).cursor(), memory.table(4294955776).cursor())\nframe = first_replace(frame, roster=assignments, candidates=roster)\ncity = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_x', city)\nwhile True:\n    officer = roster.word()\n    roster = roster.advance(2)\n    frame = first_replace(frame, candidates=roster)\n    frame = _first_word(frame, 'target_y', officer)\n    if negative_word(officer):\n        break\n    assignments.set_byte(officer, low8(frame.target_x))\n    frame = _postbattle_memory_byte_fields(frame, low8(frame.target_x))\nowners = memory.table(4294964263).cursor()\nframe = first_replace(frame, roster=owners)\nowner = memory.table(4294964877).byte()\nowners.set_byte(low16(frame.target_x), owner)\nframe = _postbattle_memory_byte_fields(frame, owner)\ngold = memory.table(4294959100).cursor()\nframe = first_replace(frame, roster=gold)\ncity = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_x', city)\nframe = _first_shift_word(frame, 'target_x', city, 2)\noffset = u16(city << 2)\nfrom ..high_level_battle_ai.business_formation import _first_compare_long\nfor source_address, staging_address, destination_is_staging in ((4294959100, 4294962568, False), (4294959260, 4294962724, True)):\n    if destination_is_staging:\n        frame = first_replace(frame, roster=memory.table(source_address).cursor())\n    value = frame.roster.long(offset)\n    frame = _first_long(frame, 'target_y', value)\n    frame = first_replace(frame, candidates=memory.table(staging_address).cursor())\n    frame = _damage_add_long(memory, frame, 'target_y', frame.candidates.long(offset))\n    frame = _first_compare_long(frame, frame.target_y, 999999)\n    if frame.target_y > 999999:\n        frame = _first_long(frame, 'target_y', 999999)\n    destination = frame.candidates if destination_is_staging else frame.roster\n    destination.set_long(offset, frame.target_y)\n    frame = _first_long(frame, 'target_y', frame.target_y)\nmemory.table(4294964784).set_word(0, 65535)\nframe = _first_memory_word(frame, 65535)\nframe = _first_word(frame, 'target_x', memory.table(4294964874).word())\nframe = _city_outcome_call_fields(memory, frame, 24392, 117786)\nframe = _first_word(frame, 'target_x', memory.table(4294964874).word())\nreturn _city_outcome_call_fields(memory, frame, 57846, 117796)"}})


# Entire current sole roster_contains_force_head_carry_fields body.
DECLARATIONS.update({'roster_contains_force_head_carry_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 57964)\ncity = low16(frame.target_x)\nowners = memory.table(4294964263).cursor()\nframe = first_replace(frame, controller=owners)\nframe = _first_word(frame, 'offset_x', 0)\nowner = owners.byte(city)\nframe = _postbattle_byte_carrier_fields(frame, 'offset_x', owner)\nframe = _first_shift_word(frame, 'offset_x', low16(frame.offset_x), 1)\nheads = memory.table(4294960704).cursor()\nframe = first_replace(frame, controller=heads)\nruler = heads.word(low16(frame.offset_x))\nframe = _first_word(frame, 'offset_x', ruler)\nsource = memory.table(4294964480).cursor()\nframe = first_replace(frame, controller=source)\nwhile True:\n    token = source.word()\n    frame = _first_memory_word(frame, token)\n    if negative_word(token):\n        return memory.finish(first_replace(frame, status=frame.status & 30))\n    token = source.word()\n    source = source.advance(2)\n    frame = first_replace(frame, controller=source)\n    frame = _first_compare_word(frame, ruler, token)\n    if ruler == token:\n        frame = _first_word(frame, 'distance', ruler)\n        return memory.finish(first_replace(frame, status=frame.status | 1))"}})

APPROVED.setdefault('business_services',set()).update({'stage_sprite_word_packet_fields'})

APPROVED.setdefault('business_formation',set()).update({'_first_compare_long', '_first_sub_word'})

DECLARATIONS.update({'_trigger_call': {'signature': 'memory, frame, target, continuation', 'returns': None, 'flow': "frame = _trigger_frame(memory, frame)\nif not memory.complete:\n    return _trigger_legacy_call(memory, frame, target)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = battle_replace(frame, stack_cursor=stack)\nif target in (99320, 123938):\n    fields = FirstDeploymentFrame(target_x=entered.target_x, target_y=entered.target_y, unit=entered.unit, count=entered.count, distance=entered.distance, offset_x=entered.offset_x, offset_y=entered.offset_y, choice=entered.choice, roster=entered.roster, candidates=entered.candidates, controller=entered.controller, scan=entered.scan, opponent=entered.opponent, scratch=entered.scratch, auxiliary=entered.auxiliary, stack_cursor=entered.stack_cursor, status=entered.status & 31)\n    if target == 123938:\n        fields = city_reserve_forces_duel_carry_fields(BattlePresentationMemory(memory.state), fields)\n    else:\n        fields = resolve_city_battle_damage_fields(BattlePresentationMemory(memory.state), fields)[0]\n    returned = battle_replace(entered, target_x=fields.target_x, target_y=fields.target_y, unit=fields.unit, count=fields.count, distance=fields.distance, offset_x=fields.offset_x, offset_y=fields.offset_y, choice=fields.choice, roster=fields.roster, candidates=fields.candidates, controller=fields.controller, scan=fields.scan, opponent=fields.opponent, scratch=fields.scratch, auxiliary=fields.auxiliary, stack_cursor=fields.stack_cursor, status=memory.state.sr)\nelse:\n    returned = memory.state.service_at(target, entered)\nif type(returned) is not BattleTriggerFrame:\n    raise Boundary('real trigger child must return all observed full fields')\nreturned.validate_complete(memory.state)\nmemory.state.sr = returned.status\nactual = returned.stack_cursor.long()\nif actual != continuation:\n    raise Boundary('original trigger return slot changed to ' + str(actual))\nreturned = battle_replace(returned, stack_cursor=returned.stack_cursor.advance(4))\nreturn (returned, low16(returned.offset_y), low16(returned.choice))"}})

DECLARATIONS.update({'city_reserve_forces_duel_carry': {'signature': 'state: GameplayState', 'returns': None, 'flow': 'checked_state(state)\nframe = city_reserve_forces_duel_carry_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())\nreturn state.set_carry(bool(frame.status & 1))'}})

DECLARATIONS.update({'city_reserve_forces_duel_carry_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 123938)\nframe = _presentation_call_fields(memory, frame, 123944, _presentation_random_fields)\ncity = memory.table(4294964874).word()\nframe = _first_word(frame, 'target_x', city)\nframe = _first_shift_word(frame, 'target_x', city, 2)\nreserves = memory.table(4294960540).cursor()\nframe = first_replace(frame, roster=reserves)\nreserve = reserves.word(u16(city << 2), 2)\nframe = _first_word(frame, 'target_x', reserve)\nframe = _first_compare_word(frame, reserve, 30)\nchoose_duel = False\nif reserve < 30:\n    frame = _first_long(frame, 'target_y', 0)\n    seed = memory.table(4294964764).word()\n    frame = _first_word(frame, 'target_y', seed)\n    frame = _first_long(frame, 'unit', frame.target_y)\n    frame = _postbattle_shift_long_fields(memory, frame, 'target_y', 1)\n    frame = _damage_add_long(memory, frame, 'target_y', frame.unit)\n    frame = _postbattle_shift_long_fields(memory, frame, 'target_y', 3)\n    frame = _damage_add_long(memory, frame, 'target_y', frame.unit)\n    frame = _postbattle_shift_long_fields(memory, frame, 'target_y', 2)\n    frame = _first_long(frame, 'target_y', swap_words(frame.target_y))\n    frame = _first_compare_word(frame, low16(frame.target_y), reserve)\n    choose_duel = low16(frame.target_y) >= reserve\nmemory.finish(frame)\nstatus = memory.state.read_status_word() & 65534 | int(choose_duel)\nmemory.state.set_status_word(status)\nreturn first_replace(frame, status=status & 31)"}})

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('contexts_services',set()).update({'SceneRefreshBoundary', 'SceneRefreshMemory'})
APPROVED.setdefault('business_scene',set()).update({'expand_glyph_stream_fields', 'decode_glyph_rows_to_buffers_fields'})
APPROVED.setdefault('business_reuse',set()).update({'sum_group_troops_fields'})
APPROVED.setdefault('business_services',set()).update({'_scene_refresh_decrement', '_scene_refresh_emit'})
APPROVED.setdefault('business_movement_support',set()).update({'_movement_binary_flags'})
DECLARATIONS.update({'_battle_labels_call_fields': {'signature': 'memory, frame: FirstDeploymentFrame, target: Long, '
                                             'continuation: Long',
                                'returns': 'FirstDeploymentFrame',
                                'flow': 'from .contexts_services import SceneRefreshBoundary\n'
                                        'from ..high_level_scene_flows.business_scene import '
                                        'decode_glyph_rows_to_buffers_fields, expand_glyph_stream_fields\n'
                                        'from .business_reuse import sum_group_troops_fields\n'
                                        'if (target, continuation) not in ((44682, 96246), (44682, 96302), '
                                        '(44682, 96746), (44682, 96774), (44830, 96438), (44830, 96534), '
                                        '(96726, 96358), (96726, 96392), (96648, 96646), (96702, 96660), '
                                        '(96702, 96676)):\n'
                                        "    raise ValueError('actual label child and return token "
                                        "required')\n"
                                        'entered = memory.sync_status(frame)\n'
                                        'if frame.stack_cursor is not None:\n'
                                        '    stack = frame.stack_cursor.advance(-4)\n'
                                        '    stack.set_long(0, continuation)\n'
                                        '    entered = first_replace(frame, stack_cursor=stack)\n'
                                        'if target == 44682:\n'
                                        '    returned = decode_glyph_rows_to_buffers_fields(memory, '
                                        'entered)\n'
                                        'elif target == 44830:\n'
                                        '    returned = expand_glyph_stream_fields(memory, entered)\n'
                                        'elif target == 96726:\n'
                                        '    returned = append_force_head_glyphs_fields(memory, entered)\n'
                                        'elif target == 96648:\n'
                                        '    returned = cache_battle_roster_totals_fields(memory, entered)\n'
                                        'else:\n'
                                        '    returned, observed_count = sum_group_troops_fields(memory, '
                                        'entered)\n'
                                        'memory.frame(returned)\n'
                                        'if frame.stack_cursor is not None:\n'
                                        '    memory.sync_status(returned)\n'
                                        '    actual = returned.stack_cursor.long()\n'
                                        '    if actual != continuation:\n'
                                        '        raise SceneRefreshBoundary(target, returned, continuation)\n'
                                        '    returned = first_replace(returned, '
                                        'stack_cursor=returned.stack_cursor.advance(4))\n'
                                        'return memory.sync_status(returned)'},
 '_battle_labels_frame': {'signature': 'memory, frame: FirstDeploymentFrame',
                          'returns': 'FirstDeploymentFrame',
                          'flow': 'from .contexts_services import SceneRefreshMemory, SceneRefreshBoundary\n'
                                  'if type(memory) is not SceneRefreshMemory:\n'
                                  "    raise ValueError('same-state Scene label memory required')\n"
                                  'memory.frame(frame)\n'
                                  'if frame.stack_cursor is None:\n'
                                  '    raise SceneRefreshBoundary(96190, frame, None)\n'
                                  'return memory.sync_status(frame)'},
 '_battle_labels_upload_longs_fields': {'signature': 'memory, frame: FirstDeploymentFrame, counter_name, '
                                                     'inclusive: Word',
                                        'returns': 'FirstDeploymentFrame',
                                        'flow': 'from .business_services import _scene_refresh_emit, '
                                                '_scene_refresh_decrement\n'
                                                'frame = _first_word(frame, counter_name, inclusive)\n'
                                                'remaining = inclusive\n'
                                                'while True:\n'
                                                '    source = frame.candidates\n'
                                                '    value = source.long()\n'
                                                '    frame = first_replace(frame, '
                                                'candidates=source.advance(4))\n'
                                                '    frame = _scene_refresh_emit(memory, frame, 12582912, 4, '
                                                'value)\n'
                                                '    frame = _scene_refresh_decrement(frame, counter_name, '
                                                'remaining)\n'
                                                '    remaining = u16(remaining - 1)\n'
                                                '    if remaining == 65535:\n'
                                                '        return frame'},
 'append_force_head_glyphs': {'signature': 'state: GameplayState, context: GlyphBatchContext',
                              'returns': 'GlyphBatchContext',
                              'flow': 'from .contexts_services import SceneRefreshMemory\n'
                                      'context = checked_context(context, GlyphBatchContext, state)\n'
                                      'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                      'roster=context.source.advance(0), '
                                      'candidates=context.destination.advance(0), '
                                      'target_x=context.background, target_y=context.foreground, '
                                      'count=context.inclusive_count)\n'
                                      'actual = append_force_head_glyphs_fields(SceneRefreshMemory(state), '
                                      'frame)\n'
                                      'context.source.base, context.destination.base = (actual.roster.base, '
                                      'actual.candidates.base)\n'
                                      'return GlyphBatchContext(context.source, context.destination, '
                                      'actual.target_x, actual.target_y, actual.count)'},
 'append_force_head_glyphs_fields': {'signature': 'memory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'from .contexts_services import SceneRefreshBoundary\n'
                                             'from .business_services import _scene_refresh_emit, '
                                             '_scene_refresh_decrement\n'
                                             'memory.frame(frame)\n'
                                             'if frame.roster is None or frame.candidates is None:\n'
                                             '    raise SceneRefreshBoundary(96726, frame, None)\n'
                                             'marker = frame.roster.word(4)\n'
                                             'frame = _first_compare_word(frame, marker, 63)\n'
                                             'if marker != 63:\n'
                                             "    frame = _first_word(frame, 'count', 2)\n"
                                             '    return _battle_labels_call_fields(memory, frame, 44682, '
                                             '96746)\n'
                                             'spacer_longs = 16\n'
                                             "frame = _first_word(frame, 'count', spacer_longs - 1)\n"
                                             'for index in range(spacer_longs):\n'
                                             '    destination = frame.candidates\n'
                                             '    frame = first_replace(frame, '
                                             'candidates=destination.advance(4))\n'
                                             '    frame = _scene_refresh_emit(memory, frame, '
                                             'destination.base, 4, 286331153)\n'
                                             "    frame = _scene_refresh_decrement(frame, 'count', "
                                             'spacer_longs - 1 - index)\n'
                                             "frame = _first_word(frame, 'count', 1)\n"
                                             'frame = _battle_labels_call_fields(memory, frame, 44682, '
                                             '96774)\n'
                                             "frame = _first_word(frame, 'count', spacer_longs - 1)\n"
                                             'for index in range(spacer_longs):\n'
                                             '    destination = frame.candidates\n'
                                             '    frame = first_replace(frame, '
                                             'candidates=destination.advance(4))\n'
                                             '    frame = _scene_refresh_emit(memory, frame, '
                                             'destination.base, 4, 286331153)\n'
                                             "    frame = _scene_refresh_decrement(frame, 'count', "
                                             'spacer_longs - 1 - index)\n'
                                             'return memory.sync_status(frame)'},
 'cache_battle_roster_totals': {'signature': 'state: GameplayState',
                                'returns': 'None',
                                'flow': 'from .contexts_services import SceneRefreshMemory\n'
                                        'checked_state(state)\n'
                                        'cache_battle_roster_totals_fields(SceneRefreshMemory(state), '
                                        'FirstDeploymentFrame.unobserved())'},
 'cache_battle_roster_totals_fields': {'signature': 'memory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'from .business_services import _scene_refresh_emit\n'
                                               'frame = _battle_labels_frame(memory, frame)\n'
                                               'frame = first_replace(frame, '
                                               'roster=memory.cursor_at(4294952960), '
                                               'candidates=memory.cursor_at(4294944080))\n'
                                               'frame = _battle_labels_call_fields(memory, frame, 96702, '
                                               '96660)\n'
                                               'frame = _scene_refresh_emit(memory, frame, 4294964910, 4, '
                                               'frame.target_x)\n'
                                               'frame = _scene_refresh_emit(memory, frame, 4294964902, 2, '
                                               'low16(frame.target_y))\n'
                                               'frame = first_replace(frame, '
                                               'candidates=memory.cursor_at(4294944164))\n'
                                               'frame = _battle_labels_call_fields(memory, frame, 96702, '
                                               '96676)\n'
                                               'frame = _scene_refresh_emit(memory, frame, 4294964914, 4, '
                                               'frame.target_x)\n'
                                               'frame = _scene_refresh_emit(memory, frame, 4294964904, 2, '
                                               'low16(frame.target_y))\n'
                                               'city = memory.cursor_at(4294964874).word()\n'
                                               "frame = _first_word(frame, 'target_x', city)\n"
                                               "frame = _first_shift_word(frame, 'target_x', city, 2)\n"
                                               'frame = first_replace(frame, '
                                               'roster=memory.cursor_at(4294960540))\n'
                                               'reserve = frame.roster.word(low16(frame.target_x), 2)\n'
                                               'return memory.sync_status(_scene_refresh_emit(memory, frame, '
                                               '4294964926, 2, reserve))'},
 'upload_battle_scene_labels': {'signature': 'state: GameplayState, context: BattleSceneContext',
                                'returns': 'BattleSceneContext',
                                'flow': 'from .contexts_services import SceneRefreshMemory\n'
                                        'context = checked_context(context, BattleSceneContext, state)\n'
                                        'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                        'target_x=context.background, target_y=context.foreground, '
                                        'count=context.glyph_count)\n'
                                        'actual = '
                                        'upload_battle_scene_labels_fields(SceneRefreshMemory(state), '
                                        'frame)\n'
                                        'return BattleSceneContext(actual.target_x, actual.target_y, '
                                        'actual.count, context.training_carrier)'},
 'upload_battle_scene_labels_fields': {'signature': 'memory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'from .business_services import _scene_refresh_emit, '
                                               '_scene_refresh_decrement\n'
                                               'from ..high_level_main_flows.business_movement_support '
                                               'import _movement_binary_flags\n'
                                               'frame = _battle_labels_frame(memory, frame)\n'
                                               'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                               '1075838978)\n'
                                               'fill_longs = 32\n'
                                               "frame = _first_word(frame, 'target_x', fill_longs - 1)\n"
                                               'for index in range(fill_longs):\n'
                                               '    frame = _scene_refresh_emit(memory, frame, 12582912, 4, '
                                               '286331153)\n'
                                               "    frame = _scene_refresh_decrement(frame, 'target_x', "
                                               'fill_longs - 1 - index)\n'
                                               'frame = first_replace(frame, '
                                               'roster=memory.cursor_at(442200), '
                                               'candidates=memory.cursor_at(4294955776))\n'
                                               "frame = _first_word(frame, 'target_x', 1)\n"
                                               "frame = _first_word(frame, 'target_y', 3)\n"
                                               "frame = _first_word(frame, 'count', 10)\n"
                                               'frame = _battle_labels_call_fields(memory, frame, 44682, '
                                               '96246)\n'
                                               'frame = first_replace(frame, '
                                               'candidates=memory.cursor_at(4294955776))\n'
                                               'frame = _battle_labels_upload_longs_fields(memory, frame, '
                                               "'count', 351)\n"
                                               'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                               '1207959554)\n'
                                               'city = memory.cursor_at(4294964874).word()\n'
                                               "frame = _first_word(frame, 'count', city)\n"
                                               "frame = _first_shift_word(frame, 'count', city, 2)\n"
                                               'frame = first_replace(frame, roster=memory.cursor_at(565778, '
                                               'low16(frame.count)), '
                                               'candidates=memory.cursor_at(4294955776))\n'
                                               "frame = _first_word(frame, 'count', 1)\n"
                                               'frame = _battle_labels_call_fields(memory, frame, 44682, '
                                               '96302)\n'
                                               'frame = first_replace(frame, '
                                               'candidates=memory.cursor_at(4294955776))\n'
                                               'frame = _battle_labels_upload_longs_fields(memory, frame, '
                                               "'count', 63)\n"
                                               'for owner_address, continuation in ((4294964878, 96358), '
                                               '(4294964876, 96392)):\n'
                                               '    owner = memory.cursor_at(owner_address).word()\n'
                                               "    frame = _first_word(frame, 'distance', owner)\n"
                                               "    frame = _first_shift_word(frame, 'distance', owner, 1)\n"
                                               '    frame = first_replace(frame, '
                                               'controller=memory.cursor_at(4294960704))\n'
                                               '    ruler = frame.controller.word(low16(frame.distance))\n'
                                               "    frame = _first_word(frame, 'distance', ruler)\n"
                                               "    frame = _first_word(frame, 'offset_x', ruler)\n"
                                               "    frame = _first_shift_word(frame, 'distance', ruler, 1)\n"
                                               '    before = low16(frame.distance)\n'
                                               '    frame, offset = _movement_binary_flags(memory.state, '
                                               'frame, before, ruler, 16)\n'
                                               '    frame = first_replace(frame, '
                                               'distance=replace_word(frame.distance, offset))\n'
                                               "    frame = _first_shift_word(frame, 'distance', offset, 1)\n"
                                               '    frame = first_replace(frame, '
                                               'roster=memory.cursor_at(566532, low16(frame.distance)))\n'
                                               '    if continuation == 96358:\n'
                                               '        frame = first_replace(frame, '
                                               'candidates=memory.cursor_at(4294955776))\n'
                                               '    frame = _battle_labels_call_fields(memory, frame, 96726, '
                                               'continuation)\n'
                                               'frame = first_replace(frame, '
                                               'candidates=memory.cursor_at(4294955776))\n'
                                               'frame = _battle_labels_upload_longs_fields(memory, frame, '
                                               "'count', 191)\n"
                                               'frame = first_replace(frame, '
                                               'roster=memory.cursor_at(566310), '
                                               'candidates=memory.cursor_at(4294955776))\n'
                                               "frame = _first_word(frame, 'target_x', 3)\n"
                                               "frame = _first_word(frame, 'target_y', 1)\n"
                                               "frame = _first_word(frame, 'count', 9)\n"
                                               'frame = _battle_labels_call_fields(memory, frame, 44830, '
                                               '96438)\n'
                                               'frame = first_replace(frame, '
                                               'candidates=memory.cursor_at(4294955776))\n'
                                               'frame = _battle_labels_upload_longs_fields(memory, frame, '
                                               "'count', 79)\n"
                                               'frame = first_replace(frame, '
                                               'candidates=memory.cursor_at(442740))\n'
                                               'frame = _battle_labels_upload_longs_fields(memory, frame, '
                                               "'count', 15)\n"
                                               'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                               '1879048193)\n'
                                               'frame = first_replace(frame, '
                                               'candidates=memory.cursor_at(442222))\n'
                                               'frame = _battle_labels_upload_longs_fields(memory, frame, '
                                               "'count', 47)\n"
                                               'frame = first_replace(frame, '
                                               'roster=memory.cursor_at(566310), '
                                               'candidates=memory.cursor_at(4294955776))\n'
                                               "frame = _first_word(frame, 'target_x', 1)\n"
                                               "frame = _first_word(frame, 'target_y', 3)\n"
                                               "frame = _first_word(frame, 'count', 9)\n"
                                               'frame = _battle_labels_call_fields(memory, frame, 44830, '
                                               '96534)\n'
                                               'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                               '1891631105)\n'
                                               'frame = first_replace(frame, '
                                               'candidates=memory.cursor_at(4294955776))\n'
                                               'frame = _battle_labels_upload_longs_fields(memory, frame, '
                                               "'unit', 79)\n"
                                               'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                               '1610612738)\n'
                                               'frame = first_replace(frame, '
                                               'candidates=memory.cursor_at(703006))\n'
                                               'frame = _battle_labels_upload_longs_fields(memory, frame, '
                                               "'target_x', 23)\n"
                                               'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                               '1509949442)\n'
                                               'frame = first_replace(frame, '
                                               'candidates=memory.cursor_at(442414))\n'
                                               'frame = _battle_labels_upload_longs_fields(memory, frame, '
                                               "'target_y', 31)\n"
                                               'frame = first_replace(frame, '
                                               'candidates=memory.cursor_at(442600))\n'
                                               'frame = _battle_labels_upload_longs_fields(memory, frame, '
                                               "'target_y', 31)\n"
                                               'return _battle_labels_call_fields(memory, frame, 96648, '
                                               '96646)'}})

DECLARATIONS.update({'_city_outcome_child_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, target: int', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary\nif target == 115452:\n    return apply_battlefield_ratio_losses_fields(memory, frame)\nif target == 115612:\n    return apply_city_assigned_heavy_losses_fields(memory, frame)\nif target == 116206:\n    return apply_battlefield_heavy_losses_and_detach_fields(memory, frame)\nif target == 116780:\n    return rebuild_primary_after_battle_fields(memory, frame)\nif target == 116924:\n    return sort_returning_officer_status_fields(memory, frame)\nif target == 117058:\n    return partition_city_survivors_fields(memory, frame)\nif target == 117246:\n    return owner_has_other_city_carry_fields(memory, frame)\nif target == 117308:\n    return restore_returning_officer_assignments_fields(memory, frame)\nif target == 117344:\n    return allocate_packed_group_resources_fields(memory, frame)\nif target == 117512:\n    return rebuild_secondary_after_battle_fields(memory, frame)\nif target == 116194:\n    return distribute_battlefield_battle_progress_fields(memory, frame)\nif target == 133326:\n    from .business_reuse import apply_returning_officer_loyalty_fields\n    return apply_returning_officer_loyalty_fields(memory, frame)\nif target == 24392:\n    return build_roster_fields(memory, frame)\nif target == 57846:\n    return choose_city_head_fields(memory, frame)\nif target == 57964:\n    return roster_contains_force_head_carry_fields(memory, frame)\nif target == 136468:\n    return append_group_from_survivor_roster_fields(memory, frame)\nif target == 139006:\n    return choose_empty_neighbor_position_fields(memory, frame)\nif target == 117654:\n    return consolidate_city_after_battle_fields(memory, frame)\nif target == 158714:\n    from .contexts_services import SceneRefreshMemory\n    from .business_services import stage_sprite_word_packet_fields\n    return stage_sprite_word_packet_fields(SceneRefreshMemory(memory.state), frame)\nif target == 199284:\n    from .contexts_services import SceneRefreshMemory\n    from .business_services import present_gameplay_message_fields\n    return present_gameplay_message_fields(SceneRefreshMemory(memory.state), frame)\nif target == 115814:\n    return consume_city_battle_resources_fields(memory, frame)\nif target == 115138:\n    return compute_outcome_force_ratio_fields(memory, frame)\nif target == 115360:\n    return build_city_assigned_outcome_candidates_fields(memory, frame)[0]\nif target == 115400:\n    return build_battlefield_outcome_candidates_fields(memory, frame)[0]\nif target == 218976:\n    from ..high_level_main_flows.business_movement_support import signed_divmod_fields\n    return signed_divmod_fields(memory.state, frame)\nif target == 116092:\n    return distribute_city_battle_progress_fields(memory, frame)\nif target == 116052:\n    return sample_city_postbattle_reserve_fields(memory, frame)\nif target == 116382:\n    return apply_assigned_city_light_attrition_fields(memory, frame)\nif target == 116530:\n    return consume_city_battle_supply_long_fields(memory, frame)\nif target == 116620:\n    return reduce_city_reserve_after_defeat_fields(memory, frame)\nif target == 116676:\n    return consume_city_battle_supply_word_fields(memory, frame)\nif target == 117908:\n    return reassign_city_flagged_officers_fields(memory, frame)\nif target == 137160:\n    return apply_postbattle_city_economic_attrition_fields(memory, frame)\nif target == 117878:\n    return clear_city_officer_links_fields(memory, frame)\nif target == 118844:\n    return settle_battle_packed_armies_fields(memory, frame)\nif target == 118946:\n    return remove_defeated_packed_member_fields(memory, frame)\nif target == 119106:\n    return replace_or_remove_group_references_fields(memory, frame)\nif target == 119192:\n    return transfer_outcome_officer_fields(memory, frame)\nif target == 119306:\n    return detach_member_keep_group_cursor_fields(memory, frame)\nif target == 119454:\n    return replace_group_head_reference_fields(memory, frame)\nif target == 119528:\n    return remove_group_reference_fields(memory, frame)\nif target == 119576:\n    return attach_member_shift_packet_fields(memory, frame)\nif target == 119740:\n    from ..high_level_remaining_flows.business_city import settle_group_at_city_fields\n    return settle_group_at_city_fields(memory.state, frame)\nif target == 120026:\n    from ..high_level_remaining_flows.business_city import adjust_battle_losing_loyalty_fields\n    return adjust_battle_losing_loyalty_fields(memory.state, frame)\nraise MovementContinuationBoundary(target, frame, 'city outcome child needs its actual field/nonlocal-return ABI')"}})

DECLARATIONS.update({'_packed_compact_reference_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, from_second: bool', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_remaining_flows.business_city import _settlement_compact_pair_member_fields\nif type(from_second) is not bool:\n    raise ValueError('original pair compaction carrier layout required')\nsource = frame.controller if from_second else frame.roster\nprojected = first_replace(frame, roster=source.cursor())\nprojected = _settlement_compact_pair_member_fields(memory.state, projected)\ndestination = projected.roster.advance(-2)\nif from_second:\n    return first_replace(frame, candidates=destination, controller=memory.table(projected.roster.base), status=projected.status)\nreturn first_replace(frame, roster=projected.roster, candidates=destination, status=projected.status)"}})

DECLARATIONS.update({'_packed_relabel_active_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, header_blind: bool', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_remaining_flows.business_city import _settlement_relabel_active_member_fields\nif type(header_blind) is not bool:\n    raise ValueError('original header-blind relabel policy required')\nif header_blind:\n    projected = first_replace(frame, roster=frame.candidates.cursor())\n    projected = _settlement_relabel_active_member_fields(memory.state, projected, 'target_y', None)\n    return first_replace(frame, candidates=projected.roster, status=projected.status)\nprojected = first_replace(frame, target_x=frame.count)\nprojected = _settlement_relabel_active_member_fields(memory.state, projected, 'distance', False)\nreturn first_replace(frame, roster=projected.roster, status=projected.status)"}})

DECLARATIONS.update({'_packed_restore_word_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, name: str', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_movement_support import _movement_move\nif name not in ('target_x', 'target_y', 'count'):\n    raise ValueError('original packed member restored WORD carrier required')\nvalue = frame.stack_cursor.word()\nframe = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\nreturn _movement_move(memory.state, frame, name, value, 16)"}})

DECLARATIONS.update({'_packed_save_word_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, name: str', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_main_flows.business_movement_support import _movement_test\nif name not in ('target_x', 'target_y', 'count'):\n    raise ValueError('original packed member saved WORD carrier required')\nstack = frame.stack_cursor.advance(-2)\nvalue = low16(frame.carrier(name))\nstack.set_word(0, value)\nreturn _movement_test(memory.state, first_replace(frame, stack_cursor=stack), value, 16)"}})

DECLARATIONS.update({'_packed_seek_reference_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, head_name: str, address_name: str, postincrement: bool', 'returns': 'tuple', 'flow': "from ..high_level_remaining_flows.business_city import _settlement_seek_pair_member_fields\nif (head_name, address_name, postincrement) not in (('count', 'roster', True), ('target_x', 'candidates', False)):\n    raise ValueError('actual packed reference scan roles required')\nsource = frame.roster if address_name == 'roster' else frame.candidates\nprojected = first_replace(frame, target_x=frame.carrier(head_name), roster=source.cursor())\nprojected, found = _settlement_seek_pair_member_fields(memory.state, projected)\ncursor = projected.roster if postincrement else projected.roster.advance(-2 if found else -1)\nreturn (first_replace(frame, **{address_name: cursor}, status=projected.status), found)"}})

DECLARATIONS.update({'_packed_slide_tail_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame, from_second: bool', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_remaining_flows.business_city import _settlement_slide_member_tail_fields\nif type(from_second) is not bool:\n    raise ValueError('actual packed tail source role required')\nsource = frame.candidates if from_second else frame.controller\ndestination = frame.controller if from_second else frame.candidates\nprojected = first_replace(frame, unit=frame.target_y, scan=source.cursor(), controller=destination)\nprojected = _settlement_slide_member_tail_fields(memory.state, projected, 'scan', 'controller')\nreturn first_replace(frame, target_y=projected.unit, candidates=projected.scan if from_second else projected.controller.cursor(), controller=memory.table(projected.controller.base if from_second else projected.scan.base), status=projected.status)"}})

DECLARATIONS.update({'attach_member_shift_packet_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 119576)\nfrom ..high_level_main_flows.business_movement_support import _movement_move, _movement_compare, _movement_move_long, _movement_test_long, _movement_binary_flags, _movement_add_word, _movement_compare_address\nfrom ..high_level_remaining_flows.business_city import _settlement_write_byte_fields, _settlement_change_header_byte_fields, _settlement_carry_packet_tail_fields\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, frame.controller.base)\nframe = _movement_test_long(memory.state, first_replace(frame, stack_cursor=stack), frame.controller.base)\nframe = _movement_move(memory.state, frame, 'target_y', frame.candidates.byte(), 8)\nframe = _movement_move(memory.state, frame, 'target_y', low16(frame.target_y) & 15, 16)\nframe = _movement_compare(memory.state, frame, low16(frame.target_y), 10, 16)\nif not frame.status & 4:\n    offset = s16(low16(frame.target_y))\n    frame = first_replace(frame, controller=frame.candidates.advance(offset + 13), scan=frame.candidates.advance(offset + 14))\n    frame = _movement_move(memory.state, frame, 'target_y', frame.controller.byte(), 8)\n    frame = _settlement_carry_packet_tail_fields(memory.state, frame, ('target_y', 'unit', 'count'), 'scan', 0, 8)\n    frame = _movement_move(memory.state, frame, 'target_y', frame.candidates.byte(), 8)\n    frame = _movement_move(memory.state, frame, 'target_y', low16(frame.target_y) & 15, 16)\n    frame = _settlement_change_header_byte_fields(memory.state, frame, frame.candidates, False)\n    frame = _settlement_write_byte_fields(memory.state, frame, frame.candidates, low8(frame.target_x), low16(frame.target_y), 13)\n    frame = first_replace(frame, controller=memory.table(4294953984))\n    frame = _movement_move(memory.state, frame, 'count', 0, 16)\n    frame = _movement_move(memory.state, frame, 'count', frame.candidates.byte(0, 4), 8)\n    frame = _movement_add_word(memory.state, frame, 'count', 41)\n    frame = _settlement_write_byte_fields(memory.state, frame, frame.controller, low8(frame.count), low16(frame.target_x))\n    frame = _movement_move(memory.state, frame, 'count', 1, 16)\nelse:\n    frame = _movement_move(memory.state, frame, 'count', 0, 16)\n    frame = first_replace(frame, controller=memory.table(4294953984))\n    frame = _movement_move(memory.state, frame, 'target_y', frame.controller.byte(low16(frame.target_x)), 8)\n    frame = _movement_move(memory.state, frame, 'target_y', low16(frame.target_y) & 63, 16)\n    frame = _movement_compare(memory.state, frame, low16(frame.target_y), 40, 16)\n    high_assignment = not frame.status & 1 and (not frame.status & 4)\n    if high_assignment:\n        frame, value = _movement_binary_flags(memory.state, frame, low16(frame.target_y), 40, 16, True)\n        frame = first_replace(frame, target_y=replace_word(frame.target_y, value))\n    previous = frame.target_y\n    frame = first_replace(frame, target_y=previous | 128)\n    frame = _postbattle_bit_fields(frame, bool(previous & 128))\n    memory.finish(frame)\n    index = low16(frame.target_x) if high_assignment else low16(frame.target_y)\n    frame = _settlement_write_byte_fields(memory.state, frame, frame.controller, low8(frame.target_y), index)\nframe = _movement_compare_address(memory.state, frame, frame.roster.base, frame.candidates.base)\nif not frame.status & 1:\n    frame = _movement_move_long(memory.state, frame, 'count', frame.count & 65535)\n    frame, pointer = _movement_binary_flags(memory.state, frame, frame.roster.base, frame.count, 32)\n    frame = first_replace(frame, roster=memory.table(pointer).cursor())\npointer = frame.stack_cursor.long()\nframe = first_replace(frame, controller=memory.table(pointer), stack_cursor=frame.stack_cursor.advance(4))\nreturn memory.finish(frame)"}})

DECLARATIONS.update({'detach_member_keep_group_cursor_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 119306)\nfrom ..high_level_main_flows.business_movement_support import _movement_move, _movement_compare, _movement_adjust_word, _movement_move_long, _movement_binary_flags, _movement_compare_address\nfrom ..high_level_remaining_flows.business_city import _settlement_write_byte_fields, _settlement_change_header_byte_fields\nframe = _packed_save_word_fields(memory, frame, 'count')\nnames = ('target_y', 'unit', 'roster', 'candidates', 'controller')\nframe, observed = _damage_save_longs(memory, frame, names)\nframe = _movement_move(memory.state, frame, 'target_y', frame.roster.byte(), 8)\nframe = _movement_move(memory.state, frame, 'target_y', low16(frame.target_y) & 15, 16)\nframe = _movement_compare(memory.state, frame, low16(frame.target_y), 1, 16)\nif not frame.status & 4:\n    frame = _movement_move(memory.state, frame, 'count', 1, 16)\n    frame = _movement_move(memory.state, frame, 'unit', 0, 16)\n    while True:\n        frame = _movement_compare(memory.state, frame, low8(frame.target_x), frame.roster.byte(low16(frame.unit), 13), 8)\n        if frame.status & 4:\n            break\n        frame = _movement_adjust_word(memory.state, frame, 'unit', 1)\n    frame = _movement_adjust_word(memory.state, frame, 'unit', 1)\n    while True:\n        frame = _movement_compare(memory.state, frame, low16(frame.unit), low16(frame.target_y), 16)\n        if frame.status & 4:\n            break\n        frame = _settlement_write_byte_fields(memory.state, frame, frame.roster, frame.roster.byte(low16(frame.unit), 13), low16(frame.unit), 12)\n        frame = _movement_adjust_word(memory.state, frame, 'unit', 1)\n    frame = _city_outcome_call_fields(memory, frame, 119454, 119366)\n    frame = _settlement_change_header_byte_fields(memory.state, frame, frame.roster, True)\n    frame = first_replace(frame, candidates=frame.roster.advance(s16(low16(frame.target_y)) + 13), controller=frame.roster.advance(s16(low16(frame.target_y)) + 12))\nelse:\n    frame = _movement_move(memory.state, frame, 'count', 14, 16)\n    frame = _city_outcome_call_fields(memory, frame, 119528, 119388)\n    frame = first_replace(frame, candidates=frame.roster.advance(s16(low16(frame.target_y)) + 13), controller=memory.table(frame.roster.base), roster=memory.table(0).cursor())\nframe = _packed_slide_tail_fields(memory, frame, True)\nframe = _damage_restore_longs(memory, frame, names, observed)\nframe = _movement_compare_address(memory.state, frame, frame.candidates.base, frame.roster.base)\nif not frame.status & 1:\n    frame = _movement_move_long(memory.state, frame, 'count', frame.count & 65535)\n    frame, pointer = _movement_binary_flags(memory.state, frame, frame.candidates.base, frame.count, 32, True)\n    frame = first_replace(frame, candidates=memory.table(pointer).cursor())\nreturn memory.finish(_packed_restore_word_fields(memory, frame, 'count'))"}})

DECLARATIONS.update({'remove_defeated_packed_member_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 118946)\nfrom ..high_level_main_flows.business_movement_support import _movement_move, _movement_compare, _movement_adjust_word, _movement_move_long, _movement_binary_flags, _movement_compare_address\nfrom ..high_level_remaining_flows.business_city import _settlement_write_byte_fields, _settlement_change_header_byte_fields\nnames = ('target_y', 'unit', 'count', 'distance', 'roster', 'candidates', 'controller')\nframe, observed = _damage_save_longs(memory, frame, names)\nframe = first_replace(frame, roster=memory.table(4294953984).cursor())\nframe = _settlement_write_byte_fields(memory.state, frame, frame.roster, 255, low16(frame.target_x))\nframe = _movement_move(memory.state, frame, 'count', 0, 16)\nframe = _movement_move(memory.state, frame, 'count', frame.candidates.byte(0, 13), 8)\nframe = first_replace(frame, roster=frame.candidates.cursor())\nframe = _movement_move(memory.state, frame, 'target_y', frame.candidates.byte(), 8)\nframe = _movement_move(memory.state, frame, 'target_y', low16(frame.target_y) & 15, 16)\nframe = _movement_compare(memory.state, frame, low16(frame.target_y), 1, 16)\nif not frame.status & 4:\n    frame = _settlement_change_header_byte_fields(memory.state, frame, frame.candidates, True)\n    frame = _movement_move(memory.state, frame, 'unit', 0, 16)\n    frame = _movement_move(memory.state, frame, 'offset_x', 1, 16)\n    while True:\n        frame = _movement_compare(memory.state, frame, low8(frame.target_x), frame.candidates.byte(low16(frame.unit), 13), 8)\n        if frame.status & 4:\n            break\n        frame = _movement_adjust_word(memory.state, frame, 'unit', 1)\n    while True:\n        frame = _movement_adjust_word(memory.state, frame, 'unit', 1)\n        frame = _movement_compare(memory.state, frame, low16(frame.target_y), low16(frame.unit), 16)\n        if frame.status & 4:\n            break\n        frame = _settlement_write_byte_fields(memory.state, frame, frame.candidates, frame.candidates.byte(low16(frame.unit), 13), low16(frame.unit), 12)\n    packet = frame.candidates\n    frame = first_replace(frame, controller=packet.advance(s16(low16(frame.target_y)) + 13), candidates=packet.advance(s16(low16(frame.target_y)) + 12))\n    frame = _movement_move(memory.state, frame, 'distance', 0, 16)\n    frame = _movement_move(memory.state, frame, 'distance', frame.roster.byte(0, 13), 8)\nelse:\n    frame = _movement_move(memory.state, frame, 'distance', 65535, 16)\n    frame = _movement_move(memory.state, frame, 'offset_x', 14, 16)\n    frame = first_replace(frame, controller=frame.candidates.advance(s16(low16(frame.target_y)) + 13))\nframe = _packed_slide_tail_fields(memory, frame, False)\nframe = _city_outcome_call_fields(memory, frame, 119106, 119078)\nframe = _damage_restore_longs(memory, frame, names, observed)\nframe = _movement_compare_address(memory.state, frame, frame.controller.base, frame.candidates.base)\nif not frame.status & 1:\n    frame = _movement_move_long(memory.state, frame, 'offset_x', frame.offset_x & 65535)\n    frame, pointer = _movement_binary_flags(memory.state, frame, frame.controller.base, frame.offset_x, 32, True)\n    frame = first_replace(frame, controller=memory.table(pointer))\nreturn memory.finish(frame)"}})

DECLARATIONS.update({'remove_group_reference_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 119528)\nframe = first_replace(frame, candidates=memory.table(16726450).advance(s16(memory.table(16726962).word())).cursor())\nframe, found = _packed_seek_reference_fields(memory, frame, 'target_x', 'candidates', False)\nif found:\n    frame = first_replace(frame, controller=memory.table(frame.candidates.advance(2).base))\n    frame = _packed_compact_reference_fields(memory, frame, True)\nreturn memory.finish(frame)"}})

DECLARATIONS.update({'replace_group_head_reference_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 119454)\nfrom ..high_level_main_flows.business_movement_support import _movement_move\nfrom ..high_level_remaining_flows.business_city import _settlement_write_byte_fields\nframe = _packed_save_word_fields(memory, frame, 'target_y')\nframe = _movement_move(memory.state, frame, 'target_y', frame.roster.byte(0, 13), 8)\nframe = _movement_move(memory.state, frame, 'target_y', low16(frame.target_y) & 255, 16)\nframe = first_replace(frame, candidates=memory.table(16726450).advance(s16(memory.table(16726962).word())).cursor())\nframe, found = _packed_seek_reference_fields(memory, frame, 'target_x', 'candidates', False)\nif found:\n    frame = _settlement_write_byte_fields(memory.state, frame, frame.candidates, low8(frame.target_y), displacement=1)\n    frame = first_replace(frame, candidates=memory.table(16723968).cursor())\n    frame = _packed_relabel_active_fields(memory, frame, True)\nreturn memory.finish(_packed_restore_word_fields(memory, frame, 'target_y'))"}})

DECLARATIONS.update({'replace_or_remove_group_references_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 119106)\nfrom ..high_level_main_flows.business_movement_support import _movement_compare, _movement_test\nfrom ..high_level_remaining_flows.business_city import _settlement_write_byte_fields\nframe = _movement_compare(memory.state, frame, low16(frame.distance), low16(frame.count), 16)\nif frame.status & 4:\n    return memory.finish(frame)\nframe = first_replace(frame, roster=memory.table(16726450).advance(s16(memory.table(16726962).word())).cursor())\nframe, found = _packed_seek_reference_fields(memory, frame, 'count', 'roster', True)\nif not found:\n    return memory.finish(frame)\nframe = _movement_test(memory.state, frame, low16(frame.distance), 16)\nif frame.status & 8:\n    frame = first_replace(frame, candidates=frame.roster.advance(-2))\n    return memory.finish(_packed_compact_reference_fields(memory, frame, False))\nframe = _settlement_write_byte_fields(memory.state, frame, frame.roster, low8(frame.distance), displacement=-1)\nframe = first_replace(frame, roster=memory.table(16723968).cursor())\nreturn memory.finish(_packed_relabel_active_fields(memory, frame, False))"}})

DECLARATIONS.update({'settle_battle_packed_armies_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 118844)\nfrom ..high_level_main_flows.business_movement_support import _movement_move, _movement_test, _movement_test_long, _movement_shift_word\nframe = _city_outcome_call_fields(memory, frame, 119192, 118848)\nframe = first_replace(frame, candidates=memory.table(memory.table(16726060).long()).cursor(), controller=memory.table(4294938624), scan=memory.table(4294963134).cursor())\nframe = _movement_move(memory.state, frame, 'target_x', memory.table(4294963142).word(), 16)\nframe = first_replace(frame, controller=frame.controller.advance(s16(frame.scan.word(low16(frame.target_x)))), roster=memory.table(4294947328).cursor())\nframe = _movement_move(memory.state, frame, 'target_x', memory.table(4294964994).word(), 16)\nframe = _movement_shift_word(memory.state, frame, 'target_x')\nframe = _movement_test(memory.state, frame, frame.roster.word(low16(frame.target_x)), 16)\nif frame.status & 4:\n    frame = _movement_move(memory.state, frame, 'target_x', memory.table(4294964994).word(), 16)\n    frame = _city_outcome_call_fields(memory, frame, 118946, 118896)\n    memory.table(16726060).long()\n    memory.table(16726060).set_long(0, 0)\n    frame = _movement_test_long(memory.state, frame, 0)\nframe = first_replace(frame, candidates=frame.controller.cursor(), controller=memory.table(frame.candidates.base), roster=memory.table(4294947328).cursor())\nframe = _movement_move(memory.state, frame, 'target_x', memory.table(4294964998).word(), 16)\nframe = _movement_shift_word(memory.state, frame, 'target_x')\nframe = _movement_test(memory.state, frame, frame.roster.word(low16(frame.target_x)), 16)\nif frame.status & 4:\n    frame = _movement_move(memory.state, frame, 'target_x', memory.table(4294964998).word(), 16)\n    frame = _city_outcome_call_fields(memory, frame, 118946, 118930)\n    memory.table(16726060).set_long(0, frame.controller.base)\n    frame = _movement_test_long(memory.state, frame, frame.controller.base)\nframe = _city_outcome_call_fields(memory, frame, 119740, 118940)\nreturn _city_outcome_call_fields(memory, frame, 120026, 118944)"}})

DECLARATIONS.update({'transfer_outcome_officer_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _city_outcome_frame_fields(memory, frame, 119192)\nfrom ..high_level_main_flows.business_movement_support import _movement_move, _movement_compare, _movement_test_long, _movement_arithmetic_long\nfrom ..high_level_remaining_flows.business_city import _settlement_store_word_fields\nframe = _movement_compare(memory.state, frame, memory.table(4294934804).word(), 6, 16)\nif frame.status & 1:\n    return memory.finish(frame)\nsource = 4294934752 if frame.status & 4 else 4294934754\nframe = _movement_move(memory.state, frame, 'target_x', memory.table(source).word(), 16)\nframe = first_replace(frame, roster=memory.table(memory.table(16726060).long()).cursor(), candidates=memory.table(4294938624).cursor(), controller=memory.table(4294963134))\nframe = _movement_move(memory.state, frame, 'target_y', memory.table(4294963142).word(), 16)\nframe = first_replace(frame, candidates=frame.candidates.advance(s16(frame.controller.word(low16(frame.target_y)))))\nframe = _movement_compare(memory.state, frame, low16(frame.target_x), memory.table(4294964994).word(), 16)\nif not frame.status & 4:\n    frame = first_replace(frame, roster=frame.candidates.cursor(), candidates=frame.roster.cursor())\nframe = _packed_save_word_fields(memory, frame, 'target_x')\nframe = _city_outcome_call_fields(memory, frame, 119306, 119262)\nframe = _city_outcome_call_fields(memory, frame, 119576, 119266)\nframe = _packed_restore_word_fields(memory, frame, 'target_x')\nframe = _movement_compare(memory.state, frame, low16(frame.target_x), memory.table(4294964994).word(), 16)\nif not frame.status & 4:\n    frame = first_replace(frame, roster=frame.candidates.cursor(), candidates=frame.roster.cursor())\nmemory.table(16726060).set_long(0, frame.roster.base)\nframe = _movement_test_long(memory.state, frame, frame.roster.base)\npointer, retained = (frame.candidates.base, frame.target_y)\nframe = first_replace(frame, target_y=pointer, candidates=memory.table(retained).cursor())\nframe = _movement_arithmetic_long(memory.state, frame, 'target_y', 4294938624, True)\nframe = first_replace(frame, controller=memory.table(4294963134))\nframe = _movement_move(memory.state, frame, 'target_x', memory.table(4294963142).word(), 16)\nframe = _settlement_store_word_fields(memory.state, frame, frame.controller, low16(frame.target_x), low16(frame.target_y))\nreturn memory.finish(frame)"}})

APPROVED.setdefault('business_movement_support',set()).update(('_movement_test', '_movement_move', '_movement_compare', '_movement_compare_address', '_movement_adjust_word', '_movement_add_word', '_movement_binary_flags', '_movement_move_long', '_movement_test_long', '_movement_arithmetic_long', '_movement_shift_word'))

APPROVED.setdefault('business_city',set()).update(('_settlement_seek_pair_member_fields', '_settlement_relabel_active_member_fields', '_settlement_slide_member_tail_fields', '_settlement_compact_pair_member_fields', '_settlement_write_byte_fields', '_settlement_change_header_byte_fields', '_settlement_store_word_fields', '_settlement_carry_packet_tail_fields', 'settle_group_at_city_fields', 'adjust_battle_losing_loyalty_fields'))

DECLARATIONS.update({'find_nearest_secondary_terrain_target_observations': {'signature': 'state: GameplayState', 'returns': 'tuple[NearestTerrainTarget, Word]', 'flow': 'checked_state(state)\nframe = find_nearest_secondary_terrain_target_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())\nreturn (NearestTerrainTarget(low16(frame.offset_x), low16(frame.offset_y)), low16(frame.choice))'}})

DECLARATIONS.update({'_trigger_call': {'signature': 'memory, frame, target, continuation', 'returns': None, 'flow': "frame = _trigger_frame(memory, frame)\nif not memory.complete:\n    return _trigger_legacy_call(memory, frame, target)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = battle_replace(frame, stack_cursor=stack)\nif target in (99320, 123938, 124004):\n    fields = FirstDeploymentFrame(target_x=entered.target_x, target_y=entered.target_y, unit=entered.unit, count=entered.count, distance=entered.distance, offset_x=entered.offset_x, offset_y=entered.offset_y, choice=entered.choice, roster=entered.roster, candidates=entered.candidates, controller=entered.controller, scan=entered.scan, opponent=entered.opponent, scratch=entered.scratch, auxiliary=entered.auxiliary, stack_cursor=entered.stack_cursor, status=entered.status & 31)\n    if target == 123938:\n        fields = city_reserve_forces_duel_carry_fields(BattlePresentationMemory(memory.state), fields)\n    elif target == 124004:\n        fields = find_nearest_secondary_terrain_target_fields(BattlePresentationMemory(memory.state), fields)\n    else:\n        fields = resolve_city_battle_damage_fields(BattlePresentationMemory(memory.state), fields)[0]\n    returned = battle_replace(entered, target_x=fields.target_x, target_y=fields.target_y, unit=fields.unit, count=fields.count, distance=fields.distance, offset_x=fields.offset_x, offset_y=fields.offset_y, choice=fields.choice, roster=fields.roster, candidates=fields.candidates, controller=fields.controller, scan=fields.scan, opponent=fields.opponent, scratch=fields.scratch, auxiliary=fields.auxiliary, stack_cursor=fields.stack_cursor, status=memory.state.sr)\nelse:\n    returned = memory.state.service_at(target, entered)\nif type(returned) is not BattleTriggerFrame:\n    raise Boundary('real trigger child must return all observed full fields')\nreturned.validate_complete(memory.state)\nmemory.state.sr = returned.status\nactual = returned.stack_cursor.long()\nif actual != continuation:\n    raise Boundary('original trigger return slot changed to ' + str(actual))\nreturned = battle_replace(returned, stack_cursor=returned.stack_cursor.advance(4))\nreturn (returned, low16(returned.offset_y), low16(returned.choice))"}})

DECLARATIONS.update({'_nearest_terrain_radial_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory\nfrom ..high_level_battle_ai.business_geometry import rounded_deployment_radial_distance_fields\nreturn rounded_deployment_radial_distance_fields(BattlePolicyMemory(memory.state), frame)'}})

DECLARATIONS.update({'find_nearest_secondary_terrain_target_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_battle_ai.business_formation import _first_sub_word\nfrom ..high_level_battle_ai.business_actions import _deployment_compare_byte\nfrom ..high_level_main_flows.business_movement_support import _movement_multiply_word\nframe = _city_outcome_frame_fields(memory, frame, 124004)\nframe = _presentation_call_fields(memory, frame, 124010, _damage_map_fields)\nframe = first_replace(frame, candidates=memory.table(4294944164).cursor(), controller=memory.table(4294943056).cursor())\nframe = _first_word(frame, 'target_x', memory.table(4294964210).word())\nframe = memory.finish(_first_shift_word(frame, 'target_x', low16(frame.target_x), 2))\nframe = _first_word(frame, 'count', frame.controller.word(s16(low16(frame.target_x))))\nframe = memory.finish(_first_right_word(frame, 'count', low16(frame.count), 7))\nframe = _first_word(frame, 'distance', frame.controller.word(s16(low16(frame.target_x)), 2))\nframe = _first_right_word(frame, 'distance', low16(frame.distance), 7)\nframe = _first_word(frame, 'offset_x', 65535)\nframe = memory.finish(_first_word(frame, 'offset_y', 32768))\nwhile True:\n    member = frame.candidates.word()\n    frame = first_replace(frame, candidates=frame.candidates.advance(2))\n    frame = memory.finish(_first_word(frame, 'choice', member))\n    if negative_word(member):\n        return frame\n    frame = _first_word(frame, 'choice', member & 255)\n    frame = memory.finish(_first_shift_word(frame, 'choice', low16(frame.choice), 2))\n    frame = _first_word(frame, 'target_y', frame.controller.word(s16(low16(frame.choice))))\n    frame = memory.finish(_first_right_word(frame, 'target_y', low16(frame.target_y), 7))\n    frame = _first_word(frame, 'unit', frame.controller.word(s16(low16(frame.choice)), 2))\n    frame = memory.finish(_first_right_word(frame, 'unit', low16(frame.unit), 7))\n    frame, terrain = _damage_terrain_fields(memory, frame, low16(frame.target_y), low16(frame.unit), 124074)\n    frame = _deployment_compare_byte(memory, frame, low8(frame.target_x), 6)\n    if low8(frame.target_x) != 6:\n        continue\n    frame = _first_sub_word(frame, 'target_y', low16(frame.target_y), low16(frame.count))\n    if frame.status & 1:\n        frame = _first_sub_word(frame, 'target_y', 0, low16(frame.target_y))\n    frame = _movement_multiply_word(memory.state, frame, 'target_y', low16(frame.target_y))\n    frame = _first_sub_word(frame, 'unit', low16(frame.unit), low16(frame.distance))\n    if frame.status & 1:\n        frame = _first_sub_word(frame, 'unit', 0, low16(frame.unit))\n    frame = _movement_multiply_word(memory.state, frame, 'unit', low16(frame.unit))\n    frame = _first_long(frame, 'target_x', frame.target_y)\n    frame = _damage_add_long(memory, frame, 'target_x', frame.unit)\n    frame = _presentation_call_fields(memory, frame, 124106, _nearest_terrain_radial_fields)\n    measured, nearest = (low16(frame.target_x), low16(frame.offset_x))\n    frame = memory.finish(_first_compare_word(frame, measured, nearest))\n    if measured > nearest:\n        continue\n    if measured == nearest:\n        tie_bit = memory.table(4294964001).byte() & 1\n        frame = memory.finish(first_replace(frame, status=frame.status & 27 | (0 if tie_bit else 4)))\n        if tie_bit:\n            continue\n    frame = _first_word(frame, 'offset_x', measured)\n    frame = _first_right_word(frame, 'choice', low16(frame.choice), 2)\n    frame = memory.finish(_first_word(frame, 'offset_y', low16(frame.choice)))"}})

APPROVED.setdefault('business_formation', set()).update({'_first_sub_word'})

APPROVED.setdefault('business_actions', set()).update({'_deployment_compare_byte'})

APPROVED.setdefault('business_movement_support', set()).update({'_movement_multiply_word'})

APPROVED.setdefault('contexts_policy_memory', set()).update({'BattlePolicyMemory'})

APPROVED.setdefault('business_geometry', set()).update({'rounded_deployment_radial_distance_fields'})

DECLARATIONS.update({'upload_battlefield_tilemap': {'signature': 'state: GameplayState, retained_tile: Long=0', 'returns': 'Long', 'flow': 'checked_state(state)\nuint(retained_tile, 32)\nframe = first_replace(FirstDeploymentFrame.unobserved(), count=retained_tile)\nreturn upload_battlefield_tilemap_fields(BattlePresentationMemory(state), frame).count'}})

DECLARATIONS.update({'upload_battlefield_tilemap_fields': {'signature': 'memory: BattlePresentationMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from .contexts_services import SceneRefreshMemory\nfrom .business_services import _scene_refresh_emit, _scene_refresh_decrement\nfrom ..high_level_main_flows.business_movement_support import _movement_move, _movement_move_long, _movement_multiply_word, _movement_arithmetic_long\nframe = _city_outcome_frame_fields(memory, frame, 96118)\nvideo = SceneRefreshMemory(memory.state)\nframe = _movement_move_long(memory.state, frame, 'unit', 1342177283)\nframe = first_replace(frame, roster=memory.table(607720).cursor())\nframe = _movement_move(memory.state, frame, 'target_x', memory.table(4294964874).word(), 16)\nframe = _movement_multiply_word(memory.state, frame, 'target_x', 2240)\nframe = first_replace(frame, roster=frame.roster.advance(frame.target_x))\nframe = _movement_move(memory.state, frame, 'target_y', 27, 16)\nwhile True:\n    frame = _scene_refresh_emit(video, frame, 12582916, 4, frame.unit)\n    frame = _movement_move(memory.state, frame, 'target_x', 39, 16)\n    while True:\n        tile = frame.roster.word()\n        frame = first_replace(frame, roster=frame.roster.advance(2))\n        frame = _movement_move(memory.state, frame, 'count', tile, 16)\n        frame = memory.finish(first_replace(frame, status=frame.status & 27 | (0 if frame.count & 256 else 4)))\n        if not frame.status & 4:\n            frame = _movement_move(memory.state, frame, 'count', low16(frame.count) | 1792, 16)\n        frame = _scene_refresh_emit(video, frame, 12582912, 2, low16(frame.count))\n        frame = _scene_refresh_decrement(frame, 'target_x', low16(frame.target_x))\n        if low16(frame.target_x) == 65535:\n            break\n    frame = _movement_arithmetic_long(memory.state, frame, 'unit', 8388608)\n    frame = _scene_refresh_decrement(frame, 'target_y', low16(frame.target_y))\n    if low16(frame.target_y) == 65535:\n        return memory.finish(frame)"}})

APPROVED.setdefault('business_services',set()).update({'_scene_refresh_emit','_scene_refresh_decrement'})

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('contexts_services',set()).update({'SceneRefreshBoundary', '_first_byte', 'SceneRefreshMemory'})
APPROVED.setdefault('business_services',set()).update({'enqueue_sound_command_fields', 'initialize_video_registers_and_planes_fields', '_scene_refresh_flags', '_scene_refresh_emit', '_scene_refresh_decrement', 'clear_video_sprite_plane_fields'})
APPROVED.setdefault('business_scene',set()).update({'write_vdp_dictionary_repeat_stream_fields'})
DECLARATIONS.update({'_battle_initialize_call_fields': {'signature': 'memory, frame: FirstDeploymentFrame, target: Long, '
                                                 'continuation: Long',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'from .contexts_services import SceneRefreshBoundary\n'
                                            'from .business_services import '
                                            'initialize_video_registers_and_planes_fields, '
                                            'clear_video_sprite_plane_fields, enqueue_sound_command_fields\n'
                                            'if (target, continuation) not in ((26662, 95776), (26830, '
                                            '95782), (96016, 95844), (96118, 95848), (96190, 95852), (32906, '
                                            '95894), (95926, 95924), (95954, 95950), (44540, 96058), (44540, '
                                            '96106), (33042, 96116)):\n'
                                            "    raise ValueError('actual battle initialization child and "
                                            "return token required')\n"
                                            'memory.frame(frame)\n'
                                            'entered = memory.sync_status(frame)\n'
                                            'if frame.stack_cursor is not None:\n'
                                            '    stack = frame.stack_cursor.advance(-4)\n'
                                            '    stack.set_long(0, continuation)\n'
                                            '    entered = first_replace(frame, stack_cursor=stack)\n'
                                            'if target == 26662:\n'
                                            '    result = '
                                            'initialize_video_registers_and_planes_fields(memory, entered)\n'
                                            'elif target == 26830:\n'
                                            '    result = clear_video_sprite_plane_fields(memory, entered)\n'
                                            'elif target == 96016:\n'
                                            '    result = upload_battle_background_planes_fields(memory, '
                                            'entered)\n'
                                            'elif target == 96118:\n'
                                            '    result = '
                                            'upload_battlefield_tilemap_fields(BattlePresentationMemory(memory.state), '
                                            'entered)\n'
                                            'elif target == 96190:\n'
                                            '    result = upload_battle_scene_labels_fields(memory, '
                                            'entered)\n'
                                            'elif target == 32906:\n'
                                            '    result = enqueue_sound_command_fields(memory, entered, '
                                            'low8(entered.target_x))\n'
                                            'elif target == 95926:\n'
                                            '    result = compact_active_packed_group_queue_fields(memory, '
                                            'entered)\n'
                                            'elif target == 95954:\n'
                                            '    result = remove_queued_packed_group_member_fields(memory, '
                                            'entered)\n'
                                            'elif target == 44540:\n'
                                            '    from ..high_level_scene_flows.business_scene import '
                                            'write_vdp_dictionary_repeat_stream_fields\n'
                                            '    result = write_vdp_dictionary_repeat_stream_fields(memory, '
                                            'entered)\n'
                                            'else:\n'
                                            '    raise SceneRefreshBoundary(target, entered, continuation)\n'
                                            'if frame.stack_cursor is not None:\n'
                                            '    memory.sync_status(result)\n'
                                            '    actual = result.stack_cursor.long()\n'
                                            '    if actual != continuation:\n'
                                            '        raise SceneRefreshBoundary(actual, result, '
                                            'continuation)\n'
                                            '    result = first_replace(result, '
                                            'stack_cursor=result.stack_cursor.advance(4))\n'
                                            'return memory.sync_status(result)'},
 'compact_active_packed_group_queue': {'signature': 'state: GameplayState, retained_member: Long=0',
                                       'returns': 'Cursor',
                                       'flow': 'from .contexts_services import SceneRefreshMemory\n'
                                               'checked_state(state)\n'
                                               'uint(retained_member, 32)\n'
                                               'entered = first_replace(FirstDeploymentFrame.unobserved(), '
                                               'target_x=retained_member)\n'
                                               'return '
                                               'compact_active_packed_group_queue_fields(SceneRefreshMemory(state), '
                                               'entered).roster'},
 'compact_active_packed_group_queue_fields': {'signature': 'memory, frame: FirstDeploymentFrame',
                                              'returns': 'FirstDeploymentFrame',
                                              'flow': 'from .contexts_services import SceneRefreshBoundary, '
                                                      '_first_byte\n'
                                                      'from .business_services import _scene_refresh_flags\n'
                                                      'memory.frame(frame)\n'
                                                      'frame = first_replace(frame, '
                                                      'roster=memory.cursor_at(16726450))\n'
                                                      'offset = memory.cursor_at(16726962).word()\n'
                                                      'frame = first_replace(frame, '
                                                      'roster=frame.roster.advance(s16(offset)))\n'
                                                      'while True:\n'
                                                      '    kind = frame.roster.byte()\n'
                                                      '    frame = first_replace(frame, '
                                                      'roster=frame.roster.advance(1))\n'
                                                      '    frame = _scene_refresh_flags(memory, frame, kind, '
                                                      '1)\n'
                                                      '    if kind == 0:\n'
                                                      '        return memory.sync_status(frame)\n'
                                                      '    member = frame.roster.byte()\n'
                                                      '    frame = first_replace(frame, '
                                                      'roster=frame.roster.advance(1))\n'
                                                      "    frame = _first_byte(frame, 'target_x', member)\n"
                                                      '    if frame.target_x is None:\n'
                                                      '        raise SceneRefreshBoundary(95946, frame, '
                                                      'None)\n'
                                                      '    frame = _battle_initialize_call_fields(memory, '
                                                      'frame, 95954, 95950)'},
 'initialize_battle_scene': {'signature': 'state: GameplayState, context: BattleSceneContext',
                             'returns': 'BattleSceneContext',
                             'flow': 'from .contexts_services import SceneRefreshMemory\n'
                                     'context = checked_context(context, BattleSceneContext, state)\n'
                                     'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                     'target_x=context.background, target_y=context.foreground, '
                                     'unit=context.glyph_count, count=context.training_carrier)\n'
                                     'actual = initialize_battle_scene_fields(SceneRefreshMemory(state), '
                                     'frame)\n'
                                     'return BattleSceneContext(actual.target_x, actual.target_y, '
                                     'actual.unit, actual.count)'},
 'initialize_battle_scene_fields': {'signature': 'memory, frame: FirstDeploymentFrame',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'from .contexts_services import SceneRefreshBoundary, '
                                            '_first_byte\n'
                                            'from .business_services import _scene_refresh_flags, '
                                            '_scene_refresh_emit, _scene_refresh_decrement\n'
                                            'memory.frame(frame)\n'
                                            'if frame.stack_cursor is None:\n'
                                            '    raise SceneRefreshBoundary(95746, frame, None)\n'
                                            'frame = memory.status_word(frame, 9984)\n'
                                            'mode = memory.cursor_at(4294964932).word()\n'
                                            'frame = _scene_refresh_flags(memory, frame, mode, 2)\n'
                                            'if mode == 0:\n'
                                            '    value = memory.cursor_at(4294963988).word()\n'
                                            '    frame = _scene_refresh_emit(memory, frame, 4294964054, 2, '
                                            'value)\n'
                                            '    value = memory.cursor_at(4294963992).word()\n'
                                            '    frame = _scene_refresh_emit(memory, frame, 4294964052, 2, '
                                            'value)\n'
                                            'frame = _battle_initialize_call_fields(memory, frame, 26662, '
                                            '95776)\n'
                                            'frame = _battle_initialize_call_fields(memory, frame, 26830, '
                                            '95782)\n'
                                            'mode = memory.cursor_at(4294964932).word()\n'
                                            'frame = _scene_refresh_flags(memory, frame, mode, 2)\n'
                                            'if mode == 0:\n'
                                            '    memory.cursor_at(4294964936).word()\n'
                                            '    frame = _scene_refresh_emit(memory, frame, 4294964936, 2, '
                                            '0)\n'
                                            '    frame = first_replace(frame, '
                                            'roster=memory.cursor_at(4294946344), '
                                            'candidates=memory.cursor_at(16726978), '
                                            'controller=memory.cursor_at(16727490), '
                                            'scan=memory.cursor_at(16727234))\n'
                                            "    frame = _first_word(frame, 'target_x', 63)\n"
                                            '    for counter in descending_inclusive(63):\n'
                                            "        for name, destination in (('roster', frame.roster), "
                                            "('candidates', frame.candidates), ('controller', "
                                            "frame.controller), ('scan', frame.scan)):\n"
                                            '            destination.long()\n'
                                            '            frame = first_replace(frame, **{name: '
                                            'destination.advance(4)})\n'
                                            '            frame = _scene_refresh_emit(memory, frame, '
                                            'destination.base, 4, 0)\n'
                                            "        frame = _scene_refresh_decrement(frame, 'target_x', "
                                            'counter)\n'
                                            'frame = _scene_refresh_emit(memory, frame, 12582916, 2, 33798)\n'
                                            'frame = _battle_initialize_call_fields(memory, frame, 96016, '
                                            '95844)\n'
                                            'frame = _battle_initialize_call_fields(memory, frame, 96118, '
                                            '95848)\n'
                                            'frame = _battle_initialize_call_fields(memory, frame, 96190, '
                                            '95852)\n'
                                            'for address in (4294963986,):\n'
                                            '    memory.cursor_at(address).word()\n'
                                            '    frame = _scene_refresh_emit(memory, frame, address, 2, 0)\n'
                                            'frame = _scene_refresh_emit(memory, frame, 4294963988, 2, 256)\n'
                                            'for address in (4294963990, 4294963992):\n'
                                            '    memory.cursor_at(address).word()\n'
                                            '    frame = _scene_refresh_emit(memory, frame, address, 2, 0)\n'
                                            'sound = memory.cursor_at(4294964133).byte()\n'
                                            'frame = first_replace(frame, status=frame.status & 27 | (0 if '
                                            'sound & 1 else 4))\n'
                                            'if sound & 1 == 0:\n'
                                            "    frame = _first_byte(frame, 'target_x', 141)\n"
                                            '    frame = _scene_refresh_emit(memory, frame, 4294965092, 1, '
                                            'low8(frame.target_x))\n'
                                            '    frame = _battle_initialize_call_fields(memory, frame, '
                                            '32906, 95894)\n'
                                            'frame = _scene_refresh_emit(memory, frame, 4294964932, 2, 1)\n'
                                            'frame = first_replace(frame, '
                                            'roster=memory.cursor_at(4294961719))\n'
                                            'city = memory.cursor_at(4294964874).word()\n'
                                            "frame = _first_word(frame, 'target_x', city)\n"
                                            'frame = _scene_refresh_emit(memory, frame, '
                                            'frame.roster.address(city), 1, 3)\n'
                                            'previous = memory.cursor_at(4294964132).word()\n'
                                            'frame = _scene_refresh_emit(memory, frame, 4294964132, 2, '
                                            'previous & 1)\n'
                                            'return _battle_initialize_call_fields(memory, frame, 95926, '
                                            '95924)'},
 'remove_queued_packed_group_member': {'signature': 'state: GameplayState, queue: Cursor, member_carrier: '
                                                    'Long',
                                       'returns': 'Cursor',
                                       'flow': 'from .contexts_services import SceneRefreshMemory\n'
                                               'checked_state(state)\n'
                                               'checked_cursor(queue, state)\n'
                                               'uint(member_carrier, 32)\n'
                                               'entered = first_replace(FirstDeploymentFrame.unobserved(), '
                                               'roster=queue.advance(0), target_x=member_carrier)\n'
                                               'actual = '
                                               'remove_queued_packed_group_member_fields(SceneRefreshMemory(state), '
                                               'entered)\n'
                                               'queue.base = actual.roster.base\n'
                                               'return queue'},
 'remove_queued_packed_group_member_fields': {'signature': 'memory, frame: FirstDeploymentFrame',
                                              'returns': 'FirstDeploymentFrame',
                                              'flow': 'from .contexts_services import SceneRefreshBoundary, '
                                                      '_first_byte\n'
                                                      'from .business_services import _scene_refresh_flags, '
                                                      '_scene_refresh_emit\n'
                                                      'memory.frame(frame)\n'
                                                      'if frame.roster is None or frame.target_x is None:\n'
                                                      '    raise SceneRefreshBoundary(95954, frame, None)\n'
                                                      'frame = first_replace(frame, '
                                                      'candidates=memory.cursor_at(16723968))\n'
                                                      'while True:\n'
                                                      '    kind = frame.candidates.byte()\n'
                                                      '    frame = first_replace(frame, '
                                                      'candidates=frame.candidates.advance(1))\n'
                                                      '    frame = _scene_refresh_flags(memory, frame, kind, '
                                                      '1)\n'
                                                      '    if negative_byte(kind):\n'
                                                      '        return memory.sync_status(frame)\n'
                                                      '    member = frame.candidates.byte()\n'
                                                      '    frame = first_replace(frame, '
                                                      'candidates=frame.candidates.advance(1))\n'
                                                      '    frame = _postbattle_compare_byte_fields(frame, '
                                                      'low8(frame.target_x), member)\n'
                                                      '    if member == low8(frame.target_x):\n'
                                                      '        break\n'
                                                      '    while True:\n'
                                                      '        token = frame.candidates.byte()\n'
                                                      '        frame = first_replace(frame, '
                                                      'candidates=frame.candidates.advance(1))\n'
                                                      '        frame = _scene_refresh_flags(memory, frame, '
                                                      'token, 1)\n'
                                                      '        if token == 0:\n'
                                                      '            break\n'
                                                      'marker = frame.candidates.byte(0, 1)\n'
                                                      'frame = _postbattle_compare_byte_fields(frame, '
                                                      'marker, 128)\n'
                                                      'if marker != 128:\n'
                                                      '    return memory.sync_status(frame)\n'
                                                      'owner = frame.candidates.byte(0, 2)\n'
                                                      "frame = _first_byte(frame, 'target_y', owner)\n"
                                                      'selected = memory.cursor_at(4294964875).byte()\n'
                                                      'frame = _postbattle_compare_byte_fields(frame, owner, '
                                                      'selected)\n'
                                                      'if owner != selected:\n'
                                                      '    return memory.sync_status(frame)\n'
                                                      'while True:\n'
                                                      '    value = frame.roster.byte()\n'
                                                      '    frame = first_replace(frame, '
                                                      'roster=frame.roster.advance(1))\n'
                                                      '    frame = _scene_refresh_emit(memory, frame, '
                                                      'u32(frame.roster.base - 3), 1, value)\n'
                                                      '    if value == 0:\n'
                                                      '        return memory.sync_status(frame)\n'
                                                      '    value = frame.roster.byte()\n'
                                                      '    frame = first_replace(frame, '
                                                      'roster=frame.roster.advance(1))\n'
                                                      '    frame = _scene_refresh_emit(memory, frame, '
                                                      'u32(frame.roster.base - 3), 1, value)'},
 'upload_battle_background_planes': {'signature': 'state: GameplayState, count_carrier: Long=0',
                                     'returns': 'Long',
                                     'flow': 'from .contexts_services import SceneRefreshMemory\n'
                                             'checked_state(state)\n'
                                             'uint(count_carrier, 32)\n'
                                             'frame = first_replace(FirstDeploymentFrame.unobserved(), '
                                             'target_x=count_carrier)\n'
                                             'return '
                                             'upload_battle_background_planes_fields(SceneRefreshMemory(state), '
                                             'frame).target_x'},
 'upload_battle_background_planes_fields': {'signature': 'memory, frame: FirstDeploymentFrame',
                                            'returns': 'FirstDeploymentFrame',
                                            'flow': 'from .contexts_services import SceneRefreshBoundary\n'
                                                    'from .business_services import _scene_refresh_emit\n'
                                                    'memory.frame(frame)\n'
                                                    'if frame.stack_cursor is None or frame.target_x is '
                                                    'None:\n'
                                                    '    raise SceneRefreshBoundary(96016, frame, None)\n'
                                                    'for index, command, continuation in ((0, 1610612739, '
                                                    '96058), (4, 1073741825, 96106)):\n'
                                                    '    frame = _scene_refresh_emit(memory, frame, '
                                                    '12582916, 4, command)\n'
                                                    '    frame = first_replace(frame, '
                                                    'controller=memory.cursor_at(429076))\n'
                                                    '    source = frame.controller.long(index)\n'
                                                    '    frame = first_replace(frame, '
                                                    'roster=memory.cursor_at(source), '
                                                    'controller=memory.cursor_at(429084))\n'
                                                    '    destination = frame.controller.long(index)\n'
                                                    '    frame = first_replace(frame, '
                                                    'candidates=memory.cursor_at(destination))\n'
                                                    "    frame = _first_right_word(frame, 'target_x', "
                                                    'low16(frame.target_x), 1)\n'
                                                    '    frame = first_replace(frame, '
                                                    'controller=memory.cursor_at(442118))\n'
                                                    '    count = frame.controller.word(index // 2)\n'
                                                    "    frame = _first_word(frame, 'target_x', count)\n"
                                                    '    frame = _battle_initialize_call_fields(memory, '
                                                    'frame, 44540, continuation)\n'
                                                    "frame = _first_word(frame, 'target_x', 6)\n"
                                                    'return _battle_initialize_call_fields(memory, frame, '
                                                    '33042, 96116)'}})

DECLARATIONS.update({'_trigger_call': {'signature': 'memory, frame, target, continuation', 'returns': None, 'flow': "frame = _trigger_frame(memory, frame)\nif not memory.complete:\n    return _trigger_legacy_call(memory, frame, target)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = battle_replace(frame, stack_cursor=stack)\nif target in (99320, 123938, 124004, 95746):\n    fields = FirstDeploymentFrame(target_x=entered.target_x, target_y=entered.target_y, unit=entered.unit, count=entered.count, distance=entered.distance, offset_x=entered.offset_x, offset_y=entered.offset_y, choice=entered.choice, roster=entered.roster, candidates=entered.candidates, controller=entered.controller, scan=entered.scan, opponent=entered.opponent, scratch=entered.scratch, auxiliary=entered.auxiliary, stack_cursor=entered.stack_cursor, status=entered.status & 31)\n    if target == 123938:\n        fields = city_reserve_forces_duel_carry_fields(BattlePresentationMemory(memory.state), fields)\n    elif target == 124004:\n        fields = find_nearest_secondary_terrain_target_fields(BattlePresentationMemory(memory.state), fields)\n    elif target == 95746:\n        from .contexts_services import SceneRefreshMemory\n        fields = initialize_battle_scene_fields(SceneRefreshMemory(memory.state), fields)\n    else:\n        fields = resolve_city_battle_damage_fields(BattlePresentationMemory(memory.state), fields)[0]\n    returned = battle_replace(entered, target_x=fields.target_x, target_y=fields.target_y, unit=fields.unit, count=fields.count, distance=fields.distance, offset_x=fields.offset_x, offset_y=fields.offset_y, choice=fields.choice, roster=fields.roster, candidates=fields.candidates, controller=fields.controller, scan=fields.scan, opponent=fields.opponent, scratch=fields.scratch, auxiliary=fields.auxiliary, stack_cursor=fields.stack_cursor, status=memory.state.sr)\nelse:\n    returned = memory.state.service_at(target, entered)\nif type(returned) is not BattleTriggerFrame:\n    raise Boundary('real trigger child must return all observed full fields')\nreturned.validate_complete(memory.state)\nmemory.state.sr = returned.status\nactual = returned.stack_cursor.long()\nif actual != continuation:\n    raise Boundary('original trigger return slot changed to ' + str(actual))\nreturned = battle_replace(returned, stack_cursor=returned.stack_cursor.advance(4))\nreturn (returned, low16(returned.offset_y), low16(returned.choice))"}})

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('contexts_services',set()).update({'SceneRefreshBoundary'})
APPROVED.setdefault('business_services',set()).update({'enqueue_sound_command_fields', 'clear_video_sprite_plane_fields', 'initialize_video_registers_and_planes_fields', 'copy_video_transfer_descriptor_fields'})
APPROVED.setdefault('business_scene',set()).update({'write_vdp_dictionary_repeat_stream_fields'})
DECLARATIONS.update({'_battle_initialize_call_fields': {'signature': 'memory, frame: FirstDeploymentFrame, target: Long, '
                                                 'continuation: Long',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'from .contexts_services import SceneRefreshBoundary\n'
                                            'from .business_services import '
                                            'initialize_video_registers_and_planes_fields, '
                                            'clear_video_sprite_plane_fields, enqueue_sound_command_fields\n'
                                            'if (target, continuation) not in ((26662, 95776), (26830, '
                                            '95782), (96016, 95844), (96118, 95848), (96190, 95852), (32906, '
                                            '95894), (95926, 95924), (95954, 95950), (44540, 96058), (44540, '
                                            '96106), (33042, 96116)):\n'
                                            "    raise ValueError('actual battle initialization child and "
                                            "return token required')\n"
                                            'memory.frame(frame)\n'
                                            'entered = memory.sync_status(frame)\n'
                                            'if frame.stack_cursor is not None:\n'
                                            '    stack = frame.stack_cursor.advance(-4)\n'
                                            '    stack.set_long(0, continuation)\n'
                                            '    entered = first_replace(frame, stack_cursor=stack)\n'
                                            'if target == 26662:\n'
                                            '    result = '
                                            'initialize_video_registers_and_planes_fields(memory, entered)\n'
                                            'elif target == 26830:\n'
                                            '    result = clear_video_sprite_plane_fields(memory, entered)\n'
                                            'elif target == 96016:\n'
                                            '    result = upload_battle_background_planes_fields(memory, '
                                            'entered)\n'
                                            'elif target == 96118:\n'
                                            '    result = '
                                            'upload_battlefield_tilemap_fields(BattlePresentationMemory(memory.state), '
                                            'entered)\n'
                                            'elif target == 96190:\n'
                                            '    result = upload_battle_scene_labels_fields(memory, '
                                            'entered)\n'
                                            'elif target == 32906:\n'
                                            '    result = enqueue_sound_command_fields(memory, entered, '
                                            'low8(entered.target_x))\n'
                                            'elif target == 95926:\n'
                                            '    result = compact_active_packed_group_queue_fields(memory, '
                                            'entered)\n'
                                            'elif target == 95954:\n'
                                            '    result = remove_queued_packed_group_member_fields(memory, '
                                            'entered)\n'
                                            'elif target == 44540:\n'
                                            '    from ..high_level_scene_flows.business_scene import '
                                            'write_vdp_dictionary_repeat_stream_fields\n'
                                            '    result = write_vdp_dictionary_repeat_stream_fields(memory, '
                                            'entered)\n'
                                            'elif target == 33042:\n'
                                            '    from .business_services import '
                                            'copy_video_transfer_descriptor_fields\n'
                                            '    result = copy_video_transfer_descriptor_fields(memory, '
                                            'entered)\n'
                                            'else:\n'
                                            '    raise SceneRefreshBoundary(target, entered, continuation)\n'
                                            'if frame.stack_cursor is not None:\n'
                                            '    memory.sync_status(result)\n'
                                            '    actual = result.stack_cursor.long()\n'
                                            '    if actual != continuation:\n'
                                            '        raise SceneRefreshBoundary(actual, result, '
                                            'continuation)\n'
                                            '    result = first_replace(result, '
                                            'stack_cursor=result.stack_cursor.advance(4))\n'
                                            'return memory.sync_status(result)'}})

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('contexts_services',set()).update({'SceneRefreshBoundary', 'SceneRefreshMemory'})
APPROVED.setdefault('business_city',set()).update({'initialize_prebattle_head_bytes_fields', 'classify_duel_object_result_fields', 'rebuild_city_links_from_primary_roster_fields'})
APPROVED.setdefault('business_services',set()).update({'initialize_video_registers_and_planes_fields'})
APPROVED.setdefault('business_movement_support',set()).update({'_movement_compare', '_movement_test'})
DECLARATIONS.update({'_battle_scene_round_call_fields': {'signature': 'memory, frame: FirstDeploymentFrame, target: Long, '
                                                  'continuation: Long',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'from .contexts_services import SceneRefreshMemory, '
                                             'SceneRefreshBoundary\n'
                                             'if (target, continuation) not in ((120186, 3532), (251476, '
                                             '3548), (26662, 3554), (100518, 3572), (159156, 3624), (26662, '
                                             '3634), (101120, 3640), (120216, 3648), (118844, 3680), '
                                             '(120130, 3706)):\n'
                                             "    raise ValueError('original battle-round child and JSR "
                                             "continuation required')\n"
                                             'memory.frame(frame)\n'
                                             'def child(actual_memory, entered):\n'
                                             '    if target == 120186:\n'
                                             '        from ..high_level_remaining_flows.business_city import '
                                             'initialize_prebattle_head_bytes_fields\n'
                                             '        return '
                                             'initialize_prebattle_head_bytes_fields(actual_memory.state, '
                                             'entered)\n'
                                             '    if target == 26662:\n'
                                             '        from .business_services import '
                                             'initialize_video_registers_and_planes_fields\n'
                                             '        return '
                                             'initialize_video_registers_and_planes_fields(SceneRefreshMemory(actual_memory.state), '
                                             'entered)\n'
                                             '    if target == 120216:\n'
                                             '        from ..high_level_remaining_flows.business_city import '
                                             'classify_duel_object_result_fields\n'
                                             '        return '
                                             'classify_duel_object_result_fields(actual_memory.state, '
                                             'entered)\n'
                                             '    if target == 118844:\n'
                                             '        return '
                                             'settle_battle_packed_armies_fields(actual_memory, entered)\n'
                                             '    if target == 120130:\n'
                                             '        from ..high_level_remaining_flows.business_city import '
                                             'rebuild_city_links_from_primary_roster_fields\n'
                                             '        return '
                                             'rebuild_city_links_from_primary_roster_fields(actual_memory.state, '
                                             'entered)\n'
                                             '    raise SceneRefreshBoundary(target, entered, continuation)\n'
                                             'return '
                                             '_presentation_call_fields(BattlePresentationMemory(memory.state), '
                                             'frame, continuation, child)'},
 '_trigger_call': {'signature': 'memory, frame, target, continuation',
                   'returns': None,
                   'flow': 'frame = _trigger_frame(memory, frame)\n'
                           'if not memory.complete:\n'
                           '    return _trigger_legacy_call(memory, frame, target)\n'
                           'stack = frame.stack_cursor.advance(-4)\n'
                           'stack.set_long(0, continuation)\n'
                           'entered = battle_replace(frame, stack_cursor=stack)\n'
                           'if target in (99320, 123938, 124004, 95746, 3520):\n'
                           '    fields = FirstDeploymentFrame(target_x=entered.target_x, '
                           'target_y=entered.target_y, unit=entered.unit, count=entered.count, '
                           'distance=entered.distance, offset_x=entered.offset_x, offset_y=entered.offset_y, '
                           'choice=entered.choice, roster=entered.roster, candidates=entered.candidates, '
                           'controller=entered.controller, scan=entered.scan, opponent=entered.opponent, '
                           'scratch=entered.scratch, auxiliary=entered.auxiliary, '
                           'stack_cursor=entered.stack_cursor, status=entered.status & 31)\n'
                           '    if target == 123938:\n'
                           '        fields = '
                           'city_reserve_forces_duel_carry_fields(BattlePresentationMemory(memory.state), '
                           'fields)\n'
                           '    elif target == 124004:\n'
                           '        fields = '
                           'find_nearest_secondary_terrain_target_fields(BattlePresentationMemory(memory.state), '
                           'fields)\n'
                           '    elif target == 95746:\n'
                           '        from .contexts_services import SceneRefreshMemory\n'
                           '        fields = '
                           'initialize_battle_scene_fields(SceneRefreshMemory(memory.state), fields)\n'
                           '    elif target == 3520:\n'
                           '        from .contexts_services import SceneRefreshMemory\n'
                           '        fields = run_battle_scene_round_fields(SceneRefreshMemory(memory.state), '
                           'fields)\n'
                           '    else:\n'
                           '        fields = '
                           'resolve_city_battle_damage_fields(BattlePresentationMemory(memory.state), '
                           'fields)[0]\n'
                           '    returned = battle_replace(entered, target_x=fields.target_x, '
                           'target_y=fields.target_y, unit=fields.unit, count=fields.count, '
                           'distance=fields.distance, offset_x=fields.offset_x, offset_y=fields.offset_y, '
                           'choice=fields.choice, roster=fields.roster, candidates=fields.candidates, '
                           'controller=fields.controller, scan=fields.scan, opponent=fields.opponent, '
                           'scratch=fields.scratch, auxiliary=fields.auxiliary, '
                           'stack_cursor=fields.stack_cursor, status=memory.state.sr)\n'
                           'else:\n'
                           '    returned = memory.state.service_at(target, entered)\n'
                           'if type(returned) is not BattleTriggerFrame:\n'
                           "    raise Boundary('real trigger child must return all observed full fields')\n"
                           'returned.validate_complete(memory.state)\n'
                           'memory.state.sr = returned.status\n'
                           'actual = returned.stack_cursor.long()\n'
                           'if actual != continuation:\n'
                           "    raise Boundary('original trigger return slot changed to ' + str(actual))\n"
                           'returned = battle_replace(returned, '
                           'stack_cursor=returned.stack_cursor.advance(4))\n'
                           'return (returned, low16(returned.offset_y), low16(returned.choice))'},
 'run_battle_scene_round': {'signature': 'state: GameplayState, context: BattleSceneContext',
                            'returns': 'BattleFlowResult',
                            'flow': 'from .contexts_services import SceneRefreshMemory\n'
                                    'context = checked_context(context, BattleSceneContext, state)\n'
                                    'entered = first_replace(FirstDeploymentFrame.unobserved(), '
                                    'target_x=context.background, target_y=context.foreground, '
                                    'unit=context.glyph_count, count=context.training_carrier)\n'
                                    'actual = run_battle_scene_round_fields(SceneRefreshMemory(state), '
                                    'entered)\n'
                                    'return BattleFlowResult(actual.count)'},
 'run_battle_scene_round_fields': {'signature': 'memory, frame: FirstDeploymentFrame',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'from .contexts_services import SceneRefreshBoundary\n'
                                           'from ..high_level_main_flows.business_movement_support import '
                                           '_movement_test, _movement_compare\n'
                                           'memory.frame(frame)\n'
                                           'if frame.stack_cursor is None:\n'
                                           '    raise SceneRefreshBoundary(3520, frame, None)\n'
                                           'frame = memory.sync_status(frame)\n'
                                           'presentation = BattlePresentationMemory(memory.state)\n'
                                           'frame = _city_outcome_store_word_fields(presentation, frame, '
                                           '4294963168, memory.state.read(4294964932, 2))\n'
                                           'frame = _battle_scene_round_call_fields(memory, frame, 120186, '
                                           '3532)\n'
                                           'while True:\n'
                                           '    frame = _city_outcome_store_word_fields(presentation, frame, '
                                           '4294964932, 2)\n'
                                           '    frame = _city_outcome_store_word_fields(presentation, frame, '
                                           '4294963998, 0, True)\n'
                                           '    frame = _battle_scene_round_call_fields(memory, frame, '
                                           '251476, 3548)\n'
                                           '    frame = _battle_scene_round_call_fields(memory, frame, '
                                           '26662, 3554)\n'
                                           '    frame = _movement_compare(memory.state, frame, '
                                           'memory.state.read(4294934804, 2), 1, 16)\n'
                                           '    if not frame.status & 4:\n'
                                           '        frame = _battle_scene_round_call_fields(memory, frame, '
                                           '100518, 3572)\n'
                                           '        frame = _movement_test(memory.state, frame, '
                                           'memory.state.read(4294963168, 2), 16)\n'
                                           '        if not frame.status & 4:\n'
                                           '            frame = '
                                           '_city_outcome_store_word_fields(presentation, frame, 4294964754, '
                                           '1024)\n'
                                           '            frame = '
                                           '_city_outcome_store_word_fields(presentation, frame, 4294964066, '
                                           '0, True)\n'
                                           '            frame = '
                                           '_city_outcome_store_word_fields(presentation, frame, 4294964050, '
                                           '0, True)\n'
                                           '            frame = '
                                           '_city_outcome_store_word_fields(presentation, frame, 4294964932, '
                                           '1)\n'
                                           '            break\n'
                                           '    else:\n'
                                           '        frame = _city_outcome_store_word_fields(presentation, '
                                           'frame, 4294964932, 3)\n'
                                           '        frame = _city_outcome_store_word_fields(presentation, '
                                           'frame, 16740596, 1)\n'
                                           '        frame = _battle_scene_round_call_fields(memory, frame, '
                                           '159156, 3624)\n'
                                           '        frame = memory.status_word(frame, 9984)\n'
                                           '        frame = _battle_scene_round_call_fields(memory, frame, '
                                           '26662, 3634)\n'
                                           '        frame = _battle_scene_round_call_fields(memory, frame, '
                                           '101120, 3640)\n'
                                           '        if frame.status & 1:\n'
                                           '            continue\n'
                                           '        frame = _battle_scene_round_call_fields(memory, frame, '
                                           '120216, 3648)\n'
                                           '        frame = _movement_test(memory.state, frame, '
                                           'memory.state.read(4294963168, 2), 16)\n'
                                           '        if not frame.status & 4:\n'
                                           '            frame = '
                                           '_city_outcome_store_word_fields(presentation, frame, 4294964754, '
                                           '1024)\n'
                                           '            frame = '
                                           '_city_outcome_store_word_fields(presentation, frame, 4294964066, '
                                           '0, True)\n'
                                           '            frame = '
                                           '_city_outcome_store_word_fields(presentation, frame, 4294964050, '
                                           '0, True)\n'
                                           '            break\n'
                                           '    frame = _battle_scene_round_call_fields(memory, frame, '
                                           '118844, 3680)\n'
                                           '    frame = _city_outcome_store_word_fields(presentation, frame, '
                                           '4294964932, 0)\n'
                                           '    frame = _city_outcome_store_word_fields(presentation, frame, '
                                           '4294964754, 512)\n'
                                           '    frame = _city_outcome_store_word_fields(presentation, frame, '
                                           '4294964050, 0, True)\n'
                                           '    frame = _city_outcome_store_word_fields(presentation, frame, '
                                           '4294965092, 0, True)\n'
                                           '    break\n'
                                           'return _battle_scene_round_call_fields(memory, frame, 120130, '
                                           '3706)'}})

DECLARATIONS.update({'_battle_scene_round_call_fields': {'signature': 'memory, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "from .contexts_services import SceneRefreshMemory, SceneRefreshBoundary\nif (target, continuation) not in ((120186, 3532), (251476, 3548), (26662, 3554), (100518, 3572), (159156, 3624), (26662, 3634), (101120, 3640), (120216, 3648), (118844, 3680), (120130, 3706)):\n    raise ValueError('original battle-round child and JSR continuation required')\nmemory.frame(frame)\ndef child(actual_memory, entered):\n    if target == 120186:\n        from ..high_level_remaining_flows.business_city import initialize_prebattle_head_bytes_fields\n        return initialize_prebattle_head_bytes_fields(actual_memory.state, entered)\n    if target == 26662:\n        from .business_services import initialize_video_registers_and_planes_fields\n        return initialize_video_registers_and_planes_fields(SceneRefreshMemory(actual_memory.state), entered)\n    if target == 100518:\n        from .business_reuse import settle_duel_training_and_troops_fields\n        return settle_duel_training_and_troops_fields(actual_memory, entered)\n    if target == 120216:\n        from ..high_level_remaining_flows.business_city import classify_duel_object_result_fields\n        return classify_duel_object_result_fields(actual_memory.state, entered)\n    if target == 118844:\n        return settle_battle_packed_armies_fields(actual_memory, entered)\n    if target == 120130:\n        from ..high_level_remaining_flows.business_city import rebuild_city_links_from_primary_roster_fields\n        return rebuild_city_links_from_primary_roster_fields(actual_memory.state, entered)\n    raise SceneRefreshBoundary(target, entered, continuation)\nreturn _presentation_call_fields(BattlePresentationMemory(memory.state), frame, continuation, child)"}})

APPROVED.setdefault('business_reuse',set()).add('settle_duel_training_and_troops_fields')

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('contexts_services',set()).update({'SceneRefreshBoundary', 'SceneRefreshMemory'})
APPROVED.setdefault('business_city',set()).update({'rebuild_city_links_from_primary_roster_fields', 'classify_duel_object_result_fields', 'initialize_prebattle_head_bytes_fields'})
APPROVED.setdefault('business_objects',set()).update({'run_scene_object_controller_fields'})
APPROVED.setdefault('business_services',set()).update({'initialize_video_registers_and_planes_fields'})
APPROVED.setdefault('business_reuse',set()).update({'settle_duel_training_and_troops_fields'})
DECLARATIONS.update({'_battle_scene_round_call_fields': {'signature': 'memory, frame: FirstDeploymentFrame, target: Long, '
                                                  'continuation: Long',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'from .contexts_services import SceneRefreshMemory, '
                                             'SceneRefreshBoundary\n'
                                             'if (target, continuation) not in ((120186, 3532), (251476, '
                                             '3548), (26662, 3554), (100518, 3572), (159156, 3624), (26662, '
                                             '3634), (101120, 3640), (120216, 3648), (118844, 3680), '
                                             '(120130, 3706)):\n'
                                             "    raise ValueError('original battle-round child and JSR "
                                             "continuation required')\n"
                                             'memory.frame(frame)\n'
                                             'def child(actual_memory, entered):\n'
                                             '    if target == 120186:\n'
                                             '        from ..high_level_remaining_flows.business_city import '
                                             'initialize_prebattle_head_bytes_fields\n'
                                             '        return '
                                             'initialize_prebattle_head_bytes_fields(actual_memory.state, '
                                             'entered)\n'
                                             '    if target == 251476:\n'
                                             '        from ..high_level_scene_flows.business_objects import '
                                             'run_scene_object_controller_fields\n'
                                             '        return '
                                             'run_scene_object_controller_fields(SceneRefreshMemory(actual_memory.state), '
                                             'entered)\n'
                                             '    if target == 26662:\n'
                                             '        from .business_services import '
                                             'initialize_video_registers_and_planes_fields\n'
                                             '        return '
                                             'initialize_video_registers_and_planes_fields(SceneRefreshMemory(actual_memory.state), '
                                             'entered)\n'
                                             '    if target == 100518:\n'
                                             '        from .business_reuse import '
                                             'settle_duel_training_and_troops_fields\n'
                                             '        return '
                                             'settle_duel_training_and_troops_fields(actual_memory, '
                                             'entered)\n'
                                             '    if target == 120216:\n'
                                             '        from ..high_level_remaining_flows.business_city import '
                                             'classify_duel_object_result_fields\n'
                                             '        return '
                                             'classify_duel_object_result_fields(actual_memory.state, '
                                             'entered)\n'
                                             '    if target == 118844:\n'
                                             '        return '
                                             'settle_battle_packed_armies_fields(actual_memory, entered)\n'
                                             '    if target == 120130:\n'
                                             '        from ..high_level_remaining_flows.business_city import '
                                             'rebuild_city_links_from_primary_roster_fields\n'
                                             '        return '
                                             'rebuild_city_links_from_primary_roster_fields(actual_memory.state, '
                                             'entered)\n'
                                             '    raise SceneRefreshBoundary(target, entered, continuation)\n'
                                             'return '
                                             '_presentation_call_fields(BattlePresentationMemory(memory.state), '
                                             'frame, continuation, child)'}})

DECLARATIONS.update({'_battle_scene_round_call_fields': {'signature': 'memory, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "from .contexts_services import SceneRefreshMemory, SceneRefreshBoundary\nif (target, continuation) not in ((120186, 3532), (251476, 3548), (26662, 3554), (100518, 3572), (159156, 3624), (26662, 3634), (101120, 3640), (120216, 3648), (118844, 3680), (120130, 3706)):\n    raise ValueError('original battle-round child and JSR continuation required')\nmemory.frame(frame)\ndef child(actual_memory, entered):\n    if target == 120186:\n        from ..high_level_remaining_flows.business_city import initialize_prebattle_head_bytes_fields\n        return initialize_prebattle_head_bytes_fields(actual_memory.state, entered)\n    if target == 251476:\n        from ..high_level_scene_flows.business_objects import run_scene_object_controller_fields\n        return run_scene_object_controller_fields(SceneRefreshMemory(actual_memory.state), entered)\n    if target == 26662:\n        from .business_services import initialize_video_registers_and_planes_fields\n        return initialize_video_registers_and_planes_fields(SceneRefreshMemory(actual_memory.state), entered)\n    if target == 100518:\n        from .business_reuse import settle_duel_training_and_troops_fields\n        return settle_duel_training_and_troops_fields(actual_memory, entered)\n    if target == 101120:\n        from .business_reuse import settle_duel_packets_fields\n        return settle_duel_packets_fields(actual_memory, entered)\n    if target == 120216:\n        from ..high_level_remaining_flows.business_city import classify_duel_object_result_fields\n        return classify_duel_object_result_fields(actual_memory.state, entered)\n    if target == 118844:\n        return settle_battle_packed_armies_fields(actual_memory, entered)\n    if target == 120130:\n        from ..high_level_remaining_flows.business_city import rebuild_city_links_from_primary_roster_fields\n        return rebuild_city_links_from_primary_roster_fields(actual_memory.state, entered)\n    raise SceneRefreshBoundary(target, entered, continuation)\nreturn _presentation_call_fields(BattlePresentationMemory(memory.state), frame, continuation, child)"}})

APPROVED.setdefault('business_reuse',set()).add('settle_duel_packets_fields')


# Source136: real existing full children; each old caller retains its own return LONG.
DECLARATIONS.update({'_battle_scene_round_call_fields': {'signature': 'memory, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "from .contexts_services import SceneRefreshMemory, SceneRefreshBoundary\nif (target, continuation) not in ((120186, 3532), (251476, 3548), (26662, 3554), (100518, 3572), (159156, 3624), (26662, 3634), (101120, 3640), (120216, 3648), (118844, 3680), (120130, 3706)):\n    raise ValueError('original battle-round child and JSR continuation required')\nmemory.frame(frame)\ndef child(actual_memory, entered):\n    if target == 120186:\n        from ..high_level_remaining_flows.business_city import initialize_prebattle_head_bytes_fields\n        return initialize_prebattle_head_bytes_fields(actual_memory.state, entered)\n    if target == 251476:\n        from ..high_level_scene_flows.business_objects import run_scene_object_controller_fields\n        return run_scene_object_controller_fields(SceneRefreshMemory(actual_memory.state), entered)\n    if target == 26662:\n        from .business_services import initialize_video_registers_and_planes_fields\n        return initialize_video_registers_and_planes_fields(SceneRefreshMemory(actual_memory.state), entered)\n    if target == 100518:\n        from .business_reuse import settle_duel_training_and_troops_fields\n        return settle_duel_training_and_troops_fields(actual_memory, entered)\n    if target == 101120:\n        from .business_reuse import settle_duel_packets_fields\n        return settle_duel_packets_fields(actual_memory, entered)\n    if target == 120216:\n        from ..high_level_remaining_flows.business_city import classify_duel_object_result_fields\n        return classify_duel_object_result_fields(actual_memory.state, entered)\n    if target == 118844:\n        return settle_battle_packed_armies_fields(actual_memory, entered)\n    if target == 120130:\n        from ..high_level_remaining_flows.business_city import rebuild_city_links_from_primary_roster_fields\n        return rebuild_city_links_from_primary_roster_fields(actual_memory.state, entered)\n    if target == 159156:\n        from ..high_level_scene_flows.business_duel import run_duel_scene_fields\n        return run_duel_scene_fields(actual_memory.state, entered)\n    raise SceneRefreshBoundary(target, entered, continuation)\nreturn _presentation_call_fields(BattlePresentationMemory(memory.state), frame, continuation, child)"}, '_trigger_call': {'signature': 'memory, frame, target, continuation', 'returns': None, 'flow': "frame = _trigger_frame(memory, frame)\nif not memory.complete:\n    return _trigger_legacy_call(memory, frame, target)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = battle_replace(frame, stack_cursor=stack)\nif target in (99320, 123938, 124004, 95746, 3520, 155876):\n    fields = FirstDeploymentFrame(target_x=entered.target_x, target_y=entered.target_y, unit=entered.unit, count=entered.count, distance=entered.distance, offset_x=entered.offset_x, offset_y=entered.offset_y, choice=entered.choice, roster=entered.roster, candidates=entered.candidates, controller=entered.controller, scan=entered.scan, opponent=entered.opponent, scratch=entered.scratch, auxiliary=entered.auxiliary, stack_cursor=entered.stack_cursor, status=entered.status & 31)\n    if target == 123938:\n        fields = city_reserve_forces_duel_carry_fields(BattlePresentationMemory(memory.state), fields)\n    elif target == 124004:\n        fields = find_nearest_secondary_terrain_target_fields(BattlePresentationMemory(memory.state), fields)\n    elif target == 95746:\n        from .contexts_services import SceneRefreshMemory\n        fields = initialize_battle_scene_fields(SceneRefreshMemory(memory.state), fields)\n    elif target == 3520:\n        from .contexts_services import SceneRefreshMemory\n        fields = run_battle_scene_round_fields(SceneRefreshMemory(memory.state), fields)\n    elif target == 155876:\n        from ..high_level_main_flows.business_movement_support import present_battle_message_fields\n        fields = present_battle_message_fields(memory.state, fields)\n    else:\n        fields = resolve_city_battle_damage_fields(BattlePresentationMemory(memory.state), fields)[0]\n    returned = battle_replace(entered, target_x=fields.target_x, target_y=fields.target_y, unit=fields.unit, count=fields.count, distance=fields.distance, offset_x=fields.offset_x, offset_y=fields.offset_y, choice=fields.choice, roster=fields.roster, candidates=fields.candidates, controller=fields.controller, scan=fields.scan, opponent=fields.opponent, scratch=fields.scratch, auxiliary=fields.auxiliary, stack_cursor=fields.stack_cursor, status=memory.state.sr)\nelse:\n    returned = memory.state.service_at(target, entered)\nif type(returned) is not BattleTriggerFrame:\n    raise Boundary('real trigger child must return all observed full fields')\nreturned.validate_complete(memory.state)\nmemory.state.sr = returned.status\nactual = returned.stack_cursor.long()\nif actual != continuation:\n    raise Boundary('original trigger return slot changed to ' + str(actual))\nreturned = battle_replace(returned, stack_cursor=returned.stack_cursor.advance(4))\nreturn (returned, low16(returned.offset_y), low16(returned.choice))"}})
APPROVED.setdefault((2, 'high_level_main_flows.business_movement_support'), set()).update(('present_battle_message_fields',))
APPROVED.setdefault((2, 'high_level_scene_flows.business_duel'), set()).update(('run_duel_scene_fields',))
