"""Debt interest, including the original date and word-half arithmetic.

Dates are read live through ports. Negative date gaps are deliberately retained;
there is no natural-game-domain clamp or host-random substitute here.
"""
from .domain import (Clock, DebtDates, signed8, sub8, mul16, add16, mul_u16,
                     low_word, high_word, rotate_words, add32, div_signed)


def debt_due(clock: Clock, record: DebtDates, principal: int, offset: int) -> int:
    year_delta = signed8(sub8(clock.year(), record.year(offset)))
    months = mul16(year_delta, 12)
    month_delta = signed8(sub8(clock.month(), record.month(offset)))
    months = add16(months, month_delta)
    if months == 0:
        return principal
    factor = mul16(months, 5)
    low_product = mul_u16(factor, low_word(principal))
    high_product = mul_u16(factor, high_word(principal))
    numerator = add32(rotate_words(high_product), low_product)
    interest = div_signed(numerator, 100)
    return add32(interest, principal)
