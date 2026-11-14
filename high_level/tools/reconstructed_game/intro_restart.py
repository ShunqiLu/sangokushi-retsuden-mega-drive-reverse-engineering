"""Finite same-application warm reset after the original4786 JMP206.

All hardware remains live. Only terminated software lifetimes are replaced
by the new original206/300/driver invocations that the game actually requests.
No old prefix is replayed to manufacture a continuation or a successful RTE.
"""
from dataclasses import dataclass
import threading

from ..high_level_main_flows.bootstrap_steps import BootstrapMainWait
from ..high_level_main_flows.city_cold_reset import CityColdResetSession
from ..high_level_main_flows.city_scene_steps import PersistentCitySceneSession
from ..high_level_main_flows.intro_irq_program import (
    IntroIrqPrograms, OriginalIntroResetJump, bind_intro_irq)
from ..high_level_audio_engine.warm_driver_installation import (
    RetainedAudioCarriers, WarmDriverInstallationCapture, DriverInstalledAuthority)
from ..high_level_audio_engine.driver_startup import AudioDriverStartupSession, Im1ClockGrant
from ..high_level_audio_engine.control_reset import FinitePulseSoundSchedule
from ..high_level_video.integrated_scene_driver import IntegratedSceneDriver, IntegratedInterruptStep
from ..high_level_scene_flows.domain import Boundary
from .audio import OwnedGameAudio


@dataclass(frozen=True)
class IntroRestartSpec:
    """One caller-declared reset supply, not automatic timing or refill.

    The three IM1 timestamps are explicitly specified positive offsets from
    the retired actual driver IRQ clock, in this declared clock frequency.
    They must also fit before the caller's next normal audio tick timestamp.
    No relationship with FM/PSG clocks or video frame time is inferred.
    """
    reset_pulse_clocks: tuple[int, int]
    irq_clock_hz: int
    startup_im1_offsets: tuple[int, int, int]

    def __post_init__(self):
        if (type(self.reset_pulse_clocks) is not tuple or len(self.reset_pulse_clocks) != 2
                or any(type(value) is not int or value < 3 for value in self.reset_pulse_clocks)):
            raise ValueError('two explicit finite RESET pulse clock grants of at least3 required')
        if type(self.irq_clock_hz) is not int or self.irq_clock_hz <= 0:
            raise ValueError('explicit matching positive driver IRQ frequency required')
        if (type(self.startup_im1_offsets) is not tuple or len(self.startup_im1_offsets) != 3
                or any(type(value) is not int or value <= 0 for value in self.startup_im1_offsets)
                or any(left >= right for left, right in zip(self.startup_im1_offsets, self.startup_im1_offsets[1:]))):
            raise ValueError('three explicit strictly increasing positive startup IM1 offsets required')


@dataclass(frozen=True)
class AcceptedIntroResetInterrupt:
    """Actual IRQ accepted, but abandoned by the game's JMP rather than RTE."""
    accepted: bool
    vector_address: int
    handler: int
    reset_source: int
    reset_target: int
    RTE_performed: bool


