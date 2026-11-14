# 桌面游戏应用

**简体中文** · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [English](README.en.md)

[`tools.reconstructed_game`](__main__.py) 使用同一游戏应用推进场景、输入、画面、音频和存档。图形窗口以 Tk 展示实际画面；控制台通过 JSON 行协议提供同一个可续接会话。

## 运行

[本地配置说明](README_LOCAL_CONFIG.md)列出源码目录、素材、程序数据、音频芯片库、设备供应和存档。使用准备好的配置启动：

```powershell
python -B -X utf8 -m tools.reconstructed_game --config build/play-config.json --frontend window
```

`--frontend console` 启用[控制台](README_CONSOLE.md)并要求完整帧计划。`--session-output` 指向配置根的 `build/` 内新的会话路径。

## 运行配置

- [应用接口与 PCM](README_APPLICATION.md)、[可选扬声器](README_SPEAKERS.md)。
- [完整帧计划](README_FRAME_PLAN.md)、[硬件输入](README_HARDWARE_INPUTS.md)、[有限输入配置](README_HARDWARE_PROFILE.md)。
- [节目与场景的有序复位](README_ORDERED_RESTARTS.md)、[冷／暖路径](README_ORDERED_COLD_PLAN.md)。
- [可选入口采集](README_ENTRY_CAPTURE.md)。

每个阶段消费配置声明的真实设备事件与数量。应用保留同一物理帧和存档介质；设备供应耗尽时返回对应的运行边界。
