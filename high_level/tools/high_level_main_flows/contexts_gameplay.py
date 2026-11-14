"""Immutable operands of projects, map presentation and battle policy.

Live views are never copied into snapshots. Entry adapters must supply the
retained carriers explicitly; no blanket zero/register-frame fallback exists.
"""
from dataclasses import dataclass
from .domain import (Long, Table, Cursor, SceneState, uint, checked_state,
                     checked_table, checked_cursor)


@dataclass(frozen=True)
class ProjectValues:
    """Current project operands and live work view.

    ``orders`` starts at the selected E80x order table, but follows the real
    work-view changes during aptitude/reward and may return BE00 or C200.
    It is not a retained snapshot of the initial order table. Gold uses a
    separate DFFC view; selecting it does not change this work view.
    """
    officer: Long
    budget: Long
    value: Long
    scale: Long
    effect: Long
    city_index: Long
    record_index: Long
    city_offset: Long
    assignments: Table
    task_flags: Table
    orders: Table | None = None

    def validate(self, state):
        checked_state(state)
        for value in (self.officer, self.budget, self.value, self.scale,
                      self.effect, self.city_index, self.record_index, self.city_offset):
            uint(value, 32)
        for view in (self.assignments, self.task_flags, self.orders):
            if view is not None:
                checked_table(view, state)
        return self


@dataclass(frozen=True)
class MapPresentation:
    """Actual D0..D7 and A0/A1/A2 carrier projection, not view-purpose names.

    x/y/attributes/tile/officer/count/index/remaining are D0..D7. source is
    current A0, destination current A1, and packet current A2. In a packet
    writer, source therefore owns the output cursor; a decimal stream placed
    in A1 is destination. Digit scratch A6 is not silently mapped to A1.
    Each mandatory LONG retains its actual full carrier. None views express
    unobserved input only; a helper consuming one must expose a Boundary.
    A3..A6, SP and complete CCR are outside this legacy projection.
    """
    x: Long
    y: Long
    attributes: Long
    tile: Long
    officer: Long
    count: Long
    index: Long
    remaining: Long
    packet: Cursor | None
    source: Cursor | None
    destination: Cursor | None

    def validate(self, state):
        checked_state(state)
        for value in (self.x, self.y, self.attributes, self.tile, self.officer,
                      self.count, self.index, self.remaining):
            uint(value, 32)
        for view in (self.packet, self.source, self.destination):
            if view is not None:
                checked_cursor(view, state)
        return self


@dataclass(frozen=True)
class TargetSearch:
    origin_x: Long
    origin_y: Long
    candidate: Long
    count: Long
    limit: Long
    city: Long
    metric_x: Long
    metric_y: Long
    destination: Cursor | None
    source: Cursor | None
    cities: Table | None
    officers: Table | None
    terrain: Table | None
    blocked: Table | None

    def validate(self, state):
        checked_state(state)
        for value in (self.origin_x, self.origin_y, self.candidate, self.count,
                      self.limit, self.city, self.metric_x, self.metric_y):
            uint(value, 32)
        for view in (self.destination, self.source):
            if view is not None:
                checked_cursor(view, state)
        for view in (self.cities, self.officers, self.terrain, self.blocked):
            if view is not None:
                checked_table(view, state)
        return self


@dataclass(frozen=True)
class BattlePolicy:
    target_x: Long
    target_y: Long
    unit: Long
    count: Long
    distance: Long
    offset_x: Long
    offset_y: Long
    choice: Long
    roster: Cursor | None
    candidates: Cursor | None
    scan: Cursor | None
    controller: Table | None
    opponent: Table | None
    scratch: Table | None
    stack_cursor: Cursor | None = None
    auxiliary: Table | None = None

    def validate(self, state):
        checked_state(state)
        for value in (self.target_x, self.target_y, self.unit, self.count,
                      self.distance, self.offset_x, self.offset_y, self.choice):
            uint(value, 32)
        for view in (self.roster, self.candidates, self.scan):
            if view is not None:
                checked_cursor(view, state)
        for view in (self.controller, self.opponent, self.scratch, self.auxiliary):
            if view is not None:
                checked_table(view, state)
        if self.stack_cursor is not None:
            checked_cursor(self.stack_cursor, state)
        return self


@dataclass(frozen=True)
class SetupValues:
    """Explicit live setup carriers; names are not positional sprite arguments.

    value/option/position are D0/D1/D2 (sprite x/y/attributes). attributes/rows/
    tile/stride/selector are D3/D4/D5/D6/D7. Selection cycling uses tile=D5;
    source/destination retain the original A0/A1 views respectively.
    """
    value: Long
    option: Long
    position: Long
    attributes: Long
    rows: Long
    tile: Long
    stride: Long
    selector: Long
    source: Cursor | None
    destination: Cursor | None

    def validate(self, state):
        checked_state(state)
        for value in (self.value, self.option, self.position, self.attributes,
                      self.rows, self.tile, self.stride, self.selector):
            uint(value, 32)
        for view in (self.source, self.destination):
            if view is not None:
                checked_cursor(view, state)
        return self


@dataclass(frozen=True)
class SetupPlane:
    command: Long
    marker: Long
    tile: Long
    repeat_count: Long
    column: Long
    row_stride: Long
    source: Cursor
    video_address: object

    def validate(self, state):
        from .domain import VideoPlaneAddress
        checked_state(state)
        for value in (self.command, self.marker, self.tile, self.repeat_count,
                      self.column, self.row_stride):
            uint(value, 32)
        checked_cursor(self.source, state)
        if type(self.video_address) is not VideoPlaneAddress:
            raise ValueError('video address, not a RAM view, required')
        uint(self.video_address.carrier, 32)
        return self


@dataclass(frozen=True)
class GameplayCall:
    operands: ProjectValues | MapPresentation | TargetSearch | BattlePolicy | SetupValues
    continuation: Long

    def validate(self, state):
        if type(self.operands) not in (ProjectValues, MapPresentation, TargetSearch, BattlePolicy, SetupValues):
            raise ValueError('known gameplay-family call operands required')
        self.operands.validate(state)
        uint(self.continuation, 32)
        return self


def checked_context(value, kind, state):
    checked_state(state)
    if type(value) is not kind:
        raise ValueError('exact gameplay-family operands required')
    return value.validate(state)


# Actual same-state movement successor carriers, not a new state.
from ..high_level_battle_ai.contexts_first_deployment import (
    FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace,
)


# Real movement wait/exception continuation fields, never a new state.
from .domain import Boundary


class MovementContinuationBoundary(Boundary):
    """An actual wait/exception instruction and its already changed live SP."""
    def __init__(self, target, frame, reason):
        uint(target, 32)
        if type(frame) is not FirstDeploymentFrame or type(reason) is not str:
            raise ValueError('actual movement continuation fields required')
        self.target, self.context, self.reason = target, frame, reason
        super().__init__(reason)
