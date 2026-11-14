"""Explicit live AI policy DATA; no ROM loader, implicit assets or CPU state.

RAM and readonly segments are supplied by the caller. Signed WORD effective
addresses and partial-width arithmetic are compatibility, not editor clamps.
"""
from dataclasses import dataclass
from typing import NewType

Byte=NewType('Byte',int)
Word=NewType('Word',int)
Long=NewType('Long',int)

class Boundary(ValueError): pass

def uint(value,bits,name='value'):
    if type(bits) is not int or bits not in (8,16,32) or type(value) is not int or not 0<=value<1<<bits:
        raise ValueError(f'strict {bits}-bit {name} required')
    return value
def u8(value):
    if type(value) is not int: raise ValueError('integer BYTE arithmetic required')
    return value&255
def u16(value):
    if type(value) is not int: raise ValueError('integer WORD arithmetic required')
    return value&65535
def u32(value):
    if type(value) is not int: raise ValueError('integer LONG arithmetic required')
    return value&0xFFFFFFFF
def s8(value):
    value=uint(value,8);return value-256 if value&128 else value
def s16(value):
    value=uint(value,16);return value-65536 if value&32768 else value
def low8(value): return u8(value)
def low16(value): return u16(value)
def high16(value): return uint(value,32)>>16
def replace_byte(value,byte): return (uint(value,32)&0xFFFFFF00)|uint(byte,8)
def replace_word(value,word): return (uint(value,32)&0xFFFF0000)|uint(word,16)
def swap_words(value):
    value=uint(value,32);return u32((value<<16)|(value>>16))
def negative_byte(value): return bool(uint(value,8)&128)
def negative_word(value): return bool(uint(value,16)&32768)
def negative_long(value): return bool(uint(value,32)&0x80000000)
def descending_inclusive(counter):
    uint(counter,16);yield from range(counter,-1,-1)
def divu_retained(numerator,denominator):
    uint(numerator,32);uint(denominator,16)
    if denominator==0: raise Boundary('original DIVU divide by zero after preceding DATA')
    q,r=divmod(numerator,denominator)
    return numerator if q>65535 else (r<<16)|q

@dataclass(frozen=True)
class CarryOutcome:
    carry:int
    conditional_sr:int
    def __post_init__(self):
        if type(self.carry) is not int or self.carry not in (0,1): raise ValueError('strict carry0/1 required')
        uint(self.conditional_sr,16)

@dataclass(frozen=True)
class BlockingMaskContext:
    """Explicit high WORD retained by the original blocking-mask ABI.

    Zero is a useful default conditional input, not a proof that the original
    caller cleared this WORD. This value is not RAM and contributes no DATA.
    """
    retained_high_word:Word=0
    def __post_init__(self):
        uint(self.retained_high_word,16,'retained blocking-mask high WORD')

@dataclass(frozen=True)
class HeadMatch:
    head:int
    carry:int
    conditional_sr:int
    def __post_init__(self):
        uint(self.head,16);CarryOutcome(self.carry,self.conditional_sr)

@dataclass(frozen=True)
class EquipmentScanContext:
    """Preserved equipment-level high BYTE; zero is only a conditional default."""
    retained_level_high_byte:Byte=0
    def __post_init__(self):
        uint(self.retained_level_high_byte,8,'retained equipment-level high BYTE')

@dataclass(frozen=True)
class NeighborSelectionContext:
    """Score lanes left untouched when no eligible neighbor is selected."""
    retained_first_score:Word=0
    retained_second_score:Word=0
    def __post_init__(self):
        uint(self.retained_first_score,16);uint(self.retained_second_score,16)

@dataclass(frozen=True)
class TroopPurchaseContext:
    """Budget operand surviving earlier helpers, not a fresh pool snapshot."""
    retained_budget:Long=0
    def __post_init__(self): uint(self.retained_budget,32)

@dataclass(frozen=True)
class ContactMaskContext:
    mask_high_word:Word=0
    def __post_init__(self): uint(self.mask_high_word,16)

