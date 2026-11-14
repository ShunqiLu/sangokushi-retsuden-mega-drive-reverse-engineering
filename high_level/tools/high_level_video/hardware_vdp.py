"""Explicit Mode-5 VDP data effects, separated from console timing.

Candidate hardware fidelity: primary port algorithms and original Scene
integration run here, but no independent console runtime comparison has been
performed. See the package README for evidence
and pending hardware behavior. This module never loads a ROM or runs opcodes.
"""
from dataclasses import dataclass

from ..high_level_scene_flows.domain import Boundary, HardwareBus, SceneState, uint


@dataclass(frozen=True)
class VdpMemory:
    """Caller-owned, live, big-endian display memories; no implicit assets.

    CRAM uses the CPU-visible 0x0EEE color-bit positions, not a packed host
    palette. VSRAM stores its eleven meaningful bits. Reserved read bits must
    come from a supplied bus source, rather than being silently forced to zero.
    """

    vram: bytearray
    cram: bytearray
    vsram: bytearray
    registers: bytearray

    def __post_init__(self):
        for name, size in (('vram', 65536), ('cram', 128),
                           ('vsram', 80), ('registers', 32)):
            value = getattr(self, name)
            if type(value) is not bytearray or len(value) != size:
                raise ValueError('explicit live ' + name + ' backing of ' + str(size) + ' bytes required')
        for index in range(0, 128, 2):
            if self.word(self.cram, index) & ~0x0EEE:
                raise ValueError('CRAM backing must contain only meaningful bus-position color bits')
        for index in range(0, 80, 2):
            if self.word(self.vsram, index) & ~0x07FF:
                raise ValueError('VSRAM backing must contain eleven-bit scroll values')

    @staticmethod
    def word(backing: bytearray, index: int) -> int:
        return (backing[index] << 8) | backing[index + 1]

    @staticmethod
    def put_word(backing: bytearray, index: int, value: int) -> None:
        backing[index] = value >> 8
        backing[index + 1] = value & 255


class VdpStatusSource:
    """External timing/open-bus contract, not an always-ready implementation.

    A concrete provider owns FIFO/blanking/region/interrupt status and the
    hardware side effects of reading it. It must be driven independently of
    reference results. The controller never invents those bits or IRQ events.
    """

    stalls_cpu_on_ram_dma = False

    def read_status(self, controller) -> int:
        raise Boundary('VDP status requires explicit real timing and bus state')

    def read_hv(self, controller) -> int:
        raise Boundary('VDP HV counter requires explicit raster timing')

    def read_open_bus(self, controller) -> int:
        raise Boundary('VDP reserved DATA bits require explicit FIFO/open-bus state')

    def handles_progress(self, reason) -> bool:
        return False

    def progress(self, state, reason, controller):
        raise Boundary('VDP progress requires an explicit asynchronous supplier')


class SceneRamDmaSource:
    """Read DMA words from the very same live Scene RAM, never a snapshot.

    The explicit E00000..FFFFFF work-RAM mirror maps to SceneState's canonical
    FF0000 window. Cartridge, Z80, I/O and expansion sources remain boundaries.
    Reads go through SceneState, retaining its budget and ordered event record.
    """

    def __init__(self, state: SceneState):
        if type(state) is not SceneState:
            raise ValueError('one actual live SceneState required for VDP DMA')
        self.state = state

    def read_word(self, physical: int) -> int:
        uint(physical, 32, 'VDP DMA source address')
        if physical & 1 or not 0xE00000 <= physical <= 0xFFFFFE:
            raise Boundary('VDP DMA source is outside explicitly supplied live Scene RAM')
        return self.state.read(0xFF0000 | (physical & 0xFFFF), 2)


class SceneDataDmaSource(SceneRamDmaSource):
    """Read explicitly supplied cartridge DATA and live work RAM through Scene.

    This is a data-bus adapter, not a ROM loader or mapper. The caller must
    publish owned resources into this same Scene's ReadOnlyData. A missing
    word stops at that word; earlier granted effects remain visible. The
    ordinary cartridge window is deliberately separate from expansion, I/O
    and the Z80 bus, which require their own electrical/device authorities.
    """

    def read_word(self, physical: int) -> int:
        uint(physical, 32, 'VDP DMA source address')
        if physical & 1:
            raise Boundary('VDP DMA requires an even data-word source')
        if 0 <= physical <= 0x3FFFFE:
            return self.state.read(physical, 2)
        return super().read_word(physical)


