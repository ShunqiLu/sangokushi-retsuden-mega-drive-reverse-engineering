# Original call catalog

[简体中文](README_PRE_CALL_CAPTURE_CATALOG.md) · [繁體中文](README_PRE_CALL_CAPTURE_CATALOG.zh-TW.md) · [日本語](README_PRE_CALL_CAPTURE_CATALOG.ja.md) · **English**

[`prepare_pre_call_index`](pre_call_capture_catalog.py) builds `PreparedPreCallIndex` from the supplied entry targets and identifiable original calls. It distinguishes parent calls, helpers, aliased entries, and source entry references, retaining the relevant symbols, calls, and return relationships.

`SourceEntryReference` describes the current source entry; `PreCallGap` marks missing evidence. Live capture uses catalog records that match actual execution. See [Entry capture](../reconstructed_game/README_ENTRY_CAPTURE.en.md) for the exact file format and configuration.
