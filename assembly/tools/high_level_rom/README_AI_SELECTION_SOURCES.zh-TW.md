# AI 候選資格

[简体中文](README_AI_SELECTION_SOURCES.md) · **繁體中文** · [日本語](README_AI_SELECTION_SOURCES.ja.md) · [English](README_AI_SELECTION_SOURCES.en.md)

`resources/data/ai_selection_fields.json` 提供 14×14 個 8 位引數，供決策的首道候選條件使用。具名檢視分別儲存分組、位置和原位元組值。

`$resources` 是同時包含 `resources/` 和 `assets/` 的本地素材根。命令從彙編版根目錄執行。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.ai_selection_sources edit --source "$resources/resources/data/ai_selection_fields.json" --edits ./ai-selection-edits.json --project-root . --output build/ai-selection.json
```

`edit` 接受 `--edits` 指向的編輯文件。`export` 和 `import` 雙向轉換具名與舊版結構化格式，並保留原分組和位元組寬度。

編輯文件的 `format` 為 `g5510-ai-candidate-first-gate-edits-v1`。在 `edits` 陣列中填寫 `row_id`、`candidate_index`、`expected_gate_byte` 和 `gate_byte`。
