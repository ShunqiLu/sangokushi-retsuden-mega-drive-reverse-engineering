"""Fixed registration of typed resource authorities for the high-level ROM.

The 109 extension codecs and 19 earlier/base authorities are declared here,
not imported from a test. Legacy source paths are a workspace preparation
convenience; a supplied source_root reads only the registered own resources/
paths. No ROM, original bank, compiler output or opcode payload is an input.
Unknown/code aliases are refused rather than clipped or silently overwritten.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from . import resource_adapters as adapters
from .media_sources import load_source

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GEOMETRY = Path(__file__).with_name('resource_geometry.json')


@dataclass(frozen=True)
class ResourceSpec:
    id: str
    codec: str
    source: str
    own_source: str
    role: str
    chain: str


RESOURCE_SPECS = (
    ResourceSpec("audio_build", "tools.audio_build.audio_build", "analysis/audio_build/generated/assets.json", "resources/audio/audio_build.json", "audio", "base"),
    ResourceSpec("dialogue_text", "tools.high_level_rom.resource_adapters_records", "analysis/dialogue_text/generated/assets.json", "resources/data/dialogue_text.json", "data", "base"),
    ResourceSpec("font_build", "tools.font_build.font_build", "analysis/font_build/generated/assets.json", "resources/images/font_build.json", "images", "base"),
    ResourceSpec("graphics_build", "tools.graphics_build.graphics_build", "analysis/graphics_build/generated/assets.json", "resources/images/graphics_build.json", "images", "base"),
    ResourceSpec("scaled_bitmaps", "tools.high_level_rom.resource_adapters_machine", "analysis/scaled_bitmaps/generated/assets.json", "resources/images/scaled_bitmaps.json", "images", "base"),
    ResourceSpec("world_resources", "tools.high_level_rom.resource_adapters_records", "analysis/world_resources/generated/assets.json", "resources/data/world_resources.json", "data", "base"),
    ResourceSpec("battle_graphics", "tools.high_level_rom.resource_adapters_maps", "analysis/battle_graphics/generated/assets.json", "resources/images/battle_graphics.json", "images", "base"),
    ResourceSpec("scenario_build", "tools.high_level_rom.resource_adapters_records", "analysis/scenario_build/generated/assets.json", "resources/data/scenario_build.json", "data", "base"),
    ResourceSpec("portrait_graphics", "tools.portrait_graphics.portrait_graphics", "analysis/portrait_graphics/generated/assets.json", "resources/images/portrait_graphics.json", "images", "base"),
    ResourceSpec("terrain_maps", "tools.high_level_rom.resource_adapters_maps", "analysis/terrain_maps/generated/assets.json", "resources/data/terrain_maps.json", "data", "base"),
    ResourceSpec("battlefield_resources", "tools.high_level_rom.resource_adapters_ui", "analysis/battlefield_resources/generated/assets.json", "resources/data/battlefield_resources.json", "data", "base"),
    ResourceSpec("ui_layouts", "tools.high_level_rom.resource_adapters_ui", "analysis/ui_layouts/generated/assets.json", "resources/data/ui_layouts.json", "data", "base"),
    ResourceSpec("personnel_flow", "tools.high_level_rom.resource_adapters_records", "analysis/personnel_flow/generated/scenario_candidates.json", "resources/data/personnel_flow.json", "data", "base"),
    ResourceSpec("candidate_tables", "tools.high_level_rom.resource_adapters_records", "analysis/candidate_tables/generated/assets.json", "resources/data/candidate_tables.json", "data", "base"),
    ResourceSpec("candidate_action_tables", "tools.high_level_rom.resource_adapters_records", "analysis/candidate_action_tables/generated/assets.json", "resources/data/candidate_action_tables.json", "data", "base"),
    ResourceSpec("candidate_handler_tables", "tools.high_level_rom.resource_adapters_records", "analysis/candidate_handler_tables/generated/assets.json", "resources/data/candidate_handler_tables.json", "data", "base"),
    ResourceSpec("vdp_word_streams", "tools.high_level_rom.resource_adapters_maps", "analysis/vdp_word_streams/generated/fields.json", "resources/data/vdp_word_streams.json", "data", "base"),
    ResourceSpec("dictionary_streams", "tools.high_level_rom.resource_adapters_maps", "analysis/dictionary_streams/generated/fields.json", "resources/data/dictionary_streams.json", "data", "base"),
    ResourceSpec("sprite_word_resources", "tools.high_level_rom.resource_adapters_tiles", "analysis/sprite_word_resources/generated/fields.json", "resources/images/sprite_word_resources.json", "images", "extension"),
    ResourceSpec("battle_variant_tiles", "tools.high_level_rom.resource_adapters_tiles", "analysis/battle_variant_tiles/generated/fields.json", "resources/images/battle_variant_tiles.json", "images", "extension"),
    ResourceSpec("world_tile_chunks", "tools.high_level_rom.resource_adapters_tiles", "analysis/world_tile_chunks/generated/fields.json", "resources/images/world_tile_chunks.json", "images", "extension"),
    ResourceSpec("compact_sprite_records", "tools.high_level_rom.resource_adapters_tiles", "analysis/compact_sprite_records/generated/fields.json", "resources/images/compact_sprite_records.json", "images", "extension"),
    ResourceSpec("scene_sprite_resources", "tools.high_level_rom.resource_adapters_scene", "analysis/scene_sprite_resources/generated/fields.json", "resources/images/scene_sprite_resources.json", "images", "extension"),
    ResourceSpec("scene_tile_resources", "tools.high_level_rom.resource_adapters_scene", "analysis/scene_tile_resources/generated/fields.json", "resources/images/scene_tile_resources.json", "images", "extension"),
    ResourceSpec("battle_overlay_maps", "tools.high_level_rom.resource_adapters_ui", "analysis/battle_overlay_maps/generated/fields.json", "resources/data/battle_overlay_maps.json", "data", "extension"),
    ResourceSpec("audio_root_resources", "tools.high_level_rom.resource_adapters_machine", "analysis/audio_root_resources/generated/fields.json", "resources/audio/audio_root_resources.json", "audio", "extension"),
    ResourceSpec("display_tile_resources", "tools.high_level_rom.resource_adapters_scene", "analysis/display_tile_resources/generated/fields.json", "resources/images/display_tile_resources.json", "images", "extension"),
    ResourceSpec("battle_rule_tables", "tools.high_level_rom.resource_adapters_structure", "analysis/battle_rule_tables/generated/fields.json", "resources/data/battle_rule_tables.json", "data", "extension"),
    ResourceSpec("battle_palette_transfers", "tools.high_level_rom.resource_adapters_sprite_palette", "analysis/battle_palette_transfers/generated/fields.json", "resources/images/battle_palette_transfers.json", "images", "extension"),
    ResourceSpec("audio_dispatch_fields", "tools.high_level_rom.resource_adapters_machine", "analysis/audio_dispatch_fields/generated/fields.json", "resources/audio/audio_dispatch_fields.json", "audio", "extension"),
    ResourceSpec("legacy_text_fields", "tools.high_level_rom.resource_adapters_records", "analysis/legacy_text_fields/generated/fields.json", "resources/data/legacy_text_fields.json", "data", "extension"),
    ResourceSpec("title_overlay_maps", "tools.high_level_rom.resource_adapters_ui", "analysis/title_overlay_maps/generated/fields.json", "resources/data/title_overlay_maps.json", "data", "extension"),
    ResourceSpec("transport_cargo_build", "tools.high_level_rom.resource_adapters_structure", "analysis/transport_cargo_build/generated/fields.json", "resources/data/transport_cargo_build.json", "data", "extension"),
    ResourceSpec("battle_scene_sprites", "tools.high_level_rom.resource_adapters_ui", "analysis/battle_scene_sprites/generated/fields.json", "resources/images/battle_scene_sprites.json", "images", "extension"),
    ResourceSpec("menu_tree_fields", "tools.high_level_rom.resource_adapters_structure", "analysis/menu_tree_fields/generated/fields.json", "resources/data/menu_tree_fields.json", "data", "extension"),
    ResourceSpec("bank08_display_resources", "tools.high_level_rom.resource_adapters_scene", "analysis/bank08_display_resources/generated/fields.json", "resources/data/bank08_display_resources.json", "data", "extension"),
    ResourceSpec("battle_effect_sprites", "tools.high_level_rom.resource_adapters_ui", "analysis/battle_effect_sprites/generated/fields.json", "resources/images/battle_effect_sprites.json", "images", "extension"),
    ResourceSpec("bank06_display_tail", "tools.high_level_rom.resource_adapters_scene", "analysis/bank06_display_tail/generated/fields.json", "resources/data/bank06_display_tail.json", "data", "extension"),
    ResourceSpec("palette_copy_fields", "tools.high_level_rom.resource_adapters_sprite_palette", "analysis/palette_copy_fields/generated/fields.json", "resources/images/palette_copy_fields.json", "images", "extension"),
    ResourceSpec("menu_tile_streams", "tools.high_level_rom.resource_adapters_ui", "analysis/menu_tile_streams/generated/fields.json", "resources/images/menu_tile_streams.json", "images", "extension"),
    ResourceSpec("ui_fixed_records", "tools.high_level_rom.resource_adapters_ui", "analysis/ui_fixed_records/generated/fields.json", "resources/data/ui_fixed_records.json", "data", "extension"),
    ResourceSpec("battle_command_sprites", "tools.high_level_rom.resource_adapters_ui", "analysis/battle_command_sprites/generated/fields.json", "resources/images/battle_command_sprites.json", "images", "extension"),
    ResourceSpec("battle_deployment_parameters", "tools.high_level_rom.resource_adapters_fields", "analysis/battle_deployment_parameters/generated/fields.json", "resources/data/battle_deployment_parameters.json", "data", "extension"),
    ResourceSpec("battle_formation_coordinates", "tools.high_level_rom.resource_adapters_fields", "analysis/battle_formation_coordinates/generated/fields.json", "resources/data/battle_formation_coordinates.json", "data", "extension"),
    ResourceSpec("officer_lookup_parameters", "tools.high_level_rom.resource_adapters_fields", "analysis/officer_lookup_parameters/generated/fields.json", "resources/data/officer_lookup_parameters.json", "data", "extension"),
    ResourceSpec("education_factor_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/education_factor_fields/generated/fields.json", "resources/data/education_factor_fields.json", "data", "extension"),
    ResourceSpec("battle_marker_sprites", "tools.high_level_rom.resource_adapters_ui", "analysis/battle_marker_sprites/generated/fields.json", "resources/images/battle_marker_sprites.json", "images", "extension"),
    ResourceSpec("ai_selection_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/ai_selection_fields/generated/fields.json", "resources/data/ai_selection_fields.json", "data", "extension"),
    ResourceSpec("save_bitwidth_masks", "tools.high_level_rom.resource_adapters_fields", "analysis/save_bitwidth_masks/generated/fields.json", "resources/data/save_bitwidth_masks.json", "data", "extension"),
    ResourceSpec("battle_outcome_masks", "tools.high_level_rom.resource_adapters_fields", "analysis/battle_outcome_masks/generated/fields.json", "resources/data/battle_outcome_masks.json", "data", "extension"),
    ResourceSpec("indexed_action_parameters", "tools.high_level_rom.resource_adapters_fields", "analysis/indexed_action_parameters/generated/fields.json", "resources/data/indexed_action_parameters.json", "data", "extension"),
    ResourceSpec("city_cycle_parameters", "tools.high_level_rom.resource_adapters_fields", "analysis/city_cycle_parameters/generated/fields.json", "resources/data/city_cycle_parameters.json", "data", "extension"),
    ResourceSpec("header_vector_fields", "tools.header_vector_fields.codec", "analysis/header_vector_fields/generated/fields.json", "resources/data/header_vector_fields.json", "data", "extension"),
    ResourceSpec("officer_status_font_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/officer_status_font_fields/generated/fields.json", "resources/images/officer_status_font_fields.json", "images", "extension"),
    ResourceSpec("duel_ui_row_stream_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/duel_ui_row_stream_fields/generated/fields.json", "resources/data/duel_ui_row_stream_fields.json", "data", "extension"),
    ResourceSpec("ui_cursor_sprite_templates", "tools.high_level_rom.resource_adapters_fields", "analysis/ui_cursor_sprite_templates/generated/fields.json", "resources/images/ui_cursor_sprite_templates.json", "images", "extension"),
    ResourceSpec("portrait_alias_tiles", "tools.high_level_rom.resource_adapters_fields", "analysis/portrait_alias_tiles/generated/fields.json", "resources/images/portrait_alias_tiles.json", "images", "extension"),
    ResourceSpec("ai_threshold_pair_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/ai_threshold_pair_fields/generated/fields.json", "resources/data/ai_threshold_pair_fields.json", "data", "extension"),
    ResourceSpec("setup_ui_sprite_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/setup_ui_sprite_fields/generated/fields.json", "resources/images/setup_ui_sprite_fields.json", "images", "extension"),
    ResourceSpec("battle_cell_offsets", "tools.high_level_rom.resource_adapters_fields", "analysis/battle_cell_offsets/generated/fields.json", "resources/data/battle_cell_offsets.json", "data", "extension"),
    ResourceSpec("portrait_blank_alias_tiles", "tools.high_level_rom.resource_adapters_fields", "analysis/portrait_blank_alias_tiles/generated/fields.json", "resources/images/portrait_blank_alias_tiles.json", "images", "extension"),
    ResourceSpec("vdp_directory_fields", "tools.high_level_rom.resource_adapters_maps", "analysis/vdp_word_streams/generated/fields.json", "resources/data/vdp_directory_fields.json", "data", "extension"),
    ResourceSpec("portrait_alias_metadata", "tools.high_level_rom.resource_adapters_fields", "analysis/portrait_alias_metadata/generated/fields.json", "resources/images/portrait_alias_metadata.json", "images", "extension"),
    ResourceSpec("fm_instrument_alias_fields", "tools.high_level_rom.resource_adapters_machine", "analysis/fm_instrument_alias_fields/generated/fields.json", "resources/audio/fm_instrument_alias_fields.json", "audio", "extension"),
    ResourceSpec("audio_frequency_fields", "tools.high_level_rom.resource_adapters_machine", "analysis/audio_frequency_fields/generated/fields.json", "resources/audio/audio_frequency_fields.json", "audio", "extension"),
    ResourceSpec("indexed_ui_lookup_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/indexed_ui_lookup_fields/generated/fields.json", "resources/data/indexed_ui_lookup_fields.json", "data", "extension"),
    ResourceSpec("portrait_external_alias_pixels", "tools.high_level_rom.resource_adapters_fields", "analysis/portrait_external_alias_pixels/generated/fields.json", "resources/images/portrait_external_alias_pixels.json", "images", "extension"),
    ResourceSpec("ui_panel_row_stream_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/ui_panel_row_stream_fields/generated/fields.json", "resources/data/ui_panel_row_stream_fields.json", "data", "extension"),
    ResourceSpec("boot_hardware_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/boot_hardware_fields/generated/fields.json", "resources/data/boot_hardware_fields.json", "data", "extension"),
    ResourceSpec("fm_external_alias_fields", "tools.fm_external_alias_fields.codec", "analysis/fm_external_alias_fields/generated/fields.json", "resources/audio/fm_external_alias_fields.json", "audio", "extension"),
    ResourceSpec("battle_probability_word_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/battle_probability_word_fields/generated/fields.json", "resources/data/battle_probability_word_fields.json", "data", "extension"),
    ResourceSpec("scene_ui_panel_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/scene_ui_panel_fields/generated/fields.json", "resources/data/scene_ui_panel_fields.json", "data", "extension"),
    ResourceSpec("scene_audio_command_word_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/scene_audio_command_word_fields/generated/fields.json", "resources/audio/scene_audio_command_word_fields.json", "audio", "extension"),
    ResourceSpec("troop_movement_source_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/troop_movement_source_fields/generated/fields.json", "resources/data/troop_movement_source_fields.json", "data", "extension"),
    ResourceSpec("font_source_alias_fields", "tools.font_source_alias_fields.codec", "analysis/font_source_alias_fields/generated/fields.json", "resources/images/font_source_alias_fields.json", "images", "extension"),
    ResourceSpec("scene_coordinate_word_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/scene_coordinate_word_fields/generated/fields.json", "resources/data/scene_coordinate_word_fields.json", "data", "extension"),
    ResourceSpec("selected_tile_row_word_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/selected_tile_row_word_fields/generated/fields.json", "resources/images/selected_tile_row_word_fields.json", "images", "extension"),
    ResourceSpec("stage_cursor_sprite_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/stage_cursor_sprite_fields/generated/fields.json", "resources/images/stage_cursor_sprite_fields.json", "images", "extension"),
    ResourceSpec("ui_resource_word_sources", "tools.high_level_rom.resource_adapters_fields", "analysis/ui_resource_word_sources/generated/fields.json", "resources/data/ui_resource_word_sources.json", "data", "extension"),
    ResourceSpec("runtime_indexed_source_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/runtime_indexed_source_fields/generated/fields.json", "resources/data/runtime_indexed_source_fields.json", "data", "extension"),
    ResourceSpec("diplomacy_parameter_word_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/diplomacy_parameter_word_fields/generated/fields.json", "resources/data/diplomacy_parameter_word_fields.json", "data", "extension"),
    ResourceSpec("ui_state_dispatch_source_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/ui_state_dispatch_source_fields/generated/fields.json", "resources/data/ui_state_dispatch_source_fields.json", "data", "extension"),
    ResourceSpec("ui_runtime_source_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/ui_runtime_source_fields/generated/fields.json", "resources/data/ui_runtime_source_fields.json", "data", "extension"),
    ResourceSpec("render_selector_source_fields", "tools.render_selector_source_fields.codec", "analysis/render_selector_source_fields/generated/fields.json", "resources/data/render_selector_source_fields.json", "data", "extension"),
    ResourceSpec("battle_action_byte_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/battle_action_byte_fields/generated/fields.json", "resources/data/battle_action_byte_fields.json", "data", "extension"),
    ResourceSpec("battle_action_rng_word_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/battle_action_rng_word_fields/generated/fields.json", "resources/data/battle_action_rng_word_fields.json", "data", "extension"),
    ResourceSpec("state_dispatch_word_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/state_dispatch_word_fields/generated/fields.json", "resources/data/state_dispatch_word_fields.json", "data", "extension"),
    ResourceSpec("display_motion_source_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/display_motion_source_fields/generated/fields.json", "resources/data/display_motion_source_fields.json", "data", "extension"),
    ResourceSpec("menu_scalar_source_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/menu_scalar_source_fields/generated/fields.json", "resources/data/menu_scalar_source_fields.json", "data", "extension"),
    ResourceSpec("ui_selector_pair_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/ui_selector_pair_fields/generated/fields.json", "resources/data/ui_selector_pair_fields.json", "data", "extension"),
    ResourceSpec("counted_ui_row_sources", "tools.high_level_rom.resource_adapters_fields", "analysis/counted_ui_row_sources/generated/fields.json", "resources/data/counted_ui_row_sources.json", "data", "extension"),
    ResourceSpec("growth_threshold_word_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/growth_threshold_word_fields/generated/fields.json", "resources/data/growth_threshold_word_fields.json", "data", "extension"),
    ResourceSpec("compact_ui_sprite_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/compact_ui_sprite_fields/generated/fields.json", "resources/images/compact_ui_sprite_fields.json", "images", "extension"),
    ResourceSpec("ui_literal_parameter_sources", "tools.high_level_rom.resource_adapters_fields", "analysis/ui_literal_parameter_sources/generated/fields.json", "resources/data/ui_literal_parameter_sources.json", "data", "extension"),
    ResourceSpec("z80_startup_seed_fields", "tools.high_level_rom.resource_adapters_machine", "analysis/z80_startup_seed_fields/generated/fields.json", "resources/audio/z80_startup_seed_fields.json", "audio", "extension"),
    ResourceSpec("parameter_ui_word_sources", "tools.parameter_ui_word_sources.codec", "analysis/parameter_ui_word_sources/generated/fields.json", "resources/data/parameter_ui_word_sources.json", "data", "extension"),
    ResourceSpec("counted_ui_shared_sources", "tools.high_level_rom.resource_adapters_fields", "analysis/counted_ui_shared_sources/generated/fields.json", "resources/data/counted_ui_shared_sources.json", "data", "extension"),
    ResourceSpec("boot_queue_dispatch_source_fields", "tools.boot_queue_dispatch_source_fields.codec", "analysis/boot_queue_dispatch_source_fields/generated/fields.json", "resources/data/boot_queue_dispatch_source_fields.json", "data", "extension"),
    ResourceSpec("counted_glyph_source_fields", "tools.counted_glyph_source_fields.codec", "analysis/counted_glyph_source_fields/generated/fields.json", "resources/data/counted_glyph_source_fields.json", "data", "extension"),
    ResourceSpec("indexed_command_source_fields", "tools.indexed_command_source_fields.codec", "analysis/indexed_command_source_fields/generated/fields.json", "resources/data/indexed_command_source_fields.json", "data", "extension"),
    ResourceSpec("ui_tile_byte_alias_fields", "tools.ui_tile_byte_alias_fields.codec", "analysis/ui_tile_byte_alias_fields/generated/fields.json", "resources/images/ui_tile_byte_alias_fields.json", "images", "extension"),
    ResourceSpec("fm_sparse_alias_fields", "tools.fm_sparse_alias_fields.codec", "analysis/fm_sparse_alias_fields/generated/fields.json", "resources/audio/fm_sparse_alias_fields.json", "audio", "extension"),
    ResourceSpec("roster_pointer_source_alias_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/roster_pointer_source_alias_fields/generated/fields.json", "resources/data/roster_pointer_source_alias_fields.json", "data", "extension"),
    ResourceSpec("indexed_scalar_source_fields", "tools.indexed_scalar_source_fields.codec", "analysis/indexed_scalar_source_fields/generated/fields.json", "resources/data/indexed_scalar_source_fields.json", "data", "extension"),
    ResourceSpec("portrait_frontier_word_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/portrait_frontier_word_fields/generated/fields.json", "resources/images/portrait_frontier_word_fields.json", "images", "extension"),
    ResourceSpec("indexed_lowbank_source_alias_fields", "tools.high_level_rom.indexed_lowbank_source_alias_fields", "tools/high_level_rom/resource_sources/indexed_lowbank_source_alias_fields.json", "resources/data/indexed_lowbank_source_alias_fields.json", "data", "extension"),
    ResourceSpec("increment_selector_source_alias_fields", "tools.increment_selector_source_alias_fields.codec", "analysis/increment_selector_source_alias_fields/generated/fields.json", "resources/data/increment_selector_source_alias_fields.json", "data", "extension"),
    ResourceSpec("indexed_command_source_alias_fields", "tools.high_level_rom.resource_adapters_fields", "analysis/indexed_command_source_alias_fields/generated/fields.json", "resources/data/indexed_command_source_alias_fields.json", "data", "extension"),
    ResourceSpec("indexed_pair_source_alias_fields", "tools.indexed_pair_source_alias_fields.codec", "analysis/indexed_pair_source_alias_fields/generated/fields.json", "resources/data/indexed_pair_source_alias_fields.json", "data", "extension"),
    ResourceSpec("vdp_empty_marker_fields", "tools.high_level_rom.resource_adapters_maps", "analysis/vdp_empty_marker_fields/generated/fields.json", "resources/data/vdp_empty_marker_fields.json", "data", "extension"),
    ResourceSpec("terrain_neighbor_source_alias_fields", "tools.terrain_neighbor_source_alias_fields.codec", "analysis/terrain_neighbor_source_alias_fields/generated/fields.json", "resources/data/terrain_neighbor_source_alias_fields.json", "data", "extension"),
    ResourceSpec("rle_gap_source_alias_fields", "tools.rle_gap_source_alias_fields.codec", "analysis/rle_gap_source_alias_fields/generated/fields.json", "resources/data/rle_gap_source_alias_fields.json", "data", "extension"),
    ResourceSpec("battle_map_source_alias_fields", "tools.battle_map_source_alias_fields.codec", "analysis/battle_map_source_alias_fields/generated/fields.json", "resources/data/battle_map_source_alias_fields.json", "data", "extension"),
    ResourceSpec("duel_record_source_alias_fields", "tools.duel_record_source_alias_fields.codec", "analysis/duel_record_source_alias_fields/generated/fields.json", "resources/data/duel_record_source_alias_fields.json", "data", "extension"),
    ResourceSpec("city_neighbor_source_alias_fields", "tools.city_neighbor_source_alias_fields.codec", "analysis/city_neighbor_source_alias_fields/generated/fields.json", "resources/data/city_neighbor_source_alias_fields.json", "data", "extension"),
    ResourceSpec("cart_mirrored_tile_source_alias_fields", "tools.cart_mirrored_tile_source_alias_fields.codec", "analysis/cart_mirrored_tile_source_alias_fields/generated/fields.json", "resources/images/cart_mirrored_tile_source_alias_fields.json", "images", "extension"),
    ResourceSpec("indexed_transfer_source_alias_fields", "tools.indexed_transfer_source_alias_fields.codec", "analysis/indexed_transfer_source_alias_fields/generated/fields.json", "resources/data/indexed_transfer_source_alias_fields.json", "data", "extension"),
    ResourceSpec("camera_chunk_source_alias_fields", "tools.camera_chunk_source_alias_fields.codec", "analysis/camera_chunk_source_alias_fields/generated/fields.json", "resources/data/camera_chunk_source_alias_fields.json", "data", "extension"),
    ResourceSpec("initial_map_source_alias_fields", "tools.initial_map_source_alias_fields.codec", "analysis/initial_map_source_alias_fields/generated/fields.json", "resources/data/initial_map_source_alias_fields.json", "data", "extension"),
    ResourceSpec("scene_descriptor_source_alias_fields", "tools.scene_descriptor_source_alias_fields.codec", "analysis/scene_descriptor_source_alias_fields/generated/fields.json", "resources/data/scene_descriptor_source_alias_fields.json", "data", "extension"),
    ResourceSpec("conditional_scene_rle_source_fields", "tools.conditional_scene_rle_source_fields.codec", "analysis/conditional_scene_rle_source_fields/generated/fields.json", "resources/data/conditional_scene_rle_source_fields.json", "data", "extension"),
    ResourceSpec("scene_object_source_alias_fields", "tools.scene_object_source_alias_fields.codec", "analysis/scene_object_source_alias_fields/generated/fields.json", "resources/data/scene_object_source_alias_fields.json", "data", "extension"),
    ResourceSpec("object_motion_source_alias_fields", "tools.object_motion_source_alias_fields.codec", "analysis/object_motion_source_alias_fields/generated/fields.json", "resources/data/object_motion_source_alias_fields.json", "data", "extension"),
    ResourceSpec("object_residue_source_alias_fields", "tools.object_residue_source_alias_fields.codec", "analysis/object_residue_source_alias_fields/generated/fields.json", "resources/data/object_residue_source_alias_fields.json", "data", "extension"),
    ResourceSpec("object_id_source_alias_fields", "tools.object_id_source_alias_fields.codec", "analysis/object_id_source_alias_fields/generated/fields.json", "resources/data/object_id_source_alias_fields.json", "data", "extension"),
    ResourceSpec("fullword_scene_rle_source_fields", "tools.fullword_scene_rle_source_fields.codec", "analysis/fullword_scene_rle_source_fields/generated/fields.json", "resources/data/fullword_scene_rle_source_fields.json", "data", "extension"),
    ResourceSpec("scene_gap_rle_source_fields", "tools.scene_gap_rle_source_fields.codec", "analysis/scene_gap_rle_source_fields/generated/fields.json", "resources/data/scene_gap_rle_source_fields.json", "data", "extension"),
    ResourceSpec("sprite_records", "tools.high_level_rom.resource_adapters_sprite_palette", "analysis/sprite_records/generated/assets.json", "resources/images/sprite_records.json", "images", "base"),
)

LIMITS = (
    'ROM-independent encoding is not hardware/CPU/natural-path equivalence',
    'registered but unported resource codecs remain explicit unavailable',
    'source BYTE/operand meanings preserve their original candidate/unknown status',
    'code intersections require explicit business-source binding; no runtime clipping',
    'workspace default reads typed JSON; independent delivery must provide own source_root',
    'legacy pure graphics/portrait helpers must be included in a self-contained delivery',
)


def registry_rows():
    """Machine-readable fixed source/role registration without reading assets."""
    return [dict(id=spec.id, codec=spec.codec, source=spec.source,
                 own_source=spec.own_source, role=spec.role, chain=spec.chain)
            for spec in RESOURCE_SPECS]


def load_resources(source_root=None, ids=None, allow_unavailable=False):
    """Encode own typed sources and retain all unavailable/conflict boundaries.

    Return blocks[{id,start,end,data,owner,role}], unavailable, conflicts,
    coverage and limits. The caller may prepare an incomplete receipt, but
    must not emit a complete ROM if any authority is unavailable or conflicting.
    """
    declaration = json.loads(GEOMETRY.read_text(encoding='utf-8'))
    if declaration['format'] != 'g5510-ROM-independent-resource-geometry-v1':
        raise ValueError('independent resource geometry format differs')
    known = {spec.id: spec for spec in RESOURCE_SPECS}
    selected = list(known) if ids is None else list(ids)
    if len(selected) != len(set(selected)) or any(ident not in known for ident in selected):
        raise ValueError('explicit unique registered resource IDs required')
    root = None if source_root is None else Path(source_root).resolve()
    rows, unavailable, conflicts, packages = [], [], [], []
    for ident in selected:
        spec = known[ident]
        contract = declaration['contracts'][ident]
        path = PROJECT_ROOT / spec.source if root is None else root / spec.own_source
        if root is not None and not path.resolve().is_relative_to(root):
            raise ValueError('resource path leaves supplied own source root')
        intersection = contract.get('code_intersection')
        if intersection:
            report = dict(owner=ident, reason=intersection['disposition'],
                          spans=intersection['spans'], byte_count=intersection['bytes'],
                          kinds=intersection['kinds'], automatic_clip=False,
                          independent_resource_authority=False)
            conflicts.append(report)
            unavailable.append(dict(id=ident, source=str(path), reason='code/resource authority intersection',
                                    disposition=intersection['disposition'], fixed_spans=contract['spans']))
            continue
        if not contract['adapter']:
            unavailable.append(dict(id=ident, source=str(path),
                                    reason='ROM-dependent resource encoder not yet independently migrated',
                                    codec=spec.codec, classification=contract['confidence']))
            continue
        try:
            fields = load_source(path, root, ident)
            if fields.get('format') != contract['format']:
                raise ValueError('registered typed source format differs')
            adapter_module = contract.get('adapter_module')
            if adapter_module == 'tools.high_level_rom.resource_adapters_tiles':
                from . import resource_adapters_tiles
                encoder = getattr(resource_adapters_tiles, contract['adapter'])
            elif adapter_module == 'tools.high_level_rom.resource_adapters_scene':
                from . import resource_adapters_scene
                encoder = getattr(resource_adapters_scene, contract['adapter'])
            elif adapter_module == 'tools.high_level_rom.resource_adapters_maps':
                from . import resource_adapters_maps
                encoder = getattr(resource_adapters_maps, contract['adapter'])
            elif adapter_module == 'tools.high_level_rom.resource_adapters_machine':
                from . import resource_adapters_machine
                encoder = getattr(resource_adapters_machine, contract['adapter'])
            elif adapter_module == 'tools.high_level_rom.resource_adapters_records':
                from . import resource_adapters_records
                encoder = getattr(resource_adapters_records, contract['adapter'])
            elif adapter_module == 'tools.high_level_rom.resource_adapters_ui':
                from . import resource_adapters_ui
                encoder = getattr(resource_adapters_ui, contract['adapter'])
            elif adapter_module == 'tools.high_level_rom.resource_adapters_structure':
                from . import resource_adapters_structure
                encoder = getattr(resource_adapters_structure, contract['adapter'])
            elif adapter_module == 'tools.high_level_rom.resource_adapters_sprite_palette':
                from . import resource_adapters_sprite_palette
                encoder = getattr(resource_adapters_sprite_palette, contract['adapter'])
            elif adapter_module == 'tools.high_level_rom.resource_adapters_fields':
                from . import resource_adapters_fields
                encoder = getattr(resource_adapters_fields, contract['adapter'])
            elif adapter_module is None:
                encoder = getattr(adapters, contract['adapter'])
            else:
                raise ValueError('unregistered resource adapter module')
            generated = encoder(fields, contract)
            actual_spans = adapters.coalesced_spans(generated)
            if actual_spans != contract['spans']:
                raise ValueError('complete fixed own resource geometry differs')
            if not generated:
                raise ValueError('nonempty registered resource authority required')
            for row in generated:
                if row['end'] - row['start'] != len(row['data']):
                    raise ValueError('resource block width differs')
                rows.append(dict(row, owner=ident))
            packages.append(dict(id=ident, blocks=len(generated),
                                 bytes=sum(row['end']-row['start'] for row in generated),
                                 confidence=contract['confidence'],
                                 adapter=contract['adapter'], limits=contract.get('limits', [])))
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as error:
            unavailable.append(dict(id=ident, source=str(path), reason='independent resource generation failed',
                                    error=str(error), classification=contract['confidence']))
    # A shared physical byte is never silently equal-merged. Even a matching
    # duplicate needs an explicit alias contract and a single editable owner.
    ordered = sorted(rows, key=lambda row: (row['start'], row['end'], row['owner'], row['id']))
    active = []
    for row in ordered:
        active = [prior for prior in active if prior['end'] > row['start']]
        for prior in active:
            start, end = max(prior['start'], row['start']), min(prior['end'], row['end'])
            conflicts.append(dict(start=start, end=end, owners=[prior['owner'], row['owner']],
                                  ids=[prior['id'], row['id']], reason='duplicate physical resource authority',
                                  automatic_clip=False, equal_bytes_are_not_authority_proof=True))
        active.append(row)
    result = dict(blocks=ordered, unavailable=unavailable, conflicts=conflicts,
                  packages=packages,
                  coverage=dict(registered=len(RESOURCE_SPECS), selected=len(selected),
                                encoded_packages=len(packages), generated_blocks=len(ordered),
                                generated_bytes=sum(row['end']-row['start'] for row in ordered),
                                complete_selected_resources=not unavailable and not conflicts,
                                complete_resources=(len(selected) == len(RESOURCE_SPECS) and
                                                    not unavailable and not conflicts)),
                  limits=list(LIMITS), original_generation_input=False,
                  opaque_opcode_payload=False, complete_ROM=False,
                  declared_code_scope_BYTES=declaration['code_scope_BYTES'],
                  code_classification_missing_PCs=declaration['missing_code_size_PCs'])
    if not allow_unavailable and (unavailable or conflicts):
        raise ValueError('independent resources incomplete: ' + str(len(unavailable)) +
                         ' unavailable; ' + str(len(conflicts)) + ' conflicts')
    return result
