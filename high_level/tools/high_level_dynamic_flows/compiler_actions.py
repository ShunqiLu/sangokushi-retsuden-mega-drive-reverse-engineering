"""Restricted semantic source admission with ordinary mnemonic lowering.

Explicit business text only; this is an intermediate structural compiler,
not arbitrary Python compilation or full natural-gameplay acceptance.
"""
from .compiler_common import semantic_functions,lower_declared
from .target import ACTIONS_BINDINGS

APPROVED={'contexts_actions': {'DuelGlyphContext',
                      'ObjectActionResult',
                      'ObjectGlyphResult',
                      'ObjectPositionOffset',
                      'ObjectRosterTotals',
                      'ObjectVectorContext',
                      'SceneControllerConditions',
                      'SceneRenderFrame',
                      'SpriteBatchContext',
                      'TileUploadResult',
                      'checked_action',
                      'checked_controller_frame'},
 'dataclasses': {'replace'},
 'domain': {'Boundary',
            'Cursor',
            'Long',
            'SceneState',
            'StackContinuation',
            'Table',
            'Word',
            'checked_cursor',
            'checked_state',
            'checked_table',
            'descending_inclusive',
            'divu_retained',
            'low16',
            'low8',
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
 'services': {'append_scene_sprite_entries',
              'decode_glyph_rows_to_buffers',
              'enqueue_sound_command',
              'offset_scene_object_position',
              'plan_scene_object_action',
              'probe_scene_object_overlap_with_frame',
              'read_object_action_mode',
              'resume_selected_object_action',
              'resume_selected_object_action_complete',
              'sample_random_pair',
              'sample_random_preserving_seed_carrier'}}

DECLARATIONS={'_ram': {'signature': 'state, low',
          'returns': None,
          'flow': "return ram_view(state, 'ram_' + low)"},
 '_result': {'signature': 'actor, opponent, frame',
             'returns': None,
             'flow': 'return ObjectActionResult(actor, opponent, frame)'},
 '_finish_action': {'signature': 'state, actor, opponent, frame',
                    'returns': None,
                    'flow': "_ram(state, '8152').set_word(0, 0)\n"
                            'return _result(actor, opponent, frame)'},
 '_sample': {'signature': 'state, frame',
             'returns': None,
             'flow': 'return replace(frame, x=sample_random_preserving_seed_carrier(state))'},
 '_probe': {'signature': 'state, actor, opponent, frame, horizontal, vertical, *, '
                         'restore=True',
            'returns': None,
            'flow': 'frame = replace(frame, x=replace_word(frame.x, horizontal), '
                    'y=replace_word(frame.y, vertical))\n'
                    'outcome, frame = probe_scene_object_overlap_with_frame(state, actor, '
                    'ObjectPositionOffset(horizontal, vertical), frame)\n'
                    'return _result(actor, opponent if restore else outcome.candidate, '
                    'frame)'},
 'probe_object_left': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: '
                                    'SceneRenderFrame',
                       'returns': 'ObjectActionResult',
                       'flow': 'checked_action(state, actor, opponent, frame)\n'
                               'return _probe(state, actor, opponent, frame, 32784, 0)'},
 'probe_object_right': {'signature': 'state: SceneState, actor: Table, opponent: Table, '
                                     'frame: SceneRenderFrame',
                        'returns': 'ObjectActionResult',
                        'flow': 'checked_action(state, actor, opponent, frame)\n'
                                'return _probe(state, actor, opponent, frame, 16, 0)'},
 'probe_object_up': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: '
                                  'SceneRenderFrame',
                     'returns': 'ObjectActionResult',
                     'flow': 'checked_action(state, actor, opponent, frame)\n'
                             'return _probe(state, actor, opponent, frame, 0, 32784)'},
 'probe_object_down': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: '
                                    'SceneRenderFrame',
                       'returns': 'ObjectActionResult',
                       'flow': 'checked_action(state, actor, opponent, frame)\n'
                               'return _probe(state, actor, opponent, frame, 0, 16)'},
 'object_movement_speed': {'signature': 'state: SceneState',
                           'returns': 'Long',
                           'flow': 'checked_state(state)\n'
                                   "return 2 if _ram(state, '840a').word() == 0 else 4"},
 'continue_object_left': {'signature': 'state: SceneState, actor: Table, opponent: Table, '
                                       'frame: SceneRenderFrame',
                          'returns': 'ObjectActionResult',
                          'flow': 'return _continue_object_motion(state, actor, opponent, '
                                  'frame, 0)[0]'},
 'continue_object_right': {'signature': 'state: SceneState, actor: Table, opponent: Table, '
                                        'frame: SceneRenderFrame',
                           'returns': 'ObjectActionResult',
                           'flow': 'return _continue_object_motion(state, actor, opponent, '
                                   'frame, 1)[0]'},
 'continue_object_up': {'signature': 'state: SceneState, actor: Table, opponent: Table, '
                                     'frame: SceneRenderFrame',
                        'returns': 'ObjectActionResult',
                        'flow': 'return _continue_object_motion(state, actor, opponent, '
                                'frame, 2)[0]'},
 'continue_object_down': {'signature': 'state: SceneState, actor: Table, opponent: Table, '
                                       'frame: SceneRenderFrame',
                          'returns': 'ObjectActionResult',
                          'flow': 'return _continue_object_motion(state, actor, opponent, '
                                  'frame, 3)[0]'},
 '_continue_object_motion': {'signature': 'state, actor, opponent, frame, direction',
                             'returns': None,
                             'flow': 'from .contexts_actions import '
                                     'SceneControllerConditions\n'
                                     'checked_action(state, actor, opponent, frame)\n'
                                     'if type(direction) is not int or direction not in (0, '
                                     '1, 2, 3):\n'
                                     "    raise ValueError('one of four original motion "
                                     "directions required')\n"
                                     'axis = 2 if direction < 2 else 4\n'
                                     'speed = object_movement_speed(state)\n'
                                     'step = -low16(speed) if direction in (0, 2) else '
                                     'low16(speed)\n'
                                     'actor.set_word(axis, u16(actor.word(axis) + step))\n'
                                     'position = actor.word(axis)\n'
                                     'frame = replace(frame, x=replace_word(speed, '
                                     'position))\n'
                                     "target = _ram(state, '8156').word()\n"
                                     'difference = u16(position - target)\n'
                                     'conditions = SceneControllerConditions(position < '
                                     'target, difference == 0, bool(difference & 32768), '
                                     'bool((position ^ target) & (position ^ difference) & '
                                     '32768))\n'
                                     'finished = position <= target if direction == 0 else '
                                     'position >= target if direction == 1 else position == '
                                     'target\n'
                                     'if finished:\n'
                                     '    actor.set_word(axis, actor.word(axis) & 504)\n'
                                     '    result = _finish_action(state, actor, opponent, '
                                     'frame)\n'
                                     '    return (result, SceneControllerConditions(False, '
                                     'True, False, False))\n'
                                     'return (_result(actor, opponent, frame), conditions)'},
 'continue_object_motion_frame': {'signature': 'state, frame, direction',
                                  'returns': None,
                                'flow': 'current = checked_controller_frame(frame, state)\n'
                                          'legacy = SceneRenderFrame(current.x, current.y, '
                                          'current.attributes, current.palette, '
                                          'current.tile)\n'
                                          'action, conditions = '
                                          '_continue_object_motion(state, current.actor, '
                                          'current.traversal, legacy, direction)\n'
                                          'return replace(current, x=action.frame.x, '
                                          'conditions=conditions).validate(state)'},
 'start_object_left': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: '
                                    'SceneRenderFrame',
                       'returns': 'ObjectActionResult',
                       'flow': 'checked_action(state, actor, opponent, frame)\n'
                               'if actor.word(2) <= 0:\n'
                               '    frame = replace(frame, x=read_object_action_mode(state, '
                               'actor))\n'
                               '    if low16(frame.x) == 6:\n'
                               '        actor.set_word(2, 512)\n'
                               '    return _finish_action(state, actor, opponent, frame)\n'
                               'result = probe_object_left(state, actor, opponent, frame)\n'
                               'frame = result.frame\n'
                               'if low16(frame.x):\n'
                               '    return _finish_action(state, actor, opponent, frame)\n'
                               'frame = replace(frame, x=replace_word(frame.x, '
                               'u16(actor.word(2) - 16)))\n'
                               "_ram(state, '8156').set_word(0, low16(frame.x))\n"
                               'actor.set_word(8, 1)\n'
                               'return continue_object_left(state, actor, opponent, frame)'},
 'start_object_right': {'signature': 'state: SceneState, actor: Table, opponent: Table, '
                                     'frame: SceneRenderFrame',
                        'returns': 'ObjectActionResult',
                        'flow': 'checked_action(state, actor, opponent, frame)\n'
                                'if actor.word(2) >= 352:\n'
                                '    frame = replace(frame, x=read_object_action_mode(state, '
                                'actor))\n'
                                '    if low16(frame.x) == 6:\n'
                                '        actor.set_word(2, 512)\n'
                                '    return _finish_action(state, actor, opponent, frame)\n'
                                'result = probe_object_right(state, actor, opponent, frame)\n'
                                'frame = result.frame\n'
                                'if low16(frame.x):\n'
                                '    return _finish_action(state, actor, opponent, frame)\n'
                                'frame = replace(frame, x=replace_word(frame.x, '
                                'u16(actor.word(2) + 16)))\n'
                                "_ram(state, '8156').set_word(0, low16(frame.x))\n"
                                'actor.set_word(8, 0)\n'
                                'return continue_object_right(state, actor, opponent, frame)'},
 'start_object_up': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: '
                                  'SceneRenderFrame',
                     'returns': 'ObjectActionResult',
                     'flow': 'checked_action(state, actor, opponent, frame)\n'
                             'result = probe_object_up(state, actor, opponent, frame)\n'
                             'frame = result.frame\n'
                             'if low16(frame.x) or actor.word(4) <= 32:\n'
                             '    return _finish_action(state, actor, opponent, frame)\n'
                             'frame = replace(frame, x=replace_word(frame.x, '
                             'u16(actor.word(4) - 16)))\n'
                             "_ram(state, '8156').set_word(0, low16(frame.x))\n"
                             'actor.set_word(8, 3)\n'
                             'return continue_object_up(state, actor, opponent, frame)'},
 'start_object_down': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: '
                                    'SceneRenderFrame',
                       'returns': 'ObjectActionResult',
                       'flow': 'checked_action(state, actor, opponent, frame)\n'
                               'result = probe_object_down(state, actor, opponent, frame)\n'
                               'frame = result.frame\n'
                               'if low16(frame.x) or actor.word(4) >= 288:\n'
                               '    return _finish_action(state, actor, opponent, frame)\n'
                               'frame = replace(frame, x=replace_word(frame.x, '
                               'u16(actor.word(4) + 16)))\n'
                               "_ram(state, '8156').set_word(0, low16(frame.x))\n"
                               'actor.set_word(8, 2)\n'
                               'return continue_object_down(state, actor, opponent, frame)'},
 '_try_up': {'signature': 'state, actor, opponent, frame',
             'returns': None,
             'flow': 'actor.set_word(10, 3)\n'
                     'result = probe_object_up(state, actor, opponent, frame)\n'
                     'if low16(result.frame.x) == 0:\n'
                     '    return start_object_up(state, actor, opponent, result.frame)\n'
                     'return _pursue_horizontal(state, actor, opponent, result.frame)'},
 '_pursue_vertical': {'signature': 'state, actor, opponent, frame',
                      'returns': None,
                      'flow': 'actor.set_word(10, 3)\n'
                              'own_y = actor.word(4)\n'
                              'other_y = opponent.word(4)\n'
                              'frame = replace(frame, x=replace_word(frame.x, own_y))\n'
                              'if own_y < other_y:\n'
                              '    return _try_up(state, actor, opponent, frame)\n'
                              'actor.set_word(10, 2)\n'
                              'result = probe_object_down(state, actor, opponent, frame)\n'
                              'if low16(result.frame.x) == 0:\n'
                              '    return start_object_down(state, actor, opponent, '
                              'result.frame)\n'
                              'return _pursue_horizontal(state, actor, opponent, '
                              'result.frame)'},
 '_pursue_horizontal': {'signature': 'state, actor, opponent, frame',
                        'returns': None,
                        'flow': 'actor.set_word(10, 0)\n'
                                'own_x = actor.word(2)\n'
                                'other_x = opponent.word(2)\n'
                                'frame = replace(frame, x=replace_word(frame.x, own_x))\n'
                                'if own_x > other_x:\n'
                                '    return start_object_left(state, actor, opponent, frame)\n'
                                'actor.set_word(10, 1)\n'
                                'frame = _sample(state, frame)\n'
                                'if frame.x & 2:\n'
                                '    if actor.word(2) <= 0:\n'
                                '        return start_object_right(state, actor, opponent, '
                                'frame)\n'
                                '    result = probe_object_left(state, actor, opponent, '
                                'frame)\n'
                                '    if low16(result.frame.x) == 0:\n'
                                '        return start_object_left(state, actor, opponent, '
                                'result.frame)\n'
                                '    return start_object_right(state, actor, opponent, '
                                'result.frame)\n'
                                'if actor.word(2) >= 352:\n'
                                '    return start_object_left(state, actor, opponent, frame)\n'
                                'result = probe_object_right(state, actor, opponent, frame)\n'
                                'if low16(result.frame.x) == 0:\n'
                                '    return start_object_right(state, actor, opponent, '
                                'result.frame)\n'
                                'return start_object_left(state, actor, opponent, '
                                'result.frame)'},
 '_pursue_other_vertical': {'signature': 'state, actor, opponent, frame',
                            'returns': None,
                            'flow': 'actor.set_word(10, 3)\n'
                                    'own_y = actor.word(4)\n'
                                    'other_y = opponent.word(4)\n'
                                    'frame = replace(frame, x=replace_word(frame.x, own_y))\n'
                                    'if own_y < other_y:\n'
                                    '    return _try_up(state, actor, opponent, frame)\n'
                                    'actor.set_word(10, 2)\n'
                                    'return start_object_down(state, actor, opponent, frame)'},
 '_random_vertical_maneuver': {'signature': 'state, actor, opponent, frame',
                               'returns': None,
                               'flow': 'frame = _sample(state, frame)\n'
                                       'if frame.x & 2:\n'
                                       '    if actor.word(4) >= 288:\n'
                                       '        return _try_up(state, actor, opponent, '
                                       'frame)\n'
                                       '    result = probe_object_down(state, actor, '
                                       'opponent, frame)\n'
                                       '    if low16(result.frame.x) == 0:\n'
                                       '        return start_object_down(state, actor, '
                                       'opponent, result.frame)\n'
                                       '    return start_object_up(state, actor, opponent, '
                                       'result.frame)\n'
                                       'if actor.word(4) <= 32:\n'
                                       '    return start_object_down(state, actor, opponent, '
                                       'frame)\n'
                                       'result = probe_object_up(state, actor, opponent, '
                                       'frame)\n'
                                       'if low16(result.frame.x) == 0:\n'
                                       '    return start_object_up(state, actor, opponent, '
                                       'result.frame)\n'
                                       'return start_object_down(state, actor, opponent, '
                                       'result.frame)'},
 '_pursue_other_horizontal': {'signature': 'state, actor, opponent, frame',
                              'returns': None,
                              'flow': 'actor.set_word(10, 1)\n'
                                      'own_x = actor.word(2)\n'
                                      'other_x = opponent.word(2)\n'
                                      'frame = replace(frame, x=replace_word(frame.x, '
                                      'own_x))\n'
                                      'if own_x < other_x:\n'
                                      '    actor.set_word(10, 1)\n'
                                      '    result = probe_object_right(state, actor, '
                                      'opponent, frame)\n'
                                      '    if low16(result.frame.x) == 0:\n'
                                      '        return start_object_right(state, actor, '
                                      'opponent, result.frame)\n'
                                      '    return _pursue_other_vertical(state, actor, '
                                      'opponent, result.frame)\n'
                                      'actor.set_word(10, 0)\n'
                                      'result = probe_object_left(state, actor, opponent, '
                                      'frame)\n'
                                      'if low16(result.frame.x) == 0:\n'
                                      '    return start_object_left(state, actor, opponent, '
                                      'result.frame)\n'
                                      'return _pursue_other_vertical(state, actor, opponent, '
                                      'result.frame)'},
 'pursue_opposing_object': {'signature': 'state: SceneState, actor: Table, opponent: Table, '
                                         'frame: SceneRenderFrame',
                            'returns': 'ObjectActionResult',
                            'flow': 'checked_action(state, actor, opponent, frame)\n'
                                    "opponent = _ram(state, '816a' if actor.base >= "
                                    "4294935146 else '826a')\n"
                                    "special_layout = _ram(state, '80db').byte() == 3\n"
                                    'if not special_layout:\n'
                                    '    kind = actor.byte(1)\n'
                                    '    if kind != 0:\n'
                                    '        if actor.byte(1) == 1:\n'
                                    '            vertical = u16(actor.word(4) - '
                                    'opponent.word(4))\n'
                                    '            if negative_word(vertical):\n'
                                    '                vertical = u16(-vertical)\n'
                                    '            frame = replace(frame, '
                                    'x=replace_word(frame.x, vertical))\n'
                                    '            if vertical > 16:\n'
                                    '                return _pursue_vertical(state, actor, '
                                    'opponent, frame)\n'
                                    '            return _pursue_other_horizontal(state, '
                                    'actor, opponent, frame)\n'
                                    '        actor.byte(1)\n'
                                    '        horizontal = u16(actor.word(2) - '
                                    'opponent.word(2))\n'
                                    '        if negative_word(horizontal):\n'
                                    '            horizontal = u16(-horizontal)\n'
                                    '        frame = replace(frame, x=replace_word(frame.x, '
                                    'horizontal))\n'
                                    '        if horizontal <= 16:\n'
                                    '            return _pursue_vertical(state, actor, '
                                    'opponent, frame)\n'
                                    'horizontal = u16(actor.word(2) - opponent.word(2))\n'
                                    'if negative_word(horizontal):\n'
                                    '    horizontal = u16(-horizontal)\n'
                                    'vertical = u16(actor.word(4) - opponent.word(4))\n'
                                    'if negative_word(vertical):\n'
                                    '    vertical = u16(-vertical)\n'
                                    'frame = replace(frame, x=replace_word(frame.x, '
                                    'horizontal), y=replace_word(frame.y, vertical))\n'
                                    'if vertical < horizontal:\n'
                                    '    return _pursue_other_horizontal(state, actor, '
                                    'opponent, frame)\n'
                                    'return _pursue_vertical(state, actor, opponent, frame)'},
 'sidestep_opposing_object': {'signature': 'state: SceneState, actor: Table, opponent: Table, '
                                           'frame: SceneRenderFrame',
                              'returns': 'ObjectActionResult',
                              'flow': 'checked_action(state, actor, opponent, frame)\n'
                                      'if actor.base >= 4294935146:\n'
                                      '    actor.set_word(10, 1)\n'
                                      '    result = probe_object_right(state, actor, '
                                      'opponent, frame)\n'
                                      '    if low16(result.frame.x) == 0:\n'
                                      '        return start_object_right(state, actor, '
                                      'opponent, result.frame)\n'
                                      'else:\n'
                                      '    actor.set_word(10, 0)\n'
                                      '    result = probe_object_left(state, actor, opponent, '
                                      'frame)\n'
                                      '    if low16(result.frame.x) == 0:\n'
                                      '        return start_object_left(state, actor, '
                                      'opponent, result.frame)\n'
                                      'actor.set_word(10, 3)\n'
                                      'frame = _sample(state, result.frame)\n'
                                      'opponent.word(4)\n'
                                      'if frame.x & 16:\n'
                                      '    return _try_up(state, actor, opponent, frame)\n'
                                      'actor.set_word(10, 2)\n'
                                      'return start_object_down(state, actor, opponent, '
                                      'frame)'},
 'resume_object_selected_action': {'signature': 'state: SceneState, actor: Table, opponent: '
                                                'Table, frame: SceneRenderFrame',
                                   'returns': 'ObjectActionResult',
                                   'flow': 'checked_action(state, actor, opponent, frame)\n'
                                           'return resume_selected_object_action(state, '
                                           'actor, opponent, frame)'},
 '_dispatch_primary_action': {'signature': 'state, actor, opponent, frame, *, resumed',
                              'returns': None,
                              'flow': 'selector = low16(frame.x)\n'
                                      'if resumed:\n'
                                      '    if selector == 0:\n'
                                      '        return continue_object_left(state, actor, '
                                      'opponent, frame)\n'
                                      '    if selector == 4:\n'
                                      '        return continue_object_right(state, actor, '
                                      'opponent, frame)\n'
                                      '    if selector == 8:\n'
                                      '        return continue_object_up(state, actor, '
                                      'opponent, frame)\n'
                                      '    if selector == 12:\n'
                                      '        return continue_object_down(state, actor, '
                                      'opponent, frame)\n'
                                      '    if selector == 16:\n'
                                      '        return finish_object_action_noop(state, actor, '
                                      'opponent, frame)\n'
                                      '    if selector in (20, 24, 28):\n'
                                      '        return resume_object_pursuit(state, actor, '
                                      'opponent, frame)\n'
                                      '    if selector == 32:\n'
                                      '        return advance_object_impact(state, actor, '
                                      'opponent, frame)\n'
                                      '    if selector == 36:\n'
                                      '        return advance_object_projectile(state, actor, '
                                      'opponent, frame)\n'
                                      '    base = 265550\n'
                                      'else:\n'
                                      '    if selector == 0:\n'
                                      '        return start_object_left(state, actor, '
                                      'opponent, frame)\n'
                                      '    if selector == 4:\n'
                                      '        return start_object_right(state, actor, '
                                      'opponent, frame)\n'
                                      '    if selector == 8:\n'
                                      '        return start_object_up(state, actor, opponent, '
                                      'frame)\n'
                                      '    if selector == 12:\n'
                                      '        return start_object_down(state, actor, '
                                      'opponent, frame)\n'
                                      '    if selector == 16:\n'
                                      '        return _resume_primary_action_selection(state, '
                                      'actor, opponent, frame)\n'
                                      '    if selector == 20:\n'
                                      '        return pursue_opposing_object(state, actor, '
                                      'opponent, frame)\n'
                                      '    if selector == 24:\n'
                                      '        return sidestep_opposing_object(state, actor, '
                                      'opponent, frame)\n'
                                      '    base = 265484\n'
                                      'result = state.service_at(u32(base + s16(selector)), '
                                      'ObjectVectorContext(actor, opponent, frame, frame.x))\n'
                                      'if type(result) is not ObjectActionResult:\n'
                                      "    raise Boundary('action vector must provide actual "
                                      "typed continuation')\n"
                                      'return result.validate(state)'},
 '_resume_primary_action_selection': {'signature': 'state, actor, opponent, frame',
                                      'returns': None,
                                      'flow': 'from .services import '
                                              'resume_selected_object_action_complete\n'
                                              'checked_action(state, actor, opponent, frame)\n'
                                              'current = checked_controller_frame(frame, '
                                              'state)\n'
                                              'if current.actor.base != actor.base or '
                                              'current.traversal.base != opponent.base:\n'
                                              "    raise ValueError('alternate caller views "
                                              "must match the current A6/A5')\n"
                                              'outcome = '
                                              'resume_selected_object_action_complete(state, '
                                              'current).validate(state)\n'
                                              'actual = outcome.frame\n'
                                              'projected = SceneRenderFrame(actual.x, '
                                              'actual.y, actual.attributes, actual.palette, '
                                              'actual.tile, actual)\n'
                                              'return ObjectActionResult(actual.actor, '
                                              'actual.traversal, projected, '
                                              'outcome.discarded_continuation).validate(state)'},
 'finish_object_action_noop': {'signature': 'state: SceneState, actor: Table, opponent: '
                                            'Table, frame: SceneRenderFrame',
                               'returns': 'ObjectActionResult',
                               'flow': 'checked_action(state, actor, opponent, frame)\n'
                                       'return _finish_action(state, actor, opponent, frame)'},
 '_resume_pursuit_direction': {'signature': 'state, actor, opponent, frame',
                               'returns': None,
                               'flow': 'selector = replace_word(frame.x, u16(actor.word(10) '
                                       '<< 2))\n'
                                       'frame = replace(frame, x=selector)\n'
                                       'direction = low16(selector)\n'
                                       'if direction == 0:\n'
                                       '    return continue_object_left(state, actor, '
                                       'opponent, frame)\n'
                                       'if direction == 4:\n'
                                       '    return continue_object_right(state, actor, '
                                       'opponent, frame)\n'
                                       'if direction == 8:\n'
                                       '    return continue_object_up(state, actor, opponent, '
                                       'frame)\n'
                                       'if direction == 12:\n'
                                       '    return continue_object_down(state, actor, '
                                       'opponent, frame)\n'
                                       'result = state.service_at(u32(266120 + '
                                       's16(direction)), ObjectVectorContext(actor, opponent, '
                                       'frame, selector))\n'
                                       'if type(result) is not ObjectActionResult:\n'
                                       "    raise Boundary('unknown pursuit vector requires "
                                       "typed actual outcome')\n"
                                       'return result.validate(state)'},
 'resume_object_pursuit': {'signature': 'state: SceneState, actor: Table, opponent: Table, '
                                        'frame: SceneRenderFrame',
                           'returns': 'ObjectActionResult',
                           'flow': 'checked_action(state, actor, opponent, frame)\n'
                                   'return _resume_pursuit_direction(state, actor, opponent, '
                                   'frame)'},
 'resume_object_pursuit_alias': {'signature': 'state: SceneState, actor: Table, opponent: '
                                              'Table, frame: SceneRenderFrame',
                                 'returns': 'ObjectActionResult',
                                 'flow': 'return resume_object_pursuit(state, actor, '
                                         'opponent, frame)'},
 'resume_object_pursuit_second_alias': {'signature': 'state: SceneState, actor: Table, '
                                                     'opponent: Table, frame: '
                                                     'SceneRenderFrame',
                                        'returns': 'ObjectActionResult',
                                        'flow': 'return resume_object_pursuit(state, actor, '
                                                'opponent, frame)'},
 'continue_object_left_vector': {'signature': 'state: SceneState, actor: Table, opponent: '
                                              'Table, frame: SceneRenderFrame',
                                 'returns': 'ObjectActionResult',
                                 'flow': 'return continue_object_left(state, actor, opponent, '
                                         'frame)'},
 'continue_object_right_vector': {'signature': 'state: SceneState, actor: Table, opponent: '
                                               'Table, frame: SceneRenderFrame',
                                  'returns': 'ObjectActionResult',
                                  'flow': 'return continue_object_right(state, actor, '
                                          'opponent, frame)'},
 'continue_object_up_vector': {'signature': 'state: SceneState, actor: Table, opponent: '
                                            'Table, frame: SceneRenderFrame',
                               'returns': 'ObjectActionResult',
                               'flow': 'return continue_object_up(state, actor, opponent, '
                                       'frame)'},
 'continue_object_down_vector': {'signature': 'state: SceneState, actor: Table, opponent: '
                                              'Table, frame: SceneRenderFrame',
                                 'returns': 'ObjectActionResult',
                                 'flow': 'return continue_object_down(state, actor, opponent, '
                                         'frame)'},
 'adjust_damage_for_object_guard': {'signature': 'state: SceneState, actor: Table, opponent: '
                                                 'Table, frame: SceneRenderFrame',
                                    'returns': 'ObjectActionResult',
                                    'flow': 'checked_action(state, actor, opponent, frame)\n'
                                            'if opponent.byte(1) != 3:\n'
                                            '    return _result(actor, opponent, frame)\n'
                                            'divisor = replace_word(frame.attributes, '
                                            "_ram(state, '8104').word())\n"
                                            "if _ram(state, '814c').word() != 2:\n"
                                            '    divisor = replace_word(divisor, _ram(state, '
                                            "'8106').word())\n"
                                            'divisor = replace_word(divisor, low16(divisor) '
                                            '>> 1)\n'
                                            'if low16(divisor) == 0:\n'
                                            '    divisor = replace_word(divisor, 1)\n'
                                            'damage = divu_retained(frame.y & 65535, '
                                            'low16(divisor))\n'
                                            'return _result(actor, opponent, replace(frame, '
                                            'y=damage, attributes=divisor))'},
 '_weighted_damage': {'signature': 'state, actor, frame, factor',
                      'returns': None,
                      'flow': 'command = replace_word(frame.x, actor.word(14))\n'
                              'strength = replace_word(frame.y, actor.word(12))\n'
                              'damage = divu_retained(low16(strength) * low16(command), 100)\n'
                              'frame = _sample(state, replace(frame, x=command))\n'
                              'command = replace_word(frame.x, u16((low16(frame.x) & 31) + '
                              'factor))\n'
                              'damage = divu_retained(low16(damage) * low16(command), 100)\n'
                              'return replace(frame, x=command, y=damage)'},
 'calculate_object_impact_damage': {'signature': 'state: SceneState, actor: Table, opponent: '
                                                 'Table, frame: SceneRenderFrame',
                                    'returns': 'ObjectActionResult',
                                    'flow': 'checked_action(state, actor, opponent, frame)\n'
                                            'if actor.byte(1) == 0:\n'
                                            '    frame = _weighted_damage(state, actor, '
                                            'frame, 60)\n'
                                            'elif actor.byte(1) == 1:\n'
                                            '    frame = _weighted_damage(state, actor, '
                                            'frame, 80)\n'
                                            'elif actor.byte(1) == 2:\n'
                                            '    frame = _weighted_damage(state, actor, '
                                            'frame, 120)\n'
                                            'else:\n'
                                            '    frame = replace(frame, '
                                            'y=replace_word(frame.y, actor.word(12)))\n'
                                            'return adjust_damage_for_object_guard(state, '
                                            'actor, opponent, frame)'},
 '_apply_object_damage': {'signature': 'state, actor, opponent, frame',
                          'returns': None,
                          'flow': 'remaining = u16(opponent.word(14) - low16(frame.y))\n'
                                  'opponent.set_word(14, remaining)\n'
                                  'if remaining != 0 and (not negative_word(remaining)):\n'
                                  '    return _finish_action(state, actor, opponent, frame)\n'
                                  'opponent.set_word(14, 0)\n'
                                  'opponent.set_word(0, 0)\n'
                                  'if opponent.base >= 4294935146:\n'
                                  "    if _ram(state, '826a').word() != 0:\n"
                                  '        return _finish_action(state, actor, opponent, '
                                  'frame)\n'
                                  "    _ram(state, '8114').set_word(0, 2)\n"
                                  "    _ram(state, '8116').set_word(0, 3)\n"
                                  'else:\n'
                                  "    if _ram(state, '816a').word() != 0:\n"
                                  '        return _finish_action(state, actor, opponent, '
                                  'frame)\n'
                                  "    _ram(state, '8114').set_word(0, 3)\n"
                                  "    _ram(state, '8116').set_word(0, 0)\n"
                                  "_ram(state, '813a').set_word(0, 4)\n"
                                  "_ram(state, '813c').set_word(0, 0)\n"
                                  "_ram(state, '813e').set_word(0, 1)\n"
                                  'command = replace_word(frame.x, u16(_ram(state, '
                                  "'814c').word() - 1) ^ 1)\n"
                                  "_ram(state, '8176').set_word(0, low16(command))\n"
                                  'return _finish_action(state, actor, opponent, '
                                  'replace(frame, x=command))'},
 '_draw_object_impact_flash': {'signature': 'state, actor, opponent, frame, *, '
                                            'projectile=False',
                               'returns': None,
                               'flow': 'saved_position = actor.long(2)\n'
                                       "direction = u16(_ram(state, '8158').word() << 2)\n"
                                       'horizontal = state.table(267752).word(direction)\n'
                                       'vertical = state.table(267754).word(direction)\n'
                                       'frame = replace(frame, x=replace_word(saved_position, '
                                       'horizontal), y=replace_word(frame.y, vertical), '
                                       'attributes=replace_word(frame.attributes, '
                                       'direction))\n'
                                       'offset_scene_object_position(state, actor, '
                                       'ObjectPositionOffset(horizontal, vertical))\n'
                                       'if projectile:\n'
                                       "    horizontal = _ram(state, '8164').word()\n"
                                       "    vertical = _ram(state, '8166').word()\n"
                                       'else:\n'
                                       '    horizontal, vertical = (actor.word(2), '
                                       'actor.word(4))\n'
                                       'frame = replace(frame, x=replace_word(frame.x, '
                                       'horizontal), y=replace_word(frame.y, vertical), '
                                       'attributes=replace_word(frame.attributes, 4), '
                                       'palette=0, tile=replace_word(frame.tile, 256))\n'
                                       'source = state.table(267746).cursor()\n'
                                       'frame = append_scene_sprite_entries(state, '
                                       'SpriteBatchContext(source, frame)).frame\n'
                                       'frame = replace(frame, x=saved_position)\n'
                                       'actor.set_long(2, saved_position)\n'
                                       'return _result(actor, opponent, frame)'},
 'advance_object_impact': {'signature': 'state: SceneState, actor: Table, opponent: Table, '
                                        'frame: SceneRenderFrame',
                           'returns': 'ObjectActionResult',
                           'flow': 'checked_action(state, actor, opponent, frame)\n'
                                   "_ram(state, '8162').set_word(0, u16(_ram(state, "
                                   "'8162').word() + 1))\n"
                                   'frame = replace(frame, x=replace_word(frame.x, '
                                   "_ram(state, '8162').word()), y=16)\n"
                                   "_ram(state, '840a').word()\n"
                                   'if low16(frame.x) < 16:\n'
                                   '    return _draw_object_impact_flash(state, actor, '
                                   'opponent, frame)\n'
                                   "opponent = state.table(_ram(state, '815c').long())\n"
                                   'result = calculate_object_impact_damage(state, actor, '
                                   'opponent, frame)\n'
                                   'return _apply_object_damage(state, actor, opponent, '
                                   'result.frame)'},
 'advance_object_projectile': {'signature': 'state: SceneState, actor: Table, opponent: '
                                            'Table, frame: SceneRenderFrame',
                               'returns': 'ObjectActionResult',
                               'flow': 'checked_action(state, actor, opponent, frame)\n'
                                       "opponent = state.table(_ram(state, '815c').long())\n"
                                       'command = replace_word(frame.x, _ram(state, '
                                       "'8164').word())\n"
                                       'arrived = low16(command) == opponent.word(2)\n'
                                       'if arrived:\n'
                                       '    command = replace_word(command, _ram(state, '
                                       "'8166').word())\n"
                                       '    arrived = low16(command) == opponent.word(4)\n'
                                       'frame = replace(frame, x=command)\n'
                                       'if arrived:\n'
                                       "    if _ram(state, '8168').word() == 0:\n"
                                       '        frame = replace(frame, '
                                       'x=replace_word(frame.x, 170))\n'
                                       '        enqueue_sound_command(state, low8(frame.x))\n'
                                       "    _ram(state, '8168').set_word(0, u16(_ram(state, "
                                       "'8168').word() + 1))\n"
                                       '    frame = replace(frame, x=replace_word(frame.x, '
                                       "_ram(state, '8168').word()), y=16)\n"
                                       "    _ram(state, '840a').word()\n"
                                       '    if low16(frame.x) < 16:\n'
                                       '        return _draw_object_impact_flash(state, '
                                       'actor, opponent, frame, projectile=True)\n'
                                       '    frame = _weighted_damage(state, actor, frame, '
                                       '80)\n'
                                       '    result = adjust_damage_for_object_guard(state, '
                                       'actor, opponent, frame)\n'
                                       '    return _apply_object_damage(state, actor, '
                                       'opponent, result.frame)\n'
                                       "speed = 4 if _ram(state, '840a').word() == 0 else 8\n"
                                       'frame = replace(frame, x=speed)\n'
                                       'if actor.word(8) == 0:\n'
                                       "    _ram(state, '8164').set_word(0, u16(_ram(state, "
                                       "'8164').word() + speed))\n"
                                       'elif actor.word(8) == 1:\n'
                                       "    _ram(state, '8164').set_word(0, u16(_ram(state, "
                                       "'8164').word() - speed))\n"
                                       'elif actor.word(8) == 2:\n'
                                       "    _ram(state, '8166').set_word(0, u16(_ram(state, "
                                       "'8166').word() + speed))\n"
                                       'elif actor.word(8) == 3:\n'
                                       "    _ram(state, '8166').set_word(0, u16(_ram(state, "
                                       "'8166').word() - speed))\n"
                                       'direction = u16(actor.word(8) << 2)\n'
                                       'source = '
                                       'state.table(state.table(268238).long(direction)).cursor()\n'
                                       'frame = replace(frame, x=replace_word(speed, '
                                       "_ram(state, '8164').word()), y=replace_word(frame.y, "
                                       "_ram(state, '8166').word()), "
                                       'attributes=replace_word(frame.attributes, 4), '
                                       'palette=0, tile=replace_word(frame.tile, 768))\n'
                                       'frame = append_scene_sprite_entries(state, '
                                       'SpriteBatchContext(source, frame)).frame\n'
                                       'return _result(actor, opponent, frame)'},
 'sum_live_object_rosters': {'signature': 'state: SceneState, retained_command: Long=0',
                             'returns': 'ObjectRosterTotals',
                             'flow': 'checked_state(state)\n'
                                     'uint(retained_command, 32)\n'
                                     'first_total, first_count = (0, 0)\n'
                                     "actor = _ram(state, '817a').cursor()\n"
                                     'for _ in descending_inclusive(14):\n'
                                     '    if actor.byte() & 128:\n'
                                     '        first_total = u16(first_total + '
                                     'actor.word(14))\n'
                                     '        first_count = u16(first_count + 1)\n'
                                     '    actor = actor.advance(16)\n'
                                     'second_total, second_count = (0, 0)\n'
                                     "actor = _ram(state, '827a').cursor()\n"
                                     'for _ in descending_inclusive(14):\n'
                                     '    if actor.byte() & 128:\n'
                                     '        second_total = u16(second_total + '
                                     'actor.word(14))\n'
                                     '        second_count = u16(second_count + 1)\n'
                                     '    actor = actor.advance(16)\n'
                                     'return ObjectRosterTotals(first_total, second_total, '
                                     'first_count, second_count, '
                                     'replace_word(retained_command, 65535), actor)'},
 '_roster_frame': {'signature': 'state, actor, opponent, frame',
                   'returns': None,
                   'flow': 'totals = sum_live_object_rosters(state, frame.x)\n'
                           'frame = SceneRenderFrame(totals.command, totals.first_total, '
                           'totals.second_total, totals.first_count, totals.second_count)\n'
                           'return _result(totals.roster_end, opponent, frame)'},
 '_set_all_object_retreat_modes': {'signature': 'state',
                                   'returns': None,
                                   'flow': "for name in ('812a', '812c', '812e', '8130'):\n"
                                           '    _ram(state, name).set_word(0, 6)'},
 '_masked_retreat_roll': {'signature': 'state, actor, opponent, frame, table',
                          'returns': None,
                          'flow': 'frame = _sample(state, frame)\n'
                                  "difficulty = _ram(state, 'efd2').word()\n"
                                  'mask = state.table(table).byte(difficulty)\n'
                                  'frame = replace(frame, x=replace_byte(frame.x, '
                                  'low8(frame.x) & mask), y=replace_word(frame.y, '
                                  'difficulty))\n'
                                  'return _result(actor, opponent, frame)'},
 'trigger_object_retreat_strength': {'signature': 'state: SceneState, actor: Table, opponent: '
                                                  'Table, frame: SceneRenderFrame',
                                     'returns': 'ObjectActionResult',
                                     'flow': 'checked_action(state, actor, opponent, frame)\n'
                                             'result = _roster_frame(state, actor, opponent, '
                                             'frame)\n'
                                             'actor, frame = (result.actor, result.frame)\n'
                                             'frame = replace(frame, '
                                             'palette=replace_word(frame.palette, '
                                             'u16(low16(frame.y) << 1)))\n'
                                             'if low16(frame.attributes) <= '
                                             'low16(frame.palette) or low16(frame.y) > 1000:\n'
                                             '    return _result(actor, opponent, frame)\n'
                                             'result = _masked_retreat_roll(state, actor, '
                                             'opponent, frame, 270068)\n'
                                             'if low8(result.frame.x):\n'
                                             '    return '
                                             'trigger_object_retreat_low_strength(state, '
                                             'actor, opponent, result.frame)\n'
                                             '_set_all_object_retreat_modes(state)\n'
                                             'return result'},
 'trigger_object_retreat_low_strength': {'signature': 'state: SceneState, actor: Table, '
                                                      'opponent: Table, frame: '
                                                      'SceneRenderFrame',
                                         'returns': 'ObjectActionResult',
                                         'flow': 'checked_action(state, actor, opponent, '
                                                 'frame)\n'
                                                 'result = _roster_frame(state, actor, '
                                                 'opponent, frame)\n'
                                                 'actor, frame = (result.actor, '
                                                 'result.frame)\n'
                                                 'frame = replace(frame, '
                                                 'palette=replace_word(frame.palette, '
                                                 'u16(low16(frame.y) << 1)))\n'
                                                 'if low16(frame.attributes) <= '
                                                 'low16(frame.palette) or low16(frame.y) > '
                                                 '500:\n'
                                                 '    return _result(actor, opponent, frame)\n'
                                                 'result = _masked_retreat_roll(state, actor, '
                                                 'opponent, frame, 270072)\n'
                                                 'if low8(result.frame.x) == 0:\n'
                                                 '    _set_all_object_retreat_modes(state)\n'
                                                 'return result'},
 'trigger_object_retreat_outnumbered': {'signature': 'state: SceneState, actor: Table, '
                                                     'opponent: Table, frame: '
                                                     'SceneRenderFrame',
                                        'returns': 'ObjectActionResult',
                                        'flow': 'checked_action(state, actor, opponent, '
                                                'frame)\n'
                                                'result = _roster_frame(state, actor, '
                                                'opponent, frame)\n'
                                                'actor, frame = (result.actor, result.frame)\n'
                                                'frame = replace(frame, '
                                                'palette=replace_word(frame.palette, '
                                                'u16(low16(frame.palette) << 1)))\n'
                                                'if low16(frame.tile) <= '
                                                'low16(frame.palette):\n'
                                                '    return _result(actor, opponent, frame)\n'
                                                'if low16(frame.attributes) <= '
                                                'low16(frame.y):\n'
                                                '    return _result(actor, opponent, frame)\n'
                                                'result = _masked_retreat_roll(state, actor, '
                                                'opponent, frame, 270076)\n'
                                                'if low8(result.frame.x) == 0:\n'
                                                '    _set_all_object_retreat_modes(state)\n'
                                                'return result'},
 'trigger_object_retreat_morale': {'signature': 'state: SceneState, actor: Table, opponent: '
                                                'Table, frame: SceneRenderFrame',
                                   'returns': 'ObjectActionResult',
                                   'flow': 'checked_action(state, actor, opponent, frame)\n'
                                           'result = _roster_frame(state, actor, opponent, '
                                           'frame)\n'
                                           'actor, frame = (result.actor, result.frame)\n'
                                           'if low16(frame.attributes) <= low16(frame.y):\n'
                                           '    return result\n'
                                           "if _ram(state, '8178').word() >= 30:\n"
                                           '    return result\n'
                                           'frame = _sample(state, frame)\n'
                                           "difficulty = _ram(state, 'efd2').word()\n"
                                           'frame = replace(frame, y=replace_word(frame.y, '
                                           'difficulty))\n'
                                           'if difficulty == 2:\n'
                                           '    frame = replace(frame, '
                                           'x=replace_word(frame.x, low16(frame.x) & 7))\n'
                                           '    retreat = low16(frame.x) < 5\n'
                                           'else:\n'
                                           '    mask = state.table(270080).byte(difficulty)\n'
                                           '    frame = replace(frame, '
                                           'x=replace_byte(frame.x, low8(frame.x) & mask))\n'
                                           '    retreat = low8(frame.x) == 0\n'
                                           'if retreat:\n'
                                           '    _set_all_object_retreat_modes(state)\n'
                                           'return _result(actor, opponent, frame)'},
 'trigger_object_retreat_quality': {'signature': 'state: SceneState, actor: Table, opponent: '
                                                 'Table, frame: SceneRenderFrame',
                                    'returns': 'ObjectActionResult',
                                    'flow': 'checked_action(state, actor, opponent, frame)\n'
                                            'result = _roster_frame(state, actor, opponent, '
                                            'frame)\n'
                                            'actor, frame = (result.actor, result.frame)\n'
                                            'command = replace_word(frame.x, _ram(state, '
                                            "'8104').word())\n"
                                            'frame = replace(frame, x=command)\n'
                                            'if low16(command) >= _ram(state, '
                                            "'8106').word():\n"
                                            '    return _result(actor, opponent, frame)\n'
                                            'command = replace_word(command, _ram(state, '
                                            "'8178').word())\n"
                                            'frame = replace(frame, x=command)\n'
                                            'if low16(command) >= _ram(state, '
                                            "'8278').word():\n"
                                            '    return _result(actor, opponent, frame)\n'
                                            "if _ram(state, '8178').word() >= 30:\n"
                                            '    return _result(actor, opponent, frame)\n'
                                            'result = _masked_retreat_roll(state, actor, '
                                            'opponent, frame, 270084)\n'
                                            'if low8(result.frame.x) == 0:\n'
                                            '    _set_all_object_retreat_modes(state)\n'
                                            'return result'},
 'advance_object_retreat_checks': {'signature': 'state: SceneState, actor: Table, opponent: '
                                                'Table, frame: SceneRenderFrame',
                                   'returns': 'ObjectActionResult',
                                   'flow': 'checked_action(state, actor, opponent, frame)\n'
                                           "if _ram(state, '8160').word() < 11:\n"
                                           '    return _result(actor, opponent, frame)\n'
                                           'result = trigger_object_retreat_strength(state, '
                                           'actor, opponent, frame)\n'
                                           'result = '
                                           'trigger_object_retreat_low_strength(state, '
                                           'result.actor, result.opponent, result.frame)\n'
                                           'result = '
                                           'trigger_object_retreat_outnumbered(state, '
                                           'result.actor, result.opponent, result.frame)\n'
                                           'result = trigger_object_retreat_morale(state, '
                                           'result.actor, result.opponent, result.frame)\n'
                                           'return trigger_object_retreat_quality(state, '
                                           'result.actor, result.opponent, result.frame)'},
 'choose_object_retreat_phase': {'signature': 'state: SceneState, actor: Table, opponent: '
                                              'Table, frame: SceneRenderFrame',
                                 'returns': 'ObjectActionResult',
                                 'flow': 'checked_action(state, actor, opponent, frame)\n'
                                         'command = replace_word(frame.x, _ram(state, '
                                         "'80dc').word())\n"
                                         'frame = replace(frame, x=command)\n'
                                         "if low16(command) == _ram(state, '80e0').word():\n"
                                         '    return _result(actor, opponent, frame)\n'
                                         'result = _roster_frame(state, actor, opponent, '
                                         'frame)\n'
                                         'actor, frame = (result.actor, result.frame)\n'
                                         'if low16(frame.attributes) <= low16(frame.y):\n'
                                         '    return result\n'
                                         "difficulty = _ram(state, 'efd2').word()\n"
                                         'frame = replace(frame, x=replace_word(frame.x, '
                                         'difficulty), y=replace_word(frame.y, _ram(state, '
                                         "'8178').word()))\n"
                                         'threshold = state.table(270316).byte(difficulty)\n'
                                         'if low8(frame.y) >= threshold:\n'
                                         '    return _result(actor, opponent, frame)\n'
                                         'frame = replace(frame, x=replace_word(frame.x, '
                                         "_ram(state, '8178').word()))\n"
                                         "if low16(frame.x) >= _ram(state, '8278').word():\n"
                                         '    return _result(actor, opponent, frame)\n'
                                         "actor = _ram(state, '816a')\n"
                                         'result = _probe(state, actor, opponent, frame, '
                                         '32784, 0, restore=False)\n'
                                         'if low16(result.frame.x) == 0:\n'
                                         '    result = _probe(state, actor, result.opponent, '
                                         'result.frame, 16, 0, restore=False)\n'
                                         'if low16(result.frame.x) == 0:\n'
                                         '    result = _probe(state, actor, result.opponent, '
                                         'result.frame, 32784, 32784, restore=False)\n'
                                         'if low16(result.frame.x) == 0:\n'
                                         '    result = _probe(state, actor, result.opponent, '
                                         'result.frame, 16, 32784, restore=False)\n'
                                         'if low16(result.frame.x) == 0:\n'
                                         '    return result\n'
                                         'frame = _sample(state, result.frame)\n'
                                         'frame = replace(frame, x=replace_word(frame.x, '
                                         'low16(frame.x) & 3))\n'
                                         'if low16(frame.x):\n'
                                         "    _ram(state, '813a').set_word(0, 6)\n"
                                         "    _ram(state, '813c').set_word(0, 0)\n"
                                         "    _ram(state, '813e').set_word(0, 1)\n"
                                         'return _result(actor, result.opponent, frame)'},
 'dispatch_object_formation_ai': {'signature': 'state: SceneState, actor: Table, opponent: '
                                               'Table, frame: SceneRenderFrame',
                                  'returns': 'ObjectActionResult',
                                  'flow': 'checked_action(state, actor, opponent, frame)\n'
                                          'selector = replace_word(frame.x, u16(_ram(state, '
                                          "'814a').word() << 2))\n"
                                          'frame = replace(frame, x=selector)\n'
                                          'result = state.service_at(u32(269294 + '
                                          's16(low16(selector))), ObjectVectorContext(actor, '
                                          'opponent, frame, selector))\n'
                                          'if type(result) is not ObjectActionResult:\n'
                                          "    raise Boundary('formation vector must provide "
                                          "actual typed continuation')\n"
                                          'return result.validate(state)'},
 'dispatch_object_formation_fallback': {'signature': 'state: SceneState, actor: Table, '
                                                     'opponent: Table, frame: '
                                                     'SceneRenderFrame',
                                        'returns': 'ObjectActionResult',
                                        'flow': 'checked_action(state, actor, opponent, '
                                                'frame)\n'
                                                "if _ram(state, '8130').word() == 6:\n"
                                                '    return _result(actor, opponent, frame)\n'
                                                'selector = replace_word(frame.x, '
                                                "u16(_ram(state, '814a').word() << 2))\n"
                                                'frame = replace(frame, x=selector)\n'
                                                'result = state.service_at(u32(269546 + '
                                                's16(low16(selector))), '
                                                'ObjectVectorContext(actor, opponent, frame, '
                                                'selector))\n'
                                                'if type(result) is not ObjectActionResult:\n'
                                                "    raise Boundary('fallback vector must "
                                                "provide actual typed continuation')\n"
                                                'return result.validate(state)'},
 'update_object_action_ai': {'signature': 'state: SceneState, actor: Table, opponent: Table, '
                                          'frame: SceneRenderFrame',
                             'returns': 'ObjectActionResult',
                             'flow': 'checked_action(state, actor, opponent, frame)\n'
                                     "if _ram(state, '80da').byte() == 1:\n"
                                     '    return _result(actor, opponent, frame)\n'
                                     "if _ram(state, '80da').byte() == 2:\n"
                                     '    return _result(actor, opponent, frame)\n'
                                     "if _ram(state, '814c').byte() != 0:\n"
                                     '    return _result(actor, opponent, frame)\n'
                                     "if _ram(state, '812a').word() == 6:\n"
                                     '    return _result(actor, opponent, frame)\n'
                                     'result = dispatch_object_formation_ai(state, actor, '
                                     'opponent, frame)\n'
                                     'result = dispatch_object_formation_fallback(state, '
                                     'result.actor, result.opponent, result.frame)\n'
                                     'result = choose_object_retreat_phase(state, '
                                     'result.actor, result.opponent, result.frame)\n'
                                     'return advance_object_retreat_checks(state, '
                                     'result.actor, result.opponent, result.frame)'},
 'upload_object_officer_name': {'signature': 'state: SceneState, officer: Long, glyphs: '
                                             'DuelGlyphContext',
                                'returns': 'ObjectGlyphResult',
                                'flow': 'checked_state(state)\n'
                                        'uint(officer, 32)\n'
                                        'if type(glyphs) is not DuelGlyphContext:\n'
                                        "    raise ValueError('typed glyph color/count "
                                        "carriers required')\n"
                                        'glyphs.validate()\n'
                                        'officer_offset = low16(officer) * 6\n'
                                        'source = '
                                        'state.table(566532).cursor(low16(officer_offset))\n'
                                        'remaining = replace_word(glyphs.remaining, 2)\n'
                                        "destination = _ram(state, 'd300').cursor()\n"
                                        'if source.word(4) == 63:\n'
                                        '    remaining = replace_word(remaining, 1)\n'
                                        '    pattern = u16(low16(glyphs.background) << 4 | '
                                        'low16(glyphs.background))\n'
                                        "    other = _ram(state, 'd440').cursor()\n"
                                        '    for _ in descending_inclusive(63):\n'
                                        '        destination.append_byte(low8(pattern))\n'
                                        '        other.append_byte(low8(pattern))\n'
                                        'decoded = decode_glyph_rows_to_buffers(state, '
                                        'source, destination, glyphs.background, '
                                        'glyphs.foreground, remaining)\n'
                                        "source = _ram(state, 'd300').cursor()\n"
                                        'for _ in descending_inclusive(95):\n'
                                        '    state.write(12582912, 4, source.next_long())\n'
                                        'glyphs = DuelGlyphContext(decoded.background, '
                                        'decoded.foreground, decoded.remaining)\n'
                                        'return ObjectGlyphResult(glyphs, source, '
                                        'replace_word(decoded.background, 65535), '
                                        'officer_offset)'},
 'upload_one_scene_tile': {'signature': 'state: SceneState, source: Cursor, frame: '
                                        'SceneRenderFrame',
                           'returns': 'TileUploadResult',
                           'flow': 'checked_state(state)\n'
                                   'checked_cursor(source, state)\n'
                                   'frame.validate(state)\n'
                                   'index = u32((frame.attributes & 65535) << 5)\n'
                                   'bank = state.table(746650).cursor().advance(index)\n'
                                   'for _ in descending_inclusive(7):\n'
                                   '    state.write(12582912, 4, bank.next_long())\n'
                                   'frame = replace(frame, attributes=index, '
                                   'palette=replace_word(frame.palette, 65535))\n'
                                   'return TileUploadResult(source, bank, frame)'},
 'upload_scene_tile_block': {'signature': 'state: SceneState, source: Cursor, frame: '
                                          'SceneRenderFrame',
                             'returns': 'TileUploadResult',
                             'flow': 'checked_state(state)\n'
                                     'checked_cursor(source, state)\n'
                                     'frame.validate(state)\n'
                                     'result = None\n'
                                     'for _ in descending_inclusive(47):\n'
                                     '    frame = replace(frame, '
                                     'attributes=replace_word(frame.attributes, '
                                     'source.next_word()))\n'
                                     '    result = upload_one_scene_tile(state, source, '
                                     'frame)\n'
                                     '    frame = result.frame\n'
                                     'return TileUploadResult(source, result.bank, '
                                     'replace(frame, tile=replace_word(frame.tile, 65535)))'},
 '_upload_banked_tile_strip': {'signature': 'state, source, frame, count',
                               'returns': None,
                               'flow': 'bank = state.table(746650).cursor()\n'
                                       'for _ in descending_inclusive(count):\n'
                                       '    tile = replace_word(frame.palette, '
                                       'source.next_word())\n'
                                       '    if low16(tile) >= 2048:\n'
                                       '        bank = bank.advance(65536)\n'
                                       '    tile = replace_word(tile, u16(low16(tile) << 5))\n'
                                       '    for _ in descending_inclusive(7):\n'
                                       '        state.write(12582912, 4, '
                                       'bank.long(low16(tile)))\n'
                                       '        tile = replace_word(tile, u16(low16(tile) + '
                                       '4))\n'
                                       '    frame = replace(frame, palette=tile, '
                                       'tile=replace_word(frame.tile, 65535))\n'
                                       'return TileUploadResult(source, bank, replace(frame, '
                                       'attributes=replace_word(frame.attributes, 65535)))'},
 'upload_portrait_tiles': {'signature': 'state: SceneState, frame: SceneRenderFrame',
                           'returns': 'TileUploadResult',
                           'flow': 'checked_state(state)\n'
                                   'frame.validate(state)\n'
                                   'video = u32((frame.y & 65535) << 7)\n'
                                   'video = replace_word(video, low16(video) >> 2 | 16384)\n'
                                   'video = swap_words(video)\n'
                                   'state.write(12582916, 4, video)\n'
                                   'offset = u16(low16(frame.x) * 3 << 5)\n'
                                   'frame = replace(frame, y=replace_word(video, offset))\n'
                                   'source = state.table(713626).cursor(offset)\n'
                                   'result = upload_scene_tile_block(state, source, frame)\n'
                                   'frame = result.frame\n'
                                   'offset = u16(low16(frame.x) << 4)\n'
                                   'frame = replace(frame, y=replace_word(frame.y, offset), '
                                   'attributes=replace_word(frame.attributes, 7))\n'
                                   'source = state.table(738202).cursor(offset)\n'
                                   'result = _upload_banked_tile_strip(state, source, frame, '
                                   '7)\n'
                                   'frame = result.frame\n'
                                   'offset = u16(low16(frame.x) << 3)\n'
                                   'frame = replace(frame, y=replace_word(frame.y, offset), '
                                   'attributes=replace_word(frame.attributes, 3))\n'
                                   'source = state.table(742298).cursor(offset)\n'
                                   'result = _upload_banked_tile_strip(state, source, frame, '
                                   '3)\n'
                                   'frame = result.frame\n'
                                   'palette_offset = state.table(746394).byte(low16(frame.x)) '
                                   '<< 5\n'
                                   'bank = '
                                   'state.table(743834).cursor().advance(palette_offset)\n'
                                   "destination = _ram(state, 'fb00').cursor()\n"
                                   "if _ram(state, 'f6c4').word() == 2:\n"
                                   "    destination = _ram(state, 'fb20').cursor()\n"
                                   'for _ in descending_inclusive(7):\n'
                                   '    destination.append_long(bank.next_long())\n'
                                   "_ram(state, 'f31e').set_word(0, 1)\n"
                                   'frame = replace(frame, y=palette_offset, '
                                   'attributes=replace_word(frame.attributes, 65535))\n'
                                   'return TileUploadResult(source, bank, frame)'}}

