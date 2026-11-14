# Windows 扬声器输出

**简体中文** · [繁體中文](README_SPEAKERS.zh-TW.md) · [日本語](README_SPEAKERS.ja.md) · [English](README_SPEAKERS.en.md)

运行配置的 `pcm_output.mode` 可选择 `speakers`，由 WinMM 播放实际的 FM 与 PSG 输出。芯片的采样率和游戏时钟仍由游戏配置决定。

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

填写与当前芯片相符的 FM、PSG 采样率，以及会话的样本容量与最大排队时间。`device_id=-1` 选择系统 Wave Mapper；也可提供实际设备的非负编号。FM 采用双声道，PSG 采用单声道，各自维持原采样率。

[`speakers.py`](speakers.py) 持有系统正在使用的缓冲区并处理归还。队列和样本容量用尽会返回明确错误。选择 `wav` 可将 FM 与 PSG 原速样本分开保存。
