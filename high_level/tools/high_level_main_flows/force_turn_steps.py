"""Persistent original first-force turn and its30A90 message wait.

Confirmed0484/30960/30A74 whole owners keep the same Scene, full frame,
original CALL LONGs, two saved WORDs, SR and continuation order. Only the
actual asynchronous request wait yields; all device timing is external.
"""
from dataclasses import dataclass
from .command_message_steps import (command_assignment_call_program,
    command_second_force_program, command_finish_assignment_call_program)
from .domain import SceneState, Boundary, checked_state, uint
from .contexts_gameplay import FirstDeploymentFrame, FirstDeploymentReturnBoundary, MovementContinuationBoundary, first_replace
from .business_movement_support import _movement_frame
from .business_main import _campaign_call_fields
from .contexts_display_fields import display_frame_fields, display_call_fields, display_move_fields, display_store_fields
from .business_commands import _city_ui_frame_fields, _diplomacy_second_force_turn_fields, _diplomacy_owner_matches_fields, _diplomacy_show_owner_packet_fields
from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory, SceneRefreshBoundary, _first_compare_word
from ..high_level_gameplay_flow.business_services import _scene_refresh_frame, _scene_refresh_flags, _scene_refresh_emit, _gameplay_message_call_fields

@dataclass(frozen=True)
class ForceTurnWait:
    state: SceneState
    frame: FirstDeploymentFrame
    poll: int = 199312

    def validate(self):
        checked_state(self.state)
        _movement_frame(self.state, self.frame)
        if self.poll != 199312:
            raise ValueError('actual first-force message wait required')
        if self.frame.status != self.state.sr & 31:
            raise ValueError('force-turn full Scene SR and software CCR disagree')
        return self

    @property
    def stage(self):
        return 'original_force_turn_message'

def _force_turn_message_call_steps(state, frame, target, continuation):
    """Original3099C LONG remains below the two actual saved WORDs."""
    if (target, continuation) != (199284, 199068):
        raise ValueError('actual first-force message CALL pair required')
    frame = display_frame_fields(state, frame)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    returned = (yield from force_turn_message_program(SceneRefreshMemory(state), entered))
    returned = display_frame_fields(state, returned)
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise MovementContinuationBoundary(actual, returned, 'original message return changed')
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))

def _force_turn_owner_call_steps(state, frame, target, continuation):
    """Only actual30960/D56 adapts; no parent slot is fabricated at yield."""
    if (target, continuation) != (199008, 3414):
        raise ValueError('actual0484 first-force CALL pair required')
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    returned = (yield from force_turn_first_program(state, entered, True))
    returned = _city_ui_frame_fields(state, returned, target)
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise FirstDeploymentReturnBoundary(actual, returned, continuation)
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))

class ForceTurnSession:
    """One0484 caller invocation; completed result still owns its incoming3CE."""

    def __init__(self, state, frame):
        self.state = checked_state(state)
        self.entry = _movement_frame(state, frame)
        if frame.status != state.sr & 31:
            raise ValueError('force-turn entry CCR and full SR disagree')
        self._program = force_turn_screen_program(state, frame)
        self._started = self._complete = self._failed = False
        self.waiting = self.result = None
        self.suspensions = 0

    def _take(self, received=None):
        try:
            waiting = next(self._program) if received is None else self._program.send(received)
        except StopIteration as finished:
            self.result = _movement_frame(self.state, finished.value)
            self.waiting, self._complete = (None, True)
            return self.result
        except BaseException:
            self._failed = True
            raise
        if type(waiting) is not ForceTurnWait or waiting.state is not self.state:
            self._failed = True
            raise ValueError('one actual same-Scene force-turn wait required')
        self.waiting = waiting.validate()
        self.suspensions += 1
        return self.waiting

    def start(self):
        if self._started:
            raise ValueError('cannot replay0484/30960 force-turn prefix')
        self._started = True
        return self._take()

    def resume(self, returned, pc):
        if not self._started or self._complete or self._failed or (self.waiting is None):
            raise ValueError('one live suspended force-turn invocation required')
        returned = _movement_frame(self.state, returned)
        uint(pc, 32)
        if pc != self.waiting.poll:
            raise MovementContinuationBoundary(pc, returned, 'IRQ did not return to original30A90')
        if returned.stack_cursor.base != self.waiting.frame.stack_cursor.base:
            raise Boundary('IRQ did not preserve force-turn saved WORDs and CALL stack')
        if returned.status != self.state.sr & 31:
            raise ValueError('actual IRQ return CCR and Scene SR disagree')
        return self._take(returned)

