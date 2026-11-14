"""Deployment lists, terrain selection and battle-action requirements.

These are gameplay decisions and live state transitions, not damage resolution.
Original fixed-width arithmetic and anomalous choices stay explicit. Resource
data is supplied by named readonly views; no ROM or file is opened here.
"""
from .domain import (GameState, Table, Word, Long, CarryOutcome, checked_state,
                     uint, u16, u32, s16, low8, low16, high16,
                     replace_byte, replace_word, negative_byte, negative_word,
                     divu_retained)
from .contexts_actions import (AnchorContext, OccupiedCellsContext,
    EmptySlotContext, EmptySlotResult, DeploymentCellContext,
    DeploymentEdgeContext, PromotionContext, RatingContext, RatingSelection,
    SelectionContext, ScoredSelection, CandidateBudgetContext,
    TerrainActorContext, ActionTerrainPolicy, ActionCandidate, ActionRandomDraw, checked_context)
from .business_geometry import (weighted_training_factor,
    load_battlefield_map_context, read_battlefield_terrain_type, read_battlefield_terrain_type_fields)

from .contexts_policy_memory import BattlePolicyMemory, DeploymentAnchorFields, checked_policy_table
from .contexts_deployment_fields import (DeploymentOccupiedFields, DeploymentSlotFields,
    checked_deployment_cursor, changed_deployment_return)
from .contexts_first_deployment import (FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace)
from .contexts_deployment_terrain import (DeploymentProbeFields, DeploymentEdgeFields)


from .business_geometry import _contact_status, _contact_retained_word, load_battlefield_map_fields, weighted_training_factor_fields


from .business_formation import first_deployment_random_fields


from .business_formation import (
    first_deployment_random_fields, _first_word, _first_byte, _first_long,
    _first_shift_word, _first_right_word, _first_add_word, _first_memory_word,
)

def read_city_deployment_anchor(state: GameState, retained: AnchorContext) -> tuple[Long, Long]:
    """Legacy x/y projection; the old API did not observe incoming D2."""
    state = checked_state(state)
    retained = checked_context(retained, AnchorContext)
    fields = read_city_deployment_anchor_fields(BattlePolicyMemory(state), retained, None)
    return fields.x, fields.y


def read_city_deployment_anchor_fields(memory: BattlePolicyMemory, retained: AnchorContext, retained_index: Long | None) -> DeploymentAnchorFields:
    """25C02's one live city/variant/cell algorithm, including retained words."""
    if type(memory) is not BattlePolicyMemory:
        raise ValueError('typed live deployment-anchor memory required')
    retained = checked_context(retained, AnchorContext)
    if retained_index is not None:
        uint(retained_index, 32)
    city = memory.battle_scene()
    formation = memory.scene_variants.byte(city)
    city_offset = u16(city << 5)
    variant_offset = u16(formation << 1)
    wide_offset = city_offset + variant_offset
    offset = u16(wide_offset)
    index = None if retained_index is None else replace_word(retained_index, offset)
    cells = memory.deployment_cells
    x_byte = cells.byte(offset)
    x = replace_word(retained.x, x_byte)
    y_byte = cells.byte(offset, 1)
    y = replace_word(retained.y, y_byte)
    return DeploymentAnchorFields(x, y, index, cells, y_byte == 0, y_byte & 128 != 0, wide_offset > 65535)


def read_city_second_deployment_anchor(state: GameState, retained: AnchorContext) -> tuple[Long, Long]:
    """Legacy x/y projection of the single 25F0A field algorithm."""
    state = checked_state(state)
    retained = checked_context(retained, AnchorContext)
    fields = read_city_second_deployment_anchor_fields(BattlePolicyMemory(state), retained, None)
    return fields.x, fields.y


def select_lowest_nonzero_rating(state: GameState, retained: RatingContext) -> RatingSelection:
    state = checked_state(state)
    retained = checked_context(retained, RatingContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        target_x=retained.rating, target_y=retained.selected)
    frame = select_lowest_nonzero_rating_fields(BattlePolicyMemory(state), frame)
    return RatingSelection(frame.target_x, frame.target_y)


def select_lowest_filtered_rating(state: GameState, retained: RatingContext) -> RatingSelection:
    """Legacy D0/D1 projection of the single live 26638 scanner."""
    state = checked_state(state)
    retained = checked_context(retained, RatingContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        target_x=retained.rating, target_y=retained.selected)
    frame = select_lowest_filtered_rating_fields(BattlePolicyMemory(state), frame)
    return RatingSelection(frame.target_x, frame.target_y)


def read_selected_action_attributes(state: GameState) -> Word:
    """Legacy amount projection; unobserved high D2 stays unobserved."""
    state = checked_state(state)
    frame, attributes = read_selected_action_attribute_fields(
        BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return attributes


def attribute_action_requirement(sample: Word, attributes: Word, base: Word) -> Long:
    uint(sample, 16)
    uint(attributes, 16)
    uint(base, 16)
    frame = _action_random_factor_fields(FirstDeploymentFrame.unobserved(),
        ActionRandomDraw(sample, sample), base, 5, 'unit')
    return _action_attribute_product_fields(frame, attributes).target_x


def read_selected_action_troops(state: GameState) -> Long:
    state = checked_state(state)
    return state.officer_troops.long(u16(state.selected_officer() << 2))


def read_candidate_action_troops(state: GameState, candidate: CandidateBudgetContext) -> Long:
    state = checked_state(state)
    candidate = checked_context(candidate, CandidateBudgetContext)
    return state.officer_troops.long(u16(low16(candidate.selected) << 2))


def troop_action_requirement(sample: Word, strength: Long, multiplier: Word, base: Word) -> Long:
    uint(sample, 16)
    uint(strength, 32)
    uint(multiplier, 16)
    uint(base, 16)
    if multiplier in (10, 11):
        frame = _action_random_factor_fields(FirstDeploymentFrame.unobserved(),
            ActionRandomDraw(sample, sample), base, multiplier)
        return low16(divu_retained(strength, low16(frame.target_x)))
    # Historical generic policies outside this original closed family remain.
    divisor = u16(high16(u32(sample * multiplier)) + base)
    return low16(divu_retained(strength, divisor))


def state_mixed_action_requirement(draw: ActionRandomDraw, strength: Long, base: Word) -> Long:
    """Historical LONG projection of the one state-mixed budget arithmetic."""
    return state_mixed_action_requirement_fields(FirstDeploymentFrame.unobserved(), draw, strength, base).unit


def commit_action_requirement(state: GameState, requirement: Long) -> Long:
    state = checked_state(state)
    uint(requirement, 32)
    state.set_action_amount(requirement)
    return requirement


def compute_selected_attribute_budget(state: GameState) -> Long:
    state = checked_state(state)
    return compute_selected_attribute_budget_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved(), 8).target_x


def compute_selected_attribute_budget_second_side(state: GameState) -> Long:
    """Legacy result projection of the same before-RNG attribute transaction."""
    state = checked_state(state)
    frame = compute_selected_attribute_budget_second_side_fields(
        BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return frame.target_x


def compute_selected_troop_budget_base20(state: GameState) -> Long:
    state = checked_state(state)
    return compute_selected_troop_budget_base20_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved(), 20).target_y


def compute_selected_troop_budget_base30(state: GameState) -> Long:
    state = checked_state(state)
    return compute_selected_troop_budget_base30_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved(), 30).target_y


def compute_then_reload_previous_selected_budget(state: GameState) -> Long:
    state = checked_state(state)
    return compute_then_reload_previous_selected_budget_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved(), 20).target_y


def compute_selected_type2_budget_base30(state: GameState) -> Long:
    state = checked_state(state)
    return compute_selected_type2_budget_base30_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved(), 30).target_y


def compute_type6_budget_from_random_state(state: GameState, candidate: CandidateBudgetContext) -> Long:
    """Legacy amount projection of the one selected type6 budget entry."""
    state = checked_state(state)
    candidate = checked_context(candidate, CandidateBudgetContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(), offset_x=candidate.selected)
    return compute_type6_budget_from_random_state_fields(BattlePolicyMemory(state), frame).unit


def compute_candidate_budget_base20(state: GameState, candidate: CandidateBudgetContext) -> Long:
    """Historical amount projection of the sole base20 candidate budget."""
    state = checked_state(state)
    candidate = checked_context(candidate, CandidateBudgetContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(), offset_x=candidate.selected)
    return compute_candidate_budget_base20_fields(BattlePolicyMemory(state), frame).unit


def compute_candidate_budget_base30(state: GameState, candidate: CandidateBudgetContext) -> Long:
    """Historical amount projection of the sole base30 candidate budget."""
    state = checked_state(state)
    candidate = checked_context(candidate, CandidateBudgetContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(), offset_x=candidate.selected)
    return compute_candidate_budget_base30_fields(BattlePolicyMemory(state), frame).unit


def compute_type1_candidate_budget_base20(state: GameState, candidate: CandidateBudgetContext) -> Long:
    """Legacy amount projection of the real 26A78 budget entry."""
    state = checked_state(state)
    candidate = checked_context(candidate, CandidateBudgetContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(), offset_x=candidate.selected)
    frame = compute_type1_candidate_budget_base20_fields(BattlePolicyMemory(state), frame)
    return frame.unit


def compute_type2_candidate_budget_base30(state: GameState, candidate: CandidateBudgetContext) -> Long:
    """Legacy amount projection of the actual 26BC6 budget entry."""
    state = checked_state(state)
    candidate = checked_context(candidate, CandidateBudgetContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(), offset_x=candidate.selected)
    frame = compute_type2_candidate_budget_base30_fields(BattlePolicyMemory(state), frame)
    return frame.unit


def append_roster_occupied_cells(state: GameState, cells: OccupiedCellsContext) -> None:
    """Legacy unobserved-carrier projection; use the same live list core."""
    state = checked_state(state)
    cells = checked_context(cells, OccupiedCellsContext, state)
    append_roster_occupied_cell_fields(BattlePolicyMemory(state), DeploymentOccupiedFields(
        None, None, cells.destination, cells.source, cells.positions, None, None))
    return None


def build_deployment_occupied_cells(state: GameState) -> None:
    """Legacy no-carrier/no-stack projection, not a complete caller claim."""
    state = checked_state(state)
    build_deployment_occupied_cell_fields(BattlePolicyMemory(state), None, None, None, None)
    return None


def find_next_empty_position_slot(state: GameState, slots: EmptySlotContext) -> EmptySlotResult:
    """The historical WORD/carry API projects the same full field scanner."""
    state = checked_state(state)
    slots = checked_context(slots, EmptySlotContext, state)
    fields = find_next_empty_position_slot_fields(BattlePolicyMemory(state),
        slots.source, slots.positions, None, None)
    return EmptySlotResult(fields.offset, slots.source, state.carry_result(1 if fields.carry else 0))


