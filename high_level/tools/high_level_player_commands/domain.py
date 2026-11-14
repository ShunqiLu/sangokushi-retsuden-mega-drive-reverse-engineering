"""Live, fixed-width player-command data and explicitly supplied readonly resources.

Business functions use named tables, scalar ports and family-local contexts.
This boundary owns address arithmetic, bus alignment and ordered DATA events;
it is not an instruction interpreter and never opens a ROM or asset file.
"""
from dataclasses import dataclass
from typing import NewType


Byte = NewType('Byte', int)
Word = NewType('Word', int)
Long = NewType('Long', int)


class Boundary(ValueError):
    """An explicit original-data or finite-model boundary, not a fake return."""


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
    """Packed remainder/quotient; overflow retains the original dividend.

    Full architectural overflow flags are outside this scalar projection.
    A zero divisor stops after preceding DATA; it is never replaced by one.
    """
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


@dataclass(frozen=True)
class RandomSample:
    """Declared original RNG results, not a CPU register collection."""
    sample: Long
    updated_state: Long

    def __post_init__(self):
        uint(self.sample, 32)
        uint(self.updated_state, 32)


class ReadOnlyData:
    """One explicit edit authority for each nonoverlapping physical segment."""

    def __init__(self, segments=()):
        if type(segments) is not tuple:
            raise ValueError('explicit readonly segment tuple required')
        rows = []
        for item in segments:
            if type(item) is not tuple or len(item) != 2:
                raise ValueError('(base,bytes) required')
            base, raw = item
            uint(base, 32)
            if (type(raw) is not bytes or not raw
                    or base + len(raw) > 0x1000000):
                raise ValueError('nonempty 24bit segment required')
            rows.append((base, raw))
        rows.sort()
        if any(base + len(raw) > following
               for (base, raw), (following, _) in zip(rows, rows[1:])):
            raise ValueError('competing readonly authorities')
        self.segments = tuple(rows)

    def read(self, address, size):
        uint(address, 32)
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('strict DATA width required')
        for base, raw in self.segments:
            if base <= address and address + size <= base + len(raw):
                start = address - base
                return int.from_bytes(raw[start:start + size], 'big')
        raise Boundary('outside explicit readonly source')


