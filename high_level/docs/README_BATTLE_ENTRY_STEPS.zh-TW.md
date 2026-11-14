# 戰鬥入口與結果續接

[简体中文](README_BATTLE_ENTRY_STEPS.md) · **繁體中文** · [日本語](README_BATTLE_ENTRY_STEPS.ja.md) · [English](README_BATTLE_ENTRY_STEPS.en.md)

[`battle_entry_steps.py`](../tools/high_level_gameplay_flow/battle_entry_steps.py) 提供同一戰鬥現場的完整呼叫。構造 `BattleEntrySession(state, frame, entry=...)` 時傳入實際場景、完整暫存器幀、物理棧和 SR。

| `entry` | 卡匣入口 | 呼叫職責 |
| --- | --- | --- |
| `round` | `0x000DC0` | 戰鬥回合和結果返回 |
| `main` | `0x000498` | 主流程跳轉至戰鬥，沿用呼叫者返回地址 |
| `allocation` | `0x03D654` | 部署、分配和場景物件控制 |
| `duel` | `0x026DB4` | 單挑行動與結果 |

`start()` 啟動呼叫；`resume_interrupt(returned, pc)` 接收真實 IRQ 返回的幀；`resume_device(event)` 使用同一個掛起幀恢復裝置等待。`close()` 釋放續接物件；呼叫體完整返回時設定 `complete` 和 `result`。生成器介面是 `battle_entry_program(state, frame, entry=...)`。

`GameplaySceneWait` 表示視訊記憶體、DMA 或音訊輪詢；`AllocationSceneWait` 表示物件控制輪詢；`DuelSceneWait` 表示單挑 IRQ 輪詢。裝置由同一應用推進，續接物件保留實際 Scene、物理棧、SR 和資源介面。
