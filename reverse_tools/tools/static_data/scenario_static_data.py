#!/usr/bin/env python3
"""Extract G-5510 scenario tables by address and import their source records."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import struct
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.rom_layout import require_g5510_rom

SCENARIO_POINTER_TABLE = 0x003E48
SCENARIO_COUNT = 3
SCENARIO_DESCRIPTOR_SIZE = 0x84
SCENARIO_BLOCK_SIZE = 0x297C
SCENARIO_YEARS = (189, 200, 215)


@dataclass(frozen=True)
class TableSpec:
    table_id: str
    descriptor_offset: int
    ram_start: int
    source_length: int
    runtime_length: int
    source_record_width: int
    runtime_record_width: int
    record_count: int
    transform: str = "identity"


# The lengths are immediate DBF loop bounds in ROM 0x003E54..0x0040AE.
# EA88 swaps bytes 0/1 of every 3-byte source record.  F000 converts 256
# big-endian words to bytes, subtracting 0x00B8 except for the 0xFFFF sentinel.
TABLE_SPECS: tuple[TableSpec, ...] = (
    TableSpec("ram_f428", 0x00, 0xFFF428, 40, 40, 1, 1, 40),
    TableSpec("ram_f460", 0x04, 0xFFF460, 80, 80, 2, 2, 40),
    TableSpec("ram_e640", 0x08, 0xFFE640, 32, 32, 2, 2, 16),
    TableSpec("ram_e000", 0x0C, 0xFFE000, 160, 160, 4, 4, 40),
    TableSpec("ram_e0a0", 0x10, 0xFFE0A0, 160, 160, 4, 4, 40),
    TableSpec("ram_e140", 0x14, 0xFFE140, 160, 160, 4, 4, 40),
    TableSpec("ram_e1e0", 0x18, 0xFFE1E0, 160, 160, 4, 4, 40),
    TableSpec("ram_e280", 0x1C, 0xFFE280, 160, 160, 4, 4, 40),
    TableSpec("ram_e320", 0x20, 0xFFE320, 160, 160, 4, 4, 40),
    TableSpec("ram_e3c0", 0x24, 0xFFE3C0, 160, 160, 4, 4, 40),
    TableSpec("ram_e460", 0x28, 0xFFE460, 160, 160, 4, 4, 40),
    TableSpec("ram_e500", 0x2C, 0xFFE500, 160, 160, 4, 4, 40),
    TableSpec("ram_e5a0", 0x30, 0xFFE5A0, 160, 160, 4, 4, 40),
    TableSpec("ram_b000", 0x34, 0xFFB000, 512, 512, 2, 2, 256),
    TableSpec("ram_b200", 0x38, 0xFFB200, 512, 512, 2, 2, 256),
    TableSpec("ram_b400", 0x3C, 0xFFB400, 512, 512, 2, 2, 256),
    TableSpec("ram_b600", 0x40, 0xFFB600, 512, 512, 2, 2, 256),
    TableSpec("ram_b800", 0x44, 0xFFB800, 512, 512, 2, 2, 256),
    TableSpec("ram_ba00", 0x48, 0xFFBA00, 512, 512, 2, 2, 256),
    TableSpec("ram_bc00", 0x4C, 0xFFBC00, 512, 512, 2, 2, 256),
    TableSpec("ram_be00", 0x50, 0xFFBE00, 512, 512, 2, 2, 256),
    TableSpec("ram_c000", 0x54, 0xFFC000, 512, 512, 2, 2, 256),
    TableSpec("ram_c200", 0x58, 0xFFC200, 256, 256, 1, 1, 256),
    TableSpec("ram_c300", 0x5C, 0xFFC300, 256, 256, 1, 1, 256),
    TableSpec("ram_c400", 0x60, 0xFFC400, 256, 256, 1, 1, 256),
    TableSpec("ram_c500", 0x64, 0xFFC500, 256, 256, 1, 1, 256),
    TableSpec("ram_c600", 0x68, 0xFFC600, 256, 256, 1, 1, 256),
    TableSpec("ram_c700", 0x6C, 0xFFC700, 256, 256, 1, 1, 256),
    TableSpec("ram_c800", 0x70, 0xFFC800, 1024, 1024, 4, 4, 256),
    TableSpec("ram_cc00", 0x74, 0xFFCC00, 256, 256, 1, 1, 256),
    TableSpec("ram_e710", 0x78, 0xFFE710, 32, 32, 2, 2, 16),
    TableSpec("ram_ea88", 0x7C, 0xFFEA88, 768, 768, 3, 3, 256, "swap_first_two_bytes"),
    TableSpec("ram_f000", 0x80, 0xFFF000, 512, 256, 2, 1, 256, "word_minus_0x00b8"),
)

TABLE_BY_ID = {spec.table_id: spec for spec in TABLE_SPECS}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_be16(data: bytes, offset: int) -> int:
    return struct.unpack_from(">H", data, offset)[0]


def read_be32(data: bytes, offset: int) -> int:
    return struct.unpack_from(">I", data, offset)[0]


def runtime_bytes(spec: TableSpec, source: bytes) -> bytes:
    if len(source) != spec.source_length:
        raise ValueError(
            f"{spec.table_id}: source length {len(source)} != {spec.source_length}"
        )
    if spec.transform == "identity":
        result = source
    elif spec.transform == "swap_first_two_bytes":
        result_buffer = bytearray(source)
        for offset in range(0, len(result_buffer), 3):
            result_buffer[offset], result_buffer[offset + 1] = (
                result_buffer[offset + 1],
                result_buffer[offset],
            )
        result = bytes(result_buffer)
    elif spec.transform == "word_minus_0x00b8":
        result_buffer = bytearray()
        for offset in range(0, len(source), 2):
            value = read_be16(source, offset)
            result_buffer.append(0xFF if value == 0xFFFF else (value - 0x00B8) & 0xFF)
        result = bytes(result_buffer)
    else:
        raise ValueError(f"unsupported transform: {spec.transform}")
    if len(result) != spec.runtime_length:
        raise AssertionError(
            f"{spec.table_id}: runtime length {len(result)} != {spec.runtime_length}"
        )
    return result


def canonical_rom(path: Path) -> bytes:
    data = path.read_bytes()
    require_g5510_rom(data)
    scenario_layout(data)
    return data


def scenario_descriptor_bases(rom: bytes) -> tuple[int, ...]:
    bases = tuple(
        read_be32(rom, SCENARIO_POINTER_TABLE + index * 4)
        for index in range(SCENARIO_COUNT)
    )
    for index, base in enumerate(bases):
        if base + SCENARIO_DESCRIPTOR_SIZE > len(rom):
            raise ValueError(f"scenario {index}: descriptor outside ROM: 0x{base:06X}")
    return bases


def scenario_layout(rom: bytes) -> list[dict[str, Any]]:
    bases = scenario_descriptor_bases(rom)
    scenarios: list[dict[str, Any]] = []
    for scenario_index, (year, descriptor_base) in enumerate(zip(SCENARIO_YEARS, bases)):
        intervals = [(descriptor_base, descriptor_base + SCENARIO_DESCRIPTOR_SIZE, "descriptor")]
        tables: list[dict[str, Any]] = []
        for spec in TABLE_SPECS:
            pointer = read_be32(rom, descriptor_base + spec.descriptor_offset)
            end = pointer + spec.source_length
            if end > len(rom):
                raise ValueError(
                    f"scenario {scenario_index} {spec.table_id}: "
                    f"0x{pointer:06X}..0x{end:06X} outside ROM"
                )
            intervals.append((pointer, end, spec.table_id))
            tables.append(
                {
                    "table_id": spec.table_id,
                    "descriptor_offset": spec.descriptor_offset,
                    "descriptor_offset_hex": f"0x{spec.descriptor_offset:02X}",
                    "source_rom_offset": pointer,
                    "source_rom_offset_hex": f"0x{pointer:06X}",
                    "source_length": spec.source_length,
                    "runtime_ram_start": spec.ram_start,
                    "runtime_ram_start_hex": f"0x{spec.ram_start:06X}",
                    "runtime_length": spec.runtime_length,
                    "source_record_width": spec.source_record_width,
                    "runtime_record_width": spec.runtime_record_width,
                    "record_count": spec.record_count,
                    "transform": spec.transform,
                }
            )

        ordered = sorted(intervals)
        expected = descriptor_base
        for start, end, label in ordered:
            if start != expected:
                relation = "overlap" if start < expected else "gap"
                raise ValueError(
                    f"scenario {scenario_index}: {relation} before {label}: "
                    f"expected 0x{expected:06X}, found 0x{start:06X}"
                )
            expected = end
        if expected - descriptor_base != SCENARIO_BLOCK_SIZE:
            raise ValueError(
                f"scenario {scenario_index}: covered block size "
                f"0x{expected - descriptor_base:X} != 0x{SCENARIO_BLOCK_SIZE:X}"
            )
        if scenario_index + 1 < len(bases) and expected != bases[scenario_index + 1]:
            raise ValueError(
                f"scenario {scenario_index}: block end 0x{expected:06X} "
                f"!= next descriptor 0x{bases[scenario_index + 1]:06X}"
            )

        scenarios.append(
            {
                "scenario_index": scenario_index,
                "year": year,
                "descriptor_rom_offset": descriptor_base,
                "descriptor_rom_offset_hex": f"0x{descriptor_base:06X}",
                "descriptor_length": SCENARIO_DESCRIPTOR_SIZE,
                "block_rom_end": expected,
                "block_rom_end_hex": f"0x{expected:06X}",
                "block_length": SCENARIO_BLOCK_SIZE,
                "tables": tables,
            }
        )
    return scenarios


def _u16_records(data: bytes) -> list[int]:
    return [read_be16(data, offset) for offset in range(0, len(data), 2)]


def _u32_records(data: bytes) -> list[int]:
    return [read_be32(data, offset) for offset in range(0, len(data), 4)]


def _hex_record(data: bytes, width: int, index: int) -> str:
    start = index * width
    return data[start : start + width].hex().upper()


def decoded_records(table_data: dict[str, bytes], scenario_index: int, year: int) -> dict[str, Any]:
    words = {
        table_id: _u16_records(table_data[table_id])
        for table_id in (
            "ram_f460",
            "ram_e640",
            "ram_b000",
            "ram_b200",
            "ram_b400",
            "ram_b600",
            "ram_b800",
            "ram_ba00",
            "ram_bc00",
            "ram_be00",
            "ram_c000",
            "ram_e710",
        )
    }
    longs = {
        table_id: _u32_records(table_data[table_id])
        for table_id in (
            "ram_e000",
            "ram_e0a0",
            "ram_e140",
            "ram_e1e0",
            "ram_e280",
            "ram_e320",
            "ram_e3c0",
            "ram_e460",
            "ram_e500",
            "ram_e5a0",
            "ram_c800",
        )
    }

    city_records: list[dict[str, Any]] = []
    city_long_tables = (
        "ram_e000",
        "ram_e0a0",
        "ram_e140",
        "ram_e1e0",
        "ram_e280",
        "ram_e320",
        "ram_e3c0",
        "ram_e460",
        "ram_e500",
        "ram_e5a0",
    )
    for index in range(40):
        record: dict[str, Any] = {
            "scenario_index": scenario_index,
            "year": year,
            "city_id": index + 1,
            "ram_f428_raw_hex": _hex_record(table_data["ram_f428"], 1, index),
            "city_force_id_probable": table_data["ram_f428"][index],
            "ram_f460_raw_hex": _hex_record(table_data["ram_f460"], 2, index),
            "city_primary_officer_id_probable": words["ram_f460"][index],
        }
        for table_id in city_long_tables:
            record[f"{table_id}_raw_hex"] = _hex_record(table_data[table_id], 4, index)
            record[f"{table_id}_u32"] = longs[table_id][index]
        record.update(
            {
                "city_gold_u32_confirmed": longs["ram_e000"][index],
                "city_development_u16_confirmed": longs["ram_e1e0"][index] & 0xFFFF,
                "city_welfare_u16_confirmed": longs["ram_e320"][index] & 0xFFFF,
                "city_defense_u16_confirmed": longs["ram_e5a0"][index] & 0xFFFF,
            }
        )
        city_records.append(record)

    officer_records: list[dict[str, Any]] = []
    officer_word_tables = (
        "ram_b000",
        "ram_b200",
        "ram_b400",
        "ram_b600",
        "ram_b800",
        "ram_ba00",
        "ram_bc00",
        "ram_be00",
        "ram_c000",
    )
    officer_byte_tables = (
        "ram_c200",
        "ram_c300",
        "ram_c400",
        "ram_c500",
        "ram_c600",
        "ram_c700",
        "ram_cc00",
    )
    for officer_id in range(256):
        record = {
            "scenario_index": scenario_index,
            "year": year,
            "officer_id": officer_id,
        }
        for table_id in officer_word_tables:
            record[f"{table_id}_raw_hex"] = _hex_record(table_data[table_id], 2, officer_id)
            record[f"{table_id}_u16"] = words[table_id][officer_id]
        for table_id in officer_byte_tables:
            record[f"{table_id}_raw_hex"] = _hex_record(table_data[table_id], 1, officer_id)
            record[f"{table_id}_u8"] = table_data[table_id][officer_id]
        record["ram_c800_raw_hex"] = _hex_record(table_data["ram_c800"], 4, officer_id)
        record["ram_c800_u32"] = longs["ram_c800"][officer_id]
        record.update(
            {
                "officer_intelligence_u16_confirmed": words["ram_b600"][officer_id],
                "officer_progress_be_u16_confirmed": words["ram_be00"][officer_id],
                "officer_progress_c000_u16_confirmed": words["ram_c000"][officer_id],
                "officer_virtue_u8_confirmed": table_data["ram_c200"][officer_id],
                "officer_city_id_u8_confirmed": table_data["ram_cc00"][officer_id],
            }
        )
        officer_records.append(record)

    force_records: list[dict[str, Any]] = []
    city_force_ids = table_data["ram_f428"]
    for force_id in range(16):
        city_ids = [index + 1 for index, value in enumerate(city_force_ids) if value == force_id]
        force_records.append(
            {
                "scenario_index": scenario_index,
                "year": year,
                "force_id": force_id,
                "ram_e640_raw_hex": _hex_record(table_data["ram_e640"], 2, force_id),
                "force_primary_officer_id_probable": words["ram_e640"][force_id],
                "ram_e710_raw_hex": _hex_record(table_data["ram_e710"], 2, force_id),
                "ram_e710_u16_unknown": words["ram_e710"][force_id],
                "city_ids_derived_probable": city_ids,
            }
        )

    return {
        "scenario_index": scenario_index,
        "year": year,
        "cities": city_records,
        "officers": officer_records,
        "forces": force_records,
    }


def write_csv(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            converted = {
                key: ";".join(str(value) for value in item) if isinstance(item, list) else item
                for key, item in row.items()
            }
            writer.writerow(converted)


def write_json(path: Path, value: Any) -> None:
    path.write_bytes(
        (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
            "utf-8"
        )
    )


def extract_bundle(rom_path: Path, output_dir: Path) -> dict[str, Any]:
    rom = canonical_rom(rom_path)
    layouts = scenario_layout(rom)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, Any] = {
        "format": "g5510-scenario-static-data-v1",
        "canonical_rom": {
            "size": len(rom),
            "sha256": sha256_bytes(rom),
        },
        "scenario_pointer_table_rom_offset": SCENARIO_POINTER_TABLE,
        "scenario_pointer_table_rom_offset_hex": f"0x{SCENARIO_POINTER_TABLE:06X}",
        "scenario_count": SCENARIO_COUNT,
        "scenario_descriptor_size": SCENARIO_DESCRIPTOR_SIZE,
        "scenario_block_size": SCENARIO_BLOCK_SIZE,
        "confidence_policy": {
            "confirmed": "direct loader, copy routine or observed field",
            "probable": "strong code/index correlation; exact gameplay label still pending",
            "unknown": "address-oriented raw field only",
        },
        "scenarios": [],
    }

    all_cities: list[dict[str, Any]] = []
    all_officers: list[dict[str, Any]] = []
    all_forces: list[dict[str, Any]] = []

    for layout in layouts:
        scenario_index = layout["scenario_index"]
        year = layout["year"]
        scenario_dir = output_dir / f"scenario_{scenario_index}_{year}"
        tables_dir = scenario_dir / "tables"
        tables_dir.mkdir(parents=True, exist_ok=True)

        descriptor_base = layout["descriptor_rom_offset"]
        descriptor = rom[descriptor_base : descriptor_base + SCENARIO_DESCRIPTOR_SIZE]
        descriptor_path = scenario_dir / "descriptor.source.bin"
        descriptor_path.write_bytes(descriptor)
        block_path = scenario_dir / "scenario_block.source.bin"
        block_path.write_bytes(rom[descriptor_base : layout["block_rom_end"]])

        table_data: dict[str, bytes] = {}
        table_manifest: list[dict[str, Any]] = []
        for table in layout["tables"]:
            spec = TABLE_BY_ID[table["table_id"]]
            pointer = table["source_rom_offset"]
            source = rom[pointer : pointer + spec.source_length]
            runtime = runtime_bytes(spec, source)
            table_data[spec.table_id] = runtime
            source_relative = Path("tables") / f"{spec.table_id}.source.bin"
            runtime_relative = Path("tables") / f"{spec.table_id}.runtime.bin"
            (scenario_dir / source_relative).write_bytes(source)
            (scenario_dir / runtime_relative).write_bytes(runtime)
            table_manifest.append(
                {
                    **table,
                    "source_file": source_relative.as_posix(),
                    "source_sha256": sha256_bytes(source),
                    "runtime_file": runtime_relative.as_posix(),
                    "runtime_sha256": sha256_bytes(runtime),
                }
            )

        records = decoded_records(table_data, scenario_index, year)
        records_path = scenario_dir / "records.json"
        write_json(records_path, records)
        write_csv(scenario_dir / "cities.csv", records["cities"])
        write_csv(scenario_dir / "officers.csv", records["officers"])
        write_csv(scenario_dir / "forces.csv", records["forces"])
        all_cities.extend(records["cities"])
        all_officers.extend(records["officers"])
        all_forces.extend(records["forces"])

        scenario_manifest = {
            **{key: value for key, value in layout.items() if key != "tables"},
            "directory": scenario_dir.relative_to(output_dir).as_posix(),
            "descriptor_file": descriptor_path.relative_to(output_dir).as_posix(),
            "descriptor_sha256": sha256_bytes(descriptor),
            "scenario_block_file": block_path.relative_to(output_dir).as_posix(),
            "scenario_block_sha256": sha256_bytes(block_path.read_bytes()),
            "tables": table_manifest,
        }
        write_json(scenario_dir / "manifest.json", scenario_manifest)
        manifest["scenarios"].append(scenario_manifest)

    write_csv(output_dir / "all_cities.csv", all_cities)
    write_csv(output_dir / "all_officers.csv", all_officers)
    write_csv(output_dir / "all_forces.csv", all_forces)
    write_json(output_dir / "manifest.json", manifest)
    return manifest


def _checked_write(
    image: bytearray,
    ownership: dict[int, tuple[int, str]],
    offset: int,
    payload: bytes,
    label: str,
) -> None:
    end = offset + len(payload)
    if offset < 0 or end > len(image):
        raise ValueError(f"{label}: write 0x{offset:X}..0x{end:X} outside base ROM")
    for index, value in enumerate(payload):
        position = offset + index
        previous = ownership.get(position)
        if previous is not None and previous[0] != value:
            raise ValueError(
                f"conflicting writes at 0x{position:06X}: {previous[1]} "
                f"has 0x{previous[0]:02X}, {label} has 0x{value:02X}"
            )
        ownership[position] = (value, label)
    image[offset:end] = payload


def import_bundle(base_rom_path: Path, bundle_dir: Path, output_rom_path: Path) -> dict[str, Any]:
    if base_rom_path.resolve() == output_rom_path.resolve():
        raise ValueError("refusing to overwrite the base/original ROM in place")
    base = canonical_rom(base_rom_path)
    manifest = json.loads((bundle_dir / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("format") != "g5510-scenario-static-data-v1":
        raise ValueError("unsupported or missing bundle format")
    if manifest.get("canonical_rom", {}).get("sha256") != sha256_bytes(base):
        raise ValueError("provide the same base BIN used to extract the scenario bundle")

    image = bytearray(base)
    ownership: dict[int, tuple[int, str]] = {}
    for scenario in manifest["scenarios"]:
        scenario_index = scenario["scenario_index"]
        descriptor_base = scenario["descriptor_rom_offset"]
        descriptor_path = bundle_dir / scenario["descriptor_file"]
        descriptor = descriptor_path.read_bytes()
        if len(descriptor) != SCENARIO_DESCRIPTOR_SIZE:
            raise ValueError(f"scenario {scenario_index}: invalid descriptor length")

        # Match every descriptor pointer to its fixed manifest slot.
        for table in scenario["tables"]:
            pointer_in_descriptor = read_be32(descriptor, table["descriptor_offset"])
            if pointer_in_descriptor != table["source_rom_offset"]:
                raise ValueError(
                    f"scenario {scenario_index} {table['table_id']}: descriptor pointer "
                    f"0x{pointer_in_descriptor:06X} differs from fixed manifest pointer "
                    f"0x{table['source_rom_offset']:06X}; relocation is unsupported"
                )
        _checked_write(
            image,
            ownership,
            descriptor_base,
            descriptor,
            f"scenario_{scenario_index}:descriptor",
        )

        for table in scenario["tables"]:
            source_path = bundle_dir / scenario["directory"] / table["source_file"]
            source = source_path.read_bytes()
            if len(source) != table["source_length"]:
                raise ValueError(
                    f"scenario {scenario_index} {table['table_id']}: source length "
                    f"{len(source)} != {table['source_length']}"
                )
            _checked_write(
                image,
                ownership,
                table["source_rom_offset"],
                source,
                f"scenario_{scenario_index}:{table['table_id']}",
            )

    output_rom_path.parent.mkdir(parents=True, exist_ok=True)
    output_rom_path.write_bytes(image)
    changed = [index for index, (old, new) in enumerate(zip(base, image)) if old != new]
    return {
        "output": str(output_rom_path),
        "size": len(image),
        "sha256": sha256_bytes(image),
        "changed_byte_count": len(changed),
        "first_changed_offset": changed[0] if changed else None,
        "last_changed_offset": changed[-1] if changed else None,
        "written_byte_count": len(ownership),
    }


def verify_bundle(rom_path: Path, bundle_dir: Path) -> dict[str, Any]:
    canonical = canonical_rom(rom_path)
    with tempfile.TemporaryDirectory(prefix="g5510-static-roundtrip-") as temporary:
        rebuilt = Path(temporary) / "roundtrip.bin"
        result = import_bundle(rom_path, bundle_dir, rebuilt)
        rebuilt_bytes = rebuilt.read_bytes()
    if rebuilt_bytes != canonical:
        mismatch = next(
            index for index, (expected, actual) in enumerate(zip(canonical, rebuilt_bytes))
            if expected != actual
        )
        raise ValueError(f"round-trip mismatch at ROM 0x{mismatch:06X}")
    return {
        **result,
        "output": "temporary/roundtrip.bin",
        "exact_match": True,
    }


def command_extract(args: argparse.Namespace) -> int:
    manifest = extract_bundle(args.rom, args.output)
    print(
        f"extracted scenarios={manifest['scenario_count']} "
        f"output={args.output} sha256={manifest['canonical_rom']['sha256']}"
    )
    return 0


def command_import(args: argparse.Namespace) -> int:
    result = import_bundle(args.base_rom, args.bundle, args.output)
    print(json.dumps(result, sort_keys=True))
    return 0


def command_verify(args: argparse.Namespace) -> int:
    result = verify_bundle(args.rom, args.bundle)
    print(json.dumps(result, sort_keys=True))
    return 0


def command_roundtrip(args: argparse.Namespace) -> int:
    extract_bundle(args.rom, args.work_dir)
    result = import_bundle(args.rom, args.work_dir, args.output)
    if result["changed_byte_count"] != 0:
        raise ValueError("extract/import must reproduce the source BIN")
    print(json.dumps({**result, "exact_match": True}, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract_parser = subparsers.add_parser("extract", help="extract all scenario data")
    extract_parser.add_argument("--rom", type=Path, required=True)
    extract_parser.add_argument("--output", type=Path, required=True)
    extract_parser.set_defaults(func=command_extract)

    import_parser = subparsers.add_parser("import", help="import source files into a ROM copy")
    import_parser.add_argument("--base-rom", type=Path, required=True)
    import_parser.add_argument("--bundle", type=Path, required=True)
    import_parser.add_argument("--output", type=Path, required=True)
    import_parser.set_defaults(func=command_import)

    verify_parser = subparsers.add_parser("verify", help="verify an exact temporary round-trip")
    verify_parser.add_argument("--rom", type=Path, required=True)
    verify_parser.add_argument("--bundle", type=Path, required=True)
    verify_parser.set_defaults(func=command_verify)

    roundtrip_parser = subparsers.add_parser(
        "roundtrip", help="clean extract then import to a persistent output copy"
    )
    roundtrip_parser.add_argument("--rom", type=Path, required=True)
    roundtrip_parser.add_argument("--work-dir", type=Path, required=True)
    roundtrip_parser.add_argument("--output", type=Path, required=True)
    roundtrip_parser.set_defaults(func=command_roundtrip)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    sys.exit(main())
