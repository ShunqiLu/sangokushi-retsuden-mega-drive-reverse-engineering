# YMFM 音訊橋

[简体中文](README_YMFM.md) · **繁體中文** · [日本語](README_YMFM.ja.md) · [English](README_YMFM.en.md)

[`YmfmDevice`](ymfm_device.py) 實現 `FmPortDevice`。遊戲的 Python 音訊驅動負責樂譜、音色、狀態和暫存器操作；外接 [YMFM](https://github.com/aaronsgiles/ymfm) 原始碼提供 YM2612 計算，PSG 使用單獨裝置。

## 建置

從 Python 版原始碼根執行。選擇現有 GNU 引數相容的 C++14 編譯器、單獨取得的相容 YMFM 原始碼根，以及新的輸出目錄。YMFM 根包含上游 `LICENSE` 和 `src/`。

```powershell
$compiler = Read-Host 'C++14 g++ 或 clang++ 的路径'
$ymfmSource = Read-Host 'YMFM 源码根目录'
python -B -X utf8 -m tools.high_level_audio_engine.build_ymfm --compiler $compiler --ymfm-source $ymfmSource --output build/host-audio
```

Windows 產物為 `g5510_ymfm.dll`，其他平臺的庫名為 `libg5510_ymfm.so`。輸出保留上游許可及說明。將庫檔案作為[桌面配置](../reconstructed_game/README_LOCAL_CONFIG.zh-TW.md)的 `--chip-library` 輸入。YMFM 遵循上游的 [BSD 3-Clause 許可證](https://github.com/aaronsgiles/ymfm/blob/main/LICENSE)。

## 晶片時鐘與 PCM

`YmfmDevice(library_path, clock_hz=..., pcm_sink=..., after_status_read=...)` 接受明確的庫、輸入時鐘和音訊接收器。呼叫方以 `advance(n)` 交付晶片時鐘；狀態讀取使用當前計時器和 BUSY 狀態。相同時刻按計時器 A、B、原生 PCM 的順序處理；每 144 個晶片輸入時鐘推進一個 YM2612 原生取樣。PCM 使用有符號 16 位交錯立體聲。
