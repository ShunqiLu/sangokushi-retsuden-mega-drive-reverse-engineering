"""Editable fixed-width arithmetic and deterministic sampling semantics."""
from .domain import (EventState, U16, U32, u16, u32, low16, high16,
                     swap_words, replace_word, join_words, negative_long,
                     divu_retained, checked_word, checked_long)


def random_sample(state: EventState) -> U16:
    seed = state.seed()
    if seed == 0:
        seed = 0x2A6D365A
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


def sample_once(state: EventState) -> U16:
    return random_sample(state)


def sample_small(state: EventState) -> U16:
    while True:
        sample = u16(random_sample(state) & 7)
        if sample < 5:
            return sample


def sample_wide(state: EventState) -> U16:
    while True:
        sample = u16(random_sample(state) & 15)
        if sample < 10:
            return sample


def wrapped_product(value: U32, factor: U16) -> U32:
    value = checked_long(value)
    factor = checked_word(factor)
    return u32(value * factor)


def divide_percent(product: U32) -> U32:
    product = checked_long(product)
    quotient, remainder = signed_divmod(product, 100)
    return quotient


def signed_divmod(numerator: U32, denominator: U32) -> tuple[U32, U32]:
    numerator = checked_long(numerator)
    denominator = checked_long(denominator)
    if negative_long(denominator):
        quotient, remainder = positive_denominator(numerator, u32(-denominator))
        return u32(-quotient), remainder
    return positive_denominator(numerator, denominator)


def positive_denominator(numerator: U32, denominator: U32) -> tuple[U32, U32]:
    """Sign handling deliberately does not retest the denominator.

    In particular negating 0x80000000 wraps; recursion into signed_divmod would
    change the original behaviour. The label's historical name is not a clamp.
    """
    numerator = checked_long(numerator)
    denominator = checked_long(denominator)
    if negative_long(numerator):
        quotient, remainder = unsigned_divmod(u32(-numerator), denominator)
        return u32(-quotient), u32(-remainder)
    return unsigned_divmod(numerator, denominator)


def unsigned_divmod(numerator: U32, denominator: U32) -> tuple[U32, U32]:
    numerator = checked_long(numerator)
    denominator = checked_long(denominator)
    if denominator <= 65535:
        return word_pair_divmod(numerator, denominator)
    if denominator == numerator:
        return 1, 0
    if denominator > numerator:
        return 0, numerator
    divisor_high = u32(high16(denominator) + 1)
    saved_numerator = numerator
    saved_denominator = denominator
    quotient, remainder = word_pair_divmod(numerator, divisor_high)
    denominator_part = divu_retained(saved_denominator, divisor_high)
    quotient = divu_retained(quotient, denominator_part)
    quotient = u32(quotient & 65535)
    while True:
        product = u32(low16(saved_denominator) * low16(quotient))
        high_product = u32(high16(saved_denominator) * low16(quotient))
        product = u32(product + swap_words(high_product))
        if product > saved_numerator:
            quotient = u32(quotient - 1)
            continue
        remainder = u32(saved_numerator - product)
        if saved_denominator <= remainder:
            quotient = u32(quotient + 1)
            continue
        return quotient, remainder


def word_pair_divmod(numerator: U32, denominator: U32) -> tuple[U32, U32]:
    numerator = checked_long(numerator)
    denominator = checked_long(denominator)
    high_division = divu_retained(high16(numerator), denominator)
    high_quotient = low16(high_division)
    low_division = divu_retained(join_words(high16(high_division), low16(numerator)), denominator)
    remainder = high16(low_division)
    quotient = join_words(high_quotient, low16(low_division))
    return quotient, remainder
