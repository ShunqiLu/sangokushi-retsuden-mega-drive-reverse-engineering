"""Finite caller-supplied video status edges, without an inferred clock.

This external-event adapter owns no game RAM, IRQ delivery, pending DMA or
readiness flag. Original AF48 still reads and tests the actual VDP status.
"""
from collections import deque
from dataclasses import dataclass

from ..high_level_main_flows.domain import Boundary, HardwareBus
from .frame_interrupts import SuppliedVideoEvents, VideoBusState


@dataclass(frozen=True)
class SuppliedVideoEdge:
    """One explicit external status snapshot for one original edge wait."""
    reason: str
    bus_state: VideoBusState

    def __post_init__(self):
        if self.reason not in ('vblank-end', 'vblank-start') or type(self.bus_state) is not VideoBusState:
            raise ValueError('explicit original video-edge reason and complete snapshot required')
        expected = self.reason == 'vblank-start'
        if bool(self.bus_state.status_without_dma & 8) != expected:
            raise ValueError('supplied bit3 does not describe the named external edge')


class FiniteVideoEdgeSchedule(HardwareBus):
    """Delegate all devices; consume only the declared finite external plan.

    Callers must bind the actual SuppliedVideoEvents to the same Scene/VDP as
    usual. A status read never consumes an event. Only the original loop's
    explicit progress call can accept its next exactly named edge. Unknown
    reasons delegate, and an exhausted/out-of-order plan remains a boundary.
    No wall time, autonomous frames, default pulse, fake IRQ or DMA grant is
    inferred. The next IRQ must still be supplied independently by the caller.
    """
    def __init__(self, video_events: SuppliedVideoEvents,
            edges: tuple[SuppliedVideoEdge, ...], devices: HardwareBus):
        if type(video_events) is not SuppliedVideoEvents or not isinstance(devices, HardwareBus):
            raise ValueError('actual video event source and explicit other devices required')
        if type(edges) is not tuple or any(type(edge) is not SuppliedVideoEdge for edge in edges):
            raise ValueError('finite explicit SuppliedVideoEdge tuple required')
        super().__init__(devices.ranges)
        self.video_events, self.devices = video_events, devices
        self.edges = deque(edges)
        self.consumed = []

    def read(self, address, size):
        return self.devices.read(address, size)

    def write(self, address, size, value):
        return self.devices.write(address, size, value)

    def after_write(self, state, address, size, value):
        return self.devices.after_write(state, address, size, value)

    def progress(self, state, reason):
        if reason not in ('vblank-end', 'vblank-start'):
            return self.devices.progress(state, reason)
        if state is not self.video_events.state:
            raise Boundary('external video edge belongs to another/unbound Scene')
        self.video_events._checked_controller(self.video_events.controller)
        if not self.edges:
            raise Boundary('finite external video edge plan exhausted')
        edge = self.edges[0]
        if edge.reason != reason:
            raise Boundary('next external video edge does not match the actual waiting loop')
        if bool(self.video_events.bus_state.status_without_dma & 8) == bool(edge.bus_state.status_without_dma & 8):
            raise Boundary('supplied snapshot does not transition the actual bit3 state')
        self.video_events.set_bus_state(edge.bus_state)
        self.edges.popleft()
        self.consumed.append(edge)
        state.events.append(('external_video_edge', reason, edge.bus_state.status_without_dma,
            edge.bus_state.hv, edge.bus_state.open_bus))
