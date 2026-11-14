# 游戏应用接口

**简体中文** · [繁體中文](README_APPLICATION.zh-TW.md) · [日本語](README_APPLICATION.ja.md) · [English](README_APPLICATION.en.md)

[`GameApplication`](application.py) 持有同一 Scene、设备、场景续接和存档介质。窗口和[控制台](README_CONSOLE.md)以同一个应用 API 提供物理按键和有限事件。

完整 [`frontend.frame_plan`](README_FRAME_PLAN.md) 将设备事件、IRQ 和音频推进组织成一帧。运行边界保留最后的实际场景。`export_save` 导出当前 8192 字节介质；窗口截图由当前显存产生。

`pcm_output` 选择 `discard`、`wav` 或 Windows [`speakers`](README_SPEAKERS.md)。WAV 保存独立的 FM、PSG 输出；两种设备按各自的原采样格式和配置的容量产生样本。运行配置和构建输入见[本地配置](README_LOCAL_CONFIG.md)。
