"""Complete semantic AST admission and fixed-layout ordinary movement lowering.

The declarations describe supported executable business control and live effects;
the backend consumes their admitted semantic literals. No original image, ASM,
IR, object, cache or instruction-byte table is read during generation.
"""
from .compiler_common import semantic_functions, lower_declared, CompileError
from .target import CAMPAIGN_BINDINGS

DECLARATIONS = {
  "prepare_transport_path": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "state = checked_state(state)\noffset = u16(state.transport_index() << 2)\nrecords = state.transport_records\nbudget = 15\nkind = records.byte(offset) & 3\nif kind == 3:\n    budget = 10\nstate.set_transport_budget(budget)\nstate.set_path_origin_x(u16(records.byte(offset, 1) << 4))\nstate.set_path_origin_y(u16(records.byte(offset, 2) << 4))\ndestination = u16(records.byte(offset, 3) << 2)\ncoordinates = state.city_coordinates\nstate.set_path_target_x(coordinates.word(destination, 2))\nstate.set_path_target_y(coordinates.word(destination))\nbuild_path(state)\nstate.set_route(522)\nstate.set_stage(1)\nstate.set_transport_progress(0)\nreturn None",
    "slots": {
      15: [
        "transport_budget",
        1,
        65535
      ]
    }
  },
  "ensure_neighbor_capacity": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "state = checked_state(state)\ncapacity = selected_roster_capacity(state)\nmode_offset = u16((state.neighbor_mode() & 3) << 1)\nselected = state.neighbor_selected_slots.at(mode_offset)\npointer = state.neighbor_source_pointers.long(u16(mode_offset << 1))\nsource_head = state.table(pointer).word()\nif not negative_word(selected.word()):\n    group = find_group_at_coordinate(state, selected.word())\n    combined = u8((group.byte() & 15) + low8(capacity))\n    if combined <= 10:\n        return None\ncount = collect_six_neighbor_candidates(state)\ncount = filter_neighbor_candidates(state, count, source_head)\nif count == 0:\n    return None\ncandidates = state.neighbor_candidates.cursor()\nfor remaining in descending_inclusive(u16(count - 1)):\n    coordinate = candidates.next_word()\n    if not negative_word(coordinate):\n        selected.set_word(0, coordinate)\n        return None\ncandidates = state.neighbor_candidates.cursor()\nfor remaining in descending_inclusive(u16(count - 1)):\n    coordinate = candidates.next_word() & 32767\n    group = find_group_at_coordinate(state, coordinate)\n    combined = u8((group.byte() & 15) + low8(capacity))\n    if combined <= 10:\n        selected.set_word(0, coordinate)\n        return None\nselected.set_word(0, 65535)\nreturn None",
    "slots": {
      10: [
        "group_capacity",
        1,
        127
      ]
    }
  },
  "find_group_at_coordinate": {
    "signature": "state: GameState, coordinate: Word",
    "returns": "Table",
    "flow": "state = checked_state(state)\ncoordinate = uint(coordinate, 16)\nx = coordinate >> 8\ny = low8(coordinate)\ngroup = state.group_packets\nwhile True:\n    members = group.byte() & 15\n    if members == 0:\n        return group\n    if group.byte(0, 1) == x:\n        if group.byte(0, 2) == y:\n            return group\n    group = group.advance(13 + members)"
  },
  "collect_six_neighbor_candidates": {
    "signature": "state: GameState",
    "returns": "Word",
    "flow": "state = checked_state(state)\noutput = state.neighbor_candidates.cursor()\ncount = 0\ncity_offset = u16(state.neighbor_city() << 2)\ncoordinates = state.city_coordinates\nx = coordinates.word(city_offset, 2) >> 4\ny = coordinates.word(city_offset) >> 4\nx = u16(x - 1)\ny = u16(y - 1)\nfor dx, dy in ((0, 0), (0, 1), (1, 1), (1, -1), (0, -1), (-1, -1)):\n    x = u16(x + dx)\n    y = u16(y + dy)\n    cost = read_neighbor_source_cost(state, x, y)\n    if s8(cost) >= 0:\n        coordinate = u16(low8(x) << 8 | low8(y))\n        output.append_word(coordinate)\n        count = u16(count + 1)\nreturn count"
  },
  "filter_neighbor_candidates": {
    "signature": "state: GameState, count: Word, source_head: Word",
    "returns": "Word",
    "flow": "state = checked_state(state)\ncount = uint(count, 16)\nsource_head = uint(source_head, 16)\ngroup = state.group_packets\ncandidates = state.neighbor_candidates_prefix\nwhile True:\n    members = group.byte() & 15\n    if members == 0:\n        return count\n    coordinate = u16(group.byte(0, 1) << 8 | group.byte(0, 2))\n    position = u16(count << 1)\n    matched = False\n    while True:\n        if candidates.word(position) == coordinate:\n            matched = True\n            break\n        position = u16(position - 2)\n        if position == 0:\n            break\n    if matched:\n        if group.byte(0, 4) == low8(source_head):\n            candidates.set_word(position, candidates.word(position) | 32768)\n        else:\n            count = u16(count - 1)\n            if count == 0:\n                return count\n            limit = u16(count << 1)\n            while True:\n                candidates.set_word(position, candidates.word(position, 2))\n                position = u16(position + 2)\n                if position >= limit:\n                    break\n    group = group.advance(13 + members)"
  },
  "selected_roster_capacity": {
    "signature": "state: GameState",
    "returns": "Word",
    "flow": "state = checked_state(state)\nif state.neighbor_mode_low() & 1:\n    return 1\nif state.neighbor_mode_low() & 2:\n    offset = u16(state.neighbor_city() << 1)\n    if state.city_heads.word(offset) != state.selected_officer():\n        return 1\n    primary = state.city_primary_roster.cursor()\n    secondary = state.city_secondary_roster.cursor()\nelse:\n    city = state.neighbor_city()\n    if state.neighbor_city_flags.byte(city) != state.selected_officer():\n        return 1\n    primary = state.primary_roster.cursor()\n    secondary = state.secondary_roster.cursor()\ncount = 0\nwhile not negative_word(primary.next_word()):\n    count = u16(count + 1)\nwhile not negative_word(secondary.next_word()):\n    count = u16(count + 1)\nif count > 10:\n    count = 10\nreturn count",
    "slots": {
      10: [
        "selected_capacity",
        1,
        32767
      ]
    }
  },
  "read_neighbor_source_cost": {
    "signature": "state: GameState, x: Word, y: Word",
    "returns": "Byte",
    "flow": "state = checked_state(state)\nx = uint(x, 16)\ny = uint(y, 16)\nindex = u16(u16(u16(x << 3) + x) << 3)\nindex = u16(index + y)\nstate.terrain_sources.byte(index)\nreturn state.terrain_costs.byte(index)"
  },
  "build_ai_movement_packet": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "state = checked_state(state)\nstate.set_path_origin_x(state.ai_origin_x())\nstate.set_path_origin_y(state.ai_origin_y())\ncoordinates = state.city_coordinates\ncity_offset = u16(state.chosen_city() << 2)\nstate.set_path_target_x(coordinates.word(city_offset, 2))\nstate.set_path_target_y(coordinates.word(city_offset))\npath = build_path(state)\noutput = state.movement_queue.cursor(state.movement_queue_offset())\noutput.append_byte(0)\noutput.append_byte(state.ai_packet_marker())\noutput.append_byte(state.ai_budget_low())\nappend_ai_path_steps(state, output, path.retained_direction)\nreturn None"
  },
  "append_ai_path_steps": {
    "signature": "state: GameState, output: Cursor, retained_direction: Word",
    "returns": "None",
    "flow": "state = checked_state(state)\nretained_direction = uint(retained_direction, 16)\noutput = checked_cursor(output, state)\nbudget = state.ai_budget()\nx = state.ai_origin_x() >> 4\ny = state.ai_origin_y() >> 4\npacket_bytes = 4\nsources = state.terrain_sources\ncosts = state.terrain_costs\npath = state.world_path_steps.cursor()\ndirection = retained_direction\nwhile True:\n    step = path.next_byte()\n    direction = u16(replace_byte(direction, step))\n    if s8(step) < 0:\n        break\n    vector_offset = u16(direction << 2)\n    vectors = state.group_step_vectors\n    x = u16(x + vectors.word(vector_offset))\n    y = u16(y + vectors.word(vector_offset, 2))\n    direction = vector_offset >> 2\n    cost = read_path_step_cost(state, x, y, sources, costs)\n    old_budget = low8(budget)\n    budget = u16(replace_byte(budget, u8(old_budget - cost)))\n    if old_budget < cost:\n        break\n    packet_bytes = u16(packet_bytes + 1)\n    output.append_byte(low8(direction))\n    if low8(budget) == 0:\n        break\noutput.set_byte(0, 0)\noutput.set_byte(0, 255, 1)\nstate.set_movement_queue_offset(u16(state.movement_queue_offset() + packet_bytes))\nreturn None"
  },
  "read_path_step_cost": {
    "signature": "state: GameState, x: Word, y: Word, sources: Table, costs: Table",
    "returns": "Byte",
    "flow": "state = checked_state(state)\nx = uint(x, 16)\ny = uint(y, 16)\nsources = state.checked_table(sources)\ncosts = state.checked_table(costs)\nindex = u16(u16(u16(x << 3) + x) << 3)\nindex = u16(index + y)\nterrain = sources.byte(index)\nreturn costs.byte(terrain)"
  },
  "choose_ai_destination": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "state = checked_state(state)\ngroup = state.group_packets.at(state.ai_group_index())\nbudget = group.byte(0, 3)\nx = group.byte(0, 1)\nstate.set_path_origin_x(u16(x << 4))\ny = group.byte(0, 2)\nstate.set_path_origin_y(u16(y << 4))\nowners = state.city_owner_slots\ncoordinates = state.following_city_coordinates\nbest = 65535\nstate.set_chosen_city(65535)\nfor city in descending_inclusive(39):\n    if owners.byte(city) != state.current_force():\n        continue\n    if city_roster_full_carry(state, city).carry:\n        continue\n    offset = u16(city << 2)\n    target_x = coordinates.word(offset, 2)\n    state.set_path_target_x(target_x)\n    target_x = target_x >> 4\n    dx = u16(target_x - x)\n    if target_x < x:\n        dx = u16(-dx)\n    if dx > budget:\n        continue\n    target_y = coordinates.word(offset)\n    state.set_path_target_y(target_y)\n    target_y = target_y >> 4\n    dy = u16(target_y - y)\n    if target_y < y:\n        dy = u16(-dy)\n    distance = u16(dx + dy)\n    if distance > budget:\n        continue\n    path = build_path(state)\n    owners = path.final_frontier_cursor\n    coordinates = path.final_grid\n    if best > state.path_length():\n        best = state.path_length()\n        state.set_chosen_city(city)\nreturn None"
  },
  "city_roster_full_carry": {
    "signature": "state: GameState, city: Word",
    "returns": "CarryOutcome",
    "flow": "state = checked_state(state)\ncity = uint(city, 16)\nassignment = u16(city + 1)\ncount = 0\nfor officer in descending_inclusive(255):\n    if state.officer_assignments.byte(officer) == low8(assignment):\n        count = u16(count + 1)\nif count >= 10:\n    return state.carry_result(1)\nreturn state.carry_result(0)",
    "slots": {
      10: [
        "city_capacity",
        1,
        65535
      ]
    }
  }
}

