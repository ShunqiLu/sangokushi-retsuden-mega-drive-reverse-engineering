"""Explicit bounded Z80 control/reset ownership, not a CPU execution model."""
from dataclasses import dataclass, replace

from tools.high_level_audio_engine.domain import AudioBoundary, AudioPlatform, byte, word
from tools.high_level_audio_engine.hardware_scene import SoundDevice, SoundSchedule
from tools.high_level_audio_engine.owned_runtime import DriverFrame, run_driver_stage


@dataclass(frozen=True)
class AudioControlState:
    """Explicit control state; None means unknown, not an invented reset value.

    pc_entry is a bounded semantic entry location, not a per-instruction PC.
    General/alternate registers, flags, RAM and sound chips are not owned here.
    """
    pc_entry: object
    interrupt_vector: object
    refresh: object
    iff1: object
    iff2: object
    interrupt_mode: object
    ei_deferred: object

    def __post_init__(self):
        for name, validator in (('pc_entry', word), ('interrupt_vector', byte),
                                ('refresh', byte)):
            value = getattr(self, name)
            if value is not None:
                validator(value)
        if self.interrupt_mode is not None and (type(self.interrupt_mode) is not int
                                                or self.interrupt_mode not in (0, 1, 2)):
            raise ValueError('interrupt_mode must be explicit 0/1/2 or unknown None')
        for name in ('iff1', 'iff2', 'ei_deferred'):
            if getattr(self, name) is not None and type(getattr(self, name)) is not bool:
                raise ValueError(name + ' must be bool or unknown None')


@dataclass(frozen=True)
class AudioFrameLease:
    """Managed semantic carrier valid for only one owner/generation/epoch."""
    owner_token: object
    generation: int
    reset_epoch: int
    entry_kind: str
    frame: DriverFrame


class AudioEntryAuthority:
    """Caller-owned source installation/startup evidence; never defaults ready.

    An implementation must actually establish its named entry and return its
    complete frame. A fixture authority is explicitly experimental, not proof
    that the game's startup ran. This service never infers executable readiness
    merely from RAM contents or a reset release.
    """
    def provide_frame(self, sound, entry_kind, entry_address, control_state):
        raise AudioBoundary('actual audio entry installation/startup authority is unbound')


