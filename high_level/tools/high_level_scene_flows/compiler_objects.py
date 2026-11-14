"""Restricted semantic source admission with ordinary mnemonic lowering.

Reads explicit source text only. This is an intermediate structural compiler,
not a general Python compiler or full-console/indirect-handler implementation.
"""
from .compiler_common import CompileError, lower_declared
from .policy_common import admit_policy_source
from .objects_policy import ROLE_SPECS, owner_rules, LOWERERS as _SOURCE_LOWERERS
from .target import OBJECTS_BINDINGS

APPROVED={'business_reuse': {'build_battlefield_outcome_candidates',
                    'clear_video_sprite_plane',
                    'distribute_battle_progress_tail',
                    'enqueue_sound_command',
                    'wait_for_scene_sound_byte'},
 'business_scene': {'advance_scene_palette_fade',
                    'advance_scene_palette_fade_frame',
                    'begin_scene_palette_darken',
                    'begin_scene_palette_darken_frame',
                    'copy_scene_palette_variant',
                    'copy_scene_palette_variant_complete',
                    'finish_actor_sprite_chains',
                    'finish_actor_sprite_chains_frame',
                    'read_vdp_plane_rle_rows',
                    'read_vdp_plane_rle_rows_frame',
                    'sample_random_preserving_seed_carrier',
                    'sample_random_preserving_seed_frame',
                    'snapshot_and_clear_scene_palette',
                    'snapshot_and_clear_scene_palette_frame',
                    'write_vdp_swapped_byte_rle_stream',
                    'write_vdp_swapped_byte_rle_stream_frame'},
 'contexts_objects': {'ActionPlanOutcome',
                      'CoordinateIntegrationOutcome',
                      'ObjectActionContext',
                      'ObjectActionDispatch',
                      'ObjectOverlapOutcome',
                      'ObjectPhaseDispatch',
                      'ObjectPositionOffset',
                      'SceneActionPlanFields',
                      'SceneControllerConditions',
                      'SceneControllerFrame',
                      'SceneControllerOutcome',
                      'SceneObjectContext',
                      'SceneRenderFrame',
                      'SpriteBatchContext',
                      'SpriteBatchResult',
                      'checked_context',
                      'checked_controller_frame'},
 'domain': {'Boundary',
            'Cursor',
            'Long',
            'SceneState',
            'StackContinuation',
            'Table',
            'VideoPlaneAddress',
            'Word',
            'checked_cursor',
            'checked_state',
            'checked_table',
            'descending_inclusive',
            'divu_retained',
            'high16',
            'low16',
            'low8',
            'negative_word',
            'replace_byte',
            'replace_word',
            's16',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'},
 'dataclasses': {'replace'},
 (2, 'high_level_gameplay_flow.business_battle'): {'_presentation_call_fields'},
 (2, 'high_level_gameplay_flow.contexts_battle'): {'BattlePresentationMemory'},
 (2, 'high_level_gameplay_flow.business_services'): {'clear_video_sprite_plane_fields',
                                                     'enqueue_sound_command_fields',
                                                     'wait_for_scene_sound_byte_fields'},
 (2, 'high_level_main_flows.business_movement_support'): {'_movement_binary_flags',
                                                          '_movement_divu_word',
                                                          '_movement_multiply_word'},
 (2, 'high_level_dynamic_flows.business_early_phase'): {'step_main_scene_phase_fields'},
 (2, 'high_level_dynamic_flows.business_actions'): {'dispatch_object_action_fields'}}

DECLARATIONS={'_ram': {'signature': 'state, name',
          'returns': None,
          'flow': "return state.table('ram_' + name)"},
 '_shift_word': {'signature': 'carrier, shift',
                 'returns': None,
                 'flow': 'return replace_word(carrier, u16(low16(carrier) << shift))'},
 '_read_pointer': {'signature': 'state, table, offset',
                   'returns': None,
                   'flow': 'return state.table_at(table.long(offset))'},
 '_scene_move_conditions': {'signature': 'value, bits',
                            'returns': None,
                            'flow': 'value &= (1 << bits) - 1\n'
                                    'return SceneControllerConditions(False, value == 0, '
                                    'bool(value & 1 << bits - 1), False)'},
 '_scene_compare_conditions': {'signature': 'left, right, bits',
                               'returns': None,
                               'flow': 'mask, sign = ((1 << bits) - 1, 1 << bits - 1)\n'
                                       'left, right = (left & mask, right & mask)\n'
                                       'difference = left - right & mask\n'
                                       'return SceneControllerConditions(left < right, '
                                       'difference == 0, bool(difference & sign), bool((left '
                                       '^ right) & (left ^ difference) & sign))'},
 '_scene_add_conditions': {'signature': 'left, right, bits',
                           'returns': None,
                           'flow': 'mask, sign = ((1 << bits) - 1, 1 << bits - 1)\n'
                                   'left, right = (left & mask, right & mask)\n'
                                   'result = left + right & mask\n'
                                   'return SceneControllerConditions(left + right > mask, '
                                   'result == 0, bool(result & sign), bool(~(left ^ right) & '
                                   '(left ^ result) & sign))'},
 '_scene_shift_conditions': {'signature': 'value, shift',
                             'returns': None,
                             'flow': 'word = low16(value)\n'
                                     'result = u16(word << shift)\n'
                                     'signs = word >> 15 - shift\n'
                                     'overflow = signs not in (0, (1 << shift + 1) - 1)\n'
                                     'return SceneControllerConditions(bool(word & 1 << 16 - '
                                     'shift), result == 0, negative_word(result), overflow)'},
 '_scene_projection': {'signature': 'frame',
                       'returns': None,
                       'flow': 'return SceneRenderFrame(frame.x, frame.y, frame.attributes, '
                               'frame.palette, frame.tile, frame)'},
 '_consume_scene_return': {'signature': 'state, frame, continuation',
                           'returns': None,
                           'flow': 'actual = frame.stack.long()\n'
                                   'if actual != continuation:\n'
                                   "    raise Boundary('scene return-token alias left the "
                                   "known continuation', actual, frame)\n"
                                   'return replace(frame, stack=frame.stack.advance(4))'},
 '_scene_call': {'signature': 'state, frame, function, continuation',
                 'returns': None,
                 'flow': 'called = replace(frame, stack=frame.stack.advance(-4))\n'
                         'called.stack.set_long(0, uint(continuation, 32))\n'
                         'actual = function(state, called)\n'
                         'if type(actual) is not SceneControllerFrame:\n'
                         "    raise Boundary('ordinary scene call requires complete current "
                         "frame return')\n"
                         'actual.validate(state)\n'
                         'return _consume_scene_return(state, actual, continuation)'},
 '_scene_service_call': {'signature': 'state, frame, entry, continuation',
                         'returns': None,
                         'flow': 'called = replace(frame, stack=frame.stack.advance(-4))\n'
                                 'called.stack.set_long(0, uint(continuation, 32))\n'
                                 'actual = state.service_at(entry, called)\n'
                                 'if type(actual) is not SceneControllerFrame:\n'
                                 "    raise Boundary('complete scene service must return "
                                 "actual current frame')\n"
                                 'actual.validate(state)\n'
                                 'return _consume_scene_return(state, actual, continuation)'},
 '_scene_action_call': {'signature': 'state, frame, function, continuation',
                        'returns': None,
                        'flow': 'called = replace(frame, stack=frame.stack.advance(-4))\n'
                                'called.stack.set_long(0, uint(continuation, 32))\n'
                                'actual = function(state, called)\n'
                                'if type(actual) is SceneControllerFrame:\n'
                                '    actual = SceneControllerOutcome(actual, None)\n'
                                'if type(actual) is not SceneControllerOutcome:\n'
                                "    raise Boundary('actual scene action outcome required')\n"
                                'actual.validate(state)\n'
                                'return SceneControllerOutcome(_consume_scene_return(state, '
                                'actual.frame, continuation), actual.discarded_continuation)'},
 'integrate_scene_coordinates': {'signature': 'state: SceneState',
                                 'returns': 'CoordinateIntegrationOutcome',
                                 'flow': 'checked_state(state)\n'
                                         "for high_name, low_name, velocity_name in (('8024', "
                                         "'802c', '8038'), ('8026', '802e', '803a'), ('8020', "
                                         "'8034', '8040')):\n"
                                         '    coordinate = _ram(state, high_name).word() << '
                                         '16\n'
                                         '    coordinate |= _ram(state, low_name).word()\n'
                                         '    velocity = _ram(state, velocity_name).word()\n'
                                         '    if negative_word(velocity):\n'
                                         '        delta = (velocity & 32767) << 8\n'
                                         '        coordinate = u32(coordinate + delta)\n'
                                         '    else:\n'
                                         '        delta = velocity << 8\n'
                                         '        coordinate = u32(coordinate - delta)\n'
                                         '    _ram(state, low_name).set_word(0, '
                                         'low16(coordinate))\n'
                                         '    _ram(state, high_name).set_word(0, '
                                         'high16(coordinate))\n'
                                         'return '
                                         'CoordinateIntegrationOutcome(swap_words(coordinate), '
                                         'delta)'},
 '_normalize_object_squad_fields': {'signature': 'state',
                                    'returns': None,
                                    'flow': 'checked_state(state)\n'
                                            'while True:\n'
                                            "    total = _ram(state, '80e4').word()\n"
                                            "    count = _ram(state, '80e8').word()\n"
                                            '    if count == 0:\n'
                                            "        _ram(state, '80e8').set_word(0, "
                                            "u16(_ram(state, '80e8').word() + 1))\n"
                                            '    elif count > 15:\n'
                                            "        _ram(state, '80e8').set_word(0, "
                                            "u16(_ram(state, '80e8').word() - 1))\n"
                                            '    else:\n'
                                            '        packed = divu_retained(total, count)\n'
                                            '        quotient = low16(packed)\n'
                                            '        if quotient > 1000:\n'
                                            "            _ram(state, '80e8').set_word(0, "
                                            "u16(_ram(state, '80e8').word() + 1))\n"
                                            '        elif quotient <= 100 and _ram(state, '
                                            "'80e8').word() > 1:\n"
                                            "            _ram(state, '80e8').set_word(0, "
                                            "u16(_ram(state, '80e8').word() - 1))\n"
                                            '        else:\n'
                                            "            _ram(state, '80ec').set_word(0, "
                                            'quotient)\n'
                                            '            packed = swap_words(packed)\n'
                                            "            _ram(state, '80f0').set_word(0, "
                                            'low16(packed))\n'
                                            '            return (packed, count)'},
 'normalize_object_squad_size': {'signature': 'state: SceneState',
                                 'returns': 'Long',
                                 'flow': 'return _normalize_object_squad_fields(state)[0]'},
 'normalize_object_squad_size_complete': {'signature': 'state, context',
                                          'returns': None,
                                          'flow': 'frame = checked_controller_frame(context, '
                                                  'state)\n'
                                                  'packed, count = '
                                                  '_normalize_object_squad_fields(state)\n'
                                                  'return replace(frame, x=packed, y=count, '
                                                  'conditions=_scene_move_conditions(low16(packed), '
                                                  '16))'},
 'cycle_special_scene_palette_complete': {'signature': 'state, context',
                                          'returns': None,
                                          'flow': 'frame = checked_controller_frame(context, '
                                                  'state)\n'
                                                  "mode = _ram(state, '80db').byte()\n"
                                                  'conditions = '
                                                  '_scene_compare_conditions(mode, 3, 8)\n'
                                                  'if mode != 3:\n'
                                                  '    return replace(frame, '
                                                  'conditions=conditions)\n'
                                                  "enabled = bool(_ram(state, '80c4').byte() "
                                                  '& 128)\n'
                                                  'conditions = replace(conditions, zero=not '
                                                  'enabled)\n'
                                                  'if not enabled:\n'
                                                  '    return replace(frame, '
                                                  'conditions=conditions)\n'
                                                  "offset = _ram(state, 'f320').word() >> 3 & "
                                                  '6\n'
                                                  'palette = state.table_at(260292)\n'
                                                  "_ram(state, 'fb02').set_word(0, "
                                                  'palette.word(offset))\n'
                                                  "_ram(state, 'fb04').set_word(0, "
                                                  'palette.word(offset, 8))\n'
                                                  'last = palette.word(offset, 16)\n'
                                                  "_ram(state, 'fb06').set_word(0, last)\n"
                                                  'return replace(frame, '
                                                  'x=replace_word(frame.x, offset), '
                                                  'source=palette.cursor(), '
                                                  'conditions=_scene_move_conditions(last, '
                                                  '16))'},
 'clear_scene_object_label_plane_complete': {'signature': 'state, context',
                                             'returns': None,
                                             'flow': 'frame = '
                                                     'checked_controller_frame(context, '
                                                     'state)\n'
                                                     'state.write(12582916, 4, 1073741827)\n'
                                                     'for _ in descending_inclusive(2047):\n'
                                                     '    state.write(12582912, 2, 1024)\n'
                                                     'return replace(frame, '
                                                     'traversal=state.table_at(12582912).cursor(), '
                                                     'row_count=replace_word(frame.row_count, '
                                                     '1024), layer=replace_word(frame.layer, '
                                                     '65535), '
                                                     'conditions=_scene_move_conditions(1024, '
                                                     '16))'},
 'read_object_action_mode': {'signature': 'state: SceneState, actor: Table',
                             'returns': 'Long',
                             'flow': 'checked_state(state)\n'
                                     'checked_table(actor, state)\n'
                                     'slot = actor.byte(0, 1)\n'
                                     'if actor.base >= 4294935146:\n'
                                     '    slot = u16(slot + 4)\n'
                                     'offset = u16(slot << 1)\n'
                                     "return _ram(state, '812a').word(offset)"},
 'offset_scene_object_position_complete': {'signature': 'state, context',
                                           'returns': None,
                                           'flow': 'frame = checked_controller_frame(context, '
                                                   'state)\n'
                                                   'actor = frame.actor\n'
                                                   'for displacement, value in ((2, '
                                                   'low16(frame.x)), (4, low16(frame.y))):\n'
                                                   '    frame = replace(frame, '
                                                   'attributes=replace_word(frame.attributes, '
                                                   'value))\n'
                                                   '    previous = actor.word(0, '
                                                   'displacement)\n'
                                                   '    if negative_word(value):\n'
                                                   '        value &= 127\n'
                                                   '        result = u16(previous - value)\n'
                                                   '        conditions = '
                                                   '_scene_compare_conditions(previous, '
                                                   'value, 16)\n'
                                                   '    else:\n'
                                                   '        result = u16(previous + value)\n'
                                                   '        conditions = '
                                                   '_scene_add_conditions(previous, value, '
                                                   '16)\n'
                                                   '    actor.set_word(0, result, '
                                                   'displacement)\n'
                                                   '    frame = replace(frame, '
                                                   'conditions=conditions, '
                                                   'x=replace_word(frame.x, value) if '
                                                   'displacement == 2 else frame.x, '
                                                   'y=replace_word(frame.y, value) if '
                                                   'displacement == 4 else frame.y)\n'
                                                   'return frame'},
 'probe_scene_object_overlap_complete': {'signature': 'state, context',
                                         'returns': None,
                                         'flow': 'frame = checked_controller_frame(context, '
                                                 'state)\n'
                                                 'actor = frame.actor\n'
                                                 'original = actor.long(0, 2)\n'
                                                 'frame = replace(frame, palette=original)\n'
                                                 'frame = _scene_call(state, frame, '
                                                 'offset_scene_object_position_complete, '
                                                 '266596)\n'
                                                 'frame = replace(frame, x=0, '
                                                 "traversal=_ram(state, '816a').cursor())\n"
                                                 'candidate = frame.traversal\n'
                                                 'while candidate.base < 4294935402:\n'
                                                 '    if candidate.byte() & 128 and '
                                                 'candidate.base != actor.base:\n'
                                                 '        horizontal = candidate.word(0, 2)\n'
                                                 '        frame = replace(frame, '
                                                 'y=replace_word(frame.y, horizontal))\n'
                                                 '        if horizontal == actor.word(0, 2):\n'
                                                 '            vertical = candidate.word(0, '
                                                 '4)\n'
                                                 '            frame = replace(frame, '
                                                 'y=replace_word(frame.y, vertical))\n'
                                                 '            if vertical == actor.word(0, '
                                                 '4):\n'
                                                 '                actor.set_long(0, original, '
                                                 '2)\n'
                                                 '                return replace(frame, x=1, '
                                                 'traversal=candidate, '
                                                 'conditions=_scene_move_conditions(original, '
                                                 '32))\n'
                                                 '    candidate = candidate.advance(16)\n'
                                                 'actor.set_long(0, original, 2)\n'
                                                 'return replace(frame, traversal=candidate, '
                                                 'conditions=_scene_move_conditions(original, '
                                                 '32))'},
 'probe_opposing_object_overlap_complete': {'signature': 'state, context',
                                            'returns': None,
                                            'flow': 'frame = '
                                                    'checked_controller_frame(context, '
                                                    'state)\n'
                                                    'frame = _scene_call(state, frame, '
                                                    'probe_scene_object_overlap_complete, '
                                                    '267518)\n'
                                                    'if low16(frame.x):\n'
                                                    '    same_side = (frame.actor.base >= '
                                                    '4294935146) == (frame.traversal.base >= '
                                                    '4294935146)\n'
                                                    '    if not same_side:\n'
                                                    '        return replace(frame, '
                                                    'conditions=_scene_compare_conditions(frame.traversal.base, '
                                                    '4294935146, 32))\n'
                                                    'return replace(frame, x=0, '
                                                    'conditions=_scene_move_conditions(0, '
                                                    '32))'},
 'rebuild_depth_sorted_object_queue_complete': {'signature': 'state, context',
                                                'returns': None,
                                                'flow': 'frame = '
                                                        'checked_controller_frame(context, '
                                                        'state)\n'
                                                        "tick = _ram(state, 'f320').word() & "
                                                        '15\n'
                                                        'frame = replace(frame, '
                                                        'x=replace_word(frame.x, tick), '
                                                        'conditions=_scene_move_conditions(tick, '
                                                        '16))\n'
                                                        'if tick:\n'
                                                        '    return frame\n'
                                                        'destination = _ram(state, '
                                                        "'836a').cursor()\n"
                                                        'for depth in '
                                                        'descending_inclusive(30):\n'
                                                        "    actor = _ram(state, '816a')\n"
                                                        '    while True:\n'
                                                        '        if actor.byte() & 128:\n'
                                                        '            horizontal = '
                                                        'actor.word(0, 2) >> 4\n'
                                                        '            frame = replace(frame, '
                                                        'y=replace_word(frame.y, '
                                                        'horizontal))\n'
                                                        '            if horizontal == depth:\n'
                                                        '                '
                                                        'destination.append_long(actor.base)\n'
                                                        '        actor = '
                                                        'state.table_at(u32(actor.base + '
                                                        '16))\n'
                                                        '        if actor.base >= '
                                                        '4294935402:\n'
                                                        '            break\n'
                                                        'destination.append_long(0)\n'
                                                        'return replace(frame, x=65535, '
                                                        'traversal=destination.advance(-4), '
                                                        'actor=actor, '
                                                        'conditions=_scene_move_conditions(0, '
                                                        '32))'},
 'dispatch_scene_object_phase_complete': {'signature': 'state: SceneState, context: '
                                                       'SceneControllerFrame',
                                          'returns': 'SceneControllerOutcome',
                                          'flow': 'frame = checked_controller_frame(context, '
                                                  'state)\n'
                                                  'phase = replace_word(frame.x, _ram(state, '
                                                  "'813a').word())\n"
                                                  'conditions = '
                                                  '_scene_shift_conditions(phase, 2)\n'
                                                  'phase = _shift_word(phase, 2)\n'
                                                  'entry = u32(253122 + s16(low16(phase)))\n'
                                                  'frame = replace(frame, x=phase, '
                                                  'conditions=conditions)\n'
                                                  'result = state.service_at(entry, frame)\n'
                                                  'if type(result) is SceneControllerFrame:\n'
                                                  '    result = '
                                                  'SceneControllerOutcome(result, None)\n'
                                                  'if type(result) is not '
                                                  'SceneControllerOutcome:\n'
                                                  "    raise Boundary('phase continuation "
                                                  "must return actual typed scene operands')\n"
                                                  'return result.validate(state)'},
 'distribute_secondary_city_battle_progress': {'signature': 'state: SceneState',
                                               'returns': 'None',
                                               'flow': 'checked_state(state)\n'
                                                       'from .business_reuse import '
                                                       'build_battlefield_outcome_candidates, '
                                                       'distribute_battle_progress_tail\n'
                                                       'count = '
                                                       'build_battlefield_outcome_candidates(state)\n'
                                                       'budget = u16(_ram(state, '
                                                       "'efba').word() << 1)\n"
                                                       'distribute_battle_progress_tail(state, '
                                                       'count, budget)'},
 '_append_sprite_entries_complete': {'signature': 'state, context',
                                     'returns': None,
                                     'flow': 'frame = checked_controller_frame(context, '
                                             'state)\n'
                                             'source = frame.source\n'
                                             'destination_role = frame.destination\n'
                                             'saved = frame.stack.advance(-12)\n'
                                             'destination_address = destination_role.carrier '
                                             'if type(destination_role) is VideoPlaneAddress '
                                             'else destination_role.base\n'
                                             'frame.stack.advance(-4).set_long(0, '
                                             'destination_address)\n'
                                             'frame.stack.advance(-8).set_long(0, '
                                             'frame.row_count)\n'
                                             'saved.set_long(0, frame.extent)\n'
                                             'frame = replace(frame, stack=saved)\n'
                                             'x, y = (frame.x, frame.y)\n'
                                             'attributes, palette, tile = (frame.attributes, '
                                             'frame.palette, frame.tile)\n'
                                             "capacity = _ram(state, 'f300').byte()\n"
                                             'conditions = '
                                             '_scene_compare_conditions(capacity, 80, 8)\n'
                                             'if capacity >= 80:\n'
                                             '    return _restore_scene_sprite_saved(state, '
                                             'replace(frame, conditions=conditions), '
                                             'destination_role)\n'
                                             'tile &= 65535\n'
                                             'bucket = u16((low16(attributes) & 7) << 2)\n'
                                             'layer = replace_word(frame.layer, bucket)\n'
                                             'attributes = replace_word(attributes, '
                                             'low16(attributes) & 65528)\n'
                                             'x = replace_word(x, u16(low16(x) - _ram(state, '
                                             "'8020').word() + 128))\n"
                                             'if negative_word(low16(x)):\n'
                                             '    conditions = '
                                             '_scene_add_conditions(u16(low16(x) - 128), 128, '
                                             '16)\n'
                                             '    return _restore_scene_sprite_saved(state, '
                                             'replace(frame, x=x, attributes=attributes, '
                                             'tile=tile, layer=layer, conditions=conditions), '
                                             'destination_role)\n'
                                             'if attributes & 32:\n'
                                             '    x = replace_word(x, u16(low16(x) - 8))\n'
                                             'y = replace_word(y, u16(low16(y) - _ram(state, '
                                             "'8022').word() + 128))\n"
                                             'if attributes & 16:\n'
                                             '    y = replace_word(y, u16(low16(y) - 8))\n'
                                             'destination = _ram(state, '
                                             "'f800').at(u16(_ram(state, 'f300').byte() << "
                                             '3))\n'
                                             "buckets = _ram(state, '8044')\n"
                                             'parameters = frame.parameters\n'
                                             'while True:\n'
                                             '    horizontal = source.byte()\n'
                                             '    if horizontal == 128:\n'
                                             '        conditions = '
                                             '_scene_compare_conditions(horizontal, 128, 8)\n'
                                             '        break\n'
                                             '    if attributes & 32:\n'
                                             '        horizontal = u8(-horizontal)\n'
                                             '    sprite_x = u16(low16(x) + (-u8(-horizontal) '
                                             'if horizontal & 128 else horizontal))\n'
                                             '    destination.set_word(0, sprite_x)\n'
                                             '    vertical = source.byte(0, 3)\n'
                                             '    if attributes & 16:\n'
                                             '        vertical = u8(-vertical)\n'
                                             '    sprite_y = u16(low16(y) + (-u8(-vertical) '
                                             'if vertical & 128 else vertical))\n'
                                             '    destination.set_word(0, sprite_y, 6)\n'
                                             '    destination.set_byte(0, source.byte(0, 1), '
                                             '2)\n'
                                             '    if buckets.long(bucket) == 0:\n'
                                             '        buckets.set_long(bucket, '
                                             'destination.base)\n'
                                             '        buckets.set_byte(bucket, _ram(state, '
                                             "'f300').byte(), 32)\n"
                                             '    else:\n'
                                             '        previous = '
                                             'state.table_at(buckets.long(bucket, 64))\n'
                                             '        parameters = previous\n'
                                             '        previous.set_byte(0, _ram(state, '
                                             "'f300').byte(), 3)\n"
                                             '    buckets.set_long(bucket, destination.base, '
                                             '64)\n'
                                             "    _ram(state, 'f300').set_byte(0, "
                                             "u8(_ram(state, 'f300').byte() + 1))\n"
                                             '    shape = source.byte(0, 1) & 240\n'
                                             '    shape = u8(shape + low8(palette))\n'
                                             '    shape = u16(shape ^ low16(attributes))\n'
                                             '    shape = u16(shape << 7)\n'
                                             '    shape = shape & 65280 | u8(low8(shape) | '
                                             'source.byte(0, 2))\n'
                                             '    destination.set_word(0, u16(shape + '
                                             'low16(tile)), 4)\n'
                                             '    destination = destination.advance(8)\n'
                                             '    source.base = u32(source.base + 4)\n'
                                             "    capacity = _ram(state, 'f300').byte()\n"
                                             '    conditions = '
                                             '_scene_compare_conditions(capacity, 80, 8)\n'
                                             '    if capacity >= 80:\n'
                                             '        break\n'
                                             'actual = replace(frame, x=x, y=y, '
                                             'attributes=attributes, palette=palette, '
                                             'tile=tile, layer=layer, source=source, '
                                             'directory=buckets, parameters=parameters, '
                                             'conditions=conditions)\n'
                                             'return _restore_scene_sprite_saved(state, '
                                             'actual, destination_role)'},
 '_restore_scene_sprite_saved': {'signature': 'state, frame, destination_role',
                                 'returns': None,
                                 'flow': 'extent = frame.stack.long()\n'
                                         'rows = frame.stack.long(0, 4)\n'
                                         'address = frame.stack.long(0, 8)\n'
                                         'destination = VideoPlaneAddress(address) if '
                                         'type(destination_role) is VideoPlaneAddress else '
                                         'state.table_at(address).cursor()\n'
                                         'return replace(frame, extent=extent, '
                                         'row_count=rows, destination=destination, '
                                         'stack=frame.stack.advance(12))'},
 '_append_sprite_entries': {'signature': 'state, context',
                            'returns': None,
                            'flow': 'checked_context(context, SpriteBatchContext, state)\n'
                                    'frame = checked_controller_frame(context.frame, state)\n'
                                    'actual = _append_sprite_entries_complete(state, '
                                    'replace(frame, source=context.source))\n'
                                    'return SpriteBatchResult(actual.source, '
                                    '_scene_projection(actual))'},
 'append_scene_center_marker_complete': {'signature': 'state: SceneState, context: '
                                                      'SceneControllerFrame',
                                         'returns': 'SceneControllerFrame',
                                         'flow': 'frame = checked_controller_frame(context, '
                                                 'state)\n'
                                                 'frame = replace(frame, '
                                                 'x=replace_word(frame.x, u16(_ram(state, '
                                                 "'8020').word() - 64)), "
                                                 'y=replace_word(frame.y, u16(_ram(state, '
                                                 "'8022').word() - 64)), attributes=0, "
                                                 'palette=0, tile=replace_word(frame.tile, '
                                                 '0))\n'
                                                 'source = state.table_at(242346).cursor()\n'
                                                 'return '
                                                 '_append_sprite_entries_complete(state, '
                                                 'replace(frame, source=source))'},
 'draw_active_scene_object_complete': {'signature': 'state: SceneState, context: '
                                                    'SceneControllerFrame',
                                       'returns': 'SceneControllerOutcome',
                                       'flow': 'frame = checked_controller_frame(context, '
                                               'state)\n'
                                               'discarded = None\n'
                                               "if _ram(state, '813e').word() == 0:\n"
                                               '    outcome = _scene_action_call(state, '
                                               'frame, '
                                               'update_selected_object_action_complete, '
                                               '263248)\n'
                                               '    frame, discarded = (outcome.frame, '
                                               'outcome.discarded_continuation)\n'
                                               'actor = frame.actor\n'
                                               'object_kind = actor.word() & 255\n'
                                               'animation = '
                                               'state.table_at(263372).byte(object_kind)\n'
                                               "if _ram(state, '80db').byte() == 3:\n"
                                               '    animation = '
                                               'state.table_at(263372).byte(object_kind, 4)\n'
                                               "if _ram(state, '8124').word() == 0:\n"
                                               '    if actor.base >= 4294935146:\n'
                                               '        animation = u16(animation + 96)\n'
                                               'elif actor.base < 4294935146:\n'
                                               '    animation = u16(animation + 96)\n'
                                               'animation = u16(animation + u16(actor.word(0, '
                                               '8) << 2))\n'
                                               "index = u16((_ram(state, 'f320').word() >> 3 "
                                               '& 3) + animation)\n'
                                               'tile = replace_word(frame.tile, index)\n'
                                               'pointer_offset = u16(index << 2)\n'
                                               'source = _read_pointer(state, '
                                               'state.table_at(263380), '
                                               'pointer_offset).cursor()\n'
                                               'x = replace_word(frame.x, actor.word(0, 2))\n'
                                               'y = replace_word(0, actor.word(0, 4))\n'
                                               'tile = _shift_word(tile, 1)\n'
                                               'tile = replace_word(tile, '
                                               'state.table_at(264148).word(low16(tile)))\n'
                                               'selected = replace(frame, x=x, y=y, '
                                               'attributes=replace_word(frame.attributes, 5), '
                                               'palette=0, tile=tile, source=source, '
                                               'destination=state.table_at(264148).cursor(), '
                                               'conditions=_scene_move_conditions(low16(tile), '
                                               '16))\n'
                                               'return '
                                               'SceneControllerOutcome(_append_sprite_entries_complete(state, '
                                               'selected), discarded)'},
 'plan_scene_object_action_complete': {'signature': 'state, context',
                                       'returns': None,
                                       'flow': 'frame = checked_controller_frame(context, '
                                               'state)\n'
                                               'actor = frame.actor\n'
                                               'from .business_reuse import '
                                               'enqueue_sound_command\n'
                                               'secondary = actor.base >= 4294935146\n'
                                               'slot = u16(actor.byte(0, 1) + (4 if secondary '
                                               'else 0) << 1)\n'
                                               "mode = _ram(state, '812a').word(slot)\n"
                                               'frame = replace(frame, x=slot, '
                                               "source=_ram(state, '812a').cursor(), "
                                               'conditions=_scene_compare_conditions(mode, 6, '
                                               '16))\n'
                                               '\n'
                                               'def try_offset(horizontal, vertical, '
                                               'continuation):\n'
                                               '    nonlocal frame\n'
                                               '    frame = replace(frame, '
                                               'x=replace_word(frame.x, horizontal), '
                                               'y=replace_word(frame.y, vertical))\n'
                                               '    frame = _scene_call(state, frame, '
                                               'probe_opposing_object_overlap_complete, '
                                               'continuation)\n'
                                               '    frame = replace(frame, '
                                               'conditions=_scene_move_conditions(low16(frame.x), '
                                               '16))\n'
                                               '    return low16(frame.x) != 0\n'
                                               '\n'
                                               'def select_direction(direction, phase):\n'
                                               "    _ram(state, '8000').set_word(0, "
                                               'direction)\n'
                                               "    _ram(state, '8158').set_word(0, phase)\n"
                                               '\n'
                                               'def finish(long_reach):\n'
                                               '    nonlocal frame\n'
                                               '    target = frame.traversal\n'
                                               '    if not long_reach and target.base in '
                                               '(4294934890, 4294935146):\n'
                                               "        if _ram(state, '814e').word() == 3:\n"
                                               '            token = frame.stack.long()\n'
                                               '            side = u16(_ram(state, '
                                               "'814c').word() - 1)\n"
                                               "            _ram(state, '8176').set_word(0, "
                                               'side)\n'
                                               "            _ram(state, '813a').set_word(0, "
                                               '3)\n'
                                               "            _ram(state, '813c').set_word(0, "
                                               '0)\n'
                                               "            _ram(state, '813e').set_word(0, "
                                               '1)\n'
                                               "            _ram(state, '8152').set_word(0, "
                                               '2)\n'
                                               '            frame = replace(frame, '
                                               'x=replace_word(token, side), '
                                               'stack=frame.stack.advance(4), '
                                               'conditions=_scene_move_conditions(2, 16))\n'
                                               '            return '
                                               'SceneControllerOutcome(frame, '
                                               'StackContinuation(token))\n'
                                               "    _ram(state, '815c').set_long(0, "
                                               'target.base)\n'
                                               "    _ram(state, '815a').set_word(0, 9 if "
                                               'long_reach else 8)\n'
                                               "    _ram(state, '8162').set_word(0, 0)\n"
                                               '    if long_reach:\n'
                                               "        _ram(state, '8164').set_word(0, "
                                               'actor.word(0, 2))\n'
                                               "        _ram(state, '8166').set_word(0, "
                                               'actor.word(0, 4))\n'
                                               "        _ram(state, '8168').set_word(0, 0)\n"
                                               '    actor.set_word(0, _ram(state, '
                                               "'8000').word(), 8)\n"
                                               '    token = frame.stack.long()\n'
                                               '    command = replace_word(token, 162 if '
                                               'long_reach else 167)\n'
                                               '    frame = replace(frame, x=command, '
                                               'stack=frame.stack.advance(4))\n'
                                               '    if long_reach:\n'
                                               '        called = replace(frame, '
                                               'stack=frame.stack.advance(-4))\n'
                                               '        called.stack.set_long(0, 267414)\n'
                                               '    enqueue_sound_command(state, '
                                               'low8(command))\n'
                                               '    if long_reach:\n'
                                               '        frame = _consume_scene_return(state, '
                                               'called, 267414)\n'
                                               '    return '
                                               'SceneControllerOutcome(replace(frame, '
                                               'conditions=_scene_move_conditions(0, 16)), '
                                               'StackContinuation(token))\n'
                                               'if mode == 6:\n'
                                               '    horizontal = 16 if secondary else 32784\n'
                                               '    select_direction(0 if secondary else 1, 1 '
                                               'if secondary else 0)\n'
                                               '    if try_offset(horizontal, 0, 266758 if '
                                               'secondary else 266884):\n'
                                               '        return finish(False)\n'
                                               '    kind = actor.byte(0, 1)\n'
                                               '    if kind != 1:\n'
                                               '        return '
                                               'SceneControllerOutcome(replace(frame, '
                                               'conditions=_scene_compare_conditions(kind, 1, '
                                               '8)), None)\n'
                                               '    select_direction(0 if secondary else 1, 1 '
                                               'if secondary else 0)\n'
                                               '    for magnitude, continuation in ((32, '
                                               '266798 if secondary else 266924), (48, 266816 '
                                               'if secondary else 266942), (64, 266834 if '
                                               'secondary else 266960)):\n'
                                               '        if try_offset(magnitude if secondary '
                                               'else magnitude | 32768, 0, continuation):\n'
                                               '            return finish(True)\n'
                                               '    return SceneControllerOutcome(frame, '
                                               'None)\n'
                                               'for direction, phase, horizontal, vertical, '
                                               'continuation in ((1, 0, 32784, 0, 266994), '
                                               '(0, 1, 16, 0, 267024), (2, 3, 0, 16, 267054), '
                                               '(3, 6, 0, 32784, 267084)):\n'
                                               '    select_direction(direction, phase)\n'
                                               '    if try_offset(horizontal, vertical, '
                                               'continuation):\n'
                                               '        return finish(False)\n'
                                               'kind = actor.byte(0, 1)\n'
                                               'if kind != 1:\n'
                                               '    return '
                                               'SceneControllerOutcome(replace(frame, '
                                               'conditions=_scene_compare_conditions(kind, 1, '
                                               '8)), None)\n'
                                               'for direction, phase, offsets in ((1, 0, '
                                               '((32800, 0, 267124), (32816, 0, 267142), '
                                               '(32832, 0, 267160))), (0, 1, ((32, 0, '
                                               '267190), (48, 0, 267208), (64, 0, 267226))), '
                                               '(2, 3, ((0, 32, 267256), (0, 3, 267274), (0, '
                                               '64, 267292))), (3, 6, ((0, 32800, 267322), '
                                               '(0, 32816, 267340), (0, 32832, 267358)))):\n'
                                               '    select_direction(direction, phase)\n'
                                               '    for horizontal, vertical, continuation in '
                                               'offsets:\n'
                                               '        if try_offset(horizontal, vertical, '
                                               'continuation):\n'
                                               '            return finish(True)\n'
                                               'return SceneControllerOutcome(frame, None)'},
 '_select_scene_object_action_complete': {'signature': 'state, context, secondary',
                                          'returns': None,
                                          'flow': 'frame = checked_controller_frame(context, '
                                                  'state)\n'
                                                  'actor = frame.actor\n'
                                                  "roster = _ram(state, '826a' if secondary "
                                                  "else '816a')\n"
                                                  'frame = replace(frame, '
                                                  'traversal=roster.cursor())\n'
                                                  "side = _ram(state, '814c').word()\n"
                                                  'frame = replace(frame, '
                                                  'conditions=_scene_compare_conditions(side, '
                                                  '2 if secondary else 1, 16))\n'
                                                  'if side != (2 if secondary else 1):\n'
                                                  '    return SceneControllerOutcome(frame, '
                                                  'None)\n'
                                                  'kind = actor.word() & 127\n'
                                                  'frame = replace(frame, '
                                                  'x=replace_word(frame.x, kind))\n'
                                                  "category = _ram(state, '814e').word()\n"
                                                  'frame = replace(frame, '
                                                  'conditions=_scene_compare_conditions(kind, '
                                                  'category, 16))\n'
                                                  'if kind != category:\n'
                                                  '    return SceneControllerOutcome(frame, '
                                                  'None)\n'
                                                  "slot = u16(_ram(state, '8150').word() << "
                                                  '4)\n'
                                                  'selected_address = u32(roster.base + '
                                                  's16(slot))\n'
                                                  'frame = replace(frame, x=slot, '
                                                  'source=state.table_at(selected_address).cursor(), '
                                                  'conditions=_scene_compare_conditions(selected_address, '
                                                  'actor.base, 32))\n'
                                                  'if selected_address != actor.base:\n'
                                                  '    return SceneControllerOutcome(frame, '
                                                  'None)\n'
                                                  "resumed = _ram(state, '8152').word() != 0\n"
                                                  'if resumed:\n'
                                                  '    selection = replace_word(frame.x, '
                                                  "_ram(state, '815a').word())\n"
                                                  '    table_base = 265550\n'
                                                  'else:\n'
                                                  "    _ram(state, '8152').set_word(0, 1)\n"
                                                  '    horizontal = actor.word(0, 2)\n'
                                                  '    frame = replace(frame, '
                                                  'conditions=_scene_compare_conditions(horizontal, '
                                                  '512, 16))\n'
                                                  '    if horizontal >= 512:\n'
                                                  "        _ram(state, '8152').set_word(0, "
                                                  '0)\n'
                                                  '        return '
                                                  'SceneControllerOutcome(replace(frame, '
                                                  'conditions=_scene_move_conditions(0, 16)), '
                                                  'None)\n'
                                                  '    from .business_scene import '
                                                  'sample_random_preserving_seed_frame\n'
                                                  '    frame = _scene_call(state, frame, '
                                                  'sample_random_preserving_seed_frame, '
                                                  '265460)\n'
                                                  '    selection = replace_word(frame.x, '
                                                  'low16(frame.x) & 3)\n'
                                                  '    frame = replace(frame, x=selection, '
                                                  'conditions=_scene_move_conditions(low16(selection), '
                                                  '16))\n'
                                                  '    if low16(selection) != 0:\n'
                                                  '        called = replace(frame, '
                                                  'stack=frame.stack.advance(-4))\n'
                                                  '        called.stack.set_long(0, 265470)\n'
                                                  '        outcome = '
                                                  'plan_scene_object_action_complete(state, '
                                                  'called).validate(state)\n'
                                                  '        frame = outcome.frame\n'
                                                  '        if outcome.discarded_continuation '
                                                  'is not None:\n'
                                                  '            return outcome\n'
                                                  '        frame = '
                                                  '_consume_scene_return(state, frame, '
                                                  '265470)\n'
                                                  '    called = replace(frame, '
                                                  'stack=frame.stack.advance(-4))\n'
                                                  '    called.stack.set_long(0, 265474)\n'
                                                  '    selection = '
                                                  'read_object_action_mode(state, '
                                                  'frame.actor)\n'
                                                  '    frame = _consume_scene_return(state, '
                                                  'called, 265474)\n'
                                                  '    frame = replace(frame, x=selection, '
                                                  "source=_ram(state, '812a').cursor(), "
                                                  'conditions=_scene_move_conditions(selection, '
                                                  '16))\n'
                                                  "    _ram(state, '815a').set_word(0, "
                                                  'low16(selection))\n'
                                                  '    table_base = 265484\n'
                                                  'conditions = '
                                                  '_scene_shift_conditions(selection, 2)\n'
                                                  'selection = _shift_word(selection, 2)\n'
                                                  'entry = u32(table_base + '
                                                  's16(low16(selection)))\n'
                                                  'frame = replace(frame, x=selection, '
                                                  'conditions=conditions)\n'
                                                  'outcome = state.service_at(entry, frame)\n'
                                                  'if type(outcome) is SceneControllerFrame:\n'
                                                  '    outcome = '
                                                  'SceneControllerOutcome(outcome, None)\n'
                                                  'if type(outcome) is not '
                                                  'SceneControllerOutcome:\n'
                                                  "    raise Boundary('action tail must "
                                                  "return actual typed scene operands')\n"
                                                  'return outcome.validate(state)'},
 'update_selected_object_action_complete': {'signature': 'state: SceneState, context: '
                                                         'SceneControllerFrame',
                                            'returns': 'SceneControllerOutcome',
                                            'flow': 'frame = '
                                                    'checked_controller_frame(context, '
                                                    'state)\n'
                                                    'secondary = frame.actor.base >= '
                                                    '4294935146\n'
                                                    'frame = replace(frame, '
                                                    'conditions=_scene_compare_conditions(frame.actor.base, '
                                                    '4294935146, 32))\n'
                                                    'return '
                                                    '_select_scene_object_action_complete(state, '
                                                    'frame, secondary)'},
 'resume_selected_object_action_complete': {'signature': 'state, context',
                                            'returns': None,
                                            'flow': 'frame = '
                                                    'checked_controller_frame(context, '
                                                    'state)\n'
                                                    'return '
                                                    '_select_scene_object_action_complete(state, '
                                                    'frame, False)'},
 'advance_scene_object_actions_complete': {'signature': 'state: SceneState, context: '
                                                        'SceneControllerFrame',
                                           'returns': 'SceneControllerOutcome',
                                           'flow': 'frame = checked_controller_frame(context, '
                                                   'state)\n'
                                                   'discarded = None\n'
                                                   'frame = _scene_call(state, frame, '
                                                   'rebuild_depth_sorted_object_queue_complete, '
                                                   '262976)\n'
                                                   'frame = replace(frame, '
                                                   "traversal=_ram(state, '836a').cursor())\n"
                                                   'while True:\n'
                                                   '    address = frame.traversal.long()\n'
                                                   '    frame = replace(frame, '
                                                   'conditions=_scene_move_conditions(address, '
                                                   '32))\n'
                                                   '    if address == 0:\n'
                                                   '        break\n'
                                                   '    actor = '
                                                   'state.table_at(frame.traversal.long())\n'
                                                   '    frame = replace(frame, '
                                                   'traversal=frame.traversal.advance(4), '
                                                   'actor=actor)\n'
                                                   '    if actor.byte() & 128:\n'
                                                   '        saved = frame.stack.advance(-4)\n'
                                                   '        saved.set_long(0, '
                                                   'frame.traversal.base)\n'
                                                   '        frame = replace(frame, '
                                                   'stack=saved)\n'
                                                   '        outcome = '
                                                   '_scene_action_call(state, frame, '
                                                   'draw_active_scene_object_complete, '
                                                   '263000)\n'
                                                   '        frame = outcome.frame\n'
                                                   '        if outcome.discarded_continuation '
                                                   'is not None:\n'
                                                   '            discarded = '
                                                   'outcome.discarded_continuation\n'
                                                   '        restored = frame.stack.long()\n'
                                                   '        frame = replace(frame, '
                                                   'traversal=state.table_at(restored).cursor(), '
                                                   'stack=frame.stack.advance(4))\n'
                                                   "side = _ram(state, '814c').word()\n"
                                                   'frame = replace(frame, '
                                                   'conditions=_scene_move_conditions(side, '
                                                   '16))\n'
                                                   'if side == 0:\n'
                                                   '    return SceneControllerOutcome(frame, '
                                                   'discarded)\n'
                                                   "state_code = _ram(state, '8152').word()\n"
                                                   'frame = replace(frame, '
                                                   'conditions=_scene_compare_conditions(state_code, '
                                                   '2, 16))\n'
                                                   'if state_code != 2:\n'
                                                   "    hold = _ram(state, '813e').word()\n"
                                                   '    frame = replace(frame, '
                                                   'conditions=_scene_move_conditions(hold, '
                                                   '16))\n'
                                                   '    if hold != 0:\n'
                                                   '        return '
                                                   'SceneControllerOutcome(frame, discarded)\n'
                                                   '    state_code = _ram(state, '
                                                   "'8152').word()\n"
                                                   '    frame = replace(frame, '
                                                   'conditions=_scene_compare_conditions(state_code, '
                                                   '1, 16))\n'
                                                   '    if state_code == 1:\n'
                                                   '        return '
                                                   'SceneControllerOutcome(frame, discarded)\n'
                                                   "_ram(state, '8152').set_word(0, 0)\n"
                                                   'previous_timer = _ram(state, '
                                                   "'8154').word()\n"
                                                   'timer = u16(previous_timer - 1)\n'
                                                   "_ram(state, '8154').set_word(0, timer)\n"
                                                   'frame = replace(frame, '
                                                   'conditions=_scene_compare_conditions(previous_timer, '
                                                   '1, 16))\n'
                                                   'if not negative_word(timer):\n'
                                                   '    return SceneControllerOutcome(frame, '
                                                   'discarded)\n'
                                                   'while True:\n'
                                                   "    slot = u16(_ram(state, '8150').word() "
                                                   '+ 1)\n'
                                                   "    _ram(state, '8150').set_word(0, "
                                                   'slot)\n'
                                                   '    if slot >= 16:\n'
                                                   "        _ram(state, '8150').set_word(0, "
                                                   '0)\n'
                                                   '        category = u16(_ram(state, '
                                                   "'814e').word() + 1)\n"
                                                   "        _ram(state, '814e').set_word(0, "
                                                   'category)\n'
                                                   '        if category >= 4:\n'
                                                   '            _ram(state, '
                                                   "'814e').set_word(0, 0)\n"
                                                   '            side = u16(_ram(state, '
                                                   "'814c').word() + 1)\n"
                                                   '            _ram(state, '
                                                   "'814c').set_word(0, side)\n"
                                                   '            if side >= 3:\n'
                                                   '                _ram(state, '
                                                   "'814c').set_word(0, 0)\n"
                                                   '        break\n'
                                                   "    roster = _ram(state, '816a')\n"
                                                   "    if _ram(state, '814c').word() != 1:\n"
                                                   "        roster = _ram(state, '826a')\n"
                                                   '    offset = u16(_ram(state, '
                                                   "'8150').word() << 4)\n"
                                                   '    frame = replace(frame, '
                                                   'source=roster.cursor(), '
                                                   'x=replace_word(frame.x, offset))\n'
                                                   '    if not roster.byte(offset) & 128:\n'
                                                   '        continue\n'
                                                   '    kind = roster.word(offset) & 127\n'
                                                   '    frame = replace(frame, '
                                                   'x=replace_word(frame.x, kind))\n'
                                                   '    selected_class = _ram(state, '
                                                   "'814e').word()\n"
                                                   '    if kind == selected_class:\n'
                                                   '        break\n'
                                                   "_ram(state, '8154').set_word(0, 0)\n"
                                                   "category = _ram(state, '814e').word()\n"
                                                   'if category >= 2:\n'
                                                   "    _ram(state, '8154').set_word(0, 1)\n"
                                                   '    conditions = '
                                                   '_scene_move_conditions(1, 16)\n'
                                                   'else:\n'
                                                   '    conditions = '
                                                   '_scene_compare_conditions(category, 2, '
                                                   '16)\n'
                                                   'return '
                                                   'SceneControllerOutcome(replace(frame, '
                                                   'conditions=conditions), discarded)'},
 'initialize_scene_object_video_complete': {'signature': 'state: SceneState, context: '
                                                         'SceneControllerFrame',
                                            'returns': 'SceneControllerFrame',
                                            'flow': 'frame = '
                                                    'checked_controller_frame(context, '
                                                    'state)\n'
                                                    'from .business_scene import '
                                                    'write_vdp_swapped_byte_rle_stream_frame, '
                                                    'read_vdp_plane_rle_rows_frame\n'
                                                    'for command in (36610, 33328, 33584, '
                                                    '33799, 34152, 34560, 35584, 35969, '
                                                    '36149, 36610, 36881, 37268, 37376):\n'
                                                    '    state.write(12582916, 2, command)\n'
                                                    'for source_address, destination, '
                                                    'continuation in ((291812, 0, 252438), '
                                                    '(299752, 8192, 252452), (305570, 16384, '
                                                    '252466), (312748, 24576, 252480), '
                                                    '(319632, 32768, 252494)):\n'
                                                    '    frame = replace(frame, '
                                                    'source=state.table_at(source_address).cursor(), '
                                                    'x=replace_word(frame.x, destination), '
                                                    'conditions=_scene_move_conditions(destination, '
                                                    '16))\n'
                                                    '    frame = _scene_call(state, frame, '
                                                    'write_vdp_swapped_byte_rle_stream_frame, '
                                                    'continuation)\n'
                                                    'for directory_address, destination, '
                                                    'continuation in ((252620, 57344, '
                                                    '252528), (252636, 57408, 252562), '
                                                    '(252620, 61440, 252590), (252636, 61504, '
                                                    '252618)):\n'
                                                    '    variant = _ram(state, '
                                                    "'80db').byte()\n"
                                                    '    offset = u16(variant << 2)\n'
                                                    '    source = _read_pointer(state, '
                                                    'state.table_at(directory_address), '
                                                    'offset).cursor()\n'
                                                    '    frame = replace(frame, x=offset, '
                                                    'source=source, '
                                                    'destination=VideoPlaneAddress(destination), '
                                                    'extent=128, '
                                                    'conditions=_scene_move_conditions(128, '
                                                    '32))\n'
                                                    '    frame = _scene_call(state, frame, '
                                                    'read_vdp_plane_rle_rows_frame, '
                                                    'continuation)\n'
                                                    'return frame'},
 '_reset_object_action_controls': {'signature': 'state',
                                   'returns': None,
                                   'flow': "for name in ('814c', '814e', '8150', '8152', "
                                           "'8154', '8156', '8158', '815a', '815c', '815e', "
                                           "'8160', '8162', '8164', '8166', '8168'):\n"
                                           '    _ram(state, name).set_word(0, 0)'},
 'initialize_scene_object_roster_complete': {'signature': 'state: SceneState, context: '
                                                          'SceneControllerFrame',
                                             'returns': 'SceneControllerFrame',
                                             'flow': 'frame = '
                                                     'checked_controller_frame(context, '
                                                     'state)\n'
                                                     'from .business_scene import '
                                                     'sample_random_preserving_seed_frame\n'
                                                     'destination = _ram(state, '
                                                     "'816a').cursor()\n"
                                                     'for _ in descending_inclusive(255):\n'
                                                     '    destination.append_word(0)\n'
                                                     'frame = replace(frame, '
                                                     'x=replace_word(frame.x, 65535), '
                                                     'actor=destination, '
                                                     'conditions=_scene_move_conditions(0, '
                                                     '16))\n'
                                                     "if _ram(state, '80da').byte() == 1 or "
                                                     "_ram(state, '80da').byte() == 2:\n"
                                                     '    '
                                                     '_reset_object_action_controls(state)\n'
                                                     '    return replace(frame, '
                                                     'conditions=_scene_move_conditions(0, '
                                                     '16))\n'
                                                     "for name in ('80e8', '80f4', '80f6', "
                                                     "'80f8'):\n"
                                                     '    _ram(state, name).set_word(0, 0)\n'
                                                     "if _ram(state, '80e4').word() != 0:\n"
                                                     "    _ram(state, '80e8').set_word(0, 1)\n"
                                                     "    if _ram(state, '80e4').word() >= "
                                                     '100:\n'
                                                     "        if _ram(state, '80e4').word() < "
                                                     '1500:\n'
                                                     '            while True:\n'
                                                     '                frame = '
                                                     '_scene_call(state, frame, '
                                                     'sample_random_preserving_seed_frame, '
                                                     '268364)\n'
                                                     '                choice = low16(frame.x) '
                                                     '& 15\n'
                                                     '                frame = replace(frame, '
                                                     'x=replace_word(frame.x, choice))\n'
                                                     '                if choice <= 9:\n'
                                                     '                    break\n'
                                                     '            frame = replace(frame, '
                                                     'x=replace_word(frame.x, u16(choice + '
                                                     '1)))\n'
                                                     '            _ram(state, '
                                                     "'80e8').set_word(0, low16(frame.x))\n"
                                                     "        elif _ram(state, '80e4').word() "
                                                     '< 5000:\n'
                                                     '            while True:\n'
                                                     '                frame = '
                                                     '_scene_call(state, frame, '
                                                     'sample_random_preserving_seed_frame, '
                                                     '268396)\n'
                                                     '                choice = low16(frame.x) '
                                                     '& 15\n'
                                                     '                frame = replace(frame, '
                                                     'x=replace_word(frame.x, choice))\n'
                                                     '                if choice <= 5:\n'
                                                     '                    break\n'
                                                     '            frame = replace(frame, '
                                                     'x=replace_word(frame.x, u16(choice + '
                                                     '5)))\n'
                                                     '            _ram(state, '
                                                     "'80e8').set_word(0, low16(frame.x))\n"
                                                     '        else:\n'
                                                     '            _ram(state, '
                                                     "'80e8').set_word(0, 15)\n"
                                                     '            if _ram(state, '
                                                     "'80e4').word() < 10000:\n"
                                                     '                while True:\n'
                                                     '                    frame = '
                                                     '_scene_call(state, frame, '
                                                     'sample_random_preserving_seed_frame, '
                                                     '268434)\n'
                                                     '                    choice = '
                                                     'low16(frame.x) & 15\n'
                                                     '                    frame = '
                                                     'replace(frame, x=replace_word(frame.x, '
                                                     'choice))\n'
                                                     '                    if choice <= 5:\n'
                                                     '                        break\n'
                                                     '                frame = replace(frame, '
                                                     'x=replace_word(frame.x, u16(choice + '
                                                     '10)))\n'
                                                     '                _ram(state, '
                                                     "'80e8').set_word(0, low16(frame.x))\n"
                                                     '    frame = _scene_call(state, frame, '
                                                     'normalize_object_squad_size_complete, '
                                                     '268460)\n'
                                                     '    first, second = (0, 2)\n'
                                                     '    for threshold, first_count, '
                                                     'second_count in ((100, 0, 2), (200, 1, '
                                                     '3), (300, 3, 4), (400, 5, 5), (500, 6, '
                                                     '6), (600, 7, 7)):\n'
                                                     '        first, second = (first_count, '
                                                     'second_count)\n'
                                                     "        if _ram(state, '8110').word() "
                                                     '<= threshold:\n'
                                                     '            break\n'
                                                     '    else:\n'
                                                     '        first, second = (8, 8)\n'
                                                     '    frame = replace(frame, x=first, '
                                                     'y=second)\n'
                                                     "    for name in ('80f4', '80f6', "
                                                     "'80f8'):\n"
                                                     '        _ram(state, name).set_word(0, '
                                                     '0)\n'
                                                     '    remainder = u16(_ram(state, '
                                                     "'80e8').word() - first)\n"
                                                     '    frame = replace(frame, '
                                                     'attributes=replace_word(frame.attributes, '
                                                     'remainder))\n'
                                                     '    if negative_word(remainder):\n'
                                                     "        _ram(state, '80f4').set_word(0, "
                                                     "_ram(state, '80e8').word())\n"
                                                     '    else:\n'
                                                     "        _ram(state, '80f4').set_word(0, "
                                                     'first)\n'
                                                     "        _ram(state, '80f6').set_word(0, "
                                                     'remainder)\n'
                                                     '        remainder = u16(remainder - '
                                                     'second)\n'
                                                     '        frame = replace(frame, '
                                                     'attributes=replace_word(frame.attributes, '
                                                     'remainder))\n'
                                                     '        if not '
                                                     'negative_word(remainder):\n'
                                                     '            _ram(state, '
                                                     "'80f6').set_word(0, second)\n"
                                                     '            _ram(state, '
                                                     "'80f8').set_word(0, remainder)\n"
                                                     "    if _ram(state, '80db').byte() == "
                                                     '3:\n'
                                                     "        _ram(state, '80f4').set_word(0, "
                                                     '0)\n'
                                                     "        _ram(state, '80f6').set_word(0, "
                                                     "_ram(state, '80e8').word())\n"
                                                     "        _ram(state, '80f8').set_word(0, "
                                                     '0)\n'
                                                     'while True:\n'
                                                     '    frame = _scene_call(state, frame, '
                                                     'sample_random_preserving_seed_frame, '
                                                     '268622)\n'
                                                     '    choice = low16(frame.x) & 7\n'
                                                     '    frame = replace(frame, '
                                                     'x=replace_word(frame.x, choice))\n'
                                                     '    if choice <= 4:\n'
                                                     '        break\n'
                                                     "    if _ram(state, '80db').byte() == "
                                                     '3:\n'
                                                     "        _ram(state, '80f4').set_word(0, "
                                                     '0)\n'
                                                     "        _ram(state, '80f6').set_word(0, "
                                                     "_ram(state, '80e8').word())\n"
                                                     "        _ram(state, '80f8').set_word(0, "
                                                     '0)\n'
                                                     "_ram(state, '814a').set_word(0, "
                                                     'choice)\n'
                                                     'layout = _read_pointer(state, '
                                                     'state.table_at(268888), u16(choice << '
                                                     '2)).cursor()\n'
                                                     "first = _ram(state, '80f4').word()\n"
                                                     "second = _ram(state, '80f6').word()\n"
                                                     "third = _ram(state, '80f8').word()\n"
                                                     "actor = _ram(state, '816a')\n"
                                                     'frame = replace(frame, '
                                                     'x=replace_word(frame.x, first), '
                                                     'y=replace_word(frame.y, second), '
                                                     'attributes=replace_word(frame.attributes, '
                                                     'third), palette=0, '
                                                     'source=state.table_at(268888).cursor(), '
                                                     'traversal=layout, actor=actor)\n'
                                                     'leader = True\n'
                                                     'object_count = 0\n'
                                                     'while True:\n'
                                                     '    if leader:\n'
                                                     '        kind = 32771\n'
                                                     '        leader = False\n'
                                                     '    elif first:\n'
                                                     '        kind, first = (32770, u16(first '
                                                     '- 1))\n'
                                                     '    elif second:\n'
                                                     '        kind, second = (32769, '
                                                     'u16(second - 1))\n'
                                                     '    elif third:\n'
                                                     '        kind, third = (32768, u16(third '
                                                     '- 1))\n'
                                                     '    else:\n'
                                                     '        break\n'
                                                     '    actor.set_word(0, '
                                                     'layout.next_word(), 2)\n'
                                                     '    actor.set_word(0, '
                                                     'layout.next_word(), 4)\n'
                                                     '    actor.set_word(0, kind)\n'
                                                     '    object_count = u16(object_count + '
                                                     '1)\n'
                                                     '    actor = actor.advance(16)\n'
                                                     '    frame = replace(frame, '
                                                     'x=replace_word(frame.x, first), '
                                                     'y=replace_word(frame.y, second), '
                                                     'attributes=replace_word(frame.attributes, '
                                                     'third), '
                                                     'palette=replace_word(frame.palette, '
                                                     'object_count), actor=actor)\n'
                                                     "quality = _ram(state, '8104').word()\n"
                                                     "factor = _ram(state, '8100').word()\n"
                                                     'packed = divu_retained(u32(factor * '
                                                     'quality), 100)\n'
                                                     "remainder = _ram(state, '80f0').word()\n"
                                                     "actor = _ram(state, '817a')\n"
                                                     'for _ in descending_inclusive(14):\n'
                                                     '    actor.set_word(0, low16(packed), '
                                                     '12)\n'
                                                     '    actor.set_word(0, _ram(state, '
                                                     "'80ec').word(), 14)\n"
                                                     '    if remainder != 0:\n'
                                                     '        remainder = u16(remainder - 1)\n'
                                                     '        actor.set_word(0, '
                                                     'u16(actor.word(0, 14) + 1), 14)\n'
                                                     '    actor = actor.advance(16)\n'
                                                     "strength = _ram(state, '8104').word()\n"
                                                     'strength = u16(strength + _ram(state, '
                                                     "'8108').word())\n"
                                                     "_ram(state, '8176').set_word(0, "
                                                     'strength)\n'
                                                     "_ram(state, '8178').set_word(0, "
                                                     "_ram(state, '810c').word())\n"
                                                     '_reset_object_action_controls(state)\n'
                                                     'return replace(frame, '
                                                     'x=replace_word(frame.x, strength), '
                                                     'y=packed, '
                                                     'attributes=replace_word(frame.attributes, '
                                                     'remainder), actor=actor, '
                                                     'conditions=_scene_move_conditions(0, '
                                                     '16))'},
 '_scene_video_command': {'signature': 'state, retained',
                          'returns': None,
                          'flow': 'carrier = replace_word(retained, _ram(state, '
                                  "'f606').word())\n"
                                  'carrier = replace_byte(carrier, low8(carrier) & 191)\n'
                                  'state.write(12582916, 2, low16(carrier))\n'
                                  'return carrier'},
 'cycle_special_scene_palette': {'signature': 'state, context=None',
                                 'returns': None,
                                 'flow': 'cycle_special_scene_palette_complete(state, '
                                         'checked_controller_frame(context, state))'},
 'clear_scene_object_label_plane': {'signature': 'state, context=None',
                                    'returns': None,
                                    'flow': 'clear_scene_object_label_plane_complete(state, '
                                            'checked_controller_frame(context, state))'},
 'offset_scene_object_position': {'signature': 'state, actor, offset, context=None',
                                  'returns': None,
                                  'flow': 'checked_table(actor, state)\n'
                                          'checked_context(offset, ObjectPositionOffset, '
                                          'state)\n'
                                          'frame = checked_controller_frame(context, state)\n'
                                          'offset_scene_object_position_complete(state, '
                                          'replace(frame, actor=actor, '
                                          'x=replace_word(frame.x, offset.horizontal), '
                                          'y=replace_word(frame.y, offset.vertical)))'},
 'probe_scene_object_overlap': {'signature': 'state, actor, offset, context=None',
                                'returns': None,
                                'flow': 'checked_table(actor, state)\n'
                                        'checked_context(offset, ObjectPositionOffset, '
                                        'state)\n'
                                        'frame = checked_controller_frame(context, state)\n'
                                        'actual = probe_scene_object_overlap_complete(state, '
                                        'replace(frame, actor=actor, x=replace_word(frame.x, '
                                        'offset.horizontal), y=replace_word(frame.y, '
                                        'offset.vertical)))\n'
                                        'return ObjectOverlapOutcome(low16(actual.x) != 0, '
                                        'actual.traversal)'},
 'probe_opposing_object_overlap': {'signature': 'state, actor, offset, context=None',
                                   'returns': None,
                                   'flow': 'checked_table(actor, state)\n'
                                           'checked_context(offset, ObjectPositionOffset, '
                                           'state)\n'
                                           'frame = checked_controller_frame(context, state)\n'
                                           'actual = '
                                           'probe_opposing_object_overlap_complete(state, '
                                           'replace(frame, actor=actor, '
                                           'x=replace_word(frame.x, offset.horizontal), '
                                           'y=replace_word(frame.y, offset.vertical)))\n'
                                           'return ObjectOverlapOutcome(low16(actual.x) != 0, '
                                           'actual.traversal)'},
 'rebuild_depth_sorted_object_queue': {'signature': 'state, context=None',
                                       'returns': None,
                                       'flow': 'return '
                                               'rebuild_depth_sorted_object_queue_complete(state, '
                                               'checked_controller_frame(context, state))'},
 'append_scene_center_marker': {'signature': 'state, context',
                                'returns': None,
                                'flow': 'return '
                                        '_scene_projection(append_scene_center_marker_complete(state, '
                                        'checked_controller_frame(context, state)))'},
 'draw_active_scene_object': {'signature': 'state, context',
                              'returns': None,
                              'flow': 'checked_context(context, SceneObjectContext, state)\n'
                                      'frame = checked_controller_frame(context.frame, '
                                      'state)\n'
                                      'actual = draw_active_scene_object_complete(state, '
                                      'replace(frame, actor=context.actor))\n'
                                      'return _scene_projection(actual.frame)'},
 'plan_scene_object_action': {'signature': 'state, actor, continuation, context=None',
                              'returns': None,
                              'flow': 'checked_table(actor, state)\n'
                                      'if type(continuation) is not StackContinuation:\n'
                                      "    raise ValueError('explicit legacy continuation "
                                      "required')\n"
                                      'frame = checked_controller_frame(context, state)\n'
                                      'actual = plan_scene_object_action_complete(state, '
                                      'replace(frame, actor=actor))\n'
                                      'return ActionPlanOutcome(actual.discarded_continuation '
                                      'is not None, actual.frame.x)'},
 'update_selected_object_action': {'signature': 'state, context',
                                   'returns': None,
                                   'flow': 'checked_context(context, SceneObjectContext, '
                                           'state)\n'
                                           'actual = '
                                           'update_selected_object_action_complete(state, '
                                           'replace(checked_controller_frame(context.frame, '
                                           'state), actor=context.actor))\n'
                                           'return _scene_projection(actual.frame)'},
 'advance_scene_object_actions': {'signature': 'state, context',
                                  'returns': None,
                                  'flow': 'actual = '
                                          'advance_scene_object_actions_complete(state, '
                                          'checked_controller_frame(context, state))\n'
                                          'return _scene_projection(actual.frame)'},
 'initialize_scene_object_video': {'signature': 'state, context',
                                   'returns': None,
                                   'flow': 'return '
                                           '_scene_projection(initialize_scene_object_video_complete(state, '
                                           'checked_controller_frame(context, state)))'},
 'initialize_scene_object_roster': {'signature': 'state, context',
                                    'returns': None,
                                    'flow': 'return '
                                            '_scene_projection(initialize_scene_object_roster_complete(state, '
                                            'checked_controller_frame(context, state)))'},
 'dispatch_scene_object_phase': {'signature': 'state, context',
                                 'returns': None,
                                 'flow': 'actual = '
                                         'dispatch_scene_object_phase_complete(state, '
                                         'checked_controller_frame(context, state))\n'
                                         'return _scene_projection(actual.frame)'},
 '_clear_controller_sprite_plane': {'signature': 'state, frame',
                                    'returns': None,
                                    'flow': 'from .business_reuse import '
                                            'clear_video_sprite_plane\n'
                                            'actual = clear_video_sprite_plane(state, '
                                            'frame.row_count)\n'
                                            'return replace(frame, row_count=actual.response, '
                                            'layer=actual.variation, '
                                            'actor=actual.destination, '
                                            'conditions=_scene_move_conditions(0, 32))'},
 '_copy_controller_palette': {'signature': 'state, frame',
                              'returns': None,
                              'flow': 'from .business_scene import '
                                      'copy_scene_palette_variant_complete\n'
                                      'actual = copy_scene_palette_variant_complete(state, '
                                      'frame.x, frame.layer)\n'
                                      'return replace(frame, x=actual.index_carrier, '
                                      'layer=actual.count_carrier, '
                                      'destination=actual.directory, directory=actual.source, '
                                      'parameters=actual.destination, '
                                      'conditions=SceneControllerConditions(actual.carry, '
                                      'actual.zero, actual.negative, actual.overflow))'},
 '_enqueue_controller_sound': {'signature': 'state, frame',
                               'returns': None,
                               'flow': 'from .business_reuse import enqueue_sound_command\n'
                                       'enqueue_sound_command(state, low8(frame.x))\n'
                                       'return replace(frame, '
                                       'conditions=_scene_move_conditions(0, 16))'},
 '_wait_controller_frame_ack': {'signature': 'state, frame',
                                'returns': None,
                                'flow': 'from .business_reuse import '
                                        'wait_for_scene_sound_byte\n'
                                        'wait_for_scene_sound_byte(state)\n'
                                        'return replace(frame, '
                                        'conditions=_scene_move_conditions(0, 8))'},
 'integrate_scene_coordinates_complete': {'signature': 'state, frame',
                                          'returns': None,
                                          'flow': 'frame = checked_controller_frame(frame, '
                                                  'state)\n'
                                                  'actual = '
                                                  'integrate_scene_coordinates(state)\n'
                                                  'return replace(frame, '
                                                  'x=actual.position_carrier, '
                                                  'y=actual.velocity_carrier, '
                                                  'conditions=_scene_move_conditions(low16(actual.position_carrier), '
                                                  '16))'},
 'run_scene_object_controller_complete': {'signature': 'state: SceneState, context: '
                                                       'SceneControllerFrame',
                                          'returns': 'SceneControllerOutcome',
                                          'flow': 'frame = checked_controller_frame(context, '
                                                  'state)\n'
                                                  'from .business_scene import '
                                                  'begin_scene_palette_darken_frame, '
                                                  'snapshot_and_clear_scene_palette_frame, '
                                                  'advance_scene_palette_fade_frame, '
                                                  'finish_actor_sprite_chains_frame\n'
                                                  'discarded = None\n'
                                                  'while True:\n'
                                                  '    state.set_status_word(9984)\n'
                                                  '    command = _scene_video_command(state, '
                                                  'frame.x)\n'
                                                  '    frame = replace(frame, x=command, '
                                                  'conditions=_scene_move_conditions(low16(command), '
                                                  '16))\n'
                                                  '    frame = _scene_call(state, frame, '
                                                  '_clear_controller_sprite_plane, 251500)\n'
                                                  "    _ram(state, 'f6c4').set_word(0, 2)\n"
                                                  '    frame = _scene_call(state, frame, '
                                                  'initialize_scene_object_video_complete, '
                                                  '251510)\n'
                                                  "    variant = _ram(state, '80db').byte()\n"
                                                  '    frame = replace(frame, x=variant, '
                                                  'conditions=_scene_move_conditions(variant, '
                                                  '8))\n'
                                                  '    frame = _scene_call(state, frame, '
                                                  '_copy_controller_palette, 251520)\n'
                                                  "    for name in ('80ca', '80cc', '80ce', "
                                                  "'80d0'):\n"
                                                  '        _ram(state, name).set_word(0, '
                                                  '65535)\n'
                                                  '    frame = replace(frame, x=1, '
                                                  'conditions=_scene_move_conditions(1, 32))\n'
                                                  '    frame = _scene_call(state, frame, '
                                                  'begin_scene_palette_darken_frame, 251550)\n'
                                                  '    frame = _scene_call(state, frame, '
                                                  'snapshot_and_clear_scene_palette_frame, '
                                                  '251554)\n'
                                                  "    phase = _ram(state, '813a').word()\n"
                                                  '    frame = replace(frame, '
                                                  'conditions=_scene_compare_conditions(phase, '
                                                  '3, 16))\n'
                                                  '    if phase == 3:\n'
                                                  '        frame = _scene_call(state, frame, '
                                                  'clear_scene_object_label_plane_complete, '
                                                  '251568)\n'
                                                  "        _ram(state, '813a').set_word(0, "
                                                  '0)\n'
                                                  "        _ram(state, '813c').set_word(0, "
                                                  '6)\n'
                                                  "        _ram(state, '813e').set_word(0, "
                                                  '0)\n'
                                                  '        reversed_sides = _ram(state, '
                                                  "'8124').word() != 0\n"
                                                  "        first_destination = '8278' if "
                                                  "reversed_sides else '8178'\n"
                                                  "        second_destination = '8178' if "
                                                  "reversed_sides else '8278'\n"
                                                  '        _ram(state, '
                                                  'first_destination).set_word(0, _ram(state, '
                                                  "'706c').word())\n"
                                                  '        _ram(state, '
                                                  'second_destination).set_word(0, '
                                                  "_ram(state, '70bc').word())\n"
                                                  '        first_won = _ram(state, '
                                                  "'70f0').byte() == 1\n"
                                                  "        destination = '8130' if first_won "
                                                  "!= reversed_sides else '8138'\n"
                                                  '        _ram(state, '
                                                  'destination).set_word(0, 6)\n'
                                                  '        frame = replace(frame, '
                                                  'conditions=_scene_move_conditions(6, 16))\n'
                                                  '    else:\n'
                                                  "        _ram(state, '8020').set_word(0, "
                                                  '0)\n'
                                                  "        _ram(state, '8024').set_long(0, "
                                                  '0)\n'
                                                  '        fields = _ram(state, '
                                                  "'812a').cursor()\n"
                                                  '        for _ in '
                                                  'descending_inclusive(263):\n'
                                                  '            fields.append_word(0)\n'
                                                  '        frame = replace(frame, '
                                                  'x=replace_word(frame.x, 65535), '
                                                  'source=fields)\n'
                                                  "        for name in ('812a', '812c', "
                                                  "'812e', '8130', '8132', '8134', '8136', "
                                                  "'8138'):\n"
                                                  '            _ram(state, name).set_word(0, '
                                                  '5)\n'
                                                  "        _ram(state, '813a').set_word(0, "
                                                  '9)\n'
                                                  "        _ram(state, '813c').set_word(0, "
                                                  '0)\n'
                                                  '        frame = replace(frame, '
                                                  'conditions=_scene_move_conditions(0, 16))\n'
                                                  '    if phase != 3:\n'
                                                  '        frame = _scene_call(state, frame, '
                                                  'initialize_scene_object_roster_complete, '
                                                  '251870)\n'
                                                  '    command = replace_word(frame.x, 142)\n'
                                                  '    frame = replace(frame, x=command, '
                                                  'conditions=_scene_move_conditions(142, '
                                                  '16))\n'
                                                  '    frame = _scene_call(state, frame, '
                                                  '_enqueue_controller_sound, 251882)\n'
                                                  '    state.set_status_word(9472)\n'
                                                  '    while True:\n'
                                                  "        _ram(state, 'f612').set_word(0, "
                                                  '1280)\n'
                                                  '        frame = _scene_call(state, frame, '
                                                  '_wait_controller_frame_ack, 251898)\n'
                                                  "        _ram(state, 'f612').set_word(0, "
                                                  '0)\n'
                                                  '        frame = replace(frame, '
                                                  'conditions=_scene_move_conditions(0, 16))\n'
                                                  '        frame = _scene_call(state, frame, '
                                                  'append_scene_center_marker_complete, '
                                                  '251906)\n'
                                                  '        frame = _scene_call(state, frame, '
                                                  'cycle_special_scene_palette_complete, '
                                                  '251910)\n'
                                                  '        frame = _scene_call(state, frame, '
                                                  'advance_scene_palette_fade_frame, 251914)\n'
                                                  '        outcome = '
                                                  '_scene_action_call(state, frame, '
                                                  'dispatch_scene_object_phase_complete, '
                                                  '251918)\n'
                                                  '        frame = outcome.frame\n'
                                                  '        if outcome.discarded_continuation '
                                                  'is not None:\n'
                                                  '            discarded = '
                                                  'outcome.discarded_continuation\n'
                                                  '        outcome = '
                                                  '_scene_action_call(state, frame, '
                                                  'advance_scene_object_actions_complete, '
                                                  '251924)\n'
                                                  '        frame = outcome.frame\n'
                                                  '        if outcome.discarded_continuation '
                                                  'is not None:\n'
                                                  '            discarded = '
                                                  'outcome.discarded_continuation\n'
                                                  '        frame = _scene_call(state, frame, '
                                                  'finish_actor_sprite_chains_frame, 251930)\n'
                                                  '        frame = _scene_call(state, frame, '
                                                  'integrate_scene_coordinates_complete, '
                                                  '251934)\n'
                                                  '        terminal = False\n'
                                                  "        if _ram(state, '813a').word() == "
                                                  '3:\n'
                                                  "            if _ram(state, '813c').word() "
                                                  '== 3:\n'
                                                  '                _ram(state, '
                                                  "'8114').set_word(0, 1)\n"
                                                  '                terminal = True\n'
                                                  '        if not terminal and _ram(state, '
                                                  "'813a').word() == 4:\n"
                                                  "            if _ram(state, '813c').word() "
                                                  '== 3:\n'
                                                  '                _ram(state, '
                                                  "'8114').set_word(0, 0)\n"
                                                  '                terminal = True\n'
                                                  '        if not terminal and _ram(state, '
                                                  "'813a').word() == 5:\n"
                                                  "            if _ram(state, '813c').word() "
                                                  '== 3:\n'
                                                  '                terminal = True\n'
                                                  '        if not terminal and _ram(state, '
                                                  "'813a').word() == 6:\n"
                                                  "            if _ram(state, '813c').word() "
                                                  '== 4:\n'
                                                  '                _ram(state, '
                                                  "'8114').set_word(0, 6)\n"
                                                  '                terminal = True\n'
                                                  '        if terminal:\n'
                                                  '            state.set_status_word(9984)\n'
                                                  '            command = '
                                                  '_scene_video_command(state, frame.x)\n'
                                                  '            return '
                                                  'SceneControllerOutcome(replace(frame, '
                                                  'x=command, '
                                                  'conditions=_scene_move_conditions(low16(command), '
                                                  '16)), discarded)\n'
                                                  '        command = replace_byte(frame.x, '
                                                  "_ram(state, 'f602').byte())\n"
                                                  '        command = replace_byte(command, '
                                                  'low8(command) & 240)\n'
                                                  '        frame = replace(frame, x=command, '
                                                  'conditions=_scene_compare_conditions(low8(command), '
                                                  '240, 8))\n'
                                                  '        if low8(command) != 240:\n'
                                                  '            continue\n'
                                                  "        if _ram(state, '80db').byte() < "
                                                  '3:\n'
                                                  '            _ram(state, '
                                                  "'80db').set_byte(0, u8(_ram(state, "
                                                  "'80db').byte() + 1))\n"
                                                  '        break'},
 'run_scene_object_controller': {'signature': 'state, context',
                                 'returns': None,
                                 'flow': 'return '
                                         '_scene_projection(run_scene_object_controller_complete(state, '
                                         'checked_controller_frame(context, state)).frame)'}}

def _lower_distribute_secondary_city_battle_progress(emitter,rules):
    _SOURCE_LOWERERS['distribute_secondary_city_battle_progress'](emitter,rules)

def _lower_append_scene_center_marker(emitter,rules):
    _SOURCE_LOWERERS['append_scene_center_marker'](emitter,rules)

def _lower_run_scene_object_controller(emitter,rules):
    _SOURCE_LOWERERS['run_scene_object_controller'](emitter,rules)

def _lower_integrate_scene_coordinates(emitter,rules):
    _SOURCE_LOWERERS['integrate_scene_coordinates'](emitter,rules)

def _lower_initialize_scene_object_video(emitter,rules):
    _SOURCE_LOWERERS['initialize_scene_object_video'](emitter,rules)

def _lower_dispatch_scene_object_phase(emitter,rules):
    _SOURCE_LOWERERS['dispatch_scene_object_phase'](emitter,rules)

def _lower_normalize_object_squad_size(emitter,rules):
    _SOURCE_LOWERERS['normalize_object_squad_size'](emitter,rules)

def _lower_cycle_special_scene_palette(emitter,rules):
    _SOURCE_LOWERERS['cycle_special_scene_palette'](emitter,rules)

def _lower_clear_scene_object_label_plane(emitter,rules):
    _SOURCE_LOWERERS['clear_scene_object_label_plane'](emitter,rules)

def _lower_advance_scene_object_actions(emitter,rules):
    _SOURCE_LOWERERS['advance_scene_object_actions'](emitter,rules)

def _lower_rebuild_depth_sorted_object_queue(emitter,rules):
    _SOURCE_LOWERERS['rebuild_depth_sorted_object_queue'](emitter,rules)

def _lower_update_selected_object_action(emitter,rules):
    _SOURCE_LOWERERS['update_selected_object_action'](emitter,rules)

def _lower_read_object_action_mode(emitter,rules):
    _SOURCE_LOWERERS['read_object_action_mode'](emitter,rules)

def _lower_probe_scene_object_overlap(emitter,rules):
    _SOURCE_LOWERERS['probe_scene_object_overlap'](emitter,rules)

def _lower_offset_scene_object_position(emitter,rules):
    _SOURCE_LOWERERS['offset_scene_object_position'](emitter,rules)

def _lower_plan_scene_object_action(emitter,rules):
    _SOURCE_LOWERERS['plan_scene_object_action'](emitter,rules)

def _lower_probe_opposing_object_overlap(emitter,rules):
    _SOURCE_LOWERERS['probe_opposing_object_overlap'](emitter,rules)

def _lower_initialize_scene_object_roster(emitter,rules):
    _SOURCE_LOWERERS['initialize_scene_object_roster'](emitter,rules)

LOWERERS={
    'distribute_secondary_city_battle_progress':_lower_distribute_secondary_city_battle_progress,
    'append_scene_center_marker':_lower_append_scene_center_marker,
    'run_scene_object_controller':_lower_run_scene_object_controller,
    'integrate_scene_coordinates':_lower_integrate_scene_coordinates,
    'initialize_scene_object_video':_lower_initialize_scene_object_video,
    'dispatch_scene_object_phase':_lower_dispatch_scene_object_phase,
    'normalize_object_squad_size':_lower_normalize_object_squad_size,
    'cycle_special_scene_palette':_lower_cycle_special_scene_palette,
    'clear_scene_object_label_plane':_lower_clear_scene_object_label_plane,
    'advance_scene_object_actions':_lower_advance_scene_object_actions,
    'rebuild_depth_sorted_object_queue':_lower_rebuild_depth_sorted_object_queue,
    'update_selected_object_action':_lower_update_selected_object_action,
    'read_object_action_mode':_lower_read_object_action_mode,
    'probe_scene_object_overlap':_lower_probe_scene_object_overlap,
    'offset_scene_object_position':_lower_offset_scene_object_position,
    'plan_scene_object_action':_lower_plan_scene_object_action,
    'probe_opposing_object_overlap':_lower_probe_opposing_object_overlap,
    'initialize_scene_object_roster':_lower_initialize_scene_object_roster,
}

def compile_objects(source):
    records, policy = admit_policy_source(
        source, DECLARATIONS, APPROVED,
        role_specs=ROLE_SPECS, rule_builders=(owner_rules,),
        bindings=OBJECTS_BINDINGS, grammar='objects-policy-path-roles-v1',
    )
    if set(policy['owner_rules']) != {binding.name for binding in OBJECTS_BINDINGS}:
        raise CompileError('the complete objects family needs one policy authority per owner')
    sole_object_fields = {name:records[name]['effects'] for name in ('_scene_controller_entry_fields', '_scene_controller_legacy_fields', '_scene_object_call_fields', '_scene_object_video_command_fields', 'initialize_scene_object_video_fields', 'run_scene_object_controller_fields')}
    for owner in ('run_scene_object_controller', 'initialize_scene_object_video'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_object_fields=sole_object_fields)
    sole_object_roster_fields = {name:records[name]['effects'] for name in ('_normalize_object_squad_fields', '_object_adjust_word_fields', '_object_clear_word_fields', '_object_count_draw_fields', '_reset_object_action_controls_fields', '_scene_object_call_fields', 'clear_scene_object_label_plane_fields', 'initialize_scene_object_roster_fields', '_initialize_scene_object_roster_tail_fields', 'initialize_scene_object_roster_after_mode_check_fields', 'normalize_object_squad_size_fields')}
    for owner in ('initialize_scene_object_roster', 'normalize_object_squad_size', 'clear_scene_object_label_plane'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_object_roster_fields=sole_object_roster_fields)
    sole_object_render_fields = {name:records[name]['effects'] for name in ('_append_object_sprite_fields', '_object_shift_velocity_fields', '_object_shift_word_right_fields', '_scene_object_call_fields', 'append_scene_center_marker_fields', 'cycle_special_scene_palette_fields', 'draw_active_scene_object_fields', 'integrate_scene_coordinates_fields')}
    for owner in ('append_scene_center_marker', 'integrate_scene_coordinates', 'cycle_special_scene_palette'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_object_render_fields=sole_object_render_fields)
    sole_object_action_fields = {name:records[name]['effects'] for name in ('_scene_object_call_fields', 'advance_scene_object_actions_fields', 'dispatch_scene_object_phase_fields', 'offset_scene_object_position_fields', 'probe_opposing_object_overlap_fields', 'probe_scene_object_overlap_fields', 'read_object_action_mode_fields', 'rebuild_depth_sorted_object_queue_fields', 'update_selected_object_action_fields')}
    for owner in ('dispatch_scene_object_phase', 'advance_scene_object_actions', 'rebuild_depth_sorted_object_queue', 'update_selected_object_action', 'read_object_action_mode', 'probe_scene_object_overlap', 'offset_scene_object_position', 'probe_opposing_object_overlap'):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_object_action_fields=sole_object_action_fields)
    sole_object_planner_fields = {name:records[name]['effects'] for name in ('_object_action_mode_slot_fields', '_object_planner_discard_fields', '_object_planner_finish_fields', '_scene_object_call_fields', '_scene_object_plan_call_fields', 'plan_scene_object_action_fields', 'read_object_action_mode_fields', 'update_selected_object_action_fields')}
    for owner in ('plan_scene_object_action',):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_object_planner_fields=sole_object_planner_fields)
    sole_motion_dispatch_fields = {name:records[name]['effects'] for name in ('update_selected_object_action_fields',)}
    for owner in ('update_selected_object_action',):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_motion_dispatch_fields=sole_motion_dispatch_fields)
    sole_main_stage_fields = {name:records[name]['effects'] for name in ('dispatch_scene_object_phase_fields',)}
    for owner in ('dispatch_scene_object_phase',):
        records[owner]['effects'] = dict(previous_fields=records[owner]['effects'],sole_main_stage_fields=sole_main_stage_fields)
    compiled = lower_declared(records, OBJECTS_BINDINGS, LOWERERS)
    compiled['source_policy'] = policy
    return compiled

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('contexts_scene',set()).update({'SceneRefreshMemory', 'FirstDeploymentFrame'})
APPROVED.setdefault('business_battle',set()).update({'_presentation_call_fields'})
APPROVED.setdefault('contexts_battle',set()).update({'BattlePresentationMemory'})
APPROVED.setdefault('business_services',set()).update({'clear_video_sprite_plane_fields', 'enqueue_sound_command_fields', 'wait_for_scene_sound_byte_fields'})
APPROVED.setdefault('business_scene',set()).update({'_scene_render_compare', '_scene_render_asl_word'})
APPROVED.setdefault('business_movement_support',set()).update({'_movement_binary_flags'})
DECLARATIONS.update({'_scene_controller_entry_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                                 'target: Long, defines_status: bool=False',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'if type(memory) is not SceneRefreshMemory or type(frame) is not '
                                            'FirstDeploymentFrame:\n'
                                            "    raise ValueError('existing Scene memory and actual full "
                                            "fields required')\n"
                                            'frame.validate(memory.state, False)\n'
                                            'if frame.stack_cursor is None or any((value is None for value '
                                            'in (frame.target_x, frame.target_y, frame.unit, frame.count, '
                                            'frame.distance, frame.offset_x, frame.offset_y, frame.choice, '
                                            'frame.roster, frame.candidates, frame.controller, frame.scan, '
                                            'frame.opponent, frame.scratch, frame.auxiliary))):\n'
                                            '    raise SceneRefreshBoundary(target, frame, None)\n'
                                            'if defines_status:\n'
                                            '    frame = memory.status_word(frame, 9984)\n'
                                            'elif frame.status is None:\n'
                                            '    raise SceneRefreshBoundary(target, frame, None)\n'
                                            'return memory.frame(frame)'},
 '_scene_controller_legacy_fields': {'signature': 'state, context', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = checked_controller_frame(context, state)\nmemory = SceneRefreshMemory(state)\ndestination = memory.cursor_at(frame.destination.carrier) if type(frame.destination) is VideoPlaneAddress else frame.destination\ndirectory = frame.directory.cursor() if type(frame.directory) is Table else frame.directory\nparameters = frame.parameters.cursor() if type(frame.parameters) is Table else frame.parameters\nlimits = frame.limits.cursor() if type(frame.limits) is Table else frame.limits\nactor = frame.actor.cursor() if type(frame.actor) is Table else frame.actor\nreturn FirstDeploymentFrame(frame.x, frame.y, frame.attributes, frame.palette, frame.tile, frame.extent, frame.row_count, frame.layer, frame.source, destination, directory, parameters, limits, frame.traversal, actor, frame.stack, None)'},
 '_scene_controller_legacy_projection': {'signature': 'state, frame: FirstDeploymentFrame',
                                         'returns': 'SceneControllerFrame',
                                         'flow': 'SceneRefreshMemory(state).frame(frame)\n'
                                                 'conditions = SceneControllerConditions(bool(frame.status & '
                                                 '1), bool(frame.status & 4), bool(frame.status & 8), '
                                                 'bool(frame.status & 2))\n'
                                                 'return SceneControllerFrame(frame.target_x, '
                                                 'frame.target_y, frame.unit, frame.count, frame.distance, '
                                                 'frame.offset_x, frame.offset_y, frame.choice, '
                                                 'frame.roster, frame.candidates, frame.controller, '
                                                 'frame.scan, frame.opponent, frame.scratch, '
                                                 'frame.auxiliary, frame.stack_cursor, conditions)'},
 '_scene_object_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                            'target: Long, continuation: Long',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'from ..high_level_gameplay_flow.business_battle import '
                                       '_presentation_call_fields\n'
                                       'from ..high_level_gameplay_flow.contexts_battle import '
                                       'BattlePresentationMemory\n'
                                       'if (target, continuation) not in ((26830, 251500), (252320, 251510), '
                                       '(240532, 251520), (240160, 251550), (240266, 251554), (262940, '
                                       '251568), (268278, 251870), (32906, 251882), (33736, 251898), '
                                       '(242312, 251906), (260240, 251910), (239992, 251914), (253112, '
                                       '251918), (262972, 251924), (242236, 251930), (252132, 251934), '
                                       '(240466, 252438), (240466, 252452), (240466, 252466), (240466, '
                                       '252480), (240466, 252494), (240334, 252528), (240334, 252562), '
                                       '(240334, 252590), (240334, 252618)):\n'
                                       "    raise ValueError('original scene object child/continuation pair "
                                       "required')\n"
                                       'memory.frame(frame)\n'
                                       'def child(actual_memory, entered):\n'
                                       '    scene = SceneRefreshMemory(actual_memory.state)\n'
                                       '    if target == 26830:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'clear_video_sprite_plane_fields\n'
                                       '        return clear_video_sprite_plane_fields(scene, entered)\n'
                                       '    if target == 252320:\n'
                                       '        return initialize_scene_object_video_fields(scene, entered)\n'
                                       '    if target == 32906:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'enqueue_sound_command_fields\n'
                                       '        return enqueue_sound_command_fields(scene, entered)\n'
                                       '    if target == 33736:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'wait_for_scene_sound_byte_fields\n'
                                       '        return wait_for_scene_sound_byte_fields(scene, entered)\n'
                                       '    raise SceneRefreshBoundary(target, entered, continuation)\n'
                                       'return '
                                       '_presentation_call_fields(BattlePresentationMemory(memory.state), '
                                       'frame, continuation, child)'},
 '_scene_object_video_command_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                     'FirstDeploymentFrame',
                                        'returns': 'FirstDeploymentFrame',
                                        'flow': 'memory.sync_status(frame)\n'
                                                "frame = _first_word(frame, 'target_x', "
                                                'memory.state.read(4294964742, 2))\n'
                                                "frame = _first_byte(frame, 'target_x', low8(frame.target_x) "
                                                '& 191)\n'
                                                'return _scene_refresh_emit(memory, frame, 12582916, 2, '
                                                'low16(frame.target_x))'},
 '_scene_video_command': {'signature': 'state, retained', 'returns': None, 'flow': 'return _scene_object_video_command_fields(SceneRefreshMemory(state), first_replace(FirstDeploymentFrame.unobserved(), target_x=retained)).target_x'},
 'initialize_scene_object_video_complete': {'signature': 'state: SceneState, context: SceneControllerFrame',
                                            'returns': 'SceneControllerFrame',
                                            'flow': 'fields = _scene_controller_legacy_fields(state, '
                                                    'context)\n'
                                                    'return _scene_controller_legacy_projection(state, '
                                                    'initialize_scene_object_video_fields(SceneRefreshMemory(state), '
                                                    'fields))'},
 'initialize_scene_object_video_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                       'FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'from .business_scene import _scene_render_asl_word\n'
                                                  'frame = _scene_controller_entry_fields(memory, frame, '
                                                  '252320)\n'
                                                  'for command in (36610, 33328, 33584, 33799, 34152, 34560, '
                                                  '35584, 35969, 36149, 36610, 36881, 37268, 37376):\n'
                                                  '    frame = _scene_refresh_emit(memory, frame, 12582916, '
                                                  '2, command)\n'
                                                  'for source, destination, continuation in ((291812, 0, '
                                                  '252438), (299752, 8192, 252452), (305570, 16384, 252466), '
                                                  '(312748, 24576, 252480), (319632, 32768, 252494)):\n'
                                                  '    frame = first_replace(frame, '
                                                  'roster=memory.cursor_at(source))\n'
                                                  "    frame = _first_word(frame, 'target_x', destination)\n"
                                                  '    frame = _scene_object_call_fields(memory, frame, '
                                                  '240466, continuation)\n'
                                                  'for directory, destination, continuation, has_lea in '
                                                  '((252620, 57344, 252528, True), (252636, 57408, 252562, '
                                                  'True), (252620, 61440, 252590, False), (252636, 61504, '
                                                  '252618, False)):\n'
                                                  "    frame = _first_long(frame, 'target_x', 0)\n"
                                                  '    memory.sync_status(frame)\n'
                                                  "    frame = _first_byte(frame, 'target_x', "
                                                  'memory.state.read(4294934747, 1))\n'
                                                  '    frame = _scene_render_asl_word(memory, frame, '
                                                  "'target_x', low16(frame.target_x), 2)\n"
                                                  '    if has_lea:\n'
                                                  '        frame = first_replace(frame, '
                                                  'roster=memory.cursor_at(directory))\n'
                                                  '    memory.sync_status(frame)\n'
                                                  '    pointer = memory.cursor_at(directory, '
                                                  's16(low16(frame.target_x))).long()\n'
                                                  '    frame = first_replace(frame, '
                                                  'roster=memory.cursor_at(pointer), '
                                                  'candidates=memory.cursor_at(destination))\n'
                                                  "    frame = _first_long(frame, 'offset_x', 128)\n"
                                                  '    frame = _scene_object_call_fields(memory, frame, '
                                                  '240334, continuation)\n'
                                                  'return memory.sync_status(frame)'},
 'run_scene_object_controller_complete': {'signature': 'state: SceneState, context: SceneControllerFrame',
                                          'returns': 'SceneControllerOutcome',
                                          'flow': 'frame = '
                                                  'run_scene_object_controller_fields(SceneRefreshMemory(state), '
                                                  '_scene_controller_legacy_fields(state, context))\n'
                                                  'return '
                                                  'SceneControllerOutcome(_scene_controller_legacy_projection(state, '
                                                  'frame), None)'},
 'run_scene_object_controller_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                     'FirstDeploymentFrame',
                                        'returns': 'FirstDeploymentFrame',
                                        'flow': 'from .business_scene import _scene_render_compare\n'
                                                'frame = _scene_controller_entry_fields(memory, frame, '
                                                '251476, True)\n'
                                                'while True:\n'
                                                '    frame = memory.status_word(frame, 9984)\n'
                                                '    frame = _scene_object_video_command_fields(memory, '
                                                'frame)\n'
                                                '    frame = _scene_object_call_fields(memory, frame, 26830, '
                                                '251500)\n'
                                                '    frame = _scene_refresh_emit(memory, frame, 4294964932, '
                                                '2, 2)\n'
                                                '    frame = _scene_object_call_fields(memory, frame, '
                                                '252320, 251510)\n'
                                                "    frame = _first_long(frame, 'target_x', 0)\n"
                                                '    memory.sync_status(frame)\n'
                                                "    frame = _first_byte(frame, 'target_x', "
                                                'memory.state.read(4294934747, 1))\n'
                                                '    frame = _scene_object_call_fields(memory, frame, '
                                                '240532, 251520)\n'
                                                '    for address in (4294934730, 4294934732, 4294934734, '
                                                '4294934736):\n'
                                                '        frame = _scene_refresh_emit(memory, frame, address, '
                                                '2, 65535)\n'
                                                "    frame = _first_long(frame, 'target_x', 1)\n"
                                                '    frame = _scene_object_call_fields(memory, frame, '
                                                '240160, 251550)\n'
                                                '    frame = _scene_object_call_fields(memory, frame, '
                                                '240266, 251554)\n'
                                                '    memory.sync_status(frame)\n'
                                                '    phase = memory.state.read(4294934842, 2)\n'
                                                '    frame = _scene_render_compare(memory, frame, phase, 3, '
                                                '16)\n'
                                                '    if phase == 3:\n'
                                                '        frame = _scene_object_call_fields(memory, frame, '
                                                '262940, 251568)\n'
                                                '        frame = _scene_refresh_emit(memory, frame, '
                                                '4294934842, 2, 0)\n'
                                                '        frame = _scene_refresh_emit(memory, frame, '
                                                '4294934844, 2, 6)\n'
                                                '        memory.state.read(4294934846, 2)\n'
                                                '        frame = _scene_refresh_emit(memory, frame, '
                                                '4294934846, 2, 0)\n'
                                                '        side = memory.state.read(4294934820, 2)\n'
                                                '        frame = _scene_refresh_flags(memory, frame, side, '
                                                '2)\n'
                                                '        reversed_sides = side != 0\n'
                                                '        first = 4294935160 if reversed_sides else '
                                                '4294934904\n'
                                                '        second = 4294934904 if reversed_sides else '
                                                '4294935160\n'
                                                '        value = memory.state.read(16740460, 2)\n'
                                                '        frame = _scene_refresh_emit(memory, frame, first, '
                                                '2, value)\n'
                                                '        value = memory.state.read(16740540, 2)\n'
                                                '        frame = _scene_refresh_emit(memory, frame, second, '
                                                '2, value)\n'
                                                '        winner = memory.state.read(16740592, 1)\n'
                                                '        frame = _scene_render_compare(memory, frame, '
                                                'winner, 1, 8)\n'
                                                '        destination = 4294934832 if (winner == 1) != '
                                                'reversed_sides else 4294934840\n'
                                                '        frame = _scene_refresh_emit(memory, frame, '
                                                'destination, 2, 6)\n'
                                                '    else:\n'
                                                '        frame = _scene_refresh_emit(memory, frame, '
                                                '4294934560, 2, 0)\n'
                                                '        frame = _scene_refresh_emit(memory, frame, '
                                                '4294934564, 4, 0)\n'
                                                "        frame = _first_word(frame, 'target_x', 263)\n"
                                                '        frame = first_replace(frame, '
                                                'roster=memory.cursor_at(4294934826))\n'
                                                '        counter = low16(frame.target_x)\n'
                                                '        while True:\n'
                                                '            memory.sync_status(frame)\n'
                                                '            frame.roster.word()\n'
                                                '            frame.roster.set_word(0, 0)\n'
                                                '            frame = _scene_refresh_flags(memory, frame, 0, '
                                                '2)\n'
                                                '            frame = first_replace(frame, '
                                                'roster=frame.roster.advance(2))\n'
                                                '            frame = _scene_refresh_decrement(frame, '
                                                "'target_x', counter)\n"
                                                '            counter = u16(counter - 1)\n'
                                                '            if counter == 65535:\n'
                                                '                break\n'
                                                '        for address in (4294934826, 4294934828, 4294934830, '
                                                '4294934832, 4294934834, 4294934836, 4294934838, '
                                                '4294934840):\n'
                                                '            frame = _scene_refresh_emit(memory, frame, '
                                                'address, 2, 5)\n'
                                                '        frame = _scene_refresh_emit(memory, frame, '
                                                '4294934842, 2, 9)\n'
                                                '        frame = _scene_refresh_emit(memory, frame, '
                                                '4294934844, 2, 0)\n'
                                                '        frame = _scene_object_call_fields(memory, frame, '
                                                '268278, 251870)\n'
                                                "    frame = _first_word(frame, 'target_x', 142)\n"
                                                '    frame = _scene_object_call_fields(memory, frame, 32906, '
                                                '251882)\n'
                                                '    frame = memory.status_word(frame, 9472)\n'
                                                '    while True:\n'
                                                '        frame = _scene_refresh_emit(memory, frame, '
                                                '4294964754, 2, 1280)\n'
                                                '        frame = _scene_object_call_fields(memory, frame, '
                                                '33736, 251898)\n'
                                                '        memory.state.read(4294964754, 2)\n'
                                                '        frame = _scene_refresh_emit(memory, frame, '
                                                '4294964754, 2, 0)\n'
                                                '        for target, continuation in ((242312, 251906), '
                                                '(260240, 251910), (239992, 251914), (253112, 251918), '
                                                '(262972, 251924), (242236, 251930), (252132, 251934)):\n'
                                                '            frame = _scene_object_call_fields(memory, '
                                                'frame, target, continuation)\n'
                                                '        phase = memory.state.read(4294934842, 2)\n'
                                                '        frame = _scene_render_compare(memory, frame, phase, '
                                                '3, 16)\n'
                                                '        terminal = False\n'
                                                '        if phase == 3:\n'
                                                '            subphase = memory.state.read(4294934844, 2)\n'
                                                '            frame = _scene_render_compare(memory, frame, '
                                                'subphase, 3, 16)\n'
                                                '            if subphase == 3:\n'
                                                '                frame = _scene_refresh_emit(memory, frame, '
                                                '4294934804, 2, 1)\n'
                                                '                terminal = True\n'
                                                '        if not terminal:\n'
                                                '            phase = memory.state.read(4294934842, 2)\n'
                                                '            frame = _scene_render_compare(memory, frame, '
                                                'phase, 4, 16)\n'
                                                '            if phase == 4:\n'
                                                '                subphase = memory.state.read(4294934844, '
                                                '2)\n'
                                                '                frame = _scene_render_compare(memory, '
                                                'frame, subphase, 3, 16)\n'
                                                '                if subphase == 3:\n'
                                                '                    frame = _scene_refresh_emit(memory, '
                                                'frame, 4294934804, 2, 0)\n'
                                                '                    terminal = True\n'
                                                '        if not terminal:\n'
                                                '            phase = memory.state.read(4294934842, 2)\n'
                                                '            frame = _scene_render_compare(memory, frame, '
                                                'phase, 5, 16)\n'
                                                '            if phase == 5:\n'
                                                '                subphase = memory.state.read(4294934844, '
                                                '2)\n'
                                                '                frame = _scene_render_compare(memory, '
                                                'frame, subphase, 3, 16)\n'
                                                '                if subphase == 3:\n'
                                                '                    terminal = True\n'
                                                '        if not terminal:\n'
                                                '            phase = memory.state.read(4294934842, 2)\n'
                                                '            frame = _scene_render_compare(memory, frame, '
                                                'phase, 6, 16)\n'
                                                '            if phase == 6:\n'
                                                '                subphase = memory.state.read(4294934844, '
                                                '2)\n'
                                                '                frame = _scene_render_compare(memory, '
                                                'frame, subphase, 4, 16)\n'
                                                '                if subphase == 4:\n'
                                                '                    frame = _scene_refresh_emit(memory, '
                                                'frame, 4294934804, 2, 6)\n'
                                                '                    terminal = True\n'
                                                '        if terminal:\n'
                                                '            frame = memory.status_word(frame, 9984)\n'
                                                '            return '
                                                '_scene_object_video_command_fields(memory, frame)\n'
                                                "        frame = _first_byte(frame, 'target_x', "
                                                'memory.state.read(4294964738, 1))\n'
                                                "        frame = _first_byte(frame, 'target_x', "
                                                'low8(frame.target_x) & 240)\n'
                                                '        frame = _scene_render_compare(memory, frame, '
                                                'low8(frame.target_x), 240, 8)\n'
                                                '        if low8(frame.target_x) != 240:\n'
                                                '            continue\n'
                                                '        variant = memory.state.read(4294934747, 1)\n'
                                                '        frame = _scene_render_compare(memory, frame, '
                                                'variant, 3, 8)\n'
                                                '        if variant < 3:\n'
                                                '            previous = memory.state.read(4294934747, 1)\n'
                                                '            from '
                                                '..high_level_main_flows.business_movement_support import '
                                                '_movement_binary_flags\n'
                                                '            frame, value = '
                                                '_movement_binary_flags(memory.state, frame, previous, 1, '
                                                '8)\n'
                                                '            memory.sync_status(frame)\n'
                                                '            memory.state.write(4294934747, 1, value)\n'
                                                '        break'}})

