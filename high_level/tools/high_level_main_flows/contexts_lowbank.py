"""Function-local immutable values and same-state view contracts.

These are not complete CPU frames or a register/PC dictionary. Retained input
carriers are explicit; return values expose only this routine's actual effects.
"""
from dataclasses import dataclass
from .domain import SceneState, Long, Table, Cursor, uint, checked_state, checked_table, checked_cursor
from ..high_level_scene_flows.contexts_scene import PacketTransferValues

@dataclass(frozen=True)
class PollWorldMapInputInput:
    value: Long
    field: Long
    tile: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class PollWorldMapInputResult:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    remaining: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self


@dataclass(frozen=True)
class PaletteRefreshFields:
    """Actual A3DA field observations, not an invented complete CPU input.

    source_if_written=None means this call did not write A1. The strict legacy
    wrapper then retains its actual incoming A1; effects-only callers need no A1.
    value_word/field_word are actual D0/D1 low WORD outputs, never full LONGs.
    extend is the actual final X observed at its defining ADDQ/LSL, not an incoming default.
    """
    destination: Table
    source_if_written: Table | None
    value_word: int
    field_word: int
    carry: bool
    zero: bool
    negative: bool
    overflow: bool
    extend: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        if self.source_if_written is not None:
            checked_table(self.source_if_written, state)
        uint(self.value_word, 16)
        uint(self.field_word, 16)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow, self.extend)):
            raise ValueError('strict known final MOVE.W outcomes required')
        return self

@dataclass(frozen=True)
class PollWorldMapInputService1:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class UploadWorldMapPaletteInput:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class UploadWorldMapPaletteResult:
    value: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class DrawSceneHeaderGlyphsInput:
    port: Table
    value: Long
    field: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class DrawSceneHeaderGlyphsResult:
    destination: Table
    source: Table
    value: Long
    field: Long
    row: Long
    offset: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class UploadSelectionLayoutInput:
    offset: Long

    def validate(self, state):
        checked_state(state)
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class UploadSelectionLayoutResult:
    destination: Table
    offset: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class DrawSceneFooterGlyphsInput:
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class DrawSceneFooterGlyphsResult:
    destination: Table
    source: Table
    tile: Long
    row: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class DrawCurrentResourceGlyphsInput:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class DrawCurrentResourceGlyphsResult:
    destination: Table
    value: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class ConfigureControllerOutputsInput:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class ConfigureControllerOutputsResult:
    value: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class PollControllerWithZ80BusInput:
    value: Long
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class PollControllerWithZ80BusResult:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class PollTwoControllerPortsInput:
    value: Long
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class PollTwoControllerPortsResult:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class PollTwoControllerPortsAlternate1Input:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class PollTwoControllerPortsAlternate1Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class InitializeZ80SoundImageInput:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class InitializeZ80SoundImageResult:
    destination: Table
    source: Table
    value: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class ReleaseZ80ResetInput:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class ReleaseZ80ResetResult:
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class QueueSoundWordListInput:
    value: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class QueueSoundWordListResult:
    source: Table
    descriptor: Table
    records: Table
    value: Long
    remaining: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class InitializeSceneGrowthAndTilesInput:
    value: Long
    offset: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class InitializeSceneGrowthAndTilesResult:
    destination: Table
    value: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class InitializeSceneGrowthAndTilesService1:
    destination: Table
    value: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class RefreshScenePalettesInput:
    source: Table
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class RefreshScenePalettesResult:
    destination: Table
    source: Table
    value: Long
    field: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class UploadSelectedModeTileRowsInput:
    destination: Table
    field: Long
    tile: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class UploadSelectedModeTileRowsResult:
    destination: Table
    port: Table
    field: Long
    tile: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.port, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class UploadSelectedTileRowInput:
    destination: Table
    port: Table
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.port, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class UploadSelectedTileRowResult:
    field: Long
    tile: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self
