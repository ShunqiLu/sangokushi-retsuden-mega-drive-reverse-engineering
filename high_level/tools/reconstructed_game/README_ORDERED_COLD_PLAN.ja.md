# コールドリセットとウォームリセット

[简体中文](README_ORDERED_COLD_PLAN.md) · [繁體中文](README_ORDERED_COLD_PLAN.zh-TW.md) · **日本語** · [English](README_ORDERED_COLD_PLAN.en.md)

順序付きリセットの形式 `g5510-original-ordered-restart-plans-v2` は `format` と `plans` を含みます。各項目は `kind`（`intro` または `narrative`）と `reset_path`（`warm` または `cold`）を選びます。実際のゲーム分岐がリセット経路を決め、設定がその経路の有限入力を供給します。

| フィールド | 値 |
| --- | --- |
| `reset_pulse_clocks` | ウォームは 2 項目、コールドは 3 項目。各項目は 3 クロック以上。 |
| `irq_clock_hz` | 実際のドライバーに合う正の整数周波数。 |
| `startup_im1_offsets` | 厳密に増加する正の整数オフセット 3 個。 |

コールド時の作業領域コピーは `transfers.driver` の許可を使い、バイトの読み書きは `sound.max_DATA_operations` を使います。いずれもセッション累計です。コールド時の作業領域 1 回につき、段階的なコピー 8153 回と音声 DATA 操作 16326 回が必要です。ドライバーの起動と通常動作は各自の残り枠を消費します。

[混合経路の例](examples/ordered_restart_cold_plan.example.json)で形式を、[順序付き再起動](README_ORDERED_RESTARTS.ja.md)で有効化の方法を確認できます。
