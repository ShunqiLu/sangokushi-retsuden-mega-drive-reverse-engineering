"""Adapted named reusable rules sharing one family-local live state.

These83 original bodies are reuse, not additional physical recovery. Private
logical helpers are not ROM bodies. No other program state or compiler facade
is invoked at runtime; original compatibility operations remain explicit.
"""
from .domain import Byte, CarryOutcome, Cursor, GameplayState, GroupContext, Long, RandomSample, Table, Word, add16, add32, byte, checked_context, checked_long, checked_state, checked_table, checked_word, clear_low_word, descending_inclusive, divu16, divu_retained, high16, integer, long, low16, low8, low_byte, low_word, mask16, mask32, minimum32, mulu16, negate32, negative_byte, negative_long, negative_word, replace_byte, replace_low_word, replace_word, s16, saturating_add32, shl16, shl32, signed_word, stitched_product, sub16, sub32, sub8, subtract_borrow32, swap_words, u16, u32, u8, uint, unsigned, word
from .contexts_reuse import DuelDispositionContext, DuelSettlementContext, DuelSettlementResult, ForceHeadMatch, RadialSeed, EventSubmission

def scale_e000(state: GameplayState, offset: Word, factor: Word) -> Long:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(offset,factor),(),())
    actual=scale_e000_fields(memory,entered)
    return actual.unit

def scale_e0a0(state: GameplayState, offset: Word, factor: Word) -> Long:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(offset,factor),(),())
    actual=scale_e0a0_fields(memory,entered)
    return actual.unit

def scale_e140(state: GameplayState, offset: Word, factor: Word) -> Long:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(offset,factor),(),())
    actual=scale_e140_fields(memory,entered)
    return actual.unit

def scale_e1e0(state: GameplayState, offset: Word, factor: Word) -> Long:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(offset,factor),(),())
    actual=scale_e1e0_fields(memory,entered)
    return actual.unit

def scale_e320(state: GameplayState, offset: Word, factor: Word) -> Long:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(offset,factor),(),())
    actual=scale_e320_fields(memory,entered)
    return actual.unit

def scale_e5a0(state: GameplayState, offset: Word, factor: Word) -> Long:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(offset,factor),(),())
    actual=scale_e5a0_fields(memory,entered)
    return actual.unit

def adjust_battle_losing_loyalty(state: GameplayState) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_gameplay_arrival_fields(state, 0x1D4DA)

def allocate_packed_group_resources(state: GameplayState, packet: Table) -> None:
    """Historical API projects the unique current core; absent full fields remain a boundary."""
    checked_state(state)
    packet = state.checked_table(packet)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=packet.cursor())
    from .business_battle import allocate_packed_group_resources_fields
    frame = allocate_packed_group_resources_fields(BattlePresentationMemory(state), frame)

def append_group_from_survivor_roster(state: GameplayState) -> Table:
    """Historical API only projects the current sole fields; missing full ABI stops honestly."""
    checked_state(state)
    from .business_battle import append_group_from_survivor_roster_fields
    frame = append_group_from_survivor_roster_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())
    return state.table(frame.roster.base)

def append_queue(state: GameplayState, city: Word, incoming_owner: Word) -> Word:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(city,incoming_owner),(),())
    actual=append_queue_fields(memory,entered)
    return low16(actual.target_x)

def apply_battlefield_heavy_losses_and_detach(state: GameplayState) -> Word:
    """Historical API projects the unique current core; absent full fields remain a boundary."""
    checked_state(state)
    frame = FirstDeploymentFrame.unobserved()
    from .business_battle import apply_battlefield_heavy_losses_and_detach_fields
    frame = apply_battlefield_heavy_losses_and_detach_fields(BattlePresentationMemory(state), frame)
    return low16(frame.choice)

def apply_battlefield_ratio_losses(state: GameplayState) -> Word:
    """Historical API projects the unique current core; absent full fields remain a boundary."""
    checked_state(state)
    frame = FirstDeploymentFrame.unobserved()
    from .business_battle import apply_battlefield_ratio_losses_fields
    frame = apply_battlefield_ratio_losses_fields(BattlePresentationMemory(state), frame)
    return low16(frame.choice)

def apply_city_assigned_heavy_losses(state: GameplayState) -> Word:
    """Historical API projects the unique current core; absent full fields remain a boundary."""
    checked_state(state)
    frame = FirstDeploymentFrame.unobserved()
    from .business_battle import apply_city_assigned_heavy_losses_fields
    frame = apply_city_assigned_heavy_losses_fields(BattlePresentationMemory(state), frame)
    return low16(frame.choice)

def apply_duel_disposition(state: GameplayState, context: DuelDispositionContext) -> None:
    """Historical officer/result observations project one full live disposition rule."""
    checked_state(state)
    context = _reuse_checked_context(context,DuelDispositionContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(),target_x=context.officer,unit=context.disposition)
    apply_duel_disposition_fields(BattlePresentationMemory(state),frame)

def apply_returning_officer_loyalty(state: GameplayState) -> None:
    """Historical Gameplay projection of the one returning-loyalty core."""
    checked_state(state)
    apply_returning_officer_loyalty_fields(BattlePresentationMemory(state),
        FirstDeploymentFrame.unobserved())

def attach_member_shift_packet(state: GameplayState, officer: Word, context: GroupContext) -> GroupContext:
    """Historical scalar API projects the sole full core; retained CPU fields are not invented."""
    checked_state(state)
    uint(officer, 16)
    context = checked_context(context, state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=context.source.cursor(), candidates=context.target.cursor())
    from .business_battle import attach_member_shift_packet_fields
    frame = attach_member_shift_packet_fields(BattlePresentationMemory(state), frame)
    return GroupContext(state.table(frame.roster.base), state.table(frame.candidates.base))

def build_battlefield_outcome_candidates(state: GameplayState) -> Word:
    """Historical count projects the same complete live candidate builder."""
    checked_state(state)
    from .business_battle import build_battlefield_outcome_candidates_fields
    from .contexts_battle import BattlePresentationMemory, FirstDeploymentFrame
    return build_battlefield_outcome_candidates_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())[1]

def build_city_assigned_outcome_candidates(state: GameplayState) -> Word:
    """Historical count projects the same complete live candidate builder."""
    checked_state(state)
    from .business_battle import build_city_assigned_outcome_candidates_fields
    from .contexts_battle import BattlePresentationMemory, FirstDeploymentFrame
    return build_city_assigned_outcome_candidates_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())[1]

def build_roster(state: GameplayState, city: Word) -> Word:
    """Historical API only projects the current sole fields; missing full ABI stops honestly."""
    checked_state(state)
    uint(city, 16)
    from .business_battle import build_roster_fields
    frame = build_roster_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())
    return low16(frame.count)

def choose_city_head(state: GameplayState, city: Word) -> Word:
    """Historical API only projects the current sole fields; missing full ABI stops honestly."""
    checked_state(state)
    uint(city, 16)
    from .business_battle import choose_city_head_fields
    frame = choose_city_head_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())
    return low16(frame.target_x)

def choose_empty_neighbor_position(state: GameplayState) -> tuple[Word, Word]:
    """Historical API only projects the current sole fields; missing full ABI stops honestly."""
    checked_state(state)
    from .business_battle import choose_empty_neighbor_position_fields
    frame = choose_empty_neighbor_position_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())
    return low16(frame.target_x), low16(frame.target_y)

def commit_income(state: GameplayState, city: Word, offset: Word, factor: Word, ledger: Table):
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(city,offset,factor),(),(('scan',ledger),))
    actual=commit_income_fields(memory,entered)

def compute_outcome_force_ratio(state: GameplayState) -> Word:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    checked_state(state)
    frame = compute_outcome_force_ratio_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())
    return low16(frame.target_y)

def consume_city_battle_resources(state: GameplayState) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    checked_state(state)
    consume_city_battle_resources_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())

def credit_packed_group_resources(state: GameplayState, packet: Table, city: Word) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_gameplay_arrival_fields(state, 0x1D44C, packet, city)

def credit_primary(state: GameplayState, city: Word):
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(city,),(),())
    actual=credit_primary_fields(memory,entered)

def credit_secondary(state: GameplayState, city: Word):
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(city,),(),())
    actual=credit_secondary_fields(memory,entered)

def debit_primary(state: GameplayState, city: Word):
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(city,),(),())
    actual=debit_primary_fields(memory,entered)

def debit_secondary(state: GameplayState, city: Word):
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(city,),(),())
    actual=debit_secondary_fields(memory,entered)

def deplete_income(state: GameplayState, city: Word, thresholds: Table):
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(city,),(),(('candidates',thresholds),))
    actual=deplete_income_fields(memory,entered)

def detach_defeated_duelist(state: GameplayState, officer: Word) -> None:
    """Historical scalar projection of the one original unbounded removal."""
    checked_state(state)
    uint(officer,16)
    frame = first_replace(FirstDeploymentFrame.unobserved(),target_x=officer)
    detach_defeated_duelist_fields(BattlePresentationMemory(state),frame)

def detach_member_keep_group_cursor(state: GameplayState, officer: Word, context: GroupContext) -> GroupContext:
    """Historical scalar API projects the sole full core; retained CPU fields are not invented."""
    checked_state(state)
    uint(officer, 16)
    context = checked_context(context, state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=context.source.cursor(), candidates=context.target.cursor())
    from .business_battle import detach_member_keep_group_cursor_fields
    frame = detach_member_keep_group_cursor_fields(BattlePresentationMemory(state), frame)
    return GroupContext(state.table(frame.roster.base), state.table(frame.candidates.base))

def detach_zero_readiness_duelists(state: GameplayState) -> None:
    """Historical projection of the sole two-packet readiness rule."""
    checked_state(state)
    detach_zero_readiness_duelists_fields(BattlePresentationMemory(state),FirstDeploymentFrame.unobserved())

def divide_percent(state: GameplayState, product: Long) -> Long:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(),(('unit',product),),())
    actual=divide_percent_fields(memory,entered)
    return actual.unit

def erase_group_packet(state: GameplayState, packet: Table) -> Table:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    frame = project_gameplay_arrival_fields(state, 0x1D4B8, packet)
    return state.table(frame.roster.base)

def find_group_at_coordinate(state: GameplayState, coordinate: Word) -> Table:
    """Return a live packed-group view, or the true zero-header sentinel view."""
    state = checked_state(state)
    coordinate = uint(coordinate, 16)
    x = coordinate >> 8
    y = low8(coordinate)
    group = state.group_packets
    while True:
        members = group.byte() & 15
        if members == 0:
            return group
        if group.byte(0, 1) == x:
            if group.byte(0, 2) == y:
                return group
        group = group.advance(13 + members)

def grant_duel_fallback_progress(state: GameplayState, receiver_offset: Word, donor: Word, progress: Table) -> Long:
    """Historical projection of sole fallback progress; retained full fields stay unknown."""
    checked_state(state)
    uint(receiver_offset, 16)
    uint(donor, 16)
    progress = state.checked_table(progress)
    frame = first_replace(FirstDeploymentFrame.unobserved(), target_x=receiver_offset,
        target_y=donor, scan=progress.cursor())
    return grant_duel_fallback_progress_fields(BattlePresentationMemory(state), frame).count

def grant_duel_troop_difference_progress(state: GameplayState, receiver: Word, troop_difference: Long, progress: Table) -> Long:
    """Historical projection of sole troop-loss gain; no alternate scalar algorithm."""
    checked_state(state)
    uint(receiver, 16)
    uint(troop_difference, 32)
    progress = state.checked_table(progress)
    frame = first_replace(FirstDeploymentFrame.unobserved(), target_x=receiver,
        unit=troop_difference, scan=progress.cursor())
    return grant_duel_troop_difference_progress_fields(BattlePresentationMemory(state), frame).count

def grow_original_long_field(state: GameplayState, target: Table) -> Long:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(),(),(('roster',target),))
    actual=grow_original_long_field_fields(memory,entered)
    return actual.target_y

def initialize_prebattle_head_bytes(state: GameplayState) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_gameplay_arrival_fields(state, 0x1D57A)

def load_battlefield_map_context(state: GameplayState) -> Table:
    """Each scene uses a 0x8c0-byte terrain map."""
    checked_state(state)
    scene = state.scalar('battle_scene')
    return state.battlefield_maps.advance(scene * 2240)

def locate_group_city(state: GameplayState, packet: Table) -> Word:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    frame = project_gameplay_arrival_fields(state, 0x1D40C, packet)
    return low16(frame.count)

def owner_has_other_city_carry(state: GameplayState) -> CarryOutcome:
    """Historical API projects the unique current core; absent full fields remain a boundary."""
    checked_state(state)
    frame = FirstDeploymentFrame.unobserved()
    from .business_battle import owner_has_other_city_carry_fields
    frame = owner_has_other_city_carry_fields(BattlePresentationMemory(state), frame)
    return state.carry_result(frame.status & 1)

