"""Current live operands for the campaign world-map update transaction.

[confirmed ABI] These fields name the eight data carriers and the four live
views used by the input/location/render family.  They are not a CPU register
dictionary: no PC, instruction decoder, hidden defaults, or copied state is
present.  Physical call-stack aliases, X/full SR and chip timing remain separate
compatibility boundaries.
"""
from dataclasses import dataclass

from .domain import (
    SceneState, Long, Table, Cursor, uint, checked_state, checked_table,
    checked_cursor,
)


@dataclass(frozen=True)
class MapTickFrame:
    motion_x: Long
    motion_y: Long
    attributes: Long
    tile_count: Long
    officer: Long
    count: Long
    index: Long
    control_latch: Long
    source: Table
    destination: Table
    packet: Table
    vdp_port: Table
    stack_cursor: Cursor
    carry: bool
    zero: bool
    negative: bool
    overflow: bool

    def validate(self, state: SceneState):
        checked_state(state)
        for value in (
                self.motion_x, self.motion_y, self.attributes, self.tile_count,
                self.officer, self.count, self.index, self.control_latch):
            uint(value, 32, 'current map tick carrier')
        for view in (
                self.source, self.destination, self.packet, self.vdp_port):
            checked_table(view, state)
        checked_cursor(self.stack_cursor, state)
        if any(type(value) is not bool for value in (
                self.carry, self.zero, self.negative, self.overflow)):
            raise ValueError('strict current map tick NZVC required')
        return self


def checked_tick_frame(frame: MapTickFrame, state: SceneState) -> MapTickFrame:
    """Reject incomplete or foreign-state frames before any DATA operation."""
    if type(frame) is not MapTickFrame:
        raise ValueError('complete current MapTickFrame required')
    return frame.validate(state)
