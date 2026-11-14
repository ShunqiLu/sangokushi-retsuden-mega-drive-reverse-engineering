"""One live sound RAM, explicit bus arbitration, and recovered audio entry calls.

This is a bounded high-level device, not a Z80 interpreter or a chip emulator.
No ACK, reset completion, open-bus data, timer or audio execution is invented.
All non-RAM sound accesses retain the supplied AudioBus owner.
"""
from ..high_level_audio_engine.domain import AudioBoundary, AudioState, byte, word
from ..high_level_scene_flows.domain import Boundary, HardwareBus, SceneState, uint


class SoundSchedule:
    """Host-supplied ordering authority; the unbound implementation stops."""

    def poll_bus_request(self, device):
        raise Boundary('pending Z80 bus transfer requires explicit synchronization')

    def read_open_bus(self, address, size):
        raise Boundary('BUSACK unused bits require actual open-bus input')

    def reset_changed(self, device, asserted):
        raise Boundary('sound reset requires actual platform/chip owner')


class SharedSoundAudioBus:
    """AudioState's real RAM bus; 8 KiB is mirrored in Z80 0000..3FFF.

    The supplied external AudioBus owns banked material, YM2612, PSG, timing,
    transfer boundaries and every address not backed by sound RAM here.
    """

    def __init__(self, ram, devices):
        if type(ram) is not bytearray or len(ram) != 8192:
            raise ValueError('one explicit live 8 KiB sound RAM required')
        if any(not callable(getattr(devices, name, None)) for name in
               ('read_byte', 'write_byte', 'progress', 'transfer_boundary')):
            raise ValueError('explicit external AudioBus owner required')
        self.ram, self.devices, self.device = ram, devices, None

    def _owner(self):
        if self.device is None:
            raise AudioBoundary('shared sound bus was not attached')
        self.device.require_audio_owner()

    def read_byte(self, address):
        word(address)
        self._owner()
        return self.ram[address & 0x1FFF] if address < 0x4000 else byte(self.devices.read_byte(address))

    def write_byte(self, address, value):
        word(address); byte(value)
        self._owner()
        if address < 0x4000:
            self.ram[address & 0x1FFF] = value
        else:
            self.devices.write_byte(address, value)

    def progress(self, reason):
        self._owner()
        return self.devices.progress(reason)

    def transfer_boundary(self, reason):
        self._owner()
        return self.devices.transfer_boundary(reason)


