# Windows スピーカー出力

[简体中文](README_SPEAKERS.md) · [繁體中文](README_SPEAKERS.zh-TW.md) · **日本語** · [English](README_SPEAKERS.en.md)

実行設定の `pcm_output.mode` で `speakers` を選ぶと、実際の FM と PSG を WinMM で再生します。チップのサンプルレートとゲームクロックはゲーム設定で決まります。

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

チップに合う FM・PSG のレート、セッションのサンプル容量、キューの最大時間を指定します。`device_id=-1` はシステムの Wave Mapper を選びます。実デバイスの非負の番号も指定できます。FM はステレオ、PSG はモノラルで、各レートは元のままです。

[`speakers.py`](speakers.py) はシステムが使用中のバッファーを保持し、返却を処理します。キューまたはサンプルの容量を使い切るとエラーを返します。`wav` を選ぶと FM と PSG を元のレートで別々に保存できます。
