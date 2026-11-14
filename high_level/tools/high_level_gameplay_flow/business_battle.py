"""Live packed groups, battle attrition and scene-flow business rules.

Each public routine corresponds to a complete original body. Neutral RAM
ports deliberately retain unresolved field meanings. Fixed-width arithmetic,
live overlapping copies, full status-word changes and original anomalies are
kept; unknown services stop explicitly instead of pretending to render.
"""
from .domain import (GameplayState, Table, Cursor, Word, Long, Boundary,
    checked_state, checked_table, checked_cursor, uint, u8, u16, u32, s16,
    low8, low16, high16, replace_byte, replace_word, swap_words,
    negative_byte, negative_word, divu_retained, descending_inclusive)
from .contexts_battle import (GlyphBatchContext, MapTransferContext,
    BattleSceneContext, PacketMutationContext, PacketResourceContext,
    PacketInsertionResult, BattleActionContext, DamagePotentialResult,
    NearestTerrainTarget, BattleFlowResult, SceneServiceContext,
    ProgressAllocationContext, checked_context)


from .contexts_battle import (BattlePresentationMemory, FirstDeploymentFrame, first_replace, _first_word, _first_long, _first_memory_word, _first_shift_word, _first_add_word, _first_right_word, _first_compare_word)

def _port(state, name):
    return state.table('ram_' + name)


def _shift_word(carrier, amount):
    return replace_word(carrier, u16(low16(carrier) << amount))


def _right_word(carrier, amount):
    return replace_word(carrier, low16(carrier) >> amount)


def _packed_resource(packet, offset, retained=0):
    """The original BYTE/WORD/LONG construction, with actual read order."""
    value = replace_byte(retained, packet.byte(0, offset))
    value = _shift_word(value, 8)
    value = replace_byte(value, packet.byte(0, offset + 1))
    value = u32(value << 8)
    value = replace_byte(value, packet.byte(0, offset + 2))
    value = u32(value << 8)
    return replace_byte(value, packet.byte(0, offset + 3))


def _store_packed_resource(packet, offset, value):
    packet.set_byte(0, low8(value), offset + 3)
    value >>= 8
    packet.set_byte(0, low8(value), offset + 2)
    value >>= 8
    packet.set_byte(0, low8(value), offset + 1)
    value = _right_word(value, 8)
    packet.set_byte(0, low8(value), offset)
    return value


def _random_fraction(state, multiplier, base=0):
    from .business_reuse import step_random
    return u16(high16(u32(low16(step_random(state)) * multiplier)) + base)


def _visible_force(state, force):
    return (force == _port(state, 'f67a').word()
            or force == _port(state, 'f67c').word()
            or force == _port(state, 'f67e').word())


def _poll_word(state, name, predicate):
    # The bus/finite DATA budget, not a fabricated interrupt, governs waiting.
    while not predicate(_port(state, name).word()):
        state.progress('battle-input-wait')


def sample_city_postbattle_reserve(state: GameplayState) -> Long:
    """Historical API projects the sole live postbattle field core."""
    checked_state(state)
    frame = sample_city_postbattle_reserve_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())
    return frame.target_x


def distribute_city_battle_progress(state: GameplayState) -> None:
    """Historical API projects the sole live postbattle field core."""
    checked_state(state)
    distribute_city_battle_progress_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())


def apply_assigned_city_light_attrition(state: GameplayState) -> None:
    """Historical API projects the sole live postbattle field core."""
    checked_state(state)
    apply_assigned_city_light_attrition_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())


def consume_city_battle_supply_long(state: GameplayState) -> None:
    """Historical API projects the sole live postbattle field core."""
    checked_state(state)
    consume_city_battle_supply_long_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())


def reduce_city_reserve_after_defeat(state: GameplayState) -> None:
    """Historical API projects the sole live postbattle field core."""
    checked_state(state)
    reduce_city_reserve_after_defeat_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())


def consume_city_battle_supply_word(state: GameplayState) -> None:
    """Historical API projects the sole live postbattle field core."""
    checked_state(state)
    consume_city_battle_supply_word_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())


def consolidate_city_after_battle(state: GameplayState) -> None:
    """Historical consolidation API projects one full field core, never invented fields."""
    checked_state(state)
    consolidate_city_after_battle_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())


def clear_city_officer_links(state: GameplayState) -> None:
    """Historical API projects the sole live postbattle field core."""
    checked_state(state)
    clear_city_officer_links_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())


def reassign_city_flagged_officers(state: GameplayState) -> None:
    """Historical API projects the sole live postbattle field core."""
    checked_state(state)
    reassign_city_flagged_officers_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())


def rebuild_city_links_from_primary_roster(state: GameplayState) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_gameplay_arrival_fields(state, 0x1d542)


def classify_duel_object_result(state: GameplayState) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_gameplay_arrival_fields(state, 0x1d598)


def apply_postbattle_city_economic_attrition(state: GameplayState) -> None:
    """Historical API projects the sole live postbattle field core."""
    checked_state(state)
    apply_postbattle_city_economic_attrition_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())


def city_reserve_forces_duel_carry(state: GameplayState):
    """Historical API projects the sole original duel-reserve gate."""
    checked_state(state)
    frame = city_reserve_forces_duel_carry_fields(
        BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())
    return state.set_carry(bool(frame.status & 1))


def group_matches_city_head_carry(state: GameplayState, candidate: Word):
    """181A6: mode selects the actual BYTE or WORD head alias."""
    checked_state(state)
    uint(candidate, 16)
    if _port(state, 'f6d7').byte() & 2:
        city = u16(_port(state, 'f68a').word() << 1)
        matched = candidate == _port(state, 'f45e').word(city)
    else:
        city = _port(state, 'f68a').word()
        matched = low8(candidate) == _port(state, 'a027').byte(city)
    return state.set_carry(matched)


def refresh_packed_group_average(state: GameplayState, packet: Table) -> Long:
    """18158: inclusive wrapped count, WORD sum and packed DIVU retained."""
    checked_state(state)
    checked_table(packet, state)
    count = packet.byte() & 15
    source, attributes = packet.cursor(13), _port(state, 'c400')
    total = 0
    for _ in descending_inclusive(u16(count - 1)):
        officer = source.next_byte()
        total = replace_word(total, u16(low16(total) + attributes.byte(officer)))
    result = divu_retained(total, count)
    packet.set_byte(0, low8(result), 3)
    return result


def copy_selected_city_group_parameter(state: GameplayState, packet: Table) -> None:
    """18184: select the original external pointer table, not a copied schema."""
    checked_state(state)
    checked_table(packet, state)
    selector = u16(_port(state, 'f6d6').word() << 2)
    source = state.table(state.table(0x18196).long(selector))
    packet.set_byte(0, source.byte(0, 1), 4)


def reserve_packed_group_member_byte(state: GameplayState,
        packet: Table, previous_count: Word) -> PacketInsertionResult:
    """1802A: reverse copy the live following packet bytes one position up."""
    checked_state(state)
    checked_table(packet, state)
    uint(previous_count, 16)
    source = packet.cursor(previous_count)
    source.base = u32(source.base + 13)
    start = source.base
    if previous_count == 0:
        source.set_byte(0, 0)
    while True:
        count = source.byte() & 15
        if count == 0:
            break
        source.base = u32(source.base + 13 + count)
    destination = source.cursor()
    destination.base = u32(destination.base + 1)
    destination.set_byte(0, 0)
    while source.base > start:
        value = source.previous_byte()
        destination.base = u32(destination.base - 1)
        destination.set_byte(0, value)
    return PacketInsertionResult(packet, destination, previous_count)


def append_survivors_to_packed_group(state: GameplayState,
        context: PacketMutationContext) -> PacketInsertionResult:
    """181E8: original forward overlapping packet shift and roster drain."""
    context = checked_context(context, PacketMutationContext, state)
    packet = context.packet
    count = packet.byte() & 15
    source = packet.cursor(u16(13 + count))
    append = source.cursor()
    packet.set_byte(0, u8(packet.byte() + context.member_count))
    destination = packet.cursor(u16(13 + u16(count + context.member_count)))
    while True:
        following = source.byte() & 15
        if following == 0:
            break
        for _ in descending_inclusive(u16(following + 12)):
            destination.append_byte(source.next_byte())
    destination.set_byte(0, 0)
    roster = context.insertion_roster
    while True:
        officer = roster.word()
        if negative_word(officer):
            return PacketInsertionResult(packet, roster, context.member_count)
        roster.append_word(65535)
        append.append_byte(low8(officer))


def add_staged_resources_to_packed_group(state: GameplayState, packet: Table) -> None:
    """18224: retain the second quantity's original two WORD shifts."""
    checked_state(state)
    checked_table(packet, state)
    if _port(state, 'f6d7').byte() & 2:
        first, second = _port(state, 'f69a'), _port(state, 'f6a2')
    else:
        first, second = _port(state, 'f696'), _port(state, 'f69e')
    carrier = _packed_resource(packet, 5)
    carrier = min(u32(carrier + first.long()), 999999)
    carrier = _store_packed_resource(packet, 5, carrier)
    carrier = replace_byte(carrier, packet.byte(0, 9))
    carrier = _shift_word(carrier, 8)
    carrier = replace_byte(carrier, packet.byte(0, 10))
    carrier = _shift_word(carrier, 8)  # original WORD, not LONG
    carrier = replace_byte(carrier, packet.byte(0, 11))
    carrier = u32(carrier << 8)
    carrier = replace_byte(carrier, packet.byte(0, 12))
    carrier = min(u32(carrier + second.long()), 999999)
    _store_packed_resource(packet, 9, carrier)
    first.set_long(0, 0)
    second.set_long(0, 0)


def split_city_resources_into_group(state: GameplayState,
        context: PacketResourceContext) -> None:
    """1807A: troop-weighted packed resource shares using original division."""
    context = checked_context(context, PacketResourceContext, state)
    from .business_reuse import signed_divmod
    selector = u16(_port(state, 'f6d6').word() << 2)
    first = state.table(state.table(0x1805A).long(selector))
    second = state.table(state.table(0x1806A).long(selector))
    amount = _right_word(first.long(), 8)
    offset = u16(_port(state, 'f3a6').word() << 2)
    troops = _port(state, 'c800')
    selected = u32(troops.long(offset) + 100)
    numerator = u32(low16(amount) * low16(selected))
    denominator = low16(selected)
    while True:
        member = context.roster.next_word()
        if negative_word(member):
            break
        offset = u16((member & 255) << 2)
        denominator = u32(denominator + troops.long(offset))
        denominator = u32(denominator + 100)
    quotient, remainder = signed_divmod(state, numerator, denominator)
    share = u32(quotient << 8)
    first.set_long(0, u32(first.long() - share))
    quantity = _packed_resource(context.packet, 5, remainder)
    _store_packed_resource(context.packet, 5, min(u32(share + quantity), 999999))
    amount = _right_word(second.long(), 8)
    quotient, remainder = signed_divmod(state, u32(low16(amount) * low16(selected)), denominator)
    share = u32(quotient << 8)
    second.set_long(0, u32(second.long() - share))
    quantity = _packed_resource(context.packet, 9, remainder)
    _store_packed_resource(context.packet, 9, min(u32(share + quantity), 999999))


def collect_battle_special_status_members(state: GameplayState,
        source: Cursor, destination: Cursor, side_bits: Word) -> Cursor:
    """Historical cursor API is a projection of the unique 1A78A fields."""
    checked_state(state)
    checked_cursor(source, state)
    checked_cursor(destination, state)
    uint(side_bits, 16)
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        roster=destination, candidates=source, controller=_port(state, 'c700'))
    return collect_battle_special_status_members_fields(
        BattlePresentationMemory(state), frame, side_bits).roster


def sample_battle_special_status_factor(state: GameplayState) -> Long:
    """Historical scalar API projects the unique 1A706 field algorithm."""
    checked_state(state)
    return sample_battle_special_status_factor_fields(
        BattlePresentationMemory(state), FirstDeploymentFrame.unobserved()).target_x


def compute_battle_damage_potential(state: GameplayState,
        factor: Long, retained_damage: Long) -> DamagePotentialResult:
    """Historical D0/D7 API projects the unique 1A7A2 field algorithm."""
    checked_state(state)
    uint(factor, 32)
    uint(retained_damage, 32)
    frame = first_replace(FirstDeploymentFrame.unobserved(),
        target_x=factor, choice=retained_damage)
    returned = compute_battle_damage_potential_fields(
        BattlePresentationMemory(state), frame, factor)
    return DamagePotentialResult(returned.target_x, returned.choice)


def find_nearest_secondary_terrain_target(state: GameplayState) -> NearestTerrainTarget:
    """Legacy result projects the unique 1E464 algorithm, without extra reads."""
    return find_nearest_secondary_terrain_target_observations(state)[0]


def secondary_roster_has_terrain_six_carry(state: GameplayState):
    """Historical carry API projects the one18706 query and real saved fields."""
    checked_state(state)
    _, selected = secondary_roster_has_terrain_six_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())
    return state.carry_observed(int(selected))


def merge_city_survivor_rosters(state: GameplayState, destination: Cursor) -> Cursor:
    """1830A: concatenate live lists; over-ten tail releases keep original order."""
    checked_state(state)
    checked_cursor(destination, state)
    source = _port(state, 'a5ce' if _port(state, 'f6d7').byte() & 2 else 'a57a').cursor()
    source_head = source.cursor()
    count = 0
    while not negative_word(destination.next_word()):
        count = u16(count + 1)
    destination.base = u32(destination.base - 2)
    while True:
        member = source.next_word()
        destination.append_word(member)
        if negative_word(member):
            break
        count = u16(count + 1)
    source_head.put_word(65535)
    if count <= 10:
        return destination
    inclusive_extra = u16(count - 11)
    destination.base = u32(destination.base - 2)
    token = _port(state, 'f68a').word() | 128
    assignments = _port(state, 'cc00')
    owner = _port(state, 'f68c').word()
    if _port(state, 'f6d7').byte() & 2:
        owner = _port(state, 'f68e').word()
    notify = _visible_force(state, owner)
    for _ in descending_inclusive(inclusive_extra):
        member = destination.previous_word()
        if notify:
            _port(state, 'f3d0').set_word(0, member)
        assignments.set_byte(member, low8(token))
        if notify:
            _port(state, 'f740').set_word(0, 320)
            present_battle_message(state)
    destination.put_word(65535)
    return destination


def assign_city_survivor_roster_tokens(state: GameplayState, roster: Cursor) -> None:
    """182C4: concatenate before writing owner+105 and clearing positions."""
    checked_state(state)
    checked_cursor(roster, state)
    saved_base = roster.base
    merge_city_survivor_rosters(state, roster)
    roster.base = saved_base  # actual callee restores its A4 after its live DATA
    assignments, positions = _port(state, 'cc00'), _port(state, 'a150')
    _port(state, 'f68a').word()  # original MOVE.W load is a real DATA event
    owner = _port(state, 'f68c').word()
    if _port(state, 'f6d7').byte() & 2:
        owner = _port(state, 'f68e').word()
    token = u16(owner + 105)
    while True:
        member = roster.next_word()
        if negative_word(member):
            roster.base = saved_base
            return
        member &= 255
        assignments.set_byte(member, low8(token))
        positions.set_long(u16(member << 2), 0)


def remove_queued_packed_group_member(state: GameplayState, queue: Cursor, member_carrier: Long) -> Cursor:
    """Historical queue observations project the sole176D2 overlapping copy."""
    from .contexts_services import SceneRefreshMemory
    checked_state(state)
    checked_cursor(queue,state)
    uint(member_carrier,32)
    entered = first_replace(FirstDeploymentFrame.unobserved(),roster=queue.advance(0),target_x=member_carrier)
    actual = remove_queued_packed_group_member_fields(SceneRefreshMemory(state),entered)
    queue.base = actual.roster.base
    return queue


def compact_active_packed_group_queue(state: GameplayState, retained_member: Long = 0) -> Cursor:
    """Historical explicitly retained D0 projects the unique176B6 queue loop."""
    from .contexts_services import SceneRefreshMemory
    checked_state(state)
    uint(retained_member,32)
    entered = first_replace(FirstDeploymentFrame.unobserved(),target_x=retained_member)
    return compact_active_packed_group_queue_fields(SceneRefreshMemory(state),entered).roster


def cache_battle_roster_totals(state: GameplayState) -> None:
    """Historical state-only API cannot invent the BSR full-field entry."""
    from .contexts_services import SceneRefreshMemory
    checked_state(state)
    cache_battle_roster_totals_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def upload_battlefield_tilemap(state: GameplayState, retained_tile: Long = 0) -> Long:
    """Historical tile observation projects the one complete upload core."""
    checked_state(state)
    uint(retained_tile,32)
    frame = first_replace(FirstDeploymentFrame.unobserved(),count=retained_tile)
    return upload_battlefield_tilemap_fields(BattlePresentationMemory(state),frame).count


def upload_battle_background_planes(state: GameplayState, count_carrier: Long = 0) -> Long:
    """Old count observation cannot invent the dictionary full-frame entry."""
    from .contexts_services import SceneRefreshMemory
    checked_state(state)
    uint(count_carrier,32)
    frame = first_replace(FirstDeploymentFrame.unobserved(),target_x=count_carrier)
    return upload_battle_background_planes_fields(SceneRefreshMemory(state),frame).target_x


def append_force_head_glyphs(state: GameplayState, context: GlyphBatchContext) -> GlyphBatchContext:
    """Historical five observations project the sole179D6 core, no full SP claim."""
    from .contexts_services import SceneRefreshMemory
    context = checked_context(context,GlyphBatchContext,state)
    frame = first_replace(FirstDeploymentFrame.unobserved(),roster=context.source.advance(0),
        candidates=context.destination.advance(0),target_x=context.background,target_y=context.foreground,count=context.inclusive_count)
    actual = append_force_head_glyphs_fields(SceneRefreshMemory(state),frame)
    context.source.base,context.destination.base = actual.roster.base,actual.candidates.base
    return GlyphBatchContext(context.source,context.destination,actual.target_x,actual.target_y,actual.count)


def present_battle_message(state: GameplayState) -> None:
    """260E4: asynchronous message wait with actual 2500/2700 SR transitions."""
    checked_state(state)
    from .business_services import clear_scene_video_and_state
    saved_scene = _port(state, 'f612').word()
    saved_menu = _port(state, 'f362').word()
    _port(state, 'f612').set_word(0, 1044)
    _port(state, 'f362').set_word(0, 0)
    _port(state, 'f600').set_word(0, 0)
    state.set_status_word(0x2500)
    while True:
        _poll_word(state, 'f600', lambda value: value != 0)
        if _port(state, 'f600').word() != 40:
            break
        clear_scene_video_and_state(state)
        _port(state, 'f600').set_word(0, 0)
        state.set_status_word(0x2500)
    state.set_status_word(0x2700)
    _port(state, 'f362').set_word(0, saved_menu)
    _port(state, 'f612').set_word(0, saved_scene)


def integrate_selected_officer_into_packed_group(state: GameplayState) -> Table:
    """17F30: remove one selected officer or absorb the city's live roster."""
    checked_state(state)
    from .business_reuse import find_group_at_coordinate
    selector = u16((_port(state, 'f6d6').word() & 2) << 1)
    selected = state.table(state.table(0x17F18).long(selector)).cursor()
    selected_head = selected.cursor()
    count_view = state.table(state.table(0x17F20).long(selector))
    coordinate_view = state.table(state.table(0x17F28).long(selector))
    count_view.set_word(0, u16(count_view.word() - 1))
    officer = _port(state, 'f3a6').word()
    if not group_matches_city_head_carry(state, officer).carry:
        while selected.next_word() != officer:
            pass
        while True:
            value = selected.next_word()
            selected.set_word(0, value, -4)
            if negative_word(value):
                break
        coordinate = coordinate_view.word()
        packet = find_group_at_coordinate(state, coordinate)
        packet.set_byte(0, coordinate >> 8, 1)
        packet.set_byte(0, low8(coordinate), 2)
        previous = packet.byte() & 15
        if previous == 0:
            for displacement in range(5, 14):
                packet.set_byte(0, 0, displacement)
        packet.set_byte(0, u8(packet.byte() + 1))
        reserve_packed_group_member_byte(state, packet, previous)
        packet.set_byte(u16(13 + previous), _port(state, 'f3a7').byte())
        split_city_resources_into_group(state, PacketResourceContext(packet, selected_head))
        add_staged_resources_to_packed_group(state, packet)
        assignments = _port(state, 'cc00')
        officer = _port(state, 'f3a6').word()
        assignments.set_byte(officer, assignments.byte(officer) | 64)
        _port(state, 'a150').set_long(u16(officer << 2), 0)
    else:
        survivors = selected.cursor()
        saved_base = survivors.base
        merge_city_survivor_rosters(state, survivors)
        survivors.base = saved_base
        counter_source = selected.cursor()
        member_count = 0
        while not negative_word(counter_source.next_word()):
            member_count = u16(member_count + 1)
        coordinate = coordinate_view.word()
        packet = find_group_at_coordinate(state, coordinate)
        packet.set_byte(0, coordinate >> 8, 1)
        packet.set_byte(0, low8(coordinate), 2)
        if packet.byte() & 15 == 0:
            for displacement in range(5, 14):
                packet.set_byte(0, 0, displacement)
        append_survivors_to_packed_group(state,
            PacketMutationContext(packet, selected, survivors, member_count))
        assign_city_survivor_roster_tokens(state, survivors)
    refresh_packed_group_average(state, packet)
    copy_selected_city_group_parameter(state, packet)
    return packet


def award_city_reserve_attrition(state: GameplayState) -> Long:
    """Historical loss value is the same185E4 core's actual D0."""
    checked_state(state)
    return award_city_reserve_attrition_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved()).target_x


def resolve_city_battle_damage(state: GameplayState,
        retained_damage: Long = 0) -> Long:
    """Historical award API projects the one183F8 full field algorithm."""
    checked_state(state)
    uint(retained_damage, 32)
    frame = first_replace(FirstDeploymentFrame.unobserved(), choice=retained_damage)
    return resolve_city_battle_damage_fields(BattlePresentationMemory(state), frame)[1]


def settle_city_battle_outcome(state: GameplayState) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    checked_state(state)
    settle_city_battle_outcome_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())


def upload_battle_scene_labels(state: GameplayState, context: BattleSceneContext) -> BattleSceneContext:
    """Historical four observations do not fabricate all D/A/A7 of177BE."""
    from .contexts_services import SceneRefreshMemory
    context = checked_context(context,BattleSceneContext,state)
    frame = first_replace(FirstDeploymentFrame.unobserved(),target_x=context.background,
        target_y=context.foreground,count=context.glyph_count)
    actual = upload_battle_scene_labels_fields(SceneRefreshMemory(state),frame)
    return BattleSceneContext(actual.target_x,actual.target_y,actual.count,context.training_carrier)


def initialize_battle_scene(state: GameplayState, context: BattleSceneContext) -> BattleSceneContext:
    """Old four observations cannot fabricate complete Scene registers or A7."""
    from .contexts_services import SceneRefreshMemory
    context = checked_context(context,BattleSceneContext,state)
    frame = first_replace(FirstDeploymentFrame.unobserved(),target_x=context.background,target_y=context.foreground,
        unit=context.glyph_count,count=context.training_carrier)
    actual = initialize_battle_scene_fields(SceneRefreshMemory(state),frame)
    return BattleSceneContext(actual.target_x,actual.target_y,actual.unit,actual.count)


def run_battle_scene_round(state: GameplayState,
        context: BattleSceneContext) -> BattleFlowResult:
    """Historical four observations project sole DC0, never a default full ABI."""
    from .contexts_services import SceneRefreshMemory
    context = checked_context(context,BattleSceneContext,state)
    entered = first_replace(FirstDeploymentFrame.unobserved(),target_x=context.background,
        target_y=context.foreground,unit=context.glyph_count,count=context.training_carrier)
    actual = run_battle_scene_round_fields(SceneRefreshMemory(state),entered)
    return BattleFlowResult(actual.count)


def trigger_battle_for_city_rectangle(state: GameplayState,
        context: BattleActionContext):
    """Historical scalar inputs project the same 23736 field algorithm."""
    context = checked_context(context, BattleActionContext, state)
    frame = BattleTriggerFrame(target_x=None, target_y=None, unit=None,
        count=None, distance=None, offset_x=None, offset_y=None, choice=None,
        roster=None, candidates=None, controller=None, scan=None,
        opponent=None, scratch=None, auxiliary=None, stack_cursor=None,
        status=state.sr, legacy_context=context)
    frame = trigger_battle_for_city_rectangle_fields(BattleTriggerMemory(state),
        frame, context.acting_officer)
    return state.carry_observed(int(bool(frame.status & 1)))


# One city-trigger authority; imported ports do not copy the live RAM.
from .contexts_battle import BattleTriggerMemory, BattleTriggerFrame, battle_replace

def find_nearest_secondary_terrain_target_observations(state: GameplayState) -> tuple[NearestTerrainTarget, Word]:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    checked_state(state)
    frame = find_nearest_secondary_terrain_target_fields(BattlePresentationMemory(state), FirstDeploymentFrame.unobserved())
    return NearestTerrainTarget(low16(frame.offset_x), low16(frame.offset_y)), low16(frame.choice)

def _trigger_frame(memory, frame):
    if type(memory) is not BattleTriggerMemory or type(frame) is not BattleTriggerFrame:
        raise ValueError('sealed same-state trigger frame required')
    return frame.validate(memory.state)


def _trigger_conditions(memory, frame, value, bits):
    """MOVE/TST clear V/C, preserve X and all non-CCR SR bits."""
    uint(value, bits)
    status = (frame.status & 65520) | (8 if value & (1 << (bits - 1)) else 0) | (4 if value == 0 else 0)
    memory.state.sr = status
    return battle_replace(frame, status=status)


def _trigger_compare(memory, frame, left, right):
    uint(left, 16)
    uint(right, 16)
    value = u16(left - right)
    overflow = ((left ^ right) & (left ^ value) & 32768) != 0
    status = (frame.status & 65520) | (8 if value & 32768 else 0) | (4 if value == 0 else 0) | (2 if overflow else 0) | (1 if left < right else 0)
    memory.state.sr = status
    return battle_replace(frame, status=status)


def _trigger_shift(memory, frame, value, amount):
    uint(value, 16)
    result = u16(value << amount)
    carry = bool(value & (1 << (16 - amount)))
    status = (frame.status & 65504) | (17 if carry else 0) | (8 if result & 32768 else 0) | (4 if result == 0 else 0)
    memory.state.sr = status
    return battle_replace(frame, status=status), result


def _trigger_retained_word(carrier, value):
    # None is an explicitly unobserved legacy high carrier, never zero.
    uint(value, 16)
    return None if carrier is None else replace_word(carrier, value)


def _trigger_store(memory, frame, suffix, value, bits=16):
    frame = _trigger_conditions(memory, frame, value, bits)
    if bits == 16:
        memory.port(suffix).set_word(0, value)
    elif bits == 32:
        memory.port(suffix).set_long(0, value)
    else:
        raise ValueError('actual trigger store width required')
    return frame


