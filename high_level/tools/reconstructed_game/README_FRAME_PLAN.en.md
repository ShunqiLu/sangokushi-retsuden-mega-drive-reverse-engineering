# Full frame plan

[简体中文](README_FRAME_PLAN.md) · [繁體中文](README_FRAME_PLAN.zh-TW.md) · [日本語](README_FRAME_PLAN.ja.md) · **English**

The runtime configuration's `frontend` selects `events` or `frame_plan`. The console uses `frame_plan`; the window supports both forms.

| `frame_plan` field | Meaning |
| --- | --- |
| `max_frames` | Frame allowance for the whole session. |
| `max_device_steps_per_frame` | Shared device progression limit per frame. |
| `irq_level`, `video` | IRQ level and video bus state for that frame. |
| `pad_changes`, `live_pad_ports` | Physical controller input and interactive ports. |
| `audio` | `fm_ticks`、`psg_input_clocks`、`max_software_steps`、`im1`。 |

Audio `im1` is `null` or an object with `clock_hz`, `first_timestamp`, and `timestamp_step`. The timestamp for frame n is `first_timestamp + (n - 1) × timestamp_step`. Chip clocks and window timing are configured separately.

[`FiniteFramePlan`](frame_plan.py) advances real device events, supplies IRQ and physical inputs, and steps audio in the same application. Device events, IRQ, and program frames use their respective configuration and remaining allowance. `extend_max_frames` increases the total frame allowance of the same session after it is used up normally.
