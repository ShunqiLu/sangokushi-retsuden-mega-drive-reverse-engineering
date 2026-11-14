"""Live fixed-width AI data boundary, not a register/PC CPU or implicit ROM reader."""
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
def negative_byte(value): return bool(uint(value, 8) & 128)
def negative_word(value): return bool(uint(value, 16) & 32768)
def negative_long(value): return bool(uint(value, 32) & 0x80000000)
def replace_byte(value, byte): return (uint(value, 32) & 0xFFFFFF00) | uint(byte, 8)
def replace_word(value, word): return (uint(value, 32) & 0xFFFF0000) | uint(word, 16)
def add_low_word(value, amount): return replace_word(value, u16(low16(value) + uint(amount, 16)))
def zero_extend_word(value): return uint(value, 16)


def descending_inclusive(counter):
    uint(counter, 16, 'inclusive countdown')
    yield from range(counter, -1, -1)


def divu_retained(numerator, denominator):
    uint(numerator, 32, 'DIVU numerator'); uint(denominator, 16, 'DIVU denominator')
    if denominator == 0: raise Boundary('original DIVU zero after preceding DATA prefix')
    quotient, remainder = divmod(numerator, denominator)
    return numerator if quotient > 65535 else (remainder << 16) | quotient


@dataclass(frozen=True)
class CarryOutcome:
    carry: int
    conditional_sr: int

    def __post_init__(self):
        if type(self.carry) is not int or self.carry not in (0, 1): raise ValueError('strict carry 0/1 required')
        uint(self.conditional_sr, 16, 'conditional SR diagnostic')


class ReadOnlyData:
    """Caller-supplied editable segments, including explicit old code/data aliases."""
    def __init__(self, segments=()):
        if type(segments) is not tuple: raise ValueError('explicit readonly segment tuple required')
        rows = []
        for item in segments:
            if type(item) is not tuple or len(item) != 2: raise ValueError('segment is (physical base, bytes)')
            base, data = item
            uint(base, 32, 'physical readonly base')
            if type(data) is not bytes or not data or base + len(data) > 0x1000000:
                raise ValueError('nonempty explicit segment within 24-bit bus required')
            rows.append((base, data))
        rows.sort()
        if any(a+len(raw)>b for (a, raw), (b, _) in zip(rows, rows[1:])): raise ValueError('competing readonly authority')
        self.segments = tuple(rows)

    def read(self, address, size):
        uint(address, 32, 'physical DATA address')
        if type(size) is not int or size not in (1, 2, 4): raise ValueError('strict readonly width required')
        for base, raw in self.segments:
            if base <= address and address + size <= base + len(raw):
                return int.from_bytes(raw[address-base:address-base+size], 'big')
        raise Boundary('outside explicitly supplied readonly DATA segments')


VIEW_BASES = {
    'roster': 0xFFFFF72A, 'officer_roster': 0xFFFFF72A,
    'b600': 0xFFFFB600, 'attributes_b600': 0xFFFFB600,
    'b400': 0xFFFFB400, 'attributes_b400': 0xFFFFB400,
    'c300': 0xFFFFC300, 'officer_status': 0xFFFFC300,
    'c000': 0xFFFFC000, 'c500': 0xFFFFC500, 'c600': 0xFFFFC600,
    'c700': 0xFFFFC700, 'c800': 0xFFFFC800, 'be00': 0xFFFFBE00,
    'officer_assignments': 0xFFFFCC00, 'officer_flags': 0xFFFFCD00,
    'city_assignments': 0xFFFFCD00, 'city_owners': 0xFFFFF427,
    'city_heads': 0xFFFFF45E, 'city_processed': 0xFFFFEA37,
    'force_heads': 0xFFFFE640, 'force_leaders': 0xFFFFE640,
    'force_masks': 0xFFFFE710, 'force_rows': 0x32660,
    'force_city_assignments': 0xFFFFF428, 'neighbors': 0xD4BDA,
    'city_balances': 0xFFFFDFFC, 'city_rice': 0xFFFFE09C,
    'order_gates': 0xFFFFE59C, 'city_orders': 0xFFFFE80C,
}
SCALARS = {
    'current_city': (0xFFFFF364, 2), 'neighbor_city': (0xFFFFF364, 2),
    'force_selector': (0xFFFFF376, 2), 'current_force': (0xFFFFF376, 2),
    'force_id': (0xFFFFF376, 2),
    'selected_city': (0xFFFFF3A8, 2), 'selected_officer': (0xFFFFF3A6, 2),
    'chosen_city': (0xFFFFF392, 2), 'command': (0xFFFFF728, 2),
    'next_state': (0xFFFFF728, 2), 'order_amount': (0xFFFFF39E, 4),
    'action_amount': (0xFFFFF39E, 4), 'roster_second': (0xFFFFF72C, 2),
    'player_first': (0xFFFFF67B, 1), 'player_second': (0xFFFFF67D, 1),
    'player_third': (0xFFFFF67F, 1), 'player_force_1': (0xFFFFF67B, 1),
    'player_force_2': (0xFFFFF67D, 1), 'player_force_3': (0xFFFFF67F, 1),
    'seed_word': (0xFFFFF61C, 2), 'seed_high_word': (0xFFFFF61C, 2),
    'seed_low_byte': (0xFFFFF61D, 1),
}


