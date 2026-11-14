"""Scene-object scheduling, live sprites, movement and action planning.

Probable role names organize confirmed original operations. Dynamic phase
and action targets are genuine typed boundaries. Shared source tails are
called once, media remain external read-only inputs, and quirks are retained.
"""
from dataclasses import replace
from .domain import (SceneState, Table, Cursor, Word, Long, Boundary,
    StackContinuation, VideoPlaneAddress,
    checked_state, checked_table, checked_cursor, uint, u8, u16, u32, s16,
    low8, low16, high16, replace_byte, replace_word, swap_words,
    negative_word, divu_retained, descending_inclusive)
from .contexts_objects import (SceneRenderFrame, SpriteBatchContext,
    SpriteBatchResult, SceneObjectContext, CoordinateIntegrationOutcome, ObjectPositionOffset,
    ObjectOverlapOutcome, ActionPlanOutcome, ObjectActionContext,
    ObjectPhaseDispatch, ObjectActionDispatch, checked_context,
    SceneControllerFrame, SceneControllerConditions, SceneControllerOutcome,
    checked_controller_frame)

from .contexts_objects import SceneActionPlanFields

# Existing same-state frame vocabulary, no new SOURCE/State union.
from .contexts_scene import (
    SceneRefreshMemory, SceneRefreshBoundary, FirstDeploymentFrame, first_replace, _first_word, _first_byte, _first_long, _scene_refresh_emit, _scene_refresh_flags, _scene_refresh_decrement
)


def _ram(state, name):
    return state.table('ram_' + name)


def _shift_word(carrier, shift):
    return replace_word(carrier, u16(low16(carrier) << shift))


def _read_pointer(state, table, offset):
    return state.table_at(table.long(offset))


def _scene_move_conditions(value, bits):
    value &= (1 << bits) - 1
    return SceneControllerConditions(False, value == 0,
                                     bool(value & (1 << (bits - 1))), False)


def _scene_compare_conditions(left, right, bits):
    mask, sign = (1 << bits) - 1, 1 << (bits - 1)
    left, right = left & mask, right & mask
    difference = (left - right) & mask
    return SceneControllerConditions(left < right, difference == 0,
        bool(difference & sign), bool((left ^ right) & (left ^ difference) & sign))


def _scene_add_conditions(left, right, bits):
    mask, sign = (1 << bits) - 1, 1 << (bits - 1)
    left, right = left & mask, right & mask
    result = (left + right) & mask
    return SceneControllerConditions(left + right > mask, result == 0,
        bool(result & sign), bool(~(left ^ right) & (left ^ result) & sign))


def _scene_shift_conditions(value, shift):
    """Documented ASL.W observations, not X or full SR/IRQ state."""
    word = low16(value)
    result = u16(word << shift)
    signs = word >> (15 - shift)
    overflow = signs not in (0, (1 << (shift + 1)) - 1)
    return SceneControllerConditions(bool(word & (1 << (16 - shift))),
        result == 0, negative_word(result), overflow)


def _scene_projection(frame):
    return SceneRenderFrame(frame.x, frame.y, frame.attributes,
                            frame.palette, frame.tile, frame)


def _consume_scene_return(state, frame, continuation):
    """RTS reads the actual stack token; an altered target is not guessed."""
    actual = frame.stack.long()
    if actual != continuation:
        raise Boundary('scene return-token alias left the known continuation',
                       actual, frame)
    return replace(frame, stack=frame.stack.advance(4))


def _scene_call(state, frame, function, continuation):
    """One known ordinary call, with the callee's actual entry stack view.

    The known instruction's continuation is physically written before the
    callee. IRQ, arbitrary entry tokens and a CPU model are not invented.
    """
    called = replace(frame, stack=frame.stack.advance(-4))
    called.stack.set_long(0, uint(continuation, 32))
    actual = function(state, called)
    if type(actual) is not SceneControllerFrame:
        raise Boundary('ordinary scene call requires complete current frame return')
    actual.validate(state)
    return _consume_scene_return(state, actual, continuation)


def _scene_service_call(state, frame, entry, continuation):
    called = replace(frame, stack=frame.stack.advance(-4))
    called.stack.set_long(0, uint(continuation, 32))
    actual = state.service_at(entry, called)
    if type(actual) is not SceneControllerFrame:
        raise Boundary('complete scene service must return actual current frame')
    actual.validate(state)
    return _consume_scene_return(state, actual, continuation)


def _scene_action_call(state, frame, function, continuation):
    """Known caller consumes one ordinary return; preserve consumed metadata.

    A callee reports a continuation it has already consumed. This helper never
    pops that token again, nor substitutes a token value for physical memory.
    """
    called = replace(frame, stack=frame.stack.advance(-4))
    called.stack.set_long(0, uint(continuation, 32))
    actual = function(state, called)
    if type(actual) is SceneControllerFrame:
        actual = SceneControllerOutcome(actual, None)
    if type(actual) is not SceneControllerOutcome:
        raise Boundary('actual scene action outcome required')
    actual.validate(state)
    return SceneControllerOutcome(_consume_scene_return(state, actual.frame, continuation),
                                  actual.discarded_continuation)


def integrate_scene_coordinates(state: SceneState) -> CoordinateIntegrationOutcome:
    """Legacy observations are derived from the sole live field core."""
    actual = integrate_scene_coordinates_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())
    return CoordinateIntegrationOutcome(actual.target_x,actual.target_y)


def _normalize_object_squad_fields(state):
    frame = normalize_object_squad_size_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())
    return frame.target_x,frame.target_y


def normalize_object_squad_size(state: SceneState) -> Long:
    """Legacy scalar projection of the unique live squad-size transaction."""
    return _normalize_object_squad_fields(state)[0]


def normalize_object_squad_size_complete(state, context):
    fields = normalize_object_squad_size_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,context))
    return _scene_controller_legacy_projection(state,fields)


def cycle_special_scene_palette_complete(state, context):
    actual = cycle_special_scene_palette_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,context))
    return _scene_controller_legacy_projection(state,actual)


def clear_scene_object_label_plane_complete(state, context):
    fields = clear_scene_object_label_plane_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,context))
    return _scene_controller_legacy_projection(state,fields)


def read_object_action_mode(state: SceneState, actor: Table) -> Long:
    checked_table(actor,state)
    actual = read_object_action_mode_fields(SceneRefreshMemory(state),first_replace(FirstDeploymentFrame.unobserved(),auxiliary=actor.cursor()))
    return actual.target_x


def offset_scene_object_position_complete(state, context):
    actual = offset_scene_object_position_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,context))
    return _scene_controller_legacy_projection(state,actual)


def probe_scene_object_overlap_complete(state, context):
    actual = probe_scene_object_overlap_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,context))
    return _scene_controller_legacy_projection(state,actual)


def probe_opposing_object_overlap_complete(state, context):
    actual = probe_opposing_object_overlap_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,context))
    return _scene_controller_legacy_projection(state,actual)


def rebuild_depth_sorted_object_queue_complete(state, context):
    actual = rebuild_depth_sorted_object_queue_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,context))
    return _scene_controller_legacy_projection(state,actual)


def dispatch_scene_object_phase_complete(state: SceneState,
        context: SceneControllerFrame) -> SceneControllerOutcome:
    actual = dispatch_scene_object_phase_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,context))
    return SceneControllerOutcome(_scene_controller_legacy_projection(state,actual),None)


def distribute_secondary_city_battle_progress(state: SceneState) -> None:
    """1C5E2: build once, then enter the already-owned 1C586 allocation tail."""
    checked_state(state)
    from .business_reuse import (build_battlefield_outcome_candidates,
                                 distribute_battle_progress_tail)
    count = build_battlefield_outcome_candidates(state)
    budget = u16(_ram(state, 'efba').word() << 1)
    distribute_battle_progress_tail(state, count, budget)


def _append_sprite_entries_complete(state, context):
    actual = _append_object_sprite_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,context))
    return _scene_controller_legacy_projection(state,actual)


def _restore_scene_sprite_saved(state, frame, destination_role):
    """Compatibility projection of the same three live LONG readbacks."""
    from .business_scene import _scene_render_restore_sprite
    actual = _scene_render_restore_sprite(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,frame))
    return _scene_controller_legacy_projection(state,actual)


def _append_sprite_entries(state, context):
    checked_context(context, SpriteBatchContext, state)
    frame = checked_controller_frame(context.frame, state)
    actual = _append_sprite_entries_complete(state, replace(frame, source=context.source))
    return SpriteBatchResult(actual.source, _scene_projection(actual))


def append_scene_center_marker_complete(state: SceneState,
        context: SceneControllerFrame) -> SceneControllerFrame:
    actual = append_scene_center_marker_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,context))
    return _scene_controller_legacy_projection(state,actual)


def draw_active_scene_object_complete(state: SceneState,
        context: SceneControllerFrame) -> SceneControllerOutcome:
    actual = draw_active_scene_object_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,context))
    return SceneControllerOutcome(_scene_controller_legacy_projection(state,actual),None)


def plan_scene_object_action_complete(state, context):
    """Old current-frame API projects the sole planner and actual discard token."""
    outcome = plan_scene_object_action_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,context))
    return SceneControllerOutcome(_scene_controller_legacy_projection(state,outcome.frame),outcome.discarded_continuation)


def _select_scene_object_action_complete(state, context, secondary):
    """Historical helper is only a projection of the whole original owner."""
    return update_selected_object_action_complete(state,context)


def update_selected_object_action_complete(state: SceneState,
        context: SceneControllerFrame) -> SceneControllerOutcome:
    actual = update_selected_object_action_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,context))
    return SceneControllerOutcome(_scene_controller_legacy_projection(state,actual),None)


def resume_selected_object_action_complete(state, context):
    actual = update_selected_object_action_fields(SceneRefreshMemory(state),
        _scene_controller_legacy_fields(state,context),primary_middle=True)
    return SceneControllerOutcome(_scene_controller_legacy_projection(state,actual),None)


def advance_scene_object_actions_complete(state: SceneState,
        context: SceneControllerFrame) -> SceneControllerOutcome:
    actual = advance_scene_object_actions_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,context))
    return SceneControllerOutcome(_scene_controller_legacy_projection(state,actual),None)


def initialize_scene_object_video_complete(state: SceneState,
        context: SceneControllerFrame) -> SceneControllerFrame:
    """Legacy NZVC has no X; require the real missing entry observation."""
    fields = _scene_controller_legacy_fields(state,context)
    return _scene_controller_legacy_projection(state,
        initialize_scene_object_video_fields(SceneRefreshMemory(state),fields))


def _reset_object_action_controls(state):
    _reset_object_action_controls_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def initialize_scene_object_roster_complete(state: SceneState,
        context: SceneControllerFrame) -> SceneControllerFrame:
    fields = initialize_scene_object_roster_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,context))
    return _scene_controller_legacy_projection(state,fields)


