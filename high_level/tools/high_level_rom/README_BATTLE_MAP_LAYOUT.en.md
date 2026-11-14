# Battle background layout

[简体中文](README_BATTLE_MAP_LAYOUT.md) · [繁體中文](README_BATTLE_MAP_LAYOUT.zh-TW.md) · [日本語](README_BATTLE_MAP_LAYOUT.ja.md) · **English**

[`battle_map_layout.py`](battle_map_layout.py) exports a 32 × 32 grid of background cells. Each cell contains `tile`, `palette_line`, `flip_x`, `flip_y`, and `priority`. Pixels come from the [tile PNGs](README_BATTLE_TILE_SHEET.en.md).

```powershell
$resources = Read-Host '兼容素材根'
python -B -m tools.high_level_rom.battle_map_layout export --edition-root $resources --map map_a_0 --output ./map-layout
python -B -m tools.high_level_rom.battle_map_layout prepare --edition-root $resources --edits ./map-edits.json --output ./map-replacements
```

In `layout.json`, `rows` uses zero-based row and column numbers, and `uses` lists directories and slots. Directory A uses the left half of Plane B, and directory B uses the right half. Edit files use format `g5510-battle-background-layout-edits-v1` with `map_id` and `edits`. Each edit specifies `row`, `column`, the full original value `expected`, and the changes `changes`. Tile IDs range from 0 to 1279.

Replacement files use the resource-relative path `assets/images/backgrounds/battle_graphics/maps/`. `replacements.json` records references and changed bytes. Encoding preserves the original compression commands, terminator, and slot length. Cells covered by one repeat command must have the same complete value.