def try_place_deployment_cell(state: GameState, cell: DeploymentCellContext) -> CarryOutcome:
    state = checked_state(state)
    cell = checked_context(cell, DeploymentCellContext, state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=cell.map,
        candidates=cell.positions, status=state.sr & 31)
    fields = try_place_deployment_cell_fields(BattlePolicyMemory(state), frame,
        cell.x, cell.y, cell.offset).validate(state)
    return state.carry_result(1 if fields.placed else 0)


def scan_deployment_first_edge(state: GameState, edge: DeploymentEdgeContext) -> EmptySlotResult:
    state = checked_state(state)
    edge = checked_context(edge, DeploymentEdgeContext, state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=edge.map,
        candidates=edge.positions, scan=edge.source, status=state.sr & 31)
    fields = scan_deployment_first_edge_fields(BattlePolicyMemory(state), frame,
        edge.center_x, edge.center_y, edge.radius, edge.offset).validate(state)
    return EmptySlotResult(fields.offset, fields.source, state.carry_result(1 if fields.found else 0))


def scan_deployment_second_edge(state: GameState, edge: DeploymentEdgeContext) -> EmptySlotResult:
    state = checked_state(state)
    edge = checked_context(edge, DeploymentEdgeContext, state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=edge.map,
        candidates=edge.positions, scan=edge.source, status=state.sr & 31)
    fields = scan_deployment_second_edge_fields(BattlePolicyMemory(state), frame,
        edge.center_x, edge.center_y, edge.radius, edge.offset).validate(state)
    return EmptySlotResult(fields.offset, fields.source, state.carry_result(1 if fields.found else 0))


def promote_first_roster_deployment_candidate(state: GameState, retained: PromotionContext) -> None:
    state = checked_state(state)
    retained = checked_context(retained, PromotionContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        count=retained.formation_carrier, status=state.sr & 31)
    promote_first_roster_deployment_candidate_fields(BattlePolicyMemory(state), frame)
    return None


def promote_second_roster_deployment_candidate(state: GameState) -> None:
    state = checked_state(state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), status=state.sr & 31)
    promote_second_roster_deployment_candidate_fields(BattlePolicyMemory(state), frame)
    return None


def test_actor_types_0_4_8(state: GameState, actor: TerrainActorContext) -> CarryOutcome:
    state = checked_state(state)
    actor = checked_context(actor, TerrainActorContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        choice=actor.actor, target_x=actor.terrain_carrier)
    frame = test_actor_types_0_4_8_fields(BattlePolicyMemory(state), frame)
    return state.carry_result(int(bool(frame.status & 1)))


def test_actor_map_relative_types(state: GameState, actor: TerrainActorContext) -> CarryOutcome:
    """Legacy carry projection; preserve the original map-relative coordinate alias."""
    state = checked_state(state)
    actor = checked_context(actor, TerrainActorContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        choice=actor.actor, target_x=actor.terrain_carrier)
    frame = test_actor_map_relative_types_fields(BattlePolicyMemory(state), frame)
    return state.carry_result(1 if frame.status & 1 else 0)


def build_non_type6_candidates(state: GameState, retained: SelectionContext) -> Table:
    """The old map-only API projects the unique 26692 filter transaction."""
    state = checked_state(state)
    retained = checked_context(retained, SelectionContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        target_x=retained.terrain_carrier, target_y=retained.selected)
    frame = build_non_type6_candidates_fields(BattlePolicyMemory(state), frame)
    return state.checked_table(frame.roster)


def action_terrain_is_eligible(terrain: Long, policy: ActionTerrainPolicy) -> bool:
    uint(terrain, 32)
    if type(policy) is not ActionTerrainPolicy:
        raise ValueError('typed action terrain policy required')
    return low8(terrain) in policy.kinds


def is_better_action_score(score: Long, strongest: Long) -> bool:
    """Strictly greater wins; the first tied candidate stays selected."""
    uint(score, 32)
    uint(strongest, 32)
    return score > strongest


def observe_action_candidate(state: GameState, map_context: Table, member: Word, retained_terrain: Long) -> ActionCandidate:
    state = checked_state(state)
    map_context = state.checked_table(map_context)
    uint(member, 16)
    uint(retained_terrain, 32)
    member = u16(member & 255)
    offset = u16(member << 2)
    x = state.battle_positions.word(offset) >> 7
    y = state.battle_positions.word(offset, 2) >> 7
    terrain = read_battlefield_terrain_type(state, map_context, x, y, retained_terrain)
    return ActionCandidate(member, offset, terrain)


def read_action_candidate_score(state: GameState, candidate: ActionCandidate) -> Long:
    state = checked_state(state)
    candidate = checked_context(candidate, ActionCandidate)
    training = low16(weighted_training_factor(state, candidate.member))
    return u32(training * state.officer_troops.word(candidate.offset, 2))


def select_action_candidate_by_terrain(state: GameState, retained: SelectionContext, map_context: Table, policy: ActionTerrainPolicy) -> ScoredSelection:
    """Legacy score/map projection of the one shared live ranking loop."""
    state = checked_state(state)
    retained = checked_context(retained, SelectionContext)
    map_context = state.checked_table(map_context)
    frame = first_replace(FirstDeploymentFrame.unobserved(), target_x=retained.terrain_carrier,
        offset_x=retained.selected, roster=map_context.cursor())
    returned = select_action_candidate_by_terrain_fields(BattlePolicyMemory(state), frame, policy)
    return ScoredSelection(returned.distance, returned.offset_x, returned.roster)


def select_strongest_open_terrain_candidate(state: GameState, retained: SelectionContext) -> ScoredSelection:
    state = checked_state(state)
    retained = checked_context(retained, SelectionContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        target_x=retained.terrain_carrier, offset_x=retained.selected)
    frame = select_strongest_open_terrain_candidate_fields(BattlePolicyMemory(state), frame)
    return ScoredSelection(frame.distance, frame.offset_x, frame.roster)


def select_strongest_type1_candidate(state: GameState, retained: SelectionContext) -> ScoredSelection:
    state = checked_state(state)
    retained = checked_context(retained, SelectionContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        target_x=retained.terrain_carrier, offset_x=retained.selected)
    frame = select_strongest_type1_candidate_fields(BattlePolicyMemory(state), frame)
    return ScoredSelection(frame.distance, frame.offset_x, frame.roster)


def select_strongest_type2_candidate(state: GameState, retained: SelectionContext) -> ScoredSelection:
    state = checked_state(state)
    retained = checked_context(retained, SelectionContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        target_x=retained.terrain_carrier, offset_x=retained.selected)
    frame = select_strongest_type2_candidate_fields(BattlePolicyMemory(state), frame)
    return ScoredSelection(frame.distance, frame.offset_x, frame.roster)


def select_strongest_type6_candidate(state: GameState, retained: SelectionContext) -> ScoredSelection:
    """Historical type6 result projection of its sole complete field entry."""
    state = checked_state(state)
    retained = checked_context(retained, SelectionContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(), target_x=retained.terrain_carrier,
        offset_x=retained.selected)
    returned = select_strongest_type6_candidate_fields(BattlePolicyMemory(state), frame)
    return ScoredSelection(returned.distance, returned.offset_x, returned.roster)


def select_strongest_open_terrain_candidate_second_side(state: GameState, retained: SelectionContext) -> ScoredSelection:
    """Legacy score/map projection of the sole second-side open policy."""
    state = checked_state(state)
    retained = checked_context(retained, SelectionContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(), target_x=retained.terrain_carrier,
        offset_x=retained.selected)
    returned = select_strongest_open_terrain_candidate_second_side_fields(BattlePolicyMemory(state), frame)
    return ScoredSelection(returned.distance, returned.offset_x, returned.roster)


def select_strongest_type1_candidate_second_side(state: GameState, retained: SelectionContext) -> ScoredSelection:
    """Legacy selection projection of the one 26A20 actual-field entry."""
    state = checked_state(state)
    retained = checked_context(retained, SelectionContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        offset_x=retained.selected, target_x=retained.terrain_carrier)
    frame = select_strongest_type1_candidate_second_side_fields(BattlePolicyMemory(state), frame)
    return ScoredSelection(frame.distance, frame.offset_x, state.checked_table(frame.roster))


def select_strongest_type2_candidate_with_map_context(state: GameState, retained: SelectionContext, map_context: Table) -> ScoredSelection:
    """Legacy observed map/selection projection; no second map load occurs."""
    state = checked_state(state)
    retained = checked_context(retained, SelectionContext)
    map_context = state.checked_table(map_context)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=map_context.cursor(),
        offset_x=retained.selected, target_x=retained.terrain_carrier)
    frame = select_strongest_type2_candidate_with_map_context_fields(BattlePolicyMemory(state), frame)
    return ScoredSelection(frame.distance, frame.offset_x, state.checked_table(frame.roster))


def read_city_second_deployment_anchor_fields(memory: BattlePolicyMemory, retained: AnchorContext, retained_index: Long | None) -> DeploymentAnchorFields:
    """25F0A, distinct from the first-side variant table at ABDA8."""
    if type(memory) is not BattlePolicyMemory:
        raise ValueError('typed live second-anchor memory required')
    retained = checked_context(retained, AnchorContext)
    if retained_index is not None:
        uint(retained_index, 32)
    offset = u16(memory.battle_scene() << 2)
    index = None if retained_index is None else replace_word(retained_index, offset)
    cells = memory.state.table(0xAE2F6)
    original_x = cells.word(offset)
    x = replace_word(retained.x, (original_x >> 3) >> 7)
    original_y = cells.word(offset, 2)
    y = replace_word(retained.y, (original_y >> 3) >> 7)
    return DeploymentAnchorFields(x, y, index, cells, low16(y) == 0, False, original_y & 512 != 0)


def append_roster_occupied_cell_fields(memory: BattlePolicyMemory, fields: DeploymentOccupiedFields) -> DeploymentOccupiedFields:
    """25C48 preserves D2/D3 high words and ordered live BYTE-pair writes."""
    if type(memory) is not BattlePolicyMemory or type(fields) is not DeploymentOccupiedFields:
        raise ValueError('typed same-state occupied fields required')
    fields.validate(memory.state)
    member_carrier = fields.member
    coordinate_carrier = fields.coordinate
    extend = fields.extend
    while True:
        member = fields.source.next_word()
        member_carrier = None if member_carrier is None else replace_word(member_carrier, member)
        if negative_word(member):
            break
        offset = u16(member << 2)
        member_carrier = None if member_carrier is None else replace_word(member_carrier, offset)
        extend = member & 16384 != 0
        x = fields.positions.word(offset)
        coordinate_carrier = None if coordinate_carrier is None else replace_word(coordinate_carrier, x)
        if x == 0:
            continue
        original_x = x
        x = (x >> 7) >> 3
        coordinate_carrier = None if coordinate_carrier is None else replace_word(coordinate_carrier, x)
        extend = original_x & 512 != 0
        fields.destination.append_byte(x)
        y = fields.positions.word(offset, 2)
        coordinate_carrier = None if coordinate_carrier is None else replace_word(coordinate_carrier, y)
        original_y = y
        y = (y >> 7) >> 3
        coordinate_carrier = None if coordinate_carrier is None else replace_word(coordinate_carrier, y)
        extend = original_y & 512 != 0
        fields.destination.append_byte(y)
    return DeploymentOccupiedFields(member_carrier, coordinate_carrier, fields.destination,
        fields.source, fields.positions, extend, fields.stack_cursor).validate(memory.state)


