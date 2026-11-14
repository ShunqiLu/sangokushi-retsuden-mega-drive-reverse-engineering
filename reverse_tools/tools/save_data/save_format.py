#!/usr/bin/env python3
"""Read and write the G-5510 cartridge SRAM format.

The game maps 8 KiB of logical SRAM onto odd CPU addresses starting at
0x200001. The 16 KiB MAME container stores two equal copies of every byte.
Import preserves reserved source bytes and computes the additive checksum.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


FORMAT_ID = "g5510-sram-save-v1"
LOGICAL_SIZE = 0x2000
MAME_CONTAINER_SIZE = 0x4000
CPU_SRAM_FIRST = 0x200001

SIGNATURE_OFFSET = 0x0082
SIGNATURE = b"SEGA"
CHECKSUM_OFFSET = 0x0086
CHECKSUM_REGION_START = 0x008A
CHECKSUM_REGION_LENGTH = 0x1EED
CHECKSUM_REGION_END = CHECKSUM_REGION_START + CHECKSUM_REGION_LENGTH
METADATA_OFFSET = 0x008A
PAYLOAD_OFFSET = 0x0093

CE00_OFFSET = 0x1678
CE00_LENGTH = 110
VARIABLE_OFFSET = 0x16E6


class SaveFormatError(ValueError):
    """Raised when an image or editable bundle violates the proven format."""


@dataclass(frozen=True)
class MetadataField:
    field_id: str
    logical_offset: int
    runtime_ram_address: int


METADATA_FIELDS: tuple[MetadataField, ...] = tuple(
    MetadataField(field_id, METADATA_OFFSET + index, address)
    for index, (field_id, address) in enumerate(
        (
            ("ram_f67b", 0xFFF67B),
            ("ram_f67d", 0xFFF67D),
            ("ram_f67f", 0xFFF67F),
            ("ram_f374", 0xFFF374),
            ("ram_f375", 0xFFF375),
            ("ram_efd3", 0xFFEFD3),
            ("ram_efe5", 0xFFEFE5),
            ("ram_efd7", 0xFFEFD7),
            ("ram_efd9", 0xFFEFD9),
        )
    )
)


@dataclass(frozen=True)
class SegmentSpec:
    segment_id: str
    logical_offset: int
    encoding: str
    encoded_length: int
    runtime_ram_source: str
    bit_width: int | None = None
    record_count: int | None = None
    source_record_width: int | None = None
    transform: str = "identity_low_bits"


def _generic_length(bit_width: int, record_count: int) -> int:
    total_bits = bit_width * record_count
    if total_bits % 8:
        raise AssertionError(
            f"fixed generic segment is not byte aligned: {bit_width}*{record_count}"
        )
    return total_bits // 8


def _build_fixed_segments() -> tuple[SegmentSpec, ...]:
    """Build the exact sequential call order used by ROM 0x008A60."""

    # kind, id, source, width/count/source-stride or raw length, transform
    descriptions: tuple[tuple[Any, ...], ...] = (
        ("bits", "ram_a000", "0xFFA000", 5, 40, 1, "identity_low_bits"),
        ("raw", "ram_efaa", "0xFFEFAA", 5),
        ("bits", "ram_a028", "0xFFA028", 8, 40, 1, "identity_low_bits"),
        ("bits", "ram_a050", "0xFFA050", 8, 256, 1, "identity_low_bits"),
        ("bits", "derived_a150_high_shift7", "0xFFA150 high word lane via 0xFFD300", 8, 256, 2, "derived_shift_right_7"),
        ("bits", "derived_a150_low_shift7", "0xFFA150 low word lane via 0xFFD500", 9, 256, 2, "derived_shift_right_7"),
        ("bits", "ram_b200", "0xFFB200", 8, 256, 2, "identity_low_bits"),
        ("bits", "ram_b400", "0xFFB400", 8, 256, 2, "identity_low_bits"),
        ("bits", "ram_b600", "0xFFB600", 8, 256, 2, "identity_low_bits"),
        ("bits", "derived_b800_div5", "0xFFB800 via 0xFFD300", 5, 256, 2, "derived_unsigned_divide_5"),
        ("bits", "ram_c000", "0xFFC000", 10, 256, 2, "identity_low_bits"),
        ("bits", "ram_be00", "0xFFBE00", 10, 256, 2, "identity_low_bits"),
        ("bits", "ram_c200", "0xFFC200", 7, 256, 1, "identity_low_bits"),
        ("bits", "ram_c300", "0xFFC300", 7, 256, 1, "identity_low_bits"),
        ("bits", "ram_c400", "0xFFC400", 5, 256, 1, "identity_low_bits"),
        ("bits", "ram_c500", "0xFFC500", 7, 256, 1, "identity_low_bits"),
        ("bits", "ram_c700", "0xFFC700", 5, 256, 1, "identity_low_bits"),
        ("bits", "ram_c800", "0xFFC800", 14, 256, 4, "identity_low_bits"),
        ("bits", "ram_cc00", "0xFFCC00", 8, 256, 1, "identity_low_bits"),
        ("bits", "ram_e000", "0xFFE000", 20, 40, 4, "identity_low_bits"),
        ("bits", "ram_e0a0", "0xFFE0A0", 20, 40, 4, "identity_low_bits"),
        ("bits", "ram_e140", "0xFFE140", 10, 40, 4, "identity_low_bits"),
        ("bits", "ram_e1e0", "0xFFE1E0", 10, 40, 4, "identity_low_bits"),
        ("bits", "ram_e280", "0xFFE280", 7, 40, 4, "identity_low_bits"),
        ("bits", "ram_e320", "0xFFE320", 7, 40, 4, "identity_low_bits"),
        ("bits", "ram_e3c0", "0xFFE3C0", 7, 40, 4, "identity_low_bits"),
        ("bits", "ram_e5a0", "0xFFE5A0", 7, 40, 4, "identity_low_bits"),
        ("bits", "ram_f428", "0xFFF428", 4, 40, 1, "load_sentinel_0x0f_to_0xff"),
        ("bits", "ram_e640", "0xFFE640", 9, 16, 2, "load_sentinel_0x01ff_to_0xffff"),
        ("bits", "ram_f460", "0xFFF460", 9, 40, 2, "load_sentinel_0x01ff_to_0xffff"),
        ("bits", "ram_e660", "0xFFE660", 20, 40, 4, "identity_low_bits"),
        ("raw", "ram_e700_e701", "0xFFE700..0xFFE701", 2),
        ("raw", "ram_e710", "0xFFE710", 32),
        ("bits", "ram_e778", "0xFFE778", 17, 40, 4, "identity_low_bits"),
        ("bits", "derived_e818_field0", "0xFFE818 field +0 via 0xFFD300", 9, 40, 2, "sentinel_normalized"),
        ("bits", "derived_e818_field2", "0xFFE818 field +2 via 0xFFD350", 14, 40, 2, "sentinel_normalized"),
        ("bits", "derived_e818_field4", "0xFFE818 field +4 via 0xFFD3A0", 9, 40, 2, "sentinel_normalized"),
        ("bits", "derived_e818_field6_div100", "0xFFE818 field +6 via 0xFFD3F0", 7, 40, 2, "sentinel_or_unsigned_divide_100"),
        ("bits", "derived_e818_field8", "0xFFE818 field +8 via 0xFFD440", 9, 40, 2, "sentinel_normalized"),
        ("bits", "derived_e818_field10", "0xFFE818 field +10 via 0xFFD490", 10, 40, 2, "sentinel_normalized"),
        ("bits", "derived_e9f8_lane0", "0xFFE9F8 lane 0 via 0xFFD300", 6, 16, 1, "deinterleaved_lane"),
        ("bits", "derived_e9f8_lane1", "0xFFE9F8 lane 1 via 0xFFD310", 6, 16, 1, "deinterleaved_lane"),
        ("bits", "derived_e9f8_lane2", "0xFFE9F8 lane 2 via 0xFFD320", 8, 16, 1, "deinterleaved_lane"),
        ("bits", "derived_e9f8_lane3", "0xFFE9F8 lane 3 via 0xFFD330", 4, 16, 1, "deinterleaved_lane"),
        ("bits", "ram_ea38", "0xFFEA38", 1, 40, 1, "identity_low_bits"),
        ("bits", "ram_ea88", "0xFFEA88", 2, 768, 1, "identity_low_bits"),
        ("bits", "ram_ed88", "0xFFED88", 18, 40, 4, "identity_low_bits"),
        ("bits", "ram_ee28", "0xFFEE28", 20, 40, 4, "identity_low_bits"),
        ("bits", "ram_f590", "0xFFF590", 2, 16, 1, "identity_low_bits"),
    )

    result: list[SegmentSpec] = []
    offset = PAYLOAD_OFFSET
    for description in descriptions:
        kind, segment_id, source, *parameters = description
        if kind == "raw":
            (length,) = parameters
            result.append(
                SegmentSpec(segment_id, offset, "raw", length, source)
            )
            offset += length
        elif kind == "bits":
            bit_width, count, source_width, transform = parameters
            length = _generic_length(bit_width, count)
            result.append(
                SegmentSpec(
                    segment_id,
                    offset,
                    "generic_lsb_bitpack",
                    length,
                    source,
                    bit_width,
                    count,
                    source_width,
                    transform,
                )
            )
            offset += length
        else:  # pragma: no cover - construction constant
            raise AssertionError(kind)

    if offset != CE00_OFFSET:
        raise AssertionError(f"fixed layout ended at 0x{offset:04X}, not 0x{CE00_OFFSET:04X}")
    return tuple(result)


FIXED_SEGMENTS = _build_fixed_segments()
SEGMENT_BY_ID = {segment.segment_id: segment for segment in FIXED_SEGMENTS}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def logical_offset_to_cpu_address(offset: int) -> int:
    if not 0 <= offset < LOGICAL_SIZE:
        raise SaveFormatError(f"logical offset outside SRAM: 0x{offset:X}")
    return CPU_SRAM_FIRST + offset * 2


def collapse_mame_nvram(container: bytes) -> bytes:
    if len(container) != MAME_CONTAINER_SIZE:
        raise SaveFormatError(
            f"MAME NVRAM size is 0x{len(container):X}, expected 0x{MAME_CONTAINER_SIZE:X}"
        )
    mismatches = [
        index
        for index in range(LOGICAL_SIZE)
        if container[index * 2] != container[index * 2 + 1]
    ]
    if mismatches:
        first = mismatches[0]
        raise SaveFormatError(
            "MAME duplicated-byte pair mismatch at logical "
            f"0x{first:04X}: {container[first * 2]:02X}!={container[first * 2 + 1]:02X}"
        )
    return bytes(container[::2])


def expand_mame_nvram(logical: bytes) -> bytes:
    if len(logical) != LOGICAL_SIZE:
        raise SaveFormatError(
            f"logical SRAM size is 0x{len(logical):X}, expected 0x{LOGICAL_SIZE:X}"
        )
    result = bytearray(MAME_CONTAINER_SIZE)
    result[0::2] = logical
    result[1::2] = logical
    return bytes(result)


def decode_container(data: bytes) -> tuple[bytes, str]:
    if len(data) == LOGICAL_SIZE:
        return data, "logical_0x2000"
    if len(data) == MAME_CONTAINER_SIZE:
        return collapse_mame_nvram(data), "mame_duplicated_0x4000"
    raise SaveFormatError(
        f"unsupported save container size 0x{len(data):X}; expected 0x2000 or 0x4000"
    )


def encode_container(logical: bytes, container_format: str) -> bytes:
    if container_format == "logical_0x2000":
        if len(logical) != LOGICAL_SIZE:
            raise SaveFormatError("logical image has the wrong size")
        return logical
    if container_format == "mame_duplicated_0x4000":
        return expand_mame_nvram(logical)
    raise SaveFormatError(f"unsupported container format: {container_format}")


def stored_checksum(logical: bytes) -> int:
    if len(logical) != LOGICAL_SIZE:
        raise SaveFormatError("logical image has the wrong size")
    return int.from_bytes(logical[CHECKSUM_OFFSET : CHECKSUM_OFFSET + 4], "little")


def computed_checksum(logical: bytes) -> int:
    if len(logical) != LOGICAL_SIZE:
        raise SaveFormatError("logical image has the wrong size")
    return sum(logical[CHECKSUM_REGION_START:CHECKSUM_REGION_END]) & 0xFFFFFFFF


def validate_logical(logical: bytes) -> dict[str, Any]:
    if len(logical) != LOGICAL_SIZE:
        raise SaveFormatError(
            f"logical SRAM size is 0x{len(logical):X}, expected 0x{LOGICAL_SIZE:X}"
        )
    signature = logical[SIGNATURE_OFFSET : SIGNATURE_OFFSET + len(SIGNATURE)]
    if signature != SIGNATURE:
        raise SaveFormatError(
            f"signature at 0x{SIGNATURE_OFFSET:04X} is {signature!r}, expected {SIGNATURE!r}"
        )
    stored = stored_checksum(logical)
    computed = computed_checksum(logical)
    if stored != computed:
        raise SaveFormatError(
            f"checksum mismatch: stored=0x{stored:08X}, computed=0x{computed:08X}"
        )
    return {
        "valid": True,
        "signature": signature.decode("ascii"),
        "stored_checksum": stored,
        "stored_checksum_hex": f"0x{stored:08X}",
        "computed_checksum": computed,
        "computed_checksum_hex": f"0x{computed:08X}",
    }


def write_checksum(logical: bytearray) -> int:
    checksum = computed_checksum(bytes(logical))
    logical[CHECKSUM_OFFSET : CHECKSUM_OFFSET + 4] = checksum.to_bytes(4, "little")
    return checksum


class LsbBitReader:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.bit_position = 0

    def read(self, width: int) -> int:
        if width < 0:
            raise SaveFormatError("negative bit width")
        if self.bit_position + width > len(self.data) * 8:
            raise SaveFormatError(
                f"bitstream ends at bit {len(self.data) * 8}, need {self.bit_position + width}"
            )
        value = 0
        for output_bit in range(width):
            position = self.bit_position + output_bit
            value |= ((self.data[position // 8] >> (position % 8)) & 1) << output_bit
        self.bit_position += width
        return value


class LsbBitWriter:
    def __init__(self) -> None:
        self.output = bytearray()
        self.accumulator = 0
        self.buffered_bits = 0

    def write(self, value: int, width: int) -> None:
        if width < 0:
            raise SaveFormatError("negative bit width")
        if value < 0 or value >= (1 << width):
            raise SaveFormatError(
                f"value {value} does not fit in unsigned {width}-bit field"
            )
        self.accumulator |= value << self.buffered_bits
        self.buffered_bits += width
        while self.buffered_bits >= 8:
            self.output.append(self.accumulator & 0xFF)
            self.accumulator >>= 8
            self.buffered_bits -= 8

    def finish(self, *, force_final_byte: bool = False) -> bytes:
        if self.buffered_bits or force_final_byte:
            self.output.append(self.accumulator & 0xFF)
            self.accumulator = 0
            self.buffered_bits = 0
        return bytes(self.output)


def unpack_values(data: bytes, bit_width: int, record_count: int) -> list[int]:
    expected = _generic_length(bit_width, record_count)
    if len(data) != expected:
        raise SaveFormatError(
            f"packed segment length {len(data)} != expected {expected}"
        )
    reader = LsbBitReader(data)
    values = [reader.read(bit_width) for _ in range(record_count)]
    if reader.bit_position != len(data) * 8:
        raise AssertionError("fixed segment decoder did not consume all bits")
    return values


def pack_values(values: Sequence[int], bit_width: int, record_count: int) -> bytes:
    if len(values) != record_count:
        raise SaveFormatError(f"record count {len(values)} != expected {record_count}")
    writer = LsbBitWriter()
    for value in values:
        if not isinstance(value, int) or isinstance(value, bool):
            raise SaveFormatError(f"non-integer packed value: {value!r}")
        writer.write(value, bit_width)
    result = writer.finish()
    expected = _generic_length(bit_width, record_count)
    if len(result) != expected:
        raise AssertionError(f"packed length {len(result)} != {expected}")
    return result


def unpack_ce00(data: bytes) -> list[dict[str, int]]:
    if len(data) != CE00_LENGTH:
        raise SaveFormatError(f"CE00 stream length {len(data)} != {CE00_LENGTH}")
    reader = LsbBitReader(data)
    records: list[dict[str, int]] = []
    for index in range(40):
        # On-media order follows the inverse load routine: CE03, CE02, CE01, CE00.
        field3 = reader.read(6)
        field2 = reader.read(7)
        field1 = reader.read(7)
        field0 = reader.read(2)
        records.append(
            {
                "record_index": index,
                "ram_ce00_field0_u2": field0,
                "ram_ce00_field1_u7": field1,
                "ram_ce00_field2_u7": field2,
                "ram_ce00_field3_u6": field3,
            }
        )
    if reader.bit_position != CE00_LENGTH * 8:
        raise AssertionError("CE00 decoder did not consume all bits")
    return records


def pack_ce00(records: Sequence[dict[str, Any]]) -> bytes:
    if len(records) != 40:
        raise SaveFormatError(f"CE00 record count {len(records)} != 40")
    writer = LsbBitWriter()
    for index, record in enumerate(records):
        _validate_record_object(record, "CE00", index)
        _validate_optional_record_index(record, "CE00", index)
        writer.write(_json_int(record, "ram_ce00_field3_u6"), 6)
        writer.write(_json_int(record, "ram_ce00_field2_u7"), 7)
        writer.write(_json_int(record, "ram_ce00_field1_u7"), 7)
        writer.write(_json_int(record, "ram_ce00_field0_u2"), 2)
    result = writer.finish()
    if len(result) != CE00_LENGTH:
        raise AssertionError(f"CE00 packed length {len(result)} != {CE00_LENGTH}")
    return result


def unpack_variable_records(
    data: bytes, *, maximum_records: int = 512
) -> tuple[list[dict[str, Any]], int, int]:
    """Decode the variable RAM 0xFF9000 stream.

    Returns ``(records, encoded_length, meaningful_bits)``.  The game's save
    routine always writes one final accumulator byte after the zero-count
    terminator, including when that accumulator is already byte aligned.
    """

    if (
        not isinstance(maximum_records, int)
        or isinstance(maximum_records, bool)
        or maximum_records < 0
    ):
        raise SaveFormatError("maximum_records must be a non-negative integer")
    reader = LsbBitReader(data)
    records: list[dict[str, Any]] = []
    for record_index in range(maximum_records + 1):
        count = reader.read(4)
        if count == 0:
            meaningful_bits = reader.bit_position
            encoded_length = meaningful_bits // 8 + 1
            if encoded_length > len(data):
                raise SaveFormatError("variable stream terminator byte is truncated")
            final_byte = data[encoded_length - 1]
            if meaningful_bits % 8 == 0:
                if final_byte != 0:
                    raise SaveFormatError(
                        f"aligned variable terminator byte is nonzero: 0x{final_byte:02X}"
                    )
            else:
                used = meaningful_bits % 8
                if final_byte >> used:
                    raise SaveFormatError("variable terminator has nonzero unused high bits")
            return records, encoded_length, meaningful_bits
        if record_index >= maximum_records:
            raise SaveFormatError("variable stream exceeded maximum record count")

        field_7a = reader.read(7)
        field_7b = reader.read(7)
        field_4 = reader.read(4)
        value_18 = reader.read(18)
        value_20 = reader.read(20)
        items = [reader.read(8) for _ in range(count)]
        records.append(
            {
                "record_index": record_index,
                "count_u4": count,
                "field_7a": field_7a,
                "field_7b": field_7b,
                "derived_runtime_byte_at_offset3": None,
                "field_4": field_4,
                "value_18": value_18,
                "value_20": value_20,
                "items_u8": items,
                "runtime_record_length": 13 + count,
            }
        )
    raise AssertionError("unreachable variable-stream loop exit")


def pack_variable_records(records: Sequence[dict[str, Any]]) -> bytes:
    if len(records) > 512:
        raise SaveFormatError("variable stream exceeds the audited 512-record safety limit")
    writer = LsbBitWriter()
    for index, record in enumerate(records):
        _validate_record_object(record, "variable", index)
        _validate_optional_record_index(record, "variable", index)
        items = record.get("items_u8")
        if not isinstance(items, list):
            raise SaveFormatError(f"variable record {index}: items_u8 must be a list")
        count = _json_int(record, "count_u4")
        if count == 0:
            raise SaveFormatError("zero count is reserved for the implicit terminator")
        if count != len(items):
            raise SaveFormatError(
                f"variable record {index}: count {count} != item count {len(items)}"
            )
        writer.write(count, 4)
        writer.write(_json_int(record, "field_7a"), 7)
        writer.write(_json_int(record, "field_7b"), 7)
        writer.write(_json_int(record, "field_4"), 4)
        writer.write(_json_int(record, "value_18"), 18)
        writer.write(_json_int(record, "value_20"), 20)
        for item in items:
            if not isinstance(item, int) or isinstance(item, bool):
                raise SaveFormatError(f"variable record {index}: non-integer item {item!r}")
            writer.write(item, 8)
    writer.write(0, 4)
    return writer.finish(force_final_byte=True)


def _json_int(record: dict[str, Any], key: str) -> int:
    value = record.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise SaveFormatError(f"field {key} is not an integer: {value!r}")
    return value


def _validate_record_object(record: Any, context: str, index: int) -> None:
    if not isinstance(record, dict):
        raise SaveFormatError(
            f"{context} record {index} is not an object: {record!r}"
        )


def _validate_optional_record_index(
    record: dict[str, Any], context: str, expected: int
) -> None:
    if "record_index" not in record:
        return
    value = record["record_index"]
    if not isinstance(value, int) or isinstance(value, bool):
        raise SaveFormatError(
            f"{context} record_index at position {expected} is not an integer: {value!r}"
        )
    if value != expected:
        raise SaveFormatError(
            f"{context} record index changed at position {expected}: {value}"
        )


def inspect_logical(logical: bytes) -> dict[str, Any]:
    validation = validate_logical(logical)
    variable_records, variable_length, variable_bits = unpack_variable_records(
        logical[VARIABLE_OFFSET:CHECKSUM_REGION_END]
    )
    return {
        **validation,
        "logical_size": len(logical),
        "logical_sha256": sha256_bytes(logical),
        "signature_logical_offset": SIGNATURE_OFFSET,
        "signature_cpu_address": logical_offset_to_cpu_address(SIGNATURE_OFFSET),
        "checksum_region": {
            "logical_start": CHECKSUM_REGION_START,
            "logical_end_exclusive": CHECKSUM_REGION_END,
            "length": CHECKSUM_REGION_LENGTH,
        },
        "metadata": [
            {
                **asdict(field),
                "cpu_address": logical_offset_to_cpu_address(field.logical_offset),
                "value": logical[field.logical_offset],
            }
            for field in METADATA_FIELDS
        ],
        "fixed_segment_count": len(FIXED_SEGMENTS),
        "fixed_payload_start": PAYLOAD_OFFSET,
        "fixed_payload_end": CE00_OFFSET,
        "ce00": {"logical_offset": CE00_OFFSET, "encoded_length": CE00_LENGTH},
        "variable": {
            "logical_offset": VARIABLE_OFFSET,
            "record_count": len(variable_records),
            "encoded_length": variable_length,
            "meaningful_bits_including_terminator": variable_bits,
        },
    }


def _write_json(path: Path, value: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as output:
        output.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SaveFormatError(f"cannot read JSON {path}: {error}") from error


def _require_new_directory(path: Path) -> None:
    if path.exists():
        if not path.is_dir():
            raise SaveFormatError(f"output bundle path exists and is not a directory: {path}")
        if any(path.iterdir()):
            raise SaveFormatError(f"output bundle directory is not empty: {path}")
    path.mkdir(parents=True, exist_ok=True)


def extract_bundle(save_path: Path, output_directory: Path) -> dict[str, Any]:
    container = save_path.read_bytes()
    logical, container_format = decode_container(container)
    validation = validate_logical(logical)
    _require_new_directory(output_directory)

    (output_directory / "base_logical.bin").write_bytes(logical)
    metadata = {
        "evidence": "ROM save and load routines",
        "fields": [
            {
                **asdict(field),
                "logical_offset_hex": f"0x{field.logical_offset:04X}",
                "runtime_ram_address_hex": f"0x{field.runtime_ram_address:06X}",
                "cpu_address": logical_offset_to_cpu_address(field.logical_offset),
                "cpu_address_hex": f"0x{logical_offset_to_cpu_address(field.logical_offset):06X}",
                "value": logical[field.logical_offset],
            }
            for field in METADATA_FIELDS
        ],
    }
    _write_json(output_directory / "metadata.json", metadata)

    segments_directory = output_directory / "fixed_segments"
    segments_directory.mkdir()
    segment_manifest: list[dict[str, Any]] = []
    for index, segment in enumerate(FIXED_SEGMENTS):
        prefix = f"{index:02d}_{segment.segment_id}"
        encoded = logical[
            segment.logical_offset : segment.logical_offset + segment.encoded_length
        ]
        encoded_name = prefix + (".raw.bin" if segment.encoding == "raw" else ".packed.bin")
        (segments_directory / encoded_name).write_bytes(encoded)
        entry = {
            **asdict(segment),
            "logical_offset_hex": f"0x{segment.logical_offset:04X}",
            "cpu_address_hex": f"0x{logical_offset_to_cpu_address(segment.logical_offset):06X}",
            "encoded_file": f"fixed_segments/{encoded_name}",
            "encoded_sha256": sha256_bytes(encoded),
        }
        if segment.encoding == "generic_lsb_bitpack":
            assert segment.bit_width is not None and segment.record_count is not None
            values = unpack_values(encoded, segment.bit_width, segment.record_count)
            values_name = prefix + ".values.json"
            _write_json(
                segments_directory / values_name,
                {
                    "segment_id": segment.segment_id,
                    "bit_width": segment.bit_width,
                    "record_count": segment.record_count,
                    "values": values,
                },
            )
            entry["editable_values_file"] = f"fixed_segments/{values_name}"
        segment_manifest.append(entry)

    ce00_data = logical[CE00_OFFSET : CE00_OFFSET + CE00_LENGTH]
    (output_directory / "ce00.packed.bin").write_bytes(ce00_data)
    _write_json(
        output_directory / "ce00.records.json",
        {
            "runtime_ram_start": "0xFFCE00",
            "record_count": 40,
            "record_width_bits": 22,
            "records": unpack_ce00(ce00_data),
        },
    )

    variable_records, variable_length, variable_bits = unpack_variable_records(
        logical[VARIABLE_OFFSET:CHECKSUM_REGION_END]
    )
    variable_data = logical[VARIABLE_OFFSET : VARIABLE_OFFSET + variable_length]
    variable_tail = logical[VARIABLE_OFFSET + variable_length : CHECKSUM_REGION_END]
    (output_directory / "ram9000_variable.packed.bin").write_bytes(variable_data)
    (output_directory / "checksum_region_unused_tail.bin").write_bytes(variable_tail)
    _write_json(
        output_directory / "ram9000_variable.records.json",
        {
            "runtime_ram_start": "0xFF9000",
            "record_count": len(variable_records),
            "encoded_length": variable_length,
            "meaningful_bits_including_terminator": variable_bits,
            "derived_runtime_byte_at_offset3": (
                "not stored; load routine derives the average of RAM C400 values "
                "selected by items_u8"
            ),
            "records": variable_records,
        },
    )

    manifest = {
        "format": FORMAT_ID,
        "evidence_grade": "confirmed",
        "source_path_for_reference": save_path.name,
        "source_container_format": container_format,
        "source_container_size": len(container),
        "source_container_sha256": sha256_bytes(container),
        "source_logical_size": len(logical),
        "source_logical_sha256": sha256_bytes(logical),
        "validation": validation,
        "layout": {
            "signature_offset": SIGNATURE_OFFSET,
            "checksum_offset": CHECKSUM_OFFSET,
            "checksum_region_start": CHECKSUM_REGION_START,
            "checksum_region_length": CHECKSUM_REGION_LENGTH,
            "metadata_offset": METADATA_OFFSET,
            "payload_offset": PAYLOAD_OFFSET,
            "ce00_offset": CE00_OFFSET,
            "ce00_length": CE00_LENGTH,
            "variable_offset": VARIABLE_OFFSET,
            "variable_original_encoded_length": variable_length,
        },
        "fixed_segments": segment_manifest,
        "files": {
            "base_logical": "base_logical.bin",
            "metadata": "metadata.json",
            "ce00_values": "ce00.records.json",
            "variable_values": "ram9000_variable.records.json",
            "variable_unused_tail": "checksum_region_unused_tail.bin",
        },
    }
    _write_json(output_directory / "manifest.json", manifest)
    return manifest


def _validate_manifest(manifest: dict[str, Any]) -> None:
    if manifest.get("format") != FORMAT_ID:
        raise SaveFormatError(f"unsupported bundle format: {manifest.get('format')!r}")
    expected_layout = {
        "signature_offset": SIGNATURE_OFFSET,
        "checksum_offset": CHECKSUM_OFFSET,
        "checksum_region_start": CHECKSUM_REGION_START,
        "checksum_region_length": CHECKSUM_REGION_LENGTH,
        "metadata_offset": METADATA_OFFSET,
        "payload_offset": PAYLOAD_OFFSET,
        "ce00_offset": CE00_OFFSET,
        "ce00_length": CE00_LENGTH,
        "variable_offset": VARIABLE_OFFSET,
    }
    layout = manifest.get("layout")
    if not isinstance(layout, dict):
        raise SaveFormatError("bundle layout is missing")
    for key, value in expected_layout.items():
        if layout.get(key) != value:
            raise SaveFormatError(f"bundle layout field {key} was changed")
    entries = manifest.get("fixed_segments")
    if not isinstance(entries, list) or len(entries) != len(FIXED_SEGMENTS):
        raise SaveFormatError("fixed segment manifest count changed")
    for index, (expected, entry) in enumerate(zip(FIXED_SEGMENTS, entries)):
        for key in (
            "segment_id",
            "logical_offset",
            "encoding",
            "encoded_length",
            "bit_width",
            "record_count",
        ):
            if entry.get(key) != getattr(expected, key):
                raise SaveFormatError(
                    f"fixed segment {expected.segment_id} field {key} was changed"
                )
        prefix = f"{index:02d}_{expected.segment_id}"
        expected_encoded_file = (
            f"fixed_segments/{prefix}.raw.bin"
            if expected.encoding == "raw"
            else f"fixed_segments/{prefix}.packed.bin"
        )
        if entry.get("encoded_file") != expected_encoded_file:
            raise SaveFormatError(
                f"fixed segment {expected.segment_id} encoded file was changed"
            )
        if expected.encoding == "generic_lsb_bitpack":
            expected_values_file = f"fixed_segments/{prefix}.values.json"
            if entry.get("editable_values_file") != expected_values_file:
                raise SaveFormatError(
                    f"fixed segment {expected.segment_id} values file was changed"
                )


def _metadata_values(bundle: Path) -> list[int]:
    document = _read_json(bundle / "metadata.json")
    fields = document.get("fields") if isinstance(document, dict) else None
    if not isinstance(fields, list) or len(fields) != len(METADATA_FIELDS):
        raise SaveFormatError("metadata field count changed")
    values: list[int] = []
    for expected, entry in zip(METADATA_FIELDS, fields):
        if not isinstance(entry, dict):
            raise SaveFormatError("metadata entry is not an object")
        if entry.get("field_id") != expected.field_id:
            raise SaveFormatError(f"metadata field order/name changed at {expected.field_id}")
        if entry.get("logical_offset") != expected.logical_offset:
            raise SaveFormatError(f"metadata field {expected.field_id} was relocated")
        if entry.get("runtime_ram_address") != expected.runtime_ram_address:
            raise SaveFormatError(
                f"metadata field {expected.field_id} runtime address was changed"
            )
        value = _json_int(entry, "value")
        if not 0 <= value <= 0xFF:
            raise SaveFormatError(f"metadata field {expected.field_id} exceeds one byte")
        values.append(value)
    return values


def import_bundle(
    bundle: Path,
    output_path: Path,
    *,
    allow_variable_resize: bool = False,
) -> dict[str, Any]:
    if output_path.exists():
        raise SaveFormatError(f"refusing to overwrite existing output: {output_path}")
    manifest = _read_json(bundle / "manifest.json")
    if not isinstance(manifest, dict):
        raise SaveFormatError("manifest is not an object")
    _validate_manifest(manifest)

    base_path = bundle / "base_logical.bin"
    base = base_path.read_bytes()
    if len(base) != LOGICAL_SIZE:
        raise SaveFormatError("bundle base logical image has the wrong size")
    expected_base_hash = manifest.get("source_logical_sha256")
    if sha256_bytes(base) != expected_base_hash:
        raise SaveFormatError("bundle base logical image hash mismatch")
    validate_logical(base)
    _, base_variable_length, _ = unpack_variable_records(
        base[VARIABLE_OFFSET:CHECKSUM_REGION_END]
    )
    logical = bytearray(base)

    for field, value in zip(METADATA_FIELDS, _metadata_values(bundle)):
        logical[field.logical_offset] = value

    segment_entries = manifest["fixed_segments"]
    for spec, entry in zip(FIXED_SEGMENTS, segment_entries):
        if spec.encoding == "raw":
            encoded_file = entry.get("encoded_file")
            if not isinstance(encoded_file, str):
                raise SaveFormatError(f"{spec.segment_id}: missing raw file")
            encoded = (bundle / encoded_file).read_bytes()
        else:
            values_file = entry.get("editable_values_file")
            if not isinstance(values_file, str):
                raise SaveFormatError(f"{spec.segment_id}: missing values file")
            document = _read_json(bundle / values_file)
            if not isinstance(document, dict):
                raise SaveFormatError(f"{spec.segment_id}: values document is not an object")
            if document.get("segment_id") != spec.segment_id:
                raise SaveFormatError(f"{spec.segment_id}: values document identity changed")
            if document.get("bit_width") != spec.bit_width:
                raise SaveFormatError(f"{spec.segment_id}: bit width changed")
            if document.get("record_count") != spec.record_count:
                raise SaveFormatError(f"{spec.segment_id}: record count metadata changed")
            values = document.get("values")
            if not isinstance(values, list):
                raise SaveFormatError(f"{spec.segment_id}: values must be a list")
            assert spec.bit_width is not None and spec.record_count is not None
            encoded = pack_values(values, spec.bit_width, spec.record_count)
        if len(encoded) != spec.encoded_length:
            raise SaveFormatError(
                f"{spec.segment_id}: encoded length {len(encoded)} != {spec.encoded_length}"
            )
        logical[spec.logical_offset : spec.logical_offset + spec.encoded_length] = encoded

    ce00_document = _read_json(bundle / "ce00.records.json")
    if not isinstance(ce00_document, dict) or not isinstance(
        ce00_document.get("records"), list
    ):
        raise SaveFormatError("CE00 records are missing")
    ce00_data = pack_ce00(ce00_document["records"])
    logical[CE00_OFFSET : CE00_OFFSET + CE00_LENGTH] = ce00_data

    variable_document = _read_json(bundle / "ram9000_variable.records.json")
    if not isinstance(variable_document, dict) or not isinstance(
        variable_document.get("records"), list
    ):
        raise SaveFormatError("RAM9000 variable records are missing")
    variable_data = pack_variable_records(variable_document["records"])
    original_variable_length = manifest["layout"].get(
        "variable_original_encoded_length"
    )
    if not isinstance(original_variable_length, int):
        raise SaveFormatError("original variable stream length is missing")
    if original_variable_length != base_variable_length:
        raise SaveFormatError(
            "manifest original variable stream length does not match the hash-gated base image"
        )
    if len(variable_data) != base_variable_length and not allow_variable_resize:
        raise SaveFormatError(
            "variable stream encoded length changed; pass allow_variable_resize only "
            "after reviewing the unused-tail replacement"
        )
    if VARIABLE_OFFSET + len(variable_data) > CHECKSUM_REGION_END:
        raise SaveFormatError("variable stream no longer fits in the checksummed save area")
    if len(variable_data) != base_variable_length:
        logical[VARIABLE_OFFSET:CHECKSUM_REGION_END] = b"\xFF" * (
            CHECKSUM_REGION_END - VARIABLE_OFFSET
        )
    logical[VARIABLE_OFFSET : VARIABLE_OFFSET + len(variable_data)] = variable_data

    write_checksum(logical)
    validation = validate_logical(bytes(logical))
    container_format = manifest.get("source_container_format")
    if not isinstance(container_format, str):
        raise SaveFormatError("source container format is missing")
    output = encode_container(bytes(logical), container_format)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with output_path.open("xb") as output_file:
            output_file.write(output)
    except FileExistsError as error:
        raise SaveFormatError(f"refusing to overwrite existing output: {output_path}") from error
    return {
        "format": FORMAT_ID,
        "output_path": str(output_path.resolve()),
        "container_format": container_format,
        "container_size": len(output),
        "container_sha256": sha256_bytes(output),
        "logical_sha256": sha256_bytes(bytes(logical)),
        "checksum": validation["stored_checksum"],
        "checksum_hex": validation["stored_checksum_hex"],
        "changed_logical_byte_count": sum(
            before != after for before, after in zip(base, logical)
        ),
        "variable_encoded_length": len(variable_data),
    }


def _command_inspect(arguments: argparse.Namespace) -> int:
    data = Path(arguments.save).read_bytes()
    logical, container_format = decode_container(data)
    report = inspect_logical(logical)
    report["container_format"] = container_format
    report["container_size"] = len(data)
    report["container_sha256"] = sha256_bytes(data)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def _command_extract(arguments: argparse.Namespace) -> int:
    manifest = extract_bundle(Path(arguments.save), Path(arguments.output_directory))
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


def _command_import(arguments: argparse.Namespace) -> int:
    report = import_bundle(
        Path(arguments.bundle),
        Path(arguments.output),
        allow_variable_resize=arguments.allow_variable_resize,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="validate and summarize a save")
    inspect_parser.add_argument("save")
    inspect_parser.set_defaults(handler=_command_inspect)

    extract_parser = subparsers.add_parser(
        "extract", help="export a lossless editable save bundle"
    )
    extract_parser.add_argument("save")
    extract_parser.add_argument("output_directory")
    extract_parser.set_defaults(handler=_command_extract)

    import_parser = subparsers.add_parser(
        "import", help="rebuild a new checksummed save from a bundle"
    )
    import_parser.add_argument("bundle")
    import_parser.add_argument("output")
    import_parser.add_argument(
        "--allow-variable-resize",
        action="store_true",
        help="permit a RAM9000 stream length change and replace its unused tail with FF",
    )
    import_parser.set_defaults(handler=_command_import)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_argument_parser()
    arguments = parser.parse_args(argv)
    try:
        return int(arguments.handler(arguments))
    except (OSError, SaveFormatError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
