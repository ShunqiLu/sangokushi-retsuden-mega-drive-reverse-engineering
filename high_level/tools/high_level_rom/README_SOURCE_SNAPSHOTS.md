# 源码与资源快照

[`stage_sources.py`](stage_sources.py) 提供两种在内存中组织构建输入的接口：

- `snapshot_resources(resource_root, resource_registration, ...)` 根据资源登记读取元数据和文件内容，使用相对路径索引每份字节快照，并支持多根清单。
- `snapshot_source_tree(project_root, resource_snapshot=...)` 准备本版源码依赖，并合并调用方提供的资源快照。

资源登记使用固定 ID、编解码器、源路径、角色及构建链。映射的路径相对目标根，包含素材成员以及需要的 Scene 清单。源码计数与素材计数分列。共享快照可供多个源码目标使用；目录创建由 [`stage_sources` 命令](README_GAME_SOURCE_STAGE.md)办理。