def _scene_video_command(state, retained):
    return _scene_object_video_command_fields(SceneRefreshMemory(state),
        first_replace(FirstDeploymentFrame.unobserved(),target_x=retained)).target_x


def cycle_special_scene_palette(state, context=None):
    """Legacy effects-only projection; full live operands remain mandatory."""
    cycle_special_scene_palette_complete(state, checked_controller_frame(context, state))


def clear_scene_object_label_plane(state, context=None):
    clear_scene_object_label_plane_complete(state, checked_controller_frame(context, state))


def offset_scene_object_position(state, actor, offset, context=None):
    checked_table(actor, state)
    checked_context(offset, ObjectPositionOffset, state)
    frame = checked_controller_frame(context, state)
    offset_scene_object_position_complete(state, replace(frame, actor=actor,
        x=replace_word(frame.x, offset.horizontal), y=replace_word(frame.y, offset.vertical)))


def probe_scene_object_overlap(state, actor, offset, context=None):
    checked_table(actor, state)
    checked_context(offset, ObjectPositionOffset, state)
    frame = checked_controller_frame(context, state)
    actual = probe_scene_object_overlap_complete(state, replace(frame, actor=actor,
        x=replace_word(frame.x, offset.horizontal), y=replace_word(frame.y, offset.vertical)))
    return ObjectOverlapOutcome(low16(actual.x) != 0, actual.traversal)


def probe_opposing_object_overlap(state, actor, offset, context=None):
    checked_table(actor, state)
    checked_context(offset, ObjectPositionOffset, state)
    frame = checked_controller_frame(context, state)
    actual = probe_opposing_object_overlap_complete(state, replace(frame, actor=actor,
        x=replace_word(frame.x, offset.horizontal), y=replace_word(frame.y, offset.vertical)))
    return ObjectOverlapOutcome(low16(actual.x) != 0, actual.traversal)


def rebuild_depth_sorted_object_queue(state, context=None):
    return rebuild_depth_sorted_object_queue_complete(state, checked_controller_frame(context, state))


def append_scene_center_marker(state, context):
    return _scene_projection(append_scene_center_marker_complete(state,
        checked_controller_frame(context, state)))


def draw_active_scene_object(state, context):
    checked_context(context, SceneObjectContext, state)
    frame = checked_controller_frame(context.frame, state)
    actual = draw_active_scene_object_complete(state, replace(frame, actor=context.actor))
    return _scene_projection(actual.frame)


def plan_scene_object_action(state, actor, continuation, context=None):
    checked_table(actor, state)
    if type(continuation) is not StackContinuation:
        raise ValueError('explicit legacy continuation required')
    frame = checked_controller_frame(context, state)
    actual = plan_scene_object_action_complete(state, replace(frame, actor=actor))
    return ActionPlanOutcome(actual.discarded_continuation is not None, actual.frame.x)


def update_selected_object_action(state, context):
    checked_context(context, SceneObjectContext, state)
    actual = update_selected_object_action_complete(state,
        replace(checked_controller_frame(context.frame, state), actor=context.actor))
    return _scene_projection(actual.frame)


def advance_scene_object_actions(state, context):
    actual = advance_scene_object_actions_complete(state, checked_controller_frame(context, state))
    return _scene_projection(actual.frame)


def initialize_scene_object_video(state, context):
    return _scene_projection(initialize_scene_object_video_complete(state,
        checked_controller_frame(context, state)))


def initialize_scene_object_roster(state, context):
    return _scene_projection(initialize_scene_object_roster_complete(state,
        checked_controller_frame(context, state)))


def dispatch_scene_object_phase(state, context):
    actual = dispatch_scene_object_phase_complete(state, checked_controller_frame(context, state))
    return _scene_projection(actual.frame)


def _clear_controller_sprite_plane(state, frame):
    from .business_reuse import clear_video_sprite_plane
    actual = clear_video_sprite_plane(state, frame.row_count)
    return replace(frame, row_count=actual.response, layer=actual.variation,
        actor=actual.destination, conditions=_scene_move_conditions(0, 32))


def _copy_controller_palette(state, frame):
    from .business_scene import copy_scene_palette_variant_complete
    actual = copy_scene_palette_variant_complete(state, frame.x, frame.layer)
    return replace(frame, x=actual.index_carrier, layer=actual.count_carrier,
        destination=actual.directory, directory=actual.source, parameters=actual.destination,
        conditions=SceneControllerConditions(actual.carry, actual.zero,
                                              actual.negative, actual.overflow))


def _enqueue_controller_sound(state, frame):
    from .business_reuse import enqueue_sound_command
    enqueue_sound_command(state, low8(frame.x))
    return replace(frame, conditions=_scene_move_conditions(0, 16))


def _wait_controller_frame_ack(state, frame):
    from .business_reuse import wait_for_scene_sound_byte
    wait_for_scene_sound_byte(state)
    return replace(frame, conditions=_scene_move_conditions(0, 8))


def integrate_scene_coordinates_complete(state, frame):
    actual = integrate_scene_coordinates_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,frame))
    return _scene_controller_legacy_projection(state,actual)


def run_scene_object_controller_complete(state: SceneState,
        context: SceneControllerFrame) -> SceneControllerOutcome:
    """The historical interface only projects the one actual controller core."""
    frame = run_scene_object_controller_fields(SceneRefreshMemory(state),
        _scene_controller_legacy_fields(state,context))
    return SceneControllerOutcome(_scene_controller_legacy_projection(state,frame),None)


def run_scene_object_controller(state, context):
    """Legacy five-operand projection, never a fabricated complete frame."""
    return _scene_projection(run_scene_object_controller_complete(state,
        checked_controller_frame(context, state)).frame)

def _scene_controller_entry_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        target: Long, defines_status: bool = False) -> FirstDeploymentFrame:
    """Require the actual eight D/A values; only 3D654 itself defines X.

    The historical controller has NZVC but no observed X. Its first real
    MOVE #2700,SR can supply that missing value; the video child cannot.
    """
    if type(memory) is not SceneRefreshMemory or type(frame) is not FirstDeploymentFrame:
        raise ValueError('existing Scene memory and actual full fields required')
    frame.validate(memory.state,False)
    if frame.stack_cursor is None or any(value is None for value in (
            frame.target_x,frame.target_y,frame.unit,frame.count,frame.distance,
            frame.offset_x,frame.offset_y,frame.choice,frame.roster,frame.candidates,
            frame.controller,frame.scan,frame.opponent,frame.scratch,frame.auxiliary)):
        raise SceneRefreshBoundary(target,frame,None)
    if defines_status:
        frame = memory.status_word(frame,0x2700)
    elif frame.status is None:
        raise SceneRefreshBoundary(target,frame,None)
    return memory.frame(frame)

def _scene_controller_legacy_fields(state, context) -> FirstDeploymentFrame:
    """Observe existing complete legacy values, without an invented X bit."""
    frame = checked_controller_frame(context,state)
    memory = SceneRefreshMemory(state)
    destination = memory.cursor_at(frame.destination.carrier) if type(frame.destination) is VideoPlaneAddress else frame.destination
    directory = frame.directory.cursor() if type(frame.directory) is Table else frame.directory
    parameters = frame.parameters.cursor() if type(frame.parameters) is Table else frame.parameters
    limits = frame.limits.cursor() if type(frame.limits) is Table else frame.limits
    actor = frame.actor.cursor() if type(frame.actor) is Table else frame.actor
    return FirstDeploymentFrame(frame.x,frame.y,frame.attributes,frame.palette,
        frame.tile,frame.extent,frame.row_count,frame.layer,frame.source,
        destination,directory,parameters,limits,frame.traversal,actor,frame.stack,None)

def _scene_controller_legacy_projection(state, frame: FirstDeploymentFrame) -> SceneControllerFrame:
    """Project actual full returns; never synthesize unobserved upper bits."""
    SceneRefreshMemory(state).frame(frame)
    conditions = SceneControllerConditions(bool(frame.status & 1),bool(frame.status & 4),
        bool(frame.status & 8),bool(frame.status & 2))
    return SceneControllerFrame(frame.target_x,frame.target_y,frame.unit,frame.count,
        frame.distance,frame.offset_x,frame.offset_y,frame.choice,frame.roster,
        frame.candidates,frame.controller,frame.scan,frame.opponent,frame.scratch,
        frame.auxiliary,frame.stack_cursor,conditions)

