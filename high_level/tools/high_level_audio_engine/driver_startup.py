"""Persistent real driver-PC0 startup, with explicit IM1 grants to006F.

Only two typed suspension sites are added to a guarded view of the complete
existing business owner. No opcode execution, changed flags, global callee
replacement, assumed timer, cold-workspace substitution or invented RET.
"""
import ast
import copy
from dataclasses import dataclass, fields
import inspect
import threading
from types import FunctionType

from tools.high_level_audio_engine import business_hardware, business_loaders, contexts
from tools.high_level_audio_engine.domain import AudioBoundary, Continuation
from tools.high_level_audio_engine.hardware_scene import SoundDevice
from tools.high_level_audio_engine.owned_runtime import DriverFrame


_CARRIERS = tuple(field.name for field in fields(DriverFrame))


@dataclass(frozen=True)
class DriverStartupPoint:
    session: object
    pc: int
    frame: DriverFrame
    generation: int
    reset_epoch: int
    kind: str


@dataclass(frozen=True)
class Im1ClockGrant:
    timestamp: int
    clock_hz: int

    def __post_init__(self):
        if type(self.timestamp) is not int or self.timestamp < 0:
            raise ValueError('explicit nonnegative IRQ timestamp required')
        if type(self.clock_hz) is not int or self.clock_hz <= 0:
            raise ValueError('explicit positive IRQ clock frequency required')


def _dump(node):
    return ast.dump(node, include_attributes=False)


