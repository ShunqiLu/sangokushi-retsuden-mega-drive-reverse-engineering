# Z80 audio entry snapshot

[简体中文](README_AUDIO_ENTRY_CAPTURE.md) · [繁體中文](README_AUDIO_ENTRY_CAPTURE.zh-TW.md) · [日本語](README_AUDIO_ENTRY_CAPTURE.ja.md) · **English**

[`snapshot_audio_entry`](audio_entry_capture.py) reads the snapshot from the caller's actual audio state, frame, entry binding, and continuation. It reads the Z80 carrier, control state, alternate registers, and return word from available fields, each with an observable source. Unknown parts of PC and R are `missing`; known bits retain their width and order.

Audio entry records use `g5510-actual-z80-entry-capture-v1`. The [storage component](README_ENTRY_CAPTURE_STORE.en.md) saves the captured 8192 bytes of sound RAM separately. The [Z80 observer](README_Z80_ENTRY_CAPTURE.en.md) binds snapshots to live function entries in the same game.
