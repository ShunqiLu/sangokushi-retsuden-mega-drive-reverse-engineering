"""Live battlefield formation and deployment rules.

The scene, side and strength labels are probable business roles. Widths,
conditional DATA order and original wrapped arithmetic are compatibility
contracts. This is executable Python; read-only sources are supplied explicitly
through the state, never opened from a ROM or existing assembly.
"""
from .domain import (
    Boundary, Byte, CarryOutcome, Cursor, GameState, Long, Table, Word, checked_cursor, checked_state,
    checked_table, descending_inclusive, low16, negative_word, replace_byte, replace_word, u8, u16, u32, uint,
)
from .contexts_formation import (
    BattleBounds, ClosestBattleUnit, DeploymentViews, EastFormationRegion, FormationCursors,
    LeaderRank, Point, RegionDecision, RegionInput, RosterStrength, SampledFlankPoint,
    SampledFormationPoint, ShuffleSlots, WeightedDeploymentRoster,
)
from .business_geometry import (
    collect_contacts_in_speed_radius, load_battlefield_map_context,
    read_battlefield_terrain_type, select_weakest_contact_strength,
    weighted_training_factor, weighted_training_factor_fields,
)

from .contexts_policy_memory import BattlePolicyMemory, checked_policy_table
from .contexts_first_deployment import FirstDeploymentFrame, FirstLeaderFields, FirstDeploymentReturnBoundary, first_replace


def sum_first_side_roster_troops(state: GameState) -> RosterStrength:
    checked_state(state)
    _, byte_length, total = sum_first_side_roster_troops_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return RosterStrength(byte_length, total)


def test_force_has_city_assignment(state: GameState) -> CarryOutcome:
    checked_state(state)
    _, assigned = test_force_has_city_assignment_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return state.carry_result(int(assigned))


def test_second_side_total_with_single_first_roster(state: GameState) -> CarryOutcome:
    checked_state(state)
    _, selected = test_second_side_total_with_single_first_roster_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return state.carry_result(int(selected))


def test_second_side_total_with_small_second_roster(state: GameState) -> CarryOutcome:
    checked_state(state)
    _, selected = test_second_side_total_with_small_second_roster_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return state.carry_result(int(selected))


def test_point_in_battlefield_staging_rectangle(state: GameState, point: Point) -> tuple:
    """Legacy WORD-only projection of the one live rectangle core."""
    checked_state(state)
    if type(point) is not Point:
        raise ValueError('typed point required')
    frame = first_replace(FirstDeploymentFrame.unobserved(), target_x=point.x,
        target_y=point.y, unit=0, count=0, distance=0, offset_x=0,
        offset_y=0, status=state.sr & 31)
    frame = test_point_in_battlefield_staging_rectangle_fields(BattlePolicyMemory(state), frame)
    bounds = BattleBounds(low16(frame.unit), low16(frame.count),
        low16(frame.distance), low16(frame.offset_x))
    return bounds, state.carry_result(frame.status & 1)


def sample_battlefield_staging_rectangle(state: GameState, bounds: BattleBounds) -> Point:
    """Legacy coordinate projection; sampling has one actual field core."""
    checked_state(state)
    if type(bounds) is not BattleBounds:
        raise ValueError('typed bounds required')
    frame = first_replace(FirstDeploymentFrame.unobserved(), target_x=0,
        target_y=0, unit=bounds.left, count=bounds.right,
        distance=bounds.lower, offset_x=bounds.upper, status=state.sr & 31)
    frame = sample_battlefield_staging_rectangle_fields(BattlePolicyMemory(state), frame)
    return Point(low16(frame.unit), low16(frame.distance))


def read_first_side_staging_anchor(state: GameState) -> Point:
    """Legacy projection of the single 23BF4 first-side staging anchor."""
    checked_state(state)
    return read_first_side_staging_anchor_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved())[1]


def test_second_side_relative_total_shortfall(state: GameState) -> CarryOutcome:
    checked_state(state)
    _, selected = test_second_side_relative_total_shortfall_fields(
        BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return state.carry_result(int(selected))


def test_second_side_relative_total_shortfall_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, bool]:
    """23C9A: compare the live secondary total with two conditional limits.

    The second limit is read only after the first comparison succeeds. The
    actual full D0 and comparison flags return; untouched carriers stay live.
    """
    frame = _first_frame(memory, frame)
    total = memory.state.read(0xFFFFF6A2, 4)
    status = None if frame.status is None else (frame.status & 16) | (8 if total & 0x80000000 else 0) | (4 if total == 0 else 0)
    frame = first_replace(frame, target_x=total, status=status)
    primary = memory.state.read(0xFFFFF69E, 4)
    frame = _first_compare_long(frame, total, primary)
    selected = False
    if total < primary:
        limit = memory.state.read(0xFFFFF76C, 4)
        frame = _first_compare_long(frame, total, limit)
        selected = total < limit
    return _battle_roster_gate_carry(memory, frame, selected), selected


def read_second_side_staging_anchor(state: GameState) -> Point:
    """Legacy projection of the one23D54 second-side staging anchor."""
    checked_state(state)
    return read_second_side_staging_anchor_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved())[1]


def read_east_formation_region(state: GameState, context: RegionInput) -> EastFormationRegion:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    return read_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), context.origin, context.offset, 1)[1]


def east_formation_contains(point: Point, region: EastFormationRegion) -> bool:
    """Business acceptance policy, separate from carry and span conventions.

    This is intentionally one-sided in x, as in the original program. The
    compiler consumes these three unsigned comparisons, including supported
    edits to their operators, rather than treating this helper as a comment.
    """
    if type(point) is not Point or type(region) is not EastFormationRegion:
        raise ValueError('typed east formation geometry required')
    return point.x <= region.east_limit and point.y >= region.lower and point.y <= region.upper


def sample_east_formation_point(state: GameState, region: EastFormationRegion) -> SampledFormationPoint:
    checked_state(state)
    values = sample_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), region, 1)
    return SampledFormationPoint(values[1], values[3], values[4])


def sample_or_accept_east_formation_region(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = sample_or_accept_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 1, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def read_west_formation_region(state: GameState, context: RegionInput) -> BattleBounds:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    return read_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), context.origin, context.offset, 2)[1]


def west_formation_contains(point: Point, region: BattleBounds) -> bool:
    """Original one-sided west policy; there is no upper x test."""
    if type(point) is not Point or type(region) is not BattleBounds:
        raise ValueError('typed west formation geometry required')
    return point.x >= region.left and point.y >= region.lower and point.y <= region.upper


def sample_west_formation_point(state: GameState, region: BattleBounds) -> SampledFormationPoint:
    checked_state(state)
    values = sample_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), region, 2)
    return SampledFormationPoint(values[1], values[3], values[4])


def sample_or_accept_west_formation_region(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = sample_or_accept_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 2, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def read_east_flank_region(state: GameState, context: RegionInput) -> BattleBounds:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    return read_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), context.origin, context.offset, 3)[1]


def east_flank_contains(point: Point, region: BattleBounds) -> bool:
    if type(point) is not Point or type(region) is not BattleBounds:
        raise ValueError('typed east flank geometry required')
    return point.x >= region.left and point.x <= region.right and point.y >= region.lower and point.y <= region.upper


def sample_east_flank_point(state: GameState, region: BattleBounds) -> SampledFlankPoint:
    checked_state(state)
    values = sample_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), region, 3)
    return SampledFlankPoint(values[1], values[2])


def sample_or_accept_east_flank_region(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = sample_or_accept_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 3, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def read_west_flank_region(state: GameState, context: RegionInput) -> BattleBounds:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    return read_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), context.origin, context.offset, 5)[1]


def west_flank_contains(point: Point, region: BattleBounds) -> bool:
    if type(point) is not Point or type(region) is not BattleBounds:
        raise ValueError('typed west flank geometry required')
    return point.x >= region.left and point.x <= region.right and point.y >= region.lower and point.y <= region.upper


def sample_west_flank_point(state: GameState, region: BattleBounds) -> SampledFlankPoint:
    checked_state(state)
    values = sample_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), region, 5)
    return SampledFlankPoint(values[1], values[2])


def sample_or_accept_west_flank_region(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = sample_or_accept_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 5, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def read_lower_formation_region(state: GameState, context: RegionInput) -> BattleBounds:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    return read_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), context.origin, context.offset, 4)[1]


def lower_formation_contains(point: Point, region: BattleBounds) -> bool:
    if type(point) is not Point or type(region) is not BattleBounds:
        raise ValueError('typed lower formation geometry required')
    return point.x >= region.left and point.x <= region.right and point.y >= region.lower and point.y <= region.upper


def sample_lower_formation_point(state: GameState, region: BattleBounds) -> Point:
    checked_state(state)
    values = sample_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), region, 4)
    return values[1]


def sample_or_accept_lower_formation_region(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = sample_or_accept_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 4, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def read_upper_formation_region(state: GameState, context: RegionInput) -> BattleBounds:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    return read_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), context.origin, context.offset, 6)[1]


def upper_formation_contains(point: Point, region: BattleBounds) -> bool:
    if type(point) is not Point or type(region) is not BattleBounds:
        raise ValueError('typed upper formation geometry required')
    return point.x >= region.left and point.x <= region.right and point.y >= region.lower and point.y <= region.upper


def sample_upper_formation_point(state: GameState, region: BattleBounds) -> Point:
    checked_state(state)
    values = sample_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), region, 6)
    return values[1]


def sample_or_accept_upper_formation_region(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = sample_or_accept_first_formation_region_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 6, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def translate_accepted_formation_point(state: GameState, result: RegionDecision, shift: Point) -> RegionDecision:
    """Translate only an accepted result; retain the final WORD-add carry."""
    checked_state(state)
    if type(result) is not RegionDecision or type(shift) is not Point:
        raise ValueError('typed accepted formation result and shift required')
    if result.carry.carry:
        raw_y = result.point.y + shift.y
        result = result.with_point(u16(result.point.x + shift.x), u16(raw_y),
                                   state.carry_observed(int(raw_y > 65535)))
    return result


def choose_east_center_first_formation_point(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = choose_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 1, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def choose_west_center_first_formation_point(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = choose_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 2, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def choose_east_flank_first_formation_point(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = choose_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 3, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def choose_lower_center_first_formation_point(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = choose_first_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 4, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def choose_east_center_second_formation_point(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = choose_second_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 1, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def choose_west_center_second_formation_point(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = choose_second_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 2, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def choose_west_flank_second_formation_point(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = choose_second_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 5, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def choose_upper_center_second_formation_point(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = choose_second_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 6, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def choose_east_center_third_formation_point(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = choose_third_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 1, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def choose_west_center_third_formation_point(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = choose_third_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 2, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def choose_west_flank_third_formation_point(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = choose_third_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 5, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def choose_upper_center_third_formation_point(state: GameState, context: RegionInput) -> RegionDecision:
    checked_state(state)
    if type(context) is not RegionInput:
        raise ValueError('typed region input required')
    values = choose_third_formation_point_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), 6, context.origin, context.offset, context.point)
    return _first_region_legacy_decision(state, values)


def compare_actor_shifted_troop_word_to_weakest_contact(state: GameState, actor: Word) -> CarryOutcome:
    """Old API projects the one243A0 comparison, including shifted LONG+2."""
    checked_state(state)
    uint(actor, 16)
    frame = first_replace(FirstDeploymentFrame.unobserved(), choice=actor)
    frame, accepted = compare_actor_shifted_troop_word_to_weakest_contact_fields(
        BattlePolicyMemory(state), frame)
    return state.carry_result(int(accepted))


def read_outer_east_staging_anchor(state: GameState) -> Point:
    checked_state(state)
    return read_outer_east_staging_anchor_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved())[1]


def read_outer_west_staging_anchor(state: GameState) -> Point:
    checked_state(state)
    return read_outer_west_staging_anchor_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())[1]


def select_contact_nearest_deployment_anchor(state: GameState, retained_unit: Word = 0) -> ClosestBattleUnit:
    checked_state(state)
    uint(retained_unit, 16)
    return select_contact_nearest_deployment_anchor_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved(), retained_unit)[1]


def read_formation_relative_position_delta(state: GameState, retained_position: Word = 0) -> Word:
    checked_state(state)
    uint(retained_position, 16)
    return read_formation_relative_position_delta_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved(), retained_position)[1]


def test_first_side_relative_total_shortfall(state: GameState) -> CarryOutcome:
    checked_state(state)
    _, selected = test_first_side_relative_total_shortfall_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return state.carry_observed(int(selected))


def test_second_roster_type6_count_below_four(state: GameState) -> CarryOutcome:
    checked_state(state)
    _, selected = test_second_roster_type6_count_below_four_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return state.carry_observed(int(selected))


def test_second_side_threshold_shortfall(state: GameState) -> CarryOutcome:
    checked_state(state)
    _, selected = test_second_side_threshold_shortfall_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return state.carry_observed(int(selected))


def initialize_second_side_deployment(state: GameState) -> None:
    checked_state(state)
    initialize_second_side_deployment_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())


def prepare_second_side_formation_assignment(state: GameState) -> None:
    checked_state(state)
    prepare_second_side_formation_assignment_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())


def read_assignment_subroster_count(state: GameState, roster: Table) -> Word:
    checked_state(state)
    checked_table(roster, state)
    return read_first_side_assignment_count_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), roster)[1]


def sort_side_subroster_by_weighted_troops(state: GameState) -> Word:
    checked_state(state)
    return sort_first_side_roster_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())[1]


def read_weighted_deployment_roster(state: GameState) -> WeightedDeploymentRoster:
    checked_state(state)
    frame = read_first_side_weighted_roster_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return WeightedDeploymentRoster(frame.opponent, state.formation_scratch)


def weighted_deployment_product(troops: Long, factor: Long) -> Long:
    """Original MULU uses only both low WORDs, even with full LONG inputs."""
    uint(troops, 32)
    uint(factor, 32)
    return u32(low16(troops) * low16(factor))


def collect_deployment_weights(state: GameState, views: WeightedDeploymentRoster) -> Word:
    checked_state(state)
    if type(views) is not WeightedDeploymentRoster:
        raise ValueError('live weighted roster required')
    checked_table(views.roster, state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=views.roster.cursor(), candidates=views.weights.cursor(), scan=state.officer_troops.cursor())
    return collect_first_side_weight_fields(BattlePolicyMemory(state), frame)[1]


def weighted_neighbor_should_move_forward(value: Long, previous: Long) -> bool:
    uint(value, 32)
    uint(previous, 32)
    return value >= previous


def swap_live_weighted_neighbors(state: GameState, views: WeightedDeploymentRoster, offset: Word, member_offset: Word, value: Long) -> None:
    checked_state(state)
    if type(views) is not WeightedDeploymentRoster:
        raise ValueError('live weighted roster required')
    checked_table(views.roster, state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=views.roster.cursor(), candidates=views.weights.cursor())
    swap_first_side_weight_fields(BattlePolicyMemory(state), frame, offset, member_offset, value)


def order_live_weighted_roster(state: GameState, views: WeightedDeploymentRoster, count: Word) -> None:
    checked_state(state)
    if type(views) is not WeightedDeploymentRoster:
        raise ValueError('live weighted roster required')
    checked_table(views.roster, state)
    uint(count, 16)
    limit = u16(u16(count - 1) << 2)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=views.roster.cursor(), candidates=views.weights.cursor())
    order_first_side_weight_fields(BattlePolicyMemory(state), frame, count, limit)


