"""Read and edit one actual 32×32 Plane B map without modifying the ROM."""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, replace
from pathlib import Path

from tools.battle_graphics import battle_graphics as battle

from . import media_sources as media
from .battle_asset_streams import BattleAssets, WordStream, load_assets, publish_files, read_json, word_replacements


WIDTH = HEIGHT = 32
MAP_IDS = tuple(stream.id for stream in battle.STREAMS if stream.vram is None)
LOADED_TILE_COUNT = sum(stream.words * 2 // 32 for stream in battle.STREAMS if stream.vram is not None)
LAYOUT_FORMAT = 'g5510-battle-background-layout-v1'
EDIT_FORMAT = 'g5510-battle-background-layout-edits-v1'


@dataclass(frozen=True)
class Cell:
    tile: int
    palette_line: int
    flip_x: bool
    flip_y: bool
    priority: bool

    @classmethod
    def from_word(cls, word: int) -> Cell:
        return cls(word & 0x7FF, (word >> 13) & 3, bool(word & 0x0800),
                   bool(word & 0x1000), bool(word & 0x8000))

    def to_word(self) -> int:
        if (type(self.tile) is not int or not 0 <= self.tile < 2048 or
                type(self.palette_line) is not int or not 0 <= self.palette_line < 4 or
                any(type(flag) is not bool for flag in (self.flip_x, self.flip_y, self.priority))):
            raise ValueError('a cell needs an 11-bit tile, palette line 0..3 and three boolean flags')
        return (self.tile | self.flip_x << 11 | self.flip_y << 12 |
                self.palette_line << 13 | self.priority << 15)


CELL_FIELDS = frozenset(Cell.__dataclass_fields__)


@dataclass(frozen=True)
class MapLayout:
    source: WordStream
    cells: tuple[Cell, ...]
    uses: tuple[tuple[str, int], ...]

    def document(self) -> dict:
        return dict(format=LAYOUT_FORMAT, map_id=self.source.stream.id,
                    source_start=self.source.stream.start, source_end=self.source.stream.end,
                    uses=_uses(self), width=WIDTH, height=HEIGHT,
                    rows=[[asdict(cell) for cell in self.cells[start:start + WIDTH]]
                          for start in range(0, len(self.cells), WIDTH)])


def _uses(layout: MapLayout) -> list[dict]:
    return [dict(directory=directory, slot=slot, side='left' if directory == 'directory_a' else 'right')
            for directory, slot in layout.uses]


def layouts_from_assets(assets: BattleAssets) -> tuple[MapLayout, ...]:
    layouts = []
    for asset in assets.streams:
        stream = asset.stream
        if stream.id not in MAP_IDS or stream.order != 'big' or stream.words != WIDTH * HEIGHT:
            raise ValueError('a registered 32×32 battle map is required')
        cells = tuple(Cell.from_word(int.from_bytes(asset.decoded[index:index + 2], 'big'))
                      for index in range(0, len(asset.decoded), 2))
        uses = tuple((name, slot) for name, targets in assets.directories for slot, target in enumerate(targets)
                     if target == stream.id)
        layouts.append(MapLayout(asset, cells, uses))
    return tuple(layouts)


def load_layout(root: Path, map_id: str) -> MapLayout:
    if map_id not in MAP_IDS:
        raise ValueError('choose one of the eight registered battle maps')
    layout, = layouts_from_assets(load_assets(root, (map_id,)))
    return layout


def prepare(layout: MapLayout, transaction: dict) -> tuple[dict[str, bytes], dict]:
    """Apply guarded cell edits and return replacement files in the edition layout."""
    if (type(transaction) is not dict or set(transaction) != {'format', 'map_id', 'edits'}
            or transaction['format'] != EDIT_FORMAT or transaction['map_id'] != layout.source.stream.id
            or type(transaction['edits']) is not list or not 1 <= len(transaction['edits']) <= WIDTH * HEIGHT):
        raise ValueError('one explicit battle map edit document for this registered map is required')
    edited = list(layout.cells)
    used, affected = set(), []
    for item in transaction['edits']:
        if type(item) is not dict or set(item) != {'row', 'column', 'expected', 'changes'}:
            raise ValueError('each map edit must have row, column, expected and changes')
        row, column, expected, changes = (item[key] for key in ('row', 'column', 'expected', 'changes'))
        if type(row) is not int or type(column) is not int or not 0 <= row < HEIGHT or not 0 <= column < WIDTH:
            raise ValueError('row and column are zero-based and must be within the 32×32 map')
        index = row * WIDTH + column
        if index in used:
            raise ValueError(f'duplicate map cell ({row},{column})')
        used.add(index)
        if type(expected) is not dict or set(expected) != CELL_FIELDS:
            raise ValueError(f'provide the complete original cell ({row},{column})')
        before = layout.cells[index]
        if Cell(**expected).to_word() != before.to_word():
            raise ValueError(f'original cell ({row},{column}) has changed; export the map again')
        if type(changes) is not dict or not changes or not set(changes) <= CELL_FIELDS:
            raise ValueError(f'unknown or empty map attributes for cell ({row},{column})')
        after = replace(before, **changes)
        word = after.to_word()
        if after.tile != before.tile and after.tile >= LOADED_TILE_COUNT:
            raise ValueError(f'tile {after.tile} is outside the known battle uploads (0..{LOADED_TILE_COUNT - 1})')
        edited[index] = after
        if word != before.to_word():
            affected.append(dict(row=row, column=column, before=asdict(before), after=asdict(after)))
    files, result = word_replacements(layout.source, tuple(cell.to_word() for cell in edited))
    return files, dict(format=LAYOUT_FORMAT, uses=_uses(layout), cells=affected, **result)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest='mode', required=True)
    export, edit = (modes.add_parser(mode) for mode in ('export', 'prepare'))
    for command in (export, edit):
        command.add_argument('--edition-root', required=True, type=Path)
        command.add_argument('--output', required=True, type=Path)
    export.add_argument('--map', required=True, choices=MAP_IDS)
    edit.add_argument('--edits', required=True, type=Path)
    args = parser.parse_args(argv)
    if args.mode == 'export':
        layout = load_layout(args.edition_root, args.map)
        files = {'layout.json': media.json_bytes(layout.document())}
    else:
        transaction = read_json(args.edits.parent, args.edits.name)
        if type(transaction) is not dict or type(transaction.get('map_id')) is not str:
            raise ValueError('provide the map_id in the edit document')
        layout = load_layout(args.edition_root, transaction['map_id'])
        files, result = prepare(layout, transaction)
        files['replacements.json'] = media.json_bytes(result)
    print(publish_files(args.edition_root, args.output, files))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
