# 城市命令与资源入账

**简体中文** · [繁體中文](README_SCENE_ORDERS.zh-TW.md) · [日本語](README_SCENE_ORDERS.ja.md) · [English](README_SCENE_ORDERS.en.md)

关系协议按方向更新双方标志；资源入账读取当前势力和领袖所在城市，选取资金或粮食栏，再进行 32 位累加和上限比较。汇编入口为 `m68k_0318ac`，相关逻辑见 [68000 分派源码](../../src/m68k/dispatch_descendants.s)。
