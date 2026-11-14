"""Live storage boundary shared by save, restore and bit-stream logic.

The explicit 8 KiB cartridge backing is separate from main RAM. The selected
original routines access only odd BYTE lanes with a two-byte CPU stride; the
MAME duplicated-file container is not this bus. Mapping/read/write permissions
are caller-supplied preconditions, not emulation of unselected cartridge MMIO.
No files, original ROM images, CPU instruction interpreter or asset payloads
are loaded here. All successful business DATA accesses share one event order.
"""
from dataclasses import dataclass
from typing import NewType

Byte = NewType('Byte', int)
Word = NewType('Word', int)
Long = NewType('Long', int)


class Boundary(ValueError):
    """Original-data or finite-model stop; never a fake successful return."""


def uint(value, bits, name='value'):
    if (type(bits) is not int or bits not in (8, 16, 32)
            or type(value) is not int or not 0 <= value < 1 << bits):
        raise ValueError(f'strict {bits}-bit {name} required')
    return value


def u8(value):
    if type(value) is not int:
        raise ValueError('integer BYTE arithmetic required')
    return value & 255


def u16(value):
    if type(value) is not int:
        raise ValueError('integer WORD arithmetic required')
    return value & 65535


def u32(value):
    if type(value) is not int:
        raise ValueError('integer LONG arithmetic required')
    return value & 0xFFFFFFFF


def s8(value):
    value = uint(value, 8)
    return value - 256 if value & 128 else value


def s16(value):
    value = uint(value, 16)
    return value - 65536 if value & 32768 else value


def low8(value):
    return u8(value)


def low16(value):
    return u16(value)


def high16(value):
    return uint(value, 32) >> 16


def replace_byte(value, byte):
    return (uint(value, 32) & 0xFFFFFF00) | uint(byte, 8)


def replace_word(value, word):
    return (uint(value, 32) & 0xFFFF0000) | uint(word, 16)


def swap_words(value):
    value = uint(value, 32)
    return u32((value << 16) | (value >> 16))


def negative_byte(value):
    return bool(uint(value, 8) & 128)


def negative_word(value):
    return bool(uint(value, 16) & 32768)


def negative_long(value):
    return bool(uint(value, 32) & 0x80000000)


def descending_inclusive(counter):
    uint(counter, 16)
    yield from range(counter, -1, -1)


def divu_retained(numerator, denominator):
    """Original packed WORD quotient/remainder; overflow retains dividend."""
    uint(numerator, 32)
    uint(denominator, 16)
    if denominator == 0:
        raise Boundary('original DIVU divide by zero after preceding DATA')
    quotient, remainder = divmod(numerator, denominator)
    return numerator if quotient > 65535 else (remainder << 16) | quotient


@dataclass(frozen=True)
class CarryOutcome:
    carry: int
    conditional_sr: Word

    def __post_init__(self):
        if type(self.carry) is not int or self.carry not in (0, 1):
            raise ValueError('strict carry0/1 required')
        uint(self.conditional_sr, 16)


class SaveImage:
    """Explicit, live logical SRAM backing with supplied mapping permissions."""

    def __init__(self, backing, *, readable=True, writable=True):
        if type(backing) is not bytearray or len(backing) != 8192:
            raise ValueError('one explicit live 8 KiB logical SRAM required')
        if type(readable) is not bool or type(writable) is not bool:
            raise ValueError('explicit Boolean cartridge permissions required')
        self.backing, self.readable, self.writable = backing, readable, writable

    def offset(self, bus, size):
        if size != 1 or not bus & 1 or not 0x200001 <= bus <= 0x203FFF:
            raise Boundary('outside declared odd-BYTE cartridge SRAM lanes')
        return (bus - 0x200001) // 2

    def read(self, bus, size):
        index = self.offset(bus, size)
        if not self.readable:
            raise Boundary('cartridge SRAM read mapping not supplied')
        return self.backing[index]

    def write(self, bus, size, value):
        index = self.offset(bus, size)
        if not self.writable:
            raise Boundary('cartridge SRAM write mapping not supplied')
        self.backing[index] = uint(value, 8)


