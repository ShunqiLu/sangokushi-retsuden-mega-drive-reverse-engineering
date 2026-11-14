"""Original-compatible addresses, register storage, and fixed target extent.

This isolated compatibility layer is not business logic or stored machine code.
The dividend helper is an explicit external dependency until its separate
high-level implementation has been independently accepted.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Binding:
    entry: int = 0xFBAA
    allocated_bytes: int = 70
    year_address: int = 0xFFFFF374
    month_address: int = 0xFFFFF375
    record_register: str = 'a1'
    offset_register: str = 'd0'
    principal_register: str = 'd1'
    division_entry: int = 0x35760
    scratch_register: str = 'd3'
    year_displacement: int = 2
    month_displacement: int = 3


BINDING = Binding()
# Virtual-local allocation hints are independent of the names used in source.
# The front end supplies definition order; liveness must validate every reuse.
ALLOCATION = ('d2', 'd2', 'd3', 'd2', 'd2', 'd3', 'd2', 'd2', 'd1')


def validate_binding(binding):
    if type(binding) is not Binding:
        raise ValueError('explicit finance Binding required')
    for field in ('entry', 'allocated_bytes', 'year_address', 'month_address',
                  'division_entry', 'year_displacement', 'month_displacement'):
        if type(getattr(binding, field)) is not int:
            raise ValueError('strict integer binding fields required')
    if binding != BINDING:
        raise ValueError('only reviewed original ABI/extent is currently admitted')
