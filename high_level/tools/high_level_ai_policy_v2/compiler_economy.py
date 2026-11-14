"""Complete structured semantic contracts lowered to ordinary GNU operations.

Only explicit business Python is compilation input. Complete typed flows are
consumed, approved constants are editable, and unknown edits fail closed.
"""
import ast
from copy import deepcopy

from .compiler_common import CompileError, semantic_functions, lower_declared
from .target import ECONOMY_BINDINGS, TABLE_BINDINGS, SCALAR_BINDINGS

DECLARATIONS = {'select_welfare_officer': {'signature': 'state: GameState',
                            'returns': 'tuple[Word, Word]',
                            'flow': 'roster = state.economy_roster.cursor()\n'
                                    'intelligence = state.officer_intelligence\n'
                                    'education = state.officer_education\n'
                                    'best_score = u16(0)\n'
                                    'best_officer = u16(65535)\n'
                                    'while True:\n'
                                    '    officer = roster.next_word()\n'
                                    '    if negative_word(officer):\n'
                                    '        break\n'
                                    '    if officer & 16384 != 0:\n'
                                    '        continue\n'
                                    '    officer = u16(officer & 255)\n'
                                    '    score = u16(education.byte(officer))\n'
                                    '    index = u16(officer << 1)\n'
                                    '    score = u16(score + intelligence.word(index))\n'
                                    '    if score > best_score:\n'
                                    '        best_score = score\n'
                                    '        best_officer = officer\n'
                                    'return (best_score, best_officer)',
                            'slots': {}},
 'plan_welfare_budget': {'signature': 'state: GameState',
                         'returns': 'None',
                         'flow': 'sample = u32(low16(state.sample_random()))\n'
                                 'original_sample = sample\n'
                                 'sample = u32(sample << 2)\n'
                                 'sample = u32(sample + original_sample)\n'
                                 'sample = u32(sample << 2)\n'
                                 'sample = u32(sample + original_sample)\n'
                                 'sample = swap_words(sample)\n'
                                 'factor = u16(low16(sample) + 20)\n'
                                 'gold = state.city_gold\n'
                                 'city = u16(state.current_city() << 2)\n'
                                 'balance = gold.long(city)\n'
                                 'lower_product = u32(low16(balance) * factor)\n'
                                 'balance = swap_words(balance)\n'
                                 'balance = u32(low16(balance) * factor)\n'
                                 'balance = swap_words(balance)\n'
                                 'balance = u32(balance + lower_product)\n'
                                 'budget, remainder = state.divide_signed(balance, 100)\n'
                                 'if budget > 9999:\n'
                                 '    budget = u32(9999)\n'
                                 'state.set_order_amount(budget)',
                         'slots': {}},
 'select_development_officer': {'signature': 'state: GameState',
                                'returns': 'tuple[Word, Word]',
                                'flow': 'roster = state.economy_roster.cursor()\n'
                                        'intelligence = state.officer_intelligence\n'
                                        'best_score = u16(0)\n'
                                        'best_officer = u16(65535)\n'
                                        'while True:\n'
                                        '    officer = roster.next_word()\n'
                                        '    if negative_word(officer):\n'
                                        '        break\n'
                                        '    if officer & 16384 != 0:\n'
                                        '        continue\n'
                                        '    index = u16(officer << 1)\n'
                                        '    score = intelligence.word(index)\n'
                                        '    if score > best_score:\n'
                                        '        best_score = score\n'
                                        '        best_officer = officer\n'
                                        'return (best_score, best_officer)',
                                'slots': {}},
 'plan_development_budget': {'signature': 'state: GameState',
                             'returns': 'None',
                             'flow': 'sample = u32(low16(state.sample_random()))\n'
                                     'original_sample = sample\n'
                                     'sample = u32(sample << 2)\n'
                                     'sample = u32(sample + original_sample)\n'
                                     'sample = u32(sample << 2)\n'
                                     'sample = u32(sample + original_sample)\n'
                                     'sample = swap_words(sample)\n'
                                     'discarded_factor = u16(low16(sample) + 30)\n'
                                     'gold = state.city_gold\n'
                                     'factor = u16(state.current_city() << 2)\n'
                                     'balance = gold.long(factor)\n'
                                     'lower_product = u32(low16(balance) * factor)\n'
                                     'balance = swap_words(balance)\n'
                                     'balance = u32(low16(balance) * factor)\n'
                                     'balance = swap_words(balance)\n'
                                     'balance = u32(balance + lower_product)\n'
                                     'budget, remainder = state.divide_signed(balance, 100)\n'
                                     'if budget > 9999:\n'
                                     '    budget = u32(9999)\n'
                                     'state.set_order_amount(budget)',
                             'slots': {}},
 'select_resource_support_city': {'signature': 'state: GameState',
                                  'returns': 'tuple[Long, Word]',
                                  'flow': 'force = state.current_force()\n'
                                          'current_city = state.current_city()\n'
                                          'troops = state.officer_troops\n'
                                          'gold = state.city_gold\n'
                                          'rice = state.city_rice\n'
                                          'processed = state.city_processed\n'
                                          'minimum = u32(4294967295)\n'
                                          'selected = u16(65535)\n'
                                          'owners = state.city_owners_predecrement.cursor()\n'
                                          'for city in descending_inclusive(40):\n'
                                          '    if city == 0:\n'
                                          '        break\n'
                                          '    owner = owners.previous_byte()\n'
                                          '    if low8(force) != owner:\n'
                                          '        continue\n'
                                          '    if processed.byte(city) != 0:\n'
                                          '        continue\n'
                                          '    if city == current_city:\n'
                                          '        continue\n'
                                          '    requirement = '
                                          'estimate_city_troop_requirement(state, city, troops)\n'
                                          '    processed = state.officer_assignments\n'
                                          '    index = u16(city << 2)\n'
                                          '    if requirement <= rice.long(index):\n'
                                          '        continue\n'
                                          '    total = gold.long(index)\n'
                                          '    total = u32(total + rice.long(index))\n'
                                          '    if total < minimum:\n'
                                          '        minimum = total\n'
                                          '        selected = city\n'
                                          'return (minimum, selected)',
                                  'slots': {}},
 'estimate_city_troop_requirement': {'signature': 'state: GameState, city: Word, troops: Table',
                                     'returns': 'Long',
                                     'flow': 'city = uint(city, 16)\n'
                                             'troops = state.checked_table(troops)\n'
                                             'assignments = '
                                             'state.officer_action_predecrement.cursor()\n'
                                             'total = u32(0)\n'
                                             'for officer in descending_inclusive(255):\n'
                                             '    assignment = u16(assignments.previous_byte() & '
                                             '63)\n'
                                             '    if assignment == city:\n'
                                             '        index = u16(officer << 2)\n'
                                             '        total = u32(total + troops.long(index))\n'
                                             '        total = u32(total + 100)\n'
                                             'total = divu_retained(total, 10)\n'
                                             'total = u32(low16(total))\n'
                                             'saved_total = total\n'
                                             'total = u32(total << 3)\n'
                                             'total = u32(total + saved_total)\n'
                                             'return total',
                                     'slots': {}},
 'plan_city_defense_target': {'signature': 'state: GameState',
                              'returns': 'None',
                              'flow': 'state.sample_random()\n'
                                      'summary = state.force_summary\n'
                                      'index = u16(state.current_force() << 2)\n'
                                      'tier = u16(summary.word(index) - 5)\n'
                                      'if tier > 3:\n'
                                      '    tier = u16(3)\n'
                                      'saved_tier = tier\n'
                                      'tier = u16(tier << 2)\n'
                                      'tier = u16(tier + saved_tier)\n'
                                      'target = u16(55 - tier)\n'
                                      'sample = u32(state.seed_word())\n'
                                      'saved_sample = sample\n'
                                      'sample = u32(sample << 2)\n'
                                      'sample = u32(sample + saved_sample)\n'
                                      'sample = u32(sample << 1)\n'
                                      'sample = swap_words(sample)\n'
                                      'target = u16(target + low16(sample))\n'
                                      'defense = state.city_defense_targets\n'
                                      'welfare = state.city_welfare\n'
                                      'city = u16(state.current_city() << 2)\n'
                                      'if welfare.long(city) < 40:\n'
                                      '    target = u16(target - 10)\n'
                                      'defense.set_long(city, u32(s16(target)))',
                              'slots': {}},
 'plan_force_support_action': {'signature': 'state: GameState',
                               'returns': 'None',
                               'flow': 'state.sample_random()\n'
                                       'owned = state.count_force_cities(state.current_force())\n'
                                       'cities, rival = state.select_force_by_city_count()\n'
                                       'if negative_word(rival):\n'
                                       '    state.set_command(2)\n'
                                       '    return\n'
                                       'threshold = u16(2)\n'
                                       'if cities <= owned:\n'
                                       '    threshold = u16(1)\n'
                                       'sample = u32(state.seed_word())\n'
                                       'sample = u32(sample << 3)\n'
                                       'sample = swap_words(sample)\n'
                                       'if low16(sample) >= threshold:\n'
                                       '    state.set_command(2)\n'
                                       'else:\n'
                                       '    state.set_support_city(rival)\n'
                                       '    state.set_support_amount(0)\n'
                                       '    state.set_command(7)',
                               'slots': {}},
 'clear_economy_command': {'signature': 'state: GameState',
                           'returns': 'None',
                           'flow': 'state.set_command(65535)',
                           'slots': {}},
 'count_economy_roster': {'signature': 'state: GameState',
                          'returns': 'Word',
                          'flow': 'roster = state.economy_roster.cursor()\n'
                                  'count = u16(0)\n'
                                  'while True:\n'
                                  '    if negative_word(roster.next_word()):\n'
                                  '        break\n'
                                  '    count = u16(count + 1)\n'
                                  'return count',
                          'slots': {}},
 'select_roster_intelligence_max': {'signature': 'state: GameState',
                                    'returns': 'tuple[Word, Word]',
                                    'flow': 'roster = state.economy_roster.cursor()\n'
                                            'intelligence = state.officer_intelligence\n'
                                            'best_score = u16(0)\n'
                                            'best_officer = u16(65535)\n'
                                            'while True:\n'
                                            '    officer = roster.next_word()\n'
                                            '    if negative_word(officer):\n'
                                            '        break\n'
                                            '    score = intelligence.word(u16(officer << 1))\n'
                                            '    if score > best_score:\n'
                                            '        best_score = score\n'
                                            '        best_officer = officer\n'
                                            'return (best_score, best_officer)',
                                    'slots': {}},
 'plan_foreign_officer_recruitment': {'signature': 'state: GameState',
                                      'returns': 'None',
                                      'flow': 'city = state.current_city()\n'
                                              'state.set_roster_exclusion(65535)\n'
                                              'count = state.build_roster(city)\n'
                                              'if count >= 10:\n'
                                              '    state.set_command(3)\n'
                                              '    return\n'
                                              'score, officer, city, first, second = '
                                              'select_foreign_neighbor_officer(state)\n'
                                              'if negative_word(officer):\n'
                                              '    state.set_command(3)\n'
                                              '    return\n'
                                              'if first < 75 and second < 75:\n'
                                              '    state.set_command(3)\n'
                                              '    return\n'
                                              'sample = state.sample_random()\n'
                                              'if sample & 16 != 0:\n'
                                              '    state.set_command(3)\n'
                                              'else:\n'
                                              '    state.set_candidate_officer(officer)\n'
                                              '    state.set_selected_city(city)\n'
                                              '    state.set_command(6)',
                                      'slots': {}},
 'select_foreign_neighbor_officer': {'signature': 'state: GameState',
                                     'returns': 'tuple[Word, Word, Word, Word, Word]',
                                     'flow': 'neighbors = '
                                             'state.neighbors.at(u16(state.current_city() << '
                                             '3)).cursor()\n'
                                             'force = state.current_force()\n'
                                             'primary = state.officer_primary_attribute\n'
                                             'secondary = state.officer_intelligence\n'
                                             'status = state.officer_status\n'
                                             'owners = state.city_owners\n'
                                             'processed = state.city_processed\n'
                                             'best_score = u16(0)\n'
                                             'best_officer = u16(65535)\n'
                                             'best_city = u16(65535)\n'
                                             'first = '
                                             'state.neighbor_selection_context.retained_first_score\n'
                                             'second = '
                                             'state.neighbor_selection_context.retained_second_score\n'
                                             'while True:\n'
                                             '    city = u16(neighbors.next_byte())\n'
                                             '    if negative_byte(low8(city)):\n'
                                             '        break\n'
                                             '    if processed.byte(city) != 0:\n'
                                             '        continue\n'
                                             '    if owners.byte(city) == low8(force):\n'
                                             '        continue\n'
                                             '    best_score, best_officer, best_city = '
                                             'scan_city_officer_candidate(state, city, best_score, '
                                             'best_officer, best_city, primary, secondary, '
                                             'status)\n'
                                             'if not negative_word(best_officer):\n'
                                             '    index = u16(best_officer << 1)\n'
                                             '    first = primary.word(index)\n'
                                             '    second = secondary.word(index)\n'
                                             'return (best_score, best_officer, best_city, first, '
                                             'second)',
                                     'slots': {}},
 'scan_city_officer_candidate': {'signature': 'state: GameState, city: Word, best_score: Word, '
                                              'best_officer: Word, best_city: Word, primary: '
                                              'Table, secondary: Table, status: Table',
                                 'returns': 'tuple[Word, Word, Word]',
                                 'flow': 'city = uint(city, 16)\n'
                                         'best_score = uint(best_score, 16)\n'
                                         'best_officer = uint(best_officer, 16)\n'
                                         'best_city = uint(best_city, 16)\n'
                                         'primary = state.checked_table(primary)\n'
                                         'secondary = state.checked_table(secondary)\n'
                                         'status = state.checked_table(status)\n'
                                         'owner = u16(state.city_owners.byte(city))\n'
                                         'if negative_byte(low8(owner)):\n'
                                         '    return (best_score, best_officer, best_city)\n'
                                         'leader = state.force_heads.word(u16(owner << 1))\n'
                                         'assignments = state.officer_assignments\n'
                                         'for officer in descending_inclusive(255):\n'
                                         '    if assignments.byte(officer) != low8(city):\n'
                                         '        continue\n'
                                         '    if low8(officer) == low8(leader):\n'
                                         '        continue\n'
                                         '    if status.byte(officer) > 65:\n'
                                         '        continue\n'
                                         '    index = u16(officer << 1)\n'
                                         '    score = primary.word(index)\n'
                                         '    score = u16(score + secondary.word(index))\n'
                                         '    if score > best_score:\n'
                                         '        best_score = score\n'
                                         '        best_officer = officer\n'
                                         '        best_city = city\n'
                                         'return (best_score, best_officer, best_city)',
                                 'slots': {}},
 'choose_resource_action': {'signature': 'state: GameState',
                            'returns': 'None',
                            'flow': 'gold = state.city_gold\n'
                                    'city = u16(state.current_city() << 2)\n'
                                    'if gold.long(city) >= 10000:\n'
                                    '    state.set_command(7)\n'
                                    'else:\n'
                                    '    state.set_command(4)',
                            'slots': {}},
 'choose_training_action': {'signature': 'state: GameState',
                            'returns': 'None',
                            'flow': 'candidate = query_training_candidate(state)\n'
                                    'order = decide_training_order(candidate)\n'
                                    'submit_training_order(state, order)',
                            'slots': {}},
 'select_roster_training_min': {'signature': 'state: GameState',
                                'returns': 'tuple[Word, Word]',
                                'flow': 'candidate = query_training_candidate(state)\n'
                                        'return candidate.minimum_score, candidate.officer_id',
                                'slots': {}},
 'commit_recruitment_candidate': {'signature': 'state: GameState',
                                  'returns': 'None',
                                  'flow': 'city = state.current_city()\n'
                                          'state.set_roster_exclusion(65535)\n'
                                          'count = state.build_roster(city)\n'
                                          'if count < 10:\n'
                                          '    city = state.current_city()\n'
                                          '    assignments = state.officer_assignments\n'
                                          '    candidate = state.candidate_officer()\n'
                                          '    assignments.set_byte(candidate, low8(city))\n'
                                          '    progress = state.officer_progress\n'
                                          '    officer = u16(state.selected_officer() << 1)\n'
                                          '    gain = u16(progress.word(officer) + 10)\n'
                                          '    if gain > 999:\n'
                                          '        gain = u16(999)\n'
                                          '    progress.set_word(officer, gain)\n'
                                          '    officer = u16(officer >> 1)\n'
                                          '    action = state.officer_action\n'
                                          '    action.set_byte(officer, 1)\n'
                                          '    state.mark_selected_roster_bit14(officer)\n'
                                          'state.set_command(8)',
                                  'slots': {}},
 'select_unmarked_roster_intelligence_max': {'signature': 'state: GameState',
                                             'returns': 'tuple[Word, Word]',
                                             'flow': 'roster = state.economy_roster.cursor()\n'
                                                     'intelligence = state.officer_intelligence\n'
                                                     'best_score = u16(0)\n'
                                                     'best_officer = u16(65535)\n'
                                                     'while True:\n'
                                                     '    officer = roster.next_word()\n'
                                                     '    if negative_word(officer):\n'
                                                     '        break\n'
                                                     '    if officer & 16384 != 0:\n'
                                                     '        continue\n'
                                                     '    score = intelligence.word(u16(officer << '
                                                     '1))\n'
                                                     '    if score > best_score:\n'
                                                     '        best_score = score\n'
                                                     '        best_officer = officer\n'
                                                     'return (best_score, best_officer)',
                                             'slots': {}},
 'clear_candidate_city_order': {'signature': 'state: GameState',
                                'returns': 'None',
                                'flow': 'orders = state.city_orders\n'
                                        'city = u16(state.selected_city() << 1)\n'
                                        'city = u16(city + state.selected_city())\n'
                                        'city = u16(city << 2)\n'
                                        'candidate = state.candidate_officer()\n'
                                        'if candidate == orders.word(city):\n'
                                        '    orders.set_word(city, 65535)\n'
                                        'elif candidate == orders.word(city, 4):\n'
                                        '    orders.set_word(city, 65535, 4)\n'
                                        'elif candidate == orders.word(city, 8):\n'
                                        '    orders.set_word(city, 65535, 8)',
                                'slots': {}},
 'plan_equipment_action': {'signature': 'state: GameState',
                           'returns': 'None',
                           'flow': 'city = u16(state.current_city() << 1)\n'
                                   'head = state.city_heads.word(city)\n'
                                   'action = state.officer_action\n'
                                   'if action.byte(head) == 0:\n'
                                   '    sort_equipment_roster(state)\n'
                                   '    purchase_roster_equipment(state)\n'
                                   'state.set_command(10)',
                           'slots': {}},
 'sort_equipment_roster': {'signature': 'state: GameState',
                           'returns': 'None',
                           'flow': 'roster = state.economy_roster.cursor()\n'
                                   'attributes = state.officer_primary_attribute\n'
                                   'work = state.equipment_work.cursor()\n'
                                   'count = u16(0)\n'
                                   'while True:\n'
                                   '    officer = roster.next_word()\n'
                                   '    if negative_word(officer):\n'
                                   '        break\n'
                                   '    officer = u16(officer & 255)\n'
                                   '    index = u16(officer << 1)\n'
                                   '    work.append_word(attributes.word(index))\n'
                                   '    count = u16(count + 1)\n'
                                   'if count == 1:\n'
                                   '    return\n'
                                   'limit = u16(count << 1)\n'
                                   'work = state.equipment_work\n'
                                   'roster = state.economy_roster\n'
                                   'while True:\n'
                                   '    index = u16(2)\n'
                                   '    while True:\n'
                                   '        previous = work.word(index, -2)\n'
                                   '        if previous < work.word(index):\n'
                                   '            previous = work.word(index)\n'
                                   '            work.set_word(index, work.word(index, -2))\n'
                                   '            work.set_word(index, previous, -2)\n'
                                   '            previous = roster.word(index)\n'
                                   '            roster.set_word(index, roster.word(index, -2))\n'
                                   '            roster.set_word(index, previous, -2)\n'
                                   '        index = u16(index + 2)\n'
                                   '        if index >= limit:\n'
                                   '            break\n'
                                   '    limit = u16(limit - 2)\n'
                                   '    if limit <= 2:\n'
                                   '        break',
                           'slots': {}},
 'purchase_roster_equipment': {'signature': 'state: GameState',
                               'returns': 'None',
                               'flow': 'views = read_equipment_purchase_views(state)\n'
                                       'remaining = views.initial_balance\n'
                                       'level = views.retained_level\n'
                                       'while True:\n'
                                       '    officer = views.roster.next_word()\n'
                                       '    if negative_word(officer):\n'
                                       '        break\n'
                                       '    selection = read_officer_equipment_categories(state, views.attributes, officer)\n'
                                       '    while True:\n'
                                       '        category = u16(selection.categories.next_byte())\n'
                                       '        if negative_byte(low8(category)):\n'
                                       '            break\n'
                                       '        level = read_equipment_level(views.equipment, category, selection.equipment_row, level)\n'
                                       '        if level >= 3:\n'
                                       '            continue\n'
                                       '        quote = read_equipment_quote(state, category, level)\n'
                                       '        level = quote.next_level\n'
                                       '        decision = decide_equipment_budget(quote, remaining)\n'
                                       '        if decision is EquipmentBudgetDecision.REJECT:\n'
                                       '            break\n'
                                       '        remaining = commit_equipment_purchase(views.equipment, remaining, quote)\n'
                                       '        break\n'
                                       'settle_equipment_balance(views, remaining)',
                               'slots': {}},
 'plan_troop_purchase_action': {'signature': 'state: GameState',
                                'returns': 'None',
                                'flow': 'if state.ai_recruitment_capacity_gate().carry == 0:\n'
                                        '    sort_equipment_roster(state)\n'
                                        '    distribution = '
                                        'state.distribute_existing_troop_pool()\n'
                                        '    if distribution.carry == 0:\n'
                                        '        '
                                        'state.buy_and_distribute_troops(state.troop_purchase_context.retained_budget)\n'
                                        'state.set_command(11)',
                                'slots': {}},
 'clear_equipment_command': {'signature': 'state: GameState',
                             'returns': 'None',
                             'flow': 'state.set_command(65535)',
                             'slots': {}}}


