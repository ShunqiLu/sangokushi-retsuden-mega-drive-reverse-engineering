# Python 构建器

从 [Python 版首页](../../README.md) 配置运行环境。在源码根调用 `tools.high_level_rom.build`，以兼容素材根、工具目录及新输出路径作为显式输入。

| 参数 | 用途 |
| --- | --- |
| `build` | 编译领域规则与音频驱动，编码素材，组装卡带镜像。 |
| `plan` | 调用源码编译器，生成构建计划。 |
| `--project-root` | Python 源码根，默认取本项目根。 |
| `--resource-root` | 兼容素材根，包含 `resources/` 和 `assets/`。 |
| `--m68k-tools`、`--z80-tools` | Windows 本地 GNU 工具目录，由 WSL 调用。 |
| `--output` | 项目 `build/` 内专用的新输出目录。 |
| `--workers` | 构建工作数，默认 2。 |
| `--copier-header-fields` | 从结构化头字段同时构建 SMD。 |
| `--copier-header` | 使用调用者提供的容器头；与头字段选项二选一。 |

```powershell
python -B -X utf8 -m tools.high_level_rom.build build --project-root . --resource-root $resources --m68k-tools $m68k --z80-tools $z80 --output build/python-image --copier-header-fields tools/high_level_rom/resource_sources/copier_header.json
```

构建以明确的代码与资源分区生成 `SANGO.bin`。指定 SMD 头后，构建器另写 `SANGO.smd`。分区检查要求图像中的位置全部有来源；源码准备失败时，输出目录提供构建诊断。卡带校验字段由登记源提供，游戏逻辑按原格式使用它。

业务规则、编译器和物理目标分属领域模块。编辑接口见[规则与素材指南](../../EDITING.md)，桌面配置见[运行说明](../reconstructed_game/README_LOCAL_CONFIG.md)。
