"""Structured arrival AST -> consumed semantic effects -> ordinary GNU.

The complete supported semantic flows are explicit below. Unknown expressions,
ABI changes and incomplete control/return edits fail closed. No file reader,
sample, old assembly, opcode table, object or source-hash selector is used.
"""
from .compiler_common import CompileError, semantic_functions, lower_declared
from .target import ARRIVAL_BINDINGS

DECLARATIONS = {'hostile_adjacent_block': {'signature': 'state: GameState',
                            'returns': 'CarryOutcome',
                            'flow': 'if state.position_x() & 15 != 0:\n'
                                    '    return state.carry_result(0)\n'
                                    'if state.position_y() & 15 != 0:\n'
                                    '    return state.carry_result(0)\n'
                                    'center_x = u16(state.position_x() >> 4)\n'
                                    'left_x = u16(center_x - 1)\n'
                                    'right_x = u16(center_x + 1)\n'
                                    'center_y = u16(state.position_y() >> 4)\n'
                                    'upper_y = u16(center_y - 1)\n'
                                    'lower_y = u16(center_y + 1)\n'
                                    'packet = state.table(state.active_packet())\n'
                                    'owner = u16(packet.byte(0, 4))\n'
                                    'state.set_blocking_owner(owner)\n'
                                    'mask = state.force_masks.word(u16(owner << 1))\n'
                                    'state.set_blocking_mask(mask)\n'
                                    'groups = state.packed_groups\n'
                                    'while True:\n'
                                    '    count = u16(groups.byte() & 15)\n'
                                    '    if count == 0:\n'
                                    '        break\n'
                                    '    if groups.byte() & 32 == 0:\n'
                                    '        other_owner = u16(groups.byte(0, 4))\n'
                                    '        if low8(other_owner) != state.blocking_owner_tail():\n'
                                    '            mask = state.blocking_mask()\n'
                                    '            mask = state.effective_blocking_mask(mask)\n'
                                    '            if mask & 1 << (other_owner & 31) == 0:\n'
                                    '                if low8(left_x) == groups.byte(0, 1) and low8(center_y) '
                                    '== groups.byte(0, 2):\n'
                                    '                    return state.carry_result(1)\n'
                                    '                if low8(center_x) == groups.byte(0, 1):\n'
                                    '                    if low8(upper_y) == groups.byte(0, 2):\n'
                                    '                        return state.carry_result(1)\n'
                                    '                    if low8(lower_y) == groups.byte(0, 2):\n'
                                    '                        return state.carry_result(1)\n'
                                    '                if low8(right_x) == groups.byte(0, 1) and '
                                    'low8(center_y) == groups.byte(0, 2):\n'
                                    '                    return state.carry_result(1)\n'
                                    '    count = u16(groups.byte() & 15)\n'
                                    '    groups = groups.advance(u32(count + 13))\n'
                                    'grid = state.city_grid\n'
                                    'for city in descending_inclusive(39):\n'
                                    '    if grid.byte() != 0:\n'
                                    '        other_owner = u16(state.city_owners_reverse.byte(city))\n'
                                    '        if low8(other_owner) != state.blocking_owner_tail():\n'
                                    '            mask = state.blocking_mask()\n'
                                    '            mask = state.effective_blocking_mask(mask)\n'
                                    '            if mask & 1 << (other_owner & 31) == 0:\n'
                                    '                if low8(left_x) == grid.byte(0, 1) and low8(center_y) '
                                    '== grid.byte(0, 2):\n'
                                    '                    collect_blocked_cargo(state, grid)\n'
                                    '                    return state.carry_result(1)\n'
                                    '                if low8(center_x) == grid.byte(0, 1):\n'
                                    '                    if low8(lower_y) == grid.byte(0, 2):\n'
                                    '                        collect_blocked_cargo(state, grid)\n'
                                    '                        return state.carry_result(1)\n'
                                    '                    if low8(upper_y) == grid.byte(0, 2):\n'
                                    '                        collect_blocked_cargo(state, grid)\n'
                                    '                        return state.carry_result(1)\n'
                                    '                if low8(right_x) == grid.byte(0, 1) and low8(center_y) '
                                    '== grid.byte(0, 2):\n'
                                    '                    collect_blocked_cargo(state, grid)\n'
                                    '                    return state.carry_result(1)\n'
                                    '    grid = grid.advance(-4)\n'
                                    'return state.carry_result(0)',
                            'slots': {}},
 'collect_blocked_cargo': {'signature': 'state: GameState, obstacle: Table',
                           'returns': 'None',
                           'flow': 'obstacle = state.checked_table(obstacle)\n'
                                   'cargo = state.table(state.active_packet())\n'
                                   'kind = u16(obstacle.byte() & 3)\n'
                                   'if kind != 2:\n'
                                   '    amount = u32(cargo.byte(0, 5) << 24)\n'
                                   '    amount = u32(amount | cargo.byte(0, 6) << 16)\n'
                                   '    amount = u32(amount | cargo.byte(0, 7) << 8)\n'
                                   '    amount = u32(amount | cargo.byte(0, 8))\n'
                                   '    amount = u32(amount + 10000)\n'
                                   '    if amount > 999999:\n'
                                   '        amount = u32(999999)\n'
                                   '    cargo.set_byte(0, low8(amount), 8)\n'
                                   '    amount = u32(amount >> 8)\n'
                                   '    cargo.set_byte(0, low8(amount), 7)\n'
                                   '    amount = u32(amount >> 8)\n'
                                   '    cargo.set_byte(0, low8(amount), 6)\n'
                                   '    amount = u16(low16(amount) >> 8)\n'
                                   '    cargo.set_byte(0, low8(amount), 5)\n'
                                   '    if kind != 3:\n'
                                   '        obstacle.set_byte(0, 0)\n'
                                   '    else:\n'
                                   '        obstacle.set_byte(0, obstacle.byte() & 128)\n'
                                   '        obstacle.set_byte(0, obstacle.byte() | 2)\n'
                                   'else:\n'
                                   '    amount = u32(cargo.byte(0, 9) << 24)\n'
                                   '    amount = u32(amount | cargo.byte(0, 10) << 16)\n'
                                   '    amount = u32(amount | cargo.byte(0, 11) << 8)\n'
                                   '    amount = u32(amount | cargo.byte(0, 12))\n'
                                   '    amount = u32(amount + 10000)\n'
                                   '    if amount > 999999:\n'
                                   '        amount = u32(99999)\n'
                                   '    cargo.set_byte(0, low8(amount), 12)\n'
                                   '    amount = u32(amount >> 8)\n'
                                   '    cargo.set_byte(0, low8(amount), 11)\n'
                                   '    amount = u32(amount >> 8)\n'
                                   '    cargo.set_byte(0, low8(amount), 10)\n'
                                   '    amount = u16(low16(amount) >> 8)\n'
                                   '    cargo.set_byte(0, low8(amount), 9)\n'
                                   '    obstacle.set_byte(0, 0)',
                           'slots': {10000: ('cargo_gain', 0, 4294967295)}},
 'settle_arriving_group': {'signature': 'state: GameState, cargo_source: Table',
                           'returns': 'CarryOutcome',
                           'flow': 'cargo_source = state.checked_table(cargo_source)\n'
                                   'packet = state.table(state.active_packet())\n'
                                   'owner, city_index = locate_arrival_city(state, packet)\n'
                                   'if negative_byte(owner):\n'
                                   '    owner = u16(replace_byte(owner, packet.byte(0, 4)))\n'
                                   '    cargo_source = state.city_owners_reverse\n'
                                   '    cargo_source.set_byte(city_index, low8(owner))\n'
                                   '    initialize_arrival_loyalty(state, owner, city_index)\n'
                                   '    clear_arrival_city_order(state)\n'
                                   'elif low8(owner) != packet.byte(0, 4):\n'
                                   '    if owner == 16:\n'
                                   '        return state.carry_observed(0)\n'
                                   '    state.set_current_force(0)\n'
                                   '    state.set_current_force_tail(packet.byte(0, 4))\n'
                                   '    force = state.current_force()\n'
                                   '    if force != state.player_force_word_1():\n'
                                   '        if force != state.player_force_word_2():\n'
                                   '            if force != state.player_force_word_3():\n'
                                   '                return state.carry_result(0)\n'
                                   '    if state.city_processed.byte(state.selected_city()) & 2 != 0:\n'
                                   '        return state.carry_result(0)\n'
                                   '    state.set_command_step(12)\n'
                                   '    return state.carry_result(1)\n'
                                   'city = u16(city_index + 1)\n'
                                   'state.set_current_city(city)\n'
                                   'state.set_roster_exclusion(65535)\n'
                                   'total_count = state.build_roster(city)\n'
                                   'if total_count >= 10:\n'
                                   '    return state.carry_result(0)\n'
                                   'packet = state.table(state.active_packet())\n'
                                   'state.set_current_force_tail(packet.byte(0, 4))\n'
                                   'member_count = u16(packet.byte() & 15)\n'
                                   'total_count = u16(total_count + member_count)\n'
                                   'if total_count <= 10:\n'
                                   '    state.credit_packet(city, packet)\n'
                                   '    assign_packet_members(state, packet, city, member_count)\n'
                                   '    compact_after_packet(state, packet, member_count)\n'
                                   '    city = state.current_city()\n'
                                   '    if negative_word(state.city_heads.word(u16(city << 1))):\n'
                                   '        city = state.current_city()\n'
                                   '        state.set_roster_exclusion(65535)\n'
                                   '        state.build_roster(city)\n'
                                   '        state.choose_city_head(city)\n'
                                   '    return state.carry_result(0)\n'
                                   'owner = packet.byte(0, 4)\n'
                                   'if owner == state.player_force_1():\n'
                                   '    total_count = detach_packet_force_head(state, packet, city_index, '
                                   'total_count)\n'
                                   'elif owner == state.player_force_2():\n'
                                   '    total_count = detach_packet_force_head(state, packet, city_index, '
                                   'total_count)\n'
                                   'elif owner == state.player_force_3():\n'
                                   '    total_count = detach_packet_force_head(state, packet, city_index, '
                                   'total_count)\n'
                                   'else:\n'
                                   '    total_count = merge_overcapacity_arrival(state, packet, city_index, '
                                   'total_count)\n'
                                   '    return state.carry_result(0)\n'
                                   'state.set_current_city(owner)\n'
                                   'excess = u16(total_count - 10)\n'
                                   'remaining = u16(member_count - excess)\n'
                                   'if remaining == 0:\n'
                                   '    return state.carry_result(0)\n'
                                   'state.set_remaining_members(remaining)\n'
                                   'state.set_command_step(u16(state.command_step() + 1))\n'
                                   'return state.carry_result(1)',
                           'slots': {}},
 'assign_packet_members': {'signature': 'state: GameState, packet: Table, city: Word, count: Word',
                           'returns': 'None',
                           'flow': 'packet = state.checked_table(packet)\n'
                                   'city = uint(city, 16)\n'
                                   'count = uint(count, 16)\n'
                                   'roster = packet.at(0, 13).cursor()\n'
                                   'member = u16(0)\n'
                                   'force = u16(packet.byte(0, 4))\n'
                                   'head = state.force_heads.word(u16(force << 1))\n'
                                   'for position in descending_inclusive(u16(count - 1)):\n'
                                   '    member = u16(replace_byte(member, roster.next_byte()))\n'
                                   '    state.officer_assignments.set_byte(member, low8(city))\n'
                                   '    if low8(member) == low8(head):\n'
                                   '        member = u16(city << 1)\n'
                                   '        state.city_heads.set_word(member, head)',
                           'slots': {}},
 'compact_after_packet': {'signature': 'state: GameState, packet: Table, count: Word',
                          'returns': 'None',
                          'flow': 'packet = state.checked_table(packet)\n'
                                  'count = uint(count, 16)\n'
                                  'source = packet.at(count, 13).cursor()\n'
                                  'destination = packet.cursor()\n'
                                  'while True:\n'
                                  '    size = u16(source.byte() & 15)\n'
                                  '    if size == 0:\n'
                                  '        break\n'
                                  '    for position in descending_inclusive(u16(size + 12)):\n'
                                  '        value = source.next_byte()\n'
                                  '        destination.append_byte(value)\n'
                                  'destination.set_byte(0, 0)\n'
                                  'state.set_active_packet(0)',
                          'slots': {}},
 'initialize_arrival_loyalty': {'signature': 'state: GameState, force: Word, city_index: Word',
                                'returns': 'None',
                                'flow': 'force = uint(force, 16)\n'
                                        'city_index = uint(city_index, 16)\n'
                                        'head = state.force_heads.word(u16(force << 1))\n'
                                        'affinity = u16(state.loyalty.byte(head))\n'
                                        'sample = u32(state.sample_random())\n'
                                        'multiplier = u16(high16(u32(sample * 3)) + 6)\n'
                                        'result = divu_retained(u32(affinity * multiplier), 10)\n'
                                        'state.city_reserves.set_word(u16(city_index << 2), low16(result), '
                                        '2)',
                                'slots': {}},
 'clear_arrival_city_order': {'signature': 'state: GameState',
                              'returns': 'None',
                              'flow': 'city = u16(state.selected_city() << 2)\n'
                                      'state.selected_orders.set_long(city, 0)',
                              'slots': {}},
 'merge_overcapacity_arrival': {'signature': 'state: GameState, packet: Table, city_index: Word, '
                                             'total_count: Word',
                                'returns': 'Word',
                                'flow': 'packet = state.checked_table(packet)\n'
                                        'city_index = uint(city_index, 16)\n'
                                        'total_count = uint(total_count, 16)\n'
                                        'city = u16(city_index + 1)\n'
                                        'build_packet_member_roster(state, packet)\n'
                                        'extract_force_head_from_roster(state, packet, city)\n'
                                        'sort_packet_roster_by_status(state)\n'
                                        'excess = assign_ranked_packet_members(state, packet, city, '
                                        'total_count)\n'
                                        'state.credit_packet_wrapped(city, packet)\n'
                                        'compact_arrival_packet(state, packet)\n'
                                        'return excess',
                                'slots': {}},
 'build_packet_member_roster': {'signature': 'state: GameState, packet: Table',
                                'returns': 'None',
                                'flow': 'packet = state.checked_table(packet)\n'
                                        'roster = state.member_roster.cursor()\n'
                                        'count = u16(packet.byte() & 15)\n'
                                        'member = u16(0)\n'
                                        'for position in descending_inclusive(u16(count - 1)):\n'
                                        '    member = u16(replace_byte(member, packet.byte(position, 13)))\n'
                                        '    roster.append_word(member)\n'
                                        'roster.set_word(0, 65535)',
                                'slots': {}},
 'extract_force_head_from_roster': {'signature': 'state: GameState, packet: Table, city: Word',
                                    'returns': 'None',
                                    'flow': 'packet = state.checked_table(packet)\n'
                                            'city = uint(city, 16)\n'
                                            'force = u16(packet.byte(0, 4))\n'
                                            'head = state.force_heads.word(u16(force << 1))\n'
                                            'source = state.member_roster.cursor()\n'
                                            'ranked = state.ranked_roster.cursor()\n'
                                            'weights = state.ranked_status.cursor()\n'
                                            'while True:\n'
                                            '    member = source.next_word()\n'
                                            '    if negative_word(member):\n'
                                            '        break\n'
                                            '    if member == head:\n'
                                            '        ranked.append_word(head)\n'
                                            '        weights.append_word(100)\n'
                                            '        while True:\n'
                                            '            shifted = source.next_word()\n'
                                            '            source.set_word(u16(65532), shifted)\n'
                                            '            if negative_word(shifted):\n'
                                            '                break\n'
                                            '        state.city_heads.set_word(u16(city << 1), head)\n'
                                            '        break\n'
                                            'ranked.set_word(0, 65535)',
                                    'slots': {}},
 'sort_packet_roster_by_status': {'signature': 'state: GameState',
                                  'returns': 'None',
                                  'flow': 'source = state.member_roster.cursor()\n'
                                          'attribute = u16(0)\n'
                                          'while True:\n'
                                          '    member = source.next_word()\n'
                                          '    if negative_word(member):\n'
                                          '        break\n'
                                          '    attribute = u16(replace_byte(attribute, '
                                          'state.officer_status.byte(member)))\n'
                                          '    ranked = state.ranked_roster.cursor()\n'
                                          '    weights = state.ranked_status.cursor()\n'
                                          '    while not negative_word(ranked.word()):\n'
                                          '        if attribute > weights.word():\n'
                                          '            break\n'
                                          '        ranked = ranked.advance(2)\n'
                                          '        weights = weights.advance(2)\n'
                                          '    while True:\n'
                                          '        old_member = ranked.word()\n'
                                          '        old_attribute = weights.word()\n'
                                          '        ranked.append_word(member)\n'
                                          '        weights.append_word(attribute)\n'
                                          '        member = old_member\n'
                                          '        if negative_word(member):\n'
                                          '            break\n'
                                          '        attribute = old_attribute\n'
                                          '    ranked.set_word(0, 65535)',
                                  'slots': {}},
 'assign_ranked_packet_members': {'signature': 'state: GameState, packet: Table, city: Word, total_count: '
                                               'Word',
                                  'returns': 'Word',
                                  'flow': 'packet = state.checked_table(packet)\n'
                                          'city = uint(city, 16)\n'
                                          'total_count = uint(total_count, 16)\n'
                                          'count = u16(packet.byte() & 15)\n'
                                          'excess = u16(total_count - 9)\n'
                                          'available = u16(count - excess)\n'
                                          'roster = state.ranked_roster.cursor()\n'
                                          'for position in descending_inclusive(available):\n'
                                          '    member = roster.next_word()\n'
                                          '    state.officer_assignments.set_byte(member, low8(city))\n'
                                          'city = u16(city | 128)\n'
                                          'while True:\n'
                                          '    member = roster.next_word()\n'
                                          '    if negative_word(member):\n'
                                          '        break\n'
                                          '    state.officer_assignments.set_byte(member, low8(city))\n'
                                          'city = u16(city & 65407)\n'
                                          'return excess',
                                  'slots': {}},
 'compact_arrival_packet': {'signature': 'state: GameState, packet: Table',
                            'returns': 'None',
                            'flow': 'packet = state.checked_table(packet)\n'
                                    'count = u16(packet.byte() & 15)\n'
                                    'source = packet.at(count, 13).cursor()\n'
                                    'destination = packet.cursor()\n'
                                    'while True:\n'
                                    '    size = u16(source.byte() & 15)\n'
                                    '    if size == 0:\n'
                                    '        break\n'
                                    '    for position in descending_inclusive(u16(size + 12)):\n'
                                    '        value = source.next_byte()\n'
                                    '        destination.append_byte(value)\n'
                                    'destination.set_byte(0, 0)\n'
                                    'state.set_active_packet(0)',
                            'slots': {}},
 'detach_packet_force_head': {'signature': 'state: GameState, packet: Table, city_index: Word, total_count: '
                                           'Word',
                              'returns': 'Word',
                              'flow': 'packet = state.checked_table(packet)\n'
                                      'city_index = uint(city_index, 16)\n'
                                      'total_count = uint(total_count, 16)\n'
                                      'last = u16((packet.byte() & 15) - 1)\n'
                                      'force = u16(packet.byte(0, 4))\n'
                                      'head = state.force_heads.word(u16(force << 1))\n'
                                      'index = u16(0)\n'
                                      'while True:\n'
                                      '    if low8(head) == packet.byte(index, 13):\n'
                                      '        break\n'
                                      '    index = u16(index + 1)\n'
                                      '    if index >= last:\n'
                                      '        return total_count\n'
                                      'index = u16(index + 1)\n'
                                      'while index < last:\n'
                                      '    value = packet.byte(index, 13)\n'
                                      '    packet.set_byte(index, value, 12)\n'
                                      '    index = u16(index + 1)\n'
                                      'while True:\n'
                                      '    size = u16(packet.byte(index, 13) & 15)\n'
                                      '    if size == 0:\n'
                                      '        break\n'
                                      '    for position in descending_inclusive(u16(size + 12)):\n'
                                      '        value = packet.byte(index, 13)\n'
                                      '        packet.set_byte(index, value, 12)\n'
                                      '        index = u16(index + 1)\n'
                                      'packet.set_byte(index, 0, 12)\n'
                                      'packet.set_byte(0, u8(packet.byte() - 1))\n'
                                      'city = u16(replace_byte(index, low8(city_index)))\n'
                                      'city = u16(city + 1)\n'
                                      'state.officer_assignments.set_byte(head, low8(city))\n'
                                      'state.city_heads.set_word(u16(city << 1), head)\n'
                                      'return u16(total_count + 1)',
                              'slots': {}},
 'locate_arrival_city': {'signature': 'state: GameState, packet: Table',
                         'returns': 'tuple[Word, Word]',
                         'flow': 'packet = state.checked_table(packet)\n'
                                 'vertical = u16(packet.byte(0, 2) << 4)\n'
                                 'horizontal = u16(packet.byte(0, 1) << 4)\n'
                                 'coordinates = state.following_city_coordinates.cursor()\n'
                                 'city = u16(0)\n'
                                 'state.set_selected_city(1)\n'
                                 'for remaining in descending_inclusive(39):\n'
                                 '    first = coordinates.next_word()\n'
                                 '    second = coordinates.next_word()\n'
                                 '    if horizontal == u16(second - 24):\n'
                                 '        if vertical == first or vertical == u16(first - 16):\n'
                                 '            return (u16(state.city_owners_reverse.byte(city)), city)\n'
                                 '    if horizontal == u16(second - 8):\n'
                                 '        if vertical == u16(first + 16) or vertical == first:\n'
                                 '            return (u16(state.city_owners_reverse.byte(city)), city)\n'
                                 '        if u16(first - 16) == first:\n'
                                 '            return (u16(state.city_owners_reverse.byte(city)), city)\n'
                                 '        if vertical == u16(first - 32):\n'
                                 '            return (u16(state.city_owners_reverse.byte(city)), city)\n'
                                 '    if horizontal == u16(second + 8):\n'
                                 '        if vertical == first or vertical == u16(first - 16):\n'
                                 '            return (u16(state.city_owners_reverse.byte(city)), city)\n'
                                 '    city = u16(city + 1)\n'
                                 '    state.set_selected_city(u16(state.selected_city() + 1))\n'
                                 'return (u16(16), city)',
                         'slots': {}}}
