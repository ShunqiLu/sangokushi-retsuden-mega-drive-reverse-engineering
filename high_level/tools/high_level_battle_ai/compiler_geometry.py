"""Complete geometry AST contracts and ordinary 68000 target selection.

The business rules live in business_geometry, separate from this backend.
Only explicit source text is consumed during compilation, never ROM or old ASM.
This is a restricted byte-compatible frontend, not a general Python compiler.
"""
import ast
from .compiler_common import CompileError, semantic_functions, lower_declared
from .target import GEOMETRY_BINDINGS

APPROVED = {'contexts_geometry': {'TargetCoordinate', 'ContactStrength', 'ContactCollection', 'RadialSeed'},
 'domain': {'CarryOutcome',
            'GameState',
            'Long',
            'Table',
            'Word',
            'checked_state',
            'checked_table',
            'divu_retained',
            'low16',
            'low8',
            'negative_byte',
            'negative_word',
            'replace_byte',
            'replace_word',
            'u16',
            'u32',
            'uint'},
 'contexts_radial': {'RadialDistanceFields',
                     'RadialMemory',
                     'RadialSeedFields',
                     'RadialTable',
                     'SceneState',
                     'checked_radial_table',
                     'checked_scene_state'}}

DECLARATIONS = {'weighted_training_factor': {'signature': 'state: GameState, unit: Word',
                              'returns': 'Long',
                              'flow': 'checked_state(state)\n'
                                      'uint(unit, 16)\n'
                                      'training = state.officer_training.byte(unit)\n'
                                      'rating = state.officer_word_b400.word(u16(unit * 2))\n'
                                      'return divu_retained(training * rating, 100)',
                              'slots': {100: ('training_divisor', 1, 65535)}},
 'load_battlefield_map_context': {'signature': 'state: GameState', 'returns': 'Table', 'flow': 'checked_state(state)\nreturn load_battlefield_map_fields(BattlePolicyMemory(state))'},
 'read_battlefield_terrain_type': {'signature': 'state: GameState, map_context: Table, x: Word, y: '
                                                'Word, retained: Long=0',
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
 'constrain_transposed_target_coordinate': {'signature': 'state: GameState, actor: Word, x: Word, '
                                                         'y: Word',
                                            'returns': 'TargetCoordinate',
                                            'flow': 'checked_state(state)\n'
                                                    'uint(actor, 16)\n'
                                                    'uint(x, 16)\n'
                                                    'uint(y, 16)\n'
                                                    'return '
                                                    'constrain_target_near_battlefield_anchor(state, '
                                                    'actor, x, y)'},
 'compare_actor_to_weakest_contact_strength': {'signature': 'state: GameState, actor: Word',
                                               'returns': 'CarryOutcome',
                                               'flow': 'checked_state(state)\n'
                                                       'uint(actor, 16)\n'
                                                       'collect_contacts_in_speed_radius(state, '
                                                       'actor)\n'
                                                       'if '
                                                       'negative_word(state.action_candidates.word()):\n'
                                                       '    return state.carry_result(0)\n'
                                                       'weakest = '
                                                       'select_weakest_contact_strength(state)\n'
                                                       'training = weighted_training_factor(state, '
                                                       'actor)\n'
                                                       'troops = weakest.troops.long(u16(actor * '
                                                       '4))\n'
                                                       'own_strength = low16(troops) * '
                                                       'low16(training)\n'
                                                       'return '
                                                       'state.carry_result(int(weakest.strength <= '
                                                       'own_strength))'},
 'select_weakest_contact_strength': {'signature': 'state: GameState, retained_member: Word=0, '
                                                  'retained_weighting: Long=0',
                                     'returns': 'ContactStrength',
                                     'flow': 'checked_state(state)\n'
                                             'uint(retained_member, 16)\n'
                                             'uint(retained_weighting, 32)\n'
                                             'candidates = state.action_candidates.cursor()\n'
                                             'troops = state.officer_troops\n'
                                             'best_strength = 4294967295\n'
                                             'best_member = retained_member\n'
                                             'last_weighting = retained_weighting\n'
                                             'while True:\n'
                                             '    member = candidates.next_word()\n'
                                             '    if negative_word(member):\n'
                                             '        return ContactStrength(best_strength, '
                                             'best_member, last_weighting, candidates, troops)\n'
                                             '    last_weighting = weighted_training_factor(state, '
                                             'member)\n'
                                             '    offset = u16(member * 4)\n'
                                             '    strength = low16(troops.long(offset)) * '
                                             'low16(last_weighting)\n'
                                             '    if strength < best_strength:\n'
                                             '        best_strength = strength\n'
                                             '        best_member = offset >> 2'},
 'constrain_pursuit_target_coordinate': {'signature': 'state: GameState, actor: Word, x: Word, y: '
                                                      'Word',
                                         'returns': 'TargetCoordinate',
                                         'flow': 'checked_state(state)\n'
                                                 'uint(actor, 16)\n'
                                                 'uint(x, 16)\n'
                                                 'uint(y, 16)\n'
                                                 'return '
                                                 'constrain_target_near_battlefield_anchor(state, '
                                                 'actor, x, y)'},
 'test_other_side_total_shortfall': {'signature': 'state: GameState',
                                     'returns': 'CarryOutcome',
                                     'flow': 'checked_state(state)\n'
                                             'primary = state.table(4294964894)\n'
                                             'secondary = state.table(4294964898)\n'
                                             "if state.scalar('battle_side_flags') & 2:\n"
                                             '    primary, secondary = (secondary, primary)\n'
                                             'strength = secondary.long()\n'
                                             'if strength >= primary.long():\n'
                                             '    return state.carry_result(0)\n'
                                             'return state.carry_result(int(strength < '
                                             "state.scalar('secondary_strength_limit')))"},
 'mark_eligible_actor_for_retreat': {'signature': 'state: GameState, actor: Word',
                                     'returns': 'CarryOutcome',
                                     'flow': 'checked_state(state)\n'
                                             'uint(actor, 16)\n'
                                             'eligible = test_actor_terrain_types_3_or_7(state, '
                                             'actor).carry == 1\n'
                                             'if eligible:\n'
                                             '    eligible = state.officer_troops.long(u16(actor * '
                                             '4)) <= 5000\n'
                                             'if eligible:\n'
                                             '    eligible = '
                                             'count_roster_nonnegative_prefix_bytes(state) >= 4\n'
                                             'if eligible:\n'
                                             '    collect_contacts_in_speed_radius(state, actor)\n'
                                             '    eligible = not '
                                             'negative_word(state.action_candidates.word())\n'
                                             'if eligible:\n'
                                             '    marked = state.unit_retreat_flags.byte(actor)\n'
                                             '    if marked == 0:\n'
                                             '        eligible = not bool(state.sample_random() & '
                                             '32768)\n'
                                             'if not eligible:\n'
                                             '    state.unit_retreat_flags.set_byte(actor, 0)\n'
                                             '    return state.carry_result(0)\n'
                                             'state.unit_retreat_flags.set_byte(actor, 1)\n'
                                             'state.deployed_flags.set_byte(actor, 0)\n'
                                             'return state.carry_result(1)',
                                     'slots': {5000: ('retreat_troop_limit', 0, 4294967295)}},
 'test_actor_terrain_types_3_or_7': {'signature': 'state: GameState, actor: Word',
                                     'returns': 'CarryOutcome',
                                     'flow': 'checked_state(state)\n'
                                             'uint(actor, 16)\n'
                                             'map_context = load_battlefield_map_context(state)\n'
                                             'offset = u16(actor * 4)\n'
                                             'x = state.battle_positions.word(offset) >> 7\n'
                                             'y = state.battle_positions.word(offset, 2) >> 7\n'
                                             'terrain = low8(read_battlefield_terrain_type(state, '
                                             'map_context, x, y))\n'
                                             'return state.carry_result(int(terrain == 3 or '
                                             'terrain == 7))'},
 'count_roster_nonnegative_prefix_bytes': {'signature': 'state: GameState',
                                           'returns': 'Word',
                                           'flow': 'checked_state(state)\n'
                                                   'roster = state.secondary_battle_roster if '
                                                   "state.scalar('battle_side_flags') & 2 else "
                                                   'state.primary_battle_roster\n'
                                                   'source = roster.cursor()\n'
                                                   'count = 0\n'
                                                   'while not negative_byte(source.next_byte()):\n'
                                                   '    count = u16(count + 1)\n'
                                                   'return count'},
 'constrain_second_pursuit_target_coordinate': {'signature': 'state: GameState, actor: Word, x: '
                                                             'Word, y: Word',
                                                'returns': 'TargetCoordinate',
                                                'flow': 'checked_state(state)\n'
                                                        'uint(actor, 16)\n'
                                                        'uint(x, 16)\n'
                                                        'uint(y, 16)\n'
                                                        'return '
                                                        'constrain_target_near_battlefield_anchor(state, '
                                                        'actor, x, y)'},
 'test_other_roster_single_member': {'signature': 'state: GameState',
                                     'returns': 'CarryOutcome',
                                     'flow': 'checked_state(state)\n'
                                             'roster = state.primary_battle_roster if '
                                             "state.scalar('battle_side_flags') & 2 else "
                                             'state.secondary_battle_roster\n'
                                             'return '
                                             'state.carry_result(int(negative_word(roster.word(0, '
                                             '2))))'},
 'constrain_target_near_battlefield_anchor': {'signature': 'state: GameState, actor: Word, x: '
                                                           'Word, y: Word',
                                              'returns': 'TargetCoordinate',
                                              'flow': 'checked_state(state)\n'
                                                      'uint(actor, 16)\n'
                                                      'uint(x, 16)\n'
                                                      'uint(y, 16)\n'
                                                      'actor_offset = u16(actor * 4)\n'
                                                      'own_x = '
                                                      'state.battle_positions.word(actor_offset)\n'
                                                      'own_y = '
                                                      'state.battle_positions.word(actor_offset, '
                                                      '2)\n'
                                                      'anchor_offset = '
                                                      "u16(state.scalar('battle_scene') * 4)\n"
                                                      'center_y = '
                                                      'state.scene_anchor_positions.word(anchor_offset, '
                                                      '2)\n'
                                                      'center_x = '
                                                      'state.scene_anchor_positions.word(anchor_offset)\n'
                                                      'x_distance = u16(own_x - center_x)\n'
                                                      'if own_x < center_x:\n'
                                                      '    x_distance = u16(-x_distance)\n'
                                                      'if x_distance > 4096:\n'
                                                      '    return TargetCoordinate(x, y)\n'
                                                      'if x_distance == 4096:\n'
                                                      '    y_distance = u16(own_y - center_y)\n'
                                                      '    if own_y < center_y:\n'
                                                      '        y_distance = u16(-y_distance)\n'
                                                      '    if y_distance > 4096:\n'
                                                      '        return TargetCoordinate(x, y)\n'
                                                      '    if own_x <= center_x and x <= own_x or '
                                                      '(own_x > center_x and x >= own_x):\n'
                                                      '        return TargetCoordinate(x, y)\n'
                                                      '    edge_y = u16(center_y + 4096) if y > '
                                                      'center_y else u16(center_y - 4096)\n'
                                                      '    if edge_y != own_y:\n'
                                                      '        return TargetCoordinate(own_x, '
                                                      'edge_y)\n'
                                                      '    target_dx = u16(own_x - x)\n'
                                                      '    if own_x < x:\n'
                                                      '        target_dx = u16(-target_dx)\n'
                                                      '    target_dy = u16(own_y - y)\n'
                                                      '    if own_y < y:\n'
                                                      '        target_dy = u16(-target_dy)\n'
                                                      '    return TargetCoordinate(own_x, y) if '
                                                      'target_dy > target_dx else '
                                                      'TargetCoordinate(x, own_y)\n'
                                                      'y_distance = u16(own_y - center_y)\n'
                                                      'if own_y < center_y:\n'
                                                      '    y_distance = u16(-y_distance)\n'
                                                      'if y_distance != 4096:\n'
                                                      '    return TargetCoordinate(x, y)\n'
                                                      'if own_y <= center_y and y <= own_y or '
                                                      '(own_y > center_y and y >= own_y):\n'
                                                      '    return TargetCoordinate(x, y)\n'
                                                      'edge_x = u16(center_x + 4096) if x > '
                                                      'center_x else u16(center_x - 4096)\n'
                                                      'return TargetCoordinate(edge_x, own_y)',
                                              'slots': {4096: ('anchor_edge', 0, 65535)}},
 'select_nearest_contact_to_battlefield_center': {'signature': 'state: GameState, retained_member: '
                                                               'Word=0',
                                                  'returns': 'Word',
                                                  'flow': 'checked_state(state)\n'
                                                          'uint(retained_member, 16)\n'
                                                          'if '
                                                          'negative_word(state.action_candidates.word(0, '
                                                          '2)):\n'
                                                          '    selected = '
                                                          'state.action_candidates.word()\n'
                                                          'else:\n'
                                                          '    offset = '
                                                          "u16(state.scalar('battle_scene') * 4)\n"
                                                          '    center_x = '
                                                          'state.scene_anchor_positions.word(offset)\n'
                                                          '    center_y = '
                                                          'state.scene_anchor_positions.word(offset, '
                                                          '2)\n'
                                                          '    candidates = '
                                                          'state.action_candidates.cursor()\n'
                                                          '    closest = 65535\n'
                                                          '    selected = retained_member\n'
                                                          '    while True:\n'
                                                          '        member = '
                                                          'candidates.next_word()\n'
                                                          '        if negative_word(member):\n'
                                                          '            break\n'
                                                          '        unit_offset = u16(member * 4)\n'
                                                          '        candidate_y = '
                                                          'state.battle_positions.word(unit_offset, '
                                                          '2)\n'
                                                          '        distance_y = u16(candidate_y - '
                                                          'center_y)\n'
                                                          '        if candidate_y < center_y:\n'
                                                          '            distance_y = '
                                                          'u16(-distance_y)\n'
                                                          '        candidate_x = '
                                                          'state.battle_positions.word(unit_offset)\n'
                                                          '        distance_x = u16(candidate_x - '
                                                          'center_x)\n'
                                                          '        if candidate_x < center_x:\n'
                                                          '            distance_x = '
                                                          'u16(-distance_x)\n'
                                                          '        distance = u16(distance_y + '
                                                          'distance_x)\n'
                                                          '        if distance < closest:\n'
                                                          '            closest = distance\n'
                                                          '            selected = member\n'
                                                          "state.set_scalar('selected_officer', "
                                                          'selected)\n'
                                                          'return selected'},
 'test_same_side_total_shortfall': {'signature': 'state: GameState',
                                    'returns': 'CarryOutcome',
                                    'flow': 'checked_state(state)\n'
                                            'primary = state.table(4294964894)\n'
                                            'secondary = state.table(4294964898)\n'
                                            "if state.scalar('battle_side_flags') & 2:\n"
                                            '    primary, secondary = (secondary, primary)\n'
                                            'strength = primary.long()\n'
                                            'if strength >= secondary.long():\n'
                                            '    return state.carry_result(0)\n'
                                            'return state.carry_result(int(strength < '
                                            "state.scalar('primary_strength_limit')))"},
 'collect_contacts_in_speed_radius': {'signature': 'state: GameState, actor: Word',
                                      'returns': 'ContactCollection',
                                      'flow': 'checked_state(state)\n'
                                              'uint(actor, 16)\n'
                                              'radius = u16(state.officer_march_speed.byte(actor) '
                                              '* 10)\n'
                                              'output = state.action_candidates.cursor()\n'
                                              'positions = state.battle_positions\n'
                                              'own_offset = u16(actor * 4)\n'
                                              'own_x = positions.word(own_offset)\n'
                                              'own_y = positions.word(own_offset, 2)\n'
                                              'roster = state.primary_battle_roster if '
                                              "state.scalar('battle_side_flags') & 2 else "
                                              'state.secondary_battle_roster\n'
                                              'candidates = roster.cursor()\n'
                                              'while True:\n'
                                              '    member = candidates.next_word()\n'
                                              '    if negative_word(member):\n'
                                              '        output.put_word(65535)\n'
                                              '        return ContactCollection(radius, own_x, '
                                              'own_y, output, candidates, positions)\n'
                                              '    if state.unit_retreat_flags.byte(member) != 0:\n'
                                              '        continue\n'
                                              '    offset = u16(member * 4)\n'
                                              '    candidate_y = positions.word(offset, 2)\n'
                                              '    distance_y = u16(candidate_y - own_y)\n'
                                              '    if candidate_y < own_y:\n'
                                              '        distance_y = u16(-distance_y)\n'
                                              '    distance_y >>= 7\n'
                                              '    if distance_y > radius:\n'
                                              '        continue\n'
                                              '    candidate_x = positions.word(offset)\n'
                                              '    distance_x = u16(candidate_x - own_x)\n'
                                              '    if candidate_x < own_x:\n'
                                              '        distance_x = u16(-distance_x)\n'
                                              '    distance_x >>= 7\n'
                                              '    if distance_x > radius:\n'
                                              '        continue\n'
                                              '    distance = low16(rounded_radial_distance(state, '
                                              'u32(distance_y * distance_y + distance_x * '
                                              'distance_x)))\n'
                                              '    if distance <= radius:\n'
                                              '        output.append_word(member)'},
 'test_battlefield_leader_roster_presence': {'signature': 'state: GameState',
                                             'returns': 'CarryOutcome',
                                             'flow': 'checked_state(state)\n'
                                                     "scene = state.scalar('battle_scene')\n"
                                                     'leader = scene & 65280 | '
                                                     'state.scene_primary_head.byte(scene)\n'
                                                     'roster = '
                                                     'state.primary_battle_roster.cursor()\n'
                                                     'while True:\n'
                                                     '    member = roster.next_word()\n'
                                                     '    if negative_word(member):\n'
                                                     "        state.set_scalar('route', 1041)\n"
                                                     "        state.set_scalar('command_step', 0)\n"
                                                     "        state.set_scalar('battle_phase', 2)\n"
                                                     '        return state.carry_result(1)\n'
                                                     '    if member == leader:\n'
                                                     '        return state.carry_result(0)'},
 'rounded_radial_distance': {'signature': 'state: GameState, squared_distance: Long',
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
 'seed_radial_distance_from_thresholds': {'signature': 'state: GameState, squared_distance: Long, '
                                                       'retained_count: Long=0, '
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
                                                  'preceding_threshold, thresholds)'}}

def _lower_weighted_training_factor(e, rules):
    e.ins('movem.l', '%d0/%a0,-(%a7)', 4)
    e.ins('lea.l', '0xc500:w,%a0', 4)
    e.ins('clr.w', '%d1', 2)
    e.ins('move.b', '(%a0, %d0.w),%d1', 4)
    e.ins('lea.l', '0xb400:w,%a0', 4)
    e.ins('lsl.w', '#0x1,%d0', 2)
    e.ins('mulu.w', '(%a0, %d0.w),%d1', 4)
    e.ins('divu.w', f"#{rules['training_divisor']},%d1", 4)
    e.ins('movem.l', '(%a7)+,%d0/%a0', 4)

def _lower_load_battlefield_map_context(e, rules):
    e.ins('move.l', '%d4,-(%a7)', 2)
    e.ins('lea.l', '0x945e8:l,%a0', 6)
    e.ins('move.w', '0xf68a:w,%d4', 4)
    e.ins('mulu.w', '#0x8c0,%d4', 4)
    e.ins('adda.l', '%d4,%a0', 2)
    e.ins('move.l', '(%a7)+,%d4', 2)

def _lower_read_battlefield_terrain_type(e, rules):
    e.ins('movem.l', '%d1-%d3/%a0,-(%a7)', 4)
    e.ins('lsr.w', '#0x3,%d1', 2)
    e.ins('move.w', '%d1,%d3', 2)
    e.ins('lsl.w', '#0x2,%d1', 2)
    e.ins('add.w', '%d3,%d1', 2)
    e.ins('lsl.w', '#0x3,%d1', 2)
    e.ins('lsr.w', '#0x3,%d2', 2)
    e.ins('add.w', '%d2,%d1', 2)
    e.ins('lsl.w', '#0x1,%d1', 2)
    e.ins('move.w', '(%a0, %d1.w),%d0', 4)
    e.ins('andi.w', '#0x3ff,%d0', 4)
    e.ins('lea.l', '0x6c0b4:l,%a0', 6)
    e.ins('move.b', '(%a0, %d0.w),%d0', 4)
    e.ins('movem.l', '(%a7)+,%d1-%d3/%a0', 4)

def _lower_constrain_transposed_target_coordinate(e, rules):
    e.ins('move.w', '%d2,%d4', 2)
    e.ins('move.w', '%d3,%d0', 2)
    e.ins('move.w', '%d0,%d1', 2)
    e.ins('move.w', '%d4,%d0', 2)
    e.ins('bsr.w', 'constrain_target_near_battlefield_anchor', 4)
    e.ins('move.w', '%d0,%d4', 2)
    e.ins('move.w', '%d1,%d0', 2)

def _lower_compare_actor_to_weakest_contact_strength(e, rules):
    e.ins('bsr.w', 'collect_contacts_in_speed_radius', 4)
    e.ins('tst.w', '0xd300:w', 4)
    e.ins('bmi.w', 'compare_actor_to_weakest_contact_strength_at_22c46', 4)
    e.ins('bsr.w', 'select_weakest_contact_strength', 4)
    e.ins('move.w', '%d7,%d0', 2)
    e.ins('jsr', 'weighted_training_factor:l', 6)
    e.ins('lsl.w', '#0x2,%d0', 2)
    e.ins('move.l', '(%a1, %d0.w),%d0', 4)
    e.ins('mulu.w', '%d1,%d0', 2)
    e.ins('cmp.l', '%d0,%d2', 2)
    e.ins(rules['actor_failure']+'.w', 'compare_actor_to_weakest_contact_strength_at_22c46', 4)
    e.ins('ori.w', '#0x1,%sr', 4)
    e.ins('bra.w', 'compare_actor_to_weakest_contact_strength_at_22c4a', 4)
    e.label('compare_actor_to_weakest_contact_strength_at_22c46')
    e.ins('andi.w', '#0xfffe,%sr', 4)
    e.label('compare_actor_to_weakest_contact_strength_at_22c4a')

def _lower_select_weakest_contact_strength(e, rules):
    e.ins('lea.l', '0xd300:w,%a0', 4)
    e.ins('lea.l', '0xc800:w,%a1', 4)
    e.ins('moveq', '#-1,%d2', 2)
    e.label('select_weakest_contact_strength_at_22c56')
    e.ins('move.w', '(%a0)+,%d0', 2)
    e.ins('bmi.w', 'select_weakest_contact_strength_at_22c76', 4)
    e.ins('jsr', 'weighted_training_factor:l', 6)
    e.ins('lsl.w', '#0x2,%d0', 2)
    e.ins('move.l', '(%a1, %d0.w),%d4', 4)
    e.ins('mulu.w', '%d1,%d4', 2)
    e.ins('cmp.l', '%d2,%d4', 2)
    e.ins(rules['weakest_failure']+'.b', 'select_weakest_contact_strength_at_22c56', 2)
    e.ins('move.l', '%d4,%d2', 2)
    e.ins('lsr.w', '#0x2,%d0', 2)
    e.ins('move.w', '%d0,%d3', 2)
    e.ins('bra.b', 'select_weakest_contact_strength_at_22c56', 2)
    e.label('select_weakest_contact_strength_at_22c76')

def _lower_constrain_pursuit_target_coordinate(e, rules):
    e.ins('move.w', '%d2,%d0', 2)
    e.ins('move.w', '%d3,%d1', 2)
    e.ins('bsr.w', 'constrain_target_near_battlefield_anchor', 4)
    e.ins('move.w', '%d0,%d4', 2)
    e.ins('move.w', '%d1,%d0', 2)

def _lower_test_other_side_total_shortfall(e, rules):
    e.ins('lea.l', '0xf69e:w,%a0', 4)
    e.ins('lea.l', '0xf6a2:w,%a1', 4)
    e.ins('btst.b', '#0x1,0xf6d7:w', 6)
    e.ins('beq.w', 'test_other_side_total_shortfall_at_22d12', 4)
    e.ins('exg', '%a0,%a1', 2)
    e.label('test_other_side_total_shortfall_at_22d12')
    e.ins('move.l', '(%a1),%d0', 2)
    e.ins('cmp.l', '(%a0),%d0', 2)
    e.ins('bcc.w', 'test_other_side_total_shortfall_at_22d2a', 4)
    e.ins('cmp.l', '0xf76c:w,%d0', 4)
    e.ins('bcc.w', 'test_other_side_total_shortfall_at_22d2a', 4)
    e.ins('ori.w', '#0x1,%sr', 4)
    e.ins('bra.w', 'test_other_side_total_shortfall_at_22d2e', 4)
    e.label('test_other_side_total_shortfall_at_22d2a')
    e.ins('andi.w', '#0xfffe,%sr', 4)
    e.label('test_other_side_total_shortfall_at_22d2e')

def _lower_mark_eligible_actor_for_retreat(e, rules):
    e.ins('bsr.w', 'test_actor_terrain_types_3_or_7', 4)
    e.ins('bcc.w', 'mark_eligible_actor_for_retreat_at_22d96', 4)
    e.ins('lea.l', '0xc800:w,%a0', 4)
    e.ins('move.w', '%d7,%d0', 2)
    e.ins('lsl.w', '#0x2,%d0', 2)
    e.ins('cmpi.l', f"#{rules['retreat_troop_limit']},(%a0, %d0.w)", 8)
    e.ins(rules['retreat_troop_failure']+'.w', 'mark_eligible_actor_for_retreat_at_22d96', 4)
    e.ins('bsr.w', 'count_roster_nonnegative_prefix_bytes', 4)
    e.ins('cmpi.w', '#0x4,%d0', 4)
    e.ins(rules['retreat_prefix_failure']+'.w', 'mark_eligible_actor_for_retreat_at_22d96', 4)
    e.ins('bsr.w', 'collect_contacts_in_speed_radius', 4)
    e.ins('tst.w', '0xd300:w', 4)
    e.ins('bmi.w', 'mark_eligible_actor_for_retreat_at_22d96', 4)
    e.ins('lea.l', '0xff3bc2:l,%a0', 6)
    e.ins('tst.b', '(%a0, %d7.w)', 4)
    e.ins('bne.w', 'mark_eligible_actor_for_retreat_at_22d80', 4)
    e.ins('jsr', 'step_random:l', 6)
    e.ins('btst.l', '#0xf,%d0', 4)
    e.ins('bne.w', 'mark_eligible_actor_for_retreat_at_22d96', 4)
    e.label('mark_eligible_actor_for_retreat_at_22d80')
    e.ins('move.b', '#0x1,(%a0, %d7.w)', 6)
    e.ins('lea.l', '0xae28:w,%a0', 4)
    e.ins('clr.b', '(%a0, %d7.w)', 4)
    e.ins('ori.w', '#0x1,%sr', 4)
    e.ins('bra.w', 'mark_eligible_actor_for_retreat_at_22da4', 4)
    e.label('mark_eligible_actor_for_retreat_at_22d96')
    e.ins('lea.l', '0xff3bc2:l,%a0', 6)
    e.ins('clr.b', '(%a0, %d7.w)', 4)
    e.ins('andi.w', '#0xfffe,%sr', 4)
    e.label('mark_eligible_actor_for_retreat_at_22da4')

def _lower_test_actor_terrain_types_3_or_7(e, rules):
    e.ins('jsr', 'load_battlefield_map_context:l', 6)
    e.ins('lea.l', '0xa150:w,%a1', 4)
    e.ins('move.w', '%d7,%d0', 2)
    e.ins('lsl.w', '#0x2,%d0', 2)
    e.ins('move.w', '(%a1, %d0.w),%d1', 4)
    e.ins('lsr.w', '#0x7,%d1', 2)
    e.ins('move.w', '0x2(%a1, %d0.w),%d2', 4)
    e.ins('lsr.w', '#0x7,%d2', 2)
    e.ins('jsr', 'read_battlefield_terrain_type:l', 6)
    e.ins('cmpi.b', '#0x3,%d0', 4)
    e.ins('beq.w', 'test_actor_terrain_types_3_or_7_at_22dde', 4)
    e.ins('cmpi.b', '#0x7,%d0', 4)
    e.ins('beq.w', 'test_actor_terrain_types_3_or_7_at_22dde', 4)
    e.ins('andi.w', '#0xfffe,%sr', 4)
    e.ins('bra.w', 'test_actor_terrain_types_3_or_7_at_22de2', 4)
    e.label('test_actor_terrain_types_3_or_7_at_22dde')
    e.ins('ori.w', '#0x1,%sr', 4)
    e.label('test_actor_terrain_types_3_or_7_at_22de2')

def _lower_count_roster_nonnegative_prefix_bytes(e, rules):
    e.ins('lea.l', '0xa5a4:w,%a0', 4)
    e.ins('btst.b', '#0x1,0xf6d7:w', 6)
    e.ins('bne.w', 'count_roster_nonnegative_prefix_bytes_at_22df6', 4)
    e.ins('lea.l', '0xa550:w,%a0', 4)
    e.label('count_roster_nonnegative_prefix_bytes_at_22df6')
    e.ins('clr.w', '%d0', 2)
    e.label('count_roster_nonnegative_prefix_bytes_at_22df8')
    e.ins('tst.b', '(%a0)+', 2)
    e.ins('bmi.w', 'count_roster_nonnegative_prefix_bytes_at_22e02', 4)
    e.ins('addq.w', '#0x1,%d0', 2)
    e.ins('bra.b', 'count_roster_nonnegative_prefix_bytes_at_22df8', 2)
    e.label('count_roster_nonnegative_prefix_bytes_at_22e02')

def _lower_constrain_second_pursuit_target_coordinate(e, rules):
    e.ins('move.w', '%d2,%d0', 2)
    e.ins('move.w', '%d3,%d1', 2)
    e.ins('bsr.w', 'constrain_target_near_battlefield_anchor', 4)
    e.ins('move.w', '%d0,%d4', 2)
    e.ins('move.w', '%d1,%d0', 2)

def _lower_test_other_roster_single_member(e, rules):
    e.ins('btst.b', '#0x1,0xf6d7:w', 6)
    e.ins('bne.w', 'test_other_roster_single_member_at_23058', 4)
    e.ins('lea.l', '0xa5a4:w,%a0', 4)
    e.ins('bra.w', 'test_other_roster_single_member_at_2305c', 4)
    e.label('test_other_roster_single_member_at_23058')
    e.ins('lea.l', '0xa550:w,%a0', 4)
    e.label('test_other_roster_single_member_at_2305c')
    e.ins('tst.w', '0x2(%a0)', 4)
    e.ins('bpl.w', 'test_other_roster_single_member_at_2306c', 4)
    e.ins('ori.w', '#0x1,%sr', 4)
    e.ins('bra.w', 'test_other_roster_single_member_at_23070', 4)
    e.label('test_other_roster_single_member_at_2306c')
    e.ins('andi.w', '#0xfffe,%sr', 4)
    e.label('test_other_roster_single_member_at_23070')

def _lower_constrain_target_near_battlefield_anchor(e, rules):
    e.ins('move.w', '%d7,-(%a7)', 2)
    e.ins('lea.l', '0xa150:w,%a0', 4)
    e.ins('move.w', '%d7,%d2', 2)
    e.ins('lsl.w', '#0x2,%d2', 2)
    e.ins('move.w', '(%a0, %d2.w),%d3', 4)
    e.ins('move.w', '0x2(%a0, %d2.w),%d4', 4)
    e.ins('lea.l', '0xae2f6:l,%a0', 6)
    e.ins('move.w', '0xf68a:w,%d5', 4)
    e.ins('lsl.w', '#0x2,%d5', 2)
    e.ins('move.w', '0x2(%a0, %d5.w),%d6', 4)
    e.ins('move.w', '(%a0, %d5.w),%d5', 4)
    e.ins('move.w', '%d3,%d7', 2)
    e.ins('sub.w', '%d5,%d7', 2)
    e.ins('bcc.w', 'constrain_target_near_battlefield_anchor_at_231c8', 4)
    e.ins('neg.w', '%d7', 2)
    e.label('constrain_target_near_battlefield_anchor_at_231c8')
    e.ins('cmpi.w', f"#{rules['anchor_edge']},%d7", 4)
    e.ins('bcs.w', 'constrain_target_near_battlefield_anchor_at_23228', 4)
    e.ins('bhi.w', 'constrain_target_near_battlefield_anchor_at_2328c', 4)
    e.ins('move.w', '%d4,%d7', 2)
    e.ins('sub.w', '%d6,%d7', 2)
    e.ins('bcc.w', 'constrain_target_near_battlefield_anchor_at_231de', 4)
    e.ins('neg.w', '%d7', 2)
    e.label('constrain_target_near_battlefield_anchor_at_231de')
    e.ins('cmpi.w', f"#{rules['anchor_edge']},%d7", 4)
    e.ins('bhi.w', 'constrain_target_near_battlefield_anchor_at_2328c', 4)
    e.ins('cmp.w', '%d5,%d3', 2)
    e.ins('bhi.w', 'constrain_target_near_battlefield_anchor_at_23220', 4)
    e.ins('cmp.w', '%d3,%d0', 2)
    e.ins('bls.w', 'constrain_target_near_battlefield_anchor_at_2328c', 4)
    e.label('constrain_target_near_battlefield_anchor_at_231f2')
    e.ins('cmp.w', '%d6,%d1', 2)
    e.ins('bhi.w', 'constrain_target_near_battlefield_anchor_at_2320c', 4)
    e.ins('move.w', '%d6,%d7', 2)
    e.ins('subi.w', f"#{rules['anchor_edge']},%d7", 4)
    e.ins('cmp.w', '%d4,%d7', 2)
    e.ins('beq.w', 'constrain_target_near_battlefield_anchor_at_2326a', 4)
    e.ins('move.w', '%d3,%d0', 2)
    e.ins('move.w', '%d7,%d1', 2)
    e.ins('bra.w', 'constrain_target_near_battlefield_anchor_at_2328c', 4)
    e.label('constrain_target_near_battlefield_anchor_at_2320c')
    e.ins('move.w', '%d6,%d7', 2)
    e.ins('addi.w', f"#{rules['anchor_edge']},%d7", 4)
    e.ins('cmp.w', '%d4,%d7', 2)
    e.ins('beq.w', 'constrain_target_near_battlefield_anchor_at_2326a', 4)
    e.ins('move.w', '%d3,%d0', 2)
    e.ins('move.w', '%d7,%d1', 2)
    e.ins('bra.w', 'constrain_target_near_battlefield_anchor_at_2328c', 4)
    e.label('constrain_target_near_battlefield_anchor_at_23220')
    e.ins('cmp.w', '%d3,%d0', 2)
    e.ins('bcc.w', 'constrain_target_near_battlefield_anchor_at_2328c', 4)
    e.ins('bra.b', 'constrain_target_near_battlefield_anchor_at_231f2', 2)
    e.label('constrain_target_near_battlefield_anchor_at_23228')
    e.ins('move.w', '%d4,%d7', 2)
    e.ins('sub.w', '%d6,%d7', 2)
    e.ins('bcc.w', 'constrain_target_near_battlefield_anchor_at_23232', 4)
    e.ins('neg.w', '%d7', 2)
    e.label('constrain_target_near_battlefield_anchor_at_23232')
    e.ins('cmpi.w', f"#{rules['anchor_edge']},%d7", 4)
    e.ins('bne.w', 'constrain_target_near_battlefield_anchor_at_2328c', 4)
    e.ins('cmp.w', '%d6,%d4', 2)
    e.ins('bhi.w', 'constrain_target_near_battlefield_anchor_at_23262', 4)
    e.ins('cmp.w', '%d4,%d1', 2)
    e.ins('bls.w', 'constrain_target_near_battlefield_anchor_at_2328c', 4)
    e.label('constrain_target_near_battlefield_anchor_at_23246')
    e.ins('move.w', '%d4,%d1', 2)
    e.ins('cmp.w', '%d5,%d0', 2)
    e.ins('bhi.w', 'constrain_target_near_battlefield_anchor_at_23258', 4)
    e.ins('move.w', '%d5,%d0', 2)
    e.ins('subi.w', f"#{rules['anchor_edge']},%d0", 4)
    e.ins('bra.w', 'constrain_target_near_battlefield_anchor_at_2328c', 4)
    e.label('constrain_target_near_battlefield_anchor_at_23258')
    e.ins('move.w', '%d5,%d0', 2)
    e.ins('addi.w', f"#{rules['anchor_edge']},%d0", 4)
    e.ins('bra.w', 'constrain_target_near_battlefield_anchor_at_2328c', 4)
    e.label('constrain_target_near_battlefield_anchor_at_23262')
    e.ins('cmp.w', '%d4,%d1', 2)
    e.ins('bcc.w', 'constrain_target_near_battlefield_anchor_at_2328c', 4)
    e.ins('bra.b', 'constrain_target_near_battlefield_anchor_at_23246', 2)
    e.label('constrain_target_near_battlefield_anchor_at_2326a')
    e.ins('move.w', '%d3,%d5', 2)
    e.ins('sub.w', '%d0,%d5', 2)
    e.ins('bcc.w', 'constrain_target_near_battlefield_anchor_at_23274', 4)
    e.ins('neg.w', '%d5', 2)
    e.label('constrain_target_near_battlefield_anchor_at_23274')
    e.ins('move.w', '%d4,%d6', 2)
    e.ins('sub.w', '%d1,%d6', 2)
    e.ins('bcc.w', 'constrain_target_near_battlefield_anchor_at_2327e', 4)
    e.ins('neg.w', '%d6', 2)
    e.label('constrain_target_near_battlefield_anchor_at_2327e')
    e.ins('cmp.w', '%d5,%d6', 2)
    e.ins('bhi.w', 'constrain_target_near_battlefield_anchor_at_2328a', 4)
    e.ins('move.w', '%d4,%d1', 2)
    e.ins('bra.w', 'constrain_target_near_battlefield_anchor_at_2328c', 4)
    e.label('constrain_target_near_battlefield_anchor_at_2328a')
    e.ins('move.w', '%d3,%d0', 2)
    e.label('constrain_target_near_battlefield_anchor_at_2328c')
    e.ins('move.w', '(%a7)+,%d7', 2)

def _lower_select_nearest_contact_to_battlefield_center(e, rules):
    e.ins('move.l', '%d7,-(%a7)', 2)
    e.ins('tst.w', '0xd302:w', 4)
    e.ins('bmi.w', 'select_nearest_contact_to_battlefield_center_at_23362', 4)
    e.ins('lea.l', '0xae2f6:l,%a0', 6)
    e.ins('move.w', '0xf68a:w,%d0', 4)
    e.ins('lsl.w', '#0x2,%d0', 2)
    e.ins('move.w', '(%a0, %d0.w),%d1', 4)
    e.ins('move.w', '0x2(%a0, %d0.w),%d2', 4)
    e.ins('lea.l', '0xa150:w,%a0', 4)
    e.ins('lea.l', '0xd300:w,%a1', 4)
    e.ins('move.w', '#0xffff,%d3', 4)
    e.label('select_nearest_contact_to_battlefield_center_at_23334')
    e.ins('move.w', '(%a1)+,%d5', 2)
    e.ins('bmi.w', 'select_nearest_contact_to_battlefield_center_at_23366', 4)
    e.ins('move.w', '%d5,%d6', 2)
    e.ins('lsl.w', '#0x2,%d6', 2)
    e.ins('move.w', '0x2(%a0, %d6.w),%d7', 4)
    e.ins('sub.w', '%d2,%d7', 2)
    e.ins('bcc.w', 'select_nearest_contact_to_battlefield_center_at_2334a', 4)
    e.ins('neg.w', '%d7', 2)
    e.label('select_nearest_contact_to_battlefield_center_at_2334a')
    e.ins('move.w', '(%a0, %d6.w),%d6', 4)
    e.ins('sub.w', '%d1,%d6', 2)
    e.ins('bcc.w', 'select_nearest_contact_to_battlefield_center_at_23356', 4)
    e.ins('neg.w', '%d6', 2)
    e.label('select_nearest_contact_to_battlefield_center_at_23356')
    e.ins('add.w', '%d6,%d7', 2)
    e.ins('cmp.w', '%d3,%d7', 2)
    e.ins(rules['nearest_failure']+'.b', 'select_nearest_contact_to_battlefield_center_at_23334', 2)
    e.ins('move.w', '%d7,%d3', 2)
    e.ins('move.w', '%d5,%d4', 2)
    e.ins('bra.b', 'select_nearest_contact_to_battlefield_center_at_23334', 2)
    e.label('select_nearest_contact_to_battlefield_center_at_23362')
    e.ins('move.w', '0xd300:w,%d4', 4)
    e.label('select_nearest_contact_to_battlefield_center_at_23366')
    e.ins('move.w', '%d4,0xf3a6:w', 4)
    e.ins('move.l', '(%a7)+,%d7', 2)

def _lower_test_same_side_total_shortfall(e, rules):
    e.ins('lea.l', '0xf69e:w,%a0', 4)
    e.ins('lea.l', '0xf6a2:w,%a1', 4)
    e.ins('btst.b', '#0x1,0xf6d7:w', 6)
    e.ins('beq.w', 'test_same_side_total_shortfall_at_233f6', 4)
    e.ins('exg', '%a0,%a1', 2)
    e.label('test_same_side_total_shortfall_at_233f6')
    e.ins('move.l', '(%a0),%d0', 2)
    e.ins('cmp.l', '(%a1),%d0', 2)
    e.ins('bcc.w', 'test_same_side_total_shortfall_at_2340e', 4)
    e.ins('cmp.l', '0xf768:w,%d0', 4)
    e.ins('bcc.w', 'test_same_side_total_shortfall_at_2340e', 4)
    e.ins('ori.w', '#0x1,%sr', 4)
    e.ins('bra.w', 'test_same_side_total_shortfall_at_23412', 4)
    e.label('test_same_side_total_shortfall_at_2340e')
    e.ins('andi.w', '#0xfffe,%sr', 4)
    e.label('test_same_side_total_shortfall_at_23412')

def _lower_collect_contacts_in_speed_radius(e, rules):
    e.ins('lea.l', '0xc400:w,%a0', 4)
    e.ins('clr.w', '%d3', 2)
    e.ins('move.b', '(%a0, %d7.w),%d3', 4)
    e.ins('move.w', '%d3,%d5', 2)
    e.ins('lsl.w', '#0x2,%d3', 2)
    e.ins('add.w', '%d5,%d3', 2)
    e.ins('lsl.w', '#0x1,%d3', 2)
    e.ins('lea.l', '0xd300:w,%a0', 4)
    e.ins('lea.l', '0xa150:w,%a1', 4)
    e.ins('move.w', '%d7,%d2', 2)
    e.ins('lsl.w', '#0x2,%d2', 2)
    e.ins('move.w', '(%a1, %d2.w),%d1', 4)
    e.ins('move.w', '0x2(%a1, %d2.w),%d2', 4)
    e.ins('lea.l', '0xff3bc2:l,%a4', 6)
    e.ins('btst.b', '#0x1,0xf6d7:w', 6)
    e.ins('bne.w', 'collect_contacts_in_speed_radius_at_23510', 4)
    e.ins('lea.l', '0xa5a4:w,%a2', 4)
    e.ins('bra.w', 'collect_contacts_in_speed_radius_at_23514', 4)
    e.label('collect_contacts_in_speed_radius_at_23510')
    e.ins('lea.l', '0xa550:w,%a2', 4)
    e.label('collect_contacts_in_speed_radius_at_23514')
    e.ins('move.w', '(%a2)+,%d4', 2)
    e.ins('bmi.w', 'collect_contacts_in_speed_radius_at_2355c', 4)
    e.ins('tst.b', '(%a4, %d4.w)', 4)
    e.ins('bne.b', 'collect_contacts_in_speed_radius_at_23514', 2)
    e.ins('move.w', '%d4,%d5', 2)
    e.ins('lsl.w', '#0x2,%d5', 2)
    e.ins('move.w', '0x2(%a1, %d5.w),%d0', 4)
    e.ins('sub.w', '%d2,%d0', 2)
    e.ins('bcc.w', 'collect_contacts_in_speed_radius_at_23530', 4)
    e.ins('neg.w', '%d0', 2)
    e.label('collect_contacts_in_speed_radius_at_23530')
    e.ins('lsr.w', '#0x7,%d0', 2)
    e.ins('cmp.w', '%d3,%d0', 2)
    e.ins(rules['axis_skip']+'.b', 'collect_contacts_in_speed_radius_at_23514', 2)
    e.ins('mulu.w', '%d0,%d0', 2)
    e.ins('move.w', '(%a1, %d5.w),%d5', 4)
    e.ins('sub.w', '%d1,%d5', 2)
    e.ins('bcc.w', 'collect_contacts_in_speed_radius_at_23544', 4)
    e.ins('neg.w', '%d5', 2)
    e.label('collect_contacts_in_speed_radius_at_23544')
    e.ins('lsr.w', '#0x7,%d5', 2)
    e.ins('cmp.w', '%d3,%d5', 2)
    e.ins(rules['axis_skip']+'.b', 'collect_contacts_in_speed_radius_at_23514', 2)
    e.ins('mulu.w', '%d5,%d5', 2)
    e.ins('add.l', '%d5,%d0', 2)
    e.ins('jsr', 'rounded_radial_distance:l', 6)
    e.ins('cmp.w', '%d3,%d0', 2)
    e.ins(rules['radial_failure']+'.b', 'collect_contacts_in_speed_radius_at_23514', 2)
    e.ins('move.w', '%d4,(%a0)+', 2)
    e.ins('bra.b', 'collect_contacts_in_speed_radius_at_23514', 2)
    e.label('collect_contacts_in_speed_radius_at_2355c')
    e.ins('move.w', '#0xffff,(%a0)', 4)

def _lower_test_battlefield_leader_roster_presence(e, rules):
    e.ins('movem.l', '%d0-%d1/%a0,-(%a7)', 4)
    e.ins('lea.l', '0xa027:w,%a0', 4)
    e.ins('move.w', '0xf68a:w,%d0', 4)
    e.ins('move.b', '(%a0, %d0.w),%d0', 4)
    e.ins('lea.l', '0xa550:w,%a0', 4)
    e.label('test_battlefield_leader_roster_presence_at_235e0')
    e.ins('move.w', '(%a0)+,%d1', 2)
    e.ins('bmi.w', 'test_battlefield_leader_roster_presence_at_235f6', 4)
    e.ins('cmp.w', '%d0,%d1', 2)
    e.ins('bne.b', 'test_battlefield_leader_roster_presence_at_235e0', 2)
    e.ins('movem.l', '(%a7)+,%d0-%d1/%a0', 4)
    e.ins('andi.w', '#0xfffe,%sr', 4)
    e.ins('bra.w', 'test_battlefield_leader_roster_presence_at_2360e', 4)
    e.label('test_battlefield_leader_roster_presence_at_235f6')
    e.ins('movem.l', '(%a7)+,%d0-%d1/%a0', 4)
    e.ins('move.w', '#0x411,0xf612:w', 6)
    e.ins('clr.w', '0xf362:w', 4)
    e.ins('move.w', '#0x2,0xf6d6:w', 6)
    e.ins('ori.w', '#0x1,%sr', 4)
    e.label('test_battlefield_leader_roster_presence_at_2360e')

def _lower_rounded_radial_distance(e, rules):
    e.ins('movem.l', '%d1-%d3/%a0,-(%a7)', 4)
    e.ins('tst.l', '%d0', 2)
    e.ins('beq.w', 'rounded_radial_distance_at_3082a', 4)
    e.ins('bsr.w', 'seed_radial_distance_from_thresholds', 4)
    e.label('rounded_radial_distance_at_3081c')
    e.ins('sub.l', '%d2,%d0', 2)
    e.ins('bcs.w', 'rounded_radial_distance_at_30828', 4)
    e.ins('addq.w', '#0x1,%d1', 2)
    e.ins('addq.w', '#0x2,%d2', 2)
    e.ins('bra.b', 'rounded_radial_distance_at_3081c', 2)
    e.label('rounded_radial_distance_at_30828')
    e.ins('move.w', '%d1,%d0', 2)
    e.label('rounded_radial_distance_at_3082a')
    e.ins('movem.l', '(%a7)+,%d1-%d3/%a0', 4)

def _lower_seed_radial_distance_from_thresholds(e, rules):
    e.ins('cmpi.l', '#0x2358d,%d0', 6)
    e.ins('bcs.b', 'seed_radial_distance_from_thresholds_at_3084c', 2)
    e.ins('subi.l', '#0x2358d,%d0', 6)
    e.ins('move.l', '#0x2fa,%d2', 6)
    e.ins('move.w', '#0x17d,%d1', 4)
    e.ins('bra.w', 'seed_radial_distance_from_thresholds_at_30874', 4)
    e.label('seed_radial_distance_from_thresholds_at_3084c')
    e.ins('clr.w', '%d1', 2)
    e.ins('moveq', '#1,%d2', 2)
    e.ins('clr.w', '%d3', 2)
    e.ins('lea.l', 'seed_radial_distance_from_thresholds_end(%pc),%a0', 4)
    e.label('seed_radial_distance_from_thresholds_at_30856')
    e.ins('cmp.l', '(%a0),%d0', 2)
    e.ins('bcs.w', 'seed_radial_distance_from_thresholds_at_30860', 4)
    e.ins('addq.l', '#0x6,%a0', 2)
    e.ins('bra.b', 'seed_radial_distance_from_thresholds_at_30856', 2)
    e.label('seed_radial_distance_from_thresholds_at_30860')
    e.ins('move.l', '-0x6(%a0),%d3', 4)
    e.ins('move.w', '-0x2(%a0),%d2', 4)
    e.ins('sub.l', '%d3,%d0', 2)
    e.ins('move.w', '%d2,%d1', 2)
    e.ins('lsr.w', '#0x1,%d1', 2)
    e.ins('andi.l', '#0xffff,%d2', 6)
    e.label('seed_radial_distance_from_thresholds_at_30874')

LOWERERS = {
    'weighted_training_factor': _lower_weighted_training_factor,
    'load_battlefield_map_context': _lower_load_battlefield_map_context,
    'read_battlefield_terrain_type': _lower_read_battlefield_terrain_type,
    'constrain_transposed_target_coordinate': _lower_constrain_transposed_target_coordinate,
    'compare_actor_to_weakest_contact_strength': _lower_compare_actor_to_weakest_contact_strength,
    'select_weakest_contact_strength': _lower_select_weakest_contact_strength,
    'constrain_pursuit_target_coordinate': _lower_constrain_pursuit_target_coordinate,
    'test_other_side_total_shortfall': _lower_test_other_side_total_shortfall,
    'mark_eligible_actor_for_retreat': _lower_mark_eligible_actor_for_retreat,
    'test_actor_terrain_types_3_or_7': _lower_test_actor_terrain_types_3_or_7,
    'count_roster_nonnegative_prefix_bytes': _lower_count_roster_nonnegative_prefix_bytes,
    'constrain_second_pursuit_target_coordinate': _lower_constrain_second_pursuit_target_coordinate,
    'test_other_roster_single_member': _lower_test_other_roster_single_member,
    'constrain_target_near_battlefield_anchor': _lower_constrain_target_near_battlefield_anchor,
    'select_nearest_contact_to_battlefield_center': _lower_select_nearest_contact_to_battlefield_center,
    'test_same_side_total_shortfall': _lower_test_same_side_total_shortfall,
    'collect_contacts_in_speed_radius': _lower_collect_contacts_in_speed_radius,
    'test_battlefield_leader_roster_presence': _lower_test_battlefield_leader_roster_presence,
    'rounded_radial_distance': _lower_rounded_radial_distance,
    'seed_radial_distance_from_thresholds': _lower_seed_radial_distance_from_thresholds,
}

DECLARATIONS.update({'rounded_deployment_radial_distance_fields': {'signature': 'memory: BattlePolicyMemory, frame: '
                                                            'FirstDeploymentFrame',
                                               'returns': 'FirstDeploymentFrame',
                                               'flow': 'if type(memory) is not BattlePolicyMemory '
                                                       'or type(frame) is not '
                                                       'FirstDeploymentFrame:\n'
                                                       "    raise ValueError('same-state radial "
                                                       "memory and actual frame required')\n"
                                                       'frame.validate(memory.state, '
                                                       'frame.stack_cursor is not None)\n'
                                                       'uint(frame.target_x, 32)\n'
                                                       'original = frame.target_x\n'
                                                       'stack = frame.stack_cursor\n'
                                                       'if stack is not None:\n'
                                                       '    checked_policy_table(frame.roster, '
                                                       'memory.state)\n'
                                                       '    for saved in (frame.roster.base, '
                                                       'frame.count, frame.unit, frame.target_y):\n'
                                                       '        uint(saved, 32)\n'
                                                       '        stack = stack.advance(-4)\n'
                                                       '        stack.set_long(0, saved)\n'
                                                       'radial = RadialMemory(memory.state, '
                                                       'stack)\n'
                                                       'result = _rounded_radial_fields(radial, '
                                                       'original)\n'
                                                       'stack = radial.stack_cursor\n'
                                                       'returned = first_replace(frame, '
                                                       'target_x=result.value)\n'
                                                       'if stack is not None:\n'
                                                       '    restored_y = stack.long()\n'
                                                       '    stack = stack.advance(4)\n'
                                                       '    restored_unit = stack.long()\n'
                                                       '    stack = stack.advance(4)\n'
                                                       '    restored_count = stack.long()\n'
                                                       '    stack = stack.advance(4)\n'
                                                       '    restored_roster = '
                                                       'memory.state.table(stack.long()).cursor()\n'
                                                       '    stack = stack.advance(4)\n'
                                                       '    returned = first_replace(returned, '
                                                       'target_y=restored_y, unit=restored_unit, '
                                                       'count=restored_count, '
                                                       'roster=restored_roster, '
                                                       'stack_cursor=stack)\n'
                                                       'extend = (None if frame.status is None '
                                                       'else frame.status & 16) if original == 0 '
                                                       'else 16\n'
                                                       'status = None if extend is None else '
                                                       'extend | int(result.carry) | (2 if '
                                                       'result.overflow else 0) | (4 if '
                                                       'result.zero else 0) | (8 if '
                                                       'result.negative else 0)\n'
                                                       'return first_replace(returned, '
                                                       'status=status).validate(memory.state, '
                                                       'frame.stack_cursor is not None)'}})


def compile_geometry(source, *, selected_names=None):
    normalized, policies, actual = _geometry_policies(source)
    declarations = dict(DECLARATIONS, **DOMAIN_DECLARATIONS)
    records = semantic_functions(normalized, declarations, APPROVED)
    terrain_fields = records.pop('read_battlefield_terrain_type_fields')
    records['read_battlefield_terrain_type']['effects'] += '\nactual sole terrain fields: ' + terrain_fields['effects']
    leader_fields = records.pop('test_battlefield_leader_roster_presence_fields')
    records['test_battlefield_leader_roster_presence']['effects'] += '\nactual sole leader-roster transaction: ' + leader_fields['effects']
    map_fields = records.pop('load_battlefield_map_fields')
    records['load_battlefield_map_context']['effects'] += '\nactual supplied map-reader fields: ' + map_fields['effects']
    helper_records = {name: records.pop(name) for name in INLINE_HELPERS}
    if helper_records['weighted_training_factor_fields']['rules']['training_divisor'] != helper_records['packed_training_strength']['rules']['training_divisor']:
        raise CompileError('training value and actual field flags require one coupled divisor')
    records['weighted_training_factor']['rules'].update(helper_records['packed_training_strength']['rules'])
    records['constrain_target_near_battlefield_anchor']['rules'].update(helper_records['constrain_target_near_battlefield_anchor_fields']['rules'])
    records['mark_eligible_actor_for_retreat']['rules'].update(helper_records['retreat_troops_are_eligible']['rules'])
    for policy, (target, role, _, _) in POLICY_BINDINGS.items():
        records[target]['rules'][role] = policies[policy]
    for name in DOMAIN_BODIES:
        records[name]['effects'] += '\nfinite-inline actual supplied helper effects:\n' + '\n'.join((ast.dump(actual[helper], include_attributes=False) for helper in INLINE_HELPERS))
    for owner in ('test_other_roster_single_member', 'constrain_target_near_battlefield_anchor', 'select_nearest_contact_to_battlefield_center', 'test_same_side_total_shortfall'):
        records[owner]['effects'] += '\nsole contact-anchor full fields: ' + repr({name: helper_records[name]['effects'] for name in ('_contact_strategy_actor_slot_fields', '_contact_strategy_axis_distance_fields', 'test_other_roster_single_member_fields', 'constrain_target_near_battlefield_anchor_fields', 'select_nearest_contact_to_battlefield_center_fields', 'test_same_side_total_shortfall_fields')})
    records['test_other_side_total_shortfall']['effects'] += '\nsole other-side threshold full fields: ' + helper_records['test_other_side_total_shortfall_fields']['effects']
    if selected_names is not None:
        if type(selected_names) is not tuple or (selected_names != CONTACT_NATIVE_NAMES and selected_names != ('test_other_side_total_shortfall',)):
            raise CompileError('only the fixed complete contact family or sole other-side50B threshold is admitted')
        selected_bindings = tuple((binding for binding in GEOMETRY_BINDINGS if binding.name in selected_names))
        if len(selected_bindings) != len(selected_names):
            raise CompileError('all selected contact whole owners are required')
        selected_lowerers = {name: LOWERERS[name] for name in selected_names}
        return lower_declared({name: records[name] for name in selected_names}, selected_bindings, selected_lowerers)
    return lower_declared(records, GEOMETRY_BINDINGS, LOWERERS)


# A finite inlining contract, not arbitrary Python or a hidden runtime source.
# Complete reader/calculation/control AST is admitted; only these unsigned
# comparison operators and the already supported divisor/troop limit may vary.
POLICY_BINDINGS = {
    'weakest_contact_is_outmatched': ('compare_actor_to_weakest_contact_strength', 'actor_failure', ast.LtE, False),
    'is_weaker_contact': ('select_weakest_contact_strength', 'weakest_failure', ast.Lt, False),
    'retreat_troops_are_eligible': ('mark_eligible_actor_for_retreat', 'retreat_troop_failure', ast.LtE, False),
    'retreat_roster_is_sufficient': ('mark_eligible_actor_for_retreat', 'retreat_prefix_failure', ast.GtE, False),
    'is_nearer_contact': ('select_nearest_contact_to_battlefield_center', 'nearest_failure', ast.Lt, False),
    'axis_outside_contact_radius': ('collect_contacts_in_speed_radius', 'axis_skip', ast.Gt, True),
    'radial_contact_is_in_range': ('collect_contacts_in_speed_radius', 'radial_failure', ast.LtE, False),
}


def _geometry_policies(source):
    if type(source) is not str or len(source) > 300000:
        raise CompileError('bounded explicit geometry Python required')
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError) as exc:
        raise CompileError('invalid geometry Python') from exc
    functions = {}
    actual = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            if node.name in functions:
                raise CompileError('one complete geometry declaration required')
            functions[node.name] = node
            actual[node.name] = ast.parse(ast.unparse(node)).body[0]
    true_branch = {ast.Lt: 'bcs', ast.LtE: 'bls', ast.Gt: 'bhi', ast.GtE: 'bcc', ast.Eq: 'beq', ast.NotEq: 'bne'}
    false_branch = {ast.Lt: 'bcc', ast.LtE: 'bhi', ast.Gt: 'bls', ast.GtE: 'bcs', ast.Eq: 'bne', ast.NotEq: 'beq'}
    policies = {}
    for name, (_, _, canonical, true_on_branch) in POLICY_BINDINGS.items():
        fn = functions.get(name)
        if fn is None or not fn.body or not isinstance(fn.body[-1], ast.Return):
            raise CompileError('complete explicit geometry policy return required')
        comparison = fn.body[-1].value
        if (not isinstance(comparison, ast.Compare) or len(comparison.ops) != 1 or
                len(comparison.comparators) != 1 or type(comparison.ops[0]) not in true_branch):
            raise CompileError('one unsigned geometry comparison required')
        policies[name] = (true_branch if true_on_branch else false_branch)[type(comparison.ops[0])]
        comparison.ops = [canonical()]
    return ast.unparse(tree), policies, actual


APPROVED['contexts_geometry'].update({'TrainingInputs', 'WeightedContact', 'ContactSearch', 'RadialStep'})

DOMAIN_BODIES = ('weighted_training_factor', 'load_battlefield_map_context', 'read_battlefield_terrain_type', 'compare_actor_to_weakest_contact_strength', 'select_weakest_contact_strength', 'mark_eligible_actor_for_retreat', 'test_actor_terrain_types_3_or_7', 'count_roster_nonnegative_prefix_bytes', 'select_nearest_contact_to_battlefield_center', 'collect_contacts_in_speed_radius', 'rounded_radial_distance', 'seed_radial_distance_from_thresholds')
INLINE_HELPERS = ('read_training_inputs', 'packed_training_strength', 'battlefield_map_offset', 'battlefield_cell_offset', 'weakest_contact_is_outmatched', 'read_contact_weighted_strength', 'is_weaker_contact', 'retreat_troops_are_eligible', 'retreat_roster_is_sufficient', 'retreat_random_gate', 'commit_actor_retreat', 'terrain_is_retreat_compatible', 'is_nearer_contact', 'wrapped_axis_distance', 'read_contact_search', 'read_vertical_contact_distance', 'read_horizontal_contact_distance', 'axis_outside_contact_radius', 'radial_contact_is_in_range', 'squared_contact_distance', 'subtract_radial_increment', 'radial_seed_from_previous_threshold')
INLINE_HELPERS += ('_rounded_radial_fields', '_seed_radial_fields', '_radial_previous_fields', 'rounded_scene_radial_distance')
DOMAIN_DECLARATIONS = {'read_training_inputs': {'signature': 'state: GameState, unit: Word', 'returns': 'TrainingInputs', 'flow': 'checked_state(state)\nreturn read_training_inputs_fields(BattlePolicyMemory(state), unit)'},
 'packed_training_strength': {'signature': 'inputs: TrainingInputs',
                              'returns': 'Long',
                              'flow': 'if type(inputs) is not TrainingInputs:\n'
                                      "    raise ValueError('typed live training inputs required')\n"
                                      'return divu_retained(inputs.training * inputs.rating, 100)',
                              'slots': {100: ('training_divisor', 1, 65535)}},
 'weighted_training_factor': {'signature': 'state: GameState, unit: Word', 'returns': 'Long', 'flow': 'checked_state(state)\nreturn weighted_training_factor_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), unit).factor'},
 'battlefield_map_offset': {'signature': 'scene: Word',
                            'returns': 'Long',
                            'flow': 'uint(scene, 16)\nreturn scene * 2240'},
 'load_battlefield_map_context': {'signature': 'state: GameState', 'returns': 'Table', 'flow': 'checked_state(state)\nreturn load_battlefield_map_fields(BattlePolicyMemory(state))'},
 'battlefield_cell_offset': {'signature': 'x: Word, y: Word',
                             'returns': 'Word',
                             'flow': 'uint(x, 16)\nuint(y, 16)\nreturn u16(((x >> 3) * 40 + (y >> 3)) * 2)'},
 'read_battlefield_terrain_type': {'signature': 'state: GameState, map_context: Table, x: Word, y: Word, '
                                                'retained: Long=0',
                                   'returns': 'Long',
                                   'flow': 'checked_state(state)\n'
                                           'checked_table(map_context, state)\n'
                                           'uint(x, 16)\n'
                                           'uint(y, 16)\n'
                                           'uint(retained, 32)\n'
                                           'offset = battlefield_cell_offset(x, y)\n'
                                           'tile = map_context.word(offset) & 1023\n'
                                           'carrier = replace_word(retained, tile)\n'
                                           'return replace_byte(carrier, '
                                           'state.terrain_category_lookup.byte(tile))'},
 'compare_actor_to_weakest_contact_strength': {'signature': 'state: GameState, actor: Word',
                                               'returns': 'CarryOutcome',
                                               'flow': 'checked_state(state)\n'
                                                       'uint(actor, 16)\n'
                                                       'collect_contacts_in_speed_radius(state, actor)\n'
                                                       'if negative_word(state.action_candidates.word()):\n'
                                                       '    return state.carry_result(0)\n'
                                                       'weakest = select_weakest_contact_strength(state)\n'
                                                       'training = weighted_training_factor(state, actor)\n'
                                                       'troops = weakest.troops.long(u16(actor * 4))\n'
                                                       'own_strength = low16(troops) * low16(training)\n'
                                                       'return '
                                                       'state.carry_result(int(weakest_contact_is_outmatched(weakest.strength, '
                                                       'own_strength)))'},
 'weakest_contact_is_outmatched': {'signature': 'weakest: Long, own: Long',
                                   'returns': 'bool',
                                   'flow': 'uint(weakest, 32)\nuint(own, 32)\nreturn weakest <= own'},
 'read_contact_weighted_strength': {'signature': 'state: GameState, troops: Table, member: Word',
                                    'returns': 'WeightedContact',
                                    'flow': 'checked_state(state)\n'
                                            'checked_table(troops, state)\n'
                                            'uint(member, 16)\n'
                                            'weighting = weighted_training_factor(state, member)\n'
                                            'offset = u16(member * 4)\n'
                                            'strength = low16(troops.long(offset)) * low16(weighting)\n'
                                            'return WeightedContact(strength, offset, weighting)'},
 'is_weaker_contact': {'signature': 'strength: Long, weakest: Long',
                       'returns': 'bool',
                       'flow': 'uint(strength, 32)\nuint(weakest, 32)\nreturn strength < weakest'},
 'select_weakest_contact_strength': {'signature': 'state: GameState, retained_member: Word=0, '
                                                  'retained_weighting: Long=0',
                                     'returns': 'ContactStrength',
                                     'flow': 'checked_state(state)\n'
                                             'uint(retained_member, 16)\n'
                                             'uint(retained_weighting, 32)\n'
                                             'candidates = state.action_candidates.cursor()\n'
                                             'troops = state.officer_troops\n'
                                             'best_strength = 4294967295\n'
                                             'best_member = retained_member\n'
                                             'last_weighting = retained_weighting\n'
                                             'while True:\n'
                                             '    member = candidates.next_word()\n'
                                             '    if negative_word(member):\n'
                                             '        return ContactStrength(best_strength, best_member, '
                                             'last_weighting, candidates, troops)\n'
                                             '    candidate = read_contact_weighted_strength(state, troops, '
                                             'member)\n'
                                             '    last_weighting = candidate.weighting\n'
                                             '    if is_weaker_contact(candidate.strength, best_strength):\n'
                                             '        best_strength = candidate.strength\n'
                                             '        best_member = candidate.offset >> 2'},
 'mark_eligible_actor_for_retreat': {'signature': 'state: GameState, actor: Word',
                                     'returns': 'CarryOutcome',
                                     'flow': 'checked_state(state)\n'
                                             'uint(actor, 16)\n'
                                             'eligible = test_actor_terrain_types_3_or_7(state, actor).carry '
                                             '== 1\n'
                                             'if eligible:\n'
                                             '    eligible = '
                                             'retreat_troops_are_eligible(state.officer_troops.long(u16(actor '
                                             '* 4)))\n'
                                             'if eligible:\n'
                                             '    eligible = '
                                             'retreat_roster_is_sufficient(count_roster_nonnegative_prefix_bytes(state))\n'
                                             'if eligible:\n'
                                             '    collect_contacts_in_speed_radius(state, actor)\n'
                                             '    eligible = not '
                                             'negative_word(state.action_candidates.word())\n'
                                             'if eligible:\n'
                                             '    marked = state.unit_retreat_flags.byte(actor)\n'
                                             '    if marked == 0:\n'
                                             '        eligible = retreat_random_gate(state.sample_random())\n'
                                             'return commit_actor_retreat(state, actor, eligible)'},
 'retreat_troops_are_eligible': {'signature': 'troops: Long',
                                 'returns': 'bool',
                                 'flow': 'uint(troops, 32)\nreturn troops <= 5000',
                                 'slots': {5000: ('retreat_troop_limit', 0, 4294967295)}},
 'retreat_roster_is_sufficient': {'signature': 'prefix_bytes: Word',
                                  'returns': 'bool',
                                  'flow': 'uint(prefix_bytes, 16)\nreturn prefix_bytes >= 4'},
 'retreat_random_gate': {'signature': 'sample: Long',
                         'returns': 'bool',
                         'flow': 'uint(sample, 32)\nreturn not bool(sample & 32768)'},
 'commit_actor_retreat': {'signature': 'state: GameState, actor: Word, eligible: bool',
                          'returns': 'CarryOutcome',
                          'flow': 'checked_state(state)\n'
                                  'uint(actor, 16)\n'
                                  'if type(eligible) is not bool:\n'
                                  "    raise ValueError('strict retreat decision required')\n"
                                  'if not eligible:\n'
                                  '    state.unit_retreat_flags.set_byte(actor, 0)\n'
                                  '    return state.carry_result(0)\n'
                                  'state.unit_retreat_flags.set_byte(actor, 1)\n'
                                  'state.deployed_flags.set_byte(actor, 0)\n'
                                  'return state.carry_result(1)'},
 'test_actor_terrain_types_3_or_7': {'signature': 'state: GameState, actor: Word',
                                     'returns': 'CarryOutcome',
                                     'flow': 'checked_state(state)\n'
                                             'uint(actor, 16)\n'
                                             'map_context = load_battlefield_map_context(state)\n'
                                             'offset = u16(actor * 4)\n'
                                             'x = state.battle_positions.word(offset) >> 7\n'
                                             'y = state.battle_positions.word(offset, 2) >> 7\n'
                                             'terrain = low8(read_battlefield_terrain_type(state, '
                                             'map_context, x, y))\n'
                                             'return '
                                             'state.carry_result(int(terrain_is_retreat_compatible(terrain)))'},
 'terrain_is_retreat_compatible': {'signature': 'terrain: Word',
                                   'returns': 'bool',
                                   'flow': 'uint(terrain, 16)\nreturn terrain == 3 or terrain == 7'},
 'count_roster_nonnegative_prefix_bytes': {'signature': 'state: GameState',
                                           'returns': 'Word',
                                           'flow': 'checked_state(state)\n'
                                                   'roster = state.secondary_battle_roster if '
                                                   "state.scalar('battle_side_flags') & 2 else "
                                                   'state.primary_battle_roster\n'
                                                   'source = roster.cursor()\n'
                                                   'count = 0\n'
                                                   'while not negative_byte(source.next_byte()):\n'
                                                   '    count = u16(count + 1)\n'
                                                   'return count'},
 'select_nearest_contact_to_battlefield_center': {'signature': 'state: GameState, retained_member: Word=0',
                                                  'returns': 'Word',
                                                  'flow': 'checked_state(state)\n'
                                                          'uint(retained_member, 16)\n'
                                                          'if negative_word(state.action_candidates.word(0, '
                                                          '2)):\n'
                                                          '    selected = state.action_candidates.word()\n'
                                                          'else:\n'
                                                          "    offset = u16(state.scalar('battle_scene') * "
                                                          '4)\n'
                                                          '    center_x = '
                                                          'state.scene_anchor_positions.word(offset)\n'
                                                          '    center_y = '
                                                          'state.scene_anchor_positions.word(offset, 2)\n'
                                                          '    candidates = '
                                                          'state.action_candidates.cursor()\n'
                                                          '    closest = 65535\n'
                                                          '    selected = retained_member\n'
                                                          '    while True:\n'
                                                          '        member = candidates.next_word()\n'
                                                          '        if negative_word(member):\n'
                                                          '            break\n'
                                                          '        unit_offset = u16(member * 4)\n'
                                                          '        candidate_y = '
                                                          'state.battle_positions.word(unit_offset, 2)\n'
                                                          '        distance_y = '
                                                          'wrapped_axis_distance(candidate_y, center_y)\n'
                                                          '        candidate_x = '
                                                          'state.battle_positions.word(unit_offset)\n'
                                                          '        distance_x = '
                                                          'wrapped_axis_distance(candidate_x, center_x)\n'
                                                          '        distance = u16(distance_y + distance_x)\n'
                                                          '        if is_nearer_contact(distance, closest):\n'
                                                          '            closest = distance\n'
                                                          '            selected = member\n'
                                                          "state.set_scalar('selected_officer', selected)\n"
                                                          'return selected'},
 'is_nearer_contact': {'signature': 'distance: Word, closest: Word',
                       'returns': 'bool',
                       'flow': 'uint(distance, 16)\nuint(closest, 16)\nreturn distance < closest'},
 'wrapped_axis_distance': {'signature': 'coordinate: Word, origin: Word',
                           'returns': 'Word',
                           'flow': 'uint(coordinate, 16)\n'
                                   'uint(origin, 16)\n'
                                   'distance = u16(coordinate - origin)\n'
                                   'if coordinate < origin:\n'
                                   '    distance = u16(-distance)\n'
                                   'return distance'},
 'collect_contacts_in_speed_radius': {'signature': 'state: GameState, actor: Word',
                                      'returns': 'ContactCollection',
                                      'flow': 'checked_state(state)\n'
                                              'uint(actor, 16)\n'
                                              'search = read_contact_search(state, actor)\n'
                                              'output, positions, candidates = (search.output, '
                                              'search.positions, search.roster)\n'
                                              'while True:\n'
                                              '    member = candidates.next_word()\n'
                                              '    if negative_word(member):\n'
                                              '        output.put_word(65535)\n'
                                              '        return ContactCollection(search.radius, '
                                              'search.origin.x, search.origin.y, output, candidates, '
                                              'positions)\n'
                                              '    if state.unit_retreat_flags.byte(member) != 0:\n'
                                              '        continue\n'
                                              '    distance_y = read_vertical_contact_distance(state, '
                                              'positions, member, search.origin.y)\n'
                                              '    if axis_outside_contact_radius(distance_y, '
                                              'search.radius):\n'
                                              '        continue\n'
                                              '    distance_x = read_horizontal_contact_distance(state, '
                                              'positions, member, search.origin.x)\n'
                                              '    if axis_outside_contact_radius(distance_x, '
                                              'search.radius):\n'
                                              '        continue\n'
                                              '    squared = squared_contact_distance(distance_y, '
                                              'distance_x)\n'
                                              '    distance = low16(rounded_radial_distance(state, '
                                              'squared))\n'
                                              '    if radial_contact_is_in_range(distance, search.radius):\n'
                                              '        output.append_word(member)'},
 'read_contact_search': {'signature': 'state: GameState, actor: Word',
                         'returns': 'ContactSearch',
                         'flow': 'checked_state(state)\n'
                                 'uint(actor, 16)\n'
                                 'radius = u16(state.officer_march_speed.byte(actor) * 10)\n'
                                 'output = state.action_candidates.cursor()\n'
                                 'positions = state.battle_positions\n'
                                 'own_offset = u16(actor * 4)\n'
                                 'own_x = positions.word(own_offset)\n'
                                 'own_y = positions.word(own_offset, 2)\n'
                                 "roster = state.primary_battle_roster if state.scalar('battle_side_flags') "
                                 '& 2 else state.secondary_battle_roster\n'
                                 'candidates = roster.cursor()\n'
                                 'return ContactSearch(radius, TargetCoordinate(own_x, own_y), output, '
                                 'candidates, positions)'},
 'read_vertical_contact_distance': {'signature': 'state: GameState, positions: Table, member: Word, origin: '
                                                 'Word',
                                    'returns': 'Word',
                                    'flow': 'checked_state(state)\n'
                                            'checked_table(positions, state)\n'
                                            'uint(member, 16)\n'
                                            'uint(origin, 16)\n'
                                            'return wrapped_axis_distance(positions.word(u16(member * 4), '
                                            '2), origin) >> 7'},
 'read_horizontal_contact_distance': {'signature': 'state: GameState, positions: Table, member: Word, '
                                                   'origin: Word',
                                      'returns': 'Word',
                                      'flow': 'checked_state(state)\n'
                                              'checked_table(positions, state)\n'
                                              'uint(member, 16)\n'
                                              'uint(origin, 16)\n'
                                              'return wrapped_axis_distance(positions.word(u16(member * 4)), '
                                              'origin) >> 7'},
 'axis_outside_contact_radius': {'signature': 'distance: Word, radius: Word',
                                 'returns': 'bool',
                                 'flow': 'uint(distance, 16)\nuint(radius, 16)\nreturn distance > radius'},
 'radial_contact_is_in_range': {'signature': 'distance: Word, radius: Word',
                                'returns': 'bool',
                                'flow': 'uint(distance, 16)\nuint(radius, 16)\nreturn distance <= radius'},
 'squared_contact_distance': {'signature': 'y_distance: Word, x_distance: Word',
                              'returns': 'Long',
                              'flow': 'uint(y_distance, 16)\n'
                                      'uint(x_distance, 16)\n'
                                      'return u32(y_distance * y_distance + x_distance * x_distance)'},
 'rounded_radial_distance': {'signature': 'state: GameState, squared_distance: Long',
                             'returns': 'Long',
                             'flow': 'checked_state(state)\n'
                                     'return _rounded_radial_fields(RadialMemory(state), '
                                     'squared_distance).value'},
 'subtract_radial_increment': {'signature': 'remaining: Long, increment: Long',
                               'returns': 'RadialStep',
                               'flow': 'uint(remaining, 32)\n'
                                       'uint(increment, 32)\n'
                                       'return RadialStep(u32(remaining - increment), remaining < '
                                       'increment)'},
 'seed_radial_distance_from_thresholds': {'signature': 'state: GameState, squared_distance: Long, '
                                                       'retained_count: Long=0, retained_threshold: Long=0',
                                          'returns': 'RadialSeed',
                                          'flow': 'checked_state(state)\n'
                                                  'fields = _seed_radial_fields(RadialMemory(state), '
                                                  'squared_distance, retained_count, retained_threshold)\n'
                                                  'return RadialSeed(fields.remaining, fields.count, '
                                                  'fields.increment, fields.last_threshold, '
                                                  'fields.threshold_cursor)'},
 'radial_seed_from_previous_threshold': {'signature': 'squared_distance: Long, retained_count: Long, '
                                                      'increment: Word, previous: Long, cursor: Table',
                                         'returns': 'RadialSeed',
                                         'flow': 'checked_table(cursor)\n'
                                                 'fields = _radial_previous_fields(squared_distance, '
                                                 'retained_count, increment, previous, cursor)\n'
                                                 'return RadialSeed(fields.remaining, fields.count, '
                                                 'fields.increment, fields.last_threshold, '
                                                 'fields.threshold_cursor)'},
 '_radial_previous_fields': {'signature': 'squared_distance: Long, retained_count: Long, increment: Word, '
                                          'previous: Long, cursor: RadialTable',
                             'returns': 'RadialSeedFields',
                             'flow': 'uint(squared_distance, 32)\n'
                                     'uint(retained_count, 32)\n'
                                     'uint(increment, 16)\n'
                                     'uint(previous, 32)\n'
                                     'checked_radial_table(cursor)\n'
                                     'remaining = u32(squared_distance - previous)\n'
                                     'count = replace_word(retained_count, increment >> 1)\n'
                                     'return RadialSeedFields(remaining, count, increment, previous, '
                                     'cursor)'},
 'rounded_scene_radial_distance': {'signature': 'state: SceneState, squared_distance: Long',
                                   'returns': 'RadialDistanceFields',
                                   'flow': 'checked_scene_state(state)\n'
                                           'return _rounded_radial_fields(RadialMemory(state), '
                                           'squared_distance)'},
 '_rounded_radial_fields': {'signature': 'memory: RadialMemory, squared_distance: Long',
 'returns': 'RadialDistanceFields',
 'flow': 'if type(memory) is not RadialMemory:\n'
         "    raise ValueError('closed radial memory required')\n"
         'uint(squared_distance, 32)\n'
         'if squared_distance == 0:\n'
         '    return RadialDistanceFields(0, False, True, False, False)\n'
         'memory.enter_seed()\n'
         'seed = _seed_radial_fields(memory, squared_distance)\n'
         'memory.leave_seed()\n'
         'remaining, count, increment = (seed.remaining, seed.count, seed.increment)\n'
         'while True:\n'
         '    step = subtract_radial_increment(remaining, increment)\n'
         '    remaining = step.remaining\n'
         '    if step.crossed:\n'
         '        return RadialDistanceFields(replace_word(remaining, low16(count)), False, '
         'low16(count) == 0, bool(low16(count) & 32768), False)\n'
         '    count = replace_word(count, u16(count + 1))\n'
         '    increment = replace_word(increment, u16(increment + 2))'},
 '_seed_radial_fields': {'signature': 'memory: RadialMemory, squared_distance: Long, retained_count: Long=0, '
                                      'retained_threshold: Long=0',
                         'returns': 'RadialSeedFields',
                         'flow': 'if type(memory) is not RadialMemory:\n'
                                 "    raise ValueError('closed radial memory required')\n"
                                 'uint(squared_distance, 32)\n'
                                 'uint(retained_count, 32)\n'
                                 'uint(retained_threshold, 32)\n'
                                 'if squared_distance >= 144781:\n'
                                 '    return RadialSeedFields(u32(squared_distance - 144781), '
                                 'replace_word(retained_count, 381), 762, retained_threshold, None)\n'
                                 'thresholds = memory.thresholds\n'
                                 'while squared_distance >= thresholds.long():\n'
                                 '    thresholds = thresholds.advance(6)\n'
                                 'preceding_threshold = thresholds.long(0, -6)\n'
                                 'increment = thresholds.word(0, -2)\n'
                                 'return _radial_previous_fields(squared_distance, retained_count, '
                                 'increment, preceding_threshold, thresholds)'}}


# Complete supplied map-reader body; no alternate state or old-body fallback.
DOMAIN_DECLARATIONS.update({'load_battlefield_map_fields': {'signature': 'memory: BattlePolicyMemory', 'returns': 'PolicyTable', 'flow': "if type(memory) is not BattlePolicyMemory:\n    raise ValueError('typed live battlefield-map memory required')\nscene = memory.battle_scene()\nreturn memory.battlefield_maps.advance(battlefield_map_offset(scene))"}})
APPROVED['contexts_policy_memory'] = {'BattlePolicyMemory', 'PolicyTable'}


# The same supplied tile/category reader serves legacy and complete callers.
DOMAIN_DECLARATIONS.update({'read_battlefield_terrain_type': {'signature': 'state: GameState, map_context: Table, x: Word, y: Word, retained: Long=0', 'returns': 'Long', 'flow': 'checked_state(state)\nchecked_table(map_context, state)\nuint(retained, 32)\nreturn read_battlefield_terrain_type_fields(BattlePolicyMemory(state), map_context, x, y, retained).carrier'}, 'read_battlefield_terrain_type_fields': {'signature': 'memory: BattlePolicyMemory, map_context: PolicyTable, x: Word, y: Word, retained: Long | None', 'returns': 'DeploymentTerrainFields', 'flow': "if type(memory) is not BattlePolicyMemory:\n    raise ValueError('sealed battlefield memory required')\nchecked_policy_table(map_context, memory.state)\nuint(x, 16)\nuint(y, 16)\nif retained is not None:\n    uint(retained, 32)\nbefore_shift = u16(u16((x >> 3) * 40) + (y >> 3))\noffset = battlefield_cell_offset(x, y)\ntile = map_context.word(offset) & 1023\nlookup = memory.state.table(442548)\ncategory = lookup.byte(tile)\nword = tile & 65280 | category\ncarrier = None if retained is None else replace_word(retained, word)\nreturn DeploymentTerrainFields(carrier, word, category, lookup, before_shift & 32768 != 0).validate(memory.state)"}})
APPROVED['contexts_policy_memory'].add('checked_policy_table')
APPROVED['contexts_deployment_terrain'] = {'DeploymentTerrainFields'}

# Actual one-core235CC complete and legacy projections.
DOMAIN_DECLARATIONS.update({'test_battlefield_leader_roster_presence': {'signature': 'state: GameState', 'returns': 'CarryOutcome', 'flow': 'checked_state(state)\nfields = test_battlefield_leader_roster_presence_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn state.carry_result(int(not fields.present))'}, 'test_battlefield_leader_roster_presence_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'LeaderRosterPresenceFields', 'flow': "if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:\n    raise ValueError('sealed memory and actual leader-roster frame required')\nframe.validate(memory.state, type(memory.state) is not GameState or frame.stack_cursor is not None)\nstack = frame.stack_cursor\nif stack is not None:\n    checked_policy_table(frame.roster, memory.state)\n    stack = stack.advance(-4)\n    stack.set_long(0, frame.roster.base)\n    stack = stack.advance(-4)\n    stack.set_long(0, frame.target_y)\n    stack = stack.advance(-4)\n    stack.set_long(0, frame.target_x)\n    frame = first_replace(frame, stack_cursor=stack)\nhead = memory.state.table(4294942759)\nscene = memory.battle_scene()\nleader = scene & 65280 | head.byte(scene)\nroster = memory.state.table(4294944080).cursor()\nwhile True:\n    member = roster.next_word()\n    if negative_word(member):\n        present = False\n        break\n    if member == leader:\n        present = True\n        break\nif stack is not None:\n    restored_x = stack.long()\n    stack = stack.advance(4)\n    restored_y = stack.long()\n    stack = stack.advance(4)\n    restored_roster = memory.state.table(stack.long()).cursor()\n    stack = stack.advance(4)\n    frame = first_replace(frame, target_x=restored_x, target_y=restored_y, roster=restored_roster, stack_cursor=stack)\nif not present:\n    memory.state.write(4294964754, 2, 1041)\n    memory.state.read(4294964066, 2)\n    memory.state.write(4294964066, 2, 0)\n    memory.state.write(4294964950, 2, 2)\nif not memory.state.sr & 8192:\n    raise Boundary('original leader-roster full-SR operation requires supervisor')\nif memory.state.sr & 32768:\n    raise Boundary('leader-roster trace continuation is not modeled')\nstatus = None if frame.status is None else frame.status & 16 | (4 if present else 1)\nreturn LeaderRosterPresenceFields(first_replace(frame, status=status), present).validate(memory.state)"}})
APPROVED['contexts_first_deployment'] = {'FirstDeploymentFrame', 'first_replace'}
APPROVED['contexts_geometry'].add('LeaderRosterPresenceFields')
APPROVED['domain'].add('Boundary')

DOMAIN_DECLARATIONS.update({'read_training_inputs_fields': {'signature': 'memory: BattlePolicyMemory, unit: Word', 'returns': 'TrainingInputs', 'flow': "if type(memory) is not BattlePolicyMemory:\n    raise ValueError('one sealed same-state memory required')\nuint(unit, 16)\ntraining = memory.state.table(4294952192).byte(unit)\nrating = memory.state.table(4294947840).word(u16(unit << 1))\nreturn TrainingInputs(training, rating)"}, 'weighted_training_factor_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, unit: Word', 'returns': 'FirstTrainingFields', 'flow': "if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:\n    raise ValueError('closed training memory and current fields required')\nuint(unit, 16)\ncomplete = type(memory.state) is not GameState\nframe.validate(memory.state, complete)\nsaved_unit, saved_source = (frame.target_x, frame.roster)\nstack = frame.stack_cursor\nif stack is not None:\n    if saved_unit is None or saved_source is None:\n        raise ValueError('actual MOVEM D0/A0 inputs required before any save')\n    if low16(saved_unit) != unit:\n        raise ValueError('training unit must be the actual current D0 WORD')\n    checked_policy_table(saved_source, memory.state)\n    stack = stack.advance(-4)\n    stack.set_long(0, saved_source.base)\n    stack = stack.advance(-4)\n    stack.set_long(0, saved_unit)\ninputs = read_training_inputs_fields(memory, unit)\nfactor = packed_training_strength(inputs)\ndivisor = 100\nquotient = inputs.training * inputs.rating // divisor\noverflow = quotient > 65535\nif overflow and complete:\n    current = first_replace(frame, target_x=replace_word(frame.target_x, u16(unit << 1)), target_y=inputs.training * inputs.rating, roster=memory.state.table(4294947840).cursor(), stack_cursor=stack, status=None)\n    raise FirstDeploymentArithmeticBoundary(47840, current, factor)\nstatus = None if overflow else (16 if unit & 32768 else 0) | (8 if quotient & 32768 else 0) | (4 if quotient == 0 else 0)\nrestored_unit = unit\nif stack is not None:\n    saved_unit = stack.long()\n    stack = stack.advance(4)\n    saved_source = memory.state.table(stack.long()).cursor()\n    stack = stack.advance(4)\n    restored_unit = low16(saved_unit)\nreturned = first_replace(frame, target_x=saved_unit, target_y=factor, roster=saved_source, stack_cursor=stack, status=status)\nreturn FirstTrainingFields(returned, factor, restored_unit)", 'slots': {100: ('training_divisor', 1, 65535)}}})
INLINE_HELPERS += ('read_training_inputs_fields', 'weighted_training_factor_fields')
APPROVED['contexts_first_deployment'] = {'FirstDeploymentFrame', 'FirstTrainingFields', 'FirstDeploymentArithmeticBoundary', 'first_replace'}
APPROVED['contexts_policy_memory'].add('checked_policy_table')

INLINE_HELPERS += ('rounded_deployment_radial_distance_fields',)

DOMAIN_DECLARATIONS.update({'collect_contacts_in_speed_radius': {'signature': 'state: GameState, actor: Word', 'returns': 'ContactCollection', 'flow': 'checked_state(state)\nuint(actor, 16)\nfields = collect_contacts_in_speed_radius_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), actor)\nframe = fields.frame\nreturn ContactCollection(fields.radius, fields.x, fields.y, frame.roster, frame.controller, frame.candidates)'}})

DOMAIN_DECLARATIONS.update({'_contact_retained_word': {'signature': 'carrier: Long | None, value: Word', 'returns': 'Long | None', 'flow': 'uint(value, 16)\nif carrier is None:\n    return None\nuint(carrier, 32)\nreturn replace_word(carrier, value)'}})

DOMAIN_DECLARATIONS.update({'_contact_status': {'signature': 'frame: FirstDeploymentFrame, value: Long, width: int, carry: bool=False, overflow: bool=False, extend: bool | None=None', 'returns': 'FirstDeploymentFrame', 'flow': "if width not in (8, 16, 32):\n    raise ValueError('original contact BYTE/WORD/LONG flag width required')\nuint(value, width)\nif type(carry) is not bool or type(overflow) is not bool:\n    raise ValueError('actual arithmetic carry and overflow required')\nif extend is not None and type(extend) is not bool:\n    raise ValueError('extend must be observed or explicitly unobserved')\nflags = int(carry) | (2 if overflow else 0) | (4 if value == 0 else 0) | (8 if value & 1 << width - 1 else 0)\nif extend is None:\n    status = None if frame.status is None else frame.status & 16 | flags\nelse:\n    status = (16 if extend else 0) | flags\nreturn first_replace(frame, status=status)"}})

DOMAIN_DECLARATIONS.update({'_contact_difference': {'signature': 'frame: FirstDeploymentFrame, coordinate: Word, origin: Word', 'returns': 'tuple', 'flow': 'uint(coordinate, 16)\nuint(origin, 16)\ndifference = u16(coordinate - origin)\nborrowed = coordinate < origin\nframe = _contact_status(frame, difference, 16, borrowed, bool((coordinate ^ origin) & (coordinate ^ difference) & 32768), borrowed)\nif borrowed:\n    before = difference\n    difference = u16(-before)\n    frame = _contact_status(frame, difference, 16, before != 0, before == 32768, before != 0)\nreturn (frame, difference)'}})

DOMAIN_DECLARATIONS.update({'_contact_radial_call': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "complete = type(memory.state) is not GameState or frame.stack_cursor is not None\nif frame.stack_cursor is not None:\n    stack = frame.stack_cursor.advance(-4)\n    stack.set_long(0, 144724)\n    frame = first_replace(frame, stack_cursor=stack)\nif frame.status is not None:\n    memory.state.sr = memory.state.sr & 65504 | frame.status\nreturned = rounded_deployment_radial_distance_fields(memory, frame)\nif type(returned) is not FirstDeploymentFrame:\n    raise Boundary('sole radial core must return the actual current frame')\nreturned.validate(memory.state, complete)\nif returned.stack_cursor is not None:\n    stack = returned.stack_cursor\n    actual = stack.long()\n    if actual != 144724:\n        raise FirstDeploymentReturnBoundary(actual, returned, 144724)\n    returned = first_replace(returned, stack_cursor=stack.advance(4))\nreturn returned.validate(memory.state, complete)"}})

DOMAIN_DECLARATIONS.update({'collect_contacts_in_speed_radius_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, actor: Word | None=None', 'returns': 'ContactCollectionFields', 'flow': "if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:\n    raise ValueError('same existing policy memory and sole current frame required')\nstate = memory.state\ncomplete = type(state) is not GameState or frame.stack_cursor is not None\nframe.validate(state, complete)\nif actor is None:\n    uint(frame.choice, 32)\n    actor = low16(frame.choice)\nelse:\n    uint(actor, 16)\n    if frame.choice is not None and low16(frame.choice) != actor:\n        raise ValueError('legacy actor must agree with an observed current D7 WORD')\nspeed_table = state.table(4294951936).cursor()\nframe = first_replace(frame, roster=speed_table, count=_contact_retained_word(frame.count, 0))\nframe = _contact_status(frame, 0, 16)\nspeed = speed_table.byte(actor)\nframe = first_replace(frame, count=_contact_retained_word(frame.count, speed))\nframe = _contact_status(frame, speed, 8)\nframe = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, speed))\nframe = _contact_status(frame, speed, 16)\nradius = u16(speed << 2)\nframe = first_replace(frame, count=_contact_retained_word(frame.count, radius))\nframe = _contact_status(frame, radius, 16, bool(speed & 16384), False, bool(speed & 16384))\ncombined = radius + speed\nradius = u16(combined)\nframe = first_replace(frame, count=_contact_retained_word(frame.count, radius))\nframe = _contact_status(frame, radius, 16, combined > 65535, bool(~(speed << 2 ^ speed) & (speed << 2 ^ radius) & 32768), combined > 65535)\nshifted = radius\nradius = u16(radius << 1)\nframe = first_replace(frame, count=_contact_retained_word(frame.count, radius))\nframe = _contact_status(frame, radius, 16, bool(shifted & 32768), False, bool(shifted & 32768))\noutput = state.table(4294955776).cursor()\npositions = state.table(4294943056).cursor()\nframe = first_replace(frame, roster=output, candidates=positions, unit=_contact_retained_word(frame.unit, actor))\nframe = _contact_status(frame, actor, 16)\nactor_offset = u16(actor << 2)\nframe = first_replace(frame, unit=_contact_retained_word(frame.unit, actor_offset))\nframe = _contact_status(frame, actor_offset, 16, bool(actor & 16384), False, bool(actor & 16384))\norigin_x = positions.word(actor_offset)\nframe = first_replace(frame, target_y=_contact_retained_word(frame.target_y, origin_x))\nframe = _contact_status(frame, origin_x, 16)\norigin_y = positions.word(actor_offset, 2)\nframe = first_replace(frame, unit=_contact_retained_word(frame.unit, origin_y))\nframe = _contact_status(frame, origin_y, 16)\nretreat_flags = state.table(16726978).cursor()\nframe = first_replace(frame, opponent=retreat_flags)\nother_side = bool(state.read(4294964951, 1) & 2)\nframe = first_replace(frame, status=None if frame.status is None else frame.status & 27 | (0 if other_side else 4))\nframe = first_replace(frame, controller=state.table(4294944080 if other_side else 4294944164).cursor())\nwhile True:\n    source = frame.controller\n    member = source.word()\n    frame = first_replace(frame, controller=source.advance(2), distance=_contact_retained_word(frame.distance, member))\n    frame = _contact_status(frame, member, 16)\n    if negative_word(member):\n        frame.roster.set_word(0, 65535)\n        frame = _contact_status(frame, 65535, 16)\n        if frame.status is not None:\n            state.sr = state.sr & 65504 | frame.status\n        return ContactCollectionFields(frame, radius, origin_x, origin_y).validate(state, complete)\n    marked = frame.opponent.byte(member)\n    frame = _contact_status(frame, marked, 8)\n    if marked != 0:\n        continue\n    frame = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, member))\n    frame = _contact_status(frame, member, 16)\n    position_offset = u16(member << 2)\n    frame = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, position_offset))\n    frame = _contact_status(frame, position_offset, 16, bool(member & 16384), False, bool(member & 16384))\n    candidate_y = frame.candidates.word(position_offset, 2)\n    frame = first_replace(frame, target_x=_contact_retained_word(frame.target_x, candidate_y))\n    frame = _contact_status(frame, candidate_y, 16)\n    live_y = origin_y if frame.unit is None else low16(frame.unit)\n    frame, vertical = _contact_difference(frame, candidate_y, live_y)\n    frame = first_replace(frame, target_x=_contact_retained_word(frame.target_x, vertical))\n    distance_y = vertical >> 7\n    frame = first_replace(frame, target_x=_contact_retained_word(frame.target_x, distance_y))\n    frame = _contact_status(frame, distance_y, 16, bool(vertical & 64), False, bool(vertical & 64))\n    live_radius = radius if frame.count is None else low16(frame.count)\n    compared = u16(distance_y - live_radius)\n    frame = _contact_status(frame, compared, 16, distance_y < live_radius, bool((distance_y ^ live_radius) & (distance_y ^ compared) & 32768))\n    if axis_outside_contact_radius(distance_y, live_radius):\n        continue\n    frame = first_replace(frame, target_x=distance_y * distance_y)\n    frame = _contact_status(frame, frame.target_x, 32)\n    candidate_x = frame.candidates.word(position_offset)\n    frame = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, candidate_x))\n    frame = _contact_status(frame, candidate_x, 16)\n    live_x = origin_x if frame.target_y is None else low16(frame.target_y)\n    frame, horizontal = _contact_difference(frame, candidate_x, live_x)\n    frame = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, horizontal))\n    distance_x = horizontal >> 7\n    frame = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, distance_x))\n    frame = _contact_status(frame, distance_x, 16, bool(horizontal & 64), False, bool(horizontal & 64))\n    compared = u16(distance_x - live_radius)\n    frame = _contact_status(frame, compared, 16, distance_x < live_radius, bool((distance_x ^ live_radius) & (distance_x ^ compared) & 32768))\n    if axis_outside_contact_radius(distance_x, live_radius):\n        continue\n    frame = first_replace(frame, offset_x=distance_x * distance_x)\n    frame = _contact_status(frame, frame.offset_x, 32)\n    before = frame.target_x\n    total = before + frame.offset_x\n    squared = squared_contact_distance(distance_y, distance_x)\n    frame = first_replace(frame, target_x=squared)\n    frame = _contact_status(frame, squared, 32, total > 4294967295, bool(~(before ^ frame.offset_x) & (before ^ squared) & 2147483648), total > 4294967295)\n    frame = _contact_radial_call(memory, frame)\n    distance = low16(frame.target_x)\n    live_radius = radius if frame.count is None else low16(frame.count)\n    compared = u16(distance - live_radius)\n    frame = _contact_status(frame, compared, 16, distance < live_radius, bool((distance ^ live_radius) & (distance ^ compared) & 32768))\n    if not radial_contact_is_in_range(distance, live_radius):\n        continue\n    member = member if frame.distance is None else low16(frame.distance)\n    output = frame.roster\n    output.set_word(0, member)\n    frame = first_replace(frame, roster=output.advance(2))\n    frame = _contact_status(frame, member, 16)"}})

