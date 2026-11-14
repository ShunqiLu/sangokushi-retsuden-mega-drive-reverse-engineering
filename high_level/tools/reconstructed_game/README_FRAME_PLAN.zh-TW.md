# 有限整幀計劃

[简体中文](README_FRAME_PLAN.md) · **繁體中文** · [日本語](README_FRAME_PLAN.ja.md) · [English](README_FRAME_PLAN.en.md)

執行配置的 `frontend` 選擇 `events` 或 `frame_plan`。控制檯使用 `frame_plan`；視窗支援兩個配置形狀。

| `frame_plan` 欄位 | 含義 |
| --- | --- |
| `max_frames` | 完整會話幀容量。 |
| `max_device_steps_per_frame` | 每幀共享的裝置推進上限。 |
| `irq_level`、`video` | IRQ 等級與該幀的影片匯流排狀態。 |
| `pad_changes`、`live_pad_ports` | 物理控制器輸入及允許互動的埠。 |
| `audio` | `fm_ticks`、`psg_input_clocks`、`max_software_steps`、`im1`。 |

音訊 `im1` 可為 `null` 或包含 `clock_hz`、`first_timestamp`、`timestamp_step` 的物件。第 n 幀的時間戳為 `first_timestamp + (n - 1) × timestamp_step`。晶片時鐘與視窗計時單獨配置。

[`FiniteFramePlan`](frame_plan.py) 使用同一應用推進必要的實際裝置事件，供給 IRQ 與物理輸入，並呼叫音訊步進。裝置事件、IRQ 和程式幀沿用各自的配置和實際剩餘容量。`extend_max_frames` 在現有幀額度正常用盡後擴大同一會話的總幀數。
