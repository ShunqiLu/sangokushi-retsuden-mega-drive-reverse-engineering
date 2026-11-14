# Entry capture catalog

[简体中文](README_ENTRY_CAPTURE_CATALOG.md) · [繁體中文](README_ENTRY_CAPTURE_CATALOG.zh-TW.md) · [日本語](README_ENTRY_CAPTURE_CATALOG.ja.md) · **English**

[`load_capture_targets(batch, project_root)`](entry_capture_catalog.py) returns a fixed tuple of `CaptureTarget` from a `g5510-concentrated-explicit-input-batch-v1` document. Each target matches a declaration by original entry address, Python module and function, frame type, and call arguments.

Loading checks the source, exact identifier, and entry identity. The [entry monitor](README_ENTRY_MONITOR.en.md) captures live state at the actual call.
