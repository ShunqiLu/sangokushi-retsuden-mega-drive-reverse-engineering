# 三国志列传：乱世群英 · Mega Drive 逆向工程

**简体中文** · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [English](README.en.md)

**Sangokushi Retsuden: Ransei no Eiyuutachi** · 繁体中文版卡带 `G-5510-00`

本项目提供汇编语言和高级语言重建代码。这是首个针对该版本、同时公开汇编和 Python 两套可构建源码的项目。

## 源码

- [汇编源码](assembly/README.md)：68000 主程序、Z80 音频驱动和卡带地址布局。参见[编辑指南](assembly/EDITING.md)。
- [Python 源码](high_level/README.md)：内政、武将、行军、战斗、AI 和音频等游戏规则及其编译器。参见[编辑指南](high_level/EDITING.md)和[原地址索引](high_level/PENDING_SOURCE_INDEX.md)。

## 工具

[逆向工具](reverse_tools/README.md)支持 BIN/SMD 互转、卡带头检查、68000/Z80 反汇编和 MAME 运行跟踪，也可解析图形、音频、剧本和 SRAM 存档。

## 构建

两套源码都能构建 Mega Drive 的 `SANGO.bin` 和 `SANGO.smd`。构建使用 Windows + WSL、Python 3.12+、Pillow、支持 M68K 的 Capstone 5，以及 68000 和 Z80 的 GNU 交叉工具。

通过 `--resource-root` 指定兼容的[素材包](high_level/ASSETS.md)，其中 `assets/` 和 `resources/` 位于同一级。构建命令见[汇编版](assembly/README.md)和[Python 版](high_level/README.md)。
