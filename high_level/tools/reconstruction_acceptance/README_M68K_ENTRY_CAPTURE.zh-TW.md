# M68000 入口快照

[简体中文](README_M68K_ENTRY_CAPTURE.md) · **繁體中文** · [日本語](README_M68K_ENTRY_CAPTURE.ja.md) · [English](README_M68K_ENTRY_CAPTURE.en.md)

[`M68KEntryCapture`](m68k_entry_capture.py) 在登記的 Python 業務函式入口讀取同一場景的暫存器幀、SR、返回槽和 RAM。採集需要原始檔、函式、幀型別與實際程式碼物件對應；返回位置來自真實物理呼叫棧。

記錄格式為 `g5510-actual-m68k-entry-capture-v1`。只讀 DATA 可透過同一會話的一次共享上下文保留。函式入口快照描述已進入的呼叫；需要原呼叫指令前的狀態時使用[呼叫前觀察器](README_M68K_PRE_CALL_CAPTURE.zh-TW.md)。
