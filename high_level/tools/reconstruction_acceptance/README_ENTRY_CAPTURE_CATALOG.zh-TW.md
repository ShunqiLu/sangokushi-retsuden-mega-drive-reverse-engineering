# 入口採集目錄

[简体中文](README_ENTRY_CAPTURE_CATALOG.md) · **繁體中文** · [日本語](README_ENTRY_CAPTURE_CATALOG.ja.md) · [English](README_ENTRY_CAPTURE_CATALOG.en.md)

[`load_capture_targets(batch, project_root)`](entry_capture_catalog.py) 從 `g5510-concentrated-explicit-input-batch-v1` 文件返回固定的 `CaptureTarget` 元組。目標透過原入口地址、Python 模組與函式名、幀型別和呼叫引數關聯當前宣告。

目錄裝載核對來源、精確標識與入口身份。現場資料由[入口監視器](README_ENTRY_MONITOR.zh-TW.md)在實際呼叫時記錄。
