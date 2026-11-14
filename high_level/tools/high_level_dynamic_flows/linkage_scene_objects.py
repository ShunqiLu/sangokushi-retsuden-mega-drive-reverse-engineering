"""Known complete object-action continuations on the controller's live state.

These are actual semantic callees, not an indexed-PC interpreter. The selected
BRA slots share the same movement core as the legacy action API. Unknown
natural indices and action bodies without a complete return remain unbound;
installing this provider does not prove the full action family or gameplay.
"""
from dataclasses import replace

from ..high_level_scene_flows.contexts_objects import (
    SceneControllerFrame, SceneControllerConditions, SceneControllerOutcome,
    SceneRenderFrame, checked_controller_frame,
)
from ..high_level_main_flows.services import ServiceBinding


def _motion_handler(direction):
    def invoke(state, frame):
        from .business_actions import continue_object_motion_frame
        actual = continue_object_motion_frame(state, frame, direction)
        return SceneControllerOutcome(actual, None).validate(state)
    return invoke


def _clear_selected_action(state, frame):
    """40D5E's actual BRA to 40D76; clear control, retain all operands/views."""
    from .business_actions import finish_object_action_noop
    current = checked_controller_frame(frame, state)
    legacy = SceneRenderFrame(current.x, current.y, current.attributes,
                              current.palette, current.tile)
    finish_object_action_noop(state, current.actor, current.traversal, legacy)
    actual = replace(current,
        conditions=SceneControllerConditions(False, True, False, False))
    return SceneControllerOutcome(actual, None).validate(state)


def scene_object_bindings():
    """Exact full-input contracts for proven motion slots and the clear tail.

    BRA/JMP entry does not push another token. The controller/selector supplies
    the actual current entry stack; these callees do not manufacture call or
    return-memory effects. Both primary and pursuit continuation slots are
    executable aliases of the same four original direction algorithms.
    """
    entries = (
        (0x40D4E, 0), (0x40D52, 1), (0x40D56, 2), (0x40D5A, 3),
        (0x40F88, 0), (0x40F8C, 1), (0x40F90, 2), (0x40F94, 3),
    )
    bindings = tuple(ServiceBinding(entry, SceneControllerFrame,
        SceneControllerOutcome, _motion_handler(direction))
        for entry, direction in entries)
    return bindings + (
        ServiceBinding(0x40D5E, SceneControllerFrame, SceneControllerOutcome,
                       _clear_selected_action),
        ServiceBinding(0x40D76, SceneControllerFrame, SceneControllerOutcome,
                       _clear_selected_action),
    )
