# 完全フレーム計画

[简体中文](README_FRAME_PLAN.md) · [繁體中文](README_FRAME_PLAN.zh-TW.md) · **日本語** · [English](README_FRAME_PLAN.en.md)

実行設定の `frontend` は `events` または `frame_plan` を選びます。コンソールは `frame_plan` を使用し、ウィンドウ版は両方に対応します。

| `frame_plan` フィールド | 意味 |
| --- | --- |
| `max_frames` | セッション全体のフレーム枠。 |
| `max_device_steps_per_frame` | フレームごとの共通デバイス進行上限。 |
| `irq_level`、`video` | そのフレームの IRQ レベルと映像バスの状態。 |
| `pad_changes`、`live_pad_ports` | 物理コントローラーの入力と操作可能なポート。 |
| `audio` | `fm_ticks`、`psg_input_clocks`、`max_software_steps`、`im1`。 |

音声の `im1` は `null`、または `clock_hz`、`first_timestamp`、`timestamp_step` を含むオブジェクトです。フレーム n の時刻は `first_timestamp + (n - 1) × timestamp_step` です。チップクロックとウィンドウのタイミングは別設定です。

[`FiniteFramePlan`](frame_plan.py) は同じアプリ内で必要なデバイスイベントを進め、IRQ と物理入力を供給し、音声を進めます。デバイスイベント、IRQ、プログラムフレームはそれぞれの設定と残り枠に従います。通常のフレーム枠を使い切った後は、`extend_max_frames` で同じセッションの合計枠を増やせます。