APPROVED = {
    'domain': {'GameState','Table','Cursor','Word','Byte','CarryOutcome','uint',
               'u8','u16','low8','replace_byte','s8','negative_word',
               'descending_inclusive','checked_state','checked_cursor'},
    'business_path': {'build_path'},
}


def _prepare_transport(e, rules):
    kind_done = e.fresh('kind_budget')
    e.ins('move.w', '0xcea0:w,%d0', 4)
    e.ins('lsl.w', '#2,%d0')
    e.ins('lea.l', '0xce00:w,%a0', 4)
    e.ins('move.w', f"#{rules['transport_budget']},%d1", 4)
    e.ins('move.b', '(%a0,%d0.w),%d2', 4)
    e.ins('andi.w', '#3,%d2', 4)
    e.ins('cmpi.b', '#3,%d2', 4)
    e.ins('bne.b', kind_done)
    e.ins('move.w', '#10,%d1', 4)
    e.label(kind_done)
    e.ins('move.w', '%d1,0xcea2:w', 4)
    for displacement, target in ((1, 0xF63C), (2, 0xF63E)):
        e.ins('clr.w', '%d1')
        e.ins('move.b', f'{displacement}(%a0,%d0.w),%d1', 4)
        e.ins('lsl.w', '#4,%d1')
        e.ins('move.w', f'%d1,0x{target:x}:w', 4)
    e.ins('clr.w', '%d1')
    e.ins('move.b', '3(%a0,%d0.w),%d1', 4)
    e.ins('lsl.w', '#2,%d1')
    e.ins('lea.l', '0xd4ac6:l,%a0', 6)
    e.ins('move.w', '2(%a0,%d1.w),0xf640:w', 6)
    e.ins('move.w', '(%a0,%d1.w),0xf642:w', 6)
    e.ins('jsr', 'build_path:l', 6)
    e.ins('move.w', '#522,0xf612:w', 6)
    e.ins('move.w', '#1,0xf362:w', 6)
    e.ins('clr.w', '0xceac:w', 4)


