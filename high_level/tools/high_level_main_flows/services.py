"""Typed semantic call boundary for boot/map/gameplay modules.

This links actual logical implementations when explicit ABI adapters are
provided. It does not interpret instructions, invent return values, read source
files or replay cached reference state. Unresolved calls expose their target
and original supplied context so callers cannot mistake them for completion.
"""
from dataclasses import dataclass, is_dataclass
from types import MappingProxyType
from typing import Callable

from .domain import (
    Boundary, SceneServices, SceneState, Cursor, Long, Word, VideoPlaneAddress,
    StackContinuation, checked_state, checked_cursor, uint, low8,
    descending_inclusive, replace_word, typed_service_context,
)
from ..high_level_scene_flows.business_reuse import (
    clear_video_sprite_plane, enqueue_sound_command, wait_for_scene_sound_byte, step_random,
    expand_glyph_row, expand_glyph_stream, stage_sprite_word_packet,
)
from ..high_level_scene_flows.business_scene import (
    decode_glyph_rows_to_buffers, write_vdp_packet_stream, write_vdp_dictionary_repeat_stream,
    append_clipped_scene_sprites,
    append_unclipped_scene_sprites, write_vdp_word_rle_stream,
    write_vdp_swapped_byte_rle_stream, write_vdp_swapped_byte_rle_stream_complete,
    read_vdp_plane_rle_rows,
    advance_plane_row, advance_scene_palette_fade, flush_scene_transfer_queue,
    copy_scene_palette_variant, snapshot_and_clear_scene_palette,
    begin_scene_palette_darken, darken_palette,
    sample_random_preserving_seed_carrier,
)
from ..high_level_scene_flows.contexts_reuse import (
    GlyphColors, GlyphStreamResult, SpriteControlContext, SpriteControlResult,
)
from ..high_level_scene_flows.contexts_scene import (
    PlaneRowContext, PlaneRowResult, PlaneStreamResult, VdpStreamResult,
    GlyphRowsResult, SwappedByteRleRetained,
)
from ..high_level_scene_flows.contexts_objects import (
    SceneRenderFrame, SpriteBatchContext, SpriteBatchResult,
)
from ..high_level_dynamic_flows.contexts_actions import TileUploadResult
from ..high_level_command_actions.business_reuse import build_scene_roster, prepare_scene_message_fields
from .reuse_display import append_map_sprites, append_six_place_decimal_value, append_six_place_decimal_fields
from .contexts_display_reuse import MapSpriteResult
from .contexts_rule_reuse import (
    DefenseProgressResult, MonthlyActionsResult, TerrainQueryResult,
)

from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
from ..high_level_battle_ai.business_formation import read_first_side_staging_anchor_fields

from ..high_level_battle_ai.business_formation import read_second_side_staging_anchor_fields

from ..high_level_battle_ai.business_geometry import select_weakest_contact_strength_fields
from ..high_level_battle_ai.business_formation import (
    compare_actor_shifted_troop_word_to_weakest_contact_fields, read_outer_east_staging_anchor_fields, select_contact_nearest_deployment_anchor_fields, read_formation_relative_position_delta_fields, test_point_in_battlefield_staging_rectangle_fields, sample_battlefield_staging_rectangle_fields,
)

from ..high_level_battle_ai.contexts_actions import AnchorContext
from ..high_level_battle_ai.business_geometry import load_battlefield_map_fields, collect_contacts_in_speed_radius_fields
from ..high_level_battle_ai.business_actions import (
    read_city_deployment_anchor_fields, read_city_second_deployment_anchor_fields,
    build_deployment_occupied_cell_fields, find_next_empty_position_slot_fields,
    deployment_edge_coordinate_allowed,
    sample_battle_action_random_fields, select_strongest_type6_candidate_fields, compute_type6_budget_from_random_state_fields,
    select_strongest_open_terrain_candidate_second_side_fields, compute_candidate_budget_fields, compute_candidate_budget_base20_fields, compute_candidate_budget_base30_fields,
)