def _trigger_carry(memory, frame, carry):
    """238A0 ORI/238A8 ANDI are full-SR, not synthetic carry results."""
    if type(carry) is not bool:
        raise ValueError('actual carry branch required')
    status = (frame.status & 65534) | int(carry)
    memory.state.set_status_word(status)
    return battle_replace(frame, status=status)


def _trigger_push_word(memory, frame, value):
    frame = _trigger_conditions(memory, frame, uint(value, 16), 16)
    if frame.stack_cursor is None:
        return frame
    stack = frame.stack_cursor.advance(-2)
    stack.set_word(0, value)
    return battle_replace(frame, stack_cursor=stack)


def _trigger_pop_word(memory, frame, legacy_value):
    if frame.stack_cursor is None:
        value = uint(legacy_value, 16)
    else:
        value = frame.stack_cursor.word()
        frame = battle_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
    return _trigger_conditions(memory, frame, value, 16), value


def _trigger_legacy_call(memory, frame, target):
    """Old typed APIs observe partial fields; they never claim full Scene ABI."""
    state, context = memory.state, frame.legacy_context
    selected, terminator = None, None
    if target == 0x1E464:
        result, terminator = find_nearest_secondary_terrain_target_observations(state)
        selected = result.officer
        frame = battle_replace(frame,
            offset_y=_trigger_retained_word(frame.offset_y, selected),
            choice=_trigger_retained_word(frame.choice, terminator))
    elif target == 0x1E422:
        city_reserve_forces_duel_carry(state)
    elif target == 0x260E4:
        present_battle_message(state)
    elif target == 0x183F8:
        resolve_city_battle_damage(state, context.damage_carrier)
    elif target == 0xDC0:
        run_battle_scene_round(state, context.scene)
    elif target == 0x17602:
        initialize_battle_scene(state, context.scene)
    else:
        raise Boundary('unrecovered original legacy battle trigger call ' + str(target))
    return battle_replace(frame, status=state.sr), selected, terminator


def _trigger_call(memory, frame, target, continuation):
    """Full Scene calls use real current SP/token and consume a full result."""
    frame = _trigger_frame(memory, frame)
    if not memory.complete:
        return _trigger_legacy_call(memory, frame, target)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = battle_replace(frame, stack_cursor=stack)
    if target in (99320, 123938, 124004, 95746, 3520, 155876):
        fields = FirstDeploymentFrame(target_x=entered.target_x, target_y=entered.target_y, unit=entered.unit, count=entered.count, distance=entered.distance, offset_x=entered.offset_x, offset_y=entered.offset_y, choice=entered.choice, roster=entered.roster, candidates=entered.candidates, controller=entered.controller, scan=entered.scan, opponent=entered.opponent, scratch=entered.scratch, auxiliary=entered.auxiliary, stack_cursor=entered.stack_cursor, status=entered.status & 31)
        if target == 123938:
            fields = city_reserve_forces_duel_carry_fields(BattlePresentationMemory(memory.state), fields)
        elif target == 124004:
            fields = find_nearest_secondary_terrain_target_fields(BattlePresentationMemory(memory.state), fields)
        elif target == 95746:
            from .contexts_services import SceneRefreshMemory
            fields = initialize_battle_scene_fields(SceneRefreshMemory(memory.state), fields)
        elif target == 3520:
            from .contexts_services import SceneRefreshMemory
            fields = run_battle_scene_round_fields(SceneRefreshMemory(memory.state), fields)
        elif target == 155876:
            from ..high_level_main_flows.business_movement_support import present_battle_message_fields
            fields = present_battle_message_fields(memory.state, fields)
        else:
            fields = resolve_city_battle_damage_fields(BattlePresentationMemory(memory.state), fields)[0]
        returned = battle_replace(entered, target_x=fields.target_x, target_y=fields.target_y, unit=fields.unit, count=fields.count, distance=fields.distance, offset_x=fields.offset_x, offset_y=fields.offset_y, choice=fields.choice, roster=fields.roster, candidates=fields.candidates, controller=fields.controller, scan=fields.scan, opponent=fields.opponent, scratch=fields.scratch, auxiliary=fields.auxiliary, stack_cursor=fields.stack_cursor, status=memory.state.sr)
    else:
        returned = memory.state.service_at(target, entered)
    if type(returned) is not BattleTriggerFrame:
        raise Boundary('real trigger child must return all observed full fields')
    returned.validate_complete(memory.state)
    memory.state.sr = returned.status
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise Boundary('original trigger return slot changed to ' + str(actual))
    returned = battle_replace(returned, stack_cursor=returned.stack_cursor.advance(4))
    return (returned, low16(returned.offset_y), low16(returned.choice))


def _trigger_notification(memory, frame, message, continuation):
    frame = _trigger_store(memory, frame, 'f740', message)
    value = memory.port('f6d7').byte()
    status = (frame.status & 65531) | (0 if value & 2 else 4)
    memory.state.sr = status
    memory.port('f6d7').set_byte(0, value ^ 2)
    frame, _, _ = _trigger_call(memory, battle_replace(frame, status=status),
        0x260E4, continuation)
    # The callee may mutate the byte. BCHG must read it anew, not undo a snapshot.
    value = memory.port('f6d7').byte()
    status = (frame.status & 65531) | (0 if value & 2 else 4)
    memory.state.sr = status
    memory.port('f6d7').set_byte(0, value ^ 2)
    return battle_replace(frame, status=status)


def _trigger_wait(memory, frame, suffix, expected, reason):
    """No unchanged CPU-frame assumption is made across an unknown Scene IRQ."""
    while True:
        value = memory.port(suffix).word()
        frame = _trigger_compare(memory, frame, value, expected)
        if value == expected:
            return frame
        if memory.complete:
            raise Boundary('original interrupt wait requires full resumed trigger fields: ' + reason)
        memory.state.progress(reason)
        frame = battle_replace(frame, status=memory.state.sr)


def _trigger_regular_damage(memory, frame):
    frame = _trigger_notification(memory, frame, 303, 0x237C4)
    frame, _, _ = _trigger_call(memory, frame, 0x183F8, 0x237D0)
    mode = memory.port('f612').word()
    frame = _trigger_compare(memory, frame, mode, 1041)
    if mode == 1041:
        return frame
    offset = memory.port('f68a').word()
    frame = _trigger_conditions(memory, battle_replace(frame,
        target_x=_trigger_retained_word(frame.target_x, offset)), offset, 16)
    frame, offset = _trigger_shift(memory, frame, offset, 2)
    source = memory.port('e59c').cursor()
    frame = battle_replace(frame, target_x=_trigger_retained_word(frame.target_x, offset), roster=source)
    frame = _trigger_store(memory, frame, 'f3c8', source.long(offset), 32)
    return _trigger_notification(memory, frame, 275, 0x237FC)


def _trigger_duel(memory, frame):
    frame = _trigger_store(memory, frame, 'f3d0', memory.port('f3f2').word())
    frame = _trigger_store(memory, frame, 'f3d2', memory.port('f3a6').word())
    frame = _trigger_notification(memory, frame, 276, 0x23824)
    frame = _trigger_store(memory, frame, 'f702', memory.port('f3f2').word())
    frame = _trigger_store(memory, frame, 'f706', memory.port('f3a6').word())
    saved_scene = memory.port('f612').word()
    frame = _trigger_push_word(memory, frame, saved_scene)
    saved_menu = memory.port('f362').word()
    frame = _trigger_push_word(memory, frame, saved_menu)
    frame = _trigger_store(memory, frame, 'f772', 2)
    frame = _trigger_store(memory, frame, 'f612', 1031)
    frame = _trigger_store(memory, frame, 'f362', 3)
    # MC68000 memory CLR owns its original read before the write.
    memory.port('f352').word()
    frame = _trigger_store(memory, frame, 'f352', 0)
    memory.state.set_status_word(0x2500)
    frame = _trigger_wait(memory, battle_replace(frame, status=0x2500),
        'f600', 196, 'battle-input-wait')
    memory.state.set_status_word(0x2700)
    frame, _, _ = _trigger_call(memory, battle_replace(frame, status=0x2700), 0xDC0, 0x2386A)
    memory.state.set_status_word(0x2500)
    frame = _trigger_wait(memory, battle_replace(frame, status=0x2500),
        'f600', 132, 'battle-input-wait')
    frame, _, _ = _trigger_call(memory, frame, 0x17602, 0x2387C)
    memory.state.set_status_word(0x2500)
    frame = battle_replace(frame, status=0x2500)
    while True:
        mode = memory.port('f612').word()
        frame = _trigger_compare(memory, frame, mode, 1032)
        if mode == 1032:
            break
        mode = memory.port('f612').word()
        frame = _trigger_compare(memory, frame, mode, 1041)
        if mode == 1041:
            break
        if memory.complete:
            raise Boundary('original duel completion requires full resumed trigger fields')
        memory.state.progress('battle-scene-completion')
        frame = battle_replace(frame, status=memory.state.sr)
    memory.state.set_status_word(0x2700)
    frame, menu = _trigger_pop_word(memory, battle_replace(frame, status=0x2700), saved_menu)
    memory.port('f362').set_word(0, menu)
    frame, scene = _trigger_pop_word(memory, frame, saved_scene)
    memory.port('f612').set_word(0, scene)
    return frame


def trigger_battle_for_city_rectangle_fields(memory, frame, actor):
    """23736: one logical core, original ordered reads, full-field Scene bridge.

    Rectangle/task gates, nearest terrain target, ordinary damage and duel are
    distinct steps. Actual child CPU interfaces remain explicit; no missing
    return is substituted. Legacy projection supplies only observed inputs.
    """
    frame = _trigger_frame(memory, frame)
    actor = uint(actor, 16)
    if memory.complete and actor != low16(frame.choice):
        raise ValueError('actual incoming D7 low WORD required')
    first_flags = memory.table(0x00FF3CC2).cursor()
    frame = battle_replace(frame, roster=first_flags)
    flag = first_flags.byte(actor)
    frame = _trigger_conditions(memory, frame, flag, 8)
    if flag:
        return _trigger_carry(memory, frame, False)
    second_flags = memory.table(0x00FF3DC2).cursor()
    frame = battle_replace(frame, candidates=second_flags)
    flag = second_flags.byte(actor)
    frame = _trigger_conditions(memory, frame, flag, 8)
    if flag:
        return _trigger_carry(memory, frame, False)
    bounds = memory.table(0xAE1B2).cursor()
    frame = battle_replace(frame, roster=bounds)
    offset = memory.port('f68a').word()
    frame = _trigger_conditions(memory, battle_replace(frame,
        target_x=_trigger_retained_word(frame.target_x, offset)), offset, 16)
    frame, offset = _trigger_shift(memory, frame, offset, 3)
    frame = battle_replace(frame, target_x=_trigger_retained_word(frame.target_x, offset))
    x_min = bounds.word(offset)
    frame = _trigger_conditions(memory, battle_replace(frame, target_y=_trigger_retained_word(frame.target_y, x_min)), x_min, 16)
    x_max = bounds.word(offset, 2)
    frame = _trigger_conditions(memory, battle_replace(frame, unit=_trigger_retained_word(frame.unit, x_max)), x_max, 16)
    y_min = bounds.word(offset, 4)
    frame = _trigger_conditions(memory, battle_replace(frame, count=_trigger_retained_word(frame.count, y_min)), y_min, 16)
    y_max = bounds.word(offset, 6)
    frame = _trigger_conditions(memory, battle_replace(frame, distance=_trigger_retained_word(frame.distance, y_max)), y_max, 16)
    positions = memory.port('a150').cursor()
    frame = _trigger_conditions(memory, battle_replace(frame, roster=positions,
        target_x=_trigger_retained_word(frame.target_x, actor)), actor, 16)
    frame, actor_offset = _trigger_shift(memory, frame, actor, 2)
    frame = battle_replace(frame, target_x=_trigger_retained_word(frame.target_x, actor_offset))
    value = positions.word(actor_offset)
    frame = _trigger_compare(memory, frame, x_min, value)
    if x_min > value:
        return _trigger_carry(memory, frame, False)
    value = positions.word(actor_offset)
    frame = _trigger_compare(memory, frame, x_max, value)
    if x_max < value:
        return _trigger_carry(memory, frame, False)
    value = positions.word(actor_offset, 2)
    frame = _trigger_compare(memory, frame, y_min, value)
    if y_min > value:
        return _trigger_carry(memory, frame, False)
    value = positions.word(actor_offset, 2)
    frame = _trigger_compare(memory, frame, y_max, value)
    if y_max < value:
        return _trigger_carry(memory, frame, False)
    frame = _trigger_store(memory, frame, 'f3f2', actor)
    frame, selected, terminator = _trigger_call(memory, frame, 0x1E464, 0x2379E)
    # The real 1E464 D7 WORD is its roster terminator, not the actor.
    frame = _trigger_push_word(memory, frame, terminator)
    frame = _trigger_store(memory, frame, 'f3a6', selected)
    duel = False
    if not negative_word(selected):
        frame, _, _ = _trigger_call(memory, frame, 0x1E422, 0x237AE)
        duel = bool(frame.status & 1)
    frame = _trigger_duel(memory, frame) if duel else _trigger_regular_damage(memory, frame)
    frame, saved_choice = _trigger_pop_word(memory, frame, terminator)
    frame = battle_replace(frame, choice=_trigger_retained_word(frame.choice, saved_choice))
    return _trigger_carry(memory, frame, True)

def _presentation_frame(memory, frame):
    if type(memory) is not BattlePresentationMemory:
        raise ValueError('closed same-state presentation memory required')
    return memory.validate_frame(frame)

def _presentation_call_fields(memory, frame, continuation, algorithm):
    """A known direct child owns only its actual internal JSR/RTS slot."""
    frame = _presentation_frame(memory, frame)
    uint(continuation, 32)
    if frame.stack_cursor is None:
        return memory.finish(algorithm(memory, frame))
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    memory.finish(entered)
    returned = memory.finish(algorithm(memory, entered))
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise Boundary('original presentation child return slot changed to ' + str(actual))
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))

def _presentation_sub_long_fields(frame, name, left, right):
    """Full SUB.L defines X/C as the real borrow; MOVE later preserves X."""
    uint(left, 32)
    uint(right, 32)
    value = u32(left - right)
    overflow = bool((left ^ right) & (left ^ value) & 2147483648)
    status = (17 if left < right else 0) | (2 if overflow else 0) | (8 if value & 2147483648 else 0) | (4 if value == 0 else 0)
    return first_replace(frame, **{name: value}, status=status)

def _presentation_random_fields(memory, frame):
    return memory.random_fields(frame)

def collect_battle_special_status_members_fields(memory, frame, side_bits: Word) -> FirstDeploymentFrame:
    """1A78A sole loop: A1 source, A0 destination, A2 status, D1 side bits."""
    frame = _presentation_frame(memory, frame)
    uint(side_bits, 16)
    source, destination, statuses = frame.candidates, frame.roster, frame.controller
    for view in (source, destination, statuses):
        memory.checked_view(view)
    if frame.target_y is not None and low16(frame.target_y) != side_bits:
        raise ValueError('actual incoming D1 low WORD required')
    while True:
        member = source.next_word()
        frame = _first_word(frame, 'target_x', member)
        if negative_word(member):
            return memory.finish(frame)
        member &= 255
        frame = _first_word(frame, 'target_x', member)
        active = bool(statuses.byte(member) & 16)
        if frame.status is not None:
            frame = first_replace(frame, status=(frame.status & 27) | (0 if active else 4))
        if active:
            member |= side_bits
            frame = _first_word(frame, 'target_x', member)
            destination.append_word(member)
            frame = _first_memory_word(frame, member)

def _presentation_collect_first_fields(memory, frame):
    return collect_battle_special_status_members_fields(memory, frame, 0)

def _presentation_collect_second_fields(memory, frame):
    return collect_battle_special_status_members_fields(memory, frame, 2)

def sample_battle_special_status_factor_fields(memory, frame) -> FirstDeploymentFrame:
    """1A706 sole status list / last-maximum selection and parameter draw."""
    frame = _presentation_frame(memory, frame)
    selector = memory.table(0xFFFFEFD2).word()
    frame = _first_word(frame, 'offset_x', selector)
    frame = _first_shift_word(frame, 'offset_x', selector, 1)
    offset = u16(selector << 1)
    second_selector = memory.table(0xFFFFEFD2).word()
    frame = _first_add_word(frame, 'offset_x', offset, second_selector)
    offset = u16(offset + second_selector)
    frame = _first_shift_word(frame, 'offset_x', offset, 3)
    offset = u16(offset << 3)
    destination = memory.table(0xFFFFD300).cursor()
    frame = first_replace(frame, roster=destination,
        controller=memory.table(0xFFFFC700),
        candidates=memory.table(0xFFFFA550).cursor())
    frame = _first_word(frame, 'target_y', 0)
    frame = _presentation_call_fields(memory, frame, 0x1A724, _presentation_collect_first_fields)
    frame = _first_word(frame, 'target_y', 2)
    frame = first_replace(frame, candidates=memory.table(0xFFFFA5A4).cursor())
    frame = _presentation_call_fields(memory, frame, 0x1A730, _presentation_collect_second_fields)
    frame.roster.put_word(65535)
    frame = _first_memory_word(frame, 65535)
    first_member = memory.table(0xFFFFD300).word()
    frame = _first_memory_word(frame, first_member)
    if not negative_word(first_member):
        frame = _first_add_word(frame, 'offset_x', offset, 4)
        offset = u16(offset + 4)
        source = memory.table(0xFFFFD300).cursor()
        strengths = memory.table(0xFFFFB600).cursor()
        frame = first_replace(frame, roster=source, candidates=strengths)
        frame = _first_word(frame, 'target_x', 0)
        best_value, best_member = 0, 2
        while True:
            member = source.next_word()
            frame = _first_word(frame, 'unit', member)
            if negative_word(member):
                break
            frame = _first_word(frame, 'count', member)
            frame = _first_shift_word(frame, 'count', member, 1)
            strength = strengths.word(u16(member << 1))
            frame = _first_word(frame, 'distance', strength)
            frame = _first_compare_word(frame, strength, best_value)
            if strength >= best_value:
                best_value, best_member = strength, member
                frame = _first_word(frame, 'target_y', member)
                frame = _first_word(frame, 'target_x', strength)
        frame = _first_right_word(frame, 'target_y', best_member, 4)
        side = memory.table(0xFFFFF6D6).word()
        frame = _first_word(frame, 'target_x', side)
        selected_side = u16((best_member >> 4) ^ side)
        frame = _first_word(frame, 'target_y', selected_side)
        side_differs = bool(selected_side & 2)
        if frame.status is not None:
            frame = first_replace(frame, status=(frame.status & 27) | (0 if side_differs else 4))
        if side_differs:
            frame = _first_add_word(frame, 'offset_x', offset, 4)
            offset = u16(offset + 4)
    frame = _presentation_call_fields(memory, frame, 0x1A774, _presentation_random_fields)
    sample = low16(frame.target_x)
    frame = _first_long(frame, 'target_x', sample)
    parameters = memory.table(0x1A1DC).cursor()
    frame = first_replace(frame, roster=parameters)
    product = u32(sample * parameters.word(offset))
    frame = _first_long(frame, 'target_x', product)
    swapped = swap_words(product)
    frame = _first_long(frame, 'target_x', swapped)
    base = parameters.word(offset, 2)
    frame = _first_add_word(frame, 'target_x', low16(swapped), base)
    return memory.finish(frame)

def compute_battle_damage_potential_fields(memory, frame, factor: Long) -> FirstDeploymentFrame:
    """1A7A2 retains unclamped D7 independently of clamped D0 and true CCR."""
    frame = _presentation_frame(memory, frame)
    uint(factor, 32)
    if frame.target_x is not None and frame.target_x != factor:
        raise ValueError('actual incoming full D0 factor required')
    factor = u32(low16(factor) * 100)
    frame = _first_long(frame, 'target_x', factor)
    strengths = memory.table(0xFFFFB600).cursor()
    frame = first_replace(frame, roster=strengths)
    opposing = memory.table(0xFFFFF3A6).word()
    frame = _first_word(frame, 'target_y', opposing)
    frame = _first_shift_word(frame, 'target_y', opposing, 1)
    strength = strengths.word(u16(opposing << 1))
    frame = _first_word(frame, 'target_y', strength)
    subtraction = u32(strength * low16(factor))
    frame = _first_long(frame, 'target_y', subtraction)
    acting = memory.table(0xFFFFF3F2).word()
    frame = _first_word(frame, 'target_x', acting)
    frame = _first_shift_word(frame, 'target_x', acting, 1)
    strength = strengths.word(u16(acting << 1))
    frame = _first_word(frame, 'target_x', strength)
    numerator = u32(strength * 1000)
    frame = _first_long(frame, 'target_x', numerator)
    frame = _presentation_sub_long_fields(frame, 'target_x', numerator, subtraction)
    if numerator < subtraction:
        return memory.finish(_first_word(frame, 'choice', 0))
    divisors = memory.table(0xFFFFC000).cursor()
    frame = first_replace(frame, roster=divisors)
    opposing = memory.table(0xFFFFF3A6).word()
    frame = _first_word(frame, 'target_y', opposing)
    frame = _first_shift_word(frame, 'target_y', opposing, 1)
    divisor = divisors.word(u16(opposing << 1))
    frame = _first_word(frame, 'target_y', divisor)
    frame = _first_add_word(frame, 'target_y', divisor, 100)
    divisor = u16(divisor + 100)
    result = divu_retained(u32(numerator - subtraction), divisor)
    # DIVU may overflow: retained D0 is followed immediately by MOVE.W,
    # which overwrites all undefined NZV bits before their next observation.
    frame = first_replace(frame, target_x=result)
    frame = _first_word(frame, 'choice', low16(result))
    frame = _first_compare_word(frame, low16(result), 700)
    if low16(result) > 700:
        frame = _first_word(frame, 'target_x', 700)
    return memory.finish(frame)


# One full city battle loss family, historical APIs only project.
def _damage_store(memory, frame, address, value, width=16):
    """Original memory MOVE width; no numeric carrier is overwritten."""
    uint(value, width)
    if width == 16:
        memory.table(address).set_word(0, value)
        frame = _first_memory_word(frame, value)
    elif width == 32:
        memory.table(address).set_long(0, value)
        status = None if frame.status is None else (frame.status & 16) | (8 if value & 2147483648 else 0) | (4 if value == 0 else 0)
        frame = first_replace(frame, status=status)
    else:
        raise ValueError('actual city damage store width required')
    return memory.finish(frame)

def _damage_save_longs(memory, frame, names):
    """Physical MOVEM or explicitly unobserved historical saved fields."""
    from ..high_level_main_flows.business_movement_support import _movement_save_longs, _movement_address_carrier
    numeric = ('target_x','target_y','unit','count','distance','offset_x','offset_y','choice')
    observed = {name:(frame.carrier(name) if name in numeric else _movement_address_carrier(frame, name)) for name in names}
    if frame.stack_cursor is not None:
        frame = _movement_save_longs(memory.state, frame, names)
    return frame, observed

def _damage_restore_longs(memory, frame, names, observed):
    from ..high_level_main_flows.business_movement_support import _movement_restore_longs
    if frame.stack_cursor is not None:
        frame = _movement_restore_longs(memory.state, frame, names)
    else:
        frame = first_replace(frame, **observed)
    return memory.finish(frame)

def _damage_divide(frame, name, divisor, instruction):
    """Reuse sole packed division; actual exception/undefined CCR is a boundary."""
    from ..high_level_remaining_flows.business_city import _city_movement_divide
    return _city_movement_divide(frame, name, divisor, instruction)

def _damage_shift_long(memory, frame, name, amount):
    from ..high_level_remaining_flows.business_city import _special_action_shift_long
    return _special_action_shift_long(memory.state, frame, name, amount)

def _damage_add_long(memory, frame, name, value):
    from ..high_level_main_flows.business_movement_support import _movement_arithmetic_long
    return _movement_arithmetic_long(memory.state, frame, name, value)

def _damage_bchg_side(memory, frame):
    value = memory.table(0xFFFFF6D7).byte()
    memory.table(0xFFFFF6D7).set_byte(0, value ^ 2)
    status = None if frame.status is None else (frame.status & 27) | (0 if value & 2 else 4)
    return memory.finish(first_replace(frame, status=status))

def _damage_visible_owner(memory, frame):
    """Three live conditional WORD comparisons; no eager visibility reads."""
    owner = memory.table(0xFFFFF68C).word()
    frame = _first_word(frame, 'target_x', owner)
    for address in (0xFFFFF67A, 0xFFFFF67C, 0xFFFFF67E):
        candidate = memory.table(address).word()
        frame = _first_compare_word(frame, owner, candidate)
        if owner == candidate:
            return memory.finish(frame), True
    return memory.finish(frame), False

def _damage_external_call(memory, frame, target, continuation):
    """Current known service or actual slot followed by a truthful boundary."""
    frame = _presentation_frame(memory, frame)
    if frame.stack_cursor is None:
        if target == 0x260E4:
            present_battle_message(memory.state)
        elif target == 0x1072C:
            from .business_services import load_gameplay_scene
            load_gameplay_scene(memory.state)
        else:
            raise Boundary('unknown original city damage child ' + str(target))
        return first_replace(frame, status=None)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = memory.finish(first_replace(frame, stack_cursor=stack))
    if target == 0x260E4:
        from ..high_level_main_flows.business_movement_support import present_battle_message_fields
        returned = present_battle_message_fields(memory.state, entered)
    elif target == 0x1072C:
        from .contexts_services import SceneRefreshMemory
        from .business_services import load_gameplay_scene_fields
        returned = load_gameplay_scene_fields(SceneRefreshMemory(memory.state), entered)
    else:
        returned = memory.state.service_at(target, entered)
    returned = memory.finish(returned)
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise Boundary('original city damage child return slot changed to ' + str(actual))
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))

def _damage_map_fields(memory, frame):
    if frame.stack_cursor is not None:
        from ..high_level_battle_ai.business_actions import _battle_action_map_fields
        from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
        return _battle_action_map_fields(BattlePolicyMemory(memory.state), frame)
    from .business_reuse import load_battlefield_map_context
    terrain = load_battlefield_map_context(memory.state)
    # The old map service did not expose D4 or its final CCR.
    return first_replace(frame, roster=terrain.cursor(), status=None)

def _damage_terrain_fields(memory, frame, x, y, continuation):
    if frame.stack_cursor is not None:
        from ..high_level_battle_ai.business_actions import _deployment_terrain_lookup
        from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
        return _deployment_terrain_lookup(BattlePolicyMemory(memory.state), frame, x, y, continuation)
    from .business_reuse import read_battlefield_terrain_type_observations
    carrier, word, category, extend = read_battlefield_terrain_type_observations(
        memory.state, frame.roster, x, y, frame.target_x)
    status = (16 if extend else 0) | (8 if category & 128 else 0) | (4 if category == 0 else 0)
    return memory.finish(first_replace(frame, target_x=carrier, status=status)), category

