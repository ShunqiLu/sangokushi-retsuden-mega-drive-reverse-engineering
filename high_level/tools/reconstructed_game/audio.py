"""Application ownership of the actual installed driver and the same sound chips.

No startup replay, command injection, default clock, IRQ, R value or timer flag
is supplied here. The rig owns device lifetime; this owner holds only the real
driver-loop claim and its same-AudioState scoped mailbox/rhythm WZ service.
"""
from dataclasses import dataclass
import threading

from tools.high_level_audio_engine.domain import AudioBoundary,AudioState
from tools.high_level_audio_engine.driver_loop import AudioDriverLoopSession
from tools.high_level_audio_engine.driver_startup import AudioDriverStartupSession,Im1ClockGrant
from tools.high_level_audio_engine.hardware_scene import SoundDevice,SharedSoundAudioBus
from tools.high_level_audio_engine.live_cold_driver import LiveColdDriverRig
from tools.high_level_audio_engine.mailbox_wz import MailboxWzService
from tools.high_level_audio_engine.owned_runtime import OwnedAudioDeviceBus
from tools.high_level_audio_engine.psg_device import SegaPsgDevice
from tools.high_level_audio_engine.ymfm_device import YmfmDevice


def _clock_grant(value,maximum,name):
    if type(value)is not int or not 0<=value<=maximum:
        raise ValueError('explicit nonnegative in-range '+name+' required')
    return value


@dataclass(frozen=True)
class AudioChipAdvance:
    """Actual independent device-clock extents, not a guessed common timeline."""
    fm_before: int
    fm_after: int
    fm_native_stereo_frames: int
    psg_before: int
    psg_after: int
    psg_mono_samples: int


