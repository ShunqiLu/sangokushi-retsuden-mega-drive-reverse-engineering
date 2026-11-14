"""Officer growth/selection and high-bank scrolling message business rules.

Parameters and glyph pixels are supplied readonly resources. Original WORD
wrapping, live aliases, packed DIVU and unguarded list searches are preserved.
"""

from .contexts_gameplay import FirstDeploymentFrame, FirstDeploymentReturnBoundary, MovementContinuationBoundary, first_replace
from .business_movement_support import (_movement_move, _movement_move_long,
    _movement_test, _movement_test_long, _movement_compare, _movement_add_word,
    _movement_binary_flags, _movement_arithmetic_long, _movement_divu_word,
    _movement_multiply_word, _movement_save_longs, _movement_restore_longs, _movement_shift_long)
from .domain import low8

from dataclasses import replace
from .domain import (SceneState, Table, Cursor, Long, Word, Boundary, uint,
    u8, u16, u32, s16, low8, low16, replace_byte, replace_word, swap_words,
    negative_byte, negative_word, divu_retained, descending_inclusive,
    checked_state, ram_view, data_view)
from .contexts_highbank import (GrowthValues, GrowthResult, GrowthFrame,
    FullGrowthResult, GrowthScanObservation, OfficerSelection,
    MessageLayout, MessageDispatch, ScrollingMessageAdvance, checked_context)
from .contexts_render import RenderFields, checked_render_fields
from .contexts_tick import MapTickFrame, checked_tick_frame



from .contexts_highbank import MessageControlFields

def _ram(state, name):
    return ram_view(state, 'ram_' + name)


def _word(state, name):
    return _ram(state, name).word()


def _put(state, name, value):
    _ram(state, name).set_word(0, u16(value))


def _carry(state, value):
    status = state.read_status_word()
    state.set_status_word(status | 1 if value else status & 0xFFFE)


def _random(state):
    from .services import step_random
    return step_random(state)


def _ratio_attribute_growth(state, values, first):
    """Historical values project the sole weighted-growth fields, never a copied algorithm."""
    checked_context(values, GrowthValues, state)
    frame = _growth_ratio_attribute_fields(state, _growth_project_values_fields(values), first)
    return GrowthValues(frame.target_x, frame.target_y, frame.unit)


def increase_growth_first_attribute(state: SceneState, values: GrowthValues) -> GrowthValues:
    checked_context(values, GrowthValues, state)
    frame = increase_growth_first_attribute_fields(state, _growth_project_values_fields(values))
    return GrowthValues(frame.target_x, frame.target_y, frame.unit)


def increase_growth_second_attribute(state: SceneState, values: GrowthValues) -> GrowthValues:
    checked_context(values, GrowthValues, state)
    frame = increase_growth_second_attribute_fields(state, _growth_project_values_fields(values))
    return GrowthValues(frame.target_x, frame.target_y, frame.unit)


def increase_growth_random_attribute(state: SceneState, values: GrowthValues) -> GrowthValues:
    checked_context(values, GrowthValues, state)
    frame = increase_growth_random_attribute_fields(state, _growth_project_values_fields(values))
    return GrowthValues(frame.target_x, frame.target_y, frame.unit)


def increase_growth_command_radius(state: SceneState, values: GrowthValues) -> GrowthValues:
    checked_context(values, GrowthValues, state)
    frame = increase_growth_command_radius_fields(state, _growth_project_values_fields(values))
    return GrowthValues(frame.target_x, frame.target_y, frame.unit)


def check_growth_notification_owner(state: SceneState, values: GrowthValues) -> GrowthResult:
    checked_context(values, GrowthValues, state)
    frame = check_growth_notification_owner_fields(state, _growth_project_values_fields(values))
    return GrowthResult(GrowthValues(frame.target_x, frame.target_y, frame.unit),
        bool(frame.status & 1), frame.opponent)


def _scan_officer_growth(state, values, attribute_pointer, owner_pointer):
    """Same-core old observation projection; absent full D/A/X/SP stops before mutation."""
    checked_context(values, GrowthValues, state)
    frame = advance_officer_growth_levels_fields(state,
        _growth_project_values_fields(values, attribute_pointer, owner_pointer))
    return GrowthScanObservation(GrowthValues(frame.target_x, frame.target_y, frame.unit),
        state.table_at(frame.roster.base), state.table_at(frame.candidates.base),
        frame.controller, state.table_at(frame.scan.base), frame.opponent,
        frame.scratch, frame.auxiliary, bool(frame.status & 1), bool(frame.status & 4),
        bool(frame.status & 8), bool(frame.status & 2))


def scan_officer_growth_levels(state: SceneState, frame: GrowthFrame) -> FullGrowthResult:
    'Historical retained-view projection; unobserved complete D/A/X/SP is a genuine boundary.'
    checked_context(frame, GrowthFrame, state)
    observed = _scan_officer_growth(state, frame.values,
        frame.attribute_pointer, frame.owner_pointer)
    return observed.complete(state)


def advance_officer_growth_levels(state: SceneState, values: GrowthValues) -> GrowthResult:
    'Historical values/C/A6 projection of the sole full fields; no unobserved CPU field is invented.'
    checked_context(values, GrowthValues, state)
    observed = _scan_officer_growth(state, values, None, None)
    return GrowthResult(observed.values, observed.carry, observed.assignments)


def sort_high_loyalty_officers(state: SceneState, choice: OfficerSelection) -> OfficerSelection:
    """Legacy observations project the sole fields; missing A7/CCR/high fields stay unknown."""
    entered=_highbank_selection_observation_fields(state,choice)
    returned=sort_high_loyalty_officers_fields(state,entered)
    return _highbank_selection_projection(state,returned)


def append_mid_loyalty_officers_by_trait(state: SceneState, choice: OfficerSelection) -> OfficerSelection:
    """Legacy observations project the sole fields; missing A7/CCR/high fields stay unknown."""
    entered=_highbank_selection_observation_fields(state,choice)
    returned=append_mid_loyalty_officers_by_trait_fields(state,entered)
    return _highbank_selection_projection(state,returned)


def build_ten_officer_selection(state: SceneState, choice: OfficerSelection) -> OfficerSelection:
    """Legacy observations project the sole fields; missing A7/CCR/high fields stay unknown."""
    entered=_highbank_selection_observation_fields(state,choice)
    returned=build_ten_officer_selection_fields(state,entered)
    return _highbank_selection_projection(state,returned)


def select_highest_trait_officer(state: SceneState, choice: OfficerSelection) -> OfficerSelection:
    """Legacy observations project the sole fields; missing A7/CCR/high fields stay unknown."""
    entered=_highbank_selection_observation_fields(state,choice)
    returned=select_highest_trait_officer_fields(state,entered)
    return _highbank_selection_projection(state,returned)


def calculate_force_command_budget(state: SceneState, choice: OfficerSelection) -> OfficerSelection:
    """Legacy observations project the sole fields; missing A7/CCR/high fields stay unknown."""
    entered=_highbank_selection_observation_fields(state,choice)
    returned=calculate_force_command_budget_fields(state,entered)
    return _highbank_selection_projection(state,returned)


def _dispatch_message(state, target, selector, layout, continuation):
    from .services import call_target
    result = call_target(state, u32(target), MessageDispatch(selector, layout, continuation))
    if type(result) is not MessageLayout:
        raise Boundary('message handler must return its real layout carriers')
    return result.validate(state)


def dispatch_highbank_command_state(state: SceneState, layout: MessageLayout) -> MessageLayout:
    """Legacy observations project the sole fields; missing A7/CCR/high fields stay unknown."""
    entered=_highbank_message_observation_fields(state,layout)
    returned=dispatch_highbank_command_state_fields(state,entered)
    return _highbank_message_projection(state,returned)


def lookup_message_layout_words(state: SceneState, layout: MessageLayout) -> MessageLayout:
    """Legacy observations project the sole fields; missing A7/CCR/high fields stay unknown."""
    entered=_highbank_message_observation_fields(state,layout)
    returned=lookup_message_layout_words_fields(state,entered)
    return _highbank_message_projection(state,returned)


def lookup_message_fill_pattern(state: SceneState, layout: MessageLayout) -> MessageLayout:
    """Legacy observations project the sole fields; missing A7/CCR/high fields stay unknown."""
    entered=_highbank_message_observation_fields(state,layout)
    returned=lookup_message_fill_pattern_fields(state,entered)
    return _highbank_message_projection(state,returned)


def append_scrolling_message_header(state: SceneState, layout: MessageLayout) -> MessageLayout:
    """Legacy observations project the sole fields; missing A7/CCR/high fields stay unknown."""
    entered=_highbank_message_observation_fields(state,layout)
    returned=append_scrolling_message_header_fields(state,entered)
    return _highbank_message_projection(state,returned)


def append_scrolling_message_glyph(state: SceneState, layout: MessageLayout) -> MessageLayout:
    """Legacy observations project the sole fields; missing A7/CCR/high fields stay unknown."""
    entered=_highbank_message_observation_fields(state,layout)
    returned=append_scrolling_message_glyph_fields(state,entered)
    return _highbank_message_projection(state,returned)


