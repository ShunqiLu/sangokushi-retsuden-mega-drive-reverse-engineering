"""Live object, sprite and continuation contracts for scene business rules.

Upper bits are carried only where the original partial-width operation makes
them observable. These are semantic operands, not an emulated CPU frame.
"""
from dataclasses import dataclass
from .domain import (SceneState, Table, Cursor, Word, Long, StackContinuation, VideoPlaneAddress, Boundary, uint,
                     checked_state, checked_table, checked_cursor)


@dataclass(frozen=True)
class SceneControllerConditions:
    """Observed NZVC only; None is explicit unknown, never false by default."""
    carry: bool | None
    zero: bool | None
    negative: bool | None
    overflow: bool | None

    def validate(self):
        for value in (self.carry, self.zero, self.negative, self.overflow):
            if value is not None and type(value) is not bool:
                raise ValueError('strict observed condition or explicit unknown required')
        return self


@dataclass(frozen=True)
class SceneControllerFrame:
    """Current controller operands and views, at the original function entry.

    Eight LONG operands correspond to horizontal/command, vertical/parameter,
    attributes, palette, tile, extent/stride, row count and layer/progress.
    Source/destination may change roles as the actual algorithm changes A0/A1;
    video addresses are not dereferenceable bus views. Traversal is the live
    layout or queue cursor, and actor is the current A6 view, not a fixed side.
    This is a semantic handoff, not an instruction/CPU execution frame.
    """
    x: Long
    y: Long
    attributes: Long
    palette: Long
    tile: Long
    extent: Long
    row_count: Long
    layer: Long
    source: Cursor
    destination: Cursor | VideoPlaneAddress
    directory: Table | Cursor
    parameters: Table | Cursor
    limits: Table | Cursor
    traversal: Cursor
    actor: Table | Cursor
    stack: Cursor
    conditions: SceneControllerConditions

    def validate(self, state):
        checked_state(state)
        for value in (self.x, self.y, self.attributes, self.palette, self.tile,
                      self.extent, self.row_count, self.layer):
            uint(value, 32)
        checked_cursor(self.source, state)
        if type(self.destination) is VideoPlaneAddress:
            uint(self.destination.carrier, 32)
        else:
            checked_cursor(self.destination, state)
        for view in (self.directory, self.parameters, self.limits, self.actor):
            checked_table(view, state)
        checked_cursor(self.traversal, state)
        checked_cursor(self.stack, state)
        if type(self.conditions) is not SceneControllerConditions:
            raise ValueError('explicit scene condition observations required')
        self.conditions.validate()
        return self


@dataclass(frozen=True)
class SceneControllerOutcome:
    """A current frame plus a genuine nonlocal continuation, if consumed."""
    frame: SceneControllerFrame
    discarded_continuation: StackContinuation | None

    def validate(self, state):
        if type(self.frame) is not SceneControllerFrame:
            raise ValueError('complete current scene frame required')
        self.frame.validate(state)
        if self.discarded_continuation is not None:
            if type(self.discarded_continuation) is not StackContinuation:
                raise ValueError('actual discarded continuation required')
            uint(self.discarded_continuation.return_carrier, 32)
        return self


@dataclass(frozen=True)
class SceneRenderFrame:
    x: Long = 0
    y: Long = 0
    attributes: Long = 0
    palette: Long = 0
    tile: Long = 0
    live: SceneControllerFrame | None = None

    def validate(self, state):
        checked_state(state)
        for value in (self.x, self.y, self.attributes, self.palette, self.tile):
            uint(value, 32)
        if self.live is not None:
            if type(self.live) is not SceneControllerFrame:
                raise ValueError('exact complete scene frame required')
            self.live.validate(state)
            if (self.x, self.y, self.attributes, self.palette, self.tile) != (
                    self.live.x, self.live.y, self.live.attributes,
                    self.live.palette, self.live.tile):
                raise ValueError('legacy operands must project the actual current frame')
        return self


@dataclass(frozen=True)
class SpriteBatchContext:
    source: Cursor
    frame: SceneRenderFrame

    def validate(self, state):
        checked_cursor(self.source, state)
        if type(self.frame) is not SceneRenderFrame:
            raise ValueError('scene render operands required')
        self.frame.validate(state)
        return self


