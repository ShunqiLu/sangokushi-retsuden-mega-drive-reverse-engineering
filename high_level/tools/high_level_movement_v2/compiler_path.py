"""Typed path effects lowered to ordinary MC68000 operations.

Semantic declarations describe complete executable flows. Fixed ABI/layout
instruction selection is finite, not an opcode or original-source payload.
"""
from .compiler_common import semantic_functions,Emitter,CompileError
from .target import PATH_BINDINGS

DECLARATIONS={
 "build_path": {
  "signature": "state:GameState",
  "returns": "PathResult",
  "flow": "checked_state(state)\nnormalize_path_coordinates(state)\nreturn build_path_from_cells(state)"
 },
 "build_path_from_cells": {
  "signature": "state:GameState",
  "returns": "PathResult",
  "flow": "checked_state(state)\ninitialize_path_grid(state)\nfirst_buffer = state.path_frontier\nsecond_buffer = state.alternate_frontier\nsource = first_buffer.cursor()\nsource.append_byte(state.path_source_first_tail())\nsource.append_byte(state.path_source_second_tail())\nsource.append_byte(1)\nsource.append_byte(255)\nlength = u16(0)\nretained_direction = u16(0)\nwhile True:\n    source = first_buffer.cursor()\n    output = second_buffer.cursor()\n    outcome = expand_path_frontier(state, source, output, retained_direction)\n    retained_direction = outcome.retained_direction\n    if outcome.carry == 1:\n        break\n    first_buffer, second_buffer = (second_buffer, first_buffer)\n    length = u16(length + 1)\nlength = u16(length + 1)\nstate.set_path_length(length)\ncoordinates = reconstruct_path(state)\nreturn PathResult(length, retained_direction, coordinates, output, state.path_grid)"
 },
 "initialize_path_grid": {
  "signature": "state:GameState",
  "returns": "None",
  "flow": "checked_state(state)\ngrid = state.path_grid.cursor()\nterrain = state.terrain_sources.cursor()\ncosts = state.terrain_costs\nfor remaining in descending_inclusive(u16(5183)):\n    terrain_kind = u16(terrain.next_byte())\n    cost = u16(costs.byte(terrain_kind))\n    grid.append_word(cost)\ngrid = state.path_grid\nobjects = state.transport_records\nfor remaining in descending_inclusive(u16(39)):\n    if objects.byte() != 0:\n        if objects.byte() & 16 == 0:\n            first = u16(objects.byte(0, 1))\n            offset = u16(u16(u16(first << 3) + first) << 3)\n            second = u16(objects.byte(0, 2))\n            offset = u16(u16(offset + second) << 1)\n            grid.set_word(offset, 127)\n    objects = objects.advance(4)\nobjects = state.group_packets\nwhile True:\n    size = u16(objects.byte() & 15)\n    if size == 0:\n        break\n    first = u16(objects.byte(0, 1))\n    offset = u16(u16(u16(first << 3) + first) << 3)\n    second = u16(objects.byte(0, 2))\n    offset = u16(u16(offset + second) << 1)\n    grid.set_word(offset, 127)\n    objects = objects.at(size, 13)\ncoordinates = state.following_city_coordinates.cursor()\nfor remaining in descending_inclusive(u16(39)):\n    first = u16(coordinates.next_word() >> 4)\n    second = u16(coordinates.next_word() >> 4)\n    offset = u16(u16(u16(second << 3) + second) << 3)\n    offset = u16(u16(offset + first) << 1)\n    grid.set_word(offset, 255, -2)\n    grid.set_word(offset, 255)"
 },
 "normalize_path_coordinates": {
  "signature": "state:GameState",
  "returns": "None",
  "flow": "checked_state(state)\nstate.set_path_destination_first(u16(state.path_destination_first() >> 4))\nstate.set_path_destination_second(u16(state.path_destination_second() >> 4))\nstate.set_path_source_first(u16(state.path_source_first() >> 4))\nstate.set_path_source_second(u16(state.path_source_second() >> 4))"
 },
 "expand_path_frontier": {
  "signature": "state:GameState, source:Cursor, output:Cursor, retained_direction:Word",
  "returns": "FrontierResult",
  "flow": "checked_state(state)\nchecked_cursor(source, state)\nchecked_cursor(output, state)\nretained_direction = uint(retained_direction, 16)\nwhile True:\n    first = u16(source.next_byte())\n    second = u16(source.next_byte())\n    countdown = u8(source.next_byte() - 1)\n    if countdown != 0:\n        output.append_byte(low8(first))\n        output.append_byte(low8(second))\n        output.append_byte(countdown)\n    else:\n        borrowed = first == 0\n        first = u16(first - 1)\n        if not borrowed:\n            retained_direction = u16(3)\n            outcome = visit_path_neighbor(state, first, second, retained_direction, output)\n            first, second = (outcome.coordinates.first, outcome.coordinates.second)\n            if outcome.carry == 1:\n                return FrontierResult(1, retained_direction, PathCoordinates(first, second))\n        first = u16(first + 1)\n        borrowed = second == 0\n        second = u16(second - 1)\n        if not borrowed:\n            retained_direction = u16(2)\n            outcome = visit_path_neighbor(state, first, second, retained_direction, output)\n            first, second = (outcome.coordinates.first, outcome.coordinates.second)\n            if outcome.carry == 1:\n                return FrontierResult(1, retained_direction, PathCoordinates(first, second))\n        second = u16(second + 2)\n        if second < 72:\n            retained_direction = u16(4)\n            outcome = visit_path_neighbor(state, first, second, retained_direction, output)\n            first, second = (outcome.coordinates.first, outcome.coordinates.second)\n            if outcome.carry == 1:\n                return FrontierResult(1, retained_direction, PathCoordinates(first, second))\n        first = u16(first + 1)\n        if first < 72:\n            second = u16(second - 1)\n            retained_direction = u16(1)\n            outcome = visit_path_neighbor(state, first, second, retained_direction, output)\n            first, second = (outcome.coordinates.first, outcome.coordinates.second)\n            if outcome.carry == 1:\n                return FrontierResult(1, retained_direction, PathCoordinates(first, second))\n    if negative_byte(source.byte()):\n        break\noutput.set_byte(0, 255)\noutcome = state.carry_result(0)\nreturn FrontierResult(outcome.carry, retained_direction, PathCoordinates(first, second))"
 },
 "visit_path_neighbor": {
  "signature": "state:GameState, first:Word, second:Word, direction:Word, output:Cursor",
  "returns": "NeighborResult",
  "flow": "checked_state(state)\nfirst = uint(first, 16)\nsecond = uint(second, 16)\ndirection = uint(direction, 16)\nchecked_cursor(output, state)\noutcome = path_neighbor_is_goal(state, first, second, direction)\nif outcome.carry == 1:\n    return NeighborResult(outcome.carry, outcome.conditional_sr, PathCoordinates(first, second))\nstored_direction = read_path_direction(state, first, second)\nif low8(stored_direction) == 0:\n    cost = read_path_cost(state, first, second)\n    if not negative_byte(low8(cost)):\n        output.append_byte(low8(first))\n        first = u16(s8(low8(first)))\n        output.append_byte(low8(second))\n        second = u16(s8(low8(second)))\n        output.append_byte(low8(cost))\n        mark_path_direction(state, first, second, direction)\noutcome = state.carry_result(0)\nreturn NeighborResult(outcome.carry, outcome.conditional_sr, PathCoordinates(first, second))"
 },
 "path_neighbor_is_goal": {
  "signature": "state:GameState, first:Word, second:Word, direction:Word",
  "returns": "CarryOutcome",
  "flow": "checked_state(state)\nfirst = uint(first, 16)\nsecond = uint(second, 16)\ndirection = uint(direction, 16)\nif first == state.path_destination_first():\n    if second == state.path_destination_second():\n        mark_path_direction(state, first, second, direction)\n        return state.carry_result(1)\nreturn state.carry_result(0)"
 },
 "mark_path_direction": {
  "signature": "state:GameState, first:Word, second:Word, direction:Word",
  "returns": "None",
  "flow": "checked_state(state)\nfirst = uint(first, 16)\nsecond = uint(second, 16)\ndirection = uint(direction, 16)\noffset = u16(u16(u16(first << 3) + first) << 3)\noffset = u16(u16(offset + second) << 1)\nstate.path_grid.set_byte(offset, low8(direction))"
 },
 "read_path_direction": {
  "signature": "state:GameState, first:Word, second:Word",
  "returns": "Word",
  "flow": "checked_state(state)\nfirst = uint(first, 16)\nsecond = uint(second, 16)\nretained = u16(first << 3)\noffset = u16(u16(retained + first) << 3)\noffset = u16(u16(offset + second) << 1)\nreturn u16(retained & 65280 | state.path_grid.byte(offset))"
 },
 "read_path_cost": {
  "signature": "state:GameState, first:Word, second:Word",
  "returns": "Word",
  "flow": "checked_state(state)\nfirst = uint(first, 16)\nsecond = uint(second, 16)\noffset = u16(u16(u16(first << 3) + first) << 3)\noffset = u16(u16(offset + second) << 1)\nreturn u16(state.path_grid.byte(offset, 1))"
 },
 "reconstruct_path": {
  "signature": "state:GameState",
  "returns": "PathCoordinates",
  "flow": "checked_state(state)\nresult = state.path_frontier.cursor()\nfirst = state.path_destination_first()\nsecond = state.path_destination_second()\nwhile True:\n    direction = read_path_direction(state, first, second)\n    result.append_byte(low8(direction))\n    coordinates = step_back_path(first, second, direction)\n    first, second = (coordinates.first, coordinates.second)\n    if first == state.path_source_first():\n        if second == state.path_source_second():\n            break\nresult.set_byte(0, 255)\nreturn PathCoordinates(first, second)"
 },
 "step_back_path": {
  "signature": "first:Word, second:Word, direction:Word",
  "returns": "PathCoordinates",
  "flow": "first = uint(first, 16)\nsecond = uint(second, 16)\ndirection = uint(direction, 16)\nremaining = u8(low8(direction) - 1)\nif remaining == 0:\n    first = u16(first - 1)\nelse:\n    remaining = u8(remaining - 1)\n    if remaining == 0:\n        second = u16(second + 1)\n    else:\n        remaining = u8(remaining - 1)\n        if remaining == 0:\n            first = u16(first + 1)\n        else:\n            second = u16(second - 1)\nreturn PathCoordinates(first, second)"
 }
}
DECLARATIONS['initialize_path_grid']['slots']={127:('occupied_cell_cost',0,65535)}
APPROVED={'domain':{'GameState','Word','Table','Cursor','PathCoordinates','PathResult','FrontierResult','CarryOutcome','NeighborResult','uint','u8','u16','low8','s8','negative_byte','descending_inclusive','checked_state','checked_cursor'}}

