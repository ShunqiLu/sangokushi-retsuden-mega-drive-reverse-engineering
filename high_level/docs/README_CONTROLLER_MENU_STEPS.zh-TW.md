# 控制器設定的裝置等待

[简体中文](README_CONTROLLER_MENU_STEPS.md) · **繁體中文** · [日本語](README_CONTROLLER_MENU_STEPS.ja.md) · [English](README_CONTROLLER_MENU_STEPS.en.md)

[`ControllerMenuPrograms(provider)`](../tools/high_level_gameplay_flow/controller_menu_steps.py) 與父流程共享一個 `BattleScenePrograms` 提供器。`yield from child.program(state, frame)` 推進 `0x0305B0` 控制器設定和 `0x02AACE` 新局選單。父流程持有原 `0x0305B0 / 0x0528` 返回槽。

| 等待型別 | 事件 |
| --- | --- |
| `ControllerSetupWait` | 控制器設定和選單中的 `0x030648`、`0x02AB6C` IRQ 輪詢。 |
| `GameplaySceneWait` | 視訊記憶體 DMA、精靈平面清理和 `0x008098` 聲音匯流排輪詢。 |

宿主遞交實際 IRQ 返回幀和裝置進度；恢復時，程式讀取原來的狀態欄位。子呼叫 `0x0068CE`、`0x006826` 與 `0x00808A` 使用父流程的影片及聲音介面。`require_current(state)` 校驗同一 Scene、執行緒、呼叫體和服務，完整幀保留 SP 與 SR。
