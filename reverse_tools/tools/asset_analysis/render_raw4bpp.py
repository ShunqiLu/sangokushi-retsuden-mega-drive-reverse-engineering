#!/usr/bin/env python3
"""Preview one 0x2000-byte ROM window as packed Mega Drive 4-bpp tiles."""

from __future__ import annotations

import argparse
from pathlib import Path

from scan_assets import RAW_TILE_BANK_SIZE, render_raw4bpp_png, require_g5510_rom


def decode_tile(tile: bytes) -> list[int]:
    pixels: list[int] = []
    for byte in tile:
        pixels.extend((byte >> 4, byte & 0x0F))
    return pixels


def render_glyph16(data: bytes, offset: int, output: Path, order: str) -> bool:
    try:
        from PIL import Image
    except ImportError:
        return False
    raw = data[offset : offset + RAW_TILE_BANK_SIZE]
    tiles = [decode_tile(raw[start : start + 32]) for start in range(0, len(raw), 32)]
    glyph_count = len(tiles) // 4
    columns = 8
    rows = (glyph_count + columns - 1) // columns
    image = Image.new("L", (columns * 16, rows * 16), 0)
    palette = [round(index * 255 / 15) for index in range(16)]
    positions = [(0, 0), (8, 0), (0, 8), (8, 8)] if order == "row" else [(0, 0), (0, 8), (8, 0), (8, 8)]
    for glyph in range(glyph_count):
        base_x = (glyph % columns) * 16
        base_y = (glyph // columns) * 16
        for part, (part_x, part_y) in enumerate(positions):
            pixels = tiles[glyph * 4 + part]
            for pixel_index, value in enumerate(pixels):
                x = base_x + part_x + pixel_index % 8
                y = base_y + part_y + pixel_index // 8
                image.putpixel((x, y), palette[value])
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.NEAREST)
    image.save(output)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("offset", type=lambda value: int(value, 0))
    parser.add_argument("--rom", type=Path, required=True, help="linear G-5510 BIN")
    parser.add_argument("--output", type=Path, required=True, help="fresh PNG file")
    parser.add_argument("--layout", choices=("tile8", "glyph16"), default="tile8")
    parser.add_argument("--glyph-order", choices=("row", "column"), default="row")
    args = parser.parse_args()

    data = args.rom.resolve().read_bytes()
    try:
        require_g5510_rom(data)
    except ValueError as error:
        parser.error(str(error))
    if args.offset < 0 or args.offset + RAW_TILE_BANK_SIZE > len(data):
        raise SystemExit("offset must leave a full 0x2000-byte window inside the ROM")
    if args.output.exists() or args.output.is_symlink():
        parser.error("--output must name a fresh file")
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    rendered = (
        render_raw4bpp_png(data, args.offset, output)
        if args.layout == "tile8"
        else render_glyph16(data, args.offset, output, args.glyph_order)
    )
    if not rendered:
        raise SystemExit("Pillow is required to write a PNG preview")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