def append_scrolling_message_bitmap(state: SceneState, layout: MessageLayout) -> MessageLayout:
    """Legacy observations project the sole fields; missing A7/CCR/high fields stay unknown."""
    entered=_highbank_message_observation_fields(state,layout)
    returned=append_scrolling_message_bitmap_fields(state,entered)
    return _highbank_message_projection(state,returned)


def _advance_scrolling_message_core(state: SceneState, layout: MessageLayout | None) -> ScrollingMessageAdvance:
    """State-only non-due timing remains available; due text needs the real full ABI."""
    checked_state(state)
    entered=FirstDeploymentFrame.unobserved() if layout is None else _highbank_message_observation_fields(state,layout)
    returned,timer=_highbank_scroll_timer_fields(state,entered)
    if timer:
        return ScrollingMessageAdvance(layout,timer)
    returned=_highbank_due_message_fields(state,returned)
    return ScrollingMessageAdvance(_highbank_message_projection(state,returned),timer)



def advance_scrolling_message(state: SceneState, layout: MessageLayout) -> MessageLayout:
    """Legacy observations project the sole fields; missing A7/CCR/high fields stay unknown."""
    entered=_highbank_message_observation_fields(state,layout)
    returned=advance_scrolling_message_fields(state,entered)
    return _highbank_message_projection(state,returned)



def lookup_message_decoration_style(state: SceneState, layout: MessageLayout) -> MessageLayout:
    """Legacy observations project the sole fields; missing A7/CCR/high fields stay unknown."""
    entered=_highbank_message_observation_fields(state,layout)
    returned=lookup_message_decoration_style_fields(state,entered)
    return _highbank_message_projection(state,returned)


def advance_message_decoration_stage(state: SceneState, layout: MessageLayout) -> MessageLayout:
    """Legacy observations project the sole fields; missing A7/CCR/high fields stay unknown."""
    entered=_highbank_message_observation_fields(state,layout)
    returned=advance_message_decoration_stage_fields(state,entered)
    return _highbank_message_projection(state,returned)


def dispatch_message_control(state: SceneState, layout: MessageLayout, *, entry_frame: FirstDeploymentFrame | None=None) -> MessageLayout:
    """Legacy layout result is only a projection of the sole complete control."""
    checked_context(layout, MessageLayout, state)
    if entry_frame is None:
        raise Boundary('676C4 legacy layout is missing actual full address registers and A7/CCR-X')
    returned = dispatch_message_control_frame_fields(state, entry_frame)
    return _highbank_message_projection(state, returned)



def dispatch_message_control_fields(state: SceneState, layout: MessageLayout | None=None, *, entry_frame: FirstDeploymentFrame | None=None) -> MessageControlFields:
    """Historical WORD observations project the same full transaction.

    MessageLayout does not contain A7, all address registers or full CCR/X.
    Missing physical inputs are a real boundary and are never reconstructed.
    """
    checked_state(state)
    if layout is not None:
        checked_context(layout, MessageLayout, state)
    if entry_frame is None:
        raise Boundary('676C4 control requires its actual complete D/A/SR-X/SP entry frame')
    returned, preparation = _message_control_transaction_fields(state, entry_frame)
    current = None if layout is None else _highbank_message_projection(state, returned)
    if preparation.resolved is None:
        field = destination = source = tile = None
    else:
        field = preparation.resolved.item_offset
        destination = state.table_at(preparation.resolved.pointer).cursor()
        source = state.table_at(preparation.resolved.descriptor).cursor()
        tile = low16(returned.unit)
    status = returned.status
    return MessageControlFields(low16(returned.target_x), field, destination, source, current, bool(status & 1), bool(status & 4), bool(status & 8), bool(status & 2), tile).validate(state)


def render_force_city_markers(state: SceneState, layout: MessageLayout, *, entry_frame: FirstDeploymentFrame | None=None) -> MessageLayout:
    """Legacy layout is an explicit projection of one complete marker transaction."""
    checked_context(layout, MessageLayout, state)
    fields = RenderFields(layout.symbol, layout.position, layout.stride, layout.row_offset, layout.first_plane, layout.fill, layout.shift_count, layout.second_plane, layout.bitmap, layout.destination, layout.previous_rows, None, None, None, None, None)
    result = _force_render_fields(state, fields, entry_frame=entry_frame)
    return replace(layout, symbol=result.x, position=result.y, stride=result.attributes)



def _force_render_fields(state: SceneState, fields: RenderFields, *, entry_frame: FirstDeploymentFrame | None=None) -> RenderFields:
    """Project the one full marker algorithm after checking actual observations."""
    actual = _force_render_entry_fields(state, fields, entry_frame)
    returned = render_force_city_markers_fields(state, actual)
    return RenderFields(returned.target_x, returned.target_y, returned.unit, returned.count, returned.distance, returned.offset_x, returned.offset_y, returned.choice, returned.roster, returned.candidates, returned.controller, bool(returned.status & 1), bool(returned.status & 4), bool(returned.status & 8), bool(returned.status & 2), returned.stack_cursor)


def render_force_city_markers_complete(state: SceneState, frame: MapTickFrame, *, entry_frame: FirstDeploymentFrame | None=None) -> MapTickFrame:
    """Legacy map observations do not establish missing CCR-X/address carriers.

    An independent full entry is mandatory. The compatibility fields retain
    their existing controller/auxiliary observations; they are never used to
    manufacture a complete FirstDeploymentFrame or redefine its A-registers.
    """
    from .business_gameplay import _render_from_tick
    checked_tick_frame(frame, state)
    if entry_frame is None:
        raise Boundary('679FC MapTick projection requires independently supplied complete entry_frame')
    actual = _force_render_entry_fields(state, _render_from_tick(state, frame), entry_frame)
    if frame.vdp_port.base != actual.auxiliary.base:
        raise ValueError('679FC MapTick A6 observation contradicts actual entry')
    returned = render_force_city_markers_fields(state, actual)
    return replace(frame, motion_x=returned.target_x, motion_y=returned.target_y, attributes=returned.unit, tile_count=returned.count, officer=returned.distance, count=returned.offset_x, index=returned.offset_y, control_latch=returned.choice, source=returned.roster, destination=returned.candidates, packet=returned.controller, vdp_port=returned.auxiliary, stack_cursor=returned.stack_cursor, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def _force_render_entry_fields(state: SceneState, fields: RenderFields, entry_frame: FirstDeploymentFrame | None) -> FirstDeploymentFrame:
    """Historical observations never supply missing X/address carriers or SP.

    Given a real full entry, verify its observed subset before invoking the
    sole algorithm. Return only this interface's observation projection.
    """
    checked_render_fields(fields, state)
    if entry_frame is None:
        raise Boundary('679FC render observations require actual complete16 carriers/CCR-X/SP')
    frame = _highbank_frame_fields(state, entry_frame, 424444)
    if (fields.x, fields.y, fields.attributes, fields.tile, fields.officer, fields.count, fields.index, fields.remaining) != (frame.target_x, frame.target_y, frame.unit, frame.count, frame.distance, frame.offset_x, frame.offset_y, frame.choice):
        raise ValueError('679FC legacy numeric observations contradict actual entry')
    for observed, actual in ((fields.source, frame.roster), (fields.destination, frame.candidates), (fields.packet, frame.controller), (fields.stack_cursor, frame.stack_cursor)):
        if observed is not None and observed.base != actual.base:
            raise ValueError('679FC legacy address observation contradicts actual entry')
    for observed, mask in ((fields.carry, 1), (fields.zero, 4), (fields.negative, 8), (fields.overflow, 2)):
        if observed is not None and observed != bool(frame.status & mask):
            raise ValueError('679FC legacy condition observation contradicts actual entry')
    return frame

def render_force_city_markers_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """One complete679FC marker transaction on the supplied16 carriers/SR/SP.

    Forty city ownership bytes select animated sprite resources. Real MOVEM
    D0 saves bracket each city and resource lookup; the two existing complete
    children own their algorithms, while this caller owns their actual JSR
    tokens. Untouched carriers and original width/CCR-X effects survive.
    """
    frame = _highbank_frame_fields(state, frame, 424444)
    frame = _movement_compare(state, frame, state.read(4294964754, 2), 512, 16)
    if frame.status & 4:
        frame = _movement_compare(state, frame, state.read(4294964050, 2), 16, 16)
        if frame.status & 5:
            return frame
    frame = _movement_test(state, frame, state.read(4294963144, 2), 16)
    if frame.status & 4:
        state.set_status_word(9984)
        frame = first_replace(frame, status=0, roster=state.table_at(425104).cursor())
        frame = _movement_move(state, frame, 'target_x', 8192, 16)
        frame = _highbank_child_fields(state, frame, 240466, 424492)
        state.set_status_word(9472)
        frame = first_replace(frame, status=0)
        frame = _highbank_write_fields(state, frame, 4294963144, 1)
    frame = _movement_compare(state, frame, state.read(4294964050, 2), 32, 16)
    for offset, color in ((0, 0), (2, 3648), (4, 2798), (6, 2574), (8, 736), (10, 206), (12, 3744), (14, 0)):
        frame = _highbank_write_fields(state, frame, 4294966096 + offset, color)
    frame = _movement_move_long(state, frame, 'target_x', 0)
    while True:
        frame = _movement_save_longs(state, frame, ('target_x',))
        frame = _movement_move_long(state, frame, 'target_y', 0)
        frame = first_replace(frame, roster=state.table_at(4294964264).cursor())
        frame = _movement_move(state, frame, 'target_y', frame.roster.byte(s16(low16(frame.target_x))), 8)
        frame = _movement_compare(state, frame, low8(frame.target_y), 255, 8)
        if not frame.status & 4:
            frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
            frame = _movement_save_longs(state, frame, ('target_x',))
            frame = _movement_move(state, frame, 'target_x', state.read(4294964000, 2), 16)
            frame = _movement_fixed_shift_word(state, frame, 'target_x', 3, True)
            frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 1, 16)
            frame = _movement_add_word(state, frame, 'target_y', low16(frame.target_x))
            frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
            frame = first_replace(frame, candidates=state.table_at(424720).cursor())
            pointer = frame.candidates.long(s16(low16(frame.target_y)))
            frame = first_replace(frame, roster=state.table_at(pointer).cursor())
            frame = _movement_restore_longs(state, frame, ('target_x',))
            frame = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)
            frame = _movement_fixed_shift_word(state, frame, 'unit', 2)
            frame = first_replace(frame, candidates=state.table_at(871114).cursor())
            frame = _movement_move(state, frame, 'target_x', frame.candidates.word(s16(low16(frame.unit)), 2), 16)
            frame, value = _movement_binary_flags(state, frame, low16(frame.target_x), 16, 16, True)
            frame = first_replace(frame, target_x=replace_word(frame.target_x, value))
            frame = _movement_move(state, frame, 'target_y', frame.candidates.word(s16(low16(frame.unit))), 16)
            frame = _movement_move(state, frame, 'unit', 0, 16)
            frame = _highbank_write_fields(state, frame, 4294964746, state.read(4294963988, 2))
            frame = _highbank_write_fields(state, frame, 4294964750, state.read(4294963992, 2))
            frame = _highbank_child_fields(state, frame, 44048, 424706)
        frame = _movement_restore_longs(state, frame, ('target_x',))
        frame = _movement_add_word(state, frame, 'target_x', 1)
        frame = _movement_compare(state, frame, low16(frame.target_x), 40, 16)
        if not frame.status & 1:
            return frame