@dataclass(frozen=True)
class SpriteBatchResult:
    source: Cursor
    frame: SceneRenderFrame

    def validate(self, state):
        checked_cursor(self.source, state)
        self.frame.validate(state)
        return self


@dataclass(frozen=True)
class SceneObjectContext:
    actor: Table
    frame: SceneRenderFrame

    def validate(self, state):
        checked_table(self.actor, state)
        self.frame.validate(state)
        return self


@dataclass(frozen=True)
class CoordinateIntegrationOutcome:
    position_carrier: Long
    velocity_carrier: Long

    def validate(self, state):
        checked_state(state)
        uint(self.position_carrier, 32)
        uint(self.velocity_carrier, 32)
        return self


@dataclass(frozen=True)
class ObjectPositionOffset:
    horizontal: Word
    vertical: Word

    def validate(self, state):
        checked_state(state)
        uint(self.horizontal, 16)
        uint(self.vertical, 16)
        return self


@dataclass(frozen=True)
class ObjectOverlapOutcome:
    found: bool
    candidate: Table

    def validate(self, state):
        if type(self.found) is not bool:
            raise ValueError('strict overlap flag required')
        checked_table(self.candidate, state)
        return self


@dataclass(frozen=True)
class ActionPlanOutcome:
    discard_parent_continuation: bool
    audio_carrier: Long

    def validate(self, state):
        checked_state(state)
        if type(self.discard_parent_continuation) is not bool:
            raise ValueError('strict continuation flag required')
        uint(self.audio_carrier, 32)
        return self


@dataclass(frozen=True)
class ObjectActionContext:
    actor: Table
    roster: Table
    frame: SceneRenderFrame
    continuation: StackContinuation

    def validate(self, state):
        checked_table(self.actor, state)
        checked_table(self.roster, state)
        self.frame.validate(state)
        if type(self.continuation) is not StackContinuation:
            raise ValueError('real caller continuation required')
        uint(self.continuation.return_carrier, 32)
        return self


@dataclass(frozen=True)
class ObjectPhaseDispatch:
    phase_carrier: Long
    frame: SceneRenderFrame

    def validate(self, state):
        self.frame.validate(state)
        uint(self.phase_carrier, 32)
        return self


@dataclass(frozen=True)
class ObjectActionDispatch:
    actor: Table
    roster: Table
    selection_carrier: Long
    frame: SceneRenderFrame
    resumed: bool

    def validate(self, state):
        checked_table(self.actor, state)
        checked_table(self.roster, state)
        self.frame.validate(state)
        uint(self.selection_carrier, 32)
        if type(self.resumed) is not bool:
            raise ValueError('strict resumed-action flag required')
        return self


def checked_context(value, kind, state):
    checked_state(state)
    if type(value) is not kind:
        raise ValueError('exact scene-object context required')
    return value.validate(state)


def checked_controller_frame(value, state):
    checked_state(state)
    if type(value) is SceneControllerFrame:
        return value.validate(state)
    if type(value) is SceneRenderFrame:
        value.validate(state)
        if value.live is not None:
            return value.live
    raise Boundary('complete scene-controller live operands/views/entry stack required before DATA')

# Same existing Scene fields; no new State union or source path.
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame

@dataclass(frozen=True)
class SceneActionPlanFields:
    """Actual planner fields and a physically discarded caller token, if any.

    Discard is not an RTS: success leaves A7 on the next real outer slot.
    Normal return-token consumption belongs to the specific calling bridge.
    """
    frame: FirstDeploymentFrame
    discarded_continuation: StackContinuation | None

    def validate(self, state):
        checked_state(state)
        if type(self.frame) is not FirstDeploymentFrame:
            raise ValueError('actual complete action planner fields required')
        self.frame.validate(state,True)
        if self.discarded_continuation is not None:
            if type(self.discarded_continuation) is not StackContinuation:
                raise ValueError('actual physically discarded LONG token required')
            uint(self.discarded_continuation.return_carrier,32)
        return self
