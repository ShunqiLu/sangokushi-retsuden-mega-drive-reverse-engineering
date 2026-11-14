"""Function-local immutable values and same-state view contracts.

These are not complete CPU frames or a register/PC dictionary. Retained input
carriers are explicit; return values expose only this routine's actual effects.
"""
from dataclasses import dataclass
from .domain import SceneState, Long, Table, Cursor, uint, checked_state, checked_table, checked_cursor

@dataclass(frozen=True)
class LowbankSelectLiveState1Input:
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
class LowbankSelectLiveState1Result:
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
class LowbankCoordinateLiveState1Input:
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
class LowbankCoordinateLiveState1Result:
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
class LowbankCoordinateLiveState1Service1:
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
class LowbankCoordinateLiveState1Service2:
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
class LowbankCoordinateLiveState1Service3:
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
class LowbankCoordinateLiveState1Service4:
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
class LowbankCoordinateLiveState1Service5:
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
class LowbankCoordinateLiveState2Input:
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
class LowbankCoordinateLiveState2Result:
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
class LowbankCoordinateLiveState2Service1:
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
class LowbankCoordinateLiveState2Service2:
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
class LowbankCoordinateLiveState2Service3:
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
class LowbankCoordinateLiveState2Service4:
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
class LowbankCoordinateLiveState2Service5:
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
class LowbankSelectLiveState2Input:
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
class LowbankSelectLiveState2Result:
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
class LowbankUpdateRecordFlags1Input:
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
class LowbankUpdateRecordFlags1Result:
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
class LowbankUpdateRecordFlags1Service1:
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags1Service2:
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState3Input:
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
class LowbankCoordinateLiveState3Result:
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
class LowbankCoordinateLiveState4Input:
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
class LowbankCoordinateLiveState4Result:
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
class LowbankCoordinateLiveState5Input:
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
class LowbankCoordinateLiveState5Result:
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
class LowbankCoordinateLiveState6Input:
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
class LowbankCoordinateLiveState6Result:
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
class LowbankUpdateRecordFlags2Input:
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
class LowbankUpdateRecordFlags2Result:
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
class LowbankUpdateRecordFlags2Service1:
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
class LowbankUpdateRecordFlags2Service2:
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
class LowbankUpdateRecordFlags2Service3:
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
class LowbankUpdateRecordFlags2Service4:
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
class LowbankUpdateRecordFlags2Service5:
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
class LowbankSelectLiveState3Input:
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
class LowbankSelectLiveState3Result:
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
class LowbankSelectLiveState4Input:
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
class LowbankSelectLiveState4Result:
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
class LowbankCoordinateLiveState9Input:
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
class LowbankCoordinateLiveState9Result:
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
class LowbankCoordinateLiveState9Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState10Input:
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
class LowbankCoordinateLiveState10Result:
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
class LowbankCoordinateLiveState10Service1:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState10Service2:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState5Input:
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
class LowbankSelectLiveState5Result:
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
class LowbankUpdateRecordFlags3Input:
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
class LowbankUpdateRecordFlags3Result:
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
class LowbankSelectLiveState6Input:
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
class LowbankSelectLiveState6Result:
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
class LowbankUpdateRecordFlags2Alternate1Input:
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
class LowbankUpdateRecordFlags2Alternate1Result:
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
class LowbankUpdateRecordFlags2Alternate1Service1:
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
class LowbankUpdateRecordFlags2Alternate1Service2:
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
class LowbankUpdateRecordFlags2Alternate1Service3:
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
class LowbankUpdateRecordFlags2Alternate1Service4:
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
class LowbankUpdateRecordFlags2Alternate1Service5:
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
class LowbankUpdateRecordFlags2Alternate2Input:
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
class LowbankUpdateRecordFlags2Alternate2Result:
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
class LowbankUpdateRecordFlags2Alternate2Service1:
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
class LowbankUpdateRecordFlags2Alternate2Service2:
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
class LowbankUpdateRecordFlags2Alternate2Service3:
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
class LowbankUpdateRecordFlags2Alternate2Service4:
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
class LowbankUpdateRecordFlags2Alternate2Service5:
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
class LowbankCoordinateLiveState11Input:
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
class LowbankCoordinateLiveState11Result:
    destination: Table
    source: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState11Service1:
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
class LowbankCoordinateLiveState8Input:
    value: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState8Result:
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
class LowbankCoordinateLiveState8Service1:
    value: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState8Service2:
    value: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState8Service3:
    value: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState12Input:
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
class LowbankCoordinateLiveState12Result:
    destination: Table
    source: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState12Service1:
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
class LowbankUpdateRecordFlags2Alternate3Input:
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
class LowbankUpdateRecordFlags2Alternate3Result:
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
class LowbankUpdateRecordFlags2Alternate3Service1:
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
class LowbankUpdateRecordFlags2Alternate3Service2:
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
class LowbankUpdateRecordFlags2Alternate3Service3:
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
class LowbankUpdateRecordFlags2Alternate3Service4:
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
class LowbankUpdateRecordFlags2Alternate3Service5:
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
class LowbankUpdateRecordFlags2Alternate3Service6:
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
class LowbankUpdateRecordFlags2Alternate3Service7:
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
class LowbankUpdateRecordFlags2Alternate3Service8:
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
class LowbankUpdateRecordFlags2Alternate3Service9:
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
class LowbankUpdateRecordFlags2Alternate3Service10:
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
class LowbankUpdateRecordFlags2Alternate3Service11:
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
class LowbankUpdateRecordFlags2Alternate3Service12:
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
class LowbankUpdateRecordFlags2Alternate3Service13:
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
class LowbankUpdateRecordFlags2Alternate3Service14:
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
class LowbankCoordinateLiveState7Input:
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
class LowbankCoordinateLiveState7Result:
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
class LowbankCoordinateLiveState7Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState7Service2:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags2Alternate4Input:
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
class LowbankUpdateRecordFlags2Alternate4Result:
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
class LowbankUpdateRecordFlags2Alternate4Service1:
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
class LowbankUpdateRecordFlags2Alternate4Service2:
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
class LowbankUpdateRecordFlags2Alternate4Service3:
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
class LowbankUpdateRecordFlags2Alternate4Service4:
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
class LowbankUpdateRecordFlags2Alternate4Service5:
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
class LowbankUpdateRecordFlags3Alternate1Input:
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
class LowbankUpdateRecordFlags3Alternate1Result:
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
class LowbankUpdateRecordFlags3Alternate1Service1:
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
class LowbankCoordinateLiveState13Input:
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
class LowbankCoordinateLiveState13Result:
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
class LowbankCoordinateLiveState8Alternate1Input:
    value: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState8Alternate1Result:
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
class LowbankCoordinateLiveState8Alternate1Service1:
    value: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState8Alternate1Service2:
    value: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState8Alternate1Service3:
    value: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState7Input:
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
class LowbankSelectLiveState7Result:
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
class LowbankCoordinateLiveState14Input:
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
class LowbankCoordinateLiveState14Result:
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
class LowbankSelectLiveState8Input:
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
class LowbankSelectLiveState8Result:
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
class LowbankSelectLiveState9Input:
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
class LowbankSelectLiveState9Result:
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
class LowbankSelectLiveState10Input:
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
class LowbankSelectLiveState10Result:
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
class LowbankUpdateRecordFlags2Alternate5Input:
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
class LowbankUpdateRecordFlags2Alternate5Result:
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
class LowbankUpdateRecordFlags2Alternate5Service1:
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
class LowbankUpdateRecordFlags2Alternate5Service2:
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
class LowbankUpdateRecordFlags2Alternate5Service3:
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
class LowbankUpdateRecordFlags2Alternate5Service4:
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
class LowbankUpdateRecordFlags2Alternate5Service5:
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
class LowbankCoordinateLiveState15Input:
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
class LowbankCoordinateLiveState15Result:
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
class LowbankUpdateLiveFields1Input:
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
class LowbankUpdateLiveFields1Result:
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
class LowbankCoordinateLiveState16Input:
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
class LowbankCoordinateLiveState16Result:
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
class LowbankCoordinateLiveState16Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags4Input:
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
class LowbankUpdateRecordFlags4Result:
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
class LowbankCoordinateLiveState17Input:
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
class LowbankCoordinateLiveState17Result:
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
class LowbankCoordinateLiveState17Service1:
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
class LowbankUpdateLiveFields2Input:
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
class LowbankUpdateLiveFields2Result:
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
class LowbankUpdateLiveFields3Input:
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
class LowbankUpdateLiveFields3Result:
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
class LowbankCoordinateLiveState18Input:
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
class LowbankCoordinateLiveState18Result:
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
class LowbankCoordinateLiveState18Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState18Service2:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState18Service3:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState19Input:
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
class LowbankCoordinateLiveState19Result:
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
class LowbankCoordinateLiveState19Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState19Service2:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState20Input:
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
class LowbankCoordinateLiveState20Result:
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
class LowbankCoordinateLiveState20Service1:
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
class LowbankCoordinateLiveState20Service2:
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
class LowbankCoordinateLiveState21Input:
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
class LowbankCoordinateLiveState21Result:
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
class LowbankCoordinateLiveState21Service1:
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
class LowbankCoordinateLiveState21Service2:
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
class LowbankCoordinateLiveState22Input:
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
class LowbankCoordinateLiveState22Result:
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
class LowbankCoordinateLiveState22Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState22Service2:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags3Alternate2Input:
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
class LowbankUpdateRecordFlags3Alternate2Result:
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
class LowbankUpdateRecordFlags3Alternate2Service1:
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
class LowbankCoordinateLiveState23Input:
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
class LowbankCoordinateLiveState23Result:
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
class LowbankCoordinateLiveState23Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState23Service2:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState24Input:
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
class LowbankCoordinateLiveState24Result:
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
class LowbankCoordinateLiveState25Input:
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
class LowbankCoordinateLiveState25Result:
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
class LowbankCoordinateLiveState26Input:
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
class LowbankCoordinateLiveState26Result:
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
class LowbankCoordinateLiveState27Input:
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
class LowbankCoordinateLiveState27Result:
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
class LowbankCoordinateLiveState28Input:
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
class LowbankCoordinateLiveState28Result:
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
class LowbankCoordinateLiveState29Input:
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
class LowbankCoordinateLiveState29Result:
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
class LowbankUpdateRecordFlags5Input:
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
class LowbankUpdateRecordFlags5Result:
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
class LowbankUpdateRecordFlags5Service1:
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
class LowbankCoordinateLiveState30Input:
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
class LowbankCoordinateLiveState30Result:
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
class LowbankCoordinateLiveState30Service1:
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
class LowbankCoordinateLiveState30Service2:
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
class LowbankUpdateRecordFlags6Input:
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
class LowbankUpdateRecordFlags6Result:
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
class LowbankUpdateRecordFlags6Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags6Service2:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState31Input:
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
class LowbankCoordinateLiveState31Result:
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
class LowbankCoordinateLiveState31Service1:
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
class LowbankCoordinateLiveState31Service2:
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
class LowbankCoordinateLiveState32Input:
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
class LowbankCoordinateLiveState32Result:
    destination: Table
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags7Input:
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
class LowbankUpdateRecordFlags7Result:
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
class LowbankUpdateRecordFlags7Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags7Service2:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags7Service3:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags7Service4:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState33Input:
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
class LowbankCoordinateLiveState33Result:
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
class LowbankCoordinateLiveState33Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState33Service2:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState34Input:
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
class LowbankCoordinateLiveState34Result:
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
class LowbankCoordinateLiveState34Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags8Input:
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
class LowbankUpdateRecordFlags8Result:
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
class LowbankUpdateRecordFlags8Service1:
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags8Service2:
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState11Input:
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
class LowbankSelectLiveState11Result:
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
class LowbankCoordinateLiveState35Input:
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
class LowbankCoordinateLiveState35Result:
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
class LowbankCoordinateLiveState35Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState35Service2:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState36Input:
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
class LowbankCoordinateLiveState36Result:
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
class LowbankCoordinateLiveState37Input:
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
class LowbankCoordinateLiveState37Result:
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
class LowbankCoordinateLiveState37Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState38Input:
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
class LowbankCoordinateLiveState38Result:
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
class LowbankCoordinateLiveState38Service1:
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
class LowbankCoordinateLiveState39Input:
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
class LowbankCoordinateLiveState39Result:
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
class LowbankCoordinateLiveState39Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState39Service2:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState39Service3:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState39Service4:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState39Service5:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState40Input:
    destination: Table
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState40Result:
    destination: Table
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState40Service1:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState40Service2:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState40Service3:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState40Service4:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState41Input:
    destination: Table
    source: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState41Result:
    destination: Table
    source: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState41Service1:
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
class LowbankCoordinateLiveState41Service2:
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
class LowbankCoordinateLiveState41Service3:
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
class LowbankCoordinateLiveState42Input:
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
class LowbankCoordinateLiveState42Result:
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
class LowbankCoordinateLiveState42Service1:
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
class LowbankCoordinateLiveState42Service2:
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
class LowbankCoordinateLiveState42Service3:
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
class LowbankProcessCountedRecords1Input:
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
class LowbankProcessCountedRecords1Result:
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
class LowbankCoordinateLiveState43Input:
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
class LowbankCoordinateLiveState43Result:
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
class LowbankCoordinateLiveState43Service1:
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
class LowbankCoordinateLiveState44Input:
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
class LowbankCoordinateLiveState44Result:
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
class LowbankCoordinateLiveState45Input:
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
class LowbankCoordinateLiveState45Result:
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
class LowbankCoordinateLiveState45Service1:
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState45Service2:
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState46Input:
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
class LowbankCoordinateLiveState46Result:
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
class LowbankCoordinateLiveState46Service1:
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
class LowbankCoordinateLiveState47Input:
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
class LowbankCoordinateLiveState47Result:
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
class LowbankSelectLiveState12Input:
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
class LowbankSelectLiveState12Result:
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
class LowbankCoordinateLiveState48Input:
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
class LowbankCoordinateLiveState48Result:
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
class LowbankCoordinateLiveState48Service1:
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
class LowbankCoordinateLiveState48Service2:
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
class LowbankCoordinateLiveState48Service3:
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
class LowbankCoordinateLiveState48Service4:
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
class LowbankCoordinateLiveState48Service5:
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
class LowbankCoordinateLiveState48Service6:
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
class LowbankCoordinateLiveState49Input:
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
class LowbankCoordinateLiveState49Result:
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
class LowbankCoordinateLiveState49Service1:
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
class LowbankCoordinateLiveState50Input:
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
class LowbankCoordinateLiveState50Result:
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
class LowbankCoordinateLiveState50Service1:
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
class LowbankCoordinateLiveState50Service2:
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
class LowbankCoordinateLiveState51Input:
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
class LowbankCoordinateLiveState51Result:
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
class LowbankCoordinateLiveState51Service1:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState52Input:
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
class LowbankCoordinateLiveState52Result:
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
class LowbankCoordinateLiveState52Service1:
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
class LowbankCoordinateLiveState52Service2:
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
class LowbankCoordinateLiveState53Input:
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
class LowbankCoordinateLiveState53Result:
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
class LowbankCoordinateLiveState53Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState54Input:
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
class LowbankCoordinateLiveState54Result:
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
class LowbankCoordinateLiveState54Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState54Service2:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState55Input:
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
class LowbankCoordinateLiveState55Result:
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
class LowbankCoordinateLiveState55Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState55Service2:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState55Service3:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState56Input:
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
class LowbankCoordinateLiveState56Result:
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
class LowbankCoordinateLiveState56Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState56Service2:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState13Input:
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
class LowbankSelectLiveState13Result:
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
class LowbankSelectLiveState14Input:
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
class LowbankSelectLiveState14Result:
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
class LowbankSelectLiveState15Input:
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
class LowbankSelectLiveState15Result:
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
class LowbankCoordinateLiveState57Input:
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
class LowbankCoordinateLiveState57Result:
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
class LowbankCoordinateLiveState57Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState57Service2:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState58Input:
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
class LowbankCoordinateLiveState58Result:
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
class LowbankUpdateLiveFields4Input:
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
class LowbankUpdateLiveFields4Result:
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
class LowbankSelectLiveState16Input:
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
class LowbankSelectLiveState16Result:
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
class LowbankProcessDeviceControl1Input:
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
class LowbankProcessDeviceControl1Result:
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
class LowbankProcessDeviceControl1Service1:
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
class LowbankProcessDeviceControl1Service2:
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
class LowbankSelectLiveState17Input:
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
class LowbankSelectLiveState17Result:
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
class LowbankProcessCountedRecords2Input:
    destination: Table
    value: Long
    field: Long
    limit: Long
    remaining: Long
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
        uint(self.limit, 32, "limit carrier")
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords2Result:
    destination: Table
    value: Long
    field: Long
    limit: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl2Input:
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
class LowbankProcessDeviceControl2Result:
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
class LowbankProcessDeviceControl3Input:
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
class LowbankProcessDeviceControl3Result:
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
    remaining: Long
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
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service1:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service2:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service3:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service4:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service5:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service6:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service7:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service8:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service9:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service10:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service11:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service12:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service13:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service14:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service15:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service16:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service17:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service18:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl3Service19:
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
    remaining: Long

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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords3Input:
    value: Long
    field: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords3Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    remaining: Long
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
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords4Input:
    source: Table
    value: Long
    offset: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords4Result:
    destination: Table
    source: Table
    value: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState18Input:
    source: Table
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState18Result:
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
class LowbankProcessCountedRecords5Input:
    destination: Table
    source: Table
    value: Long
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
        uint(self.value, 32, "value carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords5Result:
    destination: Table
    source: Table
    value: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords6Input:
    source: Table
    port: Table
    value: Long
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
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords6Result:
    destination: Table
    source: Table
    port: Table
    value: Long
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
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords6Service1:
    destination: Table
    source: Table
    port: Table
    value: Long
    offset: Long
    limit: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState59Input:
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
class LowbankCoordinateLiveState59Result:
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
class LowbankCoordinateLiveState59Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState59Service2:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl5Input:
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
class LowbankProcessDeviceControl5Result:
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
class LowbankCoordinateLiveState60Input:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
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
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState60Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
    remaining: Long
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
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState60Service1:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    limit: Long
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
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState61Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    limit: Long
    remaining: Long
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
        uint(self.tile, 32, "tile carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState61Result:
    destination: Table
    value: Long
    field: Long
    tile: Long
    limit: Long
    remaining: Long
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
        uint(self.limit, 32, "limit carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState61Service1:
    destination: Table
    value: Long
    field: Long
    tile: Long
    limit: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState61Service2:
    destination: Table
    value: Long
    field: Long
    tile: Long
    limit: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState61Service3:
    destination: Table
    value: Long
    field: Long
    tile: Long
    limit: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState61Service4:
    destination: Table
    value: Long
    field: Long
    tile: Long
    limit: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.limit, 32, "limit carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl6Input:
    destination: Table
    port: Table
    value: Long
    remaining: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl6Result:
    destination: Table
    port: Table
    value: Long
    field: Long
    remaining: Long
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
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl6Service1:
    destination: Table
    port: Table
    value: Long
    field: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState62Input:
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
class LowbankCoordinateLiveState62Result:
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
class LowbankSelectLiveState19Input:
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
class LowbankSelectLiveState19Result:
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
class LowbankSelectLiveState19Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl4Input:
    value: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl4Result:
    port: Table
    value: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl4Service1:
    port: Table
    value: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl4Service2:
    port: Table
    value: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState63Input:
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
class LowbankCoordinateLiveState63Result:
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
class LowbankProcessDeviceControl7Input:
    value: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl7Result:
    port: Table
    value: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState64Input:
    value: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState64Result:
    port: Table
    value: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState64Service1:
    port: Table
    value: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState65Input:
    destination: Table
    source: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState65Result:
    destination: Table
    source: Table
    port: Table
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
class LowbankCoordinateLiveState66Input:
    destination: Table
    source: Table
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
class LowbankCoordinateLiveState66Result:
    destination: Table
    source: Table
    port: Table
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
        checked_table(self.port, state)
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
class LowbankProcessDeviceControl8Input:
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
class LowbankProcessDeviceControl8Result:
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
class LowbankProcessDeviceControl8Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl9Input:
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl9Result:
    port: Table
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.port, state)
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl9Service1:
    port: Table
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.port, state)
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState20Input:
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
class LowbankSelectLiveState20Result:
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
class LowbankCoordinateLiveState67Input:
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
class LowbankCoordinateLiveState67Result:
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
class LowbankCoordinateLiveState67Service1:
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
class LowbankSelectLiveState21Input:
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
class LowbankSelectLiveState21Result:
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
class LowbankCoordinateLiveState68Input:
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
class LowbankCoordinateLiveState68Result:
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
class LowbankCoordinateLiveState69Input:
    source: Table
    value: Long
    field: Long
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
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState69Result:
    destination: Table
    source: Table
    value: Long
    field: Long
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
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessDeviceControl10Input:
    source: Table
    descriptor: Table
    records: Table
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
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
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
class LowbankProcessDeviceControl10Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
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
class LowbankCoordinateLiveState70Input:
    source: Table
    value: Long
    field: Long
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
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState70Result:
    destination: Table
    source: Table
    value: Long
    field: Long
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
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState71Input:
    source: Table
    value: Long
    field: Long
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
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState71Result:
    destination: Table
    source: Table
    value: Long
    field: Long
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
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankUpdateLiveFields5Input:
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
class LowbankUpdateLiveFields5Result:
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
class LowbankUpdateLiveFields5Service1:
    row: Long

    def validate(self, state):
        checked_state(state)
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState22Input:
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
class LowbankSelectLiveState22Result:
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
class LowbankSelectLiveState22Service1:
    row: Long

    def validate(self, state):
        checked_state(state)
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState72Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
    member: Long
    remaining: Long
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
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState72Result:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
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
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState73Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
    member: Long
    remaining: Long
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
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState73Result:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
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
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords7Input:
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
    member: Long
    remaining: Long
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
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords7Result:
    port: Table
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
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords7Service1:
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords7Alternate1Input:
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
    remaining: Long
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
        uint(self.offset, 32, "offset carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords7Alternate1Result:
    port: Table
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
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords7Alternate1Service1:
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState23Input:
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
class LowbankSelectLiveState23Result:
    port: Table
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.port, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState24Input:
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
class LowbankSelectLiveState24Result:
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
class LowbankSelectLiveState24Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState25Input:
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
class LowbankSelectLiveState25Result:
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
class LowbankSelectLiveState25Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords8Input:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
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
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords8Result:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
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
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords8Alternate1Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
    member: Long
    remaining: Long
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
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords8Alternate1Result:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
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
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords8Alternate2Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
    member: Long
    remaining: Long
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
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords8Alternate2Result:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
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
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords8Alternate3Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
    member: Long
    remaining: Long
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
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords8Alternate3Result:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
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
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords8Alternate4Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
    member: Long
    remaining: Long
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
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords8Alternate4Result:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
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
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords8Alternate5Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
    member: Long
    remaining: Long
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
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords8Alternate5Result:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long
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
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords9Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    member: Long
    remaining: Long
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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords9Result:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
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
class LowbankProcessCountedRecords9Service1:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    member: Long
    remaining: Long

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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords9Alternate1Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    member: Long
    remaining: Long
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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords9Alternate1Result:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
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
class LowbankProcessCountedRecords9Alternate1Service1:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    member: Long
    remaining: Long

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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords9Alternate2Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    member: Long
    remaining: Long
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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords9Alternate2Result:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
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
class LowbankProcessCountedRecords9Alternate2Service1:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    member: Long
    remaining: Long

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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords9Alternate3Input:
    destination: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    member: Long
    remaining: Long
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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords9Alternate3Result:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
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
class LowbankProcessCountedRecords9Alternate3Service1:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
    member: Long
    remaining: Long

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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState74Input:
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
class LowbankCoordinateLiveState74Result:
    destination: Table
    value: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState75Input:
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
class LowbankCoordinateLiveState75Result:
    destination: Table
    value: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState76Input:
    destination: Table
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState76Result:
    destination: Table
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState76Service1:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState76Service2:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState76Service3:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState76Alternate1Input:
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
class LowbankCoordinateLiveState76Alternate1Result:
    destination: Table
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState76Alternate1Service1:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState76Alternate1Service2:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState76Alternate1Service3:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords10Input:
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
class LowbankProcessCountedRecords10Result:
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
class LowbankCoordinateLiveState77Input:
    destination: Table
    field: Long
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState77Result:
    destination: Table
    source: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState77Service1:
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
class LowbankCoordinateLiveState77Service2:
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
class LowbankCoordinateLiveState77Service3:
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
class LowbankUpdateLiveFields6Input:
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
class LowbankUpdateLiveFields6Result:
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
class LowbankProcessCountedRecords11Input:
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
class LowbankProcessCountedRecords11Result:
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
class LowbankCoordinateLiveState78Input:
    destination: Table
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
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState78Result:
    destination: Table
    source: Table
    port: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState78Service1:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords12Input:
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
class LowbankProcessCountedRecords12Result:
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
class LowbankProcessDeviceControl11Input:
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
class LowbankProcessDeviceControl11Result:
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
class LowbankProcessDeviceControl11Service1:
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
class LowbankProcessDeviceControl11Service2:
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
class LowbankSelectLiveState26Input:
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
class LowbankSelectLiveState26Result:
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
class LowbankCoordinateLiveState79Input:
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
class LowbankCoordinateLiveState79Result:
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
class LowbankCoordinateLiveState79Service1:
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
class LowbankProcessCountedRecords13Input:
    destination: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords13Result:
    destination: Table
    source: Table
    port: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords13Service1:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords14Input:
    destination: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords14Result:
    destination: Table
    source: Table
    port: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords14Service1:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords13Alternate1Input:
    destination: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords13Alternate1Result:
    destination: Table
    source: Table
    port: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords13Alternate1Service1:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords13Alternate2Input:
    destination: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords13Alternate2Result:
    destination: Table
    source: Table
    port: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords13Alternate2Service1:
    destination: Table
    source: Table
    port: Table
    value: Long
    field: Long
    tile: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState80Input:
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
class LowbankCoordinateLiveState80Result:
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
class LowbankCoordinateLiveState80Service1:
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
class LowbankCoordinateLiveState81Input:
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
class LowbankCoordinateLiveState81Result:
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
class LowbankCoordinateLiveState81Service1:
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
class LowbankCoordinateLiveState82Input:
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
class LowbankCoordinateLiveState82Result:
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
class LowbankCoordinateLiveState82Service1:
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
class LowbankProcessCountedRecords15Input:
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
class LowbankProcessCountedRecords15Result:
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
class LowbankCoordinateLiveState83Input:
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
class LowbankCoordinateLiveState83Result:
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
class LowbankUpdateLiveFields7Input:
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
class LowbankUpdateLiveFields7Result:
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
class LowbankProcessCountedRecords16Input:
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
class LowbankProcessCountedRecords16Result:
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
class LowbankProcessCountedRecords16Service1:
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
class LowbankProcessCountedRecords17Input:
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
class LowbankProcessCountedRecords17Result:
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
class LowbankSelectLiveState27Input:
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
class LowbankSelectLiveState27Result:
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
class LowbankCoordinateLiveState84Input:
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
class LowbankCoordinateLiveState84Result:
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
class LowbankCoordinateLiveState84Service1:
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
class LowbankProcessCountedRecords18Input:
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
class LowbankProcessCountedRecords18Result:
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
class LowbankUpdateRecordFlags9Input:
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
class LowbankUpdateRecordFlags9Result:
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
class LowbankUpdateRecordFlags9Service1:
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
class LowbankCoordinateLiveState85Input:
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
class LowbankCoordinateLiveState85Result:
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
class LowbankCoordinateLiveState85Service1:
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState85Service2:
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState85Service3:
    value: Long
    field: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        return self

@dataclass(frozen=True)
class LowbankResolveReadonlyState1Input:
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
class LowbankResolveReadonlyState1Result:
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
class LowbankProcessCountedRecords19Input:
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
class LowbankProcessCountedRecords19Result:
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
class LowbankCoordinateLiveState86Input:
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
class LowbankCoordinateLiveState86Result:
    destination: Table
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState86Service1:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState86Service2:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords20Input:
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
class LowbankProcessCountedRecords20Result:
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
class LowbankProcessCountedRecords21Input:
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
class LowbankProcessCountedRecords21Result:
    destination: Table
    source: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState87Input:
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
class LowbankCoordinateLiveState87Result:
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
class LowbankCoordinateLiveState87Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState87Service2:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState87Service3:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState28Input:
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
class LowbankSelectLiveState28Result:
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
class LowbankSelectLiveState29Input:
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
class LowbankSelectLiveState29Result:
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
class LowbankSelectLiveState29Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState29Service2:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState29Service3:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState29Service4:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags10Input:
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
class LowbankUpdateRecordFlags10Result:
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
class LowbankUpdateRecordFlags10Service1:
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
class LowbankProcessCountedRecords22Input:
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
class LowbankProcessCountedRecords22Result:
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
class LowbankProcessCountedRecords23Input:
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
class LowbankProcessCountedRecords23Result:
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
class LowbankCoordinateLiveState88Input:
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
class LowbankCoordinateLiveState88Result:
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
class LowbankProcessCountedRecords24Input:
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
class LowbankProcessCountedRecords24Result:
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
class LowbankUpdateLiveFields8Input:
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
class LowbankUpdateLiveFields8Result:
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
class LowbankProcessCountedRecords25Input:
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
class LowbankProcessCountedRecords25Result:
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
class LowbankProcessCountedRecords26Input:
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
class LowbankProcessCountedRecords26Result:
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
class LowbankProcessCountedRecords27Input:
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
class LowbankProcessCountedRecords27Result:
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
class LowbankCoordinateLiveState90Input:
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
class LowbankCoordinateLiveState90Result:
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
class LowbankCoordinateLiveState90Service1:
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
class LowbankCoordinateLiveState90Service2:
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
class LowbankCoordinateLiveState91Input:
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
class LowbankCoordinateLiveState91Result:
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
class LowbankCoordinateLiveState91Alternate1Input:
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
class LowbankCoordinateLiveState91Alternate1Result:
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
class LowbankSelectLiveState30Input:
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
class LowbankSelectLiveState30Result:
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
class LowbankProcessCountedRecords28Input:
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
class LowbankProcessCountedRecords28Result:
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
class LowbankProcessCountedRecords28Service1:
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
class LowbankProcessCountedRecords29Input:
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
class LowbankProcessCountedRecords29Result:
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
class LowbankCoordinateLiveState92Input:
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
class LowbankCoordinateLiveState92Result:
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
class LowbankCoordinateLiveState92Service1:
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
class LowbankSelectLiveState31Input:
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
class LowbankSelectLiveState31Result:
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
class LowbankCoordinateLiveState93Input:
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
class LowbankCoordinateLiveState93Result:
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
class LowbankProcessCountedRecords30Input:
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
class LowbankProcessCountedRecords30Result:
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
class LowbankProcessCountedRecords31Input:
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
class LowbankProcessCountedRecords31Result:
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
class LowbankProcessCountedRecords33Input:
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
class LowbankProcessCountedRecords33Result:
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
class LowbankProcessCountedRecords34Input:
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
class LowbankProcessCountedRecords34Result:
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
class LowbankCoordinateLiveState94Input:
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
class LowbankCoordinateLiveState94Result:
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
class LowbankCoordinateLiveState95Input:
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
class LowbankCoordinateLiveState95Result:
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
class LowbankCoordinateLiveState95Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState96Input:
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
class LowbankCoordinateLiveState96Result:
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
class LowbankUpdateRecordFlags11Input:
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
class LowbankUpdateRecordFlags11Result:
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
class LowbankCoordinateLiveState97Input:
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
class LowbankCoordinateLiveState97Result:
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
class LowbankCoordinateLiveState98Input:
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
class LowbankCoordinateLiveState98Result:
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
class LowbankCoordinateLiveState98Service1:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState98Service2:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState98Service3:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState99Input:
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
class LowbankCoordinateLiveState99Result:
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
class LowbankProcessCountedRecords35Input:
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
class LowbankProcessCountedRecords35Result:
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
class LowbankProcessCountedRecords36Input:
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
class LowbankProcessCountedRecords36Result:
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
class LowbankCoordinateLiveState100Input:
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
class LowbankCoordinateLiveState100Result:
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
class LowbankCoordinateLiveState101Input:
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
class LowbankCoordinateLiveState101Result:
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
class LowbankCoordinateLiveState101Service1:
    value: Long

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState102Input:
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
class LowbankCoordinateLiveState102Result:
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
class LowbankSelectLiveState32Input:
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
class LowbankSelectLiveState32Result:
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
class LowbankCoordinateLiveState103Input:
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
class LowbankCoordinateLiveState103Result:
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
class LowbankCoordinateLiveState103Service1:
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
class LowbankCoordinateLiveState103Service2:
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
class LowbankCoordinateLiveState103Service3:
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
class LowbankUpdateLiveFields9Input:
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
class LowbankUpdateLiveFields9Result:
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
class LowbankCoordinateLiveState104Input:
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
class LowbankCoordinateLiveState104Result:
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
class LowbankUpdateRecordFlags12Input:
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
class LowbankUpdateRecordFlags12Result:
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
class LowbankSelectLiveState33Input:
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
class LowbankSelectLiveState33Result:
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
class LowbankUpdateRecordFlags12Alternate1Input:
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
class LowbankUpdateRecordFlags12Alternate1Result:
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
class LowbankCoordinateLiveState105Input:
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
class LowbankCoordinateLiveState105Result:
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
class LowbankCoordinateLiveState105Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCalculateLiveQuotient1Input:
    value: Long
    tile: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCalculateLiveQuotient1Result:
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
class LowbankCalculateLiveQuotient1Service1:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCalculateLiveQuotient1Service2:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCalculateLiveQuotient1Service3:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue1Input:
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
class LowbankScaleLiveRecordValue1Result:
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
class LowbankScaleLiveRecordValue1Service1:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue1Service2:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue1Service3:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue1Service4:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankUpdateLiveFields10Input:
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
class LowbankUpdateLiveFields10Result:
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
class LowbankCoordinateLiveState107Input:
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
class LowbankCoordinateLiveState107Result:
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
class LowbankCoordinateLiveState107Service1:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState107Service2:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState107Service3:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags13Input:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
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
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags13Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
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
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags13Service1:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    value: Long
    field: Long
    tile: Long
    row: Long

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
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags13Service2:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    value: Long
    field: Long
    tile: Long
    row: Long

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
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState106Input:
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
class LowbankCoordinateLiveState106Result:
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
class LowbankCoordinateLiveState106Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankUpdateLiveFields11Input:
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
class LowbankUpdateLiveFields11Result:
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
class LowbankCoordinateLiveState108Input:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
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
class LowbankCoordinateLiveState108Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
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
class LowbankCoordinateLiveState108Service1:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
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
class LowbankCalculateLiveQuotient2Input:
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
class LowbankCalculateLiveQuotient2Result:
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
class LowbankCalculateLiveQuotient2Service1:
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
class LowbankCalculateLiveQuotient2Service2:
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
class LowbankCoordinateLiveState106Alternate1Input:
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
class LowbankCoordinateLiveState106Alternate1Result:
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
class LowbankCoordinateLiveState106Alternate1Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankCalculateLiveQuotient3Input:
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
class LowbankCalculateLiveQuotient3Result:
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
class LowbankCalculateLiveQuotient3Service1:
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
class LowbankCalculateLiveQuotient3Service2:
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
class LowbankCalculateLiveQuotient3Service3:
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
class LowbankCoordinateLiveState109Input:
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
class LowbankCoordinateLiveState109Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
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
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState109Service1:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    value: Long
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState109Service2:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    value: Long
    field: Long
    tile: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags14Input:
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
class LowbankUpdateRecordFlags14Result:
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
class LowbankSelectLiveState34Input:
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
class LowbankSelectLiveState34Result:
    destination: Table
    source: Table
    descriptor: Table
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
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords37Input:
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
class LowbankProcessCountedRecords37Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
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
class LowbankProcessCountedRecords37Service1:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    value: Long
    field: Long
    tile: Long
    row: Long
    offset: Long
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
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankCalculateLiveQuotient4Input:
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
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCalculateLiveQuotient4Result:
    descriptor: Table
    records: Table
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
        checked_table(self.records, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState110Input:
    destination: Table
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
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState110Result:
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
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState110Service1:
    destination: Table
    field: Long
    tile: Long
    row: Long
    offset: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        return self

@dataclass(frozen=True)
class LowbankUpdateLiveFields12Input:
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankUpdateLiveFields12Result:
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankUpdateLiveFields13Input:
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankUpdateLiveFields13Result:
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankUpdateLiveFields14Input:
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankUpdateLiveFields14Result:
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.field, 32, "field carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankUpdateLiveFields15Input:
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankUpdateLiveFields15Result:
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankUpdateLiveFields16Input:
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
class LowbankUpdateLiveFields16Result:
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
class LowbankUpdateLiveFields17Input:
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
class LowbankUpdateLiveFields17Result:
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
class LowbankUpdateLiveFields18Input:
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
class LowbankUpdateLiveFields18Result:
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
class LowbankUpdateLiveFields19Input:
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
class LowbankUpdateLiveFields19Result:
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
class LowbankScaleLiveRecordValue2Input:
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
class LowbankScaleLiveRecordValue2Result:
    source: Table
    descriptor: Table
    records: Table
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
class LowbankScaleLiveRecordValue2Service1:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue2Service2:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
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
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState111Input:
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
class LowbankCoordinateLiveState111Result:
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
class LowbankCoordinateLiveState112Input:
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
class LowbankCoordinateLiveState112Result:
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
class LowbankCoordinateLiveState112Service1:
    pass

    def validate(self, state):
        checked_state(state)
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags15Input:
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
class LowbankUpdateRecordFlags15Result:
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
class LowbankProcessCountedRecords38Input:
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
class LowbankProcessCountedRecords38Result:
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
class LowbankProcessCountedRecords38Service1:
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
class LowbankProcessCountedRecords38Service2:
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
class LowbankProcessCountedRecords38Service3:
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
class LowbankCalculateLiveQuotient5Input:
    field: Long
    tile: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCalculateLiveQuotient5Result:
    palette: Table
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
        checked_table(self.palette, state)
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
class LowbankCoordinateLiveState113Input:
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
class LowbankCoordinateLiveState113Result:
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
class LowbankCoordinateLiveState113Service1:
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
class LowbankCoordinateLiveState114Input:
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
class LowbankCoordinateLiveState114Result:
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
class LowbankCoordinateLiveState114Service1:
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
class LowbankCoordinateLiveState114Service2:
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
class LowbankCoordinateLiveState115Input:
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
class LowbankCoordinateLiveState115Result:
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
class LowbankCoordinateLiveState116Input:
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
class LowbankCoordinateLiveState116Result:
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
class LowbankCoordinateLiveState117Input:
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
class LowbankCoordinateLiveState117Result:
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
class LowbankCoordinateLiveState118Input:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
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
class LowbankCoordinateLiveState118Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
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
class LowbankCoordinateLiveState118Service1:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
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
class LowbankScaleLiveRecordValue3Input:
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
class LowbankScaleLiveRecordValue3Result:
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
class LowbankResolveReadonlyState2Input:
    tile: Long
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankResolveReadonlyState2Result:
    destination: Table
    row: Long
    offset: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue4Input:
    destination: Table
    tile: Long
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
        uint(self.tile, 32, "tile carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue4Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
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
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue4Service1:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue4Service2:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue4Service3:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState119Input:
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
class LowbankCoordinateLiveState119Result:
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
class LowbankCoordinateLiveState119Service1:
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
class LowbankCoordinateLiveState119Alternate1Input:
    value: Long
    row: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.value, 32, "value carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState119Alternate1Result:
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
class LowbankCoordinateLiveState119Alternate1Service1:
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
class LowbankCoordinateLiveState119Alternate1Service2:
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
class LowbankCoordinateLiveState119Alternate1Service3:
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
class LowbankCoordinateLiveState119Alternate2Input:
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
class LowbankCoordinateLiveState119Alternate2Result:
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
class LowbankCoordinateLiveState119Alternate2Service1:
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
class LowbankCoordinateLiveState119Alternate2Service2:
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
class LowbankCoordinateLiveState119Alternate2Service3:
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
class LowbankCoordinateLiveState120Input:
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
class LowbankCoordinateLiveState120Result:
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
class LowbankCoordinateLiveState121Input:
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
class LowbankCoordinateLiveState121Result:
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
class LowbankCoordinateLiveState122Input:
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
class LowbankCoordinateLiveState122Result:
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
class LowbankCoordinateLiveState123Input:
    tile: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState123Result:
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
class LowbankScaleLiveRecordValue4Alternate1Input:
    destination: Table
    value: Long
    tile: Long
    member: Long
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.member, 32, "member carrier")
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue4Alternate1Result:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
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
        uint(self.member, 32, "member carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue4Alternate1Service1:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue4Alternate1Service2:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue4Alternate1Service3:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue4Alternate1Service4:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue4Alternate1Service5:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankScaleLiveRecordValue4Alternate1Service6:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    member: Long
    remaining: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.member, 32, "member carrier")
        uint(self.remaining, 32, "remaining carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState124Input:
    destination: Table
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
        checked_table(self.destination, state)
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
class LowbankCoordinateLiveState124Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    port: Table
    value: Long
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
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState124Service1:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
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
        checked_table(self.descriptor, state)
        checked_table(self.records, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState35Input:
    destination: Table
    source: Table
    descriptor: Table
    port: Table
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
        checked_table(self.port, state)
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState35Result:
    destination: Table
    source: Table
    descriptor: Table
    tile: Long
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
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState36Input:
    destination: Table
    port: Table
    value: Long
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
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState36Result:
    destination: Table
    source: Table
    descriptor: Table
    records: Table
    tile: Long
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
        uint(self.tile, 32, "tile carrier")
        uint(self.offset, 32, "offset carrier")
        uint(self.limit, 32, "limit carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags16Input:
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
class LowbankUpdateRecordFlags16Result:
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
class LowbankUpdateRecordFlags16Service1:
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
class LowbankUpdateRecordFlags16Service2:
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
class LowbankCoordinateLiveState125Input:
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
class LowbankCoordinateLiveState125Result:
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
class LowbankCoordinateLiveState125Service1:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState126Input:
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
class LowbankCoordinateLiveState126Result:
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
class LowbankCoordinateLiveState126Service1:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState126Service2:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState126Service3:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState126Service4:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState126Service5:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState126Service6:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState126Service7:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState126Service8:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState126Service9:
    destination: Table
    source: Table
    value: Long
    field: Long
    tile: Long
    row: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags17Input:
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
class LowbankUpdateRecordFlags17Result:
    destination: Table
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags17Service1:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags17Service2:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags17Service3:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags17Service4:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags17Service5:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState127Input:
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
class LowbankCoordinateLiveState127Result:
    destination: Table
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState127Service1:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState127Service2:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState37Input:
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
class LowbankSelectLiveState37Result:
    destination: Table
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState37Service1:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags18Input:
    source: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags18Result:
    destination: Table
    source: Table
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
        checked_table(self.source, state)
        checked_table(self.port, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankUpdateRecordFlags18Service1:
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
class LowbankUpdateRecordFlags18Service2:
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
class LowbankSelectLiveState38Input:
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
class LowbankSelectLiveState38Result:
    destination: Table
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankSelectLiveState38Service1:
    destination: Table

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        return self

@dataclass(frozen=True)
class LowbankCalculateLiveQuotient6Input:
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
class LowbankCalculateLiveQuotient6Result:
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
class LowbankCalculateLiveQuotient6Service1:
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
class LowbankCalculateLiveQuotient6Service2:
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
class LowbankCalculateLiveQuotient6Service3:
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
class LowbankCalculateLiveQuotient6Service4:
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
class LowbankCalculateLiveQuotient6Service5:
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
class LowbankCoordinateLiveState128Input:
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
class LowbankCoordinateLiveState128Result:
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
class LowbankCoordinateLiveState128Service1:
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
class LowbankScaleLiveRecordValue5Input:
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
class LowbankScaleLiveRecordValue5Result:
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
class LowbankScaleLiveRecordValue5Service1:
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
class LowbankScaleLiveRecordValue5Service2:
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
class LowbankScaleLiveRecordValue5Service3:
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
class LowbankScaleLiveRecordValue5Service4:
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
class LowbankScaleLiveRecordValue5Service5:
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
class LowbankScaleLiveRecordValue5Service6:
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
class LowbankScaleLiveRecordValue5Service7:
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
class LowbankScaleLiveRecordValue5Service8:
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
class LowbankScaleLiveRecordValue5Service9:
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
class LowbankScaleLiveRecordValue5Service10:
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
class LowbankCoordinateLiveState129Input:
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
class LowbankCoordinateLiveState129Result:
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
class LowbankCoordinateLiveState129Service1:
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
class LowbankCoordinateLiveState129Service2:
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
class LowbankCoordinateLiveState129Service3:
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
class LowbankCoordinateLiveState129Service4:
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
class LowbankCoordinateLiveState129Service5:
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
class LowbankCoordinateLiveState129Service6:
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
class LowbankCoordinateLiveState129Service7:
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
class LowbankProcessCountedRecords39Input:
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
class LowbankProcessCountedRecords39Result:
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
class LowbankProcessCountedRecords39Service1:
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
class LowbankProcessCountedRecords39Service2:
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
class LowbankProcessCountedRecords39Service3:
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
class LowbankCoordinateLiveState130Input:
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
class LowbankCoordinateLiveState130Result:
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
class LowbankCoordinateLiveState130Service1:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState130Service2:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState130Service3:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState130Service4:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState130Service5:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState130Service6:
    destination: Table
    value: Long

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        uint(self.value, 32, "value carrier")
        return self

@dataclass(frozen=True)
class LowbankCoordinateLiveState89Input:
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
class LowbankCoordinateLiveState89Result:
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
class LowbankProcessCountedRecords32Input:
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
        checked_table(self.descriptor, state)
        uint(self.value, 32, "value carrier")
        uint(self.field, 32, "field carrier")
        uint(self.tile, 32, "tile carrier")
        uint(self.row, 32, "row carrier")
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError("strict partial arithmetic outcomes required")
        return self

@dataclass(frozen=True)
class LowbankProcessCountedRecords32Result:
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
