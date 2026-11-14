"""Duel turn actions, live combat statistics and table-driven AI rules.

Executable vector slots are named entry points, not interpreted code. The
three nonlocal exits return their discarded *real* caller continuation, so
the enclosing duel flow can continue at its existing 26D46 control tail.
All tables and media are supplied through the shared scene DATA interface.
"""
from dataclasses import replace
from .domain import (SceneState, Table, Word, Long, uint, low16, low8, u8,
                     u16, u32, replace_word, replace_byte, negative_word,
                     stitched_product, checked_state, checked_table, Boundary,
                     high16, swap_words, StackContinuation)
from .contexts_duel import (DuelRuleFrame, DuelTurnContext, DuelTurnOutcome,
                            DuelSpacingResult, DuelControlContext,
                            checked_duel_context, DuelCompleteTurnOutcome,
                            DuelTurnFrame, DuelConditionObservation, checked_duel_turn)
from .services import (sample_random_pair, choose_duel_status_text,
                       wait_active_duel_action, wait_either_duel_action,
                       clear_duel_text_plane, unsigned_divmod, ram_view,
                       divide_duel_frame, duel_complete_service)


def _ram(state, low):
    return ram_view(state, 'ram_' + low)
















def measure_duel_spacing(state: SceneState,
        context: DuelTurnContext) -> DuelSpacingResult:
    """Historical result projects one complete spacing body, preserving actual borrow."""
    returned=measure_duel_spacing_fields(state,_duel_rule_legacy_fields(state,context))
    return DuelSpacingResult(_duel_rule_legacy_projection(state,returned),bool(returned.status&1))














def _from_live(frame):
    return DuelRuleFrame(frame.command, frame.comparison, frame.distance,
        frame.factor, frame.weapon_difference, frame.variation, frame)


def _values(frame, **changes):
    live = frame.live
    if live is not None:
        live = replace(live, **changes)
    projection = {name: value for name, value in changes.items() if name in (
        'command', 'comparison', 'distance', 'factor', 'weapon_difference', 'variation')}
    return replace(frame, **projection, live=live)


def _full(context, state):
    checked_duel_context(context, state)
    if context.frame.live is None:
        raise Boundary('action requires actual current D5/response/A2/entry-SP, not a six-value observation')
    return checked_duel_turn(context.frame.live, state)


def _logic(value, bits=32):
    value &= (1 << bits) - 1
    return DuelConditionObservation(False, value == 0,
        bool(value & (1 << (bits - 1))), False)


def _arithmetic(left, right, bits=32, *, subtract=False):
    mask = (1 << bits) - 1
    left, right = left & mask, right & mask
    value = (left - right if subtract else left + right) & mask
    carry = left < right if subtract else left + right > mask
    overflow = bool(((left ^ right) if subtract else ~(left ^ right)) &
                    (left ^ value) & (1 << (bits - 1)))
    return DuelConditionObservation(carry, value == 0,
                                    bool(value & (1 << (bits - 1))), overflow)


def _sample(state, frame):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,frame,0x83d4,'_duel_action_call_fields')


def _message(state, frame, selection):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,frame,0x28228,'_duel_action_call_fields')


def _wait(state, frame, *, either=False):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,frame,0x2777a,'_duel_action_call_fields')


def _clear(state, frame):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,frame,0x27d76,'_duel_action_call_fields')


def _second_turn(state):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,None,0x27882,'_duel_action_second_fields')


def _toggle(state):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,None,0x27882,'toggle_duel_turn_fields')


def toggle_duel_turn(state: SceneState) -> None:
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,None,0x27882,'toggle_duel_turn_fields')


def toggle_duel_turn_complete(state, frame):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,frame,0x27882,'toggle_duel_turn_fields')


def _weight_fields(value, factor, response):
    if value < 0x10000:
        product = low16(value) * factor
        return product, response, _logic(product)
    lower_product = low16(value) * factor
    response = swap_words(u32(high16(value) * factor))
    product = u32(lower_product + response)
    return product, response, _arithmetic(lower_product, response)


def multiply_duel_weight(state: SceneState, value: Long, factor: Word) -> Long:
    """27ABE scalar observation of the same SWAP-stitched field core."""
    checked_state(state)
    uint(value, 32)
    uint(factor, 16)
    return _weight_fields(value, factor, None)[0]


def _weight_frame(state, frame):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,frame,0x27abe,'multiply_duel_weight_fields')


def prepare_duel_combat_statistics(state: SceneState, context: DuelTurnContext) -> DuelRuleFrame:
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,context,0x27ae6,'prepare_duel_combat_statistics_fields')


def _push_long(frame, value):
    """Historical observations request the single complete current action core."""
    raise Boundary('historical partial stack needs the complete current action frame')


def _pop_long(frame, name):
    """Historical observations request the single complete current action core."""
    raise Boundary('historical partial stack needs the complete current action frame')


def _divide_frame(state, frame):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,frame,0x35760,'_duel_action_call_fields')


def _frame_message(state, frame, selection):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,frame,0x28228,'_duel_action_call_fields')


def _frame_wait(state, frame, *, either=False):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,frame,0x2777a,'_duel_action_call_fields')


def _frame_clear(state, frame):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,frame,0x27d76,'_duel_action_call_fields')


def _nonlocal_complete(frame):
    """Historical observations request the single complete current action core."""
    raise Boundary('historical partial stack needs the complete current action frame')


def _legacy_turn(result):
    return DuelTurnOutcome(_from_live(result.frame), result.discarded_continuation)


def _recover_after_duel_attack(state, frame):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,frame,0x276ac,'_recover_after_duel_attack_fields')


def resolve_duel_attack_complete(state, frame):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,frame,0x27576,'resolve_duel_attack_fields')


def resolve_duel_attack(state: SceneState, context: DuelTurnContext) -> DuelTurnOutcome:
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,context,0x27576,'resolve_duel_attack_fields')


def perform_duel_feint_complete(state, frame):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,frame,0x2757a,'perform_duel_feint_fields')


