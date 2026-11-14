"""Battlefield geometry, live contact selection and original retreat policy.

The domain layer owns fixed-width arithmetic and named data ports. This file
expresses decisions in game terms. It neither decodes instructions nor embeds
ROM bytes, artwork, audio, or an assembler listing. Original oddities stay in
place; the single project bug ledger tracks changes considered for later.
"""
from .domain import (
    GameState, Word, Long, Table, CarryOutcome, uint, u16, u32,
    low8, low16, replace_word, replace_byte, negative_word, negative_byte,
    checked_state, checked_table, divu_retained,
)
from .contexts_geometry import (
    TargetCoordinate, ContactStrength, ContactCollection, RadialSeed,
    TrainingInputs, WeightedContact, ContactSearch, RadialStep,
)
from .contexts_radial import (
    SceneState, RadialTable, RadialMemory, RadialSeedFields, RadialDistanceFields,
    checked_scene_state, checked_radial_table,
)

from .contexts_policy_memory import BattlePolicyMemory, PolicyTable, checked_policy_table
from .contexts_deployment_terrain import DeploymentTerrainFields
from .contexts_first_deployment import (FirstDeploymentFrame, FirstTrainingFields,
    FirstDeploymentArithmeticBoundary, FirstDeploymentReturnBoundary, first_replace)
from .contexts_geometry import LeaderRosterPresenceFields
from .contexts_geometry import ContactCollectionFields
from .domain import Boundary


def read_training_inputs(state: GameState, unit: Word) -> TrainingInputs:
    checked_state(state)
    return read_training_inputs_fields(BattlePolicyMemory(state), unit)


def packed_training_strength(inputs: TrainingInputs) -> Long:
    if type(inputs) is not TrainingInputs:
        raise ValueError('typed live training inputs required')
    return divu_retained(inputs.training * inputs.rating, 100)


def weighted_training_factor(state: GameState, unit: Word) -> Long:
    checked_state(state)
    return weighted_training_factor_fields(BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), unit).factor


def battlefield_map_offset(scene: Word) -> Long:
    uint(scene, 16)
    return scene * 0x8C0


def load_battlefield_map_context(state: GameState) -> Table:
    """Legacy A0 projection of the same live map reader; D4/SP unobserved."""
    checked_state(state)
    return load_battlefield_map_fields(BattlePolicyMemory(state))


def load_battlefield_map_fields(memory: BattlePolicyMemory) -> PolicyTable:
    """Read the scene once, then select its 0x8c0-byte terrain map."""
    if type(memory) is not BattlePolicyMemory:
        raise ValueError('typed live battlefield-map memory required')
    scene = memory.battle_scene()
    return memory.battlefield_maps.advance(battlefield_map_offset(scene))


def battlefield_cell_offset(x: Word, y: Word) -> Word:
    uint(x, 16)
    uint(y, 16)
    return u16(((x >> 3) * 40 + (y >> 3)) * 2)


def read_battlefield_terrain_type(state: GameState, map_context: Table, x: Word, y: Word, retained: Long = 0) -> Long:
    """Legacy LONG projection of the sole tile/category lookup algorithm."""
    checked_state(state)
    checked_table(map_context, state)
    uint(retained, 32)
    return read_battlefield_terrain_type_fields(BattlePolicyMemory(state),
        map_context, x, y, retained).carrier


def constrain_transposed_target_coordinate(state: GameState, actor: Word, x: Word, y: Word) -> TargetCoordinate:
    """Expose named x/y; this original caller returns them in different slots."""
    checked_state(state)
    uint(actor, 16)
    uint(x, 16)
    uint(y, 16)
    return constrain_target_near_battlefield_anchor(state, actor, x, y)


def compare_actor_to_weakest_contact_strength(state: GameState, actor: Word) -> CarryOutcome:
    checked_state(state)
    uint(actor, 16)
    collect_contacts_in_speed_radius(state, actor)
    if negative_word(state.action_candidates.word()):
        return state.carry_result(0)
    weakest = select_weakest_contact_strength(state)
    training = weighted_training_factor(state, actor)
    troops = weakest.troops.long(u16(actor * 4))
    own_strength = low16(troops) * low16(training)
    return state.carry_result(int(weakest_contact_is_outmatched(weakest.strength, own_strength)))


def weakest_contact_is_outmatched(weakest: Long, own: Long) -> bool:
    uint(weakest, 32)
    uint(own, 32)
    return weakest <= own


def read_contact_weighted_strength(state: GameState, troops: Table, member: Word) -> WeightedContact:
    checked_state(state)
    checked_table(troops, state)
    uint(member, 16)
    weighting = weighted_training_factor(state, member)
    offset = u16(member * 4)
    strength = low16(troops.long(offset)) * low16(weighting)
    return WeightedContact(strength, offset, weighting)


def is_weaker_contact(strength: Long, weakest: Long) -> bool:
    uint(strength, 32)
    uint(weakest, 32)
    return strength < weakest


def select_weakest_contact_strength(state: GameState, retained_member: Word = 0, retained_weighting: Long = 0) -> ContactStrength:
    """Legacy projection of the sole live22C4C weighted-contact scan."""
    checked_state(state)
    uint(retained_member, 16)
    uint(retained_weighting, 32)
    frame, strength, member, weighting = select_weakest_contact_strength_fields(
        BattlePolicyMemory(state), FirstDeploymentFrame.unobserved(), retained_member, retained_weighting)
    return ContactStrength(strength, member, weighting, frame.roster,
        state.table(frame.candidates.base))


def constrain_pursuit_target_coordinate(state: GameState, actor: Word, x: Word, y: Word) -> TargetCoordinate:
    checked_state(state)
    uint(actor, 16)
    uint(x, 16)
    uint(y, 16)
    return constrain_target_near_battlefield_anchor(state, actor, x, y)


def test_other_side_total_shortfall(state: GameState) -> CarryOutcome:
    """Compatibility result from the sole original full-field threshold rule."""
    checked_state(state)
    frame, selected = test_other_side_total_shortfall_fields(
        BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return state.carry_result(int(selected))


def mark_eligible_actor_for_retreat(state: GameState, actor: Word) -> CarryOutcome:
    """Original low-strength/terrain/contact/random retreat policy, without fixes."""
    checked_state(state)
    uint(actor, 16)
    _, eligible = mark_eligible_actor_for_retreat_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved(), actor)
    return state.carry_result(int(eligible))


def retreat_troops_are_eligible(troops: Long) -> bool:
    uint(troops, 32)
    return troops <= 5000


def retreat_roster_is_sufficient(prefix_bytes: Word) -> bool:
    uint(prefix_bytes, 16)
    return prefix_bytes >= 4


def retreat_random_gate(sample: Long) -> bool:
    uint(sample, 32)
    return not bool(sample & 0x8000)


def commit_actor_retreat(state: GameState, actor: Word, eligible: bool) -> CarryOutcome:
    checked_state(state)
    uint(actor, 16)
    if type(eligible) is not bool:
        raise ValueError('strict retreat decision required')
    _commit_actor_retreat_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved(), actor, eligible)
    return state.carry_result(int(eligible))


def test_actor_terrain_types_3_or_7(state: GameState, actor: Word) -> CarryOutcome:
    checked_state(state)
    uint(actor, 16)
    _, eligible = test_actor_terrain_types_3_or_7_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved(), actor)
    return state.carry_result(int(eligible))


def terrain_is_retreat_compatible(terrain: Word) -> bool:
    uint(terrain, 16)
    return terrain == 3 or terrain == 7


