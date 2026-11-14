"""Live fixed-width data views; no file access, ROM cache or CPU register facade."""
from dataclasses import dataclass
from typing import NewType

Byte = NewType('Byte', int)
Word = NewType('Word', int)
Long = NewType('Long', int)


class Boundary(ValueError):
    """The preceding live DATA effects remain when a bounded operation stops."""


def uint(value, bits, name='value'):
    if type(bits) is not int or bits not in (8,16,32) or type(value) is not int or not 0 <= value < 1 << bits:
        raise ValueError(f'strict {bits}-bit {name} required')
    return value


def u8(value):
    if type(value) is not int: raise ValueError('integer BYTE arithmetic required')
    return value & 255


def u16(value):
    if type(value) is not int: raise ValueError('integer WORD arithmetic required')
    return value & 65535


def u32(value):
    if type(value) is not int: raise ValueError('integer LONG arithmetic required')
    return value & 0xFFFFFFFF


def s8(value):
    value=uint(value,8);return value-256 if value&128 else value


def s16(value):
    value=uint(value,16);return value-65536 if value&32768 else value


def low8(value): return u8(value)
def low16(value): return u16(value)
def high16(value): return uint(value,32) >> 16
def negative_byte(value): return bool(uint(value,8)&128)
def negative_word(value): return bool(uint(value,16)&32768)
def negative_long(value): return bool(uint(value,32)&0x80000000)
def replace_byte(value, byte): return (uint(value,32)&0xFFFFFF00)|uint(byte,8)
def replace_word(value, word): return (uint(value,32)&0xFFFF0000)|uint(word,16)
def add_low_word(value, amount): return replace_word(value,u16(low16(value)+uint(amount,16)))
def descending_inclusive(counter):
    uint(counter,16,'inclusive countdown');yield from range(counter,-1,-1)


def divu_retained(numerator, denominator):
    uint(numerator,32,'DIVU numerator');uint(denominator,16,'DIVU denominator')
    if denominator==0: raise Boundary('original division by zero after preceding DATA')
    quotient,remainder=divmod(numerator,denominator)
    return numerator if quotient>65535 else (remainder<<16)|quotient


@dataclass(frozen=True)
class CarryOutcome:
    carry: int
    conditional_sr: int

    def __post_init__(self):
        if type(self.carry) is not int or self.carry not in (0,1): raise ValueError('strict carry0/1 required')
        uint(self.conditional_sr,16,'conditional SR')


class ReadOnlyData:
    """Explicit editable segments; aliases are read live, never loaded implicitly."""
    def __init__(self, segments=()):
        if type(segments) is not tuple: raise ValueError('explicit segment tuple required')
        rows=[]
        for item in segments:
            if type(item) is not tuple or len(item)!=2: raise ValueError('segment is (physical base, bytes)')
            base,raw=item;uint(base,32,'physical readonly base')
            if type(raw) is not bytes or not raw or base+len(raw)>0x1000000: raise ValueError('nonempty explicit24bit segment required')
            rows.append((base,raw))
        rows.sort()
        if any(a+len(raw)>b for (a,raw),(b,_) in zip(rows,rows[1:])): raise ValueError('competing readonly authority')
        self.segments=tuple(rows)

    def read(self, address, size):
        uint(address,32,'physical readonly address')
        if type(size) is not int or size not in (1,2,4): raise ValueError('strict DATA width required')
        for base,raw in self.segments:
            if base<=address and address+size<=base+len(raw): return int.from_bytes(raw[address-base:address-base+size],'big')
        raise Boundary('outside explicitly supplied readonly data')


