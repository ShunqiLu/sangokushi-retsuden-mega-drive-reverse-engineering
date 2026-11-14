"""Exact narrative206 admission; original complete sound-copy proof is reused.

The original intro-only provider remains unchanged. No jump is recast as an
intro IRQ, no CODE/data copy is installed by the host and no RAM is reset here.
"""
import ast
import inspect
from types import CodeType, FunctionType

from . import driver_installation as base
from . import city_driver_installation as city
from . import warm_driver_installation as warm
from .domain import AudioBoundary
from .hardware_scene import SoundDevice, SharedSoundAudioBus
from .owned_runtime import OwnedAudioDeviceBus, ExplicitAudioPlatform
from .warm_driver_installation import RetainedAudioCarriers
from ..high_level_main_flows.city_cold_reset import CityColdResetSession
from ..high_level_scene_flows.narrative_reset import OriginalNarrativeResetJump, NarrativeScenePrograms


EXPECTED_WARM_SOURCES = {'_warm_init_tree': "def _warm_init_tree(original):\n    result = copy.deepcopy(original)\n    classes = [node for node in original.body if type(node) is ast.ClassDef\n        and node.name == 'DriverInstallationCapture']\n    if len(classes) != 1:\n        raise AudioBoundary('one complete original installation class required')\n    cls = classes[0]\n    init = next(node for node in cls.body if type(node) is ast.FunctionDef and node.name == '__init__')\n    if _dump(init) != _dump(ast.parse(EXPECTED_BASE_INIT).body[0]):\n        raise AudioBoundary('complete original cold installation constructor changed')\n    anchor = ast.parse('self.sound,self.control,self.scene,self.audio_state=sound,control,sound.scene,sound.audio_state').body[0]\n    positions = [index for index, node in enumerate(init.body) if _dump(node) == _dump(anchor)]\n    if len(positions) != 1:\n        raise AudioBoundary('one complete original capture metadata suffix required')\n    index = positions[0]\n    prefix = copy.deepcopy(init.body[:index])\n    replacement = ast.parse('platform,bus,devices,cold,idle,release = '\n        '_warm_capture_preconditions(self,sound,control,source,reset_session)').body[0]\n    changed = copy.deepcopy(init)\n    changed.body[:index] = [replacement]\n    inverse = copy.deepcopy(changed)\n    if _dump(inverse.body[0]) != _dump(replacement):\n        raise AudioBoundary('warm admission prefix inverse differs')\n    inverse.body[:1] = prefix\n    if _dump(inverse) != _dump(init):\n        raise AudioBoundary('entire installation constructor warm-prefix inverse differs')\n    changed_class = result.body[original.body.index(cls)]\n    method_index = cls.body.index(init)\n    changed_class.body[method_index] = changed\n    restored = copy.deepcopy(result)\n    restored.body[original.body.index(cls)].body[method_index] = inverse\n    if _dump(restored) != _dump(original):\n        raise AudioBoundary('entire installation module inverse differs')\n    return ast.fix_missing_locations(result)", '_warm_capture_preconditions': "def _warm_capture_preconditions(self, sound, control, source, reset_session):\n    retirement, jump = self.retirement, self.jump\n    if (type(retirement) is not RetainedAudioCarriers or type(jump) is not OriginalIntroResetJump\n            or type(sound) is not SoundDevice or sound.scene is None or control.sound is not sound\n            or jump.state is not sound.scene or jump.full_sr != sound.scene.sr\n            or type(reset_session) is not CityColdResetSession or reset_session.started\n            or reset_session.phase != 'not-started' or reset_session.state is not sound.scene\n            or reset_session.entry is not jump.frame\n            or type(source) is not base.CartridgeSourceData or sound.scene.data is not source.data):\n        raise AudioBoundary('exact actual JMP206/new city-reset/retained-audio/source window required')\n    retirement.require_retired(sound, control)\n    reset_session._guard()\n    platform, bus = sound.audio_state.platform, sound.audio_state.bus\n    if (type(platform) is not ExplicitAudioPlatform or platform.control_owner is not control\n            or type(bus) is not SharedSoundAudioBus or bus.device is not sound or bus.ram is not sound.ram):\n        raise AudioBoundary('warm entry must retain the same exact explicit platform/shared sound RAM')\n    devices = bus.devices\n    if (type(devices) is not OwnedAudioDeviceBus or not devices.material.data.segments\n            or not callable(devices.psg_write) or not callable(devices.on_transfer)):\n        raise AudioBoundary('same actual FM/PSG/nonempty owned bank material required')\n    if (len(source.data.segments) != 1 or source.data.segments[0][0] != 0\n            or len(source.data.segments[0][1]) != 0x100000\n            or source.evidence.get('format') != 'g5510-explicit-complete-cartridge-source-DATA-v1'):\n        raise AudioBoundary('complete explicit own-source partition required')\n    # Preserve the original metadata suffix without making dummy cold objects:\n    # these historical field names now retain the real retired owner, carrier\n    # witness and actual nonreturning transfer; none is an execution authority.\n    return platform, bus, devices, retirement.owner, retirement, jump"}


