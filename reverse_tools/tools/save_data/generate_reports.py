#!/usr/bin/env python3
"""Describe the SRAM layout and summarize a supplied save image."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Sequence

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.save_data import save_format


ROUTINES: tuple[dict[str, Any], ...] = (
    {"address": 0x0083FA, "role": "save_entry_and_signature", "evidence": "confirmed"},
    {"address": 0x008866, "role": "derive_a150_shifted_arrays", "evidence": "confirmed"},
    {"address": 0x008888, "role": "derive_e818_field_arrays", "evidence": "confirmed"},
    {"address": 0x0088C6, "role": "pack_ce00_40x22_bits", "evidence": "confirmed"},
    {"address": 0x008946, "role": "pack_ram9000_variable_records", "evidence": "confirmed"},
    {"address": 0x0089FE, "role": "store_checksum_little_endian", "evidence": "confirmed"},
    {"address": 0x008A22, "role": "sum_0x1eed_logical_bytes", "evidence": "confirmed"},
    {"address": 0x008A60, "role": "load_entry", "evidence": "confirmed"},
    {"address": 0x009036, "role": "unpack_ram9000_variable_records", "evidence": "confirmed"},
    {"address": 0x0090D8, "role": "validate_signature_and_checksum", "evidence": "confirmed"},
    {"address": 0x0091F8, "role": "derive_ram9000_skipped_byte", "evidence": "confirmed"},
    {"address": 0x00922A, "role": "generic_lsb_bit_packer", "evidence": "confirmed"},
    {"address": 0x00927A, "role": "generic_packer_sram_byte_write", "evidence": "confirmed"},
    {"address": 0x00931E, "role": "generic_lsb_bit_unpacker", "evidence": "confirmed"},
)


def _write_json(path: Path, value: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as output:
        output.write(json.dumps(value, indent=2) + "\n")


def layout_document() -> dict[str, Any]:
    generic_total = sum(
        item.encoded_length
        for item in save_format.FIXED_SEGMENTS
        if item.encoding == "generic_lsb_bitpack"
    )
    raw_total = sum(
        item.encoded_length
        for item in save_format.FIXED_SEGMENTS
        if item.encoding == "raw"
    )
    return {
        "format": save_format.FORMAT_ID,
        "evidence_grade": "confirmed",
        "source_rom": {
            "product": "G-5510",
        },
        "logical_sram": {
            "size": save_format.LOGICAL_SIZE,
            "cpu_first_odd_address": save_format.CPU_SRAM_FIRST,
            "cpu_last_odd_address": save_format.logical_offset_to_cpu_address(
                save_format.LOGICAL_SIZE - 1
            ),
            "mame_container_size": save_format.MAME_CONTAINER_SIZE,
            "mame_mapping": "container[2*i] == container[2*i+1] == logical[i]",
        },
        "header": {
            "signature_offset": save_format.SIGNATURE_OFFSET,
            "signature": save_format.SIGNATURE.decode("ascii"),
            "checksum_offset": save_format.CHECKSUM_OFFSET,
            "checksum_byte_order": "little",
            "checksum_algorithm": "sum(bytes) modulo 2^32",
            "checksum_region_start": save_format.CHECKSUM_REGION_START,
            "checksum_region_length": save_format.CHECKSUM_REGION_LENGTH,
            "checksum_region_end_exclusive": save_format.CHECKSUM_REGION_END,
        },
        "metadata_fields": [as_machine_metadata(item) for item in save_format.METADATA_FIELDS],
        "fixed_segments": [as_machine_segment(item) for item in save_format.FIXED_SEGMENTS],
        "fixed_totals": {
            "segment_count": len(save_format.FIXED_SEGMENTS),
            "generic_encoded_bytes": generic_total,
            "raw_encoded_bytes": raw_total,
            "all_fixed_bytes": generic_total + raw_total,
            "start": save_format.PAYLOAD_OFFSET,
            "end_exclusive": save_format.CE00_OFFSET,
        },
        "ce00": {
            "logical_offset": save_format.CE00_OFFSET,
            "encoded_length": save_format.CE00_LENGTH,
            "record_count": 40,
            "bits_per_record": 22,
            "on_media_field_order": [
                {"runtime_field_offset": 3, "bits": 6},
                {"runtime_field_offset": 2, "bits": 7},
                {"runtime_field_offset": 1, "bits": 7},
                {"runtime_field_offset": 0, "bits": 2},
            ],
        },
        "ram9000_variable": {
            "logical_offset": save_format.VARIABLE_OFFSET,
            "on_media_record_fields": [
                {"name": "count", "bits": 4},
                {"name": "field_7a", "bits": 7},
                {"name": "field_7b", "bits": 7},
                {"name": "field_4", "bits": 4},
                {"name": "value_18", "bits": 18},
                {"name": "value_20", "bits": 20},
                {"name": "items", "bits_each": 8, "count_from": "count"},
            ],
            "runtime_record_length": "13 + count bytes",
            "terminator": "zero 4-bit count",
            "final_byte_rule": (
                "save routine writes one accumulator byte after the terminator, "
                "including an extra 00 when already byte aligned"
            ),
            "omitted_runtime_byte": (
                "record offset +3; load derives the mean of RAM C400 values "
                "indexed by the trailing item bytes"
            ),
        },
        "routines": [
            {**item, "address_hex": f"0x{item['address']:06X}"} for item in ROUTINES
        ],
    }


def as_machine_metadata(field: save_format.MetadataField) -> dict[str, Any]:
    return {
        "field_id": field.field_id,
        "logical_offset": field.logical_offset,
        "logical_offset_hex": f"0x{field.logical_offset:04X}",
        "cpu_address": save_format.logical_offset_to_cpu_address(field.logical_offset),
        "cpu_address_hex": f"0x{save_format.logical_offset_to_cpu_address(field.logical_offset):06X}",
        "runtime_ram_address": field.runtime_ram_address,
        "runtime_ram_address_hex": f"0x{field.runtime_ram_address:06X}",
        "evidence": "confirmed",
    }


def as_machine_segment(segment: save_format.SegmentSpec) -> dict[str, Any]:
    return {
        "segment_id": segment.segment_id,
        "logical_offset": segment.logical_offset,
        "logical_offset_hex": f"0x{segment.logical_offset:04X}",
        "cpu_address": save_format.logical_offset_to_cpu_address(segment.logical_offset),
        "cpu_address_hex": f"0x{save_format.logical_offset_to_cpu_address(segment.logical_offset):06X}",
        "encoding": segment.encoding,
        "encoded_length": segment.encoded_length,
        "logical_end_exclusive": segment.logical_offset + segment.encoded_length,
        "runtime_ram_source": segment.runtime_ram_source,
        "bit_width": segment.bit_width,
        "record_count": segment.record_count,
        "source_record_width": segment.source_record_width,
        "transform": segment.transform,
        "evidence": "confirmed",
    }


def capture_document(path: Path) -> dict[str, Any]:
    container = path.read_bytes()
    logical, container_format = save_format.decode_container(container)
    inspection = save_format.inspect_logical(logical)

    fixed_roundtrips = []
    for segment in save_format.FIXED_SEGMENTS:
        encoded = logical[
            segment.logical_offset : segment.logical_offset + segment.encoded_length
        ]
        if segment.encoding == "generic_lsb_bitpack":
            assert segment.bit_width is not None and segment.record_count is not None
            rebuilt = save_format.pack_values(
                save_format.unpack_values(encoded, segment.bit_width, segment.record_count),
                segment.bit_width,
                segment.record_count,
            )
        else:
            rebuilt = encoded
        fixed_roundtrips.append(
            {"segment_id": segment.segment_id, "exact_roundtrip": rebuilt == encoded}
        )

    ce00 = logical[save_format.CE00_OFFSET : save_format.CE00_OFFSET + save_format.CE00_LENGTH]
    ce00_roundtrip = save_format.pack_ce00(save_format.unpack_ce00(ce00)) == ce00
    variable_records, variable_length, variable_bits = save_format.unpack_variable_records(
        logical[save_format.VARIABLE_OFFSET : save_format.CHECKSUM_REGION_END]
    )
    variable = logical[
        save_format.VARIABLE_OFFSET : save_format.VARIABLE_OFFSET + variable_length
    ]
    return {
        "capture_file_for_reference": path.name,
        "container_format": container_format,
        "container_size": len(container),
        "container_sha256": save_format.sha256_bytes(container),
        "logical_size": len(logical),
        "logical_sha256": save_format.sha256_bytes(logical),
        "validation": {
            "signature": inspection["signature"],
            "stored_checksum_hex": inspection["stored_checksum_hex"],
            "computed_checksum_hex": inspection["computed_checksum_hex"],
        },
        "non_ff_logical_byte_count": sum(value != 0xFF for value in logical),
        "first_non_ff_logical_offset": next(
            index for index, value in enumerate(logical) if value != 0xFF
        ),
        "last_non_ff_logical_offset": max(
            index for index, value in enumerate(logical) if value != 0xFF
        ),
        "metadata_values": [logical[field.logical_offset] for field in save_format.METADATA_FIELDS],
        "fixed_segment_roundtrips": fixed_roundtrips,
        "all_fixed_segments_roundtrip": all(
            item["exact_roundtrip"] for item in fixed_roundtrips
        ),
        "ce00_exact_roundtrip": ce00_roundtrip,
        "variable_record_count": len(variable_records),
        "variable_encoded_length": variable_length,
        "variable_meaningful_bits": variable_bits,
        "variable_exact_roundtrip": save_format.pack_variable_records(variable_records)
        == variable,
    }


def generate(output_directory: Path, capture: Path | None) -> None:
    output_directory.mkdir(parents=True, exist_ok=True)
    layout = layout_document()
    _write_json(output_directory / "save_layout.json", layout)
    with (output_directory / "fixed_segments.csv").open(
        "w", encoding="utf-8", newline=""
    ) as output:
        fieldnames = (
            "segment_id",
            "logical_offset_hex",
            "cpu_address_hex",
            "encoding",
            "encoded_length",
            "runtime_ram_source",
            "bit_width",
            "record_count",
            "source_record_width",
            "transform",
            "evidence",
        )
        writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for item in layout["fixed_segments"]:
            writer.writerow({key: item.get(key) for key in fieldnames})
    if capture is not None:
        _write_json(output_directory / "save_summary.json", capture_document(capture))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--capture", type=Path, help="optional 8 KiB or 16 KiB save file")
    arguments = parser.parse_args(argv)
    generate(arguments.output_directory, arguments.capture)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
