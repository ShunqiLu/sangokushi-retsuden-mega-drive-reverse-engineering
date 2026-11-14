"""The original four marker clears on the caller's current map-tick frame.

Only this exact ABI is linked. The legacy Gameplay and Scene frontends share
one ordered field algorithm over the same original state; no RAM is copied.
"""
from dataclasses import replace
from .contexts_tick import MapTickFrame, checked_tick_frame
from .services import ServiceBinding


def _reset_markers(state, frame):
    checked_tick_frame(frame, state)
    from ..high_level_gameplay_flow.business_services import _reset_scene_input_marker_fields
    from ..high_level_gameplay_flow.contexts_services import MarkerResetMemory
    _reset_scene_input_marker_fields(MarkerResetMemory(state))
    # The last CLR.W actually supplies NZVC; no carrier or view was written.
    return replace(frame, carry=False, zero=True, negative=False, overflow=False)


def input_marker_bindings():
    """Bind only the complete, same-state current frame at original 4A16."""
    return (ServiceBinding(0x4A16, MapTickFrame, MapTickFrame, _reset_markers),)