class AudioControlOwner:
    def __init__(self, initial_state, *, reset_asserted):
        if type(initial_state) is not AudioControlState or type(reset_asserted) is not bool:
            raise ValueError('explicit control state and initial RESET line required')
        self.control = initial_state
        self.reset_asserted = reset_asserted
        self.phase = 'reset-held' if reset_asserted else 'quiescent'
        self.generation, self.reset_clocks = 0, 0
        self.sound, self._lease, self._frame_session = None, None, None
        self._token, self.events = object(), []

    def bind(self, sound):
        if type(sound) is not SoundDevice:
            raise ValueError('one exact shared-RAM SoundDevice required')
        if self.sound is not None and self.sound is not sound:
            raise ValueError('control owner already belongs to another sound state')
        platform = sound.audio_state.platform
        if not isinstance(platform, AudioPlatform) or getattr(platform, 'control_owner', None) is not self:
            raise ValueError('same explicitly delegated AudioPlatform control owner required')
        if sound.reset_asserted != self.reset_asserted:
            raise ValueError('initial RESET state differs from actual SoundDevice')
        self.sound = sound
        return self

    def _bound(self, sound=None):
        if self.sound is None or (sound is not None and sound is not self.sound):
            raise AudioBoundary('audio control operation belongs to another/unbound sound')
        return self.sound

    def reset_changed(self, sound, asserted):
        self._bound(sound)
        if type(asserted) is not bool or asserted == self.reset_asserted:
            raise AudioBoundary('actual RESET transition required')
        if sound.executing:
            raise AudioBoundary('RESET cannot discard an active semantic continuation')
        if asserted:
            self.generation += 1
            self._lease = self._frame_session = None
            self.reset_clocks = 0
            self.phase, self.reset_asserted = 'reset-held', True
            self.events.append(('reset_asserted', sound.reset_epoch, self.generation))
        else:
            if self.phase != 'reset-held' or self.reset_clocks < 3:
                raise AudioBoundary('RESET release requires at least three explicitly supplied Z80 clocks')
            self.phase, self.reset_asserted = 'startup-pending', False
            # SoundDevice increments its epoch only AFTER this callback returns.
            self.events.append(('reset_released_pending', sound.reset_epoch + 1,
                                self.generation, self.reset_clocks))

    def grant_reset_clocks(self, clocks):
        self._bound()
        if type(clocks) is not int or clocks < 0:
            raise ValueError('explicit nonnegative Z80 RESET clocks required')
        if not self.reset_asserted or self.phase != 'reset-held':
            raise AudioBoundary('RESET clocks can only be granted while actually held')
        previous = self.reset_clocks
        self.reset_clocks += clocks
        self.events.append(('reset_clock_grant', clocks, self.reset_clocks))
        if previous < 3 <= self.reset_clocks:
            self.control = AudioControlState(0, 0, 0, False, False, 0, False)
            self.events.append(('reset_control_established', self.generation))

    def _write_control(self, **values):
        self._bound()
        if self.reset_asserted:
            raise AudioBoundary('software control instruction cannot execute during RESET')
        self.control = replace(self.control, **values)

    def set_interrupt_vector(self, value):
        self._write_control(interrupt_vector=byte(value))
        self.events.append(('set_interrupt_vector', value))

    def set_refresh(self, value):
        self._write_control(refresh=byte(value))
        self.events.append(('set_refresh', value))

    def interrupt_control(self, enabled, deferred_one_instruction):
        if type(enabled) is not bool or type(deferred_one_instruction) is not bool:
            raise ValueError('explicit IFF and EI-delay booleans required')
        if not enabled and deferred_one_instruction:
            raise ValueError('DI cannot introduce an EI delay')
        self._write_control(iff1=enabled, iff2=enabled,
                            ei_deferred=deferred_one_instruction)
        self.events.append(('interrupt_control', enabled, deferred_one_instruction))

    def interrupt_mode(self, mode):
        if type(mode) is not int or mode not in (0, 1, 2):
            raise ValueError('actual interrupt mode 0/1/2 required')
        self._write_control(interrupt_mode=mode)
        self.events.append(('interrupt_mode', mode))

    def complete_ei_following_instruction(self, *, generation, reset_epoch):
        sound = self._bound()
        if generation != self.generation or reset_epoch != sound.reset_epoch:
            raise AudioBoundary('instruction-completion grant belongs to another reset')
        if self.control.ei_deferred is not True:
            raise AudioBoundary('no actual deferred EI instruction to complete')
        self._write_control(ei_deferred=False)
        self.events.append(('explicit_EI_following_instruction_completed', generation, reset_epoch))

    def acquire_frame(self, entry_kind, entry_address, *, authority):
        sound = self._bound()
        word(entry_address)
        if entry_kind not in ('startup', 'driver'):
            raise ValueError('finite startup/driver entry kind required')
        if sound.executing or sound.reset_asserted or self.reset_asserted:
            raise AudioBoundary('entry authority requires a released inactive sound owner')
        if self._frame_session is not None:
            raise AudioBoundary('an actual managed frame session already owns this entry')
        if not isinstance(authority, AudioEntryAuthority):
            raise AudioBoundary('actual startup/driver installation authority required')
        frame = authority.provide_frame(sound, entry_kind, entry_address, self.control)
        if type(frame) is not DriverFrame:
            raise AudioBoundary('entry authority did not supply the complete actual DriverFrame')
        self.control = replace(self.control, pc_entry=entry_address)
        self.phase = 'startup-authorized' if entry_kind == 'startup' else 'driver-ready'
        self._lease = AudioFrameLease(self._token, self.generation, sound.reset_epoch,
                                     entry_kind, frame)
        self.events.append(('entry_authorized', entry_kind, entry_address,
                            self.generation, sound.reset_epoch))
        return self._lease

    def require_frame(self, lease):
        sound = self._bound()
        if (type(lease) is not AudioFrameLease or lease is not self._lease
                or lease.owner_token is not self._token or lease.generation != self.generation
                or lease.reset_epoch != sound.reset_epoch or self.reset_asserted
                or sound.reset_asserted):
            raise AudioBoundary('expired or foreign managed audio frame')
        return lease.frame

    def claim_frame_session(self, lease, session):
        frame = self.require_frame(lease)
        if self._frame_session is not None or session is None:
            raise AudioBoundary('one actual managed frame session required')
        self._lease, self._frame_session = None, session
        self.events.append(('frame_session_claimed', self.generation, lease.reset_epoch))
        return frame

    def require_frame_session(self, session, generation, reset_epoch):
        sound = self._bound()
        if (self._frame_session is not session or session is None
                or type(generation) is not int or generation != self.generation
                or type(reset_epoch) is not int or reset_epoch != sound.reset_epoch
                or self.reset_asserted or sound.reset_asserted):
            raise AudioBoundary('expired or foreign managed audio frame session')
        return sound

    def finish_frame_session(self, session, generation, reset_epoch, frame):
        self.require_frame_session(session, generation, reset_epoch)
        if type(frame) is not DriverFrame:
            raise ValueError('complete actual session frame required')
        self._frame_session = None
        self._lease = AudioFrameLease(self._token, generation, reset_epoch, 'driver', frame)
        self.phase = 'driver-ready'
        self.events.append(('frame_session_finished', generation, reset_epoch))
        return self._lease

    def abandon_frame_session(self, session, *, reason):
        if self._frame_session is not session or session is None:
            return  # A reset/new owner must not be modified by an old session.
        if type(reason) is not str or not reason:
            raise ValueError('actual session boundary reason required')
        self._frame_session = self._lease = None
        self.phase = 'execution-boundary'
        self.events.append(('frame_session_boundary', reason, self.generation))

    def accept_session_im1(self, session, generation, reset_epoch):
        sound = self.require_frame_session(session, generation, reset_epoch)
        if (not sound.executing or sound.bus_requested or sound.m68k_granted
                or self.control.interrupt_mode != 1 or self.control.iff1 is not True
                or self.control.ei_deferred is not False):
            raise AudioBoundary('actual released IM1-enabled instruction boundary required')
        self.control = replace(self.control, iff1=False, iff2=False, ei_deferred=False)
        self.events.append(('IM1_accepted', generation, reset_epoch, 0x38))

    def run_stage(self, lease, stage, *, return_word):
        frame = self.require_frame(lease)
        if lease.entry_kind != 'driver' or self.phase != 'driver-ready':
            raise AudioBoundary('driver stage needs actual driver-entry authority')
        # Raw DriverFrame APIs remain available and cannot enforce this lease.
        # This managed channel is linear and invalidates its carrier on failure.
        self._lease = None
        try:
            returned = run_driver_stage(self.sound, stage, frame, return_word=return_word,
                                        reset_epoch=lease.reset_epoch)
        except BaseException:
            self.phase = 'execution-boundary'
            raise
        self._lease = AudioFrameLease(self._token, self.generation, lease.reset_epoch,
                                     'driver', returned)
        return self._lease