APPROVED = {'domain': {'GameState','Word','Long','Table','uint','u16','u32','low8','low16','high16','replace_byte','swap_words','s16','negative_byte','negative_word','descending_inclusive','divu_retained'}}
APPROVED['contexts_training'] = {
    'TrainingCandidate', 'TrainingOrder', 'checked_training_candidate',
    'checked_training_order',
}
APPROVED['contexts_equipment'] = {
    'EquipmentPurchaseViews', 'OfficerEquipmentCategories', 'EquipmentQuote',
    'EquipmentBudgetDecision', 'checked_equipment_quote', 'checked_equipment_views',
}
APPROVED['contexts_recruitment'] = {
    'RecruitmentBest', 'RecruitmentCandidate', 'RecruitmentNeighborViews',
    'RecruitmentOrder', 'RecruitmentPredicate', 'checked_recruitment_best', 'checked_recruitment_candidate',
    'checked_recruitment_submission_order',
}
APPROVED['contexts_domestic'] = {
    'DomesticOfficer', 'CityBudgetBalance', 'ResourceSupportViews',
    'CitySupplyRequirement', 'ResourceSupportCandidate', 'CityResourceOrder',
    'DomesticPredicate', 'checked_city_resource_order',
}
# Editable business rules are bounded scalar choices, not code-address slots.
DECLARATIONS['plan_welfare_budget']['slots'] = {9999: ('budget_cap',0,0xFFFFFFFF)}
DECLARATIONS['plan_development_budget']['slots'] = {9999: ('budget_cap',0,0xFFFFFFFF)}
DECLARATIONS['estimate_city_troop_requirement']['slots'] = {100: ('troop_margin',0,0xFFFFFFFF)}
DECLARATIONS['choose_resource_action']['slots'] = {10000: ('gold_threshold',0,0xFFFFFFFF)}
DECLARATIONS['commit_recruitment_candidate']['slots'] = {999: ('progress_cap',0,65535)}