def secondary_roster_has_terrain_six_fields(memory, frame):
    """18706..1874A: real seven-LONG frame and shifted terrain coordinates."""
    frame = _presentation_frame(memory, frame)
    names = ('target_x','target_y','unit','count','roster','candidates','controller')
    frame, saved = _damage_save_longs(memory, frame, names)
    frame = _presentation_call_fields(memory, frame, 0x1870E, _damage_map_fields)
    roster = memory.table(0xFFFFA5A4).cursor()
    positions = memory.table(0xFFFFA150).cursor()
    frame = first_replace(frame, candidates=roster, controller=positions)
    selected = False
    while True:
        member = roster.next_word()
        frame = _first_word(frame, 'count', member)
        if negative_word(member):
            break
        offset = u16(member << 2)
        frame = _first_shift_word(frame, 'count', member, 2)
        x = positions.word(offset)
        frame = _first_word(frame, 'target_y', x)
        frame = _first_right_word(frame, 'target_y', x, 7)
        y = positions.word(offset, 2)
        frame = _first_word(frame, 'unit', y)
        frame = _first_right_word(frame, 'unit', y, 7)
        frame, category = _damage_terrain_fields(memory, frame, x >> 7, y >> 7, 0x1872E)
        from ..high_level_battle_ai.business_actions import _deployment_compare_byte
        frame = _deployment_compare_byte(memory, frame, category, 6)
        if category == 6:
            selected = True
            break
    frame = _damage_restore_longs(memory, frame, names, saved)
    memory.finish(frame)
    memory.state.set_status_word((memory.state.read_status_word() & 65534) | int(selected))
    return first_replace(frame, status=memory.state.sr & 31), selected

def award_city_reserve_attrition_fields(memory, frame):
    """185E4..18706: packed loss, underflow query and original defeat notice."""
    frame = _presentation_frame(memory, frame)
    outer_names = ('target_y','roster')
    frame, outer = _damage_save_longs(memory, frame, outer_names)
    frame = _presentation_call_fields(memory, frame, 0x185EE, _presentation_random_fields)
    frame = _first_long(frame, 'target_x', frame.target_x & 65535)
    frame = _first_long(frame, 'target_y', frame.target_x)
    frame = _damage_shift_long(memory, frame, 'target_x', 1)
    frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)
    frame = _damage_shift_long(memory, frame, 'target_x', 1)
    frame = _first_long(frame, 'target_x', swap_words(frame.target_x))
    frame = _first_add_word(frame, 'target_x', low16(frame.target_x), 10)
    frame = _first_long(frame, 'target_y', 0)
    factor = memory.table(0xFF3ED6).word()
    frame = _first_word(frame, 'target_y', factor)
    frame = _first_add_word(frame, 'target_y', factor, 100)
    frame = _damage_divide(frame, 'target_y', 10, 0x1860E)
    frame = _first_long(frame, 'target_x', low16(frame.target_x) * low16(frame.target_y))
    previous = memory.table(0xFF3ED2).long()
    frame = _first_long(frame, 'target_y', previous)
    frame = _damage_add_long(memory, frame, 'target_y', 500)
    frame = _damage_divide(frame, 'target_y', 100, 0x18620)
    frame = _first_long(frame, 'target_x', low16(frame.target_x) * low16(frame.target_y))
    actor = memory.table(0xFFFFF3F2).word()
    frame = _first_word(frame, 'unit', actor)
    frame = _first_shift_word(frame, 'unit', actor, 1)
    offset = u16(actor << 1)
    abilities = memory.table(0xFFFFB400).cursor()
    frame = first_replace(frame, roster=abilities)
    ability = abilities.word(offset)
    frame = _first_word(frame, 'target_y', ability)
    readiness = memory.table(0xFFFFB600).cursor()
    frame = first_replace(frame, roster=readiness)
    frame = _first_add_word(frame, 'target_y', ability, readiness.word(offset))
    frame = _first_long(frame, 'target_y', frame.target_y & 65535)
    frame = _damage_divide(frame, 'target_y', 10, 0x18642)
    frame = _first_long(frame, 'target_x', low16(frame.target_x) * low16(frame.target_y))
    frame = _damage_divide(frame, 'target_x', 20000, 0x18648)
    shortage = memory.table(0xFF3EDA).word()
    frame = _first_memory_word(frame, shortage)
    if shortage:
        loss = low16(frame.target_x)
        frame = _first_word(frame, 'target_y', loss)
        frame = _first_shift_word(frame, 'target_x', loss, 1)
        frame = _first_add_word(frame, 'target_x', u16(loss << 1), loss)
        frame = _first_shift_word(frame, 'target_x', u16(loss * 3), 1)
        frame = _first_long(frame, 'target_x', frame.target_x & 65535)
        frame = _damage_divide(frame, 'target_x', 10, 0x18664)
    scene = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'unit', scene)
    frame = _first_shift_word(frame, 'unit', scene, 2)
    offset = u16(scene << 2)
    reserves = memory.table(0xFFFFE59C).cursor()
    frame = first_replace(frame, roster=reserves)
    previous = reserves.long(offset)
    frame = _first_long(frame, 'target_y', previous)
    from ..high_level_battle_ai.business_formation import _first_sub_word
    loss = low16(frame.target_x)
    frame = _first_sub_word(frame, 'target_y', low16(previous), loss)
    if low16(previous) < loss:
        inner_names = ('target_x','unit','roster')
        frame, inner = _damage_save_longs(memory, frame, inner_names)
        frame = _presentation_call_fields(memory, frame, 0x18684, _damage_terrain_query_fields)
        if not frame.status & 1:
            frame, visible = _damage_visible_owner(memory, frame)
            if visible:
                frame = _damage_store(memory, frame, 0xFF7026, 24)
                frame = _damage_external_call(memory, frame, 0x1072C, 0x186B2)
            saved_owner = memory.table(0xFFFFF376).word()
            frame = _first_memory_word(frame, saved_owner)
            if frame.stack_cursor is not None:
                stack = frame.stack_cursor.advance(-2)
                stack.set_word(0, saved_owner)
                frame = first_replace(frame, stack_cursor=stack)
            frame = _damage_store(memory, frame, 0xFFFFF376, memory.table(0xFFFFF68C).word())
            owner = memory.table(0xFFFFF68E).word()
            frame = _first_word(frame, 'target_x', owner)
            frame = _first_shift_word(frame, 'target_x', owner, 1)
            heads = memory.table(0xFFFFE640).cursor()
            frame = first_replace(frame, roster=heads)
            frame = _damage_store(memory, frame, 0xFFFFF3D0, heads.word(u16(owner << 1)))
            frame = _damage_store(memory, frame, 0xFFFFF740, 319)
            frame = _damage_bchg_side(memory, frame)
            frame = _damage_external_call(memory, frame, 0x260E4, 0x186DE)
            frame = _damage_bchg_side(memory, frame)
            if frame.stack_cursor is not None:
                saved_owner = frame.stack_cursor.word()
                frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
            frame = _damage_store(memory, frame, 0xFFFFF376, saved_owner)
            frame = _damage_store(memory, frame, 0xFFFFF612, 1041)
            memory.table(0xFFFFF362).word()
            frame = _damage_store(memory, frame, 0xFFFFF362, 0)
            memory.table(0xFFFFF6D6).word()
            frame = _damage_store(memory, frame, 0xFFFFF6D6, 0)
            frame = _first_word(frame, 'target_y', 0)
        frame = _damage_restore_longs(memory, frame, inner_names, inner)
    remaining = low16(frame.target_y)
    restored_offset = offset if frame.unit is None else low16(frame.unit)
    frame.roster.set_word(restored_offset, remaining, 2)
    frame = _first_memory_word(frame, remaining)
    frame = _damage_restore_longs(memory, frame, outer_names, outer)
    return memory.finish(frame)

def _damage_terrain_query_fields(memory, frame):
    return secondary_roster_has_terrain_six_fields(memory, frame)[0]

def _damage_potential_fields(memory, frame):
    return compute_battle_damage_potential_fields(memory, frame, frame.target_x)

def _damage_raise_ability_fields(memory, frame, view, offset, increment):
    value = view.word(offset)
    frame = _first_word(frame, 'target_y', value)
    frame = _first_add_word(frame, 'target_y', value, increment)
    value = u16(value + increment)
    frame = _first_compare_word(frame, value, 999)
    if value > 999:
        value = 999
        frame = _first_word(frame, 'target_y', value)
    view.set_word(offset, value)
    return _first_memory_word(frame, value)

def resolve_city_battle_damage_fields(memory, frame):
    """183F8..185AE: sole city debit, mutual losses and reserve/progress award.

    Returns actual full frame plus the old API's separately observed award.
    The actual final D0 is the tested owner, not that old scalar return value.
    """
    frame = _presentation_frame(memory, frame)
    frame = _presentation_call_fields(memory, frame, 0x183FE, _presentation_random_fields)
    scene = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_x', scene)
    frame = _first_shift_word(frame, 'target_x', scene, 2)
    reserves = memory.table(0xFFFFE59C).cursor()
    frame = first_replace(frame, roster=reserves)
    amount = reserves.long(u16(scene << 2))
    frame = _first_long(frame, 'target_x', amount)
    frame = _first_long(frame, 'target_y', 0)
    seed = memory.table(0xFFFFF61C).word()
    frame = _first_word(frame, 'target_y', seed)
    frame = _first_long(frame, 'unit', frame.target_y)
    frame = _damage_shift_long(memory, frame, 'target_y', 1)
    frame = _damage_add_long(memory, frame, 'target_y', frame.unit)
    frame = _damage_shift_long(memory, frame, 'target_y', 1)
    frame = _first_long(frame, 'target_y', swap_words(frame.target_y))
    frame = _first_add_word(frame, 'target_y', low16(frame.target_y), 5)
    frame = _first_long(frame, 'target_x', low16(amount) * low16(frame.target_y))
    debit = frame.target_x
    side = memory.table(0xFFFFF6D6).word()
    frame = _first_word(frame, 'target_y', side)
    frame = _first_shift_word(frame, 'target_y', side, 2)
    address = memory.table(0x183F0).long(u16(side << 2))
    resources = memory.table(address).cursor()
    frame = first_replace(frame, roster=resources)
    frame = _first_word(frame, 'offset_y', 0)
    available = resources.long()
    frame = _first_long(frame, 'target_y', available)
    frame = _presentation_sub_long_fields(frame, 'target_y', available, debit)
    shortage = available < debit
    if shortage:
        frame = _first_long(frame, 'target_y', 0)
        frame = _first_word(frame, 'offset_y', 1)
    frame = _damage_store(memory, frame, 0xFF3EDA, int(shortage))
    resources.set_long(0, frame.target_y)
    status = None if frame.status is None else (frame.status & 16) | (8 if frame.target_y & 2147483648 else 0) | (4 if frame.target_y == 0 else 0)
    frame = first_replace(frame, status=status)
    troops = memory.table(0xFFFFC800).cursor()
    frame = first_replace(frame, roster=troops)
    actor = memory.table(0xFFFFF3F2).word()
    frame = _first_word(frame, 'target_x', actor)
    frame = _first_shift_word(frame, 'target_x', actor, 2)
    frame = _damage_store(memory, frame, 0xFF3ED2, troops.long(u16(actor << 2)), 32)
    frame = _damage_store(memory, frame, 0xFF3ED6, 1792)
    opposing = memory.table(0xFFFFF3A6).word()
    frame = _first_memory_word(frame, opposing)
    if not negative_word(opposing):
        frame = _presentation_call_fields(memory, frame, 0x1846A, sample_battle_special_status_factor_fields)
        frame = _presentation_call_fields(memory, frame, 0x18470, _damage_potential_fields)
        frame = _damage_apply_mutual_losses_fields(memory, frame)
    frame = _presentation_call_fields(memory, frame, 0x1855A, award_city_reserve_attrition_fields)
    award = frame.target_x
    actor = memory.table(0xFFFFF3F2).word()
    frame = _first_word(frame, 'unit', actor)
    frame = _first_shift_word(frame, 'unit', actor, 1)
    progress = memory.table(0xFFFFBE00).cursor()
    frame = first_replace(frame, roster=progress)
    frame = _damage_raise_ability_fields(memory, frame, progress, u16(actor << 1), low16(award))
    frame, visible = _damage_visible_owner(memory, frame)
    if visible:
        mode = memory.table(0xFFFFF612).word()
        frame = _first_compare_word(frame, mode, 1041)
        if mode != 1041:
            frame = _damage_store(memory, frame, 0xFF7026, 24)
            frame = _damage_external_call(memory, frame, 0x1072C, 0x185AC)
    return memory.finish(frame), award

def _damage_apply_mutual_losses_fields(memory, frame):
    """18470..18556: retain original DIVU overflow data through real MOVE/TST.

    Each division below is immediately followed by an original MOVE.W
    or TST.W. These instructions define NZVC and preserve DIVU's unchanged
    X. Compose the returned frame only after that real instruction; no
    undefined intermediate N/Z is guessed, exposed or used as a branch.
    divu_retained remains the sole numerical division authority and
    still stops on an original zero divisor before the following DATA.
    """
    frame = _damage_store(memory, frame, 0xFF3ED6, low16(frame.choice))
    frame = _first_add_word(frame, 'choice', low16(frame.choice), 200)
    scene = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_x', scene)
    frame = _first_shift_word(frame, 'target_x', scene, 2)
    reserves = memory.table(0xFFFFE59C).cursor()
    frame = first_replace(frame, roster=reserves)
    amount = reserves.long(u16(scene << 2))
    frame = _first_long(frame, 'target_x', amount)
    frame = _first_word(frame, 'target_y', 100)
    from ..high_level_battle_ai.business_formation import _first_sub_word
    frame = _first_sub_word(frame, 'target_y', 100, low16(amount))
    frame = _first_long(frame, 'choice', low16(frame.choice) * low16(frame.target_y))
    retained_choice = divu_retained(frame.choice, 100)
    actor = memory.table(0xFFFFF3F2).word()
    frame = first_replace(_first_word(frame, 'target_x', actor), choice=retained_choice)
    frame = _first_shift_word(frame, 'target_x', actor, 1)
    ability = memory.table(0xFFFFC000).cursor()
    frame = first_replace(frame, roster=ability)
    actor_ability = ability.word(u16(actor << 1))
    frame = _first_word(frame, 'target_x', actor_ability)
    frame = _first_long(frame, 'choice', low16(frame.choice) * actor_ability)
    retained_choice = divu_retained(frame.choice, 100)
    shortage = memory.table(0xFF3EDA).word()
    frame = first_replace(_first_memory_word(frame, shortage), choice=retained_choice)
    if shortage:
        frame = _first_long(frame, 'choice', frame.choice & 65535)
        frame = _damage_shift_long(memory, frame, 'choice', 2)
        retained_choice = divu_retained(frame.choice, 10)
    else:
        retained_choice = frame.choice
    opposing = memory.table(0xFFFFF3A6).word()
    frame = first_replace(_first_word(frame, 'target_x', opposing), choice=retained_choice)
    frame = _first_shift_word(frame, 'target_x', opposing, 2)
    troops = memory.table(0xFFFFC800).cursor()
    frame = first_replace(frame, roster=troops)
    original = troops.long(u16(opposing << 2))
    frame = _first_long(frame, 'target_y', original)
    damage = low16(frame.choice)
    frame = _first_sub_word(frame, 'target_y', low16(original), damage)
    if low16(original) < damage:
        frame = _first_word(frame, 'target_y', 0)
    troops.set_long(u16(opposing << 2), frame.target_y)
    frame = _first_long(frame, 'target_y', frame.target_y)
    frame = _first_long(frame, 'offset_x', 0)
    frame = _first_word(frame, 'offset_x', damage)
    frame = _damage_shift_long(memory, frame, 'offset_x', 1)
    retained_offset = divu_retained(frame.offset_x, 400)
    actor = memory.table(0xFFFFF3F2).word()
    frame = first_replace(_first_word(frame, 'target_x', actor), offset_x=retained_offset)
    frame = _first_shift_word(frame, 'target_x', actor, 1)
    offset = u16(actor << 1)
    ability = memory.table(0xFFFFC000).cursor()
    frame = first_replace(frame, roster=ability)
    original_ability = ability.word(offset)
    frame = _first_word(frame, 'target_y', original_ability)
    frame = _first_word(frame, 'unit', original_ability)
    frame = _first_add_word(frame, 'target_y', original_ability, low16(frame.offset_x))
    new_ability = u16(original_ability + low16(frame.offset_x))
    frame = _first_compare_word(frame, new_ability, 999)
    if new_ability > 999:
        new_ability = 999
        frame = _first_word(frame, 'target_y', new_ability)
    ability.set_word(offset, new_ability)
    frame = _first_memory_word(frame, new_ability)
    frame = _first_long(frame, 'choice', low16(frame.choice) * 2000)
    retained_choice = divu_retained(frame.choice, original_ability)
    shortage = memory.table(0xFF3EDA).word()
    frame = first_replace(_first_memory_word(frame, shortage), choice=retained_choice)
    if shortage:
        frame = _first_shift_word(frame, 'choice', low16(frame.choice), 1)
    frame = _first_shift_word(frame, 'target_x', offset, 1)
    offset = u16(offset << 1)
    troops = memory.table(0xFFFFC800).cursor()
    frame = first_replace(frame, roster=troops)
    original = troops.long(offset)
    frame = _first_long(frame, 'target_y', original)
    damage = low16(frame.choice)
    frame = _first_sub_word(frame, 'target_y', low16(original), damage)
    if low16(original) < damage:
        frame = _first_word(frame, 'target_y', 0)
    troops.set_long(offset, frame.target_y)
    frame = _first_long(frame, 'target_y', frame.target_y)
    frame = _first_long(frame, 'choice', frame.choice & 65535)
    retained_choice = divu_retained(frame.choice, 400)
    opposing = memory.table(0xFFFFF3A6).word()
    frame = first_replace(_first_word(frame, 'target_x', opposing), choice=retained_choice)
    frame = _first_shift_word(frame, 'target_x', opposing, 1)
    ability = memory.table(0xFFFFC000).cursor()
    frame = first_replace(frame, roster=ability)
    return _damage_raise_ability_fields(memory, frame, ability, u16(opposing << 1), low16(frame.choice))


# Sole live postbattle resources, candidates and progression.
def _postbattle_compare_byte_fields(frame, left, right):
    """CMP.B keeps the observed X; absent legacy X remains unobserved."""
    left, right = u8(left), u8(right)
    value = u8(left - right)
    overflow = bool((left ^ right) & (left ^ value) & 128)
    status = None if frame.status is None else (frame.status & 16) | (1 if left < right else 0) | (8 if value & 128 else 0) | (4 if value == 0 else 0) | (2 if overflow else 0)
    return first_replace(frame, status=status)


def _postbattle_memory_byte_fields(frame, value):
    value = u8(value)
    status = None if frame.status is None else (frame.status & 16) | (8 if value & 128 else 0) | (4 if value == 0 else 0)
    return first_replace(frame, status=status)


def _postbattle_decrement_fields(frame, name, value):
    """DBRA changes the counter WORD, never the preceding comparison CCR."""
    retained = frame.carrier(name)
    result = None if retained is None else replace_word(retained, u16(value - 1))
    return first_replace(frame, **{name: result})


def _postbattle_candidates_fields(memory, frame, battlefield, continuation=None):
    """Two actual descending candidate builders share one live-list policy.

    The separate WORD count is an observation, not a fabricated full D3.
    A supplied continuation is the parent's real BSR slot, owned only here.
    """
    frame = _presentation_frame(memory, frame)
    if continuation is not None and frame.stack_cursor is not None:
        stack = frame.stack_cursor.advance(-4)
        stack.set_long(0, continuation)
        frame = first_replace(frame, stack_cursor=stack)
    source = memory.table(0xFFFFA050 if battlefield else 0xFFFFCC00).cursor()
    destination = memory.table(0xFFFFD300).cursor()
    frame = first_replace(frame, roster=source, candidates=destination)
    city = memory.table(0xFFFFF68A).word()
    if battlefield:
        assignments = memory.table(0xFFFFCC00).cursor()
        frame = first_replace(frame, controller=assignments)
        frame = _first_word(frame, 'target_x', city)
        index_name, city_name = 'unit', 'target_x'
    else:
        index_name, city_name = 'target_y', 'unit'
    frame = _first_word(frame, index_name, 255)
    if not battlefield:
        frame = _first_word(frame, city_name, city)
    frame = _first_word(frame, 'count', 0)
    count = 0
    for officer in descending_inclusive(255):
        assigned = source.byte(officer)
        frame = _postbattle_compare_byte_fields(frame, low8(city), assigned)
        selected = assigned == low8(city)
        if selected and battlefield:
            assignment = assignments.byte(officer)
            frame = _postbattle_memory_byte_fields(frame, assignment)
            selected = not negative_byte(assignment)
        if selected:
            destination.set_word(0, officer)
            destination = destination.advance(2)
            frame = first_replace(frame, candidates=destination)
            frame = _first_memory_word(frame, officer)
            frame = _first_add_word(frame, 'count', count, 1)
            count = u16(count + 1)
        frame = _postbattle_decrement_fields(frame, index_name, officer)
    destination.set_word(0, 65535)
    frame = _first_memory_word(frame, 65535)
    if continuation is not None and frame.stack_cursor is not None:
        actual = frame.stack_cursor.long()
        if actual != continuation:
            raise Boundary('actual postbattle candidate return changed to ' + str(actual))
        frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(4))
    return memory.finish(frame), count


def build_city_assigned_outcome_candidates_fields(memory, frame):
    """1C2A0..1C2C8: exact assignment matches, descending WORD roster."""
    return _postbattle_candidates_fields(memory, frame, False)


def build_battlefield_outcome_candidates_fields(memory, frame):
    """1C2C8..1C2FC: linked officers with nonnegative live assignments."""
    return _postbattle_candidates_fields(memory, frame, True)


def _postbattle_fraction_fields(memory, frame, multiplier, base, continuation):
    """Actual RNG child plus the original fixed-width scale construction."""
    frame = _presentation_call_fields(memory, frame, continuation, _presentation_random_fields)
    if multiplier in (501, 61):
        frame = _first_long(frame, 'target_x', low16(frame.target_x) * multiplier)
    else:
        frame = _first_long(frame, 'target_x', frame.target_x & 65535)
        if multiplier != 16:
            frame = _first_long(frame, 'target_y', frame.target_x)
        if multiplier in (13, 25, 51, 6):
            frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 1)
            frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)
            frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 2 if multiplier == 13 else 1 if multiplier == 6 else 3)
            if multiplier != 6:
                frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)
            if multiplier == 51:
                frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 1)
                frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)
        elif multiplier == 40:
            frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 2)
            frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)
            frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 3)
        elif multiplier in (30, 60):
            frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 4)
            frame = _presentation_sub_long_fields(frame, 'target_x', frame.target_x, frame.target_y)
            frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 1 if multiplier == 30 else 2)
        elif multiplier == 31:
            frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 5)
            frame = _presentation_sub_long_fields(frame, 'target_x', frame.target_x, frame.target_y)
        elif multiplier == 11:
            frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 2)
            frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)
            frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 1)
            frame = _damage_add_long(memory, frame, 'target_x', frame.target_y)
        elif multiplier == 16:
            frame = _postbattle_shift_long_fields(memory, frame, 'target_x', 4)
        else:
            raise ValueError('closed original postbattle scale required')
    frame = _first_long(frame, 'target_x', swap_words(frame.target_x))
    if base:
        frame = _first_add_word(frame, 'target_x', low16(frame.target_x), base)
    return frame


def _postbattle_city_resource_fields(memory, frame, address, index_name='target_y'):
    view = memory.table(address).cursor()
    frame = first_replace(frame, roster=view)
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, index_name, city)
    frame = _first_shift_word(frame, index_name, city, 2)
    return frame, view, u16(city << 2)


def _postbattle_loss_fields(frame, amount, divisor, instruction):
    frame = _first_long(frame, 'target_x', low16(frame.target_x) * low16(amount))
    return _damage_divide(frame, 'target_x', divisor, instruction)


def sample_city_postbattle_reserve_fields(memory, frame):
    """1C554..1C57C: write only reserve's low WORD; D0 retains packed scale."""
    frame = _presentation_frame(memory, frame)
    frame = _postbattle_fraction_fields(memory, frame, 13, 0, 0x1C55A)
    frame, reserves, offset = _postbattle_city_resource_fields(memory, frame, 0xFFFFE59C)
    reserves.set_word(offset, low16(frame.target_x), 2)
    return memory.finish(_first_memory_word(frame, low16(frame.target_x)))


def distribute_city_battle_progress_fields(memory, frame):
    """1C57C..1C5E2: select larger live metric, preserving duplicate reads."""
    frame, count = _postbattle_candidates_fields(memory, frame, False, 0x1C580)
    budget = memory.table(0xFFFFEFB8).word()
    frame = _first_word(frame, 'target_x', budget)
    frame = _first_shift_word(frame, 'target_x', budget, 1)
    return _postbattle_progress_tail_fields(memory, frame, count)


def apply_assigned_city_light_attrition_fields(memory, frame):
    """1C69E..1C732: independent troop/readiness draws and actual WORD loss."""
    frame, _ = _postbattle_candidates_fields(memory, frame, False, 0x1C6A2)
    roster = memory.table(0xFFFFD300).cursor()
    troops, readiness = memory.table(0xFFFFC800).cursor(), memory.table(0xFFFFB200).cursor()
    frame = first_replace(frame, roster=roster, candidates=troops, controller=readiness,
        scan=memory.table(0xFFFFC000).cursor(), opponent=memory.table(0xFFFFC700).cursor(),
        scratch=memory.table(0xFFFFCC00).cursor(), auxiliary=memory.table(0xFFFFF45E).cursor())
    frame = _first_word(frame, 'choice', 0)
    total = 0
    from ..high_level_battle_ai.business_formation import _first_sub_word
    while True:
        member = roster.word()
        roster = roster.advance(2)
        frame = first_replace(frame, roster=roster)
        frame = _first_word(frame, 'unit', member)
        if negative_word(member):
            memory.table(0xFFFFEFBA).set_word(0, total)
            return memory.finish(_first_memory_word(frame, total))
        frame = _first_shift_word(frame, 'unit', member, 2)
        offset = u16(member << 2)
        original = troops.long(offset)
        frame = _first_long(frame, 'count', original)
        frame = _postbattle_fraction_fields(memory, frame, 31, 30, 0x1C6D2)
        frame = _postbattle_loss_fields(frame, original, 100, 0x1C6E6)
        frame = _first_sub_word(frame, 'count', low16(original), low16(frame.target_x))
        troops.set_word(offset, low16(frame.count), 2)
        frame = _first_memory_word(frame, low16(frame.count))
        frame = _first_long(frame, 'target_x', frame.target_x & 65535)
        frame = _damage_divide(frame, 'target_x', 400, 0x1C6F6)
        frame = _first_add_word(frame, 'choice', total, low16(frame.target_x))
        total = u16(total + low16(frame.target_x))
        frame = _first_right_word(frame, 'unit', offset, 1)
        offset >>= 1
        original = readiness.word(offset)
        frame = _first_word(frame, 'count', original)
        frame = _postbattle_fraction_fields(memory, frame, 31, 0, 0x1C708)
        frame = _postbattle_loss_fields(frame, original, 100, 0x1C718)
        frame = _first_sub_word(frame, 'count', original, low16(frame.target_x))
        remaining = u16(original - low16(frame.target_x))
        if remaining == 0:
            remaining = 1
            frame = _first_word(frame, 'count', remaining)
        readiness.set_word(offset, remaining)
        frame = _first_memory_word(frame, remaining)


