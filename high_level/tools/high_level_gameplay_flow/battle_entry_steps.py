"""Complete public battle/duel/allocation entry and result continuation API.

Legacy IRQ-only Sessions and their entry functions remain unchanged. This
owner exposes the complete existing Lifecycle graph, including real device
waits, without adding an outer CALL slot or manufacturing scheduler input.
"""
import threading
from types import GeneratorType

from .battle_lifecycle_steps import BattleLifecycleScenePrograms
from . import battle_round_steps
from .scene_load_steps import GameplaySceneWait
from ..high_level_dynamic_flows.allocation_steps import AllocationSceneWait
from ..high_level_scene_flows.duel_scene_steps import DuelSceneWait
from ..high_level_main_flows.domain import Boundary, checked_state, uint
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
from ..high_level_main_flows.business_movement_support import _movement_frame


ENTRY_POINTS = {'round': 0xDC0, 'main': 0x498, 'allocation': 0x3D654, 'duel': 0x26DB4}
WAIT_TYPES = (GameplaySceneWait, AllocationSceneWait, DuelSceneWait)


class BattleEntrySession:
    """One same-Scene complete entry with separate real IRQ/device resumes.

    The caller already owns the incoming physical return LONG. Entry, every
    inner call, all sixteen carriers and the actual result come exclusively
    from the existing whole algorithms. Closing a suspended Session abandons
    its Python continuation; it never fabricates an original RTS or result.
    """

    def __init__(self, state, frame, *, entry):
        self.state = checked_state(state)
        self.entry = _movement_frame(state, frame)
        self.entry.validate(state, True)
        if type(entry) is not str or entry not in ENTRY_POINTS:
            raise ValueError('exact round/main/allocation/duel entry role required')
        if frame.status != state.sr & 31:
            raise ValueError('actual complete battle entry SR and CCR-X must agree')
        self.role, self.entry_pc = entry, ENTRY_POINTS[entry]
        self._thread = threading.get_ident()
        self.programs = BattleLifecycleScenePrograms(state)
        self._provider = self.programs
        self._provider_type = type(self.programs)
        self._entry_sp = frame.stack_cursor.base
        if entry == 'round':
            self._program = self.programs._round_entry(state, frame)
        elif entry == 'allocation':
            self._program = self.programs._allocation_entry(state, frame)
        elif entry == 'duel':
            self._program = self.programs._duel_entry(state, frame)
        else:
            # Direct Main498 is its original BRA DC0. Do not invoke the
            # indexed Main CALL helper and do not write another3CE LONG.
            self._program = self.programs._message_waits(self.programs.lifecycle_round[
                'round', 'main', battle_round_steps.MAIN_VIEW](state, frame))
        if type(self._program) is not GeneratorType:
            raise TypeError('one complete existing Lifecycle generator required')
        self._program_code = self._program.gi_code
        self._started = self._complete = self._failed = self._closed = False
        self.waiting = self.result = None
        self.status_word = state.sr
        self.suspensions = 0

    @property
    def complete(self):
        return self._complete

    @property
    def failed(self):
        return self._failed

    def _require_current(self):
        if (threading.get_ident() != self._thread or self.programs is not self._provider
                or type(self.programs) is not self._provider_type
                or self._provider_type is not BattleLifecycleScenePrograms
                or self._program.gi_code is not self._program_code):
            raise ValueError('the same actual battle entry provider/generator/thread is required')
        self.programs.require_current(self.state)

    def _take(self, returned=None):
        self._require_current()
        try:
            waiting = next(self._program) if returned is None else self._program.send(returned)
        except StopIteration as finished:
            self._failed = True
            result = _movement_frame(self.state, finished.value)
            result.validate(self.state, True)
            if result.stack_cursor.base != self._entry_sp or result.status != self.state.sr & 31:
                self._failed = True
                raise Boundary('whole battle result must retain its incoming physical SP and actual SR')
            self._complete, self.waiting, self.result = True, None, result
            self._failed = False
            self.status_word = self.state.sr
            return result
        except BaseException:
            self._failed = True
            raise
        if type(waiting) not in WAIT_TYPES or waiting.state is not self.state:
            self._failed = True
            raise ValueError('an actual same-Scene battle device/allocation/duel wait is required')
        self.waiting = waiting.validate()
        self.status_word = self.state.sr
        self.suspensions += 1
        return self.waiting

    def start(self):
        self._require_current()
        if self._started or self._closed:
            raise ValueError('cannot replay a battle entry or its initialization prefix')
        self._started = True
        return self._take()

    def _live(self):
        self._require_current()
        if not self._started or self._complete or self._failed or self._closed or self.waiting is None:
            raise ValueError('one live suspended battle entry is required')

    def resume_interrupt(self, returned, pc):
        self._live()
        waiting = self.waiting
        if type(waiting) is GameplaySceneWait and not waiting.needs_interrupt:
            raise ValueError('the suspended battle point requires its exact device event, not an IRQ')
        returned = _movement_frame(self.state, returned)
        returned.validate(self.state, True)
        uint(pc, 32)
        if pc != waiting.poll:
            raise MovementContinuationBoundary(pc, returned, 'IRQ must RTE to the actual battle entry poll')
        if (returned.stack_cursor.base != waiting.frame.stack_cursor.base
                or self.state.sr != self.status_word or returned.status != self.status_word & 31):
            raise Boundary('battle IRQ must restore the suspended physical SP and complete SR/CCR-X')
        return self._take(returned)

    def resume_device(self, event):
        self._live()
        waiting = self.waiting
        if (type(waiting) is not GameplaySceneWait or waiting.needs_interrupt
                or type(event) is not str or event != waiting.event):
            raise ValueError('the exact suspended battle device event is required')
        if self.state.sr != self.status_word:
            raise Boundary('device progress cannot change the suspended software SR')
        # The external owner must already have supplied real progress. If it
        # did not, the original loop rereads the device and yields again.
        return self._take(waiting.frame)

    def close(self):
        if self._closed:
            return
        self._require_current()
        self._program.close()
        self._closed = True
        if not self._complete:
            self._failed = True


def battle_entry_program(state, frame, *, entry):
    """Forward the identical typed waits; never supply device or IRQ success."""
    session = BattleEntrySession(state, frame, entry=entry)
    current = session.start()
    try:
        while type(current) in WAIT_TYPES:
            waiting = current
            returned = yield waiting
            if type(waiting) is GameplaySceneWait and not waiting.needs_interrupt:
                if returned is not waiting.frame:
                    raise ValueError('device continuation cannot replace the actual battle frame')
                current = session.resume_device(waiting.event)
            else:
                current = session.resume_interrupt(returned, waiting.poll)
        return current
    finally:
        session.close()


def complete_battle_main_scene_program(state, frame):
    """Actual Main498 BRA lifetime, retaining the caller's existing LONG."""
    return (yield from battle_entry_program(state, frame, entry='main'))