def _build(e,r):
    e.ins('bsr.w','normalize_path_coordinates',4)
    e.lines.append('.global build_path_from_cells');e.label('build_path_from_cells')
    e.ins('bsr.w','initialize_path_grid',4)
    e.ins('lea','0xff4000:l,%a5',6);e.ins('lea','0xff4800:l,%a6',6)
    e.ins('move.b','0xf641:w,(%a5)',4);e.ins('move.b','0xf643:w,1(%a5)',6)
    e.ins('move.b','#1,2(%a5)',6);e.ins('move.b','#0xff,3(%a5)',6)
    e.ins('clr.w','%d5')
    scan,found=e.fresh('frontier'),e.fresh('found')
    e.label(scan);e.ins('movea.l','%a5,%a0');e.ins('movea.l','%a6,%a1')
    e.ins('bsr.w','expand_path_frontier',4);e.ins('bcs.w',found,4)
    e.ins('exg','%a5,%a6');e.ins('addq.w','#1,%d5');e.ins('bra.b',scan)
    e.label(found);e.ins('addq.w','#1,%d5');e.ins('move.w','%d5,0xf644:w',4)
    e.ins('bsr.w','reconstruct_path',4)


def _init(e,r):
    cell,city,next_city,packet,coords=e.fresh('cell'),e.fresh('city'),e.fresh('next_city'),e.fresh('packet'),e.fresh('coordinates')
    e.ins('lea','0xff0000:l,%a0',6);e.ins('lea','0xee5f0:l,%a1',6)
    e.ins('lea',f'{0x670A-(e.pc+2)}(%pc),%a2',4);e.ins('nop')
    e.ins('move.w','#0x143f,%d0',4);e.ins('clr.w','%d1');e.ins('clr.w','%d2')
    e.label(cell);e.ins('move.b','(%a1)+,%d1');e.ins('move.b','(%a2,%d1.w),%d2',4)
    e.ins('move.w','%d2,(%a0)+');e.ins('dbra','%d0,'+cell,4)
    e.ins('lea','0xff0000:l,%a0',6);e.ins('lea','0xce00:w,%a1',4);e.ins('move.w','#39,%d0',4)
    e.label(city);e.ins('tst.b','(%a1)');e.ins('beq.b',next_city)
    e.ins('btst.b','#4,(%a1)',4);e.ins('bne.b',next_city)
    def occupied():
        e.ins('clr.w','%d1');e.ins('move.b','1(%a1),%d1',4);e.ins('move.w','%d1,%d2')
        e.ins('lsl.w','#3,%d1');e.ins('add.w','%d2,%d1');e.ins('lsl.w','#3,%d1')
        e.ins('clr.w','%d2');e.ins('move.b','2(%a1),%d2',4);e.ins('add.w','%d2,%d1');e.ins('lsl.w','#1,%d1')
        e.ins('move.w',f"#{r['occupied_cell_cost']},(%a0,%d1.w)",6)
    occupied();e.label(next_city);e.ins('addq.w','#4,%a1');e.ins('dbra','%d0,'+city,4)
    e.ins('lea','0x9000:w,%a1',4);e.label(packet);e.ins('move.b','(%a1),%d0')
    e.ins('andi.w','#0xf,%d0',4);e.ins('beq.b',coords)
    occupied();e.ins('lea','13(%a1,%d0.w),%a1',4);e.ins('bra.b',packet)
    e.label(coords);e.ins('lea','0xd4aca:l,%a1',6);e.ins('move.w','#39,%d0',4)
    mark=e.fresh('mark_coordinates');e.label(mark);e.ins('move.w','(%a1)+,%d1');e.ins('lsr.w','#4,%d1')
    e.ins('move.w','(%a1)+,%d2');e.ins('lsr.w','#4,%d2');e.ins('move.w','%d2,%d3')
    e.ins('lsl.w','#3,%d2');e.ins('add.w','%d3,%d2');e.ins('lsl.w','#3,%d2');e.ins('add.w','%d1,%d2');e.ins('lsl.w','#1,%d2')
    e.ins('move.w','#0xff,-2(%a0,%d2.w)',6);e.ins('move.w','#0xff,(%a0,%d2.w)',6);e.ins('dbra','%d0,'+mark,4)


