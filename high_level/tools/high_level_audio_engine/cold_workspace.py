"""Original cold38 workspace owner and its self-modified JP(HL) idle point.

The existing complete business function executes unchanged. This adapter owns
only its actual nonreturning indirect continuation and the same managed entry.
It does not interpret instructions, install a driver, clear RAM, push a return
word, infer clocks, or pretend the self-loop is an ordinary function return.
"""
import ast
from dataclasses import dataclass, fields
import inspect
import sys
import threading
from types import FunctionType

from tools.high_level_audio_engine import business_boot, target
from tools.high_level_audio_engine.contexts import InitializeAudioWorkspaceInput
from tools.high_level_audio_engine.control_reset import AudioEntryAuthority
from tools.high_level_audio_engine.domain import AudioBoundary, Continuation
from tools.high_level_audio_engine.hardware_scene import SoundDevice
from tools.high_level_audio_engine.owned_runtime import DriverFrame, ExplicitAudioPlatform
from tools.high_level_scene_flows.domain import ReadOnlyData


_CARRIERS = tuple(field.name for field in fields(DriverFrame))


def _whole_ast(node):
    if sys.version_info >= (3,13):
        return ast.dump(node,include_attributes=False,show_empty=True)
    return ast.dump(node,include_attributes=False)


def _actual_whole_workspace_owner():
    """Pin the complete current original owner, without changing its AST."""
    original = business_boot.initialize_audio_workspace
    if (type(original) is not FunctionType or original.__module__ != business_boot.__name__
            or original.__name__ != 'initialize_audio_workspace'
            or inspect.isgeneratorfunction(original)):
        raise AudioBoundary('actual complete cold-workspace owner required')
    module_source = inspect.getsource(business_boot)
    if _whole_ast(ast.parse(module_source)) != target.SOURCE_TREES['business_boot.py']:
        raise AudioBoundary('complete actual cold-workspace source contract differs')
    parsed = ast.parse(inspect.getsource(original))
    namespace = dict(vars(business_boot))
    exec(compile(parsed, '<unchanged whole cold-workspace owner identity>', 'exec'), namespace)
    plain = namespace[original.__name__]
    for attribute in ('co_code','co_consts','co_names','co_varnames','co_argcount','co_kwonlyargcount',
            'co_freevars','co_cellvars','co_flags'):
        if getattr(plain.__code__,attribute) != getattr(original.__code__,attribute):
            raise AudioBoundary('loaded cold-workspace callable differs from its whole source')
    return original


class ColdWorkspaceCopyAuthority(AudioEntryAuthority):
    """Actual original38-byte Scene copy at the first released reset epoch.

    This validates real same-Scene source-read/destination-write events and
    the resulting same sound RAM. It never installs CODE or seeds POP slots.
    File/source-build provenance belongs to the explicit source loader that
    supplied this Scene's ReadOnlyData, not to RAM's apparent byte pattern.
    """
    def __init__(self, sound, control, entry_frame, source_data):
        if (type(sound) is not SoundDevice or sound.scene is None
                or type(entry_frame) is not DriverFrame or type(source_data) is not ReadOnlyData
                or sound.audio_state.platform.control_owner is not control or control.sound is not sound
                or sound.scene.data is not source_data):
            raise ValueError('actual same-Scene sound/control, source DATA and complete entry frame required')
        self.sound, self.control, self.frame, self.source_data = sound, control, entry_frame, source_data
        self.evidence = None

    def provide_frame(self, sound, entry_kind, entry_address, control_state):
        if (sound is not self.sound or entry_kind != 'startup' or entry_address != 0
                or sound.reset_epoch != 1 or self.control.generation != 1
                or self.control.phase != 'startup-pending' or control_state.pc_entry != 0
                or sound.executing or sound.reset_asserted or sound.bus_requested or sound.m68k_granted):
            raise AudioBoundary('first actual released cold-workspace PC0 entry required')
        events = sound.scene.events
        source_index = next((index for index,event in enumerate(events)
            if event[:3] == ('read',0x2CA,1)), None)
        if source_index is None:
            raise AudioBoundary('original cold38 BYTE source copy has not occurred')
        copied = bytearray()
        for offset in range(38):
            pair = events[source_index+2*offset:source_index+2*offset+2]
            if len(pair) != 2:
                raise AudioBoundary('actual cold copy is incomplete')
            read, write = pair
            expected = self.source_data.read(0x2CA+offset,1)
            if (read != ('read',0x2CA+offset,1,expected)
                    or write != ('write',0xA00000+offset,1,expected)):
                raise AudioBoundary('actual source2CA/shared-RAM cold copy differs at ' + hex(offset))
            copied.append(expected)
        if bytes(sound.ram[:38]) != bytes(copied):
            raise AudioBoundary('the actual copied cold entry was overwritten before execution')
        if not events or events[-1] != ('write',0xA11200,2,0x100):
            raise AudioBoundary('cold execution grant requires the actual260 reset release write boundary')
        self.evidence = dict(confidence='confirmed_same_Scene_original38_BYTE_copy_and_epoch1_entry',
            source_start=0x2CA,source_end=0x2F0,bytes=38,
            original_source_read_event=source_index,reset_release_write_event=len(events)-1,
            actual_shared_RAM_copy=True, host_RAM_install=False, source_alias_to_driver69D2=False)
        return self.frame