APPROVED.setdefault('contexts_scene',set()).update({'_first_long', 'FirstDeploymentFrame', '_first_byte', '_scene_refresh_decrement', 'first_replace', 'SceneRefreshBoundary', '_scene_refresh_emit', '_first_word', 'SceneRefreshMemory', '_scene_refresh_flags'})

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('business_battle',set()).update({'_presentation_call_fields'})
APPROVED.setdefault('contexts_battle',set()).update({'BattlePresentationMemory'})
APPROVED.setdefault('business_services',set()).update({'clear_video_sprite_plane_fields', 'enqueue_sound_command_fields', 'wait_for_scene_sound_byte_fields'})
APPROVED.setdefault('business_scene',set()).update({'write_vdp_swapped_byte_rle_stream_fields', 'read_vdp_plane_rle_rows_fields'})
DECLARATIONS.update({'_scene_object_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                            'target: Long, continuation: Long',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'from ..high_level_gameplay_flow.business_battle import '
                                       '_presentation_call_fields\n'
                                       'from ..high_level_gameplay_flow.contexts_battle import '
                                       'BattlePresentationMemory\n'
                                       'if (target, continuation) not in ((26830, 251500), (252320, 251510), '
                                       '(240532, 251520), (240160, 251550), (240266, 251554), (262940, '
                                       '251568), (268278, 251870), (32906, 251882), (33736, 251898), '
                                       '(242312, 251906), (260240, 251910), (239992, 251914), (253112, '
                                       '251918), (262972, 251924), (242236, 251930), (252132, 251934), '
                                       '(240466, 252438), (240466, 252452), (240466, 252466), (240466, '
                                       '252480), (240466, 252494), (240334, 252528), (240334, 252562), '
                                       '(240334, 252590), (240334, 252618)):\n'
                                       "    raise ValueError('original scene object child/continuation pair "
                                       "required')\n"
                                       'memory.frame(frame)\n'
                                       'def child(actual_memory, entered):\n'
                                       '    scene = SceneRefreshMemory(actual_memory.state)\n'
                                       '    if target == 26830:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'clear_video_sprite_plane_fields\n'
                                       '        return clear_video_sprite_plane_fields(scene, entered)\n'
                                       '    if target == 252320:\n'
                                       '        return initialize_scene_object_video_fields(scene, entered)\n'
                                       '    if target == 240466:\n'
                                       '        from .business_scene import '
                                       'write_vdp_swapped_byte_rle_stream_fields\n'
                                       '        return write_vdp_swapped_byte_rle_stream_fields(scene, '
                                       'entered)\n'
                                       '    if target == 240334:\n'
                                       '        from .business_scene import read_vdp_plane_rle_rows_fields\n'
                                       '        return read_vdp_plane_rle_rows_fields(scene, entered)\n'
                                       '    if target == 32906:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'enqueue_sound_command_fields\n'
                                       '        return enqueue_sound_command_fields(scene, entered)\n'
                                       '    if target == 33736:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'wait_for_scene_sound_byte_fields\n'
                                       '        return wait_for_scene_sound_byte_fields(scene, entered)\n'
                                       '    raise SceneRefreshBoundary(target, entered, continuation)\n'
                                       'return '
                                       '_presentation_call_fields(BattlePresentationMemory(memory.state), '
                                       'frame, continuation, child)'}})