def _normalize(e,r):
    for a in (0xf63c,0xf63e,0xf640,0xf642):
        e.ins('move.w',f'0x{a:x}:w,%d0',4);e.ins('lsr.w','#4,%d0');e.ins('move.w',f'%d0,0x{a:x}:w',4)


def _expand(e,r):
    scan,neighbors,first_restored,second_restored,next_first,after_neighbors,done=[e.fresh(n) for n in ('scan','neighbors','first_restored','second_restored','next_first','after_neighbors','done')]
    e.label(scan);e.ins('clr.w','%d0');e.ins('move.b','(%a0)+,%d0');e.ins('clr.w','%d1');e.ins('move.b','(%a0)+,%d1')
    e.ins('move.b','(%a0)+,%d2');e.ins('subq.b','#1,%d2');e.ins('beq.b',neighbors)
    for reg in ('%d0','%d1','%d2'):e.ins('move.b',reg+',(%a1)+')
    e.ins('bra.w',after_neighbors,4);e.label(neighbors)
    e.ins('subq.w','#1,%d0');e.ins('bcs.b',first_restored);e.ins('move.w','#3,%d3',4)
    e.ins('bsr.w','visit_path_neighbor',4);e.ins('bcs.w',done,4)
    e.label(first_restored);e.ins('addq.w','#1,%d0');e.ins('subq.w','#1,%d1');e.ins('bcs.b',second_restored)
    e.ins('move.w','#2,%d3',4);e.ins('bsr.w','visit_path_neighbor',4);e.ins('bcs.w',done,4)
    e.label(second_restored);e.ins('addq.w','#2,%d1');e.ins('cmpi.w','#72,%d1',4);e.ins('bcc.b',next_first)
    e.ins('move.w','#4,%d3',4);e.ins('bsr.w','visit_path_neighbor',4);e.ins('bcs.w',done,4)
    e.label(next_first);e.ins('addq.w','#1,%d0');e.ins('cmpi.w','#72,%d0',4);e.ins('bcc.w',after_neighbors,4)
    e.ins('subq.w','#1,%d1');e.ins('move.w','#1,%d3',4);e.ins('bsr.w','visit_path_neighbor',4);e.ins('bcs.w',done,4)
    e.label(after_neighbors);e.ins('tst.b','(%a0)');e.ins('bpl.b',scan)
    e.ins('move.b','#0xff,(%a1)',4);e.ins('andi.w','#0xfffe,%sr',4);e.label(done)


