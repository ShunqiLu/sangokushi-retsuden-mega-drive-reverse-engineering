# 生成 Z80 音訊程式資料

[简体中文](README_PORTABLE_BUILD.md) · **繁體中文** · [日本語](README_PORTABLE_BUILD.ja.md) · [English](README_PORTABLE_BUILD.en.md)

[`tools.high_level_audio_engine.build`](build.py) 使用本版本 Python 音訊驅動和顯式選擇的 GNU Z80 COFF 工具。選擇已存在的建置根和該根下新的輸出目錄。完整卡匣建置的 `audio_startup`、`audio_driver` 產物也可供桌面執行使用。

```powershell
$z80 = Read-Host 'Z80 COFF 交叉工具目录'
python -B -X utf8 -m tools.high_level_audio_engine.build --output-root build --output audio-native --tool-root $z80
```

獨立音訊建置生成歸一化原始碼、符號與 Z80 程式資料。桌面載入器接受與本版原始碼和音訊模組相符的一種建置形狀：完整映象輸出或歸一化音訊輸出。桌面路徑和晶片庫見[本地配置](../reconstructed_game/README_LOCAL_CONFIG.zh-TW.md)。
