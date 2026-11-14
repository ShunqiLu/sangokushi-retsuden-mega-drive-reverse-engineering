# 素材索引

[简体中文](README_MEDIA_CATALOG.md) · [繁體中文](README_MEDIA_CATALOG.zh-TW.md) · **日本語** · [English](README_MEDIA_CATALOG.en.md)

ツールはローカルのマニフェストから、素材名、パス、ピクセル寸法、エンコード形式、元のフィールド位置を取得します。機械可読の `ASSET_INDEX.json` と閲覧用の `ASSETS.md` を生成します。

`$resources` は `resources/` と `assets/` を含むローカル素材ルートです。アセンブリ版のルートで実行します。

```powershell
$resources = Read-Host '本地素材根目录'
python -B -m tools.reconstruction_delivery.media_catalog --manifest "$resources/asset-source-manifest.json" --output ./asset-catalog
```

新しい出力先を指定します。索引内のメディアパスは素材パックからの相対パスです。
