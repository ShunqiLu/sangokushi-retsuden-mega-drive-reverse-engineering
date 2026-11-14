# ハードウェア入力と音声ステップ

[简体中文](README_HARDWARE_INPUTS.md) · [繁體中文](README_HARDWARE_INPUTS.zh-TW.md) · **日本語** · [English](README_HARDWARE_INPUTS.en.md)

[アプリのハードウェア入力例](examples/application_hardware_inputs.json)は VDP、コントローラー、DMA、BUSREQ、R の観測、FM／PSG、起動イベントの有限入力を示します。容量はデバイスごとの単位です。例はクロックと入力を明示しており、実セッションでは対応するデバイスの入力を用意します。

[`audio_tick.py`](audio_tick.py) の `AudioTickSpec` は `fm_ticks`、`psg_input_clocks`、`im1_grant`、`max_software_steps` を使います。`im1_grant=None` は今回の音声割り込みなしを表します。アプリの `advance_audio_tick(spec)` が、実際のメールボックスの戻り値とタイマー A／B の処理位置を使って同じドライバーを進めます。

戻り値は今回消費した処理を示します。デバイスイベント、サンプルレート、応答は選択した設定に従います。[フレーム計画](README_FRAME_PLAN.ja.md)がハードウェア、IRQ、音声ステップをまとめます。
