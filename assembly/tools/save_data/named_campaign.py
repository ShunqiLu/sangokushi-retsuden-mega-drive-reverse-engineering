"""Pure named views and explicit edits of decoded campaign-save fixed segments.

``save_format`` remains the only storage-layout and bit-stream authority. Values
here are stored codes, not a reconstructed full RAM image. No function reads or
writes a file, supplies gameplay defaults, or synchronizes related attributes.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
from typing import Any

from . import save_format


FORMAT = "g5510-named-campaign-v1"
EDIT_FORMAT = "g5510-named-campaign-edits-v1"


class NamedCampaignError(save_format.SaveFormatError):
    """A named view or edit violates its explicit stored-value contract."""


# These names describe confirmed consumers, not additional save-format fields.
# Their widths, counts, source strides and transforms come only from SegmentSpec.
# Neutral operation roles follow high_level_rom.scenario_sources.NAMED_FIELDS
# and its cited original consumers. In particular B400 is a weighting operand;
# no formal UI name is asserted. The B800 field remains its saved DIVU quotient.
GROUP_FIELDS = {
    "cities": (
        ("gold", "ram_e000"),
        ("rice", "ram_e0a0"),
        ("income_base", "ram_e140"),
        ("development", "ram_e1e0"),
        ("income_split", "ram_e280"),
        ("welfare", "ram_e320"),
        ("income_rate", "ram_e3c0"),
        ("defense", "ram_e5a0"),
        ("force_index_code", "ram_f428"),
        ("representative_officer_code", "ram_f460"),
    ),
    "forces": (
        ("representative_officer_code", "ram_e640"),
    ),
    "officers": (
        ("readiness_current", "ram_b200"),
        ("combat_weighting_operand", "ram_b400"),
        ("intelligence", "ram_b600"),
        ("troop_capacity_base_div5_code", "derived_b800_div5"),
        ("combat_growth_score", "ram_c000"),
        ("intelligence_growth_score", "ram_be00"),
        ("virtue", "ram_c200"),
        ("education_rating", "ram_c300"),
        ("movement_factor", "ram_c400"),
        ("training_percent", "ram_c500"),
        ("class_status_flags", "ram_c700"),
        ("troop_count", "ram_c800"),
        ("assigned_city_code", "ram_cc00"),
    ),
}


def _keys(value: Any, expected: Any, context: str) -> None:
    if type(value) is not dict or set(value) != set(expected):
        raise NamedCampaignError(f"{context}: exact object fields required")


def _uint(value: Any, bits: int, context: str) -> int:
    if type(value) is not int or not 0 <= value < (1 << bits):
        raise NamedCampaignError(f"{context}: unsigned {bits}-bit integer required")
    return value


def _same(left: Any, right: Any) -> bool:
    """Compare immutable descriptors without accepting bool as integer metadata."""
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(
            _same(left[key], right[key]) for key in left
        )
    if type(left) is list:
        return len(left) == len(right) and all(
            _same(a, b) for a, b in zip(left, right)
        )
    return left == right


def _placements() -> dict[str, tuple[str, str]]:
    return {
        segment_id: (group, field)
        for group, fields in GROUP_FIELDS.items()
        for field, segment_id in fields
    }


def _storage_catalog() -> dict[str, dict[str, Any]]:
    placements = _placements()
    return {
        spec.segment_id: {
            **asdict(spec),
            "named_field": (
                {"group": placements[spec.segment_id][0],
                 "field": placements[spec.segment_id][1]}
                if spec.segment_id in placements else None
            ),
        }
        for spec in save_format.FIXED_SEGMENTS
    }


def _group_count(group: str) -> int:
    counts = {
        save_format.SEGMENT_BY_ID[segment_id].record_count
        for _, segment_id in GROUP_FIELDS[group]
    }
    if len(counts) != 1 or None in counts:
        raise NamedCampaignError(f"{group}: named source geometry is inconsistent")
    return next(iter(counts))


def _value_geometry(spec: save_format.SegmentSpec) -> tuple[int, int]:
    if spec.encoding == "raw":
        return spec.encoded_length, 8
    if (
        spec.encoding == "generic_lsb_bitpack"
        and spec.record_count is not None
        and spec.bit_width is not None
    ):
        return spec.record_count, spec.bit_width
    raise NamedCampaignError(f"{spec.segment_id}: unsupported explicit segment form")


def _values(value: Any, spec: save_format.SegmentSpec) -> list[int]:
    count, bits = _value_geometry(spec)
    if type(value) is not list or len(value) != count:
        raise NamedCampaignError(f"{spec.segment_id}: exactly {count} values required")
    for index, item in enumerate(value):
        _uint(item, bits, f"{spec.segment_id}[{index}]")
    return value


def _source_bytes(source: Any) -> bytes | None:
    if type(source) is not dict or type(source.get("kind")) is not str:
        raise NamedCampaignError("source: explicit origin object required")
    if source["kind"] == "decoded_fixed_segments":
        _keys(source, ("kind",), "decoded source")
        return None
    if source["kind"] != "exact_logical_baseline":
        raise NamedCampaignError("source: unsupported origin kind")
    _keys(source, ("kind", "logical_hex"), "logical source")
    text = source["logical_hex"]
    if (
        type(text) is not str
        or len(text) != save_format.LOGICAL_SIZE * 2
        or any(character not in "0123456789abcdef" for character in text)
    ):
        raise NamedCampaignError("source: exact canonical logical-image hex required")
    return bytes.fromhex(text)


def from_fixed_segments(decoded: dict[str, list[int]]) -> dict[str, Any]:
    """Organize every explicit decoded segment; raw segments are BYTE lists.

    Generic values can be supplied from the existing ``*.values.json`` values
    arrays. Supply every raw BYTE explicitly as well. No defaults, decoding or
    logical-image binding are performed by this function.
    """
    _keys(decoded, save_format.SEGMENT_BY_ID, "decoded fixed segments")
    for spec in save_format.FIXED_SEGMENTS:
        _values(decoded[spec.segment_id], spec)
    result: dict[str, Any] = {
        "format": FORMAT,
        "source": {"kind": "decoded_fixed_segments"},
        "storage": _storage_catalog(),
    }
    for group, fields in GROUP_FIELDS.items():
        result[group] = [
            {"record_index": index,
             "fields": {field: decoded[segment_id][index]
                        for field, segment_id in fields}}
            for index in range(_group_count(group))
        ]
    placements = _placements()
    result["remaining_segments"] = {
        spec.segment_id: list(decoded[spec.segment_id])
        for spec in save_format.FIXED_SEGMENTS
        if spec.segment_id not in placements
    }
    return result


def to_fixed_segments(named: dict[str, Any]) -> dict[str, list[int]]:
    """Validate a complete view and recover its sole editable stored values."""
    _keys(named, ("format", "source", "storage", "remaining_segments", *GROUP_FIELDS),
          "named campaign")
    if type(named["format"]) is not str or named["format"] != FORMAT:
        raise NamedCampaignError("unsupported named campaign format")
    _source_bytes(named["source"])
    if not _same(named["storage"], _storage_catalog()):
        raise NamedCampaignError("storage descriptors or named source bindings changed")
    decoded: dict[str, list[int]] = {}
    for group, fields in GROUP_FIELDS.items():
        rows = named[group]
        count = _group_count(group)
        if type(rows) is not list or len(rows) != count:
            raise NamedCampaignError(f"{group}: exactly {count} storage records required")
        for _, segment_id in fields:
            decoded[segment_id] = []
        for index, row in enumerate(rows):
            _keys(row, ("record_index", "fields"), f"{group}[{index}]")
            if type(row["record_index"]) is not int or row["record_index"] != index:
                raise NamedCampaignError(f"{group}: storage record order changed")
            _keys(row["fields"], (field for field, _ in fields), f"{group}[{index}].fields")
            for field, segment_id in fields:
                spec = save_format.SEGMENT_BY_ID[segment_id]
                _, bits = _value_geometry(spec)
                decoded[segment_id].append(
                    _uint(row["fields"][field], bits, f"{group}[{index}].{field}")
                )
    placements = _placements()
    remaining_ids = {
        spec.segment_id for spec in save_format.FIXED_SEGMENTS
        if spec.segment_id not in placements
    }
    _keys(named["remaining_segments"], remaining_ids, "remaining segments")
    for spec in save_format.FIXED_SEGMENTS:
        if spec.segment_id in remaining_ids:
            decoded[spec.segment_id] = list(
                _values(named["remaining_segments"][spec.segment_id], spec)
            )
    return {spec.segment_id: decoded[spec.segment_id]
            for spec in save_format.FIXED_SEGMENTS}


def with_edits(named: dict[str, Any], edits: list[dict[str, Any]]) -> dict[str, Any]:
    """Validate an entire named-field batch, then return an independent copy.

    Each edit has exactly group/record_index/field/expected_value/value. Values
    are stored codes within SegmentSpec's width, not intended full RAM values.
    """
    to_fixed_segments(named)
    if type(edits) is not list:
        raise NamedCampaignError("edits must be an explicit list")
    prepared: list[tuple[str, int, str, int]] = []
    seen: set[tuple[str, int]] = set()
    for edit in edits:
        _keys(edit, ("group", "record_index", "field", "expected_value", "value"), "edit")
        group, field, index = edit["group"], edit["field"], edit["record_index"]
        if type(group) is not str or group not in GROUP_FIELDS or type(field) is not str:
            raise NamedCampaignError("edit: explicit known group and field required")
        field_sources = dict(GROUP_FIELDS[group])
        if field not in field_sources:
            raise NamedCampaignError(f"edit: unknown {group} field {field!r}")
        if type(index) is not int or not 0 <= index < _group_count(group):
            raise NamedCampaignError("edit: storage record index outside its group")
        segment_id = field_sources[field]
        target = (segment_id, index)
        if target in seen:
            raise NamedCampaignError("edit: duplicate stored target in one batch")
        seen.add(target)
        _, bits = _value_geometry(save_format.SEGMENT_BY_ID[segment_id])
        expected = _uint(edit["expected_value"], bits, "edit.expected_value")
        value = _uint(edit["value"], bits, "edit.value")
        if named[group][index]["fields"][field] != expected:
            raise NamedCampaignError(f"edit: old stored value differs at {target!r}")
        prepared.append((group, index, field, value))
    result = deepcopy(named)
    for group, index, field, value in prepared:
        result[group][index]["fields"][field] = value
    return result


def with_segment_edits(named: dict[str, Any], edits: list[dict[str, Any]]) -> dict[str, Any]:
    """Edit only unassigned stored segments, without inventing field semantics.

    Each edit has exactly segment_id/value_index/expected_value/value. Named
    segments are rejected: they never acquire a second editable representation.
    """
    to_fixed_segments(named)
    if type(edits) is not list:
        raise NamedCampaignError("segment edits must be an explicit list")
    prepared: list[tuple[str, int, int]] = []
    seen: set[tuple[str, int]] = set()
    for edit in edits:
        _keys(edit, ("segment_id", "value_index", "expected_value", "value"), "segment edit")
        segment_id, index = edit["segment_id"], edit["value_index"]
        if type(segment_id) is not str or segment_id not in named["remaining_segments"]:
            raise NamedCampaignError("segment edit: an existing unnamed segment is required")
        count, bits = _value_geometry(save_format.SEGMENT_BY_ID[segment_id])
        if type(index) is not int or not 0 <= index < count:
            raise NamedCampaignError("segment edit: stored value index outside its segment")
        target = (segment_id, index)
        if target in seen:
            raise NamedCampaignError("segment edit: duplicate stored target in one batch")
        seen.add(target)
        expected = _uint(edit["expected_value"], bits, "segment edit.expected_value")
        value = _uint(edit["value"], bits, "segment edit.value")
        if named["remaining_segments"][segment_id][index] != expected:
            raise NamedCampaignError(f"segment edit: old stored value differs at {target!r}")
        prepared.append((segment_id, index, value))
    result = deepcopy(named)
    for segment_id, index, value in prepared:
        result["remaining_segments"][segment_id][index] = value
    return result


def from_logical(logical: bytes) -> dict[str, Any]:
    """Adapt one explicit valid 8 KiB logical image, using the sole save codec."""
    if type(logical) is not bytes:
        raise NamedCampaignError("logical image must be explicit immutable bytes")
    save_format.validate_logical(logical)
    decoded: dict[str, list[int]] = {}
    for spec in save_format.FIXED_SEGMENTS:
        encoded = logical[spec.logical_offset:spec.logical_offset + spec.encoded_length]
        if spec.encoding == "raw":
            decoded[spec.segment_id] = list(encoded)
        elif spec.encoding == "generic_lsb_bitpack":
            count, bits = _value_geometry(spec)
            decoded[spec.segment_id] = save_format.unpack_values(encoded, bits, count)
        else:
            raise NamedCampaignError(f"{spec.segment_id}: unsupported segment encoding")
    result = from_fixed_segments(decoded)
    result["source"] = {"kind": "exact_logical_baseline", "logical_hex": logical.hex()}
    return result


def to_logical(named: dict[str, Any], original_logical: bytes) -> bytes:
    """Overlay only fixed segments onto the exact explicitly supplied baseline.

    Metadata, CE00, the variable stream and every other byte remain original.
    Only the existing checksum writer also changes bytes outside fixed segments.
    This returns bytes; it does not replace any file or application's live SRAM.
    """
    decoded = to_fixed_segments(named)
    baseline = _source_bytes(named["source"])
    if baseline is None:
        raise NamedCampaignError("a decoded-only view has no bound logical baseline")
    if type(original_logical) is not bytes or baseline != original_logical:
        raise NamedCampaignError("explicit original logical image differs from the bound baseline")
    save_format.validate_logical(original_logical)
    result = bytearray(original_logical)
    for spec in save_format.FIXED_SEGMENTS:
        values = decoded[spec.segment_id]
        if spec.encoding == "raw":
            encoded = bytes(values)
        else:
            count, bits = _value_geometry(spec)
            encoded = save_format.pack_values(values, bits, count)
        if len(encoded) != spec.encoded_length:
            raise NamedCampaignError(f"{spec.segment_id}: encoded length changed")
        result[spec.logical_offset:spec.logical_offset + spec.encoded_length] = encoded
    save_format.write_checksum(result)
    output = bytes(result)
    save_format.validate_logical(output)
    return output
