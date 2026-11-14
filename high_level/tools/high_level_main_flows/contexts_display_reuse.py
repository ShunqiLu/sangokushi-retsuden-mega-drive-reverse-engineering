"""Same-state results for existing map sprite and decimal formatting services."""
from dataclasses import dataclass
from .domain import Cursor, Long, Word, checked_cursor, uint


@dataclass(frozen=True)
class MapSpriteResult:
    source: Cursor
    x: Long
    y: Long
    attributes: Long

    def validate(self, state):
        checked_cursor(self.source, state)
        uint(self.x, 32)
        uint(self.y, 32)
        uint(self.attributes, 32)
        return self


@dataclass(frozen=True)
class DecimalPlaceResult:
    remainder: Word
    started: Word

    def __post_init__(self):
        uint(self.remainder, 16)
        uint(self.started, 16)

@dataclass(frozen=True)
class MapSpriteTransaction:
    """Actual AC08/AC10/AC28 outputs, including the final documented CMP."""
    source: Cursor
    x: Long
    y: Long
    attributes: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self,state):
        checked_cursor(self.source,state)
        for value in (self.x,self.y,self.attributes):
            uint(value,32)
        if any(type(value) is not bool for value in (self.carry,self.zero,self.negative,self.overflow)):
            raise ValueError('strict sprite comparison outcomes required')
        return self


@dataclass(frozen=True)
class MapSpriteFields:
    """AC08/AC10/AC28 field observations; no supplied register high halves.

    This observes the non-stack transaction. It does not synthesize MOVEM
    scratch/A1 or physical SP and does not close their DATA aliases.
    """
    source: Cursor
    x: Word
    y: Word
    attributes: Word
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_cursor(self.source, state)
        for value in (self.x, self.y, self.attributes):
            uint(value, 16)
        if any(type(value) is not bool for value in (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('actual final sprite CMP observations required')
        return self


# Sole player AC08/AC10/AC28 field algorithm; no copied sprite geometry.
from ..high_level_player_commands.contexts_display import SpritePacketMemory
from ..high_level_player_commands.business_display import (
    append_live_command_sprite_packet_fields, append_live_command_sprite_fields,
)
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame, first_replace
