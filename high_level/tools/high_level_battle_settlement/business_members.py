"""Live member movement, packed-object repair, and queue consistency rules.

These are semantic rules, not CPU entry points.  Identifiers retain complete
WORD width; the compatibility layer owns signed addressing and continuation
storage.  ``RemovalOutcome`` distinguishes removal from an ordinary return.
"""
from .domain import BattleState, Table, Word, Long, RemovalOutcome, u16, low8, low16, replace_byte, mask_byte, zero_extend_word, add_low_word, divu_retained, negative_byte, negative_word, descending_inclusive, uint
from .contexts_settlement import PackedTailRepair

def remove_member(state: BattleState, officer: Word, object_view: Table, owner: Word, count: Word) -> RemovalOutcome:
    award, officer, owner = detach_assignment_and_read_removal_award(state, officer, owner)
    copy_source, object_view, count = compact_removed_member_entry(state, object_view, officer, count)
    slide_removed_packed_tail(copy_source, object_view, count)
    return finish_removal(state, award)

def finish_removal(state: BattleState, award: Long) -> RemovalOutcome:
    officer = state.first_marker()
    queue = state.pair_queue()
    queue = queue.at(state.pair_queue_offset())
    if not negative_word(state.second_marker()):
        while True:
            if queue.next_byte() == 0:
                return state.member_removed(award)
            if low8(officer) != queue.next_byte():
                continue
            break
        queue.write_relative(-1, state.second_marker_tail())
        queue = state.active_queue()
        while True:
            if negative_byte(queue.next_byte()):
                continue
            if low8(officer) == queue.next_byte():
                break
            while queue.next_byte() != 0:
                pass
        queue.write_relative(-1, state.second_marker_tail())
    else:
        while True:
            if queue.next_byte() == 0:
                return state.member_removed(award)
            if low8(officer) != queue.next_byte():
                continue
            break
        while True:
            if queue.copy_next_byte_relative(-3) == 0:
                return state.member_removed(award)
            queue.copy_next_byte_relative(-3)
    return state.member_removed(award)

def transfer_attacker(state: BattleState) -> None:
    selector = read_attacker_transfer_leader(state)
    if selector == state.attacker_officer():
        return
    destination, source, selector = read_attacker_transfer_lists(state)
    if transfer_destination_is_full(selector):
        return
    troops, doubled_officer, remaining = read_attacker_transfer_troops(state)
    if transfer_troops_are_empty(remaining):
        return
    if transfer_troops_exceed_window(remaining):
        return
    transfer_members(state, destination, source, selector, doubled_officer, remaining)

def transfer_defender(state: BattleState) -> None:
    selector = read_defender_transfer_leader(state)
    if selector == state.attacker_officer():
        return
    destination, source, selector = read_defender_transfer_lists(state)
    if transfer_destination_is_full(selector):
        return
    troops, doubled_officer, remaining = read_defender_transfer_troops(state)
    if transfer_troops_are_empty(remaining):
        return
    if transfer_troops_exceed_window(remaining):
        return
    transfer_members(state, destination, source, selector, doubled_officer, remaining)

def transfer_members(state: BattleState, destination: Table, source: Table, count: Word, doubled_officer: Word, carry: Word) -> None:
    officer, carry = insert_transfer_member_and_shift_tail(destination, count, doubled_officer, carry)
    source = source.adjust_after_insertion(destination)
    tail = detach_transferred_member_from_source(state, source, officer, carry)
    slide_transferred_packed_tail(tail.copy_source, tail.copy_target, tail.remaining_count)
    attributes = refresh_transfer_destination_average(state, destination, count)
    if tail.deleted == 0:
        refresh_transfer_source_average(state, source, count, attributes)
    sync_queues(state, tail.deleted)

def sync_queues(state: BattleState, deleted: Word) -> None:
    officer = state.second_marker()
    if officer == state.first_marker():
        return
    queue = state.pair_queue()
    queue = queue.at(state.pair_queue_offset())
    if deleted == 0:
        while True:
            if queue.next_byte() == 0:
                return
            if low8(officer) != queue.next_byte():
                continue
            break
        queue.write_relative(-1, state.first_marker_tail())
        queue = state.active_queue()
        while True:
            if negative_byte(queue.next_byte()):
                return
            if low8(officer) == queue.next_byte():
                break
            while queue.next_byte() != 0:
                pass
        queue.write_relative(-1, state.first_marker_tail())
    else:
        while True:
            if queue.next_byte() == 0:
                return
            if low8(officer) != queue.next_byte():
                continue
            break
        while True:
            if queue.copy_next_byte_relative(-3) == 0:
                return
            queue.copy_next_byte_relative(-3)

