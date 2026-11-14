"""Explicit platform transitions for the original reset and endless main loop.

These are startup contracts, not a CPU register file. Hardware and processor
transitions have to be supplied; an absent implementation stops at a boundary.
"""
from dataclasses import dataclass
from .domain import Boundary, SceneState, Cursor, Long, uint, checked_cursor


class BootstrapControl:
    """Platform-owned USP and supervisor stack effects, outside ordinary RAM."""

    def set_user_stack(self, state: SceneState, address: Long):
        uint(address, 32)
        raise Boundary('bootstrap USP transition is not supplied')

    def restore_zeroed_bootstrap_context(self, state: SceneState, source: Cursor):
        checked_cursor(source, state)
        raise Boundary('bootstrap MOVEM processor context is not supplied')

    def set_supervisor_stack(self, state: SceneState, address: Long):
        uint(address, 32)
        raise Boundary('bootstrap supervisor stack transition is not supplied')


@dataclass(frozen=True)
class ResetProfile:
    processor: BootstrapControl
    configuration: Cursor
    retained_status_carrier: Long

    def validate(self, state):
        if not isinstance(self.processor, BootstrapControl):
            raise ValueError('explicit bootstrap processor contract required')
        checked_cursor(self.configuration, state)
        uint(self.retained_status_carrier, 32)
        return self


@dataclass(frozen=True)
class BootstrapOutcome:
    status_carrier: Long

    def validate(self, state):
        uint(self.status_carrier, 32)
        return self
