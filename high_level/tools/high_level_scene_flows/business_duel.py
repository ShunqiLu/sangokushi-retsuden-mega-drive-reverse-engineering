"""Original duel setup, live actor rules, input panels and scene orchestration.

These are logical Python drafts of the selected multi-segment source flows.
Fixed-width operations, repeated live reads and original failures are retained.
The external hardware and unresolved action handlers must supply real effects;
an unavailable service stops with Boundary, never a fabricated successful RTS.
"""
from dataclasses import replace

from .domain import (
    SceneState, Word, Long, Table, Cursor, Boundary, uint, u8, u16, u32,
    s8, s16, low8, low16, high16, replace_byte, replace_word,
    swap_words, negative_word, negative_long, divu_retained,
)
from .contexts_duel import (
    DuelControlContext, DuelGlyphContext, DuelActorContext, DuelActorResult,
    DuelContact, DuelProbability, DuelAIContext, DuelAIResult,
    DuelActionContext, DuelActionResult, DuelLaneResult, DuelSpriteResult,
    DuelSceneContext, DuelSceneResult, DuelRetainedValues, DuelActorFrame,
    DuelRenderResult,
    DuelPreparationContext, DuelPreparationResult,
    DuelOverrideResult, DuelInitializationContext, DuelInitializationResult,
    DuelTurnFrame, DuelConditionObservation, DuelTurnOutcome, checked_duel_turn,
    DuelContinuationBoundary,
    checked_duel_action_outcome,
    DuelLoadoutOutcome,
)


def _live_table(state, value):
    if not isinstance(value, Table) or value.state is not state:
        raise ValueError('live same-state Table required')
    return value


def _live_cursor(state, value):
    if not isinstance(value, Cursor) or value.state is not state:
        raise ValueError('live same-state Cursor required')
    return value


def _actor_word(value, word):
    """A partial write cannot manufacture the unknown retained upper WORD."""
    return None if value is None else replace_word(value, word)


def _actor_byte(value, byte):
    return None if value is None else replace_byte(value, byte)


def _actor_reframe(base, command, comparison, distance, factor, weapon_difference,
        variation, *, working_value=None, response=None, lookup=None):
    """Same actor algorithm, preserving explicitly supplied current extra values."""
    if type(base) is not DuelActorFrame:
        raise ValueError('actual actor field source required')
    return DuelActorFrame(command, comparison, distance, factor, weapon_difference,
        variation, base.working_value if working_value is None else working_value,
        base.response if response is None else response,
        base.lookup if lookup is None else lookup).validate()


def _turn_actor_values(frame):
    return DuelActorFrame(frame.command, frame.comparison, frame.distance, frame.factor,
        frame.weapon_difference, frame.variation, frame.working_value, frame.response,
        frame.lookup).validate()


def _turn_from_actor(state, original, fields, actor, opponent, stack):
    checked_duel_turn(original, state)
    fields.validate()
    if not fields.complete or fields.working_value is None or fields.response is None or fields.lookup is None:
        raise Boundary('complete duel algorithm omitted current working/response/lookup return')
    return DuelTurnFrame(fields.command, fields.comparison, fields.distance, fields.factor,
        fields.weapon_difference, fields.working_value, fields.response, fields.variation,
        actor, opponent, fields.lookup, stack,
        DuelConditionObservation(None, None, None, None)).validate(state)


def _actor_input_frame(context):
    if type(context) is not DuelActorContext:
        raise ValueError('actual actor input required')
    context.validate()
    if context.live is not None:
        current = checked_duel_turn(context.live, context.live.actor.state)
        if (current.command, current.comparison, current.distance, current.stack) != (
                context.command, context.comparison, context.damage, context.stack):
            raise ValueError('actor observations must agree with actual full caller')
        return _turn_actor_values(current)
    retained = context.retained
    return DuelActorFrame(context.command, context.comparison, context.damage,
        retained.factor if retained is not None else None,
        retained.weapon_difference if retained is not None else None,
        retained.variation if retained is not None else None).validate()


def _actor_stack(state, frame, stack):
    if type(frame) is not DuelActorFrame:
        raise ValueError('actual current actor frame required')
    frame.validate()
    if stack is not None:
        return _live_cursor(state, stack)
    if frame.complete:
        raise Boundary('complete actor return needs the actual live stack cursor')
    return None


def _push_actor_longs(stack, values):
    if stack is None:
        return
    for value in values[::-1]:
        if value is None:
            raise Boundary('native saved actor value is unknown')
        uint(value, 32, 'actual saved actor value')
    for value in values[::-1]:
        stack.base = u32(stack.base - 4)
        stack.set_long(0, value)


def _pop_actor_longs(stack, count):
    return tuple(stack.next_long() for _ in range(count))


def _push_actor_pair_words(stack, command, comparison):
    if stack is None:
        return
    stack.base = u32(stack.base - 2)
    stack.set_word(0, low16(comparison))
    stack.base = u32(stack.base - 2)
    stack.set_word(0, low16(command))


def _pop_actor_pair_words(stack, command, comparison):
    if stack is not None:
        command, comparison = stack.next_word(), stack.next_word()
    return u32(s16(low16(command))), u32(s16(low16(comparison)))


def _duel_frame(state):
    state.set_status_word(0x2500)
    state.set_scalar('ram_f612_word', 0x700)
    while state.read(0xFFFFF612, 1) != 0:
        state.progress('duel_frame_low_byte_ack')


def _sound(state, command):
    from .business_reuse import enqueue_sound_command
    return enqueue_sound_command(state, uint(command, 8, 'sound command'))


def _random(state):
    from .business_reuse import step_random
    return step_random(state)


def _first_controls(state, controls):
    from .business_reuse import choose_first_duel_control
    result = choose_first_duel_control(state, controls.command, controls.mode)
    return DuelControlContext(result.command, result.mode_carrier)


def _second_controls(state, controls):
    from .business_reuse import choose_second_duel_control
    result = choose_second_duel_control(state, controls.command, controls.mode)
    return DuelControlContext(result.command, result.mode_carrier)


def _upload_longs(state, source, count_latch):
    source = _live_cursor(state, source)
    counter = uint(count_latch, 16, 'count latch')
    while True:
        state.mmio_write(0xC00000, 4, source.next_long())
        counter = u16(counter - 1)
        if counter == 0xFFFF:
            return source


def _upload_words(state, source, count_latch):
    source = _live_cursor(state, source)
    counter = uint(count_latch, 16, 'count latch')
    while True:
        state.mmio_write(0xC00000, 2, source.next_word())
        counter = u16(counter - 1)
        if counter == 0xFFFF:
            return source


def advance_duel_entry_palette(state: SceneState,
        preparation: DuelPreparationContext | None = None) -> DuelPreparationContext | None:
    """Missing full live-in is explicit before any palette or counter mutation."""
    entered = _duel_scene_legacy_context_fields(state, preparation, 0x26D86,
        'advance_duel_entry_palette_fields')
    advance_duel_entry_palette_fields(state, entered)
    return preparation


def show_active_duel_turn_label(state: SceneState) -> Long:
    return _duel_scene_legacy_context_fields(state,None,0x27506,'show_active_duel_turn_label_fields')


def wait_active_duel_action(state: SceneState,
                           controls: DuelControlContext = DuelControlContext()) -> DuelControlContext:
    return _duel_scene_legacy_context_fields(state,controls,0x2777A,'wait_active_duel_action_fields')


def wait_either_duel_action(state: SceneState,
                           controls: DuelControlContext = DuelControlContext()) -> DuelControlContext:
    return _duel_scene_legacy_context_fields(state,controls,0x277B8,'wait_either_duel_action_fields')


def configure_duel_weapon_motion(state: SceneState, actor: Table,
        frame: DuelActorFrame | None=None) -> DuelActorFrame | None:
    """Legacy observations project the sole live weapon-motion preparation."""
    entered=_duel_strategy_partial_fields(state,actor,None,frame)
    returned=configure_duel_weapon_motion_fields(state,entered)
    return None if frame is None else _duel_strategy_actor_values(returned)


def refresh_duel_actors(state: SceneState, frame: DuelActorFrame | None=None,
        stack: Cursor | None=None, caller_actor: Table | None=None,
        caller_opponent: Table | None=None) -> DuelRenderResult:
    """Legacy observations project the sole live two-actor renderer parent."""
    entered=_duel_strategy_partial_fields(state,caller_actor,caller_opponent,frame)
    if stack is not None:
        entered=first_replace(entered,stack_cursor=_live_cursor(state,stack))
    returned=refresh_duel_actors_fields(state,entered)
    return DuelRenderResult(_duel_strategy_actor_values(returned),returned.roster,
        returned.candidates,returned.stack_cursor).validate(state)


def upload_duel_officer_name(state: SceneState, officer: Word,
        colors: DuelGlyphContext,
        current: DuelInitializationResult | None = None) -> DuelGlyphContext | DuelInitializationResult:
    """The historical officer WORD cannot stand in for the actual D7 LONG."""
    uint(officer, 16, 'officer')
    colors.validate()
    entered = _duel_scene_legacy_context_fields(state, current, 0x27D1C,
        'upload_duel_officer_name_fields')
    returned = upload_duel_officer_name_fields(state, entered)
    return DuelGlyphContext(returned.target_x, returned.target_y, returned.count)


def upload_duel_glyph_strip(state: SceneState, source: Cursor,
        colors: DuelGlyphContext,
        current: DuelInitializationResult | None = None) -> DuelGlyphContext | DuelInitializationResult:
    """27D56 compatibility entry delegates only to its complete current core."""
    _live_cursor(state, source)
    colors.validate()
    entered = _duel_scene_legacy_context_fields(state, current, 0x27D56,
        'upload_duel_glyph_strip_fields')
    returned = upload_duel_glyph_strip_fields(state, entered)
    return DuelGlyphContext(returned.target_x, returned.target_y, returned.count)


def _expand_and_upload_duel_glyphs(state, source, destination, colors, current=None):
    """Old internal middle-entry observations retain no parallel font algorithm."""
    _live_cursor(state, source)
    _live_cursor(state, destination)
    colors.validate()
    entered = _duel_scene_legacy_context_fields(state, current, 0x27D5A,
        '_upload_duel_glyph_buffers_fields')
    returned = _upload_duel_glyph_buffers_fields(state, entered)
    return DuelGlyphContext(returned.target_x, returned.target_y, returned.count)


def clear_duel_text_plane(state: SceneState,
        frame: DuelActorFrame | None = None) -> DuelActorFrame | None:
    """Legacy numeric observations cannot invent the unobserved addresses/X/SP."""
    entered = FirstDeploymentFrame.unobserved()
    if frame is not None:
        if type(frame) is not DuelActorFrame:
            raise ValueError('actual clear-text frame required')
        frame.validate()
        entered = first_replace(entered, target_x=frame.command,
            target_y=frame.comparison, unit=frame.distance, count=frame.factor,
            distance=frame.weapon_difference, offset_x=frame.working_value,
            offset_y=frame.response, choice=frame.variation)
    returned = clear_duel_text_plane_fields(state, entered)
    return None if frame is None else _duel_strategy_actor_values(returned)


def choose_duel_two_option_menu(state: SceneState, choice: Table,
                                controls: DuelControlContext, *,
                                live: DuelTurnFrame | None = None) -> DuelControlContext:
    choice = _live_table(state, choice)
    controls.validate()
    current = _duel_legacy_menu_input(state, choice, controls, live)
    returned = choose_duel_two_option_menu_complete(state, current)
    return DuelControlContext(returned.command, returned.comparison).validate()


def _equipment_available(equipment, option):
    return equipment.word(_duel_menu_equipment_slot(option))!=0


def _choose_duel_equipment(state, choice, equipment, controls, live=None):
    choice = _live_table(state, choice)
    equipment = _live_table(state, equipment)
    controls.validate()
    current = _duel_legacy_menu_input(state, choice, controls, live)
    returned = _choose_duel_equipment_complete(state, equipment, current)
    return DuelControlContext(returned.command, returned.comparison).validate()


def choose_first_duel_equipment(state: SceneState, choice: Table,
                                controls: DuelControlContext, *,
                                live: DuelTurnFrame | None = None) -> DuelControlContext:
    return _choose_duel_equipment(state, choice, state.table(0xFF707A), controls, live)


def choose_second_duel_equipment(state: SceneState, choice: Table,
                                 controls: DuelControlContext, *,
                                 live: DuelTurnFrame | None = None) -> DuelControlContext:
    return _choose_duel_equipment(state, choice, state.table(0xFF70CA), controls, live)


def _duel_legacy_menu_input(state, choice, controls, live):
    if live is None:
        raise Boundary('loadout menu requires the actual current eight values, views and SP')
    checked_duel_turn(live, state)
    if (choice.base, controls.command, controls.mode) != (live.actor.base, live.command, live.comparison):
        raise ValueError('loadout observations must agree with current choice and values')
    return live


def _finish_duel_loadout_menu(state, frame):
    entered=_duel_menu_observations_to_fields(state,frame,0x27DF4)
    return _duel_menu_fields_to_observations(state,
        _duel_menu_adjust_memory_word_fields(state,entered,True))


def _highlight_duel_loadout_choice(state, frame, vertical_base):
    entered=_duel_menu_observations_to_fields(state,frame,0x27DDA)
    continuation=0x27DF4 if vertical_base==121 else 0x27ECA
    return _duel_menu_fields_to_observations(state,
        _duel_menu_loadout_highlight_fields(state,entered,vertical_base,continuation))


def choose_duel_two_option_menu_complete(state: SceneState,
        frame: DuelTurnFrame) -> DuelTurnFrame:
    entered=_duel_menu_observations_to_fields(state,frame,0x27D9C)
    return _duel_menu_fields_to_observations(state,
        choose_duel_two_option_menu_fields(state,entered))


def _choose_duel_equipment_complete(state, equipment, frame):
    equipment=_live_table(state,equipment)
    if equipment.base not in (0xFF707A,0xFF70CA):
        raise ValueError('actual first/second equipment view required')
    entered=_duel_menu_observations_to_fields(state,frame,
        0x27E06 if equipment.base==0xFF70CA else 0x27DFC)
    return _duel_menu_fields_to_observations(state,
        choose_duel_equipment_fields(state,entered,equipment.base==0xFF70CA))


def choose_first_duel_equipment_complete(state: SceneState,
        frame: DuelTurnFrame) -> DuelTurnFrame:
    entered=_duel_menu_observations_to_fields(state,frame,0x27DFC)
    return _duel_menu_fields_to_observations(state,
        choose_first_duel_equipment_fields(state,entered))


def choose_second_duel_equipment_complete(state: SceneState,
        frame: DuelTurnFrame) -> DuelTurnFrame:
    entered=_duel_menu_observations_to_fields(state,frame,0x27E06)
    return _duel_menu_fields_to_observations(state,
        choose_second_duel_equipment_fields(state,entered))


def choose_duel_action_menu(state: SceneState,
                            controls: DuelControlContext, *,
                            live: DuelTurnFrame | None = None) -> DuelControlContext:
    """Legacy observation of the unique full menu; missing live input stops."""
    if type(controls) is not DuelControlContext:
        raise ValueError('actual duel controls required')
    controls.validate()
    if live is None:
        raise Boundary('action menu requires current eight values, three views and entry stack')
    checked_duel_turn(live, state)
    if (controls.command, controls.mode) != (live.command, live.comparison):
        raise ValueError('menu observations must agree with the actual full caller')
    returned = choose_duel_action_menu_complete(state, live)
    return DuelControlContext(returned.command, returned.comparison).validate()


def _append_duel_menu_cursor(state, frame):
    entered=_duel_menu_observations_to_fields(state,frame,0x28F9C)
    return _duel_menu_fields_to_observations(state,
        append_duel_sprite_fields(state,entered))


def _duel_menu_highlight(state, frame, restricted):
    entered=_duel_menu_observations_to_fields(state,frame,0x27F40)
    return _duel_menu_fields_to_observations(state,
        _duel_action_menu_highlight_fields(state,entered,restricted))


def choose_duel_action_menu_complete(state: SceneState,
        frame: DuelTurnFrame) -> DuelTurnFrame:
    entered=_duel_menu_observations_to_fields(state,frame,0x27ED2)
    return _duel_menu_fields_to_observations(state,
        choose_duel_action_menu_fields(state,entered))


def decode_duel_byte_lanes(state: SceneState, source: Cursor,
        destination: Cursor, length: Word,
        repeat_value: Long = 0, pair_value: Long = 0, *,
        length_carrier: Long | None = None, count_carrier: Long | None = None,
        stack: Cursor | None = None) -> DuelLaneResult:
    """Same decoder with only explicit old observations; missing ABI stays unknown."""
    entered = _duel_lane_legacy_fields(state, source, destination, length,
        repeat_value, pair_value, length_carrier, count_carrier, stack, 0x28012)
    return _duel_lane_fields_to_observations(decode_duel_byte_lanes_fields(state, entered))


def decode_duel_byte_lane(state: SceneState, source: Cursor,
        destination: Cursor, length: Word,
        repeat_value: Long = 0, pair_value: Long = 0, *,
        length_carrier: Long | None = None,
        count_carrier: Long | None = None) -> DuelLaneResult:
    """Historical one-lane view projects the one full four-kind lane decoder."""
    entered = _duel_lane_legacy_fields(state, source, destination, length,
        repeat_value, pair_value, length_carrier, count_carrier, None, 0x2801E)
    return _duel_lane_fields_to_observations(decode_duel_byte_lane_fields(state, entered))


def choose_duel_status_text(state: SceneState, selection: Word,
                            retained: Long = 0) -> Long:
    uint(selection,16,'actual selected status WORD')
    uint(retained,32,'actual caller retained D0 LONG')
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=replace_word(retained,selection))
    return choose_duel_status_text_fields(state,entered).target_x


def scan_duel_thresholds(state: SceneState, value: Word, thresholds: Cursor) -> Word:
    """Historical WORD-only projection; missing actual retained fields stop before reads."""
    uint(value,16)
    thresholds=_live_cursor(state,thresholds)
    frame=first_replace(FirstDeploymentFrame.unobserved(),target_x=value,controller=thresholds)
    returned=scan_duel_thresholds_fields(state,frame)
    thresholds.base=returned.controller.base
    return low16(returned.target_y)


def append_duel_sprite(state: SceneState, x: Word, y: Word,
        pattern: Word, attributes: Word, frame: DuelActorFrame | None=None,
        stack: Cursor | None=None) -> DuelSpriteResult:
    """Historical observations project the one complete live emitter."""
    x,y,pattern,attributes=(uint(value,16) for value in (x,y,pattern,attributes))
    entered=_duel_strategy_partial_fields(state,None,None,frame)
    for name,value in (('target_x',x),('target_y',y),('unit',pattern),('count',attributes)):
        actual=entered.carrier(name)
        if actual is not None and low16(actual)!=value:
            raise ValueError('sprite arguments must agree with observed current fields')
        entered=first_replace(entered,**{name:value if actual is None else replace_word(actual,value)})
    if stack is not None:
        entered=first_replace(entered,stack_cursor=_live_cursor(state,stack))
    returned=append_duel_sprite_fields(state,entered)
    return DuelSpriteResult(returned.roster,state.read(0x00FF7000,2),low16(returned.offset_x),
        _duel_strategy_actor_values(returned),returned.stack_cursor,returned.candidates)


def measure_duel_weapon_contact(state: SceneState, actor: Table,
        opponent: Table, frame: DuelActorFrame | None=None) -> DuelContact:
    """Historical actor observations project one full-field contact algorithm."""
    entered=_duel_strategy_partial_fields(state,actor,opponent,frame)
    returned=measure_duel_weapon_contact_fields(state,entered)
    current=_duel_strategy_actor_values(returned)
    return DuelContact(low16(returned.unit),low16(returned.count),bool(returned.status&1),current)


