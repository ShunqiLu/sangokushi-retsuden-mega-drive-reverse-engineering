# 具名音频序列命令

`audio_sequence_sources.py` 在原定宽声音事件上提供具名参数。完整音频文档格式为 `g5510-named-audio-sequence-commands-v1`，视图成员格式为 `g5510-named-stateful-sequence-views-v1`。物理事件与视图的共享关系及读取顺序由原登记源提供。

| 参数类别 | 原始表示 |
| --- | --- |
| 声像、微调、衰减、断音延迟 | 各自的 BYTE |
| LFO 声像、相对或绝对寄存器动作 | 寄存器选择及后继 BYTE |
| Timer A、Timer B | Timer A 低／高 BYTE 与 Timer B BYTE |
| 乐器 | 选择 BYTE 的 bit 7 决定外部命令参数 |
| 跳转、调用与循环 | 原小端目标地址、BYTE 计数器索引与次数 |
| 延时倍数、移调与模式设置 | 保留原 BYTE，补码由声音驱动解释 |
| 扩展命令的未知参数 | `unknown_argument_bytes`，按原顺序保留 |

## 导出与编辑

`export` 从完整 typed 文档或素材图生成独立的具名文档；素材图提供对应的 `--source-root`。已有独立具名文档可直接用于 `edit`。输出写入已有 `build/` 下的新文件。

```powershell
python -B -X utf8 -m tools.high_level_rom.audio_sequence_sources export --source "$resources/resources/audio/audio_build.json" --source-root $resources --project-root . --output build/audio-sequences.named.json
python -B -X utf8 -m tools.high_level_rom.audio_sequence_sources edit --source build/audio-sequences.named.json --edits audio-command-edits.json --project-root . --output build/audio-sequences.edited.json
python -B -X utf8 -m tools.high_level_rom.audio_sequence_sources import --source build/audio-sequences.edited.json --project-root . --output build/audio-sequences.typed.json
```

编辑文件格式为 `g5510-named-audio-command-parameter-edits-v1`。每项的 `view` 包含原视图的 `id`、`address`、`rom_offset`、`reader`、`raw_frequency` 和 `slide`。`expected_parameters` 是当前完整参数对象，`parameters` 是保持同型的新完整对象。

`with_command_parameters(document, edits)` 应用已核对的唯一目标，并保持命令种类、参数结构、尺寸和物理分配。`to_named` 与 `from_named` 负责表示转换。使用 `tools.high_level_rom.export_media --named-audio-sequences` 可生成具名的外置音频源。
