"""Typed operands for late battle phases and live numeric panels.

The shared PhaseFrame retains only the six observable semantic carriers.
Pointers below are live views, not copied records or a register dictionary.
PhaseFrame.actors carries inherited A6/A5 views at their actual current
locations. After deployment or presentation they may address the layout or
VDP rather than a roster. None denotes insufficient inherited-view evidence,
not a request to manufacture a default pair. This remains an ABI draft.
"""
from dataclasses import dataclass
from .domain import (SceneState, Table, Cursor, Long, uint, checked_state,
                     checked_table, checked_cursor)
from .contexts_early_phase import PhaseFrame


@dataclass(frozen=True)
class DigitPanelContext:
    source: Cursor
    frame: PhaseFrame

    def validate(self, state):
        checked_cursor(self.source, state)
        checked_phase(self.frame, state)
        return self


@dataclass(frozen=True)
class DigitPanelResult:
    source: Cursor
    frame: PhaseFrame

    def validate(self, state):
        checked_cursor(self.source, state)
        checked_phase(self.frame, state)
        return self


@dataclass(frozen=True)
class ForcePanelContext:
    leader: Table
    frame: PhaseFrame

    def validate(self, state):
        checked_table(self.leader, state)
        checked_phase(self.frame, state)
        return self


@dataclass(frozen=True)
class ActionIconContext:
    mode: Long
    frame: PhaseFrame

    def validate(self, state):
        checked_phase(self.frame, state)
        uint(self.mode, 32)
        return self


@dataclass(frozen=True)
class LatePhaseDispatch:
    slot_address: Long
    frame: PhaseFrame

    def validate(self, state):
        checked_phase(self.frame, state)
        uint(self.slot_address, 32)
        return self


def checked_phase(value, state):
    checked_state(state)
    if type(value) is not PhaseFrame:
        raise ValueError('exact immutable late-phase operands required')
    return value.validate(state)


def checked_context(value, kind, state):
    checked_state(state)
    if type(value) is not kind:
        raise ValueError('exact late-phase context required')
    return value.validate(state)