def _postbattle_gold_debit_fields(memory, frame, continuation, word_borrow):
    frame = _postbattle_fraction_fields(memory, frame, 501, 500, continuation)
    frame, gold, offset = _postbattle_city_resource_fields(memory, frame, 0xFFFFDFFC)
    original = gold.long(offset)
    frame = _first_long(frame, 'unit', original)
    frame = _first_long(frame, 'target_x', frame.target_x & 65535)
    cost = frame.target_x
    if word_borrow:
        from ..high_level_battle_ai.business_formation import _first_sub_word
        frame = _first_sub_word(frame, 'unit', low16(original), low16(cost))
        insufficient = low16(original) < low16(cost)
    else:
        frame = _presentation_sub_long_fields(frame, 'unit', original, cost)
        insufficient = original < cost
    if insufficient:
        frame = _first_long(frame, 'unit', 0)
    gold.set_long(offset, frame.unit)
    return _first_long(frame, 'unit', frame.unit)


def consume_city_battle_supply_long_fields(memory, frame):
    """1C732..1C78C: packed DIVU result is subtracted as a full LONG."""
    frame = _presentation_frame(memory, frame)
    amount = memory.table(0xFFFFEFBC).word()
    frame = _first_word(frame, 'target_x', amount)
    frame = _first_long(frame, 'target_x', amount * 90)
    frame, supply, offset = _postbattle_city_resource_fields(memory, frame, 0xFFFFED84)
    original = supply.long(offset)
    frame = _first_long(frame, 'unit', original)
    frame = _postbattle_loss_fields(frame, original, 1000, 0x1C74A)
    loss = frame.target_x
    frame = _presentation_sub_long_fields(frame, 'unit', original, loss)
    if original < loss:
        frame = _first_long(frame, 'unit', 0)
    supply.set_long(offset, frame.unit)
    frame = _first_long(frame, 'unit', frame.unit)
    return memory.finish(_postbattle_gold_debit_fields(memory, frame, 0x1C760, False))


def reduce_city_reserve_after_defeat_fields(memory, frame):
    """1C78C..1C7C4: only low reserve WORD changes, upper LONG is retained."""
    frame = _presentation_frame(memory, frame)
    frame = _postbattle_fraction_fields(memory, frame, 51, 0, 0x1C792)
    frame, reserves, offset = _postbattle_city_resource_fields(memory, frame, 0xFFFFE59C)
    original = reserves.long(offset)
    frame = _first_long(frame, 'unit', original)
    frame = _postbattle_loss_fields(frame, original, 100, 0x1C7B8)
    from ..high_level_battle_ai.business_formation import _first_sub_word
    frame = _first_sub_word(frame, 'unit', low16(original), low16(frame.target_x))
    reserves.set_word(offset, low16(frame.unit), 2)
    return memory.finish(_first_memory_word(frame, low16(frame.unit)))


def consume_city_battle_supply_word_fields(memory, frame):
    """1C7C4..1C82C: distinct WORD supply and WORD-borrow/LONG gold stores."""
    frame = _presentation_frame(memory, frame)
    frame = _postbattle_fraction_fields(memory, frame, 25, 50, 0x1C7CA)
    frame, supply, offset = _postbattle_city_resource_fields(memory, frame, 0xFFFFED84)
    original = supply.long(offset)
    frame = _first_long(frame, 'unit', original)
    frame = _postbattle_loss_fields(frame, original, 100, 0x1C7F0)
    from ..high_level_battle_ai.business_formation import _first_sub_word
    frame = _first_sub_word(frame, 'unit', low16(original), low16(frame.target_x))
    supply.set_word(offset, low16(frame.unit), 2)
    frame = _first_memory_word(frame, low16(frame.unit))
    return memory.finish(_postbattle_gold_debit_fields(memory, frame, 0x1C800, True))


def clear_city_officer_links_fields(memory, frame):
    """1CC76..1CC94: matching links are read again before original CLR.B."""
    frame = _presentation_frame(memory, frame)
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_x', city)
    links = memory.table(0xFFFFA050).cursor()
    frame = first_replace(frame, roster=links)
    frame = _first_word(frame, 'target_y', 255)
    for officer in descending_inclusive(255):
        value = links.byte(officer)
        frame = _postbattle_compare_byte_fields(frame, low8(city), value)
        if value == low8(city):
            links.byte(officer)
            links.set_byte(officer, 0)
            frame = _postbattle_memory_byte_fields(frame, 0)
        frame = _postbattle_decrement_fields(frame, 'target_y', officer)
    return memory.finish(frame)


def reassign_city_flagged_officers_fields(memory, frame):
    """1CC94..1CCBE: original bit-six token and owner+41 BYTE writes."""
    frame = _presentation_frame(memory, frame)
    owner = memory.table(0xFFFFF68E).word()
    frame = _first_word(frame, 'target_x', owner)
    frame = _first_add_word(frame, 'target_x', owner, 41)
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_y', city)
    retained = frame.target_y
    status = None if frame.status is None else (frame.status & 27) | (0 if city & 64 else 4)
    frame = first_replace(frame, target_y=None if retained is None else retained | 64, status=status)
    assignments = memory.table(0xFFFFCC00).cursor()
    frame = first_replace(frame, roster=assignments)
    frame = _first_word(frame, 'unit', 255)
    for officer in descending_inclusive(255):
        value = assignments.byte(officer)
        frame = _postbattle_compare_byte_fields(frame, low8(city | 64), value)
        if value == low8(city | 64):
            assignments.set_byte(officer, low8(owner + 41))
            frame = _postbattle_memory_byte_fields(frame, low8(owner + 41))
        frame = _postbattle_decrement_fields(frame, 'unit', officer)
    return memory.finish(frame)


def apply_postbattle_city_economic_attrition_fields(memory, frame):
    """217C8..21854: three independent draws and the original mixed widths."""
    frame = _presentation_frame(memory, frame)
    frame = _postbattle_fraction_fields(memory, frame, 16, 5, 0x217CE)
    # This entry loads D2 before A0, unlike the neighboring supply routines.
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'unit', city)
    frame = _first_shift_word(frame, 'unit', city, 2)
    offset = u16(city << 2)
    from ..high_level_battle_ai.business_formation import _first_sub_word
    for address, second in ((0xFFFFE1DC, False), (0xFFFFE13C, True)):
        if second:
            frame = _postbattle_fraction_fields(memory, frame, 11, 0, 0x217FE)
        target = memory.table(address).cursor()
        frame = first_replace(frame, roster=target)
        original = target.long(offset)
        frame = _first_long(frame, 'count', original)
        frame = _first_long(frame, 'distance', original)
        frame = _first_long(frame, 'distance', low16(original) * low16(frame.target_x))
        frame = _damage_divide(frame, 'distance', 100, 0x2181C if second else 0x217EE)
        frame = _first_sub_word(frame, 'count', low16(original), low16(frame.distance))
        target.set_long(offset, frame.count)
        frame = _first_long(frame, 'count', frame.count)
    frame = _postbattle_fraction_fields(memory, frame, 6, 5, 0x2182C)
    target = memory.table(0xFFFFE31C).cursor()
    frame = first_replace(frame, roster=target)
    original = target.word(offset, 2)
    frame = _first_word(frame, 'count', original)
    loss = low16(frame.target_x)
    frame = _first_sub_word(frame, 'count', original, loss)
    if original < loss:
        frame = _first_word(frame, 'count', 0)
    target.set_word(offset, low16(frame.count), 2)
    return memory.finish(_first_memory_word(frame, low16(frame.count)))


def _postbattle_shift_long_fields(memory, frame, name, amount):
    """Share existing closed shift cores; postbattle adds no second arithmetic."""
    if amount in (3, 5):
        from ..high_level_remaining_flows.business_city import _settlement_shift_sample_long_fields
        return _settlement_shift_sample_long_fields(memory.state, frame, name, amount)
    return _damage_shift_long(memory, frame, name, amount)

from .contexts_reuse import project_gameplay_arrival_fields


def _city_outcome_frame_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame, entry: int) -> FirstDeploymentFrame:
    """Only actual full Scene entry fields; legacy scalar calls remain unknown."""
    from ..high_level_scene_flows.domain import SceneState
    from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
    from ..high_level_main_flows.business_movement_support import _movement_frame
    frame = _presentation_frame(memory, frame)
    if type(memory.state) is not SceneState or any(value is None for value in (
            frame.target_x, frame.target_y, frame.unit, frame.count, frame.distance,
            frame.offset_x, frame.offset_y, frame.choice, frame.roster,
            frame.candidates, frame.controller, frame.scan, frame.opponent,
            frame.scratch, frame.auxiliary, frame.stack_cursor, frame.status)):
        raise MovementContinuationBoundary(entry, frame,
            'city outcome requires actual retained fields and entry A7, not a zero scalar frame')
    return _movement_frame(memory.state, frame)


def _city_outcome_child_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame, target: int) -> FirstDeploymentFrame:
    """Closed direct children of the three original outcome functions."""
    from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
    if target == 0x1c2fc:
        return apply_battlefield_ratio_losses_fields(memory, frame)
    if target == 0x1c39c:
        return apply_city_assigned_heavy_losses_fields(memory, frame)
    if target == 0x1c5ee:
        return apply_battlefield_heavy_losses_and_detach_fields(memory, frame)
    if target == 0x1c82c:
        return rebuild_primary_after_battle_fields(memory, frame)
    if target == 0x1c8bc:
        return sort_returning_officer_status_fields(memory, frame)
    if target == 0x1c942:
        return partition_city_survivors_fields(memory, frame)
    if target == 0x1c9fe:
        return owner_has_other_city_carry_fields(memory, frame)
    if target == 0x1ca3c:
        return restore_returning_officer_assignments_fields(memory, frame)
    if target == 0x1ca60:
        return allocate_packed_group_resources_fields(memory, frame)
    if target == 0x1cb08:
        return rebuild_secondary_after_battle_fields(memory, frame)
    if target == 0x1C5E2:
        return distribute_battlefield_battle_progress_fields(memory, frame)
    if target == 0x208CE:
        from .business_reuse import apply_returning_officer_loyalty_fields
        return apply_returning_officer_loyalty_fields(memory, frame)
    if target == 0x5f48:
        return build_roster_fields(memory, frame)
    if target == 0xe1f6:
        return choose_city_head_fields(memory, frame)
    if target == 0xe26c:
        return roster_contains_force_head_carry_fields(memory, frame)
    if target == 0x21514:
        return append_group_from_survivor_roster_fields(memory, frame)
    if target == 0x21efe:
        return choose_empty_neighbor_position_fields(memory, frame)
    if target == 0x1CB96:
        return consolidate_city_after_battle_fields(memory, frame)
    if target == 0x26BFA:
        from .contexts_services import SceneRefreshMemory
        from .business_services import stage_sprite_word_packet_fields
        return stage_sprite_word_packet_fields(SceneRefreshMemory(memory.state), frame)
    if target == 0x30A74:
        from .contexts_services import SceneRefreshMemory
        from .business_services import present_gameplay_message_fields
        return present_gameplay_message_fields(SceneRefreshMemory(memory.state), frame)
    if target == 0x1C466:
        return consume_city_battle_resources_fields(memory, frame)
    if target == 0x1C1C2:
        return compute_outcome_force_ratio_fields(memory, frame)
    if target == 0x1C2A0:
        return build_city_assigned_outcome_candidates_fields(memory, frame)[0]
    if target == 0x1C2C8:
        return build_battlefield_outcome_candidates_fields(memory, frame)[0]
    if target == 0x35760:
        from ..high_level_main_flows.business_movement_support import signed_divmod_fields
        return signed_divmod_fields(memory.state, frame)
    if target == 0x1C57C:
        return distribute_city_battle_progress_fields(memory, frame)
    if target == 0x1C554:
        return sample_city_postbattle_reserve_fields(memory, frame)
    if target == 0x1C69E:
        return apply_assigned_city_light_attrition_fields(memory, frame)
    if target == 0x1C732:
        return consume_city_battle_supply_long_fields(memory, frame)
    if target == 0x1C78C:
        return reduce_city_reserve_after_defeat_fields(memory, frame)
    if target == 0x1C7C4:
        return consume_city_battle_supply_word_fields(memory, frame)
    if target == 0x1CC94:
        return reassign_city_flagged_officers_fields(memory, frame)
    if target == 0x217C8:
        return apply_postbattle_city_economic_attrition_fields(memory, frame)
    if target == 0x1CC76:
        return clear_city_officer_links_fields(memory, frame)
    if target == 0x1d03c:
        return settle_battle_packed_armies_fields(memory, frame)
    if target == 0x1d0a2:
        return remove_defeated_packed_member_fields(memory, frame)
    if target == 0x1d142:
        return replace_or_remove_group_references_fields(memory, frame)
    if target == 0x1d198:
        return transfer_outcome_officer_fields(memory, frame)
    if target == 0x1d20a:
        return detach_member_keep_group_cursor_fields(memory, frame)
    if target == 0x1d29e:
        return replace_group_head_reference_fields(memory, frame)
    if target == 0x1d2e8:
        return remove_group_reference_fields(memory, frame)
    if target == 0x1d318:
        return attach_member_shift_packet_fields(memory, frame)
    if target == 0x1D3BC:
        from ..high_level_remaining_flows.business_city import settle_group_at_city_fields
        return settle_group_at_city_fields(memory.state, frame)
    if target == 0x1D4DA:
        from ..high_level_remaining_flows.business_city import adjust_battle_losing_loyalty_fields
        return adjust_battle_losing_loyalty_fields(memory.state, frame)
    raise MovementContinuationBoundary(target, frame,
        'city outcome child needs its actual field/nonlocal-return ABI')


def _city_outcome_call_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame, target: int, continuation: int) -> FirstDeploymentFrame:
    """Reuse the one physical call/RTS helper; unknown child sees the true slot."""
    frame = _city_outcome_frame_fields(memory, frame, target)
    def child(actual_memory, entered):
        return _city_outcome_child_fields(actual_memory, entered, target)
    return _presentation_call_fields(memory, frame, continuation, child)


def _city_outcome_word_product_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame, product: str, scratch: str, factor: int) -> FirstDeploymentFrame:
    """Observe the sole existing low/high-WORD product through named roles.

    This adapter changes no bus state or unrelated carrier. It delegates the
    original low MULU / SWAP / high MULU / SWAP / ADD and final CCR to the
    existing recruitment product, rather than introducing a second math core.
    """
    from ..high_level_remaining_flows.business_city import _recruitment_stitched_score_product
    if (product, scratch) not in (('target_y','distance'), ('unit','offset_x'), ('unit','count'), ('target_x','target_y')):
        raise ValueError('original city outcome product roles required')
    projected = first_replace(frame, unit=frame.carrier(product), target_x=frame.carrier(scratch))
    projected = _recruitment_stitched_score_product(memory.state, projected, uint(factor, 16))
    return first_replace(frame, **{product:projected.unit, scratch:projected.target_x}, status=projected.status)


def _city_outcome_strength_totals_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame, defender: bool) -> FirstDeploymentFrame:
    """The two live D300 scans expose their different original carrier roles."""
    if type(defender) is not bool:
        raise ValueError('original city/battlefield strength role required')
    if not defender:
        frame = _first_long(frame, 'target_y', 0)
        frame = _first_word(frame, 'unit', 0)
        frame = _first_word(frame, 'count', 0)
        frame = first_replace(frame, roster=memory.table(0xFFFFC800).cursor(),
            candidates=memory.table(0xFFFFB400).cursor(), controller=memory.table(0xFFFFB600),
            scan=memory.table(0xFFFFD300).cursor())
        index_name, troop_name, first_name, second_name = 'distance','target_y','unit','count'
        source, troops, first, second = frame.scan,frame.roster,frame.candidates,frame.controller
    else:
        frame = first_replace(frame, roster=memory.table(0xFFFFD300).cursor(),
            candidates=memory.table(0xFFFFC800).cursor(), controller=memory.table(0xFFFFB400),
            scan=memory.table(0xFFFFB600).cursor())
        frame = _first_long(frame, 'unit', 0)
        frame = _first_word(frame, 'count', 0)
        frame = _first_word(frame, 'distance', 0)
        index_name, troop_name, first_name, second_name = 'offset_x','unit','count','distance'
        source, troops, first, second = frame.roster,frame.candidates,frame.controller,frame.scan
    while True:
        member = source.word()
        source = source.advance(2)
        frame = first_replace(frame, **{'roster' if defender else 'scan':source})
        frame = _first_word(frame, index_name, member)
        if negative_word(member):
            return frame
        frame = _first_shift_word(frame, index_name, member, 1)
        offset = u16(member << 1)
        frame = _first_add_word(frame, first_name, low16(frame.carrier(first_name)), first.word(offset))
        frame = _first_add_word(frame, second_name, low16(frame.carrier(second_name)), second.word(offset))
        frame = _first_shift_word(frame, index_name, offset, 1)
        frame = _damage_add_long(memory, frame, troop_name, troops.long(u16(offset << 1)))


def _city_outcome_scale_troops_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame, carrier: str) -> FirstDeploymentFrame:
    """Original LSR.L#5 only; unlike WORD shifts it discards the high bits."""
    if carrier not in ('target_y','unit'):
        raise ValueError('actual city outcome troop carrier required')
    original = uint(frame.carrier(carrier), 32)
    value = original >> 5
    status = (17 if original & 16 else 0) | (4 if value == 0 else 0)
    return memory.finish(first_replace(frame, **{carrier:value}, status=status))


def compute_outcome_force_ratio_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1C1C2..1C2A0: asymmetric totals/products, sole signed division and store.

    First troops get ADDQ.W before LSR.L5; second troops after it. The second
    denominator product intentionally repeats D3 despite a real D4 read/scale.
    """
    frame = _city_outcome_frame_fields(memory, frame, 0x1C1C2)
    frame = _postbattle_fraction_fields(memory, frame, 6, 10, 0x1C1C8)
    frame = _city_outcome_call_fields(memory, frame, 0x1C2A0, 0x1C1E0)
    frame = _city_outcome_strength_totals_fields(memory, frame, False)
    frame = _first_add_word(frame, 'target_y', low16(frame.target_y), 1)
    frame = _city_outcome_scale_troops_fields(memory, frame, 'target_y')
    frame = _first_right_word(frame, 'unit', low16(frame.unit), 3)
    frame = _first_right_word(frame, 'count', low16(frame.count), 3)
    frame = _first_add_word(frame, 'unit', low16(frame.unit), 1)
    frame = _first_add_word(frame, 'count', low16(frame.count), 1)
    frame = _city_outcome_word_product_fields(memory, frame, 'target_y', 'distance', low16(frame.unit))
    frame = _city_outcome_word_product_fields(memory, frame, 'target_y', 'distance', low16(frame.count))
    frame = _city_outcome_word_product_fields(memory, frame, 'target_y', 'distance', low16(frame.target_x))
    frame = _city_outcome_call_fields(memory, frame, 0x1C2C8, 0x1C242)
    frame = _city_outcome_strength_totals_fields(memory, frame, True)
    frame = _city_outcome_scale_troops_fields(memory, frame, 'unit')
    frame = _first_right_word(frame, 'count', low16(frame.count), 3)
    frame = _first_right_word(frame, 'distance', low16(frame.distance), 3)
    frame = _first_add_word(frame, 'unit', low16(frame.unit), 1)
    frame = _first_add_word(frame, 'count', low16(frame.count), 1)
    frame = _first_add_word(frame, 'distance', low16(frame.distance), 1)
    frame = _city_outcome_word_product_fields(memory, frame, 'unit', 'offset_x', low16(frame.count))
    frame = _city_outcome_word_product_fields(memory, frame, 'unit', 'offset_x', low16(frame.count))
    frame = _city_outcome_call_fields(memory, frame, 0x35760, 0x1C29A)
    memory.table(0xFFFFEFBC).set_word(0, low16(frame.target_y))
    return memory.finish(_first_memory_word(frame, low16(frame.target_y)))


def _city_outcome_assigned_troops_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Descending256 exact BYTE matches; each selected LONG adds100 separately."""
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_x', city)
    frame = _first_word(frame, 'target_y', 255)
    frame = _first_long(frame, 'unit', 0)
    for officer in descending_inclusive(255):
        assigned = frame.candidates.byte(officer)
        frame = _postbattle_compare_byte_fields(frame, low8(city), assigned)
        if assigned == low8(city):
            frame = _first_word(frame, 'count', officer)
            frame = _first_shift_word(frame, 'count', officer, 2)
            frame = _damage_add_long(memory, frame, 'unit', frame.roster.long(u16(officer << 2)))
            frame = _damage_add_long(memory, frame, 'unit', 100)
        frame = _postbattle_decrement_fields(frame, 'target_y', officer)
    return frame


def consume_city_battle_resources_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1C466..1C554: two independent live scans/draws with asymmetric DIVU order.

    First ANDI.L occurs after resource LONG loading; second before its LEA.
    Real divide exceptions/undefined overflow flags keep their true boundary.
    """
    frame = _city_outcome_frame_fields(memory, frame, 0x1C466)
    frame = first_replace(frame, roster=memory.table(0xFFFFC800).cursor(),
        candidates=memory.table(0xFFFFA050).cursor())
    frame = _city_outcome_assigned_troops_fields(memory, frame)
    frame = _postbattle_fraction_fields(memory, frame, 11, 10, 0x1C498)
    frame = _city_outcome_word_product_fields(memory, frame, 'unit', 'count', low16(frame.target_x))
    frame = _damage_divide(frame, 'unit', 500, 0x1C4BA)
    frame = first_replace(frame, controller=memory.table(0xFFFFEE24))
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_x', city)
    frame = _first_shift_word(frame, 'target_x', city, 2)
    resource = frame.controller.long(u16(city << 2))
    frame = _first_long(frame, 'target_y', resource)
    frame = _first_long(frame, 'unit', frame.unit & 65535)
    frame = _presentation_sub_long_fields(frame, 'target_y', resource, frame.unit)
    if frame.status & 1:
        frame = _first_long(frame, 'target_y', 0)
    frame.controller.set_long(u16(city << 2), frame.target_y)
    frame = _first_long(frame, 'target_y', frame.target_y)
    frame = first_replace(frame, candidates=memory.table(0xFFFFCC00).cursor())
    frame = _city_outcome_assigned_troops_fields(memory, frame)
    frame = _postbattle_fraction_fields(memory, frame, 11, 10, 0x1C50C)
    frame = _city_outcome_word_product_fields(memory, frame, 'unit', 'count', low16(frame.target_x))
    frame = _damage_divide(frame, 'unit', 500, 0x1C52E)
    frame = _first_long(frame, 'unit', frame.unit & 65535)
    frame = first_replace(frame, controller=memory.table(0xFFFFE09C))
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_x', city)
    frame = _first_shift_word(frame, 'target_x', city, 2)
    resource = frame.controller.long(u16(city << 2))
    frame = _first_long(frame, 'count', resource)
    frame = _presentation_sub_long_fields(frame, 'count', resource, frame.unit)
    if frame.status & 1:
        frame = _first_long(frame, 'count', 0)
    frame.controller.set_long(u16(city << 2), frame.count)
    return memory.finish(_first_long(frame, 'count', frame.count))


def _city_outcome_store_word_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame, address: int, value: int, clear: bool=False) -> FirstDeploymentFrame:
    """Store known original WORD with memory CLR's actual prior read."""
    view = memory.table(address)
    if clear:
        view.word()
    view.set_word(0, uint(value, 16))
    return memory.finish(_first_memory_word(frame, value))


