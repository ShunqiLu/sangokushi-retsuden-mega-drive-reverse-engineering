"""Live debt-record data ports; addresses are compatibility, not business names."""
from tools.high_level_city_event.domain import uint, u16, u32, s16, negative_byte, Boundary


def low8(value):
    return u16(value) & 255


def update_flag(value, bit, mode):
    value = uint(value, 16, 'flag WORD')
    bit = uint(bit, 16, 'record index WORD') & 31
    if type(mode) is not str or mode not in ('clear', 'set'):
        raise ValueError('explicit clear/set policy required')
    return u16(value & ~(1 << bit) if mode == 'clear' else value | (1 << bit))


class DebtState:
    def __init__(self, ram, *, max_reads=1000000):
        if type(ram) is not bytearray or len(ram) != 65536:
            raise ValueError('live 64-KiB RAM bytearray required')
        uint(max_reads, 32, 'read budget')
        if max_reads == 0:
            raise ValueError('positive explicit read budget required')
        self.ram, self.max_reads, self.reads, self.events = ram, max_reads, 0, []

    def read(self, address, size):
        if type(address) is not int or type(size) is not int or size not in (1, 2, 4):
            raise ValueError('typed read address and size required')
        uint(address, 32, '32-bit read address')
        if self.reads >= self.max_reads:
            raise Boundary('explicit data read budget exhausted')
        if size > 1 and address & 1:
            raise Boundary('odd WORD/LONG read')
        bus = address & 0xFFFFFF
        if not 0xFF0000 <= bus <= 0xFFFFFF - size + 1:
            raise Boundary('outside live conditional RAM read')
        value = int.from_bytes(self.ram[bus & 65535:(bus & 65535) + size], 'big')
        self.reads += 1
        self.events.append(('read', u32(address), size, value))
        return value

    def write(self, address, size, value):
        if type(address) is not int or type(size) is not int or size not in (1, 2, 4):
            raise ValueError('typed write address and size required')
        uint(address, 32, '32-bit write address')
        uint(value, size * 8)
        bus = address & 0xFFFFFF
        if (size > 1 and address & 1) or not 0xFF0000 <= bus <= 0xFFFFFF - size + 1:
            raise Boundary('outside/alignment conditional RAM write')
        self.ram[bus & 65535:(bus & 65535) + size] = value.to_bytes(size, 'big')
        self.events.append(('write', u32(address), size, value))

    def records_reverse(self):
        return Records(self, 0xFFFFEA34)

    def records_forward(self):
        return Records(self, 0xFFFFE9F8)

    def owners(self):
        return Owners(self)

    def principals(self):
        return Principals(self)

    def selected_word(self):
        return self.read(0xFFFFF3A8, 2)

    def flags(self):
        return self.read(0xFFFFE700, 2)

    def store_flags(self, value):
        self.write(0xFFFFE700, 2, uint(value, 16))


class Records:
    def __init__(self, state, cursor):
        self.state, self.cursor = state, cursor

    def first_city(self):
        return self.state.read(self.cursor, 1)

    def second_city(self):
        return self.state.read(u32(self.cursor + 1), 1)

    def clear(self):
        self.state.write(self.cursor, 4, 0)

    def reverse_slots(self, count):
        uint(count, 16, 'explicit loop count')
        for slot in range(count - 1, -1, -1):
            yield slot
            self.cursor = u32(self.cursor - 4)

    def forward_slots(self, count):
        uint(count, 16, 'explicit loop count')
        for slot in range(count):
            yield slot
            self.cursor = u32(self.cursor + 4)


class Owners:
    def __init__(self, state):
        self.state = state

    def read(self, city):
        uint(city, 16, 'city WORD offset')
        return self.state.read(u32(0xFFFFF427 + s16(city)), 1)


class Principals:
    def __init__(self, state):
        self.state = state

    def clear(self, offset):
        uint(offset, 16, 'principal WORD offset')
        self.state.write(u32(0xFFFFE65C + s16(offset)), 4, 0)
