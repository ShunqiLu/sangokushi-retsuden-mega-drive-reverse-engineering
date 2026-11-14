# M68000 entry snapshot

[简体中文](README_M68K_ENTRY_CAPTURE.md) · [繁體中文](README_M68K_ENTRY_CAPTURE.zh-TW.md) · [日本語](README_M68K_ENTRY_CAPTURE.ja.md) · **English**

[`M68KEntryCapture`](m68k_entry_capture.py) reads a register frame, SR, return slot, and RAM from the same scene at a registered Python rule function's entry. The source file, function, and frame type must match the actual code object. The return site comes from the physical call stack.

Records use `g5510-actual-m68k-entry-capture-v1`. Read-only DATA can be retained through a shared context for the session. The snapshot records a call that has already entered; use the [pre-call observer](README_M68K_PRE_CALL_CAPTURE.en.md) for state before the original call instruction.
