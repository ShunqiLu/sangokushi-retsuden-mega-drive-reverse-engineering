# Battle background tile sheets

[简体中文](README_BATTLE_TILE_SHEET.md) · [繁體中文](README_BATTLE_TILE_SHEET.zh-TW.md) · [日本語](README_BATTLE_TILE_SHEET.ja.md) · **English**

[`battle_tile_sheet.py`](battle_tile_sheet.py) exports a 128 × 128 indexed PNG for a tile group from `tiles_0` through `tiles_4`. It lays out a 16 × 16 grid of 8 × 8 tiles in VRAM upload order. Gray levels display indices; in-game colors come from the palette. Use the [layout editor](README_BATTLE_MAP_LAYOUT.en.md) for cell positions, flips, and palette rows.

```powershell
$resources = Read-Host '兼容素材根'
python -B -m tools.high_level_rom.battle_tile_sheet export --edition-root $resources --stream tiles_0 --output ./tile-sheet
python -B -m tools.high_level_rom.battle_tile_sheet prepare --edition-root $resources --stream tiles_0 --baseline-dir ./tile-sheet --edited ./tiles-edited.png --output ./tile-replacements
```

Use a fresh output directory outside the resource root. Keep the original PNG and `baseline.json` as the baseline. Supply a separate edited PNG with the same 128 × 128 dimensions, indexed mode, and first 16 palette entries. Changed strips follow the relative paths in `assets/images/backgrounds/battle_graphics/`; `replacements.json` lists replacements and original linear addresses.

All positions covered by one repeat command use the same four-pixel WORD. Encoding preserves command boundaries, repeat counts, terminators, lengths, and linear offsets. Literal commands keep their original escaping rules.
