"""Explicit external video events and original 481E interrupt/RTE execution.

confirmed: original vector table 000078 and 481E..4858 listing. No opcode
execution, automatic frame clock, guessed IRQ acknowledgment or fake wait flag.
"""
from dataclasses import dataclass
from collections import deque

from ..high_level_main_flows.domain import (
    Boundary, SceneState, Cursor, uint, checked_state, checked_cursor,
)
from ..high_level_main_flows.contexts_gameplay import (
    FirstDeploymentFrame, first_replace, MovementContinuationBoundary,
)
from ..high_level_main_flows.business_movement_support import _movement_frame
from .hardware_vdp import VdpController, VdpStatusSource, SceneVdpHardwareBus


RTE_REASON = 'real 4856 RTE target/context is not an ordinary Lowbank child return'


def _controller_owner(state, controller):
    """Require a real composed device owner, not a foreign controller snapshot."""
    checked_state(state)
    if type(controller) is not VdpController:
        raise ValueError('actual VdpController required')
    owner, seen = state.hardware, set()
    while owner is not None and id(owner) not in seen:
        if type(owner) is SceneVdpHardwareBus and owner.controller is controller:
            if owner.scene is not state:
                raise ValueError('VDP owner must already bind this exact Scene')
            return owner
        seen.add(id(owner))
        owner = getattr(owner, 'devices', None)
    raise ValueError('controller is not an actual owner in this Scene hardware chain')


@dataclass(frozen=True)
class VideoBusState:
    """Externally supplied hardware state; no frame/line/FIFO values are inferred.

    DMA busy is excluded because the owned data device supplies that one bit.
    None is an honest unavailable HV/open-bus boundary, not zero.
    """
    status_without_dma: int
    hv: int | None
    open_bus: int | None

    def __post_init__(self):
        uint(self.status_without_dma, 16)
        if self.status_without_dma & 2:
            raise ValueError('DMA busy comes only from the actual pending transfer')
        for value in (self.hv, self.open_bus):
            if value is not None:
                uint(value, 16)


class SuppliedVideoEvents(VdpStatusSource):
    """Finite explicit DMA slots plus a caller-owned current raster/bus state.

    Each slot is a transfer-unit grant, not a CPU/master-clock duration. RAM
    DMA consumes WORDs; copy/fill consumes BYTEs, as VdpController specifies.
    Missing grants never turn into an automatic DMA-ready result.
    """
    def __init__(self, bus_state: VideoBusState, dma_slots: tuple[int, ...], *,
                 cpu_dma_stalls: bool = False):
        if type(bus_state) is not VideoBusState or type(dma_slots) is not tuple:
            raise ValueError('explicit video snapshot and finite DMA slot tuple required')
        for units in dma_slots:
            if type(units) is not int or not 0 <= units <= 65536:
                raise ValueError('DMA slot must grant 0..65536 actual transfer units')
        if type(cpu_dma_stalls) is not bool:
            raise ValueError('explicit CPU RAM-DMA hold policy required')
        self.stalls_cpu_on_ram_dma = cpu_dma_stalls
        self.bus_state, self.dma_slots = bus_state, deque(dma_slots)
        self.state = self.controller = None
        self.consumed_slots = 0

    def bind_scene(self, state: SceneState, controller: VdpController):
        _controller_owner(state, controller)
        if controller.status is not self:
            raise ValueError('video events must be this actual controller status supplier')
        if self.state is not None and (self.state is not state or self.controller is not controller):
            raise ValueError('video event supply cannot change its actual Scene/device')
        self.state, self.controller = state, controller

    def set_bus_state(self, bus_state: VideoBusState):
        if type(bus_state) is not VideoBusState:
            raise ValueError('explicit complete external video bus snapshot required')
        self.bus_state = bus_state

    def _checked_controller(self, controller):
        if self.state is None or controller is not self.controller:
            raise ValueError('video event supply requires its bound actual controller')
        _controller_owner(self.state, controller)

    def read_status(self, controller):
        self._checked_controller(controller)
        busy = controller.pending_dma is not None or controller.fill_armed
        return self.bus_state.status_without_dma | (2 if busy else 0)

    def read_hv(self, controller):
        self._checked_controller(controller)
        if self.bus_state.hv is None:
            raise Boundary('external raster supplied no HV counter')
        return self.bus_state.hv

    def read_open_bus(self, controller):
        self._checked_controller(controller)
        if self.bus_state.open_bus is None:
            raise Boundary('external video bus supplied no reserved-data value')
        return self.bus_state.open_bus

    def handles_progress(self, reason):
        return reason == 'vdp-dma'

    def progress(self, state, reason, controller):
        self._checked_controller(controller)
        if state is not self.state or reason != 'vdp-dma':
            raise ValueError('explicit same-Scene VDP DMA wait required')
        if not self.dma_slots:
            raise Boundary('external DMA transfer-slot supply exhausted')
        units = self.dma_slots.popleft()
        self.consumed_slots += 1
        completed = controller.advance_dma(units)
        state.events.append(('external_dma_slot', units, completed))
        return completed