class ReadOnlyData:
    """Explicit nonoverlapping numeric parameter segments, never hidden ROM IO."""

    def __init__(self, segments=()):
        if type(segments) is not tuple:
            raise ValueError('explicit readonly segment tuple required')
        rows = []
        for item in segments:
            if type(item) is not tuple or len(item) != 2:
                raise ValueError('(base,bytes) required')
            base, raw = item
            uint(base, 32)
            if type(raw) is not bytes or not raw or base + len(raw) > 0x1000000:
                raise ValueError('nonempty 24-bit numeric segment required')
            rows.append((base, raw))
        rows.sort()
        if any(base + len(raw) > following
               for (base, raw), (following, _) in zip(rows, rows[1:])):
            raise ValueError('competing readonly source authorities')
        self.segments = tuple(rows)

    def read(self, address, size):
        for base, raw in self.segments:
            if base <= address and address + size <= base + len(raw):
                start = address - base
                return int.from_bytes(raw[start:start + size], 'big')
        raise Boundary('outside explicit readonly numeric source')


# Stable neutral names avoid inventing meanings for unresolved schema fields.
# Every ram_* view is live and can intentionally alias scratch/other views.
VIEW_BASES = {
    'ram_9000': 0xFFFF9000,
    'ram_a000': 0xFFFFA000, 'ram_a028': 0xFFFFA028,
    'ram_a050': 0xFFFFA050, 'ram_a150': 0xFFFFA150,
    'ram_b200': 0xFFFFB200, 'ram_b400': 0xFFFFB400,
    'ram_b600': 0xFFFFB600, 'ram_b800': 0xFFFFB800,
    'ram_be00': 0xFFFFBE00, 'ram_c000': 0xFFFFC000,
    'ram_c200': 0xFFFFC200, 'ram_c300': 0xFFFFC300,
    'ram_c400': 0xFFFFC400, 'ram_c500': 0xFFFFC500,
    'ram_c700': 0xFFFFC700, 'ram_c800': 0xFFFFC800,
    'ram_cc00': 0xFFFFCC00, 'ram_cd00': 0xFFFFCD00,
    'ram_ce00': 0xFFFFCE00, 'ram_d300': 0xFFFFD300,
    'ram_d310': 0xFFFFD310, 'ram_d320': 0xFFFFD320,
    'ram_d330': 0xFFFFD330, 'ram_d350': 0xFFFFD350,
    'ram_d3a0': 0xFFFFD3A0, 'ram_d3f0': 0xFFFFD3F0,
    'ram_d440': 0xFFFFD440, 'ram_d490': 0xFFFFD490,
    'ram_d500': 0xFFFFD500, 'ram_e000': 0xFFFFE000,
    'ram_e0a0': 0xFFFFE0A0, 'ram_e140': 0xFFFFE140,
    'ram_e1e0': 0xFFFFE1E0, 'ram_e280': 0xFFFFE280,
    'ram_e320': 0xFFFFE320, 'ram_e3c0': 0xFFFFE3C0,
    'ram_e5a0': 0xFFFFE5A0, 'ram_e640': 0xFFFFE640,
    'ram_e660': 0xFFFFE660, 'ram_e700': 0xFFFFE700,
    'ram_e710': 0xFFFFE710, 'ram_e778': 0xFFFFE778,
    'ram_e818': 0xFFFFE818, 'ram_e9f8': 0xFFFFE9F8,
    'ram_ea38': 0xFFFFEA38, 'ram_ea88': 0xFFFFEA88,
    'ram_ed88': 0xFFFFED88, 'ram_ee28': 0xFFFFEE28,
    'ram_efaa': 0xFFFFEFAA, 'ram_f428': 0xFFFFF428,
    'ram_f460': 0xFFFFF460, 'ram_f590': 0xFFFFF590,
    'field_masks': 0x929A,
    'transport_orders': 0xFFFFCE00,
    'packed_groups': 0xFFFF9000,
    'save_bitwidth_masks': 0x929A,
    'saved_header': 0x200105,
    'saved_checksum': 0x20010D,
    'saved_payload': 0x200115,
    'saved_game_fields': 0x200127,
    'saved_metadata': 0x200115,
    # Load names alias these same physical views; no second backing/edit owner.
    'city_owner_tokens': 0xFFFFA000,
    'city_state_a028': 0xFFFFA028,
    'officer_city_tokens': 0xFFFFA050,
    'officer_positions': 0xFFFFA150,
    'position_x_stage': 0xFFFFD300,
    'position_y_stage': 0xFFFFD500,
    'officer_readiness': 0xFFFFB200,
    'officer_resolve': 0xFFFFB400,
    'officer_strength': 0xFFFFB600,
    'officer_parameter_b800': 0xFFFFB800,
    'officer_ability': 0xFFFFC000,
    'officer_progress': 0xFFFFBE00,
    'officer_disposition': 0xFFFFC200,
    'officer_loyalty': 0xFFFFC300,
    'officer_group_attribute': 0xFFFFC400,
    'officer_training': 0xFFFFC500,
    'officer_status': 0xFFFFC700,
    'officer_troops': 0xFFFFC800,
    'officer_city_assignment': 0xFFFFCC00,
    'officer_actions': 0xFFFFCD00,
    'city_gold': 0xFFFFE000,
    'city_food': 0xFFFFE0A0,
    'city_parameter_e140': 0xFFFFE140,
    'city_parameter_e1e0': 0xFFFFE1E0,
    'city_parameter_e280': 0xFFFFE280,
    'city_parameter_e320': 0xFFFFE320,
    'city_parameter_e3c0': 0xFFFFE3C0,
    'city_parameter_e5a0': 0xFFFFE5A0,
    'city_owner_bytes': 0xFFFFF428,
    'force_heads': 0xFFFFE640,
    'city_heads': 0xFFFFF460,
    'force_relationships': 0xFFFFE660,
    'force_link_bytes': 0xFFFFE700,
    'force_state_bytes': 0xFFFFE710,
    'city_parameter_e778': 0xFFFFE778,
    'city_order_actor_stage': 0xFFFFD300,
    'city_order_quantity_stage': 0xFFFFD350,
    'city_order_welfare_actor_stage': 0xFFFFD3A0,
    'city_order_welfare_quantity_stage': 0xFFFFD3F0,
    'city_order_transport_actor_stage': 0xFFFFD440,
    'city_order_transport_quantity_stage': 0xFFFFD490,
    'city_orders': 0xFFFFE818,
    'force_column_first': 0xFFFFD300,
    'force_column_second': 0xFFFFD310,
    'force_column_third': 0xFFFFD320,
    'force_column_fourth': 0xFFFFD330,
    'force_records': 0xFFFFE9F8,
    'city_parameter_ea38': 0xFFFFEA38,
    'officer_equipment': 0xFFFFEA88,
    'city_battle_gold': 0xFFFFED88,
    'city_battle_food': 0xFFFFEE28,
    'force_parameter_f590': 0xFFFFF590,
    'loaded_state_bytes': 0xFFFFEFAA,
    'group_records': 0xFFFF9000,
}
SCALARS = {
    'metadata_f67b': (0xFFFFF67B, 1),
    'metadata_f67d': (0xFFFFF67D, 1),
    'metadata_f67f': (0xFFFFF67F, 1),
    'metadata_f374': (0xFFFFF374, 1),
    'metadata_f375': (0xFFFFF375, 1),
    'metadata_efd3': (0xFFFFEFD3, 1),
    'metadata_efe5': (0xFFFFEFE5, 1),
    'metadata_efd7': (0xFFFFEFD7, 1),
    'metadata_efd9': (0xFFFFEFD9, 1),
    'metadata_f67a_word': (0xFFFFF67A, 2),
    'metadata_f67c_word': (0xFFFFF67C, 2),
    'metadata_f67e_word': (0xFFFFF67E, 2),
    'metadata_efd2_word': (0xFFFFEFD2, 2),
    'metadata_efe4_word': (0xFFFFEFE4, 2),
    'metadata_efd6_word': (0xFFFFEFD6, 2),
    'metadata_efd8_word': (0xFFFFEFD8, 2),
    'deployment_queue_head': (0xFF3000, 2),
    'restored_load_marker': (0xFFFFF776, 2),
    'restore_counter': (0xFFFFAFFE, 2),
    'visible_force_first': (0xFFFFF67A, 2),
    'visible_force_first_low': (0xFFFFF67B, 1),
    'visible_force_second': (0xFFFFF67C, 2),
    'visible_force_second_low': (0xFFFFF67D, 1),
    'visible_force_third': (0xFFFFF67E, 2),
    'visible_force_third_low': (0xFFFFF67F, 1),
    'year_high_byte': (0xFFFFF374, 1),
    'year_low_byte': (0xFFFFF375, 1),
    'scenario_selector': (0xFFFFEFD2, 2),
    'scenario_selector_low': (0xFFFFEFD3, 1),
    'loaded_field_efe4': (0xFFFFEFE4, 2),
    'loaded_field_efe4_low': (0xFFFFEFE5, 1),
    'calendar_field_efd6': (0xFFFFEFD6, 2),
    'calendar_field_efd6_low': (0xFFFFEFD7, 1),
    'calendar_field_efd8': (0xFFFFEFD8, 2),
    'calendar_field_efd8_low': (0xFFFFEFD9, 1),
    'loaded_queue_head': (0xFF3000, 2),
    'loaded_flag_f776': (0xFFFFF776, 2),
    'loaded_generation': (0xFFFFAFFE, 2),
}


