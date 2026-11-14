#!/usr/bin/env python3
"""Losslessly extract/import the confirmed G-5510 title graphics assets."""

from __future__ import annotations

import argparse
import binascii
import hashlib
import json
import math
import struct
import sys
import zlib
from dataclasses import dataclass
from pathlib import Path


if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.rom_layout import require_g5510_rom


class GraphicsError(ValueError):
    """Raised when a graphics asset violates a confirmed invariant."""


@dataclass(frozen=True)
class Asset:
    name: str
    filename: str
    start: int
    end: int
    kind: str
    evidence: str
    decoded_words: int | None = None
    byte_order: str | None = None
    vdp_target: int | None = None


ASSETS = (
    Asset(
        "title_tiles_rle_0",
        "title_tiles_rle_0.bin",
        0x05D5E4,
        0x05F137,
        "word_rle_little_bytes_to_vram_4bpp",
        "confirmed: 0x003848 call to 0x03AB52 plus exact runtime data-port sequence",
        4096,
        "little",
        0x0000,
    ),
    Asset(
        "title_tiles_rle_1",
        "title_tiles_rle_1.bin",
        0x05F137,
        0x060E6C,
        "word_rle_little_bytes_to_vram_4bpp",
        "confirmed: 0x003858 call to 0x03AB52 plus exact runtime data-port sequence",
        4096,
        "little",
        0x2000,
    ),
    Asset(
        "title_tiles_rle_2",
        "title_tiles_rle_2.bin",
        0x060E6C,
        0x06254F,
        "word_rle_little_bytes_to_vram_4bpp",
        "confirmed: 0x003868 call to 0x03AB52 plus exact runtime data-port sequence",
        4096,
        "little",
        0x4000,
    ),
    Asset(
        "title_tiles_rle_3",
        "title_tiles_rle_3.bin",
        0x06254F,
        0x064340,
        "word_rle_little_bytes_to_vram_4bpp",
        "confirmed: 0x003878 call to 0x03AB52 plus exact runtime data-port sequence",
        4096,
        "little",
        0x8000,
    ),
    Asset(
        "title_tiles_rle_4",
        "title_tiles_rle_4.bin",
        0x064340,
        0x0655F1,
        "word_rle_little_bytes_to_vram_4bpp",
        "confirmed: 0x003888 call to 0x03AB52 plus exact runtime data-port sequence",
        4096,
        "little",
        0xA000,
    ),
    Asset(
        "title_plane_b_left",
        "title_plane_b_left.bin",
        0x0655F1,
        0x065DF1,
        "raw_be16_tilemap_half_32x32",
        "confirmed: 0x0038BE call to 0x03AAB6 and exact runtime data-port sequence",
        1024,
        "big",
        0xE000,
    ),
    Asset(
        "title_plane_b_right_rle",
        "title_plane_b_right_rle.bin",
        0x065DF3,
        0x065FF6,
        "word_rle_big_bytes_tilemap_half_32x32",
        "confirmed: 0x0038DA call to 0x03AACE plus exact runtime data-port sequence",
        1024,
        "big",
        0xE040,
    ),
    Asset(
        "title_palette",
        "title_palette_cram.bin",
        0x03B0BC,
        0x03B13C,
        "raw_cram_64_be16",
        "confirmed: palette table index 0x11, ROM-to-FFFB00 copy and exact CRAM DMA payload",
        64,
        "big",
        0x0000,
    ),
    Asset(
        "title_aux_raw_tiles",
        "title_aux_raw_tiles.bin",
        0x0D374A,
        0x0D474A,
        "raw_vram_4bpp_tiles",
        "confirmed: 0x0038AA source and 0x0038B4 direct VDP loop, exact runtime bytes",
        2048,
        "big",
        0x6E00,
    ),
)

ASSET_BY_NAME = {asset.name: asset for asset in ASSETS}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_rom(data: bytes) -> None:
    try:
        require_g5510_rom(data)
    except ValueError as error:
        raise GraphicsError(str(error)) from error
    for asset in ASSETS:
        decode_asset(asset, data[asset.start : asset.end])