# Unique complete Scene officer-growth fields; old observation interfaces project this same core.
from .contexts_gameplay import FirstDeploymentFrame, first_replace, MovementContinuationBoundary
from .business_movement_support import (_movement_move, _movement_move_long,
    _movement_test, _movement_fixed_shift_word, _movement_add_word,
    _movement_binary_flags, _movement_compare, _movement_arithmetic_long)


def _growth_carry_fields(state: SceneState, frame: FirstDeploymentFrame,
        requested: bool) -> FirstDeploymentFrame:
    """Original SR OR/AND changes C alone; X and every other real condition survive."""
    status = (frame.status & 30) | (1 if requested else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, status=status)


def _growth_project_values_fields(values: GrowthValues, attribute_pointer=None,
        owner_pointer=None) -> FirstDeploymentFrame:
    """Historical observations are not a physical frame; no X, address or SP is invented."""
    return first_replace(FirstDeploymentFrame.unobserved(), target_x=values.selected,
        target_y=values.value, unit=values.category, opponent=attribute_pointer,
        scratch=owner_pointer)


def _growth_ratio_attribute_fields(state: SceneState, frame: FirstDeploymentFrame,
        first: bool) -> FirstDeploymentFrame:
    """One original weighted-ratio rule, preserving its two actual attribute layouts."""
    from ..high_level_remaining_flows.business_city import _resource_cost_frame, _settlement_store_word_fields
    if type(first) is not bool:
        raise ValueError('closed growth attribute role required')
    frame = _resource_cost_frame(state, frame, 0x66370 if first else 0x663A2)
    frame = first_replace(frame, opponent=state.table_at(0xFFFFB400 if first else 0xFFFFB600))
    numerator = frame.roster if first else frame.candidates
    other = frame.candidates if first else frame.roster
    frame = _movement_move(state, frame, 'target_y', numerator.word(low16(frame.target_x)), 16)
    frame = _movement_move(state, frame, 'unit', low16(frame.target_y), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
    frame = _movement_add_word(state, frame, 'target_y', low16(frame.unit))
    frame = _movement_add_word(state, frame, 'unit', other.word(low16(frame.target_x)))
    frame = _movement_move_long(state, frame, 'target_y', frame.target_y & 65535)
    if low16(frame.unit) == 0:
        raise MovementContinuationBoundary(0x66388 if first else 0x663BA, frame,
            'original DIVU requires its actual divide-by-zero exception frame')
    # Unique retained DIVU arithmetic; its undefined overflow NZV are unobserved
    # and immediately replaced by the following MOVE.W, never supplied as flags.
    frame = first_replace(frame, target_y=divu_retained(frame.target_y, low16(frame.unit)))
    frame = _movement_move(state, frame, 'unit', frame.opponent.word(low16(frame.target_x)), 16)
    frame = _movement_add_word(state, frame, 'unit', low16(frame.target_y))
    frame = _movement_compare(state, frame, low16(frame.unit), 255, 16)
    if not frame.status & 5:
        frame = _movement_move(state, frame, 'unit', 255, 16)
    return _settlement_store_word_fields(state, frame, frame.opponent, low16(frame.target_x), low16(frame.unit))


def increase_growth_first_attribute_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """66370..663A2: sole strength-weighted growth phase."""
    return _growth_ratio_attribute_fields(state, frame, True)


def increase_growth_second_attribute_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """663A2..663D4: sole intellect-weighted growth phase."""
    return _growth_ratio_attribute_fields(state, frame, False)


def _growth_saved_index_random_fields(state: SceneState, frame: FirstDeploymentFrame,
        continuation: int) -> FirstDeploymentFrame:
    """Two true WORD saves around the same accepted RNG; caller child LONG remains below them."""
    if continuation not in (0x663DC, 0x66426):
        raise ValueError('closed growth random continuation required')
    from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
    from ..high_level_battle_ai.business_actions import sample_battle_action_random_fields
    stack = frame.stack_cursor.advance(-2)
    stack.set_word(0, low16(frame.target_x))
    frame = _movement_test(state, first_replace(frame, stack_cursor=stack), low16(frame.target_x), 16)
    return sample_battle_action_random_fields(BattlePolicyMemory(state), frame, continuation)


def increase_growth_random_attribute_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """663D4..6640E: original random third attribute with physical saved WORD and saturation."""
    from ..high_level_remaining_flows.business_city import _resource_cost_frame, _settlement_store_word_fields, _special_action_shift_long
    frame = _resource_cost_frame(state, frame, 0x663D4)
    frame = _growth_saved_index_random_fields(state, frame, 0x663DC)
    frame = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)
    frame = _movement_move_long(state, frame, 'target_y', frame.target_x)
    frame = _special_action_shift_long(state, frame, 'target_y', 1)
    frame = _movement_arithmetic_long(state, frame, 'target_y', frame.target_x)
    frame = _movement_move_long(state, frame, 'target_y', swap_words(frame.target_y))
    restored = frame.stack_cursor.word()
    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
    frame = _movement_move(state, frame, 'target_x', restored, 16)
    frame = _movement_move(state, frame, 'unit', low16(frame.target_y), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
    frame = _movement_add_word(state, frame, 'target_y', low16(frame.unit))
    frame = first_replace(frame, opponent=state.table_at(0xFFFFB800))
    frame = _movement_move(state, frame, 'unit', frame.opponent.word(low16(frame.target_x)), 16)
    frame = _movement_add_word(state, frame, 'unit', low16(frame.target_y))
    frame = _movement_compare(state, frame, low16(frame.unit), 150, 16)
    if not frame.status & 5:
        frame = _movement_move(state, frame, 'unit', 150, 16)
    return _settlement_store_word_fields(state, frame, frame.opponent, low16(frame.target_x), low16(frame.unit))


def increase_growth_command_radius_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6640E..6643A: command radius cap and RNG bit4, without any fake draw."""
    from ..high_level_remaining_flows.business_city import _resource_cost_frame, _settlement_change_header_byte_fields
    frame = _resource_cost_frame(state, frame, 0x6640E)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1, True)
    frame = first_replace(frame, opponent=state.table_at(0xFFFFC400))
    frame = _movement_compare(state, frame, frame.opponent.byte(low16(frame.target_x)), 20, 8)
    if not frame.status & 1:
        return frame
    frame = _growth_saved_index_random_fields(state, frame, 0x66426)
    restored = frame.stack_cursor.word()
    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
    frame = _movement_move(state, frame, 'target_x', restored, 16)
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF61C, 2), 16)
    from ..high_level_gameplay_flow.business_battle import _postbattle_bit_fields
    frame = _postbattle_bit_fields(frame, bool(frame.target_y & 16))
    state.sr = (state.sr & 65504) | frame.status
    if not frame.status & 4:
        frame = _settlement_change_header_byte_fields(state, frame, frame.opponent.at(low16(frame.target_x)), False)
    return frame


def check_growth_notification_owner_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6643A..66478: original assignment/ruler scan, negative assignment suppresses carry."""
    from ..high_level_remaining_flows.business_city import _resource_cost_frame
    frame = _resource_cost_frame(state, frame, 0x6643A)
    frame = first_replace(frame, opponent=state.table_at(0xFFFFCC00), scratch=state.table_at(0xFFFFF427))
    frame = _movement_move(state, frame, 'target_y', frame.opponent.byte(low16(frame.target_x)), 8)
    if frame.status & 8:
        return _growth_carry_fields(state, frame, False)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 63, 16)
    frame = _movement_move(state, frame, 'target_y', frame.scratch.byte(low16(frame.target_y)), 8)
    for address in (0xFFFFF67B, 0xFFFFF67D, 0xFFFFF67F):
        frame = _movement_compare(state, frame, low8(frame.target_y), state.read(address, 1), 8)
        if frame.status & 4:
            return _growth_carry_fields(state, frame, True)
    return _growth_carry_fields(state, frame, False)


