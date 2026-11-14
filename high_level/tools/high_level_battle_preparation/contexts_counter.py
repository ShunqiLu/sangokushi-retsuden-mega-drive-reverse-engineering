"""Field-level live counter transactions and genuine Scene partial returns."""
from dataclasses import dataclass
from .domain import PreparationState, uint, u32


class CounterMemory:
    def __init__(self, state):
        from ..high_level_scene_flows.domain import SceneState
        if type(state) not in (PreparationState, SceneState):
            raise ValueError('one real preparation or Scene counter state required')
        self.state = state

    def table(self, address):
        from ..high_level_scene_flows.domain import SceneState
        return self.state.table_at(address) if type(self.state) is SceneState else self.state.table(address)


@dataclass(frozen=True)
class CounterFields:
    destination: int
    source: int | None
    last_byte: int
    loop_word: int

    def __post_init__(self):
        uint(self.destination, 32)
        if self.source is not None:
            uint(self.source, 32)
        uint(self.last_byte, 8)
        uint(self.loop_word, 16)


@dataclass(frozen=True)
class SceneCounterInput:
    value: int
    field: int
    source: object | None

    def validate(self, state):
        from ..high_level_scene_flows.domain import checked_state, checked_table
        checked_state(state)
        uint(self.value, 32)
        uint(self.field, 32)
        if self.source is not None:
            checked_table(self.source, state)
        return self


@dataclass(frozen=True)
class SceneCounterResult:
    destination: object
    source: object
    value: int
    field: int
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        from ..high_level_scene_flows.domain import checked_state, checked_table
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.source, state)
        uint(self.value, 32)
        uint(self.field, 32)
        if any(type(v) is not bool for v in (self.carry,self.zero,self.negative,self.overflow)):
            raise ValueError('strict counter partial conditions required')
        return self


def project_preparation_selection_fields(state: PreparationState, target: int, object_view=None, first=None, second=None, attributes=None):
    """Preparation scalar parameters are not a physical callee-entry frame."""
    from ..high_level_scene_flows.domain import SceneState, ReadOnlyData as SceneData
    from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame, first_replace
    from ..high_level_remaining_flows.business_city import execute_deployment_menu_fields
    from .domain import Table
    if type(state) is not PreparationState:
        raise ValueError('existing PreparationState required')
    uint(target, 32)
    if object_view is not None and (type(object_view) is not Table or object_view.state is not state):
        raise ValueError('same preparation live object required')
    for value in (first, second):
        if value is not None:
            uint(value, 32)
    if attributes is not None and (type(attributes) is not Table or attributes.state is not state):
        raise ValueError('same preparation attribute view required')
    scene = SceneState(state.ram, data=SceneData(state.data.segments), max_reads=state.max_reads, sr=state.sr)
    scene.events = state.events
    scene.reads = state.reads
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        roster=None if object_view is None else scene.table_at(object_view.base).cursor(),
        target_x=first, choice=second, scratch=None if attributes is None else scene.table_at(attributes.base))
    try:
        return execute_deployment_menu_fields(scene, target, frame)
    finally:
        state.reads, state.sr = scene.reads, scene.sr
