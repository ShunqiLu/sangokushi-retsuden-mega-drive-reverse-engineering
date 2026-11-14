"""Finite narrative Main→206 warm reset on the same actual application.

An accepted IRQ has really RTE'd before the old Main executes its terminal
narrative jump. This owner does not weaken the distinct intro-IRQ contract.
"""
import threading
from types import GeneratorType

from ..high_level_main_flows.bootstrap_steps import BootstrapMainWait
from ..high_level_main_flows.city_cold_reset import CityColdResetSession
from ..high_level_main_flows.city_scene_steps import PersistentCitySceneSession
from ..high_level_scene_flows.narrative_reset import OriginalNarrativeResetJump, NarrativeScenePrograms
from ..high_level_audio_engine.narrative_driver_installation import NarrativeWarmDriverInstallationCapture as WarmDriverInstallationCapture
from ..high_level_audio_engine.warm_driver_installation import RetainedAudioCarriers, DriverInstalledAuthority
from ..high_level_audio_engine.driver_startup import AudioDriverStartupSession, Im1ClockGrant
from ..high_level_audio_engine.control_reset import FinitePulseSoundSchedule
from ..high_level_video.integrated_scene_driver import IntegratedSceneDriver, IntegratedInterruptStep
from ..high_level_video.frame_interrupts import InterruptRequest, InterruptResult, ExecutionPoint
from ..high_level_gameplay_flow.scene_load_steps import GameplaySceneWait
from ..high_level_scene_flows.domain import Boundary
from .intro_restart import IntroRestartSpec
from .audio import OwnedGameAudio


NARRATIVE_RESET_SOURCES = (0x3BBBA, 0x3C6C4, 0x3CA92, 0x3CE00, 0x3D454)