def award_defense_progress(state: SceneState, officer: Long, gain: Long) -> DefenseProgressResult:
    """Keep the rule implementation singular while avoiding bootstrap cycles."""
    from .reuse_rules import award_defense_progress
    return award_defense_progress(state, officer, gain)

def clear_completed_monthly_actions(state: SceneState, retained_counter: Long) -> MonthlyActionsResult:
    """Resolve the fixed monthly-rule adapter only when it is called."""
    from .reuse_rules import clear_completed_monthly_actions
    return clear_completed_monthly_actions(state, retained_counter)

def query_scaled_terrain(state: SceneState, row: Long, column: Long,
                        retained_terrain: Long, retained_cost: Long) -> TerrainQueryResult:
    """Delegate to the single terrain rule without an eager service back-edge."""
    from .reuse_rules import query_scaled_terrain
    return query_scaled_terrain(state, row, column, retained_terrain, retained_cost)

def sample_random_pair(state: SceneState):
    """Load the one dynamic RNG adapter at use, not during service bootstrap."""
    from ..high_level_dynamic_flows.services import sample_random_pair
    return sample_random_pair(state)

def set_vram_write_address(state: SceneState, value: VideoPlaneAddress | Long) -> Long:
    """Fixed named delegate; import ordering does not manufacture a device call."""
    from ..high_level_dynamic_flows.services import set_vram_write_address
    return set_vram_write_address(state, value)

def read_vdp_plane_rle_rows_from_control(state: SceneState, source: Cursor,
        video_address: VideoPlaneAddress, row_stride: Long, rows: Word) -> PlaneStreamResult:
    """One original plane reader behind a delayed cross-family dependency."""
    from ..high_level_dynamic_flows.services import read_vdp_plane_rle_rows_from_control
    return read_vdp_plane_rle_rows_from_control(state, source, video_address, row_stride, rows)

def append_scene_sprite_entries(state: SceneState, context: SpriteBatchContext) -> SpriteBatchResult:
    """Delegate to the one sprite algorithm without boot-time dependency cycles."""
    from ..high_level_dynamic_flows.services import append_scene_sprite_entries
    return append_scene_sprite_entries(state, context)

def upload_portrait_tiles(state: SceneState, frame: SceneRenderFrame) -> TileUploadResult:
    """The original portrait upload is resolved only when genuinely invoked."""
    from ..high_level_dynamic_flows.business_actions import upload_portrait_tiles
    return upload_portrait_tiles(state, frame)


def refresh_gameplay_scene(state: SceneState, retained: Long) -> Long:
    """Historical AF48 LONG projection of the sole same-state two-edge core."""
    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory, FirstDeploymentFrame, first_replace
    from ..high_level_gameplay_flow.business_services import refresh_gameplay_scene_fields
    checked_state(state)
    uint(retained,32)
    frame = first_replace(FirstDeploymentFrame.unobserved(),target_x=retained)
    return refresh_gameplay_scene_fields(SceneRefreshMemory(state),frame).target_x


def initialize_video_registers_and_planes(state: SceneState) -> None:
    """6826 established register/CRAM/VRAM initialization on the same state.

    The register sequence is read from externally supplied data at68A8; it is
    not copied into executable source. Original DMA/sound-bus waits and live
    register shadow observations remain ordered. This service's effects are
    previous code coverage; its complete caller scratch ABI is not asserted.
    """
    from .domain import descending_inclusive
    checked_state(state)
    registers = state.table_at(0x68A8).cursor()
    for _ in descending_inclusive(18):
        state.write(0xC00004, 2, registers.next_word())
    state.write(0xFFFFF606, 2, state.read(0x68AA, 2))
    state.write(0xC00004, 4, 0xC0000000)
    for _ in descending_inclusive(0x3F):
        state.write(0xC00000, 2, 0)
    state.write(0xC00004, 2, 0x8F01)
    state.write(0xC00004, 2, state.read(0xFFFFF606, 2) | 0x10)
    state.write(0xC00004, 4, 0x93FF94FF)
    state.write(0xC00004, 2, 0x9780)
    state.write(0xC00004, 4, 0x40000080)
    state.write(0xC00000, 2, 0)
    while state.read(0xC00004, 2) & 2:
        state.progress('vdp-dma')
    if state.read(0xFF3F00, 1) == 0:
        state.write(0xA11100, 2, 0)
    state.write(0xC00004, 2, state.read(0xFFFFF606, 2))
    state.write(0xC00004, 2, 0x8F02)