APPROVED = {'domain': {'GameState','Table','Word','CarryOutcome','uint','u8','u16','u32',
  'low8','low16','high16','replace_byte','negative_byte','negative_word',
  'descending_inclusive','divu_retained'}}


def hostile(e,r):
    i=e.ins;clear=e.fresh('clear');blocked=e.fresh('blocked');packet_blocked=e.fresh('packet_blocked');finish=e.fresh('finish')
    loop=e.fresh('packets');skip=e.fresh('skip');cities=e.fresh('cities');cityloop=e.fresh('city_loop');cityskip=e.fresh('city_skip')
    next_middle=e.fresh('next_middle');next_right=e.fresh('next_right');citymiddle=e.fresh('city_middle');cityright=e.fresh('city_right')
    i('move.w','0xff3bb6:l,%d0',6);i('andi.w','#15,%d0',4);i('bne.w',clear,4)
    i('move.w','0xff3bb8:l,%d1',6);i('andi.w','#15,%d1',4);i('bne.w',clear,4)
    i('move.w','0xff3bb6:l,%d0',6);i('lsr.w','#4,%d0');i('move.w','%d0,%d1');i('subq.w','#1,%d1');i('move.w','%d0,%d2');i('addq.w','#1,%d2')
    i('move.w','0xff3bb8:l,%d3',6);i('lsr.w','#4,%d3');i('move.w','%d3,%d4');i('subq.w','#1,%d4');i('move.w','%d3,%d5');i('addq.w','#1,%d5')
    i('lea.l','0xe710:w,%a0',4);i('movea.l','0xff382c:l,%a2',6);i('clr.w','%d6');i('move.b','4(%a2),%d6',4)
    i('move.w','%d6,0xff3bbe:l',6);i('lsl.w','#1,%d6');i('move.w','(%a0,%d6.w),%d6',4);i('move.w','%d6,0xff3bc0:l',6)
    i('lea.l','0x9000:w,%a0',4);e.label(loop);i('move.b','(%a0),%d7');i('andi.w','#15,%d7',4);i('beq.w',cities,4)
    i('btst.b','#5,(%a0)',4);i('bne.w',skip,4);i('clr.w','%d7');i('move.b','4(%a0),%d7',4)
    i('cmp.b','0xff3bbf:l,%d7',6);i('beq.b',skip);i('move.w','0xff3bc0:l,%d6',6);i('btst.l','%d7,%d6');i('bne.b',skip)
    i('cmp.b','1(%a0),%d1',4);i('bne.b',next_middle);i('cmp.b','2(%a0),%d3',4);i('beq.w',packet_blocked,4)
    e.label(next_middle);i('cmp.b','1(%a0),%d0',4);i('bne.b',next_right);i('cmp.b','2(%a0),%d4',4);i('beq.w',packet_blocked,4);i('cmp.b','2(%a0),%d5',4);i('beq.w',packet_blocked,4)
    e.label(next_right);i('cmp.b','1(%a0),%d2',4);i('bne.b',skip);i('cmp.b','2(%a0),%d3',4);i('beq.w',packet_blocked,4)
    e.label(skip);i('move.b','(%a0),%d7');i('andi.w','#15,%d7',4);i('lea.l','13(%a0,%d7.w),%a0',4);i('bra.b',loop)
    e.label(cities);i('lea.l','0xce9c:w,%a0',4);i('lea.l','0xf428:w,%a1',4);i('swap','%d0');i('move.w','#39,%d0',4)
    e.label(cityloop);i('tst.b','(%a0)');i('beq.w',cityskip,4);i('clr.w','%d7');i('move.b','(%a1,%d0.w),%d7',4)
    i('cmp.b','0xff3bbf:l,%d7',6);i('beq.b',cityskip);i('move.w','0xff3bc0:l,%d6',6);i('btst.l','%d7,%d6');i('bne.b',cityskip)
    i('swap','%d0');i('cmp.b','1(%a0),%d1',4);i('bne.b',citymiddle);i('cmp.b','2(%a0),%d3',4);i('beq.b',blocked)
    e.label(citymiddle);i('cmp.b','1(%a0),%d0',4);i('bne.b',cityright);i('cmp.b','2(%a0),%d5',4);i('beq.w',blocked,4);i('cmp.b','2(%a0),%d4',4);i('beq.w',blocked,4)
    e.label(cityright);i('cmp.b','1(%a0),%d2',4);restore=e.fresh('restore_center');i('bne.b',restore);i('cmp.b','2(%a0),%d3',4);i('beq.w',blocked,4)
    e.label(restore);i('swap','%d0');e.label(cityskip);i('subq.w','#4,%a0');i('dbra','%d0,'+cityloop,4);i('bra.w',clear,4)
    e.label(blocked);i('bsr.w','collect_blocked_cargo',4);e.label(packet_blocked);i('ori.w','#1,%sr',4);i('bra.b',finish)
    e.label(clear);i('andi.w','#0xfffe,%sr',4);e.label(finish)


