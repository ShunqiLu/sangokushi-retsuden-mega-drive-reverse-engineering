"""Attach one explicit cartridge save medium to the recovered Scene bus.

Confirmed local contract: domain.SaveImage and the complete storage algorithms
use 8 KiB of logical data at odd BYTE addresses 0x200001..0x203FFF. This module
only composes that existing contract with the caller's other hardware. It does
not implement A130F1 gating, console timing, automatic files, or missing device
responses. Read/write permissions remain owned by the supplied SaveImage.
"""
from .domain import SaveImage
from ..high_level_scene_flows.domain import Boundary, HardwareBus, uint


class SceneSaveHardwareBus(HardwareBus):
    """One live save backing and one explicit owner for every other device.

    The supplied objects are retained by identity. SceneState records successful
    accesses in its existing event list; this adapter adds no duplicate event,
    RAM copy, extra logical save image, or successful asynchronous response.
    """

    SAVE_WINDOW = (0x200000, 0x204000)

    def __init__(self, save_image: SaveImage, devices: HardwareBus):
        if type(save_image) is not SaveImage:
            raise ValueError('one explicit typed live SaveImage required')
        if not isinstance(devices, HardwareBus):
            raise ValueError('explicit existing device bus required')
        # HardwareBus rejects overlapping ownership, including an existing
        # cartridge mapping. No implicit override or fallback owner is added.
        super().__init__(devices.ranges + (self.SAVE_WINDOW,))
        self.save_image = save_image
        self.devices = devices

    def _physical_access(self, address: int, size: int) -> int:
        uint(address, 32, 'hardware address')
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('strict hardware DATA width required')
        return address & 0xFFFFFF

    def read(self, address: int, size: int) -> int:
        physical = self._physical_access(address, size)
        if self.SAVE_WINDOW[0] <= physical < self.SAVE_WINDOW[1]:
            return self.save_image.read(physical, size)
        if not self.devices.contains(physical, size):
            raise Boundary('outside explicitly supplied device mapping')
        return self.devices.read(address, size)

    def write(self, address: int, size: int, value: int) -> None:
        physical = self._physical_access(address, size)
        uint(value, size * 8, 'hardware DATA')
        if self.SAVE_WINDOW[0] <= physical < self.SAVE_WINDOW[1]:
            self.save_image.write(physical, size, value)
            return
        if not self.devices.contains(physical, size):
            raise Boundary('outside explicitly supplied device mapping')
        self.devices.write(address, size, value)

    def progress(self, state, reason):
        """Retain the same live Scene and the other device's real wait result."""
        return self.devices.progress(state, reason)