def _ai_frame(frame, command=None, comparison=None, distance=None, factor=None, variation=None):
    return _actor_reframe(frame, frame.command if command is None else command,
        frame.comparison if comparison is None else comparison,
        frame.distance if distance is None else distance,
        frame.factor if factor is None else factor, frame.weapon_difference,
        frame.variation if variation is None else variation).validate()


def _duel_observed_move(frame, value, width):
    masked = value & ((1 << width) - 1)
    return replace(frame, conditions=DuelConditionObservation(False, masked == 0,
        bool(masked & (1 << (width - 1))), False))


def _duel_observed_comparison(frame, left, right, width):
    mask = (1 << width) - 1
    left, right = left & mask, right & mask
    difference = (left - right) & mask
    sign = 1 << (width - 1)
    return replace(frame, conditions=DuelConditionObservation(left < right,
        difference == 0, bool(difference & sign),
        bool((left ^ right) & (left ^ difference) & sign)))


def _duel_observed_bit(frame, value, bit):
    """BTST supplies only Z; other known/unknown observations stay current."""
    observed = frame.conditions
    return replace(frame, conditions=DuelConditionObservation(observed.carry,
        not bool(value & (1 << bit)), observed.negative, observed.overflow))


def _duel_call_frame(state, function, frame, *args):
    """Logical original BSR slot; no fabricated physical return token."""
    checked_duel_turn(frame, state)
    called = replace(frame, stack=frame.stack.advance(-4))
    returned = checked_duel_turn(function(state, *args, called), state)
    return replace(returned, stack=returned.stack.advance(4))


def _duel_enter_actor_call(stack):
    if stack is not None:
        stack.base = u32(stack.base - 4)


def _duel_leave_actor_call(stack):
    if stack is not None:
        stack.base = u32(stack.base + 4)


def _duel_complete_controls(state, second, frame):
    checked_duel_turn(frame, state)
    if type(second) is not bool:
        raise ValueError('actual input side required')
    returned = _second_controls(state, DuelControlContext(frame.command, frame.comparison)) if second else _first_controls(
        state, DuelControlContext(frame.command, frame.comparison))
    return replace(frame, command=returned.command, comparison=returned.mode,
        conditions=DuelConditionObservation(None, None, None, None))


def clear_duel_text_complete(state: SceneState, frame: DuelTurnFrame) -> DuelTurnFrame:
    checked_duel_turn(frame, state)
    fields = clear_duel_text_plane(state, _turn_actor_values(frame))
    current = _turn_from_actor(state, frame, fields, frame.actor, frame.opponent, frame.stack)
    return _duel_observed_move(current, 0x11111111, 32)


def update_duel_actor_complete(state: SceneState, frame: DuelTurnFrame) -> DuelTurnFrame:
    checked_duel_turn(frame, state)
    values = _turn_actor_values(frame)
    result = update_duel_actor(state, frame.actor, frame.opponent,
        DuelActorContext(frame.command, frame.comparison, frame.distance,
            values.retained, frame.stack, frame))
    return _turn_from_actor(state, frame, result.frame, result.actor, result.opponent, result.stack)


def refresh_duel_actors_complete(state: SceneState, frame: DuelTurnFrame) -> DuelTurnFrame:
    checked_duel_turn(frame, state)
    result = refresh_duel_actors(state, _turn_actor_values(frame), frame.stack,
        frame.actor, frame.opponent)
    return _turn_from_actor(state, frame, result.frame, result.actor, result.opponent, result.stack)


def choose_duel_ai_command_complete(state: SceneState, frame: DuelTurnFrame) -> DuelTurnFrame:
    checked_duel_turn(frame, state)
    values = _turn_actor_values(frame)
    result = choose_duel_ai_command(state, frame.actor, frame.opponent,
        DuelAIContext(frame.command, frame.comparison, low16(frame.response),
            low16(frame.variation), values.retained, frame.response, frame))
    if result.live is None:
        raise Boundary('full AI call omitted its actual live return')
    return checked_duel_turn(result.live, state)


def choose_duel_status_text_complete(state: SceneState, selection: Word,
        frame: DuelTurnFrame) -> DuelTurnFrame:
    checked_duel_turn(frame,state)
    uint(selection,16,'actual selected status WORD')
    entered=first_replace(FirstDeploymentFrame.unobserved(),target_x=replace_word(frame.command,selection))
    returned=choose_duel_status_text_fields(state,entered)
    # This known leaf only changes D0/A2/CCR: all other observed fields pass
    # through unchanged. No unknown high bits, stack or address value is made.
    return replace(frame,command=returned.target_x,lookup=returned.controller,
        conditions=DuelConditionObservation(bool(returned.status&1),bool(returned.status&4),
            bool(returned.status&8),bool(returned.status&2))).validate(state)


def show_active_duel_turn_label_complete(state: SceneState, frame: DuelTurnFrame) -> DuelTurnFrame:
    entered=_duel_scene_legacy_context_fields(state,frame,0x27506,'show_active_duel_turn_label_fields')
    return _duel_menu_fields_to_observations(state,show_active_duel_turn_label_fields(state,entered))


def wait_active_duel_action_complete(state: SceneState, frame: DuelTurnFrame) -> DuelTurnFrame:
    entered=_duel_scene_legacy_context_fields(state,frame,0x2777A,'wait_active_duel_action_fields')
    return _duel_menu_fields_to_observations(state,wait_active_duel_action_fields(state,entered))


def wait_either_duel_action_complete(state: SceneState, frame: DuelTurnFrame) -> DuelTurnFrame:
    entered=_duel_scene_legacy_context_fields(state,frame,0x277B8,'wait_either_duel_action_fields')
    return _duel_menu_fields_to_observations(state,wait_either_duel_action_fields(state,entered))


def _ai_random(state, frame, mask):
    from .business_reuse import _reuse_advance_random_pair
    random = _reuse_advance_random_pair(state)
    return _ai_frame(frame, command=replace_word(random.sample, low16(random.sample) & mask),
                     comparison=random.updated_state)


def _ai_override_result(frame, override):
    return DuelOverrideResult(_ai_frame(frame,
        variation=_actor_word(frame.variation, override)), override).validate()


def sample_duel_probability(state: SceneState, source_word: Word,
        frame: DuelActorFrame | None=None) -> DuelProbability:
    """One mask/threshold rule; partial callers do not manufacture RNG stack slots."""
    uint(source_word,16)
    entered=_duel_strategy_partial_fields(state,None,None,frame)
    entered=first_replace(entered,unit=source_word if entered.unit is None else replace_word(entered.unit,source_word))
    returned=sample_duel_probability_fields(state,entered)
    return DuelProbability(returned.target_x,low16(returned.unit),low16(returned.count),
        bool(returned.status&1),_duel_strategy_actor_values(returned))


def choose_duel_ai_timeout(state: SceneState, actor: Table, opponent: Table,
        command: Long, override: Word, frame: DuelActorFrame | None=None) -> DuelAIResult:
    """Historical timeout interface projects the sole complete original rule."""
    uint(command,32)
    uint(override,16)
    entered=_duel_strategy_partial_fields(state,actor,opponent,frame)
    entered=first_replace(entered,target_x=command,
        choice=override if entered.choice is None else replace_word(entered.choice,override))
    returned=choose_duel_ai_timeout_fields(state,entered)
    current=_duel_strategy_actor_values(returned)
    return DuelAIResult(current.command,current.comparison,low16(current.response),
        low16(current.variation),current.retained,current,current.response)


def _copy_duel_palette(state, source_base, destination_base):
    """Legacy two-address observations lack the real counter/CCR, so stop before writes."""
    entered=first_replace(FirstDeploymentFrame.unobserved(),
        controller=state.table_at(uint(source_base,32)),
        scan=state.table_at(uint(destination_base,32)).cursor())
    entered=_resource_cost_frame(state,entered,0x28BE0)
    return _duel_actor_palette_fields(state,entered,False).controller


def update_duel_actor(state: SceneState, actor: Table, opponent: Table,
        context: DuelActorContext=DuelActorContext()) -> DuelActorResult:
    """Historical observations project the one full actor turn, without fake fields."""
    current=_actor_input_frame(context)
    entered=_duel_strategy_partial_fields(state,actor,opponent,current)
    if context.stack is not None:
        entered=first_replace(entered,stack_cursor=_live_cursor(state,context.stack))
    returned=update_duel_actor_fields(state,entered)
    values=_duel_strategy_actor_values(returned)
    return DuelActorResult(values.command,values.comparison,values.distance,values,
        returned.roster,returned.candidates,returned.stack_cursor,values.response).validate()


def _apply_duel_strike(state, actor, opponent, frame, stack):
    """Legacy strike view consumes the sole inline phase; no invented BSR."""
    entered=_duel_strategy_partial_fields(state,actor,opponent,frame)
    if stack is not None:
        entered=first_replace(entered,stack_cursor=_live_cursor(state,stack))
    entered=_resource_cost_frame(state,entered,0x28C98)
    return _duel_strategy_actor_values(_duel_actor_strike_fields(state,entered))


def render_duel_actor(state: SceneState, actor: Table, opponent: Table,
        frame: DuelActorFrame | None=None, stack: Cursor | None=None) -> DuelRenderResult:
    """Historical render entry projects the same living/death and overlay algorithm."""
    entered=_duel_strategy_partial_fields(state,actor,opponent,frame)
    if stack is not None:
        entered=first_replace(entered,stack_cursor=_live_cursor(state,stack))
    returned=render_duel_actor_fields(state,entered)
    return DuelRenderResult(_duel_strategy_actor_values(returned),returned.roster,
        returned.candidates,returned.stack_cursor).validate(state)


def _render_duel_movement_overlay(state, actor, opponent, frame, stack):
    """Compatibility names only; bit-five controls animation, not overlay drawing."""
    entered=_duel_strategy_partial_fields(state,actor,opponent,frame)
    if stack is not None:
        entered=first_replace(entered,stack_cursor=_live_cursor(state,stack))
    entered=_resource_cost_frame(state,entered,0x28ED2)
    returned=_duel_actor_overlay_fields(state,entered)
    return DuelRenderResult(_duel_strategy_actor_values(returned),returned.roster,
        returned.candidates,returned.stack_cursor).validate(state)


def choose_duel_ai_override(state: SceneState, actor: Table, opponent: Table,
                            threshold_offset: Word,
                            frame: DuelActorFrame | None = None) -> Word | DuelOverrideResult:
    """One algorithm, with an old WORD observation or its current frame return."""
    current = DuelActorFrame() if frame is None else frame
    result = _choose_duel_ai_override_current(state, actor, opponent, threshold_offset, current)
    return result.override if frame is None else result


def _choose_duel_ai_override_current(state, actor, opponent, threshold_offset, frame):
    """Historical retained-value facade of one side-specific full-field strategy."""
    uint(threshold_offset,16)
    entered=_duel_strategy_partial_fields(state,actor,opponent,frame)
    entered=first_replace(entered,offset_y=threshold_offset if entered.offset_y is None else replace_word(entered.offset_y,threshold_offset))
    returned=choose_duel_ai_override_fields(state,entered)
    return DuelOverrideResult(_duel_strategy_actor_values(returned),low16(returned.choice)).validate()


def _sample_duel_live_mode_pair(state, source, threshold_offset, second):
    return _sample_duel_live_mode_values(state, source, threshold_offset,
                                          second, DuelActorFrame()).borrowed


def _sample_duel_live_mode_values(state, source, threshold_offset, second, frame):
    """Historical observations of the sole four-family repeated mode protocol."""
    uint(threshold_offset,16)
    entered=_duel_strategy_partial_fields(state,None,None,frame)
    entered=first_replace(entered,offset_y=threshold_offset if entered.offset_y is None else replace_word(entered.offset_y,threshold_offset))
    entered=_resource_cost_frame(state,entered,source)
    returned=_duel_strategy_live_mode_fields(state,entered,source,second)
    return DuelProbability(returned.target_x,low16(returned.unit),low16(returned.count),
        bool(returned.status&1),_duel_strategy_actor_values(returned))


def _ai_observed_result(frame, response, threshold_offset, override, live=None):
    frame = replace(frame, response=response)
    actual_override = low16(frame.variation) if frame.variation is not None else override
    returned_live = None
    if live is not None:
        returned_live = _turn_from_actor(live.actor.state, live, frame,
            live.actor, live.opponent, live.stack)
    return DuelAIResult(frame.command, frame.comparison, threshold_offset, actual_override,
                         frame.retained, frame, response, returned_live).validate()


def _ai_rule_frame(state, actor, opponent, frame, threshold_offset, target_address, live=None, tail=False):
    if frame.retained is None:
        raise Boundary('actual AI rule needs current six values, not a legacy WORD observation')
    supplied = None
    if live is not None:
        supplied = _turn_from_actor(state, live, frame, actor, opponent, live.stack)
        if not tail:
            supplied = replace(supplied, stack=supplied.stack.advance(-4))
    result = state.service_at(target_address, DuelActionContext(actor, opponent,
        DuelControlContext(frame.command, frame.comparison), threshold_offset, frame.retained,
        live=supplied))
    if type(result) is not DuelActionResult:
        raise Boundary('real AI rule must return the actual typed frame')
    result.validate()
    if result.discarded_continuation is not None:
        raise Boundary('ordinary AI rule returned an unexpected nonlocal continuation')
    if result.retained is None:
        raise Boundary('AI rule omitted its actual retained return')
    if supplied is not None:
        if result.live is None:
            raise Boundary('complete AI rule omitted its current full return')
        checked_duel_turn(result.live, state)
        returned_live = result.live if tail else replace(result.live, stack=result.live.stack.advance(4))
        return _turn_actor_values(returned_live), returned_live
    return _actor_reframe(frame, result.controls.command, result.controls.mode,
        result.retained.distance, result.retained.factor,
        result.retained.weapon_difference, result.retained.variation).validate(), None


def choose_duel_ai_command(state: SceneState, actor: Table, opponent: Table,
        context: DuelAIContext=DuelAIContext()) -> DuelAIResult:
    """Historical caller facade; no invented A3-A6/X/SP for incomplete duel contexts."""
    context.validate()
    if context.live is not None:
        checked_duel_turn(context.live,state)
        current=_turn_actor_values(context.live)
    else:
        retained=context.retained
        current=DuelActorFrame(context.command,context.comparison,
            retained.distance if retained is not None else None,
            retained.factor if retained is not None else None,
            retained.weapon_difference if retained is not None else None,
            retained.variation if retained is not None else None,response=context.response)
    entered=_duel_strategy_partial_fields(state,actor,opponent,current)
    returned=choose_duel_ai_command_fields(state,entered)
    current=_duel_strategy_actor_values(returned)
    return DuelAIResult(current.command,current.comparison,low16(current.response),
        low16(current.variation),current.retained,current,current.response)


def _stage_duel_words(state, source_base, command, rows, row_command):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,None,0x27010,'_duel_scene_packet_fields')


def _configure_duel_action_dialog(state, position, source):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,None,0x27492,'_duel_scene_dialog_fields')


def _configure_duel_dialog(state, position, source):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,None,0x27034,'_duel_scene_dialog_fields')


def _choose_duel_ai_panel(state, actor, opponent, controls, preparation=None):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,preparation,0x27b58,'_duel_scene_auto_loadout_fields')


def _choose_duel_side_loadout(state, second, controls, preparation=None):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,preparation,0x2702a,'prepare_duel_loadout_fields')


def _wait_duel_status_text(state, second, controls, preparation=None):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,preparation,0x272be,'prepare_duel_readiness_fields')


def _preparation_with_frame(state, preparation, frame, actor=None, opponent=None, stack=None):
    preparation.validate(state)
    response = preparation.response if frame.response is None else frame.response
    return DuelPreparationContext(frame, response,
        preparation.actor if actor is None else actor,
        preparation.opponent if opponent is None else opponent,
        preparation.stack if stack is None else stack).validate(state)


def _wait_complete_status(state, second, preparation):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,preparation,0x272be,'prepare_duel_readiness_fields')


def _commit_complete_duel_loadout(state, preparation, second):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,preparation,0x27152,'commit_duel_loadout_fields')


def _prepare_complete_second_status(state, preparation):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,preparation,0x272f0,'prepare_duel_readiness_fields')


def _consume_complete_first_duel_frame(state, preparation):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,preparation,0x27350,'begin_duel_combat_fields')


def _duel_from_preparation(state, preparation):
    preparation.validate(state)
    values = preparation.frame
    if values.working_value is None or values.response is None or values.lookup is None:
        raise Boundary('complete preparation must return its current D5/D6/A2, not initialization defaults')
    if values.response != preparation.response:
        raise ValueError('preparation response must agree with the current actor frame')
    return DuelTurnFrame(values.command, values.comparison, values.distance,
        values.factor, values.weapon_difference, values.working_value, values.response,
        values.variation, preparation.actor, preparation.opponent, values.lookup,
        preparation.stack, DuelConditionObservation(None, None, None, None)).validate(state)


def _duel_from_first_actor(state, result):
    if type(result) is not DuelActorResult:
        raise ValueError('the continuation needs the actual first actor return')
    result.validate()
    values = result.frame
    if values is None or not values.complete or values.working_value is None or values.lookup is None:
        raise Boundary('first actor did not return its actual current working value/lookup')
    if result.response is None or values.response != result.response:
        raise Boundary('first actor omitted its current response')
    return DuelTurnFrame(values.command, values.comparison, values.distance,
        values.factor, values.weapon_difference, values.working_value, result.response,
        values.variation, result.actor, result.opponent, values.lookup, result.stack,
        DuelConditionObservation(None, None, None, None)).validate(state)


def _begin_duel_combat_frame(state, frame, clear_text):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,frame,0x27350,'begin_duel_combat_fields')


def advance_duel_turn(state: SceneState, frame: DuelTurnFrame,
        clear_text: bool = True) -> DuelTurnOutcome:
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,frame,0x27350,'begin_duel_combat_fields')


def continue_after_first_duel_actor(state: SceneState,
        frame: DuelTurnFrame) -> DuelTurnOutcome:
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,frame,0x27396,'continue_after_first_duel_actor_fields')


def choose_duel_turn_action_complete(state: SceneState,
        frame: DuelTurnFrame) -> DuelTurnOutcome:
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,frame,0x27426,'choose_duel_turn_action_fields')


def continue_manual_duel_action(state: SceneState,
        frame: DuelTurnFrame) -> DuelTurnOutcome:
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,frame,0x274c2,'continue_manual_duel_action_fields')


def perform_selected_duel_action_complete(state: SceneState,
        frame: DuelTurnFrame) -> DuelTurnOutcome:
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,frame,0x27534,'perform_selected_duel_action_fields')


def show_terminal_duel_result_complete(state: SceneState,
        frame: DuelTurnFrame) -> DuelTurnOutcome:
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,frame,0x27990,'show_terminal_duel_result_fields')


def finish_duel_turn_scene(state: SceneState, frame: DuelTurnFrame) -> DuelTurnOutcome:
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,frame,0x26d46,'finish_duel_scene_fields')


def _initialization_values(state, current, *, frame=None, response=None,
        glyph_work=None, source=None, destination=None, glyph_source=None, stack=None):
    current.validate(state)
    preparation = current.preparation
    frame = preparation.frame if frame is None else frame
    actual_response = frame.response if response is None else response
    actual_working = frame.working_value if glyph_work is None else glyph_work
    actual_lookup = frame.lookup if glyph_source is None else glyph_source
    if actual_response is None or actual_working is None or actual_lookup is None:
        raise Boundary('initialization must consume the current actual frame, not an older glyph snapshot')
    frame = replace(frame, working_value=actual_working,
        response=actual_response, lookup=actual_lookup)
    return DuelInitializationResult(DuelPreparationContext(
        frame, actual_response,
        preparation.actor if source is None else source,
        preparation.opponent if destination is None else destination,
        preparation.stack if stack is None else stack), actual_working, actual_lookup).validate(state)


def _duel_call_initialization(state, function, current, *args):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,current,0x26db4,'_duel_scene_call_fields')


