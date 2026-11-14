"""Per-invocation cold38 copy authority and exact retained platform handoff.

The old first-epoch authority, cold workspace algorithm and all entry guards
remain unchanged. This additive proof is armed before the actual206 invocation
and sealed only at its genuine260-release/262 suspension on the same Scene.
"""
import ast
from dataclasses import dataclass
import importlib
import inspect
import threading
from types import CodeType, FunctionType, GeneratorType

from . import continuations
from .control_reset import AudioEntryAuthority, AudioControlOwner, AudioControlState
from .cold_workspace import ColdWorkspacePlatform
from .domain import AudioBoundary, AudioState, AlternateGroup, word
from .hardware_scene import SoundDevice, SharedSoundAudioBus
from .owned_runtime import DriverFrame, OwnedAudioDeviceBus, ExplicitAudioPlatform
from .warm_driver_installation import RetainedAudioCarriers
from ..high_level_main_flows.cartridge_source_data import CartridgeSourceData
from ..high_level_main_flows.city_cold_reset import CityColdResetSession, ResetAudioReleasePoint
from ..high_level_main_flows.intro_irq_program import IntroIrqPrograms, OriginalIntroResetJump
from ..high_level_scene_flows.narrative_reset import NarrativeScenePrograms, OriginalNarrativeResetJump


