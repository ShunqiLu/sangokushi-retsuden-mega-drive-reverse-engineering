"""Typed stream, palette and plane-row results for recovered scene logic.

Views are live same-domain operands. A video address is never a RAM cursor;
nonlocal row completion records the real discarded caller token explicitly.
"""
from dataclasses import dataclass
from .domain import (SceneState, Cursor, Table, Byte, Word, Long,
                     VideoPlaneAddress, StackContinuation, uint,
                     checked_state, checked_cursor, checked_table)
from .contexts_reuse import GlyphSavedValues
from .contexts_objects import SceneControllerFrame

@dataclass(frozen=True)
class PacketTransferValues:
    command: Long
    increment: Long
    address: Long
    spill: Long

    def validate(self):
        for value in (self.command, self.increment, self.address, self.spill):
            uint(value, 32)
        return self


@dataclass(frozen=True)
class VdpPacketResult:
    source: Cursor
    command_carrier: Long
    increment: Word
    values: PacketTransferValues | None = None

    def validate(self, state):
        checked_cursor(self.source, state)
        uint(self.command_carrier, 32)
        uint(self.increment, 16)
        if self.values is not None:
            if type(self.values) is not PacketTransferValues:
                raise ValueError('actual packet transfer values required')
            self.values.validate()
        return self


@dataclass(frozen=True)
class VdpStreamResult:
    source: Cursor
    video_address: VideoPlaneAddress
    command_carrier: Long

    def validate(self, state):
        checked_cursor(self.source, state)
        if type(self.video_address) is not VideoPlaneAddress:
            raise ValueError('explicit video address required')
        self.video_address.__post_init__()
        uint(self.command_carrier, 32)
        return self


@dataclass(frozen=True)
class SwappedByteRleRetained:
    """3AB52's actual incoming partial-write values: D1, D2 and D4."""
    marker: Long
    token: Long
    packed_word: Long

    def validate(self):
        for value in (self.marker, self.token, self.packed_word):
            uint(value, 32)
        return self


@dataclass(frozen=True)
class SwappedByteRleObservation:
    """Values truly observed by the one decoder, not invented incoming highs."""
    source: Cursor
    video_address: VideoPlaneAddress
    command_carrier: Long
    marker: Byte
    token: Byte
    last_word: Word | None
    live: SceneControllerFrame | None = None

    def validate(self, state):
        checked_cursor(self.source, state)
        if type(self.video_address) is not VideoPlaneAddress:
            raise ValueError('explicit video address required')
        self.video_address.__post_init__()
        uint(self.command_carrier, 32)
        uint(self.marker, 8)
        uint(self.token, 8)
        if self.last_word is not None:
            uint(self.last_word, 16)
        if self.live is not None:
            self.live.validate(state)
        return self


@dataclass(frozen=True)
class SwappedByteRleResult:
    source: Cursor
    video_address: VideoPlaneAddress
    command_carrier: Long
    marker_carrier: Long
    token_carrier: Long
    count_carrier: Long
    packed_word_carrier: Long
    last_word: Word | None
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_cursor(self.source, state)
        if type(self.video_address) is not VideoPlaneAddress:
            raise ValueError('explicit video address required')
        self.video_address.__post_init__()
        for value in (self.command_carrier, self.marker_carrier, self.token_carrier,
                      self.count_carrier, self.packed_word_carrier):
            uint(value, 32)
        if self.last_word is not None:
            uint(self.last_word, 16)
        for value in (self.carry, self.zero, self.negative, self.overflow):
            if type(value) is not bool:
                raise ValueError('exact observed condition outcomes required')
        return self


@dataclass(frozen=True)
class DictionaryStreamResult:
    source: Cursor
    dictionary_cursor: Cursor | None
    remaining: Word

    def validate(self, state):
        checked_cursor(self.source, state)
        if self.dictionary_cursor is not None:
            checked_cursor(self.dictionary_cursor, state)
        uint(self.remaining, 16)
        return self


@dataclass(frozen=True)
class GlyphRowsResult:
    source: Cursor
    destination: Cursor
    remaining: Long
    background: Long
    foreground: Long
    saved: GlyphSavedValues | None = None

    def validate(self, state):
        checked_cursor(self.source, state)
        checked_cursor(self.destination, state)
        uint(self.remaining, 32)
        uint(self.background, 32)
        uint(self.foreground, 32)
        if self.saved is not None:
            if type(self.saved) is not GlyphSavedValues:
                raise ValueError('actual saved glyph return required')
            self.saved.validate(state)
        return self


@dataclass(frozen=True)
class PaletteComponentResult:
    color: Long
    accumulated: Long
    component: Long

    def validate(self, state):
        checked_state(state)
        for value in (self.color, self.accumulated, self.component):
            uint(value, 32)
        return self


@dataclass(frozen=True)
class PaletteTransformResult:
    source: Cursor
    destination: Cursor
    shade_carrier: Long
    accumulated: Long
    count_carrier: Long | None = None
    color: Long | None = None
    component: Long | None = None

    def validate(self, state):
        checked_cursor(self.source, state)
        checked_cursor(self.destination, state)
        uint(self.shade_carrier, 32)
        uint(self.accumulated, 32)
        for value in (self.count_carrier, self.color, self.component):
            if value is not None:
                uint(value, 32)
        return self