def cargo(e,r):
    i=e.ins;rice=e.fresh('rice');gold_store=e.fresh('gold_store');gold_clear=e.fresh('gold_clear');ret=e.fresh('done');kind_three=e.fresh('kind_three');rice_store=e.fresh('rice_store')
    gain=r['cargo_gain']
    i('movea.l','0xff382c:l,%a1',6);i('move.b','(%a0),%d0');i('andi.w','#3,%d0',4);i('cmpi.b','#2,%d0',4);i('beq.b',rice)
    i('move.b','5(%a1),%d1',4);i('lsl.w','#8,%d1');i('move.b','6(%a1),%d1',4);i('lsl.l','#8,%d1');i('move.b','7(%a1),%d1',4);i('lsl.l','#8,%d1');i('move.b','8(%a1),%d1',4)
    i('addi.l','#'+str(gain)+',%d1',6);i('cmpi.l','#999999,%d1',6);i('bls.b',gold_store);i('move.l','#999999,%d1',6)
    e.label(gold_store);i('move.b','%d1,8(%a1)',4);i('lsr.l','#8,%d1');i('move.b','%d1,7(%a1)',4);i('lsr.l','#8,%d1');i('move.b','%d1,6(%a1)',4);i('lsr.w','#8,%d1');i('move.b','%d1,5(%a1)',4)
    i('cmpi.b','#3,%d0',4);i('beq.b',kind_three);e.label(gold_clear);i('clr.b','(%a0)');i('bra.b',ret)
    e.label(kind_three);i('andi.b','#128,(%a0)',4);i('ori.b','#2,(%a0)',4);i('bra.b',ret)
    e.label(rice);i('move.b','9(%a1),%d1',4);i('lsl.w','#8,%d1');i('move.b','10(%a1),%d1',4);i('lsl.l','#8,%d1');i('move.b','11(%a1),%d1',4);i('lsl.l','#8,%d1');i('move.b','12(%a1),%d1',4)
    i('addi.l','#'+str(gain)+',%d1',6);i('cmpi.l','#999999,%d1',6);i('bls.b',rice_store);i('move.l','#99999,%d1',6)
    e.label(rice_store);i('move.b','%d1,12(%a1)',4);i('lsr.l','#8,%d1');i('move.b','%d1,11(%a1)',4);i('lsr.l','#8,%d1');i('move.b','%d1,10(%a1)',4);i('lsr.w','#8,%d1');i('move.b','%d1,9(%a1)',4);i('clr.b','(%a0)');e.label(ret)


