# 节奏通道的 Z80 WZ 状态

**简体中文** · [繁體中文](README_RHYTHM_WZ.zh-TW.md) · [日本語](README_RHYTHM_WZ.ja.md) · [English](README_RHYTHM_WZ.en.md)

Z80 的 `BIT 2,(HL)` 使用内部 WZ 状态形成未公开的标志位。节奏逻辑通过 [`rhythm_wz.py`](rhythm_wz.py) 追踪同一 Z80 状态中的相关地址生产者，再将该状态交给实际位检查。声音流程用原始端口、寄存器和设备输入维持该状态。

WZ 由已知的原操作更新；初始状态由带有可观察来源的运行环境提供。通道事件、计时和 IRQ 推进由声音驱动与设备提供器负责。