def partition_city_survivors(state: GameplayState) -> None:
    """Historical API projects the unique current core; absent full fields remain a boundary."""
    checked_state(state)
    frame = FirstDeploymentFrame.unobserved()
    from .business_battle import partition_city_survivors_fields
    frame = partition_city_survivors_fields(BattlePresentationMemory(state), frame)

def positive_denominator(state: GameplayState, numerator: Long, denominator: Long) -> tuple[Long, Long]:
    """Do not retest negated 80000000; preserve the original shared tail."""
    checked_state(state)
    uint(numerator, 32)
    uint(denominator, 32)
    if negative_long(numerator):
        quotient, remainder = unsigned_divmod(state, u32(-numerator), denominator)
        return (u32(-quotient), u32(-remainder))
    return unsigned_divmod(state, numerator, denominator)

def read_battlefield_terrain_type(state: GameplayState,
        map_context: Table, x: Word, y: Word, retained: Long=0) -> Long:
    """Historical explicit retained-LONG API projects its unique observation core."""
    uint(retained, 32)
    return read_battlefield_terrain_type_observations(state, map_context, x, y, retained)[0]

def rebuild_primary_after_battle(state: GameplayState) -> None:
    """Historical API projects the unique current core; absent full fields remain a boundary."""
    checked_state(state)
    frame = FirstDeploymentFrame.unobserved()
    from .business_battle import rebuild_primary_after_battle_fields
    frame = rebuild_primary_after_battle_fields(BattlePresentationMemory(state), frame)

def rebuild_secondary_after_battle(state: GameplayState) -> None:
    """Historical API projects the unique current core; absent full fields remain a boundary."""
    checked_state(state)
    frame = FirstDeploymentFrame.unobserved()
    from .business_battle import rebuild_secondary_after_battle_fields
    frame = rebuild_secondary_after_battle_fields(BattlePresentationMemory(state), frame)

def remove_defeated_packed_member(state: GameplayState, officer: Word, context: GroupContext) -> GroupContext:
    """Historical scalar API projects the sole full core; retained CPU fields are not invented."""
    checked_state(state)
    uint(officer, 16)
    context = checked_context(context, state)
    frame = first_replace(FirstDeploymentFrame.unobserved(), candidates=context.source.cursor(), controller=context.target)
    from .business_battle import remove_defeated_packed_member_fields
    frame = remove_defeated_packed_member_fields(BattlePresentationMemory(state), frame)
    return GroupContext(state.table(frame.candidates.base), state.table(frame.controller.base))

def remove_group_reference(state: GameplayState, officer: Word) -> None:
    """Historical scalar API projects the sole full core; retained CPU fields are not invented."""
    checked_state(state)
    uint(officer, 16)
    frame = FirstDeploymentFrame.unobserved()
    from .business_battle import remove_group_reference_fields
    frame = remove_group_reference_fields(BattlePresentationMemory(state), frame)

def remove_zero_readiness_duelist(state: GameplayState, officer: Word) -> None:
    """Historical officer observation projects sole live removal and physical MOVEM."""
    checked_state(state)
    uint(officer, 16)
    entered = first_replace(FirstDeploymentFrame.unobserved(), target_y=officer)
    remove_zero_readiness_duelist_fields(BattlePresentationMemory(state), entered)

def replace_group_head_reference(state: GameplayState, officer: Word, group: Table) -> None:
    """Historical scalar API projects the sole full core; retained CPU fields are not invented."""
    checked_state(state)
    uint(officer, 16)
    group = state.checked_table(group)
    frame = first_replace(FirstDeploymentFrame.unobserved(), roster=group.cursor())
    from .business_battle import replace_group_head_reference_fields
    frame = replace_group_head_reference_fields(BattlePresentationMemory(state), frame)

def replace_or_remove_group_references(state: GameplayState, old_head: Word, new_head: Word) -> None:
    """Historical scalar API projects the sole full core; retained CPU fields are not invented."""
    checked_state(state)
    uint(old_head, 16)
    uint(new_head, 16)
    frame = FirstDeploymentFrame.unobserved()
    from .business_battle import replace_or_remove_group_references_fields
    frame = replace_or_remove_group_references_fields(BattlePresentationMemory(state), frame)

def replenish_b200_troops(state: GameplayState, retained_city: Word) -> Word:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(retained_city,),(),())
    actual=replenish_b200_troops_fields(memory,entered)
    return low16(actual.target_x)

def reset_queue(state: GameplayState) -> None:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(),(),())
    actual=reset_queue_fields(memory,entered)

def restore_returning_officer_assignments(state: GameplayState) -> None:
    """Historical API projects the unique current core; absent full fields remain a boundary."""
    checked_state(state)
    frame = FirstDeploymentFrame.unobserved()
    from .business_battle import restore_returning_officer_assignments_fields
    frame = restore_returning_officer_assignments_fields(BattlePresentationMemory(state), frame)

def roster_contains_force_head_carry(state: GameplayState, city: Word, head: Word) -> ForceHeadMatch:
    """Historical API only projects the current sole fields; missing full ABI stops honestly."""
    checked_state(state)
    uint(city, 16)
    uint(head, 16)
    from .business_battle import roster_contains_force_head_carry_fields
    frame = roster_contains_force_head_carry_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())
    return ForceHeadMatch(low16(frame.distance), state.carry_result(frame.status & 1))

def rounded_radial_distance(state: GameplayState, squared_distance: Long) -> Long:
    """Original table-seeded odd-increment algorithm, including retained high bits."""
    checked_state(state)
    uint(squared_distance, 32)
    if squared_distance == 0:
        return 0
    seed = seed_radial_distance_from_thresholds(state, squared_distance)
    remaining, count, increment = (seed.remaining, seed.count, seed.increment)
    while True:
        previous = remaining
        remaining = u32(remaining - increment)
        if previous < increment:
            return replace_word(remaining, low16(count))
        count = replace_word(count, u16(count + 1))
        increment = replace_word(increment, u16(increment + 2))

def sample_once(state: GameplayState) -> Word:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(),(),())
    actual=sample_once_fields(memory,entered)
    return low16(actual.target_x)

def sample_small(state: GameplayState) -> Word:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(),(),())
    actual=sample_small_fields(memory,entered)
    return low16(actual.target_x)

def sample_wide(state: GameplayState) -> Word:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(),(),())
    actual=sample_wide_fields(memory,entered)
    return low16(actual.target_x)

def scaled_income(state: GameplayState, offset: Word, factor: Word):
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(offset,factor),(),())
    actual=scaled_income_fields(memory,entered)

def seed_radial_distance_from_thresholds(state: GameplayState, squared_distance: Long, retained_count: Long=0, retained_threshold: Long=0) -> RadialSeed:
    """For direct zero input, the original can read the preceding code row."""
    checked_state(state)
    uint(squared_distance, 32)
    uint(retained_count, 32)
    uint(retained_threshold, 32)
    if squared_distance >= 144781:
        return RadialSeed(u32(squared_distance - 144781), replace_word(retained_count, 381), 762, retained_threshold, None)
    thresholds = state.radial_threshold_rows
    while squared_distance >= thresholds.long():
        thresholds = thresholds.advance(6)
    preceding_threshold = thresholds.long(0, -6)
    increment = thresholds.word(0, -2)
    remaining = u32(squared_distance - preceding_threshold)
    count = replace_word(retained_count, increment >> 1)
    return RadialSeed(remaining, count, increment, preceding_threshold, thresholds)

def settle_battle_packed_armies(state: GameplayState) -> None:
    """Historical scalar API projects the sole full core; retained CPU fields are not invented."""
    checked_state(state)
    frame = FirstDeploymentFrame.unobserved()
    from .business_battle import settle_battle_packed_armies_fields
    frame = settle_battle_packed_armies_fields(BattlePresentationMemory(state), frame)

def settle_duel_packets(state: GameplayState, context: DuelSettlementContext) -> CarryOutcome:
    """Historical carrier projects sole packet settlement; unobserved ABI stays a boundary."""
    checked_state(state)
    context = _reuse_checked_context(context,DuelSettlementContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(),unit=context.training_carrier)
    frame = settle_duel_packets_fields(BattlePresentationMemory(state),frame)
    return state.carry_result(int(bool(frame.status & 1)))

def settle_duel_result_roster(state: GameplayState) -> None:
    """Historical projection of sole result routing, with honest missing entry fields."""
    checked_state(state)
    settle_duel_result_roster_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())

def settle_duel_training_and_troops(state: GameplayState, context: DuelSettlementContext) -> DuelSettlementResult:
    """Historical D2-only observation projects sole settlement; no default complete ABI."""
    checked_state(state)
    context = _reuse_checked_context(context, DuelSettlementContext)
    frame = first_replace(FirstDeploymentFrame.unobserved(), unit=context.training_carrier)
    actual = settle_duel_training_and_troops_fields(BattlePresentationMemory(state), frame)
    return DuelSettlementResult(actual.count)

def settle_expense(state: GameplayState, city: Word, factor: Word, ledger: Table):
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(city,factor),(),(('scratch',ledger),))
    actual=settle_expense_fields(memory,entered)

def settle_group_at_city(state: GameplayState) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_gameplay_arrival_fields(state, 0x1D3BC)

def settle_shortage(state: GameplayState, outstanding: Long, factor: Word):
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(factor,),(('distance',outstanding),),())
    actual=settle_shortage_fields(memory,entered)

def signed_divmod(state: GameplayState, numerator: Long, denominator: Long) -> tuple[Long, Long]:
    checked_state(state)
    uint(numerator, 32)
    uint(denominator, 32)
    if negative_long(denominator):
        quotient, remainder = positive_denominator(state, numerator, u32(-denominator))
        return (u32(-quotient), remainder)
    return positive_denominator(state, numerator, denominator)

def sort_returning_officer_status(state: GameplayState, surplus: Word) -> Word:
    """Historical API projects the unique current core; absent full fields remain a boundary."""
    checked_state(state)
    uint(surplus, 16)
    frame = FirstDeploymentFrame.unobserved()
    from .business_battle import sort_returning_officer_status_fields
    frame = sort_returning_officer_status_fields(BattlePresentationMemory(state), frame)
    return low16(frame.target_y)

def step_random(state: GameplayState) -> Long:
    """Return full original sample carrier; its upper WORD is the old seed's."""
    return _reuse_advance_random_pair(state).sample

def submit_classified_fields(state: GameplayState, city: Word) -> Word:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(city,),(),())
    actual=submit_calendar_classified_fields(memory,entered)
    return low16(actual.target_x)

def submit_four_fields(state: GameplayState, city: Word, incoming_owner: Word) -> EventSubmission:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(city,incoming_owner),(),())
    actual=submit_calendar_four_fields(memory,entered)
    return EventSubmission(low16(actual.target_x),low16(actual.choice))

def submit_three_fields(state: GameplayState, city: Word, incoming_owner: Word) -> EventSubmission:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    memory,entered=_calendar_legacy_entry_fields(state,(city,incoming_owner),(),())
    actual=submit_calendar_three_fields(memory,entered)
    return EventSubmission(low16(actual.target_x),low16(actual.choice))

def sum_group_troops(state: GameplayState, roster: Cursor, troops: Table) -> tuple[Long, Word]:
    """Historical cursor/count API projects the same179BE loop with D1 high unknown."""
    from .contexts_services import SceneRefreshMemory
    checked_state(state)
    checked_table(roster,state)
    checked_table(troops,state)
    entered = first_replace(FirstDeploymentFrame.unobserved(),roster=troops.cursor(),candidates=roster.advance(0))
    actual,count = sum_group_troops_fields(SceneRefreshMemory(state),entered)
    roster.base = actual.candidates.base
    return actual.target_x,count

def terrain_cell_query(state: GameplayState, row: Word, column: Word) -> tuple[Byte, Byte]:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    frame = project_gameplay_arrival_fields(state, 0x142A2, row=row, column=column)
    return low8(frame.unit), low8(frame.count)

def transfer_battle_roster(state: GameplayState, officer: Word) -> None:
    """Historical scalar projection of sole active-to-retired transfer."""
    checked_state(state)
    uint(officer, 16)
    entered = first_replace(FirstDeploymentFrame.unobserved(), target_x=officer)
    transfer_battle_roster_fields(BattlePresentationMemory(state), entered)

def transfer_outcome_officer(state: GameplayState) -> None:
    """Historical scalar API projects the sole full core; retained CPU fields are not invented."""
    checked_state(state)
    frame = FirstDeploymentFrame.unobserved()
    from .business_battle import transfer_outcome_officer_fields
    frame = transfer_outcome_officer_fields(BattlePresentationMemory(state), frame)

