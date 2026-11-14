"""Explicit DMA grants after real CPU writes, independent of a busy poll.

This supplies event ordering, not CPU/master-clock durations. It lets a cold
boot fill progress while original software copies sound bytes or clears RAM.
No default grant, complete flag, status bit or synthetic port write is supplied.
"""
from collections import Counter, deque
from dataclasses import dataclass

from ..high_level_scene_flows.domain import Boundary, HardwareBus, SceneState, uint
from .hardware_vdp import VdpController, SceneVdpHardwareBus


@dataclass(frozen=True)
class WriteDmaGrant:
    """One caller-supplied grant following the Nth matching physical write."""
    physical_address: int
    size: int
    value: int
    occurrence: int
    units: int

    def __post_init__(self):
        uint(self.physical_address, 32)
        if self.physical_address > 0xFFFFFF:
            raise ValueError('actual 24-bit physical write address required')
        if type(self.size) is not int or self.size not in (1, 2, 4):
            raise ValueError('actual BYTE/WORD/LONG write width required')
        uint(self.value, self.size * 8)
        if type(self.occurrence) is not int or self.occurrence < 1:
            raise ValueError('positive explicit matching-write ordinal required')
        if type(self.units) is not int or not 0 <= self.units <= 65536:
            raise ValueError('explicit bounded transfer-unit grant required')

    @property
    def key(self):
        return self.physical_address, self.size, self.value


class SceneWriteDmaEvents(HardwareBus):
    """Wrap the actual device chain without replacing any MMIO ownership.

    Original CPU writes are already applied and recorded by SceneState before
    this hook. The inner RAM-DMA hold still runs first. Fill/copy can then
    consume exactly the external grants scheduled at these observable writes.
    Read accesses never receive hidden clocks or transfer slots.
    """
    def __init__(self, devices: HardwareBus, controller: VdpController,
                 grants: tuple[WriteDmaGrant, ...]):
        if not isinstance(devices, HardwareBus) or type(controller) is not VdpController:
            raise ValueError('actual device chain and VDP owner required')
        if type(grants) is not tuple or any(type(grant) is not WriteDmaGrant for grant in grants):
            raise ValueError('finite explicit typed write-event grant tuple required')
        last = {}
        for grant in grants:
            if grant.occurrence <= last.get(grant.key, 0):
                raise ValueError('grant occurrences for one write key must increase')
            last[grant.key] = grant.occurrence
        super().__init__(devices.ranges)
        self.devices, self.controller = devices, controller
        self.grants, self.seen = deque(grants), Counter()
        self.scene = None
        self.consumed_grants = 0

    def bind_scene(self, state: SceneState):
        if type(state) is not SceneState or self.scene not in (None, state):
            raise ValueError('one actual Scene owner required')
        owner, visited, found_self, found_vdp = state.hardware, set(), False, False
        while isinstance(owner, HardwareBus) and id(owner) not in visited:
            visited.add(id(owner))
            found_self |= owner is self
            if type(owner) is SceneVdpHardwareBus and owner.controller is self.controller:
                found_vdp = owner.scene is state
            owner = getattr(owner, 'devices', None)
        if not found_self or not found_vdp:
            raise ValueError('event bus and bound VDP must share this actual Scene chain')
        self.scene = state

    def read(self, address, size):
        return self.devices.read(address, size)

    def write(self, address, size, value):
        return self.devices.write(address, size, value)

    def progress(self, state, reason):
        return self.devices.progress(state, reason)

    def after_write(self, state, address, size, value):
        if state is not self.scene:
            raise ValueError('write events require the actual bound Scene')
        self.devices.after_write(state, address, size, value)
        key = address & 0xFFFFFF, size, value
        self.seen[key] += 1
        if not self.grants or self.grants[0].key != key:
            return
        grant = self.grants[0]
        if self.seen[key] < grant.occurrence:
            return
        if self.seen[key] > grant.occurrence:
            raise Boundary('ordered external DMA grant missed its supplied write event')
        if self.controller.pending_dma is None:
            raise Boundary('external write-event DMA grant has no actual pending transfer')
        completed = self.controller.advance_dma(grant.units)
        self.grants.popleft()
        self.consumed_grants += 1
        state.events.append(('external_write_dma_grant', *key,
                             grant.occurrence, grant.units, completed))

    def require_consumed(self):
        if self.grants:
            raise Boundary('finite external write-event DMA grants remain unused')
