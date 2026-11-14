"""Explicit resource/code partition for the former 1170-byte alias package.

The new declaration owns only 1162 bytes. Two four-byte spans are references
to audio-driver code, never editable resource payloads. Encoding takes only a
supplied v2 declaration; migration is a separate, explicit in-memory step.
There is no ROM/file access, legacy fallback, byte clipping or CPU execution.

Confidence: the ownership transfer is confirmed by matched audio source and
the focused migration check. The remaining fragments' primary purposes and
natural indexed-reader input domains remain unknown. Conditional reader views
can cross source owners; their geometry does not create duplicate authority.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

from .image import ImageBlock, ImageError, validate_blocks


FORMAT = "g5510-indexed-lowbank-source-ownership-v2"
LEGACY_FORMAT = "g5510-indexed-lowbank-conditional-source-BYTE-aliases-v1"
OWNER = "indexed_lowbank_source_alias_fields"
RESOURCE_BYTES = 1162
ROLE = "conditional_indexed_source_alias_unknown_primary_purpose"

# Physical geometry, not payload or executable opcode storage.
RESOURCE_SPANS = (
    (0x1550, 0x1566), (0x1CDA, 0x1CEA), (0x204A, 0x2050),
    (0x2264, 0x2268), (0x24D4, 0x24DC), (0x395A, 0x3966),
    (0x39B0, 0x3A00), (0x3C66, 0x3CA6), (0x3D24, 0x3E48),
    (0x416E, 0x4178), (0x487C, 0x4890), (0x4A52, 0x4A54),
    (0x50BE, 0x50C6), (0x514A, 0x5164), (0x584A, 0x5864),
    (0x58DE, 0x58E4), (0x59C0, 0x59D8), (0x5AE6, 0x5AEE),
    (0x69B7, 0x69B8), (0x69D8, 0x69DA), (0x69ED, 0x69F2),
    (0x6A07, 0x6A0A), (0x6B94, 0x6B98), (0x6BF8, 0x6BF9),
    (0x6CC8, 0x6CD6), (0x6E9A, 0x6EB7), (0x6FB5, 0x6FC9),
    (0x70AE, 0x70DE), (0x7234, 0x7238), (0x76F7, 0x76FF),
    (0x7D34, 0x7D4D), (0x8089, 0x808A), (0x80D0, 0x80F4),
    (0xA81E, 0xA82E), (0xAAAC, 0xAAB4), (0xB40C, 0xB414),
    (0xB6E2, 0xB724), (0xBBD4, 0xBBDA), (0xBBF6, 0xBC00),
    (0xBC1C, 0xBC24), (0xBD66, 0xBD76), (0xDA7E, 0xDA8E),
    (0xDB10, 0xDB20), (0xE024, 0xE050), (0xE78F, 0xE790),
    (0xEC5C, 0xEC62), (0xEE0C, 0xEE16), (0xFA1A, 0xFA3A),
    (0xFA6A, 0xFA8A), (0xFAC0, 0xFAE0),
)
CODE_REFERENCES = ((0x7414, 0x7418, 0xA42, 0xA46),
                   (0x7556, 0x755A, 0xB84, 0xB88))


class SourceDeclarationError(ImageError):
    pass


class LegacyCodeEditError(SourceDeclarationError):
    """Legacy resource edits affect bytes now owned by real audio source."""


def _same(actual, expected, label):
    """Strict JSON shape/type equality, including bool versus int."""
    if type(actual) is not type(expected):
        raise SourceDeclarationError(f"{label}: strict type differs")
    if type(expected) is dict:
        if set(actual) != set(expected):
            raise SourceDeclarationError(f"{label}: keys differ")
        for key in expected:
            _same(actual[key], expected[key], label + "." + key)
    elif type(expected) is list:
        if len(actual) != len(expected):
            raise SourceDeclarationError(f"{label}: list size differs")
        for index, value in enumerate(expected):
            _same(actual[index], value, label + f"[{index}]")
    elif actual != expected:
        raise SourceDeclarationError(f"{label}: fixed value differs")


def _keys(value, names, label):
    if type(value) is not dict or set(value) != set(names):
        raise SourceDeclarationError(f"{label}: exact declaration keys required")


def _byte_payload(values, size, label):
    if type(values) is not list or len(values) != size:
        raise SourceDeclarationError(f"{label}: fixed BYTE count differs")
    for value in values:
        if type(value) is not int or not 0 <= value <= 255:
            raise SourceDeclarationError(f"{label}: full-width integer BYTE required")
    return bytes(values)


def _legacy_id(start, end):
    return f"rom_{start:06X}_{end:06X}_conditional_source_BYTEs"


def _source_fixed(start, end):
    return {"id": _legacy_id(start, end), "start": start, "end": end,
            "bytes": end - start, "one_physical_edit_authority": True,
            "original_fragment_business_role": "unknown"}


def _reference_rows():
    return [{"legacy_source_id": _legacy_id(start, end), "start": start,
             "end": end, "bytes": end - start, "owner": "audio_driver",
             "role": "code", "image": "driver", "logical_start": logical_start,
             "logical_end": logical_end, "editable_resource_bytes": 0,
             "ownership_confidence": "confirmed", "natural_return_domain": "unknown"}
            for start, end, logical_start, logical_end in CODE_REFERENCES]


def _metadata():
    return {
        "format": FORMAT, "owner": OWNER, "resource_bytes": RESOURCE_BYTES,
        "role": ROLE, "coordinate_system": "linear BIN physical offsets",
        "ownership_confidence": "confirmed", "primary_purpose_confidence": "unknown",
        "code_references": _reference_rows(),
        "reader_views": {
            "pattern": {"read_PC": 0x690, "source_base": 0x696,
                        "read_width_bytes": 4,
                        "index_formula": "s16(u16(already_fetched_F6C4_WORD << 2))",
                        "complete_in_ROM_window_union": [2, 0x8696],
                        "conditional_read_confidence": "confirmed",
                        "natural_selector_domain": "unknown"},
            "curve": {"read_PC": 0x94BE, "source_base": 0x94CA,
                      "read_width_bytes": 2, "reads_per_entered_window": 11,
                      "captured_index_before_memory_SUBQ2": True,
                      "F61A_SUBQ1_then_BPL_stop": True, "F618_BMI_stop": True,
                      "complete_constructed_window_union": [0x94CA, 0x114DE],
                      "conditional_read_confidence": "confirmed",
                      "natural_selector_domain": "unknown"},
            "physical_ownership": "source views do not create physical edit owners",
            "cross_owner_windows": "read live from the assembled image, including code and other resource owners",
            "selector_clamping": False, "copy_window_neighbors_into_this_source": False,
        },
        "provenance": {
            "legacy_fields": "analysis/indexed_lowbank_source_alias_fields/generated/fields.json",
            "legacy_codec": "tools/indexed_lowbank_source_alias_fields/codec.py",
            "legacy_format": LEGACY_FORMAT, "legacy_physical_bytes": 1170,
            "legacy_sources": 52, "resource_sources": 50, "transferred_code_bytes": 8,
            "source_id_mapping": "unchanged legacy source IDs for retained allocations; removed IDs are code_references only",
            "audio_source_package": "tools/high_level_audio_engine",

            "runtime_old_fields_dependency": False, "runtime_ROM_dependency": False,
        },
        "limits": {"CPU_execution": False, "new_semantic_classification": False,
                   "natural_gameplay_proof": False, "primary_purposes": "unknown",
                   "legacy_code_edits": "explicit migration rejects values unlike supplied audio-code authority",
                   "runtime_payload_clipping": False},
    }


def encode(document) -> tuple[ImageBlock, ...]:
    """Encode only the v2 source's 50 complete resource allocations.

    A v1 input is an error, not a request to discard eight editable bytes.
    Code references contain no payload and are validated as immutable geometry.
    """
    metadata = _metadata()
    _keys(document, set(metadata) | {"sources"}, "v2 source")
    for key, expected in metadata.items():
        if key == "provenance":
            source = {k: v for k, v in document[key].items()
                      if k not in ("audio_source_match", "transfer_evidence")}
            _same(source, expected, "v2 source.provenance")
        else:
            _same(document[key], expected, "v2 source." + key)
    sources = document["sources"]
    if type(sources) is not list or len(sources) != len(RESOURCE_SPANS):
        raise SourceDeclarationError("exactly 50 resource allocations required")
    blocks = []
    for row, (start, end) in zip(sources, RESOURCE_SPANS):
        fixed = _source_fixed(start, end)
        _keys(row, set(fixed) | {"BYTEs"}, "resource allocation")
        for key, expected in fixed.items():
            _same(row[key], expected, "resource allocation." + key)
        data = _byte_payload(row["BYTEs"], end - start, row["id"])
        blocks.append(ImageBlock(start, data, OWNER, ROLE))
    result = validate_blocks(blocks)
    if sum(len(block.data) for block in result) != RESOURCE_BYTES:
        raise SourceDeclarationError("1162-byte resource geometry differs")
    return result


def _legacy_metadata():
    """Fixed v1 header for explicit migration, not a generation dependency."""
    return {
        "format": LEGACY_FORMAT,
        "canonical_source": {"size": 0x100000, "sha256": reference_value(__name__, '_legacy_metadata')},
        "source_confidence": "confirmed_conditional_original_reads", "confidence": "candidate",
        "executable_code_added": 0, "recovered_functions_added": 0, "owner_bytes_added": 0,
        "natural_domains_added": 0, "complete_domains_added": 0,
        "original_business_and_code_purpose": "unknown", "natural_input_domains": "unknown",
        "evidence": {
            "frozen87_layout": reference_value(__name__, '_legacy_metadata_2'),
            "bank0_sha256": reference_value(__name__, '_legacy_metadata_3'),
            "pattern": {"prefix_start": 0x68A, "prefix_end": 0x696, "read_PC": 0x690,
                        "source_base": 0x696, "index": "s16(u16(already_fetched_F6C4_WORD<<2))",
                        "complete_in_ROM_window_union": [2, 0x8696], "new_raw_BYTES": 843},
            "curve": {"prefix_start": 0x949E, "prefix_end": 0x94CA, "read_PC": 0x94BE,
                      "captured_index_before_memory_SUBQ2": True, "timer_WORD_supplied": 0,
                      "original_timer_BPL_stop": True, "original_index_BMI_stop": True,
                      "constructed_positive_even_index_WORDs": True, "reads_per_window": 11,
                      "source_base": 0x94CA, "complete_window_union": [0x94CA, 0x114DE],
                      "new_lowbank_raw_BYTES": 327, "physical_bank0_emit_only": True,
                      "following_oldtyped_sources_not_emitted": True}},
        "supplied_values_not_natural_writer_proof": True, "oldtyped_neighbors_emitted_again": False,
        "CPU_hardware_RAM_CCR_stack": "not executed", "independent_CPU_comparison": False,
    }


def migrate_legacy(legacy_document, transferred_code_blocks) -> dict:
    """Migrate a supplied v1 document without losing any legacy BYTE edits.

    Retained resource values are copied exactly. The two removed allocations
    must equal explicitly supplied, generated audio-driver code blocks. If not,
    migration refuses; editing those bytes now requires editing audio source.
    This function does not encode or discover audio code and never reads files.
    """
    fixed_metadata = _legacy_metadata()
    _keys(legacy_document, set(fixed_metadata) | {"sources"}, "legacy source")
    for key, expected in fixed_metadata.items():
        _same(legacy_document[key], expected, "legacy source." + key)
    all_spans = sorted(RESOURCE_SPANS + tuple((start, end) for start, end, _, _ in CODE_REFERENCES))
    sources = legacy_document["sources"]
    if type(sources) is not list or len(sources) != len(all_spans):
        raise SourceDeclarationError("complete legacy 52-allocation document required")
    code = validate_blocks(transferred_code_blocks)
    expected_code_spans = [(start, end) for start, end, _, _ in CODE_REFERENCES]
    if [(block.start, block.end) for block in code] != expected_code_spans:
        raise SourceDeclarationError("supply exactly the two complete transferred audio-code allocations")
    if any(block.owner != "audio_driver" or block.role != "code" for block in code):
        raise SourceDeclarationError("transferred allocations require explicit audio_driver/code authority")
    code_values = {(block.start, block.end): block.data for block in code}
    resources = []
    for row, (start, end) in zip(sources, all_spans):
        fixed = _source_fixed(start, end)
        _keys(row, set(fixed) | {"BYTEs"}, "legacy allocation")
        for key, expected in fixed.items():
            _same(row[key], expected, "legacy allocation." + key)
        data = _byte_payload(row["BYTEs"], end - start, row["id"])
        if (start, end) in code_values:
            if data != code_values[(start, end)]:
                raise LegacyCodeEditError(f"legacy editable {row['id']} differs from audio_driver source; no silent transfer")
        else:
            resources.append({**fixed, "BYTEs": list(data)})
    document = {**_metadata(), "sources": resources}
    encode(document)
    return document