EXPECTED_SOURCE_OWNERS = {'tools.high_level_audio_engine.cold_workspace': {'_actual_whole_workspace_owner': 'def _actual_whole_workspace_owner():\n    """Pin the complete current original owner, without changing its AST."""\n    original = business_boot.initialize_audio_workspace\n    if (type(original) is not FunctionType or original.__module__ != business_boot.__name__\n            or original.__name__ != \'initialize_audio_workspace\'\n            or inspect.isgeneratorfunction(original)):\n        raise AudioBoundary(\'actual complete cold-workspace owner required\')\n    module_source = inspect.getsource(business_boot)\n    if _whole_ast(ast.parse(module_source)) != target.SOURCE_TREES[\'business_boot.py\']:\n        raise AudioBoundary(\'complete actual cold-workspace source contract differs\')\n    parsed = ast.parse(inspect.getsource(original))\n    namespace = dict(vars(business_boot))\n    exec(compile(parsed, \'<unchanged whole cold-workspace owner identity>\', \'exec\'), namespace)\n    plain = namespace[original.__name__]\n    for attribute in (\'co_code\',\'co_consts\',\'co_names\',\'co_varnames\',\'co_argcount\',\'co_kwonlyargcount\',\n            \'co_freevars\',\'co_cellvars\',\'co_flags\'):\n        if getattr(plain.__code__,attribute) != getattr(original.__code__,attribute):\n            raise AudioBoundary(\'loaded cold-workspace callable differs from its whole source\')\n    return original', 'ColdWorkspaceCopyAuthority': 'class ColdWorkspaceCopyAuthority(AudioEntryAuthority):\n    """Actual original38-byte Scene copy at the first released reset epoch.\n\n    This validates real same-Scene source-read/destination-write events and\n    the resulting same sound RAM. It never installs CODE or seeds POP slots.\n    File/source-build provenance belongs to the explicit source loader that\n    supplied this Scene\'s ReadOnlyData, not to RAM\'s apparent byte pattern.\n    """\n    def __init__(self, sound, control, entry_frame, source_data):\n        if (type(sound) is not SoundDevice or sound.scene is None\n                or type(entry_frame) is not DriverFrame or type(source_data) is not ReadOnlyData\n                or sound.audio_state.platform.control_owner is not control or control.sound is not sound\n                or sound.scene.data is not source_data):\n            raise ValueError(\'actual same-Scene sound/control, source DATA and complete entry frame required\')\n        self.sound, self.control, self.frame, self.source_data = sound, control, entry_frame, source_data\n        self.evidence = None\n\n    def provide_frame(self, sound, entry_kind, entry_address, control_state):\n        if (sound is not self.sound or entry_kind != \'startup\' or entry_address != 0\n                or sound.reset_epoch != 1 or self.control.generation != 1\n                or self.control.phase != \'startup-pending\' or control_state.pc_entry != 0\n                or sound.executing or sound.reset_asserted or sound.bus_requested or sound.m68k_granted):\n            raise AudioBoundary(\'first actual released cold-workspace PC0 entry required\')\n        events = sound.scene.events\n        source_index = next((index for index,event in enumerate(events)\n            if event[:3] == (\'read\',0x2CA,1)), None)\n        if source_index is None:\n            raise AudioBoundary(\'original cold38 BYTE source copy has not occurred\')\n        copied = bytearray()\n        for offset in range(38):\n            pair = events[source_index+2*offset:source_index+2*offset+2]\n            if len(pair) != 2:\n                raise AudioBoundary(\'actual cold copy is incomplete\')\n            read, write = pair\n            expected = self.source_data.read(0x2CA+offset,1)\n            if (read != (\'read\',0x2CA+offset,1,expected)\n                    or write != (\'write\',0xA00000+offset,1,expected)):\n                raise AudioBoundary(\'actual source2CA/shared-RAM cold copy differs at \' + hex(offset))\n            copied.append(expected)\n        if bytes(sound.ram[:38]) != bytes(copied):\n            raise AudioBoundary(\'the actual copied cold entry was overwritten before execution\')\n        if not events or events[-1] != (\'write\',0xA11200,2,0x100):\n            raise AudioBoundary(\'cold execution grant requires the actual260 reset release write boundary\')\n        self.evidence = dict(confidence=\'confirmed_same_Scene_original38_BYTE_copy_and_epoch1_entry\',\n            source_start=0x2CA,source_end=0x2F0,bytes=38,\n            original_source_read_event=source_index,reset_release_write_event=len(events)-1,\n            actual_shared_RAM_copy=True, host_RAM_install=False, source_alias_to_driver69D2=False)\n        return self.frame', 'ColdWorkspacePlatform': 'class ColdWorkspacePlatform(ExplicitAudioPlatform):\n    """Supplied normal platform plus the sole original cold indirect tail.\n\n    Alternate groups, reset/control, refresh and memory-BIT providers are still\n    explicit constructor inputs inherited from ExplicitAudioPlatform. No global\n    business callback or other platform object is replaced or monkeypatched.\n    """\n    def __init__(self, **explicit_inputs):\n        super().__init__(**explicit_inputs)\n        self.workspace_session = None\n\n    def bind_workspace_session(self, session):\n        if type(session) is not ColdWorkspaceSession or session.state.platform is not self:\n            raise ValueError(\'one actual same-platform cold workspace session required\')\n        previous = self.workspace_session\n        if (previous is not None and previous is not session\n                and previous.control.generation == previous.generation\n                and previous.sound.reset_epoch == previous.reset_epoch):\n            raise AudioBoundary(\'another live cold-workspace continuation owns this platform\')\n        self.workspace_session = session\n\n    def indirect_transfer(self, image, target_address, context):\n        session = self.workspace_session\n        if session is None:\n            raise AudioBoundary(\'actual cold-workspace indirect continuation is unbound\')\n        return session._accept_original_idle(image,target_address,context)', 'ColdWorkspaceSession': 'class ColdWorkspaceSession:\n    """One actual complete startup invocation ending at its real JP0 idle.\n\n    The startup-kind managed frame claim stays owned by this cold session.\n    finish_frame_session is deliberately NOT called: its driver-ready meaning\n    is wrong for this self-loop. A subsequent genuine RESET invalidates the\n    claim through the existing generation/epoch owner. Idle is not a RET, a\n    driver lease, an opcode polling loop, a HALT instruction or enabled IRQ.\n    """\n    def __init__(self, sound, control, lease):\n        if (type(sound) is not SoundDevice or sound.scene is None\n                or type(sound.audio_state.platform) is not ColdWorkspacePlatform\n                or sound.audio_state.platform.control_owner is not control or control.sound is not sound):\n            raise ValueError(\'same bound sound/control and explicit ColdWorkspacePlatform required\')\n        if lease.entry_kind != \'startup\' or control.phase != \'startup-authorized\':\n            raise AudioBoundary(\'actual cold-workspace startup-kind entry lease required, not driver PC0\')\n        control.require_frame(lease)\n        self.sound, self.state, self.control, self.lease = sound,sound.audio_state,control,lease\n        self.scene, self.generation, self.reset_epoch = sound.scene,lease.generation,lease.reset_epoch\n        self.thread, self.original = threading.get_ident(),_actual_whole_workspace_owner()\n        self.started = self.failed = False\n        self.waiting = None\n        self.events = []\n\n    def _guard(self, *, executing):\n        if (threading.get_ident() != self.thread or self.sound.scene is not self.scene\n                or business_boot.initialize_audio_workspace is not self.original):\n            raise AudioBoundary(\'cold-workspace owner/thread/Scene changed\')\n        if self.failed or self.sound.executing is not executing:\n            raise AudioBoundary(\'cold-workspace execution grant is not at its actual boundary\')\n        if (self.sound.reset_asserted or self.sound.bus_requested or self.sound.m68k_granted\n                or self.sound.reset_epoch != self.reset_epoch or self.control.generation != self.generation):\n            raise AudioBoundary(\'cold-workspace continuation belongs to a reset or bus owner that has changed\')\n\n    def _accept_original_idle(self, image, target_address, context):\n        self._guard(executing=True)\n        self.control.require_frame_session(self,self.generation,self.reset_epoch)\n        if image != \'startup\' or target_address != 0 or type(context) is not InitializeAudioWorkspaceInput:\n            raise AudioBoundary(\'original cold-workspace indirect target/context differs from JP(HL)0\')\n        context.validate(self.state)\n        frame = DriverFrame(**{name:getattr(context,name) for name in _CARRIERS})\n        if any(getattr(frame,name) != 0 for name in _CARRIERS):\n            raise AudioBoundary(\'actual cold POP-cleared carriers/stack do not reach the JP0 idle contract\')\n        control = self.control.control\n        if (self.sound.ram[0] != 0xE9 or control.interrupt_vector != 0\n                or control.iff1 is not False or control.iff2 is not False\n                or control.ei_deferred is not False or control.interrupt_mode != 1):\n            raise AudioBoundary(\'actual self-modifying write or DI/IM1 control has not completed\')\n        point = ColdWorkspaceIdlePoint(self,0,frame,self.generation,self.reset_epoch)\n        self.events.append((\'actual_startup_0025_JP_HL_self_idle\',0,frame.stack_cursor,\n            self.sound.ram[0],self.generation,self.reset_epoch))\n        raise _OriginalColdIdleTransfer(point)\n\n    def start(self):\n        self._guard(executing=False)\n        if self.started:\n            raise AudioBoundary(\'cold-workspace prefix cannot be replayed\')\n        frame = self.control.claim_frame_session(self.lease,self)\n        self.state.platform.bind_workspace_session(self)\n        self.started = True\n        inputs = InitializeAudioWorkspaceInput(**{name:getattr(frame,name) for name in _CARRIERS},\n            continuation=Continuation(\'startup\',0))\n        self.sound.executing = True\n        try:\n            self.original(self.state,inputs)\n        except _OriginalColdIdleTransfer as transfer:\n            point = transfer.point\n            if point.session is not self or point.reset_epoch != self.reset_epoch:\n                raise AudioBoundary(\'cold idle continuation belongs to another invocation\')\n            self.waiting = point\n        except BaseException:\n            self.failed = True\n            self.control.abandon_frame_session(self,reason=\'original cold-workspace execution boundary\')\n            raise\n        else:\n            self.failed = True\n            self.control.abandon_frame_session(self,reason=\'nonreturning cold workspace returned ordinarily\')\n            raise AudioBoundary(\'original cold workspace must not fabricate an ordinary return\')\n        finally:\n            self.sound.executing = False\n        return self.observe_idle()\n\n    def observe_idle(self):\n        """Expose the same actual self-loop; do not execute guessed JP cycles."""\n        self._guard(executing=False)\n        self.control.require_frame_session(self,self.generation,self.reset_epoch)\n        if (self.waiting is None or self.waiting.session is not self\n                or self.waiting.frame.lookup_cursor != 0 or self.sound.ram[0] != 0xE9):\n            raise AudioBoundary(\'actual resident self-modified cold idle is no longer available\')\n        return self.waiting'}, 'tools.high_level_audio_engine.warm_driver_installation': {'RetainedAudioCarriers': 'class RetainedAudioCarriers:\n    """Actual last owned driver carriers; RESET does not initialize them."""\n    owner: object\n    point: object\n    frame: DriverFrame\n    irq_clock: int\n    irq_clock_hz: int\n    generation: int\n    reset_epoch: int\n    data_operations: int\n    thread: int\n\n    @classmethod\n    def retire(cls, owner):\n        from ..reconstructed_game.audio import OwnedGameAudio\n        if type(owner) is not OwnedGameAudio:\n            raise ValueError(\'one exact actually running application audio owner required\')\n        owner._require_owned()\n        point = owner.waiting\n        if type(point.frame) is not DriverFrame:\n            raise AudioBoundary(\'the actual managed driver must retain all eight carriers\')\n        result = cls(owner, point, point.frame, owner._loop.irq_clock,\n            owner._loop.irq_clock_hz, owner.generation, owner.reset_epoch,\n            owner.audio.data_operations, threading.get_ident())\n        before = owner._read_chip_counters()\n        owner.close()\n        if owner._read_chip_counters() != before:\n            raise AudioBoundary(\'retiring software ownership must not advance or replace chips\')\n        result.require_retired(owner.sound, owner.control)\n        return result\n\n    def require_retired(self, sound, control):\n        owner = self.owner\n        if (threading.get_ident() != self.thread or not owner.closed or owner.failed\n                or owner.sound is not sound or owner.control is not control\n                or owner.waiting is not self.point or self.point.frame is not self.frame\n                or owner._loop.irq_clock != self.irq_clock or owner._loop.irq_clock_hz != self.irq_clock_hz\n                or owner.generation != self.generation or owner.reset_epoch != self.reset_epoch\n                or owner.audio.data_operations != self.data_operations\n                or sound.reset_epoch != self.reset_epoch or control.generation != self.generation\n                or control._frame_session is not None or control._lease is not None\n                or getattr(owner.audio, \'mailbox_wz_service\', None) is not None\n                or sound.executing or sound.reset_asserted or sound.bus_requested or sound.m68k_granted):\n            raise AudioBoundary(\'actual closed loop/WZ and unchanged retained general carriers required\')\n        return self.frame'}, 'tools.high_level_audio_engine.control_reset': {'AudioEntryAuthority': 'class AudioEntryAuthority:\n    """Caller-owned source installation/startup evidence; never defaults ready.\n\n    An implementation must actually establish its named entry and return its\n    complete frame. A fixture authority is explicitly experimental, not proof\n    that the game\'s startup ran. This service never infers executable readiness\n    merely from RAM contents or a reset release.\n    """\n    def provide_frame(self, sound, entry_kind, entry_address, control_state):\n        raise AudioBoundary(\'actual audio entry installation/startup authority is unbound\')', 'AudioControlOwner': "class AudioControlOwner:\n    def __init__(self, initial_state, *, reset_asserted):\n        if type(initial_state) is not AudioControlState or type(reset_asserted) is not bool:\n            raise ValueError('explicit control state and initial RESET line required')\n        self.control = initial_state\n        self.reset_asserted = reset_asserted\n        self.phase = 'reset-held' if reset_asserted else 'quiescent'\n        self.generation, self.reset_clocks = 0, 0\n        self.sound, self._lease, self._frame_session = None, None, None\n        self._token, self.events = object(), []\n\n    def bind(self, sound):\n        if type(sound) is not SoundDevice:\n            raise ValueError('one exact shared-RAM SoundDevice required')\n        if self.sound is not None and self.sound is not sound:\n            raise ValueError('control owner already belongs to another sound state')\n        platform = sound.audio_state.platform\n        if not isinstance(platform, AudioPlatform) or getattr(platform, 'control_owner', None) is not self:\n            raise ValueError('same explicitly delegated AudioPlatform control owner required')\n        if sound.reset_asserted != self.reset_asserted:\n            raise ValueError('initial RESET state differs from actual SoundDevice')\n        self.sound = sound\n        return self\n\n    def _bound(self, sound=None):\n        if self.sound is None or (sound is not None and sound is not self.sound):\n            raise AudioBoundary('audio control operation belongs to another/unbound sound')\n        return self.sound\n\n    def reset_changed(self, sound, asserted):\n        self._bound(sound)\n        if type(asserted) is not bool or asserted == self.reset_asserted:\n            raise AudioBoundary('actual RESET transition required')\n        if sound.executing:\n            raise AudioBoundary('RESET cannot discard an active semantic continuation')\n        if asserted:\n            self.generation += 1\n            self._lease = self._frame_session = None\n            self.reset_clocks = 0\n            self.phase, self.reset_asserted = 'reset-held', True\n            self.events.append(('reset_asserted', sound.reset_epoch, self.generation))\n        else:\n            if self.phase != 'reset-held' or self.reset_clocks < 3:\n                raise AudioBoundary('RESET release requires at least three explicitly supplied Z80 clocks')\n            self.phase, self.reset_asserted = 'startup-pending', False\n            # SoundDevice increments its epoch only AFTER this callback returns.\n            self.events.append(('reset_released_pending', sound.reset_epoch + 1,\n                                self.generation, self.reset_clocks))\n\n    def grant_reset_clocks(self, clocks):\n        self._bound()\n        if type(clocks) is not int or clocks < 0:\n            raise ValueError('explicit nonnegative Z80 RESET clocks required')\n        if not self.reset_asserted or self.phase != 'reset-held':\n            raise AudioBoundary('RESET clocks can only be granted while actually held')\n        previous = self.reset_clocks\n        self.reset_clocks += clocks\n        self.events.append(('reset_clock_grant', clocks, self.reset_clocks))\n        if previous < 3 <= self.reset_clocks:\n            self.control = AudioControlState(0, 0, 0, False, False, 0, False)\n            self.events.append(('reset_control_established', self.generation))\n\n    def _write_control(self, **values):\n        self._bound()\n        if self.reset_asserted:\n            raise AudioBoundary('software control instruction cannot execute during RESET')\n        self.control = replace(self.control, **values)\n\n    def set_interrupt_vector(self, value):\n        self._write_control(interrupt_vector=byte(value))\n        self.events.append(('set_interrupt_vector', value))\n\n    def set_refresh(self, value):\n        self._write_control(refresh=byte(value))\n        self.events.append(('set_refresh', value))\n\n    def interrupt_control(self, enabled, deferred_one_instruction):\n        if type(enabled) is not bool or type(deferred_one_instruction) is not bool:\n            raise ValueError('explicit IFF and EI-delay booleans required')\n        if not enabled and deferred_one_instruction:\n            raise ValueError('DI cannot introduce an EI delay')\n        self._write_control(iff1=enabled, iff2=enabled,\n                            ei_deferred=deferred_one_instruction)\n        self.events.append(('interrupt_control', enabled, deferred_one_instruction))\n\n    def interrupt_mode(self, mode):\n        if type(mode) is not int or mode not in (0, 1, 2):\n            raise ValueError('actual interrupt mode 0/1/2 required')\n        self._write_control(interrupt_mode=mode)\n        self.events.append(('interrupt_mode', mode))\n\n    def complete_ei_following_instruction(self, *, generation, reset_epoch):\n        sound = self._bound()\n        if generation != self.generation or reset_epoch != sound.reset_epoch:\n            raise AudioBoundary('instruction-completion grant belongs to another reset')\n        if self.control.ei_deferred is not True:\n            raise AudioBoundary('no actual deferred EI instruction to complete')\n        self._write_control(ei_deferred=False)\n        self.events.append(('explicit_EI_following_instruction_completed', generation, reset_epoch))\n\n    def acquire_frame(self, entry_kind, entry_address, *, authority):\n        sound = self._bound()\n        word(entry_address)\n        if entry_kind not in ('startup', 'driver'):\n            raise ValueError('finite startup/driver entry kind required')\n        if sound.executing or sound.reset_asserted or self.reset_asserted:\n            raise AudioBoundary('entry authority requires a released inactive sound owner')\n        if self._frame_session is not None:\n            raise AudioBoundary('an actual managed frame session already owns this entry')\n        if not isinstance(authority, AudioEntryAuthority):\n            raise AudioBoundary('actual startup/driver installation authority required')\n        frame = authority.provide_frame(sound, entry_kind, entry_address, self.control)\n        if type(frame) is not DriverFrame:\n            raise AudioBoundary('entry authority did not supply the complete actual DriverFrame')\n        self.control = replace(self.control, pc_entry=entry_address)\n        self.phase = 'startup-authorized' if entry_kind == 'startup' else 'driver-ready'\n        self._lease = AudioFrameLease(self._token, self.generation, sound.reset_epoch,\n                                     entry_kind, frame)\n        self.events.append(('entry_authorized', entry_kind, entry_address,\n                            self.generation, sound.reset_epoch))\n        return self._lease\n\n    def require_frame(self, lease):\n        sound = self._bound()\n        if (type(lease) is not AudioFrameLease or lease is not self._lease\n                or lease.owner_token is not self._token or lease.generation != self.generation\n                or lease.reset_epoch != sound.reset_epoch or self.reset_asserted\n                or sound.reset_asserted):\n            raise AudioBoundary('expired or foreign managed audio frame')\n        return lease.frame\n\n    def claim_frame_session(self, lease, session):\n        frame = self.require_frame(lease)\n        if self._frame_session is not None or session is None:\n            raise AudioBoundary('one actual managed frame session required')\n        self._lease, self._frame_session = None, session\n        self.events.append(('frame_session_claimed', self.generation, lease.reset_epoch))\n        return frame\n\n    def require_frame_session(self, session, generation, reset_epoch):\n        sound = self._bound()\n        if (self._frame_session is not session or session is None\n                or type(generation) is not int or generation != self.generation\n                or type(reset_epoch) is not int or reset_epoch != sound.reset_epoch\n                or self.reset_asserted or sound.reset_asserted):\n            raise AudioBoundary('expired or foreign managed audio frame session')\n        return sound\n\n    def finish_frame_session(self, session, generation, reset_epoch, frame):\n        self.require_frame_session(session, generation, reset_epoch)\n        if type(frame) is not DriverFrame:\n            raise ValueError('complete actual session frame required')\n        self._frame_session = None\n        self._lease = AudioFrameLease(self._token, generation, reset_epoch, 'driver', frame)\n        self.phase = 'driver-ready'\n        self.events.append(('frame_session_finished', generation, reset_epoch))\n        return self._lease\n\n    def abandon_frame_session(self, session, *, reason):\n        if self._frame_session is not session or session is None:\n            return  # A reset/new owner must not be modified by an old session.\n        if type(reason) is not str or not reason:\n            raise ValueError('actual session boundary reason required')\n        self._frame_session = self._lease = None\n        self.phase = 'execution-boundary'\n        self.events.append(('frame_session_boundary', reason, self.generation))\n\n    def accept_session_im1(self, session, generation, reset_epoch):\n        sound = self.require_frame_session(session, generation, reset_epoch)\n        if (not sound.executing or sound.bus_requested or sound.m68k_granted\n                or self.control.interrupt_mode != 1 or self.control.iff1 is not True\n                or self.control.ei_deferred is not False):\n            raise AudioBoundary('actual released IM1-enabled instruction boundary required')\n        self.control = replace(self.control, iff1=False, iff2=False, ei_deferred=False)\n        self.events.append(('IM1_accepted', generation, reset_epoch, 0x38))\n\n    def run_stage(self, lease, stage, *, return_word):\n        frame = self.require_frame(lease)\n        if lease.entry_kind != 'driver' or self.phase != 'driver-ready':\n            raise AudioBoundary('driver stage needs actual driver-entry authority')\n        # Raw DriverFrame APIs remain available and cannot enforce this lease.\n        # This managed channel is linear and invalidates its carrier on failure.\n        self._lease = None\n        try:\n            returned = run_driver_stage(self.sound, stage, frame, return_word=return_word,\n                                        reset_epoch=lease.reset_epoch)\n        except BaseException:\n            self.phase = 'execution-boundary'\n            raise\n        self._lease = AudioFrameLease(self._token, self.generation, lease.reset_epoch,\n                                     'driver', returned)\n        return self._lease"}, 'tools.high_level_audio_engine.owned_runtime': {'ExplicitAudioPlatform': 'class ExplicitAudioPlatform(AudioPlatform):\n    """Supplied alternate groups and condition providers, no guessed refresh/WZ."""\n\n    def __init__(self, *, alternate_accumulator, alternate_group, refresh_reader,\n                 memory_bit_reader, control_owner=None):\n        word(alternate_accumulator)\n        if type(alternate_group) is not AlternateGroup:\n            raise ValueError(\'explicit complete alternate word group required\')\n        alternate_group.validate()\n        if not callable(refresh_reader) or not callable(memory_bit_reader):\n            raise ValueError(\'actual refresh and memory-BIT condition providers required\')\n        self.alternate_accumulator, self.alternate_group = alternate_accumulator, alternate_group\n        self.refresh_reader, self.memory_bit_reader = refresh_reader, memory_bit_reader\n        if control_owner is not None and any(not callable(getattr(control_owner, name, None))\n                for name in (\'set_interrupt_vector\', \'set_refresh\', \'interrupt_control\', \'interrupt_mode\')):\n            raise ValueError(\'explicit complete audio control owner required\')\n        self.control_owner = control_owner\n\n    def set_interrupt_vector(self, value):\n        if self.control_owner is None:\n            return super().set_interrupt_vector(value)\n        return self.control_owner.set_interrupt_vector(value)\n\n    def set_refresh(self, value):\n        if self.control_owner is None:\n            return super().set_refresh(value)\n        return self.control_owner.set_refresh(value)\n\n    def interrupt_control(self, enabled, deferred_one_instruction):\n        if self.control_owner is None:\n            return super().interrupt_control(enabled, deferred_one_instruction)\n        return self.control_owner.interrupt_control(enabled, deferred_one_instruction)\n\n    def interrupt_mode(self, mode):\n        if self.control_owner is None:\n            return super().interrupt_mode(mode)\n        return self.control_owner.interrupt_mode(mode)\n\n    def exchange_alternate_accumulator(self, current):\n        word(current)\n        previous, self.alternate_accumulator = self.alternate_accumulator, current\n        return previous\n\n    def exchange_alternate_group(self, current):\n        if type(current) is not AlternateGroup:\n            raise ValueError(\'actual alternate word group required\')\n        current.validate()\n        previous, self.alternate_group = self.alternate_group, current\n        return previous\n\n    def read_refresh(self, previous_conditions):\n        value, conditions = self.refresh_reader(byte(previous_conditions))\n        return byte(value), byte(conditions)\n\n    def memory_bit_conditions(self, context):\n        return byte(self.memory_bit_reader(context.validate()))\n\n    def indirect_transfer(self, image, target, context):\n        raise AudioBoundary(\'unbound owned sound tail: \' + image + \':\' + hex(target)\n            + \' context=\' + type(context).__name__ + \' live=\' + repr(context))'}, 'tools.high_level_audio_engine.hardware_scene': {'SoundDevice': 'class SoundDevice:\n    """Own explicit line state, same AudioState, and finite semantic invocations.\n\n    A request does not itself grant ownership. A scheduler first synchronizes\n    its real sound work, then explicitly calls grant_m68k(). No cycle counts,\n    CPU registers or successful reset/IRQ continuations are synthesized.\n    """\n\n    def __init__(self, audio_state, schedule, *, reset_asserted, bus_requested,\n                 m68k_granted):\n        if type(audio_state) is not AudioState or type(audio_state.bus) is not SharedSoundAudioBus:\n            raise ValueError(\'exact AudioState with shared sound RAM bus required\')\n        if not isinstance(schedule, SoundSchedule):\n            raise ValueError(\'explicit sound scheduling authority required\')\n        if any(type(value) is not bool for value in\n               (reset_asserted, bus_requested, m68k_granted)):\n            raise ValueError(\'explicit initial sound control line states required\')\n        if m68k_granted and (reset_asserted or not bus_requested):\n            raise ValueError(\'grant requires released reset and asserted request\')\n        if audio_state.bus.device is not None:\n            raise ValueError(\'shared AudioState already has a sound owner\')\n        self.audio_state, self.schedule = audio_state, schedule\n        self.ram = audio_state.bus.ram\n        self.reset_asserted, self.bus_requested = reset_asserted, bus_requested\n        self.m68k_granted, self.executing = m68k_granted, False\n        self.reset_epoch, self.scene = 0, None\n        audio_state.bus.device = self\n\n    def request_bus(self, requested):\n        if type(requested) is not bool:\n            raise ValueError(\'explicit BUSREQ level required\')\n        self.bus_requested = requested\n        if not requested:\n            self.m68k_granted = False\n\n    def set_reset(self, asserted):\n        if type(asserted) is not bool:\n            raise ValueError(\'explicit RESET level required\')\n        if asserted == self.reset_asserted:\n            return\n        if self.executing:\n            raise Boundary(\'reset during an active audio semantic call requires its continuation\')\n        # The supplied owner must perform its real CPU/chip reset effects. If\n        # unbound/failed, this transition is not recorded as completed here.\n        self.schedule.reset_changed(self, asserted)\n        self.reset_asserted = asserted\n        if asserted:\n            self.m68k_granted = False\n        else:\n            self.reset_epoch += 1\n\n    def grant_m68k(self):\n        if not self.bus_requested or self.reset_asserted:\n            raise Boundary(\'cannot grant Z80 RAM without request and released reset\')\n        if self.executing:\n            raise Boundary(\'cannot grant Z80 RAM during an active audio semantic call\')\n        self.m68k_granted = True\n\n    def require_m68k_owner(self):\n        if not self.m68k_granted or not self.bus_requested or self.reset_asserted:\n            raise Boundary(\'68000 does not own shared Z80 RAM\')\n\n    def require_audio_owner(self):\n        if self.reset_asserted or self.m68k_granted or not self.executing:\n            raise AudioBoundary(\'audio DATA requires an active supplied execution grant\')\n\n    def bus_ack(self, address, size):\n        if self.bus_requested and not self.reset_asserted and not self.m68k_granted:\n            self.schedule.poll_bus_request(self)\n        # All other bits are actual supplied bus data, not invented zeros.\n        observed = uint(self.schedule.read_open_bus(address, size), size * 8)\n        bit = 1 if size == 1 else 0x100\n        granted = self.bus_requested and self.m68k_granted and not self.reset_asserted\n        return observed & ~bit if granted else observed | bit\n\n    def execute_audio(self, entry, inputs, *, reset_epoch):\n        """Invoke one recovered function on its actual typed inputs and stack.\n\n        This finite entry list is not opcode dispatch. Long-lived driver/startup\n        functions can still stop on genuine external continuations/budgets.\n        Caller must supply fresh inputs after reset; an old context is rejected.\n        """\n        if type(reset_epoch) is not int or reset_epoch != self.reset_epoch:\n            raise AudioBoundary(\'audio inputs belong to a different reset epoch\')\n        if self.reset_asserted or self.m68k_granted or self.executing or self.bus_requested:\n            raise AudioBoundary(\'sound execution requires released bus/reset and no active call\')\n        from .business_boot import initialize_audio_workspace\n        from .business_hardware import initialize_audio_driver, wait_fm_ready\n        from .business_mailbox import poll_command_mailboxes, arbitrate_command_slot\n        entries = {\'initialize_audio_workspace\': initialize_audio_workspace,\n                   \'initialize_audio_driver\': initialize_audio_driver,\n                   \'wait_fm_ready\': wait_fm_ready,\n                   \'poll_command_mailboxes\': poll_command_mailboxes,\n                   \'arbitrate_command_slot\': arbitrate_command_slot}\n        if type(entry) is not str or entry not in entries:\n            raise AudioBoundary(\'unbound high-level sound execution entry\')\n        self.executing = True\n        try:\n            return entries[entry](self.audio_state, inputs)\n        finally:\n            self.executing = False', 'SharedSoundAudioBus': 'class SharedSoundAudioBus:\n    """AudioState\'s real RAM bus; 8 KiB is mirrored in Z80 0000..3FFF.\n\n    The supplied external AudioBus owns banked material, YM2612, PSG, timing,\n    transfer boundaries and every address not backed by sound RAM here.\n    """\n\n    def __init__(self, ram, devices):\n        if type(ram) is not bytearray or len(ram) != 8192:\n            raise ValueError(\'one explicit live 8 KiB sound RAM required\')\n        if any(not callable(getattr(devices, name, None)) for name in\n               (\'read_byte\', \'write_byte\', \'progress\', \'transfer_boundary\')):\n            raise ValueError(\'explicit external AudioBus owner required\')\n        self.ram, self.devices, self.device = ram, devices, None\n\n    def _owner(self):\n        if self.device is None:\n            raise AudioBoundary(\'shared sound bus was not attached\')\n        self.device.require_audio_owner()\n\n    def read_byte(self, address):\n        word(address)\n        self._owner()\n        return self.ram[address & 0x1FFF] if address < 0x4000 else byte(self.devices.read_byte(address))\n\n    def write_byte(self, address, value):\n        word(address); byte(value)\n        self._owner()\n        if address < 0x4000:\n            self.ram[address & 0x1FFF] = value\n        else:\n            self.devices.write_byte(address, value)\n\n    def progress(self, reason):\n        self._owner()\n        return self.devices.progress(reason)\n\n    def transfer_boundary(self, reason):\n        self._owner()\n        return self.devices.transfer_boundary(reason)'}, 'tools.high_level_main_flows.city_cold_reset': {'CityColdResetSession': 'class CityColdResetSession(PersistentColdResetSession):\n    """One original206 invocation, choosing its city main before actual00300.\n\n    The base reset protocol and exact ResetAudioReleasePoint are retained.\n    No old BootstrapMainSession or installation authority guard is relaxed.\n    This new class has its own explicit nonreturning tail handoff contract.\n    """\n\n    def __init__(self, state, frame, profile):\n        self._source_pins = _pin_sources()\n        super().__init__(state, frame, profile)\n        self._base_factory = self.program_factory\n        self._main_code = None\n        self._entered_main = False\n        self.initial_device_waits = ()\n        self.first_main_wait = None\n        self.first_main_suspensions = None\n        self.program_factory = _clone_tail_binding(self.original, self._base_factory, self._city_main_tail)\n        self.source_contract = dict(self.source_contract,\n            confidence=\'confirmed_static_whole_reset_view_private_tail_binding\',\n            callee_or_global_replacement=True, module_global_replacement=False,\n            private_namespace_changed_names=(\'start_game_main_loop_frame_fields\',),\n            warm_and_cold_tail_calls=2, reset_generator_CodeType_identical=True,\n            selected_main=\'PersistentCitySceneSession\', additional_physical_CALL_slots=0)\n\n    def _guard(self):\n        super()._guard()\n        _require_pins(self._source_pins)\n\n    def _city_main_tail(self, state, frame):\n        self._guard()\n        if state is not self.state or self._entered_main or self.main_session is not None:\n            raise Boundary(\'one original reset tail may enter its actual00300 once\')\n        frame = _movement_frame(state, frame)\n        self._entered_main = True\n        main = city_scene_steps.PersistentCitySceneSession(state, frame)\n        self.main_session = main\n        self._main_code = main._program.gi_code\n        waiting = main.start()\n        while type(waiting) is GameplaySceneWait:\n            self._progress_initial_device(main, waiting)\n            waiting = main.resume_device(waiting.event)\n        if (type(waiting) is not BootstrapMainWait or waiting is not main.waiting\n                or waiting.state is not state or waiting.poll != 0x3BC\n                or main.suspensions != len(self.initial_device_waits) + 1):\n            raise Boundary(\'original00300 must reach its first actual3BC after its startup devices\')\n        self.first_main_wait = waiting\n        self.first_main_suspensions = main.suspensions\n        boundary = MovementContinuationBoundary(waiting.poll, waiting.frame,\n            \'actual original reset tail retains the preselected city main at3BC\')\n        boundary.city_cold_reset_session = self\n        boundary.city_main_session = main\n        boundary.city_main_wait = waiting\n        raise boundary\n\n    def _progress_initial_device(self, main, waiting):\n        """Consume only the actual startup sprite-DMA supply already bound.\n\n        Original00300 writes request4 before its first3BC. Its indexed CALL\n        enters3D8, then93F0/4EE and68CE/9408. The physical three return LONGs\n        stay on the original stack throughout every68FA busy-bit poll.\n        """\n        self._guard()\n        if (type(main) is not city_scene_steps.PersistentCitySceneSession\n                or main is not self.main_session or waiting is not main.waiting\n                or type(waiting) is not GameplaySceneWait or waiting.state is not self.state\n                or waiting.needs_interrupt or (waiting.event, waiting.poll) != (\'vdp-dma\', 0x68FA)\n                or main.suspensions != len(self.initial_device_waits) + 1):\n            raise Boundary(\'one actual initial3D8/93F0 sprite-DMA continuation required\')\n        waiting.validate()\n        stack = waiting.frame.stack_cursor\n        if stack.base != 0x00FFFDF4:\n            raise Boundary(\'initial sprite DMA must retain the real startup physical SP\')\n        # Observe the shared live backing for a host witness, not extra CPU\n        # DATA reads that would change the original event stream/read budget.\n        start = stack.base & 65535\n        slots = tuple(int.from_bytes(self.state.ram[start + offset:start + offset + 4], \'big\')\n            for offset in (0, 4, 8))\n        if slots != (0x9408, 0x4EE, 0x3CE):\n            raise Boundary(\'initial sprite DMA must retain all three real startup CALL slots\')\n        self.initial_device_waits += (waiting,)\n        # This routes to the existing same-Scene finite SuppliedVideoEvents.\n        # Missing/exhausted slots remain a Boundary; no transfer is invented.\n        self.state.progress(waiting.event)\n\n    def _advance(self, frame=None):\n        self._guard()\n        try:\n            point = next(self.program) if frame is None else self.program.send(frame)\n        except MovementContinuationBoundary as boundary:\n            main = getattr(boundary, \'city_main_session\', None)\n            waiting = getattr(boundary, \'city_main_wait\', None)\n            if (getattr(boundary, \'city_cold_reset_session\', None) is not self\n                    or type(main) is not city_scene_steps.PersistentCitySceneSession\n                    or main is not self.main_session or type(waiting) is not BootstrapMainWait\n                    or waiting is not main.waiting or waiting.state is not self.state\n                    or boundary.target != waiting.poll or boundary.context is not waiting.frame):\n                self.failed = True\n                raise\n            self.waiting, self.phase = waiting, \'original-main-tail\'\n            self.require_main_identity(main, waiting)\n            self.events.append((\'actual_original300_city_tail_handoff\', waiting.poll,\n                waiting.frame.stack_cursor.base, main.suspensions))\n            return waiting\n        except StopIteration as completion:\n            self.failed = True\n            raise Boundary(\'original nonreturning206/city00300 unexpectedly returned\') from completion\n        except BaseException:\n            self.failed = True\n            raise\n        if type(point) is not ResetAudioReleasePoint or point.session is not self:\n            self.failed = True\n            raise Boundary(\'city reset yielded no actual original260/262 release point\')\n        self.waiting, self.phase = point, \'actual-audio-release\'\n        self.events.append((\'completed_original260_suspend_before262\', point.pc,\n            point.frame.stack_cursor.base, point.full_sr))\n        return point\n\n    def require_main_identity(self, main, waiting):\n        """Read-only exact same-invocation/source witness; return actual CodeType.\n\n        The installation capture can keep its own first3BC/SP/suspension tests;\n        this method proves which real, whole-derived main generator owns it.\n        It grants nothing and does not read RAM, chips or cartridge DATA.\n        """\n        self._guard()\n        if (self.phase != \'original-main-tail\' or not self._entered_main\n                or type(main) is not city_scene_steps.PersistentCitySceneSession\n                or main is not self.main_session or main.state is not self.state\n                or waiting is not self.waiting or waiting is not main.waiting\n                or waiting.state is not self.state or main._failed\n                or type(main._program) is not GeneratorType or main._program.gi_running\n                or type(self._main_code) is not CodeType or main._program.gi_code is not self._main_code):\n            raise Boundary(\'exact original-reset/preselected-city-main source handoff required\')\n        main._require_current()\n        waiting.validate()\n        return self._main_code\n\n    def require_first_main_wait(self, main, waiting):\n        """Prove this invocation\'s first3BC, not a one-suspension shortcut."""\n        self.require_main_identity(main, waiting)\n        if (type(waiting) is not BootstrapMainWait or waiting.poll != 0x3BC\n                or waiting is not self.first_main_wait\n                or main.suspensions != self.first_main_suspensions\n                or self.first_main_suspensions != len(self.initial_device_waits) + 1\n                or waiting.frame.stack_cursor.base != 0x00FFFE00):\n            raise Boundary(\'the retained actual initial-device-to-first3BC witness is required\')\n        return True\n\n    def resume_main(self, frame, pc):\n        self._guard()\n        self.require_main_identity(self.main_session, self.waiting)\n        self.waiting = self.main_session.resume(frame, pc)\n        return self.waiting\n\n    def resume_device(self, event):\n        self._guard()\n        self.require_main_identity(self.main_session, self.waiting)\n        self.waiting = self.main_session.resume_device(event)\n        return self.waiting'}, 'tools.high_level_main_flows.intro_irq_program': {'IntroIrqPrograms': 'class IntroIrqPrograms:\n    """Explicit per-Scene provider for the complete actual original IRQ core."""\n    def __init__(self, state):\n        self.state = checked_state(state)\n        self.thread, self.active, self.pending = threading.get_ident(), False, None\n        self.entered = None\n        self.jumps = self.claimed = 0\n        tree = ast.parse(inspect.getsource(lowbank), filename=lowbank.__file__)\n        plain = compile(tree, lowbank.__file__, \'exec\', dont_inherit=True)\n        derived = compile(_lift_intro_tree(tree), lowbank.__file__, \'exec\', dont_inherit=True)\n        self.originals = {}\n        namespace = dict(vars(lowbank))\n        if \'_intro_reset_jump\' in namespace:\n            raise Boundary(\'private intro JMP name must not shadow original source\')\n        namespace[\'_intro_reset_jump\'] = self._jump\n        self.views = {}\n        for name in NAMES:\n            original = getattr(lowbank, name)\n            if (type(original) is not FunctionType or original.__globals__ is not vars(lowbank)\n                    or original.__closure__ is not None or original.__module__ != lowbank.__name__\n                    or _code_shape(original.__code__) != _code_shape(_top_code(plain, name))):\n                raise Boundary(\'actual complete original intro function/source identity required: \' + name)\n            self.originals[name] = (original, original.__code__)\n            view = FunctionType(_top_code(derived, name), namespace, name, original.__defaults__, None)\n            view.__kwdefaults__ = original.__kwdefaults__\n            view.__annotations__ = dict(original.__annotations__)\n            self.views[name] = namespace[name] = view\n        self.source_contract = dict(confidence=\'confirmed_complete_source_inverses_runtime_unverified\',\n            whole_functions=5, changed_original_expressions=1, whole_FN_inverse=True,\n            whole_module_inverse=True, module_monkeypatch=False, PC_interpreter=False,\n            real_jump=[0x4786, 0x206], ordinary_RTS_or_RTE_invented=False)\n\n    def _guard(self):\n        if threading.get_ident() != self.thread:\n            raise Boundary(\'intro IRQ provider belongs to its actual Scene thread\')\n        for name, (owner, code) in self.originals.items():\n            if getattr(lowbank, name) is not owner or owner.__code__ is not code:\n                raise Boundary(\'actual complete intro IRQ callee was rebound: \' + name)\n\n    def run_irq(self, entered):\n        self._guard()\n        entered = _movement_frame(self.state, entered)\n        if self.active or self.pending is not None or entered.status != self.state.sr & 31:\n            raise Boundary(\'one actual same-Scene IRQ invocation and no unclaimed JMP required\')\n        if not self.state.events or self.state.events[-1][:4] != (\'interrupt_enter\', 6, 0x78, 0x481E):\n            raise Boundary(\'actual original level6 exception entry must immediately precede this core\')\n        self.active, self.entered = True, entered\n        try:\n            return self.views[\'lowbank_process_device_control_6_fields\'](self.state, entered)\n        finally:\n            self.active, self.entered = False, None\n\n    def _jump(self, state, frame, source_pc, target):\n        self._guard()\n        frame = _movement_frame(state, frame)\n        if (not self.active or state is not self.state or self.pending is not None\n                or (source_pc, target) != (0x4786, 0x206)\n                or frame.status != state.sr & 31\n                or frame.stack_cursor.base != self.entered.stack_cursor.base - 68):\n            raise Boundary(\'actual4742 terminal JMP with original MOVEM/two child slots required\')\n        jump = OriginalIntroResetJump(self, frame, state.sr)\n        self.pending = jump\n        self.jumps += 1\n        state.events.append((\'original_nonreturning_jump\', 0x4786, 0x206,\n            frame.stack_cursor.base, state.sr))\n        raise jump\n\n    def claim(self, jump):\n        self._guard()\n        if (type(jump) is not OriginalIntroResetJump or jump is not self.pending\n                or jump.owner is not self or self.active or jump.state is not self.state\n                or jump.full_sr != self.state.sr or jump.frame.status != self.state.sr & 31):\n            raise Boundary(\'one unconsumed actual original4786 transfer required\')\n        self.pending = None\n        self.claimed += 1\n        return jump.frame', 'OriginalIntroResetJump': 'class OriginalIntroResetJump(Exception):\n    """A real JMP control transfer: no CALL slot, RTE result or ordinary return."""\n    def __init__(self, owner, frame, full_sr):\n        self.owner, self.state, self.frame = owner, owner.state, frame\n        self.source_pc, self.target, self.full_sr = 0x4786, 0x206, full_sr\n        super().__init__(\'original4786 JMP206 discarded the old IRQ/Main continuation\')'}, 'tools.high_level_scene_flows.narrative_reset': {'NarrativeScenePrograms': 'class NarrativeScenePrograms(RepeatingScenePrograms):\n    """Finite same-Scene narrative terminal provider for the actual Main4B4."""\n    def __init__(self,state):\n        self._narrative_own_bindings=_pin_own()\n        self._narrative_base_methods,self._narrative_base_functions=_pin_base()\n        self._narrative_base=RepeatingScenePrograms\n        self._narrative_class=NarrativeScenePrograms\n        self._narrative_methods={name:(function,function.__code__)\n            for name,function in vars(NarrativeScenePrograms).items()if type(function)is FunctionType}\n        self._narrative_jump_class=OriginalNarrativeResetJump\n        self._narrative_jump_init=(OriginalNarrativeResetJump.__init__,OriginalNarrativeResetJump.__init__.__code__)\n        self._narrative_base_methods[\'__init__\'][0](self,state)\n        self.thread=threading.get_ident();self.active=False;self.entered=None\n        self.pending=self.claimed_jump=self.terminated_jump=None\n        self.terminated=False;self.exit_site=None;self.jumps=self.claimed=0\n        self.narrative_originals={};self.narrative_views={};self.narrative_namespaces={}\n        self.narrative_bindings={}\n        modules={\'support\':self.repeat_modules[\'support\'],\'story\':self.repeat_modules[\'story\']}\n        for group,module in modules.items():\n            tree=ast.parse(inspect.getsource(module),filename=module.__file__)\n            nodes={node.name:node for node in tree.body if isinstance(node,ast.FunctionDef)}\n            plain=compile(tree,module.__file__,\'exec\',dont_inherit=True)\n            derived=compile(_narrative_tree(group,tree),module.__file__,\'exec\',dont_inherit=True)\n            namespace=dict(vars(module));self.narrative_namespaces[group]=namespace\n            for name in VIEW_NAMES[group]:\n                function=getattr(module,name)\n                if (name not in nodes or _dump(nodes[name])!=_dump(ast.parse(EXPECTED_SOURCE[group][name]).body[0])\n                        or type(function)is not FunctionType or function.__globals__ is not vars(module)\n                        or function.__module__!=module.__name__ or function.__name__!=name\n                        or function.__closure__ is not None or function.__code__.co_freevars\n                        or _code_shape(function.__code__)!=_code_shape(_code_at(plain,name))):\n                    raise Boundary(\'actual complete original story owner required: \'+name)\n                self.narrative_originals[group,name]=(module,function,function.__code__)\n                view=FunctionType(_code_at(derived,name),namespace,name,function.__defaults__,None)\n                view.__kwdefaults__=function.__kwdefaults__;view.__annotations__=dict(function.__annotations__)\n                namespace[name]=view;self.narrative_views[group,name]=(view,view.__code__)\n                self.narrative_bindings[group,name]=view\n        self._narrative_view_owners=dict(self.narrative_views)\n        aliases={\'_narrative_story\':self._story,\'_narrative_exit\':self._exit,\'_narrative_jump\':self._jump}\n        for group,namespace in self.narrative_namespaces.items():\n            for name,value in aliases.items():\n                if name in namespace:raise Boundary(\'private narrative alias cannot replace original source name\')\n                namespace[name]=value;self.narrative_bindings[group,name]=value\n        name=\'dispatch_repeating_scene_presentation_fields\'\n        self._narrative_route=self.narrative_views[\'support\',name][0]\n        # Only the same instance\'s private238 helper sees the new finite owner.\n        # No original module function, global dispatcher or original code is rebound.\n        self.repeat_namespaces[\'support\'][name]=self._narrative_route\n        self.repeat_bindings[\'support\',name]=self._narrative_route\n        self.source_contract=dict(confidence=\'confirmed_source_candidate_runtime_unverified\',\n            whole_private_views=14,changed_original_expressions=7,whole_FN_inverse=True,\n            whole_module_inverse=True,actual_jump_sites=tuple(EXIT_SITES.values()),target=0x206,\n            physical_retained_LONGs=(0x3B77E,0x580,0x3CE),new_IRQ_or_RTS=False,\n            reset_authority_supplied=False,default_clock_or_budget_added=False)\n\n    def require_current(self,state):\n        if (RepeatingScenePrograms is not self._narrative_base\n                or repeating.RepeatingScenePrograms is not self._narrative_base\n                or NarrativeScenePrograms is not self._narrative_class\n                or NarrativeScenePrograms.__bases__!=(self._narrative_base,)\n                or OriginalNarrativeResetJump is not self._narrative_jump_class):\n            raise Boundary(\'actual narrative/source parent class identity changed\')\n        for owner,name,function,code in self._narrative_own_bindings:\n            if getattr(owner,name)is not function or function.__code__ is not code:\n                raise Boundary(\'actual complete-module narrative provider binding changed: \'+name)\n        for name,(function,code)in self._narrative_methods.items():\n            if vars(self._narrative_class).get(name)is not function or function.__code__ is not code:\n                raise Boundary(\'actual narrative owner method changed: \'+name)\n        function,code=self._narrative_jump_init\n        if OriginalNarrativeResetJump.__init__ is not function or function.__code__ is not code:\n            raise Boundary(\'actual narrative transfer class changed\')\n        for name,(function,code)in self._narrative_base_methods.items():\n            if vars(self._narrative_base).get(name)is not function or function.__code__ is not code:\n                raise Boundary(\'actual repeating parent method changed: \'+name)\n        for name,(function,code)in self._narrative_base_functions.items():\n            if getattr(repeating,name)is not function or function.__code__ is not code:\n                raise Boundary(\'actual repeating parent utility changed: \'+name)\n        self._narrative_base_methods[\'require_current\'][0](self,state)\n        if not hasattr(self,\'narrative_originals\'):return\n        if threading.get_ident()!=self.thread:raise Boundary(\'narrative transfer belongs to its actual Scene thread\')\n        for (group,name),(module,function,code)in self.narrative_originals.items():\n            if getattr(module,name)is not function or function.__code__ is not code:\n                raise Boundary(\'actual original narrative callable changed: \'+name)\n        if self.narrative_views.keys()!=self._narrative_view_owners.keys():\n            raise Boundary(\'finite complete narrative graph inventory changed\')\n        for (group,name),(view,code)in self._narrative_view_owners.items():\n            if (self.narrative_views[group,name]!=(view,code)\n                    or self.narrative_namespaces[group].get(name)is not view or view.__code__ is not code):\n                raise Boundary(\'private complete narrative view changed: \'+name)\n        for (group,name),value in self.narrative_bindings.items():\n            if self.narrative_namespaces[group].get(name)is not value:\n                raise Boundary(\'private narrative source binding changed: \'+name)\n        if (self.repeat_namespaces[\'support\'].get(\'dispatch_repeating_scene_presentation_fields\')is not self._narrative_route\n                or self.repeat_bindings.get((\'support\',\'dispatch_repeating_scene_presentation_fields\'))is not self._narrative_route):\n            raise Boundary(\'same-instance Main4B4 terminal dispatcher binding changed\')\n\n    def _story(self,memory,frame,target):\n        self.require_current(memory.state)\n        if (type(memory)is not SceneRefreshMemory or not self.active\n                or target not in (0x3B79E,0x3B7A2,0x3B7A6,0x3B7AA,0x3B7AE)):\n            raise Boundary(\'actual running Main4B4 narrative dispatcher required\')\n        return self.narrative_views[\'story\',\'_story_known_fields\'][0](memory,frame,target)\n\n    def _exit(self,memory,frame,source_pc):\n        self.require_current(memory.state)\n        if (type(memory)is not SceneRefreshMemory or not self.active or self.exit_site is not None\n                or source_pc not in EXIT_SITES.values()):\n            raise Boundary(\'one actual finite original story exit caller required\')\n        self.exit_site=source_pc\n        try:return self.narrative_views[\'story\',\'_story_exit_fields\'][0](memory,frame)\n        finally:self.exit_site=None\n\n    def _jump(self,memory,frame,target):\n        self.require_current(memory.state)\n        frame=_movement_frame(self.state,frame)\n        if (type(memory)is not SceneRefreshMemory or memory.state is not self.state\n                or not self.active or self.entered is None or self.pending is not None\n                or self.claimed_jump is not None or self.exit_site not in EXIT_SITES.values()\n                or target!=0x206 or frame.status!=(self.state.sr&31)\n                or frame.stack_cursor.base!=self.entered.stack_cursor.base-12):\n            raise Boundary(\'actual pressed five-story JMP with its three original LONG slots required\')\n        jump=OriginalNarrativeResetJump(self,frame,self.state.sr,self.exit_site)\n        self.pending=jump;self.jumps+=1\n        self._jump_proof=(jump,self.state,frame,self.state.sr,self.exit_site,0x206,frame.stack_cursor.base)\n        self.state.events.append((\'original_narrative_jump\',self.exit_site,0x206,\n            frame.stack_cursor.base,self.state.sr))\n        raise jump\n\n    def main_scene_call(self,state,frame,target,continuation):\n        if (target,continuation)!=(0x4B4,0x3CE):\n            return (yield from super().main_scene_call(state,frame,target,continuation))\n        self.require_current(state)\n        if type(self)is not NarrativeScenePrograms or self.active or self.entered is not None:\n            raise Boundary(\'one exact actual Main4B4 narrative lifetime required\')\n        frame=_movement_frame(state,frame)\n        self.active=True;self.entered=frame\n        try:\n            return (yield from super().main_scene_call(state,frame,target,continuation))\n        except OriginalNarrativeResetJump as jump:\n            if type(jump)is not OriginalNarrativeResetJump or jump is not self.pending or jump.owner is not self:\n                raise Boundary(\'only this actual narrative lifetime may terminate with its own JMP\')\n            self.terminated=True;self.terminated_jump=jump\n            raise\n        finally:self.active=False\n\n    def _require_jump(self,jump):\n        self.require_current(self.state)\n        if (type(self)is not NarrativeScenePrograms or type(jump)is not OriginalNarrativeResetJump\n                or self.active or not self.terminated or self.terminated_jump is not jump\n                or jump.owner is not self or self.exit_site is not None\n                or jump is not self._jump_proof[0] or jump.frame is not self._jump_proof[2]\n                or (jump,jump.state,jump.frame,jump.full_sr,jump.source_pc,jump.target,\n                    jump.frame.stack_cursor.base)!=self._jump_proof\n                or jump.state is not self.state or jump.full_sr!=self.state.sr\n                or jump.frame.status!=(self.state.sr&31)):\n            raise Boundary(\'actual terminated unchanged Main4B4 jump proof required\')\n        return jump.frame\n\n    def claim(self,jump):\n        """Consume once only after the real source generator has unwound."""\n        frame=self._require_jump(jump)\n        if jump is not self.pending or self.claimed_jump is not None:\n            raise Boundary(\'one pending unclaimed original narrative transfer required\')\n        self.pending=None;self.claimed_jump=jump;self.claimed+=1\n        return frame\n\n    def require_claimed(self,jump):\n        """Read-only exact claimed proof for the new independent warm capture."""\n        frame=self._require_jump(jump)\n        if self.pending is not None or self.claimed_jump is not jump or self.claimed!=1:\n            raise Boundary(\'one actual already-claimed narrative JMP proof required\')\n        return frame', 'OriginalNarrativeResetJump': 'class OriginalNarrativeResetJump(Exception):\n    """An actual nonreturning JMP, not a new IRQ, RTS or reset completion."""\n    def __init__(self,owner,frame,full_sr,source_pc):\n        self.owner,self.state,self.frame=owner,owner.state,frame\n        self.full_sr,self.source_pc,self.target=full_sr,source_pc,0x206\n        super().__init__(\'original narrative JMP206 terminated its Main4B4 continuation\')'}}
_PLATFORM_METHODS = ('set_interrupt_vector','set_refresh','interrupt_control','interrupt_mode',
    'exchange_alternate_accumulator','exchange_alternate_group','read_refresh','memory_bit_conditions')


