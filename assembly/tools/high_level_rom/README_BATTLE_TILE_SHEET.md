# 战斗背景图块表

图块表为 128×128 索引 PNG，包含 16×16 个 8×8 图块。`tiles_0` 到 `tiles_4` 对应五套图块。像素编号使用图块表的 16 项索引，画面的实际配色来自游戏调色板。图块位置和翻转由[地图布局](README_BATTLE_MAP_LAYOUT.md)编辑。

`$resources` 是同时包含 `resources/` 和 `assets/` 的本地素材根。命令从汇编版根目录运行。 把结果存到素材根以外的新目录。

```powershell
$resources = Read-Host '本地素材根目录'
python -B -m tools.high_level_rom.battle_tile_sheet export --edition-root $resources --stream tiles_0 --output ./tile-sheet
python -B -m tools.high_level_rom.battle_tile_sheet prepare --edition-root $resources --stream tiles_0 --baseline-dir ./tile-sheet --edited ./tiles-edited.png --output ./tile-replacements
```

保留导出的 `baseline.json` 和原图作为比较来源。编辑副本保持不透明索引模式、128×128 尺寸和原调色板顺序。共享压缩命令的所有位置使用同一组像素。`replacements.json` 列出可复制到本地素材副本的实际图条。
