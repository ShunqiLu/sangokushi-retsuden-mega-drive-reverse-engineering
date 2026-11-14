# 硬件输入容量

**简体中文** · [繁體中文](README_HARDWARE_PROFILE.zh-TW.md) · [日本語](README_HARDWARE_PROFILE.ja.md) · [English](README_HARDWARE_PROFILE.en.md)

[`hardware_profile.py`](hardware_profile.py) 按明确的容量计划从一份完整硬件 JSON 生成新的有限输入配置。各项容量对应实际设备量，例如 DMA 转移单位、声音 DATA 操作、驱动拷贝许可和 VBlank 边沿。

```powershell
python -B -X utf8 -m tools.reconstructed_game.hardware_profile --project-root . --base-hardware tools/reconstructed_game/examples/application_hardware_inputs.json --capacity-plan tools/reconstructed_game/examples/hardware_capacity_8192.json --output build/gameplay-hardware.json
```

基线提供原对象结构和示例输入；容量计划独立提供需要扩展的各项。输出为新的有限配置。实际运行时间和事件顺序由[帧计划](README_FRAME_PLAN.md)与[硬件输入契约](README_HARDWARE_INPUTS.md)决定。
