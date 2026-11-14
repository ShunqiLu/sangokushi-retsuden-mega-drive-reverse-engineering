# 生成素材索引

[简体中文](README_MEDIA_CATALOG.md) · **繁體中文** · [日本語](README_MEDIA_CATALOG.ja.md) · [English](README_MEDIA_CATALOG.en.md)

素材目錄工具從本地素材清單收集資源名、檔案路徑、畫素尺寸、編碼方式和原欄位位置。結果包括機器可讀的 `ASSET_INDEX.json` 和可瀏覽的 `ASSETS.md`。

`$resources` 是同時包含 `resources/` 和 `assets/` 的本地素材根。命令從彙編版根目錄執行。

```powershell
$resources = Read-Host '本地素材根目录'
python -B -m tools.reconstruction_delivery.media_catalog --manifest "$resources/asset-source-manifest.json" --output ./asset-catalog
```

選擇新輸出目錄。索引中的媒體路徑相對於素材包。
