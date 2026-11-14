"""Six genuine same-state automatic loadout strategies and caller adapters.

This provider is finite linkage, not a CPU dispatcher. Unknown handler values
stay unbound; original threshold scans and signed-WORD pointer indexing remain
in business_duel. A normal response completion is not the 27572 continuation.
"""
from dataclasses import replace
from .contexts_duel import DuelPreparationContext


PANEL_TARGETS = (
    (0x27BCC, '_choose_duel_guard_response'),
    (0x27C22, '_choose_duel_balanced_response'),
    (0x27C8A, '_choose_duel_range_response'),
    (0x27CA4, '_choose_duel_pressure_response'),
    (0x27CD2, '_choose_duel_randomized_response'),
    (0x27CFC, '_choose_duel_conservative_response'),
)


def _panel_handler(name):
    def invoke(state, context):
        from ..high_level_remaining_flows import business_highbank
        from ..high_level_remaining_flows.contexts_highbank import DuelResponseInput
        if type(context) is not DuelPreparationContext:
            raise ValueError('exact complete preparation caller required')
        context.validate(state)
        frame = context.frame
        actual = DuelResponseInput(frame.command, frame.comparison,
                                   context.response, context.actor, context.stack)
        result = getattr(business_highbank, name)(state, actual)
        result.validate(state)
        current = replace(frame, command=result.sample, comparison=result.seed,
                          response=result.response)
        return DuelPreparationContext(current, result.response, result.actor,
                                      context.opponent, result.stack).validate(state)
    return invoke


def duel_panel_bindings():
    """Return an explicit tuple of six ServiceBinding, each exact context→context.

    Private remaining-flow strategies are the existing real algorithm authority;
    this module adapts their named operands and returns without a second State,
    a RAM snapshot, a zero-valued response or an extra seed read.
    """
    from ..high_level_main_flows.services import ServiceBinding
    return tuple(ServiceBinding(entry, DuelPreparationContext, DuelPreparationContext,
                                _panel_handler(name)) for entry, name in PANEL_TARGETS)