def advance_officer_growth_levels_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """662E4..66370: the unique complete live growth scan, not an input/IRQ wait service."""
    from ..high_level_remaining_flows.business_city import (_resource_cost_frame,
        _duel_menu_write_word_fields, _settlement_change_header_byte_fields, _deployment_menu_call_fields)
    frame = _resource_cost_frame(state, frame, 0x662E4)
    frame = first_replace(frame, roster=state.table_at(0xFFFFC000).cursor(),
        candidates=state.table_at(0xFFFFBE00).cursor(), controller=state.table_at(0xFFFFC600),
        scan=state.table_at(0x66478).cursor(), auxiliary=state.table_at(0xFFFFCC00))
    frame = _duel_menu_write_word_fields(state, frame, 0xFFFFEF78, 0, True)
    while True:
        frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFEF78, 2), 16)
        frame = _movement_compare(state, frame, low16(frame.target_x), 256, 16)
        if not frame.status & 1:
            frame = _duel_menu_write_word_fields(state, frame, 0xFFFFCFCC, 1)
            return _growth_carry_fields(state, frame, False)
        frame = _movement_compare(state, frame, frame.auxiliary.byte(low16(frame.target_x)), 255, 8)
        assigned = not bool(frame.status & 4)
        if assigned:
            frame = _movement_move(state, frame, 'unit', 0, 16)
            frame = _movement_move(state, frame, 'unit', frame.controller.byte(low16(frame.target_x)), 8)
            frame = _movement_fixed_shift_word(state, frame, 'unit', 1)
            frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
            frame = _movement_move(state, frame, 'target_y', frame.roster.word(low16(frame.target_x)), 16)
            frame = _movement_add_word(state, frame, 'target_y', frame.candidates.word(low16(frame.target_x)))
            frame = _movement_compare(state, frame, low16(frame.target_y), frame.scan.word(low16(frame.unit)), 16)
            if not frame.status & 1:
                frame = _deployment_menu_call_fields(state, frame, 0x66370, 0x66338)
                frame = _deployment_menu_call_fields(state, frame, 0x663A2, 0x6633C)
                frame = _deployment_menu_call_fields(state, frame, 0x663D4, 0x66340)
                frame = _deployment_menu_call_fields(state, frame, 0x6640E, 0x66344)
                frame = _settlement_change_header_byte_fields(state, frame, frame.controller.at(low16(frame.target_x)), False)
                frame = _deployment_menu_call_fields(state, frame, 0x6643A, 0x6634C)
                if not frame.status & 1:
                    # Owner notification did not fire: the same EF78 officer is rescanned.
                    continue
                frame = _duel_menu_write_word_fields(state, frame, 0xFFFFF3D0, low16(frame.target_x))
                frame = _movement_move_long(state, frame, 'target_y', 0)
                frame = _movement_move(state, frame, 'target_y', frame.controller.byte(low16(frame.target_x)), 8)
                state.write(0xFFFFF3C8, 4, frame.target_y)
                from .business_movement_support import _movement_test_long
                frame = _movement_test_long(state, frame, frame.target_y)
                return _growth_carry_fields(state, frame, True)
        old = state.read(0xFFFFEF78, 2)
        frame, advanced = _movement_binary_flags(state, frame, old, 1, 16)
        state.write(0xFFFFEF78, 2, advanced)


"""Officer selection, live command budget and scrolling text: one full ABI core."""

def _highbank_frame_fields(state: SceneState, frame: FirstDeploymentFrame, entry: int) -> FirstDeploymentFrame:
    from ..high_level_remaining_flows.business_city import _resource_cost_frame
    return _resource_cost_frame(state, frame, entry)


def _highbank_write_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, value, size: int = 2, clear: bool = False) -> FirstDeploymentFrame:
    """MOVE/CLR memory, including the original CLR's physical prior read."""
    if size not in (1, 2, 4) or type(clear) is not bool:
        raise ValueError('actual Highbank memory width required')
    if clear:
        state.read(address, size)
    state.write(address, size, value)
    if size == 4:
        return _movement_test_long(state, frame, value)
    return _movement_test(state, frame, value, size * 8)


def _highbank_memory_add_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, amount: int, size: int = 2) -> tuple:
    old = state.read(address, size)
    observed = frame.status
    working = frame if observed is not None else first_replace(frame, status=state.sr & 31)
    working, value = _movement_binary_flags(state, working, old, abs(amount), size * 8, amount < 0)
    state.write(address, size, value)
    return (working if observed is not None else first_replace(working, status=None)), value


def _highbank_shift_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, count: int) -> FirstDeploymentFrame:
    from ..high_level_remaining_flows.business_highbank import _position_order_shift
    frame = _position_order_shift(frame, name, count)
    state.sr = (state.sr & 65504) | frame.status
    return frame


def _highbank_dbra_fields(frame: FirstDeploymentFrame, name: str) -> FirstDeploymentFrame:
    return first_replace(frame, **{name: replace_word(frame.carrier(name), u16(low16(frame.carrier(name)) - 1))})


def _highbank_child_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """One actual child LONG; no new slot for a direct tail/JMP entry."""
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    result = _highbank_target_fields(state, entered, target)
    actual = result.stack_cursor.long()
    if actual != continuation:
        raise FirstDeploymentReturnBoundary(actual, result, continuation)
    return first_replace(result, stack_cursor=result.stack_cursor.advance(4))


