# Z80 WZ state in the rhythm channel

[简体中文](README_RHYTHM_WZ.md) · [繁體中文](README_RHYTHM_WZ.zh-TW.md) · [日本語](README_RHYTHM_WZ.ja.md) · **English**

The Z80 instruction `BIT 2,(HL)` uses internal WZ state to set undocumented flags. The rhythm logic uses [`rhythm_wz.py`](rhythm_wz.py) to trace the operations that produce the relevant addresses in the same Z80 state, then uses that state for the actual bit test. The audio flow maintains it with the original ports, registers, and device inputs.

Known original operations update WZ. The runtime provides the initial state with an observable source. The sound driver and device providers advance channel events, timers, and IRQs.
