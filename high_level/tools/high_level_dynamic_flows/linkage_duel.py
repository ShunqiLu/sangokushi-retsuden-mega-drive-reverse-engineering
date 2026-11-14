"""Explicit same-state duel caller/callee adapters, not an instruction VM.

Only named, reconstructed entry points are linked. Unknown signed-WORD cells
stay unbound. All retained inputs must come from the caller, never a RAM copy,
an extra seed read or an invented zero-valued register facade.
"""
from dataclasses import dataclass, replace
from .domain import (SceneState, Boundary, StackContinuation, checked_state,
                     checked_table, uint)
from .contexts_duel import (DuelRuleFrame, DuelTurnContext, DuelTurnOutcome,
                           DuelCompleteTurnOutcome)
from .contexts_actions import ObjectVectorContext, ObjectActionResult
from ..high_level_scene_flows.contexts_duel import (
    DuelActionContext, DuelActionResult, DuelControlContext, DuelRetainedValues,
    DuelTurnFrame, checked_duel_turn,
)
from ..high_level_main_flows.contexts_scene_support import ScenePresentation


TURN_ENTRIES = {
    0x27576: 'resolve_duel_attack', 0x27586: 'resolve_duel_attack',
    0x2757A: 'perform_duel_feint', 0x27812: 'perform_duel_feint',
    0x2757E: 'flee_duel', 0x278A0: 'flee_duel',
    0x27582: 'finish_special_duel_action', 0x278FE: 'finish_special_duel_action',
}
RULE_ENTRIES = {
    0x2A314: 'choose_duel_cautious_rule', 0x2A318: 'choose_duel_cautious_rule_alias',
    0x2A31C: 'choose_duel_balanced_rule', 0x2A320: 'choose_duel_balanced_rule_alias',
    0x2A324: 'choose_duel_pressure_rule', 0x2A328: 'choose_duel_aggressive_rule',
    0x2A32C: 'execute_duel_cautious_rule', 0x2A338: 'execute_duel_cautious_rule_alias',
    0x2A330: 'execute_duel_balanced_rule', 0x2A334: 'execute_duel_balanced_rule_alias',
    0x2A33C: 'execute_duel_pressure_rule', 0x2A340: 'execute_duel_aggressive_rule',
}
FORMATION_ENTRIES = {
    0x41BEE: 'set_uniform_conservative_orders',
    0x41BF2: 'set_first_timed_formation_orders',
    0x41BF6: 'set_mixed_timed_formation_orders',
    0x41BFA: 'set_third_timed_formation_orders',
    0x41BFE: 'set_uniform_timed_formation_orders',
    0x41CEA: 'choose_first_leader_action',
    0x41CEE: 'choose_second_leader_action',
    0x41CF2: 'choose_third_leader_action',
    0x41CF6: 'choose_alternate_first_leader_action',
    0x41CFA: 'choose_fifth_leader_action',
}


@dataclass(frozen=True)
class FormationVectorCall:
    """Complete caller-owned presentation values plus actual live actors.

    Legacy ObjectVectorContext exposes only five values. It is insufficient
    to manufacture this eight-value callee context; callers must supply it.
    """
    vector: ObjectVectorContext
    presentation: ScenePresentation

    def validate(self, state):
        if type(self.vector) is not ObjectVectorContext:
            raise ValueError('actual object vector call required')
        self.vector.validate(state)
        if type(self.presentation) is not ScenePresentation:
            raise ValueError('complete presentation caller values required')
        self.presentation.validate(state)
        v, p = self.vector, self.presentation
        if (p.command, p.foreground, p.mode, p.rows, p.tile) != (
                v.frame.x, v.frame.y, v.frame.attributes, v.frame.palette, v.frame.tile):
            raise ValueError('five shared presentation values must agree')
        if p.actor is not v.actor or p.opponent is not v.opponent:
            raise ValueError('formation actors must be the actual caller views')
        return self


@dataclass(frozen=True)
class FormationVectorResult:
    action: ObjectActionResult
    presentation: ScenePresentation

    def validate(self, state):
        if type(self.action) is not ObjectActionResult:
            raise ValueError('actual object action result required')
        self.action.validate(state)
        if type(self.presentation) is not ScenePresentation:
            raise ValueError('actual presentation result required')
        self.presentation.validate(state)
        return self


def turn_context(state, caller):
    """Adapt six actual values; refuse the old two-value implicit facade."""
    checked_state(state)
    if type(caller) is not DuelActionContext:
        raise ValueError('exact scene action caller required')
    caller.validate(state)
    retained = caller.retained
    if type(retained) is not DuelRetainedValues:
        raise Boundary('scene caller lacks actual retained duel handler values')
    frame = DuelRuleFrame(caller.controls.command, caller.controls.mode,
                          retained.distance, retained.factor,
                          retained.weapon_difference, retained.variation, caller.live)
    return DuelTurnContext(caller.actor, caller.opponent, frame,
                           caller.continuation).validate(state)


