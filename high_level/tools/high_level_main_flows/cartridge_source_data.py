"""Compose an explicit editable cartridge source view for original DATA reads.

The original cold 00300 checksum really reads the full cartridge body. This
module owns no ROM, reference bytes or opcode execution. It selects only real
instruction extents from explicitly named current-source-matched own builds,
plus all independently encoded registered DATA. Sparse object padding is never
an authority, and competing/missing source bytes remain errors.
"""
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from tools.code_analysis.m68k_code_map import load_capstone
from tools.m68k_build.elf_verify import verify_object
from tools.m68k_build.source import format_instruction
from tools.high_level_main_flows.compiled_copy_data import (
    M68kCopyAuthority, _owned_member, _layout_records, _source_instructions,
)
from tools.high_level_main_flows.resource_manifest import load_scene_source_manifest
from tools.high_level_audio_engine.compiled_program_data import load_compiled_sound_copy_data
from tools.high_level_rom.resource_registry import RESOURCE_SPECS
from tools.high_level_scene_flows.domain import ReadOnlyData


CARTRIDGE_END = 0x100000
CHECKSUM_START = 0x200


@dataclass(frozen=True)
class CartridgeSourceData:
    """Read-only cartridge authority, not a CPU or a completed cold boot."""
    data: ReadOnlyData
    evidence: dict


def project_cartridge_m68k_authorities() -> tuple[M68kCopyAuthority, ...]:
    """Describe the twelve relative source/build pairs; do not select a root.

    This table reads no file. A caller must explicitly pass its source root,
    the returned descriptions, a sound build/source mapping and a DATA manifest.
    Existing strict instruction-only source/object helpers are reused without
    changing their admission contract or the narrow6950 copy loader.
    """
    rows = (
        ('recovered_code.s', 'm68k_build', 'csv', 'm68k_code'),
        ('candidate_filter.s', 'candidate_source', 'csv', 'm68k_candidate_code'),
        ('candidate_action.s', 'candidate_action_source', 'csv', 'm68k_action_code'),
        ('candidate_handler_818.s', 'candidate_handler_source', 'csv', 'm68k_handler_code'),
        ('candidate_handler_49e.s', 'candidate_handler_49e_source', 'csv', 'm68k_handler49e_code'),
        ('candidate_handler_9b0.s', 'candidate_handler_9b0_source', 'csv', 'm68k_handler9b0_code'),
        ('candidate_handler_c26.s', 'candidate_handler_c26_source', 'csv', 'm68k_handlerc26_code'),
        ('direct_descendants.s', 'direct_code', 'json', 'm68k_direct_code'),
        ('dispatch_descendants.s', 'dispatch_code', 'json', 'm68k_dispatch_code'),
        ('final_dispatch_descendants.s', 'final_dispatch_code', 'json', 'm68k_final_dispatch_code'),
        ('nested_dispatch_descendants.s', 'nested_dispatch_code', 'json', 'm68k_nested_dispatch_code'),
        ('secondary_dispatch_descendants.s', 'secondary_dispatch_code', 'json', 'm68k_secondary_dispatch_code'),
    )
    return tuple(M68kCopyAuthority(
        Path('src/m68k') / source,
        Path('analysis') / ledger / 'generated' / ('instructions.' + suffix),
        Path('build') / (stem + '.o'), Path('build') / (stem + '.bin'),
    ) for source, ledger, suffix, stem in rows)


def _joined(segments):
    """Join only already-owned adjacency; never fill gaps or equal-merge."""
    joined = []
    for address, raw in sorted(segments):
        if joined:
            previous, payload = joined[-1]
            end = previous + len(payload)
            if address < end:
                raise ValueError('competing cartridge source ownership at ' + hex(address))
            if address == end:
                joined[-1] = previous, payload + raw
                continue
        joined.append((address, raw))
    return ReadOnlyData(tuple(joined))


