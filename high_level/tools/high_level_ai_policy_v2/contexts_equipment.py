"""Equipment purchase values and live views, without machine-register frames.

These values separate a quote/budget decision from compatibility storage. Views
share one actual GameState; no roster, attribute, level or asset stream is
snapshotted. Unknown gameplay intent is not inferred from storage offsets.
"""
from dataclasses import dataclass
from enum import Enum

from .domain import Cursor, Long, Table, Word, checked_cursor, checked_table, uint


@dataclass(frozen=True)
class EquipmentPurchaseViews:
    """Entry views and once-read balance/location retained through the batch."""

    roster: Cursor
    attributes: Table
    gold: Table
    equipment: Table
    city_offset: Word
    initial_balance: Long
    retained_level: Word

    def __post_init__(self):
        checked_cursor(self.roster)
        for view in (self.attributes, self.gold, self.equipment):
            checked_table(view, self.roster.state)
        uint(self.city_offset, 16, 'captured city gold offset')
        uint(self.initial_balance, 32, 'entry equipment balance')
        uint(self.retained_level, 16, 'retained equipment level WORD')


@dataclass(frozen=True)
class OfficerEquipmentCategories:
    """Live category stream and the member's original three-BYTE row offset."""

    categories: Cursor
    equipment_row: Word

    def __post_init__(self):
        checked_cursor(self.categories)
        uint(self.equipment_row, 16, 'member equipment row')


@dataclass(frozen=True)
class EquipmentQuote:
    """A category upgrade with the full next-level WORD and actual LONG price."""

    category: Word
    next_level: Word
    price: Long

    def __post_init__(self):
        uint(self.category, 16, 'equipment category')
        uint(self.next_level, 16, 'next equipment level')
        uint(self.price, 32, 'equipment price')


class EquipmentBudgetDecision(Enum):
    PURCHASE = 'purchase'
    REJECT = 'reject'


def checked_equipment_quote(value):
    if type(value) is not EquipmentQuote:
        raise ValueError('immutable EquipmentQuote required')
    uint(value.category, 16, 'equipment category')
    uint(value.next_level, 16, 'next equipment level')
    uint(value.price, 32, 'equipment price')
    return value


def checked_equipment_views(value):
    if type(value) is not EquipmentPurchaseViews:
        raise ValueError('same-state EquipmentPurchaseViews required')
    checked_cursor(value.roster)
    for view in (value.attributes, value.gold, value.equipment):
        checked_table(view, value.roster.state)
    uint(value.city_offset, 16, 'captured city gold offset')
    uint(value.initial_balance, 32, 'entry equipment balance')
    uint(value.retained_level, 16, 'retained equipment level WORD')
    return value