def _scene_object_video_command_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Actual MOVE.W F606 / ANDI.B BF / VDP WORD write, one shared core."""
    memory.sync_status(frame)
    frame = _first_word(frame,'target_x',memory.state.read(0xFFFFF606,2))
    frame = _first_byte(frame,'target_x',low8(frame.target_x) & 0xBF)
    return _scene_refresh_emit(memory,frame,0xC00004,2,low16(frame.target_x))

def _scene_object_call_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        target: Long, continuation: Long) -> FirstDeploymentFrame:
    """Closed genuine child pairs, using the one existing physical slot core.

    Unlifted NZVC-only renderers do not masquerade as full ABI callees.
    Their original token is physically present before the boundary.
    The planner uses its specific nonlocal bridge, not this ordinary RTS helper.
    """
    from ..high_level_gameplay_flow.business_battle import _presentation_call_fields
    from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
    if (target,continuation) not in ((26830, 251500), (252320, 251510), (240532, 251520), (240160, 251550), (240266, 251554), (262940, 251568), (268278, 251870), (32906, 251882), (33736, 251898), (242312, 251906), (260240, 251910), (239992, 251914), (253112, 251918), (262972, 251924), (242236, 251930), (252132, 251934), (240466, 252438), (240466, 252452), (240466, 252466), (240466, 252480), (240466, 252494), (240334, 252528), (240334, 252562), (240334, 252590), (240334, 252618), (243490, 268364), (243490, 268396), (243490, 268434), (259266, 268460), (243490, 268622), (265364, 263248), (263178, 262976), (263238, 263000), (243490, 265460), (266700, 265470), (265512, 265474), (266658, 266596), (266588, 267518), (267514, 266758), (267514, 266798), (267514, 266816), (267514, 266834), (267514, 266884), (267514, 266924), (267514, 266942), (267514, 266960), (267514, 266994), (267514, 267024), (267514, 267054), (267514, 267084), (267514, 267124), (267514, 267142), (267514, 267160), (267514, 267190), (267514, 267208), (267514, 267226), (267514, 267256), (267514, 267274), (267514, 267292), (267514, 267322), (267514, 267340), (267514, 267358), (32906, 267414)):
        raise ValueError('original scene object child/continuation pair required')
    memory.frame(frame)
    def child(actual_memory,entered):
        scene = SceneRefreshMemory(actual_memory.state)
        if target == 0x68CE:
            from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields
            return clear_video_sprite_plane_fields(scene,entered)
        if target == 0x3D9A0:
            return initialize_scene_object_video_fields(scene,entered)
        if target == 0x3AB52:
            from .business_scene import write_vdp_swapped_byte_rle_stream_fields
            return write_vdp_swapped_byte_rle_stream_fields(scene,entered)
        if target == 0x3AACE:
            from .business_scene import read_vdp_plane_rle_rows_fields
            return read_vdp_plane_rle_rows_fields(scene,entered)
        if target == 0x3ab94:
            from .business_scene import copy_scene_palette_variant_fields
            return copy_scene_palette_variant_fields(scene,entered)
        if target == 0x3aa20:
            from .business_scene import begin_scene_palette_darken_fields
            return begin_scene_palette_darken_fields(scene,entered)
        if target == 0x3aa8a:
            from .business_scene import snapshot_and_clear_scene_palette_fields
            return snapshot_and_clear_scene_palette_fields(scene,entered)
        if target == 0x4031c:
            return clear_scene_object_label_plane_fields(scene,entered)
        if target == 0x417f6:
            return initialize_scene_object_roster_fields(scene,entered)
        if target == 0x3f4c2:
            return normalize_object_squad_size_fields(scene,entered)
        if target == 0x3B722:
            from .business_scene import sample_random_preserving_seed_fields
            return sample_random_preserving_seed_fields(scene,entered)
        if target == 0x3b288:
            return append_scene_center_marker_fields(scene,entered)
        if target == 0x3f890:
            return cycle_special_scene_palette_fields(scene,entered)
        if target == 0x3d8e4:
            return integrate_scene_coordinates_fields(scene,entered)
        if target == 0x3B23C:
            from .business_scene import finish_actor_sprite_chains_fields
            return finish_actor_sprite_chains_fields(scene,entered)
        if target == 0x3dcb8:
            return dispatch_scene_object_phase_fields(scene,entered)
        if target == 0x4033c:
            return advance_scene_object_actions_fields(scene,entered)
        if target == 0x4040a:
            return rebuild_depth_sorted_object_queue_fields(scene,entered)
        if target == 0x40446:
            return draw_active_scene_object_fields(scene,entered)
        if target == 0x40c94:
            return update_selected_object_action_fields(scene,entered)
        if target == 0x40d28:
            return read_object_action_mode_fields(scene,entered)
        if target == 0x411a2:
            return offset_scene_object_position_fields(scene,entered)
        if target == 0x4115c:
            return probe_scene_object_overlap_fields(scene,entered)
        if target == 0x3A978:
            from .business_scene import advance_scene_palette_fade_fields
            return advance_scene_palette_fade_fields(scene,entered)
        if target == 0x414FA:
            return probe_opposing_object_overlap_fields(scene,entered)
        if target == 0x808A:
            from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields
            return enqueue_sound_command_fields(scene,entered)
        if target == 0x83C8:
            from ..high_level_gameplay_flow.business_services import wait_for_scene_sound_byte_fields
            return wait_for_scene_sound_byte_fields(scene,entered)
        raise SceneRefreshBoundary(target,entered,continuation)
    return _presentation_call_fields(BattlePresentationMemory(memory.state),frame,continuation,child)

def initialize_scene_object_video_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3D9A0..3DACC: all thirteen commands, five tile and four plane calls.

    A1 is the actual LONG video-address carrier. The last two indexed pointer
    instructions do not first overwrite A0 with their directory address.
    """
    from .business_scene import _scene_render_asl_word
    frame = _scene_controller_entry_fields(memory,frame,0x3D9A0)
    for command in (0x8F02,0x8230,0x8330,0x8407,0x8568,0x8700,
                    0x8B00,0x8C81,0x8D35,0x8F02,0x9011,0x9194,0x9200):
        frame = _scene_refresh_emit(memory,frame,0xC00004,2,command)
    for source,destination,continuation in ((0x473E4,0,0x3DA16),
            (0x492E8,0x2000,0x3DA24),(0x4A9A2,0x4000,0x3DA32),
            (0x4C5AC,0x6000,0x3DA40),(0x4E090,0x8000,0x3DA4E)):
        frame = first_replace(frame,roster=memory.cursor_at(source))
        frame = _first_word(frame,'target_x',destination)
        frame = _scene_object_call_fields(memory,frame,0x3AB52,continuation)
    for directory,destination,continuation,has_lea in (
            (0x3DACC,0xE000,0x3DA70,True),(0x3DADC,0xE040,0x3DA92,True),
            (0x3DACC,0xF000,0x3DAAE,False),(0x3DADC,0xF040,0x3DACA,False)):
        frame = _first_long(frame,'target_x',0)
        memory.sync_status(frame)
        frame = _first_byte(frame,'target_x',memory.state.read(0xFFFF80DB,1))
        frame = _scene_render_asl_word(memory,frame,'target_x',low16(frame.target_x),2)
        if has_lea:
            frame = first_replace(frame,roster=memory.cursor_at(directory))
        memory.sync_status(frame)
        pointer = memory.cursor_at(directory,s16(low16(frame.target_x))).long()
        frame = first_replace(frame,roster=memory.cursor_at(pointer),
            candidates=memory.cursor_at(destination))
        frame = _first_long(frame,'offset_x',0x80)
        frame = _scene_object_call_fields(memory,frame,0x3AACE,continuation)
    return memory.sync_status(frame)

def run_scene_object_controller_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3D654: sole full bootstrap, phase restoration, frame loop and restart.

    The two original owned spans exclude the intervening 3D76E..3D7DA area.
    Unknown full-child behavior stops at its actual physical call slot.
    """
    from .business_scene import _scene_render_compare
    frame = _scene_controller_entry_fields(memory,frame,0x3D654,True)
    while True:
        frame = memory.status_word(frame,0x2700)
        frame = _scene_object_video_command_fields(memory,frame)
        frame = _scene_object_call_fields(memory,frame,0x68CE,0x3D66C)
        frame = _scene_refresh_emit(memory,frame,0xFFFFF6C4,2,2)
        frame = _scene_object_call_fields(memory,frame,0x3D9A0,0x3D676)
        frame = _first_long(frame,'target_x',0)
        memory.sync_status(frame)
        frame = _first_byte(frame,'target_x',memory.state.read(0xFFFF80DB,1))
        frame = _scene_object_call_fields(memory,frame,0x3AB94,0x3D680)
        for address in (0xFFFF80CA,0xFFFF80CC,0xFFFF80CE,0xFFFF80D0):
            frame = _scene_refresh_emit(memory,frame,address,2,65535)
        frame = _first_long(frame,'target_x',1)
        frame = _scene_object_call_fields(memory,frame,0x3AA20,0x3D69E)
        frame = _scene_object_call_fields(memory,frame,0x3AA8A,0x3D6A2)
        memory.sync_status(frame)
        phase = memory.state.read(0xFFFF813A,2)
        frame = _scene_render_compare(memory,frame,phase,3,16)
        if phase == 3:
            frame = _scene_object_call_fields(memory,frame,0x4031C,0x3D6B0)
            frame = _scene_refresh_emit(memory,frame,0xFFFF813A,2,0)
            frame = _scene_refresh_emit(memory,frame,0xFFFF813C,2,6)
            memory.state.read(0xFFFF813E,2)
            frame = _scene_refresh_emit(memory,frame,0xFFFF813E,2,0)
            side = memory.state.read(0xFFFF8124,2)
            frame = _scene_refresh_flags(memory,frame,side,2)
            reversed_sides = side != 0
            first = 0xFFFF8278 if reversed_sides else 0xFFFF8178
            second = 0xFFFF8178 if reversed_sides else 0xFFFF8278
            value = memory.state.read(0x00FF706C,2)
            frame = _scene_refresh_emit(memory,frame,first,2,value)
            value = memory.state.read(0x00FF70BC,2)
            frame = _scene_refresh_emit(memory,frame,second,2,value)
            winner = memory.state.read(0x00FF70F0,1)
            frame = _scene_render_compare(memory,frame,winner,1,8)
            destination = 0xFFFF8130 if (winner == 1) != reversed_sides else 0xFFFF8138
            frame = _scene_refresh_emit(memory,frame,destination,2,6)
        else:
            frame = _scene_refresh_emit(memory,frame,0xFFFF8020,2,0)
            frame = _scene_refresh_emit(memory,frame,0xFFFF8024,4,0)
            frame = _first_word(frame,'target_x',0x107)
            frame = first_replace(frame,roster=memory.cursor_at(0xFFFF812A))
            counter = low16(frame.target_x)
            while True:
                memory.sync_status(frame)
                frame.roster.word()
                frame.roster.set_word(0,0)
                frame = _scene_refresh_flags(memory,frame,0,2)
                frame = first_replace(frame,roster=frame.roster.advance(2))
                frame = _scene_refresh_decrement(frame,'target_x',counter)
                counter = u16(counter - 1)
                if counter == 65535:
                    break
            for address in (0xFFFF812A,0xFFFF812C,0xFFFF812E,0xFFFF8130,
                            0xFFFF8132,0xFFFF8134,0xFFFF8136,0xFFFF8138):
                frame = _scene_refresh_emit(memory,frame,address,2,5)
            frame = _scene_refresh_emit(memory,frame,0xFFFF813A,2,9)
            frame = _scene_refresh_emit(memory,frame,0xFFFF813C,2,0)
            frame = _scene_object_call_fields(memory,frame,0x417F6,0x3D7DE)
        frame = _first_word(frame,'target_x',0x8E)
        frame = _scene_object_call_fields(memory,frame,0x808A,0x3D7EA)
        frame = memory.status_word(frame,0x2500)
        while True:
            frame = _scene_refresh_emit(memory,frame,0xFFFFF612,2,0x500)
            frame = _scene_object_call_fields(memory,frame,0x83C8,0x3D7FA)
            memory.state.read(0xFFFFF612,2)
            frame = _scene_refresh_emit(memory,frame,0xFFFFF612,2,0)
            for target,continuation in ((0x3B288,0x3D802),(0x3F890,0x3D806),
                    (0x3A978,0x3D80A),(0x3DCB8,0x3D80E),(0x4033C,0x3D814),
                    (0x3B23C,0x3D81A),(0x3D8E4,0x3D81E)):
                frame = _scene_object_call_fields(memory,frame,target,continuation)
            phase = memory.state.read(0xFFFF813A,2)
            frame = _scene_render_compare(memory,frame,phase,3,16)
            terminal = False
            if phase == 3:
                subphase = memory.state.read(0xFFFF813C,2)
                frame = _scene_render_compare(memory,frame,subphase,3,16)
                if subphase == 3:
                    frame = _scene_refresh_emit(memory,frame,0xFFFF8114,2,1)
                    terminal = True
            if not terminal:
                phase = memory.state.read(0xFFFF813A,2)
                frame = _scene_render_compare(memory,frame,phase,4,16)
                if phase == 4:
                    subphase = memory.state.read(0xFFFF813C,2)
                    frame = _scene_render_compare(memory,frame,subphase,3,16)
                    if subphase == 3:
                        frame = _scene_refresh_emit(memory,frame,0xFFFF8114,2,0)
                        terminal = True
            if not terminal:
                phase = memory.state.read(0xFFFF813A,2)
                frame = _scene_render_compare(memory,frame,phase,5,16)
                if phase == 5:
                    subphase = memory.state.read(0xFFFF813C,2)
                    frame = _scene_render_compare(memory,frame,subphase,3,16)
                    if subphase == 3:
                        # Original phase-five terminal does not write 8114.
                        terminal = True
            if not terminal:
                phase = memory.state.read(0xFFFF813A,2)
                frame = _scene_render_compare(memory,frame,phase,6,16)
                if phase == 6:
                    subphase = memory.state.read(0xFFFF813C,2)
                    frame = _scene_render_compare(memory,frame,subphase,4,16)
                    if subphase == 4:
                        frame = _scene_refresh_emit(memory,frame,0xFFFF8114,2,6)
                        terminal = True
            if terminal:
                frame = memory.status_word(frame,0x2700)
                return _scene_object_video_command_fields(memory,frame)
            frame = _first_byte(frame,'target_x',memory.state.read(0xFFFFF602,1))
            frame = _first_byte(frame,'target_x',low8(frame.target_x) & 0xF0)
            frame = _scene_render_compare(memory,frame,low8(frame.target_x),0xF0,8)
            if low8(frame.target_x) != 0xF0:
                continue
            variant = memory.state.read(0xFFFF80DB,1)
            frame = _scene_render_compare(memory,frame,variant,3,8)
            if variant < 3:
                # ADDQ.B rereads the memory destination; CMP's read is distinct.
                previous = memory.state.read(0xFFFF80DB,1)
                from ..high_level_main_flows.business_movement_support import _movement_binary_flags
                frame,value = _movement_binary_flags(memory.state,frame,previous,1,8)
                memory.sync_status(frame)
                memory.state.write(0xFFFF80DB,1,value)
            break

def _object_clear_word_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        address: Long) -> FirstDeploymentFrame:
    memory.sync_status(frame)
    memory.state.read(address,2)
    return _scene_refresh_emit(memory,frame,address,2,0)

def _object_adjust_word_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        address: Long, amount: Word, subtract: bool = False) -> FirstDeploymentFrame:
    from ..high_level_main_flows.business_movement_support import _movement_binary_flags
    memory.sync_status(frame)
    previous = memory.state.read(address,2)
    frame,value = _movement_binary_flags(memory.state,frame,previous,amount,16,subtract)
    memory.state.write(address,2,value)
    return memory.sync_status(frame)

def _reset_object_action_controls_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    for address in (0xFFFF814C,0xFFFF814E,0xFFFF8150,0xFFFF8152,0xFFFF8154,
                    0xFFFF8156,0xFFFF8158,0xFFFF815A,0xFFFF815C,0xFFFF815E,
                    0xFFFF8160,0xFFFF8162,0xFFFF8164,0xFFFF8166,0xFFFF8168):
        frame = _object_clear_word_fields(memory,frame,address)
    return frame

def normalize_object_squad_size_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3F4C2: sole divisor adjustment; original 15/16 cycles are not clamped."""
    from .business_scene import _scene_render_compare
    from ..high_level_main_flows.business_movement_support import _movement_divu_word
    memory.frame(frame)
    while True:
        frame = _first_long(frame,'target_x',0)
        frame = _first_long(frame,'target_y',0)
        memory.sync_status(frame)
        frame = _first_word(frame,'target_x',memory.state.read(0xFFFF80E4,2))
        frame = _first_word(frame,'target_y',memory.state.read(0xFFFF80E8,2))
        count = low16(frame.target_y)
        if count == 0:
            frame = _object_adjust_word_fields(memory,frame,0xFFFF80E8,1)
            continue
        frame = _scene_render_compare(memory,frame,count,15,16)
        if count > 15:
            frame = _object_adjust_word_fields(memory,frame,0xFFFF80E8,1,True)
            continue
        frame = _movement_divu_word(memory.state,frame,'target_x',count,0x3F4E6)
        quotient = low16(frame.target_x)
        frame = _scene_render_compare(memory,frame,quotient,1000,16)
        if quotient > 1000:
            frame = _object_adjust_word_fields(memory,frame,0xFFFF80E8,1)
            continue
        frame = _scene_render_compare(memory,frame,quotient,100,16)
        if quotient <= 100:
            live_count = memory.state.read(0xFFFF80E8,2)
            frame = _scene_render_compare(memory,frame,live_count,1,16)
            if live_count > 1:
                frame = _object_adjust_word_fields(memory,frame,0xFFFF80E8,1,True)
                continue
        frame = _scene_refresh_emit(memory,frame,0xFFFF80EC,2,quotient)
        frame = _first_long(frame,'target_x',swap_words(frame.target_x))
        return _scene_refresh_emit(memory,frame,0xFFFF80F0,2,low16(frame.target_x))

