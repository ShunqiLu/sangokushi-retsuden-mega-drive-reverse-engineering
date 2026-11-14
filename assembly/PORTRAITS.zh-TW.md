# 編輯武將頭像

[简体中文](PORTRAITS.md) · **繁體中文** · [日本語](PORTRAITS.ja.md) · [English](PORTRAITS.en.md)

[頭像索引工具](tools/high_level_rom/README_PORTRAIT_CATALOG.zh-TW.md)以文字、頭像和劇本三個來源建立人物索引。查詢索引中的 `name.text` 或 `officer_record_id`，隨後跟隨佈局、調色盤和圖塊引用編輯實際素材。共享圖塊對應多個人物。

素材根提供以下入口：

- `resources/data/dialogue_text.json`：武將姓名。
- `resources/images/portrait_graphics.json`：頭像佈局、調色盤和外接 PNG 引用。
- `resources/data/scenario_build.json`：劇本與人物記錄。