def _stage_complete_duel_packet(state, current, source_address, command, rows, row_command):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,current,0x26ff0,'_duel_scene_packet_fields')


def _duel_preparation_from_turn(state, frame):
    checked_duel_turn(frame, state)
    return DuelPreparationContext(_turn_actor_values(frame), frame.response,
        frame.actor, frame.opponent, frame.stack).validate(state)


def _advance_duel_loadout_palette(state, frame):
    preparation = advance_duel_entry_palette(state, _duel_preparation_from_turn(state, frame))
    return _duel_from_preparation(state, preparation)


def _configure_duel_loadout_motion(state, frame):
    fields = configure_duel_weapon_motion(state, frame.actor, _turn_actor_values(frame))
    return _turn_from_actor(state, frame, fields, frame.actor, frame.opponent, frame.stack)


def _choose_complete_status_text(state, selection, frame):
    return choose_duel_status_text_complete(state, selection, frame)


def _duel_loadout_ack(state, frame):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,frame,0x27060,'_duel_scene_frame_ack_fields')


def _stage_duel_loadout_packet(state, source_address, row_command, frame):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,frame,0x27098,'_duel_scene_packet_fields')


def choose_duel_loadout_complete(state: SceneState, second: bool,
        frame: DuelTurnFrame) -> DuelLoadoutOutcome:
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,frame,0x2702a,'prepare_duel_loadout_fields')


def _choose_complete_duel_loadout(state, second, preparation):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,preparation,0x2702a,'prepare_duel_loadout_fields')


def _prepare_complete_first_status(state, preparation):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,preparation,0x2729c,'prepare_duel_readiness_fields')


def prepare_duel_scene_first_frame(state: SceneState,
        context: DuelInitializationContext) -> DuelPreparationResult:
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,context,0x26db4,'initialize_duel_scene_fields')


def continue_automatic_duel_preparation(state: SceneState,
                                       preparation: DuelPreparationContext) -> DuelPreparationResult:
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,preparation,0x27b58,'_duel_scene_auto_loadout_fields')


def _initialize_duel_scene(state, context):
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,context,0x26db4,'initialize_duel_scene_fields')


def _finish_duel_scene(state, controls, actor_values):
    raise Boundary('this legacy partial observation lacks the actual current duel frame; use the complete core')


def _resolve_duel_pending_action(state, actor, opponent, controls, retained):
    raise Boundary('this legacy partial observation lacks the actual current duel frame; use the complete core')


def _choose_duel_command(state, controls, retained):
    # The source token is tested before choosing the actor and before both mode
    # reads.  High token bits participate in the WORD shift, not an ordinal clamp.
    raise Boundary('this legacy partial observation lacks the actual current duel frame; use the complete core')


def _show_duel_action_result(state, controls):
    # This original non-contiguous path rejoins the frame loop, not an extra RTS.
    raise Boundary('this legacy partial observation lacks the actual current duel frame; use the complete core')


def run_duel_scene(state: SceneState,
                    context: DuelSceneContext = DuelSceneContext()) -> DuelSceneResult:
    """Honest projection: the historical DTO omitted the current full ABI."""
    return _duel_scene_legacy_context_fields(state,context,0x26db4,'run_duel_scene_fields')


"""Root49: six sole duel strategy owners, complete actual retained fields.

Original decisions remain structured rules; cached code is evidence only, never
runtime instruction data. Widths, repeated reads and real call slots are kept.
"""

from .contexts_scene import FirstDeploymentFrame, first_replace, SceneRefreshMemory
from .business_scene import _scene_render_asl_word
from ..high_level_main_flows.business_movement_support import (
    _movement_move, _movement_move_long, _movement_test, _movement_test_long,
    _movement_compare, _movement_compare_address, _movement_add_word,
    _movement_binary_flags, _movement_fixed_shift_word,
)
from ..high_level_remaining_flows.business_city import (
    _resource_cost_frame, _duel_commit_sub_word_fields,
)
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
from ..high_level_battle_ai.business_actions import sample_battle_action_random_fields
from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
from ..high_level_gameplay_flow.business_battle import (
    _presentation_call_fields, _postbattle_bit_fields,
)
from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory


def _duel_strategy_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Only a genuine ordinary call writes its one original LONG return slot."""
    frame = _resource_cost_frame(state, frame, target)
    if target == 0x83D4:
        return sample_battle_action_random_fields(BattlePolicyMemory(state), frame, continuation)
    def algorithm(memory, entered):
        if target == 0x28F90:
            return scan_duel_thresholds_fields(memory.state, entered)
        if target == 0x2A5F4:
            return choose_duel_ai_override_fields(memory.state, entered)
        if target == 0x2AA00:
            return sample_duel_probability_fields(memory.state, entered)
        if target == 0x2AA60:
            return choose_duel_ai_timeout_fields(memory.state, entered)
        if target in (0x2A314,0x2A318,0x2A31C,0x2A320,0x2A324,0x2A328):
            from ..high_level_dynamic_flows.business_duel import choose_duel_profile_fields
            return choose_duel_profile_fields(memory.state,entered,target)
        raise MovementContinuationBoundary(target, entered,
            'actual indexed duel strategy target is not yet restored')
    return _presentation_call_fields(BattlePresentationMemory(state), frame,
        continuation, algorithm)


def _duel_strategy_probability_fields(state: SceneState, frame: FirstDeploymentFrame,
        table: int, continuation: int) -> FirstDeploymentFrame:
    """D6.W is signed only at addressing; the PC-selected full table stays live."""
    value = state.read(u32(table + s16(low16(frame.offset_y))), 2)
    frame = _movement_move(state, frame, 'unit', value, 16)
    return _duel_strategy_call_fields(state, frame, 0x2AA00, continuation)


def scan_duel_thresholds_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """28F90..28F9C: inclusive offset advance and live unsigned threshold scan."""
    frame = _resource_cost_frame(state, frame, 0x28F90)
    frame = _movement_move(state, frame, 'target_y', 0xFFFE, 16)
    while True:
        frame = _movement_add_word(state, frame, 'target_y', 2)
        threshold = frame.controller.word()
        frame = first_replace(frame, controller=frame.controller.advance(2))
        frame = _movement_compare(state, frame, low16(frame.target_x), threshold, 16)
        if low16(frame.target_x) < threshold:
            return frame


def measure_duel_weapon_contact_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2A22E..2A260: facing-adjusted weapon reach and original CMP borrow ABI."""
    facing_bit = 8
    frame = _resource_cost_frame(state, frame, 0x2A22E)
    frame = _movement_move(state, frame, 'target_y', frame.roster.word(12), 16)
    frame = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_y', low16(frame.target_y), 1)
    reach = state.read(u32(0x2A260 + s16(low16(frame.target_y))), 2)
    frame = _movement_move(state, frame, 'unit', reach, 16)
    frame = _postbattle_bit_fields(frame, bool(frame.roster.byte(24) & facing_bit))
    state.sr = (state.sr & 65504) | frame.status
    if frame.status & 4:
        frame = _duel_commit_sub_word_fields(state, frame, 'unit', 0, True)
    frame = _movement_add_word(state, frame, 'unit', frame.roster.word(14))
    frame = _duel_commit_sub_word_fields(state, frame, 'unit', frame.candidates.word(14))
    frame = _movement_move(state, frame, 'count', low16(frame.unit), 16)
    if frame.status & 8:
        frame = _duel_commit_sub_word_fields(state, frame, 'unit', 0, True)
    frame = _postbattle_bit_fields(frame, bool(frame.roster.byte(24) & facing_bit))
    state.sr = (state.sr & 65504) | frame.status
    if not frame.status & 4:
        frame = _duel_commit_sub_word_fields(state, frame, 'count', 0, True)
    limit = state.read(u32(0x2A266 + s16(low16(frame.target_y))), 2)
    return _duel_commit_sub_word_fields(state, frame, 'unit', limit)


def sample_duel_probability_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2AA00..2AA14: mask/threshold split, one genuine RNG and final CMP.W."""
    probability_mask = 7
    probability_shift = 4
    frame = _resource_cost_frame(state, frame, 0x2AA00)
    frame = _movement_move(state, frame, 'count', low16(frame.unit), 16)
    frame = _movement_move(state, frame, 'unit', low16(frame.unit) & probability_mask, 16)
    frame = _movement_fixed_shift_word(state, frame, 'count', probability_shift, True)
    frame = _duel_strategy_call_fields(state, frame, 0x83D4, 0x2AA0E)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & low16(frame.unit), 16)
    return _movement_compare(state, frame, low16(frame.target_x), low16(frame.count), 16)


def choose_duel_ai_timeout_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2AA60..2AA8E: late low-readiness escape; the other arm CLR.L only D0."""
    timer_bound = 0x1800
    mode_bound = 0x303
    timeout_command = 0x43
    frame = _resource_cost_frame(state, frame, 0x2AA60)
    timer = state.read(0x00FF70FA, 2)
    frame = _movement_compare(state, frame, timer, timer_bound, 16)
    if timer > timer_bound:
        mode = state.read(0x00FF700A, 2)
        frame = _movement_compare(state, frame, mode, mode_bound, 16)
        if mode == mode_bound:
            frame = _movement_move(state, frame, 'target_x', frame.roster.word(28), 16)
            readiness = low16(frame.target_x)
            opponent_readiness = frame.candidates.word(28)
            frame = _movement_compare(state, frame, readiness, opponent_readiness, 16)
            if readiness <= opponent_readiness:
                return _movement_move(state, frame, 'choice', timeout_command, 16)
    return _movement_move_long(state, frame, 'target_x', 0)


def _duel_strategy_live_mode_fields(state: SceneState, frame: FirstDeploymentFrame,
        branch: int, second: bool) -> FirstDeploymentFrame:
    """Four original low-readiness families share exactly the same live mode protocol."""
    mode_selector = 2
    if branch not in (0x2A72C, 0x2A7D8, 0x2A87C, 0x2A922) or type(second) is not bool:
        raise ValueError('original duel probability family required')
    table, first_return, second_return = {
        0x2A72C: (0x2A78A, 0x2A756, 0x2A784),
        0x2A7D8: (0x2A834, 0x2A802, 0x2A830),
        0x2A87C: (0x2A8DA, 0x2A8A6, 0x2A8D4),
        0x2A922: (0x2A980, 0x2A94C, 0x2A97A),
    }[branch]
    mode = state.read(0xFFFFEFD2, 2)
    frame = _movement_test(state, frame, mode, 16)
    if mode != 0:
        # TST and CMPI are separate reads, including the second probability arm.
        mode = state.read(0xFFFFEFD2, 2)
        frame = _movement_compare(state, frame, mode, mode_selector, 16)
        table += 48 if mode == mode_selector else 24
    if second:
        table += 12
    return _duel_strategy_probability_fields(state, frame, table,
        second_return if second else first_return)


def choose_duel_ai_override_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2A5F4's eight disjoint spans: side-specific readiness and strength policy."""
    tick_mask = 7
    first_opponent_bound = 51
    first_low_bound = 40
    first_high_bound = 70
    second_mid_bound = 50
    second_high_bound = 80
    offset_low_bound = 4
    offset_high_bound = 8
    first_low_opponent_mask = 1
    first_high_opponent_mask = 3
    first_low_or_mid_mask = 3
    first_high_or_mid_mask = 1
    first_high_weak_mask = 3
    command_40 = 0x40
    command_43 = 0x43
    command_42 = 0x42
    command_21 = 0x21
    frame = _resource_cost_frame(state, frame, 0x2A5F4)
    frame = _movement_move(state, frame, 'choice', 0, 16)
    frame = _movement_move(state, frame, 'target_y', state.read(0x00FF7008, 2), 16)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & tick_mask, 16)
    if not frame.status & 4:
        return frame
    frame = _movement_compare_address(state, frame, frame.roster.base, 0x00FF7050)
    if frame.status & 4:
        opponent_readiness = frame.candidates.word(28)
        frame = _movement_compare(state, frame, opponent_readiness, first_opponent_bound, 16)
        if opponent_readiness < first_opponent_bound:
            frame = _duel_strategy_call_fields(state, frame, 0x83D4, 0x2A620)
            frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & first_low_opponent_mask, 16)
            if frame.status & 4:
                return _movement_move(state, frame, 'choice', command_40, 16)
        else:
            frame = _duel_strategy_call_fields(state, frame, 0x83D4, 0x2A634)
            frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & first_high_opponent_mask, 16)
            if frame.status & 4:
                return _movement_move(state, frame, 'choice', command_40, 16)
            return frame
        frame = _movement_move(state, frame, 'unit', frame.candidates.word(30), 16)
        frame = _movement_move(state, frame, 'count', frame.roster.word(30), 16)
        frame = _movement_move(state, frame, 'target_y', frame.roster.word(28), 16)
        readiness = low16(frame.target_y)
        opponent_strength, own_strength = low16(frame.unit), low16(frame.count)
        frame = _movement_compare(state, frame, readiness, first_low_bound, 16)
        if readiness < first_low_bound:
            frame = _duel_strategy_call_fields(state, frame, 0x83D4, 0x2A68C)
            frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & first_low_or_mid_mask, 16)
            if not frame.status & 4:
                return _movement_move(state, frame, 'choice', command_43, 16)
            return frame
        frame = _movement_compare(state, frame, readiness, first_high_bound, 16)
        if readiness >= first_high_bound:
            frame = _movement_compare(state, frame, opponent_strength, own_strength, 16)
            if opponent_strength >= own_strength:
                frame = _duel_strategy_call_fields(state, frame, 0x83D4, 0x2A664)
                frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & first_high_or_mid_mask, 16)
                chosen = not frame.status & 4
            else:
                frame = _duel_strategy_call_fields(state, frame, 0x83D4, 0x2A67A)
                frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & first_high_weak_mask, 16)
                chosen = bool(frame.status & 4)
        else:
            frame = _movement_compare(state, frame, opponent_strength, own_strength, 16)
            if opponent_strength < own_strength:
                frame = _duel_strategy_call_fields(state, frame, 0x83D4, 0x2A664)
                frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & first_high_or_mid_mask, 16)
            else:
                frame = _duel_strategy_call_fields(state, frame, 0x83D4, 0x2A68C)
                frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & first_low_or_mid_mask, 16)
            chosen = not frame.status & 4
        return _movement_move(state, frame, 'choice', command_43, 16) if chosen else frame
    frame = _movement_move(state, frame, 'unit', frame.candidates.word(28), 16)
    frame = _movement_move(state, frame, 'count', frame.roster.word(28), 16)
    opponent_readiness, readiness = low16(frame.unit), low16(frame.count)
    frame = _movement_compare(state, frame, opponent_readiness, readiness, 16)
    if opponent_readiness < readiness:
        frame = _duel_strategy_probability_fields(state, frame, 0x2A9E2, 0x2A9D0)
        if frame.status & 1:
            return _movement_move(state, frame, 'choice', command_40, 16)
        frame = _duel_strategy_probability_fields(state, frame, 0x2A9EE, 0x2A9DC)
        return _movement_move(state, frame, 'choice', command_21, 16) if frame.status & 1 else frame
    frame = _movement_compare(state, frame, readiness, second_mid_bound, 16)
    if readiness >= second_mid_bound:
        frame = _movement_compare(state, frame, readiness, second_high_bound, 16)
        if readiness >= second_high_bound:
            return frame
        frame = _movement_move(state, frame, 'unit', frame.candidates.word(30), 16)
        frame = _movement_move(state, frame, 'count', frame.roster.word(30), 16)
        opponent_strength, own_strength = low16(frame.unit), low16(frame.count)
        frame = _movement_compare(state, frame, opponent_strength, own_strength, 16)
        if opponent_strength >= own_strength:
            frame = _duel_strategy_probability_fields(state, frame, 0x2A6B4, 0x2A6E2)
        else:
            frame = _duel_strategy_probability_fields(state, frame, 0x2A6F2, 0x2A706)
        if frame.status & 1:
            return _movement_move(state, frame, 'choice', command_43, 16)
        frame = _duel_strategy_probability_fields(state, frame, 0x2A6C0, 0x2A6EC)
        return _movement_move(state, frame, 'choice', command_40, 16) if frame.status & 1 else frame
    frame = _movement_move(state, frame, 'target_x', frame.candidates.word(30), 16)
    frame = first_replace(frame, controller=state.table_at(0x2A308).cursor())
    frame = _duel_strategy_call_fields(state, frame, 0x28F90, 0x2A718)
    opponent_offset = low16(frame.target_y)
    frame = _movement_compare(state, frame, opponent_offset, offset_low_bound, 16)
    if opponent_offset < offset_low_bound:
        branch = 0x2A922
    else:
        frame = _movement_compare(state, frame, opponent_offset, offset_high_bound, 16)
        if opponent_offset < offset_high_bound:
            branch = 0x2A87C
        elif opponent_offset == offset_high_bound:
            branch = 0x2A7D8
        else:
            branch = 0x2A72C
    frame = _duel_strategy_live_mode_fields(state, frame, branch, False)
    if frame.status & 1:
        return _movement_move(state, frame, 'choice', command_43, 16)
    frame = _duel_strategy_live_mode_fields(state, frame, branch, True)
    return _movement_move(state, frame, 'choice', command_42, 16) if frame.status & 1 else frame


