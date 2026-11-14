"""Exact original battle-initialization device waits, without new wait types.

This helper supplies no transfer, clock or ACK. Existing explicit owners must
make progress before the original loop resumes and rereads its hardware.
"""
from .scene_load_steps import GameplaySceneWait
from .contexts_services import SceneRefreshMemory
from ..high_level_main_flows.business_movement_support import _movement_frame


def initialization_device_wait(memory, frame, reason, sprite=None):
    """Preserve live full SR and all carriers at one source-proven device poll."""
    if type(memory) is not SceneRefreshMemory:
        raise ValueError('the actual Scene refresh memory owner is required')
    frame = _movement_frame(memory.state, frame)
    if reason == 'vdp-dma' and type(sprite) is bool:
        poll = 0x68FA if sprite else 0x6886
    elif reason == 'sound-bus-acquire' and sprite is None:
        poll = 0x8098
    else:
        raise ValueError('only original6886/68FA DMA and8098 BUSACK polls are admitted')
    # The shared original body has just performed MOVE/ANDI on its retained
    # Frame. Publish those actual CCR-X bits before an external suspension;
    # this is not a ready flag or an inferred interrupt/device result.
    frame = memory.sync_status(frame)
    return GameplaySceneWait(memory.state, frame, memory.state.sr, reason, poll).validate()
