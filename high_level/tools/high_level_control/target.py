"""Explicit 68000 compatibility bindings; no opcode or old-source templates."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Binding:
    name: str
    entry: int
    primary_byte: int
    secondary_byte: int
    default_word: int = 0xf602
    alternative_word: int = 0xf604
    allocated_bytes: int = 42


BINDINGS = (Binding('primary_700a', 0x279e6, 0xff700a, 0xff700b),
            Binding('primary_700b', 0x27a10, 0xff700b, 0xff700a))
FIELD_BITS = dict(default_word=16, alternative_word=16, primary_byte=8, secondary_byte=8)
ABI = dict(result_WORD='d0', comparison_BYTE='d1',
           result_upper_16_bits='preserved', comparison_upper_24_bits='preserved',
           stack='ordinary original RTS; caller supplies a real return frame')


def validate_binding(binding):
    if type(binding) is not Binding or type(binding.name) is not str or any(type(value) is not int for value in
            (binding.entry, binding.primary_byte, binding.secondary_byte, binding.default_word, binding.alternative_word, binding.allocated_bytes)) or binding not in BINDINGS:
        raise ValueError('one of the two explicit original compatibility bindings required')
    return binding
