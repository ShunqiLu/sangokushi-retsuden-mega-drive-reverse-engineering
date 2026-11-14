"""Recruitment domain values and live views, never a register frame.

All WORD lanes keep their original wrapped values and sentinels. Candidate and
selected-officer identities are deliberately distinct in the commit workflow.
"""
from dataclasses import dataclass
from enum import Enum

from .domain import Cursor, Table, Word, checked_cursor, checked_table, uint

# A business predicate is an ordinary bool, not a CCR/register-carrier object.
RecruitmentPredicate = bool


@dataclass(frozen=True)
class RecruitmentBest:
    score: Word
    officer: Word
    city: Word

    def __post_init__(self):
        for value in (self.score, self.officer, self.city):
            uint(value, 16, 'recruitment best WORD')


@dataclass(frozen=True)
class RecruitmentCandidate:
    score: Word
    officer: Word
    city: Word
    primary_score: Word
    secondary_score: Word

    def __post_init__(self):
        for value in (self.score, self.officer, self.city, self.primary_score, self.secondary_score):
            uint(value, 16, 'recruitment candidate WORD')


@dataclass(frozen=True)
class RecruitmentNeighborViews:
    neighbors: Cursor
    force: Word
    primary: Table
    secondary: Table
    status: Table
    owners: Table
    processed: Table

    def __post_init__(self):
        checked_cursor(self.neighbors)
        uint(self.force, 16, 'recruiting force WORD')
        for view in (self.primary, self.secondary, self.status, self.owners, self.processed):
            checked_table(view, self.neighbors.state)


class RecruitmentOrder(Enum):
    FALLBACK = 'fallback'
    ATTEMPT = 'attempt'
    RECRUIT = 'recruit'


def checked_recruitment_best(value):
    if type(value) is not RecruitmentBest:
        raise ValueError('immutable RecruitmentBest required')
    for lane in (value.score, value.officer, value.city):
        uint(lane, 16, 'recruitment best WORD')
    return value


def checked_recruitment_candidate(value):
    if type(value) is not RecruitmentCandidate:
        raise ValueError('immutable RecruitmentCandidate required')
    for lane in (value.score, value.officer, value.city, value.primary_score, value.secondary_score):
        uint(lane, 16, 'recruitment candidate WORD')
    return value


def checked_recruitment_submission_order(value):
    if type(value) is not RecruitmentOrder or value is RecruitmentOrder.ATTEMPT:
        raise ValueError('resolved FALLBACK/RECRUIT order required')
    return value