class NarrativeRestartOwner:
    """One explicit finite restart supply; same devices, source, save and sinks."""

    def __init__(self, app, *, plans):
        from .application import GameApplication
        if type(app) is not GameApplication:
            raise ValueError('one exact actual GameApplication required')
        app._live()
        if (type(plans) is not tuple or not plans
                or any(type(plan) is not IntroRestartSpec for plan in plans)):
            raise ValueError('explicit finite nonempty exact restart-plan tuple required')
        if (getattr(app, 'intro_restarts', None) is not None
                or getattr(app, 'narrative_restarts', None) is not None
                or getattr(app.scene_driver, '_intro_restart_owner', None) is not None
                or getattr(app.scene_driver, '_narrative_restart_owner', None) is not None):
            raise Boundary('narrative supply is a separate scope, mutually exclusive with intro restart plans')
        if type(app.audio) is not OwnedGameAudio or type(app.scene_driver) is not IntegratedSceneDriver:
            raise Boundary('the actual cold-created audio and integrated Main owners required')
        app.audio._require_owned()
        schedule = app.rig.hardware_schedule
        if (not isinstance(schedule, FinitePulseSoundSchedule) or schedule.owner is not app.rig.control
                or schedule._pulse is not None or schedule._pulse_index != len(schedule.reset_pulse_clocks)
                or any(plan.irq_clock_hz != app.audio._loop.irq_clock_hz for plan in plans)):
            raise Boundary('completed cold pulse phase and matching explicit future driver IRQ profile required')
        self.app, self.rig, self.state = app, app.rig, app.rig.scene
        self.thread, self.active, self.failed = threading.get_ident(), False, False
        self.plans, self.consumed, self.events = plans, 0, []
        self.driver, self.schedule = app.scene_driver, schedule
        self.pulse_start = schedule._pulse_index
        self.pulses = schedule.reset_pulse_clocks + tuple(
            value for plan in plans for value in plan.reset_pulse_clocks)
        self.hardware, self.ram, self.data = self.state.hardware, self.state.ram, self.state.data
        self.source, self.save_image, self.save_backing = self.rig.source, app.config.save_image, app.config.save_image.backing
        self.sound, self.audio_state, self.control = self.rig.sound, self.rig.audio, self.rig.control
        self.fm, self.psg, self.memory = self.rig.fm, self.rig.psg, self.rig.memory
        self.outputs, self.fm_sink, self.psg_sink = app.outputs, self.rig.fm.pcm_sink, self.rig.psg.pcm_sink
        self.programs = None
        # Explicit publication of the caller's finite future supply is not
        # RESET assertion, a clock advance, a BUSACK grant or software work.
        schedule.reset_pulse_clocks = self.pulses
        self.driver._narrative_restart_owner = self
        app.narrative_restarts = self

    def _guard(self, driver):
        if (self.failed or self.active or threading.get_ident() != self.thread
                or self.app.closed or self.app.failed or self.app.rig is not self.rig
                or self.app.scene_driver is not driver or driver is not self.driver
                or driver.rig is not self.rig or driver.state is not self.state
                or self.rig.hardware_schedule is not self.schedule
                or self.schedule.reset_pulse_clocks is not self.pulses
                or getattr(driver, '_narrative_restart_owner', None) is not self
                or getattr(self.app, 'intro_restarts', None) is not None
                or self.state.hardware is not self.hardware or self.state.ram is not self.ram
                or self.state.data is not self.data or self.rig.source is not self.source
                or self.source.data is not self.data or self.app.config.save_image is not self.save_image
                or self.save_image.backing is not self.save_backing
                or self.rig.sound is not self.sound or self.rig.audio is not self.audio_state
                or self.rig.control is not self.control or self.rig.fm is not self.fm
                or self.rig.psg is not self.psg or self.rig.memory is not self.memory
                or self.app.outputs is not self.outputs or self.fm.pcm_sink is not self.fm_sink
                or self.psg.pcm_sink is not self.psg_sink):
            raise Boundary('same active narrative application/Scene/RAM/device/source/save/sink ownership required')
        self.rig.require_live()

    def _validate_transfer(self, driver, before, jump, request, accepted_irq_result):
        main, reset = driver.main, driver.reset
        if (type(jump) is not OriginalNarrativeResetJump or type(jump.owner) is not NarrativeScenePrograms
                or jump.state is not self.state or jump.source_pc not in NARRATIVE_RESET_SOURCES
                or jump.target != 0x206 or jump.full_sr != self.state.sr
                or jump.frame.status != self.state.sr & 31
                or type(before) is not GameplaySceneWait or before.poll != 0x83CC
                or not before.needs_interrupt or before.state is not self.state
                or type(main) is not PersistentCitySceneSession or type(reset) is not CityColdResetSession
                or main is not self.rig.main_session or reset is not self.rig.reset
                or before is not main.waiting or before is not reset.waiting or before is not self.rig.main_waiting
                or main is not reset.main_session or main.state is not self.state or reset.state is not self.state
                or type(main._program) is not GeneratorType or main._program.gi_running
                or main._program.gi_frame is not None or not main._failed
                or main._program.gi_code is not reset._main_code
                or reset.failed or reset.phase != 'original-main-tail'):
            raise Boundary('exact original narrative JMP after the terminated actual83CC Main invocation required')
        if (type(request) is not InterruptRequest or request.level != 6
                or type(accepted_irq_result) is not InterruptResult or not accepted_irq_result.accepted
                or accepted_irq_result.vector_address != 0x78 or accepted_irq_result.handler != 0x481E
                or type(accepted_irq_result.point) is not ExecutionPoint
                or accepted_irq_result.point.pc != before.poll
                or accepted_irq_result.point.frame.stack_cursor.base != before.frame.stack_cursor.base):
            raise Boundary('actual accepted level6 IRQ/RTE result must precede the narrative software jump')
        # The IRQ's returned CCR may since have changed in the actual story
        # exit instructions. Do not validate its historic frame against the
        # current jump SR or pretend that the jump itself was an IRQ/RTE.
        main._require_current()
        reset._guard()
        self.programs = jump.owner

    def complete_transfer(self, driver, before, jump, request, accepted_irq_result):
        self._guard(driver)
        self._validate_transfer(driver, before, jump, request, accepted_irq_result)
        if self.consumed == len(self.plans):
            raise Boundary('explicit finite original-intro restart supply exhausted')
        plan = self.plans[self.consumed]
        if self.schedule._pulse_index != self.pulse_start + 2 * self.consumed:
            raise Boundary('unexpected intervening reset consumed this declared warm supply')
        frame = self.programs.claim(jump)
        old_main, old_reset, old_audio = (driver.main, driver.reset, self.app.audio)
        old_main._require_current()
        if old_main._program.gi_running or not old_main._failed or old_main._program.gi_frame is not None:
            raise Boundary('old actual narrative main must already be terminated by this JMP')
        self.active = True
        startup = audio = None
        self.last_reset = self.last_capture = None
        try:
            retired = RetainedAudioCarriers.retire(old_audio)
            sr = self.state.sr
            old_main._program.close()
            old_main._failed = True
            old_reset.failed = True
            driver.failed = True
            if self.state.sr != sr:
                raise Boundary('abandoning the old main may not alter original software SR')
            reset = CityColdResetSession(self.state, frame, old_reset.profile)
            self.last_reset = reset
            capture = WarmDriverInstallationCapture(self.rig.sound, self.rig.control, self.rig.source, reset_session=reset, retirement=retired, jump=jump)
            self.last_capture = capture
            waiting = reset.start()
            if type(waiting) is not BootstrapMainWait or waiting.poll != 956:
                raise Boundary('actual reentry chose cold audio-release work; explicit cold authority is required')
            installation = capture.finish(waiting)
            authority = DriverInstalledAuthority(installation, retired.frame)
            lease = self.rig.control.acquire_frame('driver', 0, authority=authority)
            startup = AudioDriverStartupSession(self.rig.sound, self.rig.control, lease, irq_clock_hz=plan.irq_clock_hz, initial_irq_clock=retired.irq_clock, main_loop_points=True, timer_b_continuation=True)
            point = startup.start()
            for offset in plan.startup_im1_offsets:
                if point.pc != 95:
                    raise Boundary('new actual driver countdown did not request the next supplied IM1')
                point = startup.deliver_im1(Im1ClockGrant(retired.irq_clock + offset, plan.irq_clock_hz))
            if point.pc != 111 or startup.ready_lease is None:
                raise Boundary('the actual three supplied startup IM1s did not reach original006F')
            if self.schedule._pulse_index != self.pulse_start + 2 * (self.consumed + 1):
                raise Boundary('original warm300 did not consume exactly its declared two reset pulses')
            self.rig.reset, self.rig.main_session, self.rig.main_waiting = (reset, reset.main_session, waiting)
            self.rig.startup, self.rig.audio_point = (startup, point)
            self.rig.stacks.capture(waiting.poll, waiting.frame)
            audio = OwnedGameAudio(self.rig)
            next_driver = IntegratedSceneDriver(self.rig)
            next_driver._narrative_restart_owner = self
            self.app.audio, self.app.scene_driver, self.driver = (audio, next_driver, next_driver)
            self.consumed += 1
            evidence = dict(source_pc=jump.source_pc, target=jump.target, actual_entry_SP=frame.stack_cursor.base, actual_entry_SR=jump.full_sr, actual_new_Main_SP=waiting.frame.stack_cursor.base, IRQ_already_returned_before_narrative_JMP=True, cold_workspace_replayed=False, old_epoch=retired.reset_epoch, new_epoch=self.rig.sound.reset_epoch, actual_copy_BYTE_writes=installation.evidence['actual_BYTE_writes'], actual_source_union=installation.evidence['source_union_bytes'], original_startup_IM1_timestamps=[retired.irq_clock + value for value in plan.startup_im1_offsets], same_Scene_RAM_FM_PSG_source_save_and_PCM=True, finite_restart_ordinal=self.consumed, remaining_restart_plans=len(self.plans) - self.consumed)
            self.events.append(evidence)
            self.rig.source_contract.setdefault('actual_original_narrative_restarts', []).append(evidence)
            return IntegratedInterruptStep(accepted_irq_result, waiting)
        except BaseException as error:
            self.failed = True
            try:
                if audio is not None and (not audio.closed):
                    audio.close()
                elif startup is not None and (not startup.closed):
                    startup.close()
            except BaseException as cleanup:
                error.add_note('Actual new warm-start software cleanup: ' + str(cleanup))
            self.events.append(dict(status='actual_restart_boundary', error_type=type(error).__name__, error=str(error), reset_phase=None if self.last_reset is None else self.last_reset.phase, actual_reset_epoch=self.rig.sound.reset_epoch, new_copies_proved=self.last_capture is not None and self.last_capture.finished))
            raise
        finally:
            self.active = False

    def diagnostics(self):
        if threading.get_ident() != self.thread:
            raise Boundary('restart diagnostics belong to the actual application thread')
        return dict(failed=self.failed, active=self.active, completed=self.consumed,
            remaining=len(self.plans)-self.consumed,
            actual_jumps=0 if self.programs is None else self.programs.jumps,
            consumed_reset_pulses=self.schedule._pulse_index-self.pulse_start,
            declared_reset_pulses=len(self.pulses)-self.pulse_start,
            last_event=None if not self.events else self.events[-1],
            original_game_bug_fixes=0, runtime_acceptance_claimed=False)


def handle_original_narrative_transfer(driver, before, request, accepted_irq_result, error):
    """Only after true main.resume raised a typed jump, never a retry handler."""
    owner = getattr(driver, '_narrative_restart_owner', None)
    if type(error) is not OriginalNarrativeResetJump or type(owner) is not NarrativeRestartOwner:
        driver.failed = True
        raise error
    try:
        return owner.complete_transfer(driver, before, error, request, accepted_irq_result)
    except BaseException:
        driver.failed = True
        raise


def enable_narrative_restarts(app, *, plans):
    return NarrativeRestartOwner(app, plans=plans)
