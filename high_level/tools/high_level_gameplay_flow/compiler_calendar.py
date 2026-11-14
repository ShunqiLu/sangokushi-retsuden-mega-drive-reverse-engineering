"""Restricted calendar structural source admission and ordinary mnemonic lowering.

Explicit semantic input only; no original ROM/ASM/IR/object input or opaque
opcode payload. Fixed original layout; unsupported source changes are rejected.
Actual service/IRQ and CPU behavior are not supplied by this finite compiler.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import CALENDAR_BINDINGS

APPROVED = {'business_reuse': {'choose_city_head',
                    'credit_primary',
                    'credit_secondary',
                    'debit_primary',
                    'debit_secondary',
                    'grow_original_long_field',
                    'replenish_b200_troops',
                    'reset_queue',
                    'step_random',
                    'submit_classified_fields',
                    'submit_four_fields',
                    'submit_three_fields'},
 'business_services': {'refresh_gameplay_scene', 'present_gameplay_message', 'load_gameplay_scene'},
 'contexts_calendar': {'CalendarContext', 'MortalityContext', 'EventContext'},
 'domain': {'GameplayState',
            'Table',
            'Word',
            'checked_state',
            'descending_inclusive',
            'low16',
            'low8',
            'negative_byte',
            'replace_byte',
            'u16',
            'u8',
            'uint'}}

DECLARATIONS = {'process_calendar_city_cycle': {'signature': 'state: GameplayState, retained: '
                                              'CalendarContext=CalendarContext()',
                                 'returns': 'CalendarContext',
                                 'flow': 'from .business_reuse import grow_original_long_field, '
                                         'credit_primary, credit_secondary, debit_primary, '
                                         'debit_secondary, replenish_b200_troops\n'
                                         'from .business_services import refresh_gameplay_scene\n'
                                         'checked_state(state)\n'
                                         'if type(retained) is not CalendarContext:\n'
                                         "    raise ValueError('typed calendar entry condition "
                                         "required')\n"
                                         'state.set_status_word(9984)\n'
                                         "saved_selection = state.scalar('ram_f376_word')\n"
                                         "month = state.scalar('metadata_f375')\n"
                                         'owners = state.ram_f450.cursor()\n'
                                         'if month == 0:\n'
                                         '    field = state.ram_e1dc\n'
                                         '    for city in descending_inclusive(39):\n'
                                         '        if not negative_byte(owners.previous_byte()):\n'
                                         '            grow_original_long_field(state, field)\n'
                                         '        field = field.advance(-4)\n'
                                         'elif month == 3:\n'
                                         '    for city in descending_inclusive(39):\n'
                                         '        if not negative_byte(owners.previous_byte()):\n'
                                         '            credit_primary(state, city)\n'
                                         '            debit_primary(state, city)\n'
                                         'elif month == 9:\n'
                                         '    for city in descending_inclusive(39):\n'
                                         '        if not negative_byte(owners.previous_byte()):\n'
                                         '            credit_secondary(state, city)\n'
                                         '            debit_secondary(state, city)\n'
                                         'replenishment = 65535 if month == 0 or month == 3 or '
                                         'month == 9 else 39\n'
                                         "if state.scalar('metadata_f375') & 1 == 0:\n"
                                         '    replenishment = replenish_b200_troops(state, '
                                         'replenishment)\n'
                                         'mortality = scan_calendar_officer_mortality(state, '
                                         'retained.mortality)\n'
                                         'events = process_calendar_event_schedulers(state, '
                                         'retained.events)\n'
                                         "state.set_scalar('ram_f376_word', saved_selection)\n"
                                         'refresh_gameplay_scene(state)\n'
                                         'return CalendarContext(mortality, events, '
                                         'replenishment)'},
 'scan_calendar_officer_mortality': {'signature': 'state: GameplayState, retained: '
                                                  'MortalityContext=MortalityContext()',
                                     'returns': 'MortalityContext',
                                     'flow': 'from .business_reuse import step_random\n'
                                             'checked_state(state)\n'
                                             'if type(retained) is not MortalityContext:\n'
                                             "    raise ValueError('typed mortality entry "
                                             "condition required')\n"
                                             'birthdays = state.ram_f100.cursor()\n'
                                             'assignments = state.ram_cc00\n'
                                             'processed = state.ram_ea37\n'
                                             'assignment_word = retained.assignment_word\n'
                                             'owner_lookup_word = retained.owner_lookup_word\n'
                                             'for officer in descending_inclusive(255):\n'
                                             '    birth_year = birthdays.previous_byte()\n'
                                             '    if birth_year == 255:\n'
                                             '        continue\n'
                                             '    assignment_word = '
                                             'u16(replace_byte(assignment_word, '
                                             'assignments.byte(officer)))\n'
                                             '    if not negative_byte(low8(assignment_word)):\n'
                                             '        if assignment_word & 64:\n'
                                             '            continue\n'
                                             '        if processed.byte(assignment_word) != 0:\n'
                                             '            continue\n'
                                             '    if low8(assignment_word) == 255:\n'
                                             '        continue\n'
                                             "    current_year = state.scalar('metadata_f374')\n"
                                             '    if current_year < birth_year:\n'
                                             '        continue\n'
                                             '    age = u8(current_year - birth_year)\n'
                                             '    threshold = u16(1 << (age & 4))\n'
                                             '    owner_lookup_word = '
                                             'u16(low16(step_random(state)) & 15)\n'
                                             '    if owner_lookup_word > threshold:\n'
                                             '        continue\n'
                                             '    owner_lookup_word = '
                                             'remove_mortal_officer_with_message(state, officer, '
                                             'assignments, owner_lookup_word)\n'
                                             'return MortalityContext(assignment_word, '
                                             'owner_lookup_word)'},
 'remove_mortal_officer_with_message': {'signature': 'state: GameplayState, officer: Word, '
                                                     'assignments: Table, retained_owner_lookup: '
                                                     'Word=0',
                                        'returns': 'Word',
                                        'flow': 'from .business_services import '
                                                'present_gameplay_message\n'
                                                'checked_state(state)\n'
                                                'uint(officer, 16)\n'
                                                'uint(retained_owner_lookup, 16)\n'
                                                'assignments = state.checked_table(assignments)\n'
                                                'city = u16(replace_byte(retained_owner_lookup, '
                                                'assignments.byte(officer)))\n'
                                                'owner = state.ram_f427.byte(city)\n'
                                                'player_owned = owner == '
                                                "state.scalar('metadata_f67b')\n"
                                                'if not player_owned:\n'
                                                '    player_owned = owner == '
                                                "state.scalar('metadata_f67d')\n"
                                                'if not player_owned:\n'
                                                '    player_owned = owner == '
                                                "state.scalar('metadata_f67f')\n"
                                                'if player_owned:\n'
                                                '    owner_offset = u16(owner << 1)\n'
                                                '    if state.ram_e640.word(owner_offset) != '
                                                'officer:\n'
                                                '        saved_selection = '
                                                "state.scalar('ram_f376_word')\n"
                                                '        saved_display = '
                                                "state.scalar('ram_f362_word')\n"
                                                "        state.set_scalar('ram_f376_word', 0)\n"
                                                "        state.set_scalar('ram_f377_byte', "
                                                'low8(owner_offset >> 1))\n'
                                                "        state.set_scalar('ram_f3d0_word', "
                                                'officer)\n'
                                                "        state.set_scalar('ram_f740_word', 205)\n"
                                                "        state.set_scalar('ram_f362_word', 0)\n"
                                                '        present_gameplay_message(state)\n'
                                                "        state.set_scalar('ram_f362_word', "
                                                'saved_display)\n'
                                                "        state.set_scalar('ram_f376_word', "
                                                'saved_selection)\n'
                                                'assignments.set_byte(officer, 255)\n'
                                                'heads = state.ram_f460.cursor()\n'
                                                'for remaining in descending_inclusive(39):\n'
                                                '    if heads.next_word() == officer:\n'
                                                '        city = u16(city & 255)\n'
                                                '        choose_city_head_after_mortality(state, '
                                                'city, assignments)\n'
                                                '        break\n'
                                                'return city'},
 'choose_city_head_after_mortality': {'signature': 'state: GameplayState, city: Word, assignments: '
                                                   'Table',
                                      'returns': 'Word',
                                      'flow': 'from .business_reuse import choose_city_head\n'
                                              'checked_state(state)\n'
                                              'uint(city, 16)\n'
                                              'assignments = state.checked_table(assignments)\n'
                                              'candidates = state.ram_f500.cursor()\n'
                                              'for officer in descending_inclusive(255):\n'
                                              '    if assignments.byte(officer) == low8(city):\n'
                                              '        candidates.append_word(officer)\n'
                                              'candidates.put_word(65535)\n'
                                              'return choose_city_head(state, city)'},
 'process_calendar_event_schedulers': {'signature': 'state: GameplayState, retained: '
                                                    'EventContext=EventContext()',
                                       'returns': 'EventContext',
                                       'flow': 'from .business_reuse import reset_queue\n'
                                               'checked_state(state)\n'
                                               'if type(retained) is not EventContext:\n'
                                               "    raise ValueError('typed event entry condition "
                                               "required')\n"
                                               'reset_queue(state)\n'
                                               'retained = process_first_calendar_event(state, '
                                               'retained)\n'
                                               'reset_queue(state)\n'
                                               'retained = process_second_calendar_event(state, '
                                               'retained)\n'
                                               'reset_queue(state)\n'
                                               'return process_third_calendar_event(state, '
                                               'retained)'},
 'show_calendar_event_message': {'signature': 'state: GameplayState, message: Word',
                                 'returns': 'None',
                                 'flow': 'from .business_services import present_gameplay_message\n'
                                         'checked_state(state)\n'
                                         'uint(message, 16)\n'
                                         "state.set_scalar('ram_f740_word', message)\n"
                                         "state.set_scalar('ram_f608_word', 128)\n"
                                         "state.set_scalar('ram_f362_word', 0)\n"
                                         "saved_parameter = state.scalar('ram_f612_word')\n"
                                         'present_gameplay_message(state)\n'
                                         "state.set_scalar('ram_f612_word', saved_parameter)",
                                 'slots': {128: ('message_parameter', 0, 65535)}},
 'process_first_calendar_event': {'signature': 'state: GameplayState, retained: '
                                               'EventContext=EventContext()',
                                  'returns': 'EventContext',
                                  'flow': 'from .business_reuse import submit_three_fields\n'
                                          'from .business_services import load_gameplay_scene\n'
                                          'checked_state(state)\n'
                                          'if type(retained) is not EventContext:\n'
                                          "    raise ValueError('typed event entry condition "
                                          "required')\n"
                                          'owner_word = retained.owner_word\n'
                                          'for city in range(39):\n'
                                          "    if state.scalar('metadata_f375') == 5:\n"
                                          '        if city == 5 or city == 8 or city == 14:\n'
                                          '            submitted = submit_three_fields(state, '
                                          'city, owner_word)\n'
                                          '            owner_word = submitted.owner_word\n'
                                          "    if state.scalar('metadata_f375') == 6:\n"
                                          '        if city == 5 or city == 8 or city == 14:\n'
                                          '            submitted = submit_three_fields(state, '
                                          'city, owner_word)\n'
                                          '            owner_word = submitted.owner_word\n'
                                          "    if state.scalar('metadata_f375') == 6:\n"
                                          '        if city == 5 or city == 8 or city == 14:\n'
                                          '            submitted = submit_three_fields(state, '
                                          'city, owner_word)\n'
                                          '            owner_word = submitted.owner_word\n'
                                          'if state.ram_d420.byte() == 255:\n'
                                          '    return EventContext(owner_word)\n'
                                          "state.set_scalar('ram_7026_word', 35)\n"
                                          'load_gameplay_scene(state)\n'
                                          'show_calendar_event_message(state, 176)\n'
                                          "if state.scalar('ram_d448_word') == 0:\n"
                                          '    show_first_calendar_event_values(state, '
                                          "state.scalar('ram_f67a_word'))\n"
                                          '    show_first_calendar_event_values(state, '
                                          "state.scalar('ram_f67c_word'))\n"
                                          '    show_first_calendar_event_values(state, '
                                          "state.scalar('ram_f67e_word'))\n"
                                          '_clear_calendar_message_plane(state)\n'
                                          'return EventContext(65535)'},
 'show_first_calendar_event_values': {'signature': 'state: GameplayState, owner: Word',
                                      'returns': 'None',
                                      'flow': 'checked_state(state)\n'
                                              'uint(owner, 16)\n'
                                              '_show_event_values(state, owner, 174)'},
 'process_second_calendar_event': {'signature': 'state: GameplayState, retained: '
                                                'EventContext=EventContext()',
                                   'returns': 'EventContext',
                                   'flow': 'from .business_reuse import submit_four_fields\n'
                                           'from .business_services import load_gameplay_scene\n'
                                           'checked_state(state)\n'
                                           'if type(retained) is not EventContext:\n'
                                           "    raise ValueError('typed event entry condition "
                                           "required')\n"
                                           'owner_word = retained.owner_word\n'
                                           'for city in range(39):\n'
                                           "    if state.scalar('metadata_f375') == 9:\n"
                                           '        if city == 4 or city == 6 or city == 7:\n'
                                           '            submitted = submit_four_fields(state, '
                                           'city, owner_word)\n'
                                           '            owner_word = submitted.owner_word\n'
                                           "    if state.scalar('metadata_f375') == 8:\n"
                                           '        if city == 13 or city == 16 or city == 17:\n'
                                           '            submitted = submit_four_fields(state, '
                                           'city, owner_word)\n'
                                           '            owner_word = submitted.owner_word\n'
                                           "    if state.scalar('metadata_f375') == 4:\n"
                                           '        if city == 18 or city == 21 or city == 22:\n'
                                           '            submitted = submit_four_fields(state, '
                                           'city, owner_word)\n'
                                           '            owner_word = submitted.owner_word\n'
                                           "    if state.scalar('metadata_f375') == 3:\n"
                                           '        if city == 26 or city == 31:\n'
                                           '            submitted = submit_four_fields(state, '
                                           'city, owner_word)\n'
                                           '            owner_word = submitted.owner_word\n'
                                           'if state.ram_d420.byte() == 255:\n'
                                           '    return EventContext(owner_word)\n'
                                           "state.set_scalar('ram_7026_word', 37)\n"
                                           'load_gameplay_scene(state)\n'
                                           'show_calendar_event_message(state, 177)\n'
                                           "if state.scalar('ram_d448_word') == 0:\n"
                                           '    show_second_calendar_event_values(state, '
                                           "state.scalar('ram_f67a_word'))\n"
                                           '    show_second_calendar_event_values(state, '
                                           "state.scalar('ram_f67c_word'))\n"
                                           '    show_second_calendar_event_values(state, '
                                           "state.scalar('ram_f67e_word'))\n"
                                           '_clear_calendar_message_plane(state)\n'
                                           'return EventContext(65535)'},
 'show_second_calendar_event_values': {'signature': 'state: GameplayState, owner: Word',
                                       'returns': 'None',
                                       'flow': 'checked_state(state)\n'
                                               'uint(owner, 16)\n'
                                               '_show_event_values(state, owner, 175)'},
 'process_third_calendar_event': {'signature': 'state: GameplayState, retained: '
                                               'EventContext=EventContext()',
                                  'returns': 'EventContext',
                                  'flow': 'from .business_reuse import submit_classified_fields\n'
                                          'from .business_services import load_gameplay_scene\n'
                                          'checked_state(state)\n'
                                          'if type(retained) is not EventContext:\n'
                                          "    raise ValueError('typed event entry condition "
                                          "required')\n"
                                          'owner_word = retained.owner_word\n'
                                          'for city in range(39):\n'
                                          "    if state.scalar('metadata_f375') & 1 == 0:\n"
                                          '        owner_word = u16(replace_byte(owner_word, '
                                          'state.ram_f428.byte(city)))\n'
                                          '        if not negative_byte(low8(owner_word)):\n'
                                          '            selected = owner_word == '
                                          "state.scalar('ram_f67a_word')\n"
                                          '            if not selected:\n'
                                          '                selected = owner_word == '
                                          "state.scalar('ram_f67c_word')\n"
                                          '            if not selected:\n'
                                          '                selected = owner_word == '
                                          "state.scalar('ram_f67e_word')\n"
                                          '            if selected:\n'
                                          '                submit_classified_fields(state, city)\n'
                                          '                owner_word = city\n'
                                          "if state.scalar('ram_d448_word') != 0:\n"
                                          '    return EventContext(owner_word)\n'
                                          "state.set_scalar('ram_7026_word', 39)\n"
                                          'load_gameplay_scene(state)\n'
                                          'show_third_calendar_event_values(state, '
                                          "state.scalar('ram_f67a_word'))\n"
                                          'show_third_calendar_event_values(state, '
                                          "state.scalar('ram_f67c_word'))\n"
                                          'show_third_calendar_event_values(state, '
                                          "state.scalar('ram_f67e_word'))\n"
                                          '_clear_calendar_message_plane(state)\n'
                                          'return EventContext(65535)'},
 'show_third_calendar_event_values': {'signature': 'state: GameplayState, owner: Word',
                                      'returns': 'None',
                                      'flow': 'checked_state(state)\n'
                                              'uint(owner, 16)\n'
                                              '_show_event_values(state, owner, 179)'},
 '_show_event_values': {'signature': 'state: GameplayState, owner: Word, message: Word',
                        'returns': 'None',
                        'flow': 'queue = state.ram_d420\n'
                                'owners = state.ram_f428\n'
                                'index = u16(0)\n'
                                'has_heading = False\n'
                                'while True:\n'
                                '    city = queue.byte(index)\n'
                                '    if city == 255:\n'
                                '        return None\n'
                                '    selected_owner = owners.byte(city)\n'
                                '    if selected_owner == owner:\n'
                                "        state.set_scalar('ram_f646_word', city)\n"
                                "        state.set_scalar('ram_f646_word', "
                                "u16(state.scalar('ram_f646_word') + 1))\n"
                                "        state.set_scalar('ram_f376_word', selected_owner)\n"
                                '        if not has_heading:\n'
                                '            show_calendar_event_message(state, 178)\n'
                                '            has_heading = True\n'
                                '        show_calendar_event_message(state, message)\n'
                                '    index = u16(index + 1)'},
 '_clear_calendar_message_plane': {'signature': 'state: GameplayState',
                                   'returns': 'None',
                                   'flow': 'state.mmio_write(12582916, 4, 1241513987)\n'
                                           'for remaining in descending_inclusive(511):\n'
                                           '    state.mmio_write(12582912, 2, 0)'}}

def _lower_process_calendar_city_cycle(e,rules):
    e.label('gameplay_pc_016b3a')
    e.ins('move.w','#0x2700,%sr',4)
    e.label('gameplay_pc_016b3e')
    e.ins('move.w','0xf376:w,-(%a7)',4)
    e.label('gameplay_pc_016b42')
    e.ins('move.w','#0x27,%d0',4)
    e.label('gameplay_pc_016b46')
    e.ins('move.b','0xf375:w,%d1',4)
    e.label('gameplay_pc_016b4a')
    e.ins('lea.l','0xf450:w,%a6',4)
    e.label('gameplay_pc_016b4e')
    e.ins('tst.b','%d1',2)
    e.label('gameplay_pc_016b50')
    e.ins('bne.b','gameplay_pc_016b68',2)
    e.label('gameplay_pc_016b52')
    e.ins('lea.l','0xe1dc:w,%a0',4)
    e.label('gameplay_pc_016b56')
    e.ins('tst.b','-(%a6)',2)
    e.label('gameplay_pc_016b58')
    e.ins('bmi.b','gameplay_pc_016b5e',2)
    e.label('gameplay_pc_016b5a')
    e.ins('bsr.w','gameplay_pc_016c0a',4)
    e.label('gameplay_pc_016b5e')
    e.ins('subq.w','#0x4,%a0',2)
    e.label('gameplay_pc_016b60')
    e.ins('dbra','%d0,gameplay_pc_016b56',4)
    e.label('gameplay_pc_016b64')
    e.ins('bra.w','gameplay_pc_016b96',4)
    e.label('gameplay_pc_016b68')
    e.ins('cmpi.b','#0x3,%d1',4)
    e.label('gameplay_pc_016b6c')
    e.ins('bne.b','gameplay_pc_016b80',2)
    e.label('gameplay_pc_016b6e')
    e.ins('tst.b','-(%a6)',2)
    e.label('gameplay_pc_016b70')
    e.ins('bmi.b','gameplay_pc_016b7a',2)
    e.label('gameplay_pc_016b72')
    e.ins('bsr.w','gameplay_pc_016c2c',4)
    e.label('gameplay_pc_016b76')
    e.ins('bsr.w','gameplay_pc_016d10',4)
    e.label('gameplay_pc_016b7a')
    e.ins('dbra','%d0,gameplay_pc_016b6e',4)
    e.label('gameplay_pc_016b7e')
    e.ins('bra.b','gameplay_pc_016b96',2)
    e.label('gameplay_pc_016b80')
    e.ins('cmpi.b','#0x9,%d1',4)
    e.label('gameplay_pc_016b84')
    e.ins('bne.b','gameplay_pc_016b96',2)
    e.label('gameplay_pc_016b86')
    e.ins('tst.b','-(%a6)',2)
    e.label('gameplay_pc_016b88')
    e.ins('bmi.b','gameplay_pc_016b92',2)
    e.label('gameplay_pc_016b8a')
    e.ins('bsr.w','gameplay_pc_016c46',4)
    e.label('gameplay_pc_016b8e')
    e.ins('bsr.w','gameplay_pc_016d2a',4)
    e.label('gameplay_pc_016b92')
    e.ins('dbra','%d0,gameplay_pc_016b86',4)
    e.label('gameplay_pc_016b96')
    e.ins('btst.b','#0x0,0xf375:w',6)
    e.label('gameplay_pc_016b9c')
    e.ins('bne.w','gameplay_pc_016ba4',4)
    e.label('gameplay_pc_016ba0')
    e.ins('bsr.w','gameplay_pc_016bb8',4)
    e.label('gameplay_pc_016ba4')
    e.ins('bsr.w','gameplay_pc_016eda',4)
    e.label('gameplay_pc_016ba8')
    e.ins('bsr.w','gameplay_pc_016ffc',4)
    e.label('gameplay_pc_016bac')
    e.ins('move.w','(%a7)+,0xf376:w',4)
    e.label('gameplay_pc_016bb0')
    e.ins('jsr','gameplay_pc_00af48:l',6)
    e.label('gameplay_pc_016bb6')
    e.ins('rts','',2)

def _lower_scan_calendar_officer_mortality(e,rules):
    e.label('gameplay_pc_016eda')
    e.ins('lea.l','0xf100:w,%a0',4)
    e.label('gameplay_pc_016ede')
    e.ins('lea.l','0xcc00:w,%a1',4)
    e.label('gameplay_pc_016ee2')
    e.ins('lea.l','0xea37:w,%a2',4)
    e.label('gameplay_pc_016ee6')
    e.ins('move.w','#0xff,%d6',4)
    e.label('gameplay_pc_016eea')
    e.ins('move.b','-(%a0),%d5',2)
    e.label('gameplay_pc_016eec')
    e.ins('cmpi.b','#0xff,%d5',4)
    e.label('gameplay_pc_016ef0')
    e.ins('beq.w','gameplay_pc_016f3c',4)
    e.label('gameplay_pc_016ef4')
    e.ins('move.b','(%a1, %d6.w),%d4',4)
    e.label('gameplay_pc_016ef8')
    e.ins('bmi.w','gameplay_pc_016f0c',4)
    e.label('gameplay_pc_016efc')
    e.ins('btst.l','#0x6,%d4',4)
    e.label('gameplay_pc_016f00')
    e.ins('bne.w','gameplay_pc_016f3c',4)
    e.label('gameplay_pc_016f04')
    e.ins('tst.b','(%a2, %d4.w)',4)
    e.label('gameplay_pc_016f08')
    e.ins('bne.w','gameplay_pc_016f3c',4)
    e.label('gameplay_pc_016f0c')
    e.ins('cmpi.b','#0xff,%d4',4)
    e.label('gameplay_pc_016f10')
    e.ins('beq.w','gameplay_pc_016f3c',4)
    e.label('gameplay_pc_016f14')
    e.ins('move.b','0xf374:w,%d7',4)
    e.label('gameplay_pc_016f18')
    e.ins('sub.b','%d5,%d7',2)
    e.label('gameplay_pc_016f1a')
    e.ins('bcs.w','gameplay_pc_016f3c',4)
    e.label('gameplay_pc_016f1e')
    e.ins('move.w','#0x1,%d5',4)
    e.label('gameplay_pc_016f22')
    e.ins('andi.w','#0x4,%d7',4)
    e.label('gameplay_pc_016f26')
    e.ins('lsl.w','%d7,%d5',2)
    e.label('gameplay_pc_016f28')
    e.ins('jsr','gameplay_pc_0083d4:l',6)
    e.label('gameplay_pc_016f2e')
    e.ins('andi.w','#0xf,%d0',4)
    e.label('gameplay_pc_016f32')
    e.ins('cmp.w','%d5,%d0',2)
    e.label('gameplay_pc_016f34')
    e.ins('bhi.w','gameplay_pc_016f3c',4)
    e.label('gameplay_pc_016f38')
    e.ins('bsr.w','gameplay_pc_016f42',4)
    e.label('gameplay_pc_016f3c')
    e.ins('dbra','%d6,gameplay_pc_016eea',4)
    e.label('gameplay_pc_016f40')
    e.ins('rts','',2)

def _lower_remove_mortal_officer_with_message(e,rules):
    e.label('gameplay_pc_016f42')
    e.ins('movem.l','%a3-%a4,-(%a7)',4)
    e.label('gameplay_pc_016f46')
    e.ins('move.b','(%a1, %d6.w),%d0',4)
    e.label('gameplay_pc_016f4a')
    e.ins('lea.l','0xf427:w,%a4',4)
    e.label('gameplay_pc_016f4e')
    e.ins('clr.w','%d1',2)
    e.label('gameplay_pc_016f50')
    e.ins('move.b','(%a4, %d0.w),%d1',4)
    e.label('gameplay_pc_016f54')
    e.ins('cmp.b','0xf67b:w,%d1',4)
    e.label('gameplay_pc_016f58')
    e.ins('beq.w','gameplay_pc_016f6c',4)
    e.label('gameplay_pc_016f5c')
    e.ins('cmp.b','0xf67d:w,%d1',4)
    e.label('gameplay_pc_016f60')
    e.ins('beq.w','gameplay_pc_016f6c',4)
    e.label('gameplay_pc_016f64')
    e.ins('cmp.b','0xf67f:w,%d1',4)
    e.label('gameplay_pc_016f68')
    e.ins('bne.w','gameplay_pc_016fb0',4)
    e.label('gameplay_pc_016f6c')
    e.ins('lea.l','0xe640:w,%a4',4)
    e.label('gameplay_pc_016f70')
    e.ins('lsl.w','#0x1,%d1',2)
    e.label('gameplay_pc_016f72')
    e.ins('cmp.w','(%a4, %d1.w),%d6',4)
    e.label('gameplay_pc_016f76')
    e.ins('beq.w','gameplay_pc_016fb0',4)
    e.label('gameplay_pc_016f7a')
    e.ins('movem.l','%d0-%d7/%a0-%a6,-(%a7)',4)
    e.label('gameplay_pc_016f7e')
    e.ins('move.w','0xf376:w,-(%a7)',4)
    e.label('gameplay_pc_016f82')
    e.ins('move.w','0xf362:w,-(%a7)',4)
    e.label('gameplay_pc_016f86')
    e.ins('clr.w','0xf376:w',4)
    e.label('gameplay_pc_016f8a')
    e.ins('lsr.w','#0x1,%d1',2)
    e.label('gameplay_pc_016f8c')
    e.ins('move.b','%d1,0xf377:w',4)
    e.label('gameplay_pc_016f90')
    e.ins('move.w','%d6,0xf3d0:w',4)
    e.label('gameplay_pc_016f94')
    e.ins('move.w','#0xcd,0xf740:w',6)
    e.label('gameplay_pc_016f9a')
    e.ins('clr.w','0xf362:w',4)
    e.label('gameplay_pc_016f9e')
    e.ins('jsr','gameplay_pc_030a74:l',6)
    e.label('gameplay_pc_016fa4')
    e.ins('move.w','(%a7)+,0xf362:w',4)
    e.label('gameplay_pc_016fa8')
    e.ins('move.w','(%a7)+,0xf376:w',4)
    e.label('gameplay_pc_016fac')
    e.ins('movem.l','(%a7)+,%d0-%d7/%a0-%a6',4)
    e.label('gameplay_pc_016fb0')
    e.ins('move.b','#0xff,(%a1, %d6.w)',6)
    e.label('gameplay_pc_016fb6')
    e.ins('lea.l','0xf460:w,%a3',4)
    e.label('gameplay_pc_016fba')
    e.ins('move.w','#0x27,%d1',4)
    e.label('gameplay_pc_016fbe')
    e.ins('cmp.w','(%a3)+,%d6',2)
    e.label('gameplay_pc_016fc0')
    e.ins('beq.w','gameplay_pc_016fcc',4)
    e.label('gameplay_pc_016fc4')
    e.ins('dbra','%d1,gameplay_pc_016fbe',4)
    e.label('gameplay_pc_016fc8')
    e.ins('bra.w','gameplay_pc_016fd4',4)
    e.label('gameplay_pc_016fcc')
    e.ins('andi.w','#0xff,%d0',4)
    e.label('gameplay_pc_016fd0')
    e.ins('bsr.w','gameplay_pc_016fda',4)
    e.label('gameplay_pc_016fd4')
    e.ins('movem.l','(%a7)+,%a3-%a4',4)
    e.label('gameplay_pc_016fd8')
    e.ins('rts','',2)

def _lower_choose_city_head_after_mortality(e,rules):
    e.label('gameplay_pc_016fda')
    e.ins('lea.l','0xf500:w,%a3',4)
    e.label('gameplay_pc_016fde')
    e.ins('move.w','#0xff,%d1',4)
    e.label('gameplay_pc_016fe2')
    e.ins('cmp.b','(%a1, %d1.w),%d0',4)
    e.label('gameplay_pc_016fe6')
    e.ins('bne.w','gameplay_pc_016fec',4)
    e.label('gameplay_pc_016fea')
    e.ins('move.w','%d1,(%a3)+',2)
    e.label('gameplay_pc_016fec')
    e.ins('dbra','%d1,gameplay_pc_016fe2',4)
    e.label('gameplay_pc_016ff0')
    e.ins('move.w','#0xffff,(%a3)',4)
    e.label('gameplay_pc_016ff4')
    e.ins('jsr','gameplay_pc_00e1f6:l',6)
    e.label('gameplay_pc_016ffa')
    e.ins('rts','',2)

def _lower_process_calendar_event_schedulers(e,rules):
    e.label('gameplay_pc_016ffc')
    e.ins('bsr.w','gameplay_pc_017016',4)
    e.label('gameplay_pc_017000')
    e.ins('bsr.w','gameplay_pc_01707e',4)
    e.label('gameplay_pc_017004')
    e.ins('bsr.w','gameplay_pc_017016',4)
    e.label('gameplay_pc_017008')
    e.ins('bsr.w','gameplay_pc_0171fc',4)
    e.label('gameplay_pc_01700c')
    e.ins('bsr.w','gameplay_pc_017016',4)
    e.label('gameplay_pc_017010')
    e.ins('bsr.w','gameplay_pc_0173a6',4)
    e.label('gameplay_pc_017014')
    e.ins('rts','',2)

def _lower_show_calendar_event_message(e,rules):
    e.label('gameplay_pc_017058')
    e.ins('movem.l','%d0-%d7,-(%a7)',4)
    e.label('gameplay_pc_01705c')
    e.ins('move.w','%d2,0xf740:w',4)
    e.label('gameplay_pc_017060')
    e.ins('move.w','#'+hex(rules['message_parameter'])+',0xf608:w',6)
    e.label('gameplay_pc_017066')
    e.ins('clr.w','0xf362:w',4)
    e.label('gameplay_pc_01706a')
    e.ins('move.w','0xf612:w,-(%a7)',4)
    e.label('gameplay_pc_01706e')
    e.ins('jsr','gameplay_pc_030a74:l',6)
    e.label('gameplay_pc_017074')
    e.ins('move.w','(%a7)+,0xf612:w',4)
    e.label('gameplay_pc_017078')
    e.ins('movem.l','(%a7)+,%d0-%d7',4)
    e.label('gameplay_pc_01707c')
    e.ins('rts','',2)

def _lower_process_first_calendar_event(e,rules):
    e.label('gameplay_pc_01707e')
    e.ins('moveq','#0,%d0',2)
    e.label('gameplay_pc_017080')
    e.ins('moveq','#0,%d1',2)
    e.label('gameplay_pc_017082')
    e.ins('cmpi.b','#0x5,0xf375:w',6)
    e.label('gameplay_pc_017088')
    e.ins('bne.b','gameplay_pc_0170a8',2)
    e.label('gameplay_pc_01708a')
    e.ins('cmpi.w','#0x5,%d0',4)
    e.label('gameplay_pc_01708e')
    e.ins('bne.b','gameplay_pc_017094',2)
    e.label('gameplay_pc_017090')
    e.ins('bsr.w','gameplay_pc_0171a6',4)
    e.label('gameplay_pc_017094')
    e.ins('cmpi.w','#0x8,%d0',4)
    e.label('gameplay_pc_017098')
    e.ins('bne.b','gameplay_pc_01709e',2)
    e.label('gameplay_pc_01709a')
    e.ins('bsr.w','gameplay_pc_0171a6',4)
    e.label('gameplay_pc_01709e')
    e.ins('cmpi.w','#0xe,%d0',4)
    e.label('gameplay_pc_0170a2')
    e.ins('bne.b','gameplay_pc_0170a8',2)
    e.label('gameplay_pc_0170a4')
    e.ins('bsr.w','gameplay_pc_0171a6',4)
    e.label('gameplay_pc_0170a8')
    e.ins('cmpi.b','#0x6,0xf375:w',6)
    e.label('gameplay_pc_0170ae')
    e.ins('bne.b','gameplay_pc_0170ce',2)
    e.label('gameplay_pc_0170b0')
    e.ins('cmpi.w','#0x5,%d0',4)
    e.label('gameplay_pc_0170b4')
    e.ins('bne.b','gameplay_pc_0170ba',2)
    e.label('gameplay_pc_0170b6')
    e.ins('bsr.w','gameplay_pc_0171a6',4)
    e.label('gameplay_pc_0170ba')
    e.ins('cmpi.w','#0x8,%d0',4)
    e.label('gameplay_pc_0170be')
    e.ins('bne.b','gameplay_pc_0170c4',2)
    e.label('gameplay_pc_0170c0')
    e.ins('bsr.w','gameplay_pc_0171a6',4)
    e.label('gameplay_pc_0170c4')
    e.ins('cmpi.w','#0xe,%d0',4)
    e.label('gameplay_pc_0170c8')
    e.ins('bne.b','gameplay_pc_0170ce',2)
    e.label('gameplay_pc_0170ca')
    e.ins('bsr.w','gameplay_pc_0171a6',4)
    e.label('gameplay_pc_0170ce')
    e.ins('cmpi.b','#0x6,0xf375:w',6)
    e.label('gameplay_pc_0170d4')
    e.ins('bne.b','gameplay_pc_0170f4',2)
    e.label('gameplay_pc_0170d6')
    e.ins('cmpi.w','#0x5,%d0',4)
    e.label('gameplay_pc_0170da')
    e.ins('bne.b','gameplay_pc_0170e0',2)
    e.label('gameplay_pc_0170dc')
    e.ins('bsr.w','gameplay_pc_0171a6',4)
    e.label('gameplay_pc_0170e0')
    e.ins('cmpi.w','#0x8,%d0',4)
    e.label('gameplay_pc_0170e4')
    e.ins('bne.b','gameplay_pc_0170ea',2)
    e.label('gameplay_pc_0170e6')
    e.ins('bsr.w','gameplay_pc_0171a6',4)
    e.label('gameplay_pc_0170ea')
    e.ins('cmpi.w','#0xe,%d0',4)
    e.label('gameplay_pc_0170ee')
    e.ins('bne.b','gameplay_pc_0170f4',2)
    e.label('gameplay_pc_0170f0')
    e.ins('bsr.w','gameplay_pc_0171a6',4)
    e.label('gameplay_pc_0170f4')
    e.ins('addq.w','#0x1,%d0',2)
    e.label('gameplay_pc_0170f6')
    e.ins('cmpi.w','#0x27,%d0',4)
    e.label('gameplay_pc_0170fa')
    e.ins('bcs.b','gameplay_pc_017082',2)
    e.label('gameplay_pc_0170fc')
    e.ins('cmpi.b','#0xff,0xd420:w',6)
    e.label('gameplay_pc_017102')
    e.ins('beq.b','gameplay_pc_017156',2)
    e.label('gameplay_pc_017104')
    e.ins('move.w','#0x23,0xff7026:l',8)
    e.label('gameplay_pc_01710c')
    e.ins('jsr','gameplay_pc_01072c:l',6)
    e.label('gameplay_pc_017112')
    e.ins('move.w','#0xb0,%d2',4)
    e.label('gameplay_pc_017116')
    e.ins('bsr.w','gameplay_pc_017058',4)
    e.label('gameplay_pc_01711a')
    e.ins('tst.w','0xd448:w',4)
    e.label('gameplay_pc_01711e')
    e.ins('bne.b','gameplay_pc_017138',2)
    e.label('gameplay_pc_017120')
    e.ins('move.w','0xf67a:w,%d4',4)
    e.label('gameplay_pc_017124')
    e.ins('bsr.w','gameplay_pc_017158',4)
    e.label('gameplay_pc_017128')
    e.ins('move.w','0xf67c:w,%d4',4)
    e.label('gameplay_pc_01712c')
    e.ins('bsr.w','gameplay_pc_017158',4)
    e.label('gameplay_pc_017130')
    e.ins('move.w','0xf67e:w,%d4',4)
    e.label('gameplay_pc_017134')
    e.ins('bsr.w','gameplay_pc_017158',4)
    e.label('gameplay_pc_017138')
    e.ins('move.l','#0x4a000003,0xc00004:l',10)
    e.label('gameplay_pc_017142')
    e.ins('lea.l','0xc00000:l,%a5',6)
    e.label('gameplay_pc_017148')
    e.ins('move.w','#0x0,%d6',4)
    e.label('gameplay_pc_01714c')
    e.ins('move.w','#0x1ff,%d7',4)
    e.label('gameplay_pc_017150')
    e.ins('move.w','%d6,(%a5)',2)
    e.label('gameplay_pc_017152')
    e.ins('dbra','%d7,gameplay_pc_017150',4)
    e.label('gameplay_pc_017156')
    e.ins('rts','',2)

def _lower_show_first_calendar_event_values(e,rules):
    e.label('gameplay_pc_017158')
    e.ins('moveq','#0,%d0',2)
    e.label('gameplay_pc_01715a')
    e.ins('moveq','#0,%d3',2)
    e.label('gameplay_pc_01715c')
    e.ins('lea.l','0xd420:w,%a0',4)
    e.label('gameplay_pc_017160')
    e.ins('lea.l','0xf428:w,%a1',4)
    e.label('gameplay_pc_017164')
    e.ins('moveq','#0,%d1',2)
    e.label('gameplay_pc_017166')
    e.ins('move.b','(%a0, %d0.w),%d1',4)
    e.label('gameplay_pc_01716a')
    e.ins('cmpi.b','#0xff,%d1',4)
    e.label('gameplay_pc_01716e')
    e.ins('beq.b','gameplay_pc_0171a4',2)
    e.label('gameplay_pc_017170')
    e.ins('moveq','#0,%d2',2)
    e.label('gameplay_pc_017172')
    e.ins('move.b','(%a1, %d1.w),%d2',4)
    e.label('gameplay_pc_017176')
    e.ins('cmp.w','%d4,%d2',2)
    e.label('gameplay_pc_017178')
    e.ins('bne.w','gameplay_pc_0171a0',4)
    e.label('gameplay_pc_01717c')
    e.ins('move.w','%d1,0xf646:w',4)
    e.label('gameplay_pc_017180')
    e.ins('addq.w','#0x1,0xf646:w',4)
    e.label('gameplay_pc_017184')
    e.ins('move.w','%d2,0xf376:w',4)
    e.label('gameplay_pc_017188')
    e.ins('tst.w','%d3',2)
    e.label('gameplay_pc_01718a')
    e.ins('bne.w','gameplay_pc_017198',4)
    e.label('gameplay_pc_01718e')
    e.ins('move.w','#0xb2,%d2',4)
    e.label('gameplay_pc_017192')
    e.ins('bsr.w','gameplay_pc_017058',4)
    e.label('gameplay_pc_017196')
    e.ins('moveq','#1,%d3',2)
    e.label('gameplay_pc_017198')
    e.ins('move.w','#0xae,%d2',4)
    e.label('gameplay_pc_01719c')
    e.ins('bsr.w','gameplay_pc_017058',4)
    e.label('gameplay_pc_0171a0')
    e.ins('addq.w','#0x1,%d0',2)
    e.label('gameplay_pc_0171a2')
    e.ins('bra.b','gameplay_pc_01715c',2)
    e.label('gameplay_pc_0171a4')
    e.ins('rts','',2)

def _lower_process_second_calendar_event(e,rules):
    e.label('gameplay_pc_0171fc')
    e.ins('moveq','#0,%d0',2)
    e.label('gameplay_pc_0171fe')
    e.ins('moveq','#0,%d1',2)
    e.label('gameplay_pc_017200')
    e.ins('cmpi.b','#0x9,0xf375:w',6)
    e.label('gameplay_pc_017206')
    e.ins('bne.b','gameplay_pc_017226',2)
    e.label('gameplay_pc_017208')
    e.ins('cmpi.w','#0x4,%d0',4)
    e.label('gameplay_pc_01720c')
    e.ins('bne.b','gameplay_pc_017212',2)
    e.label('gameplay_pc_01720e')
    e.ins('bsr.w','gameplay_pc_017342',4)
    e.label('gameplay_pc_017212')
    e.ins('cmpi.w','#0x6,%d0',4)
    e.label('gameplay_pc_017216')
    e.ins('bne.b','gameplay_pc_01721c',2)
    e.label('gameplay_pc_017218')
    e.ins('bsr.w','gameplay_pc_017342',4)
    e.label('gameplay_pc_01721c')
    e.ins('cmpi.w','#0x7,%d0',4)
    e.label('gameplay_pc_017220')
    e.ins('bne.b','gameplay_pc_017226',2)
    e.label('gameplay_pc_017222')
    e.ins('bsr.w','gameplay_pc_017342',4)
    e.label('gameplay_pc_017226')
    e.ins('cmpi.b','#0x8,0xf375:w',6)
    e.label('gameplay_pc_01722c')
    e.ins('bne.b','gameplay_pc_01724c',2)
    e.label('gameplay_pc_01722e')
    e.ins('cmpi.w','#0xd,%d0',4)
    e.label('gameplay_pc_017232')
    e.ins('bne.b','gameplay_pc_017238',2)
    e.label('gameplay_pc_017234')
    e.ins('bsr.w','gameplay_pc_017342',4)
    e.label('gameplay_pc_017238')
    e.ins('cmpi.w','#0x10,%d0',4)
    e.label('gameplay_pc_01723c')
    e.ins('bne.b','gameplay_pc_017242',2)
    e.label('gameplay_pc_01723e')
    e.ins('bsr.w','gameplay_pc_017342',4)
    e.label('gameplay_pc_017242')
    e.ins('cmpi.w','#0x11,%d0',4)
    e.label('gameplay_pc_017246')
    e.ins('bne.b','gameplay_pc_01724c',2)
    e.label('gameplay_pc_017248')
    e.ins('bsr.w','gameplay_pc_017342',4)
    e.label('gameplay_pc_01724c')
    e.ins('cmpi.b','#0x4,0xf375:w',6)
    e.label('gameplay_pc_017252')
    e.ins('bne.b','gameplay_pc_017272',2)
    e.label('gameplay_pc_017254')
    e.ins('cmpi.w','#0x12,%d0',4)
    e.label('gameplay_pc_017258')
    e.ins('bne.b','gameplay_pc_01725e',2)
    e.label('gameplay_pc_01725a')
    e.ins('bsr.w','gameplay_pc_017342',4)
    e.label('gameplay_pc_01725e')
    e.ins('cmpi.w','#0x15,%d0',4)
    e.label('gameplay_pc_017262')
    e.ins('bne.b','gameplay_pc_017268',2)
    e.label('gameplay_pc_017264')
    e.ins('bsr.w','gameplay_pc_017342',4)
    e.label('gameplay_pc_017268')
    e.ins('cmpi.w','#0x16,%d0',4)
    e.label('gameplay_pc_01726c')
    e.ins('bne.b','gameplay_pc_017272',2)
    e.label('gameplay_pc_01726e')
    e.ins('bsr.w','gameplay_pc_017342',4)
    e.label('gameplay_pc_017272')
    e.ins('cmpi.b','#0x3,0xf375:w',6)
    e.label('gameplay_pc_017278')
    e.ins('bne.b','gameplay_pc_01728e',2)
    e.label('gameplay_pc_01727a')
    e.ins('cmpi.w','#0x1a,%d0',4)
    e.label('gameplay_pc_01727e')
    e.ins('bne.b','gameplay_pc_017284',2)
    e.label('gameplay_pc_017280')
    e.ins('bsr.w','gameplay_pc_017342',4)
    e.label('gameplay_pc_017284')
    e.ins('cmpi.w','#0x1f,%d0',4)
    e.label('gameplay_pc_017288')
    e.ins('bne.b','gameplay_pc_01728e',2)
    e.label('gameplay_pc_01728a')
    e.ins('bsr.w','gameplay_pc_017342',4)
    e.label('gameplay_pc_01728e')
    e.ins('addq.w','#0x1,%d0',2)
    e.label('gameplay_pc_017290')
    e.ins('cmpi.w','#0x27,%d0',4)
    e.label('gameplay_pc_017294')
    e.ins('bcs.w','gameplay_pc_017200',4)
    e.label('gameplay_pc_017298')
    e.ins('cmpi.b','#0xff,0xd420:w',6)
    e.label('gameplay_pc_01729e')
    e.ins('beq.b','gameplay_pc_0172f2',2)
    e.label('gameplay_pc_0172a0')
    e.ins('move.w','#0x25,0xff7026:l',8)
    e.label('gameplay_pc_0172a8')
    e.ins('jsr','gameplay_pc_01072c:l',6)
    e.label('gameplay_pc_0172ae')
    e.ins('move.w','#0xb1,%d2',4)
    e.label('gameplay_pc_0172b2')
    e.ins('bsr.w','gameplay_pc_017058',4)
    e.label('gameplay_pc_0172b6')
    e.ins('tst.w','0xd448:w',4)
    e.label('gameplay_pc_0172ba')
    e.ins('bne.b','gameplay_pc_0172d4',2)
    e.label('gameplay_pc_0172bc')
    e.ins('move.w','0xf67a:w,%d4',4)
    e.label('gameplay_pc_0172c0')
    e.ins('bsr.w','gameplay_pc_0172f4',4)
    e.label('gameplay_pc_0172c4')
    e.ins('move.w','0xf67c:w,%d4',4)
    e.label('gameplay_pc_0172c8')
    e.ins('bsr.w','gameplay_pc_0172f4',4)
    e.label('gameplay_pc_0172cc')
    e.ins('move.w','0xf67e:w,%d4',4)
    e.label('gameplay_pc_0172d0')
    e.ins('bsr.w','gameplay_pc_0172f4',4)
    e.label('gameplay_pc_0172d4')
    e.ins('move.l','#0x4a000003,0xc00004:l',10)
    e.label('gameplay_pc_0172de')
    e.ins('lea.l','0xc00000:l,%a5',6)
    e.label('gameplay_pc_0172e4')
    e.ins('move.w','#0x0,%d6',4)
    e.label('gameplay_pc_0172e8')
    e.ins('move.w','#0x1ff,%d7',4)
    e.label('gameplay_pc_0172ec')
    e.ins('move.w','%d6,(%a5)',2)
    e.label('gameplay_pc_0172ee')
    e.ins('dbra','%d7,gameplay_pc_0172ec',4)
    e.label('gameplay_pc_0172f2')
    e.ins('rts','',2)

def _lower_show_second_calendar_event_values(e,rules):
    e.label('gameplay_pc_0172f4')
    e.ins('moveq','#0,%d0',2)
    e.label('gameplay_pc_0172f6')
    e.ins('moveq','#0,%d3',2)
    e.label('gameplay_pc_0172f8')
    e.ins('lea.l','0xd420:w,%a0',4)
    e.label('gameplay_pc_0172fc')
    e.ins('lea.l','0xf428:w,%a1',4)
    e.label('gameplay_pc_017300')
    e.ins('moveq','#0,%d1',2)
    e.label('gameplay_pc_017302')
    e.ins('move.b','(%a0, %d0.w),%d1',4)
    e.label('gameplay_pc_017306')
    e.ins('cmpi.b','#0xff,%d1',4)
    e.label('gameplay_pc_01730a')
    e.ins('beq.b','gameplay_pc_017340',2)
    e.label('gameplay_pc_01730c')
    e.ins('moveq','#0,%d2',2)
    e.label('gameplay_pc_01730e')
    e.ins('move.b','(%a1, %d1.w),%d2',4)
    e.label('gameplay_pc_017312')
    e.ins('cmp.w','%d4,%d2',2)
    e.label('gameplay_pc_017314')
    e.ins('bne.w','gameplay_pc_01733c',4)
    e.label('gameplay_pc_017318')
    e.ins('move.w','%d1,0xf646:w',4)
    e.label('gameplay_pc_01731c')
    e.ins('addq.w','#0x1,0xf646:w',4)
    e.label('gameplay_pc_017320')
    e.ins('move.w','%d2,0xf376:w',4)
    e.label('gameplay_pc_017324')
    e.ins('tst.w','%d3',2)
    e.label('gameplay_pc_017326')
    e.ins('bne.w','gameplay_pc_017334',4)
    e.label('gameplay_pc_01732a')
    e.ins('move.w','#0xb2,%d2',4)
    e.label('gameplay_pc_01732e')
    e.ins('bsr.w','gameplay_pc_017058',4)
    e.label('gameplay_pc_017332')
    e.ins('moveq','#1,%d3',2)
    e.label('gameplay_pc_017334')
    e.ins('move.w','#0xaf,%d2',4)
    e.label('gameplay_pc_017338')
    e.ins('bsr.w','gameplay_pc_017058',4)
    e.label('gameplay_pc_01733c')
    e.ins('addq.w','#0x1,%d0',2)
    e.label('gameplay_pc_01733e')
    e.ins('bra.b','gameplay_pc_0172f8',2)
    e.label('gameplay_pc_017340')
    e.ins('rts','',2)

def _lower_process_third_calendar_event(e,rules):
    e.label('gameplay_pc_0173a6')
    e.ins('moveq','#0,%d0',2)
    e.label('gameplay_pc_0173a8')
    e.ins('moveq','#0,%d1',2)
    e.label('gameplay_pc_0173aa')
    e.ins('btst.b','#0x0,0xf375:w',6)
    e.label('gameplay_pc_0173b0')
    e.ins('bne.b','gameplay_pc_0173d2',2)
    e.label('gameplay_pc_0173b2')
    e.ins('lea.l','0xf428:w,%a0',4)
    e.label('gameplay_pc_0173b6')
    e.ins('move.b','(%a0, %d0.w),%d7',4)
    e.label('gameplay_pc_0173ba')
    e.ins('bmi.b','gameplay_pc_0173d2',2)
    e.label('gameplay_pc_0173bc')
    e.ins('cmp.w','0xf67a:w,%d7',4)
    e.label('gameplay_pc_0173c0')
    e.ins('beq.b','gameplay_pc_0173ce',2)
    e.label('gameplay_pc_0173c2')
    e.ins('cmp.w','0xf67c:w,%d7',4)
    e.label('gameplay_pc_0173c6')
    e.ins('beq.b','gameplay_pc_0173ce',2)
    e.label('gameplay_pc_0173c8')
    e.ins('cmp.w','0xf67e:w,%d7',4)
    e.label('gameplay_pc_0173cc')
    e.ins('bne.b','gameplay_pc_0173d2',2)
    e.label('gameplay_pc_0173ce')
    e.ins('bsr.w','gameplay_pc_017474',4)
    e.label('gameplay_pc_0173d2')
    e.ins('addq.w','#0x1,%d0',2)
    e.label('gameplay_pc_0173d4')
    e.ins('cmpi.w','#0x27,%d0',4)
    e.label('gameplay_pc_0173d8')
    e.ins('bcs.b','gameplay_pc_0173aa',2)
    e.label('gameplay_pc_0173da')
    e.ins('tst.w','0xd448:w',4)
    e.label('gameplay_pc_0173de')
    e.ins('bne.b','gameplay_pc_017424',2)
    e.label('gameplay_pc_0173e0')
    e.ins('move.w','#0x27,0xff7026:l',8)
    e.label('gameplay_pc_0173e8')
    e.ins('jsr','gameplay_pc_01072c:l',6)
    e.label('gameplay_pc_0173ee')
    e.ins('move.w','0xf67a:w,%d4',4)
    e.label('gameplay_pc_0173f2')
    e.ins('bsr.w','gameplay_pc_017426',4)
    e.label('gameplay_pc_0173f6')
    e.ins('move.w','0xf67c:w,%d4',4)
    e.label('gameplay_pc_0173fa')
    e.ins('bsr.w','gameplay_pc_017426',4)
    e.label('gameplay_pc_0173fe')
    e.ins('move.w','0xf67e:w,%d4',4)
    e.label('gameplay_pc_017402')
    e.ins('bsr.w','gameplay_pc_017426',4)
    e.label('gameplay_pc_017406')
    e.ins('move.l','#0x4a000003,0xc00004:l',10)
    e.label('gameplay_pc_017410')
    e.ins('lea.l','0xc00000:l,%a5',6)
    e.label('gameplay_pc_017416')
    e.ins('move.w','#0x0,%d6',4)
    e.label('gameplay_pc_01741a')
    e.ins('move.w','#0x1ff,%d7',4)
    e.label('gameplay_pc_01741e')
    e.ins('move.w','%d6,(%a5)',2)
    e.label('gameplay_pc_017420')
    e.ins('dbra','%d7,gameplay_pc_01741e',4)
    e.label('gameplay_pc_017424')
    e.ins('rts','',2)

def _lower_show_third_calendar_event_values(e,rules):
    e.label('gameplay_pc_017426')
    e.ins('moveq','#0,%d0',2)
    e.label('gameplay_pc_017428')
    e.ins('moveq','#0,%d3',2)
    e.label('gameplay_pc_01742a')
    e.ins('lea.l','0xd420:w,%a0',4)
    e.label('gameplay_pc_01742e')
    e.ins('lea.l','0xf428:w,%a1',4)
    e.label('gameplay_pc_017432')
    e.ins('moveq','#0,%d1',2)
    e.label('gameplay_pc_017434')
    e.ins('move.b','(%a0, %d0.w),%d1',4)
    e.label('gameplay_pc_017438')
    e.ins('cmpi.b','#0xff,%d1',4)
    e.label('gameplay_pc_01743c')
    e.ins('beq.b','gameplay_pc_017472',2)
    e.label('gameplay_pc_01743e')
    e.ins('moveq','#0,%d2',2)
    e.label('gameplay_pc_017440')
    e.ins('move.b','(%a1, %d1.w),%d2',4)
    e.label('gameplay_pc_017444')
    e.ins('cmp.w','%d4,%d2',2)
    e.label('gameplay_pc_017446')
    e.ins('bne.w','gameplay_pc_01746e',4)
    e.label('gameplay_pc_01744a')
    e.ins('move.w','%d1,0xf646:w',4)
    e.label('gameplay_pc_01744e')
    e.ins('addq.w','#0x1,0xf646:w',4)
    e.label('gameplay_pc_017452')
    e.ins('move.w','%d2,0xf376:w',4)
    e.label('gameplay_pc_017456')
    e.ins('tst.w','%d3',2)
    e.label('gameplay_pc_017458')
    e.ins('bne.w','gameplay_pc_017466',4)
    e.label('gameplay_pc_01745c')
    e.ins('move.w','#0xb2,%d2',4)
    e.label('gameplay_pc_017460')
    e.ins('bsr.w','gameplay_pc_017058',4)
    e.label('gameplay_pc_017464')
    e.ins('moveq','#1,%d3',2)
    e.label('gameplay_pc_017466')
    e.ins('move.w','#0xb3,%d2',4)
    e.label('gameplay_pc_01746a')
    e.ins('bsr.w','gameplay_pc_017058',4)
    e.label('gameplay_pc_01746e')
    e.ins('addq.w','#0x1,%d0',2)
    e.label('gameplay_pc_017470')
    e.ins('bra.b','gameplay_pc_01742a',2)
    e.label('gameplay_pc_017472')
    e.ins('rts','',2)

LOWERERS = {
    'process_calendar_city_cycle':_lower_process_calendar_city_cycle,
    'scan_calendar_officer_mortality':_lower_scan_calendar_officer_mortality,
    'remove_mortal_officer_with_message':_lower_remove_mortal_officer_with_message,
    'choose_city_head_after_mortality':_lower_choose_city_head_after_mortality,
    'process_calendar_event_schedulers':_lower_process_calendar_event_schedulers,
    'show_calendar_event_message':_lower_show_calendar_event_message,
    'process_first_calendar_event':_lower_process_first_calendar_event,
    'show_first_calendar_event_values':_lower_show_first_calendar_event_values,
    'process_second_calendar_event':_lower_process_second_calendar_event,
    'show_second_calendar_event_values':_lower_show_second_calendar_event_values,
    'process_third_calendar_event':_lower_process_third_calendar_event,
    'show_third_calendar_event_values':_lower_show_third_calendar_event_values,
}

def compile_calendar(source):
    records=semantic_functions(source,DECLARATIONS,APPROVED)
    records['show_calendar_event_message']['rules'] = records['show_calendar_event_message_fields']['rules']
    sole_calendar_fields={name:records[name]['effects'] for name in ('_calendar_clear_event_plane_fields', '_calendar_device_store_fields', '_calendar_event_display_fields', '_calendar_event_owner_values_fields', '_calendar_legacy_context_fields', '_calendar_seasonal_submission_fields', 'choose_city_head_after_mortality_fields', 'process_calendar_city_cycle_fields', 'process_calendar_event_schedulers_fields', 'process_first_calendar_event_fields', 'process_second_calendar_event_fields', 'process_third_calendar_event_fields', 'remove_mortal_officer_with_message_fields', 'scan_calendar_officer_mortality_fields', 'show_calendar_event_message_fields', 'show_first_calendar_event_values_fields', 'show_second_calendar_event_values_fields', 'show_third_calendar_event_values_fields')}
    for owner in ('process_calendar_city_cycle', 'scan_calendar_officer_mortality', 'remove_mortal_officer_with_message', 'choose_city_head_after_mortality', 'process_calendar_event_schedulers', 'show_calendar_event_message', 'process_first_calendar_event', 'show_first_calendar_event_values', 'process_second_calendar_event', 'show_second_calendar_event_values', 'process_third_calendar_event', 'show_third_calendar_event_values'):
        records[owner]['effects']=dict(legacy_projection=records[owner]['effects'],sole_current_calendar_fields=sole_calendar_fields)
    return lower_declared({b.name:records[b.name] for b in CALENDAR_BINDINGS},CALENDAR_BINDINGS,LOWERERS)

# D52 exact imports/full DECL; ordinary mnemonic lowerers unchanged.
APPROVED.setdefault('business_reuse',set()).update(('_calendar_arithmetic_fields', '_calendar_bit_fields', '_calendar_call_fields', '_calendar_compare_fields', '_calendar_db_fields', '_calendar_frame_fields', '_calendar_legacy_entry_fields', '_calendar_memory_arithmetic_fields', '_calendar_move_fields', '_calendar_pop_word_fields', '_calendar_push_word_fields', '_calendar_restore_fields', '_calendar_save_fields', '_calendar_shift_fields', '_calendar_test_fields', '_calendar_write_fields'))
APPROVED.setdefault('contexts_services',set()).update(('SceneRefreshBoundary', 'SceneRefreshMemory'))
APPROVED.setdefault((2, 'high_level_battle_ai.contexts_first_deployment'),set()).update(('FirstDeploymentFrame', 'first_replace'))
APPROVED.setdefault((2, 'high_level_scene_flows.domain'),set()).update(('low16', 'low8'))
DECLARATIONS.update({'_calendar_clear_event_plane_fields': {'flow': 'frame = _calendar_device_store_fields(memory, frame, pc, 12582916, 1241513987, 4)\n'
                                                'frame = first_replace(frame, scratch=memory.cursor_at(12582912))\n'
                                                "frame = _calendar_move_fields(memory, frame, 'offset_y', 0)\n"
                                                "frame = _calendar_move_fields(memory, frame, 'choice', 511)\n"
                                                'while True:\n'
                                                '    frame = _calendar_device_store_fields(memory, frame, pc + 24, frame.scratch.base, '
                                                'low16(frame.offset_y), 2)\n'
                                                "    frame, again = _calendar_db_fields(frame, 'choice')\n"
                                                '    if not again:\n'
                                                '        return frame',
                                        'returns': None,
                                        'signature': 'memory, frame, pc'},
 '_calendar_device_store_fields': {'flow': 'if not 4294901760 <= address <= 4294967295:\n    if (pc, address, width) not in ((94520, 12582916, 4), (94544, 12582912, 2), (94932, 12582916, 4), (94956, 12582912, 2), (95238, 12582916, 4), (95262, 12582912, 2)):\n        raise SceneRefreshBoundary(pc, frame, None)\n    frame = _calendar_frame_fields(memory, frame, pc)\nreturn _calendar_write_fields(memory, frame, address, value, width)', 'returns': None, 'signature': 'memory, frame, pc, address, value, width'},
 '_calendar_event_display_fields': {'flow': 'frame = _calendar_compare_fields(memory, frame, memory.state.read(4294956064, 1), 255, 1)\n'
                                            'if frame.status & 4:\n'
                                            '    return frame\n'
                                            'frame = _calendar_write_fields(memory, frame, 16740390, scene)\n'
                                            'frame = _calendar_call_fields(memory, frame, 67372, load_token)\n'
                                            "frame = _calendar_move_fields(memory, frame, 'unit', message)\n"
                                            'frame = _calendar_call_fields(memory, frame, 94296, message_token)\n'
                                            'frame = _calendar_test_fields(memory, frame, memory.state.read(4294956104, 2))\n'
                                            'if frame.status & 4:\n'
                                            '    for address, token in ((4294964858, value_tokens[0]), (4294964860, value_tokens[1]), '
                                            '(4294964862, value_tokens[2])):\n'
                                            "        frame = _calendar_move_fields(memory, frame, 'distance', memory.state.read(address, "
                                            '2))\n'
                                            '        frame = _calendar_call_fields(memory, frame, values_target, token)\n'
                                            'return _calendar_clear_event_plane_fields(memory, frame, clear_pc)',
                                    'returns': None,
                                    'signature': 'memory, frame, scene, load_token, message, message_token, values_target, value_tokens, '
                                                 'clear_pc'},
 '_calendar_event_owner_values_fields': {'flow': "frame = _calendar_frame_fields(memory, frame, entry)\nframe = _calendar_move_fields(memory, frame, 'target_x', 0, 4)\nframe = _calendar_move_fields(memory, frame, 'count', 0, 4)\nwhile True:\n    frame = first_replace(frame, roster=memory.cursor_at(4294956064), candidates=memory.cursor_at(4294964264))\n    frame = _calendar_move_fields(memory, frame, 'target_y', 0, 4)\n    frame = _calendar_move_fields(memory, frame, 'target_y', frame.roster.byte(low16(frame.target_x)), 1)\n    frame = _calendar_compare_fields(memory, frame, low8(frame.target_y), 255, 1)\n    if frame.status & 4:\n        return frame\n    frame = _calendar_move_fields(memory, frame, 'unit', 0, 4)\n    frame = _calendar_move_fields(memory, frame, 'unit', frame.candidates.byte(low16(frame.target_y)), 1)\n    frame = _calendar_compare_fields(memory, frame, low16(frame.unit), low16(frame.distance))\n    if frame.status & 4:\n        frame = _calendar_write_fields(memory, frame, 4294964806, low16(frame.target_y))\n        from .business_reuse import _calendar_memory_arithmetic_fields\n        frame = _calendar_memory_arithmetic_fields(memory, frame, 4294964806, 1)\n        frame = _calendar_write_fields(memory, frame, 4294964086, low16(frame.unit))\n        frame = _calendar_test_fields(memory, frame, low16(frame.count))\n        if frame.status & 4:\n            frame = _calendar_move_fields(memory, frame, 'unit', 178)\n            frame = _calendar_call_fields(memory, frame, 94296, heading_token)\n            frame = _calendar_move_fields(memory, frame, 'count', 1, 4)\n        frame = _calendar_move_fields(memory, frame, 'unit', detail_message)\n        frame = _calendar_call_fields(memory, frame, 94296, detail_token)\n    frame = _calendar_arithmetic_fields(memory, frame, 'target_x', 1)",
                                         'returns': None,
                                         'signature': 'memory, frame, entry, heading_token, detail_token, detail_message'},
 '_calendar_legacy_context_fields': {'flow': 'checked_state(state)\n'
                                             "if kind == 'calendar':\n"
                                             '    if type(retained) is not CalendarContext:\n'
                                             "        raise ValueError('original calendar context required')\n"
                                             "elif kind == 'mortality':\n"
                                             '    if type(retained) is not MortalityContext:\n'
                                             "        raise ValueError('original mortality context required')\n"
                                             "elif kind == 'event':\n"
                                             '    if type(retained) is not EventContext:\n'
                                             "        raise ValueError('original event context required')\n"
                                             'else:\n'
                                             "    raise ValueError('closed historical calendar context role required')\n"
                                             'from .business_reuse import _calendar_legacy_entry_fields\n'
                                             'return _calendar_legacy_entry_fields(state)',
                                     'returns': None,
                                     'signature': 'state, retained, kind'},
 '_calendar_seasonal_submission_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, entry)\n'
                                                  "frame = _calendar_move_fields(memory, frame, 'target_x', 0, 4)\n"
                                                  "frame = _calendar_move_fields(memory, frame, 'target_y', 0, 4)\n"
                                                  'while True:\n'
                                                  '    for month, cities in blocks:\n'
                                                  '        frame = _calendar_compare_fields(memory, frame, memory.state.read(4294964085, '
                                                  '1), month, 1)\n'
                                                  '        if frame.status & 4:\n'
                                                  '            for city, token in cities:\n'
                                                  '                frame = _calendar_compare_fields(memory, frame, low16(frame.target_x), '
                                                  'city)\n'
                                                  '                if frame.status & 4:\n'
                                                  '                    frame = _calendar_call_fields(memory, frame, target, token)\n'
                                                  "    frame = _calendar_arithmetic_fields(memory, frame, 'target_x', 1)\n"
                                                  '    frame = _calendar_compare_fields(memory, frame, low16(frame.target_x), 39)\n'
                                                  '    if not frame.status & 1:\n'
                                                  '        return frame',
                                          'returns': None,
                                          'signature': 'memory, frame, entry, blocks, target'},
 'choose_city_head_after_mortality': {'flow': 'from .business_reuse import _calendar_legacy_entry_fields\n'
                                              "memory, entered = _calendar_legacy_entry_fields(state, (city,), (), (('candidates', "
                                              'assignments),))\n'
                                              'actual = choose_city_head_after_mortality_fields(memory, entered)\n'
                                              'return low16(actual.target_x)',
                                      'returns': 'Word',
                                      'signature': 'state: GameplayState, city: Word, assignments: Table'},
 'choose_city_head_after_mortality_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 94170)\n'
                                                     'frame = first_replace(frame, scan=memory.cursor_at(4294964480))\n'
                                                     "frame = _calendar_move_fields(memory, frame, 'target_y', 255)\n"
                                                     'while True:\n'
                                                     '    frame = _calendar_compare_fields(memory, frame, low8(frame.target_x), '
                                                     'frame.candidates.byte(low16(frame.target_y)), 1)\n'
                                                     '    if frame.status & 4:\n'
                                                     '        frame = _calendar_write_fields(memory, frame, frame.scan.base, '
                                                     'low16(frame.target_y))\n'
                                                     '        frame = first_replace(frame, scan=frame.scan.advance(2))\n'
                                                     "    frame, again = _calendar_db_fields(frame, 'target_y')\n"
                                                     '    if not again:\n'
                                                     '        break\n'
                                                     'frame = _calendar_write_fields(memory, frame, frame.scan.base, 65535)\n'
                                                     'return _calendar_call_fields(memory, frame, 57846, 94202)',
                                             'returns': 'FirstDeploymentFrame',
                                             'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'process_calendar_city_cycle': {'flow': 'from .business_reuse import _calendar_legacy_entry_fields\n'
                                         "memory, entered = _calendar_legacy_context_fields(state, retained, 'calendar')\n"
                                         'actual = process_calendar_city_cycle_fields(memory, entered)\n'
                                         'return retained',
                                 'returns': 'CalendarContext',
                                 'signature': 'state: GameplayState, retained: CalendarContext=CalendarContext()'},
 'process_calendar_city_cycle_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 92986)\n'
                                                'memory.state.sr = 9984\n'
                                                'frame = first_replace(frame, status=0)\n'
                                                'frame = _calendar_push_word_fields(memory, frame, memory.state.read(4294964086, 2))\n'
                                                "frame = _calendar_move_fields(memory, frame, 'target_x', 39)\n"
                                                "frame = _calendar_move_fields(memory, frame, 'target_y', memory.state.read(4294964085, "
                                                '1), 1)\n'
                                                'frame = first_replace(frame, auxiliary=memory.cursor_at(4294964304))\n'
                                                'frame = _calendar_test_fields(memory, frame, low8(frame.target_y), 1)\n'
                                                'if frame.status & 4:\n'
                                                '    frame = first_replace(frame, roster=memory.cursor_at(4294959580))\n'
                                                '    while True:\n'
                                                '        frame = first_replace(frame, auxiliary=frame.auxiliary.advance(-1))\n'
                                                '        frame = _calendar_test_fields(memory, frame, frame.auxiliary.byte(), 1)\n'
                                                '        if not frame.status & 8:\n'
                                                '            frame = _calendar_call_fields(memory, frame, 93194, 93022)\n'
                                                '        frame = first_replace(frame, roster=frame.roster.advance(-4))\n'
                                                "        frame, again = _calendar_db_fields(frame, 'target_x')\n"
                                                '        if not again:\n'
                                                '            break\n'
                                                'else:\n'
                                                '    frame = _calendar_compare_fields(memory, frame, low8(frame.target_y), 3, 1)\n'
                                                '    if frame.status & 4:\n'
                                                '        phases = ((93228, 93046), (93456, 93050))\n'
                                                '    else:\n'
                                                '        frame = _calendar_compare_fields(memory, frame, low8(frame.target_y), 9, 1)\n'
                                                '        phases = ((93254, 93070), (93482, 93074)) if frame.status & 4 else ()\n'
                                                '    if phases:\n'
                                                '        while True:\n'
                                                '            frame = first_replace(frame, auxiliary=frame.auxiliary.advance(-1))\n'
                                                '            frame = _calendar_test_fields(memory, frame, frame.auxiliary.byte(), 1)\n'
                                                '            if not frame.status & 8:\n'
                                                '                for target, token in phases:\n'
                                                '                    frame = _calendar_call_fields(memory, frame, target, token)\n'
                                                "            frame, again = _calendar_db_fields(frame, 'target_x')\n"
                                                '            if not again:\n'
                                                '                break\n'
                                                'frame = _calendar_bit_fields(memory, frame, memory.state.read(4294964085, 1), 1)\n'
                                                'if frame.status & 4:\n'
                                                '    frame = _calendar_call_fields(memory, frame, 93112, 93092)\n'
                                                'frame = _calendar_call_fields(memory, frame, 93914, 93096)\n'
                                                'frame = _calendar_call_fields(memory, frame, 94204, 93100)\n'
                                                'frame = _calendar_pop_word_fields(memory, frame, 4294964086)\n'
                                                'return _calendar_call_fields(memory, frame, 44872, 93110)',
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'process_calendar_event_schedulers': {'flow': 'from .business_reuse import _calendar_legacy_entry_fields\n'
                                               "memory, entered = _calendar_legacy_context_fields(state, retained, 'event')\n"
                                               'actual = process_calendar_event_schedulers_fields(memory, entered)\n'
                                               'return retained',
                                       'returns': 'EventContext',
                                       'signature': 'state: GameplayState, retained: EventContext=EventContext()'},
 'process_calendar_event_schedulers_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 94204)\n'
                                                      'for target, token in ((94230, 94208), (94334, 94212), (94230, 94216), (94716, '
                                                      '94220), (94230, 94224), (95142, 94228)):\n'
                                                      '    frame = _calendar_call_fields(memory, frame, target, token)\n'
                                                      'return frame',
                                              'returns': 'FirstDeploymentFrame',
                                              'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'process_first_calendar_event': {'flow': 'from .business_reuse import _calendar_legacy_entry_fields\n'
                                          "memory, entered = _calendar_legacy_context_fields(state, retained, 'event')\n"
                                          'actual = process_first_calendar_event_fields(memory, entered)\n'
                                          'return retained',
                                  'returns': 'EventContext',
                                  'signature': 'state: GameplayState, retained: EventContext=EventContext()'},
 'process_first_calendar_event_fields': {'flow': 'blocks = ((5, ((5, 94356), (8, 94366), (14, 94376))), (6, ((5, 94394), (8, 94404), (14, '
                                                 '94414))), (6, ((5, 94432), (8, 94442), (14, 94452))))\n'
                                                 'frame = _calendar_seasonal_submission_fields(memory, frame, 94334, blocks, 94630)\n'
                                                 'return _calendar_event_display_fields(memory, frame, 35, 94482, 176, 94490, 94552, '
                                                 '(94504, 94512, 94520), 94520)',
                                         'returns': 'FirstDeploymentFrame',
                                         'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'process_second_calendar_event': {'flow': 'from .business_reuse import _calendar_legacy_entry_fields\n'
                                           "memory, entered = _calendar_legacy_context_fields(state, retained, 'event')\n"
                                           'actual = process_second_calendar_event_fields(memory, entered)\n'
                                           'return retained',
                                   'returns': 'EventContext',
                                   'signature': 'state: GameplayState, retained: EventContext=EventContext()'},
 'process_second_calendar_event_fields': {'flow': 'blocks = ((9, ((4, 94738), (6, 94748), (7, 94758))), (8, ((13, 94776), (16, 94786), '
                                                  '(17, 94796))), (4, ((18, 94814), (21, 94824), (22, 94834))), (3, ((26, 94852), (31, '
                                                  '94862))))\n'
                                                  'frame = _calendar_seasonal_submission_fields(memory, frame, 94716, blocks, 95042)\n'
                                                  'return _calendar_event_display_fields(memory, frame, 37, 94894, 177, 94902, 94964, '
                                                  '(94916, 94924, 94932), 94932)',
                                          'returns': 'FirstDeploymentFrame',
                                          'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'process_third_calendar_event': {'flow': 'from .business_reuse import _calendar_legacy_entry_fields\n'
                                          "memory, entered = _calendar_legacy_context_fields(state, retained, 'event')\n"
                                          'actual = process_third_calendar_event_fields(memory, entered)\n'
                                          'return retained',
                                  'returns': 'EventContext',
                                  'signature': 'state: GameplayState, retained: EventContext=EventContext()'},
 'process_third_calendar_event_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 95142)\n'
                                                 "frame = _calendar_move_fields(memory, frame, 'target_x', 0, 4)\n"
                                                 "frame = _calendar_move_fields(memory, frame, 'target_y', 0, 4)\n"
                                                 'while True:\n'
                                                 '    frame = _calendar_bit_fields(memory, frame, memory.state.read(4294964085, 1), 1)\n'
                                                 '    if frame.status & 4:\n'
                                                 '        frame = first_replace(frame, roster=memory.cursor_at(4294964264))\n'
                                                 "        frame = _calendar_move_fields(memory, frame, 'choice', "
                                                 'frame.roster.byte(low16(frame.target_x)), 1)\n'
                                                 '        if not frame.status & 8:\n'
                                                 '            for address in (4294964858, 4294964860, 4294964862):\n'
                                                 '                frame = _calendar_compare_fields(memory, frame, low16(frame.choice), '
                                                 'memory.state.read(address, 2))\n'
                                                 '                if frame.status & 4:\n'
                                                 '                    frame = _calendar_call_fields(memory, frame, 95348, 95186)\n'
                                                 '                    break\n'
                                                 "    frame = _calendar_arithmetic_fields(memory, frame, 'target_x', 1)\n"
                                                 '    frame = _calendar_compare_fields(memory, frame, low16(frame.target_x), 39)\n'
                                                 '    if not frame.status & 1:\n'
                                                 '        break\n'
                                                 'frame = _calendar_test_fields(memory, frame, memory.state.read(4294956104, 2))\n'
                                                 'if not frame.status & 4:\n'
                                                 '    return frame\n'
                                                 'frame = _calendar_write_fields(memory, frame, 16740390, 39)\n'
                                                 'frame = _calendar_call_fields(memory, frame, 67372, 95214)\n'
                                                 'for address, token in ((4294964858, 95222), (4294964860, 95230), (4294964862, 95238)):\n'
                                                 "    frame = _calendar_move_fields(memory, frame, 'distance', memory.state.read(address, "
                                                 '2))\n'
                                                 '    frame = _calendar_call_fields(memory, frame, 95270, token)\n'
                                                 'return _calendar_clear_event_plane_fields(memory, frame, 95238)',
                                         'returns': 'FirstDeploymentFrame',
                                         'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'remove_mortal_officer_with_message': {'flow': 'from .business_reuse import _calendar_legacy_entry_fields\n'
                                                'memory, entered = _calendar_legacy_entry_fields(state, (officer, retained_owner_lookup), '
                                                "(), (('candidates', assignments),))\n"
                                                'actual = remove_mortal_officer_with_message_fields(memory, entered)\n'
                                                'return low16(actual.target_y)',
                                        'returns': 'Word',
                                        'signature': 'state: GameplayState, officer: Word, assignments: Table, retained_owner_lookup: '
                                                     'Word=0'},
 'remove_mortal_officer_with_message_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 94018)\n'
                                                       "frame = _calendar_save_fields(memory, frame, ('scan', 'opponent'))\n"
                                                       "frame = _calendar_move_fields(memory, frame, 'target_x', "
                                                       'frame.candidates.byte(low16(frame.offset_y)), 1)\n'
                                                       'frame = first_replace(frame, opponent=memory.cursor_at(4294964263))\n'
                                                       "frame = _calendar_move_fields(memory, frame, 'target_y', 0)\n"
                                                       "frame = _calendar_move_fields(memory, frame, 'target_y', "
                                                       'frame.opponent.byte(low16(frame.target_x)), 1)\n'
                                                       'player = False\n'
                                                       'for address in (4294964859, 4294964861, 4294964863):\n'
                                                       '    frame = _calendar_compare_fields(memory, frame, low8(frame.target_y), '
                                                       'memory.state.read(address, 1), 1)\n'
                                                       '    if frame.status & 4:\n'
                                                       '        player = True\n'
                                                       '        break\n'
                                                       'if player:\n'
                                                       '    frame = first_replace(frame, opponent=memory.cursor_at(4294960704))\n'
                                                       "    frame = _calendar_shift_fields(memory, frame, 'target_y', 1)\n"
                                                       '    frame = _calendar_compare_fields(memory, frame, low16(frame.offset_y), '
                                                       'frame.opponent.word(low16(frame.target_y)))\n'
                                                       '    if not frame.status & 4:\n'
                                                       "        saved = ('target_x', 'target_y', 'unit', 'count', 'distance', 'offset_x', "
                                                       "'offset_y', 'choice', 'roster', 'candidates', 'controller', 'scan', 'opponent', "
                                                       "'scratch', 'auxiliary')\n"
                                                       '        frame = _calendar_save_fields(memory, frame, saved)\n'
                                                       '        frame = _calendar_push_word_fields(memory, frame, '
                                                       'memory.state.read(4294964086, 2))\n'
                                                       '        frame = _calendar_push_word_fields(memory, frame, '
                                                       'memory.state.read(4294964066, 2))\n'
                                                       '        frame = _calendar_write_fields(memory, frame, 4294964086, 0, clear=True)\n'
                                                       "        frame = _calendar_shift_fields(memory, frame, 'target_y', 1, right=True)\n"
                                                       '        frame = _calendar_write_fields(memory, frame, 4294964087, '
                                                       'low8(frame.target_y), 1)\n'
                                                       '        frame = _calendar_write_fields(memory, frame, 4294964176, '
                                                       'low16(frame.offset_y))\n'
                                                       '        frame = _calendar_write_fields(memory, frame, 4294965056, 205)\n'
                                                       '        frame = _calendar_write_fields(memory, frame, 4294964066, 0, clear=True)\n'
                                                       '        frame = _calendar_call_fields(memory, frame, 199284, 94116)\n'
                                                       '        frame = _calendar_pop_word_fields(memory, frame, 4294964066)\n'
                                                       '        frame = _calendar_pop_word_fields(memory, frame, 4294964086)\n'
                                                       '        frame = _calendar_restore_fields(memory, frame, saved)\n'
                                                       'frame = _calendar_write_fields(memory, frame, '
                                                       'frame.candidates.address(low16(frame.offset_y)), 255, 1)\n'
                                                       'frame = first_replace(frame, scan=memory.cursor_at(4294964320))\n'
                                                       "frame = _calendar_move_fields(memory, frame, 'target_y', 39)\n"
                                                       'found = False\n'
                                                       'while True:\n'
                                                       '    frame = _calendar_compare_fields(memory, frame, low16(frame.offset_y), '
                                                       'frame.scan.word())\n'
                                                       '    frame = first_replace(frame, scan=frame.scan.advance(2))\n'
                                                       '    if frame.status & 4:\n'
                                                       '        found = True\n'
                                                       '        break\n'
                                                       "    frame, again = _calendar_db_fields(frame, 'target_y')\n"
                                                       '    if not again:\n'
                                                       '        break\n'
                                                       'if found:\n'
                                                       "    frame = _calendar_move_fields(memory, frame, 'target_x', low16(frame.target_x) "
                                                       '& 255)\n'
                                                       '    frame = _calendar_call_fields(memory, frame, 94170, 94164)\n'
                                                       "return _calendar_restore_fields(memory, frame, ('scan', 'opponent'))",
                                               'returns': 'FirstDeploymentFrame',
                                               'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'scan_calendar_officer_mortality': {'flow': 'from .business_reuse import _calendar_legacy_entry_fields\n'
                                             "memory, entered = _calendar_legacy_context_fields(state, retained, 'mortality')\n"
                                             'actual = scan_calendar_officer_mortality_fields(memory, entered)\n'
                                             'return retained',
                                     'returns': 'MortalityContext',
                                     'signature': 'state: GameplayState, retained: MortalityContext=MortalityContext()'},
 'scan_calendar_officer_mortality_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 93914)\n'
                                                    'frame = first_replace(frame, roster=memory.cursor_at(4294963456), '
                                                    'candidates=memory.cursor_at(4294953984), controller=memory.cursor_at(4294961719))\n'
                                                    "frame = _calendar_move_fields(memory, frame, 'offset_y', 255)\n"
                                                    'while True:\n'
                                                    '    frame = first_replace(frame, roster=frame.roster.advance(-1))\n'
                                                    "    frame = _calendar_move_fields(memory, frame, 'offset_x', frame.roster.byte(), 1)\n"
                                                    '    frame = _calendar_compare_fields(memory, frame, low8(frame.offset_x), 255, 1)\n'
                                                    '    eligible = not frame.status & 4\n'
                                                    '    if eligible:\n'
                                                    "        frame = _calendar_move_fields(memory, frame, 'distance', "
                                                    'frame.candidates.byte(low16(frame.offset_y)), 1)\n'
                                                    '        negative = bool(frame.status & 8)\n'
                                                    '        if not negative:\n'
                                                    '            frame = _calendar_bit_fields(memory, frame, frame.distance, 64)\n'
                                                    '            eligible = bool(frame.status & 4)\n'
                                                    '            if eligible:\n'
                                                    '                frame = _calendar_test_fields(memory, frame, '
                                                    'frame.controller.byte(low16(frame.distance)), 1)\n'
                                                    '                eligible = bool(frame.status & 4)\n'
                                                    '        if eligible:\n'
                                                    '            frame = _calendar_compare_fields(memory, frame, low8(frame.distance), '
                                                    '255, 1)\n'
                                                    '            eligible = not frame.status & 4\n'
                                                    '    if eligible:\n'
                                                    "        frame = _calendar_move_fields(memory, frame, 'choice', "
                                                    'memory.state.read(4294964084, 1), 1)\n'
                                                    "        frame = _calendar_arithmetic_fields(memory, frame, 'choice', "
                                                    'low8(frame.offset_x), 1, True)\n'
                                                    '        if not frame.status & 1:\n'
                                                    "            frame = _calendar_move_fields(memory, frame, 'offset_x', 1)\n"
                                                    "            frame = _calendar_move_fields(memory, frame, 'choice', "
                                                    'low16(frame.choice) & 4)\n'
                                                    "            frame = _calendar_shift_fields(memory, frame, 'offset_x', "
                                                    'low16(frame.choice))\n'
                                                    '            frame = _calendar_call_fields(memory, frame, 33748, 93998)\n'
                                                    "            frame = _calendar_move_fields(memory, frame, 'target_x', "
                                                    'low16(frame.target_x) & 15)\n'
                                                    '            frame = _calendar_compare_fields(memory, frame, low16(frame.target_x), '
                                                    'low16(frame.offset_x))\n'
                                                    '            if frame.status & (1 | 4):\n'
                                                    '                frame = _calendar_call_fields(memory, frame, 94018, 94012)\n'
                                                    "    frame, again = _calendar_db_fields(frame, 'offset_y')\n"
                                                    '    if not again:\n'
                                                    '        return frame',
                                            'returns': 'FirstDeploymentFrame',
                                            'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'show_calendar_event_message': {'flow': 'from .business_reuse import _calendar_legacy_entry_fields\n'
                                         'memory, entered = _calendar_legacy_entry_fields(state, (message,), (), ())\n'
                                         'actual = show_calendar_event_message_fields(memory, entered)',
                                 'returns': 'None',
                                 'signature': 'state: GameplayState, message: Word'},
 'show_calendar_event_message_fields': {'flow': 'frame = _calendar_frame_fields(memory, frame, 94296)\n'
                                                "saved = ('target_x', 'target_y', 'unit', 'count', 'distance', 'offset_x', 'offset_y', "
                                                "'choice')\n"
                                                'frame = _calendar_save_fields(memory, frame, saved)\n'
                                                'frame = _calendar_write_fields(memory, frame, 4294965056, low16(frame.unit))\n'
                                                'frame = _calendar_write_fields(memory, frame, 4294964744, 128)\n'
                                                'frame = _calendar_write_fields(memory, frame, 4294964066, 0, clear=True)\n'
                                                'frame = _calendar_push_word_fields(memory, frame, memory.state.read(4294964754, 2))\n'
                                                'frame = _calendar_call_fields(memory, frame, 199284, 94324)\n'
                                                'frame = _calendar_pop_word_fields(memory, frame, 4294964754)\n'
                                                'return _calendar_restore_fields(memory, frame, saved)',
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'show_first_calendar_event_values': {'flow': 'from .business_reuse import _calendar_legacy_entry_fields\n'
                                              'memory, entered = _calendar_legacy_entry_fields(state, (owner,), (), ())\n'
                                              'actual = show_first_calendar_event_values_fields(memory, entered)',
                                      'returns': 'None',
                                      'signature': 'state: GameplayState, owner: Word'},
 'show_first_calendar_event_values_fields': {'flow': 'return _calendar_event_owner_values_fields(memory, frame, 94552, 94614, 94624, 174)',
                                             'returns': 'FirstDeploymentFrame',
                                             'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'show_second_calendar_event_values': {'flow': 'from .business_reuse import _calendar_legacy_entry_fields\n'
                                               'memory, entered = _calendar_legacy_entry_fields(state, (owner,), (), ())\n'
                                               'actual = show_second_calendar_event_values_fields(memory, entered)',
                                       'returns': 'None',
                                       'signature': 'state: GameplayState, owner: Word'},
 'show_second_calendar_event_values_fields': {'flow': 'return _calendar_event_owner_values_fields(memory, frame, 94964, 95026, 95036, 175)',
                                              'returns': 'FirstDeploymentFrame',
                                              'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'},
 'show_third_calendar_event_values': {'flow': 'from .business_reuse import _calendar_legacy_entry_fields\n'
                                              'memory, entered = _calendar_legacy_entry_fields(state, (owner,), (), ())\n'
                                              'actual = show_third_calendar_event_values_fields(memory, entered)',
                                      'returns': 'None',
                                      'signature': 'state: GameplayState, owner: Word'},
 'show_third_calendar_event_values_fields': {'flow': 'return _calendar_event_owner_values_fields(memory, frame, 95270, 95332, 95342, 179)',
                                             'returns': 'FirstDeploymentFrame',
                                             'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame'}})

DECLARATIONS.update({'show_calendar_event_message_fields': {'flow': "frame = _calendar_frame_fields(memory, frame, 94296)\nsaved = ('target_x', 'target_y', 'unit', 'count', 'distance', 'offset_x', 'offset_y', 'choice')\nframe = _calendar_save_fields(memory, frame, saved)\nframe = _calendar_write_fields(memory, frame, 4294965056, low16(frame.unit))\nframe = _calendar_write_fields(memory, frame, 4294964744, 128)\nframe = _calendar_write_fields(memory, frame, 4294964066, 0, clear=True)\nframe = _calendar_push_word_fields(memory, frame, memory.state.read(4294964754, 2))\nframe = _calendar_call_fields(memory, frame, 199284, 94324)\nframe = _calendar_pop_word_fields(memory, frame, 4294964754)\nreturn _calendar_restore_fields(memory, frame, saved)", 'returns': 'FirstDeploymentFrame', 'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame', 'slots': {128: ('message_parameter', 0, 65535)}}})

