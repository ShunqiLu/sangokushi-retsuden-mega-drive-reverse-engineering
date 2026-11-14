"""One live gameplay state, fixed-width DATA and explicit hardware/service boundaries.

Business functions use named tables, scalar ports and family-local contexts.
This boundary owns address arithmetic, bus alignment and ordered DATA events;
it is not an instruction interpreter and never opens a ROM or asset file.
"""
from dataclasses import dataclass
from typing import NewType
import re
from dataclasses import is_dataclass


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



def integer(value):
    if type(value) is not int:
        raise ValueError('strict integer, not bool/float, required')
    return value


def unsigned(value, bits):
    integer(value)
    integer(bits)
    if not 1 <= bits <= 32:
        raise ValueError('explicit width1..32 required')
    if not 0 <= value < 1 << bits:
        raise ValueError('complete unsigned field required')
    return value


def checked_word(value): return uint(value, 16)
def checked_long(value): return uint(value, 32)
def word(value): return u16(value)
def long(value): return u32(value)
def byte(value): return u8(value)
def low_word(value): return low16(value)
def low_byte(value): return low8(value)
def signed_word(value): return (integer(value) & 32767) - (value & 32768)
def add16(left, right): return u16(integer(left) + integer(right))
def sub16(left, right): return u16(integer(left) - integer(right))
def add32(left, right): return u32(integer(left) + integer(right))
def sub32(left, right): return u32(integer(left) - integer(right))
def sub8(left, right): return (integer(left) & ~255) | u8(left - integer(right))
def shl16(value, count): return u16(integer(value) << integer(count))
def shl32(value, count): return u32(integer(value) << integer(count))
def mask16(value, mask): return u16(integer(value) & integer(mask))
def mask32(value, mask): return u32(integer(value) & integer(mask))
def clear_low_word(value): return integer(value) & 0xFFFF0000
def negate32(value): return u32(-integer(value))
def replace_low_word(value, low): return (integer(value) & 0xFFFF0000) | u16(low)
def mulu16(left, right): return u16(left) * u16(right)
def divu16(value, divisor): return divu_retained(u32(value), uint(divisor, 16))
def stitched_product(value, factor):
    return add32(mulu16(value, factor), swap_words(mulu16(swap_words(value), factor)))
def saturating_add32(left, right): return min(u32(left) + u32(right), 0xFFFFFFFF)
def subtract_borrow32(left, right): return sub32(left, right), u32(left) < u32(right)
def minimum32(value, ceiling): return min(u32(value), u32(ceiling))


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