class SoundDevice:
    """Own explicit line state, same AudioState, and finite semantic invocations.

    A request does not itself grant ownership. A scheduler first synchronizes
    its real sound work, then explicitly calls grant_m68k(). No cycle counts,
    CPU registers or successful reset/IRQ continuations are synthesized.
    """

    def __init__(self, audio_state, schedule, *, reset_asserted, bus_requested,
                 m68k_granted):
        if type(audio_state) is not AudioState or type(audio_state.bus) is not SharedSoundAudioBus:
            raise ValueError('exact AudioState with shared sound RAM bus required')
        if not isinstance(schedule, SoundSchedule):
            raise ValueError('explicit sound scheduling authority required')
        if any(type(value) is not bool for value in
               (reset_asserted, bus_requested, m68k_granted)):
            raise ValueError('explicit initial sound control line states required')
        if m68k_granted and (reset_asserted or not bus_requested):
            raise ValueError('grant requires released reset and asserted request')
        if audio_state.bus.device is not None:
            raise ValueError('shared AudioState already has a sound owner')
        self.audio_state, self.schedule = audio_state, schedule
        self.ram = audio_state.bus.ram
        self.reset_asserted, self.bus_requested = reset_asserted, bus_requested
        self.m68k_granted, self.executing = m68k_granted, False
        self.reset_epoch, self.scene = 0, None
        audio_state.bus.device = self

    def request_bus(self, requested):
        if type(requested) is not bool:
            raise ValueError('explicit BUSREQ level required')
        self.bus_requested = requested
        if not requested:
            self.m68k_granted = False

    def set_reset(self, asserted):
        if type(asserted) is not bool:
            raise ValueError('explicit RESET level required')
        if asserted == self.reset_asserted:
            return
        if self.executing:
            raise Boundary('reset during an active audio semantic call requires its continuation')
        # The supplied owner must perform its real CPU/chip reset effects. If
        # unbound/failed, this transition is not recorded as completed here.
        self.schedule.reset_changed(self, asserted)
        self.reset_asserted = asserted
        if asserted:
            self.m68k_granted = False
        else:
            self.reset_epoch += 1

    def grant_m68k(self):
        if not self.bus_requested or self.reset_asserted:
            raise Boundary('cannot grant Z80 RAM without request and released reset')
        if self.executing:
            raise Boundary('cannot grant Z80 RAM during an active audio semantic call')
        self.m68k_granted = True

    def require_m68k_owner(self):
        if not self.m68k_granted or not self.bus_requested or self.reset_asserted:
            raise Boundary('68000 does not own shared Z80 RAM')

    def require_audio_owner(self):
        if self.reset_asserted or self.m68k_granted or not self.executing:
            raise AudioBoundary('audio DATA requires an active supplied execution grant')

    def bus_ack(self, address, size):
        if self.bus_requested and not self.reset_asserted and not self.m68k_granted:
            self.schedule.poll_bus_request(self)
        # All other bits are actual supplied bus data, not invented zeros.
        observed = uint(self.schedule.read_open_bus(address, size), size * 8)
        bit = 1 if size == 1 else 0x100
        granted = self.bus_requested and self.m68k_granted and not self.reset_asserted
        return observed & ~bit if granted else observed | bit

    def execute_audio(self, entry, inputs, *, reset_epoch):
        """Invoke one recovered function on its actual typed inputs and stack.

        This finite entry list is not opcode dispatch. Long-lived driver/startup
        functions can still stop on genuine external continuations/budgets.
        Caller must supply fresh inputs after reset; an old context is rejected.
        """
        if type(reset_epoch) is not int or reset_epoch != self.reset_epoch:
            raise AudioBoundary('audio inputs belong to a different reset epoch')
        if self.reset_asserted or self.m68k_granted or self.executing or self.bus_requested:
            raise AudioBoundary('sound execution requires released bus/reset and no active call')
        from .business_boot import initialize_audio_workspace
        from .business_hardware import initialize_audio_driver, wait_fm_ready
        from .business_mailbox import poll_command_mailboxes, arbitrate_command_slot
        entries = {'initialize_audio_workspace': initialize_audio_workspace,
                   'initialize_audio_driver': initialize_audio_driver,
                   'wait_fm_ready': wait_fm_ready,
                   'poll_command_mailboxes': poll_command_mailboxes,
                   'arbitrate_command_slot': arbitrate_command_slot}
        if type(entry) is not str or entry not in entries:
            raise AudioBoundary('unbound high-level sound execution entry')
        self.executing = True
        try:
            return entries[entry](self.audio_state, inputs)
        finally:
            self.executing = False


def _default_sound_mapping(devices):
    """Only strip generic default ranges through exact known delegators."""
    from ..high_level_video.hardware_vdp import SceneVdpHardwareBus
    from ..high_level_input.hardware_controller import SceneControllerHardwareBus
    from ..high_level_storage.hardware_scene import SceneSaveHardwareBus
    wrappers = (SceneVdpHardwareBus, SceneControllerHardwareBus, SceneSaveHardwareBus)
    while type(devices) in wrappers:
        devices = devices.devices
    return type(devices) is HardwareBus


