# 编辑共享乐谱事件

此工具在本地运行目录读取 `resources/audio/audio_build.json` 和 `assets/audio/`，按当前版本的登记与编码核对编辑。编辑文件的形状见[字段示例](examples/audio_sequence_field_edits.example.json)；`view_id` 和 `expected` 来自当前 `assets/audio/shared/stateful_event_views.json`。

```powershell
New-Item -ItemType Directory -Path build/audio-sequence-edit
python -B -X utf8 -m tools.high_level_rom.audio_sequence_asset_editor --edits audio-edits.json --output build/audio-sequence-edit/stateful_event_views.json
```

编辑字段为 `note`（`0x80..0xDF`）以及 `fm_attenuation.attenuation_byte`、`fine_detune.fine_detune_byte` 和 `pan.pan_byte`。各字段使用原驱动的字节单位，命令宽度、时值和控制流保持原结构。

输出包含候选事件文件和对应的 `stateful_event_views.edit-receipt.json`。结果列出不同的编码字节，以及读取或预读这些字节的视图。以候选作为素材中的同名成员，可参加[正常构建](README_BUILD.md)。