def read_vdp_plane_literal_rows(state: SceneState, source: Cursor,
        video_address: VideoPlaneAddress, row_stride: Long, rows: Word,
        marker_carrier: Long) -> PlaneStreamResult:
    """3AAB6 literal entry, not the32-row RLE entry at3AACE.

    Clear8000 and set8002=1, then enter3AADA: the original entry neither
    resets caller rows nor consumes a marker. The incoming marker BYTE stays
    available if live8002 changes later. Row completion keeps the actual
    discarded decoder continuation; it is not an invented local RTS.
    """
    checked_state(state)
    checked_cursor(source, state)
    if type(video_address) is not VideoPlaneAddress:
        raise ValueError('explicit video-plane address required')
    video_address.__post_init__()
    uint(row_stride, 32)
    uint(rows, 16)
    uint(marker_carrier, 32)
    state.write(0xFFFF8000, 2, 0)
    state.write(0xFFFF8002, 2, 1)
    state.write(0xC00004, 2, 0x8F02)
    command = set_vram_write_address(state, video_address)
    column, marker = 0, low8(marker_carrier)
    if state.read(0xFFFF8002, 2) == 0:
        marker = source.next_byte()
    while True:
        high = source.next_byte()
        literal = state.read(0xFFFF8002, 2) != 0 or marker != high
        if literal:
            value = (high << 8 | source.next_byte()) | state.read(0xFFFF8000, 2)
            state.write(0xC00000, 2, value)
            result = advance_plane_row(state, PlaneRowContext(video_address,
                row_stride, column, rows, command, StackContinuation(0x3AB10)))
        else:
            count = source.next_byte()
            if count == 0:
                return PlaneStreamResult(source, video_address, command, column, rows, None)
            value = source.next_byte() << 8 | source.next_byte()
            for _ in descending_inclusive(count):
                # DBRA at3AB2C really returns to3AB20, before this live OR.
                value |= state.read(0xFFFF8000, 2)
                state.write(0xC00000, 2, value)
                result = advance_plane_row(state, PlaneRowContext(video_address,
                    row_stride, column, rows, command, StackContinuation(0x3AB2C)))
                video_address, column, rows, command = (result.video_address,
                    result.column, result.rows_remaining, result.command_carrier)
                if result.discarded_continuation is not None:
                    return PlaneStreamResult(source, video_address, command,
                        column, rows, result.discarded_continuation)
        video_address, column, rows, command = (result.video_address,
            result.column, result.rows_remaining, result.command_carrier)
        if result.discarded_continuation is not None:
            return PlaneStreamResult(source, video_address, command,
                column, rows, result.discarded_continuation)


class UnresolvedCall(Boundary):
    """The actual call target is known, but its typed logical ABI is unbound."""

    def __init__(self, target, context):
        self.target = uint(target, 32, 'actual service target')
        self.context = context
        super().__init__(f'unbound logical service at 0x{target:08X}')


@dataclass(frozen=True)
class ServiceBinding:
    """One explicit target ABI and its genuine semantic implementation."""

    target: int
    context_type: type
    result_type: type
    handler: Callable

    def __post_init__(self):
        uint(self.target, 32, 'service target')
        if not isinstance(self.context_type, type) or not is_dataclass(self.context_type):
            raise ValueError('declared dataclass input contract required')
        if not isinstance(self.result_type, type) or not is_dataclass(self.result_type):
            raise ValueError('declared dataclass return contract required')
        if not callable(self.handler):
            raise ValueError('actual semantic implementation required')


