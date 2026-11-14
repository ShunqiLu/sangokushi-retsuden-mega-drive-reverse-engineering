"""Ordered city ledgers, resource packets, relationships and transport.

These operations deliberately retain WORD wrapping, signed indexed addresses,
live re-reads and the original distinction between overflow saturation and
wrapped-then-capped credit.  Natural selector domains are not inferred here.
"""
from .domain import (
    CarryOutcome, GameState, Table, Word, descending_inclusive, low8,
    negative_byte, replace_byte, u8, u16, u32,
)


def commit_tax_rate(state: GameState) -> None:
    orders = state.city_tax_orders
    city = u16(state.chosen_city() << 2)
    orders.set_word(city, 0)
    orders.set_word(city, state.tax_rate(), 2)


def debit_city_gold(state: GameState) -> None:
    city = u16(state.chosen_city() << 2)
    gold = state.city_gold
    amount = state.order_amount()
    gold.set_long(city, u32(gold.long(city) - amount))


def schedule_transport_debit(state: GameState) -> None:
    city = u16(state.selected_city() << 2)
    orders = state.transport_orders
    kind = u16(state.transport_choice() + 1)
    orders.set_byte(city, low8(kind) | 16)
    coordinates = state.city_coordinates
    selected = u16(state.selected_city() << 2)
    y = u16(coordinates.word(selected, 2) >> 4)
    orders.set_byte(city, low8(y), 1)
    x = u16(coordinates.word(selected) >> 4)
    orders.set_byte(city, low8(x), 2)
    orders.set_byte(city, state.chosen_city_tail(), 3)
    selected = u16(state.selected_city() << 2)
    gold = state.city_gold
    rice = state.city_rice
    choice = u16(state.transport_choice() << 3)
    costs = state.transport_costs
    remaining = gold.long(selected)
    remaining = u32(remaining - costs.long(choice))
    gold.set_long(selected, remaining)
    remaining = rice.long(selected)
    remaining = u32(remaining - costs.long(choice, 4))
    rice.set_long(selected, remaining)


def commit_mutual_relationship(state: GameState) -> None:
    target = u16(state.relationship_target() << 1)
    targets = state.relationship_targets
    bit = targets.word(target)
    force = u16(state.current_force() << 1)
    relations = state.force_relationships
    flags = relations.word(force)
    flags = u32(flags | (1 << (bit & 31)))
    relations.set_word(force, u16(flags))
    target = u16(state.relationship_target() << 1)
    targets = state.relationship_targets
    target = targets.word(target)
    target = u16(target << 1)
    bit = state.current_force()
    relations = state.force_relationships
    flags = relations.word(target)
    flags = u32(flags | (1 << (bit & 31)))
    relations.set_word(target, u16(flags))


def commit_equipment_purchase(state: GameState) -> None:
    choice = u16(state.equipment_choice() << 2)
    prices = state.equipment_prices
    price = prices.long(choice)
    city = u16(state.chosen_city() << 2)
    gold = state.city_gold
    gold.set_long(city, u32(gold.long(city) - price))
    equipment = state.officer_equipment
    slot = u16(state.selected_officer() << 1)
    slot = u16(slot + state.selected_officer())
    slot = u16(slot + state.equipment_choice())
    choice = u16(state.equipment_choice() << 1)
    levels = state.equipment_levels
    level = u16(levels.word(choice) + 1)
    equipment.set_byte(slot, low8(level))
    state.set_command_mode(state.requested_mode())
    state.set_command_step(40)
    state.set_command_result(98)
    state.set_command_officer(state.selected_officer())
    state.set_command_active(1)
    state.set_scene_selector(9)


def add_selected_cost(state: GameState) -> None:
    selected = u16(state.selected_cost() << 2)
    costs = state.selected_costs
    total = costs.long(selected)
    total = u32(total + state.current_cost())
    if total <= state.cost_limit():
        state.set_current_cost(total)


def add_packet_city_resources(state: GameState, city: Word, packet: Table) -> None:
    city = u16(city)
    index = u16(city << 2)
    gold = state.city_gold
    amount = u32(packet.byte(0, 5) << 24)
    amount = u32(amount | (packet.byte(0, 6) << 16))
    amount = u32(amount | (packet.byte(0, 7) << 8))
    amount = u32(amount | packet.byte(0, 8))
    balance = gold.long(index)
    total = u32(amount + balance)
    if amount + balance > 4294967295 or total > 999999:
        total = u32(999999)
    gold.set_long(index, total)
    amount = u32(packet.byte(0, 9) << 24)
    amount = u32(amount | (packet.byte(0, 10) << 16))
    amount = u32(amount | (packet.byte(0, 11) << 8))
    amount = u32(amount | packet.byte(0, 12))
    rice = state.city_rice
    balance = rice.long(index)
    total = u32(amount + balance)
    if amount + balance > 4294967295 or total > 999999:
        total = u32(999999)
    rice.set_long(index, total)


