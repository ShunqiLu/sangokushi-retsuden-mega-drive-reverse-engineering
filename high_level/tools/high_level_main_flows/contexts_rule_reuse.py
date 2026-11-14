"""Caller-visible values of existing officer and terrain rules.

These are semantic results on one live state, not a complete CPU frame.
Retained upper words are explicit where the original partial writes expose them.
"""
from dataclasses import dataclass
from .domain import Long, Table, Cursor


@dataclass(frozen=True)
class DefenseProgressResult:
    officer_index: Long
    doubled_gain: Long
    progress: Table


@dataclass(frozen=True)
class MonthlyActionsResult:
    loop_counter: Long
    city_gates_end: Cursor


@dataclass(frozen=True)
class TerrainQueryResult:
    row: Long
    column: Long
    terrain: Long
    cost: Long
    costs: Table