def formation_assignment_offset(formation: Word, count: Word) -> Word:
    uint(formation, 16)
    uint(count, 16)
    return u16(u16(u16(formation << 4) + count) << 5)


def copy_live_formation_orders(state: GameState, source: Cursor, destination: Cursor) -> FormationCursors:
    checked_state(state)
    checked_cursor(source, state)
    checked_cursor(destination, state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=destination, candidates=source)
    frame = copy_first_side_order_fields(BattlePolicyMemory(state), frame)
    return FormationCursors(frame.candidates, frame.roster)


def copy_second_side_position_assignment(state: GameState, count: Word) -> FormationCursors:
    checked_state(state)
    uint(count, 16)
    frame = copy_second_side_position_assignment_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), count)
    return FormationCursors(frame.candidates, frame.roster)


def populate_second_side_unset_positions(state: GameState) -> None:
    checked_state(state)
    populate_second_side_unset_positions_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())


def deployment_position_needs_assignment(x: Word) -> bool:
    uint(x, 16)
    return x == 0


def write_live_deployment_position(state: GameState, views: DeploymentViews, offset: Word, order: Word) -> None:
    checked_state(state)
    if type(views) is not DeploymentViews:
        raise ValueError('live deployment views required')
    checked_table(views.roster, state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), controller=views.cells, scan=views.positions.cursor())
    write_unset_deployment_fields(BattlePolicyMemory(state), frame, offset, order)


def submit_unset_deployment_positions(state: GameState, views: DeploymentViews) -> None:
    checked_state(state)
    if type(views) is not DeploymentViews:
        raise ValueError('live deployment views required')
    checked_table(views.roster, state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=views.roster.cursor(), candidates=views.orders.cursor(), controller=views.cells, scan=views.positions.cursor())
    submit_unset_deployment_fields(BattlePolicyMemory(state), frame)


def prepare_second_side_battlefield_choices(state: GameState) -> FormationCursors:
    checked_state(state)
    frame = prepare_second_side_battlefield_choices_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return FormationCursors(frame.roster, frame.candidates)


def copy_choice_window_to_scratch(state: GameState, source: Cursor, count_minus_one: Word) -> Cursor:
    checked_state(state)
    checked_cursor(source, state)
    uint(count_minus_one, 16)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=source)
    frame = _second_choice_copy_window_fields(BattlePolicyMemory(state), frame, count_minus_one)
    return frame.controller


def publish_shuffled_choice_window(state: GameState, source: Cursor, destination: Cursor,
                                  count_minus_one: Word, zeros: Word) -> None:
    checked_state(state)
    checked_cursor(source, state)
    checked_cursor(destination, state)
    uint(count_minus_one, 16)
    uint(zeros, 16)
    if (count_minus_one, zeros) == (4, 3):
        continuation = 0x25280
    elif (count_minus_one, zeros) == (2, 5):
        continuation = 0x252AA
    else:
        raise Boundary('historical choice-window helper has no real source call site for this plan')
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=source, candidates=destination)
    _second_choice_publish_window_fields(BattlePolicyMemory(state), frame, count_minus_one, zeros, continuation)


def commit_second_side_selected_point(state: GameState, index: Word, chosen: Word) -> None:
    checked_state(state)
    uint(index, 16)
    uint(chosen, 16)
    _second_choice_store_selected_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), index, chosen)


def shuffle_nonzero_choice_slots(state: GameState) -> None:
    checked_state(state)
    shuffle_first_side_choice_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())


def shuffle_slots_from_sample(sample: Word) -> ShuffleSlots:
    uint(sample, 16)
    return ShuffleSlots(u16(sample & 14), u16((sample >> 4) & 14))


def swap_nonzero_choice_slots(state: GameState, choices: Table, slots: ShuffleSlots) -> None:
    checked_state(state)
    swap_nonzero_choice_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), choices, slots)


def choose_unused_second_side_point(state: GameState, source: Cursor, destination: Cursor) -> Word:
    checked_state(state)
    checked_cursor(source, state)
    checked_cursor(destination, state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=source, candidates=destination)
    frame = choose_unused_second_side_point_fields(BattlePolicyMemory(state), frame)
    return low16(frame.target_x)


def initialize_first_side_deployment(state: GameState) -> None:
    checked_state(state)
    initialize_first_side_deployment_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())


def promote_first_side_leader(state: GameState) -> Word:
    checked_state(state)
    return promote_first_side_leader_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved()).selected


def first_roster_contains_leader(state: GameState, selected: Word) -> bool:
    checked_state(state)
    return find_first_side_leader_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), selected)[1]


def leader_readiness_uses_byte_rank(readiness: Byte) -> bool:
    uint(readiness, 8)
    return readiness < 90


def leader_readiness_should_replace(readiness: Byte, best: Byte) -> bool:
    uint(readiness, 8)
    uint(best, 8)
    return readiness >= best


def leader_strength_should_replace(strength: Word, best: Word) -> bool:
    uint(strength, 16)
    uint(best, 16)
    return strength >= best


def read_wrapped_leader_strength(state: GameState, member: Word) -> Word:
    checked_state(state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), controller=state.officer_word_b200, scan=state.officer_word_b600.cursor())
    return read_first_side_strength_fields(BattlePolicyMemory(state), frame, member)[1]


def choose_first_roster_fallback_leader(state: GameState, selected: Word) -> Word:
    checked_state(state)
    return choose_first_side_leader_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), selected).selected


def move_first_side_leader_to_front(state: GameState, selected: Word) -> None:
    checked_state(state)
    move_first_side_leader_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), selected)


def prepare_first_side_formation_assignment(state: GameState) -> None:
    checked_state(state)
    prepare_first_side_assignment_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())


def copy_first_side_position_assignment(state: GameState, count: Word) -> FormationCursors:
    checked_state(state)
    frame = copy_first_side_assignment_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), count)
    return FormationCursors(frame.candidates, frame.roster)


def populate_first_side_unset_positions(state: GameState) -> None:
    checked_state(state)
    populate_first_side_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())


def prepare_first_side_battlefield_choices(state: GameState) -> FormationCursors:
    checked_state(state)
    frame = prepare_first_side_choices_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return FormationCursors(frame.roster, frame.candidates)


def prepare_first_side_reserve_choices(state: GameState, source: Cursor) -> None:
    checked_state(state)
    checked_cursor(source, state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=source)
    prepare_first_side_reserve_fields(BattlePolicyMemory(state), frame)


def submit_first_side_reserve_choices(state: GameState, destination: Cursor) -> None:
    checked_state(state)
    checked_cursor(destination, state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), candidates=destination)
    submit_first_side_reserve_fields(BattlePolicyMemory(state), frame)


def choose_unused_first_side_point(state: GameState, source: Cursor, destination: Cursor) -> Word:
    checked_state(state)
    checked_cursor(source, state)
    checked_cursor(destination, state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=source, candidates=destination)
    returned = choose_unused_first_side_fields(BattlePolicyMemory(state), frame)
    return low16(returned.target_x)


def _first_frame(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('one same-state deployment memory and actual frame required')
    return frame.validate(memory.state, type(memory.state) is not GameState)


def _first_word(frame: FirstDeploymentFrame, name, value: Word) -> FirstDeploymentFrame:
    uint(value, 16)
    retained = frame.carrier(name)
    value_carrier = None if retained is None else replace_word(retained, value)
    status = None if frame.status is None else ((frame.status & 16) | (8 if value & 32768 else 0) | (4 if value == 0 else 0))
    return first_replace(frame, **{name: value_carrier}, status=status)


def _first_byte(frame: FirstDeploymentFrame, name, value: Byte) -> FirstDeploymentFrame:
    uint(value, 8)
    retained = frame.carrier(name)
    carrier = None if retained is None else replace_byte(retained, value)
    status = None if frame.status is None else ((frame.status & 16) | (8 if value & 128 else 0) | (4 if value == 0 else 0))
    return first_replace(frame, **{name: carrier}, status=status)


def _first_transfer_word(frame: FirstDeploymentFrame, destination, source) -> FirstDeploymentFrame:
    carrier = frame.carrier(source)
    if carrier is None:
        return first_replace(frame, **{destination: None}, status=None)
    return _first_word(frame, destination, low16(carrier))


def _first_shift_word(frame: FirstDeploymentFrame, name, original: Word, count: Word) -> FirstDeploymentFrame:
    uint(original, 16)
    uint(count, 16)
    if not 1 <= count <= 8:
        raise ValueError('original bounded WORD shift required')
    value = u16(original << count)
    bit = bool(original & (1 << (16 - count)))
    retained = frame.carrier(name)
    carrier = None if retained is None else replace_word(retained, value)
    status = (17 if bit else 0) | (8 if value & 32768 else 0) | (4 if value == 0 else 0)
    return first_replace(frame, **{name: carrier}, status=status)


def _first_add_word(frame: FirstDeploymentFrame, name, left: Word, right: Word) -> FirstDeploymentFrame:
    uint(left, 16)
    uint(right, 16)
    wide = left + right
    value = u16(wide)
    overflow = not (left ^ right) & 32768 and bool((left ^ value) & 32768)
    retained = frame.carrier(name)
    carrier = None if retained is None else replace_word(retained, value)
    status = (17 if wide > 65535 else 0) | (2 if overflow else 0) | (8 if value & 32768 else 0) | (4 if value == 0 else 0)
    return first_replace(frame, **{name: carrier}, status=status)


def _first_compare_word(frame: FirstDeploymentFrame, left: Word, right: Word) -> FirstDeploymentFrame:
    uint(left, 16)
    uint(right, 16)
    value = u16(left - right)
    overflow = bool((left ^ right) & (left ^ value) & 32768)
    status = None if frame.status is None else ((frame.status & 16) | (1 if left < right else 0) | (2 if overflow else 0) | (8 if value & 32768 else 0) | (4 if value == 0 else 0))
    return first_replace(frame, status=status)


def _first_counter_end(frame: FirstDeploymentFrame, name) -> FirstDeploymentFrame:
    """DBRA termination changes the low WORD only, never the flags."""
    retained = frame.carrier(name)
    carrier = None if retained is None else replace_word(retained, 65535)
    return first_replace(frame, **{name: carrier})


def _first_memory_word(frame: FirstDeploymentFrame, value: Word) -> FirstDeploymentFrame:
    """A memory-to-memory MOVE.W changes NZVC, not a D carrier."""
    uint(value, 16)
    status = None if frame.status is None else ((frame.status & 16) | (8 if value & 32768 else 0) | (4 if value == 0 else 0))
    return first_replace(frame, status=status)


def _first_call(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, continuation: Long, algorithm) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    uint(continuation, 32)
    if frame.stack_cursor is None:
        return algorithm(memory, frame)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    returned = algorithm(memory, first_replace(frame, stack_cursor=stack))
    returned = _first_frame(memory, returned)
    target = returned.stack_cursor.long()
    if target != continuation:
        raise FirstDeploymentReturnBoundary(target, returned, continuation)
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))


def _first_pending_call(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, target: Long, continuation: Long) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    if frame.stack_cursor is None:
        raise ValueError('legacy incomplete callee cannot produce a complete field return')
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    called = first_replace(frame, stack_cursor=stack)
    memory.state.sr = (memory.state.sr & 65504) | called.status
    returned = memory.state.service_at(target, called)
    if type(returned) is not FirstDeploymentFrame:
        raise ValueError('genuine deployment callee must return complete current fields')
    returned = _first_frame(memory, returned)
    actual_target = returned.stack_cursor.long()
    if actual_target != continuation:
        raise FirstDeploymentReturnBoundary(actual_target, returned, continuation)
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))


