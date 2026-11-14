"""Closed live ports for the original 1A438 and 25C02 policy readers.

The existing battle GameState and scene SceneState keep their own identity,
RAM, DATA and budgets. This object is neither a third State nor copied RAM.
Physical call/return tokens and 1A438's saved D4 stack slot are not modeled by
this nonstack field projection. No unknown carrier is replaced with zero.
"""
from dataclasses import dataclass
from .domain import GameState, Table, Cursor, uint, checked_table
from ..high_level_scene_flows.domain import (
    SceneState, Table as SceneTable, Cursor as SceneCursor,
    checked_table as checked_scene_table,
)

PolicyTable = Table | SceneTable


def checked_policy_table(value, state=None):
    if type(value) in (Table, Cursor):
        checked_table(value, state)
    elif type(value) in (SceneTable, SceneCursor):
        checked_scene_table(value, state)
    else:
        raise ValueError('one existing same-state policy Table required')
    return value


class BattlePolicyMemory:
    """Only the two already recovered state types may own these fixed ports."""
    def __init__(self, state):
        if type(state) not in (GameState, SceneState):
            raise ValueError('existing battle or Scene policy state required')
        self.state = state

    def battle_scene(self):
        return self.state.read(0xFFFFF68A, 2)

    @property
    def battlefield_maps(self):
        return self.state.table(0x945E8)

    @property
    def scene_variants(self):
        return self.state.table(0xFFFF9FFF)

    @property
    def deployment_cells(self):
        return self.state.table(0xABDA8)

    def sample_random_pair(self):
        return deployment_random_pair(self)


@dataclass(frozen=True)
class DeploymentAnchorFields:
    """25C02's D0/D1, optional observed D2, A3 and last MOVE.B conditions.

Only the historical x/y API may leave D2 unobserved (None). The Scene caller
must validate_complete and provide its mandatory incoming full D2. A3 is the
cell-pair base, not the indexed effective address. No extra flags read occurs.
"""
    x: int
    y: int
    index: int | None
    cells: PolicyTable
    zero: bool
    negative: bool
    extend: bool

    def __post_init__(self):
        uint(self.x, 32)
        uint(self.y, 32)
        if self.index is not None:
            uint(self.index, 32)
        checked_policy_table(self.cells)
        if any(type(flag) is not bool for flag in (self.zero, self.negative, self.extend)):
            raise ValueError('real final MOVE.B observations required')

    def validate_complete(self, state):
        uint(self.index, 32)
        checked_policy_table(self.cells, state)
        return self


def deployment_random_pair(memory):
    if type(memory) is not BattlePolicyMemory:
        raise ValueError('sealed deployment memory required')
    if type(memory.state) is GameState:
        return memory.state.sample_random_pair()
    from ..high_level_scene_flows.business_reuse import _reuse_advance_random_pair
    return _reuse_advance_random_pair(memory.state)
