# 戰鬥場景生命週期

[简体中文](README_BATTLE_LIFECYCLE_STEPS.md) · **繁體中文** · [日本語](README_BATTLE_LIFECYCLE_STEPS.ja.md) · [English](README_BATTLE_LIFECYCLE_STEPS.en.md)

[`BattleLifecycleScenePrograms`](battle_lifecycle_steps.py) 連線場景初始化、分配、戰鬥回合及結果處理。各入口共享 Scene、資源和裝置提供器，合作式呼叫保留父呼叫的物理幀、返回地址、巢狀棧與條件碼。

戰鬥的入口和暫停型別見[戰鬥入口與結果續接](../../docs/README_BATTLE_ENTRY_STEPS.zh-TW.md)。戰鬥業務規則位於 [`business_battle.py`](business_battle.py)，目標宣告和指令佈局由 [`compiler_battle_lifecycle_steps.py`](compiler_battle_lifecycle_steps.py) 描述。
