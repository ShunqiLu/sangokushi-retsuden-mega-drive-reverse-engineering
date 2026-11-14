# City orders and resource deposits

[简体中文](README_SCENE_ORDERS.md) · [繁體中文](README_SCENE_ORDERS.zh-TW.md) · [日本語](README_SCENE_ORDERS.ja.md) · **English**

Treaties update both factions' flags according to direction. Resource deposits use the current faction and the leader's city to select gold or grain, then add and check the cap in 32-bit arithmetic. The entry point is `m68k_0318ac`; see the [68000 dispatcher](../../src/m68k/dispatch_descendants.s).
