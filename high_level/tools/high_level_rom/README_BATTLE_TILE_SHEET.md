# 战斗背景图块表

[`battle_tile_sheet.py`](battle_tile_sheet.py) 为 `tiles_0` 到 `tiles_4` 中选定的图块组生成 128×128 索引 PNG。16×16 个图块按 VRAM 上传顺序排列，每块为 8×8。显示灰度代表索引；游戏颜色来自实际调色板。[布局编辑器](README_BATTLE_MAP_LAYOUT.md)负责格位置、翻转和调色板行。

```powershell
$resources = Read-Host '兼容素材根'
python -B -m tools.high_level_rom.battle_tile_sheet export --edition-root $resources --stream tiles_0 --output ./tile-sheet
python -B -m tools.high_level_rom.battle_tile_sheet prepare --edition-root $resources --stream tiles_0 --baseline-dir ./tile-sheet --edited ./tiles-edited.png --output ./tile-replacements
```

输出目录为素材根之外的新增目录。以原 PNG 与 `baseline.json` 作为回写基线，并用保持 128×128、索引色和前 16 项调色板的单独 PNG 提供编辑。输出中的改变图条沿用 `assets/images/backgrounds/battle_graphics/` 的相对路径；`replacements.json` 标出替换文件与原线性地址。

同一重复命令覆盖的各位置使用相同的四像素 WORD。编码保持命令边界、重复次数、结束符、大小与线性位置；字面命令继续采用原转义规则。