def clear_scene_object_label_plane_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4031C: real command/2048 tile WORDs; no emulated VDP completion."""
    memory.frame(frame)
    frame = _scene_refresh_emit(memory,frame,0xC00004,4,0x40000003)
    frame = first_replace(frame,scratch=memory.cursor_at(0xC00000))
    frame = _first_word(frame,'offset_y',0x400)
    frame = _first_word(frame,'choice',0x7FF)
    counter = 0x7FF
    while True:
        frame = _scene_refresh_emit(memory,frame,frame.scratch.base,2,low16(frame.offset_y))
        frame = _scene_refresh_decrement(frame,'choice',counter)
        counter = u16(counter - 1)
        if counter == 65535:
            return memory.sync_status(frame)

def _object_count_draw_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        continuation: Long, bound: Word, bias: Word) -> FirstDeploymentFrame:
    """Three original rejection gates share only their actual RNG/WORD work."""
    from .business_scene import _scene_render_compare, _scene_render_arithmetic
    while True:
        frame = _scene_object_call_fields(memory,frame,0x3B722,continuation)
        choice = low16(frame.target_x) & 15
        frame = _first_word(frame,'target_x',choice)
        frame = _scene_render_compare(memory,frame,choice,bound,16)
        # The small and the two other gates remain independently editable.
        accepted = choice <= bound if continuation == 0x4184C else choice <= bound
        if accepted:
            frame = _scene_render_arithmetic(memory,frame,'target_x',choice,bias,16)
            return _scene_refresh_emit(memory,frame,0xFFFF80E8,2,low16(frame.target_x))

def initialize_scene_object_roster_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """417F6..41A58: complete count/partition/layout and fifteen-stat-row flow."""
    from .business_scene import _scene_render_compare, _scene_render_arithmetic, _scene_render_asl_word
    from ..high_level_main_flows.business_movement_support import _movement_multiply_word, _movement_divu_word
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(268278, frame, None)
    frame = _first_word(frame, 'target_x', 255)
    frame = first_replace(frame, auxiliary=memory.cursor_at(4294934890))
    counter = 255
    while True:
        frame = _object_clear_word_fields(memory, frame, frame.auxiliary.base)
        frame = first_replace(frame, auxiliary=frame.auxiliary.advance(2))
        frame = _scene_refresh_decrement(frame, 'target_x', counter)
        counter = u16(counter - 1)
        if counter == 65535:
            break
    mode = memory.state.read(4294934746, 1)
    frame = _scene_render_compare(memory, frame, mode, 1, 8)
    if mode == 1:
        return _reset_object_action_controls_fields(memory, frame)
    mode = memory.state.read(4294934746, 1)
    frame = _scene_render_compare(memory, frame, mode, 2, 8)
    if mode == 2:
        return _reset_object_action_controls_fields(memory, frame)
    return _initialize_scene_object_roster_tail_fields(memory, frame)

def _object_shift_word_right_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, name: str, word: Word, amount: Word) -> tuple:
    """LSR.W defines all CCR bits from the observed WORD, even if high is unknown."""
    result = word >> amount
    carry = bool(word & (1 << (amount - 1)))
    frame = _first_word(frame,name,result)
    status = (17 if carry else 0) | (8 if result & 32768 else 0) | (4 if result == 0 else 0)
    return memory.sync_status(first_replace(frame,status=status)),result

def _object_shift_velocity_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, amount: Word) -> FirstDeploymentFrame:
    """ASL.L of the actual zero-extended velocity, including last carry and V."""
    value = frame.target_y
    result = u32(value << amount)
    carry = bool(value & (1 << (32 - amount)))
    signs = (value >> (31 - amount)) & ((1 << (amount + 1)) - 1)
    overflow = signs not in (0,(1 << (amount + 1)) - 1)
    status = (17 if carry else 0) | (8 if result & 2147483648 else 0) | (4 if result == 0 else 0) | (2 if overflow else 0)
    return memory.sync_status(first_replace(frame,target_y=result,status=status))

def integrate_scene_coordinates_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3D8E4: three real split coordinates; low store precedes high store."""
    from .business_scene import _scene_render_arithmetic
    memory.frame(frame)
    for high_address,low_address,velocity_address in (
            (0xFFFF8024,0xFFFF802C,0xFFFF8038),
            (0xFFFF8026,0xFFFF802E,0xFFFF803A),
            (0xFFFF8020,0xFFFF8034,0xFFFF8040)):
        memory.sync_status(frame)
        high = memory.state.read(high_address,2)
        frame = _first_word(frame,'target_x',high)
        if frame.target_x is not None:
            frame = _first_long(frame,'target_x',swap_words(frame.target_x))
        low = memory.state.read(low_address,2)
        # The second MOVE.W after SWAP replaces every unknown entry bit.
        frame = first_replace(frame,target_x=u32((high << 16) | low))
        frame = _scene_refresh_flags(memory,frame,low,2)
        frame = _first_long(frame,'target_y',0)
        velocity = memory.state.read(velocity_address,2)
        frame = _first_word(frame,'target_y',velocity)
        adding = bool(velocity & 32768)
        if adding:
            frame = _first_word(frame,'target_y',velocity & 32767)
        frame = _object_shift_velocity_fields(memory,frame,8)
        frame = _scene_render_arithmetic(memory,frame,'target_x',frame.target_x,frame.target_y,32,not adding)
        frame = _scene_refresh_emit(memory,frame,low_address,2,low16(frame.target_x))
        frame = _first_long(frame,'target_x',swap_words(frame.target_x))
        frame = _scene_refresh_emit(memory,frame,high_address,2,low16(frame.target_x))
    return memory.sync_status(frame)