# Fresh same-domain ports rederived from the old selected table bindings.
# A source package's similarly named but differently addressed port is NEVER
# selected by inspecting a caller: battle_candidate_roster and candidate_roster
# explicitly distinguish D300 and F500.
VIEW_BASES.update({
    'battle_candidate_roster': 0xFFFFD300,
    'officer_assignments': 0xFFFFCC00, 'city_assignments': 0xFFFFCC00,
    'alternate_assignments': 0xFFFFA050, 'status_roster': 0xFFFFD320,
    'remaining_roster': 0xFFFFAF28, 'survivor_roster': 0xFFFFAF56,
    'status': 0xFFFFC300, 'loyalty': 0xFFFFC500, 'affinity': 0xFFFFC200,
    'attributes': 0xFFFFC400, 'troops': 0xFFFFB200,
    'officer_resources': 0xFFFFB200, 'troop_strengths': 0xFFFFC800,
    'city_owners': 0xFFFFF427, 'other_city_owners': 0xFFFFF428,
    'packed_groups': 0xFFFF9000, 'group_packets': 0xFFFF9000,
    'group_offsets': 0xFFFFEFBE, 'city_rice': 0xFFFFE09C,
    'city_ed84': 0xFFFFED84, 'city_ee24': 0xFFFFEE24,
    'pair_references': 0x00FF39B2, 'head_records': 0x00FF3000,
    'city_coordinates': 0xD4AC6, 'arrival_coordinates': 0xD4ACA,
    'neighbor_offsets': 0x21F82, 'terrain_cells': 0xEE5F0,
    'terrain_cost': 0x670A, 'terrain_costs': 0x670A,
    'capacities_b000': 0xFFFFB000, 'troops_b200': 0xFFFFB200,
    'city_processed': 0xFFFFEA37, 'battlefield_maps': 0x945E8,
    'terrain_category_lookup': 0x6C0B4, 'radial_threshold_rows': 0x30876,
    'city_modifiers': 0xFFFFE280, 'primary_ledger': 0xFFFFE000,
    'secondary_ledger': 0xFFFFE0A0, 'secondary_rates': 0xFFFFE1E0,
    'depletion_modifiers': 0xFFFFE3C0, 'income_bases': 0xFFFFE140,
    'depletion_parameters': 0x16CFC, 'depletion_reserve': 0xFFFFE320,
    'officer_categories': 0xFFFFC700, 'officer_amounts': 0xFFFFC800,
    'roster': 0xFFFFF500, 'expense_parameters': 0x16DE0,
    'scores': 0xFFFFEA60, 'first_score_components': 0xFFFFBE00,
    'second_score_components': 0xFFFFC000, 'officer_modifiers': 0xFFFFC200,
    'officer_penalties': 0xFFFFC300,
})
SCALARS.update({
    'city': (0xFFFFF68A, 2), 'primary_force': (0xFFFFF68C, 2),
    'secondary_force': (0xFFFFF68E, 2),
    'primary_owner_byte': (0xFFFFF68D, 1), 'secondary_owner_byte': (0xFFFFF68F, 1),
    'working_owner': (0xFFFFEFE2, 1), 'returning_count': (0xFFFFEFB8, 2),
    'remaining_count': (0xFFFFEFBA, 2), 'resource_side': (0xFFFFF6D6, 2),
    'side_flags': (0xFFFFF6D7, 1), 'loyalty_source': (0xFFFFF3F2, 2),
    'selected_group_offset': (0xFFFFEFC6, 2),
    'selected_group_pointer': (0x00FF382C, 4), 'opposing_group': (0x00FF382C, 4),
    'primary_officer': (0xFFFFF702, 2), 'secondary_officer': (0xFFFFF706, 2),
    'outcome': (0xFFFF8114, 2), 'winning_officer': (0xFFFF80E0, 2),
    'losing_officer': (0xFFFF80E2, 2), 'pair_reference_offset': (0x00FF3BB2, 2),
    'head': (0xFFFFF630, 2), 'roster_count': (0xFFFFF636, 2),
    'seed_high': (0xFFFFF61C, 2),
    'metadata_f374': (0xFFFFF374, 1), 'metadata_f375': (0xFFFFF375, 1),
    'metadata_f67b': (0xFFFFF67B, 1), 'metadata_f67d': (0xFFFFF67D, 1),
    'metadata_f67f': (0xFFFFF67F, 1),
})

# The C source uses these original absolute-LONG logical addresses. Other
# A/B/C/D/E/F RAM symbols in this selection use sign-extended absolute WORDs.
ABSOLUTE_LONG_RAM = {
    0x3000, 0x39B2, 0x3BB2, 0x3BC2, 0x3CC2, 0x3DC2,
    0x3ED2, 0x3ED6, 0x3EDA, 0x7026, 0x7050, 0x70A0,
    0x70F0, 0x70F1, 0x70F4,
}
EVENT_PARAMETER_BASE = 0x174F0
EVENT_FIELD_BASES = {
    'e1e0': 0xFFFFE1E0, 'e140': 0xFFFFE140, 'e320': 0xFFFFE320,
    'e000': 0xFFFFE000, 'e0a0': 0xFFFFE0A0, 'e5a0': 0xFFFFE5A0,
}


def neutral_ram_address(name):
    if type(name) is not str or not re.fullmatch(r'ram_[0-9a-f]{4}', name):
        raise ValueError('explicit ram_xxxx view name required')
    low = int(name[4:], 16)
    if low in ABSOLUTE_LONG_RAM:
        return 0x00FF0000 | low
    if low < 0x8000:
        raise ValueError('neutral low RAM view needs original LONG binding')
    return 0xFFFF0000 | low


