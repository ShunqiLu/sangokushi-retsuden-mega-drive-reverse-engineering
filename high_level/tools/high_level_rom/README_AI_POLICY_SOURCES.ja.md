# AI 命令のしきい値

[简体中文](README_AI_POLICY_SOURCES.md) · [繁體中文](README_AI_POLICY_SOURCES.zh-TW.md) · **日本語** · [English](README_AI_POLICY_SOURCES.en.md)

`ai_threshold_pair_fields` は主テーブルの 15 組 × 3 グループと、副テーブルの 3 組で、符号なし WORD の組を計 48 組持ちます。各組は `first_cutoff_word` と `second_cutoff_word` を使います。主テーブルの先頭 WORD は城防目標の計画にも使われるため、編集は両方の呼び出しに影響します。

ルールは両テーブルを元の順序で読み、符号なし比較で分岐します。グループ番号と組番号は物理位置です。同値、逆順、0～65535 の全範囲を有効な値として扱います。

## コマンド

次の書き出しでは型付きソースを含む素材ルート `$typedResources` を使います。既存の名前付きソースは `edit --source` に直接渡せます。既存の `build/` の下に新規ファイルを指定します。

```powershell
python -B -m tools.high_level_rom.ai_policy_sources export --source "$typedResources/resources/data/ai_threshold_pair_fields.json" --project-root . --output build/ai-cutoffs.named.json
python -B -m tools.high_level_rom.ai_policy_sources edit --source build/ai-cutoffs.named.json --edits cutoff-edits.json --project-root . --output build/ai-cutoffs.edited.json
python -B -m tools.high_level_rom.ai_policy_sources import --source build/ai-cutoffs.edited.json --project-root . --output build/ai-cutoffs.typed.json
```

名前付き形式は `g5510-named-ai-command-cutoffs-v1` です。編集ファイルは `g5510-ai-command-cutoff-pair-edits-v1` 形式で `format` と `edits` を含みます。各項目には `table`、`pair_index`、`field`、`expected_word`、`word` が必要です。主テーブルでは `group_index`（0～2）も指定します。組番号は主が 0～14、副が 0～2 です。現在の完全なソースと照合し、新規 JSON に出力します。

Python の `to_named` と `from_named` はデータ表現を変換し、`with_cutoff_pairs(source, edits)` は独立した編集結果を返します。名前付き形式、元の構造、重ね合わせ登録の使い方は[素材マニフェスト](README_SCENE_SOURCE_PUBLICATION.ja.md)を参照してください。