def _city_outcome_head_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Two live ruler indices, real WORD shifts and ordered name-argument writes."""
    frame = first_replace(frame, roster=memory.table(0xFFFFE640).cursor())
    owner = memory.table(0xFFFFF68C).word()
    frame = _first_word(frame, 'target_x', owner)
    frame = _first_shift_word(frame, 'target_x', owner, 1)
    frame = _city_outcome_store_word_fields(memory, frame, 0xFFFFF3D0, frame.roster.word(u16(owner << 1)))
    owner = memory.table(0xFFFFF68E).word()
    frame = _first_word(frame, 'target_x', owner)
    frame = _first_shift_word(frame, 'target_x', owner, 1)
    return _city_outcome_store_word_fields(memory, frame, 0xFFFFF3D2, frame.roster.word(u16(owner << 1)))


def _city_outcome_notify_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame, initial: bool, conquered: bool=False) -> FirstDeploymentFrame:
    """Only the three original messages; save/read/pop the real F362 WORD."""
    if type(initial) is not bool or type(conquered) is not bool:
        raise ValueError('original outcome notification arm required')
    frame = _city_outcome_head_fields(memory, frame)
    if not initial:
        frame = _city_outcome_store_word_fields(memory, frame, 0xFFFFF646, memory.table(0xFFFFF68A).word())
    saved = memory.table(0xFFFFF362).word()
    stack = frame.stack_cursor.advance(-2)
    stack.set_word(0, saved)
    frame = first_replace(frame, stack_cursor=stack)
    frame = _first_memory_word(frame, saved)
    message = 159 if initial else 161 if conquered else 162
    frame = _city_outcome_store_word_fields(memory, frame, 0xFFFFF740, message)
    if initial:
        frame = _city_outcome_store_word_fields(memory, frame, 0xFFFFF362, 0, True)
    frame = _city_outcome_store_word_fields(memory, frame, 0xFFFFF608, 300)
    frame = _city_outcome_store_word_fields(memory, frame, 0xFFFFF362, 0, True)
    continuation = 0x1C06C if initial else 0x1C0E4 if conquered else 0x1C14A
    frame = _city_outcome_call_fields(memory, frame, 0x30A74, continuation)
    saved = frame.stack_cursor.word()
    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
    return _city_outcome_store_word_fields(memory, frame, 0xFFFFF362, saved)


def settle_city_battle_outcome_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1BFEC..1C1A6: complete city outcome orchestration with actual child ABIs.

    Complete means the parent body is restored, not all descendants known.
    Unowned children stop after their physical return LONG has been written.
    """
    frame = _city_outcome_frame_fields(memory, frame, 0x1BFEC)
    frame = _city_outcome_store_word_fields(memory, frame, 0xFFFFF352, 32)
    frame = first_replace(frame, roster=memory.table(0xFFFFF427).cursor())
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_x', city)
    frame = _city_outcome_store_word_fields(memory, frame, 0xFFFFF68E, 0, True)
    value = frame.roster.byte(city)
    memory.table(0xFFFFF68F).set_byte(0, value)
    frame = _postbattle_memory_byte_fields(frame, value)
    frame = first_replace(frame, roster=memory.table(0xFFFFA050).cursor())
    frame = _first_word(frame, 'target_y', 255)
    while True:
        assigned = frame.roster.byte(low16(frame.target_y))
        frame = _postbattle_compare_byte_fields(frame, low8(frame.target_x), assigned)
        if frame.status & 4:
            break
        remaining = u16(low16(frame.target_y) - 1)
        frame = first_replace(frame, target_y=replace_word(frame.target_y, remaining))
        if remaining == 65535:
            break
    frame = first_replace(frame, roster=memory.table(0xFFFFCC00).cursor())
    frame = _first_word(frame, 'target_x', 0)
    value = frame.roster.byte(low16(frame.target_y))
    from ..high_level_battle_ai.business_formation import _first_byte
    frame = _first_byte(frame, 'target_x', value)
    frame = _first_word(frame, 'target_x', low16(frame.target_x) & 63)
    frame = first_replace(frame, roster=memory.table(0xFFFFF427).cursor())
    frame = _city_outcome_store_word_fields(memory, frame, 0xFFFFF68C, 0, True)
    value = frame.roster.byte(low16(frame.target_x))
    memory.table(0xFFFFF68D).set_byte(0, value)
    frame = _postbattle_memory_byte_fields(frame, value)
    frame = _city_outcome_notify_fields(memory, frame, True)
    frame = _city_outcome_call_fields(memory, frame, 0x1C466, 0x1C074)
    frame = _city_outcome_call_fields(memory, frame, 0x1C1C2, 0x1C078)
    frame = _first_compare_word(frame, low16(frame.target_y), 10)
    conquered = bool(frame.status & 1)
    if conquered:
        for target, continuation in ((0x1C2FC,0x1C084),(0x1C39C,0x1C088),
                (0x1C57C,0x1C08C),(0x1C5E2,0x1C090),(0x1C554,0x1C094),
                (0x1C732,0x1C098),(0x1C82C,0x1C09C),(0x1CB96,0x1C0A0),
                (0x1CC94,0x1C0A4)):
            frame = _city_outcome_call_fields(memory, frame, target, continuation)
        frame = _city_outcome_store_word_fields(memory, frame, 0xFFFFF6D6, 0, True)
    else:
        for target, continuation in ((0x1C5EE,0x1C0F0),(0x1C69E,0x1C0F4),
                (0x1C57C,0x1C0F8),(0x1C5E2,0x1C0FC),(0x1C78C,0x1C100),
                (0x1C7C4,0x1C104),(0x1CB08,0x1C108)):
            frame = _city_outcome_call_fields(memory, frame, target, continuation)
        frame = _city_outcome_store_word_fields(memory, frame, 0xFFFFF6D6, 2)
    frame = _city_outcome_notify_fields(memory, frame, False, conquered)
    frame = _city_outcome_call_fields(memory, frame, 0x217C8, 0x1C152)
    frame = _city_outcome_call_fields(memory, frame, 0x1CC76, 0x1C156)
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_x', city)
    frame = first_replace(frame, roster=memory.table(0xFFFFEA37).cursor())
    frame.roster.byte(city)
    frame.roster.set_byte(city, 0)
    frame = _postbattle_memory_byte_fields(frame, 0)
    frame = _city_outcome_store_word_fields(memory, frame, 0xFFFFF612, 513)
    frame = _first_long(frame, 'target_x', 0xC0000026)
    frame = _first_word(frame, 'target_y', 7)
    frame = _first_word(frame, 'unit', 0xCA02)
    frame = first_replace(frame, roster=memory.table(0x1C1A6).cursor())
    frame = _city_outcome_call_fields(memory, frame, 0x26BFA, 0x1C182)
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_x', city)
    frame = _first_shift_word(frame, 'target_x', city, 2)
    offset = u16(city << 2)
    for address in (0xFFFFEE24,0xFFFFED84):
        frame = first_replace(frame, roster=memory.table(address).cursor())
        frame.roster.long(offset)
        frame.roster.set_long(offset, 0)
        # CLR.L changes flags, not D0; the effective city offset is preserved.
        frame = first_replace(frame, status=frame.status & 16 | 4)
    for source, destination in ((0xFFFFF68D,0xFFFFA622),(0xFFFFF68F,0xFFFFA623)):
        value = memory.table(source).byte()
        memory.table(destination).set_byte(0, value)
        frame = _postbattle_memory_byte_fields(frame, value)
    return memory.finish(frame)


# Sole current city outcome loss and returning-roster field cores.
def _postbattle_loss_roster_fields(memory, frame, profile):
    """One live roster loss loop; profiles preserve the three original layouts.

    Troop writes are WORDs at +2, not replacement LONGs. Each officer uses
    independent RNG children for troops and readiness. The Scene path keeps
    all physical fields; missing historical fields stop before any mutation.
    """
    if profile not in ('ratio', 'assigned-heavy', 'battlefield-heavy'):
        raise ValueError('original postbattle loss profile required')
    assigned = profile == 'assigned-heavy'
    entry = 0x1C39C if assigned else 0x1C2FC if profile == 'ratio' else 0x1C5EE
    frame = _city_outcome_frame_fields(memory, frame, entry)
    frame, _ = _postbattle_candidates_fields(memory, frame, not assigned, entry + (4 if entry != 0x1C2FC else 2))
    roster = memory.table(0xFFFFD300).cursor()
    troops = memory.table(0xFFFFC800).cursor()
    readiness = memory.table(0xFFFFB200).cursor()
    ability = memory.table(0xFFFFC000).cursor()
    flags = memory.table(0xFFFFC700).cursor()
    assignments = memory.table(0xFFFFCC00).cursor()
    if profile == 'ratio':
        frame = first_replace(frame, roster=roster, candidates=troops, controller=readiness,
            scan=assignments, opponent=ability, scratch=flags)
    elif assigned:
        frame = first_replace(frame, roster=roster, candidates=troops, controller=readiness,
            scan=ability, opponent=assignments, scratch=memory.table(0xFFFFF45E).cursor(), auxiliary=flags)
    else:
        frame = first_replace(frame, roster=roster, candidates=troops, controller=readiness,
            scan=ability, opponent=flags, scratch=assignments)
    frame = _first_word(frame, 'choice', 0)
    points = 0
    from ..high_level_battle_ai.business_formation import _first_sub_word
    while True:
        officer = roster.word()
        roster = roster.advance(2)
        frame = first_replace(frame, roster=roster)
        frame = _first_word(frame, 'unit', officer)
        if negative_word(officer):
            destination = 0xFFFFEFBA if assigned else 0xFFFFEFB8
            memory.table(destination).set_word(0, points)
            return memory.finish(_first_memory_word(frame, points))
        frame = _first_shift_word(frame, 'unit', officer, 2)
        troop_index = u16(officer << 2)
        original = troops.long(troop_index)
        frame = _first_long(frame, 'count', original)
        troop_token = 0x1C32A if profile == 'ratio' else 0x1C3D0 if assigned else 0x1C61E
        frame = _postbattle_fraction_fields(memory, frame, 40, 30 if profile == 'ratio' else 50, troop_token)
        if profile == 'ratio':
            frame = _first_long(frame, 'target_x', low16(frame.target_x) * memory.table(0xFFFFEFBC).word())
            frame = _city_outcome_word_product_fields(memory, frame, 'target_x', 'target_y', low16(original))
            frame = _damage_divide(frame, 'target_x', 1000, 0x1C34E)
        else:
            frame = _postbattle_loss_fields(frame, original, 100, 0x1C3E6 if assigned else 0x1C634)
        frame = _first_sub_word(frame, 'count', low16(original), low16(frame.target_x))
        troops.set_word(troop_index, low16(frame.count), 2)
        frame = _first_memory_word(frame, low16(frame.count))
        frame = _first_long(frame, 'target_x', frame.target_x & 65535)
        frame = _damage_divide(frame, 'target_x', 400, 0x1C35E if profile == 'ratio' else 0x1C3F6 if assigned else 0x1C644)
        frame = _first_add_word(frame, 'choice', points, low16(frame.target_x))
        points = u16(points + low16(frame.target_x))
        frame = _first_right_word(frame, 'unit', troop_index, 1)
        readiness_index = troop_index >> 1
        original = readiness.word(readiness_index)
        frame = _first_word(frame, 'count', original)
        readiness_token = 0x1C370 if profile == 'ratio' else 0x1C408 if assigned else 0x1C656
        scale = 30 if profile == 'ratio' else 60 if assigned else 61
        frame = _postbattle_fraction_fields(memory, frame, scale, 0, readiness_token)
        frame = _postbattle_loss_fields(frame, original, 100, 0x1C382 if profile == 'ratio' else 0x1C41A if assigned else 0x1C65E)
        frame = _first_sub_word(frame, 'count', original, low16(frame.target_x))
        remaining = low16(frame.count)
        if profile == 'ratio' and remaining == 0:
            remaining = 1
            frame = _first_word(frame, 'count', remaining)
        readiness.set_word(readiness_index, remaining)
        frame = _first_memory_word(frame, remaining)
        if profile == 'ratio':
            continue
        frame = _first_compare_word(frame, remaining, 10)
        if remaining > 10:
            continue
        original = ability.word(readiness_index)
        frame = _first_word(frame, 'count', original)
        frame = _first_long(frame, 'count', original)
        frame = _damage_divide(frame, 'count', 5, 0x1C434 if assigned else 0x1C678)
        frame = _first_right_word(frame, 'unit', readiness_index, 1)
        officer = readiness_index >> 1
        if assigned:
            city = memory.table(0xFFFFF68A).word()
            frame = _first_word(frame, 'distance', city)
            frame = _first_shift_word(frame, 'distance', city, 1)
            head = frame.scratch.word(u16(city << 1))
            frame = _first_compare_word(frame, officer, head)
            if officer == head:
                frame = _first_add_word(frame, 'count', low16(frame.count), 30)
        else:
            assignments.set_byte(officer, 255)
            frame = _postbattle_memory_byte_fields(frame, 255)
        marked = flags.byte(officer)
        frame = _postbattle_bit_fields(frame, bool(marked & 16))
        if marked & 16:
            frame = _first_add_word(frame, 'count', low16(frame.count), 20)
        frame = _first_add_word(frame, 'choice', points, low16(frame.count))
        points = u16(points + low16(frame.count))


def apply_battlefield_ratio_losses_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1C2FC..1C39C: ratio-weighted losses and the exact zero-readiness floor."""
    return _postbattle_loss_roster_fields(memory, frame, 'ratio')


def apply_city_assigned_heavy_losses_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1C39C..1C466: assigned losses, current head bonus, status-bit bonus."""
    return _postbattle_loss_roster_fields(memory, frame, 'assigned-heavy')


def apply_battlefield_heavy_losses_and_detach_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1C5EE..1C69E: 61-scaled readiness draw; low readiness loses assignment."""
    return _postbattle_loss_roster_fields(memory, frame, 'battlefield-heavy')


def _postbattle_bit_fields(frame, present):
    """Original BTST/BSET changes only Z in the actual low CCR."""
    if type(present) is not bool:
        raise ValueError('observed original bit required')
    return first_replace(frame, status=None if frame.status is None else (frame.status & 27) | (0 if present else 4))


def _postbattle_byte_carrier_fields(frame, name, value):
    from ..high_level_battle_ai.business_formation import _first_byte
    return _first_byte(frame, name, value)


def sort_returning_officer_status_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1C8BC..1C942: live descending status insertion and overflow partition.

    D0 is the actual surplus, including its retained high WORD. Sentinel
    displacement performs the original extra status read/write before the
    negative incoming token is stored at the next position.
    """
    frame = _city_outcome_frame_fields(memory, frame, 0x1C8BC)
    from ..high_level_main_flows.business_movement_support import _movement_binary_flags
    previous = memory.table(0xFFFFEFB8).word()
    surplus = low16(frame.target_x)
    frame, added = _movement_binary_flags(memory.state, frame, previous, surplus, 16)
    memory.table(0xFFFFEFB8).set_word(0, added)
    source = memory.table(0xFFFFAF28).cursor()
    loyalty = memory.table(0xFFFFC300).cursor()
    sorted_members = memory.table(0xFFFFD300).cursor()
    sorted_status = memory.table(0xFFFFD320).cursor()
    frame = first_replace(frame, roster=source, scan=loyalty,
        candidates=sorted_members, controller=sorted_status)
    memory.table(0xFFFFD300).set_word(0, 65535)
    frame = _first_memory_word(frame, 65535)
    frame = _first_word(frame, 'unit', 0)
    while True:
        frame = _first_word(frame, 'count', 0)
        member = source.word()
        source = source.advance(2)
        frame = first_replace(frame, roster=source)
        frame = _first_word(frame, 'target_y', member)
        if negative_word(member):
            break
        frame = _postbattle_byte_carrier_fields(frame, 'unit', loyalty.byte(member))
        index = 0
        while True:
            occupied = sorted_members.word(index)
            frame = _first_memory_word(frame, occupied)
            if negative_word(occupied):
                break
            status = sorted_status.byte(index, 1)
            frame = _postbattle_compare_byte_fields(frame, low8(frame.unit), status)
            if low8(frame.unit) > status:
                break
            frame = _first_add_word(frame, 'count', index, 2)
            index = u16(index + 2)
        while True:
            displaced = sorted_members.word(index)
            frame = _first_word(frame, 'distance', displaced)
            incoming = low16(frame.target_y)
            sorted_members.set_word(index, incoming)
            frame = _first_memory_word(frame, incoming)
            if negative_word(incoming):
                break
            old_status = sorted_status.word(index)
            frame = _first_word(frame, 'offset_x', old_status)
            sorted_status.set_word(index, low16(frame.unit))
            frame = _first_memory_word(frame, low16(frame.unit))
            frame = _first_add_word(frame, 'count', index, 2)
            index = u16(index + 2)
            frame = _first_word(frame, 'target_y', low16(frame.distance))
            frame = _first_word(frame, 'unit', low16(frame.offset_x))
    returning = memory.table(0xFFFFAF56).cursor()
    frame = first_replace(frame, roster=returning)
    while True:
        value = returning.word()
        returning = returning.advance(2)
        frame = first_replace(frame, roster=returning)
        frame = _first_memory_word(frame, value)
        if negative_word(value):
            break
    returning = returning.advance(-2)
    frame = first_replace(frame, roster=returning)
    from ..high_level_battle_ai.business_formation import _first_sub_word
    frame = _first_sub_word(frame, 'target_x', surplus, 1)
    source = memory.table(0xFFFFD300).cursor()
    frame = first_replace(frame, candidates=source)
    for counter in descending_inclusive(u16(surplus - 1)):
        value = source.word()
        source, returning = source.advance(2), returning.advance(2)
        returning.advance(-2).set_word(0, value)
        frame = first_replace(frame, candidates=source, roster=returning)
        frame = _first_memory_word(frame, value)
        frame = _postbattle_decrement_fields(frame, 'target_x', counter)
    returning.set_word(0, 65535)
    frame = _first_memory_word(frame, 65535)
    remaining = memory.table(0xFFFFAF28).cursor()
    frame = first_replace(frame, roster=remaining)
    frame = _first_word(frame, 'target_y', 0)
    count = 0
    while True:
        value = source.word()
        remaining.set_word(0, value)
        source, remaining = source.advance(2), remaining.advance(2)
        frame = first_replace(frame, candidates=source, roster=remaining)
        frame = _first_memory_word(frame, value)
        if negative_word(value):
            memory.table(0xFFFFEFBA).set_word(0, count)
            return memory.finish(_first_memory_word(frame, count))
        frame = _first_add_word(frame, 'target_y', count, 1)
        count = u16(count + 1)


def owner_has_other_city_carry_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1C9FE..1CA3C: physical four-LONG save, descending owners, actual C."""
    frame = _city_outcome_frame_fields(memory, frame, 0x1C9FE)
    saved = ('target_x', 'target_y', 'unit', 'roster')
    frame, observed = _damage_save_longs(memory, frame, saved)
    owners = memory.table(0xFFFFF428).cursor()
    frame = first_replace(frame, roster=owners)
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_x', city)
    from ..high_level_battle_ai.business_formation import _first_sub_word
    frame = _first_sub_word(frame, 'target_x', city, 1)
    excluded = u16(city - 1)
    frame = _first_word(frame, 'target_y', 39)
    owner = memory.table(0xFFFFEFE2).byte()
    frame = _postbattle_byte_carrier_fields(frame, 'unit', owner)
    carry = True
    for candidate in descending_inclusive(39):
        assigned = owners.byte(candidate)
        frame = _postbattle_compare_byte_fields(frame, owner, assigned)
        if owner == assigned:
            frame = _first_compare_word(frame, candidate, excluded)
            if candidate != excluded:
                carry = False
                break
        frame = _postbattle_decrement_fields(frame, 'target_y', candidate)
    frame = _damage_restore_longs(memory, frame, saved, observed)
    return memory.finish(first_replace(frame, status=(frame.status & 30) | int(carry)))


def partition_city_survivors_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1C942..1C9FE: ordered troop gates, independent RNG and ruler handling."""
    frame = _city_outcome_frame_fields(memory, frame, 0x1C942)
    assignments = memory.table(0xFFFFCC00).cursor()
    owners = memory.table(0xFFFFF427).cursor()
    heads = memory.table(0xFFFFE640).cursor()
    frame = first_replace(frame, roster=assignments, candidates=owners, controller=heads)
    first = memory.table(0xFFFFD300).word()
    frame = _first_word(frame, 'target_x', first)
    frame = _first_word(frame, 'target_y', 0)
    city = assignments.byte(first)
    frame = _postbattle_byte_carrier_fields(frame, 'target_y', city)
    city &= 63
    frame = _first_word(frame, 'target_y', city)
    frame = _first_word(frame, 'target_x', 0)
    owner = owners.byte(city)
    frame = _postbattle_byte_carrier_fields(frame, 'target_x', owner)
    memory.table(0xFFFFEFE2).set_byte(0, owner)
    frame = _postbattle_memory_byte_fields(frame, owner)
    frame = _first_shift_word(frame, 'target_x', owner, 1)
    ruler = heads.word(u16(owner << 1))
    frame = _first_word(frame, 'choice', ruler)
    roster = memory.table(0xFFFFD300).cursor()
    troops = memory.table(0xFFFFC800).cursor()
    readiness = memory.table(0xFFFFB200).cursor()
    remaining, returning = memory.table(0xFFFFAF28).cursor(), memory.table(0xFFFFAF56).cursor()
    frame = first_replace(frame, roster=roster, candidates=troops, controller=readiness,
        scan=remaining, opponent=returning, scratch=assignments)
    frame = _first_word(frame, 'unit', 0)
    frame = _first_word(frame, 'count', 0)
    return_count, keep_count = 0, 0
    from ..high_level_battle_ai.business_formation import _first_compare_long
    while True:
        officer = roster.word()
        roster = roster.advance(2)
        frame = first_replace(frame, roster=roster)
        frame = _first_word(frame, 'offset_y', officer)
        if negative_word(officer):
            remaining.set_word(0, 65535)
            frame = _first_memory_word(frame, 65535)
            returning.set_word(0, 65535)
            frame = _first_memory_word(frame, 65535)
            memory.table(0xFFFFEFB8).set_word(0, return_count)
            frame = _first_memory_word(frame, return_count)
            memory.table(0xFFFFEFBA).set_word(0, keep_count)
            return memory.finish(_first_memory_word(frame, keep_count))
        frame = _first_compare_word(frame, officer, ruler)
        goes_back = False
        if officer == ruler:
            frame = _city_outcome_call_fields(memory, frame, 0x1C9FE, 0x1C9D4)
            if frame.status & 1:
                assignments.set_byte(officer, 255)
                frame = _postbattle_memory_byte_fields(frame, 255)
                continue
            goes_back = True
        else:
            frame = _first_word(frame, 'distance', officer)
            frame = _first_shift_word(frame, 'distance', officer, 2)
            offset = u16(officer << 2)
            original = troops.long(offset)
            frame = _first_compare_long(frame, original, 500)
            weak = original <= 500
            if not weak:
                original = troops.long(offset)
                frame = _first_compare_long(frame, original, 1000)
                weak = original <= 1000
                if weak:
                    frame = _first_right_word(frame, 'distance', offset, 1)
                    resource = readiness.word(offset >> 1)
                    frame = _first_compare_word(frame, resource, 30)
                    weak = resource <= 30
            if weak:
                frame = _presentation_call_fields(memory, frame, 0x1C9C2, _presentation_random_fields)
                sample = low16(frame.target_x) & 3
                frame = _first_word(frame, 'target_x', sample)
                goes_back = sample == 0
        if goes_back:
            returning.set_word(0, officer)
            returning = returning.advance(2)
            frame = first_replace(frame, opponent=returning)
            frame = _first_memory_word(frame, officer)
            frame = _first_add_word(frame, 'unit', return_count, 1)
            return_count = u16(return_count + 1)
        else:
            remaining.set_word(0, officer)
            remaining = remaining.advance(2)
            frame = first_replace(frame, scan=remaining)
            frame = _first_memory_word(frame, officer)
            frame = _first_add_word(frame, 'count', keep_count, 1)
            keep_count = u16(keep_count + 1)


def restore_returning_officer_assignments_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1CA3C..1CA60: each reassignment precedes the same unique loyalty child."""
    frame = _city_outcome_frame_fields(memory, frame, 0x1CA3C)
    roster = memory.table(0xFFFFAF28).cursor()
    assignments = memory.table(0xFFFFCC00).cursor()
    frame = first_replace(frame, roster=roster, candidates=assignments)
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_y', city)
    while True:
        officer = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _first_word(frame, 'target_x', officer)
        if negative_word(officer):
            return memory.finish(frame)
        frame.candidates.set_byte(officer, low8(frame.target_y))
        frame = _postbattle_memory_byte_fields(frame, low8(frame.target_y))
        memory.table(0xFFFFF3A6).set_word(0, low16(frame.target_x))
        frame = _first_memory_word(frame, low16(frame.target_x))
        frame = _city_outcome_call_fields(memory, frame, 0x208CE, 0x1CA5C)


def allocate_packed_group_resources_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1CA60..1CB08: packet count BYTE and exact asymmetric resource packing.

    The original gold high-BYTE step is LSL.W8, while rice uses LSR.W8.
    This apparent packing defect is preserved, not normalized away.
    """
    frame = _city_outcome_frame_fields(memory, frame, 0x1CA60)
    from ..high_level_main_flows.business_movement_support import _movement_shift_long
    from ..high_level_battle_ai.business_formation import _first_sub_word, _first_compare_long
    troops = memory.table(0xFFFFC800).cursor()
    frame = first_replace(frame, candidates=troops)
    count = frame.roster.byte()
    frame = _postbattle_byte_carrier_fields(frame, 'target_x', count)
    frame = _first_word(frame, 'target_x', count)
    frame = _first_sub_word(frame, 'target_x', count, 1)
    frame = _first_long(frame, 'target_y', 0)
    frame = _first_word(frame, 'unit', 0)
    for counter in descending_inclusive(u16(count - 1)):
        officer = frame.roster.byte(counter, 13)
        frame = _postbattle_byte_carrier_fields(frame, 'unit', officer)
        frame = _first_shift_word(frame, 'unit', low16(frame.unit), 2)
        frame = _damage_add_long(memory, frame, 'target_y', troops.long(low16(frame.unit)))
        frame = _damage_add_long(memory, frame, 'target_y', 100)
        frame = _postbattle_decrement_fields(frame, 'target_x', counter)
    frame = _first_long(frame, 'unit', frame.target_y)
    frame = _postbattle_shift_long_fields(memory, frame, 'unit', 1)
    frame = _damage_add_long(memory, frame, 'unit', frame.target_y)
    frame = _damage_divide(frame, 'unit', 5, 0x1CA8A)
    frame = _first_long(frame, 'unit', frame.unit & 65535)
    frame = _first_long(frame, 'count', frame.unit)
    gold, rice = memory.table(0xFFFFED84).cursor(), memory.table(0xFFFFEE24).cursor()
    frame = first_replace(frame, candidates=gold, controller=rice)
    side = memory.table(0xFFFFF6D7).byte()
    frame = _postbattle_bit_fields(frame, bool(side & 2))
    if side & 2:
        gold, rice = memory.table(0xFFFFDFFC).cursor(), memory.table(0xFFFFE09C).cursor()
        frame = first_replace(frame, candidates=gold, controller=rice)
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_x', city)
    frame = _first_shift_word(frame, 'target_x', city, 2)
    offset = u16(city << 2)
    for view, name in ((gold, 'unit'), (rice, 'count')):
        available = view.long(offset)
        frame = _first_long(frame, 'target_y', available)
        frame = _first_compare_long(frame, available, frame.carrier(name))
        if available < frame.carrier(name):
            frame = _first_long(frame, name, available)
        frame = _presentation_sub_long_fields(frame, 'target_y', frame.target_y, frame.carrier(name))
        view.set_long(offset, frame.target_y)
        frame = _first_long(frame, 'target_y', frame.target_y)
    for name, first in (('unit', 5), ('count', 9)):
        for displacement in (first + 3, first + 2, first + 1):
            value = low8(frame.carrier(name))
            frame.roster.set_byte(0, value, displacement)
            frame = _postbattle_memory_byte_fields(frame, value)
            if displacement != first + 1:
                frame = _movement_shift_long(memory.state, frame, name, True)
        if name == 'unit':
            frame = _first_shift_word(frame, name, low16(frame.unit), 8)
        else:
            frame = _first_right_word(frame, name, low16(frame.count), 8)
        value = low8(frame.carrier(name))
        frame.roster.set_byte(0, value, first)
        frame = _postbattle_memory_byte_fields(frame, value)
    return memory.finish(frame)


