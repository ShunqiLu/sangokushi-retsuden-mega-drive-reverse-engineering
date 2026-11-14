# 生成素材編輯索引

[简体中文](README_MEDIA_CATALOG.md) · **繁體中文** · [日本語](README_MEDIA_CATALOG.ja.md) · [English](README_MEDIA_CATALOG.en.md)

[`catalog_from_manifest(manifest)`](media_catalog.py) 接受 `g5510-build-connected-media-publication-v1` 資源清單，返回 JSON 索引物件與 Markdown 指南。索引按資源和檔案組織，保留外接成員的編解碼器、尺寸、位順序、資源角色及欄位路徑。

```powershell
python -B -m tools.reconstruction_delivery.media_catalog --manifest "$resources/asset-source-manifest.json" --output ./media-catalog
```

輸出為新目錄中的 `ASSET_INDEX.json` 和 `ASSETS.md`。索引中的路徑相對輸入清單所在的素材根。總容量由索引與說明各自的輸出限額約束；[素材編輯](../../ASSETS.zh-TW.md)使用索引定位源成員。
