"""Named live-operand contracts for campaign/title controls and services."""
from dataclasses import dataclass
from .contexts_map import MapCoordinate
from .domain import Cursor, Table, Long, Word, uint, checked_cursor, checked_table


@dataclass(frozen=True)
class SceneTick:
    """A RAM-driven scene service with no invented input DATA."""
    def validate(self, state):
        return self


@dataclass(frozen=True)
class SoundWord:
    command: Word
    def validate(self, state):
        uint(self.command, 16)
        return self


@dataclass(frozen=True)
class GlyphStyle:
    background: Long
    foreground: Long
    def validate(self, state):
        uint(self.background, 32)
        uint(self.foreground, 32)
        return self


@dataclass(frozen=True)
class GlyphPlacement:
    source: Cursor
    video_command: Long
    foreground: Long
    tile: Long
    def validate(self, state):
        checked_cursor(self.source, state)
        for value in (self.video_command, self.foreground, self.tile):
            uint(value, 32)
        return self


@dataclass(frozen=True)
class CameraStrip:
    coordinate_carrier: Long
    def validate(self, state):
        uint(self.coordinate_carrier, 32)
        return self


@dataclass(frozen=True)
class SelectedCity:
    city: Word
    def validate(self, state):
        uint(self.city, 16)
        return self


@dataclass(frozen=True)
class LeaderRoster:
    count: Word
    def validate(self, state):
        uint(self.count, 16)
        return self


@dataclass(frozen=True)
class SelectedOfficer:
    officer: Word
    def validate(self, state):
        uint(self.officer, 16)
        return self


@dataclass(frozen=True)
class SelectionResolution:
    officer: Long
    unavailable: Word
    def validate(self, state):
        uint(self.officer, 32)
        uint(self.unavailable, 16)
        return self


@dataclass(frozen=True)
class RosterInput:
    selection: Long
    def validate(self, state):
        uint(self.selection, 32)
        return self


@dataclass(frozen=True)
class CarryOutcome:
    carry: bool
    selection: Long | None
    def validate(self, state):
        if type(self.carry) is not bool:
            raise ValueError('explicit carry result required')
        if self.selection is not None:
            uint(self.selection, 32)
        return self


