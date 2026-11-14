# AI 候选资格

`resources/data/ai_selection_fields.json` 提供 14×14 个 8 位参数，供决策的首道候选条件使用。具名视图分别保存分组、位置和原字节值。

`$resources` 是同时包含 `resources/` 和 `assets/` 的本地素材根。命令从汇编版根目录运行。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.ai_selection_sources edit --source "$resources/resources/data/ai_selection_fields.json" --edits ./ai-selection-edits.json --project-root . --output build/ai-selection.json
```

`edit` 接受 `--edits` 指向的编辑文档。`export` 和 `import` 双向转换具名与旧版结构化格式，并保留原分组和字节宽度。

编辑文档的 `format` 为 `g5510-ai-candidate-first-gate-edits-v1`。在 `edits` 数组中填写 `row_id`、`candidate_index`、`expected_gate_byte` 和 `gate_byte`。
