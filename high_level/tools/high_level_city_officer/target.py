"""Original extent/ABI bindings and named live-data addresses; no opcode payload."""
from dataclasses import dataclass
from .domain import VIEW_BASES,SCALARS


@dataclass(frozen=True)
class Binding:
    name: str
    entry: int
    end: int
    completion: str='return'


CITY_BINDINGS=(
    Binding('commit_tax_rate',0xE57C,0xE592),
    Binding('schedule_transport_debit',0xE7B0,0xE822),
    Binding('commit_equipment_purchase',0xFC16,0xFC80),
    Binding('add_packet_city_resources',0x156B0,0x1571C),
    Binding('add_packet_city_resources_wrapped',0x158D4,0x15942),
    Binding('snapshot_city_resources',0x18FFC,0x19018),
    Binding('classify_city_resources',0x32404,0x3244A),
    Binding('commit_mutual_relationship',0xEC16,0xEC5C),
    Binding('transport_direction_or_arrival',0x16874,0x16922),
    Binding('transport_collision',0x16946,0x169AA),
    Binding('load_city_ed84_ee24_longs',0x19018,0x19034),
    Binding('commit_relationship_resource_credit',0x318AC,0x3191E),
    Binding('debit_city_gold',0xE70A,0xE71E),
    Binding('add_selected_cost',0x12A0C,0x12A2E),
)
OFFICER_BINDINGS=(
    Binding('scan_city_officers',0x11186,0x111A6),
    Binding('mark_c300_list',0x11546,0x11564),
    Binding('replace_city_assignments',0x11588,0x115BC),
    Binding('defense_progress',0x11C8C,0x11CCA),
    Binding('battle_progress_award',0x18A2E,0x18A54),
    Binding('replenish_b200_troops',0x16BB8,0x16C0A),
    Binding('grow_original_long_field',0x16C0A,0x16C2C),
    Binding('education_factor',0xE71E,0xE776),
    Binding('recover_unacted_officer_b200',0xE82E,0xE8A0),
    Binding('add_progress_be',0xEF60,0xEF80),
    Binding('split_progress',0xF990,0xF9D0),
    Binding('add_progress_c000',0xFDD0,0xFDEA),
    Binding('owner_head_lookup',0xFDEA,0xFE06),
    Binding('clear_city_orders',0x11564,0x11588),
    Binding('clear_monthly_actions',0x11CCA,0x11CF2),
    Binding('terrain_cell_query',0x142A2,0x142CA),
    Binding('queue_development_order',0xE0EE,0xE134),
    Binding('queue_welfare_order',0xE3FA,0xE440),
)
ROSTER_BINDINGS=(
    Binding('initialize_recruitment_pool',0x2A64,0x2A72),
    Binding('commit_recruitment',0xFBF4,0xFC16),
    Binding('settlement_progress',0x189D4,0x18A2E),
    Binding('remove_battle_roster',0x18A54,0x18A94),
    Binding('apply_battle_roster_outcome',0x18A94,0x18AC6),
    Binding('transfer_battle_roster',0x18AC6,0x18B00),
    Binding('remove_original_selected_roster',0x18C88,0x18CB4),
    Binding('assemble_defender_city_roster',0x18F18,0x18F66),
    Binding('initialize_prebattle_head_bytes',0x1D57A,0x1D598),
    Binding('clear_battle_assignment_state',0x1E85A,0x1E89C),
    Binding('copy_defender_roster_without_head',0x1ED78,0x1ED9A),
    Binding('ai_recruitment_capacity_gate',0x33790,0x337C6),
    Binding('distribute_existing_troop_pool',0x337C6,0x3382E),
    Binding('buy_and_distribute_troops',0x3382E,0x338BA),
)
NEW_BINDINGS=BINDINGS=tuple(sorted(CITY_BINDINGS+OFFICER_BINDINGS+ROSTER_BINDINGS,key=lambda b:b.entry))
BY_NAME={b.name:b for b in BINDINGS}
TABLE_BINDINGS={name:dict(address=base,suffix='w' if base>=0xFFFF8000 else 'l') for name,base in VIEW_BASES.items()}
SCALAR_BINDINGS={name:dict(address=address,width=size*8,suffix='w' if address>=0xFFFF8000 else 'l') for name,(address,size) in SCALARS.items()}


def validate_binding(value):
    if (type(value) is not Binding or type(value.name) is not str or type(value.entry) is not int
            or type(value.end) is not int or type(value.completion) is not str or value not in BINDINGS):
        raise ValueError('strict admitted city/officer target Binding required')