APPROVED.setdefault((2,'high_level_dynamic_flows.business_early_phase'),set()).add('_allocation_known_fields')
DECLARATIONS.update({'dispatch_scene_object_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from .business_scene import _scene_render_asl_word\nmemory.frame(frame)\nmemory.sync_status(frame)\nphase = memory.state.read(4294934842, 2)\nframe = _first_word(frame, 'target_x', phase)\nframe = _scene_render_asl_word(memory, frame, 'target_x', phase, 2)\ntarget = u32(253122 + s16(u16(phase << 2)))\nif target == 253122:\n    from ..high_level_dynamic_flows.business_early_phase import step_main_scene_phase_fields\n    return step_main_scene_phase_fields(memory, frame)\nif target in (253134, 253138, 253142, 253146, 253154):\n    from ..high_level_dynamic_flows.business_early_phase import _allocation_known_fields\n    return _allocation_known_fields(memory, frame, target)\nraise SceneRefreshBoundary(target, frame, None)"}})

# B39 actual main-stage entry route; ordinary native lowerers unchanged.
APPROVED.setdefault('business_scene',set()).update({'_scene_render_asl_word'})
APPROVED.setdefault('business_early_phase',set()).update({'step_main_scene_phase_fields'})
DECLARATIONS.update({'dispatch_scene_object_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                     'FirstDeploymentFrame',
                                        'returns': 'FirstDeploymentFrame',
                                        'flow': 'from .business_scene import _scene_render_asl_word\n'
                                                'memory.frame(frame)\n'
                                                'memory.sync_status(frame)\n'
                                                'phase = memory.state.read(4294934842, 2)\n'
                                                "frame = _first_word(frame, 'target_x', phase)\n"
                                                "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                                'phase, 2)\n'
                                                'target = u32(253122 + s16(u16(phase << 2)))\n'
                                                'if target == 253122:\n'
                                                '    from ..high_level_dynamic_flows.business_early_phase '
                                                'import step_main_scene_phase_fields\n'
                                                '    return step_main_scene_phase_fields(memory, frame)\n'
                                                'raise SceneRefreshBoundary(target, frame, None)'}})

# B35 sole selected-action field route; ordinary native lowerers unchanged.
APPROVED.setdefault('business_scene',set()).update({'_scene_render_compare', '_scene_render_asl_word'})
APPROVED.setdefault('business_actions',set()).update({'dispatch_object_action_fields'})
DECLARATIONS.update({'resume_selected_object_action_complete': {'signature': 'state, context',
                                            'returns': None,
                                            'flow': 'actual = '
                                                    'update_selected_object_action_fields(SceneRefreshMemory(state), '
                                                    '_scene_controller_legacy_fields(state, context), '
                                                    'primary_middle=True)\n'
                                                    'return '
                                                    'SceneControllerOutcome(_scene_controller_legacy_projection(state, '
                                                    'actual), None)'},
 'update_selected_object_action_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                       'FirstDeploymentFrame, primary_middle: bool=False',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'from .business_scene import _scene_render_compare, '
                                                  '_scene_render_asl_word\n'
                                                  'memory.frame(frame)\n'
                                                  'if frame.auxiliary is None or frame.target_x is None:\n'
                                                  '    raise SceneRefreshBoundary(265364, frame, None)\n'
                                                  'if type(primary_middle) is not bool:\n'
                                                  "    raise ValueError('actual primary-middle entry "
                                                  "selector required')\n"
                                                  'if not primary_middle:\n'
                                                  '    frame = _scene_render_compare(memory, frame, '
                                                  'frame.auxiliary.base, 4294935146, 32)\n'
                                                  'secondary = not primary_middle and frame.auxiliary.base '
                                                  '>= 4294935146\n'
                                                  'frame = first_replace(frame, '
                                                  'scratch=memory.cursor_at(4294935146 if secondary else '
                                                  '4294934890))\n'
                                                  'side = memory.state.read(4294934860, 2)\n'
                                                  'frame = _scene_render_compare(memory, frame, side, 2 if '
                                                  'secondary else 1, 16)\n'
                                                  'if side != (2 if secondary else 1):\n'
                                                  '    return frame\n'
                                                  'kind = frame.auxiliary.word()\n'
                                                  "frame = _first_word(frame, 'target_x', kind)\n"
                                                  "frame = _first_word(frame, 'target_x', kind & 127)\n"
                                                  'category = memory.state.read(4294934862, 2)\n'
                                                  'frame = _scene_render_compare(memory, frame, '
                                                  'low16(frame.target_x), category, 16)\n'
                                                  'if low16(frame.target_x) != category:\n'
                                                  '    return frame\n'
                                                  "frame = _first_long(frame, 'target_x', 0)\n"
                                                  'slot = memory.state.read(4294934864, 2)\n'
                                                  "frame = _first_word(frame, 'target_x', slot)\n"
                                                  "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                                  'slot, 4)\n'
                                                  'frame = first_replace(frame, '
                                                  'roster=memory.cursor_at(u32(s16(low16(frame.target_x)))))\n'
                                                  'frame = first_replace(frame, '
                                                  'roster=memory.cursor_at(u32(frame.roster.base + '
                                                  'frame.scratch.base)))\n'
                                                  'frame = _scene_render_compare(memory, frame, '
                                                  'frame.roster.base, frame.auxiliary.base, 32)\n'
                                                  'if frame.roster.base != frame.auxiliary.base:\n'
                                                  '    return frame\n'
                                                  'resumed = memory.state.read(4294934866, 2)\n'
                                                  'frame = _scene_refresh_flags(memory, frame, resumed, 2)\n'
                                                  'if resumed:\n'
                                                  '    selection = memory.state.read(4294934874, 2)\n'
                                                  "    frame = _first_word(frame, 'target_x', selection)\n"
                                                  '    table_base = 265550\n'
                                                  'else:\n'
                                                  '    frame = _scene_refresh_emit(memory, frame, '
                                                  '4294934866, 2, 1)\n'
                                                  '    horizontal = frame.auxiliary.word(0, 2)\n'
                                                  '    frame = _scene_render_compare(memory, frame, '
                                                  'horizontal, 512, 16)\n'
                                                  '    if horizontal >= 512:\n'
                                                  '        return _object_clear_word_fields(memory, frame, '
                                                  '4294934866)\n'
                                                  '    frame = _scene_object_call_fields(memory, frame, '
                                                  '243490, 265460)\n'
                                                  "    frame = _first_word(frame, 'target_x', "
                                                  'low16(frame.target_x) & 3)\n'
                                                  '    if low16(frame.target_x) != 0:\n'
                                                  '        planned = _scene_object_plan_call_fields(memory, '
                                                  'frame)\n'
                                                  '        frame = planned.frame\n'
                                                  '        if planned.discarded_continuation is not None:\n'
                                                  '            return frame\n'
                                                  '    frame = _scene_object_call_fields(memory, frame, '
                                                  '265512, 265474)\n'
                                                  '    frame = _scene_refresh_emit(memory, frame, '
                                                  '4294934874, 2, low16(frame.target_x))\n'
                                                  '    selection = low16(frame.target_x)\n'
                                                  '    table_base = 265484\n'
                                                  "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                                  'selection, 2)\n'
                                                  'target = u32(table_base + s16(u16(selection << 2)))\n'
                                                  'from ..high_level_dynamic_flows.business_actions import '
                                                  'dispatch_object_action_fields\n'
                                                  'return dispatch_object_action_fields(memory, frame, '
                                                  'target)'}})

