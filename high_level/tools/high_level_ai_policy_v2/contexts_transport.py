"""Live views and bounded values for AI neighbor, supply and staging decisions.

Views retain their actual bus identity. They are not snapshots of RAM, and the
capture order is defined by the query functions in business_routes.
"""
from dataclasses import dataclass
from .domain import Word, Long, Table, Cursor, PackedGroupCursor, checked_cursor, uint

RoutePredicate = bool


@dataclass(frozen=True)
class NeighborQueryViews:
    neighbors: Cursor
    owners: Table

    def __post_init__(self):
        checked_cursor(self.neighbors)
        self.neighbors.state.checked_table(self.owners)


@dataclass(frozen=True)
class PackedSupplyDecision:
    group: PackedGroupCursor
    price: Long
    cash: Long

    def __post_init__(self):
        checked_cursor(self.group)
        uint(self.price, 32)
        uint(self.cash, 32)


@dataclass(frozen=True)
class TransportRouteViews:
    first: Word
    second: Word
    budget: Word
    candidates: Cursor

    def __post_init__(self):
        uint(self.first, 16)
        uint(self.second, 16)
        uint(self.budget, 16)
        checked_cursor(self.candidates)


@dataclass(frozen=True)
class StagingSearchViews:
    group: PackedGroupCursor
    first: Word
    second: Word
    coordinates: Table
    owners: Table

    def __post_init__(self):
        checked_cursor(self.group)
        uint(self.first, 16)
        uint(self.second, 16)
        self.group.state.checked_table(self.coordinates)
        self.group.state.checked_table(self.owners)
