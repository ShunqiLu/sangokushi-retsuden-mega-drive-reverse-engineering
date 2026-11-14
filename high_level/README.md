# 《三國志列傳 亂世群英》G-5510-00 · Python 版

**简体中文** · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [English](README.en.md)

游戏规则以 Python 源码呈现，按内政、行军、战斗、场景、AI 和音频分组。构建器将受支持的规则编译为 Mega Drive 的 68000 和 Z80 程序，并将兼容的本地素材编码为游戏卡带镜像。

## 从源码构建

构建环境使用 Windows、WSL、Python 3.12 或更新版本、Pillow 和支持 M68K 的 Capstone 5。两套 GNU 交叉工具放在 WSL 可访问的 Windows 目录：

- 68000：`m68k-elf-as`、`m68k-elf-ld`、`m68k-elf-objcopy`。
- Z80 COFF：`z80-unknown-coff-as`、`z80-unknown-coff-objcopy`。

从本目录运行下列 PowerShell 命令，提供两个工具目录和兼容素材根。素材根包含并列的 `assets/` 和 `resources/`。

```powershell
python -m pip install Pillow "capstone>=5,<6"
$m68k = Read-Host '68000 交叉工具目录'
$z80 = Read-Host 'Z80 COFF 交叉工具目录'
$resources = Read-Host '兼容素材根'
python -B -X utf8 -m tools.high_level_rom.build build --project-root . --resource-root $resources --m68k-tools $m68k --z80-tools $z80 --output build/python-image --copier-header-fields tools/high_level_rom/resource_sources/copier_header.json
```

构建结果写入新的 `build/python-image/`。默认生成 `SANGO.bin`；这里的 `--copier-header-fields` 同时启用 `SANGO.smd`。构建输入、参数和输出见[构建说明](tools/high_level_rom/README_BUILD.md)。

## 编辑游戏

- [编辑入口](EDITING.md)按规则、初始剧本、存档、图像和音频定位源文件。
- [素材指南](ASSETS.md)介绍索引 PNG、调色板、共享音频和本地素材结构。
- [原地址索引](PENDING_SOURCE_INDEX.md)将选定的卡带入口映射到 Python 函数。
- [原版兼容行为](docs/ORIGINAL_GAME_BUGS.md)列出复原时保留的行为和边界条件。

[桌面运行](tools/reconstructed_game/README_LOCAL_CONFIG.md)使用本地运行目录、由本版源码构建的 CPU 程序数据、[由外置 YMFM 源码构建的音频桥](tools/high_level_audio_engine/README_YMFM.md)和明确的设备与存档配置。控制台和 Tk 窗口共用同一个游戏应用。