class StorageState:
    """Shared active main RAM, cartridge SRAM and externally supplied masks."""

    def __init__(self, ram, save, data=None, *, max_reads=1000000, sr=0x2700):
        if type(ram) is not bytearray or len(ram) != 65536:
            raise ValueError('one explicit live 64 KiB main RAM required')
        if type(save) is not SaveImage:
            raise ValueError('explicit typed cartridge SaveImage required')
        if data is None:
            data = ReadOnlyData()
        if type(data) is not ReadOnlyData:
            raise ValueError('typed readonly numeric data required')
        uint(max_reads, 32)
        uint(sr, 16)
        if max_reads == 0:
            raise ValueError('positive finite DATA budget required')
        self.ram, self.save, self.data = ram, save, data
        self.max_reads, self.sr, self.reads, self.events = max_reads, sr, 0, []

    def read(self, address, size):
        uint(address, 32)
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('strict DATA width required')
        if self.reads >= self.max_reads:
            raise Boundary('explicit storage DATA budget')
        if size > 1 and address & 1:
            raise Boundary('odd WORD/LONG DATA read')
        bus = address & 0xFFFFFF
        if 0xFF0000 <= bus and bus + size <= 0x1000000:
            start = bus & 65535
            value = int.from_bytes(self.ram[start:start + size], 'big')
        elif 0x200000 <= bus < 0x204000:
            value = self.save.read(bus, size)
        else:
            value = self.data.read(bus, size)
        self.reads += 1
        self.events.append(('read', address, size, value))
        return value

    def write(self, address, size, value):
        uint(address, 32)
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('strict DATA width required')
        uint(value, size * 8)
        if size > 1 and address & 1:
            raise Boundary('odd WORD/LONG DATA write')
        bus = address & 0xFFFFFF
        if 0xFF0000 <= bus and bus + size <= 0x1000000:
            start = bus & 65535
            self.ram[start:start + size] = value.to_bytes(size, 'big')
        elif 0x200000 <= bus < 0x204000:
            self.save.write(bus, size, value)
        else:
            raise Boundary('outside declared writable RAM/SRAM')
        self.events.append(('write', address, size, value))

    def table(self, base):
        return Table(self, base)

    def scalar(self, name):
        if type(name) is not str or name not in SCALARS:
            raise ValueError('declared storage scalar required')
        address, size = SCALARS[name]
        return self.read(address, size)

    def set_scalar(self, name, value):
        if type(name) is not str or name not in SCALARS:
            raise ValueError('declared storage scalar required')
        address, size = SCALARS[name]
        self.write(address, size, uint(value, size * 8))

    def __getattr__(self, name):
        if name in VIEW_BASES:
            return self.table(VIEW_BASES[name])
        raise AttributeError(name)

    def carry_result(self, value):
        if type(value) is not int or value not in (0, 1):
            raise ValueError('strict carry0/1 required')
        if not self.sr & 0x2000:
            raise Boundary('original full-SR operation requires supervisor')
        if self.sr & 0x8000:
            raise Boundary('trace continuation not modeled')
        self.sr = (self.sr & 65534) | value
        return CarryOutcome(value, self.sr)


