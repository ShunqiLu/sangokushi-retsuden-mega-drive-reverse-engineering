"""Narrow complete-save adapter onto one existing live Scene bus.

No SaveImage, ROM view or HardwareBus is synthesized.  Cartridge SRAM must
already be explicitly mapped by that Scene's supplied hardware implementation.
Only the original odd BYTE lanes are admitted in its 0x200000..0x204000 range.
Missing mapping/read/write ownership remains a real Boundary, never a fake ACK.
"""
from .domain import StorageState, Boundary, uint
from ..high_level_scene_flows.domain import SceneState


class SceneStorageState(StorageState):
    """Named exact-state bridge used only by the complete retained save core."""

    def __init__(self, scene: SceneState):
        if type(scene) is not SceneState:
            raise ValueError('one exact live SceneState required for storage bridge')
        self.scene = scene

    def validate_bus(self):
        if type(self.scene) is not SceneState:
            raise ValueError('storage bridge must retain its exact live SceneState')
        return self

    @property
    def ram(self):
        return self.scene.ram

    @property
    def data(self):
        return self.scene.data

    @property
    def events(self):
        return self.scene.events

    @property
    def reads(self):
        return self.scene.reads

    @property
    def max_reads(self):
        return self.scene.max_reads

    @property
    def sr(self):
        return self.scene.sr

    @sr.setter
    def sr(self, value):
        self.scene.sr = uint(value, 16, 'live complete storage SR-X')

    def _address(self, address, size):
        self.validate_bus()
        uint(address, 32)
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('strict DATA width required')
        physical = address & 0xFFFFFF
        if 0x200000 <= physical < 0x204000:
            if size != 1 or not physical & 1:
                raise Boundary('original cartridge SRAM odd BYTE lane required')
            if not self.scene.hardware.contains(physical, size):
                raise Boundary('actual live cartridge SRAM mapping not supplied')
        return address

    def read(self, address, size):
        return self.scene.read(self._address(address, size), size)

    def write(self, address, size, value):
        address = self._address(address, size)
        uint(value, size * 8)
        # The supplied Scene hardware owns every SRAM write/read and any stop.
        self.scene.write(address, size, value)
