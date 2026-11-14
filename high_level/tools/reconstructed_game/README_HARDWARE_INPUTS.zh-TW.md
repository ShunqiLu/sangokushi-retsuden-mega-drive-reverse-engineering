# 有限硬體輸入與音訊步進

[简体中文](README_HARDWARE_INPUTS.md) · **繁體中文** · [日本語](README_HARDWARE_INPUTS.ja.md) · [English](README_HARDWARE_INPUTS.en.md)

[應用硬體輸入示例](examples/application_hardware_inputs.json)演示有限的 VDP、控制器、DMA、BUSREQ、R 觀測、FM／PSG 和啟動事件。各容量使用對應裝置的單位。示例中的時鐘與輸入是顯式配置值，實際會話提供適用的裝置供應。

[`audio_tick.py`](audio_tick.py) 的 `AudioTickSpec` 使用 `fm_ticks`、`psg_input_clocks`、`im1_grant` 和 `max_software_steps`。`im1_grant=None` 表示本次無音訊中斷。由應用的 `advance_audio_tick(spec)` 推進同一個聲音驅動，使用其實際郵箱返回與 Timer A／B 處理點。

返回值含本次消費的有限過程。裝置事件、取樣率與響應供給均來自所選配置。[整幀計劃](README_FRAME_PLAN.zh-TW.md)組織硬體、IRQ 與音訊步進。
