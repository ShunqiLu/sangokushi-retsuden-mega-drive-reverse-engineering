# M68K program data

[简体中文](README_COMPILED_CODE_DATA.md) · [繁體中文](README_COMPILED_CODE_DATA.zh-TW.md) · [日本語](README_COMPILED_CODE_DATA.ja.md) · **English**

The game's program-copy and checksum routines use instruction data from the current cartridge build. [`compiled_code_data.py`](compiled_code_data.py) provides an interface to load that data from this edition's build:

```python
from tools.high_level_rom.compiled_code_data import load_high_level_m68k_copy_data

data, details = load_high_level_m68k_copy_data(project_root, native_build_root)
```

Specify the source directory and output directory of the [cartridge image build](README_BUILD.en.md). The loader returns `ReadOnlyData` and its descriptor. It checks the generated assembly, ELF files, and instruction bytes against each other, selects whole instructions from the registry, and verifies shared aliases. The game reads the checksum-covered program bytes through this read-only view.

[`m68k_correspondence.py`](m68k_correspondence.py) maps known GNU symbols, constants, and PC-relative addresses to Capstone's instruction display. Code addresses come from each group's registered cartridge locations. See [Program data and desktop entry](../reconstructed_game/README_HIGH_LEVEL_NATIVE_ENTRY.en.md) for how these pieces fit together at runtime.
