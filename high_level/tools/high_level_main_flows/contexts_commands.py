"""Function-local immutable values and same-state view contracts.

These are not complete CPU frames or a register/PC dictionary. Retained input
carriers are explicit; return values expose only this routine's actual effects.
"""
from dataclasses import dataclass
from .domain import SceneState, Long, Word, Table, Cursor, uint, checked_state, checked_table, checked_cursor

@dataclass(frozen=True)
class ComposeCurrentCityFieldsInput:
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
class ComposeCurrentCityFieldsResult:
    destination: Table
    source: Table
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
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class StartCurrentCityPacketInput:
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
class StartCurrentCityPacketResult:
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
class AppendCityStatusRowInput:
    destination: Table
    value: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class AppendCityStatusRowResult:
    destination: Table
    value: Long
    tile: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendCityNameFieldsInput:
    destination: Table
    source: Table
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
class AppendCityNameFieldsResult:
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
class StoreCityStatusValueInput:
    destination: Table
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class StoreCityStatusValueResult:
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
class AppendCityResourceRowInput:
    destination: Table
    value: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class AppendCityResourceRowResult:
    destination: Table
    value: Long
    tile: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendSelectedRosterValuesInput:
    destination: Table
    value: Long
    tile: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class AppendSelectedRosterValuesResult:
    destination: Table
    value: Long
    tile: Long
    remaining: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CollectCityOfficersForMenuInput:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CollectCityOfficersForMenuResult:
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
class CollectCityOfficersForMenuService1:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CollectCityOfficersForMenuService2:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CollectCityOfficersForMenuService3:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CollectCityOfficersForMenuService4:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CollectCityOfficersForMenuService5:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CollectCityOfficersForMenuService6:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CollectCityOfficersForMenuService7:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CollectCityOfficersForMenuService8:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class AppendCurrentRosterMarksInput:
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class AppendCurrentRosterMarksResult:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
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
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class RenderCurrentCityCommandLabelsInput:
    source: Table
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class RenderCurrentCityCommandLabelsResult:
    source: Table
    tile: Long
    row: Long
    offset: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class RenderCurrentCityCommandLabelsService1:
    source: Table
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class ComposeCityRosterRowsInput:
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
class ComposeCityRosterRowsResult:
    destination: Table
    source: Table
    descriptor: Table
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
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
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
class ComposeSelectedForceRowsInput:
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
class ComposeSelectedForceRowsResult:
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
class AppendCityRelationRowInput:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class AppendCityRelationRowResult:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    row: Long
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
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class RenderRosterNameOrPromptInput:
    records: Table
    palette: Table
    field: Long
    tile: Long
    row: Long
    offset: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class RenderRosterNameOrPromptResult:
    records: Table
    palette: Table
    field: Long
    tile: Long
    row: Long
    offset: Long
    member: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class RenderSelectedCityPacketInput:
    records: Table
    field: Long
    row: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.records, state)
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class RenderSelectedCityPacketResult:
    palette: Table
    field: Long
    row: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.palette, state)
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendForceRosterNamesInput:
    records: Table
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
        checked_state(state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class AppendForceRosterNamesResult:
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
class StartSelectionPromptInput:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class StartSelectionPromptResult:
    destination: Table
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class StartSelectionPromptService1:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class StartSelectionPromptService2:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class StartSelectionPromptService3:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class AppendSelectionPromptHeadingInput:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class AppendSelectionPromptHeadingResult:
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
class SetSelectionPromptValueInput:
    destination: Table
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class SetSelectionPromptValueResult:
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
class AppendSelectionPromptRowInput:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class AppendSelectionPromptRowResult:
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
class AppendCurrentCityOwnerInput:
    destination: Table
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class AppendCurrentCityOwnerResult:
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
class StoreSelectionPromptValueInput:
    destination: Table
    field: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class StoreSelectionPromptValueResult:
    destination: Table
    field: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendSelectionPromptValueInput:
    destination: Table
    field: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class AppendSelectionPromptValueResult:
    destination: Table
    field: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendSelectedForceHeadInput:
    value: Long
    field: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class AppendSelectedForceHeadResult:
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
class AppendSelectedForceHeadService1:
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
class ComposeCommandSelectionPromptInput:
    tile: Long
    row: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class ComposeCommandSelectionPromptResult:
    destination: Table
    source: Table
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
        checked_table(self.source, state)
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class ComposeCommandSelectionPromptService1:
    destination: Table
    source: Table
    tile: Long
    row: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class SetCommandSelectionCursorInput:
    destination: Table
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class SetCommandSelectionCursorResult:
    destination: Table
    row: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class StoreCommandSelectionValueInput:
    destination: Table
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class StoreCommandSelectionValueResult:
    destination: Table
    row: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendCommandSelectionHeadingInput:
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class AppendCommandSelectionHeadingResult:
    destination: Table
    tile: Long
    row: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendCommandConfirmationRowInput:
    value: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class AppendCommandConfirmationRowResult:
    destination: Table
    value: Long
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
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class PresentCurrentCommandPromptInput:
    value: Long
    field: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class PresentCurrentCommandPromptResult:
    value: Long
    field: Long
    remaining: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class PresentCurrentCommandPromptService1:
    value: Long
    field: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class PresentCommandWarningInput:
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class PresentCommandWarningResult:
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
class AppendContextualCursorCommandsInput:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class AppendContextualCursorCommandsResult:
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
class AppendContextualCursorCommandsService1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class AppendContextualCursorCommandsService2:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class DrawForceSummaryInput:
    value: Long
    field: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class DrawForceSummaryResult:
    destination: Table
    source: Table
    value: Long
    field: Long
    row: Long
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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class DrawFirstForcePromptInput:
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class DrawFirstForcePromptResult:
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
class DrawSecondForcePromptInput:
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class DrawSecondForcePromptResult:
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
class UpdateSelectedForcePromptInput:
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class UpdateSelectedForcePromptResult:
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
class DrawCurrentScenarioPromptInput:
    value: Long
    field: Long
    row: Long
    offset: Long
    limit: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class DrawCurrentScenarioPromptResult:
    destination: Table
    source: Table
    roster: Table
    port: Table
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
        checked_table(self.source, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
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
class DrawCurrentScenarioPromptService1:
    destination: Table
    source: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class DrawCurrentScenarioPromptService2:
    destination: Table
    source: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class DrawCurrentScenarioPromptService3:
    destination: Table
    source: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class AppendScenarioOwnerGlyphsInput:
    roster: Table
    port: Table
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class AppendScenarioOwnerGlyphsResult:
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
class AppendScenarioOwnerValueInput:
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class AppendScenarioOwnerValueResult:
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
class DrawTitleModePromptInput:
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
class DrawTitleModePromptResult:
    destination: Table
    source: Table
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
        checked_table(self.source, state)
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
class ComposeTitleOptionPanelInput:
    source: Table
    port: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
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
class ComposeTitleOptionPanelResult:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
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
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendTitleOptionGlyphsInput:
    destination: Table
    source: Table
    port: Table
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
        checked_table(self.port, state)
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
class AppendTitleOptionGlyphsResult:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
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
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendTitleOptionDigitInput:
    destination: Table
    value: Long
    tile: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class AppendTitleOptionDigitResult:
    destination: Table
    tile: Long
    offset: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class StoreTitleOptionDigitInput:
    destination: Table
    tile: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class StoreTitleOptionDigitResult:
    destination: Table
    tile: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class SetTitleOptionMarkerInput:
    destination: Table
    value: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class SetTitleOptionMarkerResult:
    destination: Table
    tile: Long
    row: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendTitleOptionDecorationsInput:
    destination: Table
    source: Table
    port: Table
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
        checked_table(self.port, state)
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
class AppendTitleOptionDecorationsResult:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
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
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendTitleOptionDecorationsService1:
    destination: Table
    source: Table
    port: Table
    value: Long
    tile: Long
    member: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class AppendTitleOptionDecorationValueInput:
    destination: Table
    tile: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class AppendTitleOptionDecorationValueResult:
    destination: Table
    tile: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendWorldCursorCoordinatesInput:
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
class AppendWorldCursorCoordinatesResult:
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
class DrawRosterOverviewInput:
    palette: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class DrawRosterOverviewResult:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
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
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendRosterOverviewCursorInput:
    palette: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.palette, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class AppendRosterOverviewCursorResult:
    destination: Table
    source: Table
    descriptor: Table
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
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class DrawRosterOverviewValuesInput:
    palette: Table
    roster: Table
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class DrawRosterOverviewValuesResult:
    value: Long
    field: Long
    tile: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendSelectedCityHeadInput:
    value: Long
    field: Long
    tile: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class AppendSelectedCityHeadResult:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
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
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendSelectedCityHeadService1:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class AppendRosterOverviewDigitInput:
    palette: Table
    roster: Table
    field: Long
    tile: Long
    row: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class AppendRosterOverviewDigitResult:
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
class RetainRosterOverviewColumnInput:
    palette: Table
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.palette, state)
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class RetainRosterOverviewColumnResult:
    row: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class ComposeOfficerDetailPanelInput:
    source: Table
    palette: Table
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.palette, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class ComposeOfficerDetailPanelResult:
    destination: Table
    source: Table
    port: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
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
class AppendOfficerNameValueInput:
    destination: Table
    source: Table
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class AppendOfficerNameValueResult:
    destination: Table
    source: Table
    port: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
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
class AppendOfficerNameValueAlternate1Input:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class AppendOfficerNameValueAlternate1Result:
    destination: Table
    source: Table
    port: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
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
class AppendOfficerNameValueAlternate2Input:
    destination: Table
    source: Table
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class AppendOfficerNameValueAlternate2Result:
    destination: Table
    source: Table
    port: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
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
class AppendOfficerNameValueAlternate3Input:
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class AppendOfficerNameValueAlternate3Result:
    destination: Table
    source: Table
    port: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
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
class AppendOfficerNameValueAlternate4Input:
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class AppendOfficerNameValueAlternate4Result:
    destination: Table
    source: Table
    port: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
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
class AppendOfficerAttributeValueInput:
    palette: Table
    roster: Table
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class AppendOfficerAttributeValueResult:
    destination: Table
    source: Table
    port: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
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
class AppendOfficerAttributeValueService1:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class AppendOfficerAttributeValueService2:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class ScaleOfficerDetailValueInput:
    palette: Table
    roster: Table
    value: Long
    field: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class ScaleOfficerDetailValueResult:
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
class AppendOfficerDetailCommandsInput:
    palette: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class AppendOfficerDetailCommandsResult:
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
class AppendOfficerDetailTitleInput:
    palette: Table
    field: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.palette, state)
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class AppendOfficerDetailTitleResult:
    field: Long
    row: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class DrawOfficerDetailViewInput:
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class DrawOfficerDetailViewResult:
    destination: Table
    source: Table
    descriptor: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
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
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendOfficerDetailRowsInput:
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class AppendOfficerDetailRowsResult:
    destination: Table
    source: Table
    descriptor: Table
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
class OpenRosterSelectionMessageInput:
    records: Table
    value: Long
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class OpenRosterSelectionMessageResult:
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
class SetRosterSelectionNoticeInput:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class SetRosterSelectionNoticeResult:
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
class DrawForceRelationViewInput:
    value: Long
    field: Long
    tile: Long
    row: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class DrawForceRelationViewResult:
    destination: Table
    source: Table
    port: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendForceRelationCommandsInput:
    value: Long
    field: Long
    remaining: Long
    stack_cursor: Cursor

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        return self