def choose_duel_ai_command_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2A29A..2A308: cooldown, profile decision and true indexed tail transfer."""
    cooldown_step = 1
    cooldown_mask = 31
    cooldown_bias = 30
    opponent_zero_command = 0x100
    profile_shift = 1
    executor_shift = 2
    frame = _resource_cost_frame(state, frame, 0x2A29A)
    cooldown = frame.roster.word(34)
    frame = _movement_test(state, frame, cooldown, 16)
    if not frame.status & 4:
        frame, cooldown = _movement_binary_flags(state, frame, frame.roster.word(34), cooldown_step, 16, True)
        frame.roster.set_word(34, cooldown)
    frame = _movement_move(state, frame, 'target_x', frame.roster.word(28), 16)
    if frame.status & 4:
        frame.roster.set_word(2, low16(frame.target_x))
        frame = _movement_test(state, frame, low16(frame.target_x), 16)
        frame.roster.set_word(4, low16(frame.target_x))
        return _movement_test(state, frame, low16(frame.target_x), 16)
    frame = _movement_move(state, frame, 'target_x', frame.candidates.word(28), 16)
    if frame.status & 4:
        return _movement_move(state, frame, 'target_x', opponent_zero_command, 16)
    frame = _movement_test(state, frame, frame.roster.word(34), 16)
    if frame.status & 4:
        frame = _duel_strategy_call_fields(state, frame, 0x83D4, 0x2A2CC)
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & cooldown_mask, 16)
        frame = _movement_add_word(state, frame, 'target_x', cooldown_bias)
        frame.roster.set_word(34, low16(frame.target_x))
        frame = _movement_test(state, frame, low16(frame.target_x), 16)
        frame = _movement_move(state, frame, 'target_x', frame.roster.word(30), 16)
        frame = first_replace(frame, controller=state.table_at(0x2A308).cursor())
        frame = _duel_strategy_call_fields(state, frame, 0x28F90, 0x2A2E6)
        frame = _movement_move(state, frame, 'offset_y', low16(frame.target_y), 16)
        frame = _duel_strategy_call_fields(state, frame, 0x2A5F4, 0x2A2EC)
        frame = _duel_strategy_call_fields(state, frame, 0x2AA60, 0x2A2F0)
        frame = _movement_move(state, frame, 'target_x', low16(frame.choice), 16)
        frame = _movement_test(state, frame, low16(frame.target_x), 16)
        if not frame.status & 4:
            return frame
        frame = _movement_move(state, frame, 'target_y', low16(frame.offset_y), 16)
        frame = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_y', low16(frame.target_y), profile_shift)
        target = u32(0x2A314 + s16(low16(frame.target_y)))
        frame = _duel_strategy_call_fields(state, frame, target, 0x2A2FE)
    frame = _movement_move(state, frame, 'target_x', frame.roster.word(36), 16)
    frame = _scene_render_asl_word(SceneRefreshMemory(state), frame, 'target_x', low16(frame.target_x), executor_shift)
    target = u32(0x2A32C + s16(low16(frame.target_x)))
    from ..high_level_dynamic_flows.business_duel import execute_duel_rule_fields
    return execute_duel_rule_fields(state,frame,target)


def _duel_strategy_partial_fields(state, actor, opponent, frame):
    """Project only supplied actual values; historical missing fields stay None."""
    current=DuelActorFrame() if frame is None else frame
    if type(current) is not DuelActorFrame:
        raise ValueError('actual duel actor observations required')
    current.validate()
    for view in (actor,opponent):
        if view is not None:
            _live_table(state,view)
    return first_replace(FirstDeploymentFrame.unobserved(),target_x=current.command,
        target_y=current.comparison,unit=current.distance,count=current.factor,
        distance=current.weapon_difference,offset_x=current.working_value,
        offset_y=current.response,choice=current.variation,
        roster=actor.cursor() if actor is not None else None,
        candidates=opponent.cursor() if opponent is not None else None,
        controller=current.lookup.cursor() if current.lookup is not None else None)


def _duel_strategy_actor_values(frame):
    """Compatibility names project the one current retained-field return."""
    return DuelActorFrame(frame.target_x,frame.target_y,frame.unit,frame.count,
        frame.distance,frame.choice,frame.offset_x,frame.offset_y,frame.controller).validate()


"""One complete duel sprite emitter, using the existing field/word/math cores."""
from ..high_level_main_flows.business_movement_support import (
    _movement_save_longs, _movement_restore_longs, _movement_compare_address,
)
from ..high_level_remaining_flows.business_city import _duel_velocity_asr_fields
from ..high_level_scene_flows.domain import s8


def _duel_sprite_append_word_fields(state: SceneState,
        frame: FirstDeploymentFrame, value: Word) -> FirstDeploymentFrame:
    """Original MOVE.W destination postincrement, not a host sprite record buffer."""
    frame.roster.set_word(0,value)
    frame=first_replace(frame,roster=frame.roster.advance(2))
    return _movement_test(state,frame,value,16)


def append_duel_sprite_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """28F9C..29038: live six-BYTE templates and actual saved D0-D3 readback."""
    sprite_index_step=1
    sprite_vertical_origin=128
    sprite_size_shift=8
    sprite_extent_shift=7
    sprite_extent_mask=24
    sprite_extent_bias=8
    sprite_horizontal_origin=128
    frame=_resource_cost_frame(state,frame,0x28F9C)
    frame=_movement_save_longs(state,frame,('target_x','target_y','unit','count'))
    frame=first_replace(frame,roster=state.table_at(state.read(0x00FF7002,4)).cursor(),
        candidates=state.table_at(0x29038).cursor())
    frame=_scene_render_asl_word(SceneRefreshMemory(state),frame,'unit',low16(frame.unit),2)
    template=frame.candidates.long(low16(frame.unit))
    frame=first_replace(frame,candidates=state.table_at(template).cursor())
    frame=_movement_move(state,frame,'unit',state.read(0x00FF7000,2),16)
    frame=_movement_compare_address(state,frame,frame.roster.base,0xFFFFF800)
    if not frame.status&4:
        frame.roster.set_byte(0,low8(frame.unit),-5)
        frame=_movement_test(state,frame,low8(frame.unit),8)
    frame=_movement_add_word(state,frame,'unit',sprite_index_step)
    frame=_movement_move(state,frame,'distance',low16(frame.count),16)
    frame=_movement_move(state,frame,'count',low16(frame.count)&0xE7FF,16)
    frame=_movement_move(state,frame,'distance',low16(frame.distance)&0x1800,16)
    while True:
        frame=_movement_move(state,frame,'choice',frame.candidates.byte(2),8)
        frame=_movement_move(state,frame,'choice',u16(s8(low8(frame.choice))),16)
        frame=_movement_add_word(state,frame,'choice',low16(frame.target_x))
        frame=_movement_add_word(state,frame,'choice',sprite_vertical_origin)
        frame=_duel_sprite_append_word_fields(state,frame,low16(frame.choice))
        frame=_movement_move(state,frame,'choice',frame.candidates.byte(1),8)
        frame=_scene_render_asl_word(SceneRefreshMemory(state),frame,'choice',low16(frame.choice),sprite_size_shift)
        frame=_movement_move(state,frame,'choice',low16(frame.choice)|low16(frame.unit),16)
        frame=_movement_add_word(state,frame,'unit',sprite_index_step)
        frame=_duel_sprite_append_word_fields(state,frame,low16(frame.choice))
        frame=_duel_velocity_asr_fields(state,frame,'choice',sprite_extent_shift)
        frame=_movement_move(state,frame,'choice',low16(frame.choice)&sprite_extent_mask,16)
        frame=_movement_add_word(state,frame,'choice',sprite_extent_bias)
        frame=_movement_move(state,frame,'offset_x',low16(frame.choice),16)
        frame=_movement_move(state,frame,'choice',frame.candidates.word(4),16)
        frame=_movement_add_word(state,frame,'choice',low16(frame.count))
        frame=_movement_move(state,frame,'choice',low16(frame.choice)^low16(frame.distance),16)
        frame=_duel_sprite_append_word_fields(state,frame,low16(frame.choice))
        frame=_movement_move(state,frame,'choice',frame.candidates.byte(3),8)
        frame=_movement_move(state,frame,'choice',u16(s8(low8(frame.choice))),16)
        frame=_postbattle_bit_fields(frame,bool(frame.distance&(1<<11)))
        state.sr=(state.sr&65504)|frame.status
        if not frame.status&4:
            frame=_duel_commit_sub_word_fields(state,frame,'choice',0,True)
            frame=_duel_commit_sub_word_fields(state,frame,'choice',low16(frame.offset_x))
        frame=_movement_add_word(state,frame,'choice',low16(frame.target_y))
        frame=_movement_add_word(state,frame,'choice',sprite_horizontal_origin)
        frame=_duel_sprite_append_word_fields(state,frame,low16(frame.choice))
        frame=first_replace(frame,candidates=frame.candidates.advance(6))
        frame=_postbattle_bit_fields(frame,bool(frame.candidates.byte(0,-6)&128))
        state.sr=(state.sr&65504)|frame.status
        if not frame.status&4:
            break
    frame.roster.set_byte(0,0,-5)
    frame=_movement_test(state,frame,0,8)
    state.write(0x00FF7002,4,frame.roster.base)
    frame=_movement_test_long(state,frame,frame.roster.base)
    frame=_duel_commit_sub_word_fields(state,frame,'unit',sprite_index_step)
    state.write(0x00FF7000,2,low16(frame.unit))
    frame=_movement_test(state,frame,low16(frame.unit),16)
    return _movement_restore_longs(state,frame,('target_x','target_y','unit','count'))


from .business_scene import _scene_render_bit
from ..high_level_main_flows.business_movement_support import (
    _movement_save_longs, _movement_restore_longs, _movement_multiply_word,
    _movement_divu_word,
)
from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields


def _duel_actor_call_fields(state, frame, target, continuation):
    """The eight decoded ordinary calls, each with one physical return slot."""
    pairs = ((0x2A22E,0x28C60),(0x808A,0x28C8E),(0x808A,0x28CA4),
        (0x83D4,0x28CB0),(0x28F90,0x28CCA),(0x28F9C,0x28ECE),
        (0x28F9C,0x28F4C),(0x28F9C,0x28F84))
    if (target,continuation) not in pairs:
        raise ValueError('actual actor call pair required')
    frame = _resource_cost_frame(state,frame,target)
    if target in (0x83D4,0x28F90):
        return _duel_strategy_call_fields(state,frame,target,continuation)
    def child(memory,entered):
        if target == 0x2A22E:
            return measure_duel_weapon_contact_fields(memory.state,entered)
        if target == 0x28F9C:
            return append_duel_sprite_fields(memory.state,entered)
        return enqueue_sound_command_fields(SceneRefreshMemory(memory.state),entered)
    return _presentation_call_fields(BattlePresentationMemory(state),frame,continuation,child)


def _duel_actor_store_fields(state, frame, view, offset, value, width=16):
    """A real MOVE updates memory and NZVC, preserving the current X."""
    value = uint(value,width)
    if width == 8:
        view.set_byte(offset,value)
    elif width == 16:
        view.set_word(offset,value)
    elif width == 32:
        view.set_long(offset,value)
        return _movement_test_long(state,frame,value)
    else:
        raise ValueError('actual actor MOVE width required')
    return _movement_test(state,frame,value,width)


def _duel_actor_clear_word_fields(state, frame, view, offset):
    """68000 CLR performs its live read before the zero write."""
    view.word(offset)
    return _duel_actor_store_fields(state,frame,view,offset,0)


def _duel_actor_flag_fields(state, frame, view, mask, set_bit):
    """BSET/BCLR.B alter only Z from the bit's old value, then store."""
    old = view.byte(2)
    frame = _scene_render_bit(SceneRefreshMemory(state),frame,old,mask)
    view.set_byte(2,(old | mask) if set_bit else (old & (255 ^ mask)))
    return frame


def _duel_actor_save_words_fields(state, frame):
    """MOVEM.W D0-D1: no CCR change and no synthetic high-word save."""
    stack = frame.stack_cursor
    for value in (frame.target_y,frame.target_x):
        stack = stack.advance(-2)
        stack.set_word(0,low16(value))
    return first_replace(frame,stack_cursor=stack)


def _duel_actor_restore_words_fields(state, frame):
    """MOVEM.W sign-extends each live saved WORD to the whole LONG."""
    stack = frame.stack_cursor
    for name in ('target_x','target_y'):
        value = stack.word()
        stack = stack.advance(2)
        frame = first_replace(frame,**{name:u32(s16(value))})
    return first_replace(frame,stack_cursor=stack)


def _duel_actor_motion_mode_fields():
    """One edit authority shared by movement and overlay frame restart."""
    actor_motion_mode_mask = 3072
    return actor_motion_mode_mask


def _duel_actor_render_positions_fields():
    """One edit authority for living, defeated and overlay sprite positions."""
    render_baseline_x = 88
    render_injured_x = 84
    return render_baseline_x,render_injured_x


def _duel_actor_palette_fields(state, frame, glow):
    """Two real flash arms share the live WORD copy, not a host palette array."""
    actor_flash_mask = 1
    actor_palette_words = 8
    actor_glow_first = 1024
    actor_glow_second = 2048
    actor_palette_keep_mask = 62451
    if glow:
        frame = _movement_move(state,frame,'target_y',actor_glow_first,16)
    frame = first_replace(frame,controller=state.table_at(0x28080),scan=state.table_at(0xFFFFFB00).cursor())
    frame = _movement_compare_address(state,frame,frame.roster.base,0x00FF7050)
    if frame.roster.base != 0x00FF7050:
        if glow:
            frame = _movement_move(state,frame,'target_y',actor_glow_second,16)
        frame = first_replace(frame,controller=state.table_at(0x280A0),scan=state.table_at(0xFFFFFB20).cursor())
    counter = 'count' if glow else 'choice'
    carrier = 'target_x' if glow else 'target_y'
    if not glow:
        frame = _movement_move(state,frame,counter,actor_palette_words-1,16)
    frame = _movement_move(state,frame,carrier,low16(frame.carrier(carrier)) & actor_flash_mask,16)
    if frame.status & 4:
        frame = first_replace(frame,controller=state.table_at(0x28100 if glow else 0x28110))
    if glow:
        frame = _duel_actor_store_fields(state,frame,frame.roster,0,frame.roster.word() & actor_palette_keep_mask)
        frame = _duel_actor_store_fields(state,frame,frame.roster,0,frame.roster.word() | low16(frame.target_y))
        frame = _movement_move(state,frame,counter,actor_palette_words-1,16)
    while True:
        value = frame.controller.word()
        source = frame.controller.advance(2)
        frame.scan.set_word(0,value)
        frame = first_replace(frame,controller=source,scan=frame.scan.advance(2))
        frame = _movement_test(state,frame,value,16)
        # DBRA changes only the low WORD and preserves the final MOVE flags.
        remaining = u16(low16(frame.carrier(counter))-1)
        frame = first_replace(frame,**{counter:replace_word(frame.carrier(counter),remaining)})
        if remaining == 65535:
            return frame


def _duel_actor_strike_fields(state, frame):
    """Sound, equipment-weighted damage and live WORD restore of one strike."""
    strike_sound = 167
    strike_recovery_delay = 60
    strike_random_mask = 7
    strike_random_bound = 6
    strike_random_fold = 4
    strike_second_weapon_bound = 1
    frame = _duel_actor_save_words_fields(state,frame)
    frame = _movement_move(state,frame,'target_x',strike_sound,16)
    frame = _duel_actor_call_fields(state,frame,0x808A,0x28CA4)
    frame = _duel_actor_store_fields(state,frame,frame.candidates,38,strike_recovery_delay)
    frame = _duel_actor_call_fields(state,frame,0x83D4,0x28CB0)
    frame = _movement_move(state,frame,'target_x',low16(frame.target_x) & strike_random_mask,16)
    rolled = low16(frame.target_x)
    frame = _movement_compare(state,frame,rolled,strike_random_bound,16)
    if rolled >= strike_random_bound:
        frame = _duel_commit_sub_word_fields(state,frame,'target_x',strike_random_fold)
    frame = _movement_move(state,frame,'choice',low16(frame.target_x),16)
    frame = _movement_move(state,frame,'target_x',frame.roster.word(30),16)
    frame = first_replace(frame,controller=state.table_at(0x28D32))
    frame = _duel_actor_call_fields(state,frame,0x28F90,0x28CCA)
    frame = _movement_add_word(state,frame,'choice',state.read(u32(0x28D3E+s16(low16(frame.target_y))),2))
    frame = _movement_move(state,frame,'target_x',frame.roster.word(30),16)
    frame = _movement_move(state,frame,'target_y',frame.roster.word(12),16)
    weapon = low16(frame.target_y)
    frame = _movement_test(state,frame,weapon,16)
    if weapon == 0:
        equipment_offset,table = 44,0x28D4A
    else:
        frame = _movement_compare(state,frame,weapon,strike_second_weapon_bound,16)
        if weapon <= strike_second_weapon_bound:
            equipment_offset,table = 42,0x28D52
        else:
            equipment_offset,table = 46,0x28D5A
    frame = _movement_move(state,frame,'unit',frame.roster.word(equipment_offset),16)
    frame = _scene_render_asl_word(SceneRefreshMemory(state),frame,'unit',low16(frame.unit),1)
    frame = _movement_add_word(state,frame,'target_x',state.read(u32(table+s16(low16(frame.unit))),2))
    frame = _movement_multiply_word(state,frame,'choice',low16(frame.target_x))
    frame = _movement_move(state,frame,'unit',frame.roster.word(2),16)
    frame = _movement_move(state,frame,'unit',low16(frame.unit) & 3,16)
    frame = _scene_render_asl_word(SceneRefreshMemory(state),frame,'unit',low16(frame.unit),1)
    divisor = state.read(u32(0x28D6E+s16(low16(frame.unit))),2)
    frame = _movement_divu_word(state,frame,'choice',divisor,0x28D16)
    frame = _duel_actor_restore_words_fields(state,frame)
    health = frame.roster.word(28)
    frame = _movement_test(state,frame,health,16)
    if health != 0:
        frame,remaining = _movement_binary_flags(state,frame,frame.candidates.word(28),low16(frame.choice),16,True)
        frame.candidates.set_word(28,remaining)
        if frame.status & 8:
            frame = _duel_actor_clear_word_fields(state,frame,frame.candidates,28)
    return frame


def _duel_actor_attack_fields(state, frame):
    """New command and pending attack converge on the same original phase tail."""
    actor_left_command_bit = 256
    actor_right_command_bit = 512
    actor_attack_command_bit = 16
    actor_special_command_bit = 8192
    actor_attack_phase = 4
    actor_clash_kind_mask = 3
    actor_clash_sound = 160
    actor_attack_delay = 4
    actor_attack_cycle_step = 1
    actor_attack_cycle_bound = 5
    frame = _movement_move(state,frame,'target_x',frame.roster.word(),16)
    frame = _movement_test(state,frame,frame.roster.word(2),16)
    if not frame.status & 8:
        frame = _movement_move(state,frame,'target_y',0,16)
        frame = _scene_render_bit(SceneRefreshMemory(state),frame,frame.target_x,actor_left_command_bit)
        if frame.status & 4:
            frame = _movement_add_word(state,frame,'target_y',1)
            frame = _scene_render_bit(SceneRefreshMemory(state),frame,frame.target_x,actor_right_command_bit)
            if not frame.status & 4:
                frame = _movement_add_word(state,frame,'target_y',1)
        frame = _duel_actor_store_fields(state,frame,frame.roster,3,low8(frame.target_y),8)
        frame = _scene_render_bit(SceneRefreshMemory(state),frame,frame.target_x,actor_attack_command_bit)
        if frame.status & 4:
            frame = _duel_actor_store_fields(state,frame,frame.roster,2,frame.roster.word(2) & 16383)
            frame = _scene_render_bit(SceneRefreshMemory(state),frame,frame.target_x,actor_special_command_bit)
            if not frame.status & 4:
                frame = _duel_actor_flag_fields(state,frame,frame.roster,64,True)
            return frame
        frame = _duel_actor_flag_fields(state,frame,frame.roster,128,True)
        frame = _duel_actor_flag_fields(state,frame,frame.roster,64,False)
        frame = _duel_actor_clear_word_fields(state,frame,frame.roster,4)
        frame = _duel_actor_store_fields(state,frame,frame.roster,8,frame.roster.word(22))
        # Newly entered attack falls straight into 28C48, including its delay.
    frame = _movement_move(state,frame,'target_x',frame.roster.word(4),16)
    frame = _movement_test(state,frame,frame.roster.word(8),16)
    if not frame.status & 4:
        return frame
    phase = low16(frame.target_x)
    frame = _movement_compare(state,frame,phase,actor_attack_phase,16)
    if phase == actor_attack_phase:
        frame = _duel_actor_call_fields(state,frame,0x2A22E,0x28C60)
        if frame.status & 1:
            frame = _scene_render_bit(SceneRefreshMemory(state),frame,frame.candidates.byte(2),64)
            clash = False
            if not frame.status & 4:
                frame = _movement_move(state,frame,'target_y',frame.roster.word(2),16)
                frame = _movement_move(state,frame,'unit',frame.candidates.word(2),16)
                frame = _movement_move(state,frame,'target_y',low16(frame.target_y) & actor_clash_kind_mask,16)
                frame = _movement_move(state,frame,'unit',low16(frame.unit) & actor_clash_kind_mask,16)
                own_kind,opponent_kind = low16(frame.target_y),low16(frame.unit)
                frame = _movement_compare(state,frame,opponent_kind,own_kind,16)
                if opponent_kind == own_kind:
                    clash = True
            if clash:
                frame = _duel_actor_save_words_fields(state,frame)
                frame = _movement_move(state,frame,'target_x',actor_clash_sound,16)
                frame = _duel_actor_call_fields(state,frame,0x808A,0x28C8E)
                frame = _duel_actor_restore_words_fields(state,frame)
            else:
                frame = _duel_actor_strike_fields(state,frame)
    frame = _duel_actor_store_fields(state,frame,frame.roster,8,actor_attack_delay)
    frame = _movement_add_word(state,frame,'target_x',actor_attack_cycle_step)
    phase = low16(frame.target_x)
    frame = _movement_compare(state,frame,phase,actor_attack_cycle_bound,16)
    if phase >= actor_attack_cycle_bound:
        frame = _movement_move(state,frame,'target_x',0,16)
        frame = _duel_actor_flag_fields(state,frame,frame.roster,128,False)
    return _duel_actor_store_fields(state,frame,frame.roster,4,low16(frame.target_x))


