"""Live, fixed-width battle data and explicitly supplied readonly resources.

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
    'battle_positions': 0xFFFFA150,
    'primary_battle_roster': 0xFFFFA550,
    'secondary_battle_roster': 0xFFFFA5A4,
    'officer_troops': 0xFFFFC800,
    'officer_readiness': 0xFFFFC300,
    'officer_march_speed': 0xFFFFC400,
    'officer_training': 0xFFFFC500,
    'officer_word_b200': 0xFFFFB200,
    'officer_word_b400': 0xFFFFB400,
    'officer_word_b600': 0xFFFFB600,
    'formation_scratch': 0xFFFFD300,
    'action_candidates': 0xFFFFD300,
    'filtered_action_candidates': 0xFFFFD400,
    'deployed_cell_pairs': 0xFFFFD310,
    'primary_formation_orders': 0xFFFFAF82,
    'secondary_formation_orders': 0xFFFFAF96,
    'scene_variant': 0xFFFF9FFF,
    'scene_primary_head': 0xFFFFA027,
    'force_rulers': 0xFFFFE640,
    'city_head_words': 0xFFFFF45E,
    'city_owner_bytes': 0xFFFFF428,
    'sort_auxiliary_ea88': 0xFFFFEA88,
    'deployed_flags': 0xFFFFAE28,
    'unit_retreat_flags': 0x00FF3BC2,
    'global_battle_positions': 0x00FF2C00,
    'selected_primary_positions': 0x00FF3EC2,
    'selected_secondary_positions': 0x00FF3ECA,
    'scene_anchor_positions': 0x000AE2F6,
    'scene_deployment_cells': 0x000ABDA8,
    'secondary_position_catalog': 0x000AD870,
    'preceding_secondary_position_catalog': 0x000AD86E,
    'primary_position_catalog': 0x000AC75E,
    'formation_directory': 0x00024BE4,
    'secondary_formation_parameters': 0x00024C00,
    'primary_formation_parameters': 0x0002546C,
    # Slot zero is live native code, not a second editable resource authority.
    'deployment_step_offsets': 0x000249F0,
    'battlefield_maps': 0x000945E8,
    'terrain_category_lookup': 0x0006C0B4,
    'radial_threshold_rows': 0x00030876,
}
SCALARS = {
    'battle_scene': (0xFFFFF68A, 2),
    'battle_primary_force': (0xFFFFF68C, 2),
    'battle_secondary_force': (0xFFFFF68E, 2),
    'primary_strength_total': (0xFFFFF69E, 4),
    'secondary_strength_total': (0xFFFFF6A2, 4),
    'battle_phase': (0xFFFFF6D6, 2),
    'battle_side_flags': (0xFFFFF6D7, 1),
    'primary_strength_limit': (0xFFFFF768, 4),
    'secondary_strength_limit': (0xFFFFF76C, 4),
    'deployment_step_mode': (0xFFFFF770, 2),
    'selected_position_1': (0xFFFFF744, 2),
    'selected_position_2': (0xFFFFF746, 2),
    'selected_position_3': (0xFFFFF748, 2),
    'seed_word': (0xFFFFF61C, 2),
    'selected_officer': (0xFFFFF3A6, 2),
    'action_amount': (0xFFFFF39E, 4),
    'route': (0xFFFFF612, 2),
    'command_step': (0xFFFFF362, 2),
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
        self._rng_seed_read = None
        self._rng_seed_written = None

    def read(self, address, size):
        uint(address, 32)
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('strict DATA width required')
        if self.reads >= self.max_reads:
            raise Boundary('explicit battle DATA budget')
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
            raise ValueError('declared battle scalar required')
        address, size = SCALARS[name]
        return self.read(address, size)

    def set_scalar(self, name, value):
        """Write one named scalar, sharing storage with all live views."""
        if type(name) is not str or name not in SCALARS:
            raise ValueError('declared battle scalar required')
        address, size = SCALARS[name]
        self.write(address, size, uint(value, size * 8))

    def seed(self):
        self._rng_seed_read = self.read(0xFFFFF61C, 4)
        return self._rng_seed_read

    def set_seed(self, value):
        value = uint(value, 32)
        self.write(0xFFFFF61C, 4, value)
        self._rng_seed_written = value

    def store_seed(self, value):
        self.set_seed(value)

    def sample_random_pair(self):
        """Reuse audited RNG logic, retaining its two original scalar results.

        Values are captured at the real seed read/write. Reading RAM again
        here would change original DATA order and is deliberately forbidden.
        """
        from tools.high_level_city_cycle.business import step_random
        self._rng_seed_read = None
        self._rng_seed_written = None
        sample = uint(step_random(self), 16)
        if self._rng_seed_read is None or self._rng_seed_written is None:
            raise ValueError('complete accepted RNG DATA contract required')
        original_seed = self._rng_seed_read or 0x2A6D365A
        return RandomSample((original_seed & 0xFFFF0000) | sample,
                            self._rng_seed_written)

    def sample_random(self):
        return self.sample_random_pair().sample

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
        raise ValueError('typed battle GameState required')
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


for _name, _base in VIEW_BASES.items():
    setattr(GameState, _name, property(lambda self, base=_base: Table(self, base)))
for _name, (_address, _size) in SCALARS.items():
    setattr(GameState, _name,
            lambda self, address=_address, size=_size: self.read(address, size))
    setattr(GameState, 'set_' + _name,
            lambda self, value, address=_address, size=_size:
            self.write(address, size, uint(value, size * 8)))
