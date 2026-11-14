# Resource editing index

[简体中文](README_MEDIA_CATALOG.md) · [繁體中文](README_MEDIA_CATALOG.zh-TW.md) · [日本語](README_MEDIA_CATALOG.ja.md) · **English**

[`catalog_from_manifest(manifest)`](media_catalog.py) accepts a `g5510-build-connected-media-publication-v1` resource manifest and returns a JSON index and a Markdown guide. The index groups entries by resource and file, preserving external members' codecs, dimensions, bit order, roles, and field paths.

```powershell
python -B -m tools.reconstruction_delivery.media_catalog --manifest "$resources/asset-source-manifest.json" --output ./media-catalog
```

The new output directory contains `ASSET_INDEX.json` and `ASSETS.md`. Paths in the index are relative to the resource root containing the input manifest. The index and guide each have an output size limit. Use the [resource editing guide](../../ASSETS.en.md) to locate source files through the index.
