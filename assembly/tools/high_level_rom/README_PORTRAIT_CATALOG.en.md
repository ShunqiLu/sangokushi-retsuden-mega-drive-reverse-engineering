# Officer portrait index

[简体中文](README_PORTRAIT_CATALOG.md) · [繁體中文](README_PORTRAIT_CATALOG.zh-TW.md) · [日本語](README_PORTRAIT_CATALOG.ja.md) · **English**

This tool links officer names, scenario records, and portrait selections. Each entry includes a record ID and references to the layout, shared tiles, and palette. Follow the index to the actual files in the local resource pack.

`$resources` is the local resource root containing `resources/` and `assets/`. Run from the assembly root.

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.portrait_catalog --names-source "$resources/resources/data/dialogue_text.json" --portrait-source "$resources/resources/images/portrait_graphics.json" --record-authority "$resources/resources/data/scenario_build.json" --source-root $resources --project-root . --output build/portraits.json
```