def perform_duel_feint(state: SceneState, context: DuelTurnContext) -> DuelTurnOutcome:
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,context,0x2757a,'perform_duel_feint_fields')


def flee_duel_complete(state, frame):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,frame,0x2757e,'flee_duel_fields')


def flee_duel(state: SceneState, context: DuelTurnContext) -> DuelTurnOutcome:
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,context,0x2757e,'flee_duel_fields')


def finish_special_duel_action_complete(state, frame):
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,frame,0x27582,'finish_special_duel_action_fields')


def finish_special_duel_action(state: SceneState, context: DuelTurnContext) -> DuelTurnOutcome:
    """Historical observations request the single complete current action core."""
    return _duel_action_legacy_fields(state,context,0x27582,'finish_special_duel_action_fields')


def _choose_ai_rule(state, context, threshold, easy, normal, hard):
    """Closed old table-family API of the sole original profile decision."""
    plans={(50,0x2A4A6,0x2A4B2,0x2A4BE):0x2A314,
        (60,0x2A44C,0x2A458,0x2A464):0x2A31C,
        (60,0x2A3F4,0x2A400,0x2A40C):0x2A324,
        (70,0x2A39E,0x2A3AA,0x2A3B6):0x2A328}
    entry=plans.get((threshold,easy,normal,hard))
    if entry is None:
        raise ValueError('actual original duel profile family required')
    returned=choose_duel_profile_fields(state,_duel_rule_legacy_fields(state,context),entry)
    return _duel_rule_legacy_projection(state,returned)


def choose_duel_cautious_rule(state: SceneState, context: DuelTurnContext) -> DuelRuleFrame:
    """2A314/2A318: threshold50 policy."""
    return _choose_ai_rule(state, context, 50, 0x2A4A6, 0x2A4B2, 0x2A4BE)


def choose_duel_cautious_rule_alias(state: SceneState, context: DuelTurnContext) -> DuelRuleFrame:
    return choose_duel_cautious_rule(state, context)


def choose_duel_balanced_rule(state: SceneState, context: DuelTurnContext) -> DuelRuleFrame:
    """2A31C/2A320: threshold60 policy."""
    return _choose_ai_rule(state, context, 60, 0x2A44C, 0x2A458, 0x2A464)


def choose_duel_balanced_rule_alias(state: SceneState, context: DuelTurnContext) -> DuelRuleFrame:
    return choose_duel_balanced_rule(state, context)


def choose_duel_pressure_rule(state: SceneState, context: DuelTurnContext) -> DuelRuleFrame:
    """2A324: a separate threshold60 table family."""
    return _choose_ai_rule(state, context, 60, 0x2A3F4, 0x2A400, 0x2A40C)


def choose_duel_aggressive_rule(state: SceneState, context: DuelTurnContext) -> DuelRuleFrame:
    """2A328: threshold70 policy."""
    return _choose_ai_rule(state, context, 70, 0x2A39E, 0x2A3AA, 0x2A3B6)


def choose_duel_opponent_special(state: SceneState,
        context: DuelTurnContext) -> DuelRuleFrame:
    """Historical caller observes the one complete original decision core."""
    returned=choose_duel_opponent_special_fields(state,_duel_rule_legacy_fields(state,context))
    return _duel_rule_legacy_projection(state,returned)


def choose_duel_random_motion(state: SceneState,
        context: DuelTurnContext) -> DuelRuleFrame:
    """Historical caller observes the one complete original decision core."""
    returned=choose_duel_random_motion_fields(state,_duel_rule_legacy_fields(state,context))
    return _duel_rule_legacy_projection(state,returned)


def _orient_and_gate_duel_motion(state, context, frame):
    """Old helper delegates the sole original retained-field tail."""
    returned=_duel_rule_motion_fields(state,_duel_rule_legacy_fields(state,context,frame))
    return _duel_rule_legacy_projection(state,returned)


def _motion(state, context, frame, command):
    frame = _values(frame, command=replace_word(frame.command, command))
    return _orient_and_gate_duel_motion(state, context, frame)


def _try_special(state, context, frame):
    return choose_duel_opponent_special(state, replace(context, frame=frame))


def _guarded_motion(state, context, frame):
    """Old helper delegates the sole original retained-field tail."""
    returned=_duel_rule_distant_fields(state,_duel_rule_legacy_fields(state,context,frame))
    return _duel_rule_legacy_projection(state,returned)


def execute_duel_cautious_rule(state: SceneState,
        context: DuelTurnContext) -> DuelRuleFrame:
    """Historical vector API projects the sole complete shared executor."""
    returned=execute_duel_rule_fields(state,_duel_rule_legacy_fields(state,context),172844)
    return _duel_rule_legacy_projection(state,returned)


def execute_duel_cautious_rule_alias(state: SceneState, context: DuelTurnContext) -> DuelRuleFrame:
    return execute_duel_cautious_rule(state, context)


def execute_duel_balanced_rule(state: SceneState,
        context: DuelTurnContext) -> DuelRuleFrame:
    """Historical vector API projects the sole complete shared executor."""
    returned=execute_duel_rule_fields(state,_duel_rule_legacy_fields(state,context),172848)
    return _duel_rule_legacy_projection(state,returned)


def execute_duel_balanced_rule_alias(state: SceneState, context: DuelTurnContext) -> DuelRuleFrame:
    return execute_duel_balanced_rule(state, context)


def _pressure_motion(state, context, frame):
    """Old helper delegates the sole original retained-field tail."""
    returned=_duel_rule_pressure_fields(state,_duel_rule_legacy_fields(state,context,frame))
    return _duel_rule_legacy_projection(state,returned)


def execute_duel_pressure_rule(state: SceneState,
        context: DuelTurnContext) -> DuelRuleFrame:
    """Historical vector API projects the sole complete shared executor."""
    returned=execute_duel_rule_fields(state,_duel_rule_legacy_fields(state,context),172860)
    return _duel_rule_legacy_projection(state,returned)


def execute_duel_aggressive_rule(state: SceneState,
        context: DuelTurnContext) -> DuelRuleFrame:
    """Historical vector API projects the sole complete shared executor."""
    returned=execute_duel_rule_fields(state,_duel_rule_legacy_fields(state,context),172864)
    return _duel_rule_legacy_projection(state,returned)


