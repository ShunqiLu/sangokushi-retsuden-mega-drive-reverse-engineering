# Z80 entry observer

[简体中文](README_Z80_ENTRY_CAPTURE.md) · [繁體中文](README_Z80_ENTRY_CAPTURE.zh-TW.md) · [日本語](README_Z80_ENTRY_CAPTURE.ja.md) · **English**

[`Z80EntryObserver`](z80_entry_capture.py) uses [`load_z80_capture_targets`](z80_entry_capture_catalog.py) to prepare a bounded list of public Z80 entries and captures actual calls in the same session. The `audio` section of the desktop capture configuration enables the observer.

Z80 and M68K entries share the session monitor and storage budget. Registers, control information, and return slots are read from their actual sources; missing fields are marked as unavailable. See [Audio snapshots](README_AUDIO_ENTRY_CAPTURE.en.md) and [Capture storage](README_ENTRY_CAPTURE_STORE.en.md) for the result.