@dataclass(frozen=True)
class ColdWorkspaceIdlePoint:
    session: object
    pc: int
    frame: DriverFrame
    generation: int
    reset_epoch: int
    kind: str = 'cold-workspace-self-modified-JP-HL-idle'


class _OriginalColdIdleTransfer(AudioBoundary):
    def __init__(self, point):
        self.point = point
        super().__init__('original cold workspace reached its nonreturning self-modified JP(HL) idle')


class ColdWorkspacePlatform(ExplicitAudioPlatform):
    """Supplied normal platform plus the sole original cold indirect tail.

    Alternate groups, reset/control, refresh and memory-BIT providers are still
    explicit constructor inputs inherited from ExplicitAudioPlatform. No global
    business callback or other platform object is replaced or monkeypatched.
    """
    def __init__(self, **explicit_inputs):
        super().__init__(**explicit_inputs)
        self.workspace_session = None

    def bind_workspace_session(self, session):
        if type(session) is not ColdWorkspaceSession or session.state.platform is not self:
            raise ValueError('one actual same-platform cold workspace session required')
        previous = self.workspace_session
        if (previous is not None and previous is not session
                and previous.control.generation == previous.generation
                and previous.sound.reset_epoch == previous.reset_epoch):
            raise AudioBoundary('another live cold-workspace continuation owns this platform')
        self.workspace_session = session

    def indirect_transfer(self, image, target_address, context):
        session = self.workspace_session
        if session is None:
            raise AudioBoundary('actual cold-workspace indirect continuation is unbound')
        return session._accept_original_idle(image,target_address,context)