"""Root50: original duel profile and executor decisions, not instruction replay."""
from ..high_level_scene_flows.contexts_scene import FirstDeploymentFrame, first_replace, SceneRefreshMemory
from ..high_level_scene_flows.business_scene import _scene_render_asl_word
from ..high_level_scene_flows.business_duel import (
    _duel_strategy_call_fields, _duel_strategy_actor_values,
    _duel_strategy_partial_fields, measure_duel_weapon_contact_fields,
)
from ..high_level_remaining_flows.business_city import _resource_cost_frame, _duel_commit_sub_word_fields
from ..high_level_main_flows.business_movement_support import (
    _movement_move, _movement_test, _movement_compare, _movement_add_word,
)
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
from ..high_level_gameplay_flow.business_battle import _presentation_call_fields, _postbattle_bit_fields
from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
from ..high_level_scene_flows.domain import s16


def _duel_rule_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Closed direct rule calls reuse the real stack and the one complete RNG."""
    if target == 0x83D4:
        return _duel_strategy_call_fields(state, frame, target, continuation)
    def algorithm(memory, entered):
        if target == 0x2A22E:
            return measure_duel_weapon_contact_fields(memory.state, entered)
        if target == 0x2A26C:
            return measure_duel_spacing_fields(memory.state, entered)
        if target == 0x2AA36:
            return choose_duel_opponent_special_fields(memory.state, entered)
        if target == 0x2A52A:
            return choose_duel_random_motion_fields(memory.state, entered)
        raise MovementContinuationBoundary(target, entered, 'actual duel rule child is not restored')
    return _presentation_call_fields(BattlePresentationMemory(state), frame, continuation, algorithm)


def measure_duel_spacing_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2A26C..2A294: opponent reach; D3 retains its actual incoming value."""
    frame = _resource_cost_frame(state, frame, 0x2A26C)
    frame = _movement_move(state, frame, 'target_y', frame.candidates.word(12), 16)
    frame = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_y', low16(frame.target_y), 1)
    reach = state.read(u32(0x2A260 + s16(low16(frame.target_y))), 2)
    frame = _movement_move(state, frame, 'unit', reach, 16)
    frame = _movement_add_word(state, frame, 'unit', 8)
    frame = _postbattle_bit_fields(frame, bool(frame.candidates.byte(24) & 8))
    state.sr = (state.sr & 65504) | frame.status
    if frame.status & 4:
        frame = _duel_commit_sub_word_fields(state, frame, 'unit', 0, True)
    frame = _movement_add_word(state, frame, 'unit', frame.candidates.word(14))
    frame = _duel_commit_sub_word_fields(state, frame, 'unit', frame.roster.word(14))
    if frame.status & 8:
        frame = _duel_commit_sub_word_fields(state, frame, 'unit', 0, True)
    deduction = state.read(u32(0x2A294 + s16(low16(frame.target_y))), 2)
    return _duel_commit_sub_word_fields(state, frame, 'unit', deduction)


def choose_duel_profile_fields(state: SceneState,
        frame: FirstDeploymentFrame, entry: int) -> FirstDeploymentFrame:
    """Six real instruction-vector entries share the original common profile tail."""
    frame = _resource_cost_frame(state, frame, entry)
    if entry in (0x2A314, 0x2A318):
        threshold, easy, normal, hard = 50, 0x2A4A6, 0x2A4B2, 0x2A4BE
    elif entry in (0x2A31C, 0x2A320):
        threshold, easy, normal, hard = 60, 0x2A44C, 0x2A458, 0x2A464
    elif entry == 0x2A324:
        threshold, easy, normal, hard = 60, 0x2A3F4, 0x2A400, 0x2A40C
    elif entry == 0x2A328:
        threshold, easy, normal, hard = 70, 0x2A39E, 0x2A3AA, 0x2A3B6
    else:
        raise MovementContinuationBoundary(entry, frame, 'unowned duel profile instruction entry')
    mode = state.read(0xFFFFEFD2, 2)
    frame = _movement_test(state, frame, mode, 16)
    if mode == 0:
        table = easy
    else:
        mode = state.read(0xFFFFEFD2, 2)
        frame = _movement_compare(state, frame, mode, 2, 16)
        table = hard if mode == 2 else normal
    frame = first_replace(frame, controller=state.table_at(table).cursor())
    frame = _movement_move(state, frame, 'target_x', threshold, 16)
    frame = _movement_compare(state, frame, low16(frame.target_x), frame.roster.word(28), 16)
    if not frame.status & 1:
        frame = first_replace(frame, controller=frame.controller.advance(2))
    frame = _movement_move(state, frame, 'target_x', frame.roster.word(12), 16)
    frame = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_x', low16(frame.target_x), 2)
    frame = first_replace(frame, controller=frame.controller.advance(s16(low16(frame.target_x))))
    frame = _duel_rule_call_fields(state, frame, 0x83D4, 0x2A38C)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 1, 16)
    if not frame.status & 4:
        frame = first_replace(frame, controller=frame.controller.advance(1))
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_x', frame.controller.byte(), 8)
    frame.roster.set_word(36, low16(frame.target_x))
    return _movement_test(state, frame, low16(frame.target_x), 16)


def choose_duel_random_motion_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2A52A: original300 result folds to zero; never redraw a random result."""
    frame = _resource_cost_frame(state, frame, 0x2A52A)
    frame = _duel_rule_call_fields(state, frame, 0x83D4, 0x2A530)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 0x300, 16)
    frame = _movement_compare(state, frame, low16(frame.target_x), 0x300, 16)
    if frame.status & 4:
        frame = _movement_move(state, frame, 'target_x', 0, 16)
    return _movement_move(state, frame, 'target_x', low16(frame.target_x) | 0x10, 16)


def choose_duel_opponent_special_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2AA36: opponent attack gate, true spacing borrow and live status table."""
    frame = _resource_cost_frame(state, frame, 0x2AA36)
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _postbattle_bit_fields(frame, bool(frame.candidates.byte(2) & 128))
    state.sr = (state.sr & 65504) | frame.status
    if frame.status & 4:
        return frame
    frame = _duel_rule_call_fields(state, frame, 0x2A26C, 0x2AA44)
    if not frame.status & 1:
        return frame
    frame = _movement_move(state, frame, 'target_x', frame.candidates.word(2), 16)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 3, 16)
    frame = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_x', low16(frame.target_x), 1)
    command = state.read(u32(0x2AA5A + s16(low16(frame.target_x))), 2)
    frame = _movement_move(state, frame, 'target_x', command, 16)
    return _movement_move(state, frame, 'target_x', low16(frame.target_x) | 0x2000, 16)


