"""Fresh scene/duel live state and ordered hardware/data boundary.

No old runtime State, CPU interpreter, ROM or media payload is invoked.
Gameplay rules live in separate business modules. Default asynchronous and
dynamic services stop explicitly rather than fabricating successful returns.
"""
from dataclasses import dataclass, is_dataclass
from typing import NewType
import re

Byte=NewType('Byte',int)
Word=NewType('Word',int)
Long=NewType('Long',int)

VIEW_BASES={
    'action_candidates':0xFFFFD300,
    'battlefield_city_assignment':0xFFFFA050,
    'officer_city_assignment':0xFFFFCC00,
    'first_duel_actor':0x00FF7050,
    'second_duel_actor':0x00FF70A0,
    'scene_sprite_queue':0xFFFFD100,
    'scene_palette':0xFFFFFB00,
    'scene_secondary_palette':0xFFFFFB20,
}
SCALARS={'random_seed':(0xFFFFF61C,4),'battle_scene':(0xFFFFF68A,2)}

# Only original absolute-LONG low RAM bindings. A video-plane address never
# enters this mapping. Exact logical addresses can always be explicit reads.
ABSOLUTE_LONG_RAM={24576, 28672, 28674, 28676, 28678, 28680, 28682, 28683, 28684, 28810, 28686, 28818, 28692, 28694, 28696, 28697, 28832, 28834, 28710, 28712, 28714, 28716, 28844, 28718, 28846, 28720, 28722, 28724, 28726, 28856, 28730, 28858, 28732, 28860, 28734, 28864, 28740, 28874, 28875, 28877, 28879, 28752, 28754, 28890, 28764, 28766, 28898, 28776, 28778, 28922, 28780, 28784, 28912, 28914, 28918, 28920, 28794, 28795, 28797, 28799}

def neutral_ram_address(name):
    if type(name) is not str or re.fullmatch(r'ram_[0-9a-f]{4}',name) is None:
        raise ValueError('explicit ram_xxxx view name required')
    low=int(name[4:],16)
    if low in ABSOLUTE_LONG_RAM:
        return 0x00FF0000|low
    if low<0x8000:
        raise ValueError('low RAM port needs an original absolute-LONG binding')
    return 0xFFFF0000|low

def scalar_binding(name):
    if type(name) is not str:
        raise ValueError('named scalar required')
    if name in SCALARS:
        return SCALARS[name]
    match=re.fullmatch(r'(ram_[0-9a-f]{4})_(byte|word|long)',name)
    if match is None:
        raise ValueError('declared scene scalar required')
    return neutral_ram_address(match[1]),{'byte':1,'word':2,'long':4}[match[2]]

class Boundary(ValueError):
    """An explicit original-data or finite-model boundary, not a fake return."""

def uint(value, bits, name='value'):
    if type(bits) is not int or bits not in (8, 16, 32) or type(value) is not int or (not 0 <= value < 1 << bits):
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
    return value & 4294967295

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
    return uint(value, 32) & 4294967040 | uint(byte, 8)

def replace_word(value, word):
    return uint(value, 32) & 4294901760 | uint(word, 16)

def swap_words(value):
    value = uint(value, 32)
    return u32(value << 16 | value >> 16)

def negative_byte(value):
    return bool(uint(value, 8) & 128)

def negative_word(value):
    return bool(uint(value, 16) & 32768)

def negative_long(value):
    return bool(uint(value, 32) & 2147483648)

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
    return numerator if quotient > 65535 else remainder << 16 | quotient

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

def checked_word(value):
    return uint(value, 16)

def checked_long(value):
    return uint(value, 32)

def word(value):
    return u16(value)

def long(value):
    return u32(value)

def byte(value):
    return u8(value)

def low_word(value):
    return low16(value)

def low_byte(value):
    return low8(value)

def signed_word(value):
    return (integer(value) & 32767) - (value & 32768)

def add16(left, right):
    return u16(integer(left) + integer(right))

def sub16(left, right):
    return u16(integer(left) - integer(right))

def add32(left, right):
    return u32(integer(left) + integer(right))

def sub32(left, right):
    return u32(integer(left) - integer(right))

def sub8(left, right):
    return integer(left) & ~255 | u8(left - integer(right))

def shl16(value, count):
    return u16(integer(value) << integer(count))

def shl32(value, count):
    return u32(integer(value) << integer(count))

def mask16(value, mask):
    return u16(integer(value) & integer(mask))

def mask32(value, mask):
    return u32(integer(value) & integer(mask))

def clear_low_word(value):
    return integer(value) & 4294901760

def negate32(value):
    return u32(-integer(value))

