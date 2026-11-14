# 运行程序数据

**简体中文** · [繁體中文](README_HIGH_LEVEL_NATIVE_ENTRY.zh-TW.md) · [日本語](README_HIGH_LEVEL_NATIVE_ENTRY.ja.md) · [English](README_HIGH_LEVEL_NATIVE_ENTRY.en.md)

高级语言桌面入口使用 `g5510-reconstructed-game-config-v2`。项目源码决定游戏逻辑；用于原程序复制和校验的数据来自本版本实际构建。通过 [`tools.high_level_rom.build`](../high_level_rom/README_BUILD.md) 生成新本地构建目录，将它作为 `m68k_native_root`。同一次完整输出可作为 `sound_native_root`，其中的 `audio_startup` 和 `audio_driver` 属于 Z80 构建组。

独立的[归一化音频构建](../high_level_audio_engine/README_PORTABLE_BUILD.md)可单独作为声音程序根。加载器按所选构建形状核对实际源码、汇编内容、指令与布局。原游戏的只读程序复制和校验见[M68K 程序数据](../high_level_rom/README_COMPILED_CODE_DATA.md)。

[本地配置说明](README_LOCAL_CONFIG.md)列出 Scene 资源、芯片库、有限硬件输入和存档契约。