def arriving(e,r):
    i=e.ins;owned=e.fresh('owned');common=e.fresh('common');foreign=e.fresh('foreign');player=e.fresh('player');partial=e.fresh('partial');clear=e.fresh('clear');merge=e.fresh('merge');done=e.fresh('done');head_ok=e.fresh('head_ok')
    i('movea.l','0xff382c:l,%a1',6);i('bsr.w','locate_arrival_city',4);i('tst.b','%d0');i('bpl.w',owned,4)
    i('move.b','4(%a1),%d0',4);i('lea.l','0xf428:w,%a0',4);i('move.b','%d0,(%a0,%d4.w)',4)
    i('bsr.w','initialize_arrival_loyalty',4);i('bsr.w','clear_arrival_city_order',4);i('bra.w',common,4)
    e.label(owned);i('cmp.b','4(%a1),%d0',4);i('bne.w',foreign,4)
    e.label(common);i('move.w','%d4,%d0');i('move.w','%d4,-(%a7)');i('addq.w','#1,%d0');i('move.w','%d0,0xf364:w',4);i('move.w','#0xffff,0xf630:w',6)
    i('jsr','build_roster:l',6);i('move.w','(%a7)+,%d4');i('cmpi.w','#10,%d3',4);i('bcc.w',clear,4)
    i('movea.l','0xff382c:l,%a0',6);i('move.b','4(%a0),0xf377:w',6);i('move.b','(%a0),%d1');i('andi.w','#15,%d1',4);i('add.w','%d1,%d3');i('cmpi.w','#10,%d3',4);i('bhi.w',partial,4)
    i('bsr.w','add_packet_city_resources',4);i('bsr.w','assign_packet_members',4);i('bsr.w','compact_after_packet',4)
    i('lea.l','0xf45e:w,%a0',4);i('move.w','0xf364:w,%d0',4);i('lsl.w','#1,%d0');i('tst.w','(%a0,%d0.w)',4);i('bpl.w',clear,4)
    i('move.w','0xf364:w,%d0',4);i('move.w','#0xffff,0xf630:w',6);i('jsr','build_roster:l',6);i('jsr','choose_city_head:l',6);i('bra.w',clear,4)
    e.label(partial);i('move.b','4(%a0),%d0',4);i('cmp.b','0xf67b:w,%d0',4);i('beq.w',player,4);i('cmp.b','0xf67d:w,%d0',4);i('beq.w',player,4);i('cmp.b','0xf67f:w,%d0',4);i('bne.w',merge,4)
    e.label(player);i('bsr.w','detach_packet_force_head',4);i('move.w','%d0,0xf364:w',4);i('subi.w','#10,%d3',4);i('sub.w','%d3,%d1');i('beq.w',clear,4)
    i('move.w','%d1,0xf686:w',4);i('addq.w','#1,0xf362:w',4);i('ori.w','#1,%sr',4);i('bra.w',done,4)
    e.label(clear);i('andi.w','#0xfffe,%sr',4);i('bra.w',done,4)
    e.label(merge);i('bsr.w','merge_overcapacity_arrival',4);i('andi.w','#0xfffe,%sr',4);i('bra.w',done,4)
    e.label(foreign);i('cmpi.w','#16,%d0',4);i('beq.w',done,4);i('clr.w','0xf376:w',4);i('move.b','4(%a1),0xf377:w',6)
    i('move.w','0xf376:w,%d0',4);i('cmp.w','0xf67a:w,%d0',4);gate=e.fresh('processed');i('beq.w',gate,4);i('cmp.w','0xf67c:w,%d0',4);i('beq.w',gate,4);i('cmp.w','0xf67e:w,%d0',4);i('bne.b',clear)
    e.label(gate);i('lea.l','0xea37:w,%a1',4);i('move.w','0xf392:w,%d0',4);i('btst.b','#1,(%a1,%d0.w)',6);i('bne.b',clear);i('move.w','#12,0xf362:w',6);i('ori.w','#1,%sr',4);e.label(done)