def _highbank_target_fields(state: SceneState, frame: FirstDeploymentFrame, target: int) -> FirstDeploymentFrame:
    if target == 423858:
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_178_fields
        return highbank_coordinate_live_state_178_fields(state, frame)
    if target == 423940:
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_179_fields
        return highbank_coordinate_live_state_179_fields(state, frame)
    if target == 423960:
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_180_fields
        return highbank_coordinate_live_state_180_fields(state, frame)
    if target == 424024:
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_178_alternate_1_fields
        return highbank_coordinate_live_state_178_alternate_1_fields(state, frame)
    if target == 424062:
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_178_alternate_2_fields
        return highbank_coordinate_live_state_178_alternate_2_fields(state, frame)
    if target == 424098:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_18_fields
        return highbank_update_live_fields_18_fields(state, frame)
    if target == 424104:
        from ..high_level_remaining_flows.business_highbank import highbank_select_live_state_44_fields
        return highbank_select_live_state_44_fields(state, frame)
    if target == 424120:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_19_fields
        return highbank_update_live_fields_19_fields(state, frame)
    if target == 424126:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_20_fields
        return highbank_update_live_fields_20_fields(state, frame)
    if target == 424132:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_21_fields
        return highbank_update_live_fields_21_fields(state, frame)
    if target == 424138:
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_181_fields
        return highbank_coordinate_live_state_181_fields(state, frame)
    if target == 424156:
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_182_fields
        return highbank_coordinate_live_state_182_fields(state, frame)
    if target == 424192:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_22_fields
        return highbank_update_live_fields_22_fields(state, frame)
    if target == 424198:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_23_fields
        return highbank_update_live_fields_23_fields(state, frame)
    if target == 424204:
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_183_fields
        return highbank_coordinate_live_state_183_fields(state, frame)
    if target == 424222:
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_178_alternate_3_fields
        return highbank_coordinate_live_state_178_alternate_3_fields(state, frame)
    if target == 424230:
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_178_alternate_4_fields
        return highbank_coordinate_live_state_178_alternate_4_fields(state, frame)
    if target == 424238:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_24_fields
        return highbank_update_live_fields_24_fields(state, frame)
    if target == 424244:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_25_fields
        return highbank_update_live_fields_25_fields(state, frame)
    if target == 424250:
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_178_alternate_5_fields
        return highbank_coordinate_live_state_178_alternate_5_fields(state, frame)
    if target == 424270:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_26_fields
        return highbank_update_live_fields_26_fields(state, frame)
    if target == 424276:
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_178_alternate_6_fields
        return highbank_coordinate_live_state_178_alternate_6_fields(state, frame)
    if target == 424284:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_27_fields
        return highbank_update_live_fields_27_fields(state, frame)
    if target == 424290:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_28_fields
        return highbank_update_live_fields_28_fields(state, frame)
    if target == 424296:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_29_fields
        return highbank_update_live_fields_29_fields(state, frame)
    if target == 424302:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_30_fields
        return highbank_update_live_fields_30_fields(state, frame)
    if target == 424308:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_31_fields
        return highbank_update_live_fields_31_fields(state, frame)
    if target == 424314:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_32_fields
        return highbank_update_live_fields_32_fields(state, frame)
    if target == 424320:
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_184_fields
        return highbank_coordinate_live_state_184_fields(state, frame)
    if target == 424376:
        from ..high_level_remaining_flows.business_highbank import highbank_coordinate_live_state_178_alternate_7_fields
        return highbank_coordinate_live_state_178_alternate_7_fields(state, frame)
    if target == 424384:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_33_fields
        return highbank_update_live_fields_33_fields(state, frame)
    if target == 424390:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_34_fields
        return highbank_update_live_fields_34_fields(state, frame)
    if target == 424396:
        from ..high_level_remaining_flows.business_highbank import highbank_update_live_fields_35_fields
        return highbank_update_live_fields_35_fields(state, frame)
    if target == 422492:
        from ..high_level_remaining_flows.business_highbank import toggle_scenario_choice_fields
        return toggle_scenario_choice_fields(state, frame)
    if target == 422504:
        from ..high_level_remaining_flows.business_highbank import compose_scenario_numeric_text_fields
        return compose_scenario_numeric_text_fields(state, frame)
    if target == 422556:
        from ..high_level_remaining_flows.business_highbank import compose_scenario_numeric_text_fields_entry_6729c
        return compose_scenario_numeric_text_fields_entry_6729c(state, frame)
    if target == 422562:
        from ..high_level_remaining_flows.business_highbank import compose_scenario_member_name_fields
        return compose_scenario_member_name_fields(state, frame)
    if target == 422630:
        from ..high_level_remaining_flows.business_highbank import compose_scenario_member_name_fields_entry_672e6
        return compose_scenario_member_name_fields_entry_672e6(state, frame)
    if target == 422636:
        from ..high_level_remaining_flows.business_highbank import restore_scenario_previous_text_fields
        return restore_scenario_previous_text_fields(state, frame)
    if target == 422646:
        from ..high_level_remaining_flows.business_highbank import compose_scenario_member_name_fields_entry_672f6
        return compose_scenario_member_name_fields_entry_672f6(state, frame)
    if target == 422662:
        from ..high_level_remaining_flows.business_highbank import compose_scenario_status_pair_fields
        return compose_scenario_status_pair_fields(state, frame)
    if target == 422712:
        from ..high_level_remaining_flows.business_highbank import compose_scenario_numeric_text_fields_entry_67338
        return compose_scenario_numeric_text_fields_entry_67338(state, frame)
    if target == 422726:
        from ..high_level_remaining_flows.business_highbank import compose_scenario_numeric_text_fields_entry_67346
        return compose_scenario_numeric_text_fields_entry_67346(state, frame)
    if target == 422478:
        from ..high_level_remaining_flows.business_highbank import restore_scenario_saved_command_fields
        return restore_scenario_saved_command_fields(state, frame)
    if target == 423198:
        from ..high_level_remaining_flows.business_highbank import build_scenario_single_row_fields
        return build_scenario_single_row_fields(state, frame)
    if target == 423438:
        from ..high_level_remaining_flows.business_highbank import build_scenario_triple_columns_fields
        return build_scenario_triple_columns_fields(state, frame)
    if target == 423570:
        from ..high_level_remaining_flows.business_highbank import build_scenario_alternate_row_fields
        return build_scenario_alternate_row_fields(state, frame)
    if target == 420948:
        from ..high_level_remaining_flows.business_highbank import confirm_scenario_force_choice_fields
        return confirm_scenario_force_choice_fields(state, frame)
    if target == 423344:
        from ..high_level_remaining_flows.business_highbank import build_scenario_paired_columns_fields
        return build_scenario_paired_columns_fields(state, frame)
    if target == 419076:
        return sort_high_loyalty_officers_fields(state, frame)
    if target == 419196:
        return append_mid_loyalty_officers_by_trait_fields(state, frame)
    if target == 422740:
        return append_scrolling_message_header_fields(state, frame)
    if target == 422796:
        return append_scrolling_message_glyph_fields(state, frame)
    if target == 422822:
        return append_scrolling_message_bitmap_fields(state, frame)
    if target == 423018:
        return lookup_message_layout_words_fields(state, frame)
    if target == 423054:
        return lookup_message_fill_pattern_fields(state, frame)
    if target == 423178:
        return lookup_message_decoration_style_fields(state, frame)
    if target == 44804:
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        from ..high_level_scene_flows.business_scene import expand_glyph_row_fields
        return expand_glyph_row_fields(SceneRefreshMemory(state), frame)
    if target == 41304:
        from .business_map import refresh_world_cursor_attributes_alternate_1_frame_fields
        return refresh_world_cursor_attributes_alternate_1_frame_fields(state, frame)
    if target == 55532:
        from .business_commands import append_current_command_description_frame_fields
        return append_current_command_description_frame_fields(state, frame)
    if target == 240466:
        from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
        from ..high_level_scene_flows.business_scene import write_vdp_swapped_byte_rle_stream_fields
        return write_vdp_swapped_byte_rle_stream_fields(SceneRefreshMemory(state), frame)
    if target == 44048:
        from ..high_level_player_commands.contexts_display import SpritePacketMemory
        from ..high_level_player_commands.business_display import append_live_command_sprite_fields
        return append_live_command_sprite_fields(SpritePacketMemory(state), frame, reset_scroll=False, initialize_clip=True)
    raise MovementContinuationBoundary(target, frame, 'actual Highbank child has no admitted full-field return')


def sort_high_loyalty_officers_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """66504: stable descending loyalty insertion, parallel names/scores."""
    frame = _highbank_frame_fields(state, frame, 0x66504)
    frame = first_replace(frame, controller=state.table_at(0xFFFFCC00),
        scan=state.table_at(0xFFFFC300).cursor(), opponent=state.table_at(0xFFFFF427))
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFEFB0, 2), 16)
    frame = _movement_move(state, frame, 'unit', 255, 16)
    frame = _highbank_write_fields(state, frame, 0xFFFFF100, 65535)
    while True:
        frame = _movement_move(state, frame, 'count', frame.controller.byte(low16(frame.unit)), 8)
        eligible = not bool(frame.status & 12)
        if eligible:
            frame = _movement_move(state, frame, 'count', low16(frame.count) & 63, 16)
            frame = _movement_compare(state, frame, low8(frame.target_y), frame.opponent.byte(low16(frame.count)), 8)
            eligible = bool(frame.status & 4)
        if eligible:
            frame = _movement_compare(state, frame, frame.scan.byte(low16(frame.unit)), 90, 8)
            eligible = not bool(frame.status & 1)
        if eligible:
            frame = _movement_move(state, frame, 'count', 0, 16)
            frame = _movement_move(state, frame, 'count', frame.scan.byte(low16(frame.unit)), 8)
            frame = first_replace(frame, roster=state.table_at(0xFFFFF100).cursor(), candidates=state.table_at(0xFFFFF200).cursor())
            frame = _movement_move(state, frame, 'distance', low16(frame.unit), 16)
            while True:
                frame = _movement_test(state, frame, frame.roster.word(), 16)
                if frame.status & 8:
                    break
                frame = _movement_compare(state, frame, low16(frame.count), frame.candidates.word(), 16)
                if not frame.status & 5:
                    break
                frame = first_replace(frame, roster=frame.roster.advance(2), candidates=frame.candidates.advance(2))
            while True:
                frame = _movement_move(state, frame, 'offset_y', frame.candidates.word(), 16)
                frame = _highbank_write_fields(state, frame, frame.candidates.base, low16(frame.count))
                frame = first_replace(frame, candidates=frame.candidates.advance(2))
                frame = _movement_move(state, frame, 'count', low16(frame.offset_y), 16)
                frame = _movement_move(state, frame, 'offset_x', frame.roster.word(), 16)
                frame = _highbank_write_fields(state, frame, frame.roster.base, low16(frame.distance))
                frame = first_replace(frame, roster=frame.roster.advance(2))
                frame = _movement_move(state, frame, 'distance', low16(frame.offset_x), 16)
                if frame.status & 8:
                    break
            frame = _highbank_write_fields(state, frame, frame.roster.base, 65535)
            frame = _movement_add_word(state, frame, 'target_x', 1)
        frame = _highbank_dbra_fields(frame, 'unit')
        if low16(frame.unit) == 65535:
            return frame


