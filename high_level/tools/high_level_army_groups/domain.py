"""Live business DATA views; no implicit files, decoded catalogs or CPU facade."""
from dataclasses import dataclass
from typing import NewType

Byte=NewType('Byte',int)
Word=NewType('Word',int)
Long=NewType('Long',int)


class Boundary(ValueError):
    """A bounded DATA projection stops without undoing preceding effects."""


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
def s16(value):
    value=uint(value,16);return value-65536 if value&32768 else value
def s8(value):
    value=uint(value,8);return value-256 if value&128 else value
def low8(value): return u8(value)
def low16(value): return u16(value)
def high16(value): return uint(value,32)>>16
def swap_words(value):
    value=uint(value,32);return u32((value<<16)|(value>>16))
def replace_byte(value,byte): return (uint(value,32)&0xFFFFFF00)|uint(byte,8)
def replace_word(value,word): return (uint(value,32)&0xFFFF0000)|uint(word,16)
def negative_byte(value): return bool(uint(value,8)&128)
def negative_word(value): return bool(uint(value,16)&32768)
def negative_long(value): return bool(uint(value,32)&0x80000000)
def descending_inclusive(counter):
    uint(counter,16,'inclusive countdown');yield from range(counter,-1,-1)
def divu_retained(numerator,denominator):
    uint(numerator,32,'DIVU numerator');uint(denominator,16,'DIVU denominator')
    if denominator==0: raise Boundary('original DIVU divide by zero after preceding DATA')
    quotient,remainder=divmod(numerator,denominator)
    return numerator if quotient>65535 else (remainder<<16)|quotient


@dataclass(frozen=True)
class CarryOutcome:
    carry:int
    conditional_sr:int
    def __post_init__(self):
        if type(self.carry) is not int or self.carry not in (0,1): raise ValueError('strict carry0/1 required')
        uint(self.conditional_sr,16,'conditional SR')


class ReadOnlyData:
    """Explicit editable physical segments, with live reads and no loader."""
    def __init__(self,segments=()):
        if type(segments) is not tuple: raise ValueError('explicit readonly segment tuple required')
        rows=[]
        for item in segments:
            if type(item) is not tuple or len(item)!=2: raise ValueError('segment is (physical base, bytes)')
            base,raw=item;uint(base,32,'readonly base')
            if type(raw) is not bytes or not raw or base+len(raw)>0x1000000: raise ValueError('explicit nonempty 24bit segment required')
            rows.append((base,raw))
        rows.sort()
        if any(a+len(raw)>b for (a,raw),(b,_) in zip(rows,rows[1:])): raise ValueError('competing readonly authority')
        self.segments=tuple(rows)
    def read(self,address,size):
        uint(address,32,'physical readonly address')
        if type(size) is not int or size not in (1,2,4): raise ValueError('strict DATA width required')
        for base,raw in self.segments:
            if base<=address and address+size<=base+len(raw): return int.from_bytes(raw[address-base:address-base+size],'big')
        raise Boundary('outside explicitly supplied readonly DATA')


VIEW_BASES={
    'officer_assignments':0xFFFFCC00,'city_assignments':0xFFFFCC00,
    'alternate_assignments':0xFFFFA050,'candidate_roster':0xFFFFD300,
    'status_roster':0xFFFFD320,'remaining_roster':0xFFFFAF28,'survivor_roster':0xFFFFAF56,
    'status':0xFFFFC300,'loyalty':0xFFFFC500,'affinity':0xFFFFC200,'attributes':0xFFFFC400,
    'troops':0xFFFFB200,'officer_resources':0xFFFFB200,'troop_strengths':0xFFFFC800,
    'city_owners':0xFFFFF427,'other_city_owners':0xFFFFF428,'force_heads':0xFFFFE640,
    'packed_groups':0xFFFF9000,'group_packets':0xFFFF9000,'group_offsets':0xFFFFEFBE,
    'city_gold':0xFFFFDFFC,'city_rice':0xFFFFE09C,'city_ed84':0xFFFFED84,'city_ee24':0xFFFFEE24,
    'pair_references':0x00FF39B2,'head_records':0x00FF3000,
    'city_coordinates':0xD4AC6,'arrival_coordinates':0xD4ACA,'neighbor_offsets':0x21F82,
    'terrain':0xEE5F0,'terrain_cells':0xEE5F0,'terrain_cost':0x670A,'terrain_costs':0x670A,
}
SCALARS={
    'city':(0xFFFFF68A,2),'primary_force':(0xFFFFF68C,2),'secondary_force':(0xFFFFF68E,2),
    'primary_owner_byte':(0xFFFFF68D,1),'secondary_owner_byte':(0xFFFFF68F,1),
    'working_owner':(0xFFFFEFE2,1),'returning_count':(0xFFFFEFB8,2),'remaining_count':(0xFFFFEFBA,2),
    'resource_side':(0xFFFFF6D6,2),'side_flags':(0xFFFFF6D7,1),
    'selected_officer':(0xFFFFF3A6,2),'loyalty_source':(0xFFFFF3F2,2),
    'selected_group_offset':(0xFFFFEFC6,2),'selected_group_pointer':(0x00FF382C,4),
    'opposing_group':(0x00FF382C,4),'primary_officer':(0xFFFFF702,2),'secondary_officer':(0xFFFFF706,2),
    'outcome':(0xFFFF8114,2),'winning_officer':(0xFFFF80E0,2),'losing_officer':(0xFFFF80E2,2),
    'pair_reference_offset':(0x00FF3BB2,2),
}