def count_roster_nonnegative_prefix_bytes(state: GameState) -> Word:
    """Compatibility: the original counts BYTES of a WORD roster, not members."""
    checked_state(state)
    _, count = count_roster_nonnegative_prefix_bytes_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved())
    return count


def constrain_second_pursuit_target_coordinate(state: GameState, actor: Word, x: Word, y: Word) -> TargetCoordinate:
    checked_state(state)
    uint(actor, 16)
    uint(x, 16)
    uint(y, 16)
    return constrain_target_near_battlefield_anchor(state, actor, x, y)


def test_other_roster_single_member(state: GameState) -> CarryOutcome:
    checked_state(state)
    frame, selected = test_other_roster_single_member_fields(
        BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return state.carry_result(int(selected))


def constrain_target_near_battlefield_anchor(state: GameState, actor: Word, x: Word, y: Word) -> TargetCoordinate:
    checked_state(state)
    uint(actor, 16)
    uint(x, 16)
    uint(y, 16)
    return constrain_target_near_battlefield_anchor_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved(), actor, x, y)[1]


def select_nearest_contact_to_battlefield_center(state: GameState, retained_member: Word=0) -> Word:
    checked_state(state)
    uint(retained_member, 16)
    return select_nearest_contact_to_battlefield_center_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved(), retained_member)[1]


def is_nearer_contact(distance: Word, closest: Word) -> bool:
    uint(distance, 16)
    uint(closest, 16)
    return distance < closest


def wrapped_axis_distance(coordinate: Word, origin: Word) -> Word:
    """Pure WORD projection of the existing sole SUB/BCC/NEG difference kernel."""
    uint(coordinate, 16)
    uint(origin, 16)
    return _contact_difference(FirstDeploymentFrame.unobserved(), coordinate, origin)[1]


def test_same_side_total_shortfall(state: GameState) -> CarryOutcome:
    checked_state(state)
    frame, selected = test_same_side_total_shortfall_fields(
        BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return state.carry_result(int(selected))


def collect_contacts_in_speed_radius(state: GameState, actor: Word) -> ContactCollection:
    """Legacy result projection of the sole live234D2 field selection loop."""
    checked_state(state)
    uint(actor, 16)
    fields = collect_contacts_in_speed_radius_fields(BattlePolicyMemory(state),
        FirstDeploymentFrame.unobserved(), actor)
    frame = fields.frame
    return ContactCollection(fields.radius, fields.x, fields.y,
        frame.roster, frame.controller, frame.candidates)


def _retreat_carry_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame,
        selected: bool) -> FirstDeploymentFrame:
    """Original privileged carry operations retain all other current flags."""
    if type(selected) is not bool:
        raise ValueError('actual retreat decision required')
    if frame.status is not None:
        memory.state.sr = (memory.state.sr & 65504) | frame.status
    if type(memory.state) is GameState:
        memory.state.carry_result(int(selected))
    else:
        memory.state.set_status_word((memory.state.sr & 65534) | int(selected))
    return first_replace(frame, status=None if frame.status is None else
        (frame.status & 30) | int(selected))


def _retreat_map_call_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """22DA6 calls sole1A438; actual22DAC and saved D4 slots belong here."""
    from .business_actions import _deployment_enter, _deployment_leave, _battle_action_map_fields
    frame = _deployment_enter(memory, frame, 0x22DAC)
    frame = _battle_action_map_fields(memory, frame)
    return _deployment_leave(memory, frame, 0x22DAC)


def test_actor_terrain_types_3_or_7_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, actor: Word | None = None) -> tuple:
    """22DA6: live actor coordinates and sole terrain lookup, no fixed answer."""
    from .business_actions import _deployment_terrain_lookup
    frame.validate(memory.state, type(memory.state) is not GameState)
    actor = low16(frame.choice) if actor is None else uint(actor, 16)
    frame = _retreat_map_call_fields(memory, frame)
    positions = memory.state.table(0xFFFFA150).cursor()
    offset = u16(actor << 2)
    frame = first_replace(frame, candidates=positions,
        target_x=_contact_retained_word(frame.target_x, offset))
    frame = _contact_status(frame, offset, 16, bool(actor & 0x4000),
        False, bool(actor & 0x4000))
    x = positions.word(offset)
    frame = first_replace(frame, target_y=_contact_retained_word(frame.target_y, x >> 7))
    frame = _contact_status(frame, x >> 7, 16, bool(x & 0x40), False, bool(x & 0x40))
    y = positions.word(offset, 2)
    frame = first_replace(frame, unit=_contact_retained_word(frame.unit, y >> 7))
    frame = _contact_status(frame, y >> 7, 16, bool(y & 0x40), False, bool(y & 0x40))
    frame, terrain = _deployment_terrain_lookup(memory, frame, x >> 7,
        y >> 7, continuation=0x22DC6)
    value = low8(terrain)
    difference = (value - 3) & 255
    frame = _contact_status(frame, difference, 8, value < 3,
        bool((value ^ 3) & (value ^ difference) & 128))
    eligible = value == 3
    if not eligible:
        difference = (value - 7) & 255
        frame = _contact_status(frame, difference, 8, value < 7,
            bool((value ^ 7) & (value ^ difference) & 128))
        eligible = value == 7
    return _retreat_carry_fields(memory, frame, eligible), eligible


def count_roster_nonnegative_prefix_bytes_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """22DE4 counts actual nonnegative BYTES, not WORD members (compatible)."""
    frame.validate(memory.state, type(memory.state) is not GameState)
    frame = first_replace(frame, roster=memory.state.table(0xFFFFA5A4).cursor())
    flag = memory.state.read(0xFFFFF6D7, 1)
    frame = first_replace(frame, status=None if frame.status is None else
        (frame.status & 27) | (0 if flag & 2 else 4))
    if not flag & 2:
        frame = first_replace(frame, roster=memory.state.table(0xFFFFA550).cursor())
    count = 0
    frame = first_replace(frame, target_x=_contact_retained_word(frame.target_x, 0))
    frame = _contact_status(frame, 0, 16)
    while True:
        value = frame.roster.byte()
        frame = first_replace(frame, roster=frame.roster.advance(1))
        frame = _contact_status(frame, value, 8)
        if negative_byte(value):
            return frame, count
        previous = count
        count = u16(count + 1)
        frame = first_replace(frame, target_x=_contact_retained_word(frame.target_x, count))
        frame = _contact_status(frame, count, 16, previous == 65535,
            previous == 32767, previous == 65535)


def _retreat_child_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame,
        continuation: Long, algorithm, actor: Word | None = None) -> tuple:
    from .business_actions import _deployment_enter, _deployment_leave
    frame = _deployment_enter(memory, frame, continuation)
    if actor is None:
        frame, selected = algorithm(memory, frame)
    else:
        frame, selected = algorithm(memory, frame, actor)
    return _deployment_leave(memory, frame, continuation), selected