def _duel_actor_motion_fields(state, frame):
    """Fixed-point motion, facing gate and original unsigned separation bounds."""
    actor_motion_request_mask = 12
    actor_motion_first_direction = 4
    actor_motion_second_direction = 8
    actor_motion_tick_mask = 15
    actor_motion_delay = 48
    actor_motion_boost = 32768
    actor_motion_reverse_mask = 2048
    actor_motion_minimum = 16
    actor_motion_maximum = 224
    frame = _scene_render_bit(SceneRefreshMemory(state),frame,frame.roster.byte(2),16)
    if not frame.status & 4:
        frame = _movement_test(state,frame,frame.roster.word(10),16)
        if frame.status & 4:
            frame = _duel_actor_flag_fields(state,frame,frame.roster,16,False)
        return frame
    frame = _movement_move(state,frame,'target_x',frame.roster.word(),16)
    frame = _movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame = _movement_move(state,frame,'target_x',low16(frame.target_x) & actor_motion_request_mask,16)
    if not frame.status & 4:
        frame = _movement_move(state,frame,'count',actor_motion_second_direction,16)
        frame = _scene_render_bit(SceneRefreshMemory(state),frame,frame.roster.byte(24),8)
        if not frame.status & 4:
            frame = _movement_move(state,frame,'count',actor_motion_first_direction,16)
        frame = _movement_move(state,frame,'target_x',low16(frame.target_x) & low16(frame.count),16)
        if not frame.status & 4:
            frame = _movement_move(state,frame,'target_x',state.read(0x00FF7008,2),16)
            frame = _movement_move(state,frame,'target_x',low16(frame.target_x) & actor_motion_tick_mask,16)
            if frame.status & 4:
                frame = _duel_actor_flag_fields(state,frame,frame.roster,16,True)
                return _duel_actor_store_fields(state,frame,frame.roster,10,actor_motion_delay)
    frame = _movement_move(state,frame,'target_y',low16(frame.target_y) & _duel_actor_motion_mode_fields(),16)
    if frame.status & 4:
        return frame
    frame = _duel_actor_flag_fields(state,frame,frame.roster,32,True)
    frame = _movement_move_long(state,frame,'unit',frame.roster.long(18))
    frame = _movement_move(state,frame,'count',frame.roster.word(40),16)
    frame = _movement_move(state,frame,'count',low16(frame.count) | frame.roster.word(38),16)
    if not frame.status & 4:
        frame,value = _movement_binary_flags(state,frame,frame.unit,actor_motion_boost,32)
        frame = first_replace(frame,unit=value)
    frame = _movement_move(state,frame,'target_y',low16(frame.target_y) & actor_motion_reverse_mask,16)
    if frame.status & 4:
        frame,value = _movement_binary_flags(state,frame,0,frame.unit,32,True)
        frame = first_replace(frame,unit=value)
    frame,value = _movement_binary_flags(state,frame,frame.unit,frame.roster.long(14),32)
    frame = first_replace(frame,unit=value)
    frame = _movement_move_long(state,frame,'target_y',frame.unit)
    frame,value = _movement_binary_flags(state,frame,frame.target_y,frame.candidates.long(14),32,True)
    frame = first_replace(frame,target_y=value)
    if frame.status & 8:
        frame,value = _movement_binary_flags(state,frame,0,frame.target_y,32,True)
        frame = first_replace(frame,target_y=value)
    frame = _movement_move_long(state,frame,'target_y',swap_words(frame.target_y))
    separation = low16(frame.target_y)
    frame = _movement_compare(state,frame,separation,actor_motion_maximum,16)
    if separation < actor_motion_maximum:
        frame = _movement_compare(state,frame,separation,actor_motion_minimum,16)
        if actor_motion_minimum <= separation:
            frame = _duel_actor_store_fields(state,frame,frame.roster,14,frame.unit,32)
    return frame


def _duel_actor_overlay_fields(state, frame):
    """Bit five gates animation only; the original overlay is always emitted."""
    overlay_frame_delay = 10
    overlay_animation_step = 1
    overlay_animation_bound = 5
    overlay_animation_restart = 1
    overlay_plain_pattern = 62
    overlay_armed_pattern = 54
    overlay_blink_shift = 4
    overlay_blink_mask = 1
    overlay_blink_pattern = 60
    frame = _scene_render_bit(SceneRefreshMemory(state),frame,frame.roster.byte(2),32)
    if not frame.status & 4:
        frame = _movement_test(state,frame,frame.roster.word(10),16)
        if frame.status & 4:
            frame = _duel_actor_store_fields(state,frame,frame.roster,10,overlay_frame_delay)
            frame = _movement_move(state,frame,'target_x',frame.roster.word(6),16)
            frame = _movement_add_word(state,frame,'target_x',overlay_animation_step)
            animation = low16(frame.target_x)
            frame = _movement_compare(state,frame,animation,overlay_animation_bound,16)
            if animation >= overlay_animation_bound:
                frame = _movement_move(state,frame,'target_x',overlay_animation_restart,16)
                frame = _movement_move(state,frame,'target_y',frame.roster.word(),16)
                frame = _movement_move(state,frame,'target_y',low16(frame.target_y) & _duel_actor_motion_mode_fields(),16)
                if frame.status & 4:
                    frame = _duel_actor_flag_fields(state,frame,frame.roster,32,False)
                    frame = _movement_move(state,frame,'target_x',0,16)
            frame = _duel_actor_store_fields(state,frame,frame.roster,6,low16(frame.target_x))
    baseline,injured = _duel_actor_render_positions_fields()
    frame = _movement_move(state,frame,'target_x',baseline,16)
    frame = _movement_move(state,frame,'target_y',frame.roster.word(14),16)
    frame = _duel_commit_sub_word_fields(state,frame,'target_y',state.read(0x00FF7006,2))
    frame = _movement_move(state,frame,'unit',overlay_armed_pattern,16)
    frame = _movement_test(state,frame,frame.roster.word(12),16)
    if frame.status & 4:
        frame = _movement_move(state,frame,'unit',overlay_plain_pattern,16)
    frame = _movement_add_word(state,frame,'unit',frame.roster.word(6))
    frame = _scene_render_bit(SceneRefreshMemory(state),frame,frame.roster.byte(2),16)
    if not frame.status & 4:
        frame = _movement_move(state,frame,'unit',state.read(0x00FF7008,2),16)
        frame = _movement_fixed_shift_word(state,frame,'unit',overlay_blink_shift,True)
        frame = _movement_move(state,frame,'unit',low16(frame.unit) & overlay_blink_mask,16)
        frame = _movement_add_word(state,frame,'unit',overlay_blink_pattern)
    frame = _movement_move(state,frame,'count',frame.roster.word(24),16)
    # MOVE.L A0,-(A7) affects NZVC; unlike the surrounding MOVEM saves.
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0,frame.roster.base)
    frame = first_replace(frame,stack_cursor=stack)
    frame = _movement_test_long(state,frame,frame.roster.base)
    frame = _duel_actor_call_fields(state,frame,0x28F9C,0x28F4C)
    actor = frame.stack_cursor.long()
    # MOVEA restore leaves the sprite result's CCR unchanged, and A1 stays live.
    return first_replace(frame,roster=state.table_at(actor).cursor(),stack_cursor=frame.stack_cursor.advance(4))


def render_duel_actor_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """28E6C alternate entry: living/death pose, followed by the common overlay."""
    render_skip_bit = 8
    render_mode_stride = 18
    render_direction_stride = 6
    render_special_pattern = 5
    frame = _resource_cost_frame(state,frame,0x28E6C)
    frame = _scene_render_bit(SceneRefreshMemory(state),frame,frame.roster.byte(2),render_skip_bit)
    if not frame.status & 4:
        return frame
    health = frame.roster.word(28)
    frame = _movement_test(state,frame,health,16)
    baseline,injured = _duel_actor_render_positions_fields()
    if health == 0:
        saved = ('target_x','target_y','unit','count','roster','candidates')
        frame = _movement_save_longs(state,frame,saved)
        frame = _movement_move(state,frame,'target_x',frame.roster.word(12),16)
        frame = _movement_move(state,frame,'unit',state.read(u32(0x28F8C+s16(low16(frame.target_x))),1),8)
        frame = _movement_move(state,frame,'unit',low16(frame.unit) & 255,16)
        frame = _movement_move(state,frame,'count',frame.roster.word(24),16)
        frame = _movement_move(state,frame,'target_y',frame.roster.word(14),16)
        frame = _duel_commit_sub_word_fields(state,frame,'target_y',state.read(0x00FF7006,2))
        frame = _movement_move(state,frame,'target_x',baseline,16)
        frame = _scene_render_bit(SceneRefreshMemory(state),frame,frame.roster.byte(2),16)
        if not frame.status & 4:
            frame = _movement_move(state,frame,'target_x',injured,16)
        frame = _duel_actor_call_fields(state,frame,0x28F9C,0x28F84)
        frame = _movement_restore_longs(state,frame,saved)
    else:
        frame = _movement_move(state,frame,'choice',frame.roster.word(12),16)
        frame = _movement_multiply_word(state,frame,'choice',render_mode_stride)
        frame = _movement_move(state,frame,'unit',0,16)
        frame = _movement_move(state,frame,'unit',frame.roster.byte(3),8)
        frame = _movement_multiply_word(state,frame,'unit',render_direction_stride)
        frame = _movement_add_word(state,frame,'unit',low16(frame.choice))
        frame = _movement_move(state,frame,'choice',frame.roster.word(4),16)
        frame = _scene_render_bit(SceneRefreshMemory(state),frame,frame.roster.byte(2),64)
        if not frame.status & 4:
            frame = _movement_move(state,frame,'choice',render_special_pattern,16)
        frame = _movement_add_word(state,frame,'unit',low16(frame.choice))
        frame = _movement_move(state,frame,'target_x',baseline,16)
        frame = _scene_render_bit(SceneRefreshMemory(state),frame,frame.roster.byte(2),16)
        if not frame.status & 4:
            frame = _movement_move(state,frame,'target_x',injured,16)
        frame = _movement_move(state,frame,'target_y',frame.roster.word(14),16)
        frame = _duel_commit_sub_word_fields(state,frame,'target_y',state.read(0x00FF7006,2))
        frame = _movement_move(state,frame,'count',frame.roster.word(24),16)
        frame = _movement_save_longs(state,frame,('roster','candidates'))
        frame = _duel_actor_call_fields(state,frame,0x28F9C,0x28ECE)
        frame = _movement_restore_longs(state,frame,('roster','candidates'))
    return _duel_actor_overlay_fields(state,frame)


def update_duel_actor_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """28B9A full actor turn, organized into timers, attack, palette and motion."""
    actor_timer_step = 1
    frame = _resource_cost_frame(state,frame,0x28B9A)
    for offset in (8,10,38,40):
        frame = _movement_test(state,frame,frame.roster.word(offset),16)
        if not frame.status & 4:
            frame,value = _movement_binary_flags(state,frame,frame.roster.word(offset),actor_timer_step,16,True)
            frame.roster.set_word(offset,value)
    frame = _movement_move(state,frame,'target_y',frame.roster.word(40),16)
    if not frame.status & 4:
        frame = _duel_actor_palette_fields(state,frame,False)
    frame = _duel_actor_attack_fields(state,frame)
    frame = _movement_move(state,frame,'target_x',frame.roster.word(38),16)
    if not frame.status & 4:
        frame = _duel_actor_palette_fields(state,frame,True)
    frame = _duel_actor_motion_fields(state,frame)
    # Direct same-owner fallthrough at 28E6C: no invented BSR or -4 A7 token.
    return render_duel_actor_fields(state,frame)


def _duel_actor_refresh_call_fields(state, frame, continuation):
    """27A9C and 27AB4 each own precisely their original renderer return token."""
    if continuation not in (0x27AA0,0x27AB8):
        raise ValueError('actual double-actor refresh return required')
    def child(memory,entered):
        return render_duel_actor_fields(memory.state,entered)
    return _presentation_call_fields(BattlePresentationMemory(state),frame,continuation,child)


def refresh_duel_actors_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """27A84..27ABE: two real renderer calls with original caller views read back."""
    frame = _resource_cost_frame(state,frame,0x27A84)
    saved = ('roster','candidates')
    frame = _movement_save_longs(state,frame,saved)
    for actor,opponent,continuation in ((0x00FF7050,0x00FF70A0,0x27AA0),
            (0x00FF70A0,0x00FF7050,0x27AB8)):
        # MOVE.W #0 to the fixed address precedes both LEAs; it is not CLR.
        frame = _duel_actor_store_fields(state,frame,state.table_at(actor),0,0)
        frame = first_replace(frame,roster=state.table_at(actor).cursor(),
            candidates=state.table_at(opponent).cursor())
        frame = _duel_actor_refresh_call_fields(state,frame,continuation)
    return _movement_restore_longs(state,frame,saved)


def configure_duel_weapon_motion_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """27A3A..27A7E: weapon penalty, capped aptitude, velocity and attack delay."""
    maximum_aptitude = 80
    velocity_scale = 1792
    velocity_origin = 24576
    frame = _resource_cost_frame(state,frame,0x27A3A)
    frame = _movement_move(state,frame,'target_x',frame.roster.word(30),16)
    frame = _movement_move(state,frame,'target_y',frame.roster.word(12),16)
    frame = _scene_render_asl_word(SceneRefreshMemory(state),frame,'target_y',low16(frame.target_y),1)
    penalty = state.read(u32(0x27A7E+s16(low16(frame.target_y))),2)
    frame = _duel_commit_sub_word_fields(state,frame,'target_x',penalty)
    if frame.status & 1:
        frame = _movement_move(state,frame,'target_x',0,16)
    else:
        frame = _movement_compare(state,frame,low16(frame.target_x),maximum_aptitude,16)
        if not frame.status & 1:
            frame = _movement_move(state,frame,'target_x',maximum_aptitude,16)
    frame = _movement_move(state,frame,'target_y',maximum_aptitude,16)
    frame = _duel_commit_sub_word_fields(state,frame,'target_y',low16(frame.target_x))
    frame = _movement_multiply_word(state,frame,'target_x',velocity_scale)
    frame,value = _movement_binary_flags(state,frame,frame.target_x,velocity_origin,32)
    frame = first_replace(frame,target_x=value)
    frame = _duel_actor_store_fields(state,frame,frame.roster,18,frame.target_x,32)
    frame = _movement_move_long(state,frame,'target_y',frame.target_y & 65535)
    frame = _movement_divu_word(state,frame,'target_y',2,0x27A74)
    return _duel_actor_store_fields(state,frame,frame.roster,22,low16(frame.target_y))

from ..high_level_main_flows.business_movement_support import _movement_add_byte

def _duel_menu_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Only the eight genuine BSR.W query/cursor pairs; each owns one LONG."""
    pairs=((0x279E6,0x27DBE),(0x28F9C,0x27DF4),
        (0x279E6,0x27E94),(0x28F9C,0x27ECA),
        (0x279E6,0x27F38),(0x28F9C,0x27F84),
        (0x279E6,0x27FCA),(0x28F9C,0x28006))
    if (target,continuation) not in pairs:
        raise ValueError('actual menu query/cursor return pair required')
    def algorithm(memory,entered):
        if target==0x279E6:
            from .business_reuse import choose_first_duel_control_fields
            return choose_first_duel_control_fields(memory.state,entered)
        return append_duel_sprite_fields(memory.state,entered)
    return _presentation_call_fields(BattlePresentationMemory(state),frame,
        continuation,algorithm)


def _duel_menu_button_fields(state: SceneState, frame: FirstDeploymentFrame,
        bit: int) -> FirstDeploymentFrame:
    """Dn BTST.L3/2/1/5 changes Z only, never X/N/V/C."""
    if bit not in (1,2,3,5):
        raise ValueError('actual original menu button bit required')
    frame=_postbattle_bit_fields(frame,bool(frame.target_x&(1<<bit)))
    state.sr=(state.sr&65504)|frame.status
    return frame


def _duel_menu_adjust_memory_word_fields(state: SceneState,
        frame: FirstDeploymentFrame, timer: bool=False) -> FirstDeploymentFrame:
    """Original ADDQ choice or SUBQ timer RMW; no extra MOVE clears arithmetic flags."""
    if type(timer) is not bool:
        raise ValueError('actual choice/timer memory role required')
    view=state.table_at(0x00FF70FA) if timer else frame.roster
    value=view.word(0)
    frame,value=_movement_binary_flags(state,frame,value,1,16,timer)
    view.set_word(0,value)
    return frame


def _duel_menu_equipment_slot(option: Word) -> Word:
    """Original selector0 uses+2,1 uses+0,all other WORDs use+4."""
    uint(option,16)
    return 2 if option==0 else 0 if option==1 else 4


def _duel_menu_equipment_present_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Real TST D1, optional CMP1 and selected equipment WORD TST."""
    option=low16(frame.target_y)
    frame=_movement_test(state,frame,option,16)
    if option!=0:
        frame=_movement_compare(state,frame,option,1,16)
    return _movement_test(state,frame,
        frame.scan.word(_duel_menu_equipment_slot(option)),16)


def _duel_menu_loadout_highlight_fields(state: SceneState,
        frame: FirstDeploymentFrame, vertical_base: Word,
        continuation: int) -> FirstDeploymentFrame:
    """One exact two-option/equipment blink and56-pixel cursor rule."""
    if (vertical_base,continuation) not in ((121,0x27DF4),(104,0x27ECA)):
        raise ValueError('original two-option/equipment cursor plan required')
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&12,16)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0x00FF7008,2),16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&8,16)
        if frame.status&4:
            return frame
    frame=_movement_move(state,frame,'target_x',200,16)
    frame=_movement_move(state,frame,'target_y',frame.roster.word(0),16)
    frame=_movement_multiply_word(state,frame,'target_y',56)
    frame=_movement_add_word(state,frame,'target_y',vertical_base)
    frame=_movement_move(state,frame,'unit',0x43,16)
    frame=_movement_move(state,frame,'count',0x8000,16)
    return _duel_menu_call_fields(state,frame,0x28F9C,continuation)


def choose_duel_two_option_menu_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """27D9C..27DFC: WORD choice, actual query/cursor, final timer X/CCR."""
    frame=_resource_cost_frame(state,frame,0x27D9C)
    frame=_movement_move(state,frame,'target_y',frame.roster.word(0),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&12,16)
    if not frame.status&4:
        frame=_movement_move(state,frame,'unit',1,16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&8,16)
        if frame.status&4:
            frame=_duel_commit_sub_word_fields(state,frame,'unit',0,True)
        frame=_movement_add_word(state,frame,'target_y',low16(frame.unit))
        frame=_movement_compare(state,frame,low16(frame.target_y),2,16)
        if frame.status&1:
            frame=_duel_actor_store_fields(state,frame,frame.roster,0,low16(frame.target_y))
    frame=_duel_menu_call_fields(state,frame,0x279E6,0x27DBE)
    frame=_duel_menu_button_fields(state,frame,5)
    if frame.status&4:
        frame=_duel_menu_loadout_highlight_fields(state,frame,121,0x27DF4)
    return _duel_menu_adjust_memory_word_fields(state,frame,True)


