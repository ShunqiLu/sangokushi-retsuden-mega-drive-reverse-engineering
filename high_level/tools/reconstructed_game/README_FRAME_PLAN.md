# 有限整帧计划

**简体中文** · [繁體中文](README_FRAME_PLAN.zh-TW.md) · [日本語](README_FRAME_PLAN.ja.md) · [English](README_FRAME_PLAN.en.md)

运行配置的 `frontend` 选择 `events` 或 `frame_plan`。控制台使用 `frame_plan`；窗口支持两个配置形状。

| `frame_plan` 字段 | 含义 |
| --- | --- |
| `max_frames` | 完整会话帧容量。 |
| `max_device_steps_per_frame` | 每帧共享的设备推进上限。 |
| `irq_level`、`video` | IRQ 等级与该帧的视频总线状态。 |
| `pad_changes`、`live_pad_ports` | 物理控制器输入及允许交互的端口。 |
| `audio` | `fm_ticks`、`psg_input_clocks`、`max_software_steps`、`im1`。 |

音频 `im1` 可为 `null` 或包含 `clock_hz`、`first_timestamp`、`timestamp_step` 的对象。第 n 帧的时间戳为 `first_timestamp + (n - 1) × timestamp_step`。芯片时钟与窗口计时单独配置。

[`FiniteFramePlan`](frame_plan.py) 使用同一应用推进必要的实际设备事件，供给 IRQ 与物理输入，并调用音频步进。设备事件、IRQ 和程序帧沿用各自的配置和实际剩余容量。`extend_max_frames` 在现有帧额度正常用尽后扩大同一会话的总帧数。
