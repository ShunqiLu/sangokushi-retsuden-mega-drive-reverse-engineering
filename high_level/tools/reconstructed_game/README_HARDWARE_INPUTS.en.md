# Hardware inputs and audio stepping

[简体中文](README_HARDWARE_INPUTS.md) · [繁體中文](README_HARDWARE_INPUTS.zh-TW.md) · [日本語](README_HARDWARE_INPUTS.ja.md) · **English**

The [application hardware example](examples/application_hardware_inputs.json) shows finite inputs for VDP, controllers, DMA, BUSREQ, R observations, FM/PSG, and startup events. Limits use each device's units. The example sets explicit clocks and inputs; a real session supplies values appropriate to its devices.

The `AudioTickSpec` method of [`audio_tick.py`](audio_tick.py) takes `fm_ticks`, `psg_input_clocks`, `im1_grant`, and `max_software_steps`. `im1_grant=None` means no audio interrupt for the step. The application's `advance_audio_tick(spec)` advances the same sound driver, using its actual mailbox returns and timer A/B handling points.

The return value records what the step consumed. Device events, sample rates, and responses come from the selected configuration. The [full frame plan](README_FRAME_PLAN.en.md) coordinates hardware, IRQ, and audio stepping.