def _append_occupied_deployment_call(memory: BattlePolicyMemory, fields: DeploymentOccupiedFields, continuation: Long) -> DeploymentOccupiedFields:
    """A complete 25C2A BSR writes and reads its actual known return slot."""
    uint(continuation, 32)
    if fields.stack_cursor is None:
        return append_roster_occupied_cell_fields(memory, fields)
    stack = fields.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = DeploymentOccupiedFields(fields.member, fields.coordinate, fields.destination,
        fields.source, fields.positions, fields.extend, stack)
    result = append_roster_occupied_cell_fields(memory, entered)
    actual = result.stack_cursor.long()
    if actual != continuation:
        changed_deployment_return(memory, actual)
    return DeploymentOccupiedFields(result.member, result.coordinate, result.destination,
        result.source, result.positions, result.extend, result.stack_cursor.advance(4))


def build_deployment_occupied_cell_fields(memory: BattlePolicyMemory, retained_member: Long | None, retained_coordinate: Long | None, retained_extend: bool | None, stack_cursor) -> DeploymentOccupiedFields:
    """25C2A uses both live rosters; the final sentinel is not postincremented."""
    if type(memory) is not BattlePolicyMemory:
        raise ValueError('typed same-state occupied memory required')
    positions = memory.state.table(0xFFFFA150)
    destination = memory.state.table(0xFFFFD300).cursor()
    source = memory.state.table(0xFFFFA550).cursor()
    fields = DeploymentOccupiedFields(retained_member, retained_coordinate,
        destination, source, positions, retained_extend, stack_cursor).validate(memory.state)
    fields = _append_occupied_deployment_call(memory, fields, 0x25C3A)
    source = memory.state.table(0xFFFFA5A4).cursor()
    fields = DeploymentOccupiedFields(fields.member, fields.coordinate, fields.destination,
        source, fields.positions, fields.extend, fields.stack_cursor)
    fields = _append_occupied_deployment_call(memory, fields, 0x25C42)
    fields.destination.put_word(65535)
    return fields


def find_next_empty_position_slot_fields(memory: BattlePolicyMemory, source, positions, retained_index: Long | None, retained_extend: bool | None) -> DeploymentSlotFields:
    """25C9C: signed WORD sentinel, signed WORD indexed EA and live TST.L."""
    if type(memory) is not BattlePolicyMemory:
        raise ValueError('typed same-state slot memory required')
    checked_deployment_cursor(source, memory.state)
    checked_policy_table(positions, memory.state)
    if retained_index is not None:
        uint(retained_index, 32)
    if retained_extend is not None and type(retained_extend) is not bool:
        raise ValueError('actual incoming X required when observed')
    index = retained_index
    extend = retained_extend
    while True:
        member = source.next_word()
        index = None if index is None else replace_word(index, member)
        if negative_word(member):
            return DeploymentSlotFields(index, member, source, positions, True, False, True, extend)
        offset = u16(member << 2)
        index = None if index is None else replace_word(index, offset)
        extend = member & 16384 != 0
        value = positions.long(offset)
        if value == 0:
            return DeploymentSlotFields(index, offset, source, positions, False, True, False, extend)


def deployment_edge_coordinate_allowed(coordinate: Word, maximum: Word) -> bool:
    """The two original unsigned edge bounds share only this predicate."""
    uint(coordinate, 16)
    uint(maximum, 16)
    return 3 <= coordinate <= maximum


def _deployment_word(carrier: Long | None, word: Word) -> Long | None:
    uint(word, 16)
    if carrier is None:
        return None
    return replace_word(carrier, word)


def _deployment_byte(carrier: Long | None, value: Word) -> Long | None:
    uint(value, 8)
    if carrier is None:
        return None
    return replace_byte(carrier, value)


def _deployment_flags(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, status: Word) -> FirstDeploymentFrame:
    uint(status, 8)
    if status > 31:
        raise ValueError('actual CCR must be in the low five bits')
    memory.state.sr = (memory.state.sr & 65504) | status
    return first_replace(frame, status=status)


def _deployment_move_word(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, word: Word) -> FirstDeploymentFrame:
    uint(word, 16)
    if frame.status is None:
        raise ValueError('current CCR observation required')
    return _deployment_flags(memory, frame, (frame.status & 16) |
        (8 if word & 32768 else 0) | (4 if word == 0 else 0))


def _deployment_move_byte(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, value: Word) -> FirstDeploymentFrame:
    uint(value, 8)
    if frame.status is None:
        raise ValueError('current CCR observation required')
    return _deployment_flags(memory, frame, (frame.status & 16) |
        (8 if value & 128 else 0) | (4 if value == 0 else 0))


def _deployment_sum(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, left: Word, right: Word) -> tuple[Word, FirstDeploymentFrame]:
    uint(left, 16)
    uint(right, 16)
    wide = left + right
    value = u16(wide)
    overflow = ((~(left ^ right)) & (left ^ value) & 32768) != 0
    frame = _deployment_flags(memory, frame, (17 if wide > 65535 else 0) |
        (8 if value & 32768 else 0) | (4 if value == 0 else 0) |
        (2 if overflow else 0))
    return value, frame


def _deployment_difference(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, left: Word, right: Word) -> tuple[Word, FirstDeploymentFrame]:
    uint(left, 16)
    uint(right, 16)
    value = u16(left - right)
    overflow = ((left ^ right) & (left ^ value) & 32768) != 0
    frame = _deployment_flags(memory, frame, (17 if left < right else 0) |
        (8 if value & 32768 else 0) | (4 if value == 0 else 0) |
        (2 if overflow else 0))
    return value, frame


def _deployment_compare(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, left: Word, right: Word) -> FirstDeploymentFrame:
    uint(left, 16)
    uint(right, 16)
    if frame.status is None:
        raise ValueError('current compare X observation required')
    value = u16(left - right)
    overflow = ((left ^ right) & (left ^ value) & 32768) != 0
    return _deployment_flags(memory, frame, (frame.status & 16) |
        (1 if left < right else 0) | (8 if value & 32768 else 0) |
        (4 if value == 0 else 0) | (2 if overflow else 0))


def _deployment_compare_byte(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, left: Word, right: Word) -> FirstDeploymentFrame:
    uint(left, 8)
    uint(right, 8)
    if frame.status is None:
        raise ValueError('current compare X observation required')
    value = (left - right) & 255
    overflow = ((left ^ right) & (left ^ value) & 128) != 0
    return _deployment_flags(memory, frame, (frame.status & 16) |
        (1 if left < right else 0) | (8 if value & 128 else 0) |
        (4 if value == 0 else 0) | (2 if overflow else 0))


def _deployment_left_shift(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, word: Word, count: Word) -> tuple[Word, FirstDeploymentFrame]:
    uint(word, 16)
    uint(count, 16)
    if count < 1 or count > 15:
        raise ValueError('known WORD logical shift count required')
    value = u16(word << count)
    shifted = (word >> (16 - count)) & 1
    frame = _deployment_flags(memory, frame, (17 if shifted else 0) |
        (8 if value & 32768 else 0) | (4 if value == 0 else 0))
    return value, frame


def _deployment_right_shift(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, word: Word, count: Word) -> tuple[Word, FirstDeploymentFrame]:
    uint(word, 16)
    uint(count, 16)
    if count < 1 or count > 15:
        raise ValueError('known WORD logical shift count required')
    value = word >> count
    shifted = (word >> (count - 1)) & 1
    frame = _deployment_flags(memory, frame, (17 if shifted else 0) |
        (4 if value == 0 else 0))
    return value, frame


def _deployment_carry(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, value: bool) -> FirstDeploymentFrame:
    if type(value) is not bool:
        raise ValueError('real carry decision required')
    if type(memory.state) is GameState:
        memory.state.carry_result(1 if value else 0)
    else:
        memory.state.set_status_word((memory.state.sr & 65534) | (1 if value else 0))
    return first_replace(frame, status=memory.state.sr & 31)


def _deployment_push(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, value: Long) -> FirstDeploymentFrame:
    uint(value, 32)
    frame.validate(memory.state, complete=True)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, value)
    return first_replace(frame, stack_cursor=stack)


def _deployment_pop(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, Long]:
    frame.validate(memory.state, complete=True)
    value = frame.stack_cursor.long()
    return first_replace(frame, stack_cursor=frame.stack_cursor.advance(4)), value


def _deployment_enter(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, continuation: Long) -> FirstDeploymentFrame:
    """Only an actual complete call writes its original known return LONG."""
    uint(continuation, 32)
    if frame.stack_cursor is None:
        return frame
    return _deployment_push(memory, frame, continuation)


def _deployment_leave(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, continuation: Long) -> FirstDeploymentFrame:
    uint(continuation, 32)
    if frame.stack_cursor is None:
        return frame
    current, target = _deployment_pop(memory, frame)
    if target != continuation:
        raise FirstDeploymentReturnBoundary(target, current, continuation)
    return current


