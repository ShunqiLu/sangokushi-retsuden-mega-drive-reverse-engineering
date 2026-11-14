"""Finite host-frame coordination over eight actual recovered wait types.

This is not an original-game PC dispatcher or an autonomous console clock.
Every IRQ, chip-clock extent, audio-step budget and IM1 formula is declared.
Existing finite hardware suppliers remain the only device progress owners.
"""
from dataclasses import dataclass, replace
import threading

from .config import (VideoSnapshot, PadSnapshot, _object, _integer, _list,
    _word_or_none, _pad, ConfigurationError)


def _wait_types():
    """Import the closed eight exact runtime types only after construction."""
    from ..high_level_main_flows.bootstrap_steps import BootstrapMainWait
    from ..high_level_main_flows.controller_setup_steps import ControllerSetupWait
    from ..high_level_main_flows.force_turn_steps import ForceTurnWait
    from ..high_level_gameplay_flow.scene_load_steps import GameplaySceneWait
    from ..high_level_scene_flows.scripted_scene_steps import ScriptedSceneWait
    from ..high_level_scene_flows.duel_scene_steps import DuelSceneWait
    from ..high_level_dynamic_flows.allocation_steps import AllocationSceneWait
    from ..high_level_gameplay_flow.battle_trigger_steps import BattleTriggerWait
    return (BootstrapMainWait, ControllerSetupWait, ForceTurnWait, GameplaySceneWait, ScriptedSceneWait, AllocationSceneWait, DuelSceneWait, BattleTriggerWait)


@dataclass(frozen=True)
class Im1Plan:
    clock_hz: int
    first_timestamp: int
    timestamp_step: int

    def __post_init__(self):
        _integer(self.clock_hz, 'frame_plan.audio.im1.clock_hz', 1)
        _integer(self.first_timestamp, 'frame_plan.audio.im1.first_timestamp', 0)
        _integer(self.timestamp_step, 'frame_plan.audio.im1.timestamp_step', 1)


@dataclass(frozen=True)
class AudioFramePlan:
    fm_ticks: int
    psg_input_clocks: int
    max_software_steps: int
    im1: Im1Plan | None

    def __post_init__(self):
        _integer(self.fm_ticks, 'frame_plan.audio.fm_ticks', 0)
        _integer(self.psg_input_clocks, 'frame_plan.audio.psg_input_clocks', 0)
        _integer(self.max_software_steps, 'frame_plan.audio.max_software_steps', 1)
        if self.im1 is not None and type(self.im1) is not Im1Plan:
            raise ConfigurationError('frame_plan.audio.im1 必须明确为 null 或完整时间戳计划。')

    def tick(self, ordinal):
        from .audio_tick import AudioTickSpec
        from ..high_level_audio_engine.driver_startup import Im1ClockGrant
        _integer(ordinal, 'frame_plan frame ordinal', 1)
        grant = None if self.im1 is None else Im1ClockGrant(
            self.im1.first_timestamp + (ordinal - 1) * self.im1.timestamp_step, self.im1.clock_hz)
        return AudioTickSpec(self.fm_ticks, self.psg_input_clocks, grant, self.max_software_steps)


@dataclass(frozen=True)
class FramePlanSpec:
    max_frames: int
    max_device_steps_per_frame: int
    irq_level: int
    video: VideoSnapshot
    pad_changes: tuple[PadSnapshot, ...]
    live_pad_ports: tuple[int, ...]
    audio: AudioFramePlan

    def __post_init__(self):
        _integer(self.max_frames, 'frame_plan.max_frames', 1)
        _integer(self.max_device_steps_per_frame, 'frame_plan.max_device_steps_per_frame', 0)
        if self.irq_level not in (4, 6) or type(self.irq_level) is not int:
            raise ConfigurationError('frame_plan.irq_level 必须显式是原 level4 或 level6。')
        if type(self.video) is not VideoSnapshot:
            raise ConfigurationError('frame_plan.video 必须是完整显式观察。')
        status = _integer(self.video.status_without_dma, 'frame_plan.video.status_without_dma', 0, 65535)
        if status & 2:
            raise ConfigurationError('frame_plan.video 不能外供真实 VDP owner 的 DMA busy 位。')
        _word_or_none(self.video.hv, 'frame_plan.video.hv')
        _word_or_none(self.video.open_bus, 'frame_plan.video.open_bus')
        if type(self.pad_changes) is not tuple or any(type(row) is not PadSnapshot for row in self.pad_changes):
            raise ConfigurationError('frame_plan.pad_changes 必须是有限物理端口快照。')
        if len({row.port for row in self.pad_changes}) != len(self.pad_changes):
            raise ConfigurationError('frame_plan.pad_changes 不能重复指定端口。')
        if type(self.live_pad_ports) is not tuple or len(set(self.live_pad_ports)) != len(self.live_pad_ports):
            raise ConfigurationError('frame_plan.live_pad_ports 必须是明确不重复的端口列表。')
        for port in self.live_pad_ports:
            _integer(port, 'frame_plan.live_pad_ports', 0, 2)
        if type(self.audio) is not AudioFramePlan:
            raise ConfigurationError('frame_plan.audio 必须完整声明，不默认生成时钟。')