def _duel_rule_motion_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2AA14 true shared tail: live WORD save/readback around one physical RNG call."""
    frame = _postbattle_bit_fields(frame, bool(frame.roster.byte(24) & 8))
    state.sr = (state.sr & 65504) | frame.status
    if frame.status & 4:
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) ^ 0xC00, 16)
    stack = frame.stack_cursor.advance(-2)
    stack.set_word(0, low16(frame.target_x))
    frame = first_replace(frame, stack_cursor=stack)
    frame = _movement_test(state, frame, low16(frame.target_x), 16)
    frame = _duel_rule_call_fields(state, frame, 0x83D4, 0x2AA28)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)
    restored = frame.stack_cursor.word()
    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
    frame = _movement_move(state, frame, 'target_x', restored, 16)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 14, 16)
    if frame.status & 4:
        frame = _movement_move(state, frame, 'target_x', 0, 16)
    return frame


def _duel_rule_retreat_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """The original4F4 tail probes special before falling back to400 motion."""
    frame = _duel_rule_call_fields(state, frame, 0x2AA36, 0x2A4F8)
    frame = _movement_test(state, frame, low16(frame.target_x), 16)
    if not frame.status & 4:
        return frame
    frame = _movement_move(state, frame, 'target_x', 0x400, 16)
    return _duel_rule_motion_fields(state, frame)


def _duel_rule_distant_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """506 tail: stochastic special gate and the retained D3 direction."""
    frame = _duel_rule_call_fields(state, frame, 0x83D4, 0x2A50C)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 31, 16)
    if not frame.status & 4:
        frame = _duel_rule_call_fields(state, frame, 0x2AA36, 0x2A518)
    frame = _movement_test(state, frame, low16(frame.target_x), 16)
    if not frame.status & 4:
        return frame
    frame = _movement_test(state, frame, low16(frame.count), 16)
    if frame.status & 8:
        return _duel_rule_retreat_fields(state, frame)
    frame = _movement_move(state, frame, 'target_x', 0x800, 16)
    return _duel_rule_motion_fields(state, frame)


def _duel_rule_pressure_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5A0 contact/pressure path, including the original extra contact call."""
    frame = _duel_rule_call_fields(state, frame, 0x2A22E, 0x2A5A4)
    contact = bool(frame.status & 1)
    frame = _movement_test(state, frame, low16(frame.count), 16)
    negative = bool(frame.status & 8)
    if contact and not negative:
        return choose_duel_random_motion_fields(state, frame)
    if negative:
        frame = _duel_rule_call_fields(state, frame, 0x2AA36, 0x2A5AE)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) | 0x400, 16)
    else:
        frame = _duel_rule_call_fields(state, frame, 0x83D4, 0x2A5C0)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 1, 16)
        if not frame.status & 4:
            frame = _duel_rule_call_fields(state, frame, 0x2AA36, 0x2A5CA)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) | 0x800, 16)
    return _duel_rule_motion_fields(state, frame)


def execute_duel_rule_fields(state: SceneState,
        frame: FirstDeploymentFrame, entry: int) -> FirstDeploymentFrame:
    """Six original executor vectors; tails return to the existing caller slot."""
    frame = _resource_cost_frame(state, frame, entry)
    if entry in (0x2A32C, 0x2A338):
        frame = _duel_rule_call_fields(state, frame, 0x83D4, 0x2A4D0)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 63, 16)
        if not frame.status & 4:
            frame = _duel_rule_call_fields(state, frame, 0x2AA36, 0x2A4DC)
        frame = _movement_test(state, frame, low16(frame.target_x), 16)
        if not frame.status & 4:
            return frame
        frame = _duel_rule_call_fields(state, frame, 0x2A22E, 0x2A4E6)
        if not frame.status & 1:
            return _duel_rule_distant_fields(state, frame)
        frame = _movement_test(state, frame, low16(frame.count), 16)
        if not frame.status & 8:
            frame = _movement_compare(state, frame, low16(frame.unit), 0xFFFD, 16)
            if not frame.status & 1:
                return choose_duel_random_motion_fields(state, frame)
        return _duel_rule_retreat_fields(state, frame)
    if entry in (0x2A330, 0x2A334):
        frame = _duel_rule_call_fields(state, frame, 0x2A22E, 0x2A546)
        contact = bool(frame.status & 1)
        frame = _movement_test(state, frame, low16(frame.count), 16)
        negative = bool(frame.status & 8)
        if not contact:
            if negative:
                return _duel_rule_retreat_fields(state, frame)
            frame = _movement_move(state, frame, 'target_x', 0x800, 16)
            return _duel_rule_motion_fields(state, frame)
        if not negative:
            frame = _movement_compare(state, frame, low16(frame.unit), 0xFFFD, 16)
            if not frame.status & 1:
                frame = _duel_rule_call_fields(state, frame, 0x83D4, 0x2A560)
                frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 1, 16)
                if not frame.status & 4:
                    return choose_duel_opponent_special_fields(state, frame)
                return choose_duel_random_motion_fields(state, frame)
        frame = _movement_move(state, frame, 'target_x', 0x400, 16)
        return _duel_rule_motion_fields(state, frame)
    if entry == 0x2A33C:
        return _duel_rule_pressure_fields(state, frame)
    if entry == 0x2A340:
        frame = _postbattle_bit_fields(frame, bool(frame.candidates.byte(2) & 128))
        state.sr = (state.sr & 65504) | frame.status
        if not frame.status & 4:
            frame = _duel_rule_call_fields(state, frame, 0x2A52A, 0x2A5DE)
            frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) | 0x800, 16)
            return _duel_rule_motion_fields(state, frame)
        frame = _duel_rule_call_fields(state, frame, 0x2A26C, 0x2A5EA)
        if not frame.status & 1:
            return _duel_rule_pressure_fields(state, frame)
        frame = _movement_move(state, frame, 'target_x', 0x400, 16)
        return _duel_rule_motion_fields(state, frame)
    if entry == 0x2A52A:
        return choose_duel_random_motion_fields(state, frame)
    if entry == 0x2AA36:
        return choose_duel_opponent_special_fields(state, frame)
    raise MovementContinuationBoundary(entry, frame, 'unowned duel executor instruction entry')


