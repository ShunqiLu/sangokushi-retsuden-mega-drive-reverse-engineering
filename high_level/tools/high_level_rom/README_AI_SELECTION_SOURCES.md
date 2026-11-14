# AI 候选资格表

`ai_selection_fields` 有 14 行、每行 14 个候选 BYTE。选拔业务读取 `first_gate_byte`，值 0 和 1 通过这道门槛；随后由关系位、势力代表项和城市数继续决定。0 与 1 保持为不同原值，2–255 保持各自的 BYTE 值。物理行以原记录 ID 标识。

具名素材可直接提供给 `edit`；下列导出从含 typed 源的素材根 `$typedResources` 生成具名文档。输出写入已有 `build/` 下的新文件。

```powershell
python -B -m tools.high_level_rom.ai_selection_sources export --source "$typedResources/resources/data/ai_selection_fields.json" --project-root . --output build/ai-selection.named.json
python -B -m tools.high_level_rom.ai_selection_sources edit --source build/ai-selection.named.json --edits candidate-edits.json --project-root . --output build/ai-selection.edited.json
```

编辑文件格式为 `g5510-ai-candidate-first-gate-edits-v1`，包含 `format` 与 `edits`。一个编辑项使用 `row_id`、`candidate_index`（0–13）、`expected_gate_byte` 及 `gate_byte`，并对照源中的当前记录和值。

`to_named` 生成 `g5510-named-ai-candidate-first-gates-v1`；`from_named` 恢复原字段表示。`with_candidate_gates(source, edits)` 应用整批唯一目标，保留各行、位置和附加元数据。正常编码器使用对应的登记资源。
