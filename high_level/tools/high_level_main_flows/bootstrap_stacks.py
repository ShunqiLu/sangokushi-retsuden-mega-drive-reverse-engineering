"""Banked stack ownership for original bootstrap and existing IRQ points.

The complete software frame remains the only owner of D/A carriers and CCR.
This narrow object retains only explicit USP/SSP; it is not a CPU engine.
"""
from .contexts_boot import BootstrapControl
from .domain import checked_state, uint
from ..high_level_video.frame_interrupts import ExecutionPoint


class BankedStackControl(BootstrapControl):
    """Explicit initial banks, real MOVE-to-USP, and full-frame synchronization.

    Setting a bank does not allocate RAM, fabricate stack contents, alter SR,
    or silently rewrite the caller's immutable software frame. Original MOVEM
    restoration stays in the already recovered complete bootstrap function;
    the unused legacy restore service remains an explicit base-class boundary.
    """
    def __init__(self, state, *, user_stack, supervisor_stack):
        self.state = checked_state(state)
        self.user_stack = uint(user_stack, 32)
        self.supervisor_stack = uint(supervisor_stack, 32)

    def _state(self, state):
        if state is not self.state:
            raise ValueError('bootstrap banks belong to another live Scene')

    def set_user_stack(self, state, address):
        self._state(state)
        self.user_stack = uint(address, 32)
        state.events.append(('bootstrap_USP', address))

    def set_supervisor_stack(self, state, address):
        self._state(state)
        self.supervisor_stack = uint(address, 32)
        state.events.append(('bootstrap_SSP', address))

    def capture(self, pc, frame):
        """Adopt actual software A7 and expose the other bank for IRQ entry."""
        other = self.user_stack if self.state.sr & 0x2000 else self.supervisor_stack
        point = ExecutionPoint(pc, frame, self.state.table_at(other).cursor()).validate(self.state)
        self.accept_point(point)
        return point

    def accept_point(self, point):
        """Adopt an actual validated suspended point or the IRQ's returned point."""
        if type(point) is not ExecutionPoint:
            raise ValueError('actual complete suspended execution point required')
        point.validate(self.state)
        if self.state.sr & 0x2000:
            self.supervisor_stack = point.frame.stack_cursor.base
            self.user_stack = point.inactive_stack.base
        else:
            self.user_stack = point.frame.stack_cursor.base
            self.supervisor_stack = point.inactive_stack.base
        return point
