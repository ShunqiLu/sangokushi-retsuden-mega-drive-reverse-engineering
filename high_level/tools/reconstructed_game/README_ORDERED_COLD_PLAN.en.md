# Cold and warm restarts

[简体中文](README_ORDERED_COLD_PLAN.md) · [繁體中文](README_ORDERED_COLD_PLAN.zh-TW.md) · [日本語](README_ORDERED_COLD_PLAN.ja.md) · **English**

Ordered restart format `g5510-original-ordered-restart-plans-v2` contains `format` and `plans`. Each entry selects `kind` (`intro` or `narrative`) and `reset_path` (`warm` or `cold`). The actual game branch determines the restart path; the configuration supplies its bounded inputs.

| Field | Value |
| --- | --- |
| `reset_pulse_clocks` | Two entries for warm, three for cold; at least three clocks per entry. |
| `irq_clock_hz` | Positive integer frequency matching the driver. |
| `startup_im1_offsets` | Three strictly increasing positive integer offsets. |

A cold workspace copy uses `transfers.driver` permissions and `sound.max_DATA_operations` for byte reads and writes. Both count against session totals. Each cold workspace needs 8153 progressive copy operations and 16326 audio DATA operations. Driver startup and normal runtime use their own remaining allowances.

The [mixed path example](examples/ordered_restart_cold_plan.example.json) shows the format, and the [ordered restart guide](README_ORDERED_RESTARTS.en.md) shows how to enable it.
