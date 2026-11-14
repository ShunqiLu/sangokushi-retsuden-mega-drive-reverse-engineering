# Z80 入口オブザーバー

[简体中文](README_Z80_ENTRY_CAPTURE.md) · [繁體中文](README_Z80_ENTRY_CAPTURE.zh-TW.md) · **日本語** · [English](README_Z80_ENTRY_CAPTURE.en.md)

[`Z80EntryObserver`](z80_entry_capture.py) は [`load_z80_capture_targets`](z80_entry_capture_catalog.py) を使って対象の Z80 公開入口を用意し、同じゲームセッションで実際の呼び出しを記録します。デスクトップのキャプチャー設定では `audio` セクションで有効にします。

Z80 と M68K の入口はセッションのモニターと保存容量を共有します。レジスター、制御情報、戻りスロットは実際の取得元から読み、取得できないフィールドは欠落として記録します。出力は[音声スナップショット](README_AUDIO_ENTRY_CAPTURE.ja.md)と[キャプチャーの保存](README_ENTRY_CAPTURE_STORE.ja.md)を参照してください。
