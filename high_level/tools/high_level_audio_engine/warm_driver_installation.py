"""Warm original206/300 copy evidence, preserving the exact old entry authority.

The old cold-only provider is unchanged. The original complete copy checker,
identity checker and single-use witness validator remain the sole algorithms.
"""
import ast
import copy
import inspect
import threading
from dataclasses import dataclass
from types import FunctionType

from . import driver_installation as base
from . import city_driver_installation as city
from .domain import AudioBoundary
from .owned_runtime import DriverFrame
from .hardware_scene import SoundDevice, SharedSoundAudioBus
from .owned_runtime import OwnedAudioDeviceBus, ExplicitAudioPlatform
from ..high_level_main_flows.city_cold_reset import CityColdResetSession
from ..high_level_main_flows.intro_irq_program import OriginalIntroResetJump


EXPECTED_BASE_INIT = "def __init__(self, sound, control, source, *, reset_session):\n    if type(sound) is not SoundDevice or sound.scene is None or control.sound is not sound or (type(source) is not CartridgeSourceData) or (sound.scene.data is not source.data) or (type(reset_session) is not PersistentColdResetSession) or (reset_session.state is not sound.scene):\n        raise ValueError('same actual cold Scene/sound/reset and complete typed own-source authority required')\n    reset_session._guard()\n    release = reset_session.waiting\n    platform = sound.audio_state.platform\n    if reset_session.phase != 'actual-audio-release' or type(release) is not ResetAudioReleasePoint or release.session is not reset_session or (release.pc != 610) or (type(platform) is not ColdWorkspacePlatform) or (platform.control_owner is not control):\n        raise AudioBoundary('actual cold-release/cold-platform continuation required before resume')\n    cold = platform.workspace_session\n    if type(cold) is not ColdWorkspaceSession or cold.sound is not sound:\n        raise AudioBoundary('actual same-State completed cold idle owner required')\n    idle = cold.observe_idle()\n    if idle.session is not cold or control._frame_session is not cold:\n        raise AudioBoundary('actual live cold idle claim must precede real288 invalidation')\n    bus = sound.audio_state.bus\n    if type(bus) is not SharedSoundAudioBus or bus.device is not sound or bus.ram is not sound.ram:\n        raise AudioBoundary('one actual shared8192-byte sound RAM bus required')\n    devices = bus.devices\n    if type(devices) is not OwnedAudioDeviceBus or not devices.material.data.segments or (not callable(devices.psg_write)) or (not callable(devices.on_transfer)):\n        raise AudioBoundary('same explicit nonempty owned bank DATA and device owners required')\n    if sound.executing or sound.reset_asserted or sound.bus_requested or sound.m68k_granted:\n        raise AudioBoundary('inactive released actual cold idle required')\n    if len(source.data.segments) != 1 or source.data.segments[0][0] != 0 or len(source.data.segments[0][1]) != 1048576 or (source.evidence.get('format') != 'g5510-explicit-complete-cartridge-source-DATA-v1'):\n        raise AudioBoundary('complete explicit own-source partition required, not opaque ROM fallback')\n    self.sound, self.control, self.scene, self.audio_state = (sound, control, sound.scene, sound.audio_state)\n    self.source, self.source_data, self.source_segments = (source, source.data, source.data.segments)\n    self.reset_session, self.release, self.cold, self.idle = (reset_session, release, cold, idle)\n    self.shared_bus, self.ram, self.devices = (bus, sound.ram, devices)\n    self.platform, self.schedule = (platform, sound.schedule)\n    self.fm, self.material, self.bank_data = (devices.fm, devices.material, devices.material.data)\n    self.bank_segments, self.bank_base = (self.bank_data.segments, devices.bank_base)\n    self.psg_write, self.transfer = (devices.psg_write, devices.on_transfer)\n    self.scene_events, self.control_events = (self.scene.events, control.events)\n    self.scene_start, self.control_start = (len(self.scene_events), len(self.control_events))\n    self.epoch, self.generation = (sound.reset_epoch, control.generation)\n    self.operations, self.pre_ram = (self.audio_state.data_operations, bytes(self.ram))\n    self.thread = threading.get_ident()\n    self.copy_function = business_lowbank.initialize_z80_sound_image_fields\n    self.reset_function = business_lowbank.release_z80_reset_fields\n    self.main_function = bootstrap_steps.bootstrap_main_program\n    self.copy_code, self.reset_code, self.main_code = (self.copy_function.__code__, self.reset_function.__code__, self.main_function.__code__)\n    self.witness = None\n    self.after_ram = self.after_control = None\n    self.sealed_waiting = None\n    self.finished = False"
DriverInstalledAuthority = base.DriverInstalledAuthority