def _lower_upload_object_officer_name(emitter,rules):
    emitter.segment(0x402c2,0x4031c)
    emitter.ins('mulu.w','#0x6,%d7',4)
    emitter.ins('lea.l','0x8a504:l,%a0',6)
    emitter.ins('lea.l','(%a0, %d7.w),%a0',4)
    emitter.ins('move.w','#0x2,%d3',4)
    emitter.ins('cmpi.w','#0x3f,0x4(%a0)',6)
    emitter.ins('bne.b','scene_pc_0402fc',2)
    emitter.ins('move.w','#0x1,%d3',4)
    emitter.ins('move.w','%d0,%d4',2)
    emitter.ins('asl.w','#0x4,%d4',2)
    emitter.ins('or.w','%d0,%d4',2)
    emitter.ins('move.w','#0x3f,%d5',4)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('lea.l','0xd440:w,%a2',4)
    emitter.ins('move.b','%d4,(%a1)+',2)
    emitter.ins('move.b','%d4,(%a2)+',2)
    emitter.ins('dbra','%d5,scene_pc_0402f2',4)
    emitter.ins('bra.b','scene_pc_040300',2)
    emitter.ins('lea.l','0xd300:w,%a1',4)
    emitter.ins('jsr','scene_pc_00ae8a:l',6)
    emitter.ins('lea.l','0xd300:w,%a0',4)
    emitter.ins('lea.l','0xc00000:l,%a6',6)
    emitter.ins('move.w','#0x5f,%d0',4)
    emitter.ins('move.l','(%a0)+,(%a6)',2)
    emitter.ins('dbra','%d0,scene_pc_040314',4)
    emitter.ins('rts','',2)

