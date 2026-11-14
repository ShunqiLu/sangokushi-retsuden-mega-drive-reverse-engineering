"""Typed results shared by adapted, previously reconstructed helpers.

Only logical values and live-state outcomes cross this boundary. In particular
the force-head test reports its selected member and original carry contract,
not a register collection. Fixed-width values are validated before DATA reads.
"""
from dataclasses import dataclass
from .domain import GameState, Word, CarryOutcome, uint
from ..high_level_scene_flows.domain import SceneState


@dataclass(frozen=True)
class RosterMemory:
    """Sealed roster endpoint shared by two genuine live-state interfaces.

    Reads and writes go directly to the supplied state. No RAM copy, invented
    register input, or second roster-building algorithm crosses this boundary.
    """
    state: object

    def __post_init__(self):
        if type(self.state) not in (GameState, SceneState):
            raise ValueError('genuine roster live State required')

    def read(self, address, size):
        return self.state.read(address, size)

    def write(self, address, size, value):
        self.state.write(address, size, value)


@dataclass(frozen=True)
class ForceHeadMatch:
    head: Word
    outcome: CarryOutcome

    def __post_init__(self):
        uint(self.head, 16, 'force head')
        if type(self.outcome) is not CarryOutcome:
            raise ValueError('typed original carry outcome required')
        self.outcome.__post_init__()

    @property
    def carry(self):
        return self.outcome.carry

    @property
    def conditional_sr(self):
        return self.outcome.conditional_sr
