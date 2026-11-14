# 共有素材と別名

[简体中文](README_MEDIA_ALIASES.md) · [繁體中文](README_MEDIA_ALIASES.zh-TW.md) · **日本語** · [English](README_MEDIA_ALIASES.en.md)

`media_alias_sources.py` と `media_layout_sources.py` は共有タイル、UI 配置、音声ファイルを表します。別名は元レコードと共有先を保持し、同じ PNG、配置 JSON、イベント JSON を参照します。共有ファイルを編集すると、参照する全レコードに反映されます。

```powershell
python -B -m tools.high_level_rom.export_media --source-root $typedResources --output ./editable-resources
```

素材を変換すると、素材グラフと対応する外部ファイルが生成されます。通常のビルドはグラフ内の相対パスでファイルを読みます。[顔グラフィック索引](README_PORTRAIT_CATALOG.ja.md)は名前を顔に対応付け、[音声ソース](README_AUDIO_SEQUENCE_SOURCES.ja.md)では楽譜イベントを編集できます。
