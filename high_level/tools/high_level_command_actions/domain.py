"""Live, fixed-width command-action data and explicitly supplied readonly resources.

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


# These named ports are populated from the selected candidate's original
# caller/data evidence. They describe bindings, never hidden image/audio data.
VIEW_BASES = {
    'officer_training': 0xffffc500,
    'officer_readiness': 0xffffb200,
    'officer_troops': 0xffffc800,
    'officer_word_c000': 0xffffc000,
    'officer_word_be00': 0xffffbe00,
    'officer_word_b400': 0xffffb400,
    'officer_word_b600': 0xffffb600,
    'officer_status': 0xffffc700,
    'officer_city_assignment': 0xffffcc00,
    'battlefield_city_assignment': 0xffffa050,
    'action_candidates': 0xffffd300,
    'battle_primary_roster': 0xffffa550,
    'battle_secondary_roster': 0xffffa5a4,
    'battle_primary_retired_roster': 0xffffa5ce,
    'battle_secondary_retired_roster': 0xffffa57a,
    'city_head_words': 0xfffff45e,
    'city_food': 0xffffe09c,
    'city_battle_resource': 0xffffee24,
    'duel_packet_first': 0xff7050,
    'duel_packet_second': 0xff70a0,
    'candidate_roster': 0xfffff500,
    'city_owner_bytes': 0xfffff427,
    'city_battle_gold': 0xffffed84,
    'city_battle_food': 0xffffee24,
    'city_gold': 0xffffdffc,
    'officer_loyalty': 0xffffc300,
    'officer_disposition': 0xffffc200,
    'officer_actions': 0xffffcd00,
    'officer_strength': 0xffffb600,
    'officer_progress': 0xffffbe00,
    'officer_ability': 0xffffc000,
    'officer_resolve': 0xffffb400,
    'force_heads': 0xffffe640,
    'city_recruitment_heads': 0xfffff45e,
    'officer_status_rating': 0xffffc300,
    'city_orders': 0xffffe80c,
    'education_factors': 0xe776,
    'relationship_targets': 0xffffe730,
    'force_relationships': 0xffffe710,
    'alternate_heads': 0xffffa026,
    'battle_positions': 0xffffa150,
    'selected_attributes': 0xffffc400,
    'city_command_flags': 0xffffea37,
    'deployment_queue': 0xff3000,
    'message_directory': 0x92c4a,
    'message_bank_offsets': 0x92c4e,
    'message_layout': 0x6773c,
    'relationship_character_bias': 0xec5c,
    'policy_character_bias': 0xee11,
    'target_policy_bias': 0xee0c,
    'policy_divisors': 0xdf08,
    'recruitment_score_parameters': 0xdf0e,
    'recruitment_food_parameters': 0xfa16,
    'recruitment_gold_parameters': 0xfa66,
    'recruitment_state_parameters': 0xfabc,
    'recruitment_city_food': 0xffffe0a0,
    'recruitment_city_gold': 0xffffe000,
    'recruitment_city_state': 0xffffe1e0,
}
SCALARS = {
    'active_descriptor': (0xff382c, 4),
    'candidate_member_count': (0xfffff636, 2),
    'deployment_city': (0xfffff392, 2),
    'action_amount': (0xfffff39e, 4),
    'training_cost': (0xfffff3ba, 4),
    'battle_scene': (0xfffff68a, 2),
    'battle_active': (0xffffefe0, 2),
    'duel_primary_officer': (0xffff80e0, 2),
    'duel_secondary_officer': (0xffff80e2, 2),
    'duel_training_primary': (0xffff8101, 1),
    'duel_training_secondary': (0xffff8103, 1),
    'duel_readiness_primary': (0xffff810c, 2),
    'duel_readiness_secondary': (0xffff810e, 2),
    'duel_result': (0xffff8114, 2),
    'duel_troops_primary': (0xffff8118, 2),
    'duel_troops_secondary': (0xffff811a, 2),
    'result_first': (0xff70f0, 1),
    'result_second': (0xff70f1, 1),
    'roster_side_owner': (0xfffff702, 2),
    'outcome_ratio': (0xffffefbc, 2),
    'outcome_first_points': (0xffffefb8, 2),
    'outcome_second_points': (0xffffefba, 2),
    'command_sound': (0xfffff612, 2),
    'ui_state': (0xfffff362, 2),
    'selected_officer': (0xfffff3a6, 2),
    'policy_target': (0xfffff3f2, 2),
    'selected_city': (0xfffff3a8, 2),
    'chosen_city': (0xfffff392, 2),
    'current_force': (0xfffff376, 2),
    'selected_teacher': (0xfffff630, 2),
    'alternate_teacher': (0xfffff634, 2),
    'result_pair': (0xfffff3c8, 4),
    'result_low': (0xfffff3ca, 2),
    'message': (0xfffff3fe, 2),
    'command_actor': (0xfffff3d0, 2),
    'command_target': (0xfffff3d2, 2),
    'visible_force_first': (0xfffff67a, 2),
    'visible_force_second': (0xfffff67c, 2),
    'visible_force_third': (0xfffff67e, 2),
    'random_seed_high': (0xfffff61c, 2),
    'random_seed': (0xfffff61c, 4),
    'policy_selector': (0xffffefd2, 2),
    'command_mode': (0xff7026, 2),
    'command_timer': (0xfffff608, 2),
    'command_audio': (0xfffff38a, 2),
    'preferred_head': (0xfffff630, 2),
    'relationship_target': (0xfffff3e0, 2),
    'deployment_queue_offset': (0xff3826, 2),
    'deployment_city_tail': (0xfffff393, 1),
    'message_flag': (0xfffff652, 2),
    'message_pointer': (0xfffff3be, 4),
    'message_scene': (0xfffff3c2, 2),
    'message_stage': (0xfffff3c4, 2),
    'message_kind': (0xfffff36a, 2),
    'message_parameter': (0xfffff3c6, 2),
    'message_mode': (0xfffff600, 2),
    'message_layout_index': (0xfffff6c4, 2),
    'message_pending': (0xffffefda, 2),
    'result_pair_high': (0xfffff3c8, 2),
    'result_pair_low': (0xfffff3ca, 2),
    'command_message': (0xfffff3fe, 2),
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
            raise Boundary('explicit command-action DATA budget')
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
            raise ValueError('declared command-action scalar required')
        address, size = SCALARS[name]
        return self.read(address, size)

    def set_scalar(self, name, value):
        """Write one named scalar, sharing storage with all live views."""
        if type(name) is not str or name not in SCALARS:
            raise ValueError('declared command-action scalar required')
        address, size = SCALARS[name]
        self.write(address, size, uint(value, size * 8))

    def sample_random(self):
        from .business_reuse import step_random
        return step_random(self)

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
        raise ValueError('typed command-action GameState required')
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