@dataclass
class DmaTransfer:
    """A bounded transfer awaiting explicitly granted transfer units.

    RAM units are WORDs; copy/fill units are BYTEs. The word that arms fill is
    an ordinary DATA write and is not counted among its repeated fill units.
    This object records effects, not elapsed console time or IRQ completion.
    """

    kind: str
    remaining: int
    source_counter: int
    source_bank: int
    destination_code: int
    increment: int
    fill_byte: int | None = None


class VdpController:
    """Own command latch, address/code registers and display-memory effects.

    CPU DATA effects are applied in access order. DMA effects are applied only
    by advance_dma(units). This is not a cycle-accurate FIFO or renderer, and
    successful writes make no claim about blanking, busy time or interrupts.
    """

    def __init__(self, memory: VdpMemory, *, status: VdpStatusSource | None = None,
                 dma_source: SceneRamDmaSource | SceneDataDmaSource | None = None):
        if type(memory) is not VdpMemory:
            raise ValueError('typed explicit VDP memory required')
        if status is not None and not isinstance(status, VdpStatusSource):
            raise ValueError('typed explicit VDP timing source required')
        if dma_source is not None and type(dma_source) not in (SceneRamDmaSource, SceneDataDmaSource):
            raise ValueError('typed same-Scene RAM DMA source required')
        self.memory, self.status, self.dma_source = memory, status, dma_source
        self.address = 0
        self.address_high_latch = 0
        self.code = 0
        self.command_pending = False
        self.fill_armed = False
        self.pending_dma: DmaTransfer | None = None
        self.hv_latch: int | None = None

    @property
    def registers(self):
        return self.memory.registers

    def _mode5(self):
        if not self.registers[1] & 4:
            raise Boundary('VDP Mode 4 DATA/address behavior is not supplied by this Mode-5 device')
        if self.registers[1] & 0x80:
            raise Boundary('VDP extended VRAM addressing is outside this explicit 64-KiB backing')

    def _no_active_dma(self):
        if self.pending_dma is not None:
            raise Boundary('ordered VDP DMA requires explicit transfer progress before further port DATA/control access')

    def _advance_address(self, increment: int | None = None):
        if increment is None:
            increment = self.registers[15]
        self.address = (self.address + increment) & 0xFFFF

    def _vsram_index(self) -> int:
        index = self.address & 0x7E
        if index >= 80:
            raise Boundary('VDP VSRAM hole/model-dependent access is outside forty supplied words')
        return index

    def _write_word(self, code: int, value: int):
        destination = code & 15
        if destination == 1:
            index = self.address & 0xFFFE
            if self.address & 1:
                value = ((value & 255) << 8) | (value >> 8)
            VdpMemory.put_word(self.memory.vram, index, value)
        elif destination == 3:
            VdpMemory.put_word(self.memory.cram, self.address & 0x7E, value & 0x0EEE)
        elif destination == 5:
            VdpMemory.put_word(self.memory.vsram, self._vsram_index(), value & 0x07FF)
        else:
            raise Boundary('VDP DATA write requires a supplied VRAM/CRAM/VSRAM write command')

    def _status_source(self) -> VdpStatusSource:
        if self.status is None:
            raise Boundary('VDP status/HV/open bus was not explicitly supplied')
        return self.status

    def read_status(self) -> int:
        value = uint(self._status_source().read_status(self), 16, 'VDP status WORD')
        if (self.pending_dma is not None or self.fill_armed) and not value & 2:
            raise Boundary('supplied VDP status contradicts an uncompleted DMA transfer')
        # The provider owns status-read side effects such as collision flags.
        # A successful status read cancels the two-word command latch.
        self.command_pending = False
        return value

    def read_hv(self) -> int:
        if self.hv_latch is not None:
            return self.hv_latch
        return uint(self._status_source().read_hv(self), 16, 'VDP HV WORD')

    def read_data_word(self) -> int:
        self._mode5()
        self._no_active_dma()
        if self.fill_armed:
            raise Boundary('VDP DATA read during an armed fill requires a fuller hardware FIFO model')
        destination = self.code & 31
        if destination == 0:
            value = VdpMemory.word(self.memory.vram, self.address & 0xFFFE)
        elif destination in (4, 8):
            open_bus = uint(self._status_source().read_open_bus(self), 16, 'VDP open-bus WORD')
            if destination == 4:
                value = VdpMemory.word(self.memory.vsram, self._vsram_index()) | (open_bus & 0xF800)
            else:
                value = VdpMemory.word(self.memory.cram, self.address & 0x7E) | (open_bus & 0xF111)
        else:
            raise Boundary('VDP invalid/byte-prefetch DATA read requires a supplied hardware model')
        self.command_pending = False
        self._advance_address()
        return value

    def write_data_word(self, value: int) -> None:
        uint(value, 16, 'VDP DATA WORD')
        self._mode5()
        self._no_active_dma()
        self._write_word(self.code, value)
        self.command_pending = False
        self._advance_address()
        if self.fill_armed:
            # Normal initiating WORD first; repeated high BYTE starts at the
            # newly incremented address and its adjacent internal BYTE lane.
            self.pending_dma = self._transfer('fill', value >> 8)
            self.fill_armed = False

    def _write_register(self, index: int, value: int) -> None:
        if index > 23:
            raise Boundary('undocumented VDP register write is not silently emulated')
        if index > 10 and not self.registers[1] & 4:
            return  # Actual Mode-4 access restriction, not a missing ACK.
        if index == 0 and (value ^ self.registers[0]) & 2:
            latched = None
            if value & 2:
                latched = uint(self._status_source().read_hv(self), 16, 'VDP latched HV WORD')
            self.hv_latch = latched
        self.registers[index] = value

    def _transfer(self, kind: str, fill_byte: int | None = None) -> DmaTransfer:
        length = self.registers[19] | (self.registers[20] << 8)
        source = self.registers[21] | (self.registers[22] << 8)
        bank = (self.registers[23] & 0x7F) << 17
        return DmaTransfer(kind, length or 65536, source, bank,
                           self.code & 15, self.registers[15], fill_byte)

    def _start_dma(self) -> None:
        if not (self.code & 0x20 and self.registers[1] & 0x10):
            return
        mode = self.registers[23] >> 6
        if mode == 3:
            if not self.code & 0x10:
                raise Boundary('VDP copy without CD4 would lock actual hardware; no synthetic completion')
            self.pending_dma = self._transfer('copy')
        elif mode == 2:
            if self.code & 15 != 1:
                raise Boundary('CRAM/VSRAM DMA fill requires explicit FIFO provenance, not a fabricated fill value')
            self.fill_armed = True
        else:
            if self.code & 15 not in (1, 3, 5):
                raise Boundary('VDP RAM DMA requires a complete supported destination command')
            self.pending_dma = self._transfer('ram')

    def write_control_word(self, value: int) -> None:
        uint(value, 16, 'VDP control WORD')
        self._no_active_dma()
        if self.fill_armed:
            raise Boundary('control change during an armed DMA fill needs explicit hardware sequencing')
        if self.command_pending:
            self.address_high_latch = (value & 3) << 14
            self.address = self.address_high_latch | (self.address & 0x3FFF)
            self.code = (self.code & 3) | ((value >> 2) & 0x3C)
            self.command_pending = False
            self._start_dma()
            return
        if value & 0xC000 == 0x8000:
            # A register WORD is not the first half of a two-word command.
            self._write_register((value >> 8) & 31, value & 255)
            self.address = self.address_high_latch | (value & 0x3FFF)
            self.code = (self.code & 0x3C) | ((value >> 14) & 3)
            return
        self._mode5()
        self.address = self.address_high_latch | (value & 0x3FFF)
        self.code = (self.code & 0x3C) | ((value >> 14) & 3)
        self.command_pending = True

    def advance_dma(self, units: int) -> int:
        """Apply at most explicit units; return actual units, never a wait ACK.

        The caller supplies transfer slots from its own timing policy. Missing
        source data leaves the current unit unconsumed. Completed earlier units
        remain visible, and transfers cannot exceed the sixteen-bit DMA count.
        """
        if type(units) is not int or not 0 <= units <= 65536:
            raise ValueError('bounded nonnegative explicit DMA units required')
        transfer = self.pending_dma
        if transfer is None or units == 0:
            return 0
        completed = 0
        while completed < units and transfer.remaining:
            if transfer.kind == 'ram':
                if self.dma_source is None:
                    raise Boundary('VDP RAM DMA has no explicit same-Scene source')
                physical = transfer.source_bank | (transfer.source_counter << 1)
                value = self.dma_source.read_word(physical)
                self._write_word(transfer.destination_code, value)
            elif transfer.kind == 'copy':
                # Internal byte DMA selects the lane adjacent to its counter.
                # Read each live byte just before writing, preserving overlap.
                value = self.memory.vram[transfer.source_counter ^ 1]
                self.memory.vram[self.address ^ 1] = value
            elif transfer.kind == 'fill':
                if transfer.fill_byte is None:
                    raise ValueError('complete initiating fill DATA word required')
                self.memory.vram[self.address ^ 1] = transfer.fill_byte
            else:
                raise ValueError('unknown typed DMA operation')
            self._advance_address(transfer.increment)
            transfer.source_counter = (transfer.source_counter + 1) & 0xFFFF
            transfer.remaining -= 1
            self.registers[19] = transfer.remaining & 255
            self.registers[20] = (transfer.remaining >> 8) & 255
            self.registers[21] = transfer.source_counter & 255
            self.registers[22] = transfer.source_counter >> 8
            completed += 1
        if transfer.remaining == 0:
            self.pending_dma = None
        return completed


