# 戦闘の入口と再開

[简体中文](README_BATTLE_ENTRY_STEPS.md) · [繁體中文](README_BATTLE_ENTRY_STEPS.zh-TW.md) · **日本語** · [English](README_BATTLE_ENTRY_STEPS.en.md)

[`battle_entry_steps.py`](../tools/high_level_gameplay_flow/battle_entry_steps.py) は同じ戦闘の実行状態に対する一連の呼び出しを提供します。`BattleEntrySession(state, frame, entry=...)` には実際のシーン、完全なレジスターフレーム、物理スタック、SR を渡します。

| `entry` | カートリッジの入口 | 用途 |
| --- | --- | --- |
| `round` | `0x000DC0` | 戦闘のターンと結果の返却 |
| `main` | `0x000498` | メイン処理から戦闘へ移り、呼び出し元の戻りアドレスを使用 |
| `allocation` | `0x03D654` | 配置、割り当て、シーンオブジェクト制御 |
| `duel` | `0x026DB4` | 一騎討ちの行動と結果 |

`start()` は呼び出しを開始し、`resume_interrupt(returned, pc)` は実際の IRQ 復帰フレームを受け取ります。`resume_device(event)` は中断した同じフレームでデバイス待ちを再開し、`close()` は継続オブジェクトを解放します。呼び出しが完了すると `complete` と `result` が設定されます。ジェネレーターのインターフェースは `battle_entry_program(state, frame, entry=...)` です。

`GameplaySceneWait` は VRAM・DMA・音声のポーリング、`AllocationSceneWait` はオブジェクト制御のポーリング、`DuelSceneWait` は一騎討ち IRQ のポーリングです。同じアプリがデバイスを進めます。継続オブジェクトは実際の Scene、物理スタック、SR、素材インターフェースを保持します。