def _guarded_driver_view(point_factory, *, main_loop_points=False, timer_b_continuation=False):
    original = business_hardware.initialize_audio_driver
    if (type(original) is not FunctionType or original.__name__ != 'initialize_audio_driver'
            or original.__module__ != business_hardware.__name__ or inspect.isgeneratorfunction(original)):
        raise AudioBoundary('actual complete original driver startup owner required')
    source = inspect.getsource(original)
    parsed = ast.parse(source)
    if len(parsed.body) != 1 or type(parsed.body[0]) is not ast.FunctionDef:
        raise AudioBoundary('one complete original driver function required')
    # Compile a plain view first: stale/replaced source cannot stand in for
    # the actual currently loaded owner. This is no ROM/native/hash check.
    namespace = dict(vars(business_hardware))
    exec(compile(parsed, '<plain driver owner identity guard>', 'exec'), namespace)
    plain = namespace[original.__name__]
    for name in ('co_code', 'co_consts', 'co_names', 'co_varnames', 'co_argcount', 'co_kwonlyargcount'):
        if getattr(plain.__code__, name) != getattr(original.__code__, name):
            raise AudioBoundary('loaded original driver callable differs from its complete source')
    function = parsed.body[0]
    if any(isinstance(node, ast.Name) and node.id.startswith('_startup_') for node in ast.walk(function)):
        raise AudioBoundary('original owner competes with private suspension names')
    view = copy.deepcopy(function)
    wait_sites = [node for node in view.body if isinstance(node, ast.While)
        and len(node.body) >= 3
        and _dump(node.body[1]) == _dump(ast.parse('observed_byte_1 = state.read(8191)').body[0])
        and _dump(node.body[2]) == _dump(ast.parse('sample = u8(observed_byte_1)').body[0])]
    main_sites = [node for node in view.body if isinstance(node, ast.While)
        and len(node.body) >= 2 and isinstance(node.body[1], ast.ImportFrom)
        and node.body[1].module == 'business_mailbox'
        and [item.name for item in node.body[1].names] == ['poll_command_mailboxes']]
    if len(wait_sites) != 1 or len(main_sites) != 1:
        raise AudioBoundary('the two exact original startup/main suspension sites differ')
    timer_b_patch = None
    if timer_b_continuation:
        from tools.high_level_audio_engine.driver_timer_b import TimerBTailPatch
        timer_b_patch = TimerBTailPatch(view,main_sites[0],_CARRIERS)
    carriers = ', '.join(_CARRIERS)
    inserted = ast.parse('_startup_resumed = yield _startup_point(0x005F, DriverFrame(' + carriers + '))\n'
                         '(' + carriers + ') = _startup_carriers(_startup_resumed)').body
    ready = ast.parse('yield _startup_point(0x006F, DriverFrame(' + carriers + '))').body
    mailbox = []
    if main_loop_points:
        ready = ast.parse('_startup_resumed = yield _startup_point(0x006F, DriverFrame(' + carriers + '))\n'
            '(' + carriers + ') = _startup_carriers(_startup_resumed)').body
        mailbox = ast.parse('_startup_resumed = yield _startup_point(0x0073, DriverFrame(' + carriers + '))\n'
            '(' + carriers + ') = _startup_carriers(_startup_resumed)').body
        original_main = main_sites[0]
        read_sites = [index for index, statement in enumerate(original_main.body)
            if _dump(statement) == _dump(ast.parse('observed_byte_7 = state.read(7175)').body[0])]
        if len(read_sites) != 1:
            raise AudioBoundary('actual first mailbox RET/0073 owner differs')
        original_main.body[read_sites[0]:read_sites[0]] = copy.deepcopy(mailbox)
    timer_return = []
    if main_loop_points:
        timer_return = ast.parse('_startup_resumed = yield _startup_point(0x00A8, DriverFrame(' + carriers + '))\n'
            '(' + carriers + ') = _startup_carriers(_startup_resumed)').body
        timer_sites = []
        for block in ast.walk(view):
            body = getattr(block, 'body', None)
            if type(body) is list:
                for index, statement in enumerate(body):
                    if _dump(statement) == _dump(ast.parse('stack_cursor = updated_audio_values_15.stack_cursor').body[0]):
                        timer_sites.append((body,index))
        if len(timer_sites) != 1:
            raise AudioBoundary('actual timerA whole update return owner differs')
        timer_body,timer_index = timer_sites[0]
        timer_body[timer_index+1:timer_index+1] = copy.deepcopy(timer_return)
    wait_sites[0].body[3:3] = copy.deepcopy(inserted)
    main_sites[0].body[0:0] = copy.deepcopy(ready)
    # Complete-owner inverse, not just a snippet/signature/coverage assertion.
    inverse = copy.deepcopy(view)
    wait_inverse = [node for node in inverse.body if isinstance(node, ast.While)
        and len(node.body) >= 5 and _dump(node.body[3]) == _dump(inserted[0])]
    main_inverse = [node for node in inverse.body if isinstance(node, ast.While)
        and node.body and _dump(node.body[0]) == _dump(ready[0])]
    if len(wait_inverse) != 1 or len(main_inverse) != 1:
        raise AudioBoundary('driver suspension inverse sites differ')
    del wait_inverse[0].body[3:5]
    del main_inverse[0].body[:len(ready)]
    if mailbox:
        mailbox_inverse = [index for index, statement in enumerate(main_inverse[0].body)
            if _dump(statement) == _dump(mailbox[0])]
        if len(mailbox_inverse) != 1:
            raise AudioBoundary('actual mailbox continuation inverse differs')
        del main_inverse[0].body[mailbox_inverse[0]:mailbox_inverse[0]+len(mailbox)]
    if timer_return:
        timer_inverse = []
        for block in ast.walk(inverse):
            body = getattr(block, 'body', None)
            if type(body) is list:
                timer_inverse.extend((body,index) for index,statement in enumerate(body)
                    if _dump(statement) == _dump(timer_return[0]))
        if len(timer_inverse) != 1:
            raise AudioBoundary('actual timerA return inverse differs')
        timer_body,timer_index = timer_inverse[0]
        del timer_body[timer_index:timer_index+len(timer_return)]
    if timer_b_patch is not None:
        timer_b_patch.undo(inverse)
    if _dump(inverse) != _dump(function):
        raise AudioBoundary('driver view does not invert to the complete actual owner')
    namespace = dict(vars(business_hardware))
    namespace.update(DriverFrame=DriverFrame, _startup_point=point_factory,
                     _startup_carriers=lambda frame: tuple(getattr(frame, name) for name in _CARRIERS))
    module = ast.fix_missing_locations(ast.Module(body=[view], type_ignores=[]))
    exec(compile(module, '<reversible driver startup suspension view>', 'exec'), namespace)
    program = namespace[original.__name__]
    if not inspect.isgeneratorfunction(program):
        raise AudioBoundary('guarded owner view did not retain its typed suspensions')
    return original, program


