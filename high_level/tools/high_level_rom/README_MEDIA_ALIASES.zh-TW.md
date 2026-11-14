# 共享素材與別名

[简体中文](README_MEDIA_ALIASES.md) · **繁體中文** · [日本語](README_MEDIA_ALIASES.ja.md) · [English](README_MEDIA_ALIASES.en.md)

`media_alias_sources.py` 和 `media_layout_sources.py` 表示共用圖塊、介面佈局及聲音成員。每個別名保留原記錄與共享目標，依賴同一組 PNG、佈局 JSON 或事件 JSON。編輯共享成員會同時作用於引用該成員的記錄。

```powershell
python -B -m tools.high_level_rom.export_media --source-root $typedResources --output ./editable-resources
```

素材轉換為資源圖與對應外接成員，正常建置根據圖中的相對路徑讀取成員。[頭像索引](README_PORTRAIT_CATALOG.zh-TW.md)提供姓名與頭像關係；[音訊源](README_AUDIO_SEQUENCE_SOURCES.zh-TW.md)提供樂譜事件的編輯介面。
