"""Sum the live roster's troop values, stopping before a negative member WORD.

The result wraps like the original: a 32-bit total and a 16-bit member count.
The target ABI and original addresses live in the compiler, not this rule.
"""
from .domain import LongTable, WordCursor, s16, u16, u32


def sum_group_troops(roster: WordCursor, troops: LongTable) -> tuple[int, int]:
    total = u32(0)
    count = u16(0)
    while True:
        member = roster.read_word()
        if s16(member) < 0:
            return total, count
        entity = member & 255
        count = u16(count + 1)
        total = u32(total + troops[entity])