def mark_eligible_actor_for_retreat_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, actor: Word | None = None) -> tuple:
    """22D30: terrain, live strength, byte-roster, contacts and one random bit.

    An already marked actor skips RNG. Both success and failure retain the
    actual CLR read-before-write; the chosen actor is never silently changed.
    """
    from .business_actions import _deployment_enter, _deployment_leave
    frame.validate(memory.state, type(memory.state) is not GameState)
    actor = low16(frame.choice) if actor is None else uint(actor, 16)
    frame, eligible = _retreat_child_fields(memory, frame, 0x22D34,
        test_actor_terrain_types_3_or_7_fields, actor)
    if eligible:
        troops = memory.state.table(0xFFFFC800).cursor()
        offset = u16(actor << 2)
        frame = first_replace(frame, roster=troops,
            target_x=_contact_retained_word(frame.target_x, offset))
        frame = _contact_status(frame, offset, 16, bool(actor & 0x4000),
            False, bool(actor & 0x4000))
        strength = troops.long(offset)
        difference = u32(strength - 5000)
        frame = _contact_status(frame, difference, 32, strength < 5000,
            bool((strength ^ 5000) & (strength ^ difference) & 0x80000000))
        eligible = retreat_troops_are_eligible(strength)
    if eligible:
        frame, count = _retreat_child_fields(memory, frame, 0x22D50,
            count_roster_nonnegative_prefix_bytes_fields)
        difference = u16(count - 4)
        frame = _contact_status(frame, difference, 16, count < 4,
            bool((count ^ 4) & (count ^ difference) & 32768))
        eligible = retreat_roster_is_sufficient(count)
    if eligible:
        frame = _deployment_enter(memory, frame, 0x22D5C)
        frame = collect_contacts_in_speed_radius_fields(memory, frame, actor).frame
        frame = _deployment_leave(memory, frame, 0x22D5C)
        selected = memory.state.read(0xFFFFD300, 2)
        frame = _contact_status(frame, selected, 16)
        eligible = not negative_word(selected)
    if eligible:
        flags = memory.state.table(0xFF3BC2).cursor()
        frame = first_replace(frame, roster=flags)
        marked = flags.byte(actor)
        frame = _contact_status(frame, marked, 8)
        if marked == 0:
            frame = _deployment_enter(memory, frame, 0x22D78)
            from .business_formation import first_deployment_random_fields
            frame = first_deployment_random_fields(memory, frame)
            frame = _deployment_leave(memory, frame, 0x22D78)
            eligible = retreat_random_gate(frame.target_x)
            frame = first_replace(frame, status=(frame.status & 27) |
                (4 if eligible else 0))
    return _commit_actor_retreat_fields(memory, frame, actor, eligible), eligible


def _commit_actor_retreat_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, actor: Word, eligible: bool) -> FirstDeploymentFrame:
    """22D80/22D96 shared actual flag write and CLR read-before-write."""
    uint(actor, 16)
    if type(eligible) is not bool:
        raise ValueError('actual eligibility required')
    frame = first_replace(frame, roster=memory.state.table(0xFF3BC2).cursor())
    if eligible:
        frame.roster.set_byte(actor, 1)
        frame = _contact_status(frame, 1, 8)
        frame = first_replace(frame, roster=memory.state.table(0xFFFFAE28).cursor())
    frame.roster.byte(actor)
    frame.roster.set_byte(actor, 0)
    frame = _contact_status(frame, 0, 8)
    return _retreat_carry_fields(memory, frame, eligible)


def read_contact_search(state: GameState, actor: Word) -> ContactSearch:
    checked_state(state)
    uint(actor, 16)
    radius = u16(state.officer_march_speed.byte(actor) * 10)
    output = state.action_candidates.cursor()
    positions = state.battle_positions
    own_offset = u16(actor * 4)
    own_x = positions.word(own_offset)
    own_y = positions.word(own_offset, 2)
    roster = state.primary_battle_roster if state.scalar('battle_side_flags') & 2 else state.secondary_battle_roster
    candidates = roster.cursor()
    return ContactSearch(radius, TargetCoordinate(own_x, own_y), output, candidates, positions)


def read_vertical_contact_distance(state: GameState, positions: Table, member: Word, origin: Word) -> Word:
    checked_state(state)
    checked_table(positions, state)
    uint(member, 16)
    uint(origin, 16)
    return wrapped_axis_distance(positions.word(u16(member * 4), 2), origin) >> 7


def read_horizontal_contact_distance(state: GameState, positions: Table, member: Word, origin: Word) -> Word:
    checked_state(state)
    checked_table(positions, state)
    uint(member, 16)
    uint(origin, 16)
    return wrapped_axis_distance(positions.word(u16(member * 4)), origin) >> 7


def axis_outside_contact_radius(distance: Word, radius: Word) -> bool:
    uint(distance, 16)
    uint(radius, 16)
    return distance > radius


def radial_contact_is_in_range(distance: Word, radius: Word) -> bool:
    uint(distance, 16)
    uint(radius, 16)
    return distance <= radius


def squared_contact_distance(y_distance: Word, x_distance: Word) -> Long:
    uint(y_distance, 16)
    uint(x_distance, 16)
    return u32(y_distance * y_distance + x_distance * x_distance)


def test_battlefield_leader_roster_presence(state: GameState) -> CarryOutcome:
    """Historical carry projection of the one live leader-roster transaction."""
    checked_state(state)
    fields = test_battlefield_leader_roster_presence_fields(
        BattlePolicyMemory(state), FirstDeploymentFrame.unobserved())
    return state.carry_result(int(not fields.present))


def rounded_radial_distance(state: GameState, squared_distance: Long) -> Long:
    """Legacy GameState projection of the one full radial transaction."""
    checked_state(state)
    return _rounded_radial_fields(RadialMemory(state), squared_distance).value


def _rounded_radial_fields(memory: RadialMemory, squared_distance: Long) -> RadialDistanceFields:
    """Original table seed and WORD odd-increment loop; full D0 is retained."""
    if type(memory) is not RadialMemory:
        raise ValueError('closed radial memory required')
    uint(squared_distance, 32)
    if squared_distance == 0:
        return RadialDistanceFields(0, False, True, False, False)
    memory.enter_seed()
    seed = _seed_radial_fields(memory, squared_distance)
    memory.leave_seed()
    remaining, count, increment = seed.remaining, seed.count, seed.increment
    while True:
        step = subtract_radial_increment(remaining, increment)
        remaining = step.remaining
        if step.crossed:
            return RadialDistanceFields(replace_word(remaining, low16(count)), False, low16(count) == 0, bool(low16(count) & 32768), False)
        count = replace_word(count, u16(count + 1))
        increment = replace_word(increment, u16(increment + 2))


def subtract_radial_increment(remaining: Long, increment: Long) -> RadialStep:
    uint(remaining, 32)
    uint(increment, 32)
    return RadialStep(u32(remaining - increment), remaining < increment)


def seed_radial_distance_from_thresholds(state: GameState, squared_distance: Long, retained_count: Long = 0, retained_threshold: Long = 0) -> RadialSeed:
    """Legacy seed projection; direct zero still follows the original table read."""
    checked_state(state)
    fields = _seed_radial_fields(RadialMemory(state), squared_distance, retained_count, retained_threshold)
    return RadialSeed(fields.remaining, fields.count, fields.increment, fields.last_threshold, fields.threshold_cursor)


def _seed_radial_fields(memory: RadialMemory, squared_distance: Long, retained_count: Long = 0, retained_threshold: Long = 0) -> RadialSeedFields:
    if type(memory) is not RadialMemory:
        raise ValueError('closed radial memory required')
    uint(squared_distance, 32)
    uint(retained_count, 32)
    uint(retained_threshold, 32)
    if squared_distance >= 0x2358D:
        return RadialSeedFields(u32(squared_distance - 0x2358D), replace_word(retained_count, 0x17D), 0x2FA, retained_threshold, None)
    thresholds = memory.thresholds
    while squared_distance >= thresholds.long():
        thresholds = thresholds.advance(6)
    preceding_threshold = thresholds.long(0, -6)
    increment = thresholds.word(0, -2)
    return _radial_previous_fields(squared_distance, retained_count, increment, preceding_threshold, thresholds)


def radial_seed_from_previous_threshold(squared_distance: Long, retained_count: Long, increment: Word, previous: Long, cursor: Table) -> RadialSeed:
    """Legacy Table/result projection of the shared seed field calculation."""
    checked_table(cursor)
    fields = _radial_previous_fields(squared_distance, retained_count, increment, previous, cursor)
    return RadialSeed(fields.remaining, fields.count, fields.increment, fields.last_threshold, fields.threshold_cursor)