def _postbattle_rebuild_rosters_fields(memory, frame, secondary):
    """The two complete return flows share phases, not a second CPU algorithm."""
    if type(secondary) is not bool:
        raise ValueError('original primary/secondary return flow required')
    entry = 0x1CB08 if secondary else 0x1C82C
    frame = _city_outcome_frame_fields(memory, frame, entry)
    first_target, last_target = (0x1C2C8, 0x1C2A0) if secondary else (0x1C2A0, 0x1C2C8)
    frame = _city_outcome_call_fields(memory, frame, first_target, entry + 4)
    frame = _city_outcome_call_fields(memory, frame, 0x1C942, entry + 8)
    frame = _city_outcome_call_fields(memory, frame, last_target, entry + 12)
    incoming = low16(frame.count)
    frame = _first_word(frame, 'target_x', incoming)
    existing = memory.table(0xFFFFEFBA).word()
    frame = _first_add_word(frame, 'target_x', incoming, existing)
    total = u16(incoming + existing)
    from ..high_level_battle_ai.business_formation import _first_sub_word
    frame = _first_sub_word(frame, 'target_x', total, 10)
    if total > 10:
        frame = _city_outcome_call_fields(memory, frame, 0x1C8BC, 0x1CB26 if secondary else 0x1C84A)
    roster = memory.table(0xFFFFAF56).cursor()
    frame = first_replace(frame, roster=roster)
    while True:
        officer = roster.word()
        frame = _first_word(frame, 'target_x', officer)
        if negative_word(officer):
            break
        frame = _postbattle_bit_fields(frame, bool(frame.target_x & 16384))
        frame = first_replace(frame, target_x=frame.target_x | 16384)
        roster.set_word(0, low16(frame.target_x))
        roster = roster.advance(2)
        frame = first_replace(frame, roster=roster)
        frame = _first_memory_word(frame, low16(frame.target_x))
    first = memory.table(0xFFFFAF56).word()
    frame = _first_memory_word(frame, first)
    if not negative_word(first):
        owner = memory.table(0xFFFFF68D if secondary else 0xFFFFF68F).byte()
        memory.table(0xFFFFEFE2).set_byte(0, owner)
        frame = _postbattle_memory_byte_fields(frame, owner)
        frame = _city_outcome_call_fields(memory, frame, 0x1C9FE, 0x1CB4A if secondary else 0x1C86E)
        if not frame.status & 1:
            if secondary:
                memory.table(0xFFFFF6D6).word()
            memory.table(0xFFFFF6D6).set_word(0, 0 if secondary else 2)
            frame = _first_memory_word(frame, 0 if secondary else 2)
            frame = _city_outcome_call_fields(memory, frame, 0x21514, 0x1CB58 if secondary else 0x1C87E)
            frame = _city_outcome_call_fields(memory, frame, 0x1CA60, 0x1CB5C if secondary else 0x1C882)
        else:
            if secondary:
                frame = first_replace(frame, roster=memory.table(0xFFFFAF56).cursor())
            city = memory.table(0xFFFFF68A).word()
            frame = _first_word(frame, 'target_x', city)
            frame = _postbattle_bit_fields(frame, bool(frame.target_x & 128))
            frame = first_replace(frame, target_x=frame.target_x | 128)
            if not secondary:
                frame = first_replace(frame, roster=memory.table(0xFFFFAF56).cursor())
            frame = first_replace(frame, candidates=memory.table(0xFFFFCC00).cursor())
            while True:
                officer = frame.roster.word()
                frame = first_replace(frame, roster=frame.roster.advance(2))
                frame = _first_word(frame, 'target_y', officer)
                if negative_word(officer):
                    break
                officer &= 255
                frame = _first_word(frame, 'target_y', officer)
                frame.candidates.set_byte(officer, low8(frame.target_x))
                frame = _postbattle_memory_byte_fields(frame, low8(frame.target_x))
    heads = memory.table(0xFFFFE640).cursor()
    frame = first_replace(frame, roster=heads)
    force = memory.table(0xFFFFF68E if secondary else 0xFFFFF68C).word()
    frame = _first_word(frame, 'target_x', force)
    frame = _first_shift_word(frame, 'target_x', force, 1)
    ruler = heads.word(u16(force << 1))
    memory.table(0xFFFFF3F2).set_word(0, ruler)
    frame = _first_memory_word(frame, ruler)
    frame = _city_outcome_call_fields(memory, frame, 0x1CA3C, 0x1CB94 if secondary else 0x1C8BA)
    return memory.finish(frame)


def rebuild_primary_after_battle_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1C82C..1C8BC: primary return/survivor flow with real nested call slots."""
    return _postbattle_rebuild_rosters_fields(memory, frame, False)


def rebuild_secondary_after_battle_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1CB08..1CB96: reversed source owners and resource-side selection."""
    return _postbattle_rebuild_rosters_fields(memory, frame, True)



def _postbattle_progress_tail_fields(memory, frame, count):
    """Unique1C586..1C5E2 tail, shared by the two true original entries."""
    frame = _first_memory_word(frame, count)
    if count == 0:
        return memory.finish(frame)
    frame = _first_long(frame, 'target_x', low16(frame.target_x))
    frame = _damage_divide(frame, 'target_x', count, 0x1C592)
    roster = memory.table(0xFFFFD300).cursor()
    ability, progress = memory.table(0xFFFFC000).cursor(), memory.table(0xFFFFBE00).cursor()
    frame = first_replace(frame, roster=roster, candidates=ability, controller=progress)
    while True:
        member = roster.word()
        roster = roster.advance(2)
        frame = first_replace(frame, roster=roster)
        frame = _first_word(frame, 'target_y', member)
        if negative_word(member):
            return memory.finish(frame)
        frame = _first_shift_word(frame, 'target_y', member, 1)
        offset = u16(member << 1)
        current = ability.word(offset)
        frame = _first_word(frame, 'unit', current)
        comparison = progress.word(offset)
        frame = _first_compare_word(frame, current, comparison)
        destination = ability if current > comparison else progress
        if current <= comparison:
            current = progress.word(offset)
            frame = _first_word(frame, 'unit', current)
        frame = _first_add_word(frame, 'unit', current, low16(frame.target_x))
        result = u16(current + low16(frame.target_x))
        frame = _first_compare_word(frame, result, 999)
        if result > 999:
            result = 999
            frame = _first_word(frame, 'unit', result)
        destination.set_word(offset, result)
        frame = _first_memory_word(frame, result)

def distribute_battlefield_battle_progress_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1C5E2..1C5EE: distinct battlefield builder/EFBA budget, BRA1C586 tail."""
    frame = _city_outcome_frame_fields(memory, frame, 0x1C5E2)
    frame, count = _postbattle_candidates_fields(memory, frame, True, 0x1C5E6)
    budget = memory.table(0xFFFFEFBA).word()
    frame = _first_word(frame, 'target_x', budget)
    frame = _first_shift_word(frame, 'target_x', budget, 1)
    return _postbattle_progress_tail_fields(memory, frame, count)


# Current full consolidation/arrival successor; frozen history is unchanged.
def build_roster_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5F48..5F7C: nominated head first, then ascending256 live assignments."""
    frame = _city_outcome_frame_fields(memory, frame, 0x5F48)
    assignments, destination = memory.table(0xFFFFCC00).cursor(), memory.table(0xFFFFF500).cursor()
    frame = first_replace(frame, roster=assignments, candidates=destination)
    frame = _first_word(frame, 'target_y', 0)
    frame = _first_word(frame, 'count', 0)
    head = memory.table(0xFFFFF630).word()
    frame = _first_word(frame, 'distance', head)
    count = 0
    if not negative_word(head):
        destination.set_word(0, head)
        destination = destination.advance(2)
        frame = first_replace(frame, candidates=destination)
        frame = _first_memory_word(frame, head)
        frame = _first_add_word(frame, 'count', count, 1)
        count = 1
    officer = 0
    while True:
        assigned = assignments.byte()
        assignments = assignments.advance(1)
        frame = first_replace(frame, roster=assignments)
        frame = _postbattle_byte_carrier_fields(frame, 'unit', assigned)
        frame = _postbattle_compare_byte_fields(frame, assigned, low8(frame.target_x))
        if assigned == low8(frame.target_x):
            nominated = memory.table(0xFFFFF630).word()
            frame = _first_compare_word(frame, officer, nominated)
            if officer != nominated:
                destination.set_word(0, officer)
                destination = destination.advance(2)
                frame = first_replace(frame, candidates=destination)
                frame = _first_memory_word(frame, officer)
                frame = _first_add_word(frame, 'count', count, 1)
                count = u16(count + 1)
        frame = _first_add_word(frame, 'target_y', officer, 1)
        officer = u16(officer + 1)
        frame = _first_compare_word(frame, officer, 256)
        if officer >= 256:
            destination.set_word(0, 65535)
            return memory.finish(_first_memory_word(frame, 65535))


def roster_contains_force_head_carry_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E26C..E29E: choose actual owner's ruler only when in the live roster."""
    frame = _city_outcome_frame_fields(memory, frame, 0xE26C)
    city = low16(frame.target_x)
    owners = memory.table(0xFFFFF427).cursor()
    frame = first_replace(frame, controller=owners)
    frame = _first_word(frame, 'offset_x', 0)
    owner = owners.byte(city)
    frame = _postbattle_byte_carrier_fields(frame, 'offset_x', owner)
    frame = _first_shift_word(frame, 'offset_x', low16(frame.offset_x), 1)
    heads = memory.table(0xFFFFE640).cursor()
    frame = first_replace(frame, controller=heads)
    ruler = heads.word(low16(frame.offset_x))
    frame = _first_word(frame, 'offset_x', ruler)
    source = memory.table(0xFFFFF500).cursor()
    frame = first_replace(frame, controller=source)
    while True:
        token = source.word()
        frame = _first_memory_word(frame, token)
        if negative_word(token):
            return memory.finish(first_replace(frame, status=frame.status & 30))
        token = source.word()
        source = source.advance(2)
        frame = first_replace(frame, controller=source)
        frame = _first_compare_word(frame, ruler, token)
        if ruler == token:
            frame = _first_word(frame, 'distance', ruler)
            return memory.finish(first_replace(frame, status=frame.status | 1))


def choose_city_head_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E1F6..E26C: physical eight-LONG save and original strongest-head rule."""
    frame = _city_outcome_frame_fields(memory, frame, 0xE1F6)
    saved = ('target_y','unit','count','distance','offset_x','roster','candidates','controller')
    frame, observed = _damage_save_longs(memory, frame, saved)
    source = memory.table(0xFFFFF500).cursor()
    frame = first_replace(frame, roster=source)
    head = source.word()
    source = source.advance(2)
    frame = first_replace(frame, roster=source)
    frame = _first_word(frame, 'distance', head)
    if not negative_word(head):
        frame = _city_outcome_call_fields(memory, frame, 0xE26C, 0xE208)
        if not frame.status & 1:
            head = low16(frame.distance) & 255
            frame = _first_word(frame, 'distance', head)
            ratings = memory.table(0xFFFFC300).cursor()
            frame = first_replace(frame, candidates=ratings)
            frame = _first_word(frame, 'count', head)
            rating = ratings.byte(head)
            frame = _postbattle_byte_carrier_fields(frame, 'target_y', rating)
            frame = _postbattle_byte_carrier_fields(frame, 'unit', low8(frame.target_y))
            while True:
                officer = frame.roster.word()
                frame = first_replace(frame, roster=frame.roster.advance(2))
                frame = _first_word(frame, 'count', officer)
                if negative_word(officer):
                    break
                officer &= 255
                frame = _first_word(frame, 'count', officer)
                rating = frame.candidates.byte(officer)
                frame = _postbattle_byte_carrier_fields(frame, 'target_y', rating)
                frame = _postbattle_compare_byte_fields(frame, rating, low8(frame.unit))
                if rating > low8(frame.unit):
                    frame = _first_word(frame, 'distance', officer)
                    frame = _postbattle_byte_carrier_fields(frame, 'unit', low8(frame.target_y))
    else:
        owners = memory.table(0xFFFFF427).cursor()
        frame = first_replace(frame, roster=owners)
        owners.set_byte(low16(frame.target_x), 255)
        frame = _postbattle_memory_byte_fields(frame, 255)
        orders = memory.table(0xFFFFE80C).cursor()
        frame = first_replace(frame, roster=orders)
        city = low16(frame.target_x)
        frame = _first_word(frame, 'target_y', city)
        frame = _first_shift_word(frame, 'target_y', city, 1)
        frame = _first_add_word(frame, 'target_y', low16(frame.target_y), city)
        frame = _first_shift_word(frame, 'target_y', low16(frame.target_y), 2)
        for displacement in (0,4,8):
            orders.set_word(low16(frame.target_y), 65535, displacement)
            frame = _first_memory_word(frame, 65535)
    city = low16(frame.target_x)
    frame = _first_shift_word(frame, 'target_x', city, 1)
    heads = memory.table(0xFFFFF45E).cursor()
    frame = first_replace(frame, roster=heads)
    head = low16(frame.distance)
    heads.set_word(low16(frame.target_x), head)
    frame = _first_memory_word(frame, head)
    frame = _first_word(frame, 'target_x', head)
    return _damage_restore_longs(memory, frame, saved, observed)


def consolidate_city_after_battle_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1CB96..1CC26: consolidate aliases, roster and current city head.

    Food is read at E09C but the combined result is stored at EE24; gold
    staging is read at ED88, not ED84. These original aliases are retained.
    1CC26..1CC76 has no cached owner and is not included as code.
    """
    frame = _city_outcome_frame_fields(memory, frame, 0x1CB96)
    frame = _city_outcome_call_fields(memory, frame, 0x1C2C8, 0x1CB9A)
    assignments, roster = memory.table(0xFFFFCC00).cursor(), memory.table(0xFFFFD300).cursor()
    frame = first_replace(frame, roster=assignments, candidates=roster)
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_x', city)
    while True:
        officer = roster.word()
        roster = roster.advance(2)
        frame = first_replace(frame, candidates=roster)
        frame = _first_word(frame, 'target_y', officer)
        if negative_word(officer):
            break
        assignments.set_byte(officer, low8(frame.target_x))
        frame = _postbattle_memory_byte_fields(frame, low8(frame.target_x))
    owners = memory.table(0xFFFFF427).cursor()
    frame = first_replace(frame, roster=owners)
    owner = memory.table(0xFFFFF68D).byte()
    owners.set_byte(low16(frame.target_x), owner)
    frame = _postbattle_memory_byte_fields(frame, owner)
    gold = memory.table(0xFFFFDFFC).cursor()
    frame = first_replace(frame, roster=gold)
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_x', city)
    frame = _first_shift_word(frame, 'target_x', city, 2)
    offset = u16(city << 2)
    from ..high_level_battle_ai.business_formation import _first_compare_long
    for source_address, staging_address, destination_is_staging in (
            (0xFFFFDFFC,0xFFFFED88,False),(0xFFFFE09C,0xFFFFEE24,True)):
        if destination_is_staging:
            frame = first_replace(frame, roster=memory.table(source_address).cursor())
        value = frame.roster.long(offset)
        frame = _first_long(frame, 'target_y', value)
        frame = first_replace(frame, candidates=memory.table(staging_address).cursor())
        frame = _damage_add_long(memory, frame, 'target_y', frame.candidates.long(offset))
        frame = _first_compare_long(frame, frame.target_y, 999999)
        if frame.target_y > 999999:
            frame = _first_long(frame, 'target_y', 999999)
        destination = frame.candidates if destination_is_staging else frame.roster
        destination.set_long(offset, frame.target_y)
        frame = _first_long(frame, 'target_y', frame.target_y)
    memory.table(0xFFFFF630).set_word(0, 65535)
    frame = _first_memory_word(frame, 65535)
    frame = _first_word(frame, 'target_x', memory.table(0xFFFFF68A).word())
    frame = _city_outcome_call_fields(memory, frame, 0x5F48, 0x1CC1A)
    frame = _first_word(frame, 'target_x', memory.table(0xFFFFF68A).word())
    return _city_outcome_call_fields(memory, frame, 0xE1F6, 0x1CC24)


def choose_empty_neighbor_position_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """21EFE..21F82: actual ordered neighbors, terrain sign and packet occupancy.

    The original search has no synthetic neighbor limit. A failed candidate
    advances only A6; success returns the real packet terminator in A1.
    """
    frame = _city_outcome_frame_fields(memory, frame, 0x21EFE)
    neighbors = memory.table(0x21F82).cursor()
    costs, terrain = memory.table(0x670A).cursor(), memory.table(0xEE5F0).cursor()
    frame = first_replace(frame, auxiliary=neighbors, scratch=costs, opponent=terrain)
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_x', city)
    frame = _first_shift_word(frame, 'target_x', city, 2)
    coordinates = memory.table(0xD4AC6).cursor()
    frame = first_replace(frame, candidates=coordinates)
    row = coordinates.word(u16(city << 2), 2)
    frame = _first_word(frame, 'choice', row)
    frame = _first_right_word(frame, 'choice', row, 4)
    column = coordinates.word(u16(city << 2))
    frame = _first_word(frame, 'offset_y', column)
    frame = _first_right_word(frame, 'offset_y', column, 4)
    while True:
        frame = _first_word(frame, 'target_x', low16(frame.choice))
        frame = _first_add_word(frame, 'target_x', low16(frame.target_x), neighbors.word())
        frame = _first_compare_word(frame, low16(frame.target_x), 72)
        if low16(frame.target_x) < 72:
            frame = _first_word(frame, 'target_y', low16(frame.offset_y))
            frame = _first_add_word(frame, 'target_y', low16(frame.target_y), neighbors.word(0, 2))
            frame = _first_compare_word(frame, low16(frame.target_y), 72)
            if low16(frame.target_y) < 72:
                frame = _first_word(frame, 'unit', low16(frame.target_x))
                frame = _first_shift_word(frame, 'unit', low16(frame.unit), 3)
                frame = _first_add_word(frame, 'unit', low16(frame.unit), low16(frame.target_x))
                frame = _first_shift_word(frame, 'unit', low16(frame.unit), 3)
                frame = _first_add_word(frame, 'unit', low16(frame.unit), low16(frame.target_y))
                frame = _first_word(frame, 'count', 0)
                kind = terrain.byte(low16(frame.unit))
                frame = _postbattle_byte_carrier_fields(frame, 'count', kind)
                cost = costs.byte(low16(frame.count))
                frame = _postbattle_memory_byte_fields(frame, cost)
                if not negative_byte(cost):
                    groups = memory.table(0xFFFF9000).cursor()
                    frame = first_replace(frame, candidates=groups)
                    while True:
                        header = groups.byte()
                        frame = _postbattle_byte_carrier_fields(frame, 'unit', header)
                        members = header & 15
                        frame = _first_word(frame, 'unit', members)
                        if members == 0:
                            return memory.finish(frame)
                        present_row = groups.byte(0, 1)
                        frame = _postbattle_compare_byte_fields(frame, low8(frame.target_x), present_row)
                        occupied = low8(frame.target_x) == present_row
                        if occupied:
                            present_column = groups.byte(0, 2)
                            frame = _postbattle_compare_byte_fields(frame, low8(frame.target_y), present_column)
                            occupied = low8(frame.target_y) == present_column
                        if occupied:
                            break
                        groups = groups.advance(13 + s16(members))
                        frame = first_replace(frame, candidates=groups)
        neighbors = neighbors.advance(4)
        frame = first_replace(frame, auxiliary=neighbors)


def append_group_from_survivor_roster_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """21514..2159E: append selected survivors, mark assignments and average.

    No host packet copy is used. A0 remains the real insertion packet across
    the neighbor child; the child's actual D0/D1 are then stored as coordinates.
    """
    frame = _city_outcome_frame_fields(memory, frame, 0x21514)
    packet, assignments = memory.table(0xFFFF9000).cursor(), memory.table(0xFFFFCC00).cursor()
    frame = first_replace(frame, roster=packet, controller=assignments)
    while True:
        header = packet.byte()
        frame = _postbattle_byte_carrier_fields(frame, 'target_x', header)
        members = header & 15
        frame = _first_word(frame, 'target_x', members)
        if members == 0:
            break
        packet = packet.advance(13 + s16(members))
        frame = first_replace(frame, roster=packet)
    frame = _first_word(frame, 'target_x', 0)
    source = memory.table(0xFFFFAF56).cursor()
    frame = first_replace(frame, candidates=source)
    count = 0
    while True:
        officer = source.word()
        source = source.advance(2)
        frame = first_replace(frame, candidates=source)
        frame = _first_word(frame, 'target_y', officer)
        if negative_word(officer):
            break
        frame = _postbattle_bit_fields(frame, bool(frame.target_y & 16384))
        if not frame.target_y & 16384:
            continue
        packet.set_byte(count, low8(frame.target_y), 13)
        frame = _postbattle_memory_byte_fields(frame, low8(frame.target_y))
        frame = _first_add_word(frame, 'target_x', count, 1)
        count = u16(count + 1)
        officer &= 255
        frame = _first_word(frame, 'target_y', officer)
        previous = assignments.byte(officer)
        assignments.set_byte(officer, previous | 64)
        frame = _postbattle_bit_fields(frame, bool(previous & 64))
    packet.byte(count, 13)
    packet.set_byte(count, 0, 13)
    frame = _postbattle_memory_byte_fields(frame, 0)
    packet.set_byte(0, low8(frame.target_x))
    frame = _postbattle_memory_byte_fields(frame, low8(frame.target_x))
    side = memory.table(0xFFFFF6D7).byte()
    frame = _postbattle_bit_fields(frame, bool(side & 2))
    force = memory.table(0xFFFFF68E if side & 2 else 0xFFFFF68C).word()
    frame = _first_word(frame, 'target_y', force)
    packet.set_byte(0, low8(frame.target_y), 4)
    frame = _postbattle_memory_byte_fields(frame, low8(frame.target_y))
    attributes = memory.table(0xFFFFC400).cursor()
    frame = first_replace(frame, candidates=attributes)
    frame = _first_word(frame, 'target_y', low16(frame.target_x))
    from ..high_level_battle_ai.business_formation import _first_sub_word
    frame = _first_sub_word(frame, 'target_y', low16(frame.target_y), 1)
    frame = _first_long(frame, 'unit', 0)
    frame = _first_word(frame, 'count', 0)
    for counter in descending_inclusive(u16(count - 1)):
        officer = packet.byte(counter, 13)
        frame = _postbattle_byte_carrier_fields(frame, 'count', officer)
        value = attributes.byte(low16(frame.count))
        frame = _postbattle_byte_carrier_fields(frame, 'count', value)
        frame = _first_add_word(frame, 'unit', low16(frame.unit), low16(frame.count))
        frame = _postbattle_decrement_fields(frame, 'target_y', counter)
    frame = _damage_divide(frame, 'unit', low16(frame.target_x), 0x2158A)
    packet.set_byte(0, low8(frame.unit), 3)
    frame = _postbattle_memory_byte_fields(frame, low8(frame.unit))
    frame = _city_outcome_call_fields(memory, frame, 0x21EFE, 0x21594)
    frame.roster.set_byte(0, low8(frame.target_x), 1)
    frame = _postbattle_memory_byte_fields(frame, low8(frame.target_x))
    frame.roster.set_byte(0, low8(frame.target_y), 2)
    return memory.finish(_postbattle_memory_byte_fields(frame, low8(frame.target_y)))


# Sole reserve-gated duel decision and true RNG call.
"""The original reserve-vs-draw duel gate, with actual retained fields."""