class Table:
    """A live view; indexed offsets use original signed WORD addressing."""

    def __init__(self, state, base):
        checked_state(state)
        self.state, self.base = state, uint(base, 32)

    def address(self, offset=0, displacement=0):
        uint(offset, 16)
        if type(displacement) is not int or not -32768 <= displacement <= 32767:
            raise ValueError('signed WORD displacement required')
        return u32(self.base + s16(offset) + displacement)

    def byte(self, offset=0, displacement=0):
        return self.state.read(self.address(offset, displacement), 1)

    def word(self, offset=0, displacement=0):
        return self.state.read(self.address(offset, displacement), 2)

    def long(self, offset=0, displacement=0):
        return self.state.read(self.address(offset, displacement), 4)

    def set_byte(self, offset, value, displacement=0):
        self.state.write(self.address(offset, displacement), 1, uint(value, 8))

    def set_word(self, offset, value, displacement=0):
        self.state.write(self.address(offset, displacement), 2, uint(value, 16))

    def set_long(self, offset, value, displacement=0):
        self.state.write(self.address(offset, displacement), 4, uint(value, 32))

    def at(self, offset=0, displacement=0):
        return type(self)(self.state, self.address(offset, displacement))

    def advance(self, amount):
        if type(amount) is not int or not -0x80000000 <= amount <= 0x7FFFFFFF:
            raise ValueError('signed LONG advance required')
        return type(self)(self.state, u32(self.base + amount))

    def cursor(self, offset=0):
        return Cursor(self.state, self.address(offset))


