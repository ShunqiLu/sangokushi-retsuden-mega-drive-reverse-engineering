# Battle scene lifecycle

[简体中文](README_BATTLE_LIFECYCLE_STEPS.md) · [繁體中文](README_BATTLE_LIFECYCLE_STEPS.zh-TW.md) · [日本語](README_BATTLE_LIFECYCLE_STEPS.ja.md) · **English**

[`BattleLifecycleScenePrograms`](battle_lifecycle_steps.py) joins scene initialization, allocation, battle turns, and result handling. Entry points share the Scene, resources, and device providers. The cooperative calls keep the parent's physical frame, return address, nested stack, and flags.

See [Battle entry points and continuations](../../docs/README_BATTLE_ENTRY_STEPS.en.md) for entries and wait types. The battle rules are in [`business_battle.py`](business_battle.py). [`compiler_battle_lifecycle_steps.py`](compiler_battle_lifecycle_steps.py) describes the targets and instruction layout.