# B34 sole nonlocal action planner fields; ordinary native lowerers unchanged.
APPROVED.setdefault('business_scene',set()).update({'_scene_render_asl_word', 'finish_actor_sprite_chains_fields', 'write_vdp_swapped_byte_rle_stream_fields', 'advance_scene_palette_fade_fields', 'read_vdp_plane_rle_rows_fields', '_scene_render_arithmetic', 'copy_scene_palette_variant_fields', 'begin_scene_palette_darken_fields', 'snapshot_and_clear_scene_palette_fields', 'sample_random_preserving_seed_fields', '_scene_render_compare'})
APPROVED.setdefault('business_services',set()).update({'enqueue_sound_command_fields', 'wait_for_scene_sound_byte_fields', 'clear_video_sprite_plane_fields'})
APPROVED.setdefault('business_battle',set()).update({'_presentation_call_fields'})
APPROVED.setdefault('contexts_battle',set()).update({'BattlePresentationMemory'})
DECLARATIONS.update({'_object_action_mode_slot_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'from .business_scene import _scene_render_compare, '
                                             '_scene_render_arithmetic, _scene_render_asl_word\n'
                                             'memory.frame(frame)\n'
                                             'if frame.auxiliary is None:\n'
                                             '    raise SceneRefreshBoundary(265512, frame, None)\n'
                                             "frame = _first_long(frame, 'target_x', 0)\n"
                                             "frame = _first_byte(frame, 'target_x', frame.auxiliary.byte(0, "
                                             '1))\n'
                                             'frame = _scene_render_compare(memory, frame, '
                                             'frame.auxiliary.base, 4294935146, 32)\n'
                                             'if frame.auxiliary.base >= 4294935146:\n'
                                             '    frame = _scene_render_arithmetic(memory, frame, '
                                             "'target_x', low16(frame.target_x), 4, 16)\n"
                                             "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                             'low16(frame.target_x), 1)\n'
                                             'return first_replace(frame, '
                                             'roster=memory.cursor_at(4294934826))'},
 '_object_planner_discard_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                    'returns': 'tuple',
                                    'flow': 'if frame.stack_cursor is None:\n'
                                            '    raise SceneRefreshBoundary(267400, frame, None)\n'
                                            'memory.sync_status(frame)\n'
                                            'token = frame.stack_cursor.long()\n'
                                            'frame = first_replace(frame, target_x=token, '
                                            'stack_cursor=frame.stack_cursor.advance(4))\n'
                                            'return (frame, StackContinuation(token))'},
 '_object_planner_finish_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                                'long_reach: bool',
                                   'returns': 'SceneActionPlanFields',
                                   'flow': 'from .business_scene import _scene_render_compare, '
                                           '_scene_render_arithmetic\n'
                                           'if not long_reach:\n'
                                           '    frame = _scene_render_compare(memory, frame, '
                                           'frame.scratch.base, 4294934890, 32)\n'
                                           '    leader = frame.scratch.base == 4294934890\n'
                                           '    if not leader:\n'
                                           '        frame = _scene_render_compare(memory, frame, '
                                           'frame.scratch.base, 4294935146, 32)\n'
                                           '        leader = frame.scratch.base == 4294935146\n'
                                           '    if leader:\n'
                                           '        category = memory.state.read(4294934862, 2)\n'
                                           '        frame = _scene_render_compare(memory, frame, category, '
                                           '3, 16)\n'
                                           '        if category == 3:\n'
                                           '            frame, discarded = '
                                           '_object_planner_discard_fields(memory, frame)\n'
                                           '            side = memory.state.read(4294934860, 2)\n'
                                           "            frame = _first_word(frame, 'target_x', side)\n"
                                           '            frame = _scene_render_arithmetic(memory, frame, '
                                           "'target_x', side, 1, 16, True)\n"
                                           '            frame = _scene_refresh_emit(memory, frame, '
                                           '4294934902, 2, low16(frame.target_x))\n'
                                           '            frame = _scene_refresh_emit(memory, frame, '
                                           '4294934842, 2, 3)\n'
                                           '            frame = _scene_refresh_emit(memory, frame, '
                                           '4294934844, 2, 0)\n'
                                           '            frame = _scene_refresh_emit(memory, frame, '
                                           '4294934846, 2, 1)\n'
                                           '            frame = _scene_refresh_emit(memory, frame, '
                                           '4294934866, 2, 2)\n'
                                           '            return '
                                           'SceneActionPlanFields(memory.sync_status(frame), discarded)\n'
                                           'frame = _scene_refresh_emit(memory, frame, 4294934876, 4, '
                                           'frame.scratch.base)\n'
                                           'frame = _scene_refresh_emit(memory, frame, 4294934874, 2, 9 if '
                                           'long_reach else 8)\n'
                                           'frame = _object_clear_word_fields(memory, frame, 4294934882)\n'
                                           'if long_reach:\n'
                                           '    frame = _scene_refresh_emit(memory, frame, 4294934884, 2, '
                                           'frame.auxiliary.word(0, 2))\n'
                                           '    frame = _scene_refresh_emit(memory, frame, 4294934886, 2, '
                                           'frame.auxiliary.word(0, 4))\n'
                                           '    frame = _object_clear_word_fields(memory, frame, '
                                           '4294934888)\n'
                                           'direction = memory.state.read(4294934528, 2)\n'
                                           'frame = _scene_refresh_emit(memory, frame, '
                                           'u32(frame.auxiliary.base + 8), 2, direction)\n'
                                           'frame, discarded = _object_planner_discard_fields(memory, '
                                           'frame)\n'
                                           "frame = _first_word(frame, 'target_x', 162 if long_reach else "
                                           '167)\n'
                                           'if long_reach:\n'
                                           '    frame = _scene_object_call_fields(memory, frame, 32906, '
                                           '267414)\n'
                                           'else:\n'
                                           '    from ..high_level_gameplay_flow.business_services import '
                                           'enqueue_sound_command_fields\n'
                                           '    frame = enqueue_sound_command_fields(memory, frame)\n'
                                           'return SceneActionPlanFields(memory.sync_status(frame), '
                                           'discarded)'},
 '_scene_object_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                            'target: Long, continuation: Long',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'from ..high_level_gameplay_flow.business_battle import '
                                       '_presentation_call_fields\n'
                                       'from ..high_level_gameplay_flow.contexts_battle import '
                                       'BattlePresentationMemory\n'
                                       'if (target, continuation) not in ((26830, 251500), (252320, 251510), '
                                       '(240532, 251520), (240160, 251550), (240266, 251554), (262940, '
                                       '251568), (268278, 251870), (32906, 251882), (33736, 251898), '
                                       '(242312, 251906), (260240, 251910), (239992, 251914), (253112, '
                                       '251918), (262972, 251924), (242236, 251930), (252132, 251934), '
                                       '(240466, 252438), (240466, 252452), (240466, 252466), (240466, '
                                       '252480), (240466, 252494), (240334, 252528), (240334, 252562), '
                                       '(240334, 252590), (240334, 252618), (243490, 268364), (243490, '
                                       '268396), (243490, 268434), (259266, 268460), (243490, 268622), '
                                       '(265364, 263248), (263178, 262976), (263238, 263000), (243490, '
                                       '265460), (266700, 265470), (265512, 265474), (266658, 266596), '
                                       '(266588, 267518), (267514, 266758), (267514, 266798), (267514, '
                                       '266816), (267514, 266834), (267514, 266884), (267514, 266924), '
                                       '(267514, 266942), (267514, 266960), (267514, 266994), (267514, '
                                       '267024), (267514, 267054), (267514, 267084), (267514, 267124), '
                                       '(267514, 267142), (267514, 267160), (267514, 267190), (267514, '
                                       '267208), (267514, 267226), (267514, 267256), (267514, 267274), '
                                       '(267514, 267292), (267514, 267322), (267514, 267340), (267514, '
                                       '267358), (32906, 267414)):\n'
                                       "    raise ValueError('original scene object child/continuation pair "
                                       "required')\n"
                                       'memory.frame(frame)\n'
                                       'def child(actual_memory, entered):\n'
                                       '    scene = SceneRefreshMemory(actual_memory.state)\n'
                                       '    if target == 26830:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'clear_video_sprite_plane_fields\n'
                                       '        return clear_video_sprite_plane_fields(scene, entered)\n'
                                       '    if target == 252320:\n'
                                       '        return initialize_scene_object_video_fields(scene, entered)\n'
                                       '    if target == 240466:\n'
                                       '        from .business_scene import '
                                       'write_vdp_swapped_byte_rle_stream_fields\n'
                                       '        return write_vdp_swapped_byte_rle_stream_fields(scene, '
                                       'entered)\n'
                                       '    if target == 240334:\n'
                                       '        from .business_scene import read_vdp_plane_rle_rows_fields\n'
                                       '        return read_vdp_plane_rle_rows_fields(scene, entered)\n'
                                       '    if target == 240532:\n'
                                       '        from .business_scene import '
                                       'copy_scene_palette_variant_fields\n'
                                       '        return copy_scene_palette_variant_fields(scene, entered)\n'
                                       '    if target == 240160:\n'
                                       '        from .business_scene import '
                                       'begin_scene_palette_darken_fields\n'
                                       '        return begin_scene_palette_darken_fields(scene, entered)\n'
                                       '    if target == 240266:\n'
                                       '        from .business_scene import '
                                       'snapshot_and_clear_scene_palette_fields\n'
                                       '        return snapshot_and_clear_scene_palette_fields(scene, '
                                       'entered)\n'
                                       '    if target == 262940:\n'
                                       '        return clear_scene_object_label_plane_fields(scene, '
                                       'entered)\n'
                                       '    if target == 268278:\n'
                                       '        return initialize_scene_object_roster_fields(scene, '
                                       'entered)\n'
                                       '    if target == 259266:\n'
                                       '        return normalize_object_squad_size_fields(scene, entered)\n'
                                       '    if target == 243490:\n'
                                       '        from .business_scene import '
                                       'sample_random_preserving_seed_fields\n'
                                       '        return sample_random_preserving_seed_fields(scene, entered)\n'
                                       '    if target == 242312:\n'
                                       '        return append_scene_center_marker_fields(scene, entered)\n'
                                       '    if target == 260240:\n'
                                       '        return cycle_special_scene_palette_fields(scene, entered)\n'
                                       '    if target == 252132:\n'
                                       '        return integrate_scene_coordinates_fields(scene, entered)\n'
                                       '    if target == 242236:\n'
                                       '        from .business_scene import '
                                       'finish_actor_sprite_chains_fields\n'
                                       '        return finish_actor_sprite_chains_fields(scene, entered)\n'
                                       '    if target == 253112:\n'
                                       '        return dispatch_scene_object_phase_fields(scene, entered)\n'
                                       '    if target == 262972:\n'
                                       '        return advance_scene_object_actions_fields(scene, entered)\n'
                                       '    if target == 263178:\n'
                                       '        return rebuild_depth_sorted_object_queue_fields(scene, '
                                       'entered)\n'
                                       '    if target == 263238:\n'
                                       '        return draw_active_scene_object_fields(scene, entered)\n'
                                       '    if target == 265364:\n'
                                       '        return update_selected_object_action_fields(scene, entered)\n'
                                       '    if target == 265512:\n'
                                       '        return read_object_action_mode_fields(scene, entered)\n'
                                       '    if target == 266658:\n'
                                       '        return offset_scene_object_position_fields(scene, entered)\n'
                                       '    if target == 266588:\n'
                                       '        return probe_scene_object_overlap_fields(scene, entered)\n'
                                       '    if target == 239992:\n'
                                       '        from .business_scene import '
                                       'advance_scene_palette_fade_fields\n'
                                       '        return advance_scene_palette_fade_fields(scene, entered)\n'
                                       '    if target == 267514:\n'
                                       '        return probe_opposing_object_overlap_fields(scene, entered)\n'
                                       '    if target == 32906:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'enqueue_sound_command_fields\n'
                                       '        return enqueue_sound_command_fields(scene, entered)\n'
                                       '    if target == 33736:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'wait_for_scene_sound_byte_fields\n'
                                       '        return wait_for_scene_sound_byte_fields(scene, entered)\n'
                                       '    raise SceneRefreshBoundary(target, entered, continuation)\n'
                                       'return '
                                       '_presentation_call_fields(BattlePresentationMemory(memory.state), '
                                       'frame, continuation, child)'},
 '_scene_object_plan_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                    'returns': 'SceneActionPlanFields',
                                    'flow': 'memory.frame(frame)\n'
                                            'if frame.stack_cursor is None:\n'
                                            '    raise SceneRefreshBoundary(266700, frame, 265470)\n'
                                            'frame = first_replace(frame, '
                                            'stack_cursor=frame.stack_cursor.advance(-4))\n'
                                            'frame.stack_cursor.set_long(0, 265470)\n'
                                            'outcome = plan_scene_object_action_fields(memory, '
                                            'frame).validate(memory.state)\n'
                                            'if outcome.discarded_continuation is not None:\n'
                                            '    return outcome\n'
                                            'token = outcome.frame.stack_cursor.long()\n'
                                            'if token != 265470:\n'
                                            '    raise SceneRefreshBoundary(token, outcome.frame, 265470)\n'
                                            'frame = first_replace(outcome.frame, '
                                            'stack_cursor=outcome.frame.stack_cursor.advance(4))\n'
                                            'return SceneActionPlanFields(memory.sync_status(frame), None)'},
 'plan_scene_object_action_complete': {'signature': 'state, context',
                                       'returns': None,
                                       'flow': 'outcome = '
                                               'plan_scene_object_action_fields(SceneRefreshMemory(state), '
                                               '_scene_controller_legacy_fields(state, context))\n'
                                               'return '
                                               'SceneControllerOutcome(_scene_controller_legacy_projection(state, '
                                               'outcome.frame), outcome.discarded_continuation)'},
 'plan_scene_object_action_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'SceneActionPlanFields',
                                     'flow': 'from .business_scene import _scene_render_compare\n'
                                             'memory.frame(frame)\n'
                                             'if frame.stack_cursor is None:\n'
                                             '    raise SceneRefreshBoundary(266700, frame, None)\n'
                                             'frame = _object_action_mode_slot_fields(memory, frame)\n'
                                             'mode = frame.roster.word(low16(frame.target_x))\n'
                                             'frame = _scene_render_compare(memory, frame, mode, 6, 16)\n'
                                             'secondary = frame.auxiliary.base >= 4294935146\n'
                                             'def select_direction(direction, phase):\n'
                                             '    nonlocal frame\n'
                                             '    frame = _scene_refresh_emit(memory, frame, 4294934528, 2, '
                                             'direction)\n'
                                             '    frame = _scene_refresh_emit(memory, frame, 4294934872, 2, '
                                             'phase)\n'
                                             'def try_offset(horizontal, vertical, continuation):\n'
                                             '    nonlocal frame\n'
                                             "    frame = _first_word(frame, 'target_x', horizontal)\n"
                                             "    frame = _first_word(frame, 'target_y', vertical)\n"
                                             '    frame = _scene_object_call_fields(memory, frame, 267514, '
                                             'continuation)\n'
                                             '    frame = _scene_refresh_flags(memory, frame, '
                                             'low16(frame.target_x), 2)\n'
                                             '    return low16(frame.target_x) != 0\n'
                                             'if mode == 6:\n'
                                             '    horizontal = 16 if secondary else 32784\n'
                                             '    select_direction(0 if secondary else 1, 1 if secondary '
                                             'else 0)\n'
                                             '    if try_offset(horizontal, 0, 266758 if secondary else '
                                             '266884):\n'
                                             '        return _object_planner_finish_fields(memory, frame, '
                                             'False)\n'
                                             '    kind = frame.auxiliary.byte(0, 1)\n'
                                             '    frame = _scene_render_compare(memory, frame, kind, 1, 8)\n'
                                             '    if kind != 1:\n'
                                             '        return '
                                             'SceneActionPlanFields(memory.sync_status(frame), None)\n'
                                             '    select_direction(0 if secondary else 1, 1 if secondary '
                                             'else 0)\n'
                                             '    for magnitude, continuation in ((32, 266798 if secondary '
                                             'else 266924), (48, 266816 if secondary else 266942), (64, '
                                             '266834 if secondary else 266960)):\n'
                                             '        if try_offset(magnitude if secondary else magnitude | '
                                             '32768, 0, continuation):\n'
                                             '            return _object_planner_finish_fields(memory, '
                                             'frame, True)\n'
                                             '    return SceneActionPlanFields(memory.sync_status(frame), '
                                             'None)\n'
                                             'for direction, phase, horizontal, vertical, continuation in '
                                             '((1, 0, 32784, 0, 266994), (0, 1, 16, 0, 267024), (2, 3, 0, '
                                             '16, 267054), (3, 6, 0, 32784, 267084)):\n'
                                             '    select_direction(direction, phase)\n'
                                             '    if try_offset(horizontal, vertical, continuation):\n'
                                             '        return _object_planner_finish_fields(memory, frame, '
                                             'False)\n'
                                             'kind = frame.auxiliary.byte(0, 1)\n'
                                             'frame = _scene_render_compare(memory, frame, kind, 1, 8)\n'
                                             'if kind != 1:\n'
                                             '    return SceneActionPlanFields(memory.sync_status(frame), '
                                             'None)\n'
                                             'for direction, phase, offsets in ((1, 0, ((32800, 0, 267124), '
                                             '(32816, 0, 267142), (32832, 0, 267160))), (0, 1, ((32, 0, '
                                             '267190), (48, 0, 267208), (64, 0, 267226))), (2, 3, ((0, 32, '
                                             '267256), (0, 3, 267274), (0, 64, 267292))), (3, 6, ((0, 32800, '
                                             '267322), (0, 32816, 267340), (0, 32832, 267358)))):\n'
                                             '    select_direction(direction, phase)\n'
                                             '    for horizontal, vertical, continuation in offsets:\n'
                                             '        if try_offset(horizontal, vertical, continuation):\n'
                                             '            return _object_planner_finish_fields(memory, '
                                             'frame, True)\n'
                                             'return SceneActionPlanFields(memory.sync_status(frame), None)'},
 'read_object_action_mode_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'frame = _object_action_mode_slot_fields(memory, frame)\n'
                                            "return memory.sync_status(_first_word(frame, 'target_x', "
                                            'frame.roster.word(low16(frame.target_x))))'},
 'update_selected_object_action_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                       'FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'from .business_scene import _scene_render_compare, '
                                                  '_scene_render_asl_word\n'
                                                  'memory.frame(frame)\n'
                                                  'if frame.auxiliary is None or frame.target_x is None:\n'
                                                  '    raise SceneRefreshBoundary(265364, frame, None)\n'
                                                  'frame = _scene_render_compare(memory, frame, '
                                                  'frame.auxiliary.base, 4294935146, 32)\n'
                                                  'secondary = frame.auxiliary.base >= 4294935146\n'
                                                  'frame = first_replace(frame, '
                                                  'scratch=memory.cursor_at(4294935146 if secondary else '
                                                  '4294934890))\n'
                                                  'side = memory.state.read(4294934860, 2)\n'
                                                  'frame = _scene_render_compare(memory, frame, side, 2 if '
                                                  'secondary else 1, 16)\n'
                                                  'if side != (2 if secondary else 1):\n'
                                                  '    return frame\n'
                                                  'kind = frame.auxiliary.word()\n'
                                                  "frame = _first_word(frame, 'target_x', kind)\n"
                                                  "frame = _first_word(frame, 'target_x', kind & 127)\n"
                                                  'category = memory.state.read(4294934862, 2)\n'
                                                  'frame = _scene_render_compare(memory, frame, '
                                                  'low16(frame.target_x), category, 16)\n'
                                                  'if low16(frame.target_x) != category:\n'
                                                  '    return frame\n'
                                                  "frame = _first_long(frame, 'target_x', 0)\n"
                                                  'slot = memory.state.read(4294934864, 2)\n'
                                                  "frame = _first_word(frame, 'target_x', slot)\n"
                                                  "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                                  'slot, 4)\n'
                                                  'frame = first_replace(frame, '
                                                  'roster=memory.cursor_at(u32(s16(low16(frame.target_x)))))\n'
                                                  'frame = first_replace(frame, '
                                                  'roster=memory.cursor_at(u32(frame.roster.base + '
                                                  'frame.scratch.base)))\n'
                                                  'frame = _scene_render_compare(memory, frame, '
                                                  'frame.roster.base, frame.auxiliary.base, 32)\n'
                                                  'if frame.roster.base != frame.auxiliary.base:\n'
                                                  '    return frame\n'
                                                  'resumed = memory.state.read(4294934866, 2)\n'
                                                  'frame = _scene_refresh_flags(memory, frame, resumed, 2)\n'
                                                  'if resumed:\n'
                                                  '    selection = memory.state.read(4294934874, 2)\n'
                                                  "    frame = _first_word(frame, 'target_x', selection)\n"
                                                  '    table_base = 265550\n'
                                                  'else:\n'
                                                  '    frame = _scene_refresh_emit(memory, frame, '
                                                  '4294934866, 2, 1)\n'
                                                  '    horizontal = frame.auxiliary.word(0, 2)\n'
                                                  '    frame = _scene_render_compare(memory, frame, '
                                                  'horizontal, 512, 16)\n'
                                                  '    if horizontal >= 512:\n'
                                                  '        return _object_clear_word_fields(memory, frame, '
                                                  '4294934866)\n'
                                                  '    frame = _scene_object_call_fields(memory, frame, '
                                                  '243490, 265460)\n'
                                                  "    frame = _first_word(frame, 'target_x', "
                                                  'low16(frame.target_x) & 3)\n'
                                                  '    if low16(frame.target_x) != 0:\n'
                                                  '        planned = _scene_object_plan_call_fields(memory, '
                                                  'frame)\n'
                                                  '        frame = planned.frame\n'
                                                  '        if planned.discarded_continuation is not None:\n'
                                                  '            return frame\n'
                                                  '    frame = _scene_object_call_fields(memory, frame, '
                                                  '265512, 265474)\n'
                                                  '    frame = _scene_refresh_emit(memory, frame, '
                                                  '4294934874, 2, low16(frame.target_x))\n'
                                                  '    selection = low16(frame.target_x)\n'
                                                  '    table_base = 265484\n'
                                                  "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                                  'selection, 2)\n'
                                                  'target = u32(table_base + s16(u16(selection << 2)))\n'
                                                  'raise SceneRefreshBoundary(target, frame, None)'}})

