# Python entry monitor

[简体中文](README_ENTRY_MONITOR.md) · [繁體中文](README_ENTRY_MONITOR.zh-TW.md) · [日本語](README_ENTRY_MONITOR.ja.md) · **English**

[`EntryMonitor`](entry_monitor.py) uses `sys.monitoring`, available from CPython 3.12. Supply an available `tool_id` and a callback. The monitor matches live frames by their actual code objects and calls the handler on the owning thread.

`start()` and `close()` manage the monitor; closing releases its ID. Prepare targets through the [capture catalog](README_ENTRY_CAPTURE_CATALOG.en.md) and save records within the limits of the [storage component](README_ENTRY_CAPTURE_STORE.en.md).