# These named ports are populated from the accepted candidate's original
# caller/data evidence. They describe bindings, never hidden image/audio data.
VIEW_BASES = {
    'command_queue': 0xffffd100,
    'display_queue': 0xffffd100,
    'decimal_scratch': 0xffffd300,
    'training_digit_scratch': 0xffffd300,
    'amount_digits': 0xffffef00,
    'recruitment_digit_scratch': 0xffffef00,
    'selected_amount_digits': 0xffffef0c,
    'command_digit_scratch': 0xffffef0c,
    'resource_digits': 0xffffef18,
    'portrait_masks': 0xffffefb2,
    'portrait_first_bits': 0xffffef64,
    'candidate_roster': 0xfffff500,
    'command_candidates': 0xfffff500,
    'city_gold': 0xffffdffc,
    'city_food': 0xffffe09c,
    'recruitment_source': 0xffffe13c,
    'recruitment_pool': 0xffffe774,
    'officer_troops': 0xffffc800,
    'officer_march_speed': 0xffffc400,
    'portrait_pair_catalog': 0xd4d22,
    'portrait_part_masks': 0xd4d2f,
    'decimal_digit_catalog': 0x12782,
    'command_price_records': 0x12840,
    'amount_place_thresholds': 0x12500,
    'amount_value_steps': 0x124fc,
    'amount_cost_steps': 0x12514,
    'command_value_steps': 0x1344c,
    'command_row_label': 0x12248,
    'budget_place_label': 0x125d0,
    'amount_place_highlight': 0x12a90,
    'percentage_place_highlight': 0x12cb6,
    'amount_cursor_shape': 0x12a90,
    'equipment_category_cursor_shape': 0x13c1c,
    'training_cursor_shape': 0x13fdc,
    'training_point_steps': 0x13f66,
    'training_cost_steps': 0xfffff74e,
    'city_world_positions': 0xd4ac6,
    'group_records': 0xffff9000,
    'route_candidate_list': 0xffff9f00,
    'route_direction_bytes': 0xff3800,
    'selection_members': 0xff3930,
    'sprite_entries': 0xfffff800,
    'adjacent_group_offsets': 0xffffefbe,
    'group_member_scratch': 0xfffff65c,
    'officer_capacity': 0xffffb000,
    'officer_readiness': 0xffffb200,
    'city_locations': 0xffffce9c,
    'city_owner_bytes': 0xfffff428,
    'force_relationship_bits': 0xffffe710,
    'terrain_cells': 0xee5f0,
    'terrain_costs': 0x670a,
    'route_cursor_shape': 0x14150,
    'candidate_cursor_shape': 0x14956,
    'world_command_records': 0xff3000,
}
SCALARS = {
    'active_descriptor': (0xff382c, 4),
    'command_queue_offset': (0xfffff31a, 2),
    'queue_offset': (0xfffff31a, 2),
    'display_flags_BYTE': (0xfffff321, 1),
    'ui_gate_flags': (0xfffff321, 1),
    'held_controls_BYTE': (0xfffff602, 1),
    'controller_held': (0xfffff602, 1),
    'held_controls_WORD': (0xfffff602, 2),
    'pressed_controls_BYTE': (0xfffff603, 1),
    'controller_edges': (0xfffff603, 1),
    'repeat_timer': (0xfffff608, 2),
    'controller_repeat': (0xfffff608, 2),
    'command_sound': (0xfffff612, 2),
    'ui_state': (0xfffff362, 2),
    'command_id': (0xfffff362, 2),
    'current_city': (0xfffff364, 2),
    'command_city': (0xfffff364, 2),
    'return_ui_state': (0xfffff36a, 2),
    'command_message': (0xfffff38c, 2),
    'amount_place': (0xfffff39a, 2),
    'amount_digit_position': (0xfffff39a, 2),
    'amount_blink_timer': (0xfffff39c, 2),
    'cursor_blink_counter': (0xfffff39c, 2),
    'committed_amount': (0xfffff39e, 4),
    'action_amount': (0xfffff39e, 4),
    'display_flags_WORD': (0xfffff3a4, 2),
    'portrait_flags_BYTE': (0xfffff3a4, 1),
    'queue_dirty_flags': (0xfffff3a4, 1),
    'percentage_value': (0xfffff3b6, 2),
    'percentage_place': (0xfffff3b8, 2),
    'cost_amount': (0xfffff3ba, 4),
    'training_cost': (0xfffff3ba, 4),
    'recruitment_input': (0xfffff3e4, 4),
    'recruitment_capacity': (0xfffff3e8, 4),
    'recruitment_digit_start': (0xfffff3ec, 2),
    'equipment_input': (0xfffff3ee, 4),
    'command_row': (0xfffff3f0, 2),
    'selected_amount': (0xfffff3f4, 4),
    'amount_limit': (0xfffff3f8, 4),
    'training_cost_limit': (0xfffff3f8, 4),
    'amount_maximum_place': (0xfffff3fc, 2),
    'equipment_category': (0xfffff688, 2),
    'special_equipment_amount': (0xffffcfae, 4),
    'training_points': (0xfffff670, 2),
    'training_mean_speed': (0xfffff672, 2),
    'training_origin_y': (0xff3822, 2),
    'training_origin_x': (0xff3824, 2),
    'training_origin_packed': (0xff3828, 2),
    'selected_count': (0xff382a, 2),
    'training_selected_count': (0xff382a, 2),
    'controller_pair': (0xfffff602, 2),
    'training_cost_step_ones': (0xfffff74e, 4),
    'training_cost_step_tens': (0xfffff752, 4),
    'training_cost_step_hundreds': (0xfffff756, 4),
    'sprite_count': (0xfffff300, 1),
    'clip_min_x': (0xfffff302, 2),
    'clip_max_x': (0xfffff304, 2),
    'clip_min_y': (0xfffff306, 2),
    'clip_max_y': (0xfffff308, 2),
    'scroll_x': (0xfffff60a, 2),
    'scroll_y': (0xfffff60e, 2),
    'map_scroll_x': (0xfffff314, 2),
    'map_scroll_y': (0xfffff318, 2),
    'route_first_member': (0xfffff35e, 2),
    'route_second_member': (0xfffff360, 2),
    'remaining_move_budget': (0xfffff674, 2),
    'selected_candidate_index': (0xfffff676, 2),
    'selected_scene': (0xfffff68a, 2),
    'route_step_count': (0xff3820, 2),
    'route_row_coordinate': (0xff3822, 2),
    'route_column_coordinate': (0xff3824, 2),
    'world_command_offset': (0xff3826, 2),
    'selected_world_x': (0xff3bb6, 2),
    'selected_world_y': (0xff3bb8, 2),
    'pending_world_x': (0xff3bba, 2),
    'pending_world_y': (0xff3bbc, 2),
    'adjacent_count_tick': (0xff3bb2, 2),
    'candidate_member_count': (0xfffff636, 2),
    'saved_scroll_x': (0xfffff356, 2),
    'saved_scroll_y': (0xfffff354, 2),
    'world_aux_flag': (0xfffff772, 2),
}


