"""Live typed rule inputs, independent of CPU registers and physical addresses."""
from __future__ import annotations

from collections.abc import Callable


class ControlReader:
    """Read each semantic field only when the Python rule requests it.

    Callbacks allow live data, including a changed default on its second read.
    Events describe successful host data reads, not CPU cycles or exceptions.
    The probable control role does not identify either side as human/AI/player.
    """

    def __init__(self, *, default_word, alternative_word, primary_byte, secondary_byte):
        inputs = dict(default_word=default_word, alternative_word=alternative_word,
                      primary_byte=primary_byte, secondary_byte=secondary_byte)
        if any(not isinstance(callback, Callable) for callback in inputs.values()):
            raise ValueError('four live typed read callbacks required')
        self._inputs = inputs
        self.events = []

    def _read(self, field, bits):
        value = self._inputs[field]()
        if type(value) is not int or not 0 <= value < (1 << bits):
            raise ValueError(f'{field} requires a complete unsigned {bits}-bit integer')
        self.events.append(dict(field=field, width_bits=bits, value=value))
        return value

    def default_word(self):
        return self._read('default_word', 16)

    def alternative_word(self):
        return self._read('alternative_word', 16)

    def primary_byte(self):
        return self._read('primary_byte', 8)

    def secondary_byte(self):
        return self._read('secondary_byte', 8)
