"""Typed, family-local inputs for live group and battle scene operations.

Carriers name business operands whose retained upper bits are observable.
They are not a CPU register dictionary. Views remain live and are checked
against the current GameplayState before the first business DATA access.
"""
from dataclasses import dataclass
from .domain import (GameplayState, Table, Cursor, Word, Long, uint,
                     checked_state, checked_table, checked_cursor)


@dataclass(frozen=True)
class GlyphBatchContext:
    source: Cursor
    destination: Cursor
    background: Long
    foreground: Long
    inclusive_count: Long

    def validate(self, state):
        checked_cursor(self.source, state)
        checked_cursor(self.destination, state)
        uint(self.foreground, 32)
        uint(self.background, 32)
        uint(self.inclusive_count, 32)
        return self


@dataclass(frozen=True)
class MapTransferContext:
    source: Cursor
    auxiliary: Cursor
    parameters: Cursor
    inclusive_count: Long

    def validate(self, state):
        checked_cursor(self.source, state)
        checked_cursor(self.auxiliary, state)
        checked_cursor(self.parameters, state)
        uint(self.inclusive_count, 32)
        return self


@dataclass(frozen=True)
class BattleSceneContext:
    background: Long
    foreground: Long
    glyph_count: Long
    training_carrier: Long

    def validate(self, state):
        checked_state(state)
        for value in (self.foreground, self.background,
                      self.glyph_count, self.training_carrier):
            uint(value, 32)
        return self


@dataclass(frozen=True)
class PacketMutationContext:
    packet: Table
    selected_roster: Cursor
    insertion_roster: Cursor
    member_count: Word

    def validate(self, state):
        checked_table(self.packet, state)
        checked_cursor(self.selected_roster, state)
        checked_cursor(self.insertion_roster, state)
        uint(self.member_count, 16)
        return self


@dataclass(frozen=True)
class PacketResourceContext:
    packet: Table
    roster: Cursor

    def validate(self, state):
        checked_table(self.packet, state)
        checked_cursor(self.roster, state)
        return self


@dataclass(frozen=True)
class PacketInsertionResult:
    packet: Table
    insertion_roster: Cursor
    member_count: Word


@dataclass(frozen=True)
class BattleActionContext:
    acting_officer: Word
    damage_carrier: Long
    scene: BattleSceneContext

    def validate(self, state):
        uint(self.acting_officer, 16)
        uint(self.damage_carrier, 32)
        checked_context(self.scene, BattleSceneContext, state)
        return self


@dataclass(frozen=True)
class DamagePotentialResult:
    potential: Long
    effective_damage: Long


@dataclass(frozen=True)
class NearestTerrainTarget:
    distance: Word
    officer: Word


@dataclass(frozen=True)
class BattleFlowResult:
    training_carrier: Long


@dataclass(frozen=True)
class SceneServiceContext:
    training_carrier: Long

    def validate(self, state):
        checked_state(state)
        uint(self.training_carrier, 32)
        return self


@dataclass(frozen=True)
class ProgressAllocationContext:
    """1C5E2 owns its roster/count/budget reads before its nonlocal tail."""

    def validate(self, state):
        checked_state(state)
        return self


def checked_context(value, expected, state):
    checked_state(state)
    if type(value) is not expected:
        raise ValueError('exact battle-family context required')
    return value.validate(state)


# Shared 23736 fields: full Scene calls and historical scalar projection.
# Closed ports: two existing states, the same live RAM, no third state model.
from dataclasses import replace as battle_replace
from ..high_level_scene_flows.domain import (
    SceneState, Table as SceneTable, Cursor as SceneCursor,
    checked_table as checked_scene_table,
)

TriggerTable = Table | SceneTable
TriggerCursor = Cursor | SceneCursor


class BattleTriggerMemory:
    """23736 uses existing GameplayState or SceneState bus and budgets."""

    def __init__(self, state):
        if type(state) not in (GameplayState, SceneState):
            raise ValueError('existing GameplayState or SceneState required')
        self.state = state

    @property
    def complete(self):
        return type(self.state) is SceneState

    def table(self, address):
        return self.state.table(uint(address, 32))

    def port(self, suffix):
        return self.state.table('ram_' + suffix)


