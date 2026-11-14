"""Optional Windows PCM endpoint; it never schedules a game or sound chip.

Only explicitly selected speakers mode loads WinMM. The application thread
submits actual little-endian signed16 samples, retains every prepared buffer,
and releases it only after the driver returns it. No worker calls game code.
OS output mixing/conversion is outside original-console fidelity claims.
"""
from collections import deque
import ctypes
from dataclasses import dataclass
import sys
import threading


class SpeakerError(RuntimeError):
    """A device/queue failure, not permission to discard actual PCM silently."""


class _WaveFormat(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('format', ctypes.c_uint16), ('channels', ctypes.c_uint16),
        ('rate', ctypes.c_uint32), ('bytes_per_second', ctypes.c_uint32),
        ('block_align', ctypes.c_uint16), ('bits', ctypes.c_uint16),
        ('extra_size', ctypes.c_uint16)]


class _WaveHeader(ctypes.Structure):
    pass


_WaveHeader._fields_ = [('data', ctypes.c_void_p), ('length', ctypes.c_uint32),
    ('recorded', ctypes.c_uint32), ('user', ctypes.c_size_t),
    ('flags', ctypes.c_uint32), ('loops', ctypes.c_uint32),
    ('next', ctypes.POINTER(_WaveHeader)), ('reserved', ctypes.c_size_t)]

_DONE, _PREPARED, _IN_QUEUE = 1, 2, 16
# Native-owned allocations must survive even a failed reset/unprepare/close.
# Deliberately bounded by each stream's finite queue, never a game-state cache.
_FAILED_NATIVE_OWNERS = []


@dataclass
class _Block:
    backing: object
    header: _WaveHeader
    frames: int
    submitted: bool = False


def _positive(value, label, maximum):
    if type(value) is not int or not 1 <= value <= maximum:
        raise ValueError('explicit in-range ' + label + ' required')
    return value


def _winmm():
    if sys.platform != 'win32':
        raise SpeakerError('speakers 模式目前仅支持 Windows；不会自动改成静音或 WAV。')
    # System32-only loading: no project DLL or arbitrary PATH search.
    library = ctypes.WinDLL('winmm.dll', winmode=0x00000800)
    handle, header = ctypes.c_void_p, ctypes.POINTER(_WaveHeader)
    definitions = {
        'waveOutOpen': [ctypes.POINTER(handle), ctypes.c_uint32,
            ctypes.POINTER(_WaveFormat), ctypes.c_size_t, ctypes.c_size_t, ctypes.c_uint32],
        'waveOutPrepareHeader': [handle, header, ctypes.c_uint32],
        'waveOutWrite': [handle, header, ctypes.c_uint32],
        'waveOutUnprepareHeader': [handle, header, ctypes.c_uint32],
        'waveOutReset': [handle], 'waveOutClose': [handle],
    }
    for name, arguments in definitions.items():
        function = getattr(library, name)
        function.argtypes, function.restype = arguments, ctypes.c_uint32
    return library


