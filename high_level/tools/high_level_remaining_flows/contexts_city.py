"""Function-local immutable values and same-state view contracts.

These are not complete CPU frames or a register/PC dictionary. Retained input
carriers are explicit; return values expose only this routine's actual effects.
"""
from dataclasses import dataclass
from .domain import SceneState, Long, Table, Cursor, uint, checked_state, checked_table, checked_cursor

@dataclass(frozen=True)
class CityCoordinateLiveState1Input:
    destination: Table
    roster: Table
    value: Long
    field: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self


# Actual settlement control outcome, not a synthetic returned frame.
from .domain import Boundary
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame


class SettlementNonlocalReturn(Boundary):
    """Actual1BB80 RTS after two return LONGs became D0/A0, not a fake success.

    The frame already points beyond the one real RTS LONG. A matching original
    ancestor continuation consumes this control outcome without rereading it.
    """
    def __init__(self, continuation: Long, frame: FirstDeploymentFrame):
        uint(continuation, 32)
        if type(frame) is not FirstDeploymentFrame:
            raise ValueError('actual complete settlement exit frame required')
        self.continuation = continuation
        self.context = frame
        super().__init__('original settlement exited two call levels to ' + str(continuation))


@dataclass(frozen=True)
class CityCoordinateLiveState1Result:
    destination: Table
    roster: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState1Service1:
    destination: Table
    roster: Table
    value: Long
    field: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState1Service2:
    destination: Table
    roster: Table
    value: Long
    field: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState1Service3:
    destination: Table
    roster: Table
    value: Long
    field: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState1Service4:
    destination: Table
    roster: Table
    value: Long
    field: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState1Service5:
    destination: Table
    roster: Table
    value: Long
    field: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState2Input:
    destination: Table
    value: Long
    field: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState2Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState2Service1:
    destination: Table
    value: Long
    field: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState2Service2:
    destination: Table
    value: Long
    field: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState2Service3:
    destination: Table
    value: Long
    field: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState2Service4:
    destination: Table
    value: Long
    field: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields1Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields1Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields2Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields2Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields3Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields3Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields4Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields4Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState3Input:
    roster: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState3Result:
    roster: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState3Service1:
    roster: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState3Service2:
    roster: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState3Service3:
    roster: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState3Service4:
    roster: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState3Service5:
    roster: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState3Service6:
    roster: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState4Input:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState4Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState4Service1:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState4Service2:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState4Service3:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState4Service4:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState4Service5:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState5Input:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState5Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState5Service1:
    destination: Table
    source: Table
    descriptor: Table
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
class CityCoordinateLiveState5Service2:
    destination: Table
    source: Table
    descriptor: Table
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
class CityCoordinateLiveState5Service3:
    destination: Table
    source: Table
    descriptor: Table
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
class CityCoordinateLiveState5Service4:
    destination: Table
    source: Table
    descriptor: Table
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
class CityCoordinateLiveState5Service5:
    destination: Table
    source: Table
    descriptor: Table
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
class CityUpdateRecordFlags1Input:
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
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
class CityUpdateRecordFlags1Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags2Input:
    destination: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    attribute_pointer: Table
    owner_pointer: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.attribute_pointer, state)
        checked_table(self.owner_pointer, state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags2Result:
    destination: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    attribute_pointer: Table
    owner_pointer: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.attribute_pointer, state)
        checked_table(self.owner_pointer, state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags2Service1:
    destination: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags2Service2:
    destination: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags2Service3:
    destination: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags2Service4:
    destination: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags2Service5:
    destination: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags2Service6:
    destination: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    attribute_pointer: Table
    owner_pointer: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.attribute_pointer, state)
        checked_table(self.owner_pointer, state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags2Service7:
    destination: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags2Service8:
    destination: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags2Service9:
    destination: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags2Service10:
    destination: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags2Service11:
    destination: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags2Service12:
    destination: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState6Input:
    roster: Table
    field: Long
    tile: Long
    row: Long
    offset: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState6Result:
    roster: Table
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState6Service1:
    roster: Table
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState6Service2:
    roster: Table
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState6Service3:
    roster: Table
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState6Service4:
    roster: Table
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Input:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Result:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service1:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service2:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service3:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service4:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service5:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service6:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service7:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service8:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service9:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service10:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service11:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service12:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service13:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service14:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service15:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service16:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service17:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service18:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service19:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service20:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service21:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service22:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service23:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service24:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service25:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service26:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service27:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service28:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service29:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service30:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service31:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service32:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service33:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service34:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service35:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service36:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service37:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service38:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service39:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service40:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service41:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service42:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service43:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service44:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service45:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service46:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service47:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service48:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service49:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service50:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service51:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords1Service52:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords2Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords2Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityProcessCountedRecords3Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords3Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState7Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState7Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState7Service1:
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
class CityCoordinateLiveState7Service2:
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
class CitySelectLiveState1Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState1Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState8Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState8Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState8Alternate1Input:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState8Alternate1Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState9Input:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState9Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState10Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState10Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState10Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState10Service2:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState10Service3:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState10Service4:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState10Service5:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags3Input:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags3Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityProcessCountedRecords4Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords4Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState11Input:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState11Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState11Service1:
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
class CityCoordinateLiveState12Input:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState12Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState12Service1:
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
class CityCoordinateLiveState12Service2:
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
class CityCoordinateLiveState12Service3:
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
class CityCoordinateLiveState12Service4:
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
class CitySelectLiveState2Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState2Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState13Input:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState13Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState13Service1:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CitySelectLiveState3Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState3Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords5Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords5Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState14Input:
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
class CityCoordinateLiveState14Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CitySelectLiveState4Input:
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
class CitySelectLiveState4Result:
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
class CityCoordinateLiveState15Input:
    source: Table
    descriptor: Table
    value: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState15Result:
    descriptor: Table
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.descriptor, state)
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState15Service1:
    source: Table
    descriptor: Table
    value: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState16Input:
    source: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState16Result:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState16Service1:
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
class CityProcessCountedRecords6Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords6Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityUpdateRecordFlags4Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    attribute_pointer: Table
    owner_pointer: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.attribute_pointer, state)
        checked_table(self.owner_pointer, state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags4Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    attribute_pointer: Table
    owner_pointer: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.attribute_pointer, state)
        checked_table(self.owner_pointer, state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags4Service1:
    destination: Table
    value: Long
    field: Long
    tile: Long

    attribute_pointer: Table
    owner_pointer: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.attribute_pointer, state)
        checked_table(self.owner_pointer, state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags4Service2:
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
class CityUpdateRecordFlags4Service3:
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
class CityUpdateRecordFlags4Service4:
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
class CityCoordinateLiveState17Input:
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState17Result:
    destination: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState17Service1:
    destination: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState18Input:
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState18Result:
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState18Service1:
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState18Service2:
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState18Service3:
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState19Input:
    value: Long
    field: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState19Result:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState19Service1:
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
class CitySelectLiveState5Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState5Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState20Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState20Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState20Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState21Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState21Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState21Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState22Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState22Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState22Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields5Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields5Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState23Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState23Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState23Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState24Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState24Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState24Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CitySelectLiveState6Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CitySelectLiveState6Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityProcessDeviceControl1Input:
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
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessDeviceControl1Result:
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
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessDeviceControl1Service1:
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
        return self

@dataclass(frozen=True)
class CityProcessDeviceControl1Service2:
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
        return self

@dataclass(frozen=True)
class CityProcessDeviceControl1Service3:
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
        return self

@dataclass(frozen=True)
class CityProcessDeviceControl1Service4:
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
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState25Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState25Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState25Service1:
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
class CityCoordinateLiveState25Service2:
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
class CityCoordinateLiveState25Service3:
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
class CityCoordinateLiveState25Service4:
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
class CityUpdateRecordFlags5Input:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
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
class CityUpdateRecordFlags5Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
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
class CityUpdateRecordFlags5Service1:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags5Service2:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags5Service3:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags5Service4:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags5Service5:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags5Service6:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags5Service7:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags5Service8:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState26Input:
    records: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.records, state)
        checked_table(self.roster, state)
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
class CityCoordinateLiveState26Result:
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
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState26Service1:
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
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState26Service2:
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
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState26Service3:
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
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState26Service4:
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
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords7Input:
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords7Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState27Input:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState27Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState27Service1:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState27Service2:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState28Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState28Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState28Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState29Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState29Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState29Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState30Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState30Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState30Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState30Service2:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState31Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState31Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState32Input:
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState32Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState33Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState33Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState33Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState34Input:
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState34Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState35Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState35Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState35Service1:
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
class CityCoordinateLiveState35Service2:
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
class CityCoordinateLiveState35Service3:
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
class CityCoordinateLiveState35Service4:
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
class CityProcessCountedRecords8Input:
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityProcessCountedRecords8Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityProcessCountedRecords9Input:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords9Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityUpdateRecordFlags6Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityUpdateRecordFlags6Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityUpdateRecordFlags6Service1:
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
class CityCoordinateLiveState36Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState36Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState36Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState36Service2:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityProcessDeviceControl2Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessDeviceControl2Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState37Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState37Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState37Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState38Input:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState38Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState7Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState7Result:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState39Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState39Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState39Alternate1Input:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState39Alternate1Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CitySelectLiveState8Input:
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState8Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState40Input:
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState40Result:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState40Service1:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState41Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState41Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState41Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState42Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState42Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState42Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState42Service2:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState43Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState43Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState44Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState44Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState44Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState45Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState45Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState46Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState46Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CitySelectLiveState9Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState9Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState47Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState47Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState48Input:
    port: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState48Result:
    destination: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState49Input:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState49Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityUpdateLiveFields6Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields6Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState1Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState1Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState50Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState50Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState50Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState51Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState51Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState51Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState51Service2:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState52Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState52Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState52Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState53Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState53Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState54Input:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState54Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState54Service1:
    destination: Table
    source: Table
    descriptor: Table
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
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class CitySelectLiveState10Input:
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
class CitySelectLiveState10Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState55Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState55Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState55Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState55Service2:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields7Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields7Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields8Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields8Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState56Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState56Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState57Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState57Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CitySelectLiveState11Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState11Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState2Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState2Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState12Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState12Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState58Input:
    destination: Table
    source: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState58Result:
    destination: Table
    source: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState58Service1:
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
class CitySelectLiveState13Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState13Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState59Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState59Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState59Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState60Input:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState60Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState60Service1:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState3Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState3Result:
    destination: Table
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState14Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState14Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState61Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState61Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState61Service1:
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
class CityCoordinateLiveState62Input:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState62Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState62Service1:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CitySelectLiveState15Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState15Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState63Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState63Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState63Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState64Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState64Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState64Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState65Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState65Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState65Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags7Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags7Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags7Service1:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState66Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState66Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState66Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState67Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState67Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState67Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState68Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState68Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState68Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState69Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState69Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState69Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState70Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState70Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState70Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState70Service2:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState71Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState71Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState71Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CitySelectLiveState16Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState16Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields9Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields9Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords10Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityProcessCountedRecords10Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityProcessCountedRecords11Input:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords11Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords11Service1:
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
class CityProcessCountedRecords11Service2:
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
class CityProcessCountedRecords11Service3:
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
class CityProcessCountedRecords11Service4:
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
class CityCoordinateLiveState72Input:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState72Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState73Input:
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool
    row: Long | None = None
    offset: Long | None = None
    limit: Long | None = None

    def validate(self, state):
        checked_state(state)
        uint(self.field, 32, 'field carrier')
        uint(self.tile, 32, 'tile carrier')
        if any((type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow))):
            raise ValueError('strict partial arithmetic outcomes required')
        for retained in (self.row, self.offset, self.limit):
            if retained is not None:
                uint(retained, 32, 'retained decimal high carrier')
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState73Result:
    destination: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool
    row: Long | None = None
    offset: Long | None = None
    limit: Long | None = None

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.port, state)
        uint(self.value, 32, 'value carrier')
        uint(self.field, 32, 'field carrier')
        uint(self.tile, 32, 'tile carrier')
        if any((type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow))):
            raise ValueError('strict partial arithmetic outcomes required')
        for retained in (self.row, self.offset, self.limit):
            if retained is not None:
                uint(retained, 32, 'retained decimal high carrier')
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState74Input:
    destination: Table
    descriptor: Table
    records: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.roster, state)
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
class CityCoordinateLiveState74Result:
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
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState75Input:
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
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState75Result:
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
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient1Input:
    row: Long
    offset: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient1Result:
    descriptor: Table
    records: Table
    limit: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState17Input:
    limit: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState17Result:
    records: Table
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.records, state)
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState18Input:
    palette: Table
    roster: Table
    limit: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState18Result:
    roster: Table
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords12Input:
    destination: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords12Result:
    destination: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState76Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState76Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState76Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient2Input:
    descriptor: Table
    value: Long
    field: Long
    row: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient2Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCalculateLiveQuotient2Service1:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    member: Long
    remaining: Long

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
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient2Service2:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    member: Long
    remaining: Long

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
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient2Service3:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    member: Long
    remaining: Long

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
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient2Service4:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    member: Long
    remaining: Long

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
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState4Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState4Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient3Input:
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient3Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient3Service1:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient3Service2:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields10Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields10Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient4Input:
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient4Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient4Service1:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient5Input:
    value: Long
    field: Long
    tile: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient5Result:
    source: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient5Service1:
    source: Table
    value: Long
    field: Long
    tile: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient5Service2:
    source: Table
    value: Long
    field: Long
    tile: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient5Service3:
    source: Table
    value: Long
    field: Long
    tile: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields11Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields11Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient6Input:
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient6Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
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
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient6Service1:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityScaleLiveRecordValue1Input:
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityScaleLiveRecordValue1Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
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
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityScaleLiveRecordValue2Input:
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityScaleLiveRecordValue2Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState77Input:
    source: Table
    value: Long
    field: Long
    tile: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState77Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState78Input:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState78Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState78Service1:
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
class CityResolveReadonlyState5Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState5Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState79Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState79Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState79Service1:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient7Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient7Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCalculateLiveQuotient8Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient8Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCalculateLiveQuotient9Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient9Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityScaleLiveRecordValue3Input:
    value: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityScaleLiveRecordValue3Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState80Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState80Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CitySelectLiveState19Input:
    destination: Table
    source: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CitySelectLiveState19Result:
    source: Table
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState81Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState81Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState82Input:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState82Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState83Input:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState83Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState84Input:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState84Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityProcessCountedRecords13Input:
    value: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords13Result:
    destination: Table
    source: Table
    value: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords14Input:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords14Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityProcessCountedRecords15Input:
    destination: Table
    source: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityProcessCountedRecords15Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityProcessCountedRecords15Service1:
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
class CityProcessCountedRecords15Service2:
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
class CityProcessCountedRecords15Service3:
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
class CityProcessCountedRecords15Service4:
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
class CityProcessCountedRecords16Input:
    descriptor: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords16Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords16Service1:
    destination: Table
    source: Table
    descriptor: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords16Service2:
    destination: Table
    source: Table
    descriptor: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords16Service3:
    destination: Table
    source: Table
    descriptor: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords16Service4:
    destination: Table
    source: Table
    descriptor: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords16Service5:
    destination: Table
    source: Table
    descriptor: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords16Alternate1Input:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords16Alternate1Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords16Alternate1Service1:
    destination: Table
    source: Table
    descriptor: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords16Alternate1Service2:
    destination: Table
    source: Table
    descriptor: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords16Alternate1Service3:
    destination: Table
    source: Table
    descriptor: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords16Alternate1Service4:
    destination: Table
    source: Table
    descriptor: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords16Alternate1Service5:
    destination: Table
    source: Table
    descriptor: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState85Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState85Result:
    destination: Table
    source: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags8Input:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags8Result:
    source: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState86Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState86Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState86Service1:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState86Service2:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState86Service3:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState86Service4:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState86Service5:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState86Service6:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords17Input:
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
class CityProcessCountedRecords17Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
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
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords17Service1:
    destination: Table
    source: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords17Service2:
    destination: Table
    source: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords17Service3:
    destination: Table
    source: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords17Service4:
    destination: Table
    source: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords17Alternate1Input:
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
class CityProcessCountedRecords17Alternate1Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
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
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords17Alternate1Service1:
    destination: Table
    source: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords17Alternate1Service2:
    destination: Table
    source: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords17Alternate1Service3:
    destination: Table
    source: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords17Alternate1Service4:
    destination: Table
    source: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords18Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityProcessCountedRecords18Result:
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
class CityCoordinateLiveState87Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState87Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState87Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState6Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState6Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields12Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields12Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState88Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState88Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState88Service1:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CitySelectLiveState20Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState20Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState89Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState89Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState89Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState90Input:
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState90Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState91Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState91Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CitySelectLiveState21Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState21Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState92Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState92Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState93Input:
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState93Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState93Service1:
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
class CityUpdateRecordFlags9Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityUpdateRecordFlags9Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState94Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState94Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState22Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState22Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState95Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState95Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState95Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState7Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState7Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState96Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState96Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState96Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState97Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState97Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState98Input:
    destination: Table
    source: Table
    palette: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState98Result:
    destination: Table
    source: Table
    palette: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
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
class CityCoordinateLiveState99Input:
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState99Result:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
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
class CityCoordinateLiveState99Service1:
    destination: Table
    source: Table
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
class CityCoordinateLiveState99Service2:
    destination: Table
    source: Table
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
class CityCoordinateLiveState99Alternate1Input:
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState99Alternate1Result:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
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
class CityResolveReadonlyState8Input:
    value: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState8Result:
    destination: Table
    value: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState9Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState9Result:
    destination: Table
    palette: Table
    port: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.palette, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState23Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState23Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient10Input:
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
class CityCalculateLiveQuotient10Result:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
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
class CityCalculateLiveQuotient10Service1:
    destination: Table
    source: Table
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
class CityCalculateLiveQuotient10Alternate1Input:
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
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
class CityCalculateLiveQuotient10Alternate1Result:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
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
class CityCalculateLiveQuotient10Alternate1Service1:
    destination: Table
    source: Table
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
class CityUpdateRecordFlags10Input:
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags10Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
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
class CityCoordinateLiveState100Input:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState100Result:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
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
class CityUpdateLiveFields13Input:
    destination: Table
    source: Table
    value: Long
    field: Long
    member: Long
    remaining: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields13Result:
    destination: Table
    source: Table
    field: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.field, 32, "field carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields14Input:
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields14Result:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState101Input:
    source: Table
    descriptor: Table
    records: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState101Result:
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
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
class CityCoordinateLiveState102Input:
    source: Table
    port: Table
    value: Long
    offset: Long
    limit: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState102Result:
    roster: Table
    offset: Long
    limit: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState24Input:
    source: Table
    value: Long
    offset: Long
    limit: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState24Result:
    roster: Table
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.limit, 32, "limit carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState25Input:
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
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState25Result:
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
class CityScaleLiveRecordValue4Input:
    field: Long
    tile: Long
    offset: Long
    limit: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        uint(self.field, 32, 'field carrier')
        uint(self.tile, 32, 'tile carrier')
        uint(self.offset, 32, 'offset carrier')
        uint(self.limit, 32, 'limit carrier')
        checked_cursor(self.stack_cursor, state)
        if any((type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow))):
            raise ValueError('strict partial arithmetic outcomes required')
        uint(self.member, 32, 'true movement carrier')
        uint(self.remaining, 32, 'true movement carrier')
        return self