def replace_low_word(value, low):
    return integer(value) & 4294901760 | u16(low)

def mulu16(left, right):
    return u16(left) * u16(right)

def divu16(value, divisor):
    return divu_retained(u32(value), uint(divisor, 16))

def stitched_product(value, factor):
    return add32(mulu16(value, factor), swap_words(mulu16(swap_words(value), factor)))

def saturating_add32(left, right):
    return min(u32(left) + u32(right), 4294967295)

def subtract_borrow32(left, right):
    return (sub32(left, right), u32(left) < u32(right))

def minimum32(value, ceiling):
    return min(u32(value), u32(ceiling))

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
            if type(raw) is not bytes or not raw or base + len(raw) > 16777216:
                raise ValueError('nonempty 24bit segment required')
            rows.append((base, raw))
        rows.sort()
        if any((base + len(raw) > following for (base, raw), (following, _) in zip(rows, rows[1:]))):
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

class HardwareBus:
    """Explicit hardware interface; default read/write/progress stop.

    Subclasses may implement real supplied hardware effects. The selected
    program's MMIO is not readonly art/audio data. Progress receives this same
    live state so asynchronous RAM effects remain ordered through its writes.
    """

    def __init__(self, ranges=((10485760, 10616832), (12582912, 12582944))):
        if type(ranges) is not tuple:
            raise ValueError('explicit physical hardware range tuple required')
        rows = []
        for row in ranges:
            if type(row) is not tuple or len(row) != 2:
                raise ValueError('hardware (start,end) required')
            start, end = row
            uint(start, 32)
            uint(end, 32)
            if not 0 <= start < end <= 16711680:
                raise ValueError('hardware ranges must not shadow RAM')
            rows.append(row)
        rows.sort()
        if any((a[1] > b[0] for a, b in zip(rows, rows[1:]))):
            raise ValueError('overlapping hardware mapping')
        self.ranges = tuple(rows)

    def contains(self, physical, size):
        return any((start <= physical and physical + size <= end for start, end in self.ranges))

    def read(self, address, size):
        raise Boundary('unsupplied hardware read')

    def write(self, address, size, value):
        raise Boundary('unsupplied hardware write')

    def progress(self, state, reason):
        raise Boundary('unsupplied asynchronous hardware progress')

    def after_write(self, state, address, size, value):
        """Let an actual bus master hold CPU completion after its recorded write.

        Ordinary unclocked devices have no post-write effect. Known composed
        buses retain their existing owner chain; a specialized device may
        consume explicitly supplied arbitration/transfer events here. This
        hook does not choose clock counts, clear a busy flag or assert an IRQ.
        """
        devices = getattr(self, 'devices', None)
        if isinstance(devices, HardwareBus):
            return devices.after_write(state, address, size, value)

class SceneServices:
    """External finite typed services, never an interpreter or fake RTS."""

    def invoke(self, state, entry, context):
        raise Boundary('unreconstructed external service / indirect handler')

def typed_service_context(value, state):
    if isinstance(value, type) or not is_dataclass(value):
        raise ValueError('explicit dataclass service context required')
    validator = getattr(value, 'validate', None)
    if callable(validator):
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

