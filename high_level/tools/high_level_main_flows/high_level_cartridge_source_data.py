"""Compose cartridge DATA from the editable high-level build, not legacy ASM.

The game still executes its own cartridge checksum and program-copy routines.
Compiled instructions are read-only source material for those reads, never an
opcode interpreter. Nothing here builds native code or repairs missing bytes.
"""
from collections.abc import Mapping
from pathlib import Path

from .cartridge_source_data import (
    CARTRIDGE_END, CHECKSUM_START, CartridgeSourceData, _joined,
)
from .resource_manifest import load_scene_source_manifest
from ..high_level_audio_engine.rom_build_program_data import load_current_sound_copy_data as load_compiled_sound_copy_data
from ..high_level_rom.compiled_code_data import load_high_level_m68k_copy_data
from ..high_level_rom.resource_registry import RESOURCE_SPECS


def load_cartridge_source_data(source_root: Path, *, m68k_native_root: Path,
        sound_native_root: Path, sound_logical_sources: Mapping[str, str],
        resource_manifest: Path) -> CartridgeSourceData:
    """Select one exact MiB from current high-level CODE and typed resources.

    All roots are caller choices. The M68K loader compares current whole source
    modules, generated instruction source, labels and actual instructions with
    the supplied high-level build. Sound accepts one complete current grouped
    or flat build with its corresponding whole-source contract. A stale, incomplete or competing
    source is an error; there is no legacy assembly, ROM or zero-fill fallback.

    Source correspondence is not behavioral acceptance. This function neither
    computes the game checksum nor executes any reset, copy or game operation.
    """
    m68k, code_evidence = load_high_level_m68k_copy_data(source_root, m68k_native_root)
    sound = load_compiled_sound_copy_data(sound_native_root, sound_logical_sources)
    if sound.instruction_bytes != 3380:
        raise ValueError('complete current startup/driver instruction extent must be3380 bytes')
    assets = load_scene_source_manifest(resource_manifest)
    expected = {spec.id for spec in RESOURCE_SPECS}
    if len(expected) != 128 or set(assets.resource_ids) != expected:
        raise ValueError('all128 registered independent typed DATA owners required exactly once')
    if assets.encoded_bytes != 844674:
        raise ValueError('complete registered DATA geometry must be844674 bytes')
    owned = sorted((base, base + len(raw), kind) for kind, view in (
        ('M68K_CODE', m68k), ('Z80_CODE', sound.data), ('registered_DATA', assets.data),
    ) for base, raw in view.segments)
    cursor = 0
    for start, end, kind in owned:
        if start != cursor:
            reason = 'hole' if start > cursor else 'competing ownership'
            raise ValueError('cartridge ' + reason + ' at ' + hex(min(start, cursor))
                + '; next=' + hex(start) + '..' + hex(end) + ' ' + kind)
        cursor = end
    if cursor != CARTRIDGE_END:
        raise ValueError('cartridge source must end exactly at100000, not ' + hex(cursor))
    data = _joined([segment for view in (m68k, sound.data, assets.data) for segment in view.segments])
    if len(data.segments) != 1 or data.segments[0][0] != 0:
        raise ValueError('exact full source partition required without implicit gap filling')
    # Retain the typed cartridge contract consumed by the original same-source
    # audio compositor. Both current-source producers are selected before any Scene exists.
    return CartridgeSourceData(data, dict(
        format='g5510-explicit-complete-cartridge-source-DATA-v1',
        confidence='confirmed_current_source_correspondence_and_partition_only',
        source_root=str(source_root.resolve()), resource_manifest=str(resource_manifest.resolve()),
        whole_cartridge=dict(start=0, end=CARTRIDGE_END, bytes=CARTRIDGE_END,
            exact_partition=True, holes=0, competing_bytes=0),
        original_checksum_body=dict(start=CHECKSUM_START, end=CARTRIDGE_END,
            bytes=CARTRIDGE_END-CHECKSUM_START, big_endian_WORD_reads=(CARTRIDGE_END-CHECKSUM_START)//2,
            host_checksum_calculated=False, original_ADD_W_required=True),
        m68k=code_evidence,
        z80=dict(native_source_root=str(sound.native_source_root.resolve()),
            current_whole_normalized_modules=len(sound.admitted_source_modules),
            current_logical_sources=list(sound.admitted_source_modules),
            CODE_bytes=sound.instruction_bytes),
        registered_DATA=dict(packages=len(assets.resource_ids), bytes=assets.encoded_bytes,
            resource_ids=list(assets.resource_ids), package_confidence=list(assets.package_confidence)),
        selected_authority_intervals=len(owned), original_ROM_or_bank_input=False,
        analysis_opcode_payload_input=False, sparse_padding_selected=False,
        legacy_M68K_assembly_authorities_selected=False,
        m68k_native_root=str(m68k_native_root.resolve()),
        native_rebuilds=0, hashes_computed=0, new_formal_CODE_bytes=0,
        limits=['readonly original copy/checksum source, not executable opcode interpretation',
                'partition/current-source correspondence is not checksum or cold boot success',
                'resource confidence and draft/unknown business semantics are unchanged',
                'hardware reset, clocks, stack banks and DMA scheduling remain explicit caller responsibilities']))