@dataclass(frozen=True)
class CityScaleLiveRecordValue4Result:
    roster: Table
    offset: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.offset, 32, 'offset carrier')
        uint(self.limit, 32, 'limit carrier')
        if any((type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow))):
            raise ValueError('strict partial arithmetic outcomes required')
        uint(self.member, 32, 'true movement carrier')
        uint(self.remaining, 32, 'true movement carrier')
        return self

@dataclass(frozen=True)
class CityScaleLiveRecordValue4Service1:
    roster: Table
    field: Long
    tile: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.roster, state)
        uint(self.field, 32, 'field carrier')
        uint(self.tile, 32, 'tile carrier')
        uint(self.offset, 32, 'offset carrier')
        uint(self.limit, 32, 'limit carrier')
        uint(self.member, 32, 'true movement carrier')
        uint(self.remaining, 32, 'true movement carrier')
        if any((type(flag) is not bool for flag in (self.carry, self.zero, self.negative, self.overflow))):
            raise ValueError('true terrain dispatch conditions required')
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields15Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields15Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields16Input:
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields16Result:
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields17Input:
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields17Result:
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields18Input:
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields18Result:
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields19Input:
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields19Result:
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields20Input:
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields20Result:
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords19Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords19Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState103Input:
    source: Table
    descriptor: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
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
class CityCoordinateLiveState103Result:
    destination: Table
    source: Table
    descriptor: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
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
class CityCoordinateLiveState104Input:
    records: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState104Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState105Input:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState105Result:
    destination: Table
    source: Table
    records: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
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
class CitySelectLiveState26Input:
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
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
class CitySelectLiveState26Result:
    source: Table
    records: Table
    value: Long
    field: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState106Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState106Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState106Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState107Input:
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
class CityCoordinateLiveState107Result:
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
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState107Service1:
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
        return self

