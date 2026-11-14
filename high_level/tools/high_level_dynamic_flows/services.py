"""Earlier logical scene services on the same typed live RAM.

All aliases call real recovered logic. Alternate entries below intentionally
skip only the actual original prefix; no duplicate initialization or fake RTS.
Tables/art remain explicitly supplied ReadOnlyData, never embedded media.
"""
from dataclasses import dataclass, replace
from .domain import (
    SceneState, Table, Cursor, Byte, Word, Long, Boundary, uint, u8, u16, u32,
    low8, low16, high16, s16, replace_word, replace_byte, swap_words,
    negative_word, negative_long, descending_inclusive, divu_retained,
    checked_state, checked_table, checked_cursor, VideoPlaneAddress,
    StackContinuation, RandomSample, ram_view,
)
from ..high_level_scene_flows.business_reuse import (
    enqueue_sound_command, step_random, _reuse_advance_random_pair,
)
from ..high_level_scene_flows.business_duel import (
    refresh_duel_actors, choose_duel_status_text, wait_active_duel_action,
    wait_either_duel_action, clear_duel_text_plane, measure_duel_weapon_contact,
)
from ..high_level_scene_flows.business_scene import (
    advance_scene_palette_fade, append_unclipped_scene_sprites,
    read_vdp_plane_rle_rows, sample_random_preserving_seed_carrier,
    decode_glyph_rows_to_buffers, darken_palette, fade_palette_component,
    advance_plane_row, set_vram_write_address as _original_vram_address,
)
from ..high_level_scene_flows.business_objects import (
    read_object_action_mode, offset_scene_object_position, plan_scene_object_action,
    probe_scene_object_overlap, probe_opposing_object_overlap,
    clear_scene_object_label_plane, initialize_scene_object_roster,
    normalize_object_squad_size, _append_sprite_entries,
    resume_selected_object_action_complete,
)
from ..high_level_scene_flows.contexts_scene import (
    PlaneRowContext, PlaneStreamResult, PaletteComponentResult,
)
from ..high_level_scene_flows.contexts_objects import (
    SceneRenderFrame, SpriteBatchContext, SpriteBatchResult, checked_context,
    ObjectPositionOffset, ObjectOverlapOutcome,
)


def _ram(state, low):
    return ram_view(state, 'ram_' + low)


def _video_address(value):
    if type(value) is not VideoPlaneAddress:
        raise ValueError('typed video address required')
    return value


def set_vram_write_address(state: SceneState,
                           value: VideoPlaneAddress | Long) -> Long:
    """Accept an explicit video carrier, never dereference it as RAM."""
    if type(value) is not VideoPlaneAddress:
        value = VideoPlaneAddress(uint(value, 32))
    return _original_vram_address(state, value)


def append_scene_sprite_entries(state: SceneState,
                                context: SpriteBatchContext) -> SpriteBatchResult:
    """Original3B13C shared tail, without another public entry's prefix."""
    return _append_sprite_entries(state, context)


def _reset_object_action_controls(state):
    for low in ('814c', '814e', '8150', '8152', '8154', '8156', '8158',
                '815a', '815c', '815e', '8160', '8162', '8164', '8166', '8168'):
        _ram(state, low).set_word(0, 0)


def _read_pointer(state, table, offset):
    return state.table_at(table.long(offset))

def sample_random_pair(state: SceneState) -> RandomSample:
    """83D4: return sample and updated seed from the single original call.

    Several callers consume both full LONGs. Reading the seed again after
    the call would insert a new live-memory observation into that sequence.
    """
    return _reuse_advance_random_pair(state)


