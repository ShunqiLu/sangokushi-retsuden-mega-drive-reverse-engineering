"""Structured arrival AST -> consumed semantic effects -> ordinary GNU.

The complete supported semantic flows are explicit below. Unknown expressions,
ABI changes and incomplete control/return edits fail closed. No file reader,
sample, old assembly, opcode table, object or source-hash selector is used.
"""
from .compiler_common import semantic_functions, lower_declared
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

def compile_arrival(source):
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    complete_fields = {name: records[name]['effects'] for name in ('_arrival_frame_fields', '_arrival_store_fields', '_arrival_add_fields', '_arrival_db_fields', '_arrival_bit_fields', '_arrival_carry_fields', '_arrival_memory_increment_fields', '_arrival_swap_fields', '_arrival_call_fields', '_arrival_adjacent_position_fields', 'hostile_adjacent_block_fields', 'collect_blocked_cargo_fields', 'settle_arriving_group_fields', '_arrival_credit_resources_fields', 'add_packet_city_resources_fields', 'add_packet_city_resources_wrapped_fields', 'assign_packet_members_fields', '_arrival_compact_packet_tail_fields', 'compact_after_packet_fields', 'initialize_arrival_loyalty_fields', 'clear_arrival_city_order_fields', 'merge_overcapacity_arrival_fields', 'build_packet_member_roster_fields', 'extract_force_head_from_roster_fields', 'sort_packet_roster_by_status_fields', 'assign_ranked_packet_members_fields', 'compact_arrival_packet_fields', 'detach_packet_force_head_fields', '_arrival_match_coordinate_fields', 'locate_arrival_city_fields')}
    for binding in ARRIVAL_BINDINGS:
        records[binding.name]['effects'] = dict(historical_scalar=records[binding.name]['effects'], sole_complete_arrival_fields=complete_fields, actual_complete_entry=records[binding.name + '_fields']['effects'])
    ordinary = {binding.name: records[binding.name] for binding in ARRIVAL_BINDINGS}
    return lower_declared(ordinary, ARRIVAL_BINDINGS, LOWERERS)


