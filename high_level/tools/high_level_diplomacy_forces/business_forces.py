"""Live force reassignment, disbanding and packed/queued state cleanup.

Roles are probable; exact ordering, widths and unusual aliases are the original
compatibility contract. No natural force/city catalog or complete CPU is implied.
"""
from .domain import (GameState, Table, Word, uint, u16, u32, low8, low16, high16,
                     replace_byte, replace_word, negative_byte, negative_word,
                     descending_inclusive, divu_retained)
from .business_shared import choose_city_head


def resolve_force_reassignment(state: GameState) -> None:
    leaders = state.force_heads
    owners = state.city_owners
    assignments = state.officer_assignments
    statuses = state.officer_status
    change = state.pending_force_change()
    if not negative_word(change):
        new_force = u16(low8(change))
        old_force = u16(change >> 8)
        if old_force == state.removed_force():
            state.set_loyalty_source(leaders.word(u16(new_force << 1)))
            threshold = u16(50)
            city = u16(56)
            while True:
                if low8(old_force) == owners.byte(city):
                    reassign_city_officers(state, city, threshold, new_force, owners, assignments, statuses)
                    reduce_city_reserve(state, city, owners)
                    return_temporary_city_assignments(state, city)
                    clear_disbanded_city_orders(state, old_force)
                city = u16(city - 1)
                if city == 0:
                    break
            remove_force_group_packets(state, old_force, 0, assignments)
        else:
            state.set_loyalty_source(leaders.word(u16(old_force << 1)))
            threshold = u16(90)
            city = u16(56)
            while True:
                if low8(new_force) == owners.byte(city):
                    reassign_city_officers(state, city, threshold, old_force, owners, assignments, statuses)
                    reduce_city_reserve(state, city, owners)
                    return_temporary_city_assignments(state, city)
                    clear_disbanded_city_orders(state, old_force)
                city = u16(city - 1)
                if city == 0:
                    break
            remove_force_group_packets(state, new_force, 0, assignments)
    else:
        owners = state.other_city_owners
        heads = state.other_city_heads
        force = state.removed_force()
        for index in descending_inclusive(55):
            if owners.byte(index) == low8(force):
                if index < 40:
                    owners.set_byte(index, 255)
                    heads.set_word(u16(index << 1), 65535)
                mark_city_assignments_inactive(state, index)
                clear_disbanded_temporary_assignments(state, index)
                clear_disbanded_city_orders(state, index)
        disband_force_group_packets(state)
    state.force_heads.set_word(u16(state.removed_force() << 1), 65535)
    state.set_pending_force_change(0)
    state.set_route(524)


def reassign_city_officers(state: GameState, city: Word, status_threshold: Word,
                          new_force: Word, owners: Table, assignments: Table,
                          statuses: Table) -> None:
    city = uint(city, 16)
    status_threshold = uint(status_threshold, 16)
    new_force = uint(new_force, 16)
    owners = state.checked_table(owners)
    assignments = state.checked_table(assignments)
    statuses = state.checked_table(statuses)
    if city >= 41:
        return
    roster = state.candidate_roster.cursor()
    heads = state.city_heads
    count = u16(0)
    for officer in descending_inclusive(255):
        if assignments.byte(officer) == low8(city):
            if statuses.byte(officer) < low8(status_threshold):
                roster.append_word(officer)
                state.set_selected_officer(officer)
                state.apply_returning_officer_loyalty()
                count = u16(count + 1)
            else:
                assignments.set_byte(officer, assignments.byte(officer) | 128)
    roster.set_word(0, 65535)
    if count != 0:
        owners.set_byte(city, low8(new_force))
        choose_city_head(state, city)
        clear_transferred_city_orders(state, city)
    else:
        owners.set_byte(city, 255)
        heads.set_word(u16(city << 1), 65535)
        clear_transferred_city_orders(state, city)


def clear_transferred_city_orders(state: GameState, city: Word) -> None:
    city = uint(city, 16)
    if city >= 41:
        return
    index = u16(u16((city << 1) + city) << 2)
    orders = state.city_orders
    flags = state.officer_flags
    for displacement in (0, 4, 8):
        officer = orders.word(index, displacement)
        if not negative_word(officer):
            flags.set_byte(officer, 0)
            orders.set_word(index, 65535, displacement)


