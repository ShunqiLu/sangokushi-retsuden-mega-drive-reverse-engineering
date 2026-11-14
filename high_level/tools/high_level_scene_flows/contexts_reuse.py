"""Real same-state contracts for selected shared scene operations."""
from dataclasses import dataclass
from .domain import Byte,Word,Long,Cursor,Table,uint,checked_cursor,checked_table

@dataclass(frozen=True)
class GlyphSavedValues:
    """Actual MOVEM operands. Restoration reads the live backing, not this tuple."""
    working: Long
    repeat: Long
    response: Long
    pixels: Long
    glyph_source: Table
    stack: Cursor

    def validate(self, state):
        for value in (self.working, self.repeat, self.response, self.pixels):
            uint(value, 32)
        checked_table(self.glyph_source, state)
        checked_cursor(self.stack, state)
        return self

@dataclass(frozen=True)
class GlyphColors:
    background: Long
    foreground: Long

    def __post_init__(self):
        uint(self.background, 32)
        uint(self.foreground, 32)

@dataclass(frozen=True)
class GlyphStreamResult:
    tokens: Cursor
    destination: Cursor
    remaining_carrier: Long
    saved: GlyphSavedValues | None = None

    def __post_init__(self):
        checked_cursor(self.tokens)
        checked_cursor(self.destination, self.tokens.state)
        uint(self.remaining_carrier, 32)
        if self.saved is not None:
            if type(self.saved) is not GlyphSavedValues:
                raise ValueError('actual restored glyph values required')
            self.saved.validate(self.tokens.state)

@dataclass(frozen=True)
class SpritePacketContext:
    """Current packet operands and observed NZVC, not a CPU dictionary.

    Old partial callers may leave conditions explicitly unknown. Complete
    packet generation and the six actual handlers return real observations.
    Stack is the current function-entry pointer, not a fabricated token bus.
    """
    command: Long
    rows: Long
    row_command: Long
    remaining: Long
    token: Long
    run_count: Long
    response: Long
    rows_remaining: Long
    source: Cursor
    destination: Cursor
    glyph_source: Table
    stack: Cursor
    carry: bool | None = None
    zero: bool | None = None
    negative: bool | None = None
    overflow: bool | None = None

    def validate(self, state):
        for value in (self.command, self.rows, self.row_command, self.remaining,
                      self.token, self.run_count, self.response, self.rows_remaining):
            uint(value, 32)
        for view in (self.source, self.destination, self.stack):
            checked_cursor(view, state)
        checked_table(self.glyph_source, state)
        if any(value is not None and type(value) is not bool for value in
               (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('packet conditions must be bool or explicit unknown')
        return self

@dataclass(frozen=True)
class VideoClearResult:
    response: Long
    variation: Long
    destination: Cursor

    def validate(self, state):
        uint(self.response, 32)
        uint(self.variation, 32)
        checked_cursor(self.destination, state)
        return self

@dataclass(frozen=True)
class SpriteControlContext:
    token: Word
    command: Long
    row_remaining: Word
    source: Cursor
    destination: Cursor

    def __post_init__(self):
        uint(self.token, 16)
        uint(self.command, 32)
        uint(self.row_remaining, 16)
        checked_cursor(self.source)
        checked_cursor(self.destination, self.source.state)

@dataclass(frozen=True)
class SpriteControlResult:
    command: Long
    row_remaining: Word

    def __post_init__(self):
        uint(self.command, 32)
        uint(self.row_remaining, 16)

@dataclass(frozen=True)
class ControlChoice:
    command:Long
    mode_carrier:Long

    def __post_init__(self):
        uint(self.command,32)
        uint(self.mode_carrier,32)

# Same-state sole808A/83C8 refresh authorities; no duplicate mailbox or poll loop.
from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory, FirstDeploymentFrame
from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields, wait_for_scene_sound_byte_fields
