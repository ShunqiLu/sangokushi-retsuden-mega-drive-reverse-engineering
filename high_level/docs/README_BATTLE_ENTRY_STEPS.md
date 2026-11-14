# 战斗入口与结果续接

[`battle_entry_steps.py`](../tools/high_level_gameplay_flow/battle_entry_steps.py) 提供同一战斗现场的完整调用。构造 `BattleEntrySession(state, frame, entry=...)` 时传入实际场景、完整寄存器帧、物理栈和 SR。

| `entry` | 卡带入口 | 调用职责 |
| --- | --- | --- |
| `round` | `0x000DC0` | 战斗回合和结果返回 |
| `main` | `0x000498` | 主流程跳转至战斗，沿用调用者返回地址 |
| `allocation` | `0x03D654` | 部署、分配和场景对象控制 |
| `duel` | `0x026DB4` | 单挑行动与结果 |

`start()` 启动调用；`resume_interrupt(returned, pc)` 接收真实 IRQ 返回的帧；`resume_device(event)` 使用同一个挂起帧恢复设备等待。`close()` 释放续接对象；调用体完整返回时设置 `complete` 和 `result`。生成器接口是 `battle_entry_program(state, frame, entry=...)`。

`GameplaySceneWait` 表示显存、DMA 或音频轮询；`AllocationSceneWait` 表示对象控制轮询；`DuelSceneWait` 表示单挑 IRQ 轮询。设备由同一应用推进，续接对象保留实际 Scene、物理栈、SR 和资源接口。
