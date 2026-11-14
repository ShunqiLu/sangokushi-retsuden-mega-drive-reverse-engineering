"""Original complete extents and fixed ABI/data bindings; no code payload."""
from dataclasses import dataclass
from .domain import VIEW_BASES,SCALARS


@dataclass(frozen=True)
class Binding:
    name:str
    entry:int
    end:int
    completion:str='return'


DISPOSITION_BINDINGS=(
    Binding('collect_city_attached_officers',0x1C2A0,0x1C2C8),
    Binding('collect_unassigned_city_officers',0x1C2C8,0x1C2FC),
    Binding('rebuild_primary_after_battle',0x1C82C,0x1C8BC),
    Binding('sort_returning_officer_status',0x1C8BC,0x1C942),
    Binding('partition_city_survivors',0x1C942,0x1C9FE),
    Binding('owner_has_other_city_carry',0x1C9FE,0x1CA3C),
    Binding('restore_returning_officer_assignments',0x1CA3C,0x1CA60),
    Binding('allocate_packed_group_resources',0x1CA60,0x1CB08),
    Binding('rebuild_secondary_after_battle',0x1CB08,0x1CB96),
)
MEMBERS_BINDINGS=(
    Binding('settle_battle_packed_armies',0x1D03C,0x1D0A2),
    Binding('remove_defeated_packed_member',0x1D0A2,0x1D142),
    Binding('replace_or_remove_group_references',0x1D142,0x1D198),
    Binding('transfer_outcome_officer',0x1D198,0x1D20A),
    Binding('detach_member_keep_group_cursor',0x1D20A,0x1D29E),
    Binding('replace_group_head_reference',0x1D29E,0x1D2E8),
    Binding('remove_group_reference',0x1D2E8,0x1D318),
    Binding('attach_member_shift_packet',0x1D318,0x1D3BC),
)
ARRIVAL_BINDINGS=(
    Binding('settle_group_at_city',0x1D3BC,0x1D40C),
    Binding('locate_group_city',0x1D40C,0x1D44C),
    Binding('credit_packed_group_resources',0x1D44C,0x1D4B8),
    Binding('erase_group_packet',0x1D4B8,0x1D4DA),
    Binding('adjust_battle_losing_loyalty',0x1D4DA,0x1D542),
    Binding('apply_returning_officer_loyalty',0x208CE,0x20930),
    Binding('append_group_from_survivor_roster',0x21514,0x2159E),
    Binding('choose_empty_neighbor_position',0x21EFE,0x21F82),
)
REUSED_BINDINGS=(Binding('random_sample',0x83D4,0x83FA),Binding('terrain_cell_query',0x142A2,0x142CA))
NEW_BINDINGS=tuple(sorted(DISPOSITION_BINDINGS+MEMBERS_BINDINGS+ARRIVAL_BINDINGS,key=lambda b:b.entry))
BINDINGS=tuple(sorted(NEW_BINDINGS+REUSED_BINDINGS,key=lambda b:b.entry))
BY_NAME={b.name:b for b in BINDINGS}
TABLE_BINDINGS={name:dict(address=base,suffix='w' if base>=0xFFFF8000 else 'l') for name,base in VIEW_BASES.items()}
SCALAR_BINDINGS={name:dict(address=address,width=size*8,suffix='w' if address>=0xFFFF8000 else 'l') for name,(address,size) in SCALARS.items()}


def validate_binding(value):
    if (type(value) is not Binding or type(value.name) is not str or type(value.entry) is not int
        or type(value.end) is not int or type(value.completion) is not str or value not in BINDINGS):
        raise ValueError('strict admitted army-group target Binding required')
