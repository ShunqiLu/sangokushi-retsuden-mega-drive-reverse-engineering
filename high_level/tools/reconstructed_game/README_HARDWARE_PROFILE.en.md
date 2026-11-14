# Hardware input capacity

[简体中文](README_HARDWARE_PROFILE.md) · [繁體中文](README_HARDWARE_PROFILE.zh-TW.md) · [日本語](README_HARDWARE_PROFILE.ja.md) · **English**

[`hardware_profile.py`](hardware_profile.py) takes complete hardware JSON and a capacity plan, then writes a new bounded input configuration. Limits count real device units, such as DMA transfers, audio DATA operations, driver copy permissions, and VBlank edges.

```powershell
python -B -X utf8 -m tools.reconstructed_game.hardware_profile --project-root . --base-hardware tools/reconstructed_game/examples/application_hardware_inputs.json --capacity-plan tools/reconstructed_game/examples/hardware_capacity_8192.json --output build/gameplay-hardware.json
```

The baseline supplies the original structure and sample inputs. The capacity plan supplies the increases. The result is a new bounded configuration. Timing and event order follow the [frame plan](README_FRAME_PLAN.en.md) and [hardware input contract](README_HARDWARE_INPUTS.en.md).
