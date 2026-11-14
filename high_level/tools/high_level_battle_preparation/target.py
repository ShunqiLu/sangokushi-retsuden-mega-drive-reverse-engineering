"""Typed target ABI/allocations and data locations, with no encoded code."""
from dataclasses import dataclass
from .domain import VIEW_BASES, SCALARS


@dataclass(frozen=True)
class Binding:
    name: str
    entry: int
    end: int
    completion: str = 'return'


SELECTION_BINDINGS = (
    Binding('selected_attribute_average', 0x101F8, 0x10224),
    Binding('count_selected_deployment', 0x1B262, 0x1B27A),
    Binding('initialize_selected_assignment', 0x1B27A, 0x1B2BC),
    Binding('selected_troop_weights', 0x1B40E, 0x1B448),
    Binding('refresh_object_attribute_average', 0x1B4EA, 0x1B512),
    Binding('submit_deployment_queue', 0x1B512, 0x1B578),
    Binding('clear_original_tail_coordinate', 0x1B578, 0x1B59E),
    Binding('compact_active_deployment_queue', 0x1B8AC, 0x1B90C),
    Binding('deployment_force_carry', 0x1B90C, 0x1B968),
)
DESCRIPTOR_BINDINGS = (
    Binding('prepare_both_battle_sides', 0x1B6C2, 0x1B7A2),
    Binding('prepare_battle_mode_header', 0x1B7A2, 0x1B832),
    Binding('prepare_battle_terrain', 0x1B850, 0x1B890),
    Binding('choose_battle_order', 0x1B896, 0x1B8AC),
    Binding('maximum_three_live_lookup_attributes', 0x1F8D4, 0x1F910),
)
RESULT_BINDINGS = (
    Binding('decrement_battle_3cc2_counters', 0x1F13C, 0x1F156),
    Binding('decrement_battle_status_counters', 0x1FAA8, 0x1FAEC),
    Binding('select_battle_outcome_side', 0x1FB12, 0x1FB66),
    Binding('adjust_battle_pair_spacing', 0x1FBD4, 0x1FC50),
    Binding('battle_pair_removed_carry', 0x1FC50, 0x1FC7E),
    Binding('selected_battle_roster_carry', 0x1FC7E, 0x1FCAA),
)
BINDINGS = tuple(sorted(SELECTION_BINDINGS + DESCRIPTOR_BINDINGS + RESULT_BINDINGS, key=lambda b:b.entry))
BY_NAME = {b.name:b for b in BINDINGS}
TABLE_BINDINGS = {name:dict(address=base, suffix='w' if base>=0xFFFF8000 else 'l') for name,base in VIEW_BASES.items()}
SCALAR_BINDINGS = {name:dict(address=address, width=size*8,
    suffix='w' if name in ('city_word','city_tail','state_mode','command_step','tail_city','object_index','active_force_1','active_force_2','active_force_3','attacker_officer','defender_officer','first_officer','second_officer','first_force','second_force','outcome_mode','outcome_side') else 'l') for name,(address,size) in SCALARS.items()}
REGISTERS = {
    'selected_attribute_average':dict(divisor='d0',total='d2',roster_member='d3',attribute='d4',attributes='a2',roster='a3'),
    'count_selected_deployment':dict(member='d0',count='d7',roster='a1'),
    'initialize_selected_assignment':dict(object_view='a0',member='d0',force='d0',city='d1',assignments='a1',roster='a2',owners='a3',coordinates='a4'),
    'selected_troop_weights':dict(member='d2',index='d3',selected='d5',all_members='d6',roster='a1',weights='a2'),
    'refresh_object_attribute_average':dict(object_view='a0',divisor='d0',index='d1',total='d2',member='d3',attributes='a1'),
    'submit_deployment_queue':dict(object_view='a0',city='d0',officer='d0',flags='a1',queue='a1'),
    'clear_original_tail_coordinate':dict(city='d0',index='d1',coordinate_index='d2',assignments='a0',coordinates='a1'),
    'compact_active_deployment_queue':dict(member='d0',index='d0',objects='a0',object_view='a0',queue='a0',offsets='a1'),
    'deployment_force_carry':dict(force='d0',index='d0',object_view='a0',objects='a0',offsets='a1'),
    'prepare_battle_mode_header':dict(assignments='a0',owners='a1',unused_count='d7',selected='d0',first_city='d1',first_force='d1',second_city='d2',second_force='d2',mode_index='d3'),
    'prepare_battle_terrain':dict(objects='a0',offsets='a1',object_index='d0',object_view='a0',row='d0',column='d1',cell='d0',terrain='d1',cells='a0',parameters='a0'),
    'choose_battle_order':dict(first='d0',second='d7'),
    'maximum_three_live_lookup_attributes':dict(officer='d0',index='d1',attributes='a5',weights='a6',maximum='d3',selector='d2'),
    'prepare_both_battle_sides':dict(first='d0',second='d7',selected='d0',offset='d0',assignments='a0',owners='a1',leaders='a2',owner='d1',capacities='a0',side_attributes='a1',ratio_attributes='a2',troops='a3',awards='a4',attributes='a5'),
}
PRESERVED = {'submit_deployment_queue':('a0',)}


def validate_binding(value):
    if (type(value) is not Binding or type(value.name) is not str or type(value.entry) is not int
            or type(value.end) is not int or type(value.completion) is not str or value not in BINDINGS):
        raise ValueError('strict explicit preparation ABI binding required')
