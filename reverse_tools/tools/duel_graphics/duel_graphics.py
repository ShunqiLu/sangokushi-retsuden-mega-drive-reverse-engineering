#!/usr/bin/env python3
"""Read, edit and preview G-5510 duel graphics in their fixed cartridge slots."""

from __future__ import annotations

import argparse
import binascii
import csv
import hashlib
import json
import math
import os
import struct
import sys
import tempfile
import zlib
from dataclasses import asdict, dataclass
from io import StringIO
from pathlib import Path
from typing import Any, Iterable, Sequence


if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.rom_layout import require_g5510_rom

MAP_DECODED_SIZE = 0x0A00
MAP_LANE_SIZE = MAP_DECODED_SIZE // 2
MAP_CELLS_WIDE = 40
MAP_CELLS_HIGH = 32


class DuelGraphicsError(ValueError):
    """Raised when an identity, boundary, codec, or output invariant fails."""


@dataclass(frozen=True)
class Asset:
    name: str
    filename: str
    start: int
    end: int
    kind: str
    evidence: str
    semantic_evidence: str
    consumer: str
    target: str
    decoded_filename: str | None = None

    @property
    def length(self) -> int:
        return self.end - self.start


ASSETS: tuple[Asset, ...] = (
    Asset(
        "duel_raw_tiles",
        "duel_raw_tiles.bin",
        0x06C3B4,
        0x0783B4,
        "raw_md_4bpp_tiles_1536",
        "direct VRAM transfer",
        "probable_semantics",
        "026EA0 source, 026EB0 direct longword VDP loop",
        "VRAM 0000-BFFF (0xC000 bytes)",
    ),
    Asset(
        "duel_aux_raw_tiles",
        "duel_aux_raw_tiles.bin",
        0x0783B4,
        0x078474,
        "raw_direct_vdp_block",
        "direct VRAM transfer",
        "candidate",
        "026F04 source, 026F0E direct longword VDP loop",
        "VRAM D000-D0BF (0xC0 bytes)",
    ),
    Asset(
        "duel_primary_map_a",
        "duel_primary_map_a.rle.bin",
        0x078474,
        0x078656,
        "lane_interleaved_rle_be16_tilemap_40x32",
        "confirmed_static fixed stream and decoder",
        "probable_semantics",
        "026F76 default source, 026F98 call to 028012",
        "RAM FF6000-FF69FF then VRAM E000-E9FF",
        "duel_primary_map_a.decoded.bin",
    ),
    Asset(
        "duel_primary_map_b",
        "duel_primary_map_b.rle.bin",
        0x078656,
        0x07883E,
        "lane_interleaved_rle_be16_tilemap_40x32",
        "confirmed_static fixed stream and decoder",
        "probable_semantics",
        "026F88 alternate source, 026F98 call to 028012",
        "RAM FF6000-FF69FF then VRAM E000-E9FF",
        "duel_primary_map_b.decoded.bin",
    ),
    Asset(
        "duel_common_map",
        "duel_common_map.rle.bin",
        0x07883E,
        0x0789D6,
        "lane_interleaved_rle_be16_tilemap_40x32",
        "confirmed_static fixed stream and decoder",
        "probable_semantics",
        "026FB6 source, 026FC6 call to 028012",
        "RAM FF6000-FF69FF then VRAM F000-F9FF",
        "duel_common_map.decoded.bin",
    ),
    Asset(
        "duel_palette_staging_candidate",
        "duel_palette_staging_candidate.bin",
        0x028080,
        0x028100,
        "raw_64_be16_candidate_cram_words",
        "direct ROM-to-RAM transfer",
        "candidate",
        "026F5C source, 026F6A longword RAM loop",
        "RAM FFFB00-FFFB7F; candidate palette",
    ),
)

ASSET_BY_NAME = {asset.name: asset for asset in ASSETS}

ANALYSIS_FILENAMES = (
    "duel_graphics.json",
    "assets.csv",
    "anchors.csv",
    "relationships.csv",
)
ASSET_PREVIEW_FILENAMES = (
    "duel_raw_tiles_candidate_palette.png",
    "duel_primary_map_a_candidate_palette.png",
    "duel_primary_map_a_320x224_candidate_palette.png",
    "duel_primary_map_b_candidate_palette.png",
    "duel_primary_map_b_320x224_candidate_palette.png",
    "duel_common_map_candidate_palette.png",
    "duel_common_map_320x224_candidate_palette.png",
)


@dataclass(frozen=True)
class Anchor:
    name: str
    start: int
    end: int
    evidence: str
    role: str