def assign_members(e,r):
    i=e.ins;loop=e.fresh('member');skip=e.fresh('not_head')
    i('lea.l','0xcc00:w,%a1',4);i('lea.l','(%a0),%a3');i('adda.w','#13,%a3',4);i('move.w','%d1,%d3');i('subq.w','#1,%d3');i('clr.w','%d2');i('clr.w','%d4');i('move.b','4(%a0),%d4',4);i('lsl.w','#1,%d4')
    i('lea.l','0xe640:w,%a2',4);i('move.w','(%a2,%d4.w),%d4',4);i('lea.l','0xf45e:w,%a2',4)
    e.label(loop);i('move.b','(%a3)+,%d2');i('move.b','%d0,(%a1,%d2.w)',4);i('cmp.b','%d2,%d4');i('bne.b',skip);i('move.w','%d0,%d2');i('lsl.w','#1,%d2');i('move.w','%d4,(%a2,%d2.w)',4)
    e.label(skip);i('dbra','%d3,'+loop,4)


def compact(e,r):
    i=e.ins;loop=e.fresh('record');copy=e.fresh('copy');done=e.fresh('terminator')
    if r.get('from_header',False):
        i('move.b','(%a0),%d0');i('andi.w','#15,%d0',4);i('lea.l','13(%a0,%d0.w),%a1',4)
    else:i('lea.l','13(%a0,%d1.w),%a1',4)
    e.label(loop);i('move.b','(%a1),%d0');i('andi.w','#15,%d0',4);i('beq.w' if r.get('from_header',False) else 'beq.b',done,4 if r.get('from_header',False) else 2)
    i('addi.w','#12,%d0',4);e.label(copy);i('move.b','(%a1)+,(%a0)+');i('dbra','%d0,'+copy,4);i('bra.b',loop)
    e.label(done);i('clr.b','(%a0)');i('clr.l','0xff382c:l',6)