def find_first_side_leader_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, selected: Word) -> tuple[FirstDeploymentFrame, bool]:
    frame = _first_frame(memory, frame)
    uint(selected, 16)
    roster = memory.state.table(0xFFFFA550).cursor()
    frame = first_replace(frame, roster=roster)
    while True:
        member = roster.next_word()
        frame = _first_word(frame, 'target_y', member)
        if negative_word(member):
            return frame, False
        frame = _first_compare_word(frame, member, selected)
        if member == selected:
            return frame, True


def choose_first_side_leader_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, selected: Word) -> FirstLeaderFields:
    frame = _first_frame(memory, frame)
    uint(selected, 16)
    roster = memory.state.table(0xFFFFA550).cursor()
    readiness = memory.state.table(0xFFFFC300).cursor()
    skill = memory.state.table(0xFFFFB200)
    loyalty = memory.state.table(0xFFFFB600)
    frame = first_replace(frame, roster=roster, candidates=readiness, controller=skill, scan=loyalty.cursor())
    frame = _first_word(_first_word(frame, 'target_y', 0), 'unit', 0)
    best_readiness, best_strength = 0, 0
    while True:
        member = roster.next_word()
        frame = _first_word(frame, 'offset_y', member)
        if negative_word(member):
            return FirstLeaderFields(frame, selected)
        rank = readiness.byte(member)
        frame = _first_byte(frame, 'count', rank)
        if leader_readiness_uses_byte_rank(rank):
            if leader_readiness_should_replace(rank, best_readiness):
                best_readiness = rank
                selected = member
                frame = _first_byte(frame, 'target_y', rank)
                frame = _first_word(frame, 'target_x', selected)
        else:
            frame, strength = read_first_side_strength_fields(memory, frame, member)
            if leader_strength_should_replace(strength, best_strength):
                selected = member
                best_readiness, best_strength = rank, strength
                frame = _first_word(frame, 'target_x', selected)
                frame = _first_transfer_word(frame, 'target_y', 'count')
                frame = _first_word(frame, 'unit', strength)


def read_first_side_strength_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, member: Word) -> tuple[FirstDeploymentFrame, Word]:
    frame = _first_frame(memory, frame)
    uint(member, 16)
    checked_policy_table(frame.controller, memory.state)
    checked_policy_table(frame.scan, memory.state)
    frame = _first_word(frame, 'distance', member)
    frame = _first_shift_word(frame, 'distance', member, 1)
    offset = u16(member << 1)
    first = frame.controller.word(offset)
    frame = _first_word(frame, 'offset_x', first)
    second = frame.scan.word(offset)
    frame = _first_add_word(frame, 'offset_x', first, second)
    return frame, u16(first + second)


def move_first_side_leader_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, selected: Word) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    uint(selected, 16)
    head = memory.state.table(0xFFFFA027)
    scene = memory.battle_scene()
    frame = _first_word(frame, 'target_y', scene)
    head.set_byte(scene, u8(selected))
    source = memory.state.table(0xFFFFA550).cursor()
    destination = memory.state.table(0xFFFFA550).cursor()
    frame = first_replace(frame, roster=source, candidates=destination)
    pending = selected
    frame = _first_word(frame, 'unit', pending)
    while True:
        member = source.next_word()
        frame = _first_word(frame, 'target_y', member)
        if negative_word(member):
            break
        frame = _first_compare_word(frame, member, selected)
        if member == selected:
            continue
        destination.append_word(pending)
        frame = _first_word(frame, 'unit', member)
        pending = member
    frame = _first_compare_word(frame, member, selected)
    if member != selected:
        destination.put_word(pending)
        frame = _first_word(frame, 'unit', pending)
    return frame


def promote_first_side_leader_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstLeaderFields:
    frame = _first_frame(memory, frame)
    force = memory.state.read(0xFFFFF68C, 2)
    frame = _first_word(frame, 'target_x', force)
    frame = _first_shift_word(frame, 'target_x', force, 1)
    rulers = memory.state.table(0xFFFFE640).cursor()
    selected = rulers.word(u16(force << 1))
    frame = _first_word(frame, 'target_x', selected)
    frame = first_replace(frame, candidates=rulers)
    frame, found = find_first_side_leader_fields(memory, frame, selected)
    if not found:
        result = choose_first_side_leader_fields(memory, frame, selected)
        frame, selected = result.frame, result.selected
    frame = move_first_side_leader_fields(memory, frame, selected)
    return FirstLeaderFields(frame, selected)


def _first_promote_frame(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return promote_first_side_leader_fields(memory, frame).frame


def copy_first_side_assignment_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, count: Word) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    uint(count, 16)
    force = memory.state.read(0xFFFFF68C, 2)
    frame = _first_word(frame, 'target_x', force)
    frame = _first_shift_word(frame, 'target_x', force, 1)
    directory = memory.state.table(0x24BE4)
    formation = directory.word(u16(force << 1))
    frame = _first_word(frame, 'target_x', formation)
    frame = _first_shift_word(frame, 'target_x', formation, 4)
    intermediate = u16(formation << 4)
    frame = _first_add_word(frame, 'target_x', intermediate, count)
    intermediate = u16(intermediate + count)
    frame = _first_shift_word(frame, 'target_x', intermediate, 5)
    offset = formation_assignment_offset(formation, count)
    destination = memory.state.table(0xFFFFAF82).cursor()
    source = memory.state.table(0x2546C).cursor(offset)
    frame = first_replace(frame, roster=destination, candidates=source)
    return copy_first_side_order_fields(memory, frame)


def copy_first_side_order_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    destination, source = frame.roster, frame.candidates
    checked_policy_table(destination, memory.state)
    checked_policy_table(source, memory.state)
    for _ in range(10):
        word = source.next_word()
        destination.append_word(word)
        frame = first_replace(frame, status=None if frame.status is None else ((frame.status & 16) | (8 if word & 32768 else 0) | (4 if word == 0 else 0)))
    return frame


def prepare_first_side_assignment_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    roster = memory.state.table(0xFFFFA550)
    frame, count = read_first_side_assignment_count_fields(memory, frame, roster)
    return _first_call(memory, frame, 0x25436, lambda memory, frame: copy_first_side_assignment_fields(memory, frame, count))


def read_first_side_assignment_count_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, roster, continuation: Long=0x25422) -> tuple[FirstDeploymentFrame, Word]:
    frame = _first_frame(memory, frame)
    if continuation not in (0x25422, 0x24B14):
        raise ValueError('actual first/second assignment sort continuation required')
    checked_policy_table(roster, memory.state)
    third = roster.word(4)
    frame = _first_memory_word(frame, third)
    if not negative_word(third):
        second = roster.word(2)
        frame = _first_memory_word(frame, second)
        if not negative_word(second):
            if type(memory.state) is GameState and frame.stack_cursor is None:
                frame, count = sort_first_side_roster_fields(memory, frame)
            else:
                frame = _first_call(memory, frame, continuation, _first_sorted_frame)
                count = low16(frame.unit)
            return frame, count
    count = 0
    frame = _first_word(frame, 'unit', count)
    second = roster.word(2)
    frame = _first_memory_word(frame, second)
    if not negative_word(second):
        frame = _first_add_word(frame, 'unit', count, 1)
        count = 1
    return frame, count


def first_side_choice_prefix_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    scene = memory.battle_scene()
    frame = _first_word(frame, 'target_x', scene)
    frame = _first_word(frame, 'target_y', scene)
    offset = scene
    for shift in (1, 2, 1):
        frame = _first_shift_word(frame, 'target_x', offset, shift)
        offset = u16(offset << shift)
        frame = _first_add_word(frame, 'target_x', offset, scene)
        offset = u16(offset + scene)
    frame = _first_shift_word(frame, 'target_x', offset, 2)
    source = memory.state.table(0xAC75E).cursor(u16(offset << 2))
    destination = memory.state.table(0xFFFFD310).cursor()
    choice = u16(memory.state.read(0xFFFFF61C, 2) & 2)
    frame = _first_word(frame, 'target_x', choice)
    destination.append_word(source.word(choice))
    if choice == 0:
        frame = _first_add_word(frame, 'target_x', choice, 1)
        choice = 1
    scene = memory.battle_scene()
    frame = _first_word(frame, 'target_y', scene)
    variant = memory.state.table(0xFFFF9FFF)
    variant.set_byte(scene, u8(choice))
    source.base = source.advance(4).base
    clear = destination.cursor()
    frame = first_replace(frame, roster=source, candidates=destination, controller=clear, auxiliary=variant)
    frame = _first_word(frame, 'target_x', 7)
    for _ in descending_inclusive(7):
        clear.word()
        clear.append_word(0)
    frame = _first_counter_end(frame, 'target_x')
    return first_replace(frame, status=None if frame.status is None else ((frame.status & 16) | 4))


def prepare_first_side_choices_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = first_side_choice_prefix_fields(memory, frame)
    source, destination = frame.roster, frame.candidates
    for continuation in (0x25B04, 0x25B08, 0x25B0C, 0x25B10, 0x25B14, 0x25B18, 0x25B1C, 0x25B20):
        frame = _first_call(memory, frame, continuation, choose_unused_first_side_fields)
        source, destination = frame.roster, frame.candidates
    frame = prepare_first_side_reserve_fields(memory, frame)
    return submit_first_side_reserve_fields(memory, frame)


def prepare_first_side_reserve_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    source = frame.roster
    checked_policy_table(source, memory.state)
    scratch = memory.state.table(0xFFFFD300).cursor()
    frame = first_replace(frame, controller=scratch)
    if memory.battle_scene() != 23:
        frame = _first_word(frame, 'target_x', 3)
        for _ in descending_inclusive(3):
            scratch.word(0, 8)
            scratch.set_word(0, 0, 8)
            word = source.next_word()
            scratch.append_word(word)
            frame = _first_memory_word(frame, word)
        frame = _first_counter_end(frame, 'target_x')
        continuation = 0x25B40
    else:
        frame = _first_word(frame, 'target_x', 7)
        for _ in descending_inclusive(7):
            scratch.word()
            scratch.put_word(0)
            frame = _first_memory_word(frame, 0)
        frame = _first_counter_end(frame, 'target_x')
        if memory.state.read(0xFFFFD311, 1) >= 20:
            source.base = source.advance(4).base
        word = source.word()
        memory.state.table(0xFFFFD300).set_word(0, word)
        frame = _first_memory_word(frame, word)
        word = source.word(2)
        memory.state.table(0xFFFFD300).set_word(2, word)
        frame = _first_memory_word(frame, word)
        continuation = 0x25B6E
    return _first_call(memory, frame, continuation, shuffle_first_side_choice_fields)


def submit_first_side_reserve_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    destination = frame.candidates
    checked_policy_table(destination, memory.state)
    scratch = memory.state.table(0xFFFFD300)
    selected = memory.state.table(0x00FF3ECA)
    word = scratch.word()
    destination.append_word(word)
    frame = _first_memory_word(frame, word)
    word = scratch.word()
    selected.set_word(0, word)
    frame = _first_memory_word(frame, word)
    word = scratch.word(2)
    destination.put_word(word)
    frame = _first_memory_word(frame, word)
    word = scratch.word(2)
    selected.set_word(2, word)
    return _first_memory_word(frame, word)


def populate_first_side_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _first_call(memory, frame, 0x25A70, prepare_first_side_choices_fields)
    roster = memory.state.table(0xFFFFA550).cursor()
    orders = memory.state.table(0xFFFFAF82).cursor()
    cells = memory.state.table(0xFFFFD310)
    positions = memory.state.table(0xFFFFA150)
    frame = first_replace(frame, roster=roster, candidates=orders, controller=cells, scan=positions.cursor())
    return submit_unset_deployment_fields(memory, frame)


def submit_unset_deployment_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """The shared actual roster/order/cell loop, independent of side selection."""
    frame = _first_frame(memory, frame)
    roster, orders, cells, positions = frame.roster, frame.candidates, frame.controller, frame.scan
    checked_policy_table(roster, memory.state)
    checked_policy_table(orders, memory.state)
    checked_policy_table(cells, memory.state)
    checked_policy_table(positions, memory.state)
    while True:
        member = roster.next_word()
        frame = _first_word(frame, 'target_x', member)
        if negative_word(member):
            return frame
        frame = _first_shift_word(frame, 'target_x', member, 2)
        offset = u16(member << 2)
        order = orders.next_word()
        frame = _first_word(frame, 'target_y', order)
        frame = _first_shift_word(frame, 'target_y', order, 1)
        order = u16(order << 1)
        if deployment_position_needs_assignment(positions.word(offset)):
            frame = write_unset_deployment_fields(memory, frame, offset, order)


def write_unset_deployment_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, offset: Word, order: Word) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    uint(offset, 16)
    uint(order, 16)
    cells, positions = frame.controller, frame.scan
    checked_policy_table(cells, memory.state)
    checked_policy_table(positions, memory.state)
    for displacement in (0, 1):
        frame = _first_word(frame, 'unit', 0)
        value = cells.byte(order, displacement)
        frame = _first_byte(frame, 'unit', value)
        frame = _first_shift_word(frame, 'unit', value, 3)
        frame = _first_shift_word(frame, 'unit', u16(value << 3), 7)
        positions.set_word(offset, u16(value << 10), displacement * 2)
    return frame


def initialize_first_side_deployment_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    frame = _first_call(memory, frame, 0x2536E, _first_promote_frame)
    frame = _first_call(memory, frame, 0x25372, prepare_first_side_assignment_fields)
    return _first_call(memory, frame, 0x25376, populate_first_side_fields)


def _first_long(frame: FirstDeploymentFrame, name, value: Long) -> FirstDeploymentFrame:
    uint(value, 32)
    status = None if frame.status is None else ((frame.status & 16) | (8 if value & 2147483648 else 0) | (4 if value == 0 else 0))
    return first_replace(frame, **{name: value}, status=status)


