"""March plans: retained quantities and same-state live views, never RAM copies.

These contexts separate querying, cost calculation and compatibility commit.
They do not validate a natural-gameplay domain or replace original sentinels.
"""
from dataclasses import dataclass
from .domain import (Byte, Word, Long, Table, Cursor, checked_table,
                     checked_cursor, uint)

MarchPredicate = bool


@dataclass(frozen=True)
class UnownedNeighborViews:
    neighbors: Cursor
    coordinates: Table
    owners: Table

    def __post_init__(self):
        checked_cursor(self.neighbors)
        checked_table(self.coordinates, self.neighbors.state)
        checked_table(self.owners, self.neighbors.state)


@dataclass(frozen=True)
class MarchFunds:
    food: Table
    city_offset: Word
    available: Long

    def __post_init__(self):
        checked_table(self.food)
        uint(self.city_offset, 16, 'captured city food slot')
        uint(self.available, 32, 'once-read city food')


@dataclass(frozen=True)
class TwoOfficerTroopLoad:
    first_offset: Word
    second_offset: Word
    total: Long

    def __post_init__(self):
        uint(self.first_offset, 16, 'first wrapped troop offset')
        uint(self.second_offset, 16, 'second wrapped troop offset')
        uint(self.total, 32, 'wrapped two-officer troop load')


@dataclass(frozen=True)
class SupportOfficerViews:
    source: Cursor
    roster: Cursor
    troops: Table
    strengths: Table
    scratch: Cursor
    limits: Table
    loyalty: Table

    def __post_init__(self):
        checked_cursor(self.source)
        checked_cursor(self.roster, self.source.state)
        checked_cursor(self.scratch, self.source.state)
        for view in (self.troops, self.strengths, self.limits, self.loyalty):
            checked_table(view, self.source.state)


@dataclass(frozen=True)
class SupportRosterSize:
    count: Word
    accepted: MarchPredicate

    def __post_init__(self):
        uint(self.count, 16, 'retained support roster count')
        if type(self.accepted) is not bool:
            raise ValueError('resolved support roster decision required')


@dataclass(frozen=True)
class SupportTroopLoad:
    speed_sum: Byte
    total: Long
    count: Word

    def __post_init__(self):
        uint(self.speed_sum, 8, 'wrapped BYTE speed sum')
        uint(self.total, 32, 'wrapped support troop load')
        uint(self.count, 16, 'wrapped support member count')


@dataclass(frozen=True)
class MarchQuote:
    speed: Word
    duration: Word
    supply: Long

    def __post_init__(self):
        uint(self.speed, 16, 'retained average march speed')
        uint(self.duration, 16, 'retained march duration')
        uint(self.supply, 32, 'wrapped march supply quote')
