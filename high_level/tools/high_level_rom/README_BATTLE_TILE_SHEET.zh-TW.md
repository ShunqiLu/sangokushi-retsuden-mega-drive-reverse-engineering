# 戰鬥背景圖塊表

[简体中文](README_BATTLE_TILE_SHEET.md) · **繁體中文** · [日本語](README_BATTLE_TILE_SHEET.ja.md) · [English](README_BATTLE_TILE_SHEET.en.md)

[`battle_tile_sheet.py`](battle_tile_sheet.py) 為 `tiles_0` 到 `tiles_4` 中選定的圖塊組生成 128×128 索引 PNG。16×16 個圖塊按 VRAM 上傳順序排列，每塊為 8×8。顯示灰度代表索引；遊戲顏色來自實際調色盤。[佈局編輯器](README_BATTLE_MAP_LAYOUT.zh-TW.md)負責格位置、翻轉和調色盤行。

```powershell
$resources = Read-Host '兼容素材根'
python -B -m tools.high_level_rom.battle_tile_sheet export --edition-root $resources --stream tiles_0 --output ./tile-sheet
python -B -m tools.high_level_rom.battle_tile_sheet prepare --edition-root $resources --stream tiles_0 --baseline-dir ./tile-sheet --edited ./tiles-edited.png --output ./tile-replacements
```

輸出目錄為素材根之外的新增目錄。以原 PNG 與 `baseline.json` 作為回寫基線，並用保持 128×128、索引色和前 16 項調色盤的單獨 PNG 提供編輯。輸出中的改變圖條沿用 `assets/images/backgrounds/battle_graphics/` 的相對路徑；`replacements.json` 標出替換檔案與原線性地址。

同一重複命令覆蓋的各位置使用相同的四畫素 WORD。編碼保持命令邊界、重複次數、結束符、大小與線性位置；字面命令繼續採用原轉義規則。