def choose_duel_equipment_fields(state: SceneState,
        frame: FirstDeploymentFrame, second: bool=False) -> FirstDeploymentFrame:
    """Shared27DFC/27E06: publish actual A3 and retain original all-empty loop."""
    frame=_resource_cost_frame(state,frame,0x27E06 if second else 0x27DFC)
    if type(second) is not bool:
        raise ValueError('actual first/second equipment entry required')
    frame=first_replace(frame,scan=state.table_at(0x00FF70CA if second else 0x00FF707A).cursor())
    while True:
        frame=_movement_move(state,frame,'target_y',frame.roster.word(0),16)
        frame=_duel_menu_equipment_present_fields(state,frame)
        if not frame.status&4:
            break
        frame=_duel_menu_adjust_memory_word_fields(state,frame)
        selected=frame.roster.word(0)
        frame=_movement_compare(state,frame,selected,3,16)
        if not frame.status&1:
            frame=_duel_actor_clear_word_fields(state,frame,frame.roster,0)
    frame=_movement_move(state,frame,'target_y',frame.roster.word(0),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&12,16)
    if not frame.status&4:
        frame=_movement_move(state,frame,'unit',1,16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&8,16)
        if frame.status&4:
            frame=_duel_commit_sub_word_fields(state,frame,'unit',0,True)
        while True:
            frame=_movement_add_word(state,frame,'target_y',low16(frame.unit))
            if frame.status&8:
                frame=_movement_move_long(state,frame,'target_y',2)
            else:
                frame=_movement_compare(state,frame,low16(frame.target_y),3,16)
                if not frame.status&1:
                    frame=_movement_move_long(state,frame,'target_y',0)
            frame=_duel_menu_equipment_present_fields(state,frame)
            if not frame.status&4:
                break
        frame=_movement_compare(state,frame,low16(frame.target_y),3,16)
        if frame.status&1:
            frame=_duel_actor_store_fields(state,frame,frame.roster,0,low16(frame.target_y))
    frame=_duel_menu_call_fields(state,frame,0x279E6,0x27E94)
    frame=_duel_menu_button_fields(state,frame,5)
    if frame.status&4:
        frame=_duel_menu_loadout_highlight_fields(state,frame,104,0x27ECA)
    return _duel_menu_adjust_memory_word_fields(state,frame,True)


def choose_first_duel_equipment_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """27DFC establishes A3=FF707A, then the one equipment rule."""
    return choose_duel_equipment_fields(state,frame,False)


def choose_second_duel_equipment_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """27E06 establishes A3=FF70CA; BRA entry adds no fabricated call slot."""
    return choose_duel_equipment_fields(state,frame,True)


def _duel_action_direction_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original1/-1/2/-2 D2 direction, with all BTST and NEG flags."""
    frame=_movement_move(state,frame,'unit',1,16)
    frame=_duel_menu_button_fields(state,frame,3)
    if frame.status&4:
        frame=_duel_commit_sub_word_fields(state,frame,'unit',0,True)
        frame=_duel_menu_button_fields(state,frame,2)
        if frame.status&4:
            frame=_movement_move(state,frame,'unit',2,16)
            frame=_duel_menu_button_fields(state,frame,1)
            if frame.status&4:
                frame=_duel_commit_sub_word_fields(state,frame,'unit',0,True)
    return frame


def _duel_action_restricted_choice_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Restricted menu skips option2; actual MOVEQ and SUBQ define high/X."""
    frame=_movement_move_long(state,frame,'target_y',0)
    frame=_movement_move(state,frame,'target_y',state.read(0x00FF7019,1),8)
    frame=_duel_menu_button_fields(state,frame,3)
    if not frame.status&4:
        frame=_movement_add_word(state,frame,'target_y',1)
        frame=_movement_compare(state,frame,low16(frame.target_y),2,16)
        if frame.status&4:
            frame=_movement_add_word(state,frame,'target_y',1)
        frame=_movement_compare(state,frame,low16(frame.target_y),4,16)
        if not frame.status&1:
            frame=_movement_move_long(state,frame,'target_y',0)
    frame=_duel_menu_button_fields(state,frame,2)
    if not frame.status&4:
        frame=_movement_compare(state,frame,low16(frame.target_y),3,16)
        if frame.status&4:
            frame=_duel_commit_sub_word_fields(state,frame,'target_y',1)
        frame=_duel_commit_sub_word_fields(state,frame,'target_y',1)
        if frame.status&8:
            frame=_movement_move_long(state,frame,'target_y',3)
    return _duel_actor_store_fields(state,frame,state.table_at(0x00FF7019),0,
        low8(frame.target_y),8)


def _duel_action_menu_highlight_fields(state: SceneState,
        frame: FirstDeploymentFrame, restricted: bool) -> FirstDeploymentFrame:
    """Live blink, independent7018 rereads and the actual PC-indexed BYTE table."""
    if type(restricted) is not bool:
        raise ValueError('actual action menu row plan required')
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&15,16)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0x00FF7008,2),16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&8,16)
        if frame.status&4:
            return frame
    if restricted:
        frame=_movement_move(state,frame,'unit',state.read(0x00FF7018,2),16)
        frame=_movement_move(state,frame,'unit',low16(frame.unit)&3,16)
        frame=_movement_move(state,frame,'target_x',200,16)
        frame=_movement_move_long(state,frame,'target_y',0)
        vertical=state.table_at(0x2800E).byte(low16(frame.unit))
        frame=_movement_move(state,frame,'target_y',vertical,8)
        continuation=0x28006
    else:
        frame=_movement_move(state,frame,'target_x',state.read(0x00FF7018,2),16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&2,16)
        frame=_movement_multiply_word(state,frame,'target_x',12)
        frame=_movement_add_word(state,frame,'target_x',176)
        frame=_movement_move(state,frame,'target_y',state.read(0x00FF7018,2),16)
        frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&1,16)
        frame=_movement_multiply_word(state,frame,'target_y',48)
        frame=_movement_add_word(state,frame,'target_y',136)
        continuation=0x27F84
    frame=_movement_move(state,frame,'unit',0x43,16)
    frame=_movement_move(state,frame,'count',0x8000,16)
    return _duel_menu_call_fields(state,frame,0x28F9C,continuation)


def choose_duel_action_menu_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """27ED2..2800E: complete two-layout choice, query, cursor and timer transaction."""
    frame=_resource_cost_frame(state,frame,0x27ED2)
    side=state.read(0x00FF7018,2)
    frame=_movement_test(state,frame,side,16)
    second=bool(frame.status&8)
    frame=_movement_move(state,frame,'target_y',
        state.read(0x00FF70BA if second else 0x00FF706A,2),16)
    frame=_movement_compare(state,frame,low16(frame.target_y),
        state.read(0x00FF70C0 if second else 0x00FF7070,2),16)
    restricted=bool(frame.status&4)
    if restricted:
        frame=_duel_action_restricted_choice_fields(state,frame)
        query_return=0x27FCA
    else:
        frame=_movement_move(state,frame,'target_y',state.read(0x00FF7018,2),16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&15,16)
        if not frame.status&4:
            frame=_duel_action_direction_fields(state,frame)
            frame=_movement_add_byte(state,frame,'target_y',low8(frame.unit))
            frame=_movement_compare(state,frame,low8(frame.target_y),4,8)
            if frame.status&1:
                frame=_duel_actor_store_fields(state,frame,state.table_at(0x00FF7018),0,
                    low16(frame.target_y))
        query_return=0x27F38
    frame=_duel_menu_call_fields(state,frame,0x279E6,query_return)
    frame=_duel_menu_button_fields(state,frame,5)
    if frame.status&4:
        frame=_duel_action_menu_highlight_fields(state,frame,restricted)
    return _duel_menu_adjust_memory_word_fields(state,frame,True)


def _duel_menu_observations_to_fields(state: SceneState,
        frame: DuelTurnFrame, target: int) -> FirstDeploymentFrame:
    checked_duel_turn(frame,state)
    entered=first_replace(FirstDeploymentFrame.unobserved(),
        target_x=frame.command,target_y=frame.comparison,unit=frame.distance,
        count=frame.factor,distance=frame.weapon_difference,offset_x=frame.working_value,
        offset_y=frame.response,choice=frame.variation,roster=frame.actor.cursor(),
        candidates=frame.opponent.cursor(),controller=frame.lookup.cursor(),
        stack_cursor=frame.stack.advance(0))
    raise MovementContinuationBoundary(target,entered,
        'legacy DuelTurnFrame does not observe actual A3-A6 or full CCR/X; supply FirstDeploymentFrame')


def _duel_menu_fields_to_observations(state: SceneState,
        frame: FirstDeploymentFrame) -> DuelTurnFrame:
    frame=_resource_cost_frame(state,frame,0x27D9C)
    conditions=DuelConditionObservation(bool(frame.status&1),bool(frame.status&4),
        bool(frame.status&8),bool(frame.status&2))
    return DuelTurnFrame(frame.target_x,frame.target_y,frame.unit,frame.count,
        frame.distance,frame.offset_x,frame.offset_y,frame.choice,frame.roster,
        frame.candidates,frame.controller,frame.stack_cursor,conditions).validate(state)


def _duel_scene_status_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: Word) -> FirstDeploymentFrame:
    """The original explicit supervisor/IRQ mask, including its real low CCR."""
    if value not in (0x2500,0x2700):
        raise ValueError('actual duel scene status word required')
    state.set_status_word(value)
    return first_replace(frame,status=value&31)


def _duel_scene_store_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: Long, value: Long, width: int=16, clear: bool=False) -> FirstDeploymentFrame:
    """One real literal MOVE or CLR, retaining physical MMIO/readonly boundaries."""
    if type(clear) is not bool:
        raise ValueError('actual original CLR/MOVE role required')
    view=state.table_at(address)
    if clear:
        if width!=16 or value!=0:
            raise ValueError('original scene CLR.W only')
        return _duel_actor_clear_word_fields(state,frame,view,0)
    return _duel_actor_store_fields(state,frame,view,0,value,width)


def _duel_scene_frame_ack_fields(state: SceneState, frame: FirstDeploymentFrame,
        poll: int, arm: bool=True) -> FirstDeploymentFrame:
    """Original live BYTE polling; only real hardware advances a pending frame."""
    if type(arm) is not bool:
        raise ValueError('actual entry/resume poll role required')
    if arm:
        frame=_duel_scene_store_fields(state,frame,0xFFFFF612,0x700)
    while True:
        frame=_movement_test(state,frame,state.read(0xFFFFF612,1),8)
        if frame.status&4:
            return frame
        try:
            state.progress('duel-scene-frame-byte-ack')
        except Boundary:
            raise MovementContinuationBoundary(poll,frame,'actual duel frame BYTE ACK requires external IRQ progress')


def _duel_scene_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: Long, continuation: Long) -> FirstDeploymentFrame:
    """Known sole children share one physical ordinary LONG return bridge."""
    if target==0x83D4:
        return sample_battle_action_random_fields(BattlePolicyMemory(state),frame,continuation)
    def child(memory,entered):
        if target in (0x279E6,0x27A10):
            from .business_reuse import choose_first_duel_control_fields, choose_second_duel_control_fields
            return choose_second_duel_control_fields(state,entered) if target==0x27A10 else choose_first_duel_control_fields(state,entered)
        if target==0x26D86:
            return advance_duel_entry_palette_fields(state,entered)
        if target==0x27D1C:
            return upload_duel_officer_name_fields(state,entered)
        if target==0x27D56:
            return upload_duel_glyph_strip_fields(state,entered)
        if target==0x27D76:
            return clear_duel_text_plane_fields(state,entered)
        if target==0x28012:
            return decode_duel_byte_lanes_fields(state,entered)
        if target==0x2801E:
            return decode_duel_byte_lane_fields(state,entered)
        if target==0xAE8A:
            from .business_scene import decode_glyph_rows_to_buffers_fields
            return decode_glyph_rows_to_buffers_fields(SceneRefreshMemory(state),entered)
        if target==0x27D9C:
            return choose_duel_two_option_menu_fields(state,entered)
        if target==0x27DFC:
            return choose_first_duel_equipment_fields(state,entered)
        if target==0x27E06:
            return choose_second_duel_equipment_fields(state,entered)
        if target==0x27ED2:
            return choose_duel_action_menu_fields(state,entered)
        if target==0x27A3A:
            return configure_duel_weapon_motion_fields(state,entered)
        if target==0x27A84:
            return refresh_duel_actors_fields(state,entered)
        if target==0x28B9A:
            return update_duel_actor_fields(state,entered)
        if target==0x2A29A:
            return choose_duel_ai_command_fields(state,entered)
        if target==0x28F90:
            return scan_duel_thresholds_fields(state,entered)
        if target==0x27506:
            return show_active_duel_turn_label_fields(state,entered)
        if target==0x2777A:
            return wait_active_duel_action_fields(state,entered)
        if target==0x277B8:
            return wait_either_duel_action_fields(state,entered)
        if target==0x28228:
            return choose_duel_status_text_fields(state,entered)
        if target==0x808A:
            return enqueue_sound_command_fields(SceneRefreshMemory(state),entered,low8(entered.target_x))
        if target==0x26BFA:
            from ..high_level_gameplay_flow.business_services import stage_sprite_word_packet_fields
            return stage_sprite_word_packet_fields(SceneRefreshMemory(state),entered)
        if target==0xAF1E:
            from .business_scene import expand_glyph_stream_fields
            return expand_glyph_stream_fields(SceneRefreshMemory(state),entered)
        if target==0x68CE:
            from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields
            return clear_video_sprite_plane_fields(SceneRefreshMemory(state),entered)
        if target==0xAD06:
            from .business_scene import flush_scene_transfer_queue_fields
            return flush_scene_transfer_queue_fields(SceneRefreshMemory(state),entered)
        if target==0xDEA6:
            from .business_scene import darken_palette_fields
            return darken_palette_fields(SceneRefreshMemory(state),entered)
        if target in (0x27BCC,0x27C22,0x27C8A,0x27CA4,0x27CD2,0x27CFC) and continuation==0x27B7E:
            from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_92_fields
            return highbank_coordinate_live_state_92_fields(state,entered,target)
        raise MovementContinuationBoundary(target,entered,
            'actual duel controller child lacks a complete current-frame ABI')
    return _presentation_call_fields(BattlePresentationMemory(state),frame,continuation,child)


