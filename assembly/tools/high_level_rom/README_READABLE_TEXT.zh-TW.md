# 編輯對話和姓名

[简体中文](README_READABLE_TEXT.md) · **繁體中文** · [日本語](README_READABLE_TEXT.ja.md) · [English](README_READABLE_TEXT.en.md)

`resources/data/dialogue_text.json` 記錄對話、武將名和城名。具名格式保留終止控制字、原字數和無法用普通字元區分時的精確轉義。編輯應使用同樣的記錄 ID 及字數上限。

`$resources` 是同時包含 `resources/` 和 `assets/` 的本地素材根。命令從彙編版根目錄執行。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.readable_text edit --source "$resources/resources/data/dialogue_text.json" --edits ./text-edits.json --project-root . --output build/readable-text.json
```

`edit --edits` 以具名素材中的記錄 ID 和原值核對每項修改。`import` 可將具名格式轉回字碼格式。具備舊版字碼格式和兩份人工字形表時，可用 `export --glyph-sources` 轉成具名檢視。

編輯文件的 `format` 為 `g5510-main-text-record-edits-v1`。在 `edits` 陣列中，每項填寫 `collection`、`id`、`expected_text` 和 `text`；集合名稱為 `records`、`officer_names` 或 `city_names`。
