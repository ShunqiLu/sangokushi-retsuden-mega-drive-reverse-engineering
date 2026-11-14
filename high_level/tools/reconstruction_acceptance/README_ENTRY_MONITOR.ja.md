# Python の入口モニター

[简体中文](README_ENTRY_MONITOR.md) · [繁體中文](README_ENTRY_MONITOR.zh-TW.md) · **日本語** · [English](README_ENTRY_MONITOR.en.md)

[`EntryMonitor`](entry_monitor.py) は CPython 3.12 以降の `sys.monitoring` を使います。利用可能な `tool_id` と処理関数を指定します。実際のコードオブジェクトでフレームを照合し、そのフレームのスレッドで処理関数を呼び出します。

`start()` と `close()` がモニターを管理し、終了時に監視 ID を解放します。[キャプチャーカタログ](README_ENTRY_CAPTURE_CATALOG.ja.md)で対象を用意し、[保存コンポーネント](README_ENTRY_CAPTURE_STORE.ja.md)で上限内の記録を保存します。
