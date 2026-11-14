# Game application interface

[简体中文](README_APPLICATION.md) · [繁體中文](README_APPLICATION.zh-TW.md) · [日本語](README_APPLICATION.ja.md) · **English**

[`GameApplication`](application.py) holds the same Scene, devices, scene continuations, and save medium. The window and [console](README_CONSOLE.en.md) pass physical button states and finite events through the same application API.

A full [`frontend.frame_plan`](README_FRAME_PLAN.en.md) combines device events, IRQ, and audio progression into one frame. At a runtime boundary, the last real scene is preserved. `export_save` exports the current 8192-byte medium. Screenshots come from the current VRAM.

`pcm_output` selects `discard`, `wav`, or Windows [`speakers`](README_SPEAKERS.en.md). WAV saves FM and PSG separately. Each device generates samples in its native format within the configured capacity. See [Local configuration](README_LOCAL_CONFIG.en.md) for runtime and build inputs.
