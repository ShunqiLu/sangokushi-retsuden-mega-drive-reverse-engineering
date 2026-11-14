"""Live typed business data, with explicit ROM views and bounded compatibility.

No file loader, implicit asset catalog, CPU interpreter or target opcode state.
Names for uncertain original fields remain neutral rather than inventing intent.
"""
from dataclasses import dataclass
from typing import NewType

Byte=NewType('Byte',int)
Word=NewType('Word',int)
Long=NewType('Long',int)


class Boundary(ValueError):
    """An honest data/privilege boundary; preceding live effects are retained."""


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
    uint(counter,16,'inclusive countdown');yield from range(counter,-1,-1)
def divu_retained(numerator,denominator):
    uint(numerator,32);uint(denominator,16)
    if denominator==0: raise Boundary('original DIVU divide by zero after preceding DATA')
    quotient,remainder=divmod(numerator,denominator)
    return numerator if quotient>65535 else (remainder<<16)|quotient


@dataclass(frozen=True)
class CarryOutcome:
    carry:int
    conditional_sr:int
    def __post_init__(self):
        if type(self.carry) is not int or self.carry not in (0,1): raise ValueError('strict carry0/1 required')
        uint(self.conditional_sr,16)


@dataclass(frozen=True)
class HeadMatch:
    head:int
    carry:int
    conditional_sr:int
    def __post_init__(self):
        uint(self.head,16)
        CarryOutcome(self.carry,self.conditional_sr)


class ReadOnlyData:
    """Explicit editable source segments. Target generation never reads these."""
    def __init__(self,segments=()):
        if type(segments) is not tuple: raise ValueError('explicit segment tuple required')
        rows=[]
        for item in segments:
            if type(item) is not tuple or len(item)!=2: raise ValueError('(physical base, bytes) required')
            base,raw=item;uint(base,32)
            if type(raw) is not bytes or not raw or base+len(raw)>0x1000000: raise ValueError('nonempty 24bit source required')
            rows.append((base,raw))
        rows.sort()
        if any(a+len(raw)>b for (a,raw),(b,_) in zip(rows,rows[1:])): raise ValueError('competing source authorities')
        self.segments=tuple(rows)
    def read(self,address,size):
        uint(address,32)
        if type(size) is not int or size not in (1,2,4): raise ValueError('strict DATA width required')
        for base,raw in self.segments:
            if base<=address and address+size<=base+len(raw): return int.from_bytes(raw[address-base:address-base+size],'big')
        raise Boundary('outside explicit readonly source')


