"""Cooperative original controller-setup/main-menu owner, without prefix replay.

confirmed: original 305B0..30694 and its BCC30656 -> 2AACE successor.
Scheduling supplies actual IRQ events; this module owns only software flow.
"""
from dataclasses import dataclass
from typing import Generator

from .domain import SceneState, Boundary, checked_state, uint, low8
from .contexts_gameplay import FirstDeploymentFrame, MovementContinuationBoundary
from .business_movement_support import _movement_frame


@dataclass(frozen=True)
class ControllerSetupWait:
    """Actual suspended TST/BNE, not a fabricated CALL or a copied machine."""
    state: SceneState
    frame: FirstDeploymentFrame
    poll: int

    def validate(self):
        checked_state(self.state)
        _movement_frame(self.state, self.frame)
        if self.poll not in (0x30648, 0x2AB6C):
            raise ValueError('actual controller/main-menu poll required')
        if self.frame.status != self.state.sr & 31:
            raise ValueError('suspended software CCR must agree with the same Scene SR')
        return self

    @property
    def stage(self):
        return 'controller_configuration' if self.poll == 0x30648 else 'main_menu'


def _wait_for_setup_irq_steps(state: SceneState, frame: FirstDeploymentFrame,
        poll: int) -> Generator[ControllerSetupWait, FirstDeploymentFrame, FirstDeploymentFrame]:
    """Arm once per actual software iteration; resume at the same real TST.

    30642/2AB66 write 0800 once. 30648/2AB6C only repeat the BYTE test while
    waiting; writing 0800 after RTE would erase the real handler's completion.
    """
    from .business_scene_support import _setup_write_fields, _movement_test
    if poll not in (0x30648, 0x2AB6C):
        raise ValueError('actual controller/main-menu IRQ poll required')
    frame = _setup_write_fields(state, frame, 0xFFFFF612, 0x800)
    while True:
        frame = _movement_test(state, frame, state.read(0xFFFFF612, 1), 8)
        if frame.status & 4:
            return frame
        frame = yield ControllerSetupWait(state, frame, poll).validate()
        _movement_frame(state, frame)


def controller_setup_program(state: SceneState,
        frame: FirstDeploymentFrame) -> Generator[ControllerSetupWait, FirstDeploymentFrame, FirstDeploymentFrame]:
    """Whole original owner; only its two wait sites cooperate with the host.

    The reversible source guard restores those two yield-from expressions to
    the old named wait calls and compares the complete original owner AST.
    No policy, byte width, CALL target/token, branch or ordering is changed.
    """
    from .business_scene_support import (
        _resource_cost_frame, _controller_setup_begin_fields,
        _setup_compare_memory_fields, _setup_call_fields, _movement_move,
        _setup_write_fields, _movement_test, _controller_setup_main_iteration_fields,
    )
    frame = _resource_cost_frame(state, frame, 0x305B0)
    frame = _controller_setup_begin_fields(state, frame, False)
    while True:
        frame = yield from _wait_for_setup_irq_steps(state, frame, 0x30648)
        frame = _setup_compare_memory_fields(state, frame, 0x00FF703A, 16)
        if not frame.status & 1:
            break
        frame = _setup_call_fields(state, frame, 0x306EE, 0x3065E)
        frame = _setup_call_fields(state, frame, 0x30696, 0x30664)
        frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF603, 1), 8)
        frame = _movement_move(state, frame, 'target_x', low8(frame.target_x) & 32, 8)
        if not frame.status & 4:
            frame = _setup_write_fields(state, frame, 0x00FF703E, 1)
            frame = _movement_move(state, frame, 'target_x', 0xAC, 8)
            frame = _setup_call_fields(state, frame, 0x808A, 0x30684)
        frame = _movement_test(state, frame, state.read(0x00FF703E, 2), 16)
        if not frame.status & 4:
            frame = _setup_call_fields(state, frame, 0x3071A, 0x30692)
    frame = _controller_setup_begin_fields(state, frame, True)
    while True:
        frame = yield from _wait_for_setup_irq_steps(state, frame, 0x2AB6C)
        frame, finished = _controller_setup_main_iteration_fields(state, frame)
        if finished:
            return frame


class ControllerSetupSession:
    """One suspended original invocation, retaining its Python and real RAM stack.

    A session has no clock, input defaults, CPU interpreter or copied RAM. The
    scheduler must deliver a genuine same-Scene IRQ and return its full frame
    at the same poll PC. Exhausted external events leave this session parked;
    start cannot be called twice to replay its initialization prefix.
    """
    def __init__(self, state: SceneState, frame: FirstDeploymentFrame):
        self.state = checked_state(state)
        self.entry = _movement_frame(state, frame)
        if frame.status != state.sr & 31:
            raise ValueError('owner entry frame and full Scene SR disagree')
        self._program = controller_setup_program(state, frame)
        self._started = self._complete = self._failed = False
        self.waiting = None
        self.result = None
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
            raise ValueError('software yielded no genuine same-Scene wait')
        self.waiting = waiting.validate()
        self.suspensions += 1
        return self.waiting

    def start(self):
        if self._started:
            raise ValueError('cannot replay controller/main-menu initialization prefix')
        self._started = True
        return self._take()

    def resume(self, returned: FirstDeploymentFrame, pc: int):
        if not self._started or self._complete or self._failed or self.waiting is None:
            raise ValueError('one live suspended controller/main-menu invocation required')
        returned = _movement_frame(self.state, returned)
        uint(pc, 32)
        if pc != self.waiting.poll:
            raise MovementContinuationBoundary(pc, returned,
                'IRQ did not return to this suspended controller/main-menu poll')
        if returned.stack_cursor.base != self.waiting.frame.stack_cursor.base:
            raise Boundary('IRQ return did not preserve the actual suspended owner SP')
        if returned.status != self.state.sr & 31:
            raise ValueError('actual IRQ return CCR and Scene SR disagree')
        return self._take(returned)


def run_controller_setup_blocking_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Compatibility facade exposes its real resumable invocation at the wait.

    The boundary is the established exact type, so physical upper CALL slots
    propagate unchanged. Its attached session resumes the already-entered
    owner. Completing this inner owner does not invent the outer caller's RTS.
    """
    session = ControllerSetupSession(state, frame)
    result = session.start()
    if type(result) is ControllerSetupWait:
        boundary = MovementContinuationBoundary(result.poll, result.frame,
            'original setup poll requires real asynchronous IRQ RAM progress')
        boundary.controller_setup_session = session
        boundary.controller_setup_wait = result
        raise boundary
    return result