def _address(port):
    row = TABLE_BINDINGS[port] if port in TABLE_BINDINGS else SCALAR_BINDINGS[port]
    address = row['address'] & (65535 if row['suffix']=='w' else 0xFFFFFFFF)
    return '0x%x:%s' % (address,row['suffix'])

def _lea(e,port,register):
    row=TABLE_BINDINGS[port];e.ins('lea.l',_address(port)+',%'+register,4 if row['suffix']=='w' else 6)

def _load(e,port,register,width='w'):
    row=SCALAR_BINDINGS[port];e.ins('move.'+width,_address(port)+',%'+register,4 if row['suffix']=='w' else 6)

def _store(e,port,register,width='w'):
    row=SCALAR_BINDINGS[port];e.ins('move.'+width,'%'+register+','+_address(port),4 if row['suffix']=='w' else 6)

def _constant(e,port,value,width='w'):
    row=SCALAR_BINDINGS[port];e.ins('move.'+width,'#%d,%s'%(value,_address(port)),6 if row['suffix']=='w' else 8)

def _jump(e,op,label,wide=True): e.ins(op+('.w' if wide else '.b'),label,4 if wide else 2)
def _call(e,name,absolute=False): e.ins('jsr' if absolute else 'bsr.w',name+(':l' if absolute else ''),6 if absolute else 4)

def _roster_max(e,rules,*,marked=False,education=False,loaded='d4',score_false_branch='bls'):
    _lea(e,'economy_roster','a0');_lea(e,'officer_intelligence','a1')
    if education:_lea(e,'officer_education','a2')
    e.ins('clr.w','%d0');e.ins('move.w','#65535,%d1',4)
    loop,done=e.fresh('roster'),e.fresh('done');e.label(loop)
    e.ins('move.w','(%a0)+,%d2');_jump(e,'bmi',done)
    if marked:
        e.ins('btst.l','#14,%d2',4);_jump(e,'bne',loop,False)
    if education:
        e.ins('andi.w','#255,%d2',4);e.ins('clr.w','%d4')
        e.ins('move.b','(%a2,%d2.w),%d4',4)
    e.ins('move.w','%d2,%d3');e.ins('lsl.w','#1,%d3')
    if education:e.ins('add.w','(%a1,%d3.w),%d4',4)
    else:e.ins('move.w','(%a1,%d3.w),%'+loaded,4)
    e.ins('cmp.w','%d0,%'+loaded);_jump(e,score_false_branch,loop,False)
    e.ins('move.w','%'+loaded+',%d0');e.ins('move.w','%d2,%d1')
    _jump(e,'bra',loop,False);e.label(done)

def _welfare(e,r): _roster_max(e,r,marked=True,education=True,score_false_branch=r['score_false_branch'])
def _development(e,r): _roster_max(e,r,marked=True,score_false_branch=r['score_false_branch'])
def _intelligence(e,r): _roster_max(e,r,loaded='d3')
def _unmarked_intelligence(e,r): _roster_max(e,r,marked=True,loaded='d3')

def _budget(e,r,*,development=False):
    _call(e,'step_random',True);e.ins('andi.l','#65535,%d0',6)
    e.ins('move.l','%d0,%d1');e.ins('lsl.l','#2,%d0');e.ins('add.l','%d1,%d0')
    e.ins('lsl.l','#2,%d0');e.ins('add.l','%d1,%d0');e.ins('swap','%d0')
    e.ins('addi.w','#%d,%%d0'%(30 if development else 20),4)
    _lea(e,'city_gold','a0');_load(e,'current_city','d0' if development else 'd1')
    e.ins('lsl.w','#2,%'+('d0' if development else 'd1'))
    e.ins('move.l','(%a0,%'+('d0' if development else 'd1')+'.w),%d1',4)
    e.ins('move.w','%d1,%d2');e.ins('mulu.w','%d0,%d2');e.ins('swap','%d1')
    e.ins('mulu.w','%d0,%d1');e.ins('swap','%d1');e.ins('add.l','%d2,%d1')
    e.ins('moveq','#100,%d2');_call(e,'signed_divmod',True)
    cap=r['budget_cap'];e.ins('cmpi.l','#%d,%%d1'%cap,6);done=e.fresh('bounded')
    _jump(e,r['budget_false_branch'],done);e.ins('move.l','#%d,%%d1'%cap,6);e.label(done);_store(e,'order_amount','d1','l')

def _welfare_budget(e,r): _budget(e,r)
def _development_budget(e,r): _budget(e,r,development=True)

def _support(e,r):
    _load(e,'current_force','d0');_load(e,'current_city','d1')
    for p,a in [('officer_troops','a0'),('city_gold','a1'),('city_rice','a2'),('city_processed','a4')]:_lea(e,p,a)
    e.ins('moveq','#-1,%d2');e.ins('move.w','#65535,%d4',4);_lea(e,'city_owners_predecrement','a3')
    e.ins('move.w','#40,%d3',4);loop,latch=e.fresh('city'),e.fresh('next');e.label(loop)
    e.ins('cmp.b','-(%a3),%d0');_jump(e,'bne',latch)
    e.ins('tst.b','(%a4,%d3.w)',4);_jump(e,'bne',latch)
    e.ins('cmp.w','%d1,%d3');_jump(e,'beq',latch)
    _call(e,'estimate_city_troop_requirement');e.ins('move.w','%d3,%d5');e.ins('lsl.w','#2,%d5')
    e.ins('cmp.l','(%a2,%d5.w),%d6',4);_jump(e,r['supply_true_branch'],latch)
    e.ins('move.l','(%a1,%d5.w),%d7',4);e.ins('add.l','(%a2,%d5.w),%d7',4)
    e.ins('cmp.l','%d2,%d7');_jump(e,r['total_false_branch'],latch);e.ins('move.l','%d7,%d2');e.ins('move.w','%d3,%d4')
    e.label(latch);e.ins('subq.w','#1,%d3');_jump(e,'bne',loop,False)

def _requirement(e,r):
    e.ins('movem.l','%d4,-(%a7)',4);_lea(e,'officer_action_predecrement','a4')
    e.ins('move.w','#255,%d5',4);e.ins('moveq','#0,%d6')
    loop,latch=e.fresh('member'),e.fresh('next');e.label(loop);e.ins('move.b','-(%a4),%d7')
    e.ins('andi.w','#63,%d7',4);e.ins('cmp.w','%d3,%d7');_jump(e,'bne',latch)
    e.ins('move.w','%d5,%d4');e.ins('lsl.w','#2,%d4');e.ins('add.l','(%a0,%d4.w),%d6',4)
    e.ins('addi.l','#%d,%%d6'%r['troop_margin'],6);e.label(latch);e.ins('dbra','%d5,'+loop,4)
    e.ins('divu.w','#10,%d6',4);e.ins('andi.l','#65535,%d6',6)
    e.ins('move.l','%d6,%d4');e.ins('lsl.l','#3,%d6');e.ins('add.l','%d4,%d6')
    e.ins('movem.l','(%a7)+,%d4',4)

def _defense(e,r):
    _call(e,'step_random',True);_lea(e,'force_summary','a0');_load(e,'current_force','d0')
    e.ins('lsl.w','#2,%d0');e.ins('move.w','(%a0,%d0.w),%d1',4);e.ins('subq.w','#5,%d1')
    e.ins('cmpi.w','#3,%d1',4);tier=e.fresh('tier');_jump(e,'bls',tier);e.ins('move.w','#3,%d1',4);e.label(tier)
    e.ins('move.w','%d1,%d2');e.ins('lsl.w','#2,%d1');e.ins('add.w','%d2,%d1')
    e.ins('move.w','#55,%d2',4);e.ins('sub.w','%d1,%d2');e.ins('moveq','#0,%d0')
    _load(e,'seed_word','d0');e.ins('move.l','%d0,%d1');e.ins('lsl.l','#2,%d0');e.ins('add.l','%d1,%d0')
    e.ins('lsl.l','#1,%d0');e.ins('swap','%d0');e.ins('add.w','%d0,%d2')
    _lea(e,'city_defense_targets','a0');_lea(e,'city_welfare','a1');_load(e,'current_city','d0');e.ins('lsl.w','#2,%d0')
    e.ins('cmpi.l','#40,(%a1,%d0.w)',8);store=e.fresh('store');_jump(e,'bcc',store)
    e.ins('subi.w','#10,%d2',4);e.label(store);e.ins('ext.l','%d2');e.ins('move.l','%d2,(%a0,%d0.w)',4)

def _force_action(e,r):
    _call(e,'step_random',True);_load(e,'current_force','d0');_call(e,'count_force_cities')
    e.ins('move.w','%d1,%d7');_call(e,'select_force_by_city_count')
    e.ins('tst.w','%d4');no=e.fresh('no_support');send=e.fresh('send');done=e.fresh('done');_jump(e,'bmi',no)
    e.ins('move.w','#2,%d1',4);e.ins('cmp.w','%d7,%d3');threshold=e.fresh('threshold')
    _jump(e,'bhi',threshold);e.ins('move.w','#1,%d1',4);e.label(threshold)
    e.ins('moveq','#0,%d0');_load(e,'seed_word','d0');e.ins('lsl.l','#3,%d0');e.ins('swap','%d0')
    e.ins('cmp.w','%d1,%d0');_jump(e,'bcs',send);e.label(no);_constant(e,'command',2);_jump(e,'bra',done)
    e.label(send);_store(e,'support_city','d4');e.ins('clr.w',_address('support_amount'),4);_constant(e,'command',7);e.label(done)

def _clear(e,r): _constant(e,'command',65535)

def _count(e,r):
    _lea(e,'economy_roster','a0');e.ins('clr.w','%d0');loop,done=e.fresh('member'),e.fresh('done')
    e.label(loop);e.ins('tst.w','(%a0)+');_jump(e,'bmi',done);e.ins('addq.w','#1,%d0');_jump(e,'bra',loop,False);e.label(done)

def _recruit_plan(e,r):
    _load(e,'current_city','d0');_constant(e,'roster_exclusion',65535);_call(e,'build_roster',True)
    no,yes,done=e.fresh('fallback'),e.fresh('selected'),e.fresh('done')
    e.ins('cmpi.w','#%d,%%d3'%r['city_capacity'],4);_jump(e,r['capacity_false_branch'],no);_call(e,'select_foreign_neighbor_officer')
    e.ins('tst.w','%d2');_jump(e,'bmi',no);e.ins('cmpi.w','#%d,%%d5'%r['primary_threshold'],4);_jump(e,r['primary_false_branch'],yes)
    e.ins('cmpi.w','#%d,%%d6'%r['secondary_threshold'],4);_jump(e,r['secondary_true_branch'],no);e.label(yes);_call(e,'step_random',True)
    e.ins('btst.l','#4,%d0',4);_jump(e,'bne',no);_store(e,'candidate_officer','d2');_store(e,'selected_city','d3')
    _constant(e,'command',6);_jump(e,'bra',done);e.label(no);_constant(e,'command',3);e.label(done)

def _neighbor(e,r):
    _lea(e,'neighbors','a0');_load(e,'current_city','d0');e.ins('lsl.w','#3,%d0');e.ins('adda.w','%d0,%a0')
    _load(e,'current_force','d7')
    for p,a in [('officer_primary_attribute','a1'),('officer_intelligence','a2'),('officer_status','a3'),('city_owners','a5'),('city_processed','a6')]:_lea(e,p,a)
    e.ins('clr.w','%d0');e.ins('clr.w','%d1');e.ins('move.w','#65535,%d2',4);e.ins('move.w','#65535,%d3',4)
    loop,end,done=e.fresh('neighbor'),e.fresh('scores'),e.fresh('done');e.label(loop)
    e.ins('move.b','(%a0)+,%d0');_jump(e,'bmi',end);e.ins('tst.b','(%a6,%d0.w)',4);_jump(e,'bne',loop,False)
    e.ins('cmp.b','(%a5,%d0.w),%d7',4);_jump(e,'beq',loop,False);_call(e,'scan_city_officer_candidate');_jump(e,'bra',loop,False)
    e.label(end);e.ins('move.w','%d2,%d4');_jump(e,'bmi',done);e.ins('lsl.w','#1,%d4')
    e.ins('move.w','(%a1,%d4.w),%d5',4);e.ins('move.w','(%a2,%d4.w),%d6',4);e.label(done)

