# 编辑共享乐谱事件

共享乐谱事件保存在本地运行副本的 `assets/audio/shared/stateful_event_views.json`。一项编辑提供视图 `view_id`、字段 `field`、原值 `expected` 和新值 `value`；[编辑示例](examples/audio_sequence_field_edits.example.json)展示文档结构。

请从具备源码和本地素材的副本根目录执行：

```powershell
python -B -m tools.high_level_rom.audio_sequence_asset_editor --edits ./sequence-edits.json --output ./stateful_event_views.json
```

输出包括新素材和记录变更位置及共享视图的摘要。检查后把新素材放回本地副本的对应路径，再按[构建说明](../../README.md)编入卡带。
