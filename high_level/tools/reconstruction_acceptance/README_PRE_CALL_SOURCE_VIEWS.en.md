# Pre-call source views

[简体中文](README_PRE_CALL_SOURCE_VIEWS.md) · [繁體中文](README_PRE_CALL_SOURCE_VIEWS.zh-TW.md) · [日本語](README_PRE_CALL_SOURCE_VIEWS.ja.md) · **English**

[`pre_call_source_views.py`](pre_call_source_views.py) links prepared helper sources to actual Python code objects. It preserves the full function shape, entry binding, and live identity needed for the same call. Runtime callbacks use the prepared view to identify pre-call execution.

The [original call catalog](README_PRE_CALL_CAPTURE_CATALOG.en.md) supplies parent calls and entry references. The [pre-call observer](README_M68K_PRE_CALL_CAPTURE.en.md) reads the actual state at the call site.