INLINE_HELPERS += ('_contact_retained_word', '_contact_status', '_contact_difference', '_contact_radial_call', 'collect_contacts_in_speed_radius_fields')
APPROVED['contexts_geometry'].add('ContactCollectionFields')

# Root: sole22D30/22DA6/22DE4 logical policies and historical projections.
DECLARATIONS.update({"mark_eligible_actor_for_retreat":{"signature":"state: GameState, actor: Word","returns":"CarryOutcome","flow":"checked_state(state)\nuint(actor, 16)\n_, eligible = mark_eligible_actor_for_retreat_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), actor)\nreturn state.carry_result(int(eligible))"},"test_actor_terrain_types_3_or_7":{"signature":"state: GameState, actor: Word","returns":"CarryOutcome","flow":"checked_state(state)\nuint(actor, 16)\n_, eligible = test_actor_terrain_types_3_or_7_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), actor)\nreturn state.carry_result(int(eligible))"},"count_roster_nonnegative_prefix_bytes":{"signature":"state: GameState","returns":"Word","flow":"checked_state(state)\n_, count = count_roster_nonnegative_prefix_bytes_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn count"}})
DECLARATIONS.update({"_retreat_carry_fields":{"signature":"memory: BattlePolicyMemory, frame: FirstDeploymentFrame, selected: bool","returns":"FirstDeploymentFrame","flow":"if type(selected) is not bool:\n    raise ValueError('actual retreat decision required')\nif frame.status is not None:\n    memory.state.sr = memory.state.sr & 65504 | frame.status\nif type(memory.state) is GameState:\n    memory.state.carry_result(int(selected))\nelse:\n    memory.state.set_status_word(memory.state.sr & 65534 | int(selected))\nreturn first_replace(frame, status=None if frame.status is None else frame.status & 30 | int(selected))"},"_retreat_map_call_fields":{"signature":"memory: BattlePolicyMemory, frame: FirstDeploymentFrame","returns":"FirstDeploymentFrame","flow":"from .business_actions import _deployment_enter, _deployment_leave, _battle_action_map_fields\nframe = _deployment_enter(memory, frame, 142764)\nframe = _battle_action_map_fields(memory, frame)\nreturn _deployment_leave(memory, frame, 142764)"},"test_actor_terrain_types_3_or_7_fields":{"signature":"memory: BattlePolicyMemory, frame: FirstDeploymentFrame, actor: Word | None=None","returns":"tuple","flow":"from .business_actions import _deployment_terrain_lookup\nframe.validate(memory.state, type(memory.state) is not GameState)\nactor = low16(frame.choice) if actor is None else uint(actor, 16)\nframe = _retreat_map_call_fields(memory, frame)\npositions = memory.state.table(4294943056).cursor()\noffset = u16(actor << 2)\nframe = first_replace(frame, candidates=positions, target_x=_contact_retained_word(frame.target_x, offset))\nframe = _contact_status(frame, offset, 16, bool(actor & 16384), False, bool(actor & 16384))\nx = positions.word(offset)\nframe = first_replace(frame, target_y=_contact_retained_word(frame.target_y, x >> 7))\nframe = _contact_status(frame, x >> 7, 16, bool(x & 64), False, bool(x & 64))\ny = positions.word(offset, 2)\nframe = first_replace(frame, unit=_contact_retained_word(frame.unit, y >> 7))\nframe = _contact_status(frame, y >> 7, 16, bool(y & 64), False, bool(y & 64))\nframe, terrain = _deployment_terrain_lookup(memory, frame, x >> 7, y >> 7, continuation=142790)\nvalue = low8(terrain)\ndifference = value - 3 & 255\nframe = _contact_status(frame, difference, 8, value < 3, bool((value ^ 3) & (value ^ difference) & 128))\neligible = value == 3\nif not eligible:\n    difference = value - 7 & 255\n    frame = _contact_status(frame, difference, 8, value < 7, bool((value ^ 7) & (value ^ difference) & 128))\n    eligible = value == 7\nreturn (_retreat_carry_fields(memory, frame, eligible), eligible)"},"count_roster_nonnegative_prefix_bytes_fields":{"signature":"memory: BattlePolicyMemory, frame: FirstDeploymentFrame","returns":"tuple","flow":"frame.validate(memory.state, type(memory.state) is not GameState)\nframe = first_replace(frame, roster=memory.state.table(4294944164).cursor())\nflag = memory.state.read(4294964951, 1)\nframe = first_replace(frame, status=None if frame.status is None else frame.status & 27 | (0 if flag & 2 else 4))\nif not flag & 2:\n    frame = first_replace(frame, roster=memory.state.table(4294944080).cursor())\ncount = 0\nframe = first_replace(frame, target_x=_contact_retained_word(frame.target_x, 0))\nframe = _contact_status(frame, 0, 16)\nwhile True:\n    value = frame.roster.byte()\n    frame = first_replace(frame, roster=frame.roster.advance(1))\n    frame = _contact_status(frame, value, 8)\n    if negative_byte(value):\n        return (frame, count)\n    previous = count\n    count = u16(count + 1)\n    frame = first_replace(frame, target_x=_contact_retained_word(frame.target_x, count))\n    frame = _contact_status(frame, count, 16, previous == 65535, previous == 32767, previous == 65535)"},"_retreat_child_fields":{"signature":"memory: BattlePolicyMemory, frame: FirstDeploymentFrame, continuation: Long, algorithm, actor: Word | None=None","returns":"tuple","flow":"from .business_actions import _deployment_enter, _deployment_leave\nframe = _deployment_enter(memory, frame, continuation)\nif actor is None:\n    frame, selected = algorithm(memory, frame)\nelse:\n    frame, selected = algorithm(memory, frame, actor)\nreturn (_deployment_leave(memory, frame, continuation), selected)"},"mark_eligible_actor_for_retreat_fields":{"signature":"memory: BattlePolicyMemory, frame: FirstDeploymentFrame, actor: Word | None=None","returns":"tuple","flow":"from .business_actions import _deployment_enter, _deployment_leave\nframe.validate(memory.state, type(memory.state) is not GameState)\nactor = low16(frame.choice) if actor is None else uint(actor, 16)\nframe, eligible = _retreat_child_fields(memory, frame, 142644, test_actor_terrain_types_3_or_7_fields, actor)\nif eligible:\n    troops = memory.state.table(4294952960).cursor()\n    offset = u16(actor << 2)\n    frame = first_replace(frame, roster=troops, target_x=_contact_retained_word(frame.target_x, offset))\n    frame = _contact_status(frame, offset, 16, bool(actor & 16384), False, bool(actor & 16384))\n    strength = troops.long(offset)\n    difference = u32(strength - 5000)\n    frame = _contact_status(frame, difference, 32, strength < 5000, bool((strength ^ 5000) & (strength ^ difference) & 2147483648))\n    eligible = retreat_troops_are_eligible(strength)\nif eligible:\n    frame, count = _retreat_child_fields(memory, frame, 142672, count_roster_nonnegative_prefix_bytes_fields)\n    difference = u16(count - 4)\n    frame = _contact_status(frame, difference, 16, count < 4, bool((count ^ 4) & (count ^ difference) & 32768))\n    eligible = retreat_roster_is_sufficient(count)\nif eligible:\n    frame = _deployment_enter(memory, frame, 142684)\n    frame = collect_contacts_in_speed_radius_fields(memory, frame, actor).frame\n    frame = _deployment_leave(memory, frame, 142684)\n    selected = memory.state.read(4294955776, 2)\n    frame = _contact_status(frame, selected, 16)\n    eligible = not negative_word(selected)\nif eligible:\n    flags = memory.state.table(16726978).cursor()\n    frame = first_replace(frame, roster=flags)\n    marked = flags.byte(actor)\n    frame = _contact_status(frame, marked, 8)\n    if marked == 0:\n        frame = _deployment_enter(memory, frame, 142712)\n        from .business_formation import first_deployment_random_fields\n        frame = first_deployment_random_fields(memory, frame)\n        frame = _deployment_leave(memory, frame, 142712)\n        eligible = retreat_random_gate(frame.target_x)\n        frame = first_replace(frame, status=frame.status & 27 | (4 if eligible else 0))\nif eligible:\n    frame.roster.set_byte(actor, 1)\n    frame = _contact_status(frame, 1, 8)\n    frame = first_replace(frame, roster=memory.state.table(4294946344).cursor())\nelse:\n    frame = first_replace(frame, roster=memory.state.table(16726978).cursor())\nframe.roster.byte(actor)\nframe.roster.set_byte(actor, 0)\nframe = _contact_status(frame, 0, 8)\nreturn (_retreat_carry_fields(memory, frame, eligible), eligible)"}})
INLINE_HELPERS += ("_retreat_carry_fields","_retreat_map_call_fields","test_actor_terrain_types_3_or_7_fields","count_roster_nonnegative_prefix_bytes_fields","_retreat_child_fields","mark_eligible_actor_for_retreat_fields",)
APPROVED['contexts_first_deployment'].add('FirstDeploymentReturnBoundary')

