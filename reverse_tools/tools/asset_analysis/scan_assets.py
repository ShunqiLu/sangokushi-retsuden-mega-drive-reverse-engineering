#!/usr/bin/env python3
"""Map resources and candidate structures in the G-5510 linear ROM.

Pillow provides PNG previews. MAME's unidasm provides an optional independent
listing of the extracted Z80 address-space payload.
"""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import math
import statistics
import struct
import subprocess
import sys
import zlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.rom_layout import require_g5510_rom

# Independently validated in the surrounding reverse-engineering work.  The
# code at 0x28228 indexes this table with index*4 and writes the selected long
# pointer to RAM 0xFF700E.
KNOWN_TEXT_POINTER_TABLE = 0x28240
KNOWN_TEXT_POINTER_COUNT = 52

WINDOW_SIZE = 0x1000
ENTROPY_SUBWINDOW = 0x400
RAW_TILE_BANK_SIZE = 0x2000


@dataclass
class Segment:
    start: int
    end: int
    label: str
    status: str
    confidence: str
    category: str
    evidence: list[str]
    caveats: list[str]

    @property
    def size(self) -> int:
        return self.end - self.start

    def serializable(self) -> dict[str, Any]:
        row = asdict(self)
        row["size"] = self.size
        row["start_hex"] = f"0x{self.start:06X}"
        row["end_hex"] = f"0x{self.end:06X}"
        return row


def be16(data: bytes, offset: int) -> int:
    return struct.unpack_from(">H", data, offset)[0]


def be32(data: bytes, offset: int) -> int:
    return struct.unpack_from(">I", data, offset)[0]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = collections.Counter(data)
    length = len(data)
    return -sum((count / length) * math.log2(count / length) for count in counts.values())


def ratio(count: int, total: int) -> float:
    return count / total if total else 0.0