@dataclass(frozen=True)
class RankingContext:
    strength_offset:Word
    tail:'Cursor'
    def __post_init__(self):
        uint(self.strength_offset,16);checked_cursor(self.tail)

@dataclass(frozen=True)
class CoordinateScratchContext:
    coordinate_high_word:Word=0
    def __post_init__(self): uint(self.coordinate_high_word,16)

@dataclass(frozen=True)
class PackedCountContext:
    count_high_byte:Byte=0
    def __post_init__(self): uint(self.count_high_byte,8)

@dataclass(frozen=True)
class CandidateSelectionContext:
    fallback_offset:Word=0
    def __post_init__(self): uint(self.fallback_offset,16)

@dataclass(frozen=True)
class RosterStrengthContext:
    last_strength:Long=0
    def __post_init__(self): uint(self.last_strength,32)

@dataclass(frozen=True)
class PathCoordinates:
    first:int
    second:int
    def __post_init__(self): uint(self.first,16);uint(self.second,16)

@dataclass(frozen=True)
class PathResult:
    length:int
    retained_direction:int
    final_coordinates:PathCoordinates
    final_frontier_cursor:'Cursor'
    final_grid:'Table'
    def __post_init__(self):
        uint(self.length,16);uint(self.retained_direction,16)
        if type(self.final_coordinates) is not PathCoordinates: raise ValueError('typed coordinates required')
        checked_cursor(self.final_frontier_cursor)
        checked_table(self.final_grid,self.final_frontier_cursor.state)

@dataclass(frozen=True)
class FrontierResult:
    carry:int
    retained_direction:int
    coordinates:PathCoordinates
    def __post_init__(self):
        if type(self.carry) is not int or self.carry not in (0,1): raise ValueError('strict carry required')
        uint(self.retained_direction,16)
        if type(self.coordinates) is not PathCoordinates: raise ValueError('typed coordinates required')

@dataclass(frozen=True)
class NeighborResult:
    carry:int
    conditional_sr:int
    coordinates:PathCoordinates
    def __post_init__(self):
        CarryOutcome(self.carry,self.conditional_sr)
        if type(self.coordinates) is not PathCoordinates: raise ValueError('typed coordinates required')

@dataclass(frozen=True)
class CityTroopSummary:
    total:Long
    qualifying_count:Word
    def __post_init__(self):
        uint(self.total,32);uint(self.qualifying_count,16)

@dataclass(frozen=True)
class NeighborRoute:
    length:Word
    city:Word
    def __post_init__(self):
        uint(self.length,16);uint(self.city,16)

class ReadOnlyData:
    def __init__(self,segments=()):
        if type(segments) is not tuple: raise ValueError('explicit readonly segment tuple required')
        rows=[]
        for item in segments:
            if type(item) is not tuple or len(item)!=2: raise ValueError('(base,bytes) required')
            base,raw=item;uint(base,32)
            if type(raw) is not bytes or not raw or base+len(raw)>0x1000000: raise ValueError('nonempty 24bit segment required')
            rows.append((base,raw))
        rows.sort()
        if any(a+len(raw)>b for (a,raw),(b,_) in zip(rows,rows[1:])): raise ValueError('competing readonly authorities')
        self.segments=tuple(rows)
    def read(self,address,size):
        uint(address,32)
        if type(size) is not int or size not in (1,2,4): raise ValueError('strict width required')
        for base,raw in self.segments:
            if base<=address and address+size<=base+len(raw): return int.from_bytes(raw[address-base:address-base+size],'big')
        raise Boundary('outside explicit readonly source')

