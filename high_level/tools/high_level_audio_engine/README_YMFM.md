# YMFM 音频桥

[`YmfmDevice`](ymfm_device.py) 实现 `FmPortDevice`。游戏的 Python 音频驱动负责乐谱、音色、状态和寄存器操作；外置 [YMFM](https://github.com/aaronsgiles/ymfm) 源码提供 YM2612 计算，PSG 使用单独设备。

## 构建

从 Python 版源码根执行。选择现有 GNU 参数兼容的 C++14 编译器、单独取得的兼容 YMFM 源码根，以及新的输出目录。YMFM 根包含上游 `LICENSE` 和 `src/`。

```powershell
$compiler = Read-Host 'C++14 g++ 或 clang++ 的路径'
$ymfmSource = Read-Host 'YMFM 源码根目录'
python -B -X utf8 -m tools.high_level_audio_engine.build_ymfm --compiler $compiler --ymfm-source $ymfmSource --output build/host-audio
```

Windows 产物为 `g5510_ymfm.dll`，其他平台的库名为 `libg5510_ymfm.so`。输出保留上游许可及说明。将库文件作为[桌面配置](../reconstructed_game/README_LOCAL_CONFIG.md)的 `--chip-library` 输入。YMFM 遵循上游的 [BSD 3-Clause 许可证](https://github.com/aaronsgiles/ymfm/blob/main/LICENSE)。

## 芯片时钟与 PCM

`YmfmDevice(library_path, clock_hz=..., pcm_sink=..., after_status_read=...)` 接受明确的库、输入时钟和音频接收器。调用方以 `advance(n)` 交付芯片时钟；状态读取使用当前计时器和 BUSY 状态。相同时刻按计时器 A、B、原生 PCM 的顺序处理；每 144 个芯片输入时钟推进一个 YM2612 原生采样。PCM 使用有符号 16 位交错立体声。
