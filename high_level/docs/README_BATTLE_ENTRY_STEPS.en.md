# Battle entry points and continuations

[简体中文](README_BATTLE_ENTRY_STEPS.md) · [繁體中文](README_BATTLE_ENTRY_STEPS.zh-TW.md) · [日本語](README_BATTLE_ENTRY_STEPS.ja.md) · **English**

[`battle_entry_steps.py`](../tools/high_level_gameplay_flow/battle_entry_steps.py) provides complete calls into the same battle state. Construct `BattleEntrySession(state, frame, entry=...)` with the live scene, the full register frame, the physical stack, and SR.

| `entry` | Cartridge entry point | Role |
| --- | --- | --- |
| `round` | `0x000DC0` | Battle turns and result return |
| `main` | `0x000498` | Main flow into battle, using the caller's return address |
| `allocation` | `0x03D654` | Deployment, assignment, and scene object control |
| `duel` | `0x026DB4` | Duel actions and outcomes |

`start()` starts the call. `resume_interrupt(returned, pc)` accepts the actual IRQ return frame. `resume_device(event)` resumes a device wait with the same suspended frame. `close()` releases the continuation. A complete return sets `complete` and `result`. The generator interface is `battle_entry_program(state, frame, entry=...)`.

`GameplaySceneWait` means VRAM, DMA, or audio polling. `AllocationSceneWait` means object control polling. `DuelSceneWait` means duel IRQ polling. The same application advances the devices. The continuation keeps the live Scene, physical stack, SR, and resource interfaces.
