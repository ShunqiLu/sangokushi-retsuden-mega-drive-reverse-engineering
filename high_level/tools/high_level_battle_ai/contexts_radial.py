"""Closed live-DATA boundary for the original 3080E/30830 algorithm.

This is not another State or a register emulator. The original GameState and
the city's actual SceneState retain their own RAM, DATA, views and budgets.
Unobserved legacy stacks stay None; complete callers supply real MOVEM/BSR slots.
"""
from dataclasses import dataclass
from .domain import GameState, Table, Cursor, uint, checked_table
from ..high_level_scene_flows.domain import SceneState, Table as SceneTable, checked_state as checked_scene_state

RadialTable = Table | SceneTable


def checked_radial_table(value, state=None):
    from ..high_level_scene_flows.domain import Table as SceneTable, Cursor as SceneCursor
    from ..high_level_scene_flows.domain import checked_table as scene_table
    if type(value) in (Table, Cursor):
        checked_table(value, state)
    elif type(value) in (SceneTable, SceneCursor):
        scene_table(value, state)
    else:
        raise ValueError('one real radial live Table required')
    return value


class RadialMemory:
    """An identity-preserving view factory, not copied RAM or fake services."""
    def __init__(self, state, stack_cursor=None):
        if type(state) not in (GameState, SceneState):
            raise ValueError('real battle or Scene radial state required')
        self.state = state
        self.stack_cursor = stack_cursor
        if stack_cursor is not None:
            checked_radial_table(stack_cursor, state)

    def enter_seed(self):
        """30818 BSR.W's true3081C continuation, only when A7 was observed."""
        if self.stack_cursor is not None:
            self.stack_cursor = self.stack_cursor.advance(-4)
            self.stack_cursor.set_long(0, 0x3081C)

    def leave_seed(self):
        """30874 RTS actual LONG read; altered original control is not success."""
        if self.stack_cursor is not None:
            actual = self.stack_cursor.long()
            self.stack_cursor = self.stack_cursor.advance(4)
            if actual != 0x3081C:
                from .domain import Boundary
                from ..high_level_scene_flows.domain import Boundary as SceneBoundary
                if type(self.state) is SceneState:
                    raise SceneBoundary('modified original radial seed return target ' + str(actual))
                raise Boundary('modified original radial seed return target ' + str(actual))

    @property
    def thresholds(self):
        if type(self.state) is GameState:
            return Table(self.state, 0x30876)
        return self.state.table_at(0x30876)


@dataclass(frozen=True)
class RadialSeedFields:
    remaining: int
    count: int
    increment: int
    last_threshold: int
    threshold_cursor: object | None

    def __post_init__(self):
        for value in (self.remaining, self.count, self.increment, self.last_threshold):
            uint(value, 32)
        if self.threshold_cursor is not None:
            checked_radial_table(self.threshold_cursor)


@dataclass(frozen=True)
class RadialDistanceFields:
    """Actual full D0 and last TST.L/MOVE.W NZVC, not a full CPU frame."""
    value: int
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def __post_init__(self):
        uint(self.value, 32)
        if any(type(flag) is not bool for flag in
               (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('strict original radial conditions required')
