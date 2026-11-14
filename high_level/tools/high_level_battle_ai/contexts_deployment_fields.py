"""Retained deployment fields over the existing sealed policy memory.

None denotes only a legacy unobserved carrier;
validate_complete rejects it before complete callers use the fields. Actual
Scene/battle views retain their State and live cursor identity. No RAM copy or
synthetic pointer is introduced.
"""
from dataclasses import dataclass
from .domain import Cursor, uint
from .contexts_policy_memory import BattlePolicyMemory, PolicyTable, checked_policy_table
from ..high_level_scene_flows.domain import Cursor as SceneCursor


def checked_deployment_cursor(value, state=None):
    if type(value) not in (Cursor, SceneCursor):
        raise ValueError('existing live policy Cursor required')
    checked_policy_table(value, state)
    return value


def changed_deployment_return(memory, target):
    """The alias-derived target is exposed, never silently treated as RTS."""
    from .domain import Boundary, GameState
    from ..high_level_scene_flows.domain import Boundary as SceneBoundary
    if type(memory) is not BattlePolicyMemory:
        raise ValueError('sealed deployment memory required')
    uint(target, 32)
    message = 'occupied-list return slot changed to actual target ' + str(target)
    if type(memory.state) is GameState:
        raise Boundary(message)
    raise SceneBoundary(message)


@dataclass(frozen=True)
class DeploymentOccupiedFields:
    """D2/D3, A1/A2/A3 and X after the actual 25C48 list algorithm."""
    member: int | None
    coordinate: int | None
    destination: Cursor | SceneCursor
    source: Cursor | SceneCursor
    positions: PolicyTable
    extend: bool | None
    stack_cursor: Cursor | SceneCursor | None

    def validate(self, state):
        for value in (self.member, self.coordinate):
            if value is not None:
                uint(value, 32)
        checked_deployment_cursor(self.destination, state)
        checked_deployment_cursor(self.source, state)
        checked_policy_table(self.positions, state)
        if self.extend is not None and type(self.extend) is not bool:
            raise ValueError('observed X must be a strict bool')
        if self.stack_cursor is not None:
            checked_deployment_cursor(self.stack_cursor, state)
        return self

    def validate_complete(self, state):
        self.validate(state)
        uint(self.member, 32)
        uint(self.coordinate, 32)
        if type(self.extend) is not bool:
            raise ValueError('complete occupied fields require observed X')
        checked_deployment_cursor(self.stack_cursor, state)
        return self


@dataclass(frozen=True)
class DeploymentSlotFields:
    """25C9C's full D6 when supplied, A3, low-WORD projection and NZVC/X."""
    index: int | None
    offset: int
    source: Cursor | SceneCursor
    positions: PolicyTable
    carry: bool
    zero: bool
    negative: bool
    extend: bool | None

    def validate(self, state):
        if self.index is not None:
            uint(self.index, 32)
        uint(self.offset, 16)
        checked_deployment_cursor(self.source, state)
        checked_policy_table(self.positions, state)
        for flag in (self.carry, self.zero, self.negative):
            if type(flag) is not bool:
                raise ValueError('actual slot condition must be a strict bool')
        if self.extend is not None and type(self.extend) is not bool:
            raise ValueError('observed X must be a strict bool')
        return self

    def validate_complete(self, state):
        self.validate(state)
        uint(self.index, 32)
        if type(self.extend) is not bool:
            raise ValueError('complete slot fields require observed X')
        return self