def _radial_previous_fields(squared_distance: Long, retained_count: Long, increment: Word, previous: Long, cursor: RadialTable) -> RadialSeedFields:
    uint(squared_distance, 32)
    uint(retained_count, 32)
    uint(increment, 16)
    uint(previous, 32)
    checked_radial_table(cursor)
    remaining = u32(squared_distance - previous)
    count = replace_word(retained_count, increment >> 1)
    return RadialSeedFields(remaining, count, increment, previous, cursor)


def rounded_scene_radial_distance(state: SceneState, squared_distance: Long) -> RadialDistanceFields:
    """City entry uses its original live State, with no RAM copying or reread."""
    checked_scene_state(state)
    return _rounded_radial_fields(RadialMemory(state), squared_distance)


def read_battlefield_terrain_type_fields(memory: BattlePolicyMemory, map_context: PolicyTable, x: Word, y: Word, retained: Long | None) -> DeploymentTerrainFields:
    """1A44E's map WORD and category BYTE; no fabricated retained high WORD."""
    if type(memory) is not BattlePolicyMemory:
        raise ValueError('sealed battlefield memory required')
    checked_policy_table(map_context, memory.state)
    uint(x, 16)
    uint(y, 16)
    if retained is not None:
        uint(retained, 32)
    before_shift = u16(u16((x >> 3) * 40) + (y >> 3))
    offset = battlefield_cell_offset(x, y)
    tile = map_context.word(offset) & 1023
    lookup = memory.state.table(0x6C0B4)
    category = lookup.byte(tile)
    word = (tile & 65280) | category
    carrier = None if retained is None else replace_word(retained, word)
    return DeploymentTerrainFields(carrier, word, category, lookup,
        before_shift & 32768 != 0).validate(memory.state)


def test_battlefield_leader_roster_presence_fields(
        memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> LeaderRosterPresenceFields:
    """235CC: live city head, sentinel roster and real D0/D1/A0 save/readback.

    Legacy carry-only calls leave their unobserved carriers explicit. Complete
    callers supply the actual callee-entry SP and current A0, not a snapshot.
    The city high BYTE retained by MOVE.B is part of the original comparison.
    """
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('sealed memory and actual leader-roster frame required')
    frame.validate(memory.state, type(memory.state) is not GameState or frame.stack_cursor is not None)
    stack = frame.stack_cursor
    if stack is not None:
        checked_policy_table(frame.roster, memory.state)
        stack = stack.advance(-4)
        stack.set_long(0, frame.roster.base)
        stack = stack.advance(-4)
        stack.set_long(0, frame.target_y)
        stack = stack.advance(-4)
        stack.set_long(0, frame.target_x)
        frame = first_replace(frame, stack_cursor=stack)
    head = memory.state.table(0xFFFFA027)
    scene = memory.battle_scene()
    leader = (scene & 0xFF00) | head.byte(scene)
    roster = memory.state.table(0xFFFFA550).cursor()
    while True:
        member = roster.next_word()
        if negative_word(member):
            present = False
            break
        if member == leader:
            present = True
            break
    if stack is not None:
        restored_x = stack.long()
        stack = stack.advance(4)
        restored_y = stack.long()
        stack = stack.advance(4)
        restored_roster = memory.state.table(stack.long()).cursor()
        stack = stack.advance(4)
        frame = first_replace(frame, target_x=restored_x, target_y=restored_y,
            roster=restored_roster, stack_cursor=stack)
    if not present:
        memory.state.write(0xFFFFF612, 2, 0x411)
        memory.state.read(0xFFFFF362, 2)
        memory.state.write(0xFFFFF362, 2, 0)
        memory.state.write(0xFFFFF6D6, 2, 2)
    if not memory.state.sr & 8192:
        raise Boundary('original leader-roster full-SR operation requires supervisor')
    if memory.state.sr & 32768:
        raise Boundary('leader-roster trace continuation is not modeled')
    status = None if frame.status is None else (frame.status & 16) | (4 if present else 1)
    return LeaderRosterPresenceFields(first_replace(frame, status=status), present).validate(memory.state)


def read_training_inputs_fields(memory: BattlePolicyMemory, unit: Word) -> TrainingInputs:
    if type(memory) is not BattlePolicyMemory:
        raise ValueError('one sealed same-state memory required')
    uint(unit, 16)
    training = memory.state.table(0xFFFFC500).byte(unit)
    rating = memory.state.table(0xFFFFB400).word(u16(unit << 1))
    return TrainingInputs(training, rating)


def weighted_training_factor_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, unit: Word) -> FirstTrainingFields:
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('closed training memory and current fields required')
    uint(unit, 16)
    complete = type(memory.state) is not GameState
    frame.validate(memory.state, complete)
    saved_unit, saved_source = frame.target_x, frame.roster
    stack = frame.stack_cursor
    if stack is not None:
        if saved_unit is None or saved_source is None:
            raise ValueError('actual MOVEM D0/A0 inputs required before any save')
        if low16(saved_unit) != unit:
            raise ValueError('training unit must be the actual current D0 WORD')
        checked_policy_table(saved_source, memory.state)
        stack = stack.advance(-4)
        stack.set_long(0, saved_source.base)
        stack = stack.advance(-4)
        stack.set_long(0, saved_unit)
    inputs = read_training_inputs_fields(memory, unit)
    factor = packed_training_strength(inputs)
    # This literal is the same finite role as packed_training_strength's
    # divisor; compiler admission requires the supplied source uses to agree.
    divisor = 100
    quotient = inputs.training * inputs.rating // divisor
    overflow = quotient > 65535
    if overflow and complete:
        # MC68000 overflow does not supply defined N/Z; a full CCR cannot be
        # invented. Keep its real target/state rather than a fabricated result.
        current = first_replace(frame, target_x=replace_word(frame.target_x, u16(unit << 1)),
            target_y=inputs.training * inputs.rating, roster=memory.state.table(0xFFFFB400).cursor(),
            stack_cursor=stack, status=None)
        raise FirstDeploymentArithmeticBoundary(0xBAE0, current, factor)
    status = None if overflow else ((16 if unit & 32768 else 0) | (8 if quotient & 32768 else 0) | (4 if quotient == 0 else 0))
    restored_unit = unit
    if stack is not None:
        saved_unit = stack.long()
        stack = stack.advance(4)
        saved_source = memory.state.table(stack.long()).cursor()
        stack = stack.advance(4)
        restored_unit = low16(saved_unit)
    returned = first_replace(frame, target_x=saved_unit, target_y=factor,
        roster=saved_source, stack_cursor=stack, status=status)
    return FirstTrainingFields(returned, factor, restored_unit)