def _ensure_neighbor(e, rules):
    cap = rules['group_capacity']
    collect, done, first, favorable, marked, second, exhausted = (
        e.fresh(n) for n in ('collect', 'done', 'first', 'favorable', 'marked', 'second', 'exhausted'))
    e.ins('bsr.w', 'selected_roster_capacity', 4)
    e.ins('move.w', '0xf6d6:w,%d0', 4)
    e.ins('andi.w', '#3,%d0', 4)
    e.ins('lsl.w', '#1,%d0')
    e.ins('lea.l', '0xf6e8:w,%a6', 4)
    e.ins('adda.w', '%d0,%a6')
    e.ins('lsl.w', '#1,%d0')
    e.ins('movea.l', '-40(%pc,%d0.w),%a5', 4)
    e.ins('move.w', '(%a5),%d7')
    e.ins('tst.w', '(%a6)')
    e.ins('bmi.w', collect, 4)
    e.ins('move.w', '(%a6),%d0')
    e.ins('bsr.w', 'find_group_at_coordinate', 4)
    e.ins('move.b', '(%a0),%d0')
    e.ins('andi.b', '#15,%d0', 4)
    e.ins('add.b', '%d6,%d0')
    e.ins('cmpi.b', f'#{cap},%d0', 4)
    e.ins('bls.w', done, 4)
    e.label(collect)
    e.ins('bsr.w', 'collect_six_neighbor_candidates', 4)
    e.ins('bsr.w', 'filter_neighbor_candidates', 4)
    e.ins('tst.w', '%d3')
    e.ins('beq.w', done, 4)
    e.ins('move.w', '%d3,%d2')
    e.ins('subq.w', '#1,%d2')
    e.ins('lea.l', '0xa954:w,%a0', 4)
    e.label(first)
    e.ins('move.w', '(%a0)+,%d0')
    e.ins('bpl.b', favorable)
    e.ins('dbra', '%d2,' + first, 4)
    e.ins('lea.l', '0xa954:w,%a1', 4)
    e.ins('subq.w', '#1,%d3')
    e.label(second)
    e.ins('move.w', '(%a1)+,%d0')
    e.ins('andi.w', '#32767,%d0', 4)
    e.ins('bsr.w', 'find_group_at_coordinate', 4)
    e.ins('move.b', '(%a0),%d1')
    e.ins('andi.b', '#15,%d1', 4)
    e.ins('add.b', '%d6,%d1')
    e.ins('cmpi.b', f'#{cap},%d1', 4)
    e.ins('bls.w', favorable, 4)
    e.ins('dbra', '%d3,' + second, 4)
    e.label(exhausted)
    e.ins('move.w', '#65535,(%a6)', 4)
    e.ins('bra.w', done, 4)
    e.label(favorable)
    e.ins('move.w', '%d0,(%a6)')
    e.label(done)