def probe_scene_object_overlap_with_frame(state: SceneState, actor: Table,
        offset: ObjectPositionOffset, frame: SceneRenderFrame
        ) -> tuple[ObjectOverlapOutcome, SceneRenderFrame]:
    """4115C including observable coordinate and saved-position values.

    Candidate coordinates are read once in original order. y retains its
    high WORD; the full saved XY pair becomes palette's retained carrier.
    Both successful and exhausted scans restore with one LONG write.
    """
    checked_state(state)
    checked_table(actor, state)
    checked_context(offset, ObjectPositionOffset, state)
    checked_context(frame, SceneRenderFrame, state)
    saved_position = actor.long(0, 2)
    offset_scene_object_position(state, actor, offset)
    y = replace_word(frame.y, offset.vertical & 0x7F
                     if negative_word(offset.vertical) else offset.vertical)
    attributes = replace_word(frame.attributes, offset.vertical)
    candidate = _ram(state, '816a')
    found = False
    while candidate.base < 0xFFFF836A:
        if candidate.byte() & 128 and candidate.base != actor.base:
            y = replace_word(y, candidate.word(0, 2))
            if low16(y) == actor.word(0, 2):
                y = replace_word(y, candidate.word(0, 4))
                if low16(y) == actor.word(0, 4):
                    found = True
                    break
        candidate = state.table_at(u32(candidate.base + 16))
    actor.set_long(0, saved_position, 2)
    return (ObjectOverlapOutcome(found, candidate),
            SceneRenderFrame(1 if found else 0, y, attributes,
                             saved_position, frame.tile))


def resume_selected_object_action(state: SceneState, actor: Table,
                                 opponent: Table, frame: SceneRenderFrame):
    """40CAC alternate entry, not another full40C94 side-selection call."""
    from .business_actions import _resume_primary_action_selection
    return _resume_primary_action_selection(state, actor, opponent, frame)


def continue_duel_fadeout(state: SceneState, controls, actor_values):
    """26D46 real fade-out tail, never return to discarded27572.

    Keep the earlier typed scene result contract. Callers separately propagate
    a DuelTurnOutcome's nonlocal marker rather than consuming it locally.
    """
    from ..high_level_scene_flows.business_duel import _finish_duel_scene
    return _finish_duel_scene(state, controls, actor_values)


def read_vdp_plane_rle_rows_from_control(state: SceneState, source: Cursor,
        video_address: VideoPlaneAddress, row_stride: Long, rows: Word) -> PlaneStreamResult:
    """3AAD6 alternate entry: preserve8000 and the caller-supplied rows."""
    checked_state(state)
    checked_cursor(source, state)
    _video_address(video_address)
    uint(row_stride, 32)
    uint(rows, 16)
    _ram(state, '8002').set_word(0, 0)
    state.write(0xC00004, 2, 0x8F02)
    command = set_vram_write_address(state, video_address)
    column, marker = 0, 0
    if _ram(state, '8002').word() == 0:
        marker = source.next_byte()
    while True:
        high = source.next_byte()
        literal = _ram(state, '8002').word() != 0 or marker != high
        if literal:
            value = high << 8 | source.next_byte()
            value |= _ram(state, '8000').word()
            state.write(0xC00000, 2, value)
            row = advance_plane_row(state, PlaneRowContext(video_address,
                row_stride, column, rows, command, StackContinuation(0x3AB10)))
        else:
            count = source.next_byte()
            if count == 0:
                return PlaneStreamResult(source, video_address, command, column, rows, None)
            value = source.next_byte() << 8 | source.next_byte()
            for _ in descending_inclusive(count):
                value |= _ram(state, '8000').word()
                state.write(0xC00000, 2, value)
                row = advance_plane_row(state, PlaneRowContext(video_address,
                    row_stride, column, rows, command, StackContinuation(0x3AB2C)))
                video_address, column, rows, command = (row.video_address,
                    row.column, row.rows_remaining, row.command_carrier)
                if row.discarded_continuation is not None:
                    return PlaneStreamResult(source, video_address, command,
                        column, rows, row.discarded_continuation)
        video_address, column, rows, command = (row.video_address,
            row.column, row.rows_remaining, row.command_carrier)
        if row.discarded_continuation is not None:
            return PlaneStreamResult(source, video_address, command,
                column, rows, row.discarded_continuation)

