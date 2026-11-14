"""Original complete extents and fixed compatibility ABI, never code bytes."""
from dataclasses import dataclass
from .domain import VIEW_BASES,SCALARS
@dataclass(frozen=True)
class Binding:
    name:str
    entry:int
    end:int
    completion:str='return'
PATH_BINDINGS=(
 Binding('build_path',0x6518,0x6562),Binding('initialize_path_grid',0x6562,0x6624),
 Binding('normalize_path_coordinates',0x6624,0x664E),Binding('expand_path_frontier',0x664E,0x66C2),
 Binding('visit_path_neighbor',0x66C2,0x66EE),Binding('path_neighbor_is_goal',0x66EE,0x670A),
 Binding('mark_path_direction',0x6710,0x672C),Binding('read_path_direction',0x672C,0x6748),
 Binding('read_path_cost',0x6748,0x6764),Binding('reconstruct_path',0x6764,0x678E),
 Binding('step_back_path',0x678E,0x67B4),
)
ARRIVAL_BINDINGS=(
 Binding('hostile_adjacent_block',0x15384,0x154C8),Binding('collect_blocked_cargo',0x154C8,0x15572),
 Binding('settle_arriving_group',0x15572,0x156B0),Binding('assign_packet_members',0x1571C,0x15758),
 Binding('compact_after_packet',0x15758,0x1577A),Binding('initialize_arrival_loyalty',0x1577A,0x157C0),
 Binding('clear_arrival_city_order',0x157C0,0x157D8),Binding('merge_overcapacity_arrival',0x157D8,0x157F4),
 Binding('build_packet_member_roster',0x157F4,0x15814),Binding('extract_force_head_from_roster',0x15814,0x15858),
 Binding('sort_packet_roster_by_status',0x15858,0x158A0),Binding('assign_ranked_packet_members',0x158A0,0x158D4),
 Binding('compact_arrival_packet',0x15942,0x1596C),Binding('detach_packet_force_head',0x1596C,0x159EA),
 Binding('locate_arrival_city',0x164D4,0x16588),
)
CAMPAIGN_BINDINGS=(
 Binding('prepare_transport_path',0x16ACC,0x16B3A),Binding('ensure_neighbor_capacity',0x17C8A,0x17D10),
 Binding('find_group_at_coordinate',0x17D10,0x17D3C),Binding('collect_six_neighbor_candidates',0x17D3C,0x17DDC),
 Binding('filter_neighbor_candidates',0x17DDC,0x17E3C),Binding('selected_roster_capacity',0x17E3C,0x17EBA),
 Binding('read_neighbor_source_cost',0x17EBA,0x17EDE),Binding('build_ai_movement_packet',0x33CC8,0x33D0E),
 Binding('append_ai_path_steps',0x33D0E,0x33D6C),Binding('read_path_step_cost',0x33D7C,0x33D92),
 Binding('choose_ai_destination',0x341CE,0x34280),Binding('city_roster_full_carry',0x34280,0x342BE),
)
REUSED_BINDINGS=(Binding('build_roster',0x5F48,0x5F7C),Binding('step_random',0x83D4,0x83FA),
 Binding('choose_city_head',0xE1F6,0xE26C),Binding('roster_contains_force_head_carry',0xE26C,0xE29E),
 Binding('add_packet_city_resources',0x156B0,0x1571C),Binding('add_packet_city_resources_wrapped',0x158D4,0x15942))
NEW_BINDINGS=tuple(sorted(PATH_BINDINGS+ARRIVAL_BINDINGS+CAMPAIGN_BINDINGS,key=lambda b:b.entry))
BINDINGS=tuple(sorted(NEW_BINDINGS+REUSED_BINDINGS,key=lambda b:b.entry))
BY_NAME={b.name:b for b in BINDINGS}
TABLE_BINDINGS={n:dict(address=a,suffix='w' if a>=0xFFFF8000 else 'l') for n,a in VIEW_BASES.items()}
SCALAR_BINDINGS={n:dict(address=a,width=s*8,suffix='w' if a>=0xFFFF8000 else 'l') for n,(a,s) in SCALARS.items()}
ALTERNATE_ENTRY=0x651C
def validate_binding(value):
    if type(value) is not Binding or type(value.name) is not str or type(value.entry) is not int or type(value.end) is not int or type(value.completion) is not str or value not in BINDINGS:
        raise ValueError('strict movement complete Binding required')
