# 戦闘シーンのライフサイクル

[简体中文](README_BATTLE_LIFECYCLE_STEPS.md) · [繁體中文](README_BATTLE_LIFECYCLE_STEPS.zh-TW.md) · **日本語** · [English](README_BATTLE_LIFECYCLE_STEPS.en.md)

[`BattleLifecycleScenePrograms`](battle_lifecycle_steps.py) はシーン初期化、割り当て、戦闘ターン、結果処理をつなぎます。各入口は Scene、素材、デバイスプロバイダーを共有します。協調呼び出しは親の物理フレーム、戻りアドレス、入れ子のスタック、条件コードを保持します。

入口と中断の種類は[戦闘の入口と再開](../../docs/README_BATTLE_ENTRY_STEPS.ja.md)を参照してください。戦闘ルールは [`business_battle.py`](business_battle.py) に、ターゲット定義と命令配置は [`compiler_battle_lifecycle_steps.py`](compiler_battle_lifecycle_steps.py) にあります。
