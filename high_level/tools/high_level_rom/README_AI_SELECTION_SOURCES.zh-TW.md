# AI 候選資格表

[简体中文](README_AI_SELECTION_SOURCES.md) · **繁體中文** · [日本語](README_AI_SELECTION_SOURCES.ja.md) · [English](README_AI_SELECTION_SOURCES.en.md)

`ai_selection_fields` 有 14 行、每行 14 個候選 BYTE。選拔業務讀取 `first_gate_byte`，值 0 和 1 透過這道門檻；隨後由關係位、勢力代表項和城市數繼續決定。0 與 1 保持為不同原值，2–255 保持各自的 BYTE 值。物理行以原記錄 ID 標識。

具名素材可直接提供給 `edit`；下列匯出從含 typed 源的素材根 `$typedResources` 生成具名文件。輸出寫入已有 `build/` 下的新檔案。

```powershell
python -B -m tools.high_level_rom.ai_selection_sources export --source "$typedResources/resources/data/ai_selection_fields.json" --project-root . --output build/ai-selection.named.json
python -B -m tools.high_level_rom.ai_selection_sources edit --source build/ai-selection.named.json --edits candidate-edits.json --project-root . --output build/ai-selection.edited.json
```

編輯檔案格式為 `g5510-ai-candidate-first-gate-edits-v1`，包含 `format` 與 `edits`。一個編輯項使用 `row_id`、`candidate_index`（0–13）、`expected_gate_byte` 及 `gate_byte`，並對照源中的當前記錄和值。

`to_named` 生成 `g5510-named-ai-candidate-first-gates-v1`；`from_named` 恢復原欄位表示。`with_candidate_gates(source, edits)` 應用整批唯一目標，保留各行、位置和附加後設資料。正常編碼器使用對應的登記資源。
