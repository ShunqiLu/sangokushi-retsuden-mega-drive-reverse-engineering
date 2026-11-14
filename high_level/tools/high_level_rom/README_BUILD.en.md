# Python builder

[简体中文](README_BUILD.md) · [繁體中文](README_BUILD.zh-TW.md) · [日本語](README_BUILD.ja.md) · **English**

Set up the environment described in the [Python edition README](../../README.en.md). Run `tools.high_level_rom.build` from the source root, with a compatible resource root, toolchain directories, and a fresh output path.

| Argument | Purpose |
| --- | --- |
| `build` | Compiles game rules and the sound driver, encodes resources, and assembles a cartridge image. |
| `plan` | Runs the source compilers and produces a build plan. |
| `--project-root` | Python source root; defaults to the project root. |
| `--resource-root` | Compatible resource root containing `resources/` and `assets/`. |
| `--m68k-tools`, `--z80-tools` | Local Windows directories for GNU cross-tools run through WSL. |
| `--output` | A fresh output directory under the project’s `build/`. |
| `--workers` | Number of build workers; defaults to 2. |
| `--copier-header-fields` | Also builds SMD from structured header fields. |
| `--copier-header` | Uses a supplied container header instead of the header fields option. |

```powershell
python -B -X utf8 -m tools.high_level_rom.build build --project-root . --resource-root $resources --m68k-tools $m68k --z80-tools $z80 --output build/python-image --copier-header-fields tools/high_level_rom/resource_sources/copier_header.json
```

The build assigns explicit code and resource regions to produce `SANGO.bin`. With an SMD header it also writes `SANGO.smd`. Every position in the image must have a source. If preparation fails, diagnostics go to the output directory. The resource registry supplies the cartridge checksum field in the game's original format.

Domain modules contain the game rules, compilers, and physical targets. See [Game rules and resources](../../EDITING.en.md) for edits and [Run configuration](../reconstructed_game/README_LOCAL_CONFIG.en.md) for desktop use.