class LogicalServices(SceneServices):
    """Explicit finite linkage, not a general CPU/PC execution dispatcher.

    Bindings adapt known source interfaces; an absent entry stops immediately.
    The same original callee can have several caller-specific typed contracts.
    Each (target, exact input type) has one authority; no adapter is selected by
    guessing fields, dropping carriers or treating an arbitrary type as valid.
    Installing a binding alone is not evidence of natural gameplay or full
    caller-carrier preservation. Those contracts require separate verification.
    """

    def __init__(self, bindings=()):
        if type(bindings) is not tuple or any(type(b) is not ServiceBinding for b in bindings):
            raise ValueError('explicit tuple of service ABI bindings required')
        signatures = tuple((binding.target, binding.context_type) for binding in bindings)
        if len(set(signatures)) != len(signatures):
            raise ValueError('one semantic call authority per target and exact input contract')
        self.bindings = MappingProxyType(dict(zip(signatures, bindings)))
        self.targets = frozenset(binding.target for binding in bindings)

    def invoke(self, state, entry, context):
        checked_state(state)
        uint(entry, 32, 'actual service target')
        typed_service_context(context, state)
        binding = self.bindings.get((entry, type(context)))
        if binding is None:
            if entry not in self.targets:
                raise UnresolvedCall(entry, context)
            raise Boundary(f'input ABI mismatch at 0x{entry:08X}')
        result = binding.handler(state, context)
        if type(result) is not binding.result_type:
            raise Boundary(f'return ABI mismatch at 0x{entry:08X}')
        return typed_service_context(result, state)


def call_target(state: SceneState, target: int, context):
    """Invoke a supplied typed semantic service; never substitute fake success."""
    checked_state(state)
    uint(target, 32, 'actual original call target')
    typed_service_context(context, state)
    if type(state.services) is SceneServices:
        raise UnresolvedCall(target, context)
    result = state.service_at(target, context)
    return typed_service_context(result, state)


# Real same-state deployment edge and promotion cores.
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame
from ..high_level_battle_ai.business_actions import (
    scan_deployment_first_edge_fields, scan_deployment_second_edge_fields,
    promote_first_roster_deployment_candidate_fields,
    promote_second_roster_deployment_candidate_fields,
)

# Same-state first-side fields; no second deployment implementation.
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame
from ..high_level_battle_ai.business_formation import initialize_first_side_deployment_fields, prepare_first_side_assignment_fields

# Sole leader-roster fields shared with battle AI; same live state.
from ..high_level_battle_ai.business_geometry import test_battlefield_leader_roster_presence_fields

# Same-state sole WORD special-message cores; no second implementation.
def enter_special_message_mode_fields(state: SceneState):
    """Resolve the sole message core without importing a partial highbank module."""
    from ..high_level_remaining_flows.business_highbank import enter_special_message_mode_fields
    return enter_special_message_mode_fields(state)

def fixed_special_message_fields(state: SceneState):
    """Fixed same-state delegate, with no additional game call or result."""
    from ..high_level_remaining_flows.business_highbank import fixed_special_message_fields
    return fixed_special_message_fields(state)

def choose_special_message_for_action_fields(state: SceneState):
    """Use the unique message-selection algorithm after module initialization."""
    from ..high_level_remaining_flows.business_highbank import choose_special_message_for_action_fields
    return choose_special_message_for_action_fields(state)


# Original239D6/239F4 same-state complete field authorities.
from ..high_level_battle_ai.business_formation import (
    sum_first_side_roster_troops_fields, test_force_has_city_assignment_fields,
)

