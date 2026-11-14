"""Whole original 00300 bootstrap/main owner with a persistent 003BC wait.

The sole cooperative substitution is the actual zero-request wait. Both
original loops, checksum gate, RAM ranges, all full carriers and CALL/RTS
slots remain in their original order. Hardware waits remain real boundaries.
"""
from __future__ import annotations
from .controller_setup_steps import ControllerSetupWait
from .force_turn_steps import ForceTurnWait
from dataclasses import dataclass
from typing import Generator
from .domain import SceneState, Boundary, checked_state, uint, low16, s16, u32, replace_word
from .contexts_gameplay import FirstDeploymentFrame, first_replace, MovementContinuationBoundary
from .business_movement_support import _movement_frame
from .business_boot import _bootstrap_checksum_extent_frame_fields, _bootstrap_checksum_failed_frame_fields
from .contexts_display_fields import display_frame_fields, display_move_fields, display_address_fields, display_loop_fields, display_store_fields, display_call_fields, display_status_fields

def bootstrap_main_program(state: SceneState, frame: FirstDeploymentFrame) -> Generator[BootstrapMainWait, FirstDeploymentFrame, FirstDeploymentFrame]:
    """300 actual busy bit, checksum, clear ranges and endless scene dispatch."""
    from .business_movement_support import _movement_test, _movement_compare, _movement_binary_flags, _movement_add_word
    from ..high_level_scene_flows.business_scene import _scene_render_compare
    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
    from ..high_level_remaining_flows.business_city import _special_action_swap
    from .business_map import _world_map_bit_fields
    frame = display_frame_fields(state, frame)
    frame = _movement_test(state, frame, state.read(12582916, 2), 16)
    frame = display_address_fields(state, frame, 'auxiliary', 12582916)
    while True:
        frame = display_move_fields(state, frame, 'target_x', frame.auxiliary.word())
        frame = display_move_fields(state, frame, 'target_x', low16(frame.target_x) & 2)
        if frame.status & 4:
            break
        state.progress('original30C bootstrap VDP DMA wait')
    frame = _world_map_bit_fields(state, frame, state.read(10551309, 1), 6)
    retained = not frame.status & 4
    if retained:
        frame = _scene_render_compare(SceneRefreshMemory(state), frame, state.read(4294967292, 4), 1768843636, 32)
        retained = bool(frame.status & 4)
    if not retained:
        frame = display_address_fields(state, frame, 'roster', 420)
        frame = display_move_fields(state, frame, 'target_x', frame.roster.long(), 32)
        frame, value = _movement_binary_flags(state, frame, frame.target_x, 1, 32)
        frame = first_replace(frame, target_x=value)
        frame = display_address_fields(state, frame, 'roster', 512)
        frame, value = _movement_binary_flags(state, frame, frame.target_x, frame.roster.base, 32, True)
        frame = first_replace(frame, target_x=value)
        frame = _bootstrap_checksum_extent_frame_fields(state, frame)
        frame = display_move_fields(state, frame, 'unit', low16(frame.target_x))
        frame, value = _movement_binary_flags(state, frame, low16(frame.unit), 1, 16, True)
        frame = first_replace(frame, unit=replace_word(frame.unit, value))
        frame = _special_action_swap(state, frame, 'target_x')
        frame = display_move_fields(state, frame, 'target_y', 0, 32)
        while True:
            while True:
                value = frame.roster.word()
                frame = first_replace(frame, roster=frame.roster.advance(2))
                frame = _movement_add_word(state, frame, 'target_y', value)
                frame, more = display_loop_fields(frame, 'unit')
                if not more:
                    break
            frame, more = display_loop_fields(frame, 'target_x')
            if not more:
                break
        frame = display_address_fields(state, frame, 'roster', 398)
        frame = _movement_compare(state, frame, low16(frame.target_y), frame.roster.word(), 16)
        if not frame.status & 4:
            return _bootstrap_checksum_failed_frame_fields(state, frame)
        frame = display_address_fields(state, frame, 'auxiliary', 4294966784)
        frame = display_move_fields(state, frame, 'choice', 0, 32)
        frame = display_move_fields(state, frame, 'offset_y', 127)
        while True:
            frame = display_store_fields(state, frame, 864, frame.auxiliary.base, frame.choice, 4)
            frame = first_replace(frame, auxiliary=frame.auxiliary.advance(4))
            frame, more = display_loop_fields(frame, 'offset_y')
            if not more:
                break
        frame = display_store_fields(state, frame, 870, 4294967292, 1768843636, 4)
    frame = display_address_fields(state, frame, 'auxiliary', 16711680)
    frame = display_move_fields(state, frame, 'choice', 0, 32)
    frame = display_move_fields(state, frame, 'offset_y', 16255)
    while True:
        frame = display_store_fields(state, frame, 890, frame.auxiliary.base, frame.choice, 4)
        frame = first_replace(frame, auxiliary=frame.auxiliary.advance(4))
        frame, more = display_loop_fields(frame, 'offset_y')
        if not more:
            break
    frame = display_address_fields(state, frame, 'stack_cursor', 16776704)
    frame = display_call_fields(state, frame, 26662, 908)
    frame = display_call_fields(state, frame, 26960, 914)
    frame = display_call_fields(state, frame, 26548, 920)
    for pc, address, value in ((920, 4294963978, 80), (926, 4294963980, 160), (932, 4294963982, 6144), (938, 4294963160, 2), (944, 4294946814, 1), (950, 4294964736, 4)):
        frame = display_store_fields(state, frame, pc, address, value)
    while True:
        while True:
            frame = _movement_test(state, frame, state.read(4294964736, 2), 16)
            if not frame.status & 4:
                break
            frame = (yield BootstrapMainWait(state, frame).validate())
        frame = display_move_fields(state, frame, 'target_x', state.read(4294964736, 2))
        frame = display_move_fields(state, frame, 'target_x', low16(frame.target_x) & 65532)
        frame = (yield from _bootstrap_dispatch_call_steps(state, frame, u32(980 + s16(low16(frame.target_x))), 974))
        frame = display_store_fields(state, frame, 974, 4294964736, 0, clear=True)
        frame = display_status_fields(state, frame, 9472)