# Both interfaces share the actual retreat flag commit, not a second algorithm.
DECLARATIONS.update({"commit_actor_retreat":{"signature":"state: GameState, actor: Word, eligible: bool","returns":"CarryOutcome","flow":"checked_state(state)\nuint(actor, 16)\nif type(eligible) is not bool:\n    raise ValueError('strict retreat decision required')\n_commit_actor_retreat_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), actor, eligible)\nreturn state.carry_result(int(eligible))"},"mark_eligible_actor_for_retreat_fields":{"signature":"memory: BattlePolicyMemory, frame: FirstDeploymentFrame, actor: Word | None=None","returns":"tuple","flow":"from .business_actions import _deployment_enter, _deployment_leave\nframe.validate(memory.state, type(memory.state) is not GameState)\nactor = low16(frame.choice) if actor is None else uint(actor, 16)\nframe, eligible = _retreat_child_fields(memory, frame, 142644, test_actor_terrain_types_3_or_7_fields, actor)\nif eligible:\n    troops = memory.state.table(4294952960).cursor()\n    offset = u16(actor << 2)\n    frame = first_replace(frame, roster=troops, target_x=_contact_retained_word(frame.target_x, offset))\n    frame = _contact_status(frame, offset, 16, bool(actor & 16384), False, bool(actor & 16384))\n    strength = troops.long(offset)\n    difference = u32(strength - 5000)\n    frame = _contact_status(frame, difference, 32, strength < 5000, bool((strength ^ 5000) & (strength ^ difference) & 2147483648))\n    eligible = retreat_troops_are_eligible(strength)\nif eligible:\n    frame, count = _retreat_child_fields(memory, frame, 142672, count_roster_nonnegative_prefix_bytes_fields)\n    difference = u16(count - 4)\n    frame = _contact_status(frame, difference, 16, count < 4, bool((count ^ 4) & (count ^ difference) & 32768))\n    eligible = retreat_roster_is_sufficient(count)\nif eligible:\n    frame = _deployment_enter(memory, frame, 142684)\n    frame = collect_contacts_in_speed_radius_fields(memory, frame, actor).frame\n    frame = _deployment_leave(memory, frame, 142684)\n    selected = memory.state.read(4294955776, 2)\n    frame = _contact_status(frame, selected, 16)\n    eligible = not negative_word(selected)\nif eligible:\n    flags = memory.state.table(16726978).cursor()\n    frame = first_replace(frame, roster=flags)\n    marked = flags.byte(actor)\n    frame = _contact_status(frame, marked, 8)\n    if marked == 0:\n        frame = _deployment_enter(memory, frame, 142712)\n        from .business_formation import first_deployment_random_fields\n        frame = first_deployment_random_fields(memory, frame)\n        frame = _deployment_leave(memory, frame, 142712)\n        eligible = retreat_random_gate(frame.target_x)\n        frame = first_replace(frame, status=frame.status & 27 | (4 if eligible else 0))\nreturn (_commit_actor_retreat_fields(memory, frame, actor, eligible), eligible)"},"_commit_actor_retreat_fields":{"signature":"memory: BattlePolicyMemory, frame: FirstDeploymentFrame, actor: Word, eligible: bool","returns":"FirstDeploymentFrame","flow":"uint(actor, 16)\nif type(eligible) is not bool:\n    raise ValueError('actual eligibility required')\nframe = first_replace(frame, roster=memory.state.table(16726978).cursor())\nif eligible:\n    frame.roster.set_byte(actor, 1)\n    frame = _contact_status(frame, 1, 8)\n    frame = first_replace(frame, roster=memory.state.table(4294946344).cursor())\nframe.roster.byte(actor)\nframe.roster.set_byte(actor, 0)\nframe = _contact_status(frame, 0, 8)\nreturn _retreat_carry_fields(memory, frame, eligible)"}})
INLINE_HELPERS += ('_commit_actor_retreat_fields',)
APPROVED['business_actions'] = {'_deployment_enter', '_deployment_leave', '_deployment_push', '_deployment_pop', '_battle_action_map_fields', '_deployment_terrain_lookup'}
APPROVED['business_formation'] = {'first_deployment_random_fields'}