def _lower_start_object_left(emitter,rules):
    emitter.segment(0x40d0c,0x40d1c)
    emitter.ins('bra.w','scene_pc_040d7c',4)
    emitter.ins('bra.w','scene_pc_040df6',4)
    emitter.ins('bra.w','scene_pc_040e66',4)
    emitter.ins('bra.w','scene_pc_040ec0',4)
    emitter.segment(0x40d20,0x40d28)
    emitter.ins('bra.w','scene_pc_040f1a',4)
    emitter.ins('bra.w','scene_pc_041110',4)
    emitter.segment(0x40d4e,0x40d5e)
    emitter.ins('bra.w','scene_pc_040db6',4)
    emitter.ins('bra.w','scene_pc_040e32',4)
    emitter.ins('bra.w','scene_pc_040e8c',4)
    emitter.ins('bra.w','scene_pc_040ee6',4)
    emitter.segment(0x40d7c,0x40dd4)
    emitter.ins('cmpi.w','#0x0,0x2(%a6)',6)
    emitter.ins('bhi.w','scene_pc_040d9a',4)
    emitter.ins('bsr.w','scene_pc_040d28',4)
    emitter.ins('cmpi.w','#0x6,%d0',4)
    emitter.ins('bne.b','scene_pc_040d76',2)
    emitter.ins('move.w','#0x200,0x2(%a6)',6)
    emitter.ins('bra.w','scene_pc_040d76',4)
    emitter.ins('bsr.w','scene_pc_040dd4',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('bne.w','scene_pc_040d76',4)
    emitter.ins('move.w','0x2(%a6),%d0',4)
    emitter.ins('subi.w','#0x10,%d0',4)
    emitter.ins('move.w','%d0,0x8156:w',4)
    emitter.ins('move.w','#0x1,0x8(%a6)',6)
    emitter.ins('bsr.w','scene_pc_040dea',4)
    emitter.ins('sub.w','%d0,0x2(%a6)',4)
    emitter.ins('move.w','0x2(%a6),%d0',4)
    emitter.ins('cmp.w','0x8156:w,%d0',4)
    emitter.ins('bhi.w','scene_pc_040d7a',4)
    emitter.ins('andi.w','#0x1f8,0x2(%a6)',6)
    emitter.ins('bra.w','scene_pc_040d76',4)
    emitter.segment(0x40df6,0x40e50)
    emitter.ins('cmpi.w','#0x160,0x2(%a6)',6)
    emitter.ins('bcs.w','scene_pc_040e16',4)
    emitter.ins('bsr.w','scene_pc_040d28',4)
    emitter.ins('cmpi.w','#0x6,%d0',4)
    emitter.ins('bne.w','scene_pc_040d76',4)
    emitter.ins('move.w','#0x200,0x2(%a6)',6)
    emitter.ins('bra.w','scene_pc_040d76',4)
    emitter.ins('bsr.w','scene_pc_040e50',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('bne.w','scene_pc_040d76',4)
    emitter.ins('move.w','0x2(%a6),%d0',4)
    emitter.ins('addi.w','#0x10,%d0',4)
    emitter.ins('move.w','%d0,0x8156:w',4)
    emitter.ins('move.w','#0x0,0x8(%a6)',6)
    emitter.ins('bsr.w','scene_pc_040dea',4)
    emitter.ins('add.w','%d0,0x2(%a6)',4)
    emitter.ins('move.w','0x2(%a6),%d0',4)
    emitter.ins('cmp.w','0x8156:w,%d0',4)
    emitter.ins('bcs.w','scene_pc_040d7a',4)
    emitter.ins('andi.w','#0x1f8,0x2(%a6)',6)
    emitter.ins('bra.w','scene_pc_040d76',4)
    emitter.segment(0x40e66,0x40eaa)
    emitter.ins('bsr.w','scene_pc_040eaa',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('bne.w','scene_pc_040d76',4)
    emitter.ins('cmpi.w','#0x20,0x4(%a6)',6)
    emitter.ins('bls.w','scene_pc_040d76',4)
    emitter.ins('move.w','0x4(%a6),%d0',4)
    emitter.ins('subi.w','#0x10,%d0',4)
    emitter.ins('move.w','%d0,0x8156:w',4)
    emitter.ins('move.w','#0x3,0x8(%a6)',6)
    emitter.ins('bsr.w','scene_pc_040dea',4)
    emitter.ins('sub.w','%d0,0x4(%a6)',4)
    emitter.ins('move.w','0x4(%a6),%d0',4)
    emitter.ins('cmp.w','0x8156:w,%d0',4)
    emitter.ins('bne.w','scene_pc_040d7a',4)
    emitter.ins('andi.w','#0x1f8,0x4(%a6)',6)
    emitter.ins('bra.w','scene_pc_040d76',4)
    emitter.segment(0x40ec0,0x40f04)
    emitter.ins('bsr.w','scene_pc_040f04',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('bne.w','scene_pc_040d76',4)
    emitter.ins('cmpi.w','#0x120,0x4(%a6)',6)
    emitter.ins('bcc.w','scene_pc_040d76',4)
    emitter.ins('move.w','0x4(%a6),%d0',4)
    emitter.ins('addi.w','#0x10,%d0',4)
    emitter.ins('move.w','%d0,0x8156:w',4)
    emitter.ins('move.w','#0x2,0x8(%a6)',6)
    emitter.ins('bsr.w','scene_pc_040dea',4)
    emitter.ins('add.w','%d0,0x4(%a6)',4)
    emitter.ins('move.w','0x4(%a6),%d0',4)
    emitter.ins('cmp.w','0x8156:w,%d0',4)
    emitter.ins('bne.w','scene_pc_040d7a',4)
    emitter.ins('andi.w','#0x1f8,0x4(%a6)',6)
    emitter.ins('bra.w','scene_pc_040d76',4)
    emitter.segment(0x40f1a,0x40f7e)
    emitter.ins('cmpa.l','#0xffff826a,%a6',6)
    emitter.ins('bcs.b','scene_pc_040f50',2)
    emitter.ins('lea.l','0x816a:w,%a5',4)
    emitter.ins('cmpi.b','#0x3,0x80db:w',6)
    emitter.ins('beq.w','scene_pc_040f98',4)
    emitter.ins('tst.b','0x1(%a6)',4)
    emitter.ins('beq.w','scene_pc_040f98',4)
    emitter.ins('cmpi.b','#0x1,0x1(%a6)',6)
    emitter.ins('beq.w','scene_pc_0410dc',4)
    emitter.ins('cmpi.b','#0x2,0x1(%a6)',6)
    emitter.ins('beq.w','scene_pc_0410f6',4)
    emitter.ins('bra.w','scene_pc_0410f6',4)
    emitter.ins('lea.l','0x826a:w,%a5',4)
    emitter.ins('cmpi.b','#0x3,0x80db:w',6)
    emitter.ins('beq.w','scene_pc_040f98',4)
    emitter.ins('tst.b','0x1(%a6)',4)
    emitter.ins('beq.w','scene_pc_040f98',4)
    emitter.ins('cmpi.b','#0x1,0x1(%a6)',6)
    emitter.ins('beq.w','scene_pc_0410dc',4)
    emitter.ins('cmpi.b','#0x2,0x1(%a6)',6)
    emitter.ins('beq.w','scene_pc_0410f6',4)
    emitter.ins('bra.w','scene_pc_0410f6',4)
    emitter.segment(0x40f88,0x4115c)
    emitter.ins('bra.w','scene_pc_040db6',4)
    emitter.ins('bra.w','scene_pc_040e32',4)
    emitter.ins('bra.w','scene_pc_040e8c',4)
    emitter.ins('bra.w','scene_pc_040ee6',4)
    emitter.ins('move.w','0x2(%a6),%d0',4)
    emitter.ins('sub.w','0x2(%a5),%d0',4)
    emitter.ins('bpl.w','scene_pc_040fa6',4)
    emitter.ins('neg.w','%d0',2)
    emitter.ins('move.w','0x4(%a6),%d1',4)
    emitter.ins('sub.w','0x4(%a5),%d1',4)
    emitter.ins('bpl.w','scene_pc_040fb4',4)
    emitter.ins('neg.w','%d1',2)
    emitter.ins('cmp.w','%d0,%d1',2)
    emitter.ins('bcs.w','scene_pc_04104a',4)
    emitter.ins('move.w','#0x3,0xa(%a6)',6)
    emitter.ins('move.w','0x4(%a6),%d0',4)
    emitter.ins('cmp.w','0x4(%a5),%d0',4)
    emitter.ins('bcs.w','scene_pc_041038',4)
    emitter.ins('move.w','#0x2,0xa(%a6)',6)
    emitter.ins('bsr.w','scene_pc_040eaa',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('beq.w','scene_pc_040e66',4)
    emitter.ins('move.w','#0x0,0xa(%a6)',6)
    emitter.ins('move.w','0x2(%a6),%d0',4)
    emitter.ins('cmp.w','0x2(%a5),%d0',4)
    emitter.ins('bhi.w','scene_pc_040d7c',4)
    emitter.ins('move.w','#0x1,0xa(%a6)',6)
    emitter.ins('bcs.w','scene_pc_040df6',4)
    emitter.ins('jsr','-22744(%pc)',4)
    emitter.ins('btst.l','#0x1,%d0',4)
    emitter.ins('bne.w','scene_pc_041008',4)
    emitter.ins('bra.w','scene_pc_041020',4)
    emitter.ins('cmpi.w','#0x0,0x2(%a6)',6)
    emitter.ins('bls.w','scene_pc_040df6',4)
    emitter.ins('bsr.w','scene_pc_040dd4',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('beq.w','scene_pc_040d7c',4)
    emitter.ins('bra.w','scene_pc_040df6',4)
    emitter.ins('cmpi.w','#0x160,0x2(%a6)',6)
    emitter.ins('bcc.w','scene_pc_040d7c',4)
    emitter.ins('bsr.w','scene_pc_040e50',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('beq.w','scene_pc_040df6',4)
    emitter.ins('bra.w','scene_pc_040d7c',4)
    emitter.ins('move.w','#0x3,0xa(%a6)',6)
    emitter.ins('bsr.w','scene_pc_040f04',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('beq.w','scene_pc_040ec0',4)
    emitter.ins('bra.b','scene_pc_040fdc',2)
    emitter.ins('move.w','#0x1,0xa(%a6)',6)
    emitter.ins('move.w','0x2(%a6),%d0',4)
    emitter.ins('cmp.w','0x2(%a5),%d0',4)
    emitter.ins('bcs.w','scene_pc_0410c8',4)
    emitter.ins('move.w','#0x0,0xa(%a6)',6)
    emitter.ins('bsr.w','scene_pc_040dd4',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('beq.w','scene_pc_040d7c',4)
    emitter.ins('move.w','#0x3,0xa(%a6)',6)
    emitter.ins('move.w','0x4(%a6),%d0',4)
    emitter.ins('cmp.w','0x4(%a5),%d0',4)
    emitter.ins('bcs.w','scene_pc_040ec0',4)
    emitter.ins('move.w','#0x2,0xa(%a6)',6)
    emitter.ins('bhi.w','scene_pc_040e66',4)
    emitter.ins('jsr','-22888(%pc)',4)
    emitter.ins('btst.l','#0x1,%d0',4)
    emitter.ins('bne.w','scene_pc_041098',4)
    emitter.ins('bra.w','scene_pc_0410b0',4)
    emitter.ins('cmpi.w','#0x120,0x4(%a6)',6)
    emitter.ins('bcc.w','scene_pc_040e66',4)
    emitter.ins('bsr.w','scene_pc_040f04',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('beq.w','scene_pc_040ec0',4)
    emitter.ins('bra.w','scene_pc_040e66',4)
    emitter.ins('cmpi.w','#0x20,0x4(%a6)',6)
    emitter.ins('bls.w','scene_pc_040ec0',4)
    emitter.ins('bsr.w','scene_pc_040eaa',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('beq.w','scene_pc_040e66',4)
    emitter.ins('bra.w','scene_pc_040ec0',4)
    emitter.ins('move.w','#0x1,0xa(%a6)',6)
    emitter.ins('bsr.w','scene_pc_040e50',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('beq.w','scene_pc_040df6',4)
    emitter.ins('bra.w','scene_pc_04106c',4)
    emitter.ins('move.w','0x4(%a6),%d0',4)
    emitter.ins('sub.w','0x4(%a5),%d0',4)
    emitter.ins('bpl.w','scene_pc_0410ea',4)
    emitter.ins('neg.w','%d0',2)
    emitter.ins('cmpi.w','#0x10,%d0',4)
    emitter.ins('bhi.w','scene_pc_040fba',4)
    emitter.ins('bra.w','scene_pc_04104a',4)
    emitter.ins('move.w','0x2(%a6),%d0',4)
    emitter.ins('sub.w','0x2(%a5),%d0',4)
    emitter.ins('bpl.w','scene_pc_041104',4)
    emitter.ins('neg.w','%d0',2)
    emitter.ins('cmpi.w','#0x10,%d0',4)
    emitter.ins('bhi.w','scene_pc_04104a',4)
    emitter.ins('bra.w','scene_pc_040fba',4)
    emitter.ins('cmpa.l','#0xffff826a,%a6',6)
    emitter.ins('bcs.b','scene_pc_04112c',2)
    emitter.ins('move.w','#0x1,0xa(%a6)',6)
    emitter.ins('bsr.w','scene_pc_040e50',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('beq.w','scene_pc_040df6',4)
    emitter.ins('bra.w','scene_pc_04113c',4)
    emitter.ins('move.w','#0x0,0xa(%a6)',6)
    emitter.ins('bsr.w','scene_pc_040dd4',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('beq.w','scene_pc_040d7c',4)
    emitter.ins('move.w','#0x3,0xa(%a6)',6)
    emitter.ins('jsr','-23074(%pc)',4)
    emitter.ins('cmp.w','0x4(%a5),%d0',4)
    emitter.ins('btst.l','#0x4,%d0',4)
    emitter.ins('bne.w','scene_pc_040ec0',4)
    emitter.ins('move.w','#0x2,0xa(%a6)',6)
    emitter.ins('bra.w','scene_pc_040e66',4)

def _lower_resume_object_selected_action(emitter,rules):
    emitter.segment(0x40d1c,0x40d20)
    emitter.ins('bra.w','scene_pc_040cac',4)

def _lower_finish_object_action_noop(emitter,rules):
    emitter.segment(0x40d5e,0x40d62)
    emitter.ins('bra.w','scene_pc_040d76',4)

def _lower_resume_object_pursuit(emitter,rules):
    emitter.segment(0x40d62,0x40d6e)
    emitter.ins('bra.w','scene_pc_040f7e',4)
    emitter.ins('bra.w','scene_pc_040f7e',4)
    emitter.ins('bra.w','scene_pc_040f7e',4)
    emitter.segment(0x40f7e,0x40f88)
    emitter.ins('move.w','0xa(%a6),%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('jmp','2(%pc, %d0.w)',4)

def _lower_advance_object_impact(emitter,rules):
    emitter.segment(0x40d6e,0x40d76)
    emitter.ins('bra.w','scene_pc_041524',4)
    emitter.ins('bra.w','scene_pc_0416f8',4)
    emitter.segment(0x41524,0x415e2)
    emitter.ins('addq.w','#0x1,0x8162:w',4)
    emitter.ins('move.w','0x8162:w,%d0',4)
    emitter.ins('moveq','#16,%d1',2)
    emitter.ins('tst.w','0x840a:w',4)
    emitter.ins('beq.b','scene_pc_041536',2)
    emitter.ins('moveq','#16,%d1',2)
    emitter.ins('cmp.w','%d1,%d0',2)
    emitter.ins('bcs.w','scene_pc_0415a2',4)
    emitter.ins('movea.l','0x815c:w,%a5',4)
    emitter.ins('bsr.w','scene_pc_04162e',4)
    emitter.ins('sub.w','%d1,0xe(%a5)',4)
    emitter.ins('beq.b','scene_pc_04154c',2)
    emitter.ins('bpl.b','scene_pc_04159e',2)
    emitter.ins('clr.w','0xe(%a5)',4)
    emitter.ins('clr.w','(%a5)',2)
    emitter.ins('cmpa.l','#0xffff826a,%a5',6)
    emitter.ins('bcs.b','scene_pc_04156e',2)
    emitter.ins('tst.w','0x826a:w',4)
    emitter.ins('bne.b','scene_pc_04159e',2)
    emitter.ins('move.w','#0x2,0x8114:w',6)
    emitter.ins('move.w','#0x3,0x8116:w',6)
    emitter.ins('bra.b','scene_pc_04157e',2)
    emitter.ins('tst.w','0x816a:w',4)
    emitter.ins('bne.b','scene_pc_04159e',2)
    emitter.ins('move.w','#0x3,0x8114:w',6)
    emitter.ins('clr.w','0x8116:w',4)
    emitter.ins('move.w','#0x4,0x813a:w',6)
    emitter.ins('move.w','#0x0,0x813c:w',6)
    emitter.ins('move.w','#0x1,0x813e:w',6)
    emitter.ins('move.w','0x814c:w,%d0',4)
    emitter.ins('subq.w','#0x1,%d0',2)
    emitter.ins('eori.w','#0x1,%d0',4)
    emitter.ins('move.w','%d0,0x8176:w',4)
    emitter.ins('bra.w','scene_pc_040d76',4)
    emitter.ins('move.l','0x2(%a6),%d0',4)
    emitter.ins('movem.l','%d0,-(%a7)',4)
    emitter.ins('move.w','0x8158:w,%d2',4)
    emitter.ins('asl.w','#0x2,%d2',2)
    emitter.ins('move.w','54(%pc, %d2.w),%d0',4)
    emitter.ins('move.w','52(%pc, %d2.w),%d1',4)
    emitter.ins('bsr.w','scene_pc_0411a2',4)
    emitter.ins('move.w','0x2(%a6),%d0',4)
    emitter.ins('move.w','0x4(%a6),%d1',4)
    emitter.ins('move.w','#0x4,%d2',4)
    emitter.ins('moveq','#0,%d3',2)
    emitter.ins('move.w','#0x100,%d4',4)
    emitter.ins('lea.l','18(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','-25754(%pc)',4)
    emitter.ins('movem.l','(%a7)+,%d0',4)
    emitter.ins('move.l','%d0,0x2(%a6)',4)
    emitter.ins('rts','',2)
    emitter.segment(0x41608,0x4162e)
    emitter.ins('move.l','0x2(%a6),%d0',4)
    emitter.ins('movem.l','%d0,-(%a7)',4)
    emitter.ins('move.w','0x8158:w,%d2',4)
    emitter.ins('asl.w','#0x2,%d2',2)
    emitter.ins('move.w','-48(%pc, %d2.w),%d0',4)
    emitter.ins('move.w','-50(%pc, %d2.w),%d1',4)
    emitter.ins('bsr.w','scene_pc_0411a2',4)
    emitter.ins('move.w','0x8164:w,%d0',4)
    emitter.ins('move.w','0x8166:w,%d1',4)
    emitter.ins('bra.w','scene_pc_0415c4',4)
    emitter.segment(0x416f8,0x417ce)
    emitter.ins('movea.l','0x815c:w,%a5',4)
    emitter.ins('move.w','0x8164:w,%d0',4)
    emitter.ins('cmp.w','0x2(%a5),%d0',4)
    emitter.ins('bne.b','scene_pc_041768',2)
    emitter.ins('move.w','0x8166:w,%d0',4)
    emitter.ins('cmp.w','0x4(%a5),%d0',4)
    emitter.ins('bne.b','scene_pc_041768',2)
    emitter.ins('tst.w','0x8168:w',4)
    emitter.ins('bne.b','scene_pc_041720',2)
    emitter.ins('move.w','#0xaa,%d0',4)
    emitter.ins('jsr','scene_pc_00808a:l',6)
    emitter.ins('addq.w','#0x1,0x8168:w',4)
    emitter.ins('move.w','0x8168:w,%d0',4)
    emitter.ins('moveq','#16,%d1',2)
    emitter.ins('tst.w','0x840a:w',4)
    emitter.ins('beq.b','scene_pc_041732',2)
    emitter.ins('moveq','#16,%d1',2)
    emitter.ins('cmp.w','%d1,%d0',2)
    emitter.ins('bcs.w','scene_pc_041608',4)
    emitter.ins('move.w','0xe(%a6),%d0',4)
    emitter.ins('move.w','0xc(%a6),%d1',4)
    emitter.ins('mulu.w','%d0,%d1',2)
    emitter.ins('divu.w','#0x64,%d1',4)
    emitter.ins('movem.l','%d1,-(%a7)',4)
    emitter.ins('jsr','-24618(%pc)',4)
    emitter.ins('andi.w','#0x1f,%d0',4)
    emitter.ins('addi.w','#0x50,%d0',4)
    emitter.ins('movem.l','(%a7)+,%d1',4)
    emitter.ins('mulu.w','%d0,%d1',2)
    emitter.ins('divu.w','#0x64,%d1',4)
    emitter.ins('bsr.w','scene_pc_0416ce',4)
    emitter.ins('bra.w','scene_pc_04153c',4)
    emitter.ins('moveq','#4,%d0',2)
    emitter.ins('tst.w','0x840a:w',4)
    emitter.ins('beq.b','scene_pc_041772',2)
    emitter.ins('moveq','#8,%d0',2)
    emitter.ins('tst.w','0x8(%a6)',4)
    emitter.ins('bne.w','scene_pc_041780',4)
    emitter.ins('add.w','%d0,0x8164:w',4)
    emitter.ins('bra.b','scene_pc_0417ae',2)
    emitter.ins('cmpi.w','#0x1,0x8(%a6)',6)
    emitter.ins('bne.w','scene_pc_041790',4)
    emitter.ins('sub.w','%d0,0x8164:w',4)
    emitter.ins('bra.b','scene_pc_0417ae',2)
    emitter.ins('cmpi.w','#0x2,0x8(%a6)',6)
    emitter.ins('bne.w','scene_pc_0417a0',4)
    emitter.ins('add.w','%d0,0x8166:w',4)
    emitter.ins('bra.b','scene_pc_0417ae',2)
    emitter.ins('cmpi.w','#0x3,0x8(%a6)',6)
    emitter.ins('bne.w','scene_pc_0417ae',4)
    emitter.ins('sub.w','%d0,0x8166:w',4)
    emitter.ins('move.w','0x8(%a6),%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('movea.l','24(%pc, %d0.w),%a0',4)
    emitter.ins('move.w','0x8164:w,%d0',4)
    emitter.ins('move.w','0x8166:w,%d1',4)
    emitter.ins('move.w','#0x4,%d2',4)
    emitter.ins('moveq','#0,%d3',2)
    emitter.ins('move.w','#0x300,%d4',4)
    emitter.ins('jmp','-26256(%pc)',4)

def _lower_probe_object_left(emitter,rules):
    emitter.segment(0x40dd4,0x40dea)
    emitter.ins('movem.l','%a5,-(%a7)',4)
    emitter.ins('move.w','#0x8010,%d0',4)
    emitter.ins('move.w','#0x0,%d1',4)
    emitter.ins('bsr.w','scene_pc_04115c',4)
    emitter.ins('movem.l','(%a7)+,%a5',4)
    emitter.ins('rts','',2)

def _lower_object_movement_speed(emitter,rules):
    emitter.segment(0x40dea,0x40df6)
    emitter.ins('moveq','#2,%d0',2)
    emitter.ins('tst.w','0x840a:w',4)
    emitter.ins('beq.b','scene_pc_040df4',2)
    emitter.ins('moveq','#4,%d0',2)
    emitter.ins('rts','',2)

def _lower_probe_object_right(emitter,rules):
    emitter.segment(0x40e50,0x40e66)
    emitter.ins('movem.l','%a5,-(%a7)',4)
    emitter.ins('move.w','#0x10,%d0',4)
    emitter.ins('move.w','#0x0,%d1',4)
    emitter.ins('bsr.w','scene_pc_04115c',4)
    emitter.ins('movem.l','(%a7)+,%a5',4)
    emitter.ins('rts','',2)

def _lower_probe_object_up(emitter,rules):
    emitter.segment(0x40eaa,0x40ec0)
    emitter.ins('movem.l','%a5,-(%a7)',4)
    emitter.ins('move.w','#0x0,%d0',4)
    emitter.ins('move.w','#0x8010,%d1',4)
    emitter.ins('bsr.w','scene_pc_04115c',4)
    emitter.ins('movem.l','(%a7)+,%a5',4)
    emitter.ins('rts','',2)

def _lower_probe_object_down(emitter,rules):
    emitter.segment(0x40f04,0x40f1a)
    emitter.ins('movem.l','%a5,-(%a7)',4)
    emitter.ins('move.w','#0x0,%d0',4)
    emitter.ins('move.w','#0x10,%d1',4)
    emitter.ins('bsr.w','scene_pc_04115c',4)
    emitter.ins('movem.l','(%a7)+,%a5',4)
    emitter.ins('rts','',2)

def _lower_calculate_object_impact_damage(emitter,rules):
    emitter.segment(0x4162e,0x416f8)
    emitter.ins('cmpi.b','#0x0,0x1(%a6)',6)
    emitter.ins('beq.b','scene_pc_0416a6',2)
    emitter.ins('cmpi.b','#0x1,0x1(%a6)',6)
    emitter.ins('beq.b','scene_pc_04167a',2)
    emitter.ins('cmpi.b','#0x2,0x1(%a6)',6)
    emitter.ins('beq.b','scene_pc_04164e',2)
    emitter.ins('move.w','0xc(%a6),%d1',4)
    emitter.ins('bra.w','scene_pc_0416ce',4)
    emitter.ins('move.w','0xe(%a6),%d0',4)
    emitter.ins('move.w','0xc(%a6),%d1',4)
    emitter.ins('mulu.w','%d0,%d1',2)
    emitter.ins('divu.w','#0x64,%d1',4)
    emitter.ins('movem.l','%d1,-(%a7)',4)
    emitter.ins('jsr','-24384(%pc)',4)
    emitter.ins('andi.w','#0x1f,%d0',4)
    emitter.ins('addi.w','#0x78,%d0',4)
    emitter.ins('movem.l','(%a7)+,%d1',4)
    emitter.ins('mulu.w','%d0,%d1',2)
    emitter.ins('divu.w','#0x64,%d1',4)
    emitter.ins('bra.w','scene_pc_0416ce',4)
    emitter.ins('move.w','0xe(%a6),%d0',4)
    emitter.ins('move.w','0xc(%a6),%d1',4)
    emitter.ins('mulu.w','%d0,%d1',2)
    emitter.ins('divu.w','#0x64,%d1',4)
    emitter.ins('movem.l','%d1,-(%a7)',4)
    emitter.ins('jsr','-24428(%pc)',4)
    emitter.ins('andi.w','#0x1f,%d0',4)
    emitter.ins('addi.w','#0x50,%d0',4)
    emitter.ins('movem.l','(%a7)+,%d1',4)
    emitter.ins('mulu.w','%d0,%d1',2)
    emitter.ins('divu.w','#0x64,%d1',4)
    emitter.ins('bra.w','scene_pc_0416ce',4)
    emitter.ins('move.w','0xe(%a6),%d0',4)
    emitter.ins('move.w','0xc(%a6),%d1',4)
    emitter.ins('mulu.w','%d0,%d1',2)
    emitter.ins('divu.w','#0x64,%d1',4)
    emitter.ins('movem.l','%d1,-(%a7)',4)
    emitter.ins('jsr','-24472(%pc)',4)
    emitter.ins('andi.w','#0x1f,%d0',4)
    emitter.ins('addi.w','#0x3c,%d0',4)
    emitter.ins('movem.l','(%a7)+,%d1',4)
    emitter.ins('mulu.w','%d0,%d1',2)
    emitter.ins('divu.w','#0x64,%d1',4)
    emitter.ins('cmpi.b','#0x3,0x1(%a5)',6)
    emitter.ins('bne.b','scene_pc_0416f6',2)
    emitter.ins('move.w','0x8104:w,%d2',4)
    emitter.ins('cmpi.w','#0x2,0x814c:w',6)
    emitter.ins('beq.b','scene_pc_0416e6',2)
    emitter.ins('move.w','0x8106:w,%d2',4)
    emitter.ins('lsr.w','#0x1,%d2',2)
    emitter.ins('bne.b','scene_pc_0416ee',2)
    emitter.ins('move.w','#0x1,%d2',4)
    emitter.ins('andi.l','#0xffff,%d1',6)
    emitter.ins('divu.w','%d2,%d1',2)
    emitter.ins('rts','',2)

def _lower_update_object_action_ai(emitter,rules):
    emitter.segment(0x41bac,0x41be4)
    emitter.ins('cmpi.b','#0x1,0x80da:w',6)
    emitter.ins('beq.b','scene_pc_041be2',2)
    emitter.ins('cmpi.b','#0x2,0x80da:w',6)
    emitter.ins('beq.b','scene_pc_041be2',2)
    emitter.ins('tst.b','0x814c:w',4)
    emitter.ins('bne.b','scene_pc_041be2',2)
    emitter.ins('cmpi.w','#0x6,0x812a:w',6)
    emitter.ins('beq.b','scene_pc_041be2',2)
    emitter.ins('jsr','24(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','260(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','882(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','482(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('rts','',2)

def _lower_dispatch_object_formation_ai(emitter,rules):
    emitter.segment(0x41be4,0x41bee)
    emitter.ins('move.w','0x814a:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('jmp','2(%pc, %d0.w)',4)

def _lower_dispatch_object_formation_fallback(emitter,rules):
    emitter.segment(0x41cd6,0x41cea)
    emitter.ins('cmpi.w','#0x6,0x8130:w',6)
    emitter.ins('beq.w','scene_pc_041d3c',4)
    emitter.ins('move.w','0x814a:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('jmp','2(%pc, %d0.w)',4)
    emitter.segment(0x41d3c,0x41d3e)
    emitter.ins('rts','',2)

def _lower_advance_object_retreat_checks(emitter,rules):
    emitter.segment(0x41d7a,0x41d7c)
    emitter.ins('rts','',2)
    emitter.segment(0x41dc0,0x41dde)
    emitter.ins('cmpi.w','#0xb,0x8160:w',6)
    emitter.ins('bcs.b','scene_pc_041d7a',2)
    emitter.ins('bsr.w','scene_pc_041dde',4)
    emitter.ins('bsr.w','scene_pc_041e1e',4)
    emitter.ins('bsr.w','scene_pc_041e4c',4)
    emitter.ins('bsr.w','scene_pc_041e76',4)
    emitter.ins('bsr.w','scene_pc_041eb6',4)
    emitter.ins('rts','',2)

def _lower_trigger_object_retreat_strength(emitter,rules):
    emitter.segment(0x41dde,0x41ef4)
    emitter.ins('bsr.w','scene_pc_041f08',4)
    emitter.ins('move.w','%d1,%d3',2)
    emitter.ins('asl.w','#0x1,%d3',2)
    emitter.ins('cmp.w','%d3,%d2',2)
    emitter.ins('bls.b','scene_pc_041e1c',2)
    emitter.ins('cmpi.w','#0x3e8,%d1',4)
    emitter.ins('bhi.b','scene_pc_041e1c',2)
    emitter.ins('jsr','-26320(%pc)',4)
    emitter.ins('move.w','0xefd2:w,%d1',4)
    emitter.ins('lea.l','250(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('and.b','(%a0, %d1.w),%d0',4)
    emitter.ins('bne.b','scene_pc_041e1c',2)
    emitter.ins('move.w','#0x6,0x812a:w',6)
    emitter.ins('move.w','#0x6,0x812c:w',6)
    emitter.ins('move.w','#0x6,0x812e:w',6)
    emitter.ins('move.w','#0x6,0x8130:w',6)
    emitter.ins('rts','',2)
    emitter.ins('bsr.w','scene_pc_041f08',4)
    emitter.ins('move.w','%d1,%d3',2)
    emitter.ins('asl.w','#0x1,%d3',2)
    emitter.ins('cmp.w','%d3,%d2',2)
    emitter.ins('bls.w','scene_pc_041e1c',4)
    emitter.ins('cmpi.w','#0x1f4,%d1',4)
    emitter.ins('bhi.w','scene_pc_041e1c',4)
    emitter.ins('jsr','-26388(%pc)',4)
    emitter.ins('move.w','0xefd2:w,%d1',4)
    emitter.ins('lea.l','186(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('and.b','(%a0, %d1.w),%d0',4)
    emitter.ins('beq.w','scene_pc_041e04',4)
    emitter.ins('rts','',2)
    emitter.ins('bsr.w','scene_pc_041f08',4)
    emitter.ins('asl.w','#0x1,%d3',2)
    emitter.ins('cmp.w','%d3,%d4',2)
    emitter.ins('bls.w','scene_pc_041e1c',4)
    emitter.ins('cmp.w','%d1,%d2',2)
    emitter.ins('bls.w','scene_pc_041e1c',4)
    emitter.ins('jsr','-26430(%pc)',4)
    emitter.ins('move.w','0xefd2:w,%d1',4)
    emitter.ins('lea.l','148(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('and.b','(%a0, %d1.w),%d0',4)
    emitter.ins('beq.w','scene_pc_041e04',4)
    emitter.ins('rts','',2)
    emitter.ins('bsr.w','scene_pc_041f08',4)
    emitter.ins('cmp.w','%d1,%d2',2)
    emitter.ins('bls.w','scene_pc_041e1c',4)
    emitter.ins('cmpi.w','#0x1e,0x8178:w',6)
    emitter.ins('bcc.w','scene_pc_041e1c',4)
    emitter.ins('jsr','-26474(%pc)',4)
    emitter.ins('move.w','0xefd2:w,%d1',4)
    emitter.ins('cmpi.w','#0x2,%d1',4)
    emitter.ins('bne.b','scene_pc_041ea6',2)
    emitter.ins('andi.w','#0x7,%d0',4)
    emitter.ins('cmpi.w','#0x5,%d0',4)
    emitter.ins('bcs.w','scene_pc_041e04',4)
    emitter.ins('rts','',2)
    emitter.ins('lea.l','88(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('and.b','(%a0, %d1.w),%d0',4)
    emitter.ins('beq.w','scene_pc_041e04',4)
    emitter.ins('rts','',2)
    emitter.ins('bsr.w','scene_pc_041f08',4)
    emitter.ins('move.w','0x8104:w,%d0',4)
    emitter.ins('cmp.w','0x8106:w,%d0',4)
    emitter.ins('bcc.w','scene_pc_041e1c',4)
    emitter.ins('move.w','0x8178:w,%d0',4)
    emitter.ins('cmp.w','0x8278:w,%d0',4)
    emitter.ins('bcc.w','scene_pc_041e1c',4)
    emitter.ins('cmpi.w','#0x1e,0x8178:w',6)
    emitter.ins('bcc.w','scene_pc_041e1c',4)
    emitter.ins('jsr','-26556(%pc)',4)
    emitter.ins('move.w','0xefd2:w,%d1',4)
    emitter.ins('lea.l','30(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('and.b','(%a0, %d1.w),%d0',4)
    emitter.ins('beq.w','scene_pc_041e04',4)
    emitter.ins('rts','',2)

def _lower_sum_live_object_rosters(emitter,rules):
    emitter.segment(0x41f08,0x41f4a)
    emitter.ins('moveq','#0,%d1',2)
    emitter.ins('moveq','#0,%d3',2)
    emitter.ins('move.w','#0xe,%d0',4)
    emitter.ins('lea.l','0x817a:w,%a6',4)
    emitter.ins('btst.b','#0x7,(%a6)',4)
    emitter.ins('beq.b','scene_pc_041f20',2)
    emitter.ins('add.w','0xe(%a6),%d1',4)
    emitter.ins('addq.w','#0x1,%d3',2)
    emitter.ins('adda.w','#0x10,%a6',4)
    emitter.ins('dbra','%d0,scene_pc_041f14',4)
    emitter.ins('moveq','#0,%d2',2)
    emitter.ins('moveq','#0,%d4',2)
    emitter.ins('move.w','#0xe,%d0',4)
    emitter.ins('lea.l','0x827a:w,%a6',4)
    emitter.ins('btst.b','#0x7,(%a6)',4)
    emitter.ins('beq.b','scene_pc_041f40',2)
    emitter.ins('add.w','0xe(%a6),%d2',4)
    emitter.ins('addq.w','#0x1,%d4',2)
    emitter.ins('adda.w','#0x10,%a6',4)
    emitter.ins('dbra','%d0,scene_pc_041f34',4)
    emitter.ins('rts','',2)

def _lower_choose_object_retreat_phase(emitter,rules):
    emitter.segment(0x41f4a,0x41fec)
    emitter.ins('move.w','0x80dc:w,%d0',4)
    emitter.ins('cmp.w','0x80e0:w,%d0',4)
    emitter.ins('beq.w','scene_pc_041fea',4)
    emitter.ins('bsr.w','scene_pc_041f08',4)
    emitter.ins('cmp.w','%d1,%d2',2)
    emitter.ins('bls.w','scene_pc_041fea',4)
    emitter.ins('move.w','0xefd2:w,%d0',4)
    emitter.ins('lea.l','134(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','0x8178:w,%d1',4)
    emitter.ins('cmp.b','(%a0, %d0.w),%d1',4)
    emitter.ins('bcc.w','scene_pc_041fea',4)
    emitter.ins('move.w','0x8178:w,%d0',4)
    emitter.ins('cmp.w','0x8278:w,%d0',4)
    emitter.ins('bcc.w','scene_pc_041fea',4)
    emitter.ins('lea.l','0x816a:w,%a6',4)
    emitter.ins('move.w','#0x8010,%d0',4)
    emitter.ins('move.w','#0x0,%d1',4)
    emitter.ins('bsr.w','scene_pc_0414fa',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('bne.w','scene_pc_041fce',4)
    emitter.ins('move.w','#0x10,%d0',4)
    emitter.ins('move.w','#0x0,%d1',4)
    emitter.ins('bsr.w','scene_pc_0414fa',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('bne.w','scene_pc_041fce',4)
    emitter.ins('move.w','#0x8010,%d0',4)
    emitter.ins('move.w','#0x8010,%d1',4)
    emitter.ins('bsr.w','scene_pc_0414fa',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('bne.w','scene_pc_041fce',4)
    emitter.ins('move.w','#0x10,%d0',4)
    emitter.ins('move.w','#0x8010,%d1',4)
    emitter.ins('bsr.w','scene_pc_0414fa',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('beq.w','scene_pc_041fea',4)
    emitter.ins('jsr','-26798(%pc)',4)
    emitter.ins('andi.w','#0x3,%d0',4)
    emitter.ins('beq.b','scene_pc_041fea',2)
    emitter.ins('move.w','#0x6,0x813a:w',6)
    emitter.ins('move.w','#0x0,0x813c:w',6)
    emitter.ins('move.w','#0x1,0x813e:w',6)
    emitter.ins('rts','',2)

def _lower_upload_portrait_tiles(emitter,rules):
    emitter.segment(0x661d4,0x662b4)
    emitter.ins('andi.l','#0xffff,%d1',6)
    emitter.ins('lsl.l','#0x7,%d1',2)
    emitter.ins('lsr.w','#0x2,%d1',2)
    emitter.ins('ori.w','#0x4000,%d1',4)
    emitter.ins('swap','%d1',2)
    emitter.ins('move.l','%d1,0xc00004:l',6)
    emitter.ins('move.w','%d0,%d1',2)
    emitter.ins('lsl.w','#0x1,%d1',2)
    emitter.ins('add.w','%d0,%d1',2)
    emitter.ins('lsl.w','#0x5,%d1',2)
    emitter.ins('lea.l','0xae39a:l,%a0',6)
    emitter.ins('adda.w','%d1,%a0',2)
    emitter.ins('bsr.w','scene_pc_0662b4',4)
    emitter.ins('move.w','%d0,%d1',2)
    emitter.ins('lsl.w','#0x4,%d1',2)
    emitter.ins('lea.l','0xb439a:l,%a0',6)
    emitter.ins('adda.w','%d1,%a0',2)
    emitter.ins('move.w','#0x7,%d2',4)
    emitter.ins('lea.l','0xb649a:l,%a1',6)
    emitter.ins('move.w','(%a0)+,%d3',2)
    emitter.ins('cmpi.w','#0x800,%d3',4)
    emitter.ins('bcs.w','scene_pc_066224',4)
    emitter.ins('adda.l','#0x10000,%a1',6)
    emitter.ins('lsl.w','#0x5,%d3',2)
    emitter.ins('move.w','#0x7,%d4',4)
    emitter.ins('move.l','(%a1, %d3.w),0xc00000:l',8)
    emitter.ins('addq.w','#0x4,%d3',2)
    emitter.ins('dbra','%d4,scene_pc_06622a',4)
    emitter.ins('dbra','%d2,scene_pc_06620e',4)
    emitter.ins('move.w','%d0,%d1',2)
    emitter.ins('lsl.w','#0x3,%d1',2)
    emitter.ins('lea.l','0xb539a:l,%a0',6)
    emitter.ins('adda.w','%d1,%a0',2)
    emitter.ins('move.w','#0x3,%d2',4)
    emitter.ins('lea.l','0xb649a:l,%a1',6)
    emitter.ins('move.w','(%a0)+,%d3',2)
    emitter.ins('cmpi.w','#0x800,%d3',4)
    emitter.ins('bcs.w','scene_pc_066262',4)
    emitter.ins('adda.l','#0x10000,%a1',6)
    emitter.ins('lsl.w','#0x5,%d3',2)
    emitter.ins('move.w','#0x7,%d4',4)
    emitter.ins('move.l','(%a1, %d3.w),0xc00000:l',8)
    emitter.ins('addq.w','#0x4,%d3',2)
    emitter.ins('dbra','%d4,scene_pc_066268',4)
    emitter.ins('dbra','%d2,scene_pc_06624c',4)
    emitter.ins('lea.l','0xb599a:l,%a1',6)
    emitter.ins('lea.l','0xb639a:l,%a2',6)
    emitter.ins('moveq','#0,%d1',2)
    emitter.ins('move.b','(%a2, %d0.w),%d1',4)
    emitter.ins('lsl.l','#0x5,%d1',2)
    emitter.ins('adda.l','%d1,%a1',2)
    emitter.ins('move.w','#0x7,%d2',4)
    emitter.ins('lea.l','0xfb00:w,%a2',4)
    emitter.ins('cmpi.w','#0x2,0xf6c4:w',6)
    emitter.ins('bne.w','scene_pc_0662a6',4)
    emitter.ins('lea.l','0xfb20:w,%a2',4)
    emitter.ins('move.l','(%a1)+,(%a2)+',2)
    emitter.ins('dbra','%d2,scene_pc_0662a6',4)
    emitter.ins('move.w','#0x1,0xf31e:w',6)
    emitter.ins('rts','',2)

def _lower_upload_scene_tile_block(emitter,rules):
    emitter.segment(0x662b4,0x662c4)
    emitter.ins('move.w','#0x2f,%d4',4)
    emitter.ins('move.w','(%a0)+,%d2',2)
    emitter.ins('bsr.w','scene_pc_0662c4',4)
    emitter.ins('dbra','%d4,scene_pc_0662b8',4)
    emitter.ins('rts','',2)

def _lower_upload_one_scene_tile(emitter,rules):
    emitter.segment(0x662c4,0x662e4)
    emitter.ins('lea.l','0xb649a:l,%a1',6)
    emitter.ins('andi.l','#0xffff,%d2',6)
    emitter.ins('lsl.l','#0x5,%d2',2)
    emitter.ins('adda.l','%d2,%a1',2)
    emitter.ins('move.w','#0x7,%d3',4)
    emitter.ins('move.l','(%a1)+,0xc00000:l',6)
    emitter.ins('dbra','%d3,scene_pc_0662d8',4)
    emitter.ins('rts','',2)

LOWERERS={
    'upload_object_officer_name':_lower_upload_object_officer_name,
    'start_object_left':_lower_start_object_left,
    'resume_object_selected_action':_lower_resume_object_selected_action,
    'finish_object_action_noop':_lower_finish_object_action_noop,
    'resume_object_pursuit':_lower_resume_object_pursuit,
    'advance_object_impact':_lower_advance_object_impact,
    'probe_object_left':_lower_probe_object_left,
    'object_movement_speed':_lower_object_movement_speed,
    'probe_object_right':_lower_probe_object_right,
    'probe_object_up':_lower_probe_object_up,
    'probe_object_down':_lower_probe_object_down,
    'calculate_object_impact_damage':_lower_calculate_object_impact_damage,
    'update_object_action_ai':_lower_update_object_action_ai,
    'dispatch_object_formation_ai':_lower_dispatch_object_formation_ai,
    'dispatch_object_formation_fallback':_lower_dispatch_object_formation_fallback,
    'advance_object_retreat_checks':_lower_advance_object_retreat_checks,
    'trigger_object_retreat_strength':_lower_trigger_object_retreat_strength,
    'sum_live_object_rosters':_lower_sum_live_object_rosters,
    'choose_object_retreat_phase':_lower_choose_object_retreat_phase,
    'upload_portrait_tiles':_lower_upload_portrait_tiles,
    'upload_scene_tile_block':_lower_upload_scene_tile_block,
    'upload_one_scene_tile':_lower_upload_one_scene_tile,
}

def compile_actions(source):
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    sole_motion_fields = {name: records[name]['effects'] for name in ('_object_action_legacy_fields', '_object_direction_probe_fields', '_object_motion_call_fields', '_object_motion_finish_fields', '_object_pursuit_abs_axis_fields', '_object_pursuit_horizontal_fields', '_object_pursuit_other_horizontal_fields', '_object_pursuit_other_vertical_fields', '_object_pursuit_probe_fields', '_object_pursuit_random_vertical_fields', '_object_pursuit_store_fields', '_object_pursuit_try_increasing_fields', '_object_pursuit_vertical_fields', 'continue_object_motion_fields', 'dispatch_object_action_fields', 'object_movement_speed_fields', 'pursue_opposing_object_fields', 'resume_object_pursuit_fields', 'sidestep_opposing_object_fields', 'start_object_motion_fields')}
    for owner in ('start_object_left', 'resume_object_selected_action', 'finish_object_action_noop', 'resume_object_pursuit', 'probe_object_left', 'object_movement_speed', 'probe_object_right', 'probe_object_up', 'probe_object_down'):
        records[owner]['effects'] = dict(previous=records[owner]['effects'], sole_motion_fields=sole_motion_fields)
    sole_impact_fields = {name: records[name]['effects'] for name in ('_apply_object_damage_fields', '_draw_object_impact_flash_fields', '_object_impact_call_fields', '_object_impact_restore_long_fields', '_object_impact_timer_fields', '_object_projectile_motion_fields', '_object_weighted_damage_fields', 'adjust_damage_for_object_guard_fields', 'advance_object_impact_fields', 'advance_object_projectile_fields', 'calculate_object_impact_damage_fields', 'dispatch_object_action_fields')}
    for owner in ('advance_object_impact', 'calculate_object_impact_damage'):
        records[owner]['effects'] = dict(previous=records[owner]['effects'], sole_impact_fields=sole_impact_fields)
    sole_ai_retreat_fields = {name: records[name]['effects'] for name in ('_object_ai_call_fields', '_object_retreat_roll_fields', '_set_all_object_retreat_modes_fields', 'advance_object_retreat_checks_fields', 'choose_object_retreat_phase_fields', 'dispatch_object_formation_ai_fields', 'dispatch_object_formation_fallback_fields', 'sum_live_object_rosters_fields', 'trigger_object_retreat_check_fields', 'trigger_object_retreat_low_strength_fields', 'trigger_object_retreat_morale_fields', 'trigger_object_retreat_outnumbered_fields', 'trigger_object_retreat_quality_fields', 'trigger_object_retreat_strength_fields', 'update_object_action_ai_fields')}
    for owner in ('update_object_action_ai', 'dispatch_object_formation_ai', 'dispatch_object_formation_fallback', 'advance_object_retreat_checks', 'trigger_object_retreat_strength', 'sum_live_object_rosters', 'choose_object_retreat_phase'):
        records[owner]['effects'] = dict(previous=records[owner]['effects'], sole_ai_retreat_fields=sole_ai_retreat_fields)
    for owner, field in (('upload_object_officer_name', 'upload_object_officer_name_frame_fields'), ('upload_portrait_tiles', 'upload_portrait_tiles_frame_fields'), ('upload_scene_tile_block', 'upload_scene_tile_block_frame_fields'), ('upload_one_scene_tile', 'upload_one_scene_tile_frame_fields')):
        records[owner]['effects'] = dict(historical_projection=records[owner]['effects'], sole_complete_fields=records[field]['effects'], parameter_edit_status='NOT_AVAILABLE')
    return lower_declared(records, ACTIONS_BINDINGS, LOWERERS)

# B35 sole full movement/action fields; ordinary native lowering unchanged.
for _module,_names in {'contexts_actions': ['DuelGlyphContext',
                      'ObjectActionResult',
                      'ObjectGlyphResult',
                      'ObjectPositionOffset',
                      'ObjectRosterTotals',
                      'ObjectVectorContext',
                      'SceneRenderFrame',
                      'SpriteBatchContext',
                      'TileUploadResult',
                      'checked_action',
                      'checked_controller_frame'],
 'domain': ['Boundary',
            'Cursor',
            'Long',
            'SceneState',
            'StackContinuation',
            'Table',
            'Word',
            'checked_cursor',
            'checked_state',
            'checked_table',
            'descending_inclusive',
            'divu_retained',
            'low16',
            'low8',
            'negative_word',
            'ram_view',
            'replace_byte',
            'replace_word',
            's16',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'],
 'services': ['BattlePresentationMemory',
              'FirstDeploymentFrame',
              'SceneRefreshBoundary',
              'SceneRefreshMemory',
              '_first_long',
              '_first_word',
              '_movement_binary_flags',
              '_object_clear_word_fields',
              '_presentation_call_fields',
              '_scene_controller_legacy_fields',
              '_scene_controller_legacy_projection',
              '_scene_refresh_emit',
              '_scene_refresh_flags',
              '_scene_render_arithmetic',
              '_scene_render_asl_word',
              '_scene_render_bit',
              '_scene_render_compare',
              'append_scene_sprite_entries',
              'decode_glyph_rows_to_buffers',
              'enqueue_sound_command',
              'first_replace',
              'offset_scene_object_position',
              'plan_scene_object_action',
              'probe_scene_object_overlap_fields',
              'probe_scene_object_overlap_with_frame',
              'read_object_action_mode',
              'read_object_action_mode_fields',
              'resume_selected_object_action',
              'sample_random_pair',
              'sample_random_preserving_seed_carrier',
              'sample_random_preserving_seed_fields',
              'update_selected_object_action_fields']}.items():
    APPROVED.setdefault(_module,set()).update(_names)
DECLARATIONS.update({'_continue_object_motion': {'signature': 'state, actor, opponent, frame, direction',
                             'returns': None,
                             'flow': 'actual = continue_object_motion_fields(SceneRefreshMemory(state), '
                                     '_object_action_legacy_fields(state, actor, opponent, frame), direction)\n'
                                     'current = _scene_controller_legacy_projection(state, actual)\n'
                                     'return (_object_action_legacy_result(state, actual), current.conditions)'},
 '_dispatch_primary_action': {'signature': 'state, actor, opponent, frame, *, resumed',
                              'returns': None,
                              'flow': 'actual = _object_action_legacy_fields(state, actor, opponent, frame)\n'
                                      'target = u32((265550 if resumed else 265484) + s16(low16(actual.target_x)))\n'
                                      'return _object_action_legacy_result(state, '
                                      'dispatch_object_action_fields(SceneRefreshMemory(state), actual, target))'},
 '_finish_action': {'signature': 'state, actor, opponent, frame',
                    'returns': None,
                    'flow': 'actual = _object_motion_finish_fields(SceneRefreshMemory(state), '
                            '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                            'return _object_action_legacy_result(state, actual)'},
 '_object_action_legacy_fields': {'signature': 'state, actor, opponent, frame',
                                  'returns': None,
                                  'flow': 'checked_action(state, actor, opponent, frame)\n'
                                          'current = checked_controller_frame(frame, state)\n'
                                          'actual = _scene_controller_legacy_fields(state, current)\n'
                                          'return first_replace(actual, auxiliary=actor.cursor(), scratch=opponent.cursor())'},
 '_object_action_legacy_result': {'signature': 'state, actual',
                                  'returns': None,
                                  'flow': 'current = _scene_controller_legacy_projection(state, actual)\n'
                                          'frame = SceneRenderFrame(current.x, current.y, current.attributes, current.palette, '
                                          'current.tile, current)\n'
                                          'return ObjectActionResult(state.table_at(actual.auxiliary.base), '
                                          'state.table_at(actual.scratch.base), frame)'},
 '_object_direction_probe_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, direction: Word',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'memory.frame(frame)\n'
                                            'if frame.stack_cursor is None or direction not in (0, 1, 2, 3):\n'
                                            '    raise SceneRefreshBoundary(265684, frame, None)\n'
                                            'horizontal, vertical, continuation = ((32784, 0, 265700), (16, 0, 265824), (0, '
                                            '32784, 265914), (0, 16, 266004))[direction]\n'
                                            'memory.sync_status(frame)\n'
                                            'frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(-4))\n'
                                            'frame.stack_cursor.set_long(0, frame.scratch.base)\n'
                                            "frame = _first_word(frame, 'target_x', horizontal)\n"
                                            "frame = _first_word(frame, 'target_y', vertical)\n"
                                            'frame = _object_motion_call_fields(memory, frame, 266588, continuation)\n'
                                            'restored = frame.stack_cursor.long()\n'
                                            'return memory.sync_status(first_replace(frame, scratch=memory.cursor_at(restored), '
                                            'stack_cursor=frame.stack_cursor.advance(4)))'},
 '_object_motion_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, '
                                             'continuation: Long',
                                'returns': 'FirstDeploymentFrame',
                                'flow': 'if (target, continuation) not in ((265512, 265610), (265684, 265630), (265706, 265658), '
                                        '(266588, 265700), (265512, 265732), (265808, 265754), (265706, 265782), (266588, '
                                        '265824), (265898, 265834), (265706, 265872), (266588, 265914), (265988, 265924), '
                                        '(265706, 265962), (266588, 266004), (265898, 266198), (243490, 266236), (265684, '
                                        '266262), (265808, 266286), (265988, 266306), (265684, 266342), (243490, 266380), '
                                        '(265988, 266406), (265898, 266430), (265808, 266450), (265808, 266530), (265684, '
                                        '266550), (243490, 266566)):\n'
                                        "    raise ValueError('actual object movement call/token pair required')\n"
                                        'memory.frame(frame)\n'
                                        'def child(actual_memory, entered):\n'
                                        '    scene = SceneRefreshMemory(actual_memory.state)\n'
                                        '    if target == 265512:\n'
                                        '        return read_object_action_mode_fields(scene, entered)\n'
                                        '    if target == 265706:\n'
                                        '        return object_movement_speed_fields(scene, entered)\n'
                                        '    if target == 266588:\n'
                                        '        return probe_scene_object_overlap_fields(scene, entered)\n'
                                        '    if target == 243490:\n'
                                        '        return sample_random_preserving_seed_fields(scene, entered)\n'
                                        '    for address, direction in ((265684, 0), (265808, 1), (265898, 2), (265988, 3)):\n'
                                        '        if target == address:\n'
                                        '            return _object_direction_probe_fields(scene, entered, direction)\n'
                                        '    raise SceneRefreshBoundary(target, entered, continuation)\n'
                                        'return _presentation_call_fields(BattlePresentationMemory(memory.state), frame, '
                                        'continuation, child)'},
 '_object_motion_finish_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'return _object_clear_word_fields(memory, frame, 4294934866)'},
 '_object_pursuit_abs_axis_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name: str, axis: '
                                                  'Word',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'own = frame.auxiliary.word(0, axis)\n'
                                             'frame = _first_word(frame, name, own)\n'
                                             'other = frame.scratch.word(0, axis)\n'
                                             'frame = _scene_render_arithmetic(memory, frame, name, own, other, 16, True)\n'
                                             'if low16(frame.carrier(name)) & 32768:\n'
                                             '    frame = _scene_render_arithmetic(memory, frame, name, 0, '
                                             'low16(frame.carrier(name)), 16, True)\n'
                                             'return memory.sync_status(frame)'},
 '_object_pursuit_horizontal_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'frame = _object_pursuit_store_fields(memory, frame, 0)\n'
                                               'own = frame.auxiliary.word(0, 2)\n'
                                               "frame = _first_word(frame, 'target_x', own)\n"
                                               'other = frame.scratch.word(0, 2)\n'
                                               'frame = _scene_render_compare(memory, frame, own, other, 16)\n'
                                               'if own > other:\n'
                                               '    return start_object_motion_fields(memory, frame, 0)\n'
                                               'frame = _object_pursuit_store_fields(memory, frame, 1)\n'
                                               'frame = _object_motion_call_fields(memory, frame, 243490, 266236)\n'
                                               'frame = _scene_render_bit(memory, frame, frame.target_x, 2)\n'
                                               'if frame.target_x & 2:\n'
                                               '    position = frame.auxiliary.word(0, 2)\n'
                                               '    frame = _scene_render_compare(memory, frame, position, 0, 16)\n'
                                               '    if position <= 0:\n'
                                               '        return start_object_motion_fields(memory, frame, 1)\n'
                                               '    frame = _object_pursuit_probe_fields(memory, frame, 265684, 266262)\n'
                                               '    return start_object_motion_fields(memory, frame, 0 if low16(frame.target_x) '
                                               '== 0 else 1)\n'
                                               'position = frame.auxiliary.word(0, 2)\n'
                                               'frame = _scene_render_compare(memory, frame, position, 352, 16)\n'
                                               'if position >= 352:\n'
                                               '    return start_object_motion_fields(memory, frame, 0)\n'
                                               'frame = _object_pursuit_probe_fields(memory, frame, 265808, 266286)\n'
                                               'return start_object_motion_fields(memory, frame, 1 if low16(frame.target_x) == 0 '
                                               'else 0)'},
 '_object_pursuit_other_horizontal_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                             'returns': 'FirstDeploymentFrame',
                                             'flow': 'frame = _object_pursuit_store_fields(memory, frame, 1)\n'
                                                     'own = frame.auxiliary.word(0, 2)\n'
                                                     "frame = _first_word(frame, 'target_x', own)\n"
                                                     'other = frame.scratch.word(0, 2)\n'
                                                     'frame = _scene_render_compare(memory, frame, own, other, 16)\n'
                                                     'if own < other:\n'
                                                     '    frame = _object_pursuit_store_fields(memory, frame, 1)\n'
                                                     '    frame = _object_pursuit_probe_fields(memory, frame, 265808, 266450)\n'
                                                     '    if low16(frame.target_x) == 0:\n'
                                                     '        return start_object_motion_fields(memory, frame, 1)\n'
                                                     'else:\n'
                                                     '    frame = _object_pursuit_store_fields(memory, frame, 0)\n'
                                                     '    frame = _object_pursuit_probe_fields(memory, frame, 265684, 266342)\n'
                                                     '    if low16(frame.target_x) == 0:\n'
                                                     '        return start_object_motion_fields(memory, frame, 0)\n'
                                                     'return _object_pursuit_other_vertical_fields(memory, frame)'},
 '_object_pursuit_other_vertical_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                           'returns': 'FirstDeploymentFrame',
                                           'flow': 'frame = _object_pursuit_store_fields(memory, frame, 3)\n'
                                                   'own = frame.auxiliary.word(0, 4)\n'
                                                   "frame = _first_word(frame, 'target_x', own)\n"
                                                   'other = frame.scratch.word(0, 4)\n'
                                                   'frame = _scene_render_compare(memory, frame, own, other, 16)\n'
                                                   'if own < other:\n'
                                                   '    return start_object_motion_fields(memory, frame, 3)\n'
                                                   'frame = _object_pursuit_store_fields(memory, frame, 2)\n'
                                                   'return start_object_motion_fields(memory, frame, 2)'},
 '_object_pursuit_probe_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, '
                                               'continuation: Long',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'frame = _object_motion_call_fields(memory, frame, target, continuation)\n'
                                          'return _scene_refresh_flags(memory, frame, low16(frame.target_x), 2)'},
 '_object_pursuit_random_vertical_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                            'returns': 'FirstDeploymentFrame',
                                            'flow': 'frame = _object_motion_call_fields(memory, frame, 243490, 266380)\n'
                                                    'frame = _scene_render_bit(memory, frame, frame.target_x, 2)\n'
                                                    'if frame.target_x & 2:\n'
                                                    '    position = frame.auxiliary.word(0, 4)\n'
                                                    '    frame = _scene_render_compare(memory, frame, position, 288, 16)\n'
                                                    '    if position >= 288:\n'
                                                    '        return _object_pursuit_try_increasing_fields(memory, frame)\n'
                                                    '    frame = _object_pursuit_probe_fields(memory, frame, 265988, 266406)\n'
                                                    '    return start_object_motion_fields(memory, frame, 3 if '
                                                    'low16(frame.target_x) == 0 else 2)\n'
                                                    'position = frame.auxiliary.word(0, 4)\n'
                                                    'frame = _scene_render_compare(memory, frame, position, 32, 16)\n'
                                                    'if position <= 32:\n'
                                                    '    return start_object_motion_fields(memory, frame, 3)\n'
                                                    'frame = _object_pursuit_probe_fields(memory, frame, 265898, 266430)\n'
                                                    'return start_object_motion_fields(memory, frame, 2 if low16(frame.target_x) '
                                                    '== 0 else 3)'},
 '_object_pursuit_store_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, direction: Word',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'return _scene_refresh_emit(memory, frame, u32(frame.auxiliary.base + 10), 2, '
                                          'direction)'},
 '_object_pursuit_try_increasing_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                           'returns': 'FirstDeploymentFrame',
                                           'flow': 'frame = _object_pursuit_store_fields(memory, frame, 3)\n'
                                                   'frame = _object_pursuit_probe_fields(memory, frame, 265988, 266306)\n'
                                                   'if low16(frame.target_x) == 0:\n'
                                                   '    return start_object_motion_fields(memory, frame, 3)\n'
                                                   'return _object_pursuit_horizontal_fields(memory, frame)'},
 '_object_pursuit_vertical_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'frame = _object_pursuit_store_fields(memory, frame, 3)\n'
                                             'own = frame.auxiliary.word(0, 4)\n'
                                             "frame = _first_word(frame, 'target_x', own)\n"
                                             'other = frame.scratch.word(0, 4)\n'
                                             'frame = _scene_render_compare(memory, frame, own, other, 16)\n'
                                             'if own < other:\n'
                                             '    return _object_pursuit_try_increasing_fields(memory, frame)\n'
                                             'else:\n'
                                             '    frame = _object_pursuit_store_fields(memory, frame, 2)\n'
                                             '    frame = _object_pursuit_probe_fields(memory, frame, 265898, 266198)\n'
                                             '    if low16(frame.target_x) == 0:\n'
                                             '        return start_object_motion_fields(memory, frame, 2)\n'
                                             'return _object_pursuit_horizontal_fields(memory, frame)'},
 '_pursue_horizontal': {'signature': 'state, actor, opponent, frame',
                        'returns': None,
                        'flow': 'actual = _object_pursuit_horizontal_fields(SceneRefreshMemory(state), '
                                '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                'return _object_action_legacy_result(state, actual)'},
 '_pursue_other_horizontal': {'signature': 'state, actor, opponent, frame',
                              'returns': None,
                              'flow': 'actual = _object_pursuit_other_horizontal_fields(SceneRefreshMemory(state), '
                                      '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                      'return _object_action_legacy_result(state, actual)'},
 '_pursue_other_vertical': {'signature': 'state, actor, opponent, frame',
                            'returns': None,
                            'flow': 'actual = _object_pursuit_other_vertical_fields(SceneRefreshMemory(state), '
                                    '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                    'return _object_action_legacy_result(state, actual)'},
 '_pursue_vertical': {'signature': 'state, actor, opponent, frame',
                      'returns': None,
                      'flow': 'actual = _object_pursuit_vertical_fields(SceneRefreshMemory(state), '
                              '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                              'return _object_action_legacy_result(state, actual)'},
 '_random_vertical_maneuver': {'signature': 'state, actor, opponent, frame',
                               'returns': None,
                               'flow': 'actual = _object_pursuit_random_vertical_fields(SceneRefreshMemory(state), '
                                       '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                       'return _object_action_legacy_result(state, actual)'},
 '_resume_primary_action_selection': {'signature': 'state, actor, opponent, frame',
                                      'returns': None,
                                      'flow': 'actual = update_selected_object_action_fields(SceneRefreshMemory(state), '
                                              '_object_action_legacy_fields(state, actor, opponent, frame), '
                                              'primary_middle=True)\n'
                                              'return _object_action_legacy_result(state, actual)'},
 '_resume_pursuit_direction': {'signature': 'state, actor, opponent, frame',
                               'returns': None,
                               'flow': 'actual = resume_object_pursuit_fields(SceneRefreshMemory(state), '
                                       '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                       'return _object_action_legacy_result(state, actual)'},
 '_try_up': {'signature': 'state, actor, opponent, frame',
             'returns': None,
             'flow': 'actual = _object_pursuit_try_increasing_fields(SceneRefreshMemory(state), '
                     '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                     'return _object_action_legacy_result(state, actual)'},
 'continue_object_down': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                          'returns': 'ObjectActionResult',
                          'flow': 'actual = continue_object_motion_fields(SceneRefreshMemory(state), '
                                  '_object_action_legacy_fields(state, actor, opponent, frame), 3)\n'
                                  'return _object_action_legacy_result(state, actual)'},
 'continue_object_left': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                          'returns': 'ObjectActionResult',
                          'flow': 'actual = continue_object_motion_fields(SceneRefreshMemory(state), '
                                  '_object_action_legacy_fields(state, actor, opponent, frame), 0)\n'
                                  'return _object_action_legacy_result(state, actual)'},
 'continue_object_motion_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, direction: Word',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'memory.frame(frame)\n'
                                           'if frame.stack_cursor is None or direction not in (0, 1, 2, 3):\n'
                                           '    raise SceneRefreshBoundary(265654, frame, None)\n'
                                           'axis = 2 if direction < 2 else 4\n'
                                           'continuation = (265658, 265782, 265872, 265962)[direction]\n'
                                           'frame = _object_motion_call_fields(memory, frame, 265706, continuation)\n'
                                           'previous = frame.auxiliary.word(0, axis)\n'
                                           'frame, value = _movement_binary_flags(memory.state, frame, previous, '
                                           'low16(frame.target_x), 16, direction in (0, 2))\n'
                                           'frame.auxiliary.set_word(0, value, axis)\n'
                                           'position = frame.auxiliary.word(0, axis)\n'
                                           "frame = _first_word(frame, 'target_x', position)\n"
                                           'target = memory.state.read(4294934870, 2)\n'
                                           'frame = _scene_render_compare(memory, frame, position, target, 16)\n'
                                           'finished = position <= target if direction == 0 else position >= target if direction '
                                           '== 1 else position == target\n'
                                           'if not finished:\n'
                                           '    return memory.sync_status(frame)\n'
                                           'current = frame.auxiliary.word(0, axis)\n'
                                           'value = current & 504\n'
                                           'frame = _scene_refresh_flags(memory, frame, value, 2)\n'
                                           'frame.auxiliary.set_word(0, value, axis)\n'
                                           'return _object_motion_finish_fields(memory, frame)'},
 'continue_object_motion_frame': {'signature': 'state, frame, direction',
                                  'returns': None,
                                  'flow': 'actual = continue_object_motion_fields(SceneRefreshMemory(state), '
                                          '_scene_controller_legacy_fields(state, frame), direction)\n'
                                          'return _scene_controller_legacy_projection(state, actual)'},
 'continue_object_right': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                           'returns': 'ObjectActionResult',
                           'flow': 'actual = continue_object_motion_fields(SceneRefreshMemory(state), '
                                   '_object_action_legacy_fields(state, actor, opponent, frame), 1)\n'
                                   'return _object_action_legacy_result(state, actual)'},
 'continue_object_up': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                        'returns': 'ObjectActionResult',
                        'flow': 'actual = continue_object_motion_fields(SceneRefreshMemory(state), '
                                '_object_action_legacy_fields(state, actor, opponent, frame), 2)\n'
                                'return _object_action_legacy_result(state, actual)'},
 'dispatch_object_action_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'memory.frame(frame)\n'
                                           'for address, direction in ((265484, 0), (265488, 1), (265492, 2), (265496, 3)):\n'
                                           '    if target == address:\n'
                                           '        return start_object_motion_fields(memory, frame, direction)\n'
                                           'for address, direction in ((265550, 0), (265554, 1), (265558, 2), (265562, 3), '
                                           '(266120, 0), (266124, 1), (266128, 2), (266132, 3)):\n'
                                           '    if target == address:\n'
                                           '        return continue_object_motion_fields(memory, frame, direction)\n'
                                           'if target == 265504:\n'
                                           '    return pursue_opposing_object_fields(memory, frame)\n'
                                           'if target == 265508:\n'
                                           '    return sidestep_opposing_object_fields(memory, frame)\n'
                                           'if target == 265500:\n'
                                           '    return update_selected_object_action_fields(memory, frame, primary_middle=True)\n'
                                           'if target == 265566:\n'
                                           '    return _object_motion_finish_fields(memory, frame)\n'
                                           'if target in (265570, 265574, 265578):\n'
                                           '    return resume_object_pursuit_fields(memory, frame)\n'
                                           'raise SceneRefreshBoundary(target, frame, None)'},
 'finish_object_action_noop': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                               'returns': 'ObjectActionResult',
                               'flow': 'actual = _object_motion_finish_fields(SceneRefreshMemory(state), '
                                       '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                       'return _object_action_legacy_result(state, actual)'},
 'object_movement_speed': {'signature': 'state: SceneState',
                           'returns': 'Long',
                           'flow': 'actual = object_movement_speed_fields(SceneRefreshMemory(state), '
                                   'FirstDeploymentFrame.unobserved())\n'
                                   'return actual.target_x'},
 'object_movement_speed_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'memory.frame(frame)\n'
                                          "frame = _first_long(frame, 'target_x', 2)\n"
                                          'memory.sync_status(frame)\n'
                                          'option = memory.state.read(4294935562, 2)\n'
                                          'frame = _scene_refresh_flags(memory, frame, option, 2)\n'
                                          'if option != 0:\n'
                                          "    frame = _first_long(frame, 'target_x', 4)\n"
                                          'return memory.sync_status(frame)'},
 'probe_object_down': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                       'returns': 'ObjectActionResult',
                       'flow': 'actual = _object_direction_probe_fields(SceneRefreshMemory(state), '
                               '_object_action_legacy_fields(state, actor, opponent, frame), 3)\n'
                               'return _object_action_legacy_result(state, actual)'},
 'probe_object_left': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                       'returns': 'ObjectActionResult',
                       'flow': 'actual = _object_direction_probe_fields(SceneRefreshMemory(state), '
                               '_object_action_legacy_fields(state, actor, opponent, frame), 0)\n'
                               'return _object_action_legacy_result(state, actual)'},
 'probe_object_right': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                        'returns': 'ObjectActionResult',
                        'flow': 'actual = _object_direction_probe_fields(SceneRefreshMemory(state), '
                                '_object_action_legacy_fields(state, actor, opponent, frame), 1)\n'
                                'return _object_action_legacy_result(state, actual)'},
 'probe_object_up': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                     'returns': 'ObjectActionResult',
                     'flow': 'actual = _object_direction_probe_fields(SceneRefreshMemory(state), '
                             '_object_action_legacy_fields(state, actor, opponent, frame), 2)\n'
                             'return _object_action_legacy_result(state, actual)'},
 'pursue_opposing_object': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                            'returns': 'ObjectActionResult',
                            'flow': 'actual = pursue_opposing_object_fields(SceneRefreshMemory(state), '
                                    '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                    'return _object_action_legacy_result(state, actual)'},
 'pursue_opposing_object_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'memory.frame(frame)\n'
                                           'if frame.stack_cursor is None:\n'
                                           '    raise SceneRefreshBoundary(266010, frame, None)\n'
                                           'frame = _scene_render_compare(memory, frame, frame.auxiliary.base, 4294935146, 32)\n'
                                           'frame = first_replace(frame, scratch=memory.cursor_at(4294934890 if '
                                           'frame.auxiliary.base >= 4294935146 else 4294935146))\n'
                                           'mode = memory.state.read(4294934747, 1)\n'
                                           'frame = _scene_render_compare(memory, frame, mode, 3, 8)\n'
                                           'if mode != 3:\n'
                                           '    kind = frame.auxiliary.byte(0, 1)\n'
                                           '    frame = _scene_refresh_flags(memory, frame, kind, 1)\n'
                                           '    if kind != 0:\n'
                                           '        kind = frame.auxiliary.byte(0, 1)\n'
                                           '        frame = _scene_render_compare(memory, frame, kind, 1, 8)\n'
                                           '        if kind == 1:\n'
                                           "            frame = _object_pursuit_abs_axis_fields(memory, frame, 'target_x', 4)\n"
                                           '            frame = _scene_render_compare(memory, frame, low16(frame.target_x), 16, '
                                           '16)\n'
                                           '            if low16(frame.target_x) > 16:\n'
                                           '                return _object_pursuit_vertical_fields(memory, frame)\n'
                                           '            return _object_pursuit_other_horizontal_fields(memory, frame)\n'
                                           '        kind = frame.auxiliary.byte(0, 1)\n'
                                           '        frame = _scene_render_compare(memory, frame, kind, 2, 8)\n'
                                           "        frame = _object_pursuit_abs_axis_fields(memory, frame, 'target_x', 2)\n"
                                           '        frame = _scene_render_compare(memory, frame, low16(frame.target_x), 16, 16)\n'
                                           '        if low16(frame.target_x) > 16:\n'
                                           '            return _object_pursuit_other_horizontal_fields(memory, frame)\n'
                                           '        return _object_pursuit_vertical_fields(memory, frame)\n'
                                           "frame = _object_pursuit_abs_axis_fields(memory, frame, 'target_x', 2)\n"
                                           "frame = _object_pursuit_abs_axis_fields(memory, frame, 'target_y', 4)\n"
                                           'frame = _scene_render_compare(memory, frame, low16(frame.target_y), '
                                           'low16(frame.target_x), 16)\n'
                                           'if low16(frame.target_y) < low16(frame.target_x):\n'
                                           '    return _object_pursuit_other_horizontal_fields(memory, frame)\n'
                                           'return _object_pursuit_vertical_fields(memory, frame)'},
 'resume_object_pursuit': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                           'returns': 'ObjectActionResult',
                           'flow': 'actual = resume_object_pursuit_fields(SceneRefreshMemory(state), '
                                   '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                   'return _object_action_legacy_result(state, actual)'},
 'resume_object_pursuit_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'memory.frame(frame)\n'
                                          'value = frame.auxiliary.word(0, 10)\n'
                                          "frame = _first_word(frame, 'target_x', value)\n"
                                          "frame = _scene_render_asl_word(memory, frame, 'target_x', value, 2)\n"
                                          'target = u32(266120 + s16(u16(value << 2)))\n'
                                          'if target in (266120, 266124, 266128, 266132):\n'
                                          '    return continue_object_motion_fields(memory, frame, (target - 266120) // 4)\n'
                                          'raise SceneRefreshBoundary(target, frame, None)'},
 'resume_object_selected_action': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                                   'returns': 'ObjectActionResult',
                                   'flow': 'actual = update_selected_object_action_fields(SceneRefreshMemory(state), '
                                           '_object_action_legacy_fields(state, actor, opponent, frame), primary_middle=True)\n'
                                           'return _object_action_legacy_result(state, actual)'},
 'sidestep_opposing_object': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                              'returns': 'ObjectActionResult',
                              'flow': 'actual = sidestep_opposing_object_fields(SceneRefreshMemory(state), '
                                      '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                      'return _object_action_legacy_result(state, actual)'},
 'sidestep_opposing_object_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'memory.frame(frame)\n'
                                             'if frame.stack_cursor is None:\n'
                                             '    raise SceneRefreshBoundary(266512, frame, None)\n'
                                             'frame = _scene_render_compare(memory, frame, frame.auxiliary.base, 4294935146, '
                                             '32)\n'
                                             'if frame.auxiliary.base >= 4294935146:\n'
                                             '    frame = _object_pursuit_store_fields(memory, frame, 1)\n'
                                             '    frame = _object_pursuit_probe_fields(memory, frame, 265808, 266530)\n'
                                             '    if low16(frame.target_x) == 0:\n'
                                             '        return start_object_motion_fields(memory, frame, 1)\n'
                                             'else:\n'
                                             '    frame = _object_pursuit_store_fields(memory, frame, 0)\n'
                                             '    frame = _object_pursuit_probe_fields(memory, frame, 265684, 266550)\n'
                                             '    if low16(frame.target_x) == 0:\n'
                                             '        return start_object_motion_fields(memory, frame, 0)\n'
                                             'frame = _object_pursuit_store_fields(memory, frame, 3)\n'
                                             'frame = _object_motion_call_fields(memory, frame, 243490, 266566)\n'
                                             'other_y = frame.scratch.word(0, 4)\n'
                                             'frame = _scene_render_compare(memory, frame, low16(frame.target_x), other_y, 16)\n'
                                             'frame = _scene_render_bit(memory, frame, frame.target_x, 16)\n'
                                             'if frame.target_x & 16:\n'
                                             '    return start_object_motion_fields(memory, frame, 3)\n'
                                             'frame = _object_pursuit_store_fields(memory, frame, 2)\n'
                                             'return start_object_motion_fields(memory, frame, 2)'},
 'start_object_down': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                       'returns': 'ObjectActionResult',
                       'flow': 'actual = start_object_motion_fields(SceneRefreshMemory(state), '
                               '_object_action_legacy_fields(state, actor, opponent, frame), 3)\n'
                               'return _object_action_legacy_result(state, actual)'},
 'start_object_left': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                       'returns': 'ObjectActionResult',
                       'flow': 'actual = start_object_motion_fields(SceneRefreshMemory(state), '
                               '_object_action_legacy_fields(state, actor, opponent, frame), 0)\n'
                               'return _object_action_legacy_result(state, actual)'},
 'start_object_motion_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, direction: Word',
                                'returns': 'FirstDeploymentFrame',
                                'flow': 'memory.frame(frame)\n'
                                        'if frame.stack_cursor is None or direction not in (0, 1, 2, 3):\n'
                                        '    raise SceneRefreshBoundary(265484, frame, None)\n'
                                        'axis = 2 if direction < 2 else 4\n'
                                        'if direction < 2:\n'
                                        '    position = frame.auxiliary.word(0, axis)\n'
                                        '    limit = 0 if direction == 0 else 352\n'
                                        '    frame = _scene_render_compare(memory, frame, position, limit, 16)\n'
                                        '    at_edge = position <= limit if direction == 0 else position >= limit\n'
                                        '    if at_edge:\n'
                                        '        frame = _object_motion_call_fields(memory, frame, 265512, 265610 if direction '
                                        '== 0 else 265732)\n'
                                        '        frame = _scene_render_compare(memory, frame, low16(frame.target_x), 6, 16)\n'
                                        '        if low16(frame.target_x) == 6:\n'
                                        '            frame = _scene_refresh_emit(memory, frame, u32(frame.auxiliary.base + 2), '
                                        '2, 512)\n'
                                        '        return _object_motion_finish_fields(memory, frame)\n'
                                        'probe, continuation = ((265684, 265630), (265808, 265754), (265898, 265834), (265988, '
                                        '265924))[direction]\n'
                                        'frame = _object_motion_call_fields(memory, frame, probe, continuation)\n'
                                        'frame = _scene_refresh_flags(memory, frame, low16(frame.target_x), 2)\n'
                                        'if low16(frame.target_x):\n'
                                        '    return _object_motion_finish_fields(memory, frame)\n'
                                        'if direction >= 2:\n'
                                        '    position = frame.auxiliary.word(0, 4)\n'
                                        '    limit = 32 if direction == 2 else 288\n'
                                        '    frame = _scene_render_compare(memory, frame, position, limit, 16)\n'
                                        '    at_edge = position <= limit if direction == 2 else position >= limit\n'
                                        '    if at_edge:\n'
                                        '        return _object_motion_finish_fields(memory, frame)\n'
                                        'position = frame.auxiliary.word(0, axis)\n'
                                        "frame = _first_word(frame, 'target_x', position)\n"
                                        "frame = _scene_render_arithmetic(memory, frame, 'target_x', position, 16, 16, direction "
                                        'in (0, 2))\n'
                                        'frame = _scene_refresh_emit(memory, frame, 4294934870, 2, low16(frame.target_x))\n'
                                        'frame = _scene_refresh_emit(memory, frame, u32(frame.auxiliary.base + 8), 2, (1, 0, 3, '
                                        '2)[direction])\n'
                                        'return continue_object_motion_fields(memory, frame, direction)'},
 'start_object_right': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                        'returns': 'ObjectActionResult',
                        'flow': 'actual = start_object_motion_fields(SceneRefreshMemory(state), '
                                '_object_action_legacy_fields(state, actor, opponent, frame), 1)\n'
                                'return _object_action_legacy_result(state, actual)'},
 'start_object_up': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                     'returns': 'ObjectActionResult',
                     'flow': 'actual = start_object_motion_fields(SceneRefreshMemory(state), _object_action_legacy_fields(state, '
                             'actor, opponent, frame), 2)\n'
                             'return _object_action_legacy_result(state, actual)'}})

# B36 sole impact/projectile fields; ordinary native lowering remains unchanged.
for _module,_names in {'contexts_actions': ['DuelGlyphContext',
                      'ObjectActionResult',
                      'ObjectGlyphResult',
                      'ObjectPositionOffset',
                      'ObjectRosterTotals',
                      'ObjectVectorContext',
                      'SceneRenderFrame',
                      'SpriteBatchContext',
                      'TileUploadResult',
                      'checked_action',
                      'checked_controller_frame'],
 'domain': ['Boundary',
            'Cursor',
            'Long',
            'SceneState',
            'StackContinuation',
            'Table',
            'Word',
            'checked_cursor',
            'checked_state',
            'checked_table',
            'descending_inclusive',
            'divu_retained',
            'low16',
            'low8',
            'negative_word',
            'ram_view',
            'replace_byte',
            'replace_word',
            's16',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'],
 'services': ['BattlePresentationMemory',
              'FirstDeploymentFrame',
              'SceneRefreshBoundary',
              'SceneRefreshMemory',
              '_append_object_sprite_fields',
              '_first_long',
              '_first_word',
              '_movement_binary_flags',
              '_movement_divu_word',
              '_object_adjust_word_fields',
              '_object_clear_word_fields',
              '_object_shift_word_right_fields',
              '_presentation_call_fields',
              '_scene_controller_legacy_fields',
              '_scene_controller_legacy_projection',
              '_scene_refresh_emit',
              '_scene_refresh_flags',
              '_scene_render_arithmetic',
              '_scene_render_asl_word',
              '_scene_render_bit',
              '_scene_render_compare',
              '_scene_render_push_longs',
              'append_scene_sprite_entries',
              'decode_glyph_rows_to_buffers',
              'enqueue_sound_command',
              'enqueue_sound_command_fields',
              'first_replace',
              'offset_scene_object_position',
              'offset_scene_object_position_fields',
              'plan_scene_object_action',
              'probe_scene_object_overlap_fields',
              'probe_scene_object_overlap_with_frame',
              'read_object_action_mode',
              'read_object_action_mode_fields',
              'resume_selected_object_action',
              'sample_random_pair',
              'sample_random_preserving_seed_carrier',
              'sample_random_preserving_seed_fields',
              'update_selected_object_action_fields']}.items():
    APPROVED.setdefault(_module,set()).update(_names)
DECLARATIONS.update({'_apply_object_damage': {'signature': 'state, actor, opponent, frame',
                          'returns': None,
                          'flow': 'actual = _apply_object_damage_fields(SceneRefreshMemory(state), '
                                  '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                  'return _object_action_legacy_result(state, actual)'},
 '_apply_object_damage_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                 'returns': 'FirstDeploymentFrame',
                                 'flow': 'memory.frame(frame)\n'
                                         'memory.sync_status(frame)\n'
                                         'previous = frame.scratch.word(0, 14)\n'
                                         'frame, remaining = _movement_binary_flags(memory.state, frame, previous, '
                                         'low16(frame.target_y), 16, True)\n'
                                         'memory.sync_status(frame)\n'
                                         'frame.scratch.set_word(0, remaining, 14)\n'
                                         'if remaining != 0 and (not remaining & 32768):\n'
                                         '    return _object_motion_finish_fields(memory, frame)\n'
                                         'frame = _object_clear_word_fields(memory, frame, u32(frame.scratch.base + 14))\n'
                                         'frame = _object_clear_word_fields(memory, frame, frame.scratch.base)\n'
                                         'frame = _scene_render_compare(memory, frame, frame.scratch.base, 4294935146, 32)\n'
                                         'if frame.scratch.base >= 4294935146:\n'
                                         '    leader = memory.state.read(4294935146, 2)\n'
                                         '    frame = _scene_refresh_flags(memory, frame, leader, 2)\n'
                                         '    if leader != 0:\n'
                                         '        return _object_motion_finish_fields(memory, frame)\n'
                                         '    frame = _scene_refresh_emit(memory, frame, 4294934804, 2, 2)\n'
                                         '    frame = _scene_refresh_emit(memory, frame, 4294934806, 2, 3)\n'
                                         'else:\n'
                                         '    leader = memory.state.read(4294934890, 2)\n'
                                         '    frame = _scene_refresh_flags(memory, frame, leader, 2)\n'
                                         '    if leader != 0:\n'
                                         '        return _object_motion_finish_fields(memory, frame)\n'
                                         '    frame = _scene_refresh_emit(memory, frame, 4294934804, 2, 3)\n'
                                         '    frame = _object_clear_word_fields(memory, frame, 4294934806)\n'
                                         'frame = _scene_refresh_emit(memory, frame, 4294934842, 2, 4)\n'
                                         'frame = _scene_refresh_emit(memory, frame, 4294934844, 2, 0)\n'
                                         'frame = _scene_refresh_emit(memory, frame, 4294934846, 2, 1)\n'
                                         "frame = _first_word(frame, 'target_x', memory.state.read(4294934860, 2))\n"
                                         "frame = _scene_render_arithmetic(memory, frame, 'target_x', low16(frame.target_x), 1, "
                                         '16, True)\n'
                                         "frame = _first_word(frame, 'target_x', low16(frame.target_x) ^ 1)\n"
                                         'frame = _scene_refresh_emit(memory, frame, 4294934902, 2, low16(frame.target_x))\n'
                                         'return _object_motion_finish_fields(memory, frame)'},
 '_draw_object_impact_flash': {'signature': 'state, actor, opponent, frame, *, projectile=False',
                               'returns': None,
                               'flow': 'actual = _draw_object_impact_flash_fields(SceneRefreshMemory(state), '
                                       '_object_action_legacy_fields(state, actor, opponent, frame), projectile)\n'
                                       'return _object_action_legacy_result(state, actual)'},
 '_draw_object_impact_flash_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, projectile: '
                                                   'bool=False',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': 'if type(projectile) is not bool:\n'
                                              "    raise ValueError('actual flash entry required')\n"
                                              'memory.frame(frame)\n'
                                              'memory.sync_status(frame)\n'
                                              "frame = _first_long(frame, 'target_x', frame.auxiliary.long(0, 2))\n"
                                              'memory.sync_status(frame)\n'
                                              'frame = _scene_render_push_longs(memory, frame, (frame.target_x,))\n'
                                              "frame = _first_word(frame, 'unit', memory.state.read(4294934872, 2))\n"
                                              "frame = _scene_render_asl_word(memory, frame, 'unit', low16(frame.unit), 2)\n"
                                              'memory.sync_status(frame)\n'
                                              "frame = _first_word(frame, 'target_x', memory.state.read(u32(267752 + "
                                              's16(low16(frame.unit))), 2))\n'
                                              'memory.sync_status(frame)\n'
                                              "frame = _first_word(frame, 'target_y', memory.state.read(u32(267754 + "
                                              's16(low16(frame.unit))), 2))\n'
                                              'frame = _object_impact_call_fields(memory, frame, 266658, 267810 if projectile '
                                              'else 267708)\n'
                                              'if projectile:\n'
                                              "    frame = _first_word(frame, 'target_x', memory.state.read(4294934884, 2))\n"
                                              '    memory.sync_status(frame)\n'
                                              "    frame = _first_word(frame, 'target_y', memory.state.read(4294934886, 2))\n"
                                              'else:\n'
                                              "    frame = _first_word(frame, 'target_x', frame.auxiliary.word(0, 2))\n"
                                              '    memory.sync_status(frame)\n'
                                              "    frame = _first_word(frame, 'target_y', frame.auxiliary.word(0, 4))\n"
                                              "frame = _first_word(frame, 'unit', 4)\n"
                                              "frame = _first_long(frame, 'count', 0)\n"
                                              "frame = _first_word(frame, 'distance', 256)\n"
                                              'frame = first_replace(frame, roster=memory.cursor_at(267746))\n'
                                              'frame = _object_impact_call_fields(memory, frame, 241980, 267736)\n'
                                              "frame = _object_impact_restore_long_fields(memory, frame, 'target_x')\n"
                                              'return _scene_refresh_emit(memory, frame, u32(frame.auxiliary.base + 2), 4, '
                                              'frame.target_x)'},
 '_object_impact_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, '
                                             'continuation: Long',
                                'returns': 'FirstDeploymentFrame',
                                'flow': 'if (target, continuation) not in ((267822, 267588), (266658, 267708), (241980, 267736), '
                                        '(266658, 267810), (243490, 267876), (243490, 267920), (243490, 267964), (32906, '
                                        '268064), (243490, 268110), (267982, 268132)):\n'
                                        "    raise ValueError('actual impact/projectile call/token pair required')\n"
                                        'memory.frame(frame)\n'
                                        'def child(actual_memory, entered):\n'
                                        '    scene = SceneRefreshMemory(actual_memory.state)\n'
                                        '    if target == 267822:\n'
                                        '        return calculate_object_impact_damage_fields(scene, entered)\n'
                                        '    if target == 267982:\n'
                                        '        return adjust_damage_for_object_guard_fields(scene, entered)\n'
                                        '    if target == 266658:\n'
                                        '        return offset_scene_object_position_fields(scene, entered)\n'
                                        '    if target == 241980:\n'
                                        '        return _append_object_sprite_fields(scene, entered)\n'
                                        '    if target == 243490:\n'
                                        '        return sample_random_preserving_seed_fields(scene, entered)\n'
                                        '    if target == 32906:\n'
                                        '        return enqueue_sound_command_fields(scene, entered)\n'
                                        '    raise SceneRefreshBoundary(target, entered, continuation)\n'
                                        'return _presentation_call_fields(BattlePresentationMemory(memory.state), frame, '
                                        'continuation, child)'},
 '_object_impact_restore_long_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, name: str',
                                        'returns': 'FirstDeploymentFrame',
                                        'flow': 'if frame.stack_cursor is None:\n'
                                                '    raise SceneRefreshBoundary(267822, frame, None)\n'
                                                'memory.sync_status(frame)\n'
                                                'value = frame.stack_cursor.long()\n'
                                                'return first_replace(frame, **{name: value}, '
                                                'stack_cursor=frame.stack_cursor.advance(4))'},
 '_object_impact_timer_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, address: Long',
                                 'returns': 'FirstDeploymentFrame',
                                 'flow': 'frame = _object_adjust_word_fields(memory, frame, address, 1)\n'
                                         "frame = _first_word(frame, 'target_x', memory.state.read(address, 2))\n"
                                         "frame = _first_long(frame, 'target_y', 16)\n"
                                         'memory.sync_status(frame)\n'
                                         'option = memory.state.read(4294935562, 2)\n'
                                         'frame = _scene_refresh_flags(memory, frame, option, 2)\n'
                                         'if option != 0:\n'
                                         "    frame = _first_long(frame, 'target_y', 16)\n"
                                         'return _scene_render_compare(memory, frame, low16(frame.target_x), '
                                         'low16(frame.target_y), 16)'},
 '_object_projectile_motion_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': "frame = _first_long(frame, 'target_x', 4)\n"
                                              'memory.sync_status(frame)\n'
                                              'option = memory.state.read(4294935562, 2)\n'
                                              'frame = _scene_refresh_flags(memory, frame, option, 2)\n'
                                              'if option != 0:\n'
                                              "    frame = _first_long(frame, 'target_x', 8)\n"
                                              'memory.sync_status(frame)\n'
                                              'direction = frame.auxiliary.word(0, 8)\n'
                                              'frame = _scene_refresh_flags(memory, frame, direction, 2)\n'
                                              'if direction == 0:\n'
                                              '    frame = _object_adjust_word_fields(memory, frame, 4294934884, '
                                              'low16(frame.target_x))\n'
                                              'else:\n'
                                              '    for expected, address, subtract in ((1, 4294934884, True), (2, 4294934886, '
                                              'False), (3, 4294934886, True)):\n'
                                              '        memory.sync_status(frame)\n'
                                              '        direction = frame.auxiliary.word(0, 8)\n'
                                              '        frame = _scene_render_compare(memory, frame, direction, expected, 16)\n'
                                              '        if direction == expected:\n'
                                              '            frame = _object_adjust_word_fields(memory, frame, address, '
                                              'low16(frame.target_x), subtract)\n'
                                              '            break\n'
                                              'memory.sync_status(frame)\n'
                                              "frame = _first_word(frame, 'target_x', frame.auxiliary.word(0, 8))\n"
                                              "frame = _scene_render_asl_word(memory, frame, 'target_x', low16(frame.target_x), "
                                              '2)\n'
                                              'memory.sync_status(frame)\n'
                                              'source = memory.state.read(u32(268238 + s16(low16(frame.target_x))), 4)\n'
                                              'frame = first_replace(frame, roster=memory.cursor_at(source))\n'
                                              "frame = _first_word(frame, 'target_x', memory.state.read(4294934884, 2))\n"
                                              'memory.sync_status(frame)\n'
                                              "frame = _first_word(frame, 'target_y', memory.state.read(4294934886, 2))\n"
                                              "frame = _first_word(frame, 'unit', 4)\n"
                                              "frame = _first_long(frame, 'count', 0)\n"
                                              "frame = _first_word(frame, 'distance', 768)\n"
                                              'return _append_object_sprite_fields(memory, frame)'},
 '_object_weighted_damage_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, factor: Word, '
                                                 'continuation: Long',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'sites = ((120, 267876, 267864, 267890), (80, 267920, 267908, 267934), (60, 267964, '
                                            '267952, 267978), (80, 268110, 268098, 268124))\n'
                                            'selected = None\n'
                                            'for item in sites:\n'
                                            '    if item[:2] == (factor, continuation):\n'
                                            '        selected = item\n'
                                            '        break\n'
                                            'if selected is None:\n'
                                            "    raise ValueError('actual weighted-damage arm and RNG continuation required')\n"
                                            'memory.frame(frame)\n'
                                            'memory.sync_status(frame)\n'
                                            "frame = _first_word(frame, 'target_x', frame.auxiliary.word(0, 14))\n"
                                            'memory.sync_status(frame)\n'
                                            "frame = _first_word(frame, 'target_y', frame.auxiliary.word(0, 12))\n"
                                            "frame = _first_long(frame, 'target_y', low16(frame.target_y) * "
                                            'low16(frame.target_x))\n'
                                            "frame = _movement_divu_word(memory.state, frame, 'target_y', 100, selected[2])\n"
                                            'memory.sync_status(frame)\n'
                                            'frame = _scene_render_push_longs(memory, frame, (frame.target_y,))\n'
                                            'frame = _object_impact_call_fields(memory, frame, 243490, continuation)\n'
                                            "frame = _first_word(frame, 'target_x', low16(frame.target_x) & 31)\n"
                                            "frame = _scene_render_arithmetic(memory, frame, 'target_x', low16(frame.target_x), "
                                            'factor, 16)\n'
                                            "frame = _object_impact_restore_long_fields(memory, frame, 'target_y')\n"
                                            "frame = _first_long(frame, 'target_y', low16(frame.target_y) * "
                                            'low16(frame.target_x))\n'
                                            "frame = _movement_divu_word(memory.state, frame, 'target_y', 100, selected[3])\n"
                                            'return memory.sync_status(frame)'},
 '_weighted_damage': {'signature': 'state, actor, frame, factor',
                      'returns': None,
                      'flow': 'actual = _object_action_legacy_fields(state, actor, actor, frame)\n'
                              'sites = ((60, 267964), (80, 267920), (120, 267876))\n'
                              'continuation = None\n'
                              'for base, token in sites:\n'
                              '    if base == factor:\n'
                              '        continuation = token\n'
                              '        break\n'
                              'if continuation is None:\n'
                              "    raise ValueError('actual legacy weighted-damage factor required')\n"
                              'actual = _object_weighted_damage_fields(SceneRefreshMemory(state), actual, factor, continuation)\n'
                              'return _object_action_legacy_result(state, actual).frame'},
 'adjust_damage_for_object_guard': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                                    'returns': 'ObjectActionResult',
                                    'flow': 'actual = adjust_damage_for_object_guard_fields(SceneRefreshMemory(state), '
                                            '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                            'return _object_action_legacy_result(state, actual)'},
 'adjust_damage_for_object_guard_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                           'returns': 'FirstDeploymentFrame',
                                           'flow': 'memory.frame(frame)\n'
                                                   'memory.sync_status(frame)\n'
                                                   'kind = frame.scratch.byte(0, 1)\n'
                                                   'frame = _scene_render_compare(memory, frame, kind, 3, 8)\n'
                                                   'if kind != 3:\n'
                                                   '    return memory.sync_status(frame)\n'
                                                   "frame = _first_word(frame, 'unit', memory.state.read(4294934788, 2))\n"
                                                   'memory.sync_status(frame)\n'
                                                   'side = memory.state.read(4294934860, 2)\n'
                                                   'frame = _scene_render_compare(memory, frame, side, 2, 16)\n'
                                                   'if side != 2:\n'
                                                   "    frame = _first_word(frame, 'unit', memory.state.read(4294934790, 2))\n"
                                                   "frame, divisor = _object_shift_word_right_fields(memory, frame, 'unit', "
                                                   'low16(frame.unit), 1)\n'
                                                   'if divisor == 0:\n'
                                                   '    divisor = 1\n'
                                                   "    frame = _first_word(frame, 'unit', divisor)\n"
                                                   "frame = _first_long(frame, 'target_y', frame.target_y & 65535)\n"
                                                   "frame = _movement_divu_word(memory.state, frame, 'target_y', divisor, "
                                                   '268020)\n'
                                                   'return memory.sync_status(frame)'},
 'advance_object_impact': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                           'returns': 'ObjectActionResult',
                           'flow': 'actual = advance_object_impact_fields(SceneRefreshMemory(state), '
                                   '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                   'return _object_action_legacy_result(state, actual)'},
 'advance_object_impact_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'memory.frame(frame)\n'
                                          'frame = _object_impact_timer_fields(memory, frame, 4294934882)\n'
                                          'if low16(frame.target_x) < low16(frame.target_y):\n'
                                          '    return _draw_object_impact_flash_fields(memory, frame)\n'
                                          'frame = first_replace(frame, scratch=memory.cursor_at(memory.state.read(4294934876, '
                                          '4)))\n'
                                          'frame = _object_impact_call_fields(memory, frame, 267822, 267588)\n'
                                          'return _apply_object_damage_fields(memory, frame)'},
 'advance_object_projectile': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                               'returns': 'ObjectActionResult',
                               'flow': 'actual = advance_object_projectile_fields(SceneRefreshMemory(state), '
                                       '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                       'return _object_action_legacy_result(state, actual)'},
 'advance_object_projectile_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                      'returns': 'FirstDeploymentFrame',
                                      'flow': 'memory.frame(frame)\n'
                                              'memory.sync_status(frame)\n'
                                              'frame = first_replace(frame, '
                                              'scratch=memory.cursor_at(memory.state.read(4294934876, 4)))\n'
                                              "frame = _first_word(frame, 'target_x', memory.state.read(4294934884, 2))\n"
                                              'memory.sync_status(frame)\n'
                                              'destination = frame.scratch.word(0, 2)\n'
                                              'frame = _scene_render_compare(memory, frame, low16(frame.target_x), destination, '
                                              '16)\n'
                                              'if low16(frame.target_x) != destination:\n'
                                              '    return _object_projectile_motion_fields(memory, frame)\n'
                                              "frame = _first_word(frame, 'target_x', memory.state.read(4294934886, 2))\n"
                                              'memory.sync_status(frame)\n'
                                              'destination = frame.scratch.word(0, 4)\n'
                                              'frame = _scene_render_compare(memory, frame, low16(frame.target_x), destination, '
                                              '16)\n'
                                              'if low16(frame.target_x) != destination:\n'
                                              '    return _object_projectile_motion_fields(memory, frame)\n'
                                              'timer = memory.state.read(4294934888, 2)\n'
                                              'frame = _scene_refresh_flags(memory, frame, timer, 2)\n'
                                              'if timer == 0:\n'
                                              "    frame = _first_word(frame, 'target_x', 170)\n"
                                              '    frame = _object_impact_call_fields(memory, frame, 32906, 268064)\n'
                                              'frame = _object_impact_timer_fields(memory, frame, 4294934888)\n'
                                              'if low16(frame.target_x) < low16(frame.target_y):\n'
                                              '    return _draw_object_impact_flash_fields(memory, frame, True)\n'
                                              'frame = _object_weighted_damage_fields(memory, frame, 80, 268110)\n'
                                              'frame = _object_impact_call_fields(memory, frame, 267982, 268132)\n'
                                              'return _apply_object_damage_fields(memory, frame)'},
 'calculate_object_impact_damage': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                                    'returns': 'ObjectActionResult',
                                    'flow': 'actual = calculate_object_impact_damage_fields(SceneRefreshMemory(state), '
                                            '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                            'return _object_action_legacy_result(state, actual)'},
 'calculate_object_impact_damage_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                           'returns': 'FirstDeploymentFrame',
                                           'flow': 'memory.frame(frame)\n'
                                                   'for kind, factor, continuation in ((0, 60, 267964), (1, 80, 267920), (2, '
                                                   '120, 267876)):\n'
                                                   '    memory.sync_status(frame)\n'
                                                   '    live_kind = frame.auxiliary.byte(0, 1)\n'
                                                   '    frame = _scene_render_compare(memory, frame, live_kind, kind, 8)\n'
                                                   '    if live_kind == kind:\n'
                                                   '        frame = _object_weighted_damage_fields(memory, frame, factor, '
                                                   'continuation)\n'
                                                   '        break\n'
                                                   'else:\n'
                                                   "    frame = _first_word(frame, 'target_y', frame.auxiliary.word(0, 12))\n"
                                                   'return adjust_damage_for_object_guard_fields(memory, frame)'},
 'dispatch_object_action_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'memory.frame(frame)\n'
                                           'for address, direction in ((265484, 0), (265488, 1), (265492, 2), (265496, 3)):\n'
                                           '    if target == address:\n'
                                           '        return start_object_motion_fields(memory, frame, direction)\n'
                                           'for address, direction in ((265550, 0), (265554, 1), (265558, 2), (265562, 3), '
                                           '(266120, 0), (266124, 1), (266128, 2), (266132, 3)):\n'
                                           '    if target == address:\n'
                                           '        return continue_object_motion_fields(memory, frame, direction)\n'
                                           'if target == 265504:\n'
                                           '    return pursue_opposing_object_fields(memory, frame)\n'
                                           'if target == 265508:\n'
                                           '    return sidestep_opposing_object_fields(memory, frame)\n'
                                           'if target == 265500:\n'
                                           '    return update_selected_object_action_fields(memory, frame, primary_middle=True)\n'
                                           'if target == 265566:\n'
                                           '    return _object_motion_finish_fields(memory, frame)\n'
                                           'if target in (265570, 265574, 265578):\n'
                                           '    return resume_object_pursuit_fields(memory, frame)\n'
                                           'if target == 265582:\n'
                                           '    return advance_object_impact_fields(memory, frame)\n'
                                           'if target == 265586:\n'
                                           '    return advance_object_projectile_fields(memory, frame)\n'
                                           'raise SceneRefreshBoundary(target, frame, None)'}})

