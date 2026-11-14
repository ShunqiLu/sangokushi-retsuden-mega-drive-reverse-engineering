# 准备本地运行目录

[`stage_sources.py`](stage_sources.py) 读取显式源码目录及登记资源，生成独立运行目录中的源码、配置模板、素材和 Scene 清单。输入为完整本地素材根，或完整的多根 Scene 清单及素材元数据清单。

```powershell
python -B -X utf8 -m tools.high_level_rom.stage_sources stage --project-root . --resource-root $resources --output ../local-game
```

多根形式使用 `--source-manifest` 与 `--asset-metadata-manifest`，完整清单中的每个资源 ID 使用唯一来源。`plan` 输出源码依赖计划；`stage` 写入工程和素材根之外的新目录。路径和值由显式资源登记及本版静态、动态源码声明解析。

[素材根与别名](README_SCENE_SOURCE_PUBLICATION.md)说明多根清单的边界。[桌面配置](../reconstructed_game/README_LOCAL_CONFIG.md)说明镜像构建、芯片库、设备输入和存档。
