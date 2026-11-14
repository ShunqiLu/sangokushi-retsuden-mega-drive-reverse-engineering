# 汇编构建参数

**简体中文** · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [English](README.en.md)

构建器按各组地址布局读取助记符，使用 GNU 交叉工具生成指令，再与资源编码器产生的数据合并。68000 和 Z80 的指令宽度分别由 ELF 符号和 COFF 边界核对。

| 参数 | 用途 |
| --- | --- |
| `--source-root` | `src/m68k/` 与 `src/z80/` 所在的本版根 |
| `--layout-root` | `tools/reconstructed_assembly/layout/`，含清单和 14 组指令范围 |
| `--resource-root` | 外部素材根，含 `resources/` 与 `assets/` |
| `--m68k-tools`、`--z80-tools` | Windows 本地磁盘上的两套 GNU 工具目录，由 WSL 执行 |
| `--output` | 位于本版 `build/` 下的新目录 |
| `--copier-header-fields` | 可选 SMD 文件头字段；项目模板在 `tools/high_level_rom/resource_sources/` |
| `--workers` | 并发任务数，取 1 到 4 |

生成结果为线性 BIN 和可选 SMD。完整地址区间由唯一源码或资源所有者提供；工具会提示缺项、重复区间或宽度变化。完整命令见[汇编版首页](../../README.md)。