def _duel_rule_legacy_fields(state, context, frame=None):
    """Only observed old values project; missing A3-A6/X/SP never become defaults."""
    checked_duel_context(context,state)
    current=context.frame if frame is None else frame
    current.validate(state)
    if current.live is not None:
        actor_values=_duel_strategy_actor_values(first_replace(FirstDeploymentFrame.unobserved(),
            target_x=current.command,target_y=current.comparison,unit=current.distance,
            count=current.factor,distance=current.weapon_difference,choice=current.variation,
            offset_x=current.live.working_value,offset_y=current.live.response,
            controller=current.live.lookup.cursor()))
    else:
        from ..high_level_scene_flows.contexts_duel import DuelActorFrame
        actor_values=DuelActorFrame(current.command,current.comparison,current.distance,
            current.factor,current.weapon_difference,current.variation)
    return _duel_strategy_partial_fields(state,context.actor,context.opponent,actor_values)


def _duel_rule_legacy_projection(state, frame):
    """The old frame has no complete 8D/8A/X vocabulary; it remains a projection."""
    return DuelRuleFrame(frame.target_x,frame.target_y,frame.unit,frame.count,
        frame.distance,frame.choice).validate(state)

from ..high_level_scene_flows.business_duel import _duel_actor_store_fields
from ..high_level_main_flows.business_movement_support import (
    _movement_move_long, _movement_test_long, _movement_compare_address,
    _movement_binary_flags, _movement_multiply_word, _movement_save_longs, _movement_restore_longs,
)


def _duel_action_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """One actual child LONG; complete unique scene/math helpers only."""
    if target==0x83D4:
        return _duel_strategy_call_fields(state,frame,target,continuation)
    def child(memory,entered):
        if target==0x27ABE:
            return multiply_duel_weight_fields(state,entered)
        if target==0x27AE6:
            return prepare_duel_combat_statistics_fields(state,entered)
        if target==0x27882:
            return toggle_duel_turn_fields(state,entered)
        if target==0x35760:
            from ..high_level_main_flows.business_movement_support import signed_divmod_fields
            return signed_divmod_fields(state,entered)
        from ..high_level_scene_flows.business_duel import (
            choose_duel_status_text_fields, wait_active_duel_action_fields,
            wait_either_duel_action_fields, clear_duel_text_plane_fields)
        if target==0x28228:
            return choose_duel_status_text_fields(state,entered)
        if target==0x2777A:
            return wait_active_duel_action_fields(state,entered)
        if target==0x277B8:
            return wait_either_duel_action_fields(state,entered)
        if target==0x27D76:
            return clear_duel_text_plane_fields(state,entered)
        raise MovementContinuationBoundary(target,entered,'actual duel action child is not restored')
    return _presentation_call_fields(BattlePresentationMemory(state),frame,continuation,child)


def _duel_action_second_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, bool]:
    """Each source occurrence rereads actual7018 and produces its own TST flags."""
    frame=_movement_test(state,frame,state.read(0x00FF7018,2),16)
    return frame,bool(frame.status&8)


def toggle_duel_turn_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """27882 two actual BYTE gates, then the original WORD EORI RMW."""
    frame=_resource_cost_frame(state,frame,0x27882)
    for address in (0x00FF700A,0x00FF700B):
        frame=_movement_compare(state,frame,state.read(address,1),3,8)
        if frame.status&4:
            return frame
    value=state.read(0x00FF7018,2)^0x8000
    from ..high_level_scene_flows.business_duel import _duel_scene_store_fields
    return _duel_scene_store_fields(state,frame,0x00FF7018,value)


def multiply_duel_weight_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """27ABE extends the one existing SWAP-stitched pure product rule to full ABI."""
    frame=_resource_cost_frame(state,frame,0x27ABE)
    value=frame.target_y
    frame=_movement_compare_address(state,frame,value,0x10000)
    product,response,conditions=_weight_fields(value,low16(frame.count),frame.offset_y)
    frame=first_replace(frame,target_y=product,offset_y=response)
    if value<0x10000:
        return _movement_test_long(state,frame,product)
    status=(17 if conditions.carry else 0)|(8 if conditions.negative else 0)|\
        (4 if conditions.zero else 0)|(2 if conditions.overflow else 0)
    state.sr=(state.sr&65504)|status
    return first_replace(frame,status=status)


def _duel_action_add_memory_byte_fields(state: SceneState, frame: FirstDeploymentFrame,
        view: Table, offset: Word) -> FirstDeploymentFrame:
    """Two actual statistics ADDQ.B1 sites share one prior-read/write operation."""
    value=view.byte(offset)
    frame,value=_movement_binary_flags(state,frame,value,1,8)
    view.set_byte(offset,value)
    return frame