def _duel_scene_copy_fields(state: SceneState, frame: FirstDeploymentFrame,
        source: Long, count: Word, width: int=32, destination: Long | None=None) -> FirstDeploymentFrame:
    """DBRA block transfer preserves last MOVE flags and actual pointer increments."""
    if width not in (16,32):
        raise ValueError('actual WORD/LONG scene transfer required')
    frame=first_replace(frame,roster=state.table_at(source).cursor())
    if destination is not None:
        frame=first_replace(frame,candidates=state.table_at(destination).cursor())
    frame=_movement_move(state,frame,'target_x',count,16)
    while True:
        value=frame.roster.word(0) if width==16 else frame.roster.long(0)
        frame=first_replace(frame,roster=frame.roster.advance(width//8))
        view=frame.auxiliary if destination is None else frame.candidates
        frame=_duel_actor_store_fields(state,frame,view,0,value,width)
        if destination is not None:
            frame=first_replace(frame,candidates=frame.candidates.advance(width//8))
        remaining=u16(low16(frame.target_x)-1)
        frame=first_replace(frame,target_x=replace_word(frame.target_x,remaining))
        if remaining==65535:
            return frame


def _duel_scene_dialog_fields(state: SceneState, frame: FirstDeploymentFrame,
        source: Long, position: Word, dimensions: bool=True) -> FirstDeploymentFrame:
    """Only the real four-field loadout dialog or two-field action dialog writes."""
    frame=_duel_scene_store_fields(state,frame,0x00FF700C,position)
    frame=_duel_scene_store_fields(state,frame,0x00FF700E,source,32)
    if dimensions:
        frame=_duel_scene_store_fields(state,frame,0x00FF7014,1)
        frame=_duel_scene_store_fields(state,frame,0x00FF7016,2)
    return frame


def _duel_scene_packet_fields(state: SceneState, frame: FirstDeploymentFrame,
        source: Long, command: Long, rows: Word, row_command: Word,
        continuation: Long) -> FirstDeploymentFrame:
    frame=first_replace(frame,roster=state.table_at(source).cursor())
    frame=_movement_move_long(state,frame,'target_x',command)
    frame=_movement_move(state,frame,'target_y',rows,16)
    frame=_movement_move(state,frame,'unit',row_command,16)
    return _duel_scene_call_fields(state,frame,0x26BFA,continuation)


def initialize_duel_scene_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26DB4..2702A setup; no decoded media or fabricated DMA/child return."""
    frame=_resource_cost_frame(state,frame,0x26DB4)
    frame=_duel_scene_status_fields(state,frame,0x2700)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF606,2),16)
    frame=_movement_move(state,frame,'target_x',low8(frame.target_x)&0xBF,8)
    frame=_duel_scene_store_fields(state,frame,0xC00004,low16(frame.target_x))
    frame=_duel_scene_store_fields(state,frame,0xFFFFF612,0,clear=True)
    frame=_duel_scene_call_fields(state,frame,0x68CE,0x26DD0)
    for command in (0x8338,0x8238,0x8407,0x856C,0x8D37,0x9294,0x8B03):
        frame=_duel_scene_store_fields(state,frame,0xC00004,command)
    for address,value,width in ((0x00FF705E,0x00400000,32),(0x00FF7068,0x8800,16),
            (0x00FF7052,1,16),(0x00FF70AE,0x01000000,32),
            (0x00FF70B8,0xA000,16),(0x00FF70A2,1,16)):
        frame=_duel_scene_store_fields(state,frame,address,value,width)
    for address in (0x00FF70F0,0x00FF70F6,0x00FF70F8):
        frame=_duel_scene_store_fields(state,frame,address,0,clear=True)
    for officer_address,destination in ((0x00FF706A,0x00FF707B),(0x00FF70BA,0x00FF70CB)):
        frame=_movement_move_long(state,frame,'distance',0)
        frame=first_replace(frame,scratch=state.table_at(0xFFFFEA88).cursor())
        frame=_movement_move(state,frame,'distance',state.read(officer_address,2),16)
        frame=_movement_multiply_word(state,frame,'distance',3)
        frame=first_replace(frame,scratch=frame.scratch.advance(s16(low16(frame.distance))))
        for offset in (0,2):
            value=frame.scratch.byte(0)
            frame=first_replace(frame,scratch=frame.scratch.advance(1))
            frame=_duel_scene_store_fields(state,frame,destination+offset,value,8)
        frame=_duel_scene_store_fields(state,frame,destination+4,frame.scratch.byte(0),8)
    frame=_duel_scene_store_fields(state,frame,0xC00004,0x40000000,32)
    frame=first_replace(frame,auxiliary=state.table_at(0xC00000).cursor())
    frame=_duel_scene_copy_fields(state,frame,0x6C3B4,0x2FFF)
    frame=_duel_scene_store_fields(state,frame,0xC00004,0x40000003,32)
    frame=_duel_scene_copy_fields(state,frame,0x89DDC,0x1F)
    frame=first_replace(frame,roster=state.table_at(0x8A426).cursor(),candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_movement_move(state,frame,'target_y',2,16)
    frame=_movement_move(state,frame,'count',9,16)
    frame=_duel_scene_call_fields(state,frame,0xAF1E,0x26EEC)
    frame=_duel_scene_copy_fields(state,frame,0xFFFFD300,0x4F)
    frame=_duel_scene_store_fields(state,frame,0xC00004,0x50000003,32)
    frame=_duel_scene_copy_fields(state,frame,0x783B4,0x2F)
    frame=_duel_scene_store_fields(state,frame,0xC00004,0x42000003,32)
    for officer,continuation in ((0x00FF706A,0x26F30),(0x00FF70BA,0x26F42)):
        frame=_movement_move(state,frame,'choice',state.read(officer,2),16)
        frame=_movement_move(state,frame,'target_x',1,16)
        frame=_movement_move(state,frame,'target_y',2,16)
        frame=_duel_scene_call_fields(state,frame,0x27D1C,continuation)
    frame=first_replace(frame,roster=state.table_at(0x288BA).cursor())
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_movement_move(state,frame,'target_y',2,16)
    frame=_movement_move(state,frame,'count',1,16)
    frame=_duel_scene_call_fields(state,frame,0x27D56,0x26F58)
    frame=_duel_scene_call_fields(state,frame,0x27D76,0x26F5C)
    frame=_duel_scene_copy_fields(state,frame,0x28080,0x1F,32,0xFFFFFB00)
    frame=_duel_scene_store_fields(state,frame,0xFFFFF31E,1)
    frame=first_replace(frame,roster=state.table_at(0x78474).cursor())
    frame=_movement_compare(state,frame,state.read(0x00FF70F2,2),3,16)
    if frame.status&4:
        frame=first_replace(frame,roster=state.table_at(0x78656).cursor())
    for source_override,continuation,control in ((None,0x26F9C,0x60000003),(0x7883E,0x26FCA,0x70000003)):
        if source_override is not None:
            frame=first_replace(frame,roster=state.table_at(source_override).cursor())
        frame=first_replace(frame,candidates=state.table_at(0x00FF6000).cursor())
        frame=_movement_move(state,frame,'target_x',0x500,16)
        frame=_duel_scene_call_fields(state,frame,0x28012,continuation)
        frame=_duel_scene_store_fields(state,frame,0xC00004,control,32)
        frame=_duel_scene_copy_fields(state,frame,0x00FF6000,0x4FF,16)
    frame=_duel_scene_store_fields(state,frame,0xFFFFF694,0x603)
    frame=_duel_scene_store_fields(state,frame,0xFFFFF692,0x604)
    frame=_duel_scene_packet_fields(state,frame,0x28120,0x60000028,3,0xEA00,0x2700A)
    frame=_duel_scene_call_fields(state,frame,0xAD06,0x27010)
    return _duel_scene_packet_fields(state,frame,0x28174,0x60000028,5,0xEB80,0x2702A)


def _duel_scene_auto_loadout_fields(state: SceneState,
        frame: FirstDeploymentFrame, second: bool) -> tuple[FirstDeploymentFrame, bool]:
    """Original A0-dependent automatic panel tail; never guess indexed handler D6."""
    frame=first_replace(frame,roster=state.table_at(0x00FF70A0 if second else 0x00FF7050).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.word(0x1E),16)
    frame=first_replace(frame,controller=state.table_at(0x27B96).cursor())
    frame=_duel_scene_call_fields(state,frame,0x28F90,0x27B76)
    frame=_scene_render_asl_word(SceneRefreshMemory(state),frame,'target_y',low16(frame.target_y),1)
    target=state.read(u32(0x27BA2+s16(low16(frame.target_y))),4)
    frame=first_replace(frame,scan=state.table_at(target).cursor())
    frame=_duel_scene_call_fields(state,frame,target,0x27B7E)
    frame=_movement_test(state,frame,low16(frame.offset_y),16)
    commit=not bool(frame.status&4)
    frame=_movement_compare_address(state,frame,frame.roster.base,0x00FF7050)
    return frame,commit


def prepare_duel_loadout_fields(state: SceneState, frame: FirstDeploymentFrame,
        second: bool=False) -> tuple[bool, FirstDeploymentFrame]:
    """One closed first/second weapon-and-controller transaction, exact original calls."""
    if type(second) is not bool:
        raise ValueError('actual first/second loadout role required')
    frame=_resource_cost_frame(state,frame,0x27164 if second else 0x2702A)
    mode=0x00FF700B if second else 0x00FF700A
    actor=0x00FF70A0 if second else 0x00FF7050
    weapon=0x00FF70AC if second else 0x00FF705C
    control_choice=0x00FF70E2 if second else 0x00FF7092
    query=0x27A10 if second else 0x279E6
    frame=_movement_compare(state,frame,state.read(mode,1),3,8)
    if not frame.status&4:
        frame=_duel_scene_dialog_fields(state,frame,0x288BE,0xC600)
        if second:
            frame=_duel_scene_store_fields(state,frame,0x00FF70DA,1)
    if not second:
        frame=_duel_scene_call_fields(state,frame,0x26D86,0x2705C)
    controller=False
    frame=_duel_scene_status_fields(state,frame,0x2500)
    while True:
        frame=_duel_scene_frame_ack_fields(state,frame,0x271A4 if second else 0x27066)
        frame=_duel_scene_call_fields(state,frame,0x26D86,0x271AE if second else 0x27070)
        frame=_duel_scene_call_fields(state,frame,0x27A84,0x271B2 if second else 0x27074)
        if not second:
            frame=_duel_scene_store_fields(state,frame,0x00FF708A,0,clear=True)
        frame=_movement_compare(state,frame,state.read(mode,1),3,8)
        if frame.status&4:
            frame,commit=_duel_scene_auto_loadout_fields(state,frame,second)
            # The source checks returned A0, not the old host side snapshot.
            second=not bool(frame.status&4)
            actor=0x00FF70A0 if second else 0x00FF7050
            mode=0x00FF700B if second else 0x00FF700A
            weapon=0x00FF70AC if second else 0x00FF705C
            control_choice=0x00FF70E2 if second else 0x00FF7092
            query=0x27A10 if second else 0x279E6
            # The actual zero-response second-side tail goes directly to
            # 2728A; only the returned first-side actor retries 27060.
            if not commit and not second:
                continue
            controller=False
            break
        frame=first_replace(frame,roster=state.table_at(weapon).cursor())
        frame=_duel_scene_call_fields(state,frame,query,0x271C8 if second else 0x27090)
        frame=_duel_scene_call_fields(state,frame,0x27E06 if second else 0x27DFC,
            0x271CC if second else 0x27094)
        frame=_movement_test(state,frame,state.read(0x00FF700C,2),16)
        if not frame.status&4:
            continue
        frame=_duel_scene_packet_fields(state,frame,0x28202 if second else 0x281EC,
            0x60000004,1,0xED44 if second else 0xED08,0x271EE if second else 0x270B6)
        frame=_duel_scene_call_fields(state,frame,query,0x271F2 if second else 0x270BA)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&0xF0,16)
        if frame.status&4:
            continue
        frame=_movement_move(state,frame,'target_x',0xAC,16)
        frame=_duel_scene_call_fields(state,frame,0x808A,0x27202 if second else 0x270CA)
        frame=_movement_compare(state,frame,state.read(mode,1),3,8)
        controller=not bool(frame.status&4)
        break
    if controller:
        frame=_duel_scene_call_fields(state,frame,0x27D76,0x27212 if second else 0x270DA)
        frame=_duel_scene_dialog_fields(state,frame,0x2890A,0xC600)
        frame=_duel_scene_status_fields(state,frame,0x2500)
        while True:
            frame=_duel_scene_frame_ack_fields(state,frame,0x2723E if second else 0x27106)
            frame=_duel_scene_call_fields(state,frame,0x26D86,0x27248 if second else 0x27110)
            frame=_duel_scene_call_fields(state,frame,0x27A84,0x2724C if second else 0x27114)
            frame=first_replace(frame,roster=state.table_at(control_choice).cursor())
            frame=_duel_scene_call_fields(state,frame,0x27A10 if second else 0x279E6,
                0x27256 if second else 0x2711E)
            frame=_duel_scene_call_fields(state,frame,0x27D9C,0x2725A if second else 0x27122)
            frame=_movement_test(state,frame,state.read(0x00FF700C,2),16)
            if not frame.status&4:
                continue
            frame=_duel_scene_call_fields(state,frame,0x27A10 if second else 0x279E6,
                0x27266 if second else 0x2712E)
            frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&0xF0,16)
            if frame.status&4:
                continue
            frame=_movement_move(state,frame,'target_x',0xAC,16)
            frame=_duel_scene_call_fields(state,frame,0x808A,0x27276 if second else 0x2713E)
            frame=first_replace(frame,roster=state.table_at(control_choice).cursor())
            frame=_movement_test(state,frame,frame.roster.word(0),16)
            if not frame.status&4:
                frame=_duel_scene_store_fields(state,frame,mode,3,8)
            break
    return second,commit_duel_loadout_fields(state,frame,second)


def commit_duel_loadout_fields(state: SceneState, frame: FirstDeploymentFrame,
        second: bool) -> FirstDeploymentFrame:
    """27152/2728A explicit commit follows the actual post-handler A0 branch."""
    if type(second) is not bool:
        raise ValueError('actual original selected loadout side required')
    frame=_duel_scene_status_fields(state,frame,0x2700)
    frame=first_replace(frame,roster=state.table_at(0x00FF70A0 if second else 0x00FF7050).cursor())
    frame=_duel_scene_call_fields(state,frame,0x27A3A,0x27298 if second else 0x27160)
    return _duel_scene_call_fields(state,frame,0x27D76,0x2729C if second else 0x27164)


def prepare_duel_readiness_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Two distinct status/confirmation loops retain first-only palette refresh."""
    for second in (False,True):
        if second:
            frame=_duel_scene_status_fields(state,frame,0x2700)
            frame=_duel_scene_call_fields(state,frame,0x27D76,0x272F6)
        frame=_duel_scene_call_fields(state,frame,0x83D4,0x272FC if second else 0x272A2)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&3,16)
        frame=_movement_compare(state,frame,low16(frame.target_x),3,16)
        if frame.status&4:
            frame=_movement_move(state,frame,'target_x',0,16)
        if second:
            frame=_movement_add_word(state,frame,'target_x',3)
        frame=_duel_scene_call_fields(state,frame,0x28228,0x2730E if second else 0x272B2)
        frame=_movement_move(state,frame,'target_x',0xA5,16)
        frame=_duel_scene_call_fields(state,frame,0x808A,0x2731A if second else 0x272BE)
        frame=_duel_scene_store_fields(state,frame,0x00FF70A2 if second else 0x00FF7052,0,clear=True)
        frame=_duel_scene_status_fields(state,frame,0x2500)
        while True:
            frame=_duel_scene_frame_ack_fields(state,frame,0x2732A if second else 0x272CE)
            if not second:
                frame=_duel_scene_call_fields(state,frame,0x26D86,0x272D8)
            frame=_duel_scene_call_fields(state,frame,0x27A84,0x27334 if second else 0x272DC)
            frame=_movement_test(state,frame,state.read(0x00FF700C,2),16)
            if not frame.status&4:
                continue
            frame=_duel_scene_call_fields(state,frame,0x27A10 if second else 0x279E6,
                0x27340 if second else 0x272E8)
            frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&0xF0,16)
            if not frame.status&4:
                break
    frame=_movement_move(state,frame,'target_x',0x8B,16)
    return _duel_scene_call_fields(state,frame,0x808A,0x27350)


def begin_duel_combat_fields(state: SceneState, frame: FirstDeploymentFrame,
        clear_text: bool=True) -> tuple[str, FirstDeploymentFrame]:
    """One two-actor combat frame, health/pending gates and real action request."""
    frame=_resource_cost_frame(state,frame,0x27350 if clear_text else 0x2735C)
    if type(clear_text) is not bool:
        raise ValueError('actual loop continuation required')
    if clear_text:
        frame=_duel_scene_status_fields(state,frame,0x2700)
        frame=_duel_scene_call_fields(state,frame,0x27D76,0x27358)
        frame=_duel_scene_status_fields(state,frame,0x2500)
    frame=_duel_scene_frame_ack_fields(state,frame,0x27362)
    frame=_duel_scene_actor_fields(state,frame,False)
    return continue_after_first_duel_actor_fields(state,frame)


def _duel_scene_actor_fields(state: SceneState, frame: FirstDeploymentFrame,
        second: bool) -> FirstDeploymentFrame:
    """Two closed actor roles reuse the exact query/AI/update sequence."""
    if type(second) is not bool:
        raise ValueError('actual original actor role required')
    if second:
        actor,opponent,mode=0x00FF70A0,0x00FF7050,0x00FF700B
        query,query_return,ai_return,actor_return=0x27A10,0x273A6,0x273BA,0x273C4
    else:
        actor,opponent,mode=0x00FF7050,0x00FF70A0,0x00FF700A
        query,query_return,ai_return,actor_return=0x279E6,0x27378,0x2738C,0x27396
    frame=first_replace(frame,roster=state.table_at(actor).cursor(),candidates=state.table_at(opponent).cursor())
    frame=_duel_scene_call_fields(state,frame,query,query_return)
    frame=_duel_scene_store_fields(state,frame,actor,low16(frame.target_x))
    frame=_movement_compare(state,frame,state.read(mode,1),3,8)
    if frame.status&4:
        frame=_duel_scene_call_fields(state,frame,0x2A29A,ai_return)
        frame=_duel_scene_store_fields(state,frame,actor,low16(frame.target_x))
    return _duel_scene_call_fields(state,frame,0x28B9A,actor_return)


def continue_after_first_duel_actor_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> tuple[str, FirstDeploymentFrame]:
    """27396 continuation: second actor followed by the live terminal/action gate."""
    frame=_resource_cost_frame(state,frame,0x27396)
    frame=_duel_scene_actor_fields(state,frame,True)
    frame=_duel_scene_call_fields(state,frame,0x27506,0x273C8)
    frame=_duel_scene_store_fields(state,frame,0x00FF7018,0,clear=True)
    frame=_movement_test(state,frame,state.read(0x00FF706C,2),16)
    if frame.status&4:
        return 'terminal',frame
    frame=_duel_scene_store_fields(state,frame,0x00FF7018,0x8000)
    frame=_movement_test(state,frame,state.read(0x00FF70BC,2),16)
    if frame.status&4:
        return 'terminal',frame
    frame=_movement_move(state,frame,'target_y',state.read(0x00FF7052,2),16)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_y)|state.read(0x00FF70A2,2),16)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_y)&0xD000,16)
    if not frame.status&4:
        return 'next_frame',frame
    frame=_duel_scene_store_fields(state,frame,0x00FF7018,0,clear=True)
    frame=_movement_move(state,frame,'target_x',state.read(0x00FF7050,2),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&0x40,16)
    if frame.status&4:
        frame=_duel_scene_store_fields(state,frame,0x00FF7018,0x8000)
        frame=_movement_move(state,frame,'target_x',state.read(0x00FF70A0,2),16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&0x40,16)
        if frame.status&4:
            return 'next_frame',frame
    return 'action',frame


def choose_duel_turn_action_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> tuple[str, FirstDeploymentFrame]:
    """Actual manual query/menu WORD slot and automatic selection before submit."""
    frame=_resource_cost_frame(state,frame,0x27426)
    frame=_duel_scene_status_fields(state,frame,0x2700)
    frame=_duel_scene_store_fields(state,frame,0xFFFFD100,0,clear=True)
    frame=_movement_test(state,frame,state.read(0x00FF7018,2),16)
    second=bool(frame.status&8)
    mode=state.read(0x00FF700B if second else 0x00FF700A,1)
    frame=_movement_compare(state,frame,mode,3,8)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0x00FF70A0 if second else 0x00FF7050,2),16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&3,16)
        frame=_duel_scene_store_fields(state,frame,0x00FF7019,low8(frame.target_x),8)
        return 'submit',frame
    frame=_movement_move(state,frame,'target_y',state.read(0x00FF70BA if second else 0x00FF706A,2),16)
    frame=_movement_compare(state,frame,low16(frame.target_y),state.read(0x00FF70C0 if second else 0x00FF7070,2),16)
    linked=bool(frame.status&4)
    frame=_duel_scene_dialog_fields(state,frame,0x28924 if linked else 0x288EA,
        0xCB80 if linked else 0xC740,False)
    frame=_movement_move(state,frame,'target_x',0xAD,16)
    frame=_duel_scene_call_fields(state,frame,0x808A,0x274C2)
    return continue_manual_duel_action_fields(state,frame)


def continue_manual_duel_action_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> tuple[str, FirstDeploymentFrame]:
    """274C2: caller-owned live D0.W save, menu LONG call, restored current high bits."""
    frame=_resource_cost_frame(state,frame,0x274C2)
    frame=_duel_scene_status_fields(state,frame,0x2500)
    while True:
        frame=_duel_scene_frame_ack_fields(state,frame,0x274CC)
        frame=_duel_scene_call_fields(state,frame,0x27A84,0x274D6)
        frame=_duel_scene_call_fields(state,frame,0x279E6,0x274DA)
        frame=_movement_test(state,frame,state.read(0x00FF7018,2),16)
        if frame.status&8:
            frame=_duel_scene_call_fields(state,frame,0x27A10,0x274E6)
        stack=frame.stack_cursor.advance(-2)
        stack.set_word(0,low16(frame.target_x))
        frame=first_replace(frame,stack_cursor=stack)
        frame=_movement_test(state,frame,low16(frame.target_x),16)
        frame=_duel_scene_call_fields(state,frame,0x27ED2,0x274EC)
        saved=frame.stack_cursor.word(0)
        frame=first_replace(frame,stack_cursor=frame.stack_cursor.advance(2))
        frame=_movement_move(state,frame,'target_x',saved,16)
        frame=_movement_test(state,frame,state.read(0x00FF700C,2),16)
        if not frame.status&4:
            continue
        frame=_duel_scene_button_fields(state,frame,5)
        if not frame.status&4:
            return 'submit',frame
        frame=_duel_scene_button_fields(state,frame,4)
        if not frame.status&4:
            return 'next_frame_clear',frame


def _duel_scene_button_fields(state: SceneState, frame: FirstDeploymentFrame,
        bit: int) -> FirstDeploymentFrame:
    """Actual D0 LONG cancel/confirm tests use the one existing Z-only rule."""
    if bit not in (4,5):
        raise ValueError('actual manual action button required')
    frame=_postbattle_bit_fields(frame,bool(frame.target_x&(1<<bit)))
    state.sr=(state.sr&65504)|frame.status
    return frame


def perform_selected_duel_action_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Frame-only compatibility projection; fixed fade needs the phase-bearing API."""
    phase,returned=perform_selected_duel_action_result_fields(state,frame)
    if phase!='next_frame_clear':
        raise MovementContinuationBoundary(0x26D46,returned,
            'nonlocal original action uses perform_selected_duel_action_result_fields')
    return returned


def show_terminal_duel_result_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """27990 terminal messages and actual waits before the shared fade-return tail."""
    frame=_resource_cost_frame(state,frame,0x27990)
    frame=_duel_scene_frame_ack_fields(state,frame,0x27996)
    frame=_duel_scene_call_fields(state,frame,0x27506,0x279A0)
    frame=_duel_scene_frame_ack_fields(state,frame,0x279A6)
    frame=_duel_scene_status_fields(state,frame,0x2700)
    frame=_movement_move(state,frame,'target_x',31,16)
    frame=_movement_test(state,frame,state.read(0x00FF7018,2),16)
    if frame.status&8:
        frame=_movement_move(state,frame,'target_x',34,16)
    frame=_duel_scene_call_fields(state,frame,0x28228,0x279C4)
    frame=_duel_scene_call_fields(state,frame,0x2777A,0x279C8)
    frame=_duel_scene_call_fields(state,frame,0x27D76,0x279CC)
    frame=_movement_move(state,frame,'target_x',32,16)
    frame=_movement_test(state,frame,state.read(0x00FF7018,2),16)
    if frame.status&8:
        frame=_movement_add_word(state,frame,'target_x',1)
    frame=_duel_scene_call_fields(state,frame,0x28228,0x279DE)
    return _duel_scene_call_fields(state,frame,0x277B8,0x279E2)


def finish_duel_scene_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26D46..26D86: original live16-step fade, then the genuine outer RTS."""
    frame=_resource_cost_frame(state,frame,0x26D46)
    frame=_duel_scene_status_fields(state,frame,0x2500)
    while True:
        frame=_duel_scene_frame_ack_fields(state,frame,0x26D50)
        frame=_duel_scene_call_fields(state,frame,0x27A84,0x26D5A)
        step=state.read(0x00FF70F6,2)
        frame=_movement_compare(state,frame,step,16,16)
        if not frame.status&1:
            return frame
        frame=_movement_move(state,frame,'target_x',state.read(0x00FF70F6,2),16)
        frame=_movement_move(state,frame,'target_y',0x40,16)
        frame=first_replace(frame,roster=state.table_at(0x28080).cursor())
        frame=_duel_scene_call_fields(state,frame,0xDEA6,0x26D7C)
        value=state.read(0x00FF70F6,2)
        frame,value=_movement_binary_flags(state,frame,value,1,16)
        state.write(0x00FF70F6,2,value)


