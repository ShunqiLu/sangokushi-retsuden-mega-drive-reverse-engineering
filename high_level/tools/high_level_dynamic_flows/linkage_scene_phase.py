"""Explicit complete scene-phase continuations on the current live state.

The physical BRA cells and their named entry aliases share one business core.
This is not a PC interpreter or a bound on the natural signed-WORD selector.
Uncovered presentation/action calls remain real typed boundaries, never a
legacy six-value result combined with a stale entry snapshot.
"""
from ..high_level_scene_flows.contexts_objects import (
    SceneControllerFrame, SceneControllerOutcome, checked_controller_frame,
)
from .contexts_early_phase import phase_from_controller, phase_controller_return


def _phase_handler(module_name, function_name):
    def invoke(state, supplied):
        from . import business_early_phase, business_late_phase
        module = (business_early_phase if module_name == 'early'
                  else business_late_phase)
        current = checked_controller_frame(supplied, state)
        actual = getattr(module, function_name)(state,
            phase_from_controller(state, current))
        if type(actual) is SceneControllerOutcome:
            # The real callee has already consumed its continuation. Do not
            # restore the parent's entry SP or pop that token a second time.
            return actual.validate(state)
        return SceneControllerOutcome(
            phase_controller_return(state, actual), None).validate(state)
    return invoke


def _label_clear(state, frame):
    from ..high_level_scene_flows.business_objects import clear_scene_object_label_plane_complete
    return clear_scene_object_label_plane_complete(state,
        checked_controller_frame(frame, state))


def scene_phase_bindings():
    """Finite actual entry contracts; all incoming eight values/views are required.

    Each outer prefix invokes its actual input-latch core then performs the
    original signed-WORD indexed tail. Prefix BRA aliases do not push a token.
    Known nested entries below own complete returns on the documented paths;
    branches to incomplete shared presentation/audio algorithms expose their
    exact gap instead of claiming a full return. Unlisted executable cells
    remain unbound regardless of their numeric selector value.
    """
    from ..high_level_main_flows.services import ServiceBinding
    outer = (
        (0x3DCC2, 0x3E8F2, 'step_main_scene_phase'),
        (0x3DCC6, 0x3EF78, 'step_result_scene_phase'),
        (0x3DCCA, 0x3F022, 'step_confirmation_scene_phase'),
        (0x3DCCE, 0x3F054, 'step_transfer_scene_phase'),
        (0x3DCD2, 0x3F1DC, 'step_primary_detail_scene_phase'),
        (0x3DCD6, 0x3F28E, 'step_secondary_detail_scene_phase'),
        (0x3DCDA, 0x3F340, 'step_summary_scene_phase'),
        (0x3DCDE, 0x3E614, 'step_pair_transition_scene_phase'),
        (0x3DCE2, 0x3DCEA, 'step_initial_scene_phase'),
        (0x3DCE6, 0x3E45E, 'step_exchange_scene_phase'),
    )
    bindings = []
    for slot, entry, name in outer:
        handler = _phase_handler('early', name)
        for address in (slot, entry):
            bindings.append(ServiceBinding(address, SceneControllerFrame,
                SceneControllerOutcome, handler))
    nested = (
        (0x3E900, 'early', 'wait_pair_stage_motion'),
        (0x3E904, 'early', 'advance_pair_stage_motion'),
        (0x3E622, 'early', 'process_pair_phase_counter'),
        (0x3E46C, 'early', 'wait_exchange_scene_transition'),
        (0x3E474, 'early', 'finish_exchange_scene_transition'),
        (0x3E910, 'late', 'adjust_secondary_formation_scene'),
        (0x3E914, 'late', 'confirm_secondary_formation_scene'),
        (0x3E918, 'late', 'update_active_battle_controls'),
        # 3E91C is executable TST/latch code, not an eighth BRA-table cell.
        (0x3E91C, 'late', 'latch_scene_controller_inputs'),
        (0x3F030, 'late', 'dismiss_action_mode_prompt'),
        (0x3F066, 'late', 'confirm_duel_handoff_prompt'),
        (0x3F06A, 'late', 'await_duel_handoff_palette'),
        (0x3F06E, 'late', 'finish_duel_handoff_phase'),
        (0x3F1EE, 'late', 'confirm_result_prompt'),
        (0x3F1F2, 'late', 'await_result_palette'),
        (0x3F1F6, 'late', 'finish_result_phase'),
        (0x3F2A0, 'late', 'confirm_secondary_result_prompt'),
        (0x3F2A4, 'late', 'await_secondary_result_palette'),
        (0x3F2A8, 'late', 'finish_secondary_result_phase'),
        (0x3F356, 'late', 'confirm_primary_result_prompt'),
        (0x3F35A, 'late', 'await_primary_result_palette'),
        (0x3F35E, 'late', 'finish_primary_result_phase'),
        (0x3F61C, 'late', 'adjust_secondary_formation'),
        (0x3F648, 'late', 'deploy_secondary_formation'),
        (0x3F6C2, 'late', 'adjust_primary_formation'),
        (0x3F6EE, 'late', 'deploy_primary_formation'),
        (0x3D970, 'early', 'adjust_scene_scroll'),
    )
    for entry, module, name in nested:
        bindings.append(ServiceBinding(entry, SceneControllerFrame,
            SceneControllerOutcome, _phase_handler(module, name)))
    bindings.append(ServiceBinding(0x4031C, SceneControllerFrame,
        SceneControllerFrame, _label_clear))
    return tuple(bindings)