def append_mid_loyalty_officers_by_trait_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6657C: append this requested trait without disturbing high-loyalty order."""
    frame = _highbank_frame_fields(state, frame, 0x6657C)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF100).cursor())
    while True:
        value = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_test(state, frame, value, 16)
        if frame.status & 8:
            break
    frame = first_replace(frame, roster=frame.roster.advance(-2),
        candidates=state.table_at(0xFFFFCC00).cursor(), controller=state.table_at(0xFFFFF427),
        scan=state.table_at(0xFFFFC300).cursor(), opponent=state.table_at(0xFFFFC700))
    frame = _movement_move(state, frame, 'target_y', 255, 16)
    frame = _movement_move(state, frame, 'unit', state.read(0xFFFFEFB0, 2), 16)
    while True:
        frame = _movement_move(state, frame, 'count', frame.candidates.byte(low16(frame.target_y)), 8)
        eligible = not bool(frame.status & 12)
        if eligible:
            frame = _movement_move(state, frame, 'count', low16(frame.count) & 63, 16)
            frame = _movement_compare(state, frame, low8(frame.unit), frame.controller.byte(low16(frame.count)), 8)
            eligible = bool(frame.status & 4)
        if eligible:
            frame = _movement_compare(state, frame, frame.scan.byte(low16(frame.target_y)), 80, 8)
            eligible = not bool(frame.status & 1)
        if eligible:
            frame = _movement_compare(state, frame, frame.scan.byte(low16(frame.target_y)), 90, 8)
            eligible = bool(frame.status & 1)
        if eligible:
            frame = _movement_move(state, frame, 'count', frame.opponent.byte(low16(frame.target_y)), 8)
            frame = _movement_move(state, frame, 'count', low16(frame.count) & 7, 16)
            frame = _movement_compare(state, frame, low8(frame.count), low8(frame.distance), 8)
            eligible = bool(frame.status & 4)
        if eligible:
            frame = _highbank_write_fields(state, frame, frame.roster.base, low16(frame.target_y))
            frame = first_replace(frame, roster=frame.roster.advance(2))
            frame = _movement_add_word(state, frame, 'target_x', 1)
        frame = _highbank_dbra_fields(frame, 'target_y')
        if low16(frame.target_y) == 65535:
            return _highbank_write_fields(state, frame, frame.roster.base, 65535)


def build_ten_officer_selection_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """664AC: rank, fill trait classes 4/3/2, then publish at most ten names."""
    frame = _highbank_frame_fields(state, frame, 0x664AC)
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _highbank_child_fields(state, frame, 0x66504, 0x664B2)
    for trait, continuation in ((4, 0x664C2), (3, 0x664D2), (2, 0x664E2)):
        frame = _movement_compare(state, frame, low16(frame.target_x), 10, 16)
        if not frame.status & 1:
            break
        frame = _movement_move(state, frame, 'distance', trait, 16)
        frame = _highbank_child_fields(state, frame, 0x6657C, continuation)
    frame = first_replace(frame, roster=state.table_at(0xFFFFF100).cursor(), candidates=state.table_at(0xFFFFF500).cursor())
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    while True:
        value = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _highbank_write_fields(state, frame, frame.candidates.base, value)
        frame = first_replace(frame, candidates=frame.candidates.advance(2))
        if frame.status & 8:
            break
        frame = _movement_add_word(state, frame, 'target_x', 1)
        frame = _movement_compare(state, frame, low16(frame.target_x), 10, 16)
        if not frame.status & 1:
            break
    frame = _highbank_write_fields(state, frame, frame.candidates.base, 65535)
    return _highbank_write_fields(state, frame, 0xFFFFF636, low16(frame.target_x))


def select_highest_trait_officer_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """670B8: lexicographic trait/combined training rank; retain D7 if empty."""
    frame = _highbank_frame_fields(state, frame, 0x670B8)
    frame = first_replace(frame, roster=state.table_at(0xFFFFCC00).cursor(),
        candidates=state.table_at(0xFFFFC700).cursor(), controller=state.table_at(0xFFFFC300),
        scan=state.table_at(0xFFFFB400).cursor(), opponent=state.table_at(0xFFFFB600))
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_y', 0, 16)
    frame = _movement_move(state, frame, 'unit', 255, 16)
    while True:
        frame = _movement_move(state, frame, 'count', frame.roster.byte(low16(frame.unit)), 8)
        eligible = not bool(frame.status & 4)
        if eligible:
            frame = _movement_move(state, frame, 'count', low16(frame.count) & 192, 16)
            eligible = bool(frame.status & 4)
        if eligible:
            frame = _movement_move(state, frame, 'count', frame.candidates.byte(low16(frame.unit)), 8)
            frame = _movement_move(state, frame, 'count', low16(frame.count) & 7, 16)
            frame = _movement_compare(state, frame, low16(frame.count), low16(frame.target_x), 16)
            eligible = not bool(frame.status & 1)
        if eligible:
            if not frame.status & 4:
                frame = _movement_move(state, frame, 'target_y', 0, 16)
            frame = _movement_move(state, frame, 'target_x', low16(frame.count), 16)
            frame = _movement_move(state, frame, 'count', 0, 16)
            frame = _movement_move(state, frame, 'count', frame.controller.byte(low16(frame.unit)), 8)
            frame = _movement_move(state, frame, 'distance', low16(frame.unit), 16)
            frame = _highbank_shift_fields(state, frame, 'distance', 1)
            frame = _movement_add_word(state, frame, 'count', frame.scan.word(low16(frame.distance)))
            frame = _movement_add_word(state, frame, 'count', frame.opponent.word(low16(frame.distance)))
            frame = _movement_compare(state, frame, low16(frame.count), low16(frame.target_y), 16)
            if not frame.status & 5:
                frame = _movement_move(state, frame, 'target_y', low16(frame.count), 16)
                frame = _movement_move(state, frame, 'choice', low16(frame.unit), 16)
        frame = _highbank_dbra_fields(frame, 'unit')
        if low16(frame.unit) == 65535:
            break
    frame = _highbank_write_fields(state, frame, 0xFFFFF3A6, low16(frame.choice))
    return _highbank_write_fields(state, frame, 0xFFFFF376, state.read(0xFFFFF376, 2) & 255)


def calculate_force_command_budget_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """67126: city mean and original packet-derived loyalty ratio, unchanged."""
    frame = _highbank_frame_fields(state, frame, 0x67126)
    frame = first_replace(frame, roster=state.table_at(0xFFFFE320).cursor())
    frame = _movement_move(state, frame, 'target_x', 39, 16)
    frame = _movement_move_long(state, frame, 'target_y', 0)
    while True:
        value = frame.roster.long()
        frame = first_replace(frame, roster=frame.roster.advance(4))
        frame = _movement_arithmetic_long(state, frame, 'target_y', value)
        frame = _highbank_dbra_fields(frame, 'target_x')
        if low16(frame.target_x) == 65535:
            break
    frame = _movement_divu_word(state, frame, 'target_y', 40, 0x67136)
    frame = first_replace(frame, roster=state.table_at(0xFFFFC300).cursor(), candidates=state.table_at(0xFFFFCC00).cursor())
    frame = _movement_move(state, frame, 'target_x', 255, 16)
    frame = _movement_move_long(state, frame, 'unit', 0)
    frame = _movement_move(state, frame, 'count', 0, 16)
    frame = _movement_move(state, frame, 'distance', 0, 16)
    while True:
        frame = _movement_move(state, frame, 'distance', frame.candidates.byte(low16(frame.target_x)), 8)
        eligible = not bool(frame.status & 4)
        if eligible:
            frame = _movement_move(state, frame, 'distance', low16(frame.distance) & 192, 16)
            eligible = bool(frame.status & 4)
        if eligible:
            frame = _movement_move(state, frame, 'distance', frame.roster.byte(low16(frame.target_x)), 8)
            frame = _movement_add_word(state, frame, 'unit', low16(frame.distance))
            frame = _movement_add_word(state, frame, 'count', 1)
        frame = _highbank_dbra_fields(frame, 'target_x')
        if low16(frame.target_x) == 65535:
            break
    frame = first_replace(frame, candidates=state.table_at(0xFFFF9000).cursor())
    while True:
        frame = _movement_move(state, frame, 'distance', frame.candidates.byte(), 8)
        frame = _movement_move(state, frame, 'distance', low16(frame.distance) & 15, 16)
        if frame.status & 4:
            break
        frame = _movement_move(state, frame, 'offset_x', frame.candidates.byte(0, 4), 8)
        frame = _movement_compare(state, frame, low8(frame.offset_x), state.read(0xFFFFF377, 1), 8)
        if frame.status & 4:
            frame, value = _movement_binary_flags(state, frame, low16(frame.distance), 1, 16, True)
            frame = first_replace(frame, distance=replace_word(frame.distance, value))
            while True:
                frame = _movement_move(state, frame, 'offset_x', frame.roster.byte(low16(frame.distance), 13), 8)
                frame = _movement_move(state, frame, 'offset_x', frame.candidates.byte(low16(frame.offset_x)), 8)
                frame = _movement_add_word(state, frame, 'unit', low16(frame.offset_x))
                frame = _movement_add_word(state, frame, 'count', 1)
                frame = _highbank_dbra_fields(frame, 'distance')
                if low16(frame.distance) == 65535:
                    break
        frame = _movement_move(state, frame, 'distance', frame.candidates.byte(), 8)
        frame = _movement_move(state, frame, 'distance', low16(frame.distance) & 15, 16)
        frame = first_replace(frame, candidates=frame.candidates.advance(13 + s16(low16(frame.distance))))
    frame = _movement_divu_word(state, frame, 'unit', low16(frame.count), 0x671A0)
    frame = _movement_add_word(state, frame, 'target_y', low16(frame.unit))
    frame = _movement_multiply_word(state, frame, 'target_y', low16(frame.count))
    frame = _movement_divu_word(state, frame, 'target_y', 280, 0x671A6)
    return _highbank_write_fields(state, frame, 0xFFFFEFDC, low16(frame.target_y))


def dispatch_highbank_command_state_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """66BF4: live signed WORD dispatch, followed by description/cursor refresh."""
    frame = _highbank_frame_fields(state, frame, 0x66BF4)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF362, 2), 16)
    frame = _highbank_shift_fields(state, frame, 'target_x', 1)
    frame = _movement_move(state, frame, 'target_x', state.table_at(0x66C10).word(low16(frame.target_x)), 16)
    frame = _highbank_child_fields(state, frame, u32(0x66C28 + s16(low16(frame.target_x))), 0x66C02)
    frame = _highbank_child_fields(state, frame, 0xD8EC, 0x66C08)
    return _highbank_child_fields(state, frame, 0xA158, 0x66C0E)


def lookup_message_layout_words_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6746A: MOVEM.W sign-extends both fields and does not change CCR."""
    frame = _highbank_frame_fields(state, frame, 0x6746A)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF6C4, 2), 16)
    frame = _highbank_shift_fields(state, frame, 'target_x', 2)
    frame = first_replace(frame, scan=state.table_at(0x6747E).cursor())
    offset = low16(frame.target_x)
    first = u32(s16(frame.scan.word(offset)))
    second = u32(s16(frame.scan.word(offset, 2)))
    return first_replace(frame, target_x=first, target_y=second)


