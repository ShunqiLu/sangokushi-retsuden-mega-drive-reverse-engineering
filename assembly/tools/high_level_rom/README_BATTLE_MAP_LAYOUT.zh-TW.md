# 戰鬥背景佈局

[简体中文](README_BATTLE_MAP_LAYOUT.md) · **繁體中文** · [日本語](README_BATTLE_MAP_LAYOUT.ja.md) · [English](README_BATTLE_MAP_LAYOUT.en.md)

地圖包含 32×32 個格子。每格記錄圖塊、調色盤行、橫向翻轉、縱向翻轉和優先位。A 表和 B 表分別選取同一背景的左半和右半。圖塊畫素可用[圖塊表編輯器](README_BATTLE_TILE_SHEET.zh-TW.md)修改。

`$resources` 是同時包含 `resources/` 和 `assets/` 的本地素材根。命令從彙編版根目錄執行。 把結果存到素材根以外的新目錄。

```powershell
$resources = Read-Host '本地素材根目录'
python -B -m tools.high_level_rom.battle_map_layout export --edition-root $resources --map map_a_0 --output ./map-layout
python -B -m tools.high_level_rom.battle_map_layout prepare --edition-root $resources --edits ./map-edits.json --output ./map-replacements
```

編輯文件以 `map_id` 選擇地圖，每項填寫零起算的 `row`、`column`、原格 `expected` 和待改欄位 `changes`。原格欄位從匯出檔案複製。`prepare` 保留原壓縮槽和結束命令，生成替換檔案及 `replacements.json`。同一條重複命令覆蓋的格子須使用相同的數值。核對後將替換檔案按相對路徑放入本地素材副本。