def _dump(node):
    return ast.dump(node, include_attributes=False)


def _code_shape(code):
    return tuple(getattr(code, name) for name in (
        'co_code','co_names','co_varnames','co_argcount','co_posonlyargcount',
        'co_kwonlyargcount','co_flags','co_freevars','co_cellvars')) + (tuple(
            _code_shape(value) if type(value) is CodeType else value for value in code.co_consts),)


def _named_code(parent, name):
    values = [value for value in parent.co_consts if type(value) is CodeType and value.co_name == name]
    if len(values) != 1:
        raise AudioBoundary('one complete retained-cold source code required: '+name)
    return values[0]


def _function_identity(module, function, expected_code, qualname, owner=None):
    closure_ok = type(function) is FunctionType and function.__closure__ is None and not function.__code__.co_freevars
    if type(function) is FunctionType and expected_code.co_freevars == ('__class__',):
        closure_ok = (owner is not None and function.__closure__ is not None
            and len(function.__closure__) == 1 and function.__closure__[0].cell_contents is owner)
    if (type(function) is not FunctionType or function.__globals__ is not vars(module)
            or function.__module__ != module.__name__ or function.__qualname__ != qualname
            or not closure_ok or _code_shape(function.__code__) != _code_shape(expected_code)):
        raise AudioBoundary('actual unwrapped retained-cold dependency required: '+qualname)