def _scan_city(e,r):
    e.ins('movem.l','%d7/%a5,-(%a7)',4);_lea(e,'city_owners','a5');e.ins('clr.w','%d7')
    e.ins('move.b','(%a5,%d0.w),%d7',4);done=e.fresh('done');_jump(e,'bmi',done)
    e.ins('lsl.w','#1,%d7');_lea(e,'force_heads','a5');e.ins('move.w','(%a5,%d7.w),%d7',4)
    _lea(e,'officer_assignments','a4');e.ins('move.w','#255,%d4',4);loop,latch=e.fresh('member'),e.fresh('next');e.label(loop)
    e.ins('cmp.b','(%a4,%d4.w),%d0',4);_jump(e,'bne',latch);e.ins('cmp.b','%d7,%d4');_jump(e,'beq',latch)
    e.ins('cmpi.b','#65,(%a3,%d4.w)',6);_jump(e,'bhi',latch);e.ins('move.w','%d4,%d5');e.ins('lsl.w','#1,%d5')
    e.ins('move.w','(%a1,%d5.w),%d6',4);e.ins('add.w','(%a2,%d5.w),%d6',4);e.ins('cmp.w','%d1,%d6')
    _jump(e,r['score_false_branch'],latch);e.ins('move.w','%d6,%d1');e.ins('move.w','%d4,%d2');e.ins('move.w','%d0,%d3')
    e.label(latch);e.ins('dbra','%d4,'+loop,4);e.label(done);e.ins('movem.l','(%a7)+,%d7/%a5',4)

def _resource_action(e,r):
    _lea(e,'city_gold','a0');_load(e,'current_city','d0');e.ins('lsl.w','#2,%d0')
    e.ins('cmpi.l','#%d,(%%a0,%%d0.w)'%r['gold_threshold'],8);poor,done=e.fresh('poor'),e.fresh('done')
    _jump(e,r['resource_false_branch'],poor);_constant(e,'command',7);_jump(e,'bra',done);e.label(poor);_constant(e,'command',4);e.label(done)

def _training_action(e,r):
    _call(e,'select_roster_training_min');e.ins('cmpi.w','#%d,%%d0'%r['training_threshold'],4)
    trained,done=e.fresh('trained'),e.fresh('done');_jump(e,r['false_branch'],trained)
    _constant(e,'command',r['true_command']);_jump(e,'bra',done)
    e.label(trained);_constant(e,'command',r['false_command']);e.label(done)

def _training_min(e,r):
    _lea(e,'economy_roster','a0');_lea(e,'officer_training','a1')
    e.ins('move.w','#65535,%d0',4);e.ins('move.w','#65535,%d1',4);e.ins('clr.w','%d3')
    loop,done=e.fresh('member'),e.fresh('done');e.label(loop);e.ins('move.w','(%a0)+,%d2')
    _jump(e,'bmi',done);e.ins('btst.l','#14,%d2',4);_jump(e,'bne',loop,False)
    e.ins('move.b','(%a1,%d2.w),%d3',4);e.ins('cmp.w','%d0,%d3');_jump(e,'bcc',loop,False)
    e.ins('move.w','%d3,%d0');e.ins('move.w','%d2,%d1');_jump(e,'bra',loop,False);e.label(done)

def _commit_recruitment(e,r):
    _load(e,'current_city','d0');_constant(e,'roster_exclusion',65535);_call(e,'build_roster',True)
    done,bounded=e.fresh('done'),e.fresh('bounded');e.ins('cmpi.w','#%d,%%d3'%r['city_capacity'],4);_jump(e,r['capacity_false_branch'],done)
    _load(e,'current_city','d0');_lea(e,'officer_assignments','a0');_load(e,'candidate_officer','d1')
    e.ins('move.b','%d0,(%a0,%d1.w)',4);_lea(e,'officer_progress','a0');_load(e,'selected_officer','d0')
    e.ins('lsl.w','#1,%d0');e.ins('move.w','(%a0,%d0.w),%d1',4);e.ins('addi.w','#10,%d1',4)
    e.ins('cmpi.w','#%d,%%d1'%r['progress_cap'],4);_jump(e,'bls',bounded);e.ins('move.w','#%d,%%d1'%r['progress_cap'],4)
    e.label(bounded);e.ins('move.w','%d1,(%a0,%d0.w)',4);e.ins('lsr.w','#1,%d0');_lea(e,'officer_action','a0')
    e.ins('move.b','#1,(%a0,%d0.w)',6);_call(e,'mark_selected_roster_bit14');e.label(done);_constant(e,'command',8)

def _clear_order(e,r):
    _lea(e,'city_orders','a0');_load(e,'selected_city','d0');e.ins('lsl.w','#1,%d0')
    e.ins('add.w',_address('selected_city')+',%d0',4);e.ins('lsl.w','#2,%d0');_load(e,'candidate_officer','d1')
    second,third,done=e.fresh('second'),e.fresh('third'),e.fresh('done')
    e.ins('cmp.w','(%a0,%d0.w),%d1',4);_jump(e,'bne',second);e.ins('move.w','#65535,(%a0,%d0.w)',6);_jump(e,'bra',done)
    e.label(second);e.ins('cmp.w','4(%a0,%d0.w),%d1',4);_jump(e,'bne',third)
    e.ins('move.w','#65535,4(%a0,%d0.w)',6);_jump(e,'bra',done)
    e.label(third);e.ins('cmp.w','8(%a0,%d0.w),%d1',4);_jump(e,'bne',done);e.ins('move.w','#65535,8(%a0,%d0.w)',6);e.label(done)

def _equipment_action(e,r):
    _load(e,'current_city','d0');e.ins('lsl.w','#1,%d0');_lea(e,'city_heads','a0')
    e.ins('move.w','(%a0,%d0.w),%d0',4);_lea(e,'officer_action','a0');e.ins('tst.b','(%a0,%d0.w)',4)
    done=e.fresh('done');_jump(e,'bne',done);_call(e,'sort_equipment_roster');_call(e,'purchase_roster_equipment');e.label(done);_constant(e,'command',10)

def _sort(e,r):
    _lea(e,'economy_roster','a0');_lea(e,'officer_primary_attribute','a1');_lea(e,'equipment_work','a2');e.ins('clr.w','%d0')
    scan,begin,done=e.fresh('member'),e.fresh('sort'),e.fresh('done');e.label(scan)
    e.ins('move.w','(%a0)+,%d1');_jump(e,'bmi',begin);e.ins('andi.w','#255,%d1',4);e.ins('lsl.w','#1,%d1')
    e.ins('move.w','(%a1,%d1.w),(%a2)+',4);e.ins('addq.w','#1,%d0');_jump(e,'bra',scan,False)
    e.label(begin);e.ins('cmpi.w','#1,%d0',4);_jump(e,'beq',done);e.ins('lsl.w','#1,%d0')
    _lea(e,'equipment_work','a2');_lea(e,'economy_roster','a0');outer,inner,latch=e.fresh('pass'),e.fresh('pair'),e.fresh('next');e.label(outer)
    e.ins('move.w','#2,%d1',4);e.label(inner);e.ins('move.w','-2(%a2,%d1.w),%d2',4)
    e.ins('cmp.w','(%a2,%d1.w),%d2',4);_jump(e,'bcc',latch)
    e.ins('move.w','(%a2,%d1.w),%d2',4);e.ins('move.w','-2(%a2,%d1.w),(%a2,%d1.w)',6)
    e.ins('move.w','%d2,-2(%a2,%d1.w)',4);e.ins('move.w','(%a0,%d1.w),%d2',4)
    e.ins('move.w','-2(%a0,%d1.w),(%a0,%d1.w)',6);e.ins('move.w','%d2,-2(%a0,%d1.w)',4)
    e.label(latch);e.ins('addq.w','#2,%d1');e.ins('cmp.w','%d0,%d1');_jump(e,'bcs',inner,False)
    e.ins('subq.w','#2,%d0');e.ins('cmpi.w','#2,%d0',4);_jump(e,'bhi',outer,False);e.label(done)

def _purchase(e,r):
    _lea(e,'economy_roster','a0');_lea(e,'officer_primary_attribute','a1');_lea(e,'city_gold','a2')
    _load(e,'current_city','d0');e.ins('lsl.w','#2,%d0');e.ins('move.l','(%a2,%d0.w),%d1',4)
    _lea(e,'officer_equipment','a4');outer,row,categories,done=e.fresh('member'),e.fresh('row'),e.fresh('category'),e.fresh('store')
    e.label(outer);e.ins('move.w','(%a0)+,%d2');_jump(e,'bmi',done)
    e.ins('andi.w','#255,%d2',4);e.ins('lsl.w','#1,%d2');e.ins('move.w','(%a1,%d2.w),%d3',4);e.ins('clr.w','%d4')
    e.ins('cmpi.w','#%d,%%d3'%r['primary_threshold'],4);_jump(e,'bcc',row);e.ins('addq.w','#4,%d4')
    e.ins('cmpi.w','#%d,%%d3'%r['secondary_threshold'],4);_jump(e,'bcc',row);e.ins('addq.w','#4,%d4');e.label(row)
    # The PC-relative semantic table has its independent source authority.
    displacement=TABLE_BINDINGS['equipment_categories']['address']-(e.pc+2)
    e.ins('lea.l',str(displacement)+'(%pc),%a3',4);e.ins('nop')
    e.ins('adda.w','%d4,%a3');e.ins('move.w','%d2,%d3');e.ins('lsr.w','#1,%d3');e.ins('add.w','%d2,%d3')
    e.label(categories);e.ins('clr.w','%d4');e.ins('move.b','(%a3)+,%d4');_jump(e,'bmi',outer,False)
    e.ins('move.w','%d4,%d7');e.ins('add.w','%d3,%d7');e.ins('move.b','(%a4,%d7.w),%d5',4)
    e.ins('cmpi.w','#3,%d5',4);_jump(e,'bcc',categories,False);e.ins('move.w','%d4,%d6')
    e.ins('lsl.w','#1,%d6');e.ins('add.w','%d4,%d6');e.ins('add.w','%d5,%d6');e.ins('addq.w','#1,%d5')
    e.ins('lsl.w','#2,%d6');_lea(e,'equipment_prices','a5');e.ins('move.l','(%a5,%d6.w),%d6',4)
    e.ins('move.l','%d1,%d7');e.ins('lsr.l','#2,%d7');e.ins('cmp.l','%d7,%d6');_jump(e,r['budget_reject_branch'],outer,False)
    e.ins('sub.l','%d6,%d1');e.ins('move.b','%d5,(%a4,%d4.w)',4);_jump(e,'bra',outer,False)
    e.label(done);e.ins('move.l','%d1,(%a2,%d0.w)',4)

def _troop_action(e,r):
    done=e.fresh('done');_call(e,'ai_recruitment_capacity_gate');_jump(e,'bcs',done)
    _call(e,'sort_equipment_roster');_call(e,'distribute_existing_troop_pool');_jump(e,'bcs',done)
    _call(e,'buy_and_distribute_troops');e.label(done);_constant(e,'command',11)

