# 战斗背景布局

**简体中文** · [繁體中文](README_BATTLE_MAP_LAYOUT.zh-TW.md) · [日本語](README_BATTLE_MAP_LAYOUT.ja.md) · [English](README_BATTLE_MAP_LAYOUT.en.md)

地图包含 32×32 个格子。每格记录图块、调色板行、横向翻转、纵向翻转和优先位。A 表和 B 表分别选取同一背景的左半和右半。图块像素可用[图块表编辑器](README_BATTLE_TILE_SHEET.md)修改。

`$resources` 是同时包含 `resources/` 和 `assets/` 的本地素材根。命令从汇编版根目录运行。 把结果存到素材根以外的新目录。

```powershell
$resources = Read-Host '本地素材根目录'
python -B -m tools.high_level_rom.battle_map_layout export --edition-root $resources --map map_a_0 --output ./map-layout
python -B -m tools.high_level_rom.battle_map_layout prepare --edition-root $resources --edits ./map-edits.json --output ./map-replacements
```

编辑文档以 `map_id` 选择地图，每项填写零起算的 `row`、`column`、原格 `expected` 和待改字段 `changes`。原格字段从导出文件复制。`prepare` 保留原压缩槽和结束命令，生成替换文件及 `replacements.json`。同一条重复命令覆盖的格子须使用相同的数值。核对后将替换文件按相对路径放入本地素材副本。
