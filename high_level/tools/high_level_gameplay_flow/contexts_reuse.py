"""Typed results for previously reconstructed reusable gameplay logic."""
from dataclasses import dataclass
from .domain import GameplayState, Table, Cursor, Byte, Word, Long, CarryOutcome, uint, checked_table


@dataclass(frozen=True)
class DuelDispositionContext:
    officer: Word
    disposition: Byte

    def __post_init__(self):
        uint(self.officer, 16)
        uint(self.disposition, 8)


@dataclass(frozen=True)
class DuelSettlementContext:
    training_carrier: Long

    def __post_init__(self):
        uint(self.training_carrier, 32)


@dataclass(frozen=True)
class DuelSettlementResult:
    progress_carrier: Long

    def __post_init__(self):
        uint(self.progress_carrier, 32)


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


@dataclass(frozen=True)
class RadialSeed:
    remaining: Long
    count: Long
    increment: Long
    last_threshold: Long
    threshold_cursor: Table | None

    def __post_init__(self):
        for value in (self.remaining, self.count, self.increment, self.last_threshold):
            uint(value, 32)
        if self.threshold_cursor is not None:
            checked_table(self.threshold_cursor)


@dataclass(frozen=True)
class EventSubmission:
    """Distinct main result and carried owner WORD; no additional memory read."""
    value: Word
    owner_word: Word

    def __post_init__(self):
        uint(self.value, 16)
        uint(self.owner_word, 16)


def project_gameplay_arrival_fields(state: GameplayState, target: int, packet=None, city=None, row=None, column=None):
    """Exact old GameplayState adapter; no expanded State union or fake return.

    The old interface did not observe full entry carriers or A7. External
    service/hardware ABI is consequently not invoked through this adapter;
    the complete-entry guard stops before any such missing observation.
    """
    from ..high_level_scene_flows.domain import SceneState, ReadOnlyData as SceneData
    from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame, first_replace
    from ..high_level_remaining_flows.business_city import execute_deployment_menu_fields
    from .domain import checked_state
    checked_state(state)
    uint(target, 32)
    if packet is not None:
        checked_table(packet, state)
    for value in (city, row, column):
        if value is not None:
            uint(value, 16)
    scene = SceneState(state.ram, data=SceneData(state.data.segments), max_reads=state.max_reads,
        max_samples=state.max_samples, sr=state.sr)
    scene.events, scene.reads, scene.samples = state.events, state.reads, state.samples
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        roster=None if packet is None else scene.table_at(packet.base).cursor())
    try:
        return execute_deployment_menu_fields(scene, target, frame)
    finally:
        state.reads, state.samples, state.sr = scene.reads, scene.samples, scene.sr
