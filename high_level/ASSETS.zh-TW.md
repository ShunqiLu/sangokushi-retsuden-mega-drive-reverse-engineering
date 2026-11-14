# 影象、音訊與劇本素材

[简体中文](ASSETS.md) · **繁體中文** · [日本語](ASSETS.ja.md) · [English](ASSETS.en.md)

`--resource-root` 指向一份相容的本地素材目錄。下面的路徑相對該目錄；原始碼中的建置器按資源 ID 讀取登記檔案，再解析對應的外接成員。

| 路徑 | 用途 |
| --- | --- |
| `resources/images/` | 圖塊、地圖、精靈、字型、頭像、調色盤及佈局的登記源 |
| `assets/images/` | 可編輯索引 PNG、地圖成員、佈局和調色盤 |
| `resources/audio/` | Z80 聲音驅動使用的樂譜、音色和外部事件登記源 |
| `assets/audio/` | 音符、控制事件、包絡、音色及共享聲音成員 |
| `resources/data/` | 劇本初值、AI 引數、文字和其他規則表 |

素材清單 `asset-source-manifest.json` 描述資源 ID、引用和編輯欄位。`ASSET_INDEX.json` 提供按檔案搜尋的派生檢視；[索引工具](tools/reconstruction_delivery/README_MEDIA_CATALOG.zh-TW.md)可根據素材清單生成它。

## 影象

PNG 畫素儲存的是調色盤索引，預覽顏色用於輔助辨認。實際遊戲顏色由對應的調色盤源決定。編輯時保持圖塊尺寸、索引位寬和共享成員引用；佈局的格座標、翻轉及優先順序由佈局工具處理。

- [戰鬥背景格與屬性](tools/high_level_rom/README_BATTLE_MAP_LAYOUT.zh-TW.md)、[戰鬥背景圖塊](tools/high_level_rom/README_BATTLE_TILE_SHEET.zh-TW.md)。
- [人物頭像](PORTRAITS.zh-TW.md)、[標題圖塊](tools/high_level_rom/README_TITLE_TILE_MEDIA.zh-TW.md)。
- [共享影象與音訊別名](tools/high_level_rom/README_MEDIA_ALIASES.zh-TW.md)。

## 聲音

樂譜和音效由有序事件、音色、包絡和共享成員組成。改動的物件是登記源及其成員；PCM 是音訊晶片模型產生的播放輸出。

- [音序與命令格式](tools/high_level_rom/README_AUDIO_SEQUENCE_SOURCES.zh-TW.md)、[共享事件編輯器](tools/high_level_rom/README_AUDIO_SEQUENCE_EDITOR.zh-TW.md)。
- [桌面 FM 音訊與晶片時鐘](tools/high_level_audio_engine/README_YMFM.zh-TW.md)。

## 規則資料

[具名劇本](tools/high_level_rom/README_NAMED_SCENARIO_SOURCES.zh-TW.md)、[AI 閾值](tools/high_level_rom/README_AI_POLICY_SOURCES.zh-TW.md)、[候選資格](tools/high_level_rom/README_AI_SELECTION_SOURCES.zh-TW.md)和[可讀文字](tools/high_level_rom/README_READABLE_TEXT.zh-TW.md)各有明確的編輯和編碼規則。各資源使用其原欄位寬度與佈局。
