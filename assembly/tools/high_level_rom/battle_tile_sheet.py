"""Edit an existing battle background tile stream as one indexed PNG."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from PIL import Image

from tools.battle_graphics import battle_graphics as battle

from . import media_sources as media
from .battle_asset_streams import (RESOURCE_ID, SOURCE, WordStream, load_assets, nibbles,
                                   publish_files as _publish, read_json as _read_json, word_replacements)


FORMAT = 'g5510-battle-tile-sheet-v1'
STREAM_IDS = tuple(stream.id for stream in battle.STREAMS if stream.vram is not None)
TILE_EDGE = 8
TILES_PER_ROW = 16
SIDE = TILE_EDGE * TILES_PER_ROW
WORDS_PER_TILE = TILE_EDGE * TILE_EDGE // 4
PALETTE = bytes(channel for index in range(16) for channel in (17 * index,) * 3)


@dataclass(frozen=True)
class TileSheet(WordStream):
    def baseline(self) -> dict:
        return dict(format=FORMAT, stream=self.stream.id, source_start=self.stream.start,
                    source_end=self.stream.end, vram_start=self.stream.vram, marker=self.marker,
                    output_counts=[count for count, _ in self.commands],
                    strips=[vars(strip) for strip in self.strips])


def load_sheets(root: Path, stream_ids: tuple[str, ...] = STREAM_IDS) -> tuple[TileSheet, ...]:
    """Resolve the actual edition's asset graph once without an original ROM."""
    if not stream_ids or any(stream_id not in STREAM_IDS for stream_id in stream_ids):
        raise ValueError('choose one or more of the five battle tile uploads')
    return tuple(TileSheet(**vars(asset)) for asset in load_assets(root, stream_ids).streams)


def load_sheet(root: Path, stream_id: str) -> TileSheet:
    return load_sheets(root, (stream_id,))[0]


def _word_position(word_index: int) -> int:
    tile_index, tile_word = divmod(word_index, WORDS_PER_TILE)
    tile_row, tile_column = divmod(tile_index, TILES_PER_ROW)
    row, half = divmod(tile_word, TILE_EDGE // 4)
    return (tile_row * TILE_EDGE + row) * SIDE + tile_column * TILE_EDGE + half * 4


def sheet_pixels(sheet: TileSheet) -> bytes:
    """The original upload is already ordered in 32-byte, 8×8 tiles."""
    pixels = bytearray(SIDE * SIDE)
    for index in range(sheet.stream.words):
        pos = _word_position(index)
        pixels[pos:pos + 4] = nibbles(int.from_bytes(sheet.decoded[2 * index:2 * index + 2], 'big'))
    return bytes(pixels)


def sheet_png(pixels: bytes) -> bytes:
    _validate_pixels(pixels)
    picture = Image.frombytes('P', (SIDE, SIDE), pixels)
    picture.putpalette(PALETTE)
    result = BytesIO()
    picture.save(result, format='PNG', bits=4)
    return result.getvalue()


def _validate_pixels(pixels: bytes):
    if type(pixels) is not bytes or len(pixels) != SIDE * SIDE or any(index >= 16 for index in pixels):
        raise ValueError('complete 128×128 four-bit pixel indices required')


def _read_sheet(path: Path) -> bytes:
    raw = media._read(media.member_path(path.parent, path.name), media.MAX_PNG)
    with Image.open(BytesIO(raw)) as picture:
        if (picture.format != 'PNG' or picture.mode != 'P' or picture.size != (SIDE, SIDE)
                or getattr(picture, 'n_frames', 1) != 1 or 'transparency' in picture.info
                or bytes(picture.getpalette() or ())[:len(PALETTE)] != PALETTE):
            raise ValueError('use one opaque indexed PNG with its original 16 palette entries and 128×128 dimensions')
        pixels = picture.tobytes()
    _validate_pixels(pixels)
    return pixels


def _decoded_words(pixels: bytes, count: int) -> tuple[int, ...]:
    values = []
    for index in range(count):
        offset = _word_position(index)
        a, b, c, d = pixels[offset:offset + 4]
        values.append((a << 12) | (b << 8) | (c << 4) | d)
    return tuple(values)


def replacements(sheet: TileSheet, edited: bytes) -> tuple[dict[str, bytes], dict]:
    """Prepare only the existing pixel strips that must change, keeping RLE controls."""
    _validate_pixels(edited)
    files, receipt = word_replacements(sheet, _decoded_words(edited, sheet.stream.words))
    return files, dict(format=FORMAT, **receipt)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest='mode', required=True)
    for mode in ('export', 'prepare'):
        command = modes.add_parser(mode)
        command.add_argument('--edition-root', type=Path, required=True)
        command.add_argument('--stream', choices=STREAM_IDS, required=True)
        command.add_argument('--output', type=Path, required=True)
        if mode == 'prepare':
            command.add_argument('--baseline-dir', type=Path, required=True)
            command.add_argument('--edited', type=Path, required=True)
    args = parser.parse_args(argv)
    sheet = load_sheet(args.edition_root, args.stream)
    filename = f'{args.stream}.png'
    if args.mode == 'export':
        files = {filename: sheet_png(sheet_pixels(sheet)), 'baseline.json': media.json_bytes(sheet.baseline())}
    else:
        if (_read_json(args.baseline_dir, 'baseline.json') != sheet.baseline()
                or _read_sheet(args.baseline_dir / filename) != sheet_pixels(sheet)):
            raise ValueError('battle tile baseline no longer matches this edition; export again')
        files, receipt = replacements(sheet, _read_sheet(args.edited))
        files['replacements.json'] = media.json_bytes(receipt)
    print(_publish(args.edition_root, args.output, files))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