VIEW_BASES={
 'city_owners_predecrement':0xFFFFF450,
 'combat_troops':0xFFFFB200,'officer_capacities':0xFFFFB000,
 'officer_attributes':0xFFFFB400,'officer_strengths':0xFFFFC800,
 'officer_progress':0xFFFFBE00,'officer_action_predecrement':0xFFFFCD00,
 'officer_assignments_end':0xFFFFCD00,'officer_city_links':0xFFFFA050,
 'officer_city_links_end':0xFFFFA150,'following_city_owners':0xFFFFF428,
 'city_owners_end':0xFFFFF450,'action_candidates':0xFFFFD300,
 'ranked_members':0xFFFFD320,'ranked_strengths':0xFFFFD340,
 'ranked_attributes':0xFFFFD360,'candidate_distances':0xFFFFD400,
 'candidate_distances_prefix':0xFFFFD3FE,'selected_roster':0xFFFFF72A,
 'contact_city_coordinates':0x000D4B66,'equipment_cost':0x0000D2EA,
 'route_roster':0xFFFFF72A,'remaining_roster':0xFFFFF72E,
 'officer_city':0xFFFFCC00,'officer_actions':0xFFFFCD00,
 'officer_loyalty':0xFFFFB000,'officer_loyalty_limit':0xFFFFB200,
 'officer_strength':0xFFFFB400,'officer_march_speed':0xFFFFC400,
 'city_food':0xFFFFE09C,'city_owner':0xFFFFF427,'city_owner_zero_based':0xFFFFF428,
 'officer_packet_data':0xFFFFA050,'city_coordinates_zero_based':0x000D4ACA,
 'city_neighbors':0x000D4BDA,'terrain_types':0x000EE5F0,'route_commands':0x00FF3000,
 'ai_roster':0xFFFFF72A,'capacities':0xFFFFB800,
 'recruitment_pools':0xFFFFE774,'balances':0xFFFFDFFC,
 'economy_roster':0xFFFFF72A,'officer_intelligence':0xFFFFB600,
 'officer_primary_attribute':0xFFFFB400,'officer_education':0xFFFFC200,
 'officer_training':0xFFFFC500,'officer_troops':0xFFFFC800,
 'city_welfare':0xFFFFE31C,'city_defense_targets':0xFFFFE3BC,
 'officer_action':0xFFFFCD00,'force_summary':0x311FC,
 'equipment_work':0xFFFFD300,'equipment_categories':0x33764,
 'officer_equipment':0xFFFFEA88,'equipment_prices':0xD2CA,
 'roster':0xFFFFF72A,'officer_roster':0xFFFFF72A,'support_roster':0xFFFFF500,
 'scratch_roster':0xFFFFD300,'troops':0xFFFFC800,'c800':0xFFFFC800,
 'b600':0xFFFFB600,'attributes_b600':0xFFFFB600,'b400':0xFFFFB400,'attributes_b400':0xFFFFB400,
 'c300':0xFFFFC300,'c000':0xFFFFC000,'c500':0xFFFFC500,'c600':0xFFFFC600,'c700':0xFFFFC700,'be00':0xFFFFBE00,
 'officer_flags':0xFFFFC700,'officer_action_flags':0xFFFFCD00,'city_assignments':0xFFFFCD00,
 'force_city_assignments':0xFFFFF428,'force_leaders':0xFFFFE640,'force_rows':0x32660,
 'neighbors':0xD4BDA,'neighbor_lists':0xD4BDA,'coordinate_candidates':0xD4D22,
 'city_balances':0xFFFFDFFC,'order_gates':0xFFFFE59C,

 'path_grid':0xFF0000,'path_frontier':0xFF4000,'alternate_frontier':0xFF4800,
 'terrain_sources':0xEE5F0,'terrain_costs':0x670A,'city_coordinates':0xD4AC6,'following_city_coordinates':0xD4ACA,
 'transport_records':0xFFFFCE00,'city_grid':0xFFFFCE9C,
 'group_packets':0xFFFF9000,'packed_groups':0xFFFF9000,
 'neighbor_candidates':0xFFFFA954,'neighbor_candidates_prefix':0xFFFFA952,
 'neighbor_selected_slots':0xFFFFF6E8,'neighbor_source_pointers':0x17C7A,
 'group_step_vectors':0x33D68,'world_path_steps':0xFF4000,'movement_queue':0xFF3000,
 'city_owner_slots':0xFFFFF428,'city_owners_reverse':0xFFFFF450,'city_owners':0xFFFFF427,
 'officer_assignments':0xFFFFCC00,'neighbor_city_flags':0xFFFFA027,
 'city_heads':0xFFFFF45E,'force_heads':0xFFFFE640,
 'primary_roster':0xFFFFA550,'secondary_roster':0xFFFFA57A,
 'city_primary_roster':0xFFFFA5A4,'city_secondary_roster':0xFFFFA5CE,
 'force_masks':0xFFFFE710,'loyalty':0xFFFFC200,'reserves':0xFFFFE320,
 'selected_orders':0xFFFFE774,'member_roster':0xFFFFD300,
 'ranked_roster':0xFFFFD316,'ranked_status':0xFFFFD32C,'officer_status':0xFFFFC300,
 'candidate_roster':0xFFFFF500,'city_orders':0xFFFFE80C,
 'city_gold':0xFFFFDFFC,'city_rice':0xFFFFE09C,
 'city_processed':0xFFFFEA37,'city_reserves':0xFFFFE320,
}
SCALARS={
 'current_force_low':(0xFFFFF377,1),'ai_strength':(0xFFFFF744,4),
 'ai_ready_count':(0xFFFFF748,2),'ai_selected_offset':(0xFFFFF748,2),
 'ai_packet_marker_word':(0xFFFFF74A,2),'ai_grid_x':(0xFFFFF75C,2),'ai_grid_y':(0xFFFFF75E,2),
 'selected_count':(0xFFFFF636,2),'dialogue_selection':(0xFFFFEFBE,2),
 'dialogue_auxiliary':(0xFFFFEFC6,2),'dialogue_kind':(0xFFFFF65A,2),
 'menu_record':(0xFFFFF38C,2),'dialogue_pending':(0xFFFFF576,2),
 'current_force_byte':(0xFFFFF377,1),'target_city':(0xFFFFF392,2),
 'selected_gold_budget':(0xFFFFF39E,4),'march_supply_budget':(0xFFFFF3BA,4),
 'roster_head':(0xFFFFF630,2),'path_start_first':(0xFFFFF63C,2),'path_start_second':(0xFFFFF63E,2),
 'path_goal_first':(0xFFFFF640,2),'path_goal_second':(0xFFFFF642,2),
 'phase_argument':(0xFFFFF744,2),'phase_argument_byte':(0xFFFFF745,1),
 'packed_first':(0xFFFFF746,2),'packed_first_byte':(0xFFFFF747,1),
 'packed_second':(0xFFFFF748,2),'packed_second_byte':(0xFFFFF749,1),
 'packed_head':(0xFFFFF74A,2),'packed_head_byte':(0xFFFFF74B,1),'action_phase':(0xFFFFF728,2),
 'first_candidate_officer':(0xFFFFF72A,2),'first_candidate_officer_byte':(0xFFFFF72B,1),
 'second_candidate_officer':(0xFFFFF72C,2),'second_candidate_officer_byte':(0xFFFFF72D,1),
 'packed_group_offset':(0xFFFFF75A,2),'transport_first':(0xFFFFF75C,2),'transport_second':(0xFFFFF75E,2),
 'transport_route_budget':(0xFFFFF760,2),'roster_count':(0xFFFFF762,2),'route_command_offset':(0x00FF3826,2),
 'candidate_officer':(0xFFFFF3F2,2),'support_city':(0xFFFFE730,2),'support_amount':(0xFFFFF3E0,2),
 'force_selector':(0xFFFFF376,2),'force_id':(0xFFFFF376,2),
 'command':(0xFFFFF728,2),'next_state':(0xFFFFF728,2),
 'order_amount':(0xFFFFF39E,4),'action_amount':(0xFFFFF39E,4),'roster_second':(0xFFFFF72C,2),
 'seed_word':(0xFFFFF61C,2),'seed_high_word':(0xFFFFF61C,2),'seed_low_byte':(0xFFFFF61D,1),

 'path_origin_x':(0xFFFFF63C,2),'path_origin_y':(0xFFFFF63E,2),
 'path_target_x':(0xFFFFF640,2),'path_target_y':(0xFFFFF642,2),
 'path_destination_first':(0xFFFFF63C,2),'path_destination_second':(0xFFFFF63E,2),
 'path_source_first':(0xFFFFF640,2),'path_source_second':(0xFFFFF642,2),
 'path_source_first_tail':(0xFFFFF641,1),'path_source_second_tail':(0xFFFFF643,1),'path_length':(0xFFFFF644,2),
 'transport_index':(0xFFFFCEA0,2),'transport_budget':(0xFFFFCEA2,2),'transport_progress':(0xFFFFCEAC,2),
 'neighbor_mode':(0xFFFFF6D6,2),'neighbor_mode_low':(0xFFFFF6D7,1),'neighbor_city':(0xFFFFF68A,2),
 'selected_officer':(0xFFFFF3A6,2),'chosen_city':(0xFFFFF392,2),'selected_city':(0xFFFFF3A8,2),
 'current_force':(0xFFFFF376,2),'force':(0xFFFFF376,2),'force_tail':(0xFFFFF377,1),
 'ai_group_index':(0xFFFFF75A,2),'ai_origin_x':(0xFFFFF746,2),'ai_origin_y':(0xFFFFF748,2),
 'ai_budget':(0xFFFFF744,2),'ai_budget_low':(0xFFFFF745,1),'ai_packet_marker':(0xFFFFF74B,1),
 'movement_queue_offset':(0xFF3826,2),'active_packet':(0xFF382C,4),
 'position_x':(0xFF3BB6,2),'position_y':(0xFF3BB8,2),'blocking_owner':(0xFF3BBE,2),
 'blocking_owner_tail':(0xFF3BBF,1),'blocking_mask':(0xFF3BC0,2),
 'current_city':(0xFFFFF364,2),'roster_exclusion':(0xFFFFF630,2),'head':(0xFFFFF630,2),
 'remaining_count':(0xFFFFF686,2),'command_step':(0xFFFFF362,2),
 'player_force_1':(0xFFFFF67B,1),'player_force_2':(0xFFFFF67D,1),'player_force_3':(0xFFFFF67F,1),
 'player_force_word_1':(0xFFFFF67A,2),'player_force_word_2':(0xFFFFF67C,2),'player_force_word_3':(0xFFFFF67E,2),
 'player_1_tail':(0xFFFFF67B,1),'player_2_tail':(0xFFFFF67D,1),'player_3_tail':(0xFFFFF67F,1),
 'processed':(0xFFFFEA37,1),
 'route':(0xFFFFF612,2),'stage':(0xFFFFF362,2),
 'remaining_members':(0xFFFFF686,2),'current_force_tail':(0xFFFFF377,1),
}

