# 生成素材编辑索引

**简体中文** · [繁體中文](README_MEDIA_CATALOG.zh-TW.md) · [日本語](README_MEDIA_CATALOG.ja.md) · [English](README_MEDIA_CATALOG.en.md)

[`catalog_from_manifest(manifest)`](media_catalog.py) 接受 `g5510-build-connected-media-publication-v1` 资源清单，返回 JSON 索引对象与 Markdown 指南。索引按资源和文件组织，保留外置成员的编解码器、尺寸、位顺序、资源角色及字段路径。

```powershell
python -B -m tools.reconstruction_delivery.media_catalog --manifest "$resources/asset-source-manifest.json" --output ./media-catalog
```

输出为新目录中的 `ASSET_INDEX.json` 和 `ASSETS.md`。索引中的路径相对输入清单所在的素材根。总容量由索引与说明各自的输出限额约束；[素材编辑](../../ASSETS.md)使用索引定位源成员。
