# 生成武將頭像索引

[简体中文](README_PORTRAIT_CATALOG.md) · **繁體中文** · [日本語](README_PORTRAIT_CATALOG.ja.md) · [English](README_PORTRAIT_CATALOG.en.md)

工具將武將姓名、劇本記錄及頭像選擇資料連線為索引。每項給出記錄 ID、佈局、共享圖塊和調色盤引用。編輯時沿索引找到本地素材中的實際檔案。

`$resources` 是同時包含 `resources/` 和 `assets/` 的本地素材根。命令從彙編版根目錄執行。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.portrait_catalog --names-source "$resources/resources/data/dialogue_text.json" --portrait-source "$resources/resources/images/portrait_graphics.json" --record-authority "$resources/resources/data/scenario_build.json" --source-root $resources --project-root . --output build/portraits.json
```