def remove_force_group_packets(state: GameState, force: Word, retained_stride: Word,
                               assignments: Table) -> None:
    force = uint(force, 16)
    retained_stride = uint(retained_stride, 16)
    assignments = state.checked_table(assignments)
    packet = state.packed_groups
    while True:
        retained_stride = u16(replace_byte(retained_stride, packet.byte() & 15))
        if low8(retained_stride) == 0:
            return
        if packet.byte(0, 4) == low8(force):
            remaining = u16(retained_stride - 1)
            for member in descending_inclusive(remaining):
                officer = u16(packet.byte(member, 13))
                assignments.set_byte(officer, assignments.byte(officer) | 128)
                assignments.set_byte(officer, assignments.byte(officer) & 191)
            remove_packet_pair_reference(state, packet)
            compact_following_packets(state, packet, retained_stride)
        else:
            packet = packet.at(retained_stride, 13)


def compact_following_packets(state: GameState, packet: Table, retained_stride: Word) -> None:
    retained_stride = uint(retained_stride, 16)
    packet = state.checked_table(packet)
    source = packet.at(retained_stride, 13).cursor()
    destination = packet.cursor()
    while True:
        count = u16(source.byte() & 15)
        if count == 0:
            break
        count = u16(count + 12)
        for remaining in descending_inclusive(count):
            destination.append_byte(source.next_byte())
    destination.set_byte(0, 0)


def remove_packet_pair_reference(state: GameState, packet: Table) -> None:
    packet = state.checked_table(packet)
    head = u16(packet.byte(0, 13))
    pairs = state.pair_references.at(state.pair_reference_offset())
    while pairs.byte() != 0:
        if pairs.byte(0, 1) == low8(head):
            source = pairs.at(0, 2).cursor()
            destination = pairs.cursor()
            while True:
                value = source.next_byte()
                destination.append_byte(value)
                if value == 0:
                    return
                destination.append_byte(source.next_byte())
        pairs = pairs.advance(2)


def reduce_city_reserve(state: GameState, city: Word, owners: Table) -> None:
    city = uint(city, 16)
    owners = state.checked_table(owners)
    if city >= 41:
        return
    if negative_byte(owners.byte(city)):
        return
    sample = u32(state.sample_random() & 65535)
    rate = u16(high16(u32(sample * 21)) + 10)
    reserves = state.city_reserves
    index = u16(city << 2)
    reserve = reserves.long(index)
    product = u32(low16(reserve) * low16(rate))
    quotient = divu_retained(product, 100)
    reserve = replace_word(reserve, u16(low16(reserve) - low16(quotient)))
    reserves.set_long(index, reserve)


def return_temporary_city_assignments(state: GameState, city: Word) -> None:
    city = uint(city, 16)
    assignments = state.officer_assignments
    alternate = state.alternate_assignments
    processed = state.city_processed
    temporary = state.temporary_city_flags
    mask = state.temporary_city_bits
    expected = u16(replace_byte(city, low8(city) | 64))
    for officer in descending_inclusive(255):
        value = u16(assignments.byte(officer))
        if low8(value) != low8(expected):
            value = u16(value & 63)
            if value < 41:
                continue
            value = u16(value | 64)
            if low8(value) != low8(expected):
                continue
        value = u16(alternate.byte(officer))
        if value == 0:
            continue
        value = u16(value & 63)
        assignments.set_byte(officer, low8(value | 128))
        alternate.set_byte(officer, 0)
        processed.set_byte(value, 0)
        temporary.set_byte(value, 0)
        slot = u16(value - 1)
        bit = slot & 7
        mask_index = u16(slot >> 3)
        mask.set_byte(mask_index, mask.byte(mask_index) & (255 ^ (1 << bit)))
        remove_officer_pair_reference(state, officer)


def remove_officer_pair_reference(state: GameState, officer: Word) -> None:
    officer = uint(officer, 16)
    source = state.pair_references.at(state.pair_reference_offset()).cursor()
    while source.next_byte() != 0:
        if source.next_byte() != low8(officer):
            continue
        while True:
            value = source.next_byte()
            source.set_byte(0, value, -3)
            if value == 0:
                return
            value = source.next_byte()
            source.set_byte(0, value, -3)