def detach_assignment_and_read_removal_award(state: BattleState, officer: Word, owner: Word) -> tuple[Long, Word, Word]:
    state.set_first_marker(officer)
    capacity = state.capacity_parameters
    assignments = state.assignments
    owner = replace_byte(owner, assignments.byte(officer))
    assignments.set_byte(officer, 255)
    officer = u16(officer << 1)
    award = capacity.word(officer)
    award = zero_extend_word(award)
    award = divu_retained(award, 5)
    officer = u16(officer >> 1)
    owners = state.city_owners
    owner = replace_byte(owner, owners.byte(owner))
    owner = u16(owner & 255)
    owner = u16(owner << 1)
    leaders = state.force_leaders
    if officer == leaders.word(owner):
        award = add_low_word(award, 30)
    officer_flags = state.officer_flags
    if officer_flags.byte(officer) & 16:
        award = add_low_word(award, 20)
    return (award, officer, owner)

def compact_removed_member_entry(state: BattleState, object_view: Table, officer: Word, count: Word) -> tuple[Table, Table, Word]:
    count = replace_byte(count, object_view.byte())
    count = mask_byte(count, 15)
    if count != 1:
        member_index = u16(0)
        while True:
            count = u16(count - 1)
            if low8(officer) == object_view.byte(member_index, 13):
                break
            member_index = u16(member_index + 1)
        while True:
            count = u16(count - 1)
            if negative_word(count):
                break
            object_view.set_byte(member_index, object_view.byte(member_index, 14), 13)
            member_index = u16(member_index + 1)
        count = replace_byte(count, object_view.byte())
        count = mask_byte(count, 15)
        object_view.change_byte(-1)
        state.set_second_marker_header(0)
        state.set_second_marker_tail(object_view.byte(0, 13))
        copy_source = object_view.at(count, 13)
        object_view = object_view.at(count, 12)
    else:
        state.set_second_marker(65535)
        copy_source = object_view.at(count, 13)
    return (copy_source, object_view, count)

def slide_removed_packed_tail(copy_source: Table, object_view: Table, count: Word) -> None:
    while True:
        count = replace_byte(count, copy_source.byte())
        count = u16(count & 15)
        if count == 0:
            break
        count = u16(count + 12)
        for count in descending_inclusive(count):
            copy_source.copy_next_byte(object_view)
    object_view.set_byte(0, 0)

def transfer_destination_is_full(selector: Word) -> bool:
    uint(selector, 16)
    return selector >= 10

def transfer_troops_are_empty(remaining: Word) -> bool:
    uint(remaining, 16)
    return remaining == 0

def transfer_troops_exceed_window(remaining: Word) -> bool:
    uint(remaining, 16)
    return remaining >= 25

def read_attacker_transfer_leader(state: BattleState) -> Word:
    assignments = state.assignments
    selector = state.attacker_officer()
    selector = replace_byte(selector, assignments.byte(selector))
    selector = u16(selector & 63)
    owners = state.city_owners
    selector = replace_byte(selector, owners.byte(selector))
    selector = u16(selector << 1)
    leaders = state.force_leaders
    selector = leaders.word(selector)
    return selector

def read_attacker_transfer_lists(state: BattleState) -> tuple[Table, Table, Word]:
    destination = Table(state, state.opposing_object())
    source = state.packed_entities
    offsets = state.packed_offsets
    selector = state.object_index()
    source = source.at(offsets.word(selector))
    selector = replace_byte(selector, destination.byte())
    selector = u16(selector & 15)
    return (destination, source, selector)

def read_attacker_transfer_troops(state: BattleState) -> tuple[Table, Word, Word]:
    troops = state.troops
    doubled_officer = state.attacker_officer()
    doubled_officer = u16(doubled_officer << 1)
    remaining = troops.word(doubled_officer)
    return (troops, doubled_officer, remaining)

def read_defender_transfer_leader(state: BattleState) -> Word:
    assignments = state.assignments
    selector = state.defender_officer()
    selector = replace_byte(selector, assignments.byte(selector))
    selector = u16(selector & 63)
    owners = state.city_owners
    selector = replace_byte(selector, owners.byte(selector))
    selector = u16(selector << 1)
    leaders = state.force_leaders
    selector = leaders.word(selector)
    return selector

