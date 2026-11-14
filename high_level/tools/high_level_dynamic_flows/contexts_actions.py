"""Live object-action, roster, glyph and dynamic-dispatch contracts."""
from dataclasses import dataclass
from .domain import (SceneState, Table, Cursor, Long, StackContinuation, uint, checked_state,
                     checked_table, checked_cursor)
from ..high_level_scene_flows.contexts_objects import (SceneRenderFrame,
    SpriteBatchContext, SpriteBatchResult, ObjectPositionOffset, ObjectOverlapOutcome,
    SceneControllerConditions, checked_controller_frame)
from ..high_level_scene_flows.contexts_duel import DuelGlyphContext


@dataclass(frozen=True)
class ObjectActionResult:
    actor: Table
    opponent: Table
    frame: SceneRenderFrame
    # Historical token already consumed by the actual local callee. This is
    # evidence of that return path, not authority for another caller to pop it.
    discarded_continuation: StackContinuation | None = None

    def validate(self, state):
        checked_table(self.actor, state)
        checked_table(self.opponent, state)
        self.frame.validate(state)
        if self.discarded_continuation is not None:
            if type(self.discarded_continuation) is not StackContinuation:
                raise ValueError('actual locally discarded continuation required')
            uint(self.discarded_continuation.return_carrier, 32)
        return self


@dataclass(frozen=True)
class ObjectVectorContext:
    actor: Table
    opponent: Table
    frame: SceneRenderFrame
    selector: Long

    def validate(self, state):
        ObjectActionResult(self.actor, self.opponent, self.frame).validate(state)
        uint(self.selector, 32)
        return self


@dataclass(frozen=True)
class ObjectRosterTotals:
    first_total: Long
    second_total: Long
    first_count: Long
    second_count: Long
    command: Long
    roster_end: Cursor

    def validate(self, state):
        for value in (self.first_total, self.second_total, self.first_count,
                      self.second_count, self.command):
            uint(value, 32)
        checked_cursor(self.roster_end, state)
        return self


@dataclass(frozen=True)
class ObjectGlyphResult:
    glyphs: DuelGlyphContext
    source: Cursor
    tile_counter: Long
    officer_offset: Long

    def validate(self, state):
        self.glyphs.validate()
        checked_cursor(self.source, state)
        uint(self.tile_counter, 32)
        uint(self.officer_offset, 32)
        return self


@dataclass(frozen=True)
class TileUploadResult:
    source: Cursor
    bank: Cursor
    frame: SceneRenderFrame

    def validate(self, state):
        checked_cursor(self.source, state)
        checked_cursor(self.bank, state)
        self.frame.validate(state)
        return self


def checked_action(state, actor, opponent, frame):
    checked_state(state)
    return ObjectActionResult(actor, opponent, frame).validate(state)