# B37 sole AI/retreat fields; ordinary native lowering unchanged.
for _module,_names in {'contexts_actions': ['DuelGlyphContext',
                      'ObjectActionResult',
                      'ObjectGlyphResult',
                      'ObjectPositionOffset',
                      'ObjectRosterTotals',
                      'ObjectVectorContext',
                      'SceneRenderFrame',
                      'SpriteBatchContext',
                      'TileUploadResult',
                      'checked_action',
                      'checked_controller_frame'],
 'domain': ['Boundary',
            'Cursor',
            'Long',
            'SceneState',
            'StackContinuation',
            'Table',
            'Word',
            'checked_cursor',
            'checked_state',
            'checked_table',
            'descending_inclusive',
            'divu_retained',
            'low16',
            'low8',
            'negative_word',
            'ram_view',
            'replace_byte',
            'replace_word',
            's16',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'],
 'services': ['BattlePresentationMemory',
              'FirstDeploymentFrame',
              'SceneRefreshBoundary',
              'SceneRefreshMemory',
              '_append_object_sprite_fields',
              '_first_byte',
              '_first_long',
              '_first_word',
              '_movement_binary_flags',
              '_movement_divu_word',
              '_object_adjust_word_fields',
              '_object_clear_word_fields',
              '_object_shift_word_right_fields',
              '_presentation_call_fields',
              '_scene_controller_legacy_fields',
              '_scene_controller_legacy_projection',
              '_scene_refresh_decrement',
              '_scene_refresh_emit',
              '_scene_refresh_flags',
              '_scene_render_arithmetic',
              '_scene_render_asl_word',
              '_scene_render_bit',
              '_scene_render_compare',
              '_scene_render_push_longs',
              'append_scene_sprite_entries',
              'decode_glyph_rows_to_buffers',
              'enqueue_sound_command',
              'enqueue_sound_command_fields',
              'first_replace',
              'offset_scene_object_position',
              'offset_scene_object_position_fields',
              'plan_scene_object_action',
              'probe_opposing_object_overlap_fields',
              'probe_scene_object_overlap_fields',
              'probe_scene_object_overlap_with_frame',
              'read_object_action_mode',
              'read_object_action_mode_fields',
              'resume_selected_object_action',
              'sample_random_pair',
              'sample_random_preserving_seed_carrier',
              'sample_random_preserving_seed_fields',
              'update_selected_object_action_fields']}.items():
    APPROVED.setdefault(_module,set()).update(_names)
DECLARATIONS.update({'_masked_retreat_roll': {'signature': 'state, actor, opponent, frame, table',
                          'returns': None,
                          'flow': 'sites = ((270068, 269812), (270072, 269880), (270076, 269922), (270084, 270048))\n'
                                  'continuation = None\n'
                                  'for address, token in sites:\n'
                                  '    if table == address:\n'
                                  '        continuation = token\n'
                                  '        break\n'
                                  'if continuation is None:\n'
                                  "    raise ValueError('actual legacy retreat mask table required')\n"
                                  'actual = _object_retreat_roll_fields(SceneRefreshMemory(state), '
                                  '_object_action_legacy_fields(state, actor, opponent, frame), continuation, table)\n'
                                  'return _object_action_legacy_result(state, actual)'},
 '_object_ai_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: '
                                         'Long',
                            'returns': 'FirstDeploymentFrame',
                            'flow': 'if (target, continuation) not in ((269284, 269262), (269526, 269268), (270154, 269274), '
                                    '(269760, 269280), (269790, 269772), (269854, 269776), (269900, 269780), (269942, 269784), '
                                    '(270006, 269788), (270088, 269794), (243490, 269812), (270088, 269858), (243490, 269880), '
                                    '(270088, 269904), (243490, 269922), (270088, 269946), (243490, 269966), (270088, 270010), '
                                    '(243490, 270048), (270088, 270170), (267514, 270226), (267514, 270244), (267514, 270262), '
                                    '(267514, 270280), (243490, 270290)):\n'
                                    "    raise ValueError('actual AI/retreat call/token pair required')\n"
                                    'memory.frame(frame)\n'
                                    'def child(actual_memory, entered):\n'
                                    '    scene = SceneRefreshMemory(actual_memory.state)\n'
                                    '    for address, function in ((269284, dispatch_object_formation_ai_fields), (269526, '
                                    'dispatch_object_formation_fallback_fields), (270154, choose_object_retreat_phase_fields), '
                                    '(269760, advance_object_retreat_checks_fields), (269790, '
                                    'trigger_object_retreat_strength_fields), (269854, '
                                    'trigger_object_retreat_low_strength_fields), (269900, '
                                    'trigger_object_retreat_outnumbered_fields), (269942, trigger_object_retreat_morale_fields), '
                                    '(270006, trigger_object_retreat_quality_fields), (270088, sum_live_object_rosters_fields), '
                                    '(267514, probe_opposing_object_overlap_fields), (243490, '
                                    'sample_random_preserving_seed_fields)):\n'
                                    '        if target == address:\n'
                                    '            return function(scene, entered)\n'
                                    '    raise SceneRefreshBoundary(target, entered, continuation)\n'
                                    'return _presentation_call_fields(BattlePresentationMemory(memory.state), frame, '
                                    'continuation, child)'},
 '_object_retreat_roll_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, continuation: Long, '
                                              'table: Long | None',
                                 'returns': 'FirstDeploymentFrame',
                                 'flow': 'sites = ((269812, 270068), (269880, 270072), (269922, 270076), (269966, None), '
                                         '(270048, 270084))\n'
                                         'if (continuation, table) not in sites:\n'
                                         "    raise ValueError('actual retreat RNG arm required')\n"
                                         'frame = _object_ai_call_fields(memory, frame, 243490, continuation)\n'
                                         "frame = _first_word(frame, 'target_y', memory.state.read(4294963154, 2))\n"
                                         'if table is not None:\n'
                                         '    frame = first_replace(frame, roster=memory.cursor_at(table))\n'
                                         '    memory.sync_status(frame)\n'
                                         '    mask = frame.roster.byte(low16(frame.target_y))\n'
                                         "    frame = _first_byte(frame, 'target_x', low8(frame.target_x) & mask)\n"
                                         'return memory.sync_status(frame)'},
 '_roster_frame': {'signature': 'state, actor, opponent, frame',
                   'returns': None,
                   'flow': 'actual = sum_live_object_rosters_fields(SceneRefreshMemory(state), '
                           '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                           'return _object_action_legacy_result(state, actual)'},
 '_set_all_object_retreat_modes': {'signature': 'state',
                                   'returns': None,
                                   'flow': '_set_all_object_retreat_modes_fields(SceneRefreshMemory(state), '
                                           'FirstDeploymentFrame.unobserved())'},
 '_set_all_object_retreat_modes_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'for address in (4294934826, 4294934828, 4294934830, 4294934832):\n'
                                                  '    frame = _scene_refresh_emit(memory, frame, address, 2, 6)\n'
                                                  'return frame'},
 'advance_object_retreat_checks': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                                   'returns': 'ObjectActionResult',
                                   'flow': 'actual = advance_object_retreat_checks_fields(SceneRefreshMemory(state), '
                                           '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                           'return _object_action_legacy_result(state, actual)'},
 'advance_object_retreat_checks_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'memory.frame(frame)\n'
                                                  'memory.sync_status(frame)\n'
                                                  'elapsed = memory.state.read(4294934880, 2)\n'
                                                  'frame = _scene_render_compare(memory, frame, elapsed, 11, 16)\n'
                                                  'if elapsed < 11:\n'
                                                  '    return memory.sync_status(frame)\n'
                                                  'for target, continuation in ((269790, 269772), (269854, 269776), (269900, '
                                                  '269780), (269942, 269784), (270006, 269788)):\n'
                                                  '    frame = _object_ai_call_fields(memory, frame, target, continuation)\n'
                                                  'return memory.sync_status(frame)'},
 'choose_object_retreat_phase': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                                 'returns': 'ObjectActionResult',
                                 'flow': 'actual = choose_object_retreat_phase_fields(SceneRefreshMemory(state), '
                                         '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                         'return _object_action_legacy_result(state, actual)'},
 'choose_object_retreat_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                        'returns': 'FirstDeploymentFrame',
                                        'flow': 'memory.frame(frame)\n'
                                                'memory.sync_status(frame)\n'
                                                "frame = _first_word(frame, 'target_x', memory.state.read(4294934748, 2))\n"
                                                'memory.sync_status(frame)\n'
                                                'opponent_morale = memory.state.read(4294934752, 2)\n'
                                                'frame = _scene_render_compare(memory, frame, low16(frame.target_x), '
                                                'opponent_morale, 16)\n'
                                                'if low16(frame.target_x) == opponent_morale:\n'
                                                '    return memory.sync_status(frame)\n'
                                                'frame = _object_ai_call_fields(memory, frame, 270088, 270170)\n'
                                                'frame = _scene_render_compare(memory, frame, low16(frame.unit), '
                                                'low16(frame.target_y), 16)\n'
                                                'if low16(frame.unit) <= low16(frame.target_y):\n'
                                                '    return memory.sync_status(frame)\n'
                                                "frame = _first_word(frame, 'target_x', memory.state.read(4294963154, 2))\n"
                                                'frame = first_replace(frame, roster=memory.cursor_at(270316))\n'
                                                'memory.sync_status(frame)\n'
                                                "frame = _first_word(frame, 'target_y', memory.state.read(4294934904, 2))\n"
                                                'memory.sync_status(frame)\n'
                                                'threshold = frame.roster.byte(low16(frame.target_x))\n'
                                                'frame = _scene_render_compare(memory, frame, low8(frame.target_y), threshold, '
                                                '8)\n'
                                                'if low8(frame.target_y) >= threshold:\n'
                                                '    return memory.sync_status(frame)\n'
                                                "frame = _first_word(frame, 'target_x', memory.state.read(4294934904, 2))\n"
                                                'memory.sync_status(frame)\n'
                                                'opponent_morale = memory.state.read(4294935160, 2)\n'
                                                'frame = _scene_render_compare(memory, frame, low16(frame.target_x), '
                                                'opponent_morale, 16)\n'
                                                'if low16(frame.target_x) >= opponent_morale:\n'
                                                '    return memory.sync_status(frame)\n'
                                                'frame = first_replace(frame, auxiliary=memory.cursor_at(4294934890))\n'
                                                'for horizontal, vertical, continuation in ((32784, 0, 270226), (16, 0, 270244), '
                                                '(32784, 32784, 270262), (16, 32784, 270280)):\n'
                                                "    frame = _first_word(frame, 'target_x', horizontal)\n"
                                                "    frame = _first_word(frame, 'target_y', vertical)\n"
                                                '    frame = _object_ai_call_fields(memory, frame, 267514, continuation)\n'
                                                '    frame = _scene_refresh_flags(memory, frame, low16(frame.target_x), 2)\n'
                                                '    if low16(frame.target_x):\n'
                                                '        break\n'
                                                'else:\n'
                                                '    return memory.sync_status(frame)\n'
                                                'frame = _object_ai_call_fields(memory, frame, 243490, 270290)\n'
                                                "frame = _first_word(frame, 'target_x', low16(frame.target_x) & 3)\n"
                                                'if low16(frame.target_x):\n'
                                                '    frame = _scene_refresh_emit(memory, frame, 4294934842, 2, 6)\n'
                                                '    frame = _scene_refresh_emit(memory, frame, 4294934844, 2, 0)\n'
                                                '    frame = _scene_refresh_emit(memory, frame, 4294934846, 2, 1)\n'
                                                'return memory.sync_status(frame)'},
 'dispatch_object_formation_ai': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                                  'returns': 'ObjectActionResult',
                                  'flow': 'actual = dispatch_object_formation_ai_fields(SceneRefreshMemory(state), '
                                          '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                          'return _object_action_legacy_result(state, actual)'},
 'dispatch_object_formation_ai_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                         'returns': 'FirstDeploymentFrame',
                                         'flow': 'memory.frame(frame)\n'
                                                 'memory.sync_status(frame)\n'
                                                 "frame = _first_word(frame, 'target_x', memory.state.read(4294934858, 2))\n"
                                                 "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                                 'low16(frame.target_x), 2)\n'
                                                 'target = u32(269294 + s16(low16(frame.target_x)))\n'
                                                 'raise SceneRefreshBoundary(target, memory.sync_status(frame), None)'},
 'dispatch_object_formation_fallback': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                                        'returns': 'ObjectActionResult',
                                        'flow': 'actual = dispatch_object_formation_fallback_fields(SceneRefreshMemory(state), '
                                                '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                                'return _object_action_legacy_result(state, actual)'},
 'dispatch_object_formation_fallback_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                               'returns': 'FirstDeploymentFrame',
                                               'flow': 'memory.frame(frame)\n'
                                                       'memory.sync_status(frame)\n'
                                                       'mode = memory.state.read(4294934832, 2)\n'
                                                       'frame = _scene_render_compare(memory, frame, mode, 6, 16)\n'
                                                       'if mode == 6:\n'
                                                       '    return memory.sync_status(frame)\n'
                                                       "frame = _first_word(frame, 'target_x', memory.state.read(4294934858, "
                                                       '2))\n'
                                                       "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                                       'low16(frame.target_x), 2)\n'
                                                       'target = u32(269546 + s16(low16(frame.target_x)))\n'
                                                       'raise SceneRefreshBoundary(target, memory.sync_status(frame), None)'},
 'sum_live_object_rosters': {'signature': 'state: SceneState, retained_command: Long | None=None',
                             'returns': 'ObjectRosterTotals',
                             'flow': 'memory = SceneRefreshMemory(state)\n'
                                     'actual = FirstDeploymentFrame.unobserved()\n'
                                     'if retained_command is None:\n'
                                     '    raise SceneRefreshBoundary(270088, actual, None)\n'
                                     'uint(retained_command, 32)\n'
                                     'actual = first_replace(actual, target_x=retained_command)\n'
                                     'actual = sum_live_object_rosters_fields(memory, actual)\n'
                                     'return ObjectRosterTotals(actual.target_y, actual.unit, actual.count, actual.distance, '
                                     'actual.target_x, actual.auxiliary)'},
 'sum_live_object_rosters_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'memory.frame(frame)\n'
                                            "for base, total_name, count_name in ((4294934906, 'target_y', 'count'), "
                                            "(4294935162, 'unit', 'distance')):\n"
                                            '    frame = _first_long(frame, total_name, 0)\n'
                                            '    frame = _first_long(frame, count_name, 0)\n'
                                            "    frame = _first_word(frame, 'target_x', 14)\n"
                                            '    frame = first_replace(frame, auxiliary=memory.cursor_at(base))\n'
                                            '    counter = 14\n'
                                            '    while True:\n'
                                            '        memory.sync_status(frame)\n'
                                            '        active = frame.auxiliary.byte()\n'
                                            '        frame = _scene_render_bit(memory, frame, active, 128)\n'
                                            '        if active & 128:\n'
                                            '            memory.sync_status(frame)\n'
                                            '            amount = frame.auxiliary.word(0, 14)\n'
                                            '            frame = _scene_render_arithmetic(memory, frame, total_name, '
                                            'low16(frame.carrier(total_name)), amount, 16)\n'
                                            '            frame = _scene_render_arithmetic(memory, frame, count_name, '
                                            'low16(frame.carrier(count_name)), 1, 16)\n'
                                            '        frame = first_replace(frame, auxiliary=frame.auxiliary.advance(16))\n'
                                            "        frame = _scene_refresh_decrement(frame, 'target_x', counter)\n"
                                            '        counter = u16(counter - 1)\n'
                                            '        if counter == 65535:\n'
                                            '            break\n'
                                            'return memory.sync_status(frame)'},
 'trigger_object_retreat_check_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, kind: Word',
                                         'returns': 'FirstDeploymentFrame',
                                         'flow': 'if kind not in (0, 1, 2, 3, 4):\n'
                                                 "    raise ValueError('actual retreat criterion required')\n"
                                                 'memory.frame(frame)\n'
                                                 'continuation = (269794, 269858, 269904, 269946, 270010)[kind]\n'
                                                 'frame = _object_ai_call_fields(memory, frame, 270088, continuation)\n'
                                                 'if kind in (0, 1):\n'
                                                 "    frame = _first_word(frame, 'count', low16(frame.target_y))\n"
                                                 "    frame = _scene_render_asl_word(memory, frame, 'count', low16(frame.count), "
                                                 '1)\n'
                                                 '    frame = _scene_render_compare(memory, frame, low16(frame.unit), '
                                                 'low16(frame.count), 16)\n'
                                                 '    if low16(frame.unit) <= low16(frame.count):\n'
                                                 '        return memory.sync_status(frame)\n'
                                                 '    limit = 1000 if kind == 0 else 500\n'
                                                 '    frame = _scene_render_compare(memory, frame, low16(frame.target_y), limit, '
                                                 '16)\n'
                                                 '    if low16(frame.target_y) > limit:\n'
                                                 '        return memory.sync_status(frame)\n'
                                                 '    frame = _object_retreat_roll_fields(memory, frame, 269812 if kind == 0 '
                                                 'else 269880, 270068 if kind == 0 else 270072)\n'
                                                 '    if low8(frame.target_x) == 0:\n'
                                                 '        return _set_all_object_retreat_modes_fields(memory, frame)\n'
                                                 '    return memory.sync_status(frame)\n'
                                                 'if kind == 2:\n'
                                                 "    frame = _scene_render_asl_word(memory, frame, 'count', low16(frame.count), "
                                                 '1)\n'
                                                 '    frame = _scene_render_compare(memory, frame, low16(frame.distance), '
                                                 'low16(frame.count), 16)\n'
                                                 '    if low16(frame.distance) <= low16(frame.count):\n'
                                                 '        return memory.sync_status(frame)\n'
                                                 '    frame = _scene_render_compare(memory, frame, low16(frame.unit), '
                                                 'low16(frame.target_y), 16)\n'
                                                 '    if low16(frame.unit) <= low16(frame.target_y):\n'
                                                 '        return memory.sync_status(frame)\n'
                                                 '    frame = _object_retreat_roll_fields(memory, frame, 269922, 270076)\n'
                                                 '    if low8(frame.target_x) == 0:\n'
                                                 '        return _set_all_object_retreat_modes_fields(memory, frame)\n'
                                                 '    return memory.sync_status(frame)\n'
                                                 'if kind == 3:\n'
                                                 '    frame = _scene_render_compare(memory, frame, low16(frame.unit), '
                                                 'low16(frame.target_y), 16)\n'
                                                 '    if low16(frame.unit) <= low16(frame.target_y):\n'
                                                 '        return memory.sync_status(frame)\n'
                                                 '    morale = memory.state.read(4294934904, 2)\n'
                                                 '    frame = _scene_render_compare(memory, frame, morale, 30, 16)\n'
                                                 '    if morale >= 30:\n'
                                                 '        return memory.sync_status(frame)\n'
                                                 '    frame = _object_retreat_roll_fields(memory, frame, 269966, None)\n'
                                                 '    frame = _scene_render_compare(memory, frame, low16(frame.target_y), 2, '
                                                 '16)\n'
                                                 '    if low16(frame.target_y) == 2:\n'
                                                 "        frame = _first_word(frame, 'target_x', low16(frame.target_x) & 7)\n"
                                                 '        frame = _scene_render_compare(memory, frame, low16(frame.target_x), 5, '
                                                 '16)\n'
                                                 '        retreat = low16(frame.target_x) < 5\n'
                                                 '    else:\n'
                                                 '        frame = first_replace(frame, roster=memory.cursor_at(270080))\n'
                                                 '        memory.sync_status(frame)\n'
                                                 '        mask = frame.roster.byte(low16(frame.target_y))\n'
                                                 "        frame = _first_byte(frame, 'target_x', low8(frame.target_x) & mask)\n"
                                                 '        retreat = low8(frame.target_x) == 0\n'
                                                 '    if retreat:\n'
                                                 '        return _set_all_object_retreat_modes_fields(memory, frame)\n'
                                                 '    return memory.sync_status(frame)\n'
                                                 "frame = _first_word(frame, 'target_x', memory.state.read(4294934788, 2))\n"
                                                 'memory.sync_status(frame)\n'
                                                 'quality = memory.state.read(4294934790, 2)\n'
                                                 'frame = _scene_render_compare(memory, frame, low16(frame.target_x), quality, '
                                                 '16)\n'
                                                 'if low16(frame.target_x) >= quality:\n'
                                                 '    return memory.sync_status(frame)\n'
                                                 "frame = _first_word(frame, 'target_x', memory.state.read(4294934904, 2))\n"
                                                 'memory.sync_status(frame)\n'
                                                 'opposing_morale = memory.state.read(4294935160, 2)\n'
                                                 'frame = _scene_render_compare(memory, frame, low16(frame.target_x), '
                                                 'opposing_morale, 16)\n'
                                                 'if low16(frame.target_x) >= opposing_morale:\n'
                                                 '    return memory.sync_status(frame)\n'
                                                 'morale = memory.state.read(4294934904, 2)\n'
                                                 'frame = _scene_render_compare(memory, frame, morale, 30, 16)\n'
                                                 'if morale >= 30:\n'
                                                 '    return memory.sync_status(frame)\n'
                                                 'frame = _object_retreat_roll_fields(memory, frame, 270048, 270084)\n'
                                                 'if low8(frame.target_x) == 0:\n'
                                                 '    return _set_all_object_retreat_modes_fields(memory, frame)\n'
                                                 'return memory.sync_status(frame)'},
 'trigger_object_retreat_low_strength': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                                         'returns': 'ObjectActionResult',
                                         'flow': 'actual = trigger_object_retreat_low_strength_fields(SceneRefreshMemory(state), '
                                                 '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                                 'return _object_action_legacy_result(state, actual)'},
 'trigger_object_retreat_low_strength_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                                'returns': 'FirstDeploymentFrame',
                                                'flow': 'return trigger_object_retreat_check_fields(memory, frame, 1)'},
 'trigger_object_retreat_morale': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                                   'returns': 'ObjectActionResult',
                                   'flow': 'actual = trigger_object_retreat_morale_fields(SceneRefreshMemory(state), '
                                           '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                           'return _object_action_legacy_result(state, actual)'},
 'trigger_object_retreat_morale_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'return trigger_object_retreat_check_fields(memory, frame, 3)'},
 'trigger_object_retreat_outnumbered': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                                        'returns': 'ObjectActionResult',
                                        'flow': 'actual = trigger_object_retreat_outnumbered_fields(SceneRefreshMemory(state), '
                                                '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                                'return _object_action_legacy_result(state, actual)'},
 'trigger_object_retreat_outnumbered_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                               'returns': 'FirstDeploymentFrame',
                                               'flow': 'return trigger_object_retreat_check_fields(memory, frame, 2)'},
 'trigger_object_retreat_quality': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                                    'returns': 'ObjectActionResult',
                                    'flow': 'actual = trigger_object_retreat_quality_fields(SceneRefreshMemory(state), '
                                            '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                            'return _object_action_legacy_result(state, actual)'},
 'trigger_object_retreat_quality_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                           'returns': 'FirstDeploymentFrame',
                                           'flow': 'return trigger_object_retreat_check_fields(memory, frame, 4)'},
 'trigger_object_retreat_strength': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                                     'returns': 'ObjectActionResult',
                                     'flow': 'actual = trigger_object_retreat_strength_fields(SceneRefreshMemory(state), '
                                             '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                             'return _object_action_legacy_result(state, actual)'},
 'trigger_object_retreat_strength_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                            'returns': 'FirstDeploymentFrame',
                                            'flow': 'return trigger_object_retreat_check_fields(memory, frame, 0)'},
 'update_object_action_ai': {'signature': 'state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame',
                             'returns': 'ObjectActionResult',
                             'flow': 'actual = update_object_action_ai_fields(SceneRefreshMemory(state), '
                                     '_object_action_legacy_fields(state, actor, opponent, frame))\n'
                                     'return _object_action_legacy_result(state, actual)'},
 'update_object_action_ai_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'memory.frame(frame)\n'
                                            'for expected in (1, 2):\n'
                                            '    memory.sync_status(frame)\n'
                                            '    mode = memory.state.read(4294934746, 1)\n'
                                            '    frame = _scene_render_compare(memory, frame, mode, expected, 8)\n'
                                            '    if mode == expected:\n'
                                            '        return memory.sync_status(frame)\n'
                                            'mode = memory.state.read(4294934860, 1)\n'
                                            'frame = _scene_refresh_flags(memory, frame, mode, 1)\n'
                                            'if mode != 0:\n'
                                            '    return memory.sync_status(frame)\n'
                                            'mode = memory.state.read(4294934826, 2)\n'
                                            'frame = _scene_render_compare(memory, frame, mode, 6, 16)\n'
                                            'if mode == 6:\n'
                                            '    return memory.sync_status(frame)\n'
                                            'for target, continuation in ((269284, 269262), (269526, 269268), (270154, 269274), '
                                            '(269760, 269280)):\n'
                                            '    frame = _object_ai_call_fields(memory, frame, target, continuation)\n'
                                            'return memory.sync_status(frame)'}})