DOMAIN_DECLARATIONS.update({'select_weakest_contact_strength': {'signature': 'state: GameState, retained_member: Word=0, retained_weighting: Long=0', 'returns': 'ContactStrength', 'flow': 'checked_state(state)\nuint(retained_member, 16)\nuint(retained_weighting, 32)\nframe, strength, member, weighting = select_weakest_contact_strength_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), retained_member, retained_weighting)\nreturn ContactStrength(strength, member, weighting, frame.roster, state.table(frame.candidates.base))'}})

DOMAIN_DECLARATIONS.update({'_weakest_training_call_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, member: Word', 'returns': 'FirstDeploymentFrame', 'flow': 'if frame.stack_cursor is not None:\n    stack = frame.stack_cursor.advance(-4)\n    stack.set_long(0, 142434)\n    frame = first_replace(frame, stack_cursor=stack)\nreturned = weighted_training_factor_fields(memory, frame, member).frame\nif returned.stack_cursor is not None:\n    stack = returned.stack_cursor\n    actual = stack.long()\n    if actual != 142434:\n        raise FirstDeploymentReturnBoundary(actual, returned, 142434)\n    returned = first_replace(returned, stack_cursor=stack.advance(4))\nreturn returned'}})

DOMAIN_DECLARATIONS.update({'select_weakest_contact_strength_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, retained_member: Word | None=None, retained_weighting: Long | None=None', 'returns': 'tuple', 'flow': "from .business_formation import _first_word, _first_shift_word, _first_right_word\nif type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:\n    raise ValueError('same-state contact memory and actual fields required')\nstate = memory.state\nframe.validate(state, frame.stack_cursor is not None)\nif retained_member is None:\n    uint(frame.count, 32)\n    retained_member = low16(frame.count)\nif retained_weighting is None:\n    uint(frame.target_y, 32)\n    retained_weighting = frame.target_y\nuint(retained_member, 16)\nuint(retained_weighting, 32)\nframe = first_replace(frame, roster=state.table(4294955776).cursor(), candidates=state.table(4294952960).cursor(), unit=4294967295)\nframe = _contact_status(frame, 4294967295, 32)\nselected, last_weighting = (retained_member, retained_weighting)\nwhile True:\n    source = frame.roster\n    member = source.word()\n    frame = first_replace(frame, roster=source.advance(2))\n    frame = _first_word(frame, 'target_x', member)\n    if negative_word(member):\n        return (frame, frame.unit, selected, last_weighting)\n    frame = _weakest_training_call_fields(memory, frame, member)\n    last_weighting = frame.target_y\n    live_member = member if frame.target_x is None else low16(frame.target_x)\n    offset = u16(live_member << 2)\n    frame = _first_shift_word(frame, 'target_x', live_member, 2)\n    troops = frame.candidates.long(offset)\n    frame = first_replace(frame, distance=troops)\n    frame = _contact_status(frame, troops, 32)\n    strength = low16(troops) * low16(frame.target_y)\n    frame = first_replace(frame, distance=strength)\n    frame = _contact_status(frame, strength, 32)\n    difference = u32(strength - frame.unit)\n    frame = _contact_status(frame, difference, 32, strength < frame.unit, bool((strength ^ frame.unit) & (strength ^ difference) & 2147483648))\n    if not is_weaker_contact(strength, frame.unit):\n        continue\n    frame = first_replace(frame, unit=strength)\n    frame = _contact_status(frame, strength, 32)\n    frame = _first_right_word(frame, 'target_x', offset, 2)\n    selected = offset >> 2\n    frame = _first_word(frame, 'count', selected)"}})