class SceneState:

    def __init__(self, ram, *, data=None, hardware=None, services=None, max_reads=1000000, max_samples=65536, sr=9984):
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
        self.ram, self.data, self.max_reads, self.sr = (ram, data, max_reads, sr)
        if hardware is None:
            hardware = HardwareBus()
        if not isinstance(hardware, HardwareBus):
            raise ValueError('explicit typed HardwareBus required')
        if services is None:
            services = SceneServices()
        if not isinstance(services, SceneServices):
            raise ValueError('explicit typed GameplayServices required')
        uint(max_samples, 32)
        if max_samples == 0:
            raise ValueError('positive explicit RNG budget required')
        for base, raw in data.segments:
            if base + len(raw) > 16711680:
                raise ValueError('readonly source must not compete with live RAM')
            if any((base < end and start < base + len(raw) for start, end in hardware.ranges)):
                raise ValueError('readonly source must not compete with hardware')
        self.hardware, self.services = (hardware, services)
        self.max_samples, self.samples = (max_samples, 0)
        self.reads, self.events = (0, [])

    def read(self, address, size):
        uint(address, 32)
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('strict DATA width required')
        if self.reads >= self.max_reads:
            raise Boundary('explicit gameplay DATA budget')
        if size > 1 and address & 1:
            raise Boundary('odd DATA read')
        bus = address & 16777215
        if 16711680 <= bus and bus + size <= 16777216:
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
        bus = address & 16777215
        if 16711680 <= bus and bus + size <= 16777216:
            start = bus & 65535
            self.ram[start:start + size] = value.to_bytes(size, 'big')
        elif self.hardware.contains(bus, size):
            self.hardware.write(address, size, value)
        else:
            raise Boundary('outside writable RAM or explicitly supplied hardware')
        self.events.append(('write', address, size, value))
        self.hardware.after_write(self, address, size, value)

    def table(self, base):
        if type(base) is str:
            base = VIEW_BASES[base] if base in VIEW_BASES else neutral_ram_address(base)
        return Table(self, base)

    def table_at(self, address):
        return self.table(uint(address,32))

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
        if re.fullmatch('ram_[0-9a-f]{4}', name):
            return self.table(name)
        raise AttributeError(name)

    def seed(self):
        if self.samples >= self.max_samples:
            raise Boundary('explicit RNG-call budget exhausted')
        self.samples += 1
        return self.scalar('random_seed')

    def store_seed(self, value):
        self.set_scalar('random_seed', uint(value, 32))

    def set_seed(self, value):
        self.store_seed(value)

    def read_status_word(self):
        if self.sr & 32768:
            raise Boundary('trace continuation not modeled')
        self.events.append(('status_read', self.sr))
        return self.sr

    def set_status_word(self, value):
        uint(value, 16, 'full status WORD')
        if not self.sr & 8192:
            raise Boundary('original full-SR write requires supervisor')
        if self.sr & 32768 or value & 32768:
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
        if not self.hardware.contains(address & 16777215, size):
            raise Boundary('outside explicitly mapped hardware')
        return self.read(address, size)

    def mmio_write(self, address, size, value):
        uint(address, 32)
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('strict hardware DATA width required')
        if not self.hardware.contains(address & 16777215, size):
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

class Table:

    def __init__(self, state, base):
        checked_state(state)
        self.state, self.base = (state, uint(base, 32))
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
        if type(amount) is not int or not -2147483648 <= amount <= 2147483647:
            raise ValueError('signed LONG advance required')
        return type(self)(self.state, u32(self.base + amount))

    def cursor(self, offset=0):
        return Cursor(self.state, self.address(offset))

    def _next(self, size):
        address = self.base if self._iteration_base is None else self._iteration_base
        value = self.state.read(address, size)
        self._iteration_base = u32(address + size)
        return value

    def next_byte(self):
        return self._next(1)

    def next_word(self):
        return self._next(2)

    def next_long(self):
        return self._next(4)

    def _append(self, value, size):
        address = self.base if self._iteration_base is None else self._iteration_base
        self.state.write(address, size, uint(value, size * 8))
        self._iteration_base = u32(address + size)

    def append_byte(self, value):
        self._append(value, 1)

    def append_word(self, value):
        self._append(value, 2)

    def append_long(self, value):
        self._append(value, 4)

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
    if type(value) is not SceneState:
        raise ValueError('typed SceneState required')
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
    value = u32(value << 8 | view.byte(offset, 1))
    value = u32(value << 8 | view.byte(offset, 2))
    return u32(value << 8 | view.byte(offset, 3))

def store_packed_long_reverse(view, offset, value):
    """Original least-significant BYTE first; keep live alias side effects."""
    checked_table(view)
    uint(offset, 16)
    uint(value, 32)
    view.set_byte(offset, low8(value), 3)
    view.set_byte(offset, low8(value >> 8), 2)
    view.set_byte(offset, low8(value >> 16), 1)
    view.set_byte(offset, low8(value >> 24))


# Named RAM views are actual same-domain live tables, never copied records.
for _name,_base in VIEW_BASES.items():
    setattr(SceneState,_name,property(lambda self,base=_base:Table(self,base)))

@dataclass(frozen=True)
class VideoPlaneAddress:
    """A retained video-address carrier, not a dereferenceable RAM pointer."""
    carrier:Long

    def __post_init__(self):
        uint(self.carrier,32)

    @property
    def word(self):
        return low16(self.carrier)

    def advance_full(self,amount):
        uint(amount,32)
        return VideoPlaneAddress(u32(self.carrier+amount))

    def advance_signed(self,amount):
        if type(amount) is not int or not -0x80000000<=amount<=0x7FFFFFFF:
            raise ValueError('signed LONG video stride required')
        return VideoPlaneAddress(u32(self.carrier+amount))

@dataclass(frozen=True)
class StackContinuation:
    """Explicit caller return-token value for a real nonlocal continuation.

    This records a semantic caller fact, not a virtual CPU stack. A recovered
    action can discard its parent continuation only when its original path
    actually does so; unknown callers must supply their own declared token.
    """
    return_carrier:Long

    def __post_init__(self):
        uint(self.return_carrier,32)