# B38 sole Main formation fields and genuine Dynamic JMP routes; native lowerers unchanged.
for _module,_names in {'contexts_actions': ['DuelGlyphContext',
                      'ObjectActionResult',
                      'ObjectGlyphResult',
                      'ObjectPositionOffset',
                      'ObjectRosterTotals',
                      'ObjectVectorContext',
                      'SceneRenderFrame',
                      'SpriteBatchContext',
                      'TileUploadResult',
                      'checked_action',
                      'checked_controller_frame'],
 'domain': ['Boundary',
            'Cursor',
            'Long',
            'SceneState',
            'StackContinuation',
            'Table',
            'Word',
            'checked_cursor',
            'checked_state',
            'checked_table',
            'descending_inclusive',
            'divu_retained',
            'low16',
            'low8',
            'negative_word',
            'ram_view',
            'replace_byte',
            'replace_word',
            's16',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'],
 'services': ['BattlePresentationMemory',
              'FirstDeploymentFrame',
              'SceneRefreshBoundary',
              'SceneRefreshMemory',
              '_append_object_sprite_fields',
              '_first_byte',
              '_first_long',
              '_first_word',
              '_movement_binary_flags',
              '_movement_divu_word',
              '_object_adjust_word_fields',
              '_object_clear_word_fields',
              '_object_shift_word_right_fields',
              '_presentation_call_fields',
              '_scene_controller_legacy_fields',
              '_scene_controller_legacy_projection',
              '_scene_refresh_decrement',
              '_scene_refresh_emit',
              '_scene_refresh_flags',
              '_scene_render_arithmetic',
              '_scene_render_asl_word',
              '_scene_render_bit',
              '_scene_render_compare',
              '_scene_render_push_longs',
              'append_scene_sprite_entries',
              'choose_object_formation_leader_fields',
              'decode_glyph_rows_to_buffers',
              'enqueue_sound_command',
              'enqueue_sound_command_fields',
              'first_replace',
              'offset_scene_object_position',
              'offset_scene_object_position_fields',
              'plan_scene_object_action',
              'probe_opposing_object_overlap_fields',
              'probe_scene_object_overlap_fields',
              'probe_scene_object_overlap_with_frame',
              'read_object_action_mode',
              'read_object_action_mode_fields',
              'resume_selected_object_action',
              'sample_random_pair',
              'sample_random_preserving_seed_carrier',
              'sample_random_preserving_seed_fields',
              'set_object_formation_orders_fields',
              'update_selected_object_action_fields']}.items():
    APPROVED.setdefault(_module,set()).update(_names)
DECLARATIONS.update({'dispatch_object_formation_ai_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                         'returns': 'FirstDeploymentFrame',
                                         'flow': 'memory.frame(frame)\n'
                                                 'memory.sync_status(frame)\n'
                                                 "frame = _first_word(frame, 'target_x', memory.state.read(4294934858, 2))\n"
                                                 "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                                 'low16(frame.target_x), 2)\n'
                                                 'target = u32(269294 + s16(low16(frame.target_x)))\n'
                                                 'for address, kind in ((269294, 0), (269298, 1), (269302, 2), (269306, 3), '
                                                 '(269310, 4)):\n'
                                                 '    if target == address:\n'
                                                 '        return set_object_formation_orders_fields(memory, frame, kind)\n'
                                                 'raise SceneRefreshBoundary(target, memory.sync_status(frame), None)'},
 'dispatch_object_formation_fallback_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                               'returns': 'FirstDeploymentFrame',
                                               'flow': 'memory.frame(frame)\n'
                                                       'memory.sync_status(frame)\n'
                                                       'mode = memory.state.read(4294934832, 2)\n'
                                                       'frame = _scene_render_compare(memory, frame, mode, 6, 16)\n'
                                                       'if mode == 6:\n'
                                                       '    return memory.sync_status(frame)\n'
                                                       "frame = _first_word(frame, 'target_x', memory.state.read(4294934858, "
                                                       '2))\n'
                                                       "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                                       'low16(frame.target_x), 2)\n'
                                                       'target = u32(269546 + s16(low16(frame.target_x)))\n'
                                                       'for address, kind in ((269546, 0), (269550, 1), (269554, 2), (269558, '
                                                       '0), (269562, 3)):\n'
                                                       '    if target == address:\n'
                                                       '        return choose_object_formation_leader_fields(memory, frame, '
                                                       'kind)\n'
                                                       'raise SceneRefreshBoundary(target, memory.sync_status(frame), None)'}})


