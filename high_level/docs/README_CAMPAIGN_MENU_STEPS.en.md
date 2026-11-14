# Campaign menu and initialization

[简体中文](README_CAMPAIGN_MENU_STEPS.md) · [繁體中文](README_CAMPAIGN_MENU_STEPS.zh-TW.md) · [日本語](README_CAMPAIGN_MENU_STEPS.ja.md) · **English**

[`CampaignMenuScenePrograms`](../tools/high_level_gameplay_flow/campaign_menu_steps.py) implements the main flow's `0x0004B0` entry. It uses the current Scene and the parent's `0x0003CE` return address, joining controller setup, device waits, and scenario initialization into one cooperative call.

| Call entry / return site | Role |
| --- | --- |
| `0x00808A / 0x0522` | Queue the sound command and wait for BUSACK |
| `0x0305B0 / 0x0528` | Controller and new campaign menu |
| `0x006826 / 0x0532` | VRAM registers, plane initialization, and DMA |
| `0x03076E / 0x0538` | Apply menu selections |
| `0x003E54 / 0x0548` | Read the scenario descriptor |
| `0x009390 / 0x054E` | Initialize officer growth data |
| `0x0015BE / 0x0554` | Clamp the camera axes |

Each call handles the original CALL's physical return slot, partial register writes, and flags. The host supplies IRQ and device progression through the same persistent scene. See [Controller setup](README_CONTROLLER_MENU_STEPS.en.md) for lower-level cooperative entries.