class GameState:
    def __init__(self,ram,*,data=None,max_reads=1000000,sr=0x2700,blocking_mask_context=None,equipment_scan_context=None,neighbor_selection_context=None,troop_purchase_context=None):
        if type(ram) is not bytearray or len(ram)!=65536: raise ValueError('explicit live64KiB RAM required')
        if blocking_mask_context is None: blocking_mask_context=BlockingMaskContext()
        if type(blocking_mask_context) is not BlockingMaskContext:
            raise ValueError('typed immutable BlockingMaskContext required')
        uint(blocking_mask_context.retained_high_word,16,'retained blocking-mask high WORD')
        if equipment_scan_context is None: equipment_scan_context=EquipmentScanContext()
        if type(equipment_scan_context) is not EquipmentScanContext:
            raise ValueError('typed immutable EquipmentScanContext required')
        uint(equipment_scan_context.retained_level_high_byte,8,'retained equipment-level high BYTE')
        if neighbor_selection_context is None: neighbor_selection_context=NeighborSelectionContext()
        if type(neighbor_selection_context) is not NeighborSelectionContext:
            raise ValueError('typed immutable NeighborSelectionContext required')
        uint(neighbor_selection_context.retained_first_score,16)
        uint(neighbor_selection_context.retained_second_score,16)
        if troop_purchase_context is None: troop_purchase_context=TroopPurchaseContext()
        if type(troop_purchase_context) is not TroopPurchaseContext:
            raise ValueError('typed immutable TroopPurchaseContext required')
        uint(troop_purchase_context.retained_budget,32)
        if data is None: data=ReadOnlyData()
        if type(data) is not ReadOnlyData: raise ValueError('typed readonly DATA required')
        uint(max_reads,32);uint(sr,16)
        if max_reads==0: raise ValueError('positive DATA budget required')
        self.ram,self.data,self.max_reads,self.sr=ram,data,max_reads,sr
        self._blocking_mask_context=blocking_mask_context
        self._equipment_scan_context=equipment_scan_context
        self._neighbor_selection_context=neighbor_selection_context
        self._troop_purchase_context=troop_purchase_context
        self.reads,self.events=0,[]
    @property
    def blocking_mask_context(self): return self._blocking_mask_context
    @property
    def equipment_scan_context(self): return self._equipment_scan_context
    @property
    def neighbor_selection_context(self): return self._neighbor_selection_context
    @property
    def troop_purchase_context(self): return self._troop_purchase_context
    def effective_blocking_mask(self,low_word:Word)->Long:
        """Combine an explicit preserved prefix with the freshly read low WORD."""
        low_word=uint(low_word,16,'live blocking-mask low WORD')
        high_word=uint(self.blocking_mask_context.retained_high_word,16,'retained blocking-mask high WORD')
        return Long((high_word<<16)|low_word)
    def read(self,address,size):
        uint(address,32)
        if type(size) is not int or size not in (1,2,4): raise ValueError('strict DATA width required')
        if self.reads>=self.max_reads: raise Boundary('explicit AI policy DATA budget')
        if size>1 and address&1: raise Boundary('odd DATA read')
        bus=address&0xFFFFFF
        if 0xFF0000<=bus and bus+size<=0x1000000: value=int.from_bytes(self.ram[bus&65535:(bus&65535)+size],'big')
        else: value=self.data.read(bus,size)
        self.reads+=1;self.events.append(('read',address,size,value));return value
    def write(self,address,size,value):
        uint(address,32)
        if type(size) is not int or size not in (1,2,4): raise ValueError('strict DATA width required')
        uint(value,size*8)
        if size>1 and address&1: raise Boundary('odd DATA write')
        bus=address&0xFFFFFF
        if not 0xFF0000<=bus or bus+size>0x1000000: raise Boundary('outside writable RAM')
        self.ram[bus&65535:(bus&65535)+size]=value.to_bytes(size,'big');self.events.append(('write',address,size,value))
    def table(self,base): return Table(self,base)
    def checked_table(self,value): return checked_table(value,self)
    def checked_cursor(self,value): return checked_cursor(value,self)
    def checked_contact_mask(self,value):
        if type(value) is not ContactMaskContext: raise ValueError('typed ContactMaskContext required')
        uint(value.mask_high_word,16);return value
    def checked_ranking(self,value):
        if type(value) is not RankingContext: raise ValueError('typed RankingContext required')
        uint(value.strength_offset,16);checked_cursor(value.tail,self);return value
    def checked_coordinate_scratch(self,value):
        if type(value) is not CoordinateScratchContext: raise ValueError('typed CoordinateScratchContext required')
        uint(value.coordinate_high_word,16);return value
    def checked_packed_count(self,value):
        if type(value) is not PackedCountContext: raise ValueError('typed PackedCountContext required')
        uint(value.count_high_byte,8);return value
    def checked_candidate_selection(self,value):
        if type(value) is not CandidateSelectionContext: raise ValueError('typed CandidateSelectionContext required')
        uint(value.fallback_offset,16);return value
    def checked_roster_strength(self,value):
        if type(value) is not RosterStrengthContext: raise ValueError('typed RosterStrengthContext required')
        uint(value.last_strength,32);return value
    def nonreturning_loop(self,reason):
        if type(reason) is not str or not reason: raise ValueError('named original non-return required')
        raise Boundary('original non-returning control loop: '+reason)
    def seed(self): return self.read(0xFFFFF61C,4)
    def store_seed(self,value): self.write(0xFFFFF61C,4,uint(value,32))
    def set_seed(self,value): self.store_seed(value)
    def seed_high(self): return self.read(0xFFFFF61C,2)
    def sample_random(self):
        from tools.high_level_city_event.arithmetic import random_sample
        return random_sample(self)
    def carry_result(self,value):
        if type(value) is not int or value not in (0,1): raise ValueError('strict carry0/1 required')
        if not self.sr&0x2000: raise Boundary('original full-SR operation requires supervisor')
        if self.sr&0x8000: raise Boundary('trace continuation not modeled')
        self.sr=(self.sr&65534)|value;return CarryOutcome(value,self.sr)
    def carry_observed(self,value):
        if type(value) is not int or value not in (0,1): raise ValueError('strict observed carry required')
        return CarryOutcome(value,(self.sr&65534)|value)
    def build_roster(self,city):
        city=uint(city,16)
        from tools.high_level_city_cycle.business import build_roster
        state=self
        class Adapter:
            @property
            def officer_assignments(self): return state.officer_assignments.cursor()
            @property
            def roster(self): return state.candidate_roster.cursor()
            def head(self): return state.head()
        return build_roster(Adapter(),city)
    def choose_city_head(self,city):
        city=uint(city,16)
        from tools.high_level_diplomacy_forces.business_shared import choose_city_head
        return choose_city_head(self,city)

    def divide_signed(self,numerator,denominator):
        from tools.high_level_city_event.arithmetic import signed_divmod
        return signed_divmod(uint(numerator,32),uint(denominator,32))

    def signed_divmod(self,numerator,denominator):
        return self.divide_signed(numerator,denominator)

    def count_force_cities(self,selector):
        from tools.high_level_ai_decision.business_selection import count_force_cities
        return count_force_cities(self,uint(selector,16))

    def select_force_by_city_count(self):
        from tools.high_level_ai_decision.business_selection import select_force_by_city_count
        return select_force_by_city_count(self)

    def mark_selected_roster_bit14(self,officer):
        from tools.high_level_ai_decision.business_commit import mark_selected_roster_bit14
        return mark_selected_roster_bit14(self,uint(officer,16))

    def set_carry(self,value):
        if type(value) is not bool: raise ValueError('strict carry bool required')
        return self.carry_result(int(value))

    def ai_recruitment_capacity_gate(self):
        from tools.high_level_city_officer.business_roster import ai_recruitment_capacity_gate
        outcome=ai_recruitment_capacity_gate(self)
        return CarryOutcome(outcome.carry,outcome.conditional_sr)

    def distribute_existing_troop_pool(self):
        from tools.high_level_city_officer.business_roster import distribute_existing_troop_pool
        outcome=distribute_existing_troop_pool(self)
        return CarryOutcome(outcome.carry,outcome.conditional_sr)

    def buy_and_distribute_troops(self,retained_budget):
        from tools.high_level_city_officer.business_roster import buy_and_distribute_troops
        return buy_and_distribute_troops(self,uint(retained_budget,32))

    def _movement_call(self,function,*arguments):
        """Explicit domain bridge: share live DATA, never snapshot RAM or events."""
        from tools.high_level_movement_v2 import domain as accepted
        adapter=accepted.GameState(self.ram,data=accepted.ReadOnlyData(self.data.segments),
            max_reads=self.max_reads,sr=self.sr)
        adapter.read=self.read
        adapter.write=self.write
        try:
            result=function(adapter,*arguments)
        except accepted.Boundary as error:
            raise Boundary(str(error)) from error
        finally:
            self.sr=adapter.sr
        if type(result) is accepted.PathResult:
            coordinates=PathCoordinates(result.final_coordinates.first,result.final_coordinates.second)
            return PathResult(result.length,result.retained_direction,coordinates,
                Cursor(self,result.final_frontier_cursor.base),Table(self,result.final_grid.base))
        if type(result) is accepted.CarryOutcome:
            return CarryOutcome(result.carry,result.conditional_sr)
        return result

    def build_path(self):
        from tools.high_level_movement_v2.business_path import build_path
        return self._movement_call(build_path)

    def build_path_from_cells(self):
        from tools.high_level_movement_v2.business_path import build_path_from_cells
        return self._movement_call(build_path_from_cells)

    def build_path_from_live_coordinates(self):
        return self.build_path_from_cells()

    def build_ai_movement_packet(self):
        from tools.high_level_movement_v2.business_campaign import build_ai_movement_packet
        return self._movement_call(build_ai_movement_packet)

    def choose_ai_destination(self):
        from tools.high_level_movement_v2.business_campaign import choose_ai_destination
        return self._movement_call(choose_ai_destination)

    def city_roster_full_carry(self,city):
        from tools.high_level_movement_v2.business_campaign import city_roster_full_carry
        return self._movement_call(city_roster_full_carry,uint(city,16))

    def force_troop_count(self,group):
        checked_cursor(group,self)
        from .business_routes import price_packed_group
        return price_packed_group(self,group)