@dataclass(frozen=True)
class RetainedAudioCarriers:
    """Actual last owned driver carriers; RESET does not initialize them."""
    owner: object
    point: object
    frame: DriverFrame
    irq_clock: int
    irq_clock_hz: int
    generation: int
    reset_epoch: int
    data_operations: int
    thread: int

    @classmethod
    def retire(cls, owner):
        from ..reconstructed_game.audio import OwnedGameAudio
        if type(owner) is not OwnedGameAudio:
            raise ValueError('one exact actually running application audio owner required')
        owner._require_owned()
        point = owner.waiting
        if type(point.frame) is not DriverFrame:
            raise AudioBoundary('the actual managed driver must retain all eight carriers')
        result = cls(owner, point, point.frame, owner._loop.irq_clock,
            owner._loop.irq_clock_hz, owner.generation, owner.reset_epoch,
            owner.audio.data_operations, threading.get_ident())
        before = owner._read_chip_counters()
        owner.close()
        if owner._read_chip_counters() != before:
            raise AudioBoundary('retiring software ownership must not advance or replace chips')
        result.require_retired(owner.sound, owner.control)
        return result

    def require_retired(self, sound, control):
        owner = self.owner
        if (threading.get_ident() != self.thread or not owner.closed or owner.failed
                or owner.sound is not sound or owner.control is not control
                or owner.waiting is not self.point or self.point.frame is not self.frame
                or owner._loop.irq_clock != self.irq_clock or owner._loop.irq_clock_hz != self.irq_clock_hz
                or owner.generation != self.generation or owner.reset_epoch != self.reset_epoch
                or owner.audio.data_operations != self.data_operations
                or sound.reset_epoch != self.reset_epoch or control.generation != self.generation
                or control._frame_session is not None or control._lease is not None
                or getattr(owner.audio, 'mailbox_wz_service', None) is not None
                or sound.executing or sound.reset_asserted or sound.bus_requested or sound.m68k_granted):
            raise AudioBoundary('actual closed loop/WZ and unchanged retained general carriers required')
        return self.frame


def _dump(node):
    return ast.dump(node, include_attributes=False)


def _warm_init_tree(original):
    result = copy.deepcopy(original)
    classes = [node for node in original.body if type(node) is ast.ClassDef
        and node.name == 'DriverInstallationCapture']
    if len(classes) != 1:
        raise AudioBoundary('one complete original installation class required')
    cls = classes[0]
    init = next(node for node in cls.body if type(node) is ast.FunctionDef and node.name == '__init__')
    if _dump(init) != _dump(ast.parse(EXPECTED_BASE_INIT).body[0]):
        raise AudioBoundary('complete original cold installation constructor changed')
    anchor = ast.parse('self.sound,self.control,self.scene,self.audio_state=sound,control,sound.scene,sound.audio_state').body[0]
    positions = [index for index, node in enumerate(init.body) if _dump(node) == _dump(anchor)]
    if len(positions) != 1:
        raise AudioBoundary('one complete original capture metadata suffix required')
    index = positions[0]
    prefix = copy.deepcopy(init.body[:index])
    replacement = ast.parse('platform,bus,devices,cold,idle,release = '
        '_warm_capture_preconditions(self,sound,control,source,reset_session)').body[0]
    changed = copy.deepcopy(init)
    changed.body[:index] = [replacement]
    inverse = copy.deepcopy(changed)
    if _dump(inverse.body[0]) != _dump(replacement):
        raise AudioBoundary('warm admission prefix inverse differs')
    inverse.body[:1] = prefix
    if _dump(inverse) != _dump(init):
        raise AudioBoundary('entire installation constructor warm-prefix inverse differs')
    changed_class = result.body[original.body.index(cls)]
    method_index = cls.body.index(init)
    changed_class.body[method_index] = changed
    restored = copy.deepcopy(result)
    restored.body[original.body.index(cls)].body[method_index] = inverse
    if _dump(restored) != _dump(original):
        raise AudioBoundary('entire installation module inverse differs')
    return ast.fix_missing_locations(result)