def unsigned_divmod(state: GameplayState, numerator: Long, denominator: Long) -> tuple[Long, Long]:
    """Accepted two-stage estimate and wrapped-product correction algorithm."""
    checked_state(state)
    uint(numerator, 32)
    uint(denominator, 32)
    if denominator <= 65535:
        return word_pair_divmod(state, numerator, denominator)
    if denominator == numerator:
        return (1, 0)
    if denominator > numerator:
        return (0, numerator)
    divisor_high = u32(high16(denominator) + 1)
    quotient, remainder = word_pair_divmod(state, numerator, divisor_high)
    denominator_part = divu_retained(denominator, low16(divisor_high))
    quotient = low16(divu_retained(quotient, low16(denominator_part)))
    while True:
        product = u32(low16(denominator) * low16(quotient))
        upper_product = u32(high16(denominator) * low16(quotient))
        product = u32(product + swap_words(upper_product))
        if product > numerator:
            quotient = u32(quotient - 1)
            continue
        remainder = u32(numerator - product)
        if denominator <= remainder:
            quotient = u32(quotient + 1)
            continue
        return (quotient, remainder)

def word_pair_divmod(state: GameplayState, numerator: Long, denominator: Long) -> tuple[Long, Long]:
    checked_state(state)
    uint(numerator, 32)
    uint(denominator, 32)
    divisor = low16(denominator)
    upper_division = divu_retained(high16(numerator), divisor)
    upper_quotient = low16(upper_division)
    lower_dividend = u32(high16(upper_division) << 16 | low16(numerator))
    lower_division = divu_retained(lower_dividend, divisor)
    return (u32(upper_quotient << 16 | low16(lower_division)), high16(lower_division))

def wrapped_product(value: Long, factor: Word) -> Long:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    return _calendar_product_terms(value,factor)[3]

def _reuse_active_duel_roster(state: GameplayState, officer: Word):
    if officer == state.scalar('roster_side_owner'):
        return state.battle_primary_roster.cursor()
    return state.battle_secondary_roster.cursor()

def _reuse_advance_random_pair(state: GameplayState) -> RandomSample:
    checked_state(state)
    original = state.scalar('random_seed')
    if original == 0:
        original = 711800410
    mixed = u32(u32(u32(u32(original << 2) + original) << 3) + original)
    sample = replace_word(original, low16(mixed))
    mixed = swap_words(mixed)
    sample = replace_word(sample, u16(low16(sample) + low16(mixed)))
    mixed = swap_words(replace_word(mixed, low16(sample)))
    state.set_scalar('random_seed', mixed)
    return RandomSample(sample, mixed)

def _reuse_append_at_roster_end(destination: Cursor, officer: Word) -> None:
    while not negative_word(destination.next_word()):
        pass
    destination.set_word(0, officer, -2)
    destination.put_word(65535)

def _reuse_assigned_troop_total(state: GameplayState, assignments: Table, city: Word) -> Long:
    total = 0
    for officer in range(255, -1, -1):
        if assignments.byte(officer) == city & 255:
            total = u32(total + state.officer_troops.long(u16(officer << 2)))
            total = u32(total + 100)
    return total

def _reuse_candidate_strength_totals(state: GameplayState) -> tuple[Long, Word, Word]:
    source = state.action_candidates.cursor()
    troops, first_attribute, second_attribute = (0, 0, 0)
    while True:
        officer = source.next_word()
        if negative_word(officer):
            return (troops, first_attribute, second_attribute)
        offset = u16(officer << 1)
        first_attribute = u16(first_attribute + state.officer_word_b400.word(offset))
        second_attribute = u16(second_attribute + state.officer_word_b600.word(offset))
        troops = u32(troops + state.officer_troops.long(u16(offset << 1)))

def _reuse_compact_after_match(source):
    while True:
        member = source.next_word()
        source.set_word(0, member, -4)
        if negative_word(member):
            return

def _reuse_compact_live_roster(source: Cursor) -> None:
    while True:
        member = source.next_word()
        source.set_word(0, member, -4)
        if negative_word(member):
            return

def _reuse_duel_training_loss(state: GameplayState, carrier: Long) -> Long:
    sample = low16(state.sample_random())
    doubled = u32(sample << 1)
    scaled = replace_word(doubled, u16(low16(doubled) + sample))
    loss = u16(high16(scaled) + 1)
    previous = low16(carrier)
    return replace_word(carrier, 0 if previous < loss else u16(previous - loss))

def _reuse_low_readiness_progress(state: GameplayState, readiness_offset: Word, check_city_head: bool, detach: bool) -> Word:
    progress = state.officer_word_c000.word(readiness_offset)
    value = divu_retained(progress, 5)
    officer = readiness_offset >> 1
    if check_city_head:
        scene_offset = u16(state.scalar('battle_scene') << 1)
        if officer == state.city_head_words.word(scene_offset):
            value = replace_word(value, u16(low16(value) + 30))
    if detach:
        state.officer_city_assignment.set_byte(officer, 255)
    if state.officer_status.byte(officer) & 16:
        value = replace_word(value, u16(low16(value) + 20))
    return low16(value)

def _reuse_multiply_word_parts(value: Long, factor: Word) -> Long:
    """Original low/high WORD products and SWAP, including high-product spill."""
    return u32(low16(value) * factor + swap_words(high16(value) * factor))

def _reuse_random_fraction(state: GameplayState, span: Word, base: Word=0) -> Word:
    sample = low16(state.sample_random())
    return u16(high16(u32(sample * span)) + base)

def _reuse_seek_officer_unbounded(source: Cursor, officer: Word) -> None:
    """Original masked-ID search has no negative-terminator exit."""
    while source.next_word() & 255 != officer:
        pass

def _reuse_checked_context(value, expected):
    if type(value) is not expected:
        raise ValueError('exact outcome-family context required')
    value.__post_init__()
    return value

def _reuse_collect_city_attached_officers(state: GameplayState) -> Word:
    output = state.battle_candidate_roster.cursor()
    city = state.city()
    count = 0
    for officer in descending_inclusive(255):
        if state.officer_assignments.byte(officer) == low8(city):
            output.append_word(officer)
            count = u16(count + 1)
    output.set_word(0, 65535)
    return count

def _reuse_collect_unassigned_city_officers(state: GameplayState) -> Word:
    output = state.battle_candidate_roster.cursor()
    city = state.city()
    count = 0
    for officer in descending_inclusive(255):
        if state.alternate_assignments.byte(officer) == low8(city):
            if not negative_byte(state.officer_assignments.byte(officer)):
                output.append_word(officer)
                count = u16(count + 1)
    output.set_word(0, 65535)
    return count

def _reuse_random_sample(state: GameplayState) -> Word:
    seed = state.seed()
    if seed == 0:
        seed = 711800410
    original = seed
    mixed = u32(seed << 2)
    mixed = u32(mixed + original)
    mixed = u32(mixed << 3)
    mixed = u32(mixed + original)
    sample = replace_word(original, low16(mixed))
    mixed = swap_words(mixed)
    sample = replace_word(sample, u16(sample + mixed))
    mixed = replace_word(mixed, low16(sample))
    mixed = swap_words(mixed)
    state.store_seed(mixed)
    return low16(sample)

def _reuse_scale_field(state: GameplayState, offset: Word, factor: Word, field_name: str) -> Long:
    offset = checked_word(offset)
    factor = checked_word(factor)
    field = state.field(field_name)
    previous = field.read(offset)
    product = wrapped_product(previous, factor)
    result = divide_percent(state, product)
    field.write(offset, result)
    return result


from .contexts_battle import (BattlePresentationMemory, FirstDeploymentFrame, first_replace, _first_word, _first_long, _first_add_word, _first_right_word, _first_compare_word)
from ..high_level_battle_ai.business_formation import _first_byte

