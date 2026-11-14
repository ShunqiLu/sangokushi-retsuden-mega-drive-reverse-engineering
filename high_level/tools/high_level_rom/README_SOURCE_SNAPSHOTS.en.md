# Source and resource snapshots

[简体中文](README_SOURCE_SNAPSHOTS.md) · [繁體中文](README_SOURCE_SNAPSHOTS.zh-TW.md) · [日本語](README_SOURCE_SNAPSHOTS.ja.md) · **English**

[`stage_sources.py`](stage_sources.py) provides two interfaces for organizing build inputs in memory:

- `snapshot_resources(resource_root, resource_registration, ...)` reads metadata and file content from the registry, indexes the byte snapshots by relative path, and supports multi-root manifests.
- `snapshot_source_tree(project_root, resource_snapshot=...)` prepares this edition's source dependencies and merges the resource snapshot supplied by the caller.

The resource registry uses fixed IDs, codecs, source paths, roles, and build paths. Mapped paths are relative to the destination root and include resource files and any required Scene manifest. Counts for source and resource files are separate. Multiple source targets can reuse a snapshot. Use the [`stage_sources` command](README_GAME_SOURCE_STAGE.en.md) to create the directory.
