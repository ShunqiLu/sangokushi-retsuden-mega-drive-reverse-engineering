# 素材編集の索引

[简体中文](README_MEDIA_CATALOG.md) · [繁體中文](README_MEDIA_CATALOG.zh-TW.md) · **日本語** · [English](README_MEDIA_CATALOG.en.md)

[`catalog_from_manifest(manifest)`](media_catalog.py) は `g5510-build-connected-media-publication-v1` 形式の素材マニフェストから、JSON 索引と Markdown ガイドを作成します。索引は素材とファイルで整理し、外部要素のコーデック、寸法、ビット順、役割、フィールドのパスを保持します。

```powershell
python -B -m tools.reconstruction_delivery.media_catalog --manifest "$resources/asset-source-manifest.json" --output ./media-catalog
```

新しい出力先には `ASSET_INDEX.json` と `ASSETS.md` が入ります。索引のパスは入力マニフェストがある素材ルートからの相対パスです。索引とガイドにはそれぞれ出力上限があります。[素材編集ガイド](../../ASSETS.ja.md)では索引から元ファイルを探せます。
