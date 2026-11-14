"""Complete original extents and compatibility data/ABI, with no code payload."""
from dataclasses import dataclass
from .domain import VIEW_BASES,SCALARS


@dataclass(frozen=True)
class Binding:
    name:str
    entry:int
    end:int
    completion:str='return'


SHARED_BINDINGS=(
    Binding('choose_city_head',0xE1F6,0xE26C),
    Binding('roster_contains_force_head_carry',0xE26C,0xE29E),
    Binding('prepare_message',0x676F2,0x67728),
    Binding('select_message_layout',0x67728,0x6773C),
    Binding('resolve_message_pointer',0x679D2,0x679FC),
)
STRATAGEM_BINDINGS=(
    Binding('replace_removed_force_head',0xE29E,0xE38E),
    Binding('mark_removed_force_assignments',0xE38E,0xE3E2),
    Binding('clear_removed_force_roster_alias',0xE3E2,0xE3F8),
    Binding('settle_method61_stratagem',0xF018,0xF02C),
    Binding('assess_method61_side',0xF02C,0xF088),
    Binding('settle_method61_resource_attempt',0xF088,0xF18E),
    Binding('settle_method61_direct_attempt',0xF18E,0xF232),
    Binding('method61_scenario_factor',0xF232,0xF28E),
    Binding('penalize_actor_small_affinity',0xF28E,0xF2CE),
    Binding('penalize_force_small_affinity',0xF2CE,0xF314),
    Binding('reward_actor_small_c_progress',0xF314,0xF34C),
    Binding('remove_stratagem_target',0xF34C,0xF388),
    Binding('penalize_actor_large_affinity',0xF388,0xF3C6),
    Binding('penalize_force_large_affinity',0xF3C6,0xF40A),
    Binding('settle_removed_force_head',0xF40A,0xF4E6),
    Binding('remove_city_head_target',0xF4E6,0xF50C),
    Binding('reassign_or_mark_target',0xF50C,0xF574),
    Binding('try_remove_secondary_target',0xF574,0xF5B6),
    Binding('remove_secondary_city_head',0xF5B6,0xF5F6),
    Binding('reward_actor_large_c_progress',0xF5F6,0xF630),
    Binding('choose_secondary_stratagem_target',0xF630,0xF6AE),
    Binding('method61_direct_probability',0xF6AE,0xF71C),
    Binding('method61_direct_factor',0xF71C,0xF778),
)
PERSONNEL_BINDINGS=(
    Binding('settle_personnel_joining',0x111AC,0x111C0),
    Binding('settle_bribe_joining',0x111C0,0x11312),
    Binding('bribe_acceptance_factor',0x11312,0x11380),
    Binding('penalize_force_head_affinity',0x113BC,0x113F6),
    Binding('reward_force_head_small_progress',0x113F6,0x1142E),
    Binding('reward_force_head_large_progress',0x1142E,0x11466),
    Binding('transfer_joining_officer',0x11466,0x11546),
    Binding('settle_persuasion_joining',0x1161A,0x1173A),
    Binding('persuasion_scores',0x1173A,0x117F0),
    Binding('persuasion_factor',0x117F0,0x11842),
    Binding('reward_actor_small_progress',0x11874,0x118A2),
    Binding('reward_actor_large_progress',0x118A2,0x118D4),
    Binding('penalize_actor_affinity',0x118D4,0x1190E),
)
FORCES_BINDINGS=(
    Binding('resolve_force_reassignment',0x66616,0x66724),
    Binding('reassign_city_officers',0x66724,0x6679E),
    Binding('clear_transferred_city_orders',0x6679E,0x667F6),
    Binding('remove_force_group_packets',0x667F6,0x6683E),
    Binding('compact_following_packets',0x6689E,0x668BE),
    Binding('remove_packet_pair_reference',0x668BE,0x668FC),
    Binding('reduce_city_reserve',0x668FC,0x6694C),
    Binding('return_temporary_city_assignments',0x6694C,0x669D0),
    Binding('remove_officer_pair_reference',0x669D0,0x669FE),
    Binding('mark_city_assignments_inactive',0x669FE,0x66A22),
    Binding('disband_force_group_packets',0x66A22,0x66A9E),
    Binding('remove_disbanded_packet_reference',0x66A9E,0x66AD8),
    Binding('clear_disbanded_temporary_assignments',0x66AD8,0x66B54),
    Binding('clear_disbanded_city_orders',0x66B54,0x66BB0),
    Binding('clear_city_queue_principals',0x66BB0,0x66BF4),
)
REUSED_BINDINGS=(
    Binding('build_roster',0x5F48,0x5F7C),Binding('step_random',0x83D4,0x83FA),
    Binding('owner_head_lookup',0xFDEA,0xFE06),Binding('mark_c300_list',0x11546,0x11564),
    Binding('clear_city_orders',0x11564,0x11588),Binding('replace_city_assignments',0x11588,0x115BC),
    Binding('clear_selected_links',0x115BC,0x1161A),
    Binding('apply_returning_officer_loyalty',0x208CE,0x20930),
)
NEW_BINDINGS=tuple(sorted(SHARED_BINDINGS+STRATAGEM_BINDINGS+PERSONNEL_BINDINGS+FORCES_BINDINGS,key=lambda b:b.entry))
BINDINGS=tuple(sorted(NEW_BINDINGS+REUSED_BINDINGS,key=lambda b:b.entry))
BY_NAME={b.name:b for b in BINDINGS}
TABLE_BINDINGS={n:dict(address=a,suffix='w' if a>=0xFFFF8000 else 'l') for n,a in VIEW_BASES.items()}
SCALAR_BINDINGS={n:dict(address=a,width=s*8,suffix='w' if a>=0xFFFF8000 else 'l') for n,(a,s) in SCALARS.items()}


def validate_binding(value):
    if (type(value) is not Binding or type(value.name) is not str or type(value.entry) is not int
        or type(value.end) is not int or type(value.completion) is not str or value not in BINDINGS):
        raise ValueError('strict diplomacy/force complete target Binding required')