@dataclass(frozen=True)
class AppendForceRelationCommandsResult:
    destination: Table
    value: Long
    field: Long
    tile: Long
    remaining: Long
    stack_cursor: Cursor
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
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendForceRelationCommandsService1:
    destination: Table
    value: Long
    field: Long
    tile: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class AppendForceRelationHeadingInput:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class AppendForceRelationHeadingResult:
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
class SetForceRelationMarkersInput:
    destination: Table
    value: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class SetForceRelationMarkersResult:
    destination: Table
    value: Long
    remaining: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendForceRelationValueRowInput:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class AppendForceRelationValueRowResult:
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
class AppendForceRelationFooterInput:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class AppendForceRelationFooterResult:
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
class AppendForceRelationLabelInput:
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
class AppendForceRelationLabelResult:
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
class AppendForceRelationDigitsInput:
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
class AppendForceRelationDigitsResult:
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
class AdjustForceRelationSelectionInput:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class AdjustForceRelationSelectionResult:
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
class ConfirmForceRelationSelectionInput:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.negative, self.overflow)):
            raise ValueError('actual incoming C/N/V bools required')
        return self

@dataclass(frozen=True)
class ConfirmForceRelationSelectionResult:
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
class DrawCommandCostPanelInput:
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
class DrawCommandCostPanelResult:
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
class DrawCommandCostPanelService1:
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
class DrawCommandCostPanelService2:
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
class DrawCommandCostPanelAlternate1Input:
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
class DrawCommandCostPanelAlternate1Result:
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
class DrawCommandCostPanelAlternate1Service1:
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
class DrawCommandCostPanelAlternate1Service2:
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
class DivideAndScaleCommandValueInput:
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
class DivideAndScaleCommandValueResult:
    destination: Table
    source: Table
    descriptor: Table
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
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendSelectedCityCommandInput:
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class AppendSelectedCityCommandResult:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
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
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class StoreSelectedCityCommandValueInput:
    destination: Table
    offset: Long
    limit: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class StoreSelectedCityCommandValueResult:
    destination: Table
    offset: Long
    limit: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendCityCommandHeadingInput:
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
class AppendCityCommandHeadingResult:
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
class AppendCurrentCommandDescriptionInput:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.negative, self.overflow)):
            raise ValueError('actual incoming D8EC C/N/V required')
        return self