@dataclass(frozen=True)
class CitySelectLiveState27Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState27Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState108Input:
    value: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState108Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState108Service1:
    value: Long
    member: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState108Service2:
    value: Long
    member: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState108Service3:
    value: Long
    member: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState108Service4:
    value: Long
    member: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState108Service5:
    value: Long
    member: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState109Input:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState109Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags11Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags11Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState110Input:
    value: Long
    member: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState110Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState110Service1:
    value: Long
    member: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.member, 32, "member carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState111Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState111Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState111Service1:
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
class CitySelectLiveState28Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState28Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState112Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState112Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState112Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState113Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState113Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState113Service1:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState114Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState114Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState114Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState115Input:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState115Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityResolveReadonlyState10Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState10Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields21Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields21Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState116Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState116Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState116Service1:
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
class CityCoordinateLiveState116Service2:
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
class CityCoordinateLiveState117Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState117Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState117Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState118Input:
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState118Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState118Service1:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

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
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields22Input:
    source: Table
    value: Long
    field: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields22Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityUpdateRecordFlags12Input:
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags12Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityUpdateRecordFlags12Service1:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

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
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState119Input:
    destination: Table
    value: Long
    field: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState119Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState120Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState120Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState120Service1:
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
class CityCoordinateLiveState120Service2:
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
class CityCoordinateLiveState120Service3:
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
class CityCoordinateLiveState121Input:
    destination: Table
    source: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState121Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityProcessCountedRecords20Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords20Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityUpdateLiveFields23Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields23Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState122Input:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState122Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState122Service1:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

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
        return self

