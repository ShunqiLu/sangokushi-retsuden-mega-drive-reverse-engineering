# Device waits during controller setup

[简体中文](README_CONTROLLER_MENU_STEPS.md) · [繁體中文](README_CONTROLLER_MENU_STEPS.zh-TW.md) · [日本語](README_CONTROLLER_MENU_STEPS.ja.md) · **English**

[`ControllerMenuPrograms(provider)`](../tools/high_level_gameplay_flow/controller_menu_steps.py) shares a `BattleScenePrograms` provider with the parent flow. `yield from child.program(state, frame)` advances controller setup at `0x0305B0` and the new campaign menu at `0x02AACE`. The parent retains the original `0x0305B0 / 0x0528` return slot.

| Wait type | Event |
| --- | --- |
| `ControllerSetupWait` | `0x030648` and `0x02AB6C` IRQ polling in controller setup and the menu. |
| `GameplaySceneWait` | VRAM DMA, sprite plane clearing, and `0x008098` sound bus polling. |

The host supplies actual IRQ return frames and device progress. On resumption, the code reads the original state fields. Subcalls `0x0068CE`, `0x006826`, and `0x00808A` use the parent's video and sound interfaces. `require_current(state)` validates that the Scene, thread, call, and services match. Full frames preserve SP and SR.
