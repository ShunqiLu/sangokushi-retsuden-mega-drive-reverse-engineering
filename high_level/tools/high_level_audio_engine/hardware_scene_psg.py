"""Outermost Scene adapter for confirmed odd BYTE PSG write addresses.

The existing Scene records each CPU access once, after ordinary device effects.
This bridge neither queues writes nor advances PSG clocks. WORD/LONG lane and
read-back behavior remain explicit boundaries, not guessed hardware results.
"""
from tools.high_level_audio_engine.psg_device import SegaPsgDevice
from tools.high_level_scene_flows.domain import Boundary, HardwareBus, SceneState, uint


def _unbound_psg_owner(devices):
    """Only traverse exact known PSG delegators to a bare unbound bus."""
    from tools.high_level_audio_engine.hardware_scene import SceneSoundHardwareBus
    from tools.high_level_input.hardware_controller import SceneControllerHardwareBus
    from tools.high_level_storage.hardware_scene import SceneSaveHardwareBus
    from tools.high_level_video.hardware_vdp import SceneVdpHardwareBus
    from tools.high_level_video.write_dma_events import SceneWriteDmaEvents
    wrappers = (SceneSoundHardwareBus, SceneControllerHardwareBus,
                SceneSaveHardwareBus, SceneVdpHardwareBus, SceneWriteDmaEvents)
    seen = set()
    while type(devices) in wrappers:
        if id(devices) in seen:
            return False
        seen.add(id(devices))
        if any(getattr(getattr(devices, method), '__func__', None)
               is not getattr(type(devices), method)
               for method in ('read', 'write', 'after_write')):
            return False
        devices = devices.devices
    return (type(devices) is HardwareBus
        and all(getattr(getattr(devices, method), '__func__', None) is getattr(HardwareBus, method)
                for method in ('read', 'write', 'after_write')))


class ScenePsgHardwareBus(HardwareBus):
    """One actual Sega PSG over an intact pre-existing Scene device chain.

    Construct Sound/VDP/Input/Save first, then this outermost adapter. Their
    existing default-map guards need not recognize a new wrapper. Only an
    explicitly authorized generic/unbound PSG range may be removed here.
    Pass the SAME psg.write to OwnedAudioDeviceBus for its Z80 7F11 path.
    """
    PSG_WINDOW = (0xC00010, 0xC00018)
    BYTE_PORTS = (0xC00011, 0xC00013, 0xC00015, 0xC00017)

    def __init__(self, psg, devices, *, replace_psg_mapping=False):
        if type(psg) is not SegaPsgDevice or not isinstance(devices, HardwareBus):
            raise ValueError('same actual SegaPsgDevice and explicit existing hardware required')
        if type(replace_psg_mapping) is not bool:
            raise ValueError('explicit PSG mapping replacement decision required')
        first, limit = self.PSG_WINDOW
        overlap = any(start < limit and first < end for start, end in devices.ranges)
        if overlap and (not replace_psg_mapping or not _unbound_psg_owner(devices)):
            raise ValueError('PSG mapping would replace an actual or unknown device owner')
        remaining = []
        for start, end in devices.ranges:
            if end <= first or limit <= start:
                remaining.append((start, end))
            else:
                if start < first:
                    remaining.append((start, first))
                if limit < end:
                    remaining.append((limit, end))
        super().__init__(tuple(remaining) + (self.PSG_WINDOW,))
        self.psg, self.devices, self.scene = psg, devices, None
        self.observations = []

    def bind_scene(self, state):
        if type(state) is not SceneState or state.hardware is not self:
            raise ValueError('PSG must be the outermost hardware of this actual Scene')
        if self.scene is not None and self.scene is not state:
            raise ValueError('PSG bridge already belongs to another Scene')
        self.scene = state
        return self

    def _scene(self, state=None):
        if self.scene is None or self.scene.hardware is not self or (state is not None and state is not self.scene):
            raise Boundary('PSG bridge requires its same bound outermost Scene')

    @staticmethod
    def _physical(address, size):
        uint(address, 32)
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('actual BYTE/WORD/LONG hardware width required')
        return address & 0xFFFFFF

    def _touches_psg(self, physical, size):
        return physical < self.PSG_WINDOW[1] and self.PSG_WINDOW[0] < physical + size

    def read(self, address, size):
        physical = self._physical(address, size)
        if self._touches_psg(physical, size):
            self._scene()
            raise Boundary('PSG is write-only; read/open-bus authority is not supplied')
        return self.devices.read(address, size)

    def write(self, address, size, value):
        physical = self._physical(address, size)
        uint(value, size * 8)
        if not self._touches_psg(physical, size):
            return self.devices.write(address, size, value)
        self._scene()
        if size != 1 or physical not in self.BYTE_PORTS:
            raise Boundary('PSG even-BYTE/WORD/LONG lane semantics are not supplied')
        return self.psg.write(value)

    def after_write(self, state, address, size, value):
        self._scene(state)
        physical = self._physical(address, size)
        if physical in self.BYTE_PORTS and size == 1:
            expected = ('write', address, size, value)
            if not state.events or state.events[-1] != expected:
                raise Boundary('PSG observation requires the actual once-recorded Scene write')
            self.observations.append((len(state.events) - 1, len(self.psg.events) - 1,
                                      address, value, self.psg.tick))
        return self.devices.after_write(state, address, size, value)

    def progress(self, state, reason):
        self._scene(state)
        return self.devices.progress(state, reason)
