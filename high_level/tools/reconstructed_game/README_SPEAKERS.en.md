# Windows speaker output

[简体中文](README_SPEAKERS.md) · [繁體中文](README_SPEAKERS.zh-TW.md) · [日本語](README_SPEAKERS.ja.md) · **English**

The runtime's `pcm_output.mode` can select `speakers` to play actual FM and PSG output via WinMM. The game configuration still controls sample rates and game clocks.

```json
{
  "mode": "speakers",
  "fm_sample_rate_hz": 53267,
  "psg_sample_rate_hz": 44100,
  "max_fm_frames": 3196020,
  "max_psg_frames": 2646000,
  "device_id": -1,
  "max_queued_ms": 2000
}
```

Set the FM and PSG rates for the current chips, along with sample capacity and maximum queue time. `device_id=-1` selects the system Wave Mapper. You can also supply a nonnegative device number. FM is stereo, PSG is mono, and each retains its native rate.

[`speakers.py`](speakers.py) holds buffers while the system uses them and handles their return. Exhausted queue or sample capacity produces an explicit error. Select `wav` to save FM and PSG separately at their native rates.