def _deployment_save_probe(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    if frame.stack_cursor is None:
        return frame
    frame = _deployment_push(memory, frame, frame.distance)
    frame = _deployment_push(memory, frame, frame.count)
    frame = _deployment_push(memory, frame, frame.unit)
    frame = _deployment_push(memory, frame, frame.target_y)
    return _deployment_push(memory, frame, frame.target_x)


def _deployment_restore_probe(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, observed: FirstDeploymentFrame) -> FirstDeploymentFrame:
    if frame.stack_cursor is None:
        return first_replace(frame, target_x=observed.target_x, target_y=observed.target_y,
            unit=observed.unit, count=observed.count, distance=observed.distance)
    frame, target_x = _deployment_pop(memory, frame)
    frame, target_y = _deployment_pop(memory, frame)
    frame, unit = _deployment_pop(memory, frame)
    frame, count = _deployment_pop(memory, frame)
    frame, distance = _deployment_pop(memory, frame)
    return first_replace(frame, target_x=target_x, target_y=target_y, unit=unit,
        count=count, distance=distance)


def _deployment_terrain_lookup(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, x: Word, y: Word, continuation: Long=154990) -> tuple[FirstDeploymentFrame, Word]:
    """Known 1A44E unique lookup, including real inner MOVEM A0/D3/D2/D1."""
    if frame.roster is None:
        raise ValueError('actual current A0 map required')
    map_context = frame.roster
    observed = frame
    frame = _deployment_enter(memory, frame, continuation)
    if frame.stack_cursor is not None:
        frame = _deployment_push(memory, frame, frame.roster.base)
        frame = _deployment_push(memory, frame, frame.count)
        frame = _deployment_push(memory, frame, frame.unit)
        frame = _deployment_push(memory, frame, frame.target_y)
    sample = read_battlefield_terrain_type_fields(memory, map_context, x, y, frame.target_x).validate(memory.state)
    frame = first_replace(frame, target_x=sample.carrier, roster=sample.lookup.cursor())
    frame = _deployment_flags(memory, frame, (16 if sample.extend else 0) | (8 if sample.category & 128 else 0) | (4 if sample.category == 0 else 0))
    if frame.stack_cursor is None:
        frame = first_replace(frame, target_y=observed.target_y, unit=observed.unit, count=observed.count, roster=observed.roster)
    else:
        frame, target_y = _deployment_pop(memory, frame)
        frame, unit = _deployment_pop(memory, frame)
        frame, count = _deployment_pop(memory, frame)
        frame, roster = _deployment_pop(memory, frame)
        frame = first_replace(frame, target_y=target_y, unit=unit, count=count, roster=memory.state.table(roster).cursor())
    return (_deployment_leave(memory, frame, continuation), sample.category)


def try_place_deployment_cell_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, x: Word, y: Word, offset: Word) -> DeploymentProbeFields:
    """25D08: one occupied-neighborhood/terrain/placement algorithm.

    Legacy WORD callers supply explicit coordinates but leave absent LONGs/SP
    unobserved. Complete callers preserve both actual MOVEM frames and aliases.
    """
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('sealed memory and retained deployment frame required')
    frame.validate(memory.state)
    uint(x, 16)
    uint(y, 16)
    uint(offset, 16)
    if frame.roster is None or frame.candidates is None:
        raise ValueError('actual A0 terrain and A1 position views required')
    observed = frame
    frame = _deployment_save_probe(memory, frame)
    occupied = memory.state.table(0xFFFFD300).cursor()
    frame = first_replace(frame, controller=occupied)
    frame = _deployment_move_word(memory, frame, x)
    left, frame = _deployment_difference(memory, frame, x, 3)
    frame = first_replace(frame, target_x=_deployment_word(frame.target_x, left))
    right, frame = _deployment_sum(memory, frame, x, 3)
    frame = first_replace(frame, unit=_deployment_word(frame.unit, right))
    frame = _deployment_move_word(memory, frame, y)
    bottom, frame = _deployment_difference(memory, frame, y, 3)
    frame = first_replace(frame, target_y=_deployment_word(frame.target_y, bottom))
    top, frame = _deployment_sum(memory, frame, y, 3)
    frame = first_replace(frame, count=_deployment_word(frame.count, top))
    while True:
        frame = first_replace(frame, distance=_deployment_word(frame.distance, 0))
        frame = _deployment_move_word(memory, frame, 0)
        near_x = occupied.byte()
        frame = first_replace(frame, distance=_deployment_byte(frame.distance, near_x))
        frame = _deployment_move_byte(memory, frame, near_x)
        if negative_byte(near_x):
            break
        frame = _deployment_compare(memory, frame, near_x, left)
        if s16(near_x) >= s16(left):
            frame = _deployment_compare(memory, frame, near_x, right)
            if s16(near_x) <= s16(right):
                near_y = occupied.byte(0, 1)
                frame = first_replace(frame, distance=_deployment_byte(frame.distance, near_y))
                frame = _deployment_move_byte(memory, frame, near_y)
                frame = _deployment_compare(memory, frame, near_y, bottom)
                if s16(near_y) >= s16(bottom):
                    frame = _deployment_compare(memory, frame, near_y, top)
                    if s16(near_y) <= s16(top):
                        frame = _deployment_restore_probe(memory, frame, observed)
                        return DeploymentProbeFields(_deployment_carry(memory, frame, False), False)
        occupied = occupied.advance(2)
        frame = first_replace(frame, controller=occupied)
    terrain_x, frame = _deployment_sum(memory, frame, left, 3)
    terrain_x, frame = _deployment_left_shift(memory, frame, terrain_x, 3)
    frame = first_replace(frame, target_x=_deployment_word(frame.target_x, terrain_x))
    terrain_y, frame = _deployment_sum(memory, frame, bottom, 3)
    terrain_y, frame = _deployment_left_shift(memory, frame, terrain_y, 3)
    frame = first_replace(frame, target_y=_deployment_word(frame.target_y, terrain_y))
    frame = _deployment_move_word(memory, frame, terrain_y)
    frame = first_replace(frame, unit=_deployment_word(frame.unit, terrain_y))
    frame = _deployment_move_word(memory, frame, terrain_x)
    frame = first_replace(frame, target_y=_deployment_word(frame.target_y, terrain_x))
    frame, category = _deployment_terrain_lookup(memory, frame, terrain_x, terrain_y)
    frame = _deployment_compare_byte(memory, frame, category, 1)
    blocked = category == 1
    if not blocked:
        frame = _deployment_compare_byte(memory, frame, category, 6)
        blocked = category == 6
    if not blocked:
        frame = _deployment_compare_byte(memory, frame, category, 7)
        blocked = category == 7
    if blocked:
        frame = _deployment_restore_probe(memory, frame, observed)
        return DeploymentProbeFields(_deployment_carry(memory, frame, False), False)
    current_x = terrain_x if frame.target_y is None else low16(frame.target_y)
    current_y = terrain_y if frame.unit is None else low16(frame.unit)
    position_x, frame = _deployment_left_shift(memory, frame, current_x, 7)
    frame = first_replace(frame, target_y=_deployment_word(frame.target_y, position_x))
    frame.candidates.set_word(offset, position_x)
    frame = _deployment_move_word(memory, frame, position_x)
    position_y, frame = _deployment_left_shift(memory, frame, current_y, 7)
    frame = first_replace(frame, unit=_deployment_word(frame.unit, position_y))
    frame.candidates.set_word(offset, position_y, 2)
    frame = _deployment_move_word(memory, frame, position_y)
    frame = _deployment_restore_probe(memory, frame, observed)
    return DeploymentProbeFields(_deployment_carry(memory, frame, True), True)


def _deployment_probe_call(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, x: Word, y: Word, offset: Word, continuation: Long) -> DeploymentProbeFields:
    entered = _deployment_enter(memory, frame, continuation)
    result = try_place_deployment_cell_fields(memory, entered, x, y, offset).validate(memory.state)
    return DeploymentProbeFields(_deployment_leave(memory, result.frame, continuation), result.placed)


def _deployment_vacancy_call(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, continuation: Long) -> DeploymentEdgeFields:
    if frame.scan is None or frame.candidates is None:
        raise ValueError('actual current A3 roster and A1 positions required')
    entered = _deployment_enter(memory, frame, continuation)
    vacancy = find_next_empty_position_slot_fields(memory, entered.scan,
        entered.candidates, entered.offset_y, entered.status & 16 != 0)
    status = ((16 if vacancy.extend else 0) | (8 if vacancy.negative else 0) |
        (4 if vacancy.zero else 0) | (1 if vacancy.carry else 0))
    current = _deployment_flags(memory, entered, status)
    current = first_replace(current, offset_y=vacancy.index, scan=vacancy.source)
    current = _deployment_carry(memory, current, vacancy.carry)
    return DeploymentEdgeFields(_deployment_leave(memory, current, continuation),
        vacancy.offset, vacancy.source, vacancy.carry)


def scan_deployment_first_edge_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, center_x: Word, center_y: Word, radius: Word, offset: Word, prefix: bool = True) -> DeploymentEdgeFields:
    """25CB8 or true alternate 25CBE, with current returns at each BSR."""
    frame.validate(memory.state)
    for value in (center_x, center_y, radius, offset):
        uint(value, 16)
    if type(prefix) is not bool or frame.scan is None:
        raise ValueError('actual edge entry and A3 roster required')
    if prefix:
        frame = _deployment_move_word(memory, frame, radius)
        x, frame = _deployment_difference(memory, frame, 0, radius)
        x, frame = _deployment_sum(memory, frame, x, center_x)
        frame = first_replace(frame, unit=_deployment_word(frame.unit, x))
    else:
        if frame.unit is None:
            raise ValueError('alternate first edge requires current D2 LONG')
        x = low16(frame.unit)
    frame = _deployment_compare(memory, frame, x, 3)
    if x < 3:
        return DeploymentEdgeFields(_deployment_carry(memory, frame, False), offset, frame.scan, False)
    frame = _deployment_compare(memory, frame, x, 25)
    if x > 25:
        return DeploymentEdgeFields(_deployment_carry(memory, frame, False), offset, frame.scan, False)
    frame = _deployment_move_word(memory, frame, radius)
    delta, frame = _deployment_difference(memory, frame, 0, radius)
    frame = first_replace(frame, distance=_deployment_word(frame.distance, delta))
    while True:
        current_center_y = center_y if frame.target_y is None else low16(frame.target_y)
        frame = _deployment_move_word(memory, frame, delta)
        y, frame = _deployment_sum(memory, frame, delta, current_center_y)
        frame = first_replace(frame, count=_deployment_word(frame.count, y))
        frame = _deployment_compare(memory, frame, y, 3)
        if y >= 3:
            frame = _deployment_compare(memory, frame, y, 37)
            if y <= 37:
                result = _deployment_probe_call(memory, frame, x, y, offset, 0x25CEA)
                frame = result.frame
                if result.placed:
                    vacancy = _deployment_vacancy_call(memory, frame, 0x25CF0)
                    frame, offset = vacancy.frame, vacancy.offset
                    if vacancy.found:
                        return DeploymentEdgeFields(_deployment_carry(memory, frame, True), offset, frame.scan, True)
        current_delta = delta if frame.distance is None else low16(frame.distance)
        delta, frame = _deployment_sum(memory, frame, current_delta, 2)
        frame = first_replace(frame, distance=_deployment_word(frame.distance, delta))
        current_radius = radius if frame.choice is None else low16(frame.choice)
        frame = _deployment_compare(memory, frame, delta, current_radius)
        if s16(delta) > s16(current_radius):
            return DeploymentEdgeFields(_deployment_carry(memory, frame, False), offset, frame.scan, False)
        if frame.unit is not None:
            x = low16(frame.unit)