def _load_all_m68k(source_root, authorities):
    if not isinstance(source_root, Path) or not source_root.is_dir():
        raise ValueError('explicit existing M68K editable source/build root required')
    source_root = source_root.resolve()
    if (type(authorities) is not tuple or len(authorities) != 12
            or any(type(authority) is not M68kCopyAuthority for authority in authorities)):
        raise ValueError('twelve explicit typed M68K source/build authorities required')
    capstone = load_capstone()
    decoder = capstone.Cs(capstone.CS_ARCH_M68K,
        capstone.CS_MODE_BIG_ENDIAN | capstone.CS_MODE_M68K_000)
    decoder.detail = True
    chunks, evidence = [], []
    for authority in authorities:
        source = _owned_member(source_root, authority.source)
        ledger = _owned_member(source_root, authority.layout_ledger)
        object_path = _owned_member(source_root, authority.native_object)
        image_path = _owned_member(source_root, authority.native_image)
        try:
            records = _layout_records(ledger)
            # Whole source topology and every object label are checked, not
            # a signature or old file-size/cache marker. Historical ledger
            # bytes and opcode comments are not used as input.
            instructions = _source_instructions(source, records)
            image = image_path.read_bytes()
            actual_text = verify_object(object_path.read_bytes(), records)
            if (actual_text != image
                    or len(image) != records[-1]['address'] + records[-1]['size']):
                raise ValueError('explicit object .text and existing image differ')
            for row in records:
                address, width = row['address'], row['size']
                raw = image[address:address + width]
                decoded = list(decoder.disasm(raw, address, count=1))
                if len(decoded) != 1 or decoded[0].size != width:
                    raise ValueError('compiled instruction boundary differs at ' + hex(address))
                canonical = ' '.join(format_instruction(decoded[0]).split())
                if canonical != instructions[address]:
                    raise ValueError('current editable instruction differs at ' + hex(address)
                        + ': source=' + instructions[address] + ' cache=' + canonical)
                # Every selected raw BYTE lies in one actual full instruction.
                # The rest of the sparse .text/image is deliberately omitted.
                chunks.append((address, raw))
            evidence.append(dict(source=str(source), layout_ledger=str(ledger),
                native_object=str(object_path), native_image=str(image_path),
                layout_fields_read=['address', 'size'], instructions=len(records),
                CODE_bytes=sum(row['size'] for row in records),
                complete_current_mnemonics_and_operands_match=True,
                complete_source_topology_and_object_labels_match=True,
                sparse_padding_selected=False))
        except (ValueError, TypeError, KeyError, OSError) as error:
            raise ValueError('M68K source authority ' + str(authority.source) + ': ' + str(error)) from error
    data = _joined(chunks)
    total = sum(len(raw) for base, raw in data.segments)
    if total != 200522:
        raise ValueError('complete current M68K instruction extent must be200522 bytes')
    return data, dict(authorities=evidence, instructions=sum(row['instructions'] for row in evidence),
        CODE_bytes=total, disassembler='Capstone ' + capstone.__version__)


def load_cartridge_source_data(source_root: Path, *,
        m68k_authorities: tuple[M68kCopyAuthority, ...],
        sound_native_root: Path, sound_logical_sources: Mapping[str, str],
        resource_manifest: Path) -> CartridgeSourceData:
    """Return exact one-MiB own-source view for genuine game COPY/checksum reads.

    No implicit project/private location, reference cartridge, rebuilt bank,
    compiler invocation, hash or precomputed game checksum is selected. The
    sound loader compares every complete normalized current logical module
    with its explicit build snapshot. The DATA loader uses its existing typed
    codecs. Any unknown/source mismatch is an exception, without a fallback.

    This function does not execute, skip or replace the original ADD.W loop,
    cold hardware setup, RAM clear, sound reset or any other game software.
    """
    m68k, code_evidence = _load_all_m68k(source_root, m68k_authorities)
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
        native_rebuilds=0, hashes_computed=0, new_formal_CODE_bytes=0,
        limits=['readonly original copy/checksum source, not executable opcode interpretation',
                'partition/current-source correspondence is not checksum or cold boot success',
                'resource confidence and draft/unknown business semantics are unchanged',
                'hardware reset, clocks, stack banks and DMA scheduling remain explicit caller responsibilities']))
