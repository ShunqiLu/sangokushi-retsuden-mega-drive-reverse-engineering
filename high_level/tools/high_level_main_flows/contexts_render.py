"""Observed fields of the map render algorithms, on one live SceneState.

The legacy APIs do not observe all aliases or condition bits. Their unknown
fields remain None here; only a complete MapTickFrame can be projected back
to a complete tick. This record neither creates RAM nor guesses input values.
"""
from dataclasses import dataclass
from .domain import (SceneState, Long, Table, Cursor, uint, checked_state,
                     checked_table, checked_cursor)


@dataclass(frozen=True)
class RenderFields:
    x: Long
    y: Long
    attributes: Long
    tile: Long
    officer: Long
    count: Long
    index: Long
    remaining: Long
    source: Table | None
    destination: Table | None
    packet: Table | None
    carry: bool | None
    zero: bool | None
    negative: bool | None
    overflow: bool | None
    stack_cursor: Cursor | None

    def validate(self, state: SceneState):
        checked_state(state)
        for value in (self.x, self.y, self.attributes, self.tile, self.officer,
                      self.count, self.index, self.remaining):
            uint(value, 32)
        for view in (self.source, self.destination, self.packet):
            if view is not None:
                checked_table(view, state)
        if self.stack_cursor is not None:
            checked_cursor(self.stack_cursor, state)
        for value in (self.carry, self.zero, self.negative, self.overflow):
            if value is not None and type(value) is not bool:
                raise ValueError('observed render NZVC or explicit unknown required')
        return self


def checked_render_fields(fields: RenderFields, state: SceneState):
    if type(fields) is not RenderFields:
        raise ValueError('exact render algorithm fields required')
    return fields.validate(state)