# Source149: complete live arrival fields, all admitted before original lowering.
DECLARATIONS.update({'_arrival_frame_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _movement_frame(state, frame)\nstate.sr = state.sr & 65504 | frame.status\nreturn frame'}, '_arrival_store_fields': {'signature': 'state, frame, address, value, width=2, clear=False', 'returns': 'FirstDeploymentFrame', 'flow': 'if clear:\n    state.read(address, width)\nstate.write(address, width, value)\nif width == 4:\n    return _movement_test_long(state, frame, value)\nreturn _movement_test(state, frame, value, width * 8)'}, '_arrival_add_fields': {'signature': 'state, frame, carrier, value, subtract=False', 'returns': 'FirstDeploymentFrame', 'flow': 'frame, result = _movement_binary_flags(state, frame, low16(frame.carrier(carrier)), value, 16, subtract)\nreturn first_replace(frame, **{carrier: frame.carrier(carrier) & 4294901760 | result})'}, '_arrival_db_fields': {'signature': 'frame, carrier', 'returns': 'tuple', 'flow': 'remaining = u16(low16(frame.carrier(carrier)) - 1)\nreturn (first_replace(frame, **{carrier: frame.carrier(carrier) & 4294901760 | remaining}), remaining != 65535)'}, '_arrival_bit_fields': {'signature': 'state, frame, value, bit', 'returns': 'FirstDeploymentFrame', 'flow': 'status = frame.status & 27 | (4 if not value & 1 << (bit & 31) else 0)\nstate.sr = state.sr & 65504 | status\nreturn first_replace(frame, status=status)'}, '_arrival_carry_fields': {'signature': 'state, frame, carry', 'returns': 'FirstDeploymentFrame', 'flow': '_order_full_sr_carry(state, carry)\nreturn first_replace(frame, status=state.sr & 31)'}, '_arrival_memory_increment_fields': {'signature': 'state, frame, address', 'returns': 'FirstDeploymentFrame', 'flow': 'prior = state.read(address, 2)\nframe, value = _movement_mutation_flags(state, frame, prior, 1, 16)\nstate.write(address, 2, value)\nreturn frame'}, '_arrival_swap_fields': {'signature': 'state, frame, carrier', 'returns': 'FirstDeploymentFrame', 'flow': 'value = frame.carrier(carrier)\nreturn _movement_move_long(state, frame, carrier, u32(value << 16 | value >> 16))'}, '_arrival_call_fields': {'signature': 'state, frame, target, continuation', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _arrival_frame_fields(state, frame)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, uint(continuation, 32))\nentered = first_replace(frame, stack_cursor=stack)\nchildren = {87240: collect_blocked_cargo_fields, 87410: settle_arriving_group_fields, 87728: add_packet_city_resources_fields, 87836: assign_packet_members_fields, 87896: compact_after_packet_fields, 87930: initialize_arrival_loyalty_fields, 88000: clear_arrival_city_order_fields, 88024: merge_overcapacity_arrival_fields, 88052: build_packet_member_roster_fields, 88084: extract_force_head_from_roster_fields, 88152: sort_packet_roster_by_status_fields, 88224: assign_ranked_packet_members_fields, 88276: add_packet_city_resources_wrapped_fields, 88386: compact_arrival_packet_fields, 88428: detach_packet_force_head_fields, 91348: locate_arrival_city_fields}\nif target in children:\n    returned = children[target](state, entered)\nelif target == 24392:\n    returned = build_roster_fields(BattlePresentationMemory(state), entered)\nelif target == 57846:\n    returned = choose_city_head_fields(BattlePresentationMemory(state), entered)\nelif target == 33748:\n    returned = first_deployment_random_fields(BattlePolicyMemory(state), entered)\nelse:\n    raise MovementContinuationBoundary(target, entered, 'arrival child full algorithm not owned')\nreturned = _arrival_frame_fields(state, returned)\nactual = returned.stack_cursor.long()\nif actual != continuation:\n    raise MovementContinuationBoundary(actual, returned, 'original arrival return LONG changed')\nreturn first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))"}, '_arrival_adjacent_position_fields': {'signature': 'state, frame, city_order', 'returns': 'tuple', 'flow': "frame = _movement_compare(state, frame, low8(frame.target_y), frame.roster.byte(0, 1), 8)\nif frame.status & 4:\n    frame = _movement_compare(state, frame, low8(frame.count), frame.roster.byte(0, 2), 8)\n    if frame.status & 4:\n        return (frame, True)\nframe = _movement_compare(state, frame, low8(frame.target_x), frame.roster.byte(0, 1), 8)\nif frame.status & 4:\n    for carrier in ('offset_x', 'distance') if city_order else ('distance', 'offset_x'):\n        frame = _movement_compare(state, frame, low8(frame.carrier(carrier)), frame.roster.byte(0, 2), 8)\n        if frame.status & 4:\n            return (frame, True)\nframe = _movement_compare(state, frame, low8(frame.unit), frame.roster.byte(0, 1), 8)\nif frame.status & 4:\n    frame = _movement_compare(state, frame, low8(frame.count), frame.roster.byte(0, 2), 8)\n    if frame.status & 4:\n        return (frame, True)\nreturn (frame, False)"}, 'hostile_adjacent_block_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _arrival_frame_fields(state, frame)\nframe = _movement_move(state, frame, 'target_x', state.read(16726966, 2), 16)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)\nif not frame.status & 4:\n    return _arrival_carry_fields(state, frame, False)\nframe = _movement_move(state, frame, 'target_y', state.read(16726968, 2), 16)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 15, 16)\nif not frame.status & 4:\n    return _arrival_carry_fields(state, frame, False)\nframe = _movement_move(state, frame, 'target_x', state.read(16726966, 2), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_x', 4, True)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\nframe = _movement_adjust_word(state, frame, 'target_y', -1)\nframe = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)\nframe = _movement_adjust_word(state, frame, 'unit', 1)\nframe = _movement_move(state, frame, 'count', state.read(16726968, 2), 16)\nframe = _movement_fixed_shift_word(state, frame, 'count', 4, True)\nframe = _movement_move(state, frame, 'distance', low16(frame.count), 16)\nframe = _movement_adjust_word(state, frame, 'distance', -1)\nframe = _movement_move(state, frame, 'offset_x', low16(frame.count), 16)\nframe = _movement_adjust_word(state, frame, 'offset_x', 1)\nframe = first_replace(frame, roster=state.table_at(4294960912).cursor(), controller=state.table_at(state.read(16726060, 4)).cursor())\nframe = _movement_move(state, frame, 'offset_y', 0, 16)\nframe = _movement_move(state, frame, 'offset_y', frame.controller.byte(0, 4), 8)\nframe = _arrival_store_fields(state, frame, 16726974, low16(frame.offset_y))\nframe = _movement_fixed_shift_word(state, frame, 'offset_y', 1)\nframe = _movement_move(state, frame, 'offset_y', frame.roster.word(low16(frame.offset_y)), 16)\nframe = _arrival_store_fields(state, frame, 16726976, low16(frame.offset_y))\nframe = first_replace(frame, roster=state.table_at(4294938624).cursor())\nwhile True:\n    frame = _movement_move(state, frame, 'choice', frame.roster.byte(), 8)\n    frame = _movement_move(state, frame, 'choice', low16(frame.choice) & 15, 16)\n    if frame.status & 4:\n        break\n    frame = _arrival_bit_fields(state, frame, frame.roster.byte(), 5)\n    if frame.status & 4:\n        frame = _movement_move(state, frame, 'choice', 0, 16)\n        frame = _movement_move(state, frame, 'choice', frame.roster.byte(0, 4), 8)\n        frame = _movement_compare(state, frame, low8(frame.choice), state.read(16726975, 1), 8)\n        if not frame.status & 4:\n            frame = _movement_move(state, frame, 'offset_y', state.read(16726976, 2), 16)\n            frame = _arrival_bit_fields(state, frame, frame.offset_y, frame.choice)\n            if frame.status & 4:\n                frame, adjacent = _arrival_adjacent_position_fields(state, frame, False)\n                if adjacent:\n                    return _arrival_carry_fields(state, frame, True)\n    frame = _movement_move(state, frame, 'choice', frame.roster.byte(), 8)\n    frame = _movement_move(state, frame, 'choice', low16(frame.choice) & 15, 16)\n    frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.choice)) + 13))\nframe = first_replace(frame, roster=state.table_at(4294954652).cursor(), candidates=state.table_at(4294964264).cursor())\nframe = _arrival_swap_fields(state, frame, 'target_x')\nframe = _movement_move(state, frame, 'target_x', 39, 16)\nwhile True:\n    frame = _movement_test(state, frame, frame.roster.byte(), 8)\n    if not frame.status & 4:\n        frame = _movement_move(state, frame, 'choice', 0, 16)\n        frame = _movement_move(state, frame, 'choice', frame.candidates.byte(low16(frame.target_x)), 8)\n        frame = _movement_compare(state, frame, low8(frame.choice), state.read(16726975, 1), 8)\n        if not frame.status & 4:\n            frame = _movement_move(state, frame, 'offset_y', state.read(16726976, 2), 16)\n            frame = _arrival_bit_fields(state, frame, frame.offset_y, frame.choice)\n            if frame.status & 4:\n                frame = _arrival_swap_fields(state, frame, 'target_x')\n                frame, adjacent = _arrival_adjacent_position_fields(state, frame, True)\n                if adjacent:\n                    frame = _arrival_call_fields(state, frame, 87240, 87228)\n                    return _arrival_carry_fields(state, frame, True)\n                frame = _arrival_swap_fields(state, frame, 'target_x')\n    frame = first_replace(frame, roster=frame.roster.advance(-4))\n    frame, again = _arrival_db_fields(frame, 'target_x')\n    if not again:\n        return _arrival_carry_fields(state, frame, False)"}, 'collect_blocked_cargo_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _arrival_frame_fields(state, frame)\nframe = first_replace(frame, candidates=state.table_at(state.read(16726060, 4)).cursor())\nframe = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 3, 16)\nframe = _movement_compare(state, frame, low8(frame.target_x), 2, 8)\nrice = frame.status & 4 != 0\nfirst = 9 if rice else 5\nframe = _movement_move(state, frame, 'target_y', frame.candidates.byte(0, first), 8)\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 8)\nframe = _movement_move(state, frame, 'target_y', frame.candidates.byte(0, first + 1), 8)\nframe = _movement_shift_long(state, frame, 'target_y')\nframe = _movement_move(state, frame, 'target_y', frame.candidates.byte(0, first + 2), 8)\nframe = _movement_shift_long(state, frame, 'target_y')\nframe = _movement_move(state, frame, 'target_y', frame.candidates.byte(0, first + 3), 8)\nframe = _movement_arithmetic_long(state, frame, 'target_y', 10000)\nframe = _movement_compare_address(state, frame, frame.target_y, 999999)\nif not frame.status & 5:\n    frame = _movement_move_long(state, frame, 'target_y', 99999 if rice else 999999)\nfor displacement, long_shift in ((first + 3, True), (first + 2, True), (first + 1, False)):\n    frame = _arrival_store_fields(state, frame, frame.candidates.address(0, displacement), low8(frame.target_y), 1)\n    if long_shift:\n        frame = _movement_shift_long(state, frame, 'target_y', True)\n    else:\n        frame = _movement_fixed_shift_word(state, frame, 'target_y', 8, True)\nframe = _arrival_store_fields(state, frame, frame.candidates.address(0, first), low8(frame.target_y), 1)\nif not rice:\n    frame = _movement_compare(state, frame, low8(frame.target_x), 3, 8)\n    if frame.status & 4:\n        value = frame.roster.byte() & 128\n        frame = _arrival_store_fields(state, frame, frame.roster.base, value, 1)\n        value = frame.roster.byte() | 2\n        return _arrival_store_fields(state, frame, frame.roster.base, value, 1)\nreturn _arrival_store_fields(state, frame, frame.roster.base, 0, 1, True)"}, 'settle_arriving_group_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _arrival_frame_fields(state, frame)\nframe = first_replace(frame, candidates=state.table_at(state.read(16726060, 4)).cursor())\nframe = _arrival_call_fields(state, frame, 91348, 87420)\nframe = _movement_test(state, frame, low8(frame.target_x), 8)\nif frame.status & 8:\n    frame = _movement_move(state, frame, 'target_x', frame.candidates.byte(0, 4), 8)\n    frame = first_replace(frame, roster=state.table_at(4294964264).cursor())\n    frame = _arrival_store_fields(state, frame, frame.roster.address(low16(frame.distance)), low8(frame.target_x), 1)\n    frame = _arrival_call_fields(state, frame, 87930, 87442)\n    frame = _arrival_call_fields(state, frame, 88000, 87446)\nelse:\n    frame = _movement_compare(state, frame, low8(frame.target_x), frame.candidates.byte(0, 4), 8)\n    if not frame.status & 4:\n        frame = _movement_compare(state, frame, low16(frame.target_x), 16, 16)\n        if frame.status & 4:\n            return frame\n        frame = _arrival_store_fields(state, frame, 4294964086, 0, 2, True)\n        frame = _arrival_store_fields(state, frame, 4294964087, frame.candidates.byte(0, 4), 1)\n        frame = _movement_move(state, frame, 'target_x', state.read(4294964086, 2), 16)\n        for address in (4294964858, 4294964860, 4294964862):\n            frame = _movement_compare(state, frame, low16(frame.target_x), state.read(address, 2), 16)\n            if frame.status & 4:\n                break\n        if not frame.status & 4:\n            return _arrival_carry_fields(state, frame, False)\n        frame = first_replace(frame, candidates=state.table_at(4294961719).cursor())\n        frame = _movement_move(state, frame, 'target_x', state.read(4294964114, 2), 16)\n        frame = _arrival_bit_fields(state, frame, frame.candidates.byte(low16(frame.target_x)), 1)\n        if not frame.status & 4:\n            return _arrival_carry_fields(state, frame, False)\n        frame = _arrival_store_fields(state, frame, 4294964066, 12)\n        return _arrival_carry_fields(state, frame, True)\nframe = _movement_move(state, frame, 'target_x', low16(frame.distance), 16)\nstack = frame.stack_cursor.advance(-2)\nstack.set_word(0, low16(frame.distance))\nframe = _movement_test(state, first_replace(frame, stack_cursor=stack), low16(frame.distance), 16)\nframe = _movement_adjust_word(state, frame, 'target_x', 1)\nframe = _arrival_store_fields(state, frame, 4294964068, low16(frame.target_x))\nframe = _arrival_store_fields(state, frame, 4294964784, 65535)\nframe = _arrival_call_fields(state, frame, 24392, 87480)\nrestored = frame.stack_cursor.word()\nframe = _movement_move(state, first_replace(frame, stack_cursor=frame.stack_cursor.advance(2)), 'distance', restored, 16)\nframe = _movement_compare(state, frame, low16(frame.count), 10, 16)\nif not frame.status & 1:\n    return _arrival_carry_fields(state, frame, False)\nframe = first_replace(frame, roster=state.table_at(state.read(16726060, 4)).cursor())\nframe = _arrival_store_fields(state, frame, 4294964087, frame.roster.byte(0, 4), 1)\nframe = _movement_move(state, frame, 'target_y', frame.roster.byte(), 8)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 15, 16)\nframe = _arrival_add_fields(state, frame, 'count', low16(frame.target_y))\nframe = _movement_compare(state, frame, low16(frame.count), 10, 16)\nif not frame.status & 5:\n    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(0, 4), 8)\n    for address in (4294964859, 4294964861, 4294964863):\n        frame = _movement_compare(state, frame, low8(frame.target_x), state.read(address, 1), 8)\n        if frame.status & 4:\n            break\n    if not frame.status & 4:\n        frame = _arrival_call_fields(state, frame, 88024, 87648)\n        return _arrival_carry_fields(state, frame, False)\n    frame = _arrival_call_fields(state, frame, 88428, 87606)\n    frame = _arrival_store_fields(state, frame, 4294964068, low16(frame.target_x))\n    frame = _arrival_add_fields(state, frame, 'count', 10, True)\n    frame = _arrival_add_fields(state, frame, 'target_y', low16(frame.count), True)\n    if frame.status & 4:\n        return _arrival_carry_fields(state, frame, False)\n    frame = _arrival_store_fields(state, frame, 4294964870, low16(frame.target_y))\n    frame = _arrival_memory_increment_fields(state, frame, 4294964066)\n    return _arrival_carry_fields(state, frame, True)\nframe = _arrival_call_fields(state, frame, 87728, 87522)\nframe = _arrival_call_fields(state, frame, 87836, 87526)\nframe = _arrival_call_fields(state, frame, 87896, 87530)\nframe = first_replace(frame, roster=state.table_at(4294964318).cursor())\nframe = _movement_move(state, frame, 'target_x', state.read(4294964068, 2), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_x', 1)\nframe = _movement_test(state, frame, frame.roster.word(low16(frame.target_x)), 16)\nif frame.status & 8:\n    frame = _movement_move(state, frame, 'target_x', state.read(4294964068, 2), 16)\n    frame = _arrival_store_fields(state, frame, 4294964784, 65535)\n    frame = _arrival_call_fields(state, frame, 24392, 87564)\n    frame = _arrival_call_fields(state, frame, 57846, 87570)\nreturn _arrival_carry_fields(state, frame, False)"}, '_arrival_credit_resources_fields': {'signature': 'state, frame, wrapped', 'returns': 'FirstDeploymentFrame', 'flow': "carrier = 'target_x' if wrapped else 'offset_x'\naccumulator = 'unit' if wrapped else 'offset_x'\nindex = 'target_y' if wrapped else 'distance'\ncity = low16(frame.distance) if wrapped else low16(frame.target_x)\nframe = _movement_move(state, frame, index, city, 16)\nframe = _movement_fixed_shift_word(state, frame, index, 2)\nfor first, address in ((5, 4294959100), (9, 4294959260)):\n    if not wrapped:\n        frame = first_replace(frame, opponent=state.table_at(address).cursor())\n    frame = _movement_move(state, frame, carrier, frame.roster.byte(0, first), 8)\n    frame = _movement_fixed_shift_word(state, frame, carrier, 8)\n    frame = _movement_move(state, frame, carrier, frame.roster.byte(0, first + 1), 8)\n    frame = _movement_shift_long(state, frame, carrier)\n    frame = _movement_move(state, frame, carrier, frame.roster.byte(0, first + 2), 8)\n    frame = _movement_shift_long(state, frame, carrier)\n    frame = _movement_move(state, frame, carrier, frame.roster.byte(0, first + 3), 8)\n    if wrapped:\n        frame = first_replace(frame, candidates=state.table_at(address).cursor())\n        frame = _movement_move_long(state, frame, accumulator, frame.candidates.long(low16(frame.carrier(index))))\n        frame = _movement_arithmetic_long(state, frame, accumulator, frame.carrier(carrier))\n        frame = _movement_compare_address(state, frame, frame.carrier(accumulator), 999999)\n        cap = not frame.status & 5\n    else:\n        frame = _movement_arithmetic_long(state, frame, accumulator, frame.opponent.long(low16(frame.carrier(index))))\n        cap = frame.status & 1 != 0\n        if not cap:\n            frame = _movement_compare_address(state, frame, frame.carrier(accumulator), 999999)\n            cap = not frame.status & 5\n    if cap:\n        frame = _movement_move_long(state, frame, accumulator, 999999)\n    destination = frame.candidates if wrapped else frame.opponent\n    frame = _arrival_store_fields(state, frame, destination.address(low16(frame.carrier(index))), frame.carrier(accumulator), 4)\nreturn frame"}, 'add_packet_city_resources_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _arrival_credit_resources_fields(state, _arrival_frame_fields(state, frame), False)'}, 'add_packet_city_resources_wrapped_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'return _arrival_credit_resources_fields(state, _arrival_frame_fields(state, frame), True)'}, 'assign_packet_members_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _arrival_frame_fields(state, frame)\nframe = first_replace(frame, candidates=state.table_at(4294953984).cursor(), scan=frame.roster.advance(13))\nframe = _movement_move(state, frame, 'count', low16(frame.target_y), 16)\nframe = _movement_adjust_word(state, frame, 'count', -1)\nframe = _movement_move(state, frame, 'unit', 0, 16)\nframe = _movement_move(state, frame, 'distance', 0, 16)\nframe = _movement_move(state, frame, 'distance', frame.roster.byte(0, 4), 8)\nframe = _movement_fixed_shift_word(state, frame, 'distance', 1)\nframe = first_replace(frame, controller=state.table_at(4294960704).cursor())\nframe = _movement_move(state, frame, 'distance', frame.controller.word(low16(frame.distance)), 16)\nframe = first_replace(frame, controller=state.table_at(4294964318).cursor())\nwhile True:\n    value = frame.scan.byte()\n    frame = _movement_move(state, first_replace(frame, scan=frame.scan.advance(1)), 'unit', value, 8)\n    frame = _arrival_store_fields(state, frame, frame.candidates.address(low16(frame.unit)), low8(frame.target_x), 1)\n    frame = _movement_compare(state, frame, low8(frame.distance), low8(frame.unit), 8)\n    if frame.status & 4:\n        frame = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)\n        frame = _movement_fixed_shift_word(state, frame, 'unit', 1)\n        frame = _arrival_store_fields(state, frame, frame.controller.address(low16(frame.unit)), low16(frame.distance))\n    frame, again = _arrival_db_fields(frame, 'count')\n    if not again:\n        return frame"}, '_arrival_compact_packet_tail_fields': {'signature': 'state, frame', 'returns': 'FirstDeploymentFrame', 'flow': "while True:\n    frame = _movement_move(state, frame, 'target_x', frame.candidates.byte(), 8)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)\n    if frame.status & 4:\n        break\n    frame = _arrival_add_fields(state, frame, 'target_x', 12)\n    while True:\n        value = frame.candidates.byte()\n        frame = _arrival_store_fields(state, frame, frame.roster.base, value, 1)\n        frame = first_replace(frame, candidates=frame.candidates.advance(1), roster=frame.roster.advance(1))\n        frame, again = _arrival_db_fields(frame, 'target_x')\n        if not again:\n            break\nframe = _arrival_store_fields(state, frame, frame.roster.base, 0, 1, True)\nreturn _arrival_store_fields(state, frame, 16726060, 0, 4, True)"}, 'compact_after_packet_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _arrival_frame_fields(state, frame)\nframe = first_replace(frame, candidates=frame.roster.advance(s16(low16(frame.target_y)) + 13))\nreturn _arrival_compact_packet_tail_fields(state, frame)'}, 'initialize_arrival_loyalty_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _arrival_frame_fields(state, frame)\nsaved = ('target_x', 'target_y', 'unit', 'distance', 'roster')\nframe = _movement_save_longs(state, frame, saved)\nframe = first_replace(frame, roster=state.table_at(4294960704).cursor())\nframe = _movement_fixed_shift_word(state, frame, 'target_x', 1)\nframe = _movement_move(state, frame, 'target_x', frame.roster.word(low16(frame.target_x)), 16)\nframe = first_replace(frame, roster=state.table_at(4294951424).cursor())\nframe = _movement_move(state, frame, 'unit', 0, 16)\nframe = _movement_move(state, frame, 'unit', frame.roster.byte(low16(frame.target_x)), 8)\nframe = _arrival_call_fields(state, frame, 33748, 87960)\nframe = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)\nframe = _movement_move_long(state, frame, 'target_y', frame.target_x)\nvalue = frame.target_x\nshifted = u32(value << 1)\nstatus = (17 if value & 2147483648 else 0) | (8 if shifted & 2147483648 else 0) | (4 if shifted == 0 else 0)\nstate.sr = state.sr & 65504 | status\nframe = first_replace(frame, target_x=shifted, status=status)\nframe = _movement_arithmetic_long(state, frame, 'target_x', frame.target_y)\nframe = _arrival_swap_fields(state, frame, 'target_x')\nframe = _arrival_add_fields(state, frame, 'target_x', 6)\nframe = _movement_multiply_word(state, frame, 'unit', low16(frame.target_x))\nframe = _movement_divu_word(state, frame, 'unit', 10, 87980)\nframe = first_replace(frame, roster=state.table_at(4294959904).cursor())\nframe = _movement_fixed_shift_word(state, frame, 'distance', 2)\nframe = _arrival_store_fields(state, frame, frame.roster.address(low16(frame.distance), 2), low16(frame.unit))\nreturn _movement_restore_longs(state, frame, saved)"}, 'clear_arrival_city_order_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _arrival_frame_fields(state, frame)\nsaved = ('target_x', 'roster')\nframe = _movement_save_longs(state, frame, saved)\nframe = first_replace(frame, roster=state.table_at(4294961012).cursor())\nframe = _movement_move(state, frame, 'target_x', state.read(4294964114, 2), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_x', 2)\nframe = _arrival_store_fields(state, frame, frame.roster.address(low16(frame.target_x)), 0, 4, True)\nreturn _movement_restore_longs(state, frame, saved)"}, 'merge_overcapacity_arrival_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _arrival_frame_fields(state, frame)\nframe = _movement_adjust_word(state, frame, 'distance', 1)\nfor target, continuation in ((88052, 88030), (88084, 88034), (88152, 88038), (88224, 88042), (88276, 88046), (88386, 88050)):\n    frame = _arrival_call_fields(state, frame, target, continuation)\nreturn frame"}, 'build_packet_member_roster_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _arrival_frame_fields(state, frame)\nframe = first_replace(frame, candidates=state.table_at(4294955776).cursor())\nframe = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\nframe = _movement_adjust_word(state, frame, 'target_y', -1)\nframe = _movement_move(state, frame, 'unit', 0, 16)\nwhile True:\n    frame = _movement_move(state, frame, 'unit', frame.roster.byte(low16(frame.target_y), 13), 8)\n    frame = _arrival_store_fields(state, frame, frame.candidates.base, low16(frame.unit))\n    frame = first_replace(frame, candidates=frame.candidates.advance(2))\n    frame, again = _arrival_db_fields(frame, 'target_y')\n    if not again:\n        return _arrival_store_fields(state, frame, frame.candidates.base, 65535)"}, 'extract_force_head_from_roster_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _arrival_frame_fields(state, frame)\nframe = _movement_move(state, frame, 'target_y', 0, 16)\nframe = _movement_move(state, frame, 'target_y', frame.roster.byte(0, 4), 8)\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 1)\nframe = first_replace(frame, candidates=state.table_at(4294960704).cursor())\nframe = _movement_move(state, frame, 'target_y', frame.candidates.word(low16(frame.target_y)), 16)\nframe = first_replace(frame, candidates=state.table_at(4294955776).cursor(), controller=state.table_at(4294955798).cursor(), scan=state.table_at(4294955820).cursor())\nwhile True:\n    value = frame.candidates.word()\n    frame = _movement_move(state, first_replace(frame, candidates=frame.candidates.advance(2)), 'unit', value, 16)\n    if frame.status & 8:\n        break\n    frame = _movement_compare(state, frame, low16(frame.unit), low16(frame.target_y), 16)\n    if not frame.status & 4:\n        continue\n    frame = _arrival_store_fields(state, frame, frame.controller.base, low16(frame.target_y))\n    frame = first_replace(frame, controller=frame.controller.advance(2))\n    frame = _arrival_store_fields(state, frame, frame.scan.base, 100)\n    frame = first_replace(frame, scan=frame.scan.advance(2))\n    while True:\n        value = frame.candidates.word()\n        frame = first_replace(frame, candidates=frame.candidates.advance(2))\n        frame = _arrival_store_fields(state, frame, frame.candidates.address(0, -4), value)\n        if frame.status & 8:\n            break\n    frame = _movement_move(state, frame, 'unit', low16(frame.distance), 16)\n    frame = _movement_fixed_shift_word(state, frame, 'unit', 1)\n    frame = first_replace(frame, candidates=state.table_at(4294964318).cursor())\n    frame = _arrival_store_fields(state, frame, frame.candidates.address(low16(frame.unit)), low16(frame.target_y))\n    break\nreturn _arrival_store_fields(state, frame, frame.controller.base, 65535)"}, 'sort_packet_roster_by_status_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _arrival_frame_fields(state, frame)\nframe = first_replace(frame, candidates=state.table_at(4294955776).cursor(), opponent=state.table_at(4294951680).cursor())\nframe = _movement_move(state, frame, 'unit', 0, 16)\nwhile True:\n    value = frame.candidates.word()\n    frame = _movement_move(state, first_replace(frame, candidates=frame.candidates.advance(2)), 'target_y', value, 16)\n    if frame.status & 8:\n        return frame\n    frame = _movement_move(state, frame, 'unit', frame.opponent.byte(low16(frame.target_y)), 8)\n    frame = first_replace(frame, controller=state.table_at(4294955798).cursor(), scan=state.table_at(4294955820).cursor())\n    while True:\n        frame = _movement_test(state, frame, frame.controller.word(), 16)\n        if frame.status & 8:\n            break\n        frame = _movement_compare(state, frame, low16(frame.unit), frame.scan.word(), 16)\n        if not frame.status & 5:\n            break\n        frame = first_replace(frame, controller=frame.controller.advance(2), scan=frame.scan.advance(2))\n    while True:\n        frame = _movement_move(state, frame, 'offset_x', frame.controller.word(), 16)\n        frame = _movement_move(state, frame, 'offset_y', frame.scan.word(), 16)\n        frame = _arrival_store_fields(state, frame, frame.controller.base, low16(frame.target_y))\n        frame = first_replace(frame, controller=frame.controller.advance(2))\n        frame = _arrival_store_fields(state, frame, frame.scan.base, low16(frame.unit))\n        frame = first_replace(frame, scan=frame.scan.advance(2))\n        frame = _movement_move(state, frame, 'target_y', low16(frame.offset_x), 16)\n        if frame.status & 8:\n            break\n        frame = _movement_move(state, frame, 'unit', low16(frame.offset_y), 16)\n    frame = _arrival_store_fields(state, frame, frame.controller.base, 65535)"}, 'assign_ranked_packet_members_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _arrival_frame_fields(state, frame)\nframe = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)\nframe = _arrival_add_fields(state, frame, 'count', 9, True)\nframe = _arrival_add_fields(state, frame, 'target_x', low16(frame.count), True)\nframe = first_replace(frame, candidates=state.table_at(4294955798).cursor(), controller=state.table_at(4294953984).cursor())\nwhile True:\n    value = frame.candidates.word()\n    frame = _movement_move(state, first_replace(frame, candidates=frame.candidates.advance(2)), 'target_y', value, 16)\n    frame = _arrival_store_fields(state, frame, frame.controller.address(low16(frame.target_y)), low8(frame.distance), 1)\n    frame, again = _arrival_db_fields(frame, 'target_x')\n    if not again:\n        break\nframe = _arrival_bit_fields(state, frame, low8(frame.distance), 7)\nframe = first_replace(frame, distance=replace_byte(frame.distance, low8(frame.distance) | 128))\nwhile True:\n    value = frame.candidates.word()\n    frame = _movement_move(state, first_replace(frame, candidates=frame.candidates.advance(2)), 'target_y', value, 16)\n    if frame.status & 8:\n        break\n    frame = _arrival_store_fields(state, frame, frame.controller.address(low16(frame.target_y)), low8(frame.distance), 1)\nframe = _arrival_bit_fields(state, frame, low8(frame.distance), 7)\nreturn first_replace(frame, distance=replace_byte(frame.distance, low8(frame.distance) & 127))"}, 'compact_arrival_packet_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _arrival_frame_fields(state, frame)\nframe = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)\nframe = first_replace(frame, candidates=frame.roster.advance(s16(low16(frame.target_x)) + 13))\nreturn _arrival_compact_packet_tail_fields(state, frame)"}, 'detach_packet_force_head_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _arrival_frame_fields(state, frame)\nsaved = ('target_x', 'target_y', 'unit', 'candidates')\nframe = _movement_save_longs(state, frame, saved)\nframe = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)\nframe = _movement_adjust_word(state, frame, 'target_x', -1)\nframe = _movement_move(state, frame, 'target_y', 0, 16)\nframe = _movement_move(state, frame, 'target_y', frame.roster.byte(0, 4), 8)\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 1)\nframe = first_replace(frame, candidates=state.table_at(4294960704).cursor())\nframe = _movement_move(state, frame, 'target_y', frame.candidates.word(low16(frame.target_y)), 16)\nframe = _movement_move(state, frame, 'unit', 0, 16)\nwhile True:\n    frame = _movement_compare(state, frame, low8(frame.target_y), frame.roster.byte(low16(frame.unit), 13), 8)\n    if frame.status & 4:\n        break\n    frame = _movement_adjust_word(state, frame, 'unit', 1)\n    frame = _movement_compare(state, frame, low16(frame.unit), low16(frame.target_x), 16)\n    if not frame.status & 1:\n        return _movement_restore_longs(state, frame, saved)\nwhile True:\n    frame = _movement_adjust_word(state, frame, 'unit', 1)\n    frame = _movement_compare(state, frame, low16(frame.unit), low16(frame.target_x), 16)\n    if not frame.status & 1:\n        break\n    value = frame.roster.byte(low16(frame.unit), 13)\n    frame = _arrival_store_fields(state, frame, frame.roster.address(low16(frame.unit), 12), value, 1)\nwhile True:\n    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(low16(frame.unit), 13), 8)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)\n    if frame.status & 4:\n        break\n    frame = _arrival_add_fields(state, frame, 'target_x', 12)\n    while True:\n        value = frame.roster.byte(low16(frame.unit), 13)\n        frame = _arrival_store_fields(state, frame, frame.roster.address(low16(frame.unit), 12), value, 1)\n        frame = _movement_adjust_word(state, frame, 'unit', 1)\n        frame, again = _arrival_db_fields(frame, 'target_x')\n        if not again:\n            break\nframe = _arrival_store_fields(state, frame, frame.roster.address(low16(frame.unit), 12), 0, 1, True)\noriginal = frame.roster.byte()\nframe, reduced = _movement_mutation_flags(state, frame, original, -1, 8)\nframe.roster.set_byte(0, reduced)\nframe = first_replace(frame, candidates=state.table_at(4294953984).cursor())\nframe = _movement_move(state, frame, 'unit', low8(frame.distance), 8)\nframe = _movement_adjust_word(state, frame, 'unit', 1)\nframe = _arrival_store_fields(state, frame, frame.candidates.address(low16(frame.target_y)), low8(frame.unit), 1)\nframe = _movement_fixed_shift_word(state, frame, 'unit', 1)\nframe = first_replace(frame, candidates=state.table_at(4294964318).cursor())\nframe = _arrival_store_fields(state, frame, frame.candidates.address(low16(frame.unit)), low16(frame.target_y))\nframe = _movement_adjust_word(state, frame, 'count', 1)\nreturn _movement_restore_longs(state, frame, saved)"}, '_arrival_match_coordinate_fields': {'signature': 'state, frame', 'returns': 'tuple', 'flow': "frame = _movement_move(state, frame, 'choice', low16(frame.offset_y), 16)\nframe = _arrival_add_fields(state, frame, 'choice', 24, True)\nframe = _movement_compare(state, frame, low16(frame.target_y), low16(frame.choice), 16)\nif frame.status & 4:\n    frame = _movement_move(state, frame, 'choice', low16(frame.offset_x), 16)\n    frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.choice), 16)\n    if frame.status & 4:\n        return (frame, True)\n    frame = _arrival_add_fields(state, frame, 'choice', 16, True)\n    frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.choice), 16)\n    if frame.status & 4:\n        return (frame, True)\nframe = _movement_move(state, frame, 'choice', low16(frame.offset_y), 16)\nframe = _arrival_add_fields(state, frame, 'choice', 8, True)\nframe = _movement_compare(state, frame, low16(frame.target_y), low16(frame.choice), 16)\nif frame.status & 4:\n    frame = _movement_move(state, frame, 'choice', low16(frame.offset_x), 16)\n    frame = _arrival_add_fields(state, frame, 'choice', 16)\n    frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.choice), 16)\n    if frame.status & 4:\n        return (frame, True)\n    frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.offset_x), 16)\n    if frame.status & 4:\n        return (frame, True)\n    frame = _movement_move(state, frame, 'choice', low16(frame.offset_x), 16)\n    frame = _arrival_add_fields(state, frame, 'choice', 16, True)\n    frame = _movement_compare(state, frame, low16(frame.choice), low16(frame.offset_x), 16)\n    if frame.status & 4:\n        return (frame, True)\n    frame = _movement_move(state, frame, 'choice', low16(frame.offset_x), 16)\n    frame = _arrival_add_fields(state, frame, 'choice', 32, True)\n    frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.choice), 16)\n    if frame.status & 4:\n        return (frame, True)\nframe = _movement_move(state, frame, 'choice', low16(frame.offset_y), 16)\nframe = _arrival_add_fields(state, frame, 'choice', 8, False)\nframe = _movement_compare(state, frame, low16(frame.target_y), low16(frame.choice), 16)\nif frame.status & 4:\n    frame = _movement_move(state, frame, 'choice', low16(frame.offset_x), 16)\n    frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.choice), 16)\n    if frame.status & 4:\n        return (frame, True)\n    frame = _arrival_add_fields(state, frame, 'choice', 16, True)\n    frame = _movement_compare(state, frame, low16(frame.target_x), low16(frame.choice), 16)\n    if frame.status & 4:\n        return (frame, True)\nreturn (frame, False)"}, 'locate_arrival_city_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _arrival_frame_fields(state, frame)\nframe = _movement_move(state, frame, 'target_x', 0, 16)\nframe = _movement_move(state, frame, 'target_x', frame.candidates.byte(0, 2), 8)\nframe = _movement_fixed_shift_word(state, frame, 'target_x', 4)\nframe = _movement_move(state, frame, 'target_y', 0, 16)\nframe = _movement_move(state, frame, 'target_y', frame.candidates.byte(0, 1), 8)\nframe = _movement_fixed_shift_word(state, frame, 'target_y', 4)\nframe = first_replace(frame, controller=state.table_at(871114).cursor(), scan=state.table_at(4294964264).cursor())\nframe = _movement_move(state, frame, 'count', 39, 16)\nframe = _movement_move(state, frame, 'distance', 0, 16)\nframe = _arrival_store_fields(state, frame, 4294964114, 1)\nwhile True:\n    value = frame.controller.word()\n    frame = _movement_move(state, first_replace(frame, controller=frame.controller.advance(2)), 'offset_x', value, 16)\n    value = frame.controller.word()\n    frame = _movement_move(state, first_replace(frame, controller=frame.controller.advance(2)), 'offset_y', value, 16)\n    frame, matched = _arrival_match_coordinate_fields(state, frame)\n    if matched:\n        frame = first_replace(frame, controller=state.table_at(4294964264).cursor())\n        frame = _movement_move(state, frame, 'target_x', 0, 16)\n        return _movement_move(state, frame, 'target_x', frame.controller.byte(low16(frame.distance)), 8)\n    frame = _movement_adjust_word(state, frame, 'distance', 1)\n    frame = _arrival_memory_increment_fields(state, frame, 4294964114)\n    frame, again = _arrival_db_fields(frame, 'count')\n    if not again:\n        return _movement_move(state, frame, 'target_x', 16, 16)"}})
APPROVED.setdefault('domain', set()).update(('s16',))
APPROVED.setdefault((2, 'high_level_scene_flows.domain'), set()).update(('SceneState',))
APPROVED.setdefault((2, 'high_level_main_flows.services'), set()).update(('FirstDeploymentFrame',))
APPROVED.setdefault((2, 'high_level_main_flows.business_movement_support'), set()).update(('first_replace', 'MovementContinuationBoundary', '_movement_frame', '_movement_move', '_movement_test', '_movement_test_long', '_movement_move_long', '_movement_compare', '_movement_compare_address', '_movement_binary_flags', '_movement_fixed_shift_word', '_movement_shift_long', '_movement_adjust_word', '_movement_arithmetic_long', '_movement_multiply_word', '_movement_divu_word', '_movement_save_longs', '_movement_restore_longs', '_movement_mutation_flags'))
APPROVED.setdefault((2, 'high_level_main_flows.business_gameplay'), set()).update(('_order_full_sr_carry',))
APPROVED.setdefault((2, 'high_level_gameplay_flow.contexts_battle'), set()).update(('BattlePresentationMemory',))
APPROVED.setdefault((2, 'high_level_gameplay_flow.business_battle'), set()).update(('build_roster_fields', 'choose_city_head_fields'))
APPROVED.setdefault((2, 'high_level_battle_ai.contexts_policy_memory'), set()).update(('BattlePolicyMemory',))
APPROVED.setdefault((2, 'high_level_battle_ai.business_formation'), set()).update(('first_deployment_random_fields',))
