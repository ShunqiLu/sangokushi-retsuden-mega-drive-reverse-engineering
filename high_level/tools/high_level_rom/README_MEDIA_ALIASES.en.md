# Shared resources and aliases

[简体中文](README_MEDIA_ALIASES.md) · [繁體中文](README_MEDIA_ALIASES.zh-TW.md) · [日本語](README_MEDIA_ALIASES.ja.md) · **English**

`media_alias_sources.py` and `media_layout_sources.py` refer to shared tiles, UI layouts, and audio members. An alias preserves its original record and shared target. The records depend on the same PNG, layout JSON, or event JSON. Editing the shared file affects every record that uses it.

```powershell
python -B -m tools.high_level_rom.export_media --source-root $typedResources --output ./editable-resources
```

Resource conversion produces a graph and its external files. The build loads files by their paths in the graph. The [portrait index](README_PORTRAIT_CATALOG.en.md) links names to portraits, and [audio sources](README_AUDIO_SEQUENCE_SOURCES.en.md) provides the score event editing interface.