def _find_group(e, rules):
    loop, following, done = (e.fresh(n) for n in ('loop', 'following', 'done'))
    e.ins('clr.w', '%d1')
    e.ins('move.b', '%d0,%d1')
    e.ins('lsr.w', '#8,%d0')
    e.ins('lea.l', '0x9000:w,%a0', 4)
    e.label(loop)
    e.ins('move.b', '(%a0),%d2')
    e.ins('andi.w', '#15,%d2', 4)
    e.ins('beq.w', done, 4)
    e.ins('cmp.b', '1(%a0),%d0', 4)
    e.ins('bne.w', following, 4)
    e.ins('cmp.b', '2(%a0),%d1', 4)
    e.ins('beq.w', done, 4)
    e.label(following)
    e.ins('lea.l', '13(%a0,%d2.w),%a0', 4)
    e.ins('bra.b', loop)
    e.label(done)


def _collect_neighbors(e, rules):
    e.ins('lea.l', '0xa954:w,%a0', 4)
    e.ins('clr.w', '%d3')
    e.ins('move.w', '0xf68a:w,%d2', 4)
    e.ins('lsl.w', '#2,%d2')
    e.ins('lea.l', '0xd4ac6:l,%a1', 6)
    e.ins('move.w', '2(%a1,%d2.w),%d0', 4)
    e.ins('lsr.w', '#4,%d0')
    e.ins('move.w', '(%a1,%d2.w),%d1', 4)
    e.ins('lsr.w', '#4,%d1')
    e.ins('subq.w', '#1,%d0')
    e.ins('subq.w', '#1,%d1')
    for dx, dy in ((0, 0), (0, 1), (1, 1), (1, -1), (0, -1), (-1, -1)):
        for delta, target in ((dx, '%d0'), (dy, '%d1')):
            if delta:
                e.ins('addq.w' if delta > 0 else 'subq.w', '#1,' + target)
        following = e.fresh('next_neighbor')
        e.ins('jsr', 'read_neighbor_source_cost(%pc)', 4)
        e.ins('nop')
        e.ins('bmi.b', following)
        e.ins('move.b', '%d0,%d2')
        e.ins('lsl.w', '#8,%d2')
        e.ins('move.b', '%d1,%d2')
        e.ins('move.w', '%d2,(%a0)+')
        e.ins('addq.w', '#1,%d3')
        e.label(following)


