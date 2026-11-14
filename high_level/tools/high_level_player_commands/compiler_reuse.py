"""Draft restricted semantic frontend and ordinary GNU target lowering.

Generated development draft; Python rules remain in business_reuse.
Only these explicit structural forms and declared literal rules are admitted.
Not a general Python compiler or a complete CPU equivalence proof.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import REUSED_BINDINGS

APPROVED = {'domain': {'Byte',
            'GameState',
            'Table',
            'Word',
            'checked_state',
            'checked_table',
            'low8',
            'read_packed_long',
            'store_packed_long_reverse',
            'u16',
            'u32',
            'uint'}}

DECLARATIONS = {'add_selected_cost': {'signature': 'state: GameState',
                       'returns': 'None',
                       'flow': 'checked_state(state)\n'
                               "selected = u16(state.scalar('amount_place') << 2)\n"
                               'total = state.command_value_steps.long(selected)\n'
                               "total = u32(total + state.scalar('selected_amount'))\n"
                               "if total <= state.scalar('amount_limit'):\n"
                               "    state.set_scalar('selected_amount', total)"},
 'terrain_cell_query': {'signature': 'state: GameState, row: Word, column: Word',
                        'returns': 'tuple',
                        'flow': 'checked_state(state)\n'
                                'uint(row, 16)\n'
                                'uint(column, 16)\n'
                                'index = u16(u16(row * 72) + column)\n'
                                'terrain = state.terrain_cells.byte(index)\n'
                                'return (terrain, state.terrain_costs.byte(terrain))'},
 'collect_blocked_cargo': {'signature': 'state: GameState, obstacle: Table',
                           'returns': 'None',
                           'flow': 'checked_state(state)\n'
                                   'checked_table(obstacle, state)\n'
                                   "cargo = state.table(state.scalar('active_descriptor'))\n"
                                   'kind = obstacle.byte() & 3\n'
                                   'if kind != 2:\n'
                                   '    amount = u32(read_packed_long(cargo, 5) + 10000)\n'
                                   '    if amount > 999999:\n'
                                   '        amount = 999999\n'
                                   '    store_packed_long_reverse(cargo, 5, amount)\n'
                                   '    if kind != 3:\n'
                                   '        obstacle.set_byte(0, 0)\n'
                                   '    else:\n'
                                   '        obstacle.set_byte(0, obstacle.byte() & 128)\n'
                                   '        obstacle.set_byte(0, obstacle.byte() | 2)\n'
                                   'else:\n'
                                   '    amount = u32(read_packed_long(cargo, 9) + 10000)\n'
                                   '    if amount > 999999:\n'
                                   '        amount = 99999\n'
                                   '    store_packed_long_reverse(cargo, 9, amount)\n'
                                   '    obstacle.set_byte(0, 0)',
                           'slots': {10000: ('pickup_amount', 0, 65535),
                                     999999: ('resource_cap', 0, 2147483647),
                                     99999: ('rice_overflow_value', 0, 2147483647)}}}

def _lower_add_selected_cost(e, rules):
    e.label('player_pc_012a0c')
    e.ins('move.w', '0xf39a:w,%d1', 4)
    e.label('player_pc_012a10')
    e.ins('lsl.w', '#0x2,%d1', 2)
    e.label('player_pc_012a12')
    e.ins('lea.l', '2616(%pc),%a0', 4)
    e.label('player_pc_012a16')
    e.ins('nop', '', 2)
    e.label('player_pc_012a18')
    e.ins('move.l', '(%a0, %d1.w),%d1', 4)
    e.label('player_pc_012a1c')
    e.ins('add.l', '0xf3f4:w,%d1', 4)
    e.label('player_pc_012a20')
    e.ins('cmp.l', '0xf3f8:w,%d1', 4)
    e.label('player_pc_012a24')
    e.ins('bhi.w', 'player_pc_012a2c', 4)
    e.label('player_pc_012a28')
    e.ins('move.l', '%d1,0xf3f4:w', 4)
    e.label('player_pc_012a2c')
    e.ins('rts', '', 2)

def _lower_terrain_cell_query(e, rules):
    e.label('player_pc_0142a2')
    e.ins('move.l', '%d0,-(%a7)', 2)
    e.label('player_pc_0142a4')
    e.ins('move.w', '%d0,%d2', 2)
    e.label('player_pc_0142a6')
    e.ins('lsl.w', '#0x3,%d2', 2)
    e.label('player_pc_0142a8')
    e.ins('add.w', '%d2,%d0', 2)
    e.label('player_pc_0142aa')
    e.ins('lsl.w', '#0x3,%d0', 2)
    e.label('player_pc_0142ac')
    e.ins('add.w', '%d1,%d0', 2)
    e.label('player_pc_0142ae')
    e.ins('lea.l', '0xee5f0:l,%a2', 6)
    e.label('player_pc_0142b4')
    e.ins('clr.w', '%d2', 2)
    e.label('player_pc_0142b6')
    e.ins('move.b', '(%a2, %d0.w),%d2', 4)
    e.label('player_pc_0142ba')
    e.ins('lea.l', '0x670a:l,%a2', 6)
    e.label('player_pc_0142c0')
    e.ins('clr.w', '%d3', 2)
    e.label('player_pc_0142c2')
    e.ins('move.b', '(%a2, %d2.w),%d3', 4)
    e.label('player_pc_0142c6')
    e.ins('move.l', '(%a7)+,%d0', 2)
    e.label('player_pc_0142c8')
    e.ins('rts', '', 2)

def _lower_collect_blocked_cargo(e, rules):
    e.label('player_pc_0154c8')
    e.ins('movea.l', '0xff382c:l,%a1', 6)
    e.label('player_pc_0154ce')
    e.ins('move.b', '(%a0),%d0', 2)
    e.label('player_pc_0154d0')
    e.ins('andi.w', '#0x3,%d0', 4)
    e.label('player_pc_0154d4')
    e.ins('cmpi.b', '#0x2,%d0', 4)
    e.label('player_pc_0154d8')
    e.ins('beq.b', 'player_pc_01552e', 2)
    e.label('player_pc_0154da')
    e.ins('move.b', '0x5(%a1),%d1', 4)
    e.label('player_pc_0154de')
    e.ins('lsl.w', '#0x8,%d1', 2)
    e.label('player_pc_0154e0')
    e.ins('move.b', '0x6(%a1),%d1', 4)
    e.label('player_pc_0154e4')
    e.ins('lsl.l', '#0x8,%d1', 2)
    e.label('player_pc_0154e6')
    e.ins('move.b', '0x7(%a1),%d1', 4)
    e.label('player_pc_0154ea')
    e.ins('lsl.l', '#0x8,%d1', 2)
    e.label('player_pc_0154ec')
    e.ins('move.b', '0x8(%a1),%d1', 4)
    e.label('player_pc_0154f0')
    e.ins('addi.l', '#'+hex(rules['pickup_amount'])+',%d1', 6)
    e.label('player_pc_0154f6')
    e.ins('cmpi.l', '#'+hex(rules['resource_cap'])+',%d1', 6)
    e.label('player_pc_0154fc')
    e.ins('bls.b', 'player_pc_015504', 2)
    e.label('player_pc_0154fe')
    e.ins('move.l', '#'+hex(rules['resource_cap'])+',%d1', 6)
    e.label('player_pc_015504')
    e.ins('move.b', '%d1,0x8(%a1)', 4)
    e.label('player_pc_015508')
    e.ins('lsr.l', '#0x8,%d1', 2)
    e.label('player_pc_01550a')
    e.ins('move.b', '%d1,0x7(%a1)', 4)
    e.label('player_pc_01550e')
    e.ins('lsr.l', '#0x8,%d1', 2)
    e.label('player_pc_015510')
    e.ins('move.b', '%d1,0x6(%a1)', 4)
    e.label('player_pc_015514')
    e.ins('lsr.w', '#0x8,%d1', 2)
    e.label('player_pc_015516')
    e.ins('move.b', '%d1,0x5(%a1)', 4)
    e.label('player_pc_01551a')
    e.ins('cmpi.b', '#0x3,%d0', 4)
    e.label('player_pc_01551e')
    e.ins('beq.b', 'player_pc_015524', 2)
    e.label('player_pc_015520')
    e.ins('clr.b', '(%a0)', 2)
    e.label('player_pc_015522')
    e.ins('bra.b', 'player_pc_015570', 2)
    e.label('player_pc_015524')
    e.ins('andi.b', '#0x80,(%a0)', 4)
    e.label('player_pc_015528')
    e.ins('ori.b', '#0x2,(%a0)', 4)
    e.label('player_pc_01552c')
    e.ins('bra.b', 'player_pc_015570', 2)
    e.label('player_pc_01552e')
    e.ins('move.b', '0x9(%a1),%d1', 4)
    e.label('player_pc_015532')
    e.ins('lsl.w', '#0x8,%d1', 2)
    e.label('player_pc_015534')
    e.ins('move.b', '0xa(%a1),%d1', 4)
    e.label('player_pc_015538')
    e.ins('lsl.l', '#0x8,%d1', 2)
    e.label('player_pc_01553a')
    e.ins('move.b', '0xb(%a1),%d1', 4)
    e.label('player_pc_01553e')
    e.ins('lsl.l', '#0x8,%d1', 2)
    e.label('player_pc_015540')
    e.ins('move.b', '0xc(%a1),%d1', 4)
    e.label('player_pc_015544')
    e.ins('addi.l', '#'+hex(rules['pickup_amount'])+',%d1', 6)
    e.label('player_pc_01554a')
    e.ins('cmpi.l', '#'+hex(rules['resource_cap'])+',%d1', 6)
    e.label('player_pc_015550')
    e.ins('bls.b', 'player_pc_015558', 2)
    e.label('player_pc_015552')
    e.ins('move.l', '#'+hex(rules['rice_overflow_value'])+',%d1', 6)
    e.label('player_pc_015558')
    e.ins('move.b', '%d1,0xc(%a1)', 4)
    e.label('player_pc_01555c')
    e.ins('lsr.l', '#0x8,%d1', 2)
    e.label('player_pc_01555e')
    e.ins('move.b', '%d1,0xb(%a1)', 4)
    e.label('player_pc_015562')
    e.ins('lsr.l', '#0x8,%d1', 2)
    e.label('player_pc_015564')
    e.ins('move.b', '%d1,0xa(%a1)', 4)
    e.label('player_pc_015568')
    e.ins('lsr.w', '#0x8,%d1', 2)
    e.label('player_pc_01556a')
    e.ins('move.b', '%d1,0x9(%a1)', 4)
    e.label('player_pc_01556e')
    e.ins('clr.b', '(%a0)', 2)
    e.label('player_pc_015570')
    e.ins('rts', '', 2)

LOWERERS = {
    'add_selected_cost':_lower_add_selected_cost,
    'terrain_cell_query':_lower_terrain_cell_query,
    'collect_blocked_cargo':_lower_collect_blocked_cargo,
}

def compile_reuse(source):
    records = semantic_functions(source, DECLARATIONS, APPROVED)
    return lower_declared({b.name:records[b.name] for b in REUSED_BINDINGS}, REUSED_BINDINGS, LOWERERS)