VIEW_BASES={
    'officer_assignments':0xFFFFCC00,'officer_actions':0xFFFFCD00,'officer_flags':0xFFFFCD00,
    'city_owners':0xFFFFF427,'other_city_owners':0xFFFFF428,'force_heads':0xFFFFE640,'force_leaders':0xFFFFE640,
    'city_heads':0xFFFFF45E,'other_city_heads':0xFFFFF460,'candidate_roster':0xFFFFF500,
    'action_roster':0xFFFFF502,'officer_status':0xFFFFC300,'status':0xFFFFC300,
    'affinity':0xFFFFC200,'officer_affinity':0xFFFFC200,'progress_be':0xFFFFBE00,
    'progress_c':0xFFFFC000,'intelligence':0xFFFFB600,'base_attribute':0xFFFFB400,
    'troops':0xFFFFB200,'traits':0xFFFFC700,'officer_traits':0xFFFFC700,'officer_ability':0xFFFFB600,
    'city_gold':0xFFFFDFFC,'city_rice':0xFFFFE09C,
    'city_orders':0xFFFFE80C,'other_city_orders':0xFFFFE818,'owner_change_count':0xFFFFF590,
    'force_city_roster':0xFFFFF5A0,'player_forces':0xFFFFF67A,'head_alias':0xFFFFF630,
    'packed_groups':0xFFFF9000,'pair_references':0x00FF39B2,'alternate_assignments':0xFFFFA050,
    'city_processed':0xFFFFEA37,'temporary_city_flags':0xFFFF9FFF,'temporary_city_bits':0xFFFFEFAA,
    'city_reserves':0xFFFFE31C,
    'queue_principals':0xFFFFE65C,'force_queue':0xFFFFE9F8,
    'scenario_factors':0xDF1A,'direct_factors':0xDF3E,'bribe_factors':0x11380,
    'persuasion_factors':0x11842,'scenario_join_factors':0x111A6,'persuasion_weights':0x111A6,
    'message_directory':0x92C4A,'message_bank_offsets':0x92C4E,'message_layout':0x6773C,
}
SCALARS={
    'selected_city':(0xFFFFF3A8,2),'current_city':(0xFFFFF392,2),'current_city_byte':(0xFFFFF393,1),
    'selected_officer':(0xFFFFF3A6,2),'target_officer':(0xFFFFF3F2,2),'loyalty_source':(0xFFFFF3F2,2),
    'secondary_target':(0xFFFFF372,2),'current_force':(0xFFFFF376,2),'current_force_byte':(0xFFFFF377,1),
    'method':(0xFFFFF57D,1),'response':(0xFFFFF38C,2),'request_gold':(0xFFFFF39E,4),
    'request_rice':(0xFFFFF3BA,4),'head':(0xFFFFF630,2),'scenario':(0xFFFFEFD2,2),
    'mode_side':(0xFFFFF64A,2),'working_force':(0xFFFFF64C,2),'scene':(0xFFFFF612,2),
    'route':(0xFFFFF612,2),'stage':(0xFFFFF362,2),'message_scene':(0xFFFFF3C2,2),
    'message_stage':(0xFFFFF3C4,2),'message_pointer':(0xFFFFF3BE,4),'message_flag':(0xFFFFF652,2),
    'message_kind':(0xFFFFF36A,2),'message_parameter':(0xFFFFF3C6,2),'message_mode':(0xFFFFF600,2),
    'message_layout_index':(0xFFFFF6C4,2),'message_pending':(0xFFFFEFDA,2),'message_delay':(0xFFFFF608,2),
    'message_code':(0xFFFFF3FE,2),'display_target':(0xFFFFF3D2,2),'display_actor':(0xFFFFF3D0,2),
    'scene_queue':(0x00FF7026,2),'scene_x':(0xFFFFF386,2),'scene_y':(0xFFFFF384,2),
    'scene_aux':(0xFFFFF64E,2),'pending_force_change':(0xFFFFA622,2),'removed_force':(0xFFFFEFB0,2),
    'temporary_city_mask':(0xFFFFEFAA,2),'force_queue_mask':(0xFFFFE700,2),
    'pair_reference_offset':(0x00FF3BB2,2),
    'city_tail':(0xFFFFF393,1),'current_city_high':(0xFFFFF392,1),'current_force_tail':(0xFFFFF377,1),'difficulty':(0xFFFFEFD2,2),
    'protected_head':(0xFFFFF62E,2),
    'player_force_1':(0xFFFFF67A,2),'player_force_2':(0xFFFFF67C,2),'player_force_3':(0xFFFFF67E,2),
    'step':(0xFFFFF362,2),'message':(0xFFFFF3FE,2),'message_actor':(0xFFFFF3D0,2),
    'message_target':(0xFFFFF3D2,2),'message_gate':(0xFFFFF652,2),
    'roster_exclusion':(0xFFFFF630,2),'ui_first':(0xFFFFF386,2),'ui_second':(0xFFFFF384,2),
    'joining_refresh':(0xFFFFF64E,2),'seed_word':(0xFFFFF61C,2),
}