def prepare_duel_combat_statistics_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """27AE6 physical indexed tables publish actual A3/A4/A5 and D5/D6."""
    frame=_resource_cost_frame(state,frame,0x27AE6)
    frame=first_replace(frame,scan=state.table_at(0xFFFFC300).cursor(),
        scratch=state.table_at(0xFFFFC200).cursor())
    frame=first_replace(frame,scan=frame.scan.advance(s16(low16(frame.target_y))),
        scratch=frame.scratch.advance(s16(low16(frame.target_y))))
    frame=_duel_actor_store_fields(state,frame,frame.candidates,0x39,frame.scan.byte(0),8)
    frame=_duel_actor_store_fields(state,frame,frame.candidates,0x33,frame.scratch.byte(0),8)
    frame=_duel_action_add_memory_byte_fields(state,frame,frame.candidates,0x33)
    frame=first_replace(frame,opponent=state.table_at(0xFFFFC200).cursor())
    frame=first_replace(frame,opponent=frame.opponent.advance(s16(low16(frame.target_x))))
    frame=_duel_actor_store_fields(state,frame,frame.roster,0x33,frame.opponent.byte(0),8)
    frame=_duel_action_add_memory_byte_fields(state,frame,frame.roster,0x33)
    frame=_scene_render_asl_word(SceneRefreshMemory(state),frame,'target_x',low16(frame.target_x),1)
    frame=_scene_render_asl_word(SceneRefreshMemory(state),frame,'target_y',low16(frame.target_y),1)
    frame=first_replace(frame,opponent=state.table_at(0xFFFFB000).cursor(),
        scratch=state.table_at(0xFFFFB600).cursor())
    frame=first_replace(frame,opponent=frame.opponent.advance(s16(low16(frame.target_y))),
        scratch=frame.scratch.advance(s16(low16(frame.target_y))))
    frame=_duel_actor_store_fields(state,frame,frame.candidates,0x34,frame.candidates.word(0x1C))
    frame=_duel_actor_store_fields(state,frame,frame.candidates,0x36,frame.opponent.word(0))
    frame=_duel_actor_store_fields(state,frame,frame.candidates,0x30,frame.scratch.word(0))
    frame=first_replace(frame,scan=state.table_at(0xFFFFB600).cursor())
    frame=first_replace(frame,scan=frame.scan.advance(s16(low16(frame.target_x))))
    frame=_duel_actor_store_fields(state,frame,frame.roster,0x30,frame.scan.word(0))
    frame=_movement_move(state,frame,'target_x',frame.roster.word(0x1A),16)
    frame=_movement_move(state,frame,'target_y',frame.candidates.word(0x1A),16)
    frame=first_replace(frame,scan=state.table_at(0xFFFFC700).cursor())
    frame=first_replace(frame,scan=frame.scan.advance(s16(low16(frame.target_x))))
    frame=_movement_move(state,frame,'offset_x',frame.scan.byte(0),8)
    frame=_movement_move(state,frame,'offset_x',low16(frame.offset_x)&15,16)
    frame=first_replace(frame,scan=state.table_at(0xFFFFC700).cursor())
    frame=first_replace(frame,scan=frame.scan.advance(s16(low16(frame.target_y))))
    frame=_movement_move(state,frame,'offset_y',frame.scan.byte(0),8)
    frame=_movement_move(state,frame,'offset_y',low16(frame.offset_y)&15,16)
    return _duel_commit_sub_word_fields(state,frame,'offset_x',low16(frame.offset_y))


def _duel_action_random_message_fields(state: SceneState, frame: FirstDeploymentFrame,
        role: str) -> FirstDeploymentFrame:
    """Six closed random/status roles retain their distinct widths and tokens."""
    plans={
        'recovery':(0x276B2,1,0x25,0x1D,0x276CA),
        'attack_success':(0x27704,1,0x27,0x27,0x27720),
        'feint_open':(0x27818,3,0x0E,0x0E,0x2783C),
        'feint_reply':(0x2784A,3,0x31,0x31,0x2786E),
        'flee':(0x278A6,1,0x14,0x14,0x278C2),
        'special':(0x27904,3,0x18,0x18,0x2792A)}
    if role not in plans:
        raise ValueError('actual original random-message role required')
    random_return,mask,bias,subtract,message_return=plans[role]
    frame=_duel_action_call_fields(state,frame,0x83D4,random_return)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&mask,16)
    if mask==3:
        frame=_movement_compare(state,frame,low16(frame.target_x),3,16)
        if frame.status&4:
            if role=='special':
                frame=_movement_move_long(state,frame,'target_x',0)
            else:
                frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_add_word(state,frame,'target_x',bias)
    frame,second=_duel_action_second_fields(state,frame)
    if second:
        frame=_duel_commit_sub_word_fields(state,frame,'target_x',subtract)
        second_bias={'attack_success':0x0A,'feint_open':0x2E,'feint_reply':0x11,'flee':0x2C,'special':0x29}
        if role in second_bias:
            frame=_movement_add_word(state,frame,'target_x',second_bias[role])
    return _duel_action_call_fields(state,frame,0x28228,message_return)


def _duel_action_nonlocal_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> tuple[str, FirstDeploymentFrame]:
    """Actual MOVE.L(A7)+,D0 then fixed BRA26D46; popped value is not a PC test."""
    discarded=frame.stack_cursor.long(0)
    frame=first_replace(frame,stack_cursor=frame.stack_cursor.advance(4))
    frame=_movement_move_long(state,frame,'target_x',discarded)
    return 'fade',frame


def _duel_action_terminal_fields(state: SceneState, frame: FirstDeploymentFrame,
        role: str) -> tuple[str, FirstDeploymentFrame]:
    """Three original terminal status/wait/result/pop tails, no default result."""
    plans={'attack':(0x0D,-1,0x27758,0x2775C,2,0x200),
        'flee':(0x16,1,0x278DC,0x278E0,0x300,3),
        'special':(0x1D,1,0x2796E,0x27972,0x100,1)}
    if role not in plans:
        raise ValueError('actual original terminal action role required')
    selection,step,message_return,wait_return,result_first,result_second=plans[role]
    frame=_movement_move(state,frame,'target_x',selection,16)
    frame,second=_duel_action_second_fields(state,frame)
    if second:
        if step==1:
            frame=_movement_add_word(state,frame,'target_x',1)
        else:
            frame=_duel_commit_sub_word_fields(state,frame,'target_x',1)
    frame=_duel_action_call_fields(state,frame,0x28228,message_return)
    frame=_duel_action_call_fields(state,frame,0x277B8,wait_return)
    from ..high_level_scene_flows.business_duel import _duel_scene_store_fields
    frame=_duel_scene_store_fields(state,frame,0x00FF70F0,result_first)
    frame,second=_duel_action_second_fields(state,frame)
    if second:
        frame=_duel_scene_store_fields(state,frame,0x00FF70F0,result_second)
    return _duel_action_nonlocal_fields(state,frame)


