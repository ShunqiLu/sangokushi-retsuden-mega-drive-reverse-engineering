"""Training policy values, independent of RAM layout and machine command IDs.

The alternate order's wider gameplay purpose is not inferred here. Empty or
excluded rosters retain the original 0xFFFF pair; they are not silently treated
as a new 'no order' rule. These values contain no live views or CPU state.
"""
from dataclasses import dataclass
from enum import Enum

from .domain import Word, uint


@dataclass(frozen=True)
class TrainingCandidate:
    """Lowest observed training WORD and its full, unmasked roster member ID."""

    minimum_score: Word
    officer_id: Word

    def __post_init__(self):
        uint(self.minimum_score, 16, 'minimum training score')
        uint(self.officer_id, 16, 'training candidate roster ID')


class TrainingOrder(Enum):
    """Policy choices, not the original command numbers stored in RAM."""

    TRAIN = 'train'
    ALTERNATE = 'alternate'


def checked_training_candidate(value):
    if type(value) is not TrainingCandidate:
        raise ValueError('immutable TrainingCandidate required')
    uint(value.minimum_score, 16, 'minimum training score')
    uint(value.officer_id, 16, 'training candidate roster ID')
    return value


def checked_training_order(value):
    if type(value) is not TrainingOrder:
        raise ValueError('named TrainingOrder required')
    return value