def run_duel_scene_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """One complete logical controller; named phases, no PC/opcode interpreter."""
    frame=_resource_cost_frame(state,frame,0x26DB4)
    frame=initialize_duel_scene_fields(state,frame)
    second=False
    while True:
        committed_second,frame=prepare_duel_loadout_fields(state,frame,second)
        if committed_second:
            break
        second=True
    frame=prepare_duel_readiness_fields(state,frame)
    clear_text=True
    while True:
        phase,frame=begin_duel_combat_fields(state,frame,clear_text)
        if phase=='terminal':
            frame=show_terminal_duel_result_fields(state,frame)
            return finish_duel_scene_fields(state,frame)
        if phase=='action':
            phase,frame=choose_duel_turn_action_fields(state,frame)
            if phase=='submit':
                phase,frame=perform_selected_duel_action_result_fields(state,frame)
                if phase=='fade':
                    return finish_duel_scene_fields(state,frame)
        clear_text=phase=='next_frame_clear'


def _duel_scene_legacy_context_fields(state: SceneState, observation,
        target: int, sole_core: str) -> FirstDeploymentFrame:
    """Record exactly the old DTO's live values before requesting the full ABI.

    The old contracts cannot supply A3-A6 and CCR/X. Their projections therefore
    stop before a state-changing full-core entry. This is not a zero-state
    fallback and does not widen any accepted SceneState contract.
    """
    if type(state) is not SceneState or type(sole_core) is not str:
        raise ValueError('actual Scene state and named sole duel core required')
    if type(observation) is DuelTurnFrame:
        return _duel_menu_observations_to_fields(state,observation,target)
    if type(observation) is DuelSceneContext:
        observation.validate()
        if observation.initialization is not None:
            observation=observation.initialization
        else:
            raise MovementContinuationBoundary(target,FirstDeploymentFrame.unobserved(),
                'legacy scene omits its current complete live-in; use '+sole_core)
    if type(observation) is DuelInitializationResult:
        observation.validate(state)
        observation=observation.preparation
    entered=FirstDeploymentFrame.unobserved()
    if type(observation) is DuelInitializationContext:
        observation.validate(state)
        values=observation.frame
        entered=first_replace(entered,target_x=values.command,target_y=values.comparison,
            unit=values.distance,count=values.factor,distance=values.weapon_difference,
            offset_x=observation.glyph_work,offset_y=observation.response,
            choice=values.variation,controller=values.lookup,
            stack_cursor=observation.stack.advance(0))
    elif type(observation) is DuelPreparationContext:
        observation.validate(state)
        values=observation.frame
        entered=first_replace(entered,target_x=values.command,target_y=values.comparison,
            unit=values.distance,count=values.factor,distance=values.weapon_difference,
            offset_x=values.working_value,offset_y=observation.response,
            choice=values.variation,roster=observation.actor.cursor(),
            candidates=observation.opponent.cursor(),controller=values.lookup,
            stack_cursor=observation.stack.advance(0))
    elif type(observation) is DuelControlContext:
        observation.validate()
        entered=first_replace(entered,target_x=observation.command,target_y=observation.mode)
    elif observation is not None:
        raise ValueError('actual historical duel observation required')
    raise MovementContinuationBoundary(target,entered,
        'legacy duel observation omits live A3-A6 and full CCR/X; use '+sole_core)


def show_active_duel_turn_label_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """27506: tick-selected one-row packet tails directly into unique26BFA."""
    frame=_resource_cost_frame(state,frame,0x27506)
    frame=first_replace(frame,roster=state.table_at(0x281A0).cursor())
    frame=_movement_move(state,frame,'unit',0xEC08,16)
    frame=_movement_move(state,frame,'target_x',state.read(0x00FF7008,2),16)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&1,16)
    if not frame.status&4:
        frame=first_replace(frame,roster=state.table_at(0x281B6).cursor())
        frame=_movement_move(state,frame,'unit',0xEC44,16)
    frame=_movement_move_long(state,frame,'target_x',0x60000004)
    frame=_movement_move(state,frame,'target_y',1,16)
    from ..high_level_gameplay_flow.business_services import stage_sprite_word_packet_fields
    # BRA.W26BFA owns no new slot: its RTS uses the caller's current LONG.
    return stage_sprite_word_packet_fields(SceneRefreshMemory(state),frame)


def choose_duel_status_text_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """28228: live PC table, real ASL.W2 and position's final MOVE flags.

    This leaf also honestly supports the old supplied-D0 observation. ASL
    defines all CCR bits naturally; unrelated omitted carriers remain None.
    """
    if type(state) is not SceneState or type(frame) is not FirstDeploymentFrame:
        raise ValueError('actual Scene state and current status frame required')
    frame.validate(state,False)
    if frame.target_x is None:
        raise MovementContinuationBoundary(0x28228,frame,'actual selected D0 LONG required')
    frame=first_replace(frame,controller=state.table_at(0x28240).cursor())
    frame=_scene_render_asl_word(SceneRefreshMemory(state),frame,'target_x',low16(frame.target_x),2)
    pointer=frame.controller.long(low16(frame.target_x))
    frame=_duel_scene_store_fields(state,frame,0x00FF700E,pointer,32)
    return _duel_scene_store_fields(state,frame,0x00FF700C,0xC600)


def _wait_duel_action_fields(state: SceneState, frame: FirstDeploymentFrame,
        either: bool, resume_poll: bool=False) -> FirstDeploymentFrame:
    """One closed active/either wait body with the actual six child slots.

    Resume means the previous actual F612 poll stopped for external IRQ
    progress. It skips no business step and never rewrites the mask/ACK.
    """
    if type(either) is not bool or type(resume_poll) is not bool:
        raise ValueError('actual original wait role and poll continuation required')
    frame=_resource_cost_frame(state,frame,0x277DA if either and resume_poll else
        0x27784 if resume_poll else 0x277D0 if either else 0x2777A)
    if not resume_poll:
        frame=_duel_scene_status_fields(state,frame,0x2500)
    while True:
        frame=_duel_scene_frame_ack_fields(state,frame,0x277DA if either else 0x27784,
            arm=not resume_poll)
        resume_poll=False
        value=state.read(0x00FF70FA,2)
        frame,value=_movement_binary_flags(state,frame,value,1,16,True)
        state.write(0x00FF70FA,2,value)
        frame=_duel_scene_call_fields(state,frame,0x27A84,0x277EA if either else 0x27794)
        frame=_movement_test(state,frame,state.read(0x00FF700C,2),16)
        if not frame.status&4:
            continue
        frame=_duel_scene_call_fields(state,frame,0x279E6,0x277F6 if either else 0x277A0)
        if either:
            frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
            frame=_movement_save_longs(state,frame,('target_y',))
            frame=_duel_scene_call_fields(state,frame,0x27A10,0x27800)
            frame=_movement_restore_longs(state,frame,('target_y',))
            frame=_movement_move(state,frame,'target_x',low16(frame.target_x)|low16(frame.target_y),16)
        else:
            frame=_movement_test(state,frame,state.read(0x00FF7018,2),16)
            if frame.status&8:
                frame=_duel_scene_call_fields(state,frame,0x27A10,0x277AC)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&0x70,16)
        if not frame.status&4:
            return _duel_scene_status_fields(state,frame,0x2700)


def wait_active_duel_action_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2777A normal active-side wait; its own outer token remains caller-owned."""
    return _wait_duel_action_fields(state,frame,False)


def wait_either_duel_action_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """277B8 shares the active body whenever either actual BYTE mode is3."""
    frame=_resource_cost_frame(state,frame,0x277B8)
    frame=_movement_compare(state,frame,state.read(0x00FF700A,1),3,8)
    if frame.status&4:
        return _wait_duel_action_fields(state,frame,False)
    frame=_movement_compare(state,frame,state.read(0x00FF700B,1),3,8)
    return _wait_duel_action_fields(state,frame,not bool(frame.status&4))


def continue_duel_action_wait_fields(state: SceneState, frame: FirstDeploymentFrame,
        either: bool=False) -> FirstDeploymentFrame:
    """Resume only the chosen actual F612 poll after real external progress."""
    return _wait_duel_action_fields(state,frame,either,True)


"""Four original duel setup owners: one complete same-Scene field algorithm.

The caller owns the outer token. Only 26DAC, 27D60 and 28018 are local calls;
the second byte lane is a fall-through, not a second invented BSR.
"""


def advance_duel_entry_palette_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """26D86: real two-read entrance shade, preserving the unsigned guard."""
    frame = _resource_cost_frame(state, frame, 0x26D86)
    step = state.read(0xFF70F8, 2)
    frame = _movement_compare(state, frame, step, 16, 16)
    if not frame.status & 1:
        return frame
    frame = _movement_move(state, frame, 'target_x', 15, 16)
    frame = _duel_commit_sub_word_fields(state, frame, 'target_x',
        state.read(0xFF70F8, 2))
    frame = _movement_move(state, frame, 'target_y', 64, 16)
    frame = first_replace(frame, roster=state.table_at(0x28080).cursor())
    frame = _duel_scene_call_fields(state, frame, 0xDEA6, 0x26DAC)
    frame, next_step = _movement_binary_flags(state, frame,
        state.read(0xFF70F8, 2), 1, 16)
    state.write(0xFF70F8, 2, next_step)
    return frame


def upload_duel_officer_name_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """27D1C: a short name gets the original asymmetric two-buffer padding."""
    frame = _resource_cost_frame(state, frame, 0x27D1C)
    frame = _movement_multiply_word(state, frame, 'choice', 6)
    frame = first_replace(frame, roster=state.table_at(0x8A504).cursor())
    frame = first_replace(frame, roster=frame.roster.at(low16(frame.choice)))
    frame = _movement_move(state, frame, 'count', 2, 16)
    frame = _movement_compare(state, frame, frame.roster.word(4), 63, 16)
    if not frame.status & 4:
        return upload_duel_glyph_strip_fields(state, frame)
    frame = _movement_move(state, frame, 'count', 1, 16)
    frame = _movement_move(state, frame, 'distance', low16(frame.target_x), 16)
    frame = _scene_render_asl_word(SceneRefreshMemory(state), frame,
        'distance', low16(frame.distance), 4)
    frame = _movement_move(state, frame, 'distance',
        low16(frame.distance) | low16(frame.target_x), 16)
    frame = _movement_move(state, frame, 'offset_x', 63, 16)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFD300).cursor(),
        controller=state.table_at(0xFFFFD440).cursor())
    while True:
        frame = _duel_actor_store_fields(state, frame, frame.candidates, 0,
            low8(frame.distance), 8)
        frame = first_replace(frame, candidates=frame.candidates.advance(1))
        frame = _duel_actor_store_fields(state, frame, frame.controller, 0,
            low8(frame.distance), 8)
        frame = first_replace(frame, controller=frame.controller.advance(1))
        remaining = u16(low16(frame.offset_x) - 1)
        frame = first_replace(frame, offset_x=replace_word(frame.offset_x, remaining))
        if remaining == 65535:
            # BRA 27D5A skips LEA 27D56: A1 stays beyond the 64-byte fill.
            return _upload_duel_glyph_buffers_fields(state, frame)


def upload_duel_glyph_strip_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """27D56 is a genuine middle entry of the one name-upload owner."""
    frame = _resource_cost_frame(state, frame, 0x27D56)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFD300).cursor())
    return _upload_duel_glyph_buffers_fields(state, frame)


def _upload_duel_glyph_buffers_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """27D5A: sole AE8A glyph decoder, then 96 actual LONG VDP writes."""
    frame = _duel_scene_call_fields(state, frame, 0xAE8A, 0x27D60)
    frame = first_replace(frame, roster=state.table_at(0xFFFFD300).cursor(),
        auxiliary=state.table_at(0xC00000))
    frame = _movement_move(state, frame, 'target_x', 95, 16)
    while True:
        value = frame.roster.long(0)
        frame = first_replace(frame, roster=frame.roster.advance(4))
        frame = _duel_actor_store_fields(state, frame, frame.auxiliary, 0, value, 32)
        remaining = u16(low16(frame.target_x) - 1)
        frame = first_replace(frame, target_x=replace_word(frame.target_x, remaining))
        if remaining == 65535:
            return frame


def clear_duel_text_plane_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """27D76: real CLR read, VDP command and 640 non-elided pattern writes."""
    frame = _resource_cost_frame(state, frame, 0x27D76)
    frame = _duel_scene_store_fields(state, frame, 0xFFFFD100, 0, clear=True)
    frame = _duel_scene_store_fields(state, frame, 0xC00004, 0x46000003, 32)
    frame = first_replace(frame, auxiliary=state.table_at(0xC00000))
    frame = _movement_move_long(state, frame, 'target_x', 0x11111111)
    frame = _movement_move(state, frame, 'target_y', 639, 16)
    while True:
        frame = _duel_actor_store_fields(state, frame, frame.auxiliary, 0,
            frame.target_x, 32)
        remaining = u16(low16(frame.target_y) - 1)
        frame = first_replace(frame, target_y=replace_word(frame.target_y, remaining))
        if remaining == 65535:
            return frame


def decode_duel_byte_lanes_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """28012: physical D0/A1 MOVEM and one BSR, then the second-lane tail."""
    frame = _resource_cost_frame(state, frame, 0x28012)
    frame = _movement_save_longs(state, frame, ('target_x', 'candidates'))
    frame = _duel_scene_call_fields(state, frame, 0x2801E, 0x28018)
    frame = _movement_restore_longs(state, frame, ('target_x', 'candidates'))
    frame = first_replace(frame, candidates=frame.candidates.advance(1))
    return decode_duel_byte_lane_fields(state, frame)


def _duel_lane_emit_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: Word) -> FirstDeploymentFrame:
    """The interleaved destination advances by two; MOVE.B changes NZVC only."""
    frame = _duel_actor_store_fields(state, frame, frame.candidates, 0, value, 8)
    return first_replace(frame, candidates=frame.candidates.advance(2))


def decode_duel_byte_lane_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2801E sole four-kind lane decoder; packet overrun is not clamped."""
    frame = _resource_cost_frame(state, frame, 0x2801E)
    while True:
        frame = _movement_test(state, frame, low16(frame.target_x), 16)
        if frame.status & 4:
            return frame
        frame = _movement_move(state, frame, 'target_y', 0, 16)
        token = frame.roster.byte(0)
        frame = first_replace(frame, roster=frame.roster.advance(1))
        frame = _movement_move(state, frame, 'target_y', token, 8)
        if not frame.status & 8:
            kind = 'literal'
        else:
            frame = _postbattle_bit_fields(frame, bool(frame.target_y & 64))
            state.sr = (state.sr & 65504) | frame.status
            if frame.status & 4:
                kind = 'repeat'
                frame = _movement_move(state, frame, 'target_y',
                    low16(frame.target_y) & 63, 16)
            else:
                frame = _postbattle_bit_fields(frame, bool(frame.target_y & 32))
                state.sr = (state.sr & 65504) | frame.status
                kind = 'pair' if frame.status & 4 else 'ascending'
                frame = _movement_move(state, frame, 'target_y',
                    low16(frame.target_y) & 31, 16)
            value = frame.roster.byte(0)
            frame = first_replace(frame, roster=frame.roster.advance(1))
            frame = _movement_move(state, frame, 'unit', value, 8)
            if kind == 'pair':
                value = frame.roster.byte(0)
                frame = first_replace(frame, roster=frame.roster.advance(1))
                frame = _movement_move(state, frame, 'count', value, 8)
        while True:
            if kind == 'literal':
                value = frame.roster.byte(0)
                frame = first_replace(frame, roster=frame.roster.advance(1))
                frame = _duel_lane_emit_fields(state, frame, value)
            else:
                frame = _duel_lane_emit_fields(state, frame, low8(frame.unit))
                if kind == 'pair':
                    frame = _duel_lane_emit_fields(state, frame, low8(frame.count))
            frame, remaining = _movement_binary_flags(state, frame,
                low16(frame.target_x), 2 if kind == 'pair' else 1, 16, True)
            frame = first_replace(frame, target_x=replace_word(frame.target_x, remaining))
            if kind == 'ascending':
                frame = _movement_add_word(state, frame, 'unit', 1)
            count = u16(low16(frame.target_y) - 1)
            frame = first_replace(frame, target_y=replace_word(frame.target_y, count))
            if count == 65535:
                break


def _duel_lane_legacy_fields(state: SceneState, source: Cursor,
        destination: Cursor, length: Word, repeat_value: Long, pair_value: Long,
        length_carrier: Long | None, count_carrier: Long | None,
        stack: Cursor | None, target: Long) -> FirstDeploymentFrame:
    """Only explicit old observations are recorded; no missing high word or X."""
    source = _live_cursor(state, source)
    destination = _live_cursor(state, destination)
    length = uint(length, 16, 'length')
    repeat_value = uint(repeat_value, 32, 'repeat value')
    pair_value = uint(pair_value, 32, 'pair value')
    if length_carrier is not None:
        uint(length_carrier, 32)
        if low16(length_carrier) != length:
            raise ValueError('lane length must agree with actual caller')
    if count_carrier is not None:
        uint(count_carrier, 32)
    if stack is not None:
        stack = _live_cursor(state, stack)
    entered = first_replace(FirstDeploymentFrame.unobserved(),
        target_x=length_carrier, target_y=count_carrier, unit=repeat_value,
        count=pair_value, roster=source, candidates=destination, stack_cursor=stack)
    entered.validate(state, False)
    raise MovementContinuationBoundary(target, entered,
        'legacy lane observations omit live D4-D7/A2-A6 and CCR/X; use the full lane core')


def _duel_lane_fields_to_observations(frame: FirstDeploymentFrame) -> DuelLaneResult:
    """Compatibility result is just the sole current-field projection."""
    return DuelLaneResult(frame.roster, frame.candidates, low16(frame.target_x),
        frame.unit, frame.count, frame.target_x, frame.target_y)


def _duel_scene_indexed_action_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int) -> tuple[str, FirstDeploymentFrame]:
    """2756E owns27572 once; the discarded LONG is never treated as a PC test."""
    stack=frame.stack_cursor.advance(-4)
    stack.set_long(0,0x27572)
    entered=first_replace(frame,stack_cursor=stack)
    from ..high_level_dynamic_flows.business_duel import execute_indexed_duel_action_fields
    phase,returned=execute_indexed_duel_action_fields(state,entered,target)
    if phase=='fade':
        # The child's actual MOVE.L(A7)+ already discarded this physical
        # LONG. Even an aliased value only becomes D0; BRA26D46 is fixed.
        return phase,returned
    if phase!='return':
        raise ValueError('actual ordinary or fixed-fade action result required')
    actual=returned.stack_cursor.long(0)
    returned=first_replace(returned,stack_cursor=returned.stack_cursor.advance(4))
    if actual!=0x27572:
        raise MovementContinuationBoundary(actual,returned,'actual action RTS reaches an unowned return address')
    return 'next_frame_clear',returned


def perform_selected_duel_action_result_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> tuple[str, FirstDeploymentFrame]:
    """27534: actual side-relative JSR entry, no guessed handler or fake return."""
    frame=_resource_cost_frame(state,frame,0x27534)
    frame=_movement_move(state,frame,'target_x',0xAC,16)
    frame=_duel_scene_call_fields(state,frame,0x808A,0x2753E)
    frame=_duel_scene_status_fields(state,frame,0x2700)
    frame=_duel_scene_call_fields(state,frame,0x27D76,0x27546)
    frame=first_replace(frame,roster=state.table_at(0x00FF7050).cursor(),candidates=state.table_at(0x00FF70A0).cursor())
    frame=_movement_test(state,frame,state.read(0x00FF7018,2),16)
    if frame.status&8:
        frame=first_replace(frame,roster=state.table_at(0x00FF70A0).cursor(),candidates=state.table_at(0x00FF7050).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0x00FF7018,2),16)
    frame=_scene_render_asl_word(SceneRefreshMemory(state),frame,'target_x',low16(frame.target_x),2)
    target=u32(0x27576+s16(low16(frame.target_x)))
    return _duel_scene_indexed_action_fields(state,frame,target)