LOWERERS={
 'select_welfare_officer':_welfare,'plan_welfare_budget':_welfare_budget,
 'select_development_officer':_development,'plan_development_budget':_development_budget,
 'select_resource_support_city':_support,'estimate_city_troop_requirement':_requirement,
 'plan_city_defense_target':_defense,'plan_force_support_action':_force_action,
 'clear_economy_command':_clear,'count_economy_roster':_count,
 'select_roster_intelligence_max':_intelligence,'plan_foreign_officer_recruitment':_recruit_plan,
 'select_foreign_neighbor_officer':_neighbor,'scan_city_officer_candidate':_scan_city,
 'choose_resource_action':_resource_action,'choose_training_action':_training_action,
 'select_roster_training_min':_training_min,'commit_recruitment_candidate':_commit_recruitment,
 'select_unmarked_roster_intelligence_max':_unmarked_intelligence,
 'clear_candidate_city_order':_clear_order,'plan_equipment_action':_equipment_action,
 'sort_equipment_roster':_sort,'purchase_roster_equipment':_purchase,
 'plan_troop_purchase_action':_troop_action,'clear_equipment_command':_clear,
}

TRAINING_SOURCE_FUNCTIONS = (
    'choose_training_action', 'select_roster_training_min',
    'query_training_candidate', 'decide_training_order', 'submit_training_order',
)

# The three domain helpers are inlined into the existing two native entries.
# Constructors/checkers are typed value operations with no additional DATA.
# All five complete source bodies are admitted, not just their public wrappers.
DECLARATIONS['query_training_candidate'] = {
    'signature': 'state: GameState', 'returns': 'TrainingCandidate',
    'flow': '''roster = state.economy_roster.cursor()
training = state.officer_training
best_score = u16(65535)
best_officer = u16(65535)
score = u16(0)
while True:
    officer = roster.next_word()
    if negative_word(officer):
        break
    if officer & 16384 != 0:
        continue
    score = u16(replace_byte(score, training.byte(officer)))
    if score < best_score:
        best_score = score
        best_officer = officer
return TrainingCandidate(best_score, best_officer)''',
}
DECLARATIONS['decide_training_order'] = {
    'signature': 'candidate: TrainingCandidate', 'returns': 'TrainingOrder',
    'flow': '''candidate = checked_training_candidate(candidate)
if candidate.minimum_score < 80:
    return TrainingOrder.TRAIN
return TrainingOrder.ALTERNATE''',
    'slots': {80: ('training_threshold', 0, 65535)},
}
DECLARATIONS['submit_training_order'] = {
    'signature': 'state: GameState, order: TrainingOrder', 'returns': 'None',
    'flow': '''order = checked_training_order(order)
if order is TrainingOrder.TRAIN:
    state.set_command(8)
else:
    state.set_command(9)''',
}


def _body(function):
    body = function.body
    if (body and isinstance(body[0], ast.Expr) and
            isinstance(body[0].value, ast.Constant) and
            type(body[0].value.value) is str):
        body = body[1:]
    return body


def _named_order(statement):
    if (not isinstance(statement, ast.Return) or
            not isinstance(statement.value, ast.Attribute) or
            not isinstance(statement.value.value, ast.Name) or
            statement.value.value.id != 'TrainingOrder' or
            statement.value.attr not in ('TRAIN', 'ALTERNATE')):
        raise CompileError('training policy branches must return named orders')
    return statement.value.attr


def _command_literal(statement):
    if (not isinstance(statement, ast.Expr) or
            not isinstance(statement.value, ast.Call) or
            len(statement.value.args) != 1 or
            not isinstance(statement.value.args[0], ast.Constant)):
        raise CompileError('training writeback requires one literal WORD command')
    value = statement.value.args[0].value
    if type(value) is not int or not 0 <= value <= 65535:
        raise CompileError('training command must be a strict WORD integer')
    return value


def _training_source(source):
    """Read a finite policy AST, then normalize only consumed semantic choices.

    The normalized tree is solely a topology/type gate. The original operator,
    returned orders and writeback constants are carried to instruction selection
    below; they are not accepted and then discarded. Every remaining expression,
    call, import, return, query operation and native ABI stays fully checked.
    """
    if type(source) is not str or len(source) > 300000:
        raise CompileError('bounded explicit economy Python text required')
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError) as error:
        raise CompileError('invalid economy Python') from error
    functions = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            if node.name in functions:
                raise CompileError('duplicate economy function')
            functions[node.name] = node
    if any(name not in functions for name in TRAINING_SOURCE_FUNCTIONS):
        raise CompileError('the complete training domain chain is required')
    original_functions = {
        name: ast.dump(functions[name], include_attributes=False)
        for name in TRAINING_SOURCE_FUNCTIONS
    }
    policy = _body(functions['decide_training_order'])
    if (len(policy) != 3 or not isinstance(policy[1], ast.If) or
            len(policy[1].body) != 1 or policy[1].orelse):
        raise CompileError('one explicit training-policy comparison required')
    test = policy[1].test
    if (not isinstance(test, ast.Compare) or len(test.ops) != 1 or
            len(test.comparators) != 1):
        raise CompileError('one unsigned WORD policy comparison required')
    # CMP.W compares the nonnegative, validated score to the threshold. Branch
    # on the negated source relation; canonical < remains the original BCC.
    inverse = {ast.Lt: 'bcc', ast.LtE: 'bhi', ast.Gt: 'bls',
               ast.GtE: 'bcs', ast.Eq: 'bne', ast.NotEq: 'beq'}
    false_branch = inverse.get(type(test.ops[0]))
    if false_branch is None:
        raise CompileError('unsupported training policy comparison')
    true_order = _named_order(policy[1].body[0])
    false_order = _named_order(policy[2])
    submission = _body(functions['submit_training_order'])
    if (len(submission) != 2 or not isinstance(submission[1], ast.If) or
            len(submission[1].body) != 1 or len(submission[1].orelse) != 1):
        raise CompileError('one compatibility write per named training order required')
    commands = {
        'TRAIN': _command_literal(submission[1].body[0]),
        'ALTERNATE': _command_literal(submission[1].orelse[0]),
    }
    # A separate copy keeps the admitted source effect evidence unchanged.
    normalized = deepcopy(tree)
    copied = {node.name: node for node in normalized.body
              if isinstance(node, ast.FunctionDef)}
    normalized_policy = _body(copied['decide_training_order'])
    normalized_policy[1].test.ops[0] = ast.Lt()
    normalized_policy[1].body[0].value.attr = 'TRAIN'
    normalized_policy[2].value.attr = 'ALTERNATE'
    normalized_submission = _body(copied['submit_training_order'])[1]
    normalized_submission.body[0].value.args[0].value = 8
    normalized_submission.orelse[0].value.args[0].value = 9
    records = semantic_functions(ast.unparse(normalized), DECLARATIONS, APPROVED)
    rules = dict(records['decide_training_order']['rules'])
    rules.update(false_branch=false_branch,
                 true_command=commands[true_order],
                 false_command=commands[false_order])
    records['choose_training_action']['rules'] = rules
    records['choose_training_action']['effects'] = repr({
        name: original_functions[name]
        for name in ('choose_training_action', 'decide_training_order',
                     'submit_training_order')
    })
    records['select_roster_training_min']['effects'] = repr({
        name: original_functions[name]
        for name in ('select_roster_training_min', 'query_training_candidate')
    })
    native_records = {name: records[name] for name in LOWERERS}
    return native_records, dict(
        comparison=type(test.ops[0]).__name__, **rules,
        true_order=true_order, false_order=false_order,
        source_functions=TRAINING_SOURCE_FUNCTIONS,
        pure_helpers_inlined=True, general_Python=False,
    )


EQUIPMENT_SOURCE_FUNCTIONS = (
    'purchase_roster_equipment', 'read_equipment_purchase_views',
    'read_officer_equipment_categories', 'read_equipment_level',
    'read_equipment_quote', 'decide_equipment_budget',
    'commit_equipment_purchase', 'settle_equipment_balance',
)

# Typed value/checker operations do not add original DATA or new machine entries.
# Every helper is consumed by the same full semantic gate as the native bodies.
DECLARATIONS['read_equipment_purchase_views'] = {
    'signature': 'state: GameState', 'returns': 'EquipmentPurchaseViews',
    'flow': '''roster = state.economy_roster.cursor()
attributes = state.officer_primary_attribute
gold = state.city_gold
city = u16(state.current_city() << 2)
remaining = gold.long(city)
equipment = state.officer_equipment
level = u16(state.equipment_scan_context.retained_level_high_byte << 8)
return EquipmentPurchaseViews(roster, attributes, gold, equipment, city, remaining, level)''',
}
DECLARATIONS['read_officer_equipment_categories'] = {
    'signature': 'state: GameState, attributes: Table, officer: Word',
    'returns': 'OfficerEquipmentCategories',
    'flow': '''attributes = state.checked_table(attributes)
officer = u16(uint(officer, 16) & 255)
index = u16(officer << 1)
score = attributes.word(index)
category_row = u16(0)
if score < 100:
    category_row = u16(category_row + 4)
    if score < 60:
        category_row = u16(category_row + 4)
categories = state.equipment_categories.at(category_row).cursor()
officer_row = u16(index >> 1)
officer_row = u16(officer_row + index)
return OfficerEquipmentCategories(categories, officer_row)''',
    'slots': {100: ('primary_threshold', 0, 65535), 60: ('secondary_threshold', 0, 65535)},
}
DECLARATIONS['read_equipment_level'] = {
    'signature': 'equipment: Table, category: Word, officer_row: Word, retained_level: Word',
    'returns': 'Word',
    'flow': '''equipment = equipment.state.checked_table(equipment)
category = uint(category, 16)
officer_row = uint(officer_row, 16)
retained_level = uint(retained_level, 16)
equipment_slot = u16(category + officer_row)
return u16(replace_byte(retained_level, equipment.byte(equipment_slot)))''',
}
DECLARATIONS['read_equipment_quote'] = {
    'signature': 'state: GameState, category: Word, level: Word',
    'returns': 'EquipmentQuote',
    'flow': '''category = uint(category, 16)
level = uint(level, 16)
price_slot = u16(category << 1)
price_slot = u16(price_slot + category)
price_slot = u16(price_slot + level)
next_level = u16(level + 1)
price_slot = u16(price_slot << 2)
price = state.equipment_prices.long(price_slot)
return EquipmentQuote(category, next_level, price)''',
}
DECLARATIONS['decide_equipment_budget'] = {
    'signature': 'quote: EquipmentQuote, remaining_gold: Long',
    'returns': 'EquipmentBudgetDecision',
    'flow': '''quote = checked_equipment_quote(quote)
remaining_gold = uint(remaining_gold, 32)
available = u32(remaining_gold >> 2)
if quote.price > available:
    return EquipmentBudgetDecision.REJECT
return EquipmentBudgetDecision.PURCHASE''',
}
DECLARATIONS['commit_equipment_purchase'] = {
    'signature': 'equipment: Table, remaining_gold: Long, quote: EquipmentQuote',
    'returns': 'Long',
    'flow': '''equipment = equipment.state.checked_table(equipment)
remaining_gold = uint(remaining_gold, 32)
quote = checked_equipment_quote(quote)
remaining_gold = u32(remaining_gold - quote.price)
equipment.set_byte(quote.category, low8(quote.next_level))
return remaining_gold''',
}
DECLARATIONS['settle_equipment_balance'] = {
    'signature': 'views: EquipmentPurchaseViews, remaining_gold: Long',
    'returns': 'None',
    'flow': '''views = checked_equipment_views(views)
remaining_gold = uint(remaining_gold, 32)
views.gold.set_long(views.city_offset, remaining_gold)''',
}


# Complete recruitment bodies/helpers: development-derived fixed topology.

RECRUITMENT_SOURCE_FUNCTIONS = ('plan_foreign_officer_recruitment', 'select_foreign_neighbor_officer', 'scan_city_officer_candidate', 'commit_recruitment_candidate', 'read_recruitment_city_roster_count', 'recruitment_city_has_capacity', 'decide_foreign_recruitment_candidate', 'decide_foreign_recruitment_lottery', 'submit_foreign_recruitment_order', 'read_foreign_recruitment_views', 'query_foreign_recruitment_candidate', 'query_recruitment_city_candidate', 'read_recruitment_officer_score', 'recruitment_score_is_better', 'assign_live_recruitment_candidate', 'reward_selected_recruitment_officer', 'compute_recruitment_progress_gain')