def scan_deployment_second_edge_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, center_x: Word, center_y: Word, radius: Word, offset: Word, prefix: bool = True) -> DeploymentEdgeFields:
    """25D96 or true alternate 25D9C; the signed final test is strict <."""
    frame.validate(memory.state)
    for value in (center_x, center_y, radius, offset):
        uint(value, 16)
    if type(prefix) is not bool or frame.scan is None:
        raise ValueError('actual edge entry and A3 roster required')
    if prefix:
        frame = _deployment_move_word(memory, frame, radius)
        y, frame = _deployment_difference(memory, frame, 0, radius)
        y, frame = _deployment_sum(memory, frame, y, center_y)
        frame = first_replace(frame, count=_deployment_word(frame.count, y))
    else:
        if frame.count is None:
            raise ValueError('alternate second edge requires current D3 LONG')
        y = low16(frame.count)
    frame = _deployment_compare(memory, frame, y, 3)
    if y < 3:
        return DeploymentEdgeFields(_deployment_carry(memory, frame, False), offset, frame.scan, False)
    frame = _deployment_compare(memory, frame, y, 37)
    if y > 37:
        return DeploymentEdgeFields(_deployment_carry(memory, frame, False), offset, frame.scan, False)
    frame = _deployment_move_word(memory, frame, radius)
    delta, frame = _deployment_difference(memory, frame, radius, 2)
    delta, frame = _deployment_difference(memory, frame, 0, delta)
    frame = first_replace(frame, distance=_deployment_word(frame.distance, delta))
    while True:
        current_center_x = center_x if frame.target_x is None else low16(frame.target_x)
        frame = _deployment_move_word(memory, frame, delta)
        x, frame = _deployment_sum(memory, frame, delta, current_center_x)
        frame = first_replace(frame, unit=_deployment_word(frame.unit, x))
        frame = _deployment_compare(memory, frame, x, 3)
        if x >= 3:
            frame = _deployment_compare(memory, frame, x, 25)
            if x <= 25:
                result = _deployment_probe_call(memory, frame, x, y, offset, 0x25DCA)
                frame = result.frame
                if result.placed:
                    vacancy = _deployment_vacancy_call(memory, frame, 0x25DD2)
                    frame, offset = vacancy.frame, vacancy.offset
                    if vacancy.found:
                        return DeploymentEdgeFields(_deployment_carry(memory, frame, True), offset, frame.scan, True)
        current_delta = delta if frame.distance is None else low16(frame.distance)
        delta, frame = _deployment_sum(memory, frame, current_delta, 2)
        frame = first_replace(frame, distance=_deployment_word(frame.distance, delta))
        current_radius = radius if frame.choice is None else low16(frame.choice)
        frame = _deployment_compare(memory, frame, delta, current_radius)
        if s16(delta) >= s16(current_radius):
            return DeploymentEdgeFields(_deployment_carry(memory, frame, False), offset, frame.scan, False)
        if frame.count is not None:
            y = low16(frame.count)


def promote_first_roster_deployment_candidate_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """25DF8's sole live first-roster algorithm, not the distinct 25378 policy."""
    frame.validate(memory.state)
    rulers = memory.state.table(0xFFFFE640)
    frame = first_replace(frame, roster=rulers.cursor())
    member = memory.state.read(0xFFFFF68C, 2)
    frame = first_replace(frame, target_x=_deployment_word(frame.target_x, member))
    frame = _deployment_move_word(memory, frame, member)
    member, frame = _deployment_left_shift(memory, frame, member, 1)
    member = rulers.word(member)
    frame = first_replace(frame, target_x=_deployment_word(frame.target_x, member))
    frame = _deployment_move_word(memory, frame, member)
    heads = memory.state.table(0xFFFFA027)
    frame = first_replace(frame, roster=heads.cursor())
    previous = memory.battle_scene()
    frame = first_replace(frame, target_y=_deployment_word(frame.target_y, previous))
    frame = _deployment_move_word(memory, frame, previous)
    previous_byte = heads.byte(previous)
    previous = (previous & 65280) | previous_byte
    frame = first_replace(frame, target_y=_deployment_byte(frame.target_y, previous_byte))
    frame = _deployment_move_byte(memory, frame, previous_byte)
    frame = _deployment_compare(memory, frame, previous, member)
    if previous == member:
        return frame
    roster = memory.state.table(0xFFFFA550)
    source = roster.cursor()
    frame = first_replace(frame, roster=source)
    while True:
        item = source.next_word()
        frame = first_replace(frame, unit=_deployment_word(frame.unit, item))
        frame = _deployment_move_word(memory, frame, item)
        if negative_word(item):
            return frame
        item &= 255
        frame = first_replace(frame, unit=_deployment_word(frame.unit, item))
        frame = _deployment_move_word(memory, frame, item)
        frame = _deployment_compare(memory, frame, member, item)
        if member == item:
            break
    deployed = memory.state.table(0xFFFFAE28)
    frame = first_replace(frame, controller=deployed.cursor())
    deployed.set_byte(member, 1)
    frame = _deployment_move_byte(memory, frame, 1)
    variants = memory.scene_variants
    frame = first_replace(frame, roster=variants.cursor())
    scene = memory.battle_scene()
    frame = first_replace(frame, unit=_deployment_word(frame.unit, scene))
    frame = _deployment_move_word(memory, frame, scene)
    formation_byte = variants.byte(scene)
    if frame.count is None:
        raise ValueError('actual retained D3 needed by first promotion variant BYTE alias')
    formation = low16(replace_byte(frame.count, formation_byte))
    frame = first_replace(frame, count=_deployment_byte(frame.count, formation_byte))
    frame = _deployment_move_byte(memory, frame, formation_byte)
    formation, frame = _deployment_left_shift(memory, frame, formation, 1)
    frame = first_replace(frame, count=_deployment_word(frame.count, formation))
    cell, frame = _deployment_left_shift(memory, frame, scene, 5)
    cell, frame = _deployment_sum(memory, frame, cell, formation)
    frame = first_replace(frame, unit=_deployment_word(frame.unit, cell))
    member_offset, frame = _deployment_left_shift(memory, frame, member, 2)
    frame = first_replace(frame, target_x=_deployment_word(frame.target_x, member_offset))
    cells = memory.deployment_cells
    positions = memory.state.table(0x00FF2C00)
    frame = first_replace(frame, candidates=cells.cursor(), scan=positions.cursor())
    frame = first_replace(frame, count=_deployment_word(frame.count, 0))
    frame = _deployment_move_word(memory, frame, 0)
    x_byte = cells.byte(cell)
    frame = first_replace(frame, count=_deployment_byte(frame.count, x_byte))
    frame = _deployment_move_byte(memory, frame, x_byte)
    x, frame = _deployment_left_shift(memory, frame, x_byte, 3)
    frame = first_replace(frame, count=_deployment_word(frame.count, x))
    positions.set_word(member_offset, x)
    frame = _deployment_move_word(memory, frame, x)
    frame = first_replace(frame, count=_deployment_word(frame.count, 0))
    frame = _deployment_move_word(memory, frame, 0)
    y_byte = cells.byte(cell, 1)
    frame = first_replace(frame, count=_deployment_byte(frame.count, y_byte))
    frame = _deployment_move_byte(memory, frame, y_byte)
    y, frame = _deployment_left_shift(memory, frame, y_byte, 3)
    frame = first_replace(frame, count=_deployment_word(frame.count, y))
    positions.set_word(member_offset, y, 2)
    frame = _deployment_move_word(memory, frame, y)
    fixed_positions = memory.state.table(0xFFFFA150)
    frame = first_replace(frame, roster=fixed_positions.cursor())
    previous_offset, frame = _deployment_left_shift(memory, frame, previous, 2)
    frame = first_replace(frame, target_y=_deployment_word(frame.target_y, previous_offset))
    frame = first_replace(frame, count=_deployment_word(frame.count, 0))
    frame = _deployment_move_word(memory, frame, 0)
    x_byte = cells.byte(cell)
    frame = _deployment_move_byte(memory, frame, x_byte)
    x, frame = _deployment_left_shift(memory, frame, x_byte, 3)
    x, frame = _deployment_left_shift(memory, frame, x, 7)
    previous_x = fixed_positions.word(previous_offset)
    x_difference, frame = _deployment_difference(memory, frame, x, previous_x)
    if x < previous_x:
        x_difference, frame = _deployment_difference(memory, frame, 0, x_difference)
    frame = first_replace(frame, count=_deployment_word(frame.count, x_difference))
    frame = _deployment_compare(memory, frame, x_difference, 1024)
    if x_difference <= 1024:
        frame = first_replace(frame, count=_deployment_word(frame.count, 0))
        frame = _deployment_move_word(memory, frame, 0)
        y_byte = cells.byte(cell, 1)
        frame = _deployment_move_byte(memory, frame, y_byte)
        y, frame = _deployment_left_shift(memory, frame, y_byte, 3)
        y, frame = _deployment_left_shift(memory, frame, y, 7)
        previous_y = fixed_positions.word(previous_offset, 2)
        y_difference, frame = _deployment_difference(memory, frame, y, previous_y)
        if y < previous_y:
            y_difference, frame = _deployment_difference(memory, frame, 0, y_difference)
        frame = first_replace(frame, count=_deployment_word(frame.count, y_difference))
        frame = _deployment_compare(memory, frame, y_difference, 1024)
        if y_difference < 1024:
            x = fixed_positions.word(member_offset)
            frame = _deployment_move_word(memory, frame, x)
            x, frame = _deployment_right_shift(memory, frame, x, 7)
            frame = first_replace(frame, count=_deployment_word(frame.count, x))
            positions.set_word(previous_offset, x)
            frame = _deployment_move_word(memory, frame, x)
            y = fixed_positions.word(member_offset, 2)
            frame = _deployment_move_word(memory, frame, y)
            y, frame = _deployment_right_shift(memory, frame, y, 7)
            frame = first_replace(frame, count=_deployment_word(frame.count, y))
            positions.set_word(previous_offset, y, 2)
            frame = _deployment_move_word(memory, frame, y)
            previous, frame = _deployment_right_shift(memory, frame, previous_offset, 2)
            frame = first_replace(frame, target_y=_deployment_word(frame.target_y, previous))
            deployed.set_byte(previous, 1)
            frame = _deployment_move_byte(memory, frame, 1)
    member, frame = _deployment_right_shift(memory, frame, member_offset, 2)
    frame = first_replace(frame, target_x=_deployment_word(frame.target_x, member))
    source, destination = roster.cursor(), roster.cursor(2)
    frame = first_replace(frame, roster=source, candidates=destination)
    while True:
        item = source.next_word()
        frame = first_replace(frame, target_y=_deployment_word(frame.target_y, item))
        frame = _deployment_move_word(memory, frame, item)
        if negative_word(item):
            break
        frame = _deployment_compare(memory, frame, item, member)
        if item == member:
            continue
        destination.append_word(item)
        frame = _deployment_move_word(memory, frame, item)
    roster.set_word(0, member)
    frame = _deployment_move_word(memory, frame, member)
    frame = first_replace(frame, roster=heads.cursor())
    scene = memory.battle_scene()
    frame = first_replace(frame, target_y=_deployment_word(frame.target_y, scene))
    frame = _deployment_move_word(memory, frame, scene)
    heads.set_byte(scene, low8(member))
    return _deployment_move_byte(memory, frame, low8(member))


