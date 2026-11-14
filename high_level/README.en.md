# Sangokushi Retsuden: Python source · G-5510-00

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · **English**

The Python source covers city management, marches, battles, scenes, AI, and audio. The build compiles the supported rules to Mega Drive 68000 and Z80 code and encodes local resources into a cartridge image.

## Build

The build uses Windows with WSL, Python 3.12 or later, Pillow, and Capstone 5 with M68K support. Put these GNU cross-tools in Windows directories accessible from WSL:

- 68000：`m68k-elf-as`、`m68k-elf-ld`、`m68k-elf-objcopy`。
- Z80 COFF：`z80-unknown-coff-as`、`z80-unknown-coff-objcopy`。

Run the PowerShell commands below from this directory. Supply both toolchain paths and a compatible resource directory containing `assets/` and `resources/` side by side.

```powershell
python -m pip install Pillow "capstone>=5,<6"
$m68k = Read-Host '68000 交叉工具目录'
$z80 = Read-Host 'Z80 COFF 交叉工具目录'
$resources = Read-Host '兼容素材根'
python -B -X utf8 -m tools.high_level_rom.build build --project-root . --resource-root $resources --m68k-tools $m68k --z80-tools $z80 --output build/python-image --copier-header-fields tools/high_level_rom/resource_sources/copier_header.json
```

The build writes to a fresh `build/python-image/`. It produces `SANGO.bin` by default; `--copier-header-fields` also generates `SANGO.smd`. See [Build options](tools/high_level_rom/README_BUILD.en.md) for inputs, flags, and outputs.

## Editing

- The [editing guide](EDITING.en.md) locates sources for rules, starting scenarios, saves, graphics, and audio.
- The [resource guide](ASSETS.en.md) covers indexed PNGs, palettes, shared audio, and the local resource layout.
- The [original address index](PENDING_SOURCE_INDEX.en.md) maps selected cartridge entry points to Python functions.
- [Original behavior](docs/ORIGINAL_GAME_BUGS.en.md) lists rules and edge cases retained by the reconstruction.

[Desktop mode](tools/reconstructed_game/README_LOCAL_CONFIG.en.md) uses a local run directory, CPU code built from this source tree, an [audio bridge built with external YMFM sources](tools/high_level_audio_engine/README_YMFM.en.md), and explicit device and save settings. The console and Tk window use the same game application.