@dataclass(frozen=True)
class PaletteCopyResult:
    index_carrier: Long
    source: Cursor
    destination: Cursor
    directory: Cursor

    def validate(self, state):
        uint(self.index_carrier, 32)
        for value in (self.source, self.destination, self.directory):
            checked_cursor(value, state)
        return self


@dataclass(frozen=True)
class PaletteCopyFields:
    """One copy transaction; None records an unobserved legacy D7 high WORD."""
    index_carrier: Long
    source: Cursor
    destination: Cursor
    directory: Cursor
    count_carrier: Long | None
    last_color_pair: Long

    def validate(self, state):
        uint(self.index_carrier, 32)
        uint(self.last_color_pair, 32)
        if self.count_carrier is not None:
            uint(self.count_carrier, 32)
        for view in (self.source, self.destination, self.directory):
            checked_cursor(view, state)
        return self


@dataclass(frozen=True)
class PaletteCopyCompleteResult:
    """Actual D0/D7, A1/A2/A3 and last MOVE.L NZVC for 3AB94."""
    index_carrier: Long
    source: Cursor
    destination: Cursor
    directory: Cursor
    count_carrier: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        uint(self.index_carrier, 32)
        uint(self.count_carrier, 32)
        for view in (self.source, self.destination, self.directory):
            checked_cursor(view, state)
        if any(type(value) is not bool for value in
               (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('actual complete palette NZVC required')
        return self


@dataclass(frozen=True)
class PaletteSnapshotResult:
    source: Cursor
    destination: Cursor

    def validate(self, state):
        checked_cursor(self.source, state)
        checked_cursor(self.destination, state)
        return self


@dataclass(frozen=True)
class PlaneRowContext:
    video_address: VideoPlaneAddress
    row_stride: Long
    column: Word
    rows_remaining: Word
    command_carrier: Long
    continuation: StackContinuation

    def validate(self, state):
        checked_state(state)
        if type(self.video_address) is not VideoPlaneAddress:
            raise ValueError('explicit plane address required')
        self.video_address.__post_init__()
        uint(self.row_stride, 32)
        uint(self.column, 16)
        uint(self.rows_remaining, 16)
        uint(self.command_carrier, 32)
        if type(self.continuation) is not StackContinuation:
            raise ValueError('actual decoder continuation required')
        self.continuation.__post_init__()
        return self


@dataclass(frozen=True)
class PlaneRowResult:
    video_address: VideoPlaneAddress
    column: Word
    rows_remaining: Word
    command_carrier: Long
    discarded_continuation: StackContinuation | None
    live: SceneControllerFrame | None = None

    def validate(self, state):
        checked_state(state)
        if type(self.video_address) is not VideoPlaneAddress:
            raise ValueError('explicit plane address required')
        self.video_address.__post_init__()
        uint(self.column, 16)
        uint(self.rows_remaining, 16)
        uint(self.command_carrier, 32)
        if self.discarded_continuation is not None:
            if type(self.discarded_continuation) is not StackContinuation:
                raise ValueError('actual discarded continuation required')
            self.discarded_continuation.__post_init__()
        if self.live is not None:
            self.live.validate(state)
        return self


@dataclass(frozen=True)
class PlaneStreamResult:
    source: Cursor
    video_address: VideoPlaneAddress
    command_carrier: Long
    column: Word
    rows_remaining: Word
    discarded_continuation: StackContinuation | None
    live: SceneControllerFrame | None = None

    def validate(self, state):
        checked_cursor(self.source, state)
        PlaneRowResult(self.video_address, self.column, self.rows_remaining,
                       self.command_carrier, self.discarded_continuation).validate(state)
        if self.live is not None:
            self.live.validate(state)
        return self


@dataclass(frozen=True)
class SceneFrameResult:
    source: Cursor
    frame_offset: Long

    def validate(self, state):
        checked_cursor(self.source, state)
        uint(self.frame_offset, 32)
        return self


@dataclass(frozen=True)
class ScenePlaybackResult:
    mode_offset: Long
    duration: Long

    def validate(self, state):
        checked_state(state)
        uint(self.mode_offset, 32)
        uint(self.duration, 32)
        return self


def checked_context(value, kind, state):
    checked_state(state)
    if type(value) is not kind:
        raise ValueError('exact scene-flow context required')
    return value.validate(state)


# Current same-state renderer field vocabularies; no widened State union.
from ..high_level_gameplay_flow.contexts_services import (
    SceneRefreshMemory, SceneRefreshBoundary, FirstDeploymentFrame, first_replace,
    _first_word, _first_byte, _first_long, _first_shift_word,
)
from ..high_level_gameplay_flow.business_services import (
    _scene_refresh_emit, _scene_refresh_flags, _scene_refresh_decrement,
)
from ..high_level_main_flows.business_movement_support import _movement_compare, _movement_binary_flags
