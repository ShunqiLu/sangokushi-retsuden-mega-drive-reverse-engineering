"""Named finite calendar carriers, not a CPU register or instruction state.

BYTE loads leave the rest of their original WORD live. These explicit entry
conditions preserve that compatibility without guessing the natural caller
domain. Message services and hardware are separate, possibly stopping effects.
"""
from dataclasses import dataclass
from .domain import Word, uint


@dataclass(frozen=True)
class MortalityContext:
    assignment_word: Word = 0
    owner_lookup_word: Word = 0

    def __post_init__(self):
        uint(self.assignment_word, 16)
        uint(self.owner_lookup_word, 16)


@dataclass(frozen=True)
class EventContext:
    owner_word: Word = 0

    def __post_init__(self):
        uint(self.owner_word, 16)


@dataclass(frozen=True)
class CalendarContext:
    mortality: MortalityContext = MortalityContext()
    events: EventContext = EventContext()
    replenishment_city_word: Word = 0

    def __post_init__(self):
        if type(self.mortality) is not MortalityContext:
            raise ValueError('typed mortality entry condition required')
        if type(self.events) is not EventContext:
            raise ValueError('typed calendar event entry condition required')
        uint(self.replenishment_city_word, 16)
