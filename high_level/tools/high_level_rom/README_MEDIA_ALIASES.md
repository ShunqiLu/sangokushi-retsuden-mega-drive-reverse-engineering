# 共享素材与别名

**简体中文** · [繁體中文](README_MEDIA_ALIASES.zh-TW.md) · [日本語](README_MEDIA_ALIASES.ja.md) · [English](README_MEDIA_ALIASES.en.md)

`media_alias_sources.py` 和 `media_layout_sources.py` 表示共用图块、界面布局及声音成员。每个别名保留原记录与共享目标，依赖同一组 PNG、布局 JSON 或事件 JSON。编辑共享成员会同时作用于引用该成员的记录。

```powershell
python -B -m tools.high_level_rom.export_media --source-root $typedResources --output ./editable-resources
```

素材转换为资源图与对应外置成员，正常构建根据图中的相对路径读取成员。[头像索引](README_PORTRAIT_CATALOG.md)提供姓名与头像关系；[音频源](README_AUDIO_SEQUENCE_SOURCES.md)提供乐谱事件的编辑接口。
