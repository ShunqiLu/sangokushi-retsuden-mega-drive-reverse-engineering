"""Three already-recovered leaf rules, adapted to the player-command live ports.

Their 244 original target bytes are reuse, never new recovery coverage.
"""
from .domain import (
    GameState, Word, Byte, Table, checked_state, checked_table, uint,
    u16, u32, low8, read_packed_long, store_packed_long_reverse,
)


def add_selected_cost(state: GameState) -> None:
    checked_state(state)
    selected = u16(state.scalar('amount_place') << 2)
    total = state.command_value_steps.long(selected)
    total = u32(total + state.scalar('selected_amount'))
    if total <= state.scalar('amount_limit'):
        state.set_scalar('selected_amount', total)


def terrain_cell_query(state: GameState, row: Word, column: Word) -> tuple:
    checked_state(state)
    uint(row, 16)
    uint(column, 16)
    index = u16(u16(row * 72) + column)
    terrain = state.terrain_cells.byte(index)
    return terrain, state.terrain_costs.byte(terrain)


def collect_blocked_cargo(state: GameState, obstacle: Table) -> None:
    checked_state(state)
    checked_table(obstacle, state)
    cargo = state.table(state.scalar('active_descriptor'))
    kind = obstacle.byte() & 3
    if kind != 2:
        amount = u32(read_packed_long(cargo, 5) + 10000)
        if amount > 999999:
            amount = 999999
        store_packed_long_reverse(cargo, 5, amount)
        if kind != 3:
            obstacle.set_byte(0, 0)
        else:
            obstacle.set_byte(0, obstacle.byte() & 128)
            obstacle.set_byte(0, obstacle.byte() | 2)
    else:
        amount = u32(read_packed_long(cargo, 9) + 10000)
        if amount > 999999:
            amount = 99999
        store_packed_long_reverse(cargo, 9, amount)
        obstacle.set_byte(0, 0)
