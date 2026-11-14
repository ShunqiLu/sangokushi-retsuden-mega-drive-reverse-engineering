"""Typed queue, command, glyph and presentation operands on one live state."""
from dataclasses import dataclass
from .domain import (Long, Table, Cursor, VideoPlaneAddress, uint, checked_state,
                     checked_table, checked_cursor)


@dataclass(frozen=True)
class CityCommandValues:
    value: Long
    field: Long
    member: Long
    count: Long
    readiness_loss: Long
    troop_rate: Long
    force_index: Long
    selected: Long
    packet: Cursor | None
    roster: Cursor | None
    destination: Cursor | None
    assignments: Table | None
    troops: Table | None
    readiness: Table | None
    scratch: Table | None

    def validate(self, state):
        checked_state(state)
        for value in (self.value, self.field, self.member, self.count, self.readiness_loss,
                      self.troop_rate, self.force_index, self.selected):
            uint(value, 32)
        for view in (self.packet, self.roster, self.destination):
            if view is not None:
                checked_cursor(view, state)
        for view in (self.assignments, self.troops, self.readiness, self.scratch):
            if view is not None:
                checked_table(view, state)
        return self


@dataclass(frozen=True)
class GlyphTileLayout:
    value: Long
    row_stride: Long
    remaining: Long
    glyph: Long
    rows: Long
    shift_count: Long
    packed_bits: Long
    pixels: Long
    video_command: Long
    counts: Cursor | None
    identifiers: Cursor | None
    bitmap: Cursor | None
    destination: Cursor | None

    def validate(self, state):
        checked_state(state)
        for value in (self.value, self.row_stride, self.remaining, self.glyph,
                      self.rows, self.shift_count, self.packed_bits, self.pixels,
                      self.video_command):
            uint(value, 32)
        for view in (self.counts, self.identifiers, self.bitmap, self.destination):
            if view is not None:
                checked_cursor(view, state)
        return self


@dataclass(frozen=True)
class ScenePresentation:
    command: Long
    foreground: Long
    mode: Long
    rows: Long
    tile: Long
    stride: Long
    palette: Long
    remaining: Long
    source: Cursor | None
    destination: Cursor | None
    actor: Table | None
    opponent: Table | None
    video_address: VideoPlaneAddress | None = None

    def validate(self, state):
        checked_state(state)
        for value in (self.command, self.foreground, self.mode, self.rows,
                      self.tile, self.stride, self.palette, self.remaining):
            uint(value, 32)
        for view in (self.source, self.destination):
            if view is not None:
                checked_cursor(view, state)
        for view in (self.actor, self.opponent):
            if view is not None:
                checked_table(view, state)
        if self.video_address is not None:
            if type(self.video_address) is not VideoPlaneAddress:
                raise ValueError('independent video address required')
            uint(self.video_address.carrier, 32)
        return self


@dataclass(frozen=True)
class SceneCall:
    operands: CityCommandValues | GlyphTileLayout | ScenePresentation
    continuation: Long

    def validate(self, state):
        if type(self.operands) not in (CityCommandValues, GlyphTileLayout, ScenePresentation):
            raise ValueError('known scene-support call operands required')
        self.operands.validate(state)
        uint(self.continuation, 32)
        return self


def checked_context(value, kind, state):
    checked_state(state)
    if type(value) is not kind:
        raise ValueError('exact scene-support operands required')
    return value.validate(state)