# B33 sole palette/action/overlap fields; ordinary native lowerers unchanged.
APPROVED.setdefault('business_battle',set()).update({'_presentation_call_fields'})
APPROVED.setdefault('contexts_battle',set()).update({'BattlePresentationMemory'})
APPROVED.setdefault('business_services',set()).update({'enqueue_sound_command_fields', 'clear_video_sprite_plane_fields', 'wait_for_scene_sound_byte_fields'})
APPROVED.setdefault('business_scene',set()).update({'_scene_render_compare', 'finish_actor_sprite_chains_fields', '_scene_render_arithmetic', 'begin_scene_palette_darken_fields', '_scene_render_bit', 'copy_scene_palette_variant_fields', 'snapshot_and_clear_scene_palette_fields', 'sample_random_preserving_seed_fields', 'read_vdp_plane_rle_rows_fields', '_scene_render_asl_word', 'write_vdp_swapped_byte_rle_stream_fields', 'advance_scene_palette_fade_fields'})
APPROVED.setdefault('business_movement_support',set()).update({'_movement_binary_flags'})
DECLARATIONS.update({'_scene_object_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                            'target: Long, continuation: Long',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'from ..high_level_gameplay_flow.business_battle import '
                                       '_presentation_call_fields\n'
                                       'from ..high_level_gameplay_flow.contexts_battle import '
                                       'BattlePresentationMemory\n'
                                       'if (target, continuation) not in ((26830, 251500), (252320, 251510), '
                                       '(240532, 251520), (240160, 251550), (240266, 251554), (262940, '
                                       '251568), (268278, 251870), (32906, 251882), (33736, 251898), '
                                       '(242312, 251906), (260240, 251910), (239992, 251914), (253112, '
                                       '251918), (262972, 251924), (242236, 251930), (252132, 251934), '
                                       '(240466, 252438), (240466, 252452), (240466, 252466), (240466, '
                                       '252480), (240466, 252494), (240334, 252528), (240334, 252562), '
                                       '(240334, 252590), (240334, 252618), (243490, 268364), (243490, '
                                       '268396), (243490, 268434), (259266, 268460), (243490, 268622), '
                                       '(265364, 263248), (263178, 262976), (263238, 263000), (243490, '
                                       '265460), (266700, 265470), (265512, 265474), (266658, 266596), '
                                       '(266588, 267518)):\n'
                                       "    raise ValueError('original scene object child/continuation pair "
                                       "required')\n"
                                       'memory.frame(frame)\n'
                                       'def child(actual_memory, entered):\n'
                                       '    scene = SceneRefreshMemory(actual_memory.state)\n'
                                       '    if target == 26830:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'clear_video_sprite_plane_fields\n'
                                       '        return clear_video_sprite_plane_fields(scene, entered)\n'
                                       '    if target == 252320:\n'
                                       '        return initialize_scene_object_video_fields(scene, entered)\n'
                                       '    if target == 240466:\n'
                                       '        from .business_scene import '
                                       'write_vdp_swapped_byte_rle_stream_fields\n'
                                       '        return write_vdp_swapped_byte_rle_stream_fields(scene, '
                                       'entered)\n'
                                       '    if target == 240334:\n'
                                       '        from .business_scene import read_vdp_plane_rle_rows_fields\n'
                                       '        return read_vdp_plane_rle_rows_fields(scene, entered)\n'
                                       '    if target == 240532:\n'
                                       '        from .business_scene import '
                                       'copy_scene_palette_variant_fields\n'
                                       '        return copy_scene_palette_variant_fields(scene, entered)\n'
                                       '    if target == 240160:\n'
                                       '        from .business_scene import '
                                       'begin_scene_palette_darken_fields\n'
                                       '        return begin_scene_palette_darken_fields(scene, entered)\n'
                                       '    if target == 240266:\n'
                                       '        from .business_scene import '
                                       'snapshot_and_clear_scene_palette_fields\n'
                                       '        return snapshot_and_clear_scene_palette_fields(scene, '
                                       'entered)\n'
                                       '    if target == 262940:\n'
                                       '        return clear_scene_object_label_plane_fields(scene, '
                                       'entered)\n'
                                       '    if target == 268278:\n'
                                       '        return initialize_scene_object_roster_fields(scene, '
                                       'entered)\n'
                                       '    if target == 259266:\n'
                                       '        return normalize_object_squad_size_fields(scene, entered)\n'
                                       '    if target == 243490:\n'
                                       '        from .business_scene import '
                                       'sample_random_preserving_seed_fields\n'
                                       '        return sample_random_preserving_seed_fields(scene, entered)\n'
                                       '    if target == 242312:\n'
                                       '        return append_scene_center_marker_fields(scene, entered)\n'
                                       '    if target == 260240:\n'
                                       '        return cycle_special_scene_palette_fields(scene, entered)\n'
                                       '    if target == 252132:\n'
                                       '        return integrate_scene_coordinates_fields(scene, entered)\n'
                                       '    if target == 242236:\n'
                                       '        from .business_scene import '
                                       'finish_actor_sprite_chains_fields\n'
                                       '        return finish_actor_sprite_chains_fields(scene, entered)\n'
                                       '    if target == 253112:\n'
                                       '        return dispatch_scene_object_phase_fields(scene, entered)\n'
                                       '    if target == 262972:\n'
                                       '        return advance_scene_object_actions_fields(scene, entered)\n'
                                       '    if target == 263178:\n'
                                       '        return rebuild_depth_sorted_object_queue_fields(scene, '
                                       'entered)\n'
                                       '    if target == 263238:\n'
                                       '        return draw_active_scene_object_fields(scene, entered)\n'
                                       '    if target == 265364:\n'
                                       '        return update_selected_object_action_fields(scene, entered)\n'
                                       '    if target == 265512:\n'
                                       '        return read_object_action_mode_fields(scene, entered)\n'
                                       '    if target == 266658:\n'
                                       '        return offset_scene_object_position_fields(scene, entered)\n'
                                       '    if target == 266588:\n'
                                       '        return probe_scene_object_overlap_fields(scene, entered)\n'
                                       '    if target == 239992:\n'
                                       '        from .business_scene import '
                                       'advance_scene_palette_fade_fields\n'
                                       '        return advance_scene_palette_fade_fields(scene, entered)\n'
                                       '    if target == 32906:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'enqueue_sound_command_fields\n'
                                       '        return enqueue_sound_command_fields(scene, entered)\n'
                                       '    if target == 33736:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'wait_for_scene_sound_byte_fields\n'
                                       '        return wait_for_scene_sound_byte_fields(scene, entered)\n'
                                       '    raise SceneRefreshBoundary(target, entered, continuation)\n'
                                       'return '
                                       '_presentation_call_fields(BattlePresentationMemory(memory.state), '
                                       'frame, continuation, child)'},
 '_select_scene_object_action_complete': {'signature': 'state, context, secondary',
                                          'returns': None,
                                          'flow': 'return update_selected_object_action_complete(state, '
                                                  'context)'},
 'advance_scene_object_actions_complete': {'signature': 'state: SceneState, context: SceneControllerFrame',
                                           'returns': 'SceneControllerOutcome',
                                           'flow': 'actual = '
                                                   'advance_scene_object_actions_fields(SceneRefreshMemory(state), '
                                                   '_scene_controller_legacy_fields(state, context))\n'
                                                   'return '
                                                   'SceneControllerOutcome(_scene_controller_legacy_projection(state, '
                                                   'actual), None)'},
 'advance_scene_object_actions_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                      'FirstDeploymentFrame',
                                         'returns': 'FirstDeploymentFrame',
                                         'flow': 'from .business_scene import _scene_render_compare, '
                                                 '_scene_render_bit, _scene_render_asl_word\n'
                                                 'memory.frame(frame)\n'
                                                 'if frame.stack_cursor is None:\n'
                                                 '    raise SceneRefreshBoundary(262972, frame, None)\n'
                                                 'frame = _scene_object_call_fields(memory, frame, 263178, '
                                                 '262976)\n'
                                                 'frame = first_replace(frame, '
                                                 'scratch=memory.cursor_at(4294935402))\n'
                                                 'while True:\n'
                                                 '    value = frame.scratch.long()\n'
                                                 '    frame = _scene_refresh_flags(memory, frame, value, 4)\n'
                                                 '    if value == 0:\n'
                                                 '        break\n'
                                                 '    pointer = frame.scratch.long()\n'
                                                 '    frame = first_replace(frame, '
                                                 'auxiliary=memory.cursor_at(pointer), '
                                                 'scratch=frame.scratch.advance(4))\n'
                                                 '    active = frame.auxiliary.byte()\n'
                                                 '    frame = _scene_render_bit(memory, frame, active, 128)\n'
                                                 '    if not active & 128:\n'
                                                 '        continue\n'
                                                 '    frame = first_replace(frame, '
                                                 'stack_cursor=frame.stack_cursor.advance(-4))\n'
                                                 '    frame.stack_cursor.set_long(0, frame.scratch.base)\n'
                                                 '    frame = _scene_object_call_fields(memory, frame, '
                                                 '263238, 263000)\n'
                                                 '    restored = frame.stack_cursor.long()\n'
                                                 '    frame = first_replace(frame, '
                                                 'scratch=memory.cursor_at(restored), '
                                                 'stack_cursor=frame.stack_cursor.advance(4))\n'
                                                 'side = memory.state.read(4294934860, 2)\n'
                                                 'frame = _scene_refresh_flags(memory, frame, side, 2)\n'
                                                 'if side == 0:\n'
                                                 '    return frame\n'
                                                 'state_code = memory.state.read(4294934866, 2)\n'
                                                 'frame = _scene_render_compare(memory, frame, state_code, '
                                                 '2, 16)\n'
                                                 'if state_code != 2:\n'
                                                 '    hold = memory.state.read(4294934846, 2)\n'
                                                 '    frame = _scene_refresh_flags(memory, frame, hold, 2)\n'
                                                 '    if hold != 0:\n'
                                                 '        return frame\n'
                                                 '    state_code = memory.state.read(4294934866, 2)\n'
                                                 '    frame = _scene_render_compare(memory, frame, '
                                                 'state_code, 1, 16)\n'
                                                 '    if state_code == 1:\n'
                                                 '        return frame\n'
                                                 'frame = _object_clear_word_fields(memory, frame, '
                                                 '4294934866)\n'
                                                 'frame = _object_adjust_word_fields(memory, frame, '
                                                 '4294934868, 1, True)\n'
                                                 'if not frame.status & 8:\n'
                                                 '    return frame\n'
                                                 'while True:\n'
                                                 '    frame = _object_adjust_word_fields(memory, frame, '
                                                 '4294934864, 1)\n'
                                                 '    slot = memory.state.read(4294934864, 2)\n'
                                                 '    frame = _scene_render_compare(memory, frame, slot, 16, '
                                                 '16)\n'
                                                 '    if slot >= 16:\n'
                                                 '        frame = _object_clear_word_fields(memory, frame, '
                                                 '4294934864)\n'
                                                 '        frame = _object_adjust_word_fields(memory, frame, '
                                                 '4294934862, 1)\n'
                                                 '        category = memory.state.read(4294934862, 2)\n'
                                                 '        frame = _scene_render_compare(memory, frame, '
                                                 'category, 4, 16)\n'
                                                 '        if category >= 4:\n'
                                                 '            frame = _object_clear_word_fields(memory, '
                                                 'frame, 4294934862)\n'
                                                 '            frame = _object_adjust_word_fields(memory, '
                                                 'frame, 4294934860, 1)\n'
                                                 '            side = memory.state.read(4294934860, 2)\n'
                                                 '            frame = _scene_render_compare(memory, frame, '
                                                 'side, 3, 16)\n'
                                                 '            if side >= 3:\n'
                                                 '                frame = _object_clear_word_fields(memory, '
                                                 'frame, 4294934860)\n'
                                                 '        break\n'
                                                 '    frame = first_replace(frame, '
                                                 'roster=memory.cursor_at(4294934890))\n'
                                                 '    side = memory.state.read(4294934860, 2)\n'
                                                 '    frame = _scene_render_compare(memory, frame, side, 1, '
                                                 '16)\n'
                                                 '    if side != 1:\n'
                                                 '        frame = first_replace(frame, '
                                                 'roster=memory.cursor_at(4294935146))\n'
                                                 '    slot = memory.state.read(4294934864, 2)\n'
                                                 "    frame = _first_word(frame, 'target_x', slot)\n"
                                                 '    frame = _scene_render_asl_word(memory, frame, '
                                                 "'target_x', slot, 4)\n"
                                                 '    active = frame.roster.byte(low16(frame.target_x))\n'
                                                 '    frame = _scene_render_bit(memory, frame, active, 128)\n'
                                                 '    if not active & 128:\n'
                                                 '        continue\n'
                                                 '    kind = frame.roster.word(low16(frame.target_x))\n'
                                                 "    frame = _first_word(frame, 'target_x', kind)\n"
                                                 "    frame = _first_word(frame, 'target_x', kind & 127)\n"
                                                 '    category = memory.state.read(4294934862, 2)\n'
                                                 '    frame = _scene_render_compare(memory, frame, '
                                                 'low16(frame.target_x), category, 16)\n'
                                                 '    if low16(frame.target_x) == category:\n'
                                                 '        break\n'
                                                 'frame = _object_clear_word_fields(memory, frame, '
                                                 '4294934868)\n'
                                                 'category = memory.state.read(4294934862, 2)\n'
                                                 'frame = _scene_render_compare(memory, frame, category, 2, '
                                                 '16)\n'
                                                 'if category >= 2:\n'
                                                 '    frame = _scene_refresh_emit(memory, frame, 4294934868, '
                                                 '2, 1)\n'
                                                 'return memory.sync_status(frame)'},
 'dispatch_scene_object_phase_complete': {'signature': 'state: SceneState, context: SceneControllerFrame',
                                          'returns': 'SceneControllerOutcome',
                                          'flow': 'actual = '
                                                  'dispatch_scene_object_phase_fields(SceneRefreshMemory(state), '
                                                  '_scene_controller_legacy_fields(state, context))\n'
                                                  'return '
                                                  'SceneControllerOutcome(_scene_controller_legacy_projection(state, '
                                                  'actual), None)'},
 'dispatch_scene_object_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                     'FirstDeploymentFrame',
                                        'returns': 'FirstDeploymentFrame',
                                        'flow': 'from .business_scene import _scene_render_asl_word\n'
                                                'memory.frame(frame)\n'
                                                'memory.sync_status(frame)\n'
                                                'phase = memory.state.read(4294934842, 2)\n'
                                                "frame = _first_word(frame, 'target_x', phase)\n"
                                                "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                                'phase, 2)\n'
                                                'target = u32(253122 + s16(u16(phase << 2)))\n'
                                                'raise SceneRefreshBoundary(target, frame, None)'},
 'offset_scene_object_position_complete': {'signature': 'state, context',
                                           'returns': None,
                                           'flow': 'actual = '
                                                   'offset_scene_object_position_fields(SceneRefreshMemory(state), '
                                                   '_scene_controller_legacy_fields(state, context))\n'
                                                   'return _scene_controller_legacy_projection(state, '
                                                   'actual)'},
 'offset_scene_object_position_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                      'FirstDeploymentFrame',
                                         'returns': 'FirstDeploymentFrame',
                                         'flow': 'from ..high_level_main_flows.business_movement_support '
                                                 'import _movement_binary_flags\n'
                                                 'memory.frame(frame)\n'
                                                 'if frame.auxiliary is None or frame.target_x is None or '
                                                 'frame.target_y is None:\n'
                                                 '    raise SceneRefreshBoundary(266658, frame, None)\n'
                                                 "for displacement, name in ((2, 'target_x'), (4, "
                                                 "'target_y')):\n"
                                                 '    magnitude = low16(frame.carrier(name))\n'
                                                 "    frame = _first_word(frame, 'unit', magnitude)\n"
                                                 '    subtract = bool(magnitude & 32768)\n'
                                                 '    if subtract:\n'
                                                 '        magnitude &= 127\n'
                                                 '        frame = _first_word(frame, name, magnitude)\n'
                                                 '    memory.sync_status(frame)\n'
                                                 '    previous = frame.auxiliary.word(0, displacement)\n'
                                                 '    frame, value = _movement_binary_flags(memory.state, '
                                                 'frame, previous, magnitude, 16, subtract)\n'
                                                 '    frame.auxiliary.set_word(0, value, displacement)\n'
                                                 'return memory.sync_status(frame)'},
 'probe_opposing_object_overlap_complete': {'signature': 'state, context',
                                            'returns': None,
                                            'flow': 'actual = '
                                                    'probe_opposing_object_overlap_fields(SceneRefreshMemory(state), '
                                                    '_scene_controller_legacy_fields(state, context))\n'
                                                    'return _scene_controller_legacy_projection(state, '
                                                    'actual)'},
 'probe_opposing_object_overlap_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                       'FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'from .business_scene import _scene_render_compare\n'
                                                  'memory.frame(frame)\n'
                                                  'if frame.stack_cursor is None:\n'
                                                  '    raise SceneRefreshBoundary(267514, frame, None)\n'
                                                  'frame = _scene_object_call_fields(memory, frame, 266588, '
                                                  '267518)\n'
                                                  'frame = _scene_refresh_flags(memory, frame, '
                                                  'low16(frame.target_x), 2)\n'
                                                  'if low16(frame.target_x):\n'
                                                  '    frame = _scene_render_compare(memory, frame, '
                                                  'frame.auxiliary.base, 4294935146, 32)\n'
                                                  '    secondary = frame.auxiliary.base >= 4294935146\n'
                                                  '    frame = _scene_render_compare(memory, frame, '
                                                  'frame.scratch.base, 4294935146, 32)\n'
                                                  '    if secondary and frame.scratch.base < 4294935146:\n'
                                                  '        return frame\n'
                                                  '    if not secondary and frame.scratch.base >= '
                                                  '4294935146:\n'
                                                  '        return frame\n'
                                                  "return memory.sync_status(_first_long(frame, 'target_x', "
                                                  '0))'},
 'probe_scene_object_overlap_complete': {'signature': 'state, context',
                                         'returns': None,
                                         'flow': 'actual = '
                                                 'probe_scene_object_overlap_fields(SceneRefreshMemory(state), '
                                                 '_scene_controller_legacy_fields(state, context))\n'
                                                 'return _scene_controller_legacy_projection(state, actual)'},
 'probe_scene_object_overlap_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'from .business_scene import _scene_render_compare, '
                                               '_scene_render_bit\n'
                                               'memory.frame(frame)\n'
                                               'if frame.stack_cursor is None or frame.auxiliary is None:\n'
                                               '    raise SceneRefreshBoundary(266588, frame, None)\n'
                                               'memory.sync_status(frame)\n'
                                               "frame = _first_long(frame, 'count', frame.auxiliary.long(0, "
                                               '2))\n'
                                               'frame = _scene_object_call_fields(memory, frame, 266658, '
                                               '266596)\n'
                                               "frame = _first_long(frame, 'target_x', 0)\n"
                                               'frame = first_replace(frame, '
                                               'scratch=memory.cursor_at(4294934890))\n'
                                               'while True:\n'
                                               '    active = frame.scratch.byte()\n'
                                               '    frame = _scene_render_bit(memory, frame, active, 128)\n'
                                               '    matched = False\n'
                                               '    if active & 128:\n'
                                               '        frame = _scene_render_compare(memory, frame, '
                                               'frame.auxiliary.base, frame.scratch.base, 32)\n'
                                               '        if frame.auxiliary.base != frame.scratch.base:\n'
                                               '            horizontal = frame.scratch.word(0, 2)\n'
                                               "            frame = _first_word(frame, 'target_y', "
                                               'horizontal)\n'
                                               '            actor_horizontal = frame.auxiliary.word(0, 2)\n'
                                               '            frame = _scene_render_compare(memory, frame, '
                                               'horizontal, actor_horizontal, 16)\n'
                                               '            if horizontal == actor_horizontal:\n'
                                               '                vertical = frame.scratch.word(0, 4)\n'
                                               "                frame = _first_word(frame, 'target_y', "
                                               'vertical)\n'
                                               '                actor_vertical = frame.auxiliary.word(0, 4)\n'
                                               '                frame = _scene_render_compare(memory, frame, '
                                               'vertical, actor_vertical, 16)\n'
                                               '                matched = vertical == actor_vertical\n'
                                               '    if matched:\n'
                                               "        frame = _first_long(frame, 'target_x', 1)\n"
                                               '        return _scene_refresh_emit(memory, frame, '
                                               'u32(frame.auxiliary.base + 2), 4, frame.count)\n'
                                               '    frame = first_replace(frame, '
                                               'scratch=frame.scratch.advance(16))\n'
                                               '    frame = _scene_render_compare(memory, frame, '
                                               'frame.scratch.base, 4294935402, 32)\n'
                                               '    if frame.scratch.base >= 4294935402:\n'
                                               '        return _scene_refresh_emit(memory, frame, '
                                               'u32(frame.auxiliary.base + 2), 4, frame.count)'},
 'read_object_action_mode': {'signature': 'state: SceneState, actor: Table',
                             'returns': 'Long',
                             'flow': 'checked_table(actor, state)\n'
                                     'actual = read_object_action_mode_fields(SceneRefreshMemory(state), '
                                     'first_replace(FirstDeploymentFrame.unobserved(), '
                                     'auxiliary=actor.cursor()))\n'
                                     'return actual.target_x'},
 'read_object_action_mode_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'from .business_scene import _scene_render_compare, '
                                            '_scene_render_arithmetic, _scene_render_asl_word\n'
                                            'memory.frame(frame)\n'
                                            'if frame.auxiliary is None:\n'
                                            '    raise SceneRefreshBoundary(265512, frame, None)\n'
                                            "frame = _first_long(frame, 'target_x', 0)\n"
                                            "frame = _first_byte(frame, 'target_x', frame.auxiliary.byte(0, "
                                            '1))\n'
                                            'frame = _scene_render_compare(memory, frame, '
                                            'frame.auxiliary.base, 4294935146, 32)\n'
                                            'if frame.auxiliary.base >= 4294935146:\n'
                                            "    frame = _scene_render_arithmetic(memory, frame, 'target_x', "
                                            'low16(frame.target_x), 4, 16)\n'
                                            "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                            'low16(frame.target_x), 1)\n'
                                            'frame = first_replace(frame, '
                                            'roster=memory.cursor_at(4294934826))\n'
                                            "frame = _first_word(frame, 'target_x', "
                                            'frame.roster.word(low16(frame.target_x)))\n'
                                            'return memory.sync_status(frame)'},
 'rebuild_depth_sorted_object_queue_complete': {'signature': 'state, context',
                                                'returns': None,
                                                'flow': 'actual = '
                                                        'rebuild_depth_sorted_object_queue_fields(SceneRefreshMemory(state), '
                                                        '_scene_controller_legacy_fields(state, context))\n'
                                                        'return _scene_controller_legacy_projection(state, '
                                                        'actual)'},
 'rebuild_depth_sorted_object_queue_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
 'returns': 'FirstDeploymentFrame',
 'flow': 'from .business_scene import _scene_render_compare, _scene_render_bit\n'
         'memory.frame(frame)\n'
         'memory.sync_status(frame)\n'
         'tick = memory.state.read(4294964000, 2)\n'
         "frame = _first_word(frame, 'target_x', tick)\n"
         "frame = _first_word(frame, 'target_x', tick & 15)\n"
         'if tick & 15:\n'
         '    return frame\n'
         'frame = first_replace(frame, scratch=memory.cursor_at(4294935402))\n'
         "frame = _first_long(frame, 'target_x', 30)\n"
         'while True:\n'
         '    frame = first_replace(frame, auxiliary=memory.cursor_at(4294934890))\n'
         '    while True:\n'
         '        active = frame.auxiliary.byte()\n'
         '        frame = _scene_render_bit(memory, frame, active, 128)\n'
         '        if active & 128:\n'
         '            horizontal = frame.auxiliary.word(0, 2)\n'
         "            frame = _first_word(frame, 'target_y', horizontal)\n"
         "            frame, depth = _object_shift_word_right_fields(memory, frame, 'target_y', horizontal, "
         '4)\n'
         '            frame = _scene_render_compare(memory, frame, depth, low16(frame.target_x), 16)\n'
         '            if depth == low16(frame.target_x):\n'
         '                frame = _scene_refresh_emit(memory, frame, frame.scratch.base, 4, '
         'frame.auxiliary.base)\n'
         '                frame = first_replace(frame, scratch=frame.scratch.advance(4))\n'
         '        frame = first_replace(frame, auxiliary=frame.auxiliary.advance(16))\n'
         '        frame = _scene_render_compare(memory, frame, frame.auxiliary.base, 4294935402, 32)\n'
         '        if frame.auxiliary.base >= 4294935402:\n'
         '            break\n'
         "    frame = _scene_refresh_decrement(frame, 'target_x', low16(frame.target_x))\n"
         '    if low16(frame.target_x) == 65535:\n'
         '        break\n'
         'memory.sync_status(frame)\n'
         'memory.state.read(frame.scratch.base, 4)\n'
         'return _scene_refresh_emit(memory, frame, frame.scratch.base, 4, 0)'},
 'update_selected_object_action_complete': {'signature': 'state: SceneState, context: SceneControllerFrame',
                                            'returns': 'SceneControllerOutcome',
                                            'flow': 'actual = '
                                                    'update_selected_object_action_fields(SceneRefreshMemory(state), '
                                                    '_scene_controller_legacy_fields(state, context))\n'
                                                    'return '
                                                    'SceneControllerOutcome(_scene_controller_legacy_projection(state, '
                                                    'actual), None)'},
 'update_selected_object_action_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                       'FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'from .business_scene import _scene_render_compare, '
                                                  '_scene_render_asl_word\n'
                                                  'memory.frame(frame)\n'
                                                  'if frame.auxiliary is None or frame.target_x is None:\n'
                                                  '    raise SceneRefreshBoundary(265364, frame, None)\n'
                                                  'frame = _scene_render_compare(memory, frame, '
                                                  'frame.auxiliary.base, 4294935146, 32)\n'
                                                  'secondary = frame.auxiliary.base >= 4294935146\n'
                                                  'frame = first_replace(frame, '
                                                  'scratch=memory.cursor_at(4294935146 if secondary else '
                                                  '4294934890))\n'
                                                  'side = memory.state.read(4294934860, 2)\n'
                                                  'frame = _scene_render_compare(memory, frame, side, 2 if '
                                                  'secondary else 1, 16)\n'
                                                  'if side != (2 if secondary else 1):\n'
                                                  '    return frame\n'
                                                  'kind = frame.auxiliary.word()\n'
                                                  "frame = _first_word(frame, 'target_x', kind)\n"
                                                  "frame = _first_word(frame, 'target_x', kind & 127)\n"
                                                  'category = memory.state.read(4294934862, 2)\n'
                                                  'frame = _scene_render_compare(memory, frame, '
                                                  'low16(frame.target_x), category, 16)\n'
                                                  'if low16(frame.target_x) != category:\n'
                                                  '    return frame\n'
                                                  "frame = _first_long(frame, 'target_x', 0)\n"
                                                  'slot = memory.state.read(4294934864, 2)\n'
                                                  "frame = _first_word(frame, 'target_x', slot)\n"
                                                  "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                                  'slot, 4)\n'
                                                  'frame = first_replace(frame, '
                                                  'roster=memory.cursor_at(u32(s16(low16(frame.target_x)))))\n'
                                                  'frame = first_replace(frame, '
                                                  'roster=memory.cursor_at(u32(frame.roster.base + '
                                                  'frame.scratch.base)))\n'
                                                  'frame = _scene_render_compare(memory, frame, '
                                                  'frame.roster.base, frame.auxiliary.base, 32)\n'
                                                  'if frame.roster.base != frame.auxiliary.base:\n'
                                                  '    return frame\n'
                                                  'resumed = memory.state.read(4294934866, 2)\n'
                                                  'frame = _scene_refresh_flags(memory, frame, resumed, 2)\n'
                                                  'if resumed:\n'
                                                  '    selection = memory.state.read(4294934874, 2)\n'
                                                  "    frame = _first_word(frame, 'target_x', selection)\n"
                                                  '    table_base = 265550\n'
                                                  'else:\n'
                                                  '    frame = _scene_refresh_emit(memory, frame, '
                                                  '4294934866, 2, 1)\n'
                                                  '    horizontal = frame.auxiliary.word(0, 2)\n'
                                                  '    frame = _scene_render_compare(memory, frame, '
                                                  'horizontal, 512, 16)\n'
                                                  '    if horizontal >= 512:\n'
                                                  '        return _object_clear_word_fields(memory, frame, '
                                                  '4294934866)\n'
                                                  '    frame = _scene_object_call_fields(memory, frame, '
                                                  '243490, 265460)\n'
                                                  "    frame = _first_word(frame, 'target_x', "
                                                  'low16(frame.target_x) & 3)\n'
                                                  '    if low16(frame.target_x) != 0:\n'
                                                  '        frame = _scene_object_call_fields(memory, frame, '
                                                  '266700, 265470)\n'
                                                  '    frame = _scene_object_call_fields(memory, frame, '
                                                  '265512, 265474)\n'
                                                  '    frame = _scene_refresh_emit(memory, frame, '
                                                  '4294934874, 2, low16(frame.target_x))\n'
                                                  '    selection = low16(frame.target_x)\n'
                                                  '    table_base = 265484\n'
                                                  "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                                  'selection, 2)\n'
                                                  'target = u32(table_base + s16(u16(selection << 2)))\n'
                                                  'raise SceneRefreshBoundary(target, frame, None)'}})

