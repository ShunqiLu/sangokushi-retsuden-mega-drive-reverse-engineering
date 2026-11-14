# 中文对话、武将名与城市名

[`readable_text.py`](readable_text.py) 将 typed 文本转换为 `g5510-owned-main-text-unicode-source-v1`。字符由 [低段字形表](text_sources/glyphs_lower.json) 与 [高段字形表](text_sources/glyphs_upper.json) 映射；重码、未知图形及非规范控制值用四位大写十六进制 `⟦XXXX⟧` 精确表示。

对话保留原文字槽与各个控制 WORD 的位置和值，含末尾恢复控制。对话中的 `0000` 是图形操作，`4000` 对应字形 0；名称中的 `0000` 对应字形 0。武将名占 3 WORD，城市名占 2 WORD。

`export` 使用含 typed 文本的素材根 `$typedResources`；已有可读文档可直接作为 `edit --source` 的输入。输出写入已有 `build/` 下的新文件。

```powershell
python -B -X utf8 -m tools.high_level_rom.readable_text export --project-root . --source "$typedResources/resources/data/dialogue_text.json" --glyph-sources tools/high_level_rom/text_sources/glyphs_lower.json tools/high_level_rom/text_sources/glyphs_upper.json --output build/dialogue-readable.json
python -B -X utf8 -m tools.high_level_rom.readable_text edit --project-root . --source build/dialogue-readable.json --edits text-edits.json --output build/dialogue-edited.json
```

编辑文件格式为 `g5510-main-text-record-edits-v1`，包含 `format` 与 `edits`。各项通过 `collection` 和 `id` 定位实际记录，提供原完整 `expected_text` 和新 `text`。批处理核对固定 WORD 数和控制符，返回独立文档。Python 调用可使用 `with_text_edits`；`MainTextWordCodec` 执行字符与精确 WORD 的转换。