def promote_second_roster_deployment_candidate_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """25F28 preserves candidate*4 as ID; it is not 253E0's head/reorder tail."""
    frame.validate(memory.state)
    rulers = memory.state.table(0xFFFFE640)
    frame = first_replace(frame, roster=rulers.cursor())
    member = memory.state.read(0xFFFFF68E, 2)
    frame = first_replace(frame, target_x=_deployment_word(frame.target_x, member))
    frame = _deployment_move_word(memory, frame, member)
    member, frame = _deployment_left_shift(memory, frame, member, 1)
    member = rulers.word(member)
    frame = first_replace(frame, target_x=_deployment_word(frame.target_x, member))
    frame = _deployment_move_word(memory, frame, member)
    heads = memory.state.table(0xFFFFF45E)
    frame = first_replace(frame, roster=heads.cursor())
    scene = memory.battle_scene()
    frame = first_replace(frame, target_y=_deployment_word(frame.target_y, scene))
    frame = _deployment_move_word(memory, frame, scene)
    scene_offset, frame = _deployment_left_shift(memory, frame, scene, 1)
    previous = heads.word(scene_offset)
    frame = first_replace(frame, target_y=_deployment_word(frame.target_y, previous))
    frame = _deployment_move_word(memory, frame, previous)
    frame = _deployment_compare(memory, frame, previous, member)
    if previous == member:
        return frame
    roster = memory.state.table(0xFFFFA5A4)
    source = roster.cursor()
    frame = first_replace(frame, roster=source)
    while True:
        item = source.next_word()
        frame = first_replace(frame, unit=_deployment_word(frame.unit, item))
        frame = _deployment_move_word(memory, frame, item)
        if negative_word(item):
            return frame
        item &= 255
        frame = first_replace(frame, unit=_deployment_word(frame.unit, item))
        frame = _deployment_move_word(memory, frame, item)
        frame = _deployment_compare(memory, frame, item, member)
        if item == member:
            break
    deployed = memory.state.table(0xFFFFAE28)
    frame = first_replace(frame, controller=deployed.cursor())
    deployed.set_byte(member, 1)
    frame = _deployment_move_byte(memory, frame, 1)
    catalog = memory.state.table(0xAD86E)
    frame = first_replace(frame, roster=catalog.cursor())
    scene = memory.battle_scene()
    frame = first_replace(frame, unit=_deployment_word(frame.unit, scene))
    frame = _deployment_move_word(memory, frame, scene)
    frame = first_replace(frame, count=_deployment_word(frame.count, scene))
    frame = _deployment_move_word(memory, frame, scene)
    cell, frame = _deployment_left_shift(memory, frame, scene, 1)
    cell, frame = _deployment_sum(memory, frame, cell, scene)
    cell, frame = _deployment_left_shift(memory, frame, cell, 1)
    cell, frame = _deployment_sum(memory, frame, cell, scene)
    cell, frame = _deployment_left_shift(memory, frame, cell, 2)
    cell, frame = _deployment_sum(memory, frame, cell, scene)
    cell, frame = _deployment_left_shift(memory, frame, cell, 1)
    frame = first_replace(frame, unit=_deployment_word(frame.unit, cell))
    positions = memory.state.table(0x00FF2C00)
    frame = first_replace(frame, candidates=positions.cursor())
    scaled_member, frame = _deployment_left_shift(memory, frame, member, 2)
    frame = first_replace(frame, target_x=_deployment_word(frame.target_x, scaled_member))
    frame = first_replace(frame, count=_deployment_word(frame.count, 0))
    frame = _deployment_move_word(memory, frame, 0)
    x_byte = catalog.byte(cell)
    frame = _deployment_move_byte(memory, frame, x_byte)
    x, frame = _deployment_left_shift(memory, frame, x_byte, 3)
    x, frame = _deployment_left_shift(memory, frame, x, 7)
    frame = first_replace(frame, count=_deployment_word(frame.count, x))
    positions.set_word(scaled_member, x)
    frame = _deployment_move_word(memory, frame, x)
    frame = first_replace(frame, count=_deployment_word(frame.count, 0))
    frame = _deployment_move_word(memory, frame, 0)
    y_byte = catalog.byte(cell, 1)
    frame = _deployment_move_byte(memory, frame, y_byte)
    y, frame = _deployment_left_shift(memory, frame, y_byte, 3)
    y, frame = _deployment_left_shift(memory, frame, y, 7)
    frame = first_replace(frame, count=_deployment_word(frame.count, y))
    positions.set_word(scaled_member, y, 2)
    frame = _deployment_move_word(memory, frame, y)
    source, destination = roster.cursor(), roster.cursor(2)
    frame = first_replace(frame, roster=source, candidates=destination)
    while True:
        item = source.next_word()
        frame = first_replace(frame, unit=_deployment_word(frame.unit, item))
        frame = _deployment_move_word(memory, frame, item)
        if negative_word(item):
            break
        item &= 255
        frame = first_replace(frame, unit=_deployment_word(frame.unit, item))
        frame = _deployment_move_word(memory, frame, item)
        frame = _deployment_compare(memory, frame, item, scaled_member)
        if item == scaled_member:
            continue
        destination.append_word(item)
        frame = _deployment_move_word(memory, frame, item)
    roster.set_word(0, scaled_member)
    frame = _deployment_move_word(memory, frame, scaled_member)
    frame = first_replace(frame, roster=heads.cursor())
    scene = memory.battle_scene()
    frame = first_replace(frame, target_y=_deployment_word(frame.target_y, scene))
    frame = _deployment_move_word(memory, frame, scene)
    scene_offset, frame = _deployment_left_shift(memory, frame, scene, 1)
    frame = first_replace(frame, target_y=_deployment_word(frame.target_y, scene_offset))
    heads.set_word(scene_offset, scaled_member)
    return _deployment_move_word(memory, frame, scaled_member)


def sample_battle_action_random_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, continuation: Long) -> FirstDeploymentFrame:
    """One accepted RNG algorithm, with the caller's actual return LONG."""
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('same-state memory and actual battle action fields required')
    frame.validate(memory.state, frame.stack_cursor is not None)
    frame = _deployment_enter(memory, frame, continuation)
    frame = first_deployment_random_fields(memory, frame)
    memory.state.sr = (memory.state.sr & 65504) | frame.status
    return _deployment_leave(memory, frame, continuation)


def _battle_action_map_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1A438 fields around its unique map reader, including the real D4 slot."""
    frame.validate(memory.state, frame.stack_cursor is not None)
    observed = frame.distance
    if frame.stack_cursor is not None:
        frame = _deployment_push(memory, frame, observed)
    map_context = load_battlefield_map_fields(memory)
    frame = first_replace(frame, roster=map_context.cursor())
    if frame.stack_cursor is not None:
        frame, observed = _deployment_pop(memory, frame)
    frame = first_replace(frame, distance=observed)
    if observed is not None:
        frame = _contact_status(frame, observed, 32)
    else:
        frame = first_replace(frame, status=None)
    return frame


def select_action_candidate_by_terrain_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, policy: ActionTerrainPolicy, terrain_return: Long | None=None, training_return: Long | None=None, positions_in_controller: bool=False) -> FirstDeploymentFrame:
    """The sole shared live ranking loop, now preserving actual partial writes."""
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('same current candidate memory and fields required')
    if type(policy) is not ActionTerrainPolicy:
        raise ValueError('original typed terrain policy required')
    state = memory.state
    complete = frame.stack_cursor is not None
    frame.validate(state, complete)
    if type(positions_in_controller) is not bool:
        raise ValueError('actual candidate pointer-role selector required')
    if complete:
        uint(terrain_return, 32)
        uint(training_return, 32)
    checked_policy_table(frame.roster, state)
    frame = first_replace(frame, candidates=state.table(4294955776).cursor(), controller=state.table(4294943056 if positions_in_controller else 4294952960).cursor(), scan=state.table(4294952960 if positions_in_controller else 4294943056).cursor(), distance=0)
    frame = _contact_status(frame, 0, 32)
    frame = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, 65535))
    frame = _contact_status(frame, 65535, 16)
    while True:
        source = frame.candidates
        member = source.word()
        frame = first_replace(frame, candidates=source.advance(2), count=_contact_retained_word(frame.count, member))
        frame = _contact_status(frame, member, 16)
        if negative_word(member):
            return frame.validate(state, complete)
        member &= 255
        frame = first_replace(frame, count=_contact_retained_word(frame.count, member))
        frame = _contact_status(frame, member, 16)
        frame = first_replace(frame, unit=_contact_retained_word(frame.unit, member))
        frame = _contact_status(frame, member, 16)
        offset, frame = _deployment_left_shift(memory, frame, member, 2)
        frame = first_replace(frame, unit=_contact_retained_word(frame.unit, offset))
        positions = frame.controller if positions_in_controller else frame.scan
        x = positions.word(offset)
        frame = first_replace(frame, target_y=_contact_retained_word(frame.target_y, x))
        frame = _contact_status(frame, x, 16)
        x, frame = _deployment_right_shift(memory, frame, x, 7)
        frame = first_replace(frame, target_y=_contact_retained_word(frame.target_y, x))
        y = positions.word(offset, 2)
        frame = first_replace(frame, unit=_contact_retained_word(frame.unit, y))
        frame = _contact_status(frame, y, 16)
        y, frame = _deployment_right_shift(memory, frame, y, 7)
        frame = first_replace(frame, unit=_contact_retained_word(frame.unit, y))
        frame, terrain = _deployment_terrain_lookup(memory, frame, x, y, 157578 if terrain_return is None else terrain_return)
        for kind in policy.kinds:
            frame = _deployment_compare_byte(memory, frame, terrain, kind)
            if terrain == kind:
                break
        if not action_terrain_is_eligible(frame.target_x, policy):
            continue
        member = member if frame.count is None else low16(frame.count)
        frame = first_replace(frame, target_x=_contact_retained_word(frame.target_x, member))
        frame = _contact_status(frame, member, 16)
        entered = _deployment_enter(memory, frame, 157592 if training_return is None else training_return)
        trained = weighted_training_factor_fields(memory, entered, member)
        frame = _deployment_leave(memory, trained.frame, 157592 if training_return is None else training_return)
        offset, frame = _deployment_left_shift(memory, frame, low16(frame.target_x), 2)
        frame = first_replace(frame, target_x=_contact_retained_word(frame.target_x, offset))
        troop_table = frame.scan if positions_in_controller else frame.controller
        troops = troop_table.word(offset, 2)
        score = low16(frame.target_y) * troops
        frame = first_replace(frame, target_y=score)
        frame = _contact_status(frame, score, 32)
        strongest = frame.distance
        compared = u32(score - strongest)
        frame = _contact_status(frame, compared, 32, score < strongest, bool((score ^ strongest) & (score ^ compared) & 2147483648))
        if is_better_action_score(score, strongest):
            frame = first_replace(frame, distance=score)
            frame = _contact_status(frame, score, 32)
            member = member if frame.count is None else low16(frame.count)
            frame = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, member))
            frame = _contact_status(frame, member, 16)


def select_strongest_type6_candidate_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26752 uses the one map reader and the same shared candidate ranking."""
    frame.validate(memory.state, frame.stack_cursor is not None)
    frame = _deployment_enter(memory, frame, 0x26758)
    frame = _battle_action_map_fields(memory, frame)
    frame = _deployment_leave(memory, frame, 0x26758)
    return select_action_candidate_by_terrain_fields(memory, frame, ActionTerrainPolicy((6,)),
        0x2678A, 0x26798)


def state_mixed_action_requirement_fields(frame: FirstDeploymentFrame, draw: ActionRandomDraw,
        strength: Long, base: Word) -> FirstDeploymentFrame:
    """The existing mixed-state transaction delegates the sole11-factor rule."""
    if type(frame) is not FirstDeploymentFrame or type(draw) is not ActionRandomDraw:
        raise ValueError('current fields and actual full random-state draw required')
    uint(strength, 32)
    uint(base, 16)
    frame = first_replace(frame, unit=strength)
    frame = _action_random_factor_fields(frame, draw, base)
    divided = divu_retained(strength, low16(frame.target_x))
    return _first_long(frame, 'unit', low16(divided))