def cycle_special_scene_palette_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3F890: actual mode/enable branch and three table-backed WORD stores."""
    from .business_scene import _scene_render_compare, _scene_render_bit
    memory.frame(frame)
    memory.sync_status(frame)
    mode = memory.state.read(0xFFFF80DB,1)
    frame = _scene_render_compare(memory,frame,mode,3,8)
    if mode != 3:
        return frame
    enabled = memory.state.read(0xFFFF80C4,1)
    frame = _scene_render_bit(memory,frame,enabled,128)
    if not enabled & 128:
        return frame
    tick = memory.state.read(0xFFFFF320,2)
    frame = _first_word(frame,'target_x',tick)
    frame,shifted_tick = _object_shift_word_right_fields(memory,frame,'target_x',tick,3)
    offset = shifted_tick & 6
    frame = _first_word(frame,'target_x',offset)
    frame = first_replace(frame,roster=memory.cursor_at(0x3F8C4))
    for displacement,address in ((0,0xFFFFFB02),(8,0xFFFFFB04),(16,0xFFFFFB06)):
        frame = _scene_refresh_emit(memory,frame,address,2,frame.roster.word(offset,displacement))
    return memory.sync_status(frame)

def _append_object_sprite_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Sole 3B13C object packet tail: world offsets and the 80-sprite actor list.

    It is not the separate clipped Scene packet entry. Both entries share the
    same BYTE delta math and physical save/readback helpers.
    """
    from .business_scene import (_scene_render_push_longs,_scene_render_restore_sprite,
        _scene_render_compare,_scene_render_bit,_scene_render_arithmetic,
        _scene_render_asl_word,_scene_render_apply_delta)
    from .contexts_scene import _first_shift_word
    from ..high_level_main_flows.business_movement_support import _movement_binary_flags
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x3B13C,frame,None)
    frame = _scene_render_push_longs(memory,frame,(frame.candidates.base,frame.offset_y,frame.offset_x))
    memory.sync_status(frame)
    capacity = memory.state.read(0xFFFFF300,1)
    frame = _scene_render_compare(memory,frame,capacity,80,8)
    if capacity >= 80:
        return memory.sync_status(_scene_render_restore_sprite(memory,frame))
    frame = _first_long(frame,'distance',frame.distance & 65535)
    frame = _first_word(frame,'choice',low16(frame.unit))
    frame = _first_word(frame,'unit',low16(frame.unit) & 0xFFF8)
    frame = _first_word(frame,'choice',low16(frame.choice) & 7)
    frame = _scene_render_asl_word(memory,frame,'choice',low16(frame.choice),2)
    frame = _scene_render_arithmetic(memory,frame,'target_x',low16(frame.target_x),memory.state.read(0xFFFF8020,2),16,True)
    frame = _scene_render_arithmetic(memory,frame,'target_x',low16(frame.target_x),128,16)
    if low16(frame.target_x) & 32768:
        return memory.sync_status(_scene_render_restore_sprite(memory,frame))
    frame = _scene_render_bit(memory,frame,frame.unit,32)
    if frame.unit & 32:
        frame = _scene_render_arithmetic(memory,frame,'target_x',low16(frame.target_x),8,16,True)
    frame = _scene_render_arithmetic(memory,frame,'target_y',low16(frame.target_y),memory.state.read(0xFFFF8022,2),16,True)
    frame = _scene_render_arithmetic(memory,frame,'target_y',low16(frame.target_y),128,16)
    frame = _scene_render_bit(memory,frame,frame.unit,16)
    if frame.unit & 16:
        frame = _scene_render_arithmetic(memory,frame,'target_y',low16(frame.target_y),8,16,True)
    frame = _first_word(frame,'offset_x',0)
    count = memory.state.read(0xFFFFF300,1)
    frame = _first_byte(frame,'offset_x',count)
    frame = _first_shift_word(frame,'offset_x',count,3)
    frame = first_replace(frame,candidates=memory.cursor_at(0xFFFFF800),controller=memory.cursor_at(0xFFFF8044))
    frame = first_replace(frame,candidates=frame.candidates.advance(s16(low16(frame.offset_x))))
    while True:
        # Encoded 3B232 backedge reloads horizontal D6 before every packet.
        frame = _first_word(frame,'offset_y',low16(frame.target_x))
        frame = _first_long(frame,'offset_x',0)
        horizontal = frame.roster.byte()
        frame = _first_byte(frame,'offset_x',horizontal)
        frame = _scene_render_compare(memory,frame,horizontal,128,8)
        if horizontal == 128:
            break
        frame,horizontal_position = _scene_render_apply_delta(memory,frame,32,low16(frame.offset_y))
        frame = _scene_refresh_emit(memory,frame,frame.candidates.base,2,horizontal_position)
        frame = _first_word(frame,'offset_y',low16(frame.target_y))
        frame = _first_byte(frame,'offset_x',frame.roster.byte(0,3))
        frame,vertical_position = _scene_render_apply_delta(memory,frame,16,low16(frame.offset_y))
        # The cached tail repeats BTST7 once; the identical test has no DATA
        # or surviving flag difference and remains in its native owner rows.
        frame = _scene_refresh_emit(memory,frame,frame.candidates.base + 6,2,vertical_position)
        frame = _scene_refresh_emit(memory,frame,frame.candidates.base + 2,1,frame.roster.byte(0,1))
        layer = s16(low16(frame.choice))
        head = frame.controller.long(layer)
        frame = _scene_refresh_flags(memory,frame,head,4)
        if head == 0:
            frame = _scene_refresh_emit(memory,frame,u32(frame.controller.base + layer),4,frame.candidates.base)
            frame = _scene_refresh_emit(memory,frame,u32(frame.controller.base + layer + 0x20),1,memory.state.read(0xFFFFF300,1))
        else:
            frame = first_replace(frame,scan=memory.cursor_at(frame.controller.long(layer,0x40)))
            frame = _scene_refresh_emit(memory,frame,u32(frame.scan.base + 3),1,memory.state.read(0xFFFFF300,1))
        frame = _scene_refresh_emit(memory,frame,u32(frame.controller.base + layer + 0x40),4,frame.candidates.base)
        count = memory.state.read(0xFFFFF300,1)
        frame,new_count = _movement_binary_flags(memory.state,frame,count,1,8)
        memory.sync_status(frame)
        memory.state.write(0xFFFFF300,1,new_count)
        frame = _first_byte(frame,'offset_x',frame.roster.byte(0,1))
        frame = _first_word(frame,'offset_x',low16(frame.offset_x) & 240)
        frame = _scene_render_arithmetic(memory,frame,'offset_x',low8(frame.offset_x),low8(frame.count),8)
        frame = _first_word(frame,'offset_x',low16(frame.offset_x) ^ low16(frame.unit))
        frame = _scene_render_asl_word(memory,frame,'offset_x',low16(frame.offset_x),7)
        frame = _first_byte(frame,'offset_x',low8(frame.offset_x) | frame.roster.byte(0,2))
        frame = _scene_render_arithmetic(memory,frame,'offset_x',low16(frame.offset_x),low16(frame.distance),16)
        frame = _scene_refresh_emit(memory,frame,frame.candidates.base + 4,2,low16(frame.offset_x))
        frame = first_replace(frame,candidates=frame.candidates.advance(8),roster=frame.roster.advance(4))
        capacity = memory.state.read(0xFFFFF300,1)
        frame = _scene_render_compare(memory,frame,capacity,80,8)
        if capacity >= 80:
            break
    return memory.sync_status(_scene_render_restore_sprite(memory,frame))

def append_scene_center_marker_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3B288: actual world origin minus 64 and the original marker stream."""
    from .business_scene import _scene_render_arithmetic
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x3B288,frame,None)
    memory.sync_status(frame)
    frame = _first_word(frame,'target_x',memory.state.read(0xFFFF8020,2))
    frame = _scene_render_arithmetic(memory,frame,'target_x',low16(frame.target_x),64,16,True)
    frame = _first_word(frame,'target_y',memory.state.read(0xFFFF8022,2))
    frame = _scene_render_arithmetic(memory,frame,'target_y',low16(frame.target_y),64,16,True)
    frame = _first_long(frame,'unit',0)
    frame = _first_long(frame,'count',0)
    frame = _first_word(frame,'distance',0)
    frame = first_replace(frame,roster=memory.cursor_at(0x3B2AA))
    return _append_object_sprite_fields(memory,frame)

def draw_active_scene_object_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """40446: sole action gate/animation selection, tail-jumping to 3B13C."""
    from .business_scene import _scene_render_compare,_scene_render_arithmetic,_scene_render_asl_word
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x40446,frame,None)
    memory.sync_status(frame)
    gate = memory.state.read(0xFFFF813E,2)
    frame = _scene_refresh_flags(memory,frame,gate,2)
    if gate == 0:
        frame = _scene_object_call_fields(memory,frame,0x40C94,0x40450)
    frame = _first_word(frame,'target_x',frame.auxiliary.word())
    frame = _first_word(frame,'target_x',low16(frame.target_x) & 255)
    frame = _first_long(frame,'target_y',0)
    frame = first_replace(frame,roster=memory.cursor_at(0x404CC))
    frame = _first_byte(frame,'target_y',frame.roster.byte(low16(frame.target_x)))
    mode = memory.state.read(0xFFFF80DB,1)
    frame = _scene_render_compare(memory,frame,mode,3,8)
    if mode == 3:
        frame = _first_byte(frame,'target_y',frame.roster.byte(low16(frame.target_x),4))
    side = memory.state.read(0xFFFF8124,2)
    frame = _scene_refresh_flags(memory,frame,side,2)
    frame = _scene_render_compare(memory,frame,frame.auxiliary.base,0xFFFF826A,32)
    if (side == 0 and frame.auxiliary.base >= 0xFFFF826A) or (side != 0 and frame.auxiliary.base < 0xFFFF826A):
        frame = _scene_render_arithmetic(memory,frame,'target_y',low16(frame.target_y),96,16)
    frame = _first_word(frame,'target_x',frame.auxiliary.word(0,8))
    frame = _scene_render_asl_word(memory,frame,'target_x',low16(frame.target_x),2)
    frame = _scene_render_arithmetic(memory,frame,'target_y',low16(frame.target_y),low16(frame.target_x),16)
    tick = memory.state.read(0xFFFFF320,2)
    frame = _first_word(frame,'target_x',tick)
    frame,shifted_tick = _object_shift_word_right_fields(memory,frame,'target_x',tick,3)
    frame = _first_word(frame,'target_x',shifted_tick & 3)
    frame = _scene_render_arithmetic(memory,frame,'target_x',low16(frame.target_x),low16(frame.target_y),16)
    frame = _first_word(frame,'distance',low16(frame.target_x))
    frame = _scene_render_asl_word(memory,frame,'target_x',low16(frame.target_x),2)
    pointer = memory.state.read(u32(0x404D4 + s16(low16(frame.target_x))),4)
    frame = first_replace(frame,roster=memory.cursor_at(pointer))
    frame = _first_word(frame,'target_x',frame.auxiliary.word(0,2))
    frame = _first_word(frame,'target_y',frame.auxiliary.word(0,4))
    frame = _first_word(frame,'unit',5)
    frame = _first_long(frame,'count',0)
    frame = _scene_render_asl_word(memory,frame,'distance',low16(frame.distance),1)
    frame = first_replace(frame,candidates=memory.cursor_at(0x407D4))
    frame = _first_word(frame,'distance',frame.candidates.word(low16(frame.distance)))
    return _append_object_sprite_fields(memory,frame)

def dispatch_scene_object_phase_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3DCB8 real indexed JMP: phase0 retains its sole core; phases1..9 enter the existing complete result, confirmation, transfer and exchange BRA facades. No new CALL slot or fabricated input."""
    from .business_scene import _scene_render_asl_word
    memory.frame(frame)
    memory.sync_status(frame)
    phase = memory.state.read(4294934842, 2)
    frame = _first_word(frame, 'target_x', phase)
    frame = _scene_render_asl_word(memory, frame, 'target_x', phase, 2)
    target = u32(253122 + s16(u16(phase << 2)))
    if target == 253122:
        from ..high_level_dynamic_flows.business_early_phase import step_main_scene_phase_fields
        return step_main_scene_phase_fields(memory, frame)
    if target in (253126, 253130, 253134, 253138, 253142, 253146, 253150, 253154, 253158):
        from ..high_level_dynamic_flows.business_early_phase import _allocation_known_fields
        return _allocation_known_fields(memory, frame, target)
    raise SceneRefreshBoundary(target, frame, None)