def mark_city_assignments_inactive(state: GameState, index: Word) -> None:
    index = uint(index, 16)
    city = u16(index + 1)
    assignments = state.officer_assignments.cursor()
    for officer in descending_inclusive(255):
        if assignments.next_byte() == low8(city):
            assignments.set_byte(0, assignments.byte(0, -1) | 128, -1)


def disband_force_group_packets(state: GameState) -> None:
    packet = state.packed_groups
    assignments = state.officer_assignments
    force = state.removed_force()
    while True:
        count = u16(packet.byte() & 15)
        if count == 0:
            return
        if packet.byte(0, 4) != low8(force):
            packet = packet.at(count, 13)
            continue
        for member in descending_inclusive(u16(count - 1)):
            officer = u16(packet.byte(member, 13))
            value = u16(assignments.byte(officer) & 63)
            if value != 0:
                value = u16(value | 128)
            else:
                value = u16(replace_byte(value, 129))
            assignments.set_byte(officer, low8(value))
        remove_disbanded_packet_reference(state, packet)
        source = packet.at(count, 13).cursor()
        destination = packet.cursor()
        while True:
            following_count = u16(source.byte() & 15)
            if following_count == 0:
                break
            for remaining in descending_inclusive(u16(following_count + 12)):
                destination.append_byte(source.next_byte())
        destination.set_byte(0, 0)


def remove_disbanded_packet_reference(state: GameState, packet: Table) -> None:
    packet = state.checked_table(packet)
    pairs = state.pair_references.at(state.pair_reference_offset())
    head = packet.byte(0, 13)
    while pairs.byte() != 0:
        if pairs.byte(0, 1) == head:
            source = pairs.at(0, 2).cursor()
            destination = pairs.cursor()
            while True:
                value = source.next_byte()
                destination.append_byte(value)
                if value == 0:
                    return
                destination.append_byte(source.next_byte())
        pairs = pairs.advance(2)


def clear_disbanded_temporary_assignments(state: GameState, index: Word) -> None:
    index = uint(index, 16)
    expected = u16(u16(index + 1) | 64)
    assignments = state.officer_assignments
    alternate = state.alternate_assignments
    processed = state.city_processed
    temporary = state.temporary_city_flags
    mask = state.temporary_city_bits
    for officer in descending_inclusive(255):
        value = u16(assignments.byte(officer))
        if not value & 64:
            if low8(value) < 41:
                continue
            value = u16(value | 64)
        if low8(value) != low8(expected):
            continue
        value = u16(alternate.byte(officer))
        if value == 0:
            continue
        value = u16(value & 63)
        processed.set_byte(value, 0)
        alternate.set_byte(officer, 0)
        temporary.set_byte(value, 0)
        assignments.set_byte(officer, low8(value | 128))
        slot = u16(value - 1)
        bit = slot & 7
        mask_index = u16(slot >> 3)
        mask.set_byte(mask_index, mask.byte(mask_index) & (255 ^ (1 << bit)))


def clear_disbanded_city_orders(state: GameState, index: Word) -> None:
    index = uint(index, 16)
    if index >= 40:
        return
    clear_city_queue_principals(state, index)
    offset = u16(u16((index << 1) + index) << 2)
    orders = state.other_city_orders
    flags = state.officer_flags
    for displacement in (0, 4, 8):
        officer = orders.word(offset, displacement)
        if not negative_word(officer):
            flags.set_byte(officer, 0)
            orders.set_word(offset, 65535, displacement)


def clear_city_queue_principals(state: GameState, index: Word) -> None:
    index = uint(index, 16)
    principals = state.queue_principals
    principals.set_long(u16(index << 2), 0)
    queue = state.force_queue
    slot = u16(0)
    while True:
        if queue.byte() == low8(index):
            other = u16(queue.byte(0, 1))
            principals.set_long(u16(other << 2), 0)
            mask = state.force_queue_mask()
            state.set_force_queue_mask(u16(mask & ~(1 << (slot & 31))))
            queue.set_long(0, 0)
        queue = queue.advance(4)
        slot = u16(slot + 1)
        if slot >= 16:
            break
