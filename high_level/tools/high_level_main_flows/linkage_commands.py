"""Exact same-state label handlers and their full caller continuation.

Only complete current frames are bound. Old GlyphStyle/SelectedOfficer
contexts do not acquire fabricated carriers. Real functions run lazily;
the explicit ordinary stack domain is not CPU or stack-bus emulation.
"""
from dataclasses import replace
from .services import ServiceBinding
from .domain import Boundary
from .contexts_commands import CommandLabelFrame
from .contexts_main import RosterPanelInput, RosterPanelResult


def _simple_label_result(state, frame, result):
    result.validate(state)
    return replace(frame, glyph_source=result.destination,
        packet_cursor=result.source, background=result.value,
        foreground=result.field, glyph_rows=result.row,
        upload_count=result.offset, carry=result.carry, zero=result.zero,
        negative=result.negative, overflow=result.overflow)


def _default_labels(state, frame):
    from .business_commands import require_command_label_stack_domain
    from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_69
    from ..high_level_remaining_flows.contexts_lowbank import (
        LowbankCoordinateLiveState69Input, LowbankCoordinateLiveState69Result)
    require_command_label_stack_domain(state, frame, 28)
    result = lowbank_coordinate_live_state_69(state, LowbankCoordinateLiveState69Input(
        frame.packet_cursor, frame.background, frame.foreground,
        frame.glyph_rows, frame.upload_count, frame.carry, frame.zero,
        frame.negative, frame.overflow))
    if type(result) is not LowbankCoordinateLiveState69Result:
        raise Boundary('50C6 requires its actual full label return')
    return _simple_label_result(state, frame, result)


def _command_labels(state, frame):
    from .business_commands import require_command_label_stack_domain
    from ..high_level_remaining_flows.business_lowbank import lowbank_process_device_control_10
    from ..high_level_remaining_flows.contexts_lowbank import (
        LowbankProcessDeviceControl10Input, LowbankProcessDeviceControl10Result)
    require_command_label_stack_domain(state, frame, 28)
    result = lowbank_process_device_control_10(state, LowbankProcessDeviceControl10Input(
        frame.packet_cursor, frame.label_codes, frame.code_lookup, frame.vdp_data_port,
        frame.background, frame.foreground, frame.selector, frame.glyph_rows,
        frame.upload_count, frame.code_index, frame.emitted_labels,
        frame.carry, frame.zero, frame.negative, frame.overflow))
    if type(result) is not LowbankProcessDeviceControl10Result:
        raise Boundary('50DC requires its actual full label return')
    result.validate(state)
    return replace(frame, glyph_source=result.destination,
        packet_cursor=result.source, label_codes=result.descriptor,
        code_lookup=result.records, vdp_data_port=result.port,
        background=result.value, foreground=result.field, selector=result.tile,
        glyph_rows=result.row, upload_count=result.offset,
        code_index=result.limit, emitted_labels=result.member,
        carry=result.carry, zero=result.zero, negative=result.negative,
        overflow=result.overflow)


def _selection_labels(state, frame):
    from .business_commands import require_command_label_stack_domain
    from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_70
    from ..high_level_remaining_flows.contexts_lowbank import (
        LowbankCoordinateLiveState70Input, LowbankCoordinateLiveState70Result)
    require_command_label_stack_domain(state, frame, 28)
    result = lowbank_coordinate_live_state_70(state, LowbankCoordinateLiveState70Input(
        frame.packet_cursor, frame.background, frame.foreground,
        frame.glyph_rows, frame.upload_count, frame.carry, frame.zero,
        frame.negative, frame.overflow))
    if type(result) is not LowbankCoordinateLiveState70Result:
        raise Boundary('5164 requires its actual full label return')
    return _simple_label_result(state, frame, result)


def _confirmation_labels(state, frame):
    from .business_commands import require_command_label_stack_domain
    from ..high_level_remaining_flows.business_lowbank import lowbank_coordinate_live_state_71
    from ..high_level_remaining_flows.contexts_lowbank import (
        LowbankCoordinateLiveState71Input, LowbankCoordinateLiveState71Result)
    require_command_label_stack_domain(state, frame, 28)
    result = lowbank_coordinate_live_state_71(state, LowbankCoordinateLiveState71Input(
        frame.packet_cursor, frame.background, frame.foreground,
        frame.glyph_rows, frame.upload_count, frame.carry, frame.zero,
        frame.negative, frame.overflow))
    if type(result) is not LowbankCoordinateLiveState71Result:
        raise Boundary('5192 requires its actual full label return')
    return _simple_label_result(state, frame, result)


def _render_labels(state, frame):
    from .business_commands import render_current_city_command_label_frame
    return render_current_city_command_label_frame(state, frame)


def _upload_roster(state, inputs):
    from .business_main import upload_officer_roster_panel_frame
    return upload_officer_roster_panel_frame(state, inputs)


def command_label_bindings():
    """Seven exact ABIs, including414's BRA alias and real53E6 entry.

    The table prefix is not a bounds clamp. Unknown target/context types keep
    the real service Boundary. Complete54CA requests use the separate genuine
    roster_name_bindings provider; partial officer contexts remain unbound.
    """
    return (
        ServiceBinding(0x506C, CommandLabelFrame, CommandLabelFrame, _render_labels),
        ServiceBinding(0x50C6, CommandLabelFrame, CommandLabelFrame, _default_labels),
        ServiceBinding(0x50DC, CommandLabelFrame, CommandLabelFrame, _command_labels),
        ServiceBinding(0x5164, CommandLabelFrame, CommandLabelFrame, _selection_labels),
        ServiceBinding(0x5192, CommandLabelFrame, CommandLabelFrame, _confirmation_labels),
        ServiceBinding(0x414, RosterPanelInput, RosterPanelResult, _upload_roster),
        ServiceBinding(0x53E6, RosterPanelInput, RosterPanelResult, _upload_roster),
    )
