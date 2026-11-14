# 有序片头与剧情复位

前端通过 `--restarts` 提供一个有序的片头及剧情复位计划。应用依照实际的片头 IRQ 跳转和剧情跳转消费 `plans`，保持同一存档介质、场景和设备所有权。

```powershell
python -m tools.reconstructed_game --config build/play-config.json --restarts restart-plan.json
```

计划的 v1 格式声明暖复位；v2 显式支持 [`warm` 与 `cold`](README_ORDERED_COLD_PLAN.md)。`--restarts`、`--intro-restarts` 与 `--narrative-restarts` 三选一。通过 [`ordered_restart_config.py`](ordered_restart_config.py) 的 `load_ordered_restart_plans` 和 `enable_configured_ordered_restarts` 可从 Python 启用。计划在新会话开始时绑定，数组顺序和有限容量在会话中保持。

[暖复位示例](examples/ordered_restart_plan.example.json)和[混合复位示例](examples/ordered_restart_cold_plan.example.json)展示数据结构。
