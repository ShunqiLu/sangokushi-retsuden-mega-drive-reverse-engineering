"""Conditional monthly event queue and neutral city-field submission rules.

    These are live state operations, not a whole monthly/UI scheduler. Field
    identifiers remain neutral because their stronger game meanings are unknown.
"""
from .domain import EventState, U16, U32, u16, replace_byte, negative_byte, low16, divu_retained, checked_word
from .arithmetic import sample_once, sample_small, sample_wide, wrapped_product, divide_percent


def reset_queue(state: EventState) -> None:
    queue = state.queue()
    for slot in range(42):
        queue.write_next(255)


def append_queue(state: EventState, city: U16, incoming_owner: U16) -> U16:
    city = checked_word(city)
    incoming_owner = checked_word(incoming_owner)
    owner = replace_byte(incoming_owner, state.owner(city))
    if not negative_byte(owner):
        if owner == state.player_owner(0) or owner == state.player_owner(1) or owner == state.player_owner(2):
            state.clear_queue_flag()
    queue = state.queue()
    while queue.read_next() != 255:
        pass
    queue.rewind_probe()
    queue.write(city)
    return owner


def scale_field(state: EventState, offset: U16, factor: U16, field_name: str) -> U32:
    offset = checked_word(offset)
    factor = checked_word(factor)
    field = state.field(field_name)
    previous = field.read(offset)
    product = wrapped_product(previous, factor)
    result = divide_percent(product)
    field.write(offset, result)
    return result


def submit_three_fields(state: EventState, city: U16, incoming_owner: U16) -> U16:
    city = checked_word(city)
    incoming_owner = checked_word(incoming_owner)
    owner = replace_byte(incoming_owner, state.owner(city))
    if negative_byte(owner):
        return city
    saved_city = city
    sample = u16(sample_once(state) & 15)
    if sample != 0:
        return saved_city
    append_queue(state, saved_city, sample)
    offset = u16(saved_city << 2)
    factor = u16(sample_wide(state) + 80)
    scale_field(state, offset, factor, 'e1e0')
    factor = u16(sample_small(state) + 95)
    scale_field(state, offset, factor, 'e140')
    factor = u16(sample_wide(state) + 85)
    scale_field(state, offset, factor, 'e320')
    return saved_city


def submit_four_fields(state: EventState, city: U16, incoming_owner: U16) -> U16:
    city = checked_word(city)
    incoming_owner = checked_word(incoming_owner)
    owner = replace_byte(incoming_owner, state.owner(city))
    if negative_byte(owner):
        return owner
    saved_city = city
    sample = u16(sample_once(state) & 15)
    if sample != 0:
        return saved_city
    append_queue(state, saved_city, sample)
    offset = u16(saved_city << 2)
    factor = u16(sample_wide(state) + 80)
    scale_field(state, offset, factor, 'e1e0')
    factor = u16(sample_small(state) + 95)
    scale_field(state, offset, factor, 'e140')
    factor = u16(sample_wide(state) + 85)
    scale_field(state, offset, factor, 'e320')
    factor = u16(sample_wide(state) + 80)
    scale_field(state, offset, factor, 'e0a0')
    return saved_city


def submit_classified_fields(state: EventState, city: U16) -> U16:
    city = checked_word(city)
    saved_city = city
    offset = u16(city << 2)
    field = state.field('e320')
    mask = 0
    classified = divu_retained(field.read(offset), 10)
    mask = replace_byte(mask, state.parameter('mask', low16(classified)))
    if low16(classified) >= 7:
        return saved_city
    sample = u16(sample_once(state) & mask)
    if sample != 0:
        return saved_city
    append_queue(state, saved_city, sample)
    offset = u16(saved_city << 2)
    base_factor = 0
    base_factor = replace_byte(base_factor, state.parameter('factor', low16(classified)))
    factor = 0
    if low16(classified) < 7:
        factor = sample_wide(state)
        if low16(classified) >= 6:
            factor = sample_small(state)
    factor = u16(factor + base_factor)
    scale_field(state, offset, factor, 'e1e0')
    scale_field(state, offset, factor, 'e000')
    scale_field(state, offset, factor, 'e0a0')
    scale_field(state, offset, factor, 'e5a0')
    factor = u16(sample_small(state) + 95)
    scale_field(state, offset, factor, 'e140')
    return saved_city
