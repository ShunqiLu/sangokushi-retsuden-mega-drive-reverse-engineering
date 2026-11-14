# YMFM audio bridge

[简体中文](README_YMFM.md) · [繁體中文](README_YMFM.zh-TW.md) · [日本語](README_YMFM.ja.md) · **English**

[`YmfmDevice`](ymfm_device.py) implements `FmPortDevice`. The Python driver handles scores, instrument patches, state, and register operations. External [YMFM](https://github.com/aaronsgiles/ymfm) sources provide YM2612 emulation; a separate device handles PSG.

## Build

Run from the Python source root. Supply a C++14 compiler compatible with GNU flags, a separately obtained compatible YMFM source root, and a fresh output directory. The YMFM root contains the upstream `LICENSE` and `src/`.

```powershell
$compiler = Read-Host 'C++14 g++ 或 clang++ 的路径'
$ymfmSource = Read-Host 'YMFM 源码根目录'
python -B -X utf8 -m tools.high_level_audio_engine.build_ymfm --compiler $compiler --ymfm-source $ymfmSource --output build/host-audio
```

The output is `g5510_ymfm.dll` on Windows and `libg5510_ymfm.so` elsewhere. It includes the upstream license and notices. Pass the library to `--chip-library` in the [desktop configuration](../reconstructed_game/README_LOCAL_CONFIG.en.md). YMFM uses the upstream [BSD 3-Clause license](https://github.com/aaronsgiles/ymfm/blob/main/LICENSE).

## Chip clocks and PCM

`YmfmDevice(library_path, clock_hz=..., pcm_sink=..., after_status_read=...)` takes an explicit library, input clock rate, and audio sink. The caller advances chip clocks with `advance(n)`. Status reads use the current timer and BUSY state. Events at the same time run in timer A, timer B, and native PCM order. One native YM2612 sample is produced every 144 input clocks. PCM is signed 16-bit interleaved stereo.
