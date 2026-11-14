# コントローラー設定のデバイス待ち

[简体中文](README_CONTROLLER_MENU_STEPS.md) · [繁體中文](README_CONTROLLER_MENU_STEPS.zh-TW.md) · **日本語** · [English](README_CONTROLLER_MENU_STEPS.en.md)

[`ControllerMenuPrograms(provider)`](../tools/high_level_gameplay_flow/controller_menu_steps.py) は親フローと `BattleScenePrograms` プロバイダーを共有します。`yield from child.program(state, frame)` は `0x0305B0` のコントローラー設定と `0x02AACE` の新規ゲームメニューを進めます。親は元の戻りスロット `0x0305B0 / 0x0528` を保持します。

| 待機種別 | イベント |
| --- | --- |
| `ControllerSetupWait` | コントローラー設定とメニューでの `0x030648`、`0x02AB6C` の IRQ ポーリング。 |
| `GameplaySceneWait` | VRAM DMA、スプライトプレーンのクリア、`0x008098` の音声バスポーリング。 |

ホストは実際の IRQ 復帰フレームとデバイスの進行を渡します。再開時に元の状態フィールドを読みます。子呼び出し `0x0068CE`、`0x006826`、`0x00808A` は親の映像・音声インターフェースを使います。`require_current(state)` は Scene、スレッド、呼び出し、サービスが同一であることを確認します。完全なフレームは SP と SR を保持します。