def rounded_deployment_radial_distance_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3080E sole radial logic plus actual D1-D3/A0 MOVEM save/readback.

    Full callers supply observed callee-entry A7. Legacy no-stack projections
    preserve None; no fake stack or high half is created. Actual saved words
    are read back from the same live state, not a retained host snapshot.
    """
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('same-state radial memory and actual frame required')
    frame.validate(memory.state, frame.stack_cursor is not None)
    uint(frame.target_x, 32)
    original = frame.target_x
    stack = frame.stack_cursor
    if stack is not None:
        checked_policy_table(frame.roster, memory.state)
        # MOVEM predecrement uses descending register order: A0,D3,D2,D1.
        for saved in (frame.roster.base, frame.count, frame.unit, frame.target_y):
            uint(saved, 32)
            stack = stack.advance(-4)
            stack.set_long(0, saved)
    radial = RadialMemory(memory.state, stack)
    result = _rounded_radial_fields(radial, original)
    stack = radial.stack_cursor
    returned = first_replace(frame, target_x=result.value)
    if stack is not None:
        restored_y = stack.long()
        stack = stack.advance(4)
        restored_unit = stack.long()
        stack = stack.advance(4)
        restored_count = stack.long()
        stack = stack.advance(4)
        restored_roster = memory.state.table(stack.long()).cursor()
        stack = stack.advance(4)
        returned = first_replace(returned, target_y=restored_y, unit=restored_unit,
            count=restored_count, roster=restored_roster, stack_cursor=stack)
    # TST.L0 leaves X untouched; a nonzero loop always ends with SUB.L borrow,
    # so its actual X=1 survives the final MOVE.W and MOVEM/RTS.
    extend = (None if frame.status is None else frame.status & 16) if original == 0 else 16
    status = None if extend is None else extend | int(result.carry) | (2 if result.overflow else 0) | (4 if result.zero else 0) | (8 if result.negative else 0)
    return first_replace(returned, status=status).validate(memory.state, frame.stack_cursor is not None)


def _contact_retained_word(carrier: Long | None, value: Word) -> Long | None:
    """A WORD overwrite does not invent an unobserved legacy upper WORD."""
    uint(value, 16)
    if carrier is None:
        return None
    uint(carrier, 32)
    return replace_word(carrier, value)


def _contact_status(frame: FirstDeploymentFrame, value: Long, width: int,
        carry: bool = False, overflow: bool = False,
        extend: bool | None = None) -> FirstDeploymentFrame:
    """Named contact arithmetic flags; None retains only an observed X."""
    if width not in (8, 16, 32):
        raise ValueError('original contact BYTE/WORD/LONG flag width required')
    uint(value, width)
    if type(carry) is not bool or type(overflow) is not bool:
        raise ValueError('actual arithmetic carry and overflow required')
    if extend is not None and type(extend) is not bool:
        raise ValueError('extend must be observed or explicitly unobserved')
    flags = int(carry) | (2 if overflow else 0) | (4 if value == 0 else 0) | (8 if value & (1 << (width - 1)) else 0)
    if extend is None:
        status = None if frame.status is None else (frame.status & 16) | flags
    else:
        status = (16 if extend else 0) | flags
    return first_replace(frame, status=status)


def _contact_difference(frame: FirstDeploymentFrame, coordinate: Word, origin: Word) -> tuple:
    """Unsigned WORD SUB/BCC/NEG order, including the original 0x8000 case."""
    uint(coordinate, 16)
    uint(origin, 16)
    difference = u16(coordinate - origin)
    borrowed = coordinate < origin
    frame = _contact_status(frame, difference, 16, borrowed,
        bool((coordinate ^ origin) & (coordinate ^ difference) & 0x8000), borrowed)
    if borrowed:
        before = difference
        difference = u16(-before)
        frame = _contact_status(frame, difference, 16, before != 0,
            before == 0x8000, before != 0)
    return frame, difference


def _contact_radial_call(memory: BattlePolicyMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2354E owns only its real23554 slot; the sole radial core owns its saves."""
    complete = type(memory.state) is not GameState or frame.stack_cursor is not None
    if frame.stack_cursor is not None:
        stack = frame.stack_cursor.advance(-4)
        stack.set_long(0, 0x23554)
        frame = first_replace(frame, stack_cursor=stack)
    if frame.status is not None:
        memory.state.sr = (memory.state.sr & 65504) | frame.status
    returned = rounded_deployment_radial_distance_fields(memory, frame)
    if type(returned) is not FirstDeploymentFrame:
        raise Boundary('sole radial core must return the actual current frame')
    returned.validate(memory.state, complete)
    if returned.stack_cursor is not None:
        stack = returned.stack_cursor
        actual = stack.long()
        if actual != 0x23554:
            raise FirstDeploymentReturnBoundary(actual, returned, 0x23554)
        returned = first_replace(returned, stack_cursor=stack.advance(4))
    return returned.validate(memory.state, complete)