# B32 sole object rendering/integration/actor-chain fields; ordinary native lowerers unchanged.
APPROVED.setdefault('business_scene',set()).update({'_scene_render_compare', 'write_vdp_swapped_byte_rle_stream_fields', '_scene_render_push_longs', '_scene_render_asl_word', 'copy_scene_palette_variant_fields', '_scene_render_apply_delta', '_scene_render_bit', 'begin_scene_palette_darken_fields', '_scene_render_arithmetic', 'snapshot_and_clear_scene_palette_fields', 'read_vdp_plane_rle_rows_fields', 'finish_actor_sprite_chains_fields', '_scene_render_restore_sprite', 'sample_random_preserving_seed_fields'})
APPROVED.setdefault('contexts_scene',set()).update({'_first_shift_word'})
APPROVED.setdefault('business_movement_support',set()).update({'_movement_binary_flags'})
APPROVED.setdefault('business_battle',set()).update({'_presentation_call_fields'})
APPROVED.setdefault('contexts_battle',set()).update({'BattlePresentationMemory'})
APPROVED.setdefault('business_services',set()).update({'enqueue_sound_command_fields', 'wait_for_scene_sound_byte_fields', 'clear_video_sprite_plane_fields'})
DECLARATIONS.update({'_append_object_sprite_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                  'returns': 'FirstDeploymentFrame',
                                  'flow': 'from .business_scene import _scene_render_push_longs, '
                                          '_scene_render_restore_sprite, _scene_render_compare, '
                                          '_scene_render_bit, _scene_render_arithmetic, '
                                          '_scene_render_asl_word, _scene_render_apply_delta\n'
                                          'from .contexts_scene import _first_shift_word\n'
                                          'from ..high_level_main_flows.business_movement_support import '
                                          '_movement_binary_flags\n'
                                          'memory.frame(frame)\n'
                                          'if frame.stack_cursor is None:\n'
                                          '    raise SceneRefreshBoundary(241980, frame, None)\n'
                                          'frame = _scene_render_push_longs(memory, frame, '
                                          '(frame.candidates.base, frame.offset_y, frame.offset_x))\n'
                                          'memory.sync_status(frame)\n'
                                          'capacity = memory.state.read(4294963968, 1)\n'
                                          'frame = _scene_render_compare(memory, frame, capacity, 80, 8)\n'
                                          'if capacity >= 80:\n'
                                          '    return '
                                          'memory.sync_status(_scene_render_restore_sprite(memory, frame))\n'
                                          "frame = _first_long(frame, 'distance', frame.distance & 65535)\n"
                                          "frame = _first_word(frame, 'choice', low16(frame.unit))\n"
                                          "frame = _first_word(frame, 'unit', low16(frame.unit) & 65528)\n"
                                          "frame = _first_word(frame, 'choice', low16(frame.choice) & 7)\n"
                                          "frame = _scene_render_asl_word(memory, frame, 'choice', "
                                          'low16(frame.choice), 2)\n'
                                          "frame = _scene_render_arithmetic(memory, frame, 'target_x', "
                                          'low16(frame.target_x), memory.state.read(4294934560, 2), 16, '
                                          'True)\n'
                                          "frame = _scene_render_arithmetic(memory, frame, 'target_x', "
                                          'low16(frame.target_x), 128, 16)\n'
                                          'if low16(frame.target_x) & 32768:\n'
                                          '    return '
                                          'memory.sync_status(_scene_render_restore_sprite(memory, frame))\n'
                                          'frame = _scene_render_bit(memory, frame, frame.unit, 32)\n'
                                          'if frame.unit & 32:\n'
                                          "    frame = _scene_render_arithmetic(memory, frame, 'target_x', "
                                          'low16(frame.target_x), 8, 16, True)\n'
                                          "frame = _scene_render_arithmetic(memory, frame, 'target_y', "
                                          'low16(frame.target_y), memory.state.read(4294934562, 2), 16, '
                                          'True)\n'
                                          "frame = _scene_render_arithmetic(memory, frame, 'target_y', "
                                          'low16(frame.target_y), 128, 16)\n'
                                          'frame = _scene_render_bit(memory, frame, frame.unit, 16)\n'
                                          'if frame.unit & 16:\n'
                                          "    frame = _scene_render_arithmetic(memory, frame, 'target_y', "
                                          'low16(frame.target_y), 8, 16, True)\n'
                                          "frame = _first_word(frame, 'offset_x', 0)\n"
                                          'count = memory.state.read(4294963968, 1)\n'
                                          "frame = _first_byte(frame, 'offset_x', count)\n"
                                          "frame = _first_shift_word(frame, 'offset_x', count, 3)\n"
                                          'frame = first_replace(frame, '
                                          'candidates=memory.cursor_at(4294965248), '
                                          'controller=memory.cursor_at(4294934596))\n'
                                          'frame = first_replace(frame, '
                                          'candidates=frame.candidates.advance(s16(low16(frame.offset_x))))\n'
                                          'while True:\n'
                                          "    frame = _first_word(frame, 'offset_y', "
                                          'low16(frame.target_x))\n'
                                          "    frame = _first_long(frame, 'offset_x', 0)\n"
                                          '    horizontal = frame.roster.byte()\n'
                                          "    frame = _first_byte(frame, 'offset_x', horizontal)\n"
                                          '    frame = _scene_render_compare(memory, frame, horizontal, 128, '
                                          '8)\n'
                                          '    if horizontal == 128:\n'
                                          '        break\n'
                                          '    frame, horizontal_position = '
                                          '_scene_render_apply_delta(memory, frame, 32, '
                                          'low16(frame.offset_y))\n'
                                          '    frame = _scene_refresh_emit(memory, frame, '
                                          'frame.candidates.base, 2, horizontal_position)\n'
                                          "    frame = _first_word(frame, 'offset_y', "
                                          'low16(frame.target_y))\n'
                                          "    frame = _first_byte(frame, 'offset_x', frame.roster.byte(0, "
                                          '3))\n'
                                          '    frame, vertical_position = _scene_render_apply_delta(memory, '
                                          'frame, 16, low16(frame.offset_y))\n'
                                          '    frame = _scene_refresh_emit(memory, frame, '
                                          'frame.candidates.base + 6, 2, vertical_position)\n'
                                          '    frame = _scene_refresh_emit(memory, frame, '
                                          'frame.candidates.base + 2, 1, frame.roster.byte(0, 1))\n'
                                          '    layer = s16(low16(frame.choice))\n'
                                          '    head = frame.controller.long(layer)\n'
                                          '    frame = _scene_refresh_flags(memory, frame, head, 4)\n'
                                          '    if head == 0:\n'
                                          '        frame = _scene_refresh_emit(memory, frame, '
                                          'u32(frame.controller.base + layer), 4, frame.candidates.base)\n'
                                          '        frame = _scene_refresh_emit(memory, frame, '
                                          'u32(frame.controller.base + layer + 32), 1, '
                                          'memory.state.read(4294963968, 1))\n'
                                          '    else:\n'
                                          '        frame = first_replace(frame, '
                                          'scan=memory.cursor_at(frame.controller.long(layer, 64)))\n'
                                          '        frame = _scene_refresh_emit(memory, frame, '
                                          'u32(frame.scan.base + 3), 1, memory.state.read(4294963968, 1))\n'
                                          '    frame = _scene_refresh_emit(memory, frame, '
                                          'u32(frame.controller.base + layer + 64), 4, '
                                          'frame.candidates.base)\n'
                                          '    count = memory.state.read(4294963968, 1)\n'
                                          '    frame, new_count = _movement_binary_flags(memory.state, '
                                          'frame, count, 1, 8)\n'
                                          '    memory.sync_status(frame)\n'
                                          '    memory.state.write(4294963968, 1, new_count)\n'
                                          "    frame = _first_byte(frame, 'offset_x', frame.roster.byte(0, "
                                          '1))\n'
                                          "    frame = _first_word(frame, 'offset_x', low16(frame.offset_x) "
                                          '& 240)\n'
                                          "    frame = _scene_render_arithmetic(memory, frame, 'offset_x', "
                                          'low8(frame.offset_x), low8(frame.count), 8)\n'
                                          "    frame = _first_word(frame, 'offset_x', low16(frame.offset_x) "
                                          '^ low16(frame.unit))\n'
                                          "    frame = _scene_render_asl_word(memory, frame, 'offset_x', "
                                          'low16(frame.offset_x), 7)\n'
                                          "    frame = _first_byte(frame, 'offset_x', low8(frame.offset_x) | "
                                          'frame.roster.byte(0, 2))\n'
                                          "    frame = _scene_render_arithmetic(memory, frame, 'offset_x', "
                                          'low16(frame.offset_x), low16(frame.distance), 16)\n'
                                          '    frame = _scene_refresh_emit(memory, frame, '
                                          'frame.candidates.base + 4, 2, low16(frame.offset_x))\n'
                                          '    frame = first_replace(frame, '
                                          'candidates=frame.candidates.advance(8), '
                                          'roster=frame.roster.advance(4))\n'
                                          '    capacity = memory.state.read(4294963968, 1)\n'
                                          '    frame = _scene_render_compare(memory, frame, capacity, 80, '
                                          '8)\n'
                                          '    if capacity >= 80:\n'
                                          '        break\n'
                                          'return memory.sync_status(_scene_render_restore_sprite(memory, '
                                          'frame))'},
 '_append_sprite_entries_complete': {'signature': 'state, context',
                                     'returns': None,
                                     'flow': 'actual = '
                                             '_append_object_sprite_fields(SceneRefreshMemory(state), '
                                             '_scene_controller_legacy_fields(state, context))\n'
                                             'return _scene_controller_legacy_projection(state, actual)'},
 '_object_shift_velocity_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                                'amount: Word',
                                   'returns': 'FirstDeploymentFrame',
                                   'flow': 'value = frame.target_y\n'
                                           'result = u32(value << amount)\n'
                                           'carry = bool(value & 1 << 32 - amount)\n'
                                           'signs = value >> 31 - amount & (1 << amount + 1) - 1\n'
                                           'overflow = signs not in (0, (1 << amount + 1) - 1)\n'
                                           'status = (17 if carry else 0) | (8 if result & 2147483648 else '
                                           '0) | (4 if result == 0 else 0) | (2 if overflow else 0)\n'
                                           'return memory.sync_status(first_replace(frame, target_y=result, '
                                           'status=status))'},
 '_object_shift_word_right_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                                  'name: str, word: Word, amount: Word',
                                     'returns': 'tuple',
                                     'flow': 'result = word >> amount\n'
                                             'carry = bool(word & 1 << amount - 1)\n'
                                             'frame = _first_word(frame, name, result)\n'
                                             'status = (17 if carry else 0) | (8 if result & 32768 else 0) | '
                                             '(4 if result == 0 else 0)\n'
                                             'return (memory.sync_status(first_replace(frame, '
                                             'status=status)), result)'},
 '_restore_scene_sprite_saved': {'signature': 'state, frame, destination_role',
                                 'returns': None,
                                 'flow': 'from .business_scene import _scene_render_restore_sprite\n'
                                         'actual = _scene_render_restore_sprite(SceneRefreshMemory(state), '
                                         '_scene_controller_legacy_fields(state, frame))\n'
                                         'return _scene_controller_legacy_projection(state, actual)'},
 '_scene_object_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                            'target: Long, continuation: Long',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'from ..high_level_gameplay_flow.business_battle import '
                                       '_presentation_call_fields\n'
                                       'from ..high_level_gameplay_flow.contexts_battle import '
                                       'BattlePresentationMemory\n'
                                       'if (target, continuation) not in ((26830, 251500), (252320, 251510), '
                                       '(240532, 251520), (240160, 251550), (240266, 251554), (262940, '
                                       '251568), (268278, 251870), (32906, 251882), (33736, 251898), '
                                       '(242312, 251906), (260240, 251910), (239992, 251914), (253112, '
                                       '251918), (262972, 251924), (242236, 251930), (252132, 251934), '
                                       '(240466, 252438), (240466, 252452), (240466, 252466), (240466, '
                                       '252480), (240466, 252494), (240334, 252528), (240334, 252562), '
                                       '(240334, 252590), (240334, 252618), (243490, 268364), (243490, '
                                       '268396), (243490, 268434), (259266, 268460), (243490, 268622), '
                                       '(265364, 263248)):\n'
                                       "    raise ValueError('original scene object child/continuation pair "
                                       "required')\n"
                                       'memory.frame(frame)\n'
                                       'def child(actual_memory, entered):\n'
                                       '    scene = SceneRefreshMemory(actual_memory.state)\n'
                                       '    if target == 26830:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'clear_video_sprite_plane_fields\n'
                                       '        return clear_video_sprite_plane_fields(scene, entered)\n'
                                       '    if target == 252320:\n'
                                       '        return initialize_scene_object_video_fields(scene, entered)\n'
                                       '    if target == 240466:\n'
                                       '        from .business_scene import '
                                       'write_vdp_swapped_byte_rle_stream_fields\n'
                                       '        return write_vdp_swapped_byte_rle_stream_fields(scene, '
                                       'entered)\n'
                                       '    if target == 240334:\n'
                                       '        from .business_scene import read_vdp_plane_rle_rows_fields\n'
                                       '        return read_vdp_plane_rle_rows_fields(scene, entered)\n'
                                       '    if target == 240532:\n'
                                       '        from .business_scene import '
                                       'copy_scene_palette_variant_fields\n'
                                       '        return copy_scene_palette_variant_fields(scene, entered)\n'
                                       '    if target == 240160:\n'
                                       '        from .business_scene import '
                                       'begin_scene_palette_darken_fields\n'
                                       '        return begin_scene_palette_darken_fields(scene, entered)\n'
                                       '    if target == 240266:\n'
                                       '        from .business_scene import '
                                       'snapshot_and_clear_scene_palette_fields\n'
                                       '        return snapshot_and_clear_scene_palette_fields(scene, '
                                       'entered)\n'
                                       '    if target == 262940:\n'
                                       '        return clear_scene_object_label_plane_fields(scene, '
                                       'entered)\n'
                                       '    if target == 268278:\n'
                                       '        return initialize_scene_object_roster_fields(scene, '
                                       'entered)\n'
                                       '    if target == 259266:\n'
                                       '        return normalize_object_squad_size_fields(scene, entered)\n'
                                       '    if target == 243490:\n'
                                       '        from .business_scene import '
                                       'sample_random_preserving_seed_fields\n'
                                       '        return sample_random_preserving_seed_fields(scene, entered)\n'
                                       '    if target == 242312:\n'
                                       '        return append_scene_center_marker_fields(scene, entered)\n'
                                       '    if target == 260240:\n'
                                       '        return cycle_special_scene_palette_fields(scene, entered)\n'
                                       '    if target == 252132:\n'
                                       '        return integrate_scene_coordinates_fields(scene, entered)\n'
                                       '    if target == 242236:\n'
                                       '        from .business_scene import '
                                       'finish_actor_sprite_chains_fields\n'
                                       '        return finish_actor_sprite_chains_fields(scene, entered)\n'
                                       '    if target == 32906:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'enqueue_sound_command_fields\n'
                                       '        return enqueue_sound_command_fields(scene, entered)\n'
                                       '    if target == 33736:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'wait_for_scene_sound_byte_fields\n'
                                       '        return wait_for_scene_sound_byte_fields(scene, entered)\n'
                                       '    raise SceneRefreshBoundary(target, entered, continuation)\n'
                                       'return '
                                       '_presentation_call_fields(BattlePresentationMemory(memory.state), '
                                       'frame, continuation, child)'},
 'append_scene_center_marker_complete': {'signature': 'state: SceneState, context: SceneControllerFrame',
                                         'returns': 'SceneControllerFrame',
                                         'flow': 'actual = '
                                                 'append_scene_center_marker_fields(SceneRefreshMemory(state), '
                                                 '_scene_controller_legacy_fields(state, context))\n'
                                                 'return _scene_controller_legacy_projection(state, actual)'},
 'append_scene_center_marker_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'from .business_scene import _scene_render_arithmetic\n'
                                               'memory.frame(frame)\n'
                                               'if frame.stack_cursor is None:\n'
                                               '    raise SceneRefreshBoundary(242312, frame, None)\n'
                                               'memory.sync_status(frame)\n'
                                               "frame = _first_word(frame, 'target_x', "
                                               'memory.state.read(4294934560, 2))\n'
                                               "frame = _scene_render_arithmetic(memory, frame, 'target_x', "
                                               'low16(frame.target_x), 64, 16, True)\n'
                                               "frame = _first_word(frame, 'target_y', "
                                               'memory.state.read(4294934562, 2))\n'
                                               "frame = _scene_render_arithmetic(memory, frame, 'target_y', "
                                               'low16(frame.target_y), 64, 16, True)\n'
                                               "frame = _first_long(frame, 'unit', 0)\n"
                                               "frame = _first_long(frame, 'count', 0)\n"
                                               "frame = _first_word(frame, 'distance', 0)\n"
                                               'frame = first_replace(frame, '
                                               'roster=memory.cursor_at(242346))\n'
                                               'return _append_object_sprite_fields(memory, frame)'},
 'cycle_special_scene_palette_complete': {'signature': 'state, context',
                                          'returns': None,
                                          'flow': 'actual = '
                                                  'cycle_special_scene_palette_fields(SceneRefreshMemory(state), '
                                                  '_scene_controller_legacy_fields(state, context))\n'
                                                  'return _scene_controller_legacy_projection(state, '
                                                  'actual)'},
 'cycle_special_scene_palette_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                     'FirstDeploymentFrame',
                                        'returns': 'FirstDeploymentFrame',
                                        'flow': 'from .business_scene import _scene_render_compare, '
                                                '_scene_render_bit\n'
                                                'memory.frame(frame)\n'
                                                'memory.sync_status(frame)\n'
                                                'mode = memory.state.read(4294934747, 1)\n'
                                                'frame = _scene_render_compare(memory, frame, mode, 3, 8)\n'
                                                'if mode != 3:\n'
                                                '    return frame\n'
                                                'enabled = memory.state.read(4294934724, 1)\n'
                                                'frame = _scene_render_bit(memory, frame, enabled, 128)\n'
                                                'if not enabled & 128:\n'
                                                '    return frame\n'
                                                'tick = memory.state.read(4294964000, 2)\n'
                                                "frame = _first_word(frame, 'target_x', tick)\n"
                                                'frame, shifted_tick = '
                                                "_object_shift_word_right_fields(memory, frame, 'target_x', "
                                                'tick, 3)\n'
                                                'offset = shifted_tick & 6\n'
                                                "frame = _first_word(frame, 'target_x', offset)\n"
                                                'frame = first_replace(frame, '
                                                'roster=memory.cursor_at(260292))\n'
                                                'for displacement, address in ((0, 4294966018), (8, '
                                                '4294966020), (16, 4294966022)):\n'
                                                '    frame = _scene_refresh_emit(memory, frame, address, 2, '
                                                'frame.roster.word(offset, displacement))\n'
                                                'return memory.sync_status(frame)'},
 'draw_active_scene_object_complete': {'signature': 'state: SceneState, context: SceneControllerFrame',
                                       'returns': 'SceneControllerOutcome',
                                       'flow': 'actual = '
                                               'draw_active_scene_object_fields(SceneRefreshMemory(state), '
                                               '_scene_controller_legacy_fields(state, context))\n'
                                               'return '
                                               'SceneControllerOutcome(_scene_controller_legacy_projection(state, '
                                               'actual), None)'},
 'draw_active_scene_object_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                     'returns': 'FirstDeploymentFrame',
                                     'flow': 'from .business_scene import _scene_render_compare, '
                                             '_scene_render_arithmetic, _scene_render_asl_word\n'
                                             'memory.frame(frame)\n'
                                             'if frame.stack_cursor is None:\n'
                                             '    raise SceneRefreshBoundary(263238, frame, None)\n'
                                             'memory.sync_status(frame)\n'
                                             'gate = memory.state.read(4294934846, 2)\n'
                                             'frame = _scene_refresh_flags(memory, frame, gate, 2)\n'
                                             'if gate == 0:\n'
                                             '    frame = _scene_object_call_fields(memory, frame, 265364, '
                                             '263248)\n'
                                             "frame = _first_word(frame, 'target_x', "
                                             'frame.auxiliary.word())\n'
                                             "frame = _first_word(frame, 'target_x', low16(frame.target_x) & "
                                             '255)\n'
                                             "frame = _first_long(frame, 'target_y', 0)\n"
                                             'frame = first_replace(frame, roster=memory.cursor_at(263372))\n'
                                             "frame = _first_byte(frame, 'target_y', "
                                             'frame.roster.byte(low16(frame.target_x)))\n'
                                             'mode = memory.state.read(4294934747, 1)\n'
                                             'frame = _scene_render_compare(memory, frame, mode, 3, 8)\n'
                                             'if mode == 3:\n'
                                             "    frame = _first_byte(frame, 'target_y', "
                                             'frame.roster.byte(low16(frame.target_x), 4))\n'
                                             'side = memory.state.read(4294934820, 2)\n'
                                             'frame = _scene_refresh_flags(memory, frame, side, 2)\n'
                                             'frame = _scene_render_compare(memory, frame, '
                                             'frame.auxiliary.base, 4294935146, 32)\n'
                                             'if side == 0 and frame.auxiliary.base >= 4294935146 or (side '
                                             '!= 0 and frame.auxiliary.base < 4294935146):\n'
                                             '    frame = _scene_render_arithmetic(memory, frame, '
                                             "'target_y', low16(frame.target_y), 96, 16)\n"
                                             "frame = _first_word(frame, 'target_x', frame.auxiliary.word(0, "
                                             '8))\n'
                                             "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                             'low16(frame.target_x), 2)\n'
                                             "frame = _scene_render_arithmetic(memory, frame, 'target_y', "
                                             'low16(frame.target_y), low16(frame.target_x), 16)\n'
                                             'tick = memory.state.read(4294964000, 2)\n'
                                             "frame = _first_word(frame, 'target_x', tick)\n"
                                             'frame, shifted_tick = _object_shift_word_right_fields(memory, '
                                             "frame, 'target_x', tick, 3)\n"
                                             "frame = _first_word(frame, 'target_x', shifted_tick & 3)\n"
                                             "frame = _scene_render_arithmetic(memory, frame, 'target_x', "
                                             'low16(frame.target_x), low16(frame.target_y), 16)\n'
                                             "frame = _first_word(frame, 'distance', low16(frame.target_x))\n"
                                             "frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                             'low16(frame.target_x), 2)\n'
                                             'pointer = memory.state.read(u32(263380 + '
                                             's16(low16(frame.target_x))), 4)\n'
                                             'frame = first_replace(frame, '
                                             'roster=memory.cursor_at(pointer))\n'
                                             "frame = _first_word(frame, 'target_x', frame.auxiliary.word(0, "
                                             '2))\n'
                                             "frame = _first_word(frame, 'target_y', frame.auxiliary.word(0, "
                                             '4))\n'
                                             "frame = _first_word(frame, 'unit', 5)\n"
                                             "frame = _first_long(frame, 'count', 0)\n"
                                             "frame = _scene_render_asl_word(memory, frame, 'distance', "
                                             'low16(frame.distance), 1)\n'
                                             'frame = first_replace(frame, '
                                             'candidates=memory.cursor_at(264148))\n'
                                             "frame = _first_word(frame, 'distance', "
                                             'frame.candidates.word(low16(frame.distance)))\n'
                                             'return _append_object_sprite_fields(memory, frame)'},
 'integrate_scene_coordinates': {'signature': 'state: SceneState',
                                 'returns': 'CoordinateIntegrationOutcome',
                                 'flow': 'actual = '
                                         'integrate_scene_coordinates_fields(SceneRefreshMemory(state), '
                                         'FirstDeploymentFrame.unobserved())\n'
                                         'return CoordinateIntegrationOutcome(actual.target_x, '
                                         'actual.target_y)'},
 'integrate_scene_coordinates_complete': {'signature': 'state, frame',
                                          'returns': None,
                                          'flow': 'actual = '
                                                  'integrate_scene_coordinates_fields(SceneRefreshMemory(state), '
                                                  '_scene_controller_legacy_fields(state, frame))\n'
                                                  'return _scene_controller_legacy_projection(state, '
                                                  'actual)'},
 'integrate_scene_coordinates_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                     'FirstDeploymentFrame',
                                        'returns': 'FirstDeploymentFrame',
                                        'flow': 'from .business_scene import _scene_render_arithmetic\n'
                                                'memory.frame(frame)\n'
                                                'for high_address, low_address, velocity_address in '
                                                '((4294934564, 4294934572, 4294934584), (4294934566, '
                                                '4294934574, 4294934586), (4294934560, 4294934580, '
                                                '4294934592)):\n'
                                                '    memory.sync_status(frame)\n'
                                                '    high = memory.state.read(high_address, 2)\n'
                                                "    frame = _first_word(frame, 'target_x', high)\n"
                                                '    if frame.target_x is not None:\n'
                                                "        frame = _first_long(frame, 'target_x', "
                                                'swap_words(frame.target_x))\n'
                                                '    low = memory.state.read(low_address, 2)\n'
                                                '    frame = first_replace(frame, target_x=u32(high << 16 | '
                                                'low))\n'
                                                '    frame = _scene_refresh_flags(memory, frame, low, 2)\n'
                                                "    frame = _first_long(frame, 'target_y', 0)\n"
                                                '    velocity = memory.state.read(velocity_address, 2)\n'
                                                "    frame = _first_word(frame, 'target_y', velocity)\n"
                                                '    adding = bool(velocity & 32768)\n'
                                                '    if adding:\n'
                                                "        frame = _first_word(frame, 'target_y', velocity & "
                                                '32767)\n'
                                                '    frame = _object_shift_velocity_fields(memory, frame, '
                                                '8)\n'
                                                '    frame = _scene_render_arithmetic(memory, frame, '
                                                "'target_x', frame.target_x, frame.target_y, 32, not "
                                                'adding)\n'
                                                '    frame = _scene_refresh_emit(memory, frame, low_address, '
                                                '2, low16(frame.target_x))\n'
                                                "    frame = _first_long(frame, 'target_x', "
                                                'swap_words(frame.target_x))\n'
                                                '    frame = _scene_refresh_emit(memory, frame, '
                                                'high_address, 2, low16(frame.target_x))\n'
                                                'return memory.sync_status(frame)'}})

