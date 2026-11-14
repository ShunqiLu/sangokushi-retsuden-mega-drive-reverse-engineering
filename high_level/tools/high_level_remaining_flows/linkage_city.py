"""Confirmed finite city/roster ABI linkage on one original live SceneState.

The original call targets are identifiers, not interpreted PCs.  Providers
lazy-import genuine semantic owners.  No RAM copy, invented conditions,
default carrier, source-file read or fake external completion is performed.
"""
from dataclasses import dataclass

from .domain import (
    SceneState, Table, Long, Boundary, checked_state, checked_table,
    uint, replace_word,
)


OWNER_CONTEXT_NAMES = (
    'CityProcessCountedRecords1Service3',
    'CityProcessCountedRecords1Service5',
    'CityProcessCountedRecords1Service8',
    'CityProcessCountedRecords1Service14',
    'CityProcessCountedRecords1Service16',
    'CityProcessCountedRecords1Service19',
    'CityProcessCountedRecords1Service22',
    'CityProcessCountedRecords1Service24',
    'CityProcessCountedRecords1Service27',
    'CityProcessCountedRecords1Service29',
    'CityProcessCountedRecords1Service31',
    'CityProcessCountedRecords1Service34',
    'CityProcessCountedRecords1Service38',
    'CityProcessCountedRecords1Service40',
    'CityProcessCountedRecords1Service43',
    'CityProcessCountedRecords1Service47',
    'CityProcessCountedRecords1Service49',
    'CityProcessCountedRecords1Service52',
)
LEADER_CONTEXT_NAMES = (
    'CityUpdateRecordFlags2Service1', 'CityUpdateRecordFlags2Service8',
)
GROWTH_CONTEXT_NAMES = (
    'CityUpdateRecordFlags2Service6', 'CityUpdateRecordFlags4Service1',
    'CityUpdateRecordFlags13Service1',
)
MESSAGE_CONTEXT_NAMES = (
    'CityUpdateRecordFlags2Service7', 'CityUpdateRecordFlags4Service2',
    'CityUpdateRecordFlags13Service2',
)
COUNTER_CONTEXT_NAMES = ('CityUpdateRecordFlags13Service3', 'CityCoordinateLiveState141Service1')
RADIAL_CONTEXT_NAMES = ('CityCalculateLiveQuotient10Service1', 'CityCalculateLiveQuotient10Alternate1Service1')
TERRAIN_TARGETS = (0x1E0AE, 0x1E0B0, 0x1E0B6, 0x1E0C8, 0x1E0DA, 0x1E0E0)


