# 配置函式入口採集

[简体中文](README_ENTRY_CAPTURE.md) · **繁體中文** · [日本語](README_ENTRY_CAPTURE.ja.md) · [English](README_ENTRY_CAPTURE.en.md)

入口採集供 [Python 版](../../../high_level/README.zh-TW.md)的桌面程式使用。執行時從已配置的會話採集選中的 68000 或 Z80 入口，並按指定額度寫入新的本地目錄。示例為 [68000 配置](examples/entry_capture.example.json)和[音訊配置](examples/entry_capture.audio.example.json)。

在 Python 版的本地執行副本中準備正常遊戲配置，再提供獨立的採集配置：

```powershell
python -B -m tools.reconstructed_game --config ./play.json --capture-entries ./entry-capture.json
```