@dataclass(frozen=True)
class CitySelectLiveState29Input:
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
class CitySelectLiveState29Result:
    destination: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
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
class CitySelectLiveState30Input:
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CitySelectLiveState30Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState123Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState123Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState123Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields24Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields24Result:
    source: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState124Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState124Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState125Input:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState125Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CitySelectLiveState31Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState31Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState126Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState126Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState127Input:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState127Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CitySelectLiveState32Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState32Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState128Input:
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
class CityCoordinateLiveState128Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState128Service1:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

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
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields25Input:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields25Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityProcessCountedRecords21Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords21Result:
    destination: Table
    source: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState129Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState129Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState129Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields26Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateLiveFields26Result:
    source: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState130Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState130Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState131Input:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState131Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState128Alternate1Input:
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
class CityCoordinateLiveState128Alternate1Result:
    destination: Table
    source: Table
    descriptor: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CitySelectLiveState33Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState33Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState132Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState132Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState132Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags13Input:
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityUpdateRecordFlags13Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
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
class CityUpdateRecordFlags13Service1:
    # These two incoming views are overwritten by662E4's entry LEAs before
    # any read. None means genuinely unobserved, not a fabricated address.
    destination: Table | None
    source: Table | None
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
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
        if self.destination is not None:
            checked_table(self.destination, state)
        if self.source is not None:
            checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
        checked_table(self.port, state)
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
class CityUpdateRecordFlags13Service2:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
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
        checked_table(self.port, state)
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
class CityUpdateRecordFlags13Service3:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    port: Table
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
        checked_table(self.port, state)
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
class CitySelectLiveState34Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState34Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState35Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState35Result:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState36Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState36Result:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState37Input:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState37Result:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState133Input:
    records: Table
    tile: Long
    row: Long
    offset: Long
    limit: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.records, state)
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState133Result:
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
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState133Service1:
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
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState133Service2:
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
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState134Input:
    records: Table
    tile: Long
    row: Long
    offset: Long
    limit: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.records, state)
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState134Result:
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
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityScaleLiveRecordValue5Input:
    descriptor: Table
    records: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityScaleLiveRecordValue5Result:
    records: Table
    value: Long
    field: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState135Input:
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState135Result:
    records: Table
    value: Long
    field: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState136Input:
    tile: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState136Result:
    records: Table
    value: Long
    field: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient11Input:
    tile: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.tile, 32, "tile carrier")
        uint(self.limit, 32, "limit carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCalculateLiveQuotient11Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CitySelectLiveState38Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState38Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState137Input:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState137Result:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState39Input:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState39Result:
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords22Input:
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.palette, state)
        checked_table(self.roster, state)
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
class CityProcessCountedRecords22Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityProcessCountedRecords22Service1:
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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState138Input:
    value: Long
    field: Long
    tile: Long
    row: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
