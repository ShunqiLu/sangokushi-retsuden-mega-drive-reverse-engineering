# 冷复位与暖复位

有序复位格式 `g5510-original-ordered-restart-plans-v2` 包含 `format` 和 `plans`。每项选择 `kind`（`intro` 或 `narrative`）与 `reset_path`（`warm` 或 `cold`）。实际游戏分支决定复位路径；配置声明该路径所用的有限供应。

| 字段 | 值 |
| --- | --- |
| `reset_pulse_clocks` | 暖复位 2 项，冷复位 3 项；每项至少 3 个时钟。 |
| `irq_clock_hz` | 与实际驱动相符的正整数频率。 |
| `startup_im1_offsets` | 3 项严格递增的正整数偏移。 |

冷复位的 workspace 拷贝使用 `transfers.driver` 许可，字节读写使用 `sound.max_DATA_operations`。两项为会话累计容量。每次冷 workspace 需要 8153 次渐进拷贝和 16326 次音频 DATA 操作；驱动启动和通常运行消费各自的余量。

[混合路径示例](examples/ordered_restart_cold_plan.example.json)展示格式，[有序复位说明](README_ORDERED_RESTARTS.md)给出启用方法。