def rebuild_depth_sorted_object_queue_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4040A: stable 31-depth live scan every sixteenth tick; CLR does not advance."""
    from .business_scene import _scene_render_compare,_scene_render_bit
    memory.frame(frame)
    memory.sync_status(frame)
    tick = memory.state.read(0xFFFFF320,2)
    frame = _first_word(frame,'target_x',tick)
    frame = _first_word(frame,'target_x',tick & 15)
    if tick & 15:
        return frame
    frame = first_replace(frame,scratch=memory.cursor_at(0xFFFF836A))
    frame = _first_long(frame,'target_x',30)
    while True:
        frame = first_replace(frame,auxiliary=memory.cursor_at(0xFFFF816A))
        while True:
            active = frame.auxiliary.byte()
            frame = _scene_render_bit(memory,frame,active,128)
            if active & 128:
                horizontal = frame.auxiliary.word(0,2)
                frame = _first_word(frame,'target_y',horizontal)
                frame,depth = _object_shift_word_right_fields(memory,frame,'target_y',horizontal,4)
                frame = _scene_render_compare(memory,frame,depth,low16(frame.target_x),16)
                if depth == low16(frame.target_x):
                    frame = _scene_refresh_emit(memory,frame,frame.scratch.base,4,frame.auxiliary.base)
                    frame = first_replace(frame,scratch=frame.scratch.advance(4))
            frame = first_replace(frame,auxiliary=frame.auxiliary.advance(16))
            frame = _scene_render_compare(memory,frame,frame.auxiliary.base,0xFFFF836A,32)
            if frame.auxiliary.base >= 0xFFFF836A:
                break
        frame = _scene_refresh_decrement(frame,'target_x',low16(frame.target_x))
        if low16(frame.target_x) == 65535:
            break
    memory.sync_status(frame)
    memory.state.read(frame.scratch.base,4)
    return _scene_refresh_emit(memory,frame,frame.scratch.base,4,0)

def offset_scene_object_position_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """411A2: actual signed WORD axes; negative offsets retain only seven bits."""
    from ..high_level_main_flows.business_movement_support import _movement_binary_flags
    memory.frame(frame)
    if frame.auxiliary is None or frame.target_x is None or frame.target_y is None:
        raise SceneRefreshBoundary(0x411A2,frame,None)
    for displacement,name in ((2,'target_x'),(4,'target_y')):
        magnitude = low16(frame.carrier(name))
        frame = _first_word(frame,'unit',magnitude)
        subtract = bool(magnitude & 32768)
        if subtract:
            magnitude &= 127
            frame = _first_word(frame,name,magnitude)
        memory.sync_status(frame)
        previous = frame.auxiliary.word(0,displacement)
        frame,value = _movement_binary_flags(memory.state,frame,previous,magnitude,16,subtract)
        frame.auxiliary.set_word(0,value,displacement)
    return memory.sync_status(frame)

def probe_scene_object_overlap_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4115C: temporarily move the actor, probe live peers, restore one LONG."""
    from .business_scene import _scene_render_compare,_scene_render_bit
    memory.frame(frame)
    if frame.stack_cursor is None or frame.auxiliary is None:
        raise SceneRefreshBoundary(0x4115C,frame,None)
    memory.sync_status(frame)
    frame = _first_long(frame,'count',frame.auxiliary.long(0,2))
    frame = _scene_object_call_fields(memory,frame,0x411A2,0x41164)
    frame = _first_long(frame,'target_x',0)
    frame = first_replace(frame,scratch=memory.cursor_at(0xFFFF816A))
    while True:
        active = frame.scratch.byte()
        frame = _scene_render_bit(memory,frame,active,128)
        matched = False
        if active & 128:
            frame = _scene_render_compare(memory,frame,frame.auxiliary.base,frame.scratch.base,32)
            if frame.auxiliary.base != frame.scratch.base:
                horizontal = frame.scratch.word(0,2)
                frame = _first_word(frame,'target_y',horizontal)
                actor_horizontal = frame.auxiliary.word(0,2)
                frame = _scene_render_compare(memory,frame,horizontal,actor_horizontal,16)
                if horizontal == actor_horizontal:
                    vertical = frame.scratch.word(0,4)
                    frame = _first_word(frame,'target_y',vertical)
                    actor_vertical = frame.auxiliary.word(0,4)
                    frame = _scene_render_compare(memory,frame,vertical,actor_vertical,16)
                    matched = vertical == actor_vertical
        if matched:
            frame = _first_long(frame,'target_x',1)
            return _scene_refresh_emit(memory,frame,u32(frame.auxiliary.base + 2),4,frame.count)
        frame = first_replace(frame,scratch=frame.scratch.advance(16))
        frame = _scene_render_compare(memory,frame,frame.scratch.base,0xFFFF836A,32)
        if frame.scratch.base >= 0xFFFF836A:
            return _scene_refresh_emit(memory,frame,u32(frame.auxiliary.base + 2),4,frame.count)

def probe_opposing_object_overlap_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """414FA: only the first peer survives when it belongs to the other side."""
    from .business_scene import _scene_render_compare
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x414FA,frame,None)
    frame = _scene_object_call_fields(memory,frame,0x4115C,0x414FE)
    frame = _scene_refresh_flags(memory,frame,low16(frame.target_x),2)
    if low16(frame.target_x):
        frame = _scene_render_compare(memory,frame,frame.auxiliary.base,0xFFFF826A,32)
        secondary = frame.auxiliary.base >= 0xFFFF826A
        frame = _scene_render_compare(memory,frame,frame.scratch.base,0xFFFF826A,32)
        if secondary and frame.scratch.base < 0xFFFF826A:
            return frame
        if not secondary and frame.scratch.base >= 0xFFFF826A:
            return frame
    return memory.sync_status(_first_long(frame,'target_x',0))

def read_object_action_mode_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """40D28 loads the mode; the planner only compares the same live slot."""
    frame = _object_action_mode_slot_fields(memory,frame)
    return memory.sync_status(_first_word(frame,'target_x',frame.roster.word(low16(frame.target_x))))

def update_selected_object_action_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, primary_middle: bool = False) -> FirstDeploymentFrame:
    """Whole noncontinuous 40C94 owner: eligibility, RNG, mode, dynamic tail.

    Planner success has physically discarded its own slot; selection
    returns immediately for the existing outer 40450 bridge. Indexed tails
    remain actual instruction entries, not ROM LONG pointers.
    """
    from .business_scene import _scene_render_compare,_scene_render_asl_word
    memory.frame(frame)
    if frame.auxiliary is None or frame.target_x is None:
        raise SceneRefreshBoundary(0x40C94,frame,None)
    if type(primary_middle) is not bool:
        raise ValueError('actual primary-middle entry selector required')
    if not primary_middle:
        frame = _scene_render_compare(memory,frame,frame.auxiliary.base,0xFFFF826A,32)
    secondary = not primary_middle and frame.auxiliary.base >= 0xFFFF826A
    frame = first_replace(frame,scratch=memory.cursor_at(0xFFFF826A if secondary else 0xFFFF816A))
    side = memory.state.read(0xFFFF814C,2)
    frame = _scene_render_compare(memory,frame,side,2 if secondary else 1,16)
    if side != (2 if secondary else 1):
        return frame
    kind = frame.auxiliary.word()
    frame = _first_word(frame,'target_x',kind)
    frame = _first_word(frame,'target_x',kind & 127)
    category = memory.state.read(0xFFFF814E,2)
    frame = _scene_render_compare(memory,frame,low16(frame.target_x),category,16)
    if low16(frame.target_x) != category:
        return frame
    frame = _first_long(frame,'target_x',0)
    slot = memory.state.read(0xFFFF8150,2)
    frame = _first_word(frame,'target_x',slot)
    frame = _scene_render_asl_word(memory,frame,'target_x',slot,4)
    frame = first_replace(frame,roster=memory.cursor_at(u32(s16(low16(frame.target_x)))))
    frame = first_replace(frame,roster=memory.cursor_at(u32(frame.roster.base + frame.scratch.base)))
    frame = _scene_render_compare(memory,frame,frame.roster.base,frame.auxiliary.base,32)
    if frame.roster.base != frame.auxiliary.base:
        return frame
    resumed = memory.state.read(0xFFFF8152,2)
    frame = _scene_refresh_flags(memory,frame,resumed,2)
    if resumed:
        selection = memory.state.read(0xFFFF815A,2)
        frame = _first_word(frame,'target_x',selection)
        table_base = 0x40D4E
    else:
        frame = _scene_refresh_emit(memory,frame,0xFFFF8152,2,1)
        horizontal = frame.auxiliary.word(0,2)
        frame = _scene_render_compare(memory,frame,horizontal,512,16)
        if horizontal >= 512:
            return _object_clear_word_fields(memory,frame,0xFFFF8152)
        frame = _scene_object_call_fields(memory,frame,0x3B722,0x40CF4)
        frame = _first_word(frame,'target_x',low16(frame.target_x) & 3)
        if low16(frame.target_x) != 0:
            planned = _scene_object_plan_call_fields(memory,frame)
            frame = planned.frame
            if planned.discarded_continuation is not None:
                return frame
        frame = _scene_object_call_fields(memory,frame,0x40D28,0x40D02)
        frame = _scene_refresh_emit(memory,frame,0xFFFF815A,2,low16(frame.target_x))
        selection = low16(frame.target_x)
        table_base = 0x40D0C
    frame = _scene_render_asl_word(memory,frame,'target_x',selection,2)
    target = u32(table_base + s16(u16(selection << 2)))
    from ..high_level_dynamic_flows.business_actions import dispatch_object_action_fields
    return dispatch_object_action_fields(memory,frame,target)