def _first_sub_word(frame: FirstDeploymentFrame, name, left: Word, right: Word) -> FirstDeploymentFrame:
    uint(left, 16)
    uint(right, 16)
    value = u16(left - right)
    retained = frame.carrier(name)
    carrier = None if retained is None else replace_word(retained, value)
    overflow = bool((left ^ right) & (left ^ value) & 32768)
    status = (17 if left < right else 0) | (2 if overflow else 0) | (8 if value & 32768 else 0) | (4 if value == 0 else 0)
    return first_replace(frame, **{name: carrier}, status=status)


def _first_right_word(frame: FirstDeploymentFrame, name, original: Word, count: Word) -> FirstDeploymentFrame:
    uint(original, 16)
    uint(count, 16)
    if not 1 <= count <= 8:
        raise ValueError('bounded original WORD shift required')
    value = original >> count
    bit = bool(original & (1 << (count - 1)))
    retained = frame.carrier(name)
    carrier = None if retained is None else replace_word(retained, value)
    status = (17 if bit else 0) | (4 if value == 0 else 0)
    return first_replace(frame, **{name: carrier}, status=status)


def _first_compare_long(frame: FirstDeploymentFrame, left: Long, right: Long) -> FirstDeploymentFrame:
    uint(left, 32)
    uint(right, 32)
    value = u32(left - right)
    overflow = bool((left ^ right) & (left ^ value) & 2147483648)
    status = None if frame.status is None else ((frame.status & 16) | (1 if left < right else 0) | (2 if overflow else 0) | (8 if value & 2147483648 else 0) | (4 if value == 0 else 0))
    return first_replace(frame, status=status)


def first_deployment_random_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('same-state RNG memory and actual frame required')
    frame.validate(memory.state, frame.stack_cursor is not None)
    sample = memory.sample_random_pair()
    uint(sample.sample, 32)
    uint(sample.updated_state, 32)
    # The retained RNG result exposes the actual final seed and D0, so the
    # original final ADD.W carry is derived without rereading seed RAM.
    high_mixed = low16(sample.updated_state)
    low_mixed = u16(low16(sample.sample) - high_mixed)
    extend = low_mixed + high_mixed > 65535
    status = (16 if extend else 0) | (8 if sample.updated_state & 2147483648 else 0) | (4 if sample.updated_state == 0 else 0)
    return first_replace(frame, target_x=sample.sample, target_y=sample.updated_state, status=status)


def shuffle_first_side_choice_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    choices = memory.state.table(0xFFFFD300).cursor()
    frame = first_replace(frame, controller=choices)
    frame = _first_word(frame, 'unit', 15)
    for counter in descending_inclusive(15):
        frame = _first_call(memory, frame, 0x25308, first_deployment_random_fields)
        sample = low16(frame.target_x)
        frame = _first_transfer_word(frame, 'target_y', 'target_x')
        slots = shuffle_slots_from_sample(sample)
        frame = _first_word(frame, 'target_x', slots.first)
        frame = _first_right_word(frame, 'target_y', sample, 4)
        frame = _first_word(frame, 'target_y', slots.second)
        frame = swap_nonzero_choice_fields(memory, frame, choices, slots)
        # DBRA publishes its real next low WORD to the following callee entry;
        # it never changes the last TST/MOVE flags or the retained upper WORD.
        retained = frame.unit
        frame = first_replace(frame, unit=None if retained is None else replace_word(retained, u16(counter - 1)))
    return _first_counter_end(frame, 'unit')


def swap_nonzero_choice_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, choices, slots: ShuffleSlots) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    checked_policy_table(choices, memory.state)
    if type(slots) is not ShuffleSlots:
        raise ValueError('typed shuffle slots required')
    first = choices.word(slots.first)
    frame = _first_memory_word(frame, first)
    if first == 0:
        return frame
    second = choices.word(slots.second)
    frame = _first_memory_word(frame, second)
    if second == 0:
        return frame
    first = choices.word(slots.first)
    frame = _first_word(frame, 'count', first)
    second = choices.word(slots.second)
    choices.set_word(slots.first, second)
    frame = _first_memory_word(frame, second)
    choices.set_word(slots.second, first)
    return _first_memory_word(frame, first)


def choose_unused_first_side_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    source, destination = frame.roster, frame.candidates
    checked_policy_table(source, memory.state)
    checked_policy_table(destination, memory.state)
    choices = memory.state.table(0xFFFFD300).cursor()
    frame = first_replace(frame, controller=choices)
    frame = _first_word(frame, 'target_x', 5)
    for _ in descending_inclusive(5):
        word = source.next_word()
        choices.append_word(word)
        frame = _first_memory_word(frame, word)
    frame = _first_counter_end(frame, 'target_x')
    choices.word()
    choices.append_word(0)
    frame = _first_memory_word(frame, 0)
    choices.word()
    choices.put_word(0)
    frame = _first_memory_word(frame, 0)
    frame = _first_call(memory, frame, 0x25B9E, shuffle_first_side_choice_fields)
    choices = memory.state.table(0xFFFFD300).cursor()
    frame = first_replace(frame, controller=choices)
    deployed = memory.state.table(0xFFFFD310)
    while True:
        candidate = choices.next_word()
        frame = _first_word(frame, 'target_x', candidate)
        duplicate = False
        for offset in range(2, 18, 2):
            previous = deployed.word(offset)
            frame = _first_compare_word(frame, candidate, previous)
            if candidate == previous:
                duplicate = True
                break
        if not duplicate:
            destination.append_word(candidate)
            return _first_memory_word(frame, candidate)


def sort_first_side_roster_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, Word]:
    frame = read_first_side_weighted_roster_fields(memory, frame)
    frame, count = collect_first_side_weight_fields(memory, frame)
    frame = _first_transfer_word(frame, 'target_x', 'unit')
    frame = _first_sub_word(frame, 'target_x', count, 1)
    limit = u16(u16(count - 1) << 2)
    frame = _first_shift_word(frame, 'target_x', u16(count - 1), 2)
    frame = _first_word(frame, 'count', 0)
    weights = memory.state.table(0xFFFFD300).cursor()
    roster = frame.opponent.cursor()
    frame = first_replace(frame, roster=roster, candidates=weights)
    return order_first_side_weight_fields(memory, frame, count, limit), count


def read_first_side_weighted_roster_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    alternate = bool(memory.state.read(0xFFFFF6D7, 1) & 2)
    selected = memory.state.table(0xFFFFA5A6 if alternate else 0xFFFFA552)
    frame = first_replace(frame, roster=selected.cursor(), candidates=memory.state.table(0xFFFFD300).cursor(),
        controller=memory.state.table(0xFFFFB400), scan=memory.state.table(0xFFFFC800).cursor(),
        opponent=selected, auxiliary=memory.state.table(0xFFFFEA88))
    return frame


def collect_first_side_weight_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, Word]:
    frame = _first_frame(memory, frame)
    source, weights = frame.roster, frame.candidates
    checked_policy_table(source, memory.state)
    checked_policy_table(weights, memory.state)
    checked_policy_table(frame.scan, memory.state)
    frame = _first_word(frame, 'unit', 0)
    count = 0
    while True:
        member = source.next_word()
        frame = _first_word(frame, 'target_x', member)
        if negative_word(member):
            break
        frame = _first_add_word(frame, 'unit', count, 1)
        count = u16(count + 1)
        frame = _first_call(memory, frame, 0x24B5E, lambda memory, frame: _first_training_frame(memory, frame, member))
        # BAC8's MOVEM may change the current D0 or source A0 through a real
        # saved-slot alias. Use the actual restored fields, never member/source.
        source = frame.roster
        current = member if type(memory.state) is GameState and frame.target_x is None else low16(frame.target_x)
        frame = _first_shift_word(frame, 'target_x', current, 2)
        troops = frame.scan.long(u16(current << 2))
        frame = _first_long(frame, 'target_x', troops)
        product = weighted_deployment_product(troops, frame.target_y)
        frame = _first_long(frame, 'target_x', product)
        weights = frame.candidates
        weights.append_long(product)
    return frame, count


def order_first_side_weight_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, count: Word, limit: Word) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    uint(count, 16)
    uint(limit, 16)
    start = 0
    while True:
        offset = limit
        frame = _first_word(frame, 'distance', offset)
        frame = _first_word(frame, 'target_y', offset)
        member_offset = u16(offset >> 1)
        frame = _first_right_word(frame, 'target_y', offset, 1)
        frame = _first_word(frame, 'offset_x', start)
        while True:
            value = frame.candidates.long(offset)
            frame = _first_long(frame, 'offset_y', value)
            previous = frame.candidates.long(offset, -4)
            frame = _first_compare_long(frame, value, previous)
            if weighted_neighbor_should_move_forward(value, previous):
                frame = swap_first_side_weight_fields(memory, frame, offset, member_offset, value)
            frame = _first_sub_word(frame, 'distance', offset, 4)
            offset = u16(offset - 4)
            frame = _first_sub_word(frame, 'target_y', member_offset, 2)
            member_offset = u16(member_offset - 2)
            frame = _first_compare_word(frame, offset, start)
            if not offset > start:
                break
        frame = _first_add_word(frame, 'count', start, 4)
        start = u16(start + 4)
        frame = _first_compare_word(frame, start, limit)
        if not start < limit:
            return frame


def swap_first_side_weight_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, offset: Word, member_offset: Word, value: Long) -> FirstDeploymentFrame:
    frame = _first_frame(memory, frame)
    uint(offset, 16)
    uint(member_offset, 16)
    uint(value, 32)
    previous = frame.candidates.long(offset, -4)
    frame.candidates.set_long(offset, previous)
    frame = _first_long(frame, 'offset_y', value)
    frame.candidates.set_long(offset, value, -4)
    member = frame.roster.word(member_offset)
    frame = _first_word(frame, 'offset_y', member)
    previous_member = frame.roster.word(member_offset, -2)
    frame.roster.set_word(member_offset, previous_member)
    frame = _first_memory_word(frame, previous_member)
    frame.roster.set_word(member_offset, member, -2)
    return _first_memory_word(frame, member)


def _first_training_frame(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, member: Word) -> FirstDeploymentFrame:
    return weighted_training_factor_fields(memory, frame, member).frame


def _first_sorted_frame(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return sort_first_side_roster_fields(memory, frame)[0]


# Complete actual239D6/239F4 fields, shared by legacy projections.
def sum_first_side_roster_troops_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, Word, Long]:
    """239D6: one live roster algorithm for historical and complete callers.

    The count is bytes, not members. D2.W retains its real high WORD; D3 is
    fully overwritten by MOVEQ. The negative terminating D5 is returned.
    """
    frame = _first_frame(memory, frame)
    roster = memory.state.table(0xFFFFA550).cursor()
    troops = memory.state.table(0xFFFFC800).cursor()
    frame = first_replace(frame, roster=roster, candidates=troops)
    frame = _first_word(frame, 'unit', 0)
    frame = first_replace(frame, count=0, status=None if frame.status is None else (frame.status & 16) | 4)
    byte_length, total = 0, 0
    while True:
        member = roster.next_word()
        frame = _first_word(frame, 'offset_x', member)
        if negative_word(member):
            return frame, byte_length, total
        frame = _first_add_word(frame, 'unit', byte_length, 2)
        byte_length = u16(byte_length + 2)
        frame = _first_shift_word(frame, 'offset_x', member, 2)
        amount = troops.long(u16(member << 2))
        wide = total + amount
        value = u32(wide)
        overflow = bool((~(total ^ amount)) & (total ^ value) & 2147483648)
        status = (17 if wide > 4294967295 else 0) | (8 if value & 2147483648 else 0) | (4 if value == 0 else 0) | (2 if overflow else 0)
        total = value
        frame = first_replace(frame, count=total, status=status)


def test_force_has_city_assignment_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, bool]:
    """239F4: scan exactly forty live city owner BYTEs, descending.

    DBRA changes only D4.W. Every CMP.B supplies real NZVC while preserving
    X; the full-SR privilege/trace operation is left at its original point.
    """
    frame = _first_frame(memory, frame)
    frame = _first_word(frame, 'distance', 39)
    force = memory.state.read(0xFFFFF68C, 2)
    frame = _first_word(frame, 'target_x', force)
    owners = memory.state.table(0xFFFFF428).cursor()
    frame = first_replace(frame, roster=owners)
    for city in descending_inclusive(39):
        owner = owners.byte(city)
        left = u8(force)
        difference = u8(left - owner)
        overflow = bool((left ^ owner) & (left ^ difference) & 128)
        status = None if frame.status is None else ((frame.status & 16) | (1 if left < owner else 0) | (2 if overflow else 0) | (8 if difference & 128 else 0) | (4 if difference == 0 else 0))
        frame = first_replace(frame, status=status)
        if left == owner:
            return _order_city_assignment_carry(memory, frame, True), True
        if frame.distance is not None:
            frame = first_replace(frame, distance=replace_word(frame.distance, u16(city - 1)))
    return _order_city_assignment_carry(memory, frame, False), False


def _order_city_assignment_carry(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, assigned: bool) -> FirstDeploymentFrame:
    if type(assigned) is not bool:
        raise ValueError('actual city assignment result required')
    if not memory.state.sr & 8192:
        raise Boundary('original city-assignment full-SR operation requires supervisor')
    if memory.state.sr & 32768:
        raise Boundary('original city-assignment trace continuation unmodeled')
    status = None if frame.status is None else ((frame.status & 30) | int(assigned))
    return first_replace(frame, status=status)