def lookup_message_fill_pattern_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _highbank_frame_fields(state, frame, 0x6748E)
    frame = _movement_move(state, frame, 'offset_x', state.read(0xFFFFF6C4, 2), 16)
    frame = _highbank_shift_fields(state, frame, 'offset_x', 2)
    return _movement_move_long(state, frame, 'offset_x', state.table_at(0x6749A).long(low16(frame.offset_x)))


def lookup_message_decoration_style_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _highbank_frame_fields(state, frame, 0x6750A)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF6C4, 2), 16)
    frame = _highbank_shift_fields(state, frame, 'target_x', 1)
    return _movement_move(state, frame, 'unit', state.table_at(0x67516).word(low16(frame.target_x)), 16)


def append_scrolling_message_header_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _highbank_frame_fields(state, frame, 0x67354)
    frame = _movement_move(state, frame, 'target_y', 0x4060, 16)
    frame = _movement_test(state, frame, state.read(0xFFFFF37A, 2), 16)
    if not frame.status & 4:
        frame = _movement_move(state, frame, 'target_y', 0x4090, 16)
    frame = _highbank_write_fields(state, frame, frame.roster.base, low16(frame.target_y))
    frame = first_replace(frame, roster=frame.roster.advance(2))
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF37C, 2), 16)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 0xFFF8, 16)
    frame = _movement_move(state, frame, 'unit', low16(frame.target_y), 16)
    frame = _movement_add_word(state, frame, 'target_y', low16(frame.unit))
    frame = _movement_test(state, frame, state.read(0xFFFFF37A, 2), 16)
    if not frame.status & 4:
        frame = _movement_add_word(state, frame, 'target_y', low16(frame.unit))
    frame = _highbank_shift_fields(state, frame, 'target_y', 2)
    frame = _movement_add_word(state, frame, 'target_y', 0xA0A0)
    frame = _movement_test(state, frame, state.read(0xFFFFF37A, 2), 16)
    if not frame.status & 4:
        frame = _movement_add_word(state, frame, 'target_y', 0x900)
    frame = _highbank_write_fields(state, frame, frame.roster.base, low16(frame.target_y))
    return first_replace(frame, roster=frame.roster.advance(2))


def _highbank_roxr_plane_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str) -> FirstDeploymentFrame:
    """This text merger's one-bit LONG rotate-through-X, not an integer shift."""
    if name not in ('target_x', 'distance', 'choice', 'offset_x'):
        raise ValueError('actual scrolling plane rotation carrier required')
    original = frame.carrier(name)
    carried = bool(original & 1)
    rotated = (original >> 1) | (0x80000000 if frame.status & 16 else 0)
    status = (17 if carried else 0) | (8 if rotated & 0x80000000 else 0) | (4 if rotated == 0 else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, **{name: rotated}, status=status)


def append_scrolling_message_glyph_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _highbank_frame_fields(state, frame, 0x6738C)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 0xFF00, 16)
    frame = _highbank_shift_fields(state, frame, 'target_y', 3)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 255, 16)
    frame = _highbank_shift_fields(state, frame, 'target_x', 5)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) | low16(frame.target_y), 16)
    frame = first_replace(frame, controller=state.table_at(u32(0x8159C + s16(low16(frame.target_x)))))
    return append_scrolling_message_bitmap_fields(state, frame)


def append_scrolling_message_bitmap_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """673A6 shared entry: sixteen expanded rows, real X propagation, three planes."""
    frame = _highbank_frame_fields(state, frame, 0x673A6)
    frame = _movement_move(state, frame, 'unit', 64, 16)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFF516).cursor())
    frame = _movement_test(state, frame, state.read(0xFFFFF37A, 2), 16)
    if not frame.status & 4:
        frame = _movement_move(state, frame, 'unit', 96, 16)
        frame = _movement_move(state, frame, 'target_y', 3, 16)
        while True:
            frame = _highbank_child_fields(state, frame, 0x6748E, 0x673C0)
            for displacement in (192, 96, 0):
                frame = _highbank_write_fields(state, frame, u32(frame.roster.base + displacement), frame.offset_x, 4)
            frame = first_replace(frame, roster=frame.roster.advance(4))
            frame = _highbank_dbra_fields(frame, 'target_y')
            if low16(frame.target_y) == 65535:
                break
    frame = _movement_move(state, frame, 'count', low16(frame.unit), 16)
    frame = _highbank_shift_fields(state, frame, 'count', 1)
    frame, value = _highbank_memory_add_fields(state, frame, 0xFFFFF31A, low16(frame.count))
    frame, value = _highbank_memory_add_fields(state, frame, 0xFFFFF31A, low16(frame.unit))
    frame, value = _highbank_memory_add_fields(state, frame, 0xFFFFF31A, 4)
    frame = _movement_move_long(state, frame, 'unit', swap_words(frame.unit))
    frame = _movement_move_long(state, frame, 'count', swap_words(frame.count))
    frame = _movement_move(state, frame, 'unit', 15, 16)
    frame = _movement_move(state, frame, 'count', state.read(0xFFFFF37C, 2), 16)
    frame = _movement_move(state, frame, 'count', low16(frame.count) & 7, 16)
    while True:
        frame = _highbank_child_fields(state, frame, 0x6746A, 0x673F4)
        frame = _highbank_child_fields(state, frame, 0xAF04, 0x673FA)
        stack = frame.stack_cursor.advance(-4)
        frame = _highbank_write_fields(state, frame, stack.base, frame.choice, 4)
        frame = first_replace(frame, stack_cursor=stack)
        frame = _highbank_child_fields(state, frame, 0xAF04, 0x67402)
        saved = frame.stack_cursor.long()
        frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(4))
        frame = _movement_move_long(state, frame, 'distance', saved)
        frame = _highbank_child_fields(state, frame, 0x6748E, 0x67408)
        frame = _movement_move(state, frame, 'offset_y', low16(frame.count), 16)
        if not frame.status & 4:
            frame = _highbank_shift_fields(state, frame, 'offset_y', 2)
            frame, value = _movement_binary_flags(state, frame, low16(frame.offset_y), 1, 16, True)
            frame = first_replace(frame, offset_y=replace_word(frame.offset_y, value))
            frame = _movement_move(state, frame, 'target_x', 0, 16)
            while True:
                state.set_status_word(state.sr & 0xFFEF)
                frame = first_replace(frame, status=state.sr & 31)
                for name in ('distance', 'choice', 'offset_x'):
                    frame = _highbank_roxr_plane_fields(state, frame, name)
                state.set_status_word(state.sr | 16)
                frame = first_replace(frame, status=state.sr & 31)
                frame = _highbank_roxr_plane_fields(state, frame, 'target_x')
                frame = _highbank_dbra_fields(frame, 'offset_y')
                if low16(frame.offset_y) == 65535:
                    break
            frame = _movement_move_long(state, frame, 'target_y', frame.candidates.long())
            frame = _movement_move_long(state, frame, 'target_y', frame.target_y & frame.target_x)
            frame = _movement_move_long(state, frame, 'distance', frame.distance | frame.target_y)
        frame = _movement_move_long(state, frame, 'unit', swap_words(frame.unit))
        frame = _movement_move_long(state, frame, 'count', swap_words(frame.count))
        frame = _highbank_write_fields(state, frame, u32(frame.roster.base + s16(low16(frame.count))), frame.offset_x, 4)
        frame = _highbank_write_fields(state, frame, u32(frame.roster.base + s16(low16(frame.unit))), frame.choice, 4)
        frame = _highbank_write_fields(state, frame, frame.roster.base, frame.distance, 4)
        frame = first_replace(frame, roster=frame.roster.advance(4))
        frame = _highbank_write_fields(state, frame, frame.candidates.base, frame.offset_x, 4)
        frame = first_replace(frame, candidates=frame.candidates.advance(4))
        frame = _movement_move_long(state, frame, 'unit', swap_words(frame.unit))
        frame = _movement_move_long(state, frame, 'count', swap_words(frame.count))
        frame = _highbank_dbra_fields(frame, 'unit')
        if low16(frame.unit) == 65535:
            break
    frame = _movement_move_long(state, frame, 'unit', swap_words(frame.unit))
    frame = _movement_move_long(state, frame, 'count', swap_words(frame.count))
    frame = _movement_test(state, frame, state.read(0xFFFFF37A, 2), 16)
    if not frame.status & 4:
        frame = _movement_move(state, frame, 'target_y', 3, 16)
        while True:
            frame = _highbank_child_fields(state, frame, 0x6748E, 0x67456)
            frame = _highbank_write_fields(state, frame, u32(frame.roster.base + s16(low16(frame.count))), frame.offset_x, 4)
            frame = _highbank_write_fields(state, frame, u32(frame.roster.base + s16(low16(frame.unit))), frame.offset_x, 4)
            frame = _highbank_write_fields(state, frame, frame.roster.base, frame.offset_x, 4)
            frame = first_replace(frame, roster=frame.roster.advance(4))
            frame = _highbank_dbra_fields(frame, 'target_y')
            if low16(frame.target_y) == 65535:
                break
    return _highbank_write_fields(state, frame, u32(frame.roster.base + s16(low16(frame.count))), 0, clear=True)


