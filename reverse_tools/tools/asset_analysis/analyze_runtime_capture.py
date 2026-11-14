#!/usr/bin/env python3
"""Correlate a MAME VRAM/Z80 capture with exact bytes in the original ROM."""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path

from scan_assets import (
    KNOWN_TEXT_POINTER_COUNT,
    KNOWN_TEXT_POINTER_TABLE,
    be16,
    be32,
    find_immediate_text_pointer_refs,
    find_known_text_records,
    require_g5510_rom,
    sha256,
    write_csv,
)
from tools.audio_analysis.z80_payload import compose_runtime, extract_components


def all_occurrences(data: bytes, needle: bytes, limit: int = 64) -> list[int]:
    results: list[int] = []
    start = 0
    while len(results) < limit:
        found = data.find(needle, start)
        if found < 0:
            break
        results.append(found)
        start = found + 1
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, required=True, help="linear G-5510 BIN")
    parser.add_argument("--vram", type=Path, required=True)
    parser.add_argument("--z80", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="fresh output directory")
    args = parser.parse_args()

    rom = args.rom.resolve().read_bytes()
    try:
        require_g5510_rom(rom)
    except ValueError as error:
        parser.error(str(error))
    vram = args.vram.resolve().read_bytes()
    z80 = args.z80.resolve().read_bytes()
    if len(vram) != 0x10000:
        raise SystemExit(f"expected 0x10000-byte VRAM capture, got {len(vram):#x}")
    if len(z80) != 0x1E00:
        raise SystemExit(f"expected 0x1E00-byte Z80 capture, got {len(z80):#x}")
    if args.output.is_symlink():
        parser.error("--output must name a fresh directory")
    output = args.output.resolve()
    output.mkdir(parents=True)

    vram_invalid_reason = ""
    if len(set(vram)) <= 1:
        vram_invalid_reason = "capture is entirely one byte value; MAME videoram read path was not exposed"
    elif vram == rom[: len(vram)]:
        vram_invalid_reason = "capture aliases the main ROM, not VDP VRAM"
    vram_valid = not vram_invalid_reason

    rows: list[dict[str, object]] = []
    page_counts: collections.Counter[int] = collections.Counter()
    exact_unique_tiles = 0
    exact_matched_tiles = 0
    for tile_index in range(0x800 if vram_valid else 0):
        tile = vram[tile_index * 32 : tile_index * 32 + 32]
        uniform = len(set(tile)) <= 1
        hits = [] if uniform else all_occurrences(rom, tile)
        if not uniform:
            exact_unique_tiles += 1
        if hits:
            exact_matched_tiles += 1
            for hit in hits:
                page_counts[hit // 0x1000] += 1
        rows.append(
            {
                "tile_index": tile_index,
                "tile_index_hex": f"0x{tile_index:03X}",
                "vram_start_hex": f"0x{tile_index * 32:04X}",
                "sha1": hashlib.sha1(tile).hexdigest(),
                "uniform": uniform,
                "rom_exact_match_count": len(hits),
                "rom_offsets": " ".join(f"0x{hit:06X}" for hit in hits),
                "status": "confirmed_exact_match" if hits else ("uninformative_uniform" if uniform else "no_exact_rom_match"),
                "caveat": "no exact match can mean decompressed/transformed/runtime-generated data",
            }
        )
    write_csv(output / "runtime_vram_tile_exact_matches.csv", rows)
    page_rows = [
        {
            "rom_page_start": page * 0x1000,
            "rom_page_start_hex": f"0x{page * 0x1000:06X}",
            "matching_vram_tile_occurrences": count,
            "status": "confirmed_exact_byte_correlation",
        }
        for page, count in page_counts.most_common()
    ]
    write_csv(output / "runtime_vram_rom_page_correlations.csv", page_rows)

    # Gather tile indices encoded in the validated text token records.  This is
    # a VDP-word hypothesis: low 11 bits are treated as a tile index, while the
    # upper five bits are retained separately as attributes.
    _, known_records, _ = find_known_text_records(rom)
    _, direct_records = find_immediate_text_pointer_refs(rom)
    referenced: dict[int, collections.Counter[int]] = collections.defaultdict(collections.Counter)
    for record in [*known_records, *direct_records]:
        tokens = [int(value, 16) for value in str(record["tokens_hex"]).split()]
        for token in tokens:
            if token in (0xFFFF, 0x8000):
                continue
            referenced[token & 0x7FF][token >> 11] += 1
    text_tile_rows: list[dict[str, object]] = []
    by_index = {int(row["tile_index"]): row for row in rows}
    for tile_index, attrs in sorted(referenced.items()) if vram_valid else []:
        match = by_index[tile_index]
        text_tile_rows.append(
            {
                "tile_index": tile_index,
                "tile_index_hex": f"0x{tile_index:03X}",
                "attribute_counts": " ".join(f"{value}:{count}" for value, count in sorted(attrs.items())),
                "vram_sha1": match["sha1"],
                "rom_exact_match_count": match["rom_exact_match_count"],
                "rom_offsets": match["rom_offsets"],
                "status": "candidate_vdp_text_word_interpretation",
                "caveat": "candidate interpretation of tile and control words",
            }
        )
    write_csv(output / "runtime_text_token_tile_hypothesis.csv", text_tile_rows)

    expected, _ = compose_runtime(extract_components(rom))
    differences = [index for index, (left, right) in enumerate(zip(expected, z80)) if left != right]
    matching = len(expected) - len(differences)
    z80_result = {
        "capture_sha256": sha256(z80),
        "expected_sha256": sha256(expected),
        "size": len(z80),
        "matching_bytes": matching,
        "different_bytes": len(differences),
        "match_ratio": matching / len(expected),
        "first_difference_offsets": [f"0x{offset:04X}" for offset in differences[:128]],
        "static_transfer_validation": {"validated": True, "runtime_size": len(expected)},
    }

    result = {
        "schema_version": 1,
        "rom_sha256": sha256(rom),
        "vram_capture": {
            "path": args.vram.name,
            "sha256": sha256(vram),
            "size": len(vram),
            "valid": vram_valid,
            "invalid_reason": vram_invalid_reason,
            "nonuniform_tiles": exact_unique_tiles,
            "tiles_with_at_least_one_exact_rom_match": exact_matched_tiles,
            "exact_match_ratio": exact_matched_tiles / exact_unique_tiles if exact_unique_tiles else 0.0,
            "rom_pages_with_matches": len(page_counts),
        },
        "text_vdp_word_hypothesis": {
            "unique_tile_indices": len(referenced),
            "rows_with_exact_rom_match": sum(int(row["rom_exact_match_count"]) > 0 for row in text_tile_rows),
        },
        "z80_capture": z80_result,
    }
    (output / "runtime_capture_analysis.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
