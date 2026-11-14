# Sangokushi Retsuden: Assembly source

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · **English**

The assembly uses GNU mnemonics for the 68000 and Z80. The build combines it with the cartridge address layout and encoded resources. The local resource pack has `resources/` and `assets/` side by side.

## Build

Use a local Windows drive, Python 3.12 or newer, Pillow, and Capstone 5 with M68K support. WSL runs two GNU toolchains: `m68k-elf-as`, `m68k-elf-ld`, and `m68k-elf-objcopy` for the 68000; `z80-unknown-coff-as` and `z80-unknown-coff-objcopy` for the Z80.

Run from this directory:

```powershell
python -m pip install Pillow "capstone>=5,<6"
$m68k = Read-Host '68000 工具目录'
$z80 = Read-Host 'Z80 COFF 工具目录'
$resources = Read-Host '本地素材根目录'
python -B -X utf8 -m tools.reconstructed_assembly --source-root . --layout-root tools/reconstructed_assembly/layout --resource-root $resources --m68k-tools $m68k --z80-tools $z80 --output build/cartridge --copier-header-fields tools/high_level_rom/resource_sources/copier_header.json --workers 2
```

`build/cartridge/` contains `SANGO.bin`, `SANGO.smd`, and the build output. Use a fresh output directory for each build. The default output is BIN; `--copier-header-fields` also writes the SMD header and interleaves the data. See [Build options](tools/reconstructed_assembly/README.en.md) for all flags.

## Editing

- Main program sources: `src/m68k/` and `src/z80/`. Address ranges, instruction sizes, and resource registrations are in `tools/reconstructed_assembly/layout/`.
- For graphics, sound effects, scenarios, and dialogue, see the [editing guide](EDITING.en.md) and the [resource paths](ASSETS.en.md).
- [Original behavior](docs/ORIGINAL_GAME_BUGS.en.md) documents quirks retained by the reconstruction.
