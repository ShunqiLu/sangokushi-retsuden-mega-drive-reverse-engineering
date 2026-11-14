# アセンブリソースのスナップショット

[简体中文](README_SOURCE_SNAPSHOT.md) · [繁體中文](README_SOURCE_SNAPSHOT.zh-TW.md) · **日本語** · [English](README_SOURCE_SNAPSHOT.en.md)

`stage_sources.snapshot_assembly_tree(project_root, resource_snapshot=...)` はアセンブリ、配置、素材エンコーダー、明示的に指定した素材ファイルを返します。呼び出し側で、返されたメタデータとバイトの対応表を保存します。

ソース一覧とローカル素材の構成を確認するには、アセンブリ版のルートで実行します。

```powershell
$resources = Read-Host '本地素材根目录'
python -B -X utf8 -m tools.reconstructed_assembly.stage_sources --project-root . --resource-root $resources
```

シーンマニフェストを使う場合は `--source-manifest` に切り替えます。必要に応じて `--asset-metadata-manifest` で素材ディレクトリの索引を指定できます。
