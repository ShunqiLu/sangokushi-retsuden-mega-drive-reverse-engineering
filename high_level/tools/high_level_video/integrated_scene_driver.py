"""Explicit event driver for the exact cold-created persistent city main.

No clock, pad plan, DMA grant, edge, BUSACK or software-ready value is created.
Only an explicit call consumes one event from its existing actual owner.
"""
import threading
from dataclasses import dataclass

from ..high_level_main_flows.domain import Boundary
from ..high_level_main_flows.bootstrap_steps import BootstrapMainWait
from ..high_level_main_flows.bootstrap_stacks import BankedStackControl
from ..high_level_main_flows.city_scene_steps import PersistentCitySceneSession
from ..high_level_main_flows.city_cold_reset import CityColdResetSession
from ..high_level_main_flows.controller_setup_steps import ControllerSetupWait
from ..high_level_main_flows.force_turn_steps import ForceTurnWait
from ..high_level_gameplay_flow.scene_load_steps import GameplaySceneWait
from ..high_level_scene_flows.scripted_scene_steps import ScriptedSceneWait
from ..high_level_scene_flows.duel_scene_steps import DuelSceneWait
from ..high_level_dynamic_flows.allocation_steps import AllocationSceneWait
from ..high_level_gameplay_flow.battle_trigger_steps import BattleTriggerWait
from ..high_level_input.hardware_controller import (
    PadButtons, ThreeButtonPad, SceneControllerHardwareBus)
from ..high_level_audio_engine.live_cold_driver import LiveColdDriverRig
from ..high_level_audio_engine.hardware_scene import SoundDevice
from ..high_level_audio_engine.control_reset import FinitePulseSoundSchedule
from .frame_interrupts import (
    SuppliedVideoEvents, VideoBusState, OriginalInterruptRuntime, InterruptRequest)
from .finite_edges import FiniteVideoEdgeSchedule


WAIT_TYPES = (BootstrapMainWait, ControllerSetupWait, ForceTurnWait, GameplaySceneWait, ScriptedSceneWait, AllocationSceneWait, DuelSceneWait, BattleTriggerWait)
DEVICE_EVENTS = ('vblank-end', 'vblank-start', 'sound-bus-acquire', 'vdp-dma')


def _chain_member(state, candidate):
    current, seen = state.hardware, set()
    while current is not None and id(current) not in seen:
        if current is candidate:
            return True
        seen.add(id(current))
        current = getattr(current, 'devices', None)
    return False


@dataclass(frozen=True)
class PhysicalPadSnapshot:
    """One explicitly supplied physical level change, not a game RAM write."""
    port: int
    buttons: PadButtons

    def __post_init__(self):
        if type(self.port) is not int or not 0 <= self.port <= 2 or type(self.buttons) is not PadButtons:
            raise ValueError('explicit physical port and exact PadButtons required')


@dataclass(frozen=True)
class IntegratedInterruptStep:
    """A masked request returns its unchanged live wait, never a fake wakeup."""
    interrupt: object
    waiting: object