def initialize_scene_object_roster_after_mode_check(
        state: SceneState, context: SceneRenderFrame) -> SceneRenderFrame:
    """41818 alternate entry: no512-byte clear or two80DA mode checks."""
    checked_context(context, SceneRenderFrame, state)
    for name in ('80e8', '80f4', '80f6', '80f8'):
        _ram(state, name).set_word(0, 0)
    if _ram(state, '80e4').word() != 0:
        _ram(state, '80e8').set_word(0, 1)
        if _ram(state, '80e4').word() >= 100:
            if _ram(state, '80e4').word() < 1500:
                while True:
                    choice = low16(sample_random_preserving_seed_carrier(state)) & 15
                    if choice <= 9:
                        break
                _ram(state, '80e8').set_word(0, u16(choice + 1))
            elif _ram(state, '80e4').word() < 5000:
                while True:
                    choice = low16(sample_random_preserving_seed_carrier(state)) & 15
                    if choice <= 5:
                        break
                _ram(state, '80e8').set_word(0, u16(choice + 5))
            else:
                _ram(state, '80e8').set_word(0, 15)
                if _ram(state, '80e4').word() < 10000:
                    while True:
                        choice = low16(sample_random_preserving_seed_carrier(state)) & 15
                        if choice <= 5:
                            break
                    _ram(state, '80e8').set_word(0, u16(choice + 10))
        normalize_object_squad_size(state)
        first, second = 0, 2
        for threshold, first_count, second_count in (
                (100, 0, 2), (200, 1, 3), (300, 3, 4),
                (400, 5, 5), (500, 6, 6), (600, 7, 7)):
            first, second = first_count, second_count
            if _ram(state, '8110').word() <= threshold:
                break
        else:
            first, second = 8, 8
        for name in ('80f4', '80f6', '80f8'):
            _ram(state, name).set_word(0, 0)
        remainder = u16(_ram(state, '80e8').word() - first)
        if negative_word(remainder):
            _ram(state, '80f4').set_word(0, _ram(state, '80e8').word())
        else:
            _ram(state, '80f4').set_word(0, first)
            _ram(state, '80f6').set_word(0, remainder)
            remainder = u16(remainder - second)
            if not negative_word(remainder):
                _ram(state, '80f6').set_word(0, second)
                _ram(state, '80f8').set_word(0, remainder)
        if _ram(state, '80db').byte() == 3:
            _ram(state, '80f4').set_word(0, 0)
            _ram(state, '80f6').set_word(0, _ram(state, '80e8').word())
            _ram(state, '80f8').set_word(0, 0)
    while True:
        layout_carrier = sample_random_preserving_seed_carrier(state)
        choice = low16(layout_carrier) & 7
        layout_carrier = replace_word(layout_carrier, choice)
        if choice <= 4:
            break
        # The original back edge includes the mode-three partition override.
        if _ram(state, '80db').byte() == 3:
            _ram(state, '80f4').set_word(0, 0)
            _ram(state, '80f6').set_word(0, _ram(state, '80e8').word())
            _ram(state, '80f8').set_word(0, 0)
    _ram(state, '814a').set_word(0, choice)
    layout = _read_pointer(state, state.table_at(0x41A58), u16(choice << 2)).cursor()
    first = _ram(state, '80f4').word()
    second = _ram(state, '80f6').word()
    third = _ram(state, '80f8').word()
    actor = _ram(state, '816a')
    leader = True
    object_count = 0
    while True:
        if leader:
            kind = 0x8003
            leader = False
        elif first:
            kind, first = 0x8002, u16(first - 1)
        elif second:
            kind, second = 0x8001, u16(second - 1)
        elif third:
            kind, third = 0x8000, u16(third - 1)
        else:
            break
        actor.set_word(0, layout.next_word(), 2)
        actor.set_word(0, layout.next_word(), 4)
        actor.set_word(0, kind)
        object_count = u16(object_count + 1)
        actor = actor.advance(16)
    quality = _ram(state, '8104').word()
    factor = _ram(state, '8100').word()
    packed = divu_retained(u32(factor * quality), 100)
    remainder = _ram(state, '80f0').word()
    actor = _ram(state, '817a')
    for _ in descending_inclusive(14):
        actor.set_word(0, low16(packed), 12)
        actor.set_word(0, _ram(state, '80ec').word(), 14)
        if remainder != 0:
            remainder = u16(remainder - 1)
            actor.set_word(0, u16(actor.word(0, 14) + 1), 14)
        actor = actor.advance(16)
    strength = _ram(state, '8104').word()
    strength = u16(strength + _ram(state, '8108').word())
    _ram(state, '8176').set_word(0, strength)
    _ram(state, '8178').set_word(0, _ram(state, '810c').word())
    _reset_object_action_controls(state)
    return SceneRenderFrame(replace_word(layout_carrier, strength), packed,
        replace_word(context.attributes, remainder), object_count,
        context.tile)