def _highbank_scroll_timer_fields(state: SceneState, frame: FirstDeploymentFrame) -> tuple:
    checked_state(state)
    if type(frame) is not FirstDeploymentFrame:
        raise ValueError('actual Highbank fields required')
    frame.validate(state, False)
    return _highbank_memory_add_fields(state, frame, 0xFFFFEFDA, -1)


def _highbank_due_message_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _highbank_frame_fields(state, frame, 0x671BE)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFEFD8, 2), 16)
    frame = _highbank_shift_fields(state, frame, 'target_x', 1)
    frame = _highbank_write_fields(state, frame, 0xFFFFEFDA, state.table_at(0x671B0).word(low16(frame.target_x)))
    frame = first_replace(frame, roster=state.table_at(state.read(0xFFFFF3BE, 4)).cursor())
    frame, value = _highbank_memory_add_fields(state, frame, 0xFFFFF3BE, 2, 4)
    frame = _movement_move(state, frame, 'target_x', frame.roster.word(), 16)
    frame = _highbank_write_fields(state, frame, 0xFFFFF77C, low16(frame.target_x))
    if frame.status & 4:
        frame = first_replace(frame, roster=state.table_at(u32(0xFFFFD100 + s16(state.read(0xFFFFF31A, 2)))).cursor())
        frame = _highbank_child_fields(state, frame, 0x67354, 0x67216)
        frame = first_replace(frame, controller=state.table_at(0x674AA))
        frame = _highbank_child_fields(state, frame, 0x673A6, 0x67220)
        frame, value = _highbank_memory_add_fields(state, frame, 0xFFFFF37C, 18)
        return frame
    if frame.status & 8:
        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 255, 16)
        frame = _movement_move(state, frame, 'target_x', state.table_at(0x67238).word(low16(frame.target_x)), 16)
        return _highbank_target_fields(state, frame, u32(0x6724E + s16(low16(frame.target_x))))
    frame = first_replace(frame, roster=state.table_at(u32(0xFFFFD100 + s16(state.read(0xFFFFF31A, 2)))).cursor())
    frame = _highbank_child_fields(state, frame, 0x67354, 0x671E8)
    frame = _highbank_child_fields(state, frame, 0x6738C, 0x671EC)
    frame, value = _highbank_memory_add_fields(state, frame, 0xFFFFF37C, 18)
    frame = _movement_compare(state, frame, state.read(0xFFFFF37C, 2), 288, 16)
    if not frame.status & 1:
        frame = _highbank_write_fields(state, frame, 0xFFFFF37A, state.read(0xFFFFF37A, 2) ^ 1)
        frame = _highbank_write_fields(state, frame, 0xFFFFF37C, 0, clear=True)
    return frame


def advance_scrolling_message_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """671B6: non-due timer needs no invented register; due entry requires full ABI."""
    frame, timer = _highbank_scroll_timer_fields(state, frame)
    return frame if timer else _highbank_due_message_fields(state, frame)


def advance_message_decoration_stage_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame = _highbank_frame_fields(state, frame, 0x674CA)
    frame = first_replace(frame, roster=state.table_at(u32(0xFFFFD100 + s16(state.read(0xFFFFF31A, 2)))).cursor())
    frame = _highbank_child_fields(state, frame, 0x6750A, 0x674D6)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF36A, 2), 16)
    frame = _highbank_shift_fields(state, frame, 'target_x', 1)
    frame = _movement_move(state, frame, 'target_x', state.table_at(0x67502).word(low16(frame.target_x)), 16)
    frame = _highbank_child_fields(state, frame, u32(0x6751E + s16(low16(frame.target_x))), 0x674E4)
    frame, value = _highbank_memory_add_fields(state, frame, 0xFFFFF36A, 1)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF36A, 2), 16)
    frame = _movement_compare(state, frame, low16(frame.target_x), 4, 16)
    if not frame.status & 1:
        frame, value = _highbank_memory_add_fields(state, frame, 0xFFFFF362, 1)
        frame = _highbank_write_fields(state, frame, 0xFFFFF36A, 0, clear=True)
        previous = state.read(0xFFFFF3A4, 1)
        state.write(0xFFFFF3A4, 1, previous | 64)
        status = (frame.status & 27) | (0 if previous & 64 else 4)
        state.sr = (state.sr & 65504) | status
        return first_replace(frame, status=status)
    return frame


def _highbank_selection_observation_fields(state: SceneState, choice: OfficerSelection) -> FirstDeploymentFrame:
    checked_context(choice, OfficerSelection, state)
    return first_replace(FirstDeploymentFrame.unobserved(), target_x=choice.count,
        target_y=choice.force, unit=choice.scan, count=choice.score, distance=choice.trait,
        offset_x=choice.displaced, offset_y=choice.displaced_score, choice=choice.selected)


def _highbank_selection_projection(state: SceneState, frame: FirstDeploymentFrame) -> OfficerSelection:
    return OfficerSelection(frame.target_x, frame.target_y, frame.unit, frame.count,
        frame.distance, frame.offset_x, frame.offset_y, frame.choice).validate(state)


def _highbank_message_observation_fields(state: SceneState, layout: MessageLayout) -> FirstDeploymentFrame:
    checked_context(layout, MessageLayout, state)
    return first_replace(FirstDeploymentFrame.unobserved(), target_x=layout.symbol,
        target_y=layout.position, unit=layout.stride, count=layout.row_offset,
        distance=layout.first_plane, offset_x=layout.fill, offset_y=layout.shift_count,
        choice=layout.second_plane, roster=layout.destination, controller=layout.bitmap,
        candidates=layout.previous_rows)


def _highbank_message_projection(state: SceneState, frame: FirstDeploymentFrame) -> MessageLayout:
    return MessageLayout(frame.target_x, frame.target_y, frame.unit, frame.count,
        frame.distance, frame.offset_x, frame.offset_y, frame.choice,
        frame.roster, None if frame.controller is None else state.table_at(frame.controller.base).cursor(),
        frame.candidates).validate(state)

def _message_control_transaction_fields(state: SceneState, frame: FirstDeploymentFrame) -> tuple:
    """Select the actual live message WORD, then enter its unique preparation.

    The ordinary BRA/fall-through has no new return slot. Only the original
    676EE indexed JSR owns its physical 676F2 inner LONG. Its unknown target
    remains a genuine entered boundary, not a partial-WORD fake full return.
    """
    from ..high_level_command_actions.contexts_message import MessageMemory
    from ..high_level_command_actions.business_reuse import _prepare_message_fields
    frame = _highbank_frame_fields(state, frame, 423620)
    frame = _movement_move(state, frame, 'target_x', state.read(4294964096, 2), 16)
    frame = _movement_compare(state, frame, low16(frame.target_x), 96, 16)
    if frame.status & 1:
        frame = _highbank_shift_fields(state, frame, 'target_x', 1)
        frame = _movement_move(state, frame, 'target_x', state.table_at(423638).word(low16(frame.target_x)), 16)
    else:
        frame, selected = _movement_binary_flags(state, frame, low16(frame.target_x), 96, 16, True)
        frame = first_replace(frame, target_x=replace_word(frame.target_x, selected))
        frame = _highbank_shift_fields(state, frame, 'target_x', 1)
        frame = _movement_move(state, frame, 'target_x', state.table_at(423756).word(low16(frame.target_x)), 16)
        frame = first_replace(frame, roster=state.table_at(423858).cursor())
        frame = _highbank_child_fields(state, frame, u32(423858 + s16(low16(frame.target_x))), 423666)
    memory = MessageMemory(state, frame)
    preparation = _prepare_message_fields(memory, low16(frame.target_x))
    return (memory.frame, preparation)

def dispatch_message_control_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """676C4 whole actual Frame entry; its incoming outer LONG is caller-owned."""
    returned, preparation = _message_control_transaction_fields(state, frame)
    return returned