class OriginalIntroRestartOwner:
    """A finite explicit application owner for original intro-reset transfers."""
    def __init__(self, app, *, plans):
        from .application import GameApplication
        if type(app) is not GameApplication:
            raise ValueError('one exact actual GameApplication required')
        app._live()
        if (type(plans) is not tuple or not plans
                or any(type(plan) is not IntroRestartSpec for plan in plans)):
            raise ValueError('explicit finite nonempty exact restart-plan tuple required')
        if getattr(app, 'intro_restarts', None) is not None:
            raise Boundary('an existing application restart owner cannot be replaced')
        if type(app.audio) is not OwnedGameAudio or type(app.scene_driver) is not IntegratedSceneDriver:
            raise Boundary('the actual cold-created audio and integrated Main owners required')
        app.audio._require_owned()
        schedule = app.rig.hardware_schedule
        if (not isinstance(schedule, FinitePulseSoundSchedule) or schedule.owner is not app.rig.control
                or schedule._pulse is not None or schedule._pulse_index != len(schedule.reset_pulse_clocks)
                or any(plan.irq_clock_hz != app.audio._loop.irq_clock_hz for plan in plans)):
            raise Boundary('completed cold pulse phase and matching explicit future driver IRQ profile required')
        if getattr(app.scene_driver, '_intro_restart_owner', None) is not None:
            raise Boundary('the actual integrated driver already has a transfer owner')
        self.app, self.rig, self.state = app, app.rig, app.rig.scene
        self.thread, self.active, self.failed = threading.get_ident(), False, False
        self.plans, self.consumed, self.events = plans, 0, []
        self.driver = app.scene_driver
        self.programs = IntroIrqPrograms(self.state)
        self.schedule = schedule
        self.pulse_start = schedule._pulse_index
        self.pulses = schedule.reset_pulse_clocks + tuple(
            value for plan in plans for value in plan.reset_pulse_clocks)
        # This publishes only the finite supply the caller just provided.
        # It does not assert RESET, consume a pulse, advance a chip or grant ACK.
        schedule.reset_pulse_clocks = self.pulses
        bind_intro_irq(self.rig.interrupt_runtime, self.programs)
        self.driver._intro_restart_owner = self
        app.intro_restarts = self

    def _guard(self, driver):
        if (self.failed or self.active or threading.get_ident() != self.thread
                or self.app.closed or self.app.failed or self.app.rig is not self.rig
                or self.app.scene_driver is not driver or driver is not self.driver
                or driver.rig is not self.rig or driver.state is not self.state
                or self.rig.hardware_schedule is not self.schedule
                or self.schedule.reset_pulse_clocks is not self.pulses
                or getattr(driver, '_intro_restart_owner', None) is not self
                or getattr(self.rig.interrupt_runtime, '_intro_reset_owner', None) is not self.programs):
            raise Boundary('same active application/source/device restart ownership required')
        self.programs._guard()

    def complete_transfer(self, driver, before, jump, request):
        self._guard(driver)
        if (type(jump) is not OriginalIntroResetJump or jump.owner is not self.programs
                or request.level != 6 or type(before) is not BootstrapMainWait or before.poll != 0x3BC
                or before is not driver.main.waiting or before is not driver.reset.waiting
                or type(driver.main) is not PersistentCitySceneSession
                or type(driver.reset) is not CityColdResetSession):
            raise Boundary('exact original intro JMP from the actual suspended main3BC required')
        if self.consumed == len(self.plans):
            raise Boundary('explicit finite original-intro restart supply exhausted')
        plan = self.plans[self.consumed]
        if self.schedule._pulse_index != self.pulse_start + 2 * self.consumed:
            raise Boundary('unexpected intervening reset consumed this declared warm supply')
        frame = self.programs.claim(jump)
        old_main, old_reset, old_audio = driver.main, driver.reset, self.app.audio
        old_main._require_current()
        if old_main._program.gi_running or old_main._failed:
            raise Boundary('old actual main must still be suspended, never re-entered')
        self.active = True
        startup = audio = None
        self.last_reset = self.last_capture = None
        try:
            retired = RetainedAudioCarriers.retire(old_audio)
            # Lifecycle invalidation does not touch game RAM, SR, saved slots,
            # hardware or old IRQ contents. Original300 itself later sets A7.
            sr = self.state.sr
            old_main._program.close()
            old_main._failed = True
            old_reset.failed = True
            driver.failed = True
            if self.state.sr != sr:
                raise Boundary('abandoning the old main may not alter original software SR')
            reset = CityColdResetSession(self.state, frame, old_reset.profile)
            self.last_reset = reset
            capture = WarmDriverInstallationCapture(self.rig.sound, self.rig.control,
                self.rig.source, reset_session=reset, retirement=retired, jump=jump)
            self.last_capture = capture
            waiting = reset.start()
            if type(waiting) is not BootstrapMainWait or waiting.poll != 0x3BC:
                raise Boundary('actual reentry chose cold audio-release work; explicit cold authority is required')
            installation = capture.finish(waiting)
            authority = DriverInstalledAuthority(installation, retired.frame)
            lease = self.rig.control.acquire_frame('driver', 0, authority=authority)
            startup = AudioDriverStartupSession(self.rig.sound, self.rig.control, lease,
                irq_clock_hz=plan.irq_clock_hz, initial_irq_clock=retired.irq_clock,
                main_loop_points=True, timer_b_continuation=True)
            point = startup.start()
            for offset in plan.startup_im1_offsets:
                if point.pc != 0x005F:
                    raise Boundary('new actual driver countdown did not request the next supplied IM1')
                point = startup.deliver_im1(Im1ClockGrant(retired.irq_clock + offset, plan.irq_clock_hz))
            if point.pc != 0x006F or startup.ready_lease is None:
                raise Boundary('the actual three supplied startup IM1s did not reach original006F')
            if self.schedule._pulse_index != self.pulse_start + 2 * (self.consumed + 1):
                raise Boundary('original warm300 did not consume exactly its declared two reset pulses')
            # Commit only actual new software owners. All device/source objects,
            # root resource finally and the original retained parent stay live.
            self.rig.reset, self.rig.main_session, self.rig.main_waiting = reset, reset.main_session, waiting
            self.rig.startup, self.rig.audio_point = startup, point
            self.rig.stacks.capture(waiting.poll, waiting.frame)
            audio = OwnedGameAudio(self.rig)
            next_driver = IntegratedSceneDriver(self.rig)
            next_driver._intro_restart_owner = self
            self.app.audio, self.app.scene_driver, self.driver = audio, next_driver, next_driver
            self.consumed += 1
            evidence = dict(source_pc=jump.source_pc, target=jump.target,
                actual_entry_SP=frame.stack_cursor.base, actual_entry_SR=jump.full_sr,
                actual_new_Main_SP=waiting.frame.stack_cursor.base,
                discarded_old_IRQ_without_RTE=True, cold_workspace_replayed=False,
                old_epoch=retired.reset_epoch, new_epoch=self.rig.sound.reset_epoch,
                actual_copy_BYTE_writes=installation.evidence['actual_BYTE_writes'],
                actual_source_union=installation.evidence['source_union_bytes'],
                original_startup_IM1_timestamps=[retired.irq_clock + value for value in plan.startup_im1_offsets],
                same_Scene_RAM_FM_PSG_source_save_and_PCM=True,
                finite_restart_ordinal=self.consumed, remaining_restart_plans=len(self.plans)-self.consumed)
            self.events.append(evidence)
            self.rig.source_contract.setdefault('actual_original_intro_restarts', []).append(evidence)
            interrupt = AcceptedIntroResetInterrupt(True, 0x78, 0x481E, 0x4786, 0x206, False)
            return IntegratedInterruptStep(interrupt, waiting)
        except BaseException as error:
            self.failed = True
            # Keep partial real state/effects. Only release software claims that
            # this actual attempt acquired; never replay or fabricate readiness.
            try:
                if audio is not None and not audio.closed:
                    audio.close()
                elif startup is not None and not startup.closed:
                    startup.close()
            except BaseException as cleanup:
                error.add_note('Actual new warm-start software cleanup: ' + str(cleanup))
            self.events.append(dict(status='actual_restart_boundary', error_type=type(error).__name__,
                error=str(error), reset_phase=None if self.last_reset is None else self.last_reset.phase,
                actual_reset_epoch=self.rig.sound.reset_epoch,
                new_copies_proved=self.last_capture is not None and self.last_capture.finished))
            raise
        finally:
            self.active = False

    def diagnostics(self):
        """Compact lifecycle observations only, including failed attempts."""
        if threading.get_ident() != self.thread:
            raise Boundary('restart diagnostics belong to the actual application thread')
        return dict(failed=self.failed, active=self.active, completed=self.consumed,
            remaining=len(self.plans)-self.consumed, actual_jumps=self.programs.jumps,
            consumed_reset_pulses=self.schedule._pulse_index-self.pulse_start,
            declared_reset_pulses=len(self.pulses)-self.pulse_start,
            last_event=None if not self.events else self.events[-1],
            original_game_bug_fixes=0, runtime_acceptance_claimed=False)


def handle_original_intro_transfer(driver, before, request, error):
    """Called only from the existing exception handler, never on Boundary re-entry."""
    owner = getattr(driver, '_intro_restart_owner', None)
    if type(error) is not OriginalIntroResetJump or type(owner) is not OriginalIntroRestartOwner:
        driver.failed = True
        raise error
    try:
        return owner.complete_transfer(driver, before, error, request)
    except BaseException:
        driver.failed = True
        raise


def enable_intro_restarts(app, *, plans):
    """Opt in once, before a new input run; every pulse/IRQ plan is explicit."""
    return OriginalIntroRestartOwner(app, plans=plans)