def _dump(node):
    return ast.dump(node, include_attributes=False)


def _code_shape(code):
    return tuple(getattr(code, name) for name in (
        'co_code', 'co_names', 'co_varnames', 'co_argcount', 'co_posonlyargcount',
        'co_kwonlyargcount', 'co_flags', 'co_freevars', 'co_cellvars')) + (tuple(
            _code_shape(value) if type(value) is CodeType else value for value in code.co_consts),)


def _warm_source_bindings():
    tree = ast.parse(inspect.getsource(warm), filename=warm.__file__)
    plain = compile(tree, warm.__file__, 'exec', dont_inherit=True)
    bindings = []
    for name, source in EXPECTED_WARM_SOURCES.items():
        nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
        actual = getattr(warm, name)
        if (len(nodes) != 1 or _dump(nodes[0]) != _dump(ast.parse(source).body[0])
                or type(actual) is not FunctionType or actual.__globals__ is not vars(warm)
                or actual.__module__ != warm.__name__ or actual.__name__ != name
                or actual.__closure__ is not None or actual.__code__.co_freevars
                or _code_shape(actual.__code__) != _code_shape(city._named_code(plain, name))):
            raise AudioBoundary('actual complete warm source utility required: ' + name)
        bindings.append((name, actual, actual.__code__))
    return tuple(bindings)


def _narrative_capture_preconditions(self, sound, control, source, reset_session):
    retirement, jump = (self.retirement, self.jump)
    if type(retirement) is not RetainedAudioCarriers or type(jump) is not OriginalNarrativeResetJump or type(sound) is not SoundDevice or (sound.scene is None) or (control.sound is not sound) or (jump.state is not sound.scene) or (jump.full_sr != sound.scene.sr) or (type(reset_session) is not CityColdResetSession) or reset_session.started or (reset_session.phase != 'not-started') or (reset_session.state is not sound.scene) or (reset_session.entry is not jump.frame) or (type(source) is not base.CartridgeSourceData) or (sound.scene.data is not source.data):
        raise AudioBoundary('exact actual JMP206/new city-reset/retained-audio/source window required')
    if type(jump.owner) is not NarrativeScenePrograms or jump.owner.require_claimed(jump) is not jump.frame:
        raise AudioBoundary('one exact claimed narrative terminal jump proof required')
    retirement.require_retired(sound, control)
    reset_session._guard()
    platform, bus = (sound.audio_state.platform, sound.audio_state.bus)
    if type(platform) is not ExplicitAudioPlatform or platform.control_owner is not control or type(bus) is not SharedSoundAudioBus or (bus.device is not sound) or (bus.ram is not sound.ram):
        raise AudioBoundary('warm entry must retain the same exact explicit platform/shared sound RAM')
    devices = bus.devices
    if type(devices) is not OwnedAudioDeviceBus or not devices.material.data.segments or (not callable(devices.psg_write)) or (not callable(devices.on_transfer)):
        raise AudioBoundary('same actual FM/PSG/nonempty owned bank material required')
    if len(source.data.segments) != 1 or source.data.segments[0][0] != 0 or len(source.data.segments[0][1]) != 1048576 or (source.evidence.get('format') != 'g5510-explicit-complete-cartridge-source-DATA-v1'):
        raise AudioBoundary('complete explicit own-source partition required')
    return (platform, bus, devices, retirement.owner, retirement, jump)


class NarrativeWarmDriverInstallationCapture:
    """Exact narrative admission, original four complete city methods reused."""

    def __init__(self, sound, control, source, *, reset_session, retirement, jump):
        self.retirement, self.jump = retirement, jump
        self._warm_bindings = _warm_source_bindings()
        self._methods, self._source_bindings = city._make_method_views()
        tree = ast.parse(inspect.getsource(base), filename=base.__file__)
        code = compile(warm._warm_init_tree(tree), base.__file__, 'exec', dont_inherit=True)
        cls_code = city._named_code(code, 'DriverInstallationCapture')
        original = base.DriverInstallationCapture.__init__
        namespace = dict(vars(base), _warm_capture_preconditions=_narrative_capture_preconditions)
        init = FunctionType(city._named_code(cls_code, '__init__'), namespace,
            '__init__', original.__defaults__, None)
        init.__kwdefaults__ = original.__kwdefaults__
        self._methods['__init__'] = init
        self._require_bindings()
        init(self, sound, control, source, reset_session=reset_session)

    def _require_bindings(self):
        if type(self) is not NarrativeWarmDriverInstallationCapture:
            raise AudioBoundary('one exact narrative installation provider required')
        for name, function, code in self._warm_bindings:
            if getattr(warm, name) is not function or function.__code__ is not code:
                raise AudioBoundary('actual warm source utility was rebound: ' + name)
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
        witness.evidence.update(entry_origin='actual_narrative_JMP206_warm300',
            narrative_source_pc=self.jump.source_pc,
            retained_general_carriers=True, cold_workspace_replayed=False,
            platform_or_chip_replaced=False)
        return witness

    def require_witness(self, witness, sound, control):
        self._require_bindings()
        return self._methods['require_witness'](self, witness, sound, control)