def _pin_source_owners():
    """Whole named source and recursive CodeType identity; execute no module."""
    bindings = []
    for path, expected in EXPECTED_SOURCE_OWNERS.items():
        module = importlib.import_module(path)
        tree = ast.parse(inspect.getsource(module), filename=module.__file__)
        plain = compile(tree, module.__file__, 'exec', dont_inherit=True)
        nodes = {node.name:node for node in tree.body if isinstance(node,(ast.FunctionDef,ast.ClassDef))}
        for name, text in expected.items():
            if name not in nodes or _dump(nodes[name]) != _dump(ast.parse(text).body[0]):
                raise AudioBoundary('complete original retained-cold source differs: '+name)
            actual = getattr(module,name)
            if isinstance(nodes[name],ast.FunctionDef):
                _function_identity(module,actual,_named_code(plain,name),name)
                bindings.append((module,name,actual,actual,actual.__code__))
                continue
            if type(actual) is not type or actual.__module__ != module.__name__ or actual.__name__ != name:
                raise AudioBoundary('exact complete retained-cold source class required: '+name)
            bindings.append((module,name,actual,None,actual.__bases__))
            class_code = _named_code(plain,name)
            for member in nodes[name].body:
                if not isinstance(member,ast.FunctionDef):
                    continue
                descriptor = vars(actual).get(member.name)
                function = descriptor.__func__ if type(descriptor) in (classmethod,staticmethod) else descriptor
                _function_identity(module,function,_named_code(class_code,member.name),name+'.'+member.name,actual)
                bindings.append((actual,member.name,descriptor,function,function.__code__))
    return tuple(bindings)


