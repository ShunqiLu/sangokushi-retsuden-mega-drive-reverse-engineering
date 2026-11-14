# 编辑对话和姓名

`resources/data/dialogue_text.json` 记录对话、武将名和城名。具名格式保留终止控制字、原字数和无法用普通字符区分时的精确转义。编辑应使用同样的记录 ID 及字数上限。

`$resources` 是同时包含 `resources/` 和 `assets/` 的本地素材根。命令从汇编版根目录运行。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.readable_text edit --source "$resources/resources/data/dialogue_text.json" --edits ./text-edits.json --project-root . --output build/readable-text.json
```

`edit --edits` 以具名素材中的记录 ID 和原值核对每项修改。`import` 可将具名格式转回字码格式。具备旧版字码格式和两份人工字形表时，可用 `export --glyph-sources` 转成具名视图。

编辑文档的 `format` 为 `g5510-main-text-record-edits-v1`。在 `edits` 数组中，每项填写 `collection`、`id`、`expected_text` 和 `text`；集合名称为 `records`、`officer_names` 或 `city_names`。
