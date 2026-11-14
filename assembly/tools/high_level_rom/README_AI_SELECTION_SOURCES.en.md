# AI candidate eligibility

[简体中文](README_AI_SELECTION_SOURCES.md) · [繁體中文](README_AI_SELECTION_SOURCES.zh-TW.md) · [日本語](README_AI_SELECTION_SOURCES.ja.md) · **English**

`resources/data/ai_selection_fields.json` supplies the 14 × 14 8-bit parameters used in the first eligibility check. The named view preserves the group, position, and original byte value for each entry.

`$resources` is the local resource root containing `resources/` and `assets/`. Run the commands from the assembly root.

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.ai_selection_sources edit --source "$resources/resources/data/ai_selection_fields.json" --edits ./ai-selection-edits.json --project-root . --output build/ai-selection.json
```

`edit` reads the edit document supplied through `--edits`. `export` and `import` convert between named and legacy structured formats while preserving groups and field widths.

Set `format` to `g5510-ai-candidate-first-gate-edits-v1`. In `edits`, give each entry `row_id`, `candidate_index`, `expected_gate_byte`, and `gate_byte`.