class GameState:
    def __init__(self,ram,*,data=None,max_reads=1000000,sr=0x2700):
        if type(ram) is not bytearray or len(ram)!=65536: raise ValueError('explicit live64KiB RAM required')
        if data is None: data=ReadOnlyData()
        if type(data) is not ReadOnlyData: raise ValueError('typed readonly source required')
        uint(max_reads,32);uint(sr,16)
        if max_reads==0: raise ValueError('positive DATA budget required')
        self.ram,self.data,self.max_reads,self.sr=ram,data,max_reads,sr
        self.reads,self.events=0,[]
    def read(self,address,size):
        uint(address,32)
        if type(size) is not int or size not in (1,2,4): raise ValueError('strict DATA width required')
        if self.reads>=self.max_reads: raise Boundary('explicit diplomacy DATA budget')
        if size>1 and address&1: raise Boundary('odd DATA read')
        bus=address&0xFFFFFF
        if 0xFF0000<=bus and bus+size<=0x1000000: value=int.from_bytes(self.ram[bus&65535:(bus&65535)+size],'big')
        else: value=self.data.read(bus,size)
        self.reads+=1;self.events.append(('read',address,size,value));return value
    def write(self,address,size,value):
        uint(address,32);uint(value,size*8)
        if type(size) is not int or size not in (1,2,4): raise ValueError('strict DATA width required')
        if size>1 and address&1: raise Boundary('odd DATA write')
        bus=address&0xFFFFFF
        if not 0xFF0000<=bus or bus+size>0x1000000: raise Boundary('outside writable RAM')
        self.ram[bus&65535:(bus&65535)+size]=value.to_bytes(size,'big');self.events.append(('write',address,size,value))
    def table(self,base): return Table(self,base)
    def checked_table(self,value): return checked_table(value,self)
    def seed(self): return self.read(0xFFFFF61C,4)
    def store_seed(self,value): self.write(0xFFFFF61C,4,uint(value,32))
    def set_seed(self,value): self.store_seed(value)
    def seed_high(self): return self.read(0xFFFFF61C,2)
    def sample_random(self):
        from tools.high_level_city_event.arithmetic import random_sample
        return random_sample(self)
    def carry_result(self,value):
        if type(value) is not int or value not in (0,1): raise ValueError('strict carry0/1 required')
        if not self.sr&0x2000: raise Boundary('original SR operation requires supervisor')
        if self.sr&0x8000: raise Boundary('trace continuation not modeled')
        self.sr=(self.sr&65534)|value
        return CarryOutcome(value,self.sr)
    def build_roster(self,city):
        city=uint(city,16)
        from tools.high_level_city_cycle.business import build_roster
        state=self
        class RosterAdapter:
            @property
            def officer_assignments(self): return state.officer_assignments.cursor()
            @property
            def roster(self): return state.candidate_roster.cursor()
            def head(self): return state.head()
        return build_roster(RosterAdapter(),city)
    @property
    def roster(self): return self.candidate_roster.cursor()
    def owner_head(self,city):
        city=uint(city,16)
        from tools.high_level_city_officer.business_officer import owner_head_lookup
        return owner_head_lookup(self,city)
    def mark_c300_list(self):
        from tools.high_level_city_officer.business_officer import mark_c300_list
        return mark_c300_list(self)
    def clear_city_orders(self):
        from tools.high_level_city_officer.business_officer import clear_city_orders
        return clear_city_orders(self)
    def replace_city_assignments(self,replacement):
        replacement=uint(replacement,16)
        from tools.high_level_city_officer.business_officer import replace_city_assignments
        return replace_city_assignments(self,replacement)
    def clear_selected_links(self):
        from tools.high_level_debt_cleanup.domain import DebtState
        from tools.high_level_debt_cleanup.business import clear_selected_links
        adapter=DebtState(self.ram)
        # Its DATA adapter is replaced explicitly to share the live event stream.
        adapter.read=self.read;adapter.write=self.write
        return clear_selected_links(adapter)
    def apply_returning_officer_loyalty(self):
        from tools.high_level_army_groups.business_arrival import apply_returning_officer_loyalty
        return apply_returning_officer_loyalty(self)


class Table:
    def __init__(self,state,base):
        if type(state) is not GameState: raise ValueError('typed live GameState required')
        self.state,self.base=state,uint(base,32)
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
    def at(self,offset=0,displacement=0): return Table(self.state,self.address(offset,displacement))
    def advance(self,amount):
        if type(amount) is not int or not -0x80000000<=amount<=0x7FFFFFFF: raise ValueError('signed LONG advance required')
        return type(self)(self.state,u32(self.base+amount))
    def cursor(self,offset=0): return Cursor(self.state,self.address(offset))


class Cursor(Table):
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


def checked_table(value,state=None):
    if type(value) not in (Table,Cursor) or type(value.state) is not GameState: raise ValueError('typed live Table/Cursor required')
    uint(value.base,32)
    if state is not None and value.state is not state: raise ValueError('view must share live state')
    return value


for _name,_base in VIEW_BASES.items():
    setattr(GameState,_name,property(lambda self,base=_base:Table(self,base)))
for _name,(_address,_size) in SCALARS.items():
    setattr(GameState,_name,lambda self,a=_address,s=_size:self.read(a,s))
    setattr(GameState,'set_'+_name,lambda self,value,a=_address,s=_size:self.write(a,s,uint(value,s*8)))
DiplomacyState=GameState
