"""Independent Sega-integrated PSG digital model with explicit host clocks.

This is new device support, not recovered original-game CODE. See README_PSG
and psg_sources.json for probable digital behavior and unverified analog scope.
No emulator source, hidden reset profile or CPU execution is embedded here.
"""
from array import array
from dataclasses import dataclass


def _integer(value, minimum, maximum, name):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f'{name} must be an integer in {minimum}..{maximum}')
    return value


def _values(value, length, minimum, maximum, name):
    if not isinstance(value, tuple) or len(value) != length:
        raise ValueError(f'{name} must be an explicit {length}-item tuple')
    return tuple(_integer(item, minimum, maximum, name) for item in value)


@dataclass(frozen=True)
class SegaPsgState:
    """Editable digital state; there is intentionally no guessed reset default.

    Counters count internal /16 clocks remaining. Zero means expiration at
    the next internal clock, not at construction or at a register write.
    tone_outputs and noise_clock are digital 0/1 phases, not analog voltages.
    """
    tone_periods: tuple
    attenuation: tuple
    latched_register: int
    tone_counters: tuple
    tone_outputs: tuple
    noise_control: int
    noise_counter: int
    noise_clock: int
    noise_lfsr: int
    divider_remainder: int


@dataclass(frozen=True)
class PsgWriteEvent:
    input_clock: int
    value: int
    register: int
    before: int
    after: int


