# Battle background layout

[简体中文](README_BATTLE_MAP_LAYOUT.md) · [繁體中文](README_BATTLE_MAP_LAYOUT.zh-TW.md) · [日本語](README_BATTLE_MAP_LAYOUT.ja.md) · **English**

The map has 32 × 32 cells. Each cell stores a tile, palette row, horizontal and vertical flip flags, and a priority bit. Tables A and B select the left and right halves of one background. Edit tile pixels with the [tile sheet editor](README_BATTLE_TILE_SHEET.en.md).

`$resources` is the local resource root containing `resources/` and `assets/`. Run from the assembly root. Write results to a new directory outside the resource root.

```powershell
$resources = Read-Host '本地素材根目录'
python -B -m tools.high_level_rom.battle_map_layout export --edition-root $resources --map map_a_0 --output ./map-layout
python -B -m tools.high_level_rom.battle_map_layout prepare --edition-root $resources --edits ./map-edits.json --output ./map-replacements
```

Select a map with `map_id`. Each edit specifies zero-based `row` and `column`, the original cell `expected`, and changed fields `changes`. Copy original fields from the export. `prepare` keeps the original compression slot and end command and writes replacements and `replacements.json`. Cells covered by the same repeat command must share one value. After review, copy the replacements to their relative paths in the local pack.
