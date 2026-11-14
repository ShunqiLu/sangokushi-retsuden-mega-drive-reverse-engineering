"""Typed growth, candidate selection and message-layout operands.

Widths are compatibility contracts. These families are not a CPU frame: each
bundle describes one algorithm's actual operands and returned observations.
"""
from dataclasses import dataclass
from .domain import (SceneState, Table, Cursor, Long, Word, uint,
                     checked_state, checked_table, checked_cursor)


@dataclass(frozen=True)
class GrowthValues:
    selected: Long
    value: Long
    category: Long

    def validate(self, state):
        checked_state(state)
        for value in (self.selected, self.value, self.category):
            uint(value, 32)
        return self


@dataclass(frozen=True)
class GrowthResult:
    values: GrowthValues
    notification_requested: bool
    assignments: Table

    def validate(self, state):
        self.values.validate(state)
        if type(self.notification_requested) is not bool:
            raise ValueError('strict notification carry required')
        checked_table(self.assignments, state)
        return self


@dataclass(frozen=True)
class GrowthFrame:
    """Real retained growth inputs; A4/A5 are not initialized at662E4.

    Names denote the actual views on entry, not a claim that their prior
    natural purpose is known. No-growth returns retain these exact aliases.
    """
    values: GrowthValues
    attribute_pointer: Table
    owner_pointer: Table

    def validate(self, state):
        checked_state(state)
        if type(self.values) is not GrowthValues:
            raise ValueError('exact growth value bundle required')
        self.values.validate(state)
        checked_table(self.attribute_pointer, state)
        checked_table(self.owner_pointer, state)
        return self


@dataclass(frozen=True)
class FullGrowthResult:
    """Complete normal-return DATA views and partial NZVC at662E4.

    These are seven same-state views and three actual live values, not a CPU
    frame. X, full SR, exception/stack/interrupt state remain outside this ABI.
    A4/A5 are CC00/F427 after a completed growth, incoming otherwise.
    """
    values: GrowthValues
    strength: Table
    intellect: Table
    levels: Table
    thresholds: Table
    attribute_pointer: Table
    owner_pointer: Table
    assignments: Table
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if type(self.values) is not GrowthValues:
            raise ValueError('exact growth value bundle required')
        self.values.validate(state)
        for view in (self.strength, self.intellect, self.levels, self.thresholds,
                     self.attribute_pointer, self.owner_pointer, self.assignments):
            checked_table(view, state)
        if any(type(v) is not bool for v in
               (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('strict final growth NZVC required')
        return self


@dataclass(frozen=True)
class GrowthScanObservation:
    """One algorithm's observations, also usable by the narrow legacy API.

    None is explicitly unobserved, never a invented RAM address. Only the
    strict frame API may expose a FullGrowthResult; legacy callers observe
    values/C/A6 and cannot promote missing retained views to complete return.
    """
    values: GrowthValues
    strength: Table
    intellect: Table
    levels: Table
    thresholds: Table
    attribute_pointer: Table | None
    owner_pointer: Table | None
    assignments: Table
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def complete(self, state):
        if self.attribute_pointer is None or self.owner_pointer is None:
            raise ValueError('unobserved retained growth views cannot be a complete return')
        return FullGrowthResult(self.values, self.strength, self.intellect,
            self.levels, self.thresholds, self.attribute_pointer, self.owner_pointer,
            self.assignments, self.carry, self.zero, self.negative, self.overflow).validate(state)


@dataclass(frozen=True)
class OfficerSelection:
    count: Long
    force: Long
    scan: Long
    score: Long
    trait: Long
    displaced: Long
    displaced_score: Long
    selected: Long

    def validate(self, state):
        checked_state(state)
        for value in (self.count, self.force, self.scan, self.score, self.trait,
                      self.displaced, self.displaced_score, self.selected):
            uint(value, 32)
        return self


@dataclass(frozen=True)
class MessageLayout:
    symbol: Long
    position: Long
    stride: Long
    row_offset: Long
    first_plane: Long
    fill: Long
    shift_count: Long
    second_plane: Long
    destination: Cursor | None = None
    bitmap: Cursor | None = None
    previous_rows: Cursor | None = None

    def validate(self, state):
        checked_state(state)
        for value in (self.symbol, self.position, self.stride, self.row_offset,
                      self.first_plane, self.fill, self.shift_count, self.second_plane):
            uint(value, 32)
        for view in (self.destination, self.bitmap, self.previous_rows):
            if view is not None:
                checked_cursor(view, state)
        return self


@dataclass(frozen=True)
class MessageDispatch:
    selector: Long
    layout: MessageLayout
    continuation: Long

    def validate(self, state):
        self.layout.validate(state)
        uint(self.selector, 32)
        uint(self.continuation, 32)
        return self


def checked_context(value, kind, state):
    checked_state(state)
    if type(value) is not kind:
        raise ValueError('exact high-bank algorithm operands required')
    return value.validate(state)


@dataclass(frozen=True)
class ScrollingMessageAdvance:
    """A real timer effect and optional actual full message observation.

    layout=None is permitted only for effects-only caller entry before the due
    branch needs current CPU values. It is not an absent view inside a fabricated
    MessageLayout. timer_after_decrement is the actual SUBQ result, not final EFDA
    after an event reload, and not a full CPU or stack result.
    """
    layout: MessageLayout | None
    timer_after_decrement: Word

    def validate(self, state):
        checked_state(state)
        uint(self.timer_after_decrement, 16)
        if self.layout is not None:
            self.layout.validate(state)
        elif self.timer_after_decrement == 0:
            raise ValueError('due message requires actual complete carrier input')
        return self


@dataclass(frozen=True)
class MessageControlFields:
    """676C4/676F2 actual partial observations, not an invented MessageLayout."""
    value: Word
    field_if_written: Word | None
    destination_if_written: Cursor | None
    source_if_written: Cursor | None
    layout_after_handler: MessageLayout | None
    carry: bool
    zero: bool
    negative: bool
    overflow: bool
    tile_if_written: Word | None = None

    def validate(self, state):
        checked_state(state)
        uint(self.value, 16)
        if self.field_if_written is not None:
            uint(self.field_if_written, 16)
        if self.tile_if_written is not None:
            uint(self.tile_if_written, 16)
        for view in (self.destination_if_written, self.source_if_written):
            if view is not None:
                checked_cursor(view, state)
        if self.layout_after_handler is not None:
            if type(self.layout_after_handler) is not MessageLayout:
                raise ValueError('actual indexed handler current layout required')
            self.layout_after_handler.validate(state)
        if any(type(flag) is not bool for flag in
               (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('true 676F2 transaction conditions required')
        return self