def decode_word_rle(data: bytes, *, byte_order: str) -> tuple[bytes, int]:
    """Decode the marker/count word RLE implemented at 0x03AAEA/0x03AB5E.

    The first byte is an escape marker.  A non-marker begins one literal word;
    a marker followed by zero terminates; otherwise count N emits N+1 copies.
    The title-tile variant stores low byte then high byte, while the tilemap
    variant stores high byte then low byte.
    """
    if byte_order not in {"little", "big"}:
        raise GraphicsError(f"unsupported RLE word byte order: {byte_order}")
    if not data:
        raise GraphicsError("empty RLE stream")
    marker = data[0]
    cursor = 1
    output = bytearray()

    def take() -> int:
        nonlocal cursor
        if cursor >= len(data):
            raise GraphicsError("unterminated RLE stream")
        value = data[cursor]
        cursor += 1
        return value

    def emit(first: int, second: int) -> bytes:
        return bytes((second, first)) if byte_order == "little" else bytes((first, second))

    while True:
        first = take()
        if first != marker:
            output.extend(emit(first, take()))
            continue
        count = take()
        if count == 0:
            break
        word = emit(take(), take())
        output.extend(word * (count + 1))
    return bytes(output), cursor


def decode_asset(asset: Asset, encoded: bytes) -> bytes:
    if asset.kind.startswith("word_rle"):
        assert asset.byte_order is not None
        decoded, consumed = decode_word_rle(encoded, byte_order=asset.byte_order)
        if consumed != len(encoded):
            raise GraphicsError(
                f"{asset.name}: terminator at {consumed:#x}, expected fixed end {len(encoded):#x}"
            )
        expected = int(asset.decoded_words or 0) * 2
        if len(decoded) != expected:
            raise GraphicsError(
                f"{asset.name}: decoded {len(decoded):#x}, expected {expected:#x} bytes"
            )
        return decoded
    if len(encoded) != asset.end - asset.start:
        raise GraphicsError(f"{asset.name}: wrong raw size")
    return encoded


def png_chunk(kind: bytes, payload: bytes) -> bytes:
    body = kind + payload
    return struct.pack(">I", len(payload)) + body + struct.pack(">I", binascii.crc32(body) & 0xFFFFFFFF)


def write_rgb_png(path: Path, width: int, height: int, pixels: bytes) -> None:
    if len(pixels) != width * height * 3:
        raise GraphicsError("RGB PNG payload has the wrong length")
    raw = b"".join(
        b"\x00" + pixels[y * width * 3 : (y + 1) * width * 3] for y in range(height)
    )
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    encoded = (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", ihdr)
        + png_chunk(b"IDAT", zlib.compress(raw, level=9))
        + png_chunk(b"IEND", b"")
    )
    path.write_bytes(encoded)


def cram_colours(cram: bytes) -> list[tuple[int, int, int]]:
    if len(cram) != 0x80:
        raise GraphicsError("CRAM palette must contain 0x80 bytes")
    # MAME's Mega Drive renderer uses the VDP's non-linear 3-bit DAC levels.
    # Keeping these levels also permits pixel-exact comparison with snapshots.
    levels = (0, 52, 87, 116, 144, 172, 206, 255)
    colours: list[tuple[int, int, int]] = []
    for offset in range(0, len(cram), 2):
        word = int.from_bytes(cram[offset : offset + 2], "big")
        red = levels[(word >> 1) & 0x07]
        green = levels[(word >> 5) & 0x07]
        blue = levels[(word >> 9) & 0x07]
        colours.append((red, green, blue))
    return colours


def tile_pixels(vram: bytes, tile_index: int) -> list[int]:
    start = tile_index * 32
    raw = vram[start : start + 32]
    if len(raw) != 32:
        return [0] * 64
    pixels: list[int] = []
    for value in raw:
        pixels.extend((value >> 4, value & 0x0F))
    return pixels


