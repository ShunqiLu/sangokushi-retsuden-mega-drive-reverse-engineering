"""Semantic operands and real continuation outcomes for duel handlers.

The retained LONGs make original partial-WORD changes explicit. Views remain
live; these contracts contain no virtual CPU, register dictionary or code.
"""
from dataclasses import dataclass
from .domain import (SceneState, Table, Long, Word, StackContinuation, uint,
                     checked_state, checked_table)
from ..high_level_scene_flows.contexts_duel import (DuelControlContext,
    DuelTurnFrame, DuelConditionObservation, checked_duel_turn)


@dataclass(frozen=True)
class DuelRuleFrame:
    command: Long = 0
    comparison: Long = 0
    distance: Long = 0
    factor: Long = 0
    weapon_difference: Long = 0
    variation: Long = 0
    live: object | None = None

    def validate(self, state):
        checked_state(state)
        for value in (self.command, self.comparison, self.distance,
                      self.factor, self.weapon_difference, self.variation):
            uint(value, 32)
        if self.live is not None:
            from ..high_level_scene_flows.contexts_duel import DuelTurnFrame, checked_duel_turn
            if type(self.live) is not DuelTurnFrame:
                raise ValueError('actual complete current duel frame required')
            checked_duel_turn(self.live, state)
            if (self.command, self.comparison, self.distance, self.factor,
                    self.weapon_difference, self.variation) != (
                    self.live.command, self.live.comparison, self.live.distance,
                    self.live.factor, self.live.weapon_difference, self.live.variation):
                raise ValueError('legacy rule projection must agree with the current frame')
        return self


@dataclass(frozen=True)
class DuelTurnContext:
    actor: Table
    opponent: Table
    frame: DuelRuleFrame = DuelRuleFrame()
    continuation: StackContinuation = StackContinuation(0x27572)

    def validate(self, state):
        checked_table(self.actor, state)
        checked_table(self.opponent, state)
        if type(self.frame) is not DuelRuleFrame:
            raise ValueError('duel rule operands required')
        self.frame.validate(state)
        if self.frame.live is not None and (
                self.actor is not self.frame.live.actor or self.opponent is not self.frame.live.opponent):
            raise ValueError('action views must be the actual current frame views')
        if type(self.continuation) is not StackContinuation:
            raise ValueError('real indexed-call continuation required')
        self.continuation.__post_init__()
        return self


@dataclass(frozen=True)
class DuelTurnOutcome:
    frame: DuelRuleFrame
    discarded_continuation: StackContinuation | None = None

    def validate(self, state):
        self.frame.validate(state)
        if self.discarded_continuation is not None:
            if type(self.discarded_continuation) is not StackContinuation:
                raise ValueError('real discarded continuation required')
            self.discarded_continuation.__post_init__()
        return self


@dataclass(frozen=True)
class DuelSpacingResult:
    frame: DuelRuleFrame
    borrowed: bool

    def validate(self, state):
        self.frame.validate(state)
        if type(self.borrowed) is not bool:
            raise ValueError('strict original subtraction carry required')
        return self


@dataclass(frozen=True)
class DuelCompleteTurnOutcome:
    """Actual current values plus a consumed real indexed-call continuation.

    Ordinary return has no discarded continuation. Neither the response nor
    an assumed constant can replace the LONG actually read from the live stack.
    """
    frame: object
    discarded_continuation: StackContinuation | None = None

    def validate(self, state):
        from ..high_level_scene_flows.contexts_duel import checked_duel_turn
        checked_duel_turn(self.frame, state)
        if self.discarded_continuation is not None:
            if type(self.discarded_continuation) is not StackContinuation:
                raise ValueError('actual discarded continuation required')
            self.discarded_continuation.__post_init__()
            if self.frame.command != self.discarded_continuation.return_carrier:
                raise ValueError('popped continuation and actual current command must agree')
        return self


def checked_duel_context(value, state):
    if type(value) is not DuelTurnContext:
        raise ValueError('exact duel turn context required')
    return value.validate(state)
