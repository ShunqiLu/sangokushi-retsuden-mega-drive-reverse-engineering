"""One application lifetime over the restored cold/main/audio/video owners.

Business algorithms remain in their domain modules. This layer composes their
actual owners, exposes explicit event ports and closes them in ownership order.
It never supplies default input, clocks, IRQs, scene state or successful results.
"""
from contextlib import nullcontext
import threading
from pathlib import Path

from ..high_level_audio_engine.city_cold_driver import build_city_cold_driver
from ..high_level_video.integrated_scene_driver import IntegratedSceneDriver
from ..high_level_video.render import render_frame
from .audio import OwnedGameAudio
from .command_observation import observe_command_order_records
from .palette_observation import observe_palette_backings
from .pcm import PcmOutputs


class GameApplication:
    """One cold-created Scene with independent rendering and explicit events."""

    def __init__(self, config, rig, outputs):
        self.config, self.rig, self.outputs = config, rig, outputs
        self.scene_journal = None
        self.thread = threading.get_ident()
        self.closed = self.failed = False
        self.last_error = None
        self.scene_driver = IntegratedSceneDriver(rig)
        self.audio = OwnedGameAudio(rig)
        self.operations = 0

    @classmethod
    def open(cls, config, *, scene_journal_path=None):
        """Construct from declared sources, save backing and fresh PCM outputs."""
        outputs = PcmOutputs(config.pcm_output)
        rig = None
        journal = None
        try:
            event_scope = nullcontext()
            if scene_journal_path is not None:
                from ..high_level_main_flows.runtime import use_new_scene_event_log
                from .config import _fresh_build_path
                from .scene_journal import SceneEventJournal
                from .session_config import _no_reparse
                candidate = Path(scene_journal_path)
                if not candidate.is_absolute():
                    candidate = config.output.parent / candidate
                _no_reparse(candidate.absolute(), 'Scene event journal')
                journal_path = _fresh_build_path(str(scene_journal_path), config.output.parent,
                    config.project_root, 'Scene event journal')
                other_outputs = (config.output, config.frontend.diagnostics_directory,
                    config.pcm_output.fm_path, config.pcm_output.psg_path)
                if journal_path in other_outputs or not journal_path.parent.is_dir():
                    raise ValueError('The Scene event journal needs a separate file with an existing parent')
                journal = SceneEventJournal(journal_path)
                event_scope = use_new_scene_event_log(journal)
            with event_scope:
                if config.m68k_native_root is None:
                    rig = build_city_cold_driver(config.project_root, config.sound_native_root,
                        config.sources, config.audio_root, config.chip_library, config.inputs,
                        config.output, save_image=config.save_image,
                        fm_pcm_sink=outputs.fm_sink, psg_pcm_sink=outputs.psg_sink)
                else:
                    from ..high_level_audio_engine.high_level_city_cold_driver import build_high_level_city_cold_driver
                    rig = build_high_level_city_cold_driver(config.project_root, config.sound_native_root,
                        config.sources, config.audio_root, config.chip_library, config.inputs,
                        config.output, m68k_native_root=config.m68k_native_root,
                        save_image=config.save_image, fm_pcm_sink=outputs.fm_sink, psg_pcm_sink=outputs.psg_sink)
            outputs.require_rates(rig.fm, rig.psg)
            app = cls(config, rig, outputs)
            app.scene_journal = journal
            return app
        except BaseException as error:
            # Only close owners actually acquired; never host-clear their
            # control state or replay cold/reset in an attempt to recover.
            if rig is not None:
                try:
                    if not rig.startup.closed:
                        rig.startup.close()
                    rig.finish(outcome='application_open_boundary', evidence={'error': str(error)})
                except BaseException as cleanup:
                    error.add_note('Retained rig cleanup: ' + str(cleanup))
            try:
                outputs.close()
            except BaseException as cleanup:
                error.add_note('PCM output cleanup: ' + str(cleanup))
            if journal is not None:
                try:
                    journal.close()
                except BaseException as cleanup:
                    error.add_note('Scene event journal cleanup: ' + str(cleanup))
            raise

    def _live(self):
        if self.closed or self.failed or threading.get_ident() != self.thread:
            raise RuntimeError('application is closed, stopped at a boundary or used from another thread')
        self.rig.require_live()

    def _operation(self, action, *args, **kwargs):
        self._live()
        try:
            result = action(*args, **kwargs)
            self.operations += 1
            return result
        except BaseException as error:
            self.failed = True
            self.last_error = str(error)
            raise

    @property
    def waiting(self):
        self._live()
        return self.scene_driver.waiting

    def step_irq(self, request, *, bus_state, pad_changes):
        return self._operation(self.scene_driver.step_irq, request,
            bus_state=bus_state, pad_changes=pad_changes)

    def step_device(self, event):
        return self._operation(self.scene_driver.step_device, event)

    def advance_audio(self):
        return self._operation(self.audio.advance)

    def advance_audio_tick(self, spec):
        """Coordinate a finite caller-declared tick through the actual owner."""
        from .audio_tick import execute_audio_tick
        return self._operation(execute_audio_tick, self.audio, spec)

    def deliver_im1(self, grant):
        return self._operation(self.audio.deliver_im1, grant)

    def advance_chips(self, *, fm_ticks, psg_input_clocks):
        return self._operation(self.audio.advance_chips,
            fm_ticks=fm_ticks, psg_input_clocks=psg_input_clocks)

    def render(self):
        """Read actual live VDP memory; no reference screen or placeholder UI."""
        if self.closed or threading.get_ident() != self.thread:
            raise RuntimeError('render requires the retained application owner thread')
        return render_frame(self.rig.memory)

    def export_save(self, destination):
        """Export actual live8192 bytes exclusively, never overwrite the input."""
        self._live()
        path = Path(destination).resolve()
        if not path.is_relative_to(self.config.project_root / 'build') or not path.parent.is_dir():
            raise ValueError('a new explicit save export inside the project build directory is required')
        with path.open('xb') as stream:
            stream.write(self.config.save_image.backing)
        return path

    def observe(self):
        """Read a fixed small live-state view without advancing software/devices.

        Raw WORDs identify the actual same-App RAM, not an inferred menu or
        a restart checkpoint. No Scene.read, renderer, bus or clock is used.
        """
        self._live()
        ram = self.rig.scene.ram
        if type(ram) is not bytearray or len(ram) != 65536:
            raise ValueError('the current application must retain its actual64KiB Scene RAM')
        addresses = (0xF612, 0xF600, 0xF352, 0xF362, 0xF36C,
            0xF376, 0xF380, 0xF386, 0xF578, 0xF650,
            0xF67A, 0xF67C, 0xF67E, 0xCEA0, 0xCEAC, 0xAFFE,
            0x80C4, 0x842A, 0x842E, 0xF32C, 0xF32E, 0xF602, 0xF776,
            0xF364, 0xF392, 0xF3A6, 0xF39E, 0xF3A0,
            0xF39A, 0xF3F4, 0xF3F6, 0xF3F8, 0xF3FA, 0xF3FC, 0xF3A4)
        return dict(source='actual_current_same_App_RAM_and_wait_owner',
            main_poll=None if self.rig.main_waiting is None else self.rig.main_waiting.poll,
            main_suspensions=self.rig.main_session.suspensions,
            operations=self.operations,
            scene_status_word=self.rig.scene.sr,
            RAM_WORDs={format(address, '04X'): int.from_bytes(ram[address:address + 2], 'big')
                for address in addresses},
            command_order_observation=observe_command_order_records(ram),
            software_device_or_clock_advanced=False, Scene_DATA_read_performed=False,
            state_or_capacity_modified=False, cross_thread_atomic_snapshot_claimed=False)

    def observe_palette(self):
        """Read fixed same-App CRAM/RAM/register backings on the live owner thread.

        No operation wrapper, Scene DATA read, bus, rendering, clock or device
        action is entered. Poll and owner counters are raw current fields, not
        a CPU snapshot or an inference about earlier palette modes.
        """
        self._live()
        observation = observe_palette_backings(self.rig.memory.cram,
            self.rig.memory.registers, self.rig.scene.ram)
        observation.update(
            main_poll=None if self.rig.main_waiting is None else self.rig.main_waiting.poll,
            main_suspensions=self.rig.main_session.suspensions,
            operations=self.operations, scene_status_word=self.rig.scene.sr)
        return observation

    def diagnostics(self):
        """Small observations, not multi-million-event or RAM/asset snapshots."""
        intro_restarts = getattr(self, 'intro_restarts', None)
        narrative_restarts = getattr(self, 'narrative_restarts', None)
        ordered_restarts = getattr(self, 'ordered_restarts', None)
        return dict(closed=self.closed, stopped_at_boundary=self.failed,
            last_error=self.last_error, operations=self.operations,
            main_suspensions=self.rig.main_session.suspensions,
            main_poll=None if self.rig.main_waiting is None else self.rig.main_waiting.poll,
            audio=self.audio.diagnostics(), PCM=self.outputs.diagnostics(),
            intro_restarts=None if intro_restarts is None else intro_restarts.diagnostics(),
            narrative_restarts=None if narrative_restarts is None else narrative_restarts.diagnostics(),
            ordered_restarts=None if ordered_restarts is None else ordered_restarts.diagnostics(),
            full_game_or_visual_acceptance_claimed=False)

    def close(self, *, outcome, evidence):
        """Release audio first, then the retained cold rig and PCM files once."""
        if self.closed:
            return
        if threading.get_ident() != self.thread:
            raise RuntimeError('only the actual application thread may close it')
        if type(outcome) is not str or not outcome or type(evidence) is not dict:
            raise ValueError('explicit application outcome and compact evidence required')
        errors = []
        closers = [self.audio.close,
            lambda: self.rig.finish(outcome=outcome, evidence=evidence), self.outputs.close]
        if self.scene_journal is not None:
            closers.append(self.scene_journal.close)
        for close in closers:
            try:
                close()
            except BaseException as error:
                errors.append(error)
        self.closed = True
        if errors:
            primary = errors[0]
            for error in errors[1:]:
                primary.add_note('Additional owner cleanup: ' + str(error))
            raise primary
