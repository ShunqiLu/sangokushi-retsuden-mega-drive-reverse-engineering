# 編輯遊戲內容

[简体中文](EDITING.md) · **繁體中文** · [日本語](EDITING.ja.md) · [English](EDITING.en.md)

程式和工具路徑從本目錄算起，素材路徑從建置引數 `--resource-root` 所選目錄算起。建議在本地副本編輯，隨後從原始碼重新建置。

| 內容 | 編輯入口 |
| --- | --- |
| 68000 和 Z80 程式 | `src/m68k/`、`src/z80/`；指令範圍見 `tools/reconstructed_assembly/layout/` |
| 城市、武將和勢力的劇本初值 | 素材根的 `resources/data/scenario_build.json`；見[劇本編輯](tools/high_level_rom/README_NAMED_SCENARIO_SOURCES.zh-TW.md) |
| 對話、武將名和城市名 | `resources/data/dialogue_text.json`；見[文字編輯](tools/high_level_rom/README_READABLE_TEXT.zh-TW.md) |
| AI 引數 | `resources/data/ai_threshold_pair_fields.json`、`resources/data/ai_selection_fields.json`；見[判斷閾值](tools/high_level_rom/README_AI_POLICY_SOURCES.zh-TW.md)和[候選資格](tools/high_level_rom/README_AI_SELECTION_SOURCES.zh-TW.md) |
| 影象和配色 | `assets/images/` 及對應佈局、調色 JSON；見[素材指南](ASSETS.zh-TW.md)、[戰鬥背景佈局](tools/high_level_rom/README_BATTLE_MAP_LAYOUT.zh-TW.md)、[圖塊表](tools/high_level_rom/README_BATTLE_TILE_SHEET.zh-TW.md)和[人物頭像](PORTRAITS.zh-TW.md) |
| 樂曲、音效和音色 | `resources/audio/` 及其引用的 `assets/audio/`；見[音訊序列](tools/high_level_rom/README_AUDIO_SEQUENCE_SOURCES.zh-TW.md)和[共享事件](tools/high_level_rom/README_AUDIO_SEQUENCE_EDITOR.zh-TW.md) |
| 當前存檔 | [存檔工具](tools/save_data/README.zh-TW.md)：[城市與勢力](tools/save_data/README_NAMED_CAMPAIGN.zh-TW.md)、[行軍隊伍](tools/save_data/README_CAMPAIGN_PACKETS.zh-TW.md)、[運輸指令](tools/save_data/README_CAMPAIGN_ORDERS.zh-TW.md) |

索引 PNG 用畫素編號表達圖塊資料。請保留畫素模式、尺寸和原檔案路徑，透過對應的調色 JSON 修改顯示顏色。按[建置說明](README.zh-TW.md)把修改後的素材根交給編譯器。
