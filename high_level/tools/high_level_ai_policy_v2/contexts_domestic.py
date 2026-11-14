"""City-resource decisions, retained values and actual same-state live views.

No original RAM/data bytes or register frames live here. FUNDED/LIMITED name the
balance decision, not an unproved meaning of original command codes 7 and 4.
"""
from dataclasses import dataclass
from enum import Enum

from .domain import Cursor, Long, Table, Word, checked_cursor, checked_table, uint

DomesticPredicate = bool


@dataclass(frozen=True)
class DomesticOfficer:
    score: Word
    officer: Word

    def __post_init__(self):
        uint(self.score, 16, 'domestic officer score')
        uint(self.officer, 16, 'domestic officer identity')


@dataclass(frozen=True)
class CityBudgetBalance:
    gold: Table
    city_offset: Word
    balance: Long

    def __post_init__(self):
        checked_table(self.gold)
        uint(self.city_offset, 16, 'captured city budget offset')
        uint(self.balance, 32, 'once-read budget balance')


@dataclass(frozen=True)
class ResourceSupportViews:
    force: Word
    current_city: Word
    troops: Table
    gold: Table
    rice: Table
    processed: Table
    owners: Cursor

    def __post_init__(self):
        checked_cursor(self.owners)
        uint(self.force, 16, 'resource support force')
        uint(self.current_city, 16, 'retained current city')
        for view in (self.troops, self.gold, self.rice, self.processed):
            checked_table(view, self.owners.state)


@dataclass(frozen=True)
class CitySupplyRequirement:
    required: Long
    next_filter: Table

    def __post_init__(self):
        uint(self.required, 32, 'city supply requirement')
        checked_table(self.next_filter)


@dataclass(frozen=True)
class ResourceSupportCandidate:
    total: Long
    city: Word

    def __post_init__(self):
        uint(self.total, 32, 'wrapped support resources')
        uint(self.city, 16, 'support city or sentinel')


class CityResourceOrder(Enum):
    FUNDED = 'funded'
    LIMITED = 'limited'


def checked_city_resource_order(value):
    if type(value) is not CityResourceOrder:
        raise ValueError('resolved CityResourceOrder required')
    return value