@dataclass(frozen=True)
class LeaderRosterDetection:
    """11EE's actual selection, last leader WORD, two live views and NZVC.

    The leader's retained high WORD belongs to the caller, not the scan.
    Conditions are those of the final MOVE/compare/ORI path; X is not exposed.
    """
    selection: Long
    leader_word: Word
    leader_cursor: Table
    assignments: Table
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        uint(self.selection, 32)
        uint(self.leader_word, 16)
        checked_table(self.leader_cursor, state)
        checked_table(self.assignments, state)
        if any(type(value) is not bool for value in
               (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('strict final partial arithmetic conditions required')
        return self


@dataclass(frozen=True)
class CampaignOwnerDetection:
    """13DC's preserved high selection carrier and final CMP/SR conditions."""
    selection: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        uint(self.selection, 32)
        if any(type(value) is not bool for value in
               (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('strict final partial arithmetic conditions required')
        return self


@dataclass(frozen=True)
class FormationBitResult:
    mask: Long
    index: Long
    def validate(self, state):
        uint(self.mask, 32)
        uint(self.index, 32)
        return self


@dataclass(frozen=True)
class BitmapRow:
    source: Table | None
    source_width: Word
    source_height: Word
    step: Long
    vertical: Long
    horizontal: Long
    pending_pixels: Long
    remaining_width: Long
    def validate(self, state):
        if self.source is not None:
            checked_table(self.source, state)
        uint(self.source_width, 16)
        uint(self.source_height, 16)
        for value in (self.step, self.vertical, self.horizontal,
                      self.pending_pixels, self.remaining_width):
            uint(value, 32)
        return self


@dataclass(frozen=True)
class BitmapTileResult:
    horizontal: Long
    pending_pixels: Long
    def validate(self, state):
        uint(self.horizontal, 32)
        uint(self.pending_pixels, 32)
        return self


@dataclass(frozen=True)
class CameraMotionInput:
    """16B4 live camera frame, including views retained on the no-strip path.

    Values are full carriers, not inferred from RAM. The strip coordinate is
    supplied separately at each physical call; a coordinate is never a RAM view.
    """
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table | MapCoordinate
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    stack_cursor: Cursor

    def validate(self, state):
        for view in (self.destination, self.source, self.descriptor,
                     self.records, self.palette):
            checked_table(view, state)
        if type(self.roster) is MapCoordinate:
            self.roster.validate(state)
        else:
            checked_table(self.roster, state)
        checked_cursor(self.stack_cursor, state)
        for value in (self.value, self.field, self.tile, self.row, self.offset,
                      self.limit, self.member, self.remaining):
            uint(value, 32)
        return self


@dataclass(frozen=True)
class CameraMotionResult(CameraMotionInput):
    """Complete live output and documented NZVC; no claim about CPU X or timing."""
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        super().validate(state)
        if any(type(value) is not bool for value in
               (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('explicit camera partial arithmetic conditions required')
        return self


@dataclass(frozen=True)
class CameraPointerBoundaryRequest:
    """An incomplete legacy caller: actual target known, live pointer ABI absent.

    This is intentionally NOT accepted by the complete 1344 provider. It carries
    a diagnostic role, never guessed scalar inputs or a fake successful return.
    """
    caller_role: str

    def validate(self, state):
        if self.caller_role not in ('camera-transition', 'mode-control', 'selection-phase'):
            raise ValueError('known incomplete campaign pointer caller required')
        return self


@dataclass(frozen=True)
class CameraTransitionInput(CameraMotionInput):
    """161E actual entry frame; no inferred post-call values or defaults."""


@dataclass(frozen=True)
class CameraTransitionResult(CameraMotionResult):
    """161E full live output after palette advance, with documented NZVC only."""

from .contexts_commands import CommandLabelFrame

@dataclass(frozen=True)
class RosterPanelInput:
    """414/53E6 inherited current label frame, not a frozen style facade."""
    frame: CommandLabelFrame

    def validate(self, state):
        if type(self.frame) is not CommandLabelFrame:
            raise ValueError('complete current roster label frame required')
        self.frame.validate(state)
        return self


@dataclass(frozen=True)
class RosterNameRequest:
    """Actual544E live-in frame; no known54CA return binding is invented."""
    frame: CommandLabelFrame

    def validate(self, state):
        if type(self.frame) is not CommandLabelFrame:
            raise ValueError('actual current roster-name frame required')
        self.frame.validate(state)
        return self


@dataclass(frozen=True)
class RosterPanelResult:
    """Complete current frame after the real AF48 status-edge handshake."""
    frame: CommandLabelFrame

    def validate(self, state):
        if type(self.frame) is not CommandLabelFrame:
            raise ValueError('actual roster frame return required')
        self.frame.validate(state)
        return self

from .contexts_commands import LocationChoiceFrame

@dataclass(frozen=True)
class LocationChoiceInput:
    frame: LocationChoiceFrame

    def validate(self,state):
        if type(self.frame) is not LocationChoiceFrame:
            raise ValueError('complete current location input required')
        self.frame.validate(state)
        return self


@dataclass(frozen=True)
class LocationChoiceResult:
    frame: LocationChoiceFrame

    def validate(self,state):
        if type(self.frame) is not LocationChoiceFrame:
            raise ValueError('complete current location return required')
        self.frame.validate(state)
        return self


@dataclass(frozen=True)
class CampaignPointerFields:
    """1344 actual writes, with explicit unobserved BTST-only C/N/V.

    None denotes no write/observation, never fabricated full register values.
    The contract excludes physical nested AC08 MOVEM/return-slot DATA aliases.
    """
    destination_if_written: Cursor | None
    value_if_written: Word | None
    field_if_written: Word | None
    tile_if_written: Word | None
    carry: bool | None
    zero: bool
    negative: bool | None
    overflow: bool | None

    def validate(self, state):
        if self.destination_if_written is not None:
            checked_cursor(self.destination_if_written, state)
        for value in (self.value_if_written, self.field_if_written, self.tile_if_written):
            if value is not None:
                uint(value, 16)
        if type(self.zero) is not bool:
            raise ValueError('actual 1344 Z observation required')
        if any(value is not None and type(value) is not bool for value in (self.carry, self.negative, self.overflow)):
            raise ValueError('actual or explicitly unobserved 1344 conditions required')
        return self
