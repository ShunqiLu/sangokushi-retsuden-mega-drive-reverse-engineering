"""Named geometry results; live cursors are kept, not copied into lists.

These are business projections, not a claim to emulate all CPU registers.
Retained values are explicit where an original partial-width write matters.
"""
from dataclasses import dataclass
from .domain import Word, Long, Table, Cursor, uint, checked_table, checked_cursor


@dataclass(frozen=True)
class TargetCoordinate:
    x: Word
    y: Word

    def __post_init__(self):
        uint(self.x, 16)
        uint(self.y, 16)


@dataclass(frozen=True)
class ContactStrength:
    strength: Long
    member: Word
    last_weighting: Long
    roster_tail: Cursor
    troops: Table

    def __post_init__(self):
        uint(self.strength, 32)
        uint(self.member, 16)
        uint(self.last_weighting, 32)
        checked_cursor(self.roster_tail)
        checked_table(self.troops, self.roster_tail.state)


@dataclass(frozen=True)
class ContactCollection:
    radius: Word
    x: Word
    y: Word
    output_tail: Cursor
    roster_tail: Cursor
    positions: Table

    def __post_init__(self):
        for value in (self.radius, self.x, self.y):
            uint(value, 16)
        checked_cursor(self.output_tail)
        checked_cursor(self.roster_tail, self.output_tail.state)
        checked_table(self.positions, self.output_tail.state)


@dataclass(frozen=True)
class RadialSeed:
    remaining: Long
    count: Long
    increment: Long
    last_threshold: Long
    threshold_cursor: Table | None

    def __post_init__(self):
        for value in (self.remaining, self.count, self.increment, self.last_threshold):
            uint(value, 32)
        if self.threshold_cursor is not None:
            checked_table(self.threshold_cursor)


@dataclass(frozen=True)
class TrainingInputs:
    training: Word
    rating: Word

    def __post_init__(self):
        uint(self.training, 16)
        uint(self.rating, 16)


@dataclass(frozen=True)
class WeightedContact:
    strength: Long
    offset: Word
    weighting: Long

    def __post_init__(self):
        uint(self.strength, 32)
        uint(self.offset, 16)
        uint(self.weighting, 32)


@dataclass(frozen=True)
class ContactSearch:
    radius: Word
    origin: TargetCoordinate
    output: Cursor
    roster: Cursor
    positions: Table

    def __post_init__(self):
        uint(self.radius, 16)
        if type(self.origin) is not TargetCoordinate:
            raise ValueError('typed contact origin required')
        checked_cursor(self.output)
        checked_cursor(self.roster, self.output.state)
        checked_table(self.positions, self.output.state)


@dataclass(frozen=True)
class RadialStep:
    remaining: Long
    crossed: bool

    def __post_init__(self):
        uint(self.remaining, 32)
        if type(self.crossed) is not bool:
            raise ValueError('strict subtraction crossing required')


from .contexts_first_deployment import FirstDeploymentFrame


@dataclass(frozen=True)
class LeaderRosterPresenceFields:
    """Actual saved-field return and observed leader presence at235CC.

    The historical carry API may keep unobserved fields as None. A Scene
    caller must consume the complete frame; present is never inferred from
    an invented carry/flag default or from its incoming roster view.
    """
    frame: FirstDeploymentFrame
    present: bool

    def validate(self, state):
        if type(self.frame) is not FirstDeploymentFrame or type(self.present) is not bool:
            raise ValueError('actual leader-roster frame and strict presence required')
        self.frame.validate(state)
        return self


@dataclass(frozen=True)
class ContactCollectionFields:
    """Actual234D2 return plus its legacy radius/origin WORD projection."""
    frame: FirstDeploymentFrame
    radius: Word
    x: Word
    y: Word

    def validate(self, state, complete=False):
        if type(self.frame) is not FirstDeploymentFrame:
            raise ValueError('actual contact return frame required')
        self.frame.validate(state, complete)
        for value in (self.radius, self.x, self.y):
            uint(value, 16)
        return self