@dataclass(frozen=True)
class DivisionFields:
    """35760 family observations, not a general CPU context."""
    quotient: Long
    remainder: Long
    factor: Long
    weapon: Long
    working: Long
    stack: Cursor | None
    conditions: object


def _math_flags(value, *, bits=32, carry=False, overflow=False):
    from ..high_level_scene_flows.contexts_duel import DuelConditionObservation
    masked = value & ((1 << bits) - 1)
    return DuelConditionObservation(carry, masked == 0,
                                    bool(masked & (1 << (bits - 1))), overflow)


def _math_stack_save(stack, values, width):
    """Actual predecrement MOVEM order; no invented BSR token write."""
    if stack is None:
        return None
    for value in reversed(values):
        stack = stack.advance(-width)
        if width == 2:
            stack.set_word(0, low16(value))
        else:
            stack.set_long(0, value)
    return stack


def _math_stack_restore(stack, fallback, width):
    if stack is None:
        return fallback, None
    value = stack.word() if width == 2 else stack.long()
    return value, stack.advance(width)


def _word_pair_fields(state, values):
    numerator, denominator = values.quotient, values.remainder
    stack = _math_stack_save(values.stack, (numerator, values.factor), 2)
    upper = divu_retained(high16(numerator), low16(denominator))
    factor = replace_word(values.factor, low16(upper))
    saved_low, stack = _math_stack_restore(stack, low16(numerator), 2)
    lower = divu_retained(replace_word(upper, saved_low), low16(denominator))
    quotient = swap_words(replace_word(swap_words(lower), low16(factor)))
    remainder = high16(lower)
    restored_factor, stack = _math_stack_restore(stack, low16(values.factor), 2)
    factor = replace_word(factor, restored_factor)
    return DivisionFields(quotient, remainder, factor, values.weapon, values.working,
                          stack, _math_flags(restored_factor, bits=16))