VIEW_BASES = {
    'officer_assignments':0xFFFFCC00,'officer_actions':0xFFFFCD00,'officer_flags':0xFFFFCD00,
    'officer_status':0xFFFFC300,'progress_be':0xFFFFBE00,'progress_c':0xFFFFC000,
    'capacities_b000':0xFFFFB000,'troops_b200':0xFFFFB200,'city_processed':0xFFFFEA37,
    'city_action_gates':0xFFFFEA38,'city_owners':0xFFFFF427,'force_heads':0xFFFFE640,
    'city_orders':0xFFFFE80C,'education_factors':0xE776,'terrain_cells':0xEE5F0,
    'terrain_costs':0x670A,'action_roster':0xFFFFF502,
    'recruitment_pools':0xFFFFE774,'balances':0xFFFFDFFC,'city_heads':0xFFFFF45E,
    'alternate_heads':0xFFFFA026,'action_flags':0xFFFFC700,'battle_primary_roster':0xFFFFA550,
    'defender_roster':0xFFFFA5A4,'primary_transfer_roster':0xFFFFA5CE,
    'secondary_transfer_roster':0xFFFFA57A,'defender_tail':0xFFFFA5A6,
    'working_roster':0xFFFFF500,'ai_roster':0xFFFFF72A,'capacities':0xFFFFB800,
    'troops':0xFFFFC800,'assignment_a654':0xFFFFA654,'assignment_a754':0xFFFFA754,
    'assignment_ae28':0xFFFFAE28,'assignment_ceae':0xFFFFCEAE,
    'city_gold':0xFFFFDFFC,'city_rice':0xFFFFE09C,'city_tax_orders':0xFFFFE3BC,
    'transport_orders':0xFFFFCDFC,'city_coordinates':0xD4AC6,'transport_costs':0x13B68,
    'transport_awards':0x13B60,'equipment_prices':0xFFFFEF6A,'equipment_levels':0xFFFFEF64,
    'officer_equipment':0xFFFFEA88,'force_leaders':0xFFFFE640,
    'relationship_targets':0xFFFFE730,'force_relationships':0xFFFFE710,
    'city_assignments':0xFFFFCC00,'route_bytes':0x00FF4000,'transport_objects':0xFFFFCE00,
    'packed_objects':0xFFFF9000,'selected_costs':0x1344C,'city_ed84':0xFFFFED84,
    'city_ee24':0xFFFFEE24,
}
SCALARS = {
    'selected_city':(0xFFFFF3A8,2),'selected_officer':(0xFFFFF3A6,2),
    'current_city':(0xFFFFF364,2),'current_force':(0xFFFFF376,2),
    'development_amount':(0xFFFFF3A0,2),'order_amount':(0xFFFFF39E,4),
    'scene':(0xFFFFF612,2),'next_state':(0xFFFFF362,2),
    'working_pool':(0xFFFFF3E4,4),'allocation_pool':(0xFFFFCFAE,4),
    'chosen_city':(0xFFFFF392,2),'cost':(0xFFFFF39E,4),'battle_city':(0xFFFFF68A,2),
    'battle_owner':(0xFFFFF68E,2),'defender_count':(0xFFFFF6A8,2),
    'active_battle':(0xFFFFEFE0,2),'outcome':(0xFFFF8114,2),
    'winning_officer':(0xFFFF80E0,2),'losing_officer':(0xFFFF80E2,2),
    'primary_officer':(0xFFFFF702,2),'working_count':(0xFFFFF636,2),
    'battle_count':(0xFFFFF6D0,2),'clear_f6e8':(0xFFFFF6E8,2),'clear_f6ea':(0xFFFFF6EA,2),
    'clear_f6ec':(0xFFFFF6EC,2),'clear_f6ee':(0xFFFFF6EE,2),
    'clear_f6c8':(0xFFFFF6C8,2),'clear_f6f8':(0xFFFFF6F8,2),
    'chosen_city_tail':(0xFFFFF393,1),'transport_choice':(0xFFFFF688,2),
    'tail_city':(0xFFFFF68A,2),'relationship_target':(0xFFFFF3E0,2),
    'equipment_choice':(0xFFFFF3F0,2),'tax_rate':(0xFFFFF3B6,2),
    'selected_cost':(0xFFFFF39A,2),'current_cost':(0xFFFFF3F4,4),'cost_limit':(0xFFFFF3F8,4),
    'relationship_credit':(0xFFFFF3C8,4),'credit_is_rice':(0xFFFFF742,2),
    'route_offset':(0xFFFFCEAC,2),'route_x':(0xFFFFCEA8,2),'route_y':(0xFFFFCEAA,2),
    'snapshot_gold':(0xFFFFF69A,4),'snapshot_rice':(0xFFFFF6A2,4),
    'city_snapshot_ed84':(0xFFFFF696,4),'city_snapshot_ee24':(0xFFFFF69E,4),
    'command_mode':(0xFFFFF612,2),'command_step':(0xFFFFF362,2),
    'command_result':(0xFFFFF3FE,2),'command_officer':(0xFFFFF3D0,2),
    'command_active':(0xFFFFF774,2),'scene_selector':(0x00FF7026,2),'requested_mode':(0xFFFFF38A,2),
}