def apply_returning_officer_loyalty_fields(memory: BattlePresentationMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """confirmed 208CE..20930: returning officer loyalty on the same live RAM.

    The Scene caller supplies its full current fields and owns its outer JSR
    and saved officer WORD. This body owns only its seven MOVEM LONGs and
    RNG208D8 slot. Historical Gameplay has no observed A7; its projection
    shares this algorithm without inventing a physical stack or high bits.
    """
    from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
    from ..high_level_main_flows.business_movement_support import (
        _movement_save_longs, _movement_restore_longs,
    )
    if type(memory) is not BattlePresentationMemory:
        raise ValueError('closed same-state returning-loyalty memory required')
    entered = memory.validate_frame(frame)
    physical = frame.stack_cursor is not None
    if type(memory.state) is not GameplayState and (
            not physical or frame.roster is None or frame.candidates is None):
        raise MovementContinuationBoundary(0x208CE, frame,
            'original loyalty MOVEM requires the actual Scene A7/A0/A1 fields')
    saved = ('target_x', 'target_y', 'unit', 'count', 'distance', 'roster', 'candidates')
    if physical:
        frame = _movement_save_longs(memory.state, frame, saved)
    frame = _presentation_call_fields(memory, frame, 0x208D8, _presentation_random_fields)
    sample = u32(frame.target_x & 65535)
    frame = _first_long(frame, 'target_x', sample)
    frame = _first_long(frame, 'target_y', sample)
    scaled = u32(sample * 5)
    frame = _first_long(frame, 'target_x', swap_words(scaled))
    factor = u16(high16(scaled) + 6)
    frame = _first_add_word(frame, 'target_x', high16(scaled), 6)
    loyalty = memory.table(0xFFFFC300).cursor()
    frame = first_replace(frame, roster=loyalty)
    frame = _first_word(frame, 'target_y', 104)
    selected = memory.table(0xFFFFF3A6).word()
    frame = _first_word(frame, 'unit', selected)
    officer = u16(selected & 255)
    frame = _first_word(frame, 'unit', officer)
    prior = loyalty.byte(officer)
    gap = u8(104 - prior)
    overflow = bool((104 ^ prior) & (104 ^ gap) & 128)
    conditions = (17 if 104 < prior else 0) | (2 if overflow else 0) | (8 if gap & 128 else 0) | (4 if gap == 0 else 0)
    frame = first_replace(frame, target_y=replace_byte(frame.target_y, gap), status=conditions)
    reduced = u16(gap >> 1)
    frame = _first_right_word(frame, 'target_y', gap, 1)
    affinity = memory.table(0xFFFFC200).cursor()
    frame = first_replace(frame, candidates=affinity)
    source_word = memory.table(0xFFFFF3F2).word()
    frame = _first_word(frame, 'distance', source_word)
    source = u16(source_word & 255)
    frame = _first_word(frame, 'distance', source)
    frame = _first_word(frame, 'count', 0)
    influence = u16(affinity.byte(source))
    frame = _first_byte(frame, 'count', influence)
    value = u32(low16(reduced) * low16(influence))
    frame = _first_long(frame, 'target_y', value)
    value = u32(low16(value) * low16(factor))
    frame = _first_long(frame, 'target_y', value)
    # Fixed bounds: <=127*255*10, so DIVU500 cannot overflow its quotient.
    value = divu_retained(value, 500)
    frame = first_replace(frame, target_y=value)
    frame = _first_word(frame, 'target_y', low16(value))
    frame = _first_compare_word(frame, low16(value), 100)
    if low16(value) > 100:
        value = u32(value & 4294901760 | 100)
        frame = _first_word(frame, 'target_y', 100)
    loyalty.set_byte(officer, low8(value))
    # Idempotent D1 BYTE projection supplies the memory MOVE.B flags only.
    frame = _first_byte(frame, 'target_y', low8(value))
    memory.finish(frame)
    if physical:
        frame = _movement_restore_longs(memory.state, frame, saved)
    else:
        frame = first_replace(frame, target_x=entered.target_x,
            target_y=entered.target_y, unit=entered.unit, count=entered.count,
            distance=entered.distance, roster=entered.roster, candidates=entered.candidates)
    return memory.finish(frame)

from .business_battle import _presentation_call_fields, _presentation_random_fields
from ..high_level_battle_ai.business_formation import _first_byte


# Sole historical terrain algorithm exposes actual partial observations.
def read_battlefield_terrain_type_observations(state: GameplayState,
        map_context: Table, x: Word, y: Word, retained: Long | None) -> tuple:
    """One historical terrain algorithm, now exposing a partial-carrier result.

    None stays unobserved; the low WORD/category and original final LSL X are
    still observable. No extra map read or synthesized retained zero occurs.
    """
    checked_state(state)
    checked_table(map_context, state)
    uint(x, 16)
    uint(y, 16)
    if retained is not None:
        uint(retained, 32)
    before_shift = u16((x >> 3) * 40 + (y >> 3))
    offset = u16(before_shift * 2)
    tile = map_context.word(offset) & 1023
    category = state.terrain_category_lookup.byte(tile)
    terrain_word = (tile & 65280) | category
    carrier = None if retained is None else replace_word(retained, terrain_word)
    return carrier, terrain_word, category, bool(before_shift & 32768)

from .contexts_reuse import project_gameplay_arrival_fields

from .business_battle import compute_outcome_force_ratio_fields, consume_city_battle_resources_fields


# The old return/loss APIs do not manufacture complete CPU fields.
from .contexts_battle import first_replace

def sum_group_troops_fields(memory, frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, Word]:
    """179BE sole sentinel roster sum; the separate WORD observation needs no fake D1 high."""
    from .contexts_services import SceneRefreshMemory, SceneRefreshBoundary
    from ..high_level_battle_ai.business_formation import _first_shift_word
    from ..high_level_main_flows.business_movement_support import _movement_binary_flags
    if type(memory) is not SceneRefreshMemory:
        raise ValueError('same-state troop-sum memory required')
    memory.frame(frame)
    if frame.roster is None or frame.candidates is None:
        raise SceneRefreshBoundary(0x179BE,frame,None)
    frame = _first_long(frame,'target_x',0)
    frame = _first_word(frame,'target_y',0)
    count = 0
    while True:
        member = frame.candidates.word()
        frame = first_replace(frame,candidates=frame.candidates.advance(2))
        frame = _first_word(frame,'unit',member)
        if negative_word(member):
            return memory.sync_status(frame),count
        officer = member & 255
        frame = _first_word(frame,'unit',officer)
        frame,count = _movement_binary_flags(memory.state,frame,count,1,16)
        frame = first_replace(frame,target_y=None if frame.target_y is None else replace_word(frame.target_y,count))
        frame = _first_shift_word(frame,'unit',officer,2)
        quantity = frame.roster.long(officer << 2)
        before = frame.target_x
        frame,total = _movement_binary_flags(memory.state,frame,before,quantity,32)
        frame = first_replace(frame,target_x=total)


"""Current complete duel settlement over one live Gameplay/Scene state."""
from ..high_level_main_flows.business_movement_support import (
    _movement_move, _movement_move_long, _movement_test, _movement_compare,
    _movement_fixed_shift_word, _movement_adjust_word, _movement_add_word,
    _movement_binary_flags, _movement_divu_word, _movement_bit,
    _movement_save_longs, _movement_restore_longs,
)


def _duel_result_write_fields(memory, frame: FirstDeploymentFrame,
        address: Long, size: Word, value: Long) -> FirstDeploymentFrame:
    """Original settlement MOVEs, with no fabricated CLR prior read."""
    if size not in (1, 2):
        raise ValueError('closed duel result BYTE/WORD store required')
    memory.state.write(address, size, value)
    return _movement_test(memory.state, frame, value, size * 8)


def _duel_result_call_fields(memory, frame: FirstDeploymentFrame,
        target: Long, continuation: Long) -> FirstDeploymentFrame:
    """Closed physical children of the six settlement owners; no scalar service substitute."""
    from .business_battle import _presentation_call_fields, _presentation_random_fields
    allowed = ((0x83D4, 0x188DA), (0x83D4, 0x1893A),
        (0x189D4, 0x18910), (0x189D4, 0x18970),
        (0x18A54, 0x1891A), (0x18A54, 0x1897A),
        (0x18A2E, 0x189A0), (0x18A2E, 0x189BA),
        (0x18A94, 0x189D2), (0x18AC6, 0x18AB6), (0x18AC6, 0x18AC4),
        (0x18B94, 0x18B56), (0x18B94, 0x18B66), (0x18C56, 0x18B82),
        (0x188A6, 0x18B86), (0x18C88, 0x18C72), (0x18C88, 0x18C86))
    if (target, continuation) not in allowed:
        raise ValueError('original duel settlement child and continuation required')
    def child(actual_memory, entered):
        if target == 0x83D4:
            return _presentation_random_fields(actual_memory, entered)
        if target == 0x189D4:
            return grant_duel_fallback_progress_fields(actual_memory, entered)
        if target == 0x18A54:
            return remove_zero_readiness_duelist_fields(actual_memory, entered)
        if target == 0x18A2E:
            return grant_duel_troop_difference_progress_fields(actual_memory, entered)
        if target == 0x18A94:
            return settle_duel_result_roster_fields(actual_memory, entered)
        if target == 0x18B94:
            return apply_duel_disposition_fields(actual_memory, entered)
        if target == 0x18C56:
            return detach_zero_readiness_duelists_fields(actual_memory, entered)
        if target == 0x18C88:
            return detach_defeated_duelist_fields(actual_memory, entered)
        if target == 0x188A6:
            return settle_duel_training_and_troops_fields(actual_memory, entered)
        return transfer_battle_roster_fields(actual_memory, entered)
    return _presentation_call_fields(memory, frame, continuation, child)


def _duel_training_side_fields(memory, frame: FirstDeploymentFrame,
        side: Word) -> FirstDeploymentFrame:
    """Two original side blocks share one ordered training/readiness rule and distinct slots."""
    if side not in (0, 1):
        raise ValueError('closed original duelist side required')
    state = memory.state
    officer_address, donor_address = ((0xFFFF80E0, 0xFFFF80E2) if side == 0
        else (0xFFFF80E2, 0xFFFF80E0))
    frame = _movement_move(state, frame, 'target_x', state.read(officer_address, 2), 16)
    frame = _movement_move(state, frame, 'unit', state.read(0xFFFF8101 + side * 2, 1), 8)
    frame = _movement_compare(state, frame, state.read(0xFFFF8114, 2), 4 + side, 16)
    if frame.status & 4:
        stack = frame.stack_cursor.advance(-2)
        stack.set_word(0, low16(frame.target_x))
        frame = first_replace(frame, stack_cursor=stack)
        frame = _movement_test(state, frame, low16(frame.target_x), 16)
        frame = _duel_result_call_fields(memory, frame, 0x83D4, 0x188DA if side == 0 else 0x1893A)
        frame = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)
        frame = _movement_move_long(state, frame, 'target_y', frame.target_x)
        # Original LSL.L #1, followed by a WORD add, not full-LONG times3.
        value = frame.target_x
        shifted = u32(value << 1)
        flags = (17 if value & 0x80000000 else 0) | (8 if shifted & 0x80000000 else 0) | (4 if shifted == 0 else 0)
        state.sr = (state.sr & 65504) | flags
        frame = first_replace(frame, target_x=shifted, status=flags)
        frame = _movement_add_word(state, frame, 'target_x', low16(frame.target_y))
        frame = _movement_move_long(state, frame, 'target_x', swap_words(frame.target_x))
        frame = _movement_adjust_word(state, frame, 'target_x', 1)
        frame, training = _movement_binary_flags(state, frame, low16(frame.unit), low16(frame.target_x), 16, True)
        frame = first_replace(frame, unit=replace_word(frame.unit, training))
        if frame.status & 1:
            frame = _movement_move(state, frame, 'unit', 0, 16)
        saved = frame.stack_cursor.word()
        frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
        frame = _movement_move(state, frame, 'target_x', saved, 16)
    frame = _duel_result_write_fields(memory, frame,
        u32(frame.roster.base + s16(low16(frame.target_x))), 1, low8(frame.unit))
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    readiness = state.read(0xFFFF810C + side * 2, 2)
    frame = _duel_result_write_fields(memory, frame,
        u32(frame.candidates.base + s16(low16(frame.target_x))), 2, readiness)
    if frame.status & 4:
        frame = _movement_move(state, frame, 'target_y', state.read(donor_address, 2), 16)
        frame = _duel_result_call_fields(memory, frame, 0x189D4, 0x18910 if side == 0 else 0x18970)
        frame = _movement_move(state, frame, 'target_y', state.read(officer_address, 2), 16)
        frame = _duel_result_call_fields(memory, frame, 0x18A54, 0x1891A if side == 0 else 0x1897A)
    return frame


def settle_duel_training_and_troops_fields(memory: BattlePresentationMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """188A6..189D4: both training blocks, real progress children and low troop WORD stores."""
    memory.validate_frame(frame)
    from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
    if frame.stack_cursor is None:
        raise MovementContinuationBoundary(0x188A6, frame, 'actual duel settlement stack required')
    state = memory.state
    frame = first_replace(frame, roster=state.table_at(0xFFFFC500).cursor(),
        candidates=state.table_at(0xFFFFB200).cursor(), controller=state.table_at(0xFFFFC800),
        scan=state.table_at(0xFFFFC000).cursor(), opponent=state.table_at(0xFFFFBE00))
    frame = _duel_training_side_fields(memory, frame, 0)
    frame = _duel_training_side_fields(memory, frame, 1)
    frame = _movement_move(state, frame, 'offset_y', state.read(0xFFFF80E0, 2), 16)
    frame = _movement_move(state, frame, 'choice', state.read(0xFFFF80E2, 2), 16)
    for old_officer, receiver, troops_address, continuation in (
            ('offset_y', 'choice', 0xFFFF8118, 0x189A0),
            ('choice', 'offset_y', 0xFFFF811A, 0x189BA)):
        frame = _movement_move(state, frame, 'target_x', low16(frame.carrier(old_officer)), 16)
        frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
        frame = _movement_move(state, frame, 'unit', frame.controller.word(s16(low16(frame.target_x)), 2), 16)
        frame, difference = _movement_binary_flags(state, frame, low16(frame.unit), state.read(troops_address, 2), 16, True)
        frame = first_replace(frame, unit=replace_word(frame.unit, difference))
        if frame.status & 1:
            frame = _movement_move(state, frame, 'unit', 0, 16)
        frame = _movement_move(state, frame, 'target_x', low16(frame.carrier(receiver)), 16)
        frame = _duel_result_call_fields(memory, frame, 0x18A2E, continuation)
    frame = _movement_fixed_shift_word(state, frame, 'offset_y', 2)
    frame = _movement_fixed_shift_word(state, frame, 'choice', 2)
    for carrier, address in (('offset_y', 0xFFFF8118), ('choice', 0xFFFF811A)):
        frame = _duel_result_write_fields(memory, frame,
            u32(frame.controller.base + s16(low16(frame.carrier(carrier))) + 2), 2, state.read(address, 2))
    return _duel_result_call_fields(memory, frame, 0x18A94, 0x189D2)


def _duel_progress_store_fields(memory, frame: FirstDeploymentFrame,
        offset: Word) -> FirstDeploymentFrame:
    """The two gain rules share only the original add/cap/store, retaining D3 upper WORD."""
    state = memory.state
    frame = _movement_move(state, frame, 'count', frame.scan.word(s16(offset)), 16)
    frame = _movement_add_word(state, frame, 'count', low16(frame.unit))
    frame = _movement_compare(state, frame, low16(frame.count), 999, 16)
    if not frame.status & 5:
        frame = _movement_move(state, frame, 'count', 999, 16)
    return _duel_result_write_fields(memory, frame, u32(frame.scan.base + s16(offset)), 2, low16(frame.count))


def grant_duel_fallback_progress_fields(memory: BattlePresentationMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """189D4..18A2E: live donor and head bonuses; original signed EXT before unsigned divide."""
    memory.validate_frame(frame)
    state = memory.state
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
    frame = _movement_move(state, frame, 'unit', frame.scan.word(s16(low16(frame.target_y))), 16)
    frame = _movement_move_long(state, frame, 'unit', u32(s16(low16(frame.unit))))
    frame = _movement_divu_word(state, frame, 'unit', 40, 0x189DC)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1, True)
    frame = _movement_move(state, frame, 'count', state.read(0xFFFFF68A, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'count', 1)
    frame = first_replace(frame, scratch=state.table_at(0xFFFFF45E))
    frame = _movement_compare(state, frame, low16(frame.target_y), frame.scratch.word(s16(low16(frame.count))), 16)
    head = bool(frame.status & 4)
    if not head:
        frame = first_replace(frame, scratch=state.table_at(0xFFFFA026))
        frame = _movement_compare(state, frame, low16(frame.target_y), frame.scratch.word(s16(low16(frame.count))), 16)
        head = bool(frame.status & 4)
    if head:
        frame = _movement_add_word(state, frame, 'unit', 30)
    frame = first_replace(frame, scratch=state.table_at(0xFFFFC700))
    from .business_battle import _postbattle_bit_fields
    frame = _postbattle_bit_fields(frame, bool(frame.scratch.byte(s16(low16(frame.target_y))) & 16))
    state.sr = (state.sr & 65504) | frame.status
    if not frame.status & 4:
        frame = _movement_add_word(state, frame, 'unit', 20)
    return _duel_progress_store_fields(memory, frame, low16(frame.target_x))


def grant_duel_troop_difference_progress_fields(memory: BattlePresentationMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """18A2E..18A54: zero-extended troop difference divided by100, with live receiver progress."""
    memory.validate_frame(frame)
    state = memory.state
    frame = _movement_move_long(state, frame, 'unit', frame.unit & 65535)
    frame = _movement_divu_word(state, frame, 'unit', 100, 0x18A34)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
    return _duel_progress_store_fields(memory, frame, low16(frame.target_y))


def _duel_result_compact_roster_fields(memory, frame: FirstDeploymentFrame,
        view_role: str='roster') -> FirstDeploymentFrame:
    """One original postincrement compaction for the two actual address roles."""
    if view_role not in ('roster','candidates'):
        raise ValueError('closed original compacted roster role required')
    while True:
        view = frame.roster if view_role == 'roster' else frame.candidates
        word_value = view.word()
        view = view.advance(2)
        frame = first_replace(frame,**{view_role:view})
        frame = _duel_result_write_fields(memory,frame,u32(view.base-4),2,word_value)
        if frame.status & 8:
            return frame


def remove_zero_readiness_duelist_fields(memory: BattlePresentationMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """18A54..18A94: preserve real MOVEM pair and remove first matching live roster entry."""
    memory.validate_frame(frame)
    state = memory.state
    frame = _movement_save_longs(state, frame, ('unit', 'roster'))
    frame = _movement_test(state, frame, state.read(0xFFFFEFE0, 2), 16)
    if not frame.status & 4:
        frame = first_replace(frame, roster=state.table_at(0xFFFFCC00).cursor())
        frame = _duel_result_write_fields(memory, frame,
            u32(frame.roster.base + s16(low16(frame.target_y))), 1, 255)
        frame = first_replace(frame, roster=state.table_at(0xFFFFA550).cursor())
        frame = _movement_compare(state, frame, low16(frame.target_y), state.read(0xFFFFF702, 2), 16)
        if not frame.status & 4:
            frame = first_replace(frame, roster=state.table_at(0xFFFFA5A4).cursor())
        while True:
            value = frame.roster.word()
            frame = first_replace(frame, roster=frame.roster.advance(2))
            frame = _movement_move(state, frame, 'unit', value, 16)
            if frame.status & 8:
                break
            frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 255, 16)
            frame = _movement_compare(state, frame, low16(frame.unit), low16(frame.target_y), 16)
            if frame.status & 4:
                frame = _duel_result_compact_roster_fields(memory, frame)
                break
    return _movement_restore_longs(state, frame, ('unit', 'roster'))


def settle_duel_result_roster_fields(memory: BattlePresentationMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """18A94..18AC6: result6 transfers primary; every other result>=6 selects secondary."""
    memory.validate_frame(frame)
    state = memory.state
    frame = _movement_test(state, frame, state.read(0xFFFFEFE0, 2), 16)
    if frame.status & 4:
        return frame
    frame = _movement_compare(state, frame, state.read(0xFFFF8114, 2), 6, 16)
    if frame.status & 1:
        return frame
    primary = bool(frame.status & 4)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFF80E0 if primary else 0xFFFF80E2, 2), 16)
    return _duel_result_call_fields(memory, frame, 0x18AC6, 0x18AB6 if primary else 0x18AC4)


def transfer_battle_roster_fields(memory: BattlePresentationMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """18AC6..18B00: live source search, shared compaction and negative-terminated retired append."""
    memory.validate_frame(frame)
    state = memory.state
    frame = first_replace(frame, roster=state.table_at(0xFFFFA5A4).cursor(),
        candidates=state.table_at(0xFFFFA57A).cursor())
    frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFFF702, 2), 16)
    if frame.status & 4:
        frame = first_replace(frame, roster=state.table_at(0xFFFFA550).cursor(),
            candidates=state.table_at(0xFFFFA5CE).cursor())
    while True:
        value = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'target_y', value, 16)
        if frame.status & 8:
            return frame
        frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 255, 16)
        frame = _movement_compare(state, frame, low16(frame.target_y), low16(frame.target_x), 16)
        if frame.status & 4:
            break
    frame = _duel_result_compact_roster_fields(memory, frame)
    while True:
        value = frame.candidates.word()
        frame = first_replace(frame, candidates=frame.candidates.advance(2))
        frame = _movement_test(state, frame, value, 16)
        if frame.status & 8:
            break
    frame = _duel_result_write_fields(memory, frame, u32(frame.candidates.base - 2), 2, low16(frame.target_x))
    return _duel_result_write_fields(memory, frame, frame.candidates.base, 2, 65535)