def _filter_neighbors(e, rules):
    loop, done, scan, match, marked, advance, shift = (
        e.fresh(n) for n in ('loop', 'done', 'scan', 'match', 'marked', 'advance', 'shift'))
    e.ins('lea.l', '0x9000:w,%a0', 4)
    e.ins('lea.l', '0xa952:w,%a1', 4)
    e.label(loop)
    e.ins('move.b', '(%a0),%d0')
    e.ins('andi.w', '#15,%d0', 4)
    e.ins('beq.w', done, 4)
    e.ins('move.b', '1(%a0),%d1', 4)
    e.ins('lsl.w', '#8,%d1')
    e.ins('move.b', '2(%a0),%d1', 4)
    e.ins('move.w', '%d3,%d2')
    e.ins('lsl.w', '#1,%d2')
    e.label(scan)
    e.ins('cmp.w', '(%a1,%d2.w),%d1', 4)
    e.ins('beq.w', match, 4)
    e.ins('subq.w', '#2,%d2')
    e.ins('bne.b', scan)
    e.ins('bra.w', advance, 4)
    e.label(match)
    e.ins('move.b', '4(%a0),%d1', 4)
    e.ins('cmp.b', '%d7,%d1')
    e.ins('beq.b', marked)
    e.ins('subq.w', '#1,%d3')
    e.ins('beq.w', done, 4)
    e.ins('move.w', '%d3,%d4')
    e.ins('lsl.w', '#1,%d4')
    e.label(shift)
    e.ins('move.w', '2(%a1,%d2.w),(%a1,%d2.w)', 6)
    e.ins('addq.w', '#2,%d2')
    e.ins('cmp.w', '%d4,%d2')
    e.ins('bcs.b', shift)
    e.ins('bra.w', advance, 4)
    e.label(marked)
    e.ins('ori.w', '#32768,(%a1,%d2.w)', 6)
    e.label(advance)
    e.ins('lea.l', '13(%a0,%d0.w),%a0', 4)
    e.ins('bra.b', loop)
    e.label(done)


