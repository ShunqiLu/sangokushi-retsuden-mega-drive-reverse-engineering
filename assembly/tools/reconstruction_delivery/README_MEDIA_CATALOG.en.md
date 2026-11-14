# Resource index

[简体中文](README_MEDIA_CATALOG.md) · [繁體中文](README_MEDIA_CATALOG.zh-TW.md) · [日本語](README_MEDIA_CATALOG.ja.md) · **English**

The tool collects resource names, paths, pixel dimensions, encoding formats, and original field positions from the local manifest. It creates a machine-readable `ASSET_INDEX.json` and a browsable `ASSETS.md`.

`$resources` is the local resource root containing `resources/` and `assets/`. Run from the assembly root.

```powershell
$resources = Read-Host '本地素材根目录'
python -B -m tools.reconstruction_delivery.media_catalog --manifest "$resources/asset-source-manifest.json" --output ./asset-catalog
```

Choose a fresh output directory. Media paths in the index are relative to the resource pack.
