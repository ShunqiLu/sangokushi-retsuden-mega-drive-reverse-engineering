# Entry capture storage

[简体中文](README_ENTRY_CAPTURE_STORE.md) · [繁體中文](README_ENTRY_CAPTURE_STORE.zh-TW.md) · [日本語](README_ENTRY_CAPTURE_STORE.ja.md) · **English**

The store receives metadata and RAM from the caller. Each record uses a distinct short ID and writes to `input.json` and `input.ram`. The caller sets limits on record count, file size, JSON size, and free disk space. Close the store after capture. Results go to a new build subdirectory selected by the caller.