def _selected_capacity(e, rules):
    cap = rules['selected_capacity']
    single, city, first, second, done, count = (
        e.fresh(n) for n in ('single', 'city', 'first', 'second', 'done', 'count'))
    e.ins('btst.b', '#0,0xf6d7:w', 6)
    e.ins('bne.w', single, 4)
    e.ins('btst.b', '#1,0xf6d7:w', 6)
    e.ins('bne.w', city, 4)
    e.ins('lea.l', '0xa027:w,%a0', 4)
    e.ins('move.w', '0xf68a:w,%d0', 4)
    e.ins('clr.w', '%d1')
    e.ins('move.b', '(%a0,%d0.w),%d1', 4)
    e.ins('cmp.w', '0xf3a6:w,%d1', 4)
    e.ins('bne.w', single, 4)
    e.ins('lea.l', '0xa550:w,%a0', 4)
    e.ins('lea.l', '0xa57a:w,%a6', 4)
    e.label(count)
    e.ins('clr.w', '%d6')
    e.label(first)
    e.ins('tst.w', '(%a0)+')
    e.ins('bmi.w', second, 4)
    e.ins('addq.w', '#1,%d6')
    e.ins('bra.b', first)
    e.label(second)
    second_next = e.fresh('second_next')
    e.ins('tst.w', '(%a6)+')
    e.ins('bmi.w', second_next, 4)
    e.ins('addq.w', '#1,%d6')
    e.ins('bra.b', second)
    e.label(second_next)
    e.ins('cmpi.w', f'#{cap},%d6', 4)
    e.ins('bls.w', done, 4)
    e.ins('move.w', f'#{cap},%d6', 4)
    e.ins('bra.w', done, 4)
    e.label(city)
    e.ins('lea.l', '0xf45e:w,%a0', 4)
    e.ins('move.w', '0xf68a:w,%d0', 4)
    e.ins('lsl.w', '#1,%d0')
    e.ins('move.w', '(%a0,%d0.w),%d1', 4)
    e.ins('cmp.w', '0xf3a6:w,%d1', 4)
    e.ins('bne.w', single, 4)
    e.ins('lea.l', '0xa5a4:w,%a0', 4)
    e.ins('lea.l', '0xa5ce:w,%a6', 4)
    e.ins('bra.b', count)
    e.label(single)
    e.ins('move.w', '#1,%d6', 4)
    e.label(done)


def _neighbor_cost(e, rules):
    e.ins('move.w', '%d0,%d4')
    e.ins('move.w', '%d4,%d2')
    e.ins('lsl.w', '#3,%d2')
    e.ins('add.w', '%d2,%d4')
    e.ins('lsl.w', '#3,%d4')
    e.ins('add.w', '%d1,%d4')
    e.ins('lea.l', '0xee5f0:l,%a2', 6)
    e.ins('clr.w', '%d2')
    e.ins('move.b', '(%a2,%d4.w),%d2', 4)
    e.ins('lea.l', '0x670a:l,%a2', 6)
    e.ins('move.b', '(%a2,%d4.w),%d2', 4)


def _build_ai_packet(e, rules):
    e.ins('move.w', '0xf746:w,0xf63c:w', 6)
    e.ins('move.w', '0xf748:w,0xf63e:w', 6)
    e.ins('lea.l', '0xd4ac6:l,%a0', 6)
    e.ins('move.w', '0xf392:w,%d0', 4)
    e.ins('lsl.w', '#2,%d0')
    e.ins('move.w', '2(%a0,%d0.w),0xf640:w', 6)
    e.ins('move.w', '(%a0,%d0.w),0xf642:w', 6)
    e.ins('jsr', 'build_path:l', 6)
    e.ins('lea.l', '0xff3000:l,%a0', 6)
    e.ins('adda.w', '0xff3826:l,%a0', 6)
    e.ins('clr.b', '(%a0)+')
    e.ins('move.b', '0xf74b:w,(%a0)+', 4)
    e.ins('move.b', '0xf745:w,(%a0)+', 4)
    e.ins('bsr.w', 'append_ai_path_steps', 4)