def city_reserve_forces_duel_carry_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1E422..1E464: one RNG draw, threshold100, actual SR carry decision.

    D0 retains its upper WORD when loading city/reserve. D1 is cleared only
    by the original MOVEQ, D2 observes that seed, and the shift/add sequence
    exposes the original CCR rather than replacing it with a Python product.
    The caller owns its outer return; this body owns only RNG's1E428 slot.
    """
    frame = _city_outcome_frame_fields(memory, frame, 0x1E422)
    frame = _presentation_call_fields(memory, frame, 0x1E428, _presentation_random_fields)
    city = memory.table(0xFFFFF68A).word()
    frame = _first_word(frame, 'target_x', city)
    frame = _first_shift_word(frame, 'target_x', city, 2)
    reserves = memory.table(0xFFFFE59C).cursor()
    frame = first_replace(frame, roster=reserves)
    reserve = reserves.word(u16(city << 2), 2)
    frame = _first_word(frame, 'target_x', reserve)
    frame = _first_compare_word(frame, reserve, 30)
    choose_duel = False
    if reserve < 30:
        frame = _first_long(frame, 'target_y', 0)
        seed = memory.table(0xFFFFF61C).word()
        frame = _first_word(frame, 'target_y', seed)
        frame = _first_long(frame, 'unit', frame.target_y)
        frame = _postbattle_shift_long_fields(memory, frame, 'target_y', 1)
        frame = _damage_add_long(memory, frame, 'target_y', frame.unit)
        frame = _postbattle_shift_long_fields(memory, frame, 'target_y', 3)
        frame = _damage_add_long(memory, frame, 'target_y', frame.unit)
        frame = _postbattle_shift_long_fields(memory, frame, 'target_y', 2)
        frame = _first_long(frame, 'target_y', swap_words(frame.target_y))
        frame = _first_compare_word(frame, low16(frame.target_y), reserve)
        choose_duel = low16(frame.target_y) >= reserve
    # ORI/ANDI.W operate on the true SR and change only its C bit here.
    memory.finish(frame)
    status = (memory.state.read_status_word() & 65534) | int(choose_duel)
    memory.state.set_status_word(status)
    return first_replace(frame, status=status & 31)

def _battle_labels_frame(memory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from .contexts_services import SceneRefreshMemory, SceneRefreshBoundary
    if type(memory) is not SceneRefreshMemory:
        raise ValueError('same-state Scene label memory required')
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x177BE,frame,None)
    return memory.sync_status(frame)

def _battle_labels_call_fields(memory, frame: FirstDeploymentFrame, target: Long, continuation: Long) -> FirstDeploymentFrame:
    from .contexts_services import SceneRefreshBoundary
    from ..high_level_scene_flows.business_scene import decode_glyph_rows_to_buffers_fields, expand_glyph_stream_fields
    from .business_reuse import sum_group_troops_fields
    if (target,continuation) not in ((0xAE8A,0x177F6),(0xAE8A,0x1782E),
            (0xAE8A,0x179EA),(0xAE8A,0x17A06),(0xAF1E,0x178B6),(0xAF1E,0x17916),
            (0x179D6,0x17866),(0x179D6,0x17888),(0x17988,0x17986),
            (0x179BE,0x17994),(0x179BE,0x179A4)):
        raise ValueError('actual label child and return token required')
    entered = memory.sync_status(frame)
    if frame.stack_cursor is not None:
        stack = frame.stack_cursor.advance(-4)
        stack.set_long(0,continuation)
        entered = first_replace(frame,stack_cursor=stack)
    if target == 0xAE8A:
        returned = decode_glyph_rows_to_buffers_fields(memory,entered)
    elif target == 0xAF1E:
        returned = expand_glyph_stream_fields(memory,entered)
    elif target == 0x179D6:
        returned = append_force_head_glyphs_fields(memory,entered)
    elif target == 0x17988:
        returned = cache_battle_roster_totals_fields(memory,entered)
    else:
        returned, observed_count = sum_group_troops_fields(memory,entered)
    memory.frame(returned)
    if frame.stack_cursor is not None:
        memory.sync_status(returned)
        actual = returned.stack_cursor.long()
        if actual != continuation:
            raise SceneRefreshBoundary(target,returned,continuation)
        returned = first_replace(returned,stack_cursor=returned.stack_cursor.advance(4))
    return memory.sync_status(returned)

def _battle_labels_upload_longs_fields(memory, frame: FirstDeploymentFrame, counter_name, inclusive: Word) -> FirstDeploymentFrame:
    from .business_services import _scene_refresh_emit, _scene_refresh_decrement
    frame = _first_word(frame,counter_name,inclusive)
    remaining = inclusive
    while True:
        source = frame.candidates
        value = source.long()
        frame = first_replace(frame,candidates=source.advance(4))
        frame = _scene_refresh_emit(memory,frame,0xC00000,4,value)
        frame = _scene_refresh_decrement(frame,counter_name,remaining)
        remaining = u16(remaining - 1)
        if remaining == 65535:
            return frame

def append_force_head_glyphs_fields(memory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """179D6: the original optional two sixteen-LONG head-label spacers."""
    from .contexts_services import SceneRefreshBoundary
    from .business_services import _scene_refresh_emit, _scene_refresh_decrement
    memory.frame(frame)
    if frame.roster is None or frame.candidates is None:
        raise SceneRefreshBoundary(0x179D6,frame,None)
    marker = frame.roster.word(4)
    frame = _first_compare_word(frame,marker,63)
    if marker != 63:
        frame = _first_word(frame,'count',2)
        return _battle_labels_call_fields(memory,frame,0xAE8A,0x179EA)
    spacer_longs = 16
    frame = _first_word(frame,'count',spacer_longs - 1)
    for index in range(spacer_longs):
        destination = frame.candidates
        frame = first_replace(frame,candidates=destination.advance(4))
        frame = _scene_refresh_emit(memory,frame,destination.base,4,0x11111111)
        frame = _scene_refresh_decrement(frame,'count',spacer_longs - 1 - index)
    frame = _first_word(frame,'count',1)
    frame = _battle_labels_call_fields(memory,frame,0xAE8A,0x17A06)
    frame = _first_word(frame,'count',spacer_longs - 1)
    for index in range(spacer_longs):
        destination = frame.candidates
        frame = first_replace(frame,candidates=destination.advance(4))
        frame = _scene_refresh_emit(memory,frame,destination.base,4,0x11111111)
        frame = _scene_refresh_decrement(frame,'count',spacer_longs - 1 - index)
    return memory.sync_status(frame)

def cache_battle_roster_totals_fields(memory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """17988: live primary/secondary sums and the selected city reserve WORD."""
    from .business_services import _scene_refresh_emit
    frame = _battle_labels_frame(memory,frame)
    frame = first_replace(frame,roster=memory.cursor_at(0xFFFFC800),candidates=memory.cursor_at(0xFFFFA550))
    frame = _battle_labels_call_fields(memory,frame,0x179BE,0x17994)
    frame = _scene_refresh_emit(memory,frame,0xFFFFF6AE,4,frame.target_x)
    frame = _scene_refresh_emit(memory,frame,0xFFFFF6A6,2,low16(frame.target_y))
    frame = first_replace(frame,candidates=memory.cursor_at(0xFFFFA5A4))
    frame = _battle_labels_call_fields(memory,frame,0x179BE,0x179A4)
    frame = _scene_refresh_emit(memory,frame,0xFFFFF6B2,4,frame.target_x)
    frame = _scene_refresh_emit(memory,frame,0xFFFFF6A8,2,low16(frame.target_y))
    city = memory.cursor_at(0xFFFFF68A).word()
    frame = _first_word(frame,'target_x',city)
    frame = _first_shift_word(frame,'target_x',city,2)
    frame = first_replace(frame,roster=memory.cursor_at(0xFFFFE59C))
    reserve = frame.roster.word(low16(frame.target_x),2)
    return memory.sync_status(_scene_refresh_emit(memory,frame,0xFFFFF6BE,2,reserve))

def upload_battle_scene_labels_fields(memory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """177BE sole composition order, glyph buffers, physical calls and VDP writes."""
    from .business_services import _scene_refresh_emit, _scene_refresh_decrement
    from ..high_level_main_flows.business_movement_support import _movement_binary_flags
    frame = _battle_labels_frame(memory,frame)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,0x40200002)
    fill_longs = 32
    frame = _first_word(frame,'target_x',fill_longs - 1)
    for index in range(fill_longs):
        frame = _scene_refresh_emit(memory,frame,0xC00000,4,0x11111111)
        frame = _scene_refresh_decrement(frame,'target_x',fill_longs - 1 - index)
    frame = first_replace(frame,roster=memory.cursor_at(0x6BF58),candidates=memory.cursor_at(0xFFFFD300))
    frame = _first_word(frame,'target_x',1)
    frame = _first_word(frame,'target_y',3)
    frame = _first_word(frame,'count',10)
    frame = _battle_labels_call_fields(memory,frame,0xAE8A,0x177F6)
    frame = first_replace(frame,candidates=memory.cursor_at(0xFFFFD300))
    frame = _battle_labels_upload_longs_fields(memory,frame,'count',351)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,0x48000002)
    city = memory.cursor_at(0xFFFFF68A).word()
    frame = _first_word(frame,'count',city)
    frame = _first_shift_word(frame,'count',city,2)
    frame = first_replace(frame,roster=memory.cursor_at(0x8A212,low16(frame.count)),candidates=memory.cursor_at(0xFFFFD300))
    frame = _first_word(frame,'count',1)
    frame = _battle_labels_call_fields(memory,frame,0xAE8A,0x1782E)
    frame = first_replace(frame,candidates=memory.cursor_at(0xFFFFD300))
    frame = _battle_labels_upload_longs_fields(memory,frame,'count',63)
    for owner_address,continuation in ((0xFFFFF68E,0x17866),(0xFFFFF68C,0x17888)):
        owner = memory.cursor_at(owner_address).word()
        frame = _first_word(frame,'distance',owner)
        frame = _first_shift_word(frame,'distance',owner,1)
        frame = first_replace(frame,controller=memory.cursor_at(0xFFFFE640))
        ruler = frame.controller.word(low16(frame.distance))
        frame = _first_word(frame,'distance',ruler)
        frame = _first_word(frame,'offset_x',ruler)
        frame = _first_shift_word(frame,'distance',ruler,1)
        before = low16(frame.distance)
        frame,offset = _movement_binary_flags(memory.state,frame,before,ruler,16)
        frame = first_replace(frame,distance=replace_word(frame.distance,offset))
        frame = _first_shift_word(frame,'distance',offset,1)
        frame = first_replace(frame,roster=memory.cursor_at(0x8A504,low16(frame.distance)))
        if continuation == 0x17866:
            frame = first_replace(frame,candidates=memory.cursor_at(0xFFFFD300))
        frame = _battle_labels_call_fields(memory,frame,0x179D6,continuation)
    frame = first_replace(frame,candidates=memory.cursor_at(0xFFFFD300))
    frame = _battle_labels_upload_longs_fields(memory,frame,'count',191)
    frame = first_replace(frame,roster=memory.cursor_at(0x8A426),candidates=memory.cursor_at(0xFFFFD300))
    frame = _first_word(frame,'target_x',3)
    frame = _first_word(frame,'target_y',1)
    frame = _first_word(frame,'count',9)
    frame = _battle_labels_call_fields(memory,frame,0xAF1E,0x178B6)
    frame = first_replace(frame,candidates=memory.cursor_at(0xFFFFD300))
    frame = _battle_labels_upload_longs_fields(memory,frame,'count',79)
    frame = first_replace(frame,candidates=memory.cursor_at(0x6C174))
    frame = _battle_labels_upload_longs_fields(memory,frame,'count',15)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,0x70000001)
    frame = first_replace(frame,candidates=memory.cursor_at(0x6BF6E))
    frame = _battle_labels_upload_longs_fields(memory,frame,'count',47)
    frame = first_replace(frame,roster=memory.cursor_at(0x8A426),candidates=memory.cursor_at(0xFFFFD300))
    frame = _first_word(frame,'target_x',1)
    frame = _first_word(frame,'target_y',3)
    frame = _first_word(frame,'count',9)
    frame = _battle_labels_call_fields(memory,frame,0xAF1E,0x17916)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,0x70C00001)
    frame = first_replace(frame,candidates=memory.cursor_at(0xFFFFD300))
    frame = _battle_labels_upload_longs_fields(memory,frame,'unit',79)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,0x60000002)
    frame = first_replace(frame,candidates=memory.cursor_at(0xABA1E))
    frame = _battle_labels_upload_longs_fields(memory,frame,'target_x',23)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,0x5A000002)
    frame = first_replace(frame,candidates=memory.cursor_at(0x6C02E))
    frame = _battle_labels_upload_longs_fields(memory,frame,'target_y',31)
    frame = first_replace(frame,candidates=memory.cursor_at(0x6C0E8))
    frame = _battle_labels_upload_longs_fields(memory,frame,'target_y',31)
    return _battle_labels_call_fields(memory,frame,0x17988,0x17986)


# Current full packed-member result successor; frozen Army history is unchanged.
def _packed_save_word_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame, name: str) -> FirstDeploymentFrame:
    """The actual MOVE.W predecrement save, including its observable MOVE CCR."""
    from ..high_level_main_flows.business_movement_support import _movement_test
    if name not in ('target_x','target_y','count'):
        raise ValueError('original packed member saved WORD carrier required')
    stack = frame.stack_cursor.advance(-2)
    value = low16(frame.carrier(name))
    stack.set_word(0, value)
    return _movement_test(memory.state, first_replace(frame, stack_cursor=stack), value, 16)


def _packed_restore_word_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame, name: str) -> FirstDeploymentFrame:
    """Read back the saved physical WORD, retaining the current high WORD."""
    from ..high_level_main_flows.business_movement_support import _movement_move
    if name not in ('target_x','target_y','count'):
        raise ValueError('original packed member restored WORD carrier required')
    value = frame.stack_cursor.word()
    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
    return _movement_move(memory.state, frame, name, value, 16)


def _packed_seek_reference_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame, head_name: str, address_name: str, postincrement: bool) -> tuple:
    """Project the existing pair scan into its two real carrier layouts."""
    from ..high_level_remaining_flows.business_city import _settlement_seek_pair_member_fields
    if (head_name,address_name,postincrement) not in (('count','roster',True),('target_x','candidates',False)):
        raise ValueError('actual packed reference scan roles required')
    source = frame.roster if address_name == 'roster' else frame.candidates
    projected = first_replace(frame, target_x=frame.carrier(head_name), roster=source.cursor())
    projected, found = _settlement_seek_pair_member_fields(memory.state, projected)
    cursor = projected.roster if postincrement else projected.roster.advance(-2 if found else -1)
    return first_replace(frame, **{address_name:cursor}, status=projected.status), found


def _packed_relabel_active_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame, header_blind: bool) -> FirstDeploymentFrame:
    """Reuse the sole live active-record relabel kernel, preserving A0/A1 ownership."""
    from ..high_level_remaining_flows.business_city import _settlement_relabel_active_member_fields
    if type(header_blind) is not bool:
        raise ValueError('original header-blind relabel policy required')
    if header_blind:
        projected = first_replace(frame, roster=frame.candidates.cursor())
        projected = _settlement_relabel_active_member_fields(memory.state, projected, 'target_y', None)
        return first_replace(frame, candidates=projected.roster, status=projected.status)
    projected = first_replace(frame, target_x=frame.count)
    projected = _settlement_relabel_active_member_fields(memory.state, projected, 'distance', False)
    return first_replace(frame, roster=projected.roster, status=projected.status)


def _packed_slide_tail_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame, from_second: bool) -> FirstDeploymentFrame:
    """Observe the sole live packet-tail slide through the actual D1/A1/A2 roles."""
    from ..high_level_remaining_flows.business_city import _settlement_slide_member_tail_fields
    if type(from_second) is not bool:
        raise ValueError('actual packed tail source role required')
    source = frame.candidates if from_second else frame.controller
    destination = frame.controller if from_second else frame.candidates
    projected = first_replace(frame, unit=frame.target_y, scan=source.cursor(), controller=destination)
    projected = _settlement_slide_member_tail_fields(memory.state, projected, 'scan', 'controller')
    return first_replace(frame, target_y=projected.unit,
        candidates=projected.scan if from_second else projected.controller.cursor(),
        controller=memory.table(projected.controller.base if from_second else projected.scan.base), status=projected.status)


def _packed_compact_reference_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame, from_second: bool) -> FirstDeploymentFrame:
    """The existing paired-byte compactor retains the genuine two-byte cursor gap."""
    from ..high_level_remaining_flows.business_city import _settlement_compact_pair_member_fields
    if type(from_second) is not bool:
        raise ValueError('original pair compaction carrier layout required')
    source = frame.controller if from_second else frame.roster
    projected = first_replace(frame, roster=source.cursor())
    projected = _settlement_compact_pair_member_fields(memory.state, projected)
    destination = projected.roster.advance(-2)
    if from_second:
        return first_replace(frame, candidates=destination, controller=memory.table(projected.roster.base), status=projected.status)
    return first_replace(frame, roster=projected.roster, candidates=destination, status=projected.status)


def settle_battle_packed_armies_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1D03C..1D0A2: transfer the outcome officer, remove losses, then settle arrival."""
    frame = _city_outcome_frame_fields(memory, frame, 0x1D03C)
    from ..high_level_main_flows.business_movement_support import _movement_move, _movement_test, _movement_test_long, _movement_shift_word
    frame = _city_outcome_call_fields(memory, frame, 0x1D198, 0x1D040)
    frame = first_replace(frame, candidates=memory.table(memory.table(0x00FF382C).long()).cursor(),
        controller=memory.table(0xFFFF9000), scan=memory.table(0xFFFFEFBE).cursor())
    frame = _movement_move(memory.state, frame, 'target_x', memory.table(0xFFFFEFC6).word(), 16)
    frame = first_replace(frame, controller=frame.controller.advance(s16(frame.scan.word(low16(frame.target_x)))),
        roster=memory.table(0xFFFFB200).cursor())
    frame = _movement_move(memory.state, frame, 'target_x', memory.table(0xFFFFF702).word(), 16)
    frame = _movement_shift_word(memory.state, frame, 'target_x')
    frame = _movement_test(memory.state, frame, frame.roster.word(low16(frame.target_x)), 16)
    if frame.status & 4:
        frame = _movement_move(memory.state, frame, 'target_x', memory.table(0xFFFFF702).word(), 16)
        frame = _city_outcome_call_fields(memory, frame, 0x1D0A2, 0x1D070)
        memory.table(0x00FF382C).long()
        memory.table(0x00FF382C).set_long(0, 0)
        frame = _movement_test_long(memory.state, frame, 0)
    frame = first_replace(frame, candidates=frame.controller.cursor(), controller=memory.table(frame.candidates.base),
        roster=memory.table(0xFFFFB200).cursor())
    frame = _movement_move(memory.state, frame, 'target_x', memory.table(0xFFFFF706).word(), 16)
    frame = _movement_shift_word(memory.state, frame, 'target_x')
    frame = _movement_test(memory.state, frame, frame.roster.word(low16(frame.target_x)), 16)
    if frame.status & 4:
        frame = _movement_move(memory.state, frame, 'target_x', memory.table(0xFFFFF706).word(), 16)
        frame = _city_outcome_call_fields(memory, frame, 0x1D0A2, 0x1D092)
        memory.table(0x00FF382C).set_long(0, frame.controller.base)
        frame = _movement_test_long(memory.state, frame, frame.controller.base)
    frame = _city_outcome_call_fields(memory, frame, 0x1D3BC, 0x1D09C)
    return _city_outcome_call_fields(memory, frame, 0x1D4DA, 0x1D0A0)


def remove_defeated_packed_member_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1D0A2..1D142: seven real saved LONGs, removal, references and aliased A2 repair."""
    frame = _city_outcome_frame_fields(memory, frame, 0x1D0A2)
    from ..high_level_main_flows.business_movement_support import _movement_move, _movement_compare, _movement_adjust_word, _movement_move_long, _movement_binary_flags, _movement_compare_address
    from ..high_level_remaining_flows.business_city import _settlement_write_byte_fields, _settlement_change_header_byte_fields
    names = ('target_y','unit','count','distance','roster','candidates','controller')
    frame, observed = _damage_save_longs(memory, frame, names)
    frame = first_replace(frame, roster=memory.table(0xFFFFCC00).cursor())
    frame = _settlement_write_byte_fields(memory.state, frame, frame.roster, 255, low16(frame.target_x))
    frame = _movement_move(memory.state, frame, 'count', 0, 16)
    frame = _movement_move(memory.state, frame, 'count', frame.candidates.byte(0, 13), 8)
    frame = first_replace(frame, roster=frame.candidates.cursor())
    frame = _movement_move(memory.state, frame, 'target_y', frame.candidates.byte(), 8)
    frame = _movement_move(memory.state, frame, 'target_y', low16(frame.target_y) & 15, 16)
    frame = _movement_compare(memory.state, frame, low16(frame.target_y), 1, 16)
    if not frame.status & 4:
        frame = _settlement_change_header_byte_fields(memory.state, frame, frame.candidates, True)
        frame = _movement_move(memory.state, frame, 'unit', 0, 16)
        frame = _movement_move(memory.state, frame, 'offset_x', 1, 16)
        while True:
            frame = _movement_compare(memory.state, frame, low8(frame.target_x), frame.candidates.byte(low16(frame.unit), 13), 8)
            if frame.status & 4:
                break
            frame = _movement_adjust_word(memory.state, frame, 'unit', 1)
        while True:
            frame = _movement_adjust_word(memory.state, frame, 'unit', 1)
            frame = _movement_compare(memory.state, frame, low16(frame.target_y), low16(frame.unit), 16)
            if frame.status & 4:
                break
            frame = _settlement_write_byte_fields(memory.state, frame, frame.candidates,
                frame.candidates.byte(low16(frame.unit), 13), low16(frame.unit), 12)
        packet = frame.candidates
        frame = first_replace(frame, controller=packet.advance(s16(low16(frame.target_y)) + 13),
            candidates=packet.advance(s16(low16(frame.target_y)) + 12))
        frame = _movement_move(memory.state, frame, 'distance', 0, 16)
        frame = _movement_move(memory.state, frame, 'distance', frame.roster.byte(0, 13), 8)
    else:
        frame = _movement_move(memory.state, frame, 'distance', 65535, 16)
        frame = _movement_move(memory.state, frame, 'offset_x', 14, 16)
        frame = first_replace(frame, controller=frame.candidates.advance(s16(low16(frame.target_y)) + 13))
    frame = _packed_slide_tail_fields(memory, frame, False)
    frame = _city_outcome_call_fields(memory, frame, 0x1D142, 0x1D126)
    frame = _damage_restore_longs(memory, frame, names, observed)
    frame = _movement_compare_address(memory.state, frame, frame.controller.base, frame.candidates.base)
    if not frame.status & 1:
        frame = _movement_move_long(memory.state, frame, 'offset_x', frame.offset_x & 65535)
        frame, pointer = _movement_binary_flags(memory.state, frame, frame.controller.base, frame.offset_x, 32, True)
        frame = first_replace(frame, controller=memory.table(pointer))
    return memory.finish(frame)


def replace_or_remove_group_references_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1D142..1D198: paired references and active-head replacement share one live scan."""
    frame = _city_outcome_frame_fields(memory, frame, 0x1D142)
    from ..high_level_main_flows.business_movement_support import _movement_compare, _movement_test
    from ..high_level_remaining_flows.business_city import _settlement_write_byte_fields
    frame = _movement_compare(memory.state, frame, low16(frame.distance), low16(frame.count), 16)
    if frame.status & 4:
        return memory.finish(frame)
    frame = first_replace(frame, roster=memory.table(0x00FF39B2).advance(s16(memory.table(0x00FF3BB2).word())).cursor())
    frame, found = _packed_seek_reference_fields(memory, frame, 'count', 'roster', True)
    if not found:
        return memory.finish(frame)
    frame = _movement_test(memory.state, frame, low16(frame.distance), 16)
    if frame.status & 8:
        frame = first_replace(frame, candidates=frame.roster.advance(-2))
        return memory.finish(_packed_compact_reference_fields(memory, frame, False))
    frame = _settlement_write_byte_fields(memory.state, frame, frame.roster, low8(frame.distance), displacement=-1)
    frame = first_replace(frame, roster=memory.table(0x00FF3000).cursor())
    return memory.finish(_packed_relabel_active_fields(memory, frame, False))


def transfer_outcome_officer_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1D198..1D20A: two ordinary child slots and a true saved officer WORD."""
    frame = _city_outcome_frame_fields(memory, frame, 0x1D198)
    from ..high_level_main_flows.business_movement_support import _movement_move, _movement_compare, _movement_test_long, _movement_arithmetic_long
    from ..high_level_remaining_flows.business_city import _settlement_store_word_fields
    frame = _movement_compare(memory.state, frame, memory.table(0xFFFF8114).word(), 6, 16)
    if frame.status & 1:
        return memory.finish(frame)
    source = 0xFFFF80E0 if frame.status & 4 else 0xFFFF80E2
    frame = _movement_move(memory.state, frame, 'target_x', memory.table(source).word(), 16)
    frame = first_replace(frame, roster=memory.table(memory.table(0x00FF382C).long()).cursor(),
        candidates=memory.table(0xFFFF9000).cursor(), controller=memory.table(0xFFFFEFBE))
    frame = _movement_move(memory.state, frame, 'target_y', memory.table(0xFFFFEFC6).word(), 16)
    frame = first_replace(frame, candidates=frame.candidates.advance(s16(frame.controller.word(low16(frame.target_y)))))
    frame = _movement_compare(memory.state, frame, low16(frame.target_x), memory.table(0xFFFFF702).word(), 16)
    if not frame.status & 4:
        frame = first_replace(frame, roster=frame.candidates.cursor(), candidates=frame.roster.cursor())
    frame = _packed_save_word_fields(memory, frame, 'target_x')
    frame = _city_outcome_call_fields(memory, frame, 0x1D20A, 0x1D1DE)
    frame = _city_outcome_call_fields(memory, frame, 0x1D318, 0x1D1E2)
    frame = _packed_restore_word_fields(memory, frame, 'target_x')
    frame = _movement_compare(memory.state, frame, low16(frame.target_x), memory.table(0xFFFFF702).word(), 16)
    if not frame.status & 4:
        frame = first_replace(frame, roster=frame.candidates.cursor(), candidates=frame.roster.cursor())
    memory.table(0x00FF382C).set_long(0, frame.roster.base)
    frame = _movement_test_long(memory.state, frame, frame.roster.base)
    # This final EXG is not paired back: A1 genuinely receives the former D1.
    pointer, retained = frame.candidates.base, frame.target_y
    frame = first_replace(frame, target_y=pointer, candidates=memory.table(retained).cursor())
    frame = _movement_arithmetic_long(memory.state, frame, 'target_y', 0xFFFF9000, True)
    frame = first_replace(frame, controller=memory.table(0xFFFFEFBE))
    frame = _movement_move(memory.state, frame, 'target_x', memory.table(0xFFFFEFC6).word(), 16)
    frame = _settlement_store_word_fields(memory.state, frame, frame.controller, low16(frame.target_x), low16(frame.target_y))
    return memory.finish(frame)


def detach_member_keep_group_cursor_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1D20A..1D29E: saved D3 WORD, five saved LONGs, live packet/reference compaction."""
    frame = _city_outcome_frame_fields(memory, frame, 0x1D20A)
    from ..high_level_main_flows.business_movement_support import _movement_move, _movement_compare, _movement_adjust_word, _movement_move_long, _movement_binary_flags, _movement_compare_address
    from ..high_level_remaining_flows.business_city import _settlement_write_byte_fields, _settlement_change_header_byte_fields
    frame = _packed_save_word_fields(memory, frame, 'count')
    names = ('target_y','unit','roster','candidates','controller')
    frame, observed = _damage_save_longs(memory, frame, names)
    frame = _movement_move(memory.state, frame, 'target_y', frame.roster.byte(), 8)
    frame = _movement_move(memory.state, frame, 'target_y', low16(frame.target_y) & 15, 16)
    frame = _movement_compare(memory.state, frame, low16(frame.target_y), 1, 16)
    if not frame.status & 4:
        frame = _movement_move(memory.state, frame, 'count', 1, 16)
        frame = _movement_move(memory.state, frame, 'unit', 0, 16)
        while True:
            frame = _movement_compare(memory.state, frame, low8(frame.target_x), frame.roster.byte(low16(frame.unit), 13), 8)
            if frame.status & 4:
                break
            frame = _movement_adjust_word(memory.state, frame, 'unit', 1)
        frame = _movement_adjust_word(memory.state, frame, 'unit', 1)
        while True:
            frame = _movement_compare(memory.state, frame, low16(frame.unit), low16(frame.target_y), 16)
            if frame.status & 4:
                break
            frame = _settlement_write_byte_fields(memory.state, frame, frame.roster,
                frame.roster.byte(low16(frame.unit), 13), low16(frame.unit), 12)
            frame = _movement_adjust_word(memory.state, frame, 'unit', 1)
        frame = _city_outcome_call_fields(memory, frame, 0x1D29E, 0x1D246)
        frame = _settlement_change_header_byte_fields(memory.state, frame, frame.roster, True)
        frame = first_replace(frame, candidates=frame.roster.advance(s16(low16(frame.target_y)) + 13),
            controller=frame.roster.advance(s16(low16(frame.target_y)) + 12))
    else:
        frame = _movement_move(memory.state, frame, 'count', 14, 16)
        frame = _city_outcome_call_fields(memory, frame, 0x1D2E8, 0x1D25C)
        frame = first_replace(frame, candidates=frame.roster.advance(s16(low16(frame.target_y)) + 13),
            controller=memory.table(frame.roster.base), roster=memory.table(0).cursor())
    frame = _packed_slide_tail_fields(memory, frame, True)
    frame = _damage_restore_longs(memory, frame, names, observed)
    frame = _movement_compare_address(memory.state, frame, frame.candidates.base, frame.roster.base)
    if not frame.status & 1:
        frame = _movement_move_long(memory.state, frame, 'count', frame.count & 65535)
        frame, pointer = _movement_binary_flags(memory.state, frame, frame.candidates.base, frame.count, 32, True)
        frame = first_replace(frame, candidates=memory.table(pointer).cursor())
    return memory.finish(_packed_restore_word_fields(memory, frame, 'count'))


def replace_group_head_reference_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1D29E..1D2E8: preserved D1 WORD and the original header-blind active queue scan."""
    frame = _city_outcome_frame_fields(memory, frame, 0x1D29E)
    from ..high_level_main_flows.business_movement_support import _movement_move
    from ..high_level_remaining_flows.business_city import _settlement_write_byte_fields
    frame = _packed_save_word_fields(memory, frame, 'target_y')
    frame = _movement_move(memory.state, frame, 'target_y', frame.roster.byte(0, 13), 8)
    frame = _movement_move(memory.state, frame, 'target_y', low16(frame.target_y) & 255, 16)
    frame = first_replace(frame, candidates=memory.table(0x00FF39B2).advance(s16(memory.table(0x00FF3BB2).word())).cursor())
    frame, found = _packed_seek_reference_fields(memory, frame, 'target_x', 'candidates', False)
    if found:
        frame = _settlement_write_byte_fields(memory.state, frame, frame.candidates, low8(frame.target_y), displacement=1)
        frame = first_replace(frame, candidates=memory.table(0x00FF3000).cursor())
        frame = _packed_relabel_active_fields(memory, frame, True)
    return memory.finish(_packed_restore_word_fields(memory, frame, 'target_y'))


def remove_group_reference_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1D2E8..1D318: remove the matching pair with live two-byte-gap compaction."""
    frame = _city_outcome_frame_fields(memory, frame, 0x1D2E8)
    frame = first_replace(frame, candidates=memory.table(0x00FF39B2).advance(s16(memory.table(0x00FF3BB2).word())).cursor())
    frame, found = _packed_seek_reference_fields(memory, frame, 'target_x', 'candidates', False)
    if found:
        frame = first_replace(frame, controller=memory.table(frame.candidates.advance(2).base))
        frame = _packed_compact_reference_fields(memory, frame, True)
    return memory.finish(frame)