def loyalty(e,r):
    i=e.ins;i('movem.l','%d0-%d2/%d4/%a0,-(%a7)',4);i('lea.l','0xe640:w,%a0',4);i('lsl.w','#1,%d0');i('move.w','(%a0,%d0.w),%d0',4);i('lea.l','0xc200:w,%a0',4);i('clr.w','%d2');i('move.b','(%a0,%d0.w),%d2',4)
    i('jsr','step_random:l',6);i('andi.l','#0xffff,%d0',6);i('move.l','%d0,%d1');i('lsl.l','#1,%d0');i('add.l','%d1,%d0');i('swap','%d0');i('addi.w','#6,%d0',4);i('mulu.w','%d0,%d2');i('divu.w','#10,%d2',4)
    i('lea.l','0xe320:w,%a0',4);i('lsl.w','#2,%d4');i('move.w','%d2,2(%a0,%d4.w)',4);i('movem.l','(%a7)+,%d0-%d2/%d4/%a0',4)


def clear_order(e,r):
    i=e.ins;i('movem.l','%d0/%a0,-(%a7)',4);i('lea.l','0xe774:w,%a0',4);i('move.w','0xf392:w,%d0',4);i('lsl.w','#2,%d0');i('clr.l','(%a0,%d0.w)',4);i('movem.l','(%a7)+,%d0/%a0',4)