"""Current sole packet settlement and disposition over the existing live state."""


def _duel_result_seek_unbounded_fields(memory, frame: FirstDeploymentFrame,
        view_role: str, carrier: str) -> FirstDeploymentFrame:
    """Original masked-ID search deliberately has no negative-sentinel escape."""
    if (view_role, carrier) not in (('roster', 'target_y'), ('candidates', 'target_y'), ('candidates', 'count')):
        raise ValueError('closed original disposition search role required')
    state = memory.state
    while True:
        view = frame.roster if view_role == 'roster' else frame.candidates
        value = view.word()
        frame = first_replace(frame, **{view_role:view.advance(2)})
        frame = _movement_move(state, frame, carrier, value, 16)
        frame = _movement_move(state, frame, carrier, low16(frame.carrier(carrier)) & 255, 16)
        frame = _movement_compare(state, frame, low16(frame.carrier(carrier)), low16(frame.target_x), 16)
        if frame.status & 4:
            return frame


def _duel_result_append_retired_fields(memory, frame: FirstDeploymentFrame,
        view_role: str) -> FirstDeploymentFrame:
    """Live negative-terminated append, with actual TST postincrement and no saved snapshot."""
    if view_role not in ('roster', 'candidates'):
        raise ValueError('closed original retired roster required')
    while True:
        view = frame.roster if view_role == 'roster' else frame.candidates
        value = view.word()
        view = view.advance(2)
        frame = first_replace(frame, **{view_role:view})
        frame = _movement_test(memory.state, frame, value, 16)
        if frame.status & 8:
            break
    frame = _duel_result_write_fields(memory, frame, u32(view.base - 2), 2, low16(frame.target_x))
    return _duel_result_write_fields(memory, frame, view.base, 2, 65535)


def settle_duel_packets_fields(memory: BattlePresentationMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """18B00..18B94: readiness routing, two dispositions, zero-ready removal and true carry result."""
    memory.validate_frame(frame)
    state = memory.state
    frame = first_replace(frame, roster=state.table_at(0x00FF7050).cursor(),
        candidates=state.table_at(0x00FF70A0).cursor(), controller=state.table_at(0x00FF70F0),
        scan=state.table_at(0x00FF70F1).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0x00FF706A, 2), 16)
    frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFF80E0, 2), 16)
    if not frame.status & 4:
        frame = first_replace(frame, roster=frame.candidates, candidates=frame.roster,
            controller=state.table_at(frame.scan.base), scan=state.table_at(frame.controller.base).cursor())
    frame = _duel_result_write_fields(memory, frame, 0xFFFF810C, 2, frame.roster.word(0, 28))
    frame = _duel_result_write_fields(memory, frame, 0xFFFF810E, 2, frame.candidates.word(0, 28))
    frame = _movement_move(state, frame, 'target_x', state.read(0x00FF706A, 2), 16)
    frame = _movement_move(state, frame, 'target_y', state.read(0x00FF70BA, 2), 16)
    frame = _movement_move(state, frame, 'unit', state.read(0x00FF70F0, 1), 8)
    if not frame.status & 4:
        frame = _duel_result_call_fields(memory, frame, 0x18B94, 0x18B56)
    frame = first_replace(frame, target_x=frame.target_y, target_y=frame.target_x)
    frame = _movement_move(state, frame, 'unit', state.read(0x00FF70F1, 1), 8)
    if not frame.status & 4:
        frame = _duel_result_call_fields(memory, frame, 0x18B94, 0x18B66)
    frame = _movement_compare(state, frame, state.read(0x00FF70F0, 1), 1, 8)
    blocked = bool(frame.status & 4)
    if not blocked:
        frame = _movement_compare(state, frame, state.read(0x00FF70F1, 1), 1, 8)
        blocked = bool(frame.status & 4)
    if not blocked:
        frame = _duel_result_call_fields(memory, frame, 0x18C56, 0x18B82)
        frame = _duel_result_call_fields(memory, frame, 0x188A6, 0x18B86)
        state.sr &= 65534
    else:
        state.sr |= 1
    return first_replace(frame, status=state.sr & 31)


def apply_duel_disposition_fields(memory: BattlePresentationMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """18B94..18C56: exact live disposition order; four saved LONGs are read back from RAM."""
    memory.validate_frame(frame)
    state = memory.state
    saved = ('target_x', 'target_y', 'roster', 'candidates')
    frame = _movement_save_longs(state, frame, saved)
    frame = _movement_test(state, frame, state.read(0xFFFFEFE0, 2), 16)
    if frame.status & 4:
        frame = _movement_compare(state, frame, low8(frame.unit), 3, 8)
        if not frame.status & 4:
            frame = _movement_move(state, frame, 'target_y', 6, 16)
            frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFF80E0, 2), 16)
            if not frame.status & 4:
                frame = _movement_move(state, frame, 'target_y', 7, 16)
            frame = _duel_result_write_fields(memory, frame, 0xFFFF8114, 2, low16(frame.target_y))
        return _movement_restore_longs(state, frame, saved)
    frame = _movement_compare(state, frame, low8(frame.unit), 2, 8)
    transfer = bool(frame.status & 4)
    if transfer:
        frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFFF702, 2), 16)
        primary = bool(frame.status & 4)
        frame = first_replace(frame, roster=state.table_at(0xFFFFA550 if primary else 0xFFFFA5A4).cursor(),
            candidates=state.table_at(0xFFFFA5CE if primary else 0xFFFFA57A).cursor())
        frame = _duel_result_seek_unbounded_fields(memory, frame, 'roster', 'target_y')
        frame = _duel_result_compact_roster_fields(memory, frame)
        frame = _duel_result_append_retired_fields(memory, frame, 'candidates')
    else:
        frame = _movement_compare(state, frame, low8(frame.unit), 3, 8)
        if frame.status & 4:
            frame = first_replace(frame, roster=state.table_at(0xFFFFA5CE).cursor(),
                candidates=state.table_at(0xFFFFA550).cursor())
            frame = _movement_move(state, frame, 'count', state.read(0xFFFFF68A, 2), 16)
            frame = _movement_move(state, frame, 'count', low16(frame.count) | 128, 16)
            frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFFF702, 2), 16)
            if not frame.status & 4:
                frame = _movement_move(state, frame, 'count', low16(frame.count) | 64, 16)
                frame = first_replace(frame, roster=state.table_at(0xFFFFA57A).cursor(),
                    candidates=state.table_at(0xFFFFA5A4).cursor())
            frame = _duel_result_append_retired_fields(memory, frame, 'roster')
            frame = _duel_result_seek_unbounded_fields(memory, frame, 'candidates', 'count')
            frame = _duel_result_compact_roster_fields(memory, frame, 'candidates')
    return _movement_restore_longs(state, frame, saved)


def detach_zero_readiness_duelists_fields(memory: BattlePresentationMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """18C56..18C88: each actual packet readiness is re-read before its independent detach child."""
    memory.validate_frame(frame)
    state = memory.state
    frame = _movement_test(state, frame, state.read(0xFFFFEFE0, 2), 16)
    if frame.status & 4:
        return frame
    for readiness, officer, continuation in ((0x00FF706C, 0x00FF706A, 0x18C72),
            (0x00FF70BC, 0x00FF70BA, 0x18C86)):
        frame = _movement_test(state, frame, state.read(readiness, 2), 16)
        if frame.status & 4:
            frame = _movement_move(state, frame, 'target_x', state.read(officer, 2), 16)
            frame = _duel_result_call_fields(memory, frame, 0x18C88, continuation)
    return frame


def detach_defeated_duelist_fields(memory: BattlePresentationMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """18C88..18CB4: assignmentFF, exact side choice and original unbounded masked search."""
    memory.validate_frame(frame)
    state = memory.state
    frame = first_replace(frame, roster=state.table_at(0xFFFFCC00).cursor())
    frame = _duel_result_write_fields(memory, frame,
        u32(frame.roster.base + s16(low16(frame.target_x))), 1, 255)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFA550).cursor())
    frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFFF702, 2), 16)
    if not frame.status & 4:
        frame = first_replace(frame, candidates=state.table_at(0xFFFFA5A4).cursor())
    frame = _duel_result_seek_unbounded_fields(memory, frame, 'candidates', 'target_y')
    return _duel_result_compact_roster_fields(memory, frame, 'candidates')

# D52 sole full calendar/economy fields; frozen historical owners remain untouched.
from .contexts_services import SceneRefreshMemory, SceneRefreshBoundary
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame, first_replace
from ..high_level_battle_ai.business_formation import (
    _first_word, _first_byte, _first_long, _first_add_word, _first_sub_word,
    _first_shift_word, _first_right_word, _first_compare_word, _first_compare_long,
)
from ..high_level_main_flows.business_movement_support import (
    _movement_binary_flags, _movement_save_longs, _movement_restore_longs,
    _movement_multiply_word, _movement_arithmetic_long,
)
from ..high_level_scene_flows.domain import (
    u8,u16,u32,s16,low8,low16,replace_byte,replace_word,swap_words,divu_retained,
)
def _calendar_frame_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        entry: int) -> FirstDeploymentFrame:
    if type(memory) is not SceneRefreshMemory:
        raise ValueError('one existing Scene/gameplay calendar memory required')
    memory.frame(frame)
    from ..high_level_scene_flows.domain import SceneState
    if type(memory.state) is SceneState:
        if frame.stack_cursor is None:
            raise SceneRefreshBoundary(entry,frame,None)
        frame.validate(memory.state,True)
    elif frame.stack_cursor is None or frame.status is None:
        # Historical scalar APIs have no actual CPU stack/X observation. They
        # project here without manufacturing a complete execution context.
        raise SceneRefreshBoundary(entry,frame,None)
    return frame