# C59 exact complete fields, compatibility projections and current closed dispatch.
DECLARATIONS.update({'_portrait_banked_strip_frame_fields': {'flow': 'from '
                                                 '..high_level_main_flows.business_movement_support '
                                                 'import _movement_compare, _movement_add_word\n'
                                                 'if type(second) is not bool:\n'
                                                 "    raise ValueError('actual first/second portrait "
                                                 "strip required')\n"
                                                 'while True:\n'
                                                 '    frame = display_address_fields(state, frame, '
                                                 "'candidates', 746650)\n"
                                                 '    tile = frame.roster.word()\n'
                                                 '    frame = first_replace(frame, '
                                                 'roster=frame.roster.advance(2))\n'
                                                 '    frame = display_move_fields(state, frame, '
                                                 "'count', tile)\n"
                                                 '    frame = _movement_compare(state, frame, '
                                                 'low16(frame.count), 2048, 16)\n'
                                                 '    if not frame.status & 1:\n'
                                                 '        frame = first_replace(frame, '
                                                 'candidates=frame.candidates.advance(65536))\n'
                                                 '    frame = display_shift_word_fields(state, frame, '
                                                 "'count', 5)\n"
                                                 '    frame = display_move_fields(state, frame, '
                                                 "'distance', 7)\n"
                                                 '    while True:\n'
                                                 '        pixels = state.read(u32(frame.candidates.base '
                                                 '+ s16(low16(frame.count))), 4)\n'
                                                 '        frame = display_store_fields(state, frame, '
                                                 '418408 if second else 418346, 12582912, pixels, 4)\n'
                                                 '        frame = _movement_add_word(state, frame, '
                                                 "'count', 4)\n"
                                                 '        frame, more = display_loop_fields(frame, '
                                                 "'distance')\n"
                                                 '        if not more:\n'
                                                 '            break\n'
                                                 "    frame, more = display_loop_fields(frame, 'unit')\n"
                                                 '    if not more:\n'
                                                 '        return frame',
                                         'returns': 'FirstDeploymentFrame',
                                         'signature': 'state: SceneState, frame: FirstDeploymentFrame, '
                                                      'second: bool'},
 '_upload_banked_tile_strip': {'flow': 'from ..high_level_main_flows.contexts_display_fields import '
                                       'display_legacy_frame_fields\n'
                                       'return display_legacy_frame_fields(state, None, 418318)',
                               'returns': '',
                               'signature': 'state, source, frame, count'},
 'upload_object_officer_name': {'flow': 'from ..high_level_main_flows.contexts_display_fields import '
                                        'display_legacy_frame_fields\n'
                                        'entered = display_legacy_frame_fields(state, officer, 262850)\n'
                                        'return upload_object_officer_name_frame_fields(state, entered)',
                                'returns': 'ObjectGlyphResult',
                                'signature': 'state: SceneState, officer: Long, glyphs: '
                                             'DuelGlyphContext'},
 'upload_object_officer_name_frame_fields': {'flow': 'from '
                                                     '..high_level_main_flows.business_movement_support '
                                                     'import _movement_multiply_word, '
                                                     '_movement_compare\n'
                                                     'frame = display_frame_fields(state, frame)\n'
                                                     'frame = _movement_multiply_word(state, frame, '
                                                     "'choice', 6)\n"
                                                     'frame = display_address_fields(state, frame, '
                                                     "'roster', 566532)\n"
                                                     'frame = first_replace(frame, '
                                                     'roster=frame.roster.advance(s16(low16(frame.choice))))\n'
                                                     'frame = display_move_fields(state, frame, '
                                                     "'count', 2)\n"
                                                     'frame = _movement_compare(state, frame, '
                                                     'frame.roster.word(4), 63, 16)\n'
                                                     'if frame.status & 4:\n'
                                                     '    frame = display_move_fields(state, frame, '
                                                     "'count', 1)\n"
                                                     '    frame = display_move_fields(state, frame, '
                                                     "'distance', low16(frame.target_x))\n"
                                                     '    frame = '
                                                     '_scene_render_asl_word(SceneRefreshMemory(state), '
                                                     "frame, 'distance', low16(frame.distance), 4)\n"
                                                     '    frame = display_move_fields(state, frame, '
                                                     "'distance', low16(frame.distance) | "
                                                     'low16(frame.target_x))\n'
                                                     '    frame = display_move_fields(state, frame, '
                                                     "'offset_x', 63)\n"
                                                     '    frame = display_address_fields(state, frame, '
                                                     "'candidates', 4294955776)\n"
                                                     '    frame = display_address_fields(state, frame, '
                                                     "'controller', 4294956096)\n"
                                                     '    while True:\n'
                                                     '        frame = display_store_fields(state, '
                                                     'frame, 262898, frame.candidates.base, '
                                                     'low8(frame.distance), 1)\n'
                                                     '        frame = first_replace(frame, '
                                                     'candidates=frame.candidates.advance(1))\n'
                                                     '        frame = display_store_fields(state, '
                                                     'frame, 262900, frame.controller.base, '
                                                     'low8(frame.distance), 1)\n'
                                                     '        frame = first_replace(frame, '
                                                     'controller=frame.controller.advance(1))\n'
                                                     '        frame, more = display_loop_fields(frame, '
                                                     "'offset_x')\n"
                                                     '        if not more:\n'
                                                     '            break\n'
                                                     'else:\n'
                                                     '    frame = display_address_fields(state, frame, '
                                                     "'candidates', 4294955776)\n"
                                                     'frame = display_call_fields(state, frame, 44682, '
                                                     '262918)\n'
                                                     'frame = display_address_fields(state, frame, '
                                                     "'roster', 4294955776)\n"
                                                     'frame = display_address_fields(state, frame, '
                                                     "'auxiliary', 12582912)\n"
                                                     'frame = display_move_fields(state, frame, '
                                                     "'target_x', 95)\n"
                                                     'while True:\n'
                                                     '    pixels = frame.roster.long()\n'
                                                     '    frame = first_replace(frame, '
                                                     'roster=frame.roster.advance(4))\n'
                                                     '    frame = display_store_fields(state, frame, '
                                                     '262932, frame.auxiliary.base, pixels, 4)\n'
                                                     '    frame, more = display_loop_fields(frame, '
                                                     "'target_x')\n"
                                                     '    if not more:\n'
                                                     '        return frame',
                                             'returns': 'FirstDeploymentFrame',
                                             'signature': 'state: SceneState, frame: '
                                                          'FirstDeploymentFrame'},
 'upload_one_scene_tile': {'flow': 'from ..high_level_main_flows.contexts_display_fields import '
                                   'display_legacy_frame_fields\n'
                                   'entered = display_legacy_frame_fields(state, source, 418500)\n'
                                   'return upload_one_scene_tile_frame_fields(state, entered)',
                           'returns': 'TileUploadResult',
                           'signature': 'state: SceneState, source: Cursor, frame: SceneRenderFrame'},
 'upload_one_scene_tile_frame_fields': {'flow': 'frame = display_frame_fields(state, frame)\n'
                                                'frame = display_address_fields(state, frame, '
                                                "'candidates', 746650)\n"
                                                "frame = display_move_fields(state, frame, 'unit', "
                                                'frame.unit & 65535, 32)\n'
                                                'frame = display_shift_long_fields(state, frame, '
                                                "'unit', 5)\n"
                                                'frame = first_replace(frame, '
                                                'candidates=frame.candidates.advance(frame.unit))\n'
                                                "frame = display_move_fields(state, frame, 'count', 7)\n"
                                                'while True:\n'
                                                '    pixels = frame.candidates.long()\n'
                                                '    frame = first_replace(frame, '
                                                'candidates=frame.candidates.advance(4))\n'
                                                '    frame = display_store_fields(state, frame, 418520, '
                                                '12582912, pixels, 4)\n'
                                                "    frame, more = display_loop_fields(frame, 'count')\n"
                                                '    if not more:\n'
                                                '        return frame',
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'upload_portrait_tiles': {'flow': 'from ..high_level_main_flows.contexts_display_fields import '
                                   'display_legacy_frame_fields\n'
                                   'entered = display_legacy_frame_fields(state, frame, 418260)\n'
                                   'return upload_portrait_tiles_frame_fields(state, entered)',
                           'returns': 'TileUploadResult',
                           'signature': 'state: SceneState, frame: SceneRenderFrame'},
 'upload_portrait_tiles_frame_fields': {'flow': 'from ..high_level_main_flows.business_movement_support '
                                                'import _movement_add_word, _movement_compare\n'
                                                'from ..high_level_remaining_flows.business_city import '
                                                '_special_action_swap\n'
                                                'frame = display_frame_fields(state, frame)\n'
                                                "frame = display_move_fields(state, frame, 'target_y', "
                                                'frame.target_y & 65535, 32)\n'
                                                'frame = display_shift_long_fields(state, frame, '
                                                "'target_y', 7)\n"
                                                'frame = display_shift_word_fields(state, frame, '
                                                "'target_y', 2, True)\n"
                                                "frame = display_move_fields(state, frame, 'target_y', "
                                                'low16(frame.target_y) | 16384)\n'
                                                'frame = _special_action_swap(state, frame, '
                                                "'target_y')\n"
                                                'frame = display_store_fields(state, frame, 418276, '
                                                '12582916, frame.target_y, 4)\n'
                                                "frame = display_move_fields(state, frame, 'target_y', "
                                                'low16(frame.target_x))\n'
                                                'frame = display_shift_word_fields(state, frame, '
                                                "'target_y', 1)\n"
                                                "frame = _movement_add_word(state, frame, 'target_y', "
                                                'low16(frame.target_x))\n'
                                                'frame = display_shift_word_fields(state, frame, '
                                                "'target_y', 5)\n"
                                                "frame = display_address_fields(state, frame, 'roster', "
                                                '713626)\n'
                                                'frame = first_replace(frame, '
                                                'roster=frame.roster.advance(s16(low16(frame.target_y))))\n'
                                                'frame = display_call_fields(state, frame, 418484, '
                                                '418302)\n'
                                                "frame = display_move_fields(state, frame, 'target_y', "
                                                'low16(frame.target_x))\n'
                                                'frame = display_shift_word_fields(state, frame, '
                                                "'target_y', 4)\n"
                                                "frame = display_address_fields(state, frame, 'roster', "
                                                '738202)\n'
                                                'frame = first_replace(frame, '
                                                'roster=frame.roster.advance(s16(low16(frame.target_y))))\n'
                                                "frame = display_move_fields(state, frame, 'unit', 7)\n"
                                                'frame = _portrait_banked_strip_frame_fields(state, '
                                                'frame, False)\n'
                                                "frame = display_move_fields(state, frame, 'target_y', "
                                                'low16(frame.target_x))\n'
                                                'frame = display_shift_word_fields(state, frame, '
                                                "'target_y', 3)\n"
                                                "frame = display_address_fields(state, frame, 'roster', "
                                                '742298)\n'
                                                'frame = first_replace(frame, '
                                                'roster=frame.roster.advance(s16(low16(frame.target_y))))\n'
                                                "frame = display_move_fields(state, frame, 'unit', 3)\n"
                                                'frame = _portrait_banked_strip_frame_fields(state, '
                                                'frame, True)\n'
                                                'frame = display_address_fields(state, frame, '
                                                "'candidates', 743834)\n"
                                                'frame = display_address_fields(state, frame, '
                                                "'controller', 746394)\n"
                                                "frame = display_move_fields(state, frame, 'target_y', "
                                                '0, 32)\n'
                                                "frame = display_move_fields(state, frame, 'target_y', "
                                                'state.read(u32(frame.controller.base + '
                                                's16(low16(frame.target_x))), 1), 8)\n'
                                                'frame = display_shift_long_fields(state, frame, '
                                                "'target_y', 5)\n"
                                                'frame = first_replace(frame, '
                                                'candidates=frame.candidates.advance(frame.target_y))\n'
                                                "frame = display_move_fields(state, frame, 'unit', 7)\n"
                                                'frame = display_address_fields(state, frame, '
                                                "'controller', 4294966016)\n"
                                                'frame = _movement_compare(state, frame, '
                                                'state.read(4294964932, 2), 2, 16)\n'
                                                'if frame.status & 4:\n'
                                                '    frame = display_address_fields(state, frame, '
                                                "'controller', 4294966048)\n"
                                                'while True:\n'
                                                '    color = frame.candidates.long()\n'
                                                '    frame = first_replace(frame, '
                                                'candidates=frame.candidates.advance(4))\n'
                                                '    frame = display_store_fields(state, frame, 418470, '
                                                'frame.controller.base, color, 4)\n'
                                                '    frame = first_replace(frame, '
                                                'controller=frame.controller.advance(4))\n'
                                                "    frame, more = display_loop_fields(frame, 'unit')\n"
                                                '    if not more:\n'
                                                '        return display_store_fields(state, frame, '
                                                '418476, 4294963998, 1)',
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'upload_scene_tile_block': {'flow': 'from ..high_level_main_flows.contexts_display_fields import '
                                     'display_legacy_frame_fields\n'
                                     'entered = display_legacy_frame_fields(state, source, 418484)\n'
                                     'return upload_scene_tile_block_frame_fields(state, entered)',
                             'returns': 'TileUploadResult',
                             'signature': 'state: SceneState, source: Cursor, frame: SceneRenderFrame'},
 'upload_scene_tile_block_frame_fields': {'flow': 'frame = display_frame_fields(state, frame)\n'
                                                  'frame = display_move_fields(state, frame, '
                                                  "'distance', 47)\n"
                                                  'while True:\n'
                                                  '    tile = frame.roster.word()\n'
                                                  '    frame = first_replace(frame, '
                                                  'roster=frame.roster.advance(2))\n'
                                                  '    frame = display_move_fields(state, frame, '
                                                  "'unit', tile)\n"
                                                  '    frame = display_call_fields(state, frame, '
                                                  '418500, 418494)\n'
                                                  '    frame, more = display_loop_fields(frame, '
                                                  "'distance')\n"
                                                  '    if not more:\n'
                                                  '        return frame',
                                          'returns': 'FirstDeploymentFrame',
                                          'signature': 'state: SceneState, frame: FirstDeploymentFrame'}})
APPROVED.setdefault((2, 'high_level_main_flows.business_movement_support'), set()).update(('_movement_add_word', '_movement_compare', '_movement_multiply_word'))
APPROVED.setdefault((2, 'high_level_main_flows.contexts_display_fields'), set()).update(('display_address_fields', 'display_call_fields', 'display_frame_fields', 'display_legacy_frame_fields', 'display_loop_fields', 'display_move_fields', 'display_shift_long_fields', 'display_shift_word_fields', 'display_store_fields'))
APPROVED.setdefault((2, 'high_level_remaining_flows.business_city'), set()).update(('_special_action_swap',))
