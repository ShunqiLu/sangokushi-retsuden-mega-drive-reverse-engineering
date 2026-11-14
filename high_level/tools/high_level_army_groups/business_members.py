"""Live packed-army member removal, transfer and reference maintenance.

Packet headers and reference lists are read in their original order, not decoded
into immutable groups.  Returned contexts carry the surviving logical views;
the compatibility backend separately preserves real save/restore stack effects.
"""
from .domain import (
    GameState, GroupContext, Table, Word, checked_context, checked_table, descending_inclusive,
    low8, negative_byte, negative_word, u8, u16, u32,
)
from .business_arrival import settle_group_at_city, adjust_battle_losing_loyalty


def settle_battle_packed_armies(state: GameState) -> None:
    transfer_outcome_officer(state)
    selected = state.table(state.selected_group_pointer())
    other = state.group_packets.at(state.group_offsets.word(state.selected_group_offset()))
    context = GroupContext(selected, other)
    officer = state.primary_officer()
    if state.troops.word(u16(officer << 1)) == 0:
        officer = state.primary_officer()
        context = remove_defeated_packed_member(state, officer, context)
        state.set_selected_group_pointer(0)
    context = GroupContext(context.target, context.source)
    officer = state.secondary_officer()
    if state.troops.word(u16(officer << 1)) == 0:
        officer = state.secondary_officer()
        context = remove_defeated_packed_member(state, officer, context)
        state.set_selected_group_pointer(context.target.address())
    settle_group_at_city(state)
    adjust_battle_losing_loyalty(state)


def remove_defeated_packed_member(state: GameState, officer: Word, context: GroupContext) -> GroupContext:
    officer = u16(officer)
    context = checked_context(context, state)
    group = context.source
    state.officer_assignments.set_byte(officer, 255)
    old_head = group.byte(13)
    count = group.byte() & 15
    if count == 1:
        new_head = 65535
        removed_bytes = 14
        tail = group.at(count, 13).cursor()
        destination = group.cursor()
    else:
        group.set_byte(0, u8(group.byte() - 1))
        index = 0
        removed_bytes = 1
        while group.byte(index, 13) != low8(officer):
            index = u16(index + 1)
        while True:
            index = u16(index + 1)
            if index == count:
                break
            group.set_byte(index, group.byte(index, 13), 12)
        tail = group.at(count, 13).cursor()
        destination = group.at(count, 12).cursor()
        new_head = group.byte(13)
    while True:
        following_count = tail.byte() & 15
        if following_count == 0:
            destination.set_byte(0, 0)
            break
        for copied in descending_inclusive(u16(following_count + 12)):
            destination.append_byte(tail.next_byte())
    replace_or_remove_group_references(state, old_head, new_head)
    other = context.target
    if other.address() >= group.address():
        other = other.advance(-removed_bytes)
    return GroupContext(group, other)


def replace_or_remove_group_references(state: GameState, old_head: Word, new_head: Word) -> None:
    old_head = u16(old_head)
    new_head = u16(new_head)
    if new_head == old_head:
        return None
    pairs = state.pair_references.at(state.pair_reference_offset()).cursor()
    while True:
        if pairs.next_byte() == 0:
            return None
        if pairs.next_byte() == low8(old_head):
            break
    if negative_word(new_head):
        destination = pairs.advance(-2).cursor()
        while True:
            value = pairs.next_byte()
            destination.append_byte(value)
            if value == 0:
                return None
            destination.append_byte(pairs.next_byte())
    pairs.set_byte(65535, low8(new_head))
    records = state.head_records.cursor()
    while True:
        if negative_byte(records.next_byte()):
            return None
        if records.next_byte() == low8(old_head):
            records.set_byte(65535, low8(new_head))
            return None
        while records.next_byte() != 0:
            pass


def transfer_outcome_officer(state: GameState) -> None:
    outcome = state.outcome()
    if outcome < 6:
        return None
    if outcome == 6:
        officer = state.winning_officer()
    else:
        officer = state.losing_officer()
    source = state.table(state.selected_group_pointer())
    target = state.group_packets.at(state.group_offsets.word(state.selected_group_offset()))
    if officer != state.primary_officer():
        source, target = target, source
    context = detach_member_keep_group_cursor(state, officer, GroupContext(source, target))
    context = attach_member_shift_packet(state, officer, context)
    if officer != state.primary_officer():
        context = GroupContext(context.target, context.source)
    state.set_selected_group_pointer(context.source.address())
    relative = u32(context.target.address() - state.group_packets.address())
    state.group_offsets.set_word(state.selected_group_offset(), u16(relative))