def _require_bindings(bindings):
    for owner,name,actual,function,code in bindings:
        if vars(owner).get(name) is not actual or (function is not None and function.__code__ is not code) \
                or (function is None and actual.__bases__ != code):
            raise AudioBoundary('retained-cold source owner changed: '+name)


def _callback(value):
    return getattr(value,'__self__',None), getattr(value,'__func__',value)


def _same_callback(left,right):
    a,b = _callback(left),_callback(right)
    return a[0] is b[0] and a[1] is b[1]


def _original_method(instance,name,owner):
    method = getattr(instance,name,None)
    if name in vars(instance) or getattr(method,'__self__',None) is not instance \
            or getattr(method,'__func__',None) is not getattr(owner,name):
        raise AudioBoundary('actual original retained platform method required: '+name)


@dataclass(frozen=True)
class ColdResetClaimWitness:
    """Read-only pending-object witness, captured before the original claim.

    It never claims, retires, resumes or grants anything. The old Intro owner
    intentionally retains only its counter after claim; this witness retains
    the actual exception identity without adding state to that original owner.
    """
    jump: object
    owner: object
    state: object
    frame: object
    full_sr: int
    source_pc: int
    target: int
    stack_pointer: int
    claimed_before: int
    jumps: int
    events: object
    event_count: int
    terminal_event: tuple
    bindings: tuple
    thread: int

    def require_claimed(self,jump):
        _require_bindings(self.bindings)
        owner,state = self.owner,self.state
        if (threading.get_ident() != self.thread or jump is not self.jump
                or jump.owner is not owner or jump.state is not state or jump.frame is not self.frame
                or (jump.full_sr,jump.source_pc,jump.target,jump.frame.stack_cursor.base)
                    != (self.full_sr,self.source_pc,self.target,self.stack_pointer)
                or state.sr != self.full_sr or jump.frame.status != state.sr & 31
                or owner.state is not state or owner.active or owner.pending is not None
                or owner.claimed != self.claimed_before+1 or owner.jumps != self.jumps
                or state.events is not self.events or len(state.events) != self.event_count
                or not state.events or state.events[-1] != self.terminal_event):
            raise AudioBoundary('the same actually claimed pending reset exception/frame/full SR required')
        if type(jump) is OriginalNarrativeResetJump and type(owner) is NarrativeScenePrograms:
            if owner.require_claimed(jump) is not self.frame:
                raise AudioBoundary('the original narrative claimed-object proof differs')
        elif type(jump) is OriginalIntroResetJump and type(owner) is IntroIrqPrograms:
            owner._guard()
        else:
            raise AudioBoundary('the witnessed exact original reset source changed')
        self.frame.validate(state,True)
        return self.frame


