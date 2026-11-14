"""Named display, route and world-selection inputs/results, not CPU dictionaries."""
from dataclasses import dataclass
from .domain import Word, Long, Table, Cursor, CarryOutcome, uint, checked_table, checked_cursor


@dataclass(frozen=True)
class SpriteAppendResult:
    source: Cursor
    attributes: Word

    def __post_init__(self):
        checked_cursor(self.source)
        uint(self.attributes, 16)


@dataclass(frozen=True)
class TileRun:
    destination: Cursor
    next_tile: Long
    remaining_counter: Long

    def __post_init__(self):
        checked_cursor(self.destination)
        uint(self.next_tile, 32)
        uint(self.remaining_counter, 32)


@dataclass(frozen=True)
class RouteCost:
    row: Word
    column: Word
    cost: Word

    def __post_init__(self):
        for value in (self.row, self.column, self.cost):
            uint(value, 16)


@dataclass(frozen=True)
class MarkerResult:
    record: Cursor
    outcome: CarryOutcome

    def __post_init__(self):
        checked_cursor(self.record)
        if type(self.outcome) is not CarryOutcome:
            raise ValueError('named carry result required')


@dataclass(frozen=True)
class WorldSelection:
    scroll_x: Word
    scroll_y: Word
    record: Table | None

    def __post_init__(self):
        uint(self.scroll_x, 16)
        uint(self.scroll_y, 16)
        if self.record is not None:
            checked_table(self.record)

from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame, first_replace
from ..high_level_battle_ai.business_formation import (
    _first_word, _first_byte, _first_long, _first_add_word, _first_sub_word,
    _first_shift_word, _first_memory_word,
)

class SpritePacketMemory:
    """Existing player/Scene sprite DATA views; no checked-State union change."""
    def __init__(self, state):
        from ..high_level_scene_flows.domain import SceneState
        from .domain import GameState
        if type(state) not in (GameState, SceneState):
            raise ValueError('actual player or Scene sprite memory required')
        self.state = state

    def cursor_at(self, address, offset=0):
        from .domain import GameState
        if type(self.state) is GameState:
            return self.state.table(address).cursor(offset)
        return self.state.table_at(address).cursor(offset)

    def check_cursor(self, view):
        from .domain import Cursor as PlayerCursor, checked_cursor as player_cursor
        from ..high_level_scene_flows.domain import Cursor as SceneCursor, checked_cursor as scene_cursor
        if type(view) is PlayerCursor:
            player_cursor(view, self.state)
        elif type(view) is SceneCursor:
            scene_cursor(view, self.state)
        else:
            raise ValueError('same-state actual sprite Cursor required')

    def frame(self, frame, complete=False):
        from .domain import GameState
        from ..high_level_scene_flows.domain import Boundary as SceneBoundary
        if type(frame) is not FirstDeploymentFrame or type(complete) is not bool:
            raise ValueError('actual typed sprite fields required')
        if type(self.state) is GameState:
            if complete or frame.stack_cursor is not None:
                raise ValueError('historical player sprite API did not observe physical SP')
            for name in ('target_x','target_y','unit','count','distance','offset_x','offset_y','choice'):
                value = frame.carrier(name)
                if value is not None:
                    uint(value,32)
            for view in (frame.roster,frame.candidates,frame.controller,frame.scan,
                         frame.opponent,frame.scratch,frame.auxiliary):
                if view is not None:
                    self.check_cursor(view)
            if frame.status is not None:
                uint(frame.status,8)
                if frame.status > 31:
                    raise ValueError('actual five-bit sprite CCR required')
        else:
            frame.validate(self.state,False)
            if complete:
                if any(value is None for value in (
                        frame.target_x,frame.target_y,frame.unit,frame.count,
                        frame.distance,frame.offset_x,frame.offset_y,frame.choice,
                        frame.roster,frame.candidates,frame.controller,frame.scan,
                        frame.opponent,frame.scratch,frame.auxiliary,
                        frame.stack_cursor,frame.status)):
                    raise SceneBoundary('AC08 sprite return requires genuine complete current fields and SP')
                frame.validate(self.state,True)
        self.check_cursor(frame.roster)
        return frame

    def sync_status(self, frame):
        from ..high_level_scene_flows.domain import SceneState
        if type(self.state) is SceneState and frame.status is not None:
            self.state.sr = (self.state.sr & 65504) | frame.status
        return frame

    def save_scratch(self, frame):
        """AC28 true predecrement MOVEM: A1,D7,D6,D5,D4,D3."""
        if frame.stack_cursor is None:
            return frame
        stack = frame.stack_cursor
        for value in (frame.candidates.base,frame.choice,frame.offset_y,
                      frame.offset_x,frame.distance,frame.count):
            stack = stack.advance(-4)
            stack.set_long(0,value)
        return first_replace(frame,stack_cursor=stack)

    def restore_scratch(self, frame):
        """AD00 reads the six live LONGs, including aliased sprite writes."""
        if frame.stack_cursor is None:
            return frame
        stack = frame.stack_cursor
        values = []
        for index in range(6):
            values.append(stack.long())
            stack = stack.advance(4)
        return first_replace(frame,count=values[0],distance=values[1],
            offset_x=values[2],offset_y=values[3],choice=values[4],
            candidates=self.cursor_at(values[5]),stack_cursor=stack)


@dataclass(frozen=True)
class SpritePacketFields:
    """Actual visible WORDs and optional genuine full entry/return carrier set."""
    frame: FirstDeploymentFrame
    x: Word
    y: Word
    attributes: Word
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, memory):
        if type(memory) is not SpritePacketMemory:
            raise ValueError('same-state sprite memory required')
        memory.frame(self.frame,self.frame.stack_cursor is not None)
        for value in (self.x,self.y,self.attributes):
            uint(value,16)
        if any(type(value) is not bool for value in (self.carry,self.zero,self.negative,self.overflow)):
            raise ValueError('actual sprite CMP outcomes required')
        return self