def longest_run(data: bytes, byte_value: int) -> int:
    longest = current = 0
    for value in data:
        if value == byte_value:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def token_pair_score(data: bytes) -> float:
    """Score the structure of the two cartridge token families.

    Family A uses glyph-like words with high bytes 0x00..0x0F and FFxx
    controls.  Family B uses high bytes 0x40..0x50 and 80xx controls.  This is
    only a structural score and must not be treated as a character mapping.
    """
    usable = len(data) & ~1
    if not usable:
        return 0.0
    good = 0
    for offset in range(0, usable, 2):
        high = data[offset]
        low = data[offset + 1]
        family_a = high <= 0x0F or high == 0xFF
        family_b = 0x40 <= high <= 0x50 or high == 0x80
        control_like = high in (0x80, 0xFF) and low <= 0xFF
        if family_a or family_b or control_like:
            good += 1
    return good / (usable // 2)


def window_metrics(data: bytes, start: int, size: int) -> dict[str, Any]:
    chunk = data[start : min(start + size, len(data))]
    counts = collections.Counter(chunk)
    dominant_byte, dominant_count = counts.most_common(1)[0] if counts else (0, 0)
    printable = sum(value in (9, 10, 13) or 0x20 <= value <= 0x7E for value in chunk)
    return {
        "start": start,
        "end": start + len(chunk),
        "start_hex": f"0x{start:06X}",
        "end_hex": f"0x{start + len(chunk):06X}",
        "size": len(chunk),
        "entropy": round(shannon_entropy(chunk), 6),
        "zero_ratio": round(ratio(counts.get(0, 0), len(chunk)), 6),
        "ff_ratio": round(ratio(counts.get(0xFF, 0), len(chunk)), 6),
        "printable_ascii_ratio": round(ratio(printable, len(chunk)), 6),
        "unique_bytes": len(counts),
        "dominant_byte": f"0x{dominant_byte:02X}",
        "dominant_ratio": round(ratio(dominant_count, len(chunk)), 6),
        "longest_zero_run": longest_run(chunk, 0),
        "longest_ff_run": longest_run(chunk, 0xFF),
        "custom_token_pair_score": round(token_pair_score(chunk), 6),
    }


def classify_statistical_page(row: dict[str, Any]) -> tuple[str, str]:
    fill = max(row["zero_ratio"], row["ff_ratio"])
    entropy = row["entropy"]
    if fill >= 0.98:
        return "filler", "confirmed"
    if entropy < 2.0:
        return "low_entropy_structured_or_sparse", "unknown"
    if entropy < 5.5:
        return "medium_entropy_structured", "unknown"
    if entropy < 7.2:
        return "high_entropy_mixed", "unknown"
    return "very_high_entropy_compressed_or_dense_candidate", "candidate"


def find_fill_runs(data: bytes, minimum: int = 64) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    index = 0
    while index < len(data):
        value = data[index]
        if value not in (0x00, 0xFF):
            index += 1
            continue
        end = index + 1
        while end < len(data) and data[end] == value:
            end += 1
        if end - index >= minimum:
            rows.append(
                {
                    "start": index,
                    "end": end,
                    "start_hex": f"0x{index:06X}",
                    "end_hex": f"0x{end:06X}",
                    "length": end - index,
                    "byte": f"0x{value:02X}",
                    "status": "confirmed",
                    "evidence": f"exact run of {end - index} identical bytes",
                }
            )
        index = end
    return rows


def find_ascii_strings(data: bytes, minimum: int = 6) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    start: int | None = None
    for index, value in enumerate(data + b"\x00"):
        printable = 0x20 <= value <= 0x7E
        if printable and start is None:
            start = index
        elif not printable and start is not None:
            if index - start >= minimum:
                raw = data[start:index]
                rows.append(
                    {
                        "start": start,
                        "end": index,
                        "start_hex": f"0x{start:06X}",
                        "end_hex": f"0x{index:06X}",
                        "length": index - start,
                        "ascii": raw.decode("ascii"),
                        "status": "confirmed_bytes_only",
                    }
                )
            start = None
    return rows


def pointer_valid(value: int, size: int) -> bool:
    return 0x200 <= value < size and value % 2 == 0


def find_u32_pointer_runs(data: bytes, minimum_count: int = 6) -> list[dict[str, Any]]:
    """Find contiguous BE32 values that could be absolute ROM pointers.

    The test is intentionally strict (in-ROM and even) yet still heuristic:
    numeric tables can satisfy it by accident.  Therefore every generic hit
    remains a candidate until a code cross-reference or runtime consumer is
    established.
    """
    candidates: list[dict[str, Any]] = []
    index = 0
    while index + 4 <= len(data):
        if index % 2 or not pointer_valid(be32(data, index), len(data)):
            index += 2
            continue
        start = index
        values: list[int] = []
        while index + 4 <= len(data):
            value = be32(data, index)
            if not pointer_valid(value, len(data)):
                break
            values.append(value)
            index += 4
        if len(values) >= minimum_count:
            monotonic_pairs = sum(a <= b for a, b in zip(values, values[1:]))
            strict_pairs = sum(a < b for a, b in zip(values, values[1:]))
            pair_count = max(1, len(values) - 1)
            target_samples = b"".join(data[v : min(v + 16, len(data))] for v in values[:64])
            known_table = start == KNOWN_TEXT_POINTER_TABLE and len(values) == KNOWN_TEXT_POINTER_COUNT
            candidates.append(
                {
                    "start": start,
                    "end": start + len(values) * 4,
                    "start_hex": f"0x{start:06X}",
                    "end_hex": f"0x{start + len(values) * 4:06X}",
                    "count": len(values),
                    "target_min": min(values),
                    "target_max": max(values),
                    "target_min_hex": f"0x{min(values):06X}",
                    "target_max_hex": f"0x{max(values):06X}",
                    "monotonic_ratio": round(monotonic_pairs / pair_count, 6),
                    "strictly_increasing_ratio": round(strict_pairs / pair_count, 6),
                    "unique_target_ratio": round(len(set(values)) / len(values), 6),
                    "target_token_pair_score": round(token_pair_score(target_samples), 6),
                    "first_values": " ".join(f"0x{value:06X}" for value in values[:12]),
                    "status": "confirmed" if known_table else "candidate",
                    "confidence": "high" if known_table else ("medium" if monotonic_pairs / pair_count >= 0.9 else "low"),
                    "caveat": (
                        "consumer proven at 0x28228; individual index meanings remain unknown"
                        if known_table
                        else "may be a numeric/offset table; no consumer cross-reference proven"
                    ),
                }
            )
        if index == start:
            index += 2
    return candidates


def find_known_text_records(data: bytes) -> tuple[list[int], list[dict[str, Any]], int]:
    table_end = KNOWN_TEXT_POINTER_TABLE + KNOWN_TEXT_POINTER_COUNT * 4
    pointers = [be32(data, KNOWN_TEXT_POINTER_TABLE + index * 4) for index in range(KNOWN_TEXT_POINTER_COUNT)]
    if not all(pointer_valid(value, len(data)) for value in pointers):
        raise ValueError("known text table failed in-ROM/even pointer validation")
    if any(left >= right for left, right in zip(pointers, pointers[1:])):
        raise ValueError("known text table is not strictly increasing")
    if pointers[0] != table_end:
        raise ValueError("known text table does not point to the byte after itself")

    records: list[dict[str, Any]] = []
    for index, start in enumerate(pointers):
        if index + 1 < len(pointers):
            end = pointers[index + 1]
            boundary_source = "next_pointer"
        else:
            end, terminator = find_token_record_end(data, start)
            if terminator is None:
                raise ValueError("final known text record has no recognized terminator")
            boundary_source = f"terminator_{terminator}"
        raw = data[start:end]
        records.append(text_record_row(index, start, end, raw, [], boundary_source))
    data_end = records[-1]["end"]
    return pointers, records, data_end


def find_token_record_end(data: bytes, start: int, limit: int = 0x800) -> tuple[int, str | None]:
    max_end = min(len(data), start + limit)
    for offset in range(start, max_end - 1, 2):
        token = be16(data, offset)
        if token in (0xFFFF, 0x8000):
            return offset + 2, f"0x{token:04X}"
    return max_end, None


def text_record_row(
    index: int | None,
    start: int,
    end: int,
    raw: bytes,
    refs: Sequence[int],
    boundary_source: str,
) -> dict[str, Any]:
    tokens = [be16(raw, offset) for offset in range(0, len(raw) & ~1, 2)]
    return {
        "index": "" if index is None else index,
        "start": start,
        "end": end,
        "start_hex": f"0x{start:06X}",
        "end_hex": f"0x{end:06X}",
        "length": end - start,
        "word_count": len(tokens),
        "terminator": f"0x{tokens[-1]:04X}" if tokens and tokens[-1] in (0xFFFF, 0x8000) else "",
        "boundary_source": boundary_source,
        "token_pair_score": round(token_pair_score(raw), 6),
        "reference_offsets": " ".join(f"0x{ref:06X}" for ref in refs),
        "tokens_hex": " ".join(f"{token:04X}" for token in tokens),
        "status": "confirmed_structure",
        "caveat": "token structure and character assignment are separate fields",
    }


def find_immediate_text_pointer_refs(data: bytes) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    # 68000: MOVE.L #<source>, $00FF700E.L
    suffix = bytes.fromhex("00ff700e")
    refs_by_target: dict[int, list[int]] = collections.defaultdict(list)
    for offset in range(0, len(data) - 10, 2):
        if data[offset : offset + 2] != b"\x23\xFC" or data[offset + 6 : offset + 10] != suffix:
            continue
        target = be32(data, offset + 2)
        if pointer_valid(target, len(data)):
            refs_by_target[target].append(offset)

    ref_rows: list[dict[str, Any]] = []
    record_rows: list[dict[str, Any]] = []
    for target in sorted(refs_by_target):
        refs = refs_by_target[target]
        end, terminator = find_token_record_end(data, target)
        raw = data[target:end]
        score = token_pair_score(raw)
        for ref in refs:
            ref_rows.append(
                {
                    "instruction_offset": ref,
                    "instruction_offset_hex": f"0x{ref:06X}",
                    "target": target,
                    "target_hex": f"0x{target:06X}",
                    "instruction_hex": data[ref : ref + 10].hex(),
                    "recognized_terminator": terminator or "",
                    "token_pair_score": round(score, 6),
                    "status": "confirmed_reference",
                    "evidence": "exact MOVE.L #ROM_address,$00FF700E instruction encoding",
                }
            )
        record_rows.append(
            text_record_row(
                None,
                target,
                end,
                raw,
                refs,
                f"terminator_{terminator}" if terminator else "scan_limit_no_terminator",
            )
        )
        if terminator is None or score < 0.85:
            record_rows[-1]["status"] = "candidate"
    return ref_rows, record_rows


def merge_ranges(ranges: Iterable[tuple[int, int]], maximum_gap: int = 0) -> list[tuple[int, int]]:
    ordered = sorted(ranges)
    if not ordered:
        return []
    merged = [ordered[0]]
    for start, end in ordered[1:]:
        old_start, old_end = merged[-1]
        if start <= old_end + maximum_gap:
            merged[-1] = (old_start, max(old_end, end))
        else:
            merged.append((start, end))
    return merged


def find_fixed_block_duplicates(data: bytes, block_size: int = 0x100) -> list[dict[str, Any]]:
    groups: dict[bytes, list[int]] = collections.defaultdict(list)
    for start in range(0, len(data) - block_size + 1, block_size):
        chunk = data[start : start + block_size]
        if len(set(chunk)) <= 1:
            continue
        groups[hashlib.sha1(chunk).digest()].append(start)
    rows: list[dict[str, Any]] = []
    for digest, offsets in groups.items():
        if len(offsets) < 2:
            continue
        rows.append(
            {
                "block_size": block_size,
                "repeat_count": len(offsets),
                "sha1": digest.hex(),
                "offsets": " ".join(f"0x{offset:06X}" for offset in offsets[:64]),
                "truncated_offset_list": len(offsets) > 64,
                "status": "confirmed_duplicate_bytes",
                "caveat": "equal fixed-size blocks provide candidate asset matches",
            }
        )
    rows.sort(key=lambda row: (-row["repeat_count"], row["offsets"]))
    return rows


def raw4bpp_metrics(data: bytes, start: int, size: int = RAW_TILE_BANK_SIZE) -> dict[str, Any]:
    raw = data[start : min(start + size, len(data))]
    raw = raw[: len(raw) - (len(raw) % 32)]
    pixels: list[int] = []
    horizontal_equal = horizontal_total = 0
    vertical_equal = vertical_total = 0
    blank_tiles = 0
    solid_tiles = 0
    tile_hashes: list[bytes] = []
    per_tile_colors: list[int] = []
    for tile_start in range(0, len(raw), 32):
        tile = raw[tile_start : tile_start + 32]
        tile_hashes.append(hashlib.sha1(tile).digest())
        tile_pixels: list[int] = []
        for byte in tile:
            tile_pixels.extend((byte >> 4, byte & 0x0F))
        pixels.extend(tile_pixels)
        colors = set(tile_pixels)
        per_tile_colors.append(len(colors))
        if len(colors) == 1 and 0 in colors:
            blank_tiles += 1
        if len(colors) == 1:
            solid_tiles += 1
        for y in range(8):
            row = tile_pixels[y * 8 : (y + 1) * 8]
            horizontal_equal += sum(left == right for left, right in zip(row, row[1:]))
            horizontal_total += 7
        for y in range(7):
            for x in range(8):
                vertical_equal += tile_pixels[y * 8 + x] == tile_pixels[(y + 1) * 8 + x]
                vertical_total += 1
    tile_count = len(raw) // 32
    pixel_counts = collections.Counter(pixels)
    duplicate_tiles = tile_count - len(set(tile_hashes))
    horizontal_ratio = ratio(horizontal_equal, horizontal_total)
    vertical_ratio = ratio(vertical_equal, vertical_total)
    blank_ratio = ratio(blank_tiles, tile_count)
    duplicate_ratio = ratio(duplicate_tiles, tile_count)
    mean_colors = statistics.mean(per_tile_colors) if per_tile_colors else 0.0

    # Rank raw tile candidates for visual inspection.
    entropy = shannon_entropy(raw)
    eligible = entropy >= 1.5 and max(blank_ratio, ratio(solid_tiles, tile_count)) < 0.90
    score = (
        horizontal_ratio * 2.0
        + vertical_ratio * 2.0
        + min(duplicate_ratio, 0.5)
        + (0.4 if 1.2 <= mean_colors <= 8.0 else 0.0)
        + (0.3 if 0.01 <= blank_ratio <= 0.75 else 0.0)
    ) if eligible else 0.0
    return {
        "start": start,
        "end": start + len(raw),
        "start_hex": f"0x{start:06X}",
        "end_hex": f"0x{start + len(raw):06X}",
        "size": len(raw),
        "tile_count": tile_count,
        "byte_entropy": round(entropy, 6),
        "horizontal_neighbor_equal_ratio": round(horizontal_ratio, 6),
        "vertical_neighbor_equal_ratio": round(vertical_ratio, 6),
        "zero_pixel_ratio": round(ratio(pixel_counts.get(0, 0), len(pixels)), 6),
        "blank_tile_ratio": round(blank_ratio, 6),
        "solid_tile_ratio": round(ratio(solid_tiles, tile_count), 6),
        "duplicate_tile_ratio": round(duplicate_ratio, 6),
        "mean_colors_per_tile": round(mean_colors, 6),
        "heuristic_score": round(score, 6),
        "eligible_candidate": eligible,
        "status": "candidate",
        "confidence": "low",
        "caveat": "viewing bytes as packed 4-bpp can make non-graphics data look patterned",
    }


def tilemap_metrics(data: bytes, start: int, size: int = 0x1000) -> dict[str, Any]:
    raw = data[start : min(start + size, len(data))]
    raw = raw[: len(raw) & ~1]
    words = [be16(raw, offset) for offset in range(0, len(raw), 2)]
    attrs = [value >> 11 for value in words]
    indices = [value & 0x7FF for value in words]
    attr_counts = collections.Counter(attrs)
    top4_attr_ratio = ratio(sum(count for _, count in attr_counts.most_common(4)), len(attrs))
    local_index_ratio = ratio(
        sum(abs(a - b) <= 64 for a, b in zip(indices, indices[1:])),
        max(1, len(indices) - 1),
    )
    zero_ratio = ratio(sum(value == 0 for value in words), len(words))
    score = top4_attr_ratio + local_index_ratio + (0.2 if zero_ratio < 0.75 else 0.0)
    return {
        "start": start,
        "end": start + len(raw),
        "start_hex": f"0x{start:06X}",
        "end_hex": f"0x{start + len(raw):06X}",
        "word_count": len(words),
        "attribute_values_used": len(attr_counts),
        "top4_attribute_ratio": round(top4_attr_ratio, 6),
        "neighbor_index_delta_le_64_ratio": round(local_index_ratio, 6),
        "zero_word_ratio": round(zero_ratio, 6),
        "heuristic_score": round(score, 6),
        "top_attributes": " ".join(f"{value}:{count}" for value, count in attr_counts.most_common(8)),
        "status": "candidate",
        "confidence": "low",
        "caveat": "16-bit numeric tables and code immediates can mimic VDP tilemap words",
    }


def render_raw4bpp_png(data: bytes, start: int, output: Path, tile_columns: int = 16) -> bool:
    try:
        from PIL import Image
    except ImportError:
        return False
    raw = data[start : min(start + RAW_TILE_BANK_SIZE, len(data))]
    tile_count = len(raw) // 32
    rows = math.ceil(tile_count / tile_columns)
    scale = 2
    image = Image.new("L", (tile_columns * 8, rows * 8), 0)
    palette = [round(index * 255 / 15) for index in range(16)]
    for tile_index in range(tile_count):
        tile = raw[tile_index * 32 : tile_index * 32 + 32]
        base_x = (tile_index % tile_columns) * 8
        base_y = (tile_index // tile_columns) * 8
        pixel_index = 0
        for byte in tile:
            for nibble in (byte >> 4, byte & 0x0F):
                x = base_x + (pixel_index % 8)
                y = base_y + (pixel_index // 8)
                image.putpixel((x, y), palette[nibble])
                pixel_index += 1
    image = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
    image.save(output)
    return True


def render_raw4bpp_overview(data: bytes, output: Path) -> bool:
    """Render non-overlapping 0x2000 banks as labelled thumbnails.

    This is a navigation aid, not evidence that every bank contains graphics.
    """
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return False
    bank_starts = list(range(0x40000, len(data) - RAW_TILE_BANK_SIZE + 1, RAW_TILE_BANK_SIZE))
    columns = 8
    cell_width = 136
    cell_height = 152
    rows = math.ceil(len(bank_starts) / columns)
    overview = Image.new("RGB", (columns * cell_width, rows * cell_height), "#202020")
    draw = ImageDraw.Draw(overview)
    for bank_index, start in enumerate(bank_starts):
        temporary = output.with_name(f".{output.stem}_{start:06x}.png")
        render_raw4bpp_png(data, start, temporary)
        tile_view = Image.open(temporary).convert("RGB").resize((128, 128), Image.Resampling.NEAREST)
        temporary.unlink()
        x = (bank_index % columns) * cell_width + 4
        y = (bank_index // columns) * cell_height + 18
        overview.paste(tile_view, (x, y))
        draw.text((x, y - 15), f"0x{start:06X}", fill="white")
    overview.save(output)
    return True


def validate_and_extract_z80(data: bytes, generated: Path) -> tuple[list[Segment], dict[str, Any]]:
    """Validate the exact 68000 copy loops and extract their ROM sources."""
    signatures = {
        "primary_copy": (0x6966, bytes.fromhex("41fa 006a 4e71 43f9 00a0 0000 303c 0fff 12d8 51c8 fffc")),
        "secondary_copy": (0x697C, bytes.fromhex("41fa 101e 4e71 303c 0dff 12d8 51c8 fffc")),
        "overlay_copy": (0x698C, bytes.fromhex("41fa 001c 43f9 00a0 1c00 700c 12d8 51c8 fffc")),
    }
    validation = {
        name: data[offset : offset + len(expected)] == expected
        for name, (offset, expected) in signatures.items()
    }
    if not all(validation.values()):
        return [], {"validated": False, "signature_matches": validation}

    sources = [
        ("z80_source_primary", 0x69D2, 0x1000, 0x0000),
        ("z80_source_secondary", 0x799C, 0x0E00, 0x1000),
        ("z80_source_overlay_1c00", 0x69AA, 0x000D, 0x1C00),
    ]
    runtime = bytearray(0x1E00)
    segments: list[Segment] = []
    extracted: list[dict[str, Any]] = []
    for name, start, length, destination in sources:
        blob = data[start : start + length]
        (generated / f"{name}.bin").write_bytes(blob)
        runtime[destination : destination + length] = blob
        segments.append(
            Segment(
                start=start,
                end=start + length,
                label=name,
                status="confirmed",
                confidence="high",
                category="z80_address_space_payload",
                evidence=[
                    f"validated 68000 copy loop transfers {length:#x} bytes",
                    f"source ROM {start:#x} -> Z80 address {destination:#x}",
                ],
                caveats=["payload can contain Z80 code, music data, and tables; boundaries inside it are unresolved"],
            )
        )
        extracted.append(
            {
                "name": name,
                "rom_start": start,
                "length": length,
                "z80_destination": destination,
                "sha256": sha256(blob),
            }
        )
    runtime_path = generated / "z80_runtime_expected.bin"
    runtime_path.write_bytes(runtime)
    return segments, {
        "validated": True,
        "signature_matches": validation,
        "sources": extracted,
        "runtime_size": len(runtime),
        "runtime_sha256": sha256(runtime),
        "runtime_output": str(runtime_path),
    }


def standard_signature_hits(data: bytes) -> list[dict[str, Any]]:
    signatures = {
        "gzip": b"\x1F\x8B\x08",
        "zip_local_file": b"PK\x03\x04",
        "zlib_78_01": b"\x78\x01",
        "zlib_78_9c": b"\x78\x9C",
        "zlib_78_da": b"\x78\xDA",
        "png": b"\x89PNG\r\n\x1A\n",
        "iff_form": b"FORM",
        "midi": b"MThd",
        "riff": b"RIFF",
    }
    rows: list[dict[str, Any]] = []
    for name, signature in signatures.items():
        offset = 0
        while True:
            offset = data.find(signature, offset)
            if offset < 0:
                break
            decompression_validated = False
            decompressed_length = ""
            if name.startswith("zlib_"):
                try:
                    unpacked = zlib.decompress(data[offset:])
                    decompression_validated = True
                    decompressed_length = len(unpacked)
                except zlib.error:
                    pass
            rows.append(
                {
                    "signature": name,
                    "offset": offset,
                    "offset_hex": f"0x{offset:06X}",
                    "bytes_hex": signature.hex(),
                    "decompression_validated": decompression_validated,
                    "decompressed_length": decompressed_length,
                    "status": "byte_signature_only",
                    "caveat": "short magic can occur by chance; decompression was not validated",
                }
            )
            offset += 1
    return rows


def hardware_reference_hits(data: bytes) -> list[dict[str, Any]]:
    targets = {
        "z80_ram_base": 0x00A00000,
        "z80_bus_request": 0x00A11100,
        "z80_reset": 0x00A11200,
        "vdp_data": 0x00C00000,
        "vdp_control": 0x00C00004,
    }
    rows: list[dict[str, Any]] = []
    for name, value in targets.items():
        needle = value.to_bytes(4, "big")
        offset = 0
        while True:
            offset = data.find(needle, offset)
            if offset < 0:
                break
            rows.append(
                {
                    "target_name": name,
                    "target": f"0x{value:08X}",
                    "literal_offset": offset,
                    "literal_offset_hex": f"0x{offset:06X}",
                    "context_start_hex": f"0x{max(0, offset - 6):06X}",
                    "context_hex": data[max(0, offset - 6) : min(len(data), offset + 10)].hex(),
                    "status": "confirmed_literal_only",
                    "caveat": "literal matches are candidates for control-flow analysis",
                }
            )
            offset += 1
    return rows


def write_csv(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def run_unidasm(unidasm: Path, binary: Path, output: Path) -> dict[str, Any]:
    if not unidasm.is_file():
        return {"ran": False, "reason": f"unidasm not found: {unidasm}"}
    result = subprocess.run(
        [str(unidasm), binary.name, "-arch", "z80", "-basepc", "0"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(binary.parent),
    )
    output.write_text(result.stdout + ("\nSTDERR:\n" + result.stderr if result.stderr else ""), encoding="utf-8")
    return {"ran": True, "returncode": result.returncode, "output": str(output)}


def make_markdown(
    rom_path: Path,
    segments: Sequence[Segment],
    page_rows: Sequence[dict[str, Any]],
    pointer_runs: Sequence[dict[str, Any]],
    fill_runs: Sequence[dict[str, Any]],
    text_records: Sequence[dict[str, Any]],
    direct_text_records: Sequence[dict[str, Any]],
    tile_rows: Sequence[dict[str, Any]],
    tilemap_rows: Sequence[dict[str, Any]],
    signatures: Sequence[dict[str, Any]],
    z80_info: dict[str, Any],
    previews: Sequence[str],
) -> str:
    lines = [
        "# ROM 资源与区段",
        "",
        f"- 输入：{rom_path.name}（{rom_path.stat().st_size} 字节）。",
        f"- 区段：{len(segments)}；统计窗口：{len(page_rows)}。",
        f"- 指针序列：{len(pointer_runs)}；填充段：{len(fill_runs)}。",
        f"- 文本表记录：{len(text_records)}；直接引用目标：{len(direct_text_records)}。",
        f"- 瓦片窗口：{len(tile_rows)}；地图窗口：{len(tilemap_rows)}；预览：{len(previews)}。",
        f"- 格式签名：{len(signatures)}。",
        f"- Z80 装载：{'格式匹配' if z80_info.get('validated') else '待核对'}。",
        "",
        "区段表保存地址、类型和依据。候选项可通过消费者引用、格式检查或预览核对。",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, required=True, help="linear G-5510 BIN")
    parser.add_argument("--output", type=Path, required=True, help="fresh output directory")
    parser.add_argument(
        "--unidasm",
        type=Path,
        help="optional path to MAME's separately installed unidasm utility",
    )
    parser.add_argument("--preview-count", type=int, default=8)
    args = parser.parse_args()

    rom_path = args.rom.resolve()
    output = args.output.resolve()
    generated = output / "generated"

    data = rom_path.read_bytes()
    try:
        require_g5510_rom(data)
    except ValueError as error:
        parser.error(str(error))

    if args.output.is_symlink():
        parser.error("--output must name a fresh directory")
    output.mkdir(parents=True)
    generated.mkdir()

    segments: list[Segment] = [
        Segment(
            0x000000,
            0x000100,
            "m68k_vector_table",
            "confirmed",
            "high",
            "platform_structure",
            ["Mega Drive 68000 reset/vector area at ROM start", "initial SP and reset PC are in valid address ranges"],
            ["individual vector handlers are outside this asset-only phase"],
        ),
        Segment(
            0x000100,
            0x000200,
            "mega_drive_rom_header",
            "confirmed",
            "high",
            "platform_metadata",
            ["contains SEGA MEGA DRIVE signature, product GM G-5510, checksum and ROM/RAM ranges"],
            ["Japanese title bytes require external character decoding"],
        ),
    ]

    pages: list[dict[str, Any]] = []
    for start in range(0, len(data), WINDOW_SIZE):
        row = window_metrics(data, start, WINDOW_SIZE)
        row["statistical_class"], row["status"] = classify_statistical_page(row)
        pages.append(row)
    entropy_rows = [
        window_metrics(data, start, ENTROPY_SUBWINDOW)
        for start in range(0, len(data), ENTROPY_SUBWINDOW)
    ]
    fills = find_fill_runs(data)
    ascii_rows = find_ascii_strings(data)
    pointer_runs = find_u32_pointer_runs(data)
    duplicates = find_fixed_block_duplicates(data)
    signatures = standard_signature_hits(data)
    hardware_refs = hardware_reference_hits(data)

    pointers, known_text_records, known_text_end = find_known_text_records(data)
    table_end = KNOWN_TEXT_POINTER_TABLE + KNOWN_TEXT_POINTER_COUNT * 4
    segments.extend(
        [
            Segment(
                KNOWN_TEXT_POINTER_TABLE,
                table_end,
                "known_text_pointer_table_52_be32",
                "confirmed",
                "high",
                "text_pointer_table",
                [
                    "0x28228 LEA loads table base; index is shifted by two",
                    "selected BE32 pointer is written to RAM 0xFF700E",
                    "52/52 pointers are in-ROM, even, strictly increasing; first equals table end",
                ],
                ["table index meanings and glyph mapping remain unknown"],
            ),
            Segment(
                pointers[0],
                known_text_end,
                "known_text_token_records_52",
                "confirmed",
                "high",
                "custom_text_tokens",
                ["bounded by the 52 validated pointers", "records have regular BE16 token structure and recognized terminators"],
                ["entries retain cartridge token values"],
            ),
        ]
    )

    direct_text_refs, direct_text_records = find_immediate_text_pointer_refs(data)
    direct_text_ranges = merge_ranges(
        (row["start"], row["end"])
        for row in direct_text_records
        if row["status"] == "confirmed_structure"
    )
    for index, (start, end) in enumerate(direct_text_ranges):
        segments.append(
            Segment(
                start,
                end,
                f"direct_text_token_cluster_{index:02d}",
                "confirmed",
                "high",
                "custom_text_tokens",
                ["one or more exact MOVE.L #ROM_address,$00FF700E references", "recognized BE16 token terminator"],
                ["ranges represent contiguous cartridge tokens"],
            )
        )

    z80_segments, z80_info = validate_and_extract_z80(data, generated)
    segments.extend(z80_segments)

    raw_tile_rows = [
        raw4bpp_metrics(data, start)
        for start in range(0x40000, len(data) - RAW_TILE_BANK_SIZE + 1, 0x1000)
    ]
    raw_tile_rows.sort(key=lambda row: (-row["heuristic_score"], row["start"]))
    tilemap_rows = [
        tilemap_metrics(data, start)
        for start in range(0x40000, len(data) - 0x1000 + 1, 0x1000)
    ]
    tilemap_rows.sort(key=lambda row: (-row["heuristic_score"], row["start"]))

    # Add only the best non-overlapping statistical hypotheses to the semantic
    # map.  All detailed rankings remain in CSV.
    selected_tile_starts: list[int] = []
    for row in raw_tile_rows:
        if len(selected_tile_starts) >= max(0, args.preview_count):
            break
        if not row["eligible_candidate"]:
            continue
        if any(abs(row["start"] - prior) < RAW_TILE_BANK_SIZE for prior in selected_tile_starts):
            continue
        selected_tile_starts.append(row["start"])
        segments.append(
            Segment(
                row["start"],
                row["end"],
                f"raw4bpp_hypothesis_{row['start']:06X}",
                "candidate",
                "low",
                "graphics_candidate",
                [
                    f"packed-nibble adjacency score {row['heuristic_score']:.3f}",
                    f"mean colors/tile {row['mean_colors_per_tile']:.3f}",
                ],
                ["requires VDP/VRAM trace or recognizable rendered content"],
            )
        )

    preview_names: list[str] = []
    for start in selected_tile_starts:
        name = f"candidate_raw4bpp_0x{start:06X}.png"
        if render_raw4bpp_png(data, start, generated / name):
            preview_names.append(name)
    overview_name = "raw4bpp_bank_overview_0x040000_0x100000.png"
    if render_raw4bpp_overview(data, generated / overview_name):
        preview_names.append(overview_name)

    write_csv(output / "coverage_pages.csv", pages)
    write_csv(output / "entropy_windows.csv", entropy_rows)
    write_csv(output / "fill_runs.csv", fills)
    write_csv(output / "ascii_strings.csv", ascii_rows)
    write_csv(output / "pointer_table_candidates.csv", pointer_runs)
    write_csv(output / "duplicate_blocks.csv", duplicates)
    write_csv(output / "standard_signature_hits.csv", signatures)
    write_csv(output / "hardware_literal_refs.csv", hardware_refs)
    write_csv(output / "raw4bpp_candidates.csv", raw_tile_rows)
    write_csv(output / "tilemap_candidates.csv", tilemap_rows)
    write_csv(generated / "known_text_records.csv", known_text_records)
    write_csv(generated / "direct_text_pointer_refs.csv", direct_text_refs)
    write_csv(generated / "direct_text_records.csv", direct_text_records)

    segment_rows = [segment.serializable() for segment in segments]
    write_csv(output / "rom_segments.csv", segment_rows)

    if not z80_info.get("validated"):
        unidasm_info = {"ran": False, "reason": "Z80 source validation failed"}
    elif args.unidasm is None:
        unidasm_info = {"ran": False, "reason": "No unidasm was supplied"}
    else:
        unidasm_info = run_unidasm(
            args.unidasm.resolve(),
            generated / "z80_runtime_expected.bin",
            generated / "z80_runtime_expected.disasm.txt",
        )

    manifest = {
        "schema_version": 1,
        "scope": "ROM resource analysis",
        "input": {
            "path": rom_path.name,
            "size": len(data),
        },
        "parameters": {
            "page_size": WINDOW_SIZE,
            "entropy_window": ENTROPY_SUBWINDOW,
            "raw_tile_bank_size": RAW_TILE_BANK_SIZE,
            "known_text_pointer_table": KNOWN_TEXT_POINTER_TABLE,
            "known_text_pointer_count": KNOWN_TEXT_POINTER_COUNT,
        },
        "coverage": {
            "rom_bytes": len(data),
            "statistical_pages": len(pages),
            "statistical_bytes": sum(row["size"] for row in pages),
            "all_bytes_have_statistical_class": sum(row["size"] for row in pages) == len(data),
        },
        "segments": segment_rows,
        "known_text": {
            "pointers": pointers,
            "table_records": len(known_text_records),
            "direct_reference_instructions": len(direct_text_refs),
            "direct_unique_targets": len(direct_text_records),
        },
        "z80": z80_info,
        "unidasm": unidasm_info,
        "counts": {
            "pointer_candidates": len(pointer_runs),
            "fill_runs": len(fills),
            "duplicate_block_groups": len(duplicates),
            "ascii_strings": len(ascii_rows),
            "standard_signature_hits": len(signatures),
            "hardware_literal_refs": len(hardware_refs),
            "raw4bpp_windows": len(raw_tile_rows),
            "tilemap_windows": len(tilemap_rows),
            "rendered_previews": len(preview_names),
        },
        "status_definitions": {
            "confirmed": "validated directly from exact bytes, platform structure, or an instruction-level consumer/copy relationship",
            "candidate": "statistical/structural hypothesis requiring a consumer xref, runtime trace, decompression proof, or visual match",
            "unknown": "covered statistically but not assigned a semantic resource type",
        },
    }
    (output / "rom_segments.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    report = make_markdown(
        rom_path,
        segments,
        pages,
        pointer_runs,
        fills,
        known_text_records,
        direct_text_records,
        raw_tile_rows,
        tilemap_rows,
        signatures,
        z80_info,
        preview_names,
    )
    (output / "ROM_ASSET_MAP.md").write_text(report, encoding="utf-8")

    print(f"ROM: {rom_path}")
    print(f"Output: {output}")
    print(f"Segments: {len(segments)} ({sum(s.status == 'confirmed' for s in segments)} confirmed)")
    print(f"Known text records: {len(known_text_records)}")
    print(f"Direct text targets: {len(direct_text_records)}")
    print(f"Pointer candidates: {len(pointer_runs)}")
    print(f"Z80 transfer validated: {z80_info.get('validated', False)}")
    print(f"PNG previews: {len(preview_names)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