def scalar_binding(name):
    if type(name) is not str:
        raise ValueError('named scalar required')
    if name in SCALARS:
        return SCALARS[name]
    match = re.fullmatch(r'(ram_[0-9a-f]{4})_(byte|word|long)', name)
    if match is None:
        raise ValueError('declared gameplay scalar required')
    return neutral_ram_address(match[1]), {'byte': 1, 'word': 2, 'long': 4}[match[2]]


class HardwareBus:
    """Explicit hardware interface; default read/write/progress stop.

    Subclasses may implement real supplied hardware effects. The selected
    program's MMIO is not readonly art/audio data. Progress receives this same
    live state so asynchronous RAM effects remain ordered through its writes.
    """
    def __init__(self, ranges=((0xA00000, 0xA20000), (0xC00000, 0xC00020))):
        if type(ranges) is not tuple:
            raise ValueError('explicit physical hardware range tuple required')
        rows = []
        for row in ranges:
            if type(row) is not tuple or len(row) != 2:
                raise ValueError('hardware (start,end) required')
            start, end = row
            uint(start, 32)
            uint(end, 32)
            if not 0 <= start < end <= 0xFF0000:
                raise ValueError('hardware ranges must not shadow RAM')
            rows.append(row)
        rows.sort()
        if any(a[1] > b[0] for a,b in zip(rows, rows[1:])):
            raise ValueError('overlapping hardware mapping')
        self.ranges = tuple(rows)

    def contains(self, physical, size):
        return any(start <= physical and physical + size <= end for start,end in self.ranges)

    def read(self, address, size):
        raise Boundary('unsupplied hardware read')

    def write(self, address, size, value):
        raise Boundary('unsupplied hardware write')

    def progress(self, state, reason):
        raise Boundary('unsupplied asynchronous hardware progress')


class GameplayServices:
    """External finite typed services, never an interpreter or fake RTS."""
    def invoke(self, state, entry, context):
        raise Boundary('unreconstructed external service / indirect handler')


def typed_service_context(value, state):
    if isinstance(value, type) or not is_dataclass(value):
        raise ValueError('explicit dataclass service context required')
    validator = getattr(value, 'validate', None)
    if callable(validator):
        # Battle-family inputs validate their views against this live state.
        # Scalar service contracts use __post_init__ instead; neither protocol
        # authorizes a fabricated result from an unreconstructed handler.
        validator(state)
    else:
        validator = getattr(value, '__post_init__', None)
        if callable(validator):
            validator()
    if not callable(validator):
        raise ValueError('validated typed service context required')
    for field_name in value.__dataclass_fields__:
        supplied = getattr(value, field_name)
        if type(supplied) in (Table, Cursor):
            checked_table(supplied, state)
    return value


