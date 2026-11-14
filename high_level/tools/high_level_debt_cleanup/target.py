"""Explicit original allocation/register ABI, no opcode payload."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Binding:
    name: str
    entry: int
    end: int
    preserved: tuple


BINDINGS = (Binding('clear_unowned_records', 0xE8A0, 0xE8E6, ()),
            Binding('clear_selected_links', 0x115BC, 0x1161A, ('d0', 'd1', 'd2', 'a0', 'a1', 'a2')))
REGISTERS = {'clear_unowned_records': {'records': 'a0', 'owners': 'a1', 'index': 'd0', 'city': 'd3', 'flags': 'd3'},
             'clear_selected_links': {'selected_principal': 'a0', 'records': 'a0', 'owners': 'a1', 'linked_principal': 'a2',
                                      'selected_before_clear': 'd0', 'initial_offset': 'd0', 'selected': 'd1',
                                      'offset': 'd2', 'index': 'd0', 'other': 'd2', 'flags': 'd2'}}
VIEW_BASES = {'records_reverse': 0xEA34, 'records_forward': 0xE9F8, 'owners': 0xF427, 'principals': 0xE65C}
BRANCH_HINTS = {'clear_unowned_records': ('b', 'b', 'w'), 'clear_selected_links': ('w', 'w')}


def validate_binding(value):
    if (type(value) is not Binding or type(value.name) is not str or type(value.entry) is not int or type(value.end) is not int or
            type(value.preserved) is not tuple or any(type(item) is not str for item in value.preserved) or value not in BINDINGS):
        raise ValueError('strict explicit debt cleanup compatibility binding required')