def _append_steps(e, rules):
    loop, done = (e.fresh(n) for n in ('loop', 'done'))
    e.ins('move.w', '0xf744:w,%d0', 4)
    e.ins('move.w', '0xf746:w,%d1', 4)
    e.ins('lsr.w', '#4,%d1')
    e.ins('move.w', '0xf748:w,%d2', 4)
    e.ins('lsr.w', '#4,%d2')
    e.ins('move.w', '#4,%d6', 4)
    e.ins('lea.l', '0xee5f0:l,%a3', 6)
    e.ins('lea.l', '0x670a:l,%a4', 6)
    e.ins('lea.l', '0xff4000:l,%a1', 6)
    e.label(loop)
    e.ins('move.b', '(%a1)+,%d3')
    e.ins('bmi.w', done, 4)
    e.ins('lea.l', '44(%pc),%a2', 4)
    e.ins('lsl.w', '#2,%d3')
    e.ins('add.w', '(%a2,%d3.w),%d1', 4)
    e.ins('add.w', '2(%a2,%d3.w),%d2', 4)
    e.ins('lsr.w', '#2,%d3')
    e.ins('bsr.w', 'read_path_step_cost', 4)
    e.ins('sub.b', '%d4,%d0')
    e.ins('bcs.w', done, 4)
    e.ins('addq.w', '#1,%d6')
    e.ins('move.b', '%d3,(%a0)+')
    e.ins('tst.b', '%d0')
    e.ins('bne.b', loop)
    e.label(done)
    e.ins('clr.b', '(%a0)')
    e.ins('move.b', '#255,1(%a0)', 6)
    e.ins('add.w', '%d6,0xff3826:l', 6)


def _step_cost(e, rules):
    e.ins('move.w', '%d1,%d4')
    e.ins('lsl.w', '#3,%d4')
    e.ins('add.w', '%d1,%d4')
    e.ins('lsl.w', '#3,%d4')
    e.ins('add.w', '%d2,%d4')
    e.ins('clr.w', '%d5')
    e.ins('move.b', '(%a3,%d4.w),%d5', 4)
    e.ins('move.b', '(%a4,%d5.w),%d4', 4)


def _choose_destination(e, rules):
    loop, next_city, x_distance, y_distance = (
        e.fresh(n) for n in ('loop', 'next_city', 'x_distance', 'y_distance'))
    e.ins('lea.l', '0x9000:w,%a0', 4)
    e.ins('adda.w', '0xf75a:w,%a0', 4)
    e.ins('clr.w', '%d0')
    e.ins('move.b', '3(%a0),%d0', 4)
    e.ins('clr.w', '%d1')
    e.ins('move.b', '1(%a0),%d1', 4)
    e.ins('lsl.w', '#4,%d1')
    e.ins('move.w', '%d1,0xf63c:w', 4)
    e.ins('lsr.w', '#4,%d1')
    e.ins('clr.w', '%d2')
    e.ins('move.b', '2(%a0),%d2', 4)
    e.ins('lsl.w', '#4,%d2')
    e.ins('move.w', '%d2,0xf63e:w', 4)
    e.ins('lsr.w', '#4,%d2')
    e.ins('lea.l', '0xf428:w,%a1', 4)
    e.ins('lea.l', '0xd4aca:l,%a2', 6)
    e.ins('move.w', '#39,%d3', 4)
    e.ins('move.w', '#65535,%d7', 4)
    e.ins('move.w', '#65535,0xf392:w', 6)
    e.label(loop)
    e.ins('clr.w', '%d4')
    e.ins('move.b', '(%a1,%d3.w),%d4', 4)
    e.ins('cmp.w', '0xf376:w,%d4', 4)
    e.ins('bne.w', next_city, 4)
    e.ins('bsr.w', 'city_roster_full_carry', 4)
    e.ins('bcs.w', next_city, 4)
    e.ins('move.w', '%d3,%d4')
    e.ins('lsl.w', '#2,%d4')
    e.ins('move.w', '2(%a2,%d4.w),%d5', 4)
    e.ins('move.w', '%d5,0xf640:w', 4)
    e.ins('lsr.w', '#4,%d5')
    e.ins('sub.w', '%d1,%d5')
    e.ins('bcc.w', x_distance, 4)
    e.ins('neg.w', '%d5')
    e.label(x_distance)
    e.ins('cmp.w', '%d0,%d5')
    e.ins('bhi.w', next_city, 4)
    e.ins('move.w', '(%a2,%d4.w),%d6', 4)
    e.ins('move.w', '%d6,0xf642:w', 4)
    e.ins('lsr.w', '#4,%d6')
    e.ins('sub.w', '%d2,%d6')
    e.ins('bcc.w', y_distance, 4)
    e.ins('neg.w', '%d6')
    e.label(y_distance)
    e.ins('add.w', '%d6,%d5')
    e.ins('cmp.w', '%d0,%d5')
    e.ins('bhi.w', next_city, 4)
    e.ins('movem.l', '%d0-%d3/%d7,-(%a7)', 4)
    e.ins('jsr', 'build_path:l', 6)
    e.ins('movem.l', '(%a7)+,%d0-%d3/%d7', 4)
    e.ins('cmp.w', '0xf644:w,%d7', 4)
    e.ins('bls.w', next_city, 4)
    e.ins('move.w', '0xf644:w,%d7', 4)
    e.ins('move.w', '%d3,0xf392:w', 4)
    e.label(next_city)
    e.ins('dbra', '%d3,' + loop, 4)