# Original23A1A/23A3C: one strength/roster gate core per entry.
def _read_second_side_strength_gate_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, bool]:
    """Shared23A1A/23A3C prefix: actual fullD0 and ordered LONG comparison."""
    frame = _first_frame(memory, frame)
    total = memory.state.read(0xFFFFF6A2, 4)
    status = None if frame.status is None else (frame.status & 16) | (8 if total & 2147483648 else 0) | (4 if total == 0 else 0)
    frame = first_replace(frame, target_x=total, status=status)
    limit = memory.state.read(0xFFFFF76C, 4)
    frame = _first_compare_long(frame, total, limit)
    return frame, total >= limit


def _battle_roster_gate_carry(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, selected: bool) -> FirstDeploymentFrame:
    """Actual privileged ORI/ANDI full-SR leaf, retaining every non-C bit."""
    if type(selected) is not bool:
        raise ValueError('actual strength/roster gate decision required')
    if not memory.state.sr & 8192:
        raise Boundary('original strength gate full-SR operation requires supervisor')
    if memory.state.sr & 32768:
        raise Boundary('original strength gate trace continuation unmodeled')
    status = None if frame.status is None else (frame.status & 30) | int(selected)
    return first_replace(frame, status=status)


def test_second_side_total_with_single_first_roster_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, bool]:
    """23A1A: compare force totals, then only conditionally test A552.W.

    D0 is the full actual total, not a retained high-WORD guess. All address
    carriers remain unchanged; the final CMP/TST supplies real NZV and X.
    """
    frame, enough_strength = _read_second_side_strength_gate_fields(memory, frame)
    selected = False
    if enough_strength:
        second = memory.state.read(0xFFFFA552, 2)
        frame = _first_memory_word(frame, second)
        selected = negative_word(second)
    return _battle_roster_gate_carry(memory, frame, selected), selected


def test_second_side_total_with_small_second_roster_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, bool]:
    """23A3C: stop at the first negative of three live secondary-roster WORDs.

    Reads are conditional and ordered; a Python eager any/list does not
    replace the original three TST/branch steps or final flag authority.
    """
    frame, enough_strength = _read_second_side_strength_gate_fields(memory, frame)
    selected = False
    if enough_strength:
        for address in (0xFFFFA5A6, 0xFFFFA5A8, 0xFFFFA5AA):
            member = memory.state.read(address, 2)
            frame = _first_memory_word(frame, member)
            if negative_word(member):
                selected = True
                break
    return _battle_roster_gate_carry(memory, frame, selected), selected


def test_point_in_battlefield_staging_rectangle_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """23B08: bounded staging area, exact conditional reads and final carry.

    The special scene keeps its original reversed horizontal bounds. Bound
    coordinates occupy the real four retained WORD carriers; complete callers
    retain their upper words and the unchanged incoming point.
    """
    frame = _first_frame(memory, frame)
    frame = _first_word(frame, 'offset_y', memory.state.read(0xFFFFF68A, 2))
    frame = first_replace(frame, roster=memory.state.table(0xAE2F6).cursor())
    frame = _first_shift_word(frame, 'offset_y', low16(frame.offset_y), 2)
    offset = low16(frame.offset_y)
    frame = _first_compare_word(frame, offset, 92)
    frame = _first_word(frame, 'unit', frame.roster.word(offset))
    frame = _first_transfer_word(frame, 'count', 'unit')
    if offset != 92:
        frame = _first_sub_word(frame, 'unit', low16(frame.unit), 4096)
        if frame.status & 1:
            frame = _first_word(frame, 'unit', 3072)
        else:
            frame = _first_compare_word(frame, low16(frame.unit), 3072)
            if frame.status & 1:
                frame = _first_word(frame, 'unit', 3072)
        frame = _first_add_word(frame, 'count', low16(frame.count), 4096)
        if frame.status & 1:
            frame = _first_word(frame, 'count', 25600)
        else:
            frame = _first_compare_word(frame, low16(frame.count), 25600)
            if not frame.status & 5:
                frame = _first_word(frame, 'count', 25600)
        frame = _first_word(frame, 'distance', frame.roster.word(offset, 2))
        frame = _first_transfer_word(frame, 'offset_x', 'distance')
        frame = _first_compare_word(frame, low16(frame.distance), 20480)
        if frame.status & 1:
            frame = _first_add_word(frame, 'offset_x', low16(frame.offset_x), 14336)
        else:
            frame = _first_sub_word(frame, 'distance', low16(frame.distance), 14336)
    else:
        frame = _first_sub_word(frame, 'count', low16(frame.count), 13312)
        frame = _first_word(frame, 'distance', frame.roster.word(offset, 2))
        frame = _first_transfer_word(frame, 'offset_x', 'distance')
        frame = _first_sub_word(frame, 'distance', low16(frame.distance), 3072)
        frame = _first_add_word(frame, 'offset_x', low16(frame.offset_x), 3072)
    for coordinate, limit, lower_bound in (
            (frame.target_x, frame.unit, True),
            (frame.target_x, frame.count, False),
            (frame.target_y, frame.distance, True),
            (frame.target_y, frame.offset_x, False)):
        frame = _first_compare_word(frame, low16(coordinate), low16(limit))
        outside = bool(frame.status & 1) if lower_bound else not bool(frame.status & 5)
        if outside:
            return _battle_roster_gate_carry(memory, frame, False)
    return _battle_roster_gate_carry(memory, frame, True)


def _staging_scaled_sample_fields(frame: FirstDeploymentFrame, span: Word) -> FirstDeploymentFrame:
    """Original sample masking, unsigned multiply and full-LONG word swap."""
    uint(span, 16)
    frame = _first_long(frame, 'target_x', low16(frame.target_x))
    frame = _first_long(frame, 'target_x', low16(frame.target_x) * span)
    product = frame.target_x
    swapped = u32((low16(product) << 16) | (product >> 16))
    return _first_long(frame, 'target_x', swapped)


def sample_battlefield_staging_rectangle_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """23BA6: two actual random calls and a wrapped sampled coordinate pair."""
    frame = _first_frame(memory, frame)
    frame = _first_sub_word(frame, 'count', low16(frame.count), low16(frame.unit))
    frame = _first_call(memory, frame, 0x23BAE, first_deployment_random_fields)
    frame = _staging_scaled_sample_fields(frame, low16(frame.count))
    frame = _first_add_word(frame, 'unit', low16(frame.unit), low16(frame.target_x))
    frame = _first_sub_word(frame, 'offset_x', low16(frame.offset_x), low16(frame.distance))
    frame = _first_sub_word(frame, 'offset_x', low16(frame.offset_x), 3072)
    frame = _first_call(memory, frame, 0x23BC6, first_deployment_random_fields)
    frame = _staging_scaled_sample_fields(frame, low16(frame.offset_x))
    frame = first_replace(frame, roster=memory.state.table(0xAE2F6).cursor())
    frame = _first_word(frame, 'target_y', memory.state.read(0xFFFFF68A, 2))
    frame = _first_shift_word(frame, 'target_y', low16(frame.target_y), 2)
    frame = _first_compare_word(frame, frame.roster.word(low16(frame.target_y), 2), 20480)
    lower_side = bool(frame.status & 1)
    frame = _first_add_word(frame, 'distance', low16(frame.distance), low16(frame.target_x))
    if lower_side:
        frame = _first_add_word(frame, 'distance', low16(frame.distance), 3072)
    return frame


def _formation_position_frame(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('same-state position memory and sole actual frame required')
    return frame.validate(memory.state, frame.stack_cursor is not None)


def _formation_position_enter(frame: FirstDeploymentFrame, continuation: Long) -> FirstDeploymentFrame:
    uint(continuation, 32)
    if frame.stack_cursor is None:
        return frame
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    return first_replace(frame, stack_cursor=stack)


def _formation_position_leave(frame: FirstDeploymentFrame, continuation: Long) -> FirstDeploymentFrame:
    uint(continuation, 32)
    if frame.stack_cursor is None:
        return frame
    stack = frame.stack_cursor
    target = stack.long()
    if target != continuation:
        raise FirstDeploymentReturnBoundary(target, frame, continuation)
    return first_replace(frame, stack_cursor=stack.advance(4))


def _formation_position_carry(memory: BattlePolicyMemory, frame: FirstDeploymentFrame,
        enabled: bool) -> FirstDeploymentFrame:
    """Only the real full-SR carry instruction; original X/N/Z/V survive."""
    if type(enabled) is not bool:
        raise ValueError('actual position carry outcome required')
    if type(memory.state) is not GameState:
        if not memory.state.sr & 8192:
            raise Boundary('original position full-SR operation requires supervisor')
        if memory.state.sr & 32768:
            raise Boundary('position trace continuation remains unmodeled')
    status = None if frame.status is None else ((frame.status & 30) | int(enabled))
    if type(memory.state) is not GameState and status is not None:
        memory.state.sr = (memory.state.sr & 65504) | status
    return first_replace(frame, status=status)


def compare_actor_shifted_troop_word_to_weakest_contact_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """confirmed243A0..243DC: original strength policy and physical D0/D1 save.

    The LONG read is actor*4+2, deliberately not normalized to the ordinary
    troop LONG at actor*4. No original anomaly is repaired here.
    """
    from .business_geometry import collect_contacts_in_speed_radius_fields, select_weakest_contact_strength_fields
    frame = _formation_position_frame(memory, frame)
    uint(frame.choice, 32)
    retained_x, retained_y = frame.target_x, frame.target_y
    stack = frame.stack_cursor
    if stack is not None:
        stack = stack.advance(-4)
        stack.set_long(0, retained_y)
        stack = stack.advance(-4)
        stack.set_long(0, retained_x)
        frame = first_replace(frame, stack_cursor=stack)
    entered = _formation_position_enter(frame, 0x243A8)
    frame = collect_contacts_in_speed_radius_fields(memory, entered).frame
    frame = _formation_position_leave(frame, 0x243A8)
    contacts = memory.state.read(0xFFFFD300, 2)
    frame = _first_memory_word(frame, contacts)
    accepted = False
    if not negative_word(contacts):
        entered = _formation_position_enter(frame, 0x243B4)
        frame = select_weakest_contact_strength_fields(memory, entered,
            0 if entered.count is None else low16(entered.count),
            0 if entered.target_y is None else entered.target_y)[0]
        frame = _formation_position_leave(frame, 0x243B4)
        actor = low16(frame.choice)
        frame = _first_word(frame, 'target_x', actor)
        entered = _formation_position_enter(frame, 0x243BC)
        frame = weighted_training_factor_fields(memory, entered, actor).frame
        frame = _formation_position_leave(frame, 0x243BC)
        actor = actor if frame.target_x is None else low16(frame.target_x)
        frame = _first_shift_word(frame, 'target_x', actor, 2)
        troops = frame.candidates.long(u16(actor << 2), 2)
        frame = first_replace(frame, target_x=troops)
        frame = _first_long(frame, 'target_x', troops)
        strength = low16(troops) * low16(frame.target_y)
        frame = _first_long(frame, 'target_x', strength)
        frame = _first_compare_long(frame, frame.unit, strength)
        accepted = frame.unit <= strength
    frame = _formation_position_carry(memory, frame, accepted)
    stack = frame.stack_cursor
    if stack is not None:
        retained_x = stack.long()
        stack = stack.advance(4)
        retained_y = stack.long()
        stack = stack.advance(4)
    frame = first_replace(frame, target_x=retained_x, target_y=retained_y, stack_cursor=stack)
    return frame, accepted


def read_outer_east_staging_anchor_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """confirmed2443E..24488: scene anchor plus original asymmetric offsets."""
    frame = _formation_position_frame(memory, frame)
    origin = memory.state.table(0xAE2F6).cursor()
    frame = first_replace(frame, roster=origin)
    scene = memory.battle_scene()
    frame = _first_word(frame, 'target_x', scene)
    offset = u16(scene << 2)
    frame = _first_shift_word(frame, 'target_x', scene, 2)
    frame = _first_compare_word(frame, offset, 92)
    x = origin.word(offset)
    frame = _first_word(frame, 'unit', x)
    if offset == 92:
        frame = _first_sub_word(frame, 'unit', x, 3968)
        x = u16(x - 3968)
        y = origin.word(offset, 2)
        frame = _first_word(frame, 'distance', y)
        frame = _first_add_word(frame, 'distance', y, 3072)
        y = u16(y + 3072)
    else:
        frame = _first_add_word(frame, 'unit', x, 3072)
        x = u16(x + 3072)
        y = origin.word(offset, 2)
        frame = _first_word(frame, 'distance', y)
        frame = _first_compare_word(frame, y, 20480)
        if y >= 20480:
            frame = _first_sub_word(frame, 'distance', y, 3968)
            y = u16(y - 3968)
        else:
            frame = _first_add_word(frame, 'distance', y, 3968)
            y = u16(y + 3968)
    return frame, Point(x, y)


# Sole full first-region field algorithms and scalar projections.
def _first_region_context(memory: BattlePolicyMemory, frame: FirstDeploymentFrame,
        origin = None, offset = None, point = None) -> tuple:
    """Complete Scene fields or explicit legacy WORD observations, same RAM."""
    frame = _first_frame(memory, frame)
    if origin is None:
        origin = frame.roster
    checked_policy_table(origin, memory.state)
    if offset is None:
        uint(frame.unit, 32)
        offset = low16(frame.unit)
    uint(offset, 16)
    if point is None:
        uint(frame.target_x, 32)
        uint(frame.target_y, 32)
        point = Point(low16(frame.target_x), low16(frame.target_y))
    if type(point) is not Point:
        raise ValueError('actual first formation point WORDs required')
    return frame, origin, offset, point

def _first_region_publish(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    if frame.status is not None:
        memory.state.sr = (memory.state.sr & 65504) | frame.status
    return frame

def _first_region_carry(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, enabled: bool) -> FirstDeploymentFrame:
    """Reuse the one physical full-SR carry writer, after actual current flags."""
    from .business_actions import _deployment_carry
    frame = _first_region_publish(memory, frame)
    return _deployment_carry(memory, frame, enabled)

def read_first_formation_region_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, origin, offset: Word, kind: int) -> tuple:
    """Sole six first/second-side region-limit algorithms, in original DATA order.

    kind1/2 are east/west centers;3/5 east/west flank;4/6 lower/upper.
    Legacy projections retain missing upper LONGs and SP as unobserved.
    """
    frame = _first_frame(memory, frame)
    checked_policy_table(origin, memory.state)
    uint(offset, 16)
    if kind not in (1, 2, 3, 4, 5, 6):
        raise ValueError('one actual first formation region required')
    anchor_x = origin.word(offset)
    frame = _first_word(frame, 'count', anchor_x)
    if kind == 3:
        frame = _first_add_word(frame, 'count', anchor_x, 3968)
        left = u16(anchor_x + 3968)
        frame = _first_word(frame, 'distance', left)
        frame = _first_add_word(frame, 'distance', left, 8320)
        right = u16(left + 8320)
        if frame.status & 1:
            right = 25600
            frame = _first_word(frame, 'distance', right)
        else:
            frame = _first_compare_word(frame, right, 25600)
            if right > 25600:
                right = 25600
                frame = _first_word(frame, 'distance', right)
    else:
        frame = _first_word(frame, 'distance', anchor_x)
        if kind == 1:
            left, right = anchor_x, u16(anchor_x + 14336)
            frame = _first_add_word(frame, 'distance', anchor_x, 14336)
        elif kind == 2:
            left, right = u16(anchor_x - 14336), anchor_x
            frame = _first_sub_word(frame, 'count', anchor_x, 14336)
        elif kind == 5:
            right = u16(anchor_x - 3968)
            frame = _first_sub_word(frame, 'distance', anchor_x, 3968)
            left = u16(anchor_x - 12288)
            frame = _first_sub_word(frame, 'count', anchor_x, 12288)
            if frame.status & 1:
                left = 3072
                frame = _first_word(frame, 'count', left)
            else:
                frame = _first_compare_word(frame, left, 3072)
                if left < 3072:
                    left = 3072
                    frame = _first_word(frame, 'count', left)
        else:
            left, right = u16(anchor_x - 3072), u16(anchor_x + 3072)
            frame = _first_sub_word(frame, 'count', anchor_x, 3072)
            frame = _first_add_word(frame, 'distance', anchor_x, 3072)
    anchor_y = origin.word(offset, 2)
    frame = _first_word(frame, 'offset_x', anchor_y)
    if kind in (3, 5):
        frame = _first_compare_word(frame, anchor_y, 20480)
        frame = _first_word(frame, 'offset_y', anchor_y)
        lower, upper = anchor_y, anchor_y
        if anchor_y >= 20480:
            lower = u16(anchor_y - 14336)
            frame = _first_sub_word(frame, 'offset_x', anchor_y, 14336)
        else:
            upper = u16(anchor_y + 14336)
            frame = _first_add_word(frame, 'offset_y', anchor_y, 14336)
    else:
        frame = _first_word(frame, 'offset_y', anchor_y)
        if kind == 4:
            lower, upper = u16(anchor_y - 13312), anchor_y
            frame = _first_sub_word(frame, 'offset_x', anchor_y, 13312)
        elif kind == 6:
            lower, upper = anchor_y, u16(anchor_y + 13312)
            frame = _first_add_word(frame, 'offset_y', anchor_y, 13312)
        else:
            lower, upper = u16(anchor_y - 4096), u16(anchor_y + 4096)
            frame = _first_sub_word(frame, 'offset_x', anchor_y, 4096)
            frame = _first_compare_word(frame, lower, 3072)
            if lower < 3072:
                lower = 3072
                frame = _first_word(frame, 'offset_x', lower)
            frame = _first_add_word(frame, 'offset_y', anchor_y, 4096)
            frame = _first_compare_word(frame, upper, 37888)
            if upper > 37888:
                upper = 37888
                frame = _first_word(frame, 'offset_y', upper)
    region = EastFormationRegion(left, right, lower, upper) if kind == 1 else BattleBounds(left, right, lower, upper)
    return _first_region_publish(memory, frame), region

def _first_region_acceptance_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame,
        point: Point, region, kind: int) -> tuple:
    """Retain the existing editable policy; publish its original ordered CMPs."""
    if kind == 1:
        accepted = east_formation_contains(point, region)
        comparisons = ((point.x, region.east_limit, False),
            (point.y, region.lower, True), (point.y, region.upper, False))
    elif kind == 2:
        accepted = west_formation_contains(point, region)
        comparisons = ((point.x, region.left, True),
            (point.y, region.lower, True), (point.y, region.upper, False))
    elif kind == 3:
        accepted = east_flank_contains(point, region)
        comparisons = ((point.x, region.left, True), (point.x, region.right, False),
            (point.y, region.lower, True), (point.y, region.upper, False))
    elif kind == 4:
        accepted = lower_formation_contains(point, region)
        comparisons = ((point.x, region.left, True), (point.x, region.right, False),
            (point.y, region.lower, True), (point.y, region.upper, False))
    elif kind == 5:
        accepted = west_flank_contains(point, region)
        comparisons = ((point.x, region.left, True), (point.x, region.right, False),
            (point.y, region.lower, True), (point.y, region.upper, False))
    elif kind == 6:
        accepted = upper_formation_contains(point, region)
        comparisons = ((point.x, region.left, True), (point.x, region.right, False),
            (point.y, region.lower, True), (point.y, region.upper, False))
    else:
        raise ValueError('one original first or second formation policy required')
    for value, bound, minimum in comparisons:
        frame = _first_compare_word(frame, value, bound)
        outside = value < bound if minimum else value > bound
        if outside:
            break
    return _first_region_publish(memory, frame), accepted

