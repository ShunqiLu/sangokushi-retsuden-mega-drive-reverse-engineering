# 戰鬥背景圖塊表

[简体中文](README_BATTLE_TILE_SHEET.md) · **繁體中文** · [日本語](README_BATTLE_TILE_SHEET.ja.md) · [English](README_BATTLE_TILE_SHEET.en.md)

圖塊表為 128×128 索引 PNG，包含 16×16 個 8×8 圖塊。`tiles_0` 到 `tiles_4` 對應五套圖塊。畫素編號使用圖塊表的 16 項索引，畫面的實際配色來自遊戲調色盤。圖塊位置和翻轉由[地圖佈局](README_BATTLE_MAP_LAYOUT.zh-TW.md)編輯。

`$resources` 是同時包含 `resources/` 和 `assets/` 的本地素材根。命令從彙編版根目錄執行。 把結果存到素材根以外的新目錄。

```powershell
$resources = Read-Host '本地素材根目录'
python -B -m tools.high_level_rom.battle_tile_sheet export --edition-root $resources --stream tiles_0 --output ./tile-sheet
python -B -m tools.high_level_rom.battle_tile_sheet prepare --edition-root $resources --stream tiles_0 --baseline-dir ./tile-sheet --edited ./tiles-edited.png --output ./tile-replacements
```

保留匯出的 `baseline.json` 和原圖作為比較來源。編輯副本保持不透明索引模式、128×128 尺寸和原調色盤順序。共享壓縮命令的所有位置使用同一組畫素。`replacements.json` 列出可複製到本地素材副本的實際圖條。
