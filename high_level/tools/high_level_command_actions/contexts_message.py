"""Message transaction observations and explicit same-memory call carriers.

No opcode frame or copied State is constructed. Legacy callers observe only
their original result projection. Positive message preparation overwrites A0
and A1 before reading either input; negative early returns retain both views.
"""
from dataclasses import dataclass
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame
from .domain import GameState, Long, Word, uint
from ..high_level_scene_flows.domain import (
    SceneState, Table, Boundary, checked_state as checked_scene_state,
    checked_table as checked_scene_table,
)


@dataclass(frozen=True)
class MessageMemory:
    """Original live endpoint, optionally observing a genuine complete Scene frame.

    Accepted State types are unchanged. Old WORD APIs omit the observation and
    keep their partial contract; a provided frame must be actual complete Scene.
    No RAM copy, added State union member or invented upper carrier is made.
    """
    state: object
    frame: FirstDeploymentFrame | None = None

    def __post_init__(self):
        if type(self.state) not in (GameState,SceneState):
            raise ValueError('one genuine message live State required')
        if self.frame is not None:
            if type(self.state) is not SceneState or type(self.frame) is not FirstDeploymentFrame:
                raise ValueError('full message observation requires actual Scene frame')
            self.frame.validate(self.state,True)
            self.state.sr = (self.state.sr & 65504) | self.frame.status

    def read(self,address,size):
        return self.state.read(address,size)

    def write(self,address,size,value):
        self.state.write(address,size,value)

    def observe(self,frame: FirstDeploymentFrame) -> None:
        if self.frame is None:
            raise ValueError('partial message port cannot fabricate a full observation')
        frame.validate(self.state,True)
        self.state.sr = (self.state.sr & 65504) | frame.status
        object.__setattr__(self,'frame',frame)


@dataclass(frozen=True)
class MessagePointerFields:
    """True resolved A0/A1 addresses and the last item-relative D1 WORD."""
    pointer: Long
    descriptor: Long
    item_offset: Word

    def __post_init__(self):
        uint(self.pointer, 32)
        uint(self.descriptor, 32)
        uint(self.item_offset, 16)


@dataclass(frozen=True)
class MessagePreparation:
    """Actual transaction observations, not fabricated complete registers."""
    resolved: MessagePointerFields | None
    layout_offset: Word | None
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def __post_init__(self):
        if self.resolved is not None and type(self.resolved) is not MessagePointerFields:
            raise ValueError('genuine pointer resolution required')
        if self.layout_offset is not None:
            uint(self.layout_offset, 16)
        if (self.resolved is None) != (self.layout_offset is None):
            raise ValueError('complete positive transaction observations required')
        if any(type(v) is not bool for v in
               (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('explicit actual partial arithmetic conditions required')


@dataclass(frozen=True)
class SceneMessageInput:
    value: Long
    field: Long
    destination: Table | None
    source: Table | None

    def validate(self, state):
        checked_scene_state(state)
        uint(self.value, 32, 'actual D0 carrier')
        uint(self.field, 32, 'actual D1 carrier')
        for view in (self.destination, self.source):
            if view is not None:
                checked_scene_table(view, state)
        if self.value & 0x8000 and (self.destination is None or self.source is None):
            raise Boundary('negative message retains unprovided A0/A1 input')
        return self


@dataclass(frozen=True)
class SceneMessageResult:
    destination: Table
    source: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_scene_state(state)
        checked_scene_table(self.destination, state)
        checked_scene_table(self.source, state)
        uint(self.value, 32)
        uint(self.field, 32)
        if any(type(v) is not bool for v in
               (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('strict message partial arithmetic return required')
        return self
