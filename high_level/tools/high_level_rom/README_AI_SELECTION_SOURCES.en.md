# AI candidate eligibility table

[简体中文](README_AI_SELECTION_SOURCES.md) · [繁體中文](README_AI_SELECTION_SOURCES.zh-TW.md) · [日本語](README_AI_SELECTION_SOURCES.ja.md) · **English**

`ai_selection_fields` has 14 rows of 14 candidate BYTEs. Selection reads `first_gate_byte`. Values 0 and 1 pass this gate; relation bits, faction representative records, and city counts decide the next checks. Values 0 and 1 remain distinct, and 2–255 retain their byte values. Physical rows use original record IDs.

Pass a named source directly to `edit`, or export it from typed files in resource root `$typedResources` as shown below. Write to a new file in the existing `build/` directory.

```powershell
python -B -m tools.high_level_rom.ai_selection_sources export --source "$typedResources/resources/data/ai_selection_fields.json" --project-root . --output build/ai-selection.named.json
python -B -m tools.high_level_rom.ai_selection_sources edit --source build/ai-selection.named.json --edits candidate-edits.json --project-root . --output build/ai-selection.edited.json
```

The edit format is `g5510-ai-candidate-first-gate-edits-v1` with `format` and `edits`. An edit specifies `row_id`, `candidate_index` (0–13), `expected_gate_byte`, and `gate_byte`, checked against the current source record and value.

`to_named` produces `g5510-named-ai-candidate-first-gates-v1`. `from_named` restores the original field form. `with_candidate_gates(source, edits)` applies the batch of unique targets while preserving rows, positions, and metadata. The standard encoder uses the matching registered resource.
