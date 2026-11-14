# 節奏通道的 Z80 WZ 狀態

[简体中文](README_RHYTHM_WZ.md) · **繁體中文** · [日本語](README_RHYTHM_WZ.ja.md) · [English](README_RHYTHM_WZ.en.md)

Z80 的 `BIT 2,(HL)` 使用內部 WZ 狀態形成未公開的標誌位。節奏邏輯透過 [`rhythm_wz.py`](rhythm_wz.py) 追蹤同一 Z80 狀態中的相關地址生產者，再將該狀態交給實際位檢查。聲音流程用原始埠、暫存器和裝置輸入維持該狀態。

WZ 由已知的原操作更新；初始狀態由帶有可觀察來源的執行環境提供。通道事件、計時和 IRQ 推進由聲音驅動與裝置提供器負責。
