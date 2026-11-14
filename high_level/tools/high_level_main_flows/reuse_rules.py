"""Existing officer and terrain algorithms adapted to the shared live state.

All target bytes are reuse. Fixed-width operations, live ordering and original
unsigned comparisons remain; external terrain data is never embedded here.
The adapters expose the named caller values, not complete scratch/exception ABI.
"""
from .domain import (SceneState, Long, checked_state, uint, u8, u16,
                     low16, replace_word, descending_inclusive, ram_view,
                     data_view)
from .contexts_rule_reuse import (DefenseProgressResult, MonthlyActionsResult,
                                 TerrainQueryResult)


def award_defense_progress(state: SceneState, officer: Long,
                           gain: Long) -> DefenseProgressResult:
    """Scalar history projects the sole Scene core; unobserved saved D0/A7 cannot be manufactured."""
    checked_state(state)
    uint(officer, 32)
    uint(gain, 32)
    frame = first_replace(FirstDeploymentFrame.unobserved(), unit=officer,
        count=gain, status=state.sr & 31)
    frame = award_defense_progress_fields(state, frame)
    return DefenseProgressResult(frame.unit, frame.count, state.table_at(frame.roster.base))


def clear_completed_monthly_actions(state: SceneState,
                                    retained_counter: Long) -> MonthlyActionsResult:
    """The scalar observer projects the same actual256/40 scans without inventing other fields."""
    checked_state(state)
    uint(retained_counter, 32)
    frame = first_replace(FirstDeploymentFrame.unobserved(), target_x=retained_counter, status=state.sr & 31)
    frame = clear_completed_monthly_actions_fields(state, frame)
    return MonthlyActionsResult(frame.target_x, frame.roster)


def query_scaled_terrain(state: SceneState, row: Long, column: Long,
                         retained_terrain: Long,
                         retained_cost: Long) -> TerrainQueryResult:
    """14294/142A2: snap low coordinates, use signed WORD table offsets.

    Terrain and costs are external readonly views atEE5F0/670A. CLR.W before
    each BYTE result preserves only the input's upper word, not a fake zero
    LONG. The lower helper restores the full shifted row before rescaling.
    """
    checked_state(state)
    for value in (row, column, retained_terrain, retained_cost):
        uint(value, 32)
    cell_row = low16(row) >> 4
    cell_column = low16(column) >> 4
    index = u16(u16(u16(cell_row + u16(cell_row << 3)) << 3) + cell_column)
    terrain = data_view(state, 'data_0ee5f0').byte(index)
    costs = data_view(state, 'data_00670a')
    cost = costs.byte(terrain)
    return TerrainQueryResult(replace_word(row, u16(cell_row << 4)),
        replace_word(column, u16(cell_column << 4)),
        replace_word(retained_terrain, terrain),
        replace_word(retained_cost, cost), costs)


# Current Scene successors; frozen historical owner/source remains untouched.
from .services import FirstDeploymentFrame
from .business_movement_support import (
    first_replace, MovementContinuationBoundary, _movement_move,
    _movement_test, _movement_compare, _movement_fixed_shift_word,
    _movement_add_word)
from ..high_level_remaining_flows.business_city import (
    _settlement_store_word_fields, _settlement_write_byte_fields)
from ..high_level_gameplay_flow.business_battle import _postbattle_bit_fields


def _project_rule_frame_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: int, defense: bool) -> FirstDeploymentFrame:
    """Validate only truly observed fields for scalar projections; complete callers keep all retained fields."""
    checked_state(state)
    if type(frame) is not FirstDeploymentFrame or (entry,defense) not in ((0x11C8C,True),(0x11CCA,False)):
        raise ValueError('current sole project rule fields required')
    frame.validate(state, complete=False)
    needed = (frame.target_x,frame.unit,frame.count,frame.stack_cursor,frame.status) if defense else (frame.target_x,frame.status)
    if any(value is None for value in needed):
        raise MovementContinuationBoundary(entry, frame, 'historical rule projection lacks actual saved D0 WORD/SP or observed fields')
    state.sr = (state.sr & 65504) | frame.status
    return frame


def award_defense_progress_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """11C8C..11CCA current Scene successor: actual D0 WORD save, two live reward writes and physical restore."""
    frame = _project_rule_frame_fields(state, frame, 0x11C8C, True)
    value = low16(frame.target_x)
    stack = frame.stack_cursor.advance(-2)
    stack.set_word(0, value)
    frame = first_replace(frame, stack_cursor=stack)
    frame = _movement_test(state, frame, value, 16)
    frame = _movement_fixed_shift_word(state, frame, 'unit', 1)
    frame = _movement_fixed_shift_word(state, frame, 'count', 1)
    for address in (0xFFFFBE00,0xFFFFC000):
        frame = first_replace(frame, roster=state.table_at(address).cursor())
        frame = _movement_move(state, frame, 'target_x', frame.roster.word(low16(frame.unit)), 16)
        frame = _movement_add_word(state, frame, 'target_x', low16(frame.count))
        frame = _movement_compare(state, frame, low16(frame.target_x), 999, 16)
        if not frame.status & 5:
            frame = _movement_move(state, frame, 'target_x', 999, 16)
        frame = _settlement_store_word_fields(state, frame, frame.roster, low16(frame.unit), low16(frame.target_x))
    restored = frame.stack_cursor.word()
    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
    return _movement_move(state, frame, 'target_x', restored, 16)


def clear_completed_monthly_actions_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """11CCA..11CF2 current Scene successor: original256 action==1 clears then40 BCLR1 operations."""
    frame = _project_rule_frame_fields(state, frame, 0x11CCA, False)
    frame = first_replace(frame, roster=state.table_at(0xFFFFCD00).cursor())
    frame = _movement_move(state, frame, 'target_x', 255, 16)
    while True:
        frame = _movement_compare(state, frame, frame.roster.byte(), 1, 8)
        if frame.status & 4:
            frame = _settlement_write_byte_fields(state, frame, frame.roster, value=0, clear=True)
        frame = first_replace(frame, roster=frame.roster.advance(1))
        remaining = (low16(frame.target_x) - 1) & 65535
        frame = first_replace(frame, target_x=replace_word(frame.target_x, remaining))
        if remaining == 65535:
            break
    frame = first_replace(frame, roster=state.table_at(0xFFFFEA38).cursor())
    frame = _movement_move(state, frame, 'target_x', 39, 16)
    while True:
        value = frame.roster.byte()
        frame.roster.set_byte(0, value & 253)
        frame = first_replace(frame, roster=frame.roster.advance(1))
        frame = _postbattle_bit_fields(frame, bool(value & 2))
        state.sr = (state.sr & 65504) | frame.status
        remaining = (low16(frame.target_x) - 1) & 65535
        frame = first_replace(frame, target_x=replace_word(frame.target_x, remaining))
        if remaining == 65535:
            return frame