def _unsigned_fields(state, values):
    numerator, denominator = values.quotient, values.remainder
    if denominator <= 65535:
        return _word_pair_fields(state, values)
    if denominator == numerator:
        return replace(values, quotient=1, remainder=0, conditions=_math_flags(0))
    if denominator > numerator:
        return replace(values, quotient=0, remainder=numerator, conditions=_math_flags(0))
    # 35794 saves three LONGs. The nested word-pair call has another 4-byte
    # logical call frame; live saved values, not entry snapshots, are restored.
    saved = _math_stack_save(values.stack, (values.factor, values.weapon, values.working), 4)
    factor = u32(high16(denominator) + 1)
    nested_stack = None if saved is None else saved.advance(-4)
    pair = _word_pair_fields(state, DivisionFields(numerator, factor, factor,
        numerator, denominator, nested_stack, values.conditions))
    divisor_part = divu_retained(denominator, low16(pair.factor))
    quotient = low16(divu_retained(pair.quotient, low16(divisor_part)))
    while True:
        low_product = u32(low16(denominator) * low16(quotient))
        upper_product = swap_words(u32(high16(denominator) * low16(quotient)))
        product = u32(low_product + upper_product)
        if product > numerator:
            quotient = u32(quotient - 1)
            continue
        remainder = u32(numerator - product)
        if denominator <= remainder:
            quotient = u32(quotient + 1)
            continue
        factor, saved = _math_stack_restore(saved, values.factor, 4)
        weapon, saved = _math_stack_restore(saved, values.weapon, 4)
        working, saved = _math_stack_restore(saved, values.working, 4)
        # MOVEM does not alter flags; the final CMP D2,D5 has D5>D2.
        difference = u32(denominator - remainder)
        overflow = bool(((denominator ^ remainder) &
                         (denominator ^ difference)) & 0x80000000)
        return DivisionFields(quotient, remainder, factor, weapon, working, saved,
            _math_flags(difference, carry=denominator < remainder, overflow=overflow))


def _positive_fields(state, values):
    if negative_long(values.quotient):
        inner = replace(values, quotient=u32(-values.quotient),
            stack=None if values.stack is None else values.stack.advance(-4))
        result = _unsigned_fields(state, inner)
        quotient, remainder = u32(-result.quotient), u32(-result.remainder)
        return replace(result, quotient=quotient, remainder=remainder,
            stack=None if result.stack is None else result.stack.advance(4),
            conditions=_math_flags(remainder, carry=result.remainder != 0,
                                   overflow=result.remainder == 0x80000000))
    return _unsigned_fields(state, values)


def _signed_fields(state, values):
    if negative_long(values.remainder):
        inner = replace(values, remainder=u32(-values.remainder),
            stack=None if values.stack is None else values.stack.advance(-4))
        result = _positive_fields(state, inner)
        quotient = u32(-result.quotient)
        return replace(result, quotient=quotient,
            stack=None if result.stack is None else result.stack.advance(4),
            conditions=_math_flags(quotient, carry=result.quotient != 0,
                                   overflow=result.quotient == 0x80000000))
    return _positive_fields(state, values)


def _division_projection(state, numerator, denominator, algorithm):
    checked_state(state)
    uint(numerator, 32)
    uint(denominator, 32)
    fields = DivisionFields(numerator, denominator, 0, 0, 0, None, None)
    result = algorithm(state, fields)
    return result.quotient, result.remainder


def word_pair_divmod(state: SceneState, numerator: Long, denominator: Long) -> tuple[Long, Long]:
    return _division_projection(state, numerator, denominator, _word_pair_fields)


def unsigned_divmod(state: SceneState, numerator: Long, denominator: Long) -> tuple[Long, Long]:
    return _division_projection(state, numerator, denominator, _unsigned_fields)


def positive_denominator(state: SceneState, numerator: Long, denominator: Long) -> tuple[Long, Long]:
    return _division_projection(state, numerator, denominator, _positive_fields)


def signed_divmod(state: SceneState, numerator: Long, denominator: Long) -> tuple[Long, Long]:
    return _division_projection(state, numerator, denominator, _signed_fields)


def divide_duel_frame(state, frame):
    """Full current signed division at callee-entry SP, D0 is never written."""
    from ..high_level_scene_flows.contexts_duel import checked_duel_turn
    checked_duel_turn(frame, state)
    result = _signed_fields(state, DivisionFields(frame.comparison, frame.distance,
        frame.factor, frame.weapon_difference, frame.working_value, frame.stack,
        frame.conditions))
    return replace(frame, comparison=result.quotient, distance=result.remainder,
        factor=result.factor, weapon_difference=result.weapon, working_value=result.working,
        stack=result.stack, conditions=result.conditions)