DECLARATIONS['plan_foreign_officer_recruitment'] = {'signature': 'state: GameState',
 'returns': 'None',
 'flow': 'count = read_recruitment_city_roster_count(state)\n'
         'if not recruitment_city_has_capacity(count):\n'
         '    state.set_command(3)\n'
         '    return\n'
         'candidate = query_foreign_recruitment_candidate(state)\n'
         'order = decide_foreign_recruitment_candidate(candidate)\n'
         'if order is RecruitmentOrder.FALLBACK:\n'
         '    submit_foreign_recruitment_order(state, order, candidate)\n'
         '    return\n'
         'sample = state.sample_random()\n'
         'order = decide_foreign_recruitment_lottery(sample)\n'
         'submit_foreign_recruitment_order(state, order, candidate)'}

DECLARATIONS['select_foreign_neighbor_officer'] = {'signature': 'state: GameState',
 'returns': 'tuple[Word, Word, Word, Word, Word]',
 'flow': 'candidate = query_foreign_recruitment_candidate(state)\n'
         'return (candidate.score, candidate.officer, candidate.city, candidate.primary_score, '
         'candidate.secondary_score)'}

DECLARATIONS['scan_city_officer_candidate'] = {'signature': 'state: GameState, city: Word, best_score: Word, best_officer: Word, best_city: Word, primary: '
              'Table, secondary: Table, status: Table',
 'returns': 'tuple[Word, Word, Word]',
 'flow': 'city = uint(city, 16)\n'
         'best_score = uint(best_score, 16)\n'
         'best_officer = uint(best_officer, 16)\n'
         'best_city = uint(best_city, 16)\n'
         'primary = state.checked_table(primary)\n'
         'secondary = state.checked_table(secondary)\n'
         'status = state.checked_table(status)\n'
         'best = query_recruitment_city_candidate(state, city, RecruitmentBest(best_score, best_officer, '
         'best_city), primary, secondary, status)\n'
         'return (best.score, best.officer, best.city)'}

DECLARATIONS['commit_recruitment_candidate'] = {'signature': 'state: GameState',
 'returns': 'None',
 'flow': 'count = read_recruitment_city_roster_count(state)\n'
         'if recruitment_city_has_capacity(count):\n'
         '    assign_live_recruitment_candidate(state)\n'
         '    reward_selected_recruitment_officer(state)\n'
         'state.set_command(8)'}

DECLARATIONS['read_recruitment_city_roster_count'] = {'signature': 'state: GameState',
 'returns': 'Word',
 'flow': 'city = state.current_city()\nstate.set_roster_exclusion(65535)\nreturn state.build_roster(city)'}

DECLARATIONS['recruitment_city_has_capacity'] = {'signature': 'count: Word',
 'returns': 'RecruitmentPredicate',
 'flow': 'count = uint(count, 16)\nreturn count < 10',
 'slots': {10: ('city_capacity', 0, 65535)}}

DECLARATIONS['decide_foreign_recruitment_candidate'] = {'signature': 'candidate: RecruitmentCandidate',
 'returns': 'RecruitmentOrder',
 'flow': 'candidate = checked_recruitment_candidate(candidate)\n'
         'if negative_word(candidate.officer):\n'
         '    return RecruitmentOrder.FALLBACK\n'
         'if candidate.primary_score < 75 and candidate.secondary_score < 75:\n'
         '    return RecruitmentOrder.FALLBACK\n'
         'return RecruitmentOrder.ATTEMPT',
 'slots': {75: ('attribute_threshold', 0, 65535)}}

DECLARATIONS['decide_foreign_recruitment_lottery'] = {'signature': 'sample: Long',
 'returns': 'RecruitmentOrder',
 'flow': 'sample = uint(sample, 32)\n'
         'if sample & 16 != 0:\n'
         '    return RecruitmentOrder.FALLBACK\n'
         'return RecruitmentOrder.RECRUIT'}

DECLARATIONS['submit_foreign_recruitment_order'] = {'signature': 'state: GameState, order: RecruitmentOrder, candidate: RecruitmentCandidate',
 'returns': 'None',
 'flow': 'order = checked_recruitment_submission_order(order)\n'
         'candidate = checked_recruitment_candidate(candidate)\n'
         'if order is RecruitmentOrder.FALLBACK:\n'
         '    state.set_command(3)\n'
         'else:\n'
         '    state.set_candidate_officer(candidate.officer)\n'
         '    state.set_selected_city(candidate.city)\n'
         '    state.set_command(6)'}

DECLARATIONS['read_foreign_recruitment_views'] = {'signature': 'state: GameState',
 'returns': 'RecruitmentNeighborViews',
 'flow': 'neighbors = state.neighbors.at(u16(state.current_city() << 3)).cursor()\n'
         'force = state.current_force()\n'
         'primary = state.officer_primary_attribute\n'
         'secondary = state.officer_intelligence\n'
         'status = state.officer_status\n'
         'owners = state.city_owners\n'
         'processed = state.city_processed\n'
         'return RecruitmentNeighborViews(neighbors, force, primary, secondary, status, owners, processed)'}

DECLARATIONS['query_foreign_recruitment_candidate'] = {'signature': 'state: GameState',
 'returns': 'RecruitmentCandidate',
 'flow': 'views = read_foreign_recruitment_views(state)\n'
         'best = RecruitmentBest(0, 65535, 65535)\n'
         'first = state.neighbor_selection_context.retained_first_score\n'
         'second = state.neighbor_selection_context.retained_second_score\n'
         'while True:\n'
         '    city = u16(views.neighbors.next_byte())\n'
         '    if negative_byte(low8(city)):\n'
         '        break\n'
         '    if views.processed.byte(city) != 0:\n'
         '        continue\n'
         '    if views.owners.byte(city) == low8(views.force):\n'
         '        continue\n'
         '    best = query_recruitment_city_candidate(state, city, best, views.primary, views.secondary, '
         'views.status)\n'
         'if not negative_word(best.officer):\n'
         '    index = u16(best.officer << 1)\n'
         '    first = views.primary.word(index)\n'
         '    second = views.secondary.word(index)\n'
         'return RecruitmentCandidate(best.score, best.officer, best.city, first, second)'}

DECLARATIONS['query_recruitment_city_candidate'] = {'signature': 'state: GameState, city: Word, best: RecruitmentBest, primary: Table, secondary: Table, '
              'status: Table',
 'returns': 'RecruitmentBest',
 'flow': 'city = uint(city, 16)\n'
         'best = checked_recruitment_best(best)\n'
         'primary = state.checked_table(primary)\n'
         'secondary = state.checked_table(secondary)\n'
         'status = state.checked_table(status)\n'
         'owner = u16(state.city_owners.byte(city))\n'
         'if negative_byte(low8(owner)):\n'
         '    return best\n'
         'leader = state.force_heads.word(u16(owner << 1))\n'
         'assignments = state.officer_assignments\n'
         'for officer in descending_inclusive(255):\n'
         '    if assignments.byte(officer) != low8(city):\n'
         '        continue\n'
         '    if low8(officer) == low8(leader):\n'
         '        continue\n'
         '    if status.byte(officer) > 65:\n'
         '        continue\n'
         '    score = read_recruitment_officer_score(primary, secondary, officer)\n'
         '    if recruitment_score_is_better(score, best.score):\n'
         '        best = RecruitmentBest(score, officer, city)\n'
         'return best'}

DECLARATIONS['read_recruitment_officer_score'] = {'signature': 'primary: Table, secondary: Table, officer: Word',
 'returns': 'Word',
 'flow': 'primary = primary.state.checked_table(primary)\n'
         'secondary = primary.state.checked_table(secondary)\n'
         'officer = uint(officer, 16)\n'
         'index = u16(officer << 1)\n'
         'score = primary.word(index)\n'
         'return u16(score + secondary.word(index))'}

DECLARATIONS['recruitment_score_is_better'] = {'signature': 'score: Word, best_score: Word',
 'returns': 'RecruitmentPredicate',
 'flow': 'score = uint(score, 16)\nbest_score = uint(best_score, 16)\nreturn score > best_score'}

DECLARATIONS['assign_live_recruitment_candidate'] = {'signature': 'state: GameState',
 'returns': 'None',
 'flow': 'city = state.current_city()\n'
         'assignments = state.officer_assignments\n'
         'candidate = state.candidate_officer()\n'
         'assignments.set_byte(candidate, low8(city))'}

DECLARATIONS['reward_selected_recruitment_officer'] = {'signature': 'state: GameState',
 'returns': 'None',
 'flow': 'progress = state.officer_progress\n'
         'officer = u16(state.selected_officer() << 1)\n'
         'gain = compute_recruitment_progress_gain(progress.word(officer))\n'
         'progress.set_word(officer, gain)\n'
         'officer = u16(officer >> 1)\n'
         'action = state.officer_action\n'
         'action.set_byte(officer, 1)\n'
         'state.mark_selected_roster_bit14(officer)'}

DECLARATIONS['compute_recruitment_progress_gain'] = {'signature': 'current: Word',
 'returns': 'Word',
 'flow': 'current = uint(current, 16)\n'
         'gain = u16(current + 10)\n'
         'if gain > 999:\n'
         '    gain = u16(999)\n'
         'return gain',
 'slots': {999: ('progress_cap', 0, 65535)}}


# Complete domestic source topology; all admitted operators/literals lower below.

DOMESTIC_SOURCE_FUNCTIONS = ('select_welfare_officer', 'query_welfare_officer', 'plan_welfare_budget', 'select_development_officer', 'query_development_officer', 'domestic_officer_score_is_better', 'plan_development_budget', 'sample_domestic_budget_factor', 'read_domestic_budget_balance', 'calculate_domestic_budget', 'cap_domestic_order_amount', 'submit_domestic_order_amount', 'select_resource_support_city', 'read_resource_support_views', 'query_resource_support_city', 'estimate_resource_support_need', 'read_resource_support_total', 'city_supply_is_sufficient', 'resource_support_total_is_better', 'estimate_city_troop_requirement', 'read_city_assigned_troop_load', 'convert_city_troop_load_to_requirement', 'choose_resource_action', 'read_current_resource_balance', 'decide_city_resource_order', 'submit_city_resource_order')

DECLARATIONS['select_welfare_officer'] = {'signature': 'state: GameState',
 'returns': 'tuple[Word, Word]',
 'flow': 'candidate = query_welfare_officer(state)\nreturn (candidate.score, candidate.officer)'}

DECLARATIONS['query_welfare_officer'] = {'signature': 'state: GameState',
 'returns': 'DomesticOfficer',
 'flow': 'roster = state.economy_roster.cursor()\n'
         'intelligence = state.officer_intelligence\n'
         'education = state.officer_education\n'
         'best_score = u16(0)\n'
         'best_officer = u16(65535)\n'
         'while True:\n'
         '    officer = roster.next_word()\n'
         '    if negative_word(officer):\n'
         '        break\n'
         '    if officer & 16384 != 0:\n'
         '        continue\n'
         '    officer = u16(officer & 255)\n'
         '    score = u16(education.byte(officer))\n'
         '    index = u16(officer << 1)\n'
         '    score = u16(score + intelligence.word(index))\n'
         '    if domestic_officer_score_is_better(score, best_score):\n'
         '        best_score = score\n'
         '        best_officer = officer\n'
         'return DomesticOfficer(best_score, best_officer)'}

DECLARATIONS['plan_welfare_budget'] = {'signature': 'state: GameState',
 'returns': 'None',
 'flow': 'factor = sample_domestic_budget_factor(state, 20)\n'
         'funding = read_domestic_budget_balance(state)\n'
         'budget = calculate_domestic_budget(state, funding.balance, factor)\n'
         'submit_domestic_order_amount(state, budget)'}

DECLARATIONS['select_development_officer'] = {'signature': 'state: GameState',
 'returns': 'tuple[Word, Word]',
 'flow': 'candidate = query_development_officer(state)\nreturn (candidate.score, candidate.officer)'}