class GameState:
    def __init__(self, ram, *, data=None, max_reads=1000000, sr=0x2700):
        if type(ram) is not bytearray or len(ram)!=65536: raise ValueError('explicit live64KiB bytearray required')
        if data is None: data=ReadOnlyData()
        if type(data) is not ReadOnlyData: raise ValueError('typed explicit readonly data required')
        uint(max_reads,32,'DATA budget');uint(sr,16,'conditional SR')
        if max_reads==0: raise ValueError('positive DATA budget required')
        self.ram,self.data,self.max_reads,self.sr=ram,data,max_reads,sr
        self.reads,self.events=0,[]

    def read(self, address, size):
        uint(address,32,'logical DATA address')
        if type(size) is not int or size not in (1,2,4): raise ValueError('strict DATA width required')
        if self.reads>=self.max_reads: raise Boundary('explicit city/officer DATA budget')
        if size>1 and address&1: raise Boundary('odd DATA read')
        bus=address&0xFFFFFF
        if 0xFF0000<=bus and bus+size<=0x1000000: value=int.from_bytes(self.ram[bus&65535:(bus&65535)+size],'big')
        else: value=self.data.read(bus,size)
        self.reads+=1;self.events.append(('read',address,size,value));return value

    def write(self, address, size, value):
        uint(address,32,'logical DATA address')
        if type(size) is not int or size not in (1,2,4): raise ValueError('strict DATA width required')
        uint(value,size*8,'written DATA')
        if size>1 and address&1: raise Boundary('odd DATA write')
        bus=address&0xFFFFFF
        if not (0xFF0000<=bus and bus+size<=0x1000000): raise Boundary('outside conditional writable RAM')
        self.ram[bus&65535:(bus&65535)+size]=value.to_bytes(size,'big')
        self.events.append(('write',address,size,value))

    def table(self, base): return Table(self,base)
    def carry_result(self, value):
        if type(value) is not int or value not in (0,1): raise ValueError('strict carry0/1 required')
        return self.set_carry(bool(value))
    def set_carry(self, value):
        if type(value) is not bool: raise ValueError('strict carry boolean required')
        if not self.sr&0x2000: raise Boundary('original SR operation requires supervisor')
        if self.sr&0x8000: raise Boundary('trace continuation not modeled')
        self.sr=(self.sr&65534)|int(value);return CarryOutcome(int(value),self.sr)


class Table:
    def __init__(self, state, base):
        if type(state) is not GameState: raise ValueError('typed GameState required')
        self.state,self.base=state,uint(base,32,'view base')
    def address(self, offset=0, displacement=0):
        uint(offset,16,'signed WORD offset')
        if type(displacement) is not int or not -32768<=displacement<=32767: raise ValueError('signed displacement required')
        return u32(self.base+s16(offset)+displacement)
    def byte(self, offset=0, displacement=0): return self.state.read(self.address(offset,displacement),1)
    def word(self, offset=0, displacement=0): return self.state.read(self.address(offset,displacement),2)
    def long(self, offset=0, displacement=0): return self.state.read(self.address(offset,displacement),4)
    def set_byte(self, offset, value, displacement=0): self.state.write(self.address(offset,displacement),1,uint(value,8))
    def set_word(self, offset, value, displacement=0): self.state.write(self.address(offset,displacement),2,uint(value,16))
    def set_long(self, offset, value, displacement=0): self.state.write(self.address(offset,displacement),4,uint(value,32))
    def at(self, offset=0, displacement=0): return type(self)(self.state,self.address(offset,displacement))
    def advance(self, amount):
        if type(amount) is not int or not -0x80000000<=amount<=0x7FFFFFFF: raise ValueError('signed LONG advance required')
        return type(self)(self.state,u32(self.base+amount))
    def cursor(self, offset=0): return Cursor(self.state,self.address(offset))


class Cursor(Table):
    def next_byte(self):
        value=self.byte();self.base=u32(self.base+1);return value
    def next_word(self):
        value=self.word();self.base=u32(self.base+2);return value
    def next_long(self):
        value=self.long();self.base=u32(self.base+4);return value
    def previous_byte(self): self.base=u32(self.base-1);return self.byte()
    def previous_word(self): self.base=u32(self.base-2);return self.word()
    def previous_long(self): self.base=u32(self.base-4);return self.long()
    def append_byte(self,value): self.set_byte(0,value);self.base=u32(self.base+1)
    def append_word(self,value): self.set_word(0,value);self.base=u32(self.base+2)
    def append_long(self,value): self.set_long(0,value);self.base=u32(self.base+4)


def _view(name): return property(lambda self:Table(self,VIEW_BASES[name]))
def _reader(name): return lambda self:self.read(*SCALARS[name])
def _writer(name):
    address,size=SCALARS[name]
    return lambda self,value:self.write(address,size,uint(value,size*8))


for _name in VIEW_BASES: setattr(GameState,_name,_view(_name))
for _name in SCALARS:
    setattr(GameState,_name,_reader(_name));setattr(GameState,'set_'+_name,_writer(_name))


def project_officer_arrival_fields(state: GameState, target: int, row=None, column=None):
    """Same-RAM officer API projection, with unobserved full WORD high halves."""
    from ..high_level_scene_flows.domain import SceneState, ReadOnlyData as SceneData
    from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame
    from ..high_level_remaining_flows.business_city import execute_deployment_menu_fields
    if type(state) is not GameState:
        raise ValueError('actual historical officer GameState required')
    uint(target, 32)
    for value in (row, column):
        if value is not None:
            uint(value, 16)
    scene = SceneState(state.ram, data=SceneData(state.data.segments), max_reads=state.max_reads, sr=state.sr)
    scene.events, scene.reads = state.events, state.reads
    try:
        return execute_deployment_menu_fields(scene, target, FirstDeploymentFrame.unobserved())
    finally:
        state.reads, state.sr = scene.reads, scene.sr
