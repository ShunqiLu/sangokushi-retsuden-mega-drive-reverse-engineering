# 汇编源码快照

`stage_sources.snapshot_assembly_tree(project_root, resource_snapshot=...)` 返回汇编源码、布局、资源编码器和明确传入的资源文件集合。调用方负责保存返回的元数据及字节映射。

从汇编版根目录检查源码清单与本地素材结构：

```powershell
$resources = Read-Host '本地素材根目录'
python -B -X utf8 -m tools.reconstructed_assembly.stage_sources --project-root . --resource-root $resources
```

使用场景清单时，改为 `--source-manifest`。可配合 `--asset-metadata-manifest` 提供素材目录索引。
