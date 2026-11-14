# 有限硬件输入与音频步进

[应用硬件输入示例](examples/application_hardware_inputs.json)演示有限的 VDP、控制器、DMA、BUSREQ、R 观测、FM／PSG 和启动事件。各容量使用对应设备的单位。示例中的时钟与输入是显式配置值，实际会话提供适用的设备供应。

[`audio_tick.py`](audio_tick.py) 的 `AudioTickSpec` 使用 `fm_ticks`、`psg_input_clocks`、`im1_grant` 和 `max_software_steps`。`im1_grant=None` 表示本次无音频中断。由应用的 `advance_audio_tick(spec)` 推进同一个声音驱动，使用其实际邮箱返回与 Timer A／B 处理点。

返回值含本次消费的有限过程。设备事件、采样率与响应供给均来自所选配置。[整帧计划](README_FRAME_PLAN.md)组织硬件、IRQ 与音频步进。