def _first_region_draw(memory: BattlePolicyMemory, frame: FirstDeploymentFrame,
        continuation: Long, multiplier: Word, swapped: bool = True) -> FirstDeploymentFrame:
    """One existing RNG, actual return slot, mask, MULU and optional SWAP."""
    frame = _first_region_publish(memory, frame)
    frame = _first_call(memory, frame, continuation, first_deployment_random_fields)
    frame = _first_long(frame, 'target_x', frame.target_x & 65535)
    frame = _first_long(frame, 'target_x', low16(frame.target_x) * uint(multiplier, 16))
    if swapped:
        sample = frame.target_x
        frame = _first_long(frame, 'target_x', u32((sample << 16) | (sample >> 16)))
    return _first_region_publish(memory, frame)

def sample_first_formation_point_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, region, kind: int) -> tuple:
    """Sole sampling algorithm; lower and upper Y retain the original low product."""
    frame = _first_frame(memory, frame)
    if kind == 1:
        if type(region) is not EastFormationRegion:
            raise ValueError('east first formation limits required')
        first_return, second_return = 0x23ECA, 0x23EE4
        initial_x, horizontal = region.anchor_x, region.east_limit
    elif kind in (2, 3, 4, 5, 6):
        if type(region) is not BattleBounds:
            raise ValueError('first formation wrapped bounds required')
        first_return, second_return = ((0x23F56, 0x23F72) if kind == 2 else
            (0x2401E, 0x24034) if kind == 3 else (0x24098, 0x240AC) if kind == 4 else
            (0x24250, 0x24264) if kind == 5 else (0x242C8, 0x242DC))
        initial_x, horizontal = region.left, region.right
    else:
        raise ValueError('one actual first formation sampler required')
    vertical = region.upper
    if kind in (3, 5):
        # Original first draw precedes the D4-D3 span mutation.
        frame = _first_region_publish(memory, frame)
        frame = _first_call(memory, frame, first_return, first_deployment_random_fields)
        frame = _first_long(frame, 'target_x', frame.target_x & 65535)
        horizontal = u16(region.right - region.left)
        frame = _first_sub_word(frame, 'distance', region.right, region.left)
        frame = _first_long(frame, 'target_x', low16(frame.target_x) * horizontal)
        product = frame.target_x
        frame = _first_long(frame, 'target_x', u32((product << 16) | (product >> 16)))
        x = u16(initial_x + low16(frame.target_x))
        frame = _first_add_word(frame, 'count', initial_x, low16(frame.target_x))
        if kind == 3:
            frame = _first_add_word(frame, 'count', x, 1)
            x = u16(x + 1)
    else:
        frame = _first_region_draw(memory, frame, first_return, 6144 if kind in (4, 6) else 8192)
        draw = low16(frame.target_x)
        if kind == 2:
            frame = _first_word(frame, 'count', region.right)
            frame = _first_sub_word(frame, 'count', region.right, draw)
            x = u16(region.right - draw)
            frame = _first_sub_word(frame, 'count', x, 3072)
            x = u16(x - 3072)
        else:
            frame = _first_add_word(frame, 'count', initial_x, draw)
            x = u16(initial_x + draw)
            if kind == 1:
                frame = _first_add_word(frame, 'count', x, 3072)
                x = u16(x + 3072)
    if kind in (1, 2):
        vertical = u16(region.upper - region.lower)
        frame = _first_sub_word(frame, 'offset_y', region.upper, region.lower)
        frame = _first_region_draw(memory, frame, second_return, vertical)
    else:
        frame = _first_region_draw(memory, frame, second_return,
            6144 if kind in (4, 6) else 8192, kind not in (4, 6))
    draw = low16(frame.target_x)
    frame = _first_add_word(frame, 'offset_x', region.lower, draw)
    y = u16(region.lower + draw)
    carry = bool(frame.status & 1)
    if kind in (3, 4, 5, 6):
        frame = _first_region_carry(memory, frame, False)
        carry = False
    return _first_region_publish(memory, frame), Point(x, y), horizontal, vertical, carry

def sample_or_accept_first_formation_region_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, kind: int, origin = None,
        offset = None, point = None) -> tuple:
    """One region decision core; both complete and legacy interfaces share it."""
    frame, origin, offset, point = _first_region_context(memory, frame, origin, offset, point)
    frame, region = read_first_formation_region_fields(memory, frame, origin, offset, kind)
    frame, accepted = _first_region_acceptance_fields(memory, frame, point, region, kind)
    if accepted:
        frame = _first_region_carry(memory, frame, True)
        x = region.anchor_x if kind == 1 else region.left
        horizontal = region.east_limit if kind == 1 else region.right
        return frame, Point(x, region.lower), horizontal, region.upper, True
    return sample_first_formation_point_fields(memory, frame, region, kind)

def choose_first_formation_point_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, kind: int, origin = None,
        offset = None, point = None) -> tuple:
    """Original first-center wrapper transforms only an actual carry result."""
    frame, origin, offset, point = _first_region_context(memory, frame, origin, offset, point)
    continuation = 0x23E6C if kind == 1 else 0x23EF6 if kind == 2 else 0x23F84 if kind == 3 else 0x2404C if kind == 4 else None
    uint(continuation, 32)
    frame = _first_region_publish(memory, frame)
    entered = _formation_position_enter(frame, continuation)
    frame, result, horizontal, vertical, carry = sample_or_accept_first_formation_region_fields(memory,
        entered, kind, origin, offset, point)
    frame = _formation_position_leave(frame, continuation)
    if carry:
        if kind == 1:
            frame = _first_add_word(frame, 'count', result.x, 3968)
            x = u16(result.x + 3968)
            frame = _first_add_word(frame, 'offset_x', result.y, 3072)
            y = u16(result.y + 3072)
        elif kind == 2:
            frame = _first_word(frame, 'count', horizontal)
            frame = _first_sub_word(frame, 'count', horizontal, 3968)
            x = u16(horizontal - 3968)
            frame = _first_add_word(frame, 'offset_x', result.y, 3072)
            y = u16(result.y + 3072)
        elif kind == 3:
            # Original accepted flank wrapper makes a new live second-WORD read.
            anchor_y = origin.word(offset, 2)
            frame = _first_compare_word(frame, anchor_y, 20480)
            x = result.x
            if anchor_y >= 20480:
                frame = _first_word(frame, 'offset_x', vertical)
                frame = _first_sub_word(frame, 'offset_x', vertical, 1024)
                y = u16(vertical - 1024)
            else:
                frame = _first_add_word(frame, 'offset_x', result.y, 1024)
                y = u16(result.y + 1024)
        else:
            frame = _first_add_word(frame, 'count', result.x, 4096)
            x = u16(result.x + 4096)
            frame = _first_add_word(frame, 'offset_x', result.y, 9344)
            y = u16(result.y + 9344)
        result, carry = Point(x, y), bool(frame.status & 1)
    return _first_region_publish(memory, frame), result, horizontal, vertical, carry

def _first_region_legacy_decision(state: GameState, values: tuple) -> RegionDecision:
    frame, point, horizontal, vertical, carry = values
    return RegionDecision(point, horizontal, vertical, state.carry_observed(int(carry)))

def sample_or_accept_east_formation_region_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return sample_or_accept_first_formation_region_fields(memory, frame, 1)

def choose_east_center_first_formation_point_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return choose_first_formation_point_fields(memory, frame, 1)

def sample_or_accept_west_formation_region_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return sample_or_accept_first_formation_region_fields(memory, frame, 2)

def choose_west_center_first_formation_point_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return choose_first_formation_point_fields(memory, frame, 2)

def sample_or_accept_east_flank_region_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return sample_or_accept_first_formation_region_fields(memory, frame, 3)

