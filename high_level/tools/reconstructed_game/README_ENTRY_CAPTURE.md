# 可选入口采集

**简体中文** · [繁體中文](README_ENTRY_CAPTURE.zh-TW.md) · [日本語](README_ENTRY_CAPTURE.ja.md) · [English](README_ENTRY_CAPTURE.en.md)

`--capture-entries` 启用同一桌面会话中的源入口采集。采集配置与游戏配置分开。入口数据来自真实调用帧、物理返回槽、存储区与调用上下文；采集器以显式的文件数和空间容量保存记录。

```powershell
python -B -X utf8 -m tools.reconstructed_game --config build/play-config.json --capture-entries entry-capture.json
```

| 字段 | 作用 |
| --- | --- |
| `format` | 选择采集配置版本。 |
| `batch` | 提供入口批次的 JSON。 |
| `output` | 父目录存在的全新 `build/` 子目录。 |
| `tool_id` | 0–5 范围内实际可用的 Python 监视工具 ID。 |
| `max_cases`、`max_captures_per_entry` | 总记录与单入口记录上限。 |
| `max_total_bytes`、`max_case_json_bytes`、`min_free_bytes` | 总字节、单个 JSON 上限及保留空间。 |

基础格式为 `g5510-entry-capture-config-v1`；v2 通过 `audio` 声明 Z80 入口，v3 通过 `pre_call` 声明调用前采集，v4 的 `pre_call` 包含实际布尔值 `enabled` 和 `include_current_source_calls`。`batch` 和 `output` 的相对路径按采集配置文件位置解析。

[`entry_capture_config.py`](entry_capture_config.py) 管理配置和启停；[采集存储](../reconstruction_acceptance/README_ENTRY_CAPTURE_STORE.md)描述文件格式和容量。[M68K](../reconstruction_acceptance/README_M68K_ENTRY_CAPTURE.md)、[Z80](../reconstruction_acceptance/README_Z80_ENTRY_CAPTURE.md)和[调用前采集](../reconstruction_acceptance/README_M68K_PRE_CALL_CAPTURE.md)各有入口合同。