def merge(e,r):
    e.ins('addq.w','#1,%d4')
    for name in ('build_packet_member_roster','extract_force_head_from_roster','sort_packet_roster_by_status','assign_ranked_packet_members','add_packet_city_resources_wrapped','compact_arrival_packet'):e.ins('bsr.w',name,4)


def packet_roster(e,r):
    i=e.ins;loop=e.fresh('roster');i('lea.l','0xd300:w,%a1',4);i('move.b','(%a0),%d0');i('andi.w','#15,%d0',4);i('move.w','%d0,%d1');i('subq.w','#1,%d1');i('clr.w','%d2')
    e.label(loop);i('move.b','13(%a0,%d1.w),%d2',4);i('move.w','%d2,(%a1)+');i('dbra','%d1,'+loop,4);i('move.w','#0xffff,(%a1)',4)


def extract_head(e,r):
    i=e.ins;loop=e.fresh('search');shift=e.fresh('shift');done=e.fresh('sentinel')
    i('clr.w','%d1');i('move.b','4(%a0),%d1',4);i('lsl.w','#1,%d1');i('lea.l','0xe640:w,%a1',4);i('move.w','(%a1,%d1.w),%d1',4);i('lea.l','0xd300:w,%a1',4);i('lea.l','0xd316:w,%a2',4);i('lea.l','0xd32c:w,%a3',4)
    e.label(loop);i('move.w','(%a1)+,%d2');i('bmi.w',done,4);i('cmp.w','%d1,%d2');i('bne.b',loop);i('move.w','%d1,(%a2)+');i('move.w','#100,(%a3)+',4)
    e.label(shift);i('move.w','(%a1)+,-4(%a1)',4);i('bpl.b',shift);i('move.w','%d4,%d2');i('lsl.w','#1,%d2');i('lea.l','0xf45e:w,%a1',4);i('move.w','%d1,(%a1,%d2.w)',4)
    e.label(done);i('move.w','#0xffff,(%a2)',4)


def sort_roster(e,r):
    i=e.ins;loop=e.fresh('members');scan=e.fresh('insertion');insert=e.fresh('insert');shift=e.fresh('shift');term=e.fresh('sentinel');done=e.fresh('done')
    i('lea.l','0xd300:w,%a1',4);i('lea.l','0xc300:w,%a4',4);i('clr.w','%d2');e.label(loop);i('move.w','(%a1)+,%d1');i('bmi.w',done,4);i('move.b','(%a4,%d1.w),%d2',4);i('lea.l','0xd316:w,%a2',4);i('lea.l','0xd32c:w,%a3',4)
    e.label(scan);i('tst.w','(%a2)');i('bmi.w',insert,4);i('cmp.w','(%a3),%d2');i('bhi.w',insert,4);i('addq.w','#2,%a2');i('addq.w','#2,%a3');i('bra.b',scan)
    e.label(insert);e.label(shift);i('move.w','(%a2),%d5');i('move.w','(%a3),%d6');i('move.w','%d1,(%a2)+');i('move.w','%d2,(%a3)+');i('move.w','%d5,%d1');i('bmi.w',term,4);i('move.w','%d6,%d2');i('bra.b',shift)
    e.label(term);i('move.w','#0xffff,(%a2)',4);i('bra.b',loop);e.label(done)


def ranked_assign(e,r):
    i=e.ins;accepted=e.fresh('accepted');rest=e.fresh('temporary');done=e.fresh('done')
    i('move.b','(%a0),%d0');i('andi.w','#15,%d0',4);i('subi.w','#9,%d3',4);i('sub.w','%d3,%d0');i('lea.l','0xd316:w,%a1',4);i('lea.l','0xcc00:w,%a2',4)
    e.label(accepted);i('move.w','(%a1)+,%d1');i('move.b','%d4,(%a2,%d1.w)',4);i('dbra','%d0,'+accepted,4);i('bset.l','#7,%d4',4)
    e.label(rest);i('move.w','(%a1)+,%d1');i('bmi.w',done,4);i('move.b','%d4,(%a2,%d1.w)',4);i('bra.b',rest);e.label(done);i('bclr.l','#7,%d4',4)


def detach(e,r):
    i=e.ins;scan=e.fresh('search');found=e.fresh('found');shift=e.fresh('shift');records=e.fresh('records');copy=e.fresh('copy');end=e.fresh('terminator');done=e.fresh('restore')
    i('movem.l','%d0-%d2/%a1,-(%a7)',4);i('move.b','(%a0),%d0');i('andi.w','#15,%d0',4);i('subq.w','#1,%d0');i('clr.w','%d1');i('move.b','4(%a0),%d1',4);i('lsl.w','#1,%d1');i('lea.l','0xe640:w,%a1',4);i('move.w','(%a1,%d1.w),%d1',4);i('clr.w','%d2')
    e.label(scan);i('cmp.b','13(%a0,%d2.w),%d1',4);i('beq.w',found,4);i('addq.w','#1,%d2');i('cmp.w','%d0,%d2');i('bcs.b',scan);i('bra.w',done,4)
    e.label(shift);i('move.b','13(%a0,%d2.w),12(%a0,%d2.w)',6);e.label(found);i('addq.w','#1,%d2');i('cmp.w','%d0,%d2');i('bcs.b',shift)
    e.label(records);i('move.b','13(%a0,%d2.w),%d0',4);i('andi.w','#15,%d0',4);i('beq.w',end,4);i('addi.w','#12,%d0',4)
    e.label(copy);i('move.b','13(%a0,%d2.w),12(%a0,%d2.w)',6);i('addq.w','#1,%d2');i('dbra','%d0,'+copy,4);i('bra.b',records)
    e.label(end);i('clr.b','12(%a0,%d2.w)',4);i('subq.b','#1,(%a0)');i('lea.l','0xcc00:w,%a1',4);i('move.b','%d4,%d2');i('addq.w','#1,%d2');i('move.b','%d2,(%a1,%d1.w)',4);i('lsl.w','#1,%d2');i('lea.l','0xf45e:w,%a1',4);i('move.w','%d1,(%a1,%d2.w)',4);i('addq.w','#1,%d3')
    e.label(done);i('movem.l','(%a7)+,%d0-%d2/%a1',4)