class SegaPsgDevice:
    """One Sega 16-bit-noise PSG, independent of ROM, scene, FM or CPUs.

    All clock and PCM parameters are required. sample_rate_hz cannot exceed
    clock_hz. PCM is unipolar, nominal 2 dB attenuation, point sampled after
    an internal edge when the two boundaries coincide. This transparent first
    output adapter is not an analog board model or an anti-aliasing filter.
    One owner must serialize write/advance calls and must not re-enter a sink.
    """
    def __init__(self, initial_state, *, clock_hz, sample_rate_hz,
                 channel_gain, pcm_sink):
        if not isinstance(initial_state, SegaPsgState):
            raise ValueError('explicit SegaPsgState required')
        self.clock_hz = _integer(clock_hz, 1, 2**63 - 1, 'clock_hz')
        self.sample_rate_hz = _integer(sample_rate_hz, 1, clock_hz, 'sample_rate_hz')
        self.channel_gain = _values(channel_gain, 4, 0, 32767, 'channel_gain')
        if sum(channel_gain) > 32767:
            raise ValueError('sum of channel_gain must fit signed 16-bit PCM')
        if pcm_sink is not None and not callable(pcm_sink):
            raise ValueError('pcm_sink must be callable or explicitly None')
        self.pcm_sink = pcm_sink
        self._periods = list(_values(initial_state.tone_periods, 3, 0, 1023, 'tone_periods'))
        self._attenuation = list(_values(initial_state.attenuation, 4, 0, 15, 'attenuation'))
        self._latch = _integer(initial_state.latched_register, 0, 7, 'latched_register')
        self._tone_counters = list(_values(initial_state.tone_counters, 3, 0, 1023, 'tone_counters'))
        self._tone_outputs = list(_values(initial_state.tone_outputs, 3, 0, 1, 'tone_outputs'))
        self._noise_control = _integer(initial_state.noise_control, 0, 7, 'noise_control')
        self._noise_counter = _integer(initial_state.noise_counter, 0, 1023, 'noise_counter')
        self._noise_clock = _integer(initial_state.noise_clock, 0, 1, 'noise_clock')
        self._noise_lfsr = _integer(initial_state.noise_lfsr, 0, 65535, 'noise_lfsr')
        self._divider_remainder = _integer(initial_state.divider_remainder, 0, 15, 'divider_remainder')
        self._levels = tuple(tuple(0 if attenuation == 15 else
            round(gain * 10 ** (-attenuation / 10)) for attenuation in range(16))
            for gain in channel_gain)
        self.tick = 0
        self.generated_samples = 0
        self.internal_ticks = 0
        self.noise_shifts = 0
        self.events = []
        self._active = False

    @property
    def state(self):
        """Immutable snapshot; editing it requires an explicit new device."""
        return SegaPsgState(tuple(self._periods), tuple(self._attenuation), self._latch,
            tuple(self._tone_counters), tuple(self._tone_outputs), self._noise_control,
            self._noise_counter, self._noise_clock, self._noise_lfsr,
            self._divider_remainder)

    def _register(self, register):
        if register & 1:
            return self._attenuation[register >> 1]
        return self._noise_control if register == 6 else self._periods[register >> 1]

    def write(self, value):
        """Accept a bus byte at the current clock; never advance time implicitly."""
        if self._active:
            raise RuntimeError('PSG sink must not re-enter its device')
        _integer(value, 0, 255, 'PSG byte')
        if value & 0x80:
            self._latch = (value >> 4) & 7
        register = self._latch
        before = self._register(register)
        if register & 1:
            self._attenuation[register >> 1] = value & 15
        elif register == 6:
            self._noise_control = value & 7
            self._noise_lfsr = 0x8000
            # Probable integrated-Sega phase rule: noise control keeps its
            # flip-flop phase; Tone2 mode aligns remaining counter time only.
            if (value & 3) == 3:
                self._noise_counter = self._tone_counters[2]
        else:
            channel = register >> 1
            self._periods[channel] = ((before & 0x3f0) | (value & 15)
                if value & 0x80 else (before & 15) | ((value & 63) << 4))
        self.events.append(PsgWriteEvent(self.tick, value, register, before,
                                        self._register(register)))

    def sample(self):
        """Current unipolar mono level; reading it does not advance any clock."""
        bits = (*self._tone_outputs, self._noise_lfsr & 1)
        return sum(bit * self._levels[channel][self._attenuation[channel]]
                   for channel, bit in enumerate(bits))

    def _counter_tick(self):
        self.internal_ticks += 1
        for channel in range(3):
            if self._tone_counters[channel] <= 1:
                # Integrated Sega zero period is one, not TI's 0x400.
                self._tone_counters[channel] = max(1, self._periods[channel])
                self._tone_outputs[channel] ^= 1
            else:
                self._tone_counters[channel] -= 1
        if self._noise_counter > 1:
            self._noise_counter -= 1
            return
        selector = self._noise_control & 3
        self._noise_counter = (max(1, self._periods[2]) if selector == 3
                               else 16 << selector)
        self._noise_clock ^= 1
        if self._noise_clock:
            low = self._noise_lfsr & 1
            feedback = low ^ ((self._noise_lfsr >> 3) & 1) if self._noise_control & 4 else low
            self._noise_lfsr = (self._noise_lfsr >> 1) | (feedback << 15)
            self.noise_shifts += 1

    def advance(self, input_clocks):
        """Advance exactly n supplied clocks and emit signed-16 mono chunks.

        Samples occur at ceil(k*clock_hz/sample_rate_hz), k starting at one.
        Divider remainder and absolute sample boundaries survive split calls.
        A None sink explicitly discards samples but does not suppress clocks.
        """
        _integer(input_clocks, 0, 2**63 - 1, 'input_clocks')
        if self._active:
            raise RuntimeError('PSG sink must not re-enter its device')
        self._active = True
        try:
            end = self.tick + input_clocks
            pending = array('h')
            while self.tick < end:
                next_sample = ((self.generated_samples + 1) * self.clock_hz
                               + self.sample_rate_hz - 1) // self.sample_rate_hz
                step = min(end - self.tick, 16 - self._divider_remainder,
                           next_sample - self.tick)
                self.tick += step
                self._divider_remainder += step
                if self._divider_remainder == 16:
                    self._divider_remainder = 0
                    self._counter_tick()
                if self.tick == next_sample:
                    pending.append(self.sample())
                    self.generated_samples += 1
                    if len(pending) == 4096:
                        if self.pcm_sink is not None:
                            self.pcm_sink(pending)
                        pending = array('h')
            if pending and self.pcm_sink is not None:
                self.pcm_sink(pending)
        finally:
            self._active = False
