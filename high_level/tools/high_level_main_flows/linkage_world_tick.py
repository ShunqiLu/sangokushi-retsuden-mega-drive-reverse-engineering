"""Strict full-frame links for the campaign input/location/update family."""
from dataclasses import replace

from .services import ServiceBinding
from .contexts_tick import MapTickFrame, checked_tick_frame
from .contexts_main import LocationChoiceInput, LocationChoiceResult
from .contexts_commands import LocationChoiceFrame


def _world_tick(state, frame):
    from .business_main import advance_campaign_world_tick
    return advance_campaign_world_tick(state, frame)


def _poll_map_input(state, frame):
    from .business_lowbank import poll_world_map_input_frame
    return poll_world_map_input_frame(state, frame)


def _merge_map_controllers(state, frame):
    from .business_commands import append_contextual_cursor_command_frame
    return append_contextual_cursor_command_frame(state, frame)


def _upload_map_palette(state, frame):
    checked_tick_frame(frame, state)
    from .business_lowbank import upload_world_map_palette
    from .contexts_lowbank import UploadWorldMapPaletteInput
    result = upload_world_map_palette(state, UploadWorldMapPaletteInput(frame.motion_x))
    result.validate(state)
    return replace(frame, motion_x=result.value, carry=result.carry,
        zero=result.zero, negative=result.negative, overflow=result.overflow)


def _choose_location(state, frame):
    """Project the call's current operands; do not freeze an entry snapshot."""
    checked_tick_frame(frame, state)
    from .business_main import advance_campaign_location_choice
    location = LocationChoiceFrame(frame.motion_x, frame.motion_y,
        frame.attributes, frame.source, frame.destination, frame.vdp_port,
        frame.stack_cursor, frame.carry, frame.zero, frame.negative, frame.overflow)
    result = advance_campaign_location_choice(state, LocationChoiceInput(location))
    if type(result) is not LocationChoiceResult:
        raise ValueError('actual complete location return required')
    result.validate(state)
    current = result.frame
    return replace(frame, motion_x=current.motion_value, motion_y=current.prompt_field,
        attributes=current.sprite_attributes, source=current.sprite_source,
        destination=current.palette_source, vdp_port=current.vdp_port,
        stack_cursor=current.stack_cursor, carry=current.carry, zero=current.zero,
        negative=current.negative, overflow=current.overflow)


def world_tick_bindings():
    """Only exact complete live ABIs; unknown table targets stay unresolved."""
    return (
        ServiceBinding(0xF10, MapTickFrame, MapTickFrame, _world_tick),
        ServiceBinding(0x4890, MapTickFrame, MapTickFrame, _poll_map_input),
        ServiceBinding(0x4998, MapTickFrame, MapTickFrame, _upload_map_palette),
        ServiceBinding(0xA370, MapTickFrame, MapTickFrame, _merge_map_controllers),
        ServiceBinding(0x14E0, MapTickFrame, MapTickFrame, _choose_location),
    )
