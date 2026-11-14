# Python 入口監視器

[简体中文](README_ENTRY_MONITOR.md) · **繁體中文** · [日本語](README_ENTRY_MONITOR.ja.md) · [English](README_ENTRY_MONITOR.en.md)

[`EntryMonitor`](entry_monitor.py) 使用 CPython 3.12 起提供的 `sys.monitoring`。呼叫者指定實際可用的 `tool_id` 與處理函式。監視器透過真實程式碼物件定位現場，在所屬執行緒執行處理。

生命週期由 `start()` 和 `close()` 管理；關閉歸還監視 ID。呼叫者透過[採集目錄](README_ENTRY_CAPTURE_CATALOG.zh-TW.md)準備目標，並透過[儲存元件](README_ENTRY_CAPTURE_STORE.zh-TW.md)儲存有限記錄。
