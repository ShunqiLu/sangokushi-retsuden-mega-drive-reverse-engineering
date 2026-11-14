# 《三國志列傳 亂世群英》汇编源码

**简体中文** · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [English](README.en.md)

汇编版以 GNU 68000 和 Z80 助记符描述程序，通过地址布局和资源编码器生成 Mega Drive 卡带镜像。构建使用本地的兼容素材包，其中并列放置 `resources/` 和 `assets/`。

## 构建

在 Windows 的本地磁盘上使用 Python 3.12 或更新版本、Pillow 和支持 M68K 的 Capstone 5。WSL 调用两套 GNU 工具：68000 使用 `m68k-elf-as`、`m68k-elf-ld`、`m68k-elf-objcopy`；Z80 使用 `z80-unknown-coff-as` 和 `z80-unknown-coff-objcopy`。

在本目录执行：

```powershell
python -m pip install Pillow "capstone>=5,<6"
$m68k = Read-Host '68000 工具目录'
$z80 = Read-Host 'Z80 COFF 工具目录'
$resources = Read-Host '本地素材根目录'
python -B -X utf8 -m tools.reconstructed_assembly --source-root . --layout-root tools/reconstructed_assembly/layout --resource-root $resources --m68k-tools $m68k --z80-tools $z80 --output build/cartridge --copier-header-fields tools/high_level_rom/resource_sources/copier_header.json --workers 2
```

`build/cartridge/` 接收 `SANGO.bin`、`SANGO.smd` 和构建结果。每次构建请选择一个新的输出目录。`--copier-header-fields` 启用 SMD 文件头和交错打包；基本输出为 BIN。完整参数见[构建参数](tools/reconstructed_assembly/README.md)。

## 编辑

- 程序入口在 `src/m68k/` 和 `src/z80/`；地址、指令宽度和资源登记见 `tools/reconstructed_assembly/layout/`。
- 图像、音效、剧本和对话的源文件见[编辑说明](EDITING.md)及[素材路径指南](ASSETS.md)。
- [原版行为](docs/ORIGINAL_GAME_BUGS.md)说明程序保留的特殊规则。