INLINE_HELPERS += ('_weakest_training_call_fields', 'select_weakest_contact_strength_fields')

APPROVED.setdefault('business_formation', set()).update({'_first_word', '_first_shift_word', '_first_right_word'})

DOMAIN_DECLARATIONS.update({'test_other_roster_single_member': {'signature': 'state: GameState', 'returns': 'CarryOutcome', 'flow': 'checked_state(state)\nframe, selected = test_other_roster_single_member_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn state.carry_result(int(selected))'}})

DOMAIN_DECLARATIONS.update({'constrain_target_near_battlefield_anchor': {'signature': 'state: GameState, actor: Word, x: Word, y: Word', 'returns': 'TargetCoordinate', 'flow': 'checked_state(state)\nuint(actor, 16)\nuint(x, 16)\nuint(y, 16)\nreturn constrain_target_near_battlefield_anchor_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), actor, x, y)[1]', 'slots': {4096: ('anchor_edge', 0, 65535)}}})

DOMAIN_DECLARATIONS.update({'select_nearest_contact_to_battlefield_center': {'signature': 'state: GameState, retained_member: Word=0', 'returns': 'Word', 'flow': 'checked_state(state)\nuint(retained_member, 16)\nreturn select_nearest_contact_to_battlefield_center_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), retained_member)[1]'}})

