"""Original ABI/extent and data bindings only, never encoded instruction payload."""
from dataclasses import dataclass
from .domain import VIEW_BASES, SCALARS


@dataclass(frozen=True)
class Binding:
    name: str
    entry: int
    end: int
    completion: str = 'return'


SELECTION_BINDINGS = (
    Binding('count_force_cities', 0x325E4, 0x325FC),
    Binding('select_force_by_city_count', 0x325FC, 0x32652),
)
POLICY_BINDINGS = (
    Binding('choose_attribute_neighbor_action', 0x32732, 0x32774),
    Binding('select_foreign_neighbor_attribute_max', 0x32774, 0x327CA),
    Binding('city_officer_attribute_max', 0x327CA, 0x32808),
    Binding('choose_player_neighbor_action', 0x32808, 0x32822),
    Binding('neighbor_has_player_owner', 0x32822, 0x32868),
    Binding('choose_resource_neighbor_action', 0x32868, 0x328D8),
    Binding('select_player_neighbor_resource_sum', 0x328D8, 0x32936),
)
OFFICER_BINDINGS = (
    Binding('select_roster_attribute_max', 0x32A3A, 0x32A68),
    Binding('select_foreign_nonruler_attribute_sum', 0x32A68, 0x32AB8),
    Binding('scan_nonruler_city_attribute_sum', 0x32AB8, 0x32B10),
    Binding('selected_city_has_player_owner', 0x32B10, 0x32B42),
    Binding('selected_player_officer_removed_gate', 0x32B42, 0x32B88),
    Binding('select_player_neighbor_head_attribute_min', 0x32C40, 0x32CA8),
    Binding('select_and_mark_roster_attribute_max', 0x32D72, 0x32DCE),
    Binding('select_roster_attribute_max_preserving_id', 0x32E72, 0x32EA0),
)
COMMIT_BINDINGS = (
    Binding('mark_selected_roster_bit14', 0x320A0, 0x320C0),
    Binding('commit_roster_city_assignments', 0x320C0, 0x320D4),
    Binding('choose_city_head_from_roster', 0x320D4, 0x3213E),
    Binding('flag_roster_b600_candidate', 0x3213E, 0x32192),
    Binding('update_roster_c700_status', 0x32192, 0x32210),
    Binding('commit_city_field_order', 0x3346A, 0x334CA),
    Binding('select_order_officer_b600', 0x334CA, 0x334F8),
    Binding('prepare_city_order_amount', 0x334F8, 0x33524),
    Binding('commit_officer_training', 0x33524, 0x33574),
    Binding('select_training_officer_c500', 0x33574, 0x335AE),
    Binding('prepare_officer_training_cost', 0x335AE, 0x335C8),
    Binding('apply_officer_training_growth', 0x335C8, 0x3363C),
)
REUSED_BINDINGS = (
    Binding('random_sample', 0x83D4, 0x83FA),
    Binding('signed_divmod', 0x35760, 0x3576C),
    Binding('positive_denominator', 0x3576C, 0x3577A),
    Binding('unsigned_divmod', 0x3577A, 0x357DA),
    Binding('word_pair_divmod', 0x357DA, 0x357F8),
)
NEW_BINDINGS = tuple(sorted(SELECTION_BINDINGS+POLICY_BINDINGS+OFFICER_BINDINGS+COMMIT_BINDINGS, key=lambda b:b.entry))
BINDINGS = tuple(sorted(NEW_BINDINGS+REUSED_BINDINGS, key=lambda b:b.entry))
BY_NAME = {b.name:b for b in BINDINGS}
TABLE_BINDINGS = {name:dict(address=base, suffix='w' if base>=0xFFFF8000 else 'l') for name,base in VIEW_BASES.items()}
SCALAR_BINDINGS = {name:dict(address=address,width=size*8,suffix='w') for name,(address,size) in SCALARS.items()}


def validate_binding(value):
    if (type(value) is not Binding or type(value.name) is not str or type(value.entry) is not int
            or type(value.end) is not int or type(value.completion) is not str or value not in BINDINGS):
        raise ValueError('strict explicit AI target Binding required')
