# 控制器设置的设备等待

**简体中文** · [繁體中文](README_CONTROLLER_MENU_STEPS.zh-TW.md) · [日本語](README_CONTROLLER_MENU_STEPS.ja.md) · [English](README_CONTROLLER_MENU_STEPS.en.md)

[`ControllerMenuPrograms(provider)`](../tools/high_level_gameplay_flow/controller_menu_steps.py) 与父流程共享一个 `BattleScenePrograms` 提供器。`yield from child.program(state, frame)` 推进 `0x0305B0` 控制器设置和 `0x02AACE` 新局菜单。父流程持有原 `0x0305B0 / 0x0528` 返回槽。

| 等待类型 | 事件 |
| --- | --- |
| `ControllerSetupWait` | 控制器设置和菜单中的 `0x030648`、`0x02AB6C` IRQ 轮询。 |
| `GameplaySceneWait` | 显存 DMA、精灵平面清理和 `0x008098` 声音总线轮询。 |

宿主递交实际 IRQ 返回帧和设备进度；恢复时，程序读取原来的状态字段。子调用 `0x0068CE`、`0x006826` 与 `0x00808A` 使用父流程的视频及声音接口。`require_current(state)` 校验同一 Scene、线程、调用体和服务，完整帧保留 SP 与 SR。