DOMAIN_DECLARATIONS.update({'wrapped_axis_distance': {'signature': 'coordinate: Word, origin: Word', 'returns': 'Word', 'flow': 'uint(coordinate, 16)\nuint(origin, 16)\nreturn _contact_difference(FirstDeploymentFrame.unobserved(), coordinate, origin)[1]'}})

DOMAIN_DECLARATIONS.update({'test_same_side_total_shortfall': {'signature': 'state: GameState', 'returns': 'CarryOutcome', 'flow': 'checked_state(state)\nframe, selected = test_same_side_total_shortfall_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn state.carry_result(int(selected))'}})

DOMAIN_DECLARATIONS.update({'_contact_strategy_actor_slot_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, size: int, save: bool, actor: Word=None', 'returns': 'FirstDeploymentFrame', 'flow': "from .business_formation import _first_word, _first_long, _first_memory_word\nif size not in (2, 4) or type(save) is not bool:\n    raise ValueError('actual contact-strategy actor save width required')\nif save:\n    if size == 2:\n        uint(actor, 16)\n        frame = _first_memory_word(frame, actor)\n        value = actor\n    else:\n        value = frame.choice\n        frame = first_replace(frame, status=None) if value is None else _contact_status(frame, value, 32)\n    if frame.stack_cursor is not None:\n        stack = frame.stack_cursor.advance(-size)\n        if size == 2:\n            stack.set_word(0, value)\n        else:\n            stack.set_long(0, value)\n        return first_replace(frame, stack_cursor=stack)\n    if frame.choice is not None:\n        raise Boundary('observed actor save requires its real current stack, not a host snapshot')\n    return frame\nif frame.stack_cursor is not None:\n    value = frame.stack_cursor.word() if size == 2 else frame.stack_cursor.long()\n    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(size))\n    return _first_word(frame, 'choice', value) if size == 2 else _first_long(frame, 'choice', value)\nreturn _first_word(frame, 'choice', actor) if size == 2 else first_replace(frame, choice=None, status=None)"}})

