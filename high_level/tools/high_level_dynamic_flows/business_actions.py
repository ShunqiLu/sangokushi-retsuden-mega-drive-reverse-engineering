"""Named object movement, projectile, damage, battle-AI and tile operations.

The visible live tables are edited in original DATA order. Dynamic third-layer
targets remain an explicit typed service; indices are never clipped. The two
large action components retain their shared movement/animation tails instead
of manufacturing separate ordinary functions for each physical range.
"""
from dataclasses import replace
from .domain import (SceneState, Table, Cursor, Long, Word, uint, u8, u16, u32,
    low8, low16, s16, negative_word, replace_word, replace_byte, swap_words,
    divu_retained, descending_inclusive, checked_state, checked_table,
    checked_cursor, ram_view, Boundary)
from .contexts_actions import (SceneRenderFrame, SpriteBatchContext,
    ObjectPositionOffset, ObjectActionResult, ObjectVectorContext,
    ObjectRosterTotals, ObjectGlyphResult, TileUploadResult, DuelGlyphContext,
    checked_action, checked_controller_frame)
from .services import (read_object_action_mode, offset_scene_object_position,
    probe_scene_object_overlap_with_frame, sample_random_preserving_seed_carrier,
    append_scene_sprite_entries, decode_glyph_rows_to_buffers,
    enqueue_sound_command, resume_selected_object_action, sample_random_pair,
    plan_scene_object_action)
from .domain import StackContinuation



from .services import (
    SceneRefreshMemory,SceneRefreshBoundary,FirstDeploymentFrame,first_replace,
    _first_word,_first_long,_scene_refresh_emit,_scene_refresh_flags,
    _scene_render_compare,_scene_render_arithmetic,_scene_render_bit,
    _scene_render_asl_word,sample_random_preserving_seed_fields,
    _object_clear_word_fields,probe_scene_object_overlap_fields,
    read_object_action_mode_fields,update_selected_object_action_fields,
    _scene_controller_legacy_fields,_scene_controller_legacy_projection,
    _presentation_call_fields,BattlePresentationMemory,_movement_binary_flags,
)


from .services import (
    _object_adjust_word_fields,_object_shift_word_right_fields,
    offset_scene_object_position_fields,_append_object_sprite_fields,
    _scene_render_push_longs,_movement_divu_word,enqueue_sound_command_fields,
)


from .services import _first_byte,_scene_refresh_decrement,probe_opposing_object_overlap_fields


from .services import set_object_formation_orders_fields,choose_object_formation_leader_fields

def _ram(state, low):
    return ram_view(state, 'ram_' + low)


def _result(actor, opponent, frame):
    return ObjectActionResult(actor, opponent, frame)


def _finish_action(state, actor, opponent, frame):
    """Historical arguments only project the sole actual field core."""
    actual = _object_motion_finish_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def _sample(state, frame):
    return replace(frame, x=sample_random_preserving_seed_carrier(state))


def _probe(state, actor, opponent, frame, horizontal, vertical, *, restore=True):
    frame = replace(frame, x=replace_word(frame.x, horizontal),
                    y=replace_word(frame.y, vertical))
    outcome, frame = probe_scene_object_overlap_with_frame(state, actor,
        ObjectPositionOffset(horizontal, vertical), frame)
    return _result(actor, opponent if restore else outcome.candidate, frame)


def probe_object_left(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole actual field core."""
    actual = _object_direction_probe_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame),0)
    return _object_action_legacy_result(state,actual)


def probe_object_right(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole actual field core."""
    actual = _object_direction_probe_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame),1)
    return _object_action_legacy_result(state,actual)


def probe_object_up(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole actual field core."""
    actual = _object_direction_probe_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame),2)
    return _object_action_legacy_result(state,actual)


def probe_object_down(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole actual field core."""
    actual = _object_direction_probe_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame),3)
    return _object_action_legacy_result(state,actual)


def object_movement_speed(state: SceneState) -> Long:
    actual = object_movement_speed_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())
    return actual.target_x


def continue_object_left(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole actual field core."""
    actual = continue_object_motion_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame),0)
    return _object_action_legacy_result(state,actual)


def continue_object_right(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole actual field core."""
    actual = continue_object_motion_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame),1)
    return _object_action_legacy_result(state,actual)


def continue_object_up(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole actual field core."""
    actual = continue_object_motion_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame),2)
    return _object_action_legacy_result(state,actual)


def continue_object_down(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole actual field core."""
    actual = continue_object_motion_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame),3)
    return _object_action_legacy_result(state,actual)


def _continue_object_motion(state, actor, opponent, frame, direction):
    actual = continue_object_motion_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame),direction)
    current = _scene_controller_legacy_projection(state,actual)
    return _object_action_legacy_result(state,actual),current.conditions


def continue_object_motion_frame(state, frame, direction):
    actual = continue_object_motion_fields(SceneRefreshMemory(state),_scene_controller_legacy_fields(state,frame),direction)
    return _scene_controller_legacy_projection(state,actual)


def start_object_left(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole actual field core."""
    actual = start_object_motion_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame),0)
    return _object_action_legacy_result(state,actual)


def start_object_right(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole actual field core."""
    actual = start_object_motion_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame),1)
    return _object_action_legacy_result(state,actual)


def start_object_up(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole actual field core."""
    actual = start_object_motion_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame),2)
    return _object_action_legacy_result(state,actual)


def start_object_down(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole actual field core."""
    actual = start_object_motion_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame),3)
    return _object_action_legacy_result(state,actual)


