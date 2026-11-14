"""Exact non-prefix entries used by the original packed-group lifecycle.

confirmed: 001264..00127E plus the shared00128E RTS, and015BD0 RTS in
the editable original assembly. These are complete Scene-frame interfaces,
not scalar substitutes or aliases to owners with extra entry-side effects.
"""
from ..high_level_scene_flows.domain import SceneState
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame
from ..high_level_main_flows.business_commands import (
    _city_ui_frame_fields,
    _city_ui_bit_fields,
    _city_ui_store_fields,
    _campaign_ui_call_fields,
)


def present_group_outside_map_indicator_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1264: warn only if the original indicator bit is clear; omit1228 prefix.

    The original caller has already selected this middle entry. In particular,
    no pointer-containment checks, coordinate loads or alternative5C98 call
    belong here. The sole inner JSR retains its real127A return LONG.
    """
    frame = _city_ui_frame_fields(state, frame, 0x1264)
    frame = _city_ui_bit_fields(state, frame, state.read(0xFFFFF3A4, 1), 3)
    if not frame.status & 4:
        return frame
    frame = _city_ui_store_fields(state, frame, 0xFFFFF600, 0x74)
    return _campaign_ui_call_fields(state, frame, 0x5ABC, 0x127A)


def finish_group_split_action_fields(
        state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """15BD0: original immediate RTS; the enclosing call bridge owns its slot.

    15BAE is an actual BSR.W to this RTS, returning to15BB2 before the
    parent's independent cancel-bit test. Do not re-enter15B7E, repeat its
    prefix, clear a flag, synthesize a result or pop the caller's return LONG.
    """
    return _city_ui_frame_fields(state, frame, 0x15BD0)
