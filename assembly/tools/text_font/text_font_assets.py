#!/usr/bin/env python3
"""Losslessly extract/import the confirmed G-5510 text and font assets.

The canonical ROM is never modified in place.  ``extract`` refuses an unknown
ROM and creates a new asset directory.  ``import`` starts from the exact
canonical ROM and writes a new file, enforcing fixed-size regions and the known
52-pointer-table invariants.
"""

from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import binascii
import csv
import hashlib
import json
import math
import struct
import zlib
from collections import Counter
from pathlib import Path
from typing import Iterable


EXPECTED_ROM_SHA256 = reference_value(__name__, 'EXPECTED_ROM_SHA256')
EXPECTED_ROM_SIZE = 0x100000

POINTER_TABLE_START = 0x028240
POINTER_COUNT = 52
POINTER_TABLE_END = POINTER_TABLE_START + POINTER_COUNT * 4
TABLE_RECORDS_START = 0x028310
TABLE_RECORDS_END = 0x0288BA

FONT16_START = 0x08159C
FONT16_END = 0x0896DC
FONT16_BYTES_PER_GLYPH = 32
FONT16_GLYPH_COUNT = (FONT16_END - FONT16_START) // FONT16_BYTES_PER_GLYPH

FONT8_START = 0x0896DC
FONT8_END = 0x089EDC
FONT8_BYTES_PER_GLYPH = 8
FONT8_GLYPH_COUNT = (FONT8_END - FONT8_START) // FONT8_BYTES_PER_GLYPH

FIXED_ASSET_LAYOUT = {
    "pointer_table": ("pointer_table_52.bin", POINTER_TABLE_START, POINTER_TABLE_END),
    "pointer_table_records": (
        "pointer_table_52_records.bin",
        TABLE_RECORDS_START,
        TABLE_RECORDS_END,
    ),
    "font16": ("font16_1bpp.bin", FONT16_START, FONT16_END),
    "font8": ("font8_1bpp.bin", FONT8_START, FONT8_END),
}
DIRECT_ASSET_FILE = "direct_ff700e_records.bin"

TEXT_POINTER_DESTINATION = b"\x00\xff\x70\x0e"
MOVE_LONG_IMMEDIATE_ABSOLUTE = b"\x23\xfc"
DIRECT_RECORD_LIMIT = 0x400

CONTROL_NAMES = {
    0x8000: "end_stream_8000",
    0x8002: "layout_control_8002",
    0x8008: "colour_source_8008",
    0x800A: "colour_source_800A",
    0x800E: "colour_source_800E",
    0x8010: "dynamic_insert_8010",
    0x8011: "dynamic_insert_8011",
    0x8012: "dynamic_insert_8012",
    0xFF00: "colour_source_ff00",
    0xFF01: "colour_source_ff01",
    0xFF02: "colour_source_ff02",
    0xFF03: "colour_source_ff03",
    0xFF0A: "cursor_set_cb00",
    0xFF20: "row_advance_0040",
    0xFFFF: "end_stream_ffff",
}