def action_result(state, result):
    if type(result) is not DuelTurnOutcome:
        raise ValueError('actual duel turn outcome required')
    result.validate(state)
    frame = result.frame
    return DuelActionResult(DuelControlContext(frame.command, frame.comparison),
        None, DuelRetainedValues(frame.distance, frame.factor,
                             frame.weapon_difference, frame.variation),
        result.discarded_continuation, frame.live).validate(state)


def _duel_handler(name, *, scene, turn):
    def invoke(state, context):
        # Lazy import prevents business_scene -> services -> business_duel cycles.
        from . import business_duel
        callee = getattr(business_duel, name)
        actual = turn_context(state, context) if scene else context.validate(state)
        result = callee(state, actual)
        if not turn:
            if type(result) is not DuelRuleFrame:
                raise ValueError('actual full duel rule result required')
            result.validate(state)
            result = DuelTurnOutcome(result)
        return action_result(state, result) if scene else result if turn else result.frame
    return invoke


def _formation_handler(name):
    def invoke(state, context):
        from ..high_level_main_flows import business_scene_support
        context.validate(state)
        result = getattr(business_scene_support, name)(state, context.presentation)
        result.validate(state)
        old = context.vector.frame
        frame = replace(old, x=result.command, y=result.foreground,
                        attributes=result.mode, palette=result.rows, tile=result.tile)
        return FormationVectorResult(ObjectActionResult(context.vector.actor,
            context.vector.opponent, frame), result).validate(state)
    return invoke


def _complete_handler(name, *, turn):
    def invoke(state, frame):
        from . import business_duel
        checked_duel_turn(frame, state)
        if turn:
            result = getattr(business_duel, name + '_complete')(state, frame)
            if type(result) is not DuelCompleteTurnOutcome:
                raise ValueError('actual complete action outcome required')
            return result.validate(state)
        context = DuelTurnContext(frame.actor, frame.opponent,
            DuelRuleFrame(frame.command, frame.comparison, frame.distance,
                          frame.factor, frame.weapon_difference, frame.variation, frame))
        result = getattr(business_duel, name)(state, context)
        if type(result) is not DuelRuleFrame or result.live is None:
            raise Boundary('rule did not supply actual current full return')
        result.validate(state)
        return result.live
    return invoke


def duel_bindings():
    """Root dispatcher selects by (actual target, exact caller context type)."""
    from ..high_level_main_flows.services import ServiceBinding
    bindings = []
    for entry, name in TURN_ENTRIES.items():
        bindings.append(ServiceBinding(entry, DuelTurnFrame, DuelCompleteTurnOutcome,
                                        _complete_handler(name, turn=True)))
        bindings.append(ServiceBinding(entry, DuelActionContext, DuelActionResult,
                                        _duel_handler(name, scene=True, turn=True)))
        bindings.append(ServiceBinding(entry, DuelTurnContext, DuelTurnOutcome,
                                        _duel_handler(name, scene=False, turn=True)))
    for entry, name in RULE_ENTRIES.items():
        bindings.append(ServiceBinding(entry, DuelTurnFrame, DuelTurnFrame,
                                        _complete_handler(name, turn=False)))
        bindings.append(ServiceBinding(entry, DuelActionContext, DuelActionResult,
                                        _duel_handler(name, scene=True, turn=False)))
        bindings.append(ServiceBinding(entry, DuelTurnContext, DuelRuleFrame,
                                        _duel_handler(name, scene=False, turn=False)))
    for entry, name in FORMATION_ENTRIES.items():
        bindings.append(ServiceBinding(entry, FormationVectorCall, FormationVectorResult,
                                        _formation_handler(name)))
    return tuple(bindings)


def finish_consumed_duel_action(state, result, actor_values=None):
    """Continue at genuine26D46, not the discarded indexed-call back edge."""
    from .services import continue_duel_fadeout
    from ..high_level_scene_flows.contexts_duel import DuelActorContext
    checked_state(state)
    if type(result) is DuelCompleteTurnOutcome:
        from ..high_level_scene_flows.business_duel import finish_duel_turn_scene
        result.validate(state)
        if result.discarded_continuation is None or result.discarded_continuation.return_carrier != 0x27572:
            raise Boundary('only actual27572 consumption reaches the complete fade tail')
        return finish_duel_turn_scene(state, result.frame)
    if type(result) is not DuelActionResult:
        raise ValueError('actual action result required')
    result.validate()
    if type(actor_values) is not DuelActorContext:
        raise ValueError('actual enclosing actor values required')
    actor_values.validate()
    if result.discarded_continuation is None or result.discarded_continuation.return_carrier != 0x27572:
        raise Boundary('only real27572 consumption has this fade-out continuation')
    return continue_duel_fadeout(state, result.controls, actor_values)
