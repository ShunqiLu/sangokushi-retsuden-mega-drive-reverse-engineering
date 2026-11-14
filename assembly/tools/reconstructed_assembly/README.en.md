# Assembly build options

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · **English**

The builder reads mnemonics according to each code group's address layout, assembles instructions with GNU cross-tools, and combines them with encoded resources. It verifies 68000 and Z80 instruction sizes using ELF symbols and COFF boundaries, respectively.

| Option | Purpose |
| --- | --- |
| `--source-root` | Source root containing `src/m68k/` and `src/z80/` |
| `--layout-root` | `tools/reconstructed_assembly/layout/`, containing the manifest and 14 groups of instruction ranges |
| `--resource-root` | External resource root containing `resources/` and `assets/` |
| `--m68k-tools`, `--z80-tools` | GNU toolchain directories on a local Windows drive; WSL runs the tools |
| `--output` | New directory under `build/` in this source tree |
| `--copier-header-fields` | Optional SMD header fields; the sample is in `tools/high_level_rom/resource_sources/` |
| `--workers` | Parallel jobs, from 1 to 4 |

The build produces a linear BIN and optionally an SMD. Each address range must have exactly one source or resource owner. The builder reports gaps, overlaps, and changes in width. See the [assembly README](../../README.en.md) for the full command.