@dataclass(frozen=True)
class ExecutionPoint:
    """One actual suspended software point, full carriers and banked other SP.

    PC names a recovered continuation; it is never fetched or interpreted.
    When SR.S=1 inactive_stack is USP; when SR.S=0 it is SSP. Both are caller
    facts, not allocated stacks. All pointer carriers must use the same Scene.
    """
    pc: int
    frame: FirstDeploymentFrame
    inactive_stack: Cursor

    def validate(self, state):
        uint(self.pc, 32)
        if self.pc & 1:
            raise Boundary('odd interrupted PC requires original address-error handling')
        _movement_frame(state, self.frame)
        checked_cursor(self.inactive_stack, state)
        if self.frame.status != state.sr & 31:
            raise ValueError('actual full SR and suspended frame CCR disagree')
        if state.sr & 0x8000:
            raise Boundary('trace exception sequencing is not supplied')
        return self

    @classmethod
    def from_boundary(cls, state, boundary, inactive_stack):
        if type(boundary) is not MovementContinuationBoundary:
            raise ValueError('actual recovered wait/continuation boundary required')
        return cls(boundary.target, boundary.context, inactive_stack).validate(state)


@dataclass(frozen=True)
class InterruptRequest:
    """External assertion after device acknowledge chooses an original autovector.

    Only cartridge level4 and level6 vectors are named. A status VBlank bit
    alone does not create this event, and masked requests are not acknowledged.
    """
    level: int

    def __post_init__(self):
        if type(self.level) is not int or self.level not in (4, 6):
            raise ValueError('only recovered original level4/level6 autovectors supported')


@dataclass(frozen=True)
class InterruptResult:
    point: ExecutionPoint
    accepted: bool
    vector_address: int | None
    handler: int | None


class OriginalInterruptRuntime:
    """Run the existing original VBlank business core on the real exception stack.

    The adapter supplies exception entry/banked stack ownership and receives
    the original handler's exact RTE boundary. It does not reimplement its
    dispatch, controller poll, DMA, graphics, RNG or MOVEM business effects.
    """
    def __init__(self, state: SceneState):
        self.state = checked_state(state)
        self._active = False

    def deliver(self, point: ExecutionPoint, request: InterruptRequest):
        if type(point) is not ExecutionPoint or type(request) is not InterruptRequest:
            raise ValueError('explicit actual execution point and IRQ request required')
        state = self.state
        point.validate(state)
        if self._active:
            raise Boundary('nested interrupt needs an explicit suspended handler point')
        if request.level <= state.sr >> 8 & 7:
            return InterruptResult(point, False, None, None)
        if request.level == 4:
            raise Boundary('original level4 vector enters 4A4C masked-interrupt infinite loop; no fabricated return')
        supervisor = bool(state.sr & 8192)
        old_sr = state.sr
        old_ssp = point.frame.stack_cursor if supervisor else point.inactive_stack
        physical = old_ssp.base & 16777215
        if old_ssp.base & 1 or not 16711750 <= physical <= 16777210:
            raise Boundary('IRQ exception, fifteen saved LONGs and child slot require actual aligned work-RAM SSP')
        exception_stack = old_ssp.advance(-6)
        old_ssp.advance(-4).set_long(0, point.pc)
        exception_stack.set_word(0, old_sr)
        state.sr = old_sr & 30975 | 8192 | request.level << 8
        entered = first_replace(point.frame, stack_cursor=exception_stack, status=state.sr & 31)
        state.events.append(('interrupt_enter', 6, 120, 18462, point.pc, old_sr))
        self._active = True
        try:
            from ..high_level_remaining_flows.business_lowbank import lowbank_process_device_control_6_fields
            try:
                from ..high_level_main_flows.intro_irq_program import run_original_or_intro_irq
                run_original_or_intro_irq(self, state, entered, lowbank_process_device_control_6_fields)
            except MovementContinuationBoundary as boundary:
                if boundary.reason != RTE_REASON:
                    raise
                returned = _movement_frame(state, boundary.context)
                if returned.stack_cursor.base != old_ssp.base:
                    raise Boundary('original RTE did not finish at the actual supervisor-stack postframe')
                if boundary.target & 1:
                    raise Boundary('original RTE selected odd PC; address-error continuation required')
                if state.sr & 8192:
                    other = point.inactive_stack if supervisor else point.frame.stack_cursor
                else:
                    user_sp = point.inactive_stack if supervisor else point.frame.stack_cursor
                    returned = first_replace(returned, stack_cursor=user_sp)
                    other = old_ssp
                resumed = ExecutionPoint(boundary.target, returned, other).validate(state)
                state.events.append(('interrupt_rte', resumed.pc, state.sr, resumed.frame.stack_cursor.base))
                return InterruptResult(resumed, True, 120, 18462)
            raise Boundary('original interrupt core returned without its actual RTE boundary')
        finally:
            self._active = False