def collect_contacts_in_speed_radius_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, actor: Word | None = None) -> ContactCollectionFields:
    """Sole234D2 selection: live opposing roster, WORD radius and current fields.

    A legacy actor is a separately observed WORD, never a fabricated D7 LONG.
    Full calls use their real current D7 and keep all untouched D/A carriers.
    """
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('same existing policy memory and sole current frame required')
    state = memory.state
    complete = type(state) is not GameState or frame.stack_cursor is not None
    frame.validate(state, complete)
    if actor is None:
        uint(frame.choice, 32)
        actor = low16(frame.choice)
    else:
        uint(actor, 16)
        if frame.choice is not None and low16(frame.choice) != actor:
            raise ValueError('legacy actor must agree with an observed current D7 WORD')
    speed_table = state.table(0xFFFFC400).cursor()
    frame = first_replace(frame, roster=speed_table,
        count=_contact_retained_word(frame.count, 0))
    frame = _contact_status(frame, 0, 16)
    speed = speed_table.byte(actor)
    frame = first_replace(frame, count=_contact_retained_word(frame.count, speed))
    frame = _contact_status(frame, speed, 8)
    frame = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, speed))
    frame = _contact_status(frame, speed, 16)
    radius = u16(speed << 2)
    frame = first_replace(frame, count=_contact_retained_word(frame.count, radius))
    frame = _contact_status(frame, radius, 16, bool(speed & 0x4000), False, bool(speed & 0x4000))
    combined = radius + speed
    radius = u16(combined)
    frame = first_replace(frame, count=_contact_retained_word(frame.count, radius))
    frame = _contact_status(frame, radius, 16, combined > 65535,
        bool(~((speed << 2) ^ speed) & ((speed << 2) ^ radius) & 0x8000), combined > 65535)
    shifted = radius
    radius = u16(radius << 1)
    frame = first_replace(frame, count=_contact_retained_word(frame.count, radius))
    frame = _contact_status(frame, radius, 16, bool(shifted & 0x8000), False, bool(shifted & 0x8000))
    output = state.table(0xFFFFD300).cursor()
    positions = state.table(0xFFFFA150).cursor()
    frame = first_replace(frame, roster=output, candidates=positions,
        unit=_contact_retained_word(frame.unit, actor))
    frame = _contact_status(frame, actor, 16)
    actor_offset = u16(actor << 2)
    frame = first_replace(frame, unit=_contact_retained_word(frame.unit, actor_offset))
    frame = _contact_status(frame, actor_offset, 16, bool(actor & 0x4000), False, bool(actor & 0x4000))
    origin_x = positions.word(actor_offset)
    frame = first_replace(frame, target_y=_contact_retained_word(frame.target_y, origin_x))
    frame = _contact_status(frame, origin_x, 16)
    origin_y = positions.word(actor_offset, 2)
    frame = first_replace(frame, unit=_contact_retained_word(frame.unit, origin_y))
    frame = _contact_status(frame, origin_y, 16)
    retreat_flags = state.table(0xFF3BC2).cursor()
    frame = first_replace(frame, opponent=retreat_flags)
    other_side = bool(state.read(0xFFFFF6D7, 1) & 2)
    frame = first_replace(frame, status=None if frame.status is None else
        (frame.status & 27) | (0 if other_side else 4))
    frame = first_replace(frame, controller=state.table(0xFFFFA550 if other_side else 0xFFFFA5A4).cursor())
    while True:
        source = frame.controller
        member = source.word()
        frame = first_replace(frame, controller=source.advance(2),
            distance=_contact_retained_word(frame.distance, member))
        frame = _contact_status(frame, member, 16)
        if negative_word(member):
            frame.roster.set_word(0, 0xFFFF)
            frame = _contact_status(frame, 0xFFFF, 16)
            if frame.status is not None:
                state.sr = (state.sr & 65504) | frame.status
            return ContactCollectionFields(frame, radius, origin_x, origin_y).validate(state, complete)
        marked = frame.opponent.byte(member)
        frame = _contact_status(frame, marked, 8)
        if marked != 0:
            continue
        frame = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, member))
        frame = _contact_status(frame, member, 16)
        position_offset = u16(member << 2)
        frame = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, position_offset))
        frame = _contact_status(frame, position_offset, 16, bool(member & 0x4000), False, bool(member & 0x4000))
        candidate_y = frame.candidates.word(position_offset, 2)
        frame = first_replace(frame, target_x=_contact_retained_word(frame.target_x, candidate_y))
        frame = _contact_status(frame, candidate_y, 16)
        live_y = origin_y if frame.unit is None else low16(frame.unit)
        frame, vertical = _contact_difference(frame, candidate_y, live_y)
        frame = first_replace(frame, target_x=_contact_retained_word(frame.target_x, vertical))
        distance_y = vertical >> 7
        frame = first_replace(frame, target_x=_contact_retained_word(frame.target_x, distance_y))
        frame = _contact_status(frame, distance_y, 16, bool(vertical & 0x40), False, bool(vertical & 0x40))
        live_radius = radius if frame.count is None else low16(frame.count)
        compared = u16(distance_y - live_radius)
        frame = _contact_status(frame, compared, 16, distance_y < live_radius,
            bool((distance_y ^ live_radius) & (distance_y ^ compared) & 0x8000))
        if axis_outside_contact_radius(distance_y, live_radius):
            continue
        frame = first_replace(frame, target_x=distance_y * distance_y)
        frame = _contact_status(frame, frame.target_x, 32)
        candidate_x = frame.candidates.word(position_offset)
        frame = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, candidate_x))
        frame = _contact_status(frame, candidate_x, 16)
        live_x = origin_x if frame.target_y is None else low16(frame.target_y)
        frame, horizontal = _contact_difference(frame, candidate_x, live_x)
        frame = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, horizontal))
        distance_x = horizontal >> 7
        frame = first_replace(frame, offset_x=_contact_retained_word(frame.offset_x, distance_x))
        frame = _contact_status(frame, distance_x, 16, bool(horizontal & 0x40), False, bool(horizontal & 0x40))
        compared = u16(distance_x - live_radius)
        frame = _contact_status(frame, compared, 16, distance_x < live_radius,
            bool((distance_x ^ live_radius) & (distance_x ^ compared) & 0x8000))
        if axis_outside_contact_radius(distance_x, live_radius):
            continue
        frame = first_replace(frame, offset_x=distance_x * distance_x)
        frame = _contact_status(frame, frame.offset_x, 32)
        before = frame.target_x
        total = before + frame.offset_x
        squared = squared_contact_distance(distance_y, distance_x)
        frame = first_replace(frame, target_x=squared)
        frame = _contact_status(frame, squared, 32, total > 0xFFFFFFFF,
            bool(~(before ^ frame.offset_x) & (before ^ squared) & 0x80000000), total > 0xFFFFFFFF)
        frame = _contact_radial_call(memory, frame)
        distance = low16(frame.target_x)
        live_radius = radius if frame.count is None else low16(frame.count)
        compared = u16(distance - live_radius)
        frame = _contact_status(frame, compared, 16, distance < live_radius,
            bool((distance ^ live_radius) & (distance ^ compared) & 0x8000))
        if not radial_contact_is_in_range(distance, live_radius):
            continue
        member = member if frame.distance is None else low16(frame.distance)
        output = frame.roster
        output.set_word(0, member)
        frame = first_replace(frame, roster=output.advance(2))
        frame = _contact_status(frame, member, 16)


def _weakest_training_call_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame,
        member: Word) -> FirstDeploymentFrame:
    """The scan owns22C62; BAC8 owns its actual D0/A0 MOVEM slots."""
    if frame.stack_cursor is not None:
        stack = frame.stack_cursor.advance(-4)
        stack.set_long(0, 0x22C62)
        frame = first_replace(frame, stack_cursor=stack)
    returned = weighted_training_factor_fields(memory, frame, member).frame
    if returned.stack_cursor is not None:
        stack = returned.stack_cursor
        actual = stack.long()
        if actual != 0x22C62:
            raise FirstDeploymentReturnBoundary(actual, returned, 0x22C62)
        returned = first_replace(returned, stack_cursor=stack.advance(4))
    return returned


def select_weakest_contact_strength_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, retained_member: Word | None = None,
        retained_weighting: Long | None = None) -> tuple:
    """Unique sentinel scan, first minimum wins; D1 is last, not best, factor.

    confirmed:22C4C..22C78 listing. The same algorithm serves complete
    caller fields and the historical result-only API, without guessed highs.
    """
    from .business_formation import _first_word, _first_shift_word, _first_right_word
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('same-state contact memory and actual fields required')
    state = memory.state
    frame.validate(state, frame.stack_cursor is not None)
    if retained_member is None:
        uint(frame.count, 32)
        retained_member = low16(frame.count)
    if retained_weighting is None:
        uint(frame.target_y, 32)
        retained_weighting = frame.target_y
    uint(retained_member, 16)
    uint(retained_weighting, 32)
    frame = first_replace(frame, roster=state.table(0xFFFFD300).cursor(),
        candidates=state.table(0xFFFFC800).cursor(), unit=0xFFFFFFFF)
    frame = _contact_status(frame, 0xFFFFFFFF, 32)
    selected, last_weighting = retained_member, retained_weighting
    while True:
        source = frame.roster
        member = source.word()
        frame = first_replace(frame, roster=source.advance(2))
        frame = _first_word(frame, 'target_x', member)
        if negative_word(member):
            return frame, frame.unit, selected, last_weighting
        frame = _weakest_training_call_fields(memory, frame, member)
        last_weighting = frame.target_y
        live_member = member if frame.target_x is None else low16(frame.target_x)
        offset = u16(live_member << 2)
        frame = _first_shift_word(frame, 'target_x', live_member, 2)
        troops = frame.candidates.long(offset)
        frame = first_replace(frame, distance=troops)
        frame = _contact_status(frame, troops, 32)
        strength = low16(troops) * low16(frame.target_y)
        frame = first_replace(frame, distance=strength)
        frame = _contact_status(frame, strength, 32)
        difference = u32(strength - frame.unit)
        frame = _contact_status(frame, difference, 32, strength < frame.unit,
            bool((strength ^ frame.unit) & (strength ^ difference) & 0x80000000))
        if not is_weaker_contact(strength, frame.unit):
            continue
        frame = first_replace(frame, unit=strength)
        frame = _contact_status(frame, strength, 32)
        frame = _first_right_word(frame, 'target_x', offset, 2)
        selected = offset >> 2
        frame = _first_word(frame, 'count', selected)


def _weakest_comparison_call_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, target: Long,
        continuation: Long) -> FirstDeploymentFrame:
    """22C18's three actual children; each owns one physical CALL/RTS slot."""
    from .business_actions import _deployment_enter, _deployment_leave
    if (target, continuation) not in ((0x234D2, 0x22C1C),
            (0x22C4C, 0x22C28), (0xBAC8, 0x22C30)):
        raise ValueError('original weakest-contact child and continuation required')
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('same-state policy memory and complete current frame required')
    checked_scene_state(memory.state)
    frame.validate(memory.state, True)
    memory.state.sr = (memory.state.sr & 65504) | frame.status
    entered = _deployment_enter(memory, frame, continuation)
    if target == 0x234D2:
        returned = collect_contacts_in_speed_radius_fields(memory, entered).frame
    elif target == 0x22C4C:
        returned = select_weakest_contact_strength_fields(memory, entered)[0]
    else:
        returned = weighted_training_factor_fields(memory, entered,
            low16(entered.target_x)).frame
    returned.validate(memory.state, True)
    memory.state.sr = (memory.state.sr & 65504) | returned.status
    return _deployment_leave(memory, returned, continuation)