class Cursor(Table):
    def previous_byte(self):
        self.base = u32(self.base - 1)
        return self.byte()

    def previous_word(self):
        self.base = u32(self.base - 2)
        return self.word()

    def next_byte(self):
        value = self.byte()
        self.base = u32(self.base + 1)
        return value

    def next_word(self):
        value = self.word()
        self.base = u32(self.base + 2)
        return value

    def next_long(self):
        value = self.long()
        self.base = u32(self.base + 4)
        return value

    def append_byte(self, value):
        self.set_byte(0, value)
        self.base = u32(self.base + 1)

    def append_word(self, value):
        self.set_word(0, value)
        self.base = u32(self.base + 2)

    def append_long(self, value):
        self.set_long(0, value)
        self.base = u32(self.base + 4)

    def put_word(self, value):
        self.set_word(0, value)


def checked_state(value):
    if type(value) is StorageState:
        return value
    from .contexts_scene_storage import SceneStorageState
    if type(value) is SceneStorageState:
        return value.validate_bus()
    raise ValueError('typed family-local StorageState required')


def checked_table(value, state=None):
    if type(value) not in (Table, Cursor):
        raise ValueError('typed live Table/Cursor required')
    checked_state(value.state)
    if state is not None and value.state is not checked_state(state):
        raise ValueError('live view belongs to another storage state')
    return value


def checked_cursor(value, state=None):
    if type(value) is not Cursor:
        raise ValueError('typed live Cursor required')
    return checked_table(value, state)


def __getattr__(name):
    """Expose only StorageFrame lazily; the exact StorageState ABI is unchanged."""
    if name != 'StorageFrame':
        raise AttributeError('unknown storage domain interface: ' + name)
    from .contexts_storage_fields import StorageFrame
    return StorageFrame