def _try_up(state, actor, opponent, frame):
    """Historical arguments only project the sole actual field core."""
    actual = _object_pursuit_try_increasing_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def _pursue_vertical(state, actor, opponent, frame):
    """Historical arguments only project the sole actual field core."""
    actual = _object_pursuit_vertical_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def _pursue_horizontal(state, actor, opponent, frame):
    """Historical arguments only project the sole actual field core."""
    actual = _object_pursuit_horizontal_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def _pursue_other_vertical(state, actor, opponent, frame):
    """Historical arguments only project the sole actual field core."""
    actual = _object_pursuit_other_vertical_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def _random_vertical_maneuver(state, actor, opponent, frame):
    """Historical arguments only project the sole actual field core."""
    actual = _object_pursuit_random_vertical_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def _pursue_other_horizontal(state, actor, opponent, frame):
    """Historical arguments only project the sole actual field core."""
    actual = _object_pursuit_other_horizontal_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def pursue_opposing_object(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole actual field core."""
    actual = pursue_opposing_object_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def sidestep_opposing_object(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole actual field core."""
    actual = sidestep_opposing_object_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def resume_object_selected_action(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    actual = update_selected_object_action_fields(SceneRefreshMemory(state),
        _object_action_legacy_fields(state,actor,opponent,frame),primary_middle=True)
    return _object_action_legacy_result(state,actual)


def _dispatch_primary_action(state, actor, opponent, frame, *, resumed):
    actual = _object_action_legacy_fields(state,actor,opponent,frame)
    target = u32((0x40D4E if resumed else 0x40D0C) + s16(low16(actual.target_x)))
    return _object_action_legacy_result(state,dispatch_object_action_fields(SceneRefreshMemory(state),actual,target))


def _resume_primary_action_selection(state, actor, opponent, frame):
    actual = update_selected_object_action_fields(SceneRefreshMemory(state),
        _object_action_legacy_fields(state,actor,opponent,frame),primary_middle=True)
    return _object_action_legacy_result(state,actual)


def finish_object_action_noop(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole actual field core."""
    actual = _object_motion_finish_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def _resume_pursuit_direction(state, actor, opponent, frame):
    """Historical arguments only project the sole actual field core."""
    actual = resume_object_pursuit_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def resume_object_pursuit(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole actual field core."""
    actual = resume_object_pursuit_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def resume_object_pursuit_alias(state: SceneState, actor: Table, opponent: Table,
                                frame: SceneRenderFrame) -> ObjectActionResult:
    return resume_object_pursuit(state, actor, opponent, frame)


def resume_object_pursuit_second_alias(state: SceneState, actor: Table, opponent: Table,
                                       frame: SceneRenderFrame) -> ObjectActionResult:
    return resume_object_pursuit(state, actor, opponent, frame)


def continue_object_left_vector(state: SceneState, actor: Table, opponent: Table,
                                frame: SceneRenderFrame) -> ObjectActionResult:
    return continue_object_left(state, actor, opponent, frame)


def continue_object_right_vector(state: SceneState, actor: Table, opponent: Table,
                                 frame: SceneRenderFrame) -> ObjectActionResult:
    return continue_object_right(state, actor, opponent, frame)


def continue_object_up_vector(state: SceneState, actor: Table, opponent: Table,
                              frame: SceneRenderFrame) -> ObjectActionResult:
    return continue_object_up(state, actor, opponent, frame)


def continue_object_down_vector(state: SceneState, actor: Table, opponent: Table,
                                frame: SceneRenderFrame) -> ObjectActionResult:
    return continue_object_down(state, actor, opponent, frame)


def adjust_damage_for_object_guard(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Legacy inputs only project the sole complete field core; missing X/A7 remain unknown."""
    actual = adjust_damage_for_object_guard_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def _weighted_damage(state, actor, frame, factor):
    actual = _object_action_legacy_fields(state,actor,actor,frame)
    sites = ((60,0x416BC),(80,0x41690),(120,0x41664))
    continuation = None
    for base,token in sites:
        if base == factor:
            continuation = token
            break
    if continuation is None:
        raise ValueError('actual legacy weighted-damage factor required')
    actual = _object_weighted_damage_fields(SceneRefreshMemory(state),actual,factor,continuation)
    return _object_action_legacy_result(state,actual).frame


def calculate_object_impact_damage(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Legacy inputs only project the sole complete field core; missing X/A7 remain unknown."""
    actual = calculate_object_impact_damage_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def _apply_object_damage(state, actor, opponent, frame):
    """Legacy inputs only project the sole complete field core; missing X/A7 remain unknown."""
    actual = _apply_object_damage_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def _draw_object_impact_flash(state, actor, opponent, frame, *, projectile=False):
    actual = _draw_object_impact_flash_fields(SceneRefreshMemory(state),
        _object_action_legacy_fields(state,actor,opponent,frame),projectile)
    return _object_action_legacy_result(state,actual)


def advance_object_impact(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Legacy inputs only project the sole complete field core; missing X/A7 remain unknown."""
    actual = advance_object_impact_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def advance_object_projectile(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Legacy inputs only project the sole complete field core; missing X/A7 remain unknown."""
    actual = advance_object_projectile_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def sum_live_object_rosters(state: SceneState,
        retained_command: Long | None = None) -> ObjectRosterTotals:
    """Legacy scalar observations project the sole scan, never invent D0 high."""
    memory = SceneRefreshMemory(state)
    actual = FirstDeploymentFrame.unobserved()
    if retained_command is None:
        raise SceneRefreshBoundary(0x41F08,actual,None)
    uint(retained_command,32)
    actual = first_replace(actual,target_x=retained_command)
    actual = sum_live_object_rosters_fields(memory,actual)
    return ObjectRosterTotals(actual.target_y,actual.unit,actual.count,actual.distance,
        actual.target_x,actual.auxiliary)


def _roster_frame(state, actor, opponent, frame):
    actual = sum_live_object_rosters_fields(SceneRefreshMemory(state),
        _object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def _set_all_object_retreat_modes(state):
    _set_all_object_retreat_modes_fields(SceneRefreshMemory(state),FirstDeploymentFrame.unobserved())


def _masked_retreat_roll(state, actor, opponent, frame, table):
    sites = ((0x41EF4,0x41DF4),(0x41EF8,0x41E38),(0x41EFC,0x41E62),(0x41F04,0x41EE0))
    continuation = None
    for address,token in sites:
        if table == address:
            continuation = token
            break
    if continuation is None:
        raise ValueError('actual legacy retreat mask table required')
    actual = _object_retreat_roll_fields(SceneRefreshMemory(state),
        _object_action_legacy_fields(state,actor,opponent,frame),continuation,table)
    return _object_action_legacy_result(state,actual)


def trigger_object_retreat_strength(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole full AI/retreat core."""
    actual = trigger_object_retreat_strength_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def trigger_object_retreat_low_strength(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole full AI/retreat core."""
    actual = trigger_object_retreat_low_strength_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def trigger_object_retreat_outnumbered(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole full AI/retreat core."""
    actual = trigger_object_retreat_outnumbered_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def trigger_object_retreat_morale(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole full AI/retreat core."""
    actual = trigger_object_retreat_morale_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def trigger_object_retreat_quality(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole full AI/retreat core."""
    actual = trigger_object_retreat_quality_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def advance_object_retreat_checks(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole full AI/retreat core."""
    actual = advance_object_retreat_checks_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def choose_object_retreat_phase(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole full AI/retreat core."""
    actual = choose_object_retreat_phase_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def dispatch_object_formation_ai(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole full AI/retreat core."""
    actual = dispatch_object_formation_ai_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def dispatch_object_formation_fallback(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole full AI/retreat core."""
    actual = dispatch_object_formation_fallback_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def update_object_action_ai(state: SceneState, actor: Table, opponent: Table, frame: SceneRenderFrame) -> ObjectActionResult:
    """Historical arguments only project the sole full AI/retreat core."""
    actual = update_object_action_ai_fields(SceneRefreshMemory(state),_object_action_legacy_fields(state,actor,opponent,frame))
    return _object_action_legacy_result(state,actual)


def upload_object_officer_name(state: SceneState, officer: Long, glyphs: DuelGlyphContext) -> ObjectGlyphResult:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    from ..high_level_main_flows.contexts_display_fields import display_legacy_frame_fields
    entered = display_legacy_frame_fields(state, officer, 262850)
    return upload_object_officer_name_frame_fields(state, entered)


def upload_one_scene_tile(state: SceneState, source: Cursor, frame: SceneRenderFrame) -> TileUploadResult:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    from ..high_level_main_flows.contexts_display_fields import display_legacy_frame_fields
    entered = display_legacy_frame_fields(state, source, 418500)
    return upload_one_scene_tile_frame_fields(state, entered)


def upload_scene_tile_block(state: SceneState, source: Cursor, frame: SceneRenderFrame) -> TileUploadResult:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    from ..high_level_main_flows.contexts_display_fields import display_legacy_frame_fields
    entered = display_legacy_frame_fields(state, source, 418484)
    return upload_scene_tile_block_frame_fields(state, entered)


def _upload_banked_tile_strip(state, source, frame, count):
    from ..high_level_main_flows.contexts_display_fields import display_legacy_frame_fields
    return display_legacy_frame_fields(state, None, 418318)


def upload_portrait_tiles(state: SceneState, frame: SceneRenderFrame) -> TileUploadResult:
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    from ..high_level_main_flows.contexts_display_fields import display_legacy_frame_fields
    entered = display_legacy_frame_fields(state, frame, 418260)
    return upload_portrait_tiles_frame_fields(state, entered)

def _object_motion_finish_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Tail reuse: actual previously restored40D76 CLR/40D7A RTS."""
    return _object_clear_word_fields(memory,frame,0xFFFF8152)

def _object_motion_call_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        target: Long, continuation: Long) -> FirstDeploymentFrame:
    """Only this owner's decoded child pairs, with actual physical JSR/RTS."""
    if (target,continuation) not in ((265512, 265610), (265684, 265630), (265706, 265658), (266588, 265700), (265512, 265732), (265808, 265754), (265706, 265782), (266588, 265824), (265898, 265834), (265706, 265872), (266588, 265914), (265988, 265924), (265706, 265962), (266588, 266004), (265898, 266198), (243490, 266236), (265684, 266262), (265808, 266286), (265988, 266306), (265684, 266342), (243490, 266380), (265988, 266406), (265898, 266430), (265808, 266450), (265808, 266530), (265684, 266550), (243490, 266566)):
        raise ValueError("actual object movement call/token pair required")
    memory.frame(frame)
    def child(actual_memory,entered):
        scene = SceneRefreshMemory(actual_memory.state)
        if target == 0x40D28:
            return read_object_action_mode_fields(scene,entered)
        if target == 0x40DEA:
            return object_movement_speed_fields(scene,entered)
        if target == 0x4115C:
            return probe_scene_object_overlap_fields(scene,entered)
        if target == 0x3B722:
            return sample_random_preserving_seed_fields(scene,entered)
        for address,direction in ((0x40DD4,0),(0x40E50,1),(0x40EAA,2),(0x40F04,3)):
            if target == address:
                return _object_direction_probe_fields(scene,entered,direction)
        raise SceneRefreshBoundary(target,entered,continuation)
    return _presentation_call_fields(BattlePresentationMemory(memory.state),frame,continuation,child)

def _object_direction_probe_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, direction: Word) -> FirstDeploymentFrame:
    """Four22B probes: save real A5, probe4115C, restore its live LONG."""
    memory.frame(frame)
    if frame.stack_cursor is None or direction not in (0,1,2,3):
        raise SceneRefreshBoundary(0x40DD4,frame,None)
    horizontal,vertical,continuation = ((32784,0,0x40DE4),(16,0,0x40E60),
        (0,32784,0x40EBA),(0,16,0x40F14))[direction]
    memory.sync_status(frame)
    frame = first_replace(frame,stack_cursor=frame.stack_cursor.advance(-4))
    frame.stack_cursor.set_long(0,frame.scratch.base)
    frame = _first_word(frame,'target_x',horizontal)
    frame = _first_word(frame,'target_y',vertical)
    frame = _object_motion_call_fields(memory,frame,0x4115C,continuation)
    restored = frame.stack_cursor.long()
    return memory.sync_status(first_replace(frame,scratch=memory.cursor_at(restored),
        stack_cursor=frame.stack_cursor.advance(4)))

def object_movement_speed_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """40DEA: both speeds are full MOVEQ, with live TST.W840A in between."""
    memory.frame(frame)
    frame = _first_long(frame,'target_x',2)
    memory.sync_status(frame)
    option = memory.state.read(0xFFFF840A,2)
    frame = _scene_refresh_flags(memory,frame,option,2)
    if option != 0:
        frame = _first_long(frame,'target_x',4)
    return memory.sync_status(frame)

def continue_object_motion_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, direction: Word) -> FirstDeploymentFrame:
    """Four true movement tails: horizontal crossing, vertical exact equality."""
    memory.frame(frame)
    if frame.stack_cursor is None or direction not in (0,1,2,3):
        raise SceneRefreshBoundary(0x40DB6,frame,None)
    axis = 2 if direction < 2 else 4
    continuation = (0x40DBA,0x40E36,0x40E90,0x40EEA)[direction]
    frame = _object_motion_call_fields(memory,frame,0x40DEA,continuation)
    previous = frame.auxiliary.word(0,axis)
    frame,value = _movement_binary_flags(memory.state,frame,previous,low16(frame.target_x),16,direction in (0,2))
    frame.auxiliary.set_word(0,value,axis)
    position = frame.auxiliary.word(0,axis)
    frame = _first_word(frame,'target_x',position)
    target = memory.state.read(0xFFFF8156,2)
    frame = _scene_render_compare(memory,frame,position,target,16)
    finished = (position <= target if direction == 0 else
        position >= target if direction == 1 else position == target)
    if not finished:
        return memory.sync_status(frame)
    current = frame.auxiliary.word(0,axis)
    value = current & 504
    frame = _scene_refresh_flags(memory,frame,value,2)
    frame.auxiliary.set_word(0,value,axis)
    return _object_motion_finish_fields(memory,frame)

def start_object_motion_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, direction: Word) -> FirstDeploymentFrame:
    """Four starts, retaining boundary-mode calls and probe-before-Y-limit order."""
    memory.frame(frame)
    if frame.stack_cursor is None or direction not in (0,1,2,3):
        raise SceneRefreshBoundary(0x40D0C,frame,None)
    axis = 2 if direction < 2 else 4
    if direction < 2:
        position = frame.auxiliary.word(0,axis)
        limit = 0 if direction == 0 else 352
        frame = _scene_render_compare(memory,frame,position,limit,16)
        at_edge = position <= limit if direction == 0 else position >= limit
        if at_edge:
            frame = _object_motion_call_fields(memory,frame,0x40D28,0x40D8A if direction == 0 else 0x40E04)
            frame = _scene_render_compare(memory,frame,low16(frame.target_x),6,16)
            if low16(frame.target_x) == 6:
                frame = _scene_refresh_emit(memory,frame,u32(frame.auxiliary.base + 2),2,512)
            return _object_motion_finish_fields(memory,frame)
    probe,continuation = ((0x40DD4,0x40D9E),(0x40E50,0x40E1A),
        (0x40EAA,0x40E6A),(0x40F04,0x40EC4))[direction]
    frame = _object_motion_call_fields(memory,frame,probe,continuation)
    frame = _scene_refresh_flags(memory,frame,low16(frame.target_x),2)
    if low16(frame.target_x):
        return _object_motion_finish_fields(memory,frame)
    if direction >= 2:
        position = frame.auxiliary.word(0,4)
        limit = 32 if direction == 2 else 288
        frame = _scene_render_compare(memory,frame,position,limit,16)
        at_edge = position <= limit if direction == 2 else position >= limit
        if at_edge:
            return _object_motion_finish_fields(memory,frame)
    position = frame.auxiliary.word(0,axis)
    frame = _first_word(frame,'target_x',position)
    frame = _scene_render_arithmetic(memory,frame,'target_x',position,16,16,direction in (0,2))
    frame = _scene_refresh_emit(memory,frame,0xFFFF8156,2,low16(frame.target_x))
    frame = _scene_refresh_emit(memory,frame,u32(frame.auxiliary.base + 8),2,(1,0,3,2)[direction])
    return continue_object_motion_fields(memory,frame,direction)

def _object_pursuit_store_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, direction: Word) -> FirstDeploymentFrame:
    return _scene_refresh_emit(memory,frame,u32(frame.auxiliary.base + 10),2,direction)

def _object_pursuit_probe_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, target: Long, continuation: Long) -> FirstDeploymentFrame:
    frame = _object_motion_call_fields(memory,frame,target,continuation)
    return _scene_refresh_flags(memory,frame,low16(frame.target_x),2)

def _object_pursuit_abs_axis_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, name: str, axis: Word) -> FirstDeploymentFrame:
    own = frame.auxiliary.word(0,axis)
    frame = _first_word(frame,name,own)
    other = frame.scratch.word(0,axis)
    frame = _scene_render_arithmetic(memory,frame,name,own,other,16,True)
    if low16(frame.carrier(name)) & 32768:
        frame = _scene_render_arithmetic(memory,frame,name,0,low16(frame.carrier(name)),16,True)
    return memory.sync_status(frame)

def _object_pursuit_horizontal_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """40FDC: immediate MOVE1 clears C before the original redundant BCS."""
    frame = _object_pursuit_store_fields(memory,frame,0)
    own = frame.auxiliary.word(0,2)
    frame = _first_word(frame,'target_x',own)
    other = frame.scratch.word(0,2)
    frame = _scene_render_compare(memory,frame,own,other,16)
    if own > other:
        return start_object_motion_fields(memory,frame,0)
    frame = _object_pursuit_store_fields(memory,frame,1)
    frame = _object_motion_call_fields(memory,frame,0x3B722,0x40FFC)
    frame = _scene_render_bit(memory,frame,frame.target_x,2)
    if frame.target_x & 2:
        position = frame.auxiliary.word(0,2)
        frame = _scene_render_compare(memory,frame,position,0,16)
        if position <= 0:
            return start_object_motion_fields(memory,frame,1)
        frame = _object_pursuit_probe_fields(memory,frame,0x40DD4,0x41016)
        return start_object_motion_fields(memory,frame,0 if low16(frame.target_x) == 0 else 1)
    position = frame.auxiliary.word(0,2)
    frame = _scene_render_compare(memory,frame,position,352,16)
    if position >= 352:
        return start_object_motion_fields(memory,frame,0)
    frame = _object_pursuit_probe_fields(memory,frame,0x40E50,0x4102E)
    return start_object_motion_fields(memory,frame,1 if low16(frame.target_x) == 0 else 0)

def _object_pursuit_try_increasing_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """41038 shared target: store3, probe down, start down or resume horizontal."""
    frame = _object_pursuit_store_fields(memory,frame,3)
    frame = _object_pursuit_probe_fields(memory,frame,0x40F04,0x41042)
    if low16(frame.target_x) == 0:
        return start_object_motion_fields(memory,frame,3)
    return _object_pursuit_horizontal_fields(memory,frame)

def _object_pursuit_vertical_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """40FBA/41038: preserve actual opposite probe targets and stored directions."""
    frame = _object_pursuit_store_fields(memory,frame,3)
    own = frame.auxiliary.word(0,4)
    frame = _first_word(frame,'target_x',own)
    other = frame.scratch.word(0,4)
    frame = _scene_render_compare(memory,frame,own,other,16)
    if own < other:
        return _object_pursuit_try_increasing_fields(memory,frame)
    else:
        frame = _object_pursuit_store_fields(memory,frame,2)
        frame = _object_pursuit_probe_fields(memory,frame,0x40EAA,0x40FD6)
        if low16(frame.target_x) == 0:
            return start_object_motion_fields(memory,frame,2)
    return _object_pursuit_horizontal_fields(memory,frame)

def _object_pursuit_other_vertical_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4106C: BCS goes directly to down; MOVE2 then BHI goes directly up."""
    frame = _object_pursuit_store_fields(memory,frame,3)
    own = frame.auxiliary.word(0,4)
    frame = _first_word(frame,'target_x',own)
    other = frame.scratch.word(0,4)
    frame = _scene_render_compare(memory,frame,own,other,16)
    if own < other:
        return start_object_motion_fields(memory,frame,3)
    frame = _object_pursuit_store_fields(memory,frame,2)
    return start_object_motion_fields(memory,frame,2)

def _object_pursuit_random_vertical_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """41088 physical suffix is retained, without redirecting the prior BHI."""
    frame = _object_motion_call_fields(memory,frame,0x3B722,0x4108C)
    frame = _scene_render_bit(memory,frame,frame.target_x,2)
    if frame.target_x & 2:
        position = frame.auxiliary.word(0,4)
        frame = _scene_render_compare(memory,frame,position,288,16)
        if position >= 288:
            return _object_pursuit_try_increasing_fields(memory,frame)
        frame = _object_pursuit_probe_fields(memory,frame,0x40F04,0x410A6)
        return start_object_motion_fields(memory,frame,3 if low16(frame.target_x) == 0 else 2)
    position = frame.auxiliary.word(0,4)
    frame = _scene_render_compare(memory,frame,position,32,16)
    if position <= 32:
        return start_object_motion_fields(memory,frame,3)
    frame = _object_pursuit_probe_fields(memory,frame,0x40EAA,0x410BE)
    return start_object_motion_fields(memory,frame,2 if low16(frame.target_x) == 0 else 3)

def _object_pursuit_other_horizontal_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _object_pursuit_store_fields(memory,frame,1)
    own = frame.auxiliary.word(0,2)
    frame = _first_word(frame,'target_x',own)
    other = frame.scratch.word(0,2)
    frame = _scene_render_compare(memory,frame,own,other,16)
    if own < other:
        frame = _object_pursuit_store_fields(memory,frame,1)
        frame = _object_pursuit_probe_fields(memory,frame,0x40E50,0x410D2)
        if low16(frame.target_x) == 0:
            return start_object_motion_fields(memory,frame,1)
    else:
        frame = _object_pursuit_store_fields(memory,frame,0)
        frame = _object_pursuit_probe_fields(memory,frame,0x40DD4,0x41066)
        if low16(frame.target_x) == 0:
            return start_object_motion_fields(memory,frame,0)
    return _object_pursuit_other_vertical_fields(memory,frame)

def pursue_opposing_object_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """40F1A: actual leader selection, ordered kind reads and absolute axes."""
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x40F1A,frame,None)
    frame = _scene_render_compare(memory,frame,frame.auxiliary.base,0xFFFF826A,32)
    frame = first_replace(frame,scratch=memory.cursor_at(0xFFFF816A if frame.auxiliary.base >= 0xFFFF826A else 0xFFFF826A))
    mode = memory.state.read(0xFFFF80DB,1)
    frame = _scene_render_compare(memory,frame,mode,3,8)
    if mode != 3:
        kind = frame.auxiliary.byte(0,1)
        frame = _scene_refresh_flags(memory,frame,kind,1)
        if kind != 0:
            kind = frame.auxiliary.byte(0,1)
            frame = _scene_render_compare(memory,frame,kind,1,8)
            if kind == 1:
                frame = _object_pursuit_abs_axis_fields(memory,frame,'target_x',4)
                frame = _scene_render_compare(memory,frame,low16(frame.target_x),16,16)
                if low16(frame.target_x) > 16:
                    return _object_pursuit_vertical_fields(memory,frame)
                return _object_pursuit_other_horizontal_fields(memory,frame)
            kind = frame.auxiliary.byte(0,1)
            frame = _scene_render_compare(memory,frame,kind,2,8)
            frame = _object_pursuit_abs_axis_fields(memory,frame,'target_x',2)
            frame = _scene_render_compare(memory,frame,low16(frame.target_x),16,16)
            if low16(frame.target_x) > 16:
                return _object_pursuit_other_horizontal_fields(memory,frame)
            return _object_pursuit_vertical_fields(memory,frame)
    frame = _object_pursuit_abs_axis_fields(memory,frame,'target_x',2)
    frame = _object_pursuit_abs_axis_fields(memory,frame,'target_y',4)
    frame = _scene_render_compare(memory,frame,low16(frame.target_y),low16(frame.target_x),16)
    if low16(frame.target_y) < low16(frame.target_x):
        return _object_pursuit_other_horizontal_fields(memory,frame)
    return _object_pursuit_vertical_fields(memory,frame)

def sidestep_opposing_object_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """41110: actual side probe, RNG, otherwise-unused Y read and bit4 tail."""
    memory.frame(frame)
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x41110,frame,None)
    frame = _scene_render_compare(memory,frame,frame.auxiliary.base,0xFFFF826A,32)
    if frame.auxiliary.base >= 0xFFFF826A:
        frame = _object_pursuit_store_fields(memory,frame,1)
        frame = _object_pursuit_probe_fields(memory,frame,0x40E50,0x41122)
        if low16(frame.target_x) == 0:
            return start_object_motion_fields(memory,frame,1)
    else:
        frame = _object_pursuit_store_fields(memory,frame,0)
        frame = _object_pursuit_probe_fields(memory,frame,0x40DD4,0x41136)
        if low16(frame.target_x) == 0:
            return start_object_motion_fields(memory,frame,0)
    frame = _object_pursuit_store_fields(memory,frame,3)
    frame = _object_motion_call_fields(memory,frame,0x3B722,0x41146)
    other_y = frame.scratch.word(0,4)
    frame = _scene_render_compare(memory,frame,low16(frame.target_x),other_y,16)
    frame = _scene_render_bit(memory,frame,frame.target_x,16)
    if frame.target_x & 16:
        return start_object_motion_fields(memory,frame,3)
    frame = _object_pursuit_store_fields(memory,frame,2)
    return start_object_motion_fields(memory,frame,2)

def resume_object_pursuit_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """40F7E: actual raw WORD vector, no four-direction clamp."""
    memory.frame(frame)
    value = frame.auxiliary.word(0,10)
    frame = _first_word(frame,'target_x',value)
    frame = _scene_render_asl_word(memory,frame,'target_x',value,2)
    target = u32(0x40F88 + s16(u16(value << 2)))
    if target in (0x40F88,0x40F8C,0x40F90,0x40F94):
        return continue_object_motion_fields(memory,frame,(target - 0x40F88)//4)
    raise SceneRefreshBoundary(target,frame,None)

def dispatch_object_action_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        target: Long) -> FirstDeploymentFrame:
    """Finite actual executable-vector aliases; JMP adds no physical call slot."""
    memory.frame(frame)
    for address,direction in ((0x40D0C,0),(0x40D10,1),(0x40D14,2),(0x40D18,3)):
        if target == address:
            return start_object_motion_fields(memory,frame,direction)
    for address,direction in ((0x40D4E,0),(0x40D52,1),(0x40D56,2),(0x40D5A,3),
            (0x40F88,0),(0x40F8C,1),(0x40F90,2),(0x40F94,3)):
        if target == address:
            return continue_object_motion_fields(memory,frame,direction)
    if target == 0x40D20:
        return pursue_opposing_object_fields(memory,frame)
    if target == 0x40D24:
        return sidestep_opposing_object_fields(memory,frame)
    if target == 0x40D1C:
        return update_selected_object_action_fields(memory,frame,primary_middle=True)
    if target == 0x40D5E:
        return _object_motion_finish_fields(memory,frame)
    if target in (0x40D62,0x40D66,0x40D6A):
        return resume_object_pursuit_fields(memory,frame)
    if target == 0x40D6E:
        return advance_object_impact_fields(memory,frame)
    if target == 0x40D72:
        return advance_object_projectile_fields(memory,frame)
    raise SceneRefreshBoundary(target,frame,None)

def _object_action_legacy_fields(state, actor, opponent, frame):
    """Old convenience inputs never fill full D/A, X or A7 with default zeros."""
    checked_action(state,actor,opponent,frame)
    current = checked_controller_frame(frame,state)
    actual = _scene_controller_legacy_fields(state,current)
    return first_replace(actual,auxiliary=actor.cursor(),scratch=opponent.cursor())

def _object_action_legacy_result(state, actual):
    current = _scene_controller_legacy_projection(state,actual)
    frame = SceneRenderFrame(current.x,current.y,current.attributes,current.palette,current.tile,current)
    return ObjectActionResult(state.table_at(actual.auxiliary.base),state.table_at(actual.scratch.base),frame)

def _object_impact_call_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        target: Long, continuation: Long) -> FirstDeploymentFrame:
    """Only decoded calls belonging to impact, projectile and damage owners."""
    if (target,continuation) not in ((267822, 267588), (266658, 267708), (241980, 267736), (266658, 267810), (243490, 267876), (243490, 267920), (243490, 267964), (32906, 268064), (243490, 268110), (267982, 268132)):
        raise ValueError("actual impact/projectile call/token pair required")
    memory.frame(frame)
    def child(actual_memory,entered):
        scene = SceneRefreshMemory(actual_memory.state)
        if target == 0x4162E:
            return calculate_object_impact_damage_fields(scene,entered)
        if target == 0x416CE:
            return adjust_damage_for_object_guard_fields(scene,entered)
        if target == 0x411A2:
            return offset_scene_object_position_fields(scene,entered)
        if target == 0x3B13C:
            return _append_object_sprite_fields(scene,entered)
        if target == 0x3B722:
            return sample_random_preserving_seed_fields(scene,entered)
        if target == 0x808A:
            return enqueue_sound_command_fields(scene,entered)
        raise SceneRefreshBoundary(target,entered,continuation)
    return _presentation_call_fields(BattlePresentationMemory(memory.state),frame,continuation,child)

def _object_impact_restore_long_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, name: str) -> FirstDeploymentFrame:
    """MOVEM.L (A7)+ restores the observed carrier without changing CCR."""
    if frame.stack_cursor is None:
        raise SceneRefreshBoundary(0x4162E,frame,None)
    memory.sync_status(frame)
    value = frame.stack_cursor.long()
    return first_replace(frame,**{name:value},stack_cursor=frame.stack_cursor.advance(4))

def _object_weighted_damage_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, factor: Word, continuation: Long) -> FirstDeploymentFrame:
    """Two original WORD products/divisions, with real D1 save and RNG slot.

    The RNG factors and call sites are the four actual entry arms, not a new
    generic random formula. DIVU's undefined-overflow result remains the shared
    arithmetic boundary; it is never replaced by unlimited-precision division.
    """
    sites = ((120,0x41664,0x41658,0x41672),(80,0x41690,0x41684,0x4169E),
        (60,0x416BC,0x416B0,0x416CA),(80,0x4174E,0x41742,0x4175C))
    selected = None
    for item in sites:
        if item[:2] == (factor,continuation):
            selected = item
            break
    if selected is None:
        raise ValueError('actual weighted-damage arm and RNG continuation required')
    memory.frame(frame)
    memory.sync_status(frame)
    frame = _first_word(frame,'target_x',frame.auxiliary.word(0,0x0E))
    memory.sync_status(frame)
    frame = _first_word(frame,'target_y',frame.auxiliary.word(0,0x0C))
    frame = _first_long(frame,'target_y',low16(frame.target_y) * low16(frame.target_x))
    frame = _movement_divu_word(memory.state,frame,'target_y',100,selected[2])
    memory.sync_status(frame)
    frame = _scene_render_push_longs(memory,frame,(frame.target_y,))
    frame = _object_impact_call_fields(memory,frame,0x3B722,continuation)
    frame = _first_word(frame,'target_x',low16(frame.target_x) & 31)
    frame = _scene_render_arithmetic(memory,frame,'target_x',low16(frame.target_x),factor,16)
    frame = _object_impact_restore_long_fields(memory,frame,'target_y')
    frame = _first_long(frame,'target_y',low16(frame.target_y) * low16(frame.target_x))
    frame = _movement_divu_word(memory.state,frame,'target_y',100,selected[3])
    return memory.sync_status(frame)

def adjust_damage_for_object_guard_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """416CE alternate entry consumes the existing D1; it never samples RNG."""
    memory.frame(frame)
    memory.sync_status(frame)
    kind = frame.scratch.byte(0,1)
    frame = _scene_render_compare(memory,frame,kind,3,8)
    if kind != 3:
        return memory.sync_status(frame)
    frame = _first_word(frame,'unit',memory.state.read(0xFFFF8104,2))
    memory.sync_status(frame)
    side = memory.state.read(0xFFFF814C,2)
    frame = _scene_render_compare(memory,frame,side,2,16)
    if side != 2:
        frame = _first_word(frame,'unit',memory.state.read(0xFFFF8106,2))
    frame,divisor = _object_shift_word_right_fields(memory,frame,'unit',low16(frame.unit),1)
    if divisor == 0:
        divisor = 1
        frame = _first_word(frame,'unit',divisor)
    frame = _first_long(frame,'target_y',frame.target_y & 65535)
    frame = _movement_divu_word(memory.state,frame,'target_y',divisor,0x416F4)
    return memory.sync_status(frame)

def calculate_object_impact_damage_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4162E: separate live BYTE comparisons select the three original factors."""
    memory.frame(frame)
    for kind,factor,continuation in ((0,60,0x416BC),(1,80,0x41690),(2,120,0x41664)):
        memory.sync_status(frame)
        live_kind = frame.auxiliary.byte(0,1)
        frame = _scene_render_compare(memory,frame,live_kind,kind,8)
        if live_kind == kind:
            frame = _object_weighted_damage_fields(memory,frame,factor,continuation)
            break
    else:
        frame = _first_word(frame,'target_y',frame.auxiliary.word(0,0x0C))
    # All three branches are BRA/fallthrough, not a second invented BSR.
    return adjust_damage_for_object_guard_fields(memory,frame)

def _apply_object_damage_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """41544 shared damage tail, preserving negative/zero and leader transitions."""
    memory.frame(frame)
    memory.sync_status(frame)
    previous = frame.scratch.word(0,0x0E)
    frame,remaining = _movement_binary_flags(memory.state,frame,previous,low16(frame.target_y),16,True)
    memory.sync_status(frame)
    frame.scratch.set_word(0,remaining,0x0E)
    if remaining != 0 and not remaining & 32768:
        return _object_motion_finish_fields(memory,frame)
    frame = _object_clear_word_fields(memory,frame,u32(frame.scratch.base + 0x0E))
    frame = _object_clear_word_fields(memory,frame,frame.scratch.base)
    frame = _scene_render_compare(memory,frame,frame.scratch.base,0xFFFF826A,32)
    if frame.scratch.base >= 0xFFFF826A:
        leader = memory.state.read(0xFFFF826A,2)
        frame = _scene_refresh_flags(memory,frame,leader,2)
        if leader != 0:
            return _object_motion_finish_fields(memory,frame)
        frame = _scene_refresh_emit(memory,frame,0xFFFF8114,2,2)
        frame = _scene_refresh_emit(memory,frame,0xFFFF8116,2,3)
    else:
        leader = memory.state.read(0xFFFF816A,2)
        frame = _scene_refresh_flags(memory,frame,leader,2)
        if leader != 0:
            return _object_motion_finish_fields(memory,frame)
        frame = _scene_refresh_emit(memory,frame,0xFFFF8114,2,3)
        frame = _object_clear_word_fields(memory,frame,0xFFFF8116)
    frame = _scene_refresh_emit(memory,frame,0xFFFF813A,2,4)
    frame = _scene_refresh_emit(memory,frame,0xFFFF813C,2,0)
    frame = _scene_refresh_emit(memory,frame,0xFFFF813E,2,1)
    frame = _first_word(frame,'target_x',memory.state.read(0xFFFF814C,2))
    frame = _scene_render_arithmetic(memory,frame,'target_x',low16(frame.target_x),1,16,True)
    frame = _first_word(frame,'target_x',low16(frame.target_x) ^ 1)
    frame = _scene_refresh_emit(memory,frame,0xFFFF8176,2,low16(frame.target_x))
    return _object_motion_finish_fields(memory,frame)

def _draw_object_impact_flash_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, projectile: bool = False) -> FirstDeploymentFrame:
    """415A2/41608 save the live actor position around the shared flash packet."""
    if type(projectile) is not bool:
        raise ValueError('actual flash entry required')
    memory.frame(frame)
    memory.sync_status(frame)
    frame = _first_long(frame,'target_x',frame.auxiliary.long(0,2))
    memory.sync_status(frame)
    frame = _scene_render_push_longs(memory,frame,(frame.target_x,))
    frame = _first_word(frame,'unit',memory.state.read(0xFFFF8158,2))
    frame = _scene_render_asl_word(memory,frame,'unit',low16(frame.unit),2)
    memory.sync_status(frame)
    frame = _first_word(frame,'target_x',memory.state.read(u32(0x415E8 + s16(low16(frame.unit))),2))
    memory.sync_status(frame)
    frame = _first_word(frame,'target_y',memory.state.read(u32(0x415EA + s16(low16(frame.unit))),2))
    frame = _object_impact_call_fields(memory,frame,0x411A2,0x41622 if projectile else 0x415BC)
    if projectile:
        frame = _first_word(frame,'target_x',memory.state.read(0xFFFF8164,2))
        memory.sync_status(frame)
        frame = _first_word(frame,'target_y',memory.state.read(0xFFFF8166,2))
    else:
        frame = _first_word(frame,'target_x',frame.auxiliary.word(0,2))
        memory.sync_status(frame)
        frame = _first_word(frame,'target_y',frame.auxiliary.word(0,4))
    frame = _first_word(frame,'unit',4)
    frame = _first_long(frame,'count',0)
    frame = _first_word(frame,'distance',0x100)
    frame = first_replace(frame,roster=memory.cursor_at(0x415E2))
    frame = _object_impact_call_fields(memory,frame,0x3B13C,0x415D8)
    frame = _object_impact_restore_long_fields(memory,frame,'target_x')
    return _scene_refresh_emit(memory,frame,u32(frame.auxiliary.base + 2),4,frame.target_x)

def _object_impact_timer_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, address: Long) -> FirstDeploymentFrame:
    """Shared ADDQ/extra live MOVE/MOVEQ/TST/CMP sequence of the two timers."""
    frame = _object_adjust_word_fields(memory,frame,address,1)
    frame = _first_word(frame,'target_x',memory.state.read(address,2))
    frame = _first_long(frame,'target_y',16)
    memory.sync_status(frame)
    option = memory.state.read(0xFFFF840A,2)
    frame = _scene_refresh_flags(memory,frame,option,2)
    if option != 0:
        frame = _first_long(frame,'target_y',16)
    return _scene_render_compare(memory,frame,low16(frame.target_x),low16(frame.target_y),16)

def advance_object_impact_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """40D6E/41524 timed contact: flash until 16, then actual damage/death tail."""
    memory.frame(frame)
    frame = _object_impact_timer_fields(memory,frame,0xFFFF8162)
    if low16(frame.target_x) < low16(frame.target_y):
        return _draw_object_impact_flash_fields(memory,frame)
    frame = first_replace(frame,scratch=memory.cursor_at(memory.state.read(0xFFFF815C,4)))
    frame = _object_impact_call_fields(memory,frame,0x4162E,0x41544)
    return _apply_object_damage_fields(memory,frame)

def _object_projectile_motion_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """41768 movement arm, live direction tests and the real sprite JMP tail."""
    frame = _first_long(frame,'target_x',4)
    memory.sync_status(frame)
    option = memory.state.read(0xFFFF840A,2)
    frame = _scene_refresh_flags(memory,frame,option,2)
    if option != 0:
        frame = _first_long(frame,'target_x',8)
    memory.sync_status(frame)
    direction = frame.auxiliary.word(0,8)
    frame = _scene_refresh_flags(memory,frame,direction,2)
    if direction == 0:
        frame = _object_adjust_word_fields(memory,frame,0xFFFF8164,low16(frame.target_x))
    else:
        for expected,address,subtract in ((1,0xFFFF8164,True),(2,0xFFFF8166,False),(3,0xFFFF8166,True)):
            memory.sync_status(frame)
            direction = frame.auxiliary.word(0,8)
            frame = _scene_render_compare(memory,frame,direction,expected,16)
            if direction == expected:
                frame = _object_adjust_word_fields(memory,frame,address,low16(frame.target_x),subtract)
                break
    memory.sync_status(frame)
    frame = _first_word(frame,'target_x',frame.auxiliary.word(0,8))
    frame = _scene_render_asl_word(memory,frame,'target_x',low16(frame.target_x),2)
    memory.sync_status(frame)
    source = memory.state.read(u32(0x417CE + s16(low16(frame.target_x))),4)
    frame = first_replace(frame,roster=memory.cursor_at(source))
    frame = _first_word(frame,'target_x',memory.state.read(0xFFFF8164,2))
    memory.sync_status(frame)
    frame = _first_word(frame,'target_y',memory.state.read(0xFFFF8166,2))
    frame = _first_word(frame,'unit',4)
    frame = _first_long(frame,'count',0)
    frame = _first_word(frame,'distance',0x300)
    # Encoded 417CA JMP targets 3B13C: no extra return token is pushed.
    return _append_object_sprite_fields(memory,frame)

def advance_object_projectile_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """40D72/416F8 exact arrival, hardware sound, flash, or projectile movement."""
    memory.frame(frame)
    memory.sync_status(frame)
    frame = first_replace(frame,scratch=memory.cursor_at(memory.state.read(0xFFFF815C,4)))
    frame = _first_word(frame,'target_x',memory.state.read(0xFFFF8164,2))
    memory.sync_status(frame)
    destination = frame.scratch.word(0,2)
    frame = _scene_render_compare(memory,frame,low16(frame.target_x),destination,16)
    if low16(frame.target_x) != destination:
        return _object_projectile_motion_fields(memory,frame)
    frame = _first_word(frame,'target_x',memory.state.read(0xFFFF8166,2))
    memory.sync_status(frame)
    destination = frame.scratch.word(0,4)
    frame = _scene_render_compare(memory,frame,low16(frame.target_x),destination,16)
    if low16(frame.target_x) != destination:
        return _object_projectile_motion_fields(memory,frame)
    timer = memory.state.read(0xFFFF8168,2)
    frame = _scene_refresh_flags(memory,frame,timer,2)
    if timer == 0:
        frame = _first_word(frame,'target_x',0xAA)
        frame = _object_impact_call_fields(memory,frame,0x808A,0x41720)
    frame = _object_impact_timer_fields(memory,frame,0xFFFF8168)
    if low16(frame.target_x) < low16(frame.target_y):
        return _draw_object_impact_flash_fields(memory,frame,True)
    frame = _object_weighted_damage_fields(memory,frame,80,0x4174E)
    frame = _object_impact_call_fields(memory,frame,0x416CE,0x41764)
    return _apply_object_damage_fields(memory,frame)

def _object_ai_call_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame,
        target: Long, continuation: Long) -> FirstDeploymentFrame:
    """Only cached AI/retreat JSR and BSR pairs, with actual physical slots."""
    if (target,continuation) not in ((269284, 269262), (269526, 269268), (270154, 269274), (269760, 269280), (269790, 269772), (269854, 269776), (269900, 269780), (269942, 269784), (270006, 269788), (270088, 269794), (243490, 269812), (270088, 269858), (243490, 269880), (270088, 269904), (243490, 269922), (270088, 269946), (243490, 269966), (270088, 270010), (243490, 270048), (270088, 270170), (267514, 270226), (267514, 270244), (267514, 270262), (267514, 270280), (243490, 270290)):
        raise ValueError("actual AI/retreat call/token pair required")
    memory.frame(frame)
    def child(actual_memory,entered):
        scene = SceneRefreshMemory(actual_memory.state)
        for address,function in ((0x41BE4,dispatch_object_formation_ai_fields),
                (0x41CD6,dispatch_object_formation_fallback_fields),
                (0x41F4A,choose_object_retreat_phase_fields),(0x41DC0,advance_object_retreat_checks_fields),
                (0x41DDE,trigger_object_retreat_strength_fields),(0x41E1E,trigger_object_retreat_low_strength_fields),
                (0x41E4C,trigger_object_retreat_outnumbered_fields),(0x41E76,trigger_object_retreat_morale_fields),
                (0x41EB6,trigger_object_retreat_quality_fields),(0x41F08,sum_live_object_rosters_fields),
                (0x414FA,probe_opposing_object_overlap_fields),(0x3B722,sample_random_preserving_seed_fields)):
            if target == address:
                return function(scene,entered)
        raise SceneRefreshBoundary(target,entered,continuation)
    return _presentation_call_fields(BattlePresentationMemory(memory.state),frame,continuation,child)

def sum_live_object_rosters_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """41F08: two live fifteen-record scans, wrapped WORD sums/counts and DBRA.

    Only MOVEQ actually defines the high halves. D0 retains its supplied high
    WORD and finishes low FFFF; A6 advances through both actual live rosters.
    """
    memory.frame(frame)
    for base,total_name,count_name in ((0xFFFF817A,'target_y','count'),(0xFFFF827A,'unit','distance')):
        frame = _first_long(frame,total_name,0)
        frame = _first_long(frame,count_name,0)
        frame = _first_word(frame,'target_x',14)
        frame = first_replace(frame,auxiliary=memory.cursor_at(base))
        counter = 14
        while True:
            memory.sync_status(frame)
            active = frame.auxiliary.byte()
            frame = _scene_render_bit(memory,frame,active,128)
            if active & 128:
                memory.sync_status(frame)
                amount = frame.auxiliary.word(0,0x0E)
                frame = _scene_render_arithmetic(memory,frame,total_name,low16(frame.carrier(total_name)),amount,16)
                frame = _scene_render_arithmetic(memory,frame,count_name,low16(frame.carrier(count_name)),1,16)
            frame = first_replace(frame,auxiliary=frame.auxiliary.advance(16))
            frame = _scene_refresh_decrement(frame,'target_x',counter)
            counter = u16(counter - 1)
            if counter == 65535:
                break
    return memory.sync_status(frame)

def _set_all_object_retreat_modes_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Shared 41E04 tail: four original MOVE.W stores, not CLR or a new call."""
    for address in (0xFFFF812A,0xFFFF812C,0xFFFF812E,0xFFFF8130):
        frame = _scene_refresh_emit(memory,frame,address,2,6)
    return frame

def _object_retreat_roll_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, continuation: Long, table: Long | None) -> FirstDeploymentFrame:
    """Actual preserving-RNG call, live difficulty and optional BYTE table AND."""
    sites = ((0x41DF4,0x41EF4),(0x41E38,0x41EF8),(0x41E62,0x41EFC),
        (0x41E8E,None),(0x41EE0,0x41F04))
    if (continuation,table) not in sites:
        raise ValueError('actual retreat RNG arm required')
    frame = _object_ai_call_fields(memory,frame,0x3B722,continuation)
    frame = _first_word(frame,'target_y',memory.state.read(0xFFFFEFD2,2))
    if table is not None:
        frame = first_replace(frame,roster=memory.cursor_at(table))
        memory.sync_status(frame)
        mask = frame.roster.byte(low16(frame.target_y))
        frame = _first_byte(frame,'target_x',low8(frame.target_x) & mask)
    return memory.sync_status(frame)

def trigger_object_retreat_check_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, kind: Word) -> FirstDeploymentFrame:
    """Five original 41DDE..41EF4 criteria share actual count/roll/store tails.

    Strength's failed roll branches to the shared RTS at41E1C. The following
    caller's low-strength check is separate and must not be moved into this
    entry: doing so would invent a second roster scan and random draw.
    """
    if kind not in (0,1,2,3,4):
        raise ValueError('actual retreat criterion required')
    memory.frame(frame)
    continuation = (0x41DE2,0x41E22,0x41E50,0x41E7A,0x41EBA)[kind]
    frame = _object_ai_call_fields(memory,frame,0x41F08,continuation)
    if kind in (0,1):
        frame = _first_word(frame,'count',low16(frame.target_y))
        frame = _scene_render_asl_word(memory,frame,'count',low16(frame.count),1)
        frame = _scene_render_compare(memory,frame,low16(frame.unit),low16(frame.count),16)
        if low16(frame.unit) <= low16(frame.count):
            return memory.sync_status(frame)
        limit = 1000 if kind == 0 else 500
        frame = _scene_render_compare(memory,frame,low16(frame.target_y),limit,16)
        if low16(frame.target_y) > limit:
            return memory.sync_status(frame)
        frame = _object_retreat_roll_fields(memory,frame,0x41DF4 if kind == 0 else 0x41E38,
            0x41EF4 if kind == 0 else 0x41EF8)
        if low8(frame.target_x) == 0:
            return _set_all_object_retreat_modes_fields(memory,frame)
        return memory.sync_status(frame)
    if kind == 2:
        frame = _scene_render_asl_word(memory,frame,'count',low16(frame.count),1)
        frame = _scene_render_compare(memory,frame,low16(frame.distance),low16(frame.count),16)
        if low16(frame.distance) <= low16(frame.count):
            return memory.sync_status(frame)
        frame = _scene_render_compare(memory,frame,low16(frame.unit),low16(frame.target_y),16)
        if low16(frame.unit) <= low16(frame.target_y):
            return memory.sync_status(frame)
        frame = _object_retreat_roll_fields(memory,frame,0x41E62,0x41EFC)
        if low8(frame.target_x) == 0:
            return _set_all_object_retreat_modes_fields(memory,frame)
        return memory.sync_status(frame)
    if kind == 3:
        frame = _scene_render_compare(memory,frame,low16(frame.unit),low16(frame.target_y),16)
        if low16(frame.unit) <= low16(frame.target_y):
            return memory.sync_status(frame)
        morale = memory.state.read(0xFFFF8178,2)
        frame = _scene_render_compare(memory,frame,morale,30,16)
        if morale >= 30:
            return memory.sync_status(frame)
        frame = _object_retreat_roll_fields(memory,frame,0x41E8E,None)
        frame = _scene_render_compare(memory,frame,low16(frame.target_y),2,16)
        if low16(frame.target_y) == 2:
            frame = _first_word(frame,'target_x',low16(frame.target_x) & 7)
            frame = _scene_render_compare(memory,frame,low16(frame.target_x),5,16)
            retreat = low16(frame.target_x) < 5
        else:
            frame = first_replace(frame,roster=memory.cursor_at(0x41F00))
            memory.sync_status(frame)
            mask = frame.roster.byte(low16(frame.target_y))
            frame = _first_byte(frame,'target_x',low8(frame.target_x) & mask)
            retreat = low8(frame.target_x) == 0
        if retreat:
            return _set_all_object_retreat_modes_fields(memory,frame)
        return memory.sync_status(frame)
    frame = _first_word(frame,'target_x',memory.state.read(0xFFFF8104,2))
    memory.sync_status(frame)
    quality = memory.state.read(0xFFFF8106,2)
    frame = _scene_render_compare(memory,frame,low16(frame.target_x),quality,16)
    if low16(frame.target_x) >= quality:
        return memory.sync_status(frame)
    frame = _first_word(frame,'target_x',memory.state.read(0xFFFF8178,2))
    memory.sync_status(frame)
    opposing_morale = memory.state.read(0xFFFF8278,2)
    frame = _scene_render_compare(memory,frame,low16(frame.target_x),opposing_morale,16)
    if low16(frame.target_x) >= opposing_morale:
        return memory.sync_status(frame)
    morale = memory.state.read(0xFFFF8178,2)
    frame = _scene_render_compare(memory,frame,morale,30,16)
    if morale >= 30:
        return memory.sync_status(frame)
    frame = _object_retreat_roll_fields(memory,frame,0x41EE0,0x41F04)
    if low8(frame.target_x) == 0:
        return _set_all_object_retreat_modes_fields(memory,frame)
    return memory.sync_status(frame)

def trigger_object_retreat_strength_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return trigger_object_retreat_check_fields(memory,frame,0)

def trigger_object_retreat_low_strength_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return trigger_object_retreat_check_fields(memory,frame,1)

def trigger_object_retreat_outnumbered_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return trigger_object_retreat_check_fields(memory,frame,2)

def trigger_object_retreat_morale_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return trigger_object_retreat_check_fields(memory,frame,3)

def trigger_object_retreat_quality_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return trigger_object_retreat_check_fields(memory,frame,4)

def advance_object_retreat_checks_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """41DC0: actual eleven-tick comparison and five distinct BSR slots."""
    memory.frame(frame)
    memory.sync_status(frame)
    elapsed = memory.state.read(0xFFFF8160,2)
    frame = _scene_render_compare(memory,frame,elapsed,11,16)
    if elapsed < 11:
        return memory.sync_status(frame)
    for target,continuation in ((0x41DDE,0x41DCC),(0x41E1E,0x41DD0),(0x41E4C,0x41DD4),
            (0x41E76,0x41DD8),(0x41EB6,0x41DDC)):
        frame = _object_ai_call_fields(memory,frame,target,continuation)
    return memory.sync_status(frame)

def choose_object_retreat_phase_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """41F4A: morale/strength gates, four actual opposing probes and phase6."""
    memory.frame(frame)
    memory.sync_status(frame)
    frame = _first_word(frame,'target_x',memory.state.read(0xFFFF80DC,2))
    memory.sync_status(frame)
    opponent_morale = memory.state.read(0xFFFF80E0,2)
    frame = _scene_render_compare(memory,frame,low16(frame.target_x),opponent_morale,16)
    if low16(frame.target_x) == opponent_morale:
        return memory.sync_status(frame)
    frame = _object_ai_call_fields(memory,frame,0x41F08,0x41F5A)
    frame = _scene_render_compare(memory,frame,low16(frame.unit),low16(frame.target_y),16)
    if low16(frame.unit) <= low16(frame.target_y):
        return memory.sync_status(frame)
    frame = _first_word(frame,'target_x',memory.state.read(0xFFFFEFD2,2))
    frame = first_replace(frame,roster=memory.cursor_at(0x41FEC))
    memory.sync_status(frame)
    frame = _first_word(frame,'target_y',memory.state.read(0xFFFF8178,2))
    memory.sync_status(frame)
    threshold = frame.roster.byte(low16(frame.target_x))
    frame = _scene_render_compare(memory,frame,low8(frame.target_y),threshold,8)
    if low8(frame.target_y) >= threshold:
        return memory.sync_status(frame)
    frame = _first_word(frame,'target_x',memory.state.read(0xFFFF8178,2))
    memory.sync_status(frame)
    opponent_morale = memory.state.read(0xFFFF8278,2)
    frame = _scene_render_compare(memory,frame,low16(frame.target_x),opponent_morale,16)
    if low16(frame.target_x) >= opponent_morale:
        return memory.sync_status(frame)
    frame = first_replace(frame,auxiliary=memory.cursor_at(0xFFFF816A))
    for horizontal,vertical,continuation in ((0x8010,0,0x41F92),(0x10,0,0x41FA4),
            (0x8010,0x8010,0x41FB6),(0x10,0x8010,0x41FC8)):
        frame = _first_word(frame,'target_x',horizontal)
        frame = _first_word(frame,'target_y',vertical)
        frame = _object_ai_call_fields(memory,frame,0x414FA,continuation)
        frame = _scene_refresh_flags(memory,frame,low16(frame.target_x),2)
        if low16(frame.target_x):
            break
    else:
        return memory.sync_status(frame)
    frame = _object_ai_call_fields(memory,frame,0x3B722,0x41FD2)
    frame = _first_word(frame,'target_x',low16(frame.target_x) & 3)
    if low16(frame.target_x):
        frame = _scene_refresh_emit(memory,frame,0xFFFF813A,2,6)
        frame = _scene_refresh_emit(memory,frame,0xFFFF813C,2,0)
        frame = _scene_refresh_emit(memory,frame,0xFFFF813E,2,1)
    return memory.sync_status(frame)

def dispatch_object_formation_ai_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """41BE4 actual JMP tail: five known Main sole branches, other targets honest."""
    memory.frame(frame)
    memory.sync_status(frame)
    frame = _first_word(frame,'target_x',memory.state.read(0xFFFF814A,2))
    frame = _scene_render_asl_word(memory,frame,'target_x',low16(frame.target_x),2)
    target = u32(0x41BEE + s16(low16(frame.target_x)))
    for address,kind in ((269294, 0), (269298, 1), (269302, 2), (269306, 3), (269310, 4)):
        if target == address:
            return set_object_formation_orders_fields(memory,frame,kind)
    raise SceneRefreshBoundary(target,memory.sync_status(frame),None)

def dispatch_object_formation_fallback_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """41CD6 mode6 returns; five known Main aliases share the original outer slot."""
    memory.frame(frame)
    memory.sync_status(frame)
    mode = memory.state.read(0xFFFF8130,2)
    frame = _scene_render_compare(memory,frame,mode,6,16)
    if mode == 6:
        return memory.sync_status(frame)
    frame = _first_word(frame,'target_x',memory.state.read(0xFFFF814A,2))
    frame = _scene_render_asl_word(memory,frame,'target_x',low16(frame.target_x),2)
    target = u32(0x41CEA + s16(low16(frame.target_x)))
    for address,kind in ((269546, 0), (269550, 1), (269554, 2), (269558, 0), (269562, 3)):
        if target == address:
            return choose_object_formation_leader_fields(memory,frame,kind)
    raise SceneRefreshBoundary(target,memory.sync_status(frame),None)

def update_object_action_ai_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """41BAC live gates and four actual ordered call slots, no generic provider."""
    memory.frame(frame)
    for expected in (1,2):
        memory.sync_status(frame)
        mode = memory.state.read(0xFFFF80DA,1)
        frame = _scene_render_compare(memory,frame,mode,expected,8)
        if mode == expected:
            return memory.sync_status(frame)
    mode = memory.state.read(0xFFFF814C,1)
    frame = _scene_refresh_flags(memory,frame,mode,1)
    if mode != 0:
        return memory.sync_status(frame)
    mode = memory.state.read(0xFFFF812A,2)
    frame = _scene_render_compare(memory,frame,mode,6,16)
    if mode == 6:
        return memory.sync_status(frame)
    for target,continuation in ((0x41BE4,0x41BCE),(0x41CD6,0x41BD4),(0x41F4A,0x41BDA),(0x41DC0,0x41BE0)):
        frame = _object_ai_call_fields(memory,frame,target,continuation)
    return memory.sync_status(frame)


# C59 complete display/order ABI; historical algorithms are projections only.
"""Complete officer-name, portrait and tile uploads; actual VDP is required.

Confirmed original402C2..4031C and661D4..662E4. The single tile/strip
algorithms own the original register and address updates. Every banked tile
starts again at B649A, as both original LEA instructions require; no copied
second algorithm or ready-device substitute is supplied.
"""
from ..high_level_main_flows.contexts_display_fields import (
    display_frame_fields, display_move_fields, display_store_fields,
    display_address_fields, display_shift_word_fields, display_shift_long_fields,
    display_loop_fields, display_call_fields,
)


def upload_object_officer_name_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """402C2: actual D7 MULU, optional fill, AE8A slot40306, then96 LONGs."""
    from ..high_level_main_flows.business_movement_support import (
        _movement_multiply_word, _movement_compare)
    frame = display_frame_fields(state, frame)
    frame = _movement_multiply_word(state, frame, 'choice', 6)
    frame = display_address_fields(state, frame, 'roster', 0x8A504)
    frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.choice))))
    frame = display_move_fields(state, frame, 'count', 2)
    frame = _movement_compare(state, frame, frame.roster.word(4), 0x3F, 16)
    if frame.status & 4:
        frame = display_move_fields(state, frame, 'count', 1)
        frame = display_move_fields(state, frame, 'distance', low16(frame.target_x))
        frame = _scene_render_asl_word(SceneRefreshMemory(state), frame,
            'distance', low16(frame.distance), 4)
        frame = display_move_fields(state, frame, 'distance',
            low16(frame.distance) | low16(frame.target_x))
        frame = display_move_fields(state, frame, 'offset_x', 0x3F)
        frame = display_address_fields(state, frame, 'candidates', 0xFFFFD300)
        frame = display_address_fields(state, frame, 'controller', 0xFFFFD440)
        while True:
            frame = display_store_fields(state, frame, 0x402F2,
                frame.candidates.base, low8(frame.distance), 1)
            frame = first_replace(frame, candidates=frame.candidates.advance(1))
            frame = display_store_fields(state, frame, 0x402F4,
                frame.controller.base, low8(frame.distance), 1)
            frame = first_replace(frame, controller=frame.controller.advance(1))
            frame, more = display_loop_fields(frame, 'offset_x')
            if not more:
                break
    else:
        frame = display_address_fields(state, frame, 'candidates', 0xFFFFD300)
    frame = display_call_fields(state, frame, 0xAE8A, 0x40306)
    frame = display_address_fields(state, frame, 'roster', 0xFFFFD300)
    frame = display_address_fields(state, frame, 'auxiliary', 0xC00000)
    frame = display_move_fields(state, frame, 'target_x', 0x5F)
    while True:
        pixels = frame.roster.long()
        frame = first_replace(frame, roster=frame.roster.advance(4))
        frame = display_store_fields(state, frame, 0x40314,
            frame.auxiliary.base, pixels, 4)
        frame, more = display_loop_fields(frame, 'target_x')
        if not more:
            return frame


def upload_one_scene_tile_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """662C4: zero highWORD before LSL.L5, actual8 LONG DATA reads/writes."""
    frame = display_frame_fields(state, frame)
    frame = display_address_fields(state, frame, 'candidates', 0xB649A)
    frame = display_move_fields(state, frame, 'unit', frame.unit & 0xFFFF, 32)
    frame = display_shift_long_fields(state, frame, 'unit', 5)
    frame = first_replace(frame, candidates=frame.candidates.advance(frame.unit))
    frame = display_move_fields(state, frame, 'count', 7)
    while True:
        pixels = frame.candidates.long()
        frame = first_replace(frame, candidates=frame.candidates.advance(4))
        frame = display_store_fields(state, frame, 0x662D8, 0xC00000, pixels, 4)
        frame, more = display_loop_fields(frame, 'count')
        if not more:
            return frame


def upload_scene_tile_block_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """662B4: each of48 original WORD IDs owns its actual662BE BSR LONG."""
    frame = display_frame_fields(state, frame)
    frame = display_move_fields(state, frame, 'distance', 0x2F)
    while True:
        tile = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = display_move_fields(state, frame, 'unit', tile)
        frame = display_call_fields(state, frame, 0x662C4, 0x662BE)
        frame, more = display_loop_fields(frame, 'distance')
        if not more:
            return frame


def _portrait_banked_strip_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame, second: bool) -> FirstDeploymentFrame:
    """One two-role strip loop; both real LEAs reset A1 on EVERY tile."""
    from ..high_level_main_flows.business_movement_support import (
        _movement_compare, _movement_add_word)
    if type(second) is not bool:
        raise ValueError('actual first/second portrait strip required')
    while True:
        frame = display_address_fields(state, frame, 'candidates', 0xB649A)
        tile = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = display_move_fields(state, frame, 'count', tile)
        frame = _movement_compare(state, frame, low16(frame.count), 0x800, 16)
        if not frame.status & 1:
            frame = first_replace(frame, candidates=frame.candidates.advance(0x10000))
        frame = display_shift_word_fields(state, frame, 'count', 5)
        frame = display_move_fields(state, frame, 'distance', 7)
        while True:
            pixels = state.read(u32(frame.candidates.base + s16(low16(frame.count))), 4)
            frame = display_store_fields(state, frame,
                0x66268 if second else 0x6622A, 0xC00000, pixels, 4)
            frame = _movement_add_word(state, frame, 'count', 4)
            frame, more = display_loop_fields(frame, 'distance')
            if not more:
                break
        frame, more = display_loop_fields(frame, 'unit')
        if not more:
            return frame


def upload_portrait_tiles_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """661D4: three real tile families then the live palette BYTE directory."""
    from ..high_level_main_flows.business_movement_support import (
        _movement_add_word, _movement_compare)
    from ..high_level_remaining_flows.business_city import _special_action_swap
    frame = display_frame_fields(state, frame)
    frame = display_move_fields(state, frame, 'target_y', frame.target_y & 0xFFFF, 32)
    frame = display_shift_long_fields(state, frame, 'target_y', 7)
    frame = display_shift_word_fields(state, frame, 'target_y', 2, True)
    frame = display_move_fields(state, frame, 'target_y', low16(frame.target_y) | 0x4000)
    frame = _special_action_swap(state, frame, 'target_y')
    frame = display_store_fields(state, frame, 0x661E4, 0xC00004, frame.target_y, 4)
    frame = display_move_fields(state, frame, 'target_y', low16(frame.target_x))
    frame = display_shift_word_fields(state, frame, 'target_y', 1)
    frame = _movement_add_word(state, frame, 'target_y', low16(frame.target_x))
    frame = display_shift_word_fields(state, frame, 'target_y', 5)
    frame = display_address_fields(state, frame, 'roster', 0xAE39A)
    frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.target_y))))
    frame = display_call_fields(state, frame, 0x662B4, 0x661FE)
    frame = display_move_fields(state, frame, 'target_y', low16(frame.target_x))
    frame = display_shift_word_fields(state, frame, 'target_y', 4)
    frame = display_address_fields(state, frame, 'roster', 0xB439A)
    frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.target_y))))
    frame = display_move_fields(state, frame, 'unit', 7)
    frame = _portrait_banked_strip_frame_fields(state, frame, False)
    frame = display_move_fields(state, frame, 'target_y', low16(frame.target_x))
    frame = display_shift_word_fields(state, frame, 'target_y', 3)
    frame = display_address_fields(state, frame, 'roster', 0xB539A)
    frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.target_y))))
    frame = display_move_fields(state, frame, 'unit', 3)
    frame = _portrait_banked_strip_frame_fields(state, frame, True)
    frame = display_address_fields(state, frame, 'candidates', 0xB599A)
    frame = display_address_fields(state, frame, 'controller', 0xB639A)
    frame = display_move_fields(state, frame, 'target_y', 0, 32)
    frame = display_move_fields(state, frame, 'target_y',
        state.read(u32(frame.controller.base + s16(low16(frame.target_x))), 1), 8)
    frame = display_shift_long_fields(state, frame, 'target_y', 5)
    frame = first_replace(frame, candidates=frame.candidates.advance(frame.target_y))
    frame = display_move_fields(state, frame, 'unit', 7)
    frame = display_address_fields(state, frame, 'controller', 0xFFFFFB00)
    frame = _movement_compare(state, frame, state.read(0xFFFFF6C4, 2), 2, 16)
    if frame.status & 4:
        frame = display_address_fields(state, frame, 'controller', 0xFFFFFB20)
    while True:
        color = frame.candidates.long()
        frame = first_replace(frame, candidates=frame.candidates.advance(4))
        frame = display_store_fields(state, frame, 0x662A6, frame.controller.base, color, 4)
        frame = first_replace(frame, controller=frame.controller.advance(4))
        frame, more = display_loop_fields(frame, 'unit')
        if not more:
            return display_store_fields(state, frame, 0x662AC, 0xFFFFF31E, 1)