def compare_actor_to_weakest_contact_strength_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """22C18..22C4A: live contacts, own weighted strength and original CMP/CF.

    D7 is the actual actor carrier. No contact clears only C after TST.W;
    otherwise D2 is compared with the original MULU result, retaining NZVX.
    The caller keeps its outer slot; only the three encoded inner calls pop.
    """
    from .business_formation import _first_word, _first_shift_word, _first_compare_long
    if type(memory) is not BattlePolicyMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('same-state policy memory and complete current frame required')
    state = memory.state
    checked_scene_state(state)
    frame.validate(state, True)
    if (frame.roster is None or frame.candidates is None
            or frame.controller is None or frame.scan is None
            or frame.opponent is None or frame.scratch is None
            or frame.auxiliary is None):
        raise ValueError('weakest-contact comparison requires all actual address carriers')
    frame = _weakest_comparison_call_fields(memory, frame, 0x234D2, 0x22C1C)
    sentinel = state.read(0xFFFFD300, 2)
    frame = _contact_status(frame, sentinel, 16)
    if negative_word(sentinel):
        return _retreat_carry_fields(memory, frame, False)
    frame = _weakest_comparison_call_fields(memory, frame, 0x22C4C, 0x22C28)
    frame = _first_word(frame, 'target_x', low16(frame.choice))
    frame = _weakest_comparison_call_fields(memory, frame, 0xBAC8, 0x22C30)
    frame = _first_shift_word(frame, 'target_x', low16(frame.target_x), 2)
    state.sr = (state.sr & 65504) | frame.status
    troops = frame.candidates.long(low16(frame.target_x))
    frame = first_replace(frame, target_x=troops)
    frame = _contact_status(frame, troops, 32)
    own_strength = low16(frame.target_x) * low16(frame.target_y)
    frame = first_replace(frame, target_x=own_strength)
    frame = _contact_status(frame, own_strength, 32)
    frame = _first_compare_long(frame, frame.unit, frame.target_x)
    return _retreat_carry_fields(memory, frame, bool(frame.status & 5))


def _contact_strategy_actor_slot_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, size: int, save: bool,
        actor: Word=None) -> FirstDeploymentFrame:
    """Only the real D7 WORD/LONG saves and actual RAM restores in this family."""
    from .business_formation import _first_word, _first_long, _first_memory_word
    if size not in (2, 4) or type(save) is not bool:
        raise ValueError('actual contact-strategy actor save width required')
    if save:
        if size == 2:
            uint(actor, 16)
            frame = _first_memory_word(frame, actor)
            value = actor
        else:
            value = frame.choice
            frame = first_replace(frame, status=None) if value is None else _contact_status(frame, value, 32)
        if frame.stack_cursor is not None:
            stack = frame.stack_cursor.advance(-size)
            if size == 2:
                stack.set_word(0, value)
            else:
                stack.set_long(0, value)
            return first_replace(frame, stack_cursor=stack)
        if frame.choice is not None:
            raise Boundary('observed actor save requires its real current stack, not a host snapshot')
        return frame
    if frame.stack_cursor is not None:
        value = frame.stack_cursor.word() if size == 2 else frame.stack_cursor.long()
        frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(size))
        return _first_word(frame, 'choice', value) if size == 2 else _first_long(frame, 'choice', value)
    # Historical GameState APIs do not observe D7's upper half or physical SP.
    return _first_word(frame, 'choice', actor) if size == 2 else first_replace(frame, choice=None, status=None)


def _contact_strategy_axis_distance_fields(frame: FirstDeploymentFrame,
        carrier: str, coordinate: Word, origin: Word) -> tuple:
    """Observe real MOV.W/SUB/BCC/NEG through the sole contact difference math."""
    from .business_formation import _first_word
    if carrier not in ('choice', 'offset_x', 'offset_y'):
        raise ValueError('actual anchor/nearest axis carrier required')
    frame = _first_word(frame, carrier, coordinate)
    frame, value = _contact_difference(frame, coordinate, origin)
    return first_replace(frame, **{carrier:_contact_retained_word(frame.carrier(carrier), value)}), value


def test_other_roster_single_member_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """23046 tests only the real opposite roster's second WORD, not its first."""
    from .business_formation import _first_frame, _first_memory_word
    from ..high_level_gameplay_flow.business_battle import _postbattle_bit_fields
    frame = _first_frame(memory, frame)
    side = memory.state.read(0xFFFFF6D7, 1)
    frame = _postbattle_bit_fields(frame, bool(side & 2))
    roster = memory.state.table(0xFFFFA550 if side & 2 else 0xFFFFA5A4).cursor()
    frame = first_replace(frame, roster=roster)
    word = roster.word(0, 2)
    frame = _first_memory_word(frame, word)
    selected = negative_word(word)
    return _retreat_carry_fields(memory, frame, selected), selected


def test_other_side_total_shortfall_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """22CFE: other-side live LONG total and the original F76C limit."""
    from .business_formation import _first_frame, _first_long, _first_compare_long
    from ..high_level_gameplay_flow.business_battle import _postbattle_bit_fields
    frame = _first_frame(memory, frame)
    first = memory.state.table(0xFFFFF69E).cursor()
    second = memory.state.table(0xFFFFF6A2).cursor()
    frame = first_replace(frame, roster=first, candidates=second)
    side = memory.state.read(0xFFFFF6D7, 1)
    frame = _postbattle_bit_fields(frame, bool(side & 2))
    if side & 2:
        first, second = second, first
        frame = first_replace(frame, roster=first, candidates=second)
    strength = second.long()
    frame = _first_long(frame, 'target_x', strength)
    opposite = first.long()
    frame = _first_compare_long(frame, strength, opposite)
    selected = False
    if strength < opposite:
        limit = memory.state.read(0xFFFFF76C, 4)
        frame = _first_compare_long(frame, strength, limit)
        selected = strength < limit
    return _retreat_carry_fields(memory, frame, selected), selected


