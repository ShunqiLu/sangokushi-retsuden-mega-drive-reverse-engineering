# Function entry monitor

[简体中文](README_ENTRY_MONITOR.md) · [繁體中文](README_ENTRY_MONITOR.zh-TW.md) · [日本語](README_ENTRY_MONITOR.ja.md) · **English**

The monitor uses Python 3.12's `sys.monitoring` to match functions by code object. Register the entry points, callbacks, and limits when installing it. Closing releases the monitoring slot. See [Entry capture](../reconstructed_game/README_ENTRY_CAPTURE.en.md) for settings.
