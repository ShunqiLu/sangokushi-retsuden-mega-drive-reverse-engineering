"""Immutable live-view result contracts for selected group deployment."""
from dataclasses import dataclass
from .domain import Table, Word, Long, uint, checked_table


@dataclass(frozen=True)
class ResourceShare:
    selected: Long
    remaining: Long

    def __post_init__(self):
        uint(self.selected, 32)
        uint(self.remaining, 32)


@dataclass(frozen=True)
class DeploymentResult:
    group: Table
    selected_count: Word

    def __post_init__(self):
        checked_table(self.group)
        uint(self.selected_count, 16)

from .domain import GameState

def project_deployment_command_fields(state: GameState, target: int, group=None, amount=None, selected_weight=None, total_weight=None):
    """A historical command input does not include full high halves/SP/CCR.

    The sole Scene rule is still the authority. Missing fields produce its
    original-address boundary, not a copied scalar implementation or zero CPU.
    Readonly byte segments are shared immutable inputs; RAM/events are aliases.
    """
    from ..high_level_scene_flows.domain import SceneState, ReadOnlyData as SceneData
    from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame, first_replace
    from ..high_level_remaining_flows.business_city import execute_deployment_menu_fields
    from .domain import checked_state
    checked_state(state)
    uint(target, 32)
    if group is not None:
        checked_table(group, state)
    for value in (amount, selected_weight, total_weight):
        if value is not None:
            uint(value, 32)
    scene = SceneState(state.ram, data=SceneData(state.data.segments), max_reads=state.max_reads, sr=state.sr)
    scene.events = state.events
    scene.reads = state.reads
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        roster=None if group is None else scene.table_at(group.base).cursor(),
        unit=amount, offset_x=selected_weight, offset_y=total_weight)
    try:
        return execute_deployment_menu_fields(scene, target, frame)
    finally:
        state.reads, state.sr = scene.reads, scene.sr
