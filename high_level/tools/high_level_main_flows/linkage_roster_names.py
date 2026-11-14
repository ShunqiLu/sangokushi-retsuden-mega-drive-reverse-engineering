"""Adapt the actual roster-name color transaction to its complete caller frame.

Confirmed source: 54CA..5564 and shared 559E..55B0, with the existing
5564..559E selected-city algorithm. This module owns only the ABI projection;
the two business functions remain the sole authorities for their algorithms.
No officer-ID truncation, RAM copy, file reads or missing-carrier defaults are
introduced. Physical BSR/RTS stack DATA and arbitrary stack aliases are not
emulated here; the caller's documented ordinary stack domain remains explicit.
"""
from dataclasses import replace

from .contexts_commands import (
    CommandLabelFrame, RenderRosterNameOrPromptInput,
    RenderRosterNameOrPromptResult,
)
from .contexts_main import RosterNameRequest
from .domain import Boundary
from .services import ServiceBinding


def _render_roster_name(state, request):
    """Consume true 54CA outputs while preserving its untouched live carriers."""
    from .business_commands import render_roster_name_or_prompt

    if type(request) is not RosterNameRequest:
        raise ValueError('actual complete roster-name request required')
    request.validate(state)
    frame = request.frame
    result = render_roster_name_or_prompt(state, RenderRosterNameOrPromptInput(
        records=frame.code_lookup,
        palette=frame.auxiliary_view,
        field=frame.foreground,
        tile=frame.selector,
        row=frame.glyph_rows,
        offset=frame.upload_count,
        member=frame.emitted_labels,
        remaining=frame.glyph_scratch,
    ))
    if type(result) is not RenderRosterNameOrPromptResult:
        raise Boundary('54CA requires its actual roster-name transaction return')
    result.validate(state)
    return replace(frame,
        code_lookup=result.records,
        auxiliary_view=result.palette,
        foreground=result.field,
        selector=result.tile,
        glyph_rows=result.row,
        upload_count=result.offset,
        emitted_labels=result.member,
        carry=result.carry,
        zero=result.zero,
        negative=result.negative,
        overflow=result.overflow,
    ).validate(state)


def roster_name_bindings():
    """Bind only the complete 544E live-in contract, never SelectedOfficer."""
    return (
        ServiceBinding(0x54CA, RosterNameRequest, CommandLabelFrame,
            _render_roster_name),
    )