class SceneVdpHardwareBus(HardwareBus):
    """Compose VDP data/control/HV ports with the caller's existing devices.

    The original device object and all display backings are retained. PSG and
    other hardware are delegated. Replacing an existing mapping is explicit;
    only a bare unsupplied HardwareBus mapping may be replaced. SceneState owns
    CPU access events, so this adapter does not duplicate them or touch SR/IRQ.
    """

    VDP_WINDOW = (0xC00000, 0xC00010)

    def __init__(self, controller: VdpController, devices: HardwareBus,
                 *, replace_vdp_mapping: bool = False):
        if type(controller) is not VdpController or not isinstance(devices, HardwareBus):
            raise ValueError('typed VDP controller and explicit existing bus required')
        if type(replace_vdp_mapping) is not bool:
            raise ValueError('explicit mapping replacement decision required')
        remaining = []
        for start, end in devices.ranges:
            if start < self.VDP_WINDOW[1] and self.VDP_WINDOW[0] < end:
                if not replace_vdp_mapping or type(devices) is not HardwareBus:
                    raise ValueError('cannot implicitly replace an actual device owner; compose VDP before save/other wrappers')
                if start < self.VDP_WINDOW[0]:
                    remaining.append((start, self.VDP_WINDOW[0]))
                if end > self.VDP_WINDOW[1]:
                    remaining.append((self.VDP_WINDOW[1], end))
            else:
                remaining.append((start, end))
        super().__init__(tuple(remaining) + (self.VDP_WINDOW,))
        self.controller, self.devices = controller, devices
        self.delegated_ranges = tuple(remaining)
        self.scene: SceneState | None = None
        self._cpu_dma_stall_active = False

    def bind_scene(self, state: SceneState) -> None:
        """Attach one actual Scene after constructing its composed hardware."""
        if type(state) is not SceneState:
            raise ValueError('one actual SceneState required')
        if self.scene is not None and self.scene is not state:
            raise ValueError('VDP bus cannot silently change its live Scene')
        owner, seen = state.hardware, set()
        while isinstance(owner, HardwareBus) and id(owner) not in seen:
            if owner is self:
                break
            seen.add(id(owner))
            owner = getattr(owner, 'devices', None)
        if owner is not self:
            raise ValueError('VDP bus must be a real owner in this same Scene hardware chain')
        source = self.controller.dma_source
        if source is not None and source.state is not state:
            raise ValueError('DMA must share the actual Scene RAM, not a foreign backing')
        self.controller.dma_source = source or SceneRamDmaSource(state)
        self.scene = state

    @staticmethod
    def _physical(address: int, size: int) -> int:
        uint(address, 32, 'hardware address')
        if type(size) is not int or size not in (1, 2, 4):
            raise ValueError('strict BYTE/WORD/LONG hardware access required')
        physical = address & 0xFFFFFF
        if size > 1 and physical & 1:
            raise Boundary('unaligned VDP WORD/LONG access')
        return physical

    def _delegated(self, physical: int, size: int) -> bool:
        return any(start <= physical and physical + size <= end
                   for start, end in self.delegated_ranges)

    def _read_cycle(self, physical: int, size: int) -> int:
        select = (physical - self.VDP_WINDOW[0]) & 0x0E
        if select < 4:
            word = self.controller.read_data_word()
        elif select < 8:
            word = self.controller.read_status()
        else:
            word = self.controller.read_hv()
        return ((word >> (0 if physical & 1 else 8)) & 255) if size == 1 else word

    def _write_cycle(self, physical: int, size: int, value: int) -> None:
        select = (physical - self.VDP_WINDOW[0]) & 0x0E
        if select < 4:
            if size == 1:
                value = (value << 8) | value
            self.controller.write_data_word(value)
        elif select < 8:
            if size == 1:
                raise Boundary('BYTE control writes require separately confirmed lane semantics')
            self.controller.write_control_word(value)
        else:
            raise Boundary('write to HV/test ports is not a fabricated successful device operation')

    def read(self, address: int, size: int) -> int:
        physical = self._physical(address, size)
        if self.VDP_WINDOW[0] <= physical and physical + size <= self.VDP_WINDOW[1]:
            if size == 4:
                high = self._read_cycle(physical, 2)
                return (high << 16) | self._read_cycle(physical + 2, 2)
            return self._read_cycle(physical, size)
        if self._delegated(physical, size):
            return self.devices.read(address, size)
        raise Boundary('outside complete explicitly owned VDP/other-device access')

    def write(self, address: int, size: int, value: int) -> None:
        physical = self._physical(address, size)
        uint(value, size * 8, 'hardware DATA')
        if self.VDP_WINDOW[0] <= physical and physical + size <= self.VDP_WINDOW[1]:
            if size == 4:
                self._write_cycle(physical, 2, value >> 16)
                self._write_cycle(physical + 2, 2, value & 0xFFFF)
            else:
                self._write_cycle(physical, size, value)
            return
        if self._delegated(physical, size):
            self.devices.write(address, size, value)
            return
        raise Boundary('outside complete explicitly owned VDP/other-device access')

    def progress(self, state, reason):
        if self.scene is not None and state is not self.scene:
            raise ValueError('VDP asynchronous progress must retain the same Scene')
        status = self.controller.status
        if status is not None and status.handles_progress(reason):
            return status.progress(state, reason, self.controller)
        return self.devices.progress(state, reason)

    def after_write(self, state, address, size, value):
        """Honor explicit RAM-DMA CPU hold after the initiating write is logged.

        In the clocked profile, the original CPU must not release BUSREQ,
        change source RAM or restore a control register before its RAM DMA
        finishes. Transfer units come only from the actual status/scheduler
        owner. Fill/copy keep their independent original busy-poll behavior.
        The default bounded data profile remains manually stepped.
        """
        status = self.controller.status
        if (status is not None and status.stalls_cpu_on_ram_dma
                and not self._cpu_dma_stall_active):
            if self.scene is not state:
                raise ValueError('RAM-DMA CPU hold requires this actual bound Scene')
            self._cpu_dma_stall_active = True
            try:
                while (self.controller.pending_dma is not None
                       and self.controller.pending_dma.kind == 'ram'):
                    if not status.handles_progress('vdp-dma'):
                        raise Boundary('RAM-DMA CPU hold requires explicit transfer events')
                    status.progress(state, 'vdp-dma', self.controller)
            finally:
                self._cpu_dma_stall_active = False
        return self.devices.after_write(state, address, size, value)
