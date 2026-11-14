# AI 命令閾值

[简体中文](README_AI_POLICY_SOURCES.md) · **繁體中文** · [日本語](README_AI_POLICY_SOURCES.ja.md) · [English](README_AI_POLICY_SOURCES.en.md)

`resources/data/ai_threshold_pair_fields.json` 儲存 48 對 16 位閾值。具名檢視按命令分組，暴露每對閾值；與防禦判斷共用的第一項仍來自同一欄位。

`$resources` 是同時包含 `resources/` 和 `assets/` 的本地素材根。命令從彙編版根目錄執行。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.ai_policy_sources edit --source "$resources/resources/data/ai_threshold_pair_fields.json" --edits ./ai-policy-edits.json --project-root . --output build/ai-policy.json
```

`edit` 應用帶原值的成對編輯。`export` 將舊版結構化文件轉為具名檢視，`import` 轉回舊版格式。輸出請選擇 `build/` 下新的 JSON。

編輯文件的 `format` 為 `g5510-ai-command-cutoff-pair-edits-v1`。在 `edits` 陣列中填寫 `table`、`pair_index`、`field`、`expected_word`、`word`；`primary` 表額外填寫 `group_index`。欄位可選 `first_cutoff_word` 或 `second_cutoff_word`。
