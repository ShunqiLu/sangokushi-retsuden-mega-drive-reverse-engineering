# Runtime program data

[简体中文](README_HIGH_LEVEL_NATIVE_ENTRY.md) · [繁體中文](README_HIGH_LEVEL_NATIVE_ENTRY.zh-TW.md) · [日本語](README_HIGH_LEVEL_NATIVE_ENTRY.ja.md) · **English**

The Python desktop entry uses `g5510-reconstructed-game-config-v2`. Game logic comes from project sources; the original program-copy and checksum routines use data from this edition's build. Use [`tools.high_level_rom.build`](../high_level_rom/README_BUILD.en.md) to make a fresh local build directory for `m68k_native_root`. The same full output can serve as `sound_native_root`; its `audio_startup` and `audio_driver` are the Z80 build groups.

A standalone [normalized audio build](../high_level_audio_engine/README_PORTABLE_BUILD.en.md) can also serve as the sound program root. The loader checks the sources, assembly, instructions, and layout for the chosen build form. See [M68K program data](../high_level_rom/README_COMPILED_CODE_DATA.en.md) for read-only program copying and checksums.

See [Local configuration](README_LOCAL_CONFIG.en.md) for Scene resources, the chip library, bounded hardware inputs, and saves.
