# Assembly source snapshot

[简体中文](README_SOURCE_SNAPSHOT.md) · [繁體中文](README_SOURCE_SNAPSHOT.zh-TW.md) · [日本語](README_SOURCE_SNAPSHOT.ja.md) · **English**

`stage_sources.snapshot_assembly_tree(project_root, resource_snapshot=...)` returns the assembly, layout, resource encoders, and explicitly supplied resource files. The caller saves the returned metadata and byte mappings.

Run from the assembly root to check the source inventory and local resource layout:

```powershell
$resources = Read-Host '本地素材根目录'
python -B -X utf8 -m tools.reconstructed_assembly.stage_sources --project-root . --resource-root $resources
```

For a scene manifest, use `--source-manifest` instead. Supply a resource directory index with `--asset-metadata-manifest` if needed.