def capture_cold_reset_claim(jump):
    """Capture an actual pending JMP206 before its real owner.claim(jump)."""
    bindings = _pin_source_owners()
    if type(jump) not in (OriginalIntroResetJump,OriginalNarrativeResetJump):
        raise AudioBoundary('one actual typed pending original reset jump required')
    owner,state = jump.owner,jump.state
    if type(jump) is OriginalIntroResetJump:
        if type(owner) is not IntroIrqPrograms or jump.source_pc != 0x4786:
            raise AudioBoundary('exact pending intro source4786 required')
        owner._guard()
        event = ('original_nonreturning_jump',0x4786,0x206,jump.frame.stack_cursor.base,jump.full_sr)
    else:
        if type(owner) is not NarrativeScenePrograms:
            raise AudioBoundary('exact pending narrative source required')
        if owner._require_jump(jump) is not jump.frame or owner.claimed_jump is not None:
            raise AudioBoundary('the original terminated pending narrative proof is required')
        event = ('original_narrative_jump',jump.source_pc,0x206,jump.frame.stack_cursor.base,jump.full_sr)
    if (owner.state is not state or owner.active or owner.pending is not jump or jump.target != 0x206
            or jump.full_sr != state.sr or jump.frame.status != state.sr & 31
            or type(owner.claimed) is not int or type(owner.jumps) is not int
            or owner.claimed < 0 or owner.jumps != owner.claimed+1
            or not state.events or state.events[-1] != event):
        raise AudioBoundary('one original pending unclaimed jump must be the immediate Scene predecessor')
    jump.frame.validate(state,True)
    return ColdResetClaimWitness(jump,owner,state,jump.frame,jump.full_sr,jump.source_pc,jump.target,
        jump.frame.stack_cursor.base,owner.claimed,owner.jumps,state.events,len(state.events),event,
        bindings,threading.get_ident())


