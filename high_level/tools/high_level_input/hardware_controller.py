"""Live three-button pad wiring and the game's parallel I/O registers.

Caller-owned registers and explicit button snapshots drive real TH-selected
pin values. This layer never supplies Z80 bus acknowledgement, serial timing,
interrupt completion, cartridge data, or a missing controller's successful
response. It independently implements the documented pin/register protocol;
no external emulator code or state is imported.
"""
from dataclasses import dataclass

from ..high_level_scene_flows.domain import Boundary, HardwareBus, uint


IO_START = 0xA10000
IO_END = 0xA10020


@dataclass(frozen=True)
class PadButtons:
    """One supplied host input snapshot; True means physically pressed."""
    up: bool = False
    down: bool = False
    left: bool = False
    right: bool = False
    a: bool = False
    b: bool = False
    c: bool = False
    start: bool = False

    def __post_init__(self):
        if any(type(getattr(self, name)) is not bool for name in self.__dataclass_fields__):
            raise ValueError('explicit boolean button levels required')


class ThreeButtonPad:
    """The two combinational button banks of an explicitly connected pad."""

    def __init__(self, buttons: PadButtons):
        self.set_buttons(buttons)

    def set_buttons(self, buttons: PadButtons):
        if type(buttons) is not PadButtons:
            raise ValueError('actual three-button input snapshot required')
        self.buttons = buttons

    def input_pins(self, th_high: bool) -> int:
        if type(th_high) is not bool:
            raise ValueError('explicit TH pin level required')
        bank = (self.buttons.up, self.buttons.down, self.buttons.left,
                self.buttons.right, self.buttons.b, self.buttons.c) if th_high else (
                self.buttons.up, self.buttons.down, True, True,
                self.buttons.a, self.buttons.start)
        pins = 0x40 if th_high else 0
        for bit, pressed in enumerate(bank):
            if not pressed:
                pins |= 1 << bit
        return pins


class DisconnectedPort:
    """Explicitly disconnected parallel port with its input pull-ups."""

    def input_pins(self, th_high: bool) -> int:
        if type(th_high) is not bool:
            raise ValueError('explicit TH pin level required')
        return 0x7F


def _default_gpio_owner(devices: HardwareBus) -> bool:
    """Allow only a known default owner, never overwrite a supplied GPIO bus."""
    if type(devices) is HardwareBus:
        return True
    # The supported composition is VDP(default) -> Input -> Save. This exact
    # wrapper owns only VDP ports and delegates GPIO to the bare default bus.
    from ..high_level_video.hardware_vdp import SceneVdpHardwareBus
    return type(devices) is SceneVdpHardwareBus and type(devices.devices) is HardwareBus


class SceneControllerHardwareBus(HardwareBus):
    """Parallel controller I/O over one existing device chain.

    Only data/direction/version registers are implemented here. Serial and
    unrelated addresses retain their existing device owner. Registers are the
    caller's live 16-byte backing; no reset image or region byte is guessed.
    """

    def __init__(self, registers: bytearray, ports: tuple, devices: HardwareBus,
                 *, replace_controller_mapping: bool = False):
        if type(registers) is not bytearray or len(registers) != 16:
            raise ValueError('caller-owned 16-byte I/O register backing required')
        if type(ports) is not tuple or len(ports) != 3 or any(
                type(port) not in (ThreeButtonPad, DisconnectedPort) and port is not None
                for port in ports):
            raise ValueError('three explicit pad/disconnected/unsupplied ports required')
        if not isinstance(devices, HardwareBus) or type(replace_controller_mapping) is not bool:
            raise ValueError('actual device bus and explicit mapping authority required')
        overlap = any(start < IO_END and IO_START < end for start, end in devices.ranges)
        if overlap and (not replace_controller_mapping or not _default_gpio_owner(devices)):
            raise ValueError('controller mapping would replace a supplied device owner')
        ranges = []
        for start, end in devices.ranges:
            if end <= IO_START or start >= IO_END:
                ranges.append((start, end))
            else:
                if start < IO_START:
                    ranges.append((start, IO_START))
                if end > IO_END:
                    ranges.append((IO_END, end))
        ranges.append((IO_START, IO_END))
        super().__init__(tuple(ranges))
        self.registers, self.ports, self.devices = registers, ports, devices

    def _parallel_read(self, index: int) -> int:
        if index in (1, 2, 3):
            port = self.ports[index - 1]
            if port is None:
                raise Boundary('controller input was not supplied')
            serial = self.registers[(9, 12, 15)[index - 1]]
            if serial & 0x30:
                raise Boundary('serial controller pin ownership requires its real device')
            direction = self.registers[index + 3]
            latch = self.registers[index]
            th_high = bool(latch & 0x40) if direction & 0x40 else True
            pins = port.input_pins(th_high)
            value = latch & 0x80
            for bit in range(7):
                source = latch if direction & (1 << bit) else pins
                value |= source & (1 << bit)
            return value
        return self.registers[index]

    def _parallel_write(self, index: int, value: int):
        if index == 0:
            return  # Version is physically read-only, not an acknowledgement.
        if index in (4, 5, 6):
            old_direction = self.registers[index]
            latch = self.registers[index - 3]
            if old_direction & 0x40 and not value & 0x40 and not latch & 0x40:
                raise Boundary('TH output-low to input pull-up requires an explicit switching clock')
        self.registers[index] = value

    def read(self, address: int, size: int) -> int:
        uint(address, 32)
        if size not in (1, 2, 4) or type(size) is not int:
            raise ValueError('actual BYTE/WORD/LONG hardware width required')
        physical = address & 0xFFFFFF
        if not (IO_START <= physical and physical + size <= IO_END):
            return self.devices.read(address, size)
        if size > 1 and address & 1:
            raise Boundary('odd controller WORD/LONG read')
        if size == 4:
            return (self.read(address, 2) << 16) | self.read(address + 2, 2)
        index = (physical - IO_START) // 2
        if index > 6:
            return self.devices.read(address, size)
        value = self._parallel_read(index)
        return value if size == 1 else value * 0x101

    def write(self, address: int, size: int, value: int):
        uint(address, 32)
        if size not in (1, 2, 4) or type(size) is not int:
            raise ValueError('actual BYTE/WORD/LONG hardware width required')
        uint(value, size * 8)
        physical = address & 0xFFFFFF
        if not (IO_START <= physical and physical + size <= IO_END):
            return self.devices.write(address, size, value)
        if size > 1 and address & 1:
            raise Boundary('odd controller WORD/LONG write')
        if size == 4:
            self.write(address, 2, value >> 16)
            self.write(address + 2, 2, value & 0xFFFF)
            return
        if size == 1 and not address & 1:
            return  # Only /LWR reaches the I/O chip; the even BYTE lane is unused.
        index = (physical - IO_START) // 2
        if index > 6:
            return self.devices.write(address, size, value)
        self._parallel_write(index, value & 0xFF)

    def progress(self, state, reason):
        return self.devices.progress(state, reason)