def _warm_capture_preconditions(self, sound, control, source, reset_session):
    retirement, jump = self.retirement, self.jump
    if (type(retirement) is not RetainedAudioCarriers or type(jump) is not OriginalIntroResetJump
            or type(sound) is not SoundDevice or sound.scene is None or control.sound is not sound
            or jump.state is not sound.scene or jump.full_sr != sound.scene.sr
            or type(reset_session) is not CityColdResetSession or reset_session.started
            or reset_session.phase != 'not-started' or reset_session.state is not sound.scene
            or reset_session.entry is not jump.frame
            or type(source) is not base.CartridgeSourceData or sound.scene.data is not source.data):
        raise AudioBoundary('exact actual JMP206/new city-reset/retained-audio/source window required')
    retirement.require_retired(sound, control)
    reset_session._guard()
    platform, bus = sound.audio_state.platform, sound.audio_state.bus
    if (type(platform) is not ExplicitAudioPlatform or platform.control_owner is not control
            or type(bus) is not SharedSoundAudioBus or bus.device is not sound or bus.ram is not sound.ram):
        raise AudioBoundary('warm entry must retain the same exact explicit platform/shared sound RAM')
    devices = bus.devices
    if (type(devices) is not OwnedAudioDeviceBus or not devices.material.data.segments
            or not callable(devices.psg_write) or not callable(devices.on_transfer)):
        raise AudioBoundary('same actual FM/PSG/nonempty owned bank material required')
    if (len(source.data.segments) != 1 or source.data.segments[0][0] != 0
            or len(source.data.segments[0][1]) != 0x100000
            or source.evidence.get('format') != 'g5510-explicit-complete-cartridge-source-DATA-v1'):
        raise AudioBoundary('complete explicit own-source partition required')
    # Preserve the original metadata suffix without making dummy cold objects:
    # these historical field names now retain the real retired owner, carrier
    # witness and actual nonreturning transfer; none is an execution authority.
    return platform, bus, devices, retirement.owner, retirement, jump


class WarmDriverInstallationCapture:
    """New warm admission, original three-copy/reset/bus/RAM proof unchanged."""
    def __init__(self, sound, control, source, *, reset_session, retirement, jump):
        self.retirement, self.jump = retirement, jump
        self._methods, self._source_bindings = city._make_method_views()
        tree = ast.parse(inspect.getsource(base), filename=base.__file__)
        code = compile(_warm_init_tree(tree), base.__file__, 'exec', dont_inherit=True)
        cls_code = city._named_code(code, 'DriverInstallationCapture')
        original = base.DriverInstallationCapture.__init__
        namespace = dict(vars(base), _warm_capture_preconditions=_warm_capture_preconditions)
        init = FunctionType(city._named_code(cls_code, '__init__'), namespace,
            '__init__', original.__defaults__, None)
        init.__kwdefaults__ = original.__kwdefaults__
        self._methods['__init__'] = init
        self._require_bindings()
        init(self, sound, control, source, reset_session=reset_session)

    def _require_bindings(self):
        if type(self) is not WarmDriverInstallationCapture:
            raise AudioBoundary('one exact warm installation provider required')
        for owner, name, function, code, module in self._source_bindings:
            if getattr(owner, name) is not function or (code is not None
                    and (function.__code__ is not code or function.__globals__ is not vars(module))):
                raise AudioBoundary('actual installation dependency was rebound: ' + name)

    def _identities(self):
        self._require_bindings()
        return self._methods['_identities'](self)

    def finish(self, waiting):
        self._require_bindings()
        witness = self._methods['finish'](self, waiting)
        witness.evidence.update(entry_origin='actual4786_JMP206_warm300',
            retained_general_carriers=True, cold_workspace_replayed=False,
            platform_or_chip_replaced=False)
        return witness

    def require_witness(self, witness, sound, control):
        self._require_bindings()
        return self._methods['require_witness'](self, witness, sound, control)