DOMAIN_DECLARATIONS.update({'_contact_strategy_axis_distance_fields': {'signature': 'frame: FirstDeploymentFrame, carrier: str, coordinate: Word, origin: Word', 'returns': 'tuple', 'flow': "from .business_formation import _first_word\nif carrier not in ('choice', 'offset_x', 'offset_y'):\n    raise ValueError('actual anchor/nearest axis carrier required')\nframe = _first_word(frame, carrier, coordinate)\nframe, value = _contact_difference(frame, coordinate, origin)\nreturn (first_replace(frame, **{carrier: _contact_retained_word(frame.carrier(carrier), value)}), value)"}})

DOMAIN_DECLARATIONS.update({'test_other_roster_single_member_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': 'from .business_formation import _first_frame, _first_memory_word\nfrom ..high_level_gameplay_flow.business_battle import _postbattle_bit_fields\nframe = _first_frame(memory, frame)\nside = memory.state.read(4294964951, 1)\nframe = _postbattle_bit_fields(frame, bool(side & 2))\nroster = memory.state.table(4294944080 if side & 2 else 4294944164).cursor()\nframe = first_replace(frame, roster=roster)\nword = roster.word(0, 2)\nframe = _first_memory_word(frame, word)\nselected = negative_word(word)\nreturn (_retreat_carry_fields(memory, frame, selected), selected)'}})

DOMAIN_DECLARATIONS.update({'constrain_target_near_battlefield_anchor_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, actor: Word=None, x: Word=None, y: Word=None', 'returns': 'tuple', 'flow': "from .business_formation import _first_frame, _first_word, _first_shift_word, _first_sub_word, _first_add_word, _first_compare_word, _first_region_publish\nframe = _first_frame(memory, frame)\nactor = low16(frame.choice) if actor is None else uint(actor, 16)\nx = low16(frame.target_x) if x is None else uint(x, 16)\ny = low16(frame.target_y) if y is None else uint(y, 16)\nfor carrier, observed in ((frame.choice, actor), (frame.target_x, x), (frame.target_y, y)):\n    if carrier is not None and low16(carrier) != observed:\n        raise ValueError('legacy WORD operands must agree with observed full fields')\nframe = _contact_strategy_actor_slot_fields(memory, frame, 2, True, actor)\npositions = memory.state.table(4294943056).cursor()\nframe = first_replace(frame, roster=positions)\nframe = _first_word(frame, 'unit', actor)\nframe = _first_shift_word(frame, 'unit', actor, 2)\noffset = u16(actor << 2)\nown_x = positions.word(offset)\nframe = _first_word(frame, 'count', own_x)\nown_y = positions.word(offset, 2)\nframe = _first_word(frame, 'distance', own_y)\nanchor = memory.state.table(713462).cursor()\nframe = first_replace(frame, roster=anchor)\nscene = memory.battle_scene()\nframe = _first_word(frame, 'offset_x', scene)\nframe = _first_shift_word(frame, 'offset_x', scene, 2)\ncenter_y = anchor.word(u16(scene << 2), 2)\nframe = _first_word(frame, 'offset_y', center_y)\ncenter_x = anchor.word(u16(scene << 2))\nframe = _first_word(frame, 'offset_x', center_x)\nframe, x_distance = _contact_strategy_axis_distance_fields(frame, 'choice', own_x, center_x)\nframe = _first_compare_word(frame, x_distance, 4096)\nadjust_vertical_edge = False\nadjust_horizontal_edge = False\nchoose_nearest_axis = False\nif x_distance == 4096:\n    frame, y_distance = _contact_strategy_axis_distance_fields(frame, 'choice', own_y, center_y)\n    frame = _first_compare_word(frame, y_distance, 4096)\n    if y_distance <= 4096:\n        frame = _first_compare_word(frame, own_x, center_x)\n        frame = _first_compare_word(frame, x, own_x)\n        adjust_vertical_edge = x < own_x if own_x > center_x else x > own_x\nelif x_distance < 4096:\n    frame, y_distance = _contact_strategy_axis_distance_fields(frame, 'choice', own_y, center_y)\n    frame = _first_compare_word(frame, y_distance, 4096)\n    if y_distance == 4096:\n        frame = _first_compare_word(frame, own_y, center_y)\n        frame = _first_compare_word(frame, y, own_y)\n        adjust_horizontal_edge = y < own_y if own_y > center_y else y > own_y\nif adjust_vertical_edge:\n    frame = _first_compare_word(frame, y, center_y)\n    frame = _first_word(frame, 'choice', center_y)\n    if y > center_y:\n        frame = _first_add_word(frame, 'choice', center_y, 4096)\n        edge_y = u16(center_y + 4096)\n    else:\n        frame = _first_sub_word(frame, 'choice', center_y, 4096)\n        edge_y = u16(center_y - 4096)\n    frame = _first_compare_word(frame, edge_y, own_y)\n    if edge_y != own_y:\n        x, y = (own_x, edge_y)\n        frame = _first_word(frame, 'target_x', x)\n        frame = _first_word(frame, 'target_y', y)\n    else:\n        choose_nearest_axis = True\nelif adjust_horizontal_edge:\n    y = own_y\n    frame = _first_word(frame, 'target_y', y)\n    frame = _first_compare_word(frame, x, center_x)\n    frame = _first_word(frame, 'target_x', center_x)\n    if x > center_x:\n        frame = _first_add_word(frame, 'target_x', center_x, 4096)\n        x = u16(center_x + 4096)\n    else:\n        frame = _first_sub_word(frame, 'target_x', center_x, 4096)\n        x = u16(center_x - 4096)\nif choose_nearest_axis:\n    frame, dx = _contact_strategy_axis_distance_fields(frame, 'offset_x', own_x, x)\n    frame, dy = _contact_strategy_axis_distance_fields(frame, 'offset_y', own_y, y)\n    frame = _first_compare_word(frame, dy, dx)\n    if dy > dx:\n        x = own_x\n        frame = _first_word(frame, 'target_x', x)\n    else:\n        y = own_y\n        frame = _first_word(frame, 'target_y', y)\nframe = _contact_strategy_actor_slot_fields(memory, frame, 2, False, actor)\nreturn (_first_region_publish(memory, frame), TargetCoordinate(x, y))"}})