def render_tile_sheet(vram: bytes, cram: bytes, path: Path, *, palette: int = 0) -> None:
    columns = 32
    tile_count = len(vram) // 32
    rows = math.ceil(tile_count / columns)
    width = columns * 8
    height = rows * 8
    colours = cram_colours(cram)
    canvas = bytearray(width * height * 3)
    for tile_index in range(tile_count):
        x0 = (tile_index % columns) * 8
        y0 = (tile_index // columns) * 8
        for pixel, colour_index in enumerate(tile_pixels(vram, tile_index)):
            x = x0 + pixel % 8
            y = y0 + pixel // 8
            colour = colours[palette * 16 + colour_index]
            position = (y * width + x) * 3
            canvas[position : position + 3] = bytes(colour)
    write_rgb_png(path, width, height, bytes(canvas))


def render_palette(cram: bytes, path: Path) -> None:
    colours = cram_colours(cram)
    scale = 12
    width = 16 * scale
    height = 4 * scale
    canvas = bytearray(width * height * 3)
    for index, colour in enumerate(colours):
        x0 = (index % 16) * scale
        y0 = (index // 16) * scale
        for y in range(y0, y0 + scale):
            for x in range(x0, x0 + scale):
                position = (y * width + x) * 3
                canvas[position : position + 3] = bytes(colour)
    write_rgb_png(path, width, height, bytes(canvas))


def render_plane(
    vram: bytes,
    cram: bytes,
    tilemap: bytes,
    path: Path,
    *,
    cells_wide: int = 64,
    cells_high: int = 32,
    view_width: int | None = None,
    view_height: int | None = None,
) -> None:
    if len(tilemap) != cells_wide * cells_high * 2:
        raise GraphicsError("tilemap dimensions do not match its byte length")
    width = cells_wide * 8
    height = cells_high * 8
    colours = cram_colours(cram)
    canvas = bytearray(width * height * 3)
    for cell in range(cells_wide * cells_high):
        word = int.from_bytes(tilemap[cell * 2 : cell * 2 + 2], "big")
        index = word & 0x07FF
        hflip = bool(word & 0x0800)
        vflip = bool(word & 0x1000)
        palette = (word >> 13) & 0x03
        pixels = tile_pixels(vram, index)
        x0 = (cell % cells_wide) * 8
        y0 = (cell // cells_wide) * 8
        for source_y in range(8):
            for source_x in range(8):
                colour_index = pixels[source_y * 8 + source_x]
                draw_x = x0 + (7 - source_x if hflip else source_x)
                draw_y = y0 + (7 - source_y if vflip else source_y)
                colour = colours[palette * 16 + colour_index]
                position = (draw_y * width + draw_x) * 3
                canvas[position : position + 3] = bytes(colour)
    if view_width is not None or view_height is not None:
        cropped_width = min(width, view_width or width)
        cropped_height = min(height, view_height or height)
        cropped = b"".join(
            canvas[y * width * 3 : y * width * 3 + cropped_width * 3]
            for y in range(cropped_height)
        )
        write_rgb_png(path, cropped_width, cropped_height, cropped)
    else:
        write_rgb_png(path, width, height, bytes(canvas))


def build_title_vdp(rom: bytes) -> tuple[bytes, bytes, bytes]:
    vram = bytearray(0x10000)
    decoded: dict[str, bytes] = {}
    for asset in ASSETS:
        encoded = rom[asset.start : asset.end]
        decoded[asset.name] = decode_asset(asset, encoded)
        if "vram_4bpp" in asset.kind:
            assert asset.vdp_target is not None
            data = decoded[asset.name]
            vram[asset.vdp_target : asset.vdp_target + len(data)] = data

    tilemap = bytearray(64 * 32 * 2)
    left = decoded["title_plane_b_left"]
    right = decoded["title_plane_b_right_rle"]
    for row in range(32):
        tilemap[row * 128 : row * 128 + 64] = left[row * 64 : row * 64 + 64]
        tilemap[row * 128 + 64 : row * 128 + 128] = right[row * 64 : row * 64 + 64]
    cram = decoded["title_palette"]
    return bytes(vram), cram, bytes(tilemap)


def extract_assets(rom_path: Path, output: Path) -> dict[str, object]:
    rom = rom_path.resolve().read_bytes()
    validate_rom(rom)
    if output.exists():
        raise GraphicsError(f"refusing to overwrite existing output directory: {output}")
    output.mkdir(parents=True)

    descriptors: list[dict[str, object]] = []
    for asset in ASSETS:
        encoded = rom[asset.start : asset.end]
        decoded = decode_asset(asset, encoded)
        path = output / asset.filename
        path.write_bytes(encoded)
        decoded_file = None
        if asset.kind.startswith("word_rle"):
            decoded_file = asset.filename.replace(".bin", ".decoded.bin")
            (output / decoded_file).write_bytes(decoded)
        descriptors.append(
            {
                "name": asset.name,
                "file": asset.filename,
                "rom_start": asset.start,
                "rom_end": asset.end,
                "length": len(encoded),
                "sha256": sha256(encoded),
                "kind": asset.kind,
                "evidence": asset.evidence,
                "decoded_file": decoded_file,
                "decoded_length": len(decoded),
                "decoded_sha256": sha256(decoded),
                "vdp_target": asset.vdp_target,
            }
        )

    vram, cram, tilemap = build_title_vdp(rom)
    (output / "title_reconstructed_vram.bin").write_bytes(vram)
    (output / "title_reconstructed_cram.bin").write_bytes(cram)
    (output / "title_plane_b_64x32.bin").write_bytes(tilemap)
    render_tile_sheet(vram, cram, output / "title_tiles_palette0.png", palette=0)
    render_palette(cram, output / "title_palette.png")
    render_plane(vram, cram, tilemap, output / "title_plane_b_64x32.png")
    render_plane(
        vram,
        cram,
        tilemap,
        output / "title_opening_320x224.png",
        view_width=320,
        view_height=224,
    )

    manifest: dict[str, object] = {
        "schema_version": 1,
        "source_rom": {
            "path": "cartridge.bin",
            "size": len(rom),
            "sha256": sha256(rom),
        },
        "assets": descriptors,
        "title_vdp_model": {
            "vram_sha256": sha256(vram),
            "cram_sha256": sha256(cram),
            "plane_b_sha256": sha256(tilemap),
            "note": (
                "Static background reconstruction with independent sprite and overlay layers."
            ),
        },
        "excluded_gap": {
            "start": 0x065DF1,
            "end": 0x065DF3,
            "bytes_hex": rom[0x065DF1:0x065DF3].hex().upper(),
            "status": "unknown padding/non-consumed bytes between confirmed streams",
        },
    }
    (output / "manifest.json").write_bytes(
        (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    )
    return manifest


def import_assets(base_rom_path: Path, assets_dir: Path, output_path: Path) -> bytes:
    base = base_rom_path.resolve().read_bytes()
    validate_rom(base)
    if output_path.exists():
        raise GraphicsError(f"refusing to overwrite existing output file: {output_path}")
    manifest = json.loads((assets_dir / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1:
        raise GraphicsError("unsupported graphics manifest schema")
    source = manifest.get("source_rom")
    if not isinstance(source, dict) or source.get("sha256") != sha256(base):
        raise GraphicsError("provide the same base BIN used to extract the graphics bundle")
    described = manifest.get("assets")
    if not isinstance(described, list) or len(described) != len(ASSETS):
        raise GraphicsError("graphics manifest asset list was changed")

    rebuilt = bytearray(base)
    for descriptor, asset in zip(described, ASSETS):
        if not isinstance(descriptor, dict):
            raise GraphicsError("malformed graphics asset descriptor")
        expected = {
            "name": asset.name,
            "file": asset.filename,
            "rom_start": asset.start,
            "rom_end": asset.end,
            "length": asset.end - asset.start,
            "kind": asset.kind,
        }
        for key, value in expected.items():
            if descriptor.get(key) != value:
                raise GraphicsError(f"{asset.name}: manifest {key} was changed")
        data = (assets_dir / asset.filename).read_bytes()
        if len(data) != asset.end - asset.start:
            raise GraphicsError(f"{asset.name}: fixed encoded length changed")
        decode_asset(asset, data)
        rebuilt[asset.start : asset.end] = data

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(rebuilt)
    return bytes(rebuilt)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    extract = subparsers.add_parser("extract")
    extract.add_argument("--rom", type=Path, required=True, help="linear G-5510 BIN")
    extract.add_argument("--output", type=Path, required=True)
    importer = subparsers.add_parser("import")
    importer.add_argument("--rom", type=Path, required=True, help="linear G-5510 BIN")
    importer.add_argument("--assets", type=Path, required=True)
    importer.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "extract":
            manifest = extract_assets(args.rom, args.output.resolve())
            print(f"extracted {len(manifest['assets'])} confirmed graphics assets")
        else:
            rebuilt = import_assets(args.rom, args.assets.resolve(), args.output.resolve())
            print(f"wrote {args.output.resolve()} sha256={sha256(rebuilt)}")
    except (GraphicsError, OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"error: {error}") from error
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