def _calendar_value_fields(frame: FirstDeploymentFrame, carrier: str) -> int:
    value=frame.carrier(carrier)
    if value is None:
        raise SceneRefreshBoundary(0x16B3A,frame,None)
    return value
def _calendar_move_fields(memory,frame,carrier,value,width=2):
    if width==1:frame=_first_byte(frame,carrier,value)
    elif width==2:frame=_first_word(frame,carrier,value)
    elif width==4:frame=_first_long(frame,carrier,value)
    else:raise ValueError('actual calendar operand width required')
    return memory.sync_status(frame)
def _calendar_test_fields(memory,frame,value,width=2):
    from .business_services import _scene_refresh_flags
    return _scene_refresh_flags(memory,frame,value,width)
def _calendar_write_fields(memory,frame,address,value,width=2,clear=False):
    from .business_services import _scene_refresh_emit
    if clear:memory.state.read(address,width)
    return _scene_refresh_emit(memory,frame,address,width,value)
def _calendar_compare_fields(memory,frame,left,right,width=2):
    if width==1:
        from .business_battle import _postbattle_compare_byte_fields
        frame=_postbattle_compare_byte_fields(frame,left,right)
    elif width==2:frame=_first_compare_word(frame,left,right)
    elif width==4:frame=_first_compare_long(frame,left,right)
    else:raise ValueError('actual calendar comparison width required')
    return memory.sync_status(frame)
def _calendar_arithmetic_fields(memory,frame,carrier,operand,width=2,subtract=False):
    previous=_calendar_value_fields(frame,carrier)
    frame,value=_movement_binary_flags(memory.state,frame,previous&((1<<(width*8))-1),operand,width*8,subtract)
    retained=replace_byte(previous,value) if width==1 else replace_word(previous,value) if width==2 else value
    return first_replace(frame,**{carrier:retained})
def _calendar_memory_arithmetic_fields(memory,frame,address,operand,width=2,subtract=False):
    previous=memory.state.read(address,width)
    frame,value=_movement_binary_flags(memory.state,frame,previous,operand,width*8,subtract)
    memory.state.write(address,width,value)
    return frame
def _calendar_shift_fields(memory,frame,carrier,amount,right=False,arithmetic=False):
    original=low16(_calendar_value_fields(frame,carrier))
    if arithmetic:
        from ..high_level_main_flows.business_gameplay import _setup_asl_word_fields
        if carrier=='choice' and amount==2:
            projected=first_replace(frame,target_x=frame.choice)
            shifted=_setup_asl_word_fields(memory.state,projected,'target_x',2)
            frame=first_replace(frame,choice=shifted.target_x,status=shifted.status)
        else:frame=_setup_asl_word_fields(memory.state,frame,carrier,amount)
    elif amount==0:return _calendar_test_fields(memory,frame,original)
    elif right:frame=_first_right_word(frame,carrier,original,amount)
    else:frame=_first_shift_word(frame,carrier,original,amount)
    return memory.sync_status(frame)
def _calendar_swap_fields(memory,frame,carrier):
    return _calendar_move_fields(memory,frame,carrier,swap_words(_calendar_value_fields(frame,carrier)),4)
def _calendar_bit_fields(memory,frame,value,mask):
    from .business_battle import _postbattle_bit_fields
    return memory.sync_status(_postbattle_bit_fields(frame,bool(value&mask)))
def _calendar_db_fields(frame,carrier):
    remaining_word=u16(low16(_calendar_value_fields(frame,carrier))-1)
    return first_replace(frame,**{carrier:replace_word(frame.carrier(carrier),remaining_word)}),remaining_word!=65535
def _calendar_save_fields(memory,frame,names):
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x16F42,frame,None)
    return _movement_save_longs(memory.state,frame,names)
def _calendar_restore_fields(memory,frame,names):
    return _movement_restore_longs(memory.state,frame,names)
def _calendar_push_word_fields(memory,frame,value):
    if frame.stack_cursor is None:raise SceneRefreshBoundary(0x16B3E,frame,None)
    stack=frame.stack_cursor.advance(-2);stack.set_word(0,value)
    frame=first_replace(frame,stack_cursor=stack)
    return _calendar_test_fields(memory,frame,value)
def _calendar_pop_word_fields(memory,frame,address):
    value=frame.stack_cursor.word()
    frame=first_replace(frame,stack_cursor=frame.stack_cursor.advance(2))
    return _calendar_write_fields(memory,frame,address,value)
def _calendar_divu_fields(memory,frame,carrier,divisor,pc,discarded=False):
    previous=_calendar_value_fields(frame,carrier)
    if divisor==0:raise SceneRefreshBoundary(pc,frame,None)
    quotient=previous//divisor
    result=divu_retained(previous,divisor)
    if quotient>65535:
        # Only fixed sites whose next original operation overwrites NZVC can
        # consume the retained dividend. No undefined DIVU flag is exported.
        if not discarded or pc not in (0x16C0E,0x16C86,0x16D7A,0x16DA0,0x17482,0x16E9A):
            raise SceneRefreshBoundary(pc,frame,None)
        return first_replace(frame,**{carrier:result})
    frame=first_replace(frame,**{carrier:result})
    return _calendar_test_fields(memory,frame,quotient)
def _calendar_call_fields(memory,frame,target,token):
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(target,frame,token)
    stack=frame.stack_cursor.advance(-4);stack.set_long(0,token)
    entered=first_replace(frame,stack_cursor=stack)
    result=_calendar_child_fields(memory,entered,target)
    memory.frame(result)
    actual=result.stack_cursor.long()
    if actual!=token:raise SceneRefreshBoundary(actual,result,token)
    return memory.sync_status(first_replace(result,stack_cursor=result.stack_cursor.advance(4)))
def _calendar_child_fields(memory,frame,target):
    from .business_calendar import (
        process_calendar_city_cycle_fields,scan_calendar_officer_mortality_fields,
        remove_mortal_officer_with_message_fields,choose_city_head_after_mortality_fields,
        process_calendar_event_schedulers_fields,show_calendar_event_message_fields,
        process_first_calendar_event_fields,show_first_calendar_event_values_fields,
        process_second_calendar_event_fields,show_second_calendar_event_values_fields,
        process_third_calendar_event_fields,show_third_calendar_event_values_fields,
    )
    own={0x16BB8:replenish_b200_troops_fields,0x16C0A:grow_original_long_field_fields,
        0x16C2C:credit_primary_fields,0x16C46:credit_secondary_fields,
        0x16C5C:commit_income_fields,0x16C72:scaled_income_fields,
        0x16C98:deplete_income_fields,0x16D10:debit_primary_fields,
        0x16D2A:debit_secondary_fields,0x16D40:settle_expense_fields,
        0x16DEA:settle_shortage_fields,0x17016:reset_queue_fields,0x17026:append_queue_fields,
        0x171A6:submit_calendar_three_fields,0x17342:submit_calendar_four_fields,
        0x17474:submit_calendar_classified_fields,0x17514:scale_e1e0_fields,
        0x1752A:scale_e140_fields,0x17540:scale_e320_fields,0x17556:scale_e000_fields,
        0x1756C:scale_e0a0_fields,0x17582:scale_e5a0_fields,
        0x17598:sample_once_fields,0x175A8:sample_small_fields,0x175C2:sample_wide_fields,
        0x175DC:wrapped_product_fields,0x175EC:divide_percent_fields}
    calendar={0x16B3A:process_calendar_city_cycle_fields,0x16EDA:scan_calendar_officer_mortality_fields,
        0x16F42:remove_mortal_officer_with_message_fields,0x16FDA:choose_city_head_after_mortality_fields,
        0x16FFC:process_calendar_event_schedulers_fields,0x17058:show_calendar_event_message_fields,
        0x1707E:process_first_calendar_event_fields,0x17158:show_first_calendar_event_values_fields,
        0x171FC:process_second_calendar_event_fields,0x172F4:show_second_calendar_event_values_fields,
        0x173A6:process_third_calendar_event_fields,0x17426:show_third_calendar_event_values_fields}
    if target in own:return own[target](memory,frame)
    if target in calendar:return calendar[target](memory,frame)
    if target==0x83D4:
        from .business_battle import _presentation_random_fields
        from .contexts_battle import BattlePresentationMemory
        return _presentation_random_fields(BattlePresentationMemory(memory.state),frame)
    if target in (0x5F48,0xE1F6):
        from .business_battle import build_roster_fields,choose_city_head_fields
        from .contexts_battle import BattlePresentationMemory
        algorithm=build_roster_fields if target==0x5F48 else choose_city_head_fields
        return algorithm(BattlePresentationMemory(memory.state),frame)
    if target==0x35760:
        from ..high_level_main_flows.business_movement_support import signed_divmod_fields
        return signed_divmod_fields(memory.state,frame)
    if target in (0xAF48,0x1072C,0x30A74):
        from .business_services import refresh_gameplay_scene_fields,load_gameplay_scene_fields,present_gameplay_message_fields
        algorithm=refresh_gameplay_scene_fields if target==0xAF48 else load_gameplay_scene_fields if target==0x1072C else present_gameplay_message_fields
        return algorithm(memory,frame)
    raise SceneRefreshBoundary(target,frame,None)
def replenish_b200_troops_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x16BB8)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFFEA37),candidates=memory.cursor_at(0xFFFFCC00),
        controller=memory.cursor_at(0xFFFFB000),scan=memory.cursor_at(0xFFFFB200))
    frame=_calendar_move_fields(memory,frame,'target_x',255)
    while True:
        frame=_calendar_move_fields(memory,frame,'target_y',frame.candidates.byte(low16(frame.target_x)),1)
        frame=_calendar_compare_fields(memory,frame,low16(frame.target_y),40)
        if not frame.status&1 and not frame.status&4:
            pass
        else:
            frame=_calendar_test_fields(memory,frame,frame.roster.byte(low16(frame.target_y)),1)
            if frame.status&4:
                frame=_calendar_move_fields(memory,frame,'target_y',low16(frame.target_x))
                frame=_calendar_shift_fields(memory,frame,'target_y',1)
                frame=_calendar_move_fields(memory,frame,'unit',frame.controller.word(low16(frame.target_y)))
                frame=_calendar_move_fields(memory,frame,'count',low16(frame.unit))
                frame=_movement_multiply_word(memory.state,frame,'unit',15)
                frame=_calendar_divu_fields(memory,frame,'unit',100,0x16BEE)
                frame=_calendar_move_fields(memory,frame,'distance',frame.scan.word(low16(frame.target_y)))
                frame=_calendar_arithmetic_fields(memory,frame,'distance',low16(frame.unit))
                frame=_calendar_compare_fields(memory,frame,low16(frame.distance),low16(frame.count))
                if not frame.status&1 and not frame.status&4:
                    frame=_calendar_move_fields(memory,frame,'distance',low16(frame.count))
                frame=_calendar_write_fields(memory,frame,frame.scan.address(low16(frame.target_y)),low16(frame.distance))
        frame,again=_calendar_db_fields(frame,'target_x')
        if not again:return frame
def grow_original_long_field_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x16C0A)
    frame=_calendar_move_fields(memory,frame,'target_y',frame.roster.long(),4)
    frame=_calendar_move_fields(memory,frame,'unit',frame.target_y,4)
    frame=_calendar_divu_fields(memory,frame,'unit',100,0x16C0E,True)
    frame=_calendar_move_fields(memory,frame,'unit',frame.unit&65535,4)
    frame=_calendar_arithmetic_fields(memory,frame,'target_y',frame.unit,4)
    frame=_calendar_compare_fields(memory,frame,frame.target_y,1000,4)
    if not frame.status&1 and not frame.status&4:
        frame=_calendar_move_fields(memory,frame,'target_y',1000,4)
    return _calendar_write_fields(memory,frame,frame.roster.base,frame.target_y,4)
def credit_primary_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x16C2C)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFFE280),scan=memory.cursor_at(0xFFFFE000))
    frame=_calendar_move_fields(memory,frame,'target_y',low16(frame.target_x))
    frame=_calendar_shift_fields(memory,frame,'target_y',2)
    frame=_calendar_move_fields(memory,frame,'choice',100)
    frame=_calendar_arithmetic_fields(memory,frame,'choice',frame.roster.word(low16(frame.target_y),2),subtract=True)
    return _calendar_call_fields(memory,frame,0x16C5C,0x16C44)
def credit_secondary_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x16C46)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFFE280))
    frame=_calendar_move_fields(memory,frame,'target_y',low16(frame.target_x))
    frame=_calendar_shift_fields(memory,frame,'target_y',2)
    frame=_calendar_move_fields(memory,frame,'choice',frame.roster.long(low16(frame.target_y)),4)
    frame=first_replace(frame,scan=memory.cursor_at(0xFFFFE0A0))
    return _calendar_call_fields(memory,frame,0x16C5C,0x16C5A)