# Single recovered equipment algorithms over the caller's same live state.
from ..high_level_player_commands.contexts_equipment import EquipmentMenuMemory
from ..high_level_player_commands.business_recruitment import (
    append_equipment_dialog_frame_fields, append_equipment_input_digits_fields,
    append_equipment_total_digits_fields,
)


# Sole actual23A1A/23A3C semantic field authorities.
from ..high_level_battle_ai.business_formation import (
    test_second_side_total_with_single_first_roster_fields,
    test_second_side_total_with_small_second_roster_fields,
)


# Historical 226B6 sole roster-count / troop-total fields.
def count_opposing_battle_roster_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Share the recovered roster core while keeping service bootstrap acyclic."""
    from ..high_level_remaining_flows.business_highbank import count_opposing_battle_roster_fields
    return count_opposing_battle_roster_fields(state, frame)


# Actual sole236E4 standard-action fields, not a second decision algorithm.
def evaluate_secondary_standard_action_fields(state: SceneState, frame: FirstDeploymentFrame,
                                             complete: bool=False) -> FirstDeploymentFrame:
    """Delay only module resolution; preserve the original completeness selector."""
    from ..high_level_remaining_flows.business_highbank import evaluate_secondary_standard_action_fields
    return evaluate_secondary_standard_action_fields(state, frame, complete)


# Historical2363E single target-position authority.
def evaluate_standard_position_order_fields(state: SceneState, frame: FirstDeploymentFrame,
                                           complete: bool=False):
    """Fixed delegate to the single position-order field authority."""
    from ..high_level_remaining_flows.business_highbank import evaluate_standard_position_order_fields
    return evaluate_standard_position_order_fields(state, frame, complete)


# Unique gameplay battle authority; Scene adapter retains the same state.
from ..high_level_gameplay_flow.contexts_battle import BattleTriggerMemory, BattleTriggerFrame
from ..high_level_gameplay_flow.business_battle import trigger_battle_for_city_rectangle_fields


# Actual historical26560 sole action-chain fields, complete current return.
def execute_standard_action_chain_fields(state: SceneState, frame: FirstDeploymentFrame,
                                        complete: bool=False):
    """Fixed delegate to the single standard-action chain, without a new slot."""
    from ..high_level_remaining_flows.business_highbank import execute_standard_action_chain_fields
    return execute_standard_action_chain_fields(state, frame, complete)

# Sole recovered1DCAA complete movement-velocity authority, no copied algorithm.
def city_calculate_live_quotient_10_fields(memory: BattlePolicyMemory,
                                        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """City quotient bridge shares its one algorithm without a bootstrap cycle."""
    from ..high_level_remaining_flows.business_city import city_calculate_live_quotient_10_fields
    return city_calculate_live_quotient_10_fields(memory, frame)


# One existing22756 owner, shared full retreat-policy fields.
def evaluate_other_city_retreat_order_fields(state: SceneState, frame: FirstDeploymentFrame,
                                           complete: bool=False) -> FirstDeploymentFrame:
    """Resolve the recovered retreat core at use, not via an import back-edge."""
    from ..high_level_remaining_flows.business_highbank import evaluate_other_city_retreat_order_fields
    return evaluate_other_city_retreat_order_fields(state, frame, complete)

# One original23C9A strength gate shared by guarded primary-order tails.
from ..high_level_battle_ai.business_formation import test_second_side_relative_total_shortfall_fields

# Sole22D30 live retreat marking policy; its caller owns the return slot.
from ..high_level_battle_ai.business_geometry import mark_eligible_actor_for_retreat_fields

# B38 formation core shares actual Scene memory/frame, fixed-width CCR and sole RNG.
from ..high_level_scene_flows.contexts_scene import (
    SceneRefreshMemory,SceneRefreshBoundary,FirstDeploymentFrame,first_replace,
    _first_word,_scene_refresh_emit,
)
from ..high_level_scene_flows.business_scene import _scene_render_compare,sample_random_preserving_seed_fields
from ..high_level_gameplay_flow.business_battle import _presentation_call_fields
from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
