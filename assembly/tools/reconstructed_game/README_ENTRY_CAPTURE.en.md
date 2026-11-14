# Function entry capture

[简体中文](README_ENTRY_CAPTURE.md) · [繁體中文](README_ENTRY_CAPTURE.zh-TW.md) · [日本語](README_ENTRY_CAPTURE.ja.md) · **English**

The desktop application in the [Python edition](../../../high_level/README.en.md) can capture selected 68000 or Z80 entry points during a configured session. It writes to a new local directory within the specified limits. See the [68000 example](examples/entry_capture.example.json) and the [audio example](examples/entry_capture.audio.example.json).

In a local copy of the Python edition, prepare the normal game configuration and then supply a separate capture configuration:

```powershell
python -B -m tools.reconstructed_game --config ./play.json --capture-entries ./entry-capture.json
```
