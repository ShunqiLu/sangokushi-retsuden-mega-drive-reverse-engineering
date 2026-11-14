"""Function-local immutable values and same-state view contracts.

These are not complete CPU frames or a register/PC dictionary. Retained input
carriers are explicit; return values expose only this routine's actual effects.
"""
from dataclasses import dataclass
from .domain import SceneState, Long, Word, Table, Cursor, uint, checked_state, checked_table, checked_cursor

@dataclass(frozen=True)
class MapCoordinate:
    """Signed MOVEA-W coordinate carrier, not a RAM cursor or table."""
    base: Long

    def validate(self, state):
        checked_state(state)
        uint(self.base, 32, "sign-extended coordinate carrier")
        return self

@dataclass(frozen=True)
class RestoreSceneDescriptorInput:
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class RestoreSceneDescriptorResult:
    destination: Table
    source: Table
    descriptor: Table
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
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CopyTenSceneLongsInput:
    destination: Table
    source: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CopyTenSceneLongsResult:
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
class CopyFortySceneLongsInput:
    destination: Table
    source: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CopyFortySceneLongsResult:
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
class Copy128SceneLongsInput:
    destination: Table
    source: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class Copy128SceneLongsResult:
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
class Copy64SceneLongsInput:
    destination: Table
    source: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class Copy64SceneLongsResult:
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
class Copy256SceneLongsInput:
    destination: Table
    source: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class Copy256SceneLongsResult:
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
class CopyTwentySceneLongsInput:
    destination: Table
    source: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CopyTwentySceneLongsResult:
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
class CopyEightSceneLongsInput:
    destination: Table
    source: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CopyEightSceneLongsResult:
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
class CopyScenePaletteLongsInput:
    destination: Table
    source: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CopyScenePaletteLongsResult:
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
class CopyRemainingPaletteLongsInput:
    destination: Table
    source: Table
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class CopyRemainingPaletteLongsResult:
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
class LocateCityAtWorldCursorInput:
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class LocateCityAtWorldCursorResult:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class SelectPreviousCommandOfficerInput:
    value: Long
    field: Long
    tile: Long
    row: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class SelectPreviousCommandOfficerResult:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
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
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class SelectNextCommandOfficerInput:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    remaining: Long
    stack_cursor: Cursor | None = None

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        if self.stack_cursor is not None:
            checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class SelectNextCommandOfficerResult:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    remaining: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class SelectNextCommandOfficerService1:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class SelectNextCommandOfficerService2:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class SelectNextCommandOfficerService3:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class SelectNextCommandOfficerService4:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class SelectNextCommandOfficerService5:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class SelectNextCommandOfficerService6:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class SelectNextCommandOfficerService7:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class SelectNextCommandOfficerService8:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class AdjustSelectedRosterMemberInput:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class AdjustSelectedRosterMemberResult:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    value: Long
    field: Long
    tile: Long
    row: Long
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
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AdjustSelectedRosterMemberService1:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class AdjustSelectedRosterMemberService2:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class ScanRosterSelectionStatusInput:
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class ScanRosterSelectionStatusResult:
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class ScanCandidateRosterStatusInput:
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class ScanCandidateRosterStatusResult:
    destination: Table
    value: Long
    field: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class ClearOfficerGrowthFieldsInput:
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
class ClearOfficerGrowthFieldsResult:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
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
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class RefreshWorldMapScrollInput:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class RefreshWorldMapScrollResult:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class RefreshWorldMapScrollService1:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class RefreshWorldMapScrollService2:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class LocateMapObjectRecordInput:
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LocateMapObjectRecordResult:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class UpdateWorldCursorFromInputsInput:
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
class UpdateWorldCursorFromInputsResult:
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
class QueueMapStripTransferInput:
    source: Table
    value: Long
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class QueueMapStripTransferResult:
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
class RefreshMapTilesAroundCursorInput:
    """A01C retained live-ins; no invented register or stack defaults."""
    roster: Table | MapCoordinate
    value: Long
    field: Long
    offset: Long
    limit: Long
    member: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        if type(self.roster) is MapCoordinate:
            self.roster.validate(state)
        else:
            checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class RefreshMapTilesAroundCursorResult:
    roster: Table | MapCoordinate
    value: Long
    field: Long
    offset: Long
    limit: Long
    member: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        if type(self.roster) is MapCoordinate:
            self.roster.validate(state)
        else:
            checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class RefreshMapTilesAroundCursorService1:
    """One actual strip call, carrying its current caller locals."""
    roster: MapCoordinate
    value: Long
    field: Long
    offset: Long
    limit: Long
    member: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        if type(self.roster) is not MapCoordinate:
            raise ValueError("actual signed map coordinate required")
        self.roster.validate(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class RefreshMapTilesAroundCursorService2:
    """One actual strip call, carrying its current caller locals."""
    roster: MapCoordinate
    value: Long
    field: Long
    offset: Long
    limit: Long
    member: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        if type(self.roster) is not MapCoordinate:
            raise ValueError("actual signed map coordinate required")
        self.roster.validate(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class RefreshMapTilesAroundCursorService3:
    """One actual strip call, carrying its current caller locals."""
    roster: MapCoordinate
    value: Long
    field: Long
    offset: Long
    limit: Long
    member: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        if type(self.roster) is not MapCoordinate:
            raise ValueError("actual signed map coordinate required")
        self.roster.validate(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class RefreshMapTilesAroundCursorService4:
    """One actual strip call, carrying its current caller locals."""
    roster: MapCoordinate
    value: Long
    field: Long
    offset: Long
    limit: Long
    member: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        if type(self.roster) is not MapCoordinate:
            raise ValueError("actual signed map coordinate required")
        self.roster.validate(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class RenderMapColumnInput:
    roster: MapCoordinate
    value: Long
    field: Long
    offset: Long
    limit: Long
    member: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        if type(self.roster) is not MapCoordinate:
            raise ValueError("strict MapCoordinate required, not a RAM view")
        self.roster.validate(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class RenderMapColumnResult:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
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
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class RenderMapRowInput:
    roster: MapCoordinate
    value: Long
    field: Long
    offset: Long
    limit: Long
    member: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        if type(self.roster) is not MapCoordinate:
            raise ValueError("strict MapCoordinate required, not a RAM view")
        self.roster.validate(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class RenderMapRowResult:
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
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        if type(self.roster) is MapCoordinate:
            self.roster.validate(state)
        else:
            checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class RefreshWorldCursorAttributesInput:
    destination: Table
    value: Long
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class RefreshWorldCursorAttributesResult:
    destination: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class RefreshWorldCursorAttributesAlternate1Input:
    destination: Table
    value: Long
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class RefreshWorldCursorAttributesAlternate1Result:
    destination: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class InitializeWorldMapViewInput:
    roster: Table
    value: Long
    field: Long
    offset: Long
    limit: Long
    member: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class InitializeWorldMapViewResult:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
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
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class InitializeWorldMapViewService1:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class RenderInitialMapRowsInput:
    roster: Table
    value: Long
    field: Long
    offset: Long
    limit: Long
    member: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class RenderInitialMapRowsResult:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
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
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class ReadWorldMapTileInput:
    destination: Table
    roster: Table | MapCoordinate
    value: Long
    field: Long
    offset: Long
    limit: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        if type(self.roster) is MapCoordinate:
            self.roster.validate(state)
        else:
            checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class ReadWorldMapTileResult:
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
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        if type(self.roster) is MapCoordinate:
            self.roster.validate(state)
        else:
            checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class ReadMapCellWordInput:
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class ReadMapCellWordResult:
    value: Long
    field: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class ReadInitialMapColumnInput:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    limit: Long
    member: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class ReadInitialMapColumnResult:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    member: Long
    remaining: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class ReadWrappedMapColumnInput:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class ReadWrappedMapColumnResult:
    destination: Table
    source: Table
    descriptor: Table
    palette: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    member: Long
    remaining: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.palette, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AdvanceMapColumnSourceInput:
    destination: Table
    source: Table
    value: Long
    tile: Long
    row: Long
    limit: Long
    member: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class AdvanceMapColumnSourceResult:
    destination: Table
    palette: Table
    value: Long
    tile: Long
    member: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.palette, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class ResolveMapColumnPacketInput:
    palette: Table
    value: Long
    row: Long
    limit: Long
    member: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        checked_table(self.palette, state)
        uint(self.value, 32, "value carrier")
        uint(self.row, 32, "row carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class ResolveMapColumnPacketResult:
    palette: Table
    value: Long
    row: Long
    member: Long
    remaining: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.palette, state)
        uint(self.value, 32, "value carrier")
        uint(self.row, 32, "row carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AdvanceMapColumnSkipInput:
    source: Table
    palette: Table
    member: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.palette, state)
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class AdvanceMapColumnSkipResult:
    palette: Table
    member: Long
    remaining: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.palette, state)
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self


from .domain import Word


@dataclass(frozen=True)
class WorldCursorRefreshFields:
    """A158 actual WORD writes and true final CMP observations.

    A failed ownership match does not write A0/D1/D2: their fields are None,
    not zero. The reuse sprite transaction does not claim physical nested
    MOVEM/return-slot alias closure or fabricated register high halves.
    """
    source_if_written: Cursor | None
    x: Word
    y_if_written: Word | None
    attributes_if_written: Word | None
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if self.source_if_written is not None:
            checked_cursor(self.source_if_written, state)
        uint(self.x, 16, 'actual current cursor WORD')
        for value in (self.y_if_written, self.attributes_if_written):
            if value is not None:
                uint(value, 16, 'actual written cursor WORD')
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('actual final cursor comparison conditions required')
        if self.source_if_written is None:
            if self.y_if_written is not None or self.attributes_if_written is not None:
                raise ValueError('unmatched cursor cannot fabricate written fields')
        elif self.y_if_written is None or self.attributes_if_written is None:
            raise ValueError('matched sprite requires all actual written fields')
        return self


@dataclass(frozen=True)
class CommandOfficerSelectionFields:
    """6198 actual WORD writes and current views; no fabricated CPU frame.

    None means unmodified/unobserved, not zero. A successful C3CE full call
    supplies its actual complete return as the basis for later partial writes.
    source_if_written is the real positive-message A1 observation; the old
    six-field result does not claim that extra CPU return. Physical stack DATA
    for state-only 5A42/676F2 paths is outside this effects contract.
    """
    destination_if_written: Table | None
    source_if_written: Table | None
    value_if_written: Word
    field_if_written: Word | None
    tile_if_written: Word | None
    row_if_written: Word | None
    remaining_if_written: Word | None
    retained_after_call: SelectNextCommandOfficerResult | None
    carry: bool
    zero: bool
    negative: bool
    overflow: bool
    full_value_basis: Long | None = None

    def validate(self, state):
        checked_state(state)
        for view in (self.destination_if_written, self.source_if_written):
            if view is not None:
                checked_table(view, state)
        uint(self.value_if_written, 16)
        if self.full_value_basis is not None:
            uint(self.full_value_basis, 32)
        for value in (self.field_if_written, self.tile_if_written,
                      self.row_if_written, self.remaining_if_written):
            if value is not None:
                uint(value, 16)
        if self.retained_after_call is not None:
            if type(self.retained_after_call) is not SelectNextCommandOfficerResult:
                raise ValueError('actual current force-command return required')
            self.retained_after_call.validate(state)
        if any(type(flag) is not bool for flag in
               (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('actual last-operation CNZV required')
        return self