def commit_income_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x16C5C)
    frame=_calendar_call_fields(memory,frame,0x16C72,0x16C60)
    frame=_calendar_arithmetic_fields(memory,frame,'count',frame.scan.long(low16(frame.target_y)),4)
    if frame.status&1:frame=_calendar_move_fields(memory,frame,'count',0xFFFFFFFF,4)
    frame=_calendar_write_fields(memory,frame,frame.scan.address(low16(frame.target_y)),frame.count,4)
    return _calendar_call_fields(memory,frame,0x16C98,0x16C70)
def scaled_income_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x16C72)
    frame=first_replace(frame,candidates=memory.cursor_at(0xFFFFE1E0),controller=memory.cursor_at(0xFFFFE3C0),
        scratch=memory.cursor_at(0xFFFFE140))
    frame=_movement_multiply_word(memory.state,frame,'choice',frame.controller.word(low16(frame.target_y),2))
    frame=_movement_multiply_word(memory.state,frame,'choice',frame.candidates.word(low16(frame.target_y),2))
    frame=_calendar_divu_fields(memory,frame,'choice',15000,0x16C86,True)
    frame=_calendar_move_fields(memory,frame,'count',frame.scratch.long(low16(frame.target_y)),4)
    frame=_calendar_move_fields(memory,frame,'count',frame.count&65535,4)
    return _movement_multiply_word(memory.state,frame,'count',low16(frame.choice))
def deplete_income_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x16C98)
    frame=_calendar_move_fields(memory,frame,'target_y',low16(frame.target_x))
    frame=_calendar_shift_fields(memory,frame,'target_y',2)
    frame=_calendar_move_fields(memory,frame,'unit',frame.controller.long(low16(frame.target_y)),4)
    frame=_calendar_move_fields(memory,frame,'count',0)
    frame=_calendar_compare_fields(memory,frame,low16(frame.unit),45)
    if frame.status&(1|4):return frame
    for threshold in (55,65,75,85):
        frame=_calendar_compare_fields(memory,frame,low16(frame.unit),threshold)
        if frame.status&(1|4):break
        frame=_calendar_arithmetic_fields(memory,frame,'count',4)
    frame=_calendar_move_fields(memory,frame,'unit',low16(frame.target_x))
    frame=_calendar_call_fields(memory,frame,0x83D4,0x16CD0)
    frame=_calendar_move_fields(memory,frame,'target_x',low16(frame.unit))
    frame=first_replace(frame,candidates=memory.cursor_at(0x16CFC))
    frame=_calendar_move_fields(memory,frame,'unit',frame.candidates.word(low16(frame.count)))
    frame=_movement_multiply_word(memory.state,frame,'unit',memory.state.read(0xFFFFF61C,2))
    frame=_calendar_swap_fields(memory,frame,'unit')
    frame=_calendar_arithmetic_fields(memory,frame,'unit',frame.candidates.word(low16(frame.count),2))
    frame=first_replace(frame,controller=memory.cursor_at(0xFFFFE320))
    frame=_calendar_move_fields(memory,frame,'target_y',low16(frame.target_x))
    frame=_calendar_shift_fields(memory,frame,'target_y',2)
    frame=_calendar_move_fields(memory,frame,'count',frame.controller.word(low16(frame.target_y),2))
    frame=_movement_multiply_word(memory.state,frame,'count',low16(frame.unit))
    frame=_calendar_divu_fields(memory,frame,'count',100,0x16CF2)
    return _calendar_memory_arithmetic_fields(memory,frame,frame.controller.address(low16(frame.target_y),2),
        low16(frame.count),subtract=True)
def debit_primary_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x16D10)
    frame=first_replace(frame,scan=memory.cursor_at(0xFFFFE280))
    frame=_calendar_move_fields(memory,frame,'choice',100)
    frame=_calendar_move_fields(memory,frame,'count',low16(frame.target_x))
    frame=_calendar_shift_fields(memory,frame,'count',2)
    frame=_calendar_arithmetic_fields(memory,frame,'choice',frame.scan.word(low16(frame.count),2),subtract=True)
    frame=first_replace(frame,scratch=memory.cursor_at(0xFFFFE000))
    return _calendar_call_fields(memory,frame,0x16D40,0x16D28)
def debit_secondary_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x16D2A)
    frame=first_replace(frame,scan=memory.cursor_at(0xFFFFE280))
    frame=_calendar_move_fields(memory,frame,'target_y',low16(frame.target_x))
    frame=_calendar_shift_fields(memory,frame,'target_y',2)
    frame=_calendar_move_fields(memory,frame,'choice',frame.scan.word(low16(frame.target_y),2))
    frame=first_replace(frame,scratch=memory.cursor_at(0xFFFFE0A0))
    return _calendar_call_fields(memory,frame,0x16D40,0x16D3E)
def settle_expense_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    """City payroll plus class weights, including the original shortage branch."""
    frame=_calendar_frame_fields(memory,frame,0x16D40)
    frame=first_replace(frame,opponent=memory.cursor_at(0xFFFFC700))
    frame=_calendar_arithmetic_fields(memory,frame,'target_x',1)
    frame=_calendar_write_fields(memory,frame,0xFFFFF630,65535)
    frame=_calendar_call_fields(memory,frame,0x5F48,0x16D52)
    frame=_calendar_write_fields(memory,frame,0xFFFFF636,low16(frame.count))
    frame=_calendar_arithmetic_fields(memory,frame,'target_x',1,subtract=True)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFFC800),candidates=memory.cursor_at(0xFFFFF500))
    frame=_calendar_move_fields(memory,frame,'target_y',0,4)
    while True:
        frame=_calendar_move_fields(memory,frame,'unit',frame.candidates.word())
        frame=first_replace(frame,candidates=frame.candidates.advance(2))
        if frame.status&8:break
        frame=_calendar_shift_fields(memory,frame,'unit',2)
        frame=_calendar_arithmetic_fields(memory,frame,'target_y',frame.roster.long(low16(frame.unit)),4)
    frame=_calendar_move_fields(memory,frame,'count',frame.target_y,4)
    frame=_movement_multiply_word(memory.state,frame,'target_y',low16(frame.choice))
    frame=_calendar_swap_fields(memory,frame,'count')
    frame=_movement_multiply_word(memory.state,frame,'count',low16(frame.choice))
    frame=_calendar_swap_fields(memory,frame,'count')
    frame=_calendar_arithmetic_fields(memory,frame,'target_y',frame.count,4)
    frame=_calendar_divu_fields(memory,frame,'target_y',5000,0x16D7A,True)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFFF500),candidates=memory.cursor_at(0x16DE0))
    frame=_calendar_move_fields(memory,frame,'unit',0)
    while True:
        frame=_calendar_move_fields(memory,frame,'count',frame.roster.word())
        frame=first_replace(frame,roster=frame.roster.advance(2))
        if frame.status&8:break
        frame=_calendar_move_fields(memory,frame,'distance',frame.opponent.byte(low16(frame.count)),1)
        frame=_calendar_move_fields(memory,frame,'distance',low16(frame.distance)&5)
        frame=_calendar_shift_fields(memory,frame,'distance',1)
        frame=_calendar_arithmetic_fields(memory,frame,'unit',frame.candidates.word(low16(frame.distance)))
    frame=_movement_multiply_word(memory.state,frame,'unit',low16(frame.choice))
    frame=_calendar_divu_fields(memory,frame,'unit',100,0x16DA0,True)
    frame=_calendar_move_fields(memory,frame,'target_y',frame.target_y&65535,4)
    frame=_calendar_move_fields(memory,frame,'unit',frame.unit&65535,4)
    frame=_calendar_arithmetic_fields(memory,frame,'unit',frame.target_y,4)
    frame=_calendar_move_fields(memory,frame,'count',low16(frame.target_x))
    frame=_calendar_shift_fields(memory,frame,'count',2)
    frame=_calendar_move_fields(memory,frame,'distance',frame.scratch.long(low16(frame.count)),4)
    frame=_calendar_arithmetic_fields(memory,frame,'distance',frame.unit,4,True)
    if frame.status&1:
        frame=_calendar_call_fields(memory,frame,0x16DEA,0x16DC4)
        frame=_calendar_move_fields(memory,frame,'distance',0,4)
    else:
        frame=_calendar_compare_fields(memory,frame,frame.distance,999999,4)
        if not frame.status&(1|4):frame=_calendar_move_fields(memory,frame,'distance',999999,4)
    frame=_calendar_move_fields(memory,frame,'count',low16(frame.target_x))
    frame=_calendar_shift_fields(memory,frame,'count',2)
    return _calendar_write_fields(memory,frame,frame.scratch.address(low16(frame.count)),frame.distance,4)
def settle_shortage_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    """Sort poor officers first, consume holdings, then reduce remaining loyalty."""
    frame=_calendar_frame_fields(memory,frame,0x16DEA)
    previous=frame.distance
    frame,value=_movement_binary_flags(memory.state,frame,0,previous,32,True)
    frame=first_replace(frame,distance=value)
    frame=_calendar_move_fields(memory,frame,'offset_x',frame.distance,4)
    frame=_movement_multiply_word(memory.state,frame,'distance',low16(frame.choice))
    frame=_calendar_swap_fields(memory,frame,'offset_x')
    frame=_movement_multiply_word(memory.state,frame,'offset_x',low16(frame.choice))
    frame=_calendar_swap_fields(memory,frame,'offset_x')
    frame=_calendar_arithmetic_fields(memory,frame,'distance',frame.offset_x,4)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFFF500),candidates=memory.cursor_at(0xFFFFEA60),
        controller=memory.cursor_at(0xFFFFBE00),scan=memory.cursor_at(0xFFFFC000))
    while True:
        frame=_calendar_move_fields(memory,frame,'target_y',frame.roster.word())
        frame=first_replace(frame,roster=frame.roster.advance(2))
        if frame.status&8:break
        frame=_calendar_move_fields(memory,frame,'unit',0,4)
        frame=_calendar_shift_fields(memory,frame,'target_y',1)
        frame=_calendar_move_fields(memory,frame,'unit',frame.controller.word(low16(frame.target_y)))
        frame=_calendar_move_fields(memory,frame,'count',0,4)
        frame=_calendar_move_fields(memory,frame,'count',frame.scan.word(low16(frame.target_y)))
        frame=_calendar_arithmetic_fields(memory,frame,'count',frame.unit,4)
        frame=_calendar_write_fields(memory,frame,frame.candidates.base,frame.count,4)
        frame=first_replace(frame,candidates=frame.candidates.advance(4))
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFFEA60),candidates=memory.cursor_at(0xFFFFF500))
    frame=_calendar_move_fields(memory,frame,'target_y',memory.state.read(0xFFFFF636,2))
    frame=_calendar_compare_fields(memory,frame,low16(frame.target_y),1)
    if not frame.status&(1|4):
        frame=_calendar_arithmetic_fields(memory,frame,'target_y',1,subtract=True)
        while True:
            for carrier in ('unit','count','offset_x'):frame=_calendar_move_fields(memory,frame,carrier,0)
            while True:
                frame=_calendar_move_fields(memory,frame,'offset_y',frame.roster.long(low16(frame.offset_x)),4)
                frame=_calendar_compare_fields(memory,frame,frame.offset_y,frame.roster.long(low16(frame.offset_x),4),4)
                if not frame.status&(1|4):
                    frame=_calendar_write_fields(memory,frame,frame.roster.address(low16(frame.offset_x)),
                        frame.roster.long(low16(frame.offset_x),4),4)
                    frame=_calendar_write_fields(memory,frame,frame.roster.address(low16(frame.offset_x),4),frame.offset_y,4)
                    frame=_calendar_move_fields(memory,frame,'offset_y',frame.candidates.word(low16(frame.count)))
                    frame=_calendar_write_fields(memory,frame,frame.candidates.address(low16(frame.count)),
                        frame.candidates.word(low16(frame.count),2))
                    frame=_calendar_write_fields(memory,frame,frame.candidates.address(low16(frame.count),2),low16(frame.offset_y))
                frame=_calendar_arithmetic_fields(memory,frame,'unit',1)
                frame=_calendar_arithmetic_fields(memory,frame,'count',2)
                frame=_calendar_arithmetic_fields(memory,frame,'offset_x',4)
                frame=_calendar_compare_fields(memory,frame,low16(frame.unit),low16(frame.target_y))
                if not frame.status&1:break
            frame=_calendar_arithmetic_fields(memory,frame,'target_y',1,subtract=True)
            if frame.status&4:break
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFFF500),candidates=memory.cursor_at(0xFFFFC800),
        controller=memory.cursor_at(0xFFFFC200))
    while True:
        frame=_calendar_move_fields(memory,frame,'target_y',frame.roster.word())
        frame=first_replace(frame,roster=frame.roster.advance(2))
        if frame.status&8:break
        frame=_calendar_move_fields(memory,frame,'count',low16(frame.target_y))
        frame=_calendar_shift_fields(memory,frame,'count',2)
        frame=_calendar_move_fields(memory,frame,'unit',frame.candidates.long(low16(frame.count)),4)
        frame=_calendar_compare_fields(memory,frame,frame.unit,frame.distance,4)
        if not frame.status&(1|4):
            frame=_calendar_move_fields(memory,frame,'offset_y',frame.distance,4)
            # Original CLR.W, not CLR.L: a high-word deficit is deliberately retained.
            frame=_calendar_move_fields(memory,frame,'distance',0)
        else:
            frame=_calendar_arithmetic_fields(memory,frame,'distance',frame.unit,4,True)
            frame=_calendar_move_fields(memory,frame,'offset_y',frame.unit,4)
        frame=_calendar_move_fields(memory,frame,'offset_x',100)
        frame=_calendar_arithmetic_fields(memory,frame,'offset_x',frame.controller.byte(low16(frame.target_y)),1,True)
        frame=_movement_multiply_word(memory.state,frame,'offset_y',low16(frame.offset_x))
        frame=_calendar_divu_fields(memory,frame,'offset_y',100,0x16E9A,True)
        frame=_calendar_move_fields(memory,frame,'offset_y',frame.offset_y&65535,4)
        frame=_calendar_arithmetic_fields(memory,frame,'unit',frame.offset_y,4,True)
        frame=_calendar_write_fields(memory,frame,frame.candidates.address(low16(frame.count)),frame.unit,4)
        frame=_calendar_test_fields(memory,frame,frame.distance,4)
        if frame.status&4:break
    frame=_calendar_test_fields(memory,frame,frame.distance,4)
    if frame.status&4:return frame
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFFF500),candidates=memory.cursor_at(0xFFFFC200),
        controller=memory.cursor_at(0xFFFFC300))
    while True:
        frame=_calendar_move_fields(memory,frame,'target_y',frame.roster.word())
        frame=first_replace(frame,roster=frame.roster.advance(2))
        if frame.status&8:return frame
        frame=_calendar_move_fields(memory,frame,'unit',100,4)
        frame=_calendar_arithmetic_fields(memory,frame,'unit',frame.candidates.byte(low16(frame.target_y)),1,True)
        frame=_calendar_divu_fields(memory,frame,'unit',10,0x16EC8)
        frame=_calendar_memory_arithmetic_fields(memory,frame,frame.controller.address(low16(frame.target_y)),
            low8(frame.unit),1,True)
        if frame.status&1:frame=_calendar_write_fields(memory,frame,frame.controller.address(low16(frame.target_y)),0,1,True)