class OwnedGameAudio:
    """One linear006F takeover, with explicit software/IRQ/device-clock calls.

    PCM callbacks must already have been selected before fresh chip creation.
    This class never changes them or destroys devices/finishes the parent rig.
    All actions must remain on the owning application/rig thread; callbacks
    cannot re-enter these advancing operations.
    """
    def __init__(self,rig):
        if type(rig)is not LiveColdDriverRig:
            raise ValueError('one actual retained cold-to-driver rig required')
        rig.require_live()
        startup=rig.startup
        if (type(startup)is not AudioDriverStartupSession or startup.sound is not rig.sound
                or startup.state is not rig.audio or startup.scene is not rig.scene
                or startup.control is not rig.control or startup.closed or startup.failed
                or not startup.main_loop_points or not startup.timer_b_continuation
                or startup.waiting is None or startup.waiting.pc!=0x006F
                or startup.program is None or startup.ready_lease is None):
            raise AudioBoundary('actual opt-in startup006F and same live Scene/audio/control required')
        if (type(rig.sound)is not SoundDevice or type(rig.audio)is not AudioState
                or type(rig.audio.bus)is not SharedSoundAudioBus
                or type(rig.devices)is not OwnedAudioDeviceBus
                or type(rig.fm)is not YmfmDevice or type(rig.psg)is not SegaPsgDevice
                or rig.audio.bus.device is not rig.sound or rig.audio.bus.ram is not rig.sound.ram
                or rig.audio.bus.devices is not rig.devices or rig.devices.fm is not rig.fm
                or getattr(rig.devices.psg_write,'__self__',None) is not rig.psg
                or getattr(rig.devices.psg_write,'__func__',None) is not SegaPsgDevice.write
                or rig.audio.platform.control_owner is not rig.control
                or rig.control.sound is not rig.sound):
            raise AudioBoundary('same actual shared RAM, YMFM, PSG and owned audio bus required')
        if getattr(rig.audio,'mailbox_wz_service',None) is not None:
            raise AudioBoundary('cannot replace another actual mailbox WZ owner')
        startup._guard()
        if rig.control.require_frame(startup.ready_lease)!=startup.waiting.frame:
            raise AudioBoundary('actual006F ready lease differs from its suspended frame')

        self.rig,self.startup=rig,startup
        self.scene,self.sound,self.audio,self.control=rig.scene,rig.sound,rig.audio,rig.control
        self.scene_data,self.source=rig.scene.data,rig.source
        self.shared_bus,self.ram,self.devices=rig.audio.bus,rig.sound.ram,rig.devices
        self.fm,self.psg,self.platform=rig.fm,rig.psg,rig.audio.platform
        self.material,self.bank_data=rig.devices.material,rig.devices.material.data
        self.bank_segments=self.bank_data.segments
        self.schedule,self.psg_write,self.transfer=rig.sound.schedule,rig.devices.psg_write,rig.devices.on_transfer
        self.fm_sink,self.psg_sink=rig.fm.pcm_sink,rig.psg.pcm_sink
        self.busy_scheduler=rig.fm.after_status_read
        self.refresh_reader,self.bit_reader=self.platform.refresh_reader,self.platform.memory_bit_reader
        self.generation,self.reset_epoch=rig.control.generation,rig.sound.reset_epoch
        self.thread=threading.get_ident()
        self._closed=self._failed=self._in_call=False
        self._loop=None
        self._wz=MailboxWzService(self.sound)
        self.software_advances=self.im1_deliveries=self.explicit_chip_grants=0
        self._initial_FM_frames=self.fm.generated_frames
        self._initial_PSG_samples=self.psg.generated_samples
        self._chip_snapshot=self._read_chip_counters()
        self._wz.bind()
        try:
            self._loop=AudioDriverLoopSession(startup)
            if (not startup.closed or startup.program is not None or self._loop.program is None
                    or self._loop.origin is not startup or self.control._frame_session is not self._loop):
                raise AudioBoundary('actual006F generator and lease did not transfer linearly')
        except BaseException as error:
            self._failed=True
            self._cleanup(error,constructor=True)
            raise

    @property
    def closed(self):return self._closed

    @property
    def failed(self):return self._failed

    @property
    def waiting(self):
        """The actual driver point, not a copied/host-selected PC or frame."""
        return self._loop.waiting if self._loop is not None else None

    def _read_chip_counters(self):
        return dict(fm_tick=self.fm.tick,psg_tick=self.psg.tick,
            fm_frames=self.fm.generated_frames,psg_samples=self.psg.generated_samples)

    def _require_owned(self):
        if self._closed or self._failed or self._in_call or threading.get_ident()!=self.thread:
            raise AudioBoundary('closed/failed/reentrant/foreign application audio owner')
        self.rig.require_live()
        if (self.rig.startup is not self.startup or self.rig.scene is not self.scene
                or self.rig.sound is not self.sound or self.rig.audio is not self.audio
                or self.rig.control is not self.control or self.rig.fm is not self.fm or self.rig.psg is not self.psg
                or self.rig.source is not self.source or self.scene.data is not self.scene_data
                or self.source.data is not self.scene_data
                or self.audio.bus is not self.shared_bus or self.shared_bus.device is not self.sound
                or self.shared_bus.ram is not self.ram or self.sound.ram is not self.ram
                or self.shared_bus.devices is not self.devices or self.devices.fm is not self.fm
                or self.devices.material is not self.material or self.material.data is not self.bank_data
                or self.bank_data.segments is not self.bank_segments
                or self.sound.schedule is not self.schedule or self.devices.psg_write is not self.psg_write
                or self.devices.on_transfer is not self.transfer or self.audio.platform is not self.platform
                or self.platform.control_owner is not self.control or self.control.sound is not self.sound
                or self.platform.refresh_reader is not self.refresh_reader or self.platform.memory_bit_reader is not self.bit_reader
                or self.fm.pcm_sink is not self.fm_sink or self.psg.pcm_sink is not self.psg_sink
                or self.fm.after_status_read is not self.busy_scheduler
                or self.sound.reset_epoch!=self.reset_epoch or self.control.generation!=self.generation
                or self._loop is None or self._loop.closed or self._loop.failed
                or not self.startup.closed or self.startup.program is not None
                or self.sound.executing):
            raise AudioBoundary('actual application audio State/device/source/provider ownership changed')
        self._wz.require_bound(self.sound)
        self.control.require_frame_session(self._loop,self.generation,self.reset_epoch)

    def _execute(self,operation,*arguments):
        self._in_call=True
        try:
            result=operation(*arguments)
            self._chip_snapshot=self._read_chip_counters()
            return result
        except BaseException as error:
            self._failed=True
            self._in_call=False
            try:self._chip_snapshot=self._read_chip_counters()
            except BaseException as observation_error:
                error.add_note('last audio chip counters unavailable: '+str(observation_error))
            self._cleanup(error)
            raise
        finally:
            self._in_call=False

    def advance(self):
        """Run only the original driver to its next registered software point.

        Original status reads may consume the caller's preconfigured finite
        BUSY scheduler. This method adds no chip clocks or timer/IRQ grants.
        """
        self._require_owned()
        point=self._execute(self._loop.advance)
        self.software_advances+=1
        return point

    def deliver_im1(self,grant):
        """Deliver only an explicit matching, monotonic actual0073 IM1 grant."""
        self._require_owned()
        if (type(grant)is not Im1ClockGrant or self.waiting.pc!=0x0073
                or grant.clock_hz!=self._loop.irq_clock_hz or grant.timestamp<=self._loop.irq_clock):
            raise AudioBoundary('explicit matching monotonic IM1 grant at the actual0073 point required')
        point=self._execute(self._loop.deliver_im1,grant)
        self.im1_deliveries+=1
        return point

    def advance_chips(self,*,fm_ticks,psg_input_clocks):
        """Grant both explicitly supplied independent clock extents, in FM/PSG order.

        Zero explicitly means no clocks for that device. There is no inferred
        ratio, automatic audio-driver update, timer-ready result or rollback.
        PCM goes only to the callbacks selected before fresh chip construction.
        """
        self._require_owned()
        _clock_grant(fm_ticks,(1<<64)-145,'FM clock grant')
        _clock_grant(psg_input_clocks,(1<<63)-1,'PSG input-clock grant')
        _clock_grant(self.fm.tick+fm_ticks,(1<<64)-145,'FM target clock')
        return self._execute(self._advance_chips,fm_ticks,psg_input_clocks)

    def _advance_chips(self,fm_ticks,psg_input_clocks):
        before=self._read_chip_counters()
        generated=self.fm.advance(fm_ticks)
        self.psg.advance(psg_input_clocks)
        after=self._read_chip_counters()
        if (after['fm_tick']-before['fm_tick']!=fm_ticks or after['psg_tick']-before['psg_tick']!=psg_input_clocks
                or after['fm_frames']-before['fm_frames']!=generated):
            raise AudioBoundary('actual explicit chip-clock or PCM extent differs')
        self.explicit_chip_grants+=1
        return AudioChipAdvance(before['fm_tick'],after['fm_tick'],generated,
            before['psg_tick'],after['psg_tick'],after['psg_samples']-before['psg_samples'])

    def diagnostics(self):
        """Compact counters only; no RAM/trace copy, timer/status read or progress."""
        if threading.get_ident()!=self.thread:raise AudioBoundary('audio diagnostics belong to the actual owning thread')
        counters=self._chip_snapshot if self._closed or self._failed else self._read_chip_counters()
        point=self.waiting
        return dict(closed=self.closed,failed=self.failed,
            actual_point=None if point is None else point.pc,
            reset_epoch=self.reset_epoch,generation=self.generation,
            software_advances=self.software_advances,IM1_deliveries=self.im1_deliveries,
            explicit_chip_grants=self.explicit_chip_grants,
            FM_input_clock=counters['fm_tick'],PSG_input_clock=counters['psg_tick'],
            generated_FM_native_stereo_frames=counters['fm_frames'],
            generated_PSG_mono_samples=counters['psg_samples'],
            generated_FM_frames_since_takeover=counters['fm_frames']-self._initial_FM_frames,
            generated_PSG_samples_since_takeover=counters['psg_samples']-self._initial_PSG_samples,
            FM_PCM_sink_configured=self.fm_sink is not None,PSG_PCM_sink_configured=self.psg_sink is not None,
            WZ_events=len(self._wz.events),driver_events=0 if self._loop is None else len(self._loop.events),
            scoped_continuation_events=0 if self._loop is None else len(self._loop.continuation_events),
            PSG_writes=len(self.psg.events),FM_register_or_address_events=len(self.fm.events),
            audible_host_output_claimed=False,implicit_clock_or_IRQ_grants=0)

    def _cleanup(self,primary=None,*,constructor=False):
        errors=[]
        loop=self._loop
        # If the exact constructor failed after claiming but before returning,
        # release only that same-startup partial owner; never a foreign claim.
        if constructor and loop is None:
            candidate=self.control._frame_session
            if type(candidate)is AudioDriverLoopSession and candidate.origin is self.startup:
                loop=candidate
        if loop is not None:
            try:
                if loop.program is not None:loop.close()
                elif constructor:
                    self.control.abandon_frame_session(loop,reason='actual audio takeover constructor failed')
                    self.startup.close()
            except BaseException as error:errors.append(error)
            finally:
                # close() itself may fail while closing the generator. End only
                # this exact managed claim using the original control API.
                if self.control._frame_session is loop:
                    try:self.control.abandon_frame_session(loop,reason='application audio explicitly terminated')
                    except BaseException as error:errors.append(error)
        try:
            if getattr(self.audio,'mailbox_wz_service',None) is self._wz:
                self._wz.unbind()
            elif getattr(self.audio,'mailbox_wz_service',None) is not None:
                raise AudioBoundary('foreign WZ owner cannot be removed by application audio cleanup')
        except BaseException as error:errors.append(error)
        released=((loop is None or self.control._frame_session is not loop) and
            getattr(self.audio,'mailbox_wz_service',None) is not self._wz)
        self._closed=released and not errors
        if errors:
            if primary is not None:
                for error in errors:primary.add_note('application audio cleanup boundary: '+type(error).__name__+': '+str(error))
            else:raise BaseExceptionGroup('application audio cleanup did not finish',errors)

    def close(self):
        """Release only this loop/WZ, before the application calls rig.finish()."""
        if threading.get_ident()!=self.thread or self._in_call:
            raise AudioBoundary('only an inactive owning application thread may close audio')
        if not self._closed:self._cleanup()

    def __enter__(self):
        self._require_owned()
        return self

    def __exit__(self,error_type,error,traceback):
        if error is None:self.close()
        else:
            self._failed=True
            if threading.get_ident()!=self.thread or self._in_call:
                error.add_note('application audio cleanup requires the inactive owning thread')
            else:self._cleanup(error)
        return False
