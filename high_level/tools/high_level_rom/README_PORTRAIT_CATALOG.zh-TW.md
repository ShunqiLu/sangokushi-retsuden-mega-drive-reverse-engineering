# 頭像索引生成器

[简体中文](README_PORTRAIT_CATALOG.md) · **繁體中文** · [日本語](README_PORTRAIT_CATALOG.ja.md) · [English](README_PORTRAIT_CATALOG.en.md)

[`portrait_catalog.py`](portrait_catalog.py) 將可讀武將姓名、劇本記錄、頭像佈局、調色盤與共享圖塊連成查詢索引。輸出中的 `officers` 支援姓名和記錄 ID 查詢，`shared_tiles` 指出共同使用的影象成員。記錄與畫面之間的已知連線及待定身份各用原狀態表示。

```powershell
python -B -X utf8 -m tools.high_level_rom.portrait_catalog --project-root . --names-source "$resources/resources/data/dialogue_text.json" --portrait-source "$resources/resources/images/portrait_graphics.json" --record-authority "$resources/resources/data/scenario_build.json" --source-root $resources --output build/officer-portraits.json
```

`--names-source` 使用[可讀文字源](README_READABLE_TEXT.zh-TW.md)，可直接指向素材根中的具名對話檔案；`--source-root` 用於解析實際頭像成員。新的索引檔案寫在專案的 `build/` 內。[頭像編輯指南](../../PORTRAITS.zh-TW.md)說明如何從索引定位真正的編輯源。
