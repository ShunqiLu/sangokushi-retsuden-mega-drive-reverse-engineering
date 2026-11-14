# AI 候補の適格条件

[简体中文](README_AI_SELECTION_SOURCES.md) · [繁體中文](README_AI_SELECTION_SOURCES.zh-TW.md) · **日本語** · [English](README_AI_SELECTION_SOURCES.en.md)

`resources/data/ai_selection_fields.json` は最初の候補判定で使う 14 × 14 個の 8 ビット値を定義します。名前付きビューは各項目のグループ、位置、元のバイト値を保持します。

`$resources` は `resources/` と `assets/` を含むローカル素材ルートです。コマンドはアセンブリ版のルートで実行します。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.ai_selection_sources edit --source "$resources/resources/data/ai_selection_fields.json" --edits ./ai-selection-edits.json --project-root . --output build/ai-selection.json
```

`edit` は `--edits` で指定された編集ファイルを読みます。`export` と `import` は名前付き形式と従来の構造化形式を相互変換し、グループとバイト幅を維持します。

編集ファイルの `format` は `g5510-ai-candidate-first-gate-edits-v1` です。`edits` の各要素に `row_id`、`candidate_index`、`expected_gate_byte`、`gate_byte` を指定します。