DECLARATIONS['query_development_officer'] = {'signature': 'state: GameState',
 'returns': 'DomesticOfficer',
 'flow': 'roster = state.economy_roster.cursor()\n'
         'intelligence = state.officer_intelligence\n'
         'best_score = u16(0)\n'
         'best_officer = u16(65535)\n'
         'while True:\n'
         '    officer = roster.next_word()\n'
         '    if negative_word(officer):\n'
         '        break\n'
         '    if officer & 16384 != 0:\n'
         '        continue\n'
         '    index = u16(officer << 1)\n'
         '    score = intelligence.word(index)\n'
         '    if domestic_officer_score_is_better(score, best_score):\n'
         '        best_score = score\n'
         '        best_officer = officer\n'
         'return DomesticOfficer(best_score, best_officer)'}

DECLARATIONS['domestic_officer_score_is_better'] = {'signature': 'score: Word, best_score: Word',
 'returns': 'DomesticPredicate',
 'flow': 'score = uint(score, 16)\nbest_score = uint(best_score, 16)\nreturn score > best_score'}

DECLARATIONS['plan_development_budget'] = {'signature': 'state: GameState',
 'returns': 'None',
 'flow': 'discarded_factor = sample_domestic_budget_factor(state, 30)\n'
         'funding = read_domestic_budget_balance(state)\n'
         'factor = funding.city_offset\n'
         'budget = calculate_domestic_budget(state, funding.balance, factor)\n'
         'submit_domestic_order_amount(state, budget)'}

DECLARATIONS['sample_domestic_budget_factor'] = {'signature': 'state: GameState, base: Word',
 'returns': 'Word',
 'flow': 'base = uint(base, 16)\n'
         'sample = u32(low16(state.sample_random()))\n'
         'original_sample = sample\n'
         'sample = u32(sample << 2)\n'
         'sample = u32(sample + original_sample)\n'
         'sample = u32(sample << 2)\n'
         'sample = u32(sample + original_sample)\n'
         'sample = swap_words(sample)\n'
         'return u16(low16(sample) + base)'}

DECLARATIONS['read_domestic_budget_balance'] = {'signature': 'state: GameState',
 'returns': 'CityBudgetBalance',
 'flow': 'gold = state.city_gold\n'
         'city = u16(state.current_city() << 2)\n'
         'balance = gold.long(city)\n'
         'return CityBudgetBalance(gold, city, balance)'}

DECLARATIONS['calculate_domestic_budget'] = {'signature': 'state: GameState, balance: Long, factor: Word',
 'returns': 'Long',
 'flow': 'balance = uint(balance, 32)\n'
         'factor = uint(factor, 16)\n'
         'lower_product = u32(low16(balance) * factor)\n'
         'balance = swap_words(balance)\n'
         'balance = u32(low16(balance) * factor)\n'
         'balance = swap_words(balance)\n'
         'balance = u32(balance + lower_product)\n'
         'budget, remainder = state.divide_signed(balance, 100)\n'
         'return cap_domestic_order_amount(budget)'}

DECLARATIONS['cap_domestic_order_amount'] = {'signature': 'budget: Long',
 'returns': 'Long',
 'flow': 'budget = uint(budget, 32)\nif budget > 9999:\n    budget = u32(9999)\nreturn budget',
 'slots': {9999: ('budget_cap', 0, 4294967295)}}

DECLARATIONS['submit_domestic_order_amount'] = {'signature': 'state: GameState, amount: Long',
 'returns': 'None',
 'flow': 'amount = uint(amount, 32)\nstate.set_order_amount(amount)'}

DECLARATIONS['select_resource_support_city'] = {'signature': 'state: GameState',
 'returns': 'tuple[Long, Word]',
 'flow': 'candidate = query_resource_support_city(state)\nreturn (candidate.total, candidate.city)'}

DECLARATIONS['read_resource_support_views'] = {'signature': 'state: GameState',
 'returns': 'ResourceSupportViews',
 'flow': 'force = state.current_force()\n'
         'current_city = state.current_city()\n'
         'troops = state.officer_troops\n'
         'gold = state.city_gold\n'
         'rice = state.city_rice\n'
         'processed = state.city_processed\n'
         'owners = state.city_owners_predecrement.cursor()\n'
         'return ResourceSupportViews(force, current_city, troops, gold, rice, processed, owners)'}

DECLARATIONS['query_resource_support_city'] = {'signature': 'state: GameState',
 'returns': 'ResourceSupportCandidate',
 'flow': 'views = read_resource_support_views(state)\n'
         'minimum = u32(4294967295)\n'
         'selected = u16(65535)\n'
         'processed = views.processed\n'
         'for city in descending_inclusive(40):\n'
         '    if city == 0:\n'
         '        break\n'
         '    owner = views.owners.previous_byte()\n'
         '    if low8(views.force) != owner:\n'
         '        continue\n'
         '    if processed.byte(city) != 0:\n'
         '        continue\n'
         '    if city == views.current_city:\n'
         '        continue\n'
         '    need = estimate_resource_support_need(state, city, views.troops)\n'
         '    processed = need.next_filter\n'
         '    index = u16(city << 2)\n'
         '    if city_supply_is_sufficient(need.required, views.rice.long(index)):\n'
         '        continue\n'
         '    total = read_resource_support_total(views.gold, views.rice, index)\n'
         '    if resource_support_total_is_better(total, minimum):\n'
         '        minimum = total\n'
         '        selected = city\n'
         'return ResourceSupportCandidate(minimum, selected)'}

DECLARATIONS['estimate_resource_support_need'] = {'signature': 'state: GameState, city: Word, troops: Table',
 'returns': 'CitySupplyRequirement',
 'flow': 'requirement = estimate_city_troop_requirement(state, city, troops)\n'
         'return CitySupplyRequirement(requirement, state.officer_assignments)'}

DECLARATIONS['read_resource_support_total'] = {'signature': 'gold: Table, rice: Table, index: Word',
 'returns': 'Long',
 'flow': 'gold = gold.state.checked_table(gold)\n'
         'rice = gold.state.checked_table(rice)\n'
         'index = uint(index, 16)\n'
         'total = gold.long(index)\n'
         'return u32(total + rice.long(index))'}

DECLARATIONS['city_supply_is_sufficient'] = {'signature': 'required: Long, available: Long',
 'returns': 'DomesticPredicate',
 'flow': 'required = uint(required, 32)\navailable = uint(available, 32)\nreturn required <= available'}

DECLARATIONS['resource_support_total_is_better'] = {'signature': 'total: Long, minimum: Long',
 'returns': 'DomesticPredicate',
 'flow': 'total = uint(total, 32)\nminimum = uint(minimum, 32)\nreturn total < minimum'}

DECLARATIONS['estimate_city_troop_requirement'] = {'signature': 'state: GameState, city: Word, troops: Table',
 'returns': 'Long',
 'flow': 'city = uint(city, 16)\n'
         'troops = state.checked_table(troops)\n'
         'total = read_city_assigned_troop_load(state, city, troops)\n'
         'return convert_city_troop_load_to_requirement(total)'}

DECLARATIONS['read_city_assigned_troop_load'] = {'signature': 'state: GameState, city: Word, troops: Table',
 'returns': 'Long',
 'flow': 'city = uint(city, 16)\n'
         'troops = state.checked_table(troops)\n'
         'assignments = state.officer_action_predecrement.cursor()\n'
         'total = u32(0)\n'
         'for officer in descending_inclusive(255):\n'
         '    assignment = u16(assignments.previous_byte() & 63)\n'
         '    if assignment == city:\n'
         '        index = u16(officer << 2)\n'
         '        total = u32(total + troops.long(index))\n'
         '        total = u32(total + 100)\n'
         'return total',
 'slots': {100: ('troop_margin', 0, 4294967295)}}

DECLARATIONS['convert_city_troop_load_to_requirement'] = {'signature': 'total: Long',
 'returns': 'Long',
 'flow': 'total = uint(total, 32)\n'
         'total = divu_retained(total, 10)\n'
         'total = u32(low16(total))\n'
         'saved_total = total\n'
         'total = u32(total << 3)\n'
         'total = u32(total + saved_total)\n'
         'return total'}

DECLARATIONS['choose_resource_action'] = {'signature': 'state: GameState',
 'returns': 'None',
 'flow': 'balance = read_current_resource_balance(state)\n'
         'order = decide_city_resource_order(balance)\n'
         'submit_city_resource_order(state, order)'}

DECLARATIONS['read_current_resource_balance'] = {'signature': 'state: GameState',
 'returns': 'Long',
 'flow': 'gold = state.city_gold\ncity = u16(state.current_city() << 2)\nreturn gold.long(city)'}

DECLARATIONS['decide_city_resource_order'] = {'signature': 'balance: Long',
 'returns': 'CityResourceOrder',
 'flow': 'balance = uint(balance, 32)\n'
         'if balance >= 10000:\n'
         '    return CityResourceOrder.FUNDED\n'
         'return CityResourceOrder.LIMITED',
 'slots': {10000: ('gold_threshold', 0, 4294967295)}}

DECLARATIONS['submit_city_resource_order'] = {'signature': 'state: GameState, order: CityResourceOrder',
 'returns': 'None',
 'flow': 'order = checked_city_resource_order(order)\n'
         'if order is CityResourceOrder.FUNDED:\n'
         '    state.set_command(7)\n'
         'else:\n'
         '    state.set_command(4)'}


def _equipment_source(source):
    """Consume unsigned LONG budget policy, retaining its actual true branch.

    Only its one relation is normalized for the full topology gate. Price,
    available balance, rejection continuation, quote calculations, live views,
    payment, original write slot and complete batch loop remain checked source.
    """
    if type(source) is not str or len(source) > 300000:
        raise CompileError('bounded explicit economy Python text required')
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError) as error:
        raise CompileError('invalid economy Python') from error
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    if any(name not in functions for name in EQUIPMENT_SOURCE_FUNCTIONS):
        raise CompileError('the complete equipment purchase chain is required')
    effects = {name: ast.dump(functions[name], include_attributes=False)
               for name in EQUIPMENT_SOURCE_FUNCTIONS}
    policy = _body(functions['decide_equipment_budget'])
    if (len(policy) != 5 or not isinstance(policy[3], ast.If) or
            len(policy[3].body) != 1 or policy[3].orelse):
        raise CompileError('one explicit equipment budget decision required')
    comparison = policy[3].test
    if (not isinstance(comparison, ast.Compare) or len(comparison.ops) != 1 or
            len(comparison.comparators) != 1):
        raise CompileError('one unsigned LONG budget comparison required')
    branches = {ast.Gt: 'bhi', ast.GtE: 'bcc', ast.Lt: 'bcs',
                ast.LtE: 'bls', ast.Eq: 'beq', ast.NotEq: 'bne'}
    relation = type(comparison.ops[0])
    if relation not in branches:
        raise CompileError('unsupported equipment budget relation')
    category_body = _body(functions['read_officer_equipment_categories'])
    try:
        primary = category_body[5].test.comparators[0].value
        secondary = category_body[5].body[1].test.comparators[0].value
    except (AttributeError, IndexError) as error:
        raise CompileError('complete equipment category thresholds required') from error
    if any(type(value) is not int or not 0 <= value <= 65535 for value in (primary, secondary)):
        raise CompileError('equipment category thresholds must be strict WORDs')
    normalized = deepcopy(tree)
    normalized_policy = next(node for node in normalized.body
                             if isinstance(node, ast.FunctionDef) and node.name == 'decide_equipment_budget')
    _body(normalized_policy)[3].test.ops[0] = ast.Gt()
    return ast.unparse(normalized), effects, dict(
        relation=relation.__name__, price_width=32, available_width=32,
        unsigned_comparison=True, budget_reject_branch=branches[relation],
        primary_threshold=primary, secondary_threshold=secondary,
        source_functions=EQUIPMENT_SOURCE_FUNCTIONS,
        helpers_inlined=True, extra_native_bytes=0, general_Python=False,
    )