def locate(e,r):
    i=e.ins;loop=e.fresh('cities');second=e.fresh('second_band');third=e.fresh('third_band');next_city=e.fresh('next_city');found=e.fresh('found');done=e.fresh('done')
    i('clr.w','%d0');i('move.b','2(%a1),%d0',4);i('lsl.w','#4,%d0');i('clr.w','%d1');i('move.b','1(%a1),%d1',4);i('lsl.w','#4,%d1');i('lea.l','0xd4aca:l,%a2',6);i('lea.l','0xf428:w,%a3',4);i('move.w','#39,%d3',4);i('clr.w','%d4');i('move.w','#1,0xf392:w',6)
    e.label(loop);i('move.w','(%a2)+,%d5');i('move.w','(%a2)+,%d6');i('move.w','%d6,%d7');i('subi.w','#24,%d7',4);i('cmp.w','%d7,%d1');i('bne.b',second);i('move.w','%d5,%d7');i('cmp.w','%d7,%d0');i('beq.w',found,4);i('subi.w','#16,%d7',4);i('cmp.w','%d7,%d0');i('beq.w',found,4)
    e.label(second);i('move.w','%d6,%d7');i('subi.w','#8,%d7',4);i('cmp.w','%d7,%d1');i('bne.w',third,4);i('move.w','%d5,%d7');i('addi.w','#16,%d7',4);i('cmp.w','%d7,%d0');i('beq.w',found,4);i('cmp.w','%d5,%d0');i('beq.w',found,4);i('move.w','%d5,%d7');i('subi.w','#16,%d7',4);i('cmp.w','%d5,%d7');i('beq.w',found,4);i('move.w','%d5,%d7');i('subi.w','#32,%d7',4);i('cmp.w','%d7,%d0');i('beq.w',found,4)
    e.label(third);i('move.w','%d6,%d7');i('addi.w','#8,%d7',4);i('cmp.w','%d7,%d1');i('bne.w',next_city,4);i('move.w','%d5,%d7');i('cmp.w','%d7,%d0');i('beq.b',found);i('subi.w','#16,%d7',4);i('cmp.w','%d7,%d0');i('beq.w',found,4)
    e.label(next_city);i('addq.w','#1,%d4');i('addq.w','#1,0xf392:w',4);i('dbra','%d3,'+loop,4);i('move.w','#16,%d0',4);i('bra.b',done)
    e.label(found);i('lea.l','0xf428:w,%a2',4);i('clr.w','%d0');i('move.b','(%a2,%d4.w),%d0',4);e.label(done)


LOWERERS={'hostile_adjacent_block':hostile,'collect_blocked_cargo':cargo,'settle_arriving_group':arriving,
 'assign_packet_members':assign_members,'compact_after_packet':compact,'initialize_arrival_loyalty':loyalty,
 'clear_arrival_city_order':clear_order,'merge_overcapacity_arrival':merge,'build_packet_member_roster':packet_roster,
 'extract_force_head_from_roster':extract_head,'sort_packet_roster_by_status':sort_roster,
 'assign_ranked_packet_members':ranked_assign,'compact_arrival_packet':lambda e,r:compact(e,dict(r,from_header=True)),
 'detach_packet_force_head':detach,'locate_arrival_city':locate}

def _complete_locate_record(complete_city_source):
    """Admit the actual complete Frame owner, not the same-byte scalar facade."""
    if type(complete_city_source) is not str:
        raise CompileError('arrival locating requires explicit complete Scene city source')
    from ..high_level_remaining_flows import compiler_city
    records = compiler_city.semantic_functions(complete_city_source,
        compiler_city.DECLARATIONS, compiler_city.APPROVED)
    name = 'locate_arrival_city_frame_fields'
    declaration = compiler_city.DECLARATIONS.get(name)
    if (declaration is None or declaration['signature'] !=
            'state: SceneState, frame: FirstDeploymentFrame'
            or declaration['returns'] != 'FirstDeploymentFrame'
            or declaration.get('slots', {}) != {} or name not in records
            or records[name]['rules']):
        raise CompileError('exact complete fixed-ABI locate Scene rule without slots required')
    bindings = [binding for binding in ARRIVAL_BINDINGS if binding.name == 'locate_arrival_city']
    if len(bindings) != 1 or (bindings[0].entry, bindings[0].end) != (0x164D4, 0x16588):
        raise CompileError('the complete 180-byte locate physical allocation is required')
    return records[name]


def compile_arrival(source, *, complete_city_source):
    """Admit every scalar ABI, deriving locate effects from its whole Frame."""
    records=semantic_functions(source,DECLARATIONS,APPROVED)
    complete = _complete_locate_record(complete_city_source)
    scalar = records['locate_arrival_city']
    records['locate_arrival_city'] = dict(scalar, rules=complete['rules'], effects=dict(
        actual_scene_algorithm='locate_arrival_city_frame_fields',
        actual_scene_source='tools/high_level_remaining_flows/business_city.py',
        complete_current_Frame_effects=complete['effects'],
        scalar_facade_admitted_without_scalar_lowering=True,
        admitted_scalar_effects=scalar['effects']))
    return lower_declared(records,ARRIVAL_BINDINGS,LOWERERS)
