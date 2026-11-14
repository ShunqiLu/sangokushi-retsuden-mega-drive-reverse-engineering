"""Typed live-record and partial-value contracts for the original duel flow.

Confirmed widths and access order are compatibility facts.  Natural selector
domains and complete interrupt/exception behavior are not claimed here.
"""
from dataclasses import dataclass
from .domain import (
    Word, Long, Table, Cursor, StackContinuation, uint, checked_state,
    checked_table, checked_cursor, Boundary,
)


@dataclass(frozen=True)
class DuelConditionObservation:
    """Known NZVC observations; explicit None is unknown, never guessed flags."""
    carry: bool | None
    zero: bool | None
    negative: bool | None
    overflow: bool | None

    def validate(self):
        if any(value is not None and type(value) is not bool for value in
                (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('each observed duel condition must be bool or explicit unknown')
        return self

    def require(self, name):
        if name not in ('carry', 'zero', 'negative', 'overflow'):
            raise ValueError('named NZVC observation required')
        value = getattr(self, name)
        if value is None:
            raise Boundary('duel branch requires an unknown condition: ' + name)
        return value


@dataclass(frozen=True)
class DuelTurnFrame:
    """Eight current values and actual A0/A1/A2 roles at function-entry SP.

    actor/opponent are compatibility role names: a packet can return source and
    destination through them. They must not be reset to historical actor views.
    The manual menu's sprite likewise returns the SAT destination/template.
    Its caller's physical D0.W slot is read after the menu, preserving that
    current D0's upper WORD rather than an initial-frame snapshot.
    A3-A6, X/fullSR, IRQ and arbitrary return-token aliases are not modeled.
    """
    command: Long
    comparison: Long
    distance: Long
    factor: Long
    weapon_difference: Long
    working_value: Long
    response: Long
    variation: Long
    actor: Table
    opponent: Table
    lookup: Table
    stack: Cursor
    conditions: DuelConditionObservation

    def validate(self, state):
        checked_state(state)
        for value in (self.command, self.comparison, self.distance, self.factor,
                self.weapon_difference, self.working_value, self.response, self.variation):
            uint(value, 32, 'actual full duel turn value')
        for view in (self.actor, self.opponent, self.lookup):
            checked_table(view, state)
        checked_cursor(self.stack, state)
        if type(self.conditions) is not DuelConditionObservation:
            raise ValueError('explicit known/unknown duel conditions required')
        self.conditions.validate()
        return self


def checked_duel_turn(frame, state):
    if type(frame) is not DuelTurnFrame:
        raise ValueError('complete current DuelTurnFrame required')
    return frame.validate(state)


def checked_duel_action_outcome(value, state):
    from ..high_level_dynamic_flows.contexts_duel import DuelCompleteTurnOutcome
    if type(value) is not DuelCompleteTurnOutcome:
        raise Boundary('an indexed action must return its actual complete outcome')
    return value.validate(state)


@dataclass(frozen=True)
class DuelTurnOutcome:
    """A named finite continuation, not a fabricated RTS from the main loop."""
    phase: str
    frame: DuelTurnFrame
    discarded_continuation: StackContinuation | None

    def validate(self, state):
        if self.phase not in ('next_frame', 'next_frame_clear', 'fade', 'finished'):
            raise ValueError('actual duel continuation required')
        checked_duel_turn(self.frame, state)
        if self.discarded_continuation is not None:
            if type(self.discarded_continuation) is not StackContinuation:
                raise ValueError('actual consumed continuation required')
            self.discarded_continuation.__post_init__()
        return self


@dataclass(frozen=True)
class DuelLoadoutOutcome:
    """Known original commit path, not a side guessed from a SAT A0 return."""
    phase: str
    frame: DuelTurnFrame

    def validate(self, state):
        if self.phase not in ('first_committed', 'second_committed'):
            raise ValueError('actual loadout commit continuation required')
        checked_duel_turn(self.frame, state)
        return self


class DuelContinuationBoundary(Boundary):
    """A real unfinished continuation with its current complete live frame."""
    def __init__(self, target, frame, reason):
        uint(target, 32, 'actual continuation')
        if type(frame) is not DuelTurnFrame:
            raise ValueError('actual complete stopped caller required')
        self.target = target
        self.context = frame
        super().__init__(reason)


@dataclass(frozen=True)
class DuelRetainedValues:
    """Actual pending distance/weight/weapon/variation values, never zero fill.

    Their initial natural caller domain is unknown. A caller which cannot
    supply these live values must stop before a handler which consumes them.
    """
    distance: Long
    factor: Long
    weapon_difference: Long
    variation: Long

    def validate(self):
        for value in (self.distance, self.factor, self.weapon_difference, self.variation):
            uint(value, 32, 'retained duel value')
        return self


@dataclass(frozen=True)
class DuelControlContext:
    command: Long = 0
    mode: Long = 0

    def validate(self):
        uint(self.command, 32, 'command')
        uint(self.mode, 32, 'mode')
        return self


@dataclass(frozen=True)
class DuelGlyphContext:
    background: Long = 0
    foreground: Long = 0
    remaining: Long = 0

    def validate(self):
        uint(self.background, 32, 'background')
        uint(self.foreground, 32, 'foreground')
        uint(self.remaining, 32, 'remaining')
        return self


@dataclass(frozen=True)
class DuelActorContext:
    command: Long = 0
    comparison: Long = 0
    damage: Long = 0
    retained: DuelRetainedValues | None = None
    stack: Cursor | None = None
    live: DuelTurnFrame | None = None

    def validate(self):
        uint(self.command, 32, 'command')
        uint(self.comparison, 32, 'comparison')
        uint(self.damage, 32, 'damage')
        if self.retained is not None:
            if type(self.retained) is not DuelRetainedValues:
                raise ValueError('actual actor retained values required')
            self.retained.validate()
            if self.retained.distance != self.damage:
                raise ValueError('actor damage and retained distance must be the same current value')
        if self.stack is not None and not isinstance(self.stack, Cursor):
            raise ValueError('actual actor stack cursor required')
        if self.live is not None and type(self.live) is not DuelTurnFrame:
            raise ValueError('actual full actor caller required')
        return self


@dataclass(frozen=True)
class DuelActorFrame:
    """Six current algorithm values; None is unknown, never a zero substitute.

    The roles change through motion, strike and sprite emission. These are
    compatibility projections, not complete CPU/CCR/address-register state.
    """
    command: Long | None = None
    comparison: Long | None = None
    distance: Long | None = None
    factor: Long | None = None
    weapon_difference: Long | None = None
    variation: Long | None = None
    working_value: Long | None = None
    response: Long | None = None
    lookup: Table | None = None

    def validate(self):
        for value in (self.command, self.comparison, self.distance, self.factor,
                      self.weapon_difference, self.variation,
                      self.working_value, self.response):
            if value is not None:
                uint(value, 32, 'current actor value')
        if self.lookup is not None and type(self.lookup) not in (Table, Cursor):
            raise ValueError('actual actor lookup view required')
        return self

    @property
    def complete(self):
        return all(value is not None for value in (self.command, self.comparison,
            self.distance, self.factor, self.weapon_difference, self.variation))

    @property
    def retained(self):
        if any(value is None for value in (self.distance, self.factor,
                                           self.weapon_difference, self.variation)):
            return None
        return DuelRetainedValues(self.distance, self.factor,
                                  self.weapon_difference, self.variation).validate()


@dataclass(frozen=True)
class DuelRenderResult:
    frame: DuelActorFrame
    actor: Table | None
    opponent: Table | None
    stack: Cursor | None = None

    def validate(self, state):
        if type(self.frame) is not DuelActorFrame:
            raise ValueError('actual actor frame required')
        self.frame.validate()
        for view in (self.actor, self.opponent):
            if view is not None and (not isinstance(view, Table) or view.state is not state):
                raise ValueError('returned actor views must share live state')
        if self.stack is not None and (not isinstance(self.stack, Cursor) or self.stack.state is not state):
            raise ValueError('returned stack must share live state')
        return self


@dataclass(frozen=True)
class DuelActorResult:
    command: Long
    comparison: Long
    damage: Long
    frame: DuelActorFrame | None = None
    actor: Table | None = None
    opponent: Table | None = None
    stack: Cursor | None = None
    response: Long | None = None

    def validate(self):
        uint(self.command, 32, 'command')
        uint(self.comparison, 32, 'comparison')
        uint(self.damage, 32, 'damage')
        if self.response is not None:
            uint(self.response, 32, 'actual current response')
        if self.frame is not None:
            if type(self.frame) is not DuelActorFrame:
                raise ValueError('actual returned actor frame required')
            self.frame.validate()
            if (self.frame.command, self.frame.comparison, self.frame.distance) != (
                    self.command, self.comparison, self.damage):
                raise ValueError('three-value projection must agree with actual frame')
        return self

    @property
    def retained(self):
        return self.frame.retained if self.frame is not None else None


@dataclass(frozen=True)
class DuelContact:
    distance: Word
    relative_position: Word
    borrowed: bool
    frame: DuelActorFrame | None = None

    def __post_init__(self):
        uint(self.distance, 16, 'distance')
        uint(self.relative_position, 16, 'relative_position')
        if type(self.borrowed) is not bool:
            raise ValueError('borrowed must be bool')
        if self.frame is not None:
            if type(self.frame) is not DuelActorFrame:
                raise ValueError('actual contact frame required')
            self.frame.validate()


@dataclass(frozen=True)
class DuelProbability:
    sample: Long
    mask: Word
    threshold: Word
    borrowed: bool
    frame: DuelActorFrame | None = None

    def __post_init__(self):
        uint(self.sample, 32, 'sample')
        uint(self.mask, 16, 'mask')
        uint(self.threshold, 16, 'threshold')
        if type(self.borrowed) is not bool:
            raise ValueError('borrowed must be bool')
        if self.frame is not None:
            if type(self.frame) is not DuelActorFrame:
                raise ValueError('actual probability return frame required')
            self.frame.validate()


@dataclass(frozen=True)
class DuelOverrideResult:
    frame: DuelActorFrame
    override: Word

    def validate(self):
        if type(self.frame) is not DuelActorFrame:
            raise ValueError('actual override current frame required')
        self.frame.validate()
        uint(self.override, 16, 'actual override low WORD')
        if self.frame.variation is not None and self.frame.variation & 65535 != self.override:
            raise ValueError('override projection must agree with current variation')
        return self


@dataclass(frozen=True)
class DuelAIContext:
    command: Long = 0
    comparison: Long = 0
    threshold_offset: Word = 0
    override: Word = 0
    retained: DuelRetainedValues | None = None
    response: Long | None = None
    live: DuelTurnFrame | None = None

    def validate(self):
        uint(self.command, 32, 'command')
        uint(self.comparison, 32, 'comparison')
        uint(self.threshold_offset, 16, 'threshold_offset')
        uint(self.override, 16, 'override')
        if self.retained is not None:
            if type(self.retained) is not DuelRetainedValues:
                raise ValueError('actual retained duel values required')
            self.retained.validate()
        if self.response is not None:
            uint(self.response, 32, 'current full AI response')
            if self.response & 65535 != self.threshold_offset:
                raise ValueError('threshold must derive from current response low WORD')
            if self.retained is None or self.retained.variation & 65535 != self.override:
                raise ValueError('full AI override must derive from current variation low WORD')
        if self.live is not None and type(self.live) is not DuelTurnFrame:
            raise ValueError('actual full AI caller required')
        return self


@dataclass(frozen=True)
class DuelAIResult:
    command: Long
    comparison: Long
    threshold_offset: Word
    override: Word
    retained: DuelRetainedValues | None = None
    frame: DuelActorFrame | None = None
    response: Long | None = None
    live: DuelTurnFrame | None = None

    def validate(self):
        DuelAIContext(self.command, self.comparison,
                      self.threshold_offset, self.override, self.retained, self.response).validate()
        if self.frame is not None:
            if type(self.frame) is not DuelActorFrame:
                raise ValueError('actual current AI return frame required')
            self.frame.validate()
            if (self.frame.command, self.frame.comparison) != (self.command, self.comparison):
                raise ValueError('AI observed values must agree with actual frame')
            if self.frame.retained != self.retained:
                raise ValueError('AI retained projection must agree with actual frame')
        if self.live is not None:
            checked_duel_turn(self.live, self.live.actor.state)
            if (self.live.command, self.live.comparison, self.live.response) != (
                    self.command, self.comparison, self.response):
                raise ValueError('AI observations must project the actual live return')
        return self


@dataclass(frozen=True)
class DuelActionContext:
    actor: Table
    opponent: Table
    controls: DuelControlContext = DuelControlContext()
    threshold_offset: Word = 0
    retained: DuelRetainedValues | None = None
    continuation: StackContinuation = StackContinuation(0x27572)
    live: DuelTurnFrame | None = None

    def validate(self, state):
        if not isinstance(self.actor, Table) or self.actor.state is not state:
            raise ValueError('actor must be a live same-state Table')
        if not isinstance(self.opponent, Table) or self.opponent.state is not state:
            raise ValueError('opponent must be a live same-state Table')
        if type(self.controls) is not DuelControlContext:
            raise ValueError('typed duel controls required')
        self.controls.validate()
        uint(self.threshold_offset, 16, 'threshold_offset')
        if self.retained is not None:
            if type(self.retained) is not DuelRetainedValues:
                raise ValueError('actual retained duel values required')
            self.retained.validate()
        if type(self.continuation) is not StackContinuation:
            raise ValueError('real action continuation required')
        self.continuation.__post_init__()
        if self.live is not None:
            checked_duel_turn(self.live, state)
            if (self.live.actor is not self.actor or self.live.opponent is not self.opponent or
                    (self.live.command, self.live.comparison) !=
                    (self.controls.command, self.controls.mode)):
                raise ValueError('full action must use its actual current views and values')
        return self


@dataclass(frozen=True)
class DuelActionResult:
    controls: DuelControlContext
    completion: Word | None = 0
    retained: DuelRetainedValues | None = None
    discarded_continuation: StackContinuation | None = None
    live: DuelTurnFrame | None = None

    def validate(self, state=None):
        if type(self.controls) is not DuelControlContext:
            raise ValueError('typed duel controls required')
        self.controls.validate()
        if self.completion is not None:
            uint(self.completion, 16, 'completion')
        if self.retained is not None:
            if type(self.retained) is not DuelRetainedValues:
                raise ValueError('actual retained duel result required')
            self.retained.validate()
        if self.discarded_continuation is not None:
            if type(self.discarded_continuation) is not StackContinuation:
                raise ValueError('real discarded action continuation required')
            self.discarded_continuation.__post_init__()
        if self.live is not None:
            if type(self.live) is not DuelTurnFrame:
                raise ValueError('complete action return needs its actual frame')
            checked_duel_turn(self.live, self.live.actor.state if state is None else state)
            if (self.live.command, self.live.comparison) != (self.controls.command, self.controls.mode):
                raise ValueError('legacy action projection must agree with full current return')
        return self


@dataclass(frozen=True)
class DuelLaneResult:
    source: Cursor
    destination: Cursor
    remaining: Word
    repeat_value: Long
    pair_value: Long
    length_carrier: Long | None = None
    count_carrier: Long | None = None


@dataclass(frozen=True)
class DuelSpriteResult:
    destination: Cursor
    next_sprite: Word
    horizontal_extent: Word
    frame: DuelActorFrame | None = None
    stack: Cursor | None = None
    source: Cursor | None = None


@dataclass(frozen=True)
class DuelSceneContext:
    controls: DuelControlContext = DuelControlContext()
    glyphs: DuelGlyphContext = DuelGlyphContext()
    actor_values: DuelActorContext = DuelActorContext()
    retained: DuelRetainedValues | None = None
    stack: Cursor | None = None
    initialization: 'DuelInitializationContext | None' = None

    def validate(self):
        if type(self.controls) is not DuelControlContext:
            raise ValueError('typed duel controls required')
        if type(self.glyphs) is not DuelGlyphContext:
            raise ValueError('typed glyph colors/count required')
        if type(self.actor_values) is not DuelActorContext:
            raise ValueError('typed actor partial values required')
        self.controls.validate()
        self.glyphs.validate()
        self.actor_values.validate()
        if self.retained is not None:
            if type(self.retained) is not DuelRetainedValues:
                raise ValueError('explicit retained scene action values required')
            self.retained.validate()
        if self.stack is not None and not isinstance(self.stack, Cursor):
            raise ValueError('actual scene stack cursor required')
        if self.initialization is not None and type(self.initialization) is not DuelInitializationContext:
            raise ValueError('actual complete initialization live-in required')
        return self


@dataclass(frozen=True)
class DuelSceneResult:
    controls: DuelControlContext
    actor_values: DuelActorContext
    terminal_status_word: Word
    live: DuelTurnFrame | None = None


@dataclass(frozen=True)
class DuelPreparationContext:
    """Actual post-refresh panel live-in, not an initialization snapshot.

    Response is the complete current response carrier. The stack is the live
    semantic MOVEM backing cursor; caller BSR/JSR return addresses are not
    synthesized. All six actor values must be known before this chain runs.
    """
    frame: DuelActorFrame
    response: Long
    actor: Table
    opponent: Table
    stack: Cursor

    def validate(self, state):
        if type(self.frame) is not DuelActorFrame:
            raise ValueError('complete current preparation frame required')
        self.frame.validate()
        if not self.frame.complete:
            raise ValueError('all six current preparation values required')
        uint(self.response, 32, 'actual response carrier')
        for view in (self.actor, self.opponent):
            if not isinstance(view, Table) or view.state is not state:
                raise ValueError('preparation actors must share live state')
        if not isinstance(self.stack, Cursor) or self.stack.state is not state:
            raise ValueError('preparation requires the actual same-state stack')
        return self


@dataclass(frozen=True)
class DuelPreparationResult:
    """Distinct real continuations, not a claim of complete natural scene init.

    First-frame completion retains the current AI response. The actor family
    does not write that response operand; it is not the 27572 continuation.
    """
    phase: str
    preparation: DuelPreparationContext | None
    first_frame: DuelActorResult | None = None

    def validate(self, state):
        if self.phase not in ('repeat_first', 'needs_second_loadout', 'first_frame'):
            raise ValueError('actual preparation continuation required')
        if self.phase == 'first_frame':
            if self.preparation is not None or type(self.first_frame) is not DuelActorResult:
                raise ValueError('first frame returns its actual actor result only')
            self.first_frame.validate()
            if self.first_frame.frame is None or not self.first_frame.frame.complete:
                raise ValueError('complete actual first actor return required')
            for view in (self.first_frame.actor, self.first_frame.opponent, self.first_frame.stack):
                if not isinstance(view, Table) or view.state is not state:
                    raise ValueError('first frame returned views must share live state')
        else:
            if type(self.preparation) is not DuelPreparationContext or self.first_frame is not None:
                raise ValueError('preparation continuation must retain its current values')
            self.preparation.validate(state)
        return self


@dataclass(frozen=True)
class DuelInitializationContext:
    """Natural entry's read-before-write values and actual semantic MOVEM stack.

    Initial address operands are not invented: initialization replaces A0/A1
    before their first use, and AF1E defines its font source before AE8A saves it.
    The complete values are required because the early writes are partial WORD.
    """
    frame: DuelActorFrame
    response: Long
    glyph_work: Long
    stack: Cursor

    def validate(self, state):
        if type(self.frame) is not DuelActorFrame or not self.frame.complete:
            raise ValueError('all actual initialization values required')
        self.frame.validate()
        uint(self.response, 32)
        uint(self.glyph_work, 32)
        if not isinstance(self.stack, Cursor) or self.stack.state is not state:
            raise ValueError('actual same-state initialization stack required')
        return self


@dataclass(frozen=True)
class DuelInitializationResult:
    preparation: DuelPreparationContext
    glyph_work: Long
    glyph_source: Table

    def validate(self, state):
        if type(self.preparation) is not DuelPreparationContext:
            raise ValueError('actual initialization return required')
        self.preparation.validate(state)
        uint(self.glyph_work, 32)
        if not isinstance(self.glyph_source, Table) or self.glyph_source.state is not state:
            raise ValueError('current glyph source must share state')
        if (self.preparation.frame.working_value, self.preparation.frame.response,
                self.preparation.frame.lookup) != (self.glyph_work,
                self.preparation.response, self.glyph_source):
            raise ValueError('initialization projections must refer to the current full return')
        return self
