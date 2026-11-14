"""Named live scene operands, not a CPU/register snapshot.

The legacy six-value projection remains partial. A complete handoff carries
the actual controller frame, including all eight values, views and entry SP.
Defaults are conditional legacy inputs, never complete caller inputs.
"""
from dataclasses import dataclass, replace
from .domain import (SceneState, Table, Cursor, Long, uint, checked_state,
                     checked_cursor, checked_table, Boundary, u16, u32, low16)
from ..high_level_scene_flows.contexts_objects import (
    SceneControllerFrame, SceneControllerConditions, SceneControllerOutcome,
    checked_controller_frame)


@dataclass(frozen=True)
class BattleActors:
    """Two inherited live views at the current scene continuation.

    actor follows the original working object view, opponent its companion.
    Their physical A6/A5 provenance is documented in the private entry API.
    Phase helpers may leave a layout endpoint or a VDP data-port view here;
    these are not guaranteed to remain816A/826A actor rosters. Do not restore
    an earlier pair or dereference them until the actual consumer requires it.
    """
    actor: Table
    opponent: Table

    def validate(self, state):
        checked_table(self.actor, state)
        checked_table(self.opponent, state)
        return self


@dataclass(frozen=True)
class PhaseFrame:
    video_command: Long = 0
    foreground: Long = 0
    mode: Long = 0
    row_count: Long = 0
    tile: Long = 0
    glyph_tokens: Long = 0
    actors: BattleActors | None = None
    live: SceneControllerFrame | None = None

    def validate(self, state: SceneState):
        checked_state(state)
        for value in (self.video_command, self.foreground, self.mode,
                      self.row_count, self.tile, self.glyph_tokens):
            uint(value, 32)
        if self.actors is not None:
            if type(self.actors) is not BattleActors:
                raise ValueError('same-state live battle actors required')
            self.actors.validate(state)
        if self.live is not None:
            if type(self.live) is not SceneControllerFrame:
                raise ValueError('actual complete controller frame required')
            self.live.validate(state)
        return self


@dataclass(frozen=True)
class DecimalDigitsResult:
    value: Long
    destination: Cursor

    def validate(self, state: SceneState):
        uint(self.value, 32)
        checked_cursor(self.destination, state)
        return self


def checked_phase(state, frame):
    checked_state(state)
    if type(frame) is not PhaseFrame:
        raise ValueError('named full-width scene operands required')
    return frame.validate(state)


def phase_from_controller(state, live):
    """Project actual D0-D4/D7 and A6/A5; never manufacture missing operands."""
    live = checked_controller_frame(live, state)
    return PhaseFrame(live.x, live.y, live.attributes, live.palette, live.tile,
        live.layer, BattleActors(live.actor, live.traversal), live).validate(state)


def phase_operands(frame, conditions=None, **changes):
    """Commit only caller-proven phase effects into its current full handoff.

    Callers own their actual algorithm and observations. This helper performs
    no DATA read, restores no entry snapshot and claims no unobserved effect.
    """
    result = replace(frame, **changes)
    if result.live is None:
        return result
    live = replace(result.live, x=result.video_command, y=result.foreground,
        attributes=result.mode, palette=result.row_count, tile=result.tile,
        layer=result.glyph_tokens)
    if conditions is not None:
        live = replace(live, conditions=conditions)
    return replace(result, live=live)


def phase_controller_return(state, frame):
    """Require the real complete return, not a stale legacy five/six projection."""
    checked_phase(state, frame)
    if frame.live is None:
        raise Boundary('phase requires complete current eight-value/view/stack return')
    live = frame.live.validate(state)
    if (frame.video_command, frame.foreground, frame.mode, frame.row_count,
            frame.tile, frame.glyph_tokens) != (live.x, live.y, live.attributes,
            live.palette, live.tile, live.layer):
        raise Boundary('legacy phase algorithm has not supplied its actual full return')
    return live


def phase_enter_call(state, live, continuation):
    """Write the known original call's LONG token before any callee effect."""
    live = checked_controller_frame(live, state)
    uint(continuation, 32)
    called = replace(live, stack=live.stack.advance(-4))
    called.stack.set_long(0, continuation)
    return called


def phase_finish_call(state, actual, continuation):
    """Consume the actual RTS observation, not a saved expected entry cursor."""
    uint(continuation, 32)
    if type(actual) is SceneControllerOutcome:
        actual.validate(state)
        if actual.discarded_continuation is not None:
            return actual
        actual = actual.frame
    actual = checked_controller_frame(actual, state)
    returned_to = actual.stack.long()
    if returned_to != continuation:
        raise Boundary('phase call actual RTS target differs from its known continuation')
    return replace(actual, stack=actual.stack.advance(4))


def phase_logic(value, width=16):
    """Observed original MOVE/TST/AND result; X and full SR are not modeled."""
    mask = (1 << width) - 1
    value &= mask
    return SceneControllerConditions(False, value == 0,
        bool(value & (1 << (width - 1))), False)


def phase_compare(left, right, width=16):
    """Observed original CMP operands, with no reread to discover flags."""
    mask, sign = (1 << width) - 1, 1 << (width - 1)
    left, right = left & mask, right & mask
    result = (left - right) & mask
    return SceneControllerConditions(left < right, result == 0,
        bool(result & sign), bool((left ^ right) & (left ^ result) & sign))


def phase_add_word(value, amount):
    """Only the observed WORD ADDQ used by these phase counters."""
    value = u16(value)
    result = u16(value + amount)
    return SceneControllerConditions(value + amount > 65535, result == 0,
        bool(result & 32768), bool(~(value ^ amount) & (value ^ result) & 32768))


def phase_shifted_selector(value):
    """The actual two-bit WORD ASL; original high WORD is retained by caller."""
    shifted, overflow, carry = low16(value), False, False
    for _ in range(2):
        previous = shifted
        carry = bool(previous & 32768)
        shifted = u16(previous << 1)
        overflow = overflow or bool((previous ^ shifted) & 32768)
    return shifted, SceneControllerConditions(carry, shifted == 0,
        bool(shifted & 32768), overflow)


def phase_bit(frame, selected):
    """Memory BTST updates only Z; other observed or unknown conditions stay live."""
    if frame.live is None:
        return None
    previous = frame.live.conditions
    return SceneControllerConditions(previous.carry, not selected,
        previous.negative, previous.overflow)
