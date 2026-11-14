# M68K 呼叫前快照

[简体中文](README_M68K_PRE_CALL_CAPTURE.md) · **繁體中文** · [日本語](README_M68K_PRE_CALL_CAPTURE.ja.md) · [English](README_M68K_PRE_CALL_CAPTURE.en.md)

[`M68KPreCallObserver`](m68k_pre_call_capture.py) 識別原 helper 正文執行前的現場位置。原呼叫、返回位置、入口角色和實際呼叫體來自[呼叫目錄](README_PRE_CALL_CAPTURE_CATALOG.zh-TW.md)，執行匹配透過[原始碼檢視](README_PRE_CALL_SOURCE_VIEWS.zh-TW.md)完成。

記錄格式為 `g5510-actual-m68k-pre-CALL-capture-v1`。快照含實際父幀、物理棧、RAM 與相關來源；真實父呼叫與入口別名各保留自己的身份。輸出由[採集儲存](README_ENTRY_CAPTURE_STORE.zh-TW.md)寫入。