def advance_scene_object_actions_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4033C: physical draw saves, two live queue reads, class/side timer cycling."""
    from .business_scene import _scene_render_compare,_scene_render_bit,_scene_render_asl_word
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x4033C,frame,None)
    frame = _scene_object_call_fields(memory,frame,0x4040A,0x40340)
    frame = first_replace(frame,scratch=memory.cursor_at(0xFFFF836A))
    while True:
        value = frame.scratch.long()
        frame = _scene_refresh_flags(memory,frame,value,4)
        if value == 0:
            break
        pointer = frame.scratch.long()
        frame = first_replace(frame,auxiliary=memory.cursor_at(pointer),scratch=frame.scratch.advance(4))
        active = frame.auxiliary.byte()
        frame = _scene_render_bit(memory,frame,active,128)
        if not active & 128:
            continue
        frame = first_replace(frame,stack_cursor=frame.stack_cursor.advance(-4))
        frame.stack_cursor.set_long(0,frame.scratch.base)
        frame = _scene_object_call_fields(memory,frame,0x40446,0x40358)
        restored = frame.stack_cursor.long()
        frame = first_replace(frame,scratch=memory.cursor_at(restored),stack_cursor=frame.stack_cursor.advance(4))
    side = memory.state.read(0xFFFF814C,2)
    frame = _scene_refresh_flags(memory,frame,side,2)
    if side == 0:
        return frame
    state_code = memory.state.read(0xFFFF8152,2)
    frame = _scene_render_compare(memory,frame,state_code,2,16)
    if state_code != 2:
        hold = memory.state.read(0xFFFF813E,2)
        frame = _scene_refresh_flags(memory,frame,hold,2)
        if hold != 0:
            return frame
        state_code = memory.state.read(0xFFFF8152,2)
        frame = _scene_render_compare(memory,frame,state_code,1,16)
        if state_code == 1:
            return frame
    frame = _object_clear_word_fields(memory,frame,0xFFFF8152)
    frame = _object_adjust_word_fields(memory,frame,0xFFFF8154,1,True)
    if not frame.status & 8:
        return frame
    while True:
        frame = _object_adjust_word_fields(memory,frame,0xFFFF8150,1)
        slot = memory.state.read(0xFFFF8150,2)
        frame = _scene_render_compare(memory,frame,slot,16,16)
        if slot >= 16:
            frame = _object_clear_word_fields(memory,frame,0xFFFF8150)
            frame = _object_adjust_word_fields(memory,frame,0xFFFF814E,1)
            category = memory.state.read(0xFFFF814E,2)
            frame = _scene_render_compare(memory,frame,category,4,16)
            if category >= 4:
                frame = _object_clear_word_fields(memory,frame,0xFFFF814E)
                frame = _object_adjust_word_fields(memory,frame,0xFFFF814C,1)
                side = memory.state.read(0xFFFF814C,2)
                frame = _scene_render_compare(memory,frame,side,3,16)
                if side >= 3:
                    frame = _object_clear_word_fields(memory,frame,0xFFFF814C)
            break
        frame = first_replace(frame,roster=memory.cursor_at(0xFFFF816A))
        side = memory.state.read(0xFFFF814C,2)
        frame = _scene_render_compare(memory,frame,side,1,16)
        if side != 1:
            frame = first_replace(frame,roster=memory.cursor_at(0xFFFF826A))
        slot = memory.state.read(0xFFFF8150,2)
        frame = _first_word(frame,'target_x',slot)
        frame = _scene_render_asl_word(memory,frame,'target_x',slot,4)
        active = frame.roster.byte(low16(frame.target_x))
        frame = _scene_render_bit(memory,frame,active,128)
        if not active & 128:
            continue
        kind = frame.roster.word(low16(frame.target_x))
        frame = _first_word(frame,'target_x',kind)
        frame = _first_word(frame,'target_x',kind & 127)
        category = memory.state.read(0xFFFF814E,2)
        frame = _scene_render_compare(memory,frame,low16(frame.target_x),category,16)
        if low16(frame.target_x) == category:
            break
    frame = _object_clear_word_fields(memory,frame,0xFFFF8154)
    category = memory.state.read(0xFFFF814E,2)
    frame = _scene_render_compare(memory,frame,category,2,16)
    if category >= 2:
        frame = _scene_refresh_emit(memory,frame,0xFFFF8154,2,1)
    return memory.sync_status(frame)

def _object_action_mode_slot_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Shared actual MOVEQ/BYTE/side/ASL/LEA prefix; D0 remains the index."""
    from .business_scene import _scene_render_compare,_scene_render_arithmetic,_scene_render_asl_word
    memory.frame(frame)
    if frame.auxiliary is None:
        raise SceneRefreshBoundary(0x40D28,frame,None)
    frame = _first_long(frame,'target_x',0)
    frame = _first_byte(frame,'target_x',frame.auxiliary.byte(0,1))
    frame = _scene_render_compare(memory,frame,frame.auxiliary.base,0xFFFF826A,32)
    if frame.auxiliary.base >= 0xFFFF826A:
        frame = _scene_render_arithmetic(memory,frame,'target_x',low16(frame.target_x),4,16)
    frame = _scene_render_asl_word(memory,frame,'target_x',low16(frame.target_x),1)
    return first_replace(frame,roster=memory.cursor_at(0xFFFF812A))

def _object_planner_discard_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> tuple:
    """MOVEM.L(A7)+,D0: actual LONG read, preserving CCR, not a callee RTS."""
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x41488,frame,None)
    memory.sync_status(frame)
    token = frame.stack_cursor.long()
    frame = first_replace(frame,target_x=token,stack_cursor=frame.stack_cursor.advance(4))
    return frame,StackContinuation(token)

def _object_planner_finish_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, long_reach: bool) -> SceneActionPlanFields:
    """41464/41498/414D8: real target stores and nonlocal sound/leader tails."""
    from .business_scene import _scene_render_compare,_scene_render_arithmetic
    if not long_reach:
        frame = _scene_render_compare(memory,frame,frame.scratch.base,0xFFFF816A,32)
        leader = frame.scratch.base == 0xFFFF816A
        if not leader:
            frame = _scene_render_compare(memory,frame,frame.scratch.base,0xFFFF826A,32)
            leader = frame.scratch.base == 0xFFFF826A
        if leader:
            category = memory.state.read(0xFFFF814E,2)
            frame = _scene_render_compare(memory,frame,category,3,16)
            if category == 3:
                frame,discarded = _object_planner_discard_fields(memory,frame)
                side = memory.state.read(0xFFFF814C,2)
                frame = _first_word(frame,'target_x',side)
                frame = _scene_render_arithmetic(memory,frame,'target_x',side,1,16,True)
                frame = _scene_refresh_emit(memory,frame,0xFFFF8176,2,low16(frame.target_x))
                frame = _scene_refresh_emit(memory,frame,0xFFFF813A,2,3)
                frame = _scene_refresh_emit(memory,frame,0xFFFF813C,2,0)
                frame = _scene_refresh_emit(memory,frame,0xFFFF813E,2,1)
                frame = _scene_refresh_emit(memory,frame,0xFFFF8152,2,2)
                return SceneActionPlanFields(memory.sync_status(frame),discarded)
    frame = _scene_refresh_emit(memory,frame,0xFFFF815C,4,frame.scratch.base)
    frame = _scene_refresh_emit(memory,frame,0xFFFF815A,2,9 if long_reach else 8)
    frame = _object_clear_word_fields(memory,frame,0xFFFF8162)
    if long_reach:
        frame = _scene_refresh_emit(memory,frame,0xFFFF8164,2,frame.auxiliary.word(0,2))
        frame = _scene_refresh_emit(memory,frame,0xFFFF8166,2,frame.auxiliary.word(0,4))
        frame = _object_clear_word_fields(memory,frame,0xFFFF8168)
    direction = memory.state.read(0xFFFF8000,2)
    frame = _scene_refresh_emit(memory,frame,u32(frame.auxiliary.base + 8),2,direction)
    frame,discarded = _object_planner_discard_fields(memory,frame)
    frame = _first_word(frame,'target_x',162 if long_reach else 167)
    if long_reach:
        frame = _scene_object_call_fields(memory,frame,0x808A,0x41496)
    else:
        # The original JMP808A has no additional caller slot at 414F4.
        from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields
        frame = enqueue_sound_command_fields(memory,frame)
    return SceneActionPlanFields(memory.sync_status(frame),discarded)

def plan_scene_object_action_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> SceneActionPlanFields:
    """Whole 411CC..414FA: ordered adjacency/range planning with real discard.

    The original long south middle probe is WORD 3, not 0x30. Discarded
    token bits come from MOVEM's physical read, never an expected constant.
    """
    from .business_scene import _scene_render_compare
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x411CC,frame,None)
    frame = _object_action_mode_slot_fields(memory,frame)
    mode = frame.roster.word(low16(frame.target_x))
    frame = _scene_render_compare(memory,frame,mode,6,16)
    secondary = frame.auxiliary.base >= 0xFFFF826A

    def select_direction(direction,phase):
        nonlocal frame
        frame = _scene_refresh_emit(memory,frame,0xFFFF8000,2,direction)
        frame = _scene_refresh_emit(memory,frame,0xFFFF8158,2,phase)

    def try_offset(horizontal,vertical,continuation):
        nonlocal frame
        frame = _first_word(frame,'target_x',horizontal)
        frame = _first_word(frame,'target_y',vertical)
        frame = _scene_object_call_fields(memory,frame,0x414FA,continuation)
        frame = _scene_refresh_flags(memory,frame,low16(frame.target_x),2)
        return low16(frame.target_x) != 0

    if mode == 6:
        horizontal = 16 if secondary else 32784
        select_direction(0 if secondary else 1,1 if secondary else 0)
        if try_offset(horizontal,0,0x41206 if secondary else 0x41284):
            return _object_planner_finish_fields(memory,frame,False)
        kind = frame.auxiliary.byte(0,1)
        frame = _scene_render_compare(memory,frame,kind,1,8)
        if kind != 1:
            return SceneActionPlanFields(memory.sync_status(frame),None)
        select_direction(0 if secondary else 1,1 if secondary else 0)
        for magnitude,continuation in ((32,0x4122E if secondary else 0x412AC),
                (48,0x41240 if secondary else 0x412BE),(64,0x41252 if secondary else 0x412D0)):
            if try_offset(magnitude if secondary else magnitude | 32768,0,continuation):
                return _object_planner_finish_fields(memory,frame,True)
        return SceneActionPlanFields(memory.sync_status(frame),None)

    for direction,phase,horizontal,vertical,continuation in (
            (1,0,32784,0,0x412F2),(0,1,16,0,0x41310),
            (2,3,0,16,0x4132E),(3,6,0,32784,0x4134C)):
        select_direction(direction,phase)
        if try_offset(horizontal,vertical,continuation):
            return _object_planner_finish_fields(memory,frame,False)
    kind = frame.auxiliary.byte(0,1)
    frame = _scene_render_compare(memory,frame,kind,1,8)
    if kind != 1:
        return SceneActionPlanFields(memory.sync_status(frame),None)
    for direction,phase,offsets in (
            (1,0,((32800,0,0x41374),(32816,0,0x41386),(32832,0,0x41398))),
            (0,1,((32,0,0x413B6),(48,0,0x413C8),(64,0,0x413DA))),
            (2,3,((0,32,0x413F8),(0,3,0x4140A),(0,64,0x4141C))),
            (3,6,((0,32800,0x4143A),(0,32816,0x4144C),(0,32832,0x4145E)))):
        select_direction(direction,phase)
        for horizontal,vertical,continuation in offsets:
            if try_offset(horizontal,vertical,continuation):
                return _object_planner_finish_fields(memory,frame,True)
    return SceneActionPlanFields(memory.sync_status(frame),None)