class GameplayState:
    def __init__(self, ram, *, data=None, hardware=None, services=None,
                 max_reads=1000000, max_samples=65536, sr=0x2700):
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
        if hardware is None:
            hardware = HardwareBus()
        if not isinstance(hardware, HardwareBus):
            raise ValueError('explicit typed HardwareBus required')
        if services is None:
            services = GameplayServices()
        if not isinstance(services, GameplayServices):
            raise ValueError('explicit typed GameplayServices required')
        uint(max_samples, 32)
        if max_samples == 0:
            raise ValueError('positive explicit RNG budget required')
        for base, raw in data.segments:
            if base + len(raw) > 0xFF0000:
                raise ValueError('readonly source must not compete with live RAM')
            if any(base < end and start < base + len(raw) for start,end in hardware.ranges):
                raise ValueError('readonly source must not compete with hardware')
        self.hardware, self.services = hardware, services
        self.max_samples, self.samples = max_samples, 0
        self.reads, self.events = 0, []

    def read(self, address, size):
        uint(address, 32)
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('strict DATA width required')
        if self.reads >= self.max_reads:
            raise Boundary('explicit gameplay DATA budget')
        if size > 1 and address & 1:
            raise Boundary('odd DATA read')
        bus = address & 0xFFFFFF
        if 0xFF0000 <= bus and bus + size <= 0x1000000:
            start = bus & 65535
            value = int.from_bytes(self.ram[start:start + size], 'big')
        elif self.hardware.contains(bus, size):
            value = uint(self.hardware.read(address, size), size * 8, 'hardware DATA')
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
        if 0xFF0000 <= bus and bus + size <= 0x1000000:
            start = bus & 65535
            self.ram[start:start + size] = value.to_bytes(size, 'big')
        elif self.hardware.contains(bus, size):
            self.hardware.write(address, size, value)
        else:
            raise Boundary('outside writable RAM or explicitly supplied hardware')
        self.events.append(('write', address, size, value))

    def table(self, base):
        if type(base) is str:
            base = VIEW_BASES[base] if base in VIEW_BASES else neutral_ram_address(base)
        return Table(self, base)

    def checked_table(self, value):
        return checked_table(value, self)

    def checked_cursor(self, value):
        return checked_cursor(value, self)

    def scalar(self, name):
        """Read one named scalar at its declared original width."""
        address, size = scalar_binding(name)
        return self.read(address, size)

    def set_scalar(self, name, value):
        """Write one named scalar, sharing storage with all live views."""
        address, size = scalar_binding(name)
        self.write(address, size, uint(value, size * 8))

    def sample_random(self):
        from .business_reuse import step_random
        return step_random(self)

    def __getattr__(self, name):
        if re.fullmatch(r'ram_[0-9a-f]{4}', name):
            return self.table(name)
        raise AttributeError(name)

    def checked_context(self, value):
        return checked_context(value, self)

    def seed(self):
        if self.samples >= self.max_samples:
            raise Boundary('explicit RNG-call budget exhausted')
        self.samples += 1
        return self.scalar('random_seed')

    def store_seed(self, value):
        self.set_scalar('random_seed', uint(value, 32))

    def set_seed(self, value):
        self.store_seed(value)

    def sample_random_pair(self):
        from .business_reuse import _reuse_advance_random_pair
        return _reuse_advance_random_pair(self)

    def owner(self, city):
        return self.read(u32(0xFFFFF428 + s16(uint(city, 16))), 1)

    def player_owner(self, slot):
        uint(slot, 8)
        if slot > 2:
            raise ValueError('one of three explicit player-owner slots required')
        return self.read(0xFFFFF67A + slot * 2, 2)

    def clear_queue_flag(self):
        self.write(0xFFFFD448, 2, 0)

    def queue(self):
        return Queue(self)

    def field(self, name):
        return Field(self, name)

    def parameter(self, group, index):
        if type(group) is not str or group not in ('mask', 'factor'):
            raise ValueError('explicit mask/factor parameter group required')
        offset = s16(uint(index, 16)) + (0 if group == 'mask' else 12)
        if not 0 <= offset < 24:
            raise Boundary('event parameter read outside explicit24B allocation')
        return self.read(EVENT_PARAMETER_BASE + offset, 1)

    def terrain_query(self, row, column):
        from .business_reuse import terrain_cell_query
        return terrain_cell_query(self, u16(row), u16(column))

    def read_status_word(self):
        # MOVE from SR is not privileged on the original MC68000. This remains
        # explicit full-SR data; no automatic CCR or traced instruction model.
        if self.sr & 0x8000:
            raise Boundary('trace continuation not modeled')
        self.events.append(('status_read', self.sr))
        return self.sr

    def set_status_word(self, value):
        uint(value, 16, 'full status WORD')
        if not self.sr & 0x2000:
            raise Boundary('original full-SR write requires supervisor')
        if self.sr & 0x8000 or value & 0x8000:
            raise Boundary('trace continuation not modeled')
        self.sr = value
        self.events.append(('status_write', value))

    def read_status(self):
        return self.read_status_word()

    def set_status(self, value):
        self.set_status_word(value)

    def mmio_read(self, address, size):
        uint(address, 32)
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('strict hardware DATA width required')
        if not self.hardware.contains(address & 0xFFFFFF, size):
            raise Boundary('outside explicitly mapped hardware')
        return self.read(address, size)

    def mmio_write(self, address, size, value):
        uint(address, 32)
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('strict hardware DATA width required')
        if not self.hardware.contains(address & 0xFFFFFF, size):
            raise Boundary('outside explicitly mapped hardware')
        self.write(address, size, value)

    def progress(self, reason):
        if type(reason) is not str or not reason:
            raise ValueError('explicit asynchronous wait reason required')
        return self.hardware.progress(self, reason)

    def service_at(self, entry, context):
        uint(entry, 32, 'external original entry')
        typed_service_context(context, self)
        return self.services.invoke(self, entry, context)

    def calendar_submit_carrier(self, city, retained):
        uint(city, 16)
        uint(retained, 16)
        raise Boundary('calendar caller must consume the original helper carrier result, not reread/synthesize it')

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
        self._iteration_base = None

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


    def _next(self, size):
        address = self.base if self._iteration_base is None else self._iteration_base
        value = self.state.read(address, size)
        self._iteration_base = u32(address + size)
        return value

    def next_byte(self): return self._next(1)
    def next_word(self): return self._next(2)
    def next_long(self): return self._next(4)

    def _append(self, value, size):
        address = self.base if self._iteration_base is None else self._iteration_base
        self.state.write(address, size, uint(value, size * 8))
        self._iteration_base = u32(address + size)

    def append_byte(self, value): self._append(value, 1)
    def append_word(self, value): self._append(value, 2)
    def append_long(self, value): self._append(value, 4)

    def put_word(self, value):
        address = self.base if self._iteration_base is None else self._iteration_base
        self.state.write(address, 2, uint(value, 16))

    def subtract_word(self, offset, value, displacement=0):
        self.set_word(offset, sub16(self.word(offset, displacement), value), displacement)

    def subtract_byte(self, offset, value):
        integer(value)
        previous = self.byte(offset)
        self.set_byte(offset, u8(previous - value))
        return previous < u8(value)

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
    if type(value) is not GameplayState:
        raise ValueError('typed gameplay GameplayState required')
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
    setattr(GameplayState, _name, property(lambda self, base=_base: Table(self, base)))