def _recover_after_duel_attack_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> tuple[str, FirstDeploymentFrame]:
    """276AC rejected/blocked attack's status/toggle/wait/recovery timer path."""
    frame=_duel_action_random_message_fields(state,frame,'recovery')
    frame=_duel_action_call_fields(state,frame,0x27882,0x276CE)
    frame=_duel_action_call_fields(state,frame,0x2777A,0x276D2)
    frame=_duel_action_call_fields(state,frame,0x27882,0x276D6)
    timer=frame.candidates.word(0x28)
    frame=_movement_compare(state,frame,timer,300,16)
    if frame.status&1:
        frame=_duel_actor_store_fields(state,frame,frame.candidates,0x28,300)
    return 'return',frame


def _duel_attack_variation_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """One rejection-sampled attack roll with the actual D1 MOVEM and PC tables."""
    while True:
        frame=_movement_save_longs(state,frame,('target_y',))
        frame=_duel_action_call_fields(state,frame,0x83D4,0x27638)
        frame=_movement_restore_longs(state,frame,('target_y',))
        frame=_movement_move(state,frame,'count',low16(frame.offset_x),16)
        if frame.status&4 or frame.status&8:
            frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&7,16)
            frame=_movement_compare(state,frame,low16(frame.target_x),4,16)
            if not frame.status&5:
                continue
            frame=_duel_commit_sub_word_fields(state,frame,'offset_x',0,True)
            frame=_movement_move_long(state,frame,'choice',0)
            value=state.read(u32(0x27660+s16(low16(frame.offset_x))),1)
            frame=_movement_move(state,frame,'choice',value,8)
            frame=_movement_add_word(state,frame,'choice',low16(frame.target_x))
            frame=_movement_move(state,frame,'choice',low16(frame.choice)&255,16)
        else:
            frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&15,16)
            frame=_movement_compare(state,frame,low16(frame.target_x),8,16)
            if not frame.status&5:
                continue
            frame=_movement_move_long(state,frame,'choice',0)
            value=state.read(u32(0x2767C+s16(low16(frame.offset_x))),1)
            frame=_movement_move(state,frame,'choice',value,8)
            frame=_movement_add_word(state,frame,'choice',low16(frame.target_x))
        return _movement_move(state,frame,'count',low16(frame.choice),16)


def resolve_duel_attack_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> tuple[str, FirstDeploymentFrame]:
    """27576/27586 entire attack, real arithmetic spills, rejection and nonlocal exit."""
    frame=_resource_cost_frame(state,frame,0x27586)
    frame=_movement_move(state,frame,'target_x',6,16)
    frame=_movement_move(state,frame,'target_y',frame.roster.word(0x1A),16)
    frame=_movement_compare(state,frame,low16(frame.target_y),frame.roster.word(0x20),16)
    if frame.status&4:
        frame=_movement_add_word(state,frame,'target_x',1)
    frame,second=_duel_action_second_fields(state,frame)
    if second:
        frame=_movement_move(state,frame,'target_x',0x23,16)
        frame=_movement_move(state,frame,'target_y',frame.roster.word(0x1A),16)
        frame=_movement_compare(state,frame,low16(frame.target_y),frame.roster.word(0x20),16)
        if frame.status&4:
            frame=_movement_add_word(state,frame,'target_x',1)
    frame=_duel_action_call_fields(state,frame,0x28228,0x275B6)
    frame=_duel_action_call_fields(state,frame,0x2777A,0x275BA)
    frame=_duel_action_call_fields(state,frame,0x27D76,0x275BE)
    frame=_movement_move(state,frame,'target_x',frame.roster.word(0x1A),16)
    frame=_movement_move(state,frame,'target_y',frame.candidates.word(0x1A),16)
    frame=_duel_action_call_fields(state,frame,0x27AE6,0x275CA)
    frame=_movement_move(state,frame,'target_x',frame.candidates.word(0x38),16)
    frame=_movement_move_long(state,frame,'target_y',100)
    frame=_duel_commit_sub_word_fields(state,frame,'target_y',low16(frame.target_x))
    frame=_movement_multiply_word(state,frame,'target_y',frame.roster.word(0x30))
    frame=_movement_move(state,frame,'count',frame.roster.word(0x32),16)
    frame=_duel_action_call_fields(state,frame,0x27ABE,0x275E0)
    frame=_movement_move(state,frame,'count',frame.candidates.word(0x36),16)
    frame=_duel_action_call_fields(state,frame,0x27ABE,0x275E8)
    frame=_movement_save_longs(state,frame,('target_y',))
    frame=_movement_move_long(state,frame,'target_y',0)
    frame=_movement_move(state,frame,'target_y',frame.candidates.word(0x30),16)
    frame=_movement_multiply_word(state,frame,'target_y',frame.candidates.word(0x32))
    frame=_movement_move(state,frame,'count',frame.candidates.word(0x34),16)
    frame=_duel_action_call_fields(state,frame,0x27ABE,0x275FE)
    frame=_movement_test(state,frame,state.read(0xFFFFEFD2,2),16)
    difficulty=60
    if not frame.status&4:
        frame=_movement_compare(state,frame,state.read(0xFFFFEFD2,2),2,16)
        difficulty=100 if frame.status&4 else 80
    frame=_movement_move(state,frame,'count',difficulty,16)
    frame=_duel_action_call_fields(state,frame,0x27ABE,0x27628)
    frame=_movement_move_long(state,frame,'unit',frame.target_y)
    frame=_movement_restore_longs(state,frame,('target_y',))
    frame=_duel_attack_variation_fields(state,frame)
    frame=_duel_action_call_fields(state,frame,0x27ABE,0x27688)
    frame=_movement_save_longs(state,frame,('unit',))
    frame=_movement_move_long(state,frame,'unit',10)
    frame=_duel_action_call_fields(state,frame,0x35760,0x27694)
    frame=_movement_restore_longs(state,frame,('unit',))
    frame=_movement_test_long(state,frame,frame.unit)
    if not frame.status&4:
        frame=_duel_action_call_fields(state,frame,0x35760,0x276A4)
        frame=_movement_compare(state,frame,low16(frame.target_y),1,16)
        if frame.status&1:
            return _recover_after_duel_attack_fields(state,frame)
    frame,second=_duel_action_second_fields(state,frame)
    blocked=state.read(0xFFFFEF7E if second else 0xFFFFEF7F,1)
    frame=_movement_test(state,frame,blocked,8)
    if not frame.status&4:
        return _recover_after_duel_attack_fields(state,frame)
    frame=_duel_action_random_message_fields(state,frame,'attack_success')
    frame=_duel_action_call_fields(state,frame,0x27882,0x27724)
    frame=_duel_action_call_fields(state,frame,0x2777A,0x27728)
    frame=_duel_action_call_fields(state,frame,0x27882,0x2772C)
    frame=_movement_move(state,frame,'target_x',frame.roster.word(0x18),16)
    frame=_movement_move(state,frame,'target_y',frame.candidates.word(0x18),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&0xF7FF,16)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&0x800,16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)|low16(frame.target_y),16)
    frame=_duel_actor_store_fields(state,frame,frame.candidates,0x18,low16(frame.target_x))
    frame=_duel_action_call_fields(state,frame,0x27D76,0x27746)
    return _duel_action_terminal_fields(state,frame,'attack')