def constrain_target_near_battlefield_anchor_fields(memory: BattlePolicyMemory, frame: FirstDeploymentFrame, actor: Word=None, x: Word=None, y: Word=None) -> tuple:
    """23198: constrain inward targets on an applicable 0x1000 anchor edge."""
    anchor_edge = 4096
    from .business_formation import _first_frame, _first_word, _first_shift_word, _first_sub_word, _first_add_word, _first_compare_word, _first_region_publish
    frame = _first_frame(memory, frame)
    actor = low16(frame.choice) if actor is None else uint(actor, 16)
    x = low16(frame.target_x) if x is None else uint(x, 16)
    y = low16(frame.target_y) if y is None else uint(y, 16)
    for carrier, observed in ((frame.choice, actor), (frame.target_x, x), (frame.target_y, y)):
        if carrier is not None and low16(carrier) != observed:
            raise ValueError('legacy WORD operands must agree with observed full fields')
    frame = _contact_strategy_actor_slot_fields(memory, frame, 2, True, actor)
    positions = memory.state.table(4294943056).cursor()
    frame = first_replace(frame, roster=positions)
    frame = _first_word(frame, 'unit', actor)
    frame = _first_shift_word(frame, 'unit', actor, 2)
    offset = u16(actor << 2)
    own_x = positions.word(offset)
    frame = _first_word(frame, 'count', own_x)
    own_y = positions.word(offset, 2)
    frame = _first_word(frame, 'distance', own_y)
    anchor = memory.state.table(713462).cursor()
    frame = first_replace(frame, roster=anchor)
    scene = memory.battle_scene()
    frame = _first_word(frame, 'offset_x', scene)
    frame = _first_shift_word(frame, 'offset_x', scene, 2)
    center_y = anchor.word(u16(scene << 2), 2)
    frame = _first_word(frame, 'offset_y', center_y)
    center_x = anchor.word(u16(scene << 2))
    frame = _first_word(frame, 'offset_x', center_x)
    frame, x_distance = _contact_strategy_axis_distance_fields(frame, 'choice', own_x, center_x)
    frame = _first_compare_word(frame, x_distance, anchor_edge)
    adjust_vertical_edge = False
    adjust_horizontal_edge = False
    choose_nearest_axis = False
    if x_distance == anchor_edge:
        frame, y_distance = _contact_strategy_axis_distance_fields(frame, 'choice', own_y, center_y)
        frame = _first_compare_word(frame, y_distance, anchor_edge)
        if y_distance <= anchor_edge:
            frame = _first_compare_word(frame, own_x, center_x)
            frame = _first_compare_word(frame, x, own_x)
            adjust_vertical_edge = x < own_x if own_x > center_x else x > own_x
    elif x_distance < anchor_edge:
        frame, y_distance = _contact_strategy_axis_distance_fields(frame, 'choice', own_y, center_y)
        frame = _first_compare_word(frame, y_distance, anchor_edge)
        if y_distance == anchor_edge:
            frame = _first_compare_word(frame, own_y, center_y)
            frame = _first_compare_word(frame, y, own_y)
            adjust_horizontal_edge = y < own_y if own_y > center_y else y > own_y
    if adjust_vertical_edge:
        frame = _first_compare_word(frame, y, center_y)
        frame = _first_word(frame, 'choice', center_y)
        if y > center_y:
            frame = _first_add_word(frame, 'choice', center_y, anchor_edge)
            edge_y = u16(center_y + anchor_edge)
        else:
            frame = _first_sub_word(frame, 'choice', center_y, anchor_edge)
            edge_y = u16(center_y - anchor_edge)
        frame = _first_compare_word(frame, edge_y, own_y)
        if edge_y != own_y:
            x, y = (own_x, edge_y)
            frame = _first_word(frame, 'target_x', x)
            frame = _first_word(frame, 'target_y', y)
        else:
            choose_nearest_axis = True
    elif adjust_horizontal_edge:
        y = own_y
        frame = _first_word(frame, 'target_y', y)
        frame = _first_compare_word(frame, x, center_x)
        frame = _first_word(frame, 'target_x', center_x)
        if x > center_x:
            frame = _first_add_word(frame, 'target_x', center_x, anchor_edge)
            x = u16(center_x + anchor_edge)
        else:
            frame = _first_sub_word(frame, 'target_x', center_x, anchor_edge)
            x = u16(center_x - anchor_edge)
    if choose_nearest_axis:
        frame, dx = _contact_strategy_axis_distance_fields(frame, 'offset_x', own_x, x)
        frame, dy = _contact_strategy_axis_distance_fields(frame, 'offset_y', own_y, y)
        frame = _first_compare_word(frame, dy, dx)
        if dy > dx:
            x = own_x
            frame = _first_word(frame, 'target_x', x)
        else:
            y = own_y
            frame = _first_word(frame, 'target_y', y)
    frame = _contact_strategy_actor_slot_fields(memory, frame, 2, False, actor)
    return (_first_region_publish(memory, frame), TargetCoordinate(x, y))


def select_nearest_contact_to_battlefield_center_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame, retained_member: Word=None) -> tuple:
    """2330A: one wrapped Manhattan scan and the real full D7 LONG restore."""
    from .business_formation import (_first_frame, _first_word, _first_shift_word,
        _first_add_word, _first_compare_word, _first_memory_word, _first_region_publish)
    frame = _first_frame(memory, frame)
    selected = low16(frame.distance) if retained_member is None else uint(retained_member, 16)
    frame = _contact_strategy_actor_slot_fields(memory, frame, 4, True)
    second = memory.state.read(0xFFFFD302, 2)
    frame = _first_memory_word(frame, second)
    if negative_word(second):
        selected = memory.state.read(0xFFFFD300, 2)
        frame = _first_word(frame, 'distance', selected)
    else:
        anchor = memory.state.table(0x000AE2F6).cursor()
        frame = first_replace(frame, roster=anchor)
        scene = memory.battle_scene()
        frame = _first_word(frame, 'target_x', scene)
        frame = _first_shift_word(frame, 'target_x', scene, 2)
        center_x = anchor.word(u16(scene << 2))
        frame = _first_word(frame, 'target_y', center_x)
        center_y = anchor.word(u16(scene << 2), 2)
        frame = _first_word(frame, 'unit', center_y)
        positions = memory.state.table(0xFFFFA150).cursor()
        candidates = memory.state.table(0xFFFFD300).cursor()
        frame = first_replace(frame, roster=positions, candidates=candidates)
        closest = 65535
        frame = _first_word(frame, 'count', closest)
        while True:
            member = candidates.next_word()
            frame = _first_word(frame, 'offset_x', member)
            if negative_word(member):
                break
            frame = _first_word(frame, 'offset_y', member)
            frame = _first_shift_word(frame, 'offset_y', member, 2)
            offset = u16(member << 2)
            candidate_y = positions.word(offset, 2)
            frame, dy = _contact_strategy_axis_distance_fields(frame, 'choice', candidate_y, center_y)
            candidate_x = positions.word(offset)
            frame, dx = _contact_strategy_axis_distance_fields(frame, 'offset_y', candidate_x, center_x)
            frame = _first_add_word(frame, 'choice', dy, dx)
            distance = u16(dy + dx)
            frame = _first_compare_word(frame, distance, closest)
            if is_nearer_contact(distance, closest):
                closest, selected = distance, member
                frame = _first_word(frame, 'count', closest)
                frame = _first_word(frame, 'distance', selected)
    memory.state.table(0xFFFFF3A6).set_word(0, selected)
    frame = _first_memory_word(frame, selected)
    frame = _contact_strategy_actor_slot_fields(memory, frame, 4, False)
    return _first_region_publish(memory, frame), selected


def test_same_side_total_shortfall_fields(memory: BattlePolicyMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """233E2: side-selected live LONG totals and the actual F768 limit."""
    from .business_formation import _first_frame, _first_long, _first_compare_long
    from ..high_level_gameplay_flow.business_battle import _postbattle_bit_fields
    frame = _first_frame(memory, frame)
    first = memory.state.table(0xFFFFF69E).cursor()
    second = memory.state.table(0xFFFFF6A2).cursor()
    frame = first_replace(frame, roster=first, candidates=second)
    side = memory.state.read(0xFFFFF6D7, 1)
    frame = _postbattle_bit_fields(frame, bool(side & 2))
    if side & 2:
        first, second = second, first
        frame = first_replace(frame, roster=first, candidates=second)
    strength = first.long()
    frame = _first_long(frame, 'target_x', strength)
    opposite = second.long()
    frame = _first_compare_long(frame, strength, opposite)
    selected = False
    if strength < opposite:
        limit = memory.state.read(0xFFFFF768, 4)
        frame = _first_compare_long(frame, strength, limit)
        selected = strength < limit
    return _retreat_carry_fields(memory, frame, selected), selected
