# Ordered intro and scenario restarts

[简体中文](README_ORDERED_RESTARTS.md) · [繁體中文](README_ORDERED_RESTARTS.zh-TW.md) · [日本語](README_ORDERED_RESTARTS.ja.md) · **English**

The frontend supplies an ordered intro and scenario restart plan through `--restarts`. The application consumes `plans` at the actual intro IRQ and scenario jumps, keeping the same save, scene, and device ownership.

```powershell
python -m tools.reconstructed_game --config build/play-config.json --restarts restart-plan.json
```

Version 1 declares warm restarts. Version 2 explicitly supports [`warm` and `cold`](README_ORDERED_COLD_PLAN.en.md). Select exactly one of `--restarts`, `--intro-restarts`, or `--narrative-restarts`. From Python, use `load_ordered_restart_plans` and `enable_configured_ordered_restarts` in [`ordered_restart_config.py`](ordered_restart_config.py). The plan binds at the start of a new session and keeps its order and limits throughout.

See the [warm restart example](examples/ordered_restart_plan.example.json) and the [mixed restart example](examples/ordered_restart_cold_plan.example.json) for the data structure.