@dataclass(frozen=True)
class BootstrapMainWait:
    """Actual 003BC TST.W wait, sharing all live Scene RAM and carriers."""
    state: SceneState
    frame: FirstDeploymentFrame
    poll: int = 956

    def validate(self):
        checked_state(self.state)
        _movement_frame(self.state, self.frame)
        if self.poll != 956:
            raise ValueError('original main request poll 003BC required')
        if self.frame.status != self.state.sr & 31:
            raise ValueError('suspended bootstrap CCR and full Scene SR disagree')
        return self

class BootstrapMainSession:
    """One complete 00300 invocation, never replaying the initialization prefix.

    This owner has no clock, implicit input, cartridge image or default reset
    profile. A caller supplies the actual full entry frame, source DATA and
    devices. At 003BC it supplies the exact full frame returned by a real IRQ.
    The original nonreturning main loop has no manufactured outer RTS.
    """

    def __init__(self, state: SceneState, frame: FirstDeploymentFrame):
        self.state = checked_state(state)
        self.entry = _movement_frame(state, frame)
        if frame.status != state.sr & 31:
            raise ValueError('bootstrap entry CCR and full Scene SR disagree')
        self._program = bootstrap_main_program(state, frame)
        self._started = self._failed = False
        self.waiting = None
        self.suspensions = 0

    def _take(self, received=None):
        try:
            waiting = next(self._program) if received is None else self._program.send(received)
        except StopIteration:
            self._failed = True
            raise Boundary('original nonreturning main owner completed without a real continuation')
        except BaseException:
            self._failed = True
            raise
        if type(waiting) not in (BootstrapMainWait, ControllerSetupWait, ForceTurnWait) or waiting.state is not self.state:
            self._failed = True
            raise ValueError('bootstrap yielded no actual same-Scene main request wait')
        self.waiting = waiting.validate()
        self.suspensions += 1
        return self.waiting

    def start(self):
        if self._started:
            raise ValueError('cannot replay bootstrap hardware or RAM-clear prefix')
        self._started = True
        return self._take()

    def resume(self, returned: FirstDeploymentFrame, pc: int):
        if not self._started or self._failed or self.waiting is None:
            raise ValueError('one live suspended bootstrap invocation required')
        returned = _movement_frame(self.state, returned)
        uint(pc, 32)
        if pc != self.waiting.poll:
            raise MovementContinuationBoundary(pc, returned, 'IRQ did not return to this actual original main request poll')
        if returned.stack_cursor.base != self.waiting.frame.stack_cursor.base:
            raise Boundary('IRQ did not preserve the suspended original main SP')
        if returned.status != self.state.sr & 31:
            raise ValueError('actual IRQ return CCR and full Scene SR disagree')
        return self._take(returned)

def run_bootstrap_main_blocking_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Compatibility boundary retains the already-entered whole invocation."""
    session = BootstrapMainSession(state, frame)
    waiting = session.start()
    boundary = MovementContinuationBoundary(waiting.poll, waiting.frame, 'original main poll requires explicit asynchronous IRQ progress')
    boundary.bootstrap_main_session = session
    boundary.bootstrap_main_wait = waiting
    raise boundary

def _bootstrap_dispatch_call_steps(state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int):
    """Actual indexed main CALL; keep3CE and528 live through the one menu.

    Other original scene calls keep their sole existing exact implementation.
    The new-game child is a single live Session, not a caught boundary or a
    recreated frame.  Only actual body completion permits its real RTS read.
    """
    if target in (0x418, 0x41C, 0x434, 0x4B8):
        from .command_message_steps import command_main_scene_call_program
        return (yield from command_main_scene_call_program(state, frame, target, continuation))
    if target == 1156:
        return (yield from _bootstrap_force_turn_call_steps(state, frame, target, continuation))
    if target != 1200:
        return display_call_fields(state, frame, target, continuation)
    from .campaign_setup_steps import CampaignSetupSession
    if continuation != 974:
        raise ValueError('original indexed new-campaign return3CE required')
    frame = display_frame_fields(state, frame)
    uint(target, 32)
    uint(continuation, 32)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    child = CampaignSetupSession(state, entered)
    returned = child.start()
    while type(returned) is ControllerSetupWait:
        waiting = returned
        returned = child.resume((yield waiting), waiting.poll)
    returned = display_frame_fields(state, returned)
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise MovementContinuationBoundary(actual, returned, 'original display child continuation changed')
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))

def _bootstrap_force_turn_call_steps(state, frame, target, continuation):
    """The same main invocation keeps3CE live through0484/D56/3099C."""
    from .force_turn_steps import ForceTurnSession
    if (target, continuation) != (1156, 974):
        raise ValueError('actual main first-force indexed CALL pair required')
    frame = display_frame_fields(state, frame)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    child = ForceTurnSession(state, entered)
    returned = child.start()
    while type(returned) is ForceTurnWait:
        waiting = returned
        returned = child.resume((yield waiting), waiting.poll)
    returned = display_frame_fields(state, returned)
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise MovementContinuationBoundary(actual, returned, 'original force-turn caller return changed')
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))