def compute_type6_budget_from_random_state_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """267AA: live selected troops before RNG; both full state mixes are retained."""
    frame.validate(memory.state, frame.stack_cursor is not None)
    uint(frame.offset_x, 32)
    troops = memory.state.table(0xFFFFC800).cursor()
    frame = first_replace(frame, roster=troops)
    offset, frame = _deployment_left_shift(memory, frame, low16(frame.offset_x), 2)
    frame = first_replace(frame, offset_x=replace_word(frame.offset_x, offset))
    strength = troops.long(offset)
    frame = first_replace(frame, unit=strength)
    frame = _contact_status(frame, strength, 32)
    frame = sample_battle_action_random_fields(memory, frame, 0x267BA)
    draw = ActionRandomDraw(low16(frame.target_x), frame.target_y)
    frame = state_mixed_action_requirement_fields(frame, draw, frame.unit, 40)
    memory.state.write(0xFFFFF39E, 4, frame.unit)
    frame = _contact_status(frame, frame.unit, 32)
    memory.state.sr = (memory.state.sr & 65504) | frame.status
    return frame.validate(memory.state, frame.stack_cursor is not None)

def select_lowest_filtered_rating_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26638 retains original zero eligibility, pointers and incoming D1."""
    return select_action_lowest_rating_fields(memory, frame, False)

def select_strongest_type1_candidate_second_side_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26A20: real map call, then the sole ranking loop with A2 positions."""
    frame.validate(memory.state, frame.stack_cursor is not None)
    frame = _deployment_enter(memory, frame, 0x26A26)
    frame = _battle_action_map_fields(memory, frame)
    frame = _deployment_leave(memory, frame, 0x26A26)
    return select_action_candidate_by_terrain_fields(memory, frame,
        ActionTerrainPolicy((1,)), 0x26A58, 0x26A66, True)

def compute_type1_candidate_budget_base20_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26A78 supplies its original base20 and real26A88 RNG continuation."""
    return compute_candidate_budget_fields(memory, frame, 20, 0x26A88)

def test_actor_map_relative_types_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26B2E keeps original A0 map-coordinate alias and inverted0/4/7 carry."""
    return test_actor_action_terrain_gate_fields(memory, frame, False)

def select_strongest_type2_candidate_with_map_context_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26B74 inherits A0 from the real actor gate, using A2 positions/A3 troops."""
    frame.validate(memory.state, frame.stack_cursor is not None)
    checked_policy_table(frame.roster, memory.state)
    return select_action_candidate_by_terrain_fields(memory, frame,
        ActionTerrainPolicy((2,)), 0x26BA6, 0x26BB4, True)

def compute_type2_candidate_budget_base30_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26BC6 supplies its original base30 and true26BD6 RNG return."""
    return compute_candidate_budget_fields(memory, frame, 30, 0x26BD6)


def select_strongest_open_terrain_candidate_second_side_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26854: original ordered0/3/7/1 policy with A2 positions and A3 troops."""
    frame.validate(memory.state, frame.stack_cursor is not None)
    frame = _deployment_enter(memory, frame, 0x2685A)
    frame = _battle_action_map_fields(memory, frame)
    frame = _deployment_leave(memory, frame, 0x2685A)
    return select_action_candidate_by_terrain_fields(memory, frame,
        ActionTerrainPolicy((0, 3, 7, 1)), 0x2688C, 0x268B2, True)


def compute_candidate_budget_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame,
        base: Word, continuation: Long) -> FirstDeploymentFrame:
    """Sample-only candidate budget, sharing the sole11-term field arithmetic."""
    frame.validate(memory.state, frame.stack_cursor is not None)
    uint(frame.offset_x, 32)
    uint(base, 16)
    uint(continuation, 32)
    troops = memory.state.table(0xFFFFC800).cursor()
    frame = first_replace(frame, roster=troops)
    offset, frame = _deployment_left_shift(memory, frame, low16(frame.offset_x), 2)
    frame = first_replace(frame, offset_x=replace_word(frame.offset_x, offset))
    strength = troops.long(offset)
    frame = first_replace(frame, unit=strength)
    frame = _contact_status(frame, strength, 32)
    frame = sample_battle_action_random_fields(memory, frame, continuation)
    sample = low16(frame.target_x)
    # Original AND.L D0, then MOVE.L D0,D1: D1 is sample, not the RNG seed.
    frame = state_mixed_action_requirement_fields(frame,
        ActionRandomDraw(sample, sample), frame.unit, base)
    memory.state.write(0xFFFFF39E, 4, frame.unit)
    frame = _contact_status(frame, frame.unit, 32)
    memory.state.sr = (memory.state.sr & 65504) | frame.status
    return frame.validate(memory.state, frame.stack_cursor is not None)


def compute_candidate_budget_base20_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """268C4 actual base20 and268D4 RNG return, not the base30 entry."""
    return compute_candidate_budget_fields(memory, frame, 20, 0x268D4)


def compute_candidate_budget_base30_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26972 actual base30 and26982 RNG return."""
    return compute_candidate_budget_fields(memory, frame, 30, 0x26982)

def read_selected_action_attribute_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, Word]:
    """Shared selected-officer B400/B600 WORD reads, in original order."""
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('same-state selected attributes and actual frame required')
    frame.validate(memory.state, frame.stack_cursor is not None)
    attributes_one = memory.state.table(0xFFFFB400).cursor()
    frame = first_replace(frame, roster=attributes_one)
    selected = memory.state.read(0xFFFFF3A6, 2)
    frame = _first_word(frame, 'target_x', selected)
    frame = _first_shift_word(frame, 'target_x', selected, 1)
    offset = u16(selected << 1)
    attributes = attributes_one.word(offset)
    frame = _first_word(frame, 'unit', attributes)
    attributes_two = memory.state.table(0xFFFFB600).cursor()
    frame = first_replace(frame, roster=attributes_two)
    additional = attributes_two.word(offset)
    frame = _first_add_word(frame, 'unit', attributes, additional)
    attributes = u16(attributes + additional)
    if frame.status is not None:
        memory.state.sr = (memory.state.sr & 65504) | frame.status
    return frame, attributes

def compute_selected_attribute_budget_second_side_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2665E: both attribute reads precede the real 2667A RNG return."""
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('same-state action-budget memory and actual frame required')
    frame.validate(memory.state, frame.stack_cursor is not None)
    frame, attributes = read_selected_action_attribute_fields(memory, frame)
    frame = _deployment_enter(memory, frame, 0x2667A)
    frame = first_deployment_random_fields(memory, frame)
    frame = _deployment_leave(memory, frame, 0x2667A)
    sample = low16(frame.target_x)
    # The existing requirement policy remains the sole multiply/factor logic.
    requirement = attribute_action_requirement(sample, attributes, 8)
    # After ANDI.L/MOVE.L/LSL.L/ADD.L/SWAP/ADDQ.W, the factor is 8..12:
    # final ADDQ has no carry; MULU then MOVE.L retain X=0 and clear V/C.
    frame = first_replace(frame, target_y=sample, status=0)
    frame = _first_long(frame, 'target_x', requirement)
    memory.state.write(0xFFFFF39E, 4, requirement)
    memory.state.sr = (memory.state.sr & 65504) | frame.status
    return frame.validate(memory.state, frame.stack_cursor is not None)

def build_non_type6_candidates_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26692: live ordered exclusion list; A3, not unused A2, owns positions."""
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('same-state candidate-filter memory and actual frame required')
    frame.validate(memory.state, frame.stack_cursor is not None)
    frame = _deployment_enter(memory, frame, 0x26698)
    frame = _battle_action_map_fields(memory, frame)
    frame = _deployment_leave(memory, frame, 0x26698)
    source = memory.state.table(0xFFFFD300).cursor()
    unused_troops = memory.state.table(0xFFFFC800).cursor()
    positions = memory.state.table(0xFFFFA150).cursor()
    destination = memory.state.table(0xFFFFD400).cursor()
    frame = first_replace(frame, candidates=source, controller=unused_troops,
        scan=positions, opponent=destination)
    while True:
        member = source.next_word()
        frame = _first_word(frame, 'count', member)
        if negative_word(member):
            break
        member = member & 255
        frame = _first_word(frame, 'count', member)
        frame = _first_word(frame, 'unit', member)
        frame = _first_shift_word(frame, 'unit', member, 2)
        offset = u16(member << 2)
        x_fixed = positions.word(offset)
        frame = _first_word(frame, 'target_y', x_fixed)
        frame = _first_right_word(frame, 'target_y', x_fixed, 7)
        x = x_fixed >> 7
        y_fixed = positions.word(offset, 2)
        frame = _first_word(frame, 'unit', y_fixed)
        frame = _first_right_word(frame, 'unit', y_fixed, 7)
        y = y_fixed >> 7
        frame, terrain = _deployment_terrain_lookup(memory, frame, x, y, 0x266C8)
        frame = _deployment_compare_byte(memory, frame, terrain, 6)
        if terrain != 6:
            if frame.count is not None:
                member = low16(frame.count)
            destination.append_word(member)
            frame = _first_memory_word(frame, member)
    destination.put_word(65535)
    frame = _first_memory_word(frame, 65535)
    if frame.status is not None:
        memory.state.sr = (memory.state.sr & 65504) | frame.status
    return frame.validate(memory.state, frame.stack_cursor is not None)


