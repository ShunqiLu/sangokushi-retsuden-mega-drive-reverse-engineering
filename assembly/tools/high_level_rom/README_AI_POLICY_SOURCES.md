# AI 命令阈值

`resources/data/ai_threshold_pair_fields.json` 保存 48 对 16 位阈值。具名视图按命令分组，暴露每对阈值；与防御判断共用的第一项仍来自同一字段。

`$resources` 是同时包含 `resources/` 和 `assets/` 的本地素材根。命令从汇编版根目录运行。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.ai_policy_sources edit --source "$resources/resources/data/ai_threshold_pair_fields.json" --edits ./ai-policy-edits.json --project-root . --output build/ai-policy.json
```

`edit` 应用带原值的成对编辑。`export` 将旧版结构化文档转为具名视图，`import` 转回旧版格式。输出请选择 `build/` 下新的 JSON。

编辑文档的 `format` 为 `g5510-ai-command-cutoff-pair-edits-v1`。在 `edits` 数组中填写 `table`、`pair_index`、`field`、`expected_word`、`word`；`primary` 表额外填写 `group_index`。字段可选 `first_cutoff_word` 或 `second_cutoff_word`。