class AiState:
    def __init__(self, ram, *, data=None, max_reads=1000000, sr=0x2700):
        if type(ram) is not bytearray or len(ram) != 65536: raise ValueError('explicit live64KiB bytearray required')
        if data is None: data = ReadOnlyData()
        if type(data) is not ReadOnlyData: raise ValueError('explicit readonly data view required')
        uint(max_reads, 32, 'read budget'); uint(sr, 16, 'conditional SR')
        if max_reads == 0: raise ValueError('positive DATA budget required')
        self.ram, self.data, self.max_reads, self.sr = ram, data, max_reads, sr
        self.reads, self.events = 0, []

    def read(self, address, size):
        uint(address, 32, 'logical DATA address')
        if type(size) is not int or size not in (1, 2, 4): raise ValueError('strict DATA width required')
        if self.reads >= self.max_reads: raise Boundary('explicit AI DATA budget')
        if size > 1 and address & 1: raise Boundary('odd AI DATA read')
        bus = address & 0xFFFFFF
        if 0xFF0000 <= bus and bus + size <= 0x1000000:
            value = int.from_bytes(self.ram[bus & 65535:(bus & 65535)+size], 'big')
        else:
            value = self.data.read(bus, size)
        self.reads += 1; self.events.append(('read', address, size, value)); return value

    def write(self, address, size, value):
        uint(address, 32, 'logical DATA address')
        if type(size) is not int or size not in (1, 2, 4): raise ValueError('strict DATA width required')
        uint(value, size*8, 'written DATA')
        if size > 1 and address & 1: raise Boundary('odd AI DATA write')
        bus = address & 0xFFFFFF
        if not (0xFF0000 <= bus and bus + size <= 0x1000000): raise Boundary('outside conditional writable RAM')
        self.ram[bus & 65535:(bus & 65535)+size] = value.to_bytes(size, 'big')
        self.events.append(('write', address, size, value))

    def table(self, base): return Table(self, base)
    def seed(self): return self.read(0xFFFFF61C, 4)
    def store_seed(self, value): self.write(0xFFFFF61C, 4, uint(value, 32))
    def sample_random(self):
        from tools.high_level_city_event.arithmetic import random_sample
        return random_sample(self)
    def divide_signed(self, numerator, denominator):
        from tools.high_level_city_event.arithmetic import signed_divmod
        return signed_divmod(uint(numerator, 32), uint(denominator, 32))
    def divide_unsigned(self, numerator, denominator): return divu_retained(numerator, denominator)

    def carry_result(self, value):
        if type(value) is not int or value not in (0, 1): raise ValueError('strict carry0/1 required')
        if not self.sr & 0x2000: raise Boundary('original SR operation requires supervisor')
        if self.sr & 0x8000: raise Boundary('original trace continuation not modeled')
        self.sr = (self.sr & 65534) | value
        return CarryOutcome(value, self.sr)
    def set_carry(self, value):
        if type(value) is not bool: raise ValueError('strict carry bool required')
        return self.carry_result(int(value))


class Table:
    def __init__(self, state, base):
        if type(state) is not AiState: raise ValueError('typed AiState required')
        self.state, self.base = state, uint(base, 32, 'view base')
    def address(self, offset=0, disp=0):
        uint(offset, 16, 'signed WORD offset')
        if type(disp) is not int or not -32768 <= disp <= 32767: raise ValueError('signed displacement required')
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
    def cursor(self, offset=0): return Cursor(self.state, self.address(offset))


class Cursor(Table):
    def next_byte(self):
        value = self.byte(); self.base = u32(self.base+1); return value
    def next_word(self):
        value = self.word(); self.base = u32(self.base+2); return value
    def previous_byte(self):
        self.base = u32(self.base-1); return self.byte()
    def previous_word(self):
        self.base = u32(self.base-2); return self.word()
    def append_byte(self, value):
        self.set_byte(0, value); self.base = u32(self.base+1)
    def append_word(self, value):
        self.set_word(0, value); self.base = u32(self.base+2)


def _view(name):
    kind = Cursor if name in ('officer_roster', 'city_assignments') else Table
    return property(lambda self: kind(self, VIEW_BASES[name]))


def _scalar_reader(name):
    return lambda self: self.read(*SCALARS[name])


def _scalar_writer(name):
    address, size = SCALARS[name]
    return lambda self, value: self.write(address, size, uint(value, size*8))


for _name in VIEW_BASES: setattr(AiState, _name, _view(_name))
for _name in SCALARS:
    setattr(AiState, _name, _scalar_reader(_name))
    setattr(AiState, 'set_'+_name, _scalar_writer(_name))

CarryEffect = CarryOutcome