class RetainedColdWorkspaceCopyAuthority(AudioEntryAuthority):
    """Arm after real claim/retirement and before this exact reset.start().

    finish(release) validates this actual source/copy/control window. It grants
    no entry; control.acquire_frame('startup',0,authority=self) is still needed.
    The actual eight retired carriers are returned unchanged, never zero-seeded.
    """

    def __init__(self,sound,control,source,*,reset_session,retirement,jump,claim):
        if (type(sound) is not SoundDevice or sound.scene is None or type(control) is not AudioControlOwner
                or control.sound is not sound or type(source) is not CartridgeSourceData
                or sound.scene.data is not source.data or type(retirement) is not RetainedAudioCarriers
                or type(jump) not in (OriginalIntroResetJump,OriginalNarrativeResetJump)
                or type(claim) is not ColdResetClaimWitness or claim.jump is not jump
                or type(reset_session) is not CityColdResetSession or reset_session.state is not sound.scene
                or reset_session.started or reset_session.phase != 'not-started' or reset_session.failed
                or reset_session.entry is not jump.frame):
            raise ValueError('one same-Scene claimed jump/retirement/new unstarted city-reset/source required')
        if claim.require_claimed(jump) is not reset_session.entry:
            raise AudioBoundary('the same witnessed actual claim must supply this reset entry')
        self.bindings = claim.bindings
        retirement.require_retired(sound,control)
        reset_session._guard()
        state = sound.scene
        if (jump.state is not state or jump.target != 0x206 or jump.full_sr != state.sr
                or jump.frame.status != state.sr & 31):
            raise AudioBoundary('the actual unchanged claimed reset entry frame/full SR required')
        if type(jump) is OriginalNarrativeResetJump:
            if type(jump.owner) is not NarrativeScenePrograms or jump.owner.require_claimed(jump) is not jump.frame:
                raise AudioBoundary('one exact already-claimed narrative reset transfer required')
            event = ('original_narrative_jump',jump.source_pc,0x206,jump.frame.stack_cursor.base,jump.full_sr)
        elif type(jump) is OriginalIntroResetJump:
            owner = jump.owner
            if type(owner) is not IntroIrqPrograms:
                raise AudioBoundary('actual original intro IRQ provider required')
            owner._guard()
            if (owner.state is not state or owner.active or owner.pending is not None
                    or owner.claimed != owner.jumps or owner.claimed <= 0 or jump.source_pc != 0x4786):
                raise AudioBoundary('an actually claimed inactive intro transfer required')
            event = ('original_nonreturning_jump',0x4786,0x206,jump.frame.stack_cursor.base,jump.full_sr)
        else:
            raise AudioBoundary('only the two actual typed claimed JMP206 sources are admitted')
        if not state.events or state.events[-1] != event:
            raise AudioBoundary('the actual terminal jump must be the immediate Scene predecessor of this capture')
        audio,platform,bus = sound.audio_state,sound.audio_state.platform,sound.audio_state.bus
        if (type(audio) is not AudioState or type(platform) is not ExplicitAudioPlatform
                or platform.control_owner is not control or type(bus) is not SharedSoundAudioBus
                or bus.device is not sound or bus.ram is not sound.ram or type(bus.devices) is not OwnedAudioDeviceBus
                or bus.devices.material.data is not source.data or not callable(bus.devices.on_transfer)
                or getattr(bus.devices.psg_write,'__self__',None) is None):
            raise AudioBoundary('exact current Explicit platform/shared RAM/chips/full source material required')
        if (len(source.data.segments) != 1 or source.data.segments[0][0] != 0
                or len(source.data.segments[0][1]) != 0x100000
                or source.evidence.get('format') != 'g5510-explicit-complete-cartridge-source-DATA-v1'
                or source.evidence.get('original_ROM_or_bank_input') is not False):
            raise AudioBoundary('the same complete explicit readonly cartridge source is required')
        _original_method(audio,'indirect_transfer',AudioState)
        _original_method(platform,'indirect_transfer',ExplicitAudioPlatform)
        for name in _PLATFORM_METHODS:
            _original_method(platform,name,ExplicitAudioPlatform)
        word(platform.alternate_accumulator)
        if type(platform.alternate_group) is not AlternateGroup:
            raise AudioBoundary('actual retained alternate register group required')
        platform.alternate_group.validate()
        self.sound,self.control,self.source,self.scene = sound,control,source,state
        self.reset,self.retirement,self.jump,self.claim = reset_session,retirement,jump,claim
        self.entry,self.frame,self.jump_signature = reset_session.entry,retirement.frame,(jump.frame,jump.full_sr,jump.source_pc,jump.target)
        if type(self.frame) is not DriverFrame:
            raise AudioBoundary('the actual complete eight retired driver carriers are required')
        self.audio,self.platform,self.bus,self.devices = audio,platform,bus,bus.devices
        self.ram,self.hardware,self.data,self.segments = sound.ram,state.hardware,state.data,state.data.segments
        self.fm,self.psg = self.devices.fm,self.devices.psg_write.__self__
        self.fm_sink,self.psg_sink = self.fm.pcm_sink,self.psg.pcm_sink
        self.transfer,self.psg_write = self.devices.on_transfer,self.devices.psg_write
        self.refresh_reader,self.memory_bit_reader = platform.refresh_reader,platform.memory_bit_reader
        self.alternate_AF,self.alternate_group = platform.alternate_accumulator,platform.alternate_group
        self.schedule,self.scene_events,self.control_events = sound.schedule,state.events,control.events
        self.scene_start,self.control_start = len(state.events),len(control.events)
        self.epoch,self.generation,self.operations = sound.reset_epoch,control.generation,audio.data_operations
        self.pre_ram = bytes(sound.ram)
        self.pre_chips = self._chip_counters()
        self.factory,self.factory_code = reset_session.program_factory,reset_session.program_factory.__code__
        self.thread = threading.get_ident()
        self.release,self.evidence,self.handoff = None,None,None
        self.finished = self.used = self.failed = False

    def _chip_counters(self):
        return self.fm.tick,self.psg.tick,len(self.fm.events),len(self.psg.events)

    def _identities(self):
        _require_bindings(self.bindings)
        owner = self.retirement.owner
        if (self.failed or threading.get_ident() != self.thread or self.sound.scene is not self.scene
                or self.sound.audio_state is not self.audio or self.audio.bus is not self.bus
                or self.bus.device is not self.sound or self.bus.ram is not self.ram or self.sound.ram is not self.ram
                or self.bus.devices is not self.devices or self.devices.fm is not self.fm
                or self.devices.material.data is not self.data or self.scene.data is not self.data
                or self.source.data is not self.data or self.data.segments is not self.segments
                or self.scene.hardware is not self.hardware or self.sound.schedule is not self.schedule
                or self.control.sound is not self.sound or self.scene.events is not self.scene_events
                or self.control.events is not self.control_events or self.fm.pcm_sink is not self.fm_sink
                or self.psg.pcm_sink is not self.psg_sink or self.devices.on_transfer is not self.transfer
                or not _same_callback(self.devices.psg_write,self.psg_write)
                or self.reset.state is not self.scene or self.reset.entry is not self.entry
                or self.reset.program_factory is not self.factory or self.factory.__code__ is not self.factory_code
                or self.claim.jump is not self.jump or self.claim.frame is not self.entry
                or self.claim.bindings is not self.bindings
                or self.frame is not self.retirement.frame or self.frame is not self.retirement.point.frame
                or not owner.closed or owner.failed or owner.waiting is not self.retirement.point
                or owner.sound is not self.sound or owner.control is not self.control
                or owner.audio is not self.audio or owner._loop.irq_clock != self.retirement.irq_clock
                or owner._loop.irq_clock_hz != self.retirement.irq_clock_hz
                or (self.jump.frame,self.jump.full_sr,self.jump.source_pc,self.jump.target) != self.jump_signature):
            raise AudioBoundary('same retained cold Scene/source/RAM/chips/callbacks/entry ownership required')
        self.reset._guard()

    def _release_current(self,*,platform):
        self._identities()
        release,reset = self.release,self.reset
        if (type(release) is not ResetAudioReleasePoint or release.session is not reset or release.pc != 0x262
                or reset.waiting is not release or reset.phase != 'actual-audio-release' or not reset.started
                or reset.main_session is not None or reset._entered_main or self.scene.sr != release.full_sr
                or release.frame.status != release.full_sr & 31 or type(reset.program) is not GeneratorType
                or reset.program.gi_running or reset.program.gi_frame is None or reset.program.gi_code is not self.factory_code
                or self.sound.reset_epoch != self.epoch+1 or self.control.generation != self.generation+1
                or self.sound.executing or self.sound.reset_asserted or self.control.reset_asserted
                or self.sound.bus_requested or self.sound.m68k_granted
                or self.control.phase != 'startup-pending' or self.control._lease is not None or self.control._frame_session is not None
                or self.control.control != AudioControlState(0,0,0,False,False,0,False)
                or self.audio.data_operations != self.operations or self.audio.platform is not platform
                or self._chip_counters() != self.pre_chips):
            raise AudioBoundary('this actual released cold262/control epoch with unchanged suspended68000/audio required')
        release.frame.validate(self.scene,True)

    def finish(self,release):
        if self.finished or self.used or self.failed:
            raise AudioBoundary('one actual retained-cold copy window may be sealed once')
        try:
            self.release = release
            self._release_current(platform=self.platform)
            if (self.platform.alternate_accumulator != self.alternate_AF
                    or self.platform.alternate_group is not self.alternate_group
                    or self.platform.refresh_reader is not self.refresh_reader
                    or self.platform.memory_bit_reader is not self.memory_bit_reader):
                raise AudioBoundary('retained alternate registers/read callbacks changed before cold execution')
            events = self.scene_events
            positions = [index for index in range(self.scene_start,len(events))
                if events[index][:3] == ('read',0x2CA,1)]
            if len(positions) != 1:
                raise AudioBoundary('one new source2CA copy in this actual reset invocation required')
            start = positions[0]
            expected_ram = bytearray(self.pre_ram)
            write_indices = []
            for offset in range(38):
                value = self.data.read(0x2CA+offset,1)
                read,write = ('read',0x2CA+offset,1,value),('write',0xA00000+offset,1,value)
                index = start+2*offset
                if events[index:index+2] != [read,write]:
                    raise AudioBoundary('new actual cold38 source/read/write sequence differs at '+hex(offset))
                expected_ram[offset] = value
                write_indices.append(index+1)
            all_writes = [index for index in range(self.scene_start,len(events)) if events[index][0]=='write'
                and 0xA00000 <= (events[index][1]&0xFFFFFF) < 0xA02000]
            if all_writes != write_indices or bytes(self.ram) != bytes(expected_ram):
                raise AudioBoundary('additional/omitted sound writes or retained8192-byte RAM changed')
            prefix = [('write',0xA11100,2,0x100),('write',0xA11200,2,0x100)]
            suffix = [('write',0xA11200,2,0),('write',0xA11100,2,0),('write',0xA11200,2,0x100)]
            trace_indices = [index for index in range(self.scene_start,len(events))
                if events[index][0] in ('read','write') and events[index][1]&0xFFFFFF in (0xA11100,0xA11200)]
            trace = [events[index] for index in trace_indices]
            ack = trace[len(prefix):-len(suffix)]
            if (trace[:len(prefix)] != prefix or trace[-len(suffix):] != suffix or not ack
                    or any(event[:3] != ('read',0xA11100,1) for event in ack)
                    or any(not event[3]&1 for event in ack[:-1]) or ack[-1][3]&1
                    or not (trace_indices[len(prefix)+len(ack)-1] < start
                        and start+75 < trace_indices[-len(suffix)])
                    or events[-1] != suffix[-1]):
                raise AudioBoundary('actual24C/24E/BUSACK/copy/25C/25E/260 release order required')
            resets = [event for event in self.control_events[self.control_start:]
                if event[0] in ('reset_asserted','reset_released_pending')]
            if (len(resets) != 2 or tuple(resets[0][:3]) != ('reset_asserted',self.epoch,self.generation+1)
                    or tuple(resets[1][:3]) != ('reset_released_pending',self.epoch+1,self.generation+1)
                    or resets[1][3] < 3):
                raise AudioBoundary('exact one actual qualified relative-epoch cold reset release required')
            self.scene_end,self.control_end = len(events),len(self.control_events)
            self.sealed_ram = bytes(self.ram)
            self.finished = True
            self.evidence = dict(confidence='confirmed_actual_current_invocation_cold38_copy_and_release',
                source_start=0x2CA,source_end=0x2F0,bytes=38,Scene_window=[self.scene_start,self.scene_end],
                first_new_read_event=start,last_copy_write_event=start+75,
                actual_release_event=self.scene_end-1,previous_reset_epoch=self.epoch,previous_generation=self.generation,
                reset_epoch=self.epoch+1,generation=self.generation+1,actual_reset_transitions=resets,
                current_ram_8192_preserved_except_actual38_BYTE_copy=True,
                source_data_same_identity=True,entry_frame_is_actual_retired_frame=True,
                host_RAM_or_register_initialization=False,old_first_epoch_authority_modified=False,
                cold_budget_created=False,DATA_operations_at_capture=self.operations)
            return self
        except BaseException:
            self.failed = True
            raise

    def provide_frame(self,sound,entry_kind,entry_address,control_state):
        if not self.finished or self.used or type(self.handoff) is not RetainedColdPlatformWitness:
            raise AudioBoundary('sealed actual new copy and explicit platform handoff required before startup grant')
        self._release_current(platform=self.handoff.platform)
        self.handoff.require_attached(sound,self.control)
        if (sound is not self.sound or entry_kind != 'startup' or entry_address != 0
                or control_state is not self.control.control or len(self.scene_events) != self.scene_end
                or len(self.control_events) != self.control_end or bytes(self.ram) != self.sealed_ram):
            raise AudioBoundary('single unused current-window startup0 entry required, not a stale copy/lease')
        self.used = True
        return self.frame