def _visit(e,r):
    clear,done=e.fresh('clear'),e.fresh('done')
    e.ins('bsr.w','path_neighbor_is_goal',4);e.ins('bcs.w',done,4)
    e.ins('bsr.w','read_path_direction',4);e.ins('tst.b','%d2');e.ins('bne.b',clear)
    e.ins('bsr.w','read_path_cost',4);e.ins('tst.b','%d2');e.ins('bmi.b',clear)
    e.ins('move.b','%d0,(%a1)+');e.ins('ext.w','%d0');e.ins('move.b','%d1,(%a1)+');e.ins('ext.w','%d1')
    e.ins('move.b','%d2,(%a1)+');e.ins('bsr.w','mark_path_direction',4)
    e.label(clear);e.ins('andi.w','#0xfffe,%sr',4);e.label(done)


def _goal(e,r):
    miss=e.fresh('not_goal');e.ins('cmp.w','0xf63c:w,%d0',4);e.ins('bne.b',miss)
    e.ins('cmp.w','0xf63e:w,%d1',4);e.ins('bne.b',miss);e.ins('bsr.w','mark_path_direction',4)
    e.ins('ori.w','#1,%sr',4);e.ins('rts');e.label(miss);e.ins('andi.w','#0xfffe,%sr',4)


def _index(e,target):
    e.ins('move.w',target+',%d2');e.ins('lsl.w','#3,%d2');e.ins('add.w','%d2,'+target)
    e.ins('lsl.w','#3,'+target);e.ins('add.w','%d1,'+target);e.ins('lsl.w','#1,'+target)
    e.ins('lea','0xff0000:l,%a2',6)