def reset_queue_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x17016)
    frame=_calendar_move_fields(memory,frame,'target_x',41,4)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFFD420))
    while True:
        frame=_calendar_write_fields(memory,frame,frame.roster.base,255,1)
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame,again=_calendar_db_fields(frame,'target_x')
        if not again:return frame
def append_queue_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    """Append at the actual FF sentinel; no invented queue capacity limit."""
    frame=_calendar_frame_fields(memory,frame,0x17026)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFFF428))
    frame=_calendar_move_fields(memory,frame,'target_x',frame.roster.byte(low16(frame.choice)),1)
    if not frame.status&8:
        for address in (0xFFFFF67A,0xFFFFF67C,0xFFFFF67E):
            frame=_calendar_compare_fields(memory,frame,low16(frame.target_x),memory.state.read(address,2))
            if frame.status&4:
                frame=_calendar_write_fields(memory,frame,0xFFFFD448,0)
                break
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFFD420))
    while True:
        frame=_calendar_compare_fields(memory,frame,frame.roster.byte(),255,1)
        frame=first_replace(frame,roster=frame.roster.advance(1))
        if frame.status&4:break
    frame=first_replace(frame,roster=frame.roster.advance(-1))
    frame=_calendar_test_fields(memory,frame,frame.roster.byte(),1)
    return _calendar_write_fields(memory,frame,frame.roster.base,low8(frame.choice),1)
def _calendar_sample_fields(memory,frame,entry,token,mask=None,limit=None):
    """Save D1 once; rejection sampling re-enters the RNG call, not MOVEM."""
    frame=_calendar_frame_fields(memory,frame,entry)
    frame=_calendar_save_fields(memory,frame,('target_y',))
    while True:
        frame=_calendar_call_fields(memory,frame,0x83D4,token)
        if mask is None:break
        frame=_calendar_move_fields(memory,frame,'target_x',low16(frame.target_x)&mask)
        frame=_calendar_compare_fields(memory,frame,low16(frame.target_x),limit)
        if frame.status&1:break
    return _calendar_restore_fields(memory,frame,('target_y',))
def sample_once_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    return _calendar_sample_fields(memory,frame,0x17598,0x175A2)
def sample_small_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    return _calendar_sample_fields(memory,frame,0x175A8,0x175B2,7,5)
def sample_wide_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    return _calendar_sample_fields(memory,frame,0x175C2,0x175CC,15,10)
def _calendar_product_terms(value,factor):
    """One state-free product authority, shared by field and historical callers."""
    value=checked_long(value);factor=checked_word(factor)
    lower=mulu16(value,factor)
    upper=mulu16(swap_words(value),factor)
    shifted=u32(upper<<16)
    return lower,upper,shifted,add32(lower,shifted)
def wrapped_product_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x175DC)
    lower,upper,shifted,result=_calendar_product_terms(frame.unit,low16(frame.target_x))
    frame=_calendar_move_fields(memory,frame,'distance',frame.unit,4)
    frame=_calendar_swap_fields(memory,frame,'distance')
    frame=_calendar_move_fields(memory,frame,'distance',upper,4)
    frame=_calendar_swap_fields(memory,frame,'distance')
    frame=_calendar_move_fields(memory,frame,'distance',0)
    frame=_calendar_move_fields(memory,frame,'unit',lower,4)
    frame=_calendar_arithmetic_fields(memory,frame,'unit',shifted,4)
    return first_replace(frame,unit=result)
def divide_percent_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x175EC)
    frame=_calendar_save_fields(memory,frame,('target_y',))
    frame=_calendar_move_fields(memory,frame,'target_y',frame.unit,4)
    frame=_calendar_move_fields(memory,frame,'unit',100,4)
    frame=_calendar_call_fields(memory,frame,0x35760,0x175FA)
    frame=_calendar_move_fields(memory,frame,'unit',frame.target_y,4)
    return _calendar_restore_fields(memory,frame,('target_y',))
def _calendar_scale_fields(memory,frame,entry,address,product_token,division_token):
    frame=_calendar_frame_fields(memory,frame,entry)
    frame=first_replace(frame,roster=memory.cursor_at(address))
    frame=_calendar_move_fields(memory,frame,'unit',frame.roster.long(low16(frame.choice)),4)
    frame=_calendar_call_fields(memory,frame,0x175DC,product_token)
    frame=_calendar_call_fields(memory,frame,0x175EC,division_token)
    return _calendar_write_fields(memory,frame,frame.roster.address(low16(frame.choice)),frame.unit,4)
def scale_e1e0_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    return _calendar_scale_fields(memory,frame,0x17514,0xFFFFE1E0,0x17520,0x17524)
def scale_e140_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    return _calendar_scale_fields(memory,frame,0x1752A,0xFFFFE140,0x17536,0x1753A)
def scale_e320_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    return _calendar_scale_fields(memory,frame,0x17540,0xFFFFE320,0x1754C,0x17550)
def scale_e000_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    return _calendar_scale_fields(memory,frame,0x17556,0xFFFFE000,0x17562,0x17566)
def scale_e0a0_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    return _calendar_scale_fields(memory,frame,0x1756C,0xFFFFE0A0,0x17578,0x1757C)
def scale_e5a0_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    return _calendar_scale_fields(memory,frame,0x17582,0xFFFFE5A0,0x1758E,0x17592)
def _calendar_submit_fields(memory,frame,entry,once_token,append_token,scales):
    frame=_calendar_frame_fields(memory,frame,entry)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFFF428))
    frame=_calendar_move_fields(memory,frame,'choice',frame.roster.byte(low16(frame.target_x)),1)
    if frame.status&8:return frame
    frame=_calendar_move_fields(memory,frame,'choice',low16(frame.target_x))
    frame=_calendar_call_fields(memory,frame,0x17598,once_token)
    frame=_calendar_move_fields(memory,frame,'target_x',low16(frame.target_x)&15)
    if not frame.status&4:return _calendar_move_fields(memory,frame,'target_x',low16(frame.choice))
    frame=_calendar_call_fields(memory,frame,0x17026,append_token)
    frame=_calendar_save_fields(memory,frame,('choice',))
    frame=_calendar_shift_fields(memory,frame,'choice',2,arithmetic=True)
    for sampler,sample_token,base,target,scale_token in scales:
        frame=_calendar_call_fields(memory,frame,sampler,sample_token)
        frame=_calendar_arithmetic_fields(memory,frame,'target_x',base)
        frame=_calendar_call_fields(memory,frame,target,scale_token)
    frame=_calendar_restore_fields(memory,frame,('choice',))
    return _calendar_move_fields(memory,frame,'target_x',low16(frame.choice))
def submit_calendar_three_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    return _calendar_submit_fields(memory,frame,0x171A6,0x171B6,0x171C4,
        ((0x175C2,0x171CE,80,0x17514,0x171D8),(0x175A8,0x171DC,95,0x1752A,0x171E6),
         (0x175C2,0x171EA,85,0x17540,0x171F4)))
def submit_calendar_four_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    return _calendar_submit_fields(memory,frame,0x17342,0x17352,0x17360,
        ((0x175C2,0x1736A,80,0x17514,0x17374),(0x175A8,0x17378,95,0x1752A,0x17382),
         (0x175C2,0x17386,85,0x17540,0x17390),(0x175C2,0x17394,80,0x17556,0x1739E)))
def submit_calendar_classified_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x17474)
    frame=_calendar_move_fields(memory,frame,'choice',low16(frame.target_x))
    frame=_calendar_shift_fields(memory,frame,'target_x',2,arithmetic=True)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFFE320))
    frame=_calendar_move_fields(memory,frame,'count',0,4)
    frame=_calendar_move_fields(memory,frame,'unit',frame.roster.long(low16(frame.target_x)),4)
    frame=_calendar_divu_fields(memory,frame,'unit',10,0x17482,True)
    frame=_calendar_move_fields(memory,frame,'count',memory.state.read(0x174F0+s16(low16(frame.unit)),1),1)
    frame=_calendar_compare_fields(memory,frame,low16(frame.unit),7)
    if not frame.status&1:return _calendar_move_fields(memory,frame,'target_x',low16(frame.choice))
    frame=_calendar_call_fields(memory,frame,0x17598,0x17496)
    frame=_calendar_move_fields(memory,frame,'target_x',low16(frame.target_x)&low16(frame.count))
    if not frame.status&4:return _calendar_move_fields(memory,frame,'target_x',low16(frame.choice))
    frame=_calendar_call_fields(memory,frame,0x17026,0x174A2)
    frame=_calendar_save_fields(memory,frame,('choice',))
    frame=_calendar_shift_fields(memory,frame,'choice',2,arithmetic=True)
    frame=_calendar_move_fields(memory,frame,'count',0,4)
    frame=_calendar_move_fields(memory,frame,'count',memory.state.read(0x174FC+s16(low16(frame.unit)),1),1)
    frame=_calendar_move_fields(memory,frame,'target_x',0,4)
    frame=_calendar_compare_fields(memory,frame,low16(frame.unit),7)
    if frame.status&1:
        frame=_calendar_call_fields(memory,frame,0x175C2,0x174BA)
        frame=_calendar_compare_fields(memory,frame,low16(frame.unit),6)
        if not frame.status&1:frame=_calendar_call_fields(memory,frame,0x175A8,0x174C6)
    frame=_calendar_arithmetic_fields(memory,frame,'target_x',low16(frame.count))
    for target,token in ((0x17514,0x174CE),(0x17556,0x174D2),(0x1756C,0x174D6),(0x17582,0x174DA)):
        frame=_calendar_call_fields(memory,frame,target,token)
    frame=_calendar_call_fields(memory,frame,0x175A8,0x174DE)
    frame=_calendar_arithmetic_fields(memory,frame,'target_x',95)
    frame=_calendar_call_fields(memory,frame,0x1752A,0x174E8)
    frame=_calendar_restore_fields(memory,frame,('choice',))
    return _calendar_move_fields(memory,frame,'target_x',low16(frame.choice))

def _calendar_legacy_entry_fields(state,words=(),longs=(),views=()):
    checked_state(state)
    for value in words:uint(value,16)
    frame=FirstDeploymentFrame.unobserved()
    for carrier,value in longs:
        uint(value,32)
        frame=first_replace(frame,**{carrier:value})
    for carrier,table in views:
        table=state.checked_table(table)
        frame=first_replace(frame,**{carrier:table.cursor()})
    return SceneRefreshMemory(state),frame
