"""Closed first-side deployment carriers shared by full and legacy interfaces.

None means an old API did not observe a carrier. Complete Scene calls require
the real eight LONGs, entry SP and CCR; they never turn None into zero.
"""
from dataclasses import dataclass, replace as first_replace
from .domain import uint, Cursor
from .contexts_policy_memory import checked_policy_table
from ..high_level_scene_flows.domain import Boundary, Cursor as SceneCursor


@dataclass(frozen=True)
class FirstDeploymentFrame:
    target_x: int | None
    target_y: int | None
    unit: int | None
    count: int | None
    distance: int | None
    offset_x: int | None
    offset_y: int | None
    choice: int | None
    roster: object | None
    candidates: object | None
    controller: object | None
    scan: object | None
    opponent: object | None
    scratch: object | None
    auxiliary: object | None
    stack_cursor: object | None
    status: int | None

    @classmethod
    def unobserved(cls):
        return cls(*(None for _ in range(17)))

    def validate(self, state, complete=False):
        if type(complete) is not bool:
            raise ValueError('complete-observation selector must be an actual bool')
        for value in (self.target_x, self.target_y, self.unit, self.count,
                      self.distance, self.offset_x, self.offset_y, self.choice):
            if value is not None or complete:
                uint(value, 32)
        for view in (self.roster, self.candidates, self.controller, self.scan,
                     self.opponent, self.scratch, self.auxiliary, self.stack_cursor):
            if view is not None:
                checked_policy_table(view, state)
        if self.status is not None or complete:
            uint(self.status, 8)
            if self.status > 31:
                raise ValueError('actual CCR must be in the low five bits')
        if complete and self.stack_cursor is None:
            raise Boundary('complete deployment requires real callee-entry SP')
        if self.stack_cursor is not None and type(self.stack_cursor) not in (Cursor, SceneCursor):
            raise ValueError('deployment stack must be an actual live Cursor')
        return self

    def carrier(self, name):
        """Closed D0..D7 vocabulary; no arbitrary attribute/bus lookup."""
        if name == 'target_x':
            return self.target_x
        if name == 'target_y':
            return self.target_y
        if name == 'unit':
            return self.unit
        if name == 'count':
            return self.count
        if name == 'distance':
            return self.distance
        if name == 'offset_x':
            return self.offset_x
        if name == 'offset_y':
            return self.offset_y
        if name == 'choice':
            return self.choice
        raise ValueError('unknown deployment numeric carrier')


@dataclass(frozen=True)
class FirstLeaderFields:
    frame: FirstDeploymentFrame
    selected: int

    def __post_init__(self):
        if type(self.frame) is not FirstDeploymentFrame:
            raise ValueError('real deployment frame required')
        uint(self.selected, 16)


class FirstDeploymentReturnBoundary(Boundary):
    def __init__(self, target, frame, expected):
        self.target, self.context, self.expected = target, frame, expected
        super().__init__('live deployment return slot changed the original continuation')


@dataclass(frozen=True)
class FirstTrainingFields:
    frame: FirstDeploymentFrame
    factor: int
    restored_unit: int

    def __post_init__(self):
        if type(self.frame) is not FirstDeploymentFrame:
            raise ValueError('current training return frame required')
        uint(self.factor, 32)
        uint(self.restored_unit, 16)


class FirstDeploymentArithmeticBoundary(Boundary):
    def __init__(self, target, frame, value):
        self.target, self.context, self.value = target, frame, value
        super().__init__('original DIVU overflow leaves N/Z undefined for a complete return')