@dataclass(frozen=True)
class BattleTriggerFrame:
    """23736 full D0..D7/A0..A7 and SR, using existing business names.

    Only the old GameplayState API may leave unobserved full carriers as None.
    Scene calls require all eight full LONGs and real SP. A None address view
    means the address is unobserved, not a fabricated zero address. The old
    typed damage/scene context is never fabricated for complete Scene calls.
    """

    target_x: Long | None
    target_y: Long | None
    unit: Long | None
    count: Long | None
    distance: Long | None
    offset_x: Long | None
    offset_y: Long | None
    choice: Long | None
    roster: TriggerCursor | None
    candidates: TriggerCursor | None
    controller: TriggerTable | None
    scan: TriggerCursor | None
    opponent: TriggerTable | None
    scratch: TriggerTable | None
    auxiliary: TriggerTable | None
    stack_cursor: TriggerCursor | None
    status: Word
    legacy_context: BattleActionContext | None

    def validate(self, state):
        memory = BattleTriggerMemory(state)
        for value in (self.target_x, self.target_y, self.unit, self.count,
                      self.distance, self.offset_x, self.offset_y, self.choice):
            if value is not None or memory.complete:
                uint(value, 32)
        uint(self.status, 16)
        for view in (self.roster, self.candidates, self.controller, self.scan,
                     self.opponent, self.scratch, self.auxiliary,
                     self.stack_cursor):
            if view is not None:
                if memory.complete:
                    checked_scene_table(view, state)
                else:
                    checked_table(view, state)
        for view in (self.roster, self.candidates, self.scan, self.stack_cursor):
            if view is not None and type(view) is not (SceneCursor if memory.complete else Cursor):
                raise ValueError('actual same-state cursor required')
        if memory.complete:
            if self.stack_cursor is None or self.legacy_context is not None:
                raise ValueError('complete Scene trigger requires actual SP and no legacy context')
        else:
            checked_context(self.legacy_context, BattleActionContext, state)
        return self

    def validate_complete(self, state):
        if type(state) is not SceneState:
            raise ValueError('full trigger ABI is a SceneState contract')
        return self.validate(state)

# A closed existing-state port, not a third State or a dynamic service provider.
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame, first_replace
from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
from ..high_level_battle_ai.business_formation import (
    _first_word, _first_long, _first_memory_word, _first_shift_word,
    _first_add_word, _first_right_word, _first_compare_word,
    first_deployment_random_fields,
)


class BattlePresentationMemory:
    """1A706/1A78A/1A7A2 share existing Scene or historical Gameplay RAM.

    Scene calls use the unchanged FirstDeploymentFrame validation. Historical
    scalar calls retain None for unobserved full LONGs and A7; their Gameplay
    views are checked here, without extending the deployment State union.
    """

    def __init__(self, state):
        if type(state) not in (GameplayState, SceneState):
            raise ValueError('existing same-state presentation RAM required')
        self.state = state

    def table(self, address):
        return self.state.table(uint(address, 32))

    def checked_view(self, view):
        if type(self.state) is SceneState:
            return checked_scene_table(view, self.state)
        return checked_table(view, self.state)

    def validate_frame(self, frame):
        if type(frame) is not FirstDeploymentFrame:
            raise ValueError('sole current deployment fields required')
        if type(self.state) is SceneState:
            return frame.validate(self.state, frame.stack_cursor is not None)
        for name in ('target_x', 'target_y', 'unit', 'count', 'distance',
                     'offset_x', 'offset_y', 'choice'):
            value = frame.carrier(name)
            if value is not None:
                uint(value, 32)
        for view in (frame.roster, frame.candidates, frame.controller,
                     frame.scan, frame.opponent, frame.scratch, frame.auxiliary):
            if view is not None:
                checked_table(view, self.state)
        if frame.stack_cursor is not None:
            raise ValueError('historical presentation API did not observe A7')
        if frame.status is not None:
            uint(frame.status, 8)
            if frame.status > 31:
                raise ValueError('actual five-bit CCR required')
        return frame

    def finish(self, frame):
        frame = self.validate_frame(frame)
        if frame.status is not None:
            self.state.sr = (self.state.sr & 65504) | frame.status
        return frame

    def random_fields(self, frame):
        frame = self.validate_frame(frame)
        if type(self.state) is SceneState:
            return first_deployment_random_fields(BattlePolicyMemory(self.state), frame)
        draw = self.state.sample_random_pair()
        # Old Gameplay observes the two actual RNG carriers, not RNG flags.
        # The final factor ADD.W subsequently defines all five returned flags.
        return first_replace(frame, target_x=draw.sample,
            target_y=draw.updated_state, status=None)