def perform_duel_feint_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> tuple[str, FirstDeploymentFrame]:
    """2757A/27812 two messages, true turn toggles and900 opponent recovery."""
    frame=_resource_cost_frame(state,frame,0x27812)
    frame=_duel_action_random_message_fields(state,frame,'feint_open')
    frame=_duel_action_call_fields(state,frame,0x2777A,0x27840)
    frame=_duel_action_call_fields(state,frame,0x27D76,0x27844)
    frame=_duel_action_random_message_fields(state,frame,'feint_reply')
    frame=_duel_action_call_fields(state,frame,0x27882,0x27872)
    frame=_duel_action_call_fields(state,frame,0x2777A,0x27876)
    frame=_duel_action_call_fields(state,frame,0x27882,0x2787A)
    frame=_duel_actor_store_fields(state,frame,frame.candidates,0x28,900)
    return 'return',frame


def flee_duel_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> tuple[str, FirstDeploymentFrame]:
    """2757E/278A0 original flee messages and actual300/3 result/pop tail."""
    frame=_resource_cost_frame(state,frame,0x278A0)
    frame=_duel_action_random_message_fields(state,frame,'flee')
    frame=_duel_action_call_fields(state,frame,0x2777A,0x278C6)
    frame=_duel_action_call_fields(state,frame,0x27D76,0x278CA)
    return _duel_action_terminal_fields(state,frame,'flee')


def finish_special_duel_action_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> tuple[str, FirstDeploymentFrame]:
    """27582/278FE special BYTE BSET, status chain and100/1 actual exit."""
    frame=_resource_cost_frame(state,frame,0x278FE)
    frame=_duel_action_random_message_fields(state,frame,'special')
    frame=_duel_action_call_fields(state,frame,0x2777A,0x2792E)
    previous=frame.roster.byte(2)
    frame=_postbattle_bit_fields(frame,bool(previous&8))
    state.sr=(state.sr&65504)|frame.status
    frame.roster.set_byte(2,previous|8)
    frame=_duel_action_call_fields(state,frame,0x27D76,0x27938)
    frame=_movement_move(state,frame,'target_x',0x1C,16)
    frame,second=_duel_action_second_fields(state,frame)
    if second:
        frame=_movement_move(state,frame,'target_x',0x1B,16)
    frame=_duel_action_call_fields(state,frame,0x28228,0x2794C)
    frame=_duel_action_call_fields(state,frame,0x27882,0x27950)
    frame=_duel_action_call_fields(state,frame,0x2777A,0x27954)
    frame=_duel_action_call_fields(state,frame,0x27882,0x27958)
    frame=_duel_action_call_fields(state,frame,0x27D76,0x2795C)
    return _duel_action_terminal_fields(state,frame,'special')


def execute_indexed_duel_action_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int) -> tuple[str, FirstDeploymentFrame]:
    """Only original named executable vectors/bodies; no instruction dispatch VM."""
    if target in (0x27576,0x27586):
        return resolve_duel_attack_fields(state,frame)
    if target in (0x2757A,0x27812):
        return perform_duel_feint_fields(state,frame)
    if target in (0x2757E,0x278A0):
        return flee_duel_fields(state,frame)
    if target in (0x27582,0x278FE):
        return finish_special_duel_action_fields(state,frame)
    raise MovementContinuationBoundary(target,frame,'actual indexed action entry is not owned')


def _duel_action_legacy_fields(state: SceneState, observation,
        target: int, sole_core: str) -> FirstDeploymentFrame:
    """A six-value action context is not the full current D/A/CCR/X/SP contract."""
    from ..high_level_scene_flows.business_duel import _duel_scene_legacy_context_fields
    if type(observation) is DuelTurnContext:
        checked_duel_context(observation,state)
        if observation.frame.live is not None:
            return _duel_scene_legacy_context_fields(state,observation.frame.live,target,sole_core)
        values=observation.frame
        entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=values.command,
            target_y=values.comparison,unit=values.distance,count=values.factor,
            distance=values.weapon_difference,choice=values.variation,
            roster=observation.actor.cursor(),candidates=observation.opponent.cursor())
        raise MovementContinuationBoundary(target,entered,
            'old six-value action lacks current D5/D6/A2-A6/CCR-X/SP; use '+sole_core)
    return _duel_scene_legacy_context_fields(state,observation,target,sole_core)