class GameState:
    def __init__(self,ram,*,data=None,max_reads=1000000,sr=0x2700):
        if type(ram) is not bytearray or len(ram)!=65536: raise ValueError('explicit live64KiB bytearray required')
        if data is None: data=ReadOnlyData()
        if type(data) is not ReadOnlyData: raise ValueError('typed explicit readonly data required')
        uint(max_reads,32,'DATA budget');uint(sr,16,'conditional SR')
        if max_reads==0: raise ValueError('positive DATA budget required')
        self.ram,self.data,self.max_reads,self.sr=ram,data,max_reads,sr
        self.reads,self.events=0,[]
    def read(self,address,size):
        uint(address,32,'logical DATA address')
        if type(size) is not int or size not in (1,2,4): raise ValueError('strict DATA width required')
        if self.reads>=self.max_reads: raise Boundary('explicit army DATA budget')
        if size>1 and address&1: raise Boundary('odd DATA read')
        bus=address&0xFFFFFF
        if 0xFF0000<=bus and bus+size<=0x1000000: value=int.from_bytes(self.ram[bus&65535:(bus&65535)+size],'big')
        else: value=self.data.read(bus,size)
        self.reads+=1;self.events.append(('read',address,size,value));return value
    def write(self,address,size,value):
        uint(address,32,'logical DATA address')
        if type(size) is not int or size not in (1,2,4): raise ValueError('strict DATA width required')
        uint(value,size*8,'written DATA')
        if size>1 and address&1: raise Boundary('odd DATA write')
        bus=address&0xFFFFFF
        if not 0xFF0000<=bus or bus+size>0x1000000: raise Boundary('outside conditional writable RAM')
        self.ram[bus&65535:(bus&65535)+size]=value.to_bytes(size,'big');self.events.append(('write',address,size,value))
    def table(self,base): return Table(self,base)
    def checked_table(self,value): return checked_table(value,self)
    def checked_context(self,value): return checked_context(value,self)
    def seed(self): return self.read(0xFFFFF61C,4)
    def store_seed(self,value): self.write(0xFFFFF61C,4,uint(value,32,'random seed'))
    def sample_random(self):
        from tools.high_level_city_event.arithmetic import random_sample
        return random_sample(self)
    def terrain_query(self,row,column):
        row=u16(row);column=u16(column)
        stride=u16(row<<3);index=u16(u16(row+stride)<<3);index=u16(index+column)
        terrain=self.terrain_cells.byte(index);cost=self.terrain_costs.byte(terrain)
        return terrain,cost
    def carry_result(self,value):
        if type(value) is not int or value not in (0,1): raise ValueError('strict carry0/1 required')
        return self.set_carry(bool(value))
    def set_carry(self,value):
        if type(value) is not bool: raise ValueError('strict carry boolean required')
        if not self.sr&0x2000: raise Boundary('original SR operation requires supervisor')
        if self.sr&0x8000: raise Boundary('trace continuation not modeled')
        self.sr=(self.sr&65534)|int(value);return CarryOutcome(int(value),self.sr)


class Table:
    def __init__(self,state,base):
        if type(state) is not GameState: raise ValueError('typed live GameState required')
        self.state,self.base=state,uint(base,32,'view base')
    def address(self,offset=0,displacement=0):
        uint(offset,16,'signed WORD offset')
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
    def previous_byte(self): self.base=u32(self.base-1);return self.byte()
    def previous_word(self): self.base=u32(self.base-2);return self.word()
    def append_byte(self,value): self.set_byte(0,value);self.base=u32(self.base+1)
    def append_word(self,value): self.set_word(0,value);self.base=u32(self.base+2)
    def append_long(self,value): self.set_long(0,value);self.base=u32(self.base+4)


@dataclass(frozen=True)
class GroupContext:
    """Two live group views, including original compaction cursor corrections."""
    source:Table
    target:Table
    def __post_init__(self):
        checked_table(self.source);checked_table(self.target,self.source.state)


def checked_table(value,state=None):
    if type(value) not in (Table,Cursor) or type(value.state) is not GameState: raise ValueError('typed live Table/Cursor required')
    uint(value.base,32,'view base')
    if state is not None and value.state is not state: raise ValueError('view must share supplied live state')
    return value
def checked_context(value,state=None):
    if type(value) is not GroupContext: raise ValueError('typed GroupContext required')
    checked_table(value.source,state);checked_table(value.target,value.source.state);return value


def _view(name): return property(lambda self:Table(self,VIEW_BASES[name]))
def _reader(name): return lambda self:self.read(*SCALARS[name])
def _writer(name):
    address,size=SCALARS[name]
    return lambda self,value:self.write(address,size,uint(value,size*8))
for _name in VIEW_BASES: setattr(GameState,_name,_view(_name))
for _name in SCALARS:
    setattr(GameState,_name,_reader(_name));setattr(GameState,'set_'+_name,_writer(_name))
ArmyState=GameState


def project_army_arrival_fields(state: ArmyState, target: int, packet=None, city=None):
    """Share RAM/events; old scalar API never fabricated its missing D/A/SP/CCR."""
    from ..high_level_scene_flows.domain import SceneState, ReadOnlyData as SceneData
    from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame, first_replace
    from ..high_level_remaining_flows.business_city import execute_deployment_menu_fields
    if type(state) is not ArmyState:
        raise ValueError('actual historical ArmyState required')
    uint(target, 32)
    if packet is not None:
        checked_table(packet, state)
    if city is not None:
        uint(city, 16)
    scene = SceneState(state.ram, data=SceneData(state.data.segments), max_reads=state.max_reads, sr=state.sr)
    scene.events, scene.reads = state.events, state.reads
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        roster=None if packet is None else scene.table_at(packet.base).cursor())
    # A city WORD does not reveal the retained D3 high half.
    try:
        return execute_deployment_menu_fields(scene, target, frame)
    finally:
        state.reads, state.sr = scene.reads, scene.sr