def _scene_object_plan_call_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> SceneActionPlanFields:
    """Specific 40CFA BSR: ordinary RTS or a real consumed 40CFE slot, not both."""
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x411CC,frame,0x40CFE)
    frame = first_replace(frame,stack_cursor=frame.stack_cursor.advance(-4))
    frame.stack_cursor.set_long(0,0x40CFE)
    outcome = plan_scene_object_action_fields(memory,frame).validate(memory.state)
    if outcome.discarded_continuation is not None:
        return outcome
    token = outcome.frame.stack_cursor.long()
    if token != 0x40CFE:
        raise SceneRefreshBoundary(token,outcome.frame,0x40CFE)
    frame = first_replace(outcome.frame,stack_cursor=outcome.frame.stack_cursor.advance(4))
    return SceneActionPlanFields(memory.sync_status(frame),None)


# EARLY_OBJECTS_FULL_SOURCE_TWO_REAL_ROUTES121; internal original owner entry, zero additional CODE credit.
def _initialize_scene_object_roster_tail_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """41818..41A58 shared complete roster count/partition/layout tail; no prefix clear or mode checks."""
    from .business_scene import _scene_render_compare, _scene_render_arithmetic, _scene_render_asl_word
    from ..high_level_main_flows.business_movement_support import _movement_multiply_word, _movement_divu_word
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(268312, frame, None)
    for address in (4294934760, 4294934772, 4294934774, 4294934776):
        frame = _object_clear_word_fields(memory, frame, address)
    total = memory.state.read(4294934756, 2)
    frame = _scene_refresh_flags(memory, frame, total, 2)
    if total != 0:
        frame = _scene_refresh_emit(memory, frame, 4294934760, 2, 1)
        total = memory.state.read(4294934756, 2)
        frame = _scene_render_compare(memory, frame, total, 100, 16)
        if total >= 100:
            total = memory.state.read(4294934756, 2)
            frame = _scene_render_compare(memory, frame, total, 1500, 16)
            if total < 1500:
                frame = _object_count_draw_fields(memory, frame, 268364, 9, 1)
            else:
                total = memory.state.read(4294934756, 2)
                frame = _scene_render_compare(memory, frame, total, 5000, 16)
                if total < 5000:
                    frame = _object_count_draw_fields(memory, frame, 268396, 5, 5)
                else:
                    frame = _scene_refresh_emit(memory, frame, 4294934760, 2, 15)
                    total = memory.state.read(4294934756, 2)
                    frame = _scene_render_compare(memory, frame, total, 10000, 16)
                    if total < 10000:
                        frame = _object_count_draw_fields(memory, frame, 268434, 5, 10)
        frame = _scene_object_call_fields(memory, frame, 259266, 268460)
        for threshold, first_count, second_count in ((100, 0, 2), (200, 1, 3), (300, 3, 4), (400, 5, 5), (500, 6, 6), (600, 7, 7)):
            frame = _first_long(frame, 'target_x', first_count)
            frame = _first_long(frame, 'target_y', second_count)
            quality = memory.state.read(4294934800, 2)
            frame = _scene_render_compare(memory, frame, quality, threshold, 16)
            if quality <= threshold:
                break
        else:
            frame = _first_long(frame, 'target_x', 8)
            frame = _first_long(frame, 'target_y', 8)
        for address in (4294934772, 4294934774, 4294934776):
            frame = _object_clear_word_fields(memory, frame, address)
        frame = _first_word(frame, 'unit', memory.state.read(4294934760, 2))
        frame = _scene_render_arithmetic(memory, frame, 'unit', low16(frame.unit), low16(frame.target_x), 16, True)
        if low16(frame.unit) & 32768:
            frame = _scene_refresh_emit(memory, frame, 4294934772, 2, memory.state.read(4294934760, 2))
        else:
            frame = _scene_refresh_emit(memory, frame, 4294934772, 2, low16(frame.target_x))
            frame = _scene_refresh_emit(memory, frame, 4294934774, 2, low16(frame.unit))
            frame = _scene_render_arithmetic(memory, frame, 'unit', low16(frame.unit), low16(frame.target_y), 16, True)
            if not low16(frame.unit) & 32768:
                frame = _scene_refresh_emit(memory, frame, 4294934774, 2, low16(frame.target_y))
                frame = _scene_refresh_emit(memory, frame, 4294934776, 2, low16(frame.unit))
    include_override = total != 0
    while True:
        if include_override:
            mode = memory.state.read(4294934747, 1)
            frame = _scene_render_compare(memory, frame, mode, 3, 8)
            if mode == 3:
                frame = _object_clear_word_fields(memory, frame, 4294934772)
                frame = _scene_refresh_emit(memory, frame, 4294934774, 2, memory.state.read(4294934760, 2))
                frame = _object_clear_word_fields(memory, frame, 4294934776)
        frame = _scene_object_call_fields(memory, frame, 243490, 268622)
        choice = low16(frame.target_x) & 7
        frame = _first_word(frame, 'target_x', choice)
        frame = _scene_render_compare(memory, frame, choice, 4, 16)
        if choice <= 4:
            break
        include_override = True
    frame = _scene_refresh_emit(memory, frame, 4294934858, 2, choice)
    frame = _scene_render_asl_word(memory, frame, 'target_x', choice, 2)
    frame = first_replace(frame, roster=memory.cursor_at(268888))
    pointer = frame.roster.long(s16(low16(frame.target_x)))
    frame = first_replace(frame, scratch=memory.cursor_at(pointer))
    frame = _first_word(frame, 'target_x', memory.state.read(4294934772, 2))
    frame = _first_word(frame, 'target_y', memory.state.read(4294934774, 2))
    frame = _first_word(frame, 'unit', memory.state.read(4294934776, 2))
    frame = _first_long(frame, 'count', 0)
    frame = first_replace(frame, auxiliary=memory.cursor_at(4294934890))
    while True:
        frame = _scene_refresh_flags(memory, frame, low16(frame.count), 2)
        if low16(frame.count) == 0:
            kind, consume = (32771, None)
        else:
            frame = _scene_refresh_flags(memory, frame, low16(frame.target_x), 2)
            if low16(frame.target_x) != 0:
                kind, consume = (32770, 'target_x')
            else:
                frame = _scene_refresh_flags(memory, frame, low16(frame.target_y), 2)
                if low16(frame.target_y) != 0:
                    kind, consume = (32769, 'target_y')
                else:
                    frame = _scene_refresh_flags(memory, frame, low16(frame.unit), 2)
                    if low16(frame.unit) == 0:
                        break
                    kind, consume = (32768, 'unit')
        for displacement in (2, 4):
            value = frame.scratch.word()
            frame = first_replace(frame, scratch=frame.scratch.advance(2))
            frame = _scene_refresh_emit(memory, frame, u32(frame.auxiliary.base + displacement), 2, value)
        if consume == 'unit':
            frame = _scene_render_arithmetic(memory, frame, consume, low16(frame.carrier(consume)), 1, 16, True)
        frame = _scene_refresh_emit(memory, frame, frame.auxiliary.base, 2, kind)
        if consume is not None and consume != 'unit':
            frame = _scene_render_arithmetic(memory, frame, consume, low16(frame.carrier(consume)), 1, 16, True)
        frame = _scene_render_arithmetic(memory, frame, 'count', low16(frame.count), 1, 16)
        frame = first_replace(frame, auxiliary=frame.auxiliary.advance(16))
    frame = _first_word(frame, 'target_x', memory.state.read(4294934788, 2))
    frame = _first_word(frame, 'target_y', memory.state.read(4294934784, 2))
    frame = _movement_multiply_word(memory.state, frame, 'target_y', low16(frame.target_x))
    frame = _movement_divu_word(memory.state, frame, 'target_y', 100, 268762)
    frame = _first_word(frame, 'target_x', 14)
    frame = _first_word(frame, 'unit', memory.state.read(4294934768, 2))
    frame = first_replace(frame, auxiliary=memory.cursor_at(4294934906))
    counter = 14
    while True:
        frame = _scene_refresh_emit(memory, frame, u32(frame.auxiliary.base + 12), 2, low16(frame.target_y))
        frame = _scene_refresh_emit(memory, frame, u32(frame.auxiliary.base + 14), 2, memory.state.read(4294934764, 2))
        frame = _scene_refresh_flags(memory, frame, low16(frame.unit), 2)
        if low16(frame.unit) != 0:
            frame = _scene_render_arithmetic(memory, frame, 'unit', low16(frame.unit), 1, 16, True)
            frame = _object_adjust_word_fields(memory, frame, u32(frame.auxiliary.base + 14), 1)
        frame = first_replace(frame, auxiliary=frame.auxiliary.advance(16))
        frame = _scene_refresh_decrement(frame, 'target_x', counter)
        counter = u16(counter - 1)
        if counter == 65535:
            break
    frame = _first_word(frame, 'target_x', memory.state.read(4294934788, 2))
    frame = _scene_render_arithmetic(memory, frame, 'target_x', low16(frame.target_x), memory.state.read(4294934792, 2), 16)
    frame = _scene_refresh_emit(memory, frame, 4294934902, 2, low16(frame.target_x))
    frame = _scene_refresh_emit(memory, frame, 4294934904, 2, memory.state.read(4294934796, 2))
    return _reset_object_action_controls_fields(memory, frame)

def initialize_scene_object_roster_after_mode_check_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Real41818 internal CALL entry; retained incoming LONGs/SR and the sole shared tail."""
    return _initialize_scene_object_roster_tail_fields(memory, frame)
