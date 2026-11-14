"""Explicit live RAM and readonly data views; this is not an instruction CPU."""
from dataclasses import dataclass
from typing import NewType

Byte = NewType('Byte', int)
Word = NewType('Word', int)
Long = NewType('Long', int)


class Boundary(ValueError):
    pass


def uint(value, bits, name='value'):
    if type(bits) is not int or bits not in (8, 16, 32) or type(value) is not int or not 0 <= value < 1 << bits:
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


def s16(value):
    value = uint(value, 16, 'signed WORD')
    return value - 65536 if value & 32768 else value


def low8(value): return u8(value)
def low16(value): return u16(value)
def high16(value): return uint(value, 32) >> 16
def zero_extend_word(value): return uint(value, 16, 'zero-extended WORD')
def negative_word(value): return bool(uint(value, 16) & 32768)
def negative_byte(value): return bool(uint(value, 8) & 128)
def replace_byte(value, byte): return (uint(value, 32) & 0xFFFFFF00) | uint(byte, 8)
def replace_word(value, word): return (uint(value, 32) & 0xFFFF0000) | uint(word, 16)
def add_low_word(value, amount): return replace_word(value, u16(low16(value) + uint(amount, 16)))
def add_low_byte(value, amount): return replace_byte(value, u8(low8(value) + uint(amount, 8)))
def sub_low_byte(value, amount): return replace_byte(value, u8(low8(value) - uint(amount, 8)))
def shift_low_word(value, count): return replace_word(value, low16(value) >> uint(count, 8))


def descending_inclusive(counter):
    uint(counter, 16, 'inclusive countdown')
    yield from range(counter, -1, -1)


def consume_countdown_latch(counter):
    """Encoded DBRA self-latch consumes no additional data reads."""
    uint(counter, 16, 'latch counter')
    return 65535


def divu_retained(numerator, denominator):
    uint(numerator, 32, 'DIVU numerator'); uint(denominator, 16, 'DIVU denominator')
    if not denominator: raise Boundary('original DIVU zero after preceding DATA reads')
    quotient, remainder = divmod(numerator, denominator)
    if quotient > 65535: return numerator
    return (remainder << 16) | quotient


@dataclass(frozen=True)
class CarryOutcome:
    carry: int
    conditional_sr: int
    def __post_init__(self):
        if type(self.carry) is not int or self.carry not in (0, 1):
            raise ValueError('strict carry 0/1 required')
        uint(self.conditional_sr, 16, 'conditional SR diagnostic')


class ReadOnlyData:
    """Explicit editable source segments, not an implicit whole-ROM reader.

    Segments may include an intentional code/data alias provided by the caller.
    A catalog boundary is never a clamp: an unprovided neighbor is a boundary.
    No disk, original-ROM hash, mapper or sample-size assumption is hidden here.
    """
    def __init__(self, segments=()):
        if type(segments) is not tuple:
            raise ValueError('strict tuple of explicit readonly data segments required')
        rows = []
        for item in segments:
            if type(item) is not tuple or len(item) != 2:
                raise ValueError('readonly segment is (physical base, bytes)')
            base, data = item
            uint(base, 32, 'readonly base')
            if type(data) is not bytes or not data or base + len(data) > 0x1000000:
                raise ValueError('nonempty explicit BYTE segment within 24-bit bus required')
            rows.append((base, data))
        rows.sort()
        if any(a + len(data) > b for (a, data), (b, _) in zip(rows, rows[1:])):
            raise ValueError('readonly segments cannot have competing physical authority')
        self.segments = tuple(rows)

    def read(self, address, size):
        for base, data in self.segments:
            if base <= address and address + size <= base + len(data):
                return int.from_bytes(data[address-base:address-base+size], 'big')
        raise Boundary('outside explicitly supplied readonly DATA segments')