@dataclass(frozen=True)
class AppendCurrentCommandDescriptionResult:
    destination: Table
    source: Table
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
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class ChooseCommandDescriptionSourceInput:
    destination: Table
    source: Table
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class ChooseCommandDescriptionSourceResult:
    destination: Table
    source: Table
    row: Long
    carry: bool = False
    zero: bool = False
    negative: bool = False
    overflow: bool = False

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class AppendCommandDescriptionRowsInput:
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
class AppendCommandDescriptionRowsResult:
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
class AppendCommandDescriptionStatusInput:
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
class AppendCommandDescriptionStatusResult:
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
class DrawDiplomacyCommandPanelInput:
    value: Long
    field: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class DrawDiplomacyCommandPanelResult:
    destination: Table
    source: Table
    roster: Table
    port: Table
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
        checked_table(self.source, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class DrawDiplomacyCommandPanelService1:
    destination: Table
    source: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class DrawDiplomacyCommandPanelService2:
    destination: Table
    source: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class AppendDiplomacyCommandChoicesInput:
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
class AppendDiplomacyCommandChoicesResult:
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
class SetDiplomacyCommandMarkerInput:
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
class SetDiplomacyCommandMarkerResult:
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
class DrawDiplomacyParameterPanelInput:
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
class DrawDiplomacyParameterPanelResult:
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
class DrawDiplomacyParameterPanelService1:
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
class DrawDiplomacyParameterPanelService2:
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
class DrawDiplomacyParameterPanelService3:
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
class DrawDiplomacyParameterPanelService4:
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
class DrawDiplomacyParameterPanelService5:
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
class DrawDiplomacyParameterPanelService6:
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
class DrawDiplomacyParameterPanelService7:
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
class DrawDiplomacyParameterPanelService8:
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
class DrawDiplomacyParameterPanelService9:
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
class DrawDiplomacyParameterPanelService10:
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
class DrawDiplomacyParameterPanelService11:
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
class DrawDiplomacyParameterPanelService12:
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
class DrawDiplomacyParameterPanelService13:
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
class DrawDiplomacyParameterPanelService14:
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
class DrawDiplomacyParameterPanelAlternate1Input:
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
class DrawDiplomacyParameterPanelAlternate1Result:
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
class DrawDiplomacyParameterPanelAlternate1Service1:
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
class DrawDiplomacyParameterPanelAlternate1Service2:
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
class DrawDiplomacyParameterPanelAlternate1Service3:
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
class DrawDiplomacyParameterPanelAlternate1Service4:
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
class DrawDiplomacyParameterPanelAlternate1Service5:
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
class DrawDiplomacyParameterPanelAlternate1Service6:
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
class DrawDiplomacyParameterPanelAlternate1Service7:
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
class DrawDiplomacyParameterPanelAlternate1Service8:
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
class DrawDiplomacyParameterPanelAlternate1Service9:
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
class DrawDiplomacyParameterPanelAlternate1Service10:
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
class DrawDiplomacyParameterPanelAlternate1Service11:
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
class DrawDiplomacyParameterPanelAlternate1Service12:
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
class DrawDiplomacyParameterPanelAlternate1Service13:
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
class DrawDiplomacyParameterPanelAlternate1Service14:
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
class DrawDiplomacyParameterPanelAlternate1Service15:
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
class DrawDiplomacyParameterPanelAlternate1Service16:
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
class DrawDiplomacyParameterPanelAlternate1Service17:
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
class DrawDiplomacyParameterPanelAlternate1Service18:
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
class DrawDiplomacyParameterPanelAlternate1Service19:
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
class DrawDiplomacyParameterPanelAlternate1Service20:
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
class DrawDiplomacyParameterPanelAlternate1Service21:
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
class DrawDiplomacyParameterPanelAlternate1Service22:
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
class DrawDiplomacyParameterPanelAlternate1Service23:
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
class DrawDiplomacyParameterPanelAlternate2Input:
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
class DrawDiplomacyParameterPanelAlternate2Result:
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
class DrawDiplomacyParameterPanelAlternate2Service1:
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
class DrawDiplomacyParameterPanelAlternate2Service2:
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
class DrawDiplomacyParameterPanelAlternate2Service3:
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
class CommandLabelFrame:
    """Current label colors, counters and live views; no fabricated live-ins.

    stack_cursor is the real entry stack anchor. Logical glyph reuse does not
    reproduce physical JSR/MOVEM DATA; the business core declares a protected
    ordinary stack domain and stops its known aliases instead of faking RTS.
    """
    background: Long
    foreground: Long
    selector: Long
    glyph_rows: Long
    upload_count: Long
    code_index: Long
    emitted_labels: Long
    glyph_scratch: Long
    glyph_source: Table
    packet_cursor: Table
    label_codes: Table
    code_lookup: Table
    auxiliary_view: Table
    retained_view: Table
    vdp_data_port: Table
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        for value in (self.background, self.foreground, self.selector,
                self.glyph_rows, self.upload_count, self.code_index,
                self.emitted_labels, self.glyph_scratch):
            uint(value, 32, 'complete label carrier')
        for view in (self.glyph_source, self.packet_cursor, self.label_codes,
                self.code_lookup, self.auxiliary_view, self.retained_view,
                self.vdp_data_port):
            checked_table(view, state)
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in
                (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('strict label partial arithmetic outcomes required')
        return self


@dataclass(frozen=True)
class LocationChoiceFrame:
    """Only this location/prompt/sprite family's actual current live operands."""
    motion_value: Long
    prompt_field: Long
    sprite_attributes: Long
    sprite_source: Table
    palette_source: Table
    vdp_port: Table
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        for value in (self.motion_value,self.prompt_field,self.sprite_attributes):
            uint(value,32,'current location carrier')
        for view in (self.sprite_source,self.palette_source,self.vdp_port):
            checked_table(view,state)
        checked_cursor(self.stack_cursor,state)
        if any(type(value) is not bool for value in (self.carry,self.zero,self.negative,self.overflow)):
            raise ValueError('strict current location NZVC required')
        return self


@dataclass(frozen=True)
class SelectedCityCommandFields:
    """Actual D74A WORD writes and live views, not fabricated full carriers.

    None means that this call never wrote that WORD/view. Legacy callers retain
    their real incoming value at that site; the SceneTick field caller does not
    claim to possess or return an unobserved high WORD or unwritten input A1.
    """
    destination: Table
    source_if_written: Table | None
    value_word: Word
    field_word: Word
    tile_if_written: Word | None
    row_if_written: Word | None
    offset_if_written: Word | None
    limit_if_written: Word | None
    member_if_written: Word | None
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        if self.source_if_written is not None:
            checked_table(self.source_if_written, state)
        uint(self.value_word, 16)
        uint(self.field_word, 16)
        for value in (self.tile_if_written, self.row_if_written, self.offset_if_written,
                      self.limit_if_written, self.member_if_written):
            if value is not None:
                uint(value, 16)
        if any(type(value) is not bool for value in (self.carry,self.zero,self.negative,self.overflow)):
            raise ValueError('actual D74A final condition observations required')
        return self


@dataclass(frozen=True)
class StoreSelectedCityCommandFields:
    """Actual D89C destination and two final WORD observations."""
    destination: Table
    offset_word: Word
    limit_word: Word
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.offset_word, 16)
        uint(self.limit_word, 16)
        if any(type(value) is not bool for value in (self.carry,self.zero,self.negative,self.overflow)):
            raise ValueError('actual final D89C ADDQ conditions required')
        return self


@dataclass(frozen=True)
class ConfirmForceRelationSelectionFields:
    """Actual C790 WORD/view writes, with known-Z and retained-condition mask.

    None means the original call did not write that field. For carry/negative/
    overflow it means the BTST-only path retained a flag not present in this
    effect contract. It is not a fake pointer, high WORD, or False condition.
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
        checked_state(state)
        if self.destination_if_written is not None:
            checked_cursor(self.destination_if_written, state)
        for value in (self.value_if_written, self.field_if_written, self.tile_if_written):
            if value is not None:
                uint(value, 16)
        if type(self.zero) is not bool:
            raise ValueError('actual C790 Z observation required')
        if any(value is not None and type(value) is not bool for value in (self.carry, self.negative, self.overflow)):
            raise ValueError('actual or explicitly unobserved C790 conditions required')
        return self


@dataclass(frozen=True)
class CommandDescriptionFields:
    """Actual D8EC/D920/DA2C/DA8E WORD/current-view observations.

    Optional fields are unwritten, not zero. D920 destination is the explicitly
    supplied current A0 (even on its no-adjustment path), not a guessed source.
    C/N/V are None only when disabled D8EC executes BTST alone. This is not a
    physical stack/scratch/MOVEM contract or a full CPU result.
    """
    destination_if_written: Table | None
    source_if_written: Table | None
    value_if_written: Word | None
    field_if_written: Word | None
    tile_if_written: Word | None
    row_if_written: Word | None
    carry: bool | None
    zero: bool
    negative: bool | None
    overflow: bool | None

    def validate(self, state):
        checked_state(state)
        for view in (self.destination_if_written, self.source_if_written):
            if view is not None:
                checked_table(view, state)
        for value in (self.value_if_written, self.field_if_written, self.tile_if_written, self.row_if_written):
            if value is not None:
                uint(value, 16)
        if type(self.zero) is not bool:
            raise ValueError('actual description Z observation required')
        if any(value is not None and type(value) is not bool for value in (self.carry, self.negative, self.overflow)):
            raise ValueError('actual or explicitly unobserved description conditions required')
        return self


@dataclass(frozen=True)
class CommandSelectionHeadingFields:
    """5A42 locally defined D2/D3 WORDs and the actual live A0."""
    destination: Table
    tile: Word
    row: Word
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.tile, 16)
        uint(self.row, 16)
        if any(type(flag) is not bool for flag in
               (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('true 5A78 MOVE-W conditions required')
        return self
