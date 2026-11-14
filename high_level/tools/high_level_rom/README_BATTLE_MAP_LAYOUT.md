# 战斗背景布局

**简体中文** · [繁體中文](README_BATTLE_MAP_LAYOUT.zh-TW.md) · [日本語](README_BATTLE_MAP_LAYOUT.ja.md) · [English](README_BATTLE_MAP_LAYOUT.en.md)

[`battle_map_layout.py`](battle_map_layout.py) 导出 32×32 的背景格。每格包含 `tile`、`palette_line`、`flip_x`、`flip_y` 和 `priority`；像素来自[对应的图块 PNG](README_BATTLE_TILE_SHEET.md)。

```powershell
$resources = Read-Host '兼容素材根'
python -B -m tools.high_level_rom.battle_map_layout export --edition-root $resources --map map_a_0 --output ./map-layout
python -B -m tools.high_level_rom.battle_map_layout prepare --edition-root $resources --edits ./map-edits.json --output ./map-replacements
```

`layout.json` 的 `rows` 按行、列从 0 编号，`uses` 列出目录与槽位。目录 A 使用 Plane B 左半，目录 B 使用右半。编辑文档格式为 `g5510-battle-background-layout-edits-v1`，包含 `map_id` 与 `edits`。每项指定 `row`、`column`、完整原值 `expected` 及部分改动 `changes`。图块编号范围为 0–1279。

输出中的替换件位于素材相对路径 `assets/images/backgrounds/battle_graphics/maps/`；`replacements.json` 标出引用和变化字节。编码保持原压缩命令、结束符和槽长。一条重复命令覆盖的各格使用同一完整值。
