# Python 入口监视器

**简体中文** · [繁體中文](README_ENTRY_MONITOR.zh-TW.md) · [日本語](README_ENTRY_MONITOR.ja.md) · [English](README_ENTRY_MONITOR.en.md)

[`EntryMonitor`](entry_monitor.py) 使用 CPython 3.12 起提供的 `sys.monitoring`。调用者指定实际可用的 `tool_id` 与处理函数。监视器通过真实代码对象定位现场，在所属线程执行处理。

生命周期由 `start()` 和 `close()` 管理；关闭归还监视 ID。调用者通过[采集目录](README_ENTRY_CAPTURE_CATALOG.md)准备目标，并通过[存储组件](README_ENTRY_CAPTURE_STORE.md)保存有限记录。
