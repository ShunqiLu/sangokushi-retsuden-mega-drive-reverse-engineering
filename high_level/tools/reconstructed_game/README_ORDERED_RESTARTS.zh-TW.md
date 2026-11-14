# 有序片頭與劇情復位

[简体中文](README_ORDERED_RESTARTS.md) · **繁體中文** · [日本語](README_ORDERED_RESTARTS.ja.md) · [English](README_ORDERED_RESTARTS.en.md)

前端透過 `--restarts` 提供一個有序的片頭及劇情復位計劃。應用依照實際的片頭 IRQ 跳轉和劇情跳轉消費 `plans`，保持同一存檔介質、場景和裝置所有權。

```powershell
python -m tools.reconstructed_game --config build/play-config.json --restarts restart-plan.json
```

計劃的 v1 格式宣告暖復位；v2 顯式支援 [`warm` 與 `cold`](README_ORDERED_COLD_PLAN.zh-TW.md)。`--restarts`、`--intro-restarts` 與 `--narrative-restarts` 三選一。透過 [`ordered_restart_config.py`](ordered_restart_config.py) 的 `load_ordered_restart_plans` 和 `enable_configured_ordered_restarts` 可從 Python 啟用。計劃在新會話開始時繫結，陣列順序和有限容量在會話中保持。

[暖復位示例](examples/ordered_restart_plan.example.json)和[混合復位示例](examples/ordered_restart_cold_plan.example.json)展示資料結構。
