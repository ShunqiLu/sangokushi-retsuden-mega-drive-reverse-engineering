# Optional entry capture

[简体中文](README_ENTRY_CAPTURE.md) · [繁體中文](README_ENTRY_CAPTURE.zh-TW.md) · [日本語](README_ENTRY_CAPTURE.ja.md) · **English**

`--capture-entries` enables source entry capture in the same desktop session. Capture settings are separate from the game configuration. Entry data comes from actual call frames, physical return slots, memory, and call context. File count and space limits are explicit.

```powershell
python -B -X utf8 -m tools.reconstructed_game --config build/play-config.json --capture-entries entry-capture.json
```

| Field | Purpose |
| --- | --- |
| `format` | Capture configuration version. |
| `batch` | JSON file containing entry targets. |
| `output` | New `build/` subdirectory with an existing parent. |
| `tool_id` | Available Python monitoring tool ID from 0 to 5. |
| `max_cases`, `max_captures_per_entry` | Total record limit and per-entry record limit. |
| `max_total_bytes`, `max_case_json_bytes`, `min_free_bytes` | Total bytes, maximum JSON size, and reserved disk space. |

The base format is `g5510-entry-capture-config-v1`. Version 2 declares Z80 entries with `audio`. Version 3 declares pre-call capture with `pre_call`. In version 4, `pre_call` contains the Boolean values `enabled` and `include_current_source_calls`. Resolve relative paths for `batch` and `output` from the capture configuration file.

[`entry_capture_config.py`](entry_capture_config.py) handles configuration, start, and stop. [Capture storage](../reconstruction_acceptance/README_ENTRY_CAPTURE_STORE.en.md) describes file formats and limits. See the entry contracts for [M68K](../reconstruction_acceptance/README_M68K_ENTRY_CAPTURE.en.md), [Z80](../reconstruction_acceptance/README_Z80_ENTRY_CAPTURE.en.md), and [pre-call capture](../reconstruction_acceptance/README_M68K_PRE_CALL_CAPTURE.en.md).