class GameState:
    def __init__(self, ram, *, data=None, max_reads=1000000, sr=0x2700):
        if type(ram) is not bytearray or len(ram) != 65536:
            raise ValueError('explicit live64KiB RAM required')
        if data is None:
            data = ReadOnlyData()
        if type(data) is not ReadOnlyData:
            raise ValueError('typed readonly DATA required')
        uint(max_reads, 32)
        uint(sr, 16)
        if max_reads == 0:
            raise ValueError('positive DATA budget required')
        self.ram, self.data, self.max_reads, self.sr = ram, data, max_reads, sr
        self.reads, self.events = 0, []

    def read(self, address, size):
        uint(address, 32)
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('strict DATA width required')
        if self.reads >= self.max_reads:
            raise Boundary('explicit player-command DATA budget')
        if size > 1 and address & 1:
            raise Boundary('odd DATA read')
        bus = address & 0xFFFFFF
        if 0xFF0000 <= bus and bus + size <= 0x1000000:
            start = bus & 65535
            value = int.from_bytes(self.ram[start:start + size], 'big')
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
            raise Boundary('odd DATA write')
        bus = address & 0xFFFFFF
        if not 0xFF0000 <= bus or bus + size > 0x1000000:
            raise Boundary('outside writable RAM')
        start = bus & 65535
        self.ram[start:start + size] = value.to_bytes(size, 'big')
        self.events.append(('write', address, size, value))

    def table(self, base):
        return Table(self, base)

    def checked_table(self, value):
        return checked_table(value, self)

    def checked_cursor(self, value):
        return checked_cursor(value, self)

    def scalar(self, name):
        """Read one named scalar at its declared original width."""
        if type(name) is not str or name not in SCALARS:
            raise ValueError('declared player-command scalar required')
        address, size = SCALARS[name]
        return self.read(address, size)

    def set_scalar(self, name, value):
        """Write one named scalar, sharing storage with all live views."""
        if type(name) is not str or name not in SCALARS:
            raise ValueError('declared player-command scalar required')
        address, size = SCALARS[name]
        self.write(address, size, uint(value, size * 8))

    def append_command_label(self, source, x, y, style=0):
        from .business_display import append_live_command_string_words
        return append_live_command_string_words(self, source, x, y, style)

    def add_selected_cost(self):
        from .business_reuse import add_selected_cost
        return add_selected_cost(self)

    def carry_result(self, value):
        if type(value) is not int or value not in (0, 1):
            raise ValueError('strict carry0/1 required')
        if not self.sr & 0x2000:
            raise Boundary('original full-SR operation requires supervisor')
        if self.sr & 0x8000:
            raise Boundary('trace continuation not modeled')
        self.sr = (self.sr & 65534) | value
        return CarryOutcome(value, self.sr)

    def carry_observed(self, value):
        if type(value) is not int or value not in (0, 1):
            raise ValueError('strict observed carry required')
        return CarryOutcome(value, (self.sr & 65534) | value)

    def set_carry(self, value):
        if type(value) is not bool:
            raise ValueError('strict carry bool required')
        return self.carry_result(int(value))


class Table:
    def __init__(self, state, base):
        checked_state(state)
        self.state, self.base = state, uint(base, 32)

    def address(self, offset=0, displacement=0):
        uint(offset, 16)
        if type(displacement) is not int or not -32768 <= displacement <= 32767:
            raise ValueError('signed displacement required')
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
    if type(value) is not GameState:
        raise ValueError('typed player-command GameState required')
    return value


def checked_table(value, state=None):
    if type(value) not in (Table, Cursor):
        raise ValueError('typed live Table/Cursor required')
    checked_state(value.state)
    uint(value.base, 32)
    if state is not None and value.state is not state:
        raise ValueError('view must share live state')
    return value


def checked_cursor(value, state=None):
    if type(value) is not Cursor:
        raise ValueError('typed live Cursor required')
    return checked_table(value, state)


def read_packed_long(view, offset):
    """Four original BYTE reads, including unaligned packed object fields."""
    checked_table(view)
    uint(offset, 16)
    value = view.byte(offset)
    value = u32((value << 8) | view.byte(offset, 1))
    value = u32((value << 8) | view.byte(offset, 2))
    return u32((value << 8) | view.byte(offset, 3))


def store_packed_long_reverse(view, offset, value):
    """Original least-significant BYTE first; keep live alias side effects."""
    checked_table(view)
    uint(offset, 16)
    uint(value, 32)
    view.set_byte(offset, low8(value), 3)
    view.set_byte(offset, low8(value >> 8), 2)
    view.set_byte(offset, low8(value >> 16), 1)
    view.set_byte(offset, low8(value >> 24))


for _name, _base in VIEW_BASES.items():
    setattr(GameState, _name, property(lambda self, base=_base: Table(self, base)))
for _name, (_address, _size) in SCALARS.items():
    setattr(GameState, _name,
            lambda self, address=_address, size=_size: self.read(address, size))
    setattr(GameState, 'set_' + _name,
            lambda self, value, address=_address, size=_size:
            self.write(address, size, uint(value, size * 8)))