def _city_full(e, rules):
    loop, full, done = (e.fresh(n) for n in ('loop', 'full', 'done'))
    e.ins('movem.l', '%d0-%d2/%a0,-(%a7)', 4)
    e.ins('lea.l', '0xcc00:w,%a0', 4)
    e.ins('move.w', '%d3,%d0')
    e.ins('addq.w', '#1,%d0')
    e.ins('move.w', '#255,%d1', 4)
    e.ins('clr.w', '%d2')
    e.label(loop)
    e.ins('cmp.b', '(%a0,%d1.w),%d0', 4)
    e.ins('bne.w', full, 4)
    e.ins('addq.w', '#1,%d2')
    e.label(full)
    e.ins('dbra', '%d1,' + loop, 4)
    e.ins('cmpi.w', f"#{rules['city_capacity']},%d2", 4)
    set_full = e.fresh('set_full')
    e.ins('bcc.w', set_full, 4)
    e.ins('movem.l', '(%a7)+,%d0-%d2/%a0', 4)
    e.ins('andi.w', '#65534,%sr', 4)
    e.ins('bra.w', done, 4)
    e.label(set_full)
    e.ins('movem.l', '(%a7)+,%d0-%d2/%a0', 4)
    e.ins('ori.w', '#1,%sr', 4)
    e.label(done)


LOWERERS = {
    'prepare_transport_path': _prepare_transport,
    'ensure_neighbor_capacity': _ensure_neighbor,
    'find_group_at_coordinate': _find_group,
    'collect_six_neighbor_candidates': _collect_neighbors,
    'filter_neighbor_candidates': _filter_neighbors,
    'selected_roster_capacity': _selected_capacity,
    'read_neighbor_source_cost': _neighbor_cost,
    'build_ai_movement_packet': _build_ai_packet,
    'append_ai_path_steps': _append_steps,
    'read_path_step_cost': _step_cost,
    'choose_ai_destination': _choose_destination,
    'city_roster_full_carry': _city_full,
}


def compile_campaign(source):
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    result = lower_declared(records, CAMPAIGN_BINDINGS, LOWERERS)
    if (result['allocated_bytes'], result['instructions'], len(result['units'])) != (1132, 355, 12):
        raise CompileError('complete twelve-body campaign allocation required')
    result['assembly'] = '.cpu 68000\n.text\n' + '\n'.join(u['assembly'] for u in result['units'])
    result['effects'] = {name: record['effects'] for name, record in records.items()}
    return result
