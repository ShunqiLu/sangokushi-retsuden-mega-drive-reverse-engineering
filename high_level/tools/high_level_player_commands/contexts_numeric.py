"""One same-state decimal transaction boundary for the existing 1270A/12760.

Fields are observed algorithm data, not a fake register frame. Legacy callers
do not supply D3/D4/D5 high words; only the city caller combines those genuine
live inputs with returned WORD fields. No copied RAM, files or CPU execution.
"""
from dataclasses import dataclass
from .domain import GameState, Cursor, Boundary, uint, u16, u32, s16, checked_cursor


class DecimalMemory:
    """Closed pair of real state/view implementations, sharing original DATA."""
    def __init__(self, state, stack_cursor=None):
        from ..high_level_scene_flows.domain import SceneState
        if type(state) not in (GameState, SceneState):
            raise ValueError('one real player or Scene decimal state required')
        self.state = state
        self.stack_cursor = stack_cursor
        if stack_cursor is not None:
            self.check_cursor(stack_cursor)

    def check_cursor(self, destination):
        from ..high_level_scene_flows.domain import Cursor as SceneCursor
        from ..high_level_scene_flows.domain import checked_cursor as scene_cursor
        if type(destination) is Cursor:
            checked_cursor(destination, self.state)
        elif type(destination) is SceneCursor:
            scene_cursor(destination, self.state)
        else:
            raise ValueError('same-state decimal output Cursor required')

    def enter_call(self, continuation):
        """One actual LONG return-address write at the observed predecrement SP."""
        if self.stack_cursor is None:
            return
        uint(continuation, 32)
        self.stack_cursor = self.stack_cursor.advance(-4)
        self.stack_cursor.set_long(0, continuation)

    def leave_call(self, continuation):
        """Physical RTS read, with altered control remaining an explicit boundary."""
        if self.stack_cursor is None:
            return
        uint(continuation, 32)
        actual = self.stack_cursor.long()
        self.stack_cursor = self.stack_cursor.advance(4)
        if actual != continuation:
            from ..high_level_scene_flows.domain import SceneState, Boundary as SceneBoundary
            if type(self.state) is SceneState:
                raise SceneBoundary('modified original decimal/menu return slot')
            raise Boundary('modified original decimal/menu return slot')

    def glyph(self, index):
        return self.state.read(u32(0x12782 + s16(u16(index))), 1)


@dataclass(frozen=True)
class DecimalPlaceFields:
    remainder: int
    started: int
    glyph: int

    def __post_init__(self):
        for value in (self.remainder, self.started, self.glyph):
            uint(value, 16)


@dataclass(frozen=True)
class DecimalTransactionFields:
    destination: object
    remainder: int
    divisor: int
    started: int
    glyph: int

    def __post_init__(self):
        uint(self.remainder, 32)
        for value in (self.divisor, self.started, self.glyph):
            uint(value, 16)

    def validate(self, state):
        DecimalMemory(state).check_cursor(self.destination)
        return self