VIEW_BASES = {
    'selected_roster': 0xFFFFF500, 'selected_attributes': 0xFFFFC400,
    'capacity_fields': 0xFFFFC800, 'assignment_flags': 0xFFFFA050,
    'coordinates': 0xFFFFA150, 'city_assignments': 0xFFFFCC00,
    'city_owners': 0xFFFFF427, 'force_leaders': 0xFFFFE640,
    'packed_offsets': 0xFFFFEFBE, 'packed_entities': 0xFFFF9000,
    'side_attributes': 0xFFFFC500, 'ratio_attributes': 0xFFFFB400,
    'troops': 0xFFFFB200, 'awards': 0xFFFFC000,
    'terrain_cells': 0xEE5F0, 'battle_mode_parameters': 0x1B832,
    'terrain_parameters': 0x1B890, 'attribute_selectors': 0xFFFFEA88,
    'attribute_weights': 0x1F910, 'selected_attribute_roster': 0x00FF398A,
    'active_queue': 0x00FF3000, 'pair_queue': 0x00FF39B2,
    'status_primary': 0xFFFFA654, 'status_secondary': 0x00FF3DC2,
    'status_tertiary': 0xFFFFA754, 'status_3cc2': 0x00FF3CC2,
    'first_roster': 0xFFFFA5A4, 'second_roster': 0xFFFFA550,
    'city_flags': 0xFFFFEA37, 'average_roster': 0x00FF398A,
}
SCALARS = {
    'city_word': (0xFFFFF392, 2), 'city_tail': (0xFFFFF393, 1),
    'state_mode': (0xFFFFF612, 2), 'command_step': (0xFFFFF362, 2),
    'tail_city': (0xFFFFF68A, 2), 'object_index': (0xFFFFEFC6, 2),
    'opposing_object': (0x00FF382C, 4), 'active_force_1': (0xFFFFF67B, 1),
    'active_force_2': (0xFFFFF67D, 1), 'active_force_3': (0xFFFFF67F, 1),
    'queue_counter': (0x00FF3826, 2), 'pair_queue_offset': (0x00FF3BB2, 2),
    'attacker_officer': (0xFFFFF3A6, 2), 'defender_officer': (0xFFFFF3F2, 2),
    'first_officer': (0xFFFFF702, 2), 'second_officer': (0xFFFFF706, 2),
    'first_force': (0xFFFFF68C, 2), 'second_force': (0xFFFFF68E, 2),
    'battle_mode': (0xFFFF80DA, 1), 'battle_terrain': (0xFFFF80DB, 1),
    'mode_clear': (0xFFFF8124, 1), 'swap_sides': (0xFFFF8125, 1),
    'first_leader': (0xFFFF80DC, 2), 'second_leader': (0xFFFF80DE, 2),
    'first_selected': (0xFFFF80E0, 2), 'second_selected': (0xFFFF80E2, 2),
    'first_side_attribute': (0xFFFF8101, 1), 'second_side_attribute': (0xFFFF8103, 1),
    'first_maximum': (0xFFFF8108, 2), 'second_maximum': (0xFFFF810A, 2),
    'first_ratio_attribute': (0xFFFF8104, 2), 'second_ratio_attribute': (0xFFFF8106, 2),
    'first_troops': (0xFFFF810C, 2), 'second_troops': (0xFFFF810E, 2),
    'first_awards': (0xFFFF8110, 2), 'second_awards': (0xFFFF8112, 2),
    'first_capacity': (0xFFFF80E4, 2), 'second_capacity': (0xFFFF80E6, 2),
    'outcome': (0xFFFF8114, 2), 'outcome_mode': (0xFFFFF6D6, 2),
    'outcome_side': (0xFFFFF6D7, 1),
}


class PreparationState:
    def __init__(self, ram, *, data=None, max_reads=1000000, sr=0x2700):
        if type(ram) is not bytearray or len(ram) != 65536:
            raise ValueError('explicit live 64-KiB RAM required')
        if data is None: data = ReadOnlyData()
        if type(data) is not ReadOnlyData: raise ValueError('explicit ReadOnlyData required')
        uint(max_reads, 32, 'read budget'); uint(sr, 16, 'conditional SR')
        if not max_reads: raise ValueError('positive DATA budget required')
        self.ram, self.data, self.max_reads, self.sr = ram, data, max_reads, sr
        self.reads, self.events = 0, []

    def read(self, address, size):
        uint(address, 32, 'logical DATA address')
        if type(size) is not int or size not in (1, 2, 4): raise ValueError('strict DATA width required')
        if self.reads >= self.max_reads: raise Boundary('explicit preparation DATA budget')
        if size > 1 and address & 1: raise Boundary('odd preparation DATA read')
        bus = address & 0xFFFFFF
        if 0xFF0000 <= bus and bus + size <= 0x1000000:
            value = int.from_bytes(self.ram[bus & 65535:(bus & 65535)+size], 'big')
        else:
            value = self.data.read(bus, size)
        self.reads += 1
        self.events.append(('read', address, size, value))
        return value

    def write(self, address, size, value):
        uint(address, 32, 'logical DATA address')
        if type(size) is not int or size not in (1, 2, 4): raise ValueError('strict DATA width required')
        uint(value, size*8, 'written DATA')
        if size > 1 and address & 1: raise Boundary('odd preparation DATA write')
        bus = address & 0xFFFFFF
        if not (0xFF0000 <= bus and bus + size <= 0x1000000): raise Boundary('outside conditional writable RAM')
        self.ram[bus & 65535:(bus & 65535)+size] = value.to_bytes(size, 'big')
        self.events.append(('write', address, size, value))

    def table(self, base): return Table(self, base)
    def active_queue(self): return Cursor(self, VIEW_BASES['active_queue'])
    def pair_queue(self): return Cursor(self, VIEW_BASES['pair_queue'])
    def divide_unsigned(self, numerator, denominator): return divu_retained(numerator, denominator)
    def increment_queue_counter(self, amount):
        uint(amount, 16, 'queue increment')
        self.set_queue_counter(u16(self.queue_counter() + amount))

    def carry_result(self, value):
        if type(value) is not int or value not in (0, 1): raise ValueError('explicit carry 0/1 required')
        if not self.sr & 0x2000: raise Boundary('original SR instruction requires supervisor')
        if self.sr & 0x8000: raise Boundary('original trace continuation not modeled')
        self.sr = (self.sr & 65534) | value
        return CarryOutcome(value, self.sr)

    def supervisor_carry(self, value):
        if type(value) is not bool: raise ValueError('strict conditional carry bool required')
        return self.carry_result(int(value))

    def complete_carry(self, value): return self.carry_result(value)
    def set_carry(self, value): return self.supervisor_carry(value)


