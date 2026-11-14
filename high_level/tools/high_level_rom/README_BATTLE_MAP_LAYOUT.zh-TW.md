# 戰鬥背景佈局

[简体中文](README_BATTLE_MAP_LAYOUT.md) · **繁體中文** · [日本語](README_BATTLE_MAP_LAYOUT.ja.md) · [English](README_BATTLE_MAP_LAYOUT.en.md)

[`battle_map_layout.py`](battle_map_layout.py) 匯出 32×32 的背景格。每格包含 `tile`、`palette_line`、`flip_x`、`flip_y` 和 `priority`；畫素來自[對應的圖塊 PNG](README_BATTLE_TILE_SHEET.zh-TW.md)。

```powershell
$resources = Read-Host '兼容素材根'
python -B -m tools.high_level_rom.battle_map_layout export --edition-root $resources --map map_a_0 --output ./map-layout
python -B -m tools.high_level_rom.battle_map_layout prepare --edition-root $resources --edits ./map-edits.json --output ./map-replacements
```

`layout.json` 的 `rows` 按行、列從 0 編號，`uses` 列出目錄與槽位。目錄 A 使用 Plane B 左半，目錄 B 使用右半。編輯文件格式為 `g5510-battle-background-layout-edits-v1`，包含 `map_id` 與 `edits`。每項指定 `row`、`column`、完整原值 `expected` 及部分改動 `changes`。圖塊編號範圍為 0–1279。

輸出中的替換件位於素材相對路徑 `assets/images/backgrounds/battle_graphics/maps/`；`replacements.json` 標出引用和變化位元組。編碼保持原壓縮命令、結束符和槽長。一條重複命令覆蓋的各格使用同一完整值。