for _name, (_address, _size) in SCALARS.items():
    setattr(GameplayState, _name,
            lambda self, address=_address, size=_size: self.read(address, size))
    setattr(GameplayState, 'set_' + _name,
            lambda self, value, address=_address, size=_size:
            self.write(address, size, uint(value, size * 8)))



@dataclass(frozen=True)
class GroupContext:
    source: Table
    target: Table

    def __post_init__(self):
        checked_table(self.source)
        checked_table(self.target, self.source.state)


def checked_context(value, state=None):
    if type(value) is not GroupContext:
        raise ValueError('typed GroupContext required')
    checked_table(value.source, state)
    checked_table(value.target, value.source.state)
    return value


class Queue:
    """Original live BYTE queue; no invented terminator or fixed scan clamp."""
    def __init__(self, state):
        self.state, self.cursor = checked_state(state), 0xFFFFD420

    def read_next(self):
        value = self.state.read(self.cursor, 1)
        self.cursor = u32(self.cursor + 1)
        return value

    def rewind_probe(self):
        self.cursor = u32(self.cursor - 1)
        return self.state.read(self.cursor, 1)

    def write(self, value):
        self.state.write(self.cursor, 1, low8(uint(value, 16)))

    def write_next(self, value):
        self.write(value)
        self.cursor = u32(self.cursor + 1)


class Field:
    """One live full-LONG field with original signed-WORD indexed addressing."""
    def __init__(self, state, name):
        checked_state(state)
        if type(name) is not str or name not in EVENT_FIELD_BASES:
            raise ValueError('declared event field required')
        self.state, self.base = state, EVENT_FIELD_BASES[name]

    def read(self, offset):
        return self.state.read(u32(self.base + s16(uint(offset, 16))), 4)

    def write(self, offset, value):
        self.state.write(u32(self.base + s16(uint(offset, 16))), 4, u32(value))