class Table:
    def __init__(self,state,base):
        checked_state(state);self.state,self.base=state,uint(base,32)
    def address(self,offset=0,displacement=0):
        uint(offset,16)
        if type(displacement) is not int or not -32768<=displacement<=32767: raise ValueError('signed displacement required')
        return u32(self.base+s16(offset)+displacement)
    def byte(self,offset=0,displacement=0): return self.state.read(self.address(offset,displacement),1)
    def word(self,offset=0,displacement=0): return self.state.read(self.address(offset,displacement),2)
    def long(self,offset=0,displacement=0): return self.state.read(self.address(offset,displacement),4)
    def set_byte(self,offset,value,displacement=0): self.state.write(self.address(offset,displacement),1,uint(value,8))
    def set_word(self,offset,value,displacement=0): self.state.write(self.address(offset,displacement),2,uint(value,16))
    def set_long(self,offset,value,displacement=0): self.state.write(self.address(offset,displacement),4,uint(value,32))
    def at(self,offset=0,displacement=0): return type(self)(self.state,self.address(offset,displacement))
    def advance(self,amount):
        if type(amount) is not int or not -0x80000000<=amount<=0x7FFFFFFF: raise ValueError('signed LONG advance required')
        return type(self)(self.state,u32(self.base+amount))
    def cursor(self,offset=0): return Cursor(self.state,self.address(offset))
