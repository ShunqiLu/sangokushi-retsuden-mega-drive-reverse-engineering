# 編輯遊戲內容

[简体中文](EDITING.md) · **繁體中文** · [日本語](EDITING.ja.md) · [English](EDITING.en.md)

遊戲規則位於本原始碼目錄。影象、聲音和劇本資料位於透過 `--resource-root` 選擇的[素材根](ASSETS.zh-TW.md)。

| 內容 | 編輯入口 |
| --- | --- |
| 內政、行軍、戰鬥、AI 和場景規則 | `tools/high_level_*/business*.py` 中的領域函式，以及各領域的 `compiler*.py` 和 `target.py` |
| 城市、武將、勢力初值和劇本裝備 | [具名劇本資料](tools/high_level_rom/README_NAMED_SCENARIO_SOURCES.zh-TW.md) |
| AI 命令比較閾值 | [48 對 WORD 閾值](tools/high_level_rom/README_AI_POLICY_SOURCES.zh-TW.md) |
| AI 候選資格 | [14 × 14 BYTE 資格表](tools/high_level_rom/README_AI_SELECTION_SOURCES.zh-TW.md) |
| 中文對話、武將名和城市名 | [可讀文字格式](tools/high_level_rom/README_READABLE_TEXT.zh-TW.md) |
| 戰鬥背景 | [地圖格和屬性](tools/high_level_rom/README_BATTLE_MAP_LAYOUT.zh-TW.md)、[索引圖塊 PNG](tools/high_level_rom/README_BATTLE_TILE_SHEET.zh-TW.md) |
| 人物頭像 | [姓名、佈局、調色盤和共享圖塊](PORTRAITS.zh-TW.md) |
| 音樂、音效和音色 | [具名樂譜和事件源](tools/high_level_rom/README_AUDIO_SEQUENCE_SOURCES.zh-TW.md)、[共享事件編輯器](tools/high_level_rom/README_AUDIO_SEQUENCE_EDITOR.zh-TW.md) |
| 當前存檔 | [固定城市／武將／勢力記錄](tools/save_data/README_NAMED_CAMPAIGN.zh-TW.md)、[行軍隊伍](tools/save_data/README_CAMPAIGN_PACKETS.zh-TW.md)、[運輸命令](tools/save_data/README_CAMPAIGN_ORDERS.zh-TW.md) |

## 遊戲規則與建置

業務函式負責規則和狀態變化，`contexts*.py` 描述輸入與協作介面，編譯器和目標宣告負責指令、地址、暫存器語義及固定空間。可編譯的改動使用所屬領域支援的 Python 語句與狀態介面。原版邊界行為參見[相容行為記錄](docs/ORIGINAL_GAME_BUGS.zh-TW.md)。

編輯後的資源透過其正常登記入口參加[映象建置](tools/high_level_rom/README_BUILD.zh-TW.md)。生成的映象是產物；可重用的改動儲存在規則原始碼或本地素材源。

## 批次編輯結構化資料

編輯 API 接收完整輸入與一批明確的記錄、舊值和新值，返回一個獨立候選。原欄位的位寬、別名和檔案拓撲由各自的編碼器保持。

```python
from tools.high_level_rom.scenario_sources import with_scenario_fields

scenario = source["scenarios"][0]
city = next(row for row in scenario["cities"] if row["id"] == 3)
edited = with_scenario_fields(source, [{
    "scenario_id": scenario["id"],
    "group": "cities",
    "record_id": city["id"],
    "field": "gold",
    "expected_value": city["gold"],
    "value": 12000,
}])
```

劇本以物理記錄 ID 選擇目標，裝備使用源 BYTE 索引。城市的開發、民生和城防對應低 WORD，編碼器保留同槽的高 WORD。文字編輯保留固定字槽和控制 WORD；聲音編輯以完整檢視標識原事件，保留命令種類和尺寸。

## 當前存檔

[存檔命令](tools/save_data/README.zh-TW.md)以顯式的 8 KiB 邏輯儲存介質為基線。固定欄位、行軍隊伍和運輸命令各有獨立檢視，回寫產生新檔案。組合編輯以當前候選存檔作為下一項編輯的基線。每種檢視沿用遊戲的位寬、校驗和以及未用資料。
