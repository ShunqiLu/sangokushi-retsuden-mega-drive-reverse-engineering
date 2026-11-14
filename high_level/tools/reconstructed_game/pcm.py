"""Explicit separate FM/PSG PCM outputs, selected before chip construction.

This output boundary does not clock chips, mix/resample channels, install RAM
or select commands. Optional Windows speakers receive the same actual PCM;
native FM stereo and PSG mono stay separate until the operating-system mixer.
"""
from array import array
import sys
import wave


class PcmOutputs:
    """Bounded fresh WAV capture, optional speakers, or explicit discard."""

    def __init__(self, config):
        self.config = config
        self.closed = False
        self.fm_frames = self.psg_frames = 0
        self._streams, self._waves, self._speakers, self._writers = [], [], [], []
        self.fm_sink = self.psg_sink = None
        if config.mode == 'discard':
            return
        if config.mode == 'speakers':
            self._open_speakers()
            return
        if config.mode != 'wav':
            raise ValueError('PCM mode must explicitly be discard, wav or speakers')
        if config.fm_path == config.psg_path:
            raise ValueError('FM and PSG output paths must differ')
        try:
            for path, channels, rate in ((config.fm_path, 2, config.fm_sample_rate_hz),
                    (config.psg_path, 1, config.psg_sample_rate_hz)):
                raw = path.open('xb')
                self._streams.append(raw)
                output = wave.open(raw, 'wb')
                self._waves.append(output)
                output.setnchannels(channels)
                output.setsampwidth(2)
                output.setframerate(rate)
                self._writers.append(output.writeframesraw)
            self.fm_sink, self.psg_sink = self._fm, self._psg
        except BaseException as error:
            try:
                self.close()
            except BaseException as cleanup:
                error.add_note('PCM partial-open cleanup: ' + str(cleanup))
            raise

    def _open_speakers(self):
        from .speakers import WindowsPcmStream
        try:
            for channels, rate in ((2, self.config.fm_sample_rate_hz),
                    (1, self.config.psg_sample_rate_hz)):
                output = WindowsPcmStream(channels=channels, rate=rate,
                    device_id=self.config.device_id, max_queued_ms=self.config.max_queued_ms)
                self._speakers.append(output)
                self._writers.append(output.write_pcm)
            self.fm_sink, self.psg_sink = self._fm, self._psg
        except BaseException as error:
            try:
                self.close()
            except BaseException as cleanup:
                error.add_note('Speaker partial-open cleanup: ' + str(cleanup))
            raise

    def require_rates(self, fm, psg):
        """Output rates are explicit; no program-side resampling/clock inference."""
        if self.config.mode in ('wav', 'speakers') and (
                self.config.fm_sample_rate_hz != fm.native_sample_rate_floor
                or self.config.psg_sample_rate_hz != psg.sample_rate_hz):
            raise ValueError('PCM rates must match actual FM native-rate floor and PSG configured rate')

    def _write(self, samples, *, channels, count, limit, output):
        if self.closed or type(samples) is not array or samples.typecode != 'h' or samples.itemsize != 2:
            raise ValueError('live signed16 PCM array output required')
        if len(samples) % channels:
            raise ValueError('complete PCM channel frames required')
        frames = len(samples) // channels
        if count + frames > limit:
            raise RuntimeError('explicit finite PCM frame allowance exhausted')
        # Chip arrays have host endian storage; both output APIs use little endian.
        data = samples
        if sys.byteorder != 'little':
            data = array('h', samples)
            data.byteswap()
        output(data.tobytes())
        return frames

    def _fm(self, samples):
        self.fm_frames += self._write(samples, channels=2, count=self.fm_frames,
            limit=self.config.max_fm_frames, output=self._writers[0])

    def _psg(self, samples):
        self.psg_frames += self._write(samples, channels=1, count=self.psg_frames,
            limit=self.config.max_psg_frames, output=self._writers[1])

    def diagnostics(self):
        return dict(mode=self.config.mode, closed=self.closed,
            fm_stereo_frames=self.fm_frames, psg_mono_frames=self.psg_frames,
            host_speaker_playback=self.config.mode == 'speakers', mixing_or_resampling=False,
            OS_mixing_or_resampling_may_apply=self.config.mode == 'speakers',
            speakers=[owner.diagnostics() for owner in self._speakers],
            host_listening_verified=False,
            FM_WAV_rate_is_explicit_native_floor_not_exact_rational_clock=True)

    def close(self):
        if self.closed:
            return
        errors = []
        for owner in self._speakers + self._waves + self._streams:
            try:
                owner.close()
            except BaseException as error:
                errors.append(error)
        self.closed = not errors
        if errors:
            raise errors[0]