class AudioDriverStartupSession:
    """One same-Scene driver entry and three real countdown IRQs, no CPU loop.

    Requires an actual managed DRIVER entry lease supplied after installation.
    A cold-workspace lease is rejected. IRQ timestamps are explicitly supplied
    external events, not inferred frame cadence, FM busy clocks or cycle costs.
    """
    def __init__(self, sound, control, lease, *, irq_clock_hz, initial_irq_clock, main_loop_points=False, timer_b_continuation=False):
        if type(sound) is not SoundDevice or sound.scene is None:
            raise ValueError('one actual Scene-bound sound owner required')
        if sound.audio_state.platform.control_owner is not control or control.sound is not sound:
            raise ValueError('same explicitly bound control owner required')
        if (type(irq_clock_hz) is not int or irq_clock_hz <= 0
                or type(initial_irq_clock) is not int or initial_irq_clock < 0):
            raise ValueError('explicit IRQ clock frequency and initial timestamp required')
        if lease.entry_kind != 'driver':
            raise AudioBoundary('cold workspace PC0 is not the installed driver PC0')
        control.require_frame(lease)
        self.sound, self.state, self.control, self.lease = sound, sound.audio_state, control, lease
        self.scene = sound.scene
        self.generation, self.reset_epoch = lease.generation, lease.reset_epoch
        self.irq_clock_hz, self.irq_clock = irq_clock_hz, initial_irq_clock
        self.thread = threading.get_ident()
        if type(main_loop_points) is not bool:
            raise ValueError('explicit opt-in main loop suspension choice required')
        self.main_loop_points = main_loop_points
        if type(timer_b_continuation) is not bool or (timer_b_continuation and not main_loop_points):
            raise ValueError('explicit Timer-B continuation requires main-loop points')
        self.timer_b_continuation = timer_b_continuation
        self.original, self.program_factory = _guarded_driver_view(self._point, main_loop_points=main_loop_points, timer_b_continuation=timer_b_continuation)
        self.owners = ((business_hardware, 'initialize_audio_driver', self.original),
            (business_hardware, 'service_im1_interrupt', business_hardware.service_im1_interrupt),
            (business_hardware, 'program_timer_a', business_hardware.program_timer_a),
            (business_hardware, 'program_timer_b', business_hardware.program_timer_b),
            (business_loaders, 'clear_and_reset_driver', business_loaders.clear_and_reset_driver),
            (business_loaders, 'initialize_audio_bank', business_loaders.initialize_audio_bank))
        self.program = self.waiting = self.ready_lease = None
        self.started = self.failed = self.closed = False
        self.events = []

    def _guard(self):
        if threading.get_ident() != self.thread or self.sound.scene is not self.scene:
            raise AudioBoundary('driver startup session belongs to another thread/Scene')
        if any(getattr(module, name) is not function for module, name, function in self.owners):
            raise AudioBoundary('actual named startup callee owner changed')
        if self.failed or self.closed:
            raise AudioBoundary('failed/closed driver startup continuation cannot resume')
        if (self.sound.executing or self.sound.reset_epoch != self.reset_epoch or self.control.generation != self.generation
                or self.sound.reset_asserted or self.sound.bus_requested or self.sound.m68k_granted):
            raise AudioBoundary('startup execution grant belongs to another reset or bus owner')

    def _point(self, pc, frame):
        if pc not in ((0x005f,0x006f,0x0073,0x009b,0x00a8) if self.timer_b_continuation else ((0x005f,0x006f,0x0073,0x00a8) if self.main_loop_points else (0x005f,0x006f))) or type(frame) is not DriverFrame:
            raise AudioBoundary('actual finite driver point and complete frame required')
        return DriverStartupPoint(self, pc, frame, self.generation, self.reset_epoch,
                                  {0x005f:'countdown',0x006f:'main-loop-boundary',0x0073:'mailbox-return',0x009b:'timerB-SFX-return',0x00a8:'timerA-update-return'}[pc])

    def _advance(self, resumed=None):
        self._guard()
        self.control.require_frame_session(self, self.generation, self.reset_epoch)
        try:
            while True:
                self.sound.executing = True
                try:
                    point = next(self.program) if resumed is None else self.program.send(resumed)
                finally:
                    self.sound.executing = False
                if type(point) is not DriverStartupPoint or point.session is not self:
                    raise AudioBoundary('startup yielded a foreign typed continuation')
                self.waiting = point
                if point.pc == 0x006f:
                    self.ready_lease = self.control.finish_frame_session(self, self.generation,
                        self.reset_epoch, point.frame)
                    self.events.append(('original_main_loop_boundary', 0x006f, point.frame.stack_cursor))
                    return point
                # The original LD at005C, immediately following EI, has really
                # executed before this point. No arbitrary Python call clears EI.
                self.control.complete_ei_following_instruction(generation=self.generation,
                                                               reset_epoch=self.reset_epoch)
                self.events.append(('actual_005C_LD_completed', point.frame.sample,
                                    point.frame.stack_cursor))
                if point.frame.sample != 0:
                    return point
                # With no externally supplied IRQ at this point, the original
                # OR/JP sees its real zero sample and continues initialization.
                resumed = point.frame
        except BaseException:
            self.failed = True
            self.control.abandon_frame_session(self, reason='driver startup execution boundary')
            raise

    def start(self):
        self._guard()
        if self.started:
            raise AudioBoundary('original driver startup cannot replay its prefix')
        frame = self.control.claim_frame_session(self.lease, self)
        self.started = True
        values = {name: getattr(frame, name) for name in _CARRIERS}
        # This original owner does not return before006F. A continuation field
        # is carried for its ABI only; no return WORD is pushed or fabricated.
        inputs = contexts.InitializeAudioDriverInput(**values, continuation=Continuation('driver', 0))
        self.program = self.program_factory(self.state, inputs)
        return self._advance()

    def deliver_im1(self, grant):
        self._guard()
        if not self.started or self.waiting is None or self.waiting.pc != 0x005f:
            raise AudioBoundary('IM1 grant requires the actual countdown instruction boundary')
        if (type(grant) is not Im1ClockGrant or grant.clock_hz != self.irq_clock_hz
                or grant.timestamp <= self.irq_clock):
            raise AudioBoundary('explicit matching monotonic external IM1 clock grant required')
        self.control.require_frame_session(self, self.generation, self.reset_epoch)
        frame = self.waiting.frame
        self.sound.executing = True
        try:
            self.control.accept_session_im1(self, self.generation, self.reset_epoch)
            self.irq_clock = grant.timestamp
            before = self.state.read(0x1fff)
            stack = self.state.push_word(frame.stack_cursor, self.waiting.pc)
            values = {name: getattr(frame, name) for name in _CARRIERS}
            values['stack_cursor'] = stack
            returned = business_hardware.service_im1_interrupt(self.state,
                contexts.ServiceIm1InterruptInput(**values,
                    continuation=Continuation('driver', self.waiting.pc)))
            result = DriverFrame(**{name: getattr(returned, name) for name in _CARRIERS})
            if result.stack_cursor != frame.stack_cursor or result != frame:
                raise AudioBoundary('real countdown IRQ did not restore its complete interrupted frame')
            after = self.state.read(0x1fff)
            self.events.append(('actual_IM1', grant.timestamp, grant.clock_hz, self.waiting.pc,
                                frame.stack_cursor, stack, before, after))
            # The service's real EI at0051 was followed by the actual RET0052.
            self.control.complete_ei_following_instruction(generation=self.generation,
                                                           reset_epoch=self.reset_epoch)
        except BaseException:
            self.failed = True
            self.control.abandon_frame_session(self, reason='real IM1 delivery boundary')
            raise
        finally:
            self.sound.executing = False
        return self._advance(result)

    def close(self):
        if threading.get_ident() != self.thread:
            raise AudioBoundary('only the owning thread may close its startup continuation')
        if self.program is not None:
            self.program.close()
        self.control.abandon_frame_session(self, reason='startup session explicitly closed')
        self.closed = True
