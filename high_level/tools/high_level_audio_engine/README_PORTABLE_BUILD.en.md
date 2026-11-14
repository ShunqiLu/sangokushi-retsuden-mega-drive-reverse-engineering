# Z80 audio program build

[简体中文](README_PORTABLE_BUILD.md) · [繁體中文](README_PORTABLE_BUILD.zh-TW.md) · [日本語](README_PORTABLE_BUILD.ja.md) · **English**

[`tools.high_level_audio_engine.build`](build.py) uses this edition's Python sound driver and explicitly selected GNU Z80 COFF tools. Choose an existing build root and a new output directory beneath it. The `audio_startup` and `audio_driver` artifacts from a full cartridge build also work with desktop mode.

```powershell
$z80 = Read-Host 'Z80 COFF 交叉工具目录'
python -B -X utf8 -m tools.high_level_audio_engine.build --output-root build --output audio-native --tool-root $z80
```

The standalone sound build produces normalized sources, symbols, and Z80 program data. The desktop loader accepts either a full image build or normalized audio output, matched to this edition's sources and audio modules. See [Local configuration](../reconstructed_game/README_LOCAL_CONFIG.en.md) for paths and the chip library.