def add_packet_city_resources_wrapped(state: GameState, city: Word, packet: Table) -> None:
    city = u16(city)
    index = u16(city << 2)
    amount = u32(packet.byte(0, 5) << 24)
    amount = u32(amount | (packet.byte(0, 6) << 16))
    amount = u32(amount | (packet.byte(0, 7) << 8))
    amount = u32(amount | packet.byte(0, 8))
    gold = state.city_gold
    total = u32(gold.long(index) + amount)
    if total > 999999:
        total = u32(999999)
    gold.set_long(index, total)
    amount = u32(packet.byte(0, 9) << 24)
    amount = u32(amount | (packet.byte(0, 10) << 16))
    amount = u32(amount | (packet.byte(0, 11) << 8))
    amount = u32(amount | packet.byte(0, 12))
    rice = state.city_rice
    total = u32(rice.long(index) + amount)
    if total > 999999:
        total = u32(999999)
    rice.set_long(index, total)


def transport_direction_or_arrival(state: GameState, packet: Table) -> CarryOutcome:
    route = state.route_bytes.at(state.route_offset())
    state.set_route_offset(u16(state.route_offset() + 1))
    if not negative_byte(route.byte(0, 1)):
        direction = u8(route.byte())
        direction = u8(direction - 1)
        if direction == 0:
            delta_x, delta_y = u16(65520), u16(0)
        else:
            direction = u8(direction - 1)
            if direction == 0:
                delta_x, delta_y = u16(0), u16(16)
            else:
                direction = u8(direction - 1)
                if direction == 0:
                    delta_x, delta_y = u16(16), u16(0)
                else:
                    delta_x, delta_y = u16(0), u16(65520)
        state.set_route_x(u16(state.route_x() + delta_x))
        state.set_route_y(u16(state.route_y() + delta_y))
        return state.carry_result(0)
    kind = u16(packet.byte() & 3)
    kind = u16(kind << 3)
    city = u16(packet.byte(0, 3) << 2)
    awards = state.transport_awards
    credit = awards.long(kind)
    gold = state.city_gold
    total = u32(credit + gold.long(city))
    if total > 999999:
        total = u32(999999)
    gold.set_long(city, total)
    credit = awards.long(kind, 4)
    rice = state.city_rice
    total = u32(credit + rice.long(city))
    if total > 999999:
        total = u32(999999)
    rice.set_long(city, total)
    packet.set_byte(0, 0)
    return state.carry_result(1)


def transport_collision(state: GameState) -> CarryOutcome:
    x = u16(state.route_x() >> 4)
    y = u16(state.route_y() >> 4)
    objects = state.transport_objects
    for remaining in descending_inclusive(u16(39)):
        if objects.byte() != 0:
            if not objects.byte() & 16:
                if low8(x) == objects.byte(0, 1):
                    if low8(y) == objects.byte(0, 2):
                        return state.carry_result(1)
        objects = objects.advance(4)
    objects = state.packed_objects
    while True:
        length = u16(objects.byte() & 15)
        if length == 0:
            return state.carry_result(0)
        if low8(x) == objects.byte(0, 1):
            if low8(y) == objects.byte(0, 2):
                return state.carry_result(1)
        objects = objects.at(length, 13)


def snapshot_city_resources(state: GameState) -> None:
    gold = state.city_gold
    city = u16(state.tail_city() << 2)
    state.set_snapshot_gold(gold.long(city))
    rice = state.city_rice
    state.set_snapshot_rice(rice.long(city))


def load_city_ed84_ee24_longs(state: GameState) -> None:
    first = state.city_ed84
    city = u16(state.tail_city() << 2)
    state.set_city_snapshot_ed84(first.long(city))
    second = state.city_ee24
    state.set_city_snapshot_ee24(second.long(city))


def commit_relationship_resource_credit(state: GameState) -> None:
    force = state.current_force()
    target = state.selected_officer()
    relations = state.force_relationships
    force = u16(force << 1)
    flags = relations.word(force)
    flags = u32(flags | (1 << (target & 31)))
    relations.set_word(force, u16(flags))
    force = u16(force >> 1)
    target = u16(target << 1)
    flags = relations.word(target)
    flags = u32(flags | (1 << (force & 31)))
    relations.set_word(target, u16(flags))
    amount = state.relationship_credit()
    resources = state.city_gold
    if state.credit_is_rice() != 0:
        resources = state.city_rice
    leader = u16(state.current_force() << 1)
    leaders = state.force_leaders
    leader = leaders.word(leader)
    assignments = state.city_assignments
    city = u16(replace_byte(leader, assignments.byte(leader)))
    city = u16(city & 63)
    city = u16(city << 2)
    total = u32(resources.long(city) + amount)
    if total > 999999:
        total = u32(999999)
    resources.set_long(city, total)


def classify_city_resources(state: GameState) -> Word:
    category = u16(65535)
    gold = state.city_gold
    rice = state.city_rice
    city = u16(state.current_city() << 2)
    if gold.long(city) >= 20000:
        category = u16(0)
        if rice.long(city) >= 20000:
            category = u16(2)
    elif rice.long(city) >= 20000:
        category = u16(1)
    return category