def _action_child_frame(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('same-state action memory and actual child frame required')
    return frame.validate(memory.state, frame.stack_cursor is not None)


def _action_child_publish(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    if frame.status is not None:
        memory.state.sr = (memory.state.sr & 65504) | frame.status
    return frame.validate(memory.state, frame.stack_cursor is not None)


def _action_factor_add_long_fields(frame: FirstDeploymentFrame,
        carrier: str, source: Long) -> FirstDeploymentFrame:
    """Only the actual random-factor D0/D1/D2 ADD.L roles."""
    if carrier not in ('target_x', 'target_y', 'unit'):
        raise ValueError('actual budget-factor LONG destination required')
    left = uint(frame.carrier(carrier), 32)
    source = uint(source, 32)
    wide = left + source
    value = u32(wide)
    frame = first_replace(frame, **{carrier:value})
    return _contact_status(frame, value, 32, wide > 4294967295,
        bool(~(left ^ source) & (left ^ value) & 2147483648), wide > 4294967295)


def _action_factor_shift_long_fields(frame: FirstDeploymentFrame,
        amount: int) -> FirstDeploymentFrame:
    """The factor's original #2 and #1 LSL.L D0 operations only."""
    if amount not in (1, 2):
        raise ValueError('actual action-factor LONG shift required')
    before = uint(frame.target_x, 32)
    value = u32(before << amount)
    carry = bool(before & (1 << (32 - amount)))
    frame = first_replace(frame, target_x=value)
    return _contact_status(frame, value, 32, carry, False, carry)


def _action_random_factor_fields(frame: FirstDeploymentFrame,
        draw: ActionRandomDraw, base: Word, multiplier: Word=11,
        scratch: str='target_y') -> FirstDeploymentFrame:
    """Sole closed5/10/11 random factor; preserve even the unused10-plan ADD."""
    if type(frame) is not FirstDeploymentFrame or type(draw) is not ActionRandomDraw:
        raise ValueError('actual random draw and current factor fields required')
    uint(base, 16)
    if multiplier not in (5, 10, 11) or scratch not in ('target_y', 'unit'):
        raise ValueError('actual attribute/troop factor role required')
    frame = _first_long(frame, 'target_x', uint(draw.sample, 16))
    frame = _first_long(frame, scratch, uint(draw.updated_state, 32))
    frame = _action_factor_shift_long_fields(frame, 2)
    frame = _action_factor_add_long_fields(frame, 'target_x', frame.carrier(scratch))
    if multiplier != 5:
        frame = _action_factor_shift_long_fields(frame, 1)
        if multiplier == 10:
            # 26228 is ADD.L D0,D1. D0 stays10*sample, unlike the11 plan.
            frame = _action_factor_add_long_fields(frame, scratch, frame.target_x)
        else:
            frame = _action_factor_add_long_fields(frame, 'target_x', frame.carrier(scratch))
    value = u32((frame.target_x << 16) | (frame.target_x >> 16))
    frame = _first_long(frame, 'target_x', value)
    return _first_add_word(frame, 'target_x', low16(value), base)


def _action_attribute_product_fields(frame: FirstDeploymentFrame,
        attributes: Word) -> FirstDeploymentFrame:
    """Sole actual MULU.W attributes,D0; its complete LONG result retains X."""
    uint(attributes, 16)
    return _first_long(frame, 'target_x', low16(frame.target_x) * attributes)


def select_action_lowest_rating_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, first_side: bool) -> FirstDeploymentFrame:
    """One rating scan, with the two original pointer/init/zero-rating roles."""
    frame = _action_child_frame(memory, frame)
    if type(first_side) is not bool:
        raise ValueError('actual first/filtered-side rating role required')
    uint(frame.target_x, 32)
    uint(frame.target_y, 32)
    ratings = memory.state.table(0xFFFFC300).cursor()
    source = memory.state.table(0xFFFFD300 if first_side else 0xFFFFD400).cursor()
    frame = first_replace(frame, roster=source if first_side else ratings,
        candidates=ratings if first_side else source)
    frame = _first_word(frame, 'target_x', 65535)
    if first_side:
        frame = _first_word(frame, 'target_y', 65535)
    while True:
        member = source.next_word()
        frame = _first_word(frame, 'unit', member)
        if negative_word(member):
            break
        member &= 255
        frame = _first_word(frame, 'unit', member)
        value = ratings.byte(member)
        frame = _first_byte(frame, 'count', value)
        if first_side and value == 0:
            continue
        if frame.status is not None:
            frame = _deployment_compare_byte(memory, frame, value, low8(frame.target_x))
        if value < low8(frame.target_x):
            frame = _first_byte(frame, 'target_x', value)
            frame = _first_word(frame, 'target_y', member)
    return _action_child_publish(memory, frame)


def select_lowest_nonzero_rating_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26086: source A0 D300, rating A1 C300, both sentinel WORD initializers."""
    return select_action_lowest_rating_fields(memory, frame, True)


def compute_selected_attribute_budget_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, base: Word=8) -> FirstDeploymentFrame:
    """260B0: RNG before both attribute reads; real D2 scratch and D3 sum."""
    frame = _action_child_frame(memory, frame)
    frame = sample_battle_action_random_fields(memory, frame, 0x260B6)
    sample = low16(frame.target_x)
    frame = _action_random_factor_fields(frame, ActionRandomDraw(sample, sample), base, 5, 'unit')
    first = memory.state.table(0xFFFFB400).cursor()
    frame = first_replace(frame, roster=first)
    selected = memory.state.read(0xFFFFF3A6, 2)
    frame = _first_word(frame, 'unit', selected)
    frame = _first_shift_word(frame, 'unit', selected, 1)
    offset = u16(selected << 1)
    attributes = first.word(offset)
    frame = _first_word(frame, 'count', attributes)
    second = memory.state.table(0xFFFFB600).cursor()
    frame = first_replace(frame, roster=second)
    additional = second.word(offset)
    frame = _first_add_word(frame, 'count', attributes, additional)
    frame = _action_attribute_product_fields(frame, u16(attributes + additional))
    memory.state.write(0xFFFFF39E, 4, frame.target_x)
    frame = _first_long(frame, 'target_x', frame.target_x)
    return _action_child_publish(memory, frame)


def _select_first_side_terrain_action_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, kind: int) -> FirstDeploymentFrame:
    """Three true first-side entry plans use the already sole ranking loop."""
    frame = _action_child_frame(memory, frame)
    if kind == 0:
        map_return, terrain_return, training_return = 0x261AA, 0x261DC, 0x26202
        policy = ActionTerrainPolicy((0, 3, 7, 1))
    elif kind == 1:
        map_return, terrain_return, training_return = 0x2637E, 0x263B0, 0x263BE
        policy = ActionTerrainPolicy((1,))
    elif kind == 2:
        map_return, terrain_return, training_return = 0x264D6, 0x26508, 0x26516
        policy = ActionTerrainPolicy((2,))
    else:
        raise ValueError('actual first-side open/type1/type2 ranking role required')
    frame = _deployment_enter(memory, frame, map_return)
    frame = _battle_action_map_fields(memory, frame)
    frame = _deployment_leave(memory, frame, map_return)
    frame = select_action_candidate_by_terrain_fields(memory, frame, policy,
        terrain_return, training_return, True)
    return _action_child_publish(memory, frame)


def select_strongest_open_terrain_candidate_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """261A4: real map token, A2 positions/A3 troops and0/3/7/1 policy."""
    return _select_first_side_terrain_action_fields(memory, frame, 0)


def select_strongest_type1_candidate_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26378: one type1 ranking, with its exact map/terrain/training calls."""
    return _select_first_side_terrain_action_fields(memory, frame, 1)


def select_strongest_type2_candidate_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """264D0: one type2 ranking, with its exact map/terrain/training calls."""
    return _select_first_side_terrain_action_fields(memory, frame, 2)


def _compute_first_selected_troop_budget_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, role: int, base: Word) -> FirstDeploymentFrame:
    """One selected-troop budget transaction with four true scaling/store plans."""
    frame = _action_child_frame(memory, frame)
    if role == 0:
        continuation, multiplier, reload_previous = 0x2621A, 10, False
    elif role == 1:
        continuation, multiplier, reload_previous = 0x262CC, 11, False
    elif role == 2:
        continuation, multiplier, reload_previous = 0x263D6, 11, True
    elif role == 3:
        continuation, multiplier, reload_previous = 0x2652E, 11, False
    else:
        raise ValueError('actual first-side selected-troop budget role required')
    frame = sample_battle_action_random_fields(memory, frame, continuation)
    sample = low16(frame.target_x)
    frame = _action_random_factor_fields(frame, ActionRandomDraw(sample, sample), base, multiplier)
    troops = memory.state.table(0xFFFFC800).cursor()
    frame = first_replace(frame, roster=troops)
    selected = memory.state.read(0xFFFFF3A6, 2)
    frame = _first_word(frame, 'target_y', selected)
    frame = _first_shift_word(frame, 'target_y', selected, 2)
    strength = troops.long(u16(selected << 2))
    frame = _first_long(frame, 'target_y', strength)
    # DIVU does not change X. Overflow retains the dividend; the immediate
    # ANDI.L overwrites undefined NZVC. Use the existing sole divu_retained
    # result rather than stop before the source's real masking instruction.
    divided = divu_retained(strength, low16(frame.target_x))
    frame = _first_long(frame, 'target_y', low16(divided))
    if reload_previous:
        frame = _first_long(frame, 'target_y', memory.state.read(0xFFFFF39E, 4))
    else:
        memory.state.write(0xFFFFF39E, 4, frame.target_y)
        frame = _first_long(frame, 'target_y', frame.target_y)
    return _action_child_publish(memory, frame)


def compute_selected_troop_budget_base20_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, base: Word=20) -> FirstDeploymentFrame:
    """26214: actual10-factor D0; retain unused ADD.L D0,D1 before reload."""
    return _compute_first_selected_troop_budget_fields(memory, frame, 0, base)


def compute_selected_troop_budget_base30_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, base: Word=30) -> FirstDeploymentFrame:
    """262C6: actual11-factor and base30, returned/stored in D1."""
    return _compute_first_selected_troop_budget_fields(memory, frame, 1, base)


def compute_then_reload_previous_selected_budget_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, base: Word=20) -> FirstDeploymentFrame:
    """263D0: real division/mask followed by F39E reload, not a computed write."""
    return _compute_first_selected_troop_budget_fields(memory, frame, 2, base)


def compute_selected_type2_budget_base30_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, base: Word=30) -> FirstDeploymentFrame:
    """26528: same one selected-budget rule, own true2652E RNG token."""
    return _compute_first_selected_troop_budget_fields(memory, frame, 3, base)


def test_actor_action_terrain_gate_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, first_side: bool) -> FirstDeploymentFrame:
    """Both actor gates share coordinate/terrain code; original alias stays explicit."""
    frame = _action_child_frame(memory, frame)
    if type(first_side) is not bool:
        raise ValueError('actual first/second actor terrain gate required')
    uint(frame.choice, 32)
    map_return, terrain_return = (0x26490,0x264AA) if first_side else (0x26B34,0x26B4E)
    frame = _deployment_enter(memory, frame, map_return)
    frame = _battle_action_map_fields(memory, frame)
    frame = _deployment_leave(memory, frame, map_return)
    positions = memory.state.table(0xFFFFA150).cursor()
    frame = first_replace(frame, candidates=positions)
    actor = low16(frame.choice)
    frame = _first_word(frame, 'target_x', actor)
    frame = _first_shift_word(frame, 'target_x', actor, 2)
    coordinate_source = positions if first_side else frame.roster
    offset = u16(actor << 2)
    x_fixed = coordinate_source.word(offset)
    frame = _first_word(frame, 'target_y', x_fixed)
    frame = _first_right_word(frame, 'target_y', x_fixed, 7)
    y_fixed = coordinate_source.word(offset, 2)
    frame = _first_word(frame, 'unit', y_fixed)
    frame = _first_right_word(frame, 'unit', y_fixed, 7)
    frame, category = _deployment_terrain_lookup(memory, frame, x_fixed >> 7, y_fixed >> 7, terrain_return)
    accepted = False
    for kind in ((0, 4, 8) if first_side else (0, 4, 7)):
        frame = _deployment_compare_byte(memory, frame, category, kind)
        if category == kind:
            accepted = True
            break
    frame = _deployment_carry(memory, frame, accepted if first_side else not accepted)
    return _action_child_publish(memory, frame)


def test_actor_types_0_4_8_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2648A uses actual A1 position coordinates;0/4/8 explicitly sets carry."""
    return test_actor_action_terrain_gate_fields(memory, frame, True)