def choose_east_flank_first_formation_point_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return choose_first_formation_point_fields(memory, frame, 3)

def sample_or_accept_lower_formation_region_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return sample_or_accept_first_formation_region_fields(memory, frame, 4)

def choose_lower_center_first_formation_point_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return choose_first_formation_point_fields(memory, frame, 4)


def read_first_side_staging_anchor_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """confirmed 23BF4..23C3E: first-side anchor with original WORD wrapping.

    Scene 23 selects the exceptional offsets. Other scenes use the original
    vertical half-plane choice. The live D0, D2, D4 and A0 return together;
    unobserved upper bits and untouched fields are not fabricated.
    """
    frame = _formation_position_frame(memory, frame)
    origin = memory.state.table(0xAE2F6).cursor()
    frame = first_replace(frame, roster=origin)
    scene = memory.battle_scene()
    frame = _first_word(frame, 'target_x', scene)
    offset = u16(scene << 2)
    frame = _first_shift_word(frame, 'target_x', scene, 2)
    frame = _first_compare_word(frame, offset, 92)
    x = origin.word(offset)
    frame = _first_word(frame, 'unit', x)
    if offset == 92:
        frame = _first_sub_word(frame, 'unit', x, 4096)
        x = u16(x - 4096)
        y = origin.word(offset, 2)
        frame = _first_word(frame, 'distance', y)
        frame = _first_sub_word(frame, 'distance', y, 1152)
        y = u16(y - 1152)
    else:
        frame = _first_sub_word(frame, 'unit', x, 1024)
        x = u16(x - 1024)
        y = origin.word(offset, 2)
        frame = _first_word(frame, 'distance', y)
        frame = _first_compare_word(frame, y, 20480)
        if y >= 20480:
            frame = _first_sub_word(frame, 'distance', y, 3968)
            y = u16(y - 3968)
        else:
            frame = _first_add_word(frame, 'distance', y, 3968)
            y = u16(y + 3968)
    return frame, Point(x, y)


# Second-region wrappers share the sole field region/RNG phases.
def choose_second_formation_point_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, kind: int, origin = None,
        offset = None, point = None) -> tuple:
    return choose_lateral_formation_point_fields(memory, frame, kind, 2, origin, offset, point)

def sample_or_accept_west_flank_region_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return sample_or_accept_first_formation_region_fields(memory, frame, 5)

def sample_or_accept_upper_formation_region_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return sample_or_accept_first_formation_region_fields(memory, frame, 6)

def choose_east_center_second_formation_point_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return choose_second_formation_point_fields(memory, frame, 1)

def choose_west_center_second_formation_point_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return choose_second_formation_point_fields(memory, frame, 2)

def choose_west_flank_second_formation_point_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return choose_second_formation_point_fields(memory, frame, 5)

def choose_upper_center_second_formation_point_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return choose_second_formation_point_fields(memory, frame, 6)


def select_contact_nearest_deployment_anchor_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, retained_unit: Word | None = None) -> tuple:
    """confirmed24926..24990: first minimum WORD Manhattan distance wins."""
    from .business_geometry import _contact_difference
    frame = _formation_position_frame(memory, frame)
    if retained_unit is None:
        uint(frame.target_y, 32)
        retained_unit = low16(frame.target_y)
    uint(retained_unit, 16)
    positions = memory.state.table(0xFFFFA150).cursor()
    source = memory.state.table(0xFFFFD300).cursor()
    cells = memory.deployment_cells.cursor()
    variants = memory.scene_variants.cursor()
    frame = first_replace(frame, roster=positions, candidates=source,
        controller=cells, scan=variants)
    scene = memory.battle_scene()
    frame = _first_word(frame, 'target_x', scene)
    frame = _first_word(frame, 'target_y', 0)
    variant = variants.byte(scene)
    frame = _first_byte(frame, 'target_y', variant)
    frame = _first_shift_word(frame, 'target_x', scene, 5)
    frame = _first_shift_word(frame, 'target_y', variant, 1)
    offset = u16(u16(scene << 5) + u16(variant << 1))
    frame = _first_add_word(frame, 'target_x', u16(scene << 5), u16(variant << 1))
    frame = _first_word(frame, 'unit', 0)
    x = cells.byte(offset)
    frame = _first_byte(frame, 'unit', x)
    frame = _first_shift_word(frame, 'unit', x, 3)
    frame = _first_shift_word(frame, 'unit', u16(x << 3), 7)
    anchor_x = u16(x << 10)
    frame = _first_word(frame, 'count', 0)
    y = cells.byte(offset, 1)
    frame = _first_byte(frame, 'count', y)
    frame = _first_shift_word(frame, 'count', y, 3)
    frame = _first_shift_word(frame, 'count', u16(y << 3), 7)
    anchor_y = u16(y << 10)
    # Original D1 has already become variant*2 before the sentinel scan.
    # An empty list does not retain the incoming selection WORD.
    distance, selected = 65535, u16(variant << 1)
    frame = _first_word(frame, 'target_x', distance)
    while True:
        source = frame.candidates
        member = source.word()
        frame = first_replace(frame, candidates=source.advance(2))
        frame = _first_word(frame, 'distance', member)
        if negative_word(member):
            return frame, ClosestBattleUnit(distance, selected)
        offset = u16(member << 2)
        frame = _first_shift_word(frame, 'distance', member, 2)
        x = frame.roster.word(offset)
        frame = _first_word(frame, 'offset_x', x)
        frame, dx = _contact_difference(frame, x, anchor_x)
        frame = first_replace(frame, offset_x=None if frame.offset_x is None else replace_word(frame.offset_x, dx))
        y = frame.roster.word(offset, 2)
        frame = _first_word(frame, 'offset_y', y)
        frame, dy = _contact_difference(frame, y, anchor_y)
        frame = first_replace(frame, offset_y=None if frame.offset_y is None else replace_word(frame.offset_y, dy))
        frame = _first_add_word(frame, 'offset_x', dx, dy)
        candidate = u16(dx + dy)
        frame = _first_compare_word(frame, candidate, distance)
        if candidate >= distance:
            continue
        distance = candidate
        frame = _first_word(frame, 'target_x', candidate)
        frame = _first_right_word(frame, 'distance', offset, 2)
        selected = offset >> 2
        frame = _first_word(frame, 'target_y', selected)


def read_formation_relative_position_delta_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, retained_position: Word | None = None) -> tuple:
    """confirmed24990..249F4: unchanged mode>=9 and original packed-cell wrap."""
    frame = _formation_position_frame(memory, frame)
    if retained_position is None:
        uint(frame.unit, 32)
        retained_position = low16(frame.unit)
    uint(retained_position, 16)
    mode = memory.state.read(0xFFFFF770, 2)
    frame = _first_word(frame, 'target_x', mode)
    frame = _first_compare_word(frame, mode, 9)
    if mode >= 9:
        return frame, retained_position
    offset = u16(mode << 2)
    frame = _first_shift_word(frame, 'target_x', mode, 2)
    deltas = memory.state.table(0x249F0).cursor()
    frame = first_replace(frame, roster=deltas)
    dx = deltas.word(offset)
    frame = _first_word(frame, 'target_y', dx)
    dy = deltas.word(offset, 2)
    frame = _first_word(frame, 'unit', dy)
    variants = memory.scene_variants.cursor()
    frame = first_replace(frame, roster=variants)
    scene = memory.battle_scene()
    frame = _first_word(frame, 'target_x', scene)
    frame = _first_word(frame, 'count', 0)
    variant = variants.byte(scene)
    frame = _first_byte(frame, 'count', variant)
    cells = memory.deployment_cells.cursor()
    frame = first_replace(frame, roster=cells)
    frame = _first_shift_word(frame, 'target_x', scene, 5)
    frame = _first_shift_word(frame, 'count', variant, 1)
    offset = u16(u16(scene << 5) + u16(variant << 1))
    frame = _first_add_word(frame, 'target_x', u16(scene << 5), u16(variant << 1))
    frame = _first_word(frame, 'count', 0)
    x = cells.byte(offset)
    frame = _first_byte(frame, 'count', x)
    frame = _first_compare_word(frame, x, 14)
    if x <= 14:
        frame = _first_sub_word(frame, 'target_y', 0, dx)
        dx = u16(-dx)
    frame = _first_word(frame, 'distance', 0)
    y = cells.byte(offset, 1)
    frame = _first_byte(frame, 'distance', y)
    frame = _first_compare_word(frame, y, 20)
    if y >= 20:
        frame = _first_sub_word(frame, 'unit', 0, dy)
        dy = u16(-dy)
    frame = _first_add_word(frame, 'count', x, dx)
    x = u16(x + dx)
    frame = _first_add_word(frame, 'distance', y, dy)
    y = u16(y + dy)
    frame = _first_word(frame, 'unit', x)
    frame = _first_shift_word(frame, 'unit', x, 8)
    frame = _first_word(frame, 'distance', u16(y & 255))
    packed = u16(u16(x << 8) | u8(y))
    frame = _first_word(frame, 'unit', packed)
    return frame, packed


def read_second_side_staging_anchor_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """confirmed23D54..23D9E: live anchor and original wrapped side offsets."""
    frame = _formation_position_frame(memory, frame)
    origin = memory.state.table(0xAE2F6).cursor()
    frame = first_replace(frame, roster=origin)
    scene = memory.battle_scene()
    frame = _first_word(frame, 'target_x', scene)
    offset = u16(scene << 2)
    frame = _first_shift_word(frame, 'target_x', scene, 2)
    frame = _first_compare_word(frame, offset, 92)
    x = origin.word(offset)
    frame = _first_word(frame, 'unit', x)
    if offset == 92:
        frame = _first_sub_word(frame, 'unit', x, 4096)
        x = u16(x - 4096)
        y = origin.word(offset, 2)
        frame = _first_word(frame, 'distance', y)
        frame = _first_add_word(frame, 'distance', y, 1152)
        y = u16(y + 1152)
    else:
        frame = _first_add_word(frame, 'unit', x, 1024)
        x = u16(x + 1024)
        y = origin.word(offset, 2)
        frame = _first_word(frame, 'distance', y)
        frame = _first_compare_word(frame, y, 20480)
        if y >= 20480:
            frame = _first_sub_word(frame, 'distance', y, 3968)
            y = u16(y - 3968)
        else:
            frame = _first_add_word(frame, 'distance', y, 3968)
            y = u16(y + 3968)
    return frame, Point(x, y)


# Third deployment offsets and gates share the sole current field cores.
def choose_lateral_formation_point_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, kind: int, family: int, origin = None,
        offset = None, point = None) -> tuple:
    """Second/third wrappers share one accepted-offset and region/RNG core.

    kind1/2 select center regions,5 the west flank,6 the upper center.
    The caller's outer slot is retained; this core owns only its inner BSR.
    """
    if family not in (2, 3):
        raise ValueError('actual lateral wrapper family required')
    frame, origin, offset, point = _first_region_context(memory, frame, origin, offset, point)
    if family == 2:
        continuation = 0x2418C if kind == 1 else 0x2419E if kind == 2 else 0x241B2 if kind == 5 else 0x2427C if kind == 6 else None
    else:
        continuation = 0x24572 if kind == 1 else 0x24584 if kind == 2 else 0x24598 if kind == 5 else 0x245BE if kind == 6 else None
    uint(continuation, 32)
    frame = _first_region_publish(memory, frame)
    entered = _formation_position_enter(frame, continuation)
    frame, result, horizontal, vertical, carry = sample_or_accept_first_formation_region_fields(memory,
        entered, kind, origin, offset, point)
    frame = _formation_position_leave(frame, continuation)
    if carry:
        if kind == 1:
            frame = _first_add_word(frame, 'count', result.x, 3968)
            x = u16(result.x + 3968)
            frame = _first_add_word(frame, 'offset_x', result.y, 5120 if family == 2 else 7168)
            y = u16(result.y + (5120 if family == 2 else 7168))
        elif kind == 2:
            frame = _first_word(frame, 'count', horizontal)
            frame = _first_sub_word(frame, 'count', horizontal, 3968)
            x = u16(horizontal - 3968)
            frame = _first_add_word(frame, 'offset_x', result.y, 5120 if family == 2 else 7168)
            y = u16(result.y + (5120 if family == 2 else 7168))
        elif kind == 5:
            # This wrapper rereads Y, then uses the accepted right edge D4.
            anchor_y = origin.word(offset, 2)
            frame = _first_compare_word(frame, anchor_y, 20480)
            frame = _first_word(frame, 'count', horizontal)
            x = horizontal
            if anchor_y >= 20480:
                frame = _first_word(frame, 'offset_x', vertical)
                if family == 2:
                    frame = _first_sub_word(frame, 'offset_x', vertical, 1024)
                    y = u16(vertical - 1024)
                else:
                    frame = _first_add_word(frame, 'offset_x', vertical, 1024)
                    y = u16(vertical + 1024)
            else:
                if family == 2:
                    frame = _first_add_word(frame, 'offset_x', result.y, 1024)
                    y = u16(result.y + 1024)
                else:
                    frame = _first_sub_word(frame, 'offset_x', result.y, 1024)
                    y = u16(result.y - 1024)
        else:
            shift = 4096 if family == 2 else 2048
            frame = _first_add_word(frame, 'count', result.x, shift)
            x = u16(result.x + shift)
            frame = _first_add_word(frame, 'offset_x', result.y, 3968)
            y = u16(result.y + 3968)
        result, carry = Point(x, y), bool(frame.status & 1)
    return _first_region_publish(memory, frame), result, horizontal, vertical, carry

