# 生成 Z80 音频程序数据

[`tools.high_level_audio_engine.build`](build.py) 使用本版本 Python 音频驱动和显式选择的 GNU Z80 COFF 工具。选择已存在的构建根和该根下新的输出目录。完整卡带构建的 `audio_startup`、`audio_driver` 产物也可供桌面运行使用。

```powershell
$z80 = Read-Host 'Z80 COFF 交叉工具目录'
python -B -X utf8 -m tools.high_level_audio_engine.build --output-root build --output audio-native --tool-root $z80
```

独立音频构建生成归一化源码、符号与 Z80 程序数据。桌面加载器接受与本版源码和音频模块相符的一种构建形状：完整镜像输出或归一化音频输出。桌面路径和芯片库见[本地配置](../reconstructed_game/README_LOCAL_CONFIG.md)。
