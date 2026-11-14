# Entry capture storage

[简体中文](README_ENTRY_CAPTURE_STORE.md) · [繁體中文](README_ENTRY_CAPTURE_STORE.zh-TW.md) · [日本語](README_ENTRY_CAPTURE_STORE.ja.md) · **English**

[`EntryCaptureStore`](entry_capture_store.py) stores entry state in a new directory supplied explicitly. Its constructor takes limits for record count, total bytes, per-record metadata, and reserved space. Each record has a unique path.

| Method | Data saved |
| --- | --- |
| `write_case` | Entry metadata and original RAM bytes. |
| `write_vdp_state` | Entry records with VDP state. |
| `write_readonly_source` | Read-only data from the same session and its metadata. |
| `close(outcome)` | Writes `capture-receipt.json` with the saved records and budget limits. |

Metadata preserves the original entry, role, source, and capture location. When the capture budget runs out, writing stops; the application continues with its own runtime resources.