def _mark(e,r):
    e.ins('move.l','%d0,-(%sp)');_index(e,'%d0');e.ins('move.b','%d3,(%a2,%d0.w)',4);e.ins('move.l','(%sp)+,%d0')


def _direction(e,r):
    e.ins('move.w','%d0,-(%sp)');_index(e,'%d0');e.ins('move.b','(%a2,%d0.w),%d2',4);e.ins('move.w','(%sp)+,%d0')


def _cost(e,r):
    e.ins('move.w','%d0,%d4');_index(e,'%d4');e.ins('clr.w','%d2');e.ins('move.b','1(%a2,%d4.w),%d2',4)


def _reconstruct(e,r):
    scan,again,done=e.fresh('scan'),e.fresh('again'),e.fresh('done')
    e.ins('lea','0xff4000:l,%a0',6);e.ins('move.w','0xf63c:w,%d0',4);e.ins('move.w','0xf63e:w,%d1',4)
    e.label(scan);e.ins('bsr.b','read_path_direction');e.ins('move.b','%d2,(%a0)+');e.ins('bsr.w','step_back_path',4)
    e.ins('cmp.w','0xf640:w,%d0',4);e.ins('bne.b',again);e.ins('cmp.w','0xf642:w,%d1',4);e.ins('beq.b',done)
    e.label(again);e.ins('bra.b',scan);e.label(done);e.ins('move.b','#0xff,(%a0)',4)


def _step(e,r):
    first,second,third,done=e.fresh('first'),e.fresh('second'),e.fresh('third'),e.fresh('done')
    e.ins('subq.b','#1,%d2');e.ins('beq.w',first,4);e.ins('subq.b','#1,%d2');e.ins('beq.w',second,4)
    e.ins('subq.b','#1,%d2');e.ins('beq.w',third,4);e.ins('subq.w','#1,%d1');e.ins('bra.w',done,4)
    e.label(first);e.ins('subq.w','#1,%d0');e.ins('bra.w',done,4)
    e.label(second);e.ins('addq.w','#1,%d1');e.ins('bra.b',done)
    e.label(third);e.ins('addq.w','#1,%d0');e.label(done)

LOWERERS={'build_path':_build,'initialize_path_grid':_init,'normalize_path_coordinates':_normalize,
 'expand_path_frontier':_expand,'visit_path_neighbor':_visit,'path_neighbor_is_goal':_goal,
 'mark_path_direction':_mark,'read_path_direction':_direction,'read_path_cost':_cost,
 'reconstruct_path':_reconstruct,'step_back_path':_step}

def compile_path(source):
    records=semantic_functions(source,DECLARATIONS,APPROVED)
    units=[]
    for b in PATH_BINDINGS:
        e=Emitter(b);e.begin();record=records[b.name];LOWERERS[b.name](e,record['rules']);e.end()
        if e.pc!=b.end:raise CompileError(b.name+': fixed complete extent changed')
        effects=record['effects']
        if b.name=='build_path':effects+='; alternate651C: '+records['build_path_from_cells']['effects']
        units.append(e.unit(effects))
    return dict(units=units,allocated_bytes=662,instructions=sum(len(u['instructions']) for u in units),original_generation_input=False,complete_CPU=False)