class IntegratedSceneDriver:
    """One exact LiveColdDriverRig, with reset/main wait mirrors kept coherent.

    Construction neither starts a Session nor supplies any external event.
    The caller creates the exact CityColdResetSession/PersistentCitySceneSession
    pair at the original cold tail; no live old main can be hot-swapped here.
    Audio execution and chip clocks remain independently explicit owner calls.
    """

    def __init__(self, rig: LiveColdDriverRig):
        if type(rig) is not LiveColdDriverRig:
            raise ValueError('the actual retained LiveColdDriverRig is required')
        self.rig, self.state = (rig, rig.scene)
        self.main, self.reset = (rig.main_session, rig.reset)
        self.stacks, self.irq = (rig.stacks, rig.interrupt_runtime)
        self.video, self.edges = (rig.video_events, rig.edge_schedule)
        self.sound, self.schedule = (rig.sound, rig.hardware_schedule)
        self._thread = threading.get_ident()
        self.failed = False
        self.events = []
        self._input = None
        current, seen = (self.state.hardware, set())
        while current is not None and id(current) not in seen:
            if type(current) is SceneControllerHardwareBus:
                if self._input is not None:
                    raise Boundary('multiple controller owners in the actual Scene chain')
                self._input = current
            seen.add(id(current))
            current = getattr(current, 'devices', None)
        self._owners = tuple(((owner, name, getattr(owner, name).__func__) for owner, name in ((self.reset, 'require_main_identity'), (self.reset, 'resume_main'), (self.reset, 'resume_device'), (self.main, 'resume_interrupt'), (self.main, 'resume_device'), (self.stacks, 'capture'), (self.stacks, 'accept_point'), (self.irq, 'deliver'), (self.video, 'set_bus_state'), (self.edges, 'progress'), (self.schedule, 'poll_bus_request'), (self.video, 'progress'))))
        self._live()

    def _live(self):
        if self.failed or threading.get_ident() != self._thread:
            raise Boundary('failed or foreign-thread integrated Scene driver')
        rig = self.rig.require_live()
        if rig.scene is not self.state or rig.main_session is not self.main or rig.reset is not self.reset or (rig.stacks is not self.stacks) or (rig.interrupt_runtime is not self.irq) or (rig.video_events is not self.video) or (rig.edge_schedule is not self.edges) or (rig.sound is not self.sound) or (rig.hardware_schedule is not self.schedule) or (rig.vdp is not self.video.controller) or (rig.memory is not self.video.controller.memory) or (type(self.main) is not PersistentCitySceneSession) or (type(self.reset) is not CityColdResetSession) or (type(self.stacks) is not BankedStackControl) or (self.stacks.state is not self.state) or (type(self.irq) is not OriginalInterruptRuntime) or (self.irq.state is not self.state) or (type(self.video) is not SuppliedVideoEvents) or (self.video.state is not self.state) or (type(self.edges) is not FiniteVideoEdgeSchedule) or (self.edges.video_events is not self.video) or (not _chain_member(self.state, self.edges)) or (type(self.sound) is not SoundDevice) or (self.sound.scene is not self.state) or (self.sound.schedule is not self.schedule) or (not isinstance(self.schedule, FinitePulseSoundSchedule)) or (self.schedule.owner is not rig.control) or (self.schedule.poll_bus_request.__func__ is not FinitePulseSoundSchedule.poll_bus_request) or (self._input is None) or (self._input.ports is not rig.pads) or (not _chain_member(self.state, self._input)):
            raise Boundary('integrated Scene devices/main/reset/source ownership changed')
        if any((getattr(owner, name).__func__ is not original for owner, name, original in self._owners)):
            raise Boundary('an admitted integrated event owner was rebound')
        self.video._checked_controller(self.video.controller)
        waiting = self.main.waiting
        self.reset.require_main_identity(self.main, waiting)
        if type(waiting) not in WAIT_TYPES or waiting.state is not self.state or self.reset.waiting is not waiting or (rig.main_waiting is not waiting):
            raise Boundary('exact same-Scene reset/main/rig wait mirrors required')
        return waiting.validate()

    @property
    def waiting(self):
        return self._live()

    def _accept_wait(self, waiting):
        if waiting is not self.main.waiting or waiting is not self.reset.waiting:
            raise Boundary('actual reset resume did not publish the same main wait')
        self.rig.main_waiting = waiting
        return self._live()

    def step_irq(self, request: InterruptRequest, *, bus_state: VideoBusState, pad_changes: tuple[PhysicalPadSnapshot, ...]):
        """Supply one real external assertion, physical pins and bus snapshot.

        Every argument is explicit. The interrupt owner constructs the actual
        exception stack and original481E handler/4856 RTE; only its returned
        frame can resume the reset/main. A masked request does not resume it.
        """
        before = self._live()
        if type(before) is GameplaySceneWait and (not before.needs_interrupt):
            raise Boundary('actual suspended scene point requires its named device event, not IRQ')
        if type(request) is not InterruptRequest or type(bus_state) is not VideoBusState:
            raise ValueError('explicit original IRQ request and complete video bus snapshot required')
        if type(pad_changes) is not tuple or any((type(row) is not PhysicalPadSnapshot for row in pad_changes)) or len({row.port for row in pad_changes}) != len(pad_changes):
            raise ValueError('finite unique explicit physical pad changes required')
        for row in pad_changes:
            if row.port >= len(self.rig.pads) or type(self.rig.pads[row.port]) is not ThreeButtonPad:
                raise Boundary('physical snapshot names an unconnected or unsupported pad owner')
        narrative_resume_result = None
        try:
            for row in pad_changes:
                self.rig.pads[row.port].set_buttons(row.buttons)
            self.video.set_bus_state(bus_state)
            point = self.stacks.capture(before.poll, before.frame)
            result = self.irq.deliver(point, request)
            if not result.accepted:
                self.events.append(('masked_IRQ', request.level, before.poll))
                return IntegratedInterruptStep(result, self._live())
            self.stacks.accept_point(result.point)
            narrative_resume_result = result
            waiting = self.reset.resume_main(result.point.frame, result.point.pc)
            waiting = self._accept_wait(waiting)
            self.events.append(('actual_IRQ_RTE', request.level, before.poll, result.point.pc, waiting.poll))
            return IntegratedInterruptStep(result, waiting)
        except BaseException as _intro_error:
            if getattr(self, '_ordered_restart_owner', None) is not None:
                from ..high_level_main_flows.intro_irq_program import OriginalIntroResetJump
                from ..high_level_scene_flows.narrative_reset import OriginalNarrativeResetJump
                if type(_intro_error) in (OriginalIntroResetJump, OriginalNarrativeResetJump):
                    from ..reconstructed_game.ordered_restart import handle_ordered_restart_transfer
                    return handle_ordered_restart_transfer(self, before, request,
                        narrative_resume_result, _intro_error)
            if getattr(self, '_narrative_restart_owner', None) is not None:
                from ..high_level_scene_flows.narrative_reset import OriginalNarrativeResetJump
                if type(_intro_error) is OriginalNarrativeResetJump:
                    from ..reconstructed_game.narrative_restart import handle_original_narrative_transfer
                    return handle_original_narrative_transfer(self, before, request,
                        narrative_resume_result, _intro_error)
            if getattr(self, '_intro_restart_owner', None) is not None:
                from ..reconstructed_game.intro_restart import handle_original_intro_transfer
                return handle_original_intro_transfer(self, before, request, _intro_error)
            self.failed = True
            raise

    def step_device(self, event: str):
        """Consume one existing finite device event, then reread original MMIO.

        This never invokes resume_device first and never writes an ACK/phase.
        Out-of-order/exhausted/unsupported supplies retain their real Boundary.
        A partially advanced failure cannot be retried through this driver.
        """
        before = self._live()
        if type(before) is not GameplaySceneWait or before.needs_interrupt or event not in DEVICE_EVENTS or (event != before.event):
            raise Boundary('exact original suspended device wait and its named event required')
        try:
            if event in ('vblank-end', 'vblank-start'):
                self.edges.progress(self.state, event)
            elif event == 'sound-bus-acquire':
                self.schedule.poll_bus_request(self.sound)
            elif event == 'vdp-dma':
                self.video.progress(self.state, event, self.video.controller)
            waiting = self.reset.resume_device(event)
            waiting = self._accept_wait(waiting)
            self.events.append(('actual_device_progress', event, before.poll, waiting.poll))
            return waiting
        except BaseException:
            self.failed = True
            raise