def force_turn_screen_program(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """484: initialize support command screen; original stage and child tokens."""
    frame = _city_ui_frame_fields(state, frame, 1156)
    state.sr = 9984
    frame = first_replace(frame, status=0)
    frame = (yield from _force_turn_owner_call_steps(state, frame, 199008, 3414))
    frame = _campaign_call_fields(state, frame, 44872, 3420)
    return frame

def force_turn_first_program(state: SceneState, frame: FirstDeploymentFrame, prefix: bool) -> FirstDeploymentFrame:
    """30960/3096E: preserve the real player/non-player loop and two tails."""
    from .business_movement_support import _movement_compare
    frame = display_frame_fields(state, frame)
    if type(prefix) is not bool:
        raise ValueError('actual30960 or3096E entry required')
    if prefix:
        frame = _movement_compare(state, frame, state.read(4294964076, 2), 2, 16)
        if not frame.status & 1:
            return (yield from command_second_force_program(state, frame, True))
        frame = display_call_fields(state, frame, 200372, 199022)
    while True:
        frame = display_call_fields(state, frame, 200486, 199026)
        frame = display_move_fields(state, frame, 'target_x', state.read(4294964086, 2))
        if frame.status & 8:
            frame = (yield from command_finish_assignment_call_program(state, frame, 201190, 199078))
            return display_call_fields(state, frame, 44872, 199134)
        frame, owned = _diplomacy_owner_matches_fields(state, frame)
        if not owned:
            frame = display_store_fields(state, frame, 199058, 4294964066, 2)
            frame = (yield from _force_turn_message_call_steps(state, frame, 199284, 199068))
            frame = (yield from command_assignment_call_program(state, frame, 200618, 199072))
            continue
        frame = display_call_fields(state, frame, 199164, 199086)
        if frame.status & 1:
            continue
        frame = display_store_fields(state, frame, 199088, 4294964754, 523)
        frame = display_store_fields(state, frame, 199094, 4294964066, 4)
        frame = display_store_fields(state, frame, 199100, 4294964076, 0, clear=True)
        return _diplomacy_show_owner_packet_fields(state, frame, False)

def force_turn_message_program(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """30A74..30ABE: physical two-WORD save, vblank child and completion wait.

    A Scene IRQ with missing full CPU fields stops at the real busy-loop read.
    Historical Gameplay supplies only its existing progress observations.
    """
    frame = _scene_refresh_frame(memory, frame)
    saved = []
    for address in (4294964754, 4294964066):
        memory.sync_status(frame)
        value = memory.state.read(address, 2)
        saved.append(value)
        if frame.stack_cursor is not None:
            stack = frame.stack_cursor.advance(-2)
            stack.set_word(0, value)
            frame = first_replace(frame, stack_cursor=stack)
        frame = _scene_refresh_flags(memory, frame, value, 2)
    frame = _scene_refresh_emit(memory, frame, 4294964754, 2, 523)
    memory.state.read(4294964736, 2)
    frame = _scene_refresh_emit(memory, frame, 4294964736, 2, 0)
    frame = _gameplay_message_call_fields(memory, frame, 44872, 199308)
    frame = memory.status_word(frame, 9472)
    while True:
        while True:
            memory.sync_status(frame)
            command = memory.state.read(4294964736, 2)
            frame = _scene_refresh_flags(memory, frame, command, 2)
            if command:
                break
            frame = (yield ForceTurnWait(memory.state, frame, 199312).validate())
        command = memory.state.read(4294964736, 2)
        frame = _first_compare_word(frame, command, 40)
        memory.sync_status(frame)
        if command != 40:
            break
        frame = _gameplay_message_call_fields(memory, frame, 1548, 199334)
        memory.state.read(4294964736, 2)
        frame = _scene_refresh_emit(memory, frame, 4294964736, 2, 0)
        frame = memory.status_word(frame, 9472)
    frame = memory.status_word(frame, 9984)
    for address, legacy_value in ((4294964066, saved[1]), (4294964754, saved[0])):
        if frame.stack_cursor is None:
            value = legacy_value
        else:
            value = frame.stack_cursor.word()
            frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
        frame = _scene_refresh_emit(memory, frame, address, 2, value)
    return memory.sync_status(frame)
