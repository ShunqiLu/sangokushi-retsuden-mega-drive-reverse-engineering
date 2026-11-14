# 硬體輸入容量

[简体中文](README_HARDWARE_PROFILE.md) · **繁體中文** · [日本語](README_HARDWARE_PROFILE.ja.md) · [English](README_HARDWARE_PROFILE.en.md)

[`hardware_profile.py`](hardware_profile.py) 按明確的容量計劃從一份完整硬體 JSON 生成新的有限輸入配置。各項容量對應實際裝置量，例如 DMA 轉移單位、聲音 DATA 操作、驅動複製許可和 VBlank 邊沿。

```powershell
python -B -X utf8 -m tools.reconstructed_game.hardware_profile --project-root . --base-hardware tools/reconstructed_game/examples/application_hardware_inputs.json --capacity-plan tools/reconstructed_game/examples/hardware_capacity_8192.json --output build/gameplay-hardware.json
```

基線提供原物件結構和示例輸入；容量計劃獨立提供需要擴充套件的各項。輸出為新的有限配置。實際執行時間和事件順序由[幀計劃](README_FRAME_PLAN.zh-TW.md)與[硬體輸入契約](README_HARDWARE_INPUTS.zh-TW.md)決定。
