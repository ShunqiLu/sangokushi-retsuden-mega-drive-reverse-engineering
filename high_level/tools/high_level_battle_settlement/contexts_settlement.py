"""Meaningful fixed-width values and same-state packed-tail views."""
from dataclasses import dataclass
from .domain import BattleState, Table, Cursor, Word, Long, uint


@dataclass(frozen=True)
class RatioInputs:
    numerator: Long
    denominator: Long

    def __post_init__(self):
        uint(self.numerator, 32, 'live loss numerator')
        uint(self.denominator, 32, 'live loss denominator')


@dataclass(frozen=True)
class PackedTailRepair:
    deleted: Word
    copy_source: Table
    copy_target: Table
    remaining_count: Word

    def __post_init__(self):
        uint(self.deleted, 16, 'original deletion flag')
        uint(self.remaining_count, 16, 'packed count carrier')
        for view in (self.copy_source, self.copy_target):
            if type(view) not in (Table, Cursor) or type(view.state) is not BattleState:
                raise ValueError('live battle packed-tail views required')
        if self.copy_source.state is not self.copy_target.state:
            raise ValueError('one live battle state required')