class CityCoordinateLiveState138Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    palette: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState138Service1:
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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState138Service2:
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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState138Service3:
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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState139Input:
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState139Result:
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
class CityCoordinateLiveState139Service1:
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState139Service2:
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState11Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityResolveReadonlyState11Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState140Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState140Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState40Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState40Result:
    destination: Table
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState41Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState41Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState42Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState42Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState141Input:
    destination: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool
    source: Table
    row: Long
    offset: Long
    limit: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.port, state)
        uint(self.value, 32, 'value carrier')
        uint(self.field, 32, 'field carrier')
        uint(self.tile, 32, 'tile carrier')
        if any((type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow))):
            raise ValueError('strict partial arithmetic outcomes required')
        checked_table(self.source, state)
        for retained in (self.row, self.offset, self.limit):
            uint(retained, 32, 'complete clock live carrier')
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState141Result:
    destination: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool
    source: Table
    row: Long
    offset: Long
    limit: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.port, state)
        uint(self.value, 32, 'value carrier')
        uint(self.field, 32, 'field carrier')
        uint(self.tile, 32, 'tile carrier')
        if any((type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow))):
            raise ValueError('strict partial arithmetic outcomes required')
        checked_table(self.source, state)
        for retained in (self.row, self.offset, self.limit):
            uint(retained, 32, 'complete clock live carrier')
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState141Service1:
    destination: Table
    port: Table
    value: Long
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState142Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState142Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState142Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState143Input:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState143Result:
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState143Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState144Input:
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
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState144Result:
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
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState144Service1:
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
class CityCoordinateLiveState144Service2:
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
class CityCoordinateLiveState144Service3:
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
class CitySelectLiveState43Input:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
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
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState43Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    carry: bool
    zero: bool
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
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState145Input:
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
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
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
class CityCoordinateLiveState145Result:
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
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

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
class CityCoordinateLiveState146Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState146Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState146Service1:
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
class CitySelectLiveState44Input:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState44Result:
    value: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState147Input:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.roster, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState147Result:
    destination: Table
    source: Table
    roster: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
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
class CityCoordinateLiveState148Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState148Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState149Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CityCoordinateLiveState149Result:
    destination: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState45Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState45Result:
    destination: Table
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState46Input:
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class CitySelectLiveState46Result:
    destination: Table
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self
