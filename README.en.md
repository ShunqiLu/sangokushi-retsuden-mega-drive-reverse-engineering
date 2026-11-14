# Sangokushi Retsuden: Ransei no Eiyuutachi · Mega Drive Reverse Engineering

[简体中文](README.en.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · **English**

**Traditional Chinese cartridge `G-5510-00`** · 三國志列傳 亂世群英

This project provides reconstructed source code in assembly and Python. It is the first public project for this cartridge to offer both versions as buildable source code.

## Source code

- [Assembly](assembly/README.en.md): 68000 program, Z80 sound driver, and cartridge address layout. See the [editing guide](assembly/EDITING.en.md).
- [Python](high_level/README.en.md): game rules and compilers for city management, officers, troop movement, battles, AI, and audio. See the [editing guide](high_level/EDITING.en.md) and the [original address index](high_level/PENDING_SOURCE_INDEX.en.md).

## Tools

The [reverse-engineering tools](reverse_tools/README.en.md) convert between BIN and SMD, inspect cartridge headers, disassemble 68000 and Z80 code, and summarize MAME execution traces. They also parse graphics, audio, scenarios, and SRAM saves.

## Builds

Both versions build `SANGO.bin` and `SANGO.smd` for the Mega Drive. The build uses Windows with WSL, Python 3.12+, Pillow, Capstone 5 with M68K support, and GNU cross-tools for the 68000 and Z80.

Use `--resource-root` to point to a compatible [resource pack](high_level/ASSETS.en.md) with `assets/` and `resources/` side by side. The [assembly](assembly/README.en.md) and [Python](high_level/README.en.md) guides list the build commands.