def duel_complete_service(state, frame, name, selection=None):
    """One actual BSR bridge; scene cores themselves receive function-entry SP."""
    from ..high_level_scene_flows import business_duel
    from ..high_level_scene_flows.contexts_duel import checked_duel_turn
    checked_duel_turn(frame, state)
    child = replace(frame, stack=frame.stack.advance(-4))
    if name == 'choose_duel_status_text_complete':
        result = business_duel.choose_duel_status_text_complete(state, uint(selection, 16), child)
    elif name == 'wait_active_duel_action_complete':
        result = business_duel.wait_active_duel_action_complete(state, child)
    elif name == 'wait_either_duel_action_complete':
        result = business_duel.wait_either_duel_action_complete(state, child)
    elif name == 'clear_duel_text_complete':
        result = business_duel.clear_duel_text_complete(state, child)
    else:
        raise Boundary('unsupported complete duel service: ' + name)
    checked_duel_turn(result, state)
    return replace(result, stack=result.stack.advance(4))

# B35 same Scene state/full frame, sole established object math and real slots.
from ..high_level_scene_flows.contexts_scene import (
    SceneRefreshMemory,SceneRefreshBoundary,FirstDeploymentFrame,first_replace,
    _first_word,_first_long,_scene_refresh_emit,_scene_refresh_flags,
)
from ..high_level_scene_flows.business_scene import (
    _scene_render_compare,_scene_render_arithmetic,_scene_render_bit,
    _scene_render_asl_word,sample_random_preserving_seed_fields,
)
from ..high_level_scene_flows.business_objects import (
    _object_clear_word_fields,probe_scene_object_overlap_fields,
    read_object_action_mode_fields,update_selected_object_action_fields,
    _scene_controller_legacy_fields,_scene_controller_legacy_projection,
)
from ..high_level_gameplay_flow.business_battle import _presentation_call_fields
from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
from ..high_level_main_flows.business_movement_support import _movement_binary_flags

# B36 actual Scene sprite/offset/sound and fixed-width arithmetic, no duplicate core.
from ..high_level_scene_flows.business_objects import (
    _object_adjust_word_fields,_object_shift_word_right_fields,
    offset_scene_object_position_fields,_append_object_sprite_fields,
)
from ..high_level_scene_flows.business_scene import _scene_render_push_longs
from ..high_level_main_flows.business_movement_support import _movement_divu_word
from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields

# B37 same Scene state/full frame: sole opposing probe and DBRA/retained-BYTE helpers.
from ..high_level_scene_flows.business_objects import probe_opposing_object_overlap_fields
from ..high_level_scene_flows.contexts_scene import _first_byte
from ..high_level_gameplay_flow.business_services import _scene_refresh_decrement


def set_object_formation_orders_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, kind: Word) -> FirstDeploymentFrame:
    """Fixed lazy delegate avoids Main-services/Dynamic import cycle; no algorithm."""
    from ..high_level_main_flows.business_scene_support import set_scene_object_formation_orders_fields
    return set_scene_object_formation_orders_fields(memory,frame,kind)


def choose_object_formation_leader_fields(memory: SceneRefreshMemory,
        frame: FirstDeploymentFrame, kind: Word) -> FirstDeploymentFrame:
    """Fixed lazy delegate to the sole Main leader family; no registry/provider."""
    from ..high_level_main_flows.business_scene_support import choose_scene_object_leader_action_fields
    return choose_scene_object_leader_action_fields(memory,frame,kind)

# B39 main phase shares the already-restored Scene label/plane cores, no renderer copy.
from ..high_level_scene_flows.business_objects import clear_scene_object_label_plane_fields
from ..high_level_scene_flows.business_scene import read_vdp_plane_rle_rows_fields

# D43 current full-LONG comparison authority; no new arithmetic algorithm.
from ..high_level_battle_ai.business_formation import _first_compare_long