class FinitePulseSoundSchedule(SoundSchedule):
    """Finite explicit pulse clocks and bus grants, with no automatic success.

    reset_pulse_clocks supplies one total grant for each assert/release pulse.
    A failed release never reuses that grant. A caller may explicitly grant
    additional held clocks before retrying. No pulse or BUSACK permit is guessed.
    open_bus_reader owns all unused BUSACK bits. No chip, RAM or entry executes.
    """
    def __init__(self, owner, *, reset_pulse_clocks, bus_transfer_permits, open_bus_reader):
        if type(owner) is not AudioControlOwner:
            raise ValueError('actual AudioControlOwner required')
        if type(reset_pulse_clocks) is not tuple or any(type(n) is not int or n < 0
                                                       for n in reset_pulse_clocks):
            raise ValueError('finite explicit nonnegative RESET pulse clocks required')
        if type(bus_transfer_permits) is not tuple or any(type(v) is not bool
                                                         for v in bus_transfer_permits):
            raise ValueError('finite explicit bus-transfer permits required')
        if not callable(open_bus_reader):
            raise ValueError('actual BUSACK open-bus reader required')
        self.owner, self.reset_pulse_clocks = owner, reset_pulse_clocks
        self.bus_transfer_permits, self.open_bus_reader = bus_transfer_permits, open_bus_reader
        self._pulse_index, self._permit_index = 0, 0
        self._pulse, self._pulse_granted = None, False
        self.events = []

    def _next_pulse(self):
        if self._pulse_index == len(self.reset_pulse_clocks):
            raise AudioBoundary('explicit finite RESET pulse clock supply exhausted')
        self._pulse = self.reset_pulse_clocks[self._pulse_index]
        self._pulse_index += 1
        self._pulse_granted = False

    def reset_changed(self, device, asserted):
        self.owner._bound(device)
        if asserted:
            self._next_pulse()
            self.owner.reset_changed(device, True)
        else:
            # An explicitly initially-held reset also needs one supplied pulse.
            if self._pulse is None:
                if not self.owner.reset_asserted:
                    raise AudioBoundary('RESET release has no active pulse')
                self._next_pulse()
            if not self._pulse_granted:
                self.owner.grant_reset_clocks(self._pulse)
                self._pulse_granted = True
            self.owner.reset_changed(device, False)
            self._pulse = None
        self.events.append(('reset_transition', asserted, self._pulse_index))

    def poll_bus_request(self, device):
        self.owner._bound(device)
        if self._permit_index == len(self.bus_transfer_permits):
            raise AudioBoundary('explicit finite bus transfer supply exhausted')
        permit = self.bus_transfer_permits[self._permit_index]
        self._permit_index += 1
        self.events.append(('bus_transfer_permit', permit, self._permit_index))
        if not permit:
            raise AudioBoundary('caller explicitly withheld this bus transfer')
        device.grant_m68k()

    def read_open_bus(self, address, size):
        return self.open_bus_reader(address, size)
