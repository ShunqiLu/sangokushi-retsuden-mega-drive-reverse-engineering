# 逆向工具

**简体中文** · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [English](README.en.md)

这里提供 Mega Drive 游戏《三國志列傳 亂世群英》的 ROM 转换、反汇编、存档和资源工具。输入使用自己的卡带镜像、存档或跟踪记录。命令从本目录运行，示例使用 `input/` 和 `out/`。

Python 3.10 或更新版本即可运行基础工具。68000 反汇编使用 Capstone；原始瓦片预览使用 Pillow。

```sh
python -m pip install "capstone>=5" Pillow
```

| 用途 | 入口 |
| --- | --- |
| SMD 与线性 BIN 转换、卡带信息 | [rom_tool.py](rom_tool.py) |
| 68000 反汇编、引用和间接跳转 | [code_analysis](tools/code_analysis/) |
| Z80 载荷与驱动 | [audio_analysis](tools/audio_analysis/) |
| MAME 跟踪汇总与内存采集 | [runtime_trace](tools/runtime_trace/)、[采集脚本](tools/asset_analysis/mame_capture_memory.lua) |
| SRAM 格式和存档布局 | [save_data](tools/save_data/) |
| 图形、音频和剧本资源 | [资源参考](docs/resources.md) |

```sh
python rom_tool.py unpack input/cartridge.smd out/cartridge.bin out/copier-header.dat
python rom_tool.py info out/cartridge.bin
python tools/code_analysis/disasm_range.py out/cartridge.bin 0x11BC6:0x11C72
python tools/save_data/save_format.py inspect input/campaign.srm
```

[镜像与反汇编](docs/cartridge-and-code.md)收录 ROM、68000、Z80 和跟踪命令。[资源与存档](docs/resources.md)收录导入导出方式和数据格式。各入口通过 `--help` 列出参数。
