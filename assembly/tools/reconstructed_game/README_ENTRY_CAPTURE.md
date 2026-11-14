# 配置函数入口采集

**简体中文** · [繁體中文](README_ENTRY_CAPTURE.zh-TW.md) · [日本語](README_ENTRY_CAPTURE.ja.md) · [English](README_ENTRY_CAPTURE.en.md)

入口采集供 [Python 版](../../../high_level/README.md)的桌面程序使用。运行时从已配置的会话采集选中的 68000 或 Z80 入口，并按指定额度写入新的本地目录。示例为 [68000 配置](examples/entry_capture.example.json)和[音频配置](examples/entry_capture.audio.example.json)。

在 Python 版的本地运行副本中准备正常游戏配置，再提供独立的采集配置：

```powershell
python -B -m tools.reconstructed_game --config ./play.json --capture-entries ./entry-capture.json
```