def parse_frame_plan(value):
    """Configuration-only parser; no Scene, device or application is created."""
    context = 'frontend.frame_plan'
    row = _object(value, ('max_frames', 'max_device_steps_per_frame', 'irq_level',
        'video', 'pad_changes', 'live_pad_ports', 'audio'), context)
    video = _object(row['video'], ('status_without_dma', 'hv', 'open_bus'), context + '.video')
    snapshot = VideoSnapshot(_integer(video['status_without_dma'], context + '.video.status_without_dma', 0, 65535),
        _word_or_none(video['hv'], context + '.video.hv'),
        _word_or_none(video['open_bus'], context + '.video.open_bus'))
    pads = tuple(_pad(item, context + f'.pad_changes[{index}]')
        for index, item in enumerate(_list(row['pad_changes'], context + '.pad_changes')))
    ports = tuple(_integer(port, context + '.live_pad_ports', 0, 2)
        for port in _list(row['live_pad_ports'], context + '.live_pad_ports'))
    audio = _object(row['audio'], ('fm_ticks', 'psg_input_clocks', 'max_software_steps', 'im1'), context + '.audio')
    im1 = None
    if audio['im1'] is not None:
        item = _object(audio['im1'], ('clock_hz', 'first_timestamp', 'timestamp_step'), context + '.audio.im1')
        im1 = Im1Plan(item['clock_hz'], item['first_timestamp'], item['timestamp_step'])
    return FramePlanSpec(row['max_frames'], row['max_device_steps_per_frame'], row['irq_level'],
        snapshot, pads, ports, AudioFramePlan(audio['fm_ticks'], audio['psg_input_clocks'],
            audio['max_software_steps'], im1))


class FramePlanBoundary(ValueError):
    """Finite host budget/typed-wait boundary, not a fabricated game result."""


@dataclass(frozen=True)
class FramePlanStep:
    frame_number: int
    device_events: tuple[str, ...]
    irq_accepted: bool
    audio_tick: object


