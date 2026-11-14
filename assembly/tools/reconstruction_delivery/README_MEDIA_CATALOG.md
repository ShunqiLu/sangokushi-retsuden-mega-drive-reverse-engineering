# 生成素材索引

**简体中文** · [繁體中文](README_MEDIA_CATALOG.zh-TW.md) · [日本語](README_MEDIA_CATALOG.ja.md) · [English](README_MEDIA_CATALOG.en.md)

素材目录工具从本地素材清单收集资源名、文件路径、像素尺寸、编码方式和原字段位置。结果包括机器可读的 `ASSET_INDEX.json` 和可浏览的 `ASSETS.md`。

`$resources` 是同时包含 `resources/` 和 `assets/` 的本地素材根。命令从汇编版根目录运行。

```powershell
$resources = Read-Host '本地素材根目录'
python -B -m tools.reconstruction_delivery.media_catalog --manifest "$resources/asset-source-manifest.json" --output ./asset-catalog
```

选择新输出目录。索引中的媒体路径相对于素材包。