def choose_third_formation_point_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, kind: int, origin = None,
        offset = None, point = None) -> tuple:
    return choose_lateral_formation_point_fields(memory, frame, kind, 3, origin, offset, point)

def choose_east_center_third_formation_point_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return choose_third_formation_point_fields(memory, frame, 1)

def choose_west_center_third_formation_point_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return choose_third_formation_point_fields(memory, frame, 2)

def choose_west_flank_third_formation_point_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return choose_third_formation_point_fields(memory, frame, 5)

def choose_upper_center_third_formation_point_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple:
    return choose_third_formation_point_fields(memory, frame, 6)

def read_outer_west_staging_anchor_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """confirmed2467E..246C8: one live outer-west anchor, original WORD wrap."""
    frame = _formation_position_frame(memory, frame)
    origin = memory.state.table(0xAE2F6).cursor()
    frame = first_replace(frame, roster=origin)
    scene = memory.battle_scene()
    frame = _first_word(frame, 'target_x', scene)
    offset = u16(scene << 2)
    frame = _first_shift_word(frame, 'target_x', scene, 2)
    frame = _first_compare_word(frame, offset, 92)
    x = origin.word(offset)
    frame = _first_word(frame, 'unit', x)
    if offset == 92:
        frame = _first_sub_word(frame, 'unit', x, 3968)
        x = u16(x - 3968)
        y = origin.word(offset, 2)
        frame = _first_word(frame, 'distance', y)
        frame = _first_sub_word(frame, 'distance', y, 3072)
        y = u16(y - 3072)
    else:
        frame = _first_sub_word(frame, 'unit', x, 3072)
        x = u16(x - 3072)
        y = origin.word(offset, 2)
        frame = _first_word(frame, 'distance', y)
        frame = _first_compare_word(frame, y, 20480)
        if y >= 20480:
            frame = _first_sub_word(frame, 'distance', y, 3968)
            y = u16(y - 3968)
        else:
            frame = _first_add_word(frame, 'distance', y, 3968)
            y = u16(y + 3968)
    return _first_region_publish(memory, frame), Point(x, y)

def test_first_side_relative_total_shortfall_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """confirmed24A14..24A36: conditional primary total and primary limit."""
    frame = _first_frame(memory, frame)
    total = memory.state.read(0xFFFFF69E, 4)
    frame = _first_long(frame, 'target_x', total)
    secondary = memory.state.read(0xFFFFF6A2, 4)
    frame = _first_compare_long(frame, total, secondary)
    selected = False
    if total < secondary:
        limit = memory.state.read(0xFFFFF768, 4)
        frame = _first_compare_long(frame, total, limit)
        selected = total < limit
    return _first_region_carry(memory, frame, selected), selected

def test_second_side_threshold_shortfall_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """confirmed24AB6..24AD0: secondary total below its original live limit."""
    frame = _first_frame(memory, frame)
    total = memory.state.read(0xFFFFF6A2, 4)
    frame = _first_long(frame, 'target_x', total)
    limit = memory.state.read(0xFFFFF76C, 4)
    frame = _first_compare_long(frame, total, limit)
    selected = total < limit
    return _first_region_carry(memory, frame, selected), selected

def test_second_roster_type6_count_below_four_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """confirmed24A36..24A7A: all visited cells type6 until sentinel or four.

    A0 remains the map; A1 advances across the real WORD roster; A2 is live
    positions. One map service and one terrain lookup preserve their exact
    call tokens and internal saved fields. Non-type6/four entries return C0.
    """
    from .business_actions import _battle_action_map_fields, _deployment_terrain_lookup, _deployment_compare_byte
    frame = _first_frame(memory, frame)
    frame = _first_region_publish(memory, frame)
    frame = _first_call(memory, frame, 0x24A3C, _battle_action_map_fields)
    roster = memory.state.table(0xFFFFA5A4).cursor()
    positions = memory.state.table(0xFFFFA150).cursor()
    frame = first_replace(frame, candidates=roster, controller=positions)
    frame = _first_word(frame, 'count', 0)
    count = 0
    while True:
        member = roster.next_word()
        frame = _first_word(frame, 'distance', member)
        if negative_word(member):
            return _first_region_carry(memory, frame, True), True
        offset = u16(member << 2)
        frame = _first_shift_word(frame, 'distance', member, 2)
        x = positions.word(offset)
        frame = _first_word(frame, 'target_y', x)
        y = positions.word(offset, 2)
        frame = _first_word(frame, 'unit', y)
        frame = _first_region_publish(memory, frame)
        frame, category = _deployment_terrain_lookup(memory, frame, x, y, 0x24A5C)
        frame = _deployment_compare_byte(memory, frame, u8(category), 6)
        if u8(category) != 6:
            return _first_region_carry(memory, frame, False), False
        frame = _first_add_word(frame, 'count', count, 1)
        count = u16(count + 1)
        frame = _first_compare_word(frame, count, 4)
        if count >= 4:
            return _first_region_carry(memory, frame, False), False


from .domain import s16

def initialize_second_side_deployment_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """24AF2: assign formation, fill unset positions, then clear the phase WORD."""
    frame = _first_frame(memory, frame)
    frame = _first_call(memory, frame, 0x24AF6, prepare_second_side_formation_assignment_fields)
    frame = _first_call(memory, frame, 0x24AFA, populate_second_side_unset_positions_fields)
    phase = memory.state.table(0xFFFFF6D6)
    phase.word()
    phase.set_word(0, 0)
    return _first_region_publish(memory, _first_memory_word(frame, 0))


def prepare_second_side_formation_assignment_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """24B00: one shared sentinel/count algorithm with the real 24B14 sort slot."""
    frame = _first_frame(memory, frame)
    roster = memory.state.table(0xFFFFA5A4)
    frame, count = read_first_side_assignment_count_fields(memory, frame, roster, 0x24B14)
    frame = _first_call(memory, frame, 0x24B28,
        lambda memory, entered: copy_second_side_position_assignment_fields(memory, entered, count))
    return _first_region_publish(memory, frame)


def copy_second_side_position_assignment_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, count: Word=None) -> FirstDeploymentFrame:
    """24BB4: live force directory and signed WORD offset into the ten-order row."""
    frame = _first_frame(memory, frame)
    if count is None:
        count = low16(frame.unit)
    uint(count, 16)
    force = memory.state.read(0xFFFFF68E, 2)
    frame = _first_word(frame, 'target_x', force)
    frame = _first_shift_word(frame, 'target_x', force, 1)
    directory = memory.state.table(0x24BE4)
    formation = directory.word(u16(force << 1))
    frame = _first_word(frame, 'target_x', formation)
    frame = _first_shift_word(frame, 'target_x', formation, 4)
    intermediate = u16(formation << 4)
    frame = _first_add_word(frame, 'target_x', intermediate, count)
    intermediate = u16(intermediate + count)
    frame = _first_shift_word(frame, 'target_x', intermediate, 5)
    offset = formation_assignment_offset(formation, count)
    frame = first_replace(frame, roster=memory.state.table(0xFFFFAF96).cursor(),
        candidates=memory.state.table(0x24C00).cursor(offset))
    return _first_region_publish(memory, copy_first_side_order_fields(memory, frame))


def populate_second_side_unset_positions_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """25200: reuse the sole roster/order/cell loop after actual choice generation."""
    frame = _first_call(memory, frame, 0x25204, prepare_second_side_battlefield_choices_fields)
    frame = first_replace(frame, roster=memory.state.table(0xFFFFA5A4).cursor(),
        candidates=memory.state.table(0xFFFFAF96).cursor(),
        controller=memory.state.table(0xFFFFD310), scan=memory.state.table(0xFFFFA150).cursor())
    return _first_region_publish(memory, submit_unset_deployment_fields(memory, frame))


def _second_choice_copy_window_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, count_minus_one: Word) -> FirstDeploymentFrame:
    """The one live A0-to-A2 window copy, retaining D0's real DBRA low WORD."""
    frame = _first_frame(memory, frame)
    uint(count_minus_one, 16)
    source = frame.roster
    checked_policy_table(source, memory.state)
    scratch = memory.state.table(0xFFFFD300).cursor()
    frame = first_replace(frame, controller=scratch)
    frame = _first_word(frame, 'target_x', count_minus_one)
    for counter in descending_inclusive(count_minus_one):
        word = source.next_word()
        scratch.append_word(word)
        frame = _first_memory_word(frame, word)
        retained = frame.target_x
        frame = first_replace(frame, target_x=None if retained is None else replace_word(retained, u16(counter - 1)))
    return frame


def _second_choice_clear_scratch_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, zeros: Word) -> FirstDeploymentFrame:
    """Actual postincrement CLR.W cells, including their prior DATA reads."""
    frame = _first_frame(memory, frame)
    uint(zeros, 16)
    scratch = frame.controller
    checked_policy_table(scratch, memory.state)
    if zeros:
        for _ in descending_inclusive(zeros - 1):
            scratch.word()
            scratch.append_word(0)
            frame = _first_memory_word(frame, 0)
    return frame


def _second_choice_publish_window_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, count_minus_one: Word, zeros: Word,
        continuation: Long) -> FirstDeploymentFrame:
    """One copy/pad/shuffle/publish algorithm for the two real window plans."""
    if (count_minus_one, zeros, continuation) not in ((4, 3, 0x25280), (2, 5, 0x252AA)):
        raise ValueError('actual second deployment choice-window plan required')
    frame = _second_choice_copy_window_fields(memory, frame, count_minus_one)
    frame = _second_choice_clear_scratch_fields(memory, frame, zeros)
    frame = _first_call(memory, _first_region_publish(memory, frame), continuation, shuffle_first_side_choice_fields)
    scratch = memory.state.table(0xFFFFD300).cursor()
    frame = first_replace(frame, controller=scratch)
    frame = _first_word(frame, 'target_x', count_minus_one)
    for counter in descending_inclusive(count_minus_one):
        word = scratch.next_word()
        frame.candidates.append_word(word)
        frame = _first_memory_word(frame, word)
        retained = frame.target_x
        frame = first_replace(frame, target_x=None if retained is None else replace_word(retained, u16(counter - 1)))
    return frame


def _second_choice_store_selected_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, index: Word, chosen: Word) -> FirstDeploymentFrame:
    """First three live selected WORDs and the original secondary point directory."""
    frame = _first_frame(memory, frame)
    uint(index, 16)
    uint(chosen, 16)
    if index < 3:
        memory.state.table(0xFFFFF744).set_word(u16(index << 1), chosen)
        frame = _first_memory_word(frame, chosen)
    memory.state.table(0x00FF3EC2).set_word(u16(index << 1), chosen)
    return _first_memory_word(frame, chosen)


def prepare_second_side_battlefield_choices_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """25246: 58-byte scene catalog, two shuffled windows and four distinct picks."""
    frame = _first_frame(memory, frame)
    frame = first_replace(frame, roster=memory.state.table(0xAD870).cursor())
    scene = memory.battle_scene()
    frame = _first_word(frame, 'target_x', scene)
    frame = _first_word(frame, 'target_y', scene)
    offset = scene
    for shift in (1, 1, 2):
        frame = _first_shift_word(frame, 'target_x', offset, shift)
        offset = u16(offset << shift)
        frame = _first_add_word(frame, 'target_x', offset, scene)
        offset = u16(offset + scene)
    frame = _first_shift_word(frame, 'target_x', offset, 1)
    offset = u16(offset << 1)
    frame = first_replace(frame, roster=frame.roster.advance(s16(offset)),
        candidates=memory.state.table(0xFFFFD310).cursor())
    word = frame.roster.next_word()
    frame.candidates.append_word(word)
    frame = _first_memory_word(frame, word)
    frame = _second_choice_publish_window_fields(memory, frame, 4, 3, 0x25280)
    frame = _second_choice_publish_window_fields(memory, frame, 2, 5, 0x252AA)
    selected = memory.state.table(0xFFFFF744)
    for offset in (0, 2, 4):
        selected.word(offset)
        selected.set_word(offset, 0)
        frame = _first_memory_word(frame, 0)
    for index, continuation in ((0, 0x252C8), (1, 0x252D6), (2, 0x252E4), (3, 0x252F2)):
        frame = _first_call(memory, _first_region_publish(memory, frame), continuation,
            choose_unused_second_side_point_fields)
        # The callee's real RNG fully establishes D0 before MOVE.W; no guessed
        # upper WORD is introduced to obtain this actually observed choice.
        frame = _second_choice_store_selected_fields(memory, frame, index, low16(frame.target_x))
    return _first_region_publish(memory, frame)


def choose_unused_second_side_point_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """25338: five copied choices, real shuffle, then three lazy live rejections."""
    frame = _second_choice_copy_window_fields(memory, frame, 4)
    frame = _second_choice_clear_scratch_fields(memory, frame, 3)
    frame = _first_call(memory, _first_region_publish(memory, frame), 0x2534E,
        shuffle_first_side_choice_fields)
    scratch = memory.state.table(0xFFFFD300).cursor()
    frame = first_replace(frame, controller=scratch)
    while True:
        candidate = scratch.next_word()
        frame = _first_word(frame, 'target_x', candidate)
        selected = memory.state.read(0xFFFFF744, 2)
        frame = _first_compare_word(frame, candidate, selected)
        if candidate == selected:
            continue
        selected = memory.state.read(0xFFFFF746, 2)
        frame = _first_compare_word(frame, candidate, selected)
        if candidate == selected:
            continue
        selected = memory.state.read(0xFFFFF748, 2)
        frame = _first_compare_word(frame, candidate, selected)
        if candidate == selected:
            continue
        frame.candidates.append_word(candidate)
        return _first_region_publish(memory, _first_memory_word(frame, candidate))
