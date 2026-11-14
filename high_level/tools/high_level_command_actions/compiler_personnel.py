"""Draft restricted personnel semantic AST admission and ordinary target emission.

Business rules remain separate. Generation reads explicit source text only.
Not an arbitrary Python compiler or an independent behavior acceptance.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import PERSONNEL_BINDINGS

APPROVED = {'business_reuse': {'add_progress_be',
                    'build_roster',
                    'choose_city_head',
                    'commit_mutual_relationship',
                    'debit_city_gold',
                    'education_factor',
                    'prepare_message',
                    'split_progress',
                    'step_random'},
 'contexts_personnel': {'RecruitmentScore'},
 'domain': {'GameState',
            'Long',
            'Word',
            'checked_state',
            'descending_inclusive',
            'divu_retained',
            'high16',
            'low16',
            'low8',
            'negative_word',
            'replace_byte',
            'replace_word',
            's16',
            's8',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'}}

DECLARATIONS = {'execute_officer_loyalty_reward': {'signature': 'state: GameState',
                                    'returns': 'None',
                                    'flow': 'checked_state(state)\n'
                                            'debit_city_gold(state)\n'
                                            "teacher = state.scalar('selected_teacher')\n"
                                            "if teacher == state.scalar('selected_officer'):\n"
                                            '    teacher_loyalty = 100\n'
                                            "elif teacher == state.scalar('alternate_teacher'):\n"
                                            '    teacher_loyalty = 100\n'
                                            'else:\n'
                                            '    teacher_loyalty = '
                                            'u16(s8(state.officer_loyalty.byte(teacher)))\n'
                                            "officer = state.scalar('selected_officer')\n"
                                            'pupil_loyalty = '
                                            'u16(s8(state.officer_loyalty.byte(officer)))\n'
                                            'teaching = education_factor(state, teacher_loyalty, '
                                            'pupil_loyalty)\n'
                                            "reward = u32(state.scalar('action_amount') << 1)\n"
                                            "slot = u16(state.scalar('selected_officer') << 1)\n"
                                            'reward = u32(reward + '
                                            'state.officer_strength.word(slot) * 10)\n'
                                            'reward = u32(reward + '
                                            'state.officer_progress.word(slot) * 5)\n'
                                            "officer = state.scalar('selected_officer')\n"
                                            'disposition = '
                                            'state.officer_disposition.byte(officer)\n'
                                            'if disposition <= 30:\n'
                                            '    reward = replace_word(reward, low16(reward) >> '
                                            '1)\n'
                                            "seed_word = state.scalar('random_seed_high')\n"
                                            'weighting = swap_words(u32(seed_word * 3))\n'
                                            'weighting = replace_word(weighting, '
                                            'u16(low16(weighting) + teaching))\n'
                                            'weighting = u32(low16(weighting) * disposition)\n'
                                            'low_product = u32(low16(reward) * low16(weighting))\n'
                                            'high_product = swap_words(u32(high16(reward) * '
                                            'low16(weighting)))\n'
                                            'reward = u32(high_product + low_product)\n'
                                            'reward = low16(divu_retained(reward, 10000))\n'
                                            'reward = divu_retained(reward, 60)\n'
                                            "state.set_scalar('result_pair_high', 0)\n"
                                            "state.set_scalar('result_pair_low', low16(reward))\n"
                                            "officer = state.scalar('selected_officer')\n"
                                            'loyalty = '
                                            'u16(s8(state.officer_loyalty.byte(officer)))\n'
                                            'loyalty = u16(loyalty + low16(reward))\n'
                                            'if loyalty > 100:\n'
                                            '    excess = u16(loyalty - 100)\n'
                                            "    remaining = state.scalar('result_pair_low')\n"
                                            "    state.set_scalar('result_pair_low', u16(remaining "
                                            '- excess))\n'
                                            '    loyalty = 100\n'
                                            'state.officer_loyalty.set_byte(officer, '
                                            'low8(loyalty))\n'
                                            "teacher = state.scalar('selected_teacher')\n"
                                            "if teacher == state.scalar('selected_officer'):\n"
                                            "    teacher = state.scalar('alternate_teacher')\n"
                                            'disposition = '
                                            'u8(state.officer_disposition.byte(teacher) + 1)\n'
                                            'if disposition > 100:\n'
                                            '    disposition = 100\n'
                                            'state.officer_disposition.set_byte(teacher, '
                                            'disposition)\n'
                                            'teacher_slot = u16(teacher << 1)\n'
                                            'reward = replace_word(reward, low16(reward) >> 1)\n'
                                            'progress = u16(low16(reward) + '
                                            'state.officer_progress.word(teacher_slot))\n'
                                            'if progress > 999:\n'
                                            '    progress = 999\n'
                                            'state.officer_progress.set_word(teacher_slot, '
                                            'progress)\n'
                                            "state.officer_actions.set_byte(state.scalar('selected_officer'), "
                                            '1)\n'
                                            "force = state.scalar('current_force')\n"
                                            "if force == state.scalar('visible_force_first') or "
                                            "force == state.scalar('visible_force_second') or "
                                            "force == state.scalar('visible_force_third'):\n"
                                            "    state.set_scalar('command_mode', 22)\n"
                                            "    if state.scalar('result_pair_low') != 0:\n"
                                            '        message = 167\n'
                                            '    else:\n'
                                            '        message = 168\n'
                                            "    state.set_scalar('command_message', message)\n"
                                            "    state.set_scalar('command_sound', "
                                            "state.scalar('command_audio'))\n"
                                            "    state.set_scalar('command_sound', "
                                            "state.scalar('command_audio'))\n"
                                            "    state.set_scalar('ui_state', 40)\n"
                                            "    state.set_scalar('command_actor', "
                                            "state.scalar('selected_officer'))\n"
                                            'return None'},
 'execute_mutual_officer_relationship_reward': {'signature': 'state: GameState',
                                                'returns': 'None',
                                                'flow': 'checked_state(state)\n'
                                                        'officer = '
                                                        "state.scalar('selected_officer')\n"
                                                        'character = '
                                                        'state.officer_status.byte(officer) & 7\n'
                                                        'bias = '
                                                        'u16(s8(state.relationship_character_bias.byte(character)))\n'
                                                        'seed_word = '
                                                        "state.scalar('random_seed_high')\n"
                                                        'weighted = swap_words(u32(seed_word * '
                                                        'u16(character + 2)))\n'
                                                        'weighted = replace_word(weighted, '
                                                        'u16(low16(weighted) + bias))\n'
                                                        'weighted = u32(low16(weighted) * '
                                                        'state.officer_strength.word(u16(officer '
                                                        '<< 1)))\n'
                                                        "force = state.scalar('current_force')\n"
                                                        'head = state.force_heads.word(u16(force '
                                                        '<< 1))\n'
                                                        'disposition = '
                                                        'state.officer_disposition.byte(head)\n'
                                                        'denominator = u16(120 - disposition)\n'
                                                        'weighted = divu_retained(weighted, '
                                                        'denominator)\n'
                                                        'if low16(weighted) >= 10:\n'
                                                        '    commit_mutual_relationship(state)\n'
                                                        "    state.set_scalar('command_message', "
                                                        '38)\n'
                                                        "    state.set_scalar('command_actor', "
                                                        "state.scalar('selected_officer'))\n"
                                                        '    step_random(state)\n'
                                                        '    reward = '
                                                        "swap_words(u32(state.scalar('random_seed_high') "
                                                        '* 6))\n'
                                                        '    reward = replace_word(reward, '
                                                        'u16(low16(reward) + 5))\n'
                                                        '    force = '
                                                        "state.scalar('current_force')\n"
                                                        '    head = '
                                                        'state.force_heads.word(u16(force << 1))\n'
                                                        '    slot = u16(head << 1)\n'
                                                        '    updated = u16(low16(reward) + '
                                                        'state.officer_progress.word(slot))\n'
                                                        '    if updated > 999:\n'
                                                        '        updated = 999\n'
                                                        '    state.officer_progress.set_word(slot, '
                                                        'updated)\n'
                                                        '    step_random(state)\n'
                                                        '    reward = '
                                                        "swap_words(u32(state.scalar('random_seed_high') "
                                                        '* 6))\n'
                                                        '    reward = replace_word(reward, '
                                                        'u16(low16(reward) + 10))\n'
                                                        '    slot = '
                                                        "u16(state.scalar('selected_officer') << "
                                                        '1)\n'
                                                        '    updated = u16(low16(reward) + '
                                                        'state.officer_progress.word(slot))\n'
                                                        '    if updated > 999:\n'
                                                        '        updated = 999\n'
                                                        '    state.officer_progress.set_word(slot, '
                                                        'updated)\n'
                                                        'else:\n'
                                                        "    state.set_scalar('command_message', "
                                                        '40)\n'
                                                        '    step_random(state)\n'
                                                        '    reward = '
                                                        "swap_words(u32(state.scalar('random_seed_high') "
                                                        '* 3))\n'
                                                        '    reward = replace_word(reward, '
                                                        'u16(low16(reward) + 1))\n'
                                                        '    force = '
                                                        "state.scalar('current_force')\n"
                                                        '    head = '
                                                        'state.force_heads.word(u16(force << 1))\n'
                                                        '    slot = u16(head << 1)\n'
                                                        '    updated = u16(low16(reward) + '
                                                        'state.officer_progress.word(slot))\n'
                                                        '    if updated > 999:\n'
                                                        '        updated = 999\n'
                                                        '    state.officer_progress.set_word(slot, '
                                                        'updated)\n'
                                                        '    step_random(state)\n'
                                                        '    reward = '
                                                        "swap_words(u32(state.scalar('random_seed_high') "
                                                        '* 3))\n'
                                                        '    reward = replace_word(reward, '
                                                        'u16(low16(reward) + 1))\n'
                                                        '    step_random(state)\n'
                                                        '    reduction = '
                                                        "low16(swap_words(u32(state.scalar('random_seed_high') "
                                                        '* 3)))\n'
                                                        '    officer = '
                                                        "state.scalar('selected_officer')\n"
                                                        '    previous = '
                                                        'state.officer_disposition.byte(officer)\n'
                                                        '    '
                                                        'state.officer_disposition.set_byte(officer, '
                                                        'u8(previous - low8(reduction)))\n'
                                                        '    if previous < low8(reduction):\n'
                                                        '        '
                                                        'state.officer_disposition.set_byte(officer, '
                                                        '0)\n'
                                                        '    slot = u16(officer << 1)\n'
                                                        '    updated = u16(low16(reward) + '
                                                        'state.officer_progress.word(slot))\n'
                                                        '    if updated > 999:\n'
                                                        '        updated = 999\n'
                                                        '    state.officer_progress.set_word(slot, '
                                                        'updated)\n'
                                                        "force = state.scalar('current_force')\n"
                                                        'if force == '
                                                        "state.scalar('visible_force_first') or "
                                                        'force == '
                                                        "state.scalar('visible_force_second') or "
                                                        'force == '
                                                        "state.scalar('visible_force_third'):\n"
                                                        "    state.set_scalar('command_mode', 12)\n"
                                                        "    state.set_scalar('command_sound', "
                                                        '520)\n'
                                                        "    state.set_scalar('ui_state', 40)\n"
                                                        "    state.set_scalar('command_actor', "
                                                        "state.scalar('selected_officer'))\n"
                                                        '    prepare_message(state, 37)\n'
                                                        "state.officer_actions.set_byte(state.scalar('selected_officer'), "
                                                        '1)\n'
                                                        "state.set_scalar('command_timer', 120)\n"
                                                        'return None'},
 'execute_officer_policy_outcome': {'signature': 'state: GameState',
                                    'returns': 'None',
                                    'flow': 'checked_state(state)\n'
                                            "state.set_scalar('result_pair', 0)\n"
                                            "target = state.scalar('policy_target')\n"
                                            'city = u16(replace_byte(target, '
                                            'state.officer_city_assignment.byte(target)))\n'
                                            'owner = u16(replace_byte(city, '
                                            'state.city_owner_bytes.byte(city)))\n'
                                            'head = state.force_heads.word(u16(owner << 1))\n'
                                            'succeeded = False\n'
                                            "if head != state.scalar('policy_target'):\n"
                                            "    target = state.scalar('policy_target')\n"
                                            '    loyalty_byte = '
                                            'state.officer_loyalty.byte(target)\n'
                                            '    if loyalty_byte != 0:\n'
                                            '        loyalty = u16(s8(loyalty_byte))\n'
                                            '        distance = u16(loyalty - 50)\n'
                                            '        if loyalty < 50:\n'
                                            '            distance = u16(-distance)\n'
                                            '        window = u16(60 - distance)\n'
                                            "        officer = state.scalar('selected_officer')\n"
                                            '        character = '
                                            'state.officer_status.byte(officer) & 7\n'
                                            '        bias = '
                                            'state.policy_character_bias.byte(character)\n'
                                            '        random_bias = '
                                            "swap_words(u32(state.scalar('random_seed_high') * "
                                            '20))\n'
                                            '        random_bias = replace_word(random_bias, '
                                            'u16(low16(random_bias) + bias))\n'
                                            '        strength = '
                                            'state.officer_strength.word(u16(officer << 1))\n'
                                            '        strength = u16(strength + '
                                            'low16(random_bias))\n'
                                            "        target = state.scalar('policy_target')\n"
                                            '        character = state.officer_status.byte(target) '
                                            '& 7\n'
                                            '        random_bias = replace_byte(random_bias, '
                                            'state.target_policy_bias.byte(character))\n'
                                            '        opposition = u16(low16(random_bias) + '
                                            'state.officer_strength.word(u16(target << 1)))\n'
                                            '        difference = u16(strength - opposition)\n'
                                            '        if strength >= opposition:\n'
                                            '            numerator = u32(s16(window) * '
                                            's16(difference))\n'
                                            '            selector = '
                                            "u16(state.scalar('policy_selector') << 1)\n"
                                            '            reward = divu_retained(numerator, '
                                            'state.policy_divisors.word(selector))\n'
                                            '            if low16(reward) != 0:\n'
                                            '                reward_word = low16(reward)\n'
                                            '                if reward_word > 40:\n'
                                            '                    reward_word = 40\n'
                                            "                state.set_scalar('result_pair_high', "
                                            '0)\n'
                                            "                state.set_scalar('result_pair_low', "
                                            'reward_word)\n'
                                            '                target = '
                                            "state.scalar('policy_target')\n"
                                            '                previous = '
                                            'state.officer_loyalty.byte(target)\n'
                                            '                '
                                            'state.officer_loyalty.set_byte(target, u8(previous - '
                                            'low8(reward_word)))\n'
                                            '                if previous < low8(reward_word):\n'
                                            '                    '
                                            'state.officer_loyalty.set_byte(target, 0)\n'
                                            '                add_progress_be(state, reward_word)\n'
                                            "                state.set_scalar('command_target', "
                                            "state.scalar('policy_target'))\n"
                                            "                state.set_scalar('command_message', "
                                            '57)\n'
                                            '                succeeded = True\n'
                                            'if not succeeded:\n'
                                            '    '
                                            'reduce_selected_officer_disposition_randomly(state)\n'
                                            '    '
                                            'reduce_chosen_force_head_disposition_randomly(state)\n'
                                            '    credit_selected_officer_policy_progress(state)\n'
                                            "    state.set_scalar('command_message', 58)\n"
                                            "force = state.scalar('current_force')\n"
                                            "if force == state.scalar('visible_force_first') or "
                                            "force == state.scalar('visible_force_second') or "
                                            "force == state.scalar('visible_force_third'):\n"
                                            "    state.set_scalar('command_audio', 520)\n"
                                            "    state.set_scalar('ui_state', 40)\n"
                                            "    state.set_scalar('command_timer', 120)\n"
                                            "    state.set_scalar('command_sound', 520)\n"
                                            "    state.set_scalar('command_actor', "
                                            "state.scalar('selected_officer'))\n"
                                            '    prepare_message(state, 9)\n'
                                            'return None'},
 'reduce_selected_officer_disposition_randomly': {'signature': 'state: GameState',
                                                  'returns': 'Word',
                                                  'flow': 'checked_state(state)\n'
                                                          'reduction = '
                                                          'low16(swap_words(u32(low16(step_random(state)) '
                                                          '<< 2)))\n'
                                                          'officer = '
                                                          "state.scalar('selected_officer')\n"
                                                          'previous = '
                                                          'state.officer_disposition.byte(officer)\n'
                                                          'state.officer_disposition.set_byte(officer, '
                                                          'u8(previous - low8(reduction)))\n'
                                                          'if previous < low8(reduction):\n'
                                                          '    '
                                                          'state.officer_disposition.set_byte(officer, '
                                                          '0)\n'
                                                          'return reduction'},
 'reduce_chosen_force_head_disposition_randomly': {'signature': 'state: GameState',
                                                   'returns': 'Word',
                                                   'flow': 'checked_state(state)\n'
                                                           'reduction = '
                                                           'low16(swap_words(u32(low16(step_random(state)) '
                                                           '* 3)))\n'
                                                           "city = state.scalar('chosen_city')\n"
                                                           'owner = u16(replace_byte(city, '
                                                           'state.city_owner_bytes.byte(city))) & '
                                                           '15\n'
                                                           'head = '
                                                           'state.force_heads.word(u16(owner << '
                                                           '1))\n'
                                                           'previous = '
                                                           'state.officer_disposition.byte(head)\n'
                                                           'state.officer_disposition.set_byte(head, '
                                                           'u8(previous - low8(reduction)))\n'
                                                           'if previous < low8(reduction):\n'
                                                           '    '
                                                           'state.officer_disposition.set_byte(head, '
                                                           '0)\n'
                                                           'return reduction'},
 'credit_selected_officer_policy_progress': {'signature': 'state: GameState',
                                             'returns': 'Word',
                                             'flow': 'checked_state(state)\n'
                                                     'step_random(state)\n'
                                                     'gain = '
                                                     "low16(swap_words(u32(state.scalar('random_seed_high') "
                                                     '* 3)))\n'
                                                     'gain = u16(gain + 1)\n'
                                                     "slot = u16(state.scalar('selected_officer') "
                                                     '<< 1)\n'
                                                     'previous = '
                                                     'state.officer_progress.word(slot)\n'
                                                     'state.officer_progress.set_word(slot, '
                                                     'u16(previous + gain))\n'
                                                     'if state.officer_progress.word(slot) > 999:\n'
                                                     '    state.officer_progress.set_word(slot, '
                                                     '999)\n'
                                                     'return gain'},
 'execute_officer_recruitment_outcome': {'signature': 'state: GameState',
                                         'returns': 'None',
                                         'flow': 'checked_state(state)\n'
                                                 'score = '
                                                 'bucket_recruitment_score(score_selected_officer_recruitment(state))\n'
                                                 'probability = '
                                                 'draw_recruitment_probability(state)\n'
                                                 'if probability >= score.probability_threshold:\n'
                                                 "    state.set_scalar('command_message', 58)\n"
                                                 '    '
                                                 'apply_recruited_officer_roster_transition(state, '
                                                 'score.score)\n'
                                                 "    state.set_scalar('command_timer', 120)\n"
                                                 "    state.set_scalar('ui_state', 31)\n"
                                                 'else:\n'
                                                 "    state.set_scalar('command_message', 60)\n"
                                                 '    split_progress(state, score.score)\n'
                                                 '    '
                                                 'apply_recruitment_city_resource_losses(state, '
                                                 'score.resource_bucket)\n'
                                                 "    state.set_scalar('command_mode', 3)\n"
                                                 "    state.set_scalar('ui_state', 40)\n"
                                                 "state.set_scalar('command_sound', 520)\n"
                                                 "state.set_scalar('command_actor', "
                                                 "state.scalar('selected_officer'))\n"
                                                 'prepare_message(state, 9)\n'
                                                 "state.set_scalar('command_timer', 120)\n"
                                                 'return None'},
 'score_selected_officer_recruitment': {'signature': 'state: GameState',
                                        'returns': 'Long',
                                        'flow': 'checked_state(state)\n'
                                                "slot = u16(state.scalar('selected_officer') << "
                                                '1)\n'
                                                'score = '
                                                'divu_retained(state.officer_ability.word(slot), '
                                                '10)\n'
                                                'score = replace_word(score, u16(low16(score) + '
                                                'state.officer_strength.word(slot)))\n'
                                                'sample = step_random(state)\n'
                                                "selector = u16(state.scalar('policy_selector') << "
                                                '2)\n'
                                                'factor = '
                                                'state.recruitment_score_parameters.word(selector)\n'
                                                'weighted = swap_words(u32(low16(sample) * '
                                                'factor))\n'
                                                'weighted = replace_word(weighted, '
                                                'u16(low16(weighted) + '
                                                'state.recruitment_score_parameters.word(selector, '
                                                '2)))\n'
                                                'score = replace_word(score, u16(low16(score) + '
                                                'low16(weighted)))\n'
                                                "city = state.scalar('selected_city')\n"
                                                'head = state.city_recruitment_heads.word(u16(city '
                                                '<< 1))\n'
                                                'opposition = state.officer_strength.word(u16(head '
                                                '<< 1))\n'
                                                'return replace_word(score, u16(low16(score) - '
                                                'opposition))'},
 'bucket_recruitment_score': {'signature': 'score: Long',
                              'returns': 'RecruitmentScore',
                              'flow': 'uint(score, 32)\n'
                                      'threshold = 0\n'
                                      'bucket = 0\n'
                                      'if low16(score) == 0 or negative_word(low16(score)):\n'
                                      '    return RecruitmentScore(score, threshold, bucket)\n'
                                      'threshold = 10\n'
                                      'bucket = 1\n'
                                      'if low16(score) > 50:\n'
                                      '    threshold = 30\n'
                                      '    bucket = 2\n'
                                      '    if low16(score) > 100:\n'
                                      '        threshold = 50\n'
                                      '        bucket = 3\n'
                                      '        if low16(score) > 150:\n'
                                      '            threshold = 60\n'
                                      '            bucket = 4\n'
                                      '            if low16(score) > 200:\n'
                                      '                threshold = 70\n'
                                      '                bucket = 5\n'
                                      '                if low16(score) > 250:\n'
                                      '                    threshold = 80\n'
                                      '                    bucket = 6\n'
                                      '                    if low16(score) > 300:\n'
                                      '                        threshold = 80\n'
                                      '                        bucket = 7\n'
                                      '                        if low16(score) > 350:\n'
                                      '                            threshold = 85\n'
                                      '                            bucket = 8\n'
                                      '                            score = replace_word(score, '
                                      '351)\n'
                                      'return RecruitmentScore(score, threshold, bucket)'},
 'apply_recruited_officer_roster_transition': {'signature': 'state: GameState, score: Long',
                                               'returns': 'None',
                                               'flow': 'checked_state(state)\n'
                                                       'uint(score, 32)\n'
                                                       'officer = '
                                                       "state.scalar('selected_officer')\n"
                                                       'heads = state.force_heads.cursor()\n'
                                                       'is_head = False\n'
                                                       'for _ in descending_inclusive(21):\n'
                                                       '    if heads.next_word() == officer:\n'
                                                       '        is_head = True\n'
                                                       '        break\n'
                                                       'if is_head:\n'
                                                       '    if not negative_word(low16(score)):\n'
                                                       '        gain = divu_retained(low16(score), '
                                                       '10)\n'
                                                       '        slot = '
                                                       "u16(state.scalar('selected_officer') << "
                                                       '1)\n'
                                                       '        progress = '
                                                       'u16(state.officer_ability.word(slot) + '
                                                       'low16(gain))\n'
                                                       '        if progress > 999:\n'
                                                       '            progress = 999\n'
                                                       '        '
                                                       'state.officer_ability.set_word(slot, '
                                                       'progress)\n'
                                                       '    return None\n'
                                                       'slot = '
                                                       "u16(state.scalar('selected_officer') << "
                                                       '1)\n'
                                                       'resistance = '
                                                       'u16(state.officer_resolve.word(slot) >> '
                                                       '1)\n'
                                                       'if draw_recruitment_probability(state) < '
                                                       'resistance:\n'
                                                       '    if not negative_word(low16(score)):\n'
                                                       '        gain = divu_retained(low16(score), '
                                                       '10)\n'
                                                       '        slot = '
                                                       "u16(state.scalar('selected_officer') << "
                                                       '1)\n'
                                                       '        progress = '
                                                       'u16(state.officer_ability.word(slot) + '
                                                       'low16(gain))\n'
                                                       '        if progress > 999:\n'
                                                       '            progress = 999\n'
                                                       '        '
                                                       'state.officer_ability.set_word(slot, '
                                                       'progress)\n'
                                                       '    return None\n'
                                                       "city = state.scalar('selected_city')\n"
                                                       "state.set_scalar('selected_teacher', "
                                                       '65535)\n'
                                                       'size = build_roster(state, city)\n'
                                                       'if size < 10:\n'
                                                       '    officer = '
                                                       "state.scalar('selected_officer')\n"
                                                       '    loyalty = '
                                                       'state.officer_loyalty.byte(officer)\n'
                                                       '    resistance = u16(100 - loyalty)\n'
                                                       "    city = state.scalar('selected_city')\n"
                                                       '    head = '
                                                       'state.city_recruitment_heads.word(u16(city '
                                                       '<< 1))\n'
                                                       '    resistance = u16(resistance + '
                                                       'state.officer_disposition.byte(head))\n'
                                                       '    if resistance >= 100:\n'
                                                       '        return None\n'
                                                       '    if draw_recruitment_probability(state) '
                                                       '< resistance:\n'
                                                       '        return None\n'
                                                       "state.set_scalar('command_message', 93)\n"
                                                       'officer = '
                                                       "state.scalar('selected_officer')\n"
                                                       'state.officer_city_assignment.set_byte(officer, '
                                                       '255)\n'
                                                       "city = state.scalar('chosen_city')\n"
                                                       'officer = '
                                                       "state.scalar('selected_officer')\n"
                                                       'if '
                                                       'state.city_recruitment_heads.word(u16(city '
                                                       '<< 1)) == officer:\n'
                                                       "    city = state.scalar('chosen_city')\n"
                                                       "    state.set_scalar('selected_teacher', "
                                                       '65535)\n'
                                                       '    build_roster(state, city)\n'
                                                       '    choose_city_head(state, '
                                                       "state.scalar('chosen_city'))\n"
                                                       'return None'},
 'apply_recruitment_city_resource_losses': {'signature': 'state: GameState, bucket: Word',
                                            'returns': 'None',
                                            'flow': 'checked_state(state)\n'
                                                    'uint(bucket, 16)\n'
                                                    'if bucket != 0:\n'
                                                    '    city_offset = '
                                                    "u16(u16(state.scalar('selected_city') - 1) << "
                                                    '2)\n'
                                                    '    reduce_recruitment_city_food(state, '
                                                    'city_offset, bucket)\n'
                                                    '    reduce_recruitment_city_gold(state, '
                                                    'city_offset, bucket)\n'
                                                    '    '
                                                    'reduce_recruitment_city_state_parameter(state, '
                                                    'city_offset, bucket)\n'
                                                    'return None'},
 'reduce_recruitment_city_food': {'signature': 'state: GameState, city_offset: Word, bucket: Word',
                                  'returns': 'Long',
                                  'flow': 'checked_state(state)\n'
                                          'uint(city_offset, 16)\n'
                                          'uint(bucket, 16)\n'
                                          'slot = u16(bucket << 2)\n'
                                          'factor = state.recruitment_food_parameters.word(slot)\n'
                                          'rate = swap_words(u32(low16(step_random(state)) * '
                                          'factor))\n'
                                          'rate = replace_word(rate, u16(low16(rate) + '
                                          'state.recruitment_food_parameters.word(slot, 2)))\n'
                                          'previous = '
                                          'state.recruitment_city_food.long(city_offset)\n'
                                          'quotient = divu_retained(previous, 100)\n'
                                          'loss = u32(low16(quotient) * low16(rate))\n'
                                          'live = state.recruitment_city_food.long(city_offset)\n'
                                          'state.recruitment_city_food.set_long(city_offset, '
                                          'u32(live - loss))\n'
                                          'return loss'},
 'reduce_recruitment_city_gold': {'signature': 'state: GameState, city_offset: Word, bucket: Word',
                                  'returns': 'Long',
                                  'flow': 'checked_state(state)\n'
                                          'uint(city_offset, 16)\n'
                                          'uint(bucket, 16)\n'
                                          'slot = u16(bucket << 2)\n'
                                          'factor = state.recruitment_gold_parameters.word(slot)\n'
                                          'rate = swap_words(u32(low16(step_random(state)) * '
                                          'factor))\n'
                                          'rate = replace_word(rate, u16(low16(rate) + '
                                          'state.recruitment_gold_parameters.word(slot, 2)))\n'
                                          'previous = '
                                          'state.recruitment_city_gold.long(city_offset)\n'
                                          'quotient = divu_retained(previous, 100)\n'
                                          'loss = u32(low16(quotient) * low16(rate))\n'
                                          'live = state.recruitment_city_gold.long(city_offset)\n'
                                          'state.recruitment_city_gold.set_long(city_offset, '
                                          'u32(live - loss))\n'
                                          'return loss'},
 'reduce_recruitment_city_state_parameter': {'signature': 'state: GameState, city_offset: Word, '
                                                          'bucket: Word',
                                             'returns': 'Long',
                                             'flow': 'checked_state(state)\n'
                                                     'uint(city_offset, 16)\n'
                                                     'uint(bucket, 16)\n'
                                                     'slot = u16(bucket << 2)\n'
                                                     'factor = '
                                                     'state.recruitment_state_parameters.word(slot)\n'
                                                     'rate = '
                                                     'swap_words(u32(low16(step_random(state)) * '
                                                     'factor))\n'
                                                     'rate = replace_word(rate, u16(low16(rate) + '
                                                     'state.recruitment_state_parameters.word(slot, '
                                                     '2)))\n'
                                                     'previous = '
                                                     'state.recruitment_city_state.long(city_offset)\n'
                                                     'product = u32(low16(previous) * '
                                                     'low16(rate))\n'
                                                     'loss = low16(divu_retained(product, 100))\n'
                                                     'live = '
                                                     'state.recruitment_city_state.long(city_offset)\n'
                                                     'state.recruitment_city_state.set_long(city_offset, '
                                                     'u32(live - loss))\n'
                                                     'return loss'},
 'draw_recruitment_probability': {'signature': 'state: GameState',
                                  'returns': 'Word',
                                  'flow': 'checked_state(state)\n'
                                          'sample = low16(step_random(state))\n'
                                          'scaled = u32(sample * 3)\n'
                                          'scaled = u32((scaled << 3) + sample)\n'
                                          'scaled = u32(scaled << 2)\n'
                                          'return low16(swap_words(scaled))'}}

def _lower_execute_officer_loyalty_reward(e,rules):
    e.label('action_pc_00e592')
    e.ins('bsr.w','action_pc_00e70a',4)
    e.label('action_pc_00e596')
    e.ins('lea.l','0xc300:w,%a0',4)
    e.label('action_pc_00e59a')
    e.ins('move.w','0xf630:w,%d0',4)
    e.label('action_pc_00e59e')
    e.ins('cmp.w','0xf3a6:w,%d0',4)
    e.label('action_pc_00e5a2')
    e.ins('beq.b','action_pc_00e5b4',2)
    e.label('action_pc_00e5a4')
    e.ins('cmp.w','0xf634:w,%d0',4)
    e.label('action_pc_00e5a8')
    e.ins('beq.b','action_pc_00e5b4',2)
    e.label('action_pc_00e5aa')
    e.ins('move.b','(%a0, %d0.w),%d0',4)
    e.label('action_pc_00e5ae')
    e.ins('ext.w','%d0',2)
    e.label('action_pc_00e5b0')
    e.ins('bra.w','action_pc_00e5b8',4)
    e.label('action_pc_00e5b4')
    e.ins('move.w','#0x64,%d0',4)
    e.label('action_pc_00e5b8')
    e.ins('move.w','0xf3a6:w,%d1',4)
    e.label('action_pc_00e5bc')
    e.ins('move.b','(%a0, %d1.w),%d1',4)
    e.label('action_pc_00e5c0')
    e.ins('ext.w','%d1',2)
    e.label('action_pc_00e5c2')
    e.ins('bsr.w','action_pc_00e71e',4)
    e.label('action_pc_00e5c6')
    e.ins('move.l','0xf39e:w,%d3',4)
    e.label('action_pc_00e5ca')
    e.ins('lsl.l','#0x1,%d3',2)
    e.label('action_pc_00e5cc')
    e.ins('move.w','0xf3a6:w,%d4',4)
    e.label('action_pc_00e5d0')
    e.ins('lsl.w','#0x1,%d4',2)
    e.label('action_pc_00e5d2')
    e.ins('lea.l','0xb600:w,%a0',4)
    e.label('action_pc_00e5d6')
    e.ins('move.w','(%a0, %d4.w),%d5',4)
    e.label('action_pc_00e5da')
    e.ins('mulu.w','#0xa,%d5',4)
    e.label('action_pc_00e5de')
    e.ins('add.l','%d5,%d3',2)
    e.label('action_pc_00e5e0')
    e.ins('lea.l','0xbe00:w,%a0',4)
    e.label('action_pc_00e5e4')
    e.ins('move.w','(%a0, %d4.w),%d4',4)
    e.label('action_pc_00e5e8')
    e.ins('mulu.w','#0x5,%d4',4)
    e.label('action_pc_00e5ec')
    e.ins('add.l','%d4,%d3',2)
    e.label('action_pc_00e5ee')
    e.ins('move.w','0xf3a6:w,%d4',4)
    e.label('action_pc_00e5f2')
    e.ins('lea.l','0xc200:w,%a0',4)
    e.label('action_pc_00e5f6')
    e.ins('clr.w','%d7',2)
    e.label('action_pc_00e5f8')
    e.ins('move.b','(%a0, %d4.w),%d7',4)
    e.label('action_pc_00e5fc')
    e.ins('cmpi.w','#0x1e,%d7',4)
    e.label('action_pc_00e600')
    e.ins('bhi.b','action_pc_00e604',2)
    e.label('action_pc_00e602')
    e.ins('lsr.w','#0x1,%d3',2)
    e.label('action_pc_00e604')
    e.ins('moveq','#0,%d4',2)
    e.label('action_pc_00e606')
    e.ins('move.w','0xf61c:w,%d4',4)
    e.label('action_pc_00e60a')
    e.ins('move.l','%d4,%d5',2)
    e.label('action_pc_00e60c')
    e.ins('lsl.l','#0x1,%d4',2)
    e.label('action_pc_00e60e')
    e.ins('add.l','%d5,%d4',2)
    e.label('action_pc_00e610')
    e.ins('swap','%d4',2)
    e.label('action_pc_00e612')
    e.ins('add.w','%d2,%d4',2)
    e.label('action_pc_00e614')
    e.ins('mulu.w','%d7,%d4',2)
    e.label('action_pc_00e616')
    e.ins('move.w','%d3,%d5',2)
    e.label('action_pc_00e618')
    e.ins('mulu.w','%d4,%d5',2)
    e.label('action_pc_00e61a')
    e.ins('swap','%d3',2)
    e.label('action_pc_00e61c')
    e.ins('mulu.w','%d4,%d3',2)
    e.label('action_pc_00e61e')
    e.ins('swap','%d3',2)
    e.label('action_pc_00e620')
    e.ins('add.l','%d5,%d3',2)
    e.label('action_pc_00e622')
    e.ins('divu.w','#0x2710,%d3',4)
    e.label('action_pc_00e626')
    e.ins('andi.l','#0xffff,%d3',6)
    e.label('action_pc_00e62c')
    e.ins('divu.w','#0x3c,%d3',4)
    e.label('action_pc_00e630')
    e.ins('clr.w','0xf3c8:w',4)
    e.label('action_pc_00e634')
    e.ins('move.w','%d3,0xf3ca:w',4)
    e.label('action_pc_00e638')
    e.ins('move.w','0xf3a6:w,%d0',4)
    e.label('action_pc_00e63c')
    e.ins('lea.l','0xc300:w,%a0',4)
    e.label('action_pc_00e640')
    e.ins('move.b','(%a0, %d0.w),%d1',4)
    e.label('action_pc_00e644')
    e.ins('ext.w','%d1',2)
    e.label('action_pc_00e646')
    e.ins('add.w','%d3,%d1',2)
    e.label('action_pc_00e648')
    e.ins('cmpi.w','#0x64,%d1',4)
    e.label('action_pc_00e64c')
    e.ins('bls.b','action_pc_00e65c',2)
    e.label('action_pc_00e64e')
    e.ins('move.w','%d1,%d2',2)
    e.label('action_pc_00e650')
    e.ins('subi.w','#0x64,%d2',4)
    e.label('action_pc_00e654')
    e.ins('sub.w','%d2,0xf3ca:w',4)
    e.label('action_pc_00e658')
    e.ins('move.w','#0x64,%d1',4)
    e.label('action_pc_00e65c')
    e.ins('move.b','%d1,(%a0, %d0.w)',4)
    e.label('action_pc_00e660')
    e.ins('move.w','0xf630:w,%d0',4)
    e.label('action_pc_00e664')
    e.ins('cmp.w','0xf3a6:w,%d0',4)
    e.label('action_pc_00e668')
    e.ins('bne.w','action_pc_00e670',4)
    e.label('action_pc_00e66c')
    e.ins('move.w','0xf634:w,%d0',4)
    e.label('action_pc_00e670')
    e.ins('lea.l','0xc200:w,%a0',4)
    e.label('action_pc_00e674')
    e.ins('move.b','(%a0, %d0.w),%d1',4)
    e.label('action_pc_00e678')
    e.ins('addq.b','#0x1,%d1',2)
    e.label('action_pc_00e67a')
    e.ins('cmpi.b','#0x64,%d1',4)
    e.label('action_pc_00e67e')
    e.ins('bls.w','action_pc_00e686',4)
    e.label('action_pc_00e682')
    e.ins('move.b','#0x64,%d1',4)
    e.label('action_pc_00e686')
    e.ins('move.b','%d1,(%a0, %d0.w)',4)
    e.label('action_pc_00e68a')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00e68c')
    e.ins('lea.l','0xbe00:w,%a0',4)
    e.label('action_pc_00e690')
    e.ins('lsr.w','#0x1,%d3',2)
    e.label('action_pc_00e692')
    e.ins('add.w','(%a0, %d0.w),%d3',4)
    e.label('action_pc_00e696')
    e.ins('cmpi.w','#0x3e7,%d3',4)
    e.label('action_pc_00e69a')
    e.ins('bls.w','action_pc_00e6a2',4)
    e.label('action_pc_00e69e')
    e.ins('move.w','#0x3e7,%d3',4)
    e.label('action_pc_00e6a2')
    e.ins('move.w','%d3,(%a0, %d0.w)',4)
    e.label('action_pc_00e6a6')
    e.ins('lea.l','0xcd00:w,%a0',4)
    e.label('action_pc_00e6aa')
    e.ins('move.w','0xf3a6:w,%d0',4)
    e.label('action_pc_00e6ae')
    e.ins('move.b','#0x1,(%a0, %d0.w)',6)
    e.label('action_pc_00e6b4')
    e.ins('move.w','0xf376:w,%d0',4)
    e.label('action_pc_00e6b8')
    e.ins('cmp.w','0xf67a:w,%d0',4)
    e.label('action_pc_00e6bc')
    e.ins('beq.w','action_pc_00e6d0',4)
    e.label('action_pc_00e6c0')
    e.ins('cmp.w','0xf67c:w,%d0',4)
    e.label('action_pc_00e6c4')
    e.ins('beq.w','action_pc_00e6d0',4)
    e.label('action_pc_00e6c8')
    e.ins('cmp.w','0xf67e:w,%d0',4)
    e.label('action_pc_00e6cc')
    e.ins('bne.w','action_pc_00e708',4)
    e.label('action_pc_00e6d0')
    e.ins('move.w','#0x16,0xff7026:l',8)
    e.label('action_pc_00e6d8')
    e.ins('tst.w','0xf3ca:w',4)
    e.label('action_pc_00e6dc')
    e.ins('beq.w','action_pc_00e6e8',4)
    e.label('action_pc_00e6e0')
    e.ins('move.w','#0xa7,%d0',4)
    e.label('action_pc_00e6e4')
    e.ins('bra.w','action_pc_00e6ec',4)
    e.label('action_pc_00e6e8')
    e.ins('move.w','#0xa8,%d0',4)
    e.label('action_pc_00e6ec')
    e.ins('move.w','%d0,0xf3fe:w',4)
    e.label('action_pc_00e6f0')
    e.ins('move.w','0xf38a:w,0xf612:w',6)
    e.label('action_pc_00e6f6')
    e.ins('move.w','0xf38a:w,0xf612:w',6)
    e.label('action_pc_00e6fc')
    e.ins('move.w','#0x28,0xf362:w',6)
    e.label('action_pc_00e702')
    e.ins('move.w','0xf3a6:w,0xf3d0:w',6)
    e.label('action_pc_00e708')
    e.ins('rts','',2)

def _lower_execute_mutual_officer_relationship_reward(e,rules):
    e.label('action_pc_00ea38')
    e.ins('move.w','0xf3a6:w,%d0',4)
    e.label('action_pc_00ea3c')
    e.ins('lea.l','0xc700:w,%a0',4)
    e.label('action_pc_00ea40')
    e.ins('move.b','(%a0, %d0.w),%d1',4)
    e.label('action_pc_00ea44')
    e.ins('andi.b','#0x7,%d1',4)
    e.label('action_pc_00ea48')
    e.ins('ext.w','%d1',2)
    e.label('action_pc_00ea4a')
    e.ins('move.w','%d1,%d3',2)
    e.label('action_pc_00ea4c')
    e.ins('addq.w','#0x2,%d3',2)
    e.label('action_pc_00ea4e')
    e.ins('lea.l','524(%pc),%a0',4)
    e.label('action_pc_00ea52')
    e.ins('nop','',2)
    e.label('action_pc_00ea54')
    e.ins('move.b','(%a0, %d1.w),%d2',4)
    e.label('action_pc_00ea58')
    e.ins('ext.w','%d2',2)
    e.label('action_pc_00ea5a')
    e.ins('moveq','#0,%d1',2)
    e.label('action_pc_00ea5c')
    e.ins('move.w','0xf61c:w,%d1',4)
    e.label('action_pc_00ea60')
    e.ins('mulu.w','%d3,%d1',2)
    e.label('action_pc_00ea62')
    e.ins('swap','%d1',2)
    e.label('action_pc_00ea64')
    e.ins('add.w','%d2,%d1',2)
    e.label('action_pc_00ea66')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00ea68')
    e.ins('lea.l','0xb600:w,%a0',4)
    e.label('action_pc_00ea6c')
    e.ins('move.w','(%a0, %d0.w),%d2',4)
    e.label('action_pc_00ea70')
    e.ins('mulu.w','%d2,%d1',2)
    e.label('action_pc_00ea72')
    e.ins('move.w','0xf376:w,%d0',4)
    e.label('action_pc_00ea76')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00ea78')
    e.ins('lea.l','0xe640:w,%a0',4)
    e.label('action_pc_00ea7c')
    e.ins('move.w','(%a0, %d0.w),%d2',4)
    e.label('action_pc_00ea80')
    e.ins('lea.l','0xc200:w,%a0',4)
    e.label('action_pc_00ea84')
    e.ins('clr.w','%d3',2)
    e.label('action_pc_00ea86')
    e.ins('move.b','(%a0, %d2.w),%d3',4)
    e.label('action_pc_00ea8a')
    e.ins('move.w','#0x78,%d2',4)
    e.label('action_pc_00ea8e')
    e.ins('sub.w','%d3,%d2',2)
    e.label('action_pc_00ea90')
    e.ins('divu.w','%d2,%d1',2)
    e.label('action_pc_00ea92')
    e.ins('cmpi.w','#0xa,%d1',4)
    e.label('action_pc_00ea96')
    e.ins('bcs.w','action_pc_00eb26',4)
    e.label('action_pc_00ea9a')
    e.ins('bsr.w','action_pc_00ec16',4)
    e.label('action_pc_00ea9e')
    e.ins('move.w','#0x26,0xf3fe:w',6)
    e.label('action_pc_00eaa4')
    e.ins('move.w','0xf3a6:w,0xf3d0:w',6)
    e.label('action_pc_00eaaa')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_00eab0')
    e.ins('moveq','#0,%d0',2)
    e.label('action_pc_00eab2')
    e.ins('move.w','0xf61c:w,%d0',4)
    e.label('action_pc_00eab6')
    e.ins('move.l','%d0,%d1',2)
    e.label('action_pc_00eab8')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('action_pc_00eaba')
    e.ins('add.l','%d1,%d0',2)
    e.label('action_pc_00eabc')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('action_pc_00eabe')
    e.ins('swap','%d0',2)
    e.label('action_pc_00eac0')
    e.ins('addq.w','#0x5,%d0',2)
    e.label('action_pc_00eac2')
    e.ins('move.w','0xf376:w,%d1',4)
    e.label('action_pc_00eac6')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('action_pc_00eac8')
    e.ins('lea.l','0xe640:w,%a0',4)
    e.label('action_pc_00eacc')
    e.ins('move.w','(%a0, %d1.w),%d2',4)
    e.label('action_pc_00ead0')
    e.ins('lsl.w','#0x1,%d2',2)
    e.label('action_pc_00ead2')
    e.ins('lea.l','0xbe00:w,%a0',4)
    e.label('action_pc_00ead6')
    e.ins('add.w','(%a0, %d2.w),%d0',4)
    e.label('action_pc_00eada')
    e.ins('cmpi.w','#0x3e7,%d0',4)
    e.label('action_pc_00eade')
    e.ins('bls.w','action_pc_00eae6',4)
    e.label('action_pc_00eae2')
    e.ins('move.w','#0x3e7,%d0',4)
    e.label('action_pc_00eae6')
    e.ins('move.w','%d0,(%a0, %d2.w)',4)
    e.label('action_pc_00eaea')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_00eaf0')
    e.ins('moveq','#0,%d0',2)
    e.label('action_pc_00eaf2')
    e.ins('move.w','0xf61c:w,%d0',4)
    e.label('action_pc_00eaf6')
    e.ins('move.l','%d0,%d1',2)
    e.label('action_pc_00eaf8')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('action_pc_00eafa')
    e.ins('add.l','%d1,%d0',2)
    e.label('action_pc_00eafc')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('action_pc_00eafe')
    e.ins('swap','%d0',2)
    e.label('action_pc_00eb00')
    e.ins('addi.w','#0xa,%d0',4)
    e.label('action_pc_00eb04')
    e.ins('move.w','0xf3a6:w,%d2',4)
    e.label('action_pc_00eb08')
    e.ins('lsl.w','#0x1,%d2',2)
    e.label('action_pc_00eb0a')
    e.ins('lea.l','0xbe00:w,%a0',4)
    e.label('action_pc_00eb0e')
    e.ins('add.w','(%a0, %d2.w),%d0',4)
    e.label('action_pc_00eb12')
    e.ins('cmpi.w','#0x3e7,%d0',4)
    e.label('action_pc_00eb16')
    e.ins('bls.w','action_pc_00eb1e',4)
    e.label('action_pc_00eb1a')
    e.ins('move.w','#0x3e7,%d0',4)
    e.label('action_pc_00eb1e')
    e.ins('move.w','%d0,(%a0, %d2.w)',4)
    e.label('action_pc_00eb22')
    e.ins('bra.w','action_pc_00ebc0',4)
    e.label('action_pc_00eb26')
    e.ins('move.w','#0x28,0xf3fe:w',6)
    e.label('action_pc_00eb2c')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_00eb32')
    e.ins('moveq','#0,%d2',2)
    e.label('action_pc_00eb34')
    e.ins('move.w','0xf61c:w,%d2',4)
    e.label('action_pc_00eb38')
    e.ins('move.l','%d2,%d1',2)
    e.label('action_pc_00eb3a')
    e.ins('lsl.l','#0x1,%d2',2)
    e.label('action_pc_00eb3c')
    e.ins('add.l','%d1,%d2',2)
    e.label('action_pc_00eb3e')
    e.ins('swap','%d2',2)
    e.label('action_pc_00eb40')
    e.ins('addq.w','#0x1,%d2',2)
    e.label('action_pc_00eb42')
    e.ins('move.w','0xf376:w,%d1',4)
    e.label('action_pc_00eb46')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('action_pc_00eb48')
    e.ins('lea.l','0xe640:w,%a0',4)
    e.label('action_pc_00eb4c')
    e.ins('move.w','(%a0, %d1.w),%d0',4)
    e.label('action_pc_00eb50')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00eb52')
    e.ins('lea.l','0xbe00:w,%a0',4)
    e.label('action_pc_00eb56')
    e.ins('add.w','(%a0, %d0.w),%d2',4)
    e.label('action_pc_00eb5a')
    e.ins('cmpi.w','#0x3e7,%d2',4)
    e.label('action_pc_00eb5e')
    e.ins('bls.w','action_pc_00eb66',4)
    e.label('action_pc_00eb62')
    e.ins('move.w','#0x3e7,%d2',4)
    e.label('action_pc_00eb66')
    e.ins('move.w','%d2,(%a0, %d0.w)',4)
    e.label('action_pc_00eb6a')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_00eb70')
    e.ins('moveq','#0,%d2',2)
    e.label('action_pc_00eb72')
    e.ins('move.w','0xf61c:w,%d2',4)
    e.label('action_pc_00eb76')
    e.ins('move.l','%d2,%d1',2)
    e.label('action_pc_00eb78')
    e.ins('lsl.l','#0x1,%d2',2)
    e.label('action_pc_00eb7a')
    e.ins('add.l','%d1,%d2',2)
    e.label('action_pc_00eb7c')
    e.ins('swap','%d2',2)
    e.label('action_pc_00eb7e')
    e.ins('addq.w','#0x1,%d2',2)
    e.label('action_pc_00eb80')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_00eb86')
    e.ins('moveq','#0,%d3',2)
    e.label('action_pc_00eb88')
    e.ins('move.w','0xf61c:w,%d3',4)
    e.label('action_pc_00eb8c')
    e.ins('move.l','%d3,%d1',2)
    e.label('action_pc_00eb8e')
    e.ins('lsl.l','#0x1,%d3',2)
    e.label('action_pc_00eb90')
    e.ins('add.l','%d1,%d3',2)
    e.label('action_pc_00eb92')
    e.ins('swap','%d3',2)
    e.label('action_pc_00eb94')
    e.ins('move.w','0xf3a6:w,%d1',4)
    e.label('action_pc_00eb98')
    e.ins('lea.l','0xc200:w,%a0',4)
    e.label('action_pc_00eb9c')
    e.ins('sub.b','%d3,(%a0, %d1.w)',4)
    e.label('action_pc_00eba0')
    e.ins('bcc.b','action_pc_00eba6',2)
    e.label('action_pc_00eba2')
    e.ins('clr.b','(%a0, %d1.w)',4)
    e.label('action_pc_00eba6')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('action_pc_00eba8')
    e.ins('lea.l','0xbe00:w,%a0',4)
    e.label('action_pc_00ebac')
    e.ins('add.w','(%a0, %d1.w),%d2',4)
    e.label('action_pc_00ebb0')
    e.ins('cmpi.w','#0x3e7,%d2',4)
    e.label('action_pc_00ebb4')
    e.ins('bls.w','action_pc_00ebbc',4)
    e.label('action_pc_00ebb8')
    e.ins('move.w','#0x3e7,%d2',4)
    e.label('action_pc_00ebbc')
    e.ins('move.w','%d2,(%a0, %d1.w)',4)
    e.label('action_pc_00ebc0')
    e.ins('move.w','0xf376:w,%d0',4)
    e.label('action_pc_00ebc4')
    e.ins('cmp.w','0xf67a:w,%d0',4)
    e.label('action_pc_00ebc8')
    e.ins('beq.w','action_pc_00ebdc',4)
    e.label('action_pc_00ebcc')
    e.ins('cmp.w','0xf67c:w,%d0',4)
    e.label('action_pc_00ebd0')
    e.ins('beq.w','action_pc_00ebdc',4)
    e.label('action_pc_00ebd4')
    e.ins('cmp.w','0xf67e:w,%d0',4)
    e.label('action_pc_00ebd8')
    e.ins('bne.w','action_pc_00ec0e',4)
    e.label('action_pc_00ebdc')
    e.ins('move.w','#0xc,0xff7026:l',8)
    e.label('action_pc_00ebe4')
    e.ins('move.w','#0x208,0xf612:w',6)
    e.label('action_pc_00ebea')
    e.ins('move.w','#0x28,0xf362:w',6)
    e.label('action_pc_00ebf0')
    e.ins('move.w','#0x25,%d0',4)
    e.label('action_pc_00ebf4')
    e.ins('move.w','0xf3a6:w,0xf3d0:w',6)
    e.label('action_pc_00ebfa')
    e.ins('jsr','action_pc_0676f2:l',6)
    e.label('action_pc_00ec00')
    e.ins('move.w','0xf3a6:w,%d0',4)
    e.label('action_pc_00ec04')
    e.ins('lea.l','0xcd00:w,%a0',4)
    e.label('action_pc_00ec08')
    e.ins('move.b','#0x1,(%a0, %d0.w)',6)
    e.label('action_pc_00ec0e')
    e.ins('move.w','#0x78,0xf608:w',6)
    e.label('action_pc_00ec14')
    e.ins('rts','',2)

def _lower_execute_officer_policy_outcome(e,rules):
    e.label('action_pc_00ee16')
    e.ins('clr.l','0xf3c8:w',4)
    e.label('action_pc_00ee1a')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('action_pc_00ee1e')
    e.ins('move.w','0xf3f2:w,%d0',4)
    e.label('action_pc_00ee22')
    e.ins('move.b','(%a0, %d0.w),%d0',4)
    e.label('action_pc_00ee26')
    e.ins('lea.l','0xf427:w,%a0',4)
    e.label('action_pc_00ee2a')
    e.ins('move.b','(%a0, %d0.w),%d0',4)
    e.label('action_pc_00ee2e')
    e.ins('lea.l','0xe640:w,%a0',4)
    e.label('action_pc_00ee32')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00ee34')
    e.ins('move.w','(%a0, %d0.w),%d0',4)
    e.label('action_pc_00ee38')
    e.ins('cmp.w','0xf3f2:w,%d0',4)
    e.label('action_pc_00ee3c')
    e.ins('beq.w','action_pc_00ef08',4)
    e.label('action_pc_00ee40')
    e.ins('move.w','0xf3f2:w,%d0',4)
    e.label('action_pc_00ee44')
    e.ins('lea.l','0xc300:w,%a0',4)
    e.label('action_pc_00ee48')
    e.ins('move.b','(%a0, %d0.w),%d1',4)
    e.label('action_pc_00ee4c')
    e.ins('beq.w','action_pc_00ef08',4)
    e.label('action_pc_00ee50')
    e.ins('ext.w','%d1',2)
    e.label('action_pc_00ee52')
    e.ins('subi.w','#0x32,%d1',4)
    e.label('action_pc_00ee56')
    e.ins('bcc.b','action_pc_00ee5a',2)
    e.label('action_pc_00ee58')
    e.ins('neg.w','%d1',2)
    e.label('action_pc_00ee5a')
    e.ins('move.w','#0x3c,%d2',4)
    e.label('action_pc_00ee5e')
    e.ins('sub.w','%d1,%d2',2)
    e.label('action_pc_00ee60')
    e.ins('move.w','0xf3a6:w,%d1',4)
    e.label('action_pc_00ee64')
    e.ins('lea.l','0xc700:w,%a1',4)
    e.label('action_pc_00ee68')
    e.ins('move.b','(%a1, %d1.w),%d3',4)
    e.label('action_pc_00ee6c')
    e.ins('andi.w','#0x7,%d3',4)
    e.label('action_pc_00ee70')
    e.ins('move.b','-97(%pc, %d3.w),%d3',4)
    e.label('action_pc_00ee74')
    e.ins('moveq','#0,%d4',2)
    e.label('action_pc_00ee76')
    e.ins('move.w','0xf61c:w,%d4',4)
    e.label('action_pc_00ee7a')
    e.ins('move.l','%d4,%d5',2)
    e.label('action_pc_00ee7c')
    e.ins('lsl.l','#0x2,%d4',2)
    e.label('action_pc_00ee7e')
    e.ins('add.l','%d5,%d4',2)
    e.label('action_pc_00ee80')
    e.ins('lsl.l','#0x2,%d4',2)
    e.label('action_pc_00ee82')
    e.ins('swap','%d4',2)
    e.label('action_pc_00ee84')
    e.ins('add.w','%d3,%d4',2)
    e.label('action_pc_00ee86')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('action_pc_00ee88')
    e.ins('lea.l','0xb600:w,%a0',4)
    e.label('action_pc_00ee8c')
    e.ins('move.w','(%a0, %d1.w),%d3',4)
    e.label('action_pc_00ee90')
    e.ins('add.w','%d4,%d3',2)
    e.label('action_pc_00ee92')
    e.ins('move.w','0xf3f2:w,%d0',4)
    e.label('action_pc_00ee96')
    e.ins('lea.l','0xc700:w,%a0',4)
    e.label('action_pc_00ee9a')
    e.ins('move.b','(%a0, %d0.w),%d1',4)
    e.label('action_pc_00ee9e')
    e.ins('andi.w','#0x7,%d1',4)
    e.label('action_pc_00eea2')
    e.ins('lea.l','-152(%pc),%a1',4)
    e.label('action_pc_00eea6')
    e.ins('move.b','(%a1, %d1.w),%d4',4)
    e.label('action_pc_00eeaa')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00eeac')
    e.ins('lea.l','0xb600:w,%a1',4)
    e.label('action_pc_00eeb0')
    e.ins('add.w','(%a1, %d0.w),%d4',4)
    e.label('action_pc_00eeb4')
    e.ins('sub.w','%d4,%d3',2)
    e.label('action_pc_00eeb6')
    e.ins('bcs.w','action_pc_00ef08',4)
    e.label('action_pc_00eeba')
    e.ins('muls.w','%d3,%d2',2)
    e.label('action_pc_00eebc')
    e.ins('lea.l','-4022(%pc),%a1',4)
    e.label('action_pc_00eec0')
    e.ins('move.w','0xefd2:w,%d3',4)
    e.label('action_pc_00eec4')
    e.ins('lsl.w','#0x1,%d3',2)
    e.label('action_pc_00eec6')
    e.ins('divu.w','(%a1, %d3.w),%d2',4)
    e.label('action_pc_00eeca')
    e.ins('tst.w','%d2',2)
    e.label('action_pc_00eecc')
    e.ins('beq.w','action_pc_00ef08',4)
    e.label('action_pc_00eed0')
    e.ins('cmpi.w','#0x28,%d2',4)
    e.label('action_pc_00eed4')
    e.ins('bls.b','action_pc_00eeda',2)
    e.label('action_pc_00eed6')
    e.ins('move.w','#0x28,%d2',4)
    e.label('action_pc_00eeda')
    e.ins('clr.w','0xf3c8:w',4)
    e.label('action_pc_00eede')
    e.ins('move.w','%d2,0xf3ca:w',4)
    e.label('action_pc_00eee2')
    e.ins('move.w','0xf3f2:w,%d0',4)
    e.label('action_pc_00eee6')
    e.ins('lea.l','0xc300:w,%a0',4)
    e.label('action_pc_00eeea')
    e.ins('sub.b','%d2,(%a0, %d0.w)',4)
    e.label('action_pc_00eeee')
    e.ins('bcc.b','action_pc_00eef4',2)
    e.label('action_pc_00eef0')
    e.ins('clr.b','(%a0, %d0.w)',4)
    e.label('action_pc_00eef4')
    e.ins('bsr.w','action_pc_00ef60',4)
    e.label('action_pc_00eef8')
    e.ins('move.w','0xf3f2:w,0xf3d2:w',6)
    e.label('action_pc_00eefe')
    e.ins('move.w','#0x39,0xf3fe:w',6)
    e.label('action_pc_00ef04')
    e.ins('bra.w','action_pc_00ef1a',4)
    e.label('action_pc_00ef08')
    e.ins('bsr.w','action_pc_00ef80',4)
    e.label('action_pc_00ef0c')
    e.ins('bsr.w','action_pc_00efa4',4)
    e.label('action_pc_00ef10')
    e.ins('bsr.w','action_pc_00efe2',4)
    e.label('action_pc_00ef14')
    e.ins('move.w','#0x3a,0xf3fe:w',6)
    e.label('action_pc_00ef1a')
    e.ins('move.w','0xf376:w,%d0',4)
    e.label('action_pc_00ef1e')
    e.ins('cmp.w','0xf67a:w,%d0',4)
    e.label('action_pc_00ef22')
    e.ins('beq.w','action_pc_00ef36',4)
    e.label('action_pc_00ef26')
    e.ins('cmp.w','0xf67c:w,%d0',4)
    e.label('action_pc_00ef2a')
    e.ins('beq.w','action_pc_00ef36',4)
    e.label('action_pc_00ef2e')
    e.ins('cmp.w','0xf67e:w,%d0',4)
    e.label('action_pc_00ef32')
    e.ins('bne.w','action_pc_00ef5e',4)
    e.label('action_pc_00ef36')
    e.ins('move.w','#0x208,0xf38a:w',6)
    e.label('action_pc_00ef3c')
    e.ins('move.w','#0x28,0xf362:w',6)
    e.label('action_pc_00ef42')
    e.ins('move.w','#0x78,0xf608:w',6)
    e.label('action_pc_00ef48')
    e.ins('move.w','#0x208,0xf612:w',6)
    e.label('action_pc_00ef4e')
    e.ins('move.w','0xf3a6:w,0xf3d0:w',6)
    e.label('action_pc_00ef54')
    e.ins('move.w','#0x9,%d0',4)
    e.label('action_pc_00ef58')
    e.ins('jsr','action_pc_0676f2:l',6)
    e.label('action_pc_00ef5e')
    e.ins('rts','',2)

def _lower_reduce_selected_officer_disposition_randomly(e,rules):
    e.label('action_pc_00ef80')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_00ef86')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('action_pc_00ef8c')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('action_pc_00ef8e')
    e.ins('swap','%d0',2)
    e.label('action_pc_00ef90')
    e.ins('move.w','0xf3a6:w,%d1',4)
    e.label('action_pc_00ef94')
    e.ins('lea.l','0xc200:w,%a0',4)
    e.label('action_pc_00ef98')
    e.ins('sub.b','%d0,(%a0, %d1.w)',4)
    e.label('action_pc_00ef9c')
    e.ins('bcc.b','action_pc_00efa2',2)
    e.label('action_pc_00ef9e')
    e.ins('clr.b','(%a0, %d1.w)',4)
    e.label('action_pc_00efa2')
    e.ins('rts','',2)

def _lower_reduce_chosen_force_head_disposition_randomly(e,rules):
    e.label('action_pc_00efa4')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_00efaa')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('action_pc_00efb0')
    e.ins('move.l','%d0,%d1',2)
    e.label('action_pc_00efb2')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('action_pc_00efb4')
    e.ins('add.l','%d1,%d0',2)
    e.label('action_pc_00efb6')
    e.ins('swap','%d0',2)
    e.label('action_pc_00efb8')
    e.ins('move.w','0xf392:w,%d1',4)
    e.label('action_pc_00efbc')
    e.ins('lea.l','0xf427:w,%a0',4)
    e.label('action_pc_00efc0')
    e.ins('move.b','(%a0, %d1.w),%d1',4)
    e.label('action_pc_00efc4')
    e.ins('andi.w','#0xf,%d1',4)
    e.label('action_pc_00efc8')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('action_pc_00efca')
    e.ins('lea.l','0xe640:w,%a0',4)
    e.label('action_pc_00efce')
    e.ins('move.w','(%a0, %d1.w),%d1',4)
    e.label('action_pc_00efd2')
    e.ins('lea.l','0xc200:w,%a0',4)
    e.label('action_pc_00efd6')
    e.ins('sub.b','%d0,(%a0, %d1.w)',4)
    e.label('action_pc_00efda')
    e.ins('bcc.b','action_pc_00efe0',2)
    e.label('action_pc_00efdc')
    e.ins('clr.b','(%a0, %d1.w)',4)
    e.label('action_pc_00efe0')
    e.ins('rts','',2)

def _lower_credit_selected_officer_policy_progress(e,rules):
    e.label('action_pc_00efe2')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_00efe8')
    e.ins('moveq','#0,%d0',2)
    e.label('action_pc_00efea')
    e.ins('move.w','0xf61c:w,%d0',4)
    e.label('action_pc_00efee')
    e.ins('move.l','%d0,%d1',2)
    e.label('action_pc_00eff0')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('action_pc_00eff2')
    e.ins('add.l','%d1,%d0',2)
    e.label('action_pc_00eff4')
    e.ins('swap','%d0',2)
    e.label('action_pc_00eff6')
    e.ins('addi.w','#0x1,%d0',4)
    e.label('action_pc_00effa')
    e.ins('move.w','0xf3a6:w,%d1',4)
    e.label('action_pc_00effe')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('action_pc_00f000')
    e.ins('lea.l','0xbe00:w,%a0',4)
    e.label('action_pc_00f004')
    e.ins('add.w','%d0,(%a0, %d1.w)',4)
    e.label('action_pc_00f008')
    e.ins('cmpi.w','#0x3e7,(%a0, %d1.w)',6)
    e.label('action_pc_00f00e')
    e.ins('bls.b','action_pc_00f016',2)
    e.label('action_pc_00f010')
    e.ins('move.w','#0x3e7,(%a0, %d1.w)',6)
    e.label('action_pc_00f016')
    e.ins('rts','',2)

def _lower_execute_officer_recruitment_outcome(e,rules):
    e.label('action_pc_00f778')
    e.ins('bsr.w','action_pc_00f7da',4)
    e.label('action_pc_00f77c')
    e.ins('bsr.w','action_pc_00f82c',4)
    e.label('action_pc_00f780')
    e.ins('bsr.w','action_pc_00fae0',4)
    e.label('action_pc_00f784')
    e.ins('cmp.w','%d3,%d0',2)
    e.label('action_pc_00f786')
    e.ins('bcs.b','action_pc_00f7a0',2)
    e.label('action_pc_00f788')
    e.ins('move.w','#0x3a,0xf3fe:w',6)
    e.label('action_pc_00f78e')
    e.ins('bsr.w','action_pc_00f896',4)
    e.label('action_pc_00f792')
    e.ins('move.w','#0x78,0xf608:w',6)
    e.label('action_pc_00f798')
    e.ins('move.w','#0x1f,0xf362:w',6)
    e.label('action_pc_00f79e')
    e.ins('bra.b','action_pc_00f7bc',2)
    e.label('action_pc_00f7a0')
    e.ins('move.w','#0x3c,0xf3fe:w',6)
    e.label('action_pc_00f7a6')
    e.ins('bsr.w','action_pc_00f990',4)
    e.label('action_pc_00f7aa')
    e.ins('bsr.w','action_pc_00f9d0',4)
    e.label('action_pc_00f7ae')
    e.ins('move.w','#0x3,0xff7026:l',8)
    e.label('action_pc_00f7b6')
    e.ins('move.w','#0x28,0xf362:w',6)
    e.label('action_pc_00f7bc')
    e.ins('move.w','#0x208,0xf612:w',6)
    e.label('action_pc_00f7c2')
    e.ins('move.w','#0x9,%d0',4)
    e.label('action_pc_00f7c6')
    e.ins('move.w','0xf3a6:w,0xf3d0:w',6)
    e.label('action_pc_00f7cc')
    e.ins('jsr','action_pc_0676f2:l',6)
    e.label('action_pc_00f7d2')
    e.ins('move.w','#0x78,0xf608:w',6)
    e.label('action_pc_00f7d8')
    e.ins('rts','',2)

def _lower_score_selected_officer_recruitment(e,rules):
    e.label('action_pc_00f7da')
    e.ins('move.w','0xf3a6:w,%d0',4)
    e.label('action_pc_00f7de')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00f7e0')
    e.ins('lea.l','0xc000:w,%a0',4)
    e.label('action_pc_00f7e4')
    e.ins('moveq','#0,%d2',2)
    e.label('action_pc_00f7e6')
    e.ins('move.w','(%a0, %d0.w),%d2',4)
    e.label('action_pc_00f7ea')
    e.ins('divu.w','#0xa,%d2',4)
    e.label('action_pc_00f7ee')
    e.ins('lea.l','0xb600:w,%a0',4)
    e.label('action_pc_00f7f2')
    e.ins('add.w','(%a0, %d0.w),%d2',4)
    e.label('action_pc_00f7f6')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_00f7fc')
    e.ins('lea.l','-6384(%pc),%a0',4)
    e.label('action_pc_00f800')
    e.ins('move.w','0xefd2:w,%d1',4)
    e.label('action_pc_00f804')
    e.ins('lsl.w','#0x2,%d1',2)
    e.label('action_pc_00f806')
    e.ins('mulu.w','(%a0, %d1.w),%d0',4)
    e.label('action_pc_00f80a')
    e.ins('swap','%d0',2)
    e.label('action_pc_00f80c')
    e.ins('add.w','0x2(%a0, %d1.w),%d0',4)
    e.label('action_pc_00f810')
    e.ins('add.w','%d0,%d2',2)
    e.label('action_pc_00f812')
    e.ins('move.w','0xf3a8:w,%d0',4)
    e.label('action_pc_00f816')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00f818')
    e.ins('lea.l','0xf45e:w,%a0',4)
    e.label('action_pc_00f81c')
    e.ins('move.w','(%a0, %d0.w),%d0',4)
    e.label('action_pc_00f820')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00f822')
    e.ins('lea.l','0xb600:w,%a0',4)
    e.label('action_pc_00f826')
    e.ins('sub.w','(%a0, %d0.w),%d2',4)
    e.label('action_pc_00f82a')
    e.ins('rts','',2)

def _lower_bucket_recruitment_score(e,rules):
    e.label('action_pc_00f82c')
    e.ins('clr.w','%d3',2)
    e.label('action_pc_00f82e')
    e.ins('clr.w','%d4',2)
    e.label('action_pc_00f830')
    e.ins('tst.w','%d2',2)
    e.label('action_pc_00f832')
    e.ins('beq.b','action_pc_00f894',2)
    e.label('action_pc_00f834')
    e.ins('bmi.b','action_pc_00f894',2)
    e.label('action_pc_00f836')
    e.ins('move.w','#0xa,%d3',4)
    e.label('action_pc_00f83a')
    e.ins('addq.w','#0x1,%d4',2)
    e.label('action_pc_00f83c')
    e.ins('cmpi.w','#0x32,%d2',4)
    e.label('action_pc_00f840')
    e.ins('bls.b','action_pc_00f894',2)
    e.label('action_pc_00f842')
    e.ins('move.w','#0x1e,%d3',4)
    e.label('action_pc_00f846')
    e.ins('addq.w','#0x1,%d4',2)
    e.label('action_pc_00f848')
    e.ins('cmpi.w','#0x64,%d2',4)
    e.label('action_pc_00f84c')
    e.ins('bls.b','action_pc_00f894',2)
    e.label('action_pc_00f84e')
    e.ins('move.w','#0x32,%d3',4)
    e.label('action_pc_00f852')
    e.ins('addq.w','#0x1,%d4',2)
    e.label('action_pc_00f854')
    e.ins('cmpi.w','#0x96,%d2',4)
    e.label('action_pc_00f858')
    e.ins('bls.b','action_pc_00f894',2)
    e.label('action_pc_00f85a')
    e.ins('move.w','#0x3c,%d3',4)
    e.label('action_pc_00f85e')
    e.ins('addq.w','#0x1,%d4',2)
    e.label('action_pc_00f860')
    e.ins('cmpi.w','#0xc8,%d2',4)
    e.label('action_pc_00f864')
    e.ins('bls.b','action_pc_00f894',2)
    e.label('action_pc_00f866')
    e.ins('move.w','#0x46,%d3',4)
    e.label('action_pc_00f86a')
    e.ins('addq.w','#0x1,%d4',2)
    e.label('action_pc_00f86c')
    e.ins('cmpi.w','#0xfa,%d2',4)
    e.label('action_pc_00f870')
    e.ins('bls.b','action_pc_00f894',2)
    e.label('action_pc_00f872')
    e.ins('move.w','#0x50,%d3',4)
    e.label('action_pc_00f876')
    e.ins('addq.w','#0x1,%d4',2)
    e.label('action_pc_00f878')
    e.ins('cmpi.w','#0x12c,%d2',4)
    e.label('action_pc_00f87c')
    e.ins('bls.b','action_pc_00f894',2)
    e.label('action_pc_00f87e')
    e.ins('move.w','#0x50,%d3',4)
    e.label('action_pc_00f882')
    e.ins('addq.w','#0x1,%d4',2)
    e.label('action_pc_00f884')
    e.ins('cmpi.w','#0x15e,%d2',4)
    e.label('action_pc_00f888')
    e.ins('bls.b','action_pc_00f894',2)
    e.label('action_pc_00f88a')
    e.ins('move.w','#0x55,%d3',4)
    e.label('action_pc_00f88e')
    e.ins('addq.w','#0x1,%d4',2)
    e.label('action_pc_00f890')
    e.ins('move.w','#0x15f,%d2',4)
    e.label('action_pc_00f894')
    e.ins('rts','',2)

def _lower_apply_recruited_officer_roster_transition(e,rules):
    e.label('action_pc_00f896')
    e.ins('move.w','0xf3a6:w,%d0',4)
    e.label('action_pc_00f89a')
    e.ins('lea.l','0xe640:w,%a0',4)
    e.label('action_pc_00f89e')
    e.ins('move.w','#0x15,%d3',4)
    e.label('action_pc_00f8a2')
    e.ins('cmp.w','(%a0)+,%d0',2)
    e.label('action_pc_00f8a4')
    e.ins('beq.w','action_pc_00f962',4)
    e.label('action_pc_00f8a8')
    e.ins('dbra','%d3,action_pc_00f8a2',4)
    e.label('action_pc_00f8ac')
    e.ins('move.w','0xf3a6:w,%d0',4)
    e.label('action_pc_00f8b0')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00f8b2')
    e.ins('lea.l','0xb400:w,%a0',4)
    e.label('action_pc_00f8b6')
    e.ins('move.w','(%a0, %d0.w),%d3',4)
    e.label('action_pc_00f8ba')
    e.ins('lsr.w','#0x1,%d3',2)
    e.label('action_pc_00f8bc')
    e.ins('bsr.w','action_pc_00fae0',4)
    e.label('action_pc_00f8c0')
    e.ins('cmp.w','%d3,%d0',2)
    e.label('action_pc_00f8c2')
    e.ins('bcs.w','action_pc_00f962',4)
    e.label('action_pc_00f8c6')
    e.ins('move.w','0xf3a8:w,%d0',4)
    e.label('action_pc_00f8ca')
    e.ins('move.w','#0xffff,0xf630:w',6)
    e.label('action_pc_00f8d0')
    e.ins('jsr','action_pc_005f48:l',6)
    e.label('action_pc_00f8d6')
    e.ins('cmpi.w','#0xa,%d3',4)
    e.label('action_pc_00f8da')
    e.ins('bcc.b','action_pc_00f918',2)
    e.label('action_pc_00f8dc')
    e.ins('move.w','0xf3a6:w,%d0',4)
    e.label('action_pc_00f8e0')
    e.ins('lea.l','0xc300:w,%a0',4)
    e.label('action_pc_00f8e4')
    e.ins('clr.w','%d1',2)
    e.label('action_pc_00f8e6')
    e.ins('move.b','(%a0, %d0.w),%d1',4)
    e.label('action_pc_00f8ea')
    e.ins('move.w','#0x64,%d2',4)
    e.label('action_pc_00f8ee')
    e.ins('sub.w','%d1,%d2',2)
    e.label('action_pc_00f8f0')
    e.ins('move.w','0xf3a8:w,%d1',4)
    e.label('action_pc_00f8f4')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('action_pc_00f8f6')
    e.ins('lea.l','0xf45e:w,%a0',4)
    e.label('action_pc_00f8fa')
    e.ins('move.w','(%a0, %d1.w),%d1',4)
    e.label('action_pc_00f8fe')
    e.ins('clr.w','%d0',2)
    e.label('action_pc_00f900')
    e.ins('lea.l','0xc200:w,%a0',4)
    e.label('action_pc_00f904')
    e.ins('move.b','(%a0, %d1.w),%d0',4)
    e.label('action_pc_00f908')
    e.ins('add.w','%d0,%d2',2)
    e.label('action_pc_00f90a')
    e.ins('cmpi.w','#0x64,%d2',4)
    e.label('action_pc_00f90e')
    e.ins('bcc.b','action_pc_00f95e',2)
    e.label('action_pc_00f910')
    e.ins('bsr.w','action_pc_00fae0',4)
    e.label('action_pc_00f914')
    e.ins('cmp.w','%d2,%d0',2)
    e.label('action_pc_00f916')
    e.ins('bcs.b','action_pc_00f95e',2)
    e.label('action_pc_00f918')
    e.ins('move.w','#0x5d,0xf3fe:w',6)
    e.label('action_pc_00f91e')
    e.ins('move.w','0xf3a6:w,%d0',4)
    e.label('action_pc_00f922')
    e.ins('lea.l','0xcc00:w,%a0',4)
    e.label('action_pc_00f926')
    e.ins('move.b','#0xff,(%a0, %d0.w)',6)
    e.label('action_pc_00f92c')
    e.ins('lea.l','0xf45e:w,%a0',4)
    e.label('action_pc_00f930')
    e.ins('move.w','0xf392:w,%d0',4)
    e.label('action_pc_00f934')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00f936')
    e.ins('move.w','0xf3a6:w,%d1',4)
    e.label('action_pc_00f93a')
    e.ins('cmp.w','(%a0, %d0.w),%d1',4)
    e.label('action_pc_00f93e')
    e.ins('bne.w','action_pc_00f98e',4)
    e.label('action_pc_00f942')
    e.ins('move.w','0xf392:w,%d0',4)
    e.label('action_pc_00f946')
    e.ins('move.w','#0xffff,0xf630:w',6)
    e.label('action_pc_00f94c')
    e.ins('jsr','action_pc_005f48:l',6)
    e.label('action_pc_00f952')
    e.ins('move.w','0xf392:w,%d0',4)
    e.label('action_pc_00f956')
    e.ins('jsr','-5986(%pc)',4)
    e.label('action_pc_00f95a')
    e.ins('bra.w','action_pc_00f98e',4)
    e.label('action_pc_00f95e')
    e.ins('bra.w','action_pc_00f98e',4)
    e.label('action_pc_00f962')
    e.ins('tst.w','%d2',2)
    e.label('action_pc_00f964')
    e.ins('bmi.b','action_pc_00f98e',2)
    e.label('action_pc_00f966')
    e.ins('andi.l','#0xffff,%d2',6)
    e.label('action_pc_00f96c')
    e.ins('divu.w','#0xa,%d2',4)
    e.label('action_pc_00f970')
    e.ins('move.w','0xf3a6:w,%d0',4)
    e.label('action_pc_00f974')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_00f976')
    e.ins('lea.l','0xc000:w,%a0',4)
    e.label('action_pc_00f97a')
    e.ins('move.w','(%a0, %d0.w),%d3',4)
    e.label('action_pc_00f97e')
    e.ins('add.w','%d2,%d3',2)
    e.label('action_pc_00f980')
    e.ins('cmpi.w','#0x3e7,%d3',4)
    e.label('action_pc_00f984')
    e.ins('bls.b','action_pc_00f98a',2)
    e.label('action_pc_00f986')
    e.ins('move.w','#0x3e7,%d3',4)
    e.label('action_pc_00f98a')
    e.ins('move.w','%d3,(%a0, %d0.w)',4)
    e.label('action_pc_00f98e')
    e.ins('rts','',2)

def _lower_apply_recruitment_city_resource_losses(e,rules):
    e.label('action_pc_00f9d0')
    e.ins('tst.w','%d4',2)
    e.label('action_pc_00f9d2')
    e.ins('beq.b','action_pc_00f9e8',2)
    e.label('action_pc_00f9d4')
    e.ins('move.w','0xf3a8:w,%d2',4)
    e.label('action_pc_00f9d8')
    e.ins('subq.w','#0x1,%d2',2)
    e.label('action_pc_00f9da')
    e.ins('lsl.w','#0x2,%d2',2)
    e.label('action_pc_00f9dc')
    e.ins('bsr.w','action_pc_00f9ea',4)
    e.label('action_pc_00f9e0')
    e.ins('bsr.w','action_pc_00fa3a',4)
    e.label('action_pc_00f9e4')
    e.ins('bsr.w','action_pc_00fa8a',4)
    e.label('action_pc_00f9e8')
    e.ins('rts','',2)

def _lower_reduce_recruitment_city_food(e,rules):
    e.label('action_pc_00f9ea')
    e.ins('move.w','%d4,%d5',2)
    e.label('action_pc_00f9ec')
    e.ins('lsl.w','#0x2,%d5',2)
    e.label('action_pc_00f9ee')
    e.ins('lea.l','38(%pc),%a0',4)
    e.label('action_pc_00f9f2')
    e.ins('move.w','(%a0, %d5.w),%d6',4)
    e.label('action_pc_00f9f6')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_00f9fc')
    e.ins('mulu.w','%d6,%d0',2)
    e.label('action_pc_00f9fe')
    e.ins('swap','%d0',2)
    e.label('action_pc_00fa00')
    e.ins('add.w','0x2(%a0, %d5.w),%d0',4)
    e.label('action_pc_00fa04')
    e.ins('lea.l','0xe0a0:w,%a0',4)
    e.label('action_pc_00fa08')
    e.ins('move.l','(%a0, %d2.w),%d1',4)
    e.label('action_pc_00fa0c')
    e.ins('move.l','%d1,%d3',2)
    e.label('action_pc_00fa0e')
    e.ins('divu.w','#0x64,%d3',4)
    e.label('action_pc_00fa12')
    e.ins('mulu.w','%d0,%d3',2)
    e.label('action_pc_00fa14')
    e.ins('sub.l','%d3,(%a0, %d2.w)',4)
    e.label('action_pc_00fa18')
    e.ins('rts','',2)

def _lower_reduce_recruitment_city_gold(e,rules):
    e.label('action_pc_00fa3a')
    e.ins('move.w','%d4,%d5',2)
    e.label('action_pc_00fa3c')
    e.ins('lsl.w','#0x2,%d5',2)
    e.label('action_pc_00fa3e')
    e.ins('lea.l','38(%pc),%a0',4)
    e.label('action_pc_00fa42')
    e.ins('move.w','(%a0, %d5.w),%d6',4)
    e.label('action_pc_00fa46')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_00fa4c')
    e.ins('mulu.w','%d6,%d0',2)
    e.label('action_pc_00fa4e')
    e.ins('swap','%d0',2)
    e.label('action_pc_00fa50')
    e.ins('add.w','0x2(%a0, %d5.w),%d0',4)
    e.label('action_pc_00fa54')
    e.ins('lea.l','0xe000:w,%a0',4)
    e.label('action_pc_00fa58')
    e.ins('move.l','(%a0, %d2.w),%d1',4)
    e.label('action_pc_00fa5c')
    e.ins('move.l','%d1,%d3',2)
    e.label('action_pc_00fa5e')
    e.ins('divu.w','#0x64,%d3',4)
    e.label('action_pc_00fa62')
    e.ins('mulu.w','%d0,%d3',2)
    e.label('action_pc_00fa64')
    e.ins('sub.l','%d3,(%a0, %d2.w)',4)
    e.label('action_pc_00fa68')
    e.ins('rts','',2)

def _lower_reduce_recruitment_city_state_parameter(e,rules):
    e.label('action_pc_00fa8a')
    e.ins('move.w','%d4,%d5',2)
    e.label('action_pc_00fa8c')
    e.ins('lsl.w','#0x2,%d5',2)
    e.label('action_pc_00fa8e')
    e.ins('lea.l','44(%pc),%a0',4)
    e.label('action_pc_00fa92')
    e.ins('move.w','(%a0, %d5.w),%d6',4)
    e.label('action_pc_00fa96')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_00fa9c')
    e.ins('mulu.w','%d6,%d0',2)
    e.label('action_pc_00fa9e')
    e.ins('swap','%d0',2)
    e.label('action_pc_00faa0')
    e.ins('add.w','0x2(%a0, %d5.w),%d0',4)
    e.label('action_pc_00faa4')
    e.ins('lea.l','0xe1e0:w,%a0',4)
    e.label('action_pc_00faa8')
    e.ins('move.l','(%a0, %d2.w),%d1',4)
    e.label('action_pc_00faac')
    e.ins('move.w','%d1,%d3',2)
    e.label('action_pc_00faae')
    e.ins('mulu.w','%d0,%d3',2)
    e.label('action_pc_00fab0')
    e.ins('divu.w','#0x64,%d3',4)
    e.label('action_pc_00fab4')
    e.ins('andi.l','#0xffff,%d3',6)
    e.label('action_pc_00faba')
    e.ins('sub.l','%d3,(%a0, %d2.w)',4)
    e.label('action_pc_00fabe')
    e.ins('rts','',2)

def _lower_draw_recruitment_probability(e,rules):
    e.label('action_pc_00fae0')
    e.ins('jsr','action_pc_0083d4:l',6)
    e.label('action_pc_00fae6')
    e.ins('andi.l','#0xffff,%d0',6)
    e.label('action_pc_00faec')
    e.ins('move.l','%d0,%d1',2)
    e.label('action_pc_00faee')
    e.ins('lsl.l','#0x1,%d0',2)
    e.label('action_pc_00faf0')
    e.ins('add.l','%d1,%d0',2)
    e.label('action_pc_00faf2')
    e.ins('lsl.l','#0x3,%d0',2)
    e.label('action_pc_00faf4')
    e.ins('add.l','%d1,%d0',2)
    e.label('action_pc_00faf6')
    e.ins('lsl.l','#0x2,%d0',2)
    e.label('action_pc_00faf8')
    e.ins('swap','%d0',2)
    e.label('action_pc_00fafa')
    e.ins('rts','',2)

LOWERERS = {
    'execute_officer_loyalty_reward':_lower_execute_officer_loyalty_reward,
    'execute_mutual_officer_relationship_reward':_lower_execute_mutual_officer_relationship_reward,
    'execute_officer_policy_outcome':_lower_execute_officer_policy_outcome,
    'reduce_selected_officer_disposition_randomly':_lower_reduce_selected_officer_disposition_randomly,
    'reduce_chosen_force_head_disposition_randomly':_lower_reduce_chosen_force_head_disposition_randomly,
    'credit_selected_officer_policy_progress':_lower_credit_selected_officer_policy_progress,
    'execute_officer_recruitment_outcome':_lower_execute_officer_recruitment_outcome,
    'score_selected_officer_recruitment':_lower_score_selected_officer_recruitment,
    'bucket_recruitment_score':_lower_bucket_recruitment_score,
    'apply_recruited_officer_roster_transition':_lower_apply_recruited_officer_roster_transition,
    'apply_recruitment_city_resource_losses':_lower_apply_recruitment_city_resource_losses,
    'reduce_recruitment_city_food':_lower_reduce_recruitment_city_food,
    'reduce_recruitment_city_gold':_lower_reduce_recruitment_city_gold,
    'reduce_recruitment_city_state_parameter':_lower_reduce_recruitment_city_state_parameter,
    'draw_recruitment_probability':_lower_draw_recruitment_probability,
}

def compile_personnel(source):
    records = semantic_functions(source,DECLARATIONS,APPROVED)
    for binding in PERSONNEL_BINDINGS:
        field = binding.name+'_frame_fields'
        records[binding.name]['effects'] = dict(
            actual_legacy_projection=records[binding.name]['effects'],
            sole_complete_field_core=records[field]['effects'],
            shared_actual_fields={name:records[name]['effects'] for name in ('_personnel_recruitment_resource_fields', '_personnel_visible_force_fields', '_personnel_relationship_progress_fields')})
    return lower_declared({binding.name:records[binding.name] for binding in PERSONNEL_BINDINGS},PERSONNEL_BINDINGS,LOWERERS)

# C58 sole complete fields and compatibility projections; fixed original defaults only.
DECLARATIONS.update({'execute_officer_loyalty_reward': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 58770)\nactual = execute_officer_loyalty_reward_frame_fields(memory, entered)\nreturn None'}, 'execute_mutual_officer_relationship_reward': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 59960)\nactual = execute_mutual_officer_relationship_reward_frame_fields(memory, entered)\nreturn None'}, 'execute_officer_policy_outcome': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 60950)\nactual = execute_officer_policy_outcome_frame_fields(memory, entered)\nreturn None'}, 'reduce_selected_officer_disposition_randomly': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'Word', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 61312)\nactual = reduce_selected_officer_disposition_randomly_frame_fields(memory, entered)\nreturn actual.data[0] & 65535'}, 'reduce_chosen_force_head_disposition_randomly': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'Word', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 61348)\nactual = reduce_chosen_force_head_disposition_randomly_frame_fields(memory, entered)\nreturn actual.data[0] & 65535'}, 'credit_selected_officer_policy_progress': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'Word', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 61410)\nactual = credit_selected_officer_policy_progress_frame_fields(memory, entered)\nreturn actual.data[0] & 65535'}, 'execute_officer_recruitment_outcome': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 63352)\nactual = execute_officer_recruitment_outcome_frame_fields(memory, entered)\nreturn None'}, 'score_selected_officer_recruitment': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'Long', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 63450)\nactual = score_selected_officer_recruitment_frame_fields(memory, entered)\nreturn actual.data[2]'}, 'bucket_recruitment_score': {'signature': 'score: Long, entry_frame: CommandFrame | None=None, state: GameState | None=None', 'returns': 'RecruitmentScore', 'flow': "if state is None:\n    raise Boundary('historical value-only score API lacks actual memory/full carriers; supply state and entry_frame')\nmemory, entered = _personnel_legacy_entry(state, entry_frame, 63532)\nuint(score, 32)\nif score != entered.data[2]:\n    raise ValueError('compatibility score/gain must match real incoming D2')\nactual = bucket_recruitment_score_frame_fields(memory, entered)\nreturn RecruitmentScore(actual.data[2], actual.data[3] & 65535, actual.data[4] & 65535)"}, 'apply_recruited_officer_roster_transition': {'signature': 'state: GameState, score: Long, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': "memory, entered = _personnel_legacy_entry(state, entry_frame, 63638)\nuint(score, 32)\nif score != entered.data[2]:\n    raise ValueError('compatibility score/gain must match real incoming D2')\nactual = apply_recruited_officer_roster_transition_frame_fields(memory, entered)\nreturn None"}, 'apply_recruitment_city_resource_losses': {'signature': 'state: GameState, bucket: Word, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': "memory, entered = _personnel_legacy_entry(state, entry_frame, 63952)\nuint(bucket, 16)\nif bucket != entered.data[4] & 65535:\n    raise ValueError('compatibility bucket must match real incoming D4 WORD')\nactual = apply_recruitment_city_resource_losses_frame_fields(memory, entered)\nreturn None"}, 'reduce_recruitment_city_food': {'signature': 'state: GameState, city_offset: Word, bucket: Word, entry_frame: CommandFrame | None=None', 'returns': 'Long', 'flow': "memory, entered = _personnel_legacy_entry(state, entry_frame, 63978)\nuint(bucket, 16)\nif bucket != entered.data[4] & 65535:\n    raise ValueError('compatibility bucket must match real incoming D4 WORD')\nuint(city_offset, 16)\nif city_offset != entered.data[2] & 65535:\n    raise ValueError('compatibility city offset must match real incoming D2 WORD')\nactual = reduce_recruitment_city_food_frame_fields(memory, entered)\nreturn actual.data[3]"}, 'reduce_recruitment_city_gold': {'signature': 'state: GameState, city_offset: Word, bucket: Word, entry_frame: CommandFrame | None=None', 'returns': 'Long', 'flow': "memory, entered = _personnel_legacy_entry(state, entry_frame, 64058)\nuint(bucket, 16)\nif bucket != entered.data[4] & 65535:\n    raise ValueError('compatibility bucket must match real incoming D4 WORD')\nuint(city_offset, 16)\nif city_offset != entered.data[2] & 65535:\n    raise ValueError('compatibility city offset must match real incoming D2 WORD')\nactual = reduce_recruitment_city_gold_frame_fields(memory, entered)\nreturn actual.data[3]"}, 'reduce_recruitment_city_state_parameter': {'signature': 'state: GameState, city_offset: Word, bucket: Word, entry_frame: CommandFrame | None=None', 'returns': 'Long', 'flow': "memory, entered = _personnel_legacy_entry(state, entry_frame, 64138)\nuint(bucket, 16)\nif bucket != entered.data[4] & 65535:\n    raise ValueError('compatibility bucket must match real incoming D4 WORD')\nuint(city_offset, 16)\nif city_offset != entered.data[2] & 65535:\n    raise ValueError('compatibility city offset must match real incoming D2 WORD')\nactual = reduce_recruitment_city_state_parameter_frame_fields(memory, entered)\nreturn actual.data[3]"}, 'draw_recruitment_probability': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'Word', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 64224)\nactual = draw_recruitment_probability_frame_fields(memory, entered)\nreturn actual.data[0] & 65535'}, '_personnel_visible_force_fields': {'signature': 'memory, frame', 'returns': None, 'flow': 'frame = _personnel_read_fields(memory, frame, 0, 4294964086)\nfor address in (4294964858, 4294964860, 4294964862):\n    frame = _personnel_compare_fields(memory, frame, frame.data[0] & 65535, memory.state.read(address, 2))\n    if frame.status_word & 4:\n        return (frame, True)\nreturn (frame, False)'}, 'execute_officer_loyalty_reward_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_call_fields(memory, frame, 59146, 58774)\nframe = frame.with_address(0, 4294951680)\nframe = _personnel_read_fields(memory, frame, 0, 4294964784)\nframe = _personnel_compare_fields(memory, frame, frame.data[0] & 65535, memory.state.read(4294964134, 2))\nspecial_teacher = bool(frame.status_word & 4)\nif not special_teacher:\n    frame = _personnel_compare_fields(memory, frame, frame.data[0] & 65535, memory.state.read(4294964788, 2))\n    special_teacher = bool(frame.status_word & 4)\nif special_teacher:\n    frame = _personnel_load_fields(memory, frame, 0, 100)\nelse:\n    frame = _personnel_read_fields(memory, frame, 0, _personnel_indexed_address(frame, 0, 0), 8)\n    frame = _personnel_ext_word_fields(memory, frame, 0)\nframe = _personnel_read_fields(memory, frame, 1, 4294964134)\nframe = _personnel_read_fields(memory, frame, 1, _personnel_indexed_address(frame, 0, 1), 8)\nframe = _personnel_ext_word_fields(memory, frame, 1)\nframe = _personnel_call_fields(memory, frame, 59166, 58822)\nframe = _personnel_read_fields(memory, frame, 3, 4294964126, 32)\nframe = _personnel_shift_fields(memory, frame, 3, 1, 32)\nframe = _personnel_read_fields(memory, frame, 4, 4294964134)\nframe = _personnel_shift_fields(memory, frame, 4, 1)\nframe = frame.with_address(0, 4294948352)\nframe = _personnel_read_fields(memory, frame, 5, _personnel_indexed_address(frame, 0, 4))\nframe = _personnel_product_fields(memory, frame, 5, 10)\nframe = _personnel_arithmetic_fields(memory, frame, 3, frame.data[5], 32)\nframe = frame.with_address(0, 4294950400)\nframe = _personnel_read_fields(memory, frame, 4, _personnel_indexed_address(frame, 0, 4))\nframe = _personnel_product_fields(memory, frame, 4, 5)\nframe = _personnel_arithmetic_fields(memory, frame, 3, frame.data[4], 32)\nframe = _personnel_read_fields(memory, frame, 4, 4294964134)\nframe = frame.with_address(0, 4294951424)\nframe = _personnel_load_fields(memory, frame, 7, 0)\nframe = _personnel_read_fields(memory, frame, 7, _personnel_indexed_address(frame, 0, 4), 8)\nframe = _personnel_compare_fields(memory, frame, frame.data[7] & 65535, 30)\nif frame.status_word & 5:\n    frame = _personnel_shift_fields(memory, frame, 3, 1, 16, True)\nframe = _personnel_load_fields(memory, frame, 4, 0, 32)\nframe = _personnel_read_fields(memory, frame, 4, 4294964764)\nframe = _personnel_load_fields(memory, frame, 5, frame.data[4], 32)\nframe = _personnel_shift_fields(memory, frame, 4, 1, 32)\nframe = _personnel_arithmetic_fields(memory, frame, 4, frame.data[5], 32)\nframe = _personnel_swap_fields(memory, frame, 4)\nframe = _personnel_arithmetic_fields(memory, frame, 4, frame.data[2] & 65535)\nframe = _personnel_product_fields(memory, frame, 4, frame.data[7] & 65535)\nframe = _personnel_load_fields(memory, frame, 5, frame.data[3] & 65535)\nframe = _personnel_product_fields(memory, frame, 5, frame.data[4] & 65535)\nframe = _personnel_swap_fields(memory, frame, 3)\nframe = _personnel_product_fields(memory, frame, 3, frame.data[4] & 65535)\nframe = _personnel_swap_fields(memory, frame, 3)\nframe = _personnel_arithmetic_fields(memory, frame, 3, frame.data[5], 32)\nframe = _personnel_quotient_fields(memory, frame, 3, 10000, 58914)\nframe = _personnel_and_fields(memory, frame, 3, 65535, 32)\nframe = _personnel_quotient_fields(memory, frame, 3, 60, 58924)\nframe = _personnel_store_fields(memory, frame, 4294964168, 0, 16, True)\nframe = _personnel_store_fields(memory, frame, 4294964170, frame.data[3] & 65535)\nframe = _personnel_read_fields(memory, frame, 0, 4294964134)\nframe = frame.with_address(0, 4294951680)\nframe = _personnel_read_fields(memory, frame, 1, _personnel_indexed_address(frame, 0, 0), 8)\nframe = _personnel_ext_word_fields(memory, frame, 1)\nframe = _personnel_arithmetic_fields(memory, frame, 1, frame.data[3] & 65535)\nframe = _personnel_compare_fields(memory, frame, frame.data[1] & 65535, 100)\nif not frame.status_word & 5:\n    frame = _personnel_load_fields(memory, frame, 2, frame.data[1] & 65535)\n    frame = _personnel_arithmetic_fields(memory, frame, 2, 100, 16, True)\n    frame = _personnel_memory_arithmetic_fields(memory, frame, 4294964170, frame.data[2] & 65535, 16, True)\n    frame = _personnel_load_fields(memory, frame, 1, 100)\nframe = _personnel_store_fields(memory, frame, _personnel_indexed_address(frame, 0, 0), frame.data[1] & 255, 8)\nframe = _personnel_read_fields(memory, frame, 0, 4294964784)\nframe = _personnel_compare_fields(memory, frame, frame.data[0] & 65535, memory.state.read(4294964134, 2))\nif frame.status_word & 4:\n    frame = _personnel_read_fields(memory, frame, 0, 4294964788)\nframe = frame.with_address(0, 4294951424)\nframe = _personnel_read_fields(memory, frame, 1, _personnel_indexed_address(frame, 0, 0), 8)\nframe = _personnel_arithmetic_fields(memory, frame, 1, 1, 8)\nframe = _personnel_compare_fields(memory, frame, frame.data[1] & 255, 100, 8)\nif not frame.status_word & 5:\n    frame = _personnel_load_fields(memory, frame, 1, 100, 8)\nframe = _personnel_store_fields(memory, frame, _personnel_indexed_address(frame, 0, 0), frame.data[1] & 255, 8)\nframe = _personnel_shift_fields(memory, frame, 0, 1)\nframe = frame.with_address(0, 4294950400)\nframe = _personnel_shift_fields(memory, frame, 3, 1, 16, True)\nframe = _personnel_arithmetic_fields(memory, frame, 3, memory.state.read(_personnel_indexed_address(frame, 0, 0), 2))\nframe = _personnel_compare_fields(memory, frame, frame.data[3] & 65535, 999)\nif not frame.status_word & 5:\n    frame = _personnel_load_fields(memory, frame, 3, 999)\nframe = _personnel_store_fields(memory, frame, _personnel_indexed_address(frame, 0, 0), frame.data[3] & 65535)\nframe = frame.with_address(0, 4294954240)\nframe = _personnel_read_fields(memory, frame, 0, 4294964134)\nframe = _personnel_store_fields(memory, frame, _personnel_indexed_address(frame, 0, 0), 1, 8)\nframe, visible = _personnel_visible_force_fields(memory, frame)\nif visible:\n    frame = _personnel_store_fields(memory, frame, 16740390, 22)\n    value = memory.state.read(4294964170, 2)\n    frame = _personnel_test_fields(memory, frame, value)\n    frame = _personnel_load_fields(memory, frame, 0, 168 if frame.status_word & 4 else 167)\n    frame = _personnel_store_fields(memory, frame, 4294964222, frame.data[0] & 65535)\n    frame = _personnel_store_fields(memory, frame, 4294964754, memory.state.read(4294964106, 2))\n    frame = _personnel_store_fields(memory, frame, 4294964754, memory.state.read(4294964106, 2))\n    frame = _personnel_store_fields(memory, frame, 4294964066, 40)\n    frame = _personnel_store_fields(memory, frame, 4294964176, memory.state.read(4294964134, 2))\nreturn memory.finish(frame)'}, '_personnel_relationship_progress_fields': {'signature': 'memory, frame, carrier, bonus, head, random_token', 'returns': None, 'flow': 'frame = _personnel_call_fields(memory, frame, 33748, random_token)\nframe = _personnel_load_fields(memory, frame, carrier, 0, 32)\nframe = _personnel_read_fields(memory, frame, carrier, 4294964764)\nframe = _personnel_load_fields(memory, frame, 1, frame.data[carrier], 32)\nframe = _personnel_shift_fields(memory, frame, carrier, 1, 32)\nframe = _personnel_arithmetic_fields(memory, frame, carrier, frame.data[1], 32)\nif bonus in (5, 10):\n    frame = _personnel_shift_fields(memory, frame, carrier, 1, 32)\nframe = _personnel_swap_fields(memory, frame, carrier)\nframe = _personnel_arithmetic_fields(memory, frame, carrier, bonus)\nif head:\n    frame = _personnel_read_fields(memory, frame, 1, 4294964086)\n    frame = _personnel_shift_fields(memory, frame, 1, 1)\n    frame = frame.with_address(0, 4294960704)\n    frame = _personnel_read_fields(memory, frame, 0 if carrier == 2 else 2, _personnel_indexed_address(frame, 0, 1))\n    slot = 0 if carrier == 2 else 2\n    frame = _personnel_shift_fields(memory, frame, slot, 1)\nelse:\n    slot = 2\n    frame = _personnel_read_fields(memory, frame, slot, 4294964134)\n    frame = _personnel_shift_fields(memory, frame, slot, 1)\nframe = frame.with_address(0, 4294950400)\nframe = _personnel_arithmetic_fields(memory, frame, carrier, memory.state.read(_personnel_indexed_address(frame, 0, slot), 2))\nframe = _personnel_compare_fields(memory, frame, frame.data[carrier] & 65535, 999)\nif not frame.status_word & 5:\n    frame = _personnel_load_fields(memory, frame, carrier, 999)\nreturn _personnel_store_fields(memory, frame, _personnel_indexed_address(frame, 0, slot), frame.data[carrier] & 65535)'}, 'execute_mutual_officer_relationship_reward_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_read_fields(memory, frame, 0, 4294964134)\nframe = frame.with_address(0, 4294952704)\nframe = _personnel_read_fields(memory, frame, 1, _personnel_indexed_address(frame, 0, 0), 8)\nframe = _personnel_and_fields(memory, frame, 1, 7, 8)\nframe = _personnel_ext_word_fields(memory, frame, 1)\nframe = _personnel_load_fields(memory, frame, 3, frame.data[1] & 65535)\nframe = _personnel_arithmetic_fields(memory, frame, 3, 2)\nframe = frame.with_address(0, 60508)\nframe = _personnel_read_fields(memory, frame, 2, _personnel_indexed_address(frame, 0, 1), 8)\nframe = _personnel_ext_word_fields(memory, frame, 2)\nframe = _personnel_load_fields(memory, frame, 1, 0, 32)\nframe = _personnel_read_fields(memory, frame, 1, 4294964764)\nframe = _personnel_product_fields(memory, frame, 1, frame.data[3] & 65535)\nframe = _personnel_swap_fields(memory, frame, 1)\nframe = _personnel_arithmetic_fields(memory, frame, 1, frame.data[2] & 65535)\nframe = _personnel_shift_fields(memory, frame, 0, 1)\nframe = frame.with_address(0, 4294948352)\nframe = _personnel_read_fields(memory, frame, 2, _personnel_indexed_address(frame, 0, 0))\nframe = _personnel_product_fields(memory, frame, 1, frame.data[2] & 65535)\nframe = _personnel_read_fields(memory, frame, 0, 4294964086)\nframe = _personnel_shift_fields(memory, frame, 0, 1)\nframe = frame.with_address(0, 4294960704)\nframe = _personnel_read_fields(memory, frame, 2, _personnel_indexed_address(frame, 0, 0))\nframe = frame.with_address(0, 4294951424)\nframe = _personnel_load_fields(memory, frame, 3, 0)\nframe = _personnel_read_fields(memory, frame, 3, _personnel_indexed_address(frame, 0, 2), 8)\nframe = _personnel_load_fields(memory, frame, 2, 120)\nframe = _personnel_arithmetic_fields(memory, frame, 2, frame.data[3] & 65535, 16, True)\nframe = _personnel_quotient_fields(memory, frame, 1, frame.data[2] & 65535, 60048)\nframe = _personnel_compare_fields(memory, frame, frame.data[1] & 65535, 10)\nif not frame.status_word & 1:\n    frame = _personnel_call_fields(memory, frame, 60438, 60062)\n    frame = _personnel_store_fields(memory, frame, 4294964222, 38)\n    frame = _personnel_store_fields(memory, frame, 4294964176, memory.state.read(4294964134, 2))\n    frame = _personnel_relationship_progress_fields(memory, frame, 0, 5, True, 60080)\n    frame = _personnel_relationship_progress_fields(memory, frame, 0, 10, False, 60144)\nelse:\n    frame = _personnel_store_fields(memory, frame, 4294964222, 40)\n    frame = _personnel_relationship_progress_fields(memory, frame, 2, 1, True, 60210)\n    frame = _personnel_call_fields(memory, frame, 33748, 60272)\n    frame = _personnel_load_fields(memory, frame, 2, 0, 32)\n    frame = _personnel_read_fields(memory, frame, 2, 4294964764)\n    frame = _personnel_load_fields(memory, frame, 1, frame.data[2], 32)\n    frame = _personnel_shift_fields(memory, frame, 2, 1, 32)\n    frame = _personnel_arithmetic_fields(memory, frame, 2, frame.data[1], 32)\n    frame = _personnel_swap_fields(memory, frame, 2)\n    frame = _personnel_arithmetic_fields(memory, frame, 2, 1)\n    frame = _personnel_call_fields(memory, frame, 33748, 60294)\n    frame = _personnel_load_fields(memory, frame, 3, 0, 32)\n    frame = _personnel_read_fields(memory, frame, 3, 4294964764)\n    frame = _personnel_load_fields(memory, frame, 1, frame.data[3], 32)\n    frame = _personnel_shift_fields(memory, frame, 3, 1, 32)\n    frame = _personnel_arithmetic_fields(memory, frame, 3, frame.data[1], 32)\n    frame = _personnel_swap_fields(memory, frame, 3)\n    frame = _personnel_read_fields(memory, frame, 1, 4294964134)\n    frame = frame.with_address(0, 4294951424)\n    address = _personnel_indexed_address(frame, 0, 1)\n    frame = _personnel_memory_arithmetic_fields(memory, frame, address, frame.data[3] & 255, 8, True)\n    if frame.status_word & 1:\n        frame = _personnel_store_fields(memory, frame, address, 0, 8, True)\n    frame = _personnel_shift_fields(memory, frame, 1, 1)\n    frame = frame.with_address(0, 4294950400)\n    frame = _personnel_arithmetic_fields(memory, frame, 2, memory.state.read(_personnel_indexed_address(frame, 0, 1), 2))\n    frame = _personnel_compare_fields(memory, frame, frame.data[2] & 65535, 999)\n    if not frame.status_word & 5:\n        frame = _personnel_load_fields(memory, frame, 2, 999)\n    frame = _personnel_store_fields(memory, frame, _personnel_indexed_address(frame, 0, 1), frame.data[2] & 65535)\nframe, visible = _personnel_visible_force_fields(memory, frame)\nif visible:\n    frame = _personnel_store_fields(memory, frame, 16740390, 12)\n    frame = _personnel_store_fields(memory, frame, 4294964754, 520)\n    frame = _personnel_store_fields(memory, frame, 4294964066, 40)\n    frame = _personnel_load_fields(memory, frame, 0, 37)\n    frame = _personnel_store_fields(memory, frame, 4294964176, memory.state.read(4294964134, 2))\n    frame = _personnel_call_fields(memory, frame, 423666, 60416)\n    frame = _personnel_read_fields(memory, frame, 0, 4294964134)\n    frame = frame.with_address(0, 4294954240)\n    frame = _personnel_store_fields(memory, frame, _personnel_indexed_address(frame, 0, 0), 1, 8)\nframe = _personnel_store_fields(memory, frame, 4294964744, 120)\nreturn memory.finish(frame)'}, 'execute_officer_policy_outcome_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_store_fields(memory, frame, 4294964168, 0, 32, True)\nframe = frame.with_address(0, 4294953984)\nframe = _personnel_read_fields(memory, frame, 0, 4294964210)\nframe = _personnel_read_fields(memory, frame, 0, _personnel_indexed_address(frame, 0, 0), 8)\nframe = frame.with_address(0, 4294964263)\nframe = _personnel_read_fields(memory, frame, 0, _personnel_indexed_address(frame, 0, 0), 8)\nframe = frame.with_address(0, 4294960704)\nframe = _personnel_shift_fields(memory, frame, 0, 1)\nframe = _personnel_read_fields(memory, frame, 0, _personnel_indexed_address(frame, 0, 0))\nframe = _personnel_compare_fields(memory, frame, frame.data[0] & 65535, memory.state.read(4294964210, 2))\nfailed = bool(frame.status_word & 4)\nif not failed:\n    frame = _personnel_read_fields(memory, frame, 0, 4294964210)\n    frame = frame.with_address(0, 4294951680)\n    frame = _personnel_read_fields(memory, frame, 1, _personnel_indexed_address(frame, 0, 0), 8)\n    failed = bool(frame.status_word & 4)\nif not failed:\n    frame = _personnel_ext_word_fields(memory, frame, 1)\n    frame = _personnel_arithmetic_fields(memory, frame, 1, 50, 16, True)\n    if frame.status_word & 1:\n        frame, absolute = _command_binary_fields(memory, frame, 0, frame.data[1] & 65535, 16, True)\n        frame = frame.with_data(1, absolute, 16)\n    frame = _personnel_load_fields(memory, frame, 2, 60)\n    frame = _personnel_arithmetic_fields(memory, frame, 2, frame.data[1] & 65535, 16, True)\n    frame = _personnel_read_fields(memory, frame, 1, 4294964134)\n    frame = frame.with_address(1, 4294952704)\n    frame = _personnel_read_fields(memory, frame, 3, _personnel_indexed_address(frame, 1, 1), 8)\n    frame = _personnel_and_fields(memory, frame, 3, 7)\n    frame = _personnel_read_fields(memory, frame, 3, u32(60945 + s16(frame.data[3] & 65535)), 8)\n    frame = _personnel_load_fields(memory, frame, 4, 0, 32)\n    frame = _personnel_read_fields(memory, frame, 4, 4294964764)\n    frame = _personnel_load_fields(memory, frame, 5, frame.data[4], 32)\n    frame = _personnel_shift_fields(memory, frame, 4, 2, 32)\n    frame = _personnel_arithmetic_fields(memory, frame, 4, frame.data[5], 32)\n    frame = _personnel_shift_fields(memory, frame, 4, 2, 32)\n    frame = _personnel_swap_fields(memory, frame, 4)\n    frame = _personnel_arithmetic_fields(memory, frame, 4, frame.data[3] & 65535)\n    frame = _personnel_shift_fields(memory, frame, 1, 1)\n    frame = frame.with_address(0, 4294948352)\n    frame = _personnel_read_fields(memory, frame, 3, _personnel_indexed_address(frame, 0, 1))\n    frame = _personnel_arithmetic_fields(memory, frame, 3, frame.data[4] & 65535)\n    frame = _personnel_read_fields(memory, frame, 0, 4294964210)\n    frame = frame.with_address(0, 4294952704)\n    frame = _personnel_read_fields(memory, frame, 1, _personnel_indexed_address(frame, 0, 0), 8)\n    frame = _personnel_and_fields(memory, frame, 1, 7)\n    frame = frame.with_address(1, 60940)\n    frame = _personnel_read_fields(memory, frame, 4, _personnel_indexed_address(frame, 1, 1), 8)\n    frame = _personnel_shift_fields(memory, frame, 0, 1)\n    frame = frame.with_address(1, 4294948352)\n    frame = _personnel_arithmetic_fields(memory, frame, 4, memory.state.read(_personnel_indexed_address(frame, 1, 0), 2))\n    frame = _personnel_arithmetic_fields(memory, frame, 3, frame.data[4] & 65535, 16, True)\n    failed = bool(frame.status_word & 1)\nif not failed:\n    frame = _personnel_product_fields(memory, frame, 2, frame.data[3] & 65535, True)\n    frame = frame.with_address(1, 57096)\n    frame = _personnel_read_fields(memory, frame, 3, 4294963154)\n    frame = _personnel_shift_fields(memory, frame, 3, 1)\n    frame = _personnel_quotient_fields(memory, frame, 2, memory.state.read(_personnel_indexed_address(frame, 1, 3), 2), 61126)\n    frame = _personnel_test_fields(memory, frame, frame.data[2] & 65535)\n    failed = bool(frame.status_word & 4)\nif failed:\n    frame = _personnel_call_fields(memory, frame, 61312, 61196)\n    frame = _personnel_call_fields(memory, frame, 61348, 61200)\n    frame = _personnel_call_fields(memory, frame, 61410, 61204)\n    frame = _personnel_store_fields(memory, frame, 4294964222, 58)\nelse:\n    frame = _personnel_compare_fields(memory, frame, frame.data[2] & 65535, 40)\n    if not frame.status_word & 5:\n        frame = _personnel_load_fields(memory, frame, 2, 40)\n    frame = _personnel_store_fields(memory, frame, 4294964168, 0, 16, True)\n    frame = _personnel_store_fields(memory, frame, 4294964170, frame.data[2] & 65535)\n    frame = _personnel_read_fields(memory, frame, 0, 4294964210)\n    frame = frame.with_address(0, 4294951680)\n    address = _personnel_indexed_address(frame, 0, 0)\n    frame = _personnel_memory_arithmetic_fields(memory, frame, address, frame.data[2] & 255, 8, True)\n    if frame.status_word & 1:\n        frame = _personnel_store_fields(memory, frame, address, 0, 8, True)\n    frame = _personnel_call_fields(memory, frame, 61280, 61176)\n    frame = _personnel_store_fields(memory, frame, 4294964178, memory.state.read(4294964210, 2))\n    frame = _personnel_store_fields(memory, frame, 4294964222, 57)\nframe, visible = _personnel_visible_force_fields(memory, frame)\nif visible:\n    frame = _personnel_store_fields(memory, frame, 4294964106, 520)\n    frame = _personnel_store_fields(memory, frame, 4294964066, 40)\n    frame = _personnel_store_fields(memory, frame, 4294964744, 120)\n    frame = _personnel_store_fields(memory, frame, 4294964754, 520)\n    frame = _personnel_store_fields(memory, frame, 4294964176, memory.state.read(4294964134, 2))\n    frame = _personnel_load_fields(memory, frame, 0, 9)\n    frame = _personnel_call_fields(memory, frame, 423666, 61278)\nreturn memory.finish(frame)'}, 'reduce_selected_officer_disposition_randomly_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_call_fields(memory, frame, 33748, 61318)\nframe = _personnel_and_fields(memory, frame, 0, 65535, 32)\nframe = _personnel_shift_fields(memory, frame, 0, 2, 32)\nframe = _personnel_swap_fields(memory, frame, 0)\nframe = _personnel_read_fields(memory, frame, 1, 4294964134)\nframe = frame.with_address(0, 4294951424)\naddress = _personnel_indexed_address(frame, 0, 1)\nframe = _personnel_memory_arithmetic_fields(memory, frame, address, frame.data[0] & 255, 8, True)\nif frame.status_word & 1:\n    frame = _personnel_store_fields(memory, frame, address, 0, 8, True)\nreturn memory.finish(frame)'}, 'reduce_chosen_force_head_disposition_randomly_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_call_fields(memory, frame, 33748, 61354)\nframe = _personnel_and_fields(memory, frame, 0, 65535, 32)\nframe = _personnel_load_fields(memory, frame, 1, frame.data[0], 32)\nframe = _personnel_shift_fields(memory, frame, 0, 1, 32)\nframe = _personnel_arithmetic_fields(memory, frame, 0, frame.data[1], 32)\nframe = _personnel_swap_fields(memory, frame, 0)\nframe = _personnel_read_fields(memory, frame, 1, 4294964114)\nframe = frame.with_address(0, 4294964263)\nframe = _personnel_read_fields(memory, frame, 1, _personnel_indexed_address(frame, 0, 1), 8)\nframe = _personnel_and_fields(memory, frame, 1, 15)\nframe = _personnel_shift_fields(memory, frame, 1, 1)\nframe = frame.with_address(0, 4294960704)\nframe = _personnel_read_fields(memory, frame, 1, _personnel_indexed_address(frame, 0, 1))\nframe = frame.with_address(0, 4294951424)\naddress = _personnel_indexed_address(frame, 0, 1)\nframe = _personnel_memory_arithmetic_fields(memory, frame, address, frame.data[0] & 255, 8, True)\nif frame.status_word & 1:\n    frame = _personnel_store_fields(memory, frame, address, 0, 8, True)\nreturn memory.finish(frame)'}, 'credit_selected_officer_policy_progress_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_call_fields(memory, frame, 33748, 61416)\nframe = _personnel_load_fields(memory, frame, 0, 0, 32)\nframe = _personnel_read_fields(memory, frame, 0, 4294964764)\nframe = _personnel_load_fields(memory, frame, 1, frame.data[0], 32)\nframe = _personnel_shift_fields(memory, frame, 0, 1, 32)\nframe = _personnel_arithmetic_fields(memory, frame, 0, frame.data[1], 32)\nframe = _personnel_swap_fields(memory, frame, 0)\nframe = _personnel_arithmetic_fields(memory, frame, 0, 1)\nframe = _personnel_read_fields(memory, frame, 1, 4294964134)\nframe = _personnel_shift_fields(memory, frame, 1, 1)\nframe = frame.with_address(0, 4294950400)\nframe = _personnel_progress_cap_fields(memory, frame, _personnel_indexed_address(frame, 0, 1), frame.data[0] & 65535)\nreturn memory.finish(frame)'}, 'score_selected_officer_recruitment_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_read_fields(memory, frame, 0, 4294964134)\nframe = _personnel_shift_fields(memory, frame, 0, 1)\nframe = frame.with_address(0, 4294950912)\nframe = _personnel_load_fields(memory, frame, 2, 0, 32)\nframe = _personnel_read_fields(memory, frame, 2, _personnel_indexed_address(frame, 0, 0))\nframe = _personnel_quotient_fields(memory, frame, 2, 10, 63466)\nframe = frame.with_address(0, 4294948352)\nframe = _personnel_arithmetic_fields(memory, frame, 2, memory.state.read(_personnel_indexed_address(frame, 0, 0), 2))\nframe = _personnel_call_fields(memory, frame, 33748, 63484)\nframe = frame.with_address(0, 57102)\nframe = _personnel_read_fields(memory, frame, 1, 4294963154)\nframe = _personnel_shift_fields(memory, frame, 1, 2)\nframe = _personnel_product_fields(memory, frame, 0, memory.state.read(_personnel_indexed_address(frame, 0, 1), 2))\nframe = _personnel_swap_fields(memory, frame, 0)\nframe = _personnel_arithmetic_fields(memory, frame, 0, memory.state.read(_personnel_indexed_address(frame, 0, 1, 2), 2))\nframe = _personnel_arithmetic_fields(memory, frame, 2, frame.data[0] & 65535)\nframe = _personnel_read_fields(memory, frame, 0, 4294964136)\nframe = _personnel_shift_fields(memory, frame, 0, 1)\nframe = frame.with_address(0, 4294964318)\nframe = _personnel_read_fields(memory, frame, 0, _personnel_indexed_address(frame, 0, 0))\nframe = _personnel_shift_fields(memory, frame, 0, 1)\nframe = frame.with_address(0, 4294948352)\nframe = _personnel_arithmetic_fields(memory, frame, 2, memory.state.read(_personnel_indexed_address(frame, 0, 0), 2), 16, True)\nreturn memory.finish(frame)'}, 'bucket_recruitment_score_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_load_fields(memory, frame, 3, 0)\nframe = _personnel_load_fields(memory, frame, 4, 0)\nframe = _personnel_test_fields(memory, frame, frame.data[2] & 65535)\nif frame.status_word & 12:\n    return memory.finish(frame)\nfor cutoff, threshold in ((50, 10), (100, 30), (150, 50), (200, 60), (250, 70), (300, 80), (350, 80)):\n    frame = _personnel_load_fields(memory, frame, 3, threshold)\n    frame = _personnel_arithmetic_fields(memory, frame, 4, 1)\n    frame = _personnel_compare_fields(memory, frame, frame.data[2] & 65535, cutoff)\n    if frame.status_word & 5:\n        return memory.finish(frame)\nframe = _personnel_load_fields(memory, frame, 3, 85)\nframe = _personnel_arithmetic_fields(memory, frame, 4, 1)\nframe = _personnel_load_fields(memory, frame, 2, 351)\nreturn memory.finish(frame)'}, 'draw_recruitment_probability_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_call_fields(memory, frame, 33748, 64230)\nframe = _personnel_and_fields(memory, frame, 0, 65535, 32)\nframe = _personnel_load_fields(memory, frame, 1, frame.data[0], 32)\nframe = _personnel_shift_fields(memory, frame, 0, 1, 32)\nframe = _personnel_arithmetic_fields(memory, frame, 0, frame.data[1], 32)\nframe = _personnel_shift_fields(memory, frame, 0, 3, 32)\nframe = _personnel_arithmetic_fields(memory, frame, 0, frame.data[1], 32)\nframe = _personnel_shift_fields(memory, frame, 0, 2, 32)\nframe = _personnel_swap_fields(memory, frame, 0)\nreturn memory.finish(frame)'}, '_personnel_recruitment_resource_fields': {'signature': 'memory, frame, resource', 'returns': None, 'flow': "if resource == 'food':\n    parameter, ledger, continuation = (64022, 4294959264, 63996)\nelif resource == 'gold':\n    parameter, ledger, continuation = (64102, 4294959104, 64076)\nelif resource == 'state':\n    parameter, ledger, continuation = (64188, 4294959584, 64156)\nelse:\n    raise ValueError('original three recruitment resource roles required')\nframe = _personnel_load_fields(memory, frame, 5, frame.data[4] & 65535)\nframe = _personnel_shift_fields(memory, frame, 5, 2)\nframe = frame.with_address(0, parameter)\nframe = _personnel_read_fields(memory, frame, 6, _personnel_indexed_address(frame, 0, 5))\nframe = _personnel_call_fields(memory, frame, 33748, continuation)\nframe = _personnel_product_fields(memory, frame, 0, frame.data[6] & 65535)\nframe = _personnel_swap_fields(memory, frame, 0)\nframe = _personnel_arithmetic_fields(memory, frame, 0, memory.state.read(_personnel_indexed_address(frame, 0, 5, 2), 2))\nframe = frame.with_address(0, ledger)\nframe = _personnel_read_fields(memory, frame, 1, _personnel_indexed_address(frame, 0, 2), 32)\nif resource == 'state':\n    frame = _personnel_load_fields(memory, frame, 3, frame.data[1] & 65535)\n    frame = _personnel_product_fields(memory, frame, 3, frame.data[0] & 65535)\n    frame = _personnel_quotient_fields(memory, frame, 3, 100, 64176)\n    frame = _personnel_and_fields(memory, frame, 3, 65535, 32)\nelse:\n    frame = _personnel_load_fields(memory, frame, 3, frame.data[1], 32)\n    frame = frame.with_data(3, divu_retained(frame.data[3], 100))\n    frame = _personnel_product_fields(memory, frame, 3, frame.data[0] & 65535)\nreturn _personnel_memory_arithmetic_fields(memory, frame, _personnel_indexed_address(frame, 0, 2), frame.data[3], 32, True)"}, 'reduce_recruitment_city_food_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': "frame = memory.enter(frame)\nreturn memory.finish(_personnel_recruitment_resource_fields(memory, frame, 'food'))"}, 'reduce_recruitment_city_gold_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': "frame = memory.enter(frame)\nreturn memory.finish(_personnel_recruitment_resource_fields(memory, frame, 'gold'))"}, 'reduce_recruitment_city_state_parameter_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': "frame = memory.enter(frame)\nreturn memory.finish(_personnel_recruitment_resource_fields(memory, frame, 'state'))"}, 'apply_recruitment_city_resource_losses_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_test_fields(memory, frame, frame.data[4] & 65535)\nif frame.status_word & 4:\n    return memory.finish(frame)\nframe = _personnel_read_fields(memory, frame, 2, 4294964136)\nframe = _personnel_arithmetic_fields(memory, frame, 2, 1, 16, True)\nframe = _personnel_shift_fields(memory, frame, 2, 2)\nframe = _personnel_call_fields(memory, frame, 63978, 63968)\nframe = _personnel_call_fields(memory, frame, 64058, 63972)\nframe = _personnel_call_fields(memory, frame, 64138, 63976)\nreturn memory.finish(frame)'}, 'apply_recruited_officer_roster_transition_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_read_fields(memory, frame, 0, 4294964134)\nframe = frame.with_address(0, 4294960704)\nframe = _personnel_load_fields(memory, frame, 3, 21)\nforce_head_found = False\nwhile True:\n    value = memory.state.read(frame.addresses[0], 2)\n    frame = frame.with_address(0, frame.addresses[0] + 2)\n    frame = _personnel_compare_fields(memory, frame, frame.data[0] & 65535, value)\n    if frame.status_word & 4:\n        force_head_found = True\n        break\n    frame, more_heads = _personnel_db_fields(frame, 3)\n    if not more_heads:\n        break\naward_progress = force_head_found\nif not force_head_found:\n    frame = _personnel_read_fields(memory, frame, 0, 4294964134)\n    frame = _personnel_shift_fields(memory, frame, 0, 1)\n    frame = frame.with_address(0, 4294947840)\n    frame = _personnel_read_fields(memory, frame, 3, _personnel_indexed_address(frame, 0, 0))\n    frame = _personnel_shift_fields(memory, frame, 3, 1, 16, True)\n    frame = _personnel_call_fields(memory, frame, 64224, 63680)\n    frame = _personnel_compare_fields(memory, frame, frame.data[0] & 65535, frame.data[3] & 65535)\n    award_progress = bool(frame.status_word & 1)\nif award_progress:\n    frame = _personnel_test_fields(memory, frame, frame.data[2] & 65535)\n    if frame.status_word & 8:\n        return memory.finish(frame)\n    frame = _personnel_and_fields(memory, frame, 2, 65535, 32)\n    frame = _personnel_quotient_fields(memory, frame, 2, 10, 63852)\n    frame = _personnel_read_fields(memory, frame, 0, 4294964134)\n    frame = _personnel_shift_fields(memory, frame, 0, 1)\n    frame = frame.with_address(0, 4294950912)\n    frame = _personnel_read_fields(memory, frame, 3, _personnel_indexed_address(frame, 0, 0))\n    frame = _personnel_arithmetic_fields(memory, frame, 3, frame.data[2] & 65535)\n    frame = _personnel_compare_fields(memory, frame, frame.data[3] & 65535, 999)\n    if not frame.status_word & 5:\n        frame = _personnel_load_fields(memory, frame, 3, 999)\n    frame = _personnel_store_fields(memory, frame, _personnel_indexed_address(frame, 0, 0), frame.data[3] & 65535)\n    return memory.finish(frame)\nframe = _personnel_read_fields(memory, frame, 0, 4294964136)\nframe = _personnel_store_fields(memory, frame, 4294964784, 65535)\nframe = _personnel_call_fields(memory, frame, 24392, 63702)\nframe = _personnel_compare_fields(memory, frame, frame.data[3] & 65535, 10)\nleave_city = not bool(frame.status_word & 1)\nif not leave_city:\n    frame = _personnel_read_fields(memory, frame, 0, 4294964134)\n    frame = frame.with_address(0, 4294951680)\n    frame = _personnel_load_fields(memory, frame, 1, 0)\n    frame = _personnel_read_fields(memory, frame, 1, _personnel_indexed_address(frame, 0, 0), 8)\n    frame = _personnel_load_fields(memory, frame, 2, 100)\n    frame = _personnel_arithmetic_fields(memory, frame, 2, frame.data[1] & 65535, 16, True)\n    frame = _personnel_read_fields(memory, frame, 1, 4294964136)\n    frame = _personnel_shift_fields(memory, frame, 1, 1)\n    frame = frame.with_address(0, 4294964318)\n    frame = _personnel_read_fields(memory, frame, 1, _personnel_indexed_address(frame, 0, 1))\n    frame = _personnel_load_fields(memory, frame, 0, 0)\n    frame = frame.with_address(0, 4294951424)\n    frame = _personnel_read_fields(memory, frame, 0, _personnel_indexed_address(frame, 0, 1), 8)\n    frame = _personnel_arithmetic_fields(memory, frame, 2, frame.data[0] & 65535)\n    frame = _personnel_compare_fields(memory, frame, frame.data[2] & 65535, 100)\n    if not frame.status_word & 1:\n        return memory.finish(frame)\n    frame = _personnel_call_fields(memory, frame, 64224, 63764)\n    frame = _personnel_compare_fields(memory, frame, frame.data[0] & 65535, frame.data[2] & 65535)\n    if frame.status_word & 1:\n        return memory.finish(frame)\nframe = _personnel_store_fields(memory, frame, 4294964222, 93)\nframe = _personnel_read_fields(memory, frame, 0, 4294964134)\nframe = frame.with_address(0, 4294953984)\nframe = _personnel_store_fields(memory, frame, _personnel_indexed_address(frame, 0, 0), 255, 8)\nframe = frame.with_address(0, 4294964318)\nframe = _personnel_read_fields(memory, frame, 0, 4294964114)\nframe = _personnel_shift_fields(memory, frame, 0, 1)\nframe = _personnel_read_fields(memory, frame, 1, 4294964134)\nframe = _personnel_compare_fields(memory, frame, frame.data[1] & 65535, memory.state.read(_personnel_indexed_address(frame, 0, 0), 2))\nif not frame.status_word & 4:\n    return memory.finish(frame)\nframe = _personnel_read_fields(memory, frame, 0, 4294964114)\nframe = _personnel_store_fields(memory, frame, 4294964784, 65535)\nframe = _personnel_call_fields(memory, frame, 24392, 63826)\nframe = _personnel_read_fields(memory, frame, 0, 4294964114)\nframe = _personnel_call_fields(memory, frame, 57846, 63834)\nreturn memory.finish(frame)'}, 'execute_officer_recruitment_outcome_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'frame = memory.enter(frame)\nframe = _personnel_call_fields(memory, frame, 63450, 63356)\nframe = _personnel_call_fields(memory, frame, 63532, 63360)\nframe = _personnel_call_fields(memory, frame, 64224, 63364)\nframe = _personnel_compare_fields(memory, frame, frame.data[0] & 65535, frame.data[3] & 65535)\nif not frame.status_word & 1:\n    frame = _personnel_store_fields(memory, frame, 4294964222, 58)\n    frame = _personnel_call_fields(memory, frame, 63638, 63378)\n    frame = _personnel_store_fields(memory, frame, 4294964744, 120)\n    frame = _personnel_store_fields(memory, frame, 4294964066, 31)\nelse:\n    frame = _personnel_store_fields(memory, frame, 4294964222, 60)\n    frame = _personnel_call_fields(memory, frame, 63888, 63402)\n    frame = _personnel_call_fields(memory, frame, 63952, 63406)\n    frame = _personnel_store_fields(memory, frame, 16740390, 3)\n    frame = _personnel_store_fields(memory, frame, 4294964066, 40)\nframe = _personnel_store_fields(memory, frame, 4294964754, 520)\nframe = _personnel_load_fields(memory, frame, 0, 9)\nframe = _personnel_store_fields(memory, frame, 4294964176, memory.state.read(4294964134, 2))\nframe = _personnel_call_fields(memory, frame, 423666, 63442)\nframe = _personnel_store_fields(memory, frame, 4294964744, 120)\nreturn memory.finish(frame)'}})
APPROVED.setdefault('contexts_personnel',set()).update(['CommandFrame', 'PersonnelMemory', '_command_binary_fields', '_personnel_and_fields', '_personnel_arithmetic_fields', '_personnel_call_fields', '_personnel_compare_fields', '_personnel_db_fields', '_personnel_ext_word_fields', '_personnel_indexed_address', '_personnel_legacy_entry', '_personnel_load_fields', '_personnel_memory_arithmetic_fields', '_personnel_product_fields', '_personnel_quotient_fields', '_personnel_read_fields', '_personnel_shift_fields', '_personnel_store_fields', '_personnel_swap_fields', '_personnel_test_fields'])
APPROVED.setdefault('domain',set()).update({'Boundary'})
APPROVED.setdefault('business_reuse',set()).update({'_personnel_progress_cap_fields'})
