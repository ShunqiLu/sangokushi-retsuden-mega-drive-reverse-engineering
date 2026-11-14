# 人物頭像

[简体中文](PORTRAITS.md) · **繁體中文** · [日本語](PORTRAITS.ja.md) · [English](PORTRAITS.en.md)

素材包中的 `OFFICER_PORTRAITS.json` 提供派生查詢索引。在 `officers` 中按 `name.text` 或 `officer_record_id` 查詢；未知字形保留精確轉義。

| 欄位 | 用途 |
| --- | --- |
| `portrait.layout_file` | 畫素塊與頭像格的佈局 JSON |
| `portrait.palette.file` | 調色盤 JSON |
| `tile_groups[].tile_ref` | `shared_tiles` 中的共享 PNG 引用 |

姓名來自 `resources/data/dialogue_text.json`，頭像來自 `resources/images/portrait_graphics.json`，武將記錄來自 `resources/data/scenario_build.json`。編輯共享 PNG 會影響引用它的多個頭像；身份待定的條目以 `unknown` 表示。

[頭像索引工具](tools/high_level_rom/README_PORTRAIT_CATALOG.zh-TW.md)說明定位與生成命令。