class Cursor(Table):
    def previous_byte(self): self.base=u32(self.base-1);return self.byte()
    def previous_word(self): self.base=u32(self.base-2);return self.word()

    def next_byte(self):
        value=self.byte();self.base=u32(self.base+1);return value
    def next_word(self):
        value=self.word();self.base=u32(self.base+2);return value
    def next_long(self):
        value=self.long();self.base=u32(self.base+4);return value
    def append_byte(self,value): self.set_byte(0,value);self.base=u32(self.base+1)
    def append_word(self,value): self.set_word(0,value);self.base=u32(self.base+2)
    def append_long(self,value): self.set_long(0,value);self.base=u32(self.base+4)
    def put_word(self,value): self.set_word(0,value)
def checked_state(value):
    if type(value) is not GameState: raise ValueError('typed AI policy GameState required')
    return value
def checked_table(value,state=None):
    if type(value) not in (Table,Cursor): raise ValueError('typed live Table/Cursor required')
    checked_state(value.state);uint(value.base,32)
    if state is not None and value.state is not state: raise ValueError('view must share live state')
    return value
def checked_cursor(value,state=None):
    if type(value) is not Cursor: raise ValueError('typed live Cursor required')
    return checked_table(value,state)
def checked_city_troop_summary(value):
    if type(value) is not CityTroopSummary: raise ValueError('typed CityTroopSummary required')
    uint(value.total,32);uint(value.qualifying_count,16)
    return value

PackedGroupCursor=Cursor

for _name,_base in VIEW_BASES.items(): setattr(GameState,_name,property(lambda self,base=_base:Table(self,base)))
for _name,(_address,_size) in SCALARS.items():
    setattr(GameState,_name,lambda self,a=_address,s=_size:self.read(a,s))
    setattr(GameState,'set_'+_name,lambda self,value,a=_address,s=_size:self.write(a,s,uint(value,s*8)))
AiState=GameState

