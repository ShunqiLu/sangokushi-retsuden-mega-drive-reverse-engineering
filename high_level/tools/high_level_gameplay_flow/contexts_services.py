"""Explicit data contracts crossing video, glyph and message services.

These values describe live sources and output carriers, not CPU register
collections. Missing hardware or external handlers remain finite boundaries.
"""
from dataclasses import dataclass
from .domain import Byte, Word, Long, Cursor, uint, checked_cursor


@dataclass(frozen=True)
class MarkerResetMemory:
    """Sealed access to the original live state for the four marker WORDs.

    This adapter admits only the existing GameplayState or SceneState. It
    owns no RAM, does not translate addresses, and accepts no arbitrary port.
    The one marker algorithm can therefore serve both existing frontends.
    """
    state: object

    def __post_init__(self):
        self.validate()

    def validate(self):
        from .domain import GameplayState
        from ..high_level_scene_flows.domain import SceneState
        if type(self.state) not in (GameplayState, SceneState):
            raise ValueError('existing live GameplayState or SceneState required')
        return self

    def write_word(self, address, value):
        uint(address, 32)
        uint(value, 16)
        self.state.write(address, 2, value)


@dataclass(frozen=True)
class SceneDisplayContext:
    """Unrecovered scene service boundary; state effects are not a fake result."""
    purpose: str = 'gameplay-overlay'

    def __post_init__(self):
        if type(self.purpose) is not str or self.purpose != 'gameplay-overlay':
            raise ValueError('explicit gameplay display service purpose required')


@dataclass(frozen=True)
class SceneDisplayResult:
    """Observable retained outputs needed after the external scene service."""
    foreground: Long
    glyph_count: Long
    training_carrier: Long

    def __post_init__(self):
        uint(self.foreground, 32)
        uint(self.glyph_count, 32)
        uint(self.training_carrier, 32)


@dataclass(frozen=True)
class GlyphColors:
    background: Long
    foreground: Long

    def __post_init__(self):
        uint(self.background, 32)
        uint(self.foreground, 32)


@dataclass(frozen=True)
class GlyphStreamResult:
    tokens: Cursor
    destination: Cursor
    remaining_carrier: Long

    def __post_init__(self):
        checked_cursor(self.tokens)
        checked_cursor(self.destination, self.tokens.state)
        uint(self.remaining_carrier, 32)


@dataclass(frozen=True)
class TransferResult:
    source: Cursor
    destination: Cursor

    def __post_init__(self):
        checked_cursor(self.source)
        checked_cursor(self.destination, self.source.state)


@dataclass(frozen=True)
class SpriteControlContext:
    token: Word
    command: Long
    row_remaining: Word
    source: Cursor
    destination: Cursor

    def __post_init__(self):
        uint(self.token, 16)
        uint(self.command, 32)
        uint(self.row_remaining, 16)
        checked_cursor(self.source)
        checked_cursor(self.destination, self.source.state)


@dataclass(frozen=True)
class SpriteControlResult:
    command: Long
    row_remaining: Word

    def __post_init__(self):
        uint(self.command, 32)
        uint(self.row_remaining, 16)

from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame, first_replace
from ..high_level_scene_flows.domain import Boundary as SceneBoundary
from ..high_level_battle_ai.business_formation import (
    _first_word, _first_byte, _first_long, _first_shift_word, _first_compare_word,
)

class SceneRefreshMemory:
    """Same live gameplay/Scene storage; independent legacy frame validation.

    No alternate RAM, synthetic bus, or widened FirstDeploymentFrame contract.
    Historical APIs did not observe SP; complete Scene callers must supply it.
    """
    def __init__(self, state):
        from .domain import GameplayState
        from ..high_level_scene_flows.domain import SceneState
        if type(state) not in (GameplayState, SceneState):
            raise ValueError('existing gameplay or Scene refresh memory required')
        self.state = state

    def cursor_at(self, address, offset=0):
        from .domain import GameplayState
        if type(self.state) is GameplayState:
            return self.state.table(address).cursor(offset)
        return self.state.table_at(address).cursor(offset)

    def frame(self, frame):
        from .domain import GameplayState, checked_cursor
        if type(frame) is not FirstDeploymentFrame:
            raise ValueError('actual refresh fields required')
        if type(self.state) is GameplayState:
            if frame.stack_cursor is not None:
                raise ValueError('legacy gameplay refresh did not observe physical A7')
            for value in (frame.target_x,frame.target_y,frame.unit,frame.count,
                          frame.distance,frame.offset_x,frame.offset_y,frame.choice):
                if value is not None:
                    uint(value,32)
            for view in (frame.roster,frame.candidates,frame.controller,frame.scan,
                         frame.opponent,frame.scratch,frame.auxiliary):
                if view is not None:
                    checked_cursor(view,self.state)
            if frame.status is not None:
                uint(frame.status,8)
                if frame.status > 31:
                    raise ValueError('actual low-five-bit refresh CCR required')
        else:
            frame.validate(self.state,False)
            if frame.stack_cursor is not None:
                if any(value is None for value in (
                    frame.target_x,frame.target_y,frame.unit,frame.count,
                    frame.distance,frame.offset_x,frame.offset_y,frame.choice,
                    frame.roster,frame.candidates,frame.controller,frame.scan,
                    frame.opponent,frame.scratch,frame.auxiliary,frame.status)):
                    raise SceneRefreshBoundary(0x1072C,frame,None)
                frame.validate(self.state,True)
        return frame

    def sync_status(self, frame):
        if frame.status is not None:
            self.state.sr = (self.state.sr & 65504) | frame.status
        return frame

    def status_word(self, frame, value):
        self.sync_status(frame)
        self.state.set_status_word(value)
        return first_replace(frame,status=value & 31)


class SceneRefreshBoundary(SceneBoundary):
    """A real unobserved child/return slot, with the actual current frame."""
    def __init__(self, target, frame, expected):
        self.target,self.context,self.expected = target,frame,expected
        super().__init__('scene refresh requires genuine child fields or original continuation')


@dataclass(frozen=True)
class SceneSoundSelectionFields:
    """The observed table WORD does not invent its unobserved retained half."""
    frame: FirstDeploymentFrame
    command: Word

    def __post_init__(self):
        if type(self.frame) is not FirstDeploymentFrame:
            raise ValueError('actual scene sound fields required')
        uint(self.command,16)
