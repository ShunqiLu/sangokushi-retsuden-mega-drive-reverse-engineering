# AI 命令のしきい値

[简体中文](README_AI_POLICY_SOURCES.md) · [繁體中文](README_AI_POLICY_SOURCES.zh-TW.md) · **日本語** · [English](README_AI_POLICY_SOURCES.en.md)

`resources/data/ai_threshold_pair_fields.json` には 16 ビットのしきい値が 48 組あります。名前付きビューでは命令別に各組を確認できます。防御判定と共有する最初の値は、引き続き同じフィールドを参照します。

`$resources` は `resources/` と `assets/` を含むローカル素材ルートです。コマンドはアセンブリ版のルートで実行します。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.ai_policy_sources edit --source "$resources/resources/data/ai_threshold_pair_fields.json" --edits ./ai-policy-edits.json --project-root . --output build/ai-policy.json
```

`edit` は元の値を指定したペア編集を適用します。`export` は従来の構造化形式を名前付きビューに、`import` は従来の形式に変換します。`build/` の下に新規の JSON を指定します。

編集ファイルの `format` は `g5510-ai-command-cutoff-pair-edits-v1` です。`edits` の各要素に `table`、`pair_index`、`field`、`expected_word`、`word` を指定し、`primary` テーブルでは `group_index` も指定します。フィールドは `first_cutoff_word` または `second_cutoff_word` です。