# B31 sole object roster/label/random fields; ordinary native lowerers unchanged.
APPROVED.setdefault('business_movement_support',set()).update({'_movement_binary_flags', '_movement_divu_word', '_movement_multiply_word'})
APPROVED.setdefault('business_scene',set()).update({'write_vdp_swapped_byte_rle_stream_fields', '_scene_render_asl_word', 'snapshot_and_clear_scene_palette_fields', '_scene_render_compare', 'read_vdp_plane_rle_rows_fields', '_scene_render_arithmetic', 'copy_scene_palette_variant_fields', 'sample_random_preserving_seed_fields', 'begin_scene_palette_darken_fields'})
APPROVED.setdefault('business_battle',set()).update({'_presentation_call_fields'})
APPROVED.setdefault('contexts_battle',set()).update({'BattlePresentationMemory'})
APPROVED.setdefault('business_services',set()).update({'enqueue_sound_command_fields', 'clear_video_sprite_plane_fields', 'wait_for_scene_sound_byte_fields'})
DECLARATIONS.update({'_normalize_object_squad_fields': {'signature': 'state',
                                    'returns': None,
                                    'flow': 'frame = '
                                            'normalize_object_squad_size_fields(SceneRefreshMemory(state), '
                                            'FirstDeploymentFrame.unobserved())\n'
                                            'return (frame.target_x, frame.target_y)'},
 '_object_adjust_word_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                             'address: Long, amount: Word, subtract: bool=False',
                                'returns': 'FirstDeploymentFrame',
                                'flow': 'from ..high_level_main_flows.business_movement_support import '
                                        '_movement_binary_flags\n'
                                        'memory.sync_status(frame)\n'
                                        'previous = memory.state.read(address, 2)\n'
                                        'frame, value = _movement_binary_flags(memory.state, frame, '
                                        'previous, amount, 16, subtract)\n'
                                        'memory.state.write(address, 2, value)\n'
                                        'return memory.sync_status(frame)'},
 '_object_clear_word_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                            'address: Long',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'memory.sync_status(frame)\n'
                                       'memory.state.read(address, 2)\n'
                                       'return _scene_refresh_emit(memory, frame, address, 2, 0)'},
 '_object_count_draw_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                            'continuation: Long, bound: Word, bias: Word',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'from .business_scene import _scene_render_compare, '
                                       '_scene_render_arithmetic\n'
                                       'while True:\n'
                                       '    frame = _scene_object_call_fields(memory, frame, 243490, '
                                       'continuation)\n'
                                       '    choice = low16(frame.target_x) & 15\n'
                                       "    frame = _first_word(frame, 'target_x', choice)\n"
                                       '    frame = _scene_render_compare(memory, frame, choice, bound, 16)\n'
                                       '    accepted = choice <= bound if continuation == 268364 else choice '
                                       '<= bound\n'
                                       '    if accepted:\n'
                                       "        frame = _scene_render_arithmetic(memory, frame, 'target_x', "
                                       'choice, bias, 16)\n'
                                       '        return _scene_refresh_emit(memory, frame, 4294934760, 2, '
                                       'low16(frame.target_x))'},
 '_reset_object_action_controls': {'signature': 'state',
                                   'returns': None,
                                   'flow': '_reset_object_action_controls_fields(SceneRefreshMemory(state), '
                                           'FirstDeploymentFrame.unobserved())'},
 '_reset_object_action_controls_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                       'FirstDeploymentFrame',
                                          'returns': 'FirstDeploymentFrame',
                                          'flow': 'for address in (4294934860, 4294934862, 4294934864, '
                                                  '4294934866, 4294934868, 4294934870, 4294934872, '
                                                  '4294934874, 4294934876, 4294934878, 4294934880, '
                                                  '4294934882, 4294934884, 4294934886, 4294934888):\n'
                                                  '    frame = _object_clear_word_fields(memory, frame, '
                                                  'address)\n'
                                                  'return frame'},
 '_scene_object_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                            'target: Long, continuation: Long',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'from ..high_level_gameplay_flow.business_battle import '
                                       '_presentation_call_fields\n'
                                       'from ..high_level_gameplay_flow.contexts_battle import '
                                       'BattlePresentationMemory\n'
                                       'if (target, continuation) not in ((26830, 251500), (252320, 251510), '
                                       '(240532, 251520), (240160, 251550), (240266, 251554), (262940, '
                                       '251568), (268278, 251870), (32906, 251882), (33736, 251898), '
                                       '(242312, 251906), (260240, 251910), (239992, 251914), (253112, '
                                       '251918), (262972, 251924), (242236, 251930), (252132, 251934), '
                                       '(240466, 252438), (240466, 252452), (240466, 252466), (240466, '
                                       '252480), (240466, 252494), (240334, 252528), (240334, 252562), '
                                       '(240334, 252590), (240334, 252618), (243490, 268364), (243490, '
                                       '268396), (243490, 268434), (259266, 268460), (243490, 268622)):\n'
                                       "    raise ValueError('original scene object child/continuation pair "
                                       "required')\n"
                                       'memory.frame(frame)\n'
                                       'def child(actual_memory, entered):\n'
                                       '    scene = SceneRefreshMemory(actual_memory.state)\n'
                                       '    if target == 26830:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'clear_video_sprite_plane_fields\n'
                                       '        return clear_video_sprite_plane_fields(scene, entered)\n'
                                       '    if target == 252320:\n'
                                       '        return initialize_scene_object_video_fields(scene, entered)\n'
                                       '    if target == 240466:\n'
                                       '        from .business_scene import '
                                       'write_vdp_swapped_byte_rle_stream_fields\n'
                                       '        return write_vdp_swapped_byte_rle_stream_fields(scene, '
                                       'entered)\n'
                                       '    if target == 240334:\n'
                                       '        from .business_scene import read_vdp_plane_rle_rows_fields\n'
                                       '        return read_vdp_plane_rle_rows_fields(scene, entered)\n'
                                       '    if target == 240532:\n'
                                       '        from .business_scene import '
                                       'copy_scene_palette_variant_fields\n'
                                       '        return copy_scene_palette_variant_fields(scene, entered)\n'
                                       '    if target == 240160:\n'
                                       '        from .business_scene import '
                                       'begin_scene_palette_darken_fields\n'
                                       '        return begin_scene_palette_darken_fields(scene, entered)\n'
                                       '    if target == 240266:\n'
                                       '        from .business_scene import '
                                       'snapshot_and_clear_scene_palette_fields\n'
                                       '        return snapshot_and_clear_scene_palette_fields(scene, '
                                       'entered)\n'
                                       '    if target == 262940:\n'
                                       '        return clear_scene_object_label_plane_fields(scene, '
                                       'entered)\n'
                                       '    if target == 268278:\n'
                                       '        return initialize_scene_object_roster_fields(scene, '
                                       'entered)\n'
                                       '    if target == 259266:\n'
                                       '        return normalize_object_squad_size_fields(scene, entered)\n'
                                       '    if target == 243490:\n'
                                       '        from .business_scene import '
                                       'sample_random_preserving_seed_fields\n'
                                       '        return sample_random_preserving_seed_fields(scene, entered)\n'
                                       '    if target == 32906:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'enqueue_sound_command_fields\n'
                                       '        return enqueue_sound_command_fields(scene, entered)\n'
                                       '    if target == 33736:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'wait_for_scene_sound_byte_fields\n'
                                       '        return wait_for_scene_sound_byte_fields(scene, entered)\n'
                                       '    raise SceneRefreshBoundary(target, entered, continuation)\n'
                                       'return '
                                       '_presentation_call_fields(BattlePresentationMemory(memory.state), '
                                       'frame, continuation, child)'},
 'clear_scene_object_label_plane_complete': {'signature': 'state, context',
                                             'returns': None,
                                             'flow': 'fields = '
                                                     'clear_scene_object_label_plane_fields(SceneRefreshMemory(state), '
                                                     '_scene_controller_legacy_fields(state, context))\n'
                                                     'return _scene_controller_legacy_projection(state, '
                                                     'fields)'},
 'clear_scene_object_label_plane_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                        'FirstDeploymentFrame',
                                           'returns': 'FirstDeploymentFrame',
                                           'flow': 'memory.frame(frame)\n'
                                                   'frame = _scene_refresh_emit(memory, frame, 12582916, 4, '
                                                   '1073741827)\n'
                                                   'frame = first_replace(frame, '
                                                   'scratch=memory.cursor_at(12582912))\n'
                                                   "frame = _first_word(frame, 'offset_y', 1024)\n"
                                                   "frame = _first_word(frame, 'choice', 2047)\n"
                                                   'counter = 2047\n'
                                                   'while True:\n'
                                                   '    frame = _scene_refresh_emit(memory, frame, '
                                                   'frame.scratch.base, 2, low16(frame.offset_y))\n'
                                                   "    frame = _scene_refresh_decrement(frame, 'choice', "
                                                   'counter)\n'
                                                   '    counter = u16(counter - 1)\n'
                                                   '    if counter == 65535:\n'
                                                   '        return memory.sync_status(frame)'},
 'initialize_scene_object_roster_complete': {'signature': 'state: SceneState, context: SceneControllerFrame',
                                             'returns': 'SceneControllerFrame',
                                             'flow': 'fields = '
                                                     'initialize_scene_object_roster_fields(SceneRefreshMemory(state), '
                                                     '_scene_controller_legacy_fields(state, context))\n'
                                                     'return _scene_controller_legacy_projection(state, '
                                                     'fields)'},
 'initialize_scene_object_roster_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                        'FirstDeploymentFrame',
                                           'returns': 'FirstDeploymentFrame',
                                           'flow': 'from .business_scene import _scene_render_compare, '
                                                   '_scene_render_arithmetic, _scene_render_asl_word\n'
                                                   'from ..high_level_main_flows.business_movement_support '
                                                   'import _movement_multiply_word, _movement_divu_word\n'
                                                   'memory.frame(frame)\n'
                                                   'if frame.stack_cursor is None:\n'
                                                   '    raise SceneRefreshBoundary(268278, frame, None)\n'
                                                   "frame = _first_word(frame, 'target_x', 255)\n"
                                                   'frame = first_replace(frame, '
                                                   'auxiliary=memory.cursor_at(4294934890))\n'
                                                   'counter = 255\n'
                                                   'while True:\n'
                                                   '    frame = _object_clear_word_fields(memory, frame, '
                                                   'frame.auxiliary.base)\n'
                                                   '    frame = first_replace(frame, '
                                                   'auxiliary=frame.auxiliary.advance(2))\n'
                                                   "    frame = _scene_refresh_decrement(frame, 'target_x', "
                                                   'counter)\n'
                                                   '    counter = u16(counter - 1)\n'
                                                   '    if counter == 65535:\n'
                                                   '        break\n'
                                                   'mode = memory.state.read(4294934746, 1)\n'
                                                   'frame = _scene_render_compare(memory, frame, mode, 1, '
                                                   '8)\n'
                                                   'if mode == 1:\n'
                                                   '    return _reset_object_action_controls_fields(memory, '
                                                   'frame)\n'
                                                   'mode = memory.state.read(4294934746, 1)\n'
                                                   'frame = _scene_render_compare(memory, frame, mode, 2, '
                                                   '8)\n'
                                                   'if mode == 2:\n'
                                                   '    return _reset_object_action_controls_fields(memory, '
                                                   'frame)\n'
                                                   'for address in (4294934760, 4294934772, 4294934774, '
                                                   '4294934776):\n'
                                                   '    frame = _object_clear_word_fields(memory, frame, '
                                                   'address)\n'
                                                   'total = memory.state.read(4294934756, 2)\n'
                                                   'frame = _scene_refresh_flags(memory, frame, total, 2)\n'
                                                   'if total != 0:\n'
                                                   '    frame = _scene_refresh_emit(memory, frame, '
                                                   '4294934760, 2, 1)\n'
                                                   '    total = memory.state.read(4294934756, 2)\n'
                                                   '    frame = _scene_render_compare(memory, frame, total, '
                                                   '100, 16)\n'
                                                   '    if total >= 100:\n'
                                                   '        total = memory.state.read(4294934756, 2)\n'
                                                   '        frame = _scene_render_compare(memory, frame, '
                                                   'total, 1500, 16)\n'
                                                   '        if total < 1500:\n'
                                                   '            frame = _object_count_draw_fields(memory, '
                                                   'frame, 268364, 9, 1)\n'
                                                   '        else:\n'
                                                   '            total = memory.state.read(4294934756, 2)\n'
                                                   '            frame = _scene_render_compare(memory, frame, '
                                                   'total, 5000, 16)\n'
                                                   '            if total < 5000:\n'
                                                   '                frame = '
                                                   '_object_count_draw_fields(memory, frame, 268396, 5, 5)\n'
                                                   '            else:\n'
                                                   '                frame = _scene_refresh_emit(memory, '
                                                   'frame, 4294934760, 2, 15)\n'
                                                   '                total = memory.state.read(4294934756, '
                                                   '2)\n'
                                                   '                frame = _scene_render_compare(memory, '
                                                   'frame, total, 10000, 16)\n'
                                                   '                if total < 10000:\n'
                                                   '                    frame = '
                                                   '_object_count_draw_fields(memory, frame, 268434, 5, 10)\n'
                                                   '    frame = _scene_object_call_fields(memory, frame, '
                                                   '259266, 268460)\n'
                                                   '    for threshold, first_count, second_count in ((100, '
                                                   '0, 2), (200, 1, 3), (300, 3, 4), (400, 5, 5), (500, 6, '
                                                   '6), (600, 7, 7)):\n'
                                                   "        frame = _first_long(frame, 'target_x', "
                                                   'first_count)\n'
                                                   "        frame = _first_long(frame, 'target_y', "
                                                   'second_count)\n'
                                                   '        quality = memory.state.read(4294934800, 2)\n'
                                                   '        frame = _scene_render_compare(memory, frame, '
                                                   'quality, threshold, 16)\n'
                                                   '        if quality <= threshold:\n'
                                                   '            break\n'
                                                   '    else:\n'
                                                   "        frame = _first_long(frame, 'target_x', 8)\n"
                                                   "        frame = _first_long(frame, 'target_y', 8)\n"
                                                   '    for address in (4294934772, 4294934774, '
                                                   '4294934776):\n'
                                                   '        frame = _object_clear_word_fields(memory, frame, '
                                                   'address)\n'
                                                   "    frame = _first_word(frame, 'unit', "
                                                   'memory.state.read(4294934760, 2))\n'
                                                   '    frame = _scene_render_arithmetic(memory, frame, '
                                                   "'unit', low16(frame.unit), low16(frame.target_x), 16, "
                                                   'True)\n'
                                                   '    if low16(frame.unit) & 32768:\n'
                                                   '        frame = _scene_refresh_emit(memory, frame, '
                                                   '4294934772, 2, memory.state.read(4294934760, 2))\n'
                                                   '    else:\n'
                                                   '        frame = _scene_refresh_emit(memory, frame, '
                                                   '4294934772, 2, low16(frame.target_x))\n'
                                                   '        frame = _scene_refresh_emit(memory, frame, '
                                                   '4294934774, 2, low16(frame.unit))\n'
                                                   '        frame = _scene_render_arithmetic(memory, frame, '
                                                   "'unit', low16(frame.unit), low16(frame.target_y), 16, "
                                                   'True)\n'
                                                   '        if not low16(frame.unit) & 32768:\n'
                                                   '            frame = _scene_refresh_emit(memory, frame, '
                                                   '4294934774, 2, low16(frame.target_y))\n'
                                                   '            frame = _scene_refresh_emit(memory, frame, '
                                                   '4294934776, 2, low16(frame.unit))\n'
                                                   'include_override = total != 0\n'
                                                   'while True:\n'
                                                   '    if include_override:\n'
                                                   '        mode = memory.state.read(4294934747, 1)\n'
                                                   '        frame = _scene_render_compare(memory, frame, '
                                                   'mode, 3, 8)\n'
                                                   '        if mode == 3:\n'
                                                   '            frame = _object_clear_word_fields(memory, '
                                                   'frame, 4294934772)\n'
                                                   '            frame = _scene_refresh_emit(memory, frame, '
                                                   '4294934774, 2, memory.state.read(4294934760, 2))\n'
                                                   '            frame = _object_clear_word_fields(memory, '
                                                   'frame, 4294934776)\n'
                                                   '    frame = _scene_object_call_fields(memory, frame, '
                                                   '243490, 268622)\n'
                                                   '    choice = low16(frame.target_x) & 7\n'
                                                   "    frame = _first_word(frame, 'target_x', choice)\n"
                                                   '    frame = _scene_render_compare(memory, frame, choice, '
                                                   '4, 16)\n'
                                                   '    if choice <= 4:\n'
                                                   '        break\n'
                                                   '    include_override = True\n'
                                                   'frame = _scene_refresh_emit(memory, frame, 4294934858, '
                                                   '2, choice)\n'
                                                   'frame = _scene_render_asl_word(memory, frame, '
                                                   "'target_x', choice, 2)\n"
                                                   'frame = first_replace(frame, '
                                                   'roster=memory.cursor_at(268888))\n'
                                                   'pointer = frame.roster.long(s16(low16(frame.target_x)))\n'
                                                   'frame = first_replace(frame, '
                                                   'scratch=memory.cursor_at(pointer))\n'
                                                   "frame = _first_word(frame, 'target_x', "
                                                   'memory.state.read(4294934772, 2))\n'
                                                   "frame = _first_word(frame, 'target_y', "
                                                   'memory.state.read(4294934774, 2))\n'
                                                   "frame = _first_word(frame, 'unit', "
                                                   'memory.state.read(4294934776, 2))\n'
                                                   "frame = _first_long(frame, 'count', 0)\n"
                                                   'frame = first_replace(frame, '
                                                   'auxiliary=memory.cursor_at(4294934890))\n'
                                                   'while True:\n'
                                                   '    frame = _scene_refresh_flags(memory, frame, '
                                                   'low16(frame.count), 2)\n'
                                                   '    if low16(frame.count) == 0:\n'
                                                   '        kind, consume = (32771, None)\n'
                                                   '    else:\n'
                                                   '        frame = _scene_refresh_flags(memory, frame, '
                                                   'low16(frame.target_x), 2)\n'
                                                   '        if low16(frame.target_x) != 0:\n'
                                                   "            kind, consume = (32770, 'target_x')\n"
                                                   '        else:\n'
                                                   '            frame = _scene_refresh_flags(memory, frame, '
                                                   'low16(frame.target_y), 2)\n'
                                                   '            if low16(frame.target_y) != 0:\n'
                                                   "                kind, consume = (32769, 'target_y')\n"
                                                   '            else:\n'
                                                   '                frame = _scene_refresh_flags(memory, '
                                                   'frame, low16(frame.unit), 2)\n'
                                                   '                if low16(frame.unit) == 0:\n'
                                                   '                    break\n'
                                                   "                kind, consume = (32768, 'unit')\n"
                                                   '    for displacement in (2, 4):\n'
                                                   '        value = frame.scratch.word()\n'
                                                   '        frame = first_replace(frame, '
                                                   'scratch=frame.scratch.advance(2))\n'
                                                   '        frame = _scene_refresh_emit(memory, frame, '
                                                   'u32(frame.auxiliary.base + displacement), 2, value)\n'
                                                   "    if consume == 'unit':\n"
                                                   '        frame = _scene_render_arithmetic(memory, frame, '
                                                   'consume, low16(frame.carrier(consume)), 1, 16, True)\n'
                                                   '    frame = _scene_refresh_emit(memory, frame, '
                                                   'frame.auxiliary.base, 2, kind)\n'
                                                   "    if consume is not None and consume != 'unit':\n"
                                                   '        frame = _scene_render_arithmetic(memory, frame, '
                                                   'consume, low16(frame.carrier(consume)), 1, 16, True)\n'
                                                   '    frame = _scene_render_arithmetic(memory, frame, '
                                                   "'count', low16(frame.count), 1, 16)\n"
                                                   '    frame = first_replace(frame, '
                                                   'auxiliary=frame.auxiliary.advance(16))\n'
                                                   "frame = _first_word(frame, 'target_x', "
                                                   'memory.state.read(4294934788, 2))\n'
                                                   "frame = _first_word(frame, 'target_y', "
                                                   'memory.state.read(4294934784, 2))\n'
                                                   'frame = _movement_multiply_word(memory.state, frame, '
                                                   "'target_y', low16(frame.target_x))\n"
                                                   'frame = _movement_divu_word(memory.state, frame, '
                                                   "'target_y', 100, 268762)\n"
                                                   "frame = _first_word(frame, 'target_x', 14)\n"
                                                   "frame = _first_word(frame, 'unit', "
                                                   'memory.state.read(4294934768, 2))\n'
                                                   'frame = first_replace(frame, '
                                                   'auxiliary=memory.cursor_at(4294934906))\n'
                                                   'counter = 14\n'
                                                   'while True:\n'
                                                   '    frame = _scene_refresh_emit(memory, frame, '
                                                   'u32(frame.auxiliary.base + 12), 2, '
                                                   'low16(frame.target_y))\n'
                                                   '    frame = _scene_refresh_emit(memory, frame, '
                                                   'u32(frame.auxiliary.base + 14), 2, '
                                                   'memory.state.read(4294934764, 2))\n'
                                                   '    frame = _scene_refresh_flags(memory, frame, '
                                                   'low16(frame.unit), 2)\n'
                                                   '    if low16(frame.unit) != 0:\n'
                                                   '        frame = _scene_render_arithmetic(memory, frame, '
                                                   "'unit', low16(frame.unit), 1, 16, True)\n"
                                                   '        frame = _object_adjust_word_fields(memory, '
                                                   'frame, u32(frame.auxiliary.base + 14), 1)\n'
                                                   '    frame = first_replace(frame, '
                                                   'auxiliary=frame.auxiliary.advance(16))\n'
                                                   "    frame = _scene_refresh_decrement(frame, 'target_x', "
                                                   'counter)\n'
                                                   '    counter = u16(counter - 1)\n'
                                                   '    if counter == 65535:\n'
                                                   '        break\n'
                                                   "frame = _first_word(frame, 'target_x', "
                                                   'memory.state.read(4294934788, 2))\n'
                                                   'frame = _scene_render_arithmetic(memory, frame, '
                                                   "'target_x', low16(frame.target_x), "
                                                   'memory.state.read(4294934792, 2), 16)\n'
                                                   'frame = _scene_refresh_emit(memory, frame, 4294934902, '
                                                   '2, low16(frame.target_x))\n'
                                                   'frame = _scene_refresh_emit(memory, frame, 4294934904, '
                                                   '2, memory.state.read(4294934796, 2))\n'
                                                   'return _reset_object_action_controls_fields(memory, '
                                                   'frame)'},
 'normalize_object_squad_size_complete': {'signature': 'state, context',
                                          'returns': None,
                                          'flow': 'fields = '
                                                  'normalize_object_squad_size_fields(SceneRefreshMemory(state), '
                                                  '_scene_controller_legacy_fields(state, context))\n'
                                                  'return _scene_controller_legacy_projection(state, '
                                                  'fields)'},
 'normalize_object_squad_size_fields': {'signature': 'memory: SceneRefreshMemory, frame: '
                                                     'FirstDeploymentFrame',
                                        'returns': 'FirstDeploymentFrame',
                                        'flow': 'from .business_scene import _scene_render_compare\n'
                                                'from ..high_level_main_flows.business_movement_support '
                                                'import _movement_divu_word\n'
                                                'memory.frame(frame)\n'
                                                'while True:\n'
                                                "    frame = _first_long(frame, 'target_x', 0)\n"
                                                "    frame = _first_long(frame, 'target_y', 0)\n"
                                                '    memory.sync_status(frame)\n'
                                                "    frame = _first_word(frame, 'target_x', "
                                                'memory.state.read(4294934756, 2))\n'
                                                "    frame = _first_word(frame, 'target_y', "
                                                'memory.state.read(4294934760, 2))\n'
                                                '    count = low16(frame.target_y)\n'
                                                '    if count == 0:\n'
                                                '        frame = _object_adjust_word_fields(memory, frame, '
                                                '4294934760, 1)\n'
                                                '        continue\n'
                                                '    frame = _scene_render_compare(memory, frame, count, 15, '
                                                '16)\n'
                                                '    if count > 15:\n'
                                                '        frame = _object_adjust_word_fields(memory, frame, '
                                                '4294934760, 1, True)\n'
                                                '        continue\n'
                                                '    frame = _movement_divu_word(memory.state, frame, '
                                                "'target_x', count, 259302)\n"
                                                '    quotient = low16(frame.target_x)\n'
                                                '    frame = _scene_render_compare(memory, frame, quotient, '
                                                '1000, 16)\n'
                                                '    if quotient > 1000:\n'
                                                '        frame = _object_adjust_word_fields(memory, frame, '
                                                '4294934760, 1)\n'
                                                '        continue\n'
                                                '    frame = _scene_render_compare(memory, frame, quotient, '
                                                '100, 16)\n'
                                                '    if quotient <= 100:\n'
                                                '        live_count = memory.state.read(4294934760, 2)\n'
                                                '        frame = _scene_render_compare(memory, frame, '
                                                'live_count, 1, 16)\n'
                                                '        if live_count > 1:\n'
                                                '            frame = _object_adjust_word_fields(memory, '
                                                'frame, 4294934760, 1, True)\n'
                                                '            continue\n'
                                                '    frame = _scene_refresh_emit(memory, frame, 4294934764, '
                                                '2, quotient)\n'
                                                "    frame = _first_long(frame, 'target_x', "
                                                'swap_words(frame.target_x))\n'
                                                '    return _scene_refresh_emit(memory, frame, 4294934768, '
                                                '2, low16(frame.target_x))'}})

