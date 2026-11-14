# Z80 音訊入口快照

[简体中文](README_AUDIO_ENTRY_CAPTURE.md) · **繁體中文** · [日本語](README_AUDIO_ENTRY_CAPTURE.ja.md) · [English](README_AUDIO_ENTRY_CAPTURE.en.md)

[`snapshot_audio_entry`](audio_entry_capture.py) 從呼叫方提供的實際音訊狀態、幀、入口繫結和續接資訊讀取快照。它按已有欄位讀取 Z80 載體、控制狀態、交替暫存器與返回字；各值帶有可觀察來源。PC 與 R 的未知部分用 `missing` 記錄，真實已知部分保留原寬度和順序。

音訊入口記錄採用 `g5510-actual-z80-entry-capture-v1`；已採集的 8192 位元組聲音 RAM 由[儲存元件](README_ENTRY_CAPTURE_STORE.zh-TW.md)獨立儲存。[Z80 觀察器](README_Z80_ENTRY_CAPTURE.zh-TW.md)將快照繫結到同一遊戲中的實際函式入口。