class AssetError(ValueError):
    """Raised when an input violates a proven format or safety invariant."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def be16(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset : offset + 2], "big")


def be32(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset : offset + 4], "big")


def put_be32(data: bytearray, offset: int, value: int) -> None:
    data[offset : offset + 4] = value.to_bytes(4, "big")


def validate_rom(data: bytes) -> None:
    if len(data) != EXPECTED_ROM_SIZE:
        raise AssetError(f"expected a 0x100000-byte linear ROM, got {len(data):#x}")
    actual = sha256(data)
    if actual != EXPECTED_ROM_SHA256:
        raise AssetError(f"refusing non-canonical ROM SHA-256 {actual}")


def font16_offset(token: int) -> int:
    """Reproduce the word-sized shifts/OR at ROM 0x00AE92-0x00AEA2."""
    if not 0 <= token <= 0xFFFF:
        raise AssetError(f"token is not a word: {token!r}")
    high_component = ((token & 0xFF00) << 3) & 0xFFFF
    low_component = ((token & 0x00FF) << 5) & 0xFFFF
    return high_component | low_component


def font16_index(token: int) -> int:
    offset = font16_offset(token)
    if offset % FONT16_BYTES_PER_GLYPH:
        raise AssetError(f"token {token:04X} produces an unaligned font offset")
    return offset // FONT16_BYTES_PER_GLYPH


def font16_row_column(token: int) -> tuple[int, int]:
    """Return the 32x64 row/column encoding used by all observed glyph tokens."""
    column = token & 0xFF
    if column > 0x3F:
        raise AssetError(f"token {token:04X} has an unobserved column above 0x3F")
    return (token >> 8) & 0x1F, column


def parse_pointer_table(rom: bytes) -> list[int]:
    pointers = [be32(rom, POINTER_TABLE_START + index * 4) for index in range(POINTER_COUNT)]
    if pointers[0] != POINTER_TABLE_END or pointers[0] != TABLE_RECORDS_START:
        raise AssetError(f"first text pointer is {pointers[0]:#x}, expected {TABLE_RECORDS_START:#x}")
    if pointers != sorted(set(pointers)):
        raise AssetError("52-entry text pointers are not strictly increasing")
    if any(pointer & 1 for pointer in pointers):
        raise AssetError("52-entry text pointer table contains an odd address")
    if not all(TABLE_RECORDS_START <= pointer < TABLE_RECORDS_END for pointer in pointers):
        raise AssetError("52-entry text pointer escapes the confirmed record block")
    return pointers


def table_records(rom: bytes, pointers: list[int]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    ends = [*pointers[1:], TABLE_RECORDS_END]
    for index, (start, end) in enumerate(zip(pointers, ends)):
        if end <= start or (end - start) % 2:
            raise AssetError(f"invalid table record {index} bounds {start:#x}..{end:#x}")
        tokens = [be16(rom, offset) for offset in range(start, end, 2)]
        if not tokens or tokens[-1] != 0xFFFF:
            raise AssetError(f"table record {index} does not end in FFFF")
        records.append(
            {
                "group": "pointer_table_52",
                "index": index,
                "start": start,
                "end": end,
                "tokens": tokens,
                "terminator": 0xFFFF,
                "dialect": "ff_control_stream",
            }
        )
    return records


def parse_terminated_record(rom: bytes, start: int) -> dict[str, object]:
    if start < 0 or start >= len(rom) or start & 1:
        raise AssetError(f"invalid direct text pointer {start:#x}")
    tokens: list[int] = []
    for offset in range(start, min(start + DIRECT_RECORD_LIMIT, len(rom)), 2):
        token = be16(rom, offset)
        tokens.append(token)
        if token in (0x8000, 0xFFFF):
            return {
                "start": start,
                "end": offset + 2,
                "tokens": tokens,
                "terminator": token,
                "dialect": "80_control_stream" if token == 0x8000 else "ff_control_stream",
            }
    raise AssetError(f"direct text record at {start:#x} has no bounded terminator")


def discover_direct_records(rom: bytes) -> list[dict[str, object]]:
    references: dict[int, list[int]] = {}
    for offset in range(0, len(rom) - 10, 2):
        if rom[offset : offset + 2] != MOVE_LONG_IMMEDIATE_ABSOLUTE:
            continue
        if rom[offset + 6 : offset + 10] != TEXT_POINTER_DESTINATION:
            continue
        target = be32(rom, offset + 2)
        if target >= len(rom) or target & 1:
            continue
        references.setdefault(target, []).append(offset)

    records: list[dict[str, object]] = []
    packed_offset = 0
    for index, target in enumerate(sorted(references)):
        record = parse_terminated_record(rom, target)
        record.update(
            {
                "group": "immediate_ff700e",
                "index": index,
                "reference_offsets": references[target],
                "packed_offset": packed_offset,
            }
        )
        packed_offset += int(record["end"]) - int(record["start"])
        records.append(record)
    return records


def classify_token(token: int) -> tuple[str, int | None]:
    if token in CONTROL_NAMES:
        return CONTROL_NAMES[token], None
    if token & 0x8000:
        return "unknown_negative_control", None
    return "glyph", font16_index(token)


def validate_glyph_tokens(
    records: Iterable[dict[str, object]], *, reject_unknown_controls: bool = False
) -> list[int]:
    indices: set[int] = set()
    for record in records:
        for token in record["tokens"]:  # type: ignore[index]
            classification, index = classify_token(int(token))
            if classification == "unknown_negative_control" and reject_unknown_controls:
                raise AssetError(f"unknown negative control token {int(token):04X}")
            if classification != "glyph":
                continue
            font16_row_column(int(token))
            assert index is not None
            if index >= FONT16_GLYPH_COUNT:
                raise AssetError(
                    f"glyph token {int(token):04X} resolves to {index:#x}, "
                    f"past the confirmed 16x16 font end"
                )
            indices.add(index)
    return sorted(indices)


def png_chunk(kind: bytes, payload: bytes) -> bytes:
    body = kind + payload
    return struct.pack(">I", len(payload)) + body + struct.pack(">I", binascii.crc32(body) & 0xFFFFFFFF)


def write_grayscale_png(path: Path, rows: list[bytes]) -> None:
    if not rows or not rows[0]:
        raise AssetError("cannot render an empty PNG")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise AssetError("PNG rows have inconsistent widths")
    raw = b"".join(b"\x00" + row for row in rows)
    ihdr = struct.pack(">IIBBBBB", width, len(rows), 8, 0, 0, 0, 0)
    payload = (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", ihdr)
        + png_chunk(b"IDAT", zlib.compress(raw, level=9))
        + png_chunk(b"IEND", b"")
    )
    path.write_bytes(payload)


def decode_1bpp_glyph(raw: bytes, width: int, height: int) -> list[list[int]]:
    row_bytes = math.ceil(width / 8)
    if len(raw) != row_bytes * height:
        raise AssetError("1bpp glyph has the wrong byte length")
    pixels: list[list[int]] = []
    for y in range(height):
        row: list[int] = []
        for byte in raw[y * row_bytes : (y + 1) * row_bytes]:
            row.extend(0 if byte & (0x80 >> bit) else 255 for bit in range(8))
        pixels.append(row[:width])
    return pixels


def render_font_sheet(
    data: bytes,
    *,
    glyph_width: int,
    glyph_height: int,
    bytes_per_glyph: int,
    columns: int,
    selected_indices: list[int] | None = None,
) -> list[bytes]:
    available = len(data) // bytes_per_glyph
    indices = selected_indices if selected_indices is not None else list(range(available))
    if any(index < 0 or index >= available for index in indices):
        raise AssetError("font sheet selection is outside the extracted font")
    gap = 1
    rows_count = math.ceil(len(indices) / columns)
    width = columns * (glyph_width + gap) - gap
    height = rows_count * (glyph_height + gap) - gap
    canvas = [bytearray([255]) * width for _ in range(height)]
    for sheet_index, glyph_index in enumerate(indices):
        x0 = (sheet_index % columns) * (glyph_width + gap)
        y0 = (sheet_index // columns) * (glyph_height + gap)
        raw = data[glyph_index * bytes_per_glyph : (glyph_index + 1) * bytes_per_glyph]
        glyph = decode_1bpp_glyph(raw, glyph_width, glyph_height)
        for y, row in enumerate(glyph):
            canvas[y0 + y][x0 : x0 + glyph_width] = bytes(row)
    return [bytes(row) for row in canvas]


def write_token_csv(path: Path, records: Iterable[dict[str, object]]) -> None:
    fields = [
        "group",
        "record_index",
        "record_start_hex",
        "token_offset",
        "token_hex",
        "classification",
        "glyph_index_hex",
        "glyph_rom_start_hex",
        "attribute_bits_hex",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            start = int(record["start"])
            for token_offset, token_value in enumerate(record["tokens"]):  # type: ignore[index]
                token = int(token_value)
                classification, glyph_index_value = classify_token(token)
                writer.writerow(
                    {
                        "group": record["group"],
                        "record_index": record["index"],
                        "record_start_hex": f"0x{start:06X}",
                        "token_offset": token_offset,
                        "token_hex": f"0x{token:04X}",
                        "classification": classification,
                        "glyph_index_hex": "" if glyph_index_value is None else f"0x{glyph_index_value:03X}",
                        "glyph_rom_start_hex": ""
                        if glyph_index_value is None
                        else f"0x{FONT16_START + glyph_index_value * 32:06X}",
                        "attribute_bits_hex": "" if glyph_index_value is None else f"0x{token & 0xE000:04X}",
                    }
                )


def file_descriptor(path: Path, start: int, end: int) -> dict[str, object]:
    data = path.read_bytes()
    if len(data) != end - start:
        raise AssetError(f"{path.name} length does not match its ROM interval")
    return {
        "file": path.name,
        "rom_start": start,
        "rom_end": end,
        "length": len(data),
        "sha256": sha256(data),
    }


def extract_assets(rom_path: Path, output: Path) -> dict[str, object]:
    rom = rom_path.resolve().read_bytes()
    validate_rom(rom)
    if output.exists():
        raise AssetError(f"refusing to overwrite existing output directory: {output}")
    output.mkdir(parents=True)

    pointers = parse_pointer_table(rom)
    table = table_records(rom, pointers)
    direct = discover_direct_records(rom)
    all_records = [*table, *direct]
    referenced_indices = validate_glyph_tokens(all_records)

    pointer_path = output / "pointer_table_52.bin"
    table_records_path = output / "pointer_table_52_records.bin"
    direct_path = output / "direct_ff700e_records.bin"
    font16_path = output / "font16_1bpp.bin"
    font8_path = output / "font8_1bpp.bin"

    pointer_path.write_bytes(rom[POINTER_TABLE_START:POINTER_TABLE_END])
    table_records_path.write_bytes(rom[TABLE_RECORDS_START:TABLE_RECORDS_END])
    direct_path.write_bytes(
        b"".join(rom[int(record["start"]) : int(record["end"])] for record in direct)
    )
    font16_path.write_bytes(rom[FONT16_START:FONT16_END])
    font8_path.write_bytes(rom[FONT8_START:FONT8_END])

    write_grayscale_png(
        output / "font16_sheet.png",
        render_font_sheet(
            font16_path.read_bytes(),
            glyph_width=16,
            glyph_height=16,
            bytes_per_glyph=32,
            columns=32,
        ),
    )
    write_grayscale_png(
        output / "font16_referenced_sheet.png",
        render_font_sheet(
            font16_path.read_bytes(),
            glyph_width=16,
            glyph_height=16,
            bytes_per_glyph=32,
            columns=32,
            selected_indices=referenced_indices,
        ),
    )
    write_grayscale_png(
        output / "font8_sheet.png",
        render_font_sheet(
            font8_path.read_bytes(),
            glyph_width=8,
            glyph_height=8,
            bytes_per_glyph=8,
            columns=16,
        ),
    )
    write_token_csv(output / "tokens.csv", all_records)

    controls = Counter()
    unknown_negative = Counter()
    for record in all_records:
        for token_value in record["tokens"]:  # type: ignore[index]
            token = int(token_value)
            classification, _ = classify_token(token)
            if token in CONTROL_NAMES:
                controls[f"0x{token:04X}"] += 1
            elif classification == "unknown_negative_control":
                unknown_negative[f"0x{token:04X}"] += 1

    manifest: dict[str, object] = {
        "schema_version": 1,
        "source_rom": {
            "path": str(rom_path.resolve()),
            "size": len(rom),
            "sha256": sha256(rom),
        },
        "evidence": {
            "pointer_table": "confirmed: 0x028228 indexed BE32 consumer and structural validation",
            "font16": "confirmed base/layout: 0x00AE8A/0x00AF04; end is the next confirmed 8x8 font base",
            "font8": "confirmed base/layout: 0x00AF1E indexes 256 entries of 8 bytes",
            "direct_records": "confirmed pointers: MOVE.L #target,$00FF700E; terminators confirmed by consumers",
        },
        "assets": {
            "pointer_table": file_descriptor(pointer_path, POINTER_TABLE_START, POINTER_TABLE_END),
            "pointer_table_records": file_descriptor(
                table_records_path, TABLE_RECORDS_START, TABLE_RECORDS_END
            ),
            "font16": file_descriptor(font16_path, FONT16_START, FONT16_END),
            "font8": file_descriptor(font8_path, FONT8_START, FONT8_END),
            "direct_records": {
                "file": direct_path.name,
                "length": direct_path.stat().st_size,
                "sha256": sha256(direct_path.read_bytes()),
                "records": direct,
            },
        },
        "pointer_table": {
            "count": len(pointers),
            "pointers": pointers,
            "records": table,
        },
        "font16": {
            "glyph_count": FONT16_GLYPH_COUNT,
            "bytes_per_glyph": 32,
            "geometry": "16x16 1bpp, two bytes per row, MSB-left",
            "token_offset_formula": "(((token & 0xFF00) << 3) & 0xFFFF) | ((token & 0x00FF) << 5)",
            "observed_grid": "row=(token>>8)&0x1F, column=token&0x3F, index=row*64+column",
            "referenced_indices": referenced_indices,
        },
        "font8": {
            "glyph_count": FONT8_GLYPH_COUNT,
            "bytes_per_glyph": 8,
            "geometry": "8x8 1bpp, one byte per row, MSB-left",
        },
        "control_histogram": dict(sorted(controls.items())),
        "unknown_negative_tokens": dict(sorted(unknown_negative.items())),
        "unicode_mapping": {
            "status": "unknown",
            "note": "No token-to-Unicode assignments are fabricated by this extractor.",
        },
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def read_fixed_asset(directory: Path, descriptor: dict[str, object]) -> bytes:
    path = directory / str(descriptor["file"])
    data = path.read_bytes()
    expected = int(descriptor["length"])
    if len(data) != expected:
        raise AssetError(f"{path.name}: expected {expected:#x} bytes, got {len(data):#x}")
    return data


def import_assets(base_rom_path: Path, assets_dir: Path, output_path: Path) -> bytes:
    base = base_rom_path.resolve().read_bytes()
    validate_rom(base)
    if output_path.exists():
        raise AssetError(f"refusing to overwrite existing output file: {output_path}")
    manifest = json.loads((assets_dir / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1:
        raise AssetError("unsupported text/font asset manifest schema")
    source = manifest.get("source_rom")
    if not isinstance(source, dict) or source.get("sha256") != EXPECTED_ROM_SHA256:
        raise AssetError("manifest is not tied to the canonical ROM")
    assets = manifest["assets"]
    if not isinstance(assets, dict):
        raise AssetError("manifest assets entry is not an object")
    rebuilt = bytearray(base)

    # Placement metadata is evidence, not an editable relocation mechanism.
    # Pin it to the code-confirmed regions so a changed manifest cannot direct
    # an otherwise valid asset over unrelated ROM bytes.
    for name, (expected_file, expected_start, expected_end) in FIXED_ASSET_LAYOUT.items():
        descriptor = assets[name]
        if not isinstance(descriptor, dict):
            raise AssetError(f"{name}: manifest descriptor is not an object")
        if descriptor.get("file") != expected_file:
            raise AssetError(f"{name}: manifest file must remain {expected_file}")
        if int(descriptor.get("rom_start", -1)) != expected_start:
            raise AssetError(f"{name}: manifest ROM start was changed")
        if int(descriptor.get("rom_end", -1)) != expected_end:
            raise AssetError(f"{name}: manifest ROM end was changed")
        if int(descriptor.get("length", -1)) != expected_end - expected_start:
            raise AssetError(f"{name}: manifest length was changed")
        data = read_fixed_asset(assets_dir, descriptor)
        rebuilt[expected_start:expected_end] = data

    direct_descriptor = assets["direct_records"]
    if not isinstance(direct_descriptor, dict):
        raise AssetError("direct_records: manifest descriptor is not an object")
    expected_direct = discover_direct_records(base)
    expected_packed_length = sum(
        int(record["end"]) - int(record["start"]) for record in expected_direct
    )
    if direct_descriptor.get("file") != DIRECT_ASSET_FILE:
        raise AssetError(f"direct_records: manifest file must remain {DIRECT_ASSET_FILE}")
    if int(direct_descriptor.get("length", -1)) != expected_packed_length:
        raise AssetError("direct_records: manifest length was changed")
    described_records = direct_descriptor.get("records")
    if not isinstance(described_records, list) or len(described_records) != len(expected_direct):
        raise AssetError("direct_records: manifest record list was changed")
    for described, expected in zip(described_records, expected_direct):
        if not isinstance(described, dict):
            raise AssetError("direct_records: malformed record descriptor")
        for field in ("start", "end", "packed_offset"):
            if int(described.get(field, -1)) != int(expected[field]):
                raise AssetError(f"direct_records: manifest {field} was changed")

    packed = read_fixed_asset(assets_dir, direct_descriptor)
    for record in expected_direct:
        start = int(record["start"])
        end = int(record["end"])
        packed_offset = int(record["packed_offset"])
        length = end - start
        rebuilt[start:end] = packed[packed_offset : packed_offset + length]

    # Reject malformed edits even though same-size token/glyph changes are allowed.
    pointers = parse_pointer_table(rebuilt)
    parsed_records = table_records(rebuilt, pointers)
    for record in expected_direct:
        parsed = parse_terminated_record(rebuilt, int(record["start"]))
        if int(parsed["end"]) != int(record["end"]):
            raise AssetError(
                f"direct record at {int(record['start']):#x} changed its fixed-size boundary"
            )
        parsed_records.append(parsed)
    validate_glyph_tokens(parsed_records, reject_unknown_controls=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(rebuilt)
    return bytes(rebuilt)


def default_rom_path() -> Path:
    return Path(__file__).resolve().parents[3] / "work" / "original_g5510.bin"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract = subparsers.add_parser("extract", help="extract confirmed text/font assets")
    extract.add_argument("--rom", type=Path, default=default_rom_path())
    extract.add_argument("--output", type=Path, required=True)

    importer = subparsers.add_parser("import", help="write assets into a new canonical-ROM copy")
    importer.add_argument("--rom", type=Path, default=default_rom_path())
    importer.add_argument("--assets", type=Path, required=True)
    importer.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "extract":
            manifest = extract_assets(args.rom, args.output.resolve())
            print(
                f"extracted 52 table records, "
                f"{len(manifest['assets']['direct_records']['records'])} direct records, "
                f"{manifest['font16']['glyph_count']} 16x16 slots"
            )
        else:
            rebuilt = import_assets(args.rom, args.assets.resolve(), args.output.resolve())
            print(f"wrote {args.output.resolve()} sha256={sha256(rebuilt)}")
    except (AssetError, OSError, KeyError, json.JSONDecodeError) as error:
        raise SystemExit(f"error: {error}") from error
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