ANCHORS: tuple[Anchor, ...] = (
    Anchor(
        "DuelPresentationSetupPrefix",
        0x026DB4,
        0x027060,
        "confirmed_static",
        "Duel presentation setup and transfer sequence.",
    ),
    Anchor(
        "RawTileDirectLoader",
        0x026E96,
        0x026EB6,
        "confirmed_static",
        "026EA0 loads 06C3B4 and 026EB0 writes 0x3000 longwords to VRAM 0000.",
    ),
    Anchor(
        "AuxiliaryDirectLoader",
        0x026EFA,
        0x026F12,
        "confirmed_static",
        "026F04 loads 0783B4 and 026F0E writes 0x30 longwords to VRAM D000.",
    ),
    Anchor(
        "PaletteStagingCopy",
        0x026F5C,
        0x026F70,
        "confirmed_static; semantic candidate",
        "Copies 0x20 longwords from 028080 to FFFB00; CRAM ownership remains unclosed.",
    ),
    Anchor(
        "PrimaryMapSelectDecodeUpload",
        0x026F76,
        0x026FB6,
        "confirmed_static",
        "026F76/026F88 select a stream, 026F98 calls 028012, then 0x500 words go to VRAM E000.",
    ),
    Anchor(
        "CommonMapDecodeUpload",
        0x026FB6,
        0x026FE2,
        "confirmed_static",
        "026FB6 selects 07883E, 026FC6 calls 028012, then 0x500 words go to VRAM F000.",
    ),
    Anchor(
        "LaneInterleavedRLE",
        0x028012,
        0x028080,
        "confirmed_static exact mechanics",
        "Decodes 0x500 bytes into each alternating destination-byte lane.",
    ),
    Anchor(
        "PaletteStagingCandidateData",
        0x028080,
        0x028100,
        "confirmed_static data boundary; semantic candidate",
        "Exact 0x80-byte source copied to FFFB00; treated only as a preview palette candidate.",
    ),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_rom(data: bytes) -> None:
    try:
        require_g5510_rom(data)
    except ValueError as error:
        raise DuelGraphicsError(str(error)) from error
    for instruction, source in (
        (0x026EA0, 0x06C3B4),
        (0x026F04, 0x0783B4),
        (0x026F76, 0x078474),
        (0x026FB6, 0x07883E),
    ):
        if data[instruction : instruction + 6] != struct.pack(">HI", 0x41F9, source):
            raise DuelGraphicsError(f"unexpected graphics loader at {instruction:#08x}")
    for asset in ASSETS:
        if asset.decoded_filename:
            decoded, _ = decode_lane_rle(data[asset.start : asset.end])
            validate_tilemap(decoded, name=asset.name)


def _decode_lane(data: bytes, cursor: int, output_size: int) -> tuple[bytes, int]:
    output = bytearray()

    def take() -> int:
        nonlocal cursor
        if cursor >= len(data):
            raise DuelGraphicsError("truncated lane-RLE stream")
        value = data[cursor]
        cursor += 1
        return value

    def ensure_room(count: int) -> None:
        if count <= 0 or len(output) + count > output_size:
            raise DuelGraphicsError(
                f"lane-RLE command overruns output: {len(output)} + {count} > {output_size}"
            )

    while len(output) < output_size:
        control = take()
        if control < 0x80:
            count = control + 1
            ensure_room(count)
            if cursor + count > len(data):
                raise DuelGraphicsError("truncated lane-RLE literal")
            output.extend(data[cursor : cursor + count])
            cursor += count
        elif control < 0xC0:
            count = (control & 0x3F) + 1
            ensure_room(count)
            output.extend(bytes((take(),)) * count)
        elif control < 0xE0:
            repeats = (control & 0x1F) + 1
            count = repeats * 2
            ensure_room(count)
            first, second = take(), take()
            output.extend(bytes((first, second)) * repeats)
        else:
            count = (control & 0x1F) + 1
            ensure_room(count)
            first = take()
            output.extend((first + index) & 0xFF for index in range(count))
    return bytes(output), cursor


def decode_lane_rle(data: bytes, *, require_exhaustion: bool = True) -> tuple[bytes, tuple[int, int]]:
    """Decode both 0x500-byte lanes used by the routine at 0x028012."""

    first, cursor = _decode_lane(data, 0, MAP_LANE_SIZE)
    first_length = cursor
    second, cursor = _decode_lane(data, cursor, MAP_LANE_SIZE)
    if require_exhaustion and cursor != len(data):
        raise DuelGraphicsError(
            f"lane-RLE output completed at 0x{cursor:X}, fixed slot is 0x{len(data):X}"
        )
    decoded = bytearray(MAP_DECODED_SIZE)
    decoded[0::2] = first
    decoded[1::2] = second
    return bytes(decoded), (first_length, cursor - first_length)


@dataclass(frozen=True)
class _EncodingOption:
    end: int
    encoded: bytes

    @property
    def cost(self) -> int:
        return len(self.encoded)


def _encoding_options(data: bytes, start: int) -> list[_EncodingOption]:
    remaining = len(data) - start
    options: list[_EncodingOption] = []

    for length in range(1, min(128, remaining) + 1):
        options.append(
            _EncodingOption(
                start + length,
                bytes((length - 1,)) + data[start : start + length],
            )
        )

    repeat_limit = min(64, remaining)
    repeat_length = 0
    while repeat_length < repeat_limit and data[start + repeat_length] == data[start]:
        repeat_length += 1
        length = repeat_length
        options.append(
            _EncodingOption(start + length, bytes((0x80 | (length - 1), data[start])))
        )

    if remaining >= 2:
        pair_limit = min(32, remaining // 2)
        first, second = data[start], data[start + 1]
        for repeats in range(1, pair_limit + 1):
            position = start + (repeats - 1) * 2
            if data[position] != first or data[position + 1] != second:
                break
            options.append(
                _EncodingOption(
                    start + repeats * 2,
                    bytes((0xC0 | (repeats - 1), first, second)),
                )
            )

    increment_limit = min(32, remaining)
    increment_length = 0
    while (
        increment_length < increment_limit
        and data[start + increment_length] == ((data[start] + increment_length) & 0xFF)
    ):
        increment_length += 1
        length = increment_length
        options.append(
            _EncodingOption(start + length, bytes((0xE0 | (length - 1), data[start])))
        )

    # Sort by descending coverage, ascending cost and ascending encoded bytes.
    options.sort(key=lambda item: (-(item.end - start), item.cost, item.encoded))
    return options


def _lane_reachability(data: bytes, maximum_cost: int) -> tuple[list[int], list[list[_EncodingOption]]]:
    options = [_encoding_options(data, start) for start in range(len(data))]
    reachable = [0] * (len(data) + 1)
    reachable[0] = 1
    cost_mask = (1 << (maximum_cost + 1)) - 1
    for start in range(len(data)):
        costs = reachable[start]
        if not costs:
            continue
        for option in options[start]:
            reachable[option.end] |= (costs << option.cost) & cost_mask
    return reachable, options


def _encode_lane_with_cost(
    data: bytes,
    target_cost: int,
    reachable: list[int],
    options: list[list[_EncodingOption]],
) -> bytes:
    if target_cost < 0 or not ((reachable[len(data)] >> target_cost) & 1):
        raise DuelGraphicsError(f"lane cannot be encoded in exactly {target_cost} bytes")
    position = len(data)
    cost = target_cost
    reversed_chunks: list[bytes] = []
    while position:
        chosen_start: int | None = None
        chosen: _EncodingOption | None = None
        for start in range(max(0, position - 128), position):
            for option in options[start]:
                if option.end != position or option.cost > cost:
                    continue
                if (reachable[start] >> (cost - option.cost)) & 1:
                    chosen_start, chosen = start, option
                    break
            if chosen is not None:
                break
        if chosen is None or chosen_start is None:
            raise DuelGraphicsError("internal exact-length lane-RLE backtracking failure")
        reversed_chunks.append(chosen.encoded)
        position = chosen_start
        cost -= chosen.cost
    if cost != 0:
        raise DuelGraphicsError("internal exact-length lane-RLE cost mismatch")
    return b"".join(reversed(reversed_chunks))


def encode_lane_rle_exact(
    decoded: bytes,
    encoded_size: int,
    *,
    preferred_first_lane_size: int | None = None,
) -> bytes:
    """Encode a decoded map into exactly its existing ROM slot size.

    The dynamic programme searches all legal 0x028012 commands.  Failure is
    explicit: callers must not relocate the next asset or silently truncate.
    """

    if len(decoded) != MAP_DECODED_SIZE:
        raise DuelGraphicsError(
            f"decoded tilemap must be 0x{MAP_DECODED_SIZE:X} bytes, got 0x{len(decoded):X}"
        )
    first, second = decoded[0::2], decoded[1::2]
    reachable_first, options_first = _lane_reachability(first, encoded_size)
    reachable_second, options_second = _lane_reachability(second, encoded_size)
    candidates = [
        cost
        for cost in range(encoded_size + 1)
        if ((reachable_first[len(first)] >> cost) & 1)
        and ((reachable_second[len(second)] >> (encoded_size - cost)) & 1)
    ]
    if not candidates:
        raise DuelGraphicsError(
            f"decoded edit cannot fit the fixed 0x{encoded_size:X}-byte encoded slot"
        )
    preferred = preferred_first_lane_size
    if preferred is None:
        preferred = encoded_size // 2
    first_cost = min(candidates, key=lambda value: (abs(value - preferred), value))
    encoded = _encode_lane_with_cost(
        first, first_cost, reachable_first, options_first
    ) + _encode_lane_with_cost(
        second, encoded_size - first_cost, reachable_second, options_second
    )
    if len(encoded) != encoded_size:
        raise DuelGraphicsError("internal exact-length lane-RLE size mismatch")
    roundtrip, _ = decode_lane_rle(encoded)
    if roundtrip != decoded:
        raise DuelGraphicsError("internal exact-length lane-RLE roundtrip mismatch")
    return encoded


def tilemap_stats(decoded: bytes) -> dict[str, Any]:
    if len(decoded) != MAP_DECODED_SIZE:
        raise DuelGraphicsError("tilemap statistics require exactly 0xA00 bytes")
    words = [
        int.from_bytes(decoded[offset : offset + 2], "big")
        for offset in range(0, len(decoded), 2)
    ]
    tile_ids = [word & 0x07FF for word in words]
    return {
        "word_count": len(words),
        "logical_dimensions": [MAP_CELLS_WIDE, MAP_CELLS_HIGH],
        "unique_tile_ids": len(set(tile_ids)),
        "tile_id_min": min(tile_ids),
        "tile_id_max": max(tile_ids),
        "palette_indices": sorted({(word >> 13) & 3 for word in words}),
        "hflip_words": sum(bool(word & 0x0800) for word in words),
        "vflip_words": sum(bool(word & 0x1000) for word in words),
        "priority_words": sum(bool(word & 0x8000) for word in words),
    }


def validate_tilemap(decoded: bytes, *, name: str) -> dict[str, Any]:
    stats = tilemap_stats(decoded)
    if stats["word_count"] != MAP_CELLS_WIDE * MAP_CELLS_HIGH:
        raise DuelGraphicsError(f"{name}: tilemap is not 40x32 words")
    if int(stats["tile_id_max"]) >= 0x600:
        raise DuelGraphicsError(
            f"{name}: tile index 0x{int(stats['tile_id_max']):X} exceeds loaded 0x000-0x5FF bank"
        )
    return stats


def _png_chunk(kind: bytes, payload: bytes) -> bytes:
    body = kind + payload
    return (
        struct.pack(">I", len(payload))
        + body
        + struct.pack(">I", binascii.crc32(body) & 0xFFFFFFFF)
    )


def write_rgb_png(path: Path, width: int, height: int, pixels: bytes) -> None:
    if len(pixels) != width * height * 3:
        raise DuelGraphicsError("RGB PNG payload length mismatch")
    rows = b"".join(
        b"\x00" + pixels[y * width * 3 : (y + 1) * width * 3]
        for y in range(height)
    )
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", header)
        + _png_chunk(b"IDAT", zlib.compress(rows, level=9))
        + _png_chunk(b"IEND", b"")
    )


def cram_colours(candidate: bytes) -> list[tuple[int, int, int]]:
    if len(candidate) != 0x80:
        raise DuelGraphicsError("candidate CRAM table must contain 0x80 bytes")
    levels = (0, 52, 87, 116, 144, 172, 206, 255)
    colours: list[tuple[int, int, int]] = []
    for offset in range(0, len(candidate), 2):
        word = int.from_bytes(candidate[offset : offset + 2], "big")
        colours.append(
            (
                levels[(word >> 1) & 7],
                levels[(word >> 5) & 7],
                levels[(word >> 9) & 7],
            )
        )
    return colours


def _tile_pixels(raw_tiles: bytes, tile_index: int) -> list[int]:
    start = tile_index * 32
    tile = raw_tiles[start : start + 32]
    if len(tile) != 32:
        raise DuelGraphicsError(f"tile index 0x{tile_index:X} is outside the raw bank")
    pixels: list[int] = []
    for value in tile:
        pixels.extend((value >> 4, value & 0x0F))
    return pixels


def render_tile_sheet(raw_tiles: bytes, candidate_palette: bytes, path: Path) -> None:
    columns = 32
    count = len(raw_tiles) // 32
    rows = math.ceil(count / columns)
    width, height = columns * 8, rows * 8
    colours = cram_colours(candidate_palette)
    canvas = bytearray(width * height * 3)
    # The sheet uses palette line 2 only as a diagnostic convention.
    palette = 2
    for tile_index in range(count):
        x0, y0 = (tile_index % columns) * 8, (tile_index // columns) * 8
        for position, colour_index in enumerate(_tile_pixels(raw_tiles, tile_index)):
            x, y = x0 + position % 8, y0 + position // 8
            target = (y * width + x) * 3
            canvas[target : target + 3] = bytes(colours[palette * 16 + colour_index])
    write_rgb_png(path, width, height, bytes(canvas))


def render_tilemap(
    raw_tiles: bytes,
    candidate_palette: bytes,
    tilemap: bytes,
    path: Path,
    *,
    crop_height: int | None = None,
) -> None:
    validate_tilemap(tilemap, name=path.name)
    width, height = MAP_CELLS_WIDE * 8, MAP_CELLS_HIGH * 8
    colours = cram_colours(candidate_palette)
    canvas = bytearray(width * height * 3)
    for cell in range(MAP_CELLS_WIDE * MAP_CELLS_HIGH):
        word = int.from_bytes(tilemap[cell * 2 : cell * 2 + 2], "big")
        tile_index = word & 0x07FF
        hflip, vflip = bool(word & 0x0800), bool(word & 0x1000)
        palette = (word >> 13) & 3
        pixels = _tile_pixels(raw_tiles, tile_index)
        x0, y0 = (cell % MAP_CELLS_WIDE) * 8, (cell // MAP_CELLS_WIDE) * 8
        for source_y in range(8):
            for source_x in range(8):
                colour_index = pixels[source_y * 8 + source_x]
                draw_x = x0 + (7 - source_x if hflip else source_x)
                draw_y = y0 + (7 - source_y if vflip else source_y)
                target = (draw_y * width + draw_x) * 3
                canvas[target : target + 3] = bytes(
                    colours[palette * 16 + colour_index]
                )
    if crop_height is not None:
        crop_height = min(height, crop_height)
        cropped = b"".join(
            canvas[y * width * 3 : (y + 1) * width * 3]
            for y in range(crop_height)
        )
        write_rgb_png(path, width, crop_height, cropped)
    else:
        write_rgb_png(path, width, height, bytes(canvas))


def _asset_descriptor(asset: Asset, encoded: bytes) -> dict[str, Any]:
    if len(encoded) != asset.length:
        raise DuelGraphicsError(f"{asset.name}: expected {asset.length} encoded bytes")
    decoded = encoded
    lane_lengths: list[int] | None = None
    stats: dict[str, Any] | None = None
    if asset.decoded_filename:
        decoded, lanes = decode_lane_rle(encoded)
        lane_lengths = list(lanes)
        stats = validate_tilemap(decoded, name=asset.name)
    phase_by_name = {
        "duel_raw_tiles": "raw_tiles",
        "duel_aux_raw_tiles": "aux_raw",
        "duel_primary_map_a": "primary_map_variant_a",
        "duel_primary_map_b": "primary_map_variant_b",
        "duel_common_map": "common_map",
        "duel_palette_staging_candidate": "palette_staging_candidate",
    }
    target_endpoints_by_name: dict[str, list[dict[str, Any]]] = {
        "duel_raw_tiles": [
            {
                "address_space": "vram",
                "start": 0x0000,
                "end": 0xC000,
                "layout": "raw_md_4bpp_tiles_1536",
                "phase": "raw_tiles",
            }
        ],
        "duel_aux_raw_tiles": [
            {
                "address_space": "vram",
                "start": 0xD000,
                "end": 0xD0C0,
                "layout": "raw_direct_vdp_block",
                "phase": "aux_raw",
            }
        ],
        "duel_primary_map_a": [
            {
                "address_space": "m68k_ram",
                "start": 0xFF6000,
                "end": 0xFF6A00,
                "layout": "40x32_be16_tilemap_scratch",
                "phase": "primary_map_variant_a",
            },
            {
                "address_space": "vram",
                "start": 0xE000,
                "end": 0xEA00,
                "layout": "40x32_be16_tilemap_words",
                "phase": "primary_map_upload",
            },
        ],
        "duel_primary_map_b": [
            {
                "address_space": "m68k_ram",
                "start": 0xFF6000,
                "end": 0xFF6A00,
                "layout": "40x32_be16_tilemap_scratch",
                "phase": "primary_map_variant_b",
            },
            {
                "address_space": "vram",
                "start": 0xE000,
                "end": 0xEA00,
                "layout": "40x32_be16_tilemap_words",
                "phase": "primary_map_upload",
            },
        ],
        "duel_common_map": [
            {
                "address_space": "m68k_ram",
                "start": 0xFF6000,
                "end": 0xFF6A00,
                "layout": "40x32_be16_tilemap_scratch",
                "phase": "common_map_decode",
            },
            {
                "address_space": "vram",
                "start": 0xF000,
                "end": 0xFA00,
                "layout": "40x32_be16_tilemap_words",
                "phase": "common_map_upload",
            },
        ],
        "duel_palette_staging_candidate": [
            {
                "address_space": "m68k_ram",
                "start": 0xFFFB00,
                "end": 0xFFFB80,
                "layout": "64_be16_words_candidate_only",
                "phase": "palette_staging_candidate",
            }
        ],
    }
    return {
        "name": asset.name,
        "primary_role": (
            "m68k_data"
            if asset.name == "duel_palette_staging_candidate"
            else "graphics_data"
        ),
        "confidence": "confirmed_static",
        "phase": phase_by_name[asset.name],
        "file": asset.filename,
        "rom_start": asset.start,
        "rom_end": asset.end,
        "length": asset.length,
        "sha256": sha256(encoded),
        "kind": asset.kind,
        "evidence": asset.evidence,
        "semantic_evidence": asset.semantic_evidence,
        "consumer": asset.consumer,
        "target": asset.target,
        "source_endpoint": {
            "address_space": "m68k_rom",
            "start": asset.start,
            "end": asset.end,
            "layout": asset.kind,
            "phase": phase_by_name[asset.name],
        },
        "target_endpoints": target_endpoints_by_name[asset.name],
        "decoded_file": asset.decoded_filename,
        "decoded_length": len(decoded),
        "decoded_sha256": sha256(decoded),
        "encoded_lane_lengths": lane_lengths,
        "tilemap_stats": stats,
    }


def manifest_for_rom(rom: bytes) -> dict[str, Any]:
    validate_rom(rom)
    descriptors = [
        _asset_descriptor(asset, rom[asset.start : asset.end]) for asset in ASSETS
    ]
    return {
        "schema_version": 1,
        "source_rom": {
            "path": "cartridge.bin",
            "size": len(rom),
            "sha256": sha256(rom),
        },
        "codec": {
            "routine": "028012-028080",
            "decoded_bytes": MAP_DECODED_SIZE,
            "lane_bytes": MAP_LANE_SIZE,
            "layout": "big-endian words assembled from two sequential alternating-byte lanes",
            "decoded_edit_policy": (
                "decoded edits use exact-length encoding in the original slot"
            ),
        },
        "assets": descriptors,
        "preview_boundary": {
            "palette": (
                "028080-028100 is used only as a candidate palette for offline previews; "
                "the direct transfer stages the bytes in RAM FFFB00"
            ),
            "layout": (
                "compressed words are rendered as a logical 40x32 stream; runtime scroll, "
                "plane ordering and sprites belong to later display stages"
            ),
            "pixel_exact": False,
        },
    }


def _write_text_lf(path: Path, text: str, *, encoding: str = "utf-8") -> None:
    if "\r" in text:
        raise DuelGraphicsError(f"refusing non-LF text output: {path}")
    path.write_bytes(text.encode(encoding))


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _resolved(path: Path) -> Path:
    return path.expanduser().resolve()


def _paths_overlap(left: Path, right: Path) -> bool:
    """Return whether either resolved path contains the other."""

    return left == right or left in right.parents or right in left.parents


def _require_directory_parent(path: Path, *, label: str) -> None:
    parent = path.parent
    while True:
        if parent.exists() or parent.is_symlink():
            if not parent.is_dir():
                raise DuelGraphicsError(
                    f"{label} has a non-directory ancestor: {parent}"
                )
            return
        if parent == parent.parent:
            raise DuelGraphicsError(f"{label} has no existing directory ancestor")
        parent = parent.parent


def _require_new_directory(output: Path, *, protected: Iterable[Path] = ()) -> Path:
    resolved = _resolved(output)
    for item in protected:
        if resolved == _resolved(item):
            raise DuelGraphicsError("output directory collides with a protected input")
    if output.is_symlink():
        raise DuelGraphicsError(f"refusing symlink output directory: {output}")
    if resolved.exists():
        raise DuelGraphicsError(f"refusing to overwrite existing output directory: {resolved}")
    if resolved.suffix.lower() in {".bin", ".smd", ".sta"}:
        raise DuelGraphicsError("output directory may not use a protected binary extension")
    _require_directory_parent(resolved, label="output directory")
    return resolved


def _require_new_output_file(
    output: Path, *, rom_path: Path, assets_dir: Path | None = None
) -> Path:
    resolved = _resolved(output)
    protected = {_resolved(rom_path)}
    if assets_dir is not None:
        root = _resolved(assets_dir)
        for asset in ASSETS:
            protected.add(_resolved(root / asset.filename))
            if asset.decoded_filename:
                protected.add(_resolved(root / asset.decoded_filename))
        protected.add(_resolved(root / "manifest.json"))
    if resolved in protected:
        raise DuelGraphicsError("output path collides with a protected binary input")
    if output.is_symlink():
        raise DuelGraphicsError(f"refusing symlink output file: {output}")
    if resolved.exists():
        raise DuelGraphicsError(f"refusing to overwrite existing output file: {resolved}")
    _require_directory_parent(resolved, label="output file")
    return resolved


def _analysis_generated_files(destination: Path) -> dict[Path, str]:
    files = {
        destination / name: name
        for name in ANALYSIS_FILENAMES
    }
    assets_root = destination / "assets"
    files[assets_root / "manifest.json"] = "assets/manifest.json"
    for asset in ASSETS:
        files[assets_root / asset.filename] = f"assets/{asset.filename}"
        if asset.decoded_filename:
            files[assets_root / asset.decoded_filename] = (
                f"assets/{asset.decoded_filename}"
            )
    for name in ASSET_PREVIEW_FILENAMES:
        files[assets_root / name] = f"assets/{name}"
    return files


def _preflight_analysis_paths(
    rom_file: Path, output: Path, report: Path
) -> tuple[Path, Path]:
    destination = _require_new_directory(output, protected=(rom_file,))
    report_path = _require_new_output_file(report, rom_path=rom_file)
    generated_files = _analysis_generated_files(destination)

    if report_path == destination:
        raise DuelGraphicsError("report path collides with the analysis output directory")
    if report_path == destination / "assets":
        raise DuelGraphicsError("report path collides with the generated assets directory")
    if report_path in generated_files:
        raise DuelGraphicsError(
            f"report path collides with generated file {generated_files[report_path]}"
        )
    for target, relative_name in generated_files.items():
        if target in report_path.parents:
            raise DuelGraphicsError(
                f"report path is nested below generated file {relative_name}"
            )
    if _paths_overlap(report_path, destination):
        raise DuelGraphicsError("report path overlaps the analysis output tree")
    if _paths_overlap(destination, rom_file):
        raise DuelGraphicsError("analysis output tree collides with the canonical ROM")
    if _paths_overlap(report_path, rom_file):
        raise DuelGraphicsError("report path tree collides with the canonical ROM")
    return destination, report_path


def extract_assets(rom_path: Path, output: Path) -> dict[str, Any]:
    rom_file = _resolved(rom_path)
    rom = rom_file.read_bytes()
    manifest = manifest_for_rom(rom)
    destination = _require_new_directory(output, protected=(rom_file,))
    destination.mkdir(parents=True)
    for asset in ASSETS:
        encoded = rom[asset.start : asset.end]
        (destination / asset.filename).write_bytes(encoded)
        if asset.decoded_filename:
            decoded, _ = decode_lane_rle(encoded)
            (destination / asset.decoded_filename).write_bytes(decoded)

    raw_tiles = rom[0x06C3B4:0x0783B4]
    palette = rom[0x028080:0x028100]
    decoded_maps = {
        asset.name: decode_lane_rle(rom[asset.start : asset.end])[0]
        for asset in ASSETS
        if asset.decoded_filename
    }
    render_tile_sheet(
        raw_tiles,
        palette,
        destination / "duel_raw_tiles_candidate_palette.png",
    )
    for name in ("duel_primary_map_a", "duel_primary_map_b", "duel_common_map"):
        render_tilemap(
            raw_tiles,
            palette,
            decoded_maps[name],
            destination / f"{name}_candidate_palette.png",
        )
        render_tilemap(
            raw_tiles,
            palette,
            decoded_maps[name],
            destination / f"{name}_320x224_candidate_palette.png",
            crop_height=224,
        )
    _write_text_lf(
        destination / "manifest.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
    return manifest


def _validate_manifest(assets_dir: Path, rom: bytes) -> dict[str, Any]:
    path = assets_dir / "manifest.json"
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise DuelGraphicsError(f"cannot load asset manifest: {error}") from error
    expected = manifest_for_rom(rom)
    if manifest != expected:
        raise DuelGraphicsError("asset manifest was changed or is not canonical")
    return manifest


def import_assets(
    rom_path: Path,
    assets_dir: Path,
    output_path: Path,
) -> bytes:
    rom_file = _resolved(rom_path)
    base = rom_file.read_bytes()
    validate_rom(base)
    root = _resolved(assets_dir)
    manifest = _validate_manifest(root, base)
    destination = _require_new_output_file(
        output_path, rom_path=rom_file, assets_dir=root
    )
    rebuilt = bytearray(base)
    descriptors = manifest["assets"]
    for index, asset in enumerate(ASSETS):
        descriptor = descriptors[index]
        encoded_path = root / asset.filename
        encoded = encoded_path.read_bytes()
        if len(encoded) != asset.length:
            raise DuelGraphicsError(
                f"{asset.name}: encoded slot length changed from 0x{asset.length:X}"
            )
        if asset.decoded_filename:
            decoded_path = root / asset.decoded_filename
            decoded_edit = decoded_path.read_bytes()
            if len(decoded_edit) != MAP_DECODED_SIZE:
                raise DuelGraphicsError(
                    f"{asset.name}: decoded edit must remain exactly 0x{MAP_DECODED_SIZE:X} bytes"
                )
            base_encoded = base[asset.start : asset.end]
            base_decoded, _ = decode_lane_rle(base_encoded)
            encoded_changed = encoded != base_encoded
            decoded_changed = decoded_edit != base_decoded
            if encoded_changed and decoded_changed:
                raise DuelGraphicsError(
                    f"{asset.name}: encoded and decoded forms both changed; choose one edit path"
                )
            if decoded_changed:
                validate_tilemap(decoded_edit, name=asset.name)
                lanes = descriptor.get("encoded_lane_lengths")
                if not isinstance(lanes, list) or len(lanes) != 2:
                    raise DuelGraphicsError(f"{asset.name}: invalid canonical lane lengths")
                encoded = encode_lane_rle_exact(
                    decoded_edit,
                    asset.length,
                    preferred_first_lane_size=int(lanes[0]),
                )
            decoded, _ = decode_lane_rle(encoded)
            validate_tilemap(decoded, name=asset.name)
        rebuilt[asset.start : asset.end] = encoded
    _atomic_write(destination, bytes(rebuilt))
    return bytes(rebuilt)


def relationships() -> list[dict[str, Any]]:
    return [
        {
            "id": "duel-graphics:raw-rom-to-vram",
            "primary_role": "asset_transfer",
            "phase": "raw_tiles",
            "confidence": "confirmed_static",
            "semantic_evidence": "probable_semantics",
            "evidence": "confirmed_static; runtime payload trace",
            "source": "ROM 06C3B4-0783B4",
            "consumer": "026EA0/026EB0",
            "target": "VRAM 0000-BFFF",
            "source_endpoint": {"address_space": "m68k_rom", "start": 0x06C3B4, "end": 0x0783B4},
            "consumer_endpoint": {"address_space": "m68k_rom", "anchors": [0x026EA0, 0x026EB0]},
            "intermediate_endpoint": None,
            "target_endpoint": {"address_space": "vram", "start": 0x0000, "end": 0xC000},
            "layout": "raw_md_4bpp_tiles_1536",
            "encoded_length": 0xC000,
            "decoded_length": 0xC000,
            "transform": "0x3000 direct longword writes; no decompression",
            "limitation": "Only tiles 0500-05FF have a statically closed background-map reference.",
        },
        {
            "id": "duel-graphics:aux-rom-to-vram",
            "primary_role": "asset_transfer",
            "phase": "aux_raw",
            "confidence": "confirmed_static",
            "semantic_evidence": "candidate",
            "evidence": "confirmed_static; runtime payload trace",
            "source": "ROM 0783B4-078474",
            "consumer": "026F04/026F0E",
            "target": "VRAM D000-D0BF",
            "source_endpoint": {"address_space": "m68k_rom", "start": 0x0783B4, "end": 0x078474},
            "consumer_endpoint": {"address_space": "m68k_rom", "anchors": [0x026F04, 0x026F0E]},
            "intermediate_endpoint": None,
            "target_endpoint": {"address_space": "vram", "start": 0xD000, "end": 0xD0C0},
            "layout": "raw_direct_vdp_block",
            "encoded_length": 0xC0,
            "decoded_length": 0xC0,
            "transform": "0x30 direct longword writes",
            "limitation": "Visible purpose unknown.",
        },
        {
            "id": "duel-graphics:primary-map-a",
            "primary_role": "asset_transfer",
            "phase": "primary_map_variant_a_unless_ff70f2_eq_3",
            "confidence": "confirmed_static",
            "semantic_evidence": "probable_semantics",
            "evidence": "confirmed_static; selected runtime branch recorded separately",
            "source": "ROM 078474-078656 when FF70F2!=3",
            "consumer": "026F76/026F98 -> 028012",
            "target": "RAM FF6000-FF69FF -> VRAM E000-E9FF",
            "source_endpoint": {"address_space": "m68k_rom", "start": 0x078474, "end": 0x078656},
            "consumer_endpoint": {"address_space": "m68k_rom", "anchors": [0x026F76, 0x026F98, 0x028012]},
            "intermediate_endpoint": {"address_space": "m68k_ram", "start": 0xFF6000, "end": 0xFF6A00},
            "target_endpoint": {"address_space": "vram", "start": 0xE000, "end": 0xEA00},
            "layout": "lane_interleaved_rle_to_40x32_be16",
            "encoded_length": 0x1E2,
            "decoded_length": 0xA00,
            "transform": "two sequential lane-RLE passes assemble 0x500 BE16 words",
            "limitation": "Natural gameplay distribution of the two variants is unknown.",
        },
        {
            "id": "duel-graphics:primary-map-b",
            "primary_role": "asset_transfer",
            "phase": "primary_map_variant_b_only_if_ff70f2_eq_3",
            "confidence": "confirmed_static",
            "semantic_evidence": "probable_semantics",
            "evidence": "confirmed_static",
            "source": "ROM 078656-07883E when FF70F2==3",
            "consumer": "026F88/026F98 -> 028012",
            "target": "RAM FF6000-FF69FF -> VRAM E000-E9FF",
            "source_endpoint": {"address_space": "m68k_rom", "start": 0x078656, "end": 0x07883E},
            "consumer_endpoint": {"address_space": "m68k_rom", "anchors": [0x026F88, 0x026F98, 0x028012]},
            "intermediate_endpoint": {"address_space": "m68k_ram", "start": 0xFF6000, "end": 0xFF6A00},
            "target_endpoint": {"address_space": "vram", "start": 0xE000, "end": 0xEA00},
            "layout": "lane_interleaved_rle_to_40x32_be16",
            "encoded_length": 0x1E8,
            "decoded_length": 0xA00,
            "transform": "two sequential lane-RLE passes assemble 0x500 BE16 words",
            "limitation": "Alternative map selected by the branch at 026F82.",
        },
        {
            "id": "duel-graphics:common-map",
            "primary_role": "asset_transfer",
            "phase": "common_map",
            "confidence": "confirmed_static",
            "semantic_evidence": "probable_semantics",
            "evidence": "confirmed_static; runtime payload trace",
            "source": "ROM 07883E-0789D6",
            "consumer": "026FB6/026FC6 -> 028012",
            "target": "RAM FF6000-FF69FF -> VRAM F000-F9FF",
            "source_endpoint": {"address_space": "m68k_rom", "start": 0x07883E, "end": 0x0789D6},
            "consumer_endpoint": {"address_space": "m68k_rom", "anchors": [0x026FB6, 0x026FC6, 0x028012]},
            "intermediate_endpoint": {"address_space": "m68k_ram", "start": 0xFF6000, "end": 0xFF6A00},
            "target_endpoint": {"address_space": "vram", "start": 0xF000, "end": 0xFA00},
            "layout": "lane_interleaved_rle_to_40x32_be16",
            "encoded_length": 0x198,
            "decoded_length": 0xA00,
            "transform": "two sequential lane-RLE passes assemble 0x500 BE16 words",
            "limitation": "Preview scope: static map geometry and candidate palette.",
        },
        {
            "id": "duel-graphics:palette-staging-candidate",
            "primary_role": "asset_transfer",
            "phase": "palette_staging_candidate",
            "confidence": "confirmed_static",
            "semantic_evidence": "candidate",
            "evidence": "confirmed_static ROM-to-RAM; semantic candidate",
            "source": "ROM 028080-028100",
            "consumer": "026F5C/026F6A",
            "target": "RAM FFFB00-FFFB7F",
            "source_endpoint": {"address_space": "m68k_rom", "start": 0x028080, "end": 0x028100},
            "consumer_endpoint": {"address_space": "m68k_rom", "anchors": [0x026F5C, 0x026F6A]},
            "intermediate_endpoint": None,
            "target_endpoint": {"address_space": "m68k_ram", "start": 0xFFFB00, "end": 0xFFFB80},
            "layout": "64_be16_words_candidate_only",
            "encoded_length": 0x80,
            "decoded_length": 0x80,
            "transform": "0x20 direct longword copies",
            "limitation": "No exact later CRAM transfer correlation is claimed.",
        },
    ]


def analysis_payload(rom: bytes) -> dict[str, Any]:
    manifest = manifest_for_rom(rom)
    anchor_semantics = {
        "DuelPresentationSetupPrefix": "confirmed_static",
        "RawTileDirectLoader": "probable_semantics",
        "AuxiliaryDirectLoader": "candidate",
        "PaletteStagingCopy": "candidate",
        "PrimaryMapSelectDecodeUpload": "probable_semantics",
        "CommonMapDecodeUpload": "probable_semantics",
        "LaneInterleavedRLE": "confirmed_static",
        "PaletteStagingCandidateData": "candidate",
    }
    return {
        "schema_version": 1,
        "status": "fixed_graphics_layout",
        "identity_gate": manifest["source_rom"],
        "evidence_legend": {
            "confirmed_runtime": "Observed execution of the stated instruction.",
            "runtime_payload_trace": "Exact program-space VDP/RAM write bytes validated by the dedicated trace analyzer.",
            "confirmed_static": "Exact canonical opcodes, source range, count, target, or codec behavior.",
            "probable_semantics": "Role inferred from the data structure and its consumer.",
            "strong_static_visual_corroboration": "Geometry supported by an offline preview.",
            "candidate": "Proposed role for further analysis.",
        },
        "assets": manifest["assets"],
        "anchors": [
            {
                **asdict(anchor),
                "sha256": sha256(rom[anchor.start : anchor.end]),
                "primary_role": (
                    "m68k_data"
                    if anchor.name == "PaletteStagingCandidateData"
                    else "m68k_code"
                ),
                "confidence": "confirmed_static",
                "semantic_evidence": anchor_semantics[anchor.name],
                "length": anchor.end - anchor.start,
            }
            for anchor in ANCHORS
        ],
        "relationships": relationships(),
        "background_subset": {
            "rom_start": 0x0763B4,
            "rom_end": 0x0783B4,
            "length": 0x2000,
            "tile_indices": [0x500, 0x5FF],
            "evidence": "strong_static_visual_corroboration",
            "basis": (
                "All three decoded maps reference only tiles 0500-05FF, whose raw bytes occupy "
                "the final 0x2000 bytes of the 0xC000 bank."
            ),
        },
        "unknowns": [
            "Precise semantics and animation partition of raw tiles 0000-04FF",
            "Visible purpose of the 0xC0 VRAM D000 block",
            "Exact CRAM ownership of 028080-028100",
            "Runtime plane order, scroll, sprite table, and other dynamic layers",
            "Natural gameplay rule selecting primary map A versus B",
        ],
        "future_candidate_not_implemented": {
            "pointer_table": "003A3E-003A5A",
            "sources": "0D474A-0D4ACA",
            "shape": "seven 128-byte 32x32 1bpp sources expanded to seven 0x200-byte 4bpp blocks",
            "consumers": "003A00; converter 003A5A-003B00; uploader 003B02-003B32",
            "semantic_status": "candidate; not implemented in this package",
        },
    }


def _csv_text(fieldnames: Sequence[str], rows: Iterable[dict[str, Any]]) -> str:
    buffer = StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({name: row.get(name, "") for name in fieldnames})
    return buffer.getvalue()


def report_text(payload: dict[str, Any]) -> str:
    lines = [
        "# Duel graphics",
        "",
        "Fixed cartridge slots store VRAM transfers and lane-RLE tilemaps.",
        "",
        "| Asset | ROM span | Format | Destination |",
        "|---|---|---|---|",
    ]
    for asset in payload["assets"]:
        lines.append(
            f"| {asset['name']} | "
            f"`{asset['rom_start']:06X}–{asset['rom_end']:06X}` | "
            f"{asset['kind']} | {asset['target']} |"
        )
    lines.extend((
        "",
        "The asset bundle contains encoded source files, decoded tilemaps and PNG previews.",
        "Import accepts either representation of each tilemap within its fixed slot.",
        "The static preview uses a candidate palette and the tilemap's logical geometry.",
        "",
    ))
    return "\n".join(lines)


def generate_analysis(rom_path: Path, output: Path, report: Path) -> dict[str, Any]:
    rom_file = _resolved(rom_path)
    rom = rom_file.read_bytes()
    validate_rom(rom)
    destination, report_path = _preflight_analysis_paths(rom_file, output, report)
    destination.mkdir(parents=True)
    extract_assets(rom_file, destination / "assets")
    payload = analysis_payload(rom)
    _write_text_lf(
        destination / "duel_graphics.json",
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    )
    asset_rows = []
    for item in payload["assets"]:
        row = dict(item)
        row["rom_start_hex"] = f"{int(item['rom_start']):06X}"
        row["rom_end_hex"] = f"{int(item['rom_end']):06X}"
        row["decoded_sha256"] = item.get("decoded_sha256", "")
        row["encoded_lane_lengths"] = json.dumps(item.get("encoded_lane_lengths"))
        row["tilemap_stats"] = json.dumps(item.get("tilemap_stats"), sort_keys=True)
        row["source_endpoint"] = json.dumps(
            item.get("source_endpoint"), sort_keys=True, separators=(",", ":")
        )
        row["target_endpoints"] = json.dumps(
            item.get("target_endpoints"), sort_keys=True, separators=(",", ":")
        )
        asset_rows.append(row)
    _write_text_lf(
        destination / "assets.csv",
        _csv_text(
            (
                "name",
                "primary_role",
                "phase",
                "confidence",
                "rom_start_hex",
                "rom_end_hex",
                "length",
                "sha256",
                "kind",
                "decoded_length",
                "decoded_sha256",
                "encoded_lane_lengths",
                "consumer",
                "target",
                "evidence",
                "semantic_evidence",
                "source_endpoint",
                "target_endpoints",
                "tilemap_stats",
            ),
            asset_rows,
        ),
    )
    anchor_rows = []
    for item in payload["anchors"]:
        row = dict(item)
        row["start_hex"] = f"{int(item['start']):06X}"
        row["end_hex"] = f"{int(item['end']):06X}"
        anchor_rows.append(row)
    _write_text_lf(
        destination / "anchors.csv",
        _csv_text(
            (
                "name",
                "primary_role",
                "confidence",
                "semantic_evidence",
                "start_hex",
                "end_hex",
                "length",
                "sha256",
                "evidence",
                "role",
            ),
            anchor_rows,
        ),
    )
    relationship_rows = []
    for item in payload["relationships"]:
        row = dict(item)
        for field in (
            "source_endpoint",
            "consumer_endpoint",
            "intermediate_endpoint",
            "target_endpoint",
        ):
            row[field] = json.dumps(item.get(field), sort_keys=True, separators=(",", ":"))
        relationship_rows.append(row)
    _write_text_lf(
        destination / "relationships.csv",
        _csv_text(
            (
                "id",
                "primary_role",
                "phase",
                "confidence",
                "semantic_evidence",
                "source",
                "consumer",
                "target",
                "source_endpoint",
                "consumer_endpoint",
                "intermediate_endpoint",
                "target_endpoint",
                "layout",
                "encoded_length",
                "decoded_length",
                "transform",
                "limitation",
            ),
            relationship_rows,
        ),
    )
    _atomic_write(report_path, report_text(payload).encode("utf-8"))
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    verify = subparsers.add_parser("verify", help="verify canonical identity and every fixed span")
    verify.add_argument("--rom", type=Path, required=True, help="linear G-5510 BIN")
    extract = subparsers.add_parser("extract", help="extract assets and offline previews")
    extract.add_argument("--rom", type=Path, required=True, help="linear G-5510 BIN")
    extract.add_argument("--output", type=Path, required=True)
    importer = subparsers.add_parser("import", help="safely import fixed-slot edits")
    importer.add_argument("--rom", type=Path, required=True, help="linear G-5510 BIN")
    importer.add_argument("--assets", type=Path, required=True)
    importer.add_argument("--output", type=Path, required=True)
    generate = subparsers.add_parser("generate", help="generate JSON/CSV/manifest/previews/report")
    generate.add_argument("--rom", type=Path, required=True, help="linear G-5510 BIN")
    generate.add_argument("--output", type=Path, required=True)
    generate.add_argument("--report", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "verify":
            rom = args.rom.resolve().read_bytes()
            validate_rom(rom)
            for asset in ASSETS:
                if asset.decoded_filename:
                    decode_lane_rle(rom[asset.start : asset.end])
            print(f"duel graphics verify: PASS assets={len(ASSETS)} anchors={len(ANCHORS)}")
        elif args.command == "extract":
            manifest = extract_assets(args.rom, args.output)
            print(f"duel graphics extract: PASS assets={len(manifest['assets'])}")
        elif args.command == "import":
            rebuilt = import_assets(args.rom, args.assets, args.output)
            print(f"duel graphics import: PASS sha256={sha256(rebuilt)}")
        else:
            payload = generate_analysis(args.rom, args.output, args.report)
            print(
                "duel graphics generate: PASS "
                f"assets={len(payload['assets'])} anchors={len(payload['anchors'])}"
            )
    except (DuelGraphicsError, OSError, KeyError, TypeError, ValueError) as error:
        raise SystemExit(f"error: {error}") from error
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
