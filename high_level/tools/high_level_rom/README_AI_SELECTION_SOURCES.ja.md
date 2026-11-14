# AI 候補の適格条件表

[简体中文](README_AI_SELECTION_SOURCES.md) · [繁體中文](README_AI_SELECTION_SOURCES.zh-TW.md) · **日本語** · [English](README_AI_SELECTION_SOURCES.en.md)

`ai_selection_fields` には候補 BYTE が 14 行 × 14 項目あります。選抜は `first_gate_byte` を読み、0 と 1 が最初の条件を通過します。その後は関係ビット、勢力の代表項目、都市数で判定します。0 と 1 は区別し、2～255 も元の BYTE 値を保ちます。物理行は元のレコード ID で識別します。

名前付き素材は `edit` に直接渡せます。以下の例では、型付きソースのある素材ルート `$typedResources` から書き出します。既存の `build/` に新規ファイルを作成します。

```powershell
python -B -m tools.high_level_rom.ai_selection_sources export --source "$typedResources/resources/data/ai_selection_fields.json" --project-root . --output build/ai-selection.named.json
python -B -m tools.high_level_rom.ai_selection_sources edit --source build/ai-selection.named.json --edits candidate-edits.json --project-root . --output build/ai-selection.edited.json
```

編集形式は `g5510-ai-candidate-first-gate-edits-v1` で、`format` と `edits` を含みます。各編集は `row_id`、`candidate_index`（0～13）、`expected_gate_byte`、`gate_byte` を指定し、ソースの現在のレコードと値に照合します。

`to_named` は `g5510-named-ai-candidate-first-gates-v1` を生成し、`from_named` は元のフィールド表現に戻します。`with_candidate_gates(source, edits)` は対象が重複しない編集を一括で適用し、行、位置、付加メタデータを維持します。通常のエンコーダーは対応する登録素材を使います。
