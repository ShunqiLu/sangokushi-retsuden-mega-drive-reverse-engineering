# 編輯劇本初值

[简体中文](README_NAMED_SCENARIO_SOURCES.md) · **繁體中文** · [日本語](README_NAMED_SCENARIO_SOURCES.ja.md) · [English](README_NAMED_SCENARIO_SOURCES.en.md)

`resources/data/scenario_build.json` 儲存三套劇本的城市、勢力、武將及初始裝備。具名檢視提供資金、糧食、兵力、能力、歸屬和座標等欄位，地址鍵保留其原有範圍和寬度。當前進度見[存檔編輯](../save_data/README.zh-TW.md)。

`$resources` 是同時包含 `resources/` 和 `assets/` 的本地素材根。命令從彙編版根目錄執行。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.scenario_sources edit --source "$resources/resources/data/scenario_build.json" --edits ./scenario-edits.json --project-root . --output build/scenario.json
```

`edit` 接受具名劇本文件。裝備的三個原始位元組可用 `edit-equipment --edits` 按欄位序號處理。`export` 將舊版結構化文件轉為具名檢視，`import` 轉回舊版格式。每次使用新的輸出檔案核對結果，再放入本地素材副本。

`edit` 的輸入為陣列，每項填寫 `scenario_id`、`group`、`record_id`、`field`、`expected_value` 和 `value`。城市資源的高低字結構保留原高字，編輯寫入低字值。