# B23 sole live label/glyph fields; ordinary native lowerers unchanged.
APPROVED.setdefault('business_battle',set()).update({'_presentation_call_fields'})
APPROVED.setdefault('contexts_battle',set()).update({'BattlePresentationMemory'})
APPROVED.setdefault('business_services',set()).update({'enqueue_sound_command_fields', 'wait_for_scene_sound_byte_fields', 'clear_video_sprite_plane_fields'})
APPROVED.setdefault('business_scene',set()).update({'read_vdp_plane_rle_rows_fields', 'write_vdp_swapped_byte_rle_stream_fields', 'snapshot_and_clear_scene_palette_fields', 'begin_scene_palette_darken_fields', 'copy_scene_palette_variant_fields'})
DECLARATIONS.update({'_scene_object_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, '
                                            'target: Long, continuation: Long',
                               'returns': 'FirstDeploymentFrame',
                               'flow': 'from ..high_level_gameplay_flow.business_battle import '
                                       '_presentation_call_fields\n'
                                       'from ..high_level_gameplay_flow.contexts_battle import '
                                       'BattlePresentationMemory\n'
                                       'if (target, continuation) not in ((26830, 251500), (252320, 251510), '
                                       '(240532, 251520), (240160, 251550), (240266, 251554), (262940, '
                                       '251568), (268278, 251870), (32906, 251882), (33736, 251898), '
                                       '(242312, 251906), (260240, 251910), (239992, 251914), (253112, '
                                       '251918), (262972, 251924), (242236, 251930), (252132, 251934), '
                                       '(240466, 252438), (240466, 252452), (240466, 252466), (240466, '
                                       '252480), (240466, 252494), (240334, 252528), (240334, 252562), '
                                       '(240334, 252590), (240334, 252618)):\n'
                                       "    raise ValueError('original scene object child/continuation pair "
                                       "required')\n"
                                       'memory.frame(frame)\n'
                                       'def child(actual_memory, entered):\n'
                                       '    scene = SceneRefreshMemory(actual_memory.state)\n'
                                       '    if target == 26830:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'clear_video_sprite_plane_fields\n'
                                       '        return clear_video_sprite_plane_fields(scene, entered)\n'
                                       '    if target == 252320:\n'
                                       '        return initialize_scene_object_video_fields(scene, entered)\n'
                                       '    if target == 240466:\n'
                                       '        from .business_scene import '
                                       'write_vdp_swapped_byte_rle_stream_fields\n'
                                       '        return write_vdp_swapped_byte_rle_stream_fields(scene, '
                                       'entered)\n'
                                       '    if target == 240334:\n'
                                       '        from .business_scene import read_vdp_plane_rle_rows_fields\n'
                                       '        return read_vdp_plane_rle_rows_fields(scene, entered)\n'
                                       '    if target == 240532:\n'
                                       '        from .business_scene import '
                                       'copy_scene_palette_variant_fields\n'
                                       '        return copy_scene_palette_variant_fields(scene, entered)\n'
                                       '    if target == 240160:\n'
                                       '        from .business_scene import '
                                       'begin_scene_palette_darken_fields\n'
                                       '        return begin_scene_palette_darken_fields(scene, entered)\n'
                                       '    if target == 240266:\n'
                                       '        from .business_scene import '
                                       'snapshot_and_clear_scene_palette_fields\n'
                                       '        return snapshot_and_clear_scene_palette_fields(scene, '
                                       'entered)\n'
                                       '    if target == 32906:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'enqueue_sound_command_fields\n'
                                       '        return enqueue_sound_command_fields(scene, entered)\n'
                                       '    if target == 33736:\n'
                                       '        from ..high_level_gameplay_flow.business_services import '
                                       'wait_for_scene_sound_byte_fields\n'
                                       '        return wait_for_scene_sound_byte_fields(scene, entered)\n'
                                       '    raise SceneRefreshBoundary(target, entered, continuation)\n'
                                       'return '
                                       '_presentation_call_fields(BattlePresentationMemory(memory.state), '
                                       'frame, continuation, child)'}})

# Current selected dispatcher DECL, last-write only; original business body unchanged.
DECLARATIONS.update({'dispatch_scene_object_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                        'returns': 'FirstDeploymentFrame',
                                        'flow': 'from .business_scene import _scene_render_asl_word\n'
                                                'memory.frame(frame)\n'
                                                'memory.sync_status(frame)\n'
                                                'phase = memory.state.read(4294934842, 2)\n'
                                                "frame = _first_word(frame, 'target_x', phase)\n"
                                                "frame = _scene_render_asl_word(memory, frame, 'target_x', phase, 2)\n"
                                                'target = u32(253122 + s16(u16(phase << 2)))\n'
                                                'if target == 253122:\n'
                                                '    from ..high_level_dynamic_flows.business_early_phase import '
                                                'step_main_scene_phase_fields\n'
                                                '    return step_main_scene_phase_fields(memory, frame)\n'
                                                'if target in (253134, 253138, 253142, 253146, 253150, 253154):\n'
                                                '    from ..high_level_dynamic_flows.business_early_phase import '
                                                '_allocation_known_fields\n'
                                                '    return _allocation_known_fields(memory, frame, target)\n'
                                                'raise SceneRefreshBoundary(target, frame, None)'}})

# D59 current-field admission: synchronize only these three existing full bodies.
DECLARATIONS.update({'_scene_object_call_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "from ..high_level_gameplay_flow.business_battle import _presentation_call_fields\nfrom ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory\nif (target, continuation) not in ((26830, 251500), (252320, 251510), (240532, 251520), (240160, 251550), (240266, 251554), (262940, 251568), (268278, 251870), (32906, 251882), (33736, 251898), (242312, 251906), (260240, 251910), (239992, 251914), (253112, 251918), (262972, 251924), (242236, 251930), (252132, 251934), (240466, 252438), (240466, 252452), (240466, 252466), (240466, 252480), (240466, 252494), (240334, 252528), (240334, 252562), (240334, 252590), (240334, 252618), (243490, 268364), (243490, 268396), (243490, 268434), (259266, 268460), (243490, 268622), (265364, 263248), (263178, 262976), (263238, 263000), (243490, 265460), (266700, 265470), (265512, 265474), (266658, 266596), (266588, 267518), (267514, 266758), (267514, 266798), (267514, 266816), (267514, 266834), (267514, 266884), (267514, 266924), (267514, 266942), (267514, 266960), (267514, 266994), (267514, 267024), (267514, 267054), (267514, 267084), (267514, 267124), (267514, 267142), (267514, 267160), (267514, 267190), (267514, 267208), (267514, 267226), (267514, 267256), (267514, 267274), (267514, 267292), (267514, 267322), (267514, 267340), (267514, 267358), (32906, 267414)):\n    raise ValueError('original scene object child/continuation pair required')\nmemory.frame(frame)\ndef child(actual_memory, entered):\n    scene = SceneRefreshMemory(actual_memory.state)\n    if target == 26830:\n        from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields\n        return clear_video_sprite_plane_fields(scene, entered)\n    if target == 252320:\n        return initialize_scene_object_video_fields(scene, entered)\n    if target == 240466:\n        from .business_scene import write_vdp_swapped_byte_rle_stream_fields\n        return write_vdp_swapped_byte_rle_stream_fields(scene, entered)\n    if target == 240334:\n        from .business_scene import read_vdp_plane_rle_rows_fields\n        return read_vdp_plane_rle_rows_fields(scene, entered)\n    if target == 240532:\n        from .business_scene import copy_scene_palette_variant_fields\n        return copy_scene_palette_variant_fields(scene, entered)\n    if target == 240160:\n        from .business_scene import begin_scene_palette_darken_fields\n        return begin_scene_palette_darken_fields(scene, entered)\n    if target == 240266:\n        from .business_scene import snapshot_and_clear_scene_palette_fields\n        return snapshot_and_clear_scene_palette_fields(scene, entered)\n    if target == 262940:\n        return clear_scene_object_label_plane_fields(scene, entered)\n    if target == 268278:\n        return initialize_scene_object_roster_fields(scene, entered)\n    if target == 259266:\n        return normalize_object_squad_size_fields(scene, entered)\n    if target == 243490:\n        from .business_scene import sample_random_preserving_seed_fields\n        return sample_random_preserving_seed_fields(scene, entered)\n    if target == 242312:\n        return append_scene_center_marker_fields(scene, entered)\n    if target == 260240:\n        return cycle_special_scene_palette_fields(scene, entered)\n    if target == 252132:\n        return integrate_scene_coordinates_fields(scene, entered)\n    if target == 242236:\n        from .business_scene import finish_actor_sprite_chains_fields\n        return finish_actor_sprite_chains_fields(scene, entered)\n    if target == 253112:\n        return dispatch_scene_object_phase_fields(scene, entered)\n    if target == 262972:\n        return advance_scene_object_actions_fields(scene, entered)\n    if target == 263178:\n        return rebuild_depth_sorted_object_queue_fields(scene, entered)\n    if target == 263238:\n        return draw_active_scene_object_fields(scene, entered)\n    if target == 265364:\n        return update_selected_object_action_fields(scene, entered)\n    if target == 265512:\n        return read_object_action_mode_fields(scene, entered)\n    if target == 266658:\n        return offset_scene_object_position_fields(scene, entered)\n    if target == 266588:\n        return probe_scene_object_overlap_fields(scene, entered)\n    if target == 239992:\n        from .business_scene import advance_scene_palette_fade_fields\n        return advance_scene_palette_fade_fields(scene, entered)\n    if target == 267514:\n        return probe_opposing_object_overlap_fields(scene, entered)\n    if target == 32906:\n        from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields\n        return enqueue_sound_command_fields(scene, entered)\n    if target == 33736:\n        from ..high_level_gameplay_flow.business_services import wait_for_scene_sound_byte_fields\n        return wait_for_scene_sound_byte_fields(scene, entered)\n    raise SceneRefreshBoundary(target, entered, continuation)\nreturn _presentation_call_fields(BattlePresentationMemory(memory.state), frame, continuation, child)"}, 'read_object_action_mode_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _object_action_mode_slot_fields(memory, frame)\nreturn memory.sync_status(_first_word(frame, 'target_x', frame.roster.word(low16(frame.target_x))))"}, 'update_selected_object_action_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, primary_middle: bool=False', 'returns': 'FirstDeploymentFrame', 'flow': "from .business_scene import _scene_render_compare, _scene_render_asl_word\nmemory.frame(frame)\nif frame.auxiliary is None or frame.target_x is None:\n    raise SceneRefreshBoundary(265364, frame, None)\nif type(primary_middle) is not bool:\n    raise ValueError('actual primary-middle entry selector required')\nif not primary_middle:\n    frame = _scene_render_compare(memory, frame, frame.auxiliary.base, 4294935146, 32)\nsecondary = not primary_middle and frame.auxiliary.base >= 4294935146\nframe = first_replace(frame, scratch=memory.cursor_at(4294935146 if secondary else 4294934890))\nside = memory.state.read(4294934860, 2)\nframe = _scene_render_compare(memory, frame, side, 2 if secondary else 1, 16)\nif side != (2 if secondary else 1):\n    return frame\nkind = frame.auxiliary.word()\nframe = _first_word(frame, 'target_x', kind)\nframe = _first_word(frame, 'target_x', kind & 127)\ncategory = memory.state.read(4294934862, 2)\nframe = _scene_render_compare(memory, frame, low16(frame.target_x), category, 16)\nif low16(frame.target_x) != category:\n    return frame\nframe = _first_long(frame, 'target_x', 0)\nslot = memory.state.read(4294934864, 2)\nframe = _first_word(frame, 'target_x', slot)\nframe = _scene_render_asl_word(memory, frame, 'target_x', slot, 4)\nframe = first_replace(frame, roster=memory.cursor_at(u32(s16(low16(frame.target_x)))))\nframe = first_replace(frame, roster=memory.cursor_at(u32(frame.roster.base + frame.scratch.base)))\nframe = _scene_render_compare(memory, frame, frame.roster.base, frame.auxiliary.base, 32)\nif frame.roster.base != frame.auxiliary.base:\n    return frame\nresumed = memory.state.read(4294934866, 2)\nframe = _scene_refresh_flags(memory, frame, resumed, 2)\nif resumed:\n    selection = memory.state.read(4294934874, 2)\n    frame = _first_word(frame, 'target_x', selection)\n    table_base = 265550\nelse:\n    frame = _scene_refresh_emit(memory, frame, 4294934866, 2, 1)\n    horizontal = frame.auxiliary.word(0, 2)\n    frame = _scene_render_compare(memory, frame, horizontal, 512, 16)\n    if horizontal >= 512:\n        return _object_clear_word_fields(memory, frame, 4294934866)\n    frame = _scene_object_call_fields(memory, frame, 243490, 265460)\n    frame = _first_word(frame, 'target_x', low16(frame.target_x) & 3)\n    if low16(frame.target_x) != 0:\n        planned = _scene_object_plan_call_fields(memory, frame)\n        frame = planned.frame\n        if planned.discarded_continuation is not None:\n            return frame\n    frame = _scene_object_call_fields(memory, frame, 265512, 265474)\n    frame = _scene_refresh_emit(memory, frame, 4294934874, 2, low16(frame.target_x))\n    selection = low16(frame.target_x)\n    table_base = 265484\nframe = _scene_render_asl_word(memory, frame, 'target_x', selection, 2)\ntarget = u32(table_base + s16(u16(selection << 2)))\nfrom ..high_level_dynamic_flows.business_actions import dispatch_object_action_fields\nreturn dispatch_object_action_fields(memory, frame, target)"}})


# EARLY_OBJECTS_FULL_SOURCE_TWO_REAL_ROUTES121; complete FN/effective DECLARE, ordinary lowerers untouched.
DECLARATIONS.update({'initialize_scene_object_roster_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from .business_scene import _scene_render_compare, _scene_render_arithmetic, _scene_render_asl_word\nfrom ..high_level_main_flows.business_movement_support import _movement_multiply_word, _movement_divu_word\nmemory.frame(frame)\nif frame.stack_cursor is None:\n    raise SceneRefreshBoundary(268278, frame, None)\nframe = _first_word(frame, 'target_x', 255)\nframe = first_replace(frame, auxiliary=memory.cursor_at(4294934890))\ncounter = 255\nwhile True:\n    frame = _object_clear_word_fields(memory, frame, frame.auxiliary.base)\n    frame = first_replace(frame, auxiliary=frame.auxiliary.advance(2))\n    frame = _scene_refresh_decrement(frame, 'target_x', counter)\n    counter = u16(counter - 1)\n    if counter == 65535:\n        break\nmode = memory.state.read(4294934746, 1)\nframe = _scene_render_compare(memory, frame, mode, 1, 8)\nif mode == 1:\n    return _reset_object_action_controls_fields(memory, frame)\nmode = memory.state.read(4294934746, 1)\nframe = _scene_render_compare(memory, frame, mode, 2, 8)\nif mode == 2:\n    return _reset_object_action_controls_fields(memory, frame)\nreturn _initialize_scene_object_roster_tail_fields(memory, frame)"}, '_initialize_scene_object_roster_tail_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from .business_scene import _scene_render_compare, _scene_render_arithmetic, _scene_render_asl_word\nfrom ..high_level_main_flows.business_movement_support import _movement_multiply_word, _movement_divu_word\nmemory.frame(frame)\nif frame.stack_cursor is None:\n    raise SceneRefreshBoundary(268312, frame, None)\nfor address in (4294934760, 4294934772, 4294934774, 4294934776):\n    frame = _object_clear_word_fields(memory, frame, address)\ntotal = memory.state.read(4294934756, 2)\nframe = _scene_refresh_flags(memory, frame, total, 2)\nif total != 0:\n    frame = _scene_refresh_emit(memory, frame, 4294934760, 2, 1)\n    total = memory.state.read(4294934756, 2)\n    frame = _scene_render_compare(memory, frame, total, 100, 16)\n    if total >= 100:\n        total = memory.state.read(4294934756, 2)\n        frame = _scene_render_compare(memory, frame, total, 1500, 16)\n        if total < 1500:\n            frame = _object_count_draw_fields(memory, frame, 268364, 9, 1)\n        else:\n            total = memory.state.read(4294934756, 2)\n            frame = _scene_render_compare(memory, frame, total, 5000, 16)\n            if total < 5000:\n                frame = _object_count_draw_fields(memory, frame, 268396, 5, 5)\n            else:\n                frame = _scene_refresh_emit(memory, frame, 4294934760, 2, 15)\n                total = memory.state.read(4294934756, 2)\n                frame = _scene_render_compare(memory, frame, total, 10000, 16)\n                if total < 10000:\n                    frame = _object_count_draw_fields(memory, frame, 268434, 5, 10)\n    frame = _scene_object_call_fields(memory, frame, 259266, 268460)\n    for threshold, first_count, second_count in ((100, 0, 2), (200, 1, 3), (300, 3, 4), (400, 5, 5), (500, 6, 6), (600, 7, 7)):\n        frame = _first_long(frame, 'target_x', first_count)\n        frame = _first_long(frame, 'target_y', second_count)\n        quality = memory.state.read(4294934800, 2)\n        frame = _scene_render_compare(memory, frame, quality, threshold, 16)\n        if quality <= threshold:\n            break\n    else:\n        frame = _first_long(frame, 'target_x', 8)\n        frame = _first_long(frame, 'target_y', 8)\n    for address in (4294934772, 4294934774, 4294934776):\n        frame = _object_clear_word_fields(memory, frame, address)\n    frame = _first_word(frame, 'unit', memory.state.read(4294934760, 2))\n    frame = _scene_render_arithmetic(memory, frame, 'unit', low16(frame.unit), low16(frame.target_x), 16, True)\n    if low16(frame.unit) & 32768:\n        frame = _scene_refresh_emit(memory, frame, 4294934772, 2, memory.state.read(4294934760, 2))\n    else:\n        frame = _scene_refresh_emit(memory, frame, 4294934772, 2, low16(frame.target_x))\n        frame = _scene_refresh_emit(memory, frame, 4294934774, 2, low16(frame.unit))\n        frame = _scene_render_arithmetic(memory, frame, 'unit', low16(frame.unit), low16(frame.target_y), 16, True)\n        if not low16(frame.unit) & 32768:\n            frame = _scene_refresh_emit(memory, frame, 4294934774, 2, low16(frame.target_y))\n            frame = _scene_refresh_emit(memory, frame, 4294934776, 2, low16(frame.unit))\ninclude_override = total != 0\nwhile True:\n    if include_override:\n        mode = memory.state.read(4294934747, 1)\n        frame = _scene_render_compare(memory, frame, mode, 3, 8)\n        if mode == 3:\n            frame = _object_clear_word_fields(memory, frame, 4294934772)\n            frame = _scene_refresh_emit(memory, frame, 4294934774, 2, memory.state.read(4294934760, 2))\n            frame = _object_clear_word_fields(memory, frame, 4294934776)\n    frame = _scene_object_call_fields(memory, frame, 243490, 268622)\n    choice = low16(frame.target_x) & 7\n    frame = _first_word(frame, 'target_x', choice)\n    frame = _scene_render_compare(memory, frame, choice, 4, 16)\n    if choice <= 4:\n        break\n    include_override = True\nframe = _scene_refresh_emit(memory, frame, 4294934858, 2, choice)\nframe = _scene_render_asl_word(memory, frame, 'target_x', choice, 2)\nframe = first_replace(frame, roster=memory.cursor_at(268888))\npointer = frame.roster.long(s16(low16(frame.target_x)))\nframe = first_replace(frame, scratch=memory.cursor_at(pointer))\nframe = _first_word(frame, 'target_x', memory.state.read(4294934772, 2))\nframe = _first_word(frame, 'target_y', memory.state.read(4294934774, 2))\nframe = _first_word(frame, 'unit', memory.state.read(4294934776, 2))\nframe = _first_long(frame, 'count', 0)\nframe = first_replace(frame, auxiliary=memory.cursor_at(4294934890))\nwhile True:\n    frame = _scene_refresh_flags(memory, frame, low16(frame.count), 2)\n    if low16(frame.count) == 0:\n        kind, consume = (32771, None)\n    else:\n        frame = _scene_refresh_flags(memory, frame, low16(frame.target_x), 2)\n        if low16(frame.target_x) != 0:\n            kind, consume = (32770, 'target_x')\n        else:\n            frame = _scene_refresh_flags(memory, frame, low16(frame.target_y), 2)\n            if low16(frame.target_y) != 0:\n                kind, consume = (32769, 'target_y')\n            else:\n                frame = _scene_refresh_flags(memory, frame, low16(frame.unit), 2)\n                if low16(frame.unit) == 0:\n                    break\n                kind, consume = (32768, 'unit')\n    for displacement in (2, 4):\n        value = frame.scratch.word()\n        frame = first_replace(frame, scratch=frame.scratch.advance(2))\n        frame = _scene_refresh_emit(memory, frame, u32(frame.auxiliary.base + displacement), 2, value)\n    if consume == 'unit':\n        frame = _scene_render_arithmetic(memory, frame, consume, low16(frame.carrier(consume)), 1, 16, True)\n    frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, kind)\n    if consume is not None and consume != 'unit':\n        frame = _scene_render_arithmetic(memory, frame, consume, low16(frame.carrier(consume)), 1, 16, True)\n    frame = _scene_render_arithmetic(memory, frame, 'count', low16(frame.count), 1, 16)\n    frame = first_replace(frame, auxiliary=frame.auxiliary.advance(16))\nframe = _first_word(frame, 'target_x', memory.state.read(4294934788, 2))\nframe = _first_word(frame, 'target_y', memory.state.read(4294934784, 2))\nframe = _movement_multiply_word(memory.state, frame, 'target_y', low16(frame.target_x))\nframe = _movement_divu_word(memory.state, frame, 'target_y', 100, 268762)\nframe = _first_word(frame, 'target_x', 14)\nframe = _first_word(frame, 'unit', memory.state.read(4294934768, 2))\nframe = first_replace(frame, auxiliary=memory.cursor_at(4294934906))\ncounter = 14\nwhile True:\n    frame = _scene_refresh_emit(memory, frame, u32(frame.auxiliary.base + 12), 2, low16(frame.target_y))\n    frame = _scene_refresh_emit(memory, frame, u32(frame.auxiliary.base + 14), 2, memory.state.read(4294934764, 2))\n    frame = _scene_refresh_flags(memory, frame, low16(frame.unit), 2)\n    if low16(frame.unit) != 0:\n        frame = _scene_render_arithmetic(memory, frame, 'unit', low16(frame.unit), 1, 16, True)\n        frame = _object_adjust_word_fields(memory, frame, u32(frame.auxiliary.base + 14), 1)\n    frame = first_replace(frame, auxiliary=frame.auxiliary.advance(16))\n    frame = _scene_refresh_decrement(frame, 'target_x', counter)\n    counter = u16(counter - 1)\n    if counter == 65535:\n        break\nframe = _first_word(frame, 'target_x', memory.state.read(4294934788, 2))\nframe = _scene_render_arithmetic(memory, frame, 'target_x', low16(frame.target_x), memory.state.read(4294934792, 2), 16)\nframe = _scene_refresh_emit(memory, frame, 4294934902, 2, low16(frame.target_x))\nframe = _scene_refresh_emit(memory, frame, 4294934904, 2, memory.state.read(4294934796, 2))\nreturn _reset_object_action_controls_fields(memory, frame)"}, 'initialize_scene_object_roster_after_mode_check_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _initialize_scene_object_roster_tail_fields(memory, frame)'}})

# ROSTER_SOLE_TAIL_NORMAL_POLICY_EFFECTS123; both complete normally admitted helper effects accompany the whole root.


# Source145: actual phase BRA cells and live name CALL; original owners/lowerers unchanged.
DECLARATIONS.update({'dispatch_scene_object_phase_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "from .business_scene import _scene_render_asl_word\nmemory.frame(frame)\nmemory.sync_status(frame)\nphase = memory.state.read(4294934842, 2)\nframe = _first_word(frame, 'target_x', phase)\nframe = _scene_render_asl_word(memory, frame, 'target_x', phase, 2)\ntarget = u32(253122 + s16(u16(phase << 2)))\nif target == 253122:\n    from ..high_level_dynamic_flows.business_early_phase import step_main_scene_phase_fields\n    return step_main_scene_phase_fields(memory, frame)\nif target in (253126, 253130, 253134, 253138, 253142, 253146, 253150, 253154, 253158):\n    from ..high_level_dynamic_flows.business_early_phase import _allocation_known_fields\n    return _allocation_known_fields(memory, frame, target)\nraise SceneRefreshBoundary(target, frame, None)"}})