def read_defender_transfer_lists(state: BattleState) -> tuple[Table, Table, Word]:
    destination = state.packed_entities
    offsets = state.packed_offsets
    selector = state.object_index()
    destination = destination.at(offsets.word(selector))
    source = Table(state, state.opposing_object())
    selector = replace_byte(selector, destination.byte())
    selector = u16(selector & 15)
    return (destination, source, selector)

def read_defender_transfer_troops(state: BattleState) -> tuple[Table, Word, Word]:
    troops = state.troops
    doubled_officer = state.defender_officer()
    doubled_officer = u16(doubled_officer << 1)
    remaining = troops.word(doubled_officer)
    return (troops, doubled_officer, remaining)

def insert_transfer_member_and_shift_tail(destination: Table, count: Word, doubled_officer: Word, carry: Word) -> tuple[Word, Word]:
    officer = u16(doubled_officer >> 1)
    insertion = destination.at(count, 13)
    carry = replace_byte(carry, insertion.byte())
    while True:
        record_size = u16(carry)
        record_size = u16(record_size & 15)
        if record_size == 0:
            break
        record_size = u16(record_size + 12)
        for record_size in descending_inclusive(record_size):
            saved_byte = insertion.byte(0, 1)
            insertion.set_byte(0, low8(carry), 1)
            carry = replace_byte(carry, saved_byte)
            insertion = insertion.advance(1)
    insertion.set_byte(0, 0, 1)
    destination.set_byte(count, low8(officer), 13)
    destination.change_byte(1)
    return (officer, carry)

def detach_transferred_member_from_source(state: BattleState, source: Table, officer: Word, carry: Word) -> PackedTailRepair:
    deleted = u16(0)
    state.set_second_marker(0)
    state.set_second_marker_tail(source.byte(0, 13))
    remaining_count = replace_byte(carry, source.byte())
    remaining_count = u16(remaining_count & 15)
    if remaining_count != 1:
        search_index = u16(0)
        while True:
            remaining_count = u16(remaining_count - 1)
            if low8(officer) == source.byte(search_index, 13):
                break
            search_index = u16(search_index + 1)
        while True:
            remaining_count = u16(remaining_count - 1)
            if negative_word(remaining_count):
                break
            source.set_byte(search_index, source.byte(search_index, 14), 13)
        state.set_first_marker(0)
        state.set_first_marker_tail(source.byte(0, 13))
        remaining_count = replace_byte(remaining_count, source.byte())
        remaining_count = u16(remaining_count & 15)
        copy_source = source.at(remaining_count, 13)
        copy_target = source.at(remaining_count, 12)
        source.change_byte(-1)
    else:
        copy_source = source.at(remaining_count, 13)
        copy_target = source.at()
        deleted = u16(1)
        state.set_first_marker(65535)
    return PackedTailRepair(deleted, copy_source, copy_target, remaining_count)

def slide_transferred_packed_tail(copy_source: Table, copy_target: Table, remaining_count: Word) -> None:
    while True:
        remaining_count = replace_byte(remaining_count, copy_source.byte())
        remaining_count = u16(remaining_count & 15)
        if remaining_count == 0:
            break
        remaining_count = u16(remaining_count + 12)
        for remaining_count in descending_inclusive(remaining_count):
            copy_source.copy_next_byte(copy_target)
    copy_target.set_byte(0, 0)

def refresh_transfer_destination_average(state: BattleState, destination: Table, count: Word) -> Table:
    count = replace_byte(count, destination.byte())
    count = u16(count & 15)
    attributes = state.average_attributes
    average_index = u16(count)
    average_index = u16(average_index - 1)
    attribute = u16(0)
    total = u16(0)
    for average_index in descending_inclusive(average_index):
        attribute = replace_byte(attribute, destination.byte(average_index, 13))
        attribute = replace_byte(attribute, attributes.byte(attribute))
        total = u16(total + attribute)
    total = zero_extend_word(total)
    total = divu_retained(total, count)
    destination.set_byte(0, low8(total), 3)
    return attributes

def refresh_transfer_source_average(state: BattleState, source: Table, count: Word, attributes: Table) -> None:
    count = replace_byte(count, source.byte())
    count = u16(count & 15)
    average_index = u16(count)
    average_index = u16(average_index - 1)
    attribute = u16(0)
    total = u16(0)
    for average_index in descending_inclusive(average_index):
        attribute = replace_byte(attribute, source.byte(average_index, 13))
        attribute = replace_byte(attribute, attributes.byte(attribute))
        total = u16(total + attribute)
    total = zero_extend_word(total)
    total = divu_retained(total, count)
    source.set_byte(0, low8(total), 3)
