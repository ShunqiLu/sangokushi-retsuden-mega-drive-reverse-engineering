# ゲームアプリのインターフェース

[简体中文](README_APPLICATION.md) · [繁體中文](README_APPLICATION.zh-TW.md) · **日本語** · [English](README_APPLICATION.en.md)

[`GameApplication`](application.py) は同じ Scene、デバイス、シーンの継続状態、セーブ媒体を保持します。ウィンドウと[コンソール](README_CONSOLE.ja.md)は同じ API から物理ボタンの状態と有限のイベントを渡します。

完全な [`frontend.frame_plan`](README_FRAME_PLAN.ja.md) は、デバイスイベント、IRQ、音声の進行を 1 フレームにまとめます。実行境界では最後の実シーンを保持します。`export_save` は現在の 8192 バイトの媒体を書き出し、画面キャプチャーは現在の VRAM から生成します。

`pcm_output` で `discard`、`wav`、Windows の [`speakers`](README_SPEAKERS.ja.md) を選びます。WAV は FM と PSG を別々に保存します。両デバイスは設定された容量内で、それぞれの元の形式のサンプルを生成します。実行設定とビルド入力は[ローカル設定](README_LOCAL_CONFIG.ja.md)を参照してください。
