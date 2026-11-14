# M68K pre-call snapshot

[简体中文](README_M68K_PRE_CALL_CAPTURE.md) · [繁體中文](README_M68K_PRE_CALL_CAPTURE.zh-TW.md) · [日本語](README_M68K_PRE_CALL_CAPTURE.ja.md) · **English**

[`M68KPreCallObserver`](m68k_pre_call_capture.py) identifies execution before the original helper body. The [call catalog](README_PRE_CALL_CAPTURE_CATALOG.en.md) supplies the original call and return site, entry role, and actual call body. The [source view](README_PRE_CALL_SOURCE_VIEWS.en.md) matches them at runtime.

Records use `g5510-actual-m68k-pre-CALL-capture-v1`. Each snapshot contains the actual parent frame, physical stack, RAM, and related provenance. Parent calls and aliased entry points retain separate identities. The [capture store](README_ENTRY_CAPTURE_STORE.en.md) writes the output.
