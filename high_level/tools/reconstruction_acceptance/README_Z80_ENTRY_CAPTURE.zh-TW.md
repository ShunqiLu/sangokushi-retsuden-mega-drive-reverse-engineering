# Z80 入口觀察器

[简体中文](README_Z80_ENTRY_CAPTURE.md) · **繁體中文** · [日本語](README_Z80_ENTRY_CAPTURE.ja.md) · [English](README_Z80_ENTRY_CAPTURE.en.md)

[`Z80EntryObserver`](z80_entry_capture.py) 使用 [`load_z80_capture_targets`](z80_entry_capture_catalog.py) 準備有限的公開 Z80 入口，並在同一遊戲會話捕獲實際呼叫。桌面採集配置的 `audio` 段負責啟用該觀察器。

Z80 與 M68K 入口共享會話的監視器及儲存容量。暫存器、控制資訊和返回槽按其實際來源讀取，未取得的欄位以缺項表示。具體輸出見[音訊快照](README_AUDIO_ENTRY_CAPTURE.zh-TW.md)和[採集檔案儲存](README_ENTRY_CAPTURE_STORE.zh-TW.md)。