class SceneSoundHardwareBus(HardwareBus):
    """Canonical 68000 sound RAM and the BUSREQ/RESET register word lanes.

    Byte addresses A00000..A01FFF map the same live RAM used by AudioState.
    68000 WORD reads duplicate ONE sound byte; WORD writes use the high byte.
    LONGs issue two ordered WORDs. Other sound apertures are delegated.
    """

    WINDOWS = ((0xA00000, 0xA02000), (0xA11100, 0xA11102), (0xA11200, 0xA11202))

    def __init__(self, sound, devices, *, replace_sound_mapping=False):
        if type(sound) is not SoundDevice or not isinstance(devices, HardwareBus):
            raise ValueError('one real SoundDevice and existing Scene bus required')
        if type(replace_sound_mapping) is not bool:
            raise ValueError('explicit sound mapping authority required')
        overlaps = any(start < b and a < end for start, end in devices.ranges
                       for a, b in self.WINDOWS)
        if overlaps and (not replace_sound_mapping or not _default_sound_mapping(devices)):
            raise ValueError('sound mapping would replace a supplied device owner')
        ranges = list(devices.ranges)
        for a, b in self.WINDOWS:
            reduced = []
            for start, end in ranges:
                if end <= a or start >= b:
                    reduced.append((start, end))
                else:
                    if start < a:
                        reduced.append((start, a))
                    if b < end:
                        reduced.append((b, end))
            ranges = reduced
        super().__init__(tuple(ranges) + self.WINDOWS)
        self.sound, self.devices = sound, devices

    def bind_scene(self, state):
        if type(state) is not SceneState:
            raise ValueError('exact live SceneState required')
        current = state.hardware
        seen = set()
        while current is not self:
            if id(current) in seen or not isinstance(getattr(current, 'devices', None), HardwareBus):
                raise ValueError('sound device is not in the actual Scene chain')
            seen.add(id(current)); current = current.devices
        if self.sound.scene is not None and self.sound.scene is not state:
            raise ValueError('sound RAM already belongs to another Scene')
        self.sound.scene = state
        return self

    def _access(self, address, size):
        uint(address, 32)
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('actual BYTE/WORD/LONG hardware width required')
        if size > 1 and address & 1:
            raise Boundary('odd sound hardware WORD/LONG access')
        return address & 0xFFFFFF

    def read(self, address, size):
        physical = self._access(address, size)
        if 0xA00000 <= physical and physical + size <= 0xA02000:
            self.sound.require_m68k_owner()
            if size == 4:
                return self.read(address, 2) << 16 | self.read(address + 2, 2)
            value = self.sound.ram[physical & 0x1FFF]
            return value if size == 1 else value * 0x101
        if physical == 0xA11100 and size in (1, 2):
            return self.sound.bus_ack(address, size)
        # Odd BUSACK lane, RESET reads and crossing LONGs are true open bus /
        # undeclared registers. Preserve their supplied owner, never echo latches.
        return self.devices.read(address, size)

    def write(self, address, size, value):
        physical = self._access(address, size)
        uint(value, size * 8)
        if 0xA00000 <= physical and physical + size <= 0xA02000:
            self.sound.require_m68k_owner()
            if size == 4:
                self.write(address, 2, value >> 16)
                self.write(address + 2, 2, value & 0xFFFF)
            else:
                self.sound.ram[physical & 0x1FFF] = value if size == 1 else value >> 8
            return
        if physical in (0xA11100, 0xA11200) and size in (1, 2):
            asserted_bit = bool(value & (1 if size == 1 else 0x100))
            if physical == 0xA11100:
                self.sound.request_bus(asserted_bit)
            else:
                self.sound.set_reset(not asserted_bit)
            return
        if physical in (0xA11101, 0xA11201) and size == 1:
            return  # Lower-byte lane is not connected to these control lines.
        return self.devices.write(address, size, value)

    def progress(self, state, reason):
        if self.sound.scene is not None and self.sound.scene is not state:
            raise Boundary('asynchronous sound progress belongs to another Scene')
        return self.devices.progress(state, reason)
