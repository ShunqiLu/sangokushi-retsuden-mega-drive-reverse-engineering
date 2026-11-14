# 武将の顔グラフィック索引

[简体中文](README_PORTRAIT_CATALOG.md) · [繁體中文](README_PORTRAIT_CATALOG.zh-TW.md) · **日本語** · [English](README_PORTRAIT_CATALOG.en.md)

このツールは武将名、シナリオレコード、顔グラフィック選択を結び付けます。各項目にレコード ID と、配置・共有タイル・パレットへの参照が入ります。編集する実ファイルは索引からたどれます。

`$resources` は `resources/` と `assets/` を含むローカル素材ルートです。アセンブリ版のルートで実行します。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.portrait_catalog --names-source "$resources/resources/data/dialogue_text.json" --portrait-source "$resources/resources/images/portrait_graphics.json" --record-authority "$resources/resources/data/scenario_build.json" --source-root $resources --project-root . --output build/portraits.json
```