DOMAIN_DECLARATIONS.update({'select_nearest_contact_to_battlefield_center_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, retained_member: Word=None', 'returns': 'tuple', 'flow': "from .business_formation import _first_frame, _first_word, _first_shift_word, _first_add_word, _first_compare_word, _first_memory_word, _first_region_publish\nframe = _first_frame(memory, frame)\nselected = low16(frame.distance) if retained_member is None else uint(retained_member, 16)\nframe = _contact_strategy_actor_slot_fields(memory, frame, 4, True)\nsecond = memory.state.read(4294955778, 2)\nframe = _first_memory_word(frame, second)\nif negative_word(second):\n    selected = memory.state.read(4294955776, 2)\n    frame = _first_word(frame, 'distance', selected)\nelse:\n    anchor = memory.state.table(713462).cursor()\n    frame = first_replace(frame, roster=anchor)\n    scene = memory.battle_scene()\n    frame = _first_word(frame, 'target_x', scene)\n    frame = _first_shift_word(frame, 'target_x', scene, 2)\n    center_x = anchor.word(u16(scene << 2))\n    frame = _first_word(frame, 'target_y', center_x)\n    center_y = anchor.word(u16(scene << 2), 2)\n    frame = _first_word(frame, 'unit', center_y)\n    positions = memory.state.table(4294943056).cursor()\n    candidates = memory.state.table(4294955776).cursor()\n    frame = first_replace(frame, roster=positions, candidates=candidates)\n    closest = 65535\n    frame = _first_word(frame, 'count', closest)\n    while True:\n        member = candidates.next_word()\n        frame = _first_word(frame, 'offset_x', member)\n        if negative_word(member):\n            break\n        frame = _first_word(frame, 'offset_y', member)\n        frame = _first_shift_word(frame, 'offset_y', member, 2)\n        offset = u16(member << 2)\n        candidate_y = positions.word(offset, 2)\n        frame, dy = _contact_strategy_axis_distance_fields(frame, 'choice', candidate_y, center_y)\n        candidate_x = positions.word(offset)\n        frame, dx = _contact_strategy_axis_distance_fields(frame, 'offset_y', candidate_x, center_x)\n        frame = _first_add_word(frame, 'choice', dy, dx)\n        distance = u16(dy + dx)\n        frame = _first_compare_word(frame, distance, closest)\n        if is_nearer_contact(distance, closest):\n            closest, selected = (distance, member)\n            frame = _first_word(frame, 'count', closest)\n            frame = _first_word(frame, 'distance', selected)\nmemory.state.table(4294964134).set_word(0, selected)\nframe = _first_memory_word(frame, selected)\nframe = _contact_strategy_actor_slot_fields(memory, frame, 4, False)\nreturn (_first_region_publish(memory, frame), selected)"}})

DOMAIN_DECLARATIONS.update({'test_same_side_total_shortfall_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': "from .business_formation import _first_frame, _first_long, _first_compare_long\nfrom ..high_level_gameplay_flow.business_battle import _postbattle_bit_fields\nframe = _first_frame(memory, frame)\nfirst = memory.state.table(4294964894).cursor()\nsecond = memory.state.table(4294964898).cursor()\nframe = first_replace(frame, roster=first, candidates=second)\nside = memory.state.read(4294964951, 1)\nframe = _postbattle_bit_fields(frame, bool(side & 2))\nif side & 2:\n    first, second = (second, first)\n    frame = first_replace(frame, roster=first, candidates=second)\nstrength = first.long()\nframe = _first_long(frame, 'target_x', strength)\nopposite = second.long()\nframe = _first_compare_long(frame, strength, opposite)\nselected = False\nif strength < opposite:\n    limit = memory.state.read(4294965096, 4)\n    frame = _first_compare_long(frame, strength, limit)\n    selected = strength < limit\nreturn (_retreat_carry_fields(memory, frame, selected), selected)"}})

DOMAIN_DECLARATIONS.update({'test_other_side_total_shortfall': {'signature': 'state: GameState', 'returns': 'CarryOutcome', 'flow': 'checked_state(state)\nframe, selected = test_other_side_total_shortfall_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn state.carry_result(int(selected))'}, 'test_other_side_total_shortfall_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'tuple', 'flow': "from .business_formation import _first_frame, _first_long, _first_compare_long\nfrom ..high_level_gameplay_flow.business_battle import _postbattle_bit_fields\nframe = _first_frame(memory, frame)\nfirst = memory.state.table(4294964894).cursor()\nsecond = memory.state.table(4294964898).cursor()\nframe = first_replace(frame, roster=first, candidates=second)\nside = memory.state.read(4294964951, 1)\nframe = _postbattle_bit_fields(frame, bool(side & 2))\nif side & 2:\n    first, second = (second, first)\n    frame = first_replace(frame, roster=first, candidates=second)\nstrength = second.long()\nframe = _first_long(frame, 'target_x', strength)\nopposite = first.long()\nframe = _first_compare_long(frame, strength, opposite)\nselected = False\nif strength < opposite:\n    limit = memory.state.read(4294965100, 4)\n    frame = _first_compare_long(frame, strength, limit)\n    selected = strength < limit\nreturn (_retreat_carry_fields(memory, frame, selected), selected)"}})

INLINE_HELPERS += ('_contact_strategy_actor_slot_fields', '_contact_strategy_axis_distance_fields', 'test_other_roster_single_member_fields', 'constrain_target_near_battlefield_anchor_fields', 'select_nearest_contact_to_battlefield_center_fields', 'test_same_side_total_shortfall_fields', 'test_other_side_total_shortfall_fields')
APPROVED.setdefault('business_formation', set()).update({'_first_memory_word', '_first_add_word', '_first_frame', '_first_word', '_first_region_publish', '_first_sub_word', '_first_compare_word', '_first_compare_long', '_first_long', '_first_shift_word'})
APPROVED.setdefault('business_battle', set()).update({'_postbattle_bit_fields'})

CONTACT_NATIVE_NAMES = ('test_other_roster_single_member', 'constrain_target_near_battlefield_anchor', 'select_nearest_contact_to_battlefield_center', 'test_same_side_total_shortfall')

DOMAIN_DECLARATIONS['constrain_target_near_battlefield_anchor'].pop('slots',None)
DOMAIN_DECLARATIONS.update({'constrain_target_near_battlefield_anchor_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, actor: Word=None, x: Word=None, y: Word=None', 'returns': 'tuple', 'flow': "anchor_edge = 4096\nfrom .business_formation import _first_frame, _first_word, _first_shift_word, _first_sub_word, _first_add_word, _first_compare_word, _first_region_publish\nframe = _first_frame(memory, frame)\nactor = low16(frame.choice) if actor is None else uint(actor, 16)\nx = low16(frame.target_x) if x is None else uint(x, 16)\ny = low16(frame.target_y) if y is None else uint(y, 16)\nfor carrier, observed in ((frame.choice, actor), (frame.target_x, x), (frame.target_y, y)):\n    if carrier is not None and low16(carrier) != observed:\n        raise ValueError('legacy WORD operands must agree with observed full fields')\nframe = _contact_strategy_actor_slot_fields(memory, frame, 2, True, actor)\npositions = memory.state.table(4294943056).cursor()\nframe = first_replace(frame, roster=positions)\nframe = _first_word(frame, 'unit', actor)\nframe = _first_shift_word(frame, 'unit', actor, 2)\noffset = u16(actor << 2)\nown_x = positions.word(offset)\nframe = _first_word(frame, 'count', own_x)\nown_y = positions.word(offset, 2)\nframe = _first_word(frame, 'distance', own_y)\nanchor = memory.state.table(713462).cursor()\nframe = first_replace(frame, roster=anchor)\nscene = memory.battle_scene()\nframe = _first_word(frame, 'offset_x', scene)\nframe = _first_shift_word(frame, 'offset_x', scene, 2)\ncenter_y = anchor.word(u16(scene << 2), 2)\nframe = _first_word(frame, 'offset_y', center_y)\ncenter_x = anchor.word(u16(scene << 2))\nframe = _first_word(frame, 'offset_x', center_x)\nframe, x_distance = _contact_strategy_axis_distance_fields(frame, 'choice', own_x, center_x)\nframe = _first_compare_word(frame, x_distance, anchor_edge)\nadjust_vertical_edge = False\nadjust_horizontal_edge = False\nchoose_nearest_axis = False\nif x_distance == anchor_edge:\n    frame, y_distance = _contact_strategy_axis_distance_fields(frame, 'choice', own_y, center_y)\n    frame = _first_compare_word(frame, y_distance, anchor_edge)\n    if y_distance <= anchor_edge:\n        frame = _first_compare_word(frame, own_x, center_x)\n        frame = _first_compare_word(frame, x, own_x)\n        adjust_vertical_edge = x < own_x if own_x > center_x else x > own_x\nelif x_distance < anchor_edge:\n    frame, y_distance = _contact_strategy_axis_distance_fields(frame, 'choice', own_y, center_y)\n    frame = _first_compare_word(frame, y_distance, anchor_edge)\n    if y_distance == anchor_edge:\n        frame = _first_compare_word(frame, own_y, center_y)\n        frame = _first_compare_word(frame, y, own_y)\n        adjust_horizontal_edge = y < own_y if own_y > center_y else y > own_y\nif adjust_vertical_edge:\n    frame = _first_compare_word(frame, y, center_y)\n    frame = _first_word(frame, 'choice', center_y)\n    if y > center_y:\n        frame = _first_add_word(frame, 'choice', center_y, anchor_edge)\n        edge_y = u16(center_y + anchor_edge)\n    else:\n        frame = _first_sub_word(frame, 'choice', center_y, anchor_edge)\n        edge_y = u16(center_y - anchor_edge)\n    frame = _first_compare_word(frame, edge_y, own_y)\n    if edge_y != own_y:\n        x, y = (own_x, edge_y)\n        frame = _first_word(frame, 'target_x', x)\n        frame = _first_word(frame, 'target_y', y)\n    else:\n        choose_nearest_axis = True\nelif adjust_horizontal_edge:\n    y = own_y\n    frame = _first_word(frame, 'target_y', y)\n    frame = _first_compare_word(frame, x, center_x)\n    frame = _first_word(frame, 'target_x', center_x)\n    if x > center_x:\n        frame = _first_add_word(frame, 'target_x', center_x, anchor_edge)\n        x = u16(center_x + anchor_edge)\n    else:\n        frame = _first_sub_word(frame, 'target_x', center_x, anchor_edge)\n        x = u16(center_x - anchor_edge)\nif choose_nearest_axis:\n    frame, dx = _contact_strategy_axis_distance_fields(frame, 'offset_x', own_x, x)\n    frame, dy = _contact_strategy_axis_distance_fields(frame, 'offset_y', own_y, y)\n    frame = _first_compare_word(frame, dy, dx)\n    if dy > dx:\n        x = own_x\n        frame = _first_word(frame, 'target_x', x)\n    else:\n        y = own_y\n        frame = _first_word(frame, 'target_y', y)\nframe = _contact_strategy_actor_slot_fields(memory, frame, 2, False, actor)\nreturn (_first_region_publish(memory, frame), TargetCoordinate(x, y))", 'slots': {4096: ('anchor_edge', 0, 65535)}}})
APPROVED[(1,'business_formation')] = APPROVED['business_formation'] | {'first_deployment_random_fields'}
APPROVED[(1,'business_actions')] = {'_deployment_enter','_deployment_leave','_battle_action_map_fields','_deployment_terrain_lookup'}
APPROVED[(2,'high_level_gameplay_flow.business_battle')] = {'_postbattle_bit_fields'}

# Synchronize four already-current sole-field compatibility projections.
DOMAIN_DECLARATIONS['mark_eligible_actor_for_retreat'] = {'signature': 'state: GameState, actor: Word', 'returns': 'CarryOutcome', 'flow': 'checked_state(state)\nuint(actor, 16)\n_, eligible = mark_eligible_actor_for_retreat_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), actor)\nreturn state.carry_result(int(eligible))'}
DOMAIN_DECLARATIONS['commit_actor_retreat'] = {'signature': 'state: GameState, actor: Word, eligible: bool', 'returns': 'CarryOutcome', 'flow': "checked_state(state)\nuint(actor, 16)\nif type(eligible) is not bool:\n    raise ValueError('strict retreat decision required')\n_commit_actor_retreat_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), actor, eligible)\nreturn state.carry_result(int(eligible))"}
DOMAIN_DECLARATIONS['test_actor_terrain_types_3_or_7'] = {'signature': 'state: GameState, actor: Word', 'returns': 'CarryOutcome', 'flow': 'checked_state(state)\nuint(actor, 16)\n_, eligible = test_actor_terrain_types_3_or_7_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), actor)\nreturn state.carry_result(int(eligible))'}
DOMAIN_DECLARATIONS['count_roster_nonnegative_prefix_bytes'] = {'signature': 'state: GameState', 'returns': 'Word', 'flow': 'checked_state(state)\n_, count = count_roster_nonnegative_prefix_bytes_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())\nreturn count'}

# B170: exact existing terrain/contact owners; no wider source admission.
DOMAIN_DECLARATIONS.update({'_weakest_comparison_call_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "from .business_actions import _deployment_enter, _deployment_leave\nif (target, continuation) not in ((144594, 142364), (142412, 142376), (47816, 142384)):\n    raise ValueError('original weakest-contact child and continuation required')\nif type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:\n    raise ValueError('same-state policy memory and complete current frame required')\nchecked_scene_state(memory.state)\nframe.validate(memory.state, True)\nmemory.state.sr = memory.state.sr & 65504 | frame.status\nentered = _deployment_enter(memory, frame, continuation)\nif target == 144594:\n    returned = collect_contacts_in_speed_radius_fields(memory, entered).frame\nelif target == 142412:\n    returned = select_weakest_contact_strength_fields(memory, entered)[0]\nelse:\n    returned = weighted_training_factor_fields(memory, entered, low16(entered.target_x)).frame\nreturned.validate(memory.state, True)\nmemory.state.sr = memory.state.sr & 65504 | returned.status\nreturn _deployment_leave(memory, returned, continuation)"}, 'compare_actor_to_weakest_contact_strength_fields': {'signature': 'memory: BattlePolicyMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from .business_formation import _first_word, _first_shift_word, _first_compare_long\nif type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:\n    raise ValueError('same-state policy memory and complete current frame required')\nstate = memory.state\nchecked_scene_state(state)\nframe.validate(state, True)\nif frame.roster is None or frame.candidates is None or frame.controller is None or (frame.scan is None) or (frame.opponent is None) or (frame.scratch is None) or (frame.auxiliary is None):\n    raise ValueError('weakest-contact comparison requires all actual address carriers')\nframe = _weakest_comparison_call_fields(memory, frame, 144594, 142364)\nsentinel = state.read(4294955776, 2)\nframe = _contact_status(frame, sentinel, 16)\nif negative_word(sentinel):\n    return _retreat_carry_fields(memory, frame, False)\nframe = _weakest_comparison_call_fields(memory, frame, 142412, 142376)\nframe = _first_word(frame, 'target_x', low16(frame.choice))\nframe = _weakest_comparison_call_fields(memory, frame, 47816, 142384)\nframe = _first_shift_word(frame, 'target_x', low16(frame.target_x), 2)\nstate.sr = state.sr & 65504 | frame.status\ntroops = frame.candidates.long(low16(frame.target_x))\nframe = first_replace(frame, target_x=troops)\nframe = _contact_status(frame, troops, 32)\nown_strength = low16(frame.target_x) * low16(frame.target_y)\nframe = first_replace(frame, target_x=own_strength)\nframe = _contact_status(frame, own_strength, 32)\nframe = _first_compare_long(frame, frame.unit, frame.target_x)\nreturn _retreat_carry_fields(memory, frame, bool(frame.status & 5))"}})
INLINE_HELPERS += ('_weakest_comparison_call_fields', 'compare_actor_to_weakest_contact_strength_fields')