class ColdWorkspaceSession:
    """One actual complete startup invocation ending at its real JP0 idle.

    The startup-kind managed frame claim stays owned by this cold session.
    finish_frame_session is deliberately NOT called: its driver-ready meaning
    is wrong for this self-loop. A subsequent genuine RESET invalidates the
    claim through the existing generation/epoch owner. Idle is not a RET, a
    driver lease, an opcode polling loop, a HALT instruction or enabled IRQ.
    """
    def __init__(self, sound, control, lease):
        if (type(sound) is not SoundDevice or sound.scene is None
                or type(sound.audio_state.platform) is not ColdWorkspacePlatform
                or sound.audio_state.platform.control_owner is not control or control.sound is not sound):
            raise ValueError('same bound sound/control and explicit ColdWorkspacePlatform required')
        if lease.entry_kind != 'startup' or control.phase != 'startup-authorized':
            raise AudioBoundary('actual cold-workspace startup-kind entry lease required, not driver PC0')
        control.require_frame(lease)
        self.sound, self.state, self.control, self.lease = sound,sound.audio_state,control,lease
        self.scene, self.generation, self.reset_epoch = sound.scene,lease.generation,lease.reset_epoch
        self.thread, self.original = threading.get_ident(),_actual_whole_workspace_owner()
        self.started = self.failed = False
        self.waiting = None
        self.events = []

    def _guard(self, *, executing):
        if (threading.get_ident() != self.thread or self.sound.scene is not self.scene
                or business_boot.initialize_audio_workspace is not self.original):
            raise AudioBoundary('cold-workspace owner/thread/Scene changed')
        if self.failed or self.sound.executing is not executing:
            raise AudioBoundary('cold-workspace execution grant is not at its actual boundary')
        if (self.sound.reset_asserted or self.sound.bus_requested or self.sound.m68k_granted
                or self.sound.reset_epoch != self.reset_epoch or self.control.generation != self.generation):
            raise AudioBoundary('cold-workspace continuation belongs to a reset or bus owner that has changed')

    def _accept_original_idle(self, image, target_address, context):
        self._guard(executing=True)
        self.control.require_frame_session(self,self.generation,self.reset_epoch)
        if image != 'startup' or target_address != 0 or type(context) is not InitializeAudioWorkspaceInput:
            raise AudioBoundary('original cold-workspace indirect target/context differs from JP(HL)0')
        context.validate(self.state)
        frame = DriverFrame(**{name:getattr(context,name) for name in _CARRIERS})
        if any(getattr(frame,name) != 0 for name in _CARRIERS):
            raise AudioBoundary('actual cold POP-cleared carriers/stack do not reach the JP0 idle contract')
        control = self.control.control
        if (self.sound.ram[0] != 0xE9 or control.interrupt_vector != 0
                or control.iff1 is not False or control.iff2 is not False
                or control.ei_deferred is not False or control.interrupt_mode != 1):
            raise AudioBoundary('actual self-modifying write or DI/IM1 control has not completed')
        point = ColdWorkspaceIdlePoint(self,0,frame,self.generation,self.reset_epoch)
        self.events.append(('actual_startup_0025_JP_HL_self_idle',0,frame.stack_cursor,
            self.sound.ram[0],self.generation,self.reset_epoch))
        raise _OriginalColdIdleTransfer(point)

    def start(self):
        self._guard(executing=False)
        if self.started:
            raise AudioBoundary('cold-workspace prefix cannot be replayed')
        frame = self.control.claim_frame_session(self.lease,self)
        self.state.platform.bind_workspace_session(self)
        self.started = True
        inputs = InitializeAudioWorkspaceInput(**{name:getattr(frame,name) for name in _CARRIERS},
            continuation=Continuation('startup',0))
        self.sound.executing = True
        try:
            self.original(self.state,inputs)
        except _OriginalColdIdleTransfer as transfer:
            point = transfer.point
            if point.session is not self or point.reset_epoch != self.reset_epoch:
                raise AudioBoundary('cold idle continuation belongs to another invocation')
            self.waiting = point
        except BaseException:
            self.failed = True
            self.control.abandon_frame_session(self,reason='original cold-workspace execution boundary')
            raise
        else:
            self.failed = True
            self.control.abandon_frame_session(self,reason='nonreturning cold workspace returned ordinarily')
            raise AudioBoundary('original cold workspace must not fabricate an ordinary return')
        finally:
            self.sound.executing = False
        return self.observe_idle()

    def observe_idle(self):
        """Expose the same actual self-loop; do not execute guessed JP cycles."""
        self._guard(executing=False)
        self.control.require_frame_session(self,self.generation,self.reset_epoch)
        if (self.waiting is None or self.waiting.session is not self
                or self.waiting.frame.lookup_cursor != 0 or self.sound.ram[0] != 0xE9):
            raise AudioBoundary('actual resident self-modified cold idle is no longer available')
        return self.waiting
