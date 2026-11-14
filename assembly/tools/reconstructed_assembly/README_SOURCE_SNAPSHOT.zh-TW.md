# 彙編原始碼快照

[简体中文](README_SOURCE_SNAPSHOT.md) · **繁體中文** · [日本語](README_SOURCE_SNAPSHOT.ja.md) · [English](README_SOURCE_SNAPSHOT.en.md)

`stage_sources.snapshot_assembly_tree(project_root, resource_snapshot=...)` 返回彙編原始碼、佈局、資源編碼器和明確傳入的資原始檔集合。呼叫方負責儲存返回的後設資料及位元組對映。

從彙編版根目錄檢查原始碼清單與本地素材結構：

```powershell
$resources = Read-Host '本地素材根目录'
python -B -X utf8 -m tools.reconstructed_assembly.stage_sources --project-root . --resource-root $resources
```

使用場景清單時，改為 `--source-manifest`。可配合 `--asset-metadata-manifest` 提供素材目錄索引。
