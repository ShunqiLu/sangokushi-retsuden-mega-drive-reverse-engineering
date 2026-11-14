# 冷復位與暖復位

[简体中文](README_ORDERED_COLD_PLAN.md) · **繁體中文** · [日本語](README_ORDERED_COLD_PLAN.ja.md) · [English](README_ORDERED_COLD_PLAN.en.md)

有序復位格式 `g5510-original-ordered-restart-plans-v2` 包含 `format` 和 `plans`。每項選擇 `kind`（`intro` 或 `narrative`）與 `reset_path`（`warm` 或 `cold`）。實際遊戲分支決定復位路徑；配置宣告該路徑所用的有限供應。

| 欄位 | 值 |
| --- | --- |
| `reset_pulse_clocks` | 暖復位 2 項，冷復位 3 項；每項至少 3 個時鐘。 |
| `irq_clock_hz` | 與實際驅動相符的正整數頻率。 |
| `startup_im1_offsets` | 3 項嚴格遞增的正整數偏移。 |

冷復位的 workspace 複製使用 `transfers.driver` 許可，位元組讀寫使用 `sound.max_DATA_operations`。兩項為會話累計容量。每次冷 workspace 需要 8153 次漸進複製和 16326 次音訊 DATA 操作；驅動啟動和通常執行消費各自的餘量。

[混合路徑示例](examples/ordered_restart_cold_plan.example.json)展示格式，[有序復位說明](README_ORDERED_RESTARTS.zh-TW.md)給出啟用方法。
