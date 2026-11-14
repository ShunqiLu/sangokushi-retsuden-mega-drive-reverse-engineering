"""Immutable action-family inputs and results, with live views explicit.

The retained scalar portions are compatibility inputs, not guessed gameplay
limits. Constructors reject malformed inputs before any original DATA event.
"""
from dataclasses import dataclass
from .domain import (Word, Long, Table, Cursor, CarryOutcome, uint,
                     checked_table, checked_cursor)


@dataclass(frozen=True)
class AnchorContext:
    x: Long
    y: Long

    def __post_init__(self):
        uint(self.x, 32)
        uint(self.y, 32)


@dataclass(frozen=True)
class OccupiedCellsContext:
    source: Cursor
    destination: Cursor
    positions: Table

    def __post_init__(self):
        checked_cursor(self.source)
        checked_cursor(self.destination, self.source.state)
        checked_table(self.positions, self.source.state)


@dataclass(frozen=True)
class EmptySlotContext:
    source: Cursor
    positions: Table

    def __post_init__(self):
        checked_cursor(self.source)
        checked_table(self.positions, self.source.state)


@dataclass(frozen=True)
class EmptySlotResult:
    offset: Word
    source: Cursor
    outcome: CarryOutcome

    def __post_init__(self):
        uint(self.offset, 16)
        checked_cursor(self.source)
        if type(self.outcome) is not CarryOutcome:
            raise ValueError('typed original carry required')


@dataclass(frozen=True)
class DeploymentCellContext:
    map: Table
    positions: Table
    offset: Word
    x: Word
    y: Word

    def __post_init__(self):
        checked_table(self.map)
        checked_table(self.positions, self.map.state)
        for value in (self.offset, self.x, self.y):
            uint(value, 16)


@dataclass(frozen=True)
class DeploymentEdgeContext:
    map: Table
    positions: Table
    source: Cursor
    offset: Word
    center_x: Word
    center_y: Word
    radius: Word

    def __post_init__(self):
        checked_table(self.map)
        checked_table(self.positions, self.map.state)
        checked_cursor(self.source, self.map.state)
        for value in (self.offset, self.center_x, self.center_y, self.radius):
            uint(value, 16)


@dataclass(frozen=True)
class PromotionContext:
    formation_carrier: Long

    def __post_init__(self):
        uint(self.formation_carrier, 32)


@dataclass(frozen=True)
class RatingContext:
    rating: Long
    selected: Long

    def __post_init__(self):
        uint(self.rating, 32)
        uint(self.selected, 32)


@dataclass(frozen=True)
class RatingSelection:
    rating: Long
    selected: Long

    def __post_init__(self):
        uint(self.rating, 32)
        uint(self.selected, 32)


@dataclass(frozen=True)
class SelectionContext:
    selected: Long
    terrain_carrier: Long

    def __post_init__(self):
        uint(self.selected, 32)
        uint(self.terrain_carrier, 32)


@dataclass(frozen=True)
class ScoredSelection:
    score: Long
    selected: Long
    map: Table

    def __post_init__(self):
        uint(self.score, 32)
        uint(self.selected, 32)
        checked_table(self.map)


@dataclass(frozen=True)
class CandidateBudgetContext:
    selected: Long

    def __post_init__(self):
        uint(self.selected, 32)


@dataclass(frozen=True)
class ActionTerrainPolicy:
    """Eligible low-BYTE terrain kinds; no guess about their artwork roles."""
    kinds: tuple[Word, ...]

    def __post_init__(self):
        if type(self.kinds) is not tuple or not self.kinds:
            raise ValueError('nonempty typed terrain policy required')
        for kind in self.kinds:
            uint(kind, 8, 'eligible terrain kind')


@dataclass(frozen=True)
class ActionCandidate:
    member: Word
    offset: Word
    terrain: Long

    def __post_init__(self):
        uint(self.member, 16, 'candidate member')
        uint(self.offset, 16, 'candidate live position offset')
        uint(self.terrain, 32, 'retained terrain value')


@dataclass(frozen=True)
class ActionRandomDraw:
    sample: Word
    updated_state: Long

    def __post_init__(self):
        uint(self.sample, 16, 'random low-WORD sample')
        uint(self.updated_state, 32, 'updated random state')


@dataclass(frozen=True)
class TerrainActorContext:
    actor: Long
    terrain_carrier: Long

    def __post_init__(self):
        uint(self.actor, 32)
        uint(self.terrain_carrier, 32)


def checked_context(value, expected, state=None):
    if type(value) is not expected:
        raise ValueError('exact typed action context required')
    value.__post_init__()
    if state is not None:
        for item in value.__dict__.values():
            if type(item) in (Table, Cursor):
                checked_table(item, state)
    return value
