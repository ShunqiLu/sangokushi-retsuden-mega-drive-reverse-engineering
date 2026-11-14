# Windows 揚聲器輸出

[简体中文](README_SPEAKERS.md) · **繁體中文** · [日本語](README_SPEAKERS.ja.md) · [English](README_SPEAKERS.en.md)

執行配置的 `pcm_output.mode` 可選擇 `speakers`，由 WinMM 播放實際的 FM 與 PSG 輸出。晶片的取樣率和遊戲時鐘仍由遊戲配置決定。

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

填寫與當前晶片相符的 FM、PSG 取樣率，以及會話的樣本容量與最大排隊時間。`device_id=-1` 選擇系統 Wave Mapper；也可提供實際裝置的非負編號。FM 採用雙聲道，PSG 採用單聲道，各自維持原取樣率。

[`speakers.py`](speakers.py) 持有系統正在使用的緩衝區並處理歸還。佇列和樣本容量用盡會返回明確錯誤。選擇 `wav` 可將 FM 與 PSG 原速樣本分開儲存。
