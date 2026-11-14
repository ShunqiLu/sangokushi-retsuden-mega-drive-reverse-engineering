"""Installed original driver loop, real mailbox RET and externally granted IM1.

Consumes the actual PC006F continuation produced by driver_startup. The same
source-derived generator retains all original control flow; no prefix replay,
host poll/update pair, CPU instruction interpreter or fake return is added.
"""
from dataclasses import fields
import threading

from tools.high_level_audio_engine import business_hardware, business_mailbox, continuations, contexts
from tools.high_level_audio_engine.domain import AudioBoundary, Continuation
from tools.high_level_audio_engine.owned_runtime import DriverFrame
from tools.high_level_audio_engine import driver_startup


_CARRIERS = tuple(field.name for field in fields(DriverFrame))
_IRQ_SAVED = ('conditions','count_and_data','lookup_cursor','parameter_cursor','sample','stack_cursor')


class AudioDriverLoopSession:
    """Linear takeover of the real installed-driver ready frame and generator.

    This adapter runs only to source-derived006F/0073/00A8 instruction boundaries.
    An IM1 is accepted only at0073 after the real EI/CALL/poll/RET completed.
    Neither IRQ clocks nor LD A,R observations or chip timer flags are supplied
    here. The caller must own every such platform/device input explicitly.
    """
    def __init__(self, startup, *, startup_api=driver_startup):
        if (type(startup) is not startup_api.AudioDriverStartupSession
                or not startup.main_loop_points or startup.closed or startup.failed
                or startup.waiting is None or startup.waiting.pc != 0x006f
                or startup.program is None or startup.ready_lease is None):
            raise AudioBoundary('actual opt-in persistent startup at006F required')
        startup._guard()
        if startup.control.require_frame(startup.ready_lease) != startup.waiting.frame:
            raise AudioBoundary('ready lease differs from the actual generator frame')
        self.startup_api = startup_api
        self.origin, self.sound, self.state = startup, startup.sound, startup.state
        self.control, self.scene = startup.control, startup.scene
        self.generation, self.reset_epoch = startup.generation, startup.reset_epoch
        self.irq_clock_hz, self.irq_clock = startup.irq_clock_hz, startup.irq_clock
        self.thread = threading.get_ident()
        self.owners = startup.owners + (
            (business_mailbox,'poll_command_mailboxes',business_mailbox.poll_command_mailboxes),
            (business_hardware,'update_audio_driver',business_hardware.update_audio_driver))
        self.failed = self.closed = False
        self.events, self.continuation_events = [], []
        self.waiting = startup.waiting
        self.program = None
        self.control.claim_frame_session(startup.ready_lease,self)
        self.program, startup.program = startup.program, None
        startup.closed = True  # It no longer owns or can close this generator.
        self.events.append(('actual_generator_handoff',0x006f,self.waiting.frame.stack_cursor,
                            self.generation,self.reset_epoch))

    def _guard(self):
        if (self.closed or self.failed or threading.get_ident()!=self.thread
                or self.sound.scene is not self.scene or self.sound.audio_state is not self.state):
            raise AudioBoundary('closed/failed/foreign original driver loop owner')
        if any(getattr(module,name) is not function for module,name,function in self.owners):
            raise AudioBoundary('actual loop callee binding differs outside its finite scope')
        if (self.sound.executing or self.sound.bus_requested or self.sound.m68k_granted
                or self.sound.reset_asserted):
            raise AudioBoundary('original driver loop requires its released sound execution grant')
        self.control.require_frame_session(self,self.generation,self.reset_epoch)

    def _fail(self, reason):
        self.failed = True
        self.control.abandon_frame_session(self,reason=reason)

    def advance(self):
        """Execute original instructions to the next006F,0073 or00A8 point."""
        self._guard()
        before = self.waiting
        adapter=continuations.AudioContinuationSession(self.sound,before.frame)
        try:
            with adapter:
                self.sound.executing=True
                try:
                    point = self.program.send(before.frame)
                finally:
                    self.sound.executing=False
            if (type(point) is not self.startup_api.DriverStartupPoint
                    or point.session is not self.origin or point.pc not in ((0x006f,0x0073,0x009b,0x00a8) if self.origin.timer_b_continuation else (0x006f,0x0073,0x00a8))
                    or point.generation!=self.generation or point.reset_epoch!=self.reset_epoch):
                raise AudioBoundary('original driver yielded an unowned finite continuation')
            self.waiting=point
            if point.pc==0x0073:
                # CALL0070 is the actual completed instruction after EI006F;
                # all of its original polling instructions and RET really ran.
                self.control.complete_ei_following_instruction(generation=self.generation,
                    reset_epoch=self.reset_epoch)
                self.events.append(('actual_mailbox_RET',0x0073,point.frame.stack_cursor))
            elif point.pc==0x009b:
                self.events.append(('actual_timer_B_SFX_return',0x009b,point.frame.stack_cursor))
            elif point.pc==0x00a8:
                self.events.append(('actual_timer_A_whole_update_return',0x00a8,point.frame.stack_cursor))
            else:
                self.events.append(('actual_main_loop_branch',0x006f,point.frame.stack_cursor))
            return point
        except StopIteration as error:
            self._fail('original main branch left its registered loop continuation')
            raise AudioBoundary('original main branch requires its next typed owner') from error
        except BaseException:
            self._fail('actual main loop execution boundary')
            raise
        finally:
            self.sound.executing=False
            self.continuation_events.extend(adapter.events)

    def deliver_im1(self, grant):
        """Run the real handler, including its conditional whole00E5 update."""
        self._guard()
        if self.waiting.pc!=0x0073:
            raise AudioBoundary('IM1 requires the actual completed mailbox CALL boundary0073')
        if (type(grant) is not self.startup_api.Im1ClockGrant
                or grant.clock_hz!=self.irq_clock_hz or grant.timestamp<=self.irq_clock):
            raise AudioBoundary('explicit matching monotonic external IM1 grant required')
        frame=self.waiting.frame
        adapter=continuations.AudioContinuationSession(self.sound,frame)
        try:
            with adapter:
                self.sound.executing=True
                try:
                    self.control.accept_session_im1(self,self.generation,self.reset_epoch)
                    self.irq_clock=grant.timestamp
                    before_count=self.state.read(0x1fff)
                    mode=self.state.read(0x1c07)
                    stack=self.state.push_word(frame.stack_cursor,0x0073)
                    values={name:getattr(frame,name) for name in _CARRIERS}
                    values['stack_cursor']=stack
                    result=business_hardware.service_im1_interrupt(self.state,
                        contexts.ServiceIm1InterruptInput(**values,continuation=Continuation('driver',0x0073)))
                    returned=DriverFrame(**{name:getattr(result,name) for name in _CARRIERS})
                    if any(getattr(returned,name)!=getattr(frame,name) for name in _IRQ_SAVED):
                        raise AudioBoundary('real IM1 failed to restore its actual saved AF/BC/DE/HL/SP')
                    # IX/IY are not pushed by0038; retain real update changes.
                    self.waiting=self.startup_api.DriverStartupPoint(self.origin,0x0073,returned,
                        self.generation,self.reset_epoch,'mailbox-return')
                    after_count=self.state.read(0x1fff)
                    self.control.complete_ei_following_instruction(generation=self.generation,
                        reset_epoch=self.reset_epoch)  # Original EI0051/RET0052.
                    self.events.append(('actual_IM1',grant.timestamp,grant.clock_hz,0x0073,
                        frame.stack_cursor,stack,before_count,after_count,mode,
                        'whole_update' if before_count==0 and mode==0 else 'original_conditional_no_update'))
                finally:
                    self.sound.executing=False
        except BaseException:
            self._fail('actual main-loop IM1/whole-update boundary')
            raise
        finally:
            self.continuation_events.extend(adapter.events)
        if any(getattr(module,name) is not original for module,name,original in adapter.originals):
            self._fail('scoped continuation binding restoration boundary')
            raise AudioBoundary('actual whole update did not restore its finite callee scope')
        return self.waiting

    def close(self):
        if threading.get_ident()!=self.thread:
            raise AudioBoundary('only the actual loop owner thread may close it')
        if not self.closed:
            self.program.close()
            self.control.abandon_frame_session(self,reason='driver loop explicitly closed')
            self.closed=True
