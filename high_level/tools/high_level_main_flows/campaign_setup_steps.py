"""Cooperative original 04B0 -> 0514 new-campaign caller.

confirmed: the historical post-duel label is not semantic authority.  The
original caller invokes controller setup/main menu, commits the chosen game
options, then restores the scenario descriptors and initial campaign state.
"""
from typing import Generator

from .domain import SceneState, Boundary, checked_state, uint
from .contexts_gameplay import (
    FirstDeploymentFrame, FirstDeploymentReturnBoundary,
    MovementContinuationBoundary, first_replace,
)
from .business_movement_support import _movement_frame
from .controller_setup_steps import ControllerSetupSession, ControllerSetupWait


def _campaign_setup_menu_call_steps(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> Generator[ControllerSetupWait, FirstDeploymentFrame, FirstDeploymentFrame]:
    """The one real JSR305B0/return528 stays physically live across all IRQs.

    This is the ordinary campaign call's push/validate/pop sequence.  Only the
    child invocation cooperates: its own Session resumes the exact suspended
    TST.  No exception is caught and interpreted as a successful child return.
    """
    from .business_commands import _city_ui_frame_fields
    if (target, continuation) != (0x305B0, 0x528):
        raise ValueError('only original campaign setup JSR/return pair required')
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    child = ControllerSetupSession(state, entered)
    returned = child.start()
    while type(returned) is ControllerSetupWait:
        waiting = returned
        irq_frame = yield waiting
        returned = child.resume(irq_frame, waiting.poll)
    returned = _city_ui_frame_fields(state, returned, target)
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise FirstDeploymentReturnBoundary(actual, returned, continuation)
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))


def campaign_setup_program(state: SceneState,
        frame: FirstDeploymentFrame) -> Generator[ControllerSetupWait, FirstDeploymentFrame, FirstDeploymentFrame]:
    """Whole original 0514 owner, with exactly one cooperative child call.

    The complete inverse AST guard restores this one yield-from to the old
    _campaign_call_fields.  All following original CALLs, writes and widths
    remain unchanged.  Completion is before original554 RTS: the caller's
    incoming LONG is retained for its actual caller, never popped here.
    """
    from .business_main import (
        _campaign_screen_enter_fields, _movement_move, _campaign_call_fields,
        _campaign_emit_fields,
    )
    frame = _campaign_screen_enter_fields(state, frame, 0x4B0)
    frame = _movement_move(state, frame, 'target_x', 134, 16)
    frame = _campaign_call_fields(state, frame, 0x808A, 0x522)
    frame = yield from _campaign_setup_menu_call_steps(state, frame, 0x305B0, 0x528)
    state.sr = 0x2700
    frame = first_replace(frame, status=0)
    frame = _campaign_call_fields(state, frame, 0x6826, 0x532)
    frame = _campaign_call_fields(state, frame, 0x3076E, 0x538)
    frame = _campaign_emit_fields(state, frame, 0x538, 0xFFFFF612, 512)
    frame = _campaign_emit_fields(state, frame, 0x53E, 0xFFFFF352, 0, clear=True)
    frame = _campaign_call_fields(state, frame, 0x3E54, 0x548)
    frame = _campaign_call_fields(state, frame, 0x9390, 0x54E)
    return _campaign_call_fields(state, frame, 0x15BE, 0x554)


class CampaignSetupSession:
    """One live original new-game caller, not a menu-result reconstruction.

    Waiting exposes the existing exact child Wait for delivery through the
    original IRQ adapter.  Both Python continuations and the physical528
    return LONG remain live.  Missing DATA/hardware after menu return is a
    preserved failure, not a replayable wait or fabricated outer RTS.
    """
    completion_pc = 0x554

    def __init__(self, state: SceneState, frame: FirstDeploymentFrame):
        self.state = checked_state(state)
        self.entry = _movement_frame(state, frame)
        if frame.status != state.sr & 31:
            raise ValueError('campaign entry frame and full Scene SR disagree')
        self._program = campaign_setup_program(state, frame)
        self._started = self._complete = self._failed = False
        self.waiting = self.result = None
        self.suspensions = 0

    @property
    def complete(self):
        return self._complete

    def _take(self, received=None):
        try:
            waiting = next(self._program) if received is None else self._program.send(received)
        except StopIteration as finished:
            self.result = _movement_frame(self.state, finished.value)
            self.waiting, self._complete = None, True
            return self.result
        except BaseException:
            self._failed = True
            raise
        if type(waiting) is not ControllerSetupWait or waiting.state is not self.state:
            self._failed = True
            raise ValueError('campaign child yielded no genuine same-Scene wait')
        self.waiting = waiting.validate()
        self.suspensions += 1
        return self.waiting

    def start(self):
        if self._started:
            raise ValueError('cannot replay the original campaign setup prefix')
        self._started = True
        return self._take()

    def resume(self, returned: FirstDeploymentFrame, pc: int):
        if not self._started or self._complete or self._failed or self.waiting is None:
            raise ValueError('one live suspended campaign setup invocation required')
        returned = _movement_frame(self.state, returned)
        uint(pc, 32)
        if pc != self.waiting.poll:
            raise MovementContinuationBoundary(pc, returned,
                'IRQ did not return to this suspended campaign child poll')
        if returned.stack_cursor.base != self.waiting.frame.stack_cursor.base:
            raise Boundary('IRQ return did not preserve actual campaign child SP')
        if returned.status != self.state.sr & 31:
            raise ValueError('actual IRQ return CCR and Scene SR disagree')
        return self._take(returned)


def run_campaign_setup_blocking_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Compatibility facade retains the original caller and child continuations."""
    session = CampaignSetupSession(state, frame)
    result = session.start()
    if type(result) is ControllerSetupWait:
        boundary = MovementContinuationBoundary(result.poll, result.frame,
            'original campaign setup requires real asynchronous child IRQ progress')
        boundary.campaign_setup_session = session
        boundary.controller_setup_wait = result
        raise boundary
    return result
