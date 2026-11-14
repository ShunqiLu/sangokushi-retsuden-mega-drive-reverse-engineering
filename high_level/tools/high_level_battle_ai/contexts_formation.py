"""Immutable formation values and explicit live-view caller contexts.

These describe business inputs/results, not CPU register snapshots. Retained
limits are named because the original region routines turn one of them into a
span before returning; callers genuinely use that live result.
"""
from dataclasses import dataclass

from .domain import Byte, CarryOutcome, Cursor, Long, Table, Word, checked_cursor, checked_table, uint


@dataclass(frozen=True)
class Point:
    x: Word
    y: Word

    def __post_init__(self):
        uint(self.x, 16, 'point x')
        uint(self.y, 16, 'point y')


@dataclass(frozen=True)
class BattleBounds:
    left: Word
    right: Word
    lower: Word
    upper: Word

    def __post_init__(self):
        for value in (self.left, self.right, self.lower, self.upper):
            uint(value, 16, 'battle bound')


@dataclass(frozen=True)
class RegionInput:
    origin: Table
    offset: Word
    point: Point

    def __post_init__(self):
        checked_table(self.origin)
        uint(self.offset, 16, 'live coordinate offset')
        if type(self.point) is not Point:
            raise ValueError('typed point required')


@dataclass(frozen=True)
class EastFormationRegion:
    """Live east-side limits; deliberately not a normalized rectangle.

    The original policy has no lower x bound. WORD-wrapped vertical limits
    can also be reversed; neither property is corrected by this value type.
    """
    anchor_x: Word
    east_limit: Word
    lower: Word
    upper: Word

    def __post_init__(self):
        for value in (self.anchor_x, self.east_limit, self.lower, self.upper):
            uint(value, 16, 'east formation limit')


@dataclass(frozen=True)
class SampledFormationPoint:
    point: Point
    vertical_span: Word
    vertical_wrap: bool

    def __post_init__(self):
        if type(self.point) is not Point or type(self.vertical_wrap) is not bool:
            raise ValueError('typed sampled point and wrap outcome required')
        uint(self.vertical_span, 16, 'sampled vertical span')


@dataclass(frozen=True)
class SampledFlankPoint:
    point: Point
    horizontal_span: Word

    def __post_init__(self):
        if type(self.point) is not Point:
            raise ValueError('typed flank point required')
        uint(self.horizontal_span, 16, 'sampled horizontal span')


@dataclass(frozen=True)
class RegionDecision:
    point: Point
    horizontal_limit_or_span: Word
    vertical_limit_or_span: Word
    carry: CarryOutcome

    def __post_init__(self):
        if type(self.point) is not Point or type(self.carry) is not CarryOutcome:
            raise ValueError('typed region results required')
        uint(self.horizontal_limit_or_span, 16)
        uint(self.vertical_limit_or_span, 16)

    def with_point(self, x, y, carry=None):
        if carry is None:
            carry = self.carry
        if type(carry) is not CarryOutcome:
            raise ValueError('typed arithmetic carry required')
        return RegionDecision(Point(uint(x, 16), uint(y, 16)),
                              self.horizontal_limit_or_span,
                              self.vertical_limit_or_span, carry)


@dataclass(frozen=True)
class RosterStrength:
    byte_length: Word
    total: Long

    def __post_init__(self):
        uint(self.byte_length, 16)
        uint(self.total, 32)


@dataclass(frozen=True)
class ClosestBattleUnit:
    distance: Word
    unit: Word

    def __post_init__(self):
        uint(self.distance, 16)
        uint(self.unit, 16)


@dataclass(frozen=True)
class FormationCursors:
    source: Cursor
    destination: Cursor

    def __post_init__(self):
        checked_cursor(self.source)
        checked_cursor(self.destination, self.source.state)


@dataclass(frozen=True)
class WeightedDeploymentRoster:
    """Two live views; scoring never snapshots either allocation."""
    roster: Table
    weights: Table

    def __post_init__(self):
        checked_table(self.roster)
        checked_table(self.weights, self.roster.state)


@dataclass(frozen=True)
class DeploymentViews:
    roster: Table
    orders: Table
    cells: Table
    positions: Table

    def __post_init__(self):
        checked_table(self.roster)
        for view in (self.orders, self.cells, self.positions):
            checked_table(view, self.roster.state)


@dataclass(frozen=True)
class ShuffleSlots:
    first: Word
    second: Word

    def __post_init__(self):
        uint(self.first, 16, 'first choice byte offset')
        uint(self.second, 16, 'second choice byte offset')


@dataclass(frozen=True)
class LeaderRank:
    """Readiness BYTE and wrapped attribute sum, not a normalized ranking."""
    readiness: Byte
    strength: Word

    def __post_init__(self):
        uint(self.readiness, 8, 'leader readiness')
        uint(self.strength, 16, 'leader wrapped strength')