class FiniteFramePlan:
    """One finite declared plan; failure/exhaustion cannot recreate its prefix."""
    def __init__(self, app, spec: FramePlanSpec):
        from .application import GameApplication
        if type(app) is not GameApplication or type(spec) is not FramePlanSpec:
            raise ValueError('exact application owner and explicit FramePlanSpec required')
        self.app, self.spec = app, spec
        self.wait_types = _wait_types()
        self.device_wait_type = self.wait_types[3]
        self.thread = threading.get_ident()
        self.frames_completed = 0
        self.failed = False
        self.last_receipt = None
        self.limit_extensions = []

    @property
    def exhausted(self):
        return self.frames_completed >= self.spec.max_frames

    def extend_max_frames(self, new_max_frames):
        """Explicitly extend only a successfully exhausted live plan.

        Keep the absolute frame ordinal and original audio timestamp formula.
        This supplies no event now and does not refill hardware/PCM budgets.
        A partially failed frame, closed application or foreign thread cannot
        be revived by changing a host frame limit.
        """
        if self.failed or threading.get_ident() != self.thread:
            raise FramePlanBoundary('failed or foreign-thread frame plan cannot be extended')
        _integer(new_max_frames, 'explicit extended total frame limit', self.spec.max_frames + 1)
        if (self.frames_completed != self.spec.max_frames or self.last_receipt is None
                or self.last_receipt.get('frame') != self.frames_completed
                or self.last_receipt.get('audio_tick_completed') is not True):
            raise FramePlanBoundary('only a completely successful exhausted frame plan can be extended')
        self.app._live()
        self.app.audio._require_owned()
        self._waiting()
        previous = self.spec.max_frames
        self.spec = replace(self.spec, max_frames=new_max_frames)
        self.limit_extensions.append(dict(after_completed_frame=self.frames_completed,
            previous_max_frames=previous, explicitly_declared_max_frames=new_max_frames))
        return self.spec

    def _waiting(self):
        waiting = self.app.waiting
        if type(waiting) not in self.wait_types:
            raise FramePlanBoundary('unknown actual wait type; no guessed IRQ/device continuation')
        return waiting.validate()

    def _device_waits(self, consumed):
        while True:
            waiting = self._waiting()
            if type(waiting) is not self.device_wait_type or waiting.needs_interrupt:
                return waiting
            if len(consumed) >= self.spec.max_device_steps_per_frame:
                raise FramePlanBoundary('explicit maximum device steps exhausted in frame '
                    + str(self.frames_completed + 1) + '; actual wait ' + waiting.event)
            # IntegratedSceneDriver first consumes the existing finite edge or
            # BUSREQ supplier, then reset.resume_device rereads original MMIO.
            self.app.step_device(waiting.event)
            consumed.append(waiting.event)

    def _physical_changes(self, changes):
        from ..high_level_video.integrated_scene_driver import PhysicalPadSnapshot
        if type(changes) is not tuple or any(type(row) is not PhysicalPadSnapshot for row in changes):
            raise ValueError('one explicit finite physical pad snapshot tuple required')
        if len({row.port for row in changes}) != len(changes):
            raise ValueError('duplicate physical port in a frame plan step')
        supplied = {row.port: row for row in changes}
        expected = {row.port for row in self.spec.pad_changes} | set(self.spec.live_pad_ports)
        if set(supplied) != expected:
            raise ValueError('frame step may supply only and all its explicitly declared physical ports')
        for row in self.spec.pad_changes:
            if row.port not in self.spec.live_pad_ports:
                actual = supplied[row.port].buttons
                pressed = {name for name in actual.__dataclass_fields__ if getattr(actual, name)}
                if pressed != set(row.buttons):
                    raise ValueError('a fixed physical snapshot cannot be overridden by live input')
        return changes

    def step(self, *, pad_changes):
        from ..high_level_video.frame_interrupts import VideoBusState, InterruptRequest
        if self.failed or threading.get_ident() != self.thread:
            raise FramePlanBoundary('failed or foreign-thread finite frame plan')
        if self.exhausted:
            raise FramePlanBoundary('explicit finite maximum frame count exhausted; no automatic extension')
        pad_changes = self._physical_changes(pad_changes)
        consumed = []
        ordinal = self.frames_completed + 1
        accepted = False
        try:
            self._device_waits(consumed)
            result = self.app.step_irq(InterruptRequest(self.spec.irq_level),
                bus_state=VideoBusState(self.spec.video.status_without_dma,
                    self.spec.video.hv, self.spec.video.open_bus), pad_changes=pad_changes)
            accepted = result.interrupt.accepted
            self._device_waits(consumed)
            audio = self.app.advance_audio_tick(self.spec.audio.tick(ordinal))
            self.frames_completed = ordinal
            self.last_receipt = dict(frame=ordinal, device_events=tuple(consumed),
                IRQ_accepted=accepted, audio_tick_completed=True)
            return FramePlanStep(ordinal, tuple(consumed), accepted, audio)
        except BaseException as error:
            self.failed = True
            self.last_receipt = dict(frame=ordinal, device_events=tuple(consumed),
                IRQ_accepted=accepted, audio_tick_completed=False, boundary=str(error))
            error.add_note('Finite frame plan stopped at frame ' + str(ordinal)
                + ', consumed device events=' + str(tuple(consumed)) + '; no prefix replay or supply extension')
            raise
