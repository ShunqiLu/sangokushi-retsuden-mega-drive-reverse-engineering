"""Closed same-state equipment-menu ports and genuine returned fields.

No copied RAM, fake register dictionary, files, decoder or synthetic SP.
"""
from dataclasses import dataclass
from .domain import GameState, Word, Long, SCALARS, VIEW_BASES, uint
from .contexts_numeric import DecimalMemory


class EquipmentMenuMemory:
    """The established player/Scene state pair, not a second state."""
    def __init__(self, state, stack_cursor=None):
        self.numeric = DecimalMemory(state, stack_cursor)
        self.state = state

    @property
    def stack_cursor(self):
        return self.numeric.stack_cursor

    def enter_call(self, continuation):
        self.numeric.enter_call(continuation)

    def leave_call(self, continuation):
        self.numeric.leave_call(continuation)

    def check_cursor(self, value):
        self.numeric.check_cursor(value)

    def scalar(self, name):
        if name not in ('queue_offset', 'equipment_input', 'recruitment_input',
                        'amount_digit_position', 'command_id',
                        'special_equipment_amount', 'action_amount'):
            raise ValueError('exact equipment-menu scalar required')
        address, size = SCALARS[name]
        return self.state.read(address, size)

    def set_scalar(self, name, value):
        if name != 'queue_offset':
            raise ValueError('equipment queue write required')
        address, size = SCALARS[name]
        self.state.write(address, size, uint(value, size * 8))

    def view(self, name):
        if name not in ('display_queue', 'recruitment_digit_scratch',
                        'command_digit_scratch'):
            raise ValueError('exact equipment-menu live view required')
        return self.state.table(VIEW_BASES[name])


@dataclass(frozen=True)
class EquipmentMenuFields:
    """Actual A0/A1, low D0..D3 and optional full D0 numeric basis.

    1270A changes D0 as a LONG; the later DBRA changes only its WORD. That
    current full basis is retained, not the old caller's high WORD. D1/D2/D3
    remain WORD writes, so absent caller high halves are never invented.
    """
    destination: object
    source_if_written: object | None
    value: Word
    field_if_written: Word | None
    tile_if_written: Word | None
    row_if_written: Word | None
    full_value_basis: Long | None
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, memory):
        if type(memory) is not EquipmentMenuMemory:
            raise ValueError('sealed equipment-menu memory required')
        memory.check_cursor(self.destination)
        if self.source_if_written is not None:
            memory.check_cursor(self.source_if_written)
        uint(self.value, 16)
        for value in (self.field_if_written, self.tile_if_written,
                      self.row_if_written):
            if value is not None:
                uint(value, 16)
        if self.full_value_basis is not None:
            uint(self.full_value_basis, 32)
        if any(type(flag) is not bool for flag in
               (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('actual final queue-ADD flags required')
        return self