def attach_member_shift_packet_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1D318..1D3BC: shared insertion carry, assignment, capacity-ten original anomaly."""
    frame = _city_outcome_frame_fields(memory, frame, 0x1D318)
    from ..high_level_main_flows.business_movement_support import _movement_move, _movement_compare, _movement_move_long, _movement_test_long, _movement_binary_flags, _movement_add_word, _movement_compare_address
    from ..high_level_remaining_flows.business_city import _settlement_write_byte_fields, _settlement_change_header_byte_fields, _settlement_carry_packet_tail_fields
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, frame.controller.base)
    frame = _movement_test_long(memory.state, first_replace(frame, stack_cursor=stack), frame.controller.base)
    frame = _movement_move(memory.state, frame, 'target_y', frame.candidates.byte(), 8)
    frame = _movement_move(memory.state, frame, 'target_y', low16(frame.target_y) & 15, 16)
    frame = _movement_compare(memory.state, frame, low16(frame.target_y), 10, 16)
    if not frame.status & 4:
        offset = s16(low16(frame.target_y))
        frame = first_replace(frame, controller=frame.candidates.advance(offset + 13), scan=frame.candidates.advance(offset + 14))
        frame = _movement_move(memory.state, frame, 'target_y', frame.controller.byte(), 8)
        frame = _settlement_carry_packet_tail_fields(memory.state, frame, ('target_y','unit','count'), 'scan', 0, 8)
        frame = _movement_move(memory.state, frame, 'target_y', frame.candidates.byte(), 8)
        frame = _movement_move(memory.state, frame, 'target_y', low16(frame.target_y) & 15, 16)
        frame = _settlement_change_header_byte_fields(memory.state, frame, frame.candidates, False)
        frame = _settlement_write_byte_fields(memory.state, frame, frame.candidates, low8(frame.target_x), low16(frame.target_y), 13)
        frame = first_replace(frame, controller=memory.table(0xFFFFCC00))
        frame = _movement_move(memory.state, frame, 'count', 0, 16)
        frame = _movement_move(memory.state, frame, 'count', frame.candidates.byte(0, 4), 8)
        frame = _movement_add_word(memory.state, frame, 'count', 41)
        frame = _settlement_write_byte_fields(memory.state, frame, frame.controller, low8(frame.count), low16(frame.target_x))
        frame = _movement_move(memory.state, frame, 'count', 1, 16)
    else:
        frame = _movement_move(memory.state, frame, 'count', 0, 16)
        frame = first_replace(frame, controller=memory.table(0xFFFFCC00))
        frame = _movement_move(memory.state, frame, 'target_y', frame.controller.byte(low16(frame.target_x)), 8)
        frame = _movement_move(memory.state, frame, 'target_y', low16(frame.target_y) & 63, 16)
        frame = _movement_compare(memory.state, frame, low16(frame.target_y), 40, 16)
        high_assignment = not frame.status & 1 and not frame.status & 4
        if high_assignment:
            frame, value = _movement_binary_flags(memory.state, frame, low16(frame.target_y), 40, 16, True)
            frame = first_replace(frame, target_y=replace_word(frame.target_y, value))
        previous = frame.target_y
        frame = first_replace(frame, target_y=previous | 128)
        frame = _postbattle_bit_fields(frame, bool(previous & 128))
        memory.finish(frame)
        # Confirmed original1D38E indexes by D1, not officer D0, in the <=40 arm.
        index = low16(frame.target_x) if high_assignment else low16(frame.target_y)
        frame = _settlement_write_byte_fields(memory.state, frame, frame.controller, low8(frame.target_y), index)
    # The two paired EXGs have no DATA/CCR effects; retain their exact LONG net.
    frame = _movement_compare_address(memory.state, frame, frame.roster.base, frame.candidates.base)
    if not frame.status & 1:
        frame = _movement_move_long(memory.state, frame, 'count', frame.count & 65535)
        frame, pointer = _movement_binary_flags(memory.state, frame, frame.roster.base, frame.count, 32)
        frame = first_replace(frame, roster=memory.table(pointer).cursor())
    pointer = frame.stack_cursor.long()
    frame = first_replace(frame, controller=memory.table(pointer), stack_cursor=frame.stack_cursor.advance(4))
    return memory.finish(frame)


def _nearest_terrain_radial_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3080E already owns its saved LONGs and two seed-call slots, not1E4CA."""
    from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
    from ..high_level_battle_ai.business_geometry import rounded_deployment_radial_distance_fields
    return rounded_deployment_radial_distance_fields(BattlePolicyMemory(memory.state), frame)


def find_nearest_secondary_terrain_target_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1E464..1E4E2: nearest type6 member, live tie rule and actual D7 sentinel.

    D3/D4 hold the actor's shifted map point. D5 holds the nearest measured
    WORD, D6 the chosen member or8000, and D7 returns the actual negative
    secondary-roster terminator. Every other retained carrier and address is
    the real one supplied to or returned by the three unique child cores.
    """
    from ..high_level_battle_ai.business_formation import _first_sub_word
    from ..high_level_battle_ai.business_actions import _deployment_compare_byte
    from ..high_level_main_flows.business_movement_support import _movement_multiply_word

    frame = _city_outcome_frame_fields(memory, frame, 0x1E464)
    frame = _presentation_call_fields(memory, frame, 0x1E46A, _damage_map_fields)
    frame = first_replace(frame, candidates=memory.table(0xFFFFA5A4).cursor(),
        controller=memory.table(0xFFFFA150).cursor())
    frame = _first_word(frame, 'target_x', memory.table(0xFFFFF3F2).word())
    frame = memory.finish(_first_shift_word(frame, 'target_x', low16(frame.target_x), 2))
    frame = _first_word(frame, 'count', frame.controller.word(s16(low16(frame.target_x))))
    frame = memory.finish(_first_right_word(frame, 'count', low16(frame.count), 7))
    frame = _first_word(frame, 'distance', frame.controller.word(s16(low16(frame.target_x)), 2))
    frame = _first_right_word(frame, 'distance', low16(frame.distance), 7)
    frame = _first_word(frame, 'offset_x', 65535)
    frame = memory.finish(_first_word(frame, 'offset_y', 32768))

    while True:
        member = frame.candidates.word()
        frame = first_replace(frame, candidates=frame.candidates.advance(2))
        frame = memory.finish(_first_word(frame, 'choice', member))
        if negative_word(member):
            return frame
        frame = _first_word(frame, 'choice', member & 255)
        frame = memory.finish(_first_shift_word(frame, 'choice', low16(frame.choice), 2))
        frame = _first_word(frame, 'target_y', frame.controller.word(s16(low16(frame.choice))))
        frame = memory.finish(_first_right_word(frame, 'target_y', low16(frame.target_y), 7))
        frame = _first_word(frame, 'unit', frame.controller.word(s16(low16(frame.choice)), 2))
        frame = memory.finish(_first_right_word(frame, 'unit', low16(frame.unit), 7))

        # The terrain helper owns the sole outer1E4AA slot and its internal MOVEM.
        frame, terrain = _damage_terrain_fields(memory, frame,
            low16(frame.target_y), low16(frame.unit), 0x1E4AA)
        frame = _deployment_compare_byte(memory, frame, low8(frame.target_x), 6)
        if low8(frame.target_x) != 6:
            continue

        frame = _first_sub_word(frame, 'target_y', low16(frame.target_y), low16(frame.count))
        if frame.status & 1:
            frame = _first_sub_word(frame, 'target_y', 0, low16(frame.target_y))
        frame = _movement_multiply_word(memory.state, frame, 'target_y', low16(frame.target_y))
        frame = _first_sub_word(frame, 'unit', low16(frame.unit), low16(frame.distance))
        if frame.status & 1:
            frame = _first_sub_word(frame, 'unit', 0, low16(frame.unit))
        frame = _movement_multiply_word(memory.state, frame, 'unit', low16(frame.unit))
        frame = _first_long(frame, 'target_x', frame.target_y)
        frame = _damage_add_long(memory, frame, 'target_x', frame.unit)
        frame = _presentation_call_fields(memory, frame, 0x1E4CA, _nearest_terrain_radial_fields)
        measured, nearest = low16(frame.target_x), low16(frame.offset_x)
        frame = memory.finish(_first_compare_word(frame, measured, nearest))
        if measured > nearest:
            continue
        if measured == nearest:
            tie_bit = memory.table(0xFFFFF321).byte() & 1
            frame = memory.finish(first_replace(frame,
                status=(frame.status & 27) | (0 if tie_bit else 4)))
            if tie_bit:
                continue
        frame = _first_word(frame, 'offset_x', measured)
        frame = _first_right_word(frame, 'choice', low16(frame.choice), 2)
        frame = memory.finish(_first_word(frame, 'offset_y', low16(frame.choice)))


def upload_battlefield_tilemap_fields(memory: BattlePresentationMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """17776..177BE: live 28-by-40 tile upload with the original bit8 attributes.

    Graphics stay in the external map table. This routine retains the actual
    row/column carriers, source postincrements, WORD tile high half and LONG
    VDP command arithmetic; it does not simulate completed video hardware.
    """
    from .contexts_services import SceneRefreshMemory
    from .business_services import _scene_refresh_emit, _scene_refresh_decrement
    from ..high_level_main_flows.business_movement_support import (
        _movement_move, _movement_move_long, _movement_multiply_word,
        _movement_arithmetic_long)
    frame = _city_outcome_frame_fields(memory, frame, 0x17776)
    video = SceneRefreshMemory(memory.state)
    frame = _movement_move_long(memory.state, frame, 'unit', 0x50000003)
    frame = first_replace(frame, roster=memory.table(0x945E8).cursor())
    frame = _movement_move(memory.state, frame, 'target_x', memory.table(0xFFFFF68A).word(), 16)
    frame = _movement_multiply_word(memory.state, frame, 'target_x', 0x8C0)
    frame = first_replace(frame, roster=frame.roster.advance(frame.target_x))
    frame = _movement_move(memory.state, frame, 'target_y', 27, 16)
    while True:
        frame = _scene_refresh_emit(video, frame, 0xC00004, 4, frame.unit)
        frame = _movement_move(memory.state, frame, 'target_x', 39, 16)
        while True:
            tile = frame.roster.word()
            frame = first_replace(frame, roster=frame.roster.advance(2))
            frame = _movement_move(memory.state, frame, 'count', tile, 16)
            frame = memory.finish(first_replace(frame,
                status=(frame.status & 27) | (0 if frame.count & 256 else 4)))
            if not frame.status & 4:
                frame = _movement_move(memory.state, frame, 'count', low16(frame.count) | 0x700, 16)
            frame = _scene_refresh_emit(video, frame, 0xC00000, 2, low16(frame.count))
            frame = _scene_refresh_decrement(frame, 'target_x', low16(frame.target_x))
            if low16(frame.target_x)==65535:
                break
        frame = _movement_arithmetic_long(memory.state, frame, 'unit', 0x800000)
        frame = _scene_refresh_decrement(frame, 'target_y', low16(frame.target_y))
        if low16(frame.target_y)==65535:
            return memory.finish(frame)

def _battle_initialize_call_fields(memory, frame: FirstDeploymentFrame, target: Long, continuation: Long) -> FirstDeploymentFrame:
    from .contexts_services import SceneRefreshBoundary
    from .business_services import initialize_video_registers_and_planes_fields, clear_video_sprite_plane_fields, enqueue_sound_command_fields
    if (target,continuation) not in ((0x6826,0x17620),(0x68CE,0x17626),(0x17710,0x17664),
            (0x17776,0x17668),(0x177BE,0x1766C),(0x808A,0x17696),(0x176B6,0x176B4),
            (0x176D2,0x176CE),(0xADFC,0x1773A),(0xADFC,0x1776A),(0x8112,0x17774)):
        raise ValueError('actual battle initialization child and return token required')
    memory.frame(frame)
    entered = memory.sync_status(frame)
    if frame.stack_cursor is not None:
        stack = frame.stack_cursor.advance(-4)
        stack.set_long(0,continuation)
        entered = first_replace(frame,stack_cursor=stack)
    if target == 0x6826:
        result = initialize_video_registers_and_planes_fields(memory,entered)
    elif target == 0x68CE:
        result = clear_video_sprite_plane_fields(memory,entered)
    elif target == 0x17710:
        result = upload_battle_background_planes_fields(memory,entered)
    elif target == 0x17776:
        result = upload_battlefield_tilemap_fields(BattlePresentationMemory(memory.state),entered)
    elif target == 0x177BE:
        result = upload_battle_scene_labels_fields(memory,entered)
    elif target == 0x808A:
        result = enqueue_sound_command_fields(memory,entered,low8(entered.target_x))
    elif target == 0x176B6:
        result = compact_active_packed_group_queue_fields(memory,entered)
    elif target == 0x176D2:
        result = remove_queued_packed_group_member_fields(memory,entered)
    elif target == 0xADFC:
        from ..high_level_scene_flows.business_scene import write_vdp_dictionary_repeat_stream_fields
        result = write_vdp_dictionary_repeat_stream_fields(memory,entered)
    elif target == 0x8112:
        from .business_services import copy_video_transfer_descriptor_fields
        result = copy_video_transfer_descriptor_fields(memory,entered)
    else:
        raise SceneRefreshBoundary(target,entered,continuation)
    if frame.stack_cursor is not None:
        memory.sync_status(result)
        actual = result.stack_cursor.long()
        if actual != continuation:
            raise SceneRefreshBoundary(actual,result,continuation)
        result = first_replace(result,stack_cursor=result.stack_cursor.advance(4))
    return memory.sync_status(result)

def remove_queued_packed_group_member_fields(memory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """176D2 sole live matching records and overlapping two-byte queue drain."""
    from .contexts_services import SceneRefreshBoundary, _first_byte
    from .business_services import _scene_refresh_flags, _scene_refresh_emit
    memory.frame(frame)
    if frame.roster is None or frame.target_x is None:
        raise SceneRefreshBoundary(0x176D2,frame,None)
    frame = first_replace(frame,candidates=memory.cursor_at(0xFF3000))
    while True:
        kind = frame.candidates.byte()
        frame = first_replace(frame,candidates=frame.candidates.advance(1))
        frame = _scene_refresh_flags(memory,frame,kind,1)
        if negative_byte(kind):
            return memory.sync_status(frame)
        member = frame.candidates.byte()
        frame = first_replace(frame,candidates=frame.candidates.advance(1))
        frame = _postbattle_compare_byte_fields(frame,low8(frame.target_x),member)
        if member == low8(frame.target_x):
            break
        while True:
            token = frame.candidates.byte()
            frame = first_replace(frame,candidates=frame.candidates.advance(1))
            frame = _scene_refresh_flags(memory,frame,token,1)
            if token == 0:
                break
    marker = frame.candidates.byte(0,1)
    frame = _postbattle_compare_byte_fields(frame,marker,128)
    if marker != 128:
        return memory.sync_status(frame)
    owner = frame.candidates.byte(0,2)
    frame = _first_byte(frame,'target_y',owner)
    selected = memory.cursor_at(0xFFFFF68B).byte()
    frame = _postbattle_compare_byte_fields(frame,owner,selected)
    if owner != selected:
        return memory.sync_status(frame)
    while True:
        value = frame.roster.byte()
        frame = first_replace(frame,roster=frame.roster.advance(1))
        frame = _scene_refresh_emit(memory,frame,u32(frame.roster.base - 3),1,value)
        if value == 0:
            return memory.sync_status(frame)
        value = frame.roster.byte()
        frame = first_replace(frame,roster=frame.roster.advance(1))
        frame = _scene_refresh_emit(memory,frame,u32(frame.roster.base - 3),1,value)

def compact_active_packed_group_queue_fields(memory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """176B6 sole signed-offset active queue loop, actual child176CE return."""
    from .contexts_services import SceneRefreshBoundary, _first_byte
    from .business_services import _scene_refresh_flags
    memory.frame(frame)
    frame = first_replace(frame,roster=memory.cursor_at(0xFF39B2))
    offset = memory.cursor_at(0xFF3BB2).word()
    frame = first_replace(frame,roster=frame.roster.advance(s16(offset)))
    while True:
        kind = frame.roster.byte()
        frame = first_replace(frame,roster=frame.roster.advance(1))
        frame = _scene_refresh_flags(memory,frame,kind,1)
        if kind == 0:
            return memory.sync_status(frame)
        member = frame.roster.byte()
        frame = first_replace(frame,roster=frame.roster.advance(1))
        frame = _first_byte(frame,'target_x',member)
        if frame.target_x is None:
            raise SceneRefreshBoundary(0x176CA,frame,None)
        frame = _battle_initialize_call_fields(memory,frame,0x176D2,0x176CE)

def upload_battle_background_planes_fields(memory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """17710 complete parent structure; unknown dictionary child keeps its true slot."""
    from .contexts_services import SceneRefreshBoundary
    from .business_services import _scene_refresh_emit
    memory.frame(frame)
    if frame.stack_cursor is None or frame.target_x is None:
        raise SceneRefreshBoundary(0x17710,frame,None)
    for index,command,continuation in ((0,0x60000003,0x1773A),(4,0x40000001,0x1776A)):
        frame = _scene_refresh_emit(memory,frame,0xC00004,4,command)
        frame = first_replace(frame,controller=memory.cursor_at(0x68C14))
        source = frame.controller.long(index)
        frame = first_replace(frame,roster=memory.cursor_at(source),controller=memory.cursor_at(0x68C1C))
        destination = frame.controller.long(index)
        frame = first_replace(frame,candidates=memory.cursor_at(destination))
        frame = _first_right_word(frame,'target_x',low16(frame.target_x),1)
        frame = first_replace(frame,controller=memory.cursor_at(0x6BF06))
        count = frame.controller.word(index // 2)
        frame = _first_word(frame,'target_x',count)
        frame = _battle_initialize_call_fields(memory,frame,0xADFC,continuation)
    frame = _first_word(frame,'target_x',6)
    return _battle_initialize_call_fields(memory,frame,0x8112,0x17774)

def initialize_battle_scene_fields(memory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """17602 one real battle initialization flow; every original child stays typed."""
    from .contexts_services import SceneRefreshBoundary, _first_byte
    from .business_services import _scene_refresh_flags, _scene_refresh_emit, _scene_refresh_decrement
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x17602,frame,None)
    frame = memory.status_word(frame,0x2700)
    mode = memory.cursor_at(0xFFFFF6C4).word()
    frame = _scene_refresh_flags(memory,frame,mode,2)
    if mode == 0:
        value = memory.cursor_at(0xFFFFF314).word()
        frame = _scene_refresh_emit(memory,frame,0xFFFFF356,2,value)
        value = memory.cursor_at(0xFFFFF318).word()
        frame = _scene_refresh_emit(memory,frame,0xFFFFF354,2,value)
    frame = _battle_initialize_call_fields(memory,frame,0x6826,0x17620)
    frame = _battle_initialize_call_fields(memory,frame,0x68CE,0x17626)
    mode = memory.cursor_at(0xFFFFF6C4).word()
    frame = _scene_refresh_flags(memory,frame,mode,2)
    if mode == 0:
        memory.cursor_at(0xFFFFF6C8).word()
        frame = _scene_refresh_emit(memory,frame,0xFFFFF6C8,2,0)
        frame = first_replace(frame,roster=memory.cursor_at(0xFFFFAE28),candidates=memory.cursor_at(0xFF3BC2),
            controller=memory.cursor_at(0xFF3DC2),scan=memory.cursor_at(0xFF3CC2))
        frame = _first_word(frame,'target_x',63)
        for counter in descending_inclusive(63):
            for name,destination in (('roster',frame.roster),('candidates',frame.candidates),('controller',frame.controller),('scan',frame.scan)):
                destination.long()
                frame = first_replace(frame,**{name:destination.advance(4)})
                frame = _scene_refresh_emit(memory,frame,destination.base,4,0)
            frame = _scene_refresh_decrement(frame,'target_x',counter)
    frame = _scene_refresh_emit(memory,frame,0xC00004,2,0x8406)
    frame = _battle_initialize_call_fields(memory,frame,0x17710,0x17664)
    frame = _battle_initialize_call_fields(memory,frame,0x17776,0x17668)
    frame = _battle_initialize_call_fields(memory,frame,0x177BE,0x1766C)
    for address in (0xFFFFF312,):
        memory.cursor_at(address).word()
        frame = _scene_refresh_emit(memory,frame,address,2,0)
    frame = _scene_refresh_emit(memory,frame,0xFFFFF314,2,256)
    for address in (0xFFFFF316,0xFFFFF318):
        memory.cursor_at(address).word()
        frame = _scene_refresh_emit(memory,frame,address,2,0)
    sound = memory.cursor_at(0xFFFFF3A5).byte()
    frame = first_replace(frame,status=(frame.status & 27) | (0 if sound & 1 else 4))
    if sound & 1 == 0:
        frame = _first_byte(frame,'target_x',141)
        frame = _scene_refresh_emit(memory,frame,0xFFFFF764,1,low8(frame.target_x))
        frame = _battle_initialize_call_fields(memory,frame,0x808A,0x17696)
    frame = _scene_refresh_emit(memory,frame,0xFFFFF6C4,2,1)
    frame = first_replace(frame,roster=memory.cursor_at(0xFFFFEA37))
    city = memory.cursor_at(0xFFFFF68A).word()
    frame = _first_word(frame,'target_x',city)
    frame = _scene_refresh_emit(memory,frame,frame.roster.address(city),1,3)
    previous = memory.cursor_at(0xFFFFF3A4).word()
    frame = _scene_refresh_emit(memory,frame,0xFFFFF3A4,2,previous & 1)
    return _battle_initialize_call_fields(memory,frame,0x176B6,0x176B4)

def _battle_scene_round_call_fields(memory, frame: FirstDeploymentFrame, target: Long, continuation: Long) -> FirstDeploymentFrame:
    """Own exactly one DC0 JSR slot; dispatch only recovered typed children."""
    from .contexts_services import SceneRefreshMemory, SceneRefreshBoundary
    if (target, continuation) not in ((120186, 3532), (251476, 3548), (26662, 3554), (100518, 3572), (159156, 3624), (26662, 3634), (101120, 3640), (120216, 3648), (118844, 3680), (120130, 3706)):
        raise ValueError('original battle-round child and JSR continuation required')
    memory.frame(frame)

    def child(actual_memory, entered):
        if target == 120186:
            from ..high_level_remaining_flows.business_city import initialize_prebattle_head_bytes_fields
            return initialize_prebattle_head_bytes_fields(actual_memory.state, entered)
        if target == 251476:
            from ..high_level_scene_flows.business_objects import run_scene_object_controller_fields
            return run_scene_object_controller_fields(SceneRefreshMemory(actual_memory.state), entered)
        if target == 26662:
            from .business_services import initialize_video_registers_and_planes_fields
            return initialize_video_registers_and_planes_fields(SceneRefreshMemory(actual_memory.state), entered)
        if target == 100518:
            from .business_reuse import settle_duel_training_and_troops_fields
            return settle_duel_training_and_troops_fields(actual_memory, entered)
        if target == 101120:
            from .business_reuse import settle_duel_packets_fields
            return settle_duel_packets_fields(actual_memory, entered)
        if target == 120216:
            from ..high_level_remaining_flows.business_city import classify_duel_object_result_fields
            return classify_duel_object_result_fields(actual_memory.state, entered)
        if target == 118844:
            return settle_battle_packed_armies_fields(actual_memory, entered)
        if target == 120130:
            from ..high_level_remaining_flows.business_city import rebuild_city_links_from_primary_roster_fields
            return rebuild_city_links_from_primary_roster_fields(actual_memory.state, entered)
        if target == 159156:
            from ..high_level_scene_flows.business_duel import run_duel_scene_fields
            return run_duel_scene_fields(actual_memory.state, entered)
        raise SceneRefreshBoundary(target, entered, continuation)
    return _presentation_call_fields(BattlePresentationMemory(memory.state), frame, continuation, child)

def run_battle_scene_round_fields(memory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """DC0..E7C: sole battle/duel round control with complete live fields.

    Both original return routes share their actual 1D542 tail. Carry retry
    goes back to DCC, not to the initial head/status save at DC0.
    """
    from .contexts_services import SceneRefreshBoundary
    from ..high_level_main_flows.business_movement_support import _movement_test, _movement_compare
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0xDC0,frame,None)
    frame = memory.sync_status(frame)
    presentation = BattlePresentationMemory(memory.state)
    frame = _city_outcome_store_word_fields(presentation,frame,0xFFFFEFE0,memory.state.read(0xFFFFF6C4,2))
    frame = _battle_scene_round_call_fields(memory,frame,0x1D57A,0xDCC)
    while True:
        frame = _city_outcome_store_word_fields(presentation,frame,0xFFFFF6C4,2)
        frame = _city_outcome_store_word_fields(presentation,frame,0xFFFFF31E,0,True)
        frame = _battle_scene_round_call_fields(memory,frame,0x3D654,0xDDC)
        frame = _battle_scene_round_call_fields(memory,frame,0x6826,0xDE2)
        frame = _movement_compare(memory.state,frame,memory.state.read(0xFFFF8114,2),1,16)
        if not frame.status & 4:
            frame = _battle_scene_round_call_fields(memory,frame,0x188A6,0xDF4)
            frame = _movement_test(memory.state,frame,memory.state.read(0xFFFFEFE0,2),16)
            if not frame.status & 4:
                frame = _city_outcome_store_word_fields(presentation,frame,0xFFFFF612,0x400)
                frame = _city_outcome_store_word_fields(presentation,frame,0xFFFFF362,0,True)
                frame = _city_outcome_store_word_fields(presentation,frame,0xFFFFF352,0,True)
                frame = _city_outcome_store_word_fields(presentation,frame,0xFFFFF6C4,1)
                break
        else:
            frame = _city_outcome_store_word_fields(presentation,frame,0xFFFFF6C4,3)
            frame = _city_outcome_store_word_fields(presentation,frame,0x00FF70F4,1)
            frame = _battle_scene_round_call_fields(memory,frame,0x26DB4,0xE28)
            frame = memory.status_word(frame,0x2700)
            frame = _battle_scene_round_call_fields(memory,frame,0x6826,0xE32)
            frame = _battle_scene_round_call_fields(memory,frame,0x18B00,0xE38)
            if frame.status & 1:
                continue
            frame = _battle_scene_round_call_fields(memory,frame,0x1D598,0xE40)
            frame = _movement_test(memory.state,frame,memory.state.read(0xFFFFEFE0,2),16)
            if not frame.status & 4:
                frame = _city_outcome_store_word_fields(presentation,frame,0xFFFFF612,0x400)
                frame = _city_outcome_store_word_fields(presentation,frame,0xFFFFF362,0,True)
                frame = _city_outcome_store_word_fields(presentation,frame,0xFFFFF352,0,True)
                break
        frame = _battle_scene_round_call_fields(memory,frame,0x1D03C,0xE60)
        # E60 is immediate MOVE.W #0, not memory CLR: no fake prior read.
        frame = _city_outcome_store_word_fields(presentation,frame,0xFFFFF6C4,0)
        frame = _city_outcome_store_word_fields(presentation,frame,0xFFFFF612,0x200)
        frame = _city_outcome_store_word_fields(presentation,frame,0xFFFFF352,0,True)
        frame = _city_outcome_store_word_fields(presentation,frame,0xFFFFF764,0,True)
        break
    return _battle_scene_round_call_fields(memory,frame,0x1D542,0xE7A)