@dataclass(frozen=True)
class RetainedColdPlatformWitness:
    authority: object
    previous_platform: object
    platform: object
    reset_epoch: int
    generation: int

    def require_attached(self,sound,control):
        authority = self.authority
        if type(authority) is not RetainedColdWorkspaceCopyAuthority:
            raise AudioBoundary('one exact retained-cold copy authority required')
        authority._identities()
        if (authority.handoff is not self or sound is not authority.sound or control is not authority.control
                or authority.audio.platform is not self.platform or type(self.platform) is not ColdWorkspacePlatform
                or self.platform.control_owner is not control or self.previous_platform is not authority.platform
                or sound.reset_epoch != self.reset_epoch or control.generation != self.generation):
            raise AudioBoundary('retained cold platform handoff is detached or belongs to another reset')
        return self.platform

    def describe(self):
        return dict(confidence='confirmed_explicit_same_AudioState_retained_cold_platform_commit',
            previous_platform_type='ExplicitAudioPlatform',current_platform_type='ColdWorkspacePlatform',
            reset_epoch=self.reset_epoch,generation=self.generation,same_Scene_RAM_chips_source_and_callbacks=True,
            cold_workspace_executed=False,startup_lease_granted=False,host_RAM_or_general_carrier_write=False,
            callback_budgets_extended=False,old_first_epoch_rules_changed=False)


def handoff_retained_cold_platform(sound,control,*,authority):
    """The sole ownership commit is the same AudioState.platform reference.

    No clocks, bus permissions, LDIR/DATA budget, cold session or idle is made
    here. The caller subsequently acquires startup0 and runs the old complete
    ColdWorkspaceSession using this exact new ColdWorkspacePlatform.
    """
    if type(authority) is not RetainedColdWorkspaceCopyAuthority or sound is not authority.sound \
            or control is not authority.control or not authority.finished or authority.used or authority.handoff is not None:
        raise AudioBoundary('one sealed unused exact retained-cold copy authority required')
    with continuations._SESSION_LOCK:
        authority._release_current(platform=authority.platform)
        if continuations._ACTIVE_SESSION is not None or len(authority.scene_events) != authority.scene_end \
                or len(authority.control_events) != authority.control_end or bytes(authority.ram) != authority.sealed_ram:
            raise AudioBoundary('a sealed unused copy window without concurrent audio execution required')
        old = authority.platform
        _original_method(authority.audio,'indirect_transfer',AudioState)
        _original_method(old,'indirect_transfer',ExplicitAudioPlatform)
        for name in _PLATFORM_METHODS:
            _original_method(old,name,ExplicitAudioPlatform)
        if (type(old) is not ExplicitAudioPlatform or old.control_owner is not control
                or old.alternate_accumulator != authority.alternate_AF or old.alternate_group is not authority.alternate_group
                or old.refresh_reader is not authority.refresh_reader or old.memory_bit_reader is not authority.memory_bit_reader):
            raise AudioBoundary('unchanged actual Explicit platform/alternate registers/provider callbacks required')
        new = ColdWorkspacePlatform(alternate_accumulator=old.alternate_accumulator,
            alternate_group=old.alternate_group,refresh_reader=old.refresh_reader,
            memory_bit_reader=old.memory_bit_reader,control_owner=control)
        witness = RetainedColdPlatformWitness(authority,old,new,sound.reset_epoch,control.generation)
        authority.audio.platform = new
        authority.handoff = witness
        return witness