@dataclass(frozen=True)
class CityTerrainCallReturn:
    """Only actual D5/D6/D7 and NZVC clobbers of the six original leaves."""
    limit: Long
    member: Long
    remaining: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        for value in (self.limit, self.member, self.remaining):
            uint(value, 32)
        if any(type(flag) is not bool for flag in
               (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('true terrain leaf conditions required')
        return self


def _radial_distance(state, context):
    """Original MOVEM preserves D1-D3/A0; the caller projects only full D0."""
    from ..high_level_battle_ai.business_geometry import rounded_scene_radial_distance
    checked_state(state)
    context.validate(state)
    return rounded_scene_radial_distance(state, context.value)


def _terrain_speed_provider(target):
    """Bind a recovered leaf, not a PC interpreter or category-derived target."""
    if target not in TERRAIN_TARGETS:
        raise ValueError('one recovered terrain leaf required')
    def apply(state, context):
        from . import business_city, contexts_city
        checked_state(state)
        if type(context) is not contexts_city.CityScaleLiveRecordValue4Service1:
            raise ValueError('exact terrain call context required')
        context.validate(state)
        conditions = dict(carry=context.carry, zero=context.zero,
                          negative=context.negative, overflow=context.overflow)
        if target == 0x1E0AE:
            result = business_city.city_update_live_fields_15(state,
                contexts_city.CityUpdateLiveFields15Input(**conditions))
            return CityTerrainCallReturn(context.limit, context.member, context.remaining,
                result.carry, result.zero, result.negative, result.overflow).validate(state)
        owner = {0x1E0B0: 16, 0x1E0B6: 17, 0x1E0C8: 18,
                 0x1E0DA: 19, 0x1E0E0: 20}[target]
        arguments = dict(member=context.member, remaining=context.remaining, **conditions)
        if owner in (17, 18):
            arguments['limit'] = context.limit
        result = getattr(business_city, 'city_update_live_fields_' + str(owner))(state,
            getattr(contexts_city, 'CityUpdateLiveFields' + str(owner) + 'Input')(**arguments))
        limit = result.limit if owner in (17, 18) else context.limit
        return CityTerrainCallReturn(limit, result.member, result.remaining,
            result.carry, result.zero, result.negative, result.overflow).validate(state)
    return apply


@dataclass(frozen=True)
class CityLeaderCallReturn:
    """Actual 11EE caller clobbers; other local values remain untouched.

    D1's high WORD is from the explicit caller field.  The last raw leader
    WORD and the two views are returned by the genuine scan, not reread.
    """
    destination: Table
    roster: Table
    value: Long
    field: Long
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state):
        checked_state(state)
        checked_table(self.destination, state)
        checked_table(self.roster, state)
        uint(self.value, 32)
        uint(self.field, 32)
        if any(type(v) is not bool for v in
               (self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('strict partial arithmetic result required')
        return self


class IncompleteCityGrowthReturn(Boundary):
    """Historical linkage07 exception; current strict providers never use it.

    The real prior DATA effects and result remain inspectable.  A4's active
    attribute view and final non-carry conditions are not fabricated.  This
    is not a success value, transaction rollback or resumed CPU frame.
    """
    def __init__(self, partial_result, caller_context):
        self.partial_result = partial_result
        self.caller_context = caller_context
        super().__init__('662E4 true growth completed; active attribute view/NZV return ABI remains unbound')


def _detect_city_owner(state, context):
    from ..high_level_main_flows.business_main import compare_campaign_owner_list
    checked_state(state)
    context.validate(state)
    return compare_campaign_owner_list(state, context.value)


def _detect_roster_leader(state, context):
    from ..high_level_main_flows.business_main import scan_unassigned_leader_roster
    checked_state(state)
    context.validate(state)
    scanned = scan_unassigned_leader_roster(state, context.value)
    return CityLeaderCallReturn(scanned.leader_cursor, scanned.assignments,
        scanned.selection, replace_word(context.field, scanned.leader_word),
        scanned.carry, scanned.zero, scanned.negative, scanned.overflow)


def _advance_city_growth(state, context):
    from ..high_level_main_flows.business_highbank import scan_officer_growth_levels
    from ..high_level_main_flows.contexts_highbank import GrowthValues, GrowthFrame
    from .contexts_city import (CityUpdateRecordFlags2Service6,
        CityUpdateRecordFlags4Service1, CityUpdateRecordFlags13Service1)
    checked_state(state)
    context.validate(state)
    if type(context) is CityUpdateRecordFlags13Service1:
        attribute_pointer, owner_pointer = context.palette, context.roster
    elif type(context) in (CityUpdateRecordFlags2Service6, CityUpdateRecordFlags4Service1):
        attribute_pointer, owner_pointer = context.attribute_pointer, context.owner_pointer
    else:
        raise Boundary('growth provider requires one of three proven caller ABIs')
    return scan_officer_growth_levels(state, GrowthFrame(
        GrowthValues(context.value, context.field, context.tile),
        attribute_pointer, owner_pointer))


def _prepare_city_message(state, context):
    from ..high_level_command_actions.business_reuse import prepare_scene_message
    from ..high_level_command_actions.contexts_message import SceneMessageInput
    from .contexts_city import (CityUpdateRecordFlags2Service7,
        CityUpdateRecordFlags4Service2, CityUpdateRecordFlags13Service2)
    from .contexts_highbank import HighbankUpdateRecordFlags1Service1
    checked_state(state)
    context.validate(state)
    if type(context) is CityUpdateRecordFlags2Service7:
        source = context.roster
    elif type(context) in (CityUpdateRecordFlags13Service2, HighbankUpdateRecordFlags1Service1):
        source = context.source
    elif type(context) is CityUpdateRecordFlags4Service2:
        source = None
    else:
        raise Boundary('message provider requires one of three proven city ABIs')
    return prepare_scene_message(state, SceneMessageInput(
        context.value, context.field, context.destination, source))


def _tick_city_single_counters(state, context):
    from ..high_level_battle_preparation.business_result import tick_scene_single_counters
    from ..high_level_battle_preparation.contexts_counter import SceneCounterInput
    from .contexts_city import CityUpdateRecordFlags13Service3
    checked_state(state)
    if type(context) is not CityUpdateRecordFlags13Service3:
        raise Boundary('one actual 1F12E counter ABI required')
    context.validate(state)
    return tick_scene_single_counters(state, SceneCounterInput(context.value, context.field, context.source))


def _tick_city_status_counters(state, context):
    from ..high_level_battle_preparation.business_result import tick_scene_status_counters
    from ..high_level_battle_preparation.contexts_counter import SceneCounterInput
    from .contexts_city import CityCoordinateLiveState141Service1
    checked_state(state)
    if type(context) is not CityCoordinateLiveState141Service1:
        raise Boundary('one actual 1FA94 counter ABI required')
    context.validate(state)
    # Entry LEA overwrites A1 before any read; no incoming source is observed.
    return tick_scene_status_counters(state, SceneCounterInput(context.value, context.field, None))


def city_service_bindings():
    """Return37 explicit context-specific authorities for13 actual targets.

    Twenty detection, three strict growth, four message, two counter,
    two radial and six true terrain-leaf ABIs expose genuine
    return carriers and continue original caller control, or propagate a genuine
    earlier Boundary. Installing these does not close every city
    external call or prove natural gameplay/stack/X/interrupt behavior.
    """
    from ..high_level_main_flows.services import ServiceBinding
    from ..high_level_main_flows.contexts_main import CampaignOwnerDetection
    from ..high_level_main_flows.contexts_highbank import FullGrowthResult
    from ..high_level_command_actions.contexts_message import SceneMessageResult
    from ..high_level_battle_preparation.contexts_counter import SceneCounterResult
    from ..high_level_battle_ai.contexts_radial import RadialDistanceFields
    from .contexts_highbank import HighbankUpdateRecordFlags1Service1
    from . import contexts_city
    return tuple(
        ServiceBinding(0x13DC, getattr(contexts_city, name),
            CampaignOwnerDetection, _detect_city_owner)
        for name in OWNER_CONTEXT_NAMES
    ) + tuple(
        ServiceBinding(0x11EE, getattr(contexts_city, name),
            CityLeaderCallReturn, _detect_roster_leader)
        for name in LEADER_CONTEXT_NAMES
    ) + tuple(
        ServiceBinding(0x662E4, getattr(contexts_city, name),
            FullGrowthResult, _advance_city_growth)
        for name in GROWTH_CONTEXT_NAMES
    ) + tuple(
        ServiceBinding(0x676F2, getattr(contexts_city, name),
            SceneMessageResult, _prepare_city_message)
        for name in MESSAGE_CONTEXT_NAMES
    ) + (
        ServiceBinding(0x676F2, HighbankUpdateRecordFlags1Service1,
            SceneMessageResult, _prepare_city_message),
        ServiceBinding(0x1F13C, contexts_city.CityUpdateRecordFlags13Service3,
            SceneCounterResult, _tick_city_single_counters),
        ServiceBinding(0x1FAA8, contexts_city.CityCoordinateLiveState141Service1,
            SceneCounterResult, _tick_city_status_counters),
    ) + tuple(
        ServiceBinding(0x3080E, getattr(contexts_city, name),
            RadialDistanceFields, _radial_distance)
        for name in RADIAL_CONTEXT_NAMES
    ) + tuple(
        ServiceBinding(target, contexts_city.CityScaleLiveRecordValue4Service1,
            CityTerrainCallReturn, _terrain_speed_provider(target))
        for target in TERRAIN_TARGETS
    )