class WindowsPcmStream:
    """One native-rate mono/stereo stream with a bounded nonblocking queue.

    There is no fallback, callback into Python, hidden sleep or sample dropping.
    A producer outrunning the declared host queue stops with a visible error;
    it cannot use speaker completion as a grant of console time.
    """
    def __init__(self, *, channels, rate, device_id, max_queued_ms):
        if type(channels) is not int or channels not in (1, 2):
            raise ValueError('one explicit mono/stereo PCM channel count required')
        self.rate = _positive(rate, 'PCM rate', 1_000_000)
        _positive(max_queued_ms, 'speaker queue milliseconds', 10_000)
        if type(device_id) is not int or not -1 <= device_id <= 0xFFFFFFFE:
            raise ValueError('explicit Windows device ID or -1 mapper required')
        self.channels, self.device_id = channels, device_id
        self.max_queued_frames = (rate * max_queued_ms + 999) // 1000
        self.thread, self.closed, self.failed = threading.get_ident(), False, False
        self.blocks, self.queued_frames = deque(), 0
        self.submitted_frames = self.returned_frames = self.reset_returned_frames = 0
        self.handle, self.library = ctypes.c_void_p(), _winmm()
        alignment = channels * 2
        format_ = _WaveFormat(1, channels, rate, rate * alignment, alignment, 16, 0)
        # CALLBACK_NULL: flags are inspected only on the owning application
        # thread. The OS may mix/convert; game PCM and chip rates stay intact.
        self._call('waveOutOpen', ctypes.byref(self.handle), device_id & 0xFFFFFFFF,
            ctypes.byref(format_), 0, 0, 0)

    def _call(self, name, *arguments):
        result = getattr(self.library, name)(*arguments)
        if result:
            self.failed = True
            raise SpeakerError(name + ' 失败，Windows 音频错误码 ' + str(result))

    def _thread(self):
        if threading.get_ident() != self.thread:
            raise SpeakerError('扬声器输出只能由所属游戏线程操作。')

    def _reap(self):
        while self.blocks and self.blocks[0].header.flags & _DONE:
            block = self.blocks[0]
            self._call('waveOutUnprepareHeader', self.handle,
                ctypes.byref(block.header), ctypes.sizeof(_WaveHeader))
            self.blocks.popleft()
            self.queued_frames -= block.frames
            self.returned_frames += block.frames

    def write_pcm(self, raw):
        self._thread()
        if self.closed or self.failed:
            raise SpeakerError('扬声器输出已经关闭或失败，不能重放音频前缀。')
        if type(raw) is not bytes or len(raw) % (self.channels * 2):
            raise ValueError('complete little-endian signed16 PCM frames required')
        if not raw:
            return
        self._reap()
        frames = len(raw) // (self.channels * 2)
        if (self.queued_frames + frames > self.max_queued_frames
                or len(self.blocks) >= 4096 or len(raw) > 0xFFFFFFFF):
            self.failed = True
            raise SpeakerError('扬声器有界队列已满；未丢弃样本、补静音或推进游戏时钟。')
        backing = ctypes.create_string_buffer(raw, len(raw))
        header = _WaveHeader()
        header.data, header.length = ctypes.addressof(backing), len(raw)
        block = _Block(backing, header, frames)
        # Retain before preparation: even a subsequent native error must not
        # free a prepared/native-referenced allocation through Python GC.
        self.blocks.append(block)
        self.queued_frames += frames
        self._call('waveOutPrepareHeader', self.handle,
            ctypes.byref(header), ctypes.sizeof(_WaveHeader))
        self._call('waveOutWrite', self.handle,
            ctypes.byref(header), ctypes.sizeof(_WaveHeader))
        block.submitted = True
        self.submitted_frames += frames

    def diagnostics(self):
        return dict(channels=self.channels, sample_rate_hz=self.rate,
            device_id=self.device_id, closed=self.closed, failed=self.failed,
            submitted_frames=self.submitted_frames,
            returned_buffer_frames=self.returned_frames,
            reset_returned_buffer_frames=self.reset_returned_frames,
            unreaped_queue_frames=self.queued_frames,
            max_queued_frames=self.max_queued_frames,
            listening_or_original_audio_fidelity_verified=False)

    def close(self):
        if self.closed:
            return
        try:
            self._thread()
            # A user close cancels the finite host playback tail, not the game
            # sound state. Reset returns queued buffers before unpreparation.
            self._reap()
            self._call('waveOutReset', self.handle)
            while self.blocks:
                block = self.blocks[0]
                if block.header.flags & _IN_QUEUE:
                    raise SpeakerError('Windows 尚未归还音频缓冲区；保留内存，不强行释放。')
                if block.header.flags & _PREPARED:
                    self._call('waveOutUnprepareHeader', self.handle,
                        ctypes.byref(block.header), ctypes.sizeof(_WaveHeader))
                self.blocks.popleft()
                self.queued_frames -= block.frames
                if block.submitted:
                    self.reset_returned_frames += block.frames
            self._call('waveOutClose', self.handle)
            self.handle = ctypes.c_void_p()
            self.closed = True
            if self in _FAILED_NATIVE_OWNERS:
                _FAILED_NATIVE_OWNERS.remove(self)
        except BaseException:
            self.failed = True
            if self not in _FAILED_NATIVE_OWNERS:
                _FAILED_NATIVE_OWNERS.append(self)
            raise
