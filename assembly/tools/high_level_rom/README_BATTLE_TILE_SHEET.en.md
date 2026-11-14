# Battle background tile sheets

[简体中文](README_BATTLE_TILE_SHEET.md) · [繁體中文](README_BATTLE_TILE_SHEET.zh-TW.md) · [日本語](README_BATTLE_TILE_SHEET.ja.md) · **English**

Each indexed PNG is 128 × 128 pixels, a 16 × 16 grid of 8 × 8 tiles. `tiles_0` through `tiles_4` select the five tile sets. Pixels store one of the sheet's 16 indices; in-game colors come from the game palette. Edit positions and flips through the [map layout](README_BATTLE_MAP_LAYOUT.en.md).

`$resources` is the local resource root containing `resources/` and `assets/`. Run from the assembly root. Write results to a new directory outside the resource root.

```powershell
$resources = Read-Host '本地素材根目录'
python -B -m tools.high_level_rom.battle_tile_sheet export --edition-root $resources --stream tiles_0 --output ./tile-sheet
python -B -m tools.high_level_rom.battle_tile_sheet prepare --edition-root $resources --stream tiles_0 --baseline-dir ./tile-sheet --edited ./tiles-edited.png --output ./tile-replacements
```

Keep the exported `baseline.json` and the original image for comparison. Edited sheets must stay opaque and indexed, at 128 × 128, with the original palette order. All positions covered by a shared compressed command must use the same pixels. `replacements.json` lists the tile strips to copy into the local resource pack.
