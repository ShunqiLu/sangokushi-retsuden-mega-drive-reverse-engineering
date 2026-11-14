"""Explicit-clock YM2612 ports and stereo PCM, using the BSD YMFM chip core.

This does not execute Z80/68000 instructions, supply a song, guess frame timing,
or read a ROM. The recovered Python driver remains the only game-music owner.
"""
from array import array
import ctypes
from pathlib import Path
import sys
import wave

from .domain import byte
from .fm_ports import FmPortDevice


SAMPLE_CLOCKS = 144


def _integer(value, name, maximum=(1 << 64) - 145):
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError('explicit nonnegative in-range ' + name + ' required')
    return value


def _load_library(path):
    if not isinstance(path, Path) or not path.is_absolute() or not path.is_file():
        raise ValueError('explicit existing absolute host chip-library Path required')
    library = ctypes.CDLL(str(path))
    signatures = {
        'abi': (ctypes.c_uint32, []),
        'create': (ctypes.c_void_p, [ctypes.c_uint32]),
        'destroy': (None, [ctypes.c_void_p]),
        'clock': (ctypes.c_uint64, [ctypes.c_void_p]),
        'busy_end': (ctypes.c_uint64, [ctypes.c_void_p]),
        'native_rate': (ctypes.c_uint32, [ctypes.c_void_p]),
        'status': (ctypes.c_uint32, [ctypes.c_void_p]),
        'irq': (ctypes.c_uint32, [ctypes.c_void_p]),
        'write': (ctypes.c_int32, [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32]),
        'advance': (ctypes.c_int64, [ctypes.c_void_p, ctypes.c_uint64,
                                   ctypes.POINTER(ctypes.c_int16), ctypes.c_uint64]),
    }
    for name, (returned, parameters) in signatures.items():
        function = getattr(library, 'g5510_ymfm_' + name)
        function.restype, function.argtypes = returned, parameters
    if library.g5510_ymfm_abi() != 1:
        raise ValueError('unsupported YMFM bridge ABI')
    return library


class YmfmDevice(FmPortDevice):
    """One live FM chip, with real core BUSY/timers and caller-supplied clocks.

    The PCM sink receives native-rate interleaved signed-16 stereo arrays. A
    sink of None explicitly discards audio. No clock profile or status-read
    scheduler is selected by default; after_status_read may grant real clocks.
    This owner is single-threaded, as is the recovered active sound invocation.
    """

    def __init__(self, library: Path, *, clock_hz, pcm_sink, after_status_read=None):
        _integer(clock_hz, 'chip input clock frequency', (1 << 32) - 1)
        if clock_hz < SAMPLE_CLOCKS:
            raise ValueError('chip input clock must permit native PCM generation')
        if pcm_sink is not None and not callable(pcm_sink):
            raise ValueError('explicit PCM sink or explicit None required')
        if after_status_read is not None and not callable(after_status_read):
            raise ValueError('explicit external clock scheduler required')
        self._library = _load_library(library)
        self._owner = self._library.g5510_ymfm_create(clock_hz)
        if not self._owner:
            raise RuntimeError('cannot allocate YM2612 chip owner')
        self.clock_hz, self.pcm_sink = clock_hz, pcm_sink
        self.after_status_read = after_status_read
        self.registers, self.address_latches = bytearray(512), bytearray(2)
        self.events, self.status_reads = [], []
        self.generated_frames = 0

    def _live(self):
        if not self._owner:
            raise RuntimeError('closed FM chip owner')
        return self._owner

    @property
    def tick(self):
        return self._library.g5510_ymfm_clock(self._live())

    @property
    def busy_until(self):
        return self._library.g5510_ymfm_busy_end(self._live())

    @property
    def timer_flags(self):
        return self._library.g5510_ymfm_status(self._live()) & 3

    @property
    def irq(self):
        return bool(self._library.g5510_ymfm_irq(self._live()))

    @property
    def native_sample_rate_floor(self):
        return self._library.g5510_ymfm_native_rate(self._live())

    def read_status(self):
        value = self._library.g5510_ymfm_status(self._live())
        self.status_reads.append((self.tick, value))
        if self.after_status_read is not None:
            self.after_status_read(self, value)
        return value

    def write(self, port, value):
        byte(value)
        if type(port) is not int or not 0 <= port <= 3:
            raise ValueError('actual FM port index required')
        now = self.tick
        if self._library.g5510_ymfm_write(self._live(), port, value):
            raise RuntimeError('FM port write rejected')
        bank = port // 2
        if port & 1:
            register = self.address_latches[bank]
            self.registers[bank * 256 + register] = value
            self.events.append(('register', now, bank, register, value))
        else:
            self.address_latches[bank] = value
            self.events.append(('address', now, bank, value))

    def advance(self, ticks):
        """Grant input clocks; generate at exact 144-clock native boundaries."""
        _integer(ticks, 'chip-clock grant')
        target = _integer(self.tick + ticks, 'target chip clock')
        total = 0
        while self.tick < target:
            end = min(target, self.tick + SAMPLE_CLOCKS * 8192)
            needed = end // SAMPLE_CLOCKS - self.tick // SAMPLE_CLOCKS
            samples = (ctypes.c_int16 * (needed * 2))()
            actual = self._library.g5510_ymfm_advance(self._live(), end, samples, needed)
            if actual != needed:
                raise RuntimeError('chip clock advance returned an inconsistent PCM extent')
            self.generated_frames += actual
            total += actual
            if actual and self.pcm_sink is not None:
                self.pcm_sink(array('h', samples))
        return total

    def close(self):
        if self._owner:
            self._library.g5510_ymfm_destroy(self._owner)
            self._owner = None

    def __enter__(self):
        self._live()
        return self

    def __exit__(self, *unused):
        self.close()


def write_stereo_wave(path: Path, pcm: array, *, clock_hz, sample_rate):
    """Fresh WAV, with explicit rational-clock, zero-order-hold resampling.

    Native frames represent [n*144,(n+1)*144) chip clocks. This deliberately
    simple output adapter is not an analog filter or a fidelity comparison.
    """
    if not isinstance(path, Path) or path.exists() or not path.parent.is_dir():
        raise ValueError('new audio artifact in an existing output directory required')
    if type(pcm) is not array or pcm.typecode != 'h' or len(pcm) % 2:
        raise ValueError('complete native signed-16 stereo frames required')
    _integer(clock_hz, 'chip input clock frequency', (1 << 32) - 1)
    _integer(sample_rate, 'output PCM sample rate', (1 << 31) - 1)
    if clock_hz < SAMPLE_CLOCKS or sample_rate == 0:
        raise ValueError('positive usable native/output frequencies required')
    native_frames = len(pcm) // 2
    count = native_frames * SAMPLE_CLOCKS * sample_rate // clock_hz
    output = array('h')
    for index in range(count):
        source = index * clock_hz // (sample_rate * SAMPLE_CLOCKS)
        output.extend(pcm[source * 2:source * 2 + 2])
    if sys.byteorder != 'little':
        output.byteswap()
    with path.open('xb') as stream, wave.open(stream, 'wb') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(output.tobytes())
    return count
