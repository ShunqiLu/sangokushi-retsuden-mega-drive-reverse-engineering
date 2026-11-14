"""Restricted semantic source admission with ordinary mnemonic lowering.

Explicit business text only; this is an intermediate structural compiler,
not arbitrary Python compilation or full natural-gameplay acceptance.
"""
from .compiler_common import CompileError,semantic_functions,lower_declared
from .target import DUEL_BINDINGS

APPROVED={'contexts_duel': {'DuelCompleteTurnOutcome',
                   'DuelConditionObservation',
                   'DuelControlContext',
                   'DuelRuleFrame',
                   'DuelSpacingResult',
                   'DuelTurnContext',
                   'DuelTurnFrame',
                   'DuelTurnOutcome',
                   'checked_duel_context',
                   'checked_duel_turn'},
 'dataclasses': {'replace'},
 'domain': {'Boundary',
            'Long',
            'SceneState',
            'StackContinuation',
            'Table',
            'Word',
            'checked_state',
            'checked_table',
            'high16',
            'low16',
            'low8',
            'negative_word',
            'replace_byte',
            'replace_word',
            'stitched_product',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'},
 'services': {'choose_duel_status_text',
              'clear_duel_text_plane',
              'divide_duel_frame',
              'duel_complete_service',
              'ram_view',
              'sample_random_pair',
              'unsigned_divmod',
              'wait_active_duel_action',
              'wait_either_duel_action'}}

DECLARATIONS={'_arithmetic': {'flow': 'mask = (1 << bits) - 1\n'
                         'left, right = (left & mask, right & mask)\n'
                         'value = (left - right if subtract else left + right) & mask\n'
                         'carry = left < right if subtract else left + right > mask\n'
                         'overflow = bool((left ^ right if subtract else ~(left ^ right)) & '
                         '(left ^ value) & 1 << bits - 1)\n'
                         'return DuelConditionObservation(carry, value == 0, bool(value & 1 '
                         '<< bits - 1), overflow)',
                 'returns': '',
                 'signature': 'left, right, bits=32, *, subtract=False',
                 'slots': {}},
 '_choose_ai_rule': {'flow': 'checked_duel_context(context, state)\n'
                             "if _ram(state, 'efd2').word() == 0:\n"
                             '    source = state.table(easy).cursor()\n'
                             "elif _ram(state, 'efd2').word() == 2:\n"
                             '    source = state.table(hard).cursor()\n'
                             'else:\n'
                             '    source = state.table(normal).cursor()\n'
                             'if threshold >= context.actor.word(28):\n'
                             '    source = source.advance(2)\n'
                             'profile = u16(context.actor.word(12) << 2)\n'
                             'source = source.at(profile)\n'
                             'frame = _sample(state, context.frame)\n'
                             'selected = low16(frame.command) & 1\n'
                             'if selected:\n'
                             '    source = source.advance(1)\n'
                             'command = replace_word(frame.command, 0)\n'
                             'command = replace_byte(command, source.byte())\n'
                             'context.actor.set_word(36, low16(command))\n'
                             'return _values(frame, command=command, lookup=source, '
                             'conditions=_logic(low16(command), 16))',
                     'returns': '',
                     'signature': 'state, context, threshold, easy, normal, hard',
                     'slots': {}},
 '_clear': {'flow': 'if frame.live is None:\n'
                    "    raise Boundary('complete text clear requires actual current "
                    "values')\n"
                    'return _from_live(duel_complete_service(state, frame.live, '
                    "'clear_duel_text_complete'))",
            'returns': '',
            'signature': 'state, frame',
            'slots': {}},
 '_divide_frame': {'flow': 'child = replace(frame, stack=frame.stack.advance(-4))\n'
                           'result = divide_duel_frame(state, child)\n'
                           'return replace(result, stack=result.stack.advance(4))',
                   'returns': '',
                   'signature': 'state, frame',
                   'slots': {}},
 '_frame_clear': {'flow': 'return _clear(state, _from_live(frame)).live',
                  'returns': '',
                  'signature': 'state, frame',
                  'slots': {}},
 '_frame_message': {'flow': 'return _message(state, _from_live(frame), selection).live',
                    'returns': '',
                    'signature': 'state, frame, selection',
                    'slots': {}},
 '_frame_wait': {'flow': 'return _wait(state, _from_live(frame), either=either).live',
                 'returns': '',
                 'signature': 'state, frame, *, either=False',
                 'slots': {}},
 '_from_live': {'flow': 'return DuelRuleFrame(frame.command, frame.comparison, '
                        'frame.distance, frame.factor, frame.weapon_difference, '
                        'frame.variation, frame)',
                'returns': '',
                'signature': 'frame',
                'slots': {}},
 '_full': {'flow': 'checked_duel_context(context, state)\n'
                   'if context.frame.live is None:\n'
                   "    raise Boundary('action requires actual current "
                   "D5/response/A2/entry-SP, not a six-value observation')\n"
                   'return checked_duel_turn(context.frame.live, state)',
           'returns': '',
           'signature': 'context, state',
           'slots': {}},
 '_guarded_motion': {'flow': 'frame = _sample(state, frame)\n'
                             'command = low16(frame.command) & 31\n'
                             'frame = _values(frame, command=replace_word(frame.command, '
                             'command))\n'
                             'if command:\n'
                             '    frame = _try_special(state, context, frame)\n'
                             '    if low16(frame.command):\n'
                             '        return frame\n'
                             'return _motion(state, context, frame, 1024 if '
                             'negative_word(low16(frame.factor)) else 2048)',
                     'returns': '',
                     'signature': 'state, context, frame',
                     'slots': {}},
 '_legacy_turn': {'flow': 'return DuelTurnOutcome(_from_live(result.frame), '
                          'result.discarded_continuation)',
                  'returns': '',
                  'signature': 'result',
                  'slots': {}},
 '_logic': {'flow': 'value &= (1 << bits) - 1\n'
                    'return DuelConditionObservation(False, value == 0, bool(value & 1 << '
                    'bits - 1), False)',
            'returns': '',
            'signature': 'value, bits=32',
            'slots': {}},
 '_message': {'flow': 'if frame.live is not None:\n'
                      '    return _from_live(duel_complete_service(state, frame.live, '
                      "'choose_duel_status_text_complete', uint(selection, 16)))\n"
                      'command = choose_duel_status_text(state, uint(selection, 16), '
                      'frame.command)\n'
                      'return _values(frame, command=command)',
              'returns': '',
              'signature': 'state, frame, selection',
              'slots': {}},
 '_motion': {'flow': 'frame = _values(frame, command=replace_word(frame.command, command))\n'
                     'return _orient_and_gate_duel_motion(state, context, frame)',
             'returns': '',
             'signature': 'state, context, frame, command',
             'slots': {}},
 '_nonlocal_complete': {'flow': 'command = frame.stack.long()\n'
                                'frame = replace(frame, command=command, '
                                'stack=frame.stack.advance(4), conditions=_logic(command))\n'
                                'return DuelCompleteTurnOutcome(frame, '
                                'StackContinuation(command))',
                        'returns': '',
                        'signature': 'frame',
                        'slots': {}},
 '_orient_and_gate_duel_motion': {'flow': 'command = low16(frame.command)\n'
                                          'if not context.actor.byte(24) & 8:\n'
                                          '    command ^= 3072\n'
                                          'stack = None if frame.live is None else '
                                          'frame.live.stack.advance(-2)\n'
                                          'if stack is not None:\n'
                                          '    stack.set_word(0, command)\n'
                                          'sample = sample_random_pair(state)\n'
                                          'comparison = replace_word(sample.updated_state, '
                                          'low16(sample.sample) & 14)\n'
                                          'saved_command = command if stack is None else '
                                          'stack.word()\n'
                                          'command = replace_word(sample.sample, '
                                          'saved_command)\n'
                                          'if low16(comparison) == 0:\n'
                                          '    command = replace_word(command, 0)\n'
                                          'conditions = _logic(0, 16) if low16(comparison) == '
                                          '0 else _logic(low16(comparison), 16)\n'
                                          'return _values(frame, command=command, '
                                          'comparison=comparison, conditions=conditions)',
                                  'returns': '',
                                  'signature': 'state, context, frame',
                                  'slots': {}},
 '_pop_long': {'flow': 'value = frame.stack.long()\n'
                       'return replace(frame, **{name: value}, stack=frame.stack.advance(4))',
               'returns': '',
               'signature': 'frame, name',
               'slots': {}},
 '_pressure_motion': {'flow': 'if negative_word(low16(frame.factor)):\n'
                              '    frame = _try_special(state, context, frame)\n'
                              '    return _motion(state, context, frame, low16(frame.command) '
                              '| 1024)\n'
                              'frame = _sample(state, frame)\n'
                              'frame = _values(frame, command=replace_word(frame.command, '
                              'low16(frame.command) & 1))\n'
                              'if low16(frame.command):\n'
                              '    frame = _try_special(state, context, frame)\n'
                              'return _motion(state, context, frame, low16(frame.command) | '
                              '2048)',
                      'returns': '',
                      'signature': 'state, context, frame',
                      'slots': {}},
 '_push_long': {'flow': 'stack = frame.stack.advance(-4)\n'
                        'stack.set_long(0, value)\n'
                        'return replace(frame, stack=stack)',
                'returns': '',
                'signature': 'frame, value',
                'slots': {}},
 '_ram': {'flow': "return ram_view(state, 'ram_' + low)",
          'returns': '',
          'signature': 'state, low',
          'slots': {}},
 '_recover_after_duel_attack': {'flow': 'frame = _sample(state, _from_live(frame)).live\n'
                                        'frame = replace(frame, '
                                        'command=replace_word(frame.command, '
                                        '(low16(frame.command) & 1) + 37))\n'
                                        'if _second_turn(state):\n'
                                        '    frame = replace(frame, '
                                        'command=replace_word(frame.command, '
                                        'u16(low16(frame.command) - 29)))\n'
                                        'frame = _frame_message(state, frame, '
                                        'low16(frame.command))\n'
                                        'frame = toggle_duel_turn_complete(state, frame)\n'
                                        'frame = _frame_wait(state, frame)\n'
                                        'frame = toggle_duel_turn_complete(state, frame)\n'
                                        'timer = frame.opponent.word(40)\n'
                                        'if timer < 300:\n'
                                        '    frame.opponent.set_word(40, 300)\n'
                                        '    conditions = _logic(300, 16)\n'
                                        'else:\n'
                                        '    conditions = _arithmetic(timer, 300, 16, '
                                        'subtract=True)\n'
                                        'return DuelCompleteTurnOutcome(replace(frame, '
                                        'conditions=conditions))',
                                'returns': '',
                                'signature': 'state, frame',
                                'slots': {}},
 '_sample': {'flow': 'sample = sample_random_pair(state)\n'
                     'return _values(frame, command=sample.sample, '
                     'comparison=sample.updated_state, '
                     'conditions=_logic(sample.updated_state))',
             'returns': '',
             'signature': 'state, frame',
             'slots': {}},
 '_second_turn': {'flow': "return negative_word(_ram(state, '7018').word())",
                  'returns': '',
                  'signature': 'state',
                  'slots': {}},
 '_toggle': {'flow': "value = _ram(state, '700a').byte()\n"
                     'if value == 3:\n'
                     '    return _arithmetic(value, 3, 8, subtract=True)\n'
                     "value = _ram(state, '700b').byte()\n"
                     'if value == 3:\n'
                     '    return _arithmetic(value, 3, 8, subtract=True)\n'
                     "result = _ram(state, '7018').word() ^ 32768\n"
                     "_ram(state, '7018').set_word(0, result)\n"
                     'return _logic(result, 16)',
             'returns': '',
             'signature': 'state',
             'slots': {}},
 '_try_special': {'flow': 'return choose_duel_opponent_special(state, replace(context, '
                          'frame=frame))',
                  'returns': '',
                  'signature': 'state, context, frame',
                  'slots': {}},
 '_values': {'flow': 'live = frame.live\n'
                     'if live is not None:\n'
                     '    live = replace(live, **changes)\n'
                     'projection = {name: value for name, value in changes.items() if name in '
                     "('command', 'comparison', 'distance', 'factor', 'weapon_difference', "
                     "'variation')}\n"
                     'return replace(frame, **projection, live=live)',
             'returns': '',
             'signature': 'frame, **changes',
             'slots': {}},
 '_wait': {'flow': 'if frame.live is None:\n'
                   "    raise Boundary('complete action wait requires the actual current "
                   "frame')\n"
                   "name = 'wait_either_duel_action_complete' if either else "
                   "'wait_active_duel_action_complete'\n"
                   'return _from_live(duel_complete_service(state, frame.live, name))',
           'returns': '',
           'signature': 'state, frame, *, either=False',
           'slots': {}},
 '_weight_fields': {'flow': 'if value < 65536:\n'
                            '    product = low16(value) * factor\n'
                            '    return (product, response, _logic(product))\n'
                            'lower_product = low16(value) * factor\n'
                            'response = swap_words(u32(high16(value) * factor))\n'
                            'product = u32(lower_product + response)\n'
                            'return (product, response, _arithmetic(lower_product, response))',
                    'returns': '',
                    'signature': 'value, factor, response',
                    'slots': {}},
 '_weight_frame': {'flow': 'product, response, conditions = _weight_fields(frame.comparison, '
                           'low16(frame.factor), frame.response)\n'
                           'return replace(frame, comparison=product, response=response, '
                           'conditions=conditions)',
                   'returns': '',
                   'signature': 'state, frame',
                   'slots': {}},
 'choose_duel_aggressive_rule': {'flow': 'return _choose_ai_rule(state, context, 70, 172958, '
                                         '172970, 172982)',
                                 'returns': 'DuelRuleFrame',
                                 'signature': 'state: SceneState, context: DuelTurnContext',
                                 'slots': {}},
 'choose_duel_balanced_rule': {'flow': 'return _choose_ai_rule(state, context, 60, 173132, '
                                       '173144, 173156)',
                               'returns': 'DuelRuleFrame',
                               'signature': 'state: SceneState, context: DuelTurnContext',
                               'slots': {}},
 'choose_duel_balanced_rule_alias': {'flow': 'return choose_duel_balanced_rule(state, '
                                             'context)',
                                     'returns': 'DuelRuleFrame',
                                     'signature': 'state: SceneState, context: '
                                                  'DuelTurnContext',
                                     'slots': {}},
 'choose_duel_cautious_rule': {'flow': 'return _choose_ai_rule(state, context, 50, 173222, '
                                       '173234, 173246)',
                               'returns': 'DuelRuleFrame',
                               'signature': 'state: SceneState, context: DuelTurnContext',
                               'slots': {}},
 'choose_duel_cautious_rule_alias': {'flow': 'return choose_duel_cautious_rule(state, '
                                             'context)',
                                     'returns': 'DuelRuleFrame',
                                     'signature': 'state: SceneState, context: '
                                                  'DuelTurnContext',
                                     'slots': {}},
 'choose_duel_opponent_special': {'flow': 'checked_duel_context(context, state)\n'
                                          'frame = _values(context.frame, '
                                          'command=replace_word(context.frame.command, 0), '
                                          'conditions=_logic(0, 16))\n'
                                          'if not context.opponent.byte(2) & 128:\n'
                                          '    return _values(frame, conditions=_logic(0, '
                                          '16))\n'
                                          'spacing = measure_duel_spacing(state, '
                                          'replace(context, frame=frame))\n'
                                          'frame = spacing.frame\n'
                                          'if not spacing.borrowed:\n'
                                          '    return frame\n'
                                          'offset = u16((context.opponent.word(2) & 3) << 1)\n'
                                          'command = state.table(174682).word(offset) | 8192\n'
                                          'return _values(frame, '
                                          'command=replace_word(frame.command, command), '
                                          'conditions=_logic(command, 16))',
                                  'returns': 'DuelRuleFrame',
                                  'signature': 'state: SceneState, context: DuelTurnContext',
                                  'slots': {}},
 'choose_duel_pressure_rule': {'flow': 'return _choose_ai_rule(state, context, 60, 173044, '
                                       '173056, 173068)',
                               'returns': 'DuelRuleFrame',
                               'signature': 'state: SceneState, context: DuelTurnContext',
                               'slots': {}},
 'choose_duel_random_motion': {'flow': 'checked_duel_context(context, state)\n'
                                       'frame = _sample(state, context.frame)\n'
                                       'command = low16(frame.command) & 768\n'
                                       'if command == 768:\n'
                                       '    command = 0\n'
                                       'return _values(frame, '
                                       'command=replace_word(frame.command, command | 16), '
                                       'conditions=_logic(command | 16, 16))',
                               'returns': 'DuelRuleFrame',
                               'signature': 'state: SceneState, context: DuelTurnContext',
                               'slots': {}},
 'execute_duel_aggressive_rule': {'flow': 'checked_duel_context(context, state)\n'
                                          'if context.opponent.byte(2) & 128:\n'
                                          '    frame = choose_duel_random_motion(state, '
                                          'context)\n'
                                          '    return _motion(state, context, frame, '
                                          'low16(frame.command) | 2048)\n'
                                          'spacing = measure_duel_spacing(state, context)\n'
                                          'if spacing.borrowed:\n'
                                          '    return _motion(state, context, spacing.frame, '
                                          '1024)\n'
                                          'return _pressure_motion(state, context, '
                                          'spacing.frame)',
                                  'returns': 'DuelRuleFrame',
                                  'signature': 'state: SceneState, context: DuelTurnContext',
                                  'slots': {}},
 'execute_duel_balanced_rule': {'flow': 'checked_duel_context(context, state)\n'
                                        'spacing = measure_duel_spacing(state, context)\n'
                                        'frame = spacing.frame\n'
                                        'if not spacing.borrowed:\n'
                                        '    return _motion(state, context, frame, 1024 if '
                                        'negative_word(low16(frame.factor)) else 2048)\n'
                                        'if negative_word(low16(frame.factor)) or '
                                        'low16(frame.distance) < 65533:\n'
                                        '    return _motion(state, context, frame, 1024)\n'
                                        'frame = _sample(state, frame)\n'
                                        'frame = _values(frame, '
                                        'command=replace_word(frame.command, '
                                        'low16(frame.command) & 1))\n'
                                        'if low16(frame.command):\n'
                                        '    return _try_special(state, context, frame)\n'
                                        'return _guarded_motion(state, context, frame)',
                                'returns': 'DuelRuleFrame',
                                'signature': 'state: SceneState, context: DuelTurnContext',
                                'slots': {}},
 'execute_duel_balanced_rule_alias': {'flow': 'return execute_duel_balanced_rule(state, '
                                              'context)',
                                      'returns': 'DuelRuleFrame',
                                      'signature': 'state: SceneState, context: '
                                                   'DuelTurnContext',
                                      'slots': {}},
 'execute_duel_cautious_rule': {'flow': 'checked_duel_context(context, state)\n'
                                        'frame = _sample(state, context.frame)\n'
                                        'command = low16(frame.command) & 63\n'
                                        'frame = _values(frame, '
                                        'command=replace_word(frame.command, command))\n'
                                        'if command:\n'
                                        '    frame = _try_special(state, context, frame)\n'
                                        '    if low16(frame.command):\n'
                                        '        return frame\n'
                                        'spacing = measure_duel_spacing(state, '
                                        'replace(context, frame=frame))\n'
                                        'frame = spacing.frame\n'
                                        'if not spacing.borrowed:\n'
                                        '    return _guarded_motion(state, context, frame)\n'
                                        'if not negative_word(low16(frame.factor)) and '
                                        'low16(frame.distance) >= 65533:\n'
                                        '    return choose_duel_random_motion(state, '
                                        'replace(context, frame=frame))\n'
                                        'frame = _try_special(state, context, frame)\n'
                                        'if low16(frame.command):\n'
                                        '    return frame\n'
                                        'return _motion(state, context, frame, 1024)',
                                'returns': 'DuelRuleFrame',
                                'signature': 'state: SceneState, context: DuelTurnContext',
                                'slots': {}},
 'execute_duel_cautious_rule_alias': {'flow': 'return execute_duel_cautious_rule(state, '
                                              'context)',
                                      'returns': 'DuelRuleFrame',
                                      'signature': 'state: SceneState, context: '
                                                   'DuelTurnContext',
                                      'slots': {}},
 'execute_duel_pressure_rule': {'flow': 'checked_duel_context(context, state)\n'
                                        'spacing = measure_duel_spacing(state, context)\n'
                                        'if spacing.borrowed and (not '
                                        'negative_word(low16(spacing.frame.factor))):\n'
                                        '    return choose_duel_random_motion(state, '
                                        'replace(context, frame=spacing.frame))\n'
                                        'return _pressure_motion(state, context, '
                                        'spacing.frame)',
                                'returns': 'DuelRuleFrame',
                                'signature': 'state: SceneState, context: DuelTurnContext',
                                'slots': {}},
 'finish_special_duel_action': {'flow': 'return '
                                        '_legacy_turn(finish_special_duel_action_complete(state, '
                                        '_full(context, state)))',
                                'returns': 'DuelTurnOutcome',
                                'signature': 'state: SceneState, context: DuelTurnContext',
                                'slots': {}},
 'finish_special_duel_action_complete': {'flow': 'checked_duel_turn(frame, state)\n'
                                                 'frame = _sample(state, '
                                                 '_from_live(frame)).live\n'
                                                 'roll = low16(frame.command) & 3\n'
                                                 'frame = replace(frame, command=0 if roll == '
                                                 '3 else replace_word(frame.command, roll))\n'
                                                 'selection = low16(frame.command) + 24\n'
                                                 'if _second_turn(state):\n'
                                                 '    selection = u16(selection - 24 + 41)\n'
                                                 'frame = _frame_message(state, frame, '
                                                 'selection)\n'
                                                 'frame = _frame_wait(state, frame)\n'
                                                 'frame.actor.set_byte(2, frame.actor.byte(2) '
                                                 '| 8)\n'
                                                 'frame = _frame_clear(state, frame)\n'
                                                 'frame = _frame_message(state, frame, 27 if '
                                                 '_second_turn(state) else 28)\n'
                                                 'frame = toggle_duel_turn_complete(state, '
                                                 'frame)\n'
                                                 'frame = _frame_wait(state, frame)\n'
                                                 'frame = toggle_duel_turn_complete(state, '
                                                 'frame)\n'
                                                 'frame = _frame_clear(state, frame)\n'
                                                 'frame = _frame_message(state, frame, 30 if '
                                                 '_second_turn(state) else 29)\n'
                                                 'frame = _frame_wait(state, frame, '
                                                 'either=True)\n'
                                                 "_ram(state, '70f0').set_word(0, 256)\n"
                                                 'if _second_turn(state):\n'
                                                 "    _ram(state, '70f0').set_word(0, 1)\n"
                                                 'return _nonlocal_complete(frame)',
                                         'returns': '',
                                         'signature': 'state, frame',
                                         'slots': {}},
 'flee_duel': {'flow': 'return _legacy_turn(flee_duel_complete(state, _full(context, state)))',
               'returns': 'DuelTurnOutcome',
               'signature': 'state: SceneState, context: DuelTurnContext',
               'slots': {}},
 'flee_duel_complete': {'flow': 'checked_duel_turn(frame, state)\n'
                                'frame = _sample(state, _from_live(frame)).live\n'
                                'selection = (low16(frame.command) & 1) + 20\n'
                                'if _second_turn(state):\n'
                                '    selection = u16(selection - 20 + 44)\n'
                                'frame = _frame_message(state, frame, selection)\n'
                                'frame = _frame_wait(state, frame)\n'
                                'frame = _frame_clear(state, frame)\n'
                                'frame = _frame_message(state, frame, 23 if '
                                '_second_turn(state) else 22)\n'
                                'frame = _frame_wait(state, frame, either=True)\n'
                                "_ram(state, '70f0').set_word(0, 768)\n"
                                'if _second_turn(state):\n'
                                "    _ram(state, '70f0').set_word(0, 3)\n"
                                'return _nonlocal_complete(frame)',
                        'returns': '',
                        'signature': 'state, frame',
                        'slots': {}},
 'measure_duel_spacing': {'flow': 'checked_duel_context(context, state)\n'
                                  'actor, opponent, frame = (context.actor, context.opponent, '
                                  'context.frame)\n'
                                  'profile = u16(opponent.word(12) << 1)\n'
                                  'distance = u16(state.table(172640).word(profile) + 8)\n'
                                  'if not opponent.byte(24) & 8:\n'
                                  '    distance = u16(-distance)\n'
                                  'distance = u16(distance + opponent.word(14))\n'
                                  'distance = u16(distance - actor.word(14))\n'
                                  'if negative_word(distance):\n'
                                  '    distance = u16(-distance)\n'
                                  'deduction = state.table(172692).word(profile)\n'
                                  'borrowed = distance < deduction\n'
                                  'frame = _values(frame, '
                                  'comparison=replace_word(frame.comparison, profile), '
                                  'distance=replace_word(frame.distance, u16(distance - '
                                  'deduction)), conditions=_arithmetic(distance, deduction, '
                                  '16, subtract=True))\n'
                                  'return DuelSpacingResult(frame, borrowed)',
                          'returns': 'DuelSpacingResult',
                          'signature': 'state: SceneState, context: DuelTurnContext',
                          'slots': {}},
 'multiply_duel_weight': {'flow': 'checked_state(state)\n'
                                  'uint(value, 32)\n'
                                  'uint(factor, 16)\n'
                                  'return _weight_fields(value, factor, None)[0]',
                          'returns': 'Long',
                          'signature': 'state: SceneState, value: Long, factor: Word',
                          'slots': {}},
 'perform_duel_feint': {'flow': 'return _legacy_turn(perform_duel_feint_complete(state, '
                                '_full(context, state)))',
                        'returns': 'DuelTurnOutcome',
                        'signature': 'state: SceneState, context: DuelTurnContext',
                        'slots': {}},
 'perform_duel_feint_complete': {'flow': 'checked_duel_turn(frame, state)\n'
                                         'frame = _sample(state, _from_live(frame)).live\n'
                                         'roll = low16(frame.command) & 3\n'
                                         'frame = replace(frame, '
                                         'command=replace_word(frame.command, 0 if roll == 3 '
                                         'else roll))\n'
                                         'selection = u16(low16(frame.command) + 14)\n'
                                         'if _second_turn(state):\n'
                                         '    selection = u16(selection - 14 + 46)\n'
                                         'frame = _frame_message(state, frame, selection)\n'
                                         'frame = _frame_wait(state, frame)\n'
                                         'frame = _frame_clear(state, frame)\n'
                                         'frame = _sample(state, _from_live(frame)).live\n'
                                         'roll = low16(frame.command) & 3\n'
                                         'frame = replace(frame, '
                                         'command=replace_word(frame.command, 0 if roll == 3 '
                                         'else roll))\n'
                                         'selection = u16(low16(frame.command) + 49)\n'
                                         'if _second_turn(state):\n'
                                         '    selection = u16(selection - 49 + 17)\n'
                                         'frame = _frame_message(state, frame, selection)\n'
                                         'frame = toggle_duel_turn_complete(state, frame)\n'
                                         'frame = _frame_wait(state, frame)\n'
                                         'frame = toggle_duel_turn_complete(state, frame)\n'
                                         'frame.opponent.set_word(40, 900)\n'
                                         'return DuelCompleteTurnOutcome(replace(frame, '
                                         'conditions=_logic(900, 16)))',
                                 'returns': '',
                                 'signature': 'state, frame',
                                 'slots': {}},
 'prepare_duel_combat_statistics': {'flow': 'frame = _full(context, state)\n'
                                            'actor, opponent = (frame.actor, frame.opponent)\n'
                                            'own, other = (low16(frame.command), '
                                            'low16(frame.comparison))\n'
                                            'opponent.set_byte(57, _ram(state, '
                                            "'c300').byte(other))\n"
                                            'opponent.set_byte(51, _ram(state, '
                                            "'c200').byte(other))\n"
                                            'opponent.set_byte(51, u8(opponent.byte(51) + '
                                            '1))\n'
                                            'actor.set_byte(51, _ram(state, '
                                            "'c200').byte(own))\n"
                                            'actor.set_byte(51, u8(actor.byte(51) + 1))\n'
                                            'own_offset, other_offset = (u16(own << 1), '
                                            'u16(other << 1))\n'
                                            'opponent.set_word(52, opponent.word(28))\n'
                                            'opponent.set_word(54, _ram(state, '
                                            "'b000').word(other_offset))\n"
                                            'opponent.set_word(48, _ram(state, '
                                            "'b600').word(other_offset))\n"
                                            'actor.set_word(48, _ram(state, '
                                            "'b600').word(own_offset))\n"
                                            'own = actor.word(26)\n'
                                            'other = opponent.word(26)\n'
                                            'working = replace_byte(frame.working_value, '
                                            "_ram(state, 'c700').byte(own))\n"
                                            'working = replace_word(working, low16(working) & '
                                            '15)\n'
                                            'response = replace_byte(frame.response, '
                                            "_ram(state, 'c700').byte(other))\n"
                                            'response = replace_word(response, '
                                            'low16(response) & 15)\n'
                                            'difference = u16(low16(working) - '
                                            'low16(response))\n'
                                            'return _from_live(replace(frame, '
                                            'command=replace_word(frame.command, own), '
                                            'comparison=replace_word(frame.comparison, '
                                            'other), working_value=replace_word(working, '
                                            'difference), response=response, '
                                            'conditions=_arithmetic(low16(working), '
                                            'low16(response), 16, subtract=True)))',
                                    'returns': 'DuelRuleFrame',
                                    'signature': 'state: SceneState, context: DuelTurnContext',
                                    'slots': {}},
 'resolve_duel_attack': {'flow': 'return _legacy_turn(resolve_duel_attack_complete(state, '
                                 '_full(context, state)))',
                         'returns': 'DuelTurnOutcome',
                         'signature': 'state: SceneState, context: DuelTurnContext',
                         'slots': {}},
 'resolve_duel_attack_complete': {'flow': 'checked_duel_turn(frame, state)\n'
                                          'own_id = frame.actor.word(26)\n'
                                          'frame = replace(frame, '
                                          'command=replace_word(frame.command, 6), '
                                          'comparison=replace_word(frame.comparison, '
                                          'own_id))\n'
                                          'if own_id == frame.actor.word(32):\n'
                                          '    frame = replace(frame, '
                                          'command=replace_word(frame.command, 7))\n'
                                          'if _second_turn(state):\n'
                                          '    frame = replace(frame, '
                                          'command=replace_word(frame.command, 35))\n'
                                          '    own_id = frame.actor.word(26)\n'
                                          '    frame = replace(frame, '
                                          'comparison=replace_word(frame.comparison, '
                                          'own_id))\n'
                                          '    if own_id == frame.actor.word(32):\n'
                                          '        frame = replace(frame, '
                                          'command=replace_word(frame.command, 36))\n'
                                          'frame = _frame_message(state, frame, '
                                          'low16(frame.command))\n'
                                          'frame = _frame_wait(state, frame)\n'
                                          'frame = _frame_clear(state, frame)\n'
                                          'frame = replace(frame, '
                                          'command=replace_word(frame.command, '
                                          'frame.actor.word(26)), '
                                          'comparison=replace_word(frame.comparison, '
                                          'frame.opponent.word(26)))\n'
                                          'frame = prepare_duel_combat_statistics(state, '
                                          'DuelTurnContext(frame.actor, frame.opponent, '
                                          '_from_live(frame))).live\n'
                                          'frame = replace(frame, '
                                          'command=replace_word(frame.command, '
                                          'frame.opponent.word(56)))\n'
                                          'frame = replace(frame, comparison=u16(100 - '
                                          'low16(frame.command)) * frame.actor.word(48), '
                                          'factor=replace_word(frame.factor, '
                                          'frame.actor.word(50)))\n'
                                          'frame = _weight_frame(state, frame)\n'
                                          'frame = replace(frame, '
                                          'factor=replace_word(frame.factor, '
                                          'frame.opponent.word(54)))\n'
                                          'frame = _weight_frame(state, frame)\n'
                                          'frame = _push_long(frame, frame.comparison)\n'
                                          'frame = replace(frame, '
                                          'comparison=frame.opponent.word(48) * '
                                          'frame.opponent.word(50), '
                                          'factor=replace_word(frame.factor, '
                                          'frame.opponent.word(52)))\n'
                                          'frame = _weight_frame(state, frame)\n'
                                          "if _ram(state, 'efd2').word() == 0:\n"
                                          '    difficulty = 60\n'
                                          "elif _ram(state, 'efd2').word() == 2:\n"
                                          '    difficulty = 100\n'
                                          'else:\n'
                                          '    difficulty = 80\n'
                                          'frame = replace(frame, '
                                          'factor=replace_word(frame.factor, difficulty))\n'
                                          'frame = _weight_frame(state, frame)\n'
                                          'frame = replace(frame, distance=frame.comparison)\n'
                                          "frame = _pop_long(frame, 'comparison')\n"
                                          'while True:\n'
                                          '    frame = _push_long(frame, frame.comparison)\n'
                                          '    frame = _sample(state, '
                                          '_from_live(frame)).live\n'
                                          "    frame = _pop_long(frame, 'comparison')\n"
                                          '    difference = low16(frame.working_value)\n'
                                          '    frame = replace(frame, '
                                          'factor=replace_word(frame.factor, difference))\n'
                                          '    if difference == 0 or '
                                          'negative_word(difference):\n'
                                          '        selected = low16(frame.command) & 7\n'
                                          '        frame = replace(frame, '
                                          'command=replace_word(frame.command, selected))\n'
                                          '        if selected > 4:\n'
                                          '            continue\n'
                                          '        difference = u16(-difference)\n'
                                          '        frame = replace(frame, '
                                          'working_value=replace_word(frame.working_value, '
                                          'difference))\n'
                                          '        variation = '
                                          'u16(state.table(161376).byte(difference) + '
                                          'selected) & 255\n'
                                          '    else:\n'
                                          '        selected = low16(frame.command) & 15\n'
                                          '        frame = replace(frame, '
                                          'command=replace_word(frame.command, selected))\n'
                                          '        if selected > 8:\n'
                                          '            continue\n'
                                          '        variation = '
                                          'u16(state.table(161404).byte(difference) + '
                                          'selected)\n'
                                          '    frame = replace(frame, variation=variation, '
                                          'factor=replace_word(frame.factor, variation))\n'
                                          '    break\n'
                                          'frame = _weight_frame(state, frame)\n'
                                          'frame = _push_long(frame, frame.distance)\n'
                                          'frame = replace(frame, distance=10)\n'
                                          'frame = _divide_frame(state, frame)\n'
                                          "frame = _pop_long(frame, 'distance')\n"
                                          'if frame.distance != 0:\n'
                                          '    frame = _divide_frame(state, frame)\n'
                                          '    if low16(frame.comparison) < 1:\n'
                                          '        return _recover_after_duel_attack(state, '
                                          'frame)\n'
                                          "blocked = _ram(state, 'ef7e' if "
                                          "_second_turn(state) else 'ef7f').byte()\n"
                                          'if blocked:\n'
                                          '    return _recover_after_duel_attack(state, '
                                          'frame)\n'
                                          'frame = _sample(state, _from_live(frame)).live\n'
                                          'frame = replace(frame, '
                                          'command=replace_word(frame.command, '
                                          '(low16(frame.command) & 1) + 39))\n'
                                          'if _second_turn(state):\n'
                                          '    frame = replace(frame, '
                                          'command=replace_word(frame.command, '
                                          'u16(low16(frame.command) - 39 + 10)))\n'
                                          'frame = _frame_message(state, frame, '
                                          'low16(frame.command))\n'
                                          'frame = toggle_duel_turn_complete(state, frame)\n'
                                          'frame = _frame_wait(state, frame)\n'
                                          'frame = toggle_duel_turn_complete(state, frame)\n'
                                          'command = replace_word(frame.command, '
                                          'frame.actor.word(24) & 63487)\n'
                                          'comparison = replace_word(frame.comparison, '
                                          'frame.opponent.word(24) & 2048)\n'
                                          'command = replace_word(command, low16(command) | '
                                          'low16(comparison))\n'
                                          'frame.opponent.set_word(24, low16(command))\n'
                                          'frame = _frame_clear(state, replace(frame, '
                                          'command=command, comparison=comparison))\n'
                                          'frame = _frame_message(state, frame, 12 if '
                                          '_second_turn(state) else 13)\n'
                                          'frame = _frame_wait(state, frame, either=True)\n'
                                          "_ram(state, '70f0').set_word(0, 2)\n"
                                          'if _second_turn(state):\n'
                                          "    _ram(state, '70f0').set_word(0, 512)\n"
                                          'return _nonlocal_complete(frame)',
                                  'returns': '',
                                  'signature': 'state, frame',
                                  'slots': {}},
 'toggle_duel_turn': {'flow': 'checked_state(state)\n_toggle(state)',
                      'returns': 'None',
                      'signature': 'state: SceneState',
                      'slots': {}},
 'toggle_duel_turn_complete': {'flow': 'checked_duel_turn(frame, state)\n'
                                       'return replace(frame, conditions=_toggle(state))',
                               'returns': '',
                               'signature': 'state, frame',
                               'slots': {}}}


def _lower_resolve_duel_attack(emitter,rules):
    emitter.segment(0x27576,0x2757a)
    emitter.ins('bra.w','scene_pc_027586',4)
    emitter.segment(0x27586,0x27660)
    emitter.ins('move.w','#0x6,%d0',4)
    emitter.ins('move.w','0x1a(%a0),%d1',4)
    emitter.ins('cmp.w','0x20(%a0),%d1',4)
    emitter.ins('bne.w','scene_pc_027598',4)
    emitter.ins('addq.w','#0x1,%d0',2)
    emitter.ins('tst.w','0xff7018:l',6)
    emitter.ins('bpl.b','scene_pc_0275b2',2)
    emitter.ins('move.w','#0x23,%d0',4)
    emitter.ins('move.w','0x1a(%a0),%d1',4)
    emitter.ins('cmp.w','0x20(%a0),%d1',4)
    emitter.ins('bne.w','scene_pc_0275b2',4)
    emitter.ins('addq.w','#0x1,%d0',2)
    emitter.ins('bsr.w','scene_pc_028228',4)
    emitter.ins('bsr.w','scene_pc_02777a',4)
    emitter.ins('bsr.w','scene_pc_027d76',4)
    emitter.ins('move.w','0x1a(%a0),%d0',4)
    emitter.ins('move.w','0x1a(%a1),%d1',4)
    emitter.ins('jsr','1310(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','0x38(%a1),%d0',4)
    emitter.ins('moveq','#100,%d1',2)
    emitter.ins('sub.w','%d0,%d1',2)
    emitter.ins('mulu.w','0x30(%a0),%d1',4)
    emitter.ins('move.w','0x32(%a0),%d3',4)
    emitter.ins('bsr.w','scene_pc_027abe',4)
    emitter.ins('move.w','0x36(%a1),%d3',4)
    emitter.ins('bsr.w','scene_pc_027abe',4)
    emitter.ins('movem.l','%d1,-(%a7)',4)
    emitter.ins('moveq','#0,%d1',2)
    emitter.ins('move.w','0x30(%a1),%d1',4)
    emitter.ins('mulu.w','0x32(%a1),%d1',4)
    emitter.ins('move.w','0x34(%a1),%d3',4)
    emitter.ins('bsr.w','scene_pc_027abe',4)
    emitter.ins('tst.w','0xefd2:w',4)
    emitter.ins('bne.w','scene_pc_02760e',4)
    emitter.ins('move.w','#0x3c,%d3',4)
    emitter.ins('bra.w','scene_pc_027624',4)
    emitter.ins('cmpi.w','#0x2,0xefd2:w',6)
    emitter.ins('beq.w','scene_pc_027620',4)
    emitter.ins('move.w','#0x50,%d3',4)
    emitter.ins('bra.w','scene_pc_027624',4)
    emitter.ins('move.w','#0x64,%d3',4)
    emitter.ins('bsr.w','scene_pc_027abe',4)
    emitter.ins('move.l','%d1,%d2',2)
    emitter.ins('movem.l','(%a7)+,%d1',4)
    emitter.ins('movem.l','%d1,-(%a7)',4)
    emitter.ins('jsr','scene_pc_0083d4:l',6)
    emitter.ins('movem.l','(%a7)+,%d1',4)
    emitter.ins('move.w','%d5,%d3',2)
    emitter.ins('beq.b','scene_pc_027644',2)
    emitter.ins('bpl.w','scene_pc_027666',4)
    emitter.ins('andi.w','#0x7,%d0',4)
    emitter.ins('cmpi.w','#0x4,%d0',4)
    emitter.ins('bhi.b','scene_pc_02762e',2)
    emitter.ins('neg.w','%d5',2)
    emitter.ins('moveq','#0,%d7',2)
    emitter.ins('move.b','12(%pc, %d5.w),%d7',4)
    emitter.ins('add.w','%d0,%d7',2)
    emitter.ins('andi.w','#0xff,%d7',4)
    emitter.ins('bra.w','scene_pc_027682',4)
    emitter.segment(0x27666,0x2767c)
    emitter.ins('andi.w','#0xf,%d0',4)
    emitter.ins('cmpi.w','#0x8,%d0',4)
    emitter.ins('bhi.b','scene_pc_02762e',2)
    emitter.ins('moveq','#0,%d7',2)
    emitter.ins('move.b','8(%pc, %d5.w),%d7',4)
    emitter.ins('add.w','%d0,%d7',2)
    emitter.ins('bra.w','scene_pc_027682',4)
    emitter.segment(0x27682,0x2777a)
    emitter.ins('move.w','%d7,%d3',2)
    emitter.ins('bsr.w','scene_pc_027abe',4)
    emitter.ins('movem.l','%d2,-(%a7)',4)
    emitter.ins('moveq','#10,%d2',2)
    emitter.ins('jsr','scene_pc_035760:l',6)
    emitter.ins('movem.l','(%a7)+,%d2',4)
    emitter.ins('tst.l','%d2',2)
    emitter.ins('beq.w','scene_pc_0276e6',4)
    emitter.ins('jsr','scene_pc_035760:l',6)
    emitter.ins('cmpi.w','#0x1,%d1',4)
    emitter.ins('bcc.w','scene_pc_0276e6',4)
    emitter.ins('jsr','scene_pc_0083d4:l',6)
    emitter.ins('andi.w','#0x1,%d0',4)
    emitter.ins('addi.w','#0x25,%d0',4)
    emitter.ins('tst.w','0xff7018:l',6)
    emitter.ins('bpl.b','scene_pc_0276c6',2)
    emitter.ins('subi.w','#0x1d,%d0',4)
    emitter.ins('bsr.w','scene_pc_028228',4)
    emitter.ins('bsr.w','scene_pc_027882',4)
    emitter.ins('bsr.w','scene_pc_02777a',4)
    emitter.ins('bsr.w','scene_pc_027882',4)
    emitter.ins('cmpi.w','#0x12c,0x28(%a1)',6)
    emitter.ins('bcc.b','scene_pc_0276e4',2)
    emitter.ins('move.w','#0x12c,0x28(%a1)',6)
    emitter.ins('rts','',2)
    emitter.ins('tst.w','0xff7018:l',6)
    emitter.ins('bpl.b','scene_pc_0276f8',2)
    emitter.ins('tst.b','0xef7e:w',4)
    emitter.ins('bne.b','scene_pc_0276ac',2)
    emitter.ins('bra.w','scene_pc_0276fe',4)
    emitter.ins('tst.b','0xef7f:w',4)
    emitter.ins('bne.b','scene_pc_0276ac',2)
    emitter.ins('jsr','scene_pc_0083d4:l',6)
    emitter.ins('andi.w','#0x1,%d0',4)
    emitter.ins('addi.w','#0x27,%d0',4)
    emitter.ins('tst.w','0xff7018:l',6)
    emitter.ins('bpl.b','scene_pc_02771c',2)
    emitter.ins('subi.w','#0x27,%d0',4)
    emitter.ins('addi.w','#0xa,%d0',4)
    emitter.ins('bsr.w','scene_pc_028228',4)
    emitter.ins('bsr.w','scene_pc_027882',4)
    emitter.ins('bsr.w','scene_pc_02777a',4)
    emitter.ins('bsr.w','scene_pc_027882',4)
    emitter.ins('move.w','0x18(%a0),%d0',4)
    emitter.ins('move.w','0x18(%a1),%d1',4)
    emitter.ins('andi.w','#0xf7ff,%d0',4)
    emitter.ins('andi.w','#0x800,%d1',4)
    emitter.ins('or.w','%d1,%d0',2)
    emitter.ins('move.w','%d0,0x18(%a1)',4)
    emitter.ins('bsr.w','scene_pc_027d76',4)
    emitter.ins('move.w','#0xd,%d0',4)
    emitter.ins('tst.w','0xff7018:l',6)
    emitter.ins('bpl.b','scene_pc_027754',2)
    emitter.ins('subq.w','#0x1,%d0',2)
    emitter.ins('bsr.w','scene_pc_028228',4)
    emitter.ins('bsr.w','scene_pc_0277b8',4)
    emitter.ins('move.w','#0x2,0xff70f0:l',8)
    emitter.ins('tst.w','0xff7018:l',6)
    emitter.ins('bpl.b','scene_pc_027774',2)
    emitter.ins('move.w','#0x200,0xff70f0:l',8)
    emitter.ins('move.l','(%a7)+,%d0',2)
    emitter.ins('bra.w','scene_pc_026d46',4)

def _lower_perform_duel_feint(emitter,rules):
    emitter.segment(0x2757a,0x2757e)
    emitter.ins('bra.w','scene_pc_027812',4)
    emitter.segment(0x27812,0x27882)
    emitter.ins('jsr','scene_pc_0083d4:l',6)
    emitter.ins('andi.w','#0x3,%d0',4)
    emitter.ins('cmpi.w','#0x3,%d0',4)
    emitter.ins('bne.b','scene_pc_027824',2)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('addi.w','#0xe,%d0',4)
    emitter.ins('tst.w','0xff7018:l',6)
    emitter.ins('bpl.b','scene_pc_027838',2)
    emitter.ins('subi.w','#0xe,%d0',4)
    emitter.ins('addi.w','#0x2e,%d0',4)
    emitter.ins('bsr.w','scene_pc_028228',4)
    emitter.ins('bsr.w','scene_pc_02777a',4)
    emitter.ins('bsr.w','scene_pc_027d76',4)
    emitter.ins('jsr','scene_pc_0083d4:l',6)
    emitter.ins('andi.w','#0x3,%d0',4)
    emitter.ins('cmpi.w','#0x3,%d0',4)
    emitter.ins('bne.b','scene_pc_027856',2)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('addi.w','#0x31,%d0',4)
    emitter.ins('tst.w','0xff7018:l',6)
    emitter.ins('bpl.b','scene_pc_02786a',2)
    emitter.ins('subi.w','#0x31,%d0',4)
    emitter.ins('addi.w','#0x11,%d0',4)
    emitter.ins('bsr.w','scene_pc_028228',4)
    emitter.ins('bsr.w','scene_pc_027882',4)
    emitter.ins('bsr.w','scene_pc_02777a',4)
    emitter.ins('bsr.w','scene_pc_027882',4)
    emitter.ins('move.w','#0x384,0x28(%a1)',6)
    emitter.ins('rts','',2)

def _lower_flee_duel(emitter,rules):
    emitter.segment(0x2757e,0x27582)
    emitter.ins('bra.w','scene_pc_0278a0',4)
    emitter.segment(0x278a0,0x278fe)
    emitter.ins('jsr','scene_pc_0083d4:l',6)
    emitter.ins('andi.w','#0x1,%d0',4)
    emitter.ins('addi.w','#0x14,%d0',4)
    emitter.ins('tst.w','0xff7018:l',6)
    emitter.ins('bpl.b','scene_pc_0278be',2)
    emitter.ins('subi.w','#0x14,%d0',4)
    emitter.ins('addi.w','#0x2c,%d0',4)
    emitter.ins('bsr.w','scene_pc_028228',4)
    emitter.ins('bsr.w','scene_pc_02777a',4)
    emitter.ins('bsr.w','scene_pc_027d76',4)
    emitter.ins('move.w','#0x16,%d0',4)
    emitter.ins('tst.w','0xff7018:l',6)
    emitter.ins('bpl.b','scene_pc_0278d8',2)
    emitter.ins('addq.w','#0x1,%d0',2)
    emitter.ins('bsr.w','scene_pc_028228',4)
    emitter.ins('bsr.w','scene_pc_0277b8',4)
    emitter.ins('move.w','#0x300,0xff70f0:l',8)
    emitter.ins('tst.w','0xff7018:l',6)
    emitter.ins('bpl.b','scene_pc_0278f8',2)
    emitter.ins('move.w','#0x3,0xff70f0:l',8)
    emitter.ins('move.l','(%a7)+,%d0',2)
    emitter.ins('bra.w','scene_pc_026d46',4)

def _lower_finish_special_duel_action(emitter,rules):
    emitter.segment(0x27582,0x27586)
    emitter.ins('bra.w','scene_pc_0278fe',4)
    emitter.segment(0x278fe,0x27990)
    emitter.ins('jsr','scene_pc_0083d4:l',6)
    emitter.ins('andi.w','#0x3,%d0',4)
    emitter.ins('cmpi.w','#0x3,%d0',4)
    emitter.ins('bne.w','scene_pc_027912',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('addi.w','#0x18,%d0',4)
    emitter.ins('tst.w','0xff7018:l',6)
    emitter.ins('bpl.b','scene_pc_027926',2)
    emitter.ins('subi.w','#0x18,%d0',4)
    emitter.ins('addi.w','#0x29,%d0',4)
    emitter.ins('bsr.w','scene_pc_028228',4)
    emitter.ins('bsr.w','scene_pc_02777a',4)
    emitter.ins('bset.b','#0x3,0x2(%a0)',6)
    emitter.ins('bsr.w','scene_pc_027d76',4)
    emitter.ins('move.w','#0x1c,%d0',4)
    emitter.ins('tst.w','0xff7018:l',6)
    emitter.ins('bpl.b','scene_pc_027948',2)
    emitter.ins('move.w','#0x1b,%d0',4)
    emitter.ins('bsr.w','scene_pc_028228',4)
    emitter.ins('bsr.w','scene_pc_027882',4)
    emitter.ins('bsr.w','scene_pc_02777a',4)
    emitter.ins('bsr.w','scene_pc_027882',4)
    emitter.ins('bsr.w','scene_pc_027d76',4)
    emitter.ins('move.w','#0x1d,%d0',4)
    emitter.ins('tst.w','0xff7018:l',6)
    emitter.ins('bpl.b','scene_pc_02796a',2)
    emitter.ins('addq.w','#0x1,%d0',2)
    emitter.ins('bsr.w','scene_pc_028228',4)
    emitter.ins('bsr.w','scene_pc_0277b8',4)
    emitter.ins('move.w','#0x100,0xff70f0:l',8)
    emitter.ins('tst.w','0xff7018:l',6)
    emitter.ins('bpl.b','scene_pc_02798a',2)
    emitter.ins('move.w','#0x1,0xff70f0:l',8)
    emitter.ins('move.l','(%a7)+,%d0',2)
    emitter.ins('bra.w','scene_pc_026d46',4)

def _lower_toggle_duel_turn(emitter,rules):
    emitter.segment(0x27882,0x278a0)
    emitter.ins('cmpi.b','#0x3,0xff700a:l',8)
    emitter.ins('beq.b','scene_pc_02789e',2)
    emitter.ins('cmpi.b','#0x3,0xff700b:l',8)
    emitter.ins('beq.b','scene_pc_02789e',2)
    emitter.ins('eori.w','#0x8000,0xff7018:l',8)
    emitter.ins('rts','',2)

def _lower_multiply_duel_weight(emitter,rules):
    emitter.segment(0x27abe,0x27ae6)
    emitter.ins('cmpi.l','#0x10000,%d1',6)
    emitter.ins('bcs.w','scene_pc_027ae2',4)
    emitter.ins('move.l','%d1,%d6',2)
    emitter.ins('andi.l','#0xffff,%d1',6)
    emitter.ins('mulu.w','%d3,%d1',2)
    emitter.ins('swap','%d6',2)
    emitter.ins('andi.l','#0xffff,%d6',6)
    emitter.ins('mulu.w','%d3,%d6',2)
    emitter.ins('swap','%d6',2)
    emitter.ins('add.l','%d6,%d1',2)
    emitter.ins('rts','',2)
    emitter.ins('mulu.w','%d3,%d1',2)
    emitter.ins('rts','',2)

def _lower_prepare_duel_combat_statistics(emitter,rules):
    emitter.segment(0x27ae6,0x27b58)
    emitter.ins('lea.l','0xc300:w,%a3',4)
    emitter.ins('lea.l','0xc200:w,%a5',4)
    emitter.ins('adda.w','%d1,%a3',2)
    emitter.ins('adda.w','%d1,%a5',2)
    emitter.ins('move.b','(%a3),0x39(%a1)',4)
    emitter.ins('move.b','(%a5),0x33(%a1)',4)
    emitter.ins('addq.b','#0x1,0x33(%a1)',4)
    emitter.ins('lea.l','0xc200:w,%a4',4)
    emitter.ins('adda.w','%d0,%a4',2)
    emitter.ins('move.b','(%a4),0x33(%a0)',4)
    emitter.ins('addq.b','#0x1,0x33(%a0)',4)
    emitter.ins('asl.w','#0x1,%d0',2)
    emitter.ins('asl.w','#0x1,%d1',2)
    emitter.ins('lea.l','0xb000:w,%a4',4)
    emitter.ins('lea.l','0xb600:w,%a5',4)
    emitter.ins('adda.w','%d1,%a4',2)
    emitter.ins('adda.w','%d1,%a5',2)
    emitter.ins('move.w','0x1c(%a1),0x34(%a1)',6)
    emitter.ins('move.w','(%a4),0x36(%a1)',4)
    emitter.ins('move.w','(%a5),0x30(%a1)',4)
    emitter.ins('lea.l','0xb600:w,%a3',4)
    emitter.ins('adda.w','%d0,%a3',2)
    emitter.ins('move.w','(%a3),0x30(%a0)',4)
    emitter.ins('move.w','0x1a(%a0),%d0',4)
    emitter.ins('move.w','0x1a(%a1),%d1',4)
    emitter.ins('lea.l','0xc700:w,%a3',4)
    emitter.ins('adda.w','%d0,%a3',2)
    emitter.ins('move.b','(%a3),%d5',2)
    emitter.ins('andi.w','#0xf,%d5',4)
    emitter.ins('lea.l','0xc700:w,%a3',4)
    emitter.ins('adda.w','%d1,%a3',2)
    emitter.ins('move.b','(%a3),%d6',2)
    emitter.ins('andi.w','#0xf,%d6',4)
    emitter.ins('sub.w','%d6,%d5',2)
    emitter.ins('rts','',2)

def _lower_measure_duel_spacing(emitter,rules):
    emitter.segment(0x2a26c,0x2a294)
    emitter.ins('move.w','0xc(%a1),%d1',4)
    emitter.ins('asl.w','#0x1,%d1',2)
    emitter.ins('move.w','-20(%pc, %d1.w),%d2',4)
    emitter.ins('addq.w','#0x8,%d2',2)
    emitter.ins('btst.b','#0x3,0x18(%a1)',6)
    emitter.ins('bne.b','scene_pc_02a282',2)
    emitter.ins('neg.w','%d2',2)
    emitter.ins('add.w','0xe(%a1),%d2',4)
    emitter.ins('sub.w','0xe(%a0),%d2',4)
    emitter.ins('bpl.b','scene_pc_02a28e',2)
    emitter.ins('neg.w','%d2',2)
    emitter.ins('sub.w','4(%pc, %d1.w),%d2',4)
    emitter.ins('rts','',2)

def _lower_choose_duel_cautious_rule(emitter,rules):
    emitter.segment(0x2a314,0x2a32c)
    emitter.ins('bra.w','scene_pc_02a470',4)
    emitter.ins('bra.w','scene_pc_02a470',4)
    emitter.ins('bra.w','scene_pc_02a418',4)
    emitter.ins('bra.w','scene_pc_02a418',4)
    emitter.ins('bra.w','scene_pc_02a3c2',4)
    emitter.ins('bra.w','scene_pc_02a344',4)
    emitter.segment(0x2a344,0x2a39e)
    emitter.ins('tst.w','0xefd2:w',4)
    emitter.ins('bne.w','scene_pc_02a356',4)
    emitter.ins('lea.l','80(%pc),%a2',4)
    emitter.ins('nop','',2)
    emitter.ins('bra.w','scene_pc_02a370',4)
    emitter.ins('cmpi.w','#0x2,0xefd2:w',6)
    emitter.ins('beq.w','scene_pc_02a36a',4)
    emitter.ins('lea.l','72(%pc),%a2',4)
    emitter.ins('nop','',2)
    emitter.ins('bra.w','scene_pc_02a370',4)
    emitter.ins('lea.l','74(%pc),%a2',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','#0x46,%d0',4)
    emitter.ins('cmp.w','0x1c(%a0),%d0',4)
    emitter.ins('bcs.b','scene_pc_02a37c',2)
    emitter.ins('addq.l','#0x2,%a2',2)
    emitter.ins('move.w','0xc(%a0),%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('lea.l','(%a2, %d0.w),%a2',4)
    emitter.ins('jsr','scene_pc_0083d4:l',6)
    emitter.ins('andi.w','#0x1,%d0',4)
    emitter.ins('beq.b','scene_pc_02a394',2)
    emitter.ins('addq.l','#0x1,%a2',2)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.b','(%a2),%d0',2)
    emitter.ins('move.w','%d0,0x24(%a0)',4)
    emitter.ins('rts','',2)
    emitter.segment(0x2a3c2,0x2a3f4)
    emitter.ins('tst.w','0xefd2:w',4)
    emitter.ins('bne.w','scene_pc_02a3d4',4)
    emitter.ins('lea.l','40(%pc),%a2',4)
    emitter.ins('nop','',2)
    emitter.ins('bra.w','scene_pc_02a3ee',4)
    emitter.ins('cmpi.w','#0x2,0xefd2:w',6)
    emitter.ins('beq.w','scene_pc_02a3e8',4)
    emitter.ins('lea.l','32(%pc),%a2',4)
    emitter.ins('nop','',2)
    emitter.ins('bra.w','scene_pc_02a3ee',4)
    emitter.ins('lea.l','34(%pc),%a2',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','#0x3c,%d0',4)
    emitter.ins('bra.b','scene_pc_02a374',2)
    emitter.segment(0x2a418,0x2a44c)
    emitter.ins('tst.w','0xefd2:w',4)
    emitter.ins('bne.w','scene_pc_02a42a',4)
    emitter.ins('lea.l','42(%pc),%a2',4)
    emitter.ins('nop','',2)
    emitter.ins('bra.w','scene_pc_02a444',4)
    emitter.ins('cmpi.w','#0x2,0xefd2:w',6)
    emitter.ins('beq.w','scene_pc_02a43e',4)
    emitter.ins('lea.l','34(%pc),%a2',4)
    emitter.ins('nop','',2)
    emitter.ins('bra.w','scene_pc_02a444',4)
    emitter.ins('lea.l','36(%pc),%a2',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','#0x3c,%d0',4)
    emitter.ins('bra.w','scene_pc_02a374',4)
    emitter.segment(0x2a470,0x2a4a4)
    emitter.ins('tst.w','0xefd2:w',4)
    emitter.ins('bne.w','scene_pc_02a482',4)
    emitter.ins('lea.l','44(%pc),%a2',4)
    emitter.ins('nop','',2)
    emitter.ins('bra.w','scene_pc_02a49c',4)
    emitter.ins('cmpi.w','#0x2,0xefd2:w',6)
    emitter.ins('beq.w','scene_pc_02a496',4)
    emitter.ins('lea.l','36(%pc),%a2',4)
    emitter.ins('nop','',2)
    emitter.ins('bra.w','scene_pc_02a49c',4)
    emitter.ins('lea.l','38(%pc),%a2',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','#0x32,%d0',4)
    emitter.ins('bra.w','scene_pc_02a374',4)

def _lower_execute_duel_cautious_rule(emitter,rules):
    emitter.segment(0x2a32c,0x2a344)
    emitter.ins('bra.w','scene_pc_02a4ca',4)
    emitter.ins('bra.w','scene_pc_02a542',4)
    emitter.ins('bra.w','scene_pc_02a542',4)
    emitter.ins('bra.w','scene_pc_02a4ca',4)
    emitter.ins('bra.w','scene_pc_02a5a0',4)
    emitter.ins('bra.w','scene_pc_02a5d2',4)
    emitter.segment(0x2a4ca,0x2a576)
    emitter.ins('jsr','scene_pc_0083d4:l',6)
    emitter.ins('andi.w','#0x3f,%d0',4)
    emitter.ins('beq.w','scene_pc_02a4dc',4)
    emitter.ins('bsr.w','scene_pc_02aa36',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('beq.b','scene_pc_02a4e2',2)
    emitter.ins('rts','',2)
    emitter.ins('bsr.w','scene_pc_02a22e',4)
    emitter.ins('bcc.b','scene_pc_02a506',2)
    emitter.ins('tst.w','%d3',2)
    emitter.ins('bmi.b','scene_pc_02a4f4',2)
    emitter.ins('cmpi.w','#0xfffd,%d2',4)
    emitter.ins('bcc.w','scene_pc_02a52a',4)
    emitter.ins('bsr.w','scene_pc_02aa36',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('beq.b','scene_pc_02a4fe',2)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0x400,%d0',4)
    emitter.ins('bra.w','scene_pc_02aa14',4)
    emitter.ins('jsr','scene_pc_0083d4:l',6)
    emitter.ins('andi.w','#0x1f,%d0',4)
    emitter.ins('beq.w','scene_pc_02a518',4)
    emitter.ins('bsr.w','scene_pc_02aa36',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('beq.b','scene_pc_02a51e',2)
    emitter.ins('rts','',2)
    emitter.ins('tst.w','%d3',2)
    emitter.ins('bmi.b','scene_pc_02a4f4',2)
    emitter.ins('move.w','#0x800,%d0',4)
    emitter.ins('bra.w','scene_pc_02aa14',4)
    emitter.ins('jsr','scene_pc_0083d4:l',6)
    emitter.ins('andi.w','#0x300,%d0',4)
    emitter.ins('cmpi.w','#0x300,%d0',4)
    emitter.ins('bne.b','scene_pc_02a53c',2)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('ori.w','#0x10,%d0',4)
    emitter.ins('rts','',2)
    emitter.ins('bsr.w','scene_pc_02a22e',4)
    emitter.ins('bcc.b','scene_pc_02a56a',2)
    emitter.ins('tst.w','%d3',2)
    emitter.ins('bmi.b','scene_pc_02a552',2)
    emitter.ins('cmpi.w','#0xfffd,%d2',4)
    emitter.ins('bcc.b','scene_pc_02a55a',2)
    emitter.ins('move.w','#0x400,%d0',4)
    emitter.ins('bra.w','scene_pc_02aa14',4)
    emitter.ins('jsr','scene_pc_0083d4:l',6)
    emitter.ins('andi.w','#0x1,%d0',4)
    emitter.ins('bne.w','scene_pc_02aa36',4)
    emitter.ins('bra.b','scene_pc_02a52a',2)
    emitter.ins('tst.w','%d3',2)
    emitter.ins('bmi.b','scene_pc_02a4f4',2)
    emitter.ins('move.w','#0x800,%d0',4)
    emitter.ins('bra.w','scene_pc_02aa14',4)
    emitter.segment(0x2a5a0,0x2a5f4)
    emitter.ins('bsr.w','scene_pc_02a22e',4)
    emitter.ins('bcc.b','scene_pc_02a5b6',2)
    emitter.ins('tst.w','%d3',2)
    emitter.ins('bpl.b','scene_pc_02a52a',2)
    emitter.ins('bsr.w','scene_pc_02aa36',4)
    emitter.ins('ori.w','#0x400,%d0',4)
    emitter.ins('bra.w','scene_pc_02aa14',4)
    emitter.ins('tst.w','%d3',2)
    emitter.ins('bmi.b','scene_pc_02a5aa',2)
    emitter.ins('jsr','scene_pc_0083d4:l',6)
    emitter.ins('andi.w','#0x1,%d0',4)
    emitter.ins('beq.b','scene_pc_02a5ca',2)
    emitter.ins('bsr.w','scene_pc_02aa36',4)
    emitter.ins('ori.w','#0x800,%d0',4)
    emitter.ins('bra.w','scene_pc_02aa14',4)
    emitter.ins('btst.b','#0x7,0x2(%a1)',6)
    emitter.ins('beq.b','scene_pc_02a5e6',2)
    emitter.ins('bsr.w','scene_pc_02a52a',4)
    emitter.ins('ori.w','#0x800,%d0',4)
    emitter.ins('bra.w','scene_pc_02aa14',4)
    emitter.ins('bsr.w','scene_pc_02a26c',4)
    emitter.ins('bcc.b','scene_pc_02a5a0',2)
    emitter.ins('move.w','#0x400,%d0',4)
    emitter.ins('bra.w','scene_pc_02aa14',4)
    emitter.segment(0x2aa14,0x2aa5a)
    emitter.ins('btst.b','#0x3,0x18(%a0)',6)
    emitter.ins('bne.b','scene_pc_02aa20',2)
    emitter.ins('eori.w','#0xc00,%d0',4)
    emitter.ins('move.w','%d0,-(%a7)',2)
    emitter.ins('jsr','scene_pc_0083d4:l',6)
    emitter.ins('move.w','%d0,%d1',2)
    emitter.ins('move.w','(%a7)+,%d0',2)
    emitter.ins('andi.w','#0xe,%d1',4)
    emitter.ins('bne.b','scene_pc_02aa34',2)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('rts','',2)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('btst.b','#0x7,0x2(%a1)',6)
    emitter.ins('beq.b','scene_pc_02aa58',2)
    emitter.ins('bsr.w','scene_pc_02a26c',4)
    emitter.ins('bcc.b','scene_pc_02aa58',2)
    emitter.ins('move.w','0x2(%a1),%d0',4)
    emitter.ins('andi.w','#0x3,%d0',4)
    emitter.ins('asl.w','#0x1,%d0',2)
    emitter.ins('move.w','8(%pc, %d0.w),%d0',4)
    emitter.ins('ori.w','#0x2000,%d0',4)
    emitter.ins('rts','',2)

LOWERERS={
    'resolve_duel_attack':_lower_resolve_duel_attack,
    'perform_duel_feint':_lower_perform_duel_feint,
    'flee_duel':_lower_flee_duel,
    'finish_special_duel_action':_lower_finish_special_duel_action,
    'toggle_duel_turn':_lower_toggle_duel_turn,
    'multiply_duel_weight':_lower_multiply_duel_weight,
    'prepare_duel_combat_statistics':_lower_prepare_duel_combat_statistics,
    'measure_duel_spacing':_lower_measure_duel_spacing,
    'choose_duel_cautious_rule':_lower_choose_duel_cautious_rule,
    'execute_duel_cautious_rule':_lower_execute_duel_cautious_rule,
}

def compile_duel(source, *, selected_names=None):
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    sole_rule_fields = {name: records[name]['effects'] for name in ('_duel_rule_call_fields', '_duel_rule_distant_fields', '_duel_rule_legacy_fields', '_duel_rule_legacy_projection', '_duel_rule_motion_fields', '_duel_rule_pressure_fields', '_duel_rule_retreat_fields', 'choose_duel_opponent_special_fields', 'choose_duel_profile_fields', 'choose_duel_random_motion_fields', 'execute_duel_rule_fields', 'measure_duel_spacing_fields')}
    for owner in ('measure_duel_spacing', 'choose_duel_cautious_rule', 'execute_duel_cautious_rule'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'], sole_rule_fields=sole_rule_fields)
    sole_action_fields = {name: records[name]['effects'] for name in ('_duel_action_call_fields', '_duel_action_second_fields', 'toggle_duel_turn_fields', 'multiply_duel_weight_fields', '_duel_action_add_memory_byte_fields', 'prepare_duel_combat_statistics_fields', '_duel_action_random_message_fields', '_duel_action_nonlocal_fields', '_duel_action_terminal_fields', '_recover_after_duel_attack_fields', '_duel_attack_variation_fields', 'resolve_duel_attack_fields', 'perform_duel_feint_fields', 'flee_duel_fields', 'finish_special_duel_action_fields', 'execute_indexed_duel_action_fields', '_duel_action_legacy_fields')}
    for owner in ('resolve_duel_attack', 'perform_duel_feint', 'flee_duel', 'finish_special_duel_action', 'toggle_duel_turn', 'multiply_duel_weight', 'prepare_duel_combat_statistics'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'], sole_action_fields=sole_action_fields)
    if selected_names is not None:
        if type(selected_names) is not tuple or selected_names != SELECTED_DEFAULT_NAMES:
            raise CompileError('fixed whole default family required')
        selected_bindings = tuple((binding for binding in DUEL_BINDINGS if binding.name in selected_names))
        if len(selected_bindings) != len(selected_names):
            raise CompileError('all selected whole owners required')
        return lower_declared(records, selected_bindings, {name: LOWERERS[name] for name in selected_names})
    return lower_declared(records, DUEL_BINDINGS, LOWERERS)


# Root50 sole full-field profile/executor decisions and compatibility facades.
DECLARATIONS.update({'measure_duel_spacing': {'signature': 'state: SceneState, context: DuelTurnContext', 'returns': 'DuelSpacingResult', 'flow': 'returned = measure_duel_spacing_fields(state, _duel_rule_legacy_fields(state, context))\nreturn DuelSpacingResult(_duel_rule_legacy_projection(state, returned), bool(returned.status & 1))'}, '_choose_ai_rule': {'signature': 'state, context, threshold, easy, normal, hard', 'returns': None, 'flow': "plans = {(50, 173222, 173234, 173246): 172820, (60, 173132, 173144, 173156): 172828, (60, 173044, 173056, 173068): 172836, (70, 172958, 172970, 172982): 172840}\nentry = plans.get((threshold, easy, normal, hard))\nif entry is None:\n    raise ValueError('actual original duel profile family required')\nreturned = choose_duel_profile_fields(state, _duel_rule_legacy_fields(state, context), entry)\nreturn _duel_rule_legacy_projection(state, returned)"}, 'choose_duel_opponent_special': {'signature': 'state: SceneState, context: DuelTurnContext', 'returns': 'DuelRuleFrame', 'flow': 'returned = choose_duel_opponent_special_fields(state, _duel_rule_legacy_fields(state, context))\nreturn _duel_rule_legacy_projection(state, returned)'}, 'choose_duel_random_motion': {'signature': 'state: SceneState, context: DuelTurnContext', 'returns': 'DuelRuleFrame', 'flow': 'returned = choose_duel_random_motion_fields(state, _duel_rule_legacy_fields(state, context))\nreturn _duel_rule_legacy_projection(state, returned)'}, 'execute_duel_cautious_rule': {'signature': 'state: SceneState, context: DuelTurnContext', 'returns': 'DuelRuleFrame', 'flow': 'returned = execute_duel_rule_fields(state, _duel_rule_legacy_fields(state, context), 172844)\nreturn _duel_rule_legacy_projection(state, returned)'}, 'execute_duel_balanced_rule': {'signature': 'state: SceneState, context: DuelTurnContext', 'returns': 'DuelRuleFrame', 'flow': 'returned = execute_duel_rule_fields(state, _duel_rule_legacy_fields(state, context), 172848)\nreturn _duel_rule_legacy_projection(state, returned)'}, 'execute_duel_pressure_rule': {'signature': 'state: SceneState, context: DuelTurnContext', 'returns': 'DuelRuleFrame', 'flow': 'returned = execute_duel_rule_fields(state, _duel_rule_legacy_fields(state, context), 172860)\nreturn _duel_rule_legacy_projection(state, returned)'}, 'execute_duel_aggressive_rule': {'signature': 'state: SceneState, context: DuelTurnContext', 'returns': 'DuelRuleFrame', 'flow': 'returned = execute_duel_rule_fields(state, _duel_rule_legacy_fields(state, context), 172864)\nreturn _duel_rule_legacy_projection(state, returned)'}, '_orient_and_gate_duel_motion': {'signature': 'state, context, frame', 'returns': None, 'flow': 'returned = _duel_rule_motion_fields(state, _duel_rule_legacy_fields(state, context, frame))\nreturn _duel_rule_legacy_projection(state, returned)'}, '_guarded_motion': {'signature': 'state, context, frame', 'returns': None, 'flow': 'returned = _duel_rule_distant_fields(state, _duel_rule_legacy_fields(state, context, frame))\nreturn _duel_rule_legacy_projection(state, returned)'}, '_pressure_motion': {'signature': 'state, context, frame', 'returns': None, 'flow': 'returned = _duel_rule_pressure_fields(state, _duel_rule_legacy_fields(state, context, frame))\nreturn _duel_rule_legacy_projection(state, returned)'}, '_duel_rule_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "if target == 33748:\n    return _duel_strategy_call_fields(state, frame, target, continuation)\ndef algorithm(memory, entered):\n    if target == 172590:\n        return measure_duel_weapon_contact_fields(memory.state, entered)\n    if target == 172652:\n        return measure_duel_spacing_fields(memory.state, entered)\n    if target == 174646:\n        return choose_duel_opponent_special_fields(memory.state, entered)\n    if target == 173354:\n        return choose_duel_random_motion_fields(memory.state, entered)\n    raise MovementContinuationBoundary(target, entered, 'actual duel rule child is not restored')\nreturn _presentation_call_fields(BattlePresentationMemory(state), frame, continuation, algorithm)"}, '_duel_rule_distant_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _duel_rule_call_fields(state, frame, 33748, 173324)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 31, 16)\nif not frame.status & 4:\n    frame = _duel_rule_call_fields(state, frame, 174646, 173336)\nframe = _movement_test(state, frame, low16(frame.target_x), 16)\nif not frame.status & 4:\n    return frame\nframe = _movement_test(state, frame, low16(frame.count), 16)\nif frame.status & 8:\n    return _duel_rule_retreat_fields(state, frame)\nframe = _movement_move(state, frame, 'target_x', 2048, 16)\nreturn _duel_rule_motion_fields(state, frame)"}, '_duel_rule_legacy_fields': {'signature': 'state, context, frame=None', 'returns': None, 'flow': 'checked_duel_context(context, state)\ncurrent = context.frame if frame is None else frame\ncurrent.validate(state)\nif current.live is not None:\n    actor_values = _duel_strategy_actor_values(first_replace(FirstDeploymentFrame.unobserved(), target_x=current.command, target_y=current.comparison, unit=current.distance, count=current.factor, distance=current.weapon_difference, choice=current.variation, offset_x=current.live.working_value, offset_y=current.live.response, controller=current.live.lookup.cursor()))\nelse:\n    from ..high_level_scene_flows.contexts_duel import DuelActorFrame\n    actor_values = DuelActorFrame(current.command, current.comparison, current.distance, current.factor, current.weapon_difference, current.variation)\nreturn _duel_strategy_partial_fields(state, context.actor, context.opponent, actor_values)'}, '_duel_rule_legacy_projection': {'signature': 'state, frame', 'returns': None, 'flow': 'return DuelRuleFrame(frame.target_x, frame.target_y, frame.unit, frame.count, frame.distance, frame.choice).validate(state)'}, '_duel_rule_motion_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _postbattle_bit_fields(frame, bool(frame.roster.byte(24) & 8))\nstate.sr = state.sr & 65504 | frame.status\nif frame.status & 4:\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) ^ 3072, 16)\nstack = frame.stack_cursor.advance(-2)\nstack.set_word(0, low16(frame.target_x))\nframe = first_replace(frame, stack_cursor=stack)\nframe = _movement_test(state, frame, low16(frame.target_x), 16)\nframe = _duel_rule_call_fields(state, frame, 33748, 174632)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\nrestored = frame.stack_cursor.word()\nframe = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\nframe = _movement_move(state, frame, 'target_x', restored, 16)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 14, 16)\nif frame.status & 4:\n    frame = _movement_move(state, frame, 'target_x', 0, 16)\nreturn frame"}, '_duel_rule_pressure_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _duel_rule_call_fields(state, frame, 172590, 173476)\ncontact = bool(frame.status & 1)\nframe = _movement_test(state, frame, low16(frame.count), 16)\nnegative = bool(frame.status & 8)\nif contact and (not negative):\n    return choose_duel_random_motion_fields(state, frame)\nif negative:\n    frame = _duel_rule_call_fields(state, frame, 174646, 173486)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) | 1024, 16)\nelse:\n    frame = _duel_rule_call_fields(state, frame, 33748, 173504)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 1, 16)\n    if not frame.status & 4:\n        frame = _duel_rule_call_fields(state, frame, 174646, 173514)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) | 2048, 16)\nreturn _duel_rule_motion_fields(state, frame)"}, '_duel_rule_retreat_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _duel_rule_call_fields(state, frame, 174646, 173304)\nframe = _movement_test(state, frame, low16(frame.target_x), 16)\nif not frame.status & 4:\n    return frame\nframe = _movement_move(state, frame, 'target_x', 1024, 16)\nreturn _duel_rule_motion_fields(state, frame)"}, 'choose_duel_opponent_special_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 174646)\nframe = _movement_move(state, frame, 'target_x', 0, 16)\nframe = _postbattle_bit_fields(frame, bool(frame.candidates.byte(2) & 128))\nstate.sr = state.sr & 65504 | frame.status\nif frame.status & 4:\n    return frame\nframe = _duel_rule_call_fields(state, frame, 172652, 174660)\nif not frame.status & 1:\n    return frame\nframe = _movement_move(state, frame, 'target_x', frame.candidates.word(2), 16)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 3, 16)\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_x', low16(frame.target_x), 1)\ncommand = state.read(u32(174682 + s16(low16(frame.target_x))), 2)\nframe = _movement_move(state, frame, 'target_x', command, 16)\nreturn _movement_move(state, frame, 'target_x', low16(frame.target_x) | 8192, 16)"}, 'choose_duel_profile_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, entry: int', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, entry)\nif entry in (172820, 172824):\n    threshold, easy, normal, hard = (50, 173222, 173234, 173246)\nelif entry in (172828, 172832):\n    threshold, easy, normal, hard = (60, 173132, 173144, 173156)\nelif entry == 172836:\n    threshold, easy, normal, hard = (60, 173044, 173056, 173068)\nelif entry == 172840:\n    threshold, easy, normal, hard = (70, 172958, 172970, 172982)\nelse:\n    raise MovementContinuationBoundary(entry, frame, 'unowned duel profile instruction entry')\nmode = state.read(4294963154, 2)\nframe = _movement_test(state, frame, mode, 16)\nif mode == 0:\n    table = easy\nelse:\n    mode = state.read(4294963154, 2)\n    frame = _movement_compare(state, frame, mode, 2, 16)\n    table = hard if mode == 2 else normal\nframe = first_replace(frame, controller=state.table_at(table).cursor())\nframe = _movement_move(state, frame, 'target_x', threshold, 16)\nframe = _movement_compare(state, frame, low16(frame.target_x), frame.roster.word(28), 16)\nif not frame.status & 1:\n    frame = first_replace(frame, controller=frame.controller.advance(2))\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(12), 16)\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_x', low16(frame.target_x), 2)\nframe = first_replace(frame, controller=frame.controller.advance(s16(low16(frame.target_x))))\nframe = _duel_rule_call_fields(state, frame, 33748, 172940)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 1, 16)\nif not frame.status & 4:\n    frame = first_replace(frame, controller=frame.controller.advance(1))\nframe = _movement_move(state, frame, 'target_x', 0, 16)\nframe = _movement_move(state, frame, 'target_x', frame.controller.byte(), 8)\nframe.roster.set_word(36, low16(frame.target_x))\nreturn _movement_test(state, frame, low16(frame.target_x), 16)"}, 'choose_duel_random_motion_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 173354)\nframe = _duel_rule_call_fields(state, frame, 33748, 173360)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 768, 16)\nframe = _movement_compare(state, frame, low16(frame.target_x), 768, 16)\nif frame.status & 4:\n    frame = _movement_move(state, frame, 'target_x', 0, 16)\nreturn _movement_move(state, frame, 'target_x', low16(frame.target_x) | 16, 16)"}, 'execute_duel_rule_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, entry: int', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, entry)\nif entry in (172844, 172856):\n    frame = _duel_rule_call_fields(state, frame, 33748, 173264)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 63, 16)\n    if not frame.status & 4:\n        frame = _duel_rule_call_fields(state, frame, 174646, 173276)\n    frame = _movement_test(state, frame, low16(frame.target_x), 16)\n    if not frame.status & 4:\n        return frame\n    frame = _duel_rule_call_fields(state, frame, 172590, 173286)\n    if not frame.status & 1:\n        return _duel_rule_distant_fields(state, frame)\n    frame = _movement_test(state, frame, low16(frame.count), 16)\n    if not frame.status & 8:\n        frame = _movement_compare(state, frame, low16(frame.unit), 65533, 16)\n        if not frame.status & 1:\n            return choose_duel_random_motion_fields(state, frame)\n    return _duel_rule_retreat_fields(state, frame)\nif entry in (172848, 172852):\n    frame = _duel_rule_call_fields(state, frame, 172590, 173382)\n    contact = bool(frame.status & 1)\n    frame = _movement_test(state, frame, low16(frame.count), 16)\n    negative = bool(frame.status & 8)\n    if not contact:\n        if negative:\n            return _duel_rule_retreat_fields(state, frame)\n        frame = _movement_move(state, frame, 'target_x', 2048, 16)\n        return _duel_rule_motion_fields(state, frame)\n    if not negative:\n        frame = _movement_compare(state, frame, low16(frame.unit), 65533, 16)\n        if not frame.status & 1:\n            frame = _duel_rule_call_fields(state, frame, 33748, 173408)\n            frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 1, 16)\n            if not frame.status & 4:\n                return choose_duel_opponent_special_fields(state, frame)\n            return choose_duel_random_motion_fields(state, frame)\n    frame = _movement_move(state, frame, 'target_x', 1024, 16)\n    return _duel_rule_motion_fields(state, frame)\nif entry == 172860:\n    return _duel_rule_pressure_fields(state, frame)\nif entry == 172864:\n    frame = _postbattle_bit_fields(frame, bool(frame.candidates.byte(2) & 128))\n    state.sr = state.sr & 65504 | frame.status\n    if not frame.status & 4:\n        frame = _duel_rule_call_fields(state, frame, 173354, 173534)\n        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) | 2048, 16)\n        return _duel_rule_motion_fields(state, frame)\n    frame = _duel_rule_call_fields(state, frame, 172652, 173546)\n    if not frame.status & 1:\n        return _duel_rule_pressure_fields(state, frame)\n    frame = _movement_move(state, frame, 'target_x', 1024, 16)\n    return _duel_rule_motion_fields(state, frame)\nif entry == 173354:\n    return choose_duel_random_motion_fields(state, frame)\nif entry == 174646:\n    return choose_duel_opponent_special_fields(state, frame)\nraise MovementContinuationBoundary(entry, frame, 'unowned duel executor instruction entry')"}, 'measure_duel_spacing_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 172652)\nframe = _movement_move(state, frame, 'target_y', frame.candidates.word(12), 16)\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_y', low16(frame.target_y), 1)\nreach = state.read(u32(172640 + s16(low16(frame.target_y))), 2)\nframe = _movement_move(state, frame, 'unit', reach, 16)\nframe = _movement_add_word(state, frame, 'unit', 8)\nframe = _postbattle_bit_fields(frame, bool(frame.candidates.byte(24) & 8))\nstate.sr = state.sr & 65504 | frame.status\nif frame.status & 4:\n    frame = _duel_commit_sub_word_fields(state, frame, 'unit', 0, True)\nframe = _movement_add_word(state, frame, 'unit', frame.candidates.word(14))\nframe = _duel_commit_sub_word_fields(state, frame, 'unit', frame.roster.word(14))\nif frame.status & 8:\n    frame = _duel_commit_sub_word_fields(state, frame, 'unit', 0, True)\ndeduction = state.read(u32(172692 + s16(low16(frame.target_y))), 2)\nreturn _duel_commit_sub_word_fields(state, frame, 'unit', deduction)"}})
APPROVED.setdefault('contexts_scene',set()).update({'SceneRefreshMemory', 'first_replace', 'FirstDeploymentFrame'})
APPROVED.setdefault('business_scene',set()).update({'_scene_render_asl_word'})
APPROVED.setdefault('business_duel',set()).update({'measure_duel_weapon_contact_fields', '_duel_strategy_actor_values', '_duel_strategy_partial_fields', '_duel_strategy_call_fields'})
APPROVED.setdefault('business_city',set()).update({'_resource_cost_frame', '_duel_commit_sub_word_fields'})
APPROVED.setdefault('business_movement_support',set()).update({'_movement_add_word', '_movement_move', '_movement_compare', '_movement_test'})
APPROVED.setdefault('contexts_gameplay',set()).update({'MovementContinuationBoundary'})
APPROVED.setdefault('business_battle',set()).update({'_presentation_call_fields', '_postbattle_bit_fields'})
APPROVED.setdefault('contexts_battle',set()).update({'BattlePresentationMemory'})
APPROVED.setdefault('domain',set()).update({'s16'})
APPROVED.setdefault('contexts_duel',set()).update({'DuelActorFrame'})

DECLARATIONS.update({'_sample': {'flow': "return _duel_action_legacy_fields(state, frame, 33748, '_duel_action_call_fields')", 'returns': None, 'signature': 'state, frame', 'slots': {}}})

DECLARATIONS.update({'_message': {'flow': "return _duel_action_legacy_fields(state, frame, 164392, '_duel_action_call_fields')", 'returns': None, 'signature': 'state, frame, selection', 'slots': {}}})

DECLARATIONS.update({'_wait': {'flow': "return _duel_action_legacy_fields(state, frame, 161658, '_duel_action_call_fields')", 'returns': None, 'signature': 'state, frame, *, either=False', 'slots': {}}})

DECLARATIONS.update({'_clear': {'flow': "return _duel_action_legacy_fields(state, frame, 163190, '_duel_action_call_fields')", 'returns': None, 'signature': 'state, frame', 'slots': {}}})

DECLARATIONS.update({'_second_turn': {'flow': "return _duel_action_legacy_fields(state, None, 161922, '_duel_action_second_fields')", 'returns': None, 'signature': 'state', 'slots': {}}})

DECLARATIONS.update({'_toggle': {'flow': "return _duel_action_legacy_fields(state, None, 161922, 'toggle_duel_turn_fields')", 'returns': None, 'signature': 'state', 'slots': {}}})

DECLARATIONS.update({'toggle_duel_turn': {'flow': "return _duel_action_legacy_fields(state, None, 161922, 'toggle_duel_turn_fields')", 'returns': 'None', 'signature': 'state: SceneState', 'slots': {}}})

DECLARATIONS.update({'toggle_duel_turn_complete': {'flow': "return _duel_action_legacy_fields(state, frame, 161922, 'toggle_duel_turn_fields')", 'returns': None, 'signature': 'state, frame', 'slots': {}}})

DECLARATIONS.update({'_weight_frame': {'flow': "return _duel_action_legacy_fields(state, frame, 162494, 'multiply_duel_weight_fields')", 'returns': None, 'signature': 'state, frame', 'slots': {}}})

DECLARATIONS.update({'prepare_duel_combat_statistics': {'flow': "return _duel_action_legacy_fields(state, context, 162534, 'prepare_duel_combat_statistics_fields')", 'returns': 'DuelRuleFrame', 'signature': 'state: SceneState, context: DuelTurnContext', 'slots': {}}})

DECLARATIONS.update({'_divide_frame': {'flow': "return _duel_action_legacy_fields(state, frame, 218976, '_duel_action_call_fields')", 'returns': None, 'signature': 'state, frame', 'slots': {}}})

DECLARATIONS.update({'_frame_message': {'flow': "return _duel_action_legacy_fields(state, frame, 164392, '_duel_action_call_fields')", 'returns': None, 'signature': 'state, frame, selection', 'slots': {}}})

DECLARATIONS.update({'_frame_wait': {'flow': "return _duel_action_legacy_fields(state, frame, 161658, '_duel_action_call_fields')", 'returns': None, 'signature': 'state, frame, *, either=False', 'slots': {}}})

DECLARATIONS.update({'_frame_clear': {'flow': "return _duel_action_legacy_fields(state, frame, 163190, '_duel_action_call_fields')", 'returns': None, 'signature': 'state, frame', 'slots': {}}})

DECLARATIONS.update({'_recover_after_duel_attack': {'flow': "return _duel_action_legacy_fields(state, frame, 161452, '_recover_after_duel_attack_fields')", 'returns': None, 'signature': 'state, frame', 'slots': {}}})

DECLARATIONS.update({'resolve_duel_attack_complete': {'flow': "return _duel_action_legacy_fields(state, frame, 161142, 'resolve_duel_attack_fields')", 'returns': None, 'signature': 'state, frame', 'slots': {}}})

DECLARATIONS.update({'resolve_duel_attack': {'flow': "return _duel_action_legacy_fields(state, context, 161142, 'resolve_duel_attack_fields')", 'returns': 'DuelTurnOutcome', 'signature': 'state: SceneState, context: DuelTurnContext', 'slots': {}}})

DECLARATIONS.update({'perform_duel_feint_complete': {'flow': "return _duel_action_legacy_fields(state, frame, 161146, 'perform_duel_feint_fields')", 'returns': None, 'signature': 'state, frame', 'slots': {}}})

DECLARATIONS.update({'perform_duel_feint': {'flow': "return _duel_action_legacy_fields(state, context, 161146, 'perform_duel_feint_fields')", 'returns': 'DuelTurnOutcome', 'signature': 'state: SceneState, context: DuelTurnContext', 'slots': {}}})

DECLARATIONS.update({'flee_duel_complete': {'flow': "return _duel_action_legacy_fields(state, frame, 161150, 'flee_duel_fields')", 'returns': None, 'signature': 'state, frame', 'slots': {}}})

DECLARATIONS.update({'flee_duel': {'flow': "return _duel_action_legacy_fields(state, context, 161150, 'flee_duel_fields')", 'returns': 'DuelTurnOutcome', 'signature': 'state: SceneState, context: DuelTurnContext', 'slots': {}}})

DECLARATIONS.update({'finish_special_duel_action_complete': {'flow': "return _duel_action_legacy_fields(state, frame, 161154, 'finish_special_duel_action_fields')", 'returns': None, 'signature': 'state, frame', 'slots': {}}})

DECLARATIONS.update({'finish_special_duel_action': {'flow': "return _duel_action_legacy_fields(state, context, 161154, 'finish_special_duel_action_fields')", 'returns': 'DuelTurnOutcome', 'signature': 'state: SceneState, context: DuelTurnContext', 'slots': {}}})

DECLARATIONS.update({'_push_long': {'flow': "raise Boundary('historical partial stack needs the complete current action frame')", 'returns': None, 'signature': 'frame, value', 'slots': {}}})

DECLARATIONS.update({'_pop_long': {'flow': "raise Boundary('historical partial stack needs the complete current action frame')", 'returns': None, 'signature': 'frame, name', 'slots': {}}})

DECLARATIONS.update({'_nonlocal_complete': {'flow': "raise Boundary('historical partial stack needs the complete current action frame')", 'returns': None, 'signature': 'frame', 'slots': {}}})

DECLARATIONS.update({'_duel_action_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "if target == 33748:\n    return _duel_strategy_call_fields(state, frame, target, continuation)\ndef child(memory, entered):\n    if target == 162494:\n        return multiply_duel_weight_fields(state, entered)\n    if target == 162534:\n        return prepare_duel_combat_statistics_fields(state, entered)\n    if target == 161922:\n        return toggle_duel_turn_fields(state, entered)\n    if target == 218976:\n        from ..high_level_main_flows.business_movement_support import signed_divmod_fields\n        return signed_divmod_fields(state, entered)\n    from ..high_level_scene_flows.business_duel import choose_duel_status_text_fields, wait_active_duel_action_fields, wait_either_duel_action_fields, clear_duel_text_plane_fields\n    if target == 164392:\n        return choose_duel_status_text_fields(state, entered)\n    if target == 161658:\n        return wait_active_duel_action_fields(state, entered)\n    if target == 161720:\n        return wait_either_duel_action_fields(state, entered)\n    if target == 163190:\n        return clear_duel_text_plane_fields(state, entered)\n    raise MovementContinuationBoundary(target, entered, 'actual duel action child is not restored')\nreturn _presentation_call_fields(BattlePresentationMemory(state), frame, continuation, child)"}})

DECLARATIONS.update({'_duel_action_second_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'tuple[FirstDeploymentFrame, bool]', 'flow': 'frame = _movement_test(state, frame, state.read(16740376, 2), 16)\nreturn (frame, bool(frame.status & 8))'}})

DECLARATIONS.update({'toggle_duel_turn_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _resource_cost_frame(state, frame, 161922)\nfor address in (16740362, 16740363):\n    frame = _movement_compare(state, frame, state.read(address, 1), 3, 8)\n    if frame.status & 4:\n        return frame\nvalue = state.read(16740376, 2) ^ 32768\nfrom ..high_level_scene_flows.business_duel import _duel_scene_store_fields\nreturn _duel_scene_store_fields(state, frame, 16740376, value)'}})

DECLARATIONS.update({'multiply_duel_weight_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _resource_cost_frame(state, frame, 162494)\nvalue = frame.target_y\nframe = _movement_compare_address(state, frame, value, 65536)\nproduct, response, conditions = _weight_fields(value, low16(frame.count), frame.offset_y)\nframe = first_replace(frame, target_y=product, offset_y=response)\nif value < 65536:\n    return _movement_test_long(state, frame, product)\nstatus = (17 if conditions.carry else 0) | (8 if conditions.negative else 0) | (4 if conditions.zero else 0) | (2 if conditions.overflow else 0)\nstate.sr = state.sr & 65504 | status\nreturn first_replace(frame, status=status)'}})

DECLARATIONS.update({'_duel_action_add_memory_byte_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, view: Table, offset: Word', 'returns': 'FirstDeploymentFrame', 'flow': 'value = view.byte(offset)\nframe, value = _movement_binary_flags(state, frame, value, 1, 8)\nview.set_byte(offset, value)\nreturn frame'}})

DECLARATIONS.update({'prepare_duel_combat_statistics_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 162534)\nframe = first_replace(frame, scan=state.table_at(4294951680).cursor(), scratch=state.table_at(4294951424).cursor())\nframe = first_replace(frame, scan=frame.scan.advance(s16(low16(frame.target_y))), scratch=frame.scratch.advance(s16(low16(frame.target_y))))\nframe = _duel_actor_store_fields(state, frame, frame.candidates, 57, frame.scan.byte(0), 8)\nframe = _duel_actor_store_fields(state, frame, frame.candidates, 51, frame.scratch.byte(0), 8)\nframe = _duel_action_add_memory_byte_fields(state, frame, frame.candidates, 51)\nframe = first_replace(frame, opponent=state.table_at(4294951424).cursor())\nframe = first_replace(frame, opponent=frame.opponent.advance(s16(low16(frame.target_x))))\nframe = _duel_actor_store_fields(state, frame, frame.roster, 51, frame.opponent.byte(0), 8)\nframe = _duel_action_add_memory_byte_fields(state, frame, frame.roster, 51)\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_x', low16(frame.target_x), 1)\nframe = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_y', low16(frame.target_y), 1)\nframe = first_replace(frame, opponent=state.table_at(4294946816).cursor(), scratch=state.table_at(4294948352).cursor())\nframe = first_replace(frame, opponent=frame.opponent.advance(s16(low16(frame.target_y))), scratch=frame.scratch.advance(s16(low16(frame.target_y))))\nframe = _duel_actor_store_fields(state, frame, frame.candidates, 52, frame.candidates.word(28))\nframe = _duel_actor_store_fields(state, frame, frame.candidates, 54, frame.opponent.word(0))\nframe = _duel_actor_store_fields(state, frame, frame.candidates, 48, frame.scratch.word(0))\nframe = first_replace(frame, scan=state.table_at(4294948352).cursor())\nframe = first_replace(frame, scan=frame.scan.advance(s16(low16(frame.target_x))))\nframe = _duel_actor_store_fields(state, frame, frame.roster, 48, frame.scan.word(0))\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(26), 16)\nframe = _movement_move(state, frame, 'target_y', frame.candidates.word(26), 16)\nframe = first_replace(frame, scan=state.table_at(4294952704).cursor())\nframe = first_replace(frame, scan=frame.scan.advance(s16(low16(frame.target_x))))\nframe = _movement_move(state, frame, 'offset_x', frame.scan.byte(0), 8)\nframe = _movement_move(state, frame, 'offset_x', low16(frame.offset_x) & 15, 16)\nframe = first_replace(frame, scan=state.table_at(4294952704).cursor())\nframe = first_replace(frame, scan=frame.scan.advance(s16(low16(frame.target_y))))\nframe = _movement_move(state, frame, 'offset_y', frame.scan.byte(0), 8)\nframe = _movement_move(state, frame, 'offset_y', low16(frame.offset_y) & 15, 16)\nreturn _duel_commit_sub_word_fields(state, frame, 'offset_x', low16(frame.offset_y))"}})

DECLARATIONS.update({'_duel_action_random_message_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, role: str', 'returns': 'FirstDeploymentFrame', 'flow': "plans = {'recovery': (161458, 1, 37, 29, 161482), 'attack_success': (161540, 1, 39, 39, 161568), 'feint_open': (161816, 3, 14, 14, 161852), 'feint_reply': (161866, 3, 49, 49, 161902), 'flee': (161958, 1, 20, 20, 161986), 'special': (162052, 3, 24, 24, 162090)}\nif role not in plans:\n    raise ValueError('actual original random-message role required')\nrandom_return, mask, bias, subtract, message_return = plans[role]\nframe = _duel_action_call_fields(state, frame, 33748, random_return)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & mask, 16)\nif mask == 3:\n    frame = _movement_compare(state, frame, low16(frame.target_x), 3, 16)\n    if frame.status & 4:\n        if role == 'special':\n            frame = _movement_move_long(state, frame, 'target_x', 0)\n        else:\n            frame = _movement_move(state, frame, 'target_x', 0, 16)\nframe = _movement_add_word(state, frame, 'target_x', bias)\nframe, second = _duel_action_second_fields(state, frame)\nif second:\n    frame = _duel_commit_sub_word_fields(state, frame, 'target_x', subtract)\n    second_bias = {'attack_success': 10, 'feint_open': 46, 'feint_reply': 17, 'flee': 44, 'special': 41}\n    if role in second_bias:\n        frame = _movement_add_word(state, frame, 'target_x', second_bias[role])\nreturn _duel_action_call_fields(state, frame, 164392, message_return)"}})

DECLARATIONS.update({'_duel_action_nonlocal_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'tuple[str, FirstDeploymentFrame]', 'flow': "discarded = frame.stack_cursor.long(0)\nframe = first_replace(frame, stack_cursor=frame.stack_cursor.advance(4))\nframe = _movement_move_long(state, frame, 'target_x', discarded)\nreturn ('fade', frame)"}})

DECLARATIONS.update({'_duel_action_terminal_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, role: str', 'returns': 'tuple[str, FirstDeploymentFrame]', 'flow': "plans = {'attack': (13, -1, 161624, 161628, 2, 512), 'flee': (22, 1, 162012, 162016, 768, 3), 'special': (29, 1, 162158, 162162, 256, 1)}\nif role not in plans:\n    raise ValueError('actual original terminal action role required')\nselection, step, message_return, wait_return, result_first, result_second = plans[role]\nframe = _movement_move(state, frame, 'target_x', selection, 16)\nframe, second = _duel_action_second_fields(state, frame)\nif second:\n    if step == 1:\n        frame = _movement_add_word(state, frame, 'target_x', 1)\n    else:\n        frame = _duel_commit_sub_word_fields(state, frame, 'target_x', 1)\nframe = _duel_action_call_fields(state, frame, 164392, message_return)\nframe = _duel_action_call_fields(state, frame, 161720, wait_return)\nfrom ..high_level_scene_flows.business_duel import _duel_scene_store_fields\nframe = _duel_scene_store_fields(state, frame, 16740592, result_first)\nframe, second = _duel_action_second_fields(state, frame)\nif second:\n    frame = _duel_scene_store_fields(state, frame, 16740592, result_second)\nreturn _duel_action_nonlocal_fields(state, frame)"}})

DECLARATIONS.update({'_recover_after_duel_attack_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'tuple[str, FirstDeploymentFrame]', 'flow': "frame = _duel_action_random_message_fields(state, frame, 'recovery')\nframe = _duel_action_call_fields(state, frame, 161922, 161486)\nframe = _duel_action_call_fields(state, frame, 161658, 161490)\nframe = _duel_action_call_fields(state, frame, 161922, 161494)\ntimer = frame.candidates.word(40)\nframe = _movement_compare(state, frame, timer, 300, 16)\nif frame.status & 1:\n    frame = _duel_actor_store_fields(state, frame, frame.candidates, 40, 300)\nreturn ('return', frame)"}})

DECLARATIONS.update({'_duel_attack_variation_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "while True:\n    frame = _movement_save_longs(state, frame, ('target_y',))\n    frame = _duel_action_call_fields(state, frame, 33748, 161336)\n    frame = _movement_restore_longs(state, frame, ('target_y',))\n    frame = _movement_move(state, frame, 'count', low16(frame.offset_x), 16)\n    if frame.status & 4 or frame.status & 8:\n        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 7, 16)\n        frame = _movement_compare(state, frame, low16(frame.target_x), 4, 16)\n        if not frame.status & 5:\n            continue\n        frame = _duel_commit_sub_word_fields(state, frame, 'offset_x', 0, True)\n        frame = _movement_move_long(state, frame, 'choice', 0)\n        value = state.read(u32(161376 + s16(low16(frame.offset_x))), 1)\n        frame = _movement_move(state, frame, 'choice', value, 8)\n        frame = _movement_add_word(state, frame, 'choice', low16(frame.target_x))\n        frame = _movement_move(state, frame, 'choice', low16(frame.choice) & 255, 16)\n    else:\n        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)\n        frame = _movement_compare(state, frame, low16(frame.target_x), 8, 16)\n        if not frame.status & 5:\n            continue\n        frame = _movement_move_long(state, frame, 'choice', 0)\n        value = state.read(u32(161404 + s16(low16(frame.offset_x))), 1)\n        frame = _movement_move(state, frame, 'choice', value, 8)\n        frame = _movement_add_word(state, frame, 'choice', low16(frame.target_x))\n    return _movement_move(state, frame, 'count', low16(frame.choice), 16)"}})

DECLARATIONS.update({'resolve_duel_attack_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'tuple[str, FirstDeploymentFrame]', 'flow': "frame = _resource_cost_frame(state, frame, 161158)\nframe = _movement_move(state, frame, 'target_x', 6, 16)\nframe = _movement_move(state, frame, 'target_y', frame.roster.word(26), 16)\nframe = _movement_compare(state, frame, low16(frame.target_y), frame.roster.word(32), 16)\nif frame.status & 4:\n    frame = _movement_add_word(state, frame, 'target_x', 1)\nframe, second = _duel_action_second_fields(state, frame)\nif second:\n    frame = _movement_move(state, frame, 'target_x', 35, 16)\n    frame = _movement_move(state, frame, 'target_y', frame.roster.word(26), 16)\n    frame = _movement_compare(state, frame, low16(frame.target_y), frame.roster.word(32), 16)\n    if frame.status & 4:\n        frame = _movement_add_word(state, frame, 'target_x', 1)\nframe = _duel_action_call_fields(state, frame, 164392, 161206)\nframe = _duel_action_call_fields(state, frame, 161658, 161210)\nframe = _duel_action_call_fields(state, frame, 163190, 161214)\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(26), 16)\nframe = _movement_move(state, frame, 'target_y', frame.candidates.word(26), 16)\nframe = _duel_action_call_fields(state, frame, 162534, 161226)\nframe = _movement_move(state, frame, 'target_x', frame.candidates.word(56), 16)\nframe = _movement_move_long(state, frame, 'target_y', 100)\nframe = _duel_commit_sub_word_fields(state, frame, 'target_y', low16(frame.target_x))\nframe = _movement_multiply_word(state, frame, 'target_y', frame.roster.word(48))\nframe = _movement_move(state, frame, 'count', frame.roster.word(50), 16)\nframe = _duel_action_call_fields(state, frame, 162494, 161248)\nframe = _movement_move(state, frame, 'count', frame.candidates.word(54), 16)\nframe = _duel_action_call_fields(state, frame, 162494, 161256)\nframe = _movement_save_longs(state, frame, ('target_y',))\nframe = _movement_move_long(state, frame, 'target_y', 0)\nframe = _movement_move(state, frame, 'target_y', frame.candidates.word(48), 16)\nframe = _movement_multiply_word(state, frame, 'target_y', frame.candidates.word(50))\nframe = _movement_move(state, frame, 'count', frame.candidates.word(52), 16)\nframe = _duel_action_call_fields(state, frame, 162494, 161278)\nframe = _movement_test(state, frame, state.read(4294963154, 2), 16)\ndifficulty = 60\nif not frame.status & 4:\n    frame = _movement_compare(state, frame, state.read(4294963154, 2), 2, 16)\n    difficulty = 100 if frame.status & 4 else 80\nframe = _movement_move(state, frame, 'count', difficulty, 16)\nframe = _duel_action_call_fields(state, frame, 162494, 161320)\nframe = _movement_move_long(state, frame, 'unit', frame.target_y)\nframe = _movement_restore_longs(state, frame, ('target_y',))\nframe = _duel_attack_variation_fields(state, frame)\nframe = _duel_action_call_fields(state, frame, 162494, 161416)\nframe = _movement_save_longs(state, frame, ('unit',))\nframe = _movement_move_long(state, frame, 'unit', 10)\nframe = _duel_action_call_fields(state, frame, 218976, 161428)\nframe = _movement_restore_longs(state, frame, ('unit',))\nframe = _movement_test_long(state, frame, frame.unit)\nif not frame.status & 4:\n    frame = _duel_action_call_fields(state, frame, 218976, 161444)\n    frame = _movement_compare(state, frame, low16(frame.target_y), 1, 16)\n    if frame.status & 1:\n        return _recover_after_duel_attack_fields(state, frame)\nframe, second = _duel_action_second_fields(state, frame)\nblocked = state.read(4294963070 if second else 4294963071, 1)\nframe = _movement_test(state, frame, blocked, 8)\nif not frame.status & 4:\n    return _recover_after_duel_attack_fields(state, frame)\nframe = _duel_action_random_message_fields(state, frame, 'attack_success')\nframe = _duel_action_call_fields(state, frame, 161922, 161572)\nframe = _duel_action_call_fields(state, frame, 161658, 161576)\nframe = _duel_action_call_fields(state, frame, 161922, 161580)\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(24), 16)\nframe = _movement_move(state, frame, 'target_y', frame.candidates.word(24), 16)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 63487, 16)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 2048, 16)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) | low16(frame.target_y), 16)\nframe = _duel_actor_store_fields(state, frame, frame.candidates, 24, low16(frame.target_x))\nframe = _duel_action_call_fields(state, frame, 163190, 161606)\nreturn _duel_action_terminal_fields(state, frame, 'attack')"}})

DECLARATIONS.update({'perform_duel_feint_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'tuple[str, FirstDeploymentFrame]', 'flow': "frame = _resource_cost_frame(state, frame, 161810)\nframe = _duel_action_random_message_fields(state, frame, 'feint_open')\nframe = _duel_action_call_fields(state, frame, 161658, 161856)\nframe = _duel_action_call_fields(state, frame, 163190, 161860)\nframe = _duel_action_random_message_fields(state, frame, 'feint_reply')\nframe = _duel_action_call_fields(state, frame, 161922, 161906)\nframe = _duel_action_call_fields(state, frame, 161658, 161910)\nframe = _duel_action_call_fields(state, frame, 161922, 161914)\nframe = _duel_actor_store_fields(state, frame, frame.candidates, 40, 900)\nreturn ('return', frame)"}})

DECLARATIONS.update({'flee_duel_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'tuple[str, FirstDeploymentFrame]', 'flow': "frame = _resource_cost_frame(state, frame, 161952)\nframe = _duel_action_random_message_fields(state, frame, 'flee')\nframe = _duel_action_call_fields(state, frame, 161658, 161990)\nframe = _duel_action_call_fields(state, frame, 163190, 161994)\nreturn _duel_action_terminal_fields(state, frame, 'flee')"}})

DECLARATIONS.update({'finish_special_duel_action_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'tuple[str, FirstDeploymentFrame]', 'flow': "frame = _resource_cost_frame(state, frame, 162046)\nframe = _duel_action_random_message_fields(state, frame, 'special')\nframe = _duel_action_call_fields(state, frame, 161658, 162094)\nprevious = frame.roster.byte(2)\nframe = _postbattle_bit_fields(frame, bool(previous & 8))\nstate.sr = state.sr & 65504 | frame.status\nframe.roster.set_byte(2, previous | 8)\nframe = _duel_action_call_fields(state, frame, 163190, 162104)\nframe = _movement_move(state, frame, 'target_x', 28, 16)\nframe, second = _duel_action_second_fields(state, frame)\nif second:\n    frame = _movement_move(state, frame, 'target_x', 27, 16)\nframe = _duel_action_call_fields(state, frame, 164392, 162124)\nframe = _duel_action_call_fields(state, frame, 161922, 162128)\nframe = _duel_action_call_fields(state, frame, 161658, 162132)\nframe = _duel_action_call_fields(state, frame, 161922, 162136)\nframe = _duel_action_call_fields(state, frame, 163190, 162140)\nreturn _duel_action_terminal_fields(state, frame, 'special')"}})

DECLARATIONS.update({'execute_indexed_duel_action_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int', 'returns': 'tuple[str, FirstDeploymentFrame]', 'flow': "if target in (161142, 161158):\n    return resolve_duel_attack_fields(state, frame)\nif target in (161146, 161810):\n    return perform_duel_feint_fields(state, frame)\nif target in (161150, 161952):\n    return flee_duel_fields(state, frame)\nif target in (161154, 162046):\n    return finish_special_duel_action_fields(state, frame)\nraise MovementContinuationBoundary(target, frame, 'actual indexed action entry is not owned')"}})

DECLARATIONS.update({'_duel_action_legacy_fields': {'signature': 'state: SceneState, observation, target: int, sole_core: str', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_scene_flows.business_duel import _duel_scene_legacy_context_fields\nif type(observation) is DuelTurnContext:\n    checked_duel_context(observation, state)\n    if observation.frame.live is not None:\n        return _duel_scene_legacy_context_fields(state, observation.frame.live, target, sole_core)\n    values = observation.frame\n    entered = first_replace(FirstDeploymentFrame.unobserved(), target_x=values.command, target_y=values.comparison, unit=values.distance, count=values.factor, distance=values.weapon_difference, choice=values.variation, roster=observation.actor.cursor(), candidates=observation.opponent.cursor())\n    raise MovementContinuationBoundary(target, entered, 'old six-value action lacks current D5/D6/A2-A6/CCR-X/SP; use ' + sole_core)\nreturn _duel_scene_legacy_context_fields(state, observation, target, sole_core)"}})

APPROVED.setdefault('business_duel',set()).update({'_duel_actor_store_fields','_duel_scene_store_fields','_duel_scene_legacy_context_fields','choose_duel_status_text_fields','wait_active_duel_action_fields','wait_either_duel_action_fields','clear_duel_text_plane_fields'})
APPROVED.setdefault('business_movement_support',set()).update({'_movement_move_long','_movement_test_long','_movement_compare_address','_movement_binary_flags','_movement_multiply_word','_movement_save_longs','_movement_restore_longs','signed_divmod_fields'})

SELECTED_DEFAULT_NAMES = ('toggle_duel_turn', 'multiply_duel_weight', 'prepare_duel_combat_statistics')

APPROVED.setdefault((2, 'high_level_gameplay_flow.business_battle'),set()).update(['_postbattle_bit_fields', '_presentation_call_fields'])

APPROVED.setdefault((2, 'high_level_gameplay_flow.contexts_battle'),set()).update(['BattlePresentationMemory'])

APPROVED.setdefault((2, 'high_level_main_flows.business_movement_support'),set()).update(['_movement_add_word', '_movement_binary_flags', '_movement_compare', '_movement_compare_address', '_movement_move', '_movement_move_long', '_movement_multiply_word', '_movement_restore_longs', '_movement_save_longs', '_movement_test', '_movement_test_long', 'signed_divmod_fields'])

APPROVED.setdefault((2, 'high_level_main_flows.contexts_gameplay'),set()).update(['MovementContinuationBoundary'])

APPROVED.setdefault((2, 'high_level_remaining_flows.business_city'),set()).update(['_duel_commit_sub_word_fields', '_resource_cost_frame'])

APPROVED.setdefault((2, 'high_level_scene_flows.business_duel'),set()).update(['_duel_actor_store_fields', '_duel_scene_legacy_context_fields', '_duel_scene_store_fields', '_duel_strategy_actor_values', '_duel_strategy_call_fields', '_duel_strategy_partial_fields', 'choose_duel_status_text_fields', 'clear_duel_text_plane_fields', 'measure_duel_weapon_contact_fields', 'wait_active_duel_action_fields', 'wait_either_duel_action_fields'])

APPROVED.setdefault((2, 'high_level_scene_flows.business_scene'),set()).update(['_scene_render_asl_word'])

APPROVED.setdefault((2, 'high_level_scene_flows.contexts_duel'),set()).update(['DuelActorFrame'])

APPROVED.setdefault((2, 'high_level_scene_flows.contexts_scene'),set()).update(['FirstDeploymentFrame', 'SceneRefreshMemory', 'first_replace'])

APPROVED.setdefault((2, 'high_level_scene_flows.domain'),set()).update(['s16'])