def _view_property(name):
    return property(lambda self: (Cursor if name in ('selected_roster','average_roster','selected_attribute_roster') else Table)(self, VIEW_BASES[name]))


def _read_scalar(name):
    return lambda self: self.read(*SCALARS[name])


def _write_scalar(name):
    address, size = SCALARS[name]
    return lambda self, value: self.write(address, size, uint(value, size*8))


for _name in VIEW_BASES:
    if _name not in ('active_queue', 'pair_queue'):
        setattr(PreparationState, _name, _view_property(_name))
for _name in SCALARS:
    setattr(PreparationState, _name, _read_scalar(_name))
    setattr(PreparationState, 'set_' + _name, _write_scalar(_name))

BattleState = PreparationState
CarryEffect = CarryOutcome


class Table:
    def __init__(self, state, base):
        if type(state) is not PreparationState: raise ValueError('typed preparation state required')
        self.state, self.base = state, uint(base, 32, 'view base')
    def address(self, offset=0, disp=0):
        uint(offset, 16, 'signed WORD offset')
        if type(disp) is not int or not -32768 <= disp <= 32767: raise ValueError('strict displacement required')
        return u32(self.base + s16(offset) + disp)
    def byte(self, offset=0, displacement=0): return self.state.read(self.address(offset, displacement), 1)
    def word(self, offset=0, displacement=0): return self.state.read(self.address(offset, displacement), 2)
    def long(self, offset=0, displacement=0): return self.state.read(self.address(offset, displacement), 4)
    def set_byte(self, offset, value, displacement=0): self.state.write(self.address(offset, displacement), 1, uint(value, 8))
    def set_word(self, offset, value, displacement=0): self.state.write(self.address(offset, displacement), 2, uint(value, 16))
    def set_long(self, offset, value, displacement=0): self.state.write(self.address(offset, displacement), 4, uint(value, 32))
    def at(self, offset=0, disp=0): return type(self)(self.state, self.address(offset, disp))
    def advance(self, amount):
        if type(amount) is not int or not -0x80000000 <= amount <= 0x7FFFFFFF: raise ValueError('signed LONG advance required')
        return type(self)(self.state, u32(self.base + amount))
    def advance_lowword(self, amount): return type(self)(self.state, replace_word(self.base, u16(low16(self.base)+uint(amount,16))))
    def cursor(self, offset=0): return Cursor(self.state, self.address(offset))


class Cursor(Table):
    def next_byte(self):
        value = self.byte(); self.base = u32(self.base + 1); return value
    def next_word(self):
        value = self.word(); self.base = u32(self.base + 2); return value
    def append_byte(self, value):
        self.set_byte(0, value); self.base = u32(self.base + 1)
    def clear_next_byte(self):
        self.set_byte(0, 0); self.base = u32(self.base + 1)
    def write_relative(self, delta, value):
        if type(delta) is not int or not -32768 <= delta <= 32767: raise ValueError('strict relative displacement required')
        self.state.write(u32(self.base + delta), 1, uint(value, 8))
    def copy_next_byte_relative(self, delta):
        value = self.next_byte(); self.write_relative(delta, value); return value
