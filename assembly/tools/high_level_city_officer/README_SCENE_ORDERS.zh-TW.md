# 城市命令與資源入賬

[简体中文](README_SCENE_ORDERS.md) · **繁體中文** · [日本語](README_SCENE_ORDERS.ja.md) · [English](README_SCENE_ORDERS.en.md)

關係協議按方向更新雙方標誌；資源入賬讀取當前勢力和領袖所在城市，選取資金或糧食欄，再進行 32 位累加和上限比較。彙編入口為 `m68k_0318ac`，相關邏輯見 [68000 分派原始碼](../../src/m68k/dispatch_descendants.s)。