def _recruitment_source(source):
    """Consume real unsigned WORD policies, then gate every remaining effect.

    Relation normalization is only for complete fixed-topology admission. The
    actual operators/literals are carried to the existing native comparisons
    and their true/false continuations, never discarded as an AST signature.
    """
    if type(source) is not str or len(source) > 300000:
        raise CompileError('bounded explicit recruitment Python text required')
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError) as error:
        raise CompileError('invalid recruitment Python') from error
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    if any(name not in functions for name in RECRUITMENT_SOURCE_FUNCTIONS):
        raise CompileError('the complete recruitment domain chain is required')
    effects = {name: ast.dump(functions[name], include_attributes=False)
               for name in RECRUITMENT_SOURCE_FUNCTIONS}
    inverse = {ast.Lt: 'bcc', ast.LtE: 'bhi', ast.Gt: 'bls',
               ast.GtE: 'bcs', ast.Eq: 'bne', ast.NotEq: 'beq'}
    direct = {ast.Lt: 'bcs', ast.LtE: 'bls', ast.Gt: 'bhi',
              ast.GtE: 'bcc', ast.Eq: 'beq', ast.NotEq: 'bne'}

    def comparison(node):
        if (not isinstance(node, ast.Compare) or len(node.ops) != 1 or
                len(node.comparators) != 1 or type(node.ops[0]) not in inverse):
            raise CompileError('one declared unsigned WORD comparison required')
        return node

    score_body = _body(functions['recruitment_score_is_better'])
    capacity_body = _body(functions['recruitment_city_has_capacity'])
    candidate_body = _body(functions['decide_foreign_recruitment_candidate'])
    progress_body = _body(functions['compute_recruitment_progress_gain'])
    try:
        score_test = comparison(score_body[2].value)
        capacity_test = comparison(capacity_body[1].value)
        candidate_test = candidate_body[2].test
        if not isinstance(candidate_test, ast.BoolOp) or len(candidate_test.values) != 2:
            raise CompileError('the two original candidate gates are required')
        primary_test = comparison(candidate_test.values[0])
        secondary_test = comparison(candidate_test.values[1])
        values = dict(city_capacity=capacity_test.comparators[0].value,
                      primary_threshold=primary_test.comparators[0].value,
                      secondary_threshold=secondary_test.comparators[0].value,
                      progress_cap=progress_body[2].test.comparators[0].value)
    except (AttributeError, IndexError) as error:
        raise CompileError('complete recruitment policies and compatibility reward required') from error
    if any(type(value) is not int or not 0 <= value <= 65535 for value in values.values()):
        raise CompileError('recruitment thresholds must be strict WORDs')
    contract = dict(values, score_relation=type(score_test.ops[0]).__name__,
                    capacity_relation=type(capacity_test.ops[0]).__name__,
                    primary_relation=type(primary_test.ops[0]).__name__,
                    secondary_relation=type(secondary_test.ops[0]).__name__,
                    score_false_branch=inverse[type(score_test.ops[0])],
                    capacity_false_branch=inverse[type(capacity_test.ops[0])],
                    primary_false_branch=inverse[type(primary_test.ops[0])],
                    secondary_true_branch=direct[type(secondary_test.ops[0])],
                    comparison_width=16, unsigned_comparison=True,
                    source_functions=RECRUITMENT_SOURCE_FUNCTIONS,
                    helpers_inlined=True, extra_native_bytes=0, general_Python=False)
    normalized = deepcopy(tree)
    copied = {node.name: node for node in normalized.body if isinstance(node, ast.FunctionDef)}
    _body(copied['recruitment_score_is_better'])[2].value.ops[0] = ast.Gt()
    _body(copied['recruitment_city_has_capacity'])[1].value.ops[0] = ast.Lt()
    copied_gates = _body(copied['decide_foreign_recruitment_candidate'])[2].test.values
    copied_gates[0].ops[0] = ast.Lt()
    copied_gates[1].ops[0] = ast.Lt()
    return ast.unparse(normalized), effects, contract


def _domestic_source(source):
    """Read genuine resource/selection/cap policy AST and fixed-width literals.

    Only comparison operators are normalized for topology admission. Every
    original relation is retained for branch selection; no new DATA or native
    entry is introduced by the domain helper organization.
    """
    if type(source) is not str or len(source) > 300000:
        raise CompileError('bounded explicit domestic Python text required')
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError) as error:
        raise CompileError('invalid domestic Python') from error
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    if any(name not in functions for name in DOMESTIC_SOURCE_FUNCTIONS):
        raise CompileError('the complete domestic source family is required')
    effects = {name: ast.dump(functions[name], include_attributes=False)
               for name in DOMESTIC_SOURCE_FUNCTIONS}
    inverse = {ast.Lt: 'bcc', ast.LtE: 'bhi', ast.Gt: 'bls',
               ast.GtE: 'bcs', ast.Eq: 'bne', ast.NotEq: 'beq'}
    direct = {ast.Lt: 'bcs', ast.LtE: 'bls', ast.Gt: 'bhi',
              ast.GtE: 'bcc', ast.Eq: 'beq', ast.NotEq: 'bne'}
    policies = (
        ('domestic_officer_score_is_better', 2, 'value', ast.Gt, 'score_false_branch', inverse),
        ('city_supply_is_sufficient', 2, 'value', ast.LtE, 'supply_true_branch', direct),
        ('resource_support_total_is_better', 2, 'value', ast.Lt, 'total_false_branch', inverse),
        ('cap_domestic_order_amount', 1, 'test', ast.Gt, 'budget_false_branch', inverse),
        ('decide_city_resource_order', 1, 'test', ast.GtE, 'resource_false_branch', inverse),
    )
    rules, relations = {}, {}
    normalized = deepcopy(tree)
    copied = {node.name: node for node in normalized.body if isinstance(node, ast.FunctionDef)}
    for name, index, field, canonical, role, branches in policies:
        try:
            test = getattr(_body(functions[name])[index], field)
        except (AttributeError, IndexError) as error:
            raise CompileError('complete domestic policy clauses required') from error
        if (not isinstance(test, ast.Compare) or len(test.ops) != 1 or
                len(test.comparators) != 1 or type(test.ops[0]) not in branches):
            raise CompileError('one declared unsigned domestic comparison required')
        rules[role] = branches[type(test.ops[0])]
        relations[name] = type(test.ops[0]).__name__
        getattr(_body(copied[name])[index], field).ops[0] = canonical()
        if name in ('cap_domestic_order_amount', 'decide_city_resource_order'):
            value = getattr(test.comparators[0], 'value', None)
            if type(value) is not int or not 0 <= value <= 0xFFFFFFFF:
                raise CompileError('domestic policy threshold must be strict LONG')
            rules['budget_cap' if name == 'cap_domestic_order_amount' else 'gold_threshold'] = value
    # The margin belongs to the actual WORD-indexed live troop scan. The same
    # source clause is admitted below, then this value reaches ADDI.L emission.
    scan = _body(functions['read_city_assigned_troop_load'])
    try:
        margin = scan[4].body[1].body[2].value.args[0].right.value
    except (AttributeError, IndexError) as error:
        raise CompileError('complete live troop requirement scan required') from error
    if type(margin) is not int or not 0 <= margin <= 0xFFFFFFFF:
        raise CompileError('troop margin must be strict LONG')
    rules['troop_margin'] = margin
    return ast.unparse(normalized), effects, dict(
        rules, relations=relations, score_width=16, balance_width=32,
        unsigned_comparisons=True, source_functions=DOMESTIC_SOURCE_FUNCTIONS,
        helpers_inlined=True, extra_native_bytes=0, general_Python=False,
    )


def compile_economy(source):
    domestic_normalized, domestic_effects, domestic_contract = _domestic_source(source)
    recruitment_normalized, recruitment_effects, recruitment_contract = _recruitment_source(domestic_normalized)
    normalized, equipment_effects, equipment_contract = _equipment_source(recruitment_normalized)
    records, training_contract = _training_source(normalized)
    records['purchase_roster_equipment']['rules'] = {
        name: equipment_contract[name]
        for name in ('budget_reject_branch', 'primary_threshold', 'secondary_threshold')
    }
    records['purchase_roster_equipment']['effects'] = repr(equipment_effects)
    records['plan_foreign_officer_recruitment']['rules'] = {
        name: recruitment_contract[name] for name in
        ('city_capacity', 'capacity_false_branch', 'primary_threshold',
         'primary_false_branch', 'secondary_threshold', 'secondary_true_branch')
    }
    records['scan_city_officer_candidate']['rules'] = {
        'score_false_branch': recruitment_contract['score_false_branch']
    }
    records['commit_recruitment_candidate']['rules'] = {
        name: recruitment_contract[name] for name in
        ('city_capacity', 'capacity_false_branch', 'progress_cap')
    }
    for name in ('select_welfare_officer', 'select_development_officer'):
        records[name]['rules'] = {'score_false_branch': domestic_contract['score_false_branch']}
    for name in ('plan_welfare_budget', 'plan_development_budget'):
        records[name]['rules'] = {key: domestic_contract[key] for key in ('budget_cap', 'budget_false_branch')}
    records['select_resource_support_city']['rules'] = {
        key: domestic_contract[key] for key in ('supply_true_branch', 'total_false_branch')
    }
    records['estimate_city_troop_requirement']['rules'] = {'troop_margin': domestic_contract['troop_margin']}
    records['choose_resource_action']['rules'] = {
        key: domestic_contract[key] for key in ('gold_threshold', 'resource_false_branch')
    }
    domestic_dependencies = {
        'select_welfare_officer': ('select_welfare_officer', 'query_welfare_officer', 'domestic_officer_score_is_better'),
        'select_development_officer': ('select_development_officer', 'query_development_officer', 'domestic_officer_score_is_better'),
        'plan_welfare_budget': ('plan_welfare_budget', 'sample_domestic_budget_factor', 'read_domestic_budget_balance',
                               'calculate_domestic_budget', 'cap_domestic_order_amount', 'submit_domestic_order_amount'),
        'plan_development_budget': ('plan_development_budget', 'sample_domestic_budget_factor', 'read_domestic_budget_balance',
                                   'calculate_domestic_budget', 'cap_domestic_order_amount', 'submit_domestic_order_amount'),
        'select_resource_support_city': ('select_resource_support_city', 'read_resource_support_views', 'query_resource_support_city',
                                         'estimate_resource_support_need', 'read_resource_support_total',
                                         'city_supply_is_sufficient', 'resource_support_total_is_better'),
        'estimate_city_troop_requirement': ('estimate_city_troop_requirement', 'read_city_assigned_troop_load', 'convert_city_troop_load_to_requirement'),
        'choose_resource_action': ('choose_resource_action', 'read_current_resource_balance', 'decide_city_resource_order', 'submit_city_resource_order'),
    }
    for name, helpers in domestic_dependencies.items():
        records[name]['effects'] = repr({helper: domestic_effects[helper] for helper in helpers})
    dependencies = {
        'plan_foreign_officer_recruitment': (
            'plan_foreign_officer_recruitment', 'read_recruitment_city_roster_count',
            'recruitment_city_has_capacity', 'decide_foreign_recruitment_candidate',
            'decide_foreign_recruitment_lottery', 'submit_foreign_recruitment_order'),
        'select_foreign_neighbor_officer': (
            'select_foreign_neighbor_officer', 'read_foreign_recruitment_views',
            'query_foreign_recruitment_candidate'),
        'scan_city_officer_candidate': (
            'scan_city_officer_candidate', 'query_recruitment_city_candidate',
            'read_recruitment_officer_score', 'recruitment_score_is_better'),
        'commit_recruitment_candidate': (
            'commit_recruitment_candidate', 'read_recruitment_city_roster_count',
            'recruitment_city_has_capacity', 'assign_live_recruitment_candidate',
            'reward_selected_recruitment_officer', 'compute_recruitment_progress_gain'),
    }
    for name, helpers in dependencies.items():
        records[name]['effects'] = repr({helper: recruitment_effects[helper] for helper in helpers})
    result = lower_declared(records,ECONOMY_BINDINGS,LOWERERS)
    result['training_domain_contract'] = training_contract
    result['equipment_domain_contract'] = equipment_contract
    result['recruitment_domain_contract'] = recruitment_contract
    result['domestic_domain_contract'] = domestic_contract
    return result
