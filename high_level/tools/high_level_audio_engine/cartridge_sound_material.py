"""Compose real Z80 bank DATA from the same explicit whole-cartridge source.

This is a fresh-construction adapter, not an opcode interpreter or a resource
fallback.  The five curated audio packages are still loaded and checked; their
classification cannot truncate the actual cartridge's 32 KiB bank window.
"""
from .owned_runtime import OwnedSoundMaterial, OWN_RESOURCE_IDS
from ..high_level_main_flows.cartridge_source_data import CartridgeSourceData, CARTRIDGE_END
from ..high_level_scene_flows.domain import Boundary, ReadOnlyData


def compose_cartridge_sound_material(source, selected):
    """Borrow the same full readonly authority before any Audio/Scene owner.

    Keep the old selected material's five resource contracts and empty RAM
    projection intact.  No bytes are merged, zero-filled, loaded again, copied
    into sound RAM or substituted after a driver has started.
    """
    if type(source) is not CartridgeSourceData or type(source.data) is not ReadOnlyData:
        raise ValueError('the actual complete typed cartridge source is required')
    if (type(selected) is not OwnedSoundMaterial or type(selected.data) is not ReadOnlyData
            or selected.resource_ids != OWN_RESOURCE_IDS or selected.ram_segments != ()):
        raise ValueError('the five exact fresh audio packages without host RAM projection are required')
    if (len(source.data.segments) != 1 or source.data.segments[0][0] != 0
            or len(source.data.segments[0][1]) != CARTRIDGE_END):
        raise Boundary('bank material requires the complete existing source partition, not filled holes')
    evidence = source.evidence
    if (type(evidence) is not dict
            or evidence.get('format') != 'g5510-explicit-complete-cartridge-source-DATA-v1'
            or evidence.get('original_ROM_or_bank_input') is not False
            or evidence.get('analysis_opcode_payload_input') is not False
            or evidence.get('sparse_padding_selected') is not False):
        raise Boundary('complete explicit source provenance is required for cartridge bank reads')
    partition = evidence.get('whole_cartridge')
    if partition != dict(start=0, end=CARTRIDGE_END, bytes=CARTRIDGE_END,
            exact_partition=True, holes=0, competing_bytes=0):
        raise Boundary('exact full source partition evidence differs')
    registered = evidence.get('registered_DATA')
    if (type(registered) is not dict or registered.get('packages') != 128
            or not set(OWN_RESOURCE_IDS).issubset(registered.get('resource_ids', ()))):
        raise Boundary('the full registered source must retain all five selected audio contracts')
    encoded = sum(len(raw) for base, raw in selected.data.segments)
    if type(selected.encoded_bytes) is not int or selected.encoded_bytes != encoded or not encoded:
        raise ValueError('exact selected audio encoded-byte count required')
    payload = source.data.segments[0][1]
    for base, raw in selected.data.segments:
        if base + len(raw) > CARTRIDGE_END or payload[base:base + len(raw)] != raw:
            raise Boundary('selected audio package differs from the same complete cartridge source at ' + hex(base))
    material = OwnedSoundMaterial(source.data, selected.ram_segments,
        selected.resource_ids, selected.encoded_bytes)
    return material, dict(
        confidence='confirmed_fresh_source_composition_only_not_new_runtime_acceptance',
        authority='same complete typed cartridge ReadOnlyData used by the Scene',
        physical_range=[0, CARTRIDGE_END], bank_read_authority_bytes=CARTRIDGE_END,
        selected_audio_resource_ids=list(selected.resource_ids),
        selected_audio_encoded_DATA_bytes=selected.encoded_bytes,
        selected_audio_segments=len(selected.data.segments),
        selected_audio_bytes_checked_against_complete_source=encoded,
        same_ReadOnlyData_identity=True, five_selected_audio_contracts_preserved=True,
        unchanged_empty_RAM_projection=True, constructor_device_type_unchanged=True,
        copied_or_filled_cartridge_bytes=0, runtime_material_hot_swap=False,
        instruction_fetch_or_CPU_execution=False, source_classification_is_not_a_hardware_bank_limit=True,
        out_of_cartridge_reads_remain_original_Boundary=True,
        original_ROM_or_reference_audio_input=False, formal_new_CODE_bytes=0)