def detach_member_keep_group_cursor(state: GameState, officer: Word, context: GroupContext) -> GroupContext:
    officer = u16(officer)
    context = checked_context(context, state)
    group = context.source
    count = group.byte() & 15
    if count == 1:
        removed_bytes = 14
        remove_group_reference(state, officer)
        tail = group.at(count, 13).cursor()
        destination = group.cursor()
    else:
        removed_bytes = 1
        index = 0
        while group.byte(index, 13) != low8(officer):
            index = u16(index + 1)
        index = u16(index + 1)
        while index != count:
            group.set_byte(index, group.byte(index, 13), 12)
            index = u16(index + 1)
        replace_group_head_reference(state, officer, group)
        group.set_byte(0, u8(group.byte() - 1))
        tail = group.at(count, 13).cursor()
        destination = group.at(count, 12).cursor()
    while True:
        following_count = tail.byte() & 15
        if following_count == 0:
            destination.set_byte(0, 0)
            break
        for copied in descending_inclusive(u16(following_count + 12)):
            destination.append_byte(tail.next_byte())
    other = context.target
    if other.address() >= group.address():
        other = other.advance(-removed_bytes)
    return GroupContext(group, other)


def replace_group_head_reference(state: GameState, officer: Word, group: Table) -> None:
    officer = u16(officer)
    group = checked_table(group, state)
    replacement = group.byte(13)
    pairs = state.pair_references.at(state.pair_reference_offset())
    while pairs.byte() != 0:
        if pairs.byte(0, 1) == low8(officer):
            break
        pairs = pairs.advance(2)
    else:
        return None
    pairs.set_byte(0, replacement, 1)
    records = state.head_records.cursor()
    while records.byte(0, 1) != low8(officer):
        records = records.advance(1).cursor()
        while records.next_byte() != 0:
            pass
    records.set_byte(0, replacement, 1)


def remove_group_reference(state: GameState, officer: Word) -> None:
    officer = u16(officer)
    pairs = state.pair_references.at(state.pair_reference_offset())
    while pairs.byte() != 0:
        if pairs.byte(0, 1) == low8(officer):
            break
        pairs = pairs.advance(2)
    else:
        return None
    source = pairs.advance(2).cursor()
    destination = pairs.cursor()
    while True:
        value = source.next_byte()
        destination.append_byte(value)
        if value == 0:
            return None
        destination.append_byte(source.next_byte())


def attach_member_shift_packet(state: GameState, officer: Word, context: GroupContext) -> GroupContext:
    officer = u16(officer)
    context = checked_context(context, state)
    target = context.target
    count = target.byte() & 15
    if count == 10:
        added_bytes = 0
        assignment = state.officer_assignments.byte(officer) & 63
        if assignment <= 40:
            assignment = u16(assignment | 128)
            state.officer_assignments.set_byte(assignment, low8(assignment))
        else:
            assignment = u16(assignment - 40)
            assignment = u16(assignment | 128)
            state.officer_assignments.set_byte(officer, low8(assignment))
    else:
        tail = target.at(count, 13)
        destination = target.at(count, 14).cursor()
        carried = tail.byte()
        while True:
            following_count = carried & 15
            if following_count == 0:
                destination.set_byte(0, 0)
                break
            for copied in descending_inclusive(u16(following_count + 12)):
                displaced = destination.byte()
                destination.append_byte(carried)
                carried = displaced
        count = target.byte() & 15
        target.set_byte(0, u8(target.byte() + 1))
        target.set_byte(count, low8(officer), 13)
        assignment = u16(target.byte(4) + 41)
        state.officer_assignments.set_byte(officer, low8(assignment))
        added_bytes = 1
    source = context.source
    if source.address() >= target.address():
        source = source.advance(added_bytes)
    return GroupContext(source, target)
